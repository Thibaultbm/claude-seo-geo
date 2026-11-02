---
name: youtube-description
description: "Write or fix a YouTube video description from its timestamped transcript, for any business or sector. Input: the transcript with timestamps, the total duration, the video type (solo video, tutorial, product demo, interview or podcast) and the channel's fixed blocks (offer link, social profiles, one-line introduction). Output: a ready-to-paste description with a tracked call-to-action link on line one, a keyword-rich summary, the guest and host link blocks, and valid chapters, checked by a bundled script (chapters, length, forbidden characters). Use to write, rewrite or audit a YouTube description, add chapters or timestamps, prepare a podcast episode description, or make a video findable in YouTube search, Google and AI answers."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# YouTube Description: From Transcript to a Description That Ranks

A description does three jobs at once: it sends viewers to the offer (line one), it tells YouTube, Google and AI engines what the video covers (the summary), and it lets viewers jump to the part they came for (the chapters). This skill writes all three from the transcript, never from memory of the video, and checks the result with a script before anything is pasted.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: the channel's fixed blocks (offer link, social profiles, introduction sentence), the target keywords, the house writing rules and past descriptions that performed. Ground every choice in that context instead of asking for facts the vault already holds. At the end, record any new fixed block or rule in the note that owns it.

## When to use this skill

| The user wants | Use this skill? | Where it belongs |
|---|---|---|
| A description, chapters or timestamps for a video | Yes | here |
| To fix the description of a video already online | Yes | here, then update it in YouTube Studio |
| The title of the video | No | youtube-title |
| The thumbnail | No | youtube-thumbnail |
| To turn the video into posts for other platforms | No | social-amplification |
| To get the video cited by AI engines beyond YouTube | Partly | geo-visibility owns citability rules |

## Inputs to collect

1. **The transcript with timestamps.** Sources, in order of preference: your own local transcription (Whisper with word timestamps), the transcript in YouTube Studio (Subtitles), or a transcript tool that takes the video link. Automatic transcripts have no punctuation and mangle brand names and jargon: read them for meaning, never copy them.
2. **The total duration** (the last timestamp of the transcript is close but not exact: take the real duration from the file or from YouTube Studio).
3. **The video type**: solo (face cam, tutorial, explainer, product demo, case study) or conversation (interview, podcast, panel). The structure differs.
4. **The channel's fixed blocks**, written once and reused word for word:
   - the offer line: a short benefit sentence plus a link, for example `Book your free consultation: https://example.com/contact`;
   - the social profiles (only real URLs);
   - a one-sentence introduction of the creator or the business ("New here? I am [name], [role] at [business], [what the business does for whom].").
5. **For a conversation**: the guest's full name, role, company, and the links the guest provided (website, main social profile, one free call to action). Never invent a guest link: leave the block out when no link was given.
6. **The language.** One description per language, written from the transcript in that language (a dubbed or subtitled version gets its own transcript and its own chapters, because timings shift).

## Structure A: solo video

```
[Offer line with tracked link]

[Summary: 8 sentences]

[Social profiles block]

[Introduction sentence]

Chapters
[chapters]
```

Rules for the summary:

1. Eight sentences of flowing prose, no bullet points.
2. The main keyword and the promise in the first two lines: YouTube shows roughly the first 100 to 150 characters above the "more" fold, in search results and under the player, so these lines decide the click (field heuristic, the fold moves with screen size).
3. Explain what the video shows and what the viewer will learn or get, in plain words the audience actually types (the customer's vocabulary, not the trade's jargon).
4. Vary the sentence openings: no run of "In this video...", "You will...", "We...".
5. Name the tools, methods, places or products the video really covers: they are the long-tail keywords.

## Structure B: interview or podcast

```
[Offer line with tracked link]

[Hook paragraph: 2 to 3 sentences]

[Body: 4 to 6 sentences]

Follow [Guest Full Name]
Website: [URL]
[Network]: [URL]

[Host block: offer link + social profiles, reused as is]

Chapters
[chapters]
```

