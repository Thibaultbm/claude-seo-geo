---
name: seo-local
description: "Run spec, audit, competitor benchmark and build for local visibility, on the two assets a local business owns: the location page and the Google Business Profile, plus reviews and NAP citations. Spec: LOC, GBP, REV and CIT requirements with IDs. Audit: seo_audit.py and section_audit.py --type location on the page, a manual GBP checklist. Benchmark: the local pack and top organic results for '{service} {city}', their pages via page_benchmark.py, their profiles by hand (categories, review count and velocity, photos, posts). Build: name and category decisions, a 100% complete profile, a review engine with reply templates, NAP consistency, location pages with LocalBusiness schema, multi-location and service-area setups, suspended-listing reinstatement, then a scripted acceptance re-run. Use for GBP, Google Maps, the local pack, 'best [trade] in [city]' AI answers, reviews and star ratings, citations, a business not showing on Maps, or a suspended listing."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "2.0.0"
---

# Local SEO: Google Business Profile, Reviews, Citations and Local Pages

Local SEO decides who appears when a buyer searches "plumber near me", opens Google Maps, or asks an AI assistant for "the best dentist in Geneva". Three surfaces matter: the local pack (Maps results inside the SERP), localized organic results, and AI assistant recommendations. They feed on overlapping signals: the Google Business Profile, reviews, the linked website, and the consistency of the business entity across the web. Local visibility fails when the profile is half empty, the reviews trickle in bursts, the NAP differs from one directory to the next, and the profile links to a homepage instead of a real location page.

This skill treats two assets as the "pages" it owns, the **location page** on the site and the **Google Business Profile**, and runs the four-phase standard (spec, audit, benchmark, build) on both, with the review program and the NAP citations as shared requirements. The methodology combines two evidence levels, labeled throughout:

- **Field heuristic**: rules derived from 115+ real agency audits of local and service businesses (2024-2026). Consistently observed, not lab-measured.
- **Measured**: claims backed by a published study, an industry survey, or official documentation, with the source.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use this skill

Use it to diagnose why a business is invisible in the local pack, set up or complete a Google Business Profile, build a review generation engine, write review replies, plan location pages, structure a multi-city or service-area business, or recover a suspended listing.

Stay in scope. Hand adjacent work to the right skill:

| Task | Skill |
|---|---|
| GBP, reviews, local pack, NAP, location page strategy (this skill) | seo-local |
| Finding and building citation and directory links | seo-backlinks |
| Writing service pages and city pages (copy and wireframe) | seo-content-service-page |
| LocalBusiness schema implementation details | seo-schema-markup |
| Block-by-block gap audit of any page type | seo-page-sections |
| Site crawlability, speed, AI crawler access | seo-technical |
| Local keyword selection | seo-keyword-research |
| Writing rules for AI answer citability | geo-visibility |
| Measuring AI assistant mentions | geo-tracking |
| Full-site audit | seo-geo-audit |

## Phase 1. The spec

Four tables: the location page (LOC), the Google Business Profile (GBP), the review program (REV), and NAP and citations (CIT). Common requirements C-01 to C-26: skills/seo-geo-audit/references/common-page-spec.md. They apply to the location page in full (title, meta, H1, canonical, images, breadcrumb, structured data validity, server HTML, em dashes); the LOC rows below only add what is specific to a local page. "Verified by" is a `seo_audit.py` finding code, a `section_audit.py` block, or "manual".

### Location page (LOC)

