**Language**: English | [한국어](README.md)

# Robotics Paper Phylogenetic Taxonomy

🌐 **Live site**: <https://gisbi-kim.github.io/robotics-paper-phylogeny/>

> Semantic classification of 7,477 robotics papers (T-RO / IJRR / RSS, 1988–2025), grouped into a biological-style phylogenetic taxonomy.

The source data is drawn from **RoboPaper Atlas**. Paper titles, years, authors, and citation counts from three journals — T-RO, IJRR, and RSS — are mapped onto a **4-level** (`Phylum > Class > Order > Genus`) tree using **semantic synonym clusters rather than plain TF-IDF**.

- **Every paper is labeled at all 4 depths**: Phylum / Class / Order are 100% covered, Genus is filled in when a specific rule matches (about 52%) and otherwise filled with `(general)`.

---

## EDA Visualizations (Stage B)

Four raw-data visualizations live in the [`eda/`](eda/) folder — see [eda/README.en.md](eda/README.en.md) for details.

| Plot | Preview | Description |
|---|---|---|
| 1. Phylum stack | [![](eda/figures/01_phylum_stack.png)](eda/figures/01_phylum_stack.png) | 13 Phylum × year stacked area. Field share over time. |
| 2. Per-Phylum small multiples | [![](eda/figures/02_phylum_small_multiples.png)](eda/figures/02_phylum_small_multiples.png) | Top 8 Class trends within each Phylum. |
| 3. Class heatmap | [![](eda/figures/03_class_heatmap.png)](eda/figures/03_class_heatmap.png) | 100 Class × 3-year buckets. Which Class became active when? |
| 4. Top 12 Class drill | [![](eda/figures/04_top_classes_drill.png)](eda/figures/04_top_classes_drill.png) | Order-level breakdown inside popular Classes (paradigm shifts in SLAM, Grasping, etc.). |

> Interactive versions: [eda/interactive/01_phylum_stack.html](eda/interactive/01_phylum_stack.html), [eda/interactive/03_class_heatmap.html](eda/interactive/03_class_heatmap.html) — download and open in a browser.

---

## Deliverables

| File | Description |
|---|---|
| **[`robotics_taxonomy.xlsx`](robotics_taxonomy.xlsx)** | Main result — 3 sheets (Papers / Taxonomy_Tree / Stats), **4-depth (P/C/O/G)** |
| [`TAXONOMY.md`](TAXONOMY.md) | Full tree of 13 Phylum × ~95 Class × ~330 Order |
| [`TAXONOMY_CHANGES.md`](TAXONOMY_CHANGES.md) | Diff and update notes between the draft and the post-read-through revision over all 7,477 papers |
| [`TAXONOMY_EVALUATION.en.md`](TAXONOMY_EVALUATION.en.md) | Self-evaluation: MECE and insightfulness compared against the Springer Handbook of Robotics |
| [`PLAN.en.md`](PLAN.en.md) | Work plan |
| [`REFRESH.en.md`](REFRESH.en.md) | Procedure for syncing citations/DOIs from a RoboPaper Atlas snapshot |
| [`MAINTENANCE.en.md`](MAINTENANCE.en.md) | Data provenance & timestamps, dependency map, scenario checklists for refreshing months/years from now |
| [`refresh_from_atlas.py`](refresh_from_atlas.py) | atlas xlsx → citation/DOI refresh + regeneration of `papers.json` |
| [`slides/`](slides/) | 33-frame Beamer deck (cohort wall + paradigm shifts) — compile with XeLaTeX |
| [`classify.py`](classify.py) | Levels 1–3 classifier (Phylum/Class/Order) |
| [`genus_rules.py`](genus_rules.py) | Level-4 classifier (Genus, sub-rules for the top 45 Orders) |
| [`make_excel.py`](make_excel.py) | Script that converts classification results into the Excel file |
| [`data/raw/data.txt`](data/raw/data.txt) | Source (RoboPaper Atlas dump) |
| [`data/raw/task.txt`](data/raw/task.txt) | Original user task instructions |
| [`data/intermediate/papers_parsed.json`](data/intermediate/papers_parsed.json) | First-pass parsing result (7,477 papers) |
| [`data/intermediate/titles_chronological.txt`](data/intermediate/titles_chronological.txt) | Chronological list of titles (for read-through) |
| [`data/intermediate/reading_notes.md`](data/intermediate/reading_notes.md) | Notes taken during the read-through |
| [`data/intermediate/papers_classified.json`](data/intermediate/papers_classified.json) | Papers with classification labels attached (4-depth) |

---

## Classification Distribution Summary

7,477 papers in total. 13 Phylum + Editorial + Unclassified, 15 categories overall.

