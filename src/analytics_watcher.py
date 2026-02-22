"""
Analytics Watcher — fetches LinkedIn post metrics and generates weekly reports.
Run manually or scheduled via orchestrator every Sunday at 8 PM.
"""

import os
import json
import logging
from datetime import date, datetime, timedelta
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

VAULT_PATH = Path(os.getenv("VAULT_PATH", "vault"))
PUBLISHED_DIR = VAULT_PATH / "Published"
ANALYTICS_DIR = VAULT_PATH / "Analytics"
LOGS_DIR = VAULT_PATH / "Logs"
ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"


def get_published_urns_from_logs() -> list[dict]:
    """
    Read all log files from the past 7 days and extract successful post URNs.
    Returns list of dicts: {post_urn, timestamp, topic}
    """
    posts = []
    today = date.today()
    for i in range(7):
        day = today - timedelta(days=i)
        log_file = LOGS_DIR / f"{day.isoformat()}.json"
        if not log_file.exists():
            continue
        entries = json.loads(log_file.read_text(encoding="utf-8"))
        for entry in entries:
            if entry.get("action_type") == "linkedin_post" and entry.get("result") == "success":
                if entry.get("post_urn") and entry["post_urn"] != "dry-run-urn":
                    posts.append({
                        "post_urn": entry["post_urn"],
                        "timestamp": entry.get("timestamp", ""),
                        "source_file": entry.get("parameters", {}).get("source_file", ""),
                    })
    return posts


def fetch_post_metrics(auth_headers: dict, post_urn: str) -> dict:
    """Fetch likes, comments, shares for a given post URN."""
    encoded_urn = post_urn.replace(":", "%3A").replace(",", "%2C")
    url = f"https://api.linkedin.com/v2/socialMetadata/{encoded_urn}"
    try:
        resp = requests.get(url, headers=auth_headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "likes": data.get("likesSummary", {}).get("totalLikes", 0),
                "comments": data.get("commentsSummary", {}).get("totalFirstLevelComments", 0),
                "shares": data.get("sharesSummary", {}).get("totalShares", 0),
            }
    except Exception as e:
        logger.warning(f"Could not fetch metrics for {post_urn}: {e}")
    return {"likes": 0, "comments": 0, "shares": 0}


def fetch_follower_count(auth_headers: dict, person_urn: str) -> int:
    """Fetch current follower/connection count."""
    encoded = person_urn.replace(":", "%3A")
    url = f"https://api.linkedin.com/v2/networkSizes/{encoded}?edgeType=CompanyFollowedByMember"
    try:
        resp = requests.get(url, headers=auth_headers, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("firstDegreeSize", 0)
    except Exception as e:
        logger.warning(f"Could not fetch follower count: {e}")
    return 0


def generate_weekly_report() -> Path:
    """
    Fetch metrics for all posts from the last 7 days.
    Generate a markdown report and save to /Analytics/.
    """
    from linkedin_auth import LinkedInAuth

    report_date = date.today().isoformat()
    week_start = (date.today() - timedelta(days=7)).isoformat()
    report_file = ANALYTICS_DIR / f"Weekly_Report_{report_date}.md"

    if DRY_RUN:
        logger.info("[Analytics] DRY RUN — generating sample report with mock data.")
        posts_data = [
            {"source_file": "POST_sample_1.md", "likes": 42, "comments": 8, "shares": 5},
            {"source_file": "POST_sample_2.md", "likes": 28, "comments": 3, "shares": 2},
            {"source_file": "POST_sample_3.md", "likes": 67, "comments": 15, "shares": 9},
        ]
        total_likes = sum(p["likes"] for p in posts_data)
        total_comments = sum(p["comments"] for p in posts_data)
        total_shares = sum(p["shares"] for p in posts_data)
        best_post = max(posts_data, key=lambda p: p["likes"])
        follower_count = "—"
    else:
        auth = LinkedInAuth()
        headers = auth.get_headers()
        person_urn = auth.get_profile_urn()
        follower_count = fetch_follower_count(headers, person_urn)

        published_posts = get_published_urns_from_logs()
        posts_data = []
        for post in published_posts:
            metrics = fetch_post_metrics(headers, post["post_urn"])
            metrics["source_file"] = post["source_file"]
            posts_data.append(metrics)

        if not posts_data:
            logger.info("[Analytics] No published posts found in the last 7 days.")
            posts_data = []

        total_likes = sum(p["likes"] for p in posts_data)
        total_comments = sum(p["comments"] for p in posts_data)
        total_shares = sum(p["shares"] for p in posts_data)
        best_post = max(posts_data, key=lambda p: p["likes"]) if posts_data else {}

    # Build post rows for table
    rows = ""
    for p in posts_data:
        rows += f"| {p['source_file'][:45]} | {p['likes']} | {p['comments']} | {p['shares']} |\n"

    engagement_rate = f"{(total_likes + total_comments) / max(len(posts_data), 1):.1f}" if posts_data else "0"

    report = f"""# Weekly LinkedIn Analytics Report
**Period:** {week_start} → {report_date}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Summary
| Metric | Value |
|--------|-------|
| Posts Published | {len(posts_data)} |
| Total Likes | {total_likes} |
| Total Comments | {total_comments} |
| Total Shares | {total_shares} |
| Avg. Engagement/Post | {engagement_rate} |
| Current Followers | {follower_count} |

---

## Post Performance
| Post | Likes | Comments | Shares |
|------|-------|----------|--------|
{rows if rows else "| No posts this week | — | — | — |\n"}

---

## Best Performing Post
- **File:** {best_post.get('source_file', 'N/A')}
- **Likes:** {best_post.get('likes', 0)}
- **Comments:** {best_post.get('comments', 0)}

---

## Recommendations for Next Week
- **Best days to post:** Tuesday, Wednesday, Thursday
- **Best times:** 8:00–10:00 AM, 12:00 PM, 5:00–6:00 PM
- **Content suggestion:** {"Increase how-to / tutorial posts — they tend to get more shares." if total_shares < 5 else "Keep current content mix — engagement is healthy."}
- **Hashtag tip:** Continue using `#AI` and `#SoftwareDevelopment` as anchor tags.

---

*Generated by LinkedIn FTE — AI Employee*
"""

    report_file.write_text(report, encoding="utf-8")
    logger.info(f"[Analytics] Report saved: {report_file}")
    return report_file


if __name__ == "__main__":
    report_path = generate_weekly_report()
    print(f"\nReport generated: {report_path}")
