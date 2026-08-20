---
name: seo-content-collection-page
description: "Optimize e-commerce collection, category, and product listing pages (PLPs) for Google and AI assistants. Input: a collection or category page (Shopify, WooCommerce, Magento, BigCommerce, PrestaShop, or custom). Output: a bottom-of-page SEO text block, faceted-navigation and filter URL control, pagination canonicals, thin or empty collection cleanup, internal links, and CollectionPage schema. Use to create, write, or audit a category page or PLP, or to handle filtered URLs, pagination, duplicate or empty categories, and store crawl budget."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Collection Page SEO and GEO

This skill optimizes e-commerce collection and category pages (PLPs), the page type that wins category-level money queries yet ships with no editorial content on most stores (field observation from 115+ agency audits), using placement, faceting, and pagination rules that protect both rankings and conversion.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use

Use this skill when the user:

- Creates or rewrites a collection, category, shop, or product archive page
- Asks where category text should go, how long it should be, or what it should contain
- Faces filter or parameter URLs flooding Google Search Console ("Discovered, currently not indexed", crawl spikes)
- Configures pagination, canonicals, or indexing rules for listing pages
- Cleans up empty, thin, or duplicate collections
- Wants category pages cited in AI answers such as "best X" or "where to buy Y"
- Works on Shopify, WooCommerce, Magento, BigCommerce, PrestaShop, or a custom storefront

Hand off neighboring cases:

| Case | Skill |
|---|---|
| Individual product pages (PDPs) | seo-content-product-page |
| Sitewide link architecture and anchors | seo-internal-linking |
| JSON-LD implementation details | seo-schema-markup |
| Rendering, robots.txt, crawl budget mechanics | seo-technical |
| Validating search demand for a facet | seo-keyword-research |
| Supporting buying guides on the blog | seo-content-blog |
| Whole-site audit | seo-geo-audit |
| Passage-level citability writing | geo-visibility |
| Measuring AI citations and referrals | geo-tracking |

## Workflow

1. Identify the target query for the collection (the category keyword) and confirm it is commercial: check what page types rank. Validate facet-level demand with the seo-keyword-research skill before creating any facet landing page.
2. Fetch the raw server HTML with curl and compare with the rendered page. A product grid or text block that only appears after JavaScript runs is invisible to AI assistants and unreliable for Google. For an automated full check, run the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py).
3. Map the URL surface: list the filter, sort, and pagination parameters the template can emit, and check Search Console page indexing reports for parameter URL inflation.
4. Write the two text zones: a 1-2 sentence intro at the top, a 400-800 word block at the bottom (structure below). Before writing, mine Google Search Console for the page's own keyword demand (section 0 below) and weave the high-impression secondary keywords into the block in the searchers' exact wording. Open the body with the primary keyword as the very first word (never an em-dash, a dash, or filler), and bold the primary keyword plus the most important secondary keywords.
5. Fix the metadata: H1, title, slug, meta description.
6. Set the faceted navigation and pagination directives (decision tables below).
7. Evaluate thin or empty collections and merge or noindex them.
8. Wire internal links (menu, sister collections, top products, breadcrumbs) and the schema essentials, then hand details to seo-internal-linking and seo-schema-markup.
9. Apply the GEO layer below.
10. Deliver in the exact output format at the end of this document.

## Rules and thresholds

| Element | Rule | Basis |
|---|---|---|
| Top intro | 1-2 sentences maximum under the H1 | Field heuristic from 115+ agency audits |
| Bottom text block | 400-800 words below the product grid | Field heuristic from 115+ agency audits |
| H1 | The category keyword | Standard practice |
| Title | {Category} \| {Brand}, unique per collection | Standard practice |
| Slug | Category keyword, descriptive words, hyphens | Measured correlation (Ahrefs, see Sources) |
| Meta description | Handwritten, about 150-160 characters | Field heuristic from 115+ agency audits |
| Filtered URLs | Canonical to the clean collection URL by default | Standard practice |
| Indexable facets | Only with proven demand plus distinct inventory plus unique content | Standard practice + spam policy boundary |
| Pagination | Page 2+ self-canonical, never canonical to page 1 | Standard practice (Google pagination doc) |
| Thin collections | 0-2 products: merge or noindex | Field heuristic from 115+ agency audits |
| FAQ in bottom block | 3 questions minimum | Field heuristic from 115+ agency audits |
| Punctuation | Zero em dashes and zero en dashes, replaced by commas | House rule, most recognizable AI-writing tell |

