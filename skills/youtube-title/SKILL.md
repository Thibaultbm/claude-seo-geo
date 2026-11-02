---
name: youtube-title
description: "Write YouTube video titles that get found and clicked, for any business or sector. Input: the transcript or the topic, the video type (tutorial, explainer, definition, case study with a result, product demo, interview or podcast, news), the main keyword and the language. Output: 8 to 10 candidate titles built on proven patterns, each scored on keyword position, length, promise kept by the video and fit with the thumbnail text, one recommended title per language, and the matching 2 to 6 word thumbnail hook. Use to title a new video, rename one that underperforms, title a podcast episode or a series, write titles in several languages, or pair a title with its thumbnail."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# YouTube Title: Found in Search, Clicked in the Feed

The title and the thumbnail are read together, in under a second. The title carries the search keyword so YouTube, Google and AI engines know what the video answers; the thumbnail carries the emotional hook or the result. They complete each other and never repeat each other word for word. This skill writes the title and hands the hook to youtube-thumbnail.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: target keywords, audience and personas, the house writing rules (form of address, capitalization, forbidden words) and the titles of past videos with their results. Ground every choice in that context. At the end, record the chosen title and any new rule in the note that owns them.

## When to use this skill

| The user wants | Use this skill? | Where it belongs |
|---|---|---|
| A title for a video, an episode or a series | Yes | here |
| To rename a video that gets impressions but few clicks | Yes | here, after checking the thumbnail too |
| The text written on the thumbnail | Partly | the hook is chosen here, the design in youtube-thumbnail |
| The description and chapters | No | youtube-description |
| The keyword itself (what people search) | No | seo-keyword-research |

## Inputs to collect

1. **What the video actually says**: the transcript, or at least the outline and the strongest moment (a number, a result, a surprising statement). The title only promises what the video delivers.
2. **The main keyword**: the words the audience types, found in YouTube search suggestions, Google's "People also ask", Search Console queries, or seo-keyword-research. One main keyword per video.
3. **The video type** (table below).
4. **The audience and the form of address** the channel uses (formal or informal "you", first person or not). Keep it consistent across the channel.
5. **The languages**: each language gets a title written natively, never a word-for-word translation, with the keyword people search in that language.

## Hard rules

1. **100 characters maximum** (YouTube's limit). Aim for **70 or fewer**: search results and suggested videos cut the end on most screens, and on mobile the first 40 to 50 characters carry the title (field heuristic, it moves with screen and layout).
2. **Main keyword at the start**, or in the first five words. The start is what survives truncation and what search matches first.
3. **One promise, kept.** Every claim in the title is said or shown in the video, ideally in its first 30 seconds. A title the video does not honor loses retention, and retention ranks videos.
4. **No full capitals.** One or two words in capitals for emphasis at most (a number, one key word). A title in all capitals reads as shouting and is harder to scan.
5. **No `<` or `>`** (YouTube rejects them), **no em dash**, no emoji in the title unless the channel deliberately uses one as a signature.
6. **Specific beats generic**: a number, a time frame, a named tool, place or audience. "Set up online orders in 4 minutes" beats "How to grow your bakery".

## Patterns by video type

| Video type | Pattern | Example (any sector) |
|---|---|---|
| Tutorial, how-to | [Keyword]: [result] in [time or steps] | Online ordering for bakeries: set it up in 4 minutes |
| Explainer, definition | [Term]: what it is and [why it matters to the viewer] | Escrow account: what it is and when your notary needs one |
| Case study, result | [Keyword] + [measured result] + [time frame or condition] | Local SEO for dentists: 38 new patients in 90 days |
| Mistakes, warnings | [Number] [keyword] mistakes that [cost] | 5 roofing quote mistakes that cost you thousands |
| Comparison | [Option A] vs [Option B]: [deciding criterion] | Leasing vs buying a work van: which saves more in 2026 |
| Product demo, feature | [Product or feature]: [what it does for the viewer] | Smart scheduling: fill your empty slots automatically |
| Interview, podcast | [Guest's story or result as a statement] (+ guest name if known to the audience) | From one food truck to 12 restaurants without investors |
| News, update | [What changed] + [what it means for the viewer] | New labeling rules: what every food brand must change |
| Series episode | [Keyword] + [episode promise], series label at the end if needed | Bookkeeping basics: read a balance sheet (part 3 of 10) |

For interview titles, lead with the most remarkable outcome or turning point of the guest's story, said as a statement, not with "Interview with [name]": the name only helps when the audience already searches for it.

## Pairing with the thumbnail

1. The title holds the **keyword**; the thumbnail holds the **hook**: 2 to 6 words, ideally a number or a result rather than a theme ("+38 PATIENTS", "4 MIN SETUP", "NO INVESTORS").
2. They never repeat each other word for word: together they tell more than either alone.
3. The hook is true and, ideally, the first sentence of the video says it, so the viewer who clicked hears the promise at once.
4. Hand the chosen hook to youtube-thumbnail.

## Method

1. Extract from the transcript: the main keyword, the strongest concrete element (number, result, time frame, named tool), and the viewer's problem in their own words.
2. Write 8 to 10 candidates across at least three patterns from the table.
3. Score each candidate from 0 to 2 on five criteria: keyword in the first five words; 70 characters or fewer; specific element (number, time, named thing); promise kept by the video; distinct from the thumbnail hook. Drop anything that scores 0 on "promise kept".
4. Recommend the top title, with one alternative for testing. YouTube Studio can test up to three titles or thumbnails against each other on eligible channels ("Test and compare"); when available, test the two best.
5. Check the chosen title:

```
python3 skills/youtube-description/scripts/youtube_check.py --title "Online ordering for bakeries: set it up in 4 minutes"
```

## Renaming a video that underperforms

Read YouTube Studio first. Many impressions with a low click-through rate means the title and thumbnail do not sell the click: rewrite the title, and review the thumbnail with youtube-thumbnail. Few impressions means YouTube does not know where to show it: put the searched keyword at the start of the title and make sure the description's first lines carry it too (youtube-description). Change one element at a time and wait one to two weeks before judging, so the effect is readable.

## Output format

Per language: a table of the candidates with their score, the recommended title and its alternative, the thumbnail hook to hand over, and the result of the check script.
