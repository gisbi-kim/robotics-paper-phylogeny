"""
Generate slides/robotics_phylogeny.tex (Beamer) from the classified
papers dataset.

The slides are a guided tour through robotics' 30+-year evolution
seen through the 4-depth taxonomy. The core narrative is a *cohort
wall*: 1988-2025 split into eight 5-year windows, with each window's
dominant + emerging Classes flagged so paradigm shifts (Foundation
Models 2023, SLAM 2005, sim-to-real 2018, …) jump out.

Output:
    slides/robotics_phylogeny.tex   (~40 frames)

Compile with XeLaTeX (kotex needs it for Korean):
    cd slides && xelatex robotics_phylogeny.tex
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLASSIFIED = ROOT / 'data' / 'intermediate' / 'papers_classified.json'
OUT_TEX = ROOT / 'slides' / 'robotics_phylogeny.tex'

COHORTS = [
    (1988, 1992),
    (1993, 1997),
    (1998, 2002),
    (2003, 2007),
    (2008, 2012),
    (2013, 2017),
    (2018, 2022),
    (2023, 2025),
]

# A short narrative headline for each cohort, hand-curated from the
# emerging-class data. These are the slides' editorial voice.
COHORT_HEADLINES = {
    '1988-1992': ('초기 시대',
        '기구학 · 고전 제어 · 매니퓰레이션의 정식화. 학술지 자체가 시작되는 시기.'),
    '1993-1997': ('형식의 정착',
        'Path planning · force/impedance control이 기본 어휘로. '
        'Wheeled / 모듈러 메커니즘이 표준 platform으로 자리잡음.'),
    '1998-2002': ('모바일 로봇 + 텔레오퍼레이션 등장',
        'IJRR/T-RO 특집호 다수 발행 (Editorial 급증). '
        'Teleoperation, Acoustic perception, Robot architecture가 처음 부상.'),
    '2003-2007': ('SLAM 혁명',
        r'FastSLAM/EKF-SLAM/GraphSLAM 패러다임이 SLAM을 \#9 $\to$ 주류로 끌어올림 (+43 ranks). '
        'Aerial, Medical surgical, Assistive robotics 동시 등장.'),
    '2008-2012': ('학습 기반 로보틱스의 씨앗',
        'Reinforcement Learning · Deep Learning · Datasets/Benchmarks가 '
        'Learning for Robotics Phylum 안에서 처음으로 빈도 임계점 통과.'),
    '2013-2017': ('Visual SLAM · TAMP · 협력 로봇',
        'Physical HRI 폭발 (+38 ranks), Task \\& Motion Planning 정착, '
        'Foundation Models의 미세한 첫 등장 (12편).'),
    '2018-2022': ('Sim-to-Real + RL 주류화',
        r'RL이 +17 ranks로 \#12 진입. Tactile sensing 고점 (\#17). '
        '아직 Foundation Models 폭발 직전의 plateau.'),
    '2023-2025': ('Foundation Models 시대',
        r'Foundation Models가 단 3년만에 +52 ranks $\to$ \#3 (66편). '
        'Diffusion Policy · VLA · 3D Gaussian Splatting SLAM이 동시기에 등장.'),
}


def cohort_label(year: int) -> str | None:
    for lo, hi in COHORTS:
        if lo <= year <= hi:
            return f'{lo}-{hi}'
    return None


def latex_escape(s: str) -> str:
    return (s.replace('\\', r'\textbackslash{}')
             .replace('&', r'\&')
             .replace('%', r'\%')
             .replace('#', r'\#')
             .replace('_', r'\_')
             .replace('$', r'\$')
             .replace('^', r'\^{}')
             .replace('~', r'\~{}')
             .replace('{', r'\{')
             .replace('}', r'\}'))


def load() -> list[dict]:
    with open(CLASSIFIED) as f:
        return json.load(f)


def compute_cohort_stats(papers):
    """Return dict[cohort] = {total, classes (Counter), phyla (Counter)}"""
    out = defaultdict(lambda: {'total': 0,
                               'classes': Counter(),
                               'phyla': Counter()})
    for p in papers:
        c = cohort_label(p['year'])
        if not c:
            continue
        cls = f"{p['phylum']} > {p['class']}"
        out[c]['classes'][cls] += 1
        out[c]['phyla'][p['phylum']] += 1
        out[c]['total'] += 1
    return out


def emerging_classes(stats, cohort, prev, min_count=5, top=5):
    """Classes whose rank rose the most vs prev cohort."""
    if not prev:
        return []
    cur = {n: i for i, (n, _) in enumerate(stats[cohort]['classes'].most_common())}
    pre = {n: i for i, (n, _) in enumerate(stats[prev]['classes'].most_common())}
    movers = []
    for name, cur_r in cur.items():
        if stats[cohort]['classes'][name] < min_count:
            continue
        prev_r = pre.get(name, len(pre) + 50)
        delta = prev_r - cur_r
        if delta > 0:
            movers.append((delta, name, cur_r + 1, stats[cohort]['classes'][name]))
    movers.sort(reverse=True)
    return movers[:top]


def faded_classes(stats):
    """Classes that were ≥20 in pre-2015 and ≤10% retention post-2020."""
    pre = Counter()
    post = Counter()
    pre_cohorts = ['1988-1992', '1993-1997', '1998-2002', '2003-2007', '2008-2012', '2013-2017']
    post_cohorts = ['2018-2022', '2023-2025']
    for c in pre_cohorts:
        pre.update(stats[c]['classes'])
    for c in post_cohorts:
        post.update(stats[c]['classes'])
    out = []
    for name, n_pre in pre.items():
        if n_pre < 20: continue
        n_post = post.get(name, 0)
        retain = n_post / n_pre if n_pre else 0
        if retain <= 0.10:
            out.append((retain, n_pre, n_post, name))
    out.sort()
    return out


def top_cited_per_phylum(papers, top=1):
    by_phy = defaultdict(list)
    for p in papers:
        by_phy[p['phylum']].append(p)
    out = {}
    for phy, ps in by_phy.items():
        ps.sort(key=lambda x: -(x.get('citations') or 0))
        out[phy] = ps[:top]
    return out


# --------------------------------------------------------------------
#                          Beamer template
# --------------------------------------------------------------------

PREAMBLE = r"""
\documentclass[aspectratio=169,t]{beamer}
\usepackage{kotex}              % Korean — works under XeLaTeX/LuaLaTeX
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{booktabs}
\usepackage{array}

