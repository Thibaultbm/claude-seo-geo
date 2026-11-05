---
name: seo-content-comparison-hub
description: "Spec, audit, competitor benchmark and build for comparison hubs and 'best X' ranking pages that list many items (10 to 60 tools, apps or providers): 'best {category} in {year}', top 10 and ranking pages, tool directories, marketplace comparisons. Runs four phases: the HUB spec on top of the common page spec and shared CMP rows; an audit with seo_audit.py, section_audit.py and the bundled hub_check.py (item count in H1, title, headings and ItemList, table rows, FAQPage, update date and disclosure near the H1); a benchmark against the review sites, directories and listicles that rank or get cited by AI, with page_benchmark.py; then the build: one database feeding hub, item pages, vs and alternatives pages and translations, a published ordering rule, quick picks computed from data, a fixed card per item, a long table usable on mobile, dated third-party ratings with review counts, disclosure when the publisher sells a competing product, ItemList, bulk re-verification. Use for a best X list or ranking hub."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Comparison hubs and "best X" ranking pages

The page a buyer opens to see the whole market at once: "best {category} in {year}", "top 10 {category}", "{category} comparison", a directory of tools. It lists many items (10 to 60) and has to stay true for every one of them, so its unit is not the argument between two options but the list: the order, the card, the table and the database behind them.

It fails in predictable ways: a count that differs between the title, the H1 and the markup ("40+" in one place, 45 cards in another), cards that hold a name and nothing else, a ranking whose order nobody can explain, ratings copied once and never re-read, a "non-sponsored" claim next to an unexplained "partner" badge, and a publisher that ranks its own product first without saying it sells it.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read it before writing: the items already reviewed, the data already collected per item, the commercial relationships with each item (affiliate, sponsor, none), the publisher's own competing product if any, and past verification dates. A hub asserts dozens of facts about third parties, so unsourced invention multiplies the risk by the number of items. Log the page, its item count and the date of each bulk verification to the vault's SEO action log, since that date drives the refresh cycle.

## When to use

- Planning, auditing or writing a "best {category}", "top {n} {category}", "{category} comparison" or tool directory page with 10 or more items.
- A list page exists but its cards are thin, its counts disagree, its order is unexplained, or it has no table.
- Item pages, vs pages or alternatives pages exist without a parent that links them all.
- The page is published in several languages and the numbers drift between them.
- Review sites, directories or affiliates own "best {category}" in the SERP and in AI answers.

| Need | Skill |
|---|---|
| "X vs Y", "{brand} alternatives", "best X for one use case" with 2-8 options, segment pages | seo-content-comparison-page |
| Which ranking queries have demand, and in which languages | seo-keyword-research |
| The item pages (one product or one tool) | seo-content-product-page |
| Category pages of a store (products for sale, facets, pagination) | seo-content-collection-page |
| Linking hub, item, vs and alternatives pages into one web | seo-internal-linking |
| ItemList, FAQPage, BreadcrumbList templates and validators | seo-schema-markup |
| Blocks missing on any page type | seo-page-sections |
| Getting the hub cited on "best {category}" prompts | geo-visibility, geo-tracking |

## Phase 1. The spec

Common requirements C-01 to C-27: skills/seo-geo-audit/references/common-page-spec.md

Shared rows from seo-content-comparison-page, applied as written there and not repeated here: CMP-09 (prices as HTML text with the date checked), CMP-12 (every third-party fact sourced, linked and dated), CMP-13 (methodology block), CMP-14 (visible publication and verification dates, `dateModified`), CMP-22 (comparative advertising conditions, commercial relationship disclosed), CMP-26 (honest claims, no unbacked superlative about yourself).

