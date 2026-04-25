# TAXONOMY 변경 내역 (Pre-Reading vs Post-Reading)

7,477개 논문 제목을 1988~2025 시간순으로 전부 읽고, 초안 [TAXONOMY.md](TAXONOMY.md)와 비교한 결과를 정리합니다.

> 결론: 12 Phylum 골격은 유효하나, 누락된 1개 Phylum 추가 (`Robot Software & Architecture`), 8개 Phylum 안에 새 Class 또는 Order를 28건 추가/재구성, 2건 이름 변경, 6건 Order 통합/분리.

---

## 1. 새로 추가한 **Phylum**

### 13. Robot Software & Architecture (신규) ⭐
- **왜 추가하나?** 초안에는 완전 누락. 실제 데이터에는 1990년대부터 일관된 흐름이 있음:
  - 1990s-2000s: "ControlShell", "ORCCAD", "OpenHRP", "MRROC++", Petri-net 기반 코드 생성, 로봇 프로그래밍 toolkits
  - 2010s: KnowRob, ROS 기반 frameworks, "Architecture for Autonomy"
  - 2020s: Behavior Trees (BT), SymForce, RelaxedIK, Kubernetes orchestration
- **Class 구성**:
  - Robot Architecture / Middleware
  - Behavior Trees / Reactive Architectures
  - Robot Programming / DSL
  - Code Generation / Symbolic Computation (예: SymForce)
  - Real-time Systems / Scheduling

---

## 2. **Class** 또는 **Order** 추가/재구성 (Phylum별)

### Phylum 1. Perception & Sensing — 추가/조정

- **`Tactile Sensing` Class를 큰 폭으로 강화**: 초안엔 "Tactile Sensors / Algorithms" 한 Order뿐. 실제로는 다음을 분리해야 함:
  - GelSight / Vision-based Tactile (광학 기반)
  - Capacitive / Resistive Tactile Skin
  - Event-based Tactile (Evetac 등)
  - Electrical Impedance Tomography (EIT) Skin
  - Tactile Servoing (perception-action loop)
  - **이유**: 2008-2025 사이 ~150편 이상이 이 분야. GelSight, Evetac 등 distinctive sub-areas.

- **`Visual Perception` 안에 추가할 Order**:
  - Active Perception / Active Vision (정적 perception과 별도. 1990s부터 흐름)
  - Visuo-Tactile Fusion (V-HOP, ViTaSCOPE 등 modern)
  - Foundation Models for Perception (CLIP-Fields, ConceptFusion, Octopi)

- **`LiDAR Perception` 안에 추가**:
  - Doppler / Velocity-aware Processing (DICP, DRO 같은 doppler radar/lidar)

- **`Multi-modal Perception` 강화**:
  - Visual + IMU + LiDAR + Radar + GNSS Fusion (modern era)
  - Open-vocabulary / Foundation 기반 perception을 별도 Order로

### Phylum 2. SLAM & Localization — 추가/조정

- **`SLAM` Class 안에 추가**:
  - **Neural Implicit / Gaussian Splatting SLAM** (PIN-SLAM, GS-LIVO, HI-SLAM2, VINGS-Mono, MISO 등 2023+) — 새로운 SLAM 패러다임이라 별도 Order로
  - **Multi-LiDAR / Multi-IMU / Multi-Camera SLAM** (FAST-LIVO2, MIMC-VINS, GVINS, MARS-LVIG 등)
  - **Underwater / Marine SLAM** (AQUA-SLAM, SVIn2 등)
  - **Continuous-time SLAM** (Gaussian Process priors 기반, Barfoot 계열)

- **`Place Recognition` 안에 추가**:
  - **Cross-modal Place Recognition** (i3dLoc, CMRNext: 카메라↔라이다 매칭) — 명시
  - Foundation-model-based VPR (CLIP/ConvNet 기반)

- **`Localization` 안에 추가**:
  - **Radio / UWB / WiFi based Localization** (UTIL dataset 등)
  - **Range-only SLAM / Acoustic Beacon localization**
  - **Map-free Visual Localization** (modern image retrieval-based)

### Phylum 3. Planning — 추가/조정

- **`Path/Motion Planning` 안에 추가**:
  - **Convex Decomposition / Graphs of Convex Sets** (Tedrake 계열, 2022+)
  - **Diffusion-based Planning** (Motion Planning Diffusion 등 2024+)
  - **Learning-based Motion Planning / Neural MP** (MPNet, iPlanner, NeuPAN)

- **`Navigation` 안에 추가**:
  - **Off-road / Unstructured Terrain Navigation** (이미 언급했지만 강화 — STEP, EVORA, TerrainNet, Verti-Bench 등 modern)
  - **Vision-Language Navigation** (NaVid, NaVILA, Uni-NaVid: 2024+, VLM-기반)
  - **Object-goal / Embodied Navigation** (GOAT, SEEK 등)

