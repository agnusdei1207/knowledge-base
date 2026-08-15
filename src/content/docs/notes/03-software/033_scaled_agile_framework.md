---
sidebar:
  order: 33
  label: "033. SAFe 대규모 애자일 프레임워크 (Scaled Agile Framework)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "SAFe 대규모 애자일 프레임워크 (Scaled Agile Framework)"
date: "2026-08-13T14:25:00+09:00"
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

<details><summary>용어 설명</summary>

- **SAFe (Scaled Agile Framework)**: 단일 팀 단위의 애자일(Scrum/Kanban)을 수십~수천 명 규모의 전사적(Enterprise) 대규모 개발 조직으로 확장하여 린-애자일(Lean-Agile) 문화와 비즈니스 민첩성(Business Agility)을 정착시키는 프레임워크.
- **ART (Agile Release Train)**: 다수 교차기능 팀이 공통 비전과 계획 주기로 가치 흐름을 실행하는 장기 조직 단위.
- **PI (Planning Interval)**: ART가 목표•의존성을 정렬하고 가치를 개발•검증하는 다중 반복 계획 구간.

</details>

- 정의/개념: 단일 애자일 팀의 한계를 극복하고 전사적 경영 전략(Portfolio)부터 시스템 구현(Team)까지 린-애자일 가치를 동기화하는 확장 프레임워크인 **SAFe(Scaled Agile Framework)**
- 배경/필요성: 독립 팀 최적화만으로는 **전략•투자•의존성 정렬 곤란**

#### 한줄 요약

- SAFe는 전략•투자•팀 의존성을 린•애자일 원칙으로 정렬한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **PI Planning (PI 플래닝)**: 8~12주 PI 주기마다 모든 ART 구성원(50~125명 이상)이 한자리에 모여 2일간 전사 목표, 팀 간 의존성, 위험 요소를 정렬하는 대규모 통합 계획 이벤트.
- **Value Stream (가치 스트림)**: 아이디어/요구사항이 발화된 시점부터 최종 고객에게 소프트웨어 가치가 전달될 때까지의 전 과정 활동 파이프라인.

</details>

- 구성 선택에 따른 **Essential•Large Solution•Portfolio** 적용
- **ART** 기반 교차기능 팀의 가치 흐름 실행
- **PI Planning**과 **Inspect & Adapt**로 목표•의존성 조정

#### 한줄 요약

- ART, PI, 가치 스트림을 통한 다수 팀 정렬이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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

| 구성요소 | 책임 |
|:---|:---|
| 린 포트폴리오 관리 | 전략•투자와 가치 흐름 우선순위 정렬 |
| 개발 가치 흐름 | 아이디어부터 고객 가치까지 흐름 관리 |
| 애자일 릴리스 트레인 | **PI 목표•의존성**과 시스템 통합 조정 |
| 애자일 팀 | Scrum•Kanban으로 기능 증분 구현 |

#### 한줄 요약

- LPM, DVS, 애자일 팀의 계층 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Program Board**: PI Planning 2일차에 각 팀의 Feature 개발 주입 건과 팀 간 의존성(Red String/Red Line)을 시각화하여 공유하는 매트릭스 보드.

</details>

```text
┌──────────────────────────────┐
│ 1. 전략•투자 우선순위 (LPM) │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 2. PI 목표•의존성 정렬      │
└──────────────┬───────────────┘
               ▼
╔══════════════════════════════╗
║ 3. 팀 증분•시스템 통합      ║
║    (반복 개발•검증)         ║
╚══════════════╤═══════════════╝
               ▼
┌──────────────────────────────┐
│ 4. 시스템 데모 (System Demo)│
│ 5. 검사•적응 (I&A Event)    │
└──────────────────────────────┘
```

### 동작 원리

1. **전략·투자 우선순위 (LPM)**: Portfolio 계층에서 전사 Epic 정렬 및 Lean Budget 승인.
2. **PI 목표·의존성 정렬**: 팀별 목표와 Program Board 의존성 합의
3. **팀 증분·시스템 통합**: 반복마다 기능을 구현하고 시스템 수준 통합
4. **시스템 데모**: 통합 결과를 시연하고 이해관계자 피드백 수집
5. **검사·적응**: 흐름 지표와 문제 해결 결과로 다음 구간 개선

#### 한줄 요약

- PI 계획부터 검사•적응까지의 피드백 순환이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IP Iteration (Innovation and Planning)**: 혁신•학습•계획과 다음 PI 준비를 지원하는 반복 구간.

</details>

| 비교 항목 | SAFe (Scaled Agile Framework) | LeSS (Large-Scale Scrum) | Nexus |
|:---|:---|:---|:---|
| 확장 철학 | 전사 관리 프로세스 중심 (Top-down + Bottom-up) | 미니멀 스크럼 확장 (Bottom-up 중심) | Scrum 프레임워크 확장 (3~9개 팀) |
| 구성 가이드라인 | **매우 상세하고 구체적 (프레임워크 도감)** | 유연하고 단순함 (Principles 위주) | 스크럼 통합(Nexus Integration Team) 위주 |
| 주요 적합 조직 | 대규모 금융, 공공, 제조, 자동차 엔터프라이즈 | IT 소프트웨어 중심 대규모 조직 | 중대형 개발 조직 (10팀 미만) |

#### 한줄 요약

- 팀 의존성이 크면 SAFe, 독립 팀은 스크럼이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SAFe in Name Only (SINO)**: SAFe의 용어와 표면적 이벤트만 도입하고, 실제로는 관료적 하향식(Top-down) 통제와 거대한 사전에 만들어진 계획(Big Upfront Planning)을 고수하는 파행적 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 전사적 대규모 PI Planning 시 팀 간 의존성 복잡성 폭증 | **Program Board** 시각화 및 RTE 주도 의존성 재정렬 | 팀 간 가로막힘(Block) 해소 |
| 단기 기능 중심으로 기술 부채 누적 | **IP Iteration**과 아키텍처 런웨이 투자 | 학습•기술 기반 작업의 용량 확보 |
| 명목만 SAFe 도입하고 기존 하향식 통제 지속 (**SINO**) | SPC (SAFe Program Consultant)의 리더십 린-애자일 변혁 코칭 | 진정한 비즈니스 민첩성 획득 |

> 사례: 대형 자동차(ECU/AUTOSAR) 및 금융 차세대 엔터프라이즈 내 **SAFe 6.0** 도입 사례

#### 한줄 요약

- 가치 흐름•의존성 지도화, 흐름 지표, 가드레일로 조정 범위를 최소화한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **전사 애자일 확장 기준(Enterprise Agile Scaling Criteria)**: 개발 인력 수, 팀 간 의존성 복잡도, 거버넌스 요구에 따른 확장 체계.

</details>

- 다수 팀의 강한 의존성•포트폴리오 정렬은 **SAFe**, 단순 확장은 **LeSS** 검토

#### 한줄 요약

- 가치 흐름 범위와 팀 의존성을 함께 평가하는 것이 핵심이다.
