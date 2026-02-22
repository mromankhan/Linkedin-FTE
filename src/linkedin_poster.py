"""
LinkedIn UGC Posts API — Supports text, image, and carousel/document posts.
"""

import os
import json
import logging
import mimetypes
from datetime import date, datetime
from pathlib import Path
import requests
from dotenv import load_dotenv
from linkedin_auth import LinkedInAuth

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
MAX_POSTS_PER_DAY = int(os.getenv("MAX_POSTS_PER_DAY", "3"))
VAULT_PATH = Path(os.getenv("VAULT_PATH", "vault"))
LOGS_DIR = VAULT_PATH / "Logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

UPLOAD_URL = "https://api.linkedin.com/v2/assets?action=registerUpload"
UGC_URL = "https://api.linkedin.com/v2/ugcPosts"


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def get_todays_post_count() -> int:
    log_file = LOGS_DIR / f"{date.today().isoformat()}.json"
    if not log_file.exists():
        return 0
    entries = json.loads(log_file.read_text(encoding="utf-8"))
    return sum(1 for e in entries if e.get("action_type") == "linkedin_post" and e.get("result") == "success")


def log_action(action_type: str, parameters: dict, result: str, post_urn: str = "") -> None:
    log_file = LOGS_DIR / f"{date.today().isoformat()}.json"
    entries = []
    if log_file.exists():
        entries = json.loads(log_file.read_text(encoding="utf-8"))
    entries.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action_type": action_type,
        "actor": "linkedin_fte",
        "parameters": parameters,
        "post_urn": post_urn,
        "dry_run": DRY_RUN,
        "result": result,
    })
    log_file.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def build_post_text(content: str, hashtags: list[str]) -> str:
    tags_str = " ".join(f"#{tag.lstrip('#')}" for tag in hashtags)
    return f"{content.strip()}\n\n{tags_str}"


def _rate_limit_check(params: dict) -> dict | None:
    """Returns error dict if rate limit hit, else None."""
    count = get_todays_post_count()
    if count >= MAX_POSTS_PER_DAY:
        msg = f"Rate limit reached: {count}/{MAX_POSTS_PER_DAY} posts today."
        logger.warning(msg)
        log_action("linkedin_post", params, "rate_limited")
        return {"success": False, "post_urn": "", "message": msg}
    return None


# ─────────────────────────────────────────────
# Asset Upload (used for both image and document)
# ─────────────────────────────────────────────

