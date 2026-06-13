---
name: seo-content-service-page
description: "Build service pages and landing pages that rank and convert for agencies, consultants, trades, clinics, law firms, and SaaS. Input: a service, business, and target area. Output: a field-tested wireframe (hero + CTA, social proof, benefits, numbered process, founder bio, 750+ word SEO block, reviews, FAQ), title/H1/slug/meta patterns, a competitor depth benchmark, region/city pages, and a GEO layer. Use for a service page, landing page, lead-generation page, or city/service-area page that gets no organic leads."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Service Page SEO: Money Pages That Rank and Convert

Service pages are where rankings turn into revenue. A blog post attracts readers; a service page attracts buyers typing "web design agency", "divorce lawyer geneva", or "emergency plumber lyon". This skill covers how to structure, write, and audit these pages so they rank in Google, convert visitors into leads, and get cited by AI assistants that now recommend providers directly.

The methodology combines two evidence levels, labeled throughout:

- **Field heuristic**: rules derived from 115+ real agency audits of service-business websites (2024-2026). Consistently observed, not lab-measured.
- **Measured**: claims backed by a published study or official documentation, with the source.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use this skill

Use it to create a new service page, rewrite an underperforming one, split a one-page site into service pages, plan city or region pages for a multi-area business, or audit an existing money page against the wireframe below.

Stay in scope. Hand adjacent work to the right skill:

| Task | Skill |
|---|---|
| Service pages, service landing pages, city pages (this skill) | seo-content-service-page |
| Blog articles and informational content | seo-content-blog |
| Ecommerce product pages | seo-content-product-page |
| Category and collection pages | seo-content-collection-page |
| Keyword selection and SERP intent analysis | seo-keyword-research |
| Google Business Profile, reviews, Maps, NAP | seo-local |
| Crawlability, Core Web Vitals, AI crawler access | seo-technical |
| Structured data implementation details | seo-schema-markup |
| Site-wide internal link architecture | seo-internal-linking |
| Citation and directory link building | seo-backlinks |
| Writing rules for AI answer citability | geo-visibility |
| Measuring AI assistant visibility | geo-tracking |
| Full-site audit | seo-geo-audit |

## Workflow

### Step 1: Map services to pages (one service = one page)

The single most common audit finding (field heuristic): a brochure site with one page that lists every service, invisible on all of them. Each service has its own keyword, its own SERP, and its own search intent. One page cannot win five different SERPs.

1. List every billable service the business sells.
2. For each, identify the query a buyer actually types (see seo-keyword-research).
3. Apply the SERP test: if two service names show different top 10 results, they need two pages. If Google returns the same results for both, one page covers both.
4. Plan one URL per service, plus a parent "Services" hub page that links to all of them.
5. If splitting an existing page, 301-redirect nothing that ranks; build the new pages first, then re-point internal links.

Competitor-benchmark page mapping (field heuristic): to surface missing service and sector pages fast, paste the sitemap or page list of the 10 largest competitors into an AI model and ask it to list the page types they have that the audited site lacks. This exposes one-page sites and absent service, sector, and use-case pages in one pass, before manual SERP testing. Cross-check each suggested page against real buyer demand (Step 2) before committing it.

Why: Google ranks pages, not sites, for transactional queries. A page about everything has diluted relevance for each thing. Splitting also gives each service its own title, H1, FAQ, and proof, which a combined page cannot do.

### Step 2: Pick the target keyword and read the SERP

One primary keyword per page, chosen from real buyer language, not internal jargon ("emergency plumber", not "rapid hydraulic intervention"). Check the live SERP before writing:

Read the SERP like a brief:

| SERP signal | Implication for the page |
|---|---|
| Local pack and city-modified results dominate | Treat the page as local: city in title, H1, URL (Step 7); build the profile side with the seo-local skill |
| Comparison listicles rank ("top 10 CRO agencies") | Add the proof depth listicles quote: client numbers, pricing, named differentiators |
| Competitor service pages rank | Direct wireframe battle: benchmark them and exceed (Step 3) |
| Informational guides rank | The query is not transactional; cover it with a blog post (seo-content-blog) and aim the service page at the buyer query |
| People Also Ask and AI Overviews present | Harvest the questions for the FAQ block and the GEO layer |

