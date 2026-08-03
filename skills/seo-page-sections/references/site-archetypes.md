# Site Archetypes and Global Blocks

Which page types a site needs depends on what kind of site it is. This file carries the three archetypes, the page inventory per archetype, and the two blocks that repeat on every page of every archetype (header and footer). Per-page block lists live in `page-type-matrix.md`.

Source: the Sorank master wireframe, the house template set used on client builds. Where a rule is a house convention rather than a measured fact, it says so.

## Why archetypes come first

Auditing a page type in isolation misses the most expensive gap, which is a page type that does not exist at all. A Shopify store with no collection pages and a marketplace with no reference pages fail for the same reason, and neither failure is visible when auditing the pages that do exist.

So run the audit in this order: identify the archetype, list the page types it should have, find the ones missing entirely, then audit the blocks inside the ones present.

## Archetype 1: Shopify store

Selling own products, transactional, catalog-driven.

| Page type | Required | Block list |
|---|---|---|
| Home | yes | matrix section 8 |
| Collection | yes | matrix section 2 |
| Product | yes | matrix section 1 |
| Article (single post) | yes | matrix section 7 |
| Blog (index or hub) | yes | see below |
| About | yes | matrix section 10 |
| Contact | yes | matrix section 11 |
| Affiliate or partner | no | see below |
| 404 | yes | see below |

## Archetype 2: Webflow or WordPress site

Selling services or expertise, content-driven. The most common archetype in agency work.

| Page type | Required | Block list |
|---|---|---|
| Home | yes | matrix section 8 |
| Collection (content hub or pillar) | yes | matrix section 2, adapted to content |
| Service | yes | matrix section 3 |
| Article (single post) | yes | matrix section 7 |
| Blog (index or hub) | yes | see below |
| Call or booking | yes | see below |
| Author page | yes | see below |
| Free HTML tool | no | see below |
| About | yes | matrix section 10 |
| Contact | yes | matrix section 11 |
| Wall of love | no | see below |
| Affiliate or partner | no | see below |
| 404 | yes | see below |

## Archetype 3: Marketplace

Aggregating third-party supply, directory-driven.

| Page type | Required | Block list |
|---|---|---|
| Home | yes | matrix section 8 |
| Collection (category of listings) | yes | matrix section 2 |
| Service | yes | matrix section 3 |
| Reference (single listing) | yes | see below |
| Login and signup | yes | see below |
| Top 10 or ranking | yes | see below |

Marketplaces carry a structural SEO risk the other two archetypes do not: thin, duplicated listing pages at scale, and user-generated pages with no editorial layer. Audit the listing template before auditing any single listing, since one template fix corrects every page built on it.

## Page types specific to these archetypes

Block lists for the types not already in `page-type-matrix.md`. Levels use the same R / W / O scale.

### Blog index or hub

Distinct from a single article. Its job is routing and topical authority, not depth.

| Block | Level | Why |
|---|---|---|
| H1 naming the topic territory, not "Blog" | R | "Blog" ranks for nothing; the category term does |
| Intro text, 100 to 300 words, stating what the hub covers | R | Gives an index page something to rank with |
| Article cards with real titles, dates and excerpts | R | The routing function |
| Category or pillar navigation | R | Exposes the silo structure |
| Links to the pillar pages | R | Distributes authority into the money pages |
| Pagination that keeps deep articles crawlable | R | Otherwise old posts go orphan |
| Newsletter or lead capture | W | The hub attracts the not-ready visitor |
| Featured or most-read block | W | Concentrates authority on the pages worth ranking |

### Call or booking page

| Block | Level | Why |
|---|---|---|
| H1 naming what the call is | R | "Book a call" is the query and the intent |
| What happens during the call, in steps | R | The objection is the unknown, not the price |
| Duration and cost, stated plainly | R | "Is this a sales call and will it cost me" is the real question |
| Who you will speak to, named, with a photo | R | A booking with a nobody converts worse |
| Embedded booking widget with a no-JS fallback route | R | If the widget fails, the page must still convert |
| Qualification: who it is for and not for | W | Filters out the bookings that waste both sides |
| Proof: reviews from people who booked | W | Reduces the perceived risk of the slot |
| FAQ: rescheduling, preparation, what to bring | W | The pre-call support load, answered once |

### Author page

The E-E-A-T asset. It validates every byline on the site, so its weakness propagates to every article.

