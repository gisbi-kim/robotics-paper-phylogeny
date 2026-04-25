# 로봇공학 계통도 (Robotics Phylogenetic Taxonomy) — 최종안 v2

7,477개 논문 (T-RO/IJRR/RSS, 1988-2025) 통독 후 확정.
변경 내역은 [TAXONOMY_CHANGES.md](TAXONOMY_CHANGES.md) 참조.

생물 분류처럼 4단계: **Phylum > Class > Order > Genus**

> 표기: 들여쓰기로 깊이 표시. 아래 트리 본문은 P/C/O 3단계 위주이고, **4단계 (Genus)는 별도 룰 파일** [`genus_rules.py`](genus_rules.py) 에 정의. 모든 논문은 4단계 라벨을 받음 (specific Genus 매칭 안 되면 `(general)`).

---

## 1. Perception & Sensing (지각·센싱)

- **Visual Perception**
  - Object Detection / Recognition
    - 2D Object Detection
    - 3D Object Detection
    - Pedestrian / Vehicle Detection
  - Semantic / Instance Segmentation
  - Pose Estimation (6-DoF / PnP / Human pose)
  - Depth Estimation (Monocular / Stereo / Self-supervised)
  - 3D Reconstruction / Neural Field
    - NeRF / Neural Implicit
    - 3D Gaussian Splatting
    - TSDF / Volumetric / SDF
    - Multi-view Stereo / Photogrammetry
  - Optical / Scene Flow
  - Image Enhancement / Restoration / Underwater
- **Active Perception** ⭐
  - Active Vision / Next-Best-View
  - Active Tactile Exploration
  - Active Sensing / Information-Gathering
- **LiDAR Perception**
  - Point Cloud Processing (general)
  - Point Cloud Object Detection
  - Point Cloud Semantic Segmentation
  - Point Cloud Registration (TEASER, Quatro++ 등)
  - Doppler / Velocity-aware LiDAR
- **Radar Perception**
  - Radar Object Detection / Tracking
  - mmWave / FMCW / 4D Radar
  - Radar Odometry (CFEAR, RadarSLAM)
- **Acoustic Perception**
  - Sonar Imaging / Acoustic Cameras
  - Sound Source Localization
  - Acoustic SLAM (underwater)
- **Tactile Sensing** ⭐ (큰 폭 강화)
  - GelSight / Vision-based Tactile
  - Capacitive / Resistive Tactile Skin
  - Event-based Optical Tactile (Evetac 등)
  - Electrical Impedance Tomography (EIT) Skin
  - Tactile Servoing / Active Touch
  - Visuo-Tactile Fusion
  - Slip / Contact Detection
- **Event-based Vision**
  - Event Camera Processing
  - Event-based VIO/SLAM
  - Spiking Neural Vision
- **Multi-modal Perception** ⭐
  - Sensor Fusion (Vision+LiDAR+Radar+IMU)
  - Cross-modal Learning
  - Foundation-model Perception (CLIP-Fields, ConceptFusion, Octopi)
- **Tracking**
  - Single-Object Tracking
  - Multi-Object Tracking (MOT)
  - Visual Object Tracking
- **3D Scene Graph / Spatial Perception** ⭐ (modern)
  - Hierarchical Spatial Perception (Kimera, Hydra)
  - Open-Vocabulary 3D Scene Graphs

---

## 2. SLAM & Localization (위치추정·매핑)

- **SLAM**
  - Visual SLAM / Visual Odometry
  - LiDAR SLAM / LiDAR Odometry (LOAM, FAST-LIO)
  - Visual-Inertial Odometry/SLAM (VIO; VINS-Mono, OKVIS)
  - LiDAR-Inertial Odometry/SLAM (LIO; FAST-LIO2)
  - Multi-modal SLAM (V+L+I+GNSS; FAST-LIVO2, GVINS, MARS-LVIG)
  - Multi-LiDAR / Multi-IMU / Multi-Camera SLAM
  - Radar SLAM/Odometry
  - Event-based VIO/SLAM
  - Acoustic / Underwater SLAM (AQUA-SLAM, SVIn2)
  - Semantic SLAM
  - Object SLAM (CubeSLAM, NeuSE)
  - Dynamic-environment SLAM (DefSLAM, Dynam-SLAM, NR-SLAM)
  - **Neural Implicit / Gaussian Splatting SLAM** ⭐ (PIN-SLAM, GS-LIVO, HI-SLAM2, VINGS-Mono)
  - Continuous-time SLAM (Gaussian Process priors)
  - Multi-Robot / Distributed SLAM (cross-cut Multi-Robot Phylum)
