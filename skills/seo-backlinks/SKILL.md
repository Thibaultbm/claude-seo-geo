---
name: seo-backlinks
description: "Plan and run off-page SEO to earn links and brand mentions, including for AI visibility. Input: a site, niche, and competitors. Output: a link strategy and 90-day plan, a profile review without paid tools, ninja linking, digital PR on proprietary data, broken-link building, linkable assets, and unlinked-mention conversion. Use for backlinks, link building, netlinking, domain authority, anchor text, guest posts, digital PR, disavow or toxic links, or evaluating a single link opportunity."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# SEO Backlinks: Strategy, Acquisition, and Brand Mentions

Most SEO tooling stops at link analysis: it tells you what your profile looks like and leaves you alone for the hard part. This skill covers the hard part: how to actually acquire links and brand mentions, by hand, with a defensible strategy, without a paid tool subscription and without an outreach agency.

It operates on a dual objective that defines off-page SEO in 2026:

1. **Links for Google.** Backlinks remain a major ranking factor in classic organic search.
2. **Mentions everywhere for LLMs.** Brand mentions (linked or not) correlate roughly 3x more strongly with visibility in AI answers than backlinks do. Ahrefs measured this across 75,000 brands: correlation of 0.664 for brand mentions versus 0.218 for backlinks against AI Overview presence (https://ahrefs.com/blog/ai-overview-brand-correlation/).

Every action this skill recommends should serve at least one of those two objectives, and the best actions serve both: a profile on a well-known platform is a link for Google and a citation surface for ChatGPT.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use this skill

Use it when the user wants to:

- Review or audit a backlink profile (theirs or a competitor's).
- Build a link acquisition plan (weekly cadence, 90-day program, campaign).
- Execute ninja linking: find and work concrete link spots one by one.
- Decide whether a specific link opportunity is worth taking (or buying).
- Recover or understand a drop attributed to off-page factors (spam updates, lost links).
- Increase brand mentions so AI assistants cite the brand in answers.

Related skills, and where the boundary sits:

| Skill | Boundary with this skill |
|---|---|
| seo-geo-audit | Full-site audit. It flags off-page weaknesses; this skill fixes them. |
| seo-local | Local citations, Google Business Profile, NAP consistency. Send all local citation work there. |
| geo-tracking | Measures AI citations and share of voice. This skill creates the mentions; geo-tracking measures them. |
| geo-visibility | Overall AI answer presence strategy (content, entities). This skill covers the off-site mention layer. |
| seo-keyword-research | Provides the keyword map that informs anchor text variation and target pages. |
| seo-content-blog | Creates the linkable content (studies, guides, guest articles) this skill promotes. |
| seo-content-product-page, seo-content-service-page, seo-content-collection-page | Build the money pages that deep links should point to. |
| seo-internal-linking | Distributes incoming link equity from linked pages to the rest of the site. |
| seo-technical | Redirects that preserve link equity, crawlability of linked URLs, canonical hygiene. |
| seo-schema-markup | Organization schema with sameAs pointing to the profiles built here. |

## Strategy doctrine

Internalize these principles before recommending any tactic. They are the reasoning layer; tactics change, doctrine does not.

### The five criteria of a good link

Evaluate every opportunity against all five. A link that fails on relevance or placement is rarely worth the effort, whatever its authority.

| # | Criterion | What to check | Why it matters |
|---|---|---|---|
| 1 | Source domain authority | Established site, real organic traffic, indexed pages | Authority transfers. A link from a trusted domain carries more weight and more referral traffic. |
| 2 | Topical relevance | Source covers your industry or the page topic | A link from a mid-authority site in your sector beats a stronger off-topic link. Relevance tells Google what you are an authority on. |
| 3 | Language match | Source site language = language of your target market | Language is a geographic signal. French links rank you in France; English links rank you in English-speaking markets. |
| 4 | Anchor naturalness | Varied anchors: brand, URL, generic, partial match | Fifty identical exact-match anchors is the single most readable footprint of manipulation. Natural profiles are messy. |
| 5 | Placement in content | In the body of an article, surrounded by relevant text | An in-content link beats a footer link, a sidebar link, or a slot in a 500-link resources page. Position signals editorial intent. |

External anchors are the opposite of internal anchors. Internal links use keyword anchors on purpose (see seo-internal-linking); external links should default to the brand name, the bare URL, or a generic phrase ("click here", "discover"). Keep exact-match keyword anchors on inbound external links close to zero: a keyword-heavy external anchor profile is the clearest over-optimization footprint there is, and it gets worse, not better, as more links arrive. (field heuristic from 115+ agency audits)

### Follow and nofollow: take both

Since 2019, Google treats nofollow as a hint, not a directive, and added rel="sponsored" and rel="ugc" (https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify). Practical consequences:

- A nofollow link from a powerful domain can still count, and it brings real referral traffic and a real mention.
- A profile that is 100% dofollow looks artificial, because natural profiles always accumulate nofollow links from social platforms, forums, and directories.
- Doctrine: nofollow builds the foundation (volume, naturalness, mentions, traffic), dofollow brings the juice. Never reject a relevant opportunity because the link is nofollow.

### Velocity: mimic organic growth

Acquire 2-5 links per day at most, spread over 90 days, rather than 100 links in a week (field heuristic from 115+ agency audits, reinforced after the Google spam update of August 2025). Why: organic popularity grows gradually. A sudden spike on a site with no viral content is a pattern that link-spam detection is built to catch. Slow is also operationally sustainable: 30 minutes a day beats a heroic weekend.

### The 95/5 rule

On any community, forum, or Q&A platform: 95% genuine value contribution, 5% links, and only where the link actually answers the question. Why: an account created yesterday whose three posts all contain links gets banned, and every link it placed disappears with it. The account that answers twenty questions well and links twice keeps its links for years. The 95% is not overhead; it is what makes the 5% permanent.

### Aged domains are gold

Preserve every domain the business has ever owned. Never let an old domain expire: its link history is an asset that takes years to rebuild. When consolidating, use permanent 301 redirects, which preserve link equity and history (see seo-technical for redirect implementation).

### Disavow: almost never

The disavow tool is generally useless. Google ignores spammy links by default, and disavowing on a hunch can only remove value, never add it. Use disavow in exactly one case: a manual action for unnatural links in Google Search Console. Random spam links pointing at the site (every site has them) require no action.

### An honest observation

Some niches still rank with thin content and aggressive pure link building. This is an observation, not a recommended strategy: those rankings are fragile, the sites burn down at every spam update, and the approach produces zero brand mentions, so it is invisible to AI answers. The durable play combines content worth linking to (see seo-content-blog) with the acquisition methods below.

### Buy versus grind, an honest tradeoff

There are two ways to earn the links Google still counts, and they suit different situations. The ninja linking methodology below is the zero-budget path: free, hands-on, and it doubles as the brand-mention play that feeds AI answers. But for a business with even a small budget, a single quality placement per month on a genuinely relevant thematic site, with the article written in-house to control quality and anchor, often returns more than hours spent grinding free directory and forum links by hand. The honest field position: stop pouring unpaid time into low-value free links when one well-chosen paid editorial placement plus a linkable asset moves the needle further. Keep the free ninja layer for brand presence and naturalness, concentrate paid effort on relevance and quality, never volume. The paid route carries a disclosure obligation, see The paid placement reality below. (field heuristic from 115+ agency audits)

## Workflow

### Step 1: Inventory the current profile (no paid tools required)

Build the picture from free sources first. No API keys, no subscriptions.

| Source | What it gives | Where |
|---|---|---|
| Google Search Console, Links report | Top linked pages, top linking sites, top anchor texts | Search Console > Links |
| Bing Webmaster Tools | An independent backlink index, often shows links GSC omits | Backlinks section, free account |
| Google brand search | Unlinked and linked mentions: search `"brand name" -site:yourdomain.com` | google.com |
| Google operators | Existing placements: `"yourdomain.com" -site:yourdomain.com`, `intitle:"brand name"` | google.com |
| Google Alerts | Ongoing mention monitoring for brand and key product names | google.com/alerts |

If the user has access to Ahrefs, Moz, or Semrush, use them as a complement for metrics (DR/DA, referring domain counts, competitor profiles), never as a prerequisite. The free sources above are enough to diagnose and act.

Two caveats on free sources: the GSC Links report is sampled and lagged (a representative subset, not every link, refreshed on a delay), and Google operator searches only surface pages Google chose to index. Treat the inventory as directionally complete: it reliably shows the profile's shape (anchors, relevance, targets, diversity), which is exactly what the diagnosis needs.

### Step 2: Diagnose the profile

Read the inventory against these signals:

| Signal | Healthy | Warning |
|---|---|---|
| Anchor distribution | Mostly brand and URL anchors, few exact match | One commercial keyword dominating the anchors |
| Follow ratio | Mixed follow and nofollow | 100% dofollow (artificial) or 100% nofollow (no equity) |
| Topical relevance | Majority of linking sites in or near the sector | Casino, pharma, or random foreign sites linking to a local bakery |
| Language | Linking sites match target market language | Profile dominated by a language you do not sell in |
| Link targets | Deep links to product, service, and blog pages | 95% of links to the homepage only |
| Velocity history | Gradual growth in referring domains | Spikes of dozens of domains in single weeks |
| Source diversity | Editorial, profiles, directories, forums, press | One single pattern repeated (all directories, all comments) |

Conclude with three lists: assets to protect, gaps to fill, risks to stop feeding (not to disavow, just to stop).

### Step 3: Mine competitors for opportunities

You cannot see a competitor's Search Console, but you can reverse most of their profile by hand:

1. Search `"competitorbrand"` and `"competitordomain.com" -site:competitordomain.com` to surface their placements and mentions.
2. Check their "as seen on", "press", and "partners" pages: every logo is a link source you can approach too.
3. Search `best [category]` and `[category] tools` or `top [category] companies`: every list that includes them and not you is a concrete target for the mention workflow below.
4. Search their brand on Reddit, Quora, and industry forums to find the communities where the conversation happens.
5. With optional paid tools, export their referring domains and filter by topical relevance.
6. If a competitor's profile shows an obvious ninja or spam footprint (hundreds of identical forum and directory links), do not copy it. Study instead the pages that rank for them organically and the editorial links pointing at those pages: that is the part actually earning the rankings.

### Step 4: Choose the strategy mix

Match the mix to the business. Recommended starting allocations:

| Business type | Primary plays | Secondary plays |
|---|---|---|
| Local business | Local citations (route to seo-local), local press, community sponsorships | Universal profiles, topical forums |
| SaaS / startup | SaaS directories, review platforms (G2, Capterra), integrations and partner pages, Product Hunt | Digital PR with product data, expert quotes |
| Ecommerce | Digital PR with data, linkable assets (guides, calculators), supplier and brand "where to buy" pages | Niche communities, review platforms |
| Content / media site | Expert quotes, broken link building, original studies | Universal profiles, syndication with canonical |
| Agency / services | Industry directories (Clutch class), expert quotes, guest articles on trade publications | Local citations if geo-bound, communities |

Whatever the mix, run two layers in parallel: the daily ninja linking cadence (Step 5 and methodology below) and one flagship play per quarter (a data study, a free tool, a benchmark) that earns the editorial links and press mentions.

### Step 5: Execute and track

Track every link in a simple table from day one. Memory does not scale past week two.

| Date | Spot | URL placed | Target page | Anchor | Follow/nofollow | Status |
|---|---|---|---|---|---|---|
| 2026-03-02 | Crunchbase profile | crunchbase.com/organization/brand | Homepage | Brand | nofollow | Live |
| 2026-03-03 | Industry forum thread | forum.example.com/thread/123 | Blog guide | Partial | dofollow | Pending moderation |

Review the table monthly: re-check that links are still live and indexed, log new referring domains from GSC, and feed mention counts to geo-tracking for the AI visibility side.

## What works in 2026, what is dead

### What works

| Tactic | Why it works | Evidence |
|---|---|---|
| Digital PR on proprietary data (annual study, benchmark, survey) | Journalists need numbers; a real dataset earns coverage no budget can buy. Links from press coverage of genuine studies passed the March 2026 spam update undamaged. | https://digitalapplied.com/blog/link-building-after-march-2026-strategies-post-update |
| Contextual editorial links | In-content links from relevant articles are the strongest pattern across the five criteria. | Doctrine, criteria 1-5 above |
| Linkable assets: free tools, calculators, templates, datasets | People link to things that do something. An asset earns links passively for years. | Field heuristic from 115+ agency audits |
| Broken link building | You offer the webmaster a fix, not a favor. Find dead links on resource pages in your topic, propose your equivalent page. | Field heuristic from 115+ agency audits |
| Partnerships and integrations | Partner pages, integration marketplaces, and co-marketing produce relevant dofollow links with real traffic. | Field heuristic from 115+ agency audits |
| Expert quotes (HARO-style source requests) | One good quote earns an editorial link, and quotes feed GEO directly: adding quotations measured up to +41% generative engine visibility in the Princeton GEO study. | https://arxiv.org/abs/2311.09735 |
| Podcast and interview links | Every guest you host, and every show you appear on, is an editorial link or a badge from their site. Recurring, relevant, and they compound as the show grows. | Field heuristic from 115+ agency audits |
| Embedded widget or tool on partner sites | A useful widget (calculator, live data, booking) placed on a partner page links back every time it renders. Serve it from your indexed root domain, not a separate app subdomain, or the link points at the wrong host. | Field heuristic from 115+ agency audits |
| Link from a page already ranking on page one | When you place a link inside one of your own (or a partner's) articles that already ranks on page one, Google already trusts and crawls that URL, so the new link is found and weighted faster than the same link in a brand-new article that has to earn trust first. | Field heuristic from 115+ agency audits |

The digital PR play has a GEO bonus worth spelling out to users: journalists cite the statistics, then LLMs cite the articles that repeat them. One proprietary number ("X% of [industry] does Y") can propagate through dozens of pages that all mention the brand as the source.

Broken link building, the concrete loop, since it is the most accessible editorial tactic:

1. Find resource pages in the topic: search `[niche] resources`, `[niche] useful links`, `inurl:links [niche]`.
2. Check their outbound links for dead targets (work through short lists by hand, or use a free link-checker browser extension).
3. Have, or build, the page that replaces the dead resource (see seo-content-blog).
4. Write to the page owner: report the dead link first (the favor), propose the replacement second (the ask). Expect single-digit conversion; each win is a relevant in-content link on a page whose entire purpose is linking out.

### What is dead or risky

Be frank with users about these. False hope wastes quarters.

| Tactic | Status | What happened |
|---|---|---|
| PBNs (private blog networks) | Dead | Footprint detection since March 2026: hosting patterns, registration data, and link graph shapes are flagged regardless of content quality. The network burns, and every site it links to is exposed. |
| Sponsored guest posts on high-DA general news sites | Devalued | Google devalued the "pay a big news site for a marketing post" pattern. The DA number survives; the link value does not. |
| Niche edits on aged domains with thin content | Devalued | Inserting links into old abandoned articles no longer transfers meaningful value; the host pages fail quality checks. |
| Bulk link buying (marketplaces, packages) | Risky | Volume sellers leave footprints across all their clients. You inherit the network's risk profile. |
| Comment spam, forum signature spam, profile-only blasts | Dead | Filtered or noindexed by platforms, ignored by Google, and they burn the accounts (see the 95/5 rule). |

### The paid placement reality

Present this honestly when users ask, because they will ask. Some practitioners budget one paid editorial placement per month (200-500 EUR) on a genuinely good topical site, writing the article themselves to control quality and anchor.

**Explicit risk warning: undisclosed paid links violate Google's spam policies.** Links that pass ranking credit in exchange for payment must carry rel="sponsored" to be compliant (https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify). A paid placement without it is a policy violation that can trigger link devaluation or a manual action. The compliant version (rel="sponsored") still delivers traffic, brand exposure, and an AI-citable mention, but not PageRank. If a user chooses the non-compliant route anyway, they must do it knowing the risk: present the tradeoff, never hide it, and never present paid dofollow links as a safe default.

## Ninja linking methodology

This is the signature acquisition method of this skill: go get your links yourself, one by one, for free, in places where you have a genuine reason to be present. No outreach emails, no waiting on third parties, no budget. It is quiet, hand-made, and it compounds: every spot also becomes a brand mention surface for AI answers.

### The four spot families

Full catalog with named platforms and footprints: `references/link-spot-categories.md`.

| Family | What it covers | Typical link | Main payoff |
|---|---|---|---|
| 1. Universal spots | Platform profiles, web 2.0 publishing, document and video sharing, Q&A, bookmarking. Work for any industry. Examples: Crunchbase, About.me, Gravatar, Product Hunt, Medium, Dev.to, Behance, GitHub, SlideShare, Vimeo, Quora. | Mostly nofollow, some dofollow | Foundation volume, branded search real estate, AI citation surfaces |
| 2. Directories and local citations | Business directories, industry directories, local citation sites. NAP consistency is mandatory: route all local citation work to seo-local. | Mixed | Trust signals, local pack, entity confirmation |
| 3. Topical forums | Forums in roughly 20 verticals: health, finance, real estate, travel, cooking, tech, marketing, automotive, home, legal, pets, gaming, parenting, sports, and more. Strict 95/5 rule. | Mixed, often dofollow in-thread | The most relevant links available for free, plus real referral traffic |
| 4. Communities, SaaS directories, review platforms | Subreddits, Facebook groups, Discord and Slack communities, plus SaaS and startup directories and review platforms (G2, Capterra, Trustpilot). | Mostly nofollow | The heaviest AI citation surfaces (see GEO layer below) |

### The 90-day progression

Start easy, finish hard. Reputation-gated spots (forums, communities) need account age and post history before a link is acceptable, so open those accounts in week one even though the links come in month two or three.

| Phase | Days | Focus | Cadence |
|---|---|---|---|
| 1. Foundation | 1-30 | Universal profiles, directories, review platform listings. Open forum and community accounts now, start contributing without links. | 2-5 links/day |
| 2. Participation | 31-60 | Q&A answers, first forum links where they genuinely answer the question, community contributions. | 2-5 links/day, 95/5 rule |
| 3. Authority | 61-90 | Established forum presence, harder communities, first expert quotes, inclusion requests on "best X" lists. | 2-5 links/day plus mention workflow |

Log everything in the tracking table from Step 5. The table is the deliverable that survives the 90 days: it becomes the re-verification checklist and the proof of work.

A sustainable weekly rhythm: five days of the 2-5 link cadence (about 30 minutes each), one day for the mention workflow and link-free community participation, one day off. Monthly: re-verify placed links, update the table, check GSC for new referring domains.

### Anchor plan by family

Decide anchors before placement, never improvise them. Defaults that keep the profile natural:

| Family | Default anchor | Keyword anchors? |
|---|---|---|
| Universal profiles | Brand name or bare URL | Never; profiles are brand surfaces |
| Directories | Exact business name (NAP) | Never |
| Topical forums | Natural phrase from the sentence, or bare URL | Rarely, only when the phrase is the honest way to cite the page |
| Communities and review platforms | Brand name | Never |

Reserve partial-match keyword anchors for editorial links, and keep them scarce: scarcity is what keeps them safe. Plan the keyword set with seo-keyword-research.

### Finding new spots

The catalog is a starting point; every niche has spots no list contains. Find them with search operators and footprints:

- `inurl:profile` plus the niche keyword, to surface platforms with public member profiles.
- `intitle:"add your site"` or `intitle:"submit your"` plus the niche, for directories and resource pages.
- `"powered by Discourse"` (or XenForo, vBulletin, phpBB, Flarum) plus the niche keyword, to find living forums on known platforms.
- `site:reddit.com [niche]` to map the subreddits where the audience already is.
- Mine competitors: their "as seen on" pages and brand searches reveal the spots that accept businesses like yours (their Search Console is out of reach, their public footprint is not).

### Verify every spot before use

Spot quality varies and decays. Before spending time on any spot, including those in the reference catalog, check four things:

1. **Indexed?** Search `site:thespot.com` on Google. A deindexed platform passes nothing.
2. **Moderated?** A spot overrun by spam is worthless and risky by association; a moderated spot is exactly where you want to be (moderation is what keeps it valuable).
3. **Follow or nofollow?** Inspect a published link's HTML. Both are acceptable (doctrine above), but you should know what you are getting.
4. **Real traffic?** Dead forums and ghost directories produce links no one ever sees, and AI models do not cite pages humans never visit.

## GEO layer: mentions over links

Answer engines cite pages where the brand appears, linked or not. Recall the headline numbers: mentions correlate at 0.664 with AI answer presence versus 0.218 for backlinks (Ahrefs, 75,000 brands, https://ahrefs.com/blog/ai-overview-brand-correlation/), and the large majority of AI citations point to earned media, on the order of 82% (medium confidence: single source, https://www.reporteroutreach.com/blog/unlinked-brand-mentions). Every profile, directory listing, review page, and forum thread built by the ninja methodology doubles as a potential citation surface. This section makes that layer deliberate.

### Citation surfaces

| Surface | Examples | Why AI cites it |
|---|---|---|
| Review platforms | G2, Capterra, Trustpilot | Massively cited in "best X" and "X alternatives" answers; structured, comparative, regularly updated. |
| Third-party "best of" lists | Blog roundups, trade press rankings | LLMs synthesize consensus from list pages; absence from the lists means absence from the answer. |
| Reddit and community threads | Subreddits, Hacker News, niche forums | Feeds model training and retrieval as authentic user consensus. Extreme volatility: Reddit's share of AI citations moved from roughly 60% to roughly 10% in a single month (https://www.semrush.com/blog/most-cited-domains-ai/). Participate cleanly; never bet the whole strategy on it. |
| Press and earned media | News coverage, industry publications, expert quotes | The dominant citation source overall; coverage of proprietary data compounds here. |
| Platform profiles and directories | Crunchbase, product directories, app marketplaces | Entity confirmation: consistent descriptions across profiles teach models who the brand is and what category it belongs to. |

### The mention workflow

Run this monthly alongside the link cadence:

1. **List the pages that already rank** for `best [category]`, `top [category]`, `[category] alternatives` in Google, and the pages AI assistants currently cite for those queries (measure with geo-tracking).
2. **Request inclusion with real arguments**: contact each list owner with concrete reasons the brand belongs (differentiator, data point, user count, price position), never a generic "please add us". Expect to update or provide the blurb yourself.
3. **Maintain review platform listings**: complete profiles, fresh screenshots, steady flow of genuine reviews (ask real customers; never fabricate reviews, platforms detect it and it is illegal in most markets).
4. **Answer relevant threads with value** on Reddit, forums, and Q&A under the 95/5 rule: the goal is the brand appearing in authentic conversations, not link drops.
5. **Keep entity descriptions consistent** across all profiles (same positioning sentence, same category), and mirror them in Organization schema with sameAs (see seo-schema-markup).

Strategy for what the brand should be cited about belongs to geo-visibility; measuring whether citations actually appear belongs to geo-tracking.

## Output format

Adapt the deliverable to the request:

**Link profile review.** Deliver: (1) inventory summary (referring domains, top anchors, follow ratio, top linked pages) with the free-source method used, (2) the diagnosis table from Step 2 with healthy/warning verdicts, (3) three lists: protect, fill, stop feeding, (4) a prioritized action plan mapped to the strategy mix table.

**Link acquisition plan.** Deliver: (1) strategy mix justified by business type, (2) the 90-day progression with weekly targets, (3) a starter spot list drawn from `references/link-spot-categories.md` filtered for the niche and verified, (4) the empty tracking table ready to fill, (5) one flagship play recommendation (data study or asset) with a concrete angle.

**Single opportunity evaluation.** Deliver: the five-criteria scorecard, the follow/nofollow status, an explicit risk note if money or policy is involved, and a take/skip verdict with the reasoning.

Always state which claims are measured (with the source URL) and which are field heuristics. Never present a heuristic as a measurement.

Punctuation, non-negotiable: never leave an em dash (U+2014) or an en dash (U+2013) in text published under the client's name or sent to a third party. Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. The em dash is the single most recognizable tell of AI-written text, and here it costs placements: an outreach email or a guest paragraph that reads as machine output gets deleted by the editor who was supposed to give the link. The rule covers outreach emails, guest post drafts, forum and comment contributions, profile and directory descriptions, and the blurbs you supply to list owners. Sweep for both characters before sending. Hyphens in compound words and ranges written with "to" are untouched.

## Common mistakes

| Mistake | Why it hurts | Do instead |
|---|---|---|
| Chasing DA/DR numbers only | High-authority off-topic links carry less weight than relevant mid-tier links, and metrics are third-party estimates, not Google data | Score every opportunity on all five criteria |
| Repeating one exact-match anchor | The clearest manipulation footprint there is | Default to brand and URL anchors; use keyword anchors sparingly (plan them with seo-keyword-research) |
| Rejecting nofollow opportunities | Loses mentions, traffic, and profile naturalness | Take both; nofollow is foundation, dofollow is juice |
| Burst velocity (50 links in a week) | Pattern detection flags unnatural spikes | 2-5 per day, 90-day horizon |
| Link drops without contribution | Accounts banned, links deleted, platform burned for the brand | 95/5 rule, always |
| Linking only to the homepage | Money pages and content get no direct equity | Deep link to product, service, collection, and blog pages; distribute further with seo-internal-linking |
| Letting old domains expire | Years of link history destroyed | Renew and 301 (seo-technical) |
| Disavowing preventively | Zero upside without a manual action; can remove value | Disavow only on documented manual actions |
| Buying PBN or bulk packages | Network footprints transfer their risk to you, post-March-2026 detection is structural | Spend the same budget on one data study or one quality asset |
| Ignoring unlinked mentions | Invisible to link tools but central to AI visibility | Run the mention workflow monthly; measure with geo-tracking |
| Betting the GEO strategy on Reddit alone | Citation shares swing by an order of magnitude month to month | Spread across review platforms, lists, press, and profiles |
| Skipping spot verification | Dead, deindexed, or spam-flooded spots waste the daily cadence | Four-point check before every new spot |

## Sources

- Ahrefs, brand mentions vs backlinks correlation with AI Overview presence, 75,000 brands: https://ahrefs.com/blog/ai-overview-brand-correlation/
- Google, evolution of nofollow and introduction of rel="sponsored" and rel="ugc" (2019): https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify
- Digital Applied, link building outcomes after the March 2026 spam update: https://digitalapplied.com/blog/link-building-after-march-2026-strategies-post-update
- Aggarwal et al., GEO: Generative Engine Optimization (Princeton et al.), quotation impact on generative visibility: https://arxiv.org/abs/2311.09735
- Semrush, most cited domains in AI answers and Reddit citation volatility: https://www.semrush.com/blog/most-cited-domains-ai/
- Reporter Outreach, earned media share of AI citations (single source, medium confidence): https://www.reporteroutreach.com/blog/unlinked-brand-mentions
- Velocity, 95/5 rule, spot family effectiveness: field heuristics from 115+ agency audits (2024-2026), not third-party measurements.