| Block | Level | Why |
|---|---|---|
| Full name as H1, real photo | R | The entity this page exists to establish |
| Credentials, experience, since when | R | The claim that makes the bylines worth anything |
| `sameAs` links: LinkedIn, X, GitHub, publications | R | Corroboration off-site is what makes the claim checkable |
| List of articles by this author | R | Connects the person to the body of work |
| Areas of expertise, stated concretely | W | Topical association between person and subject |
| External proof: talks, press, books, certifications | W | Third-party validation |
| Contact route | O | Journalists and partners land here |
| Person schema with `sameAs` and `knowsAbout` | R | Entity resolution |

### Free HTML tool page

A calculator, generator or checker. The strongest link magnet a content site can build, and the page type most often shipped in a way search engines cannot see.

| Block | Level | Why |
|---|---|---|
| H1 naming the tool as it is searched | R | "{thing} calculator" is a query with commercial adjacency |
| The tool itself, usable without signup | R | A gated tool earns no links |
| Static text explaining what it does and how, 300+ words | R | The tool is JavaScript; without prose the page has nothing indexable |
| Worked example with real numbers | R | Both a usability aid and indexable content |
| Method or formula used, stated | W | The provenance that makes the tool quotable |
| FAQ about the tool and its inputs | W | Long tail around the tool term |
| Links to the service the tool qualifies for | R | The commercial reason the tool exists |
| Embed or share affordance | W | How the page earns links passively |

The recurring failure: the whole page is a JavaScript app, so raw HTML is empty and AI crawlers see nothing. Ship the explanatory prose server-rendered.

### Wall of love

An aggregated testimonial wall, usually embedded from a third party.

| Block | Level | Why |
|---|---|---|
| Testimonials as server-rendered HTML text | R | A JavaScript widget is invisible to crawlers and assistants, which defeats the entire point |
| Attribution: name, role, company, photo or link | R | Anonymous praise persuades nobody and proves nothing |
| Source of each testimonial, linked where public | W | Verifiability |
| Filter or grouping by segment or use case | W | Proof only transfers from a recognizable peer |
| Aggregate rating, if real and backed by the wall | W | The summary most visitors read instead of the wall |
| CTA after the wall | R | The wall is the peak of persuasion; do not waste it |

### Affiliate or partner page

| Block | Level | Why |
|---|---|---|
| H1 naming the program | R | "{brand} affiliate program" is a query |
| Commission terms, rates and cookie window, as text | R | The only thing affiliates are here to read |
| Payment terms, threshold and schedule | R | The second thing, and the top pre-signup question |
| Who can join and who cannot | R | Filters unusable applicants |
| Signup route | R | The conversion |
| Assets provided: links, banners, tracking | W | Reduces the friction of the first promotion |
| Program rules: brand bidding, coupon sites, spam | R | Prevents the abuse that costs more than the program earns |
| FAQ: payouts, tracking, attribution, taxes | W | Support deflection |

Affiliate pages often carry outbound links at scale. Keep the link policy explicit and consistent with the site's own linking rules.

### 404 page

| Block | Level | Why |
|---|---|---|
| Returns HTTP 404 or 410, not 200 | R | A soft 404 returning 200 pollutes the index with duplicate empty pages |
| Plain statement that the page does not exist | R | Orientation |
| Search box | R | The fastest recovery route |
| Links to the main sections and the most useful pages | R | Recovers the visit instead of losing it |
| Same header, footer and navigation as the rest of the site | R | A bare 404 loses the visitor entirely |
| Noindex is unnecessary | R | A correct 404 status is enough; adding noindex to a 200 response is the wrong fix for the wrong problem |

### Reference or listing page (marketplace)

| Block | Level | Why |
|---|---|---|
| H1 naming the listing as searched | R | Entity plus category |
| Unique descriptive content, not the supplier's boilerplate | R | The duplication that kills marketplace SEO at scale |
| Structured attributes in a table | R | The filterable, extractable layer |
| Price or price range as text | R | Comparison intent |
| Photos, real, with alt text | R | Trust in a low-trust context |
| Reviews specific to this listing | R | The trust mechanism marketplaces run on |
| Availability or status, accurate | R | Stale listings destroy marketplace credibility |
| Contact or booking route | R | The conversion |
| Breadcrumb | R | Depth orientation in a large catalog |
| Cross-links: similar listings, parent category | R | Distributes crawl into the long tail |
| Editorial layer: what makes this listing notable | W | The only defense against thin-page penalties at scale |

