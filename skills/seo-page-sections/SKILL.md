---
name: seo-page-sections
description: "Generic page auditor and entry point for every page type: runs spec, audit, competitor benchmark and build. Phase 1 spec: site archetype (Shopify, Webflow or WordPress, marketplace), the page types it needs, then the page type's block list plus the common spec and the site-level, header and footer rules (SEC IDs). Phase 2 audit: section_audit.py and seo_audit.py mark rows Pass, Fail or Not verifiable. Phase 3: page_benchmark.py on 3-5 competitors of the same page type. Phase 4: write the missing blocks (FAQ, breadcrumb, definitions, comparison and spec tables, reviews, trust badges, CTA, cross-links), then re-run the scripts as the acceptance test. Covers 21 page types: routes product, collection, service, location, comparison, segment, article and homepage copy to their dedicated skills; owns pricing, about, contact, blog hub, call, author, free tool, wall of love, affiliate, 404, listing, top 10, login. Use when a clean page underperforms, to find the pages and blocks a site lacks, or for a checklist."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "2.0.0"
---

# What is missing on this page, and on this site

Most pages that fail do not fail on tags. They fail because a block that buyers and AI assistants both need is simply absent: no FAQ, no breadcrumb, no comparison, no price in text, no definitions. Most sites that fail are missing a whole page type nobody audited because it does not exist. This skill specifies what a page of a given type must contain, audits it, benchmarks it against the competitors that rank, and writes the missing blocks.

Two audits, two altitudes. `seo-geo-audit` asks "is this site healthy" (crawl, speed, indexation, tags, schema). This skill asks "does this site have the pages it needs, and does each page contain the blocks a page of its type must contain". Run it when the technical layer is already fine and the page still underperforms, or when the deliverable is a build list rather than a diagnosis. It is the entry point for every page type that has no dedicated skill, and for site-level audits.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before writing any block: real product facts, real prices, real client names, positioning, the competitors worth comparing against, and the SEO action log. Every block this skill generates asserts facts about the business, so unsourced invention is the main failure mode. Ground each block in the vault, and append what was added to the vault's SEO action log at the end of the session. Vault structure and protocols: the obsidian-brain skill.

## When to use

- Someone asks what is missing on their site, on a page, or what to add to improve it.
- A page is technically clean, indexed, and still does not rank or get cited.
- A page is being built from scratch and needs its mandatory block list.
- A client-facing checklist is needed: "here is what to add, block by block".
- A template is being designed (Figma, theme, page builder) and the block list must be decided before the design.

When the page type has a dedicated skill (Phase 1, Step 2 table), this skill identifies the type and the site-level gaps, then routes the full page work there. Other adjacent work:

| Need after the gap report | Skill |
|---|---|
| Full page rewrite of a type with a dedicated skill, not just missing blocks | the matching seo-content-* skill, seo-local |
| Real questions to put in the FAQ | seo-keyword-research |
| Schema for the new blocks | seo-schema-markup |
| Cross-link targets and anchors, header and footer link plan | seo-internal-linking |
| Blocks not visible in raw HTML, speed, crawl | seo-technical |
| Whole-site health rather than one page | seo-geo-audit |
| Whether the new blocks got the page cited | geo-visibility, geo-tracking |

## Phase 1. The spec

Built in three steps, because the most expensive gap is not a missing block, it is a page type that does not exist at all. That gap is invisible when auditing only the pages that already exist.

**Step 1, the archetype.** Read `references/site-archetypes.md` now. It gives the three archetypes (Shopify store, Webflow or WordPress site, marketplace), the page inventory each one needs, block lists for the archetype-specific page types, the header and footer rules, and the persuasion levers that apply site-wide. List the page types the site should have and does not (SEC-01) before auditing anything else.

**Step 2, the page type.** Everything downstream depends on this. A missing comparison table is a serious gap on a comparison page and irrelevant on a contact page.

