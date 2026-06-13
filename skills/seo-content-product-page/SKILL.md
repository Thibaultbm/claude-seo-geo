---
name: seo-content-product-page
description: "Optimize e-commerce product pages (PDPs) for Google and for AI assistants that now recommend products directly. Input: a product page or description (Shopify, WooCommerce, Magento, BigCommerce, PrestaShop, Wix, Webflow, or custom). Output: a rewritten PDP with unique copy, FAQ and definition blocks, review and real-photo rules, title/H1/slug/meta, out-of-stock handling, Product schema, and ChatGPT Shopping feed notes. Use to write, rewrite, or audit a product page, or when PDPs get no traffic or traffic without sales."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Product Page SEO and GEO

This skill optimizes e-commerce product pages (PDPs) so they rank in Google and get recommended directly by AI assistants, using field rules derived from 115+ real agency audits combined with sourced 2026 practices.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use

Use this skill when the user:

- Writes or rewrites a product description or a full product page
- Audits a PDP with no rankings, no traffic, or traffic without sales
- Asks how to get products recommended by ChatGPT, Perplexity, Claude, Gemini, or Google AI Overviews
- Handles out-of-stock, seasonal, or discontinued product URLs
- Reviews PDP titles, H1s, slugs, meta descriptions, images, reviews, trust badges, or Product schema
- Works on Shopify, WooCommerce, Magento, BigCommerce, PrestaShop, Wix, Webflow Ecommerce, or a custom storefront

Hand off neighboring cases:

| Case | Skill |
|---|---|
| Category, collection, or listing pages (PLPs) | seo-content-collection-page |
| Service or offer pages outside e-commerce | seo-content-service-page |
| Supporting blog content for a product | seo-content-blog |
| Keyword and intent mapping | seo-keyword-research |
| Whole-site audit | seo-geo-audit |
| Rendering, crawl access, AI crawler behavior | seo-technical |
| JSON-LD implementation details | seo-schema-markup |
| Passage-level citability writing | geo-visibility |
| Measuring AI citations and referrals | geo-tracking |

## Workflow

1. Confirm the target query and its intent. A PDP targets transactional queries only: product name searches, "buy X", "X price". If the query is informational ("how to choose X", "X vs Y"), stop and plan a blog post that links to the PDP instead; map this with the seo-keyword-research skill. Why: Google types its result pages by intent, so a PDP almost never ranks for an informational query regardless of quality.
2. Fetch the page as crawlers see it. Use curl to get the raw server HTML and compare it with the browser-rendered page. Anything absent from the raw HTML is invisible to AI assistants and unreliable for Google. For an automated full check, run the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py).
3. Score the page against the rules and thresholds below. Record every gap with a priority.
4. Rewrite the content blocks: description, specs, comparison table, FAQ, definitions.
5. Fix the metadata: title, H1, slug, meta description.
6. Check schema essentials (Product, Offer, AggregateRating, Review) and confirm the markup mirrors the visible page. Implementation belongs to the seo-schema-markup skill.
7. Apply the GEO layer below: every fact in server HTML, page self-sufficiency, product feed.
8. Deliver the result in the exact output format at the end of this document.

## Rules and thresholds

| Element | Rule | Basis |
|---|---|---|
| Description length | 150-200 words minimum, unique, benefits first | Field heuristic from 115+ agency audits |
| Description source | Never the manufacturer boilerplate | Duplicate content behavior (section 1) |
| FAQ block | 3+ real buyer questions at the bottom of the PDP | Field heuristic from 115+ agency audits |
| Definitions block | About 5 technical terms explained in plain language | Field heuristic from 115+ agency audits |
| Reviews | Stars and count visible at the top of the page | Field heuristic from 115+ agency audits |
| Images | Real product photos only on PDPs, never AI-generated | Trust + Merchant Center compliance |
| Title tag | Product + category (+ brand), unique, about 60 characters | Standard practice |
| H1 | The product name, exactly one H1 | Standard practice |
| Slug | Main keyword, descriptive words, hyphens, no SKU codes | Measured correlation (Ahrefs, see Sources) |
| Meta description | Handwritten, about 150-160 characters | Field heuristic from 115+ agency audits |
| Out of stock | HTTP 200 + availability markup + alternatives, never 404 | Standard practice |
| CRO threshold | Below about 100 organic visitors/day, build traffic before conversion tweaks | Field heuristic from 115+ agency audits |

