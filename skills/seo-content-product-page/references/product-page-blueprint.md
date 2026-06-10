# Product Page Blueprint

Section-by-section anatomy of an optimized PDP, plus the description formula and the ChatGPT Shopping feed mapping. Use this as the build order when creating or rebuilding a product page.

## Page anatomy, top to bottom

| # | Section | Content | Why here |
|---|---|---|---|
| 1 | Breadcrumb | Home > Category > Sub-category > Product, as plain links | Orientation for users, crawl path and BreadcrumbList anchor for bots |
| 2 | H1 + rating summary | Product name as the only H1; stars + review count right next to it | The rating is the strongest objection killer; most visitors never scroll to a bottom review section |
| 3 | Gallery | Real photos: front, back, detail, scale or in-use shot | Trust at the decision point; Merchant Center compliance |
| 4 | Buy box | Price as HTML text, currency, variant selector, add-to-cart | Price in HTML is quotable by AI assistants; price in an image or JS is not |
| 5 | Reassurance badges | Payment security, delivery time and cost, returns window, as text | The three live objections at the moment of decision; machine-readable offer facts |
| 6 | Benefit bullets | 3-5 one-line outcomes | Skimmers decide here; assistants lift these lines verbatim |
| 7 | Description | 150-200+ words, unique, benefits first then specs in use | The ranking surface of the page (SKILL.md section 1) |
| 8 | Spec table | All measurable attributes in an HTML table | Extraction material for assistants and comparison shopping |
| 9 | Comparison table | This product vs the 2 closest alternatives | The passage format quoted in "best X" answers |
| 10 | Reviews list | Full reviews, story format, server-rendered HTML | Social proof depth, long-tail vocabulary, Review markup source |
| 11 | FAQ block | 3+ questions, H3 each, 40-80 word answers | Long-tail capture, objection handling, AI extraction |
| 12 | Definitions block | About 5 technical terms in plain language | Qualifies non-expert buyers, adds topical depth |
| 13 | Cross-links | Parent collection, sister products, supporting blog guide | Internal linking and crawl depth (see seo-internal-linking) |

Order matters: everything a buyer needs to decide sits in sections 1-6 above the fold; everything Google and AI assistants need to understand and quote sits in sections 7-12 below it. Neither audience is sacrificed to the other.

## Description formula

Write in this order, then trim:

1. One sentence naming who the product is for and the main outcome.
2. Benefit paragraph 1: the primary job the product does, with one concrete proof (number, material, certification).
3. Benefit paragraph 2: the differentiator versus the obvious alternative.
4. Characteristics in use: translate each headline spec into what it means for the buyer.
5. Bulleted specs, compatibility, materials, care.

Worked example (camping stove, 168 words):

> The TI Stove 2 is built for hikers who cook two meals a day and count every gram: it weighs 312 g, half the weight of a comparable steel burner.
>
> Its titanium burner head resists corrosion without any coating, so it survives wet packs and salt air. The wide 11 cm pot support holds a 1.5 L pot stable on uneven ground, which is the usual failure point of ultralight stoves.
>
> The piezo igniter lights the burner without a lighter, and the simmer valve goes low enough to cook rice without scorching. A 230 g gas canister runs about 90 minutes at medium output, enough for a week of solo dinners.
>
> - Weight: 312 g including igniter
> - Material: grade 1 titanium burner, stainless valve
> - Boil time: 1 L in 3 min 40 s (sea level, no wind)
> - Fuel: EN 417 threaded canisters
> - Care: hand-wash the burner head, never submerge the valve

## Review display pattern

Format each highlighted review as: first name, buyer situation, problem, result.

> Marie, runs a food truck: "I needed a burner that survives daily transport. Two years in, it still lights on the first click."

Show 2-3 of these as text near the buy box, the full list lower. If video reviews exist, place one above the written list: video outperforms text for conversion (field observation from 115+ agency audits). Every displayed review must be real; markup only what is displayed.

## ChatGPT Shopping feed mapping

The OpenAI product feed spec (https://developers.openai.com/commerce/specs/file-upload/products) accepts JSONL, CSV, TSV, or Parquet, delivered by SFTP push or scheduled fetch, with refresh as often as every 15 minutes. Check the spec for exact field names before building; they evolve. Map feed concepts to on-page sources so the feed and the page never contradict each other:

| Feed concept | On-page source of truth |
|---|---|
| Product id, title | SKU, H1 product name |
| Description | The unique description (never the manufacturer text) |
| Link | Canonical PDP URL |
| Image links | The real photo gallery |
| Price, currency | The HTML price in the buy box |
| Availability | Live stock status, mirrored in Offer markup |
| Ratings and review count | The displayed AggregateRating values |
| Q&A content | The on-page FAQ block |
| Video | The product or review video embedded on the page |
| Shipping, returns | The reassurance badge facts |

Rule: the page is the source of truth, the feed is its export. A feed that promises what the page does not show erodes trust with both buyers and assistants, and inconsistent price or availability data risks removal from shopping surfaces.

Merchant enrollment: https://chatgpt.com/merchants.

## Pre-publish checklist

- [ ] Description 150-200+ words, unique, benefits first
- [ ] All photos real, alt text set
- [ ] Stars + count beside the H1
- [ ] Price, shipping, returns as HTML text
- [ ] Spec table complete
- [ ] Comparison table vs 2 alternatives, factually accurate
- [ ] FAQ 3+ questions, definitions about 5 terms
- [ ] Title, meta description, slug, single H1
- [ ] Product + Offer markup mirrors the visible page (validate with Rich Results Test)
- [ ] curl shows description, price, and reviews in raw HTML
- [ ] Feed entry consistent with the page
