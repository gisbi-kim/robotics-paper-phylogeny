**Language**: English | [한국어](README.md)

# EDA — Stage B: Raw Taxonomy Visualization

A first-pass analysis visualizing the classification results of 7,477 papers as 4 static plots + 2 interactive HTMLs.

> Visualization stage: **B (viewing the raw data itself)**.
> The next stage C (phylogenetic tree in biological style) is separate.

---

## Outputs

```
eda/
├── eda_plots.py              # 모든 plot 생성 스크립트
├── figures/                  # 정적 PNG (GitHub에서 바로 보임)
│   ├── 01_phylum_stack.png
│   ├── 02_phylum_small_multiples.png
│   ├── 03_class_heatmap.png
│   └── 04_top_classes_drill.png
└── interactive/              # plotly HTML (브라우저로 열어서 hover)
    ├── 01_phylum_stack.html
    └── 03_class_heatmap.html
```

---

## Plot 1 — Phylum × year stack chart

![Phylum Stack](figures/01_phylum_stack.png)

**Axes**: X = 1988~2025, Y = annual paper count (stacked).
**Colors**: 13 Phyla + Editorial + Unclassified.

**What stands out**:
- **2004 jump** — pre-RA-L era, but a sharp increase as IJRR + T-RO are combined
- **Plateau in 2017~2020**, then **another explosion from 2021** — RSS expansion + entry into the AI era
- **Light blue (SLAM & Localization)** has held a consistently large share since 2005
- **Greens (Manipulation + Locomotion)** become the thickest band from the late 2010s onward

**Interactive**: [interactive/01_phylum_stack.html](interactive/01_phylum_stack.html) — hover for exact counts.

---

## Plot 2 — Per-Phylum small multiples (Class breakdown)

![Per-Phylum](figures/02_phylum_small_multiples.png)

**Layout**: one panel for each of the 13 Phyla. Within each panel, **top 8 Classes** are stacked area.

**What stands out**:
- **SLAM & Localization**: SLAM Class explodes around 2005 (FastSLAM/GraphSLAM era)
- **Locomotion**: from 2010 onward, Aerial Locomotion catches up to Legged (drone era)
- **Learning for Robotics**: appears from 2017, with a Foundation Models explosion in 2022~2025
- **Robot Software & Architecture**: briefly active in the late 1990s, active again in the 2020s (Behavior Trees)
- **Theoretical Foundations**: dominant in the 1990s, share decreases from 2010 onward
- **HRI**: gradual growth, stable share in the 2020s

---

## Plot 3 — Class heatmap (all 100 Classes × year)

![Class Heatmap](figures/03_class_heatmap.png)

**Axes**: rows = all Classes (100, sorted by Phylum group), columns = 3-year buckets.
**Color**: log10(1 + paper count) — log scale to make sparse activity visible.
**Y-label color**: the Phylum color the Class belongs to (matches Plot 1).

**What stands out**:
- **Always-active Classes**: SLAM, Path/Motion Planning, Grasping, Bipedal/Humanoid, Mobile Wheeled — red across nearly all eras
- **Recent risers**: Foundation Models, Diffusion Policies, Aerial Swarms, 3D Scene Graph (red only in the rightmost buckets)
- **Disappeared fields**: some 1990s mechanism design Classes have faded recently
- **Overall pattern**: darker toward the right = total publication volume itself increases

**Interactive**: [interactive/03_class_heatmap.html](interactive/03_class_heatmap.html) — hover for exact counts + full Class names.

---

## Plot 4 — Top 12 Class drill-down (Order breakdown)

![Top Classes Drill](figures/04_top_classes_drill.png)

**Layout**: one mini panel for each of the 12 largest Classes. Within each, **top 6 Orders** are stacked area.

**What stands out**:
- **SLAM**: General SLAM (early) → Visual SLAM/Odometry (2010s) → LIO/VIO/Multi-modal (recent)
- **Path/Motion Planning**: Sampling-based (RRT) → diversification → Trajectory Optimization rising recently
- **Grasping**: from the mid-2010s, Learning-based overtakes Force-Closure
- **Bipedal**: paradigm shift from ZMP → HZD → Sim-to-Real RL
- **Foundation Models**: an entirely new entry post-2022 — VLA / Diffusion / LLM appearing nearly simultaneously

---

## Reproduction

```bash
cd "this-repo"
python3 eda/eda_plots.py
# → eda/figures/*.png + eda/interactive/*.html
```

> Dependencies: `matplotlib`, `plotly`.

---

## Next step

**C — Phylogenetic tree (biological style)**: the 4 plots above are "for data analysis", whereas C is "single-image impact". The idea is to draw the entire 13 Phylum × Class × Order × Genus tree in a branching form, realizing the original intent of task.txt (like a phylogenetic tree of organisms).
