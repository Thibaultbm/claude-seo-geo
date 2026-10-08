#!/usr/bin/env python3
"""Benchmark one page against the competitor pages that rank for the same query.

Phase 3 of every page skill (spec, audit, benchmark, build). Runs the two
bundled collectors on the client page and on each competitor page:

  - seo_audit.py      (this folder): scores, findings, bold, keywords,
                      readability, schema, template blocks, social profiles
  - section_audit.py  (seo-page-sections/scripts): which page blocks exist

and prints one comparison table, the blocks most competitors have and the
client does not, and the metrics where the client sits below the competitor
median. The verdict (which gaps matter for this query) stays with the model.

Zero external dependencies (standard library only, Python 3.9+), read only.

Usage:
    python3 page_benchmark.py --type service https://client.com/page https://rival1.com/page https://rival2.com/page
    python3 page_benchmark.py --type homepage https://client.com/ https://rival.com/ --json
"""

import argparse
import json
import os
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
SEO_AUDIT = os.path.join(HERE, "seo_audit.py")
SECTION_AUDIT = os.path.normpath(os.path.join(HERE, "..", "..", "seo-page-sections",
                                              "scripts", "section_audit.py"))
TYPES = ["product", "service", "collection", "location", "comparison", "audience", "blog",
         "homepage", "pricing", "about", "contact"]


def run(cmd, timeout=240):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout
    except Exception as e:  # timeout, missing interpreter
        return "ERROR {}".format(e)


def collect(url, page_type):
    """Return a flat dict of comparable metrics for one URL."""
    row = {"url": url, "site": urlparse(url).netloc.replace("www.", "")}
    out = run([sys.executable, SEO_AUDIT, url, "--no-images"])
    marker = "JSON (machine summary):"
    if marker in out:
        try:
            data = json.loads(out.split(marker, 1)[1].strip().splitlines()[0])
            pg = data["pages"][0]
            if pg.get("error"):
                row["error"] = pg["error"]
            else:
                f = pg["formatting"]
                row.update({
                    "words": pg["word_count"],
                    "seo_score": pg["score"]["seo"],
                    "geo_score": pg["score"]["geo"],
                    "bold": f["bold_count"],
                    "h2": sum(1 for h in pg["headings"]["sequence"] if h == "H2"),
                    "question_h": pg["citability"]["question_headings"],
                    "tables": f["tables"],
                    "lists": f["lists"],
                    "statistics": pg["citability"]["statistics"],
                    "placement": pg["keywords"]["placement_coverage"],
                    "readability": pg["readability"].get("score"),
                    "schema": sorted(set(pg["schema_jsonld"])),
                    "toc": pg["template"]["toc_detected"],
                    "author": bool(pg["template"]["author_block_markup"] or pg["template"]["author_in_jsonld"]),
                    "dates": bool(pg["template"]["dates"]["time_tags"] or pg["template"]["dates"]["jsonld_datePublished"]),
                    "money_links": len(pg["template"]["money_page_links"]),
                    "social": len(pg["social_links"]["networks"]),
                    "social_placeholders": len(pg["social_links"]["placeholders"]),
                    "videos": len(pg["template"]["video_embeds"]),
                    "findings": [r["code"] for r in pg["recommendations"]],
                    "high_findings": [r["message"] for r in pg["recommendations"]
                                      if r["severity"] in ("critical", "high")],
                })
        except Exception as e:
            row["error"] = "seo_audit parse: {}".format(e)
    else:
        row["error"] = "seo_audit: no output"

    cmd = [sys.executable, SECTION_AUDIT, "--json-only", url]
    if page_type:
        cmd[2:2] = ["--type", page_type]
    out = run(cmd)
    try:
        sec = json.loads(out[out.index("["):])[0]
        row["blocks"] = {k: bool(v.get("found")) for k, v in sec.get("checks", {}).items()}
    except Exception:
        row["blocks"] = {}
    return row


def fmt_cell(v):
    if isinstance(v, bool):
        return "x" if v else "."
    if isinstance(v, list):
        return ", ".join(v) if v else "-"
    return "-" if v is None else str(v)


