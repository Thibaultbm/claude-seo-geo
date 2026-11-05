#!/usr/bin/env python3
"""Turn a raw export of proprietary data into publishable, anonymized aggregates and charts.

Input: a CSV with one row per entity (a client, a store, a site, a project) or per event.
Output: aggregates per category (count, median, quartiles, mean, share), with every
identifying column dropped and every group smaller than --min-group suppressed, plus
one accessible SVG bar chart per metric (text in the SVG, a title, a description and a
source line, light and dark), and a data table ready to paste under each chart.

Pure standard library, Python 3.9+, works offline. Never sends the data anywhere.

Usage:
  python3 data_study.py export.csv --category industry --metrics growth_pct,clicks \\
      --entity client_id --min-group 5 --out study/
  python3 data_study.py export.csv --category industry --metrics growth_pct \\
      --entity client_id --drop email,name,domain --round 1 --source "Acme data, 412 stores, Jan to Sep 2026"

  --category   column that becomes the published label (e.g. industry: "E-commerce store")
  --entity     column that identifies one entity; counted distinct, never published
  --min-group  smallest number of distinct entities a published group may hold (default 5)
  --drop       extra columns to remove; columns whose name looks identifying
               (email, name, domain, url, phone, address, siret, vat, ip, id) are dropped anyway

Files written in --out: aggregates.csv, aggregates.json, suppressed.txt,
chart-<metric>.svg, table-<metric>.html, and anonymization-report.txt.
"""

import argparse
import csv
import html
import json
import os
import re
import statistics
import sys

IDENTIFYING = re.compile(r"(^|_)(e?mail|name|nom|first|last|prenom|domain|domaine|url|site|website|phone|tel|"
                         r"address|adresse|street|zip|postcode|siret|siren|vat|tva|ip|user|customer|client|"
                         r"company|societe|account|iban|id|uuid)(_|$)", re.I)


def number(v):
    v = (v or "").strip().replace(" ", "").replace(" ", "").replace("%", "")
    if not v:
        return None
    if v.count(",") == 1 and "." not in v:
        v = v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return None


def quartiles(vals):
    if len(vals) < 2:
        return vals[0], vals[0]
    q = statistics.quantiles(vals, n=4, method="inclusive")
    return q[0], q[2]


def fmt(x, nd):
    if x is None:
        return ""
    r = round(x, nd)
    return str(int(r)) if nd == 0 or r == int(r) else str(r)


def svg_bar_chart(metric, rows, source, unit, nd):
    """Horizontal bars, median per category, labels as real text. Width 720, height grows."""
    bar_h, gap, left, right, top = 26, 12, 230, 90, 70
    width = 720
    height = top + len(rows) * (bar_h + gap) + 50
    vmax = max((r["median"] for r in rows), default=0) or 1
    vmin = min((r["median"] for r in rows), default=0)
    zero = 0 if vmin >= 0 else vmin
    span = (vmax - zero) or 1
    title = "Median {} by category".format(metric.replace("_", " "))
    desc = "; ".join("{}: {}{} (n={})".format(r["category"], fmt(r["median"], nd), unit, r["entities"]) for r in rows)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" '
           'aria-labelledby="t d" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">'.format(w=width, h=height),
           '<title id="t">{}</title><desc id="d">{}</desc>'.format(html.escape(title), html.escape(desc)),
           '<style>.bg{fill:#fff}.lab{fill:#1f2937;font-size:14px}.val{fill:#111827;font-size:14px;font-weight:600}'
           '.bar{fill:#2563eb}.ttl{fill:#111827;font-size:18px;font-weight:700}.src{fill:#6b7280;font-size:12px}'
           '.axis{stroke:#d1d5db}'
           '@media (prefers-color-scheme: dark){.bg{fill:#111827}.lab{fill:#e5e7eb}.val{fill:#f9fafb}'
           '.bar{fill:#60a5fa}.ttl{fill:#f9fafb}.src{fill:#9ca3af}.axis{stroke:#374151}}</style>',
           '<rect class="bg" width="{}" height="{}"/>'.format(width, height),
           '<text class="ttl" x="20" y="34">{}</text>'.format(html.escape(title))]
    x0 = left + (0 - zero) / span * (width - left - right)
    out.append('<line class="axis" x1="{x:.1f}" y1="{y1}" x2="{x:.1f}" y2="{y2}"/>'.format(
        x=x0, y1=top - 8, y2=top + len(rows) * (bar_h + gap)))
    for i, r in enumerate(rows):
        y = top + i * (bar_h + gap)
        x1 = left + (r["median"] - zero) / span * (width - left - right)
        bx, bw = (x0, x1 - x0) if x1 >= x0 else (x1, x0 - x1)
        out.append('<text class="lab" x="{}" y="{}" text-anchor="end">{} (n={})</text>'.format(
            left - 10, y + bar_h * 0.7, html.escape(r["category"][:28]), r["entities"]))
        out.append('<rect class="bar" x="{:.1f}" y="{}" width="{:.1f}" height="{}" rx="3"/>'.format(bx, y, max(bw, 1), bar_h))
        out.append('<text class="val" x="{:.1f}" y="{}">{}{}</text>'.format(
            max(x1, x0) + 8, y + bar_h * 0.7, fmt(r["median"], nd), html.escape(unit)))
    out.append('<text class="src" x="20" y="{}">Source: {}</text>'.format(height - 18, html.escape(source)))
    out.append("</svg>")
    return "\n".join(out)


