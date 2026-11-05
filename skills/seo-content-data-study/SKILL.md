---
name: seo-content-data-study
description: "Spec, audit, competitor benchmark and build for the pages only your data can make: data studies, benchmarks, industry reports, statistics pages and case studies, with charts, infographics and downloadable data. Turns a company's proprietary data (customer results, usage, orders, tickets, prices) into anonymized aggregates published by category only ('e-commerce store', 'law firm'), never by name, with data_study.py (identifying columns dropped, groups under 5 entities suppressed, median and quartiles, accessible SVG charts and HTML tables). Covers the export, the anonymization rules, the study and case study templates (answer-first findings, charts as text, methodology, dataset download, embed code, Dataset JSON-LD), the live statistics hub, and the outreach that turns numbers into links and AI citations. Use for a data study, original research, statistics page, benchmark report, case study page, infographics, charts on a page, or when a business has data no competitor publishes."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Data studies, benchmarks and case studies from proprietary data

Every company that has customers has data nobody else has: results by type of client, prices by region, delays by season, the questions buyers ask most. Published as numbers, that data does three jobs no other page does. Journalists and bloggers need a source for a statistic and link to the one that has it. AI assistants quote a precise, sourced figure far more readily than an opinion. Buyers trust a measured result from a business like theirs more than any promise.

Competitors cannot copy these pages, because they do not have the data. That is why a data study is the flagship play of seo-backlinks and the strongest information gain a page can carry.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read it before acting: which data exists and where it lives, the consent rules for naming clients, the case study thresholds already decided, the category taxonomy, studies already published. Log each study (dataset, period, sample size, page URL) to the vault's note on studies, enriching the existing note.

## Hard rules

1. **Nobody is identifiable.** Published data names a category, never a company, unless that company gave written consent (case studies, Step 6). No name, domain, logo, exact revenue, city plus niche combination, or screenshot that shows one.
2. **No group under 5 entities.** A category with fewer than 5 distinct entities is suppressed or merged into "Other categories" (the k-anonymity floor; raise it to 10 for sensitive data like revenue or health). With a "Other categories" row hidden, the total minus the published rows can reveal a small group: publish the merged row or no total.
3. **Median first.** One outlier client moves a mean; the median with the 25th to 75th percentile range is the honest headline. The mean appears only in the table.
4. **Every number carries its sample and period.** "Median +145% clicks (62 sites, January to September 2026)". A number without n and dates is not cited and should not be.
5. **Charts are text.** Values, labels and the source are real text (inline SVG or an HTML table under every chart), never only a picture. Crawlers and AI assistants read text; an image of a chart is invisible to them.
6. **Show what goes against you.** If a category does worse, it stays in the chart. A study that only flatters the seller reads as an advert and is not cited.

## When to use

- The business has a database, a CRM, an analytics account or a spreadsheet of results, and publishes nothing from it.
- A competitor analysis (seo-competitor-analysis) shows competitors have "research", "statistics", "benchmark" or "case studies" sections.
- Link building needs a flagship asset (seo-backlinks, Step 5).
- AI assistants cite other sources' statistics on the client's topics (geo-visibility).
- Sales needs proof by client type.

## Phase 1: Spec

| ID | Requirement |
|---|---|
| DS-01 | One question per study, answered in the H1 or the first sentence with the key number ("Law firms get the most from SEO: median +144% clicks in 9 months") |
| DS-02 | Key findings block at the top: 3 to 7 findings, each one sentence with one number, its n and its period |
| DS-03 | One chart per finding, inline SVG or HTML/CSS with text values, a title that states the finding, the source line under it, readable on a phone, light and dark |
| DS-04 | A data table under each chart (or a toggle), with category, n, median, quartile range |
| DS-05 | Methodology block: data source, period, sample size, how entities were selected and excluded, how categories were assigned, the anonymization floor, what the data cannot show |
| DS-06 | Downloadable aggregated dataset (CSV) and the charts as PNG and SVG, free to reuse with credit |
| DS-07 | Embed code under each chart: an `<img>` or `<iframe>` plus a credit link to the study page |
| DS-08 | Author with real credentials and the date of the data; "Updated" date when the data is refreshed |
| DS-09 | Article (or Report-style Article) JSON-LD with author and dates, plus Dataset JSON-LD for the downloadable file (name, description, temporalCoverage, variableMeasured, license, creator, distribution) |
| DS-10 | Stable URL without a year when the study will be refreshed (`/research/seo-results-by-industry`), the year in the title only |
| DS-11 | Category pages when a category is large enough: one page per category with its own numbers, linked from the hub |
| DS-12 | Links from the study to the offer pages each finding supports, and from the blog articles that quote the numbers to the study |

