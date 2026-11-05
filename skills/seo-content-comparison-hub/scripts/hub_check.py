#!/usr/bin/env python3
"""Check a comparison hub or "best X" ranking page for the consistency rules a list page breaks most.

Reads one or more pages (URL or saved .html file) and checks, per page:
  - the item count: the number in the H1 (and the title) against the numbered item headings
    (h2/h3 starting with "N.", "N)" or "#N") and against the ItemList JSON-LD
    (numberOfItems and the length of itemListElement), plus the ItemList order and urls
  - a real <table>, and its data rows against the item count
  - JSON-LD that parses, and the presence of ItemList, FAQPage, BreadcrumbList, dateModified
  - FAQPage questions present in the visible text, one FAQ only, counts that match
  - a visible update date and a disclosure keyword near the top of the page (around the H1)
  - em dashes and en dashes in the visible text
  - an internal link inside every item card (between one numbered heading and the next)

Pure standard library, Python 3.9+, read only. Output: a Markdown report on stdout.
Exit code 1 when any page has a high finding, 0 otherwise.

Usage:
  python3 hub_check.py https://example.com/best-crm-software/
  python3 hub_check.py saved-page.html other-page.html
  python3 hub_check.py --top-chars 4000 page.html

Finding codes: count_mismatch, h1_no_count, h1_count_not_exact, items_not_numbered,
numbering_gap, itemlist_missing, itemlist_no_url, itemlist_order_mismatch, table_missing,
table_rows_mismatch, jsonld_invalid, faqpage_missing, faq_missing, faq_jsonld_mismatch,
faq_count_mismatch, faq_duplicate, breadcrumb_missing, datemodified_missing, date_missing,
disclosure_missing, em_dashes, item_no_link, rating_markup_check, fetch_failed.
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

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
TIMEOUT = 20

SKIP_TAGS = {"script", "style", "noscript", "template", "svg", "head"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
             "source", "track", "wbr"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCK_TAGS = HEADINGS | {"p", "div", "li", "tr", "td", "th", "section", "article", "summary",
                         "details", "dt", "dd", "br", "ul", "ol", "table", "caption", "header",
                         "footer", "nav", "aside", "main", "figure", "figcaption", "blockquote"}

# Dashes are written as escapes so this file passes the repository's own style sweep.
DASH_RE = re.compile("[\\u2014\\u2013]")

# "1. Name", "1) Name", "#1 Name", "#1: Name", "No. 1 Name"
ITEM_HEADING_RE = re.compile(r"^\s*(?:#\s?|no\.?\s*)?(\d{1,3})\s*[.):]\s*\S", re.I)
HASH_HEADING_RE = re.compile(r"^\s*#\s?(\d{1,3})\b")
NUMBER_RE = re.compile(r"(?<![\d.,])(\d{1,4})(\s*\+)?(?![\d.,]\d)")
NOT_EXACT_BEFORE = re.compile(r"(more than|over|plus de|mehr als|über|más de|oltre|mais de|meer dan)\s*$", re.I)

DATE_KW = re.compile(
    r"(last updated|updated|reviewed on|last reviewed|mis à jour|mise à jour|actualisé|"
    r"aktualisiert|zuletzt|actualizado|actualización|aggiornato|aggiornamento|atualizado|"
    r"bijgewerkt|uppdaterad|zaktualizowano)", re.I)
MONTHS = (r"jan(uary|vier|uar|uary)?|feb(ruary|ruar)?|f[ée]v(rier)?|mar(ch|s|z)?|m[äa]rz|apr(il)?|"
          r"avr(il)?|may|mai|juin?|june?|juil(let)?|july?|aug(ust)?|ao[ûu]t|sep(t|tember|tembre)?|"
          r"oct(ober|obre)?|okt(ober)?|nov(ember|embre)?|d[ée]c(ember|embre)?|dez(ember)?|"
          r"enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|"
          r"gennaio|febbraio|aprile|maggio|giugno|luglio|settembre|ottobre|dicembre|"
          r"janeiro|fevereiro|março|maio|junho|julho|setembro|outubro|novembro|dezembro")
DATE_VALUE = re.compile(
    r"(\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b|\b(" + MONTHS + r")\.?\s+\d{1,2}(st|nd|rd|th)?,?\s+\d{4}\b|"
    r"\b\d{1,2}\.?\s+(" + MONTHS + r")\.?\s+\d{4}\b|\b(" + MONTHS + r")\.?\s+\d{4}\b)", re.I)
DISCLOSURE_KW = re.compile(
    r"(sponsored|sponsor|affiliate|affiliation|commission|advertiser disclosure|advertising disclosure|"
    r"paid placement|partner|compensat|we may earn|how we make money|no paid|pays? for|paid|"
    r"independent|indépendan|unabhängig|independiente|indipendent|"
    r"sponsoris|partenaire|rémunér|publicité|annonce|"
    r"gesponsert|werbung|provision|anzeige|"
    r"patrocinad|afiliad|publicidad|patrocinio|"
    r"sponsorizzat|affiliazion|pubblicit|"
    r"parceir|patrocinado)", re.I)
FAQ_HEADING = re.compile(
    r"(\bfaq|frequently asked|questions fréquentes|questions frequentes|foire aux questions|"
    r"häufige fragen|haufige fragen|preguntas frecuentes|domande frequenti|perguntas frequentes|"
    r"veelgestelde vragen)", re.I)


def fetch(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
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
        m = re.search(r"charset=([\w-]+)", resp.headers.get("Content-Type", ""), re.I)
        charset = m.group(1) if m else "utf-8"
        try:
            return resp.geturl(), raw.decode(charset, "replace")
        except LookupError:
            return resp.geturl(), raw.decode("utf-8", "replace")


class HubParser(HTMLParser):
    """One pass: visible text with offsets, headings, links, tables, summaries, JSON-LD, head tags."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []          # visible text chunks
        self.length = 0          # running length of the visible text
        self.skip = 0            # depth inside SKIP_TAGS
        self.title = ""
        self.in_title = False
        self.canonical = ""
        self.og_url = ""
        self.headings = []       # dicts: level, text, start, end
        self.cur_heading = None
        self.links = []          # dicts: href, rel, offset
        self.tables = []         # dicts: rows_td (rows with a td), rows_all
        self.table_stack = []
        self.row_has_td = False
        self.summaries = []      # summary texts
        self.cur_summary = None
        self.jsonld = []         # raw strings
        self.in_jsonld = False
        self.jsonld_buf = []
        self.time_offsets = []   # offsets of <time> elements

    def _emit(self, text):
        # Whitespace collapsed as it is emitted, so offsets count visible characters only.
        text = re.sub(r"\s+", " ", text)
        if self.parts and self.parts[-1].endswith(" ") and text.startswith(" "):
            text = text[1:]
        if not text:
            return
        self.parts.append(text)
        self.length += len(text)
        if self.cur_heading is not None:
            self.cur_heading["buf"].append(text)
        if self.cur_summary is not None:
            self.cur_summary.append(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script":
            if (a.get("type") or "").lower().strip() == "application/ld+json":
                self.in_jsonld = True
                self.jsonld_buf = []
            self.skip += 1
            return
        if tag == "title" and not self.title:
            self.in_title = True
        if tag == "link" and "canonical" in (a.get("rel") or "").lower():
            self.canonical = a.get("href") or ""
        if tag == "meta" and (a.get("property") or "").lower() == "og:url":
            self.og_url = a.get("content") or ""
        if tag in SKIP_TAGS and tag != "head":
            if tag not in VOID_TAGS:
                self.skip += 1
            return
        if self.skip:
            return
        if tag in BLOCK_TAGS:
            self._emit(" ")
        if tag in HEADINGS:
            self.cur_heading = {"level": int(tag[1]), "start": self.length, "buf": []}
        elif tag == "a":
            self.links.append({"href": a.get("href") or "", "rel": (a.get("rel") or "").lower(),
                               "offset": self.length})
        elif tag == "table":
            self.table_stack.append({"rows_td": 0, "rows_all": 0})
        elif tag == "tr" and self.table_stack:
            self.table_stack[-1]["rows_all"] += 1
            self.row_has_td = False
        elif tag == "td" and self.table_stack and not self.row_has_td:
            self.row_has_td = True
            self.table_stack[-1]["rows_td"] += 1
        elif tag == "summary":
            self.cur_summary = []
        elif tag == "time":
            self.time_offsets.append(self.length)

    def handle_endtag(self, tag):
        if tag == "script":
            if self.in_jsonld:
                self.jsonld.append("".join(self.jsonld_buf))
                self.in_jsonld = False
            self.skip = max(0, self.skip - 1)
            return
        if tag == "title":
            self.in_title = False
        if tag in SKIP_TAGS and tag != "head":
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in HEADINGS and self.cur_heading is not None:
            h = self.cur_heading
            h["text"] = " ".join("".join(h.pop("buf")).split())
            h["end"] = self.length
            self.headings.append(h)
            self.cur_heading = None
        elif tag == "table" and self.table_stack:
            self.tables.append(self.table_stack.pop())
        elif tag == "summary" and self.cur_summary is not None:
            self.summaries.append(" ".join("".join(self.cur_summary).split()))
            self.cur_summary = None
        if tag in BLOCK_TAGS:
            self._emit(" ")

    def handle_data(self, data):
        if self.in_jsonld:
            self.jsonld_buf.append(data)
            return
        if self.in_title:
            self.title += data
            return
        if self.skip:
            return
        self._emit(data)

    @property
    def text(self):
        return "".join(self.parts)


def norm(s):
    s = s.lower().replace("’", "'").replace(" ", " ")
    s = re.sub(r"[^\w\s']", " ", s)
    return " ".join(s.split())


def types_of(node):
    t = node.get("@type")
    if isinstance(t, list):
        return [str(x) for x in t]
    return [str(t)] if t else []


def walk(obj):
    """Every dict with an @type, nested anywhere (graphs, mainEntity, lists)."""
    if isinstance(obj, dict):
        if "@type" in obj:
            yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def count_in(text):
    """The item count stated in a heading or title: first integer that is not a year.

    Returns (number or None, exact flag)."""
    for m in NUMBER_RE.finditer(text):
        n = int(m.group(1))
        if 1900 <= n <= 2100 or n == 0:
            continue
        exact = not m.group(2) and not NOT_EXACT_BEFORE.search(text[:m.start()])
        return n, exact
    return None, True


def host_of(url):
    try:
        return urlparse(url).netloc.lower().replace("www.", "")
    except ValueError:
        return ""


def is_internal(href, host):
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return False
    if href.startswith("//"):
        href = "https:" + href
    if href.startswith(("http://", "https://")):
        return bool(host) and host_of(href) == host
    return True


def check(source, top_chars):
    findings = []

    def add(sev, code, detail):
        findings.append((sev, code, detail))

    if source.startswith(("http://", "https://")):
        final_url, html = fetch(source)
    else:
        with open(source, encoding="utf-8", errors="replace") as fh:
            html = fh.read()
        final_url = ""

    p = HubParser()
    p.feed(html)
    p.close()
    text = p.text
    host = host_of(final_url or p.canonical or p.og_url)

    # JSON-LD
    nodes = []
    invalid = 0
    for raw in p.jsonld:
        raw = raw.strip()
        if not raw:
            continue
        try:
            nodes.extend(walk(json.loads(raw)))
        except json.JSONDecodeError as exc:
            invalid += 1
            add("high", "jsonld_invalid", "a JSON-LD block does not parse ({}).".format(str(exc)[:80]))
    by_type = {}
    for n in nodes:
        for t in types_of(n):
            by_type.setdefault(t, []).append(n)

    # Headings and item headings
    h1s = [h for h in p.headings if h["level"] == 1]
    h1 = h1s[0] if h1s else None
    numbered = {}
    for h in p.headings:
        if h["level"] in (2, 3, 4):
            m = ITEM_HEADING_RE.match(h["text"]) or HASH_HEADING_RE.match(h["text"])
            if m and 1 <= int(m.group(1)) <= 500:
                numbered.setdefault(h["level"], []).append((int(m.group(1)), h))
    item_level = max(numbered, key=lambda lv: len(numbered[lv])) if numbered else None
    items = numbered.get(item_level, [])
    item_numbers = [n for n, _ in items]
    item_count = len(items)

    h1_count, h1_exact = count_in(h1["text"]) if h1 else (None, True)
    title_count, title_exact = count_in(p.title)

    # ItemList: the one whose names match the item headings best (a site may also mark up
    # its navigation as an ItemList), then the largest
    lists = by_type.get("ItemList", [])
    heading_text = norm(" ".join(h["text"] for _, h in items))

    def il_names(n):
        el = n.get("itemListElement") or []
        out = []
        for e in (el if isinstance(el, list) else [el]):
            if isinstance(e, dict):
                name = e.get("name")
                if not name and isinstance(e.get("item"), dict):
                    name = e["item"].get("name")
                if name:
                    out.append(norm(str(name)))
        return out

    def il_score(n):
        names = il_names(n)
        hits = sum(1 for x in names if x and " {} ".format(x) in " {} ".format(heading_text))
        return (hits, len(names))

    itemlist = max(lists, key=il_score) if lists else None
    unrelated_lists = 0
    if itemlist is not None and items and il_score(itemlist)[0] < max(1, min(len(items), il_score(itemlist)[1]) / 2):
        unrelated_lists = len(lists)  # navigation or other lists, none naming the ranked items
        itemlist = None
    il_elements = []
    il_declared = None
    if itemlist:
        el = itemlist.get("itemListElement") or []
        il_elements = el if isinstance(el, list) else [el]
        try:
            il_declared = int(itemlist.get("numberOfItems")) if itemlist.get("numberOfItems") is not None else None
        except (TypeError, ValueError):
            il_declared = None

    # Tables
    data_tables = [t for t in p.tables if t["rows_td"] > 0]
    biggest_table = max((t["rows_td"] for t in data_tables), default=0)

    # FAQ
    faq_nodes = by_type.get("FAQPage", [])
    faq_questions = []
    for f in faq_nodes:
        me = f.get("mainEntity") or []
        for q in (me if isinstance(me, list) else [me]):
            if isinstance(q, dict) and q.get("name"):
                faq_questions.append(str(q["name"]))
    faq_heads = [h for h in p.headings if h["level"] in (2, 3) and FAQ_HEADING.search(h["text"])]
    visible_q = list(p.summaries)
    if faq_heads:
        start = faq_heads[0]["end"]
        for h in p.headings:
            if h["start"] > start and h["level"] >= 2 and h["text"].rstrip().endswith("?"):
                visible_q.append(h["text"])
    visible_q = [q for q in dict.fromkeys(visible_q) if q.rstrip().endswith("?")]

    # ---------- findings ----------
    counts = {"H1": h1_count, "title": title_count, "numbered item headings": item_count or None,
              "ItemList numberOfItems": il_declared, "ItemList itemListElement": len(il_elements) or None}
    stated = {k: v for k, v in counts.items() if v is not None}
    if len(set(stated.values())) > 1:
        add("high", "count_mismatch", "item counts disagree: " +
            ", ".join("{} {}".format(k, v) for k, v in stated.items()) + ".")
    if h1 is None:
        add("high", "count_mismatch", "no H1 found, so the item count cannot be checked against it.")
    elif h1_count is None:
        add("medium", "h1_no_count", "the H1 states no item count: \"{}\".".format(h1["text"][:120]))
    elif not h1_exact:
        add("medium", "h1_count_not_exact", "the H1 count is approximate (\"+\", \"more than\"): state the exact number.")
    if title_count is not None and not title_exact:
        add("medium", "h1_count_not_exact", "the title count is approximate: \"{}\".".format(" ".join(p.title.split())[:120]))
    if not items:
        add("medium", "items_not_numbered", "no numbered item headings (h2 or h3 starting with \"1.\", \"1)\" or \"#1\").")
    elif item_numbers != list(range(1, item_count + 1)):
        add("medium", "numbering_gap", "item numbers are not 1 to {} in order (first ones: {}).".format(
            item_count, ", ".join(str(n) for n in item_numbers[:12])))

    if itemlist is None:
        add("high", "itemlist_missing", "no ItemList JSON-LD for the ranking{}.".format(
            " ({} ItemList(s) found, none naming most of the ranked items)".format(unrelated_lists) if unrelated_lists else ""))
    else:
        no_url = [e for e in il_elements if isinstance(e, dict) and not (e.get("url") or (isinstance(e.get("item"), dict) and e["item"].get("url")) or isinstance(e.get("item"), str))]
        if no_url:
            add("medium", "itemlist_no_url", "{} ListItem(s) without a url to the item page.".format(len(no_url)))
        if items and il_elements:
            wrong = []
            for (n, h), e in zip(items, sorted([e for e in il_elements if isinstance(e, dict)],
                                               key=lambda e: e.get("position") or 0)):
                name = e.get("name")
                if not name and isinstance(e.get("item"), dict):
                    name = e["item"].get("name")
                if name and norm(str(name)) not in norm(h["text"]):
                    wrong.append("#{} heading \"{}\" vs ListItem \"{}\"".format(n, h["text"][:40], str(name)[:40]))
            if wrong:
                add("medium", "itemlist_order_mismatch", "{} position(s) where the ItemList name is not in the heading, e.g. {}.".format(
                    len(wrong), "; ".join(wrong[:3])))

    ref_count = item_count or il_declared or len(il_elements) or h1_count
    if not data_tables:
        add("high", "table_missing", "no HTML <table> with data rows: the comparison is not extractable.")
    elif ref_count and biggest_table < ref_count:
        add("medium", "table_rows_mismatch", "the largest table has {} data rows for {} items.".format(biggest_table, ref_count))

    if not faq_nodes:
        if visible_q or faq_heads:
            add("medium", "faqpage_missing", "a visible FAQ ({} questions) without FAQPage JSON-LD.".format(len(visible_q)))
        else:
            add("medium", "faq_missing", "no FAQ section and no FAQPage JSON-LD.")
    else:
        ntext = norm(text)
        absent = [q for q in faq_questions if norm(q) not in ntext]
        if absent:
            add("high", "faq_jsonld_mismatch", "{} FAQPage question(s) not found in the visible text, e.g. \"{}\".".format(
                len(absent), absent[0][:100]))
        if visible_q and len(visible_q) != len(faq_questions):
            add("medium", "faq_count_mismatch", "{} visible FAQ questions vs {} in FAQPage.".format(len(visible_q), len(faq_questions)))
    if len(faq_nodes) > 1 or len(faq_heads) > 1:
        add("medium", "faq_duplicate", "{} FAQPage block(s) and {} FAQ heading(s): keep one FAQ per page.".format(
            len(faq_nodes), len(faq_heads)))

    if "BreadcrumbList" not in by_type:
        add("medium", "breadcrumb_missing", "no BreadcrumbList JSON-LD.")
    if not any("dateModified" in n for n in nodes):
        add("medium", "datemodified_missing", "no dateModified in the JSON-LD.")
    if "AggregateRating" in by_type or "Review" in by_type:
        add("low", "rating_markup_check", "Review or AggregateRating markup present: each rating must be produced by the publisher and shown on the page.")

    # Top zone: from a little above the H1 to top_chars after it
    anchor = h1["start"] if h1 else 0
    top_start = max(0, anchor - 2000)
    top = text[top_start:anchor + top_chars]
    date_ok = False
    for m in DATE_KW.finditer(top):
        if DATE_VALUE.search(top[m.end():m.end() + 80]):
            date_ok = True
            break
    if not date_ok and any(top_start <= o <= anchor + top_chars for o in p.time_offsets):
        date_ok = True
    if not date_ok:
        add("high", "date_missing", "no visible update date (\"Updated {date}\") near the H1.")
    dm = DISCLOSURE_KW.search(top)
    if not dm:
        add("high", "disclosure_missing", "no disclosure keyword (sponsored, affiliate, partner, paid placement...) near the H1.")

    dashes = len(DASH_RE.findall(text))
    if dashes:
        add("medium", "em_dashes", "{} em or en dash(es) in the visible text.".format(dashes))

    no_link = []
    for i, (n, h) in enumerate(items):
        end = items[i + 1][1]["start"] if i + 1 < len(items) else h["end"] + 4000
        if not any(h["start"] <= l["offset"] < end and is_internal(l["href"], host) for l in p.links):
            no_link.append(n)
    if no_link:
        add("medium", "item_no_link", "{} item card(s) with no internal link to the item page: #{}.".format(
            len(no_link), ", #".join(str(n) for n in no_link[:15])))

    sponsored = sum(1 for l in p.links if "sponsored" in l["rel"])
    facts = [
        ("title", " ".join(p.title.split())[:110] or "-"),
        ("H1", (h1["text"][:110] if h1 else "-")),
        ("count in H1 / title", "{} / {}".format(h1_count if h1_count is not None else "-", title_count if title_count is not None else "-")),
        ("numbered item headings", "{} (h{})".format(item_count, item_level) if items else "0"),
        ("ItemList numberOfItems / elements", "{} / {}".format(il_declared if il_declared is not None else "-", len(il_elements) if itemlist else "-")),
        ("tables with data rows (largest)", "{} ({})".format(len(data_tables), biggest_table)),
        ("FAQPage questions / visible FAQ questions", "{} / {}".format(len(faq_questions), len(visible_q))),
        ("JSON-LD types", ", ".join(sorted(by_type)) or "-"),
        ("links with rel sponsored", str(sponsored)),
        ("em or en dashes", str(dashes)),
    ]
    return final_url or source, facts, findings


def report(results):
    order = {"high": 0, "medium": 1, "low": 2}
    out = ["# Comparison hub check", ""]
    for src, facts, findings in results:
        out += ["## " + src, "", "| Fact | Value |", "|---|---|"]
        out += ["| {} | {} |".format(k, str(v).replace("|", "/")) for k, v in facts]
        out.append("")
        if findings:
            out += ["| Severity | Code | Detail |", "|---|---|---|"]
            for sev, code, detail in sorted(findings, key=lambda f: order[f[0]]):
                out.append("| {} | {} | {} |".format(sev, code, detail.replace("|", "/")))
        else:
            out.append("No finding.")
        highs = sum(1 for f in findings if f[0] == "high")
        out += ["", "Verdict: {} high, {} medium, {} low.".format(
            highs, sum(1 for f in findings if f[0] == "medium"), sum(1 for f in findings if f[0] == "low")), ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Check a comparison hub or best-X ranking page.")
    ap.add_argument("sources", nargs="+", help="URL(s) or saved .html file(s)")
    ap.add_argument("--top-chars", type=int, default=3000,
                    help="visible characters after the H1 searched for the date and the disclosure (default 3000; 2000 before the H1 are searched too)")
    args = ap.parse_args()
    results = []
    failed = False
    for src in args.sources:
        try:
            results.append(check(src, args.top_chars))
        except Exception as exc:  # network error, unreadable file
            results.append((src, [("error", str(exc)[:200])], [("high", "fetch_failed", str(exc)[:200])]))
    print(report(results))
    for _, _, findings in results:
        if any(f[0] == "high" for f in findings):
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
