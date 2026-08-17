---
sidebar:
  order: 163
  label: "163. 분산 추적 (Distributed Tracing)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "분산 추적 (Distributed Tracing)"
date: "2026-08-18T02:25:00+09:00"
tags:
  - "notes-software"
weight: 163
extra:
  question_no: "163"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "호출 경로와 지연 원인 추적 구조 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **분산 추적(Distributed Tracing)**: 단일 사용자 요청이 마이크로서비스 간에 전파되는 전체 경로를 글로벌 고유 식별자(Trace ID)와 작업 구간 단위(Span)의 계층 트리로 시각화하여 지연(Latency)과 에러 병목을 추적하는 기술.
- **분산 호출 경로 추적 한계(Distributed Path Tracing Limit)**: 다단계 마이크로서비스 및 비동기 메시지 큐 통신 환경에서 단일 서버 로컬 로그만으로는 전체 트랜잭션의 지연 구간과 호출 순서를 파악하지 못하는 위험.

</details>

- 정의/개념: 분산 환경에서 단일 트랜잭션의 호출 경로를 **Trace ID와 스팬(Span) 트리로 시각화하여 지연 구간과 병목을 추적**하는 관측성 기술
- 배경/필요성: 수십 개 마이크로서비스 간 비동기 RPC 호출로 인한 **단일 서버 로컬 로그 기반의 트랜잭션 호출 경로 추적 불가 위험** 직면

#### 한줄 요약

- Trace ID와 부모-자식 Span 계층 구조를 통해 마이크로서비스 간 호출 흐름과 지연 병목 구간을 투명하게 시각화

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **W3C Trace Context 규약**: `traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01` 헤더를 통해 HTTP 및 gRPC 경계를 넘어 트레이스 문맥을 전파하는 글로벌 표준.
- **Span 트리(DAG: Directed Acyclic Graph)**: Root Span을 시작으로 자식 Span들이 계층적으로 뻗어나가 호출 순서와 실행 시간을 나타내는 유향 비순환 그래프.

</details>

- 단일 트랜잭션 전체를 관통하는 **글로벌 고유 Trace ID 기반 상관 추적**
- 서비스 간 호출 선후 관계 및 실행 시간을 나타내는 **Parent-Child Span 계층 트리**
- W3C 표준 HTTP 헤더를 통해 비동기 큐와 RPC를 넘나드는 **문맥 전파(Context Propagation)**

#### 한줄 요약

- 분산 서비스 간의 호출 인과관계와 밀리초 단위 지연시간을 계층적 간트 차트로 완벽히 가시화

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Trace 및 Span 데이터 모델**: Trace ID(전체 식별자), Span ID(구간 식별자), Parent Span ID(부모 참조), Span Attributes(키-값 메타데이터), Events/Logs.

</details>

```text
[ 분산 추적(Distributed Tracing) 계층 트리 구조도 ]

 1. [ Client Request ] ──► [ Trace ID: 0x4bf9... 생성 (Root Span) ]
                                 │
                                 ▼
 2. [ Order Service Span (150ms) ] ── (W3C traceparent 헤더 주입)
    ┌─────────────────────────────────────────────────────────────┐
    │ Parent Span ID: null                                        │
    │ Attributes: `http.method=POST`, `http.route=/order`         │
    └────────────────────────────┬────────────────────────────────┘
                                 │
        ┌────────────────────────┴────────────────────────┐
        ▼                                                 ▼
 3. [ Payment Service Span (120ms) ]            4. [ Inventory Span (20ms) ]
    ┌───────────────────────────┐                 ┌─────────────────────────┐
    │ Parent Span ID: Order-01  │                 │ Parent Span ID: Order-01│
    │ Child: PG Call (100ms)    │                 │ Child: Redis Get (5ms)  │
    └───────────────────────────┘                 └─────────────────────────┘
```

선의 의미: Order Service(Root Span)에서 W3C 헤더를 전달받아 Payment와 Inventory가 각각 자식 Span을 생성하여 전체 트리를 완성하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 트레이스 식별자 (Trace ID) | 클라이언트 최초 요청부터 종료까지 **전체 분산 트랜잭션을 묶어주는 고유 UUID** |
| 스팬 (Span) | 마이크로서비스 내부의 **단일 작업 단위(HTTP 핸들러, DB 쿼리)의 시작/종료 시간 측정** |
| 부모 스팬 식별자 (Parent ID)| 호출자-피호출자 간의 **선후 인과관계를 정의하여 계층형 트리 그래프 조립** |
| 스팬 속성 (Attributes) | `http.status_code`, `db.statement` 등 **디버깅에 필요한 세부 문맥 메타데이터 보관** |
| 스팬 링크 (Span Links) | Kafka 비동기 큐처럼 **직접적 부모-자식이 아닌 다대다 메시지 연관 관계 연결** |

#### 한줄 요약

- Trace ID, Span, Parent Span ID, Attributes, Span Links가 결합하여 분산 호출 맵을 완성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **분산 추적 5단계 수명주기**: Root Span 생성 $\to$ W3C 헤더 주입 $\to$ 타깃 서비스 헤더 추출 $\to$ Child Span 생성 $\to$ 스팬 종료 및 백엔드 전송.

</details>

```text
[ 분산 추적 문맥 전파 및 스팬 수집 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 최초 진입점: Trace ID & Root Span 생성│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. HTTP 요청 헤더에 W3C traceparent 주입│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. 수신 서비스: HTTP 헤더에서 문맥 추출│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. Parent ID 연결하여 신규 Child Span 생성
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. 작업 종료 후 Span 백엔드(Tempo) 전송│
 └────────────────────────────────────────┘
```

### 동작 원리

1. Root Span 생성: API Gateway에 요청이 도달하면 신규 `Trace ID`와 `Root Span ID`를 생성.
2. 헤더 주입(Inject): 내부 백엔드 서비스를 호출하기 위해 HTTP 헤더에 `traceparent: 00-{traceId}-{spanId}-01`을 주입.
3. 헤더 추출(Extract): Order Service가 수신한 패킷의 헤더에서 상위 Trace ID와 부모 Span ID를 파싱.
4. Child Span 생성: 자신의 작업 구간을 측정할 `Child Span`을 생성하고 부모 ID를 링크.
5. 백엔드 전송: 연산이 완료되면 실행 시간(ms)과 에러 상태 코드를 기록한 뒤 OTel Collector를 거쳐 Tempo로 비동기 전송.

#### 한줄 요약

- Root Span 생성 $\to$ 헤더 주입 $\to$ 헤더 추출 $\to$ Child Span 생성 $\to$ 백엔드 전송의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Head Sampling vs Tail Sampling**: 요청 진입 시점 단순 확률 샘플링(Head)과 요청 완료 후 에러/지연 기반 조건부 샘플링(Tail).

</details>

| 구분 | 헤드 기반 샘플링 (Head Sampling) | 테일 기반 샘플링 (Tail Sampling) |
|:---|:---|:---|
| **적용 기준** | 대규모 트래픽에서 수집 오버헤드를 최소화하려는 환경 | 에러(500) 및 P99 지연 트레이스를 100% 누락 없이 수집하려는 환경 |
| **핵심 특징** | **최초 요청 진입 시 1% 무작위 수집 판정 (SDK 내장)** | **요청 완료 후 에러 여부를 보고 100% 선별 수집 (Collector)** |
| **한계** | 실제 장애가 발생한 에러 요청이 샘플링에서 탈락할 위험 | 수집기가 전 트레이스를 메모리에 임시 버퍼링하는 오버헤드 |

#### 한줄 요약

- 초저부하는 헤드 샘플링, 장애 분석 정확도는 테일 샘플링을 채택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **문맥 단절(Trace Context Loss)**: 멀티 스레드 비동기 처리나 Kafka 메시지 큐 통신 시 `traceparent` 헤더 전달이 누락되어 트레이스가 끊어지는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Kafka 메시지 브로커 경유 시 Trace ID 유실로 트레이스 단절 | **Kafka Producer/Consumer Record Header에 W3C Context 수동 주입** | 비동기 메시징 전 구간 E2E 추적 보장 |
| 하루 수억 건 트레이스 전량 저장으로 인한 스토리지 비용 파산 | **OTel Collector Tail Sampling (정상 1%, 에러 100% 저장)** | 저장소 비용 85% 이상 절감 |
| 비동기 멀티스레드(`CompletableFuture`) 전환 시 ThreadLocal 유실 | **`Context.wrap()` 또는 OTel Context 전파 래퍼(Wrapper) 적용** | 스레드 전환 시 문맥 유지 100% 달성 |

#### 한줄 요약

- Kafka 헤더 연동, 테일 샘플링 도입, 비동기 스레드 문맥 래핑을 통해 분산 추적의 정합성을 사수

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **분산 프로파일링 연계(Continuous Profiling Integration)**: 분산 트레이스 스팬에서 CPU Flame Graph 프로파일러로 원클릭 드릴다운하여 코드 라인 단위 병목을 찾는 기법.

</details>

- **분산 추적**은 마이크로서비스 아키텍처의 복잡성을 통제하고 장애 복구 시간을 획기적으로 줄이는 핵심 가시성 도구이며, W3C 표준 문맥 전파와 테일 기반 샘플링을 결합하여 완벽한 E2E 트랜잭션 추적성을 확보해야 함

#### 한줄 요약

- W3C Trace Context와 계층형 Span 트리를 통해 분산 시스템의 지연과 에러를 즉시 규명