- **`Belief Space Planning` 안에 추가**:
  - **Active SLAM / Active Perception Planning** (별개로 강조)

- **`Specialized Planning` 안에 추가**:
  - **Multi-Robot Path Finding (MAPF)** (CBSS, Conflict-based search 등) — 초안에는 Multi-Robot Phylum에 있었으나 알고리즘적으로는 Planning에도 위치
  - **Inspection / Coverage Planning for 3D structures** (TARE, RACER, FALCON: Aerial exploration)

### Phylum 4. Control — 추가/조정

- **`Optimal / Predictive Control` 안에 추가**:
  - **Contact-Implicit MPC** (별도 Order, 2018+ 폭발적)
  - **Sampling-based MPC / MPPI** (modern, MPPI variants)
  - **Information-Theoretic MPC**

- **`Learning-based Control` 안에 강화/추가**:
  - **Koopman Operator-based Control** (별도 Order, Koopman 계열 다수)
  - **Differentiable Physics / Differentiable Simulators** (DiSECt, DiffTune 등)
  - **Neural ODE / Hamiltonian Networks** (modern)

- **`Safety-Critical Control` 안에 강화**:
  - **Neural CBF / Learned Lyapunov / Contraction** (BarrierNet, Lyapunov NN, contraction theory 계열)

- **새 Class 신설: `Bio-inspired Control`**:
  - Central Pattern Generators (CPG) — 초안에 누락
  - Limit Cycle / Hopf Oscillator-based Control
  - Phase Reset / Entrainment-based Control

### Phylum 5. Manipulation — 추가/조정

- **`Grasping` 안에 추가**:
  - **Caging-based Grasping** (별도 Genus — Rimon/Burdick 계열, "From Caging to Grasping" 등)
  - **Foundation-model Grasping** (AnyGrasp, Dex-Net 계열)
  - **Whole-arm / Whole-body Grasping**
- **`Dexterous Manipulation` 안에 추가**:
  - **Dexterous Manipulation with Tactile** (Tactile Roller Grasper, RoTipBot 등)
  - **Foundation Controllers** (DexterityGen — 새 패러다임)
  - **Learning Dexterity from Human Videos** (DexCap, DexWild, ScrewMimic, Robotic Telekinesis)
- **`Contact-rich Manipulation` 안에 추가**:
  - **Liquid / Granular Material Manipulation** (DextAIRity, RoboCraft, RoboNinja, GranularGym)
  - **Knot Tying / Cable Manipulation** (별도 Order — 2008부터 일관된 흐름)
- **신규 Class: `Distributed Manipulation`**:
  - Programmable Force Fields (Bohringer/Donald 계열)
  - Vibratory Parts Feeders / Parts Orienting
  - Air-flow / Surface-based Distributed Manipulation
  - **이유**: 1990s-2000s에 큰 흐름이었고 응용(parts feeding) 계열도 여기.
- **신규 Class: `Mobile Manipulation`** (이미 있지만 강화):
  - Loco-Manipulation (legged 로봇 + arm — 2020s 폭증)
  - Whole-body Mobile Manipulation
  - VLA-based Mobile Manipulation (OK-Robot, RT-2, Vid2Robot 등)

### Phylum 6. Locomotion — 추가/조정

- **`Legged Locomotion` 안에 추가**:
  - **Hybrid Wheel-Leg** (TurboQuad, WaLTR, Wheel Transformer — 별도 Order)
  - **Underwater Legged** (water strider, walking underwater)

- **`Aerial Locomotion` 안에 추가**:
  - **Aerial Manipulation Platform** (T-RO 2022 survey + 다수) — Manipulation과 cross-cut지만 platform 측면에서는 여기
  - **Insect-scale / Pico Aerial Robots** (RoboBee, RoboFly: 별도 Order)
  - **Hybrid Aerial-Aquatic / Aerial-Terrestrial** (HyTAQ, Dipper, Ringbot)

- **`Bio-inspired Locomotion` 안에 추가**:
  - **Sand-swimming / Granular Locomotion** (sandfish, locust 등)
  - **Crawling / Inchworm Robots** (다수)

### Phylum 7. Robot Design & Hardware — 추가/조정

- **`Soft Robotics` 안에 추가**:
  - **HASEL / Dielectric Elastomer (DEA)** (modern actuators)
  - **Twisted Coiled Polymer (TCP) / Artificial Muscle**
  - **Vine / Growing Robot** (별도 — soft growing robots are distinct)

- **`Mechanism Design` 안에 추가**:
  - **Tensegrity Robots** (별도 Order — 초안에서 누락)
  - **Hybrid Rigid-Soft Mechanisms**

