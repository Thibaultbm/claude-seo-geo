---
name: seo-content-collection-page
description: "Spec, audit, competitor benchmark and build for e-commerce collection, category and product listing pages (PLPs) on Shopify, WooCommerce, Magento, BigCommerce, PrestaShop or a custom store. Runs four phases: the collection spec (COL-01 to COL-24 plus the common rows), an audit of the live page with the bundled scripts, a benchmark against the stores and marketplaces ranking on the category term, and the build: Search Console demand mining, a 1-2 sentence top intro, a 400-800 word bottom block (buying guide, comparison table, definitions, FAQ of real questions), product cards with images, metadata, faceted-navigation and filter URL control, self-canonical pagination, thin or empty collection cleanup, internal links, CollectionPage, ItemList and BreadcrumbList JSON-LD, then the scripts re-run as the acceptance test. Use to create, write or audit a category page or PLP, or to handle filtered URLs, pagination, duplicate or empty categories and store crawl budget."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "2.0.0"
---

# Collection Page SEO and GEO

Collection and category pages (PLPs) win the category-level money queries, yet most stores ship them as a bare product grid with no editorial content (field observation from 115+ agency audits). They fail in three ways: no text to rank or quote, filter and pagination URLs that drown the crawl, and empty or duplicate collections that drag sitewide quality. This skill runs the four phases of the page standard (spec, audit, benchmark, build) with placement, faceting and pagination rules that protect both rankings and conversion.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use

- Creating or rewriting a collection, category, shop or product archive page
- Asking where category text should go, how long it should be, or what it should contain
- Filter or parameter URLs flooding Google Search Console ("Discovered, currently not indexed", crawl spikes)
- Configuring pagination, canonicals or indexing rules for listing pages
- Cleaning up empty, thin or duplicate collections
- Wanting category pages cited in AI answers such as "best X" or "where to buy Y"
- Any storefront: Shopify, WooCommerce, Magento, BigCommerce, PrestaShop or custom

| Case | Skill |
|---|---|
| Individual product pages (PDPs) | seo-content-product-page |
| Sitewide link architecture and anchors | seo-internal-linking |
| JSON-LD implementation details | seo-schema-markup |
| Rendering, robots.txt, crawl budget mechanics | seo-technical |
| Validating search demand for a facet | seo-keyword-research |
| Supporting buying guides on the blog | seo-content-blog |
| Block-by-block gaps on other page types | seo-page-sections |
| Whole-site audit | seo-geo-audit |
| Passage-level citability writing | geo-visibility |
| Measuring AI citations and referrals | geo-tracking |

## Phase 1. The spec

