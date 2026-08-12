# Investigation protocol: exports, commands, and the incident record

Load this at the start of a live investigation. It covers how to pull the right data, how to run the bundled script, the spot-check commands per hypothesis, and the incident record to leave behind.

## Pulling the exports

In Search Console, open the Performance report, set the date range, then Export. The export contains Queries.csv, Pages.csv, Countries.csv, Devices.csv, Dates.csv and Search appearance.csv.

Pull two exports:

- Healthy period: a stable stretch before the drop.
- Damaged period: after the drop settled, avoiding the transition days.

Rules that decide whether the comparison means anything:

1. Equal length. Comparing 28 days against 90 measures the calendar.
2. Same property. A domain property and a URL-prefix property of the same site return different numbers, and mixing them invents a drop.
3. Same filters. If one export is filtered to Web and the other is not, the difference is the filter.
4. Avoid the transition. A period straddling the drop date averages the two states and flattens the signal.
5. Mind the boundaries of known reporting events. Any comparison spanning 27 April 2026 crosses the Search Console impression logging fix, so impressions, CTR and average position are not comparable across it. Clicks are.
6. The last three days are incomplete. Exclude them.

For the timeline, one Dates.csv covering both periods, ideally 90 days or more, so weekday seasonality and the pre-drop baseline are both visible.

## Running the script

    # Date the drop: cliff or slope, and the onset
    python3 scripts/gsc_diff.py --dates Dates.csv

    # Which pages carry the loss, grouped by the first two path segments
    python3 scripts/gsc_diff.py healthy/Pages.csv damaged/Pages.csv --sections 2

    # Which queries carry it, ignoring the noise below 10 clicks
    python3 scripts/gsc_diff.py healthy/Queries.csv damaged/Queries.csv --min-clicks 10 --top 30

    # Machine readable, for a report or a diff against a later run
    python3 scripts/gsc_diff.py healthy/Pages.csv damaged/Pages.csv --json

It reads localized exports (clicks, clics, klicks and so on) and handles thousand separators and comma decimals, so a French or German account works without touching the file. Exit code is 1 when a material drop is present, 0 when it is not, 2 on a parsing error.

What each output block answers:

| Block | Question it settles |
|---|---|
| TOTALS | Which metric actually moved |
| SHAPE | Which mechanism produced it, in one named verdict |
| Concentration | Page-level, template-level, or sitewide |
| BIGGEST LOSSES | Where to look, with a per-row reason |
| DISAPPEARED ENTIRELY | Whether this is an indexation problem |
| GAINERS | Whether the cause is internal (cannibalization, redistribution) |
| BY SECTION | Which template or directory to inspect |

Read GAINERS before accepting any external cause. Internal redistribution is the most commonly missed explanation, because nobody looks for a winner when they are investigating a loss.

## Spot checks per hypothesis

    # Indexability as served: meta robots and the header version templates hide
    curl -sIL https://example.com/page/ | grep -i "x-robots-tag"
    curl -sL https://example.com/page/ | grep -io '<meta name="robots"[^>]*>'

    # Canonical as served
    curl -sL https://example.com/page/ | grep -io '<link rel="canonical"[^>]*>'

    # robots.txt, checking for a shipped staging config
    curl -s https://example.com/robots.txt

    # Status and redirect chain, flagging chains longer than one hop
    curl -sIL https://example.com/old-url/ | grep -iE "^HTTP|^location"

    # Does the site answer differently to Googlebot (blocking, or dynamic rendering)
    curl -sI -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" https://example.com/ | head -1

    # Is the content in the HTML at all (the AI visibility test)
    curl -sL https://example.com/page/ | grep -c "a sentence from the page"

For a full rendering verdict, use scripts/render_check.py from the seo-ai-site-builders skill. For a full technical sweep, scripts/seo_audit.py from seo-geo-audit.

## The 30-minute triage

When the answer is needed before a call, in this order. Stop as soon as one returns positive, because it explains everything downstream:

1. Manual Actions and Security Issues in Search Console. Binary, two clicks.
2. robots.txt and meta robots on three URLs. One curl each.
3. Homepage status code and TLS validity.
4. `--dates` timeline. Cliff or slope, and the onset date.
5. The release log for the onset date.
6. `--sections` comparison. Sitewide or one template.
7. Data Anomalies page for the period.

That sequence catches the majority of drops that have a single, fixable cause, and when it catches nothing it has still eliminated the cheap explanations, which is what earns the time for the full investigation.

## The incident record

Write this into the vault action log (obsidian-brain) when the investigation closes. It is what makes the second occurrence cheap.

    ## {date}: traffic drop on {property}

    Detected: how, and by whom
    Shape: cliff on {date} | slope from {date} to {date}
    Magnitude: {n} clicks lost per {period}, {n} percent
    Mechanism: visibility | ranking | click-through | demand
    Concentration: sitewide | section {path} | {n} URLs
    Cause: {confirmed cause}
    Evidence: the test that confirmed it, with the observed value
    Ruled out: {cause}, because {evidence}. Repeat per candidate.
    Fix: what shipped, and on what date
    Re-measure: {date}, comparing {exact periods}
    Outcome: filled in at re-measure, including "not recovered" when that is the answer

The "Ruled out" lines are the part people skip and the part that pays. They are what stops the next investigation from re-testing the same five hypotheses, and they are what makes the diagnosis defensible when a client asks whether it could have been something else.

Record "not recovered" honestly when it happens. A log that only contains successes is a log nobody can learn from, and structural losses (queries absorbed by AI answers, a discontinued product, a market that shrank) are real outcomes that belong in the history.
