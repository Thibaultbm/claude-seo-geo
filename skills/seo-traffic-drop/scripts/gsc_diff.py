#!/usr/bin/env python3
"""gsc_diff.py: locate a traffic drop inside Search Console exports.

Two modes.

Comparison mode takes two Search Console performance exports of the same
dimension (Queries.csv or Pages.csv), one from the healthy period and one from
the damaged period, and reports what moved: the shape of the drop (visibility,
ranking, click-through rate, or a reporting artifact), which rows carry the
loss, how concentrated it is, what disappeared entirely, and what gained while
the rest fell.

Timeline mode takes a single Dates.csv covering both periods and dates the drop:
a cliff on one day points at an event (a deploy, a manual action, an outage),
a slope over weeks points at an update rollout, decay, or competition.

Zero dependencies, Python 3.9+, read only. It parses local CSV files, nothing else.

Usage:
    python3 gsc_diff.py before/Queries.csv after/Queries.csv
    python3 gsc_diff.py before/Pages.csv after/Pages.csv --sections 2
    python3 gsc_diff.py --dates Dates.csv
    python3 gsc_diff.py before/Pages.csv after/Pages.csv --json

Options:
    --dates FILE    timeline mode: find the drop date in one Dates.csv export
    --top N         rows to list per table (default 15)
    --min-clicks N  ignore rows below this click count in the healthy period
    --sections N    also aggregate URL rows by the first N path segments
    --json          machine readable output

Exports come from the Search Console performance report: set the date range,
then Export. Both files must cover periods of equal length, or the comparison
measures the calendar rather than the site.

Exit code 0 if no material drop is found, 1 if one is (10 percent of clicks or
more), 2 on a usage or parsing error.
"""

import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

MATERIAL_DROP = 0.10          # share of clicks lost before this is called a drop
CONCENTRATION_SHARE = 0.80    # share of the loss used to measure concentration
FLAT = 0.05                   # a metric moving less than this counts as flat
POSITION_MATERIAL = 1.0       # places lost before a ranking change counts

# Search Console exports are localized. Match headers by keyword, in any language
# the operator happens to have their account set to.
CLICK_WORDS = ("click", "clic", "klick", "clique", "cliques", "kliks")
IMPRESSION_WORDS = ("impression", "impresion", "impressionen", "impressioni", "exibic")
CTR_WORDS = ("ctr", "taux de clic", "clickrate", "porcentaje de clic")
POSITION_WORDS = ("position", "posicion", "posizione", "posicao", "platzierung")
DATE_WORDS = ("date", "fecha", "datum", "data")


def normalize(text):
    text = unicodedata.normalize("NFKD", str(text or ""))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.strip().lower()


def parse_number(raw):
    """Parse a Search Console cell: 1,234 or 1 234 or 3.5% or 12,4 or empty."""
    if raw is None:
        return 0.0
    text = str(raw).strip().replace(" ", " ").replace("%", "")
    if not text:
        return 0.0
    text = text.replace(" ", "")
    # Decide which separator is the decimal one: the last one, when it leaves
    # 1 or 2 trailing digits (1,234 is a thousand separator, 12,4 is a decimal).
    if "," in text and "." in text:
        text = text.replace(",", "") if text.rfind(".") > text.rfind(",") else \
            text.replace(".", "").replace(",", ".")
    elif "," in text:
        tail = text.split(",")[-1]
        text = text.replace(",", ".") if len(tail) <= 2 else text.replace(",", "")
    try:
        return float(text)
    except ValueError:
        return 0.0


def match_column(headers, words):
    for index, header in enumerate(headers):
        if any(word in header for word in words):
            return index
    return None


