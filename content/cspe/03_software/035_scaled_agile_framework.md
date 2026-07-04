---
title: "SAFe 대규모 애자일 프레임워크 (Scaled Agile Framework)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 35
---

# 📖 【암기용】 개념 완전 이해

> 목적: SAFe를 처음 보는 사람도 팀 애자일과 대규모 조직 조율 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다. 이 문서는 SAFe의 포트폴리오 계층·거버넌스 관점에 초점을 둔다(ART/PI 실행 메커니즘은 035_safe 참고).

## 한눈에
- **개요**: SAFe(Scaled Agile Framework)는 여러 애자일 팀을 **포트폴리오-프로그램-팀 3개 계층**으로 정렬하는 **대규모 애자일 확장 프레임워크**이며, 이 문서는 그중 전략·예산을 다루는 **포트폴리오 계층(Lean Portfolio Management)**과 거버넌스 관점에 초점을 둔다.
- **왜 필요한가**: 팀 계층에서 스프린트를 잘 돌려도, 그 위에서 "이 기능에 예산을 얼마나 쓸지, 어느 ART에 우선 투입할지"를 정하는 상위 의사결정이 없으면 팀들은 각자 국지적으로만 최적화된다(Local Optima). SAFe는 이 상위 의사결정을 린 예산(Lean Budget)과 WSJF로 수치화한다.
- **핵심 직관**: 여러 공장(팀)이 부품을 잘 만들어도, 본사(포트폴리오)가 "이번 분기엔 엔진 공장에 예산을 더 준다"는 배분을 하지 않으면 전체 생산 계획이 어긋난다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| Lean-Agile | 린 제조 원칙(낭비 제거)과 애자일 원칙(반복·피드백)을 결합한 SAFe의 기반 철학 | SAFe 전체가 딛고 선 두 다리 |
| Portfolio 계층 | 전략·투자 테마·예산을 결정하는 최상위 계층 | 본사 경영진 |
| Program 계층(ART) | 여러 팀을 묶어 8~12주 PI 목표를 실행하는 계층 | 지역 공장 |
| Team 계층 | 개별 스크럼/칸반 팀이 스프린트를 수행하는 실행 계층 | 공장 내 작업 라인 |
| LPM(Lean Portfolio Management) | 전략-예산-실행을 연결하는 포트폴리오 관리 체계 | 본사의 예산 편성·집행 관리 부서 |
| 예산 가드레일(Budget Guardrail) | 각 가치 흐름(Value Stream)에 배정된 예산 상한·하한 | 부서별 지출 한도 |
| WSJF(Weighted Shortest Job First) | 비즈니스 가치를 소요 기간으로 나눠 우선순위를 매기는 계산식 | 같은 시간에 더 큰 가치를 주는 일부터 처리 |
| 가치 흐름(Value Stream) | 아이디어에서 고객 가치 전달까지 이어지는 전체 작업 경로 | 원자재부터 완성품 출고까지의 생산 라인 |
| Architecture Runway | 향후 기능 개발에 필요한 인프라·기술 기반을 미리 준비해 두는 것 | 착륙할 기능들을 위해 미리 닦아 둔 활주로 |
| System Demo / Inspect & Adapt | PI 종료 시 통합 결과를 시연하고 프로세스를 점검·개선하는 활동 | 분기별 전사 시연회와 반성회 |

## 깊이 이해

### 왜 포트폴리오 계층이 필요한가 — 국지적 최적화 문제
- 8개 스크럼 팀이 각자 자기 백로그 기준으로 "가장 급해 보이는" 기능을 골라 작업하면, 회사 전체로 봤을 때 정작 매출에 가장 큰 영향을 주는 기능은 뒤로 밀릴 수 있다. 이것이 국지적 최적화(Local Optima) 문제다. 포트폴리오 계층은 전사 전략 테마를 정하고, 그 테마에 맞춰 각 ART(프로그램 계층)에 예산을 배분해 이 어긋남을 막는다.

### WSJF로 우선순위를 정하는 원리 — 수치 예제
- WSJF = (사용자·비즈니스 가치 + 시급성 + 리스크 감소/기회 가능성) ÷ 작업 규모(Job Size). 세 요소와 작업 규모는 각각 피보나치 수열(1, 2, 3, 5, 8, 13, 20)로 상대 추정한다.
- 예: 기능 A는 (가치 8 + 시급성 5 + 리스크감소 3) ÷ 규모 5 = 3.2점. 기능 B는 (가치 5 + 시급성 3 + 리스크감소 2) ÷ 규모 2 = 5.0점. B가 A보다 개별 가치 항목 합은 작지만, 작업 규모가 더 작아 WSJF 점수는 더 높게 나온다. 이 점수가 높은 항목부터 포트폴리오 백로그 상단에 배치한다.
- 핵심은 "가치가 크다고 무조건 먼저"가 아니라 "같은 작업량 대비 더 큰 가치를 주는 일"을 먼저 한다는 점이다.

