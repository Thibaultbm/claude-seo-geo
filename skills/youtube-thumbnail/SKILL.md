---
name: youtube-thumbnail
description: "Design YouTube thumbnails that stay readable on a phone and match the brand, for any business or sector. Input: the video, its title, the 2 to 6 word hook, the brand colors and fonts, and the video type (screen recording or motion design, face cam, interview or podcast, recurring series). Output: the right production route (a frame from the video plus set text with no AI image, an AI image from a reference photo with a tested prompt template, a cut-out guest template, or an HTML template rendered in batch), a 1280x720 file under 2 MB per language, and the readability check at small sizes. Use to create, redesign or test a thumbnail, write an image-generation prompt for one, build a thumbnail template for a series or a podcast, or fix a thumbnail that gets few clicks."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# YouTube Thumbnail: Readable at Phone Size, True to the Video

Most viewers see a thumbnail at the size of a stamp, next to a dozen others. A thumbnail works when, at that size, one face or one image and two to six words make the promise obvious, in the brand's colors, and when the video keeps that promise. The automatic frame YouTube proposes is never accepted.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: the brand guidelines (colors with their hex codes, fonts, logo files), the reference photos of the people who appear on camera, and past thumbnails with their click-through rates. At the end, record the validated template and any new rule in the note that owns them.

## When to use this skill

| The user wants | Use this skill? | Where it belongs |
|---|---|---|
| A thumbnail, a template, or an image prompt for one | Yes | here |
| To choose the words on the thumbnail | Partly | the hook comes from youtube-title, its layout is here |
| The title or the description | No | youtube-title, youtube-description |
| Branded visuals for other platforms | No | social-amplification |

## Fixed specifications

1. **1280x720 pixels, 16:9**, JPEG or PNG, **under 2 MB** (YouTube's limit for custom thumbnails; the account must be verified to upload one).
2. **One thumbnail per language**: the text is rewritten in each language, never left in the original.
3. **Name the file like the video** (`<video-file-name>.jpg`) and store all thumbnails in one folder, so any video's thumbnail can be found and reused.
4. **Keep the bottom right corner free**: YouTube prints the duration there.
5. **Readability test**: shrink the thumbnail to 320x180, then to 168x94 (suggested videos on desktop). The main text must stay readable at 320x180 and the subject recognizable at 168x94. If not, cut words or enlarge them; never shrink the text to fit more.

## The text grammar

1. **2 to 6 words.** A number or a result beats a theme ("+38 PATIENTS" beats "DENTAL MARKETING").
2. **Two levels at most**: a big title in the brand's darkest color, in the heaviest weight of a bold sans-serif (Inter Black, Anton, Montserrat Black or the brand font), and one hook line in white on a pill or block in the brand's accent color. One highlighted word or line, never more.
3. **Justified block** for stacked titles: every line the same width, so a short word is written bigger. It reads as one shape.
4. **Never repeat the title word for word.** The title holds the keyword, the thumbnail the hook (see youtube-title).
5. **True**: the hook is said or shown in the video, ideally in its first sentence.
6. **Brand palette only**: the brand's dark color, one accent, white, and one light tint of the accent. No color outside it, so every thumbnail of the channel is recognizable in a feed.

## Choose the route

| Video type | Route | Why |
|---|---|---|
| Screen recording, motion design, product film, explainer | A. Frame from the video plus set text | The thumbnail shows what the video really contains; no AI image that the video does not match |
| Face cam (the creator speaks to the camera) | B. AI image from a reference photo | A strong expression and a clean background are hard to shoot; an image model does it from a real photo |
| Interview, podcast | C. Cut-out guest template | The guest is the hook; one template keeps every episode recognizable |
| Recurring series (definitions, tips, episodes) | D. HTML template rendered in batch | Fifty thumbnails with identical layout, the text auto-fitted |

### Route A: frame from the video, text set on top

1. **Pick the frame**: extract about ten frames between 8 and 70 percent of the duration and keep the richest one. A frame taken at random often falls in a transition and comes out almost blank; a simple proxy is to keep the heaviest JPEG (a frame full of detail weighs more than an empty one). Crop away the bottom strip where subtitles live.

```
ffmpeg -v error -y -ss 42.0 -i video.mp4 -frames:v 1 -vf "crop=iw:ih*0.84:0:0" frame.png
```

2. Make sure the frame is sharp: no motion blur on logos or faces. When two language versions differ, pick for each the frame closest to the other so the pair looks identical apart from the text.
3. **Compose**: enlarge the frame (about 85 to 90 percent of the canvas) or place it as a tilted card on one side, then set the text in the free area with an image library (Pillow) or the HTML template of route D. Use the logos exactly as they appear in the video; never paste a different version on top.
4. No AI-generated image in this route.

### Route B: AI image from a reference photo

Use an image model that accepts a reference photo of the person. The prompt template, the rules learned by iterating, and the fix-one-detail method are in `references/ai-prompt.md`. The rules that matter most:

1. Describe what you want, never what you do not want: writing "no outline" makes the model draw an outline.
2. Direct eye contact, a stated expression, and a hand gesture pointing at the text.
3. The subject blended into the scene by a rim light in the brand color, like a real studio photo.
4. Every color given as a hex code from the brand palette, with the instruction that the palette is strict.
5. Text "perfectly spelled", but expect to fix lettering, currency signs, apostrophes and logos afterwards in an editor (Canva, Figma, Photoshop): fix them there, not by regenerating.
6. When one detail is wrong, restart from the last image with "Keep everything identical. Change only..." rather than generating from scratch.

### Route C: interview or podcast template

1. Background: the brand's darkest color, almost black, with **no grid, no stripes, no pattern**, and a large glow in the accent color behind the guest, plus a soft vignette.
2. The guest cut out (background removal), very large on the right half, head in the upper third, cropped at the chest, looking at the camera, sharpened slightly, with a thin glow in the accent color around the silhouette.
3. On the left, a 2 to 6 word title in white, justified block, one line inside a solid block of the accent color.
4. A small channel logo in the top left corner as a signature. No name written by default; add the guest's name in a small pill at the bottom left only when the audience searches for that person.
5. Keep the template fixed across episodes: only the photo and the title change.

### Route D: HTML template for a series

`assets/thumbnail-template.html` is a 1280x720 page with placeholders (series label, term, hook, frame image, logo, brand colors) and a script that shrinks the term until it fits its column on at most two lines. Fill it per video, then render with a headless browser and compress:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --hide-scrollbars --force-device-scale-factor=1 --window-size=1280,720 \
  --virtual-time-budget=4000 --screenshot=thumb.png "file://$PWD/thumb.html"
```

On Linux the binary is `google-chrome` or `chromium`. Convert to JPEG at quality 85 to 92 to stay well under 2 MB (`sips -s format jpeg thumb.png --out thumb.jpg` on macOS, or any image tool).

## Check

```
python3 skills/youtube-description/scripts/youtube_check.py --thumbnail thumb.jpg
```

It verifies the format, the 16:9 ratio, the size and the 2 MB limit. Then open the 320x180 and 168x94 reductions and look at them: the script cannot judge readability.

## Fixing a thumbnail that gets few clicks

In YouTube Studio, compare the click-through rate of the video with the channel's usual rate for the same traffic source. Below it, test a new thumbnail before touching the title: change one thing (the hook, the face expression, the contrast), use "Test and compare" when the channel has it, and wait one to two weeks of impressions before judging.

## Output format

Per language: the route chosen and why, the hook text, the file (or the filled prompt for route B), the result of the check script, and the two small reductions for review.
