"""
Robotics Phylogenetic Taxonomy Classifier — Final Version
==========================================================
Maps 7,477 paper titles into a 4-level taxonomy:
  Phylum (대분류) > Class (중분류) > Order (소분류) > Genus (세부)

13 Phylum, ~95 Class, ~330 Order. See TAXONOMY.md for full tree.

Rules are ordered by specificity. Earlier rules win.
The patterns encode SEMANTIC equivalence (synonym clusters), not TF-IDF.
"""
import json
import re
from collections import Counter
from genus_rules import assign_genus

# ---------- Helper ----------
def t_low(s):
    return ' ' + s.lower() + ' '

def has_any(t, kws):
    return any(k in t for k in kws)

def has_all(t, kws):
    return all(k in t for k in kws)

# ============================================================
# Vocabulary clusters (semantic equivalence groups)
# ============================================================

# --- Sensors / Modalities
LIDAR = ['lidar', 'lidars', ' lidar-', 'laser scan', 'laser-based', 'laser scanner',
         'point cloud', 'point-cloud', 'pointcloud', '3d point',
         'range scan', 'range image', 'range sensor', 'ladar']
RADAR = ['radar', 'mmwave', 'millimeter wave', 'millimeter-wave', 'fmcw', '4d radar',
         'mmw radar']
SONAR = ['sonar', 'acoustic camera', 'acoustic imag', 'ultrasonic',
         'echolocation', 'side scan', 'acoustic ray']
EVENT_CAM = ['event camera', 'event-based vision', 'event-based',
             'event-driven vision', 'spiking camera', 'dynamic vision sensor',
             ' dvs ', 'neuromorphic vision', 'event cameras']
DEPTH_CAM = ['rgb-d', 'rgbd', 'depth camera', 'depth sensor',
             'kinect', 'stereo camera', 'stereo vision']
VISUAL = ['visual', 'vision', 'image', 'images', 'rgb', 'camera', 'cameras',
          'monocular', 'stereo', 'photometric']
TACTILE = ['tactile', 'gelsight', 'taxel', 'haptic sensor', 'touch sensor',
           'skin sensor', 'visuotactile', 'visuo-tactile', 'visuo tactile',
           'whisker', 'fingertip force', 'biotac', 'tactile-reactive']
IMU = [' imu ', ' imu-', 'imu-based', 'inertial measurement',
       'inertial sensor', 'gyroscope', 'accelerometer', 'inertial-aided',
       'inertial measurement unit']
GNSS = ['gnss', ' gps ', 'gps-', '-gps', 'global navigation satellite']
UWB = ['uwb', 'ultra-wideband', 'ultrawideband', 'ultra wideband']

# --- SLAM / Localization
PLACE_RECOG = ['place recognition', 'loop closure', 'loop detection',
               'loop-closure', 'loop-detection', 'loop closing',
               're-localization', 'relocalization', 'global localization',
               'visual localization', 'image retrieval for', 'topological localization',
               'place categorization', 'visual place', ' vpr ', 'pr by pe']
SLAM_KW = [' slam ', 'slam-', '-slam', 'simultaneous localization',
           'simultaneous localisation', ' lio ', '-lio', 'lio-', ' vio ', 'vio ',
           '-vio', 'vio-', 'vins', 'orb-slam', 'fast-lio', 'fast-livo',
           'visual-inertial odometry', 'visual inertial odometry',
           'lidar-inertial', 'lidar inertial', 'lio-sam',
           'visual odometry', 'lidar odometry', 'inertial odometry',
           'okvis', 'mapping and localization', 'lvi', 'vi-slam',
           'd2slam', 'kimera', 'iSAM', 'gtsam']
NEURAL_SLAM = ['nerf-slam', 'gaussian splat', 'gaussian-splat', 'splatting',
               'pin-slam', 'gs-slam', 'neural implicit', 'implicit neural',
               'hi-slam', 'gs-livo', 'vings-mono', 'splat-nav']
KALMAN = ['kalman', ' ekf ', ' ekf-', 'ekf-', '-ekf', 'ekf based',
          ' ukf ', 'iekf', 'invariant ekf', 'extended kalman',
          'unscented kalman', 'particle filter', 'monte carlo localization',
          ' mcmc', 'sequential monte carlo', 'particle filtering',
          'rao-blackwell', 'square root sam', 'square root inverse',
          'fastslam']
POSEGRAPH = ['pose graph', 'pose-graph', 'factor graph', 'factor-graph',
             'bundle adjustment', 'bundle-adjustment',
             'maximum a posteriori', ' map estimation',
             'iSAM', 'graph slam', 'graph optimization',
             'pose graph optimization', 'incremental smoothing']
CALIB = ['calibration', 'extrinsic calibration', 'intrinsic calibration',
         'hand-eye', 'hand eye', 'kalibr']

# --- Manipulation
GRASP = ['grasp', 'grasping', 'grasps', 'grasper', 'gripper', 'grippers',
         'pick-and-place', 'pick and place', 'bin picking', 'bin-picking',
         'pick success', 'graspnet', 'dex-net']
DEX_MANIP = ['dexterous', 'dexter', 'in-hand manipulation', 'in hand manipulation',
             'in-hand', 'multi-finger', 'multifinger', 'multi-fingered',
             'multifingered', 'anthropomorphic hand', 'anthropomorphic gripper',
             'finger gait', 'fingertip']
BIMAN = ['bimanual', 'two-handed', 'dual arm', 'dual-arm', 'dualarm',
         'two-arm', 'two arm', 'dual-master', 'two-fingered']
DEFORM = ['deformable', 'deformation', 'cloth', 'fabric', 'rope',
          'cable manip', 'cables manipulation', 'soft object manipulation',
          'soft body', 'plasticine', 'elastoplastic', 'liquid',
          'granular', 'food handling', 'dough', 'gel', 'flexible needle',
          'soft tissue', 'fabric manipulation', 'garment', 'dress',
          'cloth manipulation', 'unknotting', 'knot tying', 'cable manipulation',
          'untangling', 'wire']
ASSEMBLY = ['assembly', 'assemble', 'peg-in-hole', 'peg in hole',
            'insertion', 'insert ', 'snap-fit', 'screw', 'unscrew',
            'disassembly', 'mating', 'industreal', 'automate',
            'fastening', 'parts feeding', 'parts feeder', 'parts orient',
            'parts sorting']
NONPRE = ['pushing', 'pushing manipulation', 'non-prehensile', 'nonprehensile',
          'non prehensile', 'tossing', 'throwing', 'rolling manipulation',
          'sliding manipulation', 'tossnet', 'tossingbot']
TOOL_USE = ['tool use', 'tool-use', 'tool manipulation', 'tool affordance']
SUCTION = ['suction', 'suction cup', 'vacuum gripper', 'vacuum gripping',
           'sim-suction']
LIQUID_GRAN = ['liquid', 'fluid', 'pouring', 'granular material',
               'cloaking', 'paste', 'plasticine', 'elasto-plastic',
               'elastoplastic']
KNOT_CABLE = ['knot', 'knot tying', 'knot-tying', 'untangling',
              'cable manipulation', 'cable manipulati', 'wire manipulation',
              'rope manipulation']
DIST_MANIP = ['distributed manipulation', 'programmable force field',
              'parts feeder', 'parts feeders', 'parts feeding',
              'vibratory feeder', 'parts orient', 'parts sorting',
              'fixture loading', 'fixturing']
MOBILE_MANIP = ['mobile manipulation', 'mobile manipulator',
                'whole-body manipulation', 'loco-manipulation',
                'loco manipulation', 'locomanipulation']
AERIAL_MANIP = ['aerial manipulation', 'aerial grasp', 'aerial-tethered',
                'aerial manipulator']
ARTIC_OBJ = ['articulated object', 'articulated objects', 'flowbot', 'articubot',
             'articulated furniture', 'articulated-object',
             'articulated structures']

# --- Locomotion platforms
QUAD = ['quadruped', 'four-legged', 'four legged', 'quadrupedal',
        'cheetah', 'anymal', 'spot ', 'go1 ', 'mini cheetah']
BIPED = ['bipedal', ' biped ', 'biped robot', 'biped walk',
         'humanoid', 'humanoids', 'two-legged', 'cassie', 'atrias',
         'asimo', ' h-lip', 'h-lip ', 'mabel ', 'rabbit ']
HEXAPOD = ['hexapod', 'six-legged', 'six legged', 'rhex',
           'multi-legged', 'multilegged', 'multilimb',
           'multi-limb']
LEGGED_GEN = ['legged', 'legged robot', 'legged locomotion', 'leg robot',
              'legged system', 'multi-legged']
WHEELED = ['wheeled', 'wheelchair', 'differential drive',
           'differential-drive', 'mecanum', 'omnidirectional',
           'omni-directional', 'skid-steer', 'skid steer', 'ackermann']
CARLIKE = ['autonomous vehicle', 'autonomous vehicles', 'autonomous car',
           'self-driving', 'self driving', 'autonomous driving',
           'autonomous ground vehicle', 'autonomous truck',
           'driverless', 'autonomous bus', 'autonomous racing',
           'self-driving cars', 'urban driving']
UAV = ['quadrotor', 'multirotor', 'multi-rotor', 'multicopter',
       ' mav ', '-mav', 'mav-', ' uav', 'uav ', 'uav-', 'uavs',
       'drone', 'drones', 'aerial robot', 'aerial robotic',
       'aerial vehicle', 'aerial vehicles', 'aerial swarm',
       'flapping-wing', 'flapping wing', 'flapping flight',
       'fixed-wing', 'fixed wing', 'tail-sitter', 'tailsitter',
       'tail sitter', 'helicopter', 'tiltrotor', 'vtol', 'micro air',
       'micro-aerial', 'micro aerial', 'pico air', 'aerial autonomy',
       'aerial ', 'flying', 'quadcopter', 'tricopter', 'hexacopter']
UNDER = ['underwater', ' auv ', '-auv', 'auv-', ' uuv ', 'uuv-',
         'submarine', 'submersible', ' rov ', '-rov', 'rov-', 'subsea',
         'underwater vehicle', 'scuba', 'aquatic']
SURFACE = ['surface vessel', 'surface ship', 'surface vehicle',
           ' asv ', '-asv', ' usv ', '-usv', 'unmanned surface',
           ' boat ', 'boats', 'autonomous boat', 'autonomous ship',
           'sailboat', 'autonomous surface', 'maritime']
SPACE = ['space robot', 'space robotic', 'space manipulator',
         'planetary', 'martian', 'lunar', 'mars rover',
         'planetary rover', 'extraterrestrial', 'asteroid',
         'spacecraft', 'on-orbit', 'orbital', 'satellite servicing',
         'free-flying', 'cubesat', 'rocky 7', 'antarctic meteorite']
SAR = ['search and rescue', 'search-and-rescue', 'rescue robot',
       'disaster', 'urban search']
DOMESTIC = ['domestic robot', 'household', 'home robot',
            'cleaning robot', 'service robot', 'butler robot',
            'personal robot', 'museum robot', 'tour-guide']
LOGI = ['warehouse', 'logistics', 'parcel sorting', 'package delivery',
        'delivery robot', 'amazon picking']

# --- Bio-inspired locomotion
SNAKE_LOC = ['snake robot', 'snake-like robot', 'serpentine robot',
             'snake like robot', 'snake locomotion', 'sidewinding']
CLIMB_LOC = ['climbing robot', 'wall-climbing', 'wall climbing',
             'pole-climbing', 'pole climbing', 'tree-climbing',
             'tree climbing', 'climbing parallel', 'gecko',
             'spider robot', 'free-climbing']
JUMP_LOC = ['jumping robot', 'hopping robot', 'leaping',
            'salto', 'flea-inspired', 'water strider', 'jumping scout',
            'minimalist jumping']
FISH_LOC = ['fish robot', 'robotic fish', 'swimming robot',
            'fish-like', 'fishlike', 'eel-like', 'eel robot',
            'bionic fish', 'biomimetic robotic fish', 'fish locomotion']
CRAWL_LOC = ['crawling robot', 'inchworm', 'earthworm',
             'metameric', 'metameric robot', 'undulatory robot',
             'caterpillar']
SAND_LOC = ['sand-swimming', 'sandfish', 'granular locomotion',
            'sand swimmer', 'fluidizing ground']

# --- Hardware / Robots
SOFT_ROBOT = ['soft robot', 'soft robotic', 'soft actuator',
              'soft pneumatic', 'pneumatic actuator', 'soft gripper',
              'soft hand', 'origami robot', 'origami', 'jamming',
              'variable stiffness', 'variable-stiffness',
              'compliant actuator', 'soft material', 'silicone actuator',
              'fluidic actuator', 'inflatable', 'shape-memory',
              'shape memory alloy', ' sma ', 'sma-', '-sma',
              'sma actuator', 'dielectric elastomer', 'electroactive polymer',
              'soft sensor', 'soft skin', 'mckibben',
              'pneumatic muscle', 'fiber-reinforced', 'pneunets',
              'pneu-net', 'soft actuators', 'soft pneumatic actuator',
              'soft millirob', 'soft milli', 'fluidic elastomer',
              'soft continuum', 'hasel', 'electrostatic actuator',
              'electroadhesion', 'twisted coiled', 'twisted-coiled',
              'twisted string', 'tcp actuator', 'fin ray',
              'soft polyhedral']
CONTINUUM = ['continuum robot', 'continuum manipulator', 'continuum joint',
             'tendon-driven continuum', 'concentric tube', 'concentric-tube',
             'cosserat', 'snake-arm', 'snake arm', 'multisection',
             'multi-section', 'continuum arm', 'continuum tool',
             'flexible robotic mechanism', 'tendon-driven robotic',
             'flexible needle', 'steerable needle', 'precurved-tube',
             'concentric push-pull', 'eccentric tube']
PARALLEL = ['parallel robot', 'parallel manipulator', 'parallel mechanism',
            'parallel mechanisms', 'stewart platform', 'delta robot',
            'parallel kinematic', 'cable-driven parallel',
            'cable driven parallel', 'cable robot', 'gough-stewart',
            'gough stewart', 'stewart-gough', 'parallel-wire',
            'parallel manipulators', 'cable-suspended',
            'cable robots', 'cable-driven', 'wire-driven']
TENSEGRITY = ['tensegrity']
GROWING_ROBOT = ['growing robot', 'growing soft', 'vine robot',
                 'vine-inspired', 'tip-growing']
MICRO = ['microrobot', 'micro-robot', 'micro robot', 'microrobotic',
         'nanorobot', 'nano-robot', 'nanorobotic', 'microscale robot',
         'microswimmer', 'micro swimmer', 'magnetic microbot',
         'magnetic robot', 'magnetic actuation', 'microbot',
         'magnetic helical', 'milliswimmer', 'milli-swimmer',
         'millirobot', 'milli-robot', 'micromotion',
         'magnetic microrob', 'paramagnetic', 'magnetotactic',
         'biomicroirobot', 'magnetic capsule', 'magnetic flexible',
         'magnetic continuum', 'flagellated', 'magnetic tweezer',
         'optical tweezer', 'magnetic dipole', 'magnetic millirobot',
         'magnetic microswarm', 'untethered magnetic']
BIOHYBRID = ['biohybrid', 'bio-hybrid', 'bacteria-driven',
             'cell-based robot', 'living robot', 'biological actuator',
             'muscle-actuated', 'muscle actuated', 'cyborg',
             'insect-computer hybrid', 'magnetotactic bacteria']
