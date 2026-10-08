---
name: seo-content-product-page
description: "Spec, audit, competitor benchmark and build for e-commerce product pages (PDPs), so they rank in Google and get recommended by the AI assistants that now link products directly. Input: a product page URL or a product brief (Shopify, WooCommerce, Magento, BigCommerce, PrestaShop, Wix, Webflow or custom). Runs four phases: the PDP spec with stable IDs on top of the common page spec, an audit with seo_audit.py and section_audit.py --type product, a benchmark against the same product sold elsewhere, marketplace listings and the ranking brands with page_benchmark.py, then the build: unique benefits-first copy, spec and comparison tables, FAQ and definitions blocks, dated rating with count, real photos, price as HTML text, title, H1, slug and meta, out-of-stock and variant handling, Product, Offer and BreadcrumbList schema, the ChatGPT Shopping feed, and a scripted acceptance test. Use to write, rewrite or audit a product page, or when PDPs get no traffic or traffic without sales."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "2.0.0"
---

# Product Page SEO and GEO

A product page (PDP) has two jobs: win the transactional query ("buy X", "X price", the product name) in Google, and be the page an AI assistant quotes when it recommends where to buy. Most PDPs fail both the same way: the manufacturer description every reseller also publishes, supplier photos, a price and reviews injected by JavaScript, a rating buried at the bottom, and markup that contradicts the page. Nothing on the page is unique, so Google picks a stronger domain and the assistant fills the gaps from a competitor.

This skill runs the four phases of the page skill standard (`docs/page-skill-standard.md`): spec, audit, benchmark, build. Rules come from 115+ real agency audits (labeled field heuristics) combined with sourced 2026 practices (labeled measured or documented, with the source).

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use

- Writing or rewriting a product description or a full product page
- Auditing a PDP with no rankings, no traffic, or traffic without sales
- Getting products recommended by ChatGPT, Perplexity, Claude, Gemini or Google AI Overviews
- Handling out-of-stock, seasonal, discontinued or variant product URLs
- Reviewing PDP titles, H1s, slugs, meta descriptions, images, reviews, trust badges or Product schema
- Any storefront: Shopify, WooCommerce, Magento, BigCommerce, PrestaShop, Wix, Webflow Ecommerce, custom

| Case | Skill |
|---|---|
| Category, collection or listing pages (PLPs) | seo-content-collection-page |
| Service or offer pages outside e-commerce | seo-content-service-page |
| "X vs Y", alternatives and best-for pages | seo-content-comparison-page |
| Supporting blog content for a product | seo-content-blog |
| Keyword and intent mapping | seo-keyword-research |
| Whole-site audit | seo-geo-audit |
| Rendering, crawl access, AI crawler behavior, image weight | seo-technical |
| JSON-LD implementation details | seo-schema-markup |
| Passage-level citability writing | geo-visibility |
| Measuring AI citations and referrals | geo-tracking |

## Phase 1. The spec

