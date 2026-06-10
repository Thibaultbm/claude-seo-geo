# Audit deliverable templates

Two formats. Pick by audience: Template A for practitioners and teams, Template B for a non-technical owner. Both follow the same rules of tone.

## Rules of tone (both templates)

1. Write in the language of the site being audited.
2. Open with what is genuinely good. Most sites do several things right, and a report that starts with praise gets read to the end. If nothing is good, find the asset (old domain, real photos, solid reviews) and start there.
3. The verdict comes first, in one line, and it is one of three: ready to grow (scale content now), short fix list first (1-3 weeks of corrections, then scale), or rebuild before investing (blocking problems make content spend wasteful today).
4. Numbers over adjectives: "23 of 31 images have no alt text" beats "many images lack alt text".
5. State what was not verified and why (no GSC access, speed not measured, backlinks not crawled). Unverified is honest; guessed is fatal.
6. Never invent a rule to sound thorough. If a finding does not map to the checklist or to a measured source, leave it out.

## Template A: full audit report

```
# SEO + GEO audit: {domain}
Date: {date} | Pages reviewed: {list} | Competitors benchmarked: {list or "none provided"}

## Verdict
{One line: ready to grow / short fix list first / rebuild before investing} {One sentence of justification.}

## What is already good
- {3-6 bullets, specific and measured}

## Top 3 priorities
1. {Highest-impact fix, why it matters, expected effect}
2. ...
3. ...

## Findings by category
### Technical and indexation [OK / Fix / Blocking]
{Measured facts, gaps, the fix. Repeat per category: tags, images, architecture,
content, keywords, blog, GEO, conversion, e-commerce, local, backlinks.}

### AI visibility (GEO) [OK / Fix / Blocking]
- Crawler access: {AI search bots blocked or allowed, training bots}
- Rendering: {server-rendered or client-rendered, consequence}
- Citability: {passage structure, FAQ, stats and sources, entity consistency}
- Measurement: {can the site see its AI traffic today}

## Competitor benchmark
{Per competitor: the pages compared, the measurable gaps (word count, structure,
links, citability), what to copy and what to skip.}

## Action plan, in order
| # | Action | Category | Effort | Skill to use |
|---|---|---|---|---|
{Ordered list. Effort: S/M/L. Map each action to the specialized skill.}

## Not verified
{What was out of reach and what access would unlock it.}
```

## Template B: plain-language email to the owner

Rules on top of the shared ones: no acronyms at all (write "Google's free tool that shows how your site appears in search" instead of GSC the first time), explain every technical term in everyday words the moment it appears ("alt text: the text description of an image that Google reads, since it cannot look at pictures"), keep it under 600 words, no tables.

```
Subject: Review of {domain}: {verdict in plain words}

Hi {first name},

I went through {domain} in detail. The short version: {verdict sentence in
plain words, honest}.

What you are doing well:
{2-4 bullets, plain words, genuinely encouraging}

What is holding the site back, in order of impact:
1. {Finding in plain words + what it costs + the fix in one sentence}
2. ...
3. ...
{3-5 items maximum. Each technical term explained inline.}

{If competitors were provided: one short paragraph per competitor: what they
do that works, in plain words, and which of those moves makes sense to copy.}

{One paragraph on AI visibility in plain words: when people ask ChatGPT or
similar tools for recommendations in your field, here is whether your site
can appear today and why.}

The honest bottom line: {ready to grow / fix the list above first / the site
needs deeper work before content spending makes sense}.

{Sign-off}
```

## Per-competitor paragraph pattern (either template)

For each competitor page benchmarked: name the page compared, give 2-3 measured gaps (word count, structure, internal links, citability elements), and one explicit "copy this" plus one "skip this" (not everything competitors do is worth copying; say which is which and why).
