# Refresh 가이드

이 리포의 산출물은 **RoboPaper Atlas** ([https://gisbi-kim.github.io/robopaper-atlas/](https://gisbi-kim.github.io/robopaper-atlas/))의 데이터 스냅샷에서 파생된다. atlas가 갱신될 때마다 다음이 stale해진다:

- **citation 수** (`cited_by_count`) — OpenAlex가 재인덱싱할 때마다 바뀜
- **DOI / URL** — 새 논문에는 처음엔 DOI가 없다가 나중에 채워지기도 함
- **논문 로스터** — atlas에 새 T-RO/IJRR/RSS 논문이 들어오면 여기 분류 대상에서 빠진 상태가 됨

이 문서는 그 변경사항을 이 리포 (`tro-계통도`) 전반에 전파하는 절차를 정리한 것.

---

## 데이터 흐름

```
┌─────────────────────────────────────────────────────────────┐
│ 1. RoboPaper Atlas (upstream)                               │
│    https://gisbi-kim.github.io/robopaper-atlas/             │
│    └─ robopaper_atlas_all.xlsx                              │
│       (sheet: "papers", ~88k rows)                          │
│       cols: venue, year, title, authors, cited_by_count,    │
│             doi, ee, abstract, …                            │
└─────────────────────────┬───────────────────────────────────┘
                          │ refresh_from_atlas.py
                          │ (title-match + venue/year disambiguation)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. data/intermediate/papers_classified.json                 │
│    7,477 papers  ·  citations 갱신됨                        │
│    cols: idx, venue, year, title, authors, citations,       │
│          phylum, class, order, genus                        │
└─────────┬───────────────────────────┬───────────────────────┘
          │                           │
          ▼                           ▼
   eda/phylogeny_tree.py     eda/eda_plots.py
          │                           │
          ▼                           ▼
   eda/interactive/             eda/figures/*.png
   tree_data.json               eda/interactive/0X_*.html
   (radial 구조)                (정적/인터랙티브 EDA)

┌─────────────────────────────────────────────────────────────┐
│ 3. eda/interactive/papers.json                              │
│    radial viewer 모달이 fetch 하는 슬림 (2.85 MB) 페이로드 │
│    classified.json + atlas의 doi/ee를 join 한 결과          │
│    refresh_from_atlas.py가 같이 생성함                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 표준 refresh 절차

### 1. atlas 다운로드

upstream xlsx를 받는다 (~48 MB):

```bash
curl -L -o /tmp/robopaper_atlas_all.xlsx \
  https://gisbi-kim.github.io/robopaper-atlas/robopaper_atlas_all.xlsx
```

> 이미 `../robopaper atlas/robopaper_atlas_all.xlsx` 또는 `../robopaper atlas/all_enriched.json`이 로컬에 있으면 자동 감지되므로 다운로드 생략 가능.

### 2. citation + DOI 동기화

```bash
python3 refresh_from_atlas.py --xlsx /tmp/robopaper_atlas_all.xlsx
```

이 스크립트가 하는 일:

- atlas의 모든 논문을 normalized title로 인덱싱
- `data/intermediate/papers_classified.json`의 모든 논문에 대해 매칭하여:
  - `citations` 필드를 atlas의 최신값으로 갱신
  - 매칭된 `doi` / `ee`를 함께 사용
- 갱신된 `papers_classified.json`을 in-place로 저장 (taxonomy 라벨은 그대로)
- `eda/interactive/papers.json` (radial viewer 모달용 슬림 페이로드)을 재생성
- atlas에 있지만 분류되지 않은 신규 T-RO/IJRR/RSS 논문 수를 보고 (다음 단계 참조)

### 3. 신규 논문 분류 (필요 시)

위 스크립트가 `⚠ N new T-RO/IJRR/RSS papers in atlas but not in classified set`이라고 알려주면:

```bash
# 1. /tmp/papers.json에 atlas에서 추출한 신규 논문 + 기존 7,477편을 합쳐 둔다
#    (현재 자동화 스크립트는 없음 — 수작업으로 추가하거나
#     classify.py 입력 경로를 조정)
# 2. 분류 실행:
python3 classify.py
# 3. classify.py가 만든 /tmp/classified.json을 data/intermediate/papers_classified.json
#    위치로 옮긴 뒤, refresh_from_atlas.py를 다시 실행해서 DOI/citation 결합
python3 refresh_from_atlas.py --xlsx /tmp/robopaper_atlas_all.xlsx
```

> 보통 한 분기에 수십~수백 편 정도 추가. **기존 분류는 건드릴 필요 없음** — taxonomy는 citation이 아니라 title/abstract에만 의존.

### 4. tree_data + EDA 재생성

분류 결과가 바뀌었거나 citation 수치가 바뀌었으니, 아래 산출물들을 다시 만든다:

```bash
python3 eda/phylogeny_tree.py   # → eda/interactive/tree_data.json (radial viewer 데이터)
python3 eda/eda_plots.py        # → eda/figures/*.png + eda/interactive/0[1-4]_*.html
python3 make_excel.py           # → robotics_taxonomy.xlsx (Excel deliverable)
```

### 5. 확인 + 커밋

로컬에서 `index.html`을 브라우저로 열어 라이브 사이트와 동일한 동작을 확인:

```bash
python3 -m http.server 8000
# → http://localhost:8000/
# → http://localhost:8000/eda/interactive/05_phylogeny_radial_web.html
#   (파이 wedge 클릭 → "이 계열의 논문 N편 보기" → DOI 링크 동작 확인)
```

이상 없으면 변경사항 커밋:

```bash
git add data/intermediate/papers_classified.json \
        eda/interactive/papers.json \
        eda/interactive/tree_data.json \
        eda/interactive/0[1-4]_*.html \
        eda/figures \
        robotics_taxonomy.xlsx
git commit -m "Refresh from RoboPaper Atlas snapshot YYYY-MM-DD"
git push
```

GitHub Pages가 1~2분 안에 라이브 사이트에 반영함.

---

## refresh 빈도 권장

| 트리거 | 작업 |
|---|---|
| atlas가 갱신될 때마다 | 위 1~2번만 (citation/DOI 동기화). 5분 이내 |
| 분기마다 (또는 atlas의 paper count가 눈에 띄게 늘었을 때) | 1~5번 풀 사이클 |
| taxonomy 룰 (`classify.py`, `genus_rules.py`)을 손봤을 때 | classify.py부터 끝까지 다시 |

---

## 트러블슈팅

**"No atlas source found"** → `--xlsx`로 명시적 경로를 주거나, xlsx를 다운로드한 뒤 다시.

**매칭률이 90%대 이하로 떨어짐** → atlas의 title 정규화 방식이 바뀌었을 가능성. `refresh_from_atlas.py`의 `norm()` 함수를 atlas의 매칭 로직과 맞춰야 함.

**citation이 줄어듦 (delta가 음수)** → 정상. OpenAlex가 출처 일부를 제거하거나 중복 제거하면 줄어들 수 있음. 큰 폭으로 줄면 atlas 자체에서 데이터 이슈가 있는지 확인.
