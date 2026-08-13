---
sidebar:
  order: 48
  label: "048. 헥사고날 아키텍처: 포트•어댑터 (Hexagonal Architecture)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "헥사고날 아키텍처: 포트•어댑터 (Hexagonal Architecture)"
date: "2026-08-13T15:17:00+09:00"
tags:
  - "notes-software"
weight: 48
extra:
  question_no: "048"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "포트•어댑터는 도메인 의존성 격리 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Hexagonal Architecture (포트와 어댑터 아키텍처)**: 애플리케이션 핵심을 포트 계약과 어댑터로 외부 기술에서 분리하는 아키텍처.
- **Port (포트)**: 애플리케이션 코어와 외부 세계를 연결하는 기술 독립적인 인터페이스 계약 (Primary/Inbound Port, Secondary/Outbound Port).
- **Adapter (어댑터)**: 외부 기술 표준(REST, GraphQL, JPA, Kafka)을 Port 인터페이스 규격에 맞춰 상호 데이터 변환(Mapping) 및 연결해 주는 구체 모듈.

</details>

- 정의/개념: 외부 프레임워크 및 DB 기술의 변경이 비즈니스 도메인 로직에 침범하지 못하도록 **Ports & Adapters** 인터페이스 장벽을 구축하는 **Hexagonal Architecture**
- 배경/필요성: 도메인의 프레임워크•DB 직접 의존은 **기술 교체•격리 시험 방해**

#### 한줄 요약

- 포트와 어댑터를 통한 헥사고날 아키텍처의 외부 의존 격리가 핵심이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Inbound vs Outbound Port**: Inbound Port는 외부에서 도메인을 호출하는 유스케이스(Use Case) 창구, Outbound Port는 도메인이 외부 자원(DB, API)을 호출할 때 사용하는 인터페이스.
- **Dependency Inversion**: 외부에 존재하는 어댑터가 내부의 포트(인터페이스)를 구체화(Implement)하도록 하여 의존성 방향을 항상 내부(Core Domain)로만 향하게 만드는 원칙.

</details>

- 외부 어댑터가 내부 포트에 의존하는 **Dependency Inversion**
- Primary(Driving/Inbound) 대 Secondary(Driven/Outbound) **Ports & Adapters** 구조
- 포트 대역으로 외부 DB•UI 없이 핵심 로직 시험 가능

#### 한줄 요약

- 유스케이스, 오류 변환, 테스트 대역 기반 격리가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Domain Core (도메인 코어)**: 프레임워크나 외부 기술 의존성(Annotation, Library)이 0%인 순수한 엔티티(Entity) 및 비즈니스 유스케이스(Use Case) 로직의 집합.

</details>

```text
[인바운드 어댑터]
         |
 [인바운드 포트]
         |
[애플리케이션 핵심 (Domain Core)]
         |
 [아웃바운드 포트]
         |
[아웃바운드 어댑터]
```

선의 의미: 외부 요청이 Inbound Adapter를 통해 Inbound Port로 주입되어 Domain Core를 구동하고, Outbound Port를 통해 Outbound Adapter(DB/Infra)로 나아가는 육각형 구조.

| 구성요소 | 책임 |
|:---|:---|
| 인바운드 어댑터 | 외부 요청을 애플리케이션 명령으로 변환 |
| 인바운드 포트 | 외부에 제공할 유스케이스 계약 정의 |
| 애플리케이션 핵심 (Domain Core) | 도메인 규칙과 유스케이스 실행 |
| 아웃바운드 포트 | 핵심이 요구하는 외부 자원 계약 정의 |
| 아웃바운드 어댑터 | DB•Broker•외부 API 기술로 포트 구현 |

#### 한줄 요약

- 인바운드 어댑터부터 아웃바운드 어댑터까지의 경계 구조가 핵심이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Domain Model Mapping**: 외부 DTO(REST Request/JPA Entity) 데이터를 순수 Domain Entity 객체로 어댑터 상에서 매핑 변환하는 과정.