Common requirements C-01 to C-26: skills/seo-geo-audit/references/common-page-spec.md. Every C row applies to a PDP; the rows below are the product-specific ones. "Verified by" is a `seo_audit.py` finding code, a `section_audit.py --type product` block, or "manual".

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| PDP-01 | Transactional target query | Product name, "buy X", "X price"; the live SERP shows product pages, not guides | manual (SERP check) | Google types result pages by intent; a PDP almost never ranks for an informational query whatever its quality (documented behavior) |
| PDP-02 | Title tag pattern | {Product name} - {Category} \| {Brand}, with the attribute buyers search (material, size, color), unique, about 60 characters (C-01) | title_short, title_long, manual | Standard practice; Google rewrites titles it judges poor (Google title link docs) |
| PDP-03 | H1 is the product name | Exactly one H1 | h1_missing, h1_multiple | Standard practice (C-03) |
| PDP-04 | Descriptive slug | /products/{primary-keyword}, descriptive words, hyphens, no SKU codes or internal IDs | url_hygiene, manual | Measured, correlational: 89.78% of pages ChatGPT cites have descriptive slugs vs 81.11% in the comparison set (Ahrefs) |
| PDP-05 | Handwritten meta description | Benefit + differentiator + one offer fact (shipping or returns), about 150-160 characters (C-02) | meta_missing, meta_short, meta_long, manual | Field heuristic (115+ audits): auto-generated metas repeat the first sentence; offer facts win the click |
| PDP-06 | Unique description, benefits first | 150-200 words minimum, exists nowhere else on the web, never the manufacturer boilerplate; a floor, not a target to pad toward | thin_content, manual (exact-sentence search in quotes) | Field heuristic (115+ audits); Google clusters duplicates and shows one version, usually the strongest domain or the brand |
| PDP-07 | Benefit bullets near the buy box | 3-5 one-line outcomes | manual | Skimmers decide here; assistants lift these lines verbatim |
| PDP-08 | Spec table | Every measurable attribute, compatibility, materials, care, in an HTML table | section_audit spec_table, any_table | Extraction material for assistants and comparison shopping |
| PDP-09 | Comparison table vs alternatives | HTML table, this product vs the 2 closest alternatives; rows price, key specs, ideal use case; every competitor fact accurate and sourced | section_audit comparison_table, no_table | The passage format assistants lift for "best X" answers; keeps the comparison on your page instead of a third-party listicle |
| PDP-10 | FAQ block | 3+ real buyer questions at the bottom, H3 per question, 40-80 word answers, first sentence a standalone fact, text in the HTML | section_audit faq | Field heuristic (115+ audits): long-tail capture, objection handling, AI extraction |
| PDP-11 | Definitions block | About 5 technical terms from the product, 1-3 sentences each | section_audit definitions | Field heuristic (115+ audits): qualifies non-expert buyers, adds topical depth |
| PDP-12 | Dated rating with count beside the H1 | Stars + average + review count next to the title, above the fold; for third-party ratings add platform and the date read ("4.6/5, 312 reviews on Trustpilot, read on 2026-10-01") | section_audit rating_summary, manual (position) | Field heuristic (115+ audits): the strongest objection killer, and about 80% of visitors never scroll to a bottom review section; a dated, counted rating is checkable, a bare star row is not |
| PDP-13 | Real reviews in server HTML | 2-3 story-format reviews (first name + situation + problem + result) near the buy box, full list lower, never fabricated, seeded or undisclosed-incentivized | section_audit reviews, manual | Google spam policies and consumer protection law; the source for Review markup and long-tail vocabulary |
| PDP-14 | Real product photos | Own photos (not supplier stock), multiple angles: front, back, detail, scale or in-use; not AI-generated; alt = product name + distinguishing attribute shown (C-15 for weight and format) | manual (reverse image search), alt_missing, alt_quality | Field heuristic (115+ audits): trust at the moment of payment; supplier photos shared by every reseller are duplicate content and risk Merchant Center disapproval |
| PDP-15 | Price as HTML text | Price and currency in the buy box as text in the server HTML, not in an image or injected by JavaScript; identical to the Offer markup | section_audit price_in_text, likely_js_rendered, curl | Measured: major AI crawlers do not execute JavaScript (Vercel); an assistant cannot quote a price it cannot read |
| PDP-16 | Reassurance facts near the buy button | Payment security, delivery time and cost, returns window, as HTML text, not only icons | section_audit trust_badges, manual | The three live objections at the decision point; machine-readable offer facts the feed also carries |
| PDP-17 | Availability handled | Stock status visible and mirrored in Offer availability; out of stock stays HTTP 200 and indexable, with alternatives | manual (HTTP status, markup vs page) | Keeps rankings while supply returns; availability contradictions get products dropped from shopping surfaces |
| PDP-18 | Variants consolidated | One canonical parent for color and size variants, unless a variant has its own search demand (then an indexable URL with unique content) | canonical_other, manual | Google product variants guidance; avoids splitting signals across near-duplicates |
| PDP-19 | Product + Offer markup, real values only | Product (name, image, description, sku, brand) with nested Offer (price, priceCurrency, availability, url); AggregateRating and Review only when real reviews are displayed; every value identical to the visible page; no empty nodes (C-18) | schema_none, jsonld_invalid, schema_fields, manual (Rich Results Test) | Markup contradicting the page can trigger a structured data manual action (Google structured data policies) |
| PDP-20 | Self-sufficient page in server HTML | Specs, price, shipping, returns, rating, 2-3 reviews, FAQ and comparison all present in the raw HTML (C-21) | likely_js_rendered, render_check.py, curl | The assistant quotes one page, not the site; a missing fact means the product is omitted or the gap is filled from a competitor |
| PDP-21 | Cross-links | Parent collection, sister products, the supporting blog guide, in the body | section_audit internal_links, no_cta_money | Internal linking and crawl depth (seo-internal-linking) |
| PDP-22 | Product feed for ChatGPT Shopping | Feed submitted, refreshed, and consistent with the page (price, availability, ratings, Q&A) | manual | Declared data replaces crawling guesswork; the first GEO action for a store (OpenAI commerce spec) |
| PDP-23 | Video (optional) | Product in use or a video review, with a text summary | section_audit video | Field observation (115+ audits): video outperforms text for conversion where it exists |
| PDP-24 | Size, fit or compatibility guide (optional) | Where the category has a fit or compatibility question | manual | Removes the single biggest return driver in apparel and parts |