MODULAR = ['modular robot', 'modular reconfigurable', 'reconfigurable robot',
           'self-reconfigurable', 'self reconfigurable', 'self-assembly',
           'self assembly', 'm-tran', 'self-disassembly', 'modules',
           'modular self', 'modular system', 'self-reconfiguration',
           'modular robotic']
PARALLEL_CONT = ['parallel continuum']

# --- HRI / Assistive
EXOSKEL = ['exoskeleton', 'exo-skeleton', 'exosuit', 'exo-suit',
           'wearable robot', 'wearable exo', 'powered orthosis',
           'orthotic', 'wearable robotic', 'powered orthotic']
SOFT_EXO = ['soft exosuit', 'soft exo', 'exosuit', 'soft robotic suit',
            'soft wearable']
HAND_EXO = ['hand exoskeleton', 'hand-exoskeleton', 'finger exoskeleton',
            'thumb exoskeleton', 'glove exoskeleton', 'wearable hand',
            'wearable robotic finger', 'robotic glove']
PROST = ['prosthesis', 'prosthetic', 'prostheses', 'amputee',
         'transfemoral', 'transhumeral', 'transtibial',
         'prosthetic hand', 'prosthetic leg', 'prosthetic knee',
         'prosthetic ankle', 'prosthetic wrist']
REHAB = ['rehabilitation', ' rehab ', 'physical therapy',
         'gait rehabilitation', 'stroke recovery', 'neurorehabilitation',
         'rehab robot', 'rehab device', 'rehabilitative']
SURG = ['surgical robot', 'surgical robotic', ' surgery', 'surgery ',
        'surgical', 'da vinci', 'minimally invasive',
        'laparoscopic', 'endoscop', 'catheter', 'biopsy',
        'needle insertion', 'needle steering', 'needle-steering',
        'colonoscopy', 'cardiac', 'tumor', 'medical robot',
        'medical robotic', 'percutaneous', 'orthopedic',
        'da-vinci', 'raven ii', 'beating heart', 'brachytherapy',
        'neurosurg', 'microsurg', 'capsule endoscope',
        'capsule colonoscope', 'image-guided', 'mri-compatible',
        'mri-guided', 'mri-driven', 'transendoscopic']
MED_ROBOT = ['medical robot', 'medical robotic', 'medical imag',
             'medical interv', 'medical mini', 'breast biopsy']
TELEOP = ['teleoperation', 'tele-operation', 'teleop', 'tele-op',
          'remote operation', 'master-slave', 'master slave',
          'haptic teleoperation', 'bilateral teleoperation', 'tele-impedance',
          'telemanipulation', 'tele-manipulation', 'telerobot',
          'teleoperat', 'telemicromanipulation', 'telesurgery',
          'master/slave', 'remote control']
SHARED_AUT = ['shared autonomy', 'shared control', 'mixed-initiative',
              'human-in-the-loop', 'human in the loop', 'shared aut',
              'cooperative control', 'safemimic']
SOC_HRI = ['social robot', 'social robotic', 'humanoid social',
           'companion robot', 'autism', ' asd ', 'social interaction',
           'social navigation', 'pedestrian', 'crowd-aware',
           'crowd aware', 'crowd navigation', 'socially assistive',
           'socially-assistive', 'social robotics', 'sociopsychological',
           'humanoid robot social', 'tour-guide', 'socially compliant',
           'socially aware', 'socially-aware', 'paro robot']
COBOT = ['collaborative robot', 'cobot', 'human-robot collaboration',
         'human robot collaboration', 'co-manipulation', 'co manipulation',
         'physical human-robot', 'physical human robot',
         'physical interaction', 'collaborative manipulation',
         'physical hri', 'phri', 'human-collaborative']
HAPTICS = ['haptic rendering', 'haptic feedback', 'haptic interface',
           'haptic device', 'haptic display', 'haptic interaction',
           'haptic transparency', 'haptic glove', 'haptic shape',
           'haptic search', 'haptic rendering', 'haptic exploration',
           'haptics enabled', 'haptic-enabled', 'haptify',
           'cobotic hand controller', 'force-feedback', 'force feedback']
BCI = ['brain-machine interface', 'brain machine interface',
       ' bmi ', 'brain-computer', 'brain computer', ' bci ',
       'p300', 'eeg-controlled', 'eeg controlled', 'brain-actuated',
       'brain actuated', 'electroencephalogram']
EMG = [' emg ', '-emg', 'emg-', 'electromyograph', 'myoelectric',
       'sonomyography', 'semg', 'neuroprosthetic', 'neuromuscular control']

# --- Multi-robot
SWARM = ['swarm', 'swarming', 'swarm robotic', 'swarms', 'swarm of']
MULTI_R = ['multi-robot', 'multirobot', 'multi robot', 'multiagent',
           'multi-agent', 'multi agent', 'multi-vehicle', 'multivehicle',
           'multi-uav', 'multi-quadrotor', 'multi-arm', 'multiarm']
FORMATION = ['formation control', 'formation flying', 'formation flight',
             'formation reshaping', 'flocking', 'rendezvous',
             'consensus control', 'leader-follower', 'leader follower',
             'follower formation', 'distributed formation',
             'formation maneuver']
TASK_ALLOC = ['task allocation', 'task assignment', 'auction-based',
              'auction based', 'task scheduling', 'multi-robot task',
              'task swap']
PURSUIT = ['pursuit-evasion', 'pursuit evasion', 'evader', 'pursuer',
           'patrolling', 'surveillance', 'perimeter defense',
           'perimeter guard', 'orienteer', 'orienteers', 'herding',
           'reach-avoid', 'monitoring', 'persistent monitoring',
           'persistent task']
MAPF = ['multi-agent path', 'multi-robot path planning', 'mapf',
        'multi robot path', 'conflict-based search', 'conflict based search',
        ' cbs ']
RESILIENT = ['resilient', 'byzantine', 'attack-resilient',
             'attack-robust', 'adversary', 'adversarial robot',
             'resilience', 'malicious robot', 'attack-resilient',
             'spoof', 'misbehavior monitor', 'crowd vetting']
AERIAL_SWARM = ['aerial swarm', 'aerial swarms', 'multi-rotor swarm',
                'drone swarm', 'multi-quadrotor', 'quadrotor swarm',
                'omni-swarm', 'swarm-lio', 'aerial swarm robotics']

# --- Learning
RL = ['reinforcement learning', 'reinforcement-learning', ' rl ', 'rl-based',
      'rl based', ' drl ', 'drl-', 'q-learning', 'policy gradient',
      'actor-critic', 'actor critic', ' sac ', ' ppo ', ' td3 ', ' dqn',
      'value iteration', 'value-iteration', 'reward learning',
      'rl ', 'reinforcement', 'q-graph', 'reward function',
      'qt-opt', 'reinforced fine-tuning', 'rlhf']
IL = ['imitation learning', 'imitation-learning', 'behavioral cloning',
      'behavior cloning', 'learning from demonstration', 'lfd ', ' lfd',
      'demonstration learning', 'expert demonstration',
      'imitation', 'mimic', 'learning from human', 'learn from demo']
PBD = ['programming by demonstration', 'programing by demonstration',
       'programming by human demonstration', 'pbd ', 'demonstration learning']
SIM2REAL = ['sim-to-real', 'sim to real', 'sim2real', 'simtoreal',
            'domain randomization', 'reality gap', 'real-to-sim',
            'real to sim', 'sim and real', 'sim-and-real']
INV_RL = ['inverse reinforcement', 'inverse rl', ' irl ', '-irl ',
          'inverse optimal control']
META_LEARN = ['meta-learning', 'meta learning', 'few-shot', 'few shot',
              'meta-learn']
TRANSFER_L = ['transfer learning', 'domain adaptation']
CONTINUAL = ['continual learning', 'lifelong learning', ' continual ',
             ' lifelong ']
VLA = ['vision-language-action', 'vision language action', ' vla ',
       '-vla ', 'vla-', 'vla ', 'vla ', 'language-conditioned',
       'language conditioned', 'language-grounded',
       'vlm-generated', 'language-augmented', 'vision-and-language']
LLM = [' llm ', ' llms ', 'llm-', 'large language model',
       'large language models', 'gpt-', ' chatgpt', 'language model for',
       'natural language instruction', 'foundation model',
       'foundation models', 'foundation controller',
       'open-vocabulary', 'open vocabulary', 'embodied ai',
       'natural language', 'spoken language', 'language inst',
       'language for robot', 'language understanding',
       'language interaction', 'language correction',
       'foundation model', 'multimodal foundation']
DIFFUSION = ['diffusion policy', 'diffusion-based policy',
             'diffusion policies', 'diffusion model',
             'flow matching', 'denoising diffusion', 'score-based',
             'score based diffusion', 'consistency policy',
             'consistency distillation', 'visuomotor policy',
             'multimodal diffusion transformer']
SELF_SUP = ['self-supervised', 'self supervised', 'self-superv']
ACTIVE_LEARN = ['active learning', 'active reward learning']
WORLD_MODEL = ['world model', 'world models', 'denoising world',
               'unified world model']
DATASET = ['dataset', 'datasets', 'benchmark', 'benchmarking',
           ' simulator ', 'simulation framework', 'simulation platform',
           'data-set', 'data collection', 'simulation engine',
           'data set', 'corpus', 'data papers']

# --- Control
MPC = ['model predictive control', 'model-predictive', ' mpc ',
       '-mpc', 'mpc-', 'mpc ', 'mpc-based', 'predictive control',
       'mpc framework', 'nmpc', 'mppi', 'mpc-bas']
LQR = [' lqr ', '-lqr', 'lqr-', ' iLQR', 'lqr ', 'linear quadratic',
       'h-infinity', 'h infinity', 'h_infty', 'lqg-mp']
ADAPT_C = ['adaptive control', 'adaptive controller', 'adaptive tracking']
ROBUST_C = ['robust control']
SLIDE = ['sliding mode', 'sliding-mode', ' smc ', 'sliding mode control']
NONLIN_C = ['nonlinear control', 'feedback linearization', 'backstepping',
            'lyapunov-based control']
IMPED = ['impedance control', 'admittance control', 'compliance control',
         'compliant control', 'impedance/admittance', 'impedance regulation',
         'impedance-control', 'impedance-based', 'impedance learn']
PASSIVITY = ['passivity-based', 'passivity based', 'port-hamiltonian',
             'energy shaping', 'energy-shaping', 'port hamiltonian',
             'passivity controller']
FORCE_C = ['force control', 'force-control', 'hybrid position/force',
           'hybrid position-force', 'force-motion control',
           'hybrid force', 'force/position', 'force tracking']
CBF = ['control barrier function', ' cbf ', 'cbf-', '-cbf',
       'control barrier', 'barriernet', 'barrier function',
       'safety barrier']
REACH = ['reachability analysis', 'reachable set', 'hamilton-jacobi',
         'hamilton jacobi', 'reachset', 'funnel libraries',
         'reachability-based']
ILC = ['iterative learning control', 'iterative learning-control',
       ' ilc ', 'ilc-']
VS = ['visual servoing', 'visual-servoing', 'image-based control',
      'image based servoing', ' ibvs', ' pbvs', 'aural servo',
      'photometric visual servoing', 'visual servo control',
      'tactile servo', 'tactile-servoing']
WBC = ['whole-body control', 'whole body control', 'whole-body controller',
       ' wbc ', 'whole body controller', 'whole-body locomotion',
       'whole-body manipulation', 'whole body locomotion']
KOOPMAN = ['koopman']
DIFFPHY = ['differentiable physics', 'differentiable simulat',
           'differentiable particle filter', 'differentiable contact',
           'differentiable simulation engine']
CPG = [' cpg ', 'cpg-', '-cpg', 'central pattern generator',
       'central pattern generators']
HZD = [' hzd ', 'hzd ', 'hzd-', 'hybrid zero dynamics']
CONTACT_IMP_MPC = ['contact-implicit mpc', 'contact-implicit model',
                   'contact-implicit', 'contact implicit',
                   'contact-aware mpc']

# --- Theoretical
KIN_KW = ['kinematics', 'kinematic', 'inverse kinematic', 'forward kinematic',
          'workspace analysis', 'singularity analysis', 'redundancy resolution',
          'redundant manipulator', 'redundant manipulators',
          'redundant kinematic', 'jacobian', 'screw theory',
          'denavit', 'dexterity index', 'manipulability',
          'kinetostatic', 'kinematic design', 'kinemato-static']
DYN_KW = ['dynamics', 'dynamic model', 'system identification',
          'system id', 'parameter identification', 'inertia identification',
          'rigid body dynamics', 'multibody dynamics', 'lagrangian dynamics',
          'newton-euler', 'recursive newton', 'forward dynamics',
          'inverse dynamics', 'articulated body dynamics',
          'rigid-body dynamics']
CONTACT_DYN = ['contact dynamics', 'contact model', 'contact-rich',
               'frictional contact', 'friction model', 'collision response',
               'rigid contact', 'soft contact', 'multi-contact modeling',
               'multibody systems with intermittent contact',
               'lugre', 'hunt-crossley', 'hunt crossley',
               'friction modeling', 'complementarity']
OPT_KW = ['optimization', 'optimisation', 'convex optimization',
          'nonlinear optimization', 'mixed-integer', 'mixed integer',
          ' sdp', ' qp ', 'quadratic programming', 'sequential convex',
          ' admm']
LIE = ['lie group', 'lie algebra', ' so(3)', ' se(3)',
       'manifold optimization', 'riemannian', 'differential geometry',
       'screw motion', ' screws ', 'exponential map',
       'so(3)', 'se(3)']
EQUIV = ['equivariant', 'equivariance', 'invariance ', 'invariant filter']
GAME_TH = ['game theory', 'game-theoretic', 'differential game',
           'stackelberg', 'nash equilibrium', 'multi-agent game',
           'dynamic games', 'dynamic game']
FORMAL = ['formal verification', 'formal method', 'temporal logic',
          ' ltl ', 'ltl-', 'signal temporal logic', ' stl ',
          'model checking', 'synthesis from specification',
          'temporal logic motion', 'sccltl', 'scltl']
STAB = ['stability analysis', 'lyapunov stability', 'lyapunov function']
GP_KW = ['gaussian process', 'gaussian-process', ' gp regression',
         ' gp-based', 'gaussian processes']
SDPR = ['certifiable', 'certifiably correct', 'semidefinite relax',
        'sdp relaxation', 'teaser', 'se-sync', 'sdpr', 'cpl-slam']
DIFFPROG = ['differentiable program', 'symforce', 'prox-qp', 'proxddp',
            'autodifferentiation', 'differentiable', 'gauss-helmert']

# --- Application Domains
AGRI = ['agricultur', 'farming', 'crop', 'orchard', 'vineyard',
        'tomato', 'fruit picking', 'fruit harvesting', 'harvest',
        'weeding', 'plant phenotyping', 'horticulture', 'greenhouse',
        'sugar beet', 'corn stand', 'agrobot', 'cherry-picking',
        'agbot', 'agro', 'berry pick']
CONSTR = ['construction', 'excavator', 'bulldozer', 'concrete',
          'bricklaying', 'building robot', 'construction assembly',
          'autonomous excav']
INSPECT = ['inspection', 'inspect ', 'pipeline inspect', 'bridge inspect',
           'infrastructure inspection', 'cable inspection', 'cccrobot',
           'tank inspection', 'visual inspection', 'autonomous robotic inspection',
           'in-water ship hull', 'hull inspection']
