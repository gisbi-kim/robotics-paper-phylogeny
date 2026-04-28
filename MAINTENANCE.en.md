**Language**: English | [한국어](MAINTENANCE.md)

# Maintenance Guide

> The artifacts in this repo have dependencies between them — change one thing and several outputs go stale. This document covers **data provenance**, **as-of timestamps**, and **what to regenerate when**.

If you only need the quick procedure, see [REFRESH.md](REFRESH.md) (citation/DOI sync only).

---

## 1. Data provenance and coverage

### Where the data comes from

The source is a snapshot of **RoboPaper Atlas** ([https://gisbi-kim.github.io/robopaper-atlas/](https://gisbi-kim.github.io/robopaper-atlas/)). The Atlas itself integrates:

- **DBLP** — venue / journal metadata
- **OpenAlex** — citation counts, DOIs, abstracts

### What we classified

The Atlas covers 9 venues (ICRA / IROS / RA-L / T-RO / RSS / IJRR / Sci-Rob / SoRo / T-Mech). **This repo restricts to 3 of them**:

| Venue | Full name | Type | Since |
|---|---|---|---|
| **T-RO** | IEEE Transactions on Robotics | Journal | 2004 (T-RA + part of IJRR merged) |
| **IJRR** | International Journal of Robotics Research | Journal | 1982 |
| **RSS** | Robotics: Science and Systems | Conference | 2005 |

**Why these three**: all are highly selective (IJRR/T-RO acceptance rates below 30%), peer-review quality is consistently high, and they cover the *canonical* span of academic robotics research. ICRA/IROS have higher volume but more variance; RA-L is letter-format and shorter in scope.

### Snapshot timestamp

```
Snapshot date:    2025-XX-XX (last run of refresh_from_atlas.py)
Year coverage:    1988 ~ 2025
Paper count:      7,477
Per-venue split:  T-RO 4,XXX · IJRR 2,XXX · RSS 9XX  (exact split: Stats sheet of robotics_taxonomy.xlsx)
```

> **When refreshing, always update**: README counts, taxonomy.html chips, slides, and this document itself.

### License / attribution

The classification is free to use. Underlying metadata belongs to DBLP / OpenAlex / Springer / IEEE.

---

## 2. Dependency map — what staleifies what

```
            ┌─────────────────────┐
            │  Atlas snapshot     │
            │  (citation·DOI·new) │
            └─────────┬───────────┘
                      │
                      ▼
       ┌──────────────────────────┐
       │ classify.py + genus_rules│  ← editing classification rules forces a full rebuild
       │     (Phylum/Class/Order) │
       └──────────────┬───────────┘
                      │
                      ▼
            data/intermediate/
            papers_classified.json    ──── 7,477 × {P, C, O, G}
                      │
       ┌──────────────┼──────────────────┬───────────────────┐
       │              │                  │                   │
       ▼              ▼                  ▼                   ▼
  eda/phylogeny    eda/eda_plots    make_excel.py     refresh_from_atlas.py
  _tree.py         .py              robotics_         eda/interactive/
  tree_data.json   figures/*.png    taxonomy.xlsx     papers.json
                   interactive/0[1-4].html             (DOI join)
       │              │                  │                   │
       └──────────────┴──────────────────┴───────────────────┘
                                │
                                ▼
                   ┌─────────────────────────┐
                   │ Manual sync needed:     │
                   │  · README.md / .en.md   │
                   │  · taxonomy.html        │
                   │  · TAXONOMY.md          │
                   │  · TAXONOMY_CHANGES.md  │
                   │  · slides/build_slides  │
                   │  · MAINTENANCE.md (§1)  │
                   └─────────────────────────┘
```

### Per-scenario impact

| What you changed | Auto-regenerated outputs | Hand-edited text |
|---|---|---|
| **Atlas snapshot only** (citations changed) | `papers_classified.json` (citation field), `papers.json` | None (count text doesn't change) |
| **Atlas + new papers** (e.g. 2026 cohort) | All of the above + `tree_data.json` + EDA + Excel + Slides | `README.md` counts, `taxonomy.html` chips, this doc §1, slides cover year |
| **Add/remove Phylum/Class/Order** (taxonomy schema) | `papers_classified.json` from scratch, then everything below it | `TAXONOMY.md`, `TAXONOMY_CHANGES.md`, `README.md` Phylum table, `taxonomy.html` Phylum tiles, `MAINTENANCE.md`, `TAXONOMY_EVALUATION.md` (distribution numbers) |
| **Genus rules only** (`genus_rules.py`) | `papers_classified.json`, `tree_data.json`, `papers.json`, Excel | None (top-level distribution rarely shifts) |
| **README / docs only** | None | Just the file + its English mirror |

### English mirrors (`.en.md`)

The following docs come in pairs and **must** be updated together (the site toggle depends on both):

- `README.md` ↔ `README.en.md`
- `PLAN.md` ↔ `PLAN.en.md`
- `REFRESH.md` ↔ `REFRESH.en.md`
- `TAXONOMY_EVALUATION.md` ↔ `TAXONOMY_EVALUATION.en.md`
- `MAINTENANCE.md` ↔ `MAINTENANCE.en.md` (this doc)
- `eda/README.md` ↔ `eda/README.en.md`

`TAXONOMY.md` and `TAXONOMY_CHANGES.md` have no English mirror — the tree body is mostly code identifiers.

---

## 3. "N months/years from now" scenarios

### Scenario A — Quarterly light refresh (citations only)

**Time**: ~10 min

```bash
curl -L -o /tmp/atlas.xlsx https://gisbi-kim.github.io/robopaper-atlas/robopaper_atlas_all.xlsx
python3 refresh_from_atlas.py --xlsx /tmp/atlas.xlsx
python3 eda/eda_plots.py            # if any chart depends on citations
python3 make_excel.py
git add -A && git commit -m "Refresh from atlas snapshot $(date +%F)" && git push
```

→ Counts don't move. README / slides untouched.

---

### Scenario B — 6–12 months later, new year of papers

**Time**: ~1 hour

1. **Download Atlas + extract new papers**
   ```bash
   curl -L -o /tmp/atlas.xlsx https://gisbi-kim.github.io/robopaper-atlas/robopaper_atlas_all.xlsx
   python3 refresh_from_atlas.py --xlsx /tmp/atlas.xlsx
   # → console prints "⚠ N new T-RO/IJRR/RSS papers" — proceed
   ```

2. **Classify the new papers**
   - Append new entries to `data/intermediate/papers_parsed.json` (continue idx)
   - `python3 classify.py` → regenerates `data/intermediate/papers_classified.json`
   - `python3 refresh_from_atlas.py --xlsx /tmp/atlas.xlsx` again (DOI join)

3. **Regenerate everything downstream**
   ```bash
   python3 eda/phylogeny_tree.py     # tree_data.json
   python3 eda/eda_plots.py          # PNG + interactive HTML
   python3 make_excel.py             # robotics_taxonomy.xlsx
   python3 slides/build_slides.py    # rebuilds .tex (XeLaTeX compile separately)
   cd slides && docker run --rm -v "$(pwd):/work" -w /work texlive/texlive:latest \
     bash -c "xelatex -interaction=nonstopmode robotics_phylogeny.tex && \
              xelatex -interaction=nonstopmode robotics_phylogeny.tex"
   cd ..
   ```

4. **Manual sync (don't skip!)**
   - [ ] `README.md` / `.en.md` — "7,477 papers" → new count, "1988~2025" → new range
   - [ ] `taxonomy.html` — chip "📦 7,477 papers" count, Phylum-distribution table
   - [ ] `MAINTENANCE.md` / `.en.md` — §1 snapshot date and count
   - [ ] `TAXONOMY_CHANGES.md` — append fresh read-through notes (optional)
   - [ ] Slide cover year (build_slides.py handles this, but verify)

5. **Verify + commit**
   ```bash
   python3 -m http.server 8000   # check localhost:8000 matches the live site
   git add -A
   git commit -m "Update through $(date +%Y-%m): N new papers, taxonomy stable"
   git push
   ```

---

### Scenario C — Introduce a new top-level category (e.g. an 'Embodied AI' Phylum in 2027)

**Time**: half day to a full day

This is a schema change — every existing paper must be **re-labelled**.

1. **Add the new branch in TAXONOMY.md** + define the splitting criterion
2. **Record rationale in TAXONOMY_CHANGES.md** (why added/removed)
3. **Add rules to classify.py + genus_rules.py**
   - Priority matters: put more specific rules higher
4. **Re-classify and validate**
   ```bash
   python3 classify.py
   # Inspect the distribution — is the new Phylum a sane share? Did any other Phylum lose papers unfairly?
   ```
5. **Run scenario B steps 3–5 in full**
6. **Additional sync (on top of scenario B)**:
   - [ ] `README.md` / `.en.md` — update "13 Phyla" one-line table, Top 10 Class table
   - [ ] `taxonomy.html` — update the Phylum tile grid (edit HTML directly), §2 count in section-eyebrow
   - [ ] `TAXONOMY_EVALUATION.md` / `.en.md` — refresh comparison table and our-Phyla list
   - [ ] `PLAN.md` — Phylum count
   - [ ] `MAINTENANCE.md` (this doc) — §1 + dependency-map narrative

---

## 4. Pre-push verification checklist

```
☐ python3 -m http.server 8000 → matches the live site
☐ index.html / taxonomy.html KR↔EN toggle works on both pages
☐ Interactive trees (05/06) → click → paper modal → DOI link works
☐ slides/robotics_phylogeny.pdf is committed and the cover year is correct
☐ robotics_taxonomy.xlsx row count matches papers_classified.json
☐ All counts in README agree with papers_classified.json
☐ KR↔EN mirror docs updated together (README, REFRESH, MAINTENANCE, EVALUATION)
```

---

## 5. Spots people forget

| Location | Auto? | What breaks if forgotten |
|---|---|---|
| `taxonomy.html` Phylum tile grid (§2) | **manual** | New Phylum doesn't appear on the site |
| `taxonomy.html` chip count (📦 7,477 papers) | **manual** | Site count drifts from README |
| `MAINTENANCE.md` §1 (this doc's first section) | **manual** | "When was the last refresh?" becomes untraceable |
| `slides/build_slides.py` `COHORT_HEADLINES` | **manual** | Slide narrative still has the old tone |
| `eda/insights.json` | **semi-auto** (insights.py) | Chart captions show old numbers |
| Phylum-distribution % in `TAXONOMY_EVALUATION.md` | **manual** | Self-eval table goes stale |

---

## 6. Related docs

- [REFRESH.en.md](REFRESH.en.md) — citation/DOI sync procedure (scenario A in detail)
- [PLAN.en.md](PLAN.en.md) — original work plan (classification philosophy)
- [TAXONOMY.md](TAXONOMY.md) — full 13 × ~100 × ~330 tree
- [TAXONOMY_CHANGES.md](TAXONOMY_CHANGES.md) — taxonomy revision history
- [TAXONOMY_EVALUATION.en.md](TAXONOMY_EVALUATION.en.md) — self-evaluation vs. Springer Handbook
- [eda/README.en.md](eda/README.en.md) — per-chart explanations + regen instructions
- [slides/README.md](slides/README.md) — Beamer build procedure

---

*Last updated: when this document was authored. Refresh §1 (snapshot date and paper count) yourself when you re-run the pipeline.*
