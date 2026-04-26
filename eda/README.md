**언어**: [English](README.en.md) | 한국어

# EDA — Stage B: Raw Taxonomy Visualization

7,477편 분류 결과를 4개의 정적 플롯 + 2개의 인터랙티브 HTML로 시각화한 1차 분석.

> 시각화 단계: **B (raw 데이터 자체 보기)**.
> 다음 단계 C (생물 계통도 스타일 phylogenetic tree)는 별도.

---

## 산출물

```
eda/
├── eda_plots.py              # 모든 plot 생성 스크립트
├── figures/                  # 정적 PNG (GitHub에서 바로 보임)
│   ├── 01_phylum_stack.png
│   ├── 02_phylum_small_multiples.png
│   ├── 03_class_heatmap.png
│   └── 04_top_classes_drill.png
└── interactive/              # plotly HTML (브라우저로 열어서 hover)
    ├── 01_phylum_stack.html
    └── 03_class_heatmap.html
```

---

## Plot 1 — Phylum × 연도 stack chart

![Phylum Stack](figures/01_phylum_stack.png)

**축**: X = 1988~2025, Y = 연간 논문 수 (stacked).
**색**: 13개 Phylum + Editorial + Unclassified.

**보이는 것**:
- **2004년 점프** — RA-L 이전 시대지만 IJRR + T-RO 합쳐지면서 대폭 증가
- **2017~2020년 정체기** 후 **2021년부터 다시 폭발** — RSS 확대 + AI 시대 진입
- **하늘색 (SLAM&Localization)** 비중이 2005년부터 일관되게 큼
- **녹색계열 (Manipulation+Locomotion)** 이 2010년대 후반 이후 가장 두꺼워짐

**인터랙티브**: [interactive/01_phylum_stack.html](interactive/01_phylum_stack.html) — 호버로 정확한 카운트.

---

## Plot 2 — Per-Phylum small multiples (Class 분해)

![Per-Phylum](figures/02_phylum_small_multiples.png)

**구성**: 13 Phylum 각각에 대해 패널 1개. 각 패널 안에서 **top 8 Class**가 stacked area.

**보이는 것**:
- **SLAM & Localization**: 2005년경 SLAM Class 폭발 (FastSLAM/GraphSLAM era)
- **Locomotion**: 2010년 이후 Aerial Locomotion이 Legged를 따라잡음 (드론 시대)
- **Learning for Robotics**: 2017년부터 등장, 2022~2025년 Foundation Models 폭발
- **Robot Software & Architecture**: 1990년대 후반 잠깐 활성, 2020년대 다시 (Behavior Trees)
- **Theoretical Foundations**: 1990년대 dominant, 2010년 이후 비중 감소
- **HRI**: 점진적 성장, 2020년대 안정적 비중

---

## Plot 3 — Class heatmap (전체 100 Class × 연도)

![Class Heatmap](figures/03_class_heatmap.png)

**축**: 행 = 모든 Class (100개, Phylum 그룹 순서로 정렬), 열 = 3년 bucket.
**색**: log10(1 + 논문 수) — sparse 활동도 보이게 log scale.
**Y라벨 색**: 해당 Class가 속한 Phylum 색 (Plot 1과 일치).

**보이는 것**:
- **상시 활성 Class**: SLAM, Path/Motion Planning, Grasping, Bipedal/Humanoid, Mobile Wheeled — 거의 모든 시대 빨갛게
- **최근 부상**: Foundation Models, Diffusion Policies, Aerial Swarms, 3D Scene Graph (오른쪽 끝 buckets만 빨강)
- **사라진 분야**: 일부 1990년대 mechanism design은 최근 색이 옅어짐
- **전체 패턴**: 오른쪽으로 갈수록 전반적으로 진해짐 = 출판량 자체 증가

**인터랙티브**: [interactive/03_class_heatmap.html](interactive/03_class_heatmap.html) — 호버로 정확한 카운트 + Class 이름 풀버전.

---

## Plot 4 — Top 12 Class 드릴다운 (Order 분해)

![Top Classes Drill](figures/04_top_classes_drill.png)

**구성**: 가장 큰 12개 Class에 대해 각각 mini panel. 내부에서 **top 6 Order**가 stacked area.

**보이는 것**:
- **SLAM**: General SLAM (초기) → Visual SLAM/Odometry (2010년대) → LIO/VIO/Multi-modal (최근)
- **Path/Motion Planning**: Sampling-based (RRT) → 다양화 → 최근 Trajectory Optimization 부상
- **Grasping**: 2010년대 중반부터 Learning-based가 Force-Closure를 추월
- **Bipedal**: ZMP → HZD → Sim-to-Real RL로 패러다임 전환
- **Foundation Models**: 통째로 2022년 이후 신생 — VLA / Diffusion / LLM이 거의 동시에 등장

---

## 재현

```bash
cd "this-repo"
python3 eda/eda_plots.py
# → eda/figures/*.png + eda/interactive/*.html
```

> 의존성: `matplotlib`, `plotly`.

---

## 다음 단계

**C — Phylogenetic tree (생물 계통도 스타일)**: 위 4개 plot은 "데이터 분석용"인 반면, C는 "한 장으로 임팩트". 13 Phylum × Class × Order × Genus 전체 트리를 가지치기 형태로 그려서 task.txt 원래 의도(생물들 계통도처럼)를 살리는 것.