def main():
    ap = argparse.ArgumentParser(description="Benchmark a page against competitor pages")
    ap.add_argument("client", help="the client page URL")
    ap.add_argument("competitors", nargs="+", help="competitor page URLs (3-5 recommended)")
    ap.add_argument("--type", choices=TYPES, help="page type for the block detector")
    ap.add_argument("--json", action="store_true", help="print the JSON only")
    args = ap.parse_args()

    urls = [args.client] + args.competitors
    with ThreadPoolExecutor(max_workers=4) as ex:
        rows = list(ex.map(lambda u: collect(u, args.type), urls))
    client, rivals = rows[0], [r for r in rows[1:] if not r.get("error")]

    # Blocks: share of competitors that have each block
    block_names = sorted({b for r in rows for b in r.get("blocks", {})})
    gaps, majority = [], []
    for b in block_names:
        n = sum(1 for r in rivals if r.get("blocks", {}).get(b))
        if rivals and n / len(rivals) >= 0.5:
            majority.append(b)
            if not client.get("blocks", {}).get(b):
                gaps.append((b, n))
    # Schema types competitors use and the client does not
    schema_gaps = {}
    for r in rivals:
        for t in r.get("schema", []):
            if t not in client.get("schema", []):
                schema_gaps[t] = schema_gaps.get(t, 0) + 1
    # Numeric metrics below the competitor median
    below = []
    for k in ("words", "bold", "h2", "question_h", "tables", "lists", "statistics", "placement",
              "money_links", "social", "videos", "seo_score", "geo_score"):
        vals = [r[k] for r in rivals if isinstance(r.get(k), (int, float))]
        if vals and isinstance(client.get(k), (int, float)):
            med = statistics.median(vals)
            if client[k] < med:
                below.append({"metric": k, "client": client[k], "median": med, "max": max(vals)})

    report = {"type": args.type, "rows": rows, "block_gaps": [{"block": b, "competitors": n} for b, n in gaps],
              "schema_gaps": schema_gaps, "below_median": below}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return 0

    L = []
    L.append("=" * 78)
    L.append("PAGE BENCHMARK ({} page) client: {}".format(args.type or "auto", args.client))
    L.append("=" * 78)
    cols = ["words", "seo_score", "geo_score", "bold", "h2", "question_h", "tables", "lists",
            "statistics", "placement", "readability", "toc", "author", "dates", "money_links",
            "social", "social_placeholders", "videos"]
    head = ["metric"] + [r["site"][:22] for r in rows]
    L.append("| " + " | ".join(head) + " |")
    L.append("|" + "---|" * len(head))
    for c in cols:
        L.append("| {} | {} |".format(c, " | ".join(fmt_cell(r.get(c)) for r in rows)))
    L.append("| schema | {} |".format(" | ".join(fmt_cell(r.get("schema")) for r in rows)))
    for b in block_names:
        L.append("| block: {} | {} |".format(b, " | ".join(fmt_cell(r.get("blocks", {}).get(b, False)) for r in rows)))
    for r in rows:
        if r.get("error"):
            L.append("ERROR {}: {}".format(r["url"], r["error"]))
    L.append("")
    L.append("BLOCKS half or more of the competitors have and the client does not:")
    for b, n in gaps or []:
        L.append("  - {} ({}/{})".format(b, n, len(rivals)))
    if not gaps:
        L.append("  none")
    L.append("SCHEMA TYPES competitors use and the client does not:")
    for t, n in sorted(schema_gaps.items(), key=lambda kv: -kv[1]):
        L.append("  - {} ({}/{})".format(t, n, len(rivals)))
    if not schema_gaps:
        L.append("  none")
    L.append("CLIENT BELOW THE COMPETITOR MEDIAN:")
    for x in below:
        L.append("  - {}: client {} vs median {} (best {})".format(x["metric"], x["client"], x["median"], x["max"]))
    if not below:
        L.append("  none")
    L.append("CLIENT HIGH-SEVERITY FINDINGS:")
    for m in client.get("high_findings", []) or ["none"]:
        L.append("  - {}".format(m))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
