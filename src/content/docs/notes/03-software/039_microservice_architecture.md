---
sidebar:
  order: 39
  label: "039. 마이크로서비스 아키텍처 MSA (Microservice Architecture)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "마이크로서비스 아키텍처 MSA (Microservice Architecture)"
date: "2026-08-13T14:43:00+09:00"
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

<details><summary>용어 설명</summary>

- **MSA (Microservice Architecture)**: 대규모 애플리케이션을 비즈니스 도메인 단위로 분할하여, 독립적으로 배포/확장 가능한 소규모 서비스 집합으로 구성하는 소프트웨어 아키텍처 스타일.
- **Database-per-Service**: 서비스가 자신의 데이터 저장소 스키마와 접근 계약을 소유하는 원칙.
- **Decomposition**: Monolithic 시스템을 DDD(Domain-Driven Design) Bounded Context 기법을 적용하여 독립적 마이크로서비스로 분할 도출하는 설계 기법.

</details>

- 정의/개념: 단일 애플리케이션을 도메인 단위의 독립적 소형 서비스로 분할하여, 독자적 DB(Database-per-service)와 독립적 CI/CD 배포 파이프라인을 운영하는 **MSA (Microservice Architecture)**
- 배경/필요성: 단일 배포체의 강한 결합은 **변경•배포•확장 단위 분리 곤란**

#### 한줄 요약

- MSA는 업무별 데이터•배포 경계를 독립 서비스로 분리한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Fault Isolation (장애 격리)**: 특정 마이크로서비스(e.g., 추천 서비스)에 장애가 발생해도 서킷 브레이커 등을 통해 타 핵심 서비스(e.g., 결제 서비스)로 붕괴가 전파되지 않는 성질.
- **Polyglot Persistence**: 각 서비스의 특성에 맞춰 최적의 기술 스택(Java, Go, Python) 및 DB(RDBMS, NoSQL, In-memory)를 자유롭게 채택하는 속성.

</details>

- **Database-per-Service** 및 서비스 단위 독립적 CI/CD 배포 파이프라인
- **Polyglot Architecture / Polyglot Persistence** 지원
- **Fault Isolation (장애 격리)** 및 개별 서비스 단위 **Scale-out** 최적화

#### 한줄 요약

- 서비스 경계, 버전된 계약, 부분 장애 대응을 정렬한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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

| 구성요소 | 책임 |
|:---|:---|
| API 게이트웨이 | 외부 인증•라우팅•호출량 제한 적용 |
| 주문 서비스•소유 데이터 | 주문 업무와 데이터 변경 책임 소유 |
| 결제 서비스•소유 데이터 | 결제 업무와 데이터 변경 책임 소유 |
| 이벤트 브로커 | 서비스 간 비동기 상태 변화 전달 |
| 관측 플랫폼 | 로그•메트릭•**분산 추적** 상관관계 제공 |

#### 한줄 요약

- API 게이트웨이, 데이터 소유권, 이벤트 브로커, 관측 플랫폼이 서비스 경계를 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Distributed Transaction**: 여러 마이크로서비스에 걸쳐 실행되는 트랜잭션으로, 단일 2PC 대신 Saga Pattern(Orchestration/Choreography) 기반 최종 일관성(Eventual Consistency)으로 수습.

</details>

```text
┌──────────────────────────────┐
│ 클라이언트 요청 (Client)    │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 게이트웨이 진입             │
│ 1. 서비스 위치 탐색         │
│ 2. 마이크로서비스 동기 호출 │
│ 3. 이벤트 브로커 비동기 전파│
│ 4. Saga 기반 최종 일관성    │
└──────────────────────────────┘
```

### 동작 원리

1. 서비스 위치 탐색: Registry•DNS에서 목적 서비스 인스턴스 조회
2. 마이크로서비스 동기 호출: 타임아웃•회로 차단을 적용해 API 호출
3. 이벤트 브로커 비동기 전파: 로컬 변경 후 상태 이벤트 발행
4. Saga 기반 최종 일관성: 로컬 트랜잭션과 보상 동작으로 수렴

#### 한줄 요약

- 소유 서비스 로컬 처리와 동기 API 협업•비동기 이벤트 협업이 핵심이다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Distributed Monolith (분산 모놀리스)**: 서비스가 분리됐지만 동기 의존과 공동 배포로 독립성이 없는 분산 구조.

</details>

| 비교 항목 | Monolithic Architecture | Microservice Architecture (MSA) |
|:---|:---|:---|
| 시스템 형태 | 단일 배포 단위 | 업무 경계별 독립 서비스 배포체 |
| 데이터베이스 | 단일 중앙 DB 공유 | **Database-per-Service (개별 독립 DB)** |
| 배포 영향도 | 작은 수정 시에도 전체 재배포 필요 | **해당 서비스만 독립적 즉시 배포 가능** |
| 트랜잭션 | ACID 단일 DB 트랜잭션 | **Saga Pattern 기반 최종 일관성 (Eventual)** |
| 복잡도 위치 | 코드 내부 도메인 복잡도 | **네트워크/분산 인프라 및 운영 복잡도** |

#### 한줄 요약

- 독립 배포는 MSA, 단순 운영은 모듈러 모놀리스가 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

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

<details><summary>용어 설명</summary>

- **MSA 도입 판정 기준(MSA Adoption Criteria)**: 조직 도메인 복잡도, DevOps 자동화 역량, 배포 민첩성 요구에 의거한 수립 체계.

</details>

- 독립 배포 이익이 크면 **MSA**, 경계 불확실•운영 역량 부족이면 **Modulith** 선택

#### 한줄 요약

- 독립 배포 이익과 분산 비용을 함께 평가하는 것이 핵심이다.
