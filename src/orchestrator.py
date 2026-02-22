"""
Orchestrator — Master process for LinkedIn FTE.
Starts the approval watcher and schedules weekly analytics.
Run this to start your AI Employee.
"""

import os
import sys
import logging
import threading
from pathlib import Path
from datetime import datetime
import schedule
import time
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

VAULT_PATH = Path(os.getenv("VAULT_PATH", "vault"))
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║          LinkedIn Social Media FTE — Starting Up         ║
║                  Personal AI Employee                    ║
╚══════════════════════════════════════════════════════════╝
""")
    mode = "DRY RUN (safe mode)" if DRY_RUN else "LIVE MODE — real posts will be made!"
    logger.info(f"Mode: {mode}")
    logger.info(f"Vault: {VAULT_PATH.resolve()}")


def start_approval_watcher():
    """Run approval watcher in a background thread."""
    from approval_watcher import run as run_watcher
    thread = threading.Thread(target=run_watcher, daemon=True, name="ApprovalWatcher")
    thread.start()
    logger.info("[Orchestrator] Approval watcher started.")
    return thread


def run_weekly_analytics():
    """Triggered every Sunday at 20:00."""
    logger.info("[Orchestrator] Running weekly analytics report...")
    try:
        from analytics_watcher import generate_weekly_report
        report_path = generate_weekly_report()
        logger.info(f"[Orchestrator] Analytics done: {report_path}")
    except Exception as e:
        logger.error(f"[Orchestrator] Analytics failed: {e}")


def update_dashboard_status(status: str):
    """Update system status in Dashboard.md."""
    import re
    dashboard = VAULT_PATH / "Dashboard.md"
    if not dashboard.exists():
        return
    text = dashboard.read_text(encoding="utf-8")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    text = re.sub(r"- \*\*System:\*\* .*", f"- **System:** {status}", text)
    text = re.sub(r"- \*\*Last Updated:\*\* .*", f"- **Last Updated:** {now}", text)
    dashboard.write_text(text, encoding="utf-8")


def main():
    print_banner()

    # Verify vault exists
    if not VAULT_PATH.exists():
        logger.error(f"Vault not found at: {VAULT_PATH}")
        logger.error("Make sure VAULT_PATH in .env points to the correct location.")
        sys.exit(1)

    update_dashboard_status("🟢 Running" + (" (Dry Run)" if DRY_RUN else " (Live)"))

    # Start approval watcher in background
    watcher_thread = start_approval_watcher()

    # Schedule weekly analytics every Sunday at 20:00
    schedule.every().sunday.at("20:00").do(run_weekly_analytics)
    logger.info("[Orchestrator] Weekly analytics scheduled: every Sunday at 20:00")

    logger.info("[Orchestrator] All systems running. Press Ctrl+C to stop.\n")
    logger.info("NEXT STEPS:")
    logger.info("  1. Use /generate-post in Claude Code to create a LinkedIn post")
    logger.info("  2. Review the post in vault/Pending_Approval/")
    logger.info(f"  3. Move the file to vault/Approved/ to {'simulate' if DRY_RUN else 'trigger'} posting")
    logger.info("  4. Check vault/Dashboard.md for status updates\n")

    try:
        while True:
            schedule.run_pending()
            # Check watcher thread health
            if not watcher_thread.is_alive():
                logger.warning("[Orchestrator] Approval watcher died. Restarting...")
                watcher_thread = start_approval_watcher()
            time.sleep(30)
    except KeyboardInterrupt:
        update_dashboard_status("🔴 Stopped")
        logger.info("[Orchestrator] Shutting down. Goodbye!")


if __name__ == "__main__":
    main()