MINING = ['mining robot', 'underground mining', 'mining', 'lhd loader',
          ' lhd ']
SAFETY_INSP = ['inspection']
COMP_BIO = ['protein', 'molecular', 'molecule', 'rna ', 'dna ',
            ' nmr ', 'nmr ', 'proteins', 'protein folding',
            'protein structure', 'protein conformation',
            'amino acid', 'genetic network', 'biological cell',
            'protein loop', 'protein backbone', 'cell injection',
            'cell manipulation', 'biological cells', 'cell migration',
            'cell injection', 'aneurysm', 'cell punctures']
FOOD = ['cooking', 'food handling', 'food robot', 'feeding via',
        'meat factory', 'fruit and vegetable']

# --- Perception sub
OBJ_POSE = ['object pose', '6dof pose', '6-dof pose', '6d pose',
            'pose estimation', 'object 6d', 'object 6dof', ' pnp ',
            'perspective-n-point', 'perspective n point',
            '6-dof pose tracking', '6 dof pose']
SEMSEG = ['semantic segmentation', 'semantic-segmentation',
          'instance segmentation', 'panoptic segmentation',
          'scene parsing', 'lidar panoptic', 'panoptic']
OBJ_DET = ['object detection', 'object recognition', 'object classification',
           '3d object detection', '2d object detection',
           'pedestrian detection', 'vehicle detection', 'detect drone',
           'drone detection']
RECON3D = ['3d reconstruction', '3d-reconstruction', 'mesh reconstruction',
           'surface reconstruction', ' nerf ', 'nerf-', '-nerf',
           'neural radiance', 'gaussian splatting', '3d-gs ',
           '3dgs', 'volumetric reconstruction', 'tsdf', ' sdf ',
           'sdf-', '-sdf', 'neural implicit', 'multi-view stereo',
           'photogrammetry', 'isdf', 'neural sdf']
DEPTH_EST = ['depth estimation', 'depth prediction', 'monocular depth',
             'self-supervised depth']
SCENE_FLOW = ['scene flow', 'optical flow', 'motion estimation']
TRACK_KW = ['object tracking', 'multi-object tracking', ' mot ',
            'visual tracking', 'tracking algorithm', 'kalman tracking',
            'target tracking']
SCENE_GRAPH = ['scene graph', '3d scene graph', '3-d scene graph',
               'scene graphs', 'spatial perception']

# --- Planning sub
NAVIG = ['navigation', 'navigate', 'navigating', 'navigational',
         'navigator']
EXPLORE = ['exploration', 'explor', 'autonomous exploration',
           'frontier-based', 'frontier based', 'next-best-view',
           'next best view', 'active perception', 'active exploration',
           'active mapping', 'next-best-trajectory']
COVERAGE = ['coverage path', 'coverage planning', 'area coverage',
            'lawn-mower', 'boustrophedon', 'coverage control',
            'persistent coverage']
OBSTACLE = ['obstacle avoidance', 'collision avoidance', 'collision-free',
            'collision free']
PLAN_PATH = ['path planning', 'path-planning', 'trajectory planning',
             'trajectory generation', 'motion planning', 'motion-planning',
             'kinodynamic planning', 'kinodynamic motion',
             'replanning', 'planner', 'planning']
RRT_LIKE = [' rrt ', '-rrt', 'rrt ', 'rrt*', 'sampling-based',
            'sampling based', ' prm ', 'prm-', 'probabilistic roadmap',
            'asymptotically optimal', 'rrt-based', 'random-finite',
            'rapidly exploring random', 'fast marching tree',
            'fmt*', 'bit*', 'bit star']
SEARCH_PLAN = [' a*', ' a-star', 'a* search', ' jps ', 'jump point search',
               ' d* ', 'lattice planner', 'state lattice',
               'a-star']
TRAJOPT = ['trajectory optimization', 'trajectory-optimization', 'chomp',
           'trajopt', 'gpmp', ' kkt', 'optimal trajectory',
           'time-optimal trajectory', 'minimum-time trajectory',
           'minimum time trajectory', 'minimum jerk', 'minimum-jerk',
           'minimum snap', 'sequential convex', 'time-optimal',
           'spline trajectory', 'trajectory parameteriz',
           'time optimal trajectory']
TAMP = ['task and motion planning', ' tamp ', 'tamp ', 'tamp-',
        '-tamp ', 'task-and-motion', 'integrated task and motion',
        'task and motion']
SYMB_PLAN = ['symbolic planning', 'pddl', 'classical planning',
             'symbolic ai', 'task planner', 'logic planner',
             'symbolic-geometric', 'symbolic geometric']
BELIEF = ['belief space', 'belief-space', 'partially observable',
          ' pomdp', 'pomdp ', 'belief planning', 'pomdps']
FOOTSTEP = ['footstep planning', 'foothold', 'foothold planning',
            'gait planning', 'gait optimization', 'footstep']
MANIP_PLAN = ['manipulation planning', 'grasp planning', 'pick planning',
              'rearrangement planning']
MOT_PRIM = ['motion primitive', 'movement primitive', ' dmp ', 'dmps',
            'dynamic movement primitive', 'movement primitives',
            'motion primitives']
SOCIAL_NAV = ['social navigation', 'crowd navigation', 'crowd-aware',
              'pedestrian', 'socially-aware navigation',
              'socially aware navigation']
VLN = ['vision-language navigation', 'vision and language navigation',
       'vision-and-language navigation', 'vln', 'language navigation',
       'embodied navigation', 'embodied scene', 'instruction following nav']
OFFROAD_NAV = ['off-road', 'offroad', 'off road', 'unstructured terrain',
               'rough terrain', 'rugged', 'wild visual',
               'rough off-road']

# --- Software / Architecture
ARCH = ['robot architecture', 'control architecture',
        'controlshell', 'orccad', 'openhrp', 'mrroc++',
        'ros2', 'ros ', 'middleware', 'robot framework',
        'kubernetes', 'real-time architecture', 'reactive architecture',
        'subsumption']
BT = ['behavior tree', 'behavior trees', 'behaviour tree',
      'behavior-tree', 'behaviour-tree']
PROGRAMM = ['robot programming', 'programming framework',
            'programming toolset', 'programming toolkit',
            'robot programming framework']
CODEGEN = ['symbolic computation', 'code generation', 'symforce',
           'code-generation', 'codegen']
RT_SYS = ['real-time scheduling', 'real-time system',
          'real-time control', 'realtime', 'semantic-aware scheduling',
          'cyber-physical', 'cyberphysical', 'cyber physical']

