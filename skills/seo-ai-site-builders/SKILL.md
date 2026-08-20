---
name: seo-ai-site-builders
description: "Turn a JavaScript-only site built by an AI website generator into indexable HTML. Input: a site made with Lovable, Base44, Bolt, v0, Replit, Firebase Studio, Framer, Wix, Durable, Softr, Bubble, Glide or any similar tool. Output: proof of what crawlers actually receive (bundled zero-dependency script), the right conversion route (native SSR, build-time prerendering or SSG, framework migration, or crawler-only prerendering as a last resort), the HTML each page must serve, and the routing, status code and hosting config that goes with it. Use when a vibe-coded or AI-generated site is not indexed, shows an empty page in view-source, has meta tags that only appear after JavaScript runs, is invisible to ChatGPT and Perplexity, or when picking a builder before starting."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# AI-generated sites: rewrite the JavaScript into HTML

AI website generators produce a working site in minutes and, by default, most of them produce a client-rendered single page app: the server returns an almost empty HTML document plus a JavaScript bundle, and the browser builds the page afterwards. That is fine for a logged-in app and disqualifying for anything meant to be found.

The fix is never an SEO plugin or a meta tag component. It is changing what the server returns. This skill establishes what crawlers currently receive, picks the cheapest route to real HTML, and specifies the HTML those pages must serve.

One warning that shapes the whole workflow: the platforms move fast and their status changes. Lovable shipped server-side rendering for new apps in May 2026, Base44 started serving prerendered snapshots to crawlers in mid-2026. Never answer from a platform's reputation or from a blog post; fetch the URL and read the response. Step 1 exists for that reason.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, the stack already in use, past migration decisions, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use this skill

Use it for:

- A site built with Lovable, Base44, Bolt, v0, Replit, Firebase Studio, Rocket, Create, Mocha, Emergent, Dyad, Hostinger Horizons, Figma Make, Softr, Bubble, Glide, Durable, Dora, Wix, Framer or any similar generator
- "My site is live but Google only indexed the homepage"
- view-source shows an empty div and nothing else
- Page titles and descriptions that are correct in the browser tab and absent from the HTML
- Link previews (WhatsApp, Slack, LinkedIn, X) that render blank for every URL but the homepage
- ChatGPT, Claude or Perplexity answering "I cannot access that page" or describing the wrong content
- Choosing which builder to start with when the site has to rank

Hand off neighboring problems:

- Full technical audit, robots.txt, sitemaps, Core Web Vitals, the canonical AI crawler table: the seo-technical skill
- Which blocks a page is missing once it does serve HTML: the seo-page-sections skill
- JSON-LD templates: the seo-schema-markup skill
- Writing passages engines will quote: the geo-visibility skill
- Measuring the recovery in AI traffic and citations: the geo-tracking skill

## The fact that decides everything