| Type | Recognize it by | Block list (the spec) | Full spec, audit and build | `--type` |
|---|---|---|---|---|
| product | One sellable item, buy box, SKU, Product schema | matrix 1 | seo-content-product-page | product |
| collection | A list of products or listings, filters, category URL | matrix 2 | seo-content-collection-page | collection |
| service | One service sold to one audience, quote or booking CTA | matrix 3 | seo-content-service-page | service |
| location | One physical establishment, NAP, map | matrix 4 | seo-local | location |
| comparison | "X vs Y", "alternatives to X", "best X for Y" | matrix 5 | seo-content-comparison-page | comparison |
| audience | "for agencies", "for freelancers", one segment, same product | matrix 6 | seo-content-comparison-page (segment section) | audience |
| article | Single editorial post, author, date | matrix 7 | seo-content-blog | blog |
| homepage | Root URL, whole-offer overview | matrix 8 | seo-content-homepage (copy and block order), `references/transverse-pages.md` (wireframe) | homepage |
| pricing | Plans, prices, plan comparison | matrix 9 | this skill, `references/transverse-pages.md` | pricing |
| about | Company story, team, proof | matrix 10 | this skill, `references/transverse-pages.md` | about |
| contact | Form, coordinates, hours | matrix 11 | this skill, `references/transverse-pages.md` | contact |
| blog hub | Index of articles, categories, pagination | archetypes | this skill | none (auto) |
| call | Booking widget, slot selection | archetypes | this skill | none (auto) |
| author | One person, bio, list of their posts | archetypes | this skill | none (auto) |
| free tool | Calculator, generator, checker | archetypes | this skill | none (auto) |
| wall of love | Aggregated testimonial wall | archetypes | this skill | none (auto) |
| affiliate | Program terms, commission, signup | archetypes | this skill | none (auto) |
| 404 | Error page | archetypes | this skill (SEC-04) | not benchmarked |
| listing | One marketplace entry | archetypes | this skill (SEC-06) | none (auto) |
| top 10 | Ranked list of options | archetypes | this skill, seo-content-comparison-page (family 3) | comparison |
| login | Authentication, and it should be noindex | archetypes | this skill (SEC-05) | not benchmarked |

"matrix N" is section N of `references/page-type-matrix.md`; "archetypes" is the type's table in `references/site-archetypes.md`.

If a page mixes two types (a service page that also lists products, a homepage that doubles as a pricing page), audit it against both block lists and say so: a merged page usually needs splitting, which is an architecture finding (SEC-02), not a section finding. One intent equals one page.

**Step 3, assemble the checklist.** The spec of one page is three layers, each row with a stable ID:

1. Common requirements C-01 to C-27: `skills/seo-geo-audit/references/common-page-spec.md`. They are not repeated here.
2. The block list of the page type, read from `references/page-type-matrix.md` (or `references/site-archetypes.md` for the archetype-specific types), with its R, W and O levels. Cite each block by its position: `M9.2` is matrix section 9, row 2 (pricing, prices as HTML text); `A-author.3` is the third row of the author page table in site-archetypes.md (hub, call, author, tool, wall, affiliate, 404, listing, top10, login).
3. The SEC rows below: site level (checked once per site), header and footer (checked once per template), page level (checked on every page).