def html_table(metric, rows, nd, unit):
    head = ("<table>\n<caption>{} by category</caption>\n<thead><tr><th scope=\"col\">Category</th>"
            "<th scope=\"col\">Entities</th><th scope=\"col\">Median</th><th scope=\"col\">25th to 75th percentile</th>"
            "<th scope=\"col\">Mean</th></tr></thead>\n<tbody>").format(html.escape(metric.replace("_", " ").capitalize()))
    body = []
    for r in rows:
        body.append("<tr><th scope=\"row\">{}</th><td>{}</td><td>{}{u}</td><td>{}{u} to {}{u}</td><td>{}{u}</td></tr>".format(
            html.escape(r["category"]), r["entities"], fmt(r["median"], nd), fmt(r["p25"], nd), fmt(r["p75"], nd),
            fmt(r["mean"], nd), u=html.escape(unit)))
    return head + "\n" + "\n".join(body) + "\n</tbody>\n</table>\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--category", required=True)
    ap.add_argument("--metrics", required=True, help="comma-separated numeric columns")
    ap.add_argument("--entity", help="column identifying one entity (counted distinct, never published)")
    ap.add_argument("--min-group", type=int, default=5)
    ap.add_argument("--drop", default="", help="comma-separated columns to remove in addition to the automatic ones")
    ap.add_argument("--round", type=int, default=0, dest="nd", help="decimals in published numbers (default 0)")
    ap.add_argument("--unit", default="", help="unit after values: one for all (%%) or per metric (growth_pct=%%,revenue=EUR)")
    ap.add_argument("--source", default="proprietary data", help="source line printed under every chart")
    ap.add_argument("--all-label", default="All categories", help="label of the overall row")
    ap.add_argument("--out", default="data-study")
    args = ap.parse_args()

    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        rows = list(csv.DictReader(f, dialect=dialect))
    if not rows:
        print("empty file", file=sys.stderr)
        return 1
    cols = list(rows[0].keys())
    metrics = [m.strip() for m in args.metrics.split(",") if m.strip()]
    for c in [args.category] + metrics + ([args.entity] if args.entity else []):
        if c not in cols:
            print("column not found: {} (columns: {})".format(c, ", ".join(cols)), file=sys.stderr)
            return 1
    extra = {c.strip() for c in args.drop.split(",") if c.strip()}
    dropped = sorted(c for c in cols if c not in metrics and c != args.category and (c in extra or IDENTIFYING.search(c)))
    if args.entity and args.entity not in dropped:
        dropped.append(args.entity)
    kept_other = [c for c in cols if c not in dropped and c not in metrics and c != args.category]

    groups = {}
    for r in rows:
        cat = (r.get(args.category) or "").strip() or "Unclassified"
        g = groups.setdefault(cat, {"entities": set(), "rows": 0, "values": {m: [] for m in metrics}})
        g["rows"] += 1
        g["entities"].add(r[args.entity] if args.entity else id(r))
        for m in metrics:
            v = number(r.get(m))
            if v is not None:
                g["values"][m].append(v)

    total_entities = len({r[args.entity] for r in rows}) if args.entity else len(rows)
    published, suppressed = [], []
    for cat, g in sorted(groups.items()):
        (published if len(g["entities"]) >= args.min_group else suppressed).append((cat, g))
    # Suppressed groups merge into "Other" only if the merged group is itself large enough.
    other_entities = set().union(*[g["entities"] for _, g in suppressed]) if suppressed else set()
    if len(other_entities) >= args.min_group:
        merged = {"entities": other_entities, "rows": sum(g["rows"] for _, g in suppressed),
                  "values": {m: [v for _, g in suppressed for v in g["values"][m]] for m in metrics}}
        published.append(("Other categories", merged))
    allg = {"entities": set().union(*[g["entities"] for g in groups.values()]),
            "rows": len(rows), "values": {m: [v for g in groups.values() for v in g["values"][m]] for m in metrics}}

    if "=" in args.unit:
        units = dict(p.split("=", 1) for p in args.unit.split(",") if "=" in p)
    else:
        units = {m: args.unit for m in metrics}

    os.makedirs(args.out, exist_ok=True)
    result, flat = {}, []
    for m in metrics:
        unit = units.get(m, "")
        mrows = []
        for cat, g in published + [(args.all_label, allg)]:
            vals = sorted(g["values"][m])
            if len(vals) < args.min_group:
                continue
            p25, p75 = quartiles(vals)
            row = {"category": cat, "entities": len(g["entities"]), "values": len(vals),
                   "median": round(statistics.median(vals), args.nd), "p25": round(p25, args.nd),
                   "p75": round(p75, args.nd), "mean": round(statistics.fmean(vals), args.nd),
                   "share_of_entities": round(len(g["entities"]) / total_entities, 3)}
            mrows.append(row)
            flat.append(dict(metric=m, **row))
        body = [r for r in mrows if r["category"] != args.all_label]
        body.sort(key=lambda r: r["median"], reverse=True)
        overall = [r for r in mrows if r["category"] == args.all_label]
        ordered = body + overall
        result[m] = ordered
        if ordered:
            with open(os.path.join(args.out, "chart-{}.svg".format(m)), "w", encoding="utf-8") as f:
                f.write(svg_bar_chart(m, ordered, args.source, unit, args.nd))
            with open(os.path.join(args.out, "table-{}.html".format(m)), "w", encoding="utf-8") as f:
                f.write(html_table(m, ordered, args.nd, unit))

    with open(os.path.join(args.out, "aggregates.json"), "w", encoding="utf-8") as f:
        json.dump({"source": args.source, "min_group": args.min_group, "entities": total_entities,
                   "metrics": result}, f, ensure_ascii=False, indent=2)
    with open(os.path.join(args.out, "aggregates.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["metric", "category", "entities", "values", "median", "p25", "p75", "mean", "share_of_entities"])
        w.writeheader()
        w.writerows(flat)
    with open(os.path.join(args.out, "suppressed.txt"), "w", encoding="utf-8") as f:
        for cat, g in suppressed:
            f.write("{}\t{} entities (below {})\n".format(cat, len(g["entities"]), args.min_group))
    report = [
        "Anonymization report",
        "rows read: {}, distinct entities: {}".format(len(rows), total_entities),
        "columns dropped (never written): {}".format(", ".join(dropped) or "none"),
        "columns kept but not published: {}".format(", ".join(kept_other) or "none"),
        "published label: {}".format(args.category),
        "groups published: {}, suppressed (< {} entities): {}".format(len(published), args.min_group, len(suppressed)),
        "suppressed groups merged into 'Other categories': {}".format("yes" if len(other_entities) >= args.min_group else "no"),
        "check by hand: no category name that points to one known company, no extreme value that identifies an entity",
    ]
    with open(os.path.join(args.out, "anonymization-report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    print("\n".join(report))
    for m, rs in result.items():
        print("\n{}".format(m))
        for r in rs:
            print("  {:<30} n={:<5} median {:<10} p25-p75 {} to {}".format(
                r["category"][:30], r["entities"], fmt(r["median"], args.nd), fmt(r["p25"], args.nd), fmt(r["p75"], args.nd)))
    print("\nwritten to {}/".format(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
