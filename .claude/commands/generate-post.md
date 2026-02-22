Generate a LinkedIn post for the Tech/AI/Software niche.

## Instructions

Read the file `vault/Company_Handbook.md` to understand the posting rules, tone, niche, and hashtag strategy.

Then ask the user: **"What topic do you want to post about?"** (if not already provided in the command arguments).

Using the topic provided, generate a complete LinkedIn post following these rules:

### Post Structure
1. **Hook** (Line 1): A bold statement, surprising fact, or provocative question. Must grab attention in the first 2 seconds.
2. **Body** (3–5 short paragraphs): Insightful, concrete, and conversational. Max 2–3 lines per paragraph. No fluff.
3. **CTA** (Last paragraph): A genuine call to action — ask a question, invite opinions, or tell them to follow.
4. **Hashtags** (5–8): Based on topic, following the strategy in Company_Handbook.md. Place at the very end.

### Post Requirements
- Length: 150–300 words
- Tone: Professional but human. Not salesy. Thought leadership voice.
- Must feel like a real person wrote it, not a robot
- Include a "Best time to post" recommendation (day + time)

### Output Format
Save the generated post as a markdown file in `vault/Pending_Approval/` with this exact naming format:
`POST_YYYY-MM-DD_HH-MM_<topic-slug>.md`

The file must use this frontmatter schema:
```
---
topic: <topic in plain English>
hashtags: AI, Tech, SoftwareDevelopment, <2-5 more relevant tags>
best_time: <e.g., Tuesday 9:00 AM>
created: <ISO timestamp>
status: pending_approval
---

## Post Content

<full post text here, without hashtags>

## Hashtags
<hashtags listed here, one per line with # prefix>

## Notes
<any notes for the human reviewer, e.g., suggested image, link to add, etc.>
```

### After Saving
Tell the user:
1. Where the file was saved
2. What the best posting time is
3. How to approve it: "Review the post, then move the file from `vault/Pending_Approval/` to `vault/Approved/` to trigger posting."
4. If the orchestrator is running, the post will be automatically submitted to LinkedIn once moved to Approved.

### Example Topics (for Tech/AI niche)
- "5 AI tools that replaced 3 hours of my daily work"
- "Why most developers still don't understand prompting"
- "The dirty secret about AI automation in 2026"
- "How I built a personal AI employee in a weekend"
- "Python vs AI coding assistants — who wins in 2026?"
