#!/usr/bin/env python3
"""Read every sitemap of a site and its competitors, then show the gap.

For each domain: finds every sitemap (robots.txt Sitemap lines, then the usual paths),
follows sitemap indexes, reads every URL with its lastmod, sorts each URL into a page
model (blog post, comparison, alternatives, location, integration, use case, glossary,
template, free tool, case study, data study, product, category...), measures the
publishing pace, and turns slugs into topics. Then compares the competitors with the
client site: page models the client lacks, topics several competitors cover and the
client does not, and who publishes fastest.

Pure standard library, Python 3.9+, read only, no API key.

Usage:
  python3 competitor_sitemaps.py --site https://client.com \\
      --competitors https://a.com https://b.com https://c.com https://d.com https://e.com
  python3 competitor_sitemaps.py --site client.com --competitors a.com b.com \\
      --probe 40 --json market.json --csv urls.csv

  --probe N   opens up to N recent blog URLs per domain and reads the real publication
              date (article:published_time, JSON-LD datePublished). lastmod alone is an
              update date, not a publication date: the pace it gives is an upper bound.
"""

import argparse
import collections
import csv
import datetime as dt
import gzip
import json
import re
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlparse, unquote

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0 Safari/537.36 competitor-sitemaps"
FALLBACK_PATHS = ("/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml", "/wp-sitemap.xml",
                  "/sitemap/sitemap.xml", "/sitemaps/sitemap.xml")
LANGS = {"en", "fr", "de", "es", "it", "pt", "nl", "pl", "sv", "da", "no", "nb", "fi", "cs", "ro",
         "hu", "el", "tr", "ru", "uk", "ar", "he", "ko", "zh", "ja", "hi", "id", "th", "vi", "ms",
         "en-us", "en-gb", "fr-fr", "fr-ca", "fr-be", "de-de", "de-at", "de-ch", "es-es", "es-mx",
         "pt-br", "pt-pt", "zh-cn", "zh-tw", "zh-hans", "zh-hant", "it-it", "nl-nl", "ja-jp", "ko-kr"}

# Page models, first match wins. Patterns run on the lowercased path without language prefix.
MODELS = [
    ("noise", r"/(tag|tags|author|authors|auteur|page/\d+|feed|wp-content|cdn-cgi|search|login|blog-category|blog-tags?|blog/categor(y|ies)|blog/tags?|signin|signup|cart|checkout|account|panier|compte)(/|$)|\.(pdf|jpg|png|webp|xml)$"),
    ("legal", r"/(legal|privacy|terms|cookies?|mentions-legales|cgv|cgu|confidentialite|gdpr|rgpd|impressum|datenschutz|aviso-legal)(/|-|$)"),
    ("comparison", r"(^|[/-])(vs|versus|contre|compare|comparison|comparatif|comparaison|vergleich)([/-]|$)"),
    ("alternatives", r"(^|[/-])(alternatives?|alternativen?|alternativas?|alternative-to|alternative-a)([/-]|$)"),
    ("best-of list", r"(^|/)(best|top|meilleurs?|meilleures?|mejores|beste|migliori)-"),
    ("case study", r"/(case-stud(y|ies)|etudes?-de-cas|customers?|clients?|success-stor(y|ies)|temoignages?|testimonials?|references|kundenstimmen|casos-de-exito)(/|$)"),
    ("data study", r"/(research|reports?|studies|study|etudes?|statistics?|statistiques|stats|benchmarks?|data|barometre|barometer|index|state-of)(/|-|$)"),
    ("glossary", r"/(glossary|glossaire|lexique|dictionary|definitions?|wiki|what-is|qu-est-ce-que|was-ist|que-es)(/|-|$)"),
    ("template", r"/(templates?|modeles?|exemples?|examples?|vorlagen?|plantillas?|swipe-file)(/|$)"),
    ("free tool", r"/(tools?|seo-?tools|outils?|free-tools?|calculators?|calculateurs?|generators?|generateurs?|checker|simulat(or|eur)|tester|grader|werkzeuge?|herramientas?)(/|$)"),
    ("integration", r"/(integrations?|apps?|connectors?|connecteurs?|plugins?|marketplace|partners?/apps)(/|$)"),
    ("use case", r"/(use-cases?|cas-d-usage|cas-usage|solutions?|industries|industry|secteurs?|for|pour|para|fur|personas?|teams?|roles?)(/|$)|(^|/)(for|pour|para)-[a-z]"),
    ("location", r"/(locations?|villes?|city|cities|agences?|stores?|magasins?|near-me|zones?|regions?|departements?)(/|$)|/(seo|agence|agency|plombier|avocat|dentiste|[a-z]+)-(paris|lyon|marseille|toulouse|bordeaux|lille|nantes|nice|london|berlin|madrid|new-york)(/|$)"),
    ("docs and help", r"/(docs?|documentation|help|aide|support|faq|kb|knowledge-base|guides?/api|api|developers?|changelog|status)(/|$)"),
    ("course and guide", r"/(academy|academie|learn|[a-z-]*playbooks?|courses?|formations?|guides?|tutorials?|tutoriels?|ebooks?|whitepapers?|livres-blancs?|webinars?|webinaires?|podcasts?|videos?)(/|$)"),
    ("blog post", r"/(blog|news|actualites?|actus?|articles?|insights|magazine|mag|ressources|resources|posts?|journal|stories|conseils)(/|$)"),
    ("product", r"/(products?|produits?|produkt|producto|item|p)/[^/]+|/[^/]+-p-\d+|\.html$"),
    ("category", r"/(collections?|categor(y|ies)|categories|c|shop|boutique|catalog|catalogue|rayons?)(/|$)"),
    ("pricing", r"/(pricing|prix|tarifs?|plans?|preise|precios|prezzi)(/|$)"),
    ("feature", r"/(features?|fonctionnalites?|platform|plateforme|product-tour|funktionen|funcionalidades)(/|$)"),
    ("company", r"/(about|a-propos|qui-sommes-nous|team|equipe|careers?|jobs|recrutement|contact|press|presse|ueber-uns|nosotros)(/|$)"),
]
MODELS = [(name, re.compile(rx)) for name, rx in MODELS]

