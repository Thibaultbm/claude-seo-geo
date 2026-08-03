# Page Type Matrix

The block list for every page type, in page order, with a level. Companion to SKILL.md phase 3.

Which page types a given site needs, the archetype-specific types (blog hub, call, author, free tool, wall of love, affiliate, 404, marketplace listing, top 10, login), and the site-wide header and footer rules live in `site-archetypes.md`. Read that first when auditing a whole site; read this file when auditing a page.

Levels:

- **R (required)**: a page of this type without it is incomplete. Its absence goes in the report as a gap every time.
- **W (recommended)**: present on the pages that win the query. Absent is a gap unless there is a documented reason.
- **O (optional)**: raises the ceiling when the business has the material. Absent is not a finding.

"Why" states the job the block does. When two audiences are named, the block earns its place with both a human buyer and an AI assistant, which is why it survives layout pressure.

Every type below assumes the universal baseline is already true. Check it once per page, before the type-specific list.

## Universal baseline (all types)

| Block | Level | Why |
|---|---|---|
| Single H1, matching the page intent | R | One page, one subject; multiple H1s split the signal |
| Title, meta description, clean descriptive slug | R | The click surface; a descriptive slug is a retrieval signal for assistants |
| Content present in raw HTML, not JS-injected | R | AI crawlers do not execute JavaScript, so client-rendered blocks do not exist for them |
| Answer-first opening: the page's core promise in the first 100 words | R | Both the skimmer and the extractive model read the top first |
| Heading hierarchy without level jumps | R | The outline is how a model segments the page into quotable passages |
| Real images with descriptive alt text | R | Trust for humans, context and accessibility for machines |
| At least one clear CTA, repeated after long sections | R | A page with no next step converts nothing |
| Internal links out to the parent and to siblings | R | Crawl path, topical context, and the anchor text is a ranking signal |
| Header and footer navigation, reachable in under 3 clicks from home | R | Orphan pages do not rank |
| Organization schema sitewide, page-type schema per page | W | Entity clarity; see seo-schema-markup |
| A visible freshness signal on anything time-sensitive | W | Assistants prefer content that proves it is current |
| Mobile layout that keeps the same content as desktop | R | Mobile-first indexing judges the mobile HTML |

## 1. Product page

Deep copywriting spec: `seo-content-product-page/references/product-page-blueprint.md`.

| # | Block | Level | Why |
|---|---|---|---|
| 1 | Breadcrumb (Home > Category > Sub > Product) | R | Orientation, crawl path, BreadcrumbList anchor |
| 2 | H1 product name + star rating and review count beside it | R | The rating is the strongest objection killer, and most visitors never scroll to the reviews |
| 3 | Photo gallery: front, back, detail, scale or in-use | R | Trust at the decision point, and feed compliance |
| 4 | Buy box: price as HTML text, currency, variants, add to cart | R | A price in an image or in JavaScript is not quotable by an assistant |
| 5 | Reassurance badges: payment, delivery time and cost, returns window | R | The three live objections at the moment of decision |
| 6 | Benefit bullets, 3 to 5 one-line outcomes | R | Skimmers decide here; assistants lift these lines verbatim |
| 7 | Unique description, 150 to 200+ words, benefits then specs in use | R | The ranking surface of the page; never the manufacturer text |
| 8 | Spec table, every measurable attribute | R | Extraction material for assistants and comparison shopping |
| 9 | FAQ, 3+ questions, 40 to 80 word answers | R | Long-tail capture, objection handling, AI extraction |
| 10 | Reviews list, server-rendered, story format | R | Social proof depth, long-tail vocabulary, Review markup source |
| 11 | Comparison table versus the 2 closest alternatives | W | The passage format quoted in "best X" answers |
| 12 | Definitions block, about 5 technical terms | W | Qualifies non-expert buyers, adds topical depth |
| 13 | Cross-links: parent collection, sister products, supporting guide | R | Internal linking and crawl depth |
| 14 | Stock and availability status, mirrored in Offer markup | W | Availability contradictions get products dropped from shopping surfaces |
| 15 | Video: product in use or a video review | O | Outperforms text for conversion when it exists |
| 16 | Size, fit or compatibility guide | O | Kills the single biggest return driver in apparel and parts |

## 2. Collection or category page

Deep spec: `seo-content-collection-page/`.

