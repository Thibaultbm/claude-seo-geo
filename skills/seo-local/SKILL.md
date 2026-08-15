---
name: seo-local
description: "Improve local visibility so the business shows in the map pack and gets recommended by AI for 'best [trade] in [city]' queries. Input: a business, its locations, and its Google Business Profile. Output: a GBP audit and category strategy, review generation and replies, NAP consistency, location pages with LocalBusiness schema, multi-location and service-area setups, and suspended-listing reinstatement. Use for GBP, Google Maps, the local pack, reviews and star ratings, a business not showing on Maps, or a suspended listing."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Local SEO: Google Business Profile, Reviews, and Local Pages

Local SEO decides who appears when a buyer searches "plumber near me", opens Google Maps, or asks an AI assistant for "the best dentist in Geneva". Three surfaces matter: the local pack (Maps results inside the SERP), localized organic results, and AI assistant recommendations. They feed on overlapping signals: the Google Business Profile, reviews, the linked website, and the consistency of the business entity across the web.

The methodology combines two evidence levels, labeled throughout:

- **Field heuristic**: rules derived from 115+ real agency audits of local and service businesses (2024-2026). Consistently observed, not lab-measured.
- **Measured**: claims backed by a published study, an industry survey, or official documentation, with the source.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use this skill

Use it to diagnose why a business is invisible in the local pack, set up or complete a Google Business Profile, build a review generation engine, write review replies, plan location pages, structure a multi-city or service-area business, or recover a suspended listing.

Stay in scope. Hand adjacent work to the right skill:

| Task | Skill |
|---|---|
| GBP, reviews, local pack, location page strategy (this skill) | seo-local |
| Finding and building citation and directory links | seo-backlinks |
| Writing service pages and city pages (copy and wireframe) | seo-content-service-page |
| LocalBusiness schema implementation details | seo-schema-markup |
| Site crawlability, speed, AI crawler access | seo-technical |
| Local keyword selection | seo-keyword-research |
| Writing rules for AI answer citability | geo-visibility |
| Measuring AI assistant mentions | geo-tracking |
| Full-site audit | seo-geo-audit |

## The four pillars of a profile that ranks

Every diagnosis and plan in this skill hangs on these four levers, in priority order:

| Pillar | What it covers | Why it ranks |
|---|---|---|
| 1. Reviews | Count, velocity, recency, reply rate | The strongest lever observed in the field; review signals also sit among the top local pack factor groups in the Whitespark Local Search Ranking Factors survey (measured: industry survey) |
| 2. Profile completeness | Categories, services, attributes, real photos, hours, service areas | Google ranks what it understands; an empty profile gives it nothing to match queries against |
| 3. Regular activity | Posts, photo additions, Q&A, fresh info | A liveness signal; low direct ranking impact on its own (field heuristic, see Step 6) |
| 4. Linked website strength | The site's authority, local pages, on-page local signals | Website signals flow into Maps ranking; the profile and the site feed each other |

Treating reviews as the number one factor is a constant field observation across 115+ audits, consistent with industry surveys; it is not an official Google statement. Google's own documented local ranking factors are relevance, distance, and prominence (measured: Google, see Sources), and reviews feed both relevance and prominence.

Order of operations: reviews and completeness move pack positions within weeks; website strength compounds over months; posts alone move almost nothing. Plans that start with posting cadence are treating the cheapest lever first, not the strongest (field heuristic).

## Workflow

### Step 1: Diagnose before touching anything

1. Pick 5-10 real buyer queries and check the local pack from inside the service area. Distance from the searcher affects results, so a check from another city is worthless. Mix the query types:

| Query type | Example | What it tests |
|---|---|---|
| Explicit city | "plumber lyon" | Relevance and prominence across the whole city |
| Implicit near-me | "plumber near me" | Proximity-weighted ranking around the searcher |
| Service + qualifier | "emergency plumber open now" | Hours, attributes, and category coverage |
| AI assistant phrasing | "best plumber in lyon" asked to an assistant | The GEO layer: profile, reviews, and site together |
2. Compare the business against the 3 businesses that own the pack: review count, average rating, review recency, primary category, photo count, website strength.
3. Audit the profile itself: every empty field is a finding.
4. Scan NAP (Name, Address, Phone) across the site, the profile, directories, and social profiles. Note every variant.
5. Audit the linked website with the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py): does a dedicated location page exist, does it carry the local keyword pattern, does it have LocalBusiness schema?

The gap table from point 2 sets the plan. If competitors have 240 reviews and the business has 12, no amount of posting will close that gap.

