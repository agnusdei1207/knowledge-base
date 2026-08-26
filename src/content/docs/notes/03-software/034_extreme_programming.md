---
sidebar:
  order: 34
  label: "034. XP: 페어 프로그래밍•TDD"
  badge:
    text: "기출 · 50%"
    variant: note
title: "XP: 페어 프로그래밍•TDD (Extreme Programming)"
date: "2026-08-27T00:11:00+09:00"
tags:
  - "notes-software"
weight: 34
extra:
  question_no: "034"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "129회 기출, XP 실천법•피드백 주기"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **XP(eXtreme Programming)**: 소프트웨어 개발의 우수한 공학 실천법(TDD, 짝 프로그래밍, CI 등)을 극단(Extreme)까지 끌어올려 품질을 보증하는 애자일 방법론.
- **5대 핵심 가치**: 의사소통(Communication), 단순성(Simplicity), 피드백(Feedback), 용기(Courage), 존중(Respect).

</details>

- 정의/개념: 5대 가치 하에 **TDD, 짝 프로그래밍, 지속적 통합(CI), 리팩토링** 등 12대 공학 실천법을 집중 적용하는 소프트웨어 개발 방법론
- 배경/필요성: 개발 후반부 결함 발견 시 발생하는 **수정 비용의 기하급수적 폭증 및 요구사항 변경 수용 실패 해결 불가**

#### 한줄 요약
- TDD와 짝 프로그래밍 등 12대 공학 실천법을 통해 코드 품질과 변경 유연성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **TDD(Test-Driven Development)**: 구현 코드를 작성하기 전에 실패하는 단위 테스트를 먼저 작성하여 설계 결함을 사전에 방지하는 기법.
- **짝 프로그래밍(Pair Programming)**: 2명의 개발자가 단일 컴퓨터에서 드라이버(코딩)와 내비게이터(설계 검토) 역할을 번갈아 수행하는 실시간 코드 리뷰 기법.

</details>

- **Red-Green-Refactor** 사이클을 통한 결함 방지 및 강력한 테스트 자동화 안전망 구축
- **짝 프로그래밍(Pair Programming)** 및 **공동 코드 소유(Collective Ownership)** 로 지식 사일로 제거
- 잦은 **지속적 통합(CI)** 과 **지속적인 리팩토링**으로 기술 부채 누적 원천 차단

#### 한줄 요약
- TDD 안전망과 짝 프로그래밍의 실시간 교차 검증으로 무결점 코드를 생산한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **공동 코드 소유(Collective Code Ownership)**: 특정 코드의 소유권을 개인에게 두지 않고 팀원 누구나 언제든 리팩토링하고 개선할 수 있는 원칙.

</details>

```text
[XP(Extreme Programming) 4대 실천 영역 아키텍처]
|-- 개발 실천 영역 (Engineering Practices)
|   |-- TDD (Test-Driven Development: Red / Green / Refactor)
|   |-- 짝 프로그래밍 (Pair Programming: Driver & Navigator)
|   `-- 리팩토링 (Refactoring: 기능 보존 코드 개선)
|-- 통합 및 빌드 영역 (Integration Practices)
|   |-- 지속적 통합 (Continuous Integration: 하루 수십 회 자동 빌드/테스트)
|   `-- 공동 코드 소유 (Collective Ownership: 전원 수정 권한)
|-- 프로세스 및 관리 영역 (Management Practices)
|   |-- 계획 게임 (Planning Game: 사용자 스토리 기반 릴리즈 계획)
|   |-- 작은 릴리즈 (Small Releases: 1~2주 주기 배포)
|   `-- 주 40시간 작업 (Sustainable Pace: 팀 번아웃 방지)
`-- 고객 협업 영역 (Customer Practices: 상주 고객 - On-site Customer)
```

선의 의미: 계층 및 12대 세부 실천법 연계 구조

| 구성요소 | 책임 |
|:---|:---|
| 개발 실천 영역 | **TDD·짝 프로그래밍·리팩토링**으로 품질 확보 |
| 통합 및 빌드 영역 | **지속적 통합·공동 소유**로 변경 검증 |
| 프로세스 및 관리 영역 | 계획 게임·작은 릴리즈로 **지속 가능성** 확보 |
| 고객 협업 영역 | **상주 고객**으로 요구사항 모호성 해소 |

