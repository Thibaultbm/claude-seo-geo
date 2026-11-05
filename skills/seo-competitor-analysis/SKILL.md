---
name: seo-competitor-analysis
description: "Market analysis that reads every sitemap of every competitor and finds the keywords, topics and page models they cover and you do not. Always starts by asking the user for up to 5 known competitors, or whether to find them autonomously, before anything runs. Input: your site, plus competitors given or found. Output: competitor_sitemaps.py run on all of them (every sitemap followed, every URL sorted into a page model, publishing pace with real publication dates, slugs turned into topics), a page-model gap table (comparison, alternatives, glossary, free tools, integrations, use cases, locations, case studies, data studies), a topic and keyword gap validated against real demand, the publishing pace to match, and a ranked build plan handed to the page skills. Use for competitor analysis, market analysis, content gap, competitor keywords, 'they publish 200 articles a month', 'which pages do my competitors have that I do not', or scaling content to catch up."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Market analysis: competitor sitemaps, keywords and page models

A competitor's sitemap is its content strategy, published in plain text. Every page model it invested in (comparison pages, alternatives, glossary, free tools, integrations, city pages, case studies), every topic it targets, and how fast it publishes are readable there, without any paid tool. This skill reads all of them, puts them next to the client site, and turns the difference into a build plan.

It answers the three questions a business owner asks when a competitor seems to be accelerating: what are they publishing, how fast, and which of those pages should we build first.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read it before acting: the competitors already listed, the offer, the markets and languages, past competitor analyses and the SEO action log. Competitors found in the vault are proposed to the user in Step 0, never used without asking. At the end, write the competitor list, the date of the run and the top gaps to the vault's competitor note (enrich the existing note, do not create a duplicate).

## Hard rules