### Step 2: Settle the business name decision

Two facts, presented honestly:

- Adding the trade and the city to the profile name ("Plumber Smith Lyon" instead of "Smith") measurably improves local rankings; keywords in the business name have ranked among the strongest local pack factors in industry surveys for years (measured: Whitespark Local Search Ranking Factors).
- Google's guidelines require the exact real-world business name, nothing added. A keyword-stuffed name violates GBP guidelines and exposes the profile to suspension at any time, including after years of working fine (measured: Google Business Profile guidelines, see Sources).

**Explicit Google guidelines risk.** Present both facts to the user and let them make an informed choice. Recommend compliance: a suspension costs weeks of visibility (see the reinstatement reference), and competitors can report a stuffed name. If the legal name genuinely contains the trade ("Lyon Plumbing SARL"), using it is fully compliant.

### Step 3: Fix categories

1. Primary category: the single most specific category that matches the core business. "Personal injury attorney" beats "Lawyer"; "Cosmetic dentist" beats "Dentist" if that is the money service. The primary category is the strongest single relevance signal on the profile (measured: consistently top-ranked in the Whitespark survey).
2. Secondary categories: add every category that genuinely applies, nothing aspirational.
3. Re-check the pack leaders' categories: if all three use a different primary category for the target query, test theirs.

### Step 4: Complete the profile to 100%

Choose the right setup first:

| Setup | Address shown | Use when |
|---|---|---|
| Storefront | Yes | Customers come to the location (shop, clinic, restaurant) |
| Service-area business | No, service areas listed instead | Work happens at the customer's location (plumber, cleaner, landscaper) |
| Hybrid | Yes, plus service areas | Customers visit and the business also travels (showroom plus installation) |

Then budget about 1h30 of focused work (field heuristic). Fill, in order:

| Field | Standard |
|---|---|
| Services | Every billable service, each with its description and price or price range |
| Attributes | All that apply (accessibility, payments, amenities) |
| Description | 750 characters, plain factual language, services + areas + differentiators |
| Photos | Real photos only: storefront, team, work in progress, results; add new ones monthly; never stock |
| Hours | Exact, including holiday hours |
| Service areas | Every city actually served (service-area businesses: hide the address, list the areas) |
| Phone and site link | Local number; link to the matching location page, not the homepage, for multi-location businesses |
| Booking and quote links | Whatever shortens the path to contact |
| Q&A | Seed the 5 most-asked buyer questions from the owner account and answer them; transparent and allowed, and it preempts wrong answers from strangers |
| Opening date | Set it; longevity feeds prominence |

Why: every filled field is matching surface for queries, and completeness differences are visible in the Step 1 gap table in nearly every audit (field heuristic).

### Step 5: Build the review engine (the number one lever)

1. **Ask at the peak of satisfaction**: the moment the job is done, the result is visible, and the customer says thanks. Asking days later collapses the conversion rate (field heuristic).
2. **Make it one tap**: short review link (g.page/...) on a card, a QR code on the invoice or counter, an SMS or email the same day.
3. **Aim for steady velocity**, a few reviews every week, rather than bursts. A burst after months of silence looks bought, to readers and to spam filters (field heuristic). Size the target from the Step 1 gap table: (leader review count minus current count) divided by 12, plus the leader's monthly pace, gives the monthly asks needed to close the gap within a year. If that volume is unrealistic, compete on recency, detail, and reply quality instead.
4. **Reply to 100% of reviews**, positive and negative. Replies are read by every future customer and ingested by AI assistants summarizing the business (see GEO layer). The reply is written for the next 1000 readers, not for the author. Patterns:

| Review | Reply pattern |
|---|---|
| Positive | Thank by name, mention the service and city once where natural, invite back |
| Negative, legitimate | Acknowledge the facts, state the fix made, move the conversation offline; factual tone, never argue, no public discounts |
| Suspected fake | State factually that no record of this customer exists, report it through the profile; never accuse the reviewer |

5. **Encourage detail naturally**: when asking, mention the service and the city ("a quick line about the bathroom renovation we did in Croix-Rousse helps others find us"). Detailed reviews mentioning service and city feed both rankings and AI answers. Keyword hierarchy: keywords the customer writes in their own review (service plus city) carry the real weight; putting the service and city in your reply is a smaller bonus on top. Steer the customer toward their own words, never script the review for them (field heuristic from 115+ agency audits).

