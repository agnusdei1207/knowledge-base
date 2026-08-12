---
sidebar:
  order: 32
  label: "032. 애자일 스크럼 (Agile Scrum)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "애자일 스크럼 (Agile Scrum)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 32
extra:
  question_no: "032"
  source_status: "기출"
  source_history: "134회"
  priority: 50
  priority_note: "134회 기출, 책무•이벤트•산출물 구조"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Scrum Framework**: 1~4주 간격의 고정된 타임박스인 스프린트(Sprint) 동안, 3대 역할(PO, SM, Dev Team), 5대 이벤트, 3대 아티팩트를 기반으로 복잡한 제품을 반복 개발하는 대표적인 애자일 실행 프레임워크.
- **Empiricism (경험주의 3대 기둥)**: 투명성(Transparency), 점검(Inspection), 적응(Adaptation)에 기반하여 실제 작동 결과를 관찰하고 피드백을 수용하는 스크럼의 철학적 기반.
- **Increment (제품 증분)**: 매 스프린트마다 완성되어 배포 및 즉시 사용 가능한 상태의 품질 합격 제품 기능의 합.

</details>

- 정의/개념: 경험주의(Empiricism) 및 자율관리 팀을 기반으로 매 타임박스(Sprint)마다 배포 가능한 제품 증분을 만들어 내는 대표적 경량 애자일 프레임워크인 **애자일 스크럼(Agile Scrum)**
- 배경/필요성: 예측 불가능한 시장 환경 속에서 고정된 장기 계획의 위험 극복, 고객 가치 조기 전달 및 점진적 품질 향상 요구성

#### 한줄 요약

- 짧은 스프린트와 제품 증분을 통한 경험주의가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Timeboxing (타임박싱)**: 스프린트(1~4주), 일일 스크럼(15분), 리뷰(2~4시간) 등 모든 이벤트의 최대 허용 시간을 고정하여 불필요한 공수를 차단하는 통제 기법.
- **Self-Managing / Cross-Functional Team**: 스스로 일을 선택하고 추진하는 자율관리성(Self-managing)과 개발/테스트/기획 기능이 한 팀에 통합된 교차기능성(Cross-functional).

</details>

- 3대 경험주의 기둥 (**Transparency, Inspection, Adaptation**)
- 3-5-3 스크럼 구조 (**3대 역할, 5대 이벤트, 3대 아티팩트**)
- 고정 타임박스(**Timeboxing**) 및 **Self-Managing Cross-Functional Team** 구동

#### 한줄 요약

- 투명성, 점검, 적응으로 제품과 팀의 효과성을 개선한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **3대 역할 (Accountabilities)**: Product Owner (PO, 비즈니스 가치 및 백로그 총괄), Scrum Master (SM, 프로세스코칭 및 장애물 제거), Developers (개발팀, 제품 증분 직접 제작).
- **3대 산출물 (Artifacts)**: Product Backlog (전체 요구사항), Sprint Backlog (스프린트 개발 목표/할일), Increment (완성된 증분).
- **5대 이벤트 (Events)**: Sprint, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective.

</details>

```text
[제품 책임자] -- [제품•스프린트 백로그] -- [개발자] -- [제품 증분]
                                          |
                                   [스크럼 마스터]
```

선의 의미: PO가 Product Backlog를 정렬하고, 개발팀이 Sprint Backlog를 완성하여 Increment를 도출하며, SM이 스크럼 프로세스와 장애물을 코칭 관리하는 구조.

| 분 류 | 스크럼 구성요소 (3-5-3) | 핵심 역할 및 정의 |
|:---|:---|:---|
| **3대 역할** | **Product Owner (PO)** | 제품 가치 극대화, Product Backlog 관리 및 우선순위 최종 결정 |
| | **Scrum Master (SM)** | 스크럼 정착 지원, 서번트 리더십(Servant Leadership), 장애물(Impediment) 제거 |
| | **Developers (개발자)** | 스프린트 내에서 배포 가능한 Increment를 직접 설계/구현/테스트 |
| **3대 산출물** | **Product Backlog** | 제품에 필요한 모든 요구사항을 우선순위 순으로 정렬한 단일 목록 |
| | **Sprint Backlog** | 이번 스프린트에 달성할 Sprint Goal 및 선택된 PBI/Task 목록 |
| | **Increment** | Definition of Done(DoD)을 충족하여 사용 가능한 완성된 제품 결과물 |
| **5대 이벤트** | **Sprint / Planning** | 전체 타임박스 / 스프린트 목표 수립 및 Sprint Backlog 도출 |
| | **Daily / Review / Retro**| 매일 15분 점검 / 시연 및 고객 피드백 수용 / 팀 프로세스 회고 및 개선 |

