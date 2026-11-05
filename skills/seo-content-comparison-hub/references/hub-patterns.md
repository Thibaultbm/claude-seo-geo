# Comparison hub patterns

Load this file in Phase 4 of seo-content-comparison-hub. It carries the fill-in wireframe, the card and table specs, the text templates, the ordering and quick picks rules, the JSON-LD templates, the refresh and pre-publish checklists, and what the November 2026 benchmark observed.

Placeholders: `{count}` and `{year}` are computed at render from the database and the current date; `{date}` is a database date formatted per locale; `{to confirm}` marks a fact nobody verified.

## Wireframe, top to bottom

```
URL:    /best-{category}/   or   /{category}-comparison/        (literal, stable: HUB-01)
Title:  {count} best {category} in {year}: {what is compared}   (50-60 chars, HUB-02)
Meta:   Compare {count} {category} on {criterion 1}, {criterion 2} and {criterion 3}. Updated {date}.
```

```
1.  [BREADCRUMB]  Home / {parent} / {hub}                                  C-19
2.  [DISCLOSURE LINE]  one line, link to "How this page is made"           HUB-05, HUB-08
3.  [H1]  The {count} best {category} in {year}                            HUB-02
4.  [TRUST LINE]  By {author}, {role}. Reviewed by {reviewer}. Updated {date}.   HUB-04
5.  [ANSWER]  3 sentences: the top item and who it suits, 2 alternatives with their reason   HUB-03
6.  [WORK NUMBERS]  {n} items reviewed, {n} criteria, data checked on {date}   HUB-20
7.  [QUICK PICKS]  3-8 lines, each "{pick label}: {item}" linking to #item-{slug}   HUB-10
8.  [TABLE]  every item a row, 4-8 decisive columns, scroll hint, note with sources and dates   HUB-11, HUB-12
9.  [HOW THIS PAGE IS MADE]  ordering rule, revenue model, badges explained, own product   HUB-05 to HUB-08
10. [CARDS]  one fixed card per item, numbered "{n}. {name}"; full cards for the top ones,
    compact cards (same labels) beyond about 15                            HUB-13, HUB-14
11. [OTHERS CONSIDERED]  name, reason, date; closed or changed items       HUB-18
12. [BEST FOR {USE}]  links to child pages (best X for Y, vs, alternatives) when they exist   HUB-21
13. [METHOD]  items studied, criteria and weights, sources, frequency, exclusion rule, who   HUB-17, CMP-13
14. [BUYING GUIDE]  question H2s, each opened by 2 self-contained sentences   HUB-26
15. [PUBLISHER BLOCK]  the publisher's own offer, labelled, with its limits (only if it sells one)   HUB-08
16. [FAQ]  5-10 real buyer questions, once                                 HUB-22
17. [CHANGELOG]  dated entries: what changed                               HUB-19
18. [SOURCES]  official pages and studies, linked                          HUB-24
19. [AUTHOR BOX]  photo, role, real profiles                               C-20
20. [LINK GRID]  sibling hubs, vs pages, alternatives pages, guides, product pages   HUB-21
```

Beyond about 15 items, add filters (use, price band, language or market) and sorting above the table (HUB-25, recommended). Give each view with its own demand a stable URL; canonical every other view to the hub.

## Per-item card

Same fields, same order, same labels for every item. A missing value renders "not published", never a blank or a guess.

```
<article id="item-{slug}">
  <h3>{n}. {name}</h3>                                          rank in the heading (HUB-13)
  Best for {use}                                                from the data (HUB-09)
  {rating}/5 on {source}, {review_count} reviews, read on {date}   linked to the source page (HUB-14)
  {one-sentence summary}
  <dl>  {fact label 1}: {value}   ...   {fact label n}: {value}  </dl>   fixed labels = table columns
  Pros:  {bold claim}. {proof: number, test, date or source}    2-3
  Cons:  {bold claim}. {proof}                                  2-3, for every item, the publisher's included
  Price: from {price} ({plan}), checked {date}                  CMP-09
  [button]  {label by relationship, below}
  <a href="{item page}">Read the full {name} review</a>         internal link (HUB-21)
</article>
```

Button labels by relationship (HUB-06): no relationship, "Read the {name} review" (internal); affiliate or partner, "Visit {name} (partner link)" with `rel="sponsored"`; sponsored placement, outside the ranking, in a block labelled "Sponsored". The internal review link is present on every card regardless.

Compact card (items beyond the full cards): number and name, best for, rating with count, 3-4 key facts under the same labels, price with date, review link.

## Table spec

