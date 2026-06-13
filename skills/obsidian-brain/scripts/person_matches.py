#!/usr/bin/env python3
"""Find the same person stored as more than one note in an Obsidian vault.

The same human often ends up in several folders: a WhatsApp chat note, a CRM
card, a contacts export, an industry-figures list. This script normalizes every
note's basename (drops parenthetical suffixes, emoji, accents and case) and
reports basenames that appear in more than one folder, so they can be merged
into one note per person.

Two confidence tiers:
  - STRONG: names with two or more words (first + last). Safe to merge after a look.
  - WEAK:   single-word names (a bare first name). Review before merging; "Nico"
            in two folders may be two different people.

Pure Python standard library, read only. Emoji ranges are written as \\u escapes
so this file contains no emoji characters itself.

Usage:
  python3 person_matches.py <vault_dir>
"""

import os
import re
import sys
import unicodedata
from collections import defaultdict

SKIP_DIRS = {".obsidian", ".trash", ".git"}
PARENS = re.compile(r"\s*\([^)]*\)\s*")
EMOJI = re.compile(
    "[\\U0001F000-\\U0001FAFF\\u2600-\\u27BF\\U0001F1E6-\\U0001F1FF\\u2B00-\\u2BFF\\uFE0F]"
)
NONWORD = re.compile(r"[^a-z0-9]+")


def normalize(name):
    s = unicodedata.normalize("NFC", name)
    if s.lower().endswith(".md"):
        s = s[:-3]
    s = PARENS.sub(" ", s)
    s = EMOJI.sub("", s)
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = NONWORD.sub(" ", s.lower()).strip()
    return s


def main():
    if len(sys.argv) < 2:
        print("usage: python3 person_matches.py <vault_dir>")
        return 2
    vault = os.path.abspath(sys.argv[1])

    # normalized name -> { folder -> [real filenames] }
    groups = defaultdict(lambda: defaultdict(list))
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        folder = os.path.relpath(root, vault)
        for f in files:
            if not f.lower().endswith(".md"):
                continue
            n = normalize(f)
            if not n or n.replace(" ", "").isdigit():
                continue
            groups[n][folder].append(f)

    strong, weak = [], []
    for name, byfolder in groups.items():
        if len(byfolder) < 2:
            continue  # same name in one folder only is not a cross-folder duplicate
        paths = []
        for folder, names in sorted(byfolder.items()):
            for fn in names:
                paths.append(os.path.join(folder, fn))
        entry = (name, paths)
        (strong if " " in name else weak).append(entry)

    strong.sort()
    weak.sort()

    print("vault:", vault)
    print("likely duplicate people (same name, different folders):",
          len(strong) + len(weak))
    print()
    print("STRONG (multi-word names, safe to merge after a look):", len(strong))
    for name, paths in strong:
        print("  " + name)
        for p in paths:
            print("      " + p)
    print()
    print("WEAK (single-word names, review, may be different people):", len(weak))
    for name, paths in weak:
        print("  " + name + "  ::  " + "  |  ".join(paths))
    return 0


if __name__ == "__main__":
    sys.exit(main())
