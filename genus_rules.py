"""
Genus assignment rules — 4th level of taxonomy.
Called after (Phylum, Class, Order) is determined.

Targets: split top ~45 Orders that have many papers, into 3-7 Genus each.
Other Orders default to "(general)".
"""

def has_any(t, kws):
    return any(k in t for k in kws)


def assign_genus(phylum, cls, order, t):
    """t is title with leading/trailing spaces, lowercased."""

    # ============================================================
    # PLANNING
    # ============================================================
    if order == 'Motion / Path Planning':
        if has_any(t, ['multi-robot', 'multirobot', 'multi robot', 'multi-uav']):
            return 'Multi-Robot Path Planning'
        if 'humanoid' in t or 'biped' in t:
            return 'Humanoid Motion Planning'
        if 'redundant' in t or 'manipulator' in t:
            return 'Manipulator Motion Planning'
        if 'aerial' in t or 'quadrotor' in t or 'drone' in t or 'uav' in t:
            return 'Aerial Motion Planning'
        if has_any(t, ['dynamic environment', 'dynamic obstacle',
                       'moving obstacle']):
            return 'Dynamic Environment Planning'
        if 'replan' in t or 're-plan' in t:
            return 'Replanning'
        if 'safe' in t or 'safety' in t:
            return 'Safe Motion Planning'
        if 'optimal' in t:
            return 'Optimal Motion Planning'
        if 'kinodynamic' in t:
            return 'Kinodynamic Planning'
        if 'manifold' in t or 'lie group' in t:
            return 'Manifold/Lie-group Planning'
        return 'General Motion Planning'

    if order == 'Sampling-based Planning':
        if 'rrt*' in t or 'optimal' in t or 'asymptotic' in t:
            return 'Asymptotically Optimal (RRT*-family)'
        if ' rrt' in t or 'rrt-' in t or 'rrt ' in t:
            return 'RRT-family'
        if ' prm ' in t or 'prm-' in t or 'roadmap' in t:
            return 'PRM / Roadmap'
        if 'kinodynamic' in t:
            return 'Kinodynamic Sampling'
        return 'General Sampling-based'

    if order == 'Trajectory Optimization':
        if 'minimum-snap' in t or 'minimum snap' in t \
                or 'time-optimal' in t or 'time optimal' in t \
                or 'minimum-time' in t or 'minimum time' in t:
            return 'Time/Snap-Optimal'
        if 'minimum-jerk' in t or 'minimum jerk' in t:
            return 'Minimum-Jerk'
        if 'sequential convex' in t or 'scvx' in t:
            return 'Sequential Convex Optimization'
        if 'chomp' in t or 'gpmp' in t or 'trajopt' in t:
            return 'CHOMP / TrajOpt / GPMP'
        if 'mixed-integer' in t or 'milp' in t:
            return 'Mixed-Integer'
        if 'contact' in t:
            return 'Contact-Implicit Trajopt'
        return 'General Trajectory Optimization'

    if order == 'Mobile Navigation':
        if 'social' in t or 'crowd' in t or 'pedestrian' in t:
            return 'Social Navigation'
        if 'humanoid' in t:
            return 'Humanoid Navigation'
        if 'aerial' in t or 'drone' in t:
            return 'Aerial Navigation'
        if 'underwater' in t:
            return 'Underwater Navigation'
        if 'indoor' in t:
            return 'Indoor Navigation'
        if 'reactive' in t:
            return 'Reactive Navigation'
        return 'General Mobile Navigation'

    if order == 'Autonomous Exploration':
        if 'multi-robot' in t or 'multirobot' in t or 'aerial swarm' in t:
            return 'Multi-Robot Exploration'
        if 'aerial' in t or 'uav' in t or 'drone' in t:
            return 'Aerial Exploration'
        if 'underwater' in t:
            return 'Underwater Exploration'
        if 'cave' in t or 'subterranean' in t:
            return 'Cave / Subterranean Exploration'
        if 'frontier' in t:
            return 'Frontier-based Exploration'
        if 'next-best-view' in t or 'next best view' in t:
            return 'Next-Best-View'
        return 'General Autonomous Exploration'

    if order == 'Obstacle / Collision Avoidance':
        if 'multi' in t or 'reciprocal' in t:
            return 'Multi-Robot Collision Avoidance'
        if 'aerial' in t or 'quadrotor' in t or 'drone' in t:
            return 'Aerial Collision Avoidance'
        if 'safe' in t or 'safety' in t or 'cbf' in t:
            return 'Safety-Critical Avoidance'
        return 'General Collision Avoidance'

    if order == 'POMDP / Belief Space Planning':
        if 'sarsop' in t or 'despot' in t or 'magic' in t:
            return 'Online POMDP Solver'
        if 'continuous' in t or 'continuous-state' in t:
            return 'Continuous-state POMDP'
        if 'belief space planning' in t:
            return 'Belief Space Planning'
        return 'General POMDP'

    # ============================================================
    # LOCOMOTION
    # ============================================================
    if order == 'Bipedal / Humanoid':
        if 'cassie' in t:
            return 'Cassie Robot'
        if 'atrias' in t:
            return 'ATRIAS Robot'
        if 'asimo' in t:
            return 'ASIMO / Honda-class'
        if 'mabel' in t or 'rabbit' in t:
            return 'MABEL / RABBIT (UMich-class)'
        if 'berkeley humanoid' in t or 'optimus' in t \
                or 'unitree h' in t:
            return 'Modern Humanoid Platform'
        if 'hzd' in t or 'hybrid zero dynamics' in t:
            return 'HZD-based Control'
        if 'slip' in t and 'walk' in t or 'spring-loaded' in t \
                or 'spring loaded' in t or 'spring-mass' in t:
            return 'SLIP / Spring-mass Model'
        if 'passive dynamic' in t or 'passive walk' in t \
                or 'limit cycle' in t:
            return 'Passive / Limit-cycle Walker'
        if 'whole-body' in t or 'whole body' in t:
            return 'Whole-body Humanoid Control'
        if 'sim-to-real' in t or 'sim2real' in t \
                or 'reinforcement learning' in t \
                or 'rl ' in t or 'rl-' in t:
            return 'Sim-to-Real RL Locomotion'
        if 'mpc' in t or 'model predictive' in t:
            return 'MPC-based Bipedal'
        if 'zmp' in t:
            return 'ZMP-based Walking'
        if 'jump' in t:
            return 'Bipedal Jumping'
        if 'humanoid' in t and 'manipulation' in t:
            return 'Humanoid Loco-Manipulation'
        return 'General Bipedal'

    if order == 'Quadruped':
        if 'cheetah' in t and 'mit' in t:
            return 'MIT Cheetah-class'
        if 'cheetah' in t:
            return 'Cheetah-class'
        if 'anymal' in t:
            return 'ANYmal-class'
        if 'spot' in t and 'boston' in t:
            return 'Boston Dynamics Spot'
        if 'sim-to-real' in t or 'sim2real' in t \
                or 'reinforcement learning' in t \
                or 'rl ' in t or 'rl-' in t or ' rma ' in t:
            return 'Sim-to-Real RL Quadruped'
        if 'mpc' in t or 'model predictive' in t:
            return 'MPC-based Quadruped'
        if 'gait' in t:
            return 'Quadruped Gait Control'
        if 'manipulation' in t or 'loco-manip' in t:
            return 'Quadruped Loco-Manipulation'
        return 'General Quadruped'

    if order == 'Legged (general)':
        if 'gait' in t:
            return 'Multi-legged Gait'
        if 'climb' in t:
            return 'Multi-legged Climbing'
        return 'General Legged'

    if order == 'Multirotor / Quadrotor':
        if 'swarm' in t or 'aerial swarm' in t:
            return 'Quadrotor Swarm'
        if 'aggressive' in t or 'agile' in t or 'racing' in t:
            return 'Agile / Racing Flight'
        if 'manipulation' in t or 'manip' in t or 'grasp' in t:
            return 'Aerial Manipulation'
        if 'cinematography' in t:
            return 'Cinematography Drone'
        if 'learning' in t or 'reinforcement' in t or 'imitation' in t:
            return 'Learning-based Quadrotor Control'
        if 'mpc' in t or 'model predictive' in t:
            return 'MPC-based Quadrotor'
        if 'state estimation' in t or 'observer' in t:
            return 'State Estimation for Quadrotor'
        return 'General Multirotor'

    if order == 'Mobile Wheeled Robot':
        if 'differential drive' in t or 'differential-drive' in t:
            return 'Differential Drive'
        if 'omnidirectional' in t or 'omni-directional' in t \
                or 'mecanum' in t:
            return 'Omnidirectional / Mecanum'
        if 'skid-steer' in t or 'skid steer' in t:
            return 'Skid-steer'
        if 'unicycle' in t:
            return 'Unicycle'
        if 'inverted pendulum' in t or 'ball-bot' in t \
                or 'ballbot' in t:
            return 'Balancing / Inverted Pendulum'
        return 'General Wheeled Mobile'

    if order == 'AUV / UUV':
        if 'manipulation' in t or 'manip' in t:
            return 'Underwater Manipulation'
        if 'navigation' in t or 'navig' in t:
            return 'Underwater Navigation'
        if 'docking' in t:
            return 'Underwater Docking'
        if 'inspection' in t or 'hull' in t:
            return 'Hull / Underwater Inspection'
        if 'cooperative' in t or 'multiple' in t:
            return 'Multi-AUV / Cooperative'
        return 'General AUV/UUV'

    # ============================================================
    # MANIPULATION
    # ============================================================
    if order == 'Grasp Planning / Synthesis':
        if 'force closure' in t or 'force-closure' in t:
            return 'Force-Closure Grasp'
        if 'caging' in t:
            return 'Caging-based'
        if 'multi-finger' in t or 'multifinger' in t:
            return 'Multi-finger Grasping'
        if 'underactuated' in t:
            return 'Underactuated Grasping'
        if 'tactile' in t:
            return 'Tactile-based Grasping'
        if 'novel object' in t or 'unknown object' in t:
            return 'Novel/Unknown Object Grasping'
        return 'General Grasp Planning'

    if order == 'Learning-based Grasping':
        if 'dex-net' in t or 'dexnet' in t:
            return 'Dex-Net Family'
        if 'graspnet' in t or 'anygrasp' in t:
            return 'GraspNet / AnyGrasp Family'
        if 'foundation' in t or 'vision-language' in t or 'vla' in t:
            return 'Foundation-Model Grasping'
        if 'reinforcement' in t:
            return 'RL-based Grasping'
        return 'General Learning-based Grasping'

    if order == 'In-hand / Multi-finger':
        if 'tactile' in t:
            return 'Tactile-based In-hand'
        if 'reinforcement' in t or 'rl ' in t:
            return 'RL-based In-hand'
        if 'soft' in t:
            return 'Soft-finger Manipulation'
        if 'rolling' in t or 'sliding' in t:
            return 'Rolling/Sliding Manipulation'
        return 'General In-hand'

    if order == 'Manipulator Control / Planning':
        if 'redundant' in t:
            return 'Redundant Manipulator'
        if 'mobile' in t and 'manipulation' in t:
            return 'Mobile Manipulator'
        if 'aerial' in t or 'flying' in t:
            return 'Aerial Manipulator'
        if 'parallel' in t:
            return 'Parallel Manipulator Control'
        if 'cable' in t or 'tendon' in t:
            return 'Cable/Tendon-driven Manipulator'
        if 'flexible' in t or 'compliant' in t:
            return 'Flexible/Compliant Manipulator'
        if 'kinematic' in t:
            return 'Kinematic Control'
        if 'force' in t or 'compliance' in t:
            return 'Force/Compliance Control'
        return 'General Manipulator'

    if order == 'Deformable Object Manipulation':
        if 'cloth' in t or 'fabric' in t or 'garment' in t:
            return 'Cloth / Garment'
        if 'rope' in t or 'cable' in t or 'wire' in t \
                or 'string' in t:
            return 'Rope / Cable / Wire'
        if 'liquid' in t or 'fluid' in t or 'pour' in t:
            return 'Liquid Manipulation'
        if 'granular' in t or 'sand' in t or 'powder' in t:
            return 'Granular Material'
        if 'plasticine' in t or 'elastoplastic' in t \
                or 'plastic' in t and 'deform' in t:
            return 'Elasto-plastic'
        if 'soft tissue' in t:
            return 'Soft Tissue'
        return 'General Deformable'

    if order == 'Assembly / Insertion / Peg-in-hole':
        if 'peg-in-hole' in t or 'peg in hole' in t \
                or 'peg-in' in t:
            return 'Peg-in-Hole'
        if 'snap-fit' in t:
            return 'Snap-fit Assembly'
        if 'screw' in t:
            return 'Screwing'
        if 'reinforcement learning' in t or 'industreal' in t \
                or 'automate' in t:
            return 'RL-based Assembly'
        if 'multi-robot' in t or 'cooperative' in t:
            return 'Cooperative Assembly'
        return 'General Assembly / Insertion'

    if order == 'Bimanual Manipulation':
        if 'cloth' in t or 'fabric' in t:
            return 'Bimanual Cloth Manipulation'
        if 'imitation' in t or 'demonstration' in t:
            return 'Bimanual IL'
        return 'General Bimanual'

    # ============================================================
    # SLAM & LOCALIZATION
    # ============================================================
    if order == 'General SLAM':
        if 'multi-robot' in t or 'cooperative' in t or 'distributed' in t:
            return 'Multi-Robot SLAM'
        if 'graph slam' in t or 'graph-slam' in t:
            return 'Graph SLAM'
        if 'ekf slam' in t or 'ekf-slam' in t:
            return 'EKF-based SLAM'
        if 'fastslam' in t or 'particle' in t:
            return 'Particle-Filter SLAM'
        if 'large-scale' in t or 'large scale' in t:
            return 'Large-scale SLAM'
        return 'General SLAM (other)'

    if order == 'Visual SLAM/Odometry':
        if 'orb-slam' in t or 'orbslam' in t:
            return 'ORB-SLAM Family'
        if ' svo ' in t or 'svo:' in t:
            return 'SVO Family'
        if 'dso' in t or 'lsd-slam' in t:
            return 'Direct (DSO/LSD)'
        if 'monocular' in t:
            return 'Monocular VO/SLAM'
        if 'stereo' in t:
            return 'Stereo VO/SLAM'
        if 'rgb-d' in t or 'rgbd' in t:
            return 'RGB-D SLAM'
        if 'place recognition' in t:
            return 'VPR-augmented Visual SLAM'
        return 'General Visual SLAM'

    if order == 'LiDAR SLAM/Odometry':
        if 'loam' in t and 'fast-loam' not in t:
            return 'LOAM Family'
        if 'fast-lio' in t or 'fastlio' in t:
            return 'FAST-LIO Family'
        if 'lio-sam' in t or 'lego-loam' in t:
            return 'LIO-SAM / LeGO-LOAM Family'
        if 'continuous-time' in t:
            return 'Continuous-time LiDAR SLAM'
        return 'General LiDAR SLAM'

    if order == 'Visual-Inertial Odometry/SLAM (VIO)':
        if 'vins' in t:
            return 'VINS Family'
        if 'okvis' in t:
            return 'OKVIS Family'
        if 'rovio' in t:
            return 'ROVIO Family'
        if 'msckf' in t:
            return 'MSCKF Family'
        if 'preintegration' in t:
            return 'Preintegration-based VIO'
        return 'General VIO'

    if order == 'LiDAR-Inertial Odometry/SLAM (LIO)':
        if 'fast-lio' in t or 'fastlio' in t:
            return 'FAST-LIO Family'
        if 'lio-sam' in t:
            return 'LIO-SAM Family'
        if 'tightly coupled' in t:
            return 'Tightly-coupled LIO'
        return 'General LIO'

    if order == 'General Localization':
        if 'multi-robot' in t or 'cooperative' in t:
            return 'Cooperative Localization'
        if 'underwater' in t:
            return 'Underwater Localization'
        if 'aerial' in t or 'uav' in t:
            return 'Aerial Localization'
        if 'humanoid' in t:
            return 'Humanoid Localization'
        if 'particle filter' in t:
            return 'Particle Filter Localization'
        if 'mcl' in t or 'monte carlo' in t:
            return 'Monte Carlo Localization'
        if 'bayesian' in t:
            return 'Bayesian Localization'
        return 'General Localization'

    if order == 'Sensor Calibration':
        if 'extrinsic' in t:
            return 'Extrinsic Calibration'
        if 'intrinsic' in t:
            return 'Intrinsic Calibration'
        if 'multi-sensor' in t or 'multisensor' in t:
            return 'Multi-sensor Calibration'
        return 'General Sensor Calibration'

    if order == 'Bayesian Filtering':
        if 'extended kalman' in t or ' ekf' in t:
            return 'EKF / Extended Kalman'
        if 'unscented' in t or 'ukf' in t:
            return 'UKF / Unscented Kalman'
        if 'particle filter' in t or 'rao-blackwell' in t \
                or 'fastslam' in t:
            return 'Particle Filter'
        if 'invariant' in t or 'iekf' in t:
            return 'Invariant EKF'
        return 'General Bayesian Filter'

    # ============================================================
    # PERCEPTION & SENSING
    # ============================================================
    if order == 'Tactile Sensors / Algorithms':
        if 'gelsight' in t:
            return 'GelSight'
        if 'visuotactile' in t or 'visuo-tactile' in t \
                or 'visuo tactile' in t or 'vision-based tactile' in t:
            return 'Visuo-Tactile'
        if 'event' in t or 'evetac' in t:
            return 'Event-based Tactile'
        if 'eit' in t or 'electrical impedance tomography' in t:
            return 'EIT-based Skin'
        if 'slip' in t:
            return 'Slip Detection'
        if 'whisker' in t:
            return 'Whisker Sensor'
        if 'biotac' in t:
            return 'BioTac'
        return 'General Tactile Sensor'

    if order == 'Pose Estimation':
        if '6d' in t or '6-d' in t or '6dof' in t or '6-dof' in t:
            return '6D / 6-DoF Pose'
        if 'human pose' in t:
            return 'Human Pose'
        if 'pnp' in t or 'perspective-n-point' in t:
            return 'PnP / Camera Pose'
        return 'General Pose Estimation'

    if order == 'Point Cloud Processing':
        if 'segmentation' in t:
            return 'Point Cloud Segmentation'
        if 'detection' in t:
            return 'Point Cloud Detection'
        if 'registration' in t:
            return 'Point Cloud Registration'
        if 'compression' in t:
            return 'Point Cloud Compression'
        return 'General Point Cloud'

    if order == 'Point Cloud Registration':
        if 'icp' in t or 'iterative closest' in t:
            return 'ICP-family'
        if 'ndt' in t:
            return 'NDT-family'
        if 'teaser' in t or 'certifiable' in t:
            return 'Certifiable Registration (TEASER)'
        return 'General Registration'

    # ============================================================
    # ROBOT DESIGN & HARDWARE
    # ============================================================
    if order == 'Parallel Mechanism':
        if 'stewart' in t or 'gough' in t or 'gough-stewart' in t:
            return 'Stewart-Gough Platform'
        if 'delta' in t:
            return 'Delta Robot'
        if 'cable' in t or 'wire' in t:
            return 'Cable-driven Parallel'
        if 'singularity' in t:
            return 'Parallel Singularity Analysis'
        if 'kinematic' in t:
            return 'Parallel Kinematics'
        return 'General Parallel Mechanism'

    if order == 'Cable-driven Parallel Robot':
        if 'wrench' in t or 'workspace' in t:
            return 'Wrench/Workspace Analysis'
        if 'tension' in t:
            return 'Tension Distribution'
        if 'control' in t:
            return 'Cable Robot Control'
        if 'design' in t:
            return 'Cable Robot Design'
        return 'General Cable-driven Parallel'

    if order == 'Continuum Manipulator':
        if 'tendon' in t:
            return 'Tendon-driven Continuum'
        if 'pneumatic' in t or 'hydraulic' in t or 'fluidic' in t:
            return 'Fluidic Continuum'
        if 'cosserat' in t:
            return 'Cosserat-Rod Model'
        if 'multisection' in t or 'multi-section' in t:
            return 'Multi-section Continuum'
        if 'magnetic' in t:
            return 'Magnetic Continuum'
        return 'General Continuum'

    if order == 'Soft Robot Design':
        if 'gripper' in t or 'hand' in t:
            return 'Soft Gripper'
        if 'crawl' in t or 'inchworm' in t or 'snake' in t:
            return 'Soft Crawling/Snake'
        if 'fish' in t or 'swim' in t or 'aquatic' in t:
            return 'Soft Swimmer'
        if 'wearable' in t or 'exo' in t:
            return 'Soft Wearable'
        return 'General Soft Robot'

    if order == 'Modular / Reconfigurable':
        if 'self-reconfig' in t or 'self reconfig' in t:
            return 'Self-Reconfigurable'
        if 'modular' in t and 'control' in t:
            return 'Modular Control'
        if 'modular' in t and 'design' in t:
            return 'Modular Design'
        return 'General Modular'

    if order == 'Bio-inspired Mechanism':
        if 'wing' in t or 'flapping' in t:
            return 'Wing / Flapping Mechanism'
        if 'finger' in t or 'hand' in t:
            return 'Bio-inspired Hand'
        if 'leg' in t:
            return 'Bio-inspired Leg'
        return 'General Bio-inspired Mechanism'

    # ============================================================
    # CONTROL
    # ============================================================
    if order == 'Robot Control':
        if 'redundant' in t:
            return 'Redundant Robot Control'
        if 'mobile' in t:
            return 'Mobile Robot Control'
        if 'aerial' in t or 'quadrotor' in t:
            return 'Aerial Robot Control'
        if 'underwater' in t:
            return 'Underwater Robot Control'
        if 'manipulator' in t:
            return 'Manipulator Control'
        if 'safe' in t:
            return 'Safe Robot Control'
        return 'General Robot Control'

    if order == 'Visual Servoing':
        if 'image-based' in t or 'ibvs' in t:
            return 'Image-based (IBVS)'
        if 'position-based' in t or 'pbvs' in t:
            return 'Position-based (PBVS)'
        if 'photometric' in t or 'direct' in t:
            return 'Direct / Photometric VS'
        if 'aerial' in t or 'quadrotor' in t:
            return 'Aerial VS'
        if 'mobile' in t or 'unicycle' in t or 'nonholonomic' in t:
            return 'Mobile Robot VS'
        if 'parallel' in t or 'gough' in t or 'stewart' in t:
            return 'Parallel Manipulator VS'
        if 'tactile' in t:
            return 'Tactile Servoing'
        if 'aural' in t or 'auditory' in t:
            return 'Aural Servoing'
        if 'thermal' in t or 'radiation' in t:
            return 'Thermal Servoing'
        return 'General Visual Servoing'

    # ============================================================
    # HRI
    # ============================================================
    if order == 'General HRI':
        if 'safe' in t or 'safety' in t:
            return 'Safety in HRI'
        if 'trust' in t:
            return 'Trust in HRI'
        if 'collaboration' in t or 'collab' in t:
            return 'Human-Robot Collaboration'
        if 'augmentation' in t or 'augment' in t:
            return 'Human Augmentation'
        if 'evaluation' in t or 'study' in t:
            return 'HRI User Study'
        return 'General HRI'

    if order == 'General Teleoperation':
        if 'underwater' in t:
            return 'Underwater Teleoperation'
        if 'surgical' in t or 'surgery' in t:
            return 'Surgical Teleoperation'
        if 'mobile' in t:
            return 'Mobile Robot Teleop'
        if 'humanoid' in t:
            return 'Humanoid Teleop'
        return 'General Teleoperation'

    if order == 'Exoskeleton / Wearable':
        if 'lower' in t or 'leg' in t or 'knee' in t or 'ankle' in t \
                or 'hip' in t:
            return 'Lower-limb Exoskeleton'
        if 'upper' in t or 'arm' in t or 'shoulder' in t or 'elbow' in t:
            return 'Upper-limb Exoskeleton'
        if 'back' in t or 'spine' in t or 'lifting' in t:
            return 'Back / Spine Exoskeleton'
        if 'hand' in t or 'finger' in t or 'thumb' in t \
                or 'wrist' in t:
            return 'Hand / Wrist Exoskeleton'
        return 'General Exoskeleton'

    if order == 'Collaborative Robot / Co-manipulation':
        if 'safe' in t or 'safety' in t:
            return 'Safe Collaboration'
        if 'industrial' in t or 'assembly' in t:
            return 'Industrial Collaboration'
        if 'object' in t or 'transport' in t:
            return 'Co-Transport / Co-Carry'
        return 'General Collaboration'

    # ============================================================
    # MULTI-ROBOT
    # ============================================================
    if order == 'Multi-Robot Coordination':
        if 'distributed' in t:
            return 'Distributed Coordination'
        if 'consensus' in t:
            return 'Consensus-based'
        if 'cooperative' in t and 'manipulation' in t:
            return 'Cooperative Manipulation'
        if 'cooperative' in t and 'transport' in t:
            return 'Cooperative Transport'
        if 'task' in t and 'allocation' in t:
            return 'Task Allocation'
        return 'General Coordination'

    if order == 'Pursuit-Evasion / Surveillance / Patrolling':
        if 'pursuit' in t:
            return 'Pursuit-Evasion'
        if 'patrol' in t:
            return 'Patrolling'
        if 'surveillance' in t:
            return 'Surveillance'
        if 'persistent' in t and 'monitoring' in t:
            return 'Persistent Monitoring'
        if 'perimeter' in t:
            return 'Perimeter Defense'
        if 'herding' in t:
            return 'Herding'
        return 'General Pursuit / Surveillance'

    if order == 'Swarm':
        if 'aerial' in t or 'drone' in t or 'uav' in t:
            return 'Aerial Swarm'
        if 'magnetic' in t or 'micro' in t:
            return 'Microrobot Swarm'
        if 'aggregation' in t or 'formation' in t:
            return 'Swarm Aggregation / Formation'
        return 'General Swarm'

    # ============================================================
    # LEARNING
    # ============================================================
    if order == 'RL':
        if 'safe' in t:
            return 'Safe RL'
        if 'multi-agent' in t or 'multiagent' in t:
            return 'Multi-agent RL'
        if 'inverse' in t:
            return 'Inverse RL'
        if 'hierarchical' in t:
            return 'Hierarchical RL'
        if 'offline' in t:
            return 'Offline RL'
        if 'meta' in t:
            return 'Meta RL'
        return 'General RL'

    if order == 'Sim-to-Real':
        if 'quadruped' in t or 'cassie' in t or 'biped' in t \
                or 'humanoid' in t:
            return 'Sim-to-Real Locomotion'
        if 'manipulation' in t or 'grasp' in t:
            return 'Sim-to-Real Manipulation'
        if 'aerial' in t or 'drone' in t:
            return 'Sim-to-Real Aerial'
        if 'domain randomization' in t:
            return 'Domain Randomization'
        return 'General Sim-to-Real'

    if order == 'Behavior Cloning / LfD / PbD':
        if 'human video' in t or 'in-the-wild' in t \
                or 'in the wild' in t or 'youtube' in t:
            return 'In-the-Wild / Human Video IL'
        if 'dexterous' in t or 'dexcap' in t:
            return 'Dexterous IL'
        if 'multi-task' in t or 'multi task' in t:
            return 'Multi-task IL'
        return 'General Behavior Cloning / LfD'

    if order == 'Vision-Language-Action (VLA)':
        if 'rt-1' in t or 'rt-2' in t or 'rt-h' in t:
            return 'RT-series'
        if 'pi-zero' in t or ' π₀' in t or 'π₀' in t \
                or 'pi 0' in t:
            return 'π₀-family'
        if 'octo' in t and 'octopi' not in t:
            return 'Octo / OpenVLA-family'
        if 'navila' in t or 'navid' in t:
            return 'Vision-Language Navigation'
        return 'General VLA'

    if order == 'Diffusion Policies / Flow Matching':
        if '3d diffusion' in t or '3-d diffusion' in t:
            return '3D Diffusion Policy'
        if 'consistency' in t:
            return 'Consistency Policy / Distillation'
        if 'flow matching' in t:
            return 'Flow Matching Policy'
        if 'hierarchical' in t:
            return 'Hierarchical Diffusion Policy'
        return 'General Diffusion Policy'

    # ============================================================
    # APPLICATION DOMAINS
    # ============================================================
    if order == 'Surgical Robot':
        if 'minimally invasive' in t or ' mis ' in t:
            return 'Minimally Invasive Surgery'
        if 'autonomous' in t:
            return 'Autonomous Surgery'
        if 'training' in t or 'simulator' in t:
            return 'Surgical Training / Simulation'
        return 'General Surgical Robot'

    if order == 'Self-driving Vehicle / Decision Making':
        if 'imitation' in t:
            return 'IL-based Driving'
        if 'reinforcement' in t:
            return 'RL-based Driving'
        if 'mpc' in t or 'predictive' in t:
            return 'MPC for Driving'
        if 'game' in t:
            return 'Game-theoretic Driving'
        if 'safety' in t or 'safe' in t:
            return 'Safe Autonomous Driving'
        return 'General Self-driving'

    # ============================================================
    # THEORETICAL
    # ============================================================
    if order == 'Kinematic Analysis':
        if 'parallel' in t or 'stewart' in t or 'gough' in t:
            return 'Parallel Kinematics'
        if 'redundant' in t:
            return 'Redundant Kinematics'
        if 'continuum' in t:
            return 'Continuum Kinematics'
        if 'mobile' in t or 'wheeled' in t:
            return 'Mobile Robot Kinematics'
        if 'screw' in t or 'lie' in t:
            return 'Screw / Lie Theory'
        return 'General Kinematics'

    if order == 'Robot Dynamics':
        if 'flexible' in t:
            return 'Flexible Robot Dynamics'
        if 'parallel' in t:
            return 'Parallel Robot Dynamics'
        if 'multi-body' in t or 'multibody' in t:
            return 'Multi-body Dynamics'
        if 'newton-euler' in t or 'rnea' in t:
            return 'Newton-Euler / RNEA'
        if 'recursive' in t:
            return 'Recursive Dynamics'
        if 'real-time' in t:
            return 'Real-time Dynamics'
        return 'General Robot Dynamics'

    if order == 'Optimization Methods':
        if 'convex' in t:
            return 'Convex Optimization'
        if 'mixed-integer' in t or 'milp' in t:
            return 'Mixed-Integer'
        if 'distributed' in t:
            return 'Distributed Optimization'
        if 'robust' in t:
            return 'Robust Optimization'
        return 'General Optimization'

    # Default fallback
    return '(general)'