def _register_upload(auth: LinkedInAuth, person_urn: str, recipe: str) -> tuple[str, str]:
    """
    Register an asset upload with LinkedIn.
    recipe: 'feedshare-image' or 'feedshare-document'
    Returns: (asset_urn, upload_url)
    """
    payload = {
        "registerUploadRequest": {
            "recipes": [f"urn:li:digitalmediaRecipe:{recipe}"],
            "owner": person_urn,
            "serviceRelationships": [{
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }]
        }
    }
    resp = requests.post(UPLOAD_URL, headers=auth.get_headers(), json=payload, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    asset_urn = data["value"]["asset"]
    upload_url = data["value"]["uploadMechanism"][
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ]["uploadUrl"]
    return asset_urn, upload_url


def _upload_binary(upload_url: str, file_path: Path, content_type: str) -> None:
    """PUT the binary file to LinkedIn's upload URL."""
    with open(file_path, "rb") as f:
        data = f.read()
    resp = requests.put(
        upload_url,
        data=data,
        headers={"Content-Type": content_type},
        timeout=60,
    )
    resp.raise_for_status()


def upload_media(auth: LinkedInAuth, person_urn: str, file_path: Path) -> str:
    """
    Upload an image or PDF to LinkedIn.
    Returns the asset URN to embed in ugcPost.
    """
    suffix = file_path.suffix.lower()
    if suffix in (".jpg", ".jpeg", ".png", ".gif"):
        recipe = "feedshare-image"
        content_type = mimetypes.guess_type(str(file_path))[0] or "image/jpeg"
    elif suffix == ".pdf":
        recipe = "feedshare-document"
        content_type = "application/pdf"
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Use .jpg .png .gif or .pdf")

    logger.info(f"[Poster] Registering upload: {file_path.name} ({recipe})")
    asset_urn, upload_url = _register_upload(auth, person_urn, recipe)

    logger.info(f"[Poster] Uploading binary...")
    _upload_binary(upload_url, file_path, content_type)

    logger.info(f"[Poster] Upload complete. Asset URN: {asset_urn}")
    return asset_urn


# ─────────────────────────────────────────────
# Post builders
# ─────────────────────────────────────────────

def _build_text_payload(person_urn: str, post_text: str) -> dict:
    return {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }


def _build_image_payload(person_urn: str, post_text: str, asset_urn: str, title: str = "") -> dict:
    return {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "IMAGE",
                "media": [{
                    "status": "READY",
                    "media": asset_urn,
                    "title": {"text": title or ""},
                }]
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }


def _build_carousel_payload(person_urn: str, post_text: str, asset_urn: str, title: str = "") -> dict:
    return {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "DOCUMENT",
                "media": [{
                    "status": "READY",
                    "media": asset_urn,
                    "title": {"text": title or "Carousel"},
                }]
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }


# ─────────────────────────────────────────────
# Main posting functions
# ─────────────────────────────────────────────

def post_to_linkedin(content: str, hashtags: list[str], source_file: str = "") -> dict:
    """Text-only post."""
    post_text = build_post_text(content, hashtags)
    params = {"type": "text", "source_file": source_file, "char_count": len(post_text)}

    if err := _rate_limit_check(params):
        return err

    if DRY_RUN:
        logger.info("[DRY RUN] TEXT POST — Would post to LinkedIn:")
        logger.info("-" * 60)
        logger.info(post_text)
        logger.info("-" * 60)
        log_action("linkedin_post", params, "dry_run")
        return {"success": True, "post_urn": "dry-run-urn", "message": "Dry run — no real post made."}

    try:
        auth = LinkedInAuth()
        person_urn = auth.get_profile_urn()
        payload = _build_text_payload(person_urn, post_text)
        resp = requests.post(UGC_URL, headers=auth.get_headers(), json=payload, timeout=15)
        resp.raise_for_status()
        post_urn = resp.headers.get("x-restli-id", "")
        logger.info(f"[Poster] Text post published! URN: {post_urn}")
        log_action("linkedin_post", params, "success", post_urn)
        return {"success": True, "post_urn": post_urn, "message": "Text post published!"}
    except Exception as e:
        msg = str(e)
        logger.error(f"[Poster] Error: {msg}")
        log_action("linkedin_post", params, f"error: {msg}")
        return {"success": False, "post_urn": "", "message": msg}


def post_image_to_linkedin(
    content: str,
    hashtags: list[str],
    image_path: str,
    image_title: str = "",
    source_file: str = "",
) -> dict:
    """Post with a single image."""
    post_text = build_post_text(content, hashtags)
    params = {"type": "image", "source_file": source_file, "image": image_path}

    if err := _rate_limit_check(params):
        return err

    if DRY_RUN:
        logger.info("[DRY RUN] IMAGE POST — Would post to LinkedIn:")
        logger.info(f"  Image: {image_path}")
        logger.info("-" * 60)
        logger.info(post_text)
        logger.info("-" * 60)
        log_action("linkedin_post", params, "dry_run")
        return {"success": True, "post_urn": "dry-run-urn", "message": "Dry run — image post simulated."}

    try:
        auth = LinkedInAuth()
        person_urn = auth.get_profile_urn()
        asset_urn = upload_media(auth, person_urn, Path(image_path))
        payload = _build_image_payload(person_urn, post_text, asset_urn, image_title)
        resp = requests.post(UGC_URL, headers=auth.get_headers(), json=payload, timeout=15)
        resp.raise_for_status()
        post_urn = resp.headers.get("x-restli-id", "")
        logger.info(f"[Poster] Image post published! URN: {post_urn}")
        log_action("linkedin_post", params, "success", post_urn)
        return {"success": True, "post_urn": post_urn, "message": "Image post published!"}
    except Exception as e:
        msg = str(e)
        logger.error(f"[Poster] Error: {msg}")
        log_action("linkedin_post", params, f"error: {msg}")
        return {"success": False, "post_urn": "", "message": msg}


def post_carousel_to_linkedin(
    content: str,
    hashtags: list[str],
    pdf_path: str,
    carousel_title: str = "",
    source_file: str = "",
) -> dict:
    """Post a carousel (PDF — each page = one slide)."""
    post_text = build_post_text(content, hashtags)
    params = {"type": "carousel", "source_file": source_file, "pdf": pdf_path}

    if err := _rate_limit_check(params):
        return err

    if DRY_RUN:
        logger.info("[DRY RUN] CAROUSEL POST — Would post to LinkedIn:")
        logger.info(f"  PDF: {pdf_path}")
        logger.info("-" * 60)
        logger.info(post_text)
        logger.info("-" * 60)
        log_action("linkedin_post", params, "dry_run")
        return {"success": True, "post_urn": "dry-run-urn", "message": "Dry run — carousel post simulated."}

    try:
        auth = LinkedInAuth()
        person_urn = auth.get_profile_urn()
        asset_urn = upload_media(auth, person_urn, Path(pdf_path))
        payload = _build_carousel_payload(person_urn, post_text, asset_urn, carousel_title)
        resp = requests.post(UGC_URL, headers=auth.get_headers(), json=payload, timeout=15)
        resp.raise_for_status()
        post_urn = resp.headers.get("x-restli-id", "")
        logger.info(f"[Poster] Carousel post published! URN: {post_urn}")
        log_action("linkedin_post", params, "success", post_urn)
        return {"success": True, "post_urn": post_urn, "message": "Carousel post published!"}
    except Exception as e:
        msg = str(e)
        logger.error(f"[Poster] Error: {msg}")
        log_action("linkedin_post", params, f"error: {msg}")
        return {"success": False, "post_urn": "", "message": msg}