STOP = set("""a an and are as at be by de des du d en et for from how i in is it l la le les of on or our
the to un une vs what why with your you votre vos nos notre sur pour par avec dans qui que quoi comment
pourquoi est sont can here their much make old get use using 2023 2024 2025 2026 2027 guide complete ultimate best top new el los las y para con por
der die das und fur mit von zu wie was il lo gli di da per che com do dos da para um uma""".split())


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            if r.headers.get("Content-Encoding") == "gzip" or url.endswith(".gz") or body[:2] == b"\x1f\x8b":
                try:
                    body = gzip.decompress(body)
                except OSError:
                    pass
            return r.status, body.decode("utf-8", "replace"), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, "", url
    except Exception as e:  # network error: report it, never crash the run
        return 0, "{}: {}".format(type(e).__name__, e), url


def base_url(raw):
    raw = raw.strip()
    if "://" not in raw:
        raw = "https://" + raw
    p = urlparse(raw)
    return "{}://{}".format(p.scheme, p.netloc)


def discover(base):
    """Every sitemap the site declares, else the first usual path that answers."""
    status, text, _ = fetch(urljoin(base, "/robots.txt"))
    found = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", text) if status == 200 else []
    if found:
        return list(dict.fromkeys(found)), "robots.txt"
    for path in FALLBACK_PATHS:
        status, text, final = fetch(urljoin(base, path))
        if status == 200 and ("<urlset" in text or "<sitemapindex" in text):
            return [final], path
    return [], "none"


def read_sitemaps(roots, max_files, max_urls, pause):
    """Follow indexes breadth first. Returns ({url: lastmod}, files_read, errors)."""
    queue, seen, urls, errors = list(roots), set(), {}, []
    while queue and len(seen) < max_files and len(urls) < max_urls:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        status, text, _ = fetch(sm)
        if status != 200 or not text:
            errors.append("{} -> {}".format(sm, status or text[:80]))
            continue
        if "<sitemapindex" in text[:5000]:
            queue.extend(l.strip() for l in re.findall(r"<loc>\s*(?:<!\[CDATA\[)?\s*([^<\]]+?)\s*(?:\]\]>)?\s*</loc>", text))
        else:
            for block in re.findall(r"<url>(.*?)</url>", text, flags=re.S):
                loc = re.search(r"<loc>\s*(?:<!\[CDATA\[)?\s*([^<\]]+?)\s*(?:\]\]>)?\s*</loc>", block)
                if not loc:
                    continue
                lm = re.search(r"<lastmod>\s*([^<]+?)\s*</lastmod>", block)
                urls.setdefault(loc.group(1).replace("&amp;", "&"), lm.group(1)[:10] if lm else "")
                if len(urls) >= max_urls:
                    break
        if pause:
            time.sleep(pause)
    return urls, len(seen), errors