# ============================================================
# Classification function
# ============================================================
def classify(title_orig):
    """Return (Phylum, Class, Order)."""
    t = t_low(title_orig)

    # ===========================================================
    # 0. METADATA / EDITORIAL (catch first)
    # ===========================================================
    if any(p in t for p in ['editorial', 'from the editor', 'erratum',
                            'corrections to', 'comments on', ' corrections ',
                            'book review', 'farewell', 'reviewers',
                            'guest editor', 'introduction to the special',
                            'so long, t-ra', 'editor-in-chief',
                            'message from the', 'announce introduction',
                            'preface to the', 'incoming editor',
                            "communication on optimal",
                            'communication to:', "author's reply",
                            'special issue', 'special section',
                            'selected papers', ' iser ', ' wafr ',
                            'robotics: science and systems',
                            ' rss20', 'list of reviewers']):
        return ('Other / Editorial', 'Editorial / Meta', 'Editorial Material')

    # ===========================================================
    # 1. FOUNDATION MODELS / LATEST AI METHODS (highest priority — new field)
    # ===========================================================
    if has_any(t, VLA):
        return ('Learning for Robotics', 'Foundation Models',
                'Vision-Language-Action (VLA)')
    if has_any(t, ['saycan', 'rt-1 ', 'rt-1:', ' rt-2', 'opvla', 'openvla',
                   ' π₀', 'pi-zero', 'pi 0', ' octo ', 'octo:', 'navila',
                   'spatialvla', 'naivd', 'navid', 'uni-navid',
                   'clip-rt', 'fast: efficient', 'fast efficient action token']):
        return ('Learning for Robotics', 'Foundation Models',
                'Vision-Language-Action (VLA)')
    if has_any(t, DIFFUSION):
        return ('Learning for Robotics', 'Foundation Models',
                'Diffusion Policies / Flow Matching')
    if has_any(t, WORLD_MODEL):
        return ('Learning for Robotics', 'Foundation Models',
                'World Models')
    if has_any(t, LLM):
        return ('Learning for Robotics', 'Foundation Models',
                'LLM / Foundation-model Reasoning')

    # ===========================================================
    # 2. SLAM & LOCALIZATION (very high priority — strong identifiers)
    # ===========================================================
    # 2a. Place Recognition / Loop Closure
    if has_any(t, PLACE_RECOG):
        if has_any(t, LIDAR):
            return ('SLAM & Localization', 'Place Recognition',
                    'LiDAR-based Place Recognition')
        if has_any(t, RADAR):
            return ('SLAM & Localization', 'Place Recognition',
                    'Radar-based Place Recognition')
        if has_any(t, ['cross-modal', 'overhead imag', 'i3dloc', 'cmrnext',
                       'image-to-range']):
            return ('SLAM & Localization', 'Place Recognition',
                    'Cross-modal Place Recognition')
        if has_any(t, VISUAL) or 'vpr' in t:
            return ('SLAM & Localization', 'Place Recognition',
                    'Visual Place Recognition (VPR)')
        return ('SLAM & Localization', 'Place Recognition',
                'General Place Recognition')

    # 2b. Calibration
    if has_any(t, CALIB) and not has_any(t, ['kinematic calibration of']):
        if has_any(t, ['hand-eye', 'hand eye', 'axb=ycz', 'ax=yb', 'ax=xb']):
            return ('SLAM & Localization', 'Calibration',
                    'Hand-Eye Calibration')
        if has_any(t, ['camera-imu', 'camera imu', 'visual-inertial calibration',
                       'imu-camera', 'cam-imu']):
            return ('SLAM & Localization', 'Calibration',
                    'Visual-Inertial Calibration')
        if has_any(t, LIDAR + ['lidar-camera', 'lidar camera',
                               'lidar-imu', 'lidar imu']):
            return ('SLAM & Localization', 'Calibration',
                    'LiDAR / Multi-modal Calibration')
        if has_any(t, ['kinematic calibration', 'robot calibration']):
            return ('SLAM & Localization', 'Calibration',
                    'Kinematic Calibration')
        if 'targetless' in t or 'self-calibration' in t or 'online cal' in t:
            return ('SLAM & Localization', 'Calibration',
                    'Targetless / Online Calibration')
        return ('SLAM & Localization', 'Calibration',
                'Sensor Calibration')

    # 2c. SLAM family (must check more specific first)
    is_neural_slam = has_any(t, NEURAL_SLAM)
    if is_neural_slam:
        return ('SLAM & Localization', 'SLAM',
                'Neural Implicit / Gaussian Splatting SLAM')

    if has_any(t, SLAM_KW) or (has_any(t, ['mapping']) and has_any(t, ['simultan'])):
        is_lidar = has_any(t, LIDAR) or 'lio' in t
        is_visual = has_any(t, VISUAL) or 'vio' in t or 'vins' in t or 'orb-slam' in t
        is_inert = has_any(t, IMU) or 'inertial' in t or 'vio' in t \
            or 'lio' in t or 'vins' in t or 'okvis' in t
        is_radar = has_any(t, RADAR)
        is_acoust = has_any(t, SONAR) or has_any(t, UNDER)
        is_event = has_any(t, EVENT_CAM)
        is_semantic = 'semantic slam' in t or 'semantic mapping' in t
        is_dense = 'dense slam' in t or 'dense mapping' in t \
            or 'volumetric mapping' in t or 'occupancy mapping' in t \
            or 'occupancy-slam' in t or 'occupancy slam' in t
        is_object = ('object slam' in t or 'object-level slam' in t
                     or 'cubeslam' in t or 'object slam framework' in t)
        is_dyn = ('dynamic environment' in t or 'dynamic-object' in t
                  or 'dynamic scenes' in t or 'defslam' in t
                  or 'nr-slam' in t or 'dynamic env' in t)
        is_multi = has_any(t, MULTI_R) or 'distributed' in t \
            or 'collaborative' in t or 'cooperative slam' in t \
            or 'cooperative mapping' in t

        if is_object:
            return ('SLAM & Localization', 'SLAM', 'Object SLAM')
        if is_semantic:
            return ('SLAM & Localization', 'SLAM', 'Semantic SLAM')
        if is_dyn:
            return ('SLAM & Localization', 'SLAM', 'Dynamic-environment SLAM')
        if is_dense:
            return ('SLAM & Localization', 'SLAM', 'Dense Mapping / Reconstruction')
        if is_multi:
            return ('Multi-Robot Systems', 'Multi-Robot SLAM',
                    'Distributed / Cooperative SLAM')
        if is_radar:
            return ('SLAM & Localization', 'SLAM', 'Radar SLAM/Odometry')
        if is_acoust:
            return ('SLAM & Localization', 'SLAM', 'Acoustic / Underwater SLAM')
        if is_event:
            return ('SLAM & Localization', 'SLAM', 'Event-based VIO/SLAM')
        if is_lidar and is_visual and is_inert:
            return ('SLAM & Localization', 'SLAM',
                    'Multi-modal SLAM (V+L+I+GNSS)')
        if is_lidar and is_inert:
            return ('SLAM & Localization', 'SLAM',
                    'LiDAR-Inertial Odometry/SLAM (LIO)')
        if is_visual and is_inert:
            return ('SLAM & Localization', 'SLAM',
                    'Visual-Inertial Odometry/SLAM (VIO)')
        if is_lidar and is_visual:
            return ('SLAM & Localization', 'SLAM', 'Multi-modal SLAM')
        if is_lidar:
            return ('SLAM & Localization', 'SLAM', 'LiDAR SLAM/Odometry')
        if is_visual:
            return ('SLAM & Localization', 'SLAM', 'Visual SLAM/Odometry')
        if is_inert:
            return ('SLAM & Localization', 'SLAM', 'Inertial Odometry')
        return ('SLAM & Localization', 'SLAM', 'General SLAM')

    # 2d. State estimation primitives
    if has_any(t, ['imu preintegrat', 'lie group imu', 'preintegration on manifold',
                   'imu intrinsic', 'preintegration']):
        return ('SLAM & Localization', 'State Estimation',
                'Lie Group IMU Preintegration')
    if has_any(t, KALMAN):
        return ('SLAM & Localization', 'State Estimation', 'Bayesian Filtering')
    if has_any(t, POSEGRAPH):
        return ('SLAM & Localization', 'State Estimation',
                'Pose Graph / Bundle Adjustment')

    # 2e. Localization (no SLAM)
    if 'localization' in t or 'localisation' in t or 'positioning' in t:
        if has_any(t, LIDAR):
            return ('SLAM & Localization', 'Localization',
                    'LiDAR-based Localization')
        if has_any(t, UWB) or 'rfid' in t or 'wifi' in t:
            return ('SLAM & Localization', 'Localization',
                    'UWB / WiFi / Radio Localization')
        if has_any(t, ['ranging', 'range-only', 'range only', 'acoustic beacon']):
            return ('SLAM & Localization', 'Localization',
                    'Range-only / Acoustic Localization')
        if has_any(t, VISUAL):
            return ('SLAM & Localization', 'Localization', 'Visual Localization')
        if has_any(t, ['indoor', 'gps-denied', 'gps denied']):
            return ('SLAM & Localization', 'Localization',
                    'Indoor / GPS-denied Localization')
        if has_any(t, MULTI_R) or 'cooperative loc' in t:
            return ('Multi-Robot Systems', 'Coordination',
                    'Cooperative Localization')
        return ('SLAM & Localization', 'Localization', 'General Localization')

    # ===========================================================
    # 3. PERCEPTION & SENSING
    # ===========================================================
    # 3-Scene Graph / Spatial Perception (modern)
    if has_any(t, SCENE_GRAPH) or 'kimera' in t or 'hydra' in t \
            or 'foundations of spatial perception' in t:
        return ('Perception & Sensing', '3D Scene Graph / Spatial Perception',
                'Hierarchical Spatial Perception')

    # Active Perception
    if has_any(t, ['active perception', 'active vision', 'active sensing',
                   'active learning of dynamics', 'active object detection',
                   'next best view', 'next-best-view',
                   'active simultaneous localization',
                   'active exploration', 'active simu loc',
                   'active scene', 'active visual', 'active mapping',
                   'active inference for', 'active 3d', 'active velocity']):
        return ('Perception & Sensing', 'Active Perception',
                'Active Vision / Active Sensing')

    if has_any(t, RECON3D):
        return ('Perception & Sensing', 'Visual Perception',
                '3D Reconstruction / Neural Field')
    if has_any(t, OBJ_POSE):
        return ('Perception & Sensing', 'Visual Perception',
                'Pose Estimation')
    if has_any(t, SEMSEG):
        if has_any(t, LIDAR):
            return ('Perception & Sensing', 'LiDAR Perception',
                    'Semantic Segmentation')
        return ('Perception & Sensing', 'Visual Perception',
                'Semantic / Instance Segmentation')
    if has_any(t, OBJ_DET):
        if has_any(t, LIDAR):
            return ('Perception & Sensing', 'LiDAR Perception',
                    'Object Detection')
        return ('Perception & Sensing', 'Visual Perception',
                'Object Detection / Recognition')
    if has_any(t, DEPTH_EST):
        return ('Perception & Sensing', 'Visual Perception', 'Depth Estimation')
    if has_any(t, SCENE_FLOW):
        return ('Perception & Sensing', 'Visual Perception',
                'Optical / Scene Flow')
    if has_any(t, TRACK_KW):
        return ('Perception & Sensing', 'Tracking', 'Object/Target Tracking')

    if has_any(t, EVENT_CAM):
        return ('Perception & Sensing', 'Event-based Vision',
                'Event Camera Processing')
    if has_any(t, TACTILE) or 'tactile' in t:
        if has_any(t, ['gelsight', 'vision-based tactile', 'visuotactile',
                       'visuo-tactile', 'visuo tactile']):
            return ('Perception & Sensing', 'Tactile Sensing',
                    'GelSight / Vision-based Tactile')
        if 'event' in t or 'evetac' in t:
            return ('Perception & Sensing', 'Tactile Sensing',
                    'Event-based Optical Tactile')
        if 'tactile servoing' in t or 'tactile-servoing' in t \
                or 'tactile-reactive' in t:
            return ('Perception & Sensing', 'Tactile Sensing',
                    'Tactile Servoing')
        if 'eit' in t or 'electrical impedance tomography' in t:
            return ('Perception & Sensing', 'Tactile Sensing',
                    'EIT-based Tactile Skin')
        return ('Perception & Sensing', 'Tactile Sensing',
                'Tactile Sensors / Algorithms')
    if has_any(t, RADAR):
        if 'odom' in t:
            return ('Perception & Sensing', 'Radar Perception',
                    'Radar Odometry')
        return ('Perception & Sensing', 'Radar Perception', 'Radar Processing')
    if has_any(t, SONAR):
        return ('Perception & Sensing', 'Acoustic Perception',
                'Sonar / Acoustic Imaging')
    if has_any(t, LIDAR) and not has_any(t, ['lidar slam', 'lidar odom']):
        return ('Perception & Sensing', 'LiDAR Perception',
                'Point Cloud Processing')

    if 'multi-modal perception' in t or 'multimodal perception' in t \
            or 'sensor fusion' in t or 'multi-sensor fusion' in t \
            or 'multisensor' in t:
        return ('Perception & Sensing', 'Multi-modal Perception',
                'Sensor Fusion')

    # ===========================================================
    # 4. APPLICATION DOMAINS (specific applications take priority over generic methods)
    # ===========================================================

    # 4a. Medical & Surgical
    if has_any(t, SURG):
        if 'capsule' in t and ('endoscope' in t or 'colonoscope' in t):
            return ('Application Domains', 'Medical & Surgical Robotics',
                    'Capsule Endoscopy / Magnetic Capsule')
        if 'beating heart' in t or 'heart motion' in t \
                or 'cardiac motion' in t:
            return ('Application Domains', 'Medical & Surgical Robotics',
                    'Beating Heart / Motion Compensation')
        if 'needle' in t and ('steer' in t or 'insertion' in t):
            return ('Application Domains', 'Medical & Surgical Robotics',
                    'Needle Steering / Insertion')
        if has_any(t, ['neurosurg', 'microsurg', 'intraocular',
                       'mri-guided neurosurg']):
            return ('Application Domains', 'Medical & Surgical Robotics',
                    'Microsurgery / Neurosurgery')
        if 'mri-compat' in t or 'mri-driven' in t or 'mri-powered' in t \
                or 'mri-guided' in t:
            return ('Application Domains', 'Medical & Surgical Robotics',
                    'MRI-compatible / Image-guided Surgery')
        if 'endoscop' in t or 'catheter' in t or 'colonoscopy' in t \
                or 'laparoscopic' in t or 'transendoscopic' in t \
                or 'transurethral' in t:
            return ('Application Domains', 'Medical & Surgical Robotics',
                    'Endoscopy / Catheter / Laparoscopy')
        return ('Application Domains', 'Medical & Surgical Robotics',
                'Surgical Robot')
    if 'medical' in t and ('robot' in t or 'imag' in t):
        return ('Application Domains', 'Medical & Surgical Robotics',
                'Medical Robot')

    # 4b. Computational Biology
    if has_any(t, COMP_BIO):
        return ('Application Domains', 'Computational Biology Robotics',
                'Bio-molecular Modeling / Protein')

    # 4c. Field robotics
    if has_any(t, AGRI):
        return ('Application Domains', 'Field Robotics', 'Agricultural Robotics')
    if has_any(t, INSPECT):
        return ('Application Domains', 'Field Robotics', 'Inspection Robotics')
    if has_any(t, CONSTR):
        return ('Application Domains', 'Field Robotics',
                'Construction / Excavation Robotics')
    if has_any(t, MINING):
        return ('Application Domains', 'Field Robotics',
                'Mining / LHD')

    # 4d. Space (after Field)
    if has_any(t, SPACE) or 'mars rover' in t or 'lunar' in t \
            or "chang'e" in t or 'planetary' in t:
        if 'rover' in t:
            return ('Application Domains', 'Space Robotics',
                    'Planetary Rover')
        return ('Application Domains', 'Space Robotics',
                'Space / Orbital Robotics')

    # 4e. Autonomous driving
    if has_any(t, CARLIKE) or 'autonomous driving' in t \
            or 'self-driving' in t:
        return ('Application Domains', 'Autonomous Driving',
                'Self-driving Vehicle / Decision Making')
    if 'lane' in t and ('detect' in t or 'estim' in t or 'plan' in t) \
            or 'road detection' in t or 'autonomous parking' in t \
            or 'highway' in t and 'driving' in t:
        return ('Application Domains', 'Autonomous Driving',
                'Driving Perception / Lane / Road')

    # 4f. Search and rescue
    if has_any(t, SAR):
        return ('Application Domains', 'Search & Rescue', 'SAR Robotics')

    # 4g. Service / domestic
    if has_any(t, DOMESTIC):
        return ('Application Domains', 'Service Robotics',
                'Domestic / Service Robot')

    # 4h. Logistics
    if has_any(t, LOGI):
        return ('Application Domains', 'Logistics', 'Warehouse / Delivery')

    # 4i. Food
    if has_any(t, FOOD):
        return ('Application Domains', 'Service Robotics',
                'Food Service / Cooking')

    # ===========================================================
    # 5. MANIPULATION (after foundation models, since FM is more specific)
    # ===========================================================
    # Specific manipulation types first
    if has_any(t, ASSEMBLY):
        return ('Manipulation', 'Contact-rich Manipulation',
                'Assembly / Insertion / Peg-in-hole')
    if has_any(t, KNOT_CABLE):
        return ('Manipulation', 'Contact-rich Manipulation',
                'Knot / Cable / Wire Manipulation')
    if has_any(t, DEFORM):
        if 'cloth' in t or 'fabric' in t or 'garment' in t \
                or 'dress' in t:
            return ('Manipulation', 'Contact-rich Manipulation',
                    'Cloth / Garment Manipulation')
        if 'liquid' in t or 'granular' in t or 'plasticine' in t \
                or 'elasto' in t or 'paste' in t:
            return ('Manipulation', 'Contact-rich Manipulation',
                    'Liquid / Granular Manipulation')
        return ('Manipulation', 'Contact-rich Manipulation',
                'Deformable Object Manipulation')
    if has_any(t, ARTIC_OBJ):
        return ('Manipulation', 'Contact-rich Manipulation',
                'Articulated Object Manipulation')
    if has_any(t, NONPRE):
        if 'tossing' in t or 'throwing' in t:
            return ('Manipulation', 'Non-prehensile', 'Tossing / Throwing')
        return ('Manipulation', 'Non-prehensile', 'Pushing / Sliding')
    if has_any(t, TOOL_USE):
        return ('Manipulation', 'Tool Use', 'Tool Manipulation')
    if has_any(t, BIMAN):
        return ('Manipulation', 'Dexterous Manipulation',
                'Bimanual Manipulation')
    if has_any(t, DEX_MANIP):
        if 'human video' in t or 'in the wild' in t or 'in-the-wild' in t \
                or 'youtube' in t or 'human hand' in t:
            return ('Manipulation', 'Dexterous Manipulation',
                    'Learning Dexterity from Human Videos')
        if 'foundation' in t or 'dexteritygen' in t:
            return ('Manipulation', 'Dexterous Manipulation',
                    'Foundation Controllers for Dexterity')
        return ('Manipulation', 'Dexterous Manipulation',
                'In-hand / Multi-finger')
    if has_any(t, SUCTION):
        return ('Manipulation', 'Grasping', 'Suction Grasping')
    if has_any(t, MOBILE_MANIP):
        if 'loco-manipulation' in t or 'loco manipulation' in t:
            return ('Manipulation', 'Mobile Manipulation',
                    'Loco-Manipulation')
        return ('Manipulation', 'Mobile Manipulation',
                'Mobile Manipulator')
    if has_any(t, AERIAL_MANIP):
        return ('Manipulation', 'Aerial Manipulation', 'Aerial Grasping')
    if 'underwater manipulation' in t:
        return ('Manipulation', 'Underwater Manipulation',
                'Underwater Manipulation')
    if has_any(t, DIST_MANIP):
        return ('Manipulation', 'Distributed Manipulation',
                'Programmable Force Fields / Parts Feeding')

    if has_any(t, GRASP):
        if 'caging' in t:
            return ('Manipulation', 'Grasping', 'Caging-based Grasping')
        if has_any(t, ['learn', 'imitation', 'reinforcement', 'neural',
                       'deep', 'data-driven']):
            return ('Manipulation', 'Grasping', 'Learning-based Grasping')
        return ('Manipulation', 'Grasping', 'Grasp Planning / Synthesis')

    # ===========================================================
    # 6. LOCOMOTION
    # ===========================================================
    # Aerial-specific
    if has_any(t, UAV):
        if has_any(t, AERIAL_SWARM) or ('swarm' in t and 'aerial' in t):
            return ('Multi-Robot Systems', 'Aerial Swarms / UAV Swarms',
                    'Decentralized Aerial Swarm')
        if 'flapping' in t or 'flapping-wing' in t:
            return ('Locomotion', 'Aerial Locomotion', 'Flapping-wing Robot')
        if has_any(t, ['fixed-wing', 'fixed wing']):
            return ('Locomotion', 'Aerial Locomotion', 'Fixed-wing UAV')
        if has_any(t, ['tail-sitter', 'tailsitter', 'tail sitter', ' vtol']):
            return ('Locomotion', 'Aerial Locomotion', 'Tail-sitter / VTOL')
        if 'insect-scale' in t or 'pico' in t or 'robofly' in t \
                or 'insect-sized' in t or 'insect inspired' in t \
                and 'aerial' in t:
            return ('Locomotion', 'Aerial Locomotion',
                    'Insect-scale / Pico Aerial')
        if 'aerial-aquatic' in t or 'aerial aquatic' in t \
                or 'hytaq' in t or 'aerial-terrestrial' in t \
                or 'aerial/aquatic' in t:
            return ('Locomotion', 'Aerial Locomotion',
                    'Hybrid Aerial-Aquatic / Aerial-Terrestrial')
        if 'racing' in t or 'agile flight' in t or 'aggressive maneuver' in t:
            return ('Locomotion', 'Aerial Locomotion',
                    'Aggressive / Racing Flight')
        if 'drone' in t and 'cinematography' in t:
            return ('Locomotion', 'Aerial Locomotion',
                    'Aerial Cinematography')
        if 'helicopter' in t:
            return ('Locomotion', 'Aerial Locomotion',
                    'Helicopter / Autonomous Helicopter')
        return ('Locomotion', 'Aerial Locomotion',
                'Multirotor / Quadrotor')

    # Underwater
    if has_any(t, UNDER):
        if 'fish' in t or 'biomimetic' in t or 'eel' in t or 'snake' in t:
            return ('Locomotion', 'Bio-inspired Locomotion',
                    'Swimming / Fish Robot')
        return ('Locomotion', 'Underwater Locomotion', 'AUV / UUV')
    if has_any(t, SURFACE):
        return ('Locomotion', 'Surface / Marine Locomotion',
                'USV / Surface Vehicle')

    # Legged
    if has_any(t, BIPED):
        return ('Locomotion', 'Legged Locomotion', 'Bipedal / Humanoid')
    if has_any(t, QUAD):
        return ('Locomotion', 'Legged Locomotion', 'Quadruped')
    if has_any(t, HEXAPOD):
        return ('Locomotion', 'Legged Locomotion', 'Hexapod / Multi-legged')
    if has_any(t, LEGGED_GEN):
        if 'wheel' in t:
            return ('Locomotion', 'Legged Locomotion',
                    'Hybrid Wheel-Leg')
        return ('Locomotion', 'Legged Locomotion', 'Legged (general)')

    # Bio-inspired
    if has_any(t, SNAKE_LOC):
        return ('Locomotion', 'Bio-inspired Locomotion', 'Snake / Serpentine')
    if has_any(t, CLIMB_LOC):
        return ('Locomotion', 'Bio-inspired Locomotion', 'Climbing Robot')
    if has_any(t, JUMP_LOC):
        return ('Locomotion', 'Bio-inspired Locomotion',
                'Jumping / Hopping')
    if has_any(t, FISH_LOC):
        return ('Locomotion', 'Bio-inspired Locomotion',
                'Swimming / Fish Robot')
    if has_any(t, CRAWL_LOC):
        return ('Locomotion', 'Bio-inspired Locomotion',
                'Crawling / Inchworm')
    if has_any(t, SAND_LOC):
        return ('Locomotion', 'Bio-inspired Locomotion',
                'Sand-swimming / Granular Locomotion')

    # Wheeled
    if has_any(t, WHEELED):
        return ('Locomotion', 'Wheeled Locomotion', 'Mobile Wheeled Robot')

    # ===========================================================
    # 7. ROBOT DESIGN & HARDWARE
    # ===========================================================
    if has_any(t, GROWING_ROBOT):
        return ('Robot Design & Hardware', 'Soft Robotics',
                'Vine / Growing Robot')
    if has_any(t, CONTINUUM):
        if 'concentric tube' in t or 'concentric-tube' in t:
            return ('Robot Design & Hardware', 'Continuum Robot',
                    'Concentric Tube Robot')
        if 'magnetic' in t or 'magnet' in t:
            return ('Robot Design & Hardware', 'Continuum Robot',
                    'Magnetic Continuum Robot')
        if 'parallel continuum' in t or 'tendon-driven parallel' in t:
            return ('Robot Design & Hardware', 'Continuum Robot',
                    'Parallel Continuum Robot')
        return ('Robot Design & Hardware', 'Continuum Robot',
                'Continuum Manipulator')
    if has_any(t, MICRO):
        if 'magnetic' in t or 'magnet' in t:
            if 'swarm' in t:
                return ('Robot Design & Hardware', 'Microrobotics',
                        'Magnetic Microrobot Swarms')
            if 'mri' in t:
                return ('Robot Design & Hardware', 'Microrobotics',
                        'MRI-driven Microrobot')
            return ('Robot Design & Hardware', 'Microrobotics',
                    'Magnetic Microrobot')
        if 'catalytic' in t or 'self-actuating' in t \
                or 'electro-osmotic' in t:
            return ('Robot Design & Hardware', 'Microrobotics',
                    'Catalytic / Chemically-driven Microrobot')
        return ('Robot Design & Hardware', 'Microrobotics',
                'Microrobot / Microswimmer')
    if has_any(t, BIOHYBRID):
        return ('Robot Design & Hardware', 'Bio-hybrid Robot',
                'Bio-hybrid')
    if has_any(t, MODULAR):
        return ('Robot Design & Hardware', 'Modular / Reconfigurable Robot',
                'Modular / Reconfigurable')
    if has_any(t, TENSEGRITY):
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Tensegrity Robot')
    if has_any(t, PARALLEL):
        if 'cable' in t:
            return ('Robot Design & Hardware', 'Mechanism Design',
                    'Cable-driven Parallel Robot')
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Parallel Mechanism')
    if has_any(t, SOFT_ROBOT):
        if has_any(t, ['hasel', 'dielectric elastomer']):
            return ('Robot Design & Hardware', 'Soft Robotics',
                    'HASEL / Dielectric Elastomer')
        if 'twisted coiled' in t or 'twisted-coiled' in t \
                or 'twisted string' in t or 'mckibben' in t \
                or 'pneumatic muscle' in t or 'tcp ' in t \
                or 'artificial muscle' in t:
            return ('Robot Design & Hardware', 'Soft Robotics',
                    'Artificial Muscle / Pneumatic Muscle')
        if 'origami' in t:
            return ('Robot Design & Hardware', 'Soft Robotics',
                    'Origami Mechanism')
        if 'electrostatic' in t or 'electroadhesion' in t:
            return ('Robot Design & Hardware', 'Soft Robotics',
                    'Electrostatic Actuation')
        if 'actuator' in t:
            return ('Robot Design & Hardware', 'Soft Robotics',
                    'Soft Actuator')
        if 'gripper' in t or 'hand' in t:
            return ('Robot Design & Hardware', 'Soft Robotics',
                    'Soft Gripper / Hand')
        if 'sensor' in t or 'skin' in t:
            return ('Robot Design & Hardware', 'Soft Robotics',
                    'Soft Sensor / Skin')
        if 'variable stiffness' in t or 'variable-stiffness' in t \
                or 'jamming' in t:
            return ('Robot Design & Hardware', 'Soft Robotics',
                    'Variable Stiffness')
        return ('Robot Design & Hardware', 'Soft Robotics',
                'Soft Robot Design')

    if has_any(t, ['variable stiffness actuator', ' vsa ', 'vsa-',
                   'series elastic', ' sea ', 'sea-', '-sea',
                   'elastic actuator']):
        if 'series elastic' in t or 'sea ' in t:
            return ('Robot Design & Hardware', 'Actuators',
                    'Series Elastic Actuator (SEA)')
        return ('Robot Design & Hardware', 'Actuators',
                'Variable Stiffness Actuator (VSA)')
    if has_any(t, ['piezoelectric actuator', 'piezo actuator',
                   'piezoelectric robot', 'piezoactuated']):
        return ('Robot Design & Hardware', 'Actuators',
                'Piezoelectric Actuator')
    if has_any(t, ['hydraulic actuator', 'hydraulic robot']):
        return ('Robot Design & Hardware', 'Actuators',
                'Hydraulic Actuator')
    if has_any(t, ['pneumatic actuator', 'pneumatic robot']):
        return ('Robot Design & Hardware', 'Actuators',
                'Pneumatic Actuator')
    if has_any(t, ['actuator design', 'actuation design',
                   'magnetorheological']):
        if 'magnetorheological' in t:
            return ('Robot Design & Hardware', 'Actuators',
                    'Magnetorheological Actuator')
        return ('Robot Design & Hardware', 'Actuators', 'Actuator Design')
    if 'gripper design' in t or ('gripper' in t and 'design' in t):
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Gripper Design')
    if '3d-print' in t or '3d print' in t or 'additive manufactur' in t:
        return ('Robot Design & Hardware', 'Manufacturing',
                '3D Printing')

    # ===========================================================
    # 8. HUMAN-ROBOT INTERACTION (HRI)
    # ===========================================================
    if has_any(t, BCI):
        return ('Human-Robot Interaction', 'Assistive Robotics',
                'Brain-Machine Interface (BMI/BCI)')
    if has_any(t, EXOSKEL):
        if has_any(t, SOFT_EXO):
            return ('Human-Robot Interaction', 'Assistive Robotics',
                    'Soft Exosuit / Wearable Soft')
        if has_any(t, HAND_EXO):
            return ('Human-Robot Interaction', 'Assistive Robotics',
                    'Hand Exoskeleton')
        return ('Human-Robot Interaction', 'Assistive Robotics',
                'Exoskeleton / Wearable')
    if has_any(t, PROST):
        return ('Human-Robot Interaction', 'Assistive Robotics',
                'Prosthetics')
    if has_any(t, REHAB):
        return ('Human-Robot Interaction', 'Assistive Robotics',
                'Rehabilitation')
    if has_any(t, EMG) and not has_any(t, ['emg-controlled wheelchair']):
        return ('Human-Robot Interaction', 'Assistive Robotics',
                'EMG / Myoelectric Control')

    if has_any(t, HAPTICS):
        if 'rendering' in t:
            return ('Human-Robot Interaction', 'Haptic Devices & Rendering',
                    'Haptic Rendering')
        if 'wearable' in t or 'vibrotactile' in t or 'electrotactile' in t:
            return ('Human-Robot Interaction', 'Haptic Devices & Rendering',
                    'Wearable Haptic Feedback')
        return ('Human-Robot Interaction', 'Haptic Devices & Rendering',
                'Haptic Display / Force Feedback')

    if has_any(t, TELEOP):
        if 'in the wild' in t or 'in-the-wild' in t \
                or 'universal manipulation interface' in t \
                or 'anyteleop' in t or 'open-teach' in t \
                or 'tilde' in t and 'teleoperation' in t:
            return ('Human-Robot Interaction', 'Teleoperation',
                    'In-the-Wild Teleoperation')
        if 'bilateral' in t or 'time delay' in t or 'time-delay' in t:
            return ('Human-Robot Interaction', 'Teleoperation',
                    'Bilateral Teleoperation')
        if 'haptic' in t:
            return ('Human-Robot Interaction', 'Teleoperation',
                    'Haptic Teleoperation')
        if ' vr ' in t or 'virtual reality' in t or ' ar ' in t \
                or 'augmented reality' in t:
            return ('Human-Robot Interaction', 'Teleoperation',
                    'VR/AR Teleoperation')
        return ('Human-Robot Interaction', 'Teleoperation',
                'General Teleoperation')

    if has_any(t, SHARED_AUT):
        return ('Human-Robot Interaction', 'Shared Autonomy',
                'Shared Autonomy / Control')
    if has_any(t, COBOT):
        return ('Human-Robot Interaction', 'Physical HRI',
                'Collaborative Robot / Co-manipulation')
    if has_any(t, SOC_HRI):
        if 'social navigation' in t or 'crowd' in t or 'pedestrian' in t \
                or 'socially compliant' in t or 'socially-aware' in t \
                or 'socially aware' in t:
            return ('Human-Robot Interaction', 'Social Robotics',
                    'Social Navigation')
        return ('Human-Robot Interaction', 'Social Robotics',
                'Social Robot / HRI Study')
    if 'human-robot' in t or 'human robot' in t or ' hri ' in t \
            or 'human-augment' in t or 'human augmentation' in t:
        return ('Human-Robot Interaction', 'Physical HRI',
                'General HRI')

    # ===========================================================
    # 9. MULTI-ROBOT SYSTEMS
    # ===========================================================
    if has_any(t, SWARM):
        return ('Multi-Robot Systems', 'Swarm Robotics', 'Swarm')
    if has_any(t, AERIAL_SWARM):
        return ('Multi-Robot Systems', 'Aerial Swarms / UAV Swarms',
                'Decentralized Aerial Swarm')
    if has_any(t, MAPF):
        return ('Multi-Robot Systems', 'Multi-Robot Planning',
                'Multi-Agent Path Finding (MAPF)')
    if has_any(t, RESILIENT) and has_any(t, MULTI_R + ['robot']):
        return ('Multi-Robot Systems', 'Coordination',
                'Resilient / Adversarial Multi-Robot')
    if has_any(t, PURSUIT):
        return ('Multi-Robot Systems', 'Coordination',
                'Pursuit-Evasion / Surveillance / Patrolling')
    if has_any(t, FORMATION):
        return ('Multi-Robot Systems', 'Coordination',
                'Formation / Consensus / Flocking')
    if has_any(t, TASK_ALLOC):
        return ('Multi-Robot Systems', 'Coordination',
                'Task Allocation / Auction')
    if has_any(t, MULTI_R):
        if 'slam' in t or 'mapping' in t:
            return ('Multi-Robot Systems', 'Multi-Robot SLAM',
                    'Distributed / Cooperative SLAM')
        if has_any(t, PLAN_PATH) or 'planning' in t:
            return ('Multi-Robot Systems', 'Multi-Robot Planning',
                    'Multi-Robot Motion Planning')
        if 'control' in t:
            return ('Multi-Robot Systems', 'Coordination',
                    'Multi-Robot Control')
        if 'optimization' in t or 'distributed' in t:
            return ('Multi-Robot Systems',
                    'Distributed Algorithms / Optimization',
                    'Distributed Optimization')
        return ('Multi-Robot Systems', 'Coordination',
                'Multi-Robot Coordination')

    # ===========================================================
    # 10. LEARNING (general, after Foundation Models)
    # ===========================================================
    if has_any(t, SIM2REAL):
        return ('Learning for Robotics', 'Reinforcement Learning',
                'Sim-to-Real')
    if has_any(t, INV_RL):
        return ('Learning for Robotics', 'Reinforcement Learning',
                'Inverse RL')
    if has_any(t, RL):
        if has_any(t, ['multi-agent', 'multiagent']):
            return ('Learning for Robotics', 'Reinforcement Learning',
                    'Multi-agent RL')
        if has_any(t, ['safe rl', 'safe reinforcement']):
            return ('Learning for Robotics', 'Reinforcement Learning',
                    'Safe RL / Constrained RL')
        return ('Learning for Robotics', 'Reinforcement Learning', 'RL')
    if has_any(t, IL) or has_any(t, PBD):
        if 'human video' in t or 'in the wild' in t or 'in-the-wild' in t \
                or 'youtube' in t:
            return ('Learning for Robotics', 'Imitation Learning',
                    'In-the-Wild / From-Human-Video IL')
        return ('Learning for Robotics', 'Imitation Learning',
                'Behavior Cloning / LfD / PbD')
    if has_any(t, META_LEARN):
        return ('Learning for Robotics', 'Meta / Few-shot Learning',
                'Meta-learning')
    if has_any(t, TRANSFER_L):
        return ('Learning for Robotics', 'Transfer Learning',
                'Domain Adaptation / Transfer')
    if has_any(t, CONTINUAL):
        return ('Learning for Robotics', 'Continual Learning',
                'Lifelong Learning')
    if has_any(t, SELF_SUP):
        return ('Learning for Robotics', 'Self-supervised Learning',
                'Self-supervised / Representation')
    if has_any(t, ACTIVE_LEARN):
        return ('Learning for Robotics', 'Active Learning',
                'Active Learning')
    if has_any(t, DATASET):
        if 'simulator' in t or 'simulation framework' in t:
            return ('Learning for Robotics', 'Datasets & Benchmarks',
                    'Simulator')
        if 'benchmark' in t:
            return ('Learning for Robotics', 'Datasets & Benchmarks',
                    'Benchmark')
        return ('Learning for Robotics', 'Datasets & Benchmarks',
                'Dataset')

    # ===========================================================
    # 11. PLANNING
    # ===========================================================
    if has_any(t, TAMP):
        return ('Planning', 'Task & Motion Planning', 'TAMP')
    if has_any(t, SYMB_PLAN):
        return ('Planning', 'Task & Motion Planning',
                'Symbolic / PDDL Planning')
    if has_any(t, BELIEF):
        return ('Planning', 'Belief Space Planning',
                'POMDP / Belief Space Planning')
    if has_any(t, FOOTSTEP):
        return ('Planning', 'Specialized Planning',
                'Footstep / Gait Planning')
    if has_any(t, MANIP_PLAN):
        return ('Planning', 'Specialized Planning', 'Manipulation Planning')
    if has_any(t, EXPLORE):
        return ('Planning', 'Navigation', 'Autonomous Exploration')
    if has_any(t, COVERAGE):
        return ('Planning', 'Navigation', 'Coverage Planning')
    if has_any(t, OBSTACLE):
        return ('Planning', 'Navigation', 'Obstacle / Collision Avoidance')
    if has_any(t, VLN):
        return ('Planning', 'Navigation', 'Vision-Language Navigation')
    if has_any(t, OFFROAD_NAV):
        return ('Planning', 'Navigation',
                'Off-road / Unstructured Terrain Navigation')
    if has_any(t, SOCIAL_NAV):
        return ('Human-Robot Interaction', 'Social Robotics',
                'Social Navigation')
    if has_any(t, NAVIG):
        return ('Planning', 'Navigation', 'Mobile Navigation')
    if has_any(t, RRT_LIKE):
        return ('Planning', 'Path/Motion Planning',
                'Sampling-based Planning')
    if has_any(t, SEARCH_PLAN):
        return ('Planning', 'Path/Motion Planning',
                'Search-based Planning')
    if 'graphs of convex' in t or 'convex set' in t:
        return ('Planning', 'Path/Motion Planning',
                'Graphs of Convex Sets')
    if has_any(t, ['diffusion model']) and 'planning' in t:
        return ('Planning', 'Path/Motion Planning',
                'Diffusion-based Planning')
    if 'neural motion planning' in t or 'neural mp' in t \
            or 'mpnet' in t or 'iplanner' in t or 'neupan' in t:
        return ('Planning', 'Path/Motion Planning',
                'Neural / Learning-based Motion Planning')
    if has_any(t, TRAJOPT):
        return ('Planning', 'Path/Motion Planning',
                'Trajectory Optimization')
    if has_any(t, PLAN_PATH):
        return ('Planning', 'Path/Motion Planning',
                'Motion / Path Planning')
    if has_any(t, MOT_PRIM):
        return ('Planning', 'Path/Motion Planning',
                'Motion Primitives / DMP')

    # ===========================================================
    # 12. CONTROL
    # ===========================================================
    if has_any(t, CONTACT_IMP_MPC):
        return ('Control', 'Optimal / Predictive Control',
                'Contact-Implicit MPC')
    if has_any(t, MPC):
        if 'mppi' in t or 'sampling-based mpc' in t:
            return ('Control', 'Optimal / Predictive Control',
                    'Sampling-based MPC / MPPI')
        return ('Control', 'Optimal / Predictive Control',
                'Model Predictive Control (MPC)')
    if has_any(t, LQR):
        return ('Control', 'Optimal / Predictive Control',
                'LQR / iLQR / DDP')
    if has_any(t, CBF):
        return ('Control', 'Safety-Critical Control',
                'Control Barrier Functions (CBF)')
    if has_any(t, REACH):
        return ('Control', 'Safety-Critical Control',
                'Reachability Analysis')
    if has_any(t, ILC):
        return ('Control', 'Learning-based Control',
                'Iterative Learning Control')
    if has_any(t, KOOPMAN):
        return ('Control', 'Learning-based Control',
                'Koopman Operator Control')
    if has_any(t, DIFFPHY):
        return ('Control', 'Learning-based Control',
                'Differentiable Physics / Sim')
    if has_any(t, CPG):
        return ('Control', 'Bio-inspired Control', 'Central Pattern Generator')
    if has_any(t, HZD):
        return ('Control', 'Bio-inspired Control', 'Hybrid Zero Dynamics')
    if has_any(t, ADAPT_C):
        return ('Control', 'Classical Control', 'Adaptive Control')
    if has_any(t, ROBUST_C):
        return ('Control', 'Classical Control', 'Robust Control')
    if has_any(t, SLIDE):
        return ('Control', 'Classical Control', 'Sliding Mode Control')
    if has_any(t, NONLIN_C):
        return ('Control', 'Classical Control', 'Nonlinear Control')
    if has_any(t, IMPED):
        return ('Control', 'Force / Impedance Control',
                'Impedance / Admittance')
    if has_any(t, PASSIVITY):
        return ('Control', 'Force / Impedance Control',
                'Passivity-based / Port-Hamiltonian')
    if has_any(t, FORCE_C):
        return ('Control', 'Force / Impedance Control', 'Force Control')
    if has_any(t, WBC):
        return ('Control', 'Whole-Body Control', 'Whole-Body Controller')
    if has_any(t, VS):
        return ('Control', 'Visual Servoing', 'Visual Servoing')

    if 'control' in t and ('controller' in t or 'feedback' in t):
        return ('Control', 'General Control', 'Robot Control')

    # ===========================================================
    # 13. THEORETICAL FOUNDATIONS
    # ===========================================================
    if has_any(t, SDPR):
        return ('Theoretical Foundations', 'Optimization',
                'Semidefinite Relaxations / Certifiable Optimization')
    if has_any(t, DIFFPROG):
        return ('Theoretical Foundations', 'Optimization',
                'Differentiable Programming')
    if has_any(t, EQUIV):
        return ('Theoretical Foundations', 'Geometric Methods',
                'Equivariant Methods')
    if has_any(t, KIN_KW):
        if 'redundant' in t or 'redundancy' in t:
            return ('Theoretical Foundations', 'Kinematics',
                    'Redundancy Resolution')
        if 'singularity' in t:
            return ('Theoretical Foundations', 'Kinematics',
                    'Singularity Analysis')
        if 'workspace' in t:
            return ('Theoretical Foundations', 'Kinematics',
                    'Workspace Analysis')
        if 'inverse kinematic' in t:
            return ('Theoretical Foundations', 'Kinematics',
                    'Inverse Kinematics')
        if 'kinematic design' in t or 'type synthesis' in t \
                or 'kinematic synthesis' in t:
            return ('Theoretical Foundations', 'Kinematics',
                    'Kinematic Design / Type Synthesis')
        return ('Theoretical Foundations', 'Kinematics',
                'Kinematic Analysis')
    if has_any(t, CONTACT_DYN):
        return ('Theoretical Foundations', 'Dynamics',
                'Contact / Friction Modeling')
    if has_any(t, DYN_KW):
        if 'system identification' in t or 'parameter identification' in t:
            return ('Theoretical Foundations', 'Dynamics',
                    'System Identification')
        if 'flexible' in t or 'elastic' in t:
            return ('Theoretical Foundations', 'Dynamics',
                    'Flexible Body Dynamics')
        return ('Theoretical Foundations', 'Dynamics', 'Robot Dynamics')
    if has_any(t, LIE):
        return ('Theoretical Foundations', 'Geometric Methods',
                'Lie Groups / Manifolds')
    if has_any(t, GAME_TH):
        return ('Theoretical Foundations', 'Game Theory',
                'Game-theoretic Robotics')
    if has_any(t, FORMAL):
        return ('Theoretical Foundations', 'Formal Methods',
                'Temporal Logic / Verification')
    if has_any(t, STAB):
        return ('Theoretical Foundations', 'Stability', 'Lyapunov Stability')
    if has_any(t, OPT_KW):
        return ('Theoretical Foundations', 'Optimization',
                'Optimization Methods')
    if has_any(t, GP_KW):
        return ('Theoretical Foundations', 'Probabilistic Methods',
                'Gaussian Processes')

    # Robot Safety & Failure
    if 'collision detection' in t or 'fault detection' in t \
            or 'fault tolerance' in t or 'fault-tolerant' in t \
            or 'failure detection' in t or 'failure recovery' in t \
            or 'anomaly detection' in t:
        return ('Theoretical Foundations', 'Robot Safety & Failure',
                'Collision/Fault/Failure Detection')

    # ===========================================================
    # 14. SOFTWARE & ARCHITECTURE
    # ===========================================================
    if has_any(t, BT):
        return ('Robot Software & Architecture',
                'Behavior Trees / Reactive Architectures',
                'Behavior Tree')
    if has_any(t, ARCH) and not has_any(t, ['adaptive control', 'mpc']):
        return ('Robot Software & Architecture',
                'Robot Architecture / Middleware',
                'Robot Architecture')
    if has_any(t, CODEGEN):
        return ('Robot Software & Architecture',
                'Code Generation / Symbolic Computation',
                'Symbolic Codegen')
    if has_any(t, RT_SYS):
        return ('Robot Software & Architecture',
                'Real-time Systems / Scheduling',
                'Real-time Scheduling')
    if has_any(t, PROGRAMM):
        return ('Robot Software & Architecture',
                'Robot Programming / DSL',
                'Robot Programming Framework')

    # Safe RL or sim-to-real explicit
    if 'neural network' in t and 'control' in t:
        return ('Learning for Robotics', 'Deep Learning Application',
                'Neural Network Method')
    if 'deep learning' in t or 'deep neural' in t:
        return ('Learning for Robotics', 'Deep Learning Application',
                'Deep Learning Method')

    # Manipulation generic catchall
    if 'manipulation' in t or 'manipulator' in t:
        return ('Manipulation', 'General Manipulation',
                'Manipulator Control / Planning')

    # Grasping / pickup catchall
    if 'pick' in t or 'place' in t:
        return ('Manipulation', 'Grasping', 'Grasp Planning / Synthesis')

    # ===========================================================
    # SECONDARY/FALLBACK rules — catch many missed cases
    # ===========================================================

    # Foundation models / language adjacency
    if 'instruction augmentation' in t or 'instruction following' in t \
            or 'language-driven' in t or 'language driven' in t \
            or 'representation learning for robot' in t \
            or 'compositional generative' in t \
            or 'visual language' in t or 'tactile-language' in t \
            or 'embedded ai' in t or 'language inst' in t:
        return ('Learning for Robotics', 'Foundation Models',
                'Language / Foundation-model Reasoning')

    # Bipedal limit cycle walkers / passive walkers / balance
    if 'limit cycle walker' in t or 'passive walker' in t \
            or 'passive dynamic walking' in t or 'passive walking' in t \
            or 'passive dynamic' in t or 'walking machines' in t \
            or 'gait sensitivity' in t or 'compass-like biped' in t \
            or 'monopod' in t or 'point-mass hopper' in t \
            or 'point-mass sprung-leg' in t or 'spring-loaded inverted' in t \
            or 'spring loaded inverted pendulum' in t \
            or ' slip ' in t and 'walk' in t:
        return ('Locomotion', 'Legged Locomotion', 'Bipedal / Humanoid')
    if 'hopper' in t or 'hopping' in t and 'robot' in t \
            or 'jumping robot' in t or 'monopod' in t or 'leaping' in t:
        return ('Locomotion', 'Bio-inspired Locomotion', 'Jumping / Hopping')

    # Mechanism design — wrist, shoulder, finger, joint design
    if any(kw in t for kw in ['wrist mechanism', 'shoulder mechanism',
                              'wrist design', 'shoulder design',
                              'joint mechanism', 'joint design',
                              'finger design', 'finger mechanism',
                              'cybernetic shoulder', 'biological shoulder',
                              'spherical wrist', 'spherical mechanism',
                              'dexterous mechanism', 'wrist motor',
                              'compliant mechanism',
                              'parallel mechanisms', 'parallel mechanism',
                              'differential mechanism',
                              'underactuated mechanism',
                              'foldable mechanism', 'transformable mechanism',
                              'compliant joint', 'flexure mechanism']):
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Mechanism / Joint Design')

    # Robotic insect / biomimetic insect
    if 'robotic insect' in t or 'biomimetic insect' in t \
            or 'biomimetic robotic insect' in t \
            or 'insect-scale robotic' in t or 'insect scale robot' in t \
            or 'flying insect' in t and 'robot' in t \
            or 'robotic ostraciiform' in t or 'micro air vehicle' in t \
            or 'fly-inspired' in t or 'water strider' in t \
            and 'robot' in t or 'hummingbird' in t and 'robot' in t \
            or 'biologically inspired water strider' in t \
            or 'biomimetic robotic dual-camera' in t:
        return ('Locomotion', 'Aerial Locomotion',
                'Insect-scale / Pico Aerial')

    # Magnetic levitation / Magnetic actuation systems
    if 'magnetic levitation' in t or 'electromagnetic actuat' in t \
            or 'magnetic field control' in t or 'electromagnetic coil' in t \
            or 'magnetic actuat' in t and 'system' in t:
        return ('Robot Design & Hardware', 'Actuators',
                'Magnetic / Electromagnetic Actuator')

    # Multi-view / data association / state estimation
    if 'data association' in t or 'multiview' in t and 'data association' in t \
            or 'multi-view data association' in t \
            or 'random finite set' in t or 'set-labelled filter' in t \
            or 'set-labeled filter' in t or 'combinatorial filter' in t \
            or 'switching kalman' in t or 'state-space minim' in t:
        return ('SLAM & Localization', 'State Estimation',
                'Data Association / Filter Design')

    # Geometric perception / probabilistic
    if 'geometric perception' in t or 'maximum correntropy' in t \
            or 'robust geometric' in t or 'pose graph optim' in t:
        return ('Theoretical Foundations', 'Probabilistic Methods',
                'Robust Geometric Perception')

    # Collision detection / proximity queries / distance computation
    if 'collision detect' in t or 'collision check' in t \
            or 'proximity quer' in t or 'distance computation' in t \
            or 'penetration depth' in t or 'collision avoidance' in t \
            or 'minimum distance' in t and 'robot' in t \
            or 'collision proximity' in t \
            or 'continuous collision' in t:
        return ('Theoretical Foundations', 'Robot Safety & Failure',
                'Collision / Distance Computation')

    # Friction / energy / motion economy
    if 'friction estimation' in t or 'friction model' in t \
            or 'energy-minimizing path' in t or 'energy minim' in t \
            and 'path' in t:
        return ('Theoretical Foundations', 'Dynamics',
                'Contact / Friction Modeling')

    # Wheel-leg hybrid
    if ('wheel' in t and 'leg' in t) or 'wheel transformer' in t \
            or 'wheel-leg hybrid' in t or 'transformable wheel' in t \
            or 'leg-wheel' in t or 'leg wheel' in t:
        return ('Locomotion', 'Legged Locomotion', 'Hybrid Wheel-Leg')

    # Software architecture / robot frameworks (broader)
    if 'instrumented sensor system' in t or 'sensor system architecture' in t \
            or 'robot software' in t or 'software architecture' in t \
            or 'software synthesis' in t and 'robot' in t \
            or 'robotic framework' in t or 'robot framework' in t \
            or 'simulation framework' in t \
            or 'simulator design' in t or 'kubernetes' in t \
            or 'orchestration of' in t and 'robot' in t \
            or 'mixed-criticality' in t:
        return ('Robot Software & Architecture',
                'Robot Architecture / Middleware', 'Architecture / Software')

    # Anthropomorphic / Movement analysis (HRI/biomechanics)
    if 'anthropomorphic' in t and ('motion' in t or 'movement' in t
                                   or 'analysis' in t):
        return ('Human-Robot Interaction', 'Physical HRI',
                'Anthropomorphic Movement Analysis')

    # Robotic skill / task acquisition (Imitation Learning)
    if 'skill acquisition' in t or 'skill learning' in t \
            or 'task learning' in t or 'learning skill' in t \
            or 'sparse demonstration' in t or 'demonstration learning' in t \
            or 'robot learning' in t and 'demonstration' in t \
            or 'in-context imitation' in t or 'one-shot imitation' in t \
            or 'one shot imitation' in t:
        return ('Learning for Robotics', 'Imitation Learning',
                'Skill Learning from Demonstration')

    # Coverage / ergodic search
    if 'ergodic search' in t or 'ergodic exploration' in t \
            or 'ergodic coverage' in t or 'ergodic specifications' in t \
            or 'ergodic optimal' in t:
        return ('Planning', 'Navigation', 'Coverage Planning')

    # Topological mapping / scene representation
    if 'topological mapping' in t or 'topological map' in t \
            or 'topological representation' in t \
            or 'topological motion planning' in t \
            or 'persistent homology' in t or 'simplicial complex' in t:
        return ('SLAM & Localization', 'SLAM', 'Semantic SLAM')

    # Sensor planning / scheduling / view planning
    if 'view planning' in t or 'sensor planning' in t \
            or 'sensor scheduling' in t or 'view selection' in t \
            or 'sensor placement' in t or 'sensor pose' in t \
            and 'plan' in t:
        return ('Perception & Sensing', 'Active Perception',
                'View / Sensor Planning')

    # Path tracking / following
    if 'path tracking' in t or 'path-tracking' in t \
            or 'path following' in t or 'path-following' in t \
            or 'trajectory tracking' in t or 'trajectory-tracking' in t:
        return ('Control', 'General Control', 'Path/Trajectory Tracking')

    # Motion control / motion generation
    if 'motion control' in t or 'motion generation' in t \
            or 'motion synthesis' in t:
        return ('Control', 'General Control', 'Motion Control / Generation')

    # Pose tracking / pose estimation specific
    if 'pose tracking' in t or 'pose-tracking' in t:
        return ('SLAM & Localization', 'Localization', 'Pose Tracking')
    if 'perspective-n-point' in t or 'perspective n point' in t \
            or ' pnp ' in t or 'pnp problem' in t:
        return ('Perception & Sensing', 'Visual Perception',
                'Pose Estimation')

    # Stiffness modeling / soft analysis
    if 'stiffness model' in t or 'stiffness analysis' in t \
            or 'stiffness control' in t and 'soft' in t \
            or 'stiffness mapping' in t:
        return ('Robot Design & Hardware', 'Soft Robotics',
                'Soft Robot Modeling')

    # Force / force sensor / load
    if 'force sensor' in t or 'force/torque sensor' in t \
            or 'torque sensor' in t or 'load sensing' in t \
            or 'force measurement' in t or 'fiber-optic force' in t \
            or 'force/torque' in t or 'f/t sensor' in t:
        return ('Robot Design & Hardware', 'Sensors',
                'Force/Torque Sensor')

    # Drive / transmission / gear
    if 'transmission' in t and 'robot' in t or 'drive train' in t \
            or 'gear train' in t or 'differential drive' in t \
            and 'design' in t or 'harmonic drive' in t \
            or 'hydraulic transmission' in t or 'tendon-sheath' in t:
        return ('Robot Design & Hardware', 'Actuators',
                'Drive / Transmission')

    # Vector field / potential field methods
    if 'potential field' in t or 'vector field' in t \
            or 'navigation function' in t or 'guiding vector field' in t:
        return ('Planning', 'Path/Motion Planning',
                'Vector Field / Potential Field Methods')

    # Pursuit / cooperative search of moving targets
    if 'unknown moving' in t and 'target' in t or 'transient radio' in t \
            or 'target tracking' in t and 'multi' in t \
            or 'cooperative search' in t:
        return ('Multi-Robot Systems', 'Coordination',
                'Multi-Robot Search / Tracking')

    # AIBO / pet robot / digital creature
    if 'aibo' in t or 'digital creature' in t or 'pet robot' in t \
            or 'animatronic' in t:
        return ('Application Domains', 'Service Robotics',
                'Entertainment / Pet Robot')

    # Dante / volcano / specific exploration platforms
    if 'dante' in t or 'volcano' in t or 'subterranean' in t \
            or 'subt challenge' in t or 'cave exploration' in t \
            or 'underwater cave' in t or 'cavepi' in t:
        return ('Application Domains', 'Field Robotics',
                'Exploration Platforms (cave/volcano/subterranean)')

    # Polar / Antarctic / extreme environment
    if 'antarctic' in t or 'arctic' in t or 'ice field' in t \
            or 'broken ice' in t or 'extreme environment' in t \
            or 'polar robot' in t or 'lunar prosp' in t:
        return ('Application Domains', 'Field Robotics',
                'Extreme Environment / Polar')

    # Tractor-trailer / Articulated vehicle
    if 'tractor-trailer' in t or 'tractor trailer' in t \
            or 'articulated vehicle' in t or 'lhd ' in t \
            or 'agricultural vehicle' in t:
        return ('Locomotion', 'Wheeled Locomotion',
                'Articulated Vehicle / Tractor')

    # Cobot's hand controller / haptic display
    if 'cobotic' in t or 'cobot' in t and 'hand controller' in t:
        return ('Human-Robot Interaction', 'Physical HRI',
                'Collaborative Robot / Co-manipulation')

    # Body / motion analysis humans
    if 'human pose' in t or 'human motion' in t and 'tracking' in t \
            or 'human activity' in t or 'recognizing walking people' in t \
            or 'human dynamics' in t and 'monocular' in t \
            or 'motion capture' in t and 'human' in t:
        return ('Perception & Sensing', 'Visual Perception',
                'Human Motion / Activity Recognition')

    # Microassembly
    if 'microassembly' in t or 'micro assembly' in t \
            or 'micromanipulation' in t or 'micro manipulation' in t \
            or 'cell injection' in t or 'cell manipulation' in t \
            or 'microparticle' in t or 'microbead' in t \
            or 'micro-injection' in t or 'micro-objects' in t:
        return ('Robot Design & Hardware', 'Microrobotics',
                'Micromanipulation / Microassembly')

    # Compliant motion / compliant control / compliance
    if 'compliant motion' in t or 'compliance specification' in t \
            or 'compliant control' in t \
            or 'compliant robot' in t and 'motion' in t \
            or 'compliant contact' in t:
        return ('Control', 'Force / Impedance Control',
                'Compliant Motion / Specification')

    # Caging
    if 'caging' in t or 'cage ' in t and 'object' in t:
        return ('Manipulation', 'Grasping', 'Caging-based Grasping')

    # Stability / Lyapunov / region of attraction
    if 'stability' in t and 'control' in t or 'stabilization' in t \
            or 'region of attraction' in t or 'lyapunov' in t \
            or 'controllability' in t and 'robot' in t:
        return ('Theoretical Foundations', 'Stability', 'Stability / Lyapunov')

    # Differential dynamic programming / DDP
    if 'differential dynamic programming' in t or 'ddp' in t \
            or 'iLQR' in t or 'iterative lqr' in t:
        return ('Control', 'Optimal / Predictive Control', 'LQR / iLQR / DDP')

    # Recognition (general visual)
    if 'recognition' in t and ('object' in t or 'shape' in t
                               or 'visual' in t or 'pattern' in t):
        return ('Perception & Sensing', 'Visual Perception',
                'Object Detection / Recognition')

    # Workpiece / surface features (manufacturing inspection)
    if 'workpiece' in t or 'workpiece feature' in t \
            or 'manufacturing' in t and 'robot' in t:
        return ('Application Domains', 'Field Robotics',
                'Industrial / Manufacturing')

    # Welding / spray painting / industrial robot tasks
    if 'welding' in t or 'spray paint' in t or 'spray-painting' in t \
            or 'paint stripping' in t or 'aircraft assembly' in t:
        return ('Application Domains', 'Field Robotics',
                'Industrial / Manufacturing')

    # Pipeline / sewer / pipe inspection
    if 'pipe' in t and 'robot' in t or 'pipeline' in t or 'sewer' in t \
            or 'in-pipe' in t or 'tubular environment' in t:
        return ('Application Domains', 'Field Robotics', 'Inspection Robotics')

    # Generic exploration/discovery
    if 'exploration' in t and 'robot' in t:
        return ('Planning', 'Navigation', 'Autonomous Exploration')

    # Filter (state estimation)
    if 'particle filter' in t or 'kalman filter' in t \
            or 'information filter' in t:
        return ('SLAM & Localization', 'State Estimation', 'Bayesian Filtering')

    # Skin / sensor (tactile catchall)
    if 'sensitive skin' in t or 'robot skin' in t or 'tactile skin' in t \
            or 'finger-shaped sensor' in t or 'fingertip touch' in t \
            or 'whisker' in t and 'sensor' in t \
            or 'skin sensor' in t:
        return ('Perception & Sensing', 'Tactile Sensing',
                'Tactile Sensors / Algorithms')

    # Walking / gait (catchall for legged not yet caught)
    if 'walking' in t and ('robot' in t or 'machine' in t or 'biped' in t):
        return ('Locomotion', 'Legged Locomotion', 'Bipedal / Humanoid')
    if 'gait' in t and ('robot' in t or 'biped' in t or 'leg' in t
                        or 'quadruped' in t):
        return ('Locomotion', 'Legged Locomotion', 'Legged (general)')

    # Hand / finger (manipulation hardware)
    if 'robotic hand' in t or 'robotic finger' in t or 'finger gait' in t \
            or 'multifinger' in t or 'multi-finger' in t \
            or 'robot hand' in t and ('design' in t or 'mechanism' in t
                                      or 'kinematic' in t):
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Robotic Hand / Finger Design')

    # Folding / origami (catchall)
    if 'folding' in t or 'origami' in t or 'foldable' in t:
        return ('Robot Design & Hardware', 'Soft Robotics',
                'Origami / Folding Mechanism')

    # Magnetic / micro related (catchall)
    if 'magnetic' in t and ('control' in t or 'manipulat' in t
                            or 'navig' in t or 'actuat' in t):
        return ('Robot Design & Hardware', 'Microrobotics',
                'Magnetic Manipulation')

    # In-flight catching / juggling / dynamic skills
    if 'juggling' in t or 'in-flight' in t and 'object' in t \
            or 'batting' in t and 'object' in t \
            or 'catching' in t and 'object' in t:
        return ('Manipulation', 'General Manipulation',
                'Dynamic / In-flight Manipulation')

    # Model-Based / data-driven catchall
    if 'data-driven' in t or 'model-free' in t or 'model-based' in t \
            and 'control' in t:
        return ('Control', 'Learning-based Control',
                'Data-driven / Model-based Control')

    # Generic safety / safe control
    if 'safety filter' in t or 'safety-critical' in t \
            or 'safe control' in t or 'safe motion' in t \
            or 'safe planning' in t or 'safe robot' in t:
        return ('Control', 'Safety-Critical Control', 'Safe Control')

    # Estimation / observer (catchall)
    if 'observer' in t and 'control' in t or 'estimation' in t \
            and 'observer' in t:
        return ('Control', 'Classical Control', 'Observer-based Control')
    if 'estimation' in t and ('state' in t or 'parameter' in t):
        return ('SLAM & Localization', 'State Estimation', 'General State Estimation')

    # Survey/Review papers (likely in many fields)
    if 'survey' in t or 'review' in t and 'robot' in t:
        return ('Other / Editorial', 'Editorial / Meta', 'Survey / Review')

    # Generic robot motion / robot control
    if 'robot motion' in t or 'robot control' in t or 'robot dynamics' in t:
        return ('Control', 'General Control', 'Robot Control / Motion')

    # Architectures / scheduling for robots
    if 'scheduling' in t and 'robot' in t:
        return ('Multi-Robot Systems', 'Coordination',
                'Task Allocation / Scheduling')

    # Mobile robot catchall
    if 'mobile robot' in t and ('navig' in t or 'control' in t
                                or 'localiz' in t or 'plan' in t):
        return ('Locomotion', 'Wheeled Locomotion', 'Mobile Wheeled Robot')
    if 'mobile robot' in t:
        return ('Locomotion', 'Wheeled Locomotion', 'Mobile Wheeled Robot')

    # Underactuated / passive joint catchall
    if 'underactuated' in t or 'under-actuated' in t \
            or 'passive joint' in t:
        return ('Control', 'Classical Control',
                'Underactuated System Control')

    # ===========================================================
    # TERTIARY rules — third pass to mop up specific patterns
    # ===========================================================

    # Scan registration / point set registration
    if 'scan registration' in t or 'scan matching' in t \
            or 'point set registration' in t \
            or 'point cloud registration' in t \
            or ' icp ' in t or 'iterative closest point' in t \
            or 'ndt ' in t or '-ndt ' in t \
            or 'fuzzy cluster' in t and 'registration' in t \
            or 'doppler correspondence' in t:
        return ('Perception & Sensing', 'LiDAR Perception',
                'Point Cloud Registration')

    # Bio-inspired (catchall — animals/biology)
    if any(kw in t for kw in ['bio-inspired', 'bioinspired',
                              'biologically inspired', 'biomimetic',
                              'biomimetics', 'bio-mimetic']):
        if 'aerial' in t or 'flying' in t or 'wing' in t:
            return ('Locomotion', 'Aerial Locomotion',
                    'Insect-scale / Pico Aerial')
        if 'swim' in t or 'fish' in t or 'aquatic' in t \
                or 'underwater' in t:
            return ('Locomotion', 'Bio-inspired Locomotion',
                    'Swimming / Fish Robot')
        if 'leg' in t or 'walk' in t:
            return ('Locomotion', 'Legged Locomotion', 'Legged (general)')
        if 'sensor' in t or 'eye' in t or 'vision' in t:
            return ('Perception & Sensing', 'Visual Perception',
                    'Bio-inspired Vision / Sensors')
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Bio-inspired Mechanism')

    # Locust / bat / cockroach / fly / dragonfly / etc. (animal-inspired)
    if any(kw in t for kw in ['locust-', ' bats ', ' bat ',
                              'cockroach', 'fly-inspired',
                              'dragonfly', 'wasp ', 'gecko',
                              'ant ', 'salamander', 'turtle',
                              'cheetah', 'hummingbird', 'butterfly',
                              'spider', 'sandfish', 'beetle']):
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Bio-inspired Mechanism')

    # Camera / Pan-Tilt-Zoom / specific camera systems
    if 'pan-tilt' in t or 'pan tilt' in t or 'ptz' in t \
            or 'camera-orienting' in t or 'camera orient' in t:
        return ('Perception & Sensing', 'Visual Perception',
                'Camera System / Tracking')

    # Mealtime / dressing assistance / feeding
    if 'mealtime' in t or 'feeding via' in t or 'feeding-via' in t \
            or 'flair' in t and 'feeding' in t \
            or 'dress people' in t or 'dressing' in t \
            and 'assist' in t:
        return ('Human-Robot Interaction', 'Assistive Robotics',
                'Feeding / Dressing Assistance')

    # Tutor / nurse training robot
    if 'robotic tutor' in t or 'tutor robot' in t \
            or 'training robot' in t or 'nurse training' in t \
            or 'small talk' in t:
        return ('Application Domains', 'Service Robotics',
                'Educational / Healthcare Tutor')

    # Reward shaping / RL gain adaptation
    if 'reward gain' in t or 'reward learning' in t \
            or 'reward function' in t or 'reward shaping' in t \
            or 'reward design' in t or 'reward-based' in t \
            or 'reward sketching' in t or 'preference learning' in t:
        return ('Learning for Robotics', 'Reinforcement Learning',
                'Reward Learning')

    # Flying / drone in narrow spaces / tunnels
    if ('autonomous flight' in t or 'flying' in t and 'autonomous' in t) \
            and ('tunnel' in t or 'cluttered' in t or 'narrow' in t
                 or 'forest' in t):
        return ('Locomotion', 'Aerial Locomotion',
                'Aggressive / Cluttered Environment Flight')

    # Active sensing / Fisher information / mutual information
    if 'fisher information' in t or 'mutual information' in t and 'robot' in t \
            or 'information-theoretic' in t and ('mapping' in t
                                                 or 'plan' in t
                                                 or 'sensing' in t) \
            or 'shannon mutual' in t:
        return ('Perception & Sensing', 'Active Perception',
                'Information-theoretic Sensing')

    # Convex regions / safe regions
    if 'convex region' in t or 'convex hull' in t and 'plan' in t \
            or 'safe regions' in t or 'safe boxes' in t \
            or 'iris' in t and 'plan' in t \
            or 'region inflation' in t:
        return ('Planning', 'Path/Motion Planning',
                'Convex Decomposition / Safe Regions')

    # Generalized Dubins / TSP / vehicle routing
    if 'dubins' in t or 'traveling salesman' in t \
            or 'vehicle routing' in t or 'tsp ' in t:
        return ('Planning', 'Specialized Planning',
                'Routing / TSP / Dubins')

    # Mid-level / latent / policies / motion policies
    if 'motion polic' in t or 'latent action' in t \
            or 'latent policy' in t or 'latent space' in t and 'plan' in t \
            or 'generalist policy' in t or 'generalizable polic' in t \
            or 'policy distillation' in t or 'policy learning' in t \
            or 'mid-level representation' in t \
            or 'spatially-grounded' in t:
        return ('Learning for Robotics', 'Foundation Models',
                'Generalist / Cross-embodiment Policies')

    # Musculoskeletal / bionic leg
    if 'musculoskeletal' in t or 'bionic leg' in t \
            or 'bionic limb' in t or 'bionic shoulder' in t \
            or 'bionic ' in t and ('leg' in t or 'arm' in t):
        return ('Human-Robot Interaction', 'Assistive Robotics',
                'Bionic / Musculoskeletal')

    # Rehabilitation device / human stepping / robot-assisted
    if 'robot-assisted' in t and 'human' in t \
            or 'manipulating human stepping' in t \
            or 'robot-aided' in t or 'rehabilitation device' in t \
            or 'gait assistance' in t or 'walk assistance' in t:
        return ('Human-Robot Interaction', 'Assistive Robotics',
                'Rehabilitation')

    # Robotic skin / artificial skin
    if 'robotic skin' in t or 'robot skin' in t \
            or 'electronic skin' in t or 'artificial skin' in t:
        return ('Perception & Sensing', 'Tactile Sensing',
                'Robotic Skin')

    # Generic actuator catchall (with "robotic applications")
    if 'actuator' in t and 'robot' in t:
        return ('Robot Design & Hardware', 'Actuators', 'Actuator Design')

    # Stochastic / programmable / cellular actuators
    if 'cellular actuator' in t or 'stochastic actuator' in t \
            or 'binary actuator' in t:
        return ('Robot Design & Hardware', 'Actuators',
                'Cellular / Programmable Actuators')

    # Virtual fixtures / virtual constraints
    if 'virtual fixture' in t or 'virtual constraint' in t \
            or 'constraint-based control' in t:
        return ('Control', 'Force / Impedance Control',
                'Virtual Fixtures / Constraints')

    # Vehicle / car detection / aerial detection
    if 'aircraft detect' in t or 'vehicle detect' in t and 'aerial' in t:
        return ('Perception & Sensing', 'Visual Perception',
                'Vehicle / Aircraft Detection')

    # Light field / photography (perception)
    if 'light field' in t or 'plenoptic' in t \
            or 'time-lapse' in t and 'light' in t:
        return ('Perception & Sensing', 'Visual Perception',
                'Light Field / Plenoptic')

    # Dynamic vehicle routing / traffic
    if 'traffic' in t and ('flow' in t or 'control' in t or 'mixed' in t):
        return ('Application Domains', 'Autonomous Driving',
                'Traffic / Mixed Autonomy')

    # Computational design / morphology optimization
    if 'computational design' in t or 'morphology optim' in t \
            or 'co-design' in t or 'codesign' in t and 'robot' in t \
            or 'design optimization' in t and 'robot' in t:
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Computational Design / Morphology')

    # Conformal prediction / safety assurance
    if 'conformal prediction' in t or 'safety assurance' in t \
            or 'safety guarantee' in t:
        return ('Control', 'Safety-Critical Control',
                'Safety Assurance / Conformal Prediction')

    # Yoyo / swing-up / pendubot / acrobot
    if 'yoyo' in t or 'pendubot' in t or 'acrobot' in t \
            or 'swing-up' in t or 'inverted pendulum' in t:
        return ('Control', 'General Control',
                'Underactuated Pendulum / Swing-up')

    # SVD / linear algebra applied to robotics
    if 'singular value decomposition' in t and 'robot' in t \
            or 'parallel processing' in t and 'robot' in t:
        return ('Theoretical Foundations', 'Optimization',
                'Linear Algebra Methods')

    # Self-organizing maps / cellular automata for robotics
    if 'self-organizing map' in t or 'cellular automat' in t \
            or 'self organizing' in t:
        return ('Learning for Robotics', 'Deep Learning Application',
                'Self-organizing Methods')

    # Odor / chemical / gas sensing
    if 'odor' in t or 'gas source' in t or 'chemical plume' in t \
            or 'methane' in t or 'gas sensing' in t:
        return ('Perception & Sensing', 'Multi-modal Perception',
                'Olfactory / Chemical Sensing')

    # Bowl feeders / parts orienting (specific industrial)
    if 'bowl feeder' in t or 'vibratory bowl' in t \
            or 'orienting parts' in t or 'orienting toleranced' in t:
        return ('Manipulation', 'Distributed Manipulation',
                'Parts Feeders / Vibratory')

    # Object grasp / handling specific catchall (yoyo, drumming, juggling)
    if 'juggling' in t or 'drumming' in t or 'tennis' in t \
            and 'robot' in t:
        return ('Manipulation', 'General Manipulation',
                'Dynamic / Sports Manipulation')

    # Workspace / robotic orientation workspace
    if 'orientation workspace' in t or 'robotic workspace' in t \
            or 'workspace generation' in t \
            or 'workspace boundary' in t \
            or 'workspace analysis' in t:
        return ('Theoretical Foundations', 'Kinematics', 'Workspace Analysis')

    # Velocity obstacle / RVO / velocity-based collision
    if 'velocity obstacle' in t or 'velocity-obstacle' in t \
            or ' rvo ' in t or 'reciprocal velocity' in t:
        return ('Planning', 'Navigation', 'Obstacle / Collision Avoidance')

    # Model following / model-based control
    if 'model following control' in t \
            or 'model predictive' in t and 'control' in t:
        return ('Control', 'Optimal / Predictive Control',
                'Model-based Control')

    # Disturbance rejection / disturbance observer
    if 'disturbance rejection' in t or 'disturbance observer' in t \
            or 'disturbance estim' in t:
        return ('Control', 'Classical Control',
                'Disturbance Rejection / Observer')

    # Connectivity / connectivity preserving / network control
    if 'connectivity' in t and 'multi' in t \
            or 'connectivity maintenance' in t \
            or 'connectivity preserv' in t:
        return ('Multi-Robot Systems', 'Communication / Networks',
                'Connectivity Maintenance')

    # Compositional / programmable framework for robots
    if 'compositional framework' in t or 'compositional plan' in t \
            or 'compositional generative' in t \
            or 'programmable matter' in t or 'programmable swarm' in t \
            or 'programmable robot' in t:
        return ('Multi-Robot Systems', 'Swarm Robotics',
                'Programmable / Compositional Swarms')

    # Compliant legs / running with springs
    if 'compliant leg' in t or 'leg spring' in t or 'leg-spring' in t \
            or 'curating tunable' in t or 'tunable compliant' in t:
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Compliant Legs / Spring Design')

    # Curriculum learning / training
    if 'curriculum' in t and 'learn' in t \
            or 'transferring experience' in t \
            or 'agile locomotion' in t and 'transfer' in t \
            or 'fast prototyping' in t:
        return ('Learning for Robotics', 'Reinforcement Learning',
                'Sim-to-Real')

    # Aerial perching / climbing
    if 'perching' in t and ('aerial' in t or 'quadrotor' in t
                            or 'drone' in t or 'multimodal robot' in t
                            or 'vertical' in t):
        return ('Locomotion', 'Aerial Locomotion',
                'Aerial Perching / Vertical Surfaces')

    # Coordination of robotic arms (multi-arm)
    if 'multiple robotic arms' in t or 'multiple arms' in t \
            or 'multi-arm' in t and 'coordin' in t:
        return ('Multi-Robot Systems', 'Coordination',
                'Multi-Arm Coordination')

    # Conversational robot / dialogue
    if 'conversational robot' in t or 'dialogue' in t and 'robot' in t \
            or 'conversation' in t and 'robot' in t \
            or 'interruption' in t and 'robot' in t:
        return ('Human-Robot Interaction', 'Social Robotics',
                'Dialogue / Conversational Robot')

    # Vision-based / Visual + something specific
    if 'visual servo' in t or 'visual servoing' in t:
        return ('Control', 'Visual Servoing', 'Visual Servoing')

    # Coverage / sensor network
    if 'sensor network' in t or 'mobile sensor' in t \
            or 'environmental monitoring' in t and 'multi' in t:
        return ('Multi-Robot Systems', 'Coordination',
                'Sensor Network / Coverage')

    # Optical tweezers / cell manipulation
    if 'optical tweezer' in t or 'tweezers' in t and 'cell' in t \
            or 'cell injection' in t:
        return ('Robot Design & Hardware', 'Microrobotics',
                'Cell / Bio Manipulation')

    # Generic multi-rotor task (modeling, design)
    if 'multirotor' in t or 'multi-rotor' in t \
            or 'multicopter' in t or 'quadcopter' in t \
            or 'quadrotor' in t or 'aerial vehicle' in t:
        return ('Locomotion', 'Aerial Locomotion',
                'Multirotor / Quadrotor')

    # Force-based / Impedance / spring-based
    if 'spring-based' in t or 'spring based' in t and 'control' in t \
            or 'series elastic' in t:
        return ('Robot Design & Hardware', 'Actuators',
                'Series Elastic Actuator (SEA)')

    # Geometric mechanics / geometric methods (catchall for theoretical)
    if 'geometric mechanic' in t or 'geometric method' in t and 'robot' in t \
            or 'geometric reasoning' in t \
            or 'geometric treatment' in t:
        return ('Theoretical Foundations', 'Geometric Methods',
                'Geometric Mechanics')

    # Lagrangian flows / coherent structures
    if 'lagrangian coherent' in t or 'flow field' in t and 'underwater' in t:
        return ('Application Domains', 'Field Robotics',
                'Underwater / Ocean Tracking')

    # Endothelial / cell biology
    if 'endothelial' in t or 'angiogenic' in t \
            or 'biological cell' in t and 'robot' in t \
            or 'protein structure' in t and 'robot' in t:
        return ('Application Domains', 'Computational Biology Robotics',
                'Bio-molecular / Cell Biology')

    # Electric sense / aquatic perception
    if 'electric sense' in t or 'electrosense' in t \
            or 'electrolocation' in t or 'lateral line' in t:
        return ('Perception & Sensing', 'Multi-modal Perception',
                'Bio-inspired / Electric Sense')

    # Sparse depth / depth sensing
    if 'depth sensing' in t or 'sparse depth' in t \
            or 'depth sensor' in t and not 'rgb-d' in t:
        return ('Perception & Sensing', 'Visual Perception',
                'Depth Sensing')

    # Object segmentation
    if 'object segmentation' in t or 'unseen object' in t \
            or 'object instance' in t or 'object discov' in t:
        return ('Perception & Sensing', 'Visual Perception',
                'Object Segmentation / Discovery')

    # Mechanical search / object retrieval
    if 'mechanical search' in t or 'object retrieval' in t \
            or 'object rearrangement' in t or 'rearrangement' in t \
            and 'object' in t:
        return ('Manipulation', 'General Manipulation',
                'Object Rearrangement / Retrieval')

    # Robotic device / robotic system catchalls
    if 'robotic device' in t or 'robotic system' in t \
            or 'robotic platform' in t or 'robotic mechanism' in t:
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Robotic System / Device Design')

    # Synthesis of robot / mechanism synthesis
    if 'synthesis of' in t and 'robot' in t \
            or 'mechanism synthesis' in t or 'design of robot' in t \
            or 'design and analysis' in t and 'robot' in t \
            or 'design of a' in t and 'robot' in t \
            or 'design of an' in t and 'robot' in t:
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Robot Mechanism Synthesis')

    # Probabilistic / particle-based methods
    if 'probabilistic' in t and ('plan' in t or 'inference' in t):
        return ('Theoretical Foundations', 'Probabilistic Methods',
                'Probabilistic Methods')

    # Generic dataset paper detection
    if 'dataset' in t or 'data-set' in t or 'data set' in t:
        return ('Learning for Robotics', 'Datasets & Benchmarks', 'Dataset')

    # Generic benchmark
    if 'benchmark' in t:
        return ('Learning for Robotics', 'Datasets & Benchmarks', 'Benchmark')

    # Configuration space / C-space catchall
    if 'configuration space' in t or 'c-space' in t or 'c space' in t:
        return ('Planning', 'Path/Motion Planning', 'Configuration Space')

    # Demonstrating XYZ
    if t.startswith(' demonstrating'):
        return ('Learning for Robotics', 'Datasets & Benchmarks',
                'System Demonstration')

    # Generic 'robotic XYZ' patterns - broad fallbacks
    if 'wireless' in t and 'sensor' in t and 'robot' in t:
        return ('Multi-Robot Systems', 'Communication / Networks',
                'Wireless Sensing for Robots')
    if 'flying' in t or 'aerial' in t:
        return ('Locomotion', 'Aerial Locomotion',
                'General Aerial Robotics')
    if 'underwater' in t or 'aquatic' in t:
        return ('Locomotion', 'Underwater Locomotion', 'AUV / UUV')
    if 'manipulation' in t:
        return ('Manipulation', 'General Manipulation',
                'Manipulator Control / Planning')
    if 'planning' in t:
        return ('Planning', 'Path/Motion Planning', 'Motion / Path Planning')
    if 'control' in t and 'robot' in t:
        return ('Control', 'General Control', 'Robot Control')
    if 'robot' in t and 'design' in t:
        return ('Robot Design & Hardware', 'Mechanism Design',
                'Robot Design (general)')

    # ===========================================================
    # DEFAULT
    # ===========================================================
    return ('Other / Unclassified', 'Unclassified', 'Unclassified')


