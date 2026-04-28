**언어**: [English](TAXONOMY_EVALUATION.en.md) | 한국어

# 분류 체계 자체 평가: Springer Handbook of Robotics 대비

> 이 문서는 우리가 구축한 4계층 계통도(Phylum > Class > Order > Genus)가 로보틱스 분야의 사실상 표준 레퍼런스인 **Springer Handbook of Robotics** (2008, 2016판)의 목차 구조와 비교해 얼마나 MECE하고 insightful한지 평가한다.

---

## Springer Handbook of Robotics 구조 요약

Handbook은 Siciliano & Khatib이 편집한 로보틱스 분야 최대 종합 레퍼런스로, 두 판에 걸쳐 7-part 구조를 유지하고 있다.

### 2008판 (64챕터, 7개 파트)

```
Part A: Robotics Foundations        — 기구학, 동역학, 메커니즘, 센싱, 모션 계획, 제어
Part B: Robot Structures            — 매니퓰레이터, 평행기구, 다리·바퀴·공중·수중 로봇
Part C: Sensing and Perception      — 비전, 촉각/힘, 음파, GPS, SLAM
Part D: Manipulation and Interfaces — 그래스핑, 조립, 햅틱, 텔레오퍼레이션, HRI
Part E: Mobile & Distributed        — 이동 내비게이션, 다중로봇, 군집, 네트워크
Part F: Field & Service Robotics    — 의료, 광업, 건설, 농업, 우주, 수중
Part G: Human-Centered & Life-like  — 휴머노이드, 소셜, 인지, 바이오 영감, 마이크로봇
```

### 2016판 (83챕터, 동일 7-part + 확장)

동일 구조에 Cloud Robotics, Autonomous Vehicles, Surgical Robotics 등 챕터 추가.

---

## MECE 관점의 비교

### Handbook의 상호배타성(ME) 위반 사례

| 주제 | 중복 파트 | 문제 |
|---|---|---|
| Aerial Robots | Part B (Robot Structures) **&** Part E (Mobile) | 비행 로봇이 "구조"이면서 동시에 "이동 시스템" |
| Underwater Robots | Part B **&** Part F (Field) | 수중 로봇이 구조 챕터와 서비스 챕터 양쪽에 등장 |
| SLAM | Part C (Sensing) **&** Part E (Mobile) | 위치추정이 인식 파트와 이동 파트에 걸침 |
| Medical Robotics | Part D (Manipulation) **&** Part F (Service) | 수술 로봇이 조작 기술이면서 서비스 응용에도 해당 |
| Swarm Robotics | Part E (Distributed) **&** Part G (Bio-inspired) | 군집 행동이 분산 시스템과 생물 영감 양쪽으로 분류 가능 |

**근본 원인:** Handbook의 분류 원칙이 `기술 계층(Part A)` × `로봇 타입(Part B)` × `기능 영역(Part C–E)` × `응용 도메인(Part F–G)`로 **혼재**되어 있다. 한 논문이 여러 파트에 동시에 귀속될 수 있는 구조적 결함이다.

### Handbook의 완전성(CE) 부족

| 누락/부족 영역 | 설명 |
|---|---|
| **Learning for Robotics** | 2008판에 독립 파트 없음. RL·딥러닝이 Part A 뒤편에 흩어짐 |
| **Theoretical Foundations** | 기구학·최적화·Lie 그룹이 Part A "Foundations"에 뭉쳐 있어 수학 이론 계보 불분명 |
| **Foundation Models** | 2016판도 VLA·World Models·Diffusion Policy 반영 불가 (2023+ 트렌드) |
| **SLAM 독립 영역** | 별도 연구 커뮤니티임에도 Sensing 파트에 종속 |

---

## 우리 계통도의 강점

### 1. 분류 원칙 일관성

우리는 **"로봇 연구가 무엇을 가능하게 하는가 (functional capability)"** 라는 단일 원칙으로 모든 Phylum을 정의한다.

```
Phylum                    원칙
─────────────────────────────────────────────────────
Perception & Sensing      → 환경을 감지·인식하는 기술
SLAM & Localization       → 자기위치 추정 및 맵 구축
Planning                  → 행동 계획 수립
Control                   → 실시간 구동 제어
Manipulation              → 물체 조작
Locomotion                → 플랫폼 이동
Robot Design & Hardware   → 물리적 시스템 설계
Human-Robot Interaction   → 인간-로봇 인터페이스
Multi-Robot Systems       → 복수 에이전트 조정
Learning for Robotics     → 학습 기반 역량 획득
Application Domains       → 응용 도메인 (cross-cutting)
Theoretical Foundations   → 수학/이론 기반
Robot Software & Arch.    → 소프트웨어 아키텍처
```