Common requirements C-01 to C-26: skills/seo-geo-audit/references/common-page-spec.md. Every collection page must pass them too; the rows below only add or sharpen what is specific to a listing page. Evidence labels: "measured" (with source), "Google documentation", "standard practice", or "field heuristic from 115+ agency audits".

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| COL-01 | Target query is the category keyword, with commercial intent confirmed | Listing or category pages rank in the top 10 for it | manual (SERP check) | A collection cannot win a query whose SERP rewards guides or PDPs (standard practice) |
| COL-02 | Secondary keywords come from the page's own Search Console demand | 90-180 day query export for the exact URL, three buckets placed (section 4.1) | manual (GSC) | The searchers' exact words are the proven match for intent; guessing misses them |
| COL-03 | H1 names the category as buyers name it (sharpens C-03) | "Linen Dresses", never "Our Collection" | h1_missing, h1_multiple, manual | The head term of the page (standard practice) |
| COL-04 | Title {Category} \| {Brand} or {Category} - {Qualifier} \| {Brand} (sharpens C-01) | about 60 characters, unique across all collections | title_short, title_long, manual uniqueness check | Templates mint near-identical titles and Google rewrites them unpredictably (Google documentation) |
| COL-05 | Slug /collections/{category-keyword}, mirroring the motif the leaders use (sharpens C-23) | descriptive words, hyphens, no internal IDs | url_hygiene, manual | 89.78% of ChatGPT-cited pages had descriptive slugs vs 81.11% (measured, Ahrefs, correlational) |
| COL-06 | Meta description: what the range covers + one differentiator + one offer fact (sharpens C-02) | about 150-160 characters, handwritten | meta_missing, meta_short, meta_long | The snippet sells the click (field heuristic from 115+ agency audits) |
| COL-07 | Top intro under the H1, opening with the category keyword as its first word, bolded | 1-2 sentences maximum | kw_not_in_intro, kw_not_bold, manual | More text on top pushes products below the fold and costs sales (field heuristic from 115+ agency audits) |
| COL-08 | Bottom SEO block below the product grid, in the served HTML | 400-800 words; accordion allowed, hidden from users never | thin_content, page_benchmark.py "words", manual position | Feeds Google and AI assistants at no conversion cost (field heuristic from 115+ agency audits; cloaking boundary per Google spam policies) |
| COL-09 | Buying-guide headings phrased as real questions | 3+ H2/H3 (how to choose, which type for which use, sizing, materials, care) | no_question_h2, page_benchmark.py "question_h" | Matches what people and assistants ask (applies C-13) |
| COL-10 | Comparison table of the category's sub-types, as a real HTML table | rows: use case, price range, strengths | section_audit comparison_table, any_table; no_table | The passage format AI answers quote for "best X" (field heuristic from 115+ agency audits) |
| COL-11 | Definitions of category terms in plain language | 3-5 terms | section_audit definitions | Qualifies non-expert buyers, long-tail coverage |
| COL-12 | FAQ of real buyer questions (search suggestions, People Also Ask, support tickets, GSC), first sentence a standalone fact | 3+ questions, 40-80 word answers | section_audit faq, manual | Extraction material and objection handling (field heuristic from 115+ agency audits) |
| COL-13 | Keyword placement, bolding and density applied to the two text zones (applies C-09, C-10, C-11) | category keyword + the most important secondary keywords bolded; placement coverage 60%+; no term above 2.5% | no_bold, kw_not_bold, kw_placement_low, keyword_stuffing | Product names repeated in the grid inflate density: judge the copy, not the cards |
| COL-14 | Product cards with real images (alt text), name, price as HTML text, link to the PDP | every card on page 1 | section_audit images, price_in_text; alt_missing; manual | The reason the page exists; images and prices are what shoppers and assistants read (applies C-15) |
| COL-15 | H1, intro, first page of product links and the bottom block present in the raw server HTML | all four, without JavaScript | likely_js_rendered, curl | Major AI crawlers do not execute JavaScript (measured, Vercel; applies C-21) |
| COL-16 | One block per collection, written for it | 0 boilerplate paragraphs rotated across collections | manual (compare 2-3 sister collections) | Templated filler gives nothing to rank or quote |
| COL-17 | Filter, sort and parameter URLs controlled, mechanism chosen by goal (section 4.7) | canonical to the clean URL by default; never robots.txt Disallow and noindex on the same URL at the same time; sort, view, session parameters out of the crawl | manual (curl on filter URLs, GSC page indexing, logs); canonical_other is the expected result on a filter URL | Faceted navigation is the canonical crawl-waste scenario (Google documentation) |
| COL-18 | An indexable facet passes all three tests | real demand + distinct inventory + unique title, H1, intro; self-canonical; created one by one | manual + seo-keyword-research | Mass facet pages match Google's doorway definition (Google documentation) |
| COL-19 | Pagination: page 2+ self-canonical, indexable, unique title, plain links | never canonical to page 1; title {Category} - Page {N} \| {Brand}; `<a href>` links; infinite scroll with paginated fallback | seo_audit.py on ?page=2 (canonical_other = Fail), manual | Canonical to page 1 orphans deep products (Google documentation) |
| COL-20 | No indexable empty or thin collections | 0-2 products: merge or noindex; seasonal URLs kept and reused | manual (product count per collection) | Dead listings dilute sitewide quality and crawl budget (field heuristic from 115+ agency audits) |
| COL-21 | Collection linked as a money page (applies C-16, C-19) | one click from the home menu; sister-collection block; top products and blog guides link back with the category keyword as anchor; breadcrumbs on PDPs and sub-collections | section_audit breadcrumb, internal_links; generic_anchor; manual | Collections, not PDPs, win category-level queries (field observation from 115+ agency audits) |
| COL-22 | CollectionPage + ItemList + BreadcrumbList, no empty nodes (sharpens C-18) | ItemList URLs match the rendered page 1; no Product + Offer on every grid item; no empty `name` or `itemListElement` | schema_none, jsonld_invalid, schema_fields, page_benchmark.py "schema", manual | Product markup targets single-product pages; markup must mirror the page (Google documentation) |
| COL-23 | Claims are honest (sharpens C-24) | "best", "n°1", "cheapest" sourced or removed; table facts true of the live catalog; promotions and urgency real | superlative_claim, manual | Unbacked claims are discounted by shoppers, raters and models |
| COL-24 | Stable URL | no slug rename; if unavoidable, 301 + internal links updated the same day | manual | Renames discard the links, rankings and AI citations the old URL earned (field practice from 115+ agency audits) |

