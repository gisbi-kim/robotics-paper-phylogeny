**Language**: English | [한국어](REFRESH.md)

# Refresh Guide

The artifacts in this repo are derived from a data snapshot of **RoboPaper Atlas** ([https://gisbi-kim.github.io/robopaper-atlas/](https://gisbi-kim.github.io/robopaper-atlas/)). Whenever the atlas is updated, the following becomes stale:

- **citation counts** (`cited_by_count`) — change every time OpenAlex re-indexes
- **DOI / URL** — new papers may not have a DOI at first, but get one filled in later
- **paper roster** — when new T-RO/IJRR/RSS papers enter the atlas, they are missing from the classified set here

This document describes the procedure for propagating those changes throughout this repo (`tro-계통도`).

---

## Data flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. RoboPaper Atlas (upstream)                               │
│    https://gisbi-kim.github.io/robopaper-atlas/             │
│    └─ robopaper_atlas_all.xlsx                              │
│       (sheet: "papers", ~88k rows)                          │
│       cols: venue, year, title, authors, cited_by_count,    │
│             doi, ee, abstract, …                            │
└─────────────────────────┬───────────────────────────────────┘
                          │ refresh_from_atlas.py
                          │ (title-match + venue/year disambiguation)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. data/intermediate/papers_classified.json                 │
│    7,477 papers  ·  citations 갱신됨                        │
│    cols: idx, venue, year, title, authors, citations,       │
│          phylum, class, order, genus                        │
└─────────┬───────────────────────────┬───────────────────────┘
          │                           │
          ▼                           ▼
   eda/phylogeny_tree.py     eda/eda_plots.py
          │                           │
          ▼                           ▼
   eda/interactive/             eda/figures/*.png
   tree_data.json               eda/interactive/0X_*.html
   (radial 구조)                (정적/인터랙티브 EDA)

┌─────────────────────────────────────────────────────────────┐
│ 3. eda/interactive/papers.json                              │
│    radial viewer 모달이 fetch 하는 슬림 (2.85 MB) 페이로드 │
│    classified.json + atlas의 doi/ee를 join 한 결과          │
│    refresh_from_atlas.py가 같이 생성함                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Standard refresh procedure

### 1. Download the atlas

Fetch the upstream xlsx (~48 MB):

```bash
curl -L -o /tmp/robopaper_atlas_all.xlsx \
  https://gisbi-kim.github.io/robopaper-atlas/robopaper_atlas_all.xlsx
```

> If `../robopaper atlas/robopaper_atlas_all.xlsx` or `../robopaper atlas/all_enriched.json` already exists locally, it is auto-detected and the download can be skipped.

### 2. Sync citations + DOIs

```bash
python3 refresh_from_atlas.py --xlsx /tmp/robopaper_atlas_all.xlsx
```

What this script does:

- Indexes every paper in the atlas by normalized title
- For every paper in `data/intermediate/papers_classified.json`, matches and:
  - Updates the `citations` field with the latest value from the atlas
  - Pulls in the matched `doi` / `ee`
- Saves the updated `papers_classified.json` in place (taxonomy labels are preserved)
- Regenerates `eda/interactive/papers.json` (slim payload for the radial viewer modal)
- Reports how many new T-RO/IJRR/RSS papers exist in the atlas but are missing from the classified set (see next step)

### 3. Classify new papers (if needed)

If the script above prints `⚠ N new T-RO/IJRR/RSS papers in atlas but not in classified set`:

```bash
# 1. Combine the new papers extracted from the atlas with the existing 7,477 entries
#    into /tmp/papers.json
#    (no automation script for this yet — add manually or
#     adjust the input path of classify.py)
# 2. Run classification:
python3 classify.py
# 3. Move the /tmp/classified.json produced by classify.py to
#    data/intermediate/papers_classified.json, then run refresh_from_atlas.py again
#    to merge in DOI/citation
python3 refresh_from_atlas.py --xlsx /tmp/robopaper_atlas_all.xlsx
```

> Typically a few dozen to a few hundred papers are added per quarter. **Existing classifications do not need to be touched** — taxonomy depends only on title/abstract, not citations.

### 4. Regenerate tree_data + EDA

Since either the classification results or citation counts have changed, regenerate the following artifacts:

```bash
python3 eda/phylogeny_tree.py   # → eda/interactive/tree_data.json (radial viewer data)
python3 eda/eda_plots.py        # → eda/figures/*.png + eda/interactive/0[1-4]_*.html
python3 make_excel.py           # → robotics_taxonomy.xlsx (Excel deliverable)
```

### 5. Verify + commit

Open `index.html` locally in a browser and confirm it behaves the same as the live site:

```bash
python3 -m http.server 8000
# → http://localhost:8000/
# → http://localhost:8000/eda/interactive/05_phylogeny_radial_web.html
#   (click a pie wedge → "이 계열의 논문 N편 보기" → verify the DOI links work)
```

If everything looks good, commit the changes:

```bash
git add data/intermediate/papers_classified.json \
        eda/interactive/papers.json \
        eda/interactive/tree_data.json \
        eda/interactive/0[1-4]_*.html \
        eda/figures \
        robotics_taxonomy.xlsx
git commit -m "Refresh from RoboPaper Atlas snapshot YYYY-MM-DD"
git push
```

GitHub Pages reflects the changes on the live site within 1-2 minutes.

---

## Recommended refresh frequency

| Trigger | Action |
|---|---|
| Every time the atlas is updated | Steps 1-2 only (citation/DOI sync). Under 5 minutes |
| Every quarter (or when the atlas paper count grows noticeably) | Full cycle, steps 1-5 |
| When taxonomy rules (`classify.py`, `genus_rules.py`) change | Re-run from classify.py through the end |

---

## Troubleshooting

**"No atlas source found"** → Pass an explicit path with `--xlsx`, or download the xlsx and retry.

**Match rate drops below 90%** → The atlas may have changed its title normalization. The `norm()` function in `refresh_from_atlas.py` needs to be aligned with the atlas's matching logic.

**Citations decrease (negative delta)** → Normal. OpenAlex may remove some sources or de-duplicate, causing decreases. If the drop is large, check whether there is a data issue in the atlas itself.
