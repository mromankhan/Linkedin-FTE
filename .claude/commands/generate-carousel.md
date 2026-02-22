Generate a LinkedIn carousel post (PDF slider) for the Tech/AI/Software niche.

## What is a LinkedIn Carousel?
A PDF document where each page = one swipeable slide. LinkedIn renders it as an interactive slider. Carousels get 3x more reach than text posts because people swipe through them.

---

## FIRST: Topic Selection (Always do this first)

Read `vault/Company_Handbook.md` for niche, tone, and hashtag rules.

### If a topic was provided in the command arguments:
Use it directly. Skip to "Generate the Carousel" section.

### If NO topic was provided:

**Step A — Check recent posts to avoid repetition:**
List all files in `vault/Published/` and read the `topic:` field from their frontmatter.
Keep a mental note — do NOT suggest similar topics.

**Step B — Generate 6 FRESH carousel topic ideas right now.**
Do NOT use pre-written examples. Think creatively based on:
- Today's date and what is trending in Tech/AI/Software right now
- Carousel-friendly formats: listicle, step-by-step, comparison, mistakes, framework, roadmap
- The 5 content pillars from Company_Handbook.md
- Topics NOT already covered in vault/Published/

Each suggestion must be carousel-friendly — meaning it naturally breaks into 5–8 slides.

Show them like this (use your OWN generated topics, not examples):

```
Choose a topic for your LinkedIn CAROUSEL:

1. [FORMAT]  "Your generated topic idea here"
2. [FORMAT]  "Your generated topic idea here"
3. [FORMAT]  "Your generated topic idea here"
4. [FORMAT]  "Your generated topic idea here"
5. [FORMAT]  "Your generated topic idea here"
6. [FORMAT]  "Your generated topic idea here"

Type a number (1-6) or write your own topic:
```

Wait for the user to reply with a number or custom topic. Then use that topic.

---

## Generate the Carousel

Then do the following:

### 1. Plan the carousel structure
Design 5–8 slides following this structure:
- **Slide 1 (Cover):** Bold title + one-line subtitle. Must hook immediately.
- **Slides 2–N (Content):** Each slide = one insight/tip/step. Keep it focused — one idea per slide.
- **Last Slide (CTA):** Question or action that encourages comments/follows.

### 2. Write the carousel content as a JSON structure in your response
Output a Python-compatible dict like this (for the code to use):
```python
carousel_data = {
    "title": "...",
    "subtitle": "...",
    "slides": [
        {"heading": "...", "body": "..."},
        {"heading": "...", "body": "..."},
        ...
    ],
    "cta_text": "...",
    "hashtags": ["AI", "Tech", "SoftwareDevelopment", ...],
    "caption": "... (the LinkedIn post text that goes WITH the carousel, 80-120 words)"
}
```

### 3. Generate the PDF
Run this Python code using the data above:

```python
import sys
sys.path.insert(0, 'src')
from carousel_generator import create_carousel_pdf
from pathlib import Path
from datetime import datetime
import re

# Slug from title
slug = re.sub(r'[^a-z0-9]+', '-', carousel_data["title"].lower()).strip('-')[:40]
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
pdf_filename = f"CAROUSEL_{timestamp}_{slug}.pdf"
pdf_path = f"vault/Pending_Approval/{pdf_filename}"

create_carousel_pdf(
    title=carousel_data["title"],
    subtitle=carousel_data["subtitle"],
    slides=carousel_data["slides"],
    cta_text=carousel_data["cta_text"],
    hashtags=carousel_data["hashtags"],
    output_path=pdf_path,
    brand_name="",  # optional: put your LinkedIn handle here
)
```

### 4. Save the approval .md file
Save a companion markdown file at `vault/Pending_Approval/` with the same name but `.md` extension:

```markdown
---
type: carousel
topic: <topic>
pdf_path: vault/Pending_Approval/<pdf_filename>
hashtags: AI, Tech, SoftwareDevelopment, <others>
best_time: <recommend best day + time>
created: <ISO timestamp>
status: pending_approval
---

## Post Caption (goes with the carousel)

<carousel_data["caption"]>

## Hashtags
<hashtags one per line>

## Carousel Slides Preview
<list each slide heading>

## Notes
- PDF is ready at: vault/Pending_Approval/<pdf_filename>
- Move BOTH this .md file AND the .pdf to vault/Approved/ to post
```

### 5. Tell the user
1. How many slides were created
2. Where the PDF is saved (open it to preview!)
3. The best posting time
4. Instructions: "Review the PDF, then move BOTH files (`.md` + `.pdf`) to `vault/Approved/` to trigger posting."

## Slide Writing Rules
- Each slide body: max 4 lines, 2-3 sentences max
- Use → bullet points for lists (renders well on mobile)
- Numbers work great: "3 reasons", "5 tools", "7 mistakes"
- Last content slide should be a "key takeaway" or summary
- CTA should ask a genuine question to spark comments

## Example Topics (Tech/AI niche)
- "5 Python libraries every developer should know in 2026"
- "The AI workflow that replaced my 3-hour research process"
- "7 mistakes developers make when prompting Claude"
- "How to build a personal AI agent in a weekend"
- "The 4 stages of AI adoption in software teams"
