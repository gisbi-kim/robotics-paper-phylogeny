# 논문 컬렉션 계통도 구축 지침

> 어떤 분야의 논문 모음이든 **생물 계통도 구조(Phylum > Class > Order > Genus)**로 MECE하게 분류하는 분류기를 만들기 위한 범용 지침.
>
> 이 저장소([robotics-paper-phylogeny](https://github.com/gisbi-kim/robotics-paper-phylogeny))의 구축 과정을 역추론·종합해서 만들었다.

---

## 0. 원본 지침 (task.txt)

이 프로젝트는 단 한 문단짜리 프롬프트에서 시작했다:

> "역사적으로 로봇공학에 어떤 주제가 있었는지 최대한 많이 나열해서 엑셀로 줘. 단순히 단어를 분리해서 tf idf 하라는게 아니야. 시맨틱하게 너가 어텐션타서 잘 판단하란 얘기야 예를들어서 어떤 논문은 laser place recognition 이라고 할수도있고 어떤애는 point cloud based loop detection이라고도 할수있겠지만 이런 계열들은 다 place recognition으로 묶고 그 하위에 lidar-based 라는 계통도를 만들수있겠지. 아맞아 계통도까지 만들자 생물들 계통도처럼"

이 한 문단이 담고 있는 설계 원칙 세 가지:

| 원칙 | 표현 |
|------|------|
| 의미 기반 분류 | "시맨틱하게 너가 어텐션타서 잘 판단하란 얘기야" |
| 동의어 클러스터링 | "laser place recognition"과 "point cloud loop detection"을 같은 칸으로 |
| 생물 계통도 구조 | "생물들 계통도처럼" |

---

## 1. 입력 요건

| 항목 | 필수 | 비고 |
|------|------|------|
| 논문 제목 | ✅ | 최소 요건 |
| 발행 연도 | 권장 | 시대별 패러다임 추적에 필요 |
| 저널/학회명 | 권장 | 커뮤니티 성격 파악에 도움 |
| 초록 | 선택 | 있으면 정확도 향상, 없어도 작동 |

---

## 2. 계층 설계 원칙

### 2-1. 생물 계통도 메타포를 그대로 쓴다

```
Phylum  (문)   — 이 분야를 아는 사람이면 누구나 바로 납득하는 최상위 묶음
Class   (강)   — Phylum 안에서의 접근법/방법론 계열
Order   (목)   — 실제로 논문이 속하는 구체적 소주제
Genus   (속)   — 특정 기법·알고리즘·응용 수준의 세분화 (선택)
```

**Phylum 개수 기준**: 전체 논문 수의 3~15% 범위에 드는 묶음만 독립 Phylum으로. 나머지는 다른 Phylum의 Class로 흡수.

### 2-2. MECE 강제 방법

**Mutually Exclusive** — 규칙의 특이성 순서(specificity ordering)로 보장

```
더 구체적인 규칙이 앞에 온다. 먼저 매칭되면 이후 규칙은 무시.
예: "surgical robot" → Application 먼저 → Manipulation 나중
```

**Collectively Exhaustive** — 두 단계 안전망으로 보장

```
1차: Aggressive fallback rules (느슨한 키워드로 95% 이상 포획)
2차: Other/Unclassified catchall (나머지 전부 수용)
목표: Unclassified < 5%
```

---

## 3. 분류 방법론 원칙

### 3-1. TF-IDF 하지 말 것

단어 빈도 통계가 아니라 **의미적 동치(semantic equivalence)**로 판단한다.

같은 개념을 다르게 표현한 것들을 하나의 클러스터로 묶는다:

```python
# 나쁜 예: 단어 하나씩 매칭
if 'lidar' in title: ...
if 'point cloud' in title: ...  # 별도 처리

# 좋은 예: 의미 클러스터
LIDAR = ['lidar', 'laser scan', 'point cloud', 'range scan',
         'range image', '3d point', 'ladar', ...]
if has_any(title, LIDAR): ...  # 한 번에 처리
```

### 3-2. 동의어 클러스터 설계 방법

1. 논문 제목들을 쭉 읽으면서 **같은 개념의 다른 표현들**을 수집
2. 약어, 하이픈 변형, 구어적 표현까지 포함
3. 시대별 용어 변화 반영 (옛날 용어 → 새 용어)

```
예시: "place recognition" 클러스터
- 오래된 표현: loop closure, loop detection
- 현재 표현: place recognition, VPR (visual place recognition)
- 센서별:    lidar VPR, image retrieval
→ 전부 PLACE_RECOG 하나로
```

### 3-3. 우선순위 설계 원칙

```
1순위: Editorial/메타 논문 (분류 불필요)
2순위: 최신 패러다임 (LLM, Foundation Model 계열 등)
3순위: 이 분야의 강한 식별자 (분야 고유 핵심 개념)
4순위: 응용 분야 (일반 방법론보다 응용이 구체적이면 응용 우선)
5순위: 방법론 계열
마지막: Fallback / Unclassified
```

---

## 4. 구축 프로세스 (단계별)

### Step 1 — 데이터 파악

논문 제목을 **연도순**으로 훑으면서:
- 이 커뮤니티에서 반복적으로 나오는 핵심 개념 20~30개 파악
- 시대별 패러다임 전환 포착 (언제부터 새 용어가 등장하는가)
- 분량 감각 파악 (어느 주제가 많고 적은가)

### Step 2 — 초안 계통도 설계

Phylum 목록을 먼저 확정한다. 기준:
- 이 분야 전문가가 "당연히 별도 묶음"이라고 할 것들
- 서로 **접근법이 근본적으로 다른** 것들 (태스크 vs 방법론 vs 이론)
- 논문 수가 충분히 많을 것 (전체의 3% 이상 권장)

### Step 3 — 전체 통독 + 수정

초안을 들고 전체 논문 제목을 다시 읽으면서:
- 초안에서 **통째로 누락된 영역** 찾기
- 너무 작게 쪼갠 것 합치기
- 너무 크게 묶은 것 분리하기
- 변경 이유를 `TAXONOMY_CHANGES.md` 스타일로 메모

### Step 4 — 분류기 구현

```python
def classify(title):
    t = ' ' + title.lower() + ' '  # 소문자 + 공백 패딩

    # 1. Editorial/특수 케이스 먼저
    if is_editorial(t):
        return ('Editorial', ...)

    # 2. 강한 식별자 (이 분야 고유 핵심어)
    if has_any(t, STRONGEST_SIGNALS):
        ...

    # 3. 응용 분야 (방법론보다 구체적)
    if has_any(t, APPLICATION_KW):
        ...

    # 4. 방법론 계열
    if has_any(t, METHOD_KW):
        ...

    # N. Fallback
    return ('Other', 'Unclassified', 'Unclassified')
```

### Step 5 — 검증 및 보정

```
전체 분류 결과를 돌린 후 확인할 것:
□ Unclassified 비율이 5% 이하인가?
□ 가장 큰 Phylum이 전체의 20% 이하인가? (너무 크면 분리 고려)
□ 가장 작은 Phylum이 전체의 1% 이상인가? (너무 작으면 합치기 고려)
□ 시대별 분포가 말이 되는가? (옛날 논문이 최신 카테고리에 들어가면 이상)
```

---

## 5. 흔한 실수와 회피법

| 실수 | 증상 | 해결 |
|------|------|------|
| 너무 세분화 | Order가 500개 이상, 각 Order에 논문 1~2편 | 유사 Order 합치기 |
| 너무 통합 | Phylum 5개 이하, Phylum당 논문 2000편 이상 | 큰 Phylum 분리 |
| 용어 시대 편향 | 1990년대 논문이 모두 Unclassified | 오래된 표현을 클러스터에 추가 |
| 도메인 vs 방법론 혼재 | 의료 로봇이 Manipulation이기도, Application이기도 | 우선순위 규칙 명시: 도메인 > 방법론 |
| 폴리세미 | "control"이 제어이기도, 실험 통제이기도 | 공동 출현 키워드로 맥락 판단 (`has_all`) |

---

## 6. AI에게 줄 프롬프트 템플릿

```
다음은 [분야명] 분야의 논문 [N]편의 제목/연도/저널 목록이다.

이 논문들을 생물 계통도(Phylum > Class > Order) 구조로 MECE하게 분류해줘.

규칙:
1. 단순 TF-IDF 키워드 분리 말고, 같은 개념의 다른 표현들(동의어)을
   하나의 카테고리로 묶어서 시맨틱하게 판단해.
   예: "A 방식"과 "B 기법"이 같은 개념이면 같은 칸으로.

2. Phylum은 이 분야를 아는 사람이면 누구나 납득할 최상위 묶음.
   개수는 10~15개 내외.

3. 더 구체적인 것이 우선: 같은 논문이 여러 카테고리에 걸리면
   가장 specific한 카테고리로 배정.

4. 모든 논문이 어딘가에는 들어가야 함.
   Other/Unclassified 허용하되 전체의 5% 미만 목표.

5. 결과는 [원하는 출력 형식]으로 줘.
```

---

## 7. 핵심 한 줄 요약

> 구조(계통도)는 데이터를 읽은 후 **귀납적**으로 결정하고, MECE는 **규칙 순서**와 **catchall**로 기계적으로 강제한다.