def split_lang(path):
    segs = [s for s in path.lower().split("/") if s]
    if segs and segs[0] in LANGS:
        return segs[0], "/" + "/".join(segs[1:])
    return "", "/" + "/".join(segs)


def classify(path):
    if path in ("", "/"):
        return "home"
    for name, rx in MODELS:
        if rx.search(path):
            return name
    depth = len([s for s in path.split("/") if s])
    return "landing page" if depth == 1 else "other"


def topic_of(path):
    """Slug of the last meaningful segment turned into a readable topic."""
    segs = [s for s in path.split("/") if s and not s.isdigit()]
    if not segs:
        return ""
    slug = unquote(segs[-1]).lower()
    slug = re.sub(r"\.(html?|php|aspx?)$", "", slug)
    slug = re.sub(r"-?\d{4,}$", "", slug)  # trailing ids
    words = [w for w in re.split(r"[-_+.\s]+", slug) if w]
    return " ".join(words)


def tokens(topic):
    return frozenset(w for w in topic.split() if w not in STOP and len(w) > 2)


def parse_day(s):
    try:
        return dt.date.fromisoformat(s[:10])
    except ValueError:
        return None


def published_date(url):
    status, html, _ = fetch(url, timeout=20)
    if status != 200:
        return None
    for rx in (r'property=["\']article:published_time["\'][^>]*content=["\']([^"\']+)',
               r'content=["\']([^"\']+)["\'][^>]*property=["\']article:published_time',
               r'"datePublished"\s*:\s*"([^"]+)"',
               r'<time[^>]*datetime=["\'](\d{4}-\d{2}-\d{2})'):
        m = re.search(rx, html)
        if m and parse_day(m.group(1)):
            return parse_day(m.group(1))
    return None


def analyse(base, args, today):
    roots, how = discover(base)
    urls, files, errors = read_sitemaps(roots, args.max_files, args.max_urls, args.pause)
    host = urlparse(base).hostname.replace("www.", "")
    rows = []
    for u, lm in urls.items():
        p = urlparse(u)
        if (p.hostname or "").replace("www.", "") != host:
            continue
        lang, path = split_lang(p.path)
        model = classify(path)
        depth = len([x for x in path.split("/") if x])
        # A section root (/blog, /tools, /glossary) is a hub, not a topic.
        topic = "" if depth == 1 and model not in ("landing page", "other") else topic_of(path)
        rows.append({"domain": host, "url": u, "lang": lang, "model": model,
                     "topic": topic, "lastmod": lm})
    models = collections.Counter(r["model"] for r in rows if r["model"] != "noise")
    langs = collections.Counter(r["lang"] or "default" for r in rows)
    dated = [parse_day(r["lastmod"]) for r in rows if r["lastmod"]]
    dated = [d for d in dated if d]
    day_counts = collections.Counter(dated)
    top_day, top_day_n = (day_counts.most_common(1)[0] if day_counts else (None, 0))
    pace = {}
    for model in ("blog post", "all"):
        sel = [parse_day(r["lastmod"]) for r in rows if r["lastmod"] and (model == "all" or r["model"] == model)]
        sel = [d for d in sel if d]
        pace[model] = {"lastmod_30d": sum(1 for d in sel if (today - d).days <= 30),
                       "lastmod_90d": sum(1 for d in sel if (today - d).days <= 90)}
    months = collections.Counter(d.strftime("%Y-%m") for d in dated if (today - d).days <= 365)
    probe = None
    if args.probe:
        blog = sorted((r for r in rows if r["model"] == "blog post"),
                      key=lambda r: r["lastmod"], reverse=True)[:args.probe]
        found = [published_date(r["url"]) for r in blog]
        found = [d for d in found if d]
        probe = {"opened": len(blog), "with_date": len(found),
                 "published_30d": sum(1 for d in found if (today - d).days <= 30),
                 "published_90d": sum(1 for d in found if (today - d).days <= 90),
                 "newest": max(found).isoformat() if found else None}
    return {"domain": host, "base": base, "sitemaps_found_via": how, "sitemap_roots": roots,
            "files_read": files, "errors": errors[:10], "urls": len(rows),
            "lastmod_coverage": round(len(dated) / len(rows), 2) if rows else 0,
            "lastmod_most_common_day": [top_day.isoformat() if top_day else None, top_day_n],
            "models": dict(models.most_common()), "languages": dict(langs.most_common()),
            "pace": pace, "lastmod_per_month": dict(sorted(months.items())), "probe": probe,
            "capped": len(urls) >= args.max_urls, "rows": rows}


