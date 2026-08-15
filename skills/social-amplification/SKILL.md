---
name: social-amplification
description: "Turn one pillar asset into platform-native social content that drives branded search and feeds the third-party surfaces AI engines cite (YouTube, Reddit, LinkedIn). Input: a pillar article or asset. Output: native posts per platform, prioritized by search and AI return over vanity reach. Use for social media for SEO, content distribution or repurposing, YouTube SEO, Reddit or LinkedIn content, brand awareness for search, or showing up when people ask ChatGPT."
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# Social Amplification: Distribution for SEO and GEO

This skill covers how social distribution and content repurposing serve search rankings and AI visibility, and how they do not, so the effort goes where it actually pays back.

The framing that governs everything below: social distribution does not move rankings directly. It is an indirect channel. Treated as a direct ranking lever it wastes budget; treated as a feeder system for branded search and AI citation surfaces it compounds. This skill is honest about which is which, because the wrong belief here burns quarters on vanity metrics.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use this skill

Use this skill when the user wants to:

- Distribute or amplify content they already published (a blog post, a study, a guide).
- Repurpose one pillar asset into a week or a month of native social content.
- Improve YouTube discoverability for search and AI answers (titles, descriptions, transcripts).
- Show up on Reddit, LinkedIn, or YouTube specifically because AI engines cite those surfaces.
- Appear when people ask ChatGPT, Perplexity, or Gemini, through social presence rather than on-site work.
- Understand whether social media helps their Google SEO (the answer is indirect, and this skill explains how).
- Build branded search demand that supports rankings and AI visibility.

Boundaries, stated plainly so the work lands in the right skill:

| The user wants | Use this skill? | Where it belongs |
|---|---|---|
| To produce and distribute social content, repurpose assets | Yes | here |
| To earn a backlink or place a brand mention on a third party | No | seo-backlinks (mention and link acquisition workflow) |
| To know which surfaces AI engines cite, and passage citability rules | No | geo-visibility (canonical citability and surface list) |
| To measure social referrals, branded search, AI traffic | No | geo-tracking (canonical measurement) |
| The linkable asset itself (the study, the guide) | No | seo-content-blog (creates what this skill distributes) |

## Strategy doctrine

Internalize this before recommending any tactic. The value of social distribution to SEO and GEO is indirect, through three mechanisms. State each one honestly to the user, including the limits.

### Mechanism 1: distribution, traffic, and branded search

Social posts carry no PageRank. Links from social platforms are nofollow almost without exception, so they pass no ranking equity to the destination. What amplification actually does is put content in front of people, generate visits and engagement, and, most valuably, create branded search: people who saw the brand on social later search the brand name (or "brand + category") on Google.

