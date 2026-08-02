---
name: seo-page-sections
description: "Find the pages and the on-page sections a site is missing, then write them. Input: a URL (or pasted HTML) and the site archetype. Output: the page types the site should have and does not, then a block-by-block gap report (present, below bar, missing) for each page, plus ready-to-paste content for every gap: FAQ with real buyer questions, breadcrumb, definitions, comparison table, spec table, reviews, trust badges, CTA, cross-links. Covers Shopify, Webflow or WordPress and marketplace archetypes, and 20 page types: product, collection, service, location, comparison, segment, article, blog hub, homepage, pricing, about, contact, call, author, free tool, wall of love, affiliate, 404, listing, top 10, plus header and footer rules. Use when a page is technically clean and still underperforms, when someone asks what is missing on their site, when building pages or templates from scratch, or to produce a client-facing checklist of what to add."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# What is missing on this page

Most pages that fail do not fail on tags. They fail because a block that buyers and AI assistants both need is simply absent: no FAQ, no breadcrumb, no comparison, no price in text, no definitions. This skill compares a page against the reference block list for its type, reports the gaps, and writes the missing blocks.

Two audits, two altitudes. `seo-geo-audit` asks "is this site healthy" (crawl, speed, indexation, tags, schema). This skill asks "does this page contain the blocks a page of this type must contain". Run this one when the technical layer is already fine and the page still underperforms, or when the deliverable is a build list rather than a diagnosis.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before writing any block: real product facts, real prices, real client names, positioning, the competitors worth comparing against, and the SEO action log. Every block this skill generates asserts facts about the business, so unsourced invention is the main failure mode. Ground each block in the vault, and append what was added to the vault's SEO action log at the end of the session. Vault structure and protocols: the obsidian-brain skill.

## When to use

- Someone asks what is missing on their site, on a page, or what to add to improve it.
- A page is technically clean, indexed, and still does not rank or get cited.
- A page is being built from scratch and needs its mandatory block list.
- A client-facing checklist is needed: "here is what to add, block by block".
- A template is being designed (Figma, theme, page builder) and the block list must be decided before the design.

## Phase 1: identify the archetype, then the page types

Do this in two steps, because the most expensive gap is not a missing block, it is a page type that does not exist at all. That gap is invisible when auditing only the pages that already exist.

**Step 1, the archetype.** Read `references/site-archetypes.md` now. It gives the three archetypes (Shopify store, Webflow or WordPress site, marketplace), the page inventory each one needs, block lists for the archetype-specific page types, and the header, footer and persuasion rules that apply site-wide. Report the page types the site should have and does not before auditing anything else.

**Step 2, the page type.** Everything downstream depends on this. A missing comparison table is a serious gap on a comparison page and irrelevant on a contact page.

| Type | Recognize it by | Blueprint owner |
|---|---|---|
| product | One sellable item, buy box, SKU, Product schema | seo-content-product-page |
| collection | A list of products or listings, filters, category URL | seo-content-collection-page |
| service | One service sold to one audience, quote or booking CTA | seo-content-service-page |
| location | One physical establishment, NAP, map | seo-local |
| comparison | "X vs Y", "alternatives to X", "best X for Y" | seo-content-comparison-page |
| audience | "for agencies", "for freelancers", one segment, same product | seo-content-comparison-page (segment section) |
| article | Single editorial post, author, date | seo-content-blog |
| homepage | Root URL, whole-offer overview | references/transverse-pages.md |
| pricing | Plans, prices, plan comparison | references/transverse-pages.md |
| about | Company story, team, proof | references/transverse-pages.md |
| contact | Form, coordinates, hours | references/transverse-pages.md |
| blog hub | Index of articles, categories, pagination | references/site-archetypes.md |
| call | Booking widget, slot selection | references/site-archetypes.md |
| author | One person, bio, list of their posts | references/site-archetypes.md |
| free tool | Calculator, generator, checker | references/site-archetypes.md |
| wall of love | Aggregated testimonial wall | references/site-archetypes.md |
| affiliate | Program terms, commission, signup | references/site-archetypes.md |
| 404 | Error page | references/site-archetypes.md |
| listing | One marketplace entry | references/site-archetypes.md |
| top 10 | Ranked list of options | references/site-archetypes.md |
| login | Authentication, and it should be noindex | references/site-archetypes.md |