- **`Continuum Robot` 안에 강화**:
  - **Concentric Tube Robots** (별도 Order — 의료용으로 큰 흐름)
  - **Magnetic Continuum Robots** (modern)

- **`Microrobotics` 안에 강화**:
  - **Magnetic Microrobots / Swarms** (별도 Order — 2010s-2025 크게 성장)
  - **Catalytic / Chemically-driven Microrobots**
  - **MRI-driven / MR-compatible Robots** (별도 Order)
  - **Bio-hybrid Magnetotactic Bacteria**

- **`Actuators` 안에 추가**:
  - **Variable Stiffness Actuators (VSA)** (별도 Order — 2010s 큰 흐름)
  - **Magnetorheological Actuators**
  - **Electrostatic Actuators (electroadhesion, capacitive)**

### Phylum 8. Human-Robot Interaction — 추가/조정

- **`Assistive Robotics` 안에 추가**:
  - **Soft Exosuit / Wearable Soft Robots** (별도 Order: Harvard Soft Exosuit, Pisa SoftHand-Pro 계열)
  - **Hand Exoskeletons** (별도 Order)
  - **Brain-Machine Interface (BMI/BCI) controlled robots** (EEG, EMG, P300)

- **`Teleoperation` 안에 강화**:
  - **Bilateral Teleoperation Stability** (별도 Genus — Niemeyer/Slotine 계열, 30+ years of work)
  - **VR/AR Teleoperation** (modern: AnyTeleop, Tilde, Open-Teach)
  - **In-the-Wild Teleoperation** (Universal Manipulation Interface)

- **신규 Class: `Haptic Devices & Rendering`** (초안에는 Teleop 안에 들어있었지만 분리):
  - Haptic Display / Force-feedback Devices
  - Haptic Rendering Algorithms (passivity, stability)
  - Wearable Haptic Feedback (vibrotactile, electrotactile)
  - Cobotic / Hand Controllers

### Phylum 9. Multi-Robot Systems — 추가/조정

- **`Coordination` 안에 추가**:
  - **Multi-Robot Pursuit-Evasion / Surveillance** (별도 Order — 알고리즘적 robotics 핵심 주제)
  - **Multi-Robot Adversarial / Resilient (Byzantine)** (modern: 2020s)

- **`Multi-Robot Planning` 안에 강화**:
  - **Multi-Agent Path Finding (MAPF) / Conflict-Based Search** (별도 Order)

- **`Distributed Algorithms / Optimization` 강화**:
  - **Distributed Bundle Adjustment / Distributed Pose Graph** (Decentralized SLAM, Kimera-Multi, iMESA, DABA)
  - **Distributed Certifiably Correct Optimization**

- **신규 Class: `Aerial Swarms / UAV Swarms`** (초안엔 Aerial Locomotion 안에 있었지만 multi-robot 측면 강함):
  - Decentralized Aerial Swarm (Omni-Swarm, Swarm-LIO2)
  - Communication-aware Swarm
  - Drone Defense / Herding

### Phylum 10. Learning for Robotics — 추가/조정

- **`Foundation Models` 안에 강화/추가**:
  - **Vision-Language-Action (VLA)** (별도 Order — RT-1, RT-2, π₀, OpenVLA, NaVILA, SpatialVLA, Octo)
  - **LLM-based Reasoning / Planning** (SayCan, CLIP-RT, DrEureka, MOKA)
  - **Diffusion Policies / Flow Matching** (Diffusion Policy, 3D Diffusion Policy, Consistency Policy, RDT, IMLE Policy 등)
  - **Generalist Robot Policies** (Octo, OpenVLA, Cross-embodiment)

- **`Imitation Learning` 강화**:
  - **In-the-Wild / From-Human-Video IL** (DexCap, DexWild, ScrewMimic, AVID, DROID, BridgeData)
  - **Programming by Demonstration (PbD)** — 1990s부터의 흐름. Imitation Learning의 historical root로 명시

- **`Reinforcement Learning` 강화**:
  - **Sim-to-Real for Legged Locomotion** (Anymal, Cassie, Berkeley Humanoid, ASAP — 2020s 강력한 흐름)
  - **Safe RL / Constrained RL**
  - **RL for Manipulation** (Quantile QT-Opt, IndustReal, AutoMate)

- **신규 Class: `Datasets & Benchmarks & Simulators`** (이미 있지만 modern era에 폭증):
  - Robot Manipulation Datasets (DROID, BridgeData, RoboMIND, DexCap)
  - Simulators (MuJoCo Playground, ManiSkill3, RoboCasa, RoboVerse)
  - Benchmarks (FurnitureBench, COLOSSEUM, HumanoidBench)