| # | Block | Level | Why |
|---|---|---|---|
| 1 | Breadcrumb | R | Hierarchy for users and bots |
| 2 | H1 naming the category as buyers name it | R | The head term of the page |
| 3 | Intro text above the grid, 2 to 4 sentences | R | Tells both audiences what this category contains before the grid |
| 4 | Product grid with real photos, names, prices as text | R | The reason the page exists |
| 5 | Filters and sorting, with crawl control on the parameter URLs | R | Usability, and uncontrolled facets explode the crawl budget |
| 6 | Buying guide block below the grid, 400-800 words (spec: seo-content-collection-page) | R | The only real ranking surface a grid page has |
| 7 | Sub-category links | R | Distributes authority down the silo |
| 8 | FAQ about the category, 3+ questions | R | Captures the informational half of category intent (spec: seo-content-collection-page) |
| 9 | Definitions of category-specific terms | W | Topical depth on a page that is otherwise mostly product tiles |
| 10 | Cross-links to related categories and to the guides | R | Silo cohesion |
| 11 | Pagination handled so page 2+ stays crawlable | R | Deep products go orphan otherwise |
| 12 | Comparison of the top items in the category | O | Serves "best X" queries directly |

## 3. Service page

Deep spec: `seo-content-service-page/references/service-page-wireframe.md` (9-block wireframe).

| # | Block | Level | Why |
|---|---|---|---|
| 1 | Hero: H1, who it is for, one proof element, primary CTA | R | The promise and the qualifier in one screen |
| 2 | First paragraph carrying the primary keyword (and city, if local) | R | Relevance in the first 100 words |
| 3 | Client logos, certifications, review platform rating | W | Borrowed credibility before any claim |
| 4 | Benefits, 3 to 6 cards, outcomes not features | R | The buyer buys the outcome |
| 5 | Process, numbered steps with durations | R | Removes the fear of the unknown, the top objection in services |
| 6 | Founder or team block with a real photo and a real name | R | The E-E-A-T signal that separates a real business from a template |
| 7 | Deep SEO text block, 750+ words, question-shaped H2s | R | The ranking surface; benchmark the top 3 competitors |
| 8 | Price or price range in plain text | R | The most searched and least answered question in services |
| 9 | Reviews with first name, situation, problem, result | R | Specific proof beats generic praise |
| 10 | FAQ, 3+ real buyer questions | R | Long-tail capture and objection handling |
| 11 | Case study or before and after | W | The strongest asset a service business owns |
| 12 | Coverage area or eligibility (who it is for and not for) | W | Qualifies out bad leads and captures local intent |
| 13 | CTA repeated after each major section | R | Long pages lose the decision moment |
| 14 | Cross-links to related services and the parent hub | R | Silo, and it prevents cannibalization between sibling services |

## 4. Location page

Deep spec: `seo-local/references/location-page-template.md`.

| # | Block | Level | Why |
|---|---|---|---|
| 1 | H1 with service and city | R | The local head term |
| 2 | Full NAP, byte-identical to the Google Business Profile | R | Inconsistent NAP is the most common local ranking blocker |
| 3 | Opening hours matching the profile | R | Contradiction with the profile erodes both |
| 4 | Embedded map | R | Orientation and a local relevance signal |
| 5 | Services offered at this location, with prices in text | R | The commercial content of the page |
| 6 | Areas and neighborhoods served | R | Captures the long tail around the city term |
| 7 | Real photos: storefront, team, local jobs | R | Stock photos actively hurt local trust |
| 8 | Reviews from customers of this location | R | Local proof, not corporate proof |
| 9 | Local proof: projects, partnerships, local press | W | Ties the entity to the place |
| 10 | FAQ, 3+ questions buyers in this city ask | R | Local long tail |
| 11 | LocalBusiness schema matching the profile exactly | R | Entity resolution |
| 12 | Link to and from the Google Business Profile | R | Closes the loop between the two assets |
| 13 | Cross-links to the services hub and sibling cities | R | Prevents a set of orphan city pages |
| 14 | Parking, access, public transport | O | Real question, rarely answered, easy differentiation |

## 5. Comparison and alternatives page

Deep spec: `seo-content-comparison-page/`.

| # | Block | Level | Why |
|---|---|---|---|
| 1 | H1 naming both sides exactly as searched ("X vs Y", "X alternatives") | R | These are exact-match queries; the H1 must match the phrasing |
| 2 | Verdict in the first 100 words: who each option is for | R | The passage an assistant quotes; burying it forfeits the citation |
| 3 | Comparison table, feature by feature, both sides | R | The single most extractable block on the page |
| 4 | Pricing of every option compared, as HTML text, with the date checked | R | The most compared dimension, and the fastest to go stale |
| 5 | "Best for" verdict per option or per use case | R | Turns one page into answers for many intent variants |
| 6 | Honest limitations of your own option | R | The credibility mechanism; a page where you win every row is discounted by readers and models |
| 7 | Per-option detail sections, one H2 each, same criteria in the same order | R | Comparability; jagged criteria read as bias |
| 8 | Migration or switching section | W | Captures the highest-intent moment of the query |
| 9 | FAQ, 3+ questions, including the uncomfortable ones | R | "Is X better than Y", "is X worth it", "can I switch" |
| 10 | Methodology and date: what was tested, when, how | R | Provenance is what makes a comparison quotable rather than promotional |
| 11 | Definitions of the criteria being compared | W | A criterion nobody understands cannot persuade |
| 12 | Cross-links to each option's own page and to the pricing page | R | Routes the decided visitor to conversion |
| 13 | Real screenshots of each option | W | Proof the comparison was actually performed |
| 14 | Author with demonstrable experience of both options | W | E-E-A-T on a page whose whole value is judgment |

