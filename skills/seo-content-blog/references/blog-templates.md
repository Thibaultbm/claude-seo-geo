# Blog page templates: the article page and the blog hub

The 12-element skeleton in SKILL.md governs the text. This file governs the page the text lives in. A perfect article dropped into a bare template still ships without an author photo, a table of contents, dates, a call to action or social proof, and the audit catches every one of them (`seo_audit.py` reports `toc_missing`, `author_missing`, `author_page_link`, `date_missing`, `no_cta_money`, `hub_no_covers`, `social_placeholder`). When the site is generated or coded by an agent, hand it this file: templates are built once and repeated on every post, so one omission becomes N omissions.

Reference implementation observed in production: the Sorank blog (sorank.com/fr/blog-geo-seo). Each block below says what it is, the minimum spec, and why.

## 1. Article page

Desktop layout: a two-column grid, content column 680-760px, sidebar 280-320px on the right, sticky. Mobile: one column, the table of contents collapses into a `<details>` block under the intro, the sidebar CTA moves to the end of the article.

```
+-------------------------------------------------------------+
| Header (logo, menu, main CTA button)                        |
+-------------------------------------------------------------+
| Breadcrumb: Home / Blog / Category / Article title          |
| H1                                                          |
| Lead paragraph (the meta description, rewritten for humans) |
| Author line: photo 40px, name (link), role | Published dd/mm |
|   | Updated dd/mm | X min read                              |
| Cover image (16:9, WebP, eager, fetchpriority=high)         |
+--------------------------------------+----------------------+
| In short (answer-first block)        | STICKY SIDEBAR       |
| Body: H2 sections, bold, tables,     | - Table of contents  |
|   images, quotes                     |   (active section    |
| In-content CTA block after ~40%      |   highlighted)       |
| Body continues                       | - Author card: photo,|
| Conclusion + CTA                     |   name, role, 1-line |
| FAQ                                  |   bio, link to the   |
| Author box (full): photo, bio,       |   author page, social|
|   credentials, social profiles       |   icons              |
| Related articles (3 cards w/ covers) | - CTA card (offer,   |
| Final CTA banner                     |   lead magnet, quote)|
+--------------------------------------+----------------------+
| Footer (social profiles, legal, sitemap links)              |
+-------------------------------------------------------------+
```

### Block specs

| Block | Minimum spec | Why |
|---|---|---|
| Key takeaways box | 3-5 bullets or 2-4 sentences directly under the H1 block, labeled ("En bref", "Key takeaways") | The answer-first block of the skeleton, made visible as a box |
| Breadcrumb | Visible trail plus BreadcrumbList JSON-LD | Shows the page's place in the silo; feeds the breadcrumb displayed in results |
| Author line under the H1 | Photo (40px, real person, alt = name), name linked to the author page, role, published date, updated date, reading time | E-E-A-T accountability at first glance; dates are a freshness signal Perplexity and AI Overviews weigh visibly |
| Cover image | 1200px wide minimum (Discover needs 1200px+ and `max-image-preview:large`), WebP or AVIF, under 200 KB, `loading="eager"` and `fetchpriority="high"`, width and height set | It is the LCP element: lazy-loading it is the most common speed mistake on blog templates |
| Table of contents | Anchor links to every H2 (H3 optional), generated from the headings so it never drifts; sticky in the sidebar on desktop, highlights the section in view; collapsible block under the intro on mobile | Orientation on long pages, jump links in results, and the subtopic map handed to machine readers in one block |
| Sidebar author card | Photo, name, role, one-line credential, link to the author page, social profile icons (LinkedIn, YouTube, Instagram, X: real profile URLs only) | Keeps the expert visible while reading; links the author entity across platforms |
| Sidebar CTA card | One offer, one button: the product, service, lead magnet, quote or contact page that matches the article intent | Informational readers convert when the next step is always on screen; an article with no CTA wastes the traffic it earns |
| In-content CTA block | One block after roughly 40% of the body, visually distinct (background color, button), pointing to the commercial page closest to the article intent | Most readers never reach the conclusion; the mid-article block catches them |
| Conclusion CTA | Final paragraph plus button to the same commercial page | Second-most-read block for skimmers |
| Author box (end of article) | Photo 96-120px, name, role, 2-4 line bio with verifiable credentials (years, results, certifications), link to the author page, social profiles | The full E-E-A-T statement, repeated where readers decide whether to trust |
| Sources section | Before the FAQ: each source listed with what it supports in the article | Shows the work; the sourced-content signal measured in the GEO layer |
| Hub link | "Continue on {topic}" link back to the topic hub or category page | Closes the silo loop; readers move to the next article in the path |
| Glossary links | First mention of each defined term per article links to its glossary page (not every mention) | Internal linking at scale and definitions AI engines can cite |
| Share buttons | Plain links (no heavy third-party script) to the networks the audience uses | Cheap distribution; 4 of 11 audited coaching blogs show them |
| Related articles | 3 cards with cover image, title, one-line excerpt, same category first | Internal links within the silo, pages per session |
| Final CTA banner | Full-width block before the footer: promise, social proof (client avatars, rating, number of clients), button | The last conversion surface |
| Social profiles in the footer | Real profile URLs, never a network homepage (`https://www.instagram.com/` is a placeholder, not a profile) | Entity consistency across platforms, and the `sameAs` list must point to the same profiles |