**Explicit Google policy risk.** Never pay, discount, or incentivize reviews, never gate (filtering happy customers to Google and unhappy ones to a private form), never review-swap, never post fake reviews. All of these violate Google's review policies and can wipe every review or suspend the profile (measured: Google policy, see Sources); fake or incentivized undisclosed reviews are also illegal in several markets, including under the US FTC rule on consumer reviews (measured: see Sources).

### Step 6: Post regularly, with honest expectations

Weekly or biweekly posts (offers, completed jobs, seasonal info) keep the profile visibly alive and add fresh photos and keywords to the surface. Direct ranking impact is low; posts are an activity signal, not a ranking engine (field heuristic, consistent with the low weight of post signals in industry surveys). Never sell posting cadence as the fix for a review or completeness gap.

### Step 7: Strengthen the linked website

The website is the fourth pillar and the one local businesses skip most often (field heuristic). Maps ranking draws on the linked site's relevance and authority; a strong location page lifts the profile, and the profile sends behavioral signals back. Concrete case seen repeatedly: a competitor with fewer reviews but a complete linked site (online booking, real on-location photos, a proper location page) outranks a business that wins on review count alone, because the richer site gives Google more to match the query against (field heuristic from 115+ agency audits). Reviews lead, but the linked site can flip a close pack position. Build:

1. One location page per establishment, linked from the matching profile. Structure, copy, and the full local keyword pattern (city in title, URL, H1, meta description, first paragraph, image alts): see the seo-content-service-page skill and references/location-page-template.md.
2. LocalBusiness schema on each location page: name, address, phone, geo coordinates, opening hours, exactly matching the profile (implementation: seo-schema-markup skill).
3. An embedded Google map of the location.
4. City pages for the wider service area: parent region page plus unique child city pages (architecture and anti-doorway rules: seo-content-service-page skill).
5. General site authority: technical health (seo-technical) and links (seo-backlinks). A site that ranks organically pulls its profile up in the pack.

For multi-location brands:

- One profile per real, staffed branch, each verified separately; never a profile in a city with no real presence (guideline violation, removal risk).
- Each profile links to its own location page, never the shared homepage; a /locations/ index page lists every branch and links down to each.
- Keep names consistent with real-world signage across branches; location descriptors are acceptable only if they appear on the signage, anything else is the Step 2 risk.

### Step 8: Enforce NAP consistency everywhere

Name, Address, Phone: byte-identical on the site footer, location pages, GBP, every directory, every social profile. Pick one canonical format ("Rue de la République 12" vs "12 rue de la République", "+33 4 ..." vs "04 ...") and propagate it.

Why: Google and LLMs cross-check entity facts across independent sources. Consistent citations raise confidence that the business is real, located there, and reachable; conflicting data lowers it for both ranking and AI recommendation (field heuristic for the AI side; long-standing citation consistency factor in industry surveys for the ranking side). Finding and building the citation spots themselves (directories, trade associations, local listings): seo-backlinks skill.

### Step 9: Earn local brand mentions

Local press, city blogs, neighborhood associations, sponsorships, chamber of commerce features. These mentions, linked or not, build the entity prominence that both Google and AI assistants read (see GEO layer for the measured correlation). Outreach mechanics: seo-backlinks skill.

### Step 10: Monitor

Track pack positions on the Step 1 query set from inside the service area, review velocity vs competitors, and profile interactions (calls, direction requests, site clicks) monthly. For AI assistant visibility ("best [trade] in [city]" answers), use the geo-tracking skill.

### Special procedure: suspended profile

A suspension removes the profile from Maps and Search. Follow references/gbp-reinstatement.md step by step. The short version:

1. Never create a new profile to replace the suspended one. Duplicates make reinstatement harder and can get both removed (measured: Google guidelines prohibit duplicate listings).
2. Identify the likely trigger (recent name change, address edit, category stuffing, virtual office address).
3. Fix the profile to full guideline compliance first.
4. Gather evidence: proof of address (utility bill, lease), business registration, photos of the storefront and signage.
5. Submit one complete appeal through Google's appeals tool. One thorough appeal beats five thin ones; repeated weak appeals can exhaust the available attempts.
6. Expect days to weeks for a resolution. Meanwhile, the website's location page keeps the business visible in organic results, one more reason every location needs its own page.

## Rules and thresholds