def topic_gap(client, competitors, min_sites):
    """Topics covered by at least min_sites competitors and absent from the client."""
    client_sets = [tokens(r["topic"]) for r in client["rows"] if r["model"] not in ("noise", "legal")]
    client_sets = [s for s in client_sets if s]

    def covered(t):
        for s in client_sets:
            if len(t & s) / len(t | s) >= 0.6:
                return True
        return False

    groups = {}
    for comp in competitors:
        for r in comp["rows"]:
            if r["model"] in ("noise", "legal", "company", "docs and help", "home", "product", "category"):
                continue
            t = tokens(r["topic"])
            if len(t) < 1:
                continue
            key = " ".join(sorted(t))
            g = groups.setdefault(key, {"topic": r["topic"], "models": collections.Counter(), "sites": set(), "urls": []})
            g["models"][r["model"]] += 1
            g["sites"].add(comp["domain"])
            if len(g["urls"]) < 3:
                g["urls"].append(r["url"])
    out = []
    for key, g in groups.items():
        if len(g["sites"]) >= min_sites and not covered(frozenset(key.split())):
            out.append({"topic": g["topic"], "sites": sorted(g["sites"]), "model": g["models"].most_common(1)[0][0],
                        "example_urls": g["urls"]})
    out.sort(key=lambda x: (-len(x["sites"]), x["topic"]))
    return out


def single_site_topics(competitors, client, per_site):
    """Most frequent words in each competitor's slugs that the client never uses."""
    client_words = collections.Counter(w for r in client["rows"] for w in tokens(r["topic"]))
    out = {}
    for comp in competitors:
        words = collections.Counter(w for r in comp["rows"] if r["model"] not in ("noise", "legal")
                                    for w in tokens(r["topic"]))
        out[comp["domain"]] = [w for w, _ in words.most_common(200) if w not in client_words][:per_site]
    return out


