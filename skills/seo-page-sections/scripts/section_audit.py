#!/usr/bin/env python3
"""Section-level detector for web pages.

Answers one question per page: which of the sections and elements that a page
of this type is supposed to have are actually present in the raw HTML?

Unlike a classic SEO crawler, this does not judge title length or image weight
(seo-geo-audit/scripts/seo_audit.py already does that). It looks for BLOCKS:
breadcrumb, FAQ, comparison table, spec table, reviews, ratings, price in text,
definitions, author block, trust badges, CTA, video, cross-links, contact info.

Detection is deliberately generous (several independent signals per block, in
English and French) and every hit records WHY it fired, so the model can
discount a false positive instead of trusting a bare boolean. Absence is
reported as "not found in raw HTML", never as proof the block does not exist:
a client-rendered site hides everything from this parser, which is itself the
finding.

Zero external dependencies (standard library only, Python 3.9+). Output is a
readable report followed by a JSON block a model can parse. The JUDGMENT
(which missing block matters most, what to write in it) belongs to the model
guided by references/page-type-matrix.md and references/section-library.md.

Usage:
    python3 section_audit.py https://example.com/products/thing
    python3 section_audit.py https://example.com/p/a https://example.com/p/b
    python3 section_audit.py https://example.com/x --type product
"""

import argparse
import gzip
import json
import re
import ssl
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

TIMEOUT = 15

PAGE_TYPES = ["product", "service", "collection", "location", "comparison",
              "audience", "blog", "homepage", "pricing", "about", "contact"]

# Bilingual keyword sets. Add your market's language here if it is not covered:
# the detector degrades to "not found" on an unknown language, which reads as a
# false negative in the report.
KW = {
    "breadcrumb": ["breadcrumb", "fil d'ariane", "fil dariane", "ariane"],
    "faq": ["faq", "frequently asked", "questions frequentes", "questions frequemment",
            "foire aux questions", "vos questions", "questions reponses"],
    "reviews": ["review", "testimonial", "avis", "temoignage", "customer stories",
                "ils nous font confiance", "verified buyer", "acheteur verifie"],
    "rating": ["rating", "stars", "etoiles", "note moyenne", "average rating",
               "aggregaterating", "out of 5", "sur 5"],
    "definitions": ["glossary", "glossaire", "definitions", "definition",
                    "lexique", "jargon", "vocabulaire", "terms explained"],
    "author": ["about the author", "a propos de l'auteur", "written by", "ecrit par",
               "redige par", "reviewed by", "relu par", "our team", "notre equipe",
               "who you will work with", "qui vous accompagne", "fondateur", "founder"],
    "trust": ["free shipping", "livraison offerte", "livraison gratuite", "money back",
              "satisfait ou rembourse", "warranty", "garantie", "secure payment",
              "paiement securise", "return", "retour", "refund", "remboursement",
              "delivery", "livraison"],
    "cta": ["add to cart", "ajouter au panier", "buy now", "acheter", "get a quote",
            "demander un devis", "devis gratuit", "book a", "reserver", "prendre rendez",
            "contact us", "nous contacter", "start free", "essai gratuit", "get started",
            "commencer", "sign up", "s'inscrire", "subscribe", "demo"],
    "comparison": [" vs ", " vs. ", "versus", "compared to", "compare a", "comparatif",
                   "comparison", "comparaison", "alternative", "alternatives",
                   "difference between", "difference entre"],
    "pricing": ["pricing", "tarifs", "tarification", "our plans", "nos offres", "nos formules",
                "per month", "par mois", "/mo", "/mois", "free plan", "plan gratuit"],
    "process": ["how it works", "comment ca marche", "notre processus", "our process",
                "step 1", "etape 1", "in 3 steps", "en 3 etapes", "notre methode"],
    "specs": ["specification", "specifications", "caracteristiques", "fiche technique",
              "technical data", "donnees techniques", "dimensions", "materiaux"],
    "logos": ["trusted by", "ils nous font confiance", "as seen in", "vu dans",
              "our clients", "nos clients", "partners", "partenaires", "certifie",
              "certified", "featured in"],
    "guarantee": ["guarantee", "garantie", "risk free", "sans risque", "cancel anytime",
                  "sans engagement", "no credit card", "sans carte bancaire"],
    "hours": ["opening hours", "horaires", "heures d'ouverture", "monday", "lundi",
              "open today", "ouvert aujourd"],
    "map": ["google.com/maps", "maps.google", "openstreetmap", "mapbox", "leaflet"],
    "verdict": ["our verdict", "notre verdict", "bottom line", "en resume", "which one",
                "lequel choisir", "best for", "ideal pour", "recommendation", "recommandation"],
}