### Step 3: Benchmark the pages that already rank

The master volume rule: match or exceed the competitors who currently rank, then fill their gaps. 750+ words is the floor that works in most service SERPs (field heuristic), but if the top 3 average 1800 words with pricing tables and case studies, 800 words will not be enough.

Open the top 3-5 ranking pages and record: word count, section list, proof elements (logos, reviews, numbers), pricing display, FAQ presence, schema types. To extract titles, headings, and word counts at scale, run the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py) on the competitor URLs.

### Step 4: Build the page on the canonical wireframe

Nine blocks, in this order. The order follows how a skeptical visitor decides: promise, proof, benefit, process, human, depth, peers, objections, action.

| # | Block | Job |
|---|---|---|
| 1 | Hero: promise + CTA above the fold | Pass the 5-second test |
| 2 | Client and press logos | Borrowed trust, instantly scannable |
| 3 | Benefits (outcomes, not features) | Answer "what do I get" |
| 4 | How it works, 3-4 numbered steps | Reduce perceived risk and effort |
| 5 | About the founder: real photo + story | E-E-A-T and human connection |
| 6 | SEO text block, 750+ words | The semantic reservoir that ranks |
| 7 | Client reviews | Peer proof in the buyer's words |
| 8 | FAQ, 3+ questions | Kill the last objections |
| 9 | Final CTA + 2-3 related blog posts | Convert or keep them in the silo |

Block details and the reasoning behind each:

**1. Hero.** State the outcome the client gets, in their words, with the primary keyword in the H1. Why: most visitors decide to stay or bounce within seconds; if they must scroll to learn what the page sells, the page loses. Checklist:

- H1 contains the primary keyword, phrased as the outcome
- Subline names the audience and carries one number (rating, clients served, years)
- One primary CTA visible without scrolling, repeated in a sticky header on mobile
- No carousel and no autoplay video that delays the promise

**2. Logo strip.** Client logos, press mentions, certifications, review-platform ratings. Why: visitors scan for evidence that people like them already trust this business; logos deliver that faster than any sentence.

**3. Benefits.** 3-6 cards. Translate every feature into what the client obtains: "weekly report" becomes "you know exactly what changed and why, every Monday". Formula per card: feature, then the outcome it buys, then a number when one exists. Why: buyers pay for outcomes; features force them to do the translation themselves, and most will not.

**4. How it works.** 3-4 numbered steps from first contact to delivered result, each step one short paragraph. Why: a clear process makes the purchase feel reversible and managed; numbered steps also match how AI assistants and featured snippets present "how does X work" answers.

**5. About the founder.** Real photo (not stock), first and last name, and a short story: why they do this work, for whom, since when. Why: Google's quality rater guidelines evaluate experience and trustworthiness, and a named, visible human is concrete evidence (measured: E-E-A-T in Google's Search Quality Rater Guidelines). On the conversion side, a real face with real imperfections connects better than polished stock imagery (field heuristic: stock-photo "teams" are a recurring trust killer in audits).

**6. SEO text block.** 750+ words minimum (field heuristic), structured with H2/H3 subheadings. This is the page's semantic reservoir: service pages are conversion-first up top, but Google needs substantial text to understand and rank the page, and this block carries that load without hurting the sections above it. Write each H2 as a real question and open each section with a direct 2-4 sentence answer (this doubles as the GEO layer, see below). Cover, as question-form H2s:

- What the service includes (deliverables, scope, what is excluded)
- Who it is for, and who it is not for
- How much it costs and what drives the price, with the price or a range in plain HTML text: it filters unqualified leads and it is the passage AI assistants quote for "how much does X cost" (field heuristic)
- How long it takes, from start to delivered result
- Method, tools, and guarantees
- Why this provider: a proof recap with numbers

