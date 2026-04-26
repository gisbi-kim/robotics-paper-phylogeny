# Slides — Beamer presentation

A 33-frame Beamer presentation summarising the project: 4-depth taxonomy,
30-year cohort wall (8 × 5-year windows), paradigm shifts (SLAM 2003,
learning seeds 2008, sim-to-real 2018, foundation models 2023), and
educational use cases.

Generated from the live data in `../data/intermediate/papers_classified.json`,
so cohort numbers, top-class rankings, and emerging-class deltas reflect
whatever snapshot is currently committed.

## Build

This repo ships only the source. You need a TeX distribution
(TeXLive / MacTeX / MiKTeX) with **XeLaTeX** and the `kotex` package
(for Korean text support).

```bash
# 1. Regenerate the .tex from current data (optional — only if
#    papers_classified.json has changed since the last commit)
python3 slides/build_slides.py

# 2. Compile (run twice so the table-of-contents resolves)
cd slides
xelatex robotics_phylogeny.tex
xelatex robotics_phylogeny.tex
```

Output: `slides/robotics_phylogeny.pdf`

### Don't have XeLaTeX?

You can also try `lualatex` (kotex auto-detects the engine).
`pdflatex` works only with `\usepackage[hangul]{kotex}`; if you swap
the engine, change the `\usepackage{kotex}` line in
`robotics_phylogeny.tex` accordingly.

If you want to skip installing TeX entirely, the easiest path is
[Overleaf](https://www.overleaf.com/) — upload the `.tex` file, set
the compiler to XeLaTeX (Menu → Settings → Compiler), and click
Recompile.

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
