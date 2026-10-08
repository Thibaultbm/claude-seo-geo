#!/usr/bin/env python3
"""Benchmark one page against the competitor pages that rank for the same query.

Phase 3 of every page skill (spec, audit, benchmark, build). Runs the two
bundled collectors on the client page and on each competitor page:

  - seo_audit.py      (this folder): scores, findings, bold, keywords,
                      readability, schema, template blocks, social profiles
  - section_audit.py  (seo-page-sections/scripts): which page blocks exist

and prints one comparison table, the blocks most competitors have and the
client does not, the metrics where the client sits below the competitor
median, and the vocabulary gap: the terms and two-word phrases that half or
more of the competitors use (and 2 at least) and the client page never does,
with the competitor headings that carry them. The verdict (which gaps matter
for this query) stays with the model.

Zero external dependencies (standard library only, Python 3.9+), read only.

Usage:
    python3 page_benchmark.py --type service https://client.com/page https://rival1.com/page https://rival2.com/page
    python3 page_benchmark.py --type homepage https://client.com/ https://rival.com/ --json
"""

import argparse
import importlib.util
import json
import math
import os
import re
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
SEO_AUDIT = os.path.join(HERE, "seo_audit.py")
SECTION_AUDIT = os.path.normpath(os.path.join(HERE, "..", "..", "seo-page-sections",
                                              "scripts", "section_audit.py"))

_spec = importlib.util.spec_from_file_location("seo_audit", SEO_AUDIT)
SA = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SA)

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

    row["terms"], row["bigrams"], row["subheads"] = vocabulary(url)

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


def vocabulary(url):
    """Content-term and two-word-phrase counts of the main content, plus the
    H2/H3 texts, read with the same parser as seo_audit.py."""
    try:
        final, _, headers, body = SA.fetch(url)
        m = re.search(r"charset=([\w-]+)", headers.get("Content-Type", ""), re.I)
        html = body.decode(m.group(1) if m else "utf-8", errors="replace")
        p = SA.Page()
        p.feed(html)
    except Exception:
        return {}, {}, []
    terms = SA._content_terms(p.content_text())
    uni, bi = {}, {}
    for t in terms:
        uni[t] = uni.get(t, 0) + 1
    for a, b in zip(terms, terms[1:]):
        if a != b:
            k = a + " " + b
            bi[k] = bi.get(k, 0) + 1
    heads = [t for lvl, t, _ in p.headings if lvl in (2, 3) and t]
    return uni, bi, heads


def term_gap(client, rivals, key, min_count):
    """Terms used by half the competitors or more (2 at least), absent from the client."""
    if not rivals:
        return []
    need = max(2, math.ceil(len(rivals) / 2))
    df, tot = {}, {}
    for r in rivals:
        for t, n in r.get(key, {}).items():
            if n >= min_count:
                df[t] = df.get(t, 0) + 1
                tot[t] = tot.get(t, 0) + n
    have = client.get(key, {})
    gap = [{"term": t, "competitors": d, "avg_count": round(tot[t] / d, 1)}
           for t, d in df.items() if d >= need and not have.get(t)]
    gap.sort(key=lambda x: (-x["competitors"], -x["avg_count"]))
    return gap


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

    # Vocabulary gap: unigrams used twice or more per page, bigrams once or more
    uni_gap = term_gap(client, rivals, "terms", 2)[:40]
    bi_gap = term_gap(client, rivals, "bigrams", 1)[:25]
    gap_terms = {g["term"] for g in uni_gap[:20]}
    gap_phrases = [g["term"] for g in bi_gap[:15]]
    head_gap = []
    for r in rivals:
        for h in r.get("subheads", []):
            ht = SA._content_terms(h)
            seq = " ".join(ht)
            if set(ht) & gap_terms or any(ph in seq for ph in gap_phrases):
                head_gap.append({"site": r["site"], "heading": h[:100]})
    for r in rows:  # keep the JSON readable
        r["terms_count"] = len(r.pop("terms", {}) or {})
        r.pop("bigrams", None)
        r["subheads"] = r.get("subheads", [])[:30]
    report_vocab = {"term_gap": uni_gap, "phrase_gap": bi_gap, "competitor_headings_with_gap_terms": head_gap[:30]}

    report = {"type": args.type, "rows": rows, "vocabulary": report_vocab, "block_gaps": [{"block": b, "competitors": n} for b, n in gaps],
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
    L.append("VOCABULARY GAP (terms half or more of the competitors use, never on the client page):")
    L.append("  terms  : " + (", ".join("{} ({}/{})".format(g["term"], g["competitors"], len(rivals)) for g in uni_gap[:30]) or "none"))
    L.append("  phrases: " + (", ".join("{} ({}/{})".format(g["term"], g["competitors"], len(rivals)) for g in bi_gap[:20]) or "none"))
    if head_gap:
        L.append("  competitor H2/H3 that carry those terms (candidate sections to add):")
        for h in head_gap[:15]:
            L.append("    - [{}] {}".format(h["site"], h["heading"]))
    L.append("  Read it as a coverage list, not a stuffing list: add a term only where it answers")
    L.append("  something the searcher needs, and ignore competitor brand names and boilerplate.")
    L.append("CLIENT HIGH-SEVERITY FINDINGS:")
    for m in client.get("high_findings", []) or ["none"]:
        L.append("  - {}".format(m))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