- **Place Recognition / Loop Closure**
  - Visual Place Recognition (FAB-MAP, NetVLAD-style)
  - LiDAR Place Recognition (Scan Context, BEVPlace++)
  - Radar Place Recognition
  - Cross-modal Place Recognition (Vis ↔ LiDAR, i3dLoc, CMRNext)
  - Foundation-model VPR
- **Localization** (맵 사전 보유)
  - Visual Localization
  - LiDAR-based Localization
  - Cross-modal Localization
  - Indoor / GPS-denied Localization
  - UWB / Radio / WiFi Localization
  - Range-only / Acoustic Beacon Localization
  - Map-free / Internet-scale Localization
- **State Estimation**
  - Bayesian Filtering (EKF / UKF / IEKF / Particle Filter)
  - Pose Graph / Bundle Adjustment / Factor Graphs (iSAM2, SE-Sync)
  - Continuous-time State Estimation
  - Inertial Odometry / IMU bias estimation
  - **Lie Group IMU Preintegration** (강한 sub-theme)
- **Calibration**
  - Sensor Calibration (intrinsic/extrinsic)
  - Hand-Eye Calibration
  - Visual-Inertial Calibration
  - LiDAR-Camera Calibration
  - Multi-LiDAR / Multi-modal Calibration
  - Kinematic Calibration (manipulator)
  - Targetless / Online Calibration

---

## 3. Planning (계획)

- **Path / Motion Planning**
  - Sampling-based (RRT, RRT*, PRM, BIT*, FMT*)
  - Search-based (A*, JPS, lattice)
  - Optimization-based (CHOMP, TrajOpt, GPMP)
  - Trajectory Optimization (minimum-snap, time-optimal, jerk-limited)
  - Kinodynamic Planning
  - Motion Primitives / DMP (Dynamic Movement Primitives)
  - **Convex Decomposition / Graphs of Convex Sets** ⭐ (Tedrake 계열)
  - **Diffusion-based Planning** ⭐ (Motion Planning Diffusion)
  - **Neural / Learning-based Motion Planning** (MPNet, iPlanner, NeuPAN)
  - GPU-Parallel Motion Planning
- **Task & Motion Planning (TAMP)**
  - Symbolic / PDDL Planning
  - Integrated TAMP
  - Hierarchical Task Planning
  - Hypergraph / Logic-based TAMP
- **Belief Space Planning**
  - POMDP Planning (DESPOT, SARSOP, MAGIC)
  - Active SLAM / Active Perception Planning
  - Active Information Gathering
- **Navigation**
  - Mobile Navigation (general)
  - Obstacle / Collision Avoidance (CBF-based, RVO/BRVO)
  - Autonomous Exploration (frontier, NBV, FALCON, RACER, TARE)
  - Coverage Planning (lawn-mower, Boustrophedon)
  - Social Navigation (crowd-aware, SICNav, DRL-VO)
  - Off-road / Unstructured Terrain Navigation (STEP, EVORA, TerrainNet, Verti-Bench)
  - **Vision-Language Navigation** ⭐ (NaVid, NaVILA, Uni-NaVid, GOAT)
  - Object-goal / Embodied Navigation (SEEK)
- **Specialized Planning**
  - Manipulation Planning / Grasp Planning
  - Footstep / Gait Planning
  - Reactive Planning
  - Multi-Query Planning / Experience Library (E-Graphs, CoverLib)
  - **Multi-Agent Path Finding (MAPF)** ⭐ (Conflict-Based Search, CBSS) — cross-cut Multi-Robot
  - Inspection Planning / 3D Coverage

---

## 4. Control (제어)

