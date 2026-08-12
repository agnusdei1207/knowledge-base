---
sidebar:
  order: 33
  label: "033. SAFe 대규모 애자일 프레임워크 (Scaled Agile Framework)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "SAFe 대규모 애자일 프레임워크 (Scaled Agile Framework)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 33
extra:
  question_no: "033"
  source_status: "기출"
  source_history: "122회, 134회, 137회"
  priority: 70
  priority_note: "122•134•137회 반복, 규모 확장 애자일 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **SAFe (Scaled Agile Framework)**: 단일 팀 단위의 애자일(Scrum/Kanban)을 수십~수천 명 규모의 전사적(Enterprise) 대규모 개발 조직으로 확장하여 린-애자일(Lean-Agile) 문화와 비즈니스 민첩성(Business Agility)을 정착시키는 프레임워크.
- **ART (Agile Release Train)**: 50~125명 규모의 다수 교차기능 애자일 팀들이 동일한 공통 비전, 개발 주기에 맞춰 가치 스트림(Value Stream)을 지속 배포하는 대규모 조직 실행 단위.
- **PI (Planning Interval)**: ART가 비즈니스 가치를 계획하고 개발/검증하는 8~12주 단위의 대규모 고정 타임박스 (보통 5개의 2주 스프린트로 구성).

</details>

- 정의/개념: 단일 애자일 팀의 한계를 극복하고 전사적 경영 전략(Portfolio)부터 시스템 구현(Team)까지 린-애자일 가치를 동기화하는 확장 프레임워크인 **SAFe(Scaled Agile Framework)**
- 배경/필요성: 대규모 엔터프라이즈 환경에서 팀 간 의존성(Dependency) 복잡도 폭증, 전사적 전략-실행 정렬 불일치 및 가치 전달 지연(Time-to-Market) 극복 요구성

#### 한줄 요약

- SAFe는 전략•투자•팀 의존성을 린•애자일 원칙으로 정렬한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **PI Planning (PI 플래닝)**: 8~12주 PI 주기마다 모든 ART 구성원(50~125명 이상)이 한자리에 모여 2일간 전사 목표, 팀 간 의존성, 위험 요소를 정렬하는 대규모 통합 계획 이벤트.
- **Value Stream (가치 스트림)**: 아이디어/요구사항이 발화된 시점부터 최종 고객에게 소프트웨어 가치가 전달될 때까지의 전 과정 활동 파이프라인.

</details>

- 4대 레벨 구성 (**Essential, Large Solution, Portfolio, Full SAFe**)
- **ART (Agile Release Train)** 기반 50~125명 단위 교차기능 릴리스 파이프라인 구축
- **PI Planning (2일간 전사 수평적/수직적 정렬)** 및 **Inspect & Adapt (I&A 회고)**

#### 한줄 요약

- ART, PI, 가치 스트림을 통한 다수 팀 정렬이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **RTE (Release Train Engineer)**: ART 전체를 오케스트레이션하고 의존성 해소 및 PI 실행을 총괄 지휘하는 대규모 스케일의 Scrum Master.
- **System Architect**: ART 전체의 기술 아키텍처 비전, 엔지니어링 가이드라인 및 서브시스템 간 기술 정합성을 통제하는 리드 아키텍트.

</details>

```text
[린 포트폴리오 관리]
          |
[개발 가치 흐름]
          |
[애자일 릴리스 트레인]
          |
[애자일 팀]
```

선의 의미: Portfolio 전략이 Value Stream을 거쳐 ART(Agile Release Train) 단위로 할당되고, 개별 Agile Team의 스프린트 개발로 구체화되는 아키텍처.

| 구조 레벨 | 주요 역할 및 핵심 활동 | 주요 아티팩트/이벤트 |
|:---|:---|:---|
| **Portfolio Level** | **LPM (Lean Portfolio Management)**, 전사 전략 자금 배분 및 가치 스트림(Value Stream) 관리 | Epics, Lean Budget, Portfolio Canvas |
| **Large Solution Level** | 수백 명 이상 대규모 솔루션 관리, Solution Architect/Engineer | Solution Train, Solution Intent |
| **Program Level (ART)** | **ART 오케스트레이션**, **RTE (Release Train Engineer)**, **PI Planning** | Features, PI Objectives, Program Board |
| **Team Level** | 단일 팀 단위의 기존 **Scrum / Kanban** 구동, PO, SM, Devs | Stories, Sprint Backlog, Team PI Objectives |

#### 한줄 요약

