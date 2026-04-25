"""
Stage C — Phylogenetic tree visualizations (생물 계통도 스타일).

Outputs:
  figures/05_phylogeny_radial.png    — radial dendrogram (matplotlib)
  interactive/05_phylogeny_sunburst.html — 4-level interactive sunburst (plotly)
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Wedge, FancyArrowPatch
import numpy as np

import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent
FIGS = ROOT / 'figures'
INTERACTIVE = ROOT / 'interactive'
FIGS.mkdir(exist_ok=True)
INTERACTIVE.mkdir(exist_ok=True)

DATA = ROOT.parent / 'data' / 'intermediate' / 'papers_classified.json'

with open(DATA, 'r', encoding='utf-8') as f:
    papers = json.load(f)

print(f"Loaded {len(papers)} papers")

# ============================================================
# Phylum order + colors (matching eda_plots.py)
# ============================================================
PHYLA = [
    'Perception & Sensing',
    'SLAM & Localization',
    'Planning',
    'Control',
    'Manipulation',
    'Locomotion',
    'Robot Design & Hardware',
    'Human-Robot Interaction',
    'Multi-Robot Systems',
    'Learning for Robotics',
    'Application Domains',
    'Theoretical Foundations',
    'Robot Software & Architecture',
]

PHY_COLORS = {
    'Perception & Sensing':         '#1f77b4',
    'SLAM & Localization':          '#aec7e8',
    'Planning':                     '#ff7f0e',
    'Control':                      '#ffbb78',
    'Manipulation':                 '#2ca02c',
    'Locomotion':                   '#98df8a',
    'Robot Design & Hardware':      '#d62728',
    'Human-Robot Interaction':      '#ff9896',
    'Multi-Robot Systems':          '#9467bd',
    'Learning for Robotics':        '#c5b0d5',
    'Application Domains':          '#8c564b',
    'Theoretical Foundations':      '#c49c94',
    'Robot Software & Architecture':'#e377c2',
}

# ============================================================
# Build hierarchy tree (Phylum -> Class -> Order -> count)
# ============================================================
tree = defaultdict(lambda: defaultdict(Counter))
for p in papers:
    if p['phylum'] in ('Other / Unclassified', 'Other / Editorial'):
        continue
    tree[p['phylum']][p['class']][p['order']] += 1

# Total per phylum (for sizing)
phy_totals = {phy: sum(sum(o.values()) for o in tree[phy].values())
              for phy in PHYLA if phy in tree}
overall_total = sum(phy_totals.values())
print(f"Phylum totals: {sum(phy_totals.values())} (excluding Other)")


# ============================================================
# 1) Radial dendrogram (matplotlib custom drawing)
# ============================================================
def lighten(color, amount=0.3):
    """Lighten a hex color by mixing with white."""
    import matplotlib.colors as mcolors
    rgb = mcolors.to_rgb(color)
    return tuple(c + (1 - c) * amount for c in rgb)


def draw_radial_phylogeny():
    print("\n[1/2] Radial dendrogram…")
    fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # Radial bands
    R0, R1 = 0.5, 1.4   # Phylum band
    R2 = 2.4            # Class band end
    R3 = 3.4            # Order band end
    R_LABEL_PHY = 0.95
    R_LABEL_CLS = 1.9
    R_LABEL_ORD = 2.9

    # Allocate angular space proportional to phy_totals
    angles = {}
    cur = 0.0
    full_angle = 2 * np.pi
    # Padding: leave 1° between phyla
    n_phyla = len(phy_totals)
    pad_rad = np.deg2rad(1.0)
    usable = full_angle - n_phyla * pad_rad

    for phy in PHYLA:
        if phy not in phy_totals:
            continue
        share = phy_totals[phy] / overall_total
        span = usable * share
        angles[phy] = (cur, cur + span)
        cur += span + pad_rad

    # ---- Draw Phylum band (innermost) ----
    for phy, (a0, a1) in angles.items():
        color = PHY_COLORS[phy]
        # Phylum wedge — solid color
        n_pts = 50
        thetas = np.linspace(a0, a1, n_pts)
        ax.fill_between(thetas, R0, R1, color=color, alpha=0.95,
                        edgecolor='white', linewidth=0.5)
        # Phylum label at outer edge of band
        mid = (a0 + a1) / 2
        # Rotate text to follow arc
        rot = np.rad2deg(mid)
        ha = 'center'
        # Adjust rotation for readability
        if rot > 90 and rot < 270:
            rot = rot + 180
        ax.text(mid, R_LABEL_PHY, phy.replace(' & ', '\n& '),
                rotation=rot - 90, rotation_mode='anchor',
                ha=ha, va='center', fontsize=10, weight='bold',
                color='white')

    # ---- Draw Class band (middle) ----
    for phy, (pa0, pa1) in angles.items():
        classes = tree[phy]
        cls_total = sum(sum(o.values()) for o in classes.values())
        if cls_total == 0:
            continue
        # Sort classes by count desc
        cls_sorted = sorted(classes.items(),
                            key=lambda x: -sum(x[1].values()))
        cur_a = pa0
        cls_pad = np.deg2rad(0.2)
        avail = (pa1 - pa0) - len(cls_sorted) * cls_pad
        if avail < 0:
            avail = (pa1 - pa0)
            cls_pad = 0
        for cls, orders in cls_sorted:
            cls_count = sum(orders.values())
            share = cls_count / cls_total
            span = avail * share
            ca0, ca1 = cur_a, cur_a + span
            cls_color = lighten(PHY_COLORS[phy], 0.4)
            n_pts = max(6, int(span * 30))
            thetas = np.linspace(ca0, ca1, n_pts)
            ax.fill_between(thetas, R1, R2, color=cls_color,
                            alpha=0.85, edgecolor='white', linewidth=0.4)

            # Label only larger classes (>= 0.6 deg span)
            if span > np.deg2rad(0.6):
                mid = (ca0 + ca1) / 2
                rot = np.rad2deg(mid)
                if rot > 90 and rot < 270:
                    rot = rot + 180
                # Truncate long names
                label = cls if len(cls) <= 28 else cls[:26] + '…'
                ax.text(mid, R_LABEL_CLS, label,
                        rotation=rot - 90, rotation_mode='anchor',
                        ha='center', va='center', fontsize=6.5,
                        color='#222')
            cur_a = ca1 + cls_pad

    # ---- Draw Order band (outermost) ----
    for phy, (pa0, pa1) in angles.items():
        classes = tree[phy]
        cls_total = sum(sum(o.values()) for o in classes.values())
        if cls_total == 0:
            continue
        cls_sorted = sorted(classes.items(),
                            key=lambda x: -sum(x[1].values()))
        cur_a = pa0
        cls_pad = np.deg2rad(0.2)
        avail = (pa1 - pa0) - len(cls_sorted) * cls_pad
        if avail < 0:
            avail = (pa1 - pa0)
            cls_pad = 0

        for cls, orders in cls_sorted:
            cls_count = sum(orders.values())
            share = cls_count / cls_total
            span = avail * share
            ca0, ca1 = cur_a, cur_a + span

            # Sub-divide by Order
            ord_sorted = sorted(orders.items(), key=lambda x: -x[1])
            ord_total = sum(orders.values())
            ord_cur = ca0
            ord_pad = 0.0
            for ord_, ocount in ord_sorted:
                oshare = ocount / ord_total if ord_total else 0
                ospan = span * oshare
                oa0, oa1 = ord_cur, ord_cur + ospan
                ord_color = lighten(PHY_COLORS[phy], 0.65)
                n_pts = max(4, int(ospan * 30))
                thetas = np.linspace(oa0, oa1, n_pts)
                ax.fill_between(thetas, R2, R3, color=ord_color,
                                alpha=0.75, edgecolor='white',
                                linewidth=0.2)

                # Label only larger orders
                if ospan > np.deg2rad(0.4):
                    mid = (oa0 + oa1) / 2
                    rot = np.rad2deg(mid)
                    if rot > 90 and rot < 270:
                        rot = rot + 180
                    label = ord_ if len(ord_) <= 30 else ord_[:28] + '…'
                    ax.text(mid, R_LABEL_ORD, label,
                            rotation=rot - 90, rotation_mode='anchor',
                            ha='center', va='center', fontsize=5,
                            color='#444')
                ord_cur = oa1
            cur_a = ca1 + cls_pad

    # Center text
    ax.text(0, 0, 'Robotics\n7,477', ha='center', va='center',
            fontsize=14, weight='bold', color='#222',
            transform=ax.transData._b if hasattr(ax.transData, '_b') else ax.transData)
    # Use polar (0,0) center label via add_artist
    ax.set_ylim(0, R3 + 0.5)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['polar'].set_visible(False)
    ax.grid(False)

    plt.suptitle('Robotics Paper Phylogenetic Tree '
                 '(13 Phylum × Class × Order, 7,261 papers)',
                 fontsize=16, weight='bold', y=0.97)
    plt.figtext(0.5, 0.04,
                'Inner ring: Phylum (color) — Middle: Class — Outer: Order. '
                'Wedge angle ∝ paper count. '
                'Label color: white=Phylum, dark=Class, gray=Order.',
                ha='center', fontsize=10, color='#555')
    plt.tight_layout()
    plt.savefig(FIGS / '05_phylogeny_radial.png',
                dpi=170, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  → {FIGS / '05_phylogeny_radial.png'}")


# ============================================================
# 2) Plotly sunburst (4-level interactive)
# ============================================================
def draw_plotly_sunburst():
    print("\n[2/2] Plotly sunburst (4-level)…")

    # Build flat lists for plotly:
    # ids, labels, parents, values, colors
    ids = []
    labels = []
    parents = []
    values = []
    colors = []

    # Root
    ids.append('root')
    labels.append('Robotics<br>(7,477)')
    parents.append('')
    values.append(0)  # plotly autoss-up
    colors.append('#222')

    for phy in PHYLA:
        if phy not in tree:
            continue
        phy_id = f"phy::{phy}"
        ids.append(phy_id)
        labels.append(phy)
        parents.append('root')
        values.append(0)
        colors.append(PHY_COLORS[phy])

        for cls, orders in tree[phy].items():
            cls_id = f"cls::{phy}::{cls}"
            ids.append(cls_id)
            labels.append(cls)
            parents.append(phy_id)
            values.append(0)
            colors.append(lighten(PHY_COLORS[phy], 0.3))

            for ord_, ocount in orders.items():
                ord_id = f"ord::{phy}::{cls}::{ord_}"
                ids.append(ord_id)
                labels.append(ord_)
                parents.append(cls_id)
                # For Order leaves, use actual count
                # if Genus rules pushed to (general), values just become
                # leaf-count
                # Group by Genus for this order
                genus_sub = Counter()
                for p in papers:
                    if (p['phylum'] == phy and p['class'] == cls
                            and p['order'] == ord_):
                        genus_sub[p['genus']] += 1
                # If only (general) or 1 genus — leaf is order
                if len(genus_sub) <= 1:
                    values.append(ocount)
                    colors.append(lighten(PHY_COLORS[phy], 0.5))
                else:
                    values.append(0)
                    colors.append(lighten(PHY_COLORS[phy], 0.5))
                    # Add genus children
                    for gen, gcount in genus_sub.items():
                        gen_id = f"gen::{phy}::{cls}::{ord_}::{gen}"
                        ids.append(gen_id)
                        labels.append(gen)
                        parents.append(ord_id)
                        values.append(gcount)
                        colors.append(lighten(PHY_COLORS[phy], 0.7))

    # Hover text with breadcrumb
    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues='total',
        marker=dict(colors=colors,
                    line=dict(color='white', width=0.5)),
        hovertemplate='<b>%{label}</b><br>'
                      'Papers: %{value}<br>'
                      'Path: %{currentPath}<extra></extra>',
        maxdepth=3,
    ))
    fig.update_layout(
        title='Robotics Paper Phylogenetic Tree — '
              'Interactive Sunburst (Phylum → Class → Order → Genus)',
        margin=dict(t=80, l=0, r=0, b=0),
        height=900,
        template='plotly_white',
    )
    fig.write_html(INTERACTIVE / '05_phylogeny_sunburst.html')
    print(f"  → {INTERACTIVE / '05_phylogeny_sunburst.html'}")


if __name__ == '__main__':
    draw_radial_phylogeny()
    draw_plotly_sunburst()
    print("\nDone.")
