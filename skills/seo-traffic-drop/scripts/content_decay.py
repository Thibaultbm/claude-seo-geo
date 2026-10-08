#!/usr/bin/env python3
"""content_decay.py: find the pages that are slowly losing traffic and say
what kind of loss it is, so the refresh queue starts with the right pages.

A traffic drop is one event on a date (gsc_diff.py dates it). Content decay is
the slow erosion of individual pages: a competitor publishes a fresher page,
the answer moves into an AI Overview, the topic loses demand. It rarely shows
in the site total until many pages have decayed at once.

Inputs are Search Console Pages.csv exports of equal length:

  --current    the last period (for example the last 3 months)
  --previous   the period just before it (the previous 3 months)
  --last-year  optional, the same months one year earlier: separates real
               decay from seasonality
  --crawl      optional, the JSON written by site_crawl.py --out: adds the
               modification date and past years in the title, so a decaying
               page that is also stale goes to the top of the queue

Each page losing clicks is classified by its mechanism:

  ranking loss   position worse by 1+ place     refresh the content, benchmark the pages that passed it
  CTR loss       position and impressions flat,  rewrite title and meta, add an answer-first block,
                 CTR down                         check for an AI Overview or a new SERP feature
  demand loss    impressions down, position flat the topic is shrinking: merge, widen, or accept
  seasonal       down vs previous period, flat   no action, re-check next season
                 vs last year

Zero dependencies, Python 3.9+, read only. Reuses the CSV reader of gsc_diff.py.

Usage:
    python3 content_decay.py --current last3m/Pages.csv --previous prev3m/Pages.csv
    python3 content_decay.py --current a.csv --previous b.csv --last-year c.csv --crawl crawl.json
    python3 content_decay.py --current a.csv --previous b.csv --json
"""

import argparse
import datetime
import importlib.util
import json
import os
import sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("gsc_diff", os.path.join(HERE, "gsc_diff.py"))
GD = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(GD)

DECAY = 0.20          # clicks lost vs the previous period before a page counts as decaying
SEASONAL_FLAT = 0.10  # year-over-year change below this means the dip is seasonal
POSITION_LOSS = 1.0   # places lost before the loss is a ranking loss
CTR_LOSS = 0.20       # relative CTR fall that makes it a CTR loss
DEMAND_LOSS = 0.20    # relative impression fall that makes it a demand loss


def key(url):
    p = urlparse(url.strip())
    return (p.netloc.replace("www.", "") + p.path).rstrip("/").lower() or url


def index(table):
    return {key(k): (k, v) for k, v in table.items()}


def ctr(r):
    return r["clicks"] / r["impressions"] if r["impressions"] else 0.0


def change(before, after):
    return (after - before) / before if before else None


def load_crawl(path):
    if not path:
        return {}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    out = {}
    year = datetime.date.today().year
    for pg in data.get("pages", []):
        rec = {"date_modified": pg.get("date_modified"), "words": pg.get("words"),
               "inbound": pg.get("inbound"), "depth": pg.get("depth"),
               "title_past_years": [y for y in GD_years(pg.get("title") or "") if y < year]}
        if rec["date_modified"]:
            try:
                rec["days_since_update"] = (datetime.date.today() -
                                            datetime.date.fromisoformat(rec["date_modified"][:10])).days
            except ValueError:
                pass
        out[key(pg.get("final") or pg.get("url") or "")] = rec
    return out


def GD_years(text):
    import re
    return [int(y) for y in re.findall(r"\b(20[0-3]\d)\b", text)]


def classify(cur, prev, ly):
    """Return (label, action) for a page that lost clicks vs the previous period."""
    if ly is not None:
        yoy = change(ly["clicks"], cur["clicks"])
        if yoy is not None and yoy > -SEASONAL_FLAT:
            return "seasonal", "no action; compare again at the same season"
    pos_delta = (cur["position"] - prev["position"]) if cur["position"] and prev["position"] else 0.0
    imp = change(prev["impressions"], cur["impressions"]) or 0.0
    ctr_ch = change(ctr(prev), ctr(cur)) or 0.0
    if pos_delta >= POSITION_LOSS:
        return "ranking loss", "refresh the content (new facts, sections, date), then page_benchmark.py against the pages that passed it"
    if imp <= -DEMAND_LOSS:
        return "demand loss", "check the query trend; widen the angle, merge into a stronger page, or accept the smaller demand"
    if ctr_ch <= -CTR_LOSS:
        return "CTR loss", "rewrite title and meta description, add or sharpen the answer-first block; check for an AI Overview or new SERP feature"
    return "mixed", "inspect the page's queries in Search Console before acting"