def read_rows(path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as handle:
            sample = handle.read(4096)
            handle.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except csv.Error:
                dialect = csv.excel
            return [row for row in csv.reader(handle, dialect) if any(c.strip() for c in row)]
    except OSError as exc:
        sys.stderr.write("Cannot read %s: %s\n" % (path, exc))
        raise SystemExit(2)


def load_table(path):
    """Return (dimension_label, {key: metrics}) from a Queries or Pages export."""
    rows = read_rows(path)
    if len(rows) < 2:
        sys.stderr.write("%s has no data rows\n" % path)
        raise SystemExit(2)
    headers = [normalize(h) for h in rows[0]]
    cols = {
        "clicks": match_column(headers, CLICK_WORDS),
        "impressions": match_column(headers, IMPRESSION_WORDS),
        "ctr": match_column(headers, CTR_WORDS),
        "position": match_column(headers, POSITION_WORDS),
    }
    if cols["clicks"] is None and cols["impressions"] is None:
        sys.stderr.write(
            "%s does not look like a Search Console export (no clicks or "
            "impressions column found in: %s)\n" % (path, ", ".join(rows[0]))
        )
        raise SystemExit(2)

    table = {}
    for row in rows[1:]:
        key = row[0].strip()
        if not key:
            continue
        record = table.setdefault(key, {"clicks": 0.0, "impressions": 0.0,
                                        "position_weight": 0.0})
        clicks = parse_number(row[cols["clicks"]]) if cols["clicks"] is not None else 0.0
        impressions = (parse_number(row[cols["impressions"]])
                       if cols["impressions"] is not None else 0.0)
        record["clicks"] += clicks
        record["impressions"] += impressions
        if cols["position"] is not None:
            position = parse_number(row[cols["position"]])
            # Search Console averages position by impression, so weight it the same way.
            record["position_weight"] += position * max(impressions, 1.0)
    for record in table.values():
        base = max(record["impressions"], 1.0)
        record["position"] = record["position_weight"] / base if record["position_weight"] else 0.0
    return rows[0][0].strip() or "row", table


def totals(table):
    clicks = sum(r["clicks"] for r in table.values())
    impressions = sum(r["impressions"] for r in table.values())
    weight = sum(r["position_weight"] for r in table.values())
    return {
        "clicks": clicks,
        "impressions": impressions,
        "ctr": clicks / impressions if impressions else 0.0,
        "position": weight / impressions if impressions and weight else 0.0,
        "rows": len(table),
    }


def pct_change(before, after):
    if not before:
        return None if not after else float("inf")
    return (after - before) / before


def fmt_pct(value):
    if value is None:
        return "n/a"
    if value == float("inf"):
        return "new"
    return "%+.1f%%" % (value * 100)


def classify_shape(before, after):
    """Name the mechanism behind the totals. Rules are ordered, first match wins."""
    d_clicks = pct_change(before["clicks"], after["clicks"])
    d_impr = pct_change(before["impressions"], after["impressions"])
    d_pos = after["position"] - before["position"] if before["position"] and after["position"] else 0.0
    d_ctr = pct_change(before["ctr"], after["ctr"])

    if d_clicks is None or d_clicks >= -MATERIAL_DROP:
        if d_impr is not None and d_impr <= -0.20:
            return ("REPORTING ARTIFACT OR LOST LONG TAIL", [
                "Impressions fell %s while clicks held at %s." % (fmt_pct(d_impr), fmt_pct(d_clicks)),
                "Clicks are the metric that pays. Before treating this as a loss, rule out the "
                "two known reporting events: the num=100 removal of September 2025, and the "
                "Search Console impression logging fix of 27 April 2026 that corrected roughly "
                "50 weeks of inflated impressions.",
                "If both periods sit on the same side of those dates, look instead for lost "
                "long-tail visibility, which costs impressions before it costs clicks.",
            ])
        return ("NO MATERIAL CLICK DROP", [
            "Clicks moved %s, under the 10 percent threshold." % fmt_pct(d_clicks),
            "If the complaint is about sessions rather than clicks, the problem is downstream "
            "of Search Console: analytics, consent, tagging, or a different channel.",
        ])

    if d_impr is not None and d_impr <= -0.50 and after["clicks"] <= before["clicks"] * 0.5:
        return ("VISIBILITY COLLAPSE", [
            "Impressions %s and clicks %s together." % (fmt_pct(d_impr), fmt_pct(d_clicks)),
            "Pages stopped being shown at all, which points at indexation rather than ranking: "
            "noindex, a robots.txt disallow, a server or DNS outage, a hosting or domain change, "
            "a WAF blocking Googlebot, a hack, or a manual action.",
            "Check Search Console Manual Actions and the Pages report before anything else.",
        ])

    if d_impr is not None and d_impr >= -FLAT and abs(d_pos) < POSITION_MATERIAL:
        return ("CLICK-THROUGH RATE LOSS", [
            "Impressions held (%s) and position held (%+.1f places), but clicks fell %s."
            % (fmt_pct(d_impr), d_pos, fmt_pct(d_clicks)),
            "The site still ranks and is still shown. Something on the result page takes the "
            "click: an AI Overview, a new SERP feature, a competitor's snippet, or a title and "
            "description Google rewrote or that stopped matching intent.",
            "This is the shape that AI Overviews produce, and it does not respond to more content.",
        ])

    if d_pos >= POSITION_MATERIAL:
        return ("RANKING LOSS", [
            "Average position worsened by %.1f places and clicks fell %s." % (d_pos, fmt_pct(d_clicks)),
            "The site is being outranked rather than hidden. Candidates: a core or ranking system "
            "update, a content or template regression, lost links, cannibalization from a page "
            "published recently, or a competitor that improved.",
            "Date the drop first (timeline mode). A cliff is a site event, a slope is an update or competition.",
        ])

    if d_ctr is not None and d_ctr <= -0.15:
        return ("MIXED: VISIBILITY AND CLICK-THROUGH", [
            "Impressions %s, position %+.1f places, click-through %s."
            % (fmt_pct(d_impr), d_pos, fmt_pct(d_ctr)),
            "More than one thing moved. Split the analysis by section and by device before "
            "settling on a cause, and treat the concentration table below as the deciding evidence.",
        ])

    return ("DEMAND OR COVERAGE LOSS", [
        "Clicks fell %s with position roughly stable (%+.1f places)." % (fmt_pct(d_clicks), d_pos),
        "Rankings held, so fewer people searched or fewer queries matched. Check seasonality "
        "against the same period last year and verify the trend in Google Trends before "
        "diagnosing anything on the site.",
    ])


def diff_rows(before, after, min_clicks):
    joined = []
    for key in set(before) | set(after):
        b = before.get(key, {"clicks": 0.0, "impressions": 0.0, "position": 0.0})
        a = after.get(key, {"clicks": 0.0, "impressions": 0.0, "position": 0.0})
        if b["clicks"] < min_clicks and a["clicks"] < min_clicks:
            continue
        joined.append({
            "key": key,
            "clicks_before": b["clicks"],
            "clicks_after": a["clicks"],
            "clicks_delta": a["clicks"] - b["clicks"],
            "impressions_before": b["impressions"],
            "impressions_after": a["impressions"],
            "impressions_delta": a["impressions"] - b["impressions"],
            "position_before": b.get("position", 0.0),
            "position_after": a.get("position", 0.0),
            "gone": key in before and key not in after,
            "new": key not in before and key in after,
        })
    return joined


def row_mechanism(row):
    """Per-row reason, using the same logic as the totals."""
    if row["gone"]:
        return "disappeared from the export entirely"
    d_impr = pct_change(row["impressions_before"], row["impressions_after"])
    d_pos = (row["position_after"] - row["position_before"]
             if row["position_before"] and row["position_after"] else 0.0)
    if d_impr is not None and d_impr <= -0.50:
        return "impressions collapsed (%s)" % fmt_pct(d_impr)
    if d_pos >= POSITION_MATERIAL:
        return "position lost %.1f places" % d_pos
    if d_impr is not None and d_impr >= -FLAT:
        return "shown as often, clicked less (click-through loss)"
    return "impressions down %s" % fmt_pct(d_impr)


def concentration(losers, total_loss):
    """How many rows carry CONCENTRATION_SHARE of the loss, and what that means."""
    if not losers or total_loss >= 0:
        return None
    running, count = 0.0, 0
    for row in losers:
        running += -row["clicks_delta"]
        count += 1
        if running >= abs(total_loss) * CONCENTRATION_SHARE:
            break
    share_of_rows = count / len(losers) if losers else 0
    if count <= 10 or share_of_rows <= 0.05:
        verdict = ("CONCENTRATED", "a small set of URLs or queries carries the loss, so look for "
                                   "a page-level or template-level cause, not a sitewide one")
    elif share_of_rows >= 0.30:
        verdict = ("DIFFUSE", "many rows lost at once. That fits an update, a sitewide technical "
                              "regression, or a demand change, but rerun with --sections first: "
                              "a loss confined to one large template also looks diffuse here")
    else:
        verdict = ("SECTIONAL", "the loss sits in part of the site, so group by section and find "
                                "the template or directory that moved")
    return {"rows_carrying_loss": count, "rows_total": len(losers),
            "verdict": verdict[0], "reading": verdict[1]}


def group_by_section(rows, depth):
    groups = {}
    for row in rows:
        key = row["key"]
        match = re.match(r"^https?://[^/]+(/.*)?$", key)
        path = (match.group(1) or "/") if match else key
        segments = [s for s in path.split("/") if s][:depth]
        label = "/" + "/".join(segments) if segments else "/ (root)"
        group = groups.setdefault(label, {"key": label, "clicks_delta": 0.0,
                                          "clicks_before": 0.0, "urls": 0})
        group["clicks_delta"] += row["clicks_delta"]
        group["clicks_before"] += row["clicks_before"]
        group["urls"] += 1
    return sorted(groups.values(), key=lambda g: g["clicks_delta"])


def print_totals(label, before, after):
    print("\n%s" % ("=" * 78))
    print("TOTALS (%s)" % label)
    print("=" * 78)
    print("  %-14s %14s %14s %12s" % ("", "before", "after", "change"))
    for metric, fmt in (("clicks", "%.0f"), ("impressions", "%.0f")):
        print("  %-14s %14s %14s %12s" % (
            metric, fmt % before[metric], fmt % after[metric],
            fmt_pct(pct_change(before[metric], after[metric]))))
    print("  %-14s %13.2f%% %13.2f%% %12s" % (
        "ctr", before["ctr"] * 100, after["ctr"] * 100,
        fmt_pct(pct_change(before["ctr"], after["ctr"]))))
    print("  %-14s %14.1f %14.1f %+12.1f" % (
        "position", before["position"], after["position"],
        after["position"] - before["position"]))
    print("  %-14s %14d %14d %12d" % (
        "rows", before["rows"], after["rows"], after["rows"] - before["rows"]))


def print_table(title, rows, top, note=None):
    print("\n%s" % ("-" * 78))
    print(title)
    if note:
        print(note)
    print("-" * 78)
    if not rows:
        print("  none")
        return
    for row in rows[:top]:
        key = row["key"]
        if len(key) > 52:
            key = key[:49] + "..."
        print("  %-52s %+8.0f clicks" % (key, row["clicks_delta"]))
        if "urls" in row:
            print("      %d URLs, %.0f clicks before" % (row["urls"], row["clicks_before"]))
        else:
            print("      %.0f to %.0f clicks, %s" % (
                row["clicks_before"], row["clicks_after"], row_mechanism(row)))


def timeline(path, top):
    """Date the drop from a Dates.csv export."""
    rows = read_rows(path)
    headers = [normalize(h) for h in rows[0]]
    date_col = match_column(headers, DATE_WORDS)
    click_col = match_column(headers, CLICK_WORDS)
    impr_col = match_column(headers, IMPRESSION_WORDS)
    if date_col is None or click_col is None:
        sys.stderr.write("%s does not look like a Dates export (need a date and a clicks column)\n" % path)
        raise SystemExit(2)

    series = []
    for row in rows[1:]:
        if len(row) <= max(date_col, click_col):
            continue
        series.append({
            "date": row[date_col].strip(),
            "clicks": parse_number(row[click_col]),
            "impressions": parse_number(row[impr_col]) if impr_col is not None else 0.0,
        })
    series.sort(key=lambda p: p["date"])
    if len(series) < 14:
        sys.stderr.write("Need at least 14 days of data to date a drop, got %d\n" % len(series))
        raise SystemExit(2)

    # Compare each day against the trailing 7 days, so weekday seasonality cancels out.
    steps = []
    for i in range(7, len(series)):
        window = series[i - 7:i]
        baseline = sum(p["clicks"] for p in window) / 7
        if baseline < 1:
            continue
        forward = series[i:i + 7]
        forward_mean = sum(p["clicks"] for p in forward) / len(forward)
        steps.append({
            "date": series[i]["date"],
            "baseline": baseline,
            "after": forward_mean,
            "change": (forward_mean - baseline) / baseline,
        })
    if not steps:
        sys.stderr.write("Not enough traffic in this export to date a drop\n")
        raise SystemExit(2)

    worst = min(steps, key=lambda s: s["change"])
    first_half = sum(p["clicks"] for p in series[:len(series) // 2])
    second_half = sum(p["clicks"] for p in series[len(series) // 2:])
    overall = pct_change(first_half, second_half)

    print("\n%s" % ("=" * 78))
    print("TIMELINE: %d days, %s to %s" % (len(series), series[0]["date"], series[-1]["date"]))
    print("=" * 78)
    print("  First half %.0f clicks, second half %.0f clicks (%s)"
          % (first_half, second_half, fmt_pct(overall)))
    print("  Steepest 7-day step: %s, %.0f to %.0f clicks per day (%s)"
          % (worst["date"], worst["baseline"], worst["after"], fmt_pct(worst["change"])))

    # Cliff or slope: ask how much of the whole decline the single steepest step explains.
    # A one-day fall accounts for nearly all of it; a rollout spreads the loss over many
    # steps and no single one comes close. Counting days over a threshold does not work,
    # because a 7-day window reports a step for a week either side of a single-day fall.
    daily_before = first_half / max(len(series) // 2, 1)
    daily_after = second_half / max(len(series) - len(series) // 2, 1)
    total_fall = daily_before - daily_after
    step_fall = worst["baseline"] - worst["after"]
    single_step_share = step_fall / total_fall if total_fall > 0 else 0.0

    if worst["change"] <= -0.30 and single_step_share >= 0.70:
        onset = worst["date"]
        shape = ("CLIFF", "the loss lands on %s and stays down. Look for something that happened "
                          "on that date: a deploy, a migration, a robots or noindex change, a DNS "
                          "or certificate expiry, a manual action, a CDN or WAF rule. Ask for the "
                          "deployment log of that day before forming any other hypothesis." % onset)
    elif overall is not None and overall <= -0.15:
        shape = ("SLOPE", "no single day carries the loss (the steepest step explains only %d "
                          "percent of it), so this is a rollout, decay, or a competitor gaining "
                          "ground. Compare the decline window against the confirmed update dates "
                          "on the Google Search Status Dashboard."
                          % int(single_step_share * 100))
    else:
        shape = ("NO CLEAR DROP", "day-level data does not show a material decline. Confirm the "
                                  "period and the property, and check whether the complaint is "
                                  "about sessions rather than clicks.")
    print("\n  Shape: %s" % shape[0])
    print("  Reading: %s" % shape[1])

    print("\n%s" % ("-" * 78))
    print("Steepest steps (each compares the next 7 days against the previous 7)")
    print("-" * 78)
    for step in sorted(steps, key=lambda s: s["change"])[:top]:
        print("  %-12s %8.0f to %8.0f clicks/day   %s"
              % (step["date"], step["baseline"], step["after"], fmt_pct(step["change"])))
    return {"shape": shape[0], "date": worst["date"], "overall_change": overall}


def main():
    parser = argparse.ArgumentParser(
        description="Locate a traffic drop inside Search Console exports.")
    parser.add_argument("before", nargs="?", help="export from the healthy period")
    parser.add_argument("after", nargs="?", help="export from the damaged period")
    parser.add_argument("--dates", help="timeline mode: a single Dates.csv export")
    parser.add_argument("--top", type=int, default=15)
    parser.add_argument("--min-clicks", type=float, default=0.0)
    parser.add_argument("--sections", type=int, default=0,
                        help="group URL rows by the first N path segments")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    if args.dates:
        result = timeline(args.dates, args.top)
        if args.as_json:
            print(json.dumps(result, indent=2))
        return 0

    if not args.before or not args.after:
        parser.error("give two exports to compare, or --dates for timeline mode")
    for path in (args.before, args.after):
        if not Path(path).is_file():
            sys.stderr.write("No such file: %s\n" % path)
            return 2

    label_before, table_before = load_table(args.before)
    label_after, table_after = load_table(args.after)
    before, after = totals(table_before), totals(table_after)
    shape, reading = classify_shape(before, after)

    rows = diff_rows(table_before, table_after, args.min_clicks)
    losers = sorted([r for r in rows if r["clicks_delta"] < 0], key=lambda r: r["clicks_delta"])
    gainers = sorted([r for r in rows if r["clicks_delta"] > 0],
                     key=lambda r: r["clicks_delta"], reverse=True)
    gone = [r for r in losers if r["gone"]]
    total_delta = after["clicks"] - before["clicks"]
    conc = concentration(losers, total_delta)

    if args.as_json:
        print(json.dumps({
            "dimension": label_before,
            "totals": {"before": before, "after": after},
            "shape": shape,
            "reading": reading,
            "concentration": conc,
            "losers": losers[:args.top],
            "gainers": gainers[:args.top],
            "disappeared": [r["key"] for r in gone[:args.top]],
        }, indent=2))
        return 1 if pct_change(before["clicks"], after["clicks"]) <= -MATERIAL_DROP else 0

    print_totals(label_before, before, after)
    print("\n%s" % ("=" * 78))
    print("SHAPE: %s" % shape)
    print("=" * 78)
    for line in reading:
        print("  %s" % line)

    if conc:
        print("\n  Concentration: %s" % conc["verdict"])
        print("  %d of %d losing rows carry %d%% of the loss. %s"
              % (conc["rows_carrying_loss"], conc["rows_total"],
                 int(CONCENTRATION_SHARE * 100), conc["reading"]))

    print_table("BIGGEST LOSSES (%s)" % label_before, losers, args.top)
    if gone:
        print_table(
            "DISAPPEARED ENTIRELY (%d rows)" % len(gone), gone, args.top,
            note="Present in the healthy period, absent afterwards. On a Pages export this is "
                 "an indexation question; on a Queries export it can also be a filter or a "
                 "threshold effect.")
    print_table(
        "GAINERS", gainers, args.top,
        note="Read these against the losses. A page that gained while a similar one fell is the "
             "signature of cannibalization or an internal redistribution, not an external cause.")

    if args.sections:
        sections = group_by_section(rows, args.sections)
        print_table("BY SECTION (first %d path segments)" % args.sections, sections, args.top,
                    note="A single section carrying the loss means a template or a directory "
                         "changed, which is a much cheaper investigation than a sitewide one.")

    print("\n%s" % ("-" * 78))
    print("Next: confirm the hypothesis before acting. A shape is a lead, not a cause.")
    return 1 if pct_change(before["clicks"], after["clicks"]) <= -MATERIAL_DROP else 0


if __name__ == "__main__":
    sys.exit(main())