- A real `<table>` with a `<caption>`, a `<thead>` with `<th scope="col">`, and the item name as `<th scope="row">` linking to `#item-{slug}`, prefixed by its rank.
- Items as rows once the list has more than about 6 items (columns stop being readable beyond that, observed). 4-8 columns: rating with its count, entry price with date, then the criteria that decide the choice in this category, in the same order as the card facts.
- Every cell reads the same database field as the card. Unknown: "not published". Ratings: value and count, for example "4.5 (312)", or "no reviews".
- A note under the table: "{source} ratings read on {date}. Other facts from each item's own website, dated in its review."
- Mobile (HUB-12), one of:
  1. Scroll container: `<div class="table-wrap" role="region" aria-label="{caption}" tabindex="0">` with `overflow-x: auto`, the first column `position: sticky; left: 0` with a background, and a visible hint above it ("Scroll sideways to see every column").
  2. Stacked cards below a breakpoint: each row becomes a block with the column labels repeated. Keep the `<table>` in the HTML so the extractable structure stays.
- Check at a 360 px viewport: the item name stays visible while scrolling, no column is cut without the hint.

## Text templates

Disclosure line (top of page, one line):

```
No {category} pays to appear on this page or to be placed higher. How we rank and how we earn money: [how this page is made](#how-this-page-is-made).
```

Variant with affiliate links:

```
Some links on this page are partner links: we may earn a commission, at no cost to you. It never changes the order. [How we rank](#how-this-page-is-made).
```

Variant when the publisher sells a competing product (HUB-08):

```
This page is published by {brand}, which sells {product}, a {what it is}. {Product} is [not ranked here / ranked by the same rule as the others]; see [how this page is made](#how-this-page-is-made).
```

"How this page is made" block:

```
- Order: {rule}, for example "{source} rating, then number of reviews, then name". {Weights if a score is used.}
- Money: {revenue model}. {Relationship} never changes the order or the content of a card.
- Badges: "{badge}" means {exact meaning}.
- Data: each fact comes from {sources}; ratings read on {date}; prices checked on {date}.
- Publisher: {brand} sells {product}. {How it is treated on this page.}
```

Methodology (HUB-17, CMP-13):

```
We reviewed {n} {category} ({n listed}, {n considered and excluded}). Each one is compared on the same {n} criteria:
{criterion}: {what is measured, source}, weight {w} (if scored)
Updated {frequency}; ratings re-read {frequency}. An item is excluded when {rule}.
Done by {name, role}, reviewed by {name}. Last full check: {date}.
```

Others considered (HUB-18):

```
| {Item} | Why it is not ranked | Date |
| {name} | {closed / no public pricing / fewer than {n} reviews / outside the category} | {date} |
```

Changelog entry (HUB-19): `{date}: re-read {n} ratings, checked {n} prices, added {item}, moved {item} to others considered ({reason}).`

## Quick picks rules (HUB-10)

1. Each pick is a query on the database, written next to its label: "Best rated ({n} reviews or more)", "Most languages", "Lowest entry price", "Longest track record (founded before {year})", "With an API".
2. A rating competes only above a stated review count threshold. Choose the threshold from the data (how many items would qualify) and publish it; never lower it to promote one item.
3. 1-3 items per pick, ties broken by the ordering rule, each linking to its card anchor.
4. A pick with no qualifying item is not shown.
5. Never a hand-written "our top pick" that the data does not produce.

## Ordering rules (HUB-07)

- Default: rating (highest first), then review count (highest first), then name (alphabetical, locale-independent so every language shows the same order).
- Weighted score: allowed only when every criterion, its scale and its weight are published on the page; the score is computed in code from the database, shown with one decimal at most, and the card shows the sub-scores.
- Items with no rating come after rated items, by name.
- The same sorted array feeds the table, the cards, the ItemList and every language.
- Never: an order typed by hand, an order by commission, a "featured" item placed first inside the ranking.

## JSON-LD templates

ItemList, from the same sorted array as the page (HUB-23):

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "{count} best {category} in {year}",
  "numberOfItems": {count},
  "itemListOrder": "https://schema.org/ItemListOrderDescending",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "{name 1}", "url": "https://example.com/{category}/{slug-1}/" },
    { "@type": "ListItem", "position": 2, "name": "{name 2}", "url": "https://example.com/{category}/{slug-2}/" }
  ]
}
```

FAQPage, from the visible FAQ only (HUB-22):

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "{question exactly as shown}",
      "acceptedAnswer": { "@type": "Answer", "text": "{answer exactly as shown}" } }
  ]
}
```

