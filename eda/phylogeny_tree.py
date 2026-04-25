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
from matplotlib.patches import Wedge
import numpy as np

import plotly.graph_objects as go


# ============================================================
# Helpers for cartesian polar drawing (avoid matplotlib polar projection
# pitfalls with text rotation)
# ============================================================
def polar_to_xy(theta_rad, r):
    """N=0, CW polar → cartesian (x, y) with y-up."""
    return r * np.sin(theta_rad), r * np.cos(theta_rad)


def label_rotation_tangential(theta_rad):
    """Tangential (along-arc) text rotation, always upright from outside."""
    bearing = np.rad2deg(theta_rad) % 360
    rotation = -bearing
    while rotation > 180:
        rotation -= 360
    while rotation <= -180:
        rotation += 360
    if rotation > 90:
        rotation -= 180
    elif rotation < -90:
        rotation += 180
    return rotation


def label_rotation_radial(theta_rad):
    """Radial (along-radius, reading outward) text rotation,
    always upright when viewed from outside."""
    bearing = np.rad2deg(theta_rad) % 360
    rotation = 90 - bearing
    while rotation > 180:
        rotation -= 360
    while rotation <= -180:
        rotation += 360
    if rotation > 90:
        rotation -= 180
    elif rotation < -90:
        rotation += 180
    return rotation


