---
sidebar:
  order: 39
  label: "039. 마이크로서비스 아키텍처 MSA (Microservice Architecture)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "마이크로서비스 아키텍처 MSA (Microservice Architecture)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 39
extra:
  question_no: "039"
  source_status: "기출"
  source_history: "120회, 123회, 135회"
  priority: 70
  priority_note: "120•123•135회 반복, MSA 설계 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **MSA (Microservice Architecture)**: 대규모 애플리케이션을 비즈니스 도메인 단위로 분할하여, 독립적으로 배포/확장 가능한 소규모 서비스 집합으로 구성하는 소프트웨어 아키텍처 스타일.
- **Database-per-Service**: 각 마이크로서비스가 전용 독자 데이터베이스를 독립 소유하여, 타 서비스와의 DB 수준 직결 억세스를 완벽 차단하는 핵심 원칙.
- **Decomposition**: Monolithic 시스템을 DDD(Domain-Driven Design) Bounded Context 기법을 적용하여 독립적 마이크로서비스로 분할 도출하는 설계 기법.

</details>

- 정의/개념: 단일 애플리케이션을 도메인 단위의 독립적 소형 서비스로 분할하여, 독자적 DB(Database-per-service)와 독립적 CI/CD 배포 파이프라인을 운영하는 **MSA (Microservice Architecture)**
- 배경/필요성: 거대한 Monolithic 시스템의 변경 파급 효과, 배포 병목, 단일 결함 시 전체 붕괴(SPOF) 및 특정 기능별 수평 확장(Scale-out) 한계 극복 요구성

#### 한줄 요약

- MSA는 업무별 데이터•배포 경계를 독립 서비스로 분리한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Fault Isolation (장애 격리)**: 특정 마이크로서비스(e.g., 추천 서비스)에 장애가 발생해도 서킷 브레이커 등을 통해 타 핵심 서비스(e.g., 결제 서비스)로 붕괴가 전파되지 않는 성질.
- **Polyglot Persistence**: 각 서비스의 특성에 맞춰 최적의 기술 스택(Java, Go, Python) 및 DB(RDBMS, NoSQL, In-memory)를 자유롭게 채택하는 속성.

</details>

- **Database-per-Service** 및 서비스 단위 독립적 CI/CD 배포 파이프라인
- **Polyglot Architecture / Polyglot Persistence** 지원
- **Fault Isolation (장애 격리)** 및 개별 서비스 단위 **Scale-out** 최적화

#### 한줄 요약

- 서비스 경계, 버전된 계약, 부분 장애 대응을 정렬한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **API Gateway**: 클라이언트 요청의 단일 진입점으로 라우팅, 인증/인가, Rate Limiting, SSL Termination을 일괄 처리하는 중앙 엣지 서버.
- **Service Discovery**: 동적으로 스케일링/변경되는 마이크로서비스들의 IP/Port 위치 정보를 Registry(Eureka/Consul)에 등록하고 자동 매핑 검색하는 메커니즘.

</details>

```text
               [API 게이트웨이]
                  /         \
 [주문 서비스•소유 데이터] [결제 서비스•소유 데이터]
                  \         /
               [이벤트 브로커]
                      |
                [관측 플랫폼]
```

선의 의미: API Gateway가 외부 요청을 인가받아 Service Discovery 검색 후 마이크로서비스로 라우팅하고, Event Broker 기반 비동기 통신 및 Distributed Tracing 관측이 연동되는 아키텍처.

| 구분 분류 | 핵심 구성요소 (Components) | 주요 역할 및 기술 스택 |
|:---|:---|:---|
| **Outer Architecture (기반 인프라)** | **API Gateway** | 클라이언트 단일 진입점, 라우팅, 인증 (Spring Cloud Gateway, Kong) |
| | **Service Discovery** | 동적 서비스 인스턴스 위치 등록 및 탐색 (Eureka, Consul, K8s Service) |
| | **Config Server** | 각 서비스별 환경 설정 파일 중앙 집중 관리 (Spring Cloud Config) |
| | **Distributed Tracing** | 마이크로서비스 간 비동기 분산 트레이스 모니터링 (Zipkin, Jaeger, OpenTelemetry)|
| **Inner Architecture (서비스 내부)** | **Domain Service** | Bounded Context 기반 독립 비즈니스 로직 및 전용 DB 소유 |
| | **Resilience / Circuit Breaker**| 타 서비스 호출 실패 시 차단 및 Fallback 수행 (Resilience4j) |