**7. Reviews.** Format each as: first name + situation + problem + result ("Marc, bakery owner in Lyon: bookings doubled in 3 months"). Video reviews outperform written ones (field heuristic). Never invent or embellish testimonials: fake reviews are a legal risk in many markets and a trust risk everywhere. Do not add review structured data about your own organization on your own site: Google treats self-serving review markup as ineligible (measured: Google review snippet guidelines, see Sources).

**8. FAQ.** Minimum 3 questions, sourced from People Also Ask for the target keyword plus the objections sales actually hears. Answer each in 2-4 direct sentences. Why: FAQ rich results have been restricted to government and health sites since August 2023 (measured: Google, see Sources), but the content still feeds People Also Ask, AI Overviews, and assistant answers, and it closes real objections on the page.

**9. Final CTA + related articles.** Repeat the CTA, then link 2-3 supporting blog posts on the same topic. Those posts must link back to the service page. Why: this builds a mini silo, concentrating topical relevance and link equity on the money page (architecture details: seo-internal-linking skill).

**Adapt the wireframe to the business type.** The 9 blocks stay; the emphasis shifts:

| Business type | Keep everything, plus |
|---|---|
| Agency, consultant | Case results with numbers in blocks 2-3, portfolio links, team credentials |
| Trade (plumber, electrician, roofer) | Click-to-call as the primary CTA, emergency hours in the hero, service-area list, photos of real jobs |
| Solo professional (physio, coach, doctor, lawyer) | Block 5 (founder bio) is the page's lead sales argument, not a footnote: the buyer is choosing a person, so the named-and-photographed practitioner is the differentiator. Make the bio prominent, with credentials, registrations, and a real story (field heuristic) |
| Clinic, lawyer, regulated profession | Practitioner credentials and registrations in block 5, claims reviewed for regulatory compliance, consultation-booking CTA |
| SaaS or productized service | Demo or trial CTA, integration logos, security and compliance proof, transparent pricing table. Extend one service = one page into one target sector = one page (a dedicated page per vertical, e.g. "for construction firms"), one persona = one page, and one feature = one page: tighter specialization wins more long tail and converts better (field heuristic) |

### Step 5: Apply the metadata pattern

| Element | Pattern | Example |
|---|---|---|
| Title | Service keyword + brand (+ city if local), about 50-60 characters | Emergency Plumber in Lyon \| Dupont Plomberie |
| H1 | The service keyword, phrased for humans, one per page | Emergency plumber in Lyon |
| Slug | Short, keyword only, no dates or stop words | /emergency-plumber-lyon/ |
| Meta description | Handwritten, 160 characters or fewer: promise + proof + call to action | On site in under 1 hour, 24/7. 4.9/5 from 312 clients. Call now. |
| First paragraph | Primary keyword (+ city) within the first 100 words | "Looking for an emergency plumber in Lyon? ..." |
| Image alts | Describe the image; include service and city where natural, never on every image | "Dupont Plomberie technician repairing a burst pipe in a Lyon apartment" |

Why handwritten metas: Google rewrites weak ones, and the meta is ad copy for the click, not a ranking factor. The 160-character limit is a display truncation heuristic, not a Google rule.

### Step 6: Place CTAs after every major section

One CTA above the fold, then one after benefits, after the process, after reviews, and at the end. Vary the framing (book, call, get a quote) but keep one primary action. Why: readiness to act arrives at different points for different visitors; a single CTA at the bottom only catches the most patient ones (field heuristic: pages with one bottom CTA are a recurring conversion finding in audits).

### Step 7: Multi-area services: region and city pages

For a service business covering several cities, build a hub-and-spoke structure:

1. One parent region page targeting "service + region".
2. One child city page per city with real search demand, targeting "service + city".
3. Parent links to all children; each child links back to the parent and to the main service page.

The parent region page covers: the full city list with links to every child page, region-wide proof (total clients, years in the region), how the business covers the territory (dispatch, travel times, local teams), and a region-level FAQ.

Each city page must contain genuinely unique content: testimonials from clients in that city, completed projects with local photos, city specifics (neighborhoods served, response times, local regulations or permits), local phone number if one exists. Apply the local keyword pattern on every city page: city in the title, URL, H1, meta description, first paragraph, and image alts.