Case study pages add:

| ID | Requirement |
|---|---|
| CS-01 | Named only with written consent; otherwise anonymized as "{category}, {size band}, {country}" |
| CS-02 | A publication threshold decided in advance (for example: result at least x2, minimum volume, minimum duration), applied to every client, so the published set is not cherry-picked |
| CS-03 | Before and after measured from the same source over the same length, from a fixed start (contract start or first delivery), seasonality checked (same month a year earlier) |
| CS-04 | Attribution check: share of the gain coming from what was delivered, excluding brand searches and the client's own work |
| CS-05 | Context, problem, what was done, results with a chart, the time it took, and a quote (named with consent) |
| CS-06 | A hub of case studies filterable by category, each card with its headline number |

## Phase 2: Audit

On an existing study, statistics or case study page:

```
python3 skills/seo-geo-audit/scripts/seo_audit.py https://example.com/research/study
python3 skills/seo-page-sections/scripts/section_audit.py https://example.com/research/study --type blog
```

Then check the DS rows by hand: is the key number in the first sentence, does every number have n and a period, are the charts text or images (select the text in the chart), is there a methodology, a CSV, embed code, Dataset JSON-LD. Search for the study's headline number in Google and in ChatGPT or Perplexity: who quotes it, and do they credit the page with a link.

## Phase 3: Benchmark

Find the studies that already rank or get cited on the topic: search "{topic} statistics", "{topic} study", "{topic} benchmark", "{topic} report {year}", and ask AI assistants "what are the key statistics on {topic}". Run the benchmark on the top 3 to 5:

```
python3 skills/seo-geo-audit/scripts/page_benchmark.py https://client.com/research/study https://a.com/stats https://b.com/report
```

Note for each: sample size, period, freshness, how many findings, chart format, download, embed code, how many domains link to it. The information gain to claim is what they lack: a bigger or fresher sample, a breakdown by category they do not have, a measured result instead of a survey.

## Phase 4: Build

### Step 1. Inventory the data

List what the company holds and what question each source answers. Common sources: product database (usage, results per account), analytics and Search Console (traffic by client type), CRM (deal size, cycle length by segment), support tickets (top questions, resolution time), orders (basket, seasonality, region), public data the company aggregates better than anyone. Pick the question buyers and journalists ask that only this data answers.

### Step 2. Export without the identities

Export only what the study needs, from the source that holds it: a read-only SQL query on the database or warehouse (Postgres, Supabase, BigQuery, Snowflake), an API export, or a spreadsheet. Rules for the export:

- One row per entity (or per event), a category column, the metric columns. Drop names, emails, domains and free text in the query itself whenever possible.
- Pull by date slices on large tables, and count rows per day against the source to check nothing is missing.
- Keep the raw export out of any public repository and any shared folder; the mapping from entity to category is client data.
- Classify each entity by what it sells, from a fixed taxonomy kept in one file, so categories stay stable between refreshes.

### Step 3. Anonymize and aggregate

```
python3 skills/seo-content-data-study/scripts/data_study.py export.csv \
  --category industry --metrics growth_pct,clicks --entity client_id \
  --min-group 5 --unit "growth_pct=%" --source "Acme, 412 sites, January to September 2026" --out study/
```

The script drops the entity column and every column whose name looks identifying (email, name, domain, url, phone, address, company tax numbers, ip, id) plus any listed in `--drop`, counts distinct entities per category, suppresses groups under `--min-group` and merges them into "Other categories" only when the merged group itself reaches the floor, then writes per metric: median, 25th and 75th percentiles, mean, n, share of entities (`aggregates.csv`, `aggregates.json`), a bar chart of medians as accessible SVG (`chart-{metric}.svg`, text labels, title and description for screen readers, source line, light and dark), the matching HTML table (`table-{metric}.html`), the list of suppressed groups and an anonymization report. Read the report before publishing: no category name that points to one known company, no extreme value that identifies an entity.

For a time series, an evolution chart or a share chart, follow the same rules (text values, source, n) and the house chart method of the dataviz skill when it is available.

### Step 4. Write the study page

Order of blocks:

1. H1 that states the main finding, one-sentence answer with the number, n and period.
2. Key findings (DS-02), each linking to its chart.
3. One section per finding: an H2 phrased as the question, two or three sentences of reading, the chart, the table, what it means for the reader's category.
4. Category breakdown: one row or card per category, with a link to the category page when it exists (DS-11).
5. Methodology (DS-05) and limits.
6. Download and reuse: CSV, PNG and SVG charts, embed code, the credit line to use.
7. Author box, dates, and a call to action tied to the finding ("See where your site stands").

Infographic: one tall image that stacks the 3 to 5 key numbers with the source and the URL, for social networks and press. It always comes with the text version on the page; it never replaces it.

Embed code to place under each chart:

```html
<a href="https://example.com/research/study"><img src="https://example.com/research/charts/growth-by-industry.png" alt="Median growth by industry, Example study 2026" width="720"></a>
<p>Source: <a href="https://example.com/research/study">Example, SEO results by industry</a></p>
```

### Step 5. Live statistics hub

When the data refreshes (monthly product data, ongoing measurements), publish a statistics hub instead of a one-off report: a stable URL, numbers rebuilt from the data file at each update, a visible "data through {date}", category pages generated only above the anonymization floor and a minimum volume, and a changelog of what moved. Generate the page from the same JSON the charts read, so the numbers on the page, in the charts and in the download always match. A hub that stays current keeps earning links; a dated report decays.

### Step 6. Case studies

Apply CS-01 to CS-06. A client who has not consented can be asked by email with their own before and after numbers, and the text is submitted to them before publication. When consent is refused, the case is published anonymized ("an online furniture store, 12 employees, France") or aggregated into the study. Never publish a case the threshold excludes, and never one where the gain started before the work, comes from brand searches, or from seasonality.

### Step 7. Distribute

The page earns nothing until someone quotes it. Hand off to seo-backlinks (digital PR: one finding per pitch, sent to the journalists and bloggers who cite older statistics on the topic, plus the unlinked-mention conversion once it is quoted) and to social-amplification (one post per finding, the infographic, the chart as a native image). Add the headline numbers to the offer pages and the blog articles they support (DS-12).

### Step 8. Acceptance

1. `data_study.py` report read: no group under the floor, no identifying column, no category that names a company.
2. Every published number has n and a period; the H1 answer, the key findings, the charts, the table and the CSV give the same numbers.
3. Chart text is selectable; the SVG has a title and a description.
4. Rich Results Test and the Schema.org validator pass on the Article and Dataset JSON-LD (seo-schema-markup).
5. `seo_audit.py` on the published page shows no BLOCKER.

## GEO layer

AI assistants pick the passage that answers the question with a number and a source. Write each finding as a self-contained sentence: "{Category} {result}: median {number} ({n} {entities}, {period}, source {brand})". Keep the brand name inside the sentence so the citation carries it. Use the same wording on the page, in the CSV header, in the Dataset description and in the press pitch, so every copy points back to one source (geo-visibility).

## Deliverable

1. Spec scorecard (DS and CS rows: met, missing, not applicable).
2. Audit findings on the existing page, if any.
3. Benchmark: the studies that rank or get cited, and the information gain claimed.
4. Build: the anonymization report, the aggregates, the charts and tables, the page copy block by block, the JSON-LD, the embed code, the distribution list.
5. Acceptance results.

## Common mistakes

| Mistake | Why it fails | Instead |
|---|---|---|
| Publishing a category with 2 clients | Anyone in the trade knows who they are | Floor of 5, merge or suppress |
| A chart exported as a screenshot | Invisible to crawlers and AI, unreadable on a phone | Inline SVG or HTML with text values |
| The mean as the headline | One big client distorts it | Median and quartile range |
| Only the flattering categories | Reads as an advert, not cited | Every category above the floor |
| A year in the URL of a study that will be refreshed | Each update needs a new URL and loses the links | Stable URL, year in the title |
| Case studies chosen after the fact | Cherry-picking, and buyers sense it | A threshold fixed before, applied to all |

## Sources

- Google, Dataset structured data: https://developers.google.com/search/docs/appearance/structured-data/dataset
- Schema.org Dataset: https://schema.org/Dataset
- Google, creating helpful, people-first content (original information, research): https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- k-anonymity, the minimum group size principle: https://en.wikipedia.org/wiki/K-anonymity
- CNIL, anonymization (European data protection guidance): https://www.cnil.fr/en/anonymisation-personal-data
- W3C, accessible SVG and complex images: https://www.w3.org/WAI/tutorials/images/complex/