## Phase 2. Audit the existing page

Fetch the raw server HTML and audit the clean URL, page 2 and one filter URL in one run:

```
curl -sL -A "Mozilla/5.0" https://store.com/collections/linen-dresses | grep -c 'href="/products/'
python3 skills/seo-geo-audit/scripts/seo_audit.py https://store.com/collections/linen-dresses "/collections/linen-dresses?page=2" "/collections/linen-dresses?filter.v.option.color=red"
python3 skills/seo-page-sections/scripts/section_audit.py --type collection https://store.com/collections/linen-dresses
```

A grid or text block that only appears after JavaScript runs is invisible to AI assistants and unreliable for Google (COL-15). Then map the URL surface: list the filter, sort and pagination parameters the template emits, and read the Search Console page indexing reports for parameter URL inflation (COL-17). Count products per collection for COL-20.

Map the findings to spec rows. Every row ends Pass, Fail or Not verifiable (with the reason):

| Evidence | Spec rows |
|---|---|
| title_*, meta_*, h1_*, url_hygiene | COL-03 to COL-06, C-01 to C-03, C-23 |
| kw_not_in_intro, kw_not_bold, no_bold, kw_placement_low, keyword_stuffing | COL-07, COL-13, C-09 to C-11 |
| thin_content, word count, no_question_h2, no_table | COL-08 to COL-10, C-08, C-13 |
| section_audit faq, definitions, comparison_table, images, price_in_text | COL-10 to COL-12, COL-14 |
| likely_js_rendered, curl product-link count | COL-15, C-21 |
| canonical on the filter URL (should point to the clean URL) | COL-17 |
| canonical_other on ?page=2 | COL-19 Fail |
| schema_none, jsonld_invalid, schema_fields, breadcrumb | COL-22, C-18, C-19 |
| superlative_claim, claim_no_disclaimer | COL-23, C-24 |
| em_dashes | C-25 |

The scripts cannot judge COL-01, COL-02, COL-16, COL-18, COL-20 or the grid-versus-text position in COL-08: those stay manual. When no page exists yet, skip this phase and let Phase 3 set the bar.

## Phase 3. Benchmark the competitors

Pick the pages that already win the category term:

1. Search the category keyword (and the top GSC variant) in the target market, logged out, in the store's language.
2. From the top 10, take 3-5 category URLs (never their homepages): the specialist stores and retailers ranking on the term first, then one marketplace or large retailer category page if it ranks. Same-model stores are the most useful block benchmark; marketplaces often rank on domain strength alone.
3. Ask ChatGPT, Perplexity and Google AI Mode "best {category}" and "where to buy {category}"; add any cited category page to the set.
4. Note editorial listicles in the top 10 but do not benchmark them as stores: their presence means the SERP is mixed and the buying-guide block (COL-09 to COL-12) carries more weight.

```
python3 skills/seo-geo-audit/scripts/page_benchmark.py --type collection https://store.com/collections/linen-dresses https://rival1.com/category/linen-dresses https://rival2.com/c/linen-dresses https://marketplace.com/linen-dresses
```

What to read in the output:

| Output | Use |
|---|---|
| BLOCKS half or more of the competitors have | Each missing block becomes a build item (faq, comparison_table, definitions, breadcrumb, images, price_in_text) |
| SCHEMA TYPES competitors use | ItemList, BreadcrumbList, CollectionPage gaps feed COL-22 |
| CLIENT BELOW THE COMPETITOR MEDIAN | words, bold, question_h, tables, placement, money_links: the C and COL rows behind them move up in priority |
| Table row by row | The bar for COL-08: 400-800 words is the default; if the median is higher, close the gap with more buying questions answered, never with padding |

Read by hand what the script cannot: the slug motif the leaders share (COL-05), the facets they expose as indexable landing pages (a demand signal for COL-18, to validate), their sub-collection links, and how many products their grids show.

Information gain: write in 1-2 sentences what the client page will offer that none of the benchmarked pages has. Typical sources on a collection: a comparison table built from the client's own catalog criteria, sizing or fit data from returns, care answers from support tickets, original figures ({to confirm}: best-seller share, return rate by material), or a buying question from GSC no competitor answers.

## Phase 4. Build

### 4.1 Mine Search Console first (COL-02)

