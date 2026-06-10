---
name: geo-tracking
description: The canonical measurement skill for AI visibility, fully doable without paid tools or API keys. Sets up GA4 AI traffic reporting (custom channel group with a complete referrer regex placed above Referral), runs a monthly 50-100 buyer prompt panel to compute brand mention rate, citation rate, and share of voice versus competitors across ChatGPT, Perplexity, Google AI Overviews, Claude, and Gemini, and reads server logs for verified AI crawler and assistant fetcher hits as a leading indicator. Use this skill whenever the user wants to track AI traffic, measure ChatGPT or Perplexity referrals, see AI assistant visits in GA4, monitor brand mentions in AI answers, run prompt tracking, compute share of voice, build a monthly GEO report, prove AI visibility to a client, or detect AI bots in server logs. It is the repo reference for measurement. For building the prompt panel itself, use seo-keyword-research. For improving citation rates once gaps are found, use geo-visibility.
license: MIT
metadata:
  author: "Sorank (https://sorank.com)"
  version: "1.0.0"
---

# GEO Tracking: Measuring AI Visibility

AI visibility is measurable today, for free, at three layers of the funnel. Each layer answers a different question:

| Layer | Data source | Question it answers | Lag |
|---|---|---|---|
| Traffic | GA4 | How many visits and conversions do AI assistants send? | Trailing (after the click) |
| Answers | Prompt panel | What do AI engines say about the brand when buyers ask? | Current state |
| Retrieval | Server logs | Are AI systems reading the pages right now? | Leading (before citations appear) |

Run all three. GA4 alone undercounts structurally, panels alone miss revenue proof, logs alone say nothing about what answers contain. The combination is the measurement system; paid platforms are an optional layer on top, never the starting point.

This skill is the canonical measurement reference in this repo. Build the prompt panel with seo-keyword-research; act on the gaps with geo-visibility.

## Company knowledge first (Obsidian)

If the working environment contains an Obsidian vault or any local knowledge base (a folder of .md notes, often with a .obsidian directory), read the relevant notes before acting: brand and product facts, target keywords, competitors, and the SEO action log of what was already tried. Ground every recommendation in that context instead of asking the user for facts the vault already holds. At the end of the session, append the actions taken to the vault's SEO action log so the next session starts informed. Vault structure, read-first and write-back protocols: the obsidian-brain skill.

## When to use this skill

Use this skill when the user:

- Asks how much traffic comes from ChatGPT, Perplexity, Gemini, Claude, or Copilot.
- Wants AI traffic visible in GA4, Looker Studio, or a client report.
- Wants to track brand mentions, citations, or share of voice in AI answers (prompt tracking, AI rank tracking).
- Asks whether AI bots crawl the site, or what ChatGPT-User hits in the logs mean.
- Needs a monthly GEO report, a baseline before a GEO project, or proof of GEO results for a client.
- Asks whether to buy an AI visibility tool (Profound, Otterly, Brand Radar, Semrush AI tools).

## Workflow

### Day zero: capture the baseline

Do this before any GEO work starts, because every later claim of progress is judged against it; without a baseline, improvements are invisible and unprovable.

1. Create the custom GA4 channel group (Layer 1 below) and annotate the property with the date.
2. Run the full prompt panel once: that run is month zero.
3. Pull 30 days of server logs and count verified AI hits per agent (Layer 3 below).
4. Screenshot the current AI answers for the 10 most commercial prompts, brand present or not.

### Layer 1: AI traffic in GA4

#### Step 1: Know what the default gives you

