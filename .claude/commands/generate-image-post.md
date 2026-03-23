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

### Step 2 — Extract Specific Visual Elements Directly from the Caption

Re-read your caption word by word. Pull out the **exact details** that must appear in the image. Do NOT invent metaphors — translate what the caption literally says into visuals.

Answer these before touching the image prompt:

1. **Subject**: Who or what is the caption specifically about? (e.g., "a developer", "AI tools", "5 stages", "a code review")
2. **Action or contrast**: What is happening or being compared? (e.g., "struggling then succeeding", "before vs after", "5 numbered steps")
3. **Specific details**: What exact numbers, stages, names, or concepts are mentioned in the caption? List them. Every specific detail in the caption is a candidate visual element.
4. **Emotion arc**: What does the caption make the reader feel — and at what point? Map this to lighting/mood, not to a new concept.

**Caption → Image translation rule:**
Every major element in the image must trace back to a specific word, phrase, or idea from the caption. If you can't point to where in the caption a visual element came from — remove it.

Bad (generic metaphor drift): Caption says "5 stages of AI adoption" → image shows a glowing brain surrounded by data streams (not connected to what the caption says)

Good (caption-derived): Caption says "5 stages of AI adoption" and lists Denial → Curiosity → Frustration → Breakthrough → Dependence → image shows exactly 5 labelled waypoints on a path with a developer figure at each, the 3rd in storm/darkness, the 5th at a glowing peak

### Step 2.5 — Decide: Does This Post Need Text ON the Image?

Some posts land harder when key words are printed directly on the image — the viewer reads the image AND the caption together. Others are stronger with a clean visual only.

**Use text ON the image when:**
- The post is a stat, list, or comparison (e.g., "5 stages", "Before vs After", "3x faster")
- The core message is a short punchy phrase that works as a headline (e.g., "Stop Using AI Wrong")
- The format is infographic-style — the image itself needs to communicate structure
- The image alone without text would be confusing or too abstract

**Keep image text-free when:**
- The image is purely atmospheric/emotional (developer on mountain, dark cityscape)
- The visual metaphor is strong enough to speak without words
- The caption already delivers all the information — image just sets the tone

**If text ON image is needed**, decide:
- What is the ONE headline (5 words max) that goes on the image?
- Are there sub-labels needed? (e.g., stage names, step numbers, before/after labels)
- Where do they sit compositionally? (top center headline, bottom labels, inline badges)

---

### Step 3 — Generate the Gemini Image Prompt

Using **only** the specific details you extracted in Step 2, write the prompt. Every sentence must connect to something the caption actually says.

For the `Text overlay` field — choose based on your Step 2.5 decision:

**If NO text needed:**
```
Text overlay: NONE — clean visual only, LinkedIn caption handles all text
```

**If text ON image IS needed:**
```
Text overlay: YES
  - Headline: "[5-word max punchy phrase from the post]" — placed [top-center / center / bottom-center], [font style: bold sans-serif / condensed display]
  - Sub-labels (if any): [e.g., "Stage 1: Denial", "Stage 2: Curiosity" — placed at each waypoint]
  - Text color: [high contrast against background — e.g., white with subtle dark drop shadow]
  - NO other text — only the specified labels above
```

```
GEMINI IMAGE PROMPT:
─────────────────────────────────────────────
[Open with the exact subject from the caption — name it specifically, not generically]
[Describe what is happening in the scene using the exact concepts, numbers, or stages from the caption]
[Include the emotional arc from the caption: where does it start, where does it end?]
[Every visual element must be traceable to the caption — call out specifics]

Style: [choose one that fits the post mood: "3D render" / "Cinematic photo" / "Flat illustration" / "Dark digital art"]
Mood: [match the caption's emotional tone exactly: "Empowering" / "Urgent" / "Calm and focused" / "Futuristic" / "Serious"]
Colors: [derive from the topic's emotion — e.g., "Deep charcoal for struggle, electric gold for breakthrough"]
Composition: Square 1:1 ratio, 1200x1200px, centered subject, subtle depth blur at edges
Text overlay: [NONE -OR- YES with exact text, placement, and style as decided in Step 2.5]
Lighting: [match mood and caption's emotional peak: "Dramatic cinematic rim light" / "Soft morning glow" / "Neon volumetric glow"]
Key visual elements: [List 3–5 elements — each must come from a specific phrase in the caption]
Details to AVOID: No generic stock imagery, no watermarks, no logos, no handshakes, no elements not mentioned in the caption[, no extra text beyond what is specified above]
Quality: Ultra high resolution, sharp center focus, optimized for LinkedIn feed thumbnail
─────────────────────────────────────────────
```

**Relevance self-check before finalising:**
Read your prompt back. For each visual element ask: "Which line of the caption does this come from?" If you can't answer — cut it or replace it with something from the caption. The image should feel like a visual edition of the caption, not a themed decoration.

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
