#!/usr/bin/env python3
"""Check a YouTube video's metadata before publishing: description, chapters, title, thumbnail.

Stdlib only (Python 3.9+), no network, no API key.

Usage:
  python3 youtube_check.py --description description.txt --duration 3:58
  python3 youtube_check.py --title "Online ordering for bakeries: set it up in 4 minutes"
  python3 youtube_check.py --thumbnail thumb.jpg
  (the three can be combined in one call)

Checks:
  description  under 5000 characters, no < or >, no em or en dash, a link on the first line,
               own-site links carry utm_source and utm_medium (with --site example.com)
  chapters     start at 0:00, at least 3, ascending, each at least 10 s, start-and-end format
               consistent, end of the last chapter equal to --duration when given
  title        1 to 100 characters, no < or >, no em or en dash, not all capitals,
               warning above 70 characters (truncated in search on most screens)
  thumbnail    JPEG or PNG, under 2 MB, 16:9, at least 1280x720 recommended

Exit code: 0 clean, 1 at least one error. Warnings never fail the run.
"""

import argparse
import re
import struct
import sys
from pathlib import Path

DASHES = "\u2014\u2013"
TS = r"(?:\d{1,2}:)?\d{1,2}:\d{2}"
CHAPTER_RE = re.compile(rf"^\s*({TS})(?:\s*[-\u2013\u2014]\s*({TS}))?\s+(\S.*)$")
URL_RE = re.compile(r"https?://[^\s)]+")


def seconds(ts):
    parts = [int(p) for p in ts.split(":")]
    total = 0
    for p in parts:
        total = total * 60 + p
    return total


def fmt(s):
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"


def check_description(text, duration, site, errors, warnings):
    if len(text) > 5000:
        errors.append(f"description is {len(text)} characters (YouTube limit 5000)")
    if "<" in text or ">" in text:
        errors.append("description contains < or > (YouTube rejects them)")
    for n, line in enumerate(text.splitlines(), 1):
        if any(d in line for d in DASHES):
            errors.append(f"description line {n}: em or en dash")
    first = next((l for l in text.splitlines() if l.strip()), "")
    if not URL_RE.search(first):
        warnings.append("first line has no link (the offer line with its tracked link should open the description)")
    if site:
        for url in URL_RE.findall(text):
            if site in url and ("utm_source=" not in url or "utm_medium=" not in url):
                warnings.append(f"own-site link without utm_source and utm_medium: {url}")

    chapters = []
    for line in text.splitlines():
        m = CHAPTER_RE.match(line)
        if m:
            chapters.append((m.group(1), m.group(2), m.group(3).strip()))
    if not chapters:
        warnings.append("no chapters found (one per line, timestamp first)")
        return
    starts = [seconds(c[0]) for c in chapters]
    if starts[0] != 0:
        errors.append(f"first chapter starts at {chapters[0][0]}, must be 0:00")
    if len(chapters) < 3:
        errors.append(f"{len(chapters)} chapters, YouTube needs at least 3")
    with_end = [c for c in chapters if c[1]]
    if with_end and len(with_end) != len(chapters):
        errors.append("mixed chapter formats: either every line has start and end, or none")
    total = seconds(duration) if duration else None
    for i, (start, end, title) in enumerate(chapters):
        s = seconds(start)
        nxt = starts[i + 1] if i + 1 < len(starts) else (seconds(end) if end else total)
        if i + 1 < len(starts) and starts[i + 1] <= s:
            errors.append(f"chapter {i + 1} '{title}': next chapter does not start later")
        if nxt is not None and nxt - s < 10:
            errors.append(f"chapter {i + 1} '{title}': lasts {nxt - s} s, minimum 10 s")
        if end:
            e = seconds(end)
            if i + 1 < len(starts) and e != starts[i + 1]:
                errors.append(f"chapter {i + 1} '{title}': ends at {end} but the next starts at {fmt(starts[i + 1])}")
            if i + 1 == len(chapters) and total is not None and e != total:
                errors.append(f"last chapter ends at {end}, video lasts {fmt(total)}")
        words = len(title.split())
        if words > 7:
            warnings.append(f"chapter {i + 1} title has {words} words (aim for 2 to 5)")
    if total is not None and starts[-1] >= total:
        errors.append(f"last chapter starts at {fmt(starts[-1])}, after the end of the video")
    print(f"chapters: {len(chapters)} found")


def check_title(title, errors, warnings):
    n = len(title)
    if n == 0 or n > 100:
        errors.append(f"title is {n} characters (1 to 100 allowed)")
    elif n > 70:
        warnings.append(f"title is {n} characters, the end is cut in search on most screens (aim for 70 or less)")
    if "<" in title or ">" in title:
        errors.append("title contains < or >")
    if any(d in title for d in DASHES):
        errors.append("title contains an em or en dash")
    letters = [c for c in title if c.isalpha()]
    if len(letters) > 12 and sum(c.isupper() for c in letters) / len(letters) > 0.8:
        warnings.append("title is almost all capitals (keep capitals for one or two words at most)")
    print(f"title: {n} characters")


def image_size(path):
    data = Path(path).read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return "PNG", w, h, len(data)
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return "JPEG", w, h, len(data)
            i += 2 + seg_len
    return None, 0, 0, len(data)


def check_thumbnail(path, errors, warnings):
    kind, w, h, size = image_size(path)
    if kind is None:
        errors.append("thumbnail is not a JPEG or PNG")
        return
    if size >= 2 * 1024 * 1024:
        errors.append(f"thumbnail weighs {size / 1048576:.2f} MB (YouTube limit 2 MB)")
    if abs(w / h - 16 / 9) > 0.01:
        errors.append(f"thumbnail is {w}x{h}, not 16:9")
    if w < 1280:
        warnings.append(f"thumbnail is {w}x{h}, 1280x720 recommended")
    print(f"thumbnail: {kind} {w}x{h}, {size // 1024} KB")


def main():
    ap = argparse.ArgumentParser(description="Check YouTube metadata before publishing.")
    ap.add_argument("--description", help="text file with the description")
    ap.add_argument("--duration", help="total video duration, e.g. 3:58 or 1:12:05")
    ap.add_argument("--site", help="your own domain, to check UTM parameters on its links")
    ap.add_argument("--title", help="the video title")
    ap.add_argument("--thumbnail", help="the thumbnail image file")
    a = ap.parse_args()
    if not (a.description or a.title or a.thumbnail):
        ap.error("give at least one of --description, --title, --thumbnail")
    errors, warnings = [], []
    if a.description:
        text = Path(a.description).read_text(encoding="utf-8")
        check_description(text, a.duration, a.site, errors, warnings)
    if a.title is not None:
        check_title(a.title, errors, warnings)
    if a.thumbnail:
        check_thumbnail(a.thumbnail, errors, warnings)
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print("OK" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