def model_gap(client, competitors):
    rows = []
    names = sorted({m for c in competitors for m in c["models"]} - {"noise", "legal", "home", "other"})
    for m in names:
        counts = {c["domain"]: c["models"].get(m, 0) for c in competitors}
        have = [d for d, n in counts.items() if n]
        mine = client["models"].get(m, 0)
        med = sorted(counts.values())[len(counts) // 2] if counts else 0
        if not have:
            continue
        status = "MISSING" if mine == 0 else ("BEHIND" if mine < med / 2 else "ok")
        rows.append({"model": m, "client": mine, "competitors": counts, "competitors_with_it": len(have),
                     "median": med, "status": status})
    order = {"MISSING": 0, "BEHIND": 1, "ok": 2}
    rows.sort(key=lambda r: (order[r["status"]], -r["competitors_with_it"], -r["median"]))
    return rows


def print_report(client, competitors, gaps, singles, topics, today):
    allsites = [client] + competitors
    print("Market read on {} ({} competitors), {}".format(client["domain"], len(competitors), today.isoformat()))
    print("\n1. Sitemaps")
    for s in allsites:
        flag = " (capped)" if s["capped"] else ""
        print("  {:<32} {:>6} URLs{}  files {:>3}  via {}  lastmod {:.0%}".format(
            s["domain"], s["urls"], flag, s["files_read"], s["sitemaps_found_via"], s["lastmod_coverage"]))
        for e in s["errors"][:3]:
            print("      error: {}".format(e))
    print("\n2. Publishing pace (lastmod is an update date: an upper bound on new pages)")
    print("  {:<32} {:>9} {:>9} {:>9} {:>9}  {}".format("domain", "blog 30d", "blog 90d", "all 30d", "all 90d", "real publications (probe)"))
    for s in allsites:
        pr = s["probe"]
        ptxt = "{} in 30d, {} in 90d ({} of {} dated)".format(pr["published_30d"], pr["published_90d"], pr["with_date"], pr["opened"]) if pr else "-"
        print("  {:<32} {:>9} {:>9} {:>9} {:>9}  {}".format(
            s["domain"], s["pace"]["blog post"]["lastmod_30d"], s["pace"]["blog post"]["lastmod_90d"],
            s["pace"]["all"]["lastmod_30d"], s["pace"]["all"]["lastmod_90d"], ptxt))
        day, n = s["lastmod_most_common_day"]
        if s["urls"] and n / s["urls"] > 0.3:
            print("      warning: {} URLs ({:.0%}) share lastmod {}: a build or import date, pace not readable".format(n, n / s["urls"], day))
    print("\n3. Page models (client vs competitors)")
    head = "  {:<18} {:>8}".format("model", client["domain"][:8])
    for c in competitors:
        head += " {:>10}".format(c["domain"][:10])
    print(head + "  status")
    for g in gaps:
        line = "  {:<18} {:>8}".format(g["model"], g["client"])
        for c in competitors:
            line += " {:>10}".format(g["competitors"][c["domain"]])
        print(line + "  " + g["status"])
    print("\n4. Topics covered by several competitors, absent from {} ({} found)".format(client["domain"], len(topics)))
    for t in topics[:60]:
        print("  [{}] {:<50} {}  e.g. {}".format(len(t["sites"]), t["topic"][:50], t["model"], t["example_urls"][0]))
    print("\n5. Words each competitor uses in its slugs and {} never does".format(client["domain"]))
    for d, words in singles.items():
        print("  {}: {}".format(d, ", ".join(words)))
    print("\nNext: validate demand for each topic (seo-keyword-research), then brief the page skill of its model.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", required=True, help="client site (domain or URL)")
    ap.add_argument("--competitors", nargs="+", required=True, help="competitor domains or URLs (5 recommended)")
    ap.add_argument("--max-files", type=int, default=200, help="sitemap files read per domain (default 200)")
    ap.add_argument("--max-urls", type=int, default=100000, help="URLs read per domain (default 100000)")
    ap.add_argument("--probe", type=int, default=0, help="blog URLs opened per domain to read real publication dates")
    ap.add_argument("--min-sites", type=int, default=2, help="competitors that must cover a topic for it to count (default 2)")
    ap.add_argument("--pause", type=float, default=0.2, help="seconds between sitemap requests (default 0.2)")
    ap.add_argument("--json", help="write the full result (without the URL rows) to this file")
    ap.add_argument("--csv", help="write every URL (domain, url, lang, model, topic, lastmod) to this file")
    args = ap.parse_args()
    today = dt.date.today()

    client = analyse(base_url(args.site), args, today)
    competitors = [analyse(base_url(c), args, today) for c in args.competitors]
    if not client["urls"]:
        print("warning: no URL read on the client sitemap; every model and topic will show as missing", file=sys.stderr)
    gaps = model_gap(client, competitors)
    topics = topic_gap(client, competitors, min(args.min_sites, len(competitors)))
    singles = single_site_topics(competitors, client, 15)
    print_report(client, competitors, gaps, singles, topics, today)

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["domain", "url", "lang", "model", "topic", "lastmod"])
            w.writeheader()
            for s in [client] + competitors:
                w.writerows(s["rows"])
    if args.json:
        strip = lambda s: {k: v for k, v in s.items() if k != "rows"}
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"date": today.isoformat(), "client": strip(client), "competitors": [strip(c) for c in competitors],
                       "model_gap": gaps, "topic_gap": topics, "single_site_words": singles}, f, ensure_ascii=False, indent=2)
    return 0 if client["urls"] and any(c["urls"] for c in competitors) else 1


if __name__ == "__main__":
    sys.exit(main())
