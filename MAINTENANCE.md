**언어**: [English](MAINTENANCE.en.md) | 한국어

# 유지보수 가이드 (Maintenance Guide)

> 이 리포의 산출물 사이에는 의존 관계가 있어서, 한 곳을 고치면 여러 산출물이 같이 stale해진다. 이 문서는 **데이터 출처**, **시점 정보**, 그리고 **언제 무엇을 다시 만들어야 하는지** 정리한다.

빠른 절차만 필요하면 [REFRESH.md](REFRESH.md)를 보면 된다 (citation/DOI 동기화 전용).

---

## 1. 데이터 출처와 커버리지

### 어디서 온 데이터인가

원 데이터는 **RoboPaper Atlas** ([https://gisbi-kim.github.io/robopaper-atlas/](https://gisbi-kim.github.io/robopaper-atlas/))의 스냅샷이다. Atlas는 다음을 통합한 것:

- **DBLP** — 학회/저널 메타데이터
- **OpenAlex** — citation 수, DOI, abstract

### 무엇을 분류했나

Atlas가 다루는 9개 매체 (ICRA / IROS / RA-L / T-RO / RSS / IJRR / Sci-Rob / SoRo / T-Mech) 중에서, **이 리포는 3개만** 추렸다.

| 매체 | 풀네임 | 종류 | 시작 |
|---|---|---|---|
| **T-RO** | IEEE Transactions on Robotics | 저널 | 2004 (T-RA + IJRR 일부 합병) |
| **IJRR** | International Journal of Robotics Research | 저널 | 1982 |
| **RSS** | Robotics: Science and Systems | 학회 | 2005 |

**왜 이 3개인가**: 모두 selectivity가 매우 높고(IJRR/T-RO는 acceptance 30% 이하), peer-review 품질이 안정적이며, 로보틱스 academic research의 *canonical* 영역을 커버. ICRA/IROS는 양은 많지만 품질 분산이 크고, RA-L은 letter format이라 깊이가 다름.

### 시점 정보 (스냅샷 기준)

```
스냅샷 일자:     2025-XX-XX (refresh_from_atlas.py 마지막 실행일)
연도 커버리지:   1988 ~ 2025
논문 수:         7,477편
편당 매체:       T-RO 4,XXX · IJRR 2,XXX · RSS 9XX  (정확한 분포는 robotics_taxonomy.xlsx의 Stats 시트)
```

> **갱신 시 반드시 업데이트할 것**: README의 7,477 카운트, taxonomy.html 칩, 슬라이드, 그리고 이 문서 자체.

### 라이선스 / 출처 표기

분류물은 자유 사용. 원 메타데이터는 DBLP/OpenAlex/Springer/IEEE 각 저작권자에게 귀속.

---

## 2. 의존 관계 맵 — 무엇을 고치면 무엇이 stale해지나

```
            ┌─────────────────────┐
            │  Atlas snapshot     │
            │  (citation·DOI·신규)│
            └─────────┬───────────┘
                      │
                      ▼
       ┌──────────────────────────┐
       │ classify.py + genus_rules│  ← 분류 룰 자체를 수정하면 여기부터 다 다시
       │     (Phylum/Class/Order) │
       └──────────────┬───────────┘
                      │
                      ▼
            data/intermediate/
            papers_classified.json    ──── 7,477 × {P, C, O, G}
                      │
       ┌──────────────┼──────────────────┬───────────────────┐
       │              │                  │                   │
       ▼              ▼                  ▼                   ▼
  eda/phylogeny    eda/eda_plots    make_excel.py     refresh_from_atlas.py
  _tree.py         .py              robotics_         eda/interactive/
  tree_data.json   figures/*.png    taxonomy.xlsx     papers.json
                   interactive/0[1-4].html             (DOI 결합)
       │              │                  │                   │
       └──────────────┴──────────────────┴───────────────────┘
                                │
                                ▼
                   ┌─────────────────────────┐
                   │ 수동 동기화가 필요한 곳 │
                   │  · README.md / .en.md   │
                   │  · taxonomy.html        │
                   │  · TAXONOMY.md          │
                   │  · TAXONOMY_CHANGES.md  │
                   │  · slides/build_slides  │
                   │  · MAINTENANCE.md (본문)│
                   └─────────────────────────┘
```

### 시나리오별 정리

| 변경한 것 | 다시 만들어야 하는 자동 산출물 | 손으로 고쳐야 하는 텍스트 |
|---|---|---|
| **Atlas 스냅샷만 갱신** (citation 수만 바뀜) | `papers_classified.json` (citation 필드만), `papers.json` | 없음 (숫자가 안 바뀜) |
| **Atlas + 신규 논문 추가** (예: 2026년치) | 위 + `tree_data.json` + EDA 전부 + Excel + Slides | `README.md` 카운트, `taxonomy.html` 칩, 본 문서 §1, slides 표지 연도 |
| **Phylum/Class/Order 추가·삭제** (taxonomy 스키마 변경) | `papers_classified.json` 처음부터, 그 이후 전부 | `TAXONOMY.md`, `TAXONOMY_CHANGES.md`, `README.md` Phylum 표, `taxonomy.html` Phylum 타일, `MAINTENANCE.md`, `TAXONOMY_EVALUATION.md` (분포 수치) |
| **Genus 룰만 미세조정** (`genus_rules.py`) | `papers_classified.json`, `tree_data.json`, `papers.json`, Excel | 없음 (보통 분포 수치는 거의 안 변함) |
| **README/문서 텍스트만** | 없음 | 해당 파일 + 영문 미러 |

### 영문 미러 (`.en.md`)

다음 문서들은 한/영 두 벌이 **반드시 같이** 갱신되어야 한다 (사이트 토글이 둘 다 의존):

- `README.md` ↔ `README.en.md`
- `PLAN.md` ↔ `PLAN.en.md`
- `REFRESH.md` ↔ `REFRESH.en.md`
- `TAXONOMY_EVALUATION.md` ↔ `TAXONOMY_EVALUATION.en.md`
- `MAINTENANCE.md` ↔ `MAINTENANCE.en.md` (본 문서)
- `eda/README.md` ↔ `eda/README.en.md`

`TAXONOMY.md`, `TAXONOMY_CHANGES.md`는 영문 미러를 따로 두지 않음 (트리 본문은 코드 식별자라 번역 비대상).

---

## 3. "몇 개월/몇 년 뒤" 시나리오별 체크리스트

### 시나리오 A — 매분기 가벼운 갱신 (citation만 동기화)

**소요시간**: ~10분

```bash
curl -L -o /tmp/atlas.xlsx https://gisbi-kim.github.io/robopaper-atlas/robopaper_atlas_all.xlsx
python3 refresh_from_atlas.py --xlsx /tmp/atlas.xlsx
python3 eda/eda_plots.py            # citation 기반 차트가 있으면 갱신
python3 make_excel.py
git add -A && git commit -m "Refresh from atlas snapshot $(date +%F)" && git push
```

→ 수치는 안 바뀜. README/슬라이드 손댈 필요 없음.

---

### 시나리오 B — 6~12개월 뒤, 새 연도분 논문 추가

**소요시간**: ~1시간

1. **Atlas 다운로드 + 신규 추출**
   ```bash
   curl -L -o /tmp/atlas.xlsx https://gisbi-kim.github.io/robopaper-atlas/robopaper_atlas_all.xlsx
   python3 refresh_from_atlas.py --xlsx /tmp/atlas.xlsx
   # → 콘솔에 "⚠ N new T-RO/IJRR/RSS papers" 표시되면 다음으로
   ```

2. **신규 논문 분류 추가**
   - `data/intermediate/papers_parsed.json`에 신규 논문 append (idx 이어서)
   - `python3 classify.py` 실행 → `data/intermediate/papers_classified.json` 재생성
   - `python3 refresh_from_atlas.py --xlsx /tmp/atlas.xlsx` 다시 실행 (DOI 결합)

3. **모든 다운스트림 재생성**
   ```bash
   python3 eda/phylogeny_tree.py     # tree_data.json
   python3 eda/eda_plots.py          # PNG + interactive HTML
   python3 make_excel.py             # robotics_taxonomy.xlsx
   python3 slides/build_slides.py    # .tex 재생성 (XeLaTeX 컴파일은 별도)
   cd slides && docker run --rm -v "$(pwd):/work" -w /work texlive/texlive:latest \
     bash -c "xelatex -interaction=nonstopmode robotics_phylogeny.tex && \
              xelatex -interaction=nonstopmode robotics_phylogeny.tex"
   cd ..
   ```

4. **수동 동기화 (반드시!)**
   - [ ] `README.md` / `.en.md` — "7,477편" → 새 카운트, "1988~2025" → 새 연도
   - [ ] `taxonomy.html` — chips의 "📦 7,477 papers" 카운트, "Phylum 분포" 표
   - [ ] `MAINTENANCE.md` / `.en.md` — §1의 스냅샷 일자·논문 수 갱신
   - [ ] `TAXONOMY_CHANGES.md` — 새 통독 메모 추가 (선택)
   - [ ] 슬라이드 표지 연도 (build_slides.py가 자동 처리하지만 확인 권장)

5. **확인 + 커밋**
   ```bash
   python3 -m http.server 8000   # localhost:8000에서 라이브 사이트와 동일하게 동작 확인
   git add -A
   git commit -m "Update through $(date +%Y-%m): N new papers, taxonomy stable"
   git push
   ```

---

### 시나리오 C — 새 분류 카테고리 도입 (예: 2027년에 'Embodied AI' Phylum 신설)

**소요시간**: 반나절 ~ 1일

분류 스키마 자체를 바꾸는 것이라, **기존 7,000+편을 모두 재라벨링**해야 한다.

1. **TAXONOMY.md에 새 가지 추가** + 어떤 기준으로 묶을지 정의
2. **TAXONOMY_CHANGES.md에 변경 사유 기록** (왜 추가/삭제했는지)
3. **classify.py + genus_rules.py 룰 추가**
   - 우선순위 주의: 더 specific한 규칙을 위로
4. **재분류 + 검증**
   ```bash
   python3 classify.py
   # 분포 통계 확인 — 신규 Phylum이 합리적 비율인지, 다른 Phylum이 부당하게 줄지 않았는지
   ```
5. **시나리오 B의 3번부터 끝까지 동일 수행**
6. **추가 동기화 (시나리오 B에 더해)**:
   - [ ] `README.md` / `.en.md` — "13개 Phylum" 한 줄 설명 표 갱신, Top 10 Class 표 갱신
   - [ ] `taxonomy.html` — Phylum 타일 그리드 갱신 (HTML 직접 수정), section-eyebrow §2 카운트
   - [ ] `TAXONOMY_EVALUATION.md` / `.en.md` — Phylum 비교표·우리 Phylum 목록 갱신
   - [ ] `PLAN.md` — Phylum 개수
   - [ ] `MAINTENANCE.md` (본 문서) — §1의 매체/카운트 외에도 의존 맵의 분류기 박스 설명 점검

---

## 4. 체크리스트 — 푸시 직전 검증

```
☐ python3 -m http.server 8000 으로 라이브 동일 동작 확인
☐ index.html / taxonomy.html 한↔영 토글이 두 페이지 모두에서 동작
☐ 인터랙티브 트리(05/06)에서 클릭 → 논문 모달 → DOI 링크 클릭 동작
☐ slides/robotics_phylogeny.pdf 가 commit되어 있고 표지 연도가 맞음
☐ robotics_taxonomy.xlsx 가 papers_classified.json 과 row 수 일치
☐ README의 모든 카운트가 papers_classified.json 과 일치
☐ 한↔영 미러 문서가 같이 갱신됨 (README, REFRESH, MAINTENANCE, EVALUATION)
```

---

## 5. 자주 잊는 곳들

| 위치 | 자동 갱신? | 잊으면 일어나는 일 |
|---|---|---|
| `taxonomy.html` Phylum 타일 그리드 (§2) | **수동** | 새 Phylum이 사이트에 안 보임 |
| `taxonomy.html` 칩 카운트 (📦 7,477 papers) | **수동** | 사이트 카운트가 README와 불일치 |
| `MAINTENANCE.md` §1 (본 문서 첫 섹션) | **수동** | "마지막 갱신 언제였더라" 추적 불가 |
| `slides/build_slides.py` 안의 `COHORT_HEADLINES` | **수동** | 슬라이드 내러티브가 옛날 톤 유지 |
| `eda/insights.json` | **반자동** (insights.py) | 차트 캡션이 옛 수치 |
| `TAXONOMY_EVALUATION.md`의 Phylum 분포 % | **수동** | 자체평가 표가 stale |

---

## 6. 관련 문서

- [REFRESH.md](REFRESH.md) — citation/DOI 동기화 절차 (시나리오 A 상세)
- [PLAN.md](PLAN.md) — 최초 작업 플랜 (분류 철학)
- [TAXONOMY.md](TAXONOMY.md) — 13 Phylum × ~100 Class × ~330 Order 트리 본문
- [TAXONOMY_CHANGES.md](TAXONOMY_CHANGES.md) — 트리의 수정 이력
- [TAXONOMY_EVALUATION.md](TAXONOMY_EVALUATION.md) — Springer Handbook 대비 자체평가
- [eda/README.md](eda/README.md) — EDA 차트 별 설명 + 재생성 방법
- [slides/README.md](slides/README.md) — Beamer 빌드 절차

---

*최종 갱신: 본 문서 작성 시점. Atlas 스냅샷 일자와 논문 수는 §1을 직접 갱신할 것.*