Why branded search matters for SEO and GEO: branded search volume correlates with organic rankings and with AI visibility. Brand web mentions correlate with AI Overview brand presence at 0.664 versus 0.218 for backlinks (Ahrefs, 75,000 brands, https://ahrefs.com/blog/ai-overview-brand-correlation/). Rising branded search is a demand signal an engine can read; a brand people look for by name is a brand engines treat as an entity worth surfacing. Measure branded search growth in Google Search Console (filter queries containing the brand name); the setup lives in geo-tracking.

### Mechanism 2: AI citation surfaces

YouTube, Reddit, and LinkedIn are among the most cited domains in AI answers (https://www.semrush.com/blog/most-cited-domains-ai/), and Perplexity overweights YouTube, Reddit, and user-generated content (https://www.tryprofound.com/blog/ai-platform-citation-patterns). Being absent from those surfaces means being absent from a large share of AI answers, regardless of how strong the brand's own site is.

The division of labor with geo-visibility: that skill owns the list of which surfaces engines cite and the reasoning behind it. This skill owns how to actually publish well on each one (the platform playbook below). Do not re-derive the citation surface list here; build presence on the surfaces geo-visibility identifies.

### Mechanism 3: entity and brand-mention signals

Models learn a brand as an entity from repeated co-occurrence of the brand name with its category across independent surfaces. Consistent, active social presence adds those co-occurrences: a complete LinkedIn company page, a YouTube channel, and genuine forum participation all repeat "brand + category" in places models read.

The boundary with seo-backlinks: the structured workflow for building brand mentions (listicle inclusion requests, review platforms, the monthly mentions cadence) belongs to seo-backlinks. When the work is "get the brand mentioned or cited on a third party", route to seo-backlinks. This skill's contribution to the entity is the native content published on owned social channels and the genuine community participation around it.

### The honest summary to give users

Say this directly when asked whether social helps SEO: social signals (likes, shares, follower counts) are not a direct Google ranking factor, a position Google has stated publicly and repeatedly. Social helps SEO and GEO indirectly, by generating branded search, by building presence on the third-party surfaces AI engines cite, and by reinforcing the brand entity. The indirect path is real and worth the work; the direct claim ("shares push you up Google") is false and should be corrected.

## Workflow: the repurposing pipeline

One pillar asset feeds many native posts. The pipeline turns published content into distribution without producing net-new long-form for every channel.

### Step 1: Start from a pillar asset

The input is a substantial piece already built by seo-content-blog: a guide, an original study, a benchmark, a data-rich article. Repurposing is downstream of content; without a pillar asset worth distributing, there is nothing to amplify. Original data and strong opinions repurpose best, because they give each platform something specific to react to.

### Step 2: Atomize into platform-native formats

Break the pillar into its component ideas, then rebuild each idea in the native format of the target platform. The rule that decides everything: do not post the same link everywhere. Each platform rewards content created for it and penalizes content that is obviously a link dump from elsewhere.

| Pillar element | Native repurpose | Platform |
|---|---|---|
| The core argument or finding | A talking-head or screen-recording video, titled as the buyer query | YouTube |
| A counterintuitive data point | A text post or short thread that states the finding and invites discussion | LinkedIn, X |
| A how-to section | A step list written directly in the post body, no "link in bio" gate | LinkedIn, Reddit (where genuinely on-topic) |
| A definition or framework | A carousel or a single annotated image | LinkedIn, Instagram |
| A surprising stat | A short vertical clip with on-screen text and captions | YouTube Shorts, TikTok, Reels |
| The full asset | Referenced in genuine community discussion, only where it answers the question | Reddit, Discord, Slack, forums |

### Step 3: Distribute on a cadence

Stagger releases rather than firing everything at once. A pillar asset can feed one to two weeks of social content; spreading the atoms keeps a steady presence and lets each format find its audience. Sequence: native posts on owned channels first (YouTube, LinkedIn, X), genuine community participation second and only where the asset is the honest answer.

### Step 4: Engage under the 95/5 rule

Distribution without engagement is broadcasting. Reply, answer, and discuss; this is what converts reach into branded search and into the authentic conversations engines read. On any community (Reddit, forums, Discord, Slack), apply the 95/5 rule strictly: 95% genuine contribution, 5% links or self-promotion, and only where it truly fits. Never astroturf (fake accounts, coordinated upvotes, planted praise): platforms detect it, bans erase the work, and the reputational damage outlasts any short-term gain. The 95/5 rule and the no-astroturfing principle are the same discipline seo-backlinks applies to communities; honor it here too.

### Step 5: Close the loop back to keyword research

What performs in social reveals demand. A post that overperforms, a question asked repeatedly in the comments, a Reddit thread that will not die: each is a candidate topic for the next pillar asset. Feed those signals back to seo-keyword-research so the next cycle starts from validated demand. Distribution is not the end of the line; it is a listening instrument for the content engine.

## Platform playbook

Prioritized by SEO and GEO return, not by reach or follower count. Spend first where search and AI citation payback is highest.

### Priority 1: YouTube

YouTube is two things at once: the second largest search engine in the world, and a heavily cited AI surface (Perplexity overweights it, https://www.tryprofound.com/blog/ai-platform-citation-patterns; field heuristic from 115+ agency audits puts YouTube near 15% of AI answer citations). It earns the top slot because it pays back on both fronts simultaneously.

Why text matters more than production value here: AI engines and YouTube search read text (title, description, transcript, captions), not the pixels of the video. A polished video with a thin description is invisible to the systems that drive discovery.

| Lever | Do this | Why |
|---|---|---|
| Title | Phrase it as the search query a buyer types ("how to descale a tankless water heater"), not a clever headline | Title-query match drives both YouTube search and AI retrieval |
| Description | Write a rich, keyword-relevant description with the key points in text, links to the related on-site article | The description is indexable text; it is what search and AI read |
| Transcript and captions | Always provide accurate captions or a transcript; upload a corrected one rather than trusting auto-captions | Engines read the transcript; captions are the video's body text |
| On-site embed | Embed the video on the matching article on the site | Keeps people on-page, adds a media format, supports the page's multi-format citability (see geo-visibility) |

Embedding discipline, consistent with seo-content-blog: embed YouTube videos on articles, never upload video files directly to the site. The embed gives the page a media format while YouTube does the hosting and the search distribution.

### Priority 2: Reddit and communities

Reddit, forums, Discord, Slack, and niche groups feed the consensus that models learn and retrieve. They earn priority 2 because authentic community discussion is exactly what AI engines treat as real-world signal, and because genuine participation there is one of the few ways to influence what models "know" about a category.

Two hard rules govern this surface:

1. The 95/5 rule, strictly. An account whose every post links to the brand gets banned, and every contribution it made disappears with it. The account that helps twenty times and links twice keeps its standing for years. Never astroturf.
2. Volatility, stated honestly. Reddit's share of ChatGPT citations moved from roughly 60% to roughly 10% within about a month after platform shifts (https://www.semrush.com/blog/most-cited-domains-ai/). Participate cleanly because it is good practice regardless, and never bet the whole strategy on a single platform whose citation share can collapse on one partnership change.

The acquisition-of-mentions angle (getting the brand named in threads as a deliberate program) overlaps seo-backlinks; route the systematic mention workflow there. This skill's job is the genuine, sustained participation that makes any of it credible.

### Priority 3: LinkedIn

LinkedIn earns priority 3 for B2B because it is three useful things at once: an entity-corroboration surface (a complete company page repeats "brand + category" in a place models read), a brand search engine in its own right, and a cited AI surface. For B2C with no professional audience, demote it.

- Complete the company page fully, and use the canonical one-line brand description verbatim (the same sentence used on the site, G2, Crunchbase, and every profile). Consistency is the entity signal; this is the same canonical description geo-visibility and seo-backlinks specify.
- Post native text and document posts (no "link in comments" gating of the substance); LinkedIn suppresses reach on posts that push people off-platform immediately.
- Repurpose pillar findings as standalone insights, not as teasers for a click.

### Priority 4: X, Instagram, TikTok, and others

These carry brand signal and can drive traffic, but their direct SEO contribution is low; treat them by audience fit, not by default.

| Platform | Realistic SEO/GEO role | When to invest |
|---|---|---|
| X | Branded search, real-time discussion, some AI citation | If the audience and the category live there |
| Instagram | Brand awareness, visual repurposing | Visual or consumer brands |
| TikTok | Reach and branded search, growing video citation | Younger or consumer audiences; repurpose Shorts here |
| Pinterest | Referral traffic for visual and how-to niches | Recipes, home, design, e-commerce visuals |

Be honest with users: posting on every platform to "be everywhere" dilutes effort. Pick the two or three where the audience actually is and the search and AI payback is real.

## Rules and thresholds

### Repurposing rules

| Rule | Threshold | Why |
|---|---|---|
| Native format per platform | One bespoke adaptation per channel, never the same link everywhere | Each algorithm rewards native content and suppresses off-platform link dumps |
| Pillar-to-social ratio | One pillar asset feeds one to two weeks of social atoms | Sustainable cadence without net-new long-form per channel |
| Captions and transcripts | Required on every video, accuracy checked | Engines read the text track, not the video |
| Title as query | Video and post titles phrased as the buyer's search query | Drives both platform search and AI retrieval |
| Community contribution | 95% value, 5% links, only where it fits | Link-only accounts get banned and the work is erased |
| Astroturfing | Never | Detected, banned, reputationally toxic, and it backfires |
| Punctuation | Zero em dashes and zero en dashes, replaced by commas | The most recognizable AI-writing tell, and social audiences call it out fastest |

Punctuation, non-negotiable: never leave an em dash (U+2014) or an en dash (U+2013) in anything posted under the client's name. Replace every one with a comma; use a colon, a period or parentheses when a comma loses the sense. Social feeds are where readers are quickest to spot machine output and say so publicly, and a post read as AI-generated kills the reach the repurposing was meant to earn. The rule covers post copy, video titles and descriptions, thread text, captions and community replies. Sweep for both characters before scheduling. Hyphens in compound words and ranges written with "to" are untouched.

### Cadence (field heuristic from 115+ agency audits, not a measured optimum)

| Surface | Sustainable rhythm |
|---|---|
| YouTube | One well-optimized video per pillar asset, quality over frequency |
| LinkedIn | Two to four native posts per week from repurposed material |
| Reddit and communities | Daily genuine participation, links rare and only on-topic |
| X | Several short posts per week, threads from pillar findings |

Treat these as starting rhythms to sustain, not targets to hit at the cost of quality. Frequency without value trains audiences and algorithms to ignore the account.

## GEO layer

Social amplification is, in large part, a GEO activity, because the surfaces it builds on are the surfaces AI engines cite. Make this explicit in any plan.

| Action in this skill | GEO payoff |
|---|---|
| Publishing optimized YouTube videos with transcripts | Becomes citable on a surface Perplexity overweights and that carries a meaningful share of AI citations |
| Genuine Reddit and community participation | Adds the brand to the authentic consensus models retrieve, on a heavily cited (if volatile) surface |
| Complete, consistent LinkedIn company page | Reinforces the brand entity and corroborates it on a cited B2B surface |
| Repurposing that drives branded search | Branded search and brand mentions correlate with AI visibility (0.664 versus 0.218, Ahrefs) |

Citability of the content itself (answer-first passages, self-contained chunks, sourced statistics) is owned by geo-visibility; apply its rules when writing the YouTube description, the LinkedIn post, or any text that an engine may quote. A transcript or a post written answer-first is more quotable than a meandering one. The Princeton GEO study measured that adding statistics and citations raised generative visibility in its benchmark (https://arxiv.org/abs/2311.09735); the same logic applies to social text engines can read.

## Measurement

Social amplification is judged on indirect outcomes, not on likes. Route all measurement to geo-tracking; the signals that matter here are:

| Signal | Where to read it | What it proves |
|---|---|---|
| Branded search volume | Google Search Console, queries containing the brand name | Distribution created demand that reaches search |
| AI assistant referral traffic | GA4 custom channel group (geo-tracking) | Social presence is sending visits via AI answers |
| Social referral traffic and conversions | GA4 | Distribution is driving qualified visits, not just impressions |
| Brand mention and citation rate | The monthly prompt panel (geo-tracking) | Presence on cited surfaces is translating into AI mentions |

Do not report follower counts or like totals as outcomes. They are inputs at best; the outcome is branded search, referral traffic, conversions, and AI citations. State this honestly to anyone asking for a social report.

## What works versus what is dead or a myth

Answer these plainly; the wrong belief wastes effort and budget.

### What works

| Tactic | Why it works |
|---|---|
| Repurposing one pillar asset into native formats per platform | Maximizes reach per unit of content and respects each algorithm |
| YouTube videos titled as queries, with transcripts, embedded on-site | Wins on two search engines and a cited AI surface at once |
| Genuine community participation under 95/5 | Builds standing that makes occasional links and mentions credible and durable |
| Consistent entity presence across profiles | Reinforces the brand the way models learn it (co-occurrence) |
| Closing the loop from social signals to new pillar topics | Turns distribution into demand research for the content engine |

### What is dead or a myth

| Claim or tactic | Verdict | Reality |
|---|---|---|
| "Buying followers or likes" | Dead, risky | Zero SEO value, fake engagement is detected and purged, and it can damage standing on the platform |
| "Social shares push you up Google" | Myth | Social signals are not a direct Google ranking factor, a position Google has stated publicly. The benefit is indirect (branded search, citation surfaces, entity) |
| "Post the same link to every platform" | Counterproductive | Algorithms suppress non-native content and outbound-link dumps; reach collapses and nothing repurposes |
| "Automated DM and post blasting" | Dead, risky | Spam detection bans the accounts; it generates noise, not branded search, and harms the brand |
| "Be on every platform to be everywhere" | Wasteful | Effort dilutes; two or three platforms matched to the audience outperform a thin presence on ten |
| "Social links pass link equity" | False | Social links are almost universally nofollow and pass no PageRank; their value is traffic and mentions, not equity (see seo-backlinks on nofollow) |

## Output format

Deliver a social amplification plan with these blocks:

1. Pillar asset and repurposing map: the source asset, then a table of atoms (pillar element, native format, platform, title or hook written out) covering one to two weeks.
2. Platform priority and rationale: which two or three platforms to focus on for this specific audience, ordered by SEO and GEO return, with the reason each made or missed the list.
3. Per-platform execution notes: for YouTube, the query-style title, the description outline, and the on-site embed target; for communities, the subreddits or forums and the 95/5 contribution plan; for LinkedIn, the canonical one-line description and the post angles.
4. Cadence: the sustainable rhythm per platform, framed as a heuristic, not a quota.
5. Measurement handoff: the branded search, referral, and citation signals to track, with a pointer to geo-tracking and an explicit note that follower and like counts are not the outcome.
6. Loop-back: which social signals to watch for new pillar topics, routed to seo-keyword-research.

State which claims are measured (with the source URL) and which are field heuristics. Never present a heuristic as a measurement.

## Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Treating social as a direct ranking lever | Effort spent on vanity metrics that do not move rankings | Frame social as indirect: branded search, citation surfaces, entity |
| Posting the identical link everywhere | Algorithms suppress reach; nothing is native | One bespoke repurpose per platform |
| Uploading video with a thin description and no captions | Invisible to YouTube search and AI engines | Rich text description, accurate transcript, query-style title |
| Link-dropping in communities | Accounts banned, every contribution erased | 95/5 rule, links only where they answer the question |
| Astroturfing (fake accounts, bought engagement) | Detection, bans, reputational damage | Genuine participation only |
| Reporting likes and followers as results | Measures nothing about SEO or GEO | Report branded search, referral traffic, conversions, citations (geo-tracking) |
| Spreading thin across every platform | Diluted effort, weak presence everywhere | Two or three platforms matched to the audience |
| Betting the AI-visibility plan on Reddit alone | One platform shift can collapse the citation share | Diversify across YouTube, communities, and owned channels |
| Distributing without engaging | Broadcasting, no branded search created | Engage under 95/5; reach becomes demand only through interaction |
| Repurposing thin content | No pillar substance to atomize, nothing performs | Start from a real asset (study, guide) built by seo-content-blog |

## Cross-references

- seo-content-blog: builds the pillar assets this skill repurposes and distributes (start there).
- seo-keyword-research: receives the loop-back signals from social to choose the next pillar topics.
- seo-backlinks: owns brand mention and link acquisition on third parties, including listicle inclusion and the monthly mentions workflow.
- geo-visibility: owns which surfaces AI engines cite and the passage citability rules to apply to social text.
- geo-tracking: owns all measurement (branded search in GSC, AI and social referrals in GA4, the prompt panel).
- seo-schema-markup: Organization schema with sameAs pointing to the social profiles built here.
- seo-local: entity and profile consistency for local businesses (route local profiles there).
- seo-geo-audit: full-site audit; run the bundled audit script from the seo-geo-audit skill (scripts/seo_audit.py) to collect on-page facts.
- seo-technical, seo-internal-linking, seo-content-product-page, seo-content-service-page, seo-content-collection-page: the on-site work that social distribution supports rather than replaces.

## Sources

- Semrush, most cited domains in AI answers, including YouTube, Reddit, and LinkedIn, and Reddit citation volatility (roughly 60% to 10%): https://www.semrush.com/blog/most-cited-domains-ai/
- Profound, AI platform citation patterns, Perplexity overweighting YouTube, Reddit, and user-generated content: https://www.tryprofound.com/blog/ai-platform-citation-patterns
- Ahrefs, brand mentions versus backlinks correlation with AI Overview presence (0.664 versus 0.218), 75,000 brands: https://ahrefs.com/blog/ai-overview-brand-correlation/
- Aggarwal et al., GEO: Generative Engine Optimization (Princeton et al.), impact of statistics and citations on generative visibility: https://arxiv.org/abs/2311.09735
- The position that social signals are not a direct Google ranking factor, and that social links are nofollow and pass no PageRank, is stated publicly by Google and verifiable in its guidance; no single URL is cited here to avoid misattribution.
- Items marked "field heuristic from 115+ agency audits" (YouTube near 15% of AI citations, cadence figures) are practitioner observations from agency audit calls (2024-2026), not controlled studies.
