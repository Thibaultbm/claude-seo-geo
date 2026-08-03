# Comparison Page Patterns

Fill-in wireframes per page family, the criteria-selection method, verdict formulas, and the segment page structure. Companion to SKILL.md phase 3. Replace every `{placeholder}`, in the language of the site.

## Choosing the criteria

Do this before looking at who wins each row, otherwise the criteria unconsciously bend toward your strengths.

1. List every dimension a buyer weighs, from sales calls, support tickets, review sites and the objections in the vault.
2. Cut anything a buyer cannot verify or does not care about.
3. Keep 6 to 12. Below 6 the comparison looks rigged; above 12 nobody reads it.
4. Order them by how much they influence the decision, not by how you score.
5. Only now, fill in the values. If you win every row, the criteria are wrong: go back to step 1 and add the dimensions buyers raise when they choose someone else.

Rows worth including that most pages omit, because they are the ones actually searched: real total cost including setup and overage, time to first result, migration effort, support response time, contract and cancellation terms, what happens to your data if you leave.

## Family 1: head to head, "X vs Y"

```
URL:   /{you}-vs-{competitor}/
Title: {You} vs {Competitor}: {the deciding difference} ({year})       (50-60 chars)
H1:    {You} vs {Competitor}
Schema: FAQPage; Article or WebPage; Organization
```

```
[VERDICT, first 100 words]
{You} suits {situation A: who, doing what, at what scale}.
{Competitor} suits {situation B}.
The difference that decides it: {the single dimension that matters most}.
{One sentence naming the case where the competitor is the better choice.}

[COMPARISON TABLE]  real <table>, 6-12 criteria, same order for both
| Criterion | {You} | {Competitor} |
| Price ({period}) | {price, as text} | {price, as text} |
| {criterion} | {value} | {value} |
...
Verified {date} from {source for each side}.

[PER-OPTION DETAIL]  same criteria, same order, one H2 each
H2: What {You} does better
{2-4 claims, each with a concrete proof: number, screenshot, doc link.}
H2: What {Competitor} does better
{Genuine, specific, unhedged. This block is why the rest is believed.}

[BEST FOR]
H2: Which one should you choose
- Choose {You} if: {situation}, {situation}, {situation}
- Choose {Competitor} if: {situation}, {situation}
- Choose neither if: {situation} -> {what to look at instead}

[OUR LIMITATIONS]
H2: Where {You} falls short
{Stated in your own words, before a review site states them for you.}

[MIGRATION]  optional but high intent
H2: Switching from {Competitor} to {You}
{What transfers, what does not, how long it takes, what it costs.}

[METHODOLOGY]
H2: How we compared
{What was tested, on which plans, when, by whom, from which sources.}

[FAQ]  3+ real questions, including the uncomfortable ones
H3: Is {Competitor} better than {You}?
H3: Why is {Competitor} cheaper / more expensive?
H3: Can I migrate from {Competitor}?
H3: {question from real sales calls}

[CROSS-LINKS]  your product page, your pricing page, the comparison hub,
               the other head-to-head pages
[CTA]  {trial, demo, quote}, with the risk-reducer next to it
```

## Family 2: alternatives, "{brand} alternatives"

The highest-yield family for a challenger. Two variants, same skeleton, opposite psychology.

- **"{competitor} alternatives"**: the reader has decided to leave. Acquisition. Be genuinely useful about all options, including ones that are not you, and you earn the recommendation.
- **"{your brand} alternatives"**: the reader is doubting you. Retention. Owning this page means the doubts get answered by you, on your domain, with your migration path one click away. Never leave it to a review site.

```
URL:   /{brand}-alternatives/
Title: {n} best {brand} alternatives in {year} (compared)              (50-60 chars)
H1:    {brand} alternatives
Schema: FAQPage; ItemList; Article or WebPage
```

```
[VERDICT, first 100 words]
The best {brand} alternative depends on why you are leaving:
{reason 1} -> {option}. {reason 2} -> {option}. {reason 3} -> {option}.
{One sentence: when staying with {brand} is still the right call.}

[WHY PEOPLE LEAVE {BRAND}]
{3-5 real reasons, sourced from review platforms, quoted and linked.}
Real reasons, not strawmen. This block is what makes the page trusted, and
it is where the long-tail queries live.

[COMPARISON TABLE]  every option, same criteria
| Option | Price | {criterion} | {criterion} | Best for |

[ONE SECTION PER ALTERNATIVE]  same structure each, 4 to 8 options
H2: {n}. {Option name}
{One-line positioning.} 
Best for: {specific situation}
{2-3 strengths with proof} 
Limitations: {2-3, specific}
Pricing: {as text, verified {date}}
{Screenshot} {Link to their site}

Include yourself, positioned honestly, and not automatically first. A list where
the author's product is number one with no caveat is read as an advertisement by
both humans and models.

[HOW TO CHOOSE]
H2: How to pick the right {brand} alternative
{The 4-6 questions a reader should answer about their own situation.}

[METHODOLOGY + date]
[FAQ]  including "is there a free alternative to {brand}", "how do I migrate"
[CROSS-LINKS + CTA]
```