| Phylum | Papers | % |
|---|---:|---:|
| Manipulation | 934 | 12.5% |
| Locomotion | 842 | 11.3% |
| Planning | 835 | 11.2% |
| SLAM & Localization | 670 | 9.0% |
| Robot Design & Hardware | 623 | 8.3% |
| Perception & Sensing | 554 | 7.4% |
| Theoretical Foundations | 491 | 6.6% |
| Control | 441 | 5.9% |
| Multi-Robot Systems | 408 | 5.5% |
| Application Domains | 396 | 5.3% |
| Human-Robot Interaction | 395 | 5.3% |
| Learning for Robotics | 354 | 4.7% |
| Robot Software & Architecture | 30 | 0.4% |
| Other / Editorial | 288 | 3.9% |
| **Other / Unclassified** | **216** | **2.9%** |
| **Total** | **7,477** | **100%** |

### Top 10 Class

| Phylum > Class | Papers |
|---|---:|
| Planning > Path/Motion Planning | 477 |
| Locomotion > Legged Locomotion | 337 |
| Manipulation > Contact-rich Manipulation | 297 |
| Multi-Robot Systems > Coordination | 284 |
| SLAM & Localization > SLAM | 259 |
| Robot Design & Hardware > Mechanism Design | 227 |
| Manipulation > Grasping | 218 |
| Planning > Navigation | 209 |
| Manipulation > General Manipulation | 194 |
| Locomotion > Aerial Locomotion | 184 |

---

## One-Line Description of the 13 Phyla

1. **Perception & Sensing** — vision, LiDAR, tactile, event-based, multimodal perception
2. **SLAM & Localization** — localization, mapping, calibration, Place Recognition
3. **Planning** — path / motion / task / navigation / exploration planning
4. **Control** — classical, predictive, impedance, safety, learning-based control
5. **Manipulation** — grasping, dexterous, deformable, assembly, non-prehensile, mobile manipulation
6. **Locomotion** — legged, wheeled, aerial, underwater, bio-inspired locomotion
7. **Robot Design & Hardware** — soft, continuum, modular, micro, actuator design
8. **Human-Robot Interaction** — pHRI, teleoperation, assistive, haptics
9. **Multi-Robot Systems** — swarm, coordination, MAPF, distributed SLAM, aerial swarm
10. **Learning for Robotics** — RL, IL, VLA, Diffusion Policy, datasets
11. **Application Domains** — medical, field, autonomous driving, space, service, computational biology
12. **Theoretical Foundations** — kinematics, dynamics, optimization, Lie groups, safety
13. **Robot Software & Architecture** — middleware, BT, code generation, real-time

---

## Workflow (Reproducible)

```bash
# 1. Parse the data (raw → JSON)
#    Read data/raw/data.txt, extract 7,477 papers → data/intermediate/papers_parsed.json

# 2. Read through → write notes
#    Read data/intermediate/titles_chronological.txt in chronological order
#    and take notes in data/intermediate/reading_notes.md.
#    Consolidate the result into TAXONOMY_CHANGES.md and update TAXONOMY.md as the final version.

# 3. Run the classifier (P/C/O first pass + Genus 4th-level classification)
python3 classify.py
# → /tmp/classified.json (backup at data/intermediate/papers_classified.json)

# 4. Generate the Excel file (with 4-depth columns)
python3 make_excel.py → robotics_taxonomy.xlsx
```

> Dependencies: only `python3` + `openpyxl` are required.

---

## Classification Methodology (Why Not TF-IDF?)

The core requirement stated in the task instructions (`data/raw/task.txt`):
> "I'm not asking you to just split words and run tf-idf. Use your attention to judge things semantically."
> "For example, one paper might call it 'laser place recognition' and another 'point cloud based loop detection,' but lump all of these into place recognition."

→ Accordingly, the classifier ([`classify.py`](classify.py)) directly defines **synonym clusters**:

```python
LIDAR = ['lidar', 'laser scan', 'point cloud', '3d point', 'range scan', ...]
PLACE_RECOG = ['place recognition', 'loop closure', 'loop detection',
               'global localization', 'visual localization', 'vpr', ...]

if has_any(t, PLACE_RECOG):
    if has_any(t, LIDAR):
        return ('SLAM & Localization', 'Place Recognition', 'LiDAR-based')
    if has_any(t, VISUAL):
        return ('SLAM & Localization', 'Place Recognition', 'Visual-based')
```

→ Expressions like "laser place recognition," "point cloud loop detection," and "lidar VPR" **all** end up in `Place Recognition / LiDAR-based`. Cross-cutting cases are handled with priority rules (specific → general).

---

## Limitations

- **Single label**: one paper = one category. Multi-field papers are routed to the most specific bucket via priority rules.
- **Title only**: no abstracts. Classification accuracy drops when titles are ambiguous.
- **12.4% unclassified**: cases that are too specific or fail to hit any catchall. Left as `Other / Unclassified` for the user to review.

---

## License / Data Source

- Original paper metadata: T-RO, IJRR, RSS journals (RoboPaper Atlas, based on DBLP + OpenAlex)
- This classification work (code + taxonomy): free to use