Pull the collection URL's own performance from Google Search Console (Sorank GSC connector, or the GSC API): filter to the exact URL, dimension = query, 90-180 day window, sorted by impressions. Capture the whole cluster of related terms, not just the head term, and reuse the searchers' phrasing.

| Bucket | Signal | What to do |
|---|---|---|
| High impressions, low or zero clicks | The page is shown but the snippet does not earn the click, or the term is absent from the copy | Name the term explicitly, in the searcher's exact wording, in the H1-adjacent intro and a body passage |
| Real impressions, position 8-30 | One page off the clickable zone | Add a focused passage on the term so a single rank gain converts to traffic |
| Ranks for a term absent from title, H1 and body | A pure content gap | Close it verbatim: the demand already exists, the page just never says the words |

This pass supplies the secondary-keyword list for the bottom block. The seo-keyword-research skill stays the tool for validating brand-new facet pages with no Search Console history.

### 4.2 Wireframe

1. Breadcrumb (visible + BreadcrumbList)
2. H1: the category keyword (COL-03)
3. Top intro, 1-2 sentences (COL-07)
4. Sub-collection links or chips
5. Filters and sort (crawl-controlled, 4.7)
6. Product grid: cards with image and alt, name, price as text, link to the PDP (COL-14)
7. Pagination with plain `<a href>` links (4.8)
8. Bottom SEO block, 400-800 words (4.3, 4.4)
9. Related collections block, then footer

### 4.3 Text placement: almost everything goes at the bottom (COL-07, COL-08)

