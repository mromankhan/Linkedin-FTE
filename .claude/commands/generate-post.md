Generate a LinkedIn text post for the Tech/AI/Software niche.

## FIRST: Topic Selection (Always do this first)

Read `vault/Company_Handbook.md` for niche, tone, and hashtag rules.

### If a topic was provided in the command arguments:
Use it directly. Skip to "Generate the Post" section.

### If NO topic was provided:

**Step A — Check recent posts to avoid repetition:**
List all files in `vault/Published/` and read the `topic:` field from their frontmatter.
Keep a mental note of these — do NOT suggest anything similar.

**Step B — Generate 6 FRESH topic ideas right now.**
Do NOT use pre-written examples. Think creatively based on:
- Today's date and what is currently trending in Tech/AI/Software
- The 5 content pillars from Company_Handbook.md (rotate — pick different pillars)
- Formats that perform well on LinkedIn: list, hot take, story, how-to, trend, opinion
- Topics NOT already covered in vault/Published/

Each suggestion must be:
- Specific and scroll-stopping (not vague like "AI is changing things")
- A different format type from the others
- Something a real developer or founder would genuinely want to read

Show them like this (use your OWN generated topics, not examples):

```
Choose a topic for your LinkedIn post:

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

Using the selected topic, write a complete LinkedIn post:

### Post Structure
1. **Hook** (Line 1): Bold statement, surprising fact, or provocative question. Must stop the scroll.
2. **Body** (3–5 paragraphs): Insightful, concrete, conversational. Max 2–3 lines per paragraph. No filler.
3. **CTA** (Last line): Genuine question or action that sparks comments.
4. **Hashtags** (5–8): Follow handbook strategy. At the very end.

### Requirements
- Length: 150–300 words
- Tone: Professional but human. Thought leadership, not sales pitch.
- Must feel like a real person wrote it
- Best time to post: recommend specific day + time

### Save the File
Save to `vault/Pending_Approval/POST_YYYY-MM-DD_HH-MM_<topic-slug>.md`

```
---
type: text
topic: <topic>
hashtags: AI, Tech, SoftwareDevelopment, <2-5 more>
best_time: <e.g., Tuesday 9:00 AM>
created: <ISO timestamp>
status: pending_approval
---

## Post Content

<full post text — no hashtags here>

## Hashtags
<one per line, with # prefix>

## Notes
<reviewer notes: suggested edits, link to add, etc.>
```

### After Saving — Tell the User
```
POST SAVED
==========
File: vault/Pending_Approval/<filename>
Topic: <topic>
Best time to post: <day + time>

NEXT STEPS:
1. Open the file and review the post
2. Edit anything you want to change
3. Move file to vault/Approved/ to post to LinkedIn
```
