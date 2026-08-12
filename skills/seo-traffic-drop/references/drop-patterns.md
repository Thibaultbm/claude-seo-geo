# Drop pattern catalog: signature, causes, confirming test

Load this when the shape is known (skill Step 3) and the short table in Step 4 did not settle it. Each pattern gives the signature in the data, the causes that produce it, the test that confirms or kills each one, and who fixes it.

Use it as a checklist to rule things out, not a menu to pick from. The value of this file is the causes it lets you eliminate with evidence.

## How to read a signature

Four metrics, and the combination names the mechanism:

| Clicks | Impressions | Position | Mechanism |
|---|---|---|---|
| Down | Down hard | Any | Visibility: pages not shown |
| Down | Down | Worse | Ranking: outranked |
| Down | Flat | Flat | Click-through: shown, not clicked |
| Down | Down | Flat or better | Demand: fewer searches, or long tail gone |
| Flat | Down | Any | Reporting artifact, or lost long-tail impressions |
| Down | Up | Worse | Dilution: more queries matched, worse for each |

## Pattern 1: total collapse, one day

Signature: impressions and clicks approach zero across the whole property within a day or two. Rows disappear from the export wholesale.

Causes and tests:

| Cause | Confirming test |
|---|---|
| noindex shipped sitewide | Fetch the raw HTML of three URLs and check meta robots; check the X-Robots-Tag response header, which templates rarely show and CDNs sometimes add |
| robots.txt Disallow: / | Fetch robots.txt directly; check whether a staging config shipped |
| Domain or certificate expired | Fetch the domain and read the TLS error; check the registrar expiry date |
| DNS misconfiguration | Resolve the domain from an external network; compare against the expected records |
| Server or origin outage | Server logs for 5xx; Search Console Crawl Stats for a spike in failures |
| WAF, CDN or bot rule blocking Googlebot | Fetch with a Googlebot user agent and compare the status against a browser user agent; verify by IP, not user agent string |
| Manual action | Search Console Manual Actions, which is binary |
| Hack or injected content | Search the raw HTML for injected anchors; Search Console Security Issues; a site: query for unknown pages |

Owner after confirmation: seo-technical. If the site is built by an AI generator and the collapse followed a hosting change, check rendering first with seo-ai-site-builders.

## Pattern 2: one section or one template

Signature: the section aggregation shows one directory carrying the loss while the rest holds. Often a cliff.

Causes and tests:

| Cause | Confirming test |
|---|---|
| Canonical on the template now points elsewhere | Fetch three pages in the section and read the canonical as served, not as authored |
| noindex on a template variant | Compare meta robots across a losing and a holding page |
| Internal links to the section removed in a redesign | Crawl and count inbound internal links per URL, before and after if an archived crawl exists |
| Section switched to client-side rendering | Run the rendering check from seo-ai-site-builders on a losing URL |
| Pagination or faceting changed, deep pages orphaned | Check whether page 2 and beyond are reachable by real anchors |
| A content type targeted by an update | Check whether the losing section shares a content type with the losses of other sites in the same window |
| Redirects applied to the section during a migration | Verify each old URL resolves in one hop to a relevant page, not to a hub or the homepage |

Owner: seo-technical for rendering and canonicals, seo-internal-linking for link and orphan issues, seo-page-sections when the template lost content blocks.

## Pattern 3: sitewide slope during an update window

Signature: gradual decline over one to three weeks, positions worse across many pages, no single date carries it, and the window overlaps a confirmed update.

Confirm before attributing:

1. The drop starts inside the published window, not before it. A drop that began three days early has another cause, and the update is a coincidence.
2. The loss is not concentrated in one section. If it is, read Pattern 2 first; updates rarely respect a directory boundary that neatly.
3. Competitors in the same SERPs moved too. If your positions fell and nobody gained, the SERP itself changed shape rather than the ranking order.
4. Nothing shipped in the same window. Release logs beat correlation every time.

If all four hold, the update attribution is defensible. Then the honest expectation, from Google's own core update guidance: there is nothing to fix in the sense of a penalty, and broad recoveries typically arrive with later updates rather than from a single change. Work on the content quality gap the update exposed, and do not promise a date.

Owner: the content skills, plus seo-page-sections for structural gaps against what now ranks.

## Pattern 4: click-through loss

Signature: impressions and position hold, clicks fall. Frequently sitewide, frequently gradual.

Causes and tests:

| Cause | Confirming test |
|---|---|
| AI Overviews now trigger on the losing queries | Inspect the live SERP for the top 20 losing queries and count AI Overview presence; segment branded against non-branded, since branded queries with an AI Overview tend to gain CTR rather than lose it |
| A new SERP feature took the space | Compare the SERP layout against an archived screenshot or a rank tracker's SERP history |
| Google rewrote the titles | Compare the title in Search Console's appearance against the authored title tag |
| Titles and descriptions stopped matching intent | Read the top losing queries against the title actually served |
| A competitor's snippet is more compelling | Look at the SERP as a user; this one is qualitative and still real |
| Brand damage or a reputation event | Check branded query CTR specifically, and search the brand name |

Owner: the content skills for titles and intent, geo-visibility when AI Overviews are confirmed. Note that more content does not fix a CTR problem, and that a page still ranking is evidence against a quality diagnosis.

## Pattern 5: a handful of URLs, with gainers

Signature: concentrated loss, and the gainers table shows related pages of yours rising.

Causes and tests:

| Cause | Confirming test |
|---|---|
| Cannibalization from a page published recently | Query-level export: check whether the queries the losing URL held now map to the new URL |
| Internal link changes redirected authority | Compare inbound internal link counts between the two pages |
| Content merged or rewritten | Check the publication and modification history of both pages |
| A deliberate consolidation nobody logged | Ask; this is common and is not a problem if intended |

Owner: seo-internal-linking for the merge and consolidation decision, seo-keyword-research for the intent mapping.

## Pattern 6: one country or one device

Signature: the loss disappears when the export is filtered to other countries or devices.

Causes and tests:

| Cause | Confirming test |
|---|---|
| Geo-blocking by a WAF, CDN preset or hosting default | Fetch the site through an exit in that country and compare the status code against a local fetch |
| hreflang regression | Check reciprocity and x-default across the affected language pair |
| Mobile rendering or interstitial regression | Fetch and render the page as mobile; check for a full-screen interstitial |
| Mobile speed regression | Compare Core Web Vitals per device in the field data |
| A local competitor or market event | Qualitative, but check the SERP from that country |

Owner: seo-technical.

## Pattern 7: the drop that is not in Search Console

Signature: the client reports a loss that GSC does not show.

| Where the loss actually is | How to see it |
|---|---|
| Analytics only (tagging, consent, bot filtering) | Compare GSC clicks against GA4 organic sessions day by day |
| AI referral traffic (chatgpt.com, perplexity.ai and similar) | The AI channel setup in geo-tracking |
| AI citations, with rankings intact | A prompt panel run against the previous month's panel, in geo-tracking |
| Direct or branded traffic | Branded query trend in GSC, plus Google Trends on the brand |
| Conversions, not traffic | Landing page revenue by page group; the traffic may be intact and worse qualified |
| A channel that was never organic | Check the actual source before accepting the premise |

The last row matters more than it looks. A meaningful share of reported organic drops are not organic drops, and confirming which channel moved is the cheapest step in the whole investigation.
