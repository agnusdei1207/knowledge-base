---
sidebar:
  order: 38
  label: "038. 소프트웨어 아키텍처 패턴: MVC•MSA•이벤트드리븐 (Architecture Patterns)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "소프트웨어 아키텍처 패턴: MVC•MSA•이벤트드리븐 (Architecture Patterns)"
date: "2026-08-13T14:40:00+09:00"
tags:
  - "notes-software"
weight: 38
extra:
  question_no: "038"
  source_status: "기출"
  source_history: "120회"
  priority: 30
  priority_note: "120회 기출 후 저빈도, 패턴 범위•절충 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Architecture Pattern**: 소프트웨어 시스템의 전체적인 구조, 서브시스템 간 역할 분담, 통신 방식 및 고유 품질 속성(Quality Attributes)을 해결하기 위한 검증된 고차원 구조 청사진.
- **Layered Pattern (계층형 패턴)**: Presentation, Business Logic, Persistence 계층으로 세부 관심사를 세로로 분리하여 모듈성을 높이는 가장 보편적 아키텍처.
- **Trade-off Analysis (아키텍처 트레이드오프)**: 특정 패턴 채택에 따른 이점(e.g., 확장성, 변경 수용성)과 비용/오버헤드(e.g., 네트워크 지연, 복잡성, 일관성 파괴) 간의 절충안 분석.

</details>

- 정의/개념: 소프트웨어 개발 시 반복 발생하는 전체 구조 설계 문제에 대해 검증된 모듈 구성과 통신 청사진을 재사용하는 아키텍처 틀인 **Architecture Pattern**
- 배경/필요성: 변경 축과 책임 경계가 없으면 **결합도•변경 파급** 증가

#### 한줄 요약

- 반복 설계 문제에 아키텍처 패턴을 재사용하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Separation of Concerns (관심사 분리)**: 비즈니스 로직, 화면 UI, 데이터 영속화 레이어를 상호 독립적인 모듈로 격리하여 코드 수정 파급을 최소화하는 원칙.
- **System Quality Attributes (품질 속성)**: 가용성(Availability), 성능(Performance), 확장성(Scalability), 보안성(Security), 유지보수성(Modifiability) 등 아키텍처 패턴 선택을 결정짓는 척도.

</details>

- 시스템 전체 아키텍처의 **Separation of Concerns (관심사 분리)** 보장
- 시스템 비기능 **Quality Attributes (품질 속성)** 결정
- 각 패턴 간 성능-확장성-복잡도 간의 **Trade-off Analysis** 상주

#### 한줄 요약

- 책임 경계, 경계 간 계약, 결합도, 분산 복잡도의 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **MVC (Model-View-Controller)**: UI(View), 비즈니스 데이터/로직(Model), 입력 처리 및 데이터 흐름 중계(Controller)를 분리하는 데스크톱/웹 아키텍처 패턴.
- **EDA (Event-Driven Architecture)**: 이벤트 생산자(Producer)와 소비자(Consumer)가 브로커(Broker)를 경유하여 비동기 메시지 기반으로 결합도를 극단적으로 낮춘 아키텍처.

</details>

```text
┌────────────────────────────────────────────────────────┐
│                   Architecture Patterns                │
├────────────┬──────────────┬──────────────┬──────────────┤
│ Layered   │ Microservices│ Event-Driven │ Hexagonal    │
└────────────┴──────────────┴──────────────┴──────────────┘
```

선의 의미: 대표적 아키텍처 패턴인 Layered/MVC, MSA, EDA가 도메인 특성 및 분산화 수준에 따라 적용 선택되는 아키텍처 스펙트럼.

| 구성요소 | 책임 |
|:---|:---|
| Layered | 표현•업무•영속 책임을 계층으로 분리 |
| Microservices | 업무 경계별 독립 배포•데이터 소유 |
| Event-Driven | 이벤트로 생산자와 소비자 시간 결합 완화 |
| Hexagonal | 포트•어댑터로 도메인과 외부 기술 분리 |

#### 한줄 요약