### 예산 가드레일과 거버넌스가 작동하는 방식
- 포트폴리오는 연 단위 예산을 한 번에 확정하지 않고, 가치 흐름별로 상한선(Budget Guardrail)만 정한 뒤 실제 집행은 PI 단위(8~12주)로 나눠 검토한다. 예: 결제 가치 흐름에 연 100억 원 가드레일을 설정하고, 실제 투입은 PI(분기)마다 성과를 보며 증감한다.
- 이렇게 하면 폭포수처럼 연초에 예산을 확정해 1년을 버티는 대신, PI마다 우선순위가 바뀐 기능에 예산을 재배분할 수 있다.

### Architecture Runway가 병목을 막는 원리
- 특정 기능(예: 실시간 추천)을 만들려면 그 전에 이벤트 스트리밍 인프라가 있어야 한다. 이 인프라를 기능 개발 시점에 급하게 만들면 PI 내내 지연된다. Architecture Runway는 이런 공통 기반을 앞선 PI에서 미리 준비해 두어, 실제 기능 개발 PI에서는 바로 그 위에 기능을 얹기만 하면 되게 만든다.

### 판별 원리 — SAFe 도입 범위를 언제 넓히는가
- 팀 수 5개 미만이고 예산 흐름이 단순하면 포트폴리오 계층 없이 Essential SAFe(035_safe 참고)만으로 충분하다.
- 팀 수가 늘고 여러 가치 흐름에 예산을 나눠야 하면 LPM(포트폴리오 계층)을 얹는다.
- 규제 산업(금융·의료)처럼 컴플라이언스 증적이 필요하면 Portfolio/Full SAFe의 governance 요소(architecture runway, compliance evidence)까지 확장한다.

### 흔한 오해
- SAFe의 포트폴리오 계층은 "예산을 한 번에 몰아주는" 폭포수식 연간 예산 편성이 아니다. 가드레일만 정하고 실제 배분은 PI 단위로 반복 조정한다는 점이 폭포수 예산과의 핵심 차이다.
- LPM 도입 자체가 목적이 아니다. 팀 수가 적은 조직이 포트폴리오 계층부터 도입하면 회의와 산출물만 늘고 실질적 조정 효과는 적다 — 팀 계층과 프로그램 계층(ART/PI)이 먼저 안정된 뒤 확장하는 것이 순서다.

## 연결 개념
- SAFe ART/PI 실행 메커니즘(035_safe): 이 문서가 다루는 포트폴리오 계층 아래, 실제 팀을 정렬하는 실행 계층
- 애자일 스크럼(034): LPM이 예산을 배분하는 최종 실행 단위
- DORA 지표/Value Stream Management: PI 목표 달성 이후 배포 빈도·리드타임까지 수치로 관리하는 확장 개념

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: SAFe 답안은 프레임워크 구성 암기가 아니라 대규모 팀 의존성, 예산, 릴리스 거버넌스를 지표로 조정하는 관점이 필요하다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SAFe는 portfolio, program, team 계층으로 다수 애자일 팀을 하나의 가치 흐름에 정렬하는 프레임워크이다.
> 2. **가치**: ART와 PI Planning으로 팀 간 의존성, 통합 일정, 아키텍처 기준, 예산 집행을 같은 cadence에서 조정한다.
> 3. **판단 포인트**: 팀 수, 의존성 개수, 규제 거버넌스, 통합 릴리스 빈도에 따라 SAFe 도입 범위와 경량화 수준을 결정한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 대규모 애자일 조정 구조 확인 | portfolio/program/team, ART, PI Planning, system demo | Scrum 용어만 확대해 설명 |
| 거버넌스와 자율성 균형 판단 | Lean-Agile, LPM, architecture runway, dependency board | 회의와 산출물 나열로 끝냄 |
| 도입 리스크 인식 확인 | 중앙집중화, PI 계획 과부하, 대규모 조정 비용 | SAFe를 조직 문제 해결책으로 단정 |

> 요약: SAFe 문제는 대규모 팀 조율 필요성과 과도한 프로세스 리스크를 함께 평가하는 답안을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 대규모 애자일 조정 프레임워크
- 배경: 여러 팀이 동일 제품군을 개발하면 팀 간 의존성, 통합 순서, 예산 배정, 릴리스 일정이 충돌해 단일 Scrum만으로 조정하기 어려움.
- 필요성: ART, PI Planning, System Demo로 8~12주 단위 목표와 의존성을 정렬하고 feature 완료율, dependency risk, release predictability를 관리해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Strategy -> Lean Portfolio Management -> Value Stream -> ART
         -> PI Planning -> Team Sprint -> System Demo -> Inspect and Adapt
         +-> Architecture Runway / Governance / Metrics
