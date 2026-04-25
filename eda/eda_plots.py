"""
EDA plot suite (Stage B): visualize raw taxonomy data.

Outputs:
  figures/01_phylum_stack.png        — Phylum × year stacked area
  figures/02_phylum_small_multiples.png — per-Phylum Class breakdown
  figures/03_class_heatmap.png       — all ~95 Classes × year heatmap
  figures/04_top_classes_drill.png   — top-12 Classes Order/Genus drill-down
  interactive/01_phylum_stack.html   — plotly version of #1
  interactive/03_class_heatmap.html  — plotly version of #3
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import numpy as np

import plotly.graph_objects as go
import plotly.express as px

ROOT = Path(__file__).resolve().parent
FIGS = ROOT / 'figures'
INTERACTIVE = ROOT / 'interactive'
FIGS.mkdir(exist_ok=True)
INTERACTIVE.mkdir(exist_ok=True)

DATA_PATH = ROOT.parent / 'data' / 'intermediate' / 'papers_classified.json'

# ---------------- Load ----------------
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    papers = json.load(f)

print(f"Loaded {len(papers)} papers")

# Phylum order (matches TAXONOMY.md)
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
    'Other / Editorial',
    'Other / Unclassified',
]

# Color palette for Phyla — qualitative, distinguishable
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
    'Other / Editorial':            '#bcbd22',
    'Other / Unclassified':         '#7f7f7f',
}

YEARS = list(range(1988, 2026))


# ============================================================
# Plot 1: Phylum stack chart over time
# ============================================================
def plot_1_phylum_stack():
    print("\n[1/4] Phylum stack chart over time…")

    # Count per (year, phylum)
    counts = defaultdict(lambda: defaultdict(int))
    for p in papers:
        counts[p['year']][p['phylum']] += 1

    # Build matrix: rows=Phylum, cols=year
    matrix = np.zeros((len(PHYLA), len(YEARS)), dtype=int)
    for j, y in enumerate(YEARS):
        for i, phy in enumerate(PHYLA):
            matrix[i, j] = counts[y].get(phy, 0)

    # --- Static (matplotlib)
    fig, ax = plt.subplots(figsize=(15, 7))
    bottom = np.zeros(len(YEARS))
    for i, phy in enumerate(PHYLA):
        ax.fill_between(YEARS, bottom, bottom + matrix[i],
                        label=phy, color=PHY_COLORS[phy],
                        alpha=0.9, linewidth=0)
        bottom = bottom + matrix[i]
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Papers per year', fontsize=12)
    ax.set_title('Robotics papers per year, stacked by Phylum '
                 '(T-RO / IJRR / RSS, 7,477 papers)',
                 fontsize=13, weight='bold')
    ax.set_xlim(1988, 2025)
    ax.legend(loc='upper left', fontsize=8, ncol=2,
              bbox_to_anchor=(0.0, 1.0))
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGS / '01_phylum_stack.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  → {FIGS / '01_phylum_stack.png'}")

    # --- Interactive (plotly)
    fig = go.Figure()
    cumulative = np.zeros(len(YEARS))
    for i, phy in enumerate(PHYLA):
        fig.add_trace(go.Scatter(
            x=YEARS,
            y=matrix[i].tolist(),
            mode='lines',
            name=phy,
            stackgroup='one',
            fillcolor=PHY_COLORS[phy],
            line=dict(width=0.5, color='white'),
            hovertemplate=f'<b>{phy}</b><br>Year: %{{x}}<br>Papers: %{{y}}<extra></extra>',
        ))
    fig.update_layout(
        title='Robotics papers per year, stacked by Phylum '
              '(T-RO / IJRR / RSS, 7,477 papers)',
        xaxis_title='Year',
        yaxis_title='Papers per year',
        hovermode='x unified',
        template='plotly_white',
        height=600,
        legend=dict(orientation='v'),
    )
    fig.write_html(INTERACTIVE / '01_phylum_stack.html')
    print(f"  → {INTERACTIVE / '01_phylum_stack.html'}")


# ============================================================
# Plot 2: Per-Phylum small multiples (Class breakdown)
# ============================================================
def plot_2_phylum_small_multiples():
    print("\n[2/4] Per-Phylum small multiples…")

    # For each Phylum, compute Class × year matrix
    phylum_class_year = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for p in papers:
        phylum_class_year[p['phylum']][p['class']][p['year']] += 1

    # Plot 13 panels (skip Other/Unclassified)
    plot_phyla = [p for p in PHYLA if p != 'Other / Unclassified']
    n = len(plot_phyla)
    ncols = 3
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(18, 4.5 * nrows),
                             sharex=True)
    axes = axes.flatten()

    for ax_idx, phy in enumerate(plot_phyla):
        ax = axes[ax_idx]
        classes = phylum_class_year[phy]
        # Sort classes by total count, take top 8 for readability
        cls_totals = {c: sum(year_counts.values())
                      for c, year_counts in classes.items()}
        top_classes = sorted(cls_totals.items(), key=lambda x: -x[1])[:8]
        # Build cumulative stack
        bottom = np.zeros(len(YEARS))
        cmap = plt.cm.tab10
        for i, (cls, _) in enumerate(top_classes):
            yvals = np.array([classes[cls].get(y, 0) for y in YEARS])
            ax.fill_between(YEARS, bottom, bottom + yvals,
                            label=cls[:38] + ('…' if len(cls) > 38 else ''),
                            alpha=0.85, linewidth=0,
                            color=cmap(i % 10))
            bottom = bottom + yvals

        ax.set_title(phy, fontsize=11, weight='bold',
                     color=PHY_COLORS[phy])
        ax.set_xlim(1988, 2025)
        ax.grid(axis='y', alpha=0.3)
        ax.legend(fontsize=7, loc='upper left', framealpha=0.7)
        if ax_idx % ncols == 0:
            ax.set_ylabel('Papers/year')
        if ax_idx >= n - ncols:
            ax.set_xlabel('Year')

    # Hide leftover empty subplots
    for ax in axes[n:]:
        ax.set_visible(False)

    plt.suptitle('Per-Phylum breakdown by Class over time '
                 '(top 8 Classes per Phylum)',
                 fontsize=14, weight='bold', y=1.0)
    plt.tight_layout()
    plt.savefig(FIGS / '02_phylum_small_multiples.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  → {FIGS / '02_phylum_small_multiples.png'}")


# ============================================================
# Plot 3: Class heatmap
# ============================================================
def plot_3_class_heatmap():
    print("\n[3/4] Class heatmap (~95 Classes × year)…")

    # Use 5-year buckets for readability
    bucket_edges = list(range(1988, 2030, 3))
    buckets = []
    for i in range(len(bucket_edges) - 1):
        buckets.append((bucket_edges[i], bucket_edges[i + 1] - 1))

    def year_to_bucket_idx(y):
        for i, (lo, hi) in enumerate(buckets):
            if lo <= y <= hi:
                return i
        return -1

    # Get all (phylum, class) pairs sorted by phylum order, then count desc
    pc_counts = Counter((p['phylum'], p['class']) for p in papers)
    pc_sorted = []
    for phy in PHYLA:
        if phy in ('Other / Unclassified',):
            continue
        in_phy = [(pc, c) for pc, c in pc_counts.items() if pc[0] == phy]
        in_phy.sort(key=lambda x: -x[1])
        pc_sorted.extend(in_phy)

    rows = [pc[0] for pc in pc_sorted]  # (phylum, class) pairs
    nrows = len(rows)
    ncols = len(buckets)

    # Build matrix
    matrix = np.zeros((nrows, ncols), dtype=int)
    for p in papers:
        if p['phylum'] == 'Other / Unclassified':
            continue
        key = (p['phylum'], p['class'])
        if key in rows:
            i = rows.index(key)
            j = year_to_bucket_idx(p['year'])
            if j >= 0:
                matrix[i, j] += 1

    # Plot
    fig, ax = plt.subplots(figsize=(14, max(20, nrows * 0.15)))
    # Use log scale-ish: clip large values
    plot_matrix = np.log10(matrix + 1)
    im = ax.imshow(plot_matrix, aspect='auto', cmap='YlOrRd',
                   interpolation='nearest')

    # X ticks: bucket midpoints
    bucket_labels = [f"{lo}-{hi}" for lo, hi in buckets]
    ax.set_xticks(np.arange(ncols))
    ax.set_xticklabels(bucket_labels, rotation=45, ha='right', fontsize=8)

    # Y ticks: class names with phylum-color coding
    ylabels = [f"{cls}" for (phy, cls) in rows]
    ax.set_yticks(np.arange(nrows))
    ax.set_yticklabels(ylabels, fontsize=6)

    # Color y-axis labels by phylum
    for i, (phy, cls) in enumerate(rows):
        ax.get_yticklabels()[i].set_color(PHY_COLORS[phy])

    ax.set_title(f'Class × year heatmap '
                 f'({nrows} Classes, color=log10(1+count); '
                 f'y-label color = Phylum)',
                 fontsize=12, weight='bold')
    cbar = plt.colorbar(im, ax=ax, label='log10(1 + papers)',
                        fraction=0.025, pad=0.01)
    plt.tight_layout()
    plt.savefig(FIGS / '03_class_heatmap.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  → {FIGS / '03_class_heatmap.png'}")

    # --- Plotly interactive
    raw_matrix = matrix
    hover_text = [[f"{rows[i][1]}<br>{rows[i][0]}<br>"
                   f"{bucket_labels[j]}<br>{raw_matrix[i,j]} papers"
                   for j in range(ncols)] for i in range(nrows)]
    fig = go.Figure(data=go.Heatmap(
        z=plot_matrix,
        x=bucket_labels,
        y=ylabels,
        colorscale='YlOrRd',
        text=hover_text,
        hoverinfo='text',
        colorbar=dict(title='log10(1 + papers)'),
    ))
    fig.update_layout(
        title=f'Class × year heatmap ({nrows} Classes, log color)',
        xaxis_title='Year (3-year bucket)',
        yaxis_title='Class (grouped by Phylum)',
        height=max(800, nrows * 14),
        template='plotly_white',
    )
    fig.write_html(INTERACTIVE / '03_class_heatmap.html')
    print(f"  → {INTERACTIVE / '03_class_heatmap.html'}")


# ============================================================
# Plot 4: Top Classes drill-down (Order/Genus distribution)
# ============================================================
def plot_4_top_classes_drill():
    print("\n[4/4] Top Classes drill-down…")

    # Find top 12 classes by total count (excluding Unclassified)
    cls_counts = Counter()
    for p in papers:
        if p['phylum'] == 'Other / Unclassified':
            continue
        cls_counts[(p['phylum'], p['class'])] += 1

    top12 = cls_counts.most_common(12)

    fig, axes = plt.subplots(4, 3, figsize=(18, 18))
    axes = axes.flatten()

    for ax_idx, ((phy, cls), total) in enumerate(top12):
        ax = axes[ax_idx]
        # Get Order × year matrix for this class
        order_year = defaultdict(lambda: defaultdict(int))
        for p in papers:
            if p['phylum'] == phy and p['class'] == cls:
                order_year[p['order']][p['year']] += 1

        # Top 6 orders
        ord_totals = {o: sum(yc.values()) for o, yc in order_year.items()}
        top_orders = sorted(ord_totals.items(), key=lambda x: -x[1])[:6]

        bottom = np.zeros(len(YEARS))
        cmap = plt.cm.Set3
        for i, (ord_, _) in enumerate(top_orders):
            yvals = np.array([order_year[ord_].get(y, 0) for y in YEARS])
            ax.fill_between(YEARS, bottom, bottom + yvals,
                            label=ord_[:32] + ('…' if len(ord_) > 32 else ''),
                            alpha=0.85, linewidth=0,
                            color=cmap(i % 12))
            bottom = bottom + yvals

        ax.set_title(f"{phy} > {cls}\n({total} papers)",
                     fontsize=10, weight='bold',
                     color=PHY_COLORS[phy])
        ax.set_xlim(1988, 2025)
        ax.grid(axis='y', alpha=0.3)
        ax.legend(fontsize=7, loc='upper left', framealpha=0.7)
        if ax_idx % 3 == 0:
            ax.set_ylabel('Papers/year')
        if ax_idx >= 9:
            ax.set_xlabel('Year')

    plt.suptitle('Top 12 Classes — Order breakdown over time '
                 '(top 6 Orders per Class)',
                 fontsize=14, weight='bold', y=1.0)
    plt.tight_layout()
    plt.savefig(FIGS / '04_top_classes_drill.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  → {FIGS / '04_top_classes_drill.png'}")


# ============================================================
# Run all
# ============================================================
if __name__ == '__main__':
    plot_1_phylum_stack()
    plot_2_phylum_small_multiples()
    plot_3_class_heatmap()
    plot_4_top_classes_drill()
    print("\nDone.")