CURRENCY_RE = re.compile(
    r"(?:[$€£¥]\s?\d[\d\s.,]*"
    r"|(?<![a-zA-Z])\d[\d\s.,]*\s?(?:€|EUR|USD|GBP|CHF|CAD)(?![a-zA-Z]))")
TEL_RE = re.compile(r"tel:\+?[\d\s().-]{6,}")
MAILTO_RE = re.compile(r"mailto:[^\"'\s>]+@")
POSTAL_RE = re.compile(r"\b\d{4,5}\b\s+[A-ZÀ-Ü][a-zà-ü-]{2,}")
VIDEO_RE = re.compile(r"(youtube\.com/embed|youtu\.be/|player\.vimeo|wistia|loom\.com/embed|<video[\s>])", re.I)
YEAR_RE = re.compile(r"\b(20\d{2})\b")


def strip_accents(s):
    """Fold French accents so 'caracteristiques' matches 'caracteristiques'."""
    table = str.maketrans(
        "àâäáãåèéêëìíîï"
        "òóôöõùúûüçñ",
        "aaaaaaeeeeiiiiooooouuuucn")
    return s.translate(table)


def fetch(url):
    """Return (final_url, status, headers, text). Handles redirects, gzip, lax TLS."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
    })
    with urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            try:
                raw = gzip.decompress(raw)
            except OSError:
                pass
        charset = "utf-8"
        ctype = resp.headers.get("Content-Type", "")
        m = re.search(r"charset=([\w-]+)", ctype, re.I)
        if m:
            charset = m.group(1)
        return resp.geturl(), resp.status, dict(resp.headers), raw.decode(charset, "replace")


class Page(HTMLParser):
    """Collects the structural facts a section audit needs."""

    SKIP_TEXT = {"script", "style", "noscript", "template", "svg"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.headings = []          # (level, text)
        self._heading = None
        self._buf = []
        self.text_parts = []
        self._skip_depth = 0
        self.jsonld_raw = []
        self._in_jsonld = False
        self.tables = 0
        self.table_rows = []        # rows per table
        self._table_stack = []
        self.lists = 0
        self.list_items = 0
        self.details = 0
        self.images = 0
        self.images_no_alt = 0
        self.links = []             # (href, anchor_text)
        self._link_href = None
        self._link_buf = []
        self.forms = 0
        self.inputs = 0
        self.iframes = []
        self.classes = []           # class + id + aria-label values, lowercased
        self.times = []             # datetime attributes
        self.microdata_types = []
        self.buttons = 0

    # -- helpers ---------------------------------------------------------
    def _note_attrs(self, attrs):
        d = dict(attrs)
        for key in ("class", "id", "aria-label", "data-section", "name", "role"):
            v = d.get(key)
            if v:
                self.classes.append(v.lower())
        itemtype = d.get("itemtype")
        if itemtype:
            self.microdata_types.append(itemtype.rsplit("/", 1)[-1])
        return d

    # -- parser hooks ----------------------------------------------------
    def handle_starttag(self, tag, attrs):
        d = self._note_attrs(attrs)
        if tag in self.SKIP_TEXT:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading = int(tag[1])
            self._buf = []
        elif tag == "script" and d.get("type", "").lower() == "application/ld+json":
            self._in_jsonld = True
            self._buf = []
        elif tag == "table":
            self.tables += 1
            self._table_stack.append(0)
        elif tag == "tr" and self._table_stack:
            self._table_stack[-1] += 1
        elif tag in ("ul", "ol"):
            self.lists += 1
        elif tag == "li":
            self.list_items += 1
        elif tag == "details":
            self.details += 1
        elif tag == "img":
            self.images += 1
            if not (d.get("alt") or "").strip():
                self.images_no_alt += 1
        elif tag == "a":
            self._link_href = d.get("href")
            self._link_buf = []
        elif tag == "form":
            self.forms += 1
        elif tag in ("input", "textarea", "select"):
            self.inputs += 1
        elif tag == "button":
            self.buttons += 1
        elif tag == "iframe":
            self.iframes.append(d.get("src") or "")
        elif tag == "time":
            dt = d.get("datetime")
            if dt:
                self.times.append(dt)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in self.SKIP_TEXT and self._skip_depth:
            self._skip_depth -= 1

    def handle_endtag(self, tag):
        if tag in self.SKIP_TEXT and self._skip_depth:
            self._skip_depth -= 1
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._heading:
            text = " ".join("".join(self._buf).split())
            if text:
                self.headings.append((self._heading, text))
            self._heading = None
            self._buf = []
        elif tag == "script" and self._in_jsonld:
            self.jsonld_raw.append("".join(self._buf))
            self._in_jsonld = False
            self._buf = []
        elif tag == "table" and self._table_stack:
            self.table_rows.append(self._table_stack.pop())
        elif tag == "a" and self._link_href is not None:
            self.links.append((self._link_href, " ".join("".join(self._link_buf).split())))
            self._link_href = None
            self._link_buf = []

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data
        if self._heading or self._in_jsonld:
            self._buf.append(data)
        if self._link_href is not None:
            self._link_buf.append(data)
        if not self._skip_depth:
            self.text_parts.append(data)

    # -- derived ---------------------------------------------------------
    @property
    def text(self):
        return " ".join(" ".join(self.text_parts).split())


def schema_types(jsonld_blocks):
    """Flatten every @type found in the JSON-LD blocks, including nested graphs."""
    found = []

    def walk(node):
        if isinstance(node, dict):
            t = node.get("@type")
            if isinstance(t, str):
                found.append(t)
            elif isinstance(t, list):
                found.extend(x for x in t if isinstance(x, str))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for block in jsonld_blocks:
        try:
            walk(json.loads(block))
        except (ValueError, TypeError):
            continue
    return found


def any_kw(haystack, keys):
    """Return the first matching keyword from KW[key] sets, or None."""
    for key in keys:
        for word in KW[key]:
            if word in haystack:
                return word
    return None


def guess_type(url, page, schemas, lowtext):
    """Best-effort page type. The model should override this when it is wrong."""
    path = urlparse(url).path.lower().rstrip("/")
    # Drop a trailing file extension so /acme-vs-globex.html matches the same
    # patterns as /acme-vs-globex/.
    path = re.sub(r"\.(html?|php|aspx?|jsp)$", "", path)
    s = set(schemas)
    if not path or path == "/index":
        return "homepage"
    if "Product" in s or re.search(r"/(product|produit|p)/", path + "/"):
        return "product"
    if "BlogPosting" in s or "Article" in s or re.search(r"/(blog|article|news|actualites)/", path + "/"):
        return "blog"
    if re.search(r"/(collection|category|categorie|shop|boutique|c)/", path + "/"):
        return "collection"
    if any(w in path for w in ("-vs-", "/vs-", "alternative", "comparatif", "comparison", "compare")):
        return "comparison"
    if any(w in path for w in ("pricing", "tarif", "prix", "plans", "offres")):
        return "pricing"
    if any(w in path for w in ("contact",)):
        return "contact"
    if any(w in path for w in ("about", "a-propos", "qui-sommes-nous", "notre-histoire")):
        return "about"
    if "LocalBusiness" in s or any(w in path for w in ("/agence-", "/store", "/magasin", "/boutique-")):
        return "location"
    if re.search(r"/(for|pour)-[a-z]", path) or "Service" in s:
        return "service" if "Service" in s else "audience"
    return "service"


def detect(url, page, status):
    """Run every block detector. Each result: found (bool) + evidence (list of reasons)."""
    text = page.text
    low = strip_accents(text.lower())
    html_classes = strip_accents(" ".join(page.classes))
    schemas = schema_types(page.jsonld_raw) + page.microdata_types
    sset = set(schemas)
    headings = page.headings
    head_text = strip_accents(" ".join(h for _, h in headings).lower())
    questions = [h for lvl, h in headings if h.strip().endswith("?")]
    words = len(text.split())

    host = urlparse(url).netloc
    internal, external = [], []
    for href, anchor in page.links:
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        netloc = urlparse(href).netloc
        (internal if (not netloc or netloc == host) else external).append((href, anchor))

    checks = {}

    def add(name, evidence):
        checks[name] = {"found": bool(evidence), "evidence": evidence}

    # Breadcrumb
    ev = []
    if "BreadcrumbList" in sset:
        ev.append("BreadcrumbList JSON-LD present")
    if any_kw(html_classes, ["breadcrumb"]):
        ev.append("breadcrumb class, id or aria-label in markup")
    add("breadcrumb", ev)

    # FAQ
    ev = []
    if "FAQPage" in sset or "Question" in sset:
        ev.append("FAQPage or Question JSON-LD present")
    kw = any_kw(head_text, ["faq"])
    if kw:
        ev.append("heading contains '%s'" % kw)
    if len(questions) >= 3:
        ev.append("%d headings end with a question mark" % len(questions))
    if page.details >= 3:
        ev.append("%d <details> accordions" % page.details)
    add("faq", ev)

    # Reviews and ratings
    ev = []
    if "Review" in sset:
        ev.append("Review JSON-LD present")
    kw = any_kw(low, ["reviews"])
    if kw:
        ev.append("page text contains '%s'" % kw)
    if any_kw(html_classes, ["reviews"]):
        ev.append("review or testimonial class in markup")
    add("reviews", ev)

    ev = []
    if "AggregateRating" in sset:
        ev.append("AggregateRating JSON-LD present")
    kw = any_kw(low, ["rating"])
    if kw:
        ev.append("page text contains '%s'" % kw)
    add("rating_summary", ev)

    # Price as HTML text
    ev = []
    hits = CURRENCY_RE.findall(text)
    if hits:
        ev.append("%d currency amounts in raw HTML text (e.g. '%s')" % (len(hits), hits[0].strip()))
    if "Offer" in sset:
        ev.append("Offer JSON-LD present")
    add("price_in_text", ev)

    # Tables
    ev = []
    if page.tables:
        ev.append("%d HTML table(s), rows per table: %s" % (page.tables, page.table_rows or "n/a"))
    add("any_table", ev)

    ev = []
    kw = any_kw(head_text + " " + html_classes, ["comparison"])
    if kw and page.tables:
        ev.append("table present and heading or markup contains '%s'" % kw.strip())
    elif kw:
        ev.append("heading or markup contains '%s' but no HTML table found" % kw.strip())
    add("comparison_table", ev)

    ev = []
    kw = any_kw(head_text + " " + html_classes, ["specs"])
    if kw:
        ev.append("heading or markup contains '%s'" % kw)
    if page.tables and kw:
        ev.append("HTML table present alongside it")
    add("spec_table", ev)

    # Definitions
    ev = []
    kw = any_kw(head_text + " " + html_classes, ["definitions"])
    if kw:
        ev.append("heading or markup contains '%s'" % kw)
    if "DefinedTerm" in sset or "DefinedTermSet" in sset:
        ev.append("DefinedTerm JSON-LD present")
    add("definitions", ev)

    # Author / expertise
    ev = []
    if "Person" in sset:
        ev.append("Person JSON-LD present")
    kw = any_kw(low, ["author"])
    if kw:
        ev.append("page text contains '%s'" % kw)
    add("author_block", ev)

    # Trust and guarantee
    ev = []
    kw = any_kw(low, ["trust"])
    if kw:
        ev.append("page text contains '%s'" % kw)
    add("trust_badges", ev)

    ev = []
    kw = any_kw(low, ["guarantee"])
    if kw:
        ev.append("page text contains '%s'" % kw)
    add("guarantee", ev)

    # Social proof logos
    ev = []
    kw = any_kw(low + " " + html_classes, ["logos"])
    if kw:
        ev.append("page text or markup contains '%s'" % kw)
    add("social_proof_logos", ev)

    # CTA
    ev = []
    kw = any_kw(low, ["cta"])
    if kw:
        ev.append("action phrase '%s' in page text" % kw)
    if page.buttons:
        ev.append("%d <button> elements" % page.buttons)
    add("cta", ev)

    # Process / how it works
    ev = []
    kw = any_kw(head_text, ["process"])
    if kw:
        ev.append("heading contains '%s'" % kw)
    if "HowTo" in sset:
        ev.append("HowTo JSON-LD present")
    add("process_block", ev)

    # Pricing signals
    ev = []
    kw = any_kw(head_text + " " + low, ["pricing"])
    if kw:
        ev.append("page contains '%s'" % kw)
    add("pricing_block", ev)

    # Verdict / recommendation (comparison pages)
    ev = []
    kw = any_kw(head_text, ["verdict"])
    if kw:
        ev.append("heading contains '%s'" % kw)
    add("verdict_block", ev)

    # Media
    ev = []
    if VIDEO_RE.search(" ".join(page.iframes) + " " + str(page.images)):
        ev.append("video embed in iframe")
    for src in page.iframes:
        if VIDEO_RE.search(src):
            ev.append("video iframe: %s" % src[:80])
            break
    if "VideoObject" in sset:
        ev.append("VideoObject JSON-LD present")
    add("video", ev)

    ev = []
    if page.images:
        ev.append("%d <img>, %d without alt text" % (page.images, page.images_no_alt))
    add("images", ev)

    # NAP / contact
    ev = []
    if TEL_RE.search(str(page.links) + text):
        ev.append("tel: link or phone number present")
    if MAILTO_RE.search(str(page.links)):
        ev.append("mailto: link present")
    if POSTAL_RE.search(text):
        ev.append("postal-code-like pattern in text")
    if "PostalAddress" in sset:
        ev.append("PostalAddress JSON-LD present")
    add("contact_details", ev)

    ev = []
    kw = any_kw(low, ["hours"])
    if kw:
        ev.append("page text contains '%s'" % kw)
    if "openingHours" in " ".join(page.jsonld_raw):
        ev.append("openingHours in JSON-LD")
    add("opening_hours", ev)

    ev = []
    if any(re.search(r"(maps|mapbox|openstreetmap|leaflet)", s, re.I) for s in page.iframes):
        ev.append("map iframe present")
    kw = any_kw(low, ["map"])
    if kw:
        ev.append("map provider referenced in page")
    add("map_embed", ev)

    # Form
    ev = []
    if page.forms:
        ev.append("%d form(s), %d input fields" % (page.forms, page.inputs))
    add("form", ev)

    # Freshness
    ev = []
    if page.times:
        ev.append("datetime attribute(s): %s" % ", ".join(page.times[:3]))
    if "dateModified" in " ".join(page.jsonld_raw):
        ev.append("dateModified in JSON-LD")
    years = set(YEAR_RE.findall(text))
    if years:
        ev.append("year(s) mentioned in text: %s" % ", ".join(sorted(years)[-3:]))
    add("freshness_signal", ev)

    # Cross-links
    ev = []
    if internal:
        ev.append("%d internal links" % len(internal))
    add("internal_links", ev)

    stype = guess_type(url, page, schemas, low)

    return {
        "url": url,
        "http_status": status,
        "page_type_guess": stype,
        "title": (page.title or "").strip() or None,
        "word_count": words,
        "likely_js_rendered": words < 200,
        "h1_count": sum(1 for lvl, _ in headings if lvl == 1),
        "headings": [{"level": lvl, "text": txt} for lvl, txt in headings],
        "question_headings": questions,
        "schema_types": sorted(set(schemas)),
        "tables": page.tables,
        "lists": page.lists,
        "list_items": page.list_items,
        "internal_link_count": len(internal),
        "external_link_count": len(external),
        "checks": checks,
    }


def report(res):
    """Human-readable summary; the JSON block below it is the machine surface."""
    out = []
    out.append("=" * 72)
    out.append("SECTION AUDIT: %s" % res["url"])
    out.append("=" * 72)
    out.append("HTTP %s | type guess: %s | %d words | H1 count: %d"
               % (res["http_status"], res["page_type_guess"], res["word_count"], res["h1_count"]))
    if res["likely_js_rendered"]:
        out.append("WARNING: under 200 words in raw HTML. Two possible causes, and they need")
        out.append("         opposite fixes, so tell them apart in a browser before reporting:")
        out.append("         (a) the page is client-rendered, so every 'not found' below is")
        out.append("             unreliable and AI crawlers see the same emptiness this parser")
        out.append("             sees. That rendering problem outranks every other finding.")
        out.append("         (b) the page really is that thin, and the missing blocks are real.")
    out.append("")
    out.append("Schema types: %s" % (", ".join(res["schema_types"]) or "none"))
    out.append("Tables: %d | lists: %d (%d items) | internal links: %d"
               % (res["tables"], res["lists"], res["list_items"], res["internal_link_count"]))
    out.append("")
    out.append("BLOCKS FOUND")
    for name, c in sorted(res["checks"].items()):
        if c["found"]:
            out.append("  [x] %-20s %s" % (name, "; ".join(c["evidence"])))
    out.append("")
    out.append("BLOCKS NOT FOUND IN RAW HTML")
    missing = [n for n, c in sorted(res["checks"].items()) if not c["found"]]
    for name in missing:
        out.append("  [ ] %s" % name)
    if not missing:
        out.append("  (none)")
    out.append("")
    out.append("HEADING OUTLINE")
    for h in res["headings"][:60]:
        out.append("  %sH%d: %s" % ("  " * (h["level"] - 1), h["level"], h["text"][:90]))
    if len(res["headings"]) > 60:
        out.append("  ... %d more headings" % (len(res["headings"]) - 60))
    out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Detect which sections a page actually has.")
    ap.add_argument("urls", nargs="+", help="One or more full URLs")
    ap.add_argument("--type", choices=PAGE_TYPES, default=None,
                    help="Force the page type instead of guessing (applies to every URL)")
    ap.add_argument("--json-only", action="store_true", help="Print only the JSON block")
    args = ap.parse_args()

    results = []
    for url in args.urls:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        try:
            final_url, status, _, html = fetch(url)
        except HTTPError as e:
            results.append({"url": url, "error": "HTTP %s" % e.code})
            continue
        except (URLError, OSError, ValueError) as e:
            results.append({"url": url, "error": str(e)})
            continue
        page = Page()
        try:
            page.feed(html)
        except Exception as e:  # malformed markup should not kill the run
            print("warning: HTML parse issue on %s (%s)" % (url, e), file=sys.stderr)
        res = detect(final_url, page, status)
        if args.type:
            res["page_type_guess"] = args.type
            res["page_type_forced"] = True
        results.append(res)
        if not args.json_only:
            print(report(res))

    print("--- JSON ---")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