The rows below are what a hub adds. Thresholds are field heuristics from agency audits and from the November 2026 benchmark of review sites, comparators and directories summarized in `references/hub-patterns.md` (observed, not Google statements) unless marked measured. Every row is required unless its Threshold says "recommended".

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| HUB-01 | One hub per category and language owns the list; item, vs and alternatives pages are its children | no second page ranking for "best {category}"; slug literal and stable (`/best-{category}/`, `/{category}-comparison/`) | manual (seo-keyword-research, Search Console), url_hygiene | Two lists on one term cannibalize; a hub with no children is a dead end |
| HUB-02 | The exact item count and the year in the H1, and the same count everywhere | count and year computed at render from the database; identical in title, H1, intro, table title and ItemList `numberOfItems`; never "40+", "more than 40" | hub_check count_mismatch, h1_no_count, h1_count_not_exact | Two counts on one page is the first inconsistency a reader and a model notice |
| HUB-03 | The answer in the first 3 sentences | the top item, who it suits, 2 alternatives each with its reason, before any list | section_audit "verdict_block", kw_not_in_intro, manual | The passage an assistant quotes; a hub that opens on a list gives nothing to quote |
| HUB-04 | Trust line under the H1 | author with role linked to an author page (C-20), named reviewer recommended, "Updated {date}" | hub_check date_missing, section_audit "author_block", "freshness_signal", author_missing | Provenance in the first screen, where the decision to trust is made |
| HUB-05 | One-line disclosure at the top, linked to the method and the revenue model; every commercial badge explained | 1 line within the first screen; each badge ("partner", "affiliate", "sponsored") defined in one visible sentence | hub_check disclosure_missing, manual | An unexplained badge on a page that claims neutrality reads as a hidden deal |
| HUB-06 | Neutrality that can be checked | the ordering rule is stated on the page; money never changes the order; a paid link has a different label and `rel="sponsored"`; sponsored blocks sit outside the ranking, labelled | manual, hub_check "links with rel sponsored" | Readers trust a mechanism they can see, not a promise (EU ranking transparency, Sources) |
| HUB-07 | A deterministic ordering rule computed from the data | rating, then review count, then name; or a weighted score whose criteria and weights are published; no invented score without published weights | manual (recompute the order from the database) | An order nobody can reproduce is an opinion, and the first thing a listed competitor disputes |
| HUB-08 | The publisher's own competing product, declared | "This page is published by {brand}, which sells {product}" near the top; the product either outside the ranking in a labelled block, or ranked by the same rule with its own cons | manual | Self-ranking without saying so is the fastest way to lose the whole page's credibility |
| HUB-09 | A "best for {use}" label on every item | 1 per item, from its data, distinct across the top 10 | manual, section_audit "verdict_block" | Makes the order defensible and answers the long tail ("best {category} for {use}") |
| HUB-10 | Quick picks computed from the data | 3-8 picks near the top, each with its stated threshold (e.g. "best rated, 20 reviews or more"), each linking to its card anchor | manual | Hand-picked "top picks" next to a data-driven table contradict it |
| HUB-11 | A real comparison table early on the page | `<table>` with a caption, one row per item once beyond 6 items, 4-8 decisive criteria as columns, first column = item name linked to its card, values identical to the cards | hub_check table_missing, table_rows_mismatch, section_audit "comparison_table" | The most extractable block; items as columns stop working beyond about 6 |
| HUB-12 | The table usable on a phone | horizontal scroll container (`overflow-x: auto`, `tabindex="0"`, `role="region"` with a label) with a sticky first column, or stacked cards below a breakpoint; a visible scroll hint | manual (360 px viewport) | A clipped 45-row table is a wall of text on the device most readers use |
| HUB-13 | The same fixed card for every item | numbered heading "{n}. {name}" (h2 or h3), best-for, rating with review count and source, key facts under fixed labels (`<dl>`), pros and cons each with a proof, price with its date, button, link to the full review | hub_check items_not_numbered, numbering_gap, item_no_link, manual | Jagged cards read as bias, and an unnumbered list cannot be checked against its count |
| HUB-14 | Third-party ratings shown honestly | value as the source shows it, with its review count, reading date and a link to the source; "no reviews" shown as such; never rounded up, never invented; re-read at every refresh | manual (bulk re-verification log) | A rating without its count misleads: 5.0 from 1 review is not 4.6 from 3000 |
| HUB-15 | One number, one source | each value (price, rating, count, date) read from one database field and rendered identically in quick picks, table, card, JSON-LD, item page and every language | manual (spot-check 5 items across all surfaces), hub_check count_mismatch | Mismatches between card and table were observed on large review sites; each one is a credibility loss |
| HUB-16 | One database feeds the hub, the item pages, the vs and alternatives pages and every translation | one record per item with fixed fields (Phase 4, step 1); copy holds placeholders, never typed numbers | manual | Typed numbers drift between pages and languages at the first refresh |
| HUB-17 | Concrete methodology, applying CMP-13 | items studied (exact number), criteria and their weights, sources per criterion, update frequency, exclusion rule, who did it | manual | A method with numbers is quotable; "we research thoroughly" is not |
| HUB-18 | "Others considered" and "why not listed" | known names absent from the ranking, each with its reason; closed or changed items moved there with the date | manual | Covers the brands readers expect and proves the list was not cut to fit a deal |
| HUB-19 | Dated changelog | 1 entry per update: date and what changed (items added, removed, ratings re-read, prices checked) | section_audit "freshness_signal", manual | Proves freshness more than a date alone, and records each bulk verification |
| HUB-20 | Real work numbers, never rounded up | "{n} items reviewed, {n} data points, checked on {date}", every figure from the database or the log | manual | An inflated "500+ tested" is the claim a competitor checks first |
| HUB-21 | A web of internal links | hub to every item page; item pages to their alternatives and vs pages; all of them back to the hub and to sibling hubs; links to guides and to the product pages that sell (C-16) | hub_check item_no_link, section_audit "internal_links", site_crawl.py | The hub distributes authority across the set and prevents orphans |
| HUB-22 | One FAQ of real buyer questions, marked up | 5-10 questions, once per page, FAQPage questions identical to the visible ones | hub_check faqpage_missing, faq_jsonld_mismatch, faq_count_mismatch, faq_duplicate, section_audit "faq" | Two FAQs split the answers; markup that the page does not show breaks Google's policy |
| HUB-23 | Schema of a ranking, no empty nodes (applies C-18) | ItemList (`numberOfItems`, ListItem `position`, `name`, `url` in page order) + BreadcrumbList + Article, WebPage or CollectionPage with author and `dateModified`; Review or AggregateRating only for ratings the publisher produced and shows | hub_check itemlist_missing, itemlist_no_url, itemlist_order_mismatch, breadcrumb_missing, datemodified_missing, rating_markup_check, jsonld_invalid | Machines read the list and its order; borrowed third-party ratings as your markup are a policy breach |
| HUB-24 | External sources block | official pages and studies cited, linked, at the end | manual | Provenance a model can follow |
| HUB-25 | Filters and sorting with stable URLs | recommended beyond about 15 items: by use, price band, language or market; one stable URL per useful view, other views canonical to the hub | manual | Long lists need narrowing; uncontrolled filter URLs create duplicates |
| HUB-26 | Question H2s answered first (applies C-13) | 3+ H2s phrased as buyers ask AI assistants, each opened by 2 self-contained sentences | no_question_h2, page_benchmark "question_h" | The passage an assistant lifts must stand alone |

