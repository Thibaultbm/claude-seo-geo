---
name: seo-internal-linking
description: Designs and repairs internal linking architecture so authority flows from blog content to the pages that sell and every page stays crawlable. Covers money page mapping, orphan page detection, content silos and hub-and-spoke clusters, anchor text variation, breadcrumbs, menu and footer roles, blog subfolder placement, and keyword cannibalization merges with 301s. Use this skill whenever the user asks to add internal links to an article, build a topic cluster or silo, fix orphan pages, plan or audit site architecture, decide which pages a new post should link to, move a blog off a subdomain, restructure navigation menus, or asks why a page is indexed but never ranks. Also use it for requests like 'interlink these posts', 'internal linking strategy', 'link juice', or 'orphaned URLs in the sitemap'. For earning external backlinks, use the seo-backlinks skill. For making individual pages citable by AI engines, use the geo-visibility skill. For writing the article content itself, use the seo-content-blog skill.
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Internal Linking Architecture

Build the internal link graph that routes authority from blog content to commercial pages, leaves zero pages orphaned, and makes the site hierarchy legible to search engines and, through their indexes, to AI engines.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use

- Planning internal links for a new article or page (which targets, which anchors, where).
- Auditing an existing site for orphan pages, weak structure, or money pages starved of links.
- Building topic clusters: mini-silos for niche sites, hub and spoke for large sites.
- Deciding what belongs in the menu and what belongs in the footer.
- Diagnosing a page that is indexed but gets no impressions or never ranks.
- Resolving keyword cannibalization between two pages (merge and 301 decisions).
- Migrating a blog from a subdomain to a subfolder.

Route adjacent jobs to their own skills:

- External link acquisition and link spots: seo-backlinks.
- Passage-level citability of a page in AI engines: geo-visibility.
- BreadcrumbList and other markup implementation: seo-schema-markup.
- Keyword-to-page mapping and intent analysis: seo-keyword-research.
- Writing the supporting articles themselves: seo-content-blog.

## Workflow

### Step 1. Map the money pages

List every page that sells: products, services, collections, pricing, signup, contact. Rank by business value:

- Direct revenue pages first: service pages, product pages, pricing.
- Assisted conversion pages second: comparison pages, case studies, contact.
- For each, record the current inbound internal links (count and source pages).

Why: internal linking is authority budgeting; you cannot route equity before deciding where it must land. Articles are donors, money pages are receivers.

### Step 2. Detect orphan pages

Compare the full sitemap URL list against a crawl that starts from the homepage and follows links only. Any URL present in the sitemap but unreachable through links is an orphan. For the crawl and link graph collection, run the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py).

Orphan causes to check explicitly:

- Blog redesigns that dropped old posts from the index pages.
- Products or categories removed from navigation but never redirected.
- Landing pages created for ads and never linked from anywhere.
- Pagination changes that cut off deep pages.
- Localized versions referenced only in hreflang tags, never through visible links.

Why zero tolerance: search engines discover and re-crawl through links; a sitemap entry alone gets a page crawled rarely, indexed unreliably, and ranked almost never.

### Step 3. Build the article-to-money-page matrix

For every blog article, assign the 3-5 money pages it should link to, matched on topic:

- Every article supports at least one commercial page.
- Every priority money page receives links from at least 3 articles (field heuristic from 115+ agency audits).
- Place the links inside the body where the topic naturally touches the offer, not parked in a block at the end.

Why: articles capture informational traffic; the matrix is the mechanism that converts that traffic and authority into commercial rankings.

Plan a retroactive re-linking pass. You cannot link from an article to others that do not exist yet, so a corpus built over time accumulates missing cross-links. Schedule a dedicated pass once a batch is published (and re-run it as the corpus grows) to add the article-to-article links that were impossible to place at writing time. This is a recurring maintenance task, not a one-off (field heuristic from 115+ agency audits).

### Step 4. Fix the anchors

Rewrite anchors to be descriptive, varied, and natural: a mix of exact keyword, partial match, and descriptive phrases (distribution table below). Eliminate sitewide repetition of one exact-match anchor and systematic "click here".

### Step 5. Build mini-silos per service

At the bottom of each service or category page, link 2-3 topically related articles; each of those articles links back to the service page and to its siblings. Scale to hub and spoke on large sites (structures below).