#### 한줄 요약
- 개발, 통합, 관리, 고객의 4대 실천 영역이 유기적으로 결합되어 품질을 견인한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Red-Green-Refactor**: 실패하는 테스트 작성(Red) $\to$ 최소 코드로 테스트 통과(Green) $\to$ 중복 제거 및 구조 개선(Refactor)의 3단계 TDD 루프.

</details>

```text
사용자 스토리(User Story) 분석 및 인수 조건 도출
        │
   [Red 단계] 실패하는 단위 테스트 코드 작성 (구현 전 테스트 실패 확인)
        │
   [Green 단계] 테스트를 통과하기 위한 최소한의 비즈니스 코드 작성 (테스트 성공)
        │
   [Refactor 단계] 짝 프로그래머와 함께 중복 제거, 클린 코드 리팩토링 (테스트 통과 유지)
        │
   로컬 커밋 후 CI 서버로 Push (자동 빌드 및 전체 회귀 테스트 통과)
        │
   작동하는 기능 증분 배포 및 다음 스토리 반복
```

#### 한줄 요약
- Red 실패 테스트 → Green 최소 구현 → Refactor 클린 코드 → CI 통합 배포 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **XP vs Scrum**: XP는 공학 실천법(TDD, CI) 중심이고, Scrum은 프로젝트 관리/역할(PO, SM) 중심이므로 상호 결합 시 시너지 극대화.

</details>

| 비교 항목 | 익스트림 프로그래밍 (XP) | 스크럼 (Scrum) | 칸반 (Kanban) |
|:---|:---|:---|:---|
| 핵심 집중 분야 | **코드 품질 및 엔지니어링 실천법** | 프로젝트 관리 및 팀 역할 | 워크플로우 시각화 및 흐름 최적화 |
| 반복 주기 | **1~2주 (매우 짧음)** | 2~4주 스프린트 | 타임박스 없음 (연속 흐름) |
| 테스트/엔지니어링 | **TDD, 짝 프로그래밍, CI 필수 규정** | 특정 개발 기법 강제 안 함 | 특정 개발 기법 강제 안 함 |
| 변경 수용성 | 이터레이션 중에도 스토리 교체 가능 | 스프린트 도중 목표 변경 원칙적 불가 | 언제든 우선순위 변경 가능 |

#### 한줄 요약
- 스크럼이 프로젝트 관리의 틀을 제공한다면, XP는 고품질 소프트웨어를 만드는 공학적 실천 기술이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **짝 피로도(Pair Fatigue)**: 하루 종일 짝 프로그래밍을 지속할 때 발생하는 개발자의 극심한 정신적 소모와 피로.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 지속적인 짝 프로그래밍으로 인한 **짝 피로도(Pair Fatigue)** | 복잡한 핵심 도메인 로직에만 2~3시간 **선택적 짝 프로그래밍** | 리뷰 품질 유지 및 개발자 집중력 보존 |
| TDD 초기 도입 시 테스트 작성 오버헤드로 일정 지연 우려 | 단위 테스트 프레임워크 템플릿화 및 통합 테스트와 병행 | 초기 속도 유지 및 장기 결함 수정 비용 90% 절감 |
| 상주 고객(On-site Customer)의 현실적 참여 불가 | **PO(Product Owner)의 상시 대리인 역할** 및 비동기 채널 가동 | 요구사항 모호성 즉각 해소 |
| 짝 프로그래밍 시 주니어/시니어 간 지식 격차로 인한 독점 | 드라이버/내비게이터 20분 핑퐁 교체(Pomodoro) 룰 적용 | 상호 지식 전수 및 코드 소유권 평준화 |

#### 한줄 요약
- 선택적 짝 코딩, TDD 템플릿화, PO 상시 소통, 핑퐁 교대로 실무 생산성을 극대화한다.

## Ⅶ. 결론

- 프로젝트 관리는 **Scrum**, 코드 품질은 **XP 실천법** 선택

#### 한줄 요약
- XP는 개발자가 작성하는 모든 코드의 무결성을 TDD와 짝 프로그래밍을 통해 극단적으로 끌어올리는 실천 공학이다.