- MVC, MSA, 캡슐화가 책임 경계 분리 방식을 보여 준다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Architecture Decision Record (ADR)**: 특정 아키텍처 패턴 채택 이유, 맥락, 고려된 대안 및 트레이드오프 결과를 기록 관리하는 문서.

</details>

```text
┌──────────────────────────────┐
│ 주요 변경 축•품질 요구     │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 시스템 품질 목표 설정     │
│ 2. 패턴 후보군 도출         │
│ 3. Trade-off 평가           │
│ 4. 패턴 확정 및 ADR 작성    │
└──────────────┬───────────────┘
               ▼
       [아키텍처 구체화]
```

### 동작 원리

1. **시스템 품질 목표 설정**: 가용성, 확장성, 응답속도, 개발 팀 규모 등 비기능 속성 요구 파악.
2. **패턴 후보군 도출**: 단일 DB 중심(MVC/Layered) vs 분산 서비스(MSA) vs 이벤트 기반(EDA) 후보 선정.
3. **Trade-off 평가**: 분산 트랜잭션, 데이터 정합성, 네트워크 홉(Hop) 오버헤드 비교 분석.
4. **패턴 확정 및 ADR 작성**: 최종 아키텍처 결정 의사결정서(**ADR**) 문서화 및 적용.

#### 한줄 요약

- 변경 축에 따라 화면 책임 분리, 업무•데이터 경계 분리, 비동기 전파 분리를 선택한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Monolith vs Microservices vs Event-Driven**: 소규모/단순 서비스는 Monolith, 독립된 도메인 스케일링은 MSA, 실시간 비동기 스트리밍은 EDA 선택.

</details>

| 비교 항목 | Layered / MVC | Microservices (MSA) | Event-Driven (EDA) |
|:---|:---|:---|:---|
| 데이터베이스 | 단일 중앙 RDBMS 공유 | **Service-per-Database** 독립 DB | 이벤트 저장소 / 비동기 뷰 DB |
| 통신 방식 | 인메모리 함수 호출 | Synchronous REST/gRPC | **Asynchronous Event (Pub/Sub)** |
| 일관성 모델 | 강한 일관성 (ACID) | 2PC 또는 Saga 패턴 (최종 일관성) | **최종 일관성 ** |
| 적합한 분야 | 소규모 Web App, 초기 MVP | **대규모 복잡 엔터프라이즈 도메인** | **실시간 피드, IoT, 대용량 트래픽 통지** |

#### 한줄 요약

- 화면은 MVC, 독립 배포는 MSA, 비동기는 EDA가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Architectural Degradation (아키텍처 부패)**: 초기에 수립한 아키텍처 패턴 규칙(계층 무단 점프, 서비스 간 직접 DB 억세스 등)을 개발 진행 중 어김으로써 시스템이 무질서해지는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 트렌드만 따라 불필요하게 MSA/EDA 적용 시 분산 복잡도 폭증 | **Modulith (모듈리스)** 아키텍처 선적용 후 필요 시 분할 | 시스템 복잡도 통제 |
| Layered 아키텍처의 계층 침범 및 **Architectural Degradation** | **ArchUnit** 등의 아키텍처 단위 테스트 도구로 CI 검증 | 설계 규칙 강제 자동화 |
| EDA 환경에서의 이벤트 무단 변경으로 인한 파괴적 장애 | **Schema Registry (Avro/Protobuf)** 및 백워드 호환성 관리 | 이벤트 인터페이스 호환성 확보 |

> 사례: **ADR (Architecture Decision Record)** 생명주기 관리 및 **Modulith-to-MSA** 진화 아키텍처 구축

#### 한줄 요약

- ADR, 소비자 계약 시험, 트랜잭셔널 아웃박스, 관측성으로 패턴을 검증한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **아키텍처 패턴 선택 기준(Architecture Pattern Selection Criteria)**: 시스템 품질 목표(Scalability, Availability), 팀 역량 및 도메인 복잡도에 의거한 체계.

</details>

- 단일 배포는 **Layered**, 독립 배포는 **MSA**, 비동기 전파는 **EDA** 선택

#### 한줄 요약

- 화면•배포•전파 변경 축을 함께 평가하는 것이 핵심이다.
