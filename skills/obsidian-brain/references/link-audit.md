# Link audit (reference)

Load this when checking a vault's health, after a big import, or when the user reports a messy or hard-to-navigate vault. Two bundled scripts in `scripts/` do the scanning; this file explains how to run them and what to do with the output. Both are pure Python standard library, read only, and never modify the vault.

## Why audit

A vault decays as it grows. Renamed notes leave broken wikilinks. Imports land notes that nothing links to (orphans). The same person arrives as a chat note and a CRM card (duplicates). Notes drift out of reach of the index. None of this is visible by eye in a vault of hundreds of notes, but each one is a fact the agent can no longer find. The audit makes decay measurable, so it can be fixed in one pass instead of discovered one broken link at a time.

Target state: zero broken links, zero orphans, zero notes unreachable from the entry point. Duplicate basenames are reviewed by hand (some, like README files, are legitimate).

## link_graph.py

```
python3 scripts/link_graph.py <vault_dir> [entry_point.md] [--out <dir>]
```

It parses every wikilink and relative markdown link in the vault, resolves each against the actual files (handling full paths, bare basenames, and macOS NFC and NFD differences), walks the graph from the entry point, and reports:

| Metric | Meaning | Healthy value |
|---|---|---|
| broken links | a link whose target file does not exist | 0 |
| ambiguous links | a bare name that matches files in two folders | low; make them path-qualified |
| orphans | a note with no inbound link | 0 |
| unreachable from entry point | a note you cannot reach by following links from the top | 0 |
| duplicate basenames | the same filename in more than one folder | review each |

Without `--out` it prints a capped summary. With `--out <dir>` it writes four TSV files (`broken_links.tsv`, `orphans.tsv`, `unreachable.tsv`, `duplicate_basenames.tsv`) for the full lists. If the entry point is not one of `00-INDEX.md`, `_INDEX.md`, `INDEX.md`, `index.md`, pass it as the second argument.

## person_matches.py

```
python3 scripts/person_matches.py <vault_dir>
```

It normalizes every note's basename (drops parenthetical suffixes, emoji, accents, case) and reports names that appear in more than one folder, in two tiers:

- **STRONG**: multi-word names (first plus last). Almost always the same person in two places (chat plus CRM). Safe to merge after a glance.
- **WEAK**: single-word names (a bare first name). Review before merging; the same first name in two folders can be two different people.

## Fix playbook

Run the scripts, then work the output in this order. Every fix is a vault edit, so do them deliberately and re-run the audit after.

1. **Broken links.** For each, decide whether the link is wrong or the target is missing. If the target was renamed or moved, update the link to the new path. If the target never existed (a link to a note you meant to write), either create the note or remove the link. If it points at a non-vault file (an external CSV, a deleted export), replace the wikilink with plain text so it stops reading as a broken link.
2. **Orphans and unreachable.** Same root cause: nothing links to the note, or nothing on a path from the entry point does. Add the note to its domain hub (one line, a wikilink and a purpose) and give the note at least one outbound `related` link. After this, orphans and unreachable both drop to zero.
3. **Duplicate people (STRONG tier).** Merge into one note per person. Pick the canonical home (usually the CRM card, since the relationship and status live there), append the other note's content as a dated section, update every link that pointed at the old note, then delete the old note. Re-run `person_matches.py` to confirm the pair is gone.
4. **Duplicate people (WEAK tier) and other duplicate basenames.** Look at each by hand. Two different people who share a first name stay separate (qualify their titles so they stop colliding). A genuine duplicate gets merged like the strong tier. Legitimate same-name files (README, _MOC) are left alone.
5. **Ambiguous links.** A bare `[[Name]]` that matches two folders is a coin flip for the agent. Make it path-qualified: `[[crm/Name|Name]]`.
6. **Filename hazards.** While fixing, rename any file whose name carries `#`, `[`, `]` or a trailing space (these break wikilinks), and update the links that pointed at it.

## Cadence

Run the audit after any large import and whenever the user asks why something cannot be found. Record it as an action-log entry (date, what was scanned, counts before and after) so the vault's health is itself part of the vault's memory.
