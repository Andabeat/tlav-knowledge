***

# TLAV Knowledge

This repository hosts knowledge assets and automation for the **Thinking Like A Village (TLAV)** project. It currently focuses on maintaining a clean, alphabetized glossary of key concepts used across TLAV writing and teaching.

The repo is designed as a working knowledge base that can grow over time, starting with a robust glossary workflow and later expanding to other notes, datasets, or teaching materials.[1]

***

## Repository structure

Current key folders and files:

- `glossary-automation/`  
  Self-contained automation for the TLAV glossary, including:
  - `glossary.md` – the master TLAV glossary in Markdown, with one entry per concept.
  - `new-terms.md` – a staging file for new entries generated from recent blog posts or course materials.
  - `update_glossary.py` – a Python script that merges, deduplicates, and alphabetizes glossary entries while preserving a human-readable format.

- `.github/workflows/update-glossary.yml`  
  GitHub Actions workflow that can run `update_glossary.py` automatically whenever `new-terms.md` changes (optional if you prefer to run the script locally).

Additional top-level files and folders may be added over time as the TLAV knowledge base expands.

***

## TLAV glossary workflow (high level)

The glossary process is designed to minimize manual friction while keeping the final document clear and human-edited:

1. **Extract terms**  
   - An AI assistant (e.g., Comet / Perplexity) reads new TLAV blog posts or draft materials and proposes glossary entries.
   - Entries are formatted as one-line Markdown records in the form:  
     `**Term:** Definition`  
     with a blank line between entries.

2. **Stage new entries**  
   - These entries are pasted into `glossary-automation/new-terms.md` in the local clone of the repository.

3. **Merge and sort**  
   There are two options:
   - **Local script run (recommended while developing):**
     - From `glossary-automation`, run `python3 update_glossary.py`.
     - This:
       - Preserves the header/metadata at the top of `glossary.md`.
       - Merges in `new-terms.md`, removes exact duplicates, and sorts all entries alphabetically by term (case-insensitive).[2][3]
       - Rewrites `glossary.md` with one blank line between entries.
       - Clears `new-terms.md` so it’s ready for the next batch.
   - **Remote automation via GitHub Actions (optional):**
     - Commit and push changes to `glossary-automation/new-terms.md`.
     - The `update-glossary` workflow in `.github/workflows` runs the same script on GitHub’s servers and commits the updated `glossary.md` back to the repo.[4][5]

4. **Commit and push**  
   - After a local run, commit and push `glossary-automation/glossary.md` (and the cleared `new-terms.md`) to keep the remote copy in sync.

***

## Running the glossary update locally

Prerequisites:

- Python 3 installed and available as `python3` on your system.[6][7]
- A local clone of this repository.

Steps:

```bash
# From the repo root
cd glossary-automation

# Run the merge + sort script
python3 update_glossary.py

# Go back to the repo root and commit the changes
cd ..
git add glossary-automation/glossary.md glossary-automation/new-terms.md
git commit -m "Update glossary with new terms"
git push origin main
```

After this, the master glossary on GitHub will reflect the new terms and sorted order.

***

## Future directions

The `tlav-knowledge` repo can eventually include:

- Additional curated glossaries (e.g., thematic glossaries for specific courses).
- Syllabi, reading lists, and teaching materials linked to glossary terms.
- Notebooks or scripts for analyzing TLAV content (e.g., keyword clustering, topic modeling).
- Documentation for how others can adapt this automation pattern for their own knowledge projects.

For now, the focus is on building a reliable, low-friction glossary pipeline that supports ongoing TLAV writing and community learning.

[1](https://github.com/Andabeat/tlav-knowledge)
[2](https://www.geeksforgeeks.org/python/python-ways-to-sort-list-of-strings-in-case-insensitive-manner/)
[3](https://stackoverflow.com/questions/13954841/sort-list-of-strings-ignoring-upper-lower-case)
[4](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
[5](https://docs.github.com/actions/managing-workflow-runs/viewing-workflow-run-history)
[6](https://docs.python.org/3/reference/lexical_analysis.html)
[7](https://www.w3schools.com/python/ref_string_casefold.asp)
[8](https://www.utpteachingculture.com/teaching-theory/glossary-of-theory-terms/)
[9](http://www.openanthropology.org/ANS110/glossary.html)
[10](https://anthrodendum.org/2023/12/24/anthropology-blog-resurvey-project-3-the-blogroll/)
[11](https://socialsci.libretexts.org/Bookshelves/Anthropology/Cultural_Anthropology/Cultural_Anthropology_(Wikibook)/zz:_Back_Matter/20:_Glossary)
[12](https://viva.pressbooks.pub/introtoanthropology4field/back-matter/glossary/)
[13](https://github.com/adav671/BellaBeat-Tracker)
[14](https://www.alanmacfarlane.com/TEXTS/dictionary.pdf)
[15](https://perspectives.americananthro.org/archive/2017_Seeing_Like_an_Anthropologist.pdf)
[16](https://anth101.com/the-art-of-seeing/)
[17](https://www.anthroencyclopedia.com/entry/digital-anthropology)
[18](https://savageminds.org/2015/11/03/rewind-and-fast-forward-part-2/)