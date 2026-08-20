---
name: seo-technical
description: "Find and fix what stops a site from being indexed, fast, and visible to AI crawlers. Input: a site or specific pages. Output: fixes for indexation, robots.txt, sitemaps, IndexNow, Core Web Vitals (LCP/INP/CLS), JS rendering, AI crawler access (GPTBot, ClaudeBot, PerplexityBot, and more), canonicals, hreflang, HTTPS, and migrations. Repo reference for AI crawler control. Use for a technical audit, pages not indexed, slow pages, robots.txt or sitemap issues, llms.txt, content invisible to ChatGPT, a migration, or a hacked site."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Technical SEO: crawl, index, render

Technical SEO decides whether content can be fetched, parsed, indexed, and trusted by Google, Bing, and AI answer engines (ChatGPT, Claude, Perplexity, Gemini). In 2026 the discipline split in two: Googlebot renders JavaScript and tolerates slow pages, AI crawlers do neither. Treat the raw HTML response as the product.

Work in this order: indexation, rendering, speed. A fast page that is not indexed earns nothing. An indexed page whose content only appears after client-side JavaScript runs is invisible to every AI engine except Google's. Every threshold below is labeled either official or measured (with a source URL) or field heuristic from 115+ agency audits.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use this skill

Use it for:

- Full technical audits and pre-sales triage of any site
- "Why is my site (or page) not indexed" investigations
- robots.txt, meta robots, sitemap, canonical, and hreflang work
- Core Web Vitals (LCP, INP, CLS), PageSpeed, image weight
- JavaScript rendering decisions: SPA versus SSR versus SSG
- AI crawler access: this skill owns references/ai-crawlers.md, the canonical crawler reference for the whole skill set
- llms.txt questions (see the honest verdict section)
- Site migrations, redesigns, domain changes
- Hacked-site cleanup (injected spam links)

Hand off neighboring problems:

- Diagnosing a dated traffic or ranking loss before fixing anything: use the seo-traffic-drop skill
- Converting a client-rendered site built by an AI generator (Lovable, Base44, Bolt, and similar) into served HTML: use the seo-ai-site-builders skill
- Orphan pages and link architecture: use the seo-internal-linking skill
- JSON-LD and structured data: use the seo-schema-markup skill
- Writing content so AI engines quote it: use the geo-visibility skill
- Measuring AI citations and AI referral traffic: use the geo-tracking skill
- One-pass scored audit of a whole site: use the seo-geo-audit skill

## Workflow

### Step 0: Secure measurement access

Before any recommendation, confirm both:

1. Google Search Console is verified (domain property preferred) and you can actually open it.
2. GA4, or an equivalent analytics tool, is installed and collecting.

Field finding from 115+ agency audits: a large share of audited sites had neither installed, or had them installed with nobody able to access the accounts. Without GSC you cannot see coverage, queries, or manual actions, and every later step degrades into guessing. Set both up first, then add Bing Webmaster Tools: it imports GSC properties in a few clicks and matters in 2026 because Bing's index feeds ChatGPT search (https://yoast.com/chatgpt-search/).

For a fast automated first pass, run the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py), which checks robots.txt AI bot rules, sitemap, and on-page basics. Use its output to direct the manual work below.

### Step 1: Read the indexation state

In GSC, open Indexing > Pages and compute the ratio of indexed to submitted pages.

- 75 percent or more indexed (for example 3,000 indexed of 4,000 submitted) is healthy on a mature site (field heuristic).
- Below 50 percent, stop and investigate before anything else: duplication, thin pages, crawl traps, leftover noindex, or rendering failures.

Then act on the gaps:

- Priority pages not indexed: inspect each with the URL Inspection tool, fix the reported cause, then click Request Indexing. The quota is roughly 10 to 12 requests per day per property, so spend it on money pages, not the archive.
- Bulk indexation, not page by page: ignore the "index 10 URLs per day" ritual some platforms (Wix and others) push. Manual one-by-one submission scales to nothing. Submit the full sitemap in GSC once and let Google discover every URL from it; reserve manual Request Indexing for a handful of priority pages (field heuristic from 115+ agency audits).
- Scaled and programmatic pages, the indexation condition: thousands of generated pages (one per city, per combination) only get indexed when each page carries genuinely unique content. The same block copied across all of them is the classic non-indexation cause: Google treats near-duplicate templates as one page and drops the rest. Uniqueness per page is the price of admission for scaled content, not an optimization (field heuristic from 115+ agency audits).
- 404s with history: any URL that previously earned traffic or backlinks and now returns 404 gets a 301 to the closest equivalent page. Never blanket-redirect everything to the homepage: Google treats irrelevant mass redirects as soft 404s.
- Orphan pages: target zero. Detection and fixes belong to the seo-internal-linking skill.