Punctuation, non-negotiable: never leave an em dash (U+2014) or an en dash (U+2013) in copy that goes live on a client site. Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. The em dash is the single most recognizable tell of AI-written text, and one is enough for a shopper, or the client, to file the page as machine output. The rule covers every field you deliver: top intro, bottom block, FAQ answers, title tag, H1, meta description, alt text, facet labels, schema strings. Sweep the finished draft for both characters before handing it over. Hyphens in compound words and ranges written with "to" are untouched.

### 0. Mine Search Console for the page's real demand (do this first)

Before writing a single sentence, pull the collection URL's own performance from Google Search Console (Sorank GSC connector, or the GSC API): the queries the page already receives impressions on. The data tells you which keywords to write toward instead of guessing. Prioritise three buckets and place their terms into the intro, the H2/H3 questions, and the body of the block:

| Bucket | Signal | What to do |
|---|---|---|
| High impressions, low or zero clicks | The page is shown but the snippet does not earn the click, or the term is absent from the copy | Name the term explicitly, in the searcher's exact wording, in the H1-adjacent intro and a body passage |
| Real impressions, position 8-30 | One page off the clickable zone | Add a focused passage on the term so a single rank gain converts to traffic |
| Ranks for a term absent from title, H1 and body | A pure content gap | Close it verbatim: the demand already exists, the page just never says the words |

Mechanics: query GSC filtered to the exact collection URL (dimension = query) over a 90-180 day window, sorted by impressions. Capture the whole cluster of related terms, not just the head term, and reuse the searchers' phrasing, their exact words are the proven match for intent. This GSC pass is what supplies the secondary-keyword list for the bottom block; the seo-keyword-research skill stays the tool for validating brand-new facet pages that have no Search Console history yet.

### 1. Text placement: almost everything goes at the bottom

The SEO zone of a collection page is a 400-800 word rich text block placed below the product grid. At the top, under the H1, keep 1-2 sentences maximum.