Why the bottom: a text block at the top pushes the products below the fold, and visitors who came to browse bounce before seeing a single item, so the block costs sales. Placed at the bottom, the same text feeds Google and AI assistants without costing a conversion. Why it still counts for rankings: position on the page does not disqualify content; it is in the HTML, it is indexed and weighted. Collapsible or accordion presentation is fine as long as the text is present in the served HTML and accessible to users; serving the block to bots while hiding it from users entirely is cloaking territory (https://developers.google.com/search/docs/essentials/spam-policies).

Why 400-800 words: enough to cover the buying questions of the category and give assistants quotable passages, short enough to stay specific. Padding past what the category deserves invites helpful content demotions, not gains.

### 4.4 Bottom block structure (COL-09 to COL-12)

Build the block from these components, in this order:

| Component | Spec | Purpose |
|---|---|---|
| Buying guide headings | H2/H3 phrased as real questions: how to choose, which type for which use, sizing, materials, care | Matches the queries people and assistants actually ask |
| Comparison table | Sub-types of the category compared (rows: use case, price range, strengths) | The passage format AI answers quote for "best X" |
| Definitions | 3-5 category terms in plain language | Qualifies non-expert buyers, long-tail coverage |
| FAQ | 3 questions minimum, 40-80 word answers | Extraction material, objection handling |
| Links | Sub-collections, sister collections, 2-3 related blog guides | Distributes authority, deepens the topic cluster |

Write answers so the first sentence stands alone as a fact (passage construction details: geo-visibility skill). Source questions from search suggestions, People Also Ask, support tickets, GSC and the seo-keyword-research skill output.

### 4.5 Copy rules

| Rule | Detail | Spec |
|---|---|---|
| First word | Open the intro with the primary keyword as the very first word, never a dash or filler | COL-07 |
| Semantic bolding | Primary keyword bolded in the intro; the most important secondary keywords and key facts bolded in the block, one bold phrase every 100-150 words, never whole sentences | COL-13, C-09 |
| Placement | Category keyword in title, H1, an H2, meta, URL, first 100 words, bold, one image alt: 60%+ coverage | COL-13, C-10 |
| Density | No term above 2.5% of content words, brand and product names aside | COL-13, C-11 |
| Concrete criteria | Price ranges, materials, use cases, dimensions, not adjectives | COL-10, C-14 |
| Unique per collection | Every collection gets its own block; a boilerplate paragraph rotated across 50 collections adds nothing and reads as templated filler | COL-16 |
| Honest claims | No unsourced "best" or "n°1", no fake urgency, every table cell true of the live catalog | COL-23, C-24 |
| Unknown facts | `{to confirm}`, never invented | house rule |

Punctuation, non-negotiable (C-25): never leave an em dash (U+2014) or an en dash (U+2013) in copy that goes live on a client site. Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. The em dash is the single most recognizable tell of AI-written text, and one is enough for a shopper, or the client, to file the page as machine output. The rule covers every field: top intro, bottom block, FAQ answers, title tag, H1, meta description, alt text, facet labels, schema strings. Sweep the finished draft for both characters before handing it over. Hyphens in compound words and ranges written with "to" are untouched.

### 4.6 Metadata (COL-03 to COL-06)

| Field | Pattern | Notes |
|---|---|---|
| H1 | {Category keyword} | "Linen Dresses", not "Our Collection" |
| Title | {Category} \| {Brand} or {Category} - {Qualifier} \| {Brand} | Unique per collection, about 60 characters |
| Slug | /collections/{category-keyword} | Descriptive words, hyphens, no internal IDs |
| Meta description | What the range covers + one differentiator + one offer fact | About 150-160 characters, handwritten |

Why unique titles matter here specifically: collection templates generate titles mechanically, so stores routinely ship dozens of near-identical titles, and Google then rewrites them unpredictably (https://developers.google.com/search/docs/appearance/title-link). Why descriptive slugs: in an Ahrefs analysis of pages cited by ChatGPT, 89.78 percent of cited pages had descriptive slugs versus 81.11 percent in the comparison set (measured, correlational: https://ahrefs.com/blog/why-chatgpt-cites-pages/). /collections/linen-dresses earns citations that /collections/c-118 does not.

Competitive nuance on the slug: look at the URL segment the leaders already ranking for the query use (Phase 3), and match that pattern rather than inventing your own. If the pages winning "photovoltaic label" all sit on a slug like /etiquette-photovoltaique, mirror that exact wording; Google has confirmed the term matches buyer intent on that query, so reusing the proven motif is safer than a synonym (field heuristic from 115+ agency audits).

### 4.7 Faceted navigation: control the URL explosion (COL-17, COL-18)

Faceted navigation is the largest crawl trap in e-commerce: 200 collections times a handful of filters, values and sort orders generate millions of parameter URLs (?color=red&size=m&sort=price) that are near-duplicates of each other. Google documents this as the canonical crawl waste scenario (https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation). Symptoms: "Discovered, currently not indexed" inflation in Search Console, crawl stats dominated by parameter URLs, fresh products taking weeks to index.

Build steps: list every parameter pattern the template emits, then pick the mechanism per pattern by goal, never stacking them blindly:

| Goal | Mechanism | Caveat |
|---|---|---|
| Consolidate signals from filtered URLs | rel=canonical pointing to the clean collection URL | A hint, not a directive; Google can ignore it when the filtered page differs substantially |
| Stop crawl waste on filter combinations | robots.txt Disallow on parameter patterns | Does not deindex: blocked URLs can stay indexed without content if linked; Google also can no longer see any noindex on them |
| Remove filter URLs already indexed | meta robots noindex (or X-Robots-Tag) | The URL must remain crawlable until it drops out; only block it in robots.txt afterwards, if ever |
| Keep one facet as a landing page | Self-canonical + unique title, H1 and text | Only with proven demand and distinct inventory (below) |

Google's own faceted-navigation doc calls rel=canonical and nofollow "generally less effective in the long term" for facet control and prefers preventing the crawl outright (robots.txt, or URL fragments) when facet URLs are not meant for search. The table above is standard practitioner practice; on large catalogs where crawl budget is the binding constraint, lead with crawl prevention.

The interaction that burns teams: robots.txt blocking and noindex are mutually exclusive on the same URL at the same time, because a blocked page is never fetched, so its noindex is never seen (https://developers.google.com/search/docs/crawling-indexing/robots/intro). Sequence them: noindex first, block later if needed. Search Console's URL Parameters tool was retired in 2022; these on-site mechanisms are all you have (https://developers.google.com/search/blog/2022/03/url-parameters-tool-deprecated).

The exception, an indexable facet (COL-18), must pass all three tests:

1. Real search demand for the facet term ("red dresses" has volume; "red dresses size M under 50" does not). Validate with seo-keyword-research.
2. Distinct inventory: several products meaningfully different from the parent collection's default view.
3. Unique content: its own title, H1, intro, and ideally its own bottom block.

Guideline risk to flag: mass-generating facet landing pages without demand or unique content matches Google's doorway page definition (https://developers.google.com/search/docs/essentials/spam-policies). Create facet pages one by one, by demand, never by template across the whole catalog.

Decision flow, platform parameter patterns (Shopify, WooCommerce, Magento, BigCommerce, PrestaShop), robots.txt examples and the monthly monitoring loop: references/faceted-navigation-playbook.md.

### 4.8 Pagination: self-canonical, never to page 1 (COL-19)

| Item | Rule |
|---|---|
| Canonical on page 2+ | Self-referencing (page 2 canonicals to page 2) |
| Canonical to page 1 | Never |
| Title on page 2+ | {Category} - Page {N} \| {Brand} |
| Pagination controls | Plain `<a href>` links, crawlable; not JS-only buttons |
| Indexability | Keep page 2+ indexable |
| rel=prev/next | Not used by Google for indexing since 2019; harmless to keep, never a fix |

Why "canonical to page 1" is the classic self-inflicted wound: it declares every paginated page a duplicate of page 1, so Google consolidates to page 1 and stops crawling deep pages. Products linked only from page 3+ lose their only crawl path and fall out of the index. Google's own e-commerce pagination documentation prescribes self-referencing canonicals (https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading).

Infinite scroll and "load more" need a paginated URL fallback with real `<a href>` links, because crawlers do not scroll or click. If the catalog is small, a single complete page with no pagination is simpler than any of this.

### 4.9 Empty and thin collections (COL-20)

| Collection state | Action | Why |
|---|---|---|
| 0 products, line discontinued | Merge: 301 to parent or closest sibling | A dead listing page is quality dead weight |
| 0 products, temporary or seasonal | Keep the URL in 200, reuse the same URL every season; noindex during the off-season is optional | The URL accumulates links and rankings year over year ("christmas gifts" should never change slug) |
| 1-2 products | Merge into the parent unless the term has strong demand and inventory will grow | A near-empty grid satisfies nobody and drags perceived site quality |
| 3+ products with demand | Keep and optimize | Enough inventory to satisfy the query |

Why this matters at the site level: dozens of indexable empty collections dilute the quality profile Google evaluates sitewide, and they waste the crawl budget the real collections need (field heuristic from 115+ agency audits).

Mono-product case, the "real catalogue" tactic: a business selling essentially one product has no collection to fill, so the collection page looks empty and barely exists to Google. Split the single product into genuine variants (packaging, color, format, size, quantity bundle) so the collection lists several real, separately purchasable items and reads as a true category rather than a one-item shell (field heuristic from 115+ agency audits). The variants must be honestly distinct purchasable options, not the same item cloned under different URLs, which would be the doorway and near-duplicate problem from 4.7.

### 4.10 Internal links: collections are the money pages (COL-21)

In most audited stores, collections, not PDPs, win the category-level queries that drive revenue (field observation from 115+ agency audits). Link them accordingly:

- Main menu: every revenue collection reachable in one click from the home page
- Sister collections: a "related categories" block on each collection
- Top products: featured products link back to their collection
- Breadcrumbs on every PDP and sub-collection, marked up with BreadcrumbList
- Blog guides: each buying guide links to its collection with the category keyword as anchor

Anchor text: the category keyword, varied naturally. Full architecture and anchor strategy: seo-internal-linking skill.

### 4.11 Schema (COL-22)

| Type | Use |
|---|---|
| CollectionPage | The page type |
| ItemList | The products listed, as URLs to the PDPs, consistent with the rendered first page |
| BreadcrumbList | The category path |

```json
{"@context": "https://schema.org", "@graph": [
  {"@type": "CollectionPage", "@id": "https://store.com/collections/linen-dresses#page",
   "url": "https://store.com/collections/linen-dresses", "name": "Linen Dresses",
   "mainEntity": {"@id": "https://store.com/collections/linen-dresses#list"},
   "breadcrumb": {"@id": "https://store.com/collections/linen-dresses#breadcrumb"}},
  {"@type": "ItemList", "@id": "https://store.com/collections/linen-dresses#list",
   "itemListElement": [
     {"@type": "ListItem", "position": 1, "url": "https://store.com/products/{product-1}"},
     {"@type": "ListItem", "position": 2, "url": "https://store.com/products/{product-2}"}]},
  {"@type": "BreadcrumbList", "@id": "https://store.com/collections/linen-dresses#breadcrumb",
   "itemListElement": [
     {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://store.com/"},
     {"@type": "ListItem", "position": 2, "name": "Linen Dresses", "item": "https://store.com/collections/linen-dresses"}]}
]}
```

Do not attach full Product + Offer markup to every grid item: Google's Product structured data targets pages about a single product, and category pages should use ItemList instead (https://developers.google.com/search/docs/appearance/structured-data/product). Markup must mirror what the page displays: no empty node (an ItemList with no items, a ListItem with no URL, an empty `name`), no FAQPage for questions the page does not show. Implementation patterns and validation: seo-schema-markup skill.

### 4.12 Acceptance test

Re-run Phase 2 on the live or staged URLs (clean, ?page=2, one filter URL), then `page_benchmark.py --type collection` with the same competitors. Done when:

- no high or critical finding remains; BOLD count above zero with the category keyword among the samples; PLACEMENT 60%+; no `keyword_stuffing`
- section_audit finds faq, comparison_table (or any_table), definitions, breadcrumb, images and price_in_text
- schema shows CollectionPage, ItemList and BreadcrumbList with no `schema_fields` finding
- curl shows the H1, the bottom block and the first page of product links in the raw HTML
- page 2 is self-canonical; the filter URL canonicalizes to the clean URL or carries its chosen directive
- no metric on the benchmark sits below the competitor median without a written reason
- the copy holds zero em or en dashes

Any remaining Fail is either fixed or recorded as a written owner decision.

## GEO layer

### Collection pages get cited in "best X" and "where to buy Y" answers (COL-08 to COL-12)

AI assistants favor list-format content: an analysis of AI citations in commerce contexts found listicles taking the largest share of citations, with product pages at about 13.7 percent (single-source study, not independently replicated: https://almcorp.com/blog/ai-citations-listicles-articles-product-pages/). A collection page with a buying-guide block, a comparison table and an FAQ presents the same extractable structure as a listicle, with live inventory attached. A bare product grid offers an assistant nothing to quote; the bottom block is what makes the page citable.

### Write the bottom block as extraction material (COL-10, COL-12)

The comparison table and the FAQ answers are the passages assistants lift. Make each FAQ answer's first sentence a standalone fact, keep the comparison table small and labeled, and state concrete criteria (price ranges, materials, use cases) rather than adjectives. Passage construction in depth: geo-visibility skill.

### Descriptive slugs, stable URLs (COL-05, COL-24)

Beyond the Ahrefs citation correlation (4.6), assistants cite and revisit URLs: renaming a collection slug discards the citations the old URL earned. If a rename is unavoidable, 301 the old URL and update internal links the same day (field practice from 115+ agency audits).

### Server-rendered HTML only (COL-15)

Many storefront themes render the product grid, filters and even the text block client-side. Major AI crawlers fetch but do not execute JavaScript (measured by Vercel across GPTBot, ClaudeBot and others: https://vercel.com/blog/the-rise-of-the-ai-crawler), so a JS-rendered collection page is an empty page to ChatGPT, Claude and Perplexity. Test with curl: the H1, the bottom block and at least the first grid of product links must appear in the raw HTML. Rendering fixes: seo-technical skill.

### Special case: source the text from Google Maps reviews (COL-16, COL-23)

For a directory or listing page that profiles a real venue (a marketplace entry, a local annuaire, a curated collection of places), the venue's own Google Maps reviews are a source of fresh, specific themes. Use them as research, not as text: read the recent reviews and write, in your own words, a short current passage about what customers consistently mention: the atmosphere, the felt experience, in plain factual language attributed as customer feedback rather than presented as your own claims (field heuristic from 115+ agency audits). Licensing caveat: Google Maps Platform terms restrict caching and repurposing Places content (reviews are meant to be displayed as-is, with attribution, via the API), and each review text remains its author's copyright, so never republish or lightly paraphrase the review texts themselves. Done this way, the page gains concrete, up-to-date detail that a templated description lacks, exactly the kind of specific material assistants quote.

### Special case: position 2 on navigational brand queries (COL-23)

On navigational queries shaped "brand + reviews" or "brand + alternative", position 1 is the brand's own official property and is not realistically contestable. The opening is position 2: a comparative or directory page that lists the brand alongside its alternatives, or aggregates independent reviews of it (field heuristic from 115+ agency audits). This is a recurring play for marketplaces and directories: the page does not need to outrank the brand, only to own the second slot that captures the searcher looking for outside opinion. Stay accurate about every brand named; invented comparison facts are a liability.

### Measure

Track which collections get cited, for which prompts, and what AI referral traffic they receive, with the geo-tracking skill.

## Deliverable

```markdown
# Collection page: {collection name}
URL: {url} | Target query: {category keyword} (intent: commercial) | Date: {date}

## 1. Spec scorecard
| ID | Requirement | Status (Pass / Fail / Not verifiable) | Evidence |
(every COL row, then the C rows; Fails flagged P1 or P2: P1 = COL-03 to COL-08, COL-15, COL-17, COL-19; P2 = COL-20, COL-21, COL-22 and the rest)

## 2. Audit findings
(seo_audit.py SEO and GEO scores and high or medium findings for the clean URL, ?page=2 and a filter URL; section_audit.py blocks; curl raw-HTML result; GSC indexing symptoms; or "new page")

## 3. Competitor benchmark
(page_benchmark.py table, blocks and schema types the client lacks, metrics below the median, the leaders' slug motif, the information gain chosen)

## 4. Build
- Metadata: title ({n} chars), meta description ({n} chars), slug, H1
- Top intro (1-2 sentences)
- Bottom SEO block ({n} words, below the grid): question H2/H3 buying guide, comparison table of sub-types, 3-5 definitions, FAQ of 3+ real questions, links; bolding visible in markdown
- Facet and pagination directives: | URL pattern | Directive | Why |
- Thin collection decisions: | Collection | Products | Action |
- Internal links to add: | From | To | Anchor |
- JSON-LD (CollectionPage + ItemList + BreadcrumbList), handed to seo-schema-markup for implementation
- GEO checklist: raw HTML test, citable passages present, slug quality
- Placeholders {to confirm} for every unverified fact

## 5. Acceptance
(scripts re-run: remaining findings, each either fixed or a written owner decision; next actions by priority | # | Action | Why |)
```

## Common mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| 600 words of text at the top of the page | Pushes products below the fold, kills conversion | 1-2 sentences top, full block at the bottom (COL-07, COL-08) |
| Canonical from page 2+ to page 1 | Deep products lose their crawl path and deindex | Self-referencing canonicals, Page N titles (COL-19) |
| robots.txt block and noindex on the same URLs | Blocked pages are never fetched, the noindex is never seen | Sequence: noindex first, block later if needed (COL-17) |
| Indexing every color and size facet | Near-duplicate explosion, crawl waste, doorway page risk | The 3-test exception: demand, inventory, unique content (COL-18) |
| One boilerplate paragraph on 50 collections | Templated filler, nothing unique to rank or quote | Per-collection block or nothing (COL-16) |
| Keyword-stuffed block written for bots | Helpful content demotion risk, zero buyer value | Answer real buying questions, density under 2.5% (COL-13) |
| Zero bold in the block | No visible relevance, nothing for skimmers | Category keyword bolded in the intro, key facts bolded in the block (COL-13) |
| Product + Offer markup on every grid item, or empty ItemList | Wrong type for a listing; empty nodes fail validation | CollectionPage + ItemList of PDP URLs + BreadcrumbList (COL-22) |
| "Best prices" or "n°1" with no source | Discounted by shoppers and raters | Source it or remove it (COL-23) |
| Deleting seasonal collections every year | Discards the URL's accumulated equity | Stable URL, reused every season (COL-20, COL-24) |
| Text served to bots but hidden from users | Cloaking exposure | Accordion is fine; fully hidden is not (COL-08) |
| JS-only grid and filters | Invisible to AI assistants, fragile for Google | Server-render the grid and the block (COL-15) |
| Money collections absent from the menu | Weak internal authority on the pages that earn | Menu, sister links, breadcrumbs (COL-21) |

## Sources

- https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation (faceted navigation crawl management)
- https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading (self-canonical pagination, rel=prev/next status, infinite scroll)
- https://developers.google.com/search/docs/crawling-indexing/robots/intro (robots.txt does not deindex)
- https://developers.google.com/search/blog/2022/03/url-parameters-tool-deprecated (URL Parameters tool retirement)
- https://developers.google.com/search/docs/essentials/spam-policies (doorway pages, cloaking)
- https://developers.google.com/search/docs/appearance/structured-data/product (Product markup is for single-product pages)
- https://developers.google.com/search/docs/appearance/title-link (title rewriting behavior)
- https://ahrefs.com/blog/why-chatgpt-cites-pages/ (descriptive slugs, 89.78 vs 81.11 percent citation correlation)
- https://almcorp.com/blog/ai-citations-listicles-articles-product-pages/ (listicle and product page shares of AI citations)
- https://vercel.com/blog/the-rise-of-the-ai-crawler (AI crawlers do not execute JavaScript, measured)
- Common page spec C-01 to C-26: skills/seo-geo-audit/references/common-page-spec.md; finding codes: skills/seo-geo-audit/references/audit-checklist.md section 15

All thresholds labeled "field heuristic from 115+ agency audits" come from recurring patterns in real audit work, not from controlled studies. Treat them as strong defaults to adapt, not as guarantees.
