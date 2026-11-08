#!/usr/bin/env python3
"""Audit an XML sitemap: clean for robots (valid, light, honest) and elegant for people (pretty-printed raw XML).

Follows a sitemap index into its child files and prints raw facts, then a list of findings.
Pure standard library, Python 3.9+, read only, no API key.

Usage:
  python3 sitemap_audit.py https://example.com/sitemap.xml
  python3 sitemap_audit.py https://example.com            (reads robots.txt, falls back to /sitemap.xml)
  python3 sitemap_audit.py https://example.com/sitemap.xml --json report.json --max-children 200
  python3 sitemap_audit.py --format public/sitemap.xml       (rewrites a local file, pretty-printed)

Checks:
  people   pretty-printed like `xmllint --format` (one element per line, two-space indentation,
           no blank lines, no trailing spaces), no xml-stylesheet, no script, no comment
  robots   status, content type, size and URL limits, sitemap index and segmentation,
           duplicates, other hosts, http URLs, lastmod coverage and honesty,
           priority and changefreq (ignored by Google), hreflang weight, URLs per language
"""

import argparse
import collections
import gzip
import json
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0 Safari/537.36 sitemap-audit"
HTML_SITEMAP_PATHS = ("/plan-du-site", "/plan-du-site/", "/sitemap", "/sitemap/", "/site-map", "/sitemap.html", "/html-sitemap")
MAX_URLS = 50000
MAX_BYTES = 50 * 1024 * 1024


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            if r.headers.get("Content-Encoding") == "gzip" or url.endswith(".gz"):
                try:
                    body = gzip.decompress(body)
                except OSError:
                    pass
            return r.status, (r.headers.get("Content-Type") or "").lower(), body, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, (e.headers.get("Content-Type") or "").lower(), b"", url
    except Exception as e:  # network error: report it, do not crash the audit
        return 0, "{}: {}".format(type(e).__name__, e), b"", url


def origin(url):
    p = urlparse(url)
    return (p.scheme, p.hostname, p.port)


def find_sitemap(start):
    p = urlparse(start)
    if p.path and p.path not in ("", "/"):
        return start
    base = "{}://{}".format(p.scheme or "https", p.netloc or p.path)
    status, _, body, _ = fetch(urljoin(base, "/robots.txt"))
    if status == 200:
        found = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", body.decode("utf-8", "replace"))
        if found:
            return found[0]
    return urljoin(base, "/sitemap.xml")


TAG = re.compile(r"<[^>]+>|[^<]+")


def pretty(xml):
    """Canonical layout, as xmllint --format prints it. Drops xml-stylesheet, scripts and comments."""
    decl = re.match(r"\s*(<\?xml\b[^?]*\?>)", xml)
    body = xml[decl.end():] if decl else xml
    body = re.sub(r"<\?xml-stylesheet\b[^?]*\?>", "", body)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"<script\b[^>]*?(/>|>.*?</script\s*>)", "", body, flags=re.S)
    body = re.sub(r">\s+<", "><", body.strip())
    toks = TAG.findall(body)
    out, depth, i = [decl.group(1) if decl else '<?xml version="1.0" encoding="UTF-8"?>'], 0, 0
    while i < len(toks):
        tok = toks[i].strip()
        if not tok:
            i += 1
            continue
        if tok.startswith("</"):
            depth -= 1
            out.append("  " * depth + tok)
        elif tok.startswith("<?") or tok.endswith("/>"):
            out.append("  " * depth + tok)
        elif tok.startswith("<"):
            if i + 2 < len(toks) and not toks[i + 1].startswith("<") and toks[i + 2].startswith("</"):
                out.append("  " * depth + tok + toks[i + 1].strip() + toks[i + 2])
                i += 3
                continue
            out.append("  " * depth + tok)
            depth += 1
        else:
            out.append("  " * depth + tok)
        i += 1
    return "\n".join(out) + "\n"


def check_people(url, xml, cache):
    """Elegance of one sitemap file: pretty-printed raw XML, nothing added on top."""
    lines = xml.split("\n")
    out = {
        "lines": len(lines),
        "stylesheet": bool(re.search(r"<\?xml-stylesheet\b", xml[:3000])),
        "script": bool(re.search(r"<script\b", xml[:10000])),
        "comment": "<!--" in xml,
        "pretty": xml == pretty(xml),
        "first_bad_line": None,
    }
    if not out["pretty"]:
        ref = pretty(xml).split("\n")
        for n, (a, b) in enumerate(zip(lines, ref), 1):
            if a != b:
                out["first_bad_line"] = {"line": n, "found": a[:120], "expected": b[:120]}
                break
    return out


def first_segment(path):
    return path.strip("/").split("/")[0] if path.strip("/") else ""