One page per establishment. Block order and copy: references/location-page-template.md and the seo-content-service-page skill.

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| LOC-01 | Local keyword pattern: "{service} {city}" as the target keyword | City in title, URL, H1, meta description, first paragraph, one image alt | kw_placement_low, kw_not_in_intro, manual (city in each zone) | The local head term; the placement matrix applied to the place |
| LOC-02 | One page per establishment, linked from the matching profile | 1 page per real location; never one shared "Locations" page for all branches | manual | A shared page lets no branch rank locally |
| LOC-03 | Full NAP, byte-identical to the profile, canonical format | Name, address, phone match GBP character for character; service-area business with a home address keeps it off the page and leads with areas | section_audit "contact_details", manual comparison with GBP | Inconsistent NAP is the most common local ranking blocker (field heuristic) |
| LOC-04 | Opening hours identical to the profile | Same days and times, holiday hours included | section_audit "opening_hours", manual | A contradiction with the profile erodes both |
| LOC-05 | Embedded Google map of the location | 1 | section_audit "map_embed" | Orientation and a local relevance signal |
| LOC-06 | Services offered at this location, with prices | Each service with a price or price range in plain HTML text | section_audit "price_in_text", manual | The commercial content, and the facts assistants quote |
| LOC-07 | Areas and neighborhoods served from this location | Every area actually served, named | manual | Captures the long tail around the city term |
| LOC-08 | Real photos | Storefront, team, completed local jobs; zero stock | section_audit "images", manual | Stock photos actively hurt local trust |
| LOC-09 | Reviews from customers of this location | 3+ shown, each with first name, situation, problem, result; service and city mentioned where natural | section_audit "reviews", manual | Local proof, not corporate proof; feeds AI answers |
| LOC-10 | Local proof | Projects, partnerships, local press mentions (recommended) | manual | Ties the entity to the place |
| LOC-11 | FAQ of local buyer questions | 3+ questions buyers in this city ask | section_audit "faq" | Local long tail |
| LOC-12 | Call to action | Above the fold and after each major section | section_audit "cta" | Shortens the path to a call or booking |
| LOC-13 | LocalBusiness JSON-LD matching the profile exactly | Most specific schema.org subtype; name, address, telephone, geo, openingHoursSpecification, areaServed, url, image, sameAs; no self-serving aggregateRating unless reviews are shown and eligible | schema_none, schema_fields, jsonld_invalid, manual comparison with GBP | Entity resolution for Google and LLMs |
| LOC-14 | Links in the local cluster | Linked from the /locations/ index (multi-location), to the services hub and to sibling city pages | section_audit "internal_links", manual | Prevents a set of orphan city pages |
| LOC-15 | Unique local substance on every city page | A reader of city A can tell in the first paragraph the city B page was not written for them; local reviews, local jobs, neighborhoods, response times | manual | Find-and-replace city pages are doorway pages |
| LOC-16 | Extractable local facts | Response time, team, areas, prices, hours stated as plain sentences | manual (server HTML itself: C-21) | Assistants answering "best [trade] in [city]" lift isolated facts |
| LOC-17 | AI search bots allowed | GPTBot, ClaudeBot, PerplexityBot not blocked | ai_bots_blocked | Removes the page from AI answers |
| LOC-18 | Parking, access, public transport | Stated when there is a storefront (optional) | manual | Real question, rarely answered, easy differentiation |
| LOC-19 | Length | At or above the competitor median from Phase 3; no fixed floor set by this skill | thin_content, page_benchmark.py "words" (C-08) | Coverage the local SERP already rewards |

### Google Business Profile (GBP)

All manual: the profile is checked in the owner's dashboard and on the public listing.

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| GBP-01 | Business name = the exact real-world name | No trade or city added unless they are part of the legal name or signage; trade-off presented, owner decision written | manual | Keywords in the name rank, and also expose the profile to suspension (Step 2) |
| GBP-02 | Primary category | The single most specific category for the money service, revisited quarterly, tested against the pack leaders' | manual | Strongest single relevance signal on the profile (measured: Whitespark survey) |
| GBP-03 | Secondary categories | Every category that genuinely applies, nothing aspirational | manual | Matching surface without guideline risk |
| GBP-04 | Setup type matches reality | Storefront, service-area (address hidden, every city served listed) or hybrid | manual | A wrong setup is a guideline violation or a lost area |
| GBP-05 | One profile per real, staffed location | Verified separately; no duplicates; no virtual office, coworking or PO box presented as a storefront | manual | Guideline violation, suspension and removal risk |
| GBP-06 | Services | Every billable service, each with a description and a price or range | manual | Every filled field is matching surface for queries |
| GBP-07 | Attributes | All that apply (accessibility, payments, amenities) | manual | "Open now", "wheelchair accessible" style queries |
| GBP-08 | Description | 750 characters, plain factual language: services, areas, differentiators; zero em or en dashes | manual | Relevance and the sentence assistants paraphrase |
| GBP-09 | Photos | Real only: storefront, team, work in progress, results; new ones monthly; never stock | manual | Trust; stock signals a shell listing |
| GBP-10 | Hours | Exact, holiday hours included, identical to LOC-04 | manual | Wrong hours cost visits and trust |
| GBP-11 | Phone and website link | Local number; link to the matching location page, never the homepage for a multi-location business | manual | Sends the profile's relevance to the right page |
| GBP-12 | Booking and quote links | Whatever shortens the path to contact | manual | Conversion |
| GBP-13 | Q&A | 5 most-asked buyer questions seeded from the owner account and answered | manual | Transparent and allowed; preempts wrong answers from strangers |
| GBP-14 | Opening date | Set | manual | Longevity feeds prominence |
| GBP-15 | Posts | Weekly to biweekly (offers, completed jobs, seasonal info); expectations capped | manual | Activity signal, low direct ranking impact (field heuristic) |
| GBP-16 | Completeness | 100% of fields, about 1h30 of focused work | manual | Completeness gaps show in the benchmark table in nearly every audit (field heuristic) |

### Reviews (REV)

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| REV-01 | Monthly ask target sized from the gap | (leader count minus current count) / 12 + the leader's monthly pace | manual (Phase 3 table) | Closes the gap within a year; if unrealistic, compete on recency, detail and replies |
| REV-02 | Steady velocity | A few reviews every week, no bursts after silence | manual (review dates) | Bursts look bought to readers and spam filters (field heuristic) |
| REV-03 | Ask at the peak of satisfaction | Same day, when the job is done and the customer says thanks | manual | Asking days later collapses conversion (field heuristic) |
| REV-04 | One-tap path | Short review link (g.page/...), QR code on invoice or counter, same-day SMS or email | manual | Friction kills the ask |
| REV-05 | Reply to every review | 100% reply rate, negatives included; specific to the review, never one pasted text | manual | Every future customer and every AI summary reads the replies |
| REV-06 | Detailed reviews, never scripted | Ask naturally for the service and the city; never write the review for the customer | manual | Customer-written service and city carry the weight; the reply adds a smaller bonus (field heuristic) |
| REV-07 | Zero incentivized, gated, swapped or fake reviews | 0, ever | manual | Google policy and FTC rule (measured): every review or the profile can be wiped |

### NAP and citations (CIT)

| ID | Requirement | Threshold | Verified by | Why |
|---|---|---|---|---|
| CIT-01 | One canonical NAP format | Chosen once ("12 rue de la République" vs "Rue de la République 12", "+33 4 ..." vs "04 ...") | manual | Variants fragment the entity |
| CIT-02 | NAP byte-identical everywhere | Site footer, location pages, GBP, every directory, every social profile; 0 variants | manual scan, section_audit "contact_details" on the site | Google and LLMs cross-check entity facts (industry surveys + field heuristic) |
| CIT-03 | Presence on directories and review platforms assistants quote | Yelp, Trustpilot, Tripadvisor, trade-specific directories, local listings as relevant to the trade | manual (building: seo-backlinks) | More consistent material to cite in "best [trade] in [city]" answers |
| CIT-04 | Local brand mentions | Local press, city blogs, associations, sponsorships, chamber of commerce | manual (outreach: seo-backlinks) | Brand mentions correlate with AI visibility about 3x more than backlinks (measured correlation) |
| CIT-05 | Real social profiles in `sameAs` | Same URLs as the profile and the site (C-20) | social_placeholder, social_missing | Entity consistency |

## Phase 2. Audit the existing page and profile

Run the two scripts on every location page (from the repository root):

```
python3 skills/seo-geo-audit/scripts/seo_audit.py https://example.com/plumber-lyon/
python3 skills/seo-page-sections/scripts/section_audit.py --type location https://example.com/plumber-lyon/
```

Map the output to the spec, then mark every row Pass, Fail or Not verifiable with its evidence:

| Script output | Spec rows |
|---|---|
| seo_audit.py findings (title_short, meta_missing, h1_missing, canonical_missing, alt_missing, em_dashes...) | C-01 to C-26 |
| kw_placement_low, kw_not_in_intro (and the placement matrix: is the city in each zone?) | LOC-01, C-10 |
| schema_none, schema_fields, jsonld_invalid, JSON-LD properties missing per type | LOC-13, C-18 |
| thin_content, word count | LOC-19, C-08 |
| ai_bots_blocked | LOC-17 |
| social_placeholder, social_missing | CIT-05, C-20 |
| section_audit blocks contact_details, opening_hours, map_embed, price_in_text, images, reviews, faq, cta, internal_links, breadcrumb | LOC-03, LOC-04, LOC-05, LOC-06, LOC-08, LOC-09, LOC-11, LOC-12, LOC-14, C-19 |

The scripts see presence, not truth: a phone number found is not a phone number that matches the profile. LOC-03, LOC-04 and LOC-13 always need the manual side-by-side comparison with GBP. When no location page exists yet, the page audit is skipped (write "new page") and Phase 3 sets the bar for the build.

**Manual GBP and local checklist** (run even when the page is fine):

1. Pick 5-10 real buyer queries and check the local pack from inside the service area. Distance from the searcher affects results, so a check from another city is worthless. Mix the query types:

| Query type | Example | What it tests |
|---|---|---|
| Explicit city | "plumber lyon" | Relevance and prominence across the whole city |
| Implicit near-me | "plumber near me" | Proximity-weighted ranking around the searcher |
| Service + qualifier | "emergency plumber open now" | Hours, attributes, and category coverage |
| AI assistant phrasing | "best plumber in lyon" asked to an assistant | The GEO layer: profile, reviews, and site together |

