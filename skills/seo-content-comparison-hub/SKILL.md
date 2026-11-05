---
name: seo-content-comparison-hub
description: "The ideal structure of a comparison hub, the 'best X' ranking page that lists many items (10 to 60 tools, apps, providers or platforms): 'best {category} in {year}', top 10 and ranking pages, tool directories, marketplace comparisons. Gives the order of the sections from the head to the footer and, for each section, its role, its content and its organization: H1 with the exact count, short answer, quick picks computed from the data, disclosure and ordering rule, comparison table usable on a phone, the publisher's own offer kept apart, method, one fixed card per item, items considered, buying guide, related pages, FAQ, changelog and sources, author, and the structured data that mirrors the page. Use to plan, write, rebuild or review a best X list or ranking hub."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Comparison hubs and "best X" ranking pages

The page a buyer opens to see a whole market at once: "best {category} in {year}", "top 10 {category}", "{category} comparison", a directory of tools. It lists many items and has to stay true for every one of them, so it is built as a list (an order, a table, one card per item, all read from one database) wrapped in an article (an answer first, a method, a guide, a FAQ).

This skill gives that structure: the sections, in order, and for each one its role, what it contains and how it is organized. For a page comparing two options or the alternatives to one product, use seo-content-comparison-page.

Placeholders: `{count}` (number of items listed), `{year}` (current year) and `{date}` are computed when the page is rendered, never typed. A fact nobody verified stays `{to confirm}`. Every value about an item (rating, price, language, date) comes from one field of the database and is shown identically everywhere it appears.

## Section order

| # | Section | Required |
|---|---|---|
| 0 | Head: title, meta description, structured data | yes |
| 1 | Breadcrumb | yes |
| 2 | Hero: H1, lead, trust line, call to action, visual | yes |
| 3 | Short answer | yes |
| 4 | Quick picks | yes |
| 5 | How this page is made (disclosure and ordering rule) | yes |
| 6 | Comparison table | yes |
| 7 | Publisher's own offer | only if the publisher sells a product of the category |
| 8 | Method: the criteria | yes |
| 9 | The items, one card each | yes |
| 10 | Items considered and not listed | recommended |
| 11 | Buying guide | yes |
| 12 | Related pages | yes |
| 13 | FAQ | yes |
| 14 | Changelog and sources | yes |
| 15 | Author | yes |

Sections 3 to 15 sit in one article column with a table of contents of its H2s (sticky on a wide screen, closed at the top on a phone). Beyond about 15 items, filters and sorting (by use, price band, language or market) go above the table, each useful view with a stable URL, the other views canonical to the hub.

## 0. Head