The matrix's universal baseline is covered by C-01, C-02, C-03, C-04, C-15, C-18, C-21, C-23 and by SEC-03, SEC-07 and SEC-21 to SEC-25. Thresholds are field heuristics and house conventions (Sorank master wireframe) unless a source is cited; levels R (required), W (recommended), O (optional) as defined in the matrix.

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| **Site level** | | | | |
| SEC-01 | Every page type the archetype requires exists | 0 required types missing (site-archetypes.md inventory); optional types listed as opportunities | manual (sitemap, navigation, `site:` search) | A missing page type is the most expensive gap and invisible when auditing existing pages |
| SEC-02 | One intent, one page | no two pages carry the same primary keyword; a page mixing two types is split | manual | Cannibalization costs more than a missing block |
| SEC-03 | Every indexable page reachable through header, footer or body links | under 3 clicks from home, no orphan | manual (crawl) | Orphan pages do not rank |
| SEC-04 | Unknown URLs return a real 404 page | HTTP 404 or 410, never 200; same header, footer and navigation; search box and links to the main sections; no noindex as the fix | manual (`curl -sI` on an invented URL), A-404 rows | A soft 404 returning 200 pollutes the index with duplicate empty pages |
| SEC-05 | Login and signup stay out of the index | noindex; nothing that should rank gated behind it; not linked from money-page bodies | seo_audit `noindex` on the login URL (expected there), manual | Zero search value, and it dilutes crawl budget |
| SEC-06 | Marketplace and programmatic templates audited before single pages | the listing template carries unique copy, an attribute table and an editorial layer | section_audit on 3 listings of the template, manual | One template fix corrects every page; thin duplicates at scale are the structural marketplace risk |
| SEC-07 | Organization schema sitewide, page-type schema per page | W; `sameAs` to every official profile | seo_audit `schema_entity`, `schema_none` | Entity clarity (seo-schema-markup) |
| **Header (house conventions)** | | | | |
| SEC-08 | Logo at a fixed size, in a block link to the home page | R | manual | A logo that does not link home breaks expected behavior |
| SEC-09 | Link to the contact page | R, always | manual | Reachability and legitimacy |
| SEC-10 | CTA in a strong contrasting color, pointing to the call or quote page | R | section_audit `cta`, manual | The highest-traffic conversion element on the site |
| SEC-11 | Pillar pages exposed in the navigation | R; dropdown once a category holds more than 3 pages (W); no explicit "Home" link when the header has fewer than 5 links (W) | manual | The header is the strongest internal link source; every slot spent on a low-value page is lost to a page that must rank |
| SEC-12 | Navigation in HTML, same links in the mobile header | R | view-source, seo_audit `likely_js_rendered`, manual mobile check | A JS-only menu removes the primary crawl path for AI crawlers; mobile-first indexing reads the mobile markup |
| **Footer (house conventions)** | | | | |
| SEC-13 | Logo in a block link to home, one-line company description under it | R (logo), W (description) | manual | Consistency with the header; entity repetition on every page |
| SEC-14 | Links to every pillar page, grouped by subject under column headings | R; never a dump of every URL | manual | The footer states the silo structure site-wide; 200 links distribute nothing |
| SEC-15 | Social profile links with `rel="nofollow noreferrer noopener"`, to real profiles (C-20) | R | view-source, seo_audit `social_placeholder` | No authority leak; `noopener noreferrer` closes tab-nabbing and the referrer leak on `target="_blank"` |
| SEC-16 | Links to the legal pages: terms, privacy, cookies, data processing | R | manual | Legal requirement in most markets, and a legitimacy signal |
| SEC-17 | Contact details, or a link to contact | R | section_audit `contact_details`, manual | Reachability from every page |
| SEC-18 | Copyright line with the current year | O | manual | A stale year reads as an abandoned site |
| **Page level** | | | | |
| SEC-19 | Every R block of the page type present and at the section-library bar | 0 R blocks missing or below bar; "present" means visible on the rendered page and in raw HTML (C-21), not only in schema or an unrendered tab | section_audit blocks, manual quality grading | A page of this type without it is incomplete |
| SEC-20 | W blocks present, or their absence documented | each absent W block has a written reason | section_audit blocks, manual | W blocks are present on the pages that win the query |
| SEC-21 | Answer-first opening | the page's core promise in the first 100 words | manual | Both the skimmer and the extractive model read the top first |
| SEC-22 | At least one clear CTA, repeated after long sections | R | section_audit `cta` | A page with no next step converts nothing |
| SEC-23 | Internal links out to the parent and to siblings | R | section_audit `internal_links`, `breadcrumb` | Crawl path and topical context; the anchor text is a ranking signal |
| SEC-24 | Decision blocks above the fold, extraction blocks below | block order matches the type's list | manual | Order beats inventory; every block in the wrong order still converts badly |
| SEC-25 | Mobile layout keeps the same content as desktop; visible freshness signal on time-sensitive pages | R (mobile), W (freshness) | manual, section_audit `freshness_signal` | Mobile-first indexing judges the mobile HTML; assistants prefer content that proves it is current |
| SEC-26 | Every persuasion lever is true | 0 fabricated reviews, logos, ratings, scarcity or deadlines | manual (site-archetypes.md, marketing levers) | Legal exposure, and the fastest way to lose the trust the page exists to build |

## Phase 2. Audit the existing page

Run both scripts on every page in scope (for a site-level audit: one page per type and per template, plus home):

```
python3 skills/seo-page-sections/scripts/section_audit.py --type pricing https://example.com/pricing
python3 skills/seo-page-sections/scripts/section_audit.py --type comparison https://example.com/a https://example.com/b
python3 skills/seo-geo-audit/scripts/seo_audit.py https://example.com/pricing
curl -sI https://example.com/this-page-does-not-exist-7f3a     # SEC-04
```