def main():
    ap = argparse.ArgumentParser(description="Find decaying pages in Search Console exports")
    ap.add_argument("--current", required=True, help="Pages.csv for the last period")
    ap.add_argument("--previous", required=True, help="Pages.csv for the period before")
    ap.add_argument("--last-year", help="Pages.csv for the same period one year earlier")
    ap.add_argument("--crawl", help="JSON from site_crawl.py --out")
    ap.add_argument("--min-clicks", type=float, default=10.0, help="ignore pages under this many clicks in the previous period")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    _, cur_t = GD.load_table(args.current)
    _, prev_t = GD.load_table(args.previous)
    ly_t = GD.load_table(args.last_year)[1] if args.last_year else None
    cur, prev = index(cur_t), index(prev_t)
    ly = index(ly_t) if ly_t else {}
    crawl = load_crawl(args.crawl)

    rows, gone = [], []
    for k, (label, p) in prev.items():
        if p["clicks"] < args.min_clicks:
            continue
        c = cur.get(k, (label, {"clicks": 0.0, "impressions": 0.0, "position": 0.0}))[1]
        ch = change(p["clicks"], c["clicks"])
        if ch is None or ch > -DECAY:
            continue
        lyr = ly.get(k, (None, None))[1] if ly else None
        kind, action = classify(c, p, lyr)
        fresh = crawl.get(k, {})
        stale = bool(fresh.get("title_past_years") or (fresh.get("days_since_update") or 0) > 365)
        row = {
            "page": label, "clicks_before": round(p["clicks"]), "clicks_now": round(c["clicks"]),
            "clicks_lost": round(p["clicks"] - c["clicks"]), "change_pct": round(100 * ch),
            "impressions_change_pct": round(100 * (change(p["impressions"], c["impressions"]) or 0)),
            "position_before": round(p["position"], 1), "position_now": round(c["position"], 1),
            "ctr_before": round(100 * ctr(p), 2), "ctr_now": round(100 * ctr(c), 2),
            "yoy_change_pct": (round(100 * change(lyr["clicks"], c["clicks"]))
                               if lyr and change(lyr["clicks"], c["clicks"]) is not None else None),
            "kind": kind, "action": action, "stale": stale,
            "date_modified": fresh.get("date_modified"), "title_past_years": fresh.get("title_past_years"),
            "inbound_links": fresh.get("inbound"),
        }
        if c["clicks"] == 0 and c["impressions"] == 0:
            gone.append(row)
        else:
            rows.append(row)

    # Priority: real decay before seasonal, stale pages first, then the clicks at stake.
    order = {"ranking loss": 0, "CTR loss": 1, "mixed": 2, "demand loss": 3, "seasonal": 4}
    rows.sort(key=lambda r: (order[r["kind"]], not r["stale"], -r["clicks_lost"]))
    lost_total = sum(r["clicks_lost"] for r in rows if r["kind"] != "seasonal")
    summary = {"decaying_pages": len([r for r in rows if r["kind"] != "seasonal"]),
               "seasonal_pages": len([r for r in rows if r["kind"] == "seasonal"]),
               "vanished_pages": len(gone), "clicks_lost_to_decay": lost_total,
               "by_kind": {k: len([r for r in rows if r["kind"] == k]) for k in order},
               "pages": rows, "vanished": gone}
    if args.as_json:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
        return 0

    L = ["=" * 78, "CONTENT DECAY", "=" * 78]
    L.append("decaying pages {} | clicks lost {} | seasonal {} | vanished from the export {}".format(
        summary["decaying_pages"], lost_total, summary["seasonal_pages"], len(gone)))
    L.append("by mechanism: " + ", ".join("{} {}".format(k, v) for k, v in summary["by_kind"].items() if v))
    if not args.last_year:
        L.append("(no --last-year export: seasonal dips cannot be separated from decay)")
    if not args.crawl:
        L.append("(no --crawl JSON: stale dates not checked; run site_crawl.py --out crawl.json)")
    L.append("")
    L.append("REFRESH QUEUE (real decay first, stale pages first, then clicks at stake):")
    for r in [x for x in rows if x["kind"] != "seasonal"][:args.top]:
        L.append("- {}{}".format(r["page"], "  [STALE]" if r["stale"] else ""))
        L.append("    {} | clicks {} -> {} ({}%) | pos {} -> {} | CTR {}% -> {}% | impr {}%{}".format(
            r["kind"], r["clicks_before"], r["clicks_now"], r["change_pct"], r["position_before"],
            r["position_now"], r["ctr_before"], r["ctr_now"], r["impressions_change_pct"],
            " | YoY {}%".format(r["yoy_change_pct"]) if r["yoy_change_pct"] is not None else ""))
        L.append("    action: " + r["action"])
    seas = [x for x in rows if x["kind"] == "seasonal"]
    if seas:
        L.append("\nSEASONAL (down vs previous period, flat vs last year): " +
                 ", ".join(x["page"] for x in seas[:10]))
    if gone:
        L.append("\nVANISHED (clicks before, absent now: check status code, noindex, redirect, URL change):")
        for r in gone[:args.top]:
            L.append("- {} ({} clicks before)".format(r["page"], r["clicks_before"]))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