Measurement artifact (September 2025): Google removed the num=100 results parameter. Many properties saw desktop impressions collapse and average position improve overnight because rank-tracking bots stopped loading 100-result pages. Check clicks before declaring a loss: clicks typically stayed flat. Never present this artifact to a client as a traffic drop (https://searchengineland.com/google-num100-impact-data-462231).

### Step 2: Crawl controls: robots.txt, sitemaps, meta robots

robots.txt:

- Must contain a Sitemap: line pointing at the sitemap index.
- Must not contain Disallow: / (shipped staging configs cause this more often than expected; check it first on any sudden deindexation).
- AI bot rules: decide with the GEO layer below and references/ai-crawlers.md.

Sitemap.xml:

- Hard size limit: 50,000 URLs and 50 MB uncompressed per sitemap file. Google rejects an oversized file entirely, not just the overflow, so every URL in it loses sitemap discovery at once. Above the limit, split into child sitemaps under a sitemap index (an index can list up to 50,000 sitemaps, and index files can be submitted per subsection on very large sites) (https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps).
- Segment by content type (sitemap-pages.xml, sitemap-posts.xml, sitemap-products.xml) under one index. Why: GSC reports coverage per sitemap, so segmentation reveals which template fails to get indexed. Segmentation also keeps each file safely under the 50,000 URL cap.
- Keep lastmod honest: update it only when content meaningfully changes. Google states it ignores lastmod when it is uniformly fresh or inaccurate.
- Do not ping Google's sitemap endpoint: deprecated in June 2023, it returns 404. Submit through GSC and the robots.txt Sitemap: line (https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping).
- Set up IndexNow for Bing: instant push of new and updated URLs, built into many CMS plugins and Cloudflare. Bing is a primary gateway into ChatGPT search, which makes Bing Webmaster Tools standard equipment in 2026 (https://yoast.com/chatgpt-search/).

Discovery for ultra-fresh topics: when the site publishes time-sensitive news, add a dedicated News sitemap plus an RSS or Atom feed so Google can pick up items within minutes; an RSS feed is also the fastest way to source breaking topics worth covering. This channel only fits genuinely fresh, newsworthy content, not the evergreen archive.

Meta robots versus robots.txt, the distinction behind most "why is this still indexed" tickets:

| Goal | Correct tool | Why |
|---|---|---|
| Keep a page out of the index | meta robots noindex, page stays crawlable | Google must fetch the page to see the noindex |
| Keep crawlers out of infinite or private URL spaces | robots.txt Disallow | Saves crawl budget; does NOT deindex |
| Both on the same URL | Never combine them | Disallow prevents Google from ever seeing the noindex; the URL can stay indexed from external links |

A disallowed page can appear in results as a URL-only listing. If something must disappear, allow the crawl, serve noindex (or 404/410), and use the Removals tool for urgent cases.

Crawl budget (sites above roughly 10,000 URLs):

- Faceted navigation, calendar archives, and internal search results generate near-infinite URL spaces. Disallow them in robots.txt and keep them out of sitemaps.
- Read GSC Settings > Crawl stats: spikes on parameter URLs mean budget burned on noise instead of money pages.
- Below a few thousand URLs, crawl budget is never the bottleneck; do not invoice work on it (field heuristic).

### Step 3: JavaScript rendering, the number one technical check of 2026

No AI crawler executes JavaScript. The Vercel and MERJ study of 500M+ crawler fetches found that GPTBot, ClaudeBot, PerplexityBot, and Meta-ExternalAgent sometimes download JavaScript files (11.5 percent of ChatGPT fetches, 23.8 percent of Claude fetches) but execute none of it. Googlebot is the only major crawler that renders (https://vercel.com/blog/the-rise-of-the-ai-crawler and https://www.gsqi.com/marketing-blog/ai-search-javascript-rendering/).

Consequence map:

| Engine | Sees client-side rendered content |
|---|---|
| Google search, AI Overviews, AI Mode, Gemini grounding | Yes (Googlebot renders) |
| ChatGPT (search and training) | No |
| Claude (search and training) | No |
| Perplexity | No |
| Bing and Copilot | Rendering is deferred and inconsistent; treat as no |

The test costs one minute. Fetch the raw HTML and search for a sentence that should be on the page:

    curl -sL https://example.com/page/ | grep -c "exact sentence from the page"

Zero matches means AI engines see an empty shell. Cross-check with view-source in a browser (not DevTools Elements, which shows the rendered DOM) and with GSC URL Inspection for what Googlebot renders.

Decision rule: any page that should rank or be cited must serve its content in the initial HTML response. SSR or SSG is mandatory; client-side rendering is acceptable only for logged-in app surfaces.

Stack verdicts:

| Stack | Content in raw HTML | Verdict |
|---|---|---|
| WordPress, Shopify, Webflow | Yes | Hold up at volume (field experience, 115+ audits) |
| Next.js, Nuxt, Astro, SvelteKit with SSR/SSG enabled | Yes | Fine, but verify template by template: hybrid apps regress silently |
| React, Vue, Angular client-side SPA | No | Invisible to every AI engine; prerender or rebuild |
| Framer, Lovable, Base44, Bolt, and similar AI builders | Mixed and moving | Field experience: unstable for SEO at scale (rendering, redirects, sitemap control), and the platforms change their rendering defaults between releases; fetch the HTML before judging, then use the seo-ai-site-builders skill for the conversion |

Inside a stable CMS, the theme still decides the technical floor. Pick a lean, SEO-oriented e-commerce theme (clean markup, no JavaScript bloat, content in raw HTML, fast Core Web Vitals out of the box) over a heavy multi-purpose one: on Shopify, for example, the gap between a performance-focused theme and a bloated one shows up directly in LCP. Choose the domain on the same logic: for a French local business, a .fr signals geography to Google and tends to earn a better local click-through than a .com (field heuristic from 115+ agency audits). Settle the domain before launch, since changing it later means a full migration (Step 7).

### Step 4: Speed and Core Web Vitals

Judge mobile first: mobile carries 80 to 90 percent of traffic on typical lead-gen and e-commerce sites (field range). Measure with the free PageSpeed Insights web interface at https://pagespeed.web.dev: no API key, no account, and it returns both field data (CrUX, what real users experienced over 28 days) and lab data. Field data wins arguments; lab data locates causes.

| Metric | Good (at p75) | Notes |
|---|---|---|
| LCP | Under 2.5 s | Largest Contentful Paint |
| INP | Under 200 ms | Replaced FID in March 2024; roughly 43 percent of sites failed INP at the switch, making it the most commonly failed vital (https://web.dev/articles/inp) |
| CLS | Under 0.1 | Layout stability |
| PageSpeed score | 75+ desktop acceptable, aim higher | Field heuristic; mobile scores run lower, judge the trend |

Keep perspective: Core Web Vitals act as a tiebreaker, not a dominant ranking factor. Do not spend weeks chasing a score of 100 on a site with an indexation or rendering problem; sequence speed after Steps 1 to 3.

High-yield fixes, ordered by how often audits surface them:

1. Images: 200 KB or less each (field heuristic), WebP or AVIF, explicit width and height attributes to reserve layout space (prevents CLS), responsive srcset.
2. Never lazy-load above-the-fold images, least of all the LCP image; mark the LCP image fetchpriority="high".
3. Defer render-blocking third-party scripts; load chat widgets and trackers after interaction.
4. Text-to-HTML ratio under 10 percent signals a thin or bloated page (field heuristic): too little content or too much markup. Related: keep the DOM under roughly 1,500 nodes; Lighthouse flags excessive DOM size starting around 800 (https://developer.chrome.com/docs/lighthouse/performance/dom-size).

### Step 5: Duplicates and international: canonicals and hreflang

Canonicals (the e-commerce deduplication tool):

- Faceted navigation, sort parameters, and session IDs multiply URLs. Point every variant at the clean URL with rel=canonical.
- A canonical is a hint, not a directive: Google ignores canonicals contradicted by stronger signals (internal links and sitemaps pointing at variants). Align all signals on the clean URL.
- Every page self-canonicalizes. It costs nothing and absorbs parameter pollution.
- Quick win, the homepage canonical: many sites set canonicals on every inner page but leave the homepage without one, even though it is the most linked URL and the one that collects the most parameter and tracking variants. Add a self-referencing canonical on the home page; it is a two-minute fix with outsized cleanup value (field heuristic from 115+ agency audits).

hreflang (international versions):

- Every language or region page lists all alternates including itself, plus one x-default pointing at the language selector or default market page.
- Reciprocity is mandatory: if the FR page references the EN page, the EN page must reference the FR page back, or Google discards the pair.
- Prefer hreflang in sitemaps on large sites: one file to audit instead of tags scattered across templates.
- hreflang routes users; it does not consolidate authority. Near-duplicate language variants (en-US versus en-GB) still need distinct value or consolidation.

### Step 6: Security and domain integrity

- HTTPS everywhere: every HTTP URL 301s to HTTPS in one hop, no mixed content, valid certificate.
- Hack detection: search the raw HTML (hacks often cloak, so not just the rendered page) for injected casino, pharma, and replica anchors. Check GSC Security Issues and run a site: search for pages you do not recognize. On WordPress: clean the injection, update core and plugins, install Wordfence, rotate all credentials.
- Unintentional geo-blocking: a firewall rule or a country block (often shipped by a WAF, a CDN security preset, or a hosting default) can make the site unreachable from entire regions, so a slice of human visitors, search bots, and AI crawlers, and your own audit, see nothing. Symptoms: timeouts or 403s from one country but not another, missing impressions from a market that should convert. Test by fetching the site through a different-country exit (a VPN, or curl from a server in the target region) and compare the status code against your local result. Whitelist Googlebot, Bingbot, and the AI crawler ranges (references/ai-crawlers.md), and lift any country block that overlaps a real audience.
- Domain age is an asset: an old domain carries link history and trust. Never let a legacy domain expire; renew it and 301 it. Field rule: domains are cheap, history is not replaceable.

### Step 7: Migrations (when applicable)

Migrations destroy more rankings than algorithm updates do (field observation across 115+ audits). Operating rule: it is easy to break rankings and very hard to build them.

1. Keep the same domain if humanly possible, and change one thing at a time: domain, URL structure, design, or content. Stacking all four into one launch makes any later diagnosis impossible.
2. Freeze a full URL inventory before launch: GSC performance export (16 months), GSC coverage, the sitemap, and a full crawl. The menu is not the site; only the export catches the long tail.
3. Map a 301 for 100 percent of known URLs to the closest equivalent. No chains, no mass redirect to the homepage.
4. Pages that rank but embarrass the new design: hide them from the menu instead of deleting them. They keep earning; deletion burns their history.
5. Keep titles, H1s, and content on top pages as close to identical as the redesign allows (light modifications only).
6. Deindex duplicate mirrors at launch: a Substack copy of the blog, a forgotten staging subdomain, a www and non-www split. One canonical home per piece of content.
7. After launch: recrawl, verify redirects, resubmit sitemaps, use GSC Change of Address for domain moves, then watch coverage daily for two weeks.

### Spot-check commands

Fast verifications during any conversation, before reaching for tools. Each answers one question from the steps above:

    # Status code and redirect chain (flag chains longer than one hop)
    curl -sIL https://example.com/page/ | grep -iE "^HTTP|^location"

    # Indexability: X-Robots-Tag header, then meta robots in raw HTML
    curl -sIL https://example.com/page/ | grep -i "x-robots-tag"
    curl -sL https://example.com/page/ | grep -io '<meta name="robots"[^>]*>'

    # Canonical as served (must match the clean URL)
    curl -sL https://example.com/page/ | grep -io '<link rel="canonical"[^>]*>'

    # robots.txt: sitemap declared, no accidental Disallow: /
    curl -s https://example.com/robots.txt

    # Content present without JavaScript (the AI visibility test from Step 3)
    curl -sL https://example.com/page/ | grep -c "a sentence from the page"

For anything beyond spot checks, run the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py).

## Rules and thresholds

| Check | Target | Basis |
|---|---|---|
| GSC, GA4, Bing Webmaster Tools | Installed, verified, accessible | Field rule; the most common audit failure |
| Indexed to submitted ratio | 75%+ healthy; below 50% investigate first | Field heuristic from 115+ agency audits |
| Request Indexing quota | Reserve the ~10-12 daily inspections for money pages | Field rule |
| 404s with traffic or links | 301 to closest equivalent, never blanket to home | Official guidance plus field rule |
| Sitemap | Declared in robots.txt, segmented by type, honest lastmod, no Google ping (dead since 2023) | Official |
| Sitemap size | Max 50,000 URLs and 50 MB uncompressed per file; above that, child sitemaps under a sitemap index, or Google rejects the whole file | Official |
| IndexNow | Implemented (Bing is a gateway to ChatGPT search) | Sourced (yoast.com/chatgpt-search/) |
| noindex plus Disallow on one URL | Never | Official crawler logic |
| LCP, INP, CLS | Under 2.5 s, under 200 ms, under 0.1 at p75 | Official (web.dev) |
| PageSpeed score | 75+ desktop floor; judge mobile first (80-90% of traffic) | Field heuristic |
| Images | 200 KB max, WebP/AVIF, width and height set, no lazy-load above the fold | Field heuristic plus official CLS guidance |
| Text-to-HTML ratio | 10% or more | Field heuristic (thin-page signal) |
| DOM size | Under ~1,500 nodes | Official (Lighthouse) |
| Content present in raw HTML | 100% of content that must rank or be cited | Measured (Vercel/MERJ study) |
| hreflang | Reciprocal pairs, self-reference, x-default | Official |
| HTTPS | Sitewide, single 301 hop | Official |
| Migration redirects | 100% of exported URLs mapped | Field rule |

## llms.txt: the honest verdict

What the data says:

- Adoption sits around 10 percent of the 300,000 domains SE Ranking studied in 2025.
- Server-log analyses find AI bots requesting the file in a tiny fraction of hits, commonly cited near 0.1 percent.
- No engine confirms reading it: not OpenAI, not Anthropic, not Perplexity, not Google. John Mueller publicly compared it to the meta keywords tag (https://www.seroundtable.com/google-does-not-endorse-llms-txt-40789.html).
- Google states sites do not need special AI text files for its AI features (https://developers.google.com/search/docs/appearance/ai-features).

Recommendation: generating one takes 10 minutes and does not hurt, so create it when asked or when it costs nothing. Never present it, prioritize it, or bill it as a visibility lever, and never let it displace work on rendering, indexation, or content. A vendor selling llms.txt as a GEO strategy is telling you something about the vendor.

## GEO layer: AI crawler access

This skill is the canonical owner of AI crawler knowledge for the whole skill set. The full table (user agents, operators, robots.txt compliance, IP verification URLs) and paste-ready robots.txt blocks live in references/ai-crawlers.md. Read that file whenever a task touches robots.txt or bot access. Summary:

Three bot roles, three different blocking costs:

| Role | Examples | If you block it |
|---|---|---|
| Training crawlers | GPTBot, ClaudeBot, CCBot, Google-Extended, Applebot-Extended, Meta-ExternalAgent | Brand absent from future model weights; no effect on today's citations |
| Search-index crawlers | OAI-SearchBot, Claude-SearchBot, PerplexityBot, Bingbot, Googlebot | You disappear from that engine's live answers and citations |
| User-fetch agents | ChatGPT-User, Perplexity-User, Claude-User, MistralAI-User | Mostly cannot be blocked via robots.txt; they act on a user's explicit request |

Default recommendation for brands, SaaS, lead-gen, e-commerce: allow everything, including training bots. Presence in training data means the model itself knows the brand and can recommend it even when the answer runs without web search. Defensive configuration for publishers whose content is the product: keep the search surfaces (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Bingbot, Googlebot), block training (GPTBot, ClaudeBot, CCBot, Google-Extended). Both configurations are ready to paste in references/ai-crawlers.md.

The Google-Extended trap: Google-Extended is a control token, not a crawler. Blocking it only opts the site out of Gemini training and grounding. It does NOT remove the site from AI Overviews or AI Mode, which are fed by regular Googlebot crawling. The only opt-outs from AI Overviews (nosnippet, max-snippet, noindex) also reduce classic search snippets. Decide with eyes open (https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers).

Two facts from earlier sections weigh double for AI bots: they read raw HTML only (Step 3), and Bing's index reaches ChatGPT (Step 2, IndexNow). Anti-spoofing: user-agent strings are trivially forged, so verify IPs against the published ranges listed in references/ai-crawlers.md before whitelisting anything or trusting log analyses.

For what to write so engines quote it, use the geo-visibility skill. For measuring citations and AI referral traffic, use the geo-tracking skill.

## Output format

Deliver a prioritized action plan, never a data dump. Default structure:

    # Technical SEO audit: {domain} ({date})

    ## Critical (blocks indexing or AI visibility)
    Per finding: evidence (URL plus observed value), why it matters, exact fix, effort (S/M/L)

    ## Important (costs rankings or citations)
    Same fields

    ## Maintenance (hygiene, batch later)
    Same fields

    ## Verified healthy
    One line per check that passed, so the absence of findings is itself evidence

Severity rubric:

| Severity | Definition | Examples |
|---|---|---|
| Critical | Content cannot be crawled, indexed, or seen by AI engines | Disallow: /, client-side-only content, noindex on money pages, active hack |
| Important | Indexed but leaking performance | Failed INP, missing 301s, hreflang conflicts, 3 MB images |
| Maintenance | Works but fragile or wasteful | Unsegmented sitemap, dishonest lastmod, missing IndexNow |

Every claim carries its evidence (the URL tested and the raw value observed), and every number is labeled official, measured, or field heuristic.

## Common mistakes

| Mistake | Consequence | Do instead |
|---|---|---|
| Reading the September 2025 GSC impression drop as a traffic loss | False alarm, wasted remediation | Check clicks; explain the num=100 artifact |
| Blocking Google-Extended to escape AI Overviews | No effect; AI Overviews use Googlebot | nosnippet, max-snippet, or noindex, accepting the search cost |
| noindex plus robots.txt Disallow on the same URL | Page stays indexed; Google never sees the noindex | Allow the crawl, serve noindex, drop the Disallow |
| Weeks of Core Web Vitals work on an unindexed site | Polishing pages nobody is shown | Sequence: indexation, rendering, then speed |
| Lazy-loading the LCP image | LCP degrades by design | Eager-load it with fetchpriority="high" |
| Selling llms.txt as a deliverable | Credibility debt with informed clients | 10-minute add-on, framed honestly |
| Migrating with menu-only redirects | Long-tail URLs 404, history burned | 301 100% of the GSC export |
| Deleting ugly pages that rank | Rankings traded for aesthetics | Hide from the menu, keep the URL live |
| Trusting user-agent strings in logs | Spoofed bots pollute analyses and whitelists | Verify IPs (references/ai-crawlers.md) |
| lastmod bumped sitewide on every deploy | Google learns to ignore the signal | Update lastmod only on real content changes |

## Sources

- Sitemap ping deprecation: https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping
- Bing index as ChatGPT gateway: https://yoast.com/chatgpt-search/
- num=100 removal impact: https://searchengineland.com/google-num100-impact-data-462231
- INP thresholds and rollout: https://web.dev/articles/inp
- AI crawlers and JavaScript, 500M+ fetches: https://vercel.com/blog/the-rise-of-the-ai-crawler
- AI search and JS rendering: https://www.gsqi.com/marketing-blog/ai-search-javascript-rendering/
- Google on AI features and text files: https://developers.google.com/search/docs/appearance/ai-features
- Mueller on llms.txt: https://www.seroundtable.com/google-does-not-endorse-llms-txt-40789.html
- Googlebot and Google-Extended documentation: https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers
- DOM size: https://developer.chrome.com/docs/lighthouse/performance/dom-size
- PageSpeed Insights, free web interface, no API key: https://pagespeed.web.dev
- Field heuristics: 115+ agency audits, labeled as such throughout