## 6. Audience or segment page

Same product, one customer type ("for agencies", "for freelancers", "for e-commerce"). Deep spec: the segment section of `seo-content-comparison-page/`.

| # | Block | Level | Why |
|---|---|---|---|
| 1 | H1 naming the segment as the segment names itself | R | Recognition in the first second, and the exact query |
| 2 | The segment's problem in its own vocabulary, first 100 words | R | The proof that the page was written for them and not templated |
| 3 | Segment-specific benefits, not the generic feature list | R | Otherwise it is a duplicate of the homepage with a swapped title |
| 4 | Use case or workflow as this segment actually works | R | The block that makes the page non-duplicable |
| 5 | Proof from the same segment: logos, reviews, case study | R | Social proof only works from a recognizable peer |
| 6 | Pricing or plan relevant to this segment | W | Segments differ on what they can spend and on what unit |
| 7 | Objections specific to this segment, answered | R | Each segment has its own blocker, and it is rarely price |
| 8 | FAQ in the segment's vocabulary | R | Long tail, and it keeps the page distinct from its siblings (spec: seo-content-comparison-page) |
| 9 | Integrations or constraints that matter to this segment only | O | The detail that closes a technical buyer |
| 10 | CTA phrased for this segment | R | "Book a team demo" and "start free" are different asks |
| 11 | Cross-links to sibling segment pages and the main product page | R | Lets a mis-routed visitor self-correct, and prevents cannibalization |

Duplication is the failure mode of this page type. If two segment pages differ only by find-and-replace on the segment name, they compete with each other and neither ranks. The test: could a reader from segment A tell that the segment B page was not written for them, within the first paragraph? If not, merge the pages.

## 7. Blog article

Deep spec: `seo-content-blog/`.

| # | Block | Level | Why |
|---|---|---|---|
| 1 | H1 matching the query, not a clever title | R | Relevance beats wordplay on informational intent |
| 2 | Answer-first summary in the first 100 words | R | The passage extracted into AI answers and featured snippets |
| 3 | Table of contents on long articles | W | Navigation, and it exposes the outline to models |
| 4 | Question-shaped H2s | R | Matches how queries and prompts are phrased |
| 5 | At least one sourced statistic with an outbound link | R | Statistics and citations measurably raise generative visibility |
| 6 | At least one quotation from a named expert or practitioner | W | Same mechanism as the statistic |
| 7 | Table or comparison of the options discussed | W | The most extractable format in a body of prose |
| 8 | Original material: data, screenshots, photos, examples | R | The only durable defense against being outranked by the same rewrite |
| 9 | Author block with real credentials | R | E-E-A-T |
| 10 | Published and updated dates, visible | R | Freshness assessment for readers and assistants |
| 11 | FAQ at the end | R | Captures related long-tail queries on the same URL (spec: seo-content-blog, skeleton element 11) |
| 12 | Cross-links to the money pages the article supports | R | An article that links to nothing commercial earns nothing |
| 13 | Definitions of jargon used | O | Widens the audience beyond experts |

## 8. Homepage

| # | Block | Level | Why |
|---|---|---|---|
| 1 | H1 stating what the business does and for whom, in plain words | R | The most common homepage failure is a slogan where the offer should be |
| 2 | Sub-headline naming the audience and the outcome | R | Qualifies the visitor in one line |
| 3 | Primary CTA above the fold | R | The homepage is a router; the router needs a default route |
| 4 | Social proof within the first screen: logos, rating, client count | R | Credibility before claims |
| 5 | Offer overview linking to every money page | R | The homepage is the strongest internal link source on the site |
| 6 | Benefits or problems solved, 3 to 6 | R | The reason to keep scrolling |
| 7 | How it works, in steps | W | Reduces the perceived risk of a first contact |
| 8 | Proof: reviews, case studies, numbers | R | Specific proof, not adjectives |
| 9 | Descriptive text block, 300+ words | W | A homepage of headlines alone gives models nothing to read |
| 10 | Who it is for and not for | W | Qualification improves both conversion and relevance |
| 11 | Secondary CTA for the not-ready visitor | W | Newsletter, guide, call: capture instead of losing |
| 12 | Organization schema with sameAs to every official profile | R | Entity resolution across the web |
| 13 | Trust and legal links in the footer | R | Legitimacy signal, and a legal requirement in most markets |
| 14 | Contact details reachable from the homepage | R | A business with no visible way to reach it reads as a shell |