- **Classical Control**
  - PID / Feedback Control
  - Adaptive Control
  - Robust Control (H∞)
  - Sliding Mode Control
  - Nonlinear Control (Lyapunov, backstepping, feedback linearization)
- **Optimal / Predictive Control**
  - Model Predictive Control (MPC)
  - Linear MPC / Nonlinear MPC (NMPC)
  - **Contact-Implicit MPC** ⭐ (Hybrid iLQR-MPC, Cafe-MPC)
  - **Sampling-based MPC / MPPI** ⭐
  - Information-Theoretic MPC
  - LQR / iLQR / DDP / Differential Dynamic Programming
- **Force / Impedance Control**
  - Impedance / Admittance Control
  - Force Control / Hybrid Position-Force
  - Passivity-based / Port-Hamiltonian
  - Variable Impedance Control
- **Whole-Body Control**
  - Hierarchical / Prioritized Tasks
  - Multi-contact Whole-body
  - Humanoid Whole-Body (HOMIE, AMO, ASAP)
- **Safety-Critical Control**
  - Control Barrier Functions (CBF)
  - **Neural CBF / Learned Lyapunov / Contraction** ⭐ (BarrierNet)
  - Reachability Analysis (HJ, RADIUS, REFINE)
  - Safe Sets / Funnels / LQR-trees
- **Visual Servoing**
  - Image-based (IBVS)
  - Position-based (PBVS)
  - Direct / Photometric Visual Servoing
  - Visual Servoing for Continuum / Soft / Magnetic robots
- **Learning-based Control**
  - Iterative Learning Control (ILC)
  - Neural Network Controllers
  - **Koopman Operator-based Control** ⭐ (Koopman MPC for soft robots)
  - **Differentiable Physics / Differentiable Simulators** ⭐ (DiSECt, DiffTune)
  - **Neural ODE / Hamiltonian Networks on Lie Groups**
  - Meta-Learning Control / Adaptive
- **Bio-inspired Control** ⭐ (신규 Class)
  - Central Pattern Generators (CPG)
  - Limit Cycle Walkers / HZD
  - Phase Reset / Entrainment-based Control

---

## 5. Manipulation (조작)

- **Grasping**
  - Grasp Planning / Synthesis (analytical: force closure, caging)
  - Learning-based Grasping (Dex-Net, GraspNet-1Billion, AnyGrasp)
  - Suction Grasping (Sim-Suction)
  - Multi-finger Grasping
  - Anti-podal / Parallel-jaw Grasping
  - **Caging-based Grasping** ⭐ (별도 Genus)
  - Foundation-model Grasping
  - Whole-arm / Whole-body Grasping
- **Dexterous Manipulation**
  - In-hand Manipulation
  - Multi-finger Dexterous (RBO Hand, RUTH, LEAP Hand)
  - Bimanual Manipulation
  - **Foundation Controllers** ⭐ (DexterityGen)
  - **Learning Dexterity from Human Videos** ⭐ (DexCap, DexWild, ScrewMimic)
  - **Tactile Dexterous Manipulation** (Roller Grasper, RoTipBot)
- **Contact-rich Manipulation**
  - Assembly / Insertion / Peg-in-hole (IndustReal, AutoMate, Factory)
  - Deformable Object Manipulation (cloth, dough, plasticine)
  - **Knot Tying / Cable / Wire Manipulation** ⭐ (별도 Order)
  - Liquid / Granular Material Manipulation (DextAIRity, RoboCraft, GranularGym)
  - Articulated Object Manipulation (FlowBot3D, ArticuBot)
- **Non-prehensile Manipulation**
  - Pushing / Sliding
  - Tossing / Throwing (TossingBot, TossNet)
  - Rolling / Rocking
- **Tool Use**
- **Mobile Manipulation**
  - Loco-Manipulation (legged + arm)
  - Whole-body Mobile Manipulation
  - VLA-based Mobile Manipulation (OK-Robot, RT-2, Vid2Robot)
- **Aerial Manipulation**
  - Aerial Grasping / Perching
  - Aerial Manipulator Platforms (DRAGON)
- **Underwater Manipulation**
- **Distributed Manipulation** ⭐ (신규 Class)
  - Programmable Force Fields (Bohringer/Donald)
  - Vibratory Parts Feeders / Parts Orienting
  - Air-flow / Surface-based Distributed Manipulation
