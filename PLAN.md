# 로봇공학 논문 계통도(Phylogenetic Taxonomy) 작성 플랜

## 1. 작업 정의

**입력**: `data.txt` (RoboPaper Atlas, 7,477개 논문 — T-RO/IJRR/RSS, 1988~2025)
**출력**: 엑셀 파일 (.xlsx) — 모든 논문에 대해 시맨틱 계통도 라벨이 부여된 시트
**핵심 요구사항** (task.txt 발췌):
- 단순 단어 분리 + TF-IDF가 아니라, **시맨틱하게** 묶을 것
  - 예: "laser place recognition", "point cloud loop detection" → 둘 다 `Place Recognition / LiDAR-based`
- 생물 계통도처럼 **계층 구조**로 만들 것
- 역사적으로 로봇공학에 어떤 주제가 있었는지 **최대한 많이** 나열할 것

---

## 2. 계통도 설계 (4단계 hierarchy)

생물 분류처럼 4단계로 만든다.

```
Phylum (대분류)  >  Class (중분류)  >  Order (소분류)  >  Genus (세부 계열)
```

### 12개 Phylum (대분류)

1. **Perception & Sensing** — 시각/촉각/거리 센서로 세상 인식
2. **SLAM & Localization** — 위치추정·매핑
3. **Planning** — 경로·임무·작업 계획
4. **Control** — 제어 이론 및 적용
5. **Manipulation** — 조작 (그래스핑, dexterous, deformable 등)
6. **Locomotion** — 이동 (legged, aerial, underwater, …)
7. **Robot Design & Hardware** — 메커니즘·액추에이터·소프트로봇 설계
8. **Human-Robot Interaction** — HRI, 텔레오퍼레이션, 어시스티브
9. **Multi-Robot Systems** — 군집·다중로봇 협조
10. **Learning for Robotics** — RL/IL/Diffusion/VLA 등 데이터 기반
11. **Application Domains** — 의료/농업/자율주행/우주 등 응용 분야
12. **Theoretical Foundations** — 기구학·동역학·최적화·기하

각 Phylum 안에 5~15개 Class, 그 안에 다시 Order, 필요 시 Genus를 둔다.
예시는 `TAXONOMY.md` 파일에 별도로 펼쳐서 정리한다.

### 시맨틱 그룹화 예시 (TF-IDF가 아닌 이유)

| 원 제목 표현 | 묶이는 위치 |
|---|---|
| "laser place recognition" | SLAM&Loc > Place Recognition > LiDAR-based |
| "point cloud loop detection" | SLAM&Loc > Place Recognition > LiDAR-based |
| "VPR with spiking nets" | SLAM&Loc > Place Recognition > Visual-based |
| "global localization for AGV" | SLAM&Loc > Place Recognition (의도가 같음) |
| "VIO with event camera" | SLAM&Loc > SLAM > Event-based VIO/SLAM |
| "lidar-inertial odometry" | SLAM&Loc > SLAM > LiDAR-Inertial Odometry/SLAM |
| "LIO-SAM" / "FAST-LIO" | 같은 곳 (제품명까지 시맨틱 인식) |

---

## 3. 구현 전략

### 3.1 분류 방식

- 각 논문 제목에 대해, **나(Claude)의 도메인 지식으로 작성한** 시맨틱 분류 규칙을 적용한다.
- 규칙은 **우선순위 순**으로 정렬:
  1. 먼저 매우 구체적인 신호 (예: `vision-language-action`, `LIO-SAM`)
  2. 다음 중간 카테고리 (예: `place recognition` + `lidar`)
  3. 마지막 일반 카테고리 (예: 단순히 `manipulation`만 있을 때)
- TF-IDF가 아니라, **동의어 클러스터** + **공기(共起) 패턴** 기반.
  - 예: `LIDAR = ['lidar','laser scan','point cloud','3d point',...]` 처럼
    "같은 의미"의 표현들을 한 묶음으로 정의해두고 사용.

### 3.2 분류 파이프라인

1. `data.txt` → 7,477개 논문 (idx, venue, year, title, authors, citations) 파싱
2. 각 논문 제목에 분류기 적용 → `(Phylum, Class, Order, Genus)` 라벨 부여
3. 분류 분포 통계 확인:
   - Phylum별 개수
   - Class별 개수 (Top 30)
   - 미분류(Unclassified) 개수와 샘플
4. 미분류 / 의심 케이스를 살펴보고 규칙 보강 (1~2회 iteration)
5. 엑셀 출력

### 3.3 엑셀 파일 구조

`robotics_taxonomy.xlsx` (3개 시트):

**Sheet 1: `Papers` — 전체 논문 라벨링 결과**
| idx | venue | year | title | authors | citations | Phylum | Class | Order | Genus |

**Sheet 2: `Taxonomy_Tree` — 계통도 자체**
| Phylum | Class | Order | Genus | Paper Count | Description |

**Sheet 3: `Stats` — 통계 요약**
- Phylum별 논문 수
- 연도별 × Phylum 트렌드 (피벗)
- 미분류 케이스 리스트

---

## 4. 산출물 (이 폴더에 저장)

- `PLAN.md` ← 지금 보고 계신 이 파일
- `TAXONOMY.md` ← 12 Phylum × Class × Order 전체 트리 (작성 예정)
- `classify.py` ← 분류기 스크립트
- `robotics_taxonomy.xlsx` ← 최종 엑셀 결과물
- `classification_stats.txt` ← 분류 통계 (검증용)

---

## 5. 한계 및 가정

- 제목만으로 분류한다 (data.txt에 abstract가 없음). 제목이 모호한 경우 분류 정확도가 떨어질 수 있다.
- 한 논문이 여러 카테고리에 걸칠 수 있으나, **단일 라벨**을 부여한다 (가장 우선순위 높은 규칙이 매칭되는 카테고리). 멀티라벨이 필요하면 추후 확장 가능.
- 미분류는 `Other / Unclassified`로 두고 통계에 포함시켜 사용자가 확인할 수 있게 한다.

---

## 6. 진행 체크포인트

- [ ] 1단계: 플랜 컨펌 ← **지금 여기**
- [ ] 2단계: TAXONOMY.md 작성 (전체 트리 펼치기)
- [ ] 3단계: 분류기 적용 + 통계 확인
- [ ] 4단계: 미분류 보강 (필요 시)
- [ ] 5단계: 엑셀 생성

→ 1단계 컨펌 주시면 2단계로 넘어가겠습니다.
   계통도 구조에서 추가/변경하고 싶은 Phylum이나, 더 깊이 파고 싶은 Class가 있으면 알려주세요.
