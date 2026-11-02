# AI thumbnail prompts (route B and route C)

Write the prompt in English even for a thumbnail in another language; only the words displayed on the image are in the video's language. Attach the reference photo of the person, and the logo file if one appears ("use the attached logo exactly as it is").

## Rules learned by iterating

1. **Describe what you want, never what you do not want.** "No outline" or "no green" plants the word in the image. Describe the wanted state instead: "natural photographic edges, the subject sits inside the scene like a real studio photo".
2. **Name each element by what it looks like**, not only by its position: "the man in the black t-shirt", "the white rounded card".
3. **Give numbers for proportions**: the share of the frame the head takes, which third the subject sits in, how many icons.
4. **Strict palette, in hex codes.** List the brand's colors and say "only". Brand accent colors that drift (a blue turning purple, a green creeping in) are the most common failure.
5. **The key number in one flat, uniform, bright color** with a very thin dark outline: a dark shade, a gradient or a thick outline makes it dull.
6. **Eye contact, written explicitly**: "looks straight into the camera lens, direct eye contact, pupils centered, head facing forward".
7. **Expression and gesture, stated each time**: by default surprised (eyebrows raised, mouth open) with the index finger pointing at the text, hand close to the camera and sharp.
8. **Clothing stated each time**: the reference photo fixes the face, not the outfit. Printed text on clothing must be fully visible in the reference photo and quoted in the prompt.
9. **One detail wrong: retouch, do not regenerate.** Restart from the last image: "Keep everything identical. Change only [the detail]."
10. **Lettering, currency signs, apostrophes and logos are fixed in an editor**, not by regenerating twenty times.
11. When several images are attached, refer to them one by one ("image 1", "image 2"), never as a range.

## Template: face cam (route B)

Replace the bracketed parts. Colors are placeholders: put the brand's own hex codes.

```
YouTube thumbnail, 16:9, 1280x720, ultra sharp, high contrast, clean modern style.

BACKGROUND: smooth gradient from pure white on the left to [LIGHT TINT, e.g. #DCE8FF] on the right, with a soft [ACCENT, e.g. #1E6BFF] light glow behind the subject. Faint [ACCENT TINT] [MOTIF RELATED TO THE TOPIC, e.g. rising line chart, floor plan, calendar grid] in the background, very low opacity.

SUBJECT (right third of the frame, cropped at chest, head takes about 45% of frame height): the person from the reference photo, wearing [OUTFIT]. Looks straight into the camera lens, direct eye contact with the viewer, pupils centered, head facing forward. [EXPRESSION, e.g. shocked and excited: eyebrows raised high, eyes wide open, mouth open in surprise]. Right index finger points left toward the text, hand close to the camera and in sharp focus. Lighting: bright soft key light on the face, cool [ACCENT] rim light from behind that blends the hair and shoulders naturally into the glow of the background. Natural photographic edges, hair strands visible, the subject sits inside the scene like a real studio photo, with a soft ambient shadow.

TEXT (left half, stacked, heavy condensed sans-serif like Anton, all caps, perfectly spelled):
Line 1: "[2 TO 3 WORDS: THE TOPIC]" in white letters on a thick [DARK, e.g. #0A1A3F] paint-brush stroke banner, slightly tilted.
Line 2: "[THE NUMBER OR RESULT]" the largest element, [BRIGHT ACCENT, e.g. #2E8BFF], one single uniform flat color with no gradient, very thin [DARK] outline and a light soft drop shadow. It is the brightest, most eye-catching element of the thumbnail.
Line 3: "[2 TO 3 WORDS: THE CONDITION OR TIME FRAME]" in [DARK], with an [ACCENT] brush stroke underline.

TOP RIGHT, behind the subject's shoulder: one clean white rounded card with soft shadow, titled "[METRIC NAME]", showing "[METRIC VALUE]" in [DARK] and a small [ACCENT] "[CHANGE, e.g. +152%]" badge with white text, with a small [ACCENT] chart. Slightly tilted, partly hidden behind the head.

BOTTOM LEFT, under the text: a row of exactly 3 small [ACCENT] line icons separated by thin grey vertical lines, each with a short caption in [DARK] caps: [ICON 1] "[WORD]", [ICON 2] "[WORD]", [ICON 3] "[WORD]".

Strict color palette: white, [LIGHT TINT], [ACCENT], [BRIGHT ACCENT] and [DARK] only. Every accent in the brand color. Generous spacing between the text block and the subject. Every word readable on a phone at thumbnail size.
```

The card and the icon row are optional: drop them for a simpler thumbnail. Keep the three text lines short; the whole text block stays within 2 to 6 words plus the number.

Sector examples for the three lines:

| Business | Line 1 | Line 2 | Line 3 | Card |
|---|---|---|---|---|
| Dental clinic | NEW PATIENTS | +38 | IN 90 DAYS | Bookings, +41% |
| Restaurant | ONLINE ORDERS | x3 | WITHOUT APPS | Weekly orders, +212% |
| Real estate agent | SOLD IN | 9 DAYS | ABOVE ASKING | Offers received, 14 |
| Software company | CHURN | -27% | ONE EMAIL | Retention, +19% |
| Fitness coach | LOST | 12 KG | NO GYM | Weeks, 16 |

Only real numbers from the video. A thumbnail number the video does not prove is a broken promise.

## Template: interview or podcast (route C, fully generated variant)

Use it to compare with the composed template, or when no cut-out tool is at hand. Attach two or three past episode thumbnails as style references, then the guest photo last.

```
Create a YouTube podcast thumbnail, 16:9, 1280x720, in the same style as the reference thumbnails (images 1 to 3), using only the brand colors [DARK] and [ACCENT]: almost black [DARK] background, plain and smooth, a big [ACCENT] glow behind the guest, the guest very large on the right half, head in the upper third, cropped at the chest, looking into the camera, with a bright [ACCENT] rim light. The guest is the person in the last image: keep the face, hair and clothes strictly identical, clean studio lighting, ultra sharp.
Left side: a short title in a heavy bold white sans-serif, every line exactly the same width (justified block, shorter words are bigger), perfectly spelled:
Line 1: "[WORD]"
Line 2: "[WORD]"
Line 3: "[WORD]"
Line [N] sits inside a solid [ACCENT] rectangle with white text.
Small channel logo in the top left corner, nothing else written.
```

Check the spelling of every word on the result before using it.