### Top 10 or ranking page (marketplace)

Treat as a comparison page. Full spec: `seo-content-comparison-page/references/comparison-page-patterns.md`, family 3.

| Block | Level | Why |
|---|---|---|
| Selection method: how ranked, on what data, when | R | An unstated ranking rule is an opinion, not a ranking |
| Ranked list with a stated reason per position | R | The extractable answer |
| Comparison table across the ranked options | R | The block assistants quote |
| Best-for verdicts per use case | R | One page answers many query variants |
| Update date | R | Rankings decay faster than any other content |
| Disclosure of any commercial relationship | R | Legal in most markets, and a trust requirement everywhere |

### Login and signup

Not an SEO page, and that is the finding.

| Block | Level | Why |
|---|---|---|
| Noindex | R | Zero search value, and it dilutes crawl budget across a large site |
| Not linked from indexable content in a way that bleeds authority | W | Header link is fine; body links from money pages are waste |
| Working password reset and error states | R | Where signups die silently |
| No content locked behind it that should be indexable | R | The common architecture mistake: gating pages that should rank |

## Global block: header

House rules from the master wireframe. These are conventions, tuned for crawlability and CRO, not measured thresholds.

| Rule | Level | Why |
|---|---|---|
| Logo at a fixed size, wrapped in a block link to the home page | R | Universal convention; a logo that does not link home breaks expected behavior |
| Drop the explicit "Home" link when the header has fewer than 5 links | W | The logo already goes home; the slot is worth more to a money page |
| Dropdown once a category holds more than 3 pages | W | Below that, a flat header keeps the links visible to crawlers and users |
| Link to the contact page, always | R | Reachability and legitimacy |
| CTA in a strong contrasting color, pointing to the call or quote page | R | The header CTA is the highest-traffic conversion element on the site |
| Pillar pages exposed in the navigation | R | The header is the strongest internal link source; spend it on the pages that must rank |
| Same links present in the mobile header | R | Mobile-first indexing reads the mobile markup |
| Navigation in HTML, not built by JavaScript | R | A JS-only menu removes the site's primary crawl path for AI crawlers |

The header is an internal linking decision before it is a design decision. Every slot spent on a low-value page is a slot not spent on a page that needs authority (seo-internal-linking).

## Global block: footer

| Rule | Level | Why |
|---|---|---|
| Logo at a fixed size, in a block link to the home page | R | Consistency with the header |
| Links to every pillar page, grouped by subject with a column heading | R | House rule: the footer is where the silo structure is stated site-wide |
| One-line description of the company under the logo | W | Entity repetition on every page |
| Social profile links with `nofollow noreferrer noopener` | R | House rule: no authority leak, and `noopener noreferrer` closes the tab-nabbing and referrer leak on `target="_blank"` |
| Links to the legal pages: terms, privacy, cookies, data processing | R | Legal requirement in most markets, and a legitimacy signal |
| Contact details, or a link to contact | R | Reachability from every page |
| Copyright line with the current year | O | Cosmetic, but a stale year reads as an abandoned site |

Do not dump every URL into the footer. A footer linking to 200 pages distributes nothing meaningful and buries the pillar links it exists to carry.

## Global layer: marketing levers

The persuasion principles the wireframes place deliberately, rather than decoratively. Cialdini's six, applied to page blocks. Use them to judge whether a page has any persuasion architecture at all, not as a checklist to fill.

| Lever | Where it lives in the blocks | Failure mode |
|---|---|---|
| Reciprocity | Free tool, free guide, template, audit, sample | Giving something worthless, which costs trust instead of building it |
| Consistency | Micro-commitments: a short quiz, a small first step, a free tier | A first step so large it is the whole decision |
| Social proof | Reviews, ratings, logos, wall of love, case studies, counts | Proof from a segment the reader does not recognize as a peer |
| Liking | Founder block, real photos, team page, author page, story | Stock photography, which inverts the effect |
| Authority | Credentials, certifications, press, data, expert quotes, `sameAs` | Claimed authority that cannot be verified off-site |
| Scarcity | Real stock levels, real deadlines, limited cohorts | Fake countdowns, which are illegal in several markets and detectable everywhere |

Every lever must be true. A fabricated scarcity or an invented review is both a legal exposure and the fastest way to lose the trust the page exists to build.
