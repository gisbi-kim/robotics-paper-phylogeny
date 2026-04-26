"""
Join the classified 7,477 papers (data/intermediate/papers_classified.json)
with DOI/EE metadata from the upstream RoboPaper Atlas dataset
(robopaper-atlas/all_enriched.json) and emit a slim per-paper JSON
that the radial viewer fetches at runtime.

Match key: normalised title (lowercase, alphanumerics only). On collision,
disambiguate by venue + year. ~99% coverage in practice; the rest fall
back to a Google Scholar search URL on the client.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATLAS = ROOT.parent / 'robopaper atlas' / 'all_enriched.json'
CLASSIFIED = ROOT / 'data' / 'intermediate' / 'papers_classified.json'
OUT = ROOT / 'eda' / 'interactive' / 'papers.json'


def norm(t: str) -> str:
    return re.sub(r'[^a-z0-9]+', '', (t or '').lower()).strip()


def main():
    with open(CLASSIFIED) as f:
        classified = json.load(f)
    with open(ATLAS) as f:
        enriched = json.load(f)

    # Index enriched by normalised title
    idx = {}
    for p in enriched:
        k = norm(p.get('title'))
        if k:
            idx.setdefault(k, []).append(p)

    out = []
    matched = 0
    for c in classified:
        k = norm(c.get('title'))
        cands = idx.get(k, [])
        match = None
        if cands:
            if len(cands) == 1:
                match = cands[0]
            else:
                # disambiguate by venue+year
                cy = str(c.get('year'))
                cv = c.get('venue')
                same = [p for p in cands if str(p.get('year')) == cy and p.get('venue') == cv]
                match = (same or cands)[0]
            matched += 1

        out.append({
            'title':     c.get('title'),
            'authors':   c.get('authors'),
            'year':      c.get('year'),
            'venue':     c.get('venue'),
            'citations': c.get('citations'),
            'phylum':    c.get('phylum'),
            'class':     c.get('class'),
            'order':     c.get('order'),
            'genus':     c.get('genus'),
            'doi':       (match.get('doi') if match else None),
            'url':       (match.get('ee')  if match else None),
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))

    size_mb = OUT.stat().st_size / 1024 / 1024
    print(f'Wrote {OUT.relative_to(ROOT)}: {len(out)} papers, '
          f'{matched} with DOI ({matched/len(out)*100:.1f}%), '
          f'{size_mb:.2f} MB')


if __name__ == '__main__':
    main()
