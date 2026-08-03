#!/usr/bin/env python3
"""Audit an Obsidian vault's link graph.

Reports, from the entry point down:
  - broken links     wikilinks or relative markdown links with no target file
  - orphan notes     notes with zero inbound links
  - unreachable      notes not reachable by following links from the entry point
  - duplicate names  the same basename in more than one folder (often one person twice)

A healthy vault returns zero broken, zero orphan, zero unreachable. Duplicate
names are reviewed by hand (some are legitimate, like README files).

Pure Python standard library, no dependencies, read only (never writes to the vault).

Usage:
  python3 link_graph.py <vault_dir> [entry_point.md] [--out <dir>]

If the entry point is omitted, the script looks for one of these at the vault
root, in order: 00-INDEX.md, _INDEX.md, INDEX.md, index.md.
With --out, the four lists are written as TSV files in <dir>; otherwise a capped
summary is printed to stdout.
"""

import os
import re
import sys
import unicodedata
import urllib.parse
from collections import defaultdict, deque

SKIP_DIRS = {".obsidian", ".trash", ".git"}
ENTRY_CANDIDATES = ["00-INDEX.md", "_INDEX.md", "INDEX.md", "index.md"]
WIKILINK = re.compile(r"(!?)\[\[([^\[\]]+?)\]\]")
MDLINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CODEBLOCK = re.compile(r"```.*?```", re.S)
INLINECODE = re.compile(r"`[^`\n]*`")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def collect(vault):
    """Return (all_files, md_files), both vault-relative and NFC-normalized.

    Wikilinks can point at any file in the vault (notes and attachments like
    .csv, .png, .pdf), so attachments are indexed as valid targets too. Only the
    .md notes form the navigation graph (inbound counts, orphans, reachability).
    """
    all_files, md_files = [], []
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f == ".DS_Store":
                continue
            rel = nfc(os.path.relpath(os.path.join(root, f), vault))
            all_files.append(rel)
            if rel.lower().endswith(".md"):
                md_files.append(rel)
    return sorted(all_files), sorted(md_files)


def build_indexes(all_files, md_files):
    by_base_ext = defaultdict(list)  # basename WITH extension (lower) -> [any paths]
    by_path = {}                     # full path (lower) -> real path, any file
    for f in all_files:
        by_base_ext[os.path.basename(f).lower()].append(f)
        by_path[f.lower()] = f
    by_base_md = defaultdict(list)   # md basename WITHOUT .md (lower) -> [md paths]
    path_noext_md = {}               # md full path WITHOUT .md (lower) -> real path
    for f in md_files:
        by_base_md[os.path.basename(f)[:-3].lower()].append(f)
        path_noext_md[f[:-3].lower()] = f
    return by_base_ext, by_path, by_base_md, path_noext_md


def resolve(raw, src, idx):
    by_base_ext, by_path, by_base_md, path_noext_md = idx
    t = nfc(raw).strip().split("#")[0]
    t = re.split(r"\\\||\|", t)[0].strip().strip("/")
    if not t:
        return ("self", None)
    tl = t.lower()
    tl_noext = tl[:-3] if tl.endswith(".md") else tl
    if "/" in t:
        if tl in by_path:                       # exact path to any file (attachment or .md)
            return ("ok", by_path[tl])
        if tl_noext in path_noext_md:           # path to a note, .md omitted
            return ("ok", path_noext_md[tl_noext])
        srcdir = os.path.dirname(src).lower()
        for cand in (tl, tl_noext):
            full = os.path.normpath(os.path.join(srcdir, cand)).replace("\\", "/")
            if full in by_path:
                return ("ok", by_path[full])
            if full in path_noext_md:
                return ("ok", path_noext_md[full])
        suffix = [p for p in path_noext_md.values() if p.lower()[:-3].endswith("/" + tl_noext)]
        if len(suffix) == 1:
            return ("ok", suffix[0])
        if len(suffix) > 1:
            return ("ambiguous", suffix[0])
        base = tl.split("/")[-1]
        if base in by_base_ext:
            lst = by_base_ext[base]
            return ("ok" if len(lst) == 1 else "ambiguous", lst[0])
        base_noext = base[:-3] if base.endswith(".md") else base
        if base_noext in by_base_md:
            lst = by_base_md[base_noext]
            return ("ok" if len(lst) == 1 else "ambiguous", lst[0])
        return ("broken", None)
    if tl in by_base_ext:                        # bare name with extension (image.png, data.csv)
        lst = by_base_ext[tl]
        return ("ok" if len(lst) == 1 else "ambiguous", lst[0])
    if tl_noext in by_base_md:                   # bare note name
        lst = by_base_md[tl_noext]
        return ("ok" if len(lst) == 1 else "ambiguous", lst[0])
    return ("broken", None)