- Role: make the page found for "best {category}" and readable by machines exactly as people read it.
- Content: title "{count} best {category} in {year}: {what is compared}" (50 to 60 characters, keyword first, brand last); meta description naming 3 criteria and "updated {date}"; JSON-LD: `ItemList` (`numberOfItems` = `{count}`, one `ListItem` per item with `position`, `name`, `url` of its own page, in the page order), `BreadcrumbList` built from the visible breadcrumb, `FAQPage` with the visible questions only, an `Article` or `CollectionPage` with author and `dateModified`.
- Organization: every JSON-LD node built from the same sorted list as the page; nothing marked up that the page does not show; no `Review` or `AggregateRating` for ratings the publisher did not produce (a third-party rating is shown, never marked up as the publisher's own).

## 1. Breadcrumb

- Role: place the hub in the site and give the trail to search engines.
- Content: Home, the parent section if any, the hub.
- Organization: plain links, the hub last, mirrored by the `BreadcrumbList`.

## 2. Hero

- Role: say in one screen what is compared, how many, how fresh and on what terms.
- Content: H1 "The {count} best {category} in {year}" or "Best {category} in {year}: {count} compared"; a lead of 1 or 2 sentences naming the criteria; a trust line (author with role, "Updated {date}", "No paid placement" or the exact commercial terms, "{count} {items} reviewed"); one call to action of the publisher; a visual: a real screenshot or an HTML mockup of the product in the page language, never a generic image.
- Organization: text left, visual right on a wide screen, stacked on a phone with the text first; the social proof the site uses on its heroes under the button; the count in the H1 is the length of the list, the same number as in the title, the table, the card numbering and the `ItemList`.

## 3. Short answer

- Role: the passage a reader skims and an AI assistant quotes.
- Content: 3 to 5 sentences: what the category is, how the list was built, how to choose (the 2 or 3 deciding criteria), and the first move for the reader.
- Organization: first block of the article, in a tinted box with its label ("In short"); self-contained, no link needed to understand it.

## 4. Quick picks

- Role: route the reader who already knows what matters to the right item in one click.
- Content: 3 to 8 picks, each a label stating its rule ("Best rated, 20 reviews or more", "Most languages", "Lowest entry price", "Longest track record", "With an API") and 1 to 3 items with the value that earned the pick.
- Organization: a grid of small cards; every item links to its card anchor (`#item-{slug}`); each pick is computed from the database with its threshold written in the label, never chosen by hand; a pick with no qualifying item is not shown.

## 5. How this page is made

- Role: make the neutrality checkable before the reader trusts the order.
- Content: 3 to 5 lines: who pays and who does not ("No {item} pays to appear or to be placed higher", or the exact affiliate or partner terms); the ordering rule ("by {source} rating, then number of reviews, then name", or a weighted score whose criteria and weights are published); what each commercial badge means; where the data comes from and when it was read; the publisher's own competing product, declared ("This page is published by {brand}, which sells {product}").
- Organization: a framed box right after the quick picks, linked from the trust line; the same rule produces the table, the cards, the `ItemList` and every language.

## 6. Comparison table

- Role: the whole market in one extractable block.
- Content: one row per item: number and name (linking to its card), third-party rating with its review count, then 4 to 8 criteria that decide the choice in the category, in the same order and with the same labels as the card facts; yes/no features in three states ("Yes", "Partial: {detail}", "No"); "not published" for an unknown value, "no reviews" for an item without reviews; a note under the table with the sources and reading dates.
- Organization: a real `<table>` with `<caption>`, `<th scope="col">` headers and the name as `<th scope="row">`; on a phone, a scroll frame (`overflow-x: auto`, `role="region"` with a label, `tabindex="0"`) with the first column sticky and a visible hint ("Scroll sideways to see every column"), or rows turned into stacked blocks with the labels repeated; the page itself never scrolls sideways.

## 7. Publisher's own offer

- Role: present the publisher's product without bending the ranking.
- Content: what the product does differently from the listed items, its price model with a link to its pricing page, one call to action, and the proof the site uses (client logos, ratings with their source).
- Organization: a block visually distinct from the list (the site's call to action style), placed after the table and labelled as the publisher's offer; the product is either outside the ranking or ranked by the same rule as the others, as section 5 says.

## 8. Method: the criteria

- Role: explain what each column and fact measures, so the comparison can be reproduced.
- Content: one line per criterion (name, what is measured, from which source, its weight if a score is used); the number of items studied, listed and excluded; the update frequency; what the page does not rank on and why (for example a price set per site rather than per item).
- Organization: a short list under its H2, criteria in the order of the table columns.

## 9. The items, one card each

- Role: give every item the same fair hearing, and route the reader to the full review.
- Content, per card, always in this order: numbered heading "{n}. {name}" with its logo; "best for {use}" from its data; third-party rating as the source shows it, with its review count and a link to the source page; a 1 or 2 sentence summary; key facts under fixed labels (the table criteria); 2 or 3 pros and 2 or 3 cons when they exist, each a bold claim followed by its proof (a number, a test, a date or a source); price "from {price} ({plan}), checked {date}"; the date of the last update of its review; a link to its own page ("Read the {name} review"); an outbound button labelled by the relationship ("Visit {name}" when unpaid, "Visit {name} (partner link)" with `rel="sponsored"` when paid).
- Organization: one `<article id="item-{slug}">` per item in the page order, inside the article body (never a bare grid of logos); facts as a `<dl>` in two columns on a phone; full cards for the first items and compact cards with the same labels beyond about 15 when the list is long.

## 10. Items considered and not listed

- Role: answer "why is X missing?" before the reader asks.
- Content: name, the reason (closed, no public pricing, outside the category, fewer than {n} reviews) and the date.
- Organization: a small table after the cards; an item that closes or changes moves here with its date.

## 11. Buying guide

- Role: help the reader who is not ready to pick, and cover the questions people ask about the category.
- Content: 4 to 6 H2s phrased as questions ("What is a {category}?", "How to choose a {category}", "How much does it cost?", "Is it risky?", "{category} or {other approach}: what is the difference?"); each opens with 2 self-contained sentences that answer it, then details, a criteria table where useful, official sources linked, and links to the guides and tools of the site.
- Organization: after the cards, in the article body; prices given as ranges taken from the cards, dated. It may close on a decision grid of 4 to 6 lines ("If you need {criterion}: {item}"), each name linking to its card and each line computed from the data like the quick picks.

## 12. Related pages

- Role: spread the reader and the authority across the cluster.
- Content: links grouped by kind: every item page (already linked from the cards), the "best {category} for {use}" child pages, the alternatives and versus pages, sibling hubs, guides and glossary entries, the publisher's feature pages, free tools.
- Organization: a grid of 3 to 6 labelled groups of 3 to 6 links, with descriptive anchors; every target page links back to the hub.

## 13. FAQ

- Role: the real buyer questions, once.
- Content: 5 to 10 questions ("What is the best {category}?", "How much does it cost?", "Is it allowed by {platform rules}?", "How do I check an {item} before buying?", "How can I do without it?", "Is this comparison sponsored?"), answers of 1 to 3 sentences.
- Organization: one accordion of native `<details>` under its H2, mirrored by the `FAQPage`; never a second FAQ elsewhere on the page.

## 14. Changelog and sources

- Role: prove the freshness and the provenance.
- Content: dated entries ("{date}: re-read {n} ratings, checked {n} prices, added {item}, moved {item} to items considered"); the external sources cited in the page (official documentation, studies), linked.
- Organization: two short lists at the end of the article; the latest date is the "Updated {date}" of the hero and the `dateModified`.

## 15. Author

- Role: name who stands behind the judgment.
- Content: photo, name linked to an author page, role and experience of the category, real profiles.
- Organization: a compact box at the top of the side column on a wide screen (above the article on a phone), and the author named in the trust line of the hero.

## Check before publishing

Run `python3 skills/seo-content-comparison-hub/scripts/hub_check.py <url or file.html>` on every language version: it compares the count of the H1, the title, the numbered headings, the table rows and the `ItemList`, and checks the FAQPage, the visible date, the disclosure and the dashes. It exits 1 on a high finding.