How the common rows read on a product page:

| Common row | Product-page reading |
|---|---|
| C-08 length | The description floor is PDP-06; the whole page sits at or above the competitor PDP median from Phase 3 |
| C-09 semantic bolding | Product name bold once in the first paragraph of the description; then one bold phrase every 100-150 words on a measurable fact or benefit (weight, boil time, warranty); never whole sentences |
| C-10 placement | Product name and category term in 60%+ of the zones: title, H1, an H2, meta, slug, first 100 words, bold, image alt |
| C-11 density | No term above 2.5% of content words; repeated variant names and the brand inflate density, judge before rewriting |
| C-19 breadcrumb | Visible Home > Category > Sub-category > Product, plus BreadcrumbList JSON-LD |
| C-20 social profiles | Footer icons link to real profiles, never `instagram.com/` or `#`; the same URLs in the Organization `sameAs` |
| C-24 honest claims | "Best", "n°1", "#1 seller" carry a source next to them or go; regulated products (supplements, cosmetics, alcohol, medical devices, gambling, financial products) carry their legal notices and no health or results promise beyond what is authorized |
| C-25 punctuation | Zero em dashes and en dashes in every delivered field (Phase 4, copy rules) |

## Phase 2. Audit the existing page

When no page exists yet, skip to Phase 3: the benchmark sets the bar for the build.

1. Check the intent first (PDP-01). Search the target query: if the results are guides and listicles, stop and plan a blog post that links to the PDP (see Intent split below).
2. Fetch the page as crawlers see it, then run the two collectors:

```
curl -sL -A "Mozilla/5.0" https://store.com/products/ti-stove-2 -o raw.html
python3 skills/seo-geo-audit/scripts/seo_audit.py https://store.com/products/ti-stove-2
python3 skills/seo-page-sections/scripts/section_audit.py --type product https://store.com/products/ti-stove-2
python3 skills/seo-ai-site-builders/scripts/render_check.py https://store.com/products/ti-stove-2
```

Search `raw.html` for the price, a sentence of the description and a review: anything absent from the raw HTML is invisible to AI assistants and unreliable for Google (PDP-15, PDP-20). `render_check.py` makes the same raw versus rendered comparison when the store runs on a JavaScript framework.

3. Map every finding to a spec row and mark each row Pass, Fail or Not verifiable:

| Script output | Spec rows |
|---|---|
| title_short, title_long, meta_*, h1_*, url_hygiene | PDP-02 to PDP-05, C-01 to C-03, C-23 |
| thin_content, word count | PDP-06, C-08 |
| no_bold, kw_not_bold, kw_placement_low, kw_not_in_intro, keyword_stuffing | C-09 to C-11 |
| section_audit spec_table, comparison_table, faq, definitions | PDP-08 to PDP-11 |
| section_audit rating_summary, reviews | PDP-12, PDP-13 |
| section_audit price_in_text, trust_badges; likely_js_rendered | PDP-15, PDP-16, PDP-20 |
| schema_none, jsonld_invalid, schema_fields; section_audit breadcrumb | PDP-19, C-18, C-19 |
| social_placeholder, social_missing | C-20 |
| superlative_claim, claim_no_disclaimer, gambling_notice_missing | C-24 |
| em_dashes | C-25 |

4. Manual checks the scripts cannot make: search one exact sentence of the description in quotes (duplicate manufacturer text, PDP-06); reverse image search two photos (supplier or AI-generated images, PDP-14); compare every schema value with the visible page and run the Rich Results Test (PDP-19); check the HTTP status and Offer availability of out-of-stock URLs (PDP-17); check the rating sits beside the H1 (PDP-12); check the feed entry against the page (PDP-22).

## Phase 3. Benchmark the competitors

Pick 3-5 product pages, not category pages or listicles, from four sources:

1. **The same product sold elsewhere.** Search the exact product name, model number or GTIN: the brand's own page (when the client is a reseller) and the other retailers carrying the same SKU. These are the pages Google clusters the client's page with; beating them is the whole game when the product is not exclusive.
2. **Marketplace listings.** Amazon, eBay, Cdiscount, Etsy or the vertical marketplace that ranks for the query. Read their bullets, Q&A, review counts and photo sets. Marketplaces often block scripts or pad word counts with boilerplate: read them manually when the script errors, and weigh their metrics accordingly.
3. **The brands ranking for the transactional category query** ("titanium camping stove", "buy ergonomic office chair"): their PDPs show the page shape the SERP rewards.
4. **The pages AI assistants name.** Ask ChatGPT, Perplexity and Google AI Mode "best {product type} for {use}" and "where to buy {product}"; note the PDPs linked and the shopping cards shown.

```
python3 skills/seo-geo-audit/scripts/page_benchmark.py --type product https://store.com/products/ti-stove-2 https://brand.com/ti-stove-2 https://retailer.com/p/ti-stove-2 https://rival.com/products/ultralight-stove
```

What to read in the output:

- **BLOCKS half or more of the competitors have and the client does not**: on a PDP, usually rating_summary, spec_table, faq, comparison_table, video, trust_badges, price_in_text. Each gap is a Fail on the matching PDP row.
- **SCHEMA TYPES competitors use and the client does not**: Product, Offer, AggregateRating, BreadcrumbList, VideoObject. Add only what the page really shows (PDP-19).
- **CLIENT BELOW THE COMPETITOR MEDIAN**: words, bold, tables, statistics, question_h, placement. Those C rows move up in priority.
- **Proof formats**: review counts, photo count, video, warranty length, delivery promise. The competitors' strongest proof is the bar the client's proof must clear.

Then define the information gain: what the client page will say that none of the benchmarked pages says. For a product sold by many resellers, this is the only thing that separates the page from the cluster. Candidates: own photos and measured test results ("1 L boiled in 3 min 40 s, measured at sea level"), real-use numbers from customers, answers taken from your own support tickets and pre-sales emails, a compatibility list, a size guide built from return data, the comparison table versus the two closest alternatives, story-format reviews, a demo video. Write the chosen gain into the build brief before any copy.

## Phase 4. Build

### 4.1 Collect the facts

Pull from the vault, the product information system or the owner. Unknowns stay `{to confirm}`, never invented.

| Fact | Used in |
|---|---|
| Target query, product name as buyers type it, category term, buyer attributes | Title, H1, slug, first 100 words |
| Who it is for, the top 3 outcomes, with proof (numbers, materials, certifications) | Description, benefit bullets, bold |
| Full specs, compatibility, materials, care | Spec table, definitions |
| Price, currency, variants, stock status, restock date | Buy box, Offer markup, feed |
| Shipping cost and time, returns window, payment methods, warranty | Reassurance facts, meta, feed |
| Rating, review count, platform, date read; 2-3 real reviews with permission | Rating summary, reviews, AggregateRating |
| The 2 closest alternatives with sourced specs and prices | Comparison table |
| Real buyer questions (pre-sales emails, support tickets, People Also Ask, reviews) | FAQ |
| Own photos and video; real social profile URLs | Gallery, footer, `sameAs` |

### 4.2 Wireframe

Build order, top to bottom. Full block specs, the description formula with a worked example, the review display pattern and the pre-publish checklist: `references/product-page-blueprint.md`.

1. Breadcrumb (C-19)
2. H1 + dated rating with count (PDP-03, PDP-12)
3. Gallery of real photos (PDP-14)
4. Buy box: price as HTML text, currency, variants, stock status, add to cart (PDP-15, PDP-17, PDP-18)
5. Reassurance facts (PDP-16)
6. Benefit bullets (PDP-07)
7. Description (PDP-06)
8. Spec table (PDP-08)
9. Comparison table (PDP-09)
10. Reviews list (PDP-13), video when it exists (PDP-23)
11. FAQ (PDP-10)
12. Definitions (PDP-11)
13. Cross-links (PDP-21)
14. Footer with real social profiles (C-20)

Everything a buyer needs to decide sits in blocks 1-6 above the fold; everything Google and AI assistants need to understand and quote sits in blocks 7-12 below it. Neither audience is sacrificed to the other.

### 4.3 Copy rules

**Description (PDP-06).** Write at least 150-200 words that exist nowhere else on the web. The manufacturer datasheet is republished by every retailer carrying the product: Google clusters those duplicates and surfaces one version, so a duplicated description leaves the page competing on domain authority alone, and AI assistants skip pages that add nothing beyond what they already cite. Structure it for a buying decision:

1. Two or three benefit-led paragraphs: who the product is for, the top 3 outcomes, with concrete proof (numbers, materials, certifications).
2. Characteristics translated into use: "750 ml titanium pot" becomes "boils water for two people in under four minutes".
3. Specs, compatibility, materials, care as a bulleted list or table.

