# Reading Notes — 7,477 논문 제목을 시간순으로 읽으면서 기록

## Chunk 1: 1988-2001 (~650 papers) — Early/Classical era

### 빈출 테마 (현재 택소노미와 매핑됨)
- Inverse/Forward Kinematics, Redundant manipulators, Singularity, Workspace, Manipulability → Theoretical / Kinematics ✅
- Manipulator Dynamics, Parameter Identification, Inertia matrix → Theoretical / Dynamics ✅
- Force closure, Grasp synthesis, Caging → Manipulation / Grasping ✅
- Compliant motion, Impedance control → Control / Force-Impedance ✅
- Path planning, C-space, Configuration space → Planning ✅
- Mobile robot navigation, sonar mapping → SLAM&Loc / Planning ✅
- Calibration (hand-eye, kinematic) → SLAM&Loc / Calibration ✅
- Visual servoing → Control / Visual Servoing ✅
- Adaptive/Robust/Sliding mode control → Control / Classical ✅
- Bipedal walking (passive dynamic walker) → Locomotion / Legged / Biped ✅
- Quadruped/Hexapod → Locomotion / Legged ✅
- Underwater vehicle, AUV → Locomotion / Underwater ✅
- Telerobotics, teleoperation → HRI / Teleoperation ✅
- Field robotics (Mars rovers, Antarctic, sewer pipe PIRAT) → Application / Field ✅
- Surgical (early laparoscopic, endoscopy) → Application / Medical ✅
- Cooperative manipulation (multi-arm holding object) → Multi-Robot / Coordination ✅

### 새로 발견 — 택소노미에 추가 필요
1. **Robot Software & Architecture** ← 다수 논문 ("ControlShell", "ORCCAD", "Architecture for Autonomy", "Programming Toolsets", "Time Petri Net for code generation"). 현재 누락. → 새 Phylum or Class
2. **Distributed Manipulation / MEMS / Programmable Force Fields** ← Bohringer, Donald 계열. Manipulation 안에 Order로 추가
3. **Parts Feeding / Vibratory Feeders / Part Orienting** ← 산업용. Application 안에 추가? or Manipulation의 specialized order
4. **Haptic Rendering / Haptic Devices** ← Teleop과 별개. HRI 안에 Haptic Interfaces로
5. **Hyper-redundant / Snake-like (Chirikjian)** ← 1999년부터 등장. Locomotion / Bio-inspired 또는 Hardware / Continuum과 cross-cut
6. **Sequential Composition / Behavior-based** ← Brooks/Burridge/Koditschek. Control or Planning?
7. **Sensor Scheduling / Bayesian Sensor Placement** ← Perception / Active Sensing 추가
8. **Caging** (force-closure 변형) ← Grasping 안에 sub-genus
9. **Robot Wheelchair / Mobility Aid** ← HRI / Assistive (이미 있음, 강화 필요)
10. **Welding Robots, Industrial robots (programming, measurement, calibration)** ← Application / Industrial 추가
11. **Robot Books / Editorials / "From the Editor"** ← 메타. "Other / Editorial" 카테고리 필요 (가끔 등장)

### 흥미로운 관찰
- 1988-2000은 거의 모두 single-robot 분석 중심. Multi-robot은 쓰여있어도 한정적.
- Learning-based control 거의 없음 (Albus perceptron, neural net 한두개).
- "Service robot" / "Robots in Human Environments" (Khatib) 같은 비전 논문 1999년부터 등장.