### Phylum 11. Application Domains — 추가/조정

- **`Medical & Surgical Robotics` 안에 추가**:
  - **Microsurgery / Neurosurgery** (Micron, MRI-compatible neurosurgical 등)
  - **Beating Heart Surgery / Motion Compensation**
  - **Capsule Endoscopy / Magnetic Capsule** (별도 Order)
  - **Rehabilitation Robotics** (이미 HRI/Assistive에 있지만 Application도 cross-cut)

- **`Field Robotics` 안에 추가**:
  - **Underwater Field Robotics / Hull Inspection / Cave Exploration** (CavePI, AQUA-SLAM 등)
  - **Forestry / Under-canopy Navigation** (CropFollow++, agricultural)
  - **Lunar / Mars (separate from Space Robotics?)** — 함께 두는 게 적절

- **신규 Class: `Computational Biology Robotics`**:
  - Protein Folding / Molecular Motion Planning (IJRR special issue 다수)
  - DNA Origami / Bio-mechanical Modeling
  - **이유**: 2005-2015 사이 ~30+ 편이 IJRR에 등장

- **`Service Robotics` 안에 추가**:
  - **Food Service / Cooking Robotics** (Robot Cutting, FLAIR feeding 등 modern)
  - **Retail / Warehouse 자율 매장**

### Phylum 12. Theoretical Foundations — 큰 변화 없음

- **`Geometric Methods` 안에 강화**:
  - **Lie Group IMU Preintegration** (별도 Genus — 강한 sub-theme)
  - **Equivariant Methods** (modern: equivariant transporter, NeuSE 등)

- **`Optimization` 안에 추가**:
  - **Distributed Optimization** (이미 Multi-Robot에 있지만 cross-cut)
  - **Differentiable Programming** (modern: PROX-QP, ProxDDP, SymForce)
  - **Semidefinite Relaxations / Certifiable Optimization** (TEASER, SE-Sync, certifiable pose)

- **신규 Class: `Robot Safety & Failure`**:
  - Robot Collision Detection (Survey 2017 De Luca)
  - Failure Detection / Anomaly Detection
  - Fault Tolerance (manipulator, multi-robot)
  - Resilience (Byzantine, attack-resilient)

---

## 3. **이름 변경**

| 초안 | 최종 |
|---|---|
| Foundation Models (LLM/VLM/VLA) | Foundation Models for Robotics (3 Orders 명시) |
| Manipulation > Generic Manipulation | Manipulation > General Manipulation (단어 통일) |

---

## 4. **통합/분리** 결정

- **통합**: `Inertial Odometry` (혼자 Order로 두기엔 적음) → `Visual-Inertial / LiDAR-Inertial` 안에 합침
- **통합**: `Smart Materials (SMA, EAP)` → `Soft Robotics > Soft Actuators`로 흡수
- **분리**: `Concentric Tube Robots` → `Continuum Robot`에서 별도 Order로 (의료 응용 강함)
- **분리**: `VSA` (Variable Stiffness Actuator) → `Actuators` 안에 별도 Order
- **분리**: `Continual / Lifelong Learning` → 그대로 두되, 최근 BioSLAM 같은 lifelong place recognition 추가
- **분리**: `Aerial Swarms` → Multi-Robot Phylum 안의 별도 Class (단순히 Aerial UAV가 아니라 multi-robot 협조 측면)

---

## 5. 시대별 분포 통찰 (참고)

읽으면서 본 시대 패턴:
- **1988-2000**: Single-robot kinematics/dynamics/control 거의 99%. Multi-robot은 이론만.
- **2000-2008**: SLAM 폭발 (FAB-MAP, EKF SLAM observability, FastSLAM, GraphSLAM). 모듈러 self-reconfigurable robot 황금기. 의료 로봇 본격화.
- **2008-2015**: 쿼드로터 + soft robot + 변형 가능 액추에이터. 이미테이션 러닝 (PbD). Sample-based motion planning 최적성.
- **2015-2020**: Deep learning 침투. 자율주행. 시뮬레이션-실제 (Sim-to-Real). 활성 학습. ORB-SLAM2/3, VINS-Mono.
- **2020-2025**: 휴머노이드 + 사족보행 RL 폭발. VLA/Diffusion Policy. In-the-wild 데이터셋. Foundation 모델. Gaussian Splatting SLAM. 고밀도 협업 multi-robot.

---

## 6. 다음 단계

이 변경 내역을 반영해서 [TAXONOMY.md](TAXONOMY.md)를 최종안으로 갱신합니다.
- Phylum: 12 → 13
- Class: ~75개 → ~95개
- Order: ~250개 → ~330개
- Genus는 분류 결과에서 카운트가 큰 Order에 한해서만 부여