Googlebot renders JavaScript, on a deferred second pass. No AI crawler does. The Vercel and MERJ analysis of 500M+ crawler fetches found GPTBot, ClaudeBot and PerplexityBot download JavaScript files and execute none of them (https://vercel.com/blog/the-rise-of-the-ai-crawler).

So a client-rendered page is not "slightly weaker in search". It is:

| Surface | What it sees |
|---|---|
| Googlebot, AI Overviews, AI Mode, Gemini grounding | The rendered page, after a render queue delay |
| ChatGPT (search and training) | The empty shell, permanently |
| Claude, Perplexity | The empty shell, permanently |
| Bing and Copilot | Deferred and inconsistent rendering, treat as the empty shell |
| Social and chat link previews | The shell, so previews break |

A site can therefore rank acceptably on Google and be structurally absent from every AI answer. That gap is the reason this work is worth doing in 2026 and was not in 2019.

## Workflow

### Step 0: Establish builder, hosting and code ownership

Three questions, in this order. The second one matters more than users expect.

1. Which generator produced the site. Fingerprints are in the bundled script and in references/builder-matrix.md.
2. Where it is served from: the platform subdomain (project.lovable.app, project.base44.app), the platform with a custom domain attached, or an exported repository hosted elsewhere (Vercel, Netlify, Cloudflare Pages, a VPS, a bucket).
3. Whether the code is exportable and exported (GitHub connection, ZIP download), and who can deploy it.

Why question 2 decides the plan: platform-side rendering is a property of the host, not of the code. A Lovable or Base44 project that gets server-rendered HTML while hosted on the platform becomes a bare client-side app again the moment the same repository is exported and dropped on a static host. Teams that "took control of their stack" by moving to a static bucket routinely lose indexing this way and blame the migration for something the hosting change caused.

### Step 1: Prove what crawlers receive

Never trust a dashboard, an SEO tab, or a "we support SEO" claim. Fetch the URL.

    python3 scripts/render_check.py https://example.com/ https://example.com/pricing --soft404

The script fetches raw HTML with no JavaScript execution and reports, per URL: builder and framework fingerprints, word count in the HTML, title, h1, meta description, canonical, meta robots, crawlable internal links, images, JSON-LD validity, and a verdict of SERVER RENDERED, PARTIAL, SHELL ONLY or ERROR. It exits non-zero if any page fails. Useful flags: `--sitemap URL --limit N` to sample a real site, `--ua-compare` to detect a crawler-only prerender layer, `--json` for a report.

The manual equivalent, when a script cannot run:

    # Is a sentence from the page present in the HTML
    curl -sL https://example.com/page/ | grep -c "a sentence you can see on the page"

    # What the document actually contains
    curl -sL https://example.com/page/ | head -50

    # As an AI crawler
    curl -sL -A "Mozilla/5.0 (compatible; GPTBot/1.2; +https://openai.com/gptbot)" https://example.com/page/ | wc -w

Test five URLs, not one. The homepage is the page platforms prerender first and the one every vendor demo uses. Sample: homepage, a service or product page, a blog post, a dynamic detail route (an item fetched by id or slug), and a filtered or paginated list. Mixed verdicts across that sample are the normal result and they change the recommendation: partial coverage means the prerender layer skips dynamic routes, which is exactly where the long tail lives.

Verdict thresholds used throughout this skill:

| Verdict | Meaning | Threshold |
|---|---|---|
| SERVER RENDERED | The page is readable by every crawler | 250+ words in the HTML and an h1 present (field heuristic) |
| PARTIAL | Shell plus some prerendered fragments, or a thin real page | Between 60 and 250 words, or no h1 |
| SHELL ONLY | Invisible to every AI engine | Under 60 words, or an empty root div |

Record the numbers. They are the before column of the deliverable and the only honest proof the work changed anything.

### Step 2: Read the platform status, then re-verify it

Per-platform detail, native SEO controls and gotchas: references/builder-matrix.md. The short version, as of August 2026:

| Builder | Default rendering | Practical status |
|---|---|---|
| Lovable | SSR for apps created from 13 May 2026 (TanStack Start); older React and Vite apps get automatic prerendering while hosted on Lovable | Usually fixable in place; verify per route, and re-verify after any export |
| Base44 | Client-rendered React; the platform serves crawlers a prerendered snapshot since mid-2026 | Crawler-only rendering, so verify the snapshot covers dynamic routes and stays fresh |
| Bolt (StackBlitz) | Vite single page app unless the prompt asks for a framework | Fixable: rebuild or migrate, the code is yours |
| v0 (Vercel) | Next.js with server rendering | Usually fine by default, verify anyway |
| Replit, Firebase Studio, Rocket, Create, Mocha, Emergent, Dyad, Hostinger Horizons, Figma Make | Depends entirely on the generated stack, most default to a Vite single page app | Check the repo for a framework, then Route B or C |
| Bubble, Softr, Glide | Client-rendered by design, no code export | Route D, or build marketing pages on a different stack |
| Wix, Squarespace, Webflow, Framer, Shopify, WordPress | Server-rendered HTML | Rendering is not the problem, run a normal technical audit instead |

Two rules attach to that table:

- A platform-side fix disappears with the platform. Treat "SSR on Lovable hosting" and "snapshots on Base44 hosting" as hosting features. Write that down before anyone plans an export.
- Prerendering that is served only to crawlers is dynamic rendering, whatever the vendor calls it. It works, and Google classes it as a workaround rather than a long-term solution (https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering). Accept it as a stage, not a destination.

### Step 3: Choose the route

| Route | What it is | Choose it when | Cost |
|---|---|---|---|
| A. Native rendering | Turn on the platform's own SSR or prerendering, or upgrade the project to its server-rendered template | The site stays on the platform and Step 1 shows the feature exists and works | Hours |
| B. Prerender at build time | Keep the same repository, emit one static HTML file per route at build time (SSG) | The code is exportable, routes are known at build time, content is mostly static | 1 to 3 days |
| C. Migrate the framework | Move to a server-rendering framework (TanStack Start, Next.js, Astro, React Router v7 framework mode) | Content is database-driven, routes are dynamic, or the site is a real publishing operation | 1 to 3 weeks |
| D. Crawler-only prerendering | A service or edge worker renders the page and serves that HTML to bots | No code access (Bubble, Softr, Glide), or an urgent stopgap while B or C is built | Hours, plus a recurring bill and a permanent verification duty |

Decision shortcuts:

- Marketing site, portfolio, local business, brochure with a blog: Route B. Nothing on those pages needs a server at request time.
- Product-led app where marketing pages and the app live in one repo: split them. Prerender or migrate the public routes, leave the logged-in app client-rendered. Nobody indexes a dashboard.
- E-commerce, listings, anything with thousands of database-driven URLs: Route C. Build-time prerendering of 10,000 routes that change hourly is a build queue problem in disguise.
- No code export possible: Route D, and price the honest alternative of rebuilding the public pages elsewhere. On Bubble, Softr and Glide the public marketing site is usually 5 to 15 pages, which is a weekend on Astro against a permanent prerendering subscription.

Anti-pattern to name explicitly: shipping Route D while telling the client the site is now server-rendered. Two versions of the truth exist from that day on, and prerender caches fail silently after a deploy. If Route D is chosen, the monitoring in Step 6 is part of the deliverable, not an option.

Concrete configurations for each route, with the code: references/prerender-recipes.md.

### Step 4: Specify the HTML each page must serve

Whatever route runs, the target is the same. Every indexable URL returns, in the initial HTML response, before any JavaScript:

| Element | Requirement |
|---|---|
| title | Unique per URL, in the document, not set later by a client-side head manager |
| meta description | Unique per URL, in the document |
| canonical | Self-referencing, absolute, on the production host |
| h1 | Exactly one, matching the page subject |
| Body copy | The real content. 300+ words on any page meant to rank or be quoted (field heuristic) |
| Internal links | Real `<a href="/path">` anchors. A div with an onClick router push is not a link and passes nothing |
| Images | `<img src>` with alt, width and height. CSS background images injected by JavaScript are invisible content |
| JSON-LD | In the HTML. Client-injected structured data is not read by any AI crawler and is unreliable for Google |
| og:title, og:description, og:image | Per URL. This is what fixes broken link previews, which is often the symptom that got the site here |

Client-side patterns that survive a prerender and still lose the content, with their replacement:

| Pattern | Why it fails | Replacement |
|---|---|---|
| Content mounted only after a click (tabs, accordions, "read more") | Not in the DOM when the page is captured | Render every panel in the HTML, hide with CSS |
| Infinite scroll or "load more" lists | Only page one exists in HTML | Paginated routes with crawlable links, each prerendered |
| Text baked into images or canvas | Not text | HTML text |
| Copy fetched from a headless source at runtime | Arrives after capture | Fetch at build time, or server render |
| Route-level redirects done in a useEffect | Crawlers see the pre-redirect page, or nothing | HTTP 301 or 302 at the server or host level |
| Cookie or geolocation gates that block first paint | Crawler gets the gate, not the page | Serve content, apply the gate to the interactive layer |

### Step 5: Routing, status codes and hosting

Rendering fixes the body. These fix everything around it, and each one has cost real sites their indexation.

- Real 404 status. The classic single page app host rewrite (`/* -> /index.html 200`) answers 200 for every URL that does not exist, so typos, dead links and deleted pages all become soft 404s that dilute the site. Serve a real 404 for unknown routes. The bundled script's `--soft404` flag detects this in one call.
- Path routing, never hash routing. URLs of the form `example.com/#/pricing` are one URL to a crawler. Move to the History API before anything else, since prerendering hash routes is not possible.
- One canonical host. Pick www or apex, 301 the other in one hop, and keep the platform preview subdomain out of the index: the .lovable.app, .base44.app, .vercel.app or .netlify.app copy competes with the production domain for the same content. Serve noindex on the preview host, or canonical it to production.
- Check for a leftover noindex. Preview and staging environments on these platforms often ship `X-Robots-Tag: noindex` or a meta robots noindex, and it survives the move to the custom domain more often than it should. It is the single most common cause of "we did everything and nothing got indexed".
- Sitemap generated from the same route manifest that drives prerendering. A hand-written sitemap and a generated route list diverge within two deploys. Reference the sitemap in robots.txt, then submit it in Search Console.
- Do not disallow /assets/ or the JS and CSS paths in robots.txt. Googlebot needs them to render, and a blocked stylesheet degrades what it sees.
- Trailing slash consistency. Prerenderers emit `/about/index.html`, hosts differ on whether that answers at `/about` or `/about/`. Pick one, 301 the other, canonical to the winner.

### Step 6: Verify, then keep verifying

Immediately after deploying the fix:

1. Re-run the script on the same five URLs and put the before and after word counts side by side. That table is the deliverable's proof.
2. Search Console URL Inspection on two of them, and read the crawled HTML, not the screenshot.
3. Fetch one URL with a GPTBot user agent and confirm the content is there.
4. Confirm unknown routes return 404 and the preview subdomain is out of the index.
5. Resubmit the sitemap and note the indexed to submitted ratio in Search Console so the recovery is measurable.

Then schedule a recurring check, monthly at minimum, and mandatory after every deploy that touches routing or the build. Prerendering and SSR fail quietly: a build config change, a new dynamic route, an expired prerender cache or a platform migration reverts the site to shells without any visible symptom in the browser. Route D setups need this most, since nothing a human sees ever changes.

Recovery timing to set expectations honestly: Google must recrawl before anything moves, so allow weeks rather than days on a site of any size. AI engines are slower still, because a page has to be recrawled, then reselected as a source. Nothing in this work produces a same-week result, and promising one is how these projects lose credibility.

## Rules and thresholds

| Check | Target | Basis |
|---|---|---|
| Content present in the raw HTML | 100% of pages meant to rank or be quoted | Measured (Vercel and MERJ, 500M+ fetches) |
| Words in the HTML on a money page | 250+ for a SERVER RENDERED verdict, 300+ recommended | Field heuristic |
| URLs sampled before recommending anything | 5, covering static, dynamic and paginated routes | Field rule |
| title, meta description, canonical, h1, og tags | In the initial HTML, unique per URL | Official (crawler behavior) |
| Internal links | Real a href anchors, 3+ crawlable per page | Field heuristic |
| JSON-LD | Server-rendered, valid JSON | Official plus field rule |
| Unknown routes | Real 404 status, never a 200 shell | Official (soft 404 handling) |
| Hash routing | Zero indexable hash routes | Official |
| Platform preview subdomain | noindex or canonical to production | Field rule |
| Crawler-only prerendering | Stopgap only, monitored monthly | Official (Google calls dynamic rendering a workaround) |
| Verification after a deploy touching routing or build | Mandatory re-check | Field rule |

## GEO layer

Everything above is doubly true for AI answer engines, and one thing is specific to them.

An engine that cannot fetch content does not fall back to guessing politely: it either omits the brand or reconstructs it from third-party pages (directories, marketplaces, review sites, Reddit threads). So a shell site does not produce silence, it produces answers about the brand written entirely by other people. That is why the recovery in AI citations after this work often outpaces the recovery in Google rankings: the pages become quotable for the first time, in a space where competitors published quotable HTML years ago.

Sequencing that follows: get the HTML served, then apply the geo-visibility skill to make the passages quotable, then the geo-tracking skill to measure. Doing GEO content work on a client-rendered site is writing for an audience of nobody.

Rendering also decides what the model learns about the brand outside of search. Training crawlers read the same empty shell, so a site that spent two years client-rendered contributed nothing to model weights in that period. Fixing the rendering starts that clock; it does not rewind it.

## Output format

Deliver a decision, not a lecture on rendering.

    # Rendering audit: {domain} ({date})

    ## What crawlers see today
    Table: URL, verdict, words in HTML, title present, h1 present.
    One line naming the builder, the host, and whether code export exists.

    ## Consequence
    Which engines can read the site today and which cannot, in one short paragraph.

    ## Recommended route
    Route A, B, C or D with the reason it beats the others here, the effort estimate,
    and what it costs to run.

    ## Changes to make
    Ordered list, each with the file or setting it touches and the expected result.
    Rendering first, then routing and status codes, then the per-page HTML checklist.

    ## Verification
    The exact commands to re-run, and the before numbers to beat.

    ## What this will not fix
    Named honestly: thin content, no links, no demand for the topic.

Every verdict carries its evidence: the URL fetched and the word count observed. Never report a rendering problem without the number, and never report a fix without the after number.

## Common mistakes

| Mistake | Consequence | Do instead |
|---|---|---|
| Judging the platform from a blog post or its reputation | Wrong diagnosis on a platform that shipped SSR since then | Fetch the URL and read the HTML |
| Testing only the homepage | The one page platforms prerender first, the long tail stays broken | Sample five URLs including dynamic routes |
| Reading DevTools Elements as proof | That is the rendered DOM, every SPA looks fine there | view-source, curl, or Search Console crawled HTML |
| Exporting a Lovable or Base44 project to a static host to "own the stack" | Silently loses platform-side rendering, indexing collapses | Keep hosting, or ship Route B or C in the same move |
| Adding a client-side head manager and calling it fixed | Tags still absent from the HTML that crawlers read | Emit tags in the served document |
| Selling crawler-only prerendering as server rendering | Two versions of the site, silent failures, client trust | Name it as a stopgap and monitor it monthly |
| SPA fallback answering 200 for every unknown URL | Soft 404s across the site | Real 404 status for unknown routes |
| Leaving the .lovable.app or .vercel.app preview indexable | Duplicate site competing with production | noindex the preview or canonical it to production |
| Prerendering hash-routed URLs | Impossible, one URL exists | Move to path routing first |
| Announcing recovery the week of the fix | Credibility burned when nothing moves | Set a several-week expectation, measure in Search Console |
| Blocking /assets/ in robots.txt to save crawl budget | Googlebot renders a broken page | Leave build assets crawlable |
| Writing GEO content before the HTML is served | Quotable passages nothing can quote | Rendering first, then geo-visibility |

## Sources

- AI crawlers do not execute JavaScript, 500M+ fetches analyzed: https://vercel.com/blog/the-rise-of-the-ai-crawler
- AI search and JavaScript rendering: https://www.gsqi.com/marketing-blog/ai-search-javascript-rendering/
- Google on dynamic rendering as a workaround, not a long-term solution: https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering
- Google no longer recommends dynamic rendering: https://searchengineland.com/google-no-longer-recommends-using-dynamic-rendering-for-google-search-387054
- Lovable rendering and SSR status: https://docs.lovable.dev/features/upgrade-to-tanstack-start and https://lovable.dev/seo-aeo
- Base44 product changelog (SEO and crawler snapshots): https://docs.base44.com/changelog/product
- Base44 SSR and SSG feature requests, platform status in the open: https://feedback.base44.com/p/add-ssr-server-side-rendering-support
- Static generation for Vite React apps: https://github.com/Daydreamer-riri/vite-react-ssg
- Field heuristics: 115+ agency audits, labeled as such throughout