## Phase 2. Audit the existing page

Skip this phase when no hub exists yet; Phase 3 then sets the bar.

1. Inventory: every page targeting "best {category}", "top {category}", "{category} comparison" (Search Console queries, a `site:` search). Two lists on the same term fail HUB-01 before anything else.
2. Run the three collectors:

```
python3 skills/seo-geo-audit/scripts/seo_audit.py https://example.com/best-crm-software/
python3 skills/seo-page-sections/scripts/section_audit.py --type comparison https://example.com/best-crm-software/
python3 skills/seo-content-comparison-hub/scripts/hub_check.py https://example.com/best-crm-software/
```

`hub_check.py` also reads saved files (`hub_check.py page.html`), several pages at once, and exits 1 on a high finding. It reports the counts it found (H1, title, numbered headings, ItemList, table rows, FAQ questions) before the findings, so a mismatch is visible at a glance.

3. Map the output. Each finding code fails the row that lists it in "Verified by": `count_mismatch` HUB-02 and HUB-15, `date_missing` HUB-04, `disclosure_missing` HUB-05, `table_missing` and `table_rows_mismatch` HUB-11, `items_not_numbered`, `numbering_gap` and `item_no_link` HUB-13 and HUB-21, `faq_*` HUB-22, `itemlist_*`, `breadcrumb_missing`, `datemodified_missing` and `rating_markup_check` HUB-23, `em_dashes` C-25. From section_audit: `verdict_block` HUB-03, `author_block` and `freshness_signal` HUB-04 and HUB-19, `comparison_table` HUB-11, `faq` HUB-22.
4. Manual rows. Recompute the order from the data and compare it with the page (HUB-07). Pick 5 items and read each value on every surface: quick picks, table, card, JSON-LD, item page, two other languages (HUB-15). Open the source of 5 ratings and compare value, count and date (HUB-14). Read the disclosure against the badges and buttons actually on the page (HUB-05, HUB-06, HUB-08). Narrow the browser to 360 px (HUB-12).
5. Mark every C row, the shared CMP rows and every HUB row Pass, Fail or Not verifiable, with the evidence.

