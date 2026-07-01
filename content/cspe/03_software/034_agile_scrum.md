---
title: "애자일 스크럼 (Agile Scrum)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 34
---

# 📖 【암기용】 개념 완전 이해

> 목적: Scrum을 처음 보는 사람도 역할, 이벤트, 산출물을 연결해 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: Scrum은 1~4주 sprint로 제품 증분을 반복 제공하는 애자일 프레임워크
- **왜 필요한가**: 요구사항이 계속 변하는 제품 개발에서는 큰 계획을 한 번에 확정하기 어렵다. Scrum은 backlog 우선순위와 sprint 목표로 작은 범위를 자주 검증한다.
- **핵심 직관**: 긴 항해 계획보다 2주 단위 항로 점검을 반복해 목적지와 실제 바람을 맞추는 방식이다.

## 깊이 이해
- **배경·문제의식**: 전통적 개발은 고객이 완성품을 늦게 확인해 요구사항 오해가 후반에 드러난다. Scrum은 sprint review에서 작동 제품을 보여주고, retrospective에서 팀 작업 방식을 조정한다.
- **작동 원리**: Product Owner는 가치 기준으로 product backlog를 정렬한다. Scrum Master는 방해 요인을 제거하고 Scrum 이벤트를 촉진한다. Developers는 sprint backlog를 구현해 Done 상태의 increment를 만든다.
- **비유**: 식당 신메뉴를 6개월 뒤 한 번에 내는 것이 아니라, 2주마다 시식회를 열어 재료와 조리법을 바꾸는 방식이다.
- **구체 예시**: 2주 sprint에서 40 story point를 계획하고 34 point를 완료했다면 velocity는 34이다. 다음 sprint 계획은 최근 3회 평균 velocity 32~36 범위로 잡아 납기 예측을 보정한다.
- **흔한 오해·주의점**: Daily Scrum은 보고 회의가 아니라 sprint goal 달성을 위한 15분 조정 회의이다. PO 부재, 불명확한 DoD, 과도한 scope change는 Scrum 실패 원인이다.

## 연결 개념
- Product Backlog: 가치 기준으로 정렬된 요구사항 목록
- Sprint Review: 완료 증분을 이해관계자와 검증하는 이벤트
- Velocity: 팀의 반복 처리량 추정 지표

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Scrum 답안은 이벤트 암기가 아니라 backlog 우선순위, 역할 책임, sprint 지표로 요구사항 변동을 통제하는 구조를 보여야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Scrum은 PO, Scrum Master, Developers가 sprint 단위로 product increment를 만드는 애자일 프레임워크이다.
> 2. **가치**: backlog 정렬, sprint review, retrospective로 고객 피드백과 팀 개선을 반복 반영한다.
> 3. **판단 포인트**: velocity, burndown, defect leakage, sprint goal 달성률로 납기·품질·범위 통제를 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Scrum 구성요소 이해 확인 | PO, Scrum Master, Developers, backlog, sprint, increment | 애자일 가치 선언만 서술 |
| 반복 개발 통제 역량 확인 | sprint planning, daily scrum, review, retrospective | daily scrum을 상급자 보고로 설명 |
| 지표 기반 운영 판단 확인 | velocity, burndown, sprint predictability, DoD | 속도 향상만 강조하고 품질 지표 누락 |

> 요약: Scrum 문제는 역할·이벤트·산출물을 지표와 연결해 요구사항 변동을 통제하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: Sprint 기반 애자일 프레임워크
- 배경: 제품 개발은 요구사항 변경과 우선순위 변동이 반복되어, 장기 계획만으로는 고객 피드백과 개발 산출물의 차이를 조기에 발견하기 어려움.
- 필요성: Product Backlog, Sprint Review, Retrospective로 1~4주 단위 증분을 검증하고 velocity, burn-down, defect leakage를 추적해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Product Vision -> Product Backlog -> Sprint Planning -> Sprint Backlog
               -> Daily Scrum -> Increment -> Review -> Retrospective