150-200 words is a floor, not a target to pad toward: filler written for word count works against the page under Google's helpful content signals. Guideline risk: when generating descriptions for hundreds of SKUs with an LLM, add a human review pass per page; publishing unreviewed generated text at scale matches Google's scaled content abuse spam policy.

**Bold, placement, density (C-09 to C-11).** Product name bold once in the first paragraph, one bold phrase every 100-150 words on a fact or benefit, product name and category term in 60%+ of the placement zones, no term above 2.5%.

**Claims (C-24).** Every superlative carries its source or goes. Regulated products carry their legal notices. Competitor specs in the comparison table come from the competitor's own published pages; invented specs are a liability.

**Punctuation, non-negotiable (C-25).** Never leave an em dash (U+2014) or an en dash (U+2013) in copy that goes live on a client site. Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. The em dash is the single most recognizable tell of AI-written text, and one is enough for a shopper, or the client, to file the page as machine output. The rule covers every field you deliver: description, FAQ answers, definitions block, title tag, H1, meta description, alt text, comparison table cells, schema strings. Sweep the finished draft for both characters before handing it over. Hyphens in compound words and ranges written with "to" are untouched.

### 4.4 FAQ and definitions blocks (PDP-10, PDP-11)

Add both below the main description (field pattern observed on premium e-commerce brands that lead their niches, from 115+ agency audits):

| Block | Spec | Purpose |
|---|---|---|
| FAQ | 3+ questions, H3 per question, 40-80 word answers | AI extraction material, long-tail queries, objection handling |
| Definitions | About 5 technical terms from the product, 1-3 sentences each | Same, plus it qualifies non-expert buyers |

Source the questions from pre-sales emails, support tickets, Google's People Also Ask and review content. Each question targets a long-tail query too small to deserve its own page ("does X fit Y", "is X machine washable") and removes a purchase objection right where the decision happens. Write the first sentence of each answer as a standalone fact; the geo-visibility skill covers passage formatting in depth.

Guideline note: do not add FAQPage markup expecting rich results. Google restricted FAQ rich results to government and health sites in August 2023 and retired them for all sites on May 7, 2026. The value is the on-page content itself; the markup is harmless but earns nothing.

### 4.5 Images (PDP-14)

Use real photographs of the actual product: multiple angles, one scale or in-use shot. Avoid AI-generated product images on a PDP, even photorealistic ones: buyers detect synthetic imagery at the exact moment they decide to pay (field rule from 115+ agency audits). Compliance note for accuracy: Merchant Center explicitly permits AI-generated images as long as they accurately represent the product and keep the IPTC DigitalSourceType metadata intact (stripping it can trigger disapproval), and Google ships its own generator (Product Studio). The recommendation against them here is a trust and conversion call, not a Google policy requirement.

Copycat and dropshipping case: photos taken straight from the supplier or manufacturer, the ones every other reseller of the same item also uses, are the duplicate-image equivalent of the duplicate description. Merchant Center expects images that represent your own listing rather than reused stock, so identical supplier photos get the listing disapproved, and a page carrying the same images as fifty competitors gives Google and AI assistants nothing to distinguish it. Shoot the product yourself: own photos are the only fix (field heuristic from 115+ agency audits).

Alt text: product name plus the distinguishing attribute shown. Image weight, format and loading: C-15 and the seo-technical skill.

### 4.6 Rating and reviews (PDP-12, PDP-13)

Place the star rating and review count next to the product title, above the fold, with the platform and the date read when the rating comes from a third party. The full review list can live lower on the page. Why: reviews are the strongest objection killer, and a rating buried at the bottom is never seen by the 80 percent of visitors who do not scroll that far (field heuristic from 115+ agency audits).

The review format that converts (field heuristic): first name + buyer situation + the problem they had + the result. "Marie, runs a food truck: needed a stove that survives daily transport, two years in it still lights first try." Video reviews outperform written ones where available (field observation from the same audits).

Never fabricate, seed, or incentivize undisclosed reviews: this violates Google spam policies and consumer protection law in most markets. AggregateRating and Review markup must match the reviews actually displayed (4.9).

### 4.7 Reassurance facts near the buy button (PDP-16)

Place payment security, delivery time and cost, and the returns window within sight of the add-to-cart button. These answer the three objections active at the decision point. Render them as HTML text, not only icons baked into images: AI assistants extract shipping and returns facts when comparing offers, and the OpenAI product feed has dedicated fields for them (4.10).

### 4.8 Metadata (PDP-02 to PDP-05)