```

| 구성요소 | 역할 | 산출물·지표 |
|:---|:---|:---|
| Portfolio | 전략·투자·가치 흐름 관리 | portfolio backlog, budget guardrail |
| ART | 50~125명 규모 전달 조직 | PI objective, program board |
| Team | Scrum/Kanban 실행 단위 | sprint backlog, team increment |
| Governance | 아키텍처·품질·규제 통제 | architecture runway, compliance evidence |

> 요약: SAFe는 전략 예산부터 팀 sprint까지 ART cadence와 PI 목표로 연결한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Portfolio Epic -> Feature Breakdown -> PI Planning
-> Dependency Mapping -> Sprint Execution -> System Demo
-> Inspect and Adapt -> Portfolio Feedback
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | portfolio epic과 budget guardrail 설정 | WSJF, value stream budget |
| 2 | feature를 ART backlog로 분해 | feature readiness 90% 이상 |
| 3 | PI Planning에서 목표·의존성 조정 | dependency resolved rate 80% 이상 |
| 4 | 팀별 sprint와 통합 demo 수행 | PI objective 달성률 80% 이상 |
| 5 | Inspect and Adapt로 개선 항목 반영 | improvement backlog 완료율 |

> 요약: SAFe는 포트폴리오 전략을 feature와 PI objective로 분해하고 system demo로 통합 결과를 검증한다.

---

## Ⅳ. 특징

| 구분 | 팀 단위 Agile | SAFe | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 규모 | 5~9명 Scrum team | ART 50~125명 | 팀 5개 이상, 의존성 20개 이상 |
| 계획 | sprint planning | PI Planning 8~12주 | PI objective 달성률 80% 이상 |
| 거버넌스 | 팀 자율 중심 | portfolio budget, architecture runway | compliance evidence 추적 |
| 통합 | 팀별 demo | system demo, release train | integration defect trend |

> 요약: SAFe는 팀 민첩성보다 대규모 의존성 공개, 통합 검증, 예산 정렬에 초점을 둔다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | Scrum of Scrums | SAFe | 선택 기준 |
|:---|:---|:---|:---|
| 조정 범위 | 팀 간 실행 이슈 | 포트폴리오-프로그램-팀 정렬 | 예산·전략까지 연결 필요 시 SAFe |
| 릴리스 | 팀별 release | ART cadence 기반 release | 통합 릴리스 2개월 단위 |
| 관리 비용 | 회의 경량 | PI Planning, LPM 운영 | 조정 비용 대비 dependency 감소 |

> 요약: SAFe는 단순 팀 조정보다 포트폴리오 예산과 통합 릴리스가 함께 필요한 조직에 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 프로세스 과부하 | SAFe 이벤트 과다 | essential SAFe부터 단계 도입 | 회의 시간 비율 15% 이하 |
| 중앙집중화 | ART·portfolio 의사결정 집중 | team autonomy guardrail | team decision lead time |
| 의존성 잔존 | architecture runway 부족 | dependency board, enabler story | unresolved dependency count |

> 요약: SAFe 도입 리스크는 경량 도입, 팀 자율성 기준, 의존성 지표로 관리해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| PI 성과 | PI objective 달성률 80% 이상 | PI score, business value |
| 통합 품질 | integration defect PI당 감소 추세 | system demo defect log |
| 흐름 | feature lead time 30% 단축 | value stream mapping |

> 요약: SAFe 성과는 PI 목표, 통합 결함, feature lead time으로 측정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. Essential SAFe부터 적용해 1개 ART, 8~12주 PI, program board, system demo를 먼저 운영
2. Portfolio backlog에 WSJF, budget guardrail, compliance evidence를 연결해 전략-예산-개발 추적성 확보
3. Dependency board, architecture runway, integration test pipeline으로 unresolved dependency와 통합 결함을 PI마다 점검

**결론 (2줄):**
- 기술사 판단: 팀 5개 이상, 공통 릴리스와 예산 정렬이 필요하면 SAFe, 단일 제품팀이면 Scrum/Kanban을 선택함
- 향후 방향: SAFe는 Value Stream Management와 DORA 지표를 결합해 대규모 조직의 납기·품질·운영 흐름을 수치로 관리함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "SAFe를 설명하시오" | portfolio-program-team 흐름과 PI Planning | ART, LPM, governance 특징 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "리스크를 논하시오" | 의존성 조정·통합 흐름 | 프로세스 과부하, 중앙집중화 대응 |

> 요약: 설명형은 계층 구조, 방안형은 ART 도입 순서와 대규모 조정 리스크 통제를 중심으로 작성한다.