def analyse_urlset(url, xml, size):
    locs = [l.strip() for l in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", xml)]
    host = urlparse(url).hostname
    lastmods = re.findall(r"<lastmod>\s*([^<]+?)\s*</lastmod>", xml)
    days = collections.Counter(l[:10] for l in lastmods)
    alt_bytes = sum(len(m) for m in re.findall(r"<xhtml:link\b[^>]*/>", xml))
    # Language of a URL: its self-referencing hreflang alternate.
    per_lang = collections.Counter()
    for block in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>\s*([^<]+?)\s*</loc>", block)
        if not loc:
            continue
        for lang, href in re.findall(r'hreflang="([^"]+)"\s+href="([^"]+)"', block):
            if lang != "x-default" and href.strip() == loc.group(1).strip():
                per_lang[lang] += 1
                break
    sections = collections.Counter(first_segment(urlparse(l).path) for l in locs)
    return {
        "url": url,
        "bytes": size,
        "urls": len(locs),
        "duplicates": len(locs) - len(set(locs)),
        "other_hosts": sum(1 for l in locs if urlparse(l).hostname != host),
        "http_urls": sum(1 for l in locs if l.startswith("http://")),
        "lastmod_coverage": round(len(lastmods) / len(locs), 3) if locs else 0,
        "lastmod_top_day": days.most_common(1)[0] if days else None,
        "lastmod_top_day_share": round(days.most_common(1)[0][1] / len(lastmods), 3) if lastmods else 0,
        "lastmod_days": len(days),
        "has_priority": "<priority>" in xml,
        "has_changefreq": "<changefreq>" in xml,
        "hreflang_links": xml.count("<xhtml:link"),
        "hreflang_share_of_bytes": round(alt_bytes / size, 3) if size else 0,
        "per_language": dict(per_lang.most_common()),
        "sections": dict(sections.most_common()),
    }


def audit(start, max_children):
    url = find_sitemap(start)
    report = {"sitemap": url, "files": [], "people": [], "index": None}
    cache = {}
    status, ctype, body, final = fetch(url)
    report["status"], report["content_type"] = status, ctype
    if status != 200 or not body:
        report["error"] = "sitemap not reachable (HTTP {})".format(status)
        return report
    xml = body.decode("utf-8", "replace")
    report["people"].append(dict(file=url, **check_people(url, xml, cache)))
    if "<sitemapindex" in xml:
        children = [c.strip() for c in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", xml)]
        report["index"] = {"children": len(children), "read": min(len(children), max_children)}
        for child in children[:max_children]:
            s, ct, b, _ = fetch(child)
            if s != 200 or not b:
                report["files"].append({"url": child, "error": "HTTP {}".format(s)})
                continue
            cx = b.decode("utf-8", "replace")
            report["people"].append(dict(file=child, **check_people(child, cx, cache)))
            f = analyse_urlset(child, cx, len(b))
            f["content_type"] = ct
            report["files"].append(f)
    else:
        f = analyse_urlset(url, xml, len(body))
        f["content_type"] = ctype
        report["files"].append(f)
    base = "{0.scheme}://{0.netloc}".format(urlparse(url))
    report["html_sitemap"] = []
    for path in HTML_SITEMAP_PATHS:
        s, ct, b, final = fetch(urljoin(base, path))
        if s == 200 and "html" in ct and b"<a " in b:
            report["html_sitemap"].append({"url": final, "links": b.count(b"<a ")})
            break
    return report


def findings(r):
    F = []
    def add(level, who, text):
        F.append((level, who, text))
    if r.get("error"):
        add("BLOCKER", "robots", r["error"])
        return F
    files = [f for f in r["files"] if "urls" in f]
    total = sum(f["urls"] for f in files)
    # People: pretty-printed raw XML, nothing on top
    styled = [p["file"] for p in r["people"] if p.get("stylesheet")]
    if styled:
        add("FIX", "people", "{} file(s) call an xml-stylesheet: remove the instruction, the XSL and any polyfill (SMP-11). Raw XML, pretty-printed, is the expected view; Chrome drops native XSLT on 17 November 2026.".format(len(styled)))
    scripted = [p["file"] for p in r["people"] if p.get("script")]
    if scripted:
        add("FIX", "people", "{} file(s) contain a <script> element (often an xslt-polyfill): remove it, a sitemap carries URLs only (SMP-11).".format(len(scripted)))
    ugly = [p for p in r["people"] if not p.get("pretty")]
    for p in ugly[:5]:
        b = p.get("first_bad_line") or {}
        add("FIX", "people", "{} is not pretty-printed ({} lines). First difference at line {}: found '{}', expected '{}'. Run sitemap_audit.py --format on the generated file (SMP-09).".format(
            p["file"], p.get("lines"), b.get("line"), b.get("found"), b.get("expected")))
    if len(ugly) > 5:
        add("FIX", "people", "{} more file(s) not pretty-printed.".format(len(ugly) - 5))
    # Robots
    ctype = r.get("content_type", "")
    if "xml" not in ctype:
        add("FIX", "robots", "Sitemap served as '{}': use application/xml.".format(ctype))
    for f in files:
        if f["urls"] > MAX_URLS or f["bytes"] > MAX_BYTES:
            add("BLOCKER", "robots", "{} exceeds 50,000 URLs or 50 MB: Google rejects the whole file.".format(f["url"]))
        if f["duplicates"]:
            add("FIX", "robots", "{} duplicate URLs in {}.".format(f["duplicates"], f["url"]))
        if f["other_hosts"]:
            add("FIX", "robots", "{} URLs on another host in {}: a sitemap lists its own host only.".format(f["other_hosts"], f["url"]))
        if f["http_urls"]:
            add("FIX", "robots", "{} http:// URLs in {}: list the final https URLs.".format(f["http_urls"], f["url"]))
        if f["lastmod_coverage"] < 1 and f["urls"]:
            add("WATCH", "robots", "lastmod on {:.0%} of URLs in {}.".format(f["lastmod_coverage"], f["url"]))
        if f["lastmod_top_day_share"] >= 0.4 and f["urls"] >= 50:
            day, n = f["lastmod_top_day"]
            add("FIX", "robots", "{} URLs ({:.0%}) share lastmod {} in {}: a build or import date, not a content date. Google ignores lastmod it finds inaccurate. Use the date of the last real content change.".format(n, f["lastmod_top_day_share"], day, f["url"]))
        if f["has_priority"] or f["has_changefreq"]:
            add("MINOR", "robots", "priority and changefreq in {}: Google ignores both. Remove them to lighten the file and the view.".format(f["url"]))
        if f["hreflang_share_of_bytes"] >= 0.5:
            add("WATCH", "robots", "hreflang links are {:.0%} of {} ({} links). Valid, but heavy: keep them only if the pages do not already carry the same hreflang tags, and segment the file.".format(f["hreflang_share_of_bytes"], f["url"], f["hreflang_links"]))
        langs = f["per_language"]
        if len(langs) > 1 and len(set(langs.values())) > 1:
            add("FIX", "robots", "URLs per language differ in {}: {}. Find the pages missing in some languages (seo-technical, Step 2).".format(f["url"], langs))
    if r.get("index") is None and total >= 500:
        add("FIX", "robots", "One single file for {} URLs: split by section and language under a sitemap index, so Search Console reports indexation per template and each file stays readable.".format(total))
    return F


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("url", help="site or sitemap URL, or a local file with --format")
    ap.add_argument("--format", action="store_true", help="pretty-print the local sitemap file given as url, in place")
    ap.add_argument("--max-children", type=int, default=100)
    ap.add_argument("--json", help="write the full report to this file")
    a = ap.parse_args()
    if a.format:
        with open(a.url, encoding="utf-8") as fh:
            src = fh.read()
        new = pretty(src)
        with open(a.url, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(new)
        print("{}: {} lines, {}".format(a.url, new.count("\n"), "unchanged" if new == src else "reformatted"))
        return 0
    r = audit(a.url, a.max_children)
    F = findings(r)
    print("=" * 70)
    print("SITEMAP AUDIT  {}".format(r["sitemap"]))
    print("=" * 70)
    print("HTTP {}  {}".format(r.get("status"), r.get("content_type")))
    if r.get("index"):
        print("sitemap index: {children} child files ({read} read)".format(**r["index"]))
    for f in r["files"]:
        if "error" in f:
            print("  {}  ERROR {}".format(f["url"], f["error"]))
            continue
        print("\n  {}".format(f["url"]))
        print("    URLs {}  size {:.2f} MB  hreflang links {} ({:.0%} of bytes)".format(
            f["urls"], f["bytes"] / 1048576, f["hreflang_links"], f["hreflang_share_of_bytes"]))
        print("    lastmod: {:.0%} coverage, {} distinct days, most frequent {}".format(
            f["lastmod_coverage"], f["lastmod_days"], f["lastmod_top_day"]))
        print("    priority {}  changefreq {}".format(f["has_priority"], f["has_changefreq"]))
        if f["per_language"]:
            print("    per language: {}".format(", ".join("{} {}".format(k, v) for k, v in f["per_language"].items())))
        top = list(f["sections"].items())[:12]
        print("    sections: {}".format(", ".join("/{} {}".format(k, v) for k, v in top)))
    for p in r["people"]:
        print("\n  people view {}: pretty {}  lines {}  stylesheet {}  script {}".format(
            p["file"], p.get("pretty"), p.get("lines"), p.get("stylesheet"), p.get("script")))
    print("  HTML sitemap page (optional): {}".format(r.get("html_sitemap") or "not found"))
    print("\nFINDINGS")
    if not F:
        print("  none: pretty-printed for people, clean for robots")
    for level, who, text in F:
        print("  [{}] ({}) {}".format(level, who, text))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"report": r, "findings": F}, fh, indent=2, ensure_ascii=False)
    return 1 if any(l in ("BLOCKER", "PRIORITY") for l, _, _ in F) else 0


if __name__ == "__main__":
    sys.exit(main())