Since May 13, 2026, GA4 includes a default "AI Assistant" channel group. It captures referrers from chatgpt, gemini, and claude, but not perplexity and not copilot, and it is not retroactive: it only classifies data from its activation forward (https://www.searchenginejournal.com/google-analytics-adds-ai-assistant-as-default-channel-group/574974/). Useful as a zero-effort baseline, insufficient as the measurement.

#### Step 2: Build a custom channel group (the real setup)

Why: full assistant coverage, and a definition you control and can extend when new assistants appear.

1. In GA4: Admin, Data display, Channel groups, create a new channel group (or copy the default).
2. Add a channel named "AI Assistants" with the condition Session source matches the regex:

```
chatgpt\.com|chat\.openai\.com|perplexity\.ai|claude\.ai|gemini\.google\.com|copilot\.microsoft\.com|bing\.com/chat|deepseek\.com|grok\.com|meta\.ai|mistral\.ai|you\.com
```

3. Drag the "AI Assistants" channel above Referral in the channel order. Why: channel groups evaluate top-down, and these sources all qualify as referrals; placed below Referral, every AI session is swallowed by Referral first and the channel stays empty (setup walkthrough: https://www.analyticsmania.com/post/ai-traffic-in-google-analytics-4/).
4. Custom channel groups are not retroactive either. Create the group on day one of any GEO project and annotate the date; the baseline starts there.
5. Review the regex quarterly and append new assistant domains.

#### Step 3: Read the numbers honestly

Structural limit: native mobile and desktop apps frequently send no referrer, and those sessions land in Direct. Measured AI traffic is a floor, not the total. State this in every report; never present the AI channel as exhaustive, and never read a Direct uptick as noise without considering assistant apps.

#### Step 4: Report value, not just volume

AI assistant visits convert about 4.4x better than organic search visits (Semrush study, reported at https://authoritytech.io/blog/ai-traffic-attribution-how-to-track-chatgpt-perplexity-gemini). The pattern: the assistant did the comparison work, so the visitor arrives pre-sold. Always report conversion rate and conversions next to session counts; AI traffic that looks small by sessions is often material by revenue.

Also segment landing pages: in Explore, build a free-form report with Landing page as dimension and a filter on Session source matching the AI regex. The URLs receiving AI sessions are the pages engines already like; their structure is the template to replicate via geo-visibility.

#### Step 5: Know what Google Search Console cannot tell you

Google includes AI Overviews impressions and clicks inside the regular Search performance data with no separate breakdown (https://developers.google.com/search/docs/appearance/ai-features). There is no "AI Overviews" filter to pull. Consequence: the prompt panel (Layer 2) is the only direct observation of AI Overviews presence available without paid tools. Treat unexplained GSC click drops on stable rankings as a possible AI Overview substitution effect, then verify with the panel.

### Layer 2: The prompt panel protocol (share of voice)

This is the heart of the skill: a reproducible, free protocol measuring what buyers actually see in AI answers.

Why a panel at all: AI engines publish no impression count and no search volume for a brand mention, so visibility inside them is a black box. The panel is how you mime ranking measurement: send the questions buyers would actually ask, record whether the brand appears, and track that rate over time. It is a sampled proxy, not a traffic metric, and that is the best signal available without paid tools (field heuristic from 115+ agency audits).

#### Step 1: Freeze the panel

Take the 50-100 buyer prompt panel built with seo-keyword-research (patterns: "best [category] for [use case]", "[brand] vs [competitor]", "is [brand] worth it", "how to [job to be done]"). Freeze it. Comparable months require identical prompts; edit the panel quarterly at most, append rather than replace, and version it (v1, v2) so trend charts never silently mix panels.

Sizing and cadence: 50-150 prompts is the realistic working range, scaled to how broad the topic is, not bigger for its own sake. Replay monthly by default; move to weekly only for fast-moving or hotly contested topics where a month is too coarse. Daily replay rarely earns its cost in money and noise (field heuristic from 115+ agency audits).

#### Step 2: Replay monthly under controlled conditions

- Same week each month (for example the first business week).
- Fresh sessions: logged out or temporary chat, memory and personalization off, no custom instructions. Why: personalized answers measure your history, not the market's visibility.
- Note the country and language and keep them constant; answers differ materially by locale.
- For a multilingual market, build a separate panel per language AND culture, not a translation of one panel. The reference sources an engine draws on differ between cultural groups even inside one country (Flemish versus French-speaking Belgium, for example), so run a distinct setup and a distinct report per locale, and set the engine region by country and city where the interface allows it (field heuristic from 115+ agency audits).
- Engines: ChatGPT (search enabled), Perplexity, Google AI Overviews (run the prompt as a Google query and record the AI Overview if one appears), Claude, Gemini. Keep the engine set constant.

#### Step 3: Record one row per prompt and engine

| Column | Values |
|---|---|
| date | YYYY-MM |
| prompt | verbatim text |
| engine | chatgpt, perplexity, google-aio, claude, gemini |
| brand_mentioned | yes or no |
| cited_with_link | yes or no |
| position | 1st, 2nd-3rd, listed, absent |
| sentiment | positive, neutral, negative |
| competitors_mentioned | comma-separated names |
| notes | free text, screenshot reference |

Keep screenshots for wins and losses: clients believe screenshots, and they settle disputes about what an answer said.

#### Step 4: Compute the metrics

| Metric | Formula | Read it as |
|---|---|---|
| Mention rate | prompts with brand_mentioned yes / total prompts, per engine and overall | Presence in answers |
| Citation rate | prompts with cited_with_link yes / total prompts | Presence as a clickable source |
| Share of voice | brand mentions / (brand mentions + tracked competitor mentions) | Competitive position |
| Trend | current month minus previous month, per metric per engine | Direction |

Alert threshold: investigate any relative drop greater than 20% on mention rate or share of voice, but confirm with a re-run before acting (next step explains why).

Worked example, panel of 50 prompts, ChatGPT, one month:

- brand_mentioned yes on 9 prompts: mention rate 9/50 = 18%
- cited_with_link yes on 4 prompts: citation rate 4/50 = 8%
- Mentions across the answers: brand 9, competitor A 21, competitor B 13: share of voice 9 / (9 + 21 + 13) = 20.9%
- Next month the mention rate reads 14% (7/50): that is a 22% relative drop, above the alert threshold. Re-run the panel; if confirmed, list the lost prompts and hand them to geo-visibility as rewrite targets.

#### Step 5: Respect non-determinism

AI answers are non-deterministic: the same prompt can name different brands across two consecutive runs. One run of one prompt is noise. Practical discipline:

- Run each prompt 2-3 times per engine when feasible and score the majority outcome, or accept that single-run numbers only become meaningful as multi-month trends across the whole panel.
- Never report a single-prompt, single-run change as a result. Aggregate first (panel-level rates), trend second (2-3 months), conclude third.
- Budget honestly: 50 prompts across 3 engines at one run each is roughly half a day of manual work per month (field practice). Start with 50 prompts and 3 engines rather than skipping months on an oversized panel.

### Layer 3: Server logs (the leading indicator)

Why logs: referrer analytics only see clicks, but assistants read pages while composing answers. A user-triggered fetcher hit means a human asked something and the assistant pulled your page into the conversation, whether or not anyone clicked. Log activity rises before citations and traffic do, which makes it the earliest signal a GEO effort is working.

#### Step 1: Identify the agents

| User agent | Operator | A hit means |
|---|---|---|
| GPTBot | OpenAI | Training data crawl |
| OAI-SearchBot | OpenAI | Crawl for the ChatGPT search index (eligibility to appear) |
| ChatGPT-User | OpenAI | A live user conversation fetched the page right now |
| ClaudeBot | Anthropic | Training data crawl |
| Claude-User | Anthropic | A live user conversation fetched the page right now |
| PerplexityBot | Perplexity | Index crawl |
| Perplexity-User | Perplexity | A live user conversation fetched the page right now |

Filter the access logs for these strings (a plain text search is enough; no special tooling required). The full crawler table, robots.txt implications, and rendering notes live in the seo-technical skill, references/ai-crawlers.md: that file is the repo's canonical crawler reference.

#### Step 2: Verify before trusting (anti-spoofing)

User agent strings are trivially forged by scrapers. Verify that hit IPs fall inside the official published ranges before counting them:

- OpenAI GPTBot: https://openai.com/gptbot.json
- OpenAI OAI-SearchBot: https://openai.com/searchbot.json
- Anthropic bots: https://claude.com/crawling/bots.json
- PerplexityBot: https://www.perplexity.com/perplexitybot.json

Count only verified hits in reports; unverified hits are noise at best and scraper traffic at worst.

#### Step 3: Read the signals

- Rising OAI-SearchBot coverage: the site is entering or refreshing in the ChatGPT search index.
- ChatGPT-User, Claude-User, Perplexity-User hits: pages are being used in live answers. Track which URLs receive them; those are the AI-favored pages, and their structure (answer-first blocks, tables, definitional sentences) is what to replicate via geo-visibility.
- Zero verified AI hits over a month, while competitors are visible in answers: check robots.txt and server-side blocking with seo-technical before blaming content.

### Layer 4 (optional): paid platforms

Adopt only after the DIY system runs, and keep the DIY panel as the control.

| Tool | What it adds over DIY |
|---|---|
| Semrush AI Visibility Index | Large shared prompt corpus, competitive benchmarks |
| Profound | Enterprise answer monitoring, volume across regions |
| Ahrefs Brand Radar | AI mentions alongside classic SEO data |
| Otterly | Lightweight prompt tracking automation |

Why DIY first: it is free, the methodology is transparent, the prompt set matches your actual buyers (vendor indexes use their own corpora), and the numbers stay comparable over time even if you change vendors later.

### Measurement cadence

| Frequency | Task |
|---|---|
| Monthly | Replay the prompt panel, compute rates, produce the report |
| Monthly | Review GA4 AI channel sessions, conversions, landing pages |
| Monthly | Count verified AI bot hits per agent from logs |
| Quarterly | Review the GA4 regex for new assistant domains |
| Quarterly | Revise the prompt panel (versioned, append-first) |
| On alert | Re-run the panel to confirm any over 20% relative drop |

## Reading the signals together

The three layers diagnose each other. Use this table before drawing conclusions from any single number.

| Symptom | Likely meaning | Action |
|---|---|---|
| Panel shows mentions, GA4 shows near zero AI sessions | Assistant apps send no referrer; sessions hide in Direct | Keep reporting both; never conclude from GA4 alone |
| High mention rate, low citation rate | Brand known to models, pages not retrieved or not quotable | Passage citability work in geo-visibility |
| Verified fetcher hits but no mentions in answers | Retrieval without selection: fetched, not quoted | Answer-first rewrite of the fetched URLs |
| Zero verified AI bot hits over a month | Blocking, rendering, or indexation problem | robots.txt and server HTML checks in seo-technical |
| Mention rate swings wildly month to month | Panel too small or sessions not clean | 50+ prompts, fresh sessions, 2-3 runs per prompt |
| GSC clicks drop on stable rankings | Possible AI Overview substitution | Verify with the panel on the affected queries |

## Rules and thresholds

| Rule | Value | Why |
|---|---|---|
| GA4 AI channel position | Above Referral | Top-down evaluation; below Referral the channel captures nothing |
| Retroactivity | None, default or custom | GA4 channel groups classify forward only; baseline starts at creation |
| GA4 reading | Floor, not total | Assistant apps send no referrer; the rest lands in Direct |
| Panel size | 50-100 prompts, frozen | Below 50 the rates are noise; unfrozen panels break trends |
| Panel revision | Quarterly at most, versioned, append-first | Comparability is the entire value of the panel |
| Session hygiene | Memory off, logged out, fixed locale, same week | Personalization and locale shifts contaminate the measurement |
| Runs | 2-3 per prompt when feasible, majority outcome | Single runs of a non-deterministic system prove nothing |
| Alert threshold | Drop over 20% on mention rate or share of voice | Below that, normal variance; above, investigate and re-run |
| Bot hits | Count only IP-verified hits | User agents are trivially spoofed |
| Reporting | Conversions next to sessions | AI visits convert about 4.4x better; volume alone undersells |

## Output format

Produce the monthly GEO report in this structure:

```
# GEO Report, [Month YYYY], [site]

## 1. AI traffic (GA4, floor values)
- AI assistant sessions: N (previous month: N, delta %)
- AI conversions: N, conversion rate vs organic search
- Top 5 landing pages from AI assistants
- Note: app-based assistant visits land in Direct; these figures are a floor.

## 2. Answer visibility (prompt panel vN, N prompts, locale)
- Mention rate per engine: table with previous month and delta
- Citation rate per engine: same table format
- Share of voice vs [competitor list]: overall and per engine
- Wins: prompts where the brand appeared this month and not last month
- Losses: the reverse, each with a screenshot reference

## 3. Retrieval signals (server logs, IP-verified only)
- Verified hits per agent (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, PerplexityBot, Perplexity-User), with trend
- Top 10 URLs fetched by user-triggered fetchers

## 4. Actions for next month
- Pages to rewrite or create, from losses and gaps (hand to geo-visibility)
- Entity or third-party surface fixes (hand to geo-visibility)
- Technical blockers found (hand to seo-technical)
- Panel notes: prompts to add at the next quarterly revision (do not edit mid-quarter)
```

Keep every monthly report in the same format: the comparability of the document is part of the measurement.

## Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Comparing periods before and after channel group creation | Fake growth story | Channel groups are not retroactive; baseline starts at creation, annotate it |
| Leaving the AI channel below Referral | Empty channel, false "no AI traffic" conclusion | Order the channel above Referral |
| Trusting the default AI Assistant group as complete | Misses Perplexity and Copilot entirely | Custom group with the full regex |
| Presenting GA4 AI numbers as the total | Systematic undercount presented as truth | State the floor caveat in every report |
| Concluding from one run of one prompt | Acting on noise | Aggregate rates, 2-3 runs or multi-month trends |
| Editing prompts every month | Trend lines compare different things | Freeze the panel, version it, revise quarterly |
| Testing logged in with memory on | Measures personalization, not visibility | Fresh sessions, memory off, fixed locale |
| Counting bot hits by user agent string | Scrapers counted as AI visibility | Verify IPs against the official JSON ranges |
| Reporting sessions without conversions | AI channel dismissed as too small | Report the conversion multiple next to volume |
| Buying a platform before any DIY baseline | No control group, vendor-locked numbers | DIY first, platform later as a layer |

## Cross-references

- seo-keyword-research: builds the 50-100 buyer prompt panel this skill measures (do this first).
- geo-visibility: turns measured gaps into citability fixes, entity work, and third-party surface plans (canonical citability rules).
- seo-technical: canonical AI crawler reference (references/ai-crawlers.md), robots.txt and rendering checks when retrieval signals are absent.
- seo-geo-audit: the bundled audit script (scripts/seo_audit.py) scores pages flagged by this skill's reports.
- seo-backlinks: brand mentions workflow when share of voice lags despite good content.

## Sources

- Search Engine Journal, GA4 adds AI Assistant default channel group (May 13, 2026; chatgpt, gemini, claude; not perplexity or copilot; not retroactive): https://www.searchenginejournal.com/google-analytics-adds-ai-assistant-as-default-channel-group/574974/
- Analytics Mania, tracking AI traffic in GA4 (custom channel group, regex, ordering above Referral): https://www.analyticsmania.com/post/ai-traffic-in-google-analytics-4/
- AuthorityTech, AI traffic attribution guide, reporting the Semrush finding that AI visits convert about 4.4x better than organic: https://authoritytech.io/blog/ai-traffic-attribution-how-to-track-chatgpt-perplexity-gemini
- OpenAI published crawler IP ranges: https://openai.com/gptbot.json and https://openai.com/searchbot.json
- Anthropic published crawler IP ranges: https://claude.com/crawling/bots.json
- Perplexity published crawler IP ranges: https://www.perplexity.com/perplexitybot.json
- Items marked "field practice" are practitioner workload estimates, not studies; adjust to the team's capacity.