1. **Ask before running, every time.** No sitemap is read, no search is made, before the user has answered the Step 0 question. This holds when this skill is called from another skill (seo-geo-audit, seo-keyword-research): the question is asked once, at the start of the whole job.
2. **Five competitors.** Direct competitors that sell the same thing to the same buyer. Fewer than 3 gives no pattern; more than 5 dilutes the gap and slows the run. Marketplaces, media, Wikipedia and review sites are context, not competitors (they go in Step 2 as a separate SERP note).
3. **lastmod is not a publication date.** A sitemap lastmod is an update date, often a build date shared by every URL. Pace claims ("they publish 200 articles in 30 days") come from `--probe` (the page's own publication date) or are stated as an upper bound.
4. **A gap is a hypothesis until demand is validated.** A topic three competitors cover is a candidate. It enters the plan once Search Console, autocomplete or People Also Ask shows people search it (seo-keyword-research, Principle 1).
5. **Never copy a competitor's pages.** The gap tells you which page to build, the page skills tell you how to build a better one (information gain, Phase 3 of every page skill). Volume without quality is what the March 2026 spam update targeted.

## Step 0: the question (mandatory, before anything runs)

Ask exactly this, in the user's language, and wait for the answer:

> Before I start, I need the competitors. Give me up to 5 known competitors of your site (domains are enough). This is optional: do you want me to find them on my own instead? You can also mix both: give me the ones you know and I complete the list.

Three possible answers:

| Answer | What happens |
|---|---|
| A list of 5 | Use it as given. Check each domain answers; report any that does not. |
| A partial list (1 to 4) | Keep them, complete to 5 with Step 1, mark which ones were found. |
| "Find them" | Run Step 1, show the 5 found with one line of reason each, then continue. |

When the tool supports structured questions (AskUserQuestion in Claude Code), ask it with three options: "I give you my competitors", "Find them on your own", "Both". When the vault already lists competitors, show them in the question as a proposal.

## Step 1: find competitors autonomously (only when asked)

Read the client homepage and offer page first: what is sold, to whom, in which language and country. Then collect candidates from four sources and keep the domains that come up in at least two:

1. **Google results on the money queries.** The 5 to 10 queries a buyer types to find this offer (from Search Console when available, otherwise from the offer page and autocomplete). Note who ranks in the top 10, organic and ads.
2. **AI answers.** Ask ChatGPT, Perplexity and Google AI Mode the buyer questions ("best {category} for {segment}", "alternatives to {client}", "{category} tools in {country}"). The brands they name are the competitors buyers will hear about.
3. **Review and comparison sites.** G2, Capterra, Trustpilot, the category's "best of" lists, and "{client} alternatives" pages: who sits next to the client.
4. **The client's own words.** Competitors named on its comparison pages, in sales calls, in the vault.

Rank by overlap of offer and buyer, not by size. Exclude marketplaces, directories, media and generalist giants (they shape the results page but are not beaten with the same pages). Report the 5 chosen and the discarded candidates with the reason, in one table.

## Step 2: read every sitemap

```
python3 skills/seo-competitor-analysis/scripts/competitor_sitemaps.py \
  --site https://client.com \
  --competitors https://a.com https://b.com https://c.com https://d.com https://e.com \
  --probe 40 --json market.json --csv market-urls.csv
```

For each domain the script reads every `Sitemap:` line of robots.txt (falls back to the usual paths: `/sitemap.xml`, `/sitemap_index.xml`, `/wp-sitemap.xml`), follows sitemap indexes into every child file, gzip included, and keeps every URL on the site's own host with its lastmod. Limits: `--max-files` (200 per domain) and `--max-urls` (100000 per domain); the report says "capped" when a limit was hit. It prints five blocks:

1. **Sitemaps**: URLs, files read, where the sitemap was found, lastmod coverage, errors.
2. **Publishing pace**: blog URLs and all URLs with a lastmod in the last 30 and 90 days, plus, with `--probe N`, the real publication dates read on the N most recent blog posts (`article:published_time`, JSON-LD `datePublished`). A warning flags a lastmod shared by more than 30% of the URLs: that site's pace cannot be read from its sitemap.
3. **Page models**: one row per model, the client's count against each competitor, status MISSING (client has none), BEHIND (under half the competitor median) or ok.
4. **Topic gap**: topics (slugs turned into words) covered by at least `--min-sites` competitors (default 2) and by no client URL, with the model and an example URL.
5. **Words** each competitor uses in its slugs and the client never does: the vocabulary of their market.

The CSV holds every URL with domain, language, model and topic: filter it in a spreadsheet to read one competitor's glossary or city pages in full.

When a site has no readable sitemap (blocked, missing, JavaScript only), say so and fall back to a crawl: `python3 skills/seo-internal-linking/scripts/site_crawl.py https://competitor.com`. Never guess its content.

Check by eye: open two or three URLs of each model the script found. URL patterns are heuristics; a `/solutions/` folder can hold use cases or product pages. Correct the reading before reporting.

## Step 3: read the gap

Three readings, in this order:

**Page models first.** A model that 3 of 5 competitors have and the client lacks is the strongest finding: it is a template, so one decision produces dozens of pages. Map each MISSING or BEHIND model to its skill:

| Model found | What it captures | Build with |
|---|---|---|
| comparison, alternatives, best-of list | Buyers choosing between suppliers | seo-content-comparison-page |
| use case, industry, "for {segment}" | Each buyer type with its own words | seo-content-comparison-page (segment pages) |
| glossary, "what is" | Definitions AI assistants quote | seo-content-blog (definition format) |
| free tool, calculator, template | Links and recurring visits | seo-backlinks (linkable asset), seo-page-sections |
| integration | "{client} + {tool}" queries | seo-content-service-page, seo-page-sections |
| location, city | "{service} {city}" queries | seo-local |
| case study, data study, benchmark | Proof, press and AI citations | seo-content-data-study |
| blog post, guide | Informational demand | seo-content-blog |
| category, product | Shopping demand | seo-content-collection-page, seo-content-product-page |

**Topics second.** Merge the script's topic gap with the keyword research: validate each topic against Search Console impressions, autocomplete and People Also Ask (seo-keyword-research, Step 2), drop the ones without evidence, group the rest into clusters, and give each cluster one target page.

**Pace third.** Compare publication counts per 30 days (probe), not lastmod. A competitor publishing 200 articles in 30 days is a fact to verify, then to weigh: open ten of them. Programmatic pages built from one template with a city or a keyword swapped are a risk for them, not a target for the client. Match the useful pace, not the raw count: the usual answer is a steady cadence of pages each better than the best ranking one, plus the templates the competitors prove work.

## Step 4: the build plan

Rank every candidate page by: demand (validated), number of competitors covering it, buyer intent (decision pages first), and effort (a template that produces many pages counts once). Deliver one table:

| # | Page or template | Model | Competitors with it | Demand evidence | Skill | Pages it produces |
|---|---|---|---|---|---|---|

Then the pace to sustain, in pages per month per model, justified by the measured competitor pace. Never dates or durations for the client's work in an audit context (seo-geo-audit rule); a cadence ("4 comparison pages a month") is allowed.

## Deliverable

1. Competitors: the 5 used, given or found, with the reason for each found one.
2. Sitemaps read: the script's block 1, with any site that could not be read.
3. Pace: measured publications per 30 and 90 days per site, stated with its source (probe or lastmod upper bound).
4. Page-model gap table with the skill for each row.
5. Topic and keyword gap, validated, grouped by cluster.
6. The ranked build plan and the cadence.
7. Not verified: sites capped or unreadable, models read from URL patterns only, topics without demand data.

## Common mistakes

| Mistake | Why it fails | Instead |
|---|---|---|
| Running before asking for competitors | The user knows the real ones; the run is wasted on the wrong sites | Step 0, always |
| Taking lastmod as a publication date | Build dates make every site look like it publishes daily | `--probe`, or state an upper bound |
| Listing every slug as a keyword | Slugs are topics, not proven searches | Validate demand (seo-keyword-research) |
| Copying the competitor's page list | Same pages, no information gain, no reason to rank above them | Build the model better than the best one |
| Counting Wikipedia or Amazon as competitors | No page plan beats them on their terms | Note them as SERP context only |

## Sources

- Sitemaps protocol (sitemap index, lastmod): https://www.sitemaps.org/protocol.html
- Google, lastmod is used only when consistently accurate: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google, scaled content abuse (spam policies): https://developers.google.com/search/docs/essentials/spam-policies#scaled-content
- robots.txt Sitemap directive: https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt
