**Language**: English | [한국어](PLAN.md)

# Robotics Paper Phylogenetic Taxonomy Plan

## 1. Task definition

**Input**: `data.txt` (RoboPaper Atlas, 7,477 papers — T-RO/IJRR/RSS, 1988-2025)
**Output**: Excel file (.xlsx) — a sheet with semantic phylogeny labels assigned to every paper
**Core requirements** (excerpts from task.txt):
- Group **semantically**, not by simple word splitting + TF-IDF
  - e.g., "laser place recognition", "point cloud loop detection" → both `Place Recognition / LiDAR-based`
- Build a **hierarchical structure**, like biological taxonomy
- List **as many topics as possible** that have historically existed in robotics

---

## 2. Taxonomy design (4-level hierarchy)

Build it in 4 levels, like biological classification.

```
Phylum (top-level)  >  Class (mid-level)  >  Order (sub-level)  >  Genus (detailed lineage)
```

### 12 Phyla (top-level)

1. **Perception & Sensing** — perceiving the world through visual / tactile / range sensors
2. **SLAM & Localization** — pose estimation and mapping
3. **Planning** — path / mission / task planning
4. **Control** — control theory and its applications
5. **Manipulation** — manipulation (grasping, dexterous, deformable, etc.)
6. **Locomotion** — locomotion (legged, aerial, underwater, …)
7. **Robot Design & Hardware** — mechanism / actuator / soft-robot design
8. **Human-Robot Interaction** — HRI, teleoperation, assistive
9. **Multi-Robot Systems** — swarms / multi-robot coordination
10. **Learning for Robotics** — data-driven approaches such as RL/IL/Diffusion/VLA
11. **Application Domains** — application areas such as medical / agricultural / autonomous driving / space
12. **Theoretical Foundations** — kinematics / dynamics / optimization / geometry

Each Phylum contains 5-15 Classes, each Class contains Orders, and Genera are added when needed.
Examples are expanded separately in the `TAXONOMY.md` file.

### Semantic grouping examples (why not TF-IDF)

| Original title expression | Where it groups |
|---|---|
| "laser place recognition" | SLAM&Loc > Place Recognition > LiDAR-based |
| "point cloud loop detection" | SLAM&Loc > Place Recognition > LiDAR-based |
| "VPR with spiking nets" | SLAM&Loc > Place Recognition > Visual-based |
| "global localization for AGV" | SLAM&Loc > Place Recognition (same intent) |
| "VIO with event camera" | SLAM&Loc > SLAM > Event-based VIO/SLAM |
| "lidar-inertial odometry" | SLAM&Loc > SLAM > LiDAR-Inertial Odometry/SLAM |
| "LIO-SAM" / "FAST-LIO" | Same place (recognized semantically down to product names) |

---

## 3. Implementation strategy

### 3.1 Classification approach

- For each paper title, apply semantic classification rules **written by me (Claude) using domain knowledge**.
- Rules are sorted **by priority**:
  1. First, very specific signals (e.g., `vision-language-action`, `LIO-SAM`)
  2. Then mid-level categories (e.g., `place recognition` + `lidar`)
  3. Finally generic categories (e.g., when only `manipulation` is present)
- Based on **synonym clusters** + **co-occurrence patterns**, not TF-IDF.
  - e.g., `LIDAR = ['lidar','laser scan','point cloud','3d point',...]` —
    expressions with "the same meaning" are bundled together up front and used as a unit.

### 3.2 Classification pipeline

1. `data.txt` → parse 7,477 papers (idx, venue, year, title, authors, citations)
2. Apply the classifier to each paper title → assign `(Phylum, Class, Order, Genus)` labels
3. Check distribution statistics:
   - Count per Phylum
   - Count per Class (Top 30)
   - Number of Unclassified entries and samples
4. Inspect unclassified / suspect cases and reinforce the rules (1-2 iterations)
5. Export to Excel

### 3.3 Excel file structure

`robotics_taxonomy.xlsx` (3 sheets):

**Sheet 1: `Papers` — labeling result for all papers**
| idx | venue | year | title | authors | citations | Phylum | Class | Order | Genus |

**Sheet 2: `Taxonomy_Tree` — the taxonomy itself**
| Phylum | Class | Order | Genus | Paper Count | Description |

**Sheet 3: `Stats` — summary statistics**
- Paper count per Phylum
- Year × Phylum trend (pivot)
- List of unclassified cases

---

## 4. Deliverables (saved in this folder)

- `PLAN.md` ← the file you are reading now
- `TAXONOMY.md` ← full tree of 12 Phyla × Class × Order (to be written)
- `classify.py` ← classifier script
- `robotics_taxonomy.xlsx` ← final Excel deliverable
- `classification_stats.txt` ← classification statistics (for verification)

---

## 5. Limitations and assumptions

- Classification is title-only (data.txt has no abstracts). Accuracy may degrade when titles are ambiguous.
- A paper may span multiple categories, but a **single label** is assigned (the category whose highest-priority rule matches). Multi-label support can be added later if needed.
- Unclassified entries are kept as `Other / Unclassified` and included in the stats so the user can review them.

---

## 6. Progress checkpoints

- [ ] Step 1: Confirm the plan ← **you are here**
- [ ] Step 2: Write TAXONOMY.md (expand the full tree)
- [ ] Step 3: Apply the classifier + check statistics
- [ ] Step 4: Reinforce unclassified cases (if needed)
- [ ] Step 5: Generate the Excel file

→ Once step 1 is confirmed, I will proceed to step 2.
   Let me know if there are Phyla you would like to add or change in the taxonomy structure, or any Class you want to dig into more deeply.