Example for a plumbing company:

- Service page: /services/boiler-installation
- Linked at its bottom: the cost guide article, the combi vs system boiler comparison, the installation day walkthrough.
- Each of those three articles links back to /services/boiler-installation with a descriptive anchor, and to its two siblings.

### Step 6. Set the navigation

- Menu: only the most important pages.
- Footer: secondary and legal pages, plus the blog link if the menu is full.
- Breadcrumbs on every page, backed by BreadcrumbList markup (implementation: seo-schema-markup).

### Step 7. Verify

Re-crawl and confirm: zero orphans, every priority money page has at least 3 inbound internal links from articles, anchors varied, links visibly styled, breadcrumbs sitewide, priority pages within 3 clicks of the homepage.

## Rules and thresholds

| Rule | Standard | Why |
|---|---|---|
| Links per article | 3-5 internal links toward money pages (field heuristic from 115+ agency audits) | Articles capture informational traffic; links pass that authority to the pages that convert. An article linking only to other articles keeps equity circling in an informational loop that never sells |
| Link visibility | Underlined plus a distinct color | A link styled like body text is clicked by no one and is weaker as a navigation signal; internal click-through is a usage signal. If users cannot see it, it does not work |
| Orphan pages | Zero tolerated | A page with no inbound internal link is rarely crawled, often not indexed, and invisible everywhere, including to AI engines that retrieve through search indexes |
| Blog location | /blog subfolder, never a subdomain; linked from menu or footer | Authority consolidates on one domain. Google states subdomains and subfolders both work; the subfolder rule is a field heuristic from migration outcomes, where consolidation onto the main domain preceded recoveries |
| Anchor variation | Mix exact, partial, descriptive, and branded anchors; never the same exact-match anchor repeated sitewide | Dozens of identical exact-match anchors look manipulative and fall under link spam patterns; varied anchors describe the target naturally |
| Generic anchors | "Click here" and "read more" never as the dominant pattern | Anchor text is the description of the target page that crawlers and screen readers consume; a generic anchor wastes the signal entirely |
| Cannibalization | 1 keyword = 1 page | Two pages on the same intent split clicks, links, and ranking signals, and Google alternates between them. Test and merge procedure below |
| Breadcrumbs | On every page, with BreadcrumbList markup | A crawlable hierarchy on every page; feeds entity and section understanding for search and AI engines. Markup details: seo-schema-markup |
| Table of contents | On every long article | Anchor links are internal links too: they expose section structure to crawlers and AI extractors and can produce jump links in results |
| Menu | The most important pages only | Sitewide links carry the most internal weight; every addition dilutes every existing entry. The menu is a budget, not a sitemap |
| Footer | Secondary and legal pages | Keeps sitewide equity flowing to support pages without bloating the menu |
| Click depth | Priority pages within 3 clicks of the homepage (field heuristic) | Depth is the site's own statement of importance; pages buried 5+ clicks deep are crawled less often and ranked as minor |

### Anchor text mix

Target distribution for the inbound anchors of any single page (field heuristic from 115+ agency audits):

| Anchor type | Share | Example for /services/boiler-installation |
|---|---|---|
| Descriptive phrase | Most of the mix | "what a professional boiler installation includes" |
| Partial match | Common | "boiler installation cost", "installing a new boiler" |
| Exact match | Small minority | "boiler installation" |
| Branded or page name | Some | "our installation service" |
| Generic | Near zero | "click here", "read more" |

Why variation matters: anchor text is the engine's description of the target page. Identical exact-match anchors repeated at scale match the link scheme patterns in Google's spam policies, and they carry less information than varied natural descriptions.

### Link placement

| Placement | Weight | Use for |
|---|---|---|
| In-content, inside the main body | Highest | Article-to-money-page links |
| Bottom-of-page related block | Medium | Mini-silo article lists |
| Menu | Sitewide, highest aggregate | Top money pages |
| Footer | Sitewide but discounted | Secondary and legal pages |
| Sidebar | Low | Do not rely on it |

Why: Google's reasonable surfer model weights links by their probability of being clicked; a contextual link inside the content a user is reading outweighs a template link repeated on every page.

### Silo structures