| Field | Pattern | Notes |
|---|---|---|
| Title | {Product name} - {Category} \| {Brand} | About 60 characters; include the attribute buyers search (material, size, color) |
| H1 | {Product name} | Exactly one H1 on the page |
| Slug | /products/{primary-keyword} | Descriptive words with hyphens; never SKU codes or internal IDs |
| Meta description | Benefit + differentiator + one offer fact (shipping or returns) | About 150-160 characters, handwritten |

Why handwritten meta descriptions: auto-generated ones repeat the first sentence of the page; a written one adds the offer facts that win the click. Google rewrites titles and snippets when it judges them poor, which is one more reason to write them deliberately.

Why descriptive slugs: in an Ahrefs analysis of pages cited by ChatGPT, 89.78 percent of cited pages had descriptive slugs versus 81.11 percent in the comparison set (measured, correlational).

### 4.9 Schema (PDP-19, C-18, C-19)

Minimum viable markup for a PDP:

| Type | Required properties |
|---|---|
| Product | name, image, description, sku, brand |
| Offer (nested) | price, priceCurrency, availability, url |
| AggregateRating | Only when visible reviews exist on the page: ratingValue and reviewCount as displayed |
| Review | Only for reviews actually displayed |
| BreadcrumbList | The visible breadcrumb trail, item for item |

Guideline risk to flag every time: structured data must mirror the visible page content. Markup that contradicts the page (a rating with no reviews shown, a price that differs from the displayed one) can trigger a structured data manual action. Never ship an empty node: an AggregateRating with no value, an Offer with no price or a Review with no author is removed, not left blank (`schema_fields`). Validate with the Rich Results Test. JSON-LD template (Product section), merchant listing fields (shipping, returns) and validation workflow: seo-schema-markup, `references/jsonld-templates.md`.

### 4.10 ChatGPT Shopping product feed (PDP-22)

OpenAI publishes a product feed specification for ChatGPT Shopping and agentic checkout. As of this writing the spec documents UTF-8 TSV, CSV or TXT files (gzip accepted) delivered by SFTP, with fields covering price, availability, reviews, Q&A and video; formats and delivery options evolve, so read the live spec before building. Merchants enroll at chatgpt.com/merchants. For an e-commerce site, submitting and maintaining this feed is the first GEO action to take: it replaces crawling guesswork with declared, refreshed data. No API key is needed to follow this skill; enrollment is the merchant's own action. The page is the source of truth and the feed is its export: field mapping in `references/product-page-blueprint.md`.

### 4.11 Acceptance test

Re-run the Phase 2 commands on the staged or live page, and `page_benchmark.py` with the same competitors. The page is done when:

- No high or critical finding in `seo_audit.py`; no `schema_none`, `jsonld_invalid` or `schema_fields`; no `social_placeholder`; no `em_dashes`.
- BOLD above zero with the product name among the samples; PLACEMENT at 60% or more; no `keyword_stuffing`.
- `section_audit.py --type product` finds breadcrumb, rating_summary, price_in_text, spec_table, faq, reviews, trust_badges, and comparison_table and definitions when they are in scope.
- `curl` shows the description, price, rating and reviews in the raw HTML.
- Every block that half or more of the competitors have is present, and the word count is at or above the competitor median.
- The Rich Results Test passes and every markup value matches the page; the feed entry matches the page.

Any remaining Fail is fixed or recorded as a written owner decision.

## Intent split: one query family per page type (PDP-01)

| Query type | Example | Page that ranks |
|---|---|---|
| Transactional | "titanium camping stove", "buy ti stove 2" | Product page |
| Comparative or informational | "best camping stove for two", "titanium vs steel stove" | Blog post or guide that links to the PDP |

Check the live results page before assigning a query: if it shows guides and listicles, a PDP will not break in. Build the supporting article with the seo-content-blog skill and link it to the PDP. Mapping method: seo-keyword-research skill.

## Out of stock, discontinued, variants (PDP-17, PDP-18)

| Scenario | Action | Why |
|---|---|---|
| Temporarily out of stock | Keep HTTP 200 and indexable, set Offer availability to OutOfStock, show a restock estimate, list alternatives, offer a back-in-stock email | The URL keeps its rankings and captures demand while supply returns |
| Discontinued, close substitute exists | 301 to the substitute, or keep the page live with a clear notice plus links to alternatives | Preserves accumulated link equity and rankings |
| Discontinued, no substitute | Keep 200 with alternatives for a transition period, then 301 to the parent collection | Avoids dropping users and crawlers on a dead end |
| Zero traffic, zero backlinks, dead product | 410 or 404 acceptable | Nothing to preserve |