BreadcrumbList, from the visible breadcrumb:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
    { "@type": "ListItem", "position": 2, "name": "{parent}", "item": "https://example.com/{parent}/" },
    { "@type": "ListItem", "position": 3, "name": "{hub title}", "item": "https://example.com/best-{category}/" }
  ]
}
```

Add Article, WebPage or CollectionPage with `author` (Person with `sameAs`), `datePublished` and `dateModified`. No AggregateRating or Review built from third-party ratings: those stay visible text with their source.

## Refresh checklist (bulk re-verification)

1. Export from the database: every item with its source URLs (rating, pricing, site).
2. Re-read every rating and review count at its source; record value, count and reading date. Never round up; a page that disappeared becomes "no reviews" with the date.
3. Check every price and the facts that change (status, plans, coverage); record date and source.
4. Check item status: closed, merged, renamed, changed model; move to "others considered" with the reason.
5. Add new entrants that meet the inclusion rule.
6. Re-sort in code; let quick picks recompute; read the diff of the order.
7. Update relationship fields and button labels if commercial terms changed.
8. Write the changelog entry; update the page date and `dateModified` only if data changed.
9. Rebuild every language from the same database; run `hub_check.py` on each language version.
10. Log the verification date in the vault and schedule the next one.

## Pre-publish checklist

- [ ] Count and year computed, identical in title, H1, intro, table title, ItemList (HUB-02)
- [ ] Answer in the first 3 sentences: top item, who it suits, 2 alternatives with reasons (HUB-03)
- [ ] Author with role, reviewer, "Updated {date}" under the H1 (HUB-04)
- [ ] Disclosure line at the top, every badge explained, own product declared (HUB-05, HUB-08)
- [ ] Ordering rule stated and reproducible from the data; paid links labelled and `rel="sponsored"` (HUB-06, HUB-07)
- [ ] Best-for label on every item; quick picks computed with stated thresholds (HUB-09, HUB-10)
- [ ] Real table, items as rows, caption, mobile scroll with sticky first column or stacked cards, scroll hint (HUB-11, HUB-12)
- [ ] Same fixed card for every item, numbered, with a link to its review (HUB-13, HUB-21)
- [ ] Every third-party rating with count, source link and reading date (HUB-14)
- [ ] 5-item spot check: same values in quick picks, table, card, JSON-LD, item page, two languages (HUB-15)
- [ ] Method with real numbers, others considered, changelog, sources (HUB-17 to HUB-20, HUB-24)
- [ ] One FAQ of 5-10 questions, FAQPage identical to it (HUB-22)
- [ ] ItemList, BreadcrumbList, `dateModified`; no borrowed ratings in markup (HUB-23)
- [ ] Prices as text with dates; competitor facts sourced; comparative advertising rules checked (CMP-09, CMP-12, CMP-22)
- [ ] Zero em dashes and en dashes in copy, metadata and schema strings (C-25)
- [ ] `hub_check.py` exits 0 on every language version

## Patterns observed

Observed November 2026 on live HTML, or on the latest archived copy when the live page blocked automated reads. Mobile behavior was inferred from the HTML and CSS (scroll containers, sticky elements), not seen on a device. These describe what the pages did on that date, not rules, and they can change.

- VPN review sites (three large publishers). A disclosure line at the very top, an author plus a named fact-checker and an update date under the H1, a short answer naming the top pick, a 5-item quick list, then long cards with a "best for" label, a fact grid, pros and cons and a button. One publisher keeps a dated "recent updates" log; one shows work numbers (hours, services, tests). Tables sit in horizontal scroll containers. Weak points seen: a page whose update date contradicted the test dates in its cards, numbers that differed between card and table, a ranking that the page itself said took commissions into account, and an unpublished weighting behind a proprietary score. ItemList on one of the three; FAQPage on all.
- Bank comparators (one US, two French). A month or year and an item count in the title, a dated note on when rates were read, a "best for" line per item, then cards with fixed labels. The strongest pattern: a different button for partners ("on partner's site") and non-partners ("read review"), and a "why it is not one of our top picks" table for known absent brands. Profile sections ("best for students, travelers, seniors") route to child pages. Weak points seen: a bonus amount that differed between two sections of the same page, a table order that did not follow its own ratings, a comparison declared non-exhaustive because it only listed partners.
- Software directories (two large ones). The page is a list tool: filters in a sidebar, sorting, cards with the rating and its review count, sub-scores, pros and cons counted by review mentions. Paid placements in separate blocks labelled "Sponsored"; one directory's default sort was paid placement, explained in the sort menu. ItemList (18 to 25 items), BreadcrumbList and FAQPage present. A long, sourced buying guide sits below the list.
- A SaaS with alternatives, vs and apps page families. No single hub: three templates (a neutral page per competitor, an "alternative to X" page, an "X vs Y" page), each with a hub of cards, generated from one record per competitor (summary, ideal for, pros, cons, pricing, rating, review count) in many languages. Every page links to the other families, so no page is orphaned. Weak points seen: no statement that the pages are published by a competitor, rating sources not shown, no dates or authors, no ItemList or FAQPage markup despite visible FAQs.
- A tech review site. A breadcrumb, the year in the H1, authors and an update date, an affiliate line under the title, an answer in the second sentence naming the top pick and two alternatives with their reason, a quick overview where each line carries rank, use and price, a weekly news block that gives a reason to update the page without touching the ranking, "other products we tested", and a test frequency stated in the method. Tables in scroll wrappers. Question H2s instead of an FAQ block. Its only ItemList marked up the site navigation, not the ranking.

Across the families: a "best for" label per item was nearly universal; FAQPage was common, ItemList less so; inconsistencies between surfaces of the same page were the most frequent error, including on the largest sites.