def main():
    argv = sys.argv[1:]
    out_dir = None
    if "--out" in argv:
        i = argv.index("--out")
        out_dir = argv[i + 1] if i + 1 < len(argv) else "."
        del argv[i:i + 2]
    args = argv
    if not args:
        print("usage: python3 link_graph.py <vault_dir> [entry_point.md] [--out <dir>]")
        return 2
    vault = os.path.abspath(args[0])
    all_files, md_files = collect(vault)
    if not md_files:
        print("no .md files found under", vault)
        return 2
    md_set = set(md_files)
    idx = build_indexes(all_files, md_files)

    # NFC-normalize: macOS tab-completion hands over NFD, the index is NFC.
    entry = nfc(args[1]) if len(args) > 1 else None
    if entry is None:
        for cand in ENTRY_CANDIDATES:
            if cand in md_set:
                entry = cand
                break
    if entry is None or entry not in md_set:
        print("entry point not found; pass it explicitly as the second argument")
        print("looked for:", ", ".join(ENTRY_CANDIDATES))
        return 2

    out_edges = defaultdict(set)
    inbound = defaultdict(int)
    broken, ambiguous = [], []
    for f in md_files:
        try:
            text = open(os.path.join(vault, f), encoding="utf-8").read()
        except OSError:
            continue
        text = INLINECODE.sub("", CODEBLOCK.sub("", text))
        targets = set(m.group(2) for m in WIKILINK.finditer(text))
        for m in MDLINK.finditer(text):
            url = m.group(1)
            if re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I) or url.startswith("#"):
                continue
            targets.add(urllib.parse.unquote(url))
        for raw in targets:
            status, res = resolve(raw, f, idx)
            if status == "self":
                continue
            if status == "broken":
                broken.append((f, raw.strip()))
            else:
                if status == "ambiguous":
                    ambiguous.append((f, raw.strip()))
                out_edges[f].add(res)
                if res != f:
                    inbound[res] += 1

    reachable = {entry}
    q = deque([entry])
    while q:
        for nxt in out_edges.get(q.popleft(), ()):
            if nxt not in reachable and nxt in md_set:
                reachable.add(nxt)
                q.append(nxt)

    orphans = [f for f in md_files if inbound.get(f, 0) == 0 and f != entry]
    unreachable = [f for f in md_files if f not in reachable]
    by_base_md = idx[2]
    dups = {k: v for k, v in by_base_md.items() if len(v) > 1}

    print("vault:", vault)
    print("entry point:", entry)
    print("notes:", len(md_files))
    print("broken links:", len(broken))
    print("ambiguous links:", len(ambiguous))
    print("orphans (no inbound link):", len(orphans))
    print("unreachable from entry point:", len(unreachable))
    print("duplicate basenames:", len(dups))

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

        def dump(name, header, rows):
            with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
                fh.write(header + "\n")
                for r in rows:
                    fh.write("\t".join(str(x) for x in r) + "\n")

        dump("broken_links.tsv", "source\tmissing_target", sorted(broken))
        dump("orphans.tsv", "orphan_note", [(f,) for f in sorted(orphans)])
        dump("unreachable.tsv", "unreachable_note", [(f,) for f in sorted(unreachable)])
        dump("duplicate_basenames.tsv", "basename\tfiles",
             sorted((k, " | ".join(v)) for k, v in dups.items()))
        print("wrote 4 TSV files to", os.path.abspath(out_dir))
    else:
        def show(title, rows, cap=40):
            if not rows:
                return
            print("\n" + title)
            for r in rows[:cap]:
                print("  " + (r if isinstance(r, str) else "  ".join(r)))
            if len(rows) > cap:
                print("  ... and", len(rows) - cap, "more (use --out for the full list)")

        show("broken links (source -> missing target):", [f"{s}  ->  {t}" for s, t in sorted(broken)])
        show("orphans (no inbound link):", sorted(orphans))
        show("unreachable from entry point:", sorted(unreachable))
    return 0


if __name__ == "__main__":
    sys.exit(main())
