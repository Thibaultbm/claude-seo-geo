# Block library: homepage, offer page, about page

Each block: what it contains, the minimum spec, and why it exists. Replace every `{placeholder}` in the language of the site. Facts the owner has not confirmed stay as `{to confirm}`.

The IDs match the spec tables in `../SKILL.md` (Phase 1): HOME-01 to HOME-18 are the homepage blocks, OFFER-01 to OFFER-17 the sales page sequence. The cross-cutting rows (HOME-19 to HOME-33, OFFER-18 to OFFER-20) and the common rows C-01 to C-26 (`skills/seo-geo-audit/references/common-page-spec.md`) apply to every block below.

## 1. Homepage

| ID | Block | Minimum spec | Why |
|---|---|---|---|
| HOME-01 | Header | Logo, 4-6 menu items (offers, results, about, blog, contact), one CTA button in a contrasting color | The CTA is visible on every scroll position once the header is sticky |
| HOME-02 | Hero | H1 = **category term** + outcome; sub-line with one proof number; primary CTA (the main conversion) and secondary CTA (low commitment: free training, guide, quiz); hero image of the real founder or product, eager-loaded | The first screen answers what, for whom, why trust, what next |
| HOME-03 | Proof strip | Rating with platform and count (Trustpilot, Google), client count, years, press or partner logos | Borrowed authority before any claim |
| HOME-04 | Problem | 3-6 pains in the buyer's own words (from calls, comments, reviews), each with what changes | Recognition keeps the right reader scrolling |
| HOME-05 | Named method | The method has a name and 3-5 pillars, each with one line and one number | A named method is what competitors cannot copy and what AI engines quote as an entity |
| HOME-06 | Offer routing | One card per offer: who it is for, format, price or "from", link to its page | Routes the homepage authority to the money pages; the audit flags `home_no_money_links` |
| HOME-07 | Results | 3-6 results: first name, starting point, result, timeframe; screenshots or graphs; link to full case studies | Specific outcomes are the strongest conversion and citation material |
| HOME-08 | Testimonials | Video testimonials (YouTube embed with a text summary under each) plus written ones with photo | Video proves the person exists; the text summary makes it readable by crawlers |
| HOME-09 | Founder | Real photo, 80-150 words with verifiable credentials (years, track record, results, press), link to the about page, real social profiles | E-E-A-T: who stands behind the promise |
| HOME-10 | Comparison table | This offer versus the usual alternatives (free content, other programs, doing it alone): 5-8 criteria, an HTML table | Tables are the most extracted format in AI answers and the most direct answer to "why you" |
| HOME-11 | For / not for | Two short lists | Qualification raises conversion and lowers refunds |
| HOME-12 | Guarantee | Exact terms (duration, condition), when one exists | Risk reversal; vague guarantees read as traps |
| HOME-13 | Lead magnet | Free training, guide, checklist, quiz or tool with an email form | Captures the 95% not ready to buy today |
| HOME-14 | Latest articles | 3 cards with cover image, title, excerpt, date | Shows the site is alive and links the blog from the strongest page |
| HOME-15 | FAQ | 8-12 real objections answered in 2-4 sentences, `<details>` accordions with the text in the HTML | Objections handled in writing replace a sales call; question-answer pairs are extracted by AI engines |
| HOME-16 | Descriptive block | 300+ words of prose on the category term, phrased as the question buyers ask, with bold on the key facts | Gives retrieval and ranking real text when the rest of the page is short blocks |
| HOME-17 | Final CTA | Promise, one proof, one button | The last conversion surface |
| HOME-18 | Footer | Real social profiles, contact, legal pages, disclaimers, sitemap-level links | Entity consistency and trust; never placeholder icons |

FAQ (HOME-15, OFFER-16): write the objections, not definitions. Typical objection set for a coaching or training offer:

- How long before the first results, and what results are realistic?
- How much time per week does it take?
- Is it for beginners, intermediate or advanced?
- How is it different from free content on YouTube or other programs?
- How much does it cost, and are there payment options?
- What if it does not work for me (guarantee, refund)?
- How is the support delivered (calls, group, community, replies)?
- How do I join (application, call, direct purchase)?

## 2. Flagship offer page (sales page)

| ID | Block | Minimum spec |
|---|---|---|
| OFFER-01 | Hero | H1 = offer name + outcome; sub-line with the promise and timeframe; video sales letter or founder video (YouTube embed, with chapters or a text summary); primary CTA |
| OFFER-02 | Proof strip | Rating, client count, result headline |
| OFFER-03 | The problem and the cost of staying put | Buyer's words, with numbers |
| OFFER-04 | The method | Named, 3-5 pillars, each linked to what the client does with it |
| OFFER-05 | Program contents | Modules or phases listed with titles and one-line outcomes; number of lessons, hours, live sessions |
| OFFER-06 | Format and workload | Duration, hours per week, live versus recorded, access length, community, support channels and response times |
| OFFER-07 | Results | Case studies with before, after, timeframe, screenshots or graphs |
| OFFER-08 | Testimonials | Video and text, named |
| OFFER-09 | The coach or team | Photo, credentials, link to the about page |
| OFFER-10 | Comparison table | Versus alternatives, 5-8 criteria |
| OFFER-11 | Price and payment | Price as HTML text (or "from"), payment plans, what is included |
| OFFER-12 | Guarantee | Exact terms |
| OFFER-13 | Bonuses | Only real ones, each with its standalone value |
| OFFER-14 | Process to join | 3-4 numbered steps (apply, call, onboarding) with durations |
| OFFER-15 | For / not for | Two lists |
| OFFER-16 | FAQ | 10-15 objections |
| OFFER-17 | Final CTA | Promise, proof, button |

Schema (OFFER-19): Course (curriculum program) or Service (one-to-one coaching) or Product with Offer (digital product), plus BreadcrumbList and the Organization reference.

## 3. About or founder page ("Mon parcours", "Qui suis-je")

The entity anchor and, on a one-expert site, the author page every article links to. This is the ABOUT block list of the spec; the generic about wireframe and its checks are owned by seo-page-sections (`references/transverse-pages.md`, About page), audited with `section_audit.py --type about`.

- H1: full name + role ("Vincent Bellepaume, coach poker et fondateur de La Salle du Temps").
- Answer-first lead: what the person does, since when, for whom, one proof number.
- Facts block, the one assistants reuse: years of practice, results with sources, clients helped, locations, certifications, press.
- Story: honest, specific, with dates.
- Proof: press, partnerships, public profiles that confirm the claims (for players, coaches or athletes: the public results databases of the field).
- Social profiles with real URLs.
- The author's articles (cards with covers) and a CTA to the offer.
- Schema: ProfilePage with mainEntity Person (same `@id` as article bylines), `sameAs` to every real profile.

## 4. Conversion blocks worth adding when the benchmark shows them

| Block | Use when | Spec row |
|---|---|---|
| Quiz or self-assessment ("What is your level?") | The audience does not know which offer fits; it doubles as a lead magnet | HOME-13 |
| Free tool (calculator, chart, template, checker) | The niche has a recurring computation or reference table; tools earn links and branded searches | HOME-13, Phase 3 information gain |
| Glossary | The niche has jargon; one page per important term ranks on definitions and feeds AI answers | seo-content-blog |
| Community proof (Discord, group size, live events) | The offer includes a community; show the number of members and activity | HOME-03, OFFER-06 |
| Press or "as seen on" | Real mentions exist; link each to the source | HOME-03 |
| Results dashboard or graph | Results are trackable over time; one honest graph beats ten adjectives | HOME-07, OFFER-07 |
| Application form instead of checkout | High-ticket offer; the form qualifies and sets expectations | OFFER-14 |
| Podcast or YouTube series | Regular video or audio exists; embed the latest episodes with text summaries | HOME-08 |
| Sticky mobile CTA bar | Long pages on mobile; one button always reachable | HOME-01 |