Use the `--type` value from the Step 2 table; for the archetype-specific types, omit it and read the outline against the type's list.

`section_audit.py` returns per page: page type guess, word count, full heading outline, schema types, table and list counts, internal link count, and a found or not-found verdict with evidence for each block: breadcrumb, FAQ, reviews, rating summary, price in text, comparison table, spec table, definitions, author block, trust badges, guarantee, social proof logos, CTA, process, pricing, verdict, video, images, contact details, opening hours, map, form, freshness, internal links. `seo_audit.py` returns the SEO and GEO scores and the findings codes of audit-checklist.md section 15.

**Map findings to IDs.** Each `seo_audit.py` code maps to a C row (common-page-spec.md lists the codes per row). Each `section_audit.py` block maps to the matrix or archetype row that names it (`price_in_text` to M9.2 on pricing, `faq` to M9.7, `breadcrumb` to C-19) and to SEC-10, SEC-17, SEC-22, SEC-23, SEC-25. Site, header and footer rows are checked by hand on the home page and one deep page. Then mark every row Pass, Fail or Not verifiable, and grade every block with the four states (reference section "Grading").

Read the evidence, not just the checkbox. The detector fires on several independent signals per block (schema type, heading text, markup class, text pattern), in English and French. Known limits and what to do about each:

| Limit | What to do |
|---|---|
| Under 200 words in raw HTML | Distinguish client-rendered from genuinely thin, in a browser. If client-rendered, that finding (C-21) outranks everything: AI crawlers do not execute JavaScript, so they see the same emptiness the parser sees (seo-technical) |
| A block exists but under a name the keyword sets do not cover | The heading outline in the report shows the real section names; correct the verdict by hand |
| Site in a language other than English or French | The keyword sets miss it, so "not found" is unreliable; judge from the heading outline instead |
| A block is present but empty or thin (a FAQ with one question, a two-row spec table) | The detector reports presence, not quality. Grade quality yourself against the section library |
| Page type guessed wrong | Re-run with `--type` |

Presence is never the standard. A FAQ with one generic question counts as missing for the purposes of the report; say "below bar" so the owner knows to rewrite rather than to add.

When the site cannot be crawled (noindex staging, behind a login) or the page does not exist yet, skip this phase: every row is Not verifiable or "new page", and Phase 3 sets the bar.

## Phase 3. Benchmark the competitors

Compare the page with 3-5 competitor pages **of the same page type**: pricing pages against pricing pages, author pages against author pages.

**Pick them.** Search the query the page targets ("{product} pricing", "{brand category} contact", "{thing} calculator", "best {category}"); take the results of the same page type from the first page, then ask two AI assistants the same query and add the pages they cite. For transverse pages with no real query (about, contact), take the same page on the 3-5 direct competitors. Skip directories and marketplaces unless the client is one.

```
python3 skills/seo-geo-audit/scripts/page_benchmark.py --type pricing https://client.com/pricing https://rival1.com/pricing https://rival2.com/pricing https://rival3.com/pricing
```

For the archetype-specific types, omit `--type`. `page_benchmark.py` needs a client URL; when there is none (new page, uncrawlable staging), run `section_audit.py --type <type>` on the competitor URLs alone and build the table by hand.

**Read the output.**

| Output | What it changes in the spec |
|---|---|
| Block x competitor table | The reference for the scorecard and for the acceptance test |
| Blocks half or more of the competitors have and the client does not | A W or O block on that list becomes required for this query (SEC-20 absence needs a reason the competitors did not need) |
| Schema types competitors use and the client does not | Candidate schema rows, only for blocks the page will actually show (C-18) |
| Client below the competitor median (words, bold, H2, question headings, tables, statistics, placement, money links) | The matching C rows (C-08, C-09, C-13, C-14, C-16) move up in priority |
| Client high-severity findings | Fixed before any block is added |

**Site-level benchmark.** Compare page inventories too: open the competitors' navigation, footer and sitemap, and list the page types they have and the client does not (a free tool, an author page per writer, comparison pages, a wall of love). Those go under SEC-01 as opportunities.

