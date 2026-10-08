#!/usr/bin/env python3
"""Crawl a whole site the way a search engine discovers it, and report the
site-level problems a single-page audit cannot see.

Starts at the homepage, follows internal links breadth first (respecting
robots.txt for the generic user agent), and records per page: status,
redirect chain, click depth, title, meta description, H1, canonical,
noindex, word count, internal links with anchors, and dates. Then reports:

  - status: non-200 pages, broken internal links, links pointing to redirects,
    redirect chains of 2+ hops
  - indexability: noindexed or canonicalized pages that receive internal links,
    sitemap URLs that are not 200, noindex, redirected or canonicalized away
  - orphans: sitemap URLs the crawl never reached through links
  - depth: click-depth distribution, indexable pages deeper than 3 clicks
  - weak pages: indexable pages with fewer than 3 inbound internal links
  - duplicates: identical titles, meta descriptions and H1, missing ones
  - thin pages: indexable pages under 300 words
  - cannibalization candidates: page pairs whose title + H1 target the same terms
  - anchors: pages whose inbound anchors are mostly generic or empty
  - freshness: a past year in the title, a modification date older than 12 months

The page parser is the one in seo-geo-audit/scripts/seo_audit.py, so both
scripts read pages the same way. Zero external dependencies (Python 3.9+),
read only, polite (one request at a time per worker, 4 workers by default).

Usage:
    python3 site_crawl.py https://example.com
    python3 site_crawl.py https://example.com --max-pages 500 --out crawl.json
    python3 site_crawl.py https://example.com --include-params --json
"""

import argparse
import datetime
import importlib.util
import json
import os
import re
import ssl
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener, HTTPSHandler
from urllib import robotparser

HERE = os.path.dirname(os.path.abspath(__file__))
SEO_AUDIT = os.path.normpath(os.path.join(HERE, "..", "..", "seo-geo-audit", "scripts", "seo_audit.py"))