| Site size | Structure | Implementation |
|---|---|---|
| Niche site (under ~50 pages) | Mini-silo | 2-3 related articles linked at the bottom of each service page; each article links back to the service page and to its siblings. This is sufficient; do not over-engineer |
| Large site | Hub and spoke | One pillar page per topic; satellite articles link UP to the pillar and across to sibling satellites; the pillar links down to all satellites |

Hub and spoke example for a SaaS:

- Pillar: /guides/email-deliverability (the page meant to rank for "email deliverability").
- Satellites: the SPF/DKIM/DMARC setup post, the inbox warmup post, the spam trigger words post.
- Each satellite links up to the pillar with a varied descriptive anchor and across to 1-2 siblings.
- The pillar links down to every satellite from the section where it fits.

Direction matters: the page you want to rank (the hub or the service page) must RECEIVE the links. A pillar that only links out to satellites without receiving links back concentrates nothing. Keep outbound links disciplined too: link each target once per page, at the most natural spot; dozens of internal links from a single page dilute every one of them.

### Satellite site (standalone comparator)

Distinct from the satellite ARTICLES of an in-site silo above: this is a second, independent website on the same theme, positioned as the reference of the niche (a Wikipedia-plus-comparator hybrid). It lists the actors and subjects of the sector, captures educational and comparison traffic, and links out to the commercial site as the cited example. Treat it as a separate property with its own internal silo, then a controlled set of editorial links pointing to the money site.

- When it earns its keep: competitive niches where the brand site cannot credibly rank as a neutral authority, and where buyers search educational and "best X" comparison queries before they search the brand (field heuristic from 115+ agency audits).
- Build: neutral domain, sector glossary and actor profiles as the hub, comparison and "best [category]" pages as the converting layer, then descriptive editorial links to the relevant money pages on the brand site (one per natural context, never a sitewide block).
- Two sites on the same theme do NOT cannibalize each other: they are separate properties, so they occupy two distinct slots in the SERP instead of splitting one page's signals. Cannibalization is a within-site problem (two pages of the same site on the same intent), not a cross-domain one. Anti-cannibalization keyword logic: seo-keyword-research.
- This is also an off-page lever: a controlled, topically perfect referring domain into the brand site. Plan its links as part of the link profile in seo-backlinks (anchor variation and velocity rules apply there too).

### Cannibalization test and merge

Signals that two pages cannibalize:

- Both URLs alternate for the same query in Search Console.
- Impressions split between them and neither climbs.
- Searching either keyword variant returns substantially the same SERP.

Procedure:

1. Search both keyword variants in Google (for example "property management fees" vs "how much do property managers charge").
2. If the two SERPs show substantially the same results, the intent is identical: one page must absorb the other.
3. Keep the URL with the most backlinks, age, and impressions; merge the unique content from the loser into it; 301 the loser to the keeper.
4. Never delete without a 301: deletion discards the old URL's equity and its accumulated age (pages cited by ChatGPT have a median age around 500 days per Ahrefs, so an aged URL is also a GEO asset).
5. Full keyword-to-page mapping method: seo-keyword-research.

Caution: merge only on identical intent. Two pages with similar words but different intents (one informational guide, one commercial service page) are not cannibalizing; they should coexist and link to each other.

### Quick diagnostic: indexed but invisible

When a page is indexed yet gets no impressions or clicks, check in this order:

1. Inbound internal links: orphan or near-orphan status is the most common cause found in audits.
2. Click depth: count the clicks from the homepage; 5+ means the site itself marks the page as minor.
3. Anchor quality: generic anchors ("click here") tell engines nothing about the page.
4. Cannibalization: another page on the same intent absorbing the signals.
5. Only after these four: content quality (seo-content-blog) and external authority (seo-backlinks).

Why this order: architecture problems are cheaper to fix than content problems and are the usual culprit when an indexed page underperforms sitewide patterns.

## GEO layer