#### 한줄 요약

- 제품 책임자, 스크럼 마스터, 제품 백로그, 스프린트 백로그, 완료의 정의가 역할과 산출물을 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Definition of Done (DoD)**: Increment가 최종 완성되었음을 인증하는 공통 품질 기준 (Unit Test 100% Pass, Code Review, Docu, CI Build 성공 등).

</details>

```text
┌──────────────────────────────┐
│ 제품 백로그                │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 스프린트 계획 (Planning) │
│ 2. 스프린트 실행 (Daily)   │
│ 3. 완료 검증 (DoD)         │
│ 4. 스프린트 리뷰 (Review)   │
│ 5. 스프린트 회고 (Retro)   │
└──────────────────────────────┘
```

### 동작 원리

1. **Sprint Planning**: PO와 개발팀이 Product Backlog에서 우선순위 항목 선택 및 **Sprint Goal** 정의.
2. **Sprint Execution & Daily Scrum**: 1~4주 간 구동하며 매일 15분 **Daily Scrum**을 통해 진행 장애물(Impediment) 도출 및 공유.
3. **DoD Verification**: 개발 완료 건에 대해 **Definition of Done(DoD)** 기준 충족 여부 검증.
4. **Sprint Review**: 이해관계자 및 PO 대상 제품 시연(Demo) 및 피드백 수용 (Product Backlog 재정렬).
5. **Sprint Retrospective**: 프로세스/소통/도구 관점의 회고 수행 및 다음 스프린트 개선 과제(1개 이상) 도출.

#### 한줄 요약

- 스프린트 계획부터 스프린트 회고까지의 순환이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Velocity (소멸 속도/추진력)**: 한 스프린트 동안 개발팀이 완료(DoD) 처리할 수 있는 Story Point의 합산 평균 수치.

</details>

| 비교 항목 | Scrum (스크럼) | Kanban (칸반) |
|:---|:---|:---|
| 핵심 단위 | **타임박스 (1~4주 고정 Sprint)** | **지속적 흐름 (Continuous Flow)** |
| 자원 캡슐화 | 스프린트 내 백로그 변경 및 신규 투입 원칙적 금지 | 언제든 WIP(Work In Progress) 한도 내 신규 투입 가능 |
| 핵심 메트릭 | **Velocity (스토리 포인트 기반 속도)** | **Cycle Time / Lead Time (처리 소요시간)** |
| 롤 정의 | PO, SM, Developer 3대 역할 필수 정의 | 명확한 전용 롤 정의 없음 (기존 롤 수용) |

#### 한줄 요약

- 변화•제품 피드백은 스크럼, 승인 통제는 전통 방식이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Water-Scrum-Fall**: 명목상은 Scrum을 표방하나, 실제로는 요구/계획은 Waterfall, 개발만 짧게 쪼개고, 테스트/배포는 다시 통째로 미루는 파행적 애자일 변종.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 일일 스크럼이 업무 보고 회의로 변질 | SM의 서번트 리더십 코칭 및 개발자 간 3대 질문 공유 위주 변경 | 자율관리 팀 문화 정착 |
| 형식적 스프린트 운영으로 후반부 통합 폭망 (**Water-Scrum-Fall**) | **DoD 기준 강화** 및 CI/CD 자동 테스트 결합 | 진정한 배포 가능 증분 확보 |
| PO의 권한 부재로 인한 백로그 결정을 타 본부장이 번복 | PO에게 제품 백로그 최종 결정 권한 완전 위임 | 의사결정 병목 소멸 |

> 사례: JIRA / Confluence 기반 **Agile Scrum 3-5-3** 운영 및 Burndown Chart 모니터링

#### 한줄 요약

- 품질 게이트, 리뷰 결정, 회고 행동의 실행성을 확보한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **스크럼 정착 성숙도 기준(Scrum Maturity Criteria)**: 3-5-3 프레임워크 준수율, DoD 엄격성, Velocity 안정성 및 팀 자율성에 기반한 수립 체계.

</details>

- **스크럼 정착 성숙도 기준**에 따라 성공적 애자일 조직 전환을 위해 **3-5-3 프레임워크 준수** 및 **DoD 자동화** 정착

#### 한줄 요약

- 목표•완료 기준 충족 여부를 함께 평가하는 것이 핵심이다.