If a page mixes two types (a service page that also lists products, a homepage that doubles as a pricing page), audit it against both block lists and say so: a merged page usually needs splitting, which is an architecture finding, not a section finding. One intent equals one page.

## Phase 2: detect what is actually there

```
python3 scripts/section_audit.py https://example.com/products/thing
python3 scripts/section_audit.py https://example.com/a https://example.com/b --type comparison
```

Per page it returns: page type guess, word count, full heading outline, schema types, table and list counts, internal link count, and a found/not-found verdict with evidence for each of these blocks: breadcrumb, FAQ, reviews, rating summary, price in text, comparison table, spec table, definitions, author block, trust badges, guarantee, social proof logos, CTA, process, pricing, verdict, video, images, contact details, opening hours, map, form, freshness, internal links.

Read the evidence, not just the checkbox. The detector fires on several independent signals per block (schema type, heading text, markup class, text pattern), in English and French. Known limits and what to do about each:

| Limit | What to do |
|---|---|
| Under 200 words in raw HTML | Distinguish client-rendered from genuinely thin, in a browser. If client-rendered, that finding outranks everything: AI crawlers do not execute JavaScript, so they see the same emptiness the parser sees (seo-technical) |
| A block exists but under a name the keyword sets do not cover | The heading outline in the report shows the real section names; correct the verdict by hand |
| Site in a language other than English or French | The keyword sets miss it, so "not found" is unreliable; judge from the heading outline instead |
| A block is present but empty or thin (a FAQ with one question, a two-row spec table) | The detector reports presence, not quality. Grade quality yourself against the section library |
| Page type guessed wrong | Re-run with `--type` |

Presence is never the standard. A FAQ with one generic question counts as missing for the purposes of the report; say "present but below bar" so the owner knows to rewrite rather than to add.

## Phase 3: judge against the block matrix

Read `references/page-type-matrix.md` now. It gives, for each of the 11 page types, the required, recommended and optional blocks in page order, with the reason each block exists.

Grade every block in the matrix as one of four states:

| State | Meaning | Goes in the report as |
|---|---|---|
| Present | Block exists and meets the bar in the section library | OK, no action |
| Below bar | Block exists but is too thin, too generic, or not in HTML text | Rewrite, with what is wrong |
| Missing | Block absent, and required or recommended for this page type | Add, with the drafted content |
| Not applicable | Block irrelevant to this business or page | Say so explicitly, so the owner does not wonder |

Rank the gaps. A page missing eleven blocks does not get an eleven-item to-do list, it gets three priorities and a backlog. Rank by: blocks that block a purchase decision first (price, reassurance, proof), then blocks that AI assistants quote (FAQ, tables, definitions, answer-first passages), then blocks that help crawling (breadcrumb, cross-links).

## Phase 4: write the missing blocks

Read `references/section-library.md` now. Every block has a spec: what it is, why it exists for both audiences, the minimum bar, how to write it, and the schema that goes with it.

Do not just name the gap. Deliver the block, written and ready to paste, in the language of the site. "Add a FAQ" is worthless; three real questions with 40 to 80 word answers is the deliverable.

Four rules that override everything in the library:

1. Never invent a fact. Prices, delivery times, certifications, materials, client names, review text and comparison data must come from the vault, the site, or the owner. If a fact is needed and unavailable, write the block with a clearly marked `{placeholder}` and list the placeholders at the end of the deliverable as questions for the owner.
2. Never fabricate social proof. Reviews, ratings, logos and case studies must be real and already earned. Marking up a rating that is not displayed, or displaying a review that was never written, is a policy violation and a trust failure.
3. Comparison claims must be checkable. Every row of a competitor comparison must be verifiable on the competitor's own public page on the day it is written, and dated for that reason.
4. The visible page is the source of truth. Schema mirrors what a human can see; feeds export what the page says. A block that exists only in markup is a liability (seo-schema-markup).

## Phase 5: deliver

Pick the format by audience.

**Format A, build brief (practitioner).** For each block: state, reason, and the drafted content. Order by the priority ranking from phase 3. Open with the verdict line: how many required blocks are missing and what that costs.

```
SITE: example-store.com   ARCHETYPE: Shopify store
MISSING PAGE TYPES: no author page, no 404 (soft 404 returning HTTP 200)
GLOBAL: header has no contact link; footer links no pillar pages and the social
        links lack nofollow noreferrer noopener

PAGE: /products/ti-stove-2   TYPE: product
VERDICT: 4 of 13 required blocks missing. The two that cost the most are the FAQ
         (no long-tail capture, nothing for assistants to quote) and the price,
         which is injected by JavaScript and therefore invisible to AI crawlers.

PRIORITY 1  Price in HTML text        MISSING (JS-injected)   [fix + why]
PRIORITY 2  FAQ block                 MISSING                 [3 drafted Q&A]
PRIORITY 3  Definitions block         MISSING                 [5 drafted terms]
BACKLOG     Breadcrumb                MISSING                 [structure + schema]
            Comparison table          BELOW BAR (2 rows)      [drafted table]
OK          H1, gallery, spec table, reviews, cross-links
N/A         Opening hours (no physical store)
```

**Format B, client checklist (non-technical owner).** A plain checkbox list per page type, no acronyms, each line explaining what the block is and why it matters in one sentence. This is the format to send to someone who will implement it themselves, including on a site you cannot crawl (noindex, staging, behind a login): in that case skip phases 2 and 3 and deliver the matrix for their page types as a blank checklist they fill in.

Both formats: write in the language of the site, lead with what the page already does well, and state what could not be verified and why.

## Common mistakes

- Auditing sections without checking rendering first. On a client-rendered page every "missing" verdict is noise until the rendering issue is fixed.
- Delivering the gap list without the content. The owner already knows the page has no FAQ. The value is the three written questions.
- Adding every block in the library to every page. The matrix marks blocks required, recommended and optional per type for a reason. A bloated page buries the decision.
- Writing a FAQ from imagination. Real questions come from customer emails, sales calls, on-site search, People Also Ask, Reddit and review complaints (seo-keyword-research).
- Treating a block as done because it exists. A two-line description, a three-row spec table and a one-question FAQ all pass detection and all fail the bar.
- Marking up a block that is not visible. Schema must mirror the rendered page.

## Handoffs

| Need after the gap report | Skill |
|---|---|
| Full page rewrite, not just missing blocks | the matching seo-content-* skill |
| Real questions to put in the FAQ | seo-keyword-research |
| Schema for the new blocks | seo-schema-markup |
| Cross-link targets and anchors | seo-internal-linking |
| Blocks not visible in raw HTML, speed, crawl | seo-technical |
| Whole-site health rather than one page | seo-geo-audit |
| Whether the new blocks got the page cited | geo-visibility, geo-tracking |

## Sources

- AI crawlers do not execute JavaScript (500M+ fetch analysis): https://vercel.com/blog/the-rise-of-the-ai-crawler
- Why ChatGPT cites pages (1.4M prompt study): https://ahrefs.com/blog/why-chatgpt-cites-pages/
- Generative Engine Optimization, effect of statistics, quotations and citations on visibility (controlled study, KDD 2024): https://arxiv.org/abs/2311.09735
- Google structured data must match visible content: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Google guidance on AI features and structured data: https://developers.google.com/search/docs/appearance/ai-features