2. Walk GBP-01 to GBP-16 on the profile: every empty field is a finding.
3. Read the review history: count, rating, dates of the last 20 reviews (velocity, bursts), reply rate, how replies are written (REV-02, REV-05).
4. Scan NAP across the site, the profile, directories and social profiles; note every variant (CIT-01, CIT-02).
5. Check for duplicate or orphan profiles of the same business, and whether the profile is suspended (special procedure below).

## Phase 3. Benchmark the competitors

**Pick them from the query "{service} {city}"**, searched from inside the service area: the 3 businesses in the local pack, plus the top 3-5 organic results that are local businesses (not directories), plus the businesses an AI assistant names for "best {service} in {city}". Those are the bar for both assets.

**Their pages**, with the bundled benchmark (the location page of each competitor, or the page their profile links to):

```
python3 skills/seo-geo-audit/scripts/page_benchmark.py --type location https://client.com/plumber-lyon/ https://rival1.com/lyon/ https://rival2.com/plombier-lyon/ https://rival3.com/
```

Read in its output: the blocks half or more of the competitors have and the client does not (map, hours, prices in text, reviews, FAQ), the schema types they use that the client lacks (LocalBusiness or a subtype), the metrics below the competitor median (words, statistics, question headings, placement), and the client's high-severity findings. Rows of C and LOC whose metric sits below the median move up in priority.

**Their profiles, by hand**, into a gap table (the business vs each pack leader):

| Signal | Client | Leader A | Leader B | Leader C |
|---|---|---|---|---|
| Review count, average rating | | | | |
| Review recency and velocity (reviews in the last 30 and 90 days) | | | | |
| Reply rate and reply quality | | | | |
| Primary and secondary categories | | | | |
| Photo count, real vs stock, last photo added | | | | |
| Posts: date of the last one, frequency | | | | |
| Services, attributes, Q&A filled | | | | |
| Profile links to a location page or the homepage | | | | |
| Linked website strength (location page, booking, real photos, schema) | | | | |

The gap table sets the plan. If competitors have 240 reviews and the business has 12, no amount of posting will close that gap: size REV-01 from it. If all three leaders use a different primary category for the target query, test theirs (GBP-02).

**Define the information gain**: what the client will publish that no leader has, for example prices in text when none show them, a stated response time, photos of jobs in named neighborhoods, parking and access details, a local FAQ, owner replies that answer the question behind each review. That list goes into the build.

## Phase 4. Build

### Build order: the four pillars of a profile that ranks

Every plan in this skill hangs on these four levers, in priority order:

| Pillar | What it covers | Spec rows | Why it ranks |
|---|---|---|---|
| 1. Reviews | Count, velocity, recency, reply rate | REV-01 to REV-07 | The strongest lever observed in the field; review signals also sit among the top local pack factor groups in the Whitespark Local Search Ranking Factors survey (measured: industry survey) |
| 2. Profile completeness | Categories, services, attributes, real photos, hours, service areas | GBP-01 to GBP-14, GBP-16 | Google ranks what it understands; an empty profile gives it nothing to match queries against |
| 3. Regular activity | Posts, photo additions, Q&A, fresh info | GBP-15, GBP-09, GBP-13 | A liveness signal; low direct ranking impact on its own (field heuristic, Step 6) |
| 4. Linked website strength | The site's authority, local pages, on-page local signals | LOC-01 to LOC-19, CIT | Website signals flow into Maps ranking; the profile and the site feed each other |

Treating reviews as the number one factor is a constant field observation across 115+ audits, consistent with industry surveys; it is not an official Google statement. Google's own documented local ranking factors are relevance, distance, and prominence (measured: Google, see Sources), and reviews feed both relevance and prominence.

Order of operations: reviews and completeness move pack positions within weeks; website strength compounds over months; posts alone move almost nothing. Plans that start with posting cadence are treating the cheapest lever first, not the strongest (field heuristic).

### Step 1: Diagnose before touching anything

Phases 2 and 3 are the diagnosis: the query set from inside the area, the profile walk, the NAP scan, the script audit of the location page, and the gap table against the 3 pack leaders. Do not change the profile before the gap table exists.

### Step 2: Settle the business name decision (GBP-01)

Two facts, presented honestly:

- Adding the trade and the city to the profile name ("Plumber Smith Lyon" instead of "Smith") measurably improves local rankings; keywords in the business name have ranked among the strongest local pack factors in industry surveys for years (measured: Whitespark Local Search Ranking Factors).
- Google's guidelines require the exact real-world business name, nothing added. A keyword-stuffed name violates GBP guidelines and exposes the profile to suspension at any time, including after years of working fine (measured: Google Business Profile guidelines, see Sources).

**Explicit Google guidelines risk.** Present both facts to the user, recommend compliance, and do not implement a stuffed name: it is a documented guidelines violation, not a neutral option. A suspension costs weeks of visibility (see the reinstatement reference), and competitors can report a stuffed name at any time. If the legal name genuinely contains the trade ("Lyon Plumbing SARL"), using it is fully compliant.

