# LinkedIn Social Media FTE
### Personal AI Employee for LinkedIn — Tech/AI/Software Niche

An autonomous AI agent that generates, schedules, and posts LinkedIn content — with human-in-the-loop approval and weekly analytics reports.

---

## Architecture

```
You give a topic
      ↓
/generate-post skill → Claude writes post + hashtags
      ↓
vault/Pending_Approval/  ← YOU review here
      ↓  (move file to Approved)
approval_watcher.py → LinkedIn API → Published
      ↓  (every Sunday)
analytics_watcher.py → vault/Analytics/Weekly_Report.md
```

---

## Quick Start

### 1. Install Dependencies
```bash
cd "C:\Users\HP ProBook\Desktop\hackathon\Automation"
pip install -r requirements.txt
```

### 2. Set Up LinkedIn API (One-Time)

#### Step A: Create a LinkedIn Developer App
1. Go to https://developer.linkedin.com/
2. Click **"Create App"**
3. Fill in: App name (e.g., "My LinkedIn FTE"), LinkedIn Page (use your profile), App logo
4. Under **"Products"**, request access to **"Share on LinkedIn"** and **"Sign In with LinkedIn using OpenID Connect"**
5. Note down your **Client ID** and **Client Secret**

#### Step B: Get Your Access Token
LinkedIn uses OAuth 2.0. The easiest way for personal use:

1. Go to: https://www.linkedin.com/developers/tools/oauth/token-generator
2. Select your app
3. Check scopes: `w_member_social`, `openid`, `profile`
4. Click **"Request access token"**
5. Copy the **Access Token** (valid for 60 days — renew monthly)

#### Step C: Fill in .env
```
LINKEDIN_CLIENT_ID=paste_your_client_id
LINKEDIN_CLIENT_SECRET=paste_your_client_secret
LINKEDIN_ACCESS_TOKEN=paste_your_access_token
LINKEDIN_PERSON_URN=          ← leave blank, auto-fetched on first run
DRY_RUN=true                  ← change to false when ready for real posts
MAX_POSTS_PER_DAY=3
VAULT_PATH=C:\Users\HP ProBook\Desktop\hackathon\Automation\vault
```

### 3. Verify Token
```bash
cd src
python linkedin_auth.py
```
You should see: `Token valid. Logged in as: Your Name`

### 4. Start the Orchestrator
```bash
cd src
python orchestrator.py
```
Leave this running in the background.

---

## Daily Usage

### Generate a Post
In Claude Code (from the Automation folder):
```
/generate-post
```
Claude will ask for a topic, then write and save a post to `vault/Pending_Approval/`.

Or with a topic directly:
```
/generate-post "5 AI tools that saved me 10 hours this week"
```

### Approve & Post
1. Open `vault/Pending_Approval/` in File Explorer or Obsidian
2. Review the generated `.md` file
3. If happy → move/copy it to `vault/Approved/`
4. The approval watcher detects it and posts to LinkedIn automatically

### View Results
- **Dashboard:** `vault/Dashboard.md`
- **Published posts:** `vault/Published/`
- **Logs:** `vault/Logs/YYYY-MM-DD.json`

### Weekly Analytics
Auto-runs every Sunday at 8 PM. To run manually:
```bash
cd src
python analytics_watcher.py
```
Report saved to: `vault/Analytics/Weekly_Report_YYYY-MM-DD.md`

---

## File Structure
```
Automation/
├── .env                       ← Your credentials (NEVER commit)
├── .gitignore
├── requirements.txt
├── README.md
│
├── vault/
│   ├── Dashboard.md           ← Live activity overview
│   ├── Company_Handbook.md    ← Posting rules & niche (edit this!)
│   ├── Pending_Approval/      ← Generated posts awaiting your review
│   ├── Approved/              ← Drop here to trigger posting
│   ├── Published/             ← Archive of posted content
│   ├── Analytics/             ← Weekly reports
│   └── Logs/                  ← Audit trail
│
├── src/
│   ├── linkedin_auth.py       ← OAuth token management
│   ├── linkedin_poster.py     ← LinkedIn UGC API posting
│   ├── approval_watcher.py    ← Folder watcher → trigger poster
│   ├── analytics_watcher.py   ← Weekly metrics report generator
│   └── orchestrator.py        ← Master process (start this)
│
└── .claude/
    └── commands/
        └── generate-post.md   ← /generate-post skill
```

---

## Switching to Live Mode
When you're ready to post for real:
1. Open `.env`
2. Change `DRY_RUN=true` → `DRY_RUN=false`
3. Restart the orchestrator

---

## Troubleshooting

**"Token invalid" error**
→ Your access token expired (60-day limit). Go back to the LinkedIn OAuth token generator and get a new one.

**Post not triggering after moving to /Approved/**
→ Make sure `python orchestrator.py` is running in a terminal. The approval watcher needs to be active.

**"Rate limit reached" message**
→ You've hit the 3 posts/day limit. Change `MAX_POSTS_PER_DAY` in `.env` if needed (be mindful of LinkedIn limits).

**Analytics shows all zeros**
→ In DRY_RUN mode, real metrics can't be fetched. Switch to live mode and run after real posts are published.

---

## Security Notes
- `.env` is in `.gitignore` — never commit it
- All actions are logged in `vault/Logs/`
- `DRY_RUN=true` by default — safe to experiment
- Max 3 posts/day hardcoded to prevent spam
- All posts require human approval before posting