| Rule | Threshold | Evidence level |
|---|---|---|
| Review reply rate | 100%, negatives included | Field heuristic |
| Review ask timing | At the peak of satisfaction, same day | Field heuristic |
| Review velocity | Steady weekly flow beats bursts | Field heuristic |
| Incentivized, gated, or fake reviews | Zero, ever | Google policy + FTC rule (measured) |
| Business name | Exact real-world name; additions = ranking gain but suspension risk, user decides informed | Google guidelines + Whitespark survey (measured) |
| Primary category | The most specific available, revisited quarterly | Whitespark survey (measured) |
| Profile completeness | 100% of fields, about 1h30 of work | Field heuristic |
| Photos | Real only, new ones monthly | Field heuristic |
| Posts | Weekly to biweekly, expectations capped (activity signal) | Field heuristic |
| NAP | Byte-identical everywhere, one canonical format | Industry surveys + field heuristic |
| Listings | One profile per real location; service-area businesses hide the address | Google guidelines (measured) |
| Location pages | One per establishment, LocalBusiness schema, embedded map, local keyword pattern | Field heuristic |
| Suspended profile | Appeal once with complete evidence; never duplicate | Google guidelines (measured) |
| Punctuation | Zero em dashes and zero en dashes, replaced by commas | House rule, most recognizable AI-writing tell |

Punctuation, non-negotiable: never leave an em dash (U+2014) or an en dash (U+2013) in anything published under the client's name. Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. The em dash is the single most recognizable tell of AI-written text, and it does the most damage exactly here, where the copy is supposed to sound like a local owner: profile description, services and products, Google Posts, Q&A answers, review replies, location page copy and metadata. Sweep for both characters before publishing. Hyphens in compound words and ranges written with "to" are untouched.

## GEO layer

"Best [trade] in [city]" is one of the most frequent commercial questions put to AI assistants, and the answer is a direct recommendation list the business is either on or not. Assistants assemble these lists from three source families:

1. **Google Business Profile data** surfaced through Maps and Search: name, categories, rating, review count, attributes.
2. **Review platforms and directories**: Google reviews, Yelp, Trustpilot, Tripadvisor, and trade-specific directories. The richer and more consistent the presence, the more material there is to cite.
3. **The business's own local pages**: the location page and city pages, when they contain extractable facts (services, areas, prices, response times).

Apply all of the following:

- **Treat review text and owner replies as published content.** Assistants read and summarize them. Detailed reviews that name the service and the city ("they renovated our bathroom in Croix-Rousse, Lyon") feed answers directly; "great job" feeds nothing. Ask for detail naturally (Step 5), never script reviews.
- **Feed the entity, not just the profile.** Local brand mentions in press and city blogs correlate with AI visibility roughly 3 times more strongly than backlinks: 0.664 correlation for brand mentions vs 0.218 for backlinks against AI Overview brand visibility (measured correlation, not causation: ahrefs.com/blog/ai-overview-brand-correlation/).
- **Keep entity facts identical everywhere.** LLMs cross-check sources the same way Google does; NAP and service-area consistency is what lets a model state facts about the business with confidence (Step 8).
- **Make the location page self-sufficient and extractable**: services with prices or ranges, areas served, response times, team, in plain HTML. Passage-level writing rules: geo-visibility skill.
- **Get on the lists assistants quote.** "Best [trade] in [city]" answers lean heavily on existing listicles, review platforms, and trade directories; building presence on those is citation work, handled by the seo-backlinks skill.
- **Verify AI crawler access** to the site (GPTBot, ClaudeBot, PerplexityBot): seo-technical skill. Measure whether assistants actually recommend the business, and against which competitors: geo-tracking skill.

## Output format

**For a local visibility diagnosis**, deliver:

1. Gap table: the business vs the 3 pack leaders (reviews count, rating, recency, primary category, photos, site strength).
2. Findings by pillar (reviews, completeness, activity, website), each with evidence.
3. Prioritized action plan:

| Priority | Action | Pillar | Impact | Effort |
|---|---|---|---|---|

4. The business name recommendation with the guideline trade-off stated explicitly.
5. GEO layer pass: the 5 checks above, pass/fail.

**For a review engine setup**, deliver: the ask script (verbal + SMS/email), the short link and QR placement plan, the weekly velocity target based on the competitor gap, and reply templates (positive, negative, fake-suspected).

**For a suspension**, deliver: likely cause, compliance fixes, evidence checklist, and the appeal text, following references/gbp-reinstatement.md.

**For location pages**, deliver: one page brief per location from references/location-page-template.md, with schema notes for seo-schema-markup.

**For monitoring**, deliver: the fixed query set from Step 1, pack positions checked from inside the area, review velocity vs the pack leaders, profile actions (calls, direction requests, site clicks) month over month, and AI mention tracking handed to geo-tracking.

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
