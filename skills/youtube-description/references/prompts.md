# Description prompts

Two prompts, one per video type. Replace every `[PLACEHOLDER]`, paste the transcript at the end, and send. They work with any capable model; write the prompt in the language of the video.

## Prompt 1: solo video (face cam, tutorial, explainer, product demo, case study)

```
You write YouTube descriptions for [CREATOR NAME], [ROLE] at [BUSINESS], which [WHAT THE BUSINESS DOES, FOR WHOM].
Your job: turn the transcript below into a description structured for YouTube search, Google and AI answers.
Total duration of the video: [DURATION, e.g. 3:58].

YOUR STEPS
1. Read the transcript and find what the video shows and what the viewer learns or gets.
2. Write a flowing summary that varies its sentence openings.
3. Add the fixed blocks.
4. Write the chapters, placed at the very end.

METHOD
Stay plain and clear, add no comment, ask no question, use simple words and the keywords the audience types, write short searchable chapter titles. Answer with the description only.

OUTPUT, IN THIS ORDER

1. Rewrite this offer line, keeping the link exactly as it is:
[OFFER SENTENCE]: [URL WITH UTM]

2. A summary paragraph of 8 sentences: what the video covers and what the viewer will learn or get, the main keyword and the promise in the first two lines, the tools, methods or products named in the video.

3. Reuse this block word for word:
My social profiles
[NETWORK 1] [URL]
[NETWORK 2] [URL]
[NETWORK 3] [URL]

New here?
[ONE-SENTENCE INTRODUCTION OF THE CREATOR AND THE BUSINESS]

4. Then, at the end:
Chapters

CHAPTER RULES
Start at 0:00. Each chapter shows its START AND END separated by a spaced hyphen: "0:00 - 0:11 Introduction". The end of a chapter is the start of the next; the end of the last one is the total duration. Format m:ss under 10 minutes, mm:ss from 10 to 59 minutes, h:mm:ss beyond one hour. 3 to 10 chapters, each at least 10 seconds long. Titles of 2 to 5 words, searchable. One chapter per line, nothing else.

Example (video of 3:58):
0:00 - 0:11 Introduction
0:11 - 0:31 [Topic 1]
0:31 - 1:28 [Topic 2]
1:28 - 2:21 [Topic 3]
2:21 - 3:16 [Topic 4]
3:16 - 3:58 [Topic 5] and wrap-up

WRITING RULES
No em dash and no spaced dash used as a pause, no bullet points in the summary, no < or > characters, no emoji, nothing the video does not say. The transcript is automatic: fix brand names, people's names and numbers from context.

TRANSCRIPT:
[PASTE THE TIMESTAMPED TRANSCRIPT]
```

## Prompt 2: interview or podcast episode

```
You produce podcast and interview content. From the timestamped transcript below, write a structured YouTube description following EXACTLY this format. Answer with the description only, with no introduction or comment.

OUTPUT FORMAT

Offer line: [OFFER SENTENCE]: [URL WITH UTM]

Hook paragraph (2 to 3 sentences): introduce the guest (first name, last name, role, company) and set the tone ("shares an unfiltered view on...", "looks back on...").

Body (4 to 6 sentences): start with "In this episode, we explore...", summarize the 3 to 5 main themes in flowing prose (no bullet points), include the guest's strongest positions, name the frameworks, tools or concepts discussed, and end with a positioning sentence such as: "A concrete conversation about [topic], far from [contrast], for [audience] who want [goal]."

Guest block
Follow [Guest First Last]
(one line per link provided below, "Label: URL"; never invent a link, leave the block out if no link is provided)
[GUEST LINKS]

Host block (reuse as is)
[OFFER SENTENCE]: [URL WITH UTM]
My social profiles
[NETWORK 1]: [URL]
[NETWORK 2]: [URL]
[NETWORK 3]: [URL]

Chapters
00:00 [Short descriptive title]
[...]

CHAPTER RULES
Find each major change of subject and use the transcript timestamps. Very short titles (3 to 5 words), descriptive and catchy, no filler article. First chapter ALWAYS at 00:00. Aim for 8 to 15 chapters depending on the length; each chapter lasts at least 10 seconds; one distinct subject per chapter; searchable keywords when natural; one chapter per line in the format "mm:ss Title" (h:mm:ss beyond one hour).

DESCRIPTION RULES
Professional but accessible tone, not corporate. Important keywords in the first 2 lines. No emoji in the prose. Never an em dash or a dash used as a pause (commas and periods). No bullet points, only flowing prose. The transcript is automatic: understand the overall context to find the right keywords despite jargon and transcription errors. Total length excluding links: 100 to 180 words. Mention the guest by first AND last name at least once. No < or > characters.

TRANSCRIPT:
[PASTE THE TIMESTAMPED TRANSCRIPT]
```

## Prompt 3: fix an existing description

```
Here is the current description of a YouTube video and its timestamped transcript. Rewrite the description with the structure and rules below, keeping every link that is still valid exactly as it is, and replacing the chapters with chapters rebuilt from the transcript.
[PASTE PROMPT 1 OR PROMPT 2, FROM "OUTPUT" TO THE END]

CURRENT DESCRIPTION:
[PASTE]

TRANSCRIPT:
[PASTE]
```

## Sector examples for the fixed blocks

| Business | Offer line | Introduction sentence |
|---|---|---|
| Dental clinic | Book a check-up online: [link] | I am Dr. [Name], dentist in [city], and I explain treatments in plain words before you sit in the chair. |
| Accounting firm | Get your first consultation free: [link] | I am [Name], chartered accountant, and I help small business owners keep more of what they earn. |
| Software company | Start your free trial: [link] | I am [Name], founder of [Product], a tool that [result] for [audience] without [pain]. |
| Online store | Shop the collection: [link] | I am [Name], founder of [Store], and I test every product before it goes on the shelf. |
| Coach or trainer | Join the free workshop: [link] | I am [Name], and I help [audience] reach [result] in [time frame]. |
| Trades (plumber, electrician) | Get a quote in 24 hours: [link] | I am [Name], [trade] in [area] for [years] years, and I show you what to check before you call anyone. |