**Information gain.** Choose at least one thing the page will have that no competitor has: original numbers, a worked example with real figures, a dated comparison table, a named method, a free tool, the exclusions in a plan table. Name it in the deliverable. The matrix levels are the floor, not the target: match the depth of the pages that already rank for the query.

## Phase 4. Build

1. **Rank the gaps** (reference section "Gap priority"). Three priorities and a backlog, never an undifferentiated list.
2. **Create the missing page types** (SEC-01): the spec of each is its block list; the skeleton is its wireframe.
3. **Write the missing and below-bar blocks.** Read `references/section-library.md` now. Every block has a spec: what it is, why it exists for both audiences, the minimum bar, how to write it, the schema that goes with it and how it fails. Deliver the block, written and ready to paste, in the language of the site. "Add a FAQ" is worthless; three real questions with 40 to 80 word answers is the deliverable.
4. **Use the wireframes.** Homepage, pricing, about and contact: `references/transverse-pages.md` (metadata pattern, skeleton, checks); homepage copy and block order go to seo-content-homepage. Archetype-specific types: the block list in order is the skeleton. Types with a dedicated skill: hand off the full build.
5. **Fix the header and footer** (SEC-08 to SEC-18) as a link plan: which pillar pages take the header slots, the footer columns and their headings, the legal and contact links, the rel attributes.
6. **Schema.** The schema line of each section-library entry; templates in seo-schema-markup. Mark up only what the rendered page shows.
7. **Apply the five rules** (reference section "Rules for every drafted block").

**Acceptance test.** Re-run the Phase 2 commands and `page_benchmark.py` on the built or staged page. The page is done when: no R block is missing or below bar (SEC-19); every block present on half or more of the competitors is present, or its absence is a written owner decision; no high or critical `seo_audit.py` finding; no C row and no SEC row fails, the 404 check returns 404, and the deliverable contains zero em dashes and en dashes (C-25). Every remaining Fail is either fixed or a written owner decision.

## Grading: four block states

Every block in the type's list gets one state. It feeds the Evidence column of the scorecard (Present is a Pass; Below bar and Missing are a Fail; Not applicable is said explicitly).

| State | Meaning | Goes in the report as |
|---|---|---|
| Present | Block exists and meets the bar in the section library | OK, no action |
| Below bar | Block exists but is too thin, too generic, or not in HTML text | Rewrite, with what is wrong |
| Missing | Block absent, and required or recommended for this page type | Add, with the drafted content |
| Not applicable | Block irrelevant to this business or page | Say so explicitly, so the owner does not wonder |

## Gap priority

A page missing eleven blocks does not get an eleven-item to-do list, it gets three priorities and a backlog. Order:

1. Rendering (C-21): on a client-rendered page every "missing" verdict is noise until it is fixed.
2. Missing page types (SEC-01) and merged intents (SEC-02).
3. Blocks that block a purchase decision: price, reassurance, proof.
4. Blocks that AI assistants quote: FAQ, tables, definitions, answer-first passages.
5. Blocks that help crawling: breadcrumb, cross-links, header and footer links.

## Rules for every drafted block

These override everything in the section library.

1. Never invent a fact. Prices, delivery times, certifications, materials, client names, review text and comparison data must come from the vault, the site, or the owner. If a fact is needed and unavailable, write the block with a clearly marked placeholder (`{to confirm: price}`) and list the placeholders at the end of the deliverable as questions for the owner.
2. Never fabricate social proof (SEC-26). Reviews, ratings, logos and case studies must be real and already earned. Marking up a rating that is not displayed, or displaying a review that was never written, is a policy violation and a trust failure.
3. Comparison claims must be checkable. Every row of a competitor comparison must be verifiable on the competitor's own public page on the day it is written, and dated for that reason.
4. The visible page is the source of truth. Schema mirrors what a human can see; feeds export what the page says. A block that exists only in markup is a liability (seo-schema-markup).
5. Never leave an em dash (U+2014) or an en dash (U+2013) in a drafted block (C-25). Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. The em dash is the single most recognizable tell of AI-written text, and one is enough for a reader, or the client, to file the page as machine output. This covers headings, FAQ answers, definitions, table cells, CTA labels and every string you hand over for pasting. Sweep the deliverable for both characters before sending it. Hyphens in compound words and ranges written with "to" are untouched.