## 5. What 14 coaching and training sites actually ship (benchmark, October 2026)

Raw HTML of the homepage, sales page, blog hub and one article of 10 French and 4 English poker coaching and training sites (the niche of the case study that triggered this skill). The frequencies show what a buyer in a coaching or training niche sees elsewhere; the rules are not poker-specific. The counts are measured (raw HTML read in October 2026); Phase 3 of `../SKILL.md` uses them to tell table stakes from information gain.

| Element | Sites with it | Rule for any coaching or training site | Spec row |
|---|---|---|---|
| JSON-LD graph (Organization + Person + Article + BreadcrumbList) | 11 / 14 | Mandatory; the client without it is in the bottom 3 | HOME-31, OFFER-19 |
| Price shown | 12 / 14 | Show it, with instalments or annual options when they exist (5 / 14 do) | HOME-24, OFFER-11 |
| Discord or community | 12 / 14 | Show the community, its size and how members interact | HOME-03, OFFER-06 |
| Lead magnet (free course, video, guide) | 11 / 14 | One entry offer on every page: hero secondary CTA, mid-article block, footer | HOME-13 |
| Blog hub with cover images | 10 / 11 blogs | Every card has its cover | HOME-14, seo-content-blog |
| Blog categories or topic hubs | 9 / 11 blogs | Each article links back to its hub ("Parcours associé") | seo-content-blog |
| In-article CTA block | 9 / 11 blogs | Soft lead magnet mid-article, the offer at the end | seo-content-blog |
| Visible author and date on articles | 8 / 11 blogs | Byline with photo, dates, reading time | seo-content-blog |
| Comparison against alternatives (cost table, "versus a private coach") | 8 / 14 | A table of the real costs of each alternative | HOME-10, OFFER-10 |
| Curriculum by module or week | 7 / 14 | Modules with outcomes and video or hour counts | OFFER-05 |
| Responsible-play notice on a gambling topic | 7 / 14 | Footer notice, age limit, helpline, dedicated page | HOME-29 |
| Free interactive tools (calculators, charts, trainers) | 6 / 14 | One indexable page per tool, with explanatory text | Phase 3 information gain |
| Discovery call or application | 5 / 14 | Numbered process, booking link, what happens on the call | OFFER-14 |
| Rating with review count | 5 / 14 | Platform, count, date read | HOME-25 |
| Numbers-based proof (results ticker, winrate, results graph, named students with figures) | 4 strong / 14 | The strongest differentiator; most sites stay vague | HOME-07, HOME-22 |
| Glossary | 4 / 14 | One page per term; link the first mention of each term per article automatically | seo-content-blog |
| Coach linked to a checkable third-party profile | 4 / 14 | Link and `sameAs` to the field's public records | HOME-26 |
| Money-back guarantee | 3 / 14 (all English) | A real guarantee is a differentiator in French markets | HOME-12, OFFER-12 |
| Sticky table of contents in articles | 1 / 11 blogs | Rare: an easy differentiator | seo-content-blog |

Tactics worth copying, seen on the best of them:

- A "sources consulted" section that says what each source supports, plus an editorial transparency note.
- A key-takeaways box under the article title (the answer-first block, labeled).
- A footer with "editorial policy", "press" and "figures and method" pages (HOME-29).
- Persona-based offer cards ("I am stuck at my level" / "I aim for the top") instead of plan names (HOME-06).
- A results ticker or graph of real student results, each with a name (HOME-07).
- A low-price entry product or a free short course as the first step.
- Social-proof counters (subscribers, downloads, members) with real numbers (HOME-03).
- Guest articles by named practitioners, grouped into a series.
- A referral page for existing clients.
- Members-only final section on some articles, with the free part complete on its own.
