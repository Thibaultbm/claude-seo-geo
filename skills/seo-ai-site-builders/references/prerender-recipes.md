# Conversion recipes: from a JavaScript app to served HTML

Load this file after the route is chosen (skill Step 3). Each recipe states what it produces, when it fits, and the concrete steps. Verify every recipe with the bundled script before calling it done.

Read the repository first. The recipe depends on three facts: the build tool (`vite.config.*`, `next.config.*`, `astro.config.*`), the router (`react-router-dom`, TanStack Router, file-based), and where the page content comes from (in the code, from an API at runtime, from a database).

## Route A: turn on the platform's own rendering

Cheapest fix when the site stays on the platform.

1. Confirm the platform offers it and that the fetched HTML proves it works on this project, not just in the changelog.
2. Where the platform offers an upgrade path (Lovable's TanStack Start template being the current example), take the upgrade rather than the compatibility layer: the upgrade survives an export, the compatibility layer does not.
3. Re-run the check on five URLs including a dynamic detail route.
4. Write into the project notes that hosting now carries an SEO dependency, so a future migration is planned with it in mind.

Stop here if the verdicts come back SERVER RENDERED. Do not add a second prerendering layer on top; two layers disagree eventually, and debugging which one served a given response is miserable.

## Route B: prerender at build time (Vite React SPA to static HTML)

Produces one real HTML file per route, served by any static host. The right answer for marketing sites, portfolios and brochure sites with a blog. Content must be resolvable at build time.

### B1. vite-react-ssg (recommended for React Router projects)

Fits an app already using `react-router-dom` with routes declared as data. It renders each route to HTML at build time and hydrates in the browser.

1. Install `vite-react-ssg`.
2. Move the router configuration into an exported `routes` array, then replace the `createRoot(...).render(...)` entry point with the library's `ViteReactSSG` entry, passing that same array.
3. Change the build script to the library's build command so it emits per-route HTML instead of a single `index.html`.
4. For dynamic routes (`/blog/:slug`), export `getStaticPaths()` returning every path to emit. This function is also the correct source for the sitemap: generate `sitemap.xml` from the same list in a post-build step so the two can never diverge.
5. Move per-page metadata into each route so `title`, `meta description`, canonical and og tags land in that route's HTML.
6. Fetch content at build time (a loader, or a plain import of local markdown or JSON). Any content still fetched in a `useEffect` is absent from the emitted HTML, which is the failure mode that makes teams think prerendering did not work.

Verify: `python3 scripts/render_check.py` against the built output, then open `dist/blog/some-post/index.html` and confirm the article text is in the file.

### B2. A prerender plugin, when the router is not route-data based

Plugins in the `@wroud/vite-plugin-ssg` family take a list of routes and render each to a static file without owning the routing. Lighter to adopt, and the route list is maintained by hand, which is a real maintenance cost on a growing site. Good for a fixed set of pages, poor for a blog.

### B3. Headless-browser snapshotting (react-snap and similar)

Runs the built app in a headless browser and writes the resulting DOM to disk. It requires no code restructuring, which is its whole appeal, and it inherits every timing problem of the app: content that arrives after the snapshot is simply not captured, and the failure is silent. Use it to unblock a deadline, then move to B1. Never use it on a site whose content changes without a rebuild.

### Host configuration for any B recipe

- Serve the emitted files directly. Remove the catch-all `/* -> /index.html 200` rewrite, or it will shadow the static files and answer 200 for URLs that do not exist.
- Add a real 404: unknown routes must return a 404 status with a 404 page.
- Decide trailing slash behavior once, 301 the other form, and canonical to the winner.

## Route C: migrate to a server-rendering framework

For database-driven content, thousands of URLs, or content that changes without a deploy.

| Target | Fits | Notes |
|---|---|---|
| TanStack Start | React apps already on TanStack Router, and Lovable projects on the current template | Closest migration for a modern Lovable or React SPA |
| Next.js (App Router) | Product sites, e-commerce, anything needing request-time rendering and a large ecosystem | The default answer, and the most over-applied: a brochure site does not need it |
| Astro | Content sites, blogs, documentation, marketing | Ships the least JavaScript, islands keep the interactive parts. Best ranking-per-effort for content |
| React Router v7 framework mode | Existing React Router apps that want SSR and SSG in one config without changing routers | Smallest conceptual jump from an existing `react-router-dom` app |

Migration order that avoids a traffic gap:

1. Freeze the URL inventory before touching anything: crawl the site, export Search Console URLs and their clicks. The menu is not the site.
2. Port the public routes first, leave the logged-in app on the old bundle if it has to ship separately.
3. Keep URLs identical. A rendering migration that also changes URL structure turns two attributable changes into one unreadable outcome. If URLs must change, map a 301 for 100 percent of the old set and do it as a separate, later step.
4. Move content fetching from client effects to server loaders or build-time data. This is the actual work; the framework swap is the easy part.
5. Keep titles, h1s and body copy identical on the top pages, so a ranking change means rendering rather than content.
6. Ship, verify with the script, resubmit the sitemap, then watch Search Console coverage daily for two weeks.

Full migration protocol, redirect rules and the freeze checklist: the seo-technical skill, Step 7.

## Route D: crawler-only prerendering (last resort)

Serves rendered HTML to bots and the JavaScript app to humans. Google classes this as a workaround rather than a long-term solution, and maintaining two versions of a site is exactly as fragile as that implies.

Legitimate uses: no code access (Bubble, Softr, Glide), or a stopgap while Route B or C is built.

Two implementations:

- A managed service (Prerender.io being the long-running one) with a middleware, a CDN integration or a host-level rule. Fastest to install, recurring cost, and a cache that must be refreshed when content changes.
- An edge function or worker on the CDN that detects bot user agents, renders the page and returns the HTML. Cheaper at volume, and now it is your service to run: a rendering timeout becomes an empty page served to Googlebot.

Non-negotiable rules for either:

1. Serve the same content to bots and humans. Different content is cloaking, and the line is content parity, not code parity.
2. Cover every crawler that matters, not just Googlebot: OAI-SearchBot, ChatGPT-User, PerplexityBot, ClaudeBot, Claude-SearchBot, Bingbot. A prerender layer keyed to Googlebot alone leaves the AI engines exactly as blind as before, which defeats the point of the exercise in 2026. Current user agent list: the seo-technical skill's references/ai-crawlers.md.
3. Monitor monthly and after every deploy. Run the bundled script with `--ua-compare`: it fetches as a browser, as Googlebot and as GPTBot, and reports the word counts side by side. Equal counts across all three, and non-zero, is the passing state.
4. Set an exit date. Write the migration to Route B or C into the plan with an owner, or the stopgap becomes the architecture.

## The per-page HTML checklist (applies to every route)

After the rendering fix, each indexable URL must serve, before any JavaScript:

- One unique `<title>` and `<meta name="description">`
- A self-referencing absolute `<link rel="canonical">` on the production host
- Exactly one `<h1>`, the real body copy (300+ words on pages meant to rank)
- Real `<a href>` internal links, at least three
- `<img src>` with alt, width and height
- Valid JSON-LD in the document
- og:title, og:description, og:image per URL

Then, and only then, the content questions become worth asking: which blocks the page is missing (seo-page-sections), which schema types apply (seo-schema-markup), and whether the passages are quotable (geo-visibility).