A hub that ranks is fixed in place: keep the URL, rebuild the template around the same data.

## Phase 3. Benchmark the competitors

1. Pick 3-5 pages from the SERP of "best {category} {year}" in the target language and from the answers ChatGPT, Perplexity and AI Overviews give to the same prompt. Mix the families that show up: review sites, comparators, software directories, a competitor with its own alternatives and vs families, a tech or consumer review site. `references/hub-patterns.md` ("Patterns observed") lists what each family typically does.
2. Run the benchmark and the hub check on the same set:

```
python3 skills/seo-geo-audit/scripts/page_benchmark.py --type comparison https://example.com/best-crm-software/ https://review-site.com/best-crm/ https://directory.com/crm-software/ https://publisher.com/best-crm-tools/
python3 skills/seo-content-comparison-hub/scripts/hub_check.py https://review-site.com/best-crm/ https://directory.com/crm-software/ https://publisher.com/best-crm-tools/
```

3. Read the output: blocks half the competitors have and the client lacks (`comparison_table`, `verdict_block`, `faq`, `author_block`, `freshness_signal`), schema types they use (ItemList, FAQPage, BreadcrumbList; adopt only what the page shows), metrics below the median (`words`, `tables`, `question_h`, `statistics`). Large competitors often fail `count_mismatch` or `itemlist_missing` themselves (observed): consistency is an available gain.
4. Read the pages yourself: the union of their table columns (candidate criteria), their card fields, how they state their order and their revenue model, whether ratings carry a count and a date, what they list as "others considered".
5. Define the information gain in one line: candidates only the client can supply are more items covered with the same depth, fresher and dated third-party data, a reproducible order, a per-item fact that nobody else publishes, honest cons for every item including the publisher's own.

## Phase 4. Build

Read `references/hub-patterns.md` now: the wireframe top to bottom, the card template, the table spec, the disclosure and methodology templates, the quick picks and ordering rules, the JSON-LD templates and both checklists.

### Step 1. The database first (HUB-15, HUB-16)

One record per item, before any copy. Fixed fields: `id`, `name`, `slug`, item page `url`, `status` (listed, considered, closed) with `reason` and date, `best_for`, the key facts under fixed keys (the table columns), `price` with `price_checked_on` and source URL, third-party `rating`, `review_count`, `rating_source_url`, `rating_read_on`, pros and cons each with its proof, `relationship` (none, affiliate, sponsored, own product), `updated_on`. Text fields carry one value per language; numbers and dates exist once and are formatted per locale at render. The hub, the item pages, the vs and alternatives pages and every translation read this database: copy holds `{count}`, `{year}`, `{date}` placeholders and never a typed number. Unknown values stay empty and render as "not published", never guessed; client facts nobody confirmed stay `{to confirm}`.