### Step 3: Fix categories (GBP-02, GBP-03)

1. Primary category: the single most specific category that matches the core business. "Personal injury attorney" beats "Lawyer"; "Cosmetic dentist" beats "Dentist" if that is the money service. The primary category is the strongest single relevance signal on the profile (measured: consistently top-ranked in the Whitespark survey).
2. Secondary categories: add every category that genuinely applies, nothing aspirational.
3. Re-check the pack leaders' categories: if all three use a different primary category for the target query, test theirs.

### Step 4: Complete the profile to 100% (GBP-04 to GBP-14, GBP-16)

Choose the right setup first:

| Setup | Address shown | Use when |
|---|---|---|
| Storefront | Yes | Customers come to the location (shop, clinic, restaurant) |
| Service-area business | No, service areas listed instead | Work happens at the customer's location (plumber, cleaner, landscaper) |
| Hybrid | Yes, plus service areas | Customers visit and the business also travels (showroom plus installation) |

Then budget about 1h30 of focused work (field heuristic) and fill every field to the GBP table standard, in order: services, attributes, description, photos, hours, service areas (service-area businesses: hide the address, list the areas), phone and site link, booking and quote links, Q&A, opening date. Why: every filled field is matching surface for queries, and completeness differences are visible in the gap table in nearly every audit (field heuristic).

### Step 5: Build the review engine, the number one lever (REV-01 to REV-07)

1. **Ask at the peak of satisfaction**: the moment the job is done, the result is visible, and the customer says thanks. Asking days later collapses the conversion rate (field heuristic).
2. **Make it one tap**: short review link (g.page/...) on a card, a QR code on the invoice or counter, an SMS or email the same day.
3. **Aim for steady velocity**, a few reviews every week, rather than bursts. A burst after months of silence looks bought, to readers and to spam filters (field heuristic). Size the target from the gap table: (leader review count minus current count) divided by 12, plus the leader's monthly pace, gives the monthly asks needed to close the gap within a year. If that volume is unrealistic, compete on recency, detail, and reply quality instead.
4. **Reply to 100% of reviews**, positive and negative. Replies are read by every future customer and ingested by AI assistants summarizing the business (see GEO layer). The reply is written for the next 1000 readers, not for the author. Patterns:

| Review | Reply pattern |
|---|---|
| Positive | Thank by name, mention the service and city once where natural, invite back |
| Negative, legitimate | Acknowledge the facts, state the fix made, move the conversation offline; factual tone, never argue, no public discounts |
| Suspected fake | State factually that no record of this customer exists, report it through the profile; never accuse the reviewer |

5. **Encourage detail naturally**: when asking, mention the service and the city ("a quick line about the bathroom renovation we did in Croix-Rousse helps others find us"). Detailed reviews mentioning service and city feed both rankings and AI answers. Keyword hierarchy: keywords the customer writes in their own review (service plus city) carry the real weight; putting the service and city in your reply is a smaller bonus on top. Steer the customer toward their own words, never script the review for them (field heuristic from 115+ agency audits).

**Explicit Google policy risk.** Never pay, discount, or incentivize reviews, never gate (filtering happy customers to Google and unhappy ones to a private form), never review-swap, never post fake reviews. All of these violate Google's review policies and can wipe every review or suspend the profile (measured: Google policy, see Sources); fake or incentivized undisclosed reviews are also illegal in several markets, including under the US FTC rule on consumer reviews (measured: see Sources).

### Step 6: Post regularly, with honest expectations (GBP-15)

Weekly or biweekly posts (offers, completed jobs, seasonal info) keep the profile visibly alive and add fresh photos and keywords to the surface. Direct ranking impact is low; posts are an activity signal, not a ranking engine (field heuristic, consistent with the low weight of post signals in industry surveys). Never sell posting cadence as the fix for a review or completeness gap.

### Step 7: Build the location page and strengthen the linked website (LOC-01 to LOC-19)

The website is the fourth pillar and the one local businesses skip most often (field heuristic). Maps ranking draws on the linked site's relevance and authority; a strong location page lifts the profile, and the profile sends behavioral signals back. Concrete case seen repeatedly: a competitor with fewer reviews but a complete linked site (online booking, real on-location photos, a proper location page) outranks a business that wins on review count alone, because the richer site gives Google more to match the query against (field heuristic from 115+ agency audits). Reviews lead, but the linked site can flip a close pack position.