- **General Manipulation** (catchall)

---

## 6. Locomotion (이동)

- **Legged Locomotion**
  - Bipedal / Humanoid (Cassie, ATRIAS, ASIMO, Berkeley Humanoid)
  - Quadruped (Anymal, Spot, MIT Cheetah, Solo)
  - Hexapod / Multi-legged (RHex)
  - Whole-body Loco-Manipulation
  - **Hybrid Wheel-Leg** ⭐ (TurboQuad, WaLTR, Wheel Transformer)
  - Underwater Legged
- **Wheeled Locomotion**
  - Differential Drive
  - Omnidirectional / Mecanum
  - Skid-steer
  - Ball-bot / Inverted Pendulum
- **Aerial Locomotion**
  - Multirotor / Quadrotor
  - Fixed-wing
  - Tail-sitter / VTOL / Tiltrotor
  - Flapping-wing (RoboBee, Hummingbird, bat-inspired)
  - **Insect-scale / Pico Aerial** ⭐ (RoboFly, RoboBee class)
  - **Hybrid Aerial-Aquatic / Aerial-Terrestrial** (HyTAQ, Dipper, Ringbot)
  - Ultralight / Indoor Aerial
- **Underwater Locomotion**
  - AUV / UUV
  - Bio-inspired Swimmers (fish, octopus, eel, jellyfish)
  - Tethered ROV
- **Surface / Marine Locomotion**
  - USV / Surface Vehicle
  - Ice-field Navigation (AUTO-IceNav)
  - Sailboat
- **Bio-inspired Locomotion**
  - Snake / Serpentine
  - Climbing Robot (gecko, microspine, magnetic)
  - Jumping / Hopping (locust-inspired, Salto)
  - Swimming Robotic Fish
  - Crawling / Inchworm / Earthworm-like
  - **Sand-swimming / Granular Locomotion** ⭐ (sandfish)
