Generate a LinkedIn image post with a Gemini image prompt for the Tech/AI/Software niche.

## FIRST: Topic Selection (Always do this first)

Read `vault/Company_Handbook.md` for niche, tone, and hashtag rules.

### If a topic was provided in the command arguments:
Use it directly. Skip to "Generate the Post" section.

### If NO topic was provided:

**Step A — Check recent posts to avoid repetition:**
List all files in `vault/Published/` and read the `topic:` field from their frontmatter.
Keep a mental note — do NOT suggest similar topics.

**Step B — Generate 6 FRESH topic ideas right now.**
Do NOT use pre-written examples. Think creatively based on:
- Today's date and current trends in Tech/AI/Software
- Topics that produce a compelling, shareable image (visual metaphors work best)
- Formats: visual stat, tool showcase, before/after, concept explainer, hot take, infographic
- Topics NOT already covered in vault/Published/

Each suggestion must be visually strong — ask yourself: "would this make a striking image?"

Show them like this (use your OWN generated topics, not examples):

```
Choose a topic for your LinkedIn IMAGE post:

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

## Generate the Post

### Step 1 — Write the Caption FIRST
- Length: 100–200 words (image carries the visual weight)
- Strong hook in first line
- 2–3 short paragraphs
- Clear CTA at end
- 5–7 hashtags

### Step 2 — Extract the Core Visual Idea from the Caption

Before writing the image prompt, read what you just wrote in Step 1 and answer:
- **What is the single most important message of this post?**
- **What emotion or insight should someone feel when they see the image?**
- **What visual metaphor would represent this message?**

Examples of caption → visual metaphor mapping:
| Post message | Visual metaphor |
|---|---|
| "AI tools save 3 hours daily" | Hourglass with digital particles flowing through it, half sand half glowing code |
| "Junior vs Senior developer mindset" | Two paths diverging — one rocky/manual, one lit with AI glow |
| "Debugging with AI is faster" | Magnifying glass made of light rays scanning glowing code lines |
| "AI agents working 24/7" | City skyline at night with glowing digital workers floating above it |
| "Clean code vs shipped code" | Two buildings — one ornate but unfinished, one simple but standing tall |

### Step 3 — Generate the Gemini Image Prompt

Using the visual metaphor you identified in Step 2, write a **detailed, copy-paste ready** prompt that is **directly tied to what the caption says**:

```
GEMINI IMAGE PROMPT:
─────────────────────────────────────────────
[Describe the visual metaphor scene in detail — make it specific to THIS post's message]
[What object/scene represents the core idea? What is happening in the image?]
[What should the viewer feel/understand just by looking at it?]

Style: [choose one that fits the post mood: "3D render" / "Cinematic photo" / "Flat illustration" / "Dark digital art"]
Mood: [match the post tone: "Empowering" / "Urgent" / "Calm and focused" / "Futuristic" / "Serious"]
Colors: [tied to topic emotion — e.g., "Deep navy background, electric indigo for AI elements, warm amber for human elements"]
Composition: Square 1:1 ratio, 1200x1200px, centered subject, subtle depth blur at edges
Text overlay: NONE — the LinkedIn caption handles all text
Lighting: [match mood: "Dramatic cinematic rim light" / "Soft morning glow" / "Neon volumetric glow"]
Key visual elements: [3-5 specific things that make this image unique to THIS post topic]
Details to AVOID: No generic stock imagery, no text, no watermarks, no logos, no handshakes
Quality: Ultra high resolution, sharp center focus, optimized for LinkedIn feed thumbnail
─────────────────────────────────────────────
```

**Rules for a great, post-relevant image prompt:**
- The image must make sense WITH the caption — like a book cover matches the story inside
- If someone sees the image alone, they should guess roughly what the post is about
- Never use generic tech imagery (random circuit boards, keyboard close-ups) unless directly relevant
- The visual metaphor should be the central element, not a background decoration

### Step 3 — Suggest the Image Filename
```
vault/Images/IMAGE_<topic-slug>_<YYYY-MM-DD>.png
```

### Step 4 — Save the Approval File
Save to `vault/Pending_Approval/POST_YYYY-MM-DD_HH-MM_<topic-slug>.md`

```
---
type: image
topic: <topic>
image_path: vault/Images/IMAGE_<topic-slug>_<YYYY-MM-DD>.png
hashtags: AI, Tech, SoftwareDevelopment, <2-4 more>
best_time: <e.g., Thursday 9:00 AM>
created: <ISO timestamp>
status: waiting_for_image
---

## Post Content

<caption text — no hashtags>

## Hashtags
<one per line with # prefix>

## Image Instructions
Save your generated image to: `vault/Images/IMAGE_<topic-slug>_<YYYY-MM-DD>.png`

**Gemini Prompt (copy this):**
<full prompt here>

## How to Approve
1. Paste the Gemini prompt into https://gemini.google.com (or Midjourney / DALL-E / Ideogram)
2. Download the image
3. Save to: vault/Images/IMAGE_<topic-slug>_<YYYY-MM-DD>.png
4. Move THIS .md file to vault/Approved/
5. LinkedIn post fires automatically!
```

### Step 5 — Tell the User
```
IMAGE POST READY
================
Topic: <topic>
Best time to post: <day + time>
File: vault/Pending_Approval/<filename>

GEMINI IMAGE PROMPT (copy this):
─────────────────────────────────
<full prompt>
─────────────────────────────────

NEXT STEPS:
1. Go to: https://gemini.google.com
2. Paste the prompt → Generate → Download
3. Save image to: vault/Images/<filename>
4. Move .md file to vault/Approved/ → Done!
```