# ============================================================
# Run
# ============================================================
def main():
    with open('/tmp/papers.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)

    results = []
    for p in papers:
        phy, cls, ord_ = classify(p['title'])
        t = ' ' + p['title'].lower() + ' '
        gen = assign_genus(phy, cls, ord_, t)
        results.append({**p, 'phylum': phy, 'class': cls,
                        'order': ord_, 'genus': gen})

    # Stats
    phy_counts = Counter(r['phylum'] for r in results)
    print("=== PHYLUM distribution ===")
    for k, v in sorted(phy_counts.items(), key=lambda x: -x[1]):
        print(f"  {v:>5}  {k}")

    print("\n=== CLASS distribution (top 30) ===")
    cls_counts = Counter(f"{r['phylum']} > {r['class']}" for r in results)
    for k, v in sorted(cls_counts.items(), key=lambda x: -x[1])[:30]:
        print(f"  {v:>5}  {k}")

    print(f"\n=== Unclassified samples ===")
    unc = [r for r in results if r['phylum'] == 'Other / Unclassified']
    print(f"Total unclassified: {len(unc)} ({len(unc)/len(results)*100:.1f}%)")

    # Genus stats
    print("\n=== Genus assignment stats ===")
    genus_filled = sum(1 for r in results if r['genus'] != '(general)'
                       and r['genus'] != 'Unclassified')
    print(f"Papers with specific Genus (non-general): {genus_filled} "
          f"({genus_filled/len(results)*100:.1f}%)")
    print(f"Papers with '(general)' Genus: "
          f"{sum(1 for r in results if r['genus'] == '(general)')}")

    print("\n=== Top 30 Genus by count ===")
    gen_counts = Counter(f"{r['order']} > {r['genus']}" for r in results
                         if r['genus'] not in ('(general)', 'Unclassified'))
    for k, v in sorted(gen_counts.items(), key=lambda x: -x[1])[:30]:
        print(f"  {v:>4}  {k}")

    with open('/tmp/classified.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(f"\nSaved {len(results)} classified papers to /tmp/classified.json")


if __name__ == '__main__':
    main()
