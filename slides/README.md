# Slides — Beamer presentation

A 33-frame Beamer presentation summarising the project: 4-depth taxonomy,
30-year cohort wall (8 × 5-year windows), paradigm shifts (SLAM 2003,
learning seeds 2008, sim-to-real 2018, foundation models 2023), and
educational use cases.

Generated from the live data in `../data/intermediate/papers_classified.json`,
so cohort numbers, top-class rankings, and emerging-class deltas reflect
whatever snapshot is currently committed.

## Build

The compiled PDF (`robotics_phylogeny.pdf`) is committed — open it
directly. Rebuild only when the data refreshes or you edit
`build_slides.py`.

### Option A — Docker (no local TeX install)

```bash
# 1. (Optional) Regenerate the .tex from the current dataset
python3 slides/build_slides.py

# 2. Compile inside the texlive image (~8 GB on first pull, cached after)
cd slides
docker run --rm -v "$(pwd):/work" -w /work texlive/texlive:latest \
  bash -c "xelatex -interaction=nonstopmode robotics_phylogeny.tex && \
           xelatex -interaction=nonstopmode robotics_phylogeny.tex"
```

`texlive/texlive:latest-small` works for everything *except* Korean
(no `kotex` pre-installed). Use the full `latest` tag.

### Option B — Local XeLaTeX

Need a TeX distribution (TeXLive / MacTeX / MiKTeX) with the `kotex`
and `cjk-ko` packages installed.

```bash
python3 slides/build_slides.py    # optional, only if data changed
cd slides
xelatex robotics_phylogeny.tex    # run twice for the TOC to resolve
xelatex robotics_phylogeny.tex
```

`lualatex` also works (kotex auto-detects the engine).

### Option C — Overleaf

Drag the `.tex` file into a fresh project, set the compiler to
**XeLaTeX** (Menu → Settings → Compiler), and click Recompile.

## Editing

The narrative voice is in `build_slides.py`:

- `COHORT_HEADLINES` — the per-cohort title + tagline. Edit these to
  re-tone the presentation.
- `make_paradigm_shifts_frame()` — the deep-dive frames (Foundation
  Models, SLAM revolution, etc.).
- `make_validation_frames()` — citation normalisation, venue character,
  educational uses, limitations, future work.

Numbers (paper counts, ranks, dominant classes) are recomputed from
the live JSON every time you re-run `build_slides.py` — no need to
edit them by hand when the dataset refreshes.