## Deliverable

Open with the site-level verdict when the audit covers a site, then the standard five parts per page:

```
SITE: example-store.com   ARCHETYPE: Shopify store
MISSING PAGE TYPES (SEC-01): no author page, no 404 (soft 404 returning HTTP 200, SEC-04)
GLOBAL: header has no contact link (SEC-09); footer links no pillar pages (SEC-14) and
        the social links lack nofollow noreferrer noopener (SEC-15)
```

```markdown
## 1. Spec scorecard
| ID | Requirement | Status (Pass / Fail / Not verifiable) | Evidence |
(C rows, the type's block rows with their state: Present, Below bar, Missing, Not applicable; SEC rows)

## 2. Audit findings
(seo_audit.py scores and high or medium findings, section_audit.py blocks with evidence; or "new page")

## 3. Competitor benchmark
(page_benchmark.py table, blocks and schema types the client lacks, metrics below the median,
page types the competitors have, the information gain chosen)

## 4. Build
(ranked gaps, then the copy block by block, metadata, JSON-LD, internal links, header and footer
link plan; placeholders {to confirm} listed as questions for the owner)

## 5. Acceptance
(scripts re-run: remaining findings, each either fixed or a written owner decision)
```

Lead parts 1 and 4 with the verdict line and the ranked view, the build brief a practitioner reads first:

```
PAGE: /products/ti-stove-2   TYPE: product (full rebuild: seo-content-product-page)
VERDICT: 4 of 11 required blocks missing. The two that cost the most are the FAQ
         (no long-tail capture, nothing for assistants to quote) and the price,
         which is injected by JavaScript and therefore invisible to AI crawlers.

PRIORITY 1  M1.4   Price in HTML text   MISSING (JS-injected)   [fix + why]
PRIORITY 2  M1.9   FAQ block            MISSING                 [3 drafted Q&A]
PRIORITY 3  M1.12  Definitions block    MISSING                 [5 drafted terms]
BACKLOG     M1.1   Breadcrumb           MISSING                 [structure + schema]
            M1.11  Comparison table     BELOW BAR (2 rows)      [drafted table]
OK          H1, gallery, spec table, reviews, cross-links
N/A         Opening hours (no physical store)
```

**Client checklist variant (non-technical owner).** A plain checkbox list per page type, no acronyms, each line explaining what the block is and why it matters in one sentence. This is the format to send to someone who will implement it themselves, including on a site you cannot crawl (noindex, staging, behind a login): Phase 2 is skipped, and the spec of their page types is delivered as a blank checklist they fill in, with the Phase 3 competitor bar when competitors can be crawled.

Both forms: write in the language of the site, lead with what the page already does well, and state what could not be verified and why.

## Common mistakes

- Auditing sections without checking rendering first. On a client-rendered page every "missing" verdict is noise until the rendering issue is fixed.
- Auditing only the pages that exist. The missing page type (SEC-01) is the gap nobody sees.
- Delivering the gap list without the content. The owner already knows the page has no FAQ. The value is the three written questions.
- Adding every block in the library to every page. The matrix marks blocks required, recommended and optional per type for a reason. A bloated page buries the decision.
- Benchmarking against a different page type: a competitor's homepage says nothing about the bar for a pricing page.
- Writing a FAQ from imagination. Real questions come from customer emails, sales calls, on-site search, People Also Ask, Reddit and review complaints (seo-keyword-research).
- Treating a block as done because it exists. A two-line description, a three-row spec table and a one-question FAQ all pass detection and all fail the bar.
- Marking up a block that is not visible. Schema must mirror the rendered page.

## Sources

- AI crawlers do not execute JavaScript (500M+ fetch analysis): https://vercel.com/blog/the-rise-of-the-ai-crawler
- Why ChatGPT cites pages (1.4M prompt study): https://ahrefs.com/blog/why-chatgpt-cites-pages/
- Generative Engine Optimization, effect of statistics, quotations and citations on visibility (controlled study, KDD 2024): https://arxiv.org/abs/2311.09735
- Google structured data must match visible content: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Google guidance on AI features and structured data: https://developers.google.com/search/docs/appearance/ai-features
- Header, footer and archetype inventories: Sorank master wireframe, house conventions. Block levels, word counts and priority order: field heuristics, not Google statements.