1. **Hook paragraph**: introduce the guest (first name, last name, role, company) and set the tone ("shares an unfiltered view on...", "looks back on...").
2. **Body**: open with "In this episode, we explore...", cover the 3 to 5 main themes in prose, include the guest's strongest positions and the frameworks, tools or concepts named, and close with a positioning sentence: "A concrete conversation about [topic], far from [contrast], for [audience] who want [goal]."
3. 100 to 180 words excluding the link blocks; the guest's full name appears at least once in the prose.
4. A link block may start with a small marker character if the channel uses one; the prose itself stays free of emoji.

## The tracked link

Every link to your own site carries UTM parameters so the visits show up as YouTube in analytics, per video:

```
https://example.com/?utm_source=youtube&utm_medium=social&utm_campaign=<topic>&utm_content=<video-slug>-<lang>
```

Keep the same `utm_source` and `utm_medium` on every video; only `utm_campaign` and `utm_content` change. The channel and campaign naming convention belongs in geo-tracking.

## Chapters

YouTube only builds chapters when the list starts at 0:00, has at least 3 timestamps in ascending order, and every chapter lasts at least 10 seconds (YouTube Help, "Add chapters to your videos", https://support.google.com/youtube/answer/9884579). The script below enforces it.

1. **Placement**: at the end of the description, under a "Chapters" heading, one chapter per line, the timestamp at the start of the line.
2. **Count**: 3 to 10 for a video under about 20 minutes; 8 to 15 for a long interview. One distinct topic per chapter; cut at each real change of subject, using the transcript timestamps.
3. **Titles**: 2 to 5 words, descriptive, searchable keywords when natural, no filler article, no ending punctuation. "Introduction" is acceptable for the first one only.
4. **Time format**: `m:ss` under 10 minutes, `mm:ss` from 10 to 59 minutes, `h:mm:ss` beyond an hour.
5. **Two accepted line formats**, pick one per channel and keep it:
   - start only: `1:28 Filter the AI sources`
   - start and end: `1:28 - 2:21 Filter the AI sources` (the end of a chapter is the start of the next one, and the end of the last one is the total duration). The start timestamp stays first on the line so YouTube still reads it.

Example, a 3:58 tutorial for a bakery's online ordering:

```
Chapters
0:00 - 0:11 Introduction
0:11 - 0:31 Why online ordering matters
0:31 - 1:28 Set up the order page
1:28 - 2:21 Add pickup time slots
2:21 - 3:16 Take payment in advance
3:16 - 3:58 First orders and wrap-up
```

## Writing rules

1. Plain, professional, not corporate. Simple words, the audience's words.
2. No em dashes and no spaced dashes used as pauses (they read as machine-written): commas, colons, periods.
3. No bullet points in the prose blocks.
4. No `<` or `>` anywhere: YouTube rejects titles and descriptions that contain them.
5. Fix transcription errors by context: brand names, product names, numbers, names of people.
6. Nothing in the description that the video does not say. A promise the video does not keep costs retention, and retention is what YouTube ranks.
7. Total length under 5000 characters (YouTube's limit); a solo description usually lands between 1200 and 2500.

## Ready-to-use prompts

The two generation prompts (solo and conversation), written with placeholders, are in `references/prompts.md`. Fill the placeholders from the inputs above, paste the transcript at the end, and ask for the description only, with no introduction or comment.

## Check before pasting

Save the description as a text file and run:

```
python3 skills/youtube-description/scripts/youtube_check.py --description description.txt --duration 3:58
```

Add `--title "..."` to check the title and `--thumbnail thumb.jpg` to check the thumbnail in the same pass. The script verifies: chapters start at 0:00, at least 3, ascending, each at least 10 seconds, end of the last chapter equal to the duration (start-and-end format), description under 5000 characters, no `<` or `>`, no em dash, a link on the first line, and UTM parameters on own-site links. Exit code 0 means clean.

## Publishing checklist (shared with the title and thumbnail skills)

A video never goes out without its five elements: the right channel, the title (youtube-title), the description with its chapters (this skill), a custom thumbnail (youtube-thumbnail, never the automatic frame), and the language set correctly. After publishing, open the public page and check that the chapters appear on the progress bar and the thumbnail is the custom one. To fix a video already online, edit the description in YouTube Studio: chapters update without republishing.

## Output format

Deliver, per language: the description in a code block, ready to paste; under it, the script result; then one line listing anything assumed (for example a guest link that was missing and left out).
