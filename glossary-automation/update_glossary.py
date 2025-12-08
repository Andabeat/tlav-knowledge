"""
update_glossary.py

Automates merging of new glossary entries from 'new-terms.md' into 'glossary.md'.

Assumptions about glossary.md:
- At the top, there is a header/introduction section (e.g. metadata) that should be preserved exactly.
- After the header, each glossary entry is exactly one line in this format:

    **Term:** Definition text here.

- There is a blank line between entries.
- No leading '-' bullet is required.

Behavior:
- Preserves the header/introduction section exactly.
- Treats any non-empty line starting with '**' as an entry line.
- Reads existing entries from glossary.md.
- Reads new entries from new-terms.md (same one-line '**Term:** Definition' format).
- Ignores blank lines and comment lines starting with '#'.
- Merges and deduplicates entries (exact-string match on the full line).
- Sorts entries alphabetically by the visible term (case-insensitive).
- Writes header + sorted entries back to glossary.md, with one blank line between entries.
- Clears new-terms.md after processing so you can reuse it daily.
"""

import os
import re
from typing import List, Set, Tuple


GLOSSARY_FILE = "glossary.md"
NEW_TERMS_FILE = "new-terms.md"


def split_header_and_entries(path: str) -> Tuple[List[str], List[str]]:
    """
    Split glossary.md into:
    - header_lines: everything up to (but not including) the first entry line starting with '**'.
    - entry_lines: all subsequent entry lines that start with '**', ignoring blanks and comments.
    """
    if not os.path.exists(path):
        return [], []

    header_lines: List[str] = []
    entry_lines: List[str] = []

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_entries = False
    for raw in lines:
        line = raw.rstrip("\n")

        if not in_entries:
            # Detect first entry line: starts with '**'
            if line.lstrip().startswith("**"):
                in_entries = True
                if line.strip():
                    entry_lines.append(line.strip())
            else:
                header_lines.append(line)
        else:
            # We are in the entries section
            stripped = line.strip()
            if not stripped:
                # skip blank lines between entries; we reinsert later
                continue
            if stripped.startswith("#"):
                # treat any comment/heading inside entries as non-entry
                header_lines.append(line)
                continue
            if stripped.startswith("**"):
                entry_lines.append(stripped)
            else:
                # If a non-entry line appears after entries start, keep it in header to be safe
                header_lines.append(line)

    return header_lines, entry_lines


def load_new_entries(path: str) -> List[str]:
    """
    Load non-empty, non-comment lines from new-terms.md.
    Expects each new entry as one line starting with '**Term:** Definition'.
    """
    if not os.path.exists(path):
        return []

    entries: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                continue
            entries.append(stripped)
    return entries


def extract_term(entry_line: str) -> str:
    """
    Extract the term from a line formatted like:
        **Term:** Definition
    Returns 'Term' for sorting.
    Falls back to the full line if pattern not found.
    """
    pattern = r"\*\*(.+?)\*\*:"
    match = re.search(pattern, entry_line)
    if match:
        return match.group(1).strip()
    return entry_line.strip()


def merge_and_sort(existing: List[str], new: List[str]) -> List[str]:
    """
    Merge two lists of entries:
    - Remove exact duplicates (full-line match).
    - Sort by extracted term, case-insensitive.
    """
    all_entries_set: Set[str] = set(existing)
    for line in new:
        if line not in all_entries_set:
            all_entries_set.add(line)

    all_entries: List[str] = list(all_entries_set)
    all_entries.sort(key=lambda line: extract_term(line).casefold())
    return all_entries


def write_glossary(path: str, header: List[str], entries: List[str]) -> None:
    """
    Write header + entries back to glossary.md.

    - Header preserved exactly as read (including blank lines).
    - Ensures a blank line between the header and the first entry.
    - Writes each entry on its own line followed by a blank line.
    """
    with open(path, "w", encoding="utf-8") as f:
        # Write header as-is
        for line in header:
            f.write(line + "\n")

        # Ensure at least one blank line between header and entries if there are entries
        if entries:
            if not header or header[-1].strip() != "":
                f.write("\n")

        # Write entries with a blank line between each
        for i, entry in enumerate(entries):
            f.write(entry + "\n")
            if i != len(entries) - 1:
                f.write("\n")  # blank line between entries


def clear_file(path: str) -> None:
    """Empty the contents of a file if it exists."""
    if os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("")


def main() -> None:
    # Split existing glossary into header and existing entries
    header_lines, existing_entries = split_header_and_entries(GLOSSARY_FILE)

    # Load new entries from new-terms.md
    new_entries = load_new_entries(NEW_TERMS_FILE)

    if not new_entries:
        print("No new entries found in new-terms.md. Nothing to update.")
        return

    # Merge, deduplicate, and sort entries
    updated_entries = merge_and_sort(existing_entries, new_entries)

    # Write updated glossary while preserving header and blank-line spacing
    write_glossary(GLOSSARY_FILE, header_lines, updated_entries)
    print(f"Updated {GLOSSARY_FILE} with {len(new_entries)} new entries (merged and sorted).")

    # Clear new-terms.md so you can paste fresh ones next time
    clear_file(NEW_TERMS_FILE)
    print(f"Cleared {NEW_TERMS_FILE} after processing.")


if __name__ == "__main__":
    main()