#### 한줄 요약

- API 게이트웨이, 데이터 소유권, 이벤트 브로커, 관측 플랫폼이 서비스 경계를 연결한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Distributed Transaction**: 여러 마이크로서비스에 걸쳐 실행되는 트랜잭션으로, 단일 2PC 대신 Saga Pattern(Orchestration/Choreography) 기반 최종 일관성(Eventual Consistency)으로 수습.

</details>

```text
┌──────────────────────────────┐
│ 클라이언트 요청 (Client)    │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. API Gateway 진입         │
│ 2. Service Discovery 탐색   │
│ 3. 마이크로서비스 동기 호출  │
│ 4. Event Broker 비동기 전파 │
│ 5. Saga 기반 최종 일관성    │
└──────────────────────────────┘
```

### 동작 원리

1. **API Gateway 진입**: 외부 HTTP 요청 진입 시 OAuth2/JWT 인증 및 Rate Limit 검증.
2. **Service Discovery 탐색**: **Eureka / K8s DNS** 로부터 목적지 서비스의 동적 Pod IP/Port 인출.
3. **마이크로서비스 동기 호출**: REST / gRPC 기반 서킷 브레이커 wrapping 타깃 서비스 호출.
4. **Event Broker 비동기 전파**: 상태 변화(e.g., 주문완료) 발생 시 Kafka로 이벤트 발행.
5. **Saga 기반 최종 일관성**: 이벤트를 수신한 타 서비스들이 로컬 트랜잭션을 각각 수행하여 최종 정합성 완결.

#### 한줄 요약

- 소유 서비스 로컬 처리와 동기 API 협업•비동기 이벤트 협업이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Distributed Monolith (분산 모놀리스)**: MSA로 서비스는 쪼개놓았으나, 통신이 강하게 결합되고 하나를 배포하려면 전체를 동시 배포해야 하는 최악의 헛깨비 아키텍처.

</details>

| 비교 항목 | Monolithic Architecture | Microservice Architecture (MSA) |
|:---|:---|:---|
| 시스템 형태 | 단일 거대 실행 파일 (WAR/JAR) | **독립된 수십 개의 소형 서비스 배포체** |
| 데이터베이스 | 단일 중앙 DB 공유 | **Database-per-Service (개별 독립 DB)** |
| 배포 영향도 | 작은 수정 시에도 전체 재배포 필요 | **해당 서비스만 독립적 즉시 배포 가능** |
| 트랜잭션 | ACID 단일 DB 트랜잭션 | **Saga Pattern 기반 최종 일관성 (Eventual)** |
| 복잡도 위치 | 코드 내부 도메인 복잡도 | **네트워크/분산 인프라 및 운영 복잡도** |

#### 한줄 요약

- 독립 배포는 MSA, 단순 운영은 모듈러 모놀리스가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Saga Pattern**: 마이크로서비스 간 분산 트랜잭션 수행 시, 각 서비스별 로컬 트랜잭션을 순차 실행하고 실패 시 보상 트랜잭션(Compensating Transaction)을 역순으로 실행하는 디자인 패턴.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 서비스 분할로 인한 단일 ACID DB 트랜잭션 파괴 | **Saga Pattern (Choreography / Orchestration)** 채택 | 최종 일관성(Eventual Consistency) 확보 |
| 타 서비스 장애 연쇄 전파로 전체 붕괴 | **Circuit Breaker (Resilience4j)** 및 Timeout 적용 | **Fault Isolation (장애 격리)** |
| 분산 환경에서 사용자 요청 트레이스 불능 | **Distributed Tracing (OpenTelemetry / Zipkin)** 도입 | 전구간 Latency 병목 추적성 확보 |

> 사례: Netflix / 쿠팡 / 배달의민족 엔터프라이즈 **Spring Cloud + K8s** 기반 MSA 전면 구축

#### 한줄 요약

- 트랜잭셔널 아웃박스, 회로 차단기, SLO, 분산 추적으로 운영한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **MSA 도입 판정 기준(MSA Adoption Criteria)**: 조직 도메인 복잡도, DevOps 자동화 역량, 배포 민첩성 요구에 의거한 수립 체계.

</details>

- **MSA 도입 판정 기준**에 따라 무조건적인 분할을 지양하고, **DDD Bounded Context** 검증 후 **Database-per-service** 아키텍처 인가

#### 한줄 요약

- 독립 배포 이익과 분산 비용을 함께 평가하는 것이 핵심이다.
