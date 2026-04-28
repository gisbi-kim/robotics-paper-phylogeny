# TAXONOMY 제안 노트 (Forward-looking Proposals)

> 외부 신호(세미나·논문·뉴스레터·산업계 발표)를 보다가 "이 결은 우리 계통도가 아직 못 잡는다"고 느낀 후보들을 모아두는 곳.
> 논문 수가 충분히 누적되면 정식으로 [TAXONOMY.md](TAXONOMY.md)에 반영하고, 그 시점의 변경 사유는 [TAXONOMY_CHANGES.md](TAXONOMY_CHANGES.md)에 옮긴다.

**현재 상태**: 검토 중 (아직 분류기에 반영 안 됨). 새 Genus를 만들기 전에 보통 T-RO/IJRR/RSS에서 **5편 이상** 누적되었는지 확인.

---

## 제안 P-001 — VLA Genus 결 세분화 (2026-04 기록)

### 발견 맥락

2026-06-17 한국미래기술교육연구원 세미나 *"VLA(Vision-Language-Action) 기반 Physical AI 개발과 상용화 전략"*. 7명의 연사가 모두 VLA를 다뤘는데, 강연을 우리 계통도에 매핑하니 **7/7이 동일한 Genus(`General VLA`)로 수렴**했다. 즉 우리 트리가 현재 VLA의 내부 분기를 못 잡는 상태.

현재 `Learning > Foundation Models > Vision-Language-Action (VLA)` 아래의 Genus는:
- General VLA
- Vision-Language Navigation
- π₀-family
- Octo / OpenVLA-family
- RT-series

### 누락된 결들 (세미나에서 드러난)

| 후보 Genus | 시그널이 된 강연 / 키워드 | 정식 기준 충족? |
|---|---|---|
| **On-device / Lightweight VLA** | 임화섭 (KIST, 온디바이스 가속), 김태호 (노타AI, 모델 경량화·최적화) | 검토 필요 — quantized VLA, distilled VLA 논문 수 |
| **Adaptive / Feedback-driven VLA** | 최종현 (서울대, 환경 피드백 기반 오류 수정·실시간 행동 적응) | 검토 필요 — closed-loop VLA, online VLA correction 논문 수 |
| **Hierarchical / System-1·System-2 VLA** | 김혜진 (ETRI, high-level reasoning vs low-level control 속도 불균형 = 정확히 system-2/system-1 위계 문제) | 검토 필요 — Helix, GR00T-N1 등 dual-system VLA 흐름 |
| **Multi-stage / Modular VLA** | 정지훈 (오일러로보틱스, 멀티스테이지 VLA 아키텍처) | 검토 필요 — pipeline VLA, agentic VLA |
| **Physical Skill Foundation (VLA보다 상위)** | 허영진 (뉴로메카, "Physical Skill Foundation: Sim-to-Real과 Foundation Model 기반 접근"). 이건 VLA의 한 결이 아니라 *VLA의 추상 위 단계* — 이미 우리 계통도에 `Generalist / Cross-embodiment Policies` Order가 있으니 거기 그대로 사용. 다만 명칭에 "Physical Skill Foundation"을 alias로 두는 것을 고려. | Order는 이미 존재 — 키워드 매칭 룰만 보강 |

### 제안

1. 위 4개 신규 Genus를 `Vision-Language-Action (VLA)` Order 아래 추가 후보로 등록.
2. **즉시 추가하지 않고**, 다음 분기 refresh 시점에 T-RO/IJRR/RSS/CoRL/RSS 워크숍 페이퍼에서 각 Genus당 5편 이상 매칭되는지 확인.
3. 충족되면 `genus_rules.py`에 키워드 클러스터를 정의:
   ```python
   ONDEVICE_VLA = ['quantized vla', 'distilled vla', 'lightweight vla', 'edge vla', 'on-device vla', 'efficient vla']
   HIERARCHICAL_VLA = ['system-1 system-2', 'dual-system vla', 'hierarchical vla', 'fast-slow vla']
   ADAPTIVE_VLA = ['feedback vla', 'closed-loop vla', 'online vla correction', 'reactive vla']
   MODULAR_VLA = ['multi-stage vla', 'modular vla', 'agentic vla', 'pipeline vla']
   ```

### 주의

- "VLA"라는 단어 자체가 2023년부터 등장한 신생 용어라, 2025-2026 사이에 internal taxonomy가 빠르게 바뀔 가능성이 높음.
- 너무 일찍 sub-Genus를 쪼개면 후속 논문 흐름과 안 맞을 수 있으니 6~12개월 관찰 후 결정.

---

## 제안 P-002 — (다음 후보 기록 위치)

> 새 외부 신호가 생기면 위 P-001 형식으로 추가.

---

## 제안 → 채택 절차

1. 본 문서에 후보 등록 (위 형식)
2. 분기별 refresh 시점에 누적 논문 수 확인 (≥ 5편 권장)
3. 채택되면:
   - `TAXONOMY.md`에 정식 반영
   - `TAXONOMY_CHANGES.md`에 변경 사유 + 기각 후보들도 함께 기록
   - `classify.py` / `genus_rules.py`에 키워드 룰 추가
   - `papers_classified.json` 재생성 → 다운스트림 전체 갱신 (참조: [MAINTENANCE.md](MAINTENANCE.md) 시나리오 C)
4. 본 문서에서 해당 제안 삭제 또는 "✅ 채택 (커밋 SHA)" 마크

---

*관련 문서: [TAXONOMY.md](TAXONOMY.md) (현행 트리) · [TAXONOMY_CHANGES.md](TAXONOMY_CHANGES.md) (적용된 변경 이력) · [TAXONOMY_EVALUATION.md](TAXONOMY_EVALUATION.md) (Springer Handbook 대비 자체평가) · [MAINTENANCE.md](MAINTENANCE.md) (스키마 변경 시 갱신 절차)*