Never use a placeholder link: a footer icon pointing to `instagram.com/` or `#` is worse than no icon (a dead promise for visitors, a broken entity link for engines). If a profile does not exist, remove the icon.

### Sticky table of contents (framework-free)

Generated from the H2s on load, so authors never maintain it by hand. The links are in the HTML at load for crawlers when the template server-renders the list; this script only adds the active-section highlight. If the CMS cannot server-render the list, generate it client-side with the same code (Google renders JavaScript; AI crawlers do not, but the H2s themselves remain in the HTML).

```html
<aside class="article-sidebar">
  <nav class="toc" aria-label="Sommaire">
    <p class="toc-title">Sommaire</p>
    <ol>
      <li><a href="#section-1">First H2</a></li>
      <li><a href="#section-2">Second H2</a></li>
    </ol>
  </nav>
  <!-- author card, CTA card -->
</aside>

<style>
  .article-layout { display: grid; grid-template-columns: minmax(0, 720px) 300px; gap: 48px; }
  .article-sidebar { position: sticky; top: 96px; align-self: start; }
  .toc a.is-active { font-weight: 600; text-decoration: underline; }
  @media (max-width: 991px) {
    .article-layout { grid-template-columns: 1fr; }
    .article-sidebar { position: static; }
  }
</style>

<script>
  // Highlight the H2 currently in view.
  const links = document.querySelectorAll('.toc a');
  const targets = [...links].map(a => document.querySelector(a.getAttribute('href')));
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      links.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + e.target.id));
    });
  }, { rootMargin: '0px 0px -70% 0px' });
  targets.forEach(t => t && io.observe(t));
</script>
```

Every H2 carries a stable, readable `id` (the slugified heading), so the anchors survive edits and can be shared.

### Article JSON-LD

One BlogPosting with the author as a full Person (photo, role, page, social profiles), the publisher as the Organization, real dates, and the breadcrumb. Never ship FAQPage with empty `name` or `text` values: a template that outputs the FAQ markup before the CMS fills the questions produces invalid nodes on every post (the audit reports them as `Question xN: missing or empty name`).

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "@id": "https://example.com/blog/slug/#article",
      "headline": "Article title, 110 characters max",
      "description": "Meta description",
      "image": "https://example.com/images/cover-1200.webp",
      "datePublished": "2026-10-01",
      "dateModified": "2026-10-08",
      "author": { "@id": "https://example.com/auteur/firstname-lastname/#person" },
      "publisher": { "@id": "https://example.com/#organization" },
      "mainEntityOfPage": "https://example.com/blog/slug/"
    },
    {
      "@type": "Person",
      "@id": "https://example.com/auteur/firstname-lastname/#person",
      "name": "Firstname Lastname",
      "jobTitle": "Role",
      "image": "https://example.com/images/author.webp",
      "url": "https://example.com/auteur/firstname-lastname/",
      "sameAs": [
        "https://www.linkedin.com/in/real-profile/",
        "https://www.youtube.com/@realchannel",
        "https://www.instagram.com/realprofile/"
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://example.com/" },
        { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog/" },
        { "@type": "ListItem", "position": 3, "name": "Article title" }
      ]
    }
  ]
}
```

The Organization node (`@id` `#organization`) lives on every page or at least on the homepage; field rules in seo-schema-markup.