**Location page skeleton**, in order (block levels in seo-page-sections/references/page-type-matrix.md, section 4; full checklist in references/location-page-template.md): H1 "{service} in {city}" (LOC-01); intro with service and city in the first 100 words and a CTA (LOC-12); full NAP, hours and embedded map (LOC-03 to LOC-05); services at this location with prices (LOC-06); areas and neighborhoods served (LOC-07); real photos (LOC-08); reviews of this location (LOC-09); local proof (LOC-10); parking and access (LOC-18); FAQ of local questions (LOC-11); final CTA; links to the services hub and sibling cities (LOC-14). Copy rules and the wireframe for the service content: seo-content-service-page.

**Metadata pattern** (LOC-01, C-01, C-02, C-23):

```
Title:            {primary service} in {city} | {brand}            (50-60 chars)
Slug:             /{city}/ or /{service}-{city}/
H1:               {primary service} in {city}
Meta description: {promise} in {city}. {proof}. {call to action}.  (max 160 chars)
```

**Schema (LOC-13)**: LocalBusiness on each location page, typed with the most specific schema.org subtype (Plumber, Dentist, Attorney, Restaurant...): name, address, telephone, geo coordinates, openingHoursSpecification, areaServed, url, image, sameAs, every value exactly matching the profile. Service-area businesses with a hidden home address keep the address out and lead with areaServed. No aggregateRating or review markup about your own business unless the reviews are genuinely displayed on the page and eligible. Skeleton: references/location-page-template.md; validation and extensions: seo-schema-markup.

Then, on the site:

1. One location page per establishment, linked from the matching profile (LOC-02, GBP-11).
2. City pages for the wider service area: parent region page plus unique child city pages (LOC-15; architecture and anti-doorway rules: seo-content-service-page skill).
3. General site authority: technical health (seo-technical) and links (seo-backlinks). A site that ranks organically pulls its profile up in the pack.

For multi-location brands:

- One profile per real, staffed branch, each verified separately; never a profile in a city with no real presence (guideline violation, removal risk).
- Each profile links to its own location page, never the shared homepage; a /locations/ index page lists every branch with its NAP and links down to each.
- Keep names consistent with real-world signage across branches; location descriptors are acceptable only if they appear on the signage, anything else is the Step 2 risk.

### Step 8: Enforce NAP consistency everywhere (CIT-01, CIT-02)

Name, Address, Phone: byte-identical on the site footer, location pages, GBP, every directory, every social profile. Pick one canonical format ("Rue de la République 12" vs "12 rue de la République", "+33 4 ..." vs "04 ...") and propagate it.

Why: Google and LLMs cross-check entity facts across independent sources. Consistent citations raise confidence that the business is real, located there, and reachable; conflicting data lowers it for both ranking and AI recommendation (field heuristic for the AI side; long-standing citation consistency factor in industry surveys for the ranking side). Finding and building the citation spots themselves (directories, trade associations, local listings): seo-backlinks skill.

### Step 9: Earn local brand mentions (CIT-03, CIT-04)

Local press, city blogs, neighborhood associations, sponsorships, chamber of commerce features. These mentions, linked or not, build the entity prominence that both Google and AI assistants read (see GEO layer for the measured correlation). Outreach mechanics: seo-backlinks skill.

### Step 10: Monitor

Track pack positions on the Phase 2 query set from inside the service area, review velocity vs competitors, and profile interactions (calls, direction requests, site clicks) monthly. For AI assistant visibility ("best [trade] in [city]" answers), use the geo-tracking skill.

### Acceptance test

Re-run the scripts on the live or staged location page:

```
python3 skills/seo-geo-audit/scripts/seo_audit.py https://example.com/plumber-lyon/
python3 skills/seo-page-sections/scripts/section_audit.py --type location https://example.com/plumber-lyon/
```

The finish line: no high or critical finding; no `schema_none`, `schema_fields` or `jsonld_invalid`, with a LocalBusiness subtype present; placement coverage 60%+ with the city in title, H1, URL and intro; section_audit finds contact_details, opening_hours, map_embed, price_in_text, reviews, faq, cta; word count at or above the Phase 3 median; every block present on half or more of the competitors now present. Then the manual side: NAP, hours and schema values compared character for character with the profile; GBP-01 to GBP-16 all Pass; the review routine live with its monthly target; the monitoring set up. A row that still fails is either fixed or a written owner decision (typically GBP-01, the name).

### Special procedure: suspended profile

A suspension removes the profile from Maps and Search. Follow references/gbp-reinstatement.md step by step. The short version:

1. Never create a new profile to replace the suspended one. Duplicates make reinstatement harder and can get both removed (measured: Google guidelines prohibit duplicate listings).
2. Identify the likely trigger (recent name change, address edit, category stuffing, virtual office address).
3. Fix the profile to full guideline compliance first.
4. Gather evidence: proof of address (utility bill, lease), business registration, photos of the storefront and signage.
5. Submit one complete appeal through Google's appeals tool. One thorough appeal beats five thin ones; repeated weak appeals can exhaust the available attempts.
6. Expect days to weeks for a resolution. Meanwhile, the website's location page keeps the business visible in organic results, one more reason every location needs its own page.