## Family 3: best for, "best {category} for {use case}"

```
URL:   /best-{category}-for-{use-case}/
Title: {n} best {category} for {use case} ({year})                     (50-60 chars)
H1:    Best {category} for {use case}
Schema: FAQPage; ItemList
```

Same skeleton as family 2, with three differences: the verdict names one winner for the stated use case rather than routing by reason; every option is judged against the needs of that use case specifically, not in general; and the criteria are the ones that matter for that use case only. The value of the page is the narrowing, so a generic "best {category}" list with the use case bolted onto the title is not this page type.

State the selection rule explicitly: how options were shortlisted, what was excluded and why. A list with no stated inclusion rule is not a comparison, it is an opinion.

## Family 4: comparison hub

Build it once three or more comparison pages exist.

```
URL:   /compare/  or  /comparisons/
H1:    Compare {category} options
```

```
[INTRO]  what these comparisons cover, how they are verified, how often updated
[MASTER TABLE]  every option, the 5-6 criteria shared across all comparisons
[LINK GRID]
- {You} vs {Competitor A}     - {Competitor A} alternatives
- {You} vs {Competitor B}     - {Competitor B} alternatives
- Best {category} for {use case 1}, {use case 2}
[METHODOLOGY, applied to all children]
```

The hub is the internal-linking asset: it collects links earned by individual comparisons and distributes authority across the set, and it prevents the children from cannibalizing each other by giving each a clear parent (seo-internal-linking).

## Family 5: audience and segment pages

Same product, one customer type. The failure mode is find and replace, which produces near-duplicates that compete with each other.

```
URL:   /for-{segment}/  or  /{category}-for-{segment}/
Title: {Product} for {segment}: {their specific outcome}               (50-60 chars)
H1:    {Product} for {segment}
Schema: FAQPage; Service or Product; Organization
```

```
[HEADLINE + PROBLEM, first 100 words]
H1: {Product} for {segment}
{The segment's problem, in the segment's own vocabulary, with the detail
that only someone who works with them would know.}
This paragraph is the whole test of the page. If it would read identically
for a different segment, the page should not exist separately.

[SEGMENT-SPECIFIC BENEFITS]  3 to 6
Not the generic feature list. What this segment gets, in their units:
{billable hours, order volume, class size, case load, campaign count}.

[THEIR WORKFLOW]
H2: How {segment} use {product}
{The actual sequence they follow, with their tools and their constraints.}
The block that makes the page non-duplicable, and the one that requires
talking to real customers rather than imagining them.

[PROOF FROM THE SAME SEGMENT]
{Logos of recognizable peers, reviews from this segment, one case study
with a number.} Proof from a different segment does not transfer.

[SEGMENT OBJECTIONS]
H2: {the blocker specific to this segment}
{Each segment has one, and it is rarely price: compliance, team size,
integration with the tool they cannot leave, seasonality, procurement.}

[PRICING FOR THIS SEGMENT]  the relevant plan, in their terms
[FAQ]  in the segment's vocabulary
[CTA]  phrased for this segment: "book a team demo" and "start free"
       are different asks
[CROSS-LINKS]  sibling segment pages and the main product page, so a
               mis-routed visitor self-corrects instead of leaving
```

Before building a set of segment pages, check that each one has: distinct vocabulary, a distinct primary problem, distinct proof available, and real search demand. Segments that fail any of those become a section on the main page instead of a page of their own.

## Verdict formulas

The verdict block is the passage that gets quoted, so it is worth writing last and rewriting twice.

- Routing verdict (alternatives pages): "If you are leaving {brand} because of {reason}, choose {option}. If it is {other reason}, choose {other option}."
- Situational verdict (head to head): "Choose {A} if {concrete situation with a number}. Choose {B} if {different concrete situation}."
- Single-winner verdict (best-for): "{Option} is the best {category} for {use case}, because {the one criterion that decides it}. {Runner-up} wins if {condition}."
- Honest-exit verdict: "If {situation}, neither of these fits; look at {category or option} instead."

Rules: name names, use a concrete situation rather than an adjective, put a number in it where possible, and never resolve every case to your own product. Repeat the verdict at the end of the page, so the reader who scrolled arrives at the same conclusion as the reader who did not.

## Pre-publish checklist

- [ ] Verdict in the first 100 words, naming who each option suits
- [ ] Real HTML table, 6 to 12 criteria, identical order for every option
- [ ] Criteria chosen before scoring, from buyer decision factors
- [ ] At least one row where a competitor genuinely wins, unhedged
- [ ] Own limitations stated in a named block
- [ ] Every price as HTML text, with the verification date
- [ ] Every third-party claim traceable to a public source, linked
- [ ] Best-for verdicts per use case
- [ ] Methodology block: what, how, when, by whom
- [ ] FAQ with the uncomfortable questions answered
- [ ] Screenshots of each option, real and current
- [ ] Author with demonstrable experience of the options compared
- [ ] Cross-links to the hub, the product page and the pricing page
- [ ] Comparative advertising rules of the target market checked
- [ ] Verification date recorded in the vault, refresh scheduled