### 1. Description: 150-200 words minimum, unique, benefits first

Write a description of at least 150-200 words that exists nowhere else on the web. The manufacturer datasheet is republished by every retailer carrying the product: Google clusters those duplicates and surfaces one version (usually the strongest domain or the brand itself), so a duplicated description leaves the page competing on domain authority alone. AI assistants similarly skip pages that add nothing beyond what they already cite.

Structure the text for a buying decision, in this order:

1. Two or three benefit-led paragraphs: who the product is for, the top 3 outcomes it delivers, with concrete proof (numbers, materials, certifications).
2. Characteristics translated into use: "750 ml titanium pot" becomes "boils water for two people in under four minutes".
3. Specs, compatibility, materials, care instructions as a bulleted list or table.

150-200 words is a floor, not a target to pad toward. Filler text written for word count works against the page under Google's helpful content signals. Guideline risk: if you generate descriptions for hundreds of SKUs with an LLM, add a human review pass per page; publishing unreviewed generated text at scale matches Google's scaled content abuse spam policy (https://developers.google.com/search/docs/essentials/spam-policies).

### 2. Bottom of the page: FAQ block plus definitions block

Add two blocks below the main description (field pattern observed on premium e-commerce brands that lead their niches, from 115+ agency audits):

| Block | Spec | Purpose |
|---|---|---|
| FAQ | 3+ questions, H3 per question, 40-80 word answers | AI extraction material, long-tail queries, objection handling |
| Definitions | About 5 technical terms from the product, 1-3 sentences each | Same, plus it qualifies non-expert buyers |

Source the questions from pre-sales emails, support tickets, Google's People Also Ask, and review content. Each question targets a long-tail query too small to deserve its own page ("does X fit Y", "is X machine washable") and removes a purchase objection right where the decision happens. Write the first sentence of each answer as a standalone fact; the geo-visibility skill covers passage formatting in depth.

Guideline note: do not add FAQPage markup expecting rich results. Google removed FAQ rich results for most sites in August 2023 (https://developers.google.com/search/blog/2023/08/howto-faq-changes). The value is the on-page content itself; the markup is optional.

### 3. Images: real product photos only

Use real photographs of the actual product: multiple angles, one scale or in-use shot. Never use AI-generated product images on a PDP, even photorealistic ones. Two reasons: buyers detect synthetic imagery at the exact moment they decide to pay, and Google Merchant Center requires images that accurately represent the product, so misrepresentation risks disapproval of the listing (https://support.google.com/merchants/answer/6324350). AI imagery is tolerable in blog illustrations when photorealistic, never on product pages (field rule from 115+ agency audits).

Copycat and dropshipping case: photos taken straight from the supplier or manufacturer, the ones every other reseller of the same item also uses, are the duplicate-image equivalent of the duplicate description (section 1). Merchant Center expects images that represent your own listing rather than reused stock, so identical supplier photos get the listing disapproved, and a page carrying the same images as fifty competitors gives Google and AI assistants nothing to distinguish it. Shoot the product yourself: own photos are the only fix (field heuristic from 115+ agency audits).

Write alt text as product name plus the distinguishing attribute shown. Image weight and loading belong to the seo-technical skill.

### 4. Reviews: visible at the top, story format

Place the star rating and review count next to the product title, above the fold. The full review list can live lower on the page. Why: reviews are the strongest objection killer, and a rating buried at the bottom is never seen by the 80 percent of visitors who do not scroll that far (field heuristic from 115+ agency audits).

The review format that converts (field heuristic): first name + buyer situation + the problem they had + the result. "Marie, runs a food truck: needed a stove that survives daily transport, two years in it still lights first try." Video reviews outperform written ones where available (field observation from the same audits).

Never fabricate, seed, or incentivize undisclosed reviews: this violates Google spam policies and consumer protection law in most markets. AggregateRating and Review markup must match the reviews actually displayed (section 10).

### 5. Reassurance badges near the buy button

Place payment security, delivery time and cost, and the returns window within sight of the add-to-cart button. These answer the three objections active at the decision point. Render them as HTML text, not only icons baked into images: AI assistants extract shipping and returns facts when comparing offers, and the OpenAI product feed has dedicated fields for them (see GEO layer).

### 6. Metadata: title, H1, slug, meta description

| Field | Pattern | Notes |
|---|---|---|
| Title | {Product name} - {Category} \| {Brand} | About 60 characters; include the attribute buyers search (material, size, color) |
| H1 | {Product name} | Exactly one H1 on the page |
| Slug | /products/{primary-keyword} | Descriptive words with hyphens; never SKU codes or internal IDs |
| Meta description | Benefit + differentiator + one offer fact (shipping or returns) | About 150-160 characters, handwritten |

Why handwritten meta descriptions: auto-generated ones repeat the first sentence of the page; a written one adds the offer facts that win the click. Google rewrites titles and snippets when it judges them poor (https://developers.google.com/search/docs/appearance/title-link), which is one more reason to write them deliberately.

Why descriptive slugs: in an Ahrefs analysis of pages cited by ChatGPT, 89.78 percent of cited pages had descriptive slugs versus 81.11 percent in the comparison set (measured, correlational: https://ahrefs.com/blog/why-chatgpt-cites-pages/).

### 7. Intent split: one query family per page type

| Query type | Example | Page that ranks |
|---|---|---|
| Transactional | "titanium camping stove", "buy ti stove 2" | Product page |
| Comparative or informational | "best camping stove for two", "titanium vs steel stove" | Blog post or guide that links to the PDP |

Check the live results page before assigning a query: if it shows guides and listicles, a PDP will not break in. Build the supporting article with the seo-content-blog skill and link it to the PDP. Mapping method: seo-keyword-research skill.

### 8. Out of stock, discontinued, variants

| Scenario | Action | Why |
|---|---|---|
| Temporarily out of stock | Keep HTTP 200 and indexable, set Offer availability to OutOfStock, show a restock estimate, list alternatives, offer a back-in-stock email | The URL keeps its rankings and captures demand while supply returns |
| Discontinued, close substitute exists | 301 to the substitute, or keep the page live with a clear notice plus links to alternatives | Preserves accumulated link equity and rankings |
| Discontinued, no substitute | Keep 200 with alternatives for a transition period, then 301 to the parent collection | Avoids dropping users and crawlers on a dead end |
| Zero traffic, zero backlinks, dead product | 410 or 404 acceptable | Nothing to preserve |

Never return a 404 on a product URL that has rankings, traffic, or backlinks: you discard signals that took years to accumulate, and recovery after reinstating the page takes months (field observation from 115+ agency audits).

Variants: give color and size variants one canonical parent unless a specific variant has its own search demand, in which case it earns an indexable URL with unique content (Google's guidance: https://developers.google.com/search/docs/specialty/ecommerce/product-variants).

### 9. Traffic before conversion micro-optimization

Below about 100 organic visitors per day, spend optimization time on traffic volume, not conversion tweaks (field heuristic from 115+ agency audits). The math: typical e-commerce stores convert in the 2-4 percent range (field observation consistent with public benchmarks), so 30 visitors a day produce about one order a day. No A/B test reaches significance at that volume, and a conversion lift on near-zero traffic is near-zero revenue.

What still pays at low traffic: one-off hygiene from this skill (reviews at the top, badges, real photos, the description rewrite), because these are builds, not tests. Then shift effort to more indexable pages (PDPs, collections, blog) and internal links.

### 10. Schema essentials (summary)

Minimum viable markup for a PDP:

| Type | Required properties |
|---|---|
| Product | name, image, description, sku, brand |
| Offer (nested) | price, priceCurrency, availability, url |
| AggregateRating | Only when visible reviews exist on the page |
| Review | Only for reviews actually displayed |

Guideline risk to flag every time: structured data must mirror the visible page content. Markup that contradicts the page (a rating with no reviews shown, a price that differs from the displayed one) can trigger a structured data manual action (https://developers.google.com/search/docs/appearance/structured-data/sd-policies). Validate with the Rich Results Test. Full JSON-LD patterns, merchant listing fields (shipping, returns), and validation workflow: seo-schema-markup skill.

### 11. Marketplace listings: Amazon and FBA

Amazon is a search engine and a separate market with its own ranking, not a copy of Google. The same on-page audit transposes to an Amazon listing: study the keywords and descriptions the competing listings rank for on Amazon itself, then optimize the listing title, bullets, and product description as you would a web PDP, around the terms buyers type on that marketplace (field heuristic from 115+ agency audits). Keep the channel distinct: an Amazon listing and the store's own PDP serve different surfaces and rarely compete with each other. The reusable parts of this skill are the unique benefit-led copy, the buyer-question coverage, and the real-photos rule (sections 1, 2, 3); the platform-specific mechanics (A9 ranking, FBA fulfillment) live outside the scope here.

## GEO layer

### AI assistants recommend product pages directly

This is the structural difference from classic SEO, where blog content captured most organic entry points. Assistant answers to "best X for Y" and "where can I buy X" now link PDPs directly: one 2025 analysis of AI citations in commerce contexts measured product pages at about 13.7 percent of citations, with listicle-format content taking the largest share (https://almcorp.com/blog/ai-citations-listicles-articles-product-pages/). Two consequences: the PDP is now a citation target in its own right, and it must stand alone, because the assistant quotes one page, not your whole site.

### Make the PDP self-sufficient

An assistant can only recommend what the page states. Checklist:

- Full spec table in HTML
- Price and currency visible as HTML text
- Shipping cost, delivery time, returns window stated in text
- FAQ and definitions blocks (section 2)
- Comparison versus alternatives (below)
- Review count, average rating, and 2-3 quoted reviews in HTML

If a fact is missing from the page, the assistant either omits the product or fills the gap from a competitor's page.

### Submit the ChatGPT Shopping product feed

OpenAI publishes a product feed specification for ChatGPT Shopping and agentic checkout: JSONL, CSV, TSV, or Parquet formats, delivery by SFTP push or scheduled fetch, refresh as often as every 15 minutes, with fields covering price, availability, reviews, Q&A, and video (https://developers.openai.com/commerce/specs/file-upload/products). Merchants enroll at https://chatgpt.com/merchants. For an e-commerce site, submitting and maintaining this feed is the first GEO action to take: it replaces crawling guesswork with declared, refreshed data. No API key is needed to follow this skill; enrollment is the merchant's own action. Field mapping table: references/product-page-blueprint.md.

### Keep every fact in server-rendered HTML

Major AI crawlers fetch pages but do not execute JavaScript (measured by Vercel across GPTBot, ClaudeBot, and others: https://vercel.com/blog/the-rise-of-the-ai-crawler). A PDP whose price, description, or reviews are injected client-side is partially or fully invisible to assistants. Test with curl; fixes (SSR, prerendering) belong to the seo-technical skill.

### Add a comparison table

A short "this product versus the two closest alternatives" table (rows: price, key specs, ideal use case) is exactly the passage format assistants lift for "best X" answers, and it keeps the comparison happening on your page instead of a third-party listicle. Stay factually accurate about competitor products: invented specs are a liability. Passage construction details: geo-visibility skill.

### Measure

Track assistant citations, share of voice, and AI referral traffic with the geo-tracking skill. Re-run checks after each significant page change.

## Output format

Deliver every product page optimization in exactly this structure:

```markdown
# Product Page Optimization Brief: {product name}

URL: {url}
Target query: {query} (intent: transactional)
Date: {date}

## 1. Scorecard

| Check | Status | Priority |
|---|---|---|
| Unique description, 150-200+ words | pass / fail | P1 |
| FAQ block (3+ questions) | pass / fail | P1 |
| Definitions block (about 5 terms) | pass / fail | P2 |
| Real product photos | pass / fail | P1 |
| Reviews visible at the top | pass / fail | P1 |
| Reassurance badges near buy button | pass / fail | P2 |
| Title / H1 / slug / meta | pass / fail | P1 |
| Price and specs in raw HTML | pass / fail | P1 |
| Schema mirrors visible content | pass / fail | P1 |
| Out-of-stock handling correct | pass / fail / n.a. | P2 |

## 2. Metadata

- Title ({n} chars): {title}
- Meta description ({n} chars): {meta}
- Slug: {slug}
- H1: {h1}

## 3. Rewritten description ({n} words)

{benefits-first description, then specs list}

## 4. Comparison block (this product vs alternatives)

{3-column table: this product, alternative A, alternative B}

## 5. FAQ block (bottom of page)

{3-5 questions with 40-80 word answers}

## 6. Definitions block

{about 5 terms, 1-3 sentences each}

## 7. Schema checklist

{Product / Offer / AggregateRating gaps; hand implementation to seo-schema-markup}

## 8. GEO checklist

{raw HTML visibility result, self-sufficiency gaps, feed status}

## 9. Next actions by priority

| # | Action | Why |
|---|---|---|
```

## Common mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| Pasting the manufacturer description | Duplicated across every retailer; the page competes on domain strength alone | Rewrite unique, benefits first |
| AI-generated product images | Breaks trust at payment; Merchant Center disapproval risk | Real photos, multiple angles |
| Schema price or rating differing from the page | Structured data manual action risk | Markup mirrors visible content |
| 404 on a discontinued product with history | Discards years of signals and backlinks | Keep 200 with alternatives, or 301 to substitute |
| Targeting informational queries with a PDP | Intent mismatch; the page type cannot rank there | Blog post that links to the PDP |
| Reviews hidden in a JS-loaded tab at the bottom | Invisible to crawlers and to most visitors | Stars at the top, reviews in server HTML |
| A/B testing at 30 visitors/day | No statistical power; near-zero revenue upside | Build traffic volume first |
| Price rendered by JavaScript or inside an image | Assistants cannot quote the offer | Price as HTML text |
| Mass-generating descriptions with no review pass | Scaled content abuse policy exposure | Human review per page |
| Adding FAQPage markup for rich results | FAQ rich results removed for most sites in 2023 | Keep the FAQ content; treat markup as optional |

## Sources

- https://almcorp.com/blog/ai-citations-listicles-articles-product-pages/ (product pages at about 13.7 percent of AI citations)
- https://developers.openai.com/commerce/specs/file-upload/products (ChatGPT Shopping feed specification)
- https://chatgpt.com/merchants (merchant enrollment)
- https://ahrefs.com/blog/why-chatgpt-cites-pages/ (descriptive slugs, 89.78 vs 81.11 percent citation correlation)
- https://vercel.com/blog/the-rise-of-the-ai-crawler (AI crawlers do not execute JavaScript, measured)
- https://developers.google.com/search/docs/appearance/structured-data/product (Product markup reference)
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies (markup must reflect visible content, manual actions)
- https://developers.google.com/search/docs/essentials/spam-policies (scaled content abuse)
- https://developers.google.com/search/blog/2023/08/howto-faq-changes (FAQ rich results removal)
- https://support.google.com/merchants/answer/6324350 (Merchant Center image requirements)
- https://developers.google.com/search/docs/specialty/ecommerce/product-variants (variant URL handling)
- https://developers.google.com/search/docs/appearance/title-link (title rewriting behavior)

All thresholds labeled "field heuristic from 115+ agency audits" come from recurring patterns in real audit work, not from controlled studies. Treat them as strong defaults to adapt, not as guarantees.
