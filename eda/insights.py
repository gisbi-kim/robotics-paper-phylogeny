"""
Quantitative insights extraction.

Reads data/intermediate/papers_classified.json and computes:
- Per-Phylum first-year, peak-year, recent-5y growth rate
- Top-cited papers per Phylum / Class
- Hot Class top-10 in 2020-2025 (by paper count)
- "사라진" Classes — strong before 2015, near-zero after 2020
- First-paper-year for emerging categories (VLA, Diffusion, Foundation, etc.)
- Venue × Phylum heatmap (T-RO vs IJRR vs RSS)
- Citation normalization (Phylum mean cite vs overall mean)

Outputs:
  eda/insights.json  — machine-readable
  eda/insights.md    — human-readable summary, used to enrich index.html
"""
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / 'data' / 'intermediate' / 'papers_classified.json'
OUT_JSON = ROOT / 'insights.json'
OUT_MD = ROOT / 'insights.md'

with open(DATA, 'r', encoding='utf-8') as f:
    papers = json.load(f)

TOTAL = len(papers)
print(f"Loaded {TOTAL} papers")

PHYLA_ORDER = [
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

insights = {}

# ============================================================
# 1) Per-Phylum: first year, peak year, recent-5y share
# ============================================================
phy_year_counts = defaultdict(Counter)
for p in papers:
    phy_year_counts[p['phylum']][p['year']] += 1

phy_stats = {}
for phy in PHYLA_ORDER:
    yc = phy_year_counts[phy]
    if not yc:
        continue
    total = sum(yc.values())
    first_year = min(yc.keys())
    peak_year, peak_count = max(yc.items(), key=lambda x: x[1])
    # Recent 5 years (2021-2025) vs prior 5 (2016-2020)
    recent_5 = sum(yc.get(y, 0) for y in range(2021, 2026))
    prior_5 = sum(yc.get(y, 0) for y in range(2016, 2021))
    growth = ((recent_5 - prior_5) / prior_5 * 100) if prior_5 > 0 else None
    phy_stats[phy] = {
        'total': total,
        'first_year': first_year,
        'peak_year': peak_year,
        'peak_count': peak_count,
        'recent_5y_2021_2025': recent_5,
        'prior_5y_2016_2020': prior_5,
        'growth_pct': round(growth, 1) if growth is not None else None,
    }
insights['phylum_stats'] = phy_stats
print("\n=== Phylum stats ===")
for phy, s in phy_stats.items():
    print(f"  {phy}: peak={s['peak_year']} ({s['peak_count']}), "
          f"recent-5y growth={s['growth_pct']}%")

# ============================================================
# 2) Top-cited papers per Phylum
# ============================================================
top_cited = {}
for phy in PHYLA_ORDER:
    in_phy = [p for p in papers if p['phylum'] == phy]
    in_phy.sort(key=lambda p: -p['citations'])
    top_cited[phy] = [
        {
            'title': p['title'],
            'year': p['year'],
            'venue': p['venue'],
            'citations': p['citations'],
            'class': p['class'],
            'order': p['order'],
        }
        for p in in_phy[:5]
    ]
insights['top_cited_per_phylum'] = top_cited
print("\n=== Top-1 cited per Phylum ===")
for phy, lst in top_cited.items():
    if lst:
        p = lst[0]
        print(f"  {phy}: ({p['citations']}) {p['title'][:60]}")

# ============================================================
# 3) Hot Class in 2020-2025 (by recent paper count)
# ============================================================
recent_cls_counts = Counter()
for p in papers:
    if 2020 <= p['year'] <= 2025 and p['phylum'] != 'Other / Unclassified':
        recent_cls_counts[(p['phylum'], p['class'])] += 1
top_recent = recent_cls_counts.most_common(10)
insights['hot_classes_2020_2025'] = [
    {'phylum': phy, 'class': cls, 'count': cnt}
    for (phy, cls), cnt in top_recent
]
print("\n=== Hot Classes 2020-2025 ===")
for (phy, cls), cnt in top_recent:
    print(f"  {cnt:>3}  {phy} > {cls}")

# ============================================================
# 4) "사라진" Classes — high pre-2015, near-zero 2020+
# ============================================================
cls_pre2015 = Counter()
cls_post2020 = Counter()
for p in papers:
    key = (p['phylum'], p['class'])
    if p['year'] < 2015:
        cls_pre2015[key] += 1
    elif p['year'] >= 2020:
        cls_post2020[key] += 1

declined = []
for key, pre_count in cls_pre2015.items():
    post = cls_post2020.get(key, 0)
    if pre_count >= 20 and post <= max(2, pre_count * 0.10):
        ratio = post / pre_count if pre_count > 0 else 0
        declined.append({
            'phylum': key[0],
            'class': key[1],
            'pre_2015_count': pre_count,
            'post_2020_count': post,
            'decline_ratio': round(ratio, 3),
        })
declined.sort(key=lambda x: x['pre_2015_count'], reverse=True)
insights['declined_classes'] = declined[:15]
print("\n=== Declined classes (pre-2015 ≥ 20, post-2020 ≤ 10%) ===")
for d in declined[:10]:
    print(f"  {d['phylum']} > {d['class']}: "
          f"{d['pre_2015_count']} → {d['post_2020_count']}")

# ============================================================
# 5) First-paper-year for emerging categories
# ============================================================
emerging_keywords = {
    'Vision-Language-Action (VLA)': ['vision-language-action', 'vision language action',
                                     ' vla ', 'vla:', 'rt-1', 'rt-2', 'openvla',
                                     'π₀', 'pi-zero', 'octo:', 'navila', 'spatialvla'],
    'Diffusion Policies': ['diffusion polic', 'flow matching', 'diffusion-based polic',
                           'consistency policy'],
    'Foundation Models for Robotics': ['foundation model', 'foundation controller',
                                       'rt-1', 'rt-2', 'openvla'],
    '3D Gaussian Splatting SLAM': ['gaussian splat', 'splatting slam', 'gs-slam',
                                   'pin-slam', 'hi-slam'],
    'Sim-to-Real Legged Locomotion': ['sim-to-real', 'sim to real', 'sim2real'],
    'LiDAR-Inertial Odometry (LIO)': ['fast-lio', 'lio-sam', 'lidar-inertial'],
    'Visual-Inertial Odometry (VIO)': ['vins-mono', 'okvis', 'visual-inertial odometry'],
    'Soft Robotics': ['soft robot', 'soft actuator'],
    'Concentric Tube Robots': ['concentric tube', 'concentric-tube'],
    'Humanoid Whole-Body Control': ['whole-body humanoid', 'whole body humanoid',
                                    'humanoid whole-body', 'humanoid whole body'],
}

emerging = {}
for name, kws in emerging_keywords.items():
    matches = [p for p in papers
               if any(kw in p['title'].lower() for kw in kws)]
    if matches:
        matches.sort(key=lambda p: p['year'])
        first = matches[0]
        cumulative_by_year = Counter(p['year'] for p in matches)
        cum_5y = sum(cumulative_by_year.get(y, 0) for y in range(2021, 2026))
        emerging[name] = {
            'first_year': first['year'],
            'first_title': first['title'],
            'total_matched': len(matches),
            'cum_2021_2025': cum_5y,
        }
insights['emerging_categories'] = emerging
print("\n=== Emerging categories first-year ===")
for k, v in emerging.items():
    print(f"  {k}: first={v['first_year']}, total={v['total_matched']}, "
          f"cum 2021-2025={v['cum_2021_2025']}")

# ============================================================
# 6) Venue × Phylum (T-RO vs IJRR vs RSS color)
# ============================================================
venue_phy = defaultdict(Counter)
for p in papers:
    venue_phy[p['venue']][p['phylum']] += 1

# Normalize to % per venue
venue_phy_pct = {}
for v, counts in venue_phy.items():
    if not v.strip() or '+' in v:
        continue  # skip "T-RO +ICRA" etc
    total_v = sum(counts.values())
    if total_v < 100:
        continue
    venue_phy_pct[v] = {
        phy: round(counts.get(phy, 0) / total_v * 100, 1)
        for phy in PHYLA_ORDER
    }
insights['venue_phylum_pct'] = venue_phy_pct
print("\n=== Venue × Phylum % (top 3 phyla per venue) ===")
for v, pcts in venue_phy_pct.items():
    top3 = sorted(pcts.items(), key=lambda x: -x[1])[:3]
    print(f"  {v}: " + ", ".join(f"{p}={pct}%" for p, pct in top3))

# ============================================================
# 7) Citation normalization
# ============================================================
overall_mean_cite = mean(p['citations'] for p in papers)
overall_median_cite = median(p['citations'] for p in papers)

cite_by_phy = {}
for phy in PHYLA_ORDER:
    cites = [p['citations'] for p in papers if p['phylum'] == phy]
    if cites:
        cite_by_phy[phy] = {
            'n': len(cites),
            'mean': round(mean(cites), 1),
            'median': round(median(cites), 1),
            'mean_vs_overall': round(mean(cites) / overall_mean_cite, 2),
        }
insights['citation_stats'] = {
    'overall_mean': round(overall_mean_cite, 1),
    'overall_median': overall_median_cite,
    'per_phylum': cite_by_phy,
}
print(f"\n=== Citation: overall mean={overall_mean_cite:.1f}, "
      f"median={overall_median_cite} ===")
for phy, s in cite_by_phy.items():
    print(f"  {phy}: mean={s['mean']} (×{s['mean_vs_overall']} of overall)")

# ============================================================
# 8) Year-by-year totals (for normalizing growth)
# ============================================================
year_totals = Counter(p['year'] for p in papers)
insights['year_totals'] = dict(sorted(year_totals.items()))

# ============================================================
# Save
# ============================================================
with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(insights, f, ensure_ascii=False, indent=2)
print(f"\n→ {OUT_JSON}")

# ============================================================
# Markdown summary
# ============================================================
def md_section(title, body):
    return f"## {title}\n\n{body}\n\n"

lines = ['# Quantitative Insights\n']
lines.append(f'_From {TOTAL} classified papers (1988-2025)._\n\n---\n')

# Phylum stats
body = "| Phylum | Total | First | Peak (year, count) | 2016-20 | 2021-25 | Growth |\n"
body += "|---|---:|---:|---|---:|---:|---:|\n"
for phy, s in phy_stats.items():
    g = f"{s['growth_pct']:+.1f}%" if s['growth_pct'] is not None else "—"
    body += (f"| {phy} | {s['total']} | {s['first_year']} | "
             f"{s['peak_year']} ({s['peak_count']}) | {s['prior_5y_2016_2020']} | "
             f"{s['recent_5y_2021_2025']} | {g} |\n")
lines.append(md_section('1. Phylum별 출현·피크·성장률', body))

# Hot classes
body = "**최근 5년 (2021-2025) 최다 논문 Class TOP 10:**\n\n"
for i, h in enumerate(insights['hot_classes_2020_2025'], 1):
    body += f"{i}. **{h['phylum']} > {h['class']}** — {h['count']} papers\n"
lines.append(md_section('2. Hot Classes (2020-2025)', body))

# Declined
body = "**Pre-2015에 활발했지만 Post-2020에 거의 사라진 Class (≥20 → ≤10%):**\n\n"
for d in insights['declined_classes'][:10]:
    body += (f"- {d['phylum']} > {d['class']}: "
             f"{d['pre_2015_count']} → {d['post_2020_count']} "
             f"(retain {d['decline_ratio']*100:.1f}%)\n")
lines.append(md_section('3. 사라진 분야', body))

# Emerging
body = "| Category | First year | First paper | Total matched | 2021-2025 cum |\n"
body += "|---|---:|---|---:|---:|\n"
for k, v in emerging.items():
    body += (f"| {k} | {v['first_year']} | {v['first_title'][:60]}… | "
             f"{v['total_matched']} | {v['cum_2021_2025']} |\n")
lines.append(md_section('4. 신생 카테고리 first paper', body))

# Top cited per Phylum
body = ""
for phy, lst in top_cited.items():
    if not lst:
        continue
    body += f"### {phy}\n"
    for p in lst[:3]:
        body += (f"- **({p['citations']} cites, {p['year']} {p['venue']})** "
                 f"{p['title']} — *{p['class']} > {p['order']}*\n")
    body += "\n"
lines.append(md_section('5. Top-cited per Phylum (top 3)', body))

# Venue
body = "**저널별 Phylum 비중 (top 3):**\n\n"
for v, pcts in venue_phy_pct.items():
    top3 = sorted(pcts.items(), key=lambda x: -x[1])[:3]
    body += f"- **{v}**: " + ", ".join(f"{p} ({pct}%)" for p, pct in top3) + "\n"
lines.append(md_section('6. 저널 (T-RO / IJRR / RSS) 색깔', body))

# Citations
body = "| Phylum | n | Mean cite | Median | × overall mean |\n"
body += "|---|---:|---:|---:|---:|\n"
for phy, s in cite_by_phy.items():
    body += (f"| {phy} | {s['n']} | {s['mean']} | {s['median']} | "
             f"×{s['mean_vs_overall']} |\n")
body += f"\n_Overall mean = {overall_mean_cite:.1f}, median = {overall_median_cite}._\n"
lines.append(md_section('7. 인용수 정규화', body))

with open(OUT_MD, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f"→ {OUT_MD}")
