Generate a LinkedIn image post with a Gemini image prompt for the Tech/AI/Software niche.

## What This Does
1. Generates the LinkedIn post caption + hashtags
2. Generates a detailed Gemini image prompt (ready to paste into Gemini)
3. Saves the approval file — waiting for you to add the image

---

## Instructions

Read `vault/Company_Handbook.md` for tone and niche guidelines.

Ask the user: **"What is the topic for this image post?"** (if not already given in arguments).

---

## Step 1 — Write the LinkedIn Caption

Write a LinkedIn post caption following these rules:
- Length: 100–200 words (shorter than text posts — image carries the weight)
- Hook in first line (bold statement or question)
- 2–3 short paragraphs
- Clear CTA at end
- 5–7 relevant hashtags

---

## Step 2 — Generate the Gemini Image Prompt

Create a **detailed, copy-paste ready image prompt** for Gemini (image generator).

The prompt must follow this structure:

```
GEMINI IMAGE PROMPT:
─────────────────────────────────────────────
[Describe the main visual scene in detail]

Style: [e.g., "Photorealistic", "3D render", "Flat design illustration", "Dark tech aesthetic"]
Mood: [e.g., "Professional", "Futuristic", "Minimalist", "Bold and dynamic"]
Colors: [e.g., "Dark navy blue background, indigo and white accents, soft glow effects"]
Composition: [e.g., "Wide landscape 16:9", "Square 1:1 for LinkedIn", centered subject]
Text overlay: [NONE — LinkedIn caption handles the text]
Lighting: [e.g., "Cinematic lighting", "Soft studio light", "Neon glow"]
Details to include: [specific elements]
Details to AVOID: [e.g., "No text", "No watermarks", "No people's faces"]
Quality: Ultra high resolution, sharp details, LinkedIn-optimized
─────────────────────────────────────────────
```

### Image prompt guidelines for Tech/AI niche:
- Abstract tech visuals work great: circuits, glowing nodes, data streams, AI brain visualizations
- Avoid stock-photo clichés (handshakes, generic office people)
- Dark backgrounds with glowing accents perform well on LinkedIn
- Include a "visual metaphor" that connects to the post topic
- Size: always mention "square 1:1 ratio, 1200x1200px" for LinkedIn

### Example image prompts by topic:
- AI tools → "Futuristic robot hand typing on a holographic keyboard, dark navy background, glowing blue light trails, 3D render, cinematic lighting, square 1:1 ratio"
- Productivity → "Clean minimal desk with a glowing laptop showing abstract code, soft morning light, top-down view, muted warm tones, photorealistic, 1:1 ratio"
- Software development → "Abstract network of glowing nodes and connections representing code architecture, deep space background, purple and blue neon, 3D visualization, 1:1 ratio"

---

## Step 3 — Determine the Image Filename

Based on the topic, suggest a clear filename the user should save their image as:
```
suggested_filename: IMAGE_<topic-slug>_<YYYY-MM-DD>.png
example: IMAGE_ai-tools-productivity_2026-02-22.png
```

The image should be saved at:
```
vault/Images/<suggested_filename>
```

---

## Step 4 — Save the Approval File

Save a markdown file at `vault/Pending_Approval/POST_<YYYY-MM-DD>_<HH-MM>_<topic-slug>.md`:

```markdown
---
type: image
topic: <topic in plain English>
image_path: vault/Images/<suggested_filename>
hashtags: AI, Tech, SoftwareDevelopment, <2-4 more>
best_time: <recommend best day + time e.g. "Tuesday 9:00 AM">
created: <ISO timestamp>
status: waiting_for_image
---

## Post Content

<full caption here, without hashtags>

## Hashtags
<each hashtag on its own line with # prefix>

## Image Instructions
**Save your generated image here:**
`vault/Images/<suggested_filename>`

**Gemini Prompt (copy this):**
---
<paste the full gemini prompt here>
---

## How to Approve
1. Generate image using the Gemini prompt above
2. Save it to: vault/Images/<suggested_filename>
3. Move THIS .md file to vault/Approved/
4. The system will post the image + caption to LinkedIn automatically
```

---

## Step 5 — Tell the User Everything

Show a clear summary:

```
POST READY FOR IMAGE GENERATION
================================
Topic: <topic>
Caption: <first line of caption>...
Best time to post: <day + time>

GEMINI IMAGE PROMPT (copy this):
─────────────────────────────────
<full prompt>
─────────────────────────────────

NEXT STEPS:
1. Go to https://gemini.google.com or any AI image generator
2. Paste the prompt above
3. Download the generated image
4. Save it as: vault/Images/<filename>
5. Move vault/Pending_Approval/<md-file> to vault/Approved/
6. LinkedIn post will fire automatically!
```