def wedge_screen_angles(a0_polar, a1_polar):
    """
    Convert (a0, a1) in our polar (N=0, CW, radians) to matplotlib
    Wedge angles (degrees CCW from +x axis).
    """
    s_start = (90 - np.rad2deg(a1_polar)) % 360
    s_end = (90 - np.rad2deg(a0_polar)) % 360
    if s_end < s_start:
        s_end += 360
    return s_start, s_end

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
    """
    Cartesian-based radial dendrogram with Wedge patches.
    Labels always upright (auto-flip in lower half).
    Saves as SVG (vector, no pixelation) + PDF.
    """
    print("\n[1/2] Radial dendrogram (cartesian, vector output)…")
    fig, ax = plt.subplots(figsize=(20, 20))
    ax.set_aspect('equal')

    # Radial bands
    R0, R1 = 0.55, 1.45   # Phylum band
    R2 = 2.45             # Class band end
    R3 = 3.55             # Order band end
    R_LABEL_PHY = (R0 + R1) / 2
    R_LABEL_CLS = (R1 + R2) / 2
    R_LABEL_ORD = (R2 + R3) / 2

    # Allocate angular space proportional to phy_totals
    angles = {}
    cur = 0.0
    full_angle = 2 * np.pi
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

    # Helper to add a wedge
    def add_wedge(a0, a1, r_inner, r_outer, color,
                  edgecolor='white', linewidth=0.5, alpha=1.0):
        s0, s1 = wedge_screen_angles(a0, a1)
        w = Wedge(center=(0, 0), r=r_outer,
                  theta1=s0, theta2=s1,
                  width=r_outer - r_inner,
                  facecolor=color, edgecolor=edgecolor,
                  linewidth=linewidth, alpha=alpha)
        ax.add_patch(w)

    # ---- Phylum band ----
    for phy, (a0, a1) in angles.items():
        add_wedge(a0, a1, R0, R1, PHY_COLORS[phy],
                  edgecolor='white', linewidth=1.2, alpha=0.95)
        mid = (a0 + a1) / 2
        x, y = polar_to_xy(mid, R_LABEL_PHY)
        rotation = label_rotation_tangential(mid)
        label = phy.replace(' & ', '\n& ')
        ax.text(x, y, label, rotation=rotation,
                ha='center', va='center', fontsize=11, weight='bold',
                color='white')

    # ---- Class band (wedges + selective labels) ----
    # Strategy: draw all Class wedges, but only LABEL the top 3 per Phylum
    # AND only when wedge spans ≥4° (≈ enough room for tangential text).
    # All sub-detail (Order/Genus) lives in the interactive sunburst.
    for phy, (pa0, pa1) in angles.items():
        classes = tree[phy]
        cls_total = sum(sum(o.values()) for o in classes.values())
        if cls_total == 0:
            continue
        cls_sorted = sorted(classes.items(),
                            key=lambda x: -sum(x[1].values()))
        cur_a = pa0
        cls_pad = np.deg2rad(0.15)
        avail = (pa1 - pa0) - len(cls_sorted) * cls_pad
        if avail < 0:
            avail = (pa1 - pa0)
            cls_pad = 0
        cls_color = lighten(PHY_COLORS[phy], 0.4)

        for idx_c, (cls, orders) in enumerate(cls_sorted):
            cls_count = sum(orders.values())
            share = cls_count / cls_total
            span = avail * share
            ca0, ca1 = cur_a, cur_a + span
            add_wedge(ca0, ca1, R1, R2, cls_color,
                      edgecolor='white', linewidth=0.5, alpha=0.92)

            if idx_c < 3 and span > np.deg2rad(4):
                mid = (ca0 + ca1) / 2
                x, y = polar_to_xy(mid, R_LABEL_CLS)
                rotation = label_rotation_tangential(mid)
                label = cls if len(cls) <= 26 else cls[:24] + '…'
                ax.text(x, y, label, rotation=rotation,
                        ha='center', va='center', fontsize=8,
                        color='#1a1a1a', weight='500')
            cur_a = ca1 + cls_pad

    # ---- Order band (wedges only, no labels — too dense for static view) ----
    for phy, (pa0, pa1) in angles.items():
        classes = tree[phy]
        cls_total = sum(sum(o.values()) for o in classes.values())
        if cls_total == 0:
            continue
        cls_sorted = sorted(classes.items(),
                            key=lambda x: -sum(x[1].values()))
        cur_a = pa0
        cls_pad = np.deg2rad(0.15)
        avail = (pa1 - pa0) - len(cls_sorted) * cls_pad
        if avail < 0:
            avail = (pa1 - pa0)
            cls_pad = 0
        ord_color = lighten(PHY_COLORS[phy], 0.65)

        for cls, orders in cls_sorted:
            cls_count = sum(orders.values())
            share = cls_count / cls_total
            span = avail * share
            ca0, ca1 = cur_a, cur_a + span

            ord_sorted = sorted(orders.items(), key=lambda x: -x[1])
            ord_total = sum(orders.values())
            ord_cur = ca0
            for ord_, ocount in ord_sorted:
                oshare = ocount / ord_total if ord_total else 0
                ospan = span * oshare
                oa0, oa1 = ord_cur, ord_cur + ospan
                add_wedge(oa0, oa1, R2, R3, ord_color,
                          edgecolor='white', linewidth=0.2, alpha=0.85)
                ord_cur = oa1
            cur_a = ca1 + cls_pad

    # Center disc + label
    center = mpatches.Circle((0, 0), R0, facecolor='white',
                             edgecolor='#dddddd', linewidth=0.8, zorder=10)
    ax.add_patch(center)
    ax.text(0, 0.06, 'Robotics', ha='center', va='center',
            fontsize=15, weight='bold', color='#1a1a1a', zorder=11)
    ax.text(0, -0.10, f'{overall_total:,} papers', ha='center', va='center',
            fontsize=10, color='#555', zorder=11)

    # Frame
    margin = 0.4
    ax.set_xlim(-R3 - margin, R3 + margin)
    ax.set_ylim(-R3 - margin, R3 + margin)
    ax.axis('off')

    plt.suptitle('Robotics Paper Phylogenetic Tree '
                 f'(13 Phylum × Class × Order, {overall_total:,} papers)',
                 fontsize=16, weight='bold', y=0.96)
    plt.figtext(0.5, 0.05,
                'Inner ring: Phylum (color) · Middle: Class · Outer: Order · '
                'Wedge angle ∝ paper count. Labels always upright.',
                ha='center', fontsize=10, color='#666')
    plt.tight_layout()

    # Save vector formats (no pixelation on zoom)
    svg_path = FIGS / '05_phylogeny_radial.svg'
    pdf_path = FIGS / '05_phylogeny_radial.pdf'
    plt.savefig(svg_path, format='svg', bbox_inches='tight',
                facecolor='white')
    plt.savefig(pdf_path, format='pdf', bbox_inches='tight',
                facecolor='white')
    # Keep PNG fallback for GitHub README preview
    plt.savefig(FIGS / '05_phylogeny_radial.png', dpi=180,
                bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  → {svg_path}")
    print(f"  → {pdf_path}")
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


# ============================================================
# 3) Export tree JSON (for D3.js interactive web viewer)
# ============================================================
def export_tree_json():
    print("\n[3/3] Exporting tree JSON for D3 viewer…")

    # Build hierarchy with Genus as leaf when present (else Order)
    root = {'name': 'Robotics', 'color': '#888', 'children': []}
    for phy in PHYLA:
        if phy not in tree:
            continue
        phy_node = {
            'name': phy,
            'color': PHY_COLORS[phy],
            'children': []
        }
        for cls, orders in sorted(tree[phy].items(),
                                  key=lambda x: -sum(x[1].values())):
            cls_node = {
                'name': cls,
                'color': PHY_COLORS[phy],
                'children': []
            }
            for ord_, ocount in sorted(orders.items(), key=lambda x: -x[1]):
                # Group by Genus
                genus_sub = Counter()
                for p in papers:
                    if (p['phylum'] == phy and p['class'] == cls
                            and p['order'] == ord_):
                        genus_sub[p['genus']] += 1
                ord_node = {
                    'name': ord_,
                    'color': PHY_COLORS[phy],
                }
                if len(genus_sub) > 1:
                    ord_node['children'] = []
                    for gen, gcount in sorted(genus_sub.items(),
                                              key=lambda x: -x[1]):
                        ord_node['children'].append({
                            'name': gen,
                            'color': PHY_COLORS[phy],
                            'value': gcount,
                        })
                else:
                    ord_node['value'] = ocount
                cls_node['children'].append(ord_node)
            phy_node['children'].append(cls_node)
        root['children'].append(phy_node)

    out_path = INTERACTIVE / 'tree_data.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(root, f, ensure_ascii=False)
    print(f"  → {out_path}")


if __name__ == '__main__':
    draw_radial_phylogeny()
    draw_plotly_sunburst()
    export_tree_json()
    print("\nDone.")