Roles: PO / Scrum Master / Developers
```

| 구성요소 | 역할 | 산출물·지표 |
|:---|:---|:---|
| Product Owner | 가치·우선순위 결정 | product backlog, release goal |
| Scrum Master | Scrum 실행 촉진, impediment 제거 | impediment log, event adherence |
| Developers | 설계·구현·테스트 수행 | sprint backlog, increment |
| Scrum Events | 계획·동기화·검토·개선 | velocity, burndown, retro action |

> 요약: Scrum은 역할 책임과 이벤트 주기를 분리해 backlog를 완료 증분으로 전환한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Backlog Refinement -> Sprint Planning -> Sprint Execution
-> Daily Coordination -> Review Feedback -> Retrospective Action
-> Backlog Reprioritization
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | product backlog 정제 | user story, acceptance criteria 충족 |
| 2 | sprint goal과 sprint backlog 확정 | capacity 대비 계획량 80~90% |
| 3 | 개발·테스트·daily scrum 수행 | burndown 이탈 20% 이하 |
| 4 | increment review와 피드백 수집 | DoD 충족, 이해관계자 승인 |
| 5 | retrospective 개선 항목 실행 | retro action 완료율 80% 이상 |

> 요약: Scrum은 계획-실행-검토-개선 루프를 sprint마다 반복하고 backlog 우선순위를 다시 조정한다.

---

## Ⅳ. 특징

| 구분 | 전통적 프로젝트 관리 | Scrum | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 범위 관리 | 초기 범위 기준선 | product backlog 우선순위 | sprint scope change 10% 이하 |
| 일정 예측 | WBS milestone | velocity, release burndown | 최근 3회 평균 velocity |
| 품질 기준 | 테스트 단계 집중 | DoD와 자동 테스트 | DoD 위반 0건 |
| 고객 피드백 | 주요 단계 승인 | sprint review 반복 | review 참석률 80% 이상 |

> 요약: Scrum은 범위 고정보다 우선순위 조정과 완료 기준 준수로 납기와 품질을 관리한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | Scrum 미적용 | Scrum 적용 | 선택 기준 |
|:---|:---|:---|:---|
| 요구사항 | 요청 순서대로 구현 | value 기반 backlog 정렬 | 기능 우선순위 변동이 월 2회 이상 |
| 조직 | 기능별 분업 | cross-functional team | 팀 규모 5~9명 권장 |
| 릴리스 | 대형 배포 | sprint increment 누적 | 2~4주 피드백 주기 필요 |

> 요약: Scrum은 작은 제품팀, 잦은 피드백, 명확한 PO 권한이 있을 때 적용 효과를 검증할 수 있다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| PO 병목 | 의사결정 지연 | backlog refinement 정례화, 위임 기준 | story ready rate 90% 이상 |
| 품질 저하 | DoD 미준수 | 자동 테스트, code review, CI gate | defect leakage 2% 이하 |
| 형식적 이벤트 | 회의 목적 불명확 | timebox, agenda, retro action 추적 | event timebox 준수율 |

> 요약: Scrum 리스크는 역할 공백, DoD 위반, 이벤트 형식화에서 발생하므로 준비율과 품질 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 납기 예측 | sprint predictability 80% 이상 | planned vs completed story point |
| 흐름 | cycle time 5일 이하 | Jira control chart |
| 품질 | 회귀 테스트 통과율 95% 이상 | CI test report, defect trend |

> 요약: Scrum 성과는 velocity 단독이 아니라 예측 가능성, 흐름 시간, 품질 지표를 함께 봐야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Product backlog에 value, risk, effort, dependency 필드를 두고 WSJF 또는 MoSCoW로 sprint 후보를 정렬
2. Sprint 2주, daily scrum 15분, review 2시간, retrospective 1시간 timebox를 적용하고 DoD에 자동 테스트 통과 포함
3. Velocity, sprint predictability, defect leakage, cycle time을 dashboard로 운영해 scope creep과 품질 저하를 조기 식별

**결론 (2줄):**
- 기술사 판단: 요구사항 탐색형 제품은 Scrum, 규제 산출물 고정 프로젝트는 Scrum+stage gate 혼합을 선택함
- 향후 방향: Scrum은 DevOps, DORA, SAFe와 결합되어 팀 단위 반복을 조직 단위 가치 흐름 관리로 확장함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Scrum을 설명하시오" | 역할·이벤트·산출물 흐름 | backlog, sprint, review 특징 |
| 요구사항 명시형 | "운영 방안을 제시하시오", "문제점을 논하시오" | velocity·DoD·scope change 통제 | PO 병목, 품질 저하, 이벤트 형식화 대응 |

> 요약: 설명형은 Scrum 구성요소, 운영형은 지표와 리스크 대응 중심으로 답안 목차를 전환한다.