## 2. Author page

Every article links to it; it is the page that proves the expertise. Blocks: H1 with the name and role, large photo, bio of 150-300 words with verifiable facts (years of practice, results, certifications, press), social profiles, the list of the author's articles (cards with covers), a CTA to the offer. JSON-LD: ProfilePage with `mainEntity` the Person (same `@id` as in the articles). On a one-expert site the about page ("Mon parcours", "Qui suis-je") can be the author page: link to it from every byline.

## 3. Blog hub

```
+-------------------------------------------------------------+
| Breadcrumb, H1 (keyword + promise), 2-3 line intro          |
| Category filters (links to crawlable category pages)        |
| Featured article: large card, cover image, excerpt          |
| Grid of cards (3 per row desktop, 1 mobile):                |
|   cover image 16:9 (alt = article topic), category label,   |
|   title (H2 or H3), 1-2 line excerpt, date, reading time,   |
|   author photo + name                                       |
| CTA block (lead magnet or offer) after the first 6 cards    |
| Pagination with real URLs (/blog/page/2/), never only a     |
|   "load more" button                                        |
+-------------------------------------------------------------+
```

| Rule | Why |
|---|---|
| Every card carries its cover image | A text-only list looks abandoned, gets fewer clicks and loses image search entry points; the audit flags `hub_no_covers` when fewer than half the listed posts have a linked image |
| First row of covers eager, the rest lazy | First row is above the fold; the rest should not compete for bandwidth |
| Categories are real pages with an intro | Category pages rank on head terms and route authority to the posts |
| Pagination is crawlable | A "load more" button with no URL hides older posts from crawlers |
| Blog JSON-LD with a `blogPost` list, or ItemList | Hands the post inventory to machines in one block |
| Topic hubs or reading paths once there are 3+ posts per theme | Groups the posts into silos that rank on the head term of each theme |
| Search once there are about 12+ posts | Readers find the post they came for; search pages themselves stay noindex |

## 4. Pre-publish template checklist

- [ ] Breadcrumb visible and in JSON-LD
- [ ] Author line under the H1: photo, linked name, role, published and updated dates, reading time
- [ ] Cover image 1200px+, WebP or AVIF, under 200 KB, eager with fetchpriority high, width and height set
- [ ] Table of contents from the H2s, sticky in the sidebar on desktop, collapsible on mobile
- [ ] Sidebar author card with real social profiles and a link to the author page
- [ ] Sidebar CTA card plus one in-content CTA block plus the conclusion CTA, all to a commercial page
- [ ] End-of-article author box with credentials and social profiles
- [ ] 3 related articles with covers
- [ ] BlogPosting + Person (with sameAs) + BreadcrumbList JSON-LD, no empty FAQ nodes
- [ ] og:type article, og:title, og:description, og:image (the cover), twitter:card, canonical
- [ ] Key takeaways box, sources section, link back to the topic hub
- [ ] No placeholder social link anywhere on the page
- [ ] Hub: every card has a cover, categories are pages, pagination has URLs

Verify with `python3 skills/seo-geo-audit/scripts/seo_audit.py <home> /blog/ /blog/<one-post>/`: the TEMPLATE, BLOG HUB and SOCIAL lines must come back clean.
