"""
Approval Watcher — monitors /vault/Approved/ for post files.
When a file appears, parses it and triggers LinkedIn posting.
"""

import os
import re
import shutil
import logging
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

VAULT_PATH = Path(os.getenv("VAULT_PATH", "vault"))
APPROVED_DIR = VAULT_PATH / "Approved"
PUBLISHED_DIR = VAULT_PATH / "Published"
NEEDS_ACTION_DIR = VAULT_PATH / "Needs_Action"
DASHBOARD_FILE = VAULT_PATH / "Dashboard.md"


def parse_post_file(filepath: Path) -> dict:
    """
    Parse a markdown post file with YAML frontmatter.
    Returns dict with keys: type, topic, content, hashtags, pdf_path, image_path
    """
    text = filepath.read_text(encoding="utf-8")

    # Extract frontmatter between --- delimiters
    fm_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    frontmatter = {}
    if fm_match:
        for line in fm_match.group(1).splitlines():
            if ":" in line:
                key, _, val = line.partition(":")
                frontmatter[key.strip()] = val.strip()

    # Post type: text | image | carousel
    post_type = frontmatter.get("type", "text")

    # Extract caption/content
    # For carousels it's under "## Post Caption", for others "## Post Content"
    content_match = re.search(
        r"## Post (?:Content|Caption)\n\n(.*?)(?=\n## |\Z)", text, re.DOTALL
    )
    content = content_match.group(1).strip() if content_match else ""

    # Extract hashtags from frontmatter or from post
    raw_hashtags = frontmatter.get("hashtags", "")
    hashtags = [h.strip().lstrip("#") for h in raw_hashtags.split(",") if h.strip()]

    return {
        "type": post_type,
        "topic": frontmatter.get("topic", "Unknown"),
        "content": content,
        "hashtags": hashtags,
        "pdf_path": frontmatter.get("pdf_path", ""),
        "image_path": frontmatter.get("image_path", ""),
        "best_time": frontmatter.get("best_time", ""),
    }


def update_dashboard(topic: str, status: str, post_urn: str = "") -> None:
    """Append a row to the Dashboard's activity table."""
    if not DASHBOARD_FILE.exists():
        return

    text = DASHBOARD_FILE.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_row = f"| {today} | {topic[:40]} | {status} | — | — |"

    # Insert after the table header separator line
    text = re.sub(
        r"(\| Date \| Post Topic \| Status \| Likes \| Comments \|\n\|[-| ]+\|)\n",
        rf"\1\n{new_row}\n",
        text,
    )
    # Update "Last Updated"
    text = re.sub(r"- \*\*Last Updated:\*\* .*", f"- **Last Updated:** {today}", text)

    DASHBOARD_FILE.write_text(text, encoding="utf-8")


class ApprovalHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filepath = Path(event.src_path)
        if filepath.suffix != ".md":
            return

        logger.info(f"[Watcher] Approved file detected: {filepath.name}")
        self._process_post(filepath)

    def _process_post(self, filepath: Path) -> None:
        from linkedin_poster import (
            post_to_linkedin,
            post_image_to_linkedin,
            post_carousel_to_linkedin,
        )

        try:
            parsed = parse_post_file(filepath)
            post_type = parsed.get("type", "text")

            if not parsed["content"]:
                logger.warning(f"[Watcher] No content found in {filepath.name}, skipping.")
                return

            # Route to correct poster based on type
            if post_type == "image":
                image_path = parsed["image_path"]
                if not image_path or not Path(image_path).exists():
                    logger.error(f"[Watcher] Image not found: {image_path}")
                    update_dashboard(parsed["topic"], "❌ Image not found")
                    return
                result = post_image_to_linkedin(
                    content=parsed["content"],
                    hashtags=parsed["hashtags"],
                    image_path=image_path,
                    image_title=parsed["topic"],
                    source_file=filepath.name,
                )

            elif post_type == "carousel":
                pdf_path = parsed["pdf_path"]
                if not pdf_path or not Path(pdf_path).exists():
                    logger.error(f"[Watcher] PDF not found: {pdf_path}")
                    update_dashboard(parsed["topic"], "❌ PDF not found")
                    return
                result = post_carousel_to_linkedin(
                    content=parsed["content"],
                    hashtags=parsed["hashtags"],
                    pdf_path=pdf_path,
                    carousel_title=parsed["topic"],
                    source_file=filepath.name,
                )
                # Move PDF to Published too
                if result["success"]:
                    pdf_src = Path(pdf_path)
                    if pdf_src.exists():
                        shutil.move(str(pdf_src), str(PUBLISHED_DIR / pdf_src.name))

            else:
                result = post_to_linkedin(
                    content=parsed["content"],
                    hashtags=parsed["hashtags"],
                    source_file=filepath.name,
                )

            type_label = {"image": "🖼️ Image", "carousel": "📊 Carousel"}.get(post_type, "📝 Text")

            if result["success"]:
                dest = PUBLISHED_DIR / filepath.name
                shutil.move(str(filepath), str(dest))
                logger.info(f"[Watcher] Moved to Published: {filepath.name}")
                update_dashboard(parsed["topic"], f"✅ {type_label} Published", result["post_urn"])
            else:
                error_note = NEEDS_ACTION_DIR / f"ERROR_{filepath.name}"
                filepath.rename(error_note)
                error_note.write_text(
                    error_note.read_text(encoding="utf-8")
                    + f"\n\n## Error\n{result['message']}\n",
                    encoding="utf-8",
                )
                logger.error(f"[Watcher] Posting failed, moved to Needs_Action: {filepath.name}")
                update_dashboard(parsed["topic"], "❌ Failed")

        except Exception as e:
            logger.error(f"[Watcher] Error processing {filepath.name}: {e}")


def run():
    APPROVED_DIR.mkdir(parents=True, exist_ok=True)
    PUBLISHED_DIR.mkdir(parents=True, exist_ok=True)
    NEEDS_ACTION_DIR.mkdir(parents=True, exist_ok=True)

    observer = Observer()
    handler = ApprovalHandler()
    observer.schedule(handler, str(APPROVED_DIR), recursive=False)
    observer.start()

    logger.info(f"[Watcher] Watching: {APPROVED_DIR}")
    logger.info("[Watcher] Move .md files to /Approved/ to trigger posting.")

    try:
        import time
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("[Watcher] Stopped.")
    observer.join()


if __name__ == "__main__":
    run()