## 9. Pricing page

| # | Block | Level | Why |
|---|---|---|---|
| 1 | H1 naming pricing plainly | R | Exact intent, no cleverness |
| 2 | Prices as HTML text, with currency and billing period | R | A price in an image or behind a script cannot be quoted or compared |
| 3 | Plan comparison table, same criteria per plan | R | The extractable block; also how buyers actually decide |
| 4 | What is included and what is not, per plan | R | Ambiguity here is the top pre-sale support ticket |
| 5 | Recommended plan marked, with who it is for | W | Choice paralysis kills conversion |
| 6 | Total cost clarity: setup fees, overage, minimum term | R | The hidden-cost objection, answered before it forms |
| 7 | FAQ: billing, cancellation, upgrade, refund, taxes | R | Every one of these is a real query and a real blocker |
| 8 | Guarantee, trial or refund terms | W | Risk reversal at the moment of highest hesitation |
| 9 | Social proof near the plans | W | Proof adjacent to the decision, not in a distant section |
| 10 | Contact route for the non-standard case | R | Enterprise and edge cases leave otherwise |
| 11 | Offer or PriceSpecification schema matching the visible prices | W | Machine-readable pricing, only if it mirrors the page |
| 12 | Date or version of the current pricing | O | Prevents stale prices being quoted back at you |

If prices genuinely cannot be published, publish the price drivers and a range instead. A pricing page with no number is the most abandoned page type there is.

## 10. About page

| # | Block | Level | Why |
|---|---|---|---|
| 1 | H1 with the company name and what it does | R | This page is the entity anchor of the whole site |
| 2 | The story: why the business exists, since when | R | The one page where narrative outperforms optimization |
| 3 | Real photos of real people | R | Stock photography on an about page is self-defeating |
| 4 | Named team with roles and credentials | R | The core E-E-A-T page; it validates every author byline elsewhere |
| 5 | Verifiable facts: founding year, size, locations, registration | R | What an assistant reuses when asked who the company is |
| 6 | Numbers that prove scale: clients served, years, volume | W | Concrete beats "leading provider of" |
| 7 | Press, awards, certifications, memberships, with links | W | Third-party validation is the strongest entity signal |
| 8 | Values or method, stated concretely | O | Only if it says something a competitor could not copy |
| 9 | Contact route and address | R | Legitimacy |
| 10 | Organization + Person schema, sameAs to LinkedIn and profiles | R | Ties the site to the entity graph |
| 11 | Cross-links to services or products and to careers | W | The about page receives more traffic than owners expect |

Consistency matters more than prose here: the company name, one-line description, founding year and location must match across the site, LinkedIn, directories and review platforms, or the entity fragments.

## 11. Contact page

| # | Block | Level | Why |
|---|---|---|---|
| 1 | H1 naming contact plainly | R | Exact intent |
| 2 | Every contact channel as text, not images: phone, email, address | R | A phone number in an image is unusable on mobile and invisible to machines |
| 3 | `tel:` and `mailto:` links | R | One tap to convert |
| 4 | Form with the minimum viable field count | R | Every extra field costs completion |
| 5 | Expected response time | R | The unanswered question of every contact page |
| 6 | Opening hours | W | Sets expectations, and it is a local signal |
| 7 | Map, if there is a physical location | W | Orientation |
| 8 | Routing: which channel for which need | W | Sends support away from sales and vice versa |
| 9 | Confirmation state after submission | R | A form that appears to do nothing loses the lead twice |
| 10 | Link to the FAQ or help center | W | Deflects the answerable questions |
| 11 | ContactPoint schema | O | Minor, but cheap |

## Cross-type rules

1. One intent, one page. If two pages in the matrix would carry the same primary keyword, merge them. Cannibalization costs more than a missing block.
2. Every block must be visible to a human. Blocks that exist only in schema, only in a tab that never renders, or only after JavaScript, do not count as present.
3. The FAQ is the highest-leverage missing block on almost every page type. It appears as required on eight of the eleven types because it is the cheapest way to capture long-tail queries, answer objections, and hand assistants a quotable passage at the same time.
4. Order beats inventory. Decision blocks above the fold, extraction blocks below it. A page with every block in the wrong order still converts badly.
5. Match the depth of the pages that already rank for the query, rather than the numbers in this file. These levels are the floor, not the target.