Why the bottom: a text block at the top pushes the products below the fold, and visitors who came to browse bounce before seeing a single item, so the block costs sales. Placed at the bottom, the same text feeds Google and AI assistants without costing a conversion. Why it still counts for rankings: position on the page does not disqualify content; it is in the HTML, it is indexed and weighted. Collapsible or accordion presentation is fine as long as the text is present in the served HTML and accessible to users; serving the block to bots while hiding it from users entirely is cloaking territory (https://developers.google.com/search/docs/essentials/spam-policies).

Why 400-800 words: enough to cover the buying questions of the category and give assistants quotable passages, short enough to stay specific. Padding past what the category deserves invites helpful content demotions, not gains.

### 2. Bottom block structure

Build the block from these components, in this order:

| Component | Spec | Purpose |
|---|---|---|
| Buying guide headings | H2/H3 phrased as real questions: how to choose, which type for which use, sizing, materials, care | Matches the queries people and assistants actually ask |
| Comparison table | Sub-types of the category compared (rows: use case, price range, strengths) | The passage format AI answers quote for "best X" |
| Definitions | 3-5 category terms in plain language | Qualifies non-expert buyers, long-tail coverage |
| FAQ | 3 questions minimum, 40-80 word answers | Extraction material, objection handling |
| Links | Sub-collections, sister collections, 2-3 related blog guides | Distributes authority, deepens the topic cluster |

Write answers so the first sentence stands alone as a fact (passage construction details: geo-visibility skill). Source questions from search suggestions, People Also Ask, support tickets, and the seo-keyword-research skill output. Every collection gets its own block: a boilerplate paragraph rotated across 50 collections adds nothing and reads as templated filler.

### 3. Metadata

| Field | Pattern | Notes |
|---|---|---|
| H1 | {Category keyword} | "Linen Dresses", not "Our Collection" |
| Title | {Category} \| {Brand} or {Category} - {Qualifier} \| {Brand} | Unique per collection, about 60 characters |
| Slug | /collections/{category-keyword} | Descriptive words, hyphens, no internal IDs |
| Meta description | What the range covers + one differentiator + one offer fact | About 150-160 characters, handwritten |

Why unique titles matter here specifically: collection templates generate titles mechanically, so stores routinely ship dozens of near-identical titles, and Google then rewrites them unpredictably (https://developers.google.com/search/docs/appearance/title-link). Why descriptive slugs: in an Ahrefs analysis of pages cited by ChatGPT, 89.78 percent of cited pages had descriptive slugs versus 81.11 percent in the comparison set (measured, correlational: https://ahrefs.com/blog/why-chatgpt-cites-pages/). /collections/linen-dresses earns citations that /collections/c-118 does not.

Competitive nuance on the slug: look at the URL segment the leaders already ranking for the query use, and match that pattern rather than inventing your own. If the pages winning "photovoltaic label" all sit on a slug like /etiquette-photovoltaique, mirror that exact wording; Google has confirmed the term matches buyer intent on that query, so reusing the proven motif is safer than a synonym (field heuristic from 115+ agency audits).

### 4. Faceted navigation: control the URL explosion

Faceted navigation is the largest crawl trap in e-commerce: 200 collections times a handful of filters, values, and sort orders generate millions of parameter URLs (?color=red&size=m&sort=price) that are near-duplicates of each other. Google documents this as the canonical crawl waste scenario (https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation). Symptoms: "Discovered, currently not indexed" inflation in Search Console, crawl stats dominated by parameter URLs, fresh products taking weeks to index.

Pick the mechanism by goal, never stack them blindly:

| Goal | Mechanism | Caveat |
|---|---|---|
| Consolidate signals from filtered URLs | rel=canonical pointing to the clean collection URL | A hint, not a directive; Google can ignore it when the filtered page differs substantially |
| Stop crawl waste on filter combinations | robots.txt Disallow on parameter patterns | Does not deindex: blocked URLs can stay indexed without content if linked; Google also can no longer see any noindex on them |
| Remove filter URLs already indexed | meta robots noindex (or X-Robots-Tag) | The URL must remain crawlable until it drops out; only block it in robots.txt afterwards, if ever |

Google's own faceted-navigation doc adds a position worth knowing: it calls rel=canonical and nofollow "generally less effective in the long term" for facet control and states a preference for preventing the crawl outright (robots.txt, or URL fragments) when facet URLs are not meant for search (https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation). The table above is standard practitioner practice; on large catalogs where crawl budget is the binding constraint, lead with crawl prevention.
| Keep one facet as a landing page | Self-canonical + unique title, H1, and text | Only with proven demand and distinct inventory (below) |

The interaction that burns teams: robots.txt blocking and noindex are mutually exclusive on the same URL at the same time, because a blocked page is never fetched, so its noindex is never seen (https://developers.google.com/search/docs/crawling-indexing/robots/intro). Sequence them: noindex first, block later if needed. Note that Search Console's URL Parameters tool was retired in 2022; these on-site mechanisms are all you have (https://developers.google.com/search/blog/2022/03/url-parameters-tool-deprecated).

The exception, an indexable facet, must pass all three tests:

1. Real search demand for the facet term ("red dresses" has volume; "red dresses size M under 50" does not). Validate with seo-keyword-research.
2. Distinct inventory: several products meaningfully different from the parent collection's default view.
3. Unique content: its own title, H1, intro, and ideally its own bottom block.

Guideline risk to flag: mass-generating facet landing pages without demand or unique content matches Google's doorway page definition (https://developers.google.com/search/docs/essentials/spam-policies). Create facet pages one by one, by demand, never by template across the whole catalog.

Platform-specific parameter patterns and robots.txt examples: references/faceted-navigation-playbook.md.

### 5. Pagination: self-canonical, never to page 1

| Item | Rule |
|---|---|
| Canonical on page 2+ | Self-referencing (page 2 canonicals to page 2) |
| Canonical to page 1 | Never |
| Title on page 2+ | {Category} - Page {N} \| {Brand} |
| Pagination controls | Plain <a href> links, crawlable; not JS-only buttons |
| Indexability | Keep page 2+ indexable |
| rel=prev/next | Not used by Google for indexing since 2019; harmless to keep, never a fix |

Why "canonical to page 1" is the classic self-inflicted wound: it declares every paginated page a duplicate of page 1, so Google consolidates to page 1 and stops crawling deep pages. Products linked only from page 3+ lose their only crawl path and fall out of the index. Google's own e-commerce pagination documentation prescribes self-referencing canonicals (https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading).

Infinite scroll and "load more" need a paginated URL fallback with real <a href> links, because crawlers do not scroll or click. If the catalog is small, a single complete page with no pagination is simpler than any of this.

### 6. Empty and thin collections

| Collection state | Action | Why |
|---|---|---|
| 0 products, line discontinued | Merge: 301 to parent or closest sibling | A dead listing page is quality dead weight |
| 0 products, temporary or seasonal | Keep the URL in 200, reuse the same URL every season; noindex during the off-season is optional | The URL accumulates links and rankings year over year ("christmas gifts" should never change slug) |
| 1-2 products | Merge into the parent unless the term has strong demand and inventory will grow | A near-empty grid satisfies nobody and drags perceived site quality |
| 3+ products with demand | Keep and optimize | Enough inventory to satisfy the query |

Why this matters at the site level: dozens of indexable empty collections dilute the quality profile Google evaluates sitewide, and they waste the crawl budget the real collections need (field heuristic from 115+ agency audits).

Mono-product case, the "real catalogue" tactic: a business selling essentially one product has no collection to fill, so the collection page looks empty and barely exists to Google. Split the single product into genuine variants (packaging, color, format, size, quantity bundle) so the collection lists several real, separately purchasable items and reads as a true category rather than a one-item shell (field heuristic from 115+ agency audits). The variants must be honestly distinct purchasable options, not the same item cloned under different URLs, which would be the doorway and near-duplicate problem from section 4.

### 7. Internal linking: collections are the money pages

In most audited stores, collections, not PDPs, win the category-level queries that drive revenue (field observation from 115+ agency audits). Link them accordingly:

- Main menu: every revenue collection reachable in one click from the home page
- Sister collections: a "related categories" block on each collection
- Top products: featured products link back to their collection
- Breadcrumbs on every PDP and sub-collection, marked up with BreadcrumbList
- Blog guides: each buying guide links to its collection with the category keyword as anchor

Anchor text: the category keyword, varied naturally. Full architecture and anchor strategy: seo-internal-linking skill.

### 8. Schema essentials (summary)

| Type | Use |
|---|---|
| CollectionPage | The page type |
| ItemList | The products listed, as URLs to the PDPs, consistent with the rendered first page |
| BreadcrumbList | The category path |

Do not attach full Product + Offer markup to every grid item: Google's Product structured data targets pages about a single product, and category pages should use ItemList instead (https://developers.google.com/search/docs/appearance/structured-data/product). Markup must mirror what the page displays. Implementation patterns and validation: seo-schema-markup skill.

## GEO layer

### Collection pages get cited in "best X" and "where to buy Y" answers

AI assistants favor list-format content: an analysis of AI citations in commerce contexts found listicles taking the largest share of citations, with product pages at about 13.7 percent (single-source study, not independently replicated: https://almcorp.com/blog/ai-citations-listicles-articles-product-pages/). A collection page with a buying-guide block, a comparison table, and an FAQ presents the same extractable structure as a listicle, with live inventory attached. A bare product grid offers an assistant nothing to quote; the bottom block is what makes the page citable.

### Write the bottom block as extraction material

The comparison table and the FAQ answers are the passages assistants lift. Make each FAQ answer's first sentence a standalone fact, keep the comparison table small and labeled, and state concrete criteria (price ranges, materials, use cases) rather than adjectives. Passage construction in depth: geo-visibility skill.

### Descriptive slugs, stable URLs

Beyond the Ahrefs citation correlation (section 3), assistants cite and revisit URLs: renaming a collection slug discards the citations the old URL earned. If a rename is unavoidable, 301 the old URL and update internal links the same day (field practice from 115+ agency audits).

### Server-rendered HTML only

Many storefront themes render the product grid, filters, and even the text block client-side. Major AI crawlers fetch but do not execute JavaScript (measured by Vercel across GPTBot, ClaudeBot, and others: https://vercel.com/blog/the-rise-of-the-ai-crawler), so a JS-rendered collection page is an empty page to ChatGPT, Claude, and Perplexity. Test with curl: the H1, the bottom block, and at least the first grid of product links must appear in the raw HTML. Rendering fixes: seo-technical skill.

### Source the text from Google Maps reviews

For a directory or listing page that profiles a real venue (a marketplace entry, a local annuaire, a curated collection of places), the venue's own Google Maps reviews are a source of fresh, specific themes. Use them as research, not as text: read the recent reviews and write, in your own words, a short current passage about what customers consistently mention: the atmosphere, the felt experience, in plain factual language attributed as customer feedback rather than presented as your own claims (field heuristic from 115+ agency audits). Licensing caveat: Google Maps Platform terms restrict caching and repurposing Places content (reviews are meant to be displayed as-is, with attribution, via the API), and each review text remains its author's copyright, so never republish or lightly paraphrase the review texts themselves. Done this way, the page gains concrete, up-to-date detail that a templated description lacks, exactly the kind of specific material assistants quote.

### Position 2 on navigational brand queries

On navigational queries shaped "brand + reviews" or "brand + alternative", position 1 is the brand's own official property and is not realistically contestable. The opening is position 2: a comparative or directory page that lists the brand alongside its alternatives, or aggregates independent reviews of it (field heuristic from 115+ agency audits). This is a recurring play for marketplaces and directories, the page does not need to outrank the brand, only to own the second slot that captures the searcher looking for outside opinion. Stay accurate about every brand named; invented comparison facts are a liability.

### Measure

Track which collections get cited, for which prompts, and what AI referral traffic they receive, with the geo-tracking skill.

## Output format

Deliver every collection page optimization in exactly this structure:

```markdown
# Collection Page Optimization Brief: {collection name}

URL: {url}
Target query: {category keyword} (intent: commercial)
Date: {date}

## 1. Scorecard

| Check | Status | Priority |
|---|---|---|
| Top intro limited to 1-2 sentences | pass / fail | P1 |
| Bottom block 400-800 words below the grid | pass / fail | P1 |
| H1 / title / slug / meta | pass / fail | P1 |
| Filtered URLs canonicalized or controlled | pass / fail | P1 |
| Pagination self-canonical, crawlable links | pass / fail | P1 |
| No indexable empty or thin collections | pass / fail | P2 |
| Internal links (menu, sisters, breadcrumbs) | pass / fail | P2 |
| CollectionPage + ItemList + BreadcrumbList | pass / fail | P2 |
| Grid and text present in raw HTML | pass / fail | P1 |

## 2. Metadata

- Title ({n} chars): {title}
- Meta description ({n} chars): {meta}
- Slug: {slug}
- H1: {h1}

## 3. Top intro (1-2 sentences)

{intro}

## 4. Bottom SEO block ({n} words, placed below the product grid)

{H2/H3 buying-guide sections, comparison table of sub-types, 3-5 definitions, 3-question FAQ, internal links}

## 5. Facet and pagination directives

| URL pattern | Directive | Why |
|---|---|---|

## 6. Thin collection decisions

| Collection | Products | Action |
|---|---|---|

## 7. Internal links to add

| From | To | Anchor |
|---|---|---|

## 8. Schema checklist

{gaps; hand implementation to seo-schema-markup}

## 9. GEO checklist

{raw HTML test result, citable passages present, slug quality}

## 10. Next actions by priority

| # | Action | Why |
|---|---|---|
```

## Common mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| 600 words of text at the top of the page | Pushes products below the fold, kills conversion | 1-2 sentences top, full block at the bottom |
| Canonical from page 2+ to page 1 | Deep products lose their crawl path and deindex | Self-referencing canonicals, Page N titles |
| robots.txt block and noindex on the same URLs | Blocked pages are never fetched, the noindex is never seen | Sequence: noindex first, block later if needed |
| Indexing every color and size facet | Near-duplicate explosion, crawl waste, doorway page risk | The 3-test exception: demand, inventory, unique content |
| One boilerplate paragraph on 50 collections | Templated filler, nothing unique to rank or quote | Per-collection block or nothing |
| Keyword-stuffed block written for bots | Helpful content demotion risk, zero buyer value | Answer real buying questions |
| Deleting seasonal collections every year | Discards the URL's accumulated equity | Stable URL, reused every season |
| Text served to bots but hidden from users | Cloaking exposure | Accordion is fine; fully hidden is not |
| JS-only grid and filters | Invisible to AI assistants, fragile for Google | Server-render the grid and the block |
| Money collections absent from the menu | Weak internal authority on the pages that earn | Menu, sister links, breadcrumbs |

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

All thresholds labeled "field heuristic from 115+ agency audits" come from recurring patterns in real audit work, not from controlled studies. Treat them as strong defaults to adapt, not as guarantees.