## Rules and thresholds

| Rule | Threshold | Spec | Evidence level |
|---|---|---|---|
| Review reply rate | 100%, negatives included | REV-05 | Field heuristic |
| Review ask timing | At the peak of satisfaction, same day | REV-03 | Field heuristic |
| Review velocity | Steady weekly flow beats bursts | REV-02 | Field heuristic |
| Incentivized, gated, or fake reviews | Zero, ever | REV-07 | Google policy + FTC rule (measured) |
| Business name | Exact real-world name; additions = ranking gain but suspension risk, user decides informed | GBP-01 | Google guidelines + Whitespark survey (measured) |
| Primary category | The most specific available, revisited quarterly | GBP-02 | Whitespark survey (measured) |
| Profile completeness | 100% of fields, about 1h30 of work | GBP-16 | Field heuristic |
| Photos | Real only, new ones monthly | GBP-09, LOC-08 | Field heuristic |
| Posts | Weekly to biweekly, expectations capped (activity signal) | GBP-15 | Field heuristic |
| NAP | Byte-identical everywhere, one canonical format | CIT-01, CIT-02, LOC-03 | Industry surveys + field heuristic |
| Listings | One profile per real location; service-area businesses hide the address | GBP-04, GBP-05 | Google guidelines (measured) |
| Location pages | One per establishment, LocalBusiness schema, embedded map, local keyword pattern | LOC-01, LOC-02, LOC-05, LOC-13 | Field heuristic |
| Suspended profile | Appeal once with complete evidence; never duplicate | GBP-05 | Google guidelines (measured) |
| Punctuation | Zero em dashes and zero en dashes, replaced by commas | C-25, GBP-08 | House rule, most recognizable AI-writing tell |

Punctuation, non-negotiable: never leave an em dash (U+2014) or an en dash (U+2013) in anything published under the client's name. Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. The em dash is the single most recognizable tell of AI-written text, and it does the most damage exactly here, where the copy is supposed to sound like a local owner: profile description, services and products, Google Posts, Q&A answers, review replies, location page copy and metadata. Sweep for both characters before publishing. Hyphens in compound words and ranges written with "to" are untouched.

## GEO layer

"Best [trade] in [city]" is one of the most frequent commercial questions put to AI assistants, and the answer is a direct recommendation list the business is either on or not. Assistants assemble these lists from three source families:

1. **Google Business Profile data** surfaced through Maps and Search: name, categories, rating, review count, attributes.
2. **Review platforms and directories**: Google reviews, Yelp, Trustpilot, Tripadvisor, and trade-specific directories. The richer and more consistent the presence, the more material there is to cite.
3. **The business's own local pages**: the location page and city pages, when they contain extractable facts (services, areas, prices, response times).

Apply all of the following (the five checks of the GEO pass in the deliverable):

- **Treat review text and owner replies as published content (REV-05, REV-06).** Assistants read and summarize them. Detailed reviews that name the service and the city ("they renovated our bathroom in Croix-Rousse, Lyon") feed answers directly; "great job" feeds nothing. Ask for detail naturally (Step 5), never script reviews.
- **Feed the entity, not just the profile (CIT-04).** Local brand mentions in press and city blogs correlate with AI visibility roughly 3 times more strongly than backlinks: 0.664 correlation for brand mentions vs 0.218 for backlinks against AI Overview brand visibility (measured correlation, not causation: ahrefs.com/blog/ai-overview-brand-correlation/).
- **Keep entity facts identical everywhere (CIT-02, LOC-03).** LLMs cross-check sources the same way Google does; NAP and service-area consistency is what lets a model state facts about the business with confidence (Step 8).
- **Make the location page self-sufficient and extractable (LOC-06, LOC-16)**: services with prices or ranges, areas served, response times, team, in plain HTML. Passage-level writing rules: geo-visibility skill.
- **Get on the lists assistants quote (CIT-03).** "Best [trade] in [city]" answers lean heavily on existing listicles, review platforms, and trade directories; building presence on those is citation work, handled by the seo-backlinks skill.
- **Verify AI crawler access (LOC-17)** to the site (GPTBot, ClaudeBot, PerplexityBot): seo-technical skill. Measure whether assistants actually recommend the business, and against which competitors: geo-tracking skill.

## Deliverable