</details>

```text
┌──────────────────────────────┐
│ 외부 요청                    │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. 인바운드 어댑터 매핑     │
│ 2. 인바운드 포트 호출       │
│ 3. 도메인 핵심 실행         │
│ 4. 아웃바운드 포트 호출     │
│ 5. 아웃바운드 어댑터 매핑   │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 외부 자원                    │
└──────────────────────────────┘
```

### 동작 원리

1. **인바운드 어댑터 매핑**: 외부 DTO를 애플리케이션 명령으로 변환
2. **인바운드 포트 호출**: 유스케이스 계약을 통해 핵심 진입
3. **도메인 핵심 실행**: 도메인 규칙을 검증하고 상태 변경
4. **아웃바운드 포트 호출**: 저장•발행 등 필요한 외부 계약 요청
5. **아웃바운드 어댑터 매핑**: 계약을 외부 기술 호출로 변환

#### 한줄 요약

- 인바운드 매핑부터 응답•오류 변환까지의 흐름이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Clean Architecture vs Hexagonal Architecture**: Clean Architecture(Robert C. Martin)는 동심원 계층(Entities, Use Cases, Controllers, Presenters)으로 고도화한 형태이며, Hexagonal은 Port/Adapter 2원화 중심의 동일한 관점 표현.

</details>

| 비교 항목 | Traditional Layered (계층형) | Hexagonal Architecture (포트/어댑터) |
|:---|:---|:---|
| 의존성 방향 | Presentation $\rightarrow$ Domain $\rightarrow$ Persistence (DB) | **Adapter $\rightarrow$ Port $\rightarrow$ Domain Core (항상 도메인 중심)** |
| DB 기술 결합 | Domain이 JPA Entity `@Entity` 기술에 무단 결합 | **Domain은 순수 POJO, Adapter가 매핑 변환** |
| 단위 테스트 | 계층 결합에 따라 DB 대역 필요 가능 | 포트 Stub으로 핵심 로직 격리 가능 |
| 코드 초기 복잡도 | 낮음 (빠른 작성 가능) | 높음 (Port, Adapter, Mapping 보일러플레이트 코드) |

#### 한줄 요약

- 고정 연동은 계층형 아키텍처, 반복 기술 교체는 헥사고날 아키텍처가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Boilerplate Code**: Port, Adapter, DTO-Domain간 Mapper 클래스가 대량으로 늘어나 초기 클래스 개수가 폭증하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 도메인 엔티티의 JPA 기술 의존 | 영속 Entity와 Domain 분리 또는 의존성 검토 | 도메인 변경과 영속 기술 변경 분리 |
| 초기 보일러플레이트 코드 증가로 인한 생산성 저하 | **MapStruct / ModelMapper** 매핑 자동화 및 필수 도메인에만 채택 | 매핑 오버헤드 완화 |
| 프레임워크 변경 가능성이 적은 프로젝트에 과잉 적용 | 프로젝트 성격 판단 후 헥사고날 또는 Modulith 선택 | 오버엔지니어링 차단 |

> 사례: **DDD (Domain-Driven Design) + Hexagonal Architecture + Spring Boot 3** 조합 구축

#### 한줄 요약

- 업무 용어 포트, 계약 테스트, 통합 시험 기반 격리가 핵심이다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **헥사고날 아키텍처 채택 기준(Hexagonal Architecture Selection Criteria)**: 도메인 로직 복잡성, 외부 기술 교체 가능성 및 테스트 자동화 목표에 의거한 체계.

</details>

- 외부 기술 교체•격리 시험이 잦으면 **Hexagonal**, 단순 고정 연동은 계층형

#### 한줄 요약

- 기술 교체•격리 시험 빈도와 고정 연동 여부를 함께 평가하는 것이 핵심이다.
