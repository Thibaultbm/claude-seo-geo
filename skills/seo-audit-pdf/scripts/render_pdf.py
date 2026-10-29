#!/usr/bin/env python3
"""Render an audit report (HTML) to PDF with headless Chrome, then lint it.

Usage:
  python3 render_pdf.py report.html "Audit SEO GEO example.com.pdf" [--png] [--allow "2 mois"]

The lint fails (exit code 1) on:
  - an em dash or an en dash anywhere in the text
  - a schedule or delay word (week, month, day, timeline, deadline, and the French
    equivalents): the report never says when or how long, the order is the plan
  - spaced thousands before a currency ("3 000 €"): amounts are written compact (3000€)
--allow takes a phrase that is a measured fact, not a delay ("en 2 mois" in a case study).
--png writes one image per page (needs pdftoppm, from poppler) for the visual check.

Standard library only. Chrome or Chromium must be installed.
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome",
]

FORBIDDEN = [
    (r"[—–]", "dash character (use a comma, a colon or parentheses)"),
    (r"\b(semaines?|mois|(?<!à )jours?|trimestres?|délais?|échéances?|échéancier|calendrier|planning|rétroplanning|deadline)\b",
     "schedule or delay word (French)"),
    (r"\b(weeks?|months?|days?|quarters?|timeline|deadline|schedule|sprints?)\b", "schedule or delay word (English)"),
    (r"\bJ\s?\+\s?\d+|\bQ[1-4]\b|\bS\d{1,2}\b|\bM\+?\d\b", "date shorthand (J+7, Q1, S2, M2)"),
    (r">\s*(Quand|When|Délai|Timeline|Durée|Duration)\s*<", "a When or Timeline column"),
    (r"\d \d{3}(?:[ ,.]\d+)? ?(€|euros?|\$|dollars?)", "spaced thousands before a currency (write 3000€)"),
]


def find_chrome():
    for c in CHROME_CANDIDATES:
        path = c if os.path.isabs(c) else shutil.which(c)
        if path and os.path.exists(path):
            return path
    sys.exit("Chrome or Chromium not found. Install Google Chrome.")


def visible_text(src):
    """Text a reader sees: drop <head>, <style>, <script> and HTML comments."""
    src = re.sub(r"(?is)<!--.*?-->", " ", src)
    src = re.sub(r"(?is)<(head|style|script)\b.*?</\1>", " ", src)
    return src


def lint(src, allow):
    text = visible_text(src)
    for phrase in allow:
        text = text.replace(phrase, " ")
    plain = html.unescape(re.sub(r"<[^>]+>", " ", text))
    problems = []
    for pattern, label in FORBIDDEN:
        hay = text if "column" in label else plain
        for m in re.finditer(pattern, hay, flags=re.I):
            start = max(0, m.start() - 45)
            context = re.sub(r"\s+", " ", hay[start:m.end() + 45]).strip()
            problems.append(f"  - {label}: '{m.group(0).strip()}' in \"...{context}...\"")
    return problems


def render(chrome, src_html, out_pdf):
    with tempfile.TemporaryDirectory() as profile:
        cmd = [chrome, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
               f"--user-data-dir={profile}", "--no-pdf-header-footer", "--virtual-time-budget=8000",
               f"--print-to-pdf={out_pdf}", "file://" + os.path.abspath(src_html)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    if not os.path.exists(out_pdf) or os.path.getsize(out_pdf) < 1000:
        sys.exit("PDF was not produced.")


def page_count(pdf):
    if shutil.which("pdfinfo"):
        out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        m = re.search(r"Pages:\s+(\d+)", out)
        if m:
            return int(m.group(1))
    with open(pdf, "rb") as f:
        return len(re.findall(rb"/Type\s*/Page[^s]", f.read()))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("pdf")
    ap.add_argument("--png", action="store_true", help="write one PNG per page for the visual check")
    ap.add_argument("--allow", action="append", default=[], help="phrase that is a measured fact, not a delay")
    args = ap.parse_args()

    src = open(args.html, encoding="utf-8").read()
    problems = lint(src, args.allow)

    render(find_chrome(), args.html, args.pdf)
    pages = page_count(args.pdf)
    print(f"PDF: {args.pdf} ({pages} pages, {os.path.getsize(args.pdf) // 1024} KB)")

    if args.png:
        if not shutil.which("pdftoppm"):
            print("pdftoppm not found (brew install poppler): skipping page images")
        else:
            prefix = os.path.splitext(args.pdf)[0] + "-page"
            subprocess.run(["pdftoppm", "-png", "-r", "70", args.pdf, prefix], check=True)
            print(f"Page images: {prefix}-*.png  (check every page: no block cut, no lonely heading)")

    if problems:
        print(f"\nLINT FAILED, {len(problems)} problem(s):")
        print("\n".join(problems))
        return 1
    print("Lint OK: no dash, no schedule or delay word, compact amounts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
