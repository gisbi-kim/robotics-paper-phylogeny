"""
Refresh citations + DOI links from RoboPaper Atlas.

Citations (cited_by_count) and the paper roster on the upstream atlas
shift over time as OpenAlex re-indexes. This script pulls the latest
snapshot and propagates it down through this repo's outputs:

  RoboPaper Atlas xlsx  ──(title match)──▶  data/intermediate/
                                              papers_classified.json
                                              (citations refreshed)
                                                    │
                                                    ▼
                                            eda/interactive/
                                              papers.json
                                              (DOI + citations for the
                                               radial viewer's modal)

What this DOES update:
- citations on every matched paper
- DOI / url for every matched paper

What this does NOT do (run these manually after — see REFRESH.md):
- assign taxonomy to papers added since the last classify.py run
- regenerate tree_data.json / EDA figures (eda/phylogeny_tree.py,
  eda/eda_plots.py)
- regenerate the Excel deliverable (make_excel.py)

Usage:
    python3 refresh_from_atlas.py
    python3 refresh_from_atlas.py --xlsx /path/to/robopaper_atlas_all.xlsx
    python3 refresh_from_atlas.py --enriched /path/to/all_enriched.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLASSIFIED = ROOT / 'data' / 'intermediate' / 'papers_classified.json'
PAPERS_OUT = ROOT / 'eda' / 'interactive' / 'papers.json'
DEFAULT_XLSX = ROOT.parent / 'robopaper atlas' / 'robopaper_atlas_all.xlsx'
DEFAULT_JSON = ROOT.parent / 'robopaper atlas' / 'all_enriched.json'

VENUES = {'T-RO', 'IJRR', 'RSS'}  # the three this taxonomy was built on


def norm(t: str) -> str:
    return re.sub(r'[^a-z0-9]+', '', (t or '').lower()).strip()


def load_atlas_xlsx(path: Path) -> list[dict]:
    """Read the 'papers' sheet of robopaper_atlas_all.xlsx."""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb['papers']
    rows = ws.iter_rows(values_only=True)
    header = list(next(rows))
    out = []
    for r in rows:
        rec = dict(zip(header, r))
        out.append({
            'venue':            rec.get('venue'),
            'year':             rec.get('year'),
            'title':            rec.get('title'),
            'authors':          rec.get('authors'),
            'cited_by_count':   rec.get('cited_by_count'),
            'doi':              rec.get('doi'),
            'ee':               rec.get('ee'),
        })
    return out


def load_atlas_json(path: Path) -> list[dict]:
    with open(path) as f:
        return json.load(f)


def load_atlas(args) -> list[dict]:
    """Pick xlsx or json per CLI flags / availability."""
    if args.xlsx:
        return load_atlas_xlsx(Path(args.xlsx))
    if args.enriched:
        return load_atlas_json(Path(args.enriched))
    if DEFAULT_JSON.exists():
        print(f'Using local {DEFAULT_JSON.name}')
        return load_atlas_json(DEFAULT_JSON)
    if DEFAULT_XLSX.exists():
        print(f'Using local {DEFAULT_XLSX.name}')
        return load_atlas_xlsx(DEFAULT_XLSX)
    sys.exit(
        'No atlas source found. Either:\n'
        '  - download the xlsx from '
        'https://gisbi-kim.github.io/robopaper-atlas/robopaper_atlas_all.xlsx\n'
        '    and pass it with --xlsx PATH, or\n'
        '  - place all_enriched.json next to this repo at\n'
        f'    {DEFAULT_JSON}'
    )


def index_by_title(papers: list[dict]) -> dict[str, list[dict]]:
    idx: dict[str, list[dict]] = {}
    for p in papers:
        k = norm(p.get('title'))
        if k:
            idx.setdefault(k, []).append(p)
    return idx


def pick_match(cands: list[dict], year, venue) -> dict:
    if len(cands) == 1:
        return cands[0]
    same = [p for p in cands
            if str(p.get('year')) == str(year) and p.get('venue') == venue]
    return (same or cands)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--xlsx', help='Path to robopaper_atlas_all.xlsx')
    ap.add_argument('--enriched', help='Path to all_enriched.json')
    args = ap.parse_args()

    atlas = load_atlas(args)
    print(f'Loaded {len(atlas):,} atlas papers')

    with open(CLASSIFIED) as f:
        classified = json.load(f)
    print(f'Loaded {len(classified):,} classified papers')

    idx = index_by_title(atlas)

    matched = 0
    refreshed_citations = 0
    citation_delta_total = 0
    out_papers = []

    for c in classified:
        m = None
        cands = idx.get(norm(c.get('title')), [])
        if cands:
            m = pick_match(cands, c.get('year'), c.get('venue'))
            matched += 1

        # Refresh citations on the classified record (keeps taxonomy as-is).
        # Coerce both sides to int — atlas occasionally serialises numbers
        # as strings depending on the source path.
        if m and m.get('cited_by_count') is not None:
            try:
                new_c = int(m['cited_by_count'])
            except (TypeError, ValueError):
                new_c = None
            if new_c is not None:
                try:
                    old_c = int(c.get('citations') or 0)
                except (TypeError, ValueError):
                    old_c = 0
                if new_c != old_c:
                    citation_delta_total += (new_c - old_c)
                    refreshed_citations += 1
                    c['citations'] = new_c

        # Build the slim per-paper record for the radial viewer modal
        out_papers.append({
            'title':     c.get('title'),
            'authors':   c.get('authors'),
            'year':      c.get('year'),
            'venue':     c.get('venue'),
            'citations': c.get('citations'),
            'phylum':    c.get('phylum'),
            'class':     c.get('class'),
            'order':     c.get('order'),
            'genus':     c.get('genus'),
            'doi':       (m.get('doi') if m else None),
            'url':       (m.get('ee')  if m else None),
        })

    # Write back classified.json (in-place: same field order)
    with open(CLASSIFIED, 'w') as f:
        json.dump(classified, f, ensure_ascii=False, indent=1)

    # Write the slim viewer payload
    PAPERS_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(PAPERS_OUT, 'w') as f:
        json.dump(out_papers, f, ensure_ascii=False, separators=(',', ':'))

    # Detect new atlas papers (T-RO/IJRR/RSS) that have NO classified entry
    classified_titles = {norm(c.get('title')) for c in classified}
    new_in_scope = [p for p in atlas
                    if p.get('venue') in VENUES
                    and norm(p.get('title')) not in classified_titles]

    pct = matched / len(classified) * 100
    out_mb = PAPERS_OUT.stat().st_size / 1024 / 1024
    print()
    print(f'Matched   : {matched:,}/{len(classified):,} ({pct:.1f}%)')
    print(f'Citations : {refreshed_citations:,} papers updated '
          f'(net delta: {citation_delta_total:+,})')
    print(f'Wrote     : {CLASSIFIED.relative_to(ROOT)}')
    print(f'Wrote     : {PAPERS_OUT.relative_to(ROOT)} ({out_mb:.2f} MB)')

    if new_in_scope:
        print()
        print(f'⚠  {len(new_in_scope)} new T-RO/IJRR/RSS papers in atlas '
              f'but not in classified set.')
        print('   Run classify.py to label them, then re-run this script.')
        print('   First few:')
        for p in new_in_scope[:5]:
            print(f"     · {p['venue']} {p['year']}: {p['title'][:80]}")

    print()
    print('Next steps (manual):')
    print('  - python3 eda/phylogeny_tree.py   # rebuild tree_data.json + figures')
    print('  - python3 eda/eda_plots.py        # rebuild EDA figures')
    print('  - python3 make_excel.py           # rebuild robotics_taxonomy.xlsx')


if __name__ == '__main__':
    main()