- **Space Locomotion**
  - Planetary Rover (Mars, Lunar, Chang'E)
  - Microgravity / Free-flying
  - Space manipulator dynamics
- **Vibration / Stick-slip Locomotion**

---

## 7. Robot Design & Hardware (설계·하드웨어)

- **Soft Robotics**
  - Soft Actuator (pneumatic / hydraulic)
  - Soft Gripper / Hand (Pisa SoftHand, fin ray)
  - Soft Sensor / Skin
  - Variable Stiffness / Jamming (laminar, granular, layer)
  - Origami Mechanism
  - Dielectric Elastomer / EAP / **HASEL** ⭐
  - Shape-memory Alloy (SMA)
  - **Twisted Coiled Polymer (TCP) / Artificial Muscle** ⭐
  - **Vine / Growing Robot** ⭐
  - Soft Continuum Manipulator (Cosserat-based)
- **Mechanism Design**
  - Parallel / Cable-driven Mechanism (Stewart-Gough, cable-suspended)
  - Serial Manipulator Design
  - Compliant Mechanism / Flexure
  - Gripper Design
  - Spinal / Multi-joint Mechanism
  - **Tensegrity Robots** ⭐
  - Hybrid Rigid-Soft Mechanisms
- **Continuum Robot**
  - Continuum Manipulator (general)
  - Tendon-driven Continuum
  - **Concentric Tube Robots** ⭐ (의료 응용)
  - Cosserat Rod Models
  - **Magnetic Continuum Robots** ⭐
  - Parallel Continuum Robots
- **Modular / Reconfigurable Robot**
  - Self-reconfigurable (M-TRAN, Million Module March)
  - Modular Design
  - Variable Topology Truss
- **Microrobotics / Nanorobotics**
  - **Magnetic Microrobots / Swarms** ⭐ (큰 sub-area)
  - Microswimmer (helical, flagellar)
  - Catalytic / Chemically-driven
  - **MRI-driven / MR-compatible Robots** ⭐
  - Bio-medical Microrobot (capsule endoscope)
  - Optical Tweezers / Microbeads
- **Bio-hybrid Robot**
  - Magnetotactic Bacteria
  - Insect-Computer Hybrid (cyborg locust)
  - Cell-actuated
- **Actuators (rigid)**
  - Electric / Servo
  - Pneumatic / Hydraulic
  - Piezoelectric
  - Magnetic / Electromagnetic
  - Series Elastic Actuator (SEA)
  - **Variable Stiffness Actuators (VSA)** ⭐
  - **Magnetorheological Actuators** ⭐
  - **Electrostatic Actuators (electroadhesion)** ⭐
- **Sensors (Hardware design)**
  - Vision / Camera Hardware
  - Tactile Sensor Hardware
  - Force/Torque Sensor (FBG, capacitive)
  - Proximity Sensors
- **Manufacturing**
  - 3D Printing / Additive
  - Origami Fabrication
  - Self-folding / Pop-up Robotics

---

## 8. Human-Robot Interaction (HRI)

- **Physical HRI**
  - Collaborative Robot (Cobot)
  - Co-manipulation
  - Safe Physical Contact
  - pHRI Stability / Passivity
- **Social Robotics**
  - Social Robot / HRI Study
  - Social Navigation (crowd-aware)
  - Companion Robot / Elderly care (PARO, Quori)
  - Robot Gestures / Speech
- **Teleoperation**
  - Bilateral Teleoperation (stability, transparency, time-delay)
  - Haptic Teleoperation
  - VR/AR / Immersive Teleoperation
  - **In-the-Wild Teleoperation** ⭐ (UMI, AnyTeleop, Tilde)
  - Surgical / Medical Teleoperation
- **Shared Autonomy**
  - Shared Control / Mixed-Initiative
  - Intent Inference / Prediction
  - Hindsight Optimization
- **Assistive Robotics**
  - Exoskeleton / Wearable (lower-limb, upper-limb, hip, back)
  - **Soft Exosuit / Wearable Soft** ⭐ (Harvard Exosuit)
  - **Hand Exoskeletons** ⭐
  - Prosthetics (powered knee/ankle, transhumeral)
  - Rehabilitation (stroke, gait, neurorehab)
  - Mobility Aids (wheelchair)
  - Brain-Machine Interface (BMI/BCI, EEG, EMG)
- **Haptic Devices & Rendering** ⭐ (신규 Class)
  - Haptic Display / Force-feedback Devices
  - Haptic Rendering Algorithms (passivity, stability)
  - Wearable Haptic Feedback (vibrotactile, electrotactile)
  - Cobotic / Hand Controllers
- **Communication / Language**
  - Language-conditioned Behavior (cross-cut Learning Phylum)
  - Robot Speech / Gesture / Eye-gaze
- **Trust & Safety in HRI**
  - Trust Models / Transfer
  - Safety Standards / Risk Assessment

---

## 9. Multi-Robot Systems (다중로봇)

- **Swarm Robotics**
  - Bio-inspired Swarm
  - Swarm Behavior / Pattern Formation
  - Microbot / Magnetic Microbot Swarms (cross-cut Microrobotics)
- **Coordination**
  - Formation Control / Consensus
  - Flocking / Rendezvous
  - Multi-Robot Control
  - Task Allocation / Auction (Hungarian, ADMM)
  - **Pursuit-Evasion / Surveillance** ⭐ (별도 Order)
  - **Adversarial / Resilient (Byzantine)** ⭐
- **Multi-Robot Planning**
  - **Multi-Agent Path Finding (MAPF) / CBS** ⭐
  - Multi-Robot Motion Planning
  - Heterogeneous Team Planning
- **Multi-Robot SLAM**
  - Cooperative SLAM
  - **Distributed Pose Graph / Bundle Adjustment** ⭐ (Kimera-Multi, iMESA, DABA)
  - Decentralized Visual-Inertial SLAM (D2SLAM, Omni-Swarm)
- **Distributed Algorithms / Optimization**
  - Distributed Optimization (ADMM, consensus)
  - **Distributed Certifiably Correct Optimization** ⭐
  - Consensus Algorithms
- **Aerial Swarms / UAV Swarms** ⭐ (신규 Class)
  - Decentralized Aerial Swarm (Omni-Swarm, Swarm-LIO2)
  - Communication-aware Swarm
  - Drone Defense / Herding
  - Quadrotor Trajectory Generation for Swarms
- **Communication / Networks**
  - Connectivity Maintenance
  - Bandwidth-aware Coordination
  - Cloud Robotics / Edge Communication

---

## 10. Learning for Robotics (학습)

- **Reinforcement Learning**
  - RL (general)
  - **Sim-to-Real for Legged Locomotion** ⭐ (Cassie, Anymal, ASAP, RMA)
  - Sim-to-Real for Manipulation (DrEureka, RoboCasa)
  - Multi-agent RL
  - Inverse RL (IRL)
  - Hierarchical RL
  - Offline RL
  - Safe RL / Constrained RL
- **Imitation Learning**
  - Behavior Cloning / Programming by Demonstration (PbD historical)
  - Generative Imitation
  - Demonstration Curation / Selection
  - **In-the-Wild / From-Human-Video IL** ⭐ (DexCap, DexWild, ScrewMimic, AVID)
- **Foundation Models for Robotics** ⭐
  - **Vision-Language-Action (VLA)** (RT-1, RT-2, π₀, OpenVLA, Octo, NaVILA, SpatialVLA, CLIP-RT, FAST)
  - LLM-based Reasoning / Planning (SayCan, MOKA, AutoGPT+P)
  - **Diffusion Policies / Flow Matching** (Diffusion Policy, 3D DP, Consistency Policy, RDT, IMLE Policy, π₀)
  - Generalist / Cross-embodiment Policies (Octo, MIRAGE, PoCo)
  - World Models for Robotics (UWMs, PIN-WM)
- **Meta / Few-shot Learning**
- **Transfer Learning / Domain Adaptation**
- **Continual / Lifelong Learning**
- **Self-supervised / Representation Learning**
- **Active Learning**
- **Deep Learning Application** (catchall)
- **Datasets & Benchmarks & Simulators** ⭐
  - Robot Manipulation Datasets (DROID, BridgeData, RoboMIND, DexCap)
  - Simulators (MuJoCo Playground, ManiSkill3, RoboCasa, RoboVerse)
  - Benchmarks (FurnitureBench, COLOSSEUM, HumanoidBench)
  - SLAM / Perception Datasets (KITTI, Oxford RobotCar, EuRoC, NYU, NuScenes-style)

---

## 11. Application Domains (응용)

- **Medical & Surgical Robotics**
  - Surgical Robot (laparoscopic, da Vinci, RAVEN II)
  - Endoscopy / Catheter / Colonoscopy
  - Needle Steering / Biopsy / Brachytherapy
  - **Capsule Endoscopy / Magnetic Capsule** ⭐
  - Microsurgery / Neurosurgery (Micron, MRI-compat)
  - **Beating Heart Surgery / Motion Compensation** ⭐
  - Image-guided / Ultrasound-guided
  - Robotic Suturing / Cutting / Drilling
  - Rehabilitation Robotics (cross-cut Assistive)
- **Field Robotics**
  - Agricultural Robotics (harvesting, weeding, phenotyping, under-canopy)
  - Inspection Robotics (pipeline, bridge, cable, hull, building)
  - Construction Robotics
  - Mining / Excavation / CraterGrader
  - Forestry / Vineyard
- **Autonomous Driving**
  - Self-driving Vehicle (passenger car)
  - Autonomous Truck / Bus
  - Driving Perception (LiDAR, radar, camera)
  - Driving Planning / Decision (interactive, game-theoretic)
  - Traffic / Intersection / Mixed Autonomy
  - HD Map / Lane / Intersection
- **Space Robotics**
  - Planetary Rover (Mars, Lunar, Chang'E)
  - Orbital / Satellite Servicing
  - Free-flying Robot
  - Microgravity Manipulation
- **Search & Rescue**
  - SAR Robotics
  - Disaster Response / Forest canopy SAR
- **Service Robotics**
  - Domestic / Service Robot
  - Hospitality / Retail / Robotic Tutor
  - **Food Service / Cooking / Cutting** ⭐ (FLAIR, Robot Cutting)
- **Logistics**
  - Warehouse Robotics
  - Last-mile Delivery (UAV, ground)
- **Computational Biology Robotics** ⭐ (신규 Class)
  - Protein Folding / Molecular Motion Planning
  - DNA / Bio-mechanical Modeling
  - Cell Manipulation (microrobotics)
- **Education / Entertainment Robotics**
  - Robotic Tutor
  - Animatronic / Performance Robot

---

## 12. Theoretical Foundations (이론·수학)

- **Kinematics**
  - Forward / Inverse Kinematics
  - Workspace Analysis
  - Singularity Analysis
  - Redundancy Resolution
  - Kinematic Calibration
  - Manipulability / Dexterity Index
  - Type Synthesis / Kinematic Design
- **Dynamics**
  - Robot Dynamics (rigid body)
  - Flexible Body Dynamics
  - Contact / Friction Modeling (LuGre, Hunt-Crossley)
  - **Multi-contact / Complementarity** ⭐
  - System Identification
  - Articulated Body Algorithms (RNEA, ABA)
  - Articulated Body Dynamics on Lie groups
- **Optimization**
  - Convex Optimization
  - Non-convex / Mixed-integer
  - Distributed Optimization (cross-cut)
  - Robust Optimization
  - **Differentiable Programming** ⭐ (PROX-QP, ProxDDP, SymForce)
  - **Semidefinite Relaxations / Certifiable Optimization** ⭐ (TEASER, SE-Sync)
- **Geometric Methods**
  - Lie Groups / Lie Algebras (SO(3), SE(3))
  - **Lie Group IMU Preintegration** ⭐ (강한 sub-theme)
  - Riemannian / Differential Geometry
  - Screw Theory / Dual Quaternions
  - **Equivariant Methods** ⭐ (modern: Equivariant Transporter, NeuSE, RING#)
- **Probabilistic Methods**
  - Gaussian Processes
  - Bayesian Inference (POMDP, factor graphs)
  - Stochastic / Sample-based methods
- **Game Theory / Decision Theory**
  - Differential Games
  - Stackelberg / Nash
  - Active Information Acquisition
- **Formal Methods / Verification**
  - Temporal Logic (LTL/STL/sclTL)
  - Model Checking
  - Synthesis from Specification
  - Reach-avoid synthesis
- **Stability Analysis**
  - Lyapunov Stability
  - Input-to-State Stability
- **Robot Safety & Failure** ⭐ (신규 Class)
  - Robot Collision Detection
  - Failure Detection / Anomaly Detection
  - Fault Tolerance (manipulator, multi-robot)
  - Resilience / Byzantine fault-tolerance

---

## 13. Robot Software & Architecture ⭐ (신규 Phylum)

- **Robot Architecture / Middleware**
  - Modular Robot Architecture (ControlShell, ORCCAD, OpenHRP, ROS-style)
  - Real-time Architecture
  - Behavior-based / Subsumption (Brooks)
- **Behavior Trees / Reactive Architectures**
  - Behavior Tree formalism (handling concurrency, modularity)
  - Hybrid Control / Sequential Composition
- **Robot Programming / DSL**
  - Programming by Human Demonstration (workflow side)
  - Robot Programming Frameworks / Toolsets
  - Skill Frameworks (constraint-based, manipulation primitives)
- **Code Generation / Symbolic Computation**
  - SymForce-style symbolic codegen
  - Synthesis from Specification (Petri net, model checking)
- **Real-time Systems / Scheduling**
  - Real-time scheduling for robotics (semantic-aware)
  - Mixed-criticality / Kubernetes orchestration
  - Cyber-physical Systems (CPS)

---

## 0. Other / Unclassified (catchall)

- 제목만으로는 분류 불가능한 케이스
- "From the Editor" / "Editorial" / "Erratum" / "Book Review" 등 메타 페이지
- 분류 후 통계로 다시 검토하여 줄여나간다

---

## 메모 (분류 우선순위 룰)

- **단일 라벨**: 한 논문 = 한 위치. Cross-cutting 우선순위:
  1. 가장 새롭고 specific한 방법론이 핵심이면 → Learning Phylum (예: VLA, Diffusion Policy)
  2. 새 방법론을 적용한 응용이면 → 응용 Phylum (예: RL로 보행 학습 → Locomotion)
  3. 응용 분야가 매우 specific하면 → Application Phylum (예: 의료, 우주)
  4. 그 외에는 가장 큰 카테고리(Phylum) 안에서 가장 specific한 Order
- **Cross-cut 예시**:
  - "Diffusion Policy for Bimanual Cloth Manipulation" → `Learning > Foundation Models > Diffusion Policies` (방법론 새롭고 핵심)
  - "RL for Cassie biped walking" → `Locomotion > Legged > Bipedal` (RL은 도구, locomotion이 핵심)
  - "Surgical robot for needle steering" → `Application > Medical & Surgical > Needle Steering`
- 분류 후 카운트가 적은 Order는 합치고, 너무 많은 Order는 Genus로 더 쪼갠다.

---

## 부록: 4단계 (Genus) 분류 — `genus_rules.py`

본 트리에서 sub-rule로 풀려나간 Genus 카테고리. Top 45개 Order에 대해 정의됨. 매칭 안 되면 `(general)`로 fallback.

| Order | 정의된 Genus 수 | 예시 Genus |
|---|---:|---|
| Bipedal / Humanoid | 13 | Cassie / ATRIAS / HZD / SLIP / Sim-to-Real RL / Whole-body Humanoid / ZMP / Bipedal Jumping ... |
| Quadruped | 7 | MIT Cheetah / ANYmal / Boston Dynamics Spot / Sim-to-Real RL / MPC-based / Loco-Manipulation |
| Multirotor / Quadrotor | 7 | Quadrotor Swarm / Agile Racing / Aerial Manipulation / Cinematography / Learning-based / MPC / State Estimation |
| Visual SLAM/Odometry | 7 | ORB-SLAM / SVO / DSO/LSD / Monocular / Stereo / RGB-D / VPR-augmented |
| LiDAR SLAM/Odometry | 4 | LOAM / FAST-LIO / LIO-SAM / Continuous-time |
| VIO | 5 | VINS / OKVIS / ROVIO / MSCKF / Preintegration |
| Tactile Sensors | 7 | GelSight / Visuo-Tactile / Event-based / EIT / Slip Detection / Whisker / BioTac |
| Grasp Planning | 6 | Force-Closure / Caging / Multi-finger / Underactuated / Tactile-based / Novel Object |
| Deformable Object | 6 | Cloth/Garment / Rope/Cable/Wire / Liquid / Granular / Elasto-plastic / Soft Tissue |
| Assembly / Insertion | 5 | Peg-in-Hole / Snap-fit / Screwing / RL-based / Cooperative |
| Continuum Manipulator | 5 | Tendon-driven / Fluidic / Cosserat / Multi-section / Magnetic |
| Parallel Mechanism | 5 | Stewart-Gough / Delta / Cable-driven / Singularity / Kinematics |
| Visual Servoing | 8 | IBVS / PBVS / Direct/Photometric / Aerial / Mobile / Parallel / Tactile / Aural / Thermal |
| Exoskeleton / Wearable | 4 | Lower-limb / Upper-limb / Back-Spine / Hand-Wrist |
| RL | 6 | Safe RL / Multi-agent / Inverse RL / Hierarchical / Offline / Meta |
| Sim-to-Real | 4 | Locomotion / Manipulation / Aerial / Domain Randomization |
| VLA | 4 | RT-series / π₀-family / Octo/OpenVLA / VLN |
| Diffusion Policies | 4 | 3D Diffusion / Consistency / Flow Matching / Hierarchical |
| Pursuit-Evasion | 6 | Pursuit / Patrolling / Surveillance / Persistent Monitoring / Perimeter / Herding |
| ... (총 45 Order) | | 자세한 룰은 [`genus_rules.py`](genus_rules.py) |

**Genus 적용 결과**:
- 전체 7,477편 중 약 **3,902편 (52.2%)** 가 specific Genus를 받았고,
- 나머지는 `(general)` 또는 룰이 없는 Order에 속함.
- 엑셀 `Papers` 시트에 4번째 컬럼(`Genus`)으로 표시됨.