- LPM, DVS, 애자일 팀의 계층 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Program Board**: PI Planning 2일차에 각 팀의 Feature 개발 주입 건과 팀 간 의존성(Red String/Red Line)을 시각화하여 공유하는 매트릭스 보드.

</details>

```text
┌──────────────────────────────┐
│ 1. 전략•투자 우선순위 (LPM) │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 2. PI 목표•의존성 정렬       │
│    (PI Planning - 2일간)    │
└──────────────┬───────────────┘
               ▼
╔══════════════════════════════╗
║ 3. 팀 증분•시스템 통합      ║
║    (5개 Sprint 실행)        ║
╚══════════════╤═══════════════╝
               ▼
┌──────────────────────────────┐
│ 4. 시스템 데모 (System Demo)│
│ 5. 검사•적응 (I&A Event)    │
└──────────────────────────────┘
```

### 동작 원리

1. **전략·투자 우선순위 (LPM)**: Portfolio 계층에서 전사 Epic 정렬 및 Lean Budget 승인.
2. **PI 목표·의존성 정렬 (PI Planning)**: ART 전체 구성원이 모여 2일간 팀별 PI Objectives 및 **Program Board 의존성** 정렬.
3. **팀 증분·시스템 통합**: 5개 Sprint (4개 개발 + 1개 IP Sprint)를 구동하며 2주마다 **System Demo** 통합.
4. **시스템 데모 (System Demo)**: 매 2주마다 ART 전체 통합 시스템 기능 시연 및 피드백.
5. **검사·적응 (I&A)**: 10주 PI 종료 시점에 ART 전체 피드백, 정량 지표 평가 및 대규모 회고 완결.

#### 한줄 요약

- PI 계획부터 검사•적응까지의 피드백 순환이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **IP Sprint (Innovation and Planning)**: PI의 마지막 5번째 스프린트로, 혁신 실험(Hackathon), 기술 채무 해소, PI Planning 준비 및 교육에만 전념하는 특수 타임박스.

</details>

| 비교 항목 | SAFe (Scaled Agile Framework) | LeSS (Large-Scale Scrum) | Nexus |
|:---|:---|:---|:---|
| 확장 철학 | 전사 관리 프로세스 중심 (Top-down + Bottom-up) | 미니멀 스크럼 확장 (Bottom-up 중심) | Scrum 프레임워크 확장 (3~9개 팀) |
| 구성 가이드라인 | **매우 상세하고 구체적 (프레임워크 도감)** | 유연하고 단순함 (Principles 위주) | 스크럼 통합(Nexus Integration Team) 위주 |
| 주요 적합 조직 | 대규모 금융, 공공, 제조, 자동차 엔터프라이즈 | IT 소프트웨어 중심 대규모 조직 | 중대형 개발 조직 (10팀 미만) |

#### 한줄 요약

- 팀 의존성이 크면 SAFe, 독립 팀은 스크럼이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **SAFe in Name Only (SINO)**: SAFe의 용어와 표면적 이벤트만 도입하고, 실제로는 관료적 하향식(Top-down) 통제와 거대한 사전에 만들어진 계획(Big Upfront Planning)을 고수하는 파행적 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전사적 대규모 PI Planning 시 팀 간 의존성 복잡성 폭증 | **Program Board** 시각화 및 RTE 주도 의존성 재정렬 | 팀 간 가로막힘(Block) 해소 |
| 잦은 스프린트 개발로 인한 기술 채무 및 아키텍처 붕괴 | **IP Sprint (5번째 스프린트)** 보장 및 System Architect 주도 | 아키텍처 런웨이(Architectural Runway) 확보 |
| 명목만 SAFe 도입하고 기존 하향식 통제 지속 (**SINO**) | SPC (SAFe Program Consultant)의 리더십 린-애자일 변혁 코칭 | 진정한 비즈니스 민첩성 획득 |

> 사례: 대형 자동차(ECU/AUTOSAR) 및 금융 차세대 엔터프라이즈 내 **SAFe 6.0** 도입 사례

#### 한줄 요약

- 가치 흐름•의존성 지도화, 흐름 지표, 가드레일로 조정 범위를 최소화한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **전사 애자일 확장 기준(Enterprise Agile Scaling Criteria)**: 개발 인력 수, 팀 간 의존성 복잡도, 거버넌스 요구에 따른 확장 체계.

</details>

- **전사 애자일 확장 기준**에 따라 100명 이상의 대규모 엔터프라이즈 환경 구축 시 **SAFe 6.0 (ART + PI Planning)** 채택

#### 한줄 요약

- 가치 흐름 범위와 팀 의존성을 함께 평가하는 것이 핵심이다.
