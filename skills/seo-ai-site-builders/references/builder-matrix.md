# AI site generator matrix: rendering, export, and the route that fixes it

Load this file when the builder is known, or when the bundled script returns a fingerprint. Status as of August 2026. Every platform here ships changes faster than this file can track, so the matrix sets the expectation and Step 1 of the skill sets the fact. If the fetched HTML contradicts a row below, the HTML wins and the row is out of date.

Column meanings:

- Default rendering: what the platform serves when nobody has configured anything.
- Code out: whether the source can leave the platform and still run.
- Route: A native rendering, B build-time prerendering or SSG, C framework migration, D crawler-only prerendering. Defined in the skill's Step 3.

## Code generators (they hand you a repository)

### Lovable

- Default rendering: apps created from 13 May 2026 are built on TanStack Start with server-side rendering. Older React and Vite projects get automatic prerendering while they are hosted on Lovable. Both were shipped in the May 2026 discoverability release, alongside built-in SEO controls.
- Code out: yes, GitHub connection or ZIP. Projects are standard Vite or TanStack Start apps.
- Fingerprint: `cdn.gpteng.co/gptengineer.js`, `lovable-tagger`, `.lovable.app`.
- Route: A when hosted on Lovable and the fetched HTML confirms it. B or C the moment the project moves to a static host.
- Gotchas: the older-app prerendering is a hosting feature, so exporting the repo and deploying the `dist` folder to a bucket, Netlify or a plain Vercel static project returns the site to shells. Upgrading an old project to the TanStack Start template is the durable version of the same fix. Dynamic detail routes are the ones most likely to be missing from a prerender pass, so sample them specifically.

### Base44 (Wix)

- Default rendering: client-rendered React. Since mid-2026 the platform prepares a rendered version of each page behind the scenes and serves it to search and AI crawlers, refreshed on publish and on data changes. A June 2026 changelog entry added labeled page sections and per-page descriptions to that snapshot.
- Code out: limited. Treat the platform as the runtime.
- Fingerprint: `base44.app`, `base44` in asset paths.
- Route: A, with Route D's monitoring duty attached, because the rendering is crawler-side rather than in the response every visitor gets.
- Gotchas: verify the snapshot covers entity-driven detail pages, not just static routes, and that it refreshes when records change. The community feature requests for real SSR and SSG are still open, which is the clearest public signal of where the platform's limits are.

### Bolt (StackBlitz)

- Default rendering: a Vite single page app unless the prompt explicitly asked for Next.js, Astro, Nuxt or SvelteKit. Bolt will generate those frameworks on request, which makes the prompt the cheapest intervention point.
- Code out: yes.
- Fingerprint: `bolt.new`, `stackblitz`.
- Route: B for a marketing site, C when the app needs request-time data. If the project is young, regenerating with an explicit framework instruction beats retrofitting.

### v0 (Vercel)

- Default rendering: Next.js with server rendering, deployed on Vercel.
- Code out: yes.
- Fingerprint: `v0.dev`, `v0.app`, `/_next/static`.
- Route: usually none needed. Verify anyway: a Next.js app can still be effectively client-rendered when every page is a client component fetching its content in an effect, and the HTML then looks exactly like a Vite shell. The script's word count catches this in one call.

### Replit, Firebase Studio, Rocket, Create, Mocha, Emergent, Dyad, Hostinger Horizons, Figma Make and the rest of the agentic builders

- Default rendering: whatever stack the agent generated, most commonly a Vite React single page app; some produce Next.js.
- Code out: usually yes.
- Fingerprint: check the framework markers first (`/_next/static` for Next.js, `/_nuxt/` for Nuxt, `astro-island` for Astro, `/assets/index-*.js` with an empty root div for a Vite SPA), then the hosting domain.
- Route: read the repository before deciding. A `vite.config` plus `react-router-dom` means Route B or C. A `next.config` with client components everywhere means fixing the components, not the framework.
- Gotcha: these tools change their default template between releases, so two projects from the same tool three months apart can differ. Never generalize from a sibling project.

## No-code platforms (no repository to fix)

### Bubble, Softr, Glide

- Default rendering: client-rendered by design. The rendering model is the product, so no prompt or setting changes it.
- Code out: no.
- Fingerprint: `bubble.io`, `bubble_page_load`, `softr`, `glideapps.com`.
- Route: D, or move the public pages off the platform. The honest arithmetic: a marketing site on these platforms is typically 5 to 15 public pages, which rebuilds in a weekend on Astro or a static generator, against a prerendering subscription that runs forever and fails silently. Keep the app where it is, move only the pages meant to be found.

### Durable, Dora and similar one-prompt site builders

- Default rendering: varies by platform and by template, some server-render and some do not.
- Code out: generally no.
- Route: fetch first. If the HTML is a shell and there is no export, the platform choice is the problem and the fix is a platform change, which is a business decision to surface plainly rather than an engineering task.

## Established builders with AI features layered on

Wix (including ADI), Squarespace, Webflow, Framer and Shopify serve rendered HTML. Their AI features generate content and layout inside an already server-rendered system, so rendering is not the issue and this skill is the wrong tool. Run the seo-technical skill instead, and expect the real findings to be thin content, weak internal linking, template duplication and platform limits on redirects, sitemap control and URL structure.

WordPress is server-rendered too, with one exception worth checking: a headless WordPress front end built by an AI generator has all the problems in this skill, since only the API stayed on WordPress.

## Choosing a builder before the site exists

When the question is "which one should we start with", the ranking depends on one thing: whether the public pages must be found.

| Priority | Pick | Reason |
|---|---|---|
| The site is a marketing or content site that has to rank and be cited | A framework with SSG or SSR from the start (Astro, Next.js, TanStack Start), generated by Bolt or v0 with an explicit framework instruction | Rendering is decided once, at the start, and costs nothing then |
| An app with a small public surface | Any builder for the app, a separate static site for the public pages | Splitting is cheaper than retrofitting either half |
| A prototype nobody needs to find | Anything | Rendering does not matter, and this skill applies later if the prototype becomes the product |

The expensive mistake is not picking a client-rendered builder. It is picking one, publishing 60 pages, waiting nine months for traffic that structurally cannot arrive, and then paying for the migration with the content already written against the wrong routing model.