- AI crawlers (GPTBot, ClaudeBot, PerplexityBot) fetch pages independently: internal links do not propagate authority inside their systems the way PageRank does in Google.
- BUT internal linking drives AI visibility indirectly and decisively: ChatGPT and Perplexity retrieve through search indexes (Bing, Google), and your internal links control what enters those indexes and how it ranks there. An orphan page sits in no index, so it is cited nowhere, in Google AI Overviews included.
- Hub pages benefit twice: hub and spoke concentrates ranking signals on the pillar, which makes it the page engines retrieve and quote for broad queries on the topic.
- Breadcrumbs with BreadcrumbList markup feed entity understanding: AI engines learn which brand and which section a page belongs to before quoting it.
- Descriptive anchors give engines context about the target page before they ever fetch it.
- Passage-level citability rules: geo-visibility. AI crawler access and robots.txt: seo-technical. Measuring AI citations and traffic: geo-tracking.

## Output format

Deliver every internal linking engagement as this plan:

```markdown
# Internal linking plan: <domain>

## 1. Money pages (ranked by business value)
| Priority | Page | URL | Inbound internal links today | Target |
|---|---|---|---|---|
| 1 | <name> | <URL> | <n> | 3+ from articles |

## 2. Orphan pages (sitemap vs crawl)
| URL | In sitemap | Inbound links | Fix |
|---|---|---|---|
| <URL> | yes | 0 | Link from <page> with anchor "<anchor>" |

## 3. Article-to-money-page matrix
| Article | Money page target(s) | Anchor | Placement in article |
|---|---|---|---|
| <article URL> | <money page URL> | <descriptive anchor> | <section> |

## 4. Mini-silos / clusters
### <Service or topic A>
- Hub page: <URL>
- Supporting articles: <2-3 URLs, linked at the bottom of the hub, each linking back and to siblings>

## 5. Navigation changes
- Menu: <pages to keep, add, remove, with reasons>
- Footer: <secondary and legal pages>
- Breadcrumbs: <pages missing them; BreadcrumbList via seo-schema-markup>

## 6. Cannibalization merges
| Keep | Merge and 301 | Evidence (SERP overlap) |
|---|---|---|
| <URL> | <URL> | <both rank for "<keyword>", same results> |

## 7. Link styling
- Confirm links are underlined with a distinct color sitewide.
```

Every recommendation must name the exact source page, target page, and anchor text. "Add more internal links" without targets is not a deliverable.

## Common mistakes

- **Articles linking only to articles.** The informational loop never reaches a money page; traffic grows, revenue does not.
- **Links styled like body text.** No clicks, no usage signal, and users never discover the commercial pages.
- **Pages reachable only via the sitemap.** A sitemap is a hint, not a substitute for links; the page decays unindexed.
- **Blog on blog.domain.com.** Splits authority across two hosts; consolidate to /blog with page-level 301s when migrating.
- **One exact-match anchor repeated 50 times.** Over-optimization pattern; vary anchors or risk link spam classification.
- **"Click here" everywhere.** Wastes the anchor signal on every occurrence.
- **Every page in the menu.** Sitewide dilution; the menu stops marking importance when everything is important.
- **Hubs that only link down.** The pillar or service page must receive links from its satellites, not just distribute them.
- **Breadcrumbs as decoration.** Visible trail without BreadcrumbList markup misses the structured hierarchy signal.
- **Deleting a cannibalized page without a 301.** Loses its backlinks, history, and aged-URL advantage in AI citations.
- **Fixing orphans by dumping links in the footer.** A footer link from every page is a weak, sitewide-diluted fix; link from topically related content instead.
- **Linking every keyword occurrence on a page.** Dozens of outbound internal links per page dilute each one and read as navigation spam; link once per target per page, at the most natural spot.
- **Orphaning old posts during a redesign.** New blog index, old pagination gone, archive posts stranded; re-crawl after every redesign.

## Sources

- Google Search Central, how Google discovers and crawls through links: https://developers.google.com/search/docs/fundamentals/how-search-works
- Google, link best practices and crawlable links: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google spam policies (link spam): https://developers.google.com/search/docs/essentials/spam-policies
- Google, breadcrumb structured data: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- Google SEO starter guide, site organization: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google patent US 8,051,071 (reasonable surfer, link weighting by click probability): https://patents.google.com/patent/US8051071B1/en
- Ahrefs, median age of pages cited by ChatGPT (~500 days): https://ahrefs.com/blog/why-chatgpt-cites-pages/
- Link counts per article, subfolder preference, anchor distribution, silo sizing, click depth, menu rules: field heuristics from 115+ agency audits, not Google statements. Google's public position is that subdomains and subfolders are both acceptable.