### Step 2. Order and quick picks (HUB-07, HUB-09, HUB-10)

Sort in code, never by hand: rating (highest first), then review count, then name; or a weighted score with weights published in the method. Read a rating together with its count: decide and state a minimum review count under which a rating does not compete for a quick pick (the threshold is yours; publish it). Quick picks are queries on the database (best rated above the threshold, widest coverage, lowest entry price, longest track record, with an API) and each line links to the card anchor. The best-for label comes from the item's data, not from a slogan.

### Step 3. Write the page block by block

Follow the wireframe. Non-negotiables: count and year in the H1 (HUB-02), the answer in 3 sentences (HUB-03), trust line and disclosure in the first screen (HUB-04, HUB-05, HUB-08), quick picks (HUB-10), the table early and usable on mobile (HUB-11, HUB-12), every item in the same card (HUB-13, HUB-14), the method with real numbers (HUB-17, HUB-20), others considered (HUB-18), the buying guide with question H2s (HUB-26), one FAQ (HUB-22), changelog and sources (HUB-19, HUB-24), the link grid (HUB-21). Beyond about 15 items, show the top cards in full and the rest as compact cards with the same fixed labels, every one still numbered and linked.

Copy rules: prices as text with their date (CMP-09); every third-party fact linked to its source (CMP-12); no superlative about your own product (CMP-26); bold on the deciding facts, never on whole rows (C-09); zero em dashes and en dashes in copy, cards, table cells, metadata and schema strings (C-25).

### Step 4. Neutrality and the publisher's own product (HUB-05 to HUB-08, CMP-22)

State in one line who publishes the page, how it earns money and how the order is set, linked to the method. A paid link gets a different button label and `rel="sponsored"`; an unpaid link to the item page reads the same for every item. Sponsored placements, if any, sit in a block outside the ranking with a "Sponsored" label. If the publisher sells a competing product, say so at the top, and either keep it out of the ranking in its own labelled block or rank it by the same rule with its own cons. Check the ranking transparency rules of the target market (EU: main ranking parameters and paid placement must be disclosed, Sources).

### Step 5. Schema, metadata, translations (HUB-02, HUB-23)

Title: `{count} best {category} in {year}: {what is compared}` (50-60 characters), the count and year from the database. JSON-LD: ItemList in page order from the same sorted array as the table, BreadcrumbList from the visible breadcrumb, FAQPage from the visible FAQ, Article, WebPage or CollectionPage with author and `dateModified`. Templates in the reference; validation in seo-schema-markup. Translations render from the same database and the same sort, so the count, the order and every number are identical in every language; write the source language first, then translate the text fields.

### Step 6. Acceptance test

```
python3 skills/seo-geo-audit/scripts/seo_audit.py https://example.com/best-crm-software/
python3 skills/seo-page-sections/scripts/section_audit.py --type comparison https://example.com/best-crm-software/
python3 skills/seo-content-comparison-hub/scripts/hub_check.py https://example.com/best-crm-software/ https://example.com/fr/meilleurs-crm/
python3 skills/seo-geo-audit/scripts/page_benchmark.py --type comparison https://example.com/best-crm-software/ {the same competitor URLs}
```

Done when: `hub_check.py` exits 0 with no medium finding left unexplained, on every language version; no high or critical `seo_audit.py` finding; `comparison_table`, `verdict_block`, `faq`, `author_block` and `freshness_signal` found; no block half the competitors have still missing; the pre-publish checklist of the reference ticked; the verification date logged in the vault. A remaining Fail is fixed or a written owner decision.

## Maintain: bulk re-verification (HUB-14, HUB-19, CMP-14)

