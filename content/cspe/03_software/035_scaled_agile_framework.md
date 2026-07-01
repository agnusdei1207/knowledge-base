---
title: "SAFe 대규모 애자일 프레임워크 (Scaled Agile Framework)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 35
---

# 📖 【암기용】 개념 완전 이해

> 목적: SAFe를 처음 보는 사람도 팀 애자일과 대규모 조직 조율 차이를 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: SAFe는 여러 애자일 팀을 포트폴리오·프로그램·팀 계층으로 정렬하는 대규모 애자일 프레임워크
- **왜 필요한가**: Scrum 한 팀은 5~9명 규모에서 동작하지만, 수십 개 팀이 한 제품군을 만들면 의존성, 예산, 릴리스 일정, 아키텍처 기준이 충돌한다. SAFe는 이를 ART와 PI Planning으로 조정한다.
- **핵심 직관**: 작은 밴드 여러 팀이 각자 연주하지 않도록 지휘자, 악보, 합주 일정, 공연 목표를 맞추는 방식이다.

## 깊이 이해
- **배경·문제의식**: 대기업은 제품, 플랫폼, 규제, 운영 조직이 분리되어 팀별 sprint만으로는 end-to-end 가치 전달이 어렵다. SAFe는 Lean-Agile 원칙, portfolio funding, Agile Release Train(ART), PI Planning을 통해 팀 간 의존성을 공개적으로 조정한다.
- **작동 원리**: Portfolio 수준은 전략과 투자 테마를 정한다. Program 수준은 ART가 8~12주 Program Increment 목표를 세운다. Team 수준은 Scrum/Kanban으로 sprint를 수행한다. System Demo와 Inspect & Adapt로 통합 결과를 검증한다.
- **비유**: 여러 공장이 같은 자동차를 만들 때 차체, 엔진, 전장 팀이 2개월 생산 계획과 부품 의존성을 한 회의에서 맞추는 구조이다.
- **구체 예시**: 8개 팀, 80명이 참여하는 ART가 10주 PI에서 12개 feature를 계획하고 dependency board로 30개 의존성을 식별하면, 통합 지연 리스크를 PI 초반에 조정 가능함.
- **흔한 오해·주의점**: SAFe는 Scrum을 크게 만든 이름이 아니다. 포트폴리오 예산, 아키텍처 runway, governance까지 다루므로 과도한 회의와 중앙집중화 리스크를 함께 관리해야 한다.

## 연결 개념
- ART: Agile Release Train, 여러 팀이 같은 cadence로 움직이는 전달 조직
- PI Planning: 8~12주 단위 목표·의존성·리스크 조정 이벤트
- Lean Portfolio Management: 전략, 예산, 가치 흐름을 연결하는 관리 체계

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

SAFe는 대규모 애자일 조정 프레임워크이다.
여러 팀이 동일 제품군을 개발하면 의존성, 통합, 예산, 릴리스 일정이 충돌한다.
SAFe는 ART와 PI Planning으로 가치 흐름과 팀 실행을 연결해 대규모 협업 리스크를 줄임.

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

| 비교 축 | Scrum of Scrums | SAFe | 선택 기준 |
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