Never return a 404 on a product URL that has rankings, traffic or backlinks: you discard signals that took years to accumulate, and recovery after reinstating the page takes months (field observation from 115+ agency audits).

Variants: give color and size variants one canonical parent unless a specific variant has its own search demand, in which case it earns an indexable URL with unique content (Google product variants guidance).

## Traffic before conversion micro-optimization

Below about 100 organic visitors per day, spend optimization time on traffic volume, not conversion tweaks (field heuristic from 115+ agency audits). The math: typical e-commerce stores convert in the 2-4 percent range (field observation consistent with public benchmarks), so 30 visitors a day produce about one order a day. No A/B test reaches significance at that volume, and a conversion lift on near-zero traffic is near-zero revenue.

What still pays at low traffic: one-off hygiene from this skill (rating at the top, reassurance facts, real photos, the description rewrite), because these are builds, not tests. Then shift effort to more indexable pages (PDPs, collections, blog) and internal links. In the deliverable, this rule sets the priority order of the next actions.

## Marketplace listings: Amazon and FBA

Amazon is a search engine and a separate market with its own ranking, not a copy of Google. The same on-page audit transposes to an Amazon listing: study the keywords and descriptions the competing listings rank for on Amazon itself, then optimize the listing title, bullets and product description as you would a web PDP, around the terms buyers type on that marketplace (field heuristic from 115+ agency audits). Keep the channel distinct: an Amazon listing and the store's own PDP serve different surfaces and rarely compete with each other. The reusable parts of this skill are the unique benefit-led copy, the buyer-question coverage and the real-photos rule (PDP-06, PDP-10, PDP-14); the platform-specific mechanics (A9 ranking, FBA fulfillment) live outside the scope here. Marketplace listings of the same product are also Phase 3 competitors for the store's own PDP.

## GEO layer

**AI assistants recommend product pages directly.** This is the structural difference from classic SEO, where blog content captured most organic entry points. Assistant answers to "best X for Y" and "where can I buy X" now link PDPs directly: one 2025 analysis of AI citations in commerce contexts measured product pages at about 13.7 percent of citations, with listicle-format content taking the largest share (single-source study, not independently replicated: ALM Corp). Two consequences: the PDP is now a citation target in its own right, and it must stand alone, because the assistant quotes one page, not your whole site.

**Make the PDP self-sufficient (PDP-20).** An assistant can only recommend what the page states: full spec table in HTML, price and currency as HTML text, shipping cost, delivery time and returns window in text, FAQ and definitions blocks, the comparison versus alternatives, review count, average rating and 2-3 quoted reviews in HTML. If a fact is missing from the page, the assistant either omits the product or fills the gap from a competitor's page.

**Keep every fact in server-rendered HTML (PDP-15, C-21).** Major AI crawlers fetch pages but do not execute JavaScript (measured by Vercel across GPTBot, ClaudeBot and others). A PDP whose price, description or reviews are injected client-side is partially or fully invisible to assistants. Test with curl; fixes (SSR, prerendering) belong to the seo-technical skill.

**Add a comparison table (PDP-09).** A short "this product versus the two closest alternatives" table (rows: price, key specs, ideal use case) is exactly the passage format assistants lift for "best X" answers, and it keeps the comparison happening on your page instead of a third-party listicle. Stay factually accurate about competitor products. Passage construction details: geo-visibility skill.

**Submit the product feed (PDP-22)**, see 4.10.

**Measure.** Track assistant citations, share of voice and AI referral traffic with the geo-tracking skill. Re-run the acceptance test after each significant page change.

## Deliverable

Deliver every product page job in exactly this structure:

```markdown
# Product page: {product name}
URL: {url or "new page"} | Target query: {query} (intent: transactional) | Date: {date}

## 1. Spec scorecard
| ID | Requirement | Status (Pass / Fail / Not verifiable) | Evidence | Priority |
|---|---|---|---|---|
| PDP-01 ... PDP-24 | (every PDP row) | | (script code, block, or manual check) | P1 / P2 |
| C-01 ... C-26 | (every common row that fails or cannot be verified) | | | |
Default P1: PDP-01 to PDP-06, PDP-10, PDP-12, PDP-14, PDP-15, PDP-19, PDP-20. Default P2: the rest.

## 2. Audit findings
(seo_audit.py SEO and GEO scores with high or medium findings; section_audit.py blocks found and missing;
raw HTML check: price, description, reviews present or not; or "new page")

## 3. Competitor benchmark
(the competitors and why each was picked: same product elsewhere, marketplace, ranking brand, AI-cited;
page_benchmark.py table; blocks and schema types the client lacks; metrics below the median;
the information gain chosen)

## 4. Build
- Metadata: title ({n} chars), meta description ({n} chars), slug, H1
- Rewritten description ({n} words): benefits first, then specs in use, bold visible
- Benefit bullets, spec table
- Comparison block: this product, alternative A, alternative B (sourced)
- FAQ block (3-5 questions, 40-80 word answers), definitions block (about 5 terms)
- Rating line and review display, reassurance facts
- JSON-LD: Product + Offer (+ AggregateRating only when real) + BreadcrumbList; hand implementation to seo-schema-markup
- GEO checklist: raw HTML visibility, self-sufficiency gaps, feed status
- Internal links: parent collection, sister products, supporting guide
(placeholders {to confirm} for every unverified fact)

## 5. Acceptance
(scripts re-run: remaining findings, each fixed or a written owner decision)
| # | Next action | Why | Priority |
(ordered by the traffic-before-conversion rule when organic traffic is under about 100 visitors a day)
```

## Common mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| Pasting the manufacturer description | Duplicated across every retailer; the page competes on domain strength alone | Rewrite unique, benefits first (PDP-06) |
| Supplier or AI-generated product images | Duplicate images risk disapproval; synthetic ones break trust at payment (AI images allowed by Merchant Center only with IPTC metadata intact) | Own real photos, multiple angles (PDP-14) |
| Schema price or rating differing from the page, or empty nodes | Structured data manual action risk | Markup mirrors visible content, no empty node (PDP-19) |
| AggregateRating with no reviews displayed | Same manual action risk | Mark up ratings only when real reviews are shown |
| 404 on a discontinued product with history | Discards years of signals and backlinks | Keep 200 with alternatives, or 301 to substitute (PDP-17) |
| Targeting informational queries with a PDP | Intent mismatch; the page type cannot rank there | Blog post that links to the PDP (PDP-01) |
| Reviews hidden in a JS-loaded tab at the bottom | Invisible to crawlers and to most visitors | Dated rating with count at the top, reviews in server HTML (PDP-12, PDP-13) |
| Price rendered by JavaScript or inside an image | Assistants cannot quote the offer | Price as HTML text (PDP-15) |
| "Best stove on the market" with no source | Discounted by buyers and quality raters; flagged as superlative_claim | Source it or remove it (C-24) |
| Comparison table with invented competitor specs | Legal and credibility liability | Specs from the competitor's own pages, dated (PDP-09) |
| Footer icons pointing to network homepages | Broken entity links | Real profile URLs, same as `sameAs` (C-20) |
| A/B testing at 30 visitors a day | No statistical power; near-zero revenue upside | Build traffic volume first |
| Mass-generating descriptions with no review pass | Scaled content abuse policy exposure | Human review per page |
| Adding FAQPage markup for rich results | FAQ rich results restricted in 2023, fully retired May 2026 | Keep the FAQ content; treat markup as optional |

## Sources

- https://almcorp.com/blog/ai-citations-listicles-articles-product-pages/ (product pages at about 13.7 percent of AI citations)
- https://developers.openai.com/commerce/specs/file-upload/products (ChatGPT Shopping feed specification)
- https://chatgpt.com/merchants (merchant enrollment)
- https://ahrefs.com/blog/why-chatgpt-cites-pages/ (descriptive slugs, 89.78 vs 81.11 percent citation correlation)
- https://vercel.com/blog/the-rise-of-the-ai-crawler (AI crawlers do not execute JavaScript, measured)
- https://developers.google.com/search/docs/appearance/structured-data/product (Product markup reference)
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies (markup must reflect visible content, manual actions)
- https://developers.google.com/search/docs/essentials/spam-policies (scaled content abuse, fake reviews)
- https://developers.google.com/search/blog/2023/08/howto-faq-changes (FAQ rich results removal)
- https://support.google.com/merchants/answer/6324350 (Merchant Center image requirements)
- https://developers.google.com/search/docs/appearance/structured-data/product-variants (variant URL handling)
- https://developers.google.com/search/docs/appearance/title-link (title rewriting behavior)
- skills/seo-geo-audit/references/common-page-spec.md (common rows C-01 to C-26) and audit-checklist.md section 15 (finding codes)

All thresholds labeled "field heuristic from 115+ agency audits" come from recurring patterns in real audit work, not from controlled studies. Treat them as strong defaults to adapt, not as guarantees.
