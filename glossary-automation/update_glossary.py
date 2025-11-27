"""
update_glossary.py

Automates merging of new glossary entries from 'new-terms.md' into 'glossary.md'.
- Assumes each entry is a single Markdown list line, like:
  - **Term:** Definition text here.

Behavior:
- Reads all existing entries from glossary.md.
- Reads all new entries from new-terms.md.
- Ignores blank lines and comment lines starting with '#'.
- Merges and deduplicates all entries (exact-string match).
- Sorts entries alphabetically by the visible term (case-insensitive).
- Writes the updated list back to glossary.md.
- Clears new-terms.md after processing so you can reuse it daily.

Part of the Glossary Automation workflow for Thinking Like A Village.
"""

import os
import re
from typing import List, Set


GLOSSARY_FILE = "glossary.md"
NEW_TERMS_FILE = "new-terms.md"


def load_entries(path: str) -> List[str]:
    """Load non-empty, non-comment lines from a Markdown file."""
    if not os.path.exists(path):
        return []

    entries: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.rstrip("\n")
            if not stripped:
                continue  # skip blank lines
            if stripped.lstrip().startswith("#"):
                # ignore headings or comment lines that start with '#'
                continue
            entries.append(stripped)
    return entries


def extract_term(entry_line: str) -> str:
    """
    Extract the term from a line formatted like:
    - **Term:** Definition
    Returns 'Term' for sorting.
    Falls back to the full line if pattern not found.
    """
    # Match pattern: - **Term:** ...
    pattern = r"-\s*\*\*(.+?)\*\*:"
    match = re.search(pattern, entry_line)
    if match:
        return match.group(1).strip()
    # Fallback: use the whole line
    return entry_line.strip()


def merge_and_sort(existing: List[str], new: List[str]) -> List[str]:
    """
    Merge two lists of entries:
    - Remove exact duplicates.
    - Sort by extracted term, case-insensitive.
    """
    # Use a set to deduplicate on the full line
    all_entries_set: Set[str] = set(existing)
    for line in new:
        if line not in all_entries_set:
            all_entries_set.add(line)

    # Convert back to list for sorting
    all_entries: List[str] = list(all_entries_set)

    # Sort entries by extracted term, case-insensitive
    all_entries.sort(key=lambda line: extract_term(line).casefold())
    return all_entries


def write_entries(path: str, entries: List[str]) -> None:
    """Write entries back to a Markdown file, one per line, with trailing newline."""
    with open(path, "w", encoding="utf-8") as f:
        for line in entries:
            f.write(line + "\n")


def clear_file(path: str) -> None:
    """Empty the contents of a file if it exists."""
    if os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("")


def main() -> None:
    # Load existing glossary entries
    existing_entries = load_entries(GLOSSARY_FILE)

    # Load new entries
    new_entries = load_entries(NEW_TERMS_FILE)

    if not new_entries:
        print("No new entries found in new-terms.md. Nothing to update.")
        return

    # Merge, deduplicate, and sort
    updated_entries = merge_and_sort(existing_entries, new_entries)

    # Write updated glossary
    write_entries(GLOSSARY_FILE, updated_entries)
    print(f"Updated {GLOSSARY_FILE} with {len(new_entries)} new entries.")

    # Clear new-terms.md so you can paste fresh ones next time
    clear_file(NEW_TERMS_FILE)
    print(f"Cleared {NEW_TERMS_FILE} after processing.")


if __name__ == "__main__":
    main()