def load_auditor():
    if not os.path.exists(SEO_AUDIT):
        sys.stderr.write("site_crawl.py needs seo-geo-audit/scripts/seo_audit.py next to this skill "
                         "(install the whole skill set).\n")
        raise SystemExit(2)
    spec = importlib.util.spec_from_file_location("seo_audit", SEO_AUDIT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SA = load_auditor()
UA = SA.UA
TIMEOUT = 15
SKIP_EXT = re.compile(r"\.(jpg|jpeg|png|gif|webp|avif|svg|ico|pdf|zip|rar|gz|mp4|mp3|mov|avi|webm|"
                      r"css|js|json|xml|txt|woff2?|ttf|eot|docx?|xlsx?|pptx?|csv)$", re.I)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _opener():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return build_opener(NoRedirect(), HTTPSHandler(context=ctx))


OPENER = _opener()


def fetch_chain(url, max_hops=6):
    """Follow redirects by hand. Returns (chain, final_url, status, headers, body)."""
    chain = []
    cur = url
    for _ in range(max_hops):
        req = Request(cur, headers={"User-Agent": UA, "Accept": "text/html,*/*;q=0.8",
                                    "Accept-Encoding": "gzip", "Accept-Language": "en-US,en;q=0.9"})
        try:
            resp = OPENER.open(req, timeout=TIMEOUT)
            body = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                import gzip
                try:
                    body = gzip.decompress(body)
                except OSError:
                    pass
            return chain, cur, resp.status, dict(resp.headers), body
        except HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and e.headers.get("Location"):
                chain.append((e.code, cur))
                cur = urldefrag(urljoin(cur, e.headers["Location"]))[0]
                continue
            return chain, cur, e.code, dict(e.headers or {}), b""
        except (URLError, ssl.SSLError, OSError, ValueError) as e:
            return chain, cur, 0, {"error": str(e)}, b""
    return chain, cur, 310, {}, b""  # too many redirects


def norm(url, include_params):
    url = urldefrag(url)[0]
    p = urlparse(url)
    if not include_params and p.query:
        url = url.split("?", 1)[0]
    if p.path == "":
        url = url + "/"
    return url


def year_in(text):
    return [int(y) for y in re.findall(r"\b(20[0-3]\d)\b", text or "")]


def find_dates(objects, article_meta):
    blob = json.dumps(objects)
    mod = re.findall(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})', blob)
    pub = re.findall(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', blob)
    mod = mod or [v[:10] for k, v in article_meta.items() if "modified" in k and v]
    pub = pub or [v[:10] for k, v in article_meta.items() if "published" in k and v]
    return (max(mod) if mod else None), (min(pub) if pub else None)


def crawl_page(url, host, include_params):
    chain, final, status, headers, body = fetch_chain(url)
    rec = {"url": url, "final": final, "status": status,
           "redirects": [c[0] for c in chain], "links": []}
    ctype = (headers.get("Content-Type") or headers.get("content-type") or "")
    if status != 200 or "html" not in ctype.lower():
        rec["html"] = False
        return rec
    m = re.search(r"charset=([\w-]+)", ctype, re.I)
    try:
        html = body.decode(m.group(1) if m else "utf-8", errors="replace")
    except LookupError:
        html = body.decode("utf-8", errors="replace")
    p = SA.Page()
    try:
        p.feed(html)
    except Exception:
        pass
    robots = ((p.meta_robots or "") + "," + (headers.get("X-Robots-Tag") or headers.get("x-robots-tag") or "")).lower()
    canon = urljoin(final, p.canonical) if p.canonical else None
    modified, published = find_dates(p.jsonld_objects, p.article_meta)
    lm = re.search(r"<html[^>]*\blang=[\"']?([\w-]+)", html, re.I)
    seg = urlparse(final).path.strip("/").split("/")[0]
    lang = (lm.group(1) if lm else "").split("-")[0].lower()
    if re.fullmatch(r"[a-z]{2}(-[a-z]{2})?", seg or ""):
        lang = seg.split("-")[0]
    rec.update({
        "html": True,
        "lang": lang,
        "title": (p.title or "").strip(),
        "meta": (p.meta_description or "").strip(),
        "h1": [t for lvl, t, _ in p.headings if lvl == 1],
        "canonical": canon,
        "canonical_other": bool(canon and norm(canon, True).rstrip("/") != norm(final, True).rstrip("/")),
        "noindex": "noindex" in robots,
        "words": p.word_count(),
        "date_modified": modified,
        "date_published": published,
    })
    for l in p.links:
        h = (l.get("href") or "").strip()
        if not h or h.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
            continue
        absu = urljoin(final, h)
        pu = urlparse(absu)
        if pu.scheme not in ("http", "https") or pu.netloc != host:
            continue
        if SKIP_EXT.search(pu.path) or pu.path.startswith("/cdn-cgi/"):
            continue
        rec["links"].append({"to": norm(absu, include_params), "anchor": l.get("text") or l.get("aria") or "",
                             "nofollow": "nofollow" in (l.get("rel") or "")})
    return rec


def read_sitemaps(base, robots_txt):
    urls = []
    maps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", robots_txt or "") or [urljoin(base, "/sitemap.xml")]
    todo, seen = list(maps), set()
    while todo and len(seen) < 25:
        sm = todo.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        _, _, status, _, body = fetch_chain(sm)
        if status != 200:
            continue
        xml = body.decode("utf-8", errors="replace")
        locs = [x.strip() for x in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", xml)]
        if "<sitemapindex" in xml:
            todo.extend(locs)
        else:
            urls.extend(locs)
        if len(urls) > 50000:
            break
    return urls


def main():
    ap = argparse.ArgumentParser(description="Crawl a site and report site-level SEO problems")
    ap.add_argument("url", help="homepage URL")
    ap.add_argument("--max-pages", type=int, default=300, help="crawl budget (default 300)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--include-params", action="store_true", help="crawl URLs with ?parameters")
    ap.add_argument("--out", help="write the full JSON to this file (input for content_decay.py --crawl)")
    ap.add_argument("--json", action="store_true", help="print the JSON summary only")
    ap.add_argument("--top", type=int, default=15, help="rows per section")
    args = ap.parse_args()

    base = args.url if args.url.startswith("http") else "https://" + args.url
    _, start, status, _, _ = fetch_chain(base)
    if status != 200:
        sys.stderr.write("Homepage answered {} at {}\n".format(status, start))
    host = urlparse(start).netloc
    start = norm(start, args.include_params)

    rp = robotparser.RobotFileParser()
    _, _, rstatus, _, rbody = fetch_chain(urljoin(start, "/robots.txt"))
    robots_txt = rbody.decode("utf-8", errors="replace") if rstatus == 200 else ""
    rp.parse(robots_txt.splitlines())

    pages, depth = {}, {start: 0}
    frontier, blocked, truncated = [start], set(), False
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        d = 0
        while frontier:
            room = args.max_pages - len(pages)
            if room <= 0:
                truncated = True
                break
            batch = frontier[:room]
            truncated = truncated or len(frontier) > room
            results = list(ex.map(lambda u: crawl_page(u, host, args.include_params), batch))
            nxt = []
            for rec in results:
                pages[rec["url"]] = rec
                for l in rec["links"]:
                    t = l["to"]
                    if t in depth:
                        continue
                    if robots_txt and not rp.can_fetch("*", t):
                        blocked.add(t)
                        continue
                    depth[t] = d + 1
                    nxt.append(t)
            frontier = nxt
            d += 1

    for u, rec in pages.items():
        rec["depth"] = depth.get(u)
    final_of = {u: r["final"] for u, r in pages.items()}
    status_of = {u: r["status"] for u, r in pages.items()}

    # Inbound links (resolved through redirects), anchors per target
    inbound = defaultdict(set)
    anchors = defaultdict(list)
    broken, to_redirect = [], []
    for u, rec in pages.items():
        for l in rec["links"]:
            t = l["to"]
            if t == u:
                continue
            st = status_of.get(t)
            if st is not None and st >= 400 or st == 0:
                broken.append({"from": u, "to": t, "status": st, "anchor": l["anchor"][:60]})
            if t in pages and pages[t]["redirects"]:
                to_redirect.append({"from": u, "to": t, "final": final_of[t]})
            tgt = norm(final_of.get(t, t), args.include_params)
            inbound[tgt].add(u)
            anchors[tgt].append(l["anchor"])

    html_pages = {u: r for u, r in pages.items() if r.get("html")}
    by_final = {}
    for u, r in html_pages.items():
        by_final.setdefault(norm(r["final"], args.include_params), r)
    indexable = {u: r for u, r in by_final.items() if not r["noindex"] and not r["canonical_other"]}
    # Legal, account and login pages are meant to be minor: keep them out of
    # the thin and weak-inbound lists.
    content = {u: r for u, r in indexable.items() if not SA.LEGAL_PATH_RE.search(urlparse(u).path)}

    def dupes(field):
        # Compared within one language: the same title on /fr/ and /de/ is a
        # translation question, not a duplicate.
        groups = defaultdict(list)
        for u, r in indexable.items():
            v = r.get(field)
            v = " | ".join(v) if isinstance(v, list) else v
            if v:
                groups[(r.get("lang"), v.strip().lower())].append(u)
        return [{"value": k[1][:90], "lang": k[0], "urls": v} for k, v in groups.items() if len(v) > 1]

    linked_noindex = [{"url": u, "inbound": len(inbound.get(u, ())), "reason": "noindex" if r["noindex"] else "canonical elsewhere"}
                      for u, r in by_final.items() if (r["noindex"] or r["canonical_other"]) and inbound.get(u)]
    home = norm(start, args.include_params)
    weak = sorted([{"url": u, "inbound": len(inbound.get(u, ()))} for u in content
                   if u != home and len(inbound.get(u, ())) < 3], key=lambda x: x["inbound"])
    deep = sorted([{"url": u, "depth": r["depth"]} for u, r in indexable.items()
                   if r.get("depth") is not None and r["depth"] > 3], key=lambda x: -x["depth"])
    depth_dist = Counter(r.get("depth") for r in indexable.values())
    thin = sorted([{"url": u, "words": r["words"]} for u, r in content.items() if r["words"] < 300],
                  key=lambda x: x["words"])
    missing = {"title": [u for u, r in indexable.items() if not r["title"]],
               "meta": [u for u, r in indexable.items() if not r["meta"]],
               "h1": [u for u, r in indexable.items() if not r["h1"]],
               "multiple_h1": [u for u, r in indexable.items() if len(r["h1"]) > 1]}
    chains = [{"url": u, "hops": len(r["redirects"]), "codes": r["redirects"], "final": r["final"]}
              for u, r in pages.items() if len(r["redirects"]) >= 2]
    errors = [{"url": u, "status": r["status"]} for u, r in pages.items() if r["status"] != 200 and not r["redirects"]]

    # Cannibalization: same target terms in title + H1
    # Terms present in the titles of 30%+ of the pages (the brand, a site-wide
    # suffix) say nothing about the target query: drop them before comparing.
    terms = {u: set(SA._content_terms((r["title"] or "") + " " + " ".join(r["h1"]))) for u, r in content.items()}
    df = Counter(t for ts in terms.values() for t in ts)
    common = {t for t, n in df.items() if len(terms) >= 10 and n / len(terms) >= 0.3}
    terms = {u: ts - common for u, ts in terms.items()}
    cannibal = []
    keys = list(terms)
    for i in range(len(keys)):
        a = terms[keys[i]]
        if len(a) < 2:
            continue
        for j in range(i + 1, len(keys)):
            if content[keys[i]].get("lang") != content[keys[j]].get("lang"):
                continue
            b = terms[keys[j]]
            if len(b) < 2:
                continue
            inter = len(a & b)
            jac = inter / len(a | b)
            if inter >= 2 and jac >= 0.6:
                cannibal.append({"a": keys[i], "b": keys[j], "shared": sorted(a & b)[:6], "similarity": round(jac, 2)})
    cannibal.sort(key=lambda x: -x["similarity"])

    # Anchors: mostly generic or empty
    generic_targets = []
    for u, lst in anchors.items():
        if u not in indexable or len(lst) < 3:
            continue
        bad = sum(1 for a in lst if not a.strip() or SA._norm(a).strip(" .") in SA.GENERIC_ANCHORS)
        if bad / len(lst) > 0.5:
            generic_targets.append({"url": u, "generic_share": round(100 * bad / len(lst)), "links": len(lst)})

    # Sitemap: orphans and non-indexable entries
    sm_urls = read_sitemaps(start, robots_txt)
    crawled = set(pages) | set(by_final)
    sm_norm = [norm(x, True) for x in sm_urls]
    orphans = [x for x in sm_norm if x not in crawled and norm(x, args.include_params) not in crawled][:500]
    sm_bad = []
    for x in sm_norm:
        r = pages.get(x)
        if not r:
            continue
        if r["status"] != 200 or r["redirects"]:
            sm_bad.append({"url": x, "issue": "status {}".format(r["status"]) if not r["redirects"] else "redirects to " + r["final"]})
        elif r.get("noindex"):
            sm_bad.append({"url": x, "issue": "noindex"})
        elif r.get("canonical_other"):
            sm_bad.append({"url": x, "issue": "canonical to " + r["canonical"]})

    # Freshness
    this_year = datetime.date.today().year
    stale = []
    for u, r in indexable.items():
        yrs = [y for y in year_in(r["title"]) if y < this_year]
        old_mod = None
        if r.get("date_modified"):
            try:
                age = (datetime.date.today() - datetime.date.fromisoformat(r["date_modified"])).days
                old_mod = age if age > 365 else None
            except ValueError:
                pass
        if yrs or old_mod:
            stale.append({"url": u, "title_years": yrs, "date_modified": r.get("date_modified"),
                          "days_since_update": old_mod})

    summary = {
        "start": start, "pages_crawled": len(pages), "html_pages": len(html_pages),
        "indexable_pages": len(indexable), "truncated": truncated, "blocked_by_robots": len(blocked),
        "sitemap_urls": len(sm_urls),
        "errors": errors, "broken_links": broken, "links_to_redirects": to_redirect, "redirect_chains": chains,
        "linked_non_indexable": linked_noindex, "sitemap_non_indexable": sm_bad,
        "orphans": orphans if not truncated else [], "orphans_unreliable": truncated,
        "depth_distribution": {str(k): v for k, v in sorted(depth_dist.items(), key=lambda kv: (kv[0] is None, kv[0]))},
        "deep_pages": deep, "weak_inbound": weak, "thin_pages": thin,
        "duplicate_titles": dupes("title"), "duplicate_meta": dupes("meta"), "duplicate_h1": dupes("h1"),
        "missing": missing, "cannibalization": cannibal, "generic_anchor_targets": generic_targets,
        "stale": stale,
    }
    full = dict(summary)
    full["pages"] = [{k: v for k, v in r.items() if k != "links"} | {"inbound": len(inbound.get(norm(r["final"], args.include_params), ())),
                                                                       "outlinks": len(r["links"])}
                     for r in pages.values()]
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(full, fh, ensure_ascii=False, indent=1)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False))
        return 0

    T = args.top
    L = ["=" * 74, "SITE CRAWL  {}".format(start), "=" * 74]
    L.append("pages crawled {} | HTML {} | indexable {} | sitemap URLs {} | blocked by robots {}{}".format(
        len(pages), len(html_pages), len(indexable), len(sm_urls), len(blocked),
        " | TRUNCATED at --max-pages (orphan list not reliable)" if truncated else ""))
    L.append("click depth (indexable): " + ", ".join("{}: {}".format(k, v) for k, v in summary["depth_distribution"].items()))

    def section(title, rows, fmt):
        L.append("\n## {} ({})".format(title, len(rows)))
        for r in rows[:T]:
            L.append("  - " + fmt(r))
        if len(rows) > T:
            L.append("  ... {} more (use --out for the full list)".format(len(rows) - T))

    section("Pages in error", errors, lambda r: "{} {}".format(r["status"], r["url"]))
    section("Broken internal links", broken, lambda r: "{} -> {} ({}) anchor '{}'".format(r["from"], r["to"], r["status"], r["anchor"]))
    section("Internal links pointing to a redirect", to_redirect, lambda r: "{} -> {} => {}".format(r["from"], r["to"], r["final"]))
    section("Redirect chains (2+ hops)", chains, lambda r: "{} {} hops {} => {}".format(r["url"], r["hops"], r["codes"], r["final"]))
    section("Linked pages that are noindex or canonicalized away", linked_noindex, lambda r: "{} ({}, {} inbound)".format(r["url"], r["reason"], r["inbound"]))
    section("Sitemap URLs that should not be there", sm_bad, lambda r: "{} ({})".format(r["url"], r["issue"]))
    if truncated:
        L.append("\n## Orphans: not computed, the crawl hit --max-pages; raise it to cover the site")
    else:
        section("Orphans (in the sitemap, unreachable by links)", orphans, lambda r: r)
    section("Indexable pages deeper than 3 clicks", deep, lambda r: "depth {} {}".format(r["depth"], r["url"]))
    section("Indexable pages with fewer than 3 inbound internal links", weak, lambda r: "{} inbound {}".format(r["inbound"], r["url"]))
    section("Thin pages (under 300 words)", thin, lambda r: "{} words {}".format(r["words"], r["url"]))
    section("Duplicate titles", summary["duplicate_titles"], lambda r: "'{}' x{}: {}".format(r["value"], len(r["urls"]), ", ".join(r["urls"][:3])))
    section("Duplicate meta descriptions", summary["duplicate_meta"], lambda r: "'{}' x{}: {}".format(r["value"][:60], len(r["urls"]), ", ".join(r["urls"][:3])))
    section("Duplicate H1", summary["duplicate_h1"], lambda r: "'{}' x{}: {}".format(r["value"], len(r["urls"]), ", ".join(r["urls"][:3])))
    L.append("\n## Missing: title {} | meta {} | H1 {} | multiple H1 {}".format(
        len(missing["title"]), len(missing["meta"]), len(missing["h1"]), len(missing["multiple_h1"])))
    section("Cannibalization candidates (same terms in title + H1)", cannibal,
            lambda r: "{} <> {} shared {} ({})".format(r["a"], r["b"], r["shared"], r["similarity"]))
    section("Pages whose inbound anchors are mostly generic or empty", generic_targets,
            lambda r: "{}% generic over {} links {}".format(r["generic_share"], r["links"], r["url"]))
    section("Stale pages (past year in the title, or not updated for 12+ months)", stale,
            lambda r: "{} years {} modified {}".format(r["url"], r["title_years"] or "-", r["date_modified"] or "-"))
    L.append("\n" + "=" * 74)
    L.append("Verdicts belong to the model: a cannibalization pair is a candidate until Search Console")
    L.append("shows both URLs ranking for the same queries; a weak page may be intentionally minor.")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