**Explicit Google guidelines risk:** generating city pages by find-and-replace on the city name produces doorway pages, which violate Google's spam policies and can trigger manual actions (measured: Google spam policies, see Sources). The test: put two city pages side by side; if only the city name differs, they are doorways. Programmatic generation is acceptable only when each page receives unique local substance. If a city has nothing unique to say and no demand, do not create the page.

### Step 8: Add the GEO layer

Apply every item in the GEO layer section below before publishing. Service pages are no longer ranked only by Google; they are quoted by assistants.

### Step 9: Internal links and schema

- Link to the new page from the homepage, the services hub, relevant blog posts, and the footer if the service is core. Orphan money pages are a recurring audit finding (field heuristic).
- Use descriptive anchor text containing the service keyword, never "click here" or "learn more" alone.
- Add a breadcrumb (Home, then Services, then this service) so users and crawlers see the hierarchy.
- Add Service or LocalBusiness schema, Person schema for the founder, Organization with sameAs, and FAQPage markup. Implementation details and eligibility rules: seo-schema-markup skill.

### Step 10: Final QA

Run the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py) on the published URL to verify title, H1, heading structure, word count, internal links, and schema presence. Then check every row of the Rules and thresholds table manually.

## Rules and thresholds

| Rule | Threshold | Evidence level |
|---|---|---|
| One service = one page | No exceptions for distinct SERPs | Field heuristic, most common audit finding |
| Text volume | 750+ words floor; real target = top 3 competitor benchmark | Field heuristic |
| Title | Keyword first + brand, about 50-60 characters | Display heuristic + Google title link docs |
| H1 | Exactly one, contains the service keyword | Field heuristic |
| Meta description | Handwritten, 160 characters or fewer | Display heuristic |
| Slug | Contains the keyword, no filler words | Field heuristic |
| First paragraph | Keyword (+ city) in the first 100 words | Field heuristic |
| FAQ | 3+ questions from People Also Ask + sales objections | Field heuristic |
| CTA | Above the fold + after each major section | Field heuristic |
| Founder block | Real photo, real name, real story; never stock | Field heuristic + E-E-A-T (measured) |
| Reviews | First name + situation + problem + result; video beats text | Field heuristic |
| Pricing | Price or range in plain HTML text | Field heuristic |
| City pages | Unique local substance per page, never find-and-replace | Google spam policies (measured) |
| Related articles | 2-3 supporting posts linked at the bottom, linking back | Field heuristic |

## GEO layer

AI assistants now recommend providers directly: "best CRO agency for Shopify", "recommend a dentist in Geneva", "who can redesign my restaurant website". The answer is assembled from pages the assistant can read and trust. A service page earns those citations when it is self-sufficient: a model reading it in isolation can extract who the provider is, what exactly they do, for whom, how the process works, what it costs, and why they are credible.

Apply all of the following:

1. **Make the page self-sufficient.** Proof, process, FAQ, and price or price range must live in the page's HTML text, not in a PDF, an image, or a "contact us for pricing" dead end. Product and service pages account for roughly 13.7% of pages cited by AI assistants in a large citation analysis (measured: almcorp.com/blog/ai-citations-listicles-articles-product-pages/), so money pages do get quoted, but only when they contain quotable substance.
2. **Write each H2 of the text block as a real question with a direct answer.** Open every section with a 2-4 sentence answer a model can lift verbatim, then elaborate. Full passage-level writing rules: geo-visibility skill.
3. **Add sourced statistics and expert quotations to the text block.** In the GEO benchmark, adding quotations lifted generative visibility by up to 41% and adding statistics by up to 32% on the benchmark's visibility metrics (measured: Princeton GEO study, arxiv.org/abs/2311.09735). Cite real sources; invented numbers destroy trust with both readers and models.
4. **Make E-E-A-T machine-readable.** Person schema for the founder (name, jobTitle, sameAs to LinkedIn), Organization schema with sameAs to every official profile. Implementation: seo-schema-markup skill.
5. **State facts in stable, extractable sentences.** "Dupont Plomberie serves Lyon and 12 surrounding cities, with a response time under 60 minutes" is citable; a hero animation saying "We move fast" is not.
6. **Check AI crawler access.** GPTBot, ClaudeBot, PerplexityBot and similar agents must be able to fetch the page; rendering and robots rules live in the seo-technical skill. Measuring whether assistants actually cite the page: geo-tracking skill.