```markdown
## 1. Spec scorecard
| ID | Requirement | Status (Pass / Fail / Not verifiable) | Evidence |
(C-01 to C-26 and LOC rows for the location page; GBP, REV and CIT rows for the profile, reviews and citations)

## 2. Audit findings
(seo_audit.py scores and high or medium findings, section_audit.py --type location blocks; or "new page";
the manual GBP checklist: query set and pack positions from inside the area, empty fields, review history, NAP variants found;
findings grouped by pillar: reviews, completeness, activity, website, each with evidence)

## 3. Competitor benchmark
(page_benchmark.py table, blocks and schema types the client lacks, metrics below the median;
the GBP gap table vs the 3 pack leaders: reviews count, rating, recency and velocity, categories, photos, posts, site strength;
the information gain chosen)

## 4. Build
(prioritized action plan: | Priority | Action | Pillar | Spec ID | Impact | Effort |;
the business name recommendation with the guideline trade-off stated explicitly;
profile copy (description, services, Q&A), the review engine, location page copy block by block,
metadata, LocalBusiness JSON-LD, internal links; GEO layer pass: the 5 checks, pass/fail;
placeholders {to confirm} for unverified facts)

## 5. Acceptance
(scripts re-run: remaining findings, each either fixed or a written owner decision; manual GBP and NAP re-check;
monitoring set: fixed query set, review velocity vs leaders, profile actions month over month)
```

Narrower requests use the same five parts, with the build section focused:

- **Review engine setup**: the ask script (verbal + SMS/email), the short link and QR placement plan, the weekly velocity target based on the competitor gap, and reply templates (positive, negative, fake-suspected).
- **Suspension**: likely cause, compliance fixes, evidence checklist, and the appeal text, following references/gbp-reinstatement.md.
- **Location pages**: one page brief per location from references/location-page-template.md, with schema notes for seo-schema-markup.
- **Monitoring**: the fixed query set from Phase 2, pack positions checked from inside the area, review velocity vs the pack leaders, profile actions (calls, direction requests, site clicks) month over month, and AI mention tracking handed to geo-tracking.

## Common mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| Keyword-stuffing the profile name without knowing the risk | Suspension can arrive any time and costs weeks | Present both facts, decide informed, prefer compliance |
| Creating a second profile after a suspension | Flags as duplicate, blocks reinstatement | One profile, one complete appeal |
| Broad primary category ("Lawyer") | Loses to specific competitors on every money query | Most specific category that fits |
| Treating posts as the strategy | Low direct ranking impact; the review gap stays | Reviews and completeness first |
| Ignoring negative reviews | Future customers and AI assistants read the silence | 100% reply rate, factual tone |
| Review bursts after silence | Looks bought to readers and filters | Steady weekly ask routine |
| Incentivized or gated reviews | Google policy violation + legal exposure | Ask everyone, at the peak, no rewards |
| Stock photos on the profile | Kills trust, signals a shell listing | Real storefront, team, and job photos |
| Inconsistent NAP across directories | Erodes entity confidence for Google and LLMs | One canonical format, propagated |
| Linking the profile to the homepage for every branch | Generic relevance, wasted local signal | Each profile links to its location page |
| One "Locations" page for 10 branches | No branch can rank locally | One location page per establishment |
| Fake address or virtual office to appear in a city | Guideline violation, suspension and removal risk | Service-area setup or a real office |
| Checking rankings from outside the service area | Distance skews results, false conclusions | Check from inside the area or with a geo-grid tool |
| Same reply pasted under every review | Reads as automation to customers and to AIs | Reference the specific service and detail each time |
| Trusting the script's "contact_details found" as a NAP pass | Presence is not a match with the profile | Compare page, schema and GBP character for character |
| Benchmarking only the pages, not the profiles | Misses the review and category gaps that decide the pack | Page benchmark plus the manual GBP gap table |

## Sources

- Google: how local ranking works (relevance, distance, prominence): support.google.com/business/answer/7091 (official)
- Google Business Profile guidelines (name, address, duplicates): support.google.com/business/answer/3038177 (official)
- Google prohibited and restricted content for reviews (incentives, gating, fakes): support.google.com/contributionpolicy/answer/7400114 (official)
- Google Business Profile suspensions and appeals: support.google.com/business/answer/4569145 and support.google.com/business/answer/12475845 (official)
- Whitespark Local Search Ranking Factors survey: whitespark.ca/local-search-ranking-factors (measured: industry expert survey, review and category signals among top local pack factor groups)
- Ahrefs, AI Overviews brand visibility correlation (0.664 brand mentions vs 0.218 backlinks): ahrefs.com/blog/ai-overview-brand-correlation/ (measured correlation)
- US FTC rule banning fake and undisclosed incentivized reviews (16 CFR Part 465): ftc.gov/news-events/news/press-releases/2024/08/ftc-announces-final-rule-banning-fake-reviews-testimonials (official)
- Google LocalBusiness structured data: developers.google.com/search/docs/appearance/structured-data/local-business (official)
- Field heuristics: 115+ real agency audits of local and service businesses, 2024-2026 (observational, labeled as such throughout)
