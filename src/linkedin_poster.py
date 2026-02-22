"""
LinkedIn UGC Posts API — Post creator with dry-run and rate limiting.
"""

import os
import json
import logging
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


def get_todays_post_count() -> int:
    """Count how many posts were made today from the log."""
    log_file = LOGS_DIR / f"{date.today().isoformat()}.json"
    if not log_file.exists():
        return 0
    entries = json.loads(log_file.read_text(encoding="utf-8"))
    return sum(1 for e in entries if e.get("action_type") == "linkedin_post" and e.get("result") == "success")


def log_action(action_type: str, parameters: dict, result: str, post_urn: str = "") -> None:
    """Append a structured log entry to today's log file."""
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
    """Combine content and hashtags into final post text."""
    tags_str = " ".join(f"#{tag.lstrip('#')}" for tag in hashtags)
    return f"{content.strip()}\n\n{tags_str}"


def post_to_linkedin(content: str, hashtags: list[str], source_file: str = "") -> dict:
    """
    Post to LinkedIn. Respects DRY_RUN and MAX_POSTS_PER_DAY.

    Returns:
        dict with keys: success (bool), post_urn (str), message (str)
    """
    post_text = build_post_text(content, hashtags)
    params = {"source_file": source_file, "hashtags": hashtags, "char_count": len(post_text)}

    # Rate limit check
    todays_count = get_todays_post_count()
    if todays_count >= MAX_POSTS_PER_DAY:
        msg = f"Rate limit reached: {todays_count}/{MAX_POSTS_PER_DAY} posts today."
        logger.warning(msg)
        log_action("linkedin_post", params, "rate_limited")
        return {"success": False, "post_urn": "", "message": msg}

    # Dry run mode
    if DRY_RUN:
        logger.info("[DRY RUN] Would post to LinkedIn:")
        logger.info("-" * 60)
        logger.info(post_text)
        logger.info("-" * 60)
        log_action("linkedin_post", params, "dry_run")
        return {"success": True, "post_urn": "dry-run-urn", "message": "Dry run — no real post made."}

    # Real post
    try:
        auth = LinkedInAuth()
        person_urn = auth.get_profile_urn()

        payload = {
            "author": person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": post_text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }

        response = requests.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers=auth.get_headers(),
            json=payload,
            timeout=15,
        )
        response.raise_for_status()

        post_urn = response.headers.get("x-restli-id", "")
        logger.info(f"[Poster] Post published! URN: {post_urn}")
        log_action("linkedin_post", params, "success", post_urn)
        return {"success": True, "post_urn": post_urn, "message": "Post published successfully!"}

    except requests.HTTPError as e:
        msg = f"LinkedIn API error: {e.response.status_code} — {e.response.text}"
        logger.error(msg)
        log_action("linkedin_post", params, f"error: {msg}")
        return {"success": False, "post_urn": "", "message": msg}

    except Exception as e:
        msg = f"Unexpected error: {e}"
        logger.error(msg)
        log_action("linkedin_post", params, f"error: {msg}")
        return {"success": False, "post_urn": "", "message": msg}


if __name__ == "__main__":
    # Quick test
    result = post_to_linkedin(
        content="This is a test post from my LinkedIn FTE.\n\nBuilding AI agents that work 24/7 so you don't have to.",
        hashtags=["AI", "Automation", "Tech", "SoftwareDevelopment"],
        source_file="manual_test",
    )
    print(result)