% --- Theme: minimal, Material-ish ---
\usetheme{default}
\useinnertheme{rectangles}
\useoutertheme{infolines}
\setbeamercolor{structure}{fg=blue!60!black}
\setbeamerfont{frametitle}{size=\large,series=\bfseries}
\setbeamertemplate{navigation symbols}{}
\setbeamercolor{title}{fg=blue!50!black}
\setbeamercolor{frametitle}{fg=blue!50!black}
\setbeamercolor{itemize item}{fg=blue!50!black}
\setbeamercolor{section in head/foot}{bg=blue!10,fg=blue!50!black}

% Highlight macros
\definecolor{accentorange}{HTML}{ff7043}
\definecolor{accentblue}{HTML}{1a73e8}
\definecolor{mutedgray}{HTML}{5f6368}
\newcommand{\hot}[1]{\textcolor{accentorange}{\textbf{#1}}}
\newcommand{\cool}[1]{\textcolor{accentblue}{\textbf{#1}}}
\newcommand{\muted}[1]{\textcolor{mutedgray}{#1}}

\title[Robotics 30년]{Robotics 30년의 흐름}
\subtitle{4-depth Phylogenetic Taxonomy로 본 paradigm shift}
\author[Phylogeny]{Robotics Paper Phylogeny project}
\institute[7{,}477 papers]{T-RO · IJRR · RSS, 7,477 papers (1988--2025)}
\date{\today}

\begin{document}

\frame{\titlepage}

% =====================================================================
\section{왜 이걸 보는가}
% =====================================================================

\begin{frame}{왜 이런 분류가 필요한가}
\begin{itemize}
  \item Robotics는 30년+ 동안 패러다임이 빠르게 바뀐 분야.
  \item 같은 주제도 논문마다 표현이 다름 \\
        \muted{(예: ``laser place recognition'' $\approx$ ``point cloud loop detection'')}
  \item 단순 keyword/TF-IDF는 \hot{표현은 다른데 같은 의미}인 클러스터를 못 잡음.
  \item $\Rightarrow$ \cool{Semantic synonym cluster + 4-depth phylogenetic tree}
\end{itemize}
\vfill
\begin{block}{이 슬라이드의 목표}
8개의 5년 cohort로 잘라서, 각 시기의 \hot{paradigm signature}와
\hot{rank 변화}를 한눈에 보기. Taxonomy 자체가 시간의 흐름을 검증해 준다.
\end{block}
\end{frame}

\begin{frame}{데이터셋}
\begin{itemize}
  \item \cool{T-RO} 3{,}435 + \cool{IJRR} 2{,}666 + \cool{RSS} 1{,}488 + 보강 = \hot{7{,}477편}
  \item 1988 -- 2025 (37년)
  \item RoboPaper Atlas (DBLP + OpenAlex) 기반
  \item 모든 논문이 4-depth 분류됨 (Phylum/Class/Order는 100\%)
\end{itemize}
\vfill
\begin{block}{4-depth taxonomy}
\begin{tabular}{@{}lll@{}}
\textbf{L1} \textbf{Phylum} & 13   & 큰 분야 (Manipulation, Locomotion, SLAM \dots) \\
\textbf{L2} \textbf{Class}  & $\sim$100  & 분야 안의 갈래 (Grasping, Legged \dots) \\
\textbf{L3} \textbf{Order}  & $\sim$330  & 세부 주제 (Grasp Planning \dots) \\
\textbf{L4} \textbf{Genus}  & 가변 & 구체적 접근법 (Learning-based Grasping \dots) \\
\end{tabular}
\end{block}
\end{frame}

\begin{frame}{왜 ``생물 계통도''인가}
\begin{itemize}
  \item Linnaean taxonomy는 \hot{진화 계통(공통 조상)}을 표현하는 트리
  \item 로봇 분야도 비슷 — 같은 ``조상'' 문제에서 분기 \\
        \muted{(SLAM $\to$ Visual SLAM $\to$ VIO $\to$ LIO $\to$ 3D-Gaussian-Splatting SLAM)}
  \item 단계별 분기를 따라가면 \cool{paradigm 전환의 시점}이 자연스럽게 드러남
  \item 학술적 가치 + 학생 교육자료로 적합
\end{itemize}
\end{frame}

\begin{frame}{Methodology: semantic synonym cluster}
\begin{itemize}
  \item 단순 키워드 매칭 / TF-IDF의 한계 — 동의어를 못 잡음.
  \item 우리는 \hot{rule-based + manual semantic cluster}로 명시적 분류:
\end{itemize}
\vfill
\begin{block}{예: Place Recognition}
\small
\texttt{LIDAR = ['lidar', 'laser scan', 'point cloud', '3d point', 'range scan', \dots]} \\
\texttt{PLACE\_RECOG = ['place recognition', 'loop closure',} \\
\texttt{\quad\quad'loop detection', 'global localization', 'vpr', \dots]}\\[6pt]
\texttt{if has\_any(t, PLACE\_RECOG):} \\
\texttt{\quad if has\_any(t, LIDAR):} \\
\texttt{\quad\quad return ('SLAM \& Localization', 'Place Recognition', 'LiDAR-based')}
\end{block}
\vfill
\muted{$\Rightarrow$ ``laser place recognition'', ``point cloud loop detection'', ``lidar VPR''
같은 표현이 \cool{모두} 같은 leaf로 묶임.}
\end{frame}

\begin{frame}{Methodology: 우선순위 + Specific-first}
\begin{itemize}
  \item 규칙은 specific $\to$ general 순. Cross-cutting 케이스를 명시적으로 처리.
  \item Phylum/Class/Order는 100\% 라벨링.
  \item Genus는 specific rule 매칭 시 (약 \hot{52\%}) — 나머지는 \texttt{(general)}.
  \item 미분류 (Unclassified) 2.9\% — 너무 specific하거나 catchall에 안 걸린 케이스. 사용자가 직접 검토 가능.
\end{itemize}
\vfill
\begin{block}{왜 Sentence Transformer/LLM 안 썼나}
\small
\begin{itemize}
\item \cool{재현성} — rule 기반은 입력 동일하면 출력 동일.
\item \cool{투명성} — 어떤 rule이 매칭되었는지 추적 가능.
\item \cool{도메인 지식 인코딩} — robotics 표현 변천을 사람이 직접 큐레이션.
\end{itemize}
\end{block}
\end{frame}

% =====================================================================
\section{전체 분포}
% =====================================================================
"""

DISTRIBUTION_FRAME = r"""
\begin{frame}{전체 흐름: 1988-2025 누적}
\begin{itemize}
  \item 1988-1992 cohort: \cool{166편/5년} — 거의 T-RO + IJRR만
  \item 2003-2007: \hot{951편/5년} (5.7$\times$ 성장) — RSS 출범 + 자동화 데이터 수집
  \item 2008-2012: \hot{1{,}308편} — 학회 vs 학술지 균형 변화
  \item 2018-2022: \hot{1{,}547편}
  \item 2023-2025 (3년치): 이미 \hot{1{,}581편} — annualised로 환산하면 \cool{$\sim$2{,}630편/5년}
\end{itemize}
\vfill
\begin{block}{관찰}
\small Robotics 출판량은 30년에 걸쳐 거의 \hot{15$\times$ 증가}. \\
가속은 비선형 — 2023+ cohort에서만 \cool{이전 5년 대비 +70\%} (Foundation Models 효과).
\end{block}
\end{frame}

\begin{frame}{Phylum 분포 (전체 7{,}477편)}
\centering\small
\begin{tabular}{@{}lrr@{}}
\toprule
\textbf{Phylum} & \textbf{N} & \textbf{\%} \\
\midrule
Manipulation                     & 934 & 12.5\% \\
Locomotion                       & 842 & 11.3\% \\
Planning                         & 835 & 11.2\% \\
SLAM \& Localization             & 670 &  9.0\% \\
Robot Design \& Hardware         & 623 &  8.3\% \\
Perception \& Sensing            & 554 &  7.4\% \\
Theoretical Foundations          & 491 &  6.6\% \\
Control                          & 441 &  5.9\% \\
Multi-Robot Systems              & 408 &  5.5\% \\
Application Domains              & 396 &  5.3\% \\
Human-Robot Interaction          & 395 &  5.3\% \\
Learning for Robotics            & 354 &  4.7\% \\
Robot Software \& Architecture   &  30 &  0.4\% \\
\midrule
Editorial / Unclassified         & 504 &  6.7\% \\
\bottomrule
\end{tabular}
\vfill
\muted{상위 6개 Phylum이 전체의 60\%를 차지. Learning for Robotics는 비중은 4.7\%지만 최근 5년 성장률 \hot{+95.6\%}로 압도.}
\end{frame}
"""


def make_cohort_overview_frame(stats):
    rows = []
    for lo, hi in COHORTS:
        c = f'{lo}-{hi}'
        rows.append(f'  {c} & {stats[c]["total"]:,} \\\\')
    body = '\n'.join(rows)
    return r"""
\begin{frame}{8 cohorts × 5년 — 전체 카운트}
\centering
\begin{tabular}{@{}lr@{}}
\toprule
\textbf{Cohort} & \textbf{Papers} \\
\midrule
""" + body + r"""
\bottomrule
\end{tabular}
\vfill
\muted{2003 이후 paper count가 가파르게 상승 — T-RO/IJRR 통합 + RSS 출범 + 자동화된 데이터 수집의 결과.}
\end{frame}
"""


def make_cohort_frame(stats, cohort_label_str):
    title_kr, narrative = COHORT_HEADLINES[cohort_label_str]
    cohort = stats[cohort_label_str]
    top_classes = cohort['classes'].most_common(5)
    top_phyla = cohort['phyla'].most_common(3)

    # Truncate long Class names for the 2-column layout
    def short(name, n=34):
        return name if len(name) <= n else name[:n-1] + '…'

    cls_rows = '\n'.join(
        f'    {i+1}. & {latex_escape(short(name))} & {n} \\\\'
        for i, (name, n) in enumerate(top_classes))
    phy_rows = ', '.join(f'{latex_escape(n)} ({v})' for n, v in top_phyla)

    # Emerging
    cohort_idx = next(i for i, (lo, hi) in enumerate(COHORTS)
                      if f'{lo}-{hi}' == cohort_label_str)
    prev = f'{COHORTS[cohort_idx-1][0]}-{COHORTS[cohort_idx-1][1]}' if cohort_idx > 0 else None
    movers = emerging_classes(stats, cohort_label_str, prev) if prev else []
    if movers:
        mover_rows = '\n'.join(
            f'    \\hot{{$+${d}}} \\#{r}: '
            f'{latex_escape(short(name, 30))} ({v}) \\\\'
            for d, name, r, v in movers)
        emerging_block = r"""\textbf{급부상 (rank $\uparrow$ vs 직전 cohort)}\\[2pt]
\scriptsize
\begin{tabular}{@{}p{0.95\linewidth}@{}}
""" + mover_rows + r"""
\end{tabular}"""
    else:
        emerging_block = r'\muted{\small (첫 cohort — rank 비교 대상 없음)}'

    return r"""
\begin{frame}{""" + cohort_label_str + r' \quad — \quad ' + latex_escape(title_kr) + r"""}
\small
\begin{block}{Headline}
""" + narrative + r"""
\end{block}
\vspace{4pt}

\begin{columns}[T,onlytextwidth]
\begin{column}{0.52\textwidth}
\textbf{Top-5 Classes} \muted{\scriptsize (""" + f"{cohort['total']:,}" + r""" papers)}\\[2pt]
\scriptsize
\begin{tabular}{@{}rlr@{}}
""" + cls_rows + r"""
\end{tabular}
\vspace{8pt}

\textbf{\small Top-3 Phyla}\\[2pt]
\scriptsize """ + phy_rows + r"""
\end{column}

\begin{column}{0.48\textwidth}
""" + emerging_block + r"""
\end{column}
\end{columns}
\end{frame}
"""


def make_paradigm_shifts_frame():
    return r"""
\section{Paradigm shifts close-up}

\begin{frame}{Cohort 사이의 ``rank race''}
\small
\begin{tabular}{@{}lrrrrrrrr@{}}
\toprule
\textbf{Class} & \textbf{88-92} & \textbf{93-97} & \textbf{98-02} & \textbf{03-07} & \textbf{08-12} & \textbf{13-17} & \textbf{18-22} & \textbf{23-25} \\
\midrule
Path/Motion Planning  & 3 & 2 & 2 & 3 & \cool{1} & \cool{1} & \cool{1} & \cool{1} \\
Mechanism Design      & — & — & 1 & 2 & 7 & 12 & 14 & 12 \\
Legged Locomotion     & — & — & — & \cool{1} & 2 & 2 & 4 & 5 \\
SLAM                  & — & — & — & 9 & 7 & 6 & 5 & \hot{2} \\
Foundation Models     & — & — & — & — & — & 34 & — & \hot{3} \\
RL                    & — & — & — & — & 43 & 24 & \hot{12} & 11 \\
Grasping              & — & — & — & 12 & 9 & 8 & 7 & 8 \\
\bottomrule
\end{tabular}
\vfill
\muted{셀의 숫자는 해당 cohort 내 \emph{Class rank} (1 = 최다). ``--'' = 5편 미만으로 노이즈 처리.}\\
\hot{Foundation Models의 \#34 $\to$ \#3 점프}, \cool{SLAM의 꾸준한 상승}이 한눈에.
\end{frame}

\begin{frame}{2023-2025: Foundation Models의 등장}
\begin{itemize}
  \item 2022년까지 Foundation Models for Robotics는 Learning for Robotics Phylum 안에서 sub-rank.
  \item 2023-2025 cohort에서 \hot{+52 ranks $\to$ \#3} (66 papers).
  \item 동시기 등장 추가 paradigm shift:
  \begin{itemize}
    \item Diffusion Policy (2023 첫 논문 $\to$ 누적 19편)
    \item Vision-Language-Action (VLA) (2023 등장 $\to$ 누적 16편)
    \item 3D Gaussian Splatting SLAM (2024 등장 $\to$ 8편)
    \item Hierarchical / Flow Matching policies, Sim-to-Real Legged 표준화
  \end{itemize}
  \item 결론: \cool{2023년 한 해가 modern robot learning의 분기점}.
\end{itemize}
\end{frame}

\begin{frame}{2003-2007: SLAM 혁명}
\begin{itemize}
  \item 1998-2002 cohort: SLAM은 \#50+ 부근.
  \item 2003-2007: \hot{+43 ranks $\to$ \#9} (34 papers).
  \item 트리거: \cool{FastSLAM (2002)} $\to$ \cool{GraphSLAM/SAM (2006)} $\to$ \cool{EKF-SLAM 표준화}.
  \item Aerial Locomotion (+28 ranks) 동시 등장 — 드론 등장의 시발점.
  \item 의료 로봇 (+30 ranks) 본격화 — DaVinci 임상 채택 시기.
\end{itemize}
\end{frame}

\begin{frame}{2008-2012: Learning의 첫 임계점 통과}
\begin{itemize}
  \item RL이 \hot{+80 ranks} (이전엔 거의 없었음) $\to$ 8 papers
  \item Datasets \& Benchmarks (+77 ranks) 첫 등장
  \item Deep Learning Application (+74 ranks) 첫 등장
  \item Tactile Sensing (+27 ranks) — sensor fusion 시대의 신호
  \item \muted{이 cohort가 ``learning이 robotics로 들어오기 시작한 순간''로 기록될 것.}
\end{itemize}
\end{frame}

\begin{frame}{2018-2022: Sim-to-Real RL 정착}
\begin{itemize}
  \item RL이 +17 ranks $\to$ \#12 (38편) — 더 이상 niche가 아님.
  \item Sim-to-Real Legged Locomotion: 2018 첫 등장 $\to$ 2021-2025 누적 18편 \\
        \muted{단 4년만에 표준 패러다임화.}
  \item Tactile Sensing 고점 (\#17) — multi-modal perception이 끝까지 살아남는 영역.
  \item Reachability Analysis, Robot Safety 부상 — \cool{learning이 deployment 가까워질 수록 safety가 따라온다}.
\end{itemize}
\end{frame}

\begin{frame}{2013-2017: TAMP + Physical HRI + Foundation 씨앗}
\begin{itemize}
  \item Physical HRI \hot{+38 ranks $\to$ \#15} (32편). 협동로봇 (Cobot)의 등장 시기.
  \item Task \& Motion Planning (TAMP): \hot{+71 ranks} — symbolic + geometric의 결합.
  \item \cool{Foundation Models의 첫 미세한 등장 (12편)}. 5년 후 폭발의 ``ancestor''.
  \item Multi-Robot Planning (+33 ranks) — multi-agent decision making이 분리된 시기.
\end{itemize}
\end{frame}

\begin{frame}{사라진 분야 (cohort wall로 본 surface 검증)}
\begin{itemize}
  \item \hot{Visual Servoing} \\
        Pre-2015: 50편 $\to$ Post-2020: 4편 (잔존 8\%)\\
        \muted{학습 기반 제어 / end-to-end 정책에 흡수됨.}
  \item \hot{Computational Biology Robotics} \\
        Pre-2015: 28편 $\to$ Post-2020: 0편 (완전 소멸)\\
        \muted{IJRR 특집호 다수 → 2015 이후 별개 venue로 이동.}
  \item Taxonomy validation: \cool{한 분야가 실제로 ``죽었음''을 데이터로 확인}하는 능력은 phylogenetic 관점의 핵심 가치.
\end{itemize}
\end{frame}
"""


def make_validation_frames():
    return r"""
\section{Taxonomy Validation}

\begin{frame}{Citation 정규화 — ``인기'' vs ``영향력''}
\centering\small
\begin{tabular}{@{}lrrr@{}}
\toprule
\textbf{Phylum} & \textbf{Mean cites} & \textbf{Median} & \textbf{$\times$ overall} \\
\midrule
SLAM \& Localization      & 85.6 & 42 & \cool{$\times$1.26} \\
Locomotion                & 85.0 & 37 & \cool{$\times$1.26} \\
Robot Design \& Hardware  & 83.3 & 36 & \cool{$\times$1.23} \\
Human-Robot Interaction   & 77.0 & 35 & $\times$1.14 \\
\dots                      & \dots & \dots & \dots \\
Perception \& Sensing     & 59.1 & 26 & $\times$0.87 \\
Learning for Robotics     & 47.5 &  9 & \hot{$\times$0.70} \\
Theoretical Foundations   & 44.8 & 21 & \hot{$\times$0.66} \\
\bottomrule
\end{tabular}
\vfill
\begin{itemize}\small
\item Learning for Robotics는 \hot{인기 폭발했지만 평균 인용 낮음} — 대부분이 너무 최근 (median 9).
\item ``인기 분야 $\ne$ 영향력 큰 분야'' — cohort 분석이 이 차이를 설명.
\end{itemize}
\end{frame}

\begin{frame}{학술지 별 색깔 (T-RO vs IJRR vs RSS)}
\small
\begin{tabular}{@{}llll@{}}
\toprule
\textbf{Venue} & \textbf{Top 1} & \textbf{Top 2} & \textbf{Top 3} \\
\midrule
\textbf{T-RO}  & Locomotion (12.7\%)         & Manipulation (11.6\%)        & Robot Design \& HW (11.4\%) \\
\textbf{IJRR}  & Manipulation (13.9\%)       & Planning (11.9\%)            & Locomotion (11.5\%) \\
\textbf{RSS}   & Planning (14.1\%)           & \hot{Learning (13.1\%)}      & Manipulation (12.0\%) \\
\bottomrule
\end{tabular}
\vfill
\begin{itemize}
\item RSS의 Learning 비중은 \hot{다른 저널의 약 3배} — RSS가 modern AI 시대의 hub.
\item T-RO는 hardware/design, IJRR은 알고리즘 정형 — 분류가 venue의 정체성을 잘 잡아냄.
\item \cool{Cohort × Venue}로 더 잘게 보면 RSS의 Learning 비중이 어느 cohort에 폭발했는지도 추적 가능.
\end{itemize}
\end{frame}

\begin{frame}{교육적 활용}
\begin{itemize}
  \item \cool{학생 진입 시}: 13 Phylum overview $\to$ 관심 Phylum의 cohort wall $\to$ 그 안의 paradigm shift를 따라가는 \hot{독서 path}
  \item \cool{문헌 조사 시}: Cohort의 ``첫 논문 + dominant paper''를 자동 추천 가능 (이미 viewer에서 DOI 링크로 연결)
  \item \cool{커리큘럼 설계 시}: 2023+ cohort의 ``꼭 읽어야 할 5편''을 분야별로 추출 — phylogeny가 가지치기를 알려줌
  \item \cool{투자/PI 의사결정}: Faded vs emerging Class의 비대칭 — 어디에 시간을 쓸 것인가
\end{itemize}
\end{frame}

\begin{frame}{Live Tools}
\begin{itemize}
  \item Site: \url{https://gisbi-kim.github.io/robotics-paper-phylogeny/}
  \item 인터랙티브 viewer 두 가지:
  \begin{itemize}
    \item \cool{Radial Tree} — pie chart, 검색 + 추천 chip + DOI modal
    \item \cool{Horizontal Collapsible Tree} — 좌-우 phylogenetic 형태
  \end{itemize}
  \item URL state share: 특정 wedge 클릭 $\to$ \texttt{\#tab=tree\&node=...} URL 복사로 그 상태 공유
  \item KR/EN 토글: 우상단 appbar
  \item 데이터 refresh: \texttt{refresh\_from\_atlas.py} (RoboPaper Atlas snapshot에서 citation/DOI 동기화)
\end{itemize}
\end{frame}

\begin{frame}{Limitations}
\begin{itemize}
  \item \cool{단일 라벨}: 한 논문 = 한 카테고리. 멀티-필드 논문은 가장 specific한 곳으로 압축됨.
  \item \cool{제목만 사용}: Abstract 미포함 → 제목이 모호하면 분류 정확도 저하 (Editorial / Unclassified 6.7\%).
  \item \cool{3개 저널 한정}: ICRA/IROS/RA-L 미포함 — 학회 우선의 분야는 과소 표현될 수 있음.
  \item \cool{Citation 시간 효과}: 최근 cohort는 누적 인용 시간 부족 — 영향력 비교는 절대값보다 \hot{cohort-내 정규화}로 봐야 함.
\end{itemize}
\end{frame}

\begin{frame}{워크 예제: Manipulation의 30년}
\small
\begin{tabular}{@{}lll@{}}
\toprule
\textbf{Cohort} & \textbf{Top Manipulation Class} & \textbf{대표 방법론} \\
\midrule
1988-1992 & General Manipulation       & 직접 inverse kinematics, force control \\
1993-1997 & General Manipulation       & Force/Impedance control 표준화 \\
1998-2002 & Mechanism Design           & Underactuated/dexterous hand 디자인 \\
2003-2007 & Grasping (force-closure)   & Grasping wrench-space analysis \\
2008-2012 & Grasping (data-driven)     & ``Grasping novel objects'' (Saxena, 2008) \\
2013-2017 & Contact-rich Manipulation  & Tactile-driven planning, RL 시도 \\
2018-2022 & Contact-rich Manipulation  & \cool{Diffusion / IL이 force-closure를 추월} \\
2023-2025 & Contact-rich + Deformable  & \hot{VLA, Diffusion Policy, dexterous LLM-driven} \\
\bottomrule
\end{tabular}
\vfill
\muted{한 Phylum 안에서도 Class 단위로 paradigm shift가 4-5번 일어남 — phylogeny가 그 가지치기를 추적한다.}
\end{frame}

\begin{frame}{워크 예제: SLAM \& Localization의 30년}
\small
\begin{tabular}{@{}ll@{}}
\toprule
\textbf{Cohort} & \textbf{State of the art} \\
\midrule
1988-1997 & 거의 없음. Occupancy grid mapping의 초기 토대. \\
1998-2002 & Probabilistic robotics 정형화 (Thrun et al.). \\
2003-2007 & \cool{FastSLAM, GraphSLAM}. SLAM이 main-stage로 (\#9). \\
2008-2012 & \cool{Visual SLAM}, EKF/iSAM/sliding-window 표준. \\
2013-2017 & \cool{Visual-Inertial Odometry (VIO)}, ORB-SLAM 시리즈. \\
2018-2022 & \cool{LiDAR-Inertial Odometry (LIO)}, multi-modal fusion. \\
2023-2025 & \hot{3D Gaussian Splatting SLAM}, neural rendering 결합. \\
\bottomrule
\end{tabular}
\vfill
\muted{SLAM은 cohort마다 ``modality 추가'' 패턴 — 단순 → 시각 → IMU 추가 → LiDAR 추가 → neural geometry. Phylogenetic tree로 자연스럽게 표현됨.}
\end{frame}

\begin{frame}{Future Work}
\begin{itemize}
  \item \cool{Cohort × Phylum heatmap}: 각 cohort의 phylum signature를 한 행으로
  \item \cool{Class-level alluvial}: 인접 cohort 간 rank 흐름을 Sankey로 시각화
  \item \cool{Author network 결합}: 누가 어떤 paradigm shift를 끌고 왔는가
  \item \cool{Abstract 추가}: 분류 정확도 향상 + Genus 단계 sub-rule 확장
  \item \cool{ICRA/IROS 통합}: 7,477 $\to$ 80k+ 규모로 확장 (atlas에 이미 있음)
\end{itemize}
\end{frame}

\begin{frame}{한 줄 요약}
\Large\centering
\vfill
\cool{Robotics 30년}은 \\[6pt]
\hot{SLAM (2003-07)} $\to$ \hot{Learning seeds (2008-12)} $\to$ \hot{Sim-to-Real (2018-22)} $\to$ \hot{Foundation Models (2023+)}\\[6pt]
\muted{4번의 분기점으로 정리된다.}
\vfill
\end{frame}

\begin{frame}{Q\&A}
\Huge\centering
?
\vfill
\normalsize
\url{https://gisbi-kim.github.io/robotics-paper-phylogeny/}
\end{frame}

\end{document}
"""


# --------------------------------------------------------------------
def main():
    papers = load()
    stats = compute_cohort_stats(papers)

    chunks = [PREAMBLE.lstrip()]
    chunks.append(DISTRIBUTION_FRAME)
    chunks.append(make_cohort_overview_frame(stats))

    chunks.append(r'\section{Cohort Wall — 5년 단위로 본 paradigm}' + '\n')
    for lo, hi in COHORTS:
        chunks.append(make_cohort_frame(stats, f'{lo}-{hi}'))

    chunks.append(make_paradigm_shifts_frame())
    chunks.append(make_validation_frames())

    OUT_TEX.parent.mkdir(parents=True, exist_ok=True)
    OUT_TEX.write_text('\n'.join(chunks))
    print(f'Wrote {OUT_TEX.relative_to(ROOT)} ({sum(len(c) for c in chunks):,} chars)')


if __name__ == '__main__':
    main()