A hub holds dozens of third-party facts that change without notice. Re-verify in bulk, from the database, never page by page from memory.

| Trigger | Action |
|---|---|
| Every month (ratings) or quarter (prices, facts) | Re-read every rating and review count from its source, every price; update the reading dates; re-sort; changelog entry |
| An item closes, merges or changes model | Move it to "others considered" with the date and reason; redirect its item page if retired |
| A new entrant gets real demand or reviews | Add a record, apply the same rule, changelog entry |
| Your own commercial relationships change | Update relationship fields, buttons, the disclosure |

The refresh checklist in the reference lists the order of operations. Keep the URL through every refresh.

## GEO layer (HUB-03, HUB-11, HUB-15, HUB-23)

An assistant asked for "the best {category}" needs a short answer, a list it can trust and a reason per item. The first 3 sentences give the answer, the table and the ItemList give the list, the best-for labels give the reasons, and the consistency of every number across surfaces is what lets a model use the page without contradiction. Adding statistics, quotations and cited sources raised visibility in generative answers in a controlled study (Princeton GEO, KDD 2024, measured). All of it must be in the server HTML (C-21).

## Deliverable

```markdown
## 1. Spec scorecard
| ID | Requirement | Status (Pass / Fail / Not verifiable) | Evidence |
(every C row, the shared CMP rows, every HUB row)

## 2. Audit findings
(inventory and cannibalization check; seo_audit.py, section_audit.py and hub_check.py
output per language; the 5-item consistency spot-check; or "new page")

## 3. Competitor benchmark
(the pages chosen, page_benchmark.py table, hub_check.py on the competitors, criteria union,
card fields union, the information gain chosen)

## 4. Build
(database fields, ordering rule and quick pick thresholds, then the page block by block:
metadata, disclosure, table spec, card template filled for 2 items, method, FAQ, JSON-LD,
internal links; {to confirm} for unverified facts)

## 5. Acceptance
(scripts re-run on every language: remaining findings, each fixed or a written owner decision;
next bulk verification date)
```

## Common mistakes

- A count that differs between the title, the H1 and the markup, or a rounded "40+".
- Cards with a name and a badge only: a list of names compares nothing.
- An order nobody can reproduce, or an order that follows commissions.
- "Top picks" chosen by hand above a data-driven table.
- A rating shown without its review count, its source or its reading date, or rounded up.
- A "non-sponsored" claim next to an unexplained "partner" or "affiliate" badge.
- Ranking your own product first without saying you sell it.
- Numbers typed into the copy, so the card, the table and the translations drift apart.
- Items as table columns on a 40-item list, or a wide table with no mobile behavior.
- Two FAQs on one page, or FAQPage markup that the page does not show.
- Third-party ratings marked up as your own AggregateRating.

## Sources

- Google, carousel and ItemList structured data (summary page with a list of item pages): https://developers.google.com/search/docs/appearance/structured-data/carousel
- Google structured data policies (markup must match visible content): https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Google review snippet guidelines (who may mark up a rating): https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- Google, write high quality reviews (evidence, measurements, what sets items apart): https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews
- Google, qualify outbound links (`rel="sponsored"`): https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- Directive (EU) 2019/2161, ranking transparency and disclosure of paid placement in ranking results: https://eur-lex.europa.eu/eli/dir/2019/2161/oj
- Directive 2006/114/EC on comparative advertising (via CMP-22): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32006L0114
- Generative Engine Optimization (KDD 2024): https://arxiv.org/abs/2311.09735
- Benchmark of review sites, bank comparators, software directories, a SaaS with alternatives, vs and apps page families, and a tech review site, observed November 2026: `references/hub-patterns.md`, "Patterns observed".
- Common page spec and shared CMP rows: skills/seo-geo-audit/references/common-page-spec.md, skills/seo-content-comparison-page/SKILL.md.
- Card fields, 6-item table threshold, 15-item filter threshold, 5-10 FAQ questions, refresh cadence: field heuristics, not Google statements.