## Output format

**When creating or rewriting a page**, deliver in this order:

1. Target keyword, SERP intent read, and competitor benchmark summary (top 3: word count, sections, proof).
2. Metadata table: title, H1, slug, meta description, first-paragraph keyword placement.
3. Full page draft, block by block in wireframe order, with heading levels marked (H1, H2, H3) and CTA positions flagged.
4. FAQ: 3-5 questions with 2-4 sentence answers.
5. Internal link plan: links in, links out, the 2-3 supporting blog posts (existing or to be written).
6. Schema recommendations (types only; implementation via seo-schema-markup).
7. GEO checklist pass: confirm each of the 6 GEO layer items.

**When auditing an existing page**, deliver:

1. A gap table:

| Wireframe block | Present | Gap | Fix | Priority |
|---|---|---|---|---|
| 6. SEO text block | Partial | 280 words vs 1600 avg in top 3, no pricing | Rewrite to question-form H2s, add price range | High |
| 8. FAQ | No | Zero questions answered on page | Add 4 questions from People Also Ask | Medium |

(Example rows shown; fill all 9 blocks.)

2. A thresholds check against the Rules and thresholds table (word count vs competitor benchmark, metadata pattern, CTA placement).
3. The GEO layer checklist with pass/fail per item.
4. A prioritized fix list: high (blocks ranking or conversion), medium, low.

## Common mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| One page listing all services | Diluted relevance, wins no SERP | One page per service + hub page |
| Title like "Services \| Brand" | Carries zero keyword signal | Service keyword first, brand last |
| Features instead of benefits | Buyer must translate, most will not | Rewrite every feature as the outcome obtained |
| Stock photos, anonymous team | No E-E-A-T evidence, no human trust | Real founder photo + named story |
| 250 words vs 1500-word competitors | Outgunned on coverage | Benchmark top 3, close the gap |
| Single CTA at the bottom | Misses every early-ready visitor | CTA above the fold + after each major section |
| City pages by find-and-replace | Doorway pages, Google spam policy violation | Unique local proof per city or no page |
| Vague testimonials ("Great service!") | Zero credibility, zero citability | First name + situation + problem + result |
| No price information | Loses the "how much" SERP and AI answers, attracts unqualified leads | Price or range in plain HTML |
| Self-serving review schema | Ineligible per Google guidelines, wasted or risky markup | Mark up reviews only where eligible (seo-schema-markup) |
| Text block behind JS tabs or accordions | Content may not be rendered or weighted | Server-rendered visible text (seo-technical) |
| FAQ written for markup, not objections | Answers nothing a buyer asks | Source questions from People Also Ask + sales calls |

## Sources

- GEO: Generative Engine Optimization, Aggarwal et al., Princeton et al.: arxiv.org/abs/2311.09735 (measured: +41% quotations, +32% statistics on benchmark visibility metrics)
- Share of AI citations going to product and service pages (13.7%): almcorp.com/blog/ai-citations-listicles-articles-product-pages/ (measured)
- Google spam policies, doorway pages: developers.google.com/search/docs/essentials/spam-policies (official)
- Google Search Quality Rater Guidelines, E-E-A-T: static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf (official)
- Google title link documentation: developers.google.com/search/docs/appearance/title-link (official)
- Google FAQ rich results restriction, August 2023: developers.google.com/search/blog/2023/08/howto-faq-changes (official)
- Google review snippet guidelines (self-serving reviews ineligible): developers.google.com/search/docs/appearance/structured-data/review-snippet (official)
- Field heuristics: 115+ real agency audits of service-business websites, 2024-2026 (observational, labeled as such throughout)
