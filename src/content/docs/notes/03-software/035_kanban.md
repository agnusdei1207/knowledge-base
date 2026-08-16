---
sidebar:
  order: 35
  label: "035. 칸반 (Kanban)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "칸반 (Kanban)"
date: "2026-08-13T14:31:00+09:00"
tags:
  - "notes-software"
weight: 35
extra:
  question_no: "035"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "칸반은 흐름 제한•리드타임 개선 기법"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Kanban System**: 토요타(Toyota)의 JIT(Just-In-Time) 생산방식에서 유래되어, 작업의 시각화(Visualization), WIP(Work-In-Progress) 한도 제한, 그리고 연속적인 당김(Pull) 메커니즘을 통해 리드타임(Lead Time)을 최적화하는 애자일 워크플로우 관리 기법.
- **WIP (Work In Progress)**: 현재 착수되었으나 아직 최종 완료(Done)되지 않은 채 작업 보드 상의 각 상태 단계에 체류하고 있는 작업들의 수량.
- **Pull System**: 하류(Downstream) 단계의 WIP 여유 수용량이 발생할 때만 상류(Upstream) 단계에서 작업을 당겨와(Pull) 과부하 및 병목을 방지하는 시스템.

</details>

- 정의/개념: 작업을 시각화하고 각 공정 단계별 **WIP Limit**를 부여하여 작업 정체를 차단하고 연속적 가치 흐름(Flow)을 최적화하는 **칸반**
- 배경/필요성: 무제한 착수는 **대기열•멀티태스킹•리드타임 변동** 증가

#### 한줄 요약

- WIP 한도와 당김 시스템으로 과다 착수와 대기 누적을 방지한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Little's Law (리틀의 법칙)**: 안정된 시스템 상태에서 평균 리드타임(Lead Time)은 진행 중인 작업 수(WIP)에 비례하고 처리율(Throughput)에 반비례한다는 수학적 법칙 ($\text{Lead Time} = \frac{\text{WIP}}{\text{Throughput}}$).
- **Cumulative Flow Diagram (CFD)**: 시간 경과에 따른 각 공정 단계별 작업 카드 축적 상태를 누적 영역 차트로 표현하여 병목(Bottleneck) 및 리드타임을 한눈에 시각화하는 도구.

</details>

![리틀의 법칙에 따른 WIP와 평균 리드타임 관계](/study/diagrams/little-law-wip-lead-time.svg)

> 처리율을 하루 2건으로 고정한 파란 선은 WIP가 10건이면 평균 리드타임이 5일이 되는 리틀의 법칙 예시이며, 안정적인 유입•처리율을 가정한다.

- **WIP Limit**를 통한 리드타임 최적화 (**Little's Law** 기반)
- 타임박스(Sprint)가 없는 **Continuous Flow (연속적 가치 흐름)**
- **CFD (Cumulative Flow Diagram)** 및 **Lead Time / Cycle Time** 중심 성과 측정

#### 한줄 요약

- 완료 우선, 연속 흐름, 점진적 진화, 리틀의 법칙의 결합이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Kanban Board**: To Do, In Progress, Testing, Done 등의 상태 컬럼(Column)으로 나누어 작업 카드(Card)의 위치와 WIP 한도를 명시하는 시각화 보드.

</details>

```text
                   [작업 카드]
                        |
[흐름 정책] ----- [워크플로 열] ----- [흐름 지표]
```

선의 의미: Kanban Board 상의 각 상태 컬럼에 WIP Limit 정책이 설정되고, 작업 카드가 Left-to-Right로 이동하며 흐름 지표가 측정되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| 작업 카드 | 가치 항목과 상태•노화시간 표현 |
| 워크플로 열 | 작업 단계와 진입•완료 조건 시각화 |
| 흐름 정책 | **WIP Limit•Pull**과 서비스 클래스 정의 |
| 흐름 지표 | Lead Time•Cycle Time•Throughput 측정 |

#### 한줄 요약

- 작업 카드, 워크플로, 흐름 정책, 흐름 지표가 보드에 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Expedite Lane (긴급 패스트트랙)**: 장애 조치 등 초급송 긴급 작업 처리를 위해 WIP Limit 1로 별도 지정되어 타 일반 작업을 제치고 우선 처리되는 전용 라인.

</details>

```text
┌──────────────────────────────┐
│ 상위 백로그 (Backlog)       │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 수용량•WIP 확인          │
│ 2. 당김 허용 판정 (Pull)    │
│ 3. 우선순위 카드 선택        │
│ 4. 카드 이동•작업 수행       │
│ 5. 완료•흐름 지표 갱신       │
└──────────────────────────────┘
```

### 동작 원리

1. **수용량·WIP 확인**: 하류 공정 컬럼의 현재 작업 수와 설정된 **WIP Limit** 비교.
2. **당김 허용 판정 **: 하류 컬럼의 현재 작업 수가 WIP Limit 미만일 때만 상류에서 카드 당김(Pull) 승인.
3. **우선순위 카드 선택**: **Expedite Lane** 우선 처리 및 일반 큐에서 우선순위 상위 카드 선택.
4. **카드 이동·작업 수행**: 공정 정책(Policy) 준수 하에 작업을 수행하고 해당 컬럼 완료 처리.
5. **완료·흐름 지표 갱신**: 최종 Done 상태 도출 및 **Lead Time / Cycle Time** 지표 모니터링 수집.

#### 한줄 요약

- 수용량•WIP 확인과 당김 허용 판정에 따른 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Lead Time vs Cycle Time**: Lead Time은 고객 요구 접수 시점부터 최종 전달 시점까지의 총 시간, Cycle Time은 작업 착수(In Progress)부터 완료 시점까지의 실제 작업 소요 시간.

</details>

| 비교 항목 | Kanban (칸반) | Scrum (스크럼) |
|:---|:---|:---|
| 기본 단위 | **지속적 흐름 ** | 한 달 이하 고정 스프린트 |
| 요구사항 변경 | 용량이 생길 때 우선순위대로 당김 | 스프린트 목표를 지키며 범위 협상 |
| 핵심 제어 장치 | **WIP Limit (작업 수 제한)** | Timeboxing (시간 제한) |
| 팀 구조 | 현재 역할에서 시작해 점진 개선 가능 | PO•SM•Developers 책무 정의 |
| 핵심 성과 지표 | **Lead Time, Cycle Time, Throughput, CFD** | Velocity (Story Point) |

#### 한줄 요약

- 불규칙 서비스 흐름은 칸반, 시간 상자는 스크럼이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **WIP Limit Violations**: 긴급 작업 폭주로 WIP Limit가 상시 무력화되어 보드가 마비되는 파행 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| WIP Limit를 무시하고 카드를 계속 밀어넣음 (Push) | **Pull 메커니즘 강제** 및 WIP 초과 시 경고 표시 | 병목 방지 및 리드타임 준수 |
| 특정 공정 컬럼에 카드가 오랜 기간 상주하여 고사 (**Work Item Aging**) | **Daily Kanban**에서 Aging 카드 전면 점검 및 Swarming(다인 투입) 인가 | 병목 현상 즉시 해소 |
| 긴급 패스트트랙(**Expedite Lane**) 남용 | Expedite Lane 카드 수를 strict하게 1개로 제한 | 일반 작업의 기아 예방 |

> 사례: 운영 유지보수 및 장애 조치가 수시 발생하는 **ITSM / DevOps 운영팀**의 Kanban 적용

#### 한줄 요약

- 사이클타임, 작업 노화, SLE로 흐름 정책을 조정한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **칸반 도입 선택 기준(Kanban Adoption Criteria)**: 요구사항 유입의 불규칙성, 운영 유지보수성 성격 및 기존 조직 체계 유지 요구에 따른 선택 체계.

</details>

- **칸반 도입 선택 기준**에 따라 예측 불가능한 24x7 운영/유지보수 조직에는 **Kanban System + WIP Limit** 구축

#### 한줄 요약

- 불규칙 유입과 시간 상자 목표를 함께 평가하는 것이 핵심이다.