### 2. 우리가 더 잘 포착한 세부 결정들

**SLAM과 Perception의 분리**
- 실제 연구 커뮤니티가 다르고(ICRA SLAM session ≠ 비전 세션), 방법론도 다르다.
- Handbook은 SLAM을 Sensing 파트에 종속시켜 이 차이를 지운다.

**Learning for Robotics를 1등급 Phylum으로 승격**
- 현재 분류 결과 기준으로 7,477편 중 ≈354편(4.7%)이 여기 해당하지만, 2020년대 이후 논문에서는 비중이 급증한다.
- Handbook 2008판은 이 영역을 사실상 무시했고, 2016판도 독립 파트를 부여하지 않았다.

**Application Domains의 명시적 cross-cutting 처리**
- Autonomous Driving·Medical·Space는 "기술"이 아니라 "응용 맥락"이다.
- 별도 Phylum으로 격리함으로써 기술 분류(Perception, Planning…)와 응용 분류가 섞이지 않는다.

**Theoretical Foundations의 독립화**
- 기구학(Kinematics), 동역학(Dynamics), Lie 그룹, 안정성 이론, 형식 검증이 제어·계획 파트에 묻히지 않는다.
- 순수 이론 연구와 응용 연구의 계보를 분리해 추적할 수 있다.

### 3. 2020년대 연구 트렌드 반영

| 트렌드 | 우리 분류 위치 | Handbook에서 |
|---|---|---|
| VLA / π₀ / RT-2 | `Learning > Foundation Models > VLA` | 해당 없음 |
| Diffusion Policy | `Learning > Foundation Models > Diffusion Policies` | 해당 없음 |
| Gaussian Splatting SLAM | `SLAM > Neural Implicit / GS SLAM` | 해당 없음 |
| Event Camera | `Perception > Event-based Vision` | 해당 없음 |
| Safety-Critical Control (CBF) | `Control > Safety-Critical Control` | 해당 없음 |
| Loco-Manipulation | `Manipulation > Mobile Manipulation` | 해당 없음 |

---

## Handbook이 우세한 점 (솔직한 평가)

| 항목 | Handbook 우세 이유 |
|---|---|
| **로봇 타입 직관성** | "Humanoid", "Quadruped", "Aerial" 챕터처럼 로봇 종류별 탐색에 자연스러움 |
| **응용 중심 탐색** | 비전문가가 "Medical Robotics" 찾을 때 직관적 |
| **역사적 계보 서술** | 챕터 단위로 기술 발전사를 서술하는 교과서 용도에 최적화 |
| **총체적 권위** | 164명 집필, peer-review, 업계 표준 레퍼런스 |

그러나 이는 Handbook이 **"책"(pedagogy)** 으로 설계된 결과이고, **7,477편 논문 자동 분류 시스템**으로서는 위의 구조적 결함이 치명적이다.

---

## 결론

우리 4계층 계통도는 Springer Handbook of Robotics 대비 다음 측면에서 우수하다고 평가한다.

1. **MECE** — 분류 원칙이 단일(functional capability)하여 상호배타성 위반이 현저히 적다.
2. **Insightful** — SLAM/Perception 분리, Learning 독립 Phylum, Theoretical Foundations 명시화가 2020년대 연구 지형을 더 정확히 반영한다.
3. **시대성** — Foundation Models, Gaussian Splatting, Event Camera 등 2023+ 트렌드를 분류 체계에 수용했다.

가장 의미 있는 차이는 **Learning for Robotics를 1등급 Phylum으로 가져온 것**이다. Handbook은 두 판 모두 이 영역에 독립적 위상을 부여하지 않았지만, 우리 계통도는 현재 연구의 무게중심을 정확하게 반영한다.

Handbook의 구조가 더 직관적인 측면은 분명 있으나, 그것은 교과서 설계 목표의 산물이다. **5,000편 이상의 논문을 MECE하게 분류하는 목적**에서는 우리 체계가 더 적합하다.

---

*참고: Springer Handbook of Robotics, 2nd ed. (Siciliano & Khatib, 2016), ISBN 978-3-319-32550-7; 1st ed. (2008), ISBN 978-3-540-23957-4.*
