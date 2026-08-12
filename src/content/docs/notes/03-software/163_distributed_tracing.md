---
sidebar:
  order: 163
  label: "163. 분산 추적 (Distributed Tracing)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "분산 추적 (Distributed Tracing)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **Distributed Tracing (분산 추적)**: 1개의 사용자 요청이 수십 개의 MSA(마이크로서비스)를 넘나들 때, 모든 체인 구간을 단일 ID로 묶어 지연(Latency)과 에러(Error)의 정확한 발생 지점을 추적하는 Observability 핵심 기술.
- **Trace & Span**: **Trace**는 1개 요청의 전체 처음~끝 라이프사이클을 묶는 최상위 식별자이고, **Span**은 해당 요청이 거쳐 간 개별 마이크로서비스 내부의 실행 구간 단위.
- **Trace Context Propagation**: A 서비스가 B 서비스를 HTTP/gRPC로 호출할 때 헤더(Header)에 `trace_id`를 실어 보내어 추적 고리를 끊기지 않게 연결하는 문맥 전파 기술.

</details>

- 정의/개념: MSA 분산 환경에서 단일 유저 요청(Trace)이 여러 서비스 구간(Span)을 이동하는 경로와 소요 시간을 시각화하고 병목 구간을 핀포인트 추론하는 **Distributed Tracing**
- 배경/필요성: 모놀리식(Monolithic) 시스템과 달리, MSA 환경에서는 "결제가 5초 지연됨"이라는 현상만으로 10개 중 어떤 서비스(DB, API, Auth)가 병목인지 파악이 불가능한 한계성 극복

#### 한줄 요약

- 주문 하나에 같은 추적 번호를 붙이면 결제와 재고 서비스에 흩어진 처리 기록을 한 이동 경로로 이어 가장 오래 멈춘 구간을 찾을 수 있다.

## Ⅱ. 특징 (분산 추적 3대 렌더링 메커니즘)

<details><summary>핵심 용어</summary>

- **Parent-Child Span Relationship**: Span 간의 선후 종속 관계를 나타내는 구조로, 부모 Span이 여러 자식 Span(병렬 쿼리)을 품는 트리(Tree) 토폴로지.

</details>

- **Trace ID Injection (모든 요청에 글로벌 고유 식별자 Trace ID 최초 주입)**
- **Context Propagation (HTTP Header 기반 W3C Trace Context 규약 전파)**
- **Waterfall Visualization (Jaeger/Tempo UI 기반 계층형 트리 폭포수 지연 시각화)**

#### 한줄 요약

- 같은 추적 번호만으로는 순서를 알 수 없으므로 각 스팬의 부모 정보를 함께 기록하고 비동기 작업은 스팬 링크로 인과관계를 남긴다.

## Ⅲ. 구조 및 구성요소 (W3C Trace Context 데이터 아키텍처)

<details><summary>핵심 용어</summary>

- **W3C Trace Context**: HTTP 헤더 표준 규약(`traceparent: 00-4bf92f3...-01`)으로 벤더 종속 없이 추적 문맥을 호환 이관하는 W3C 글로벌 표준.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Distributed Tracing Tree Structure                   │
├────────────────────────────────────────────────────────────────────────┤
│ Trace ID: 9f8a... (Total: 1.5s)                                        │
│  ├── [Span A] Frontend API (Parent) ....................... 1.5s       │
│  │    ├── [Span B] Auth Service (Child) ........ 0.3s                  │
│  │    └── [Span C] Order Service (Child) ................. 1.1s (병목) │
│  │         └── [Span D] DB Query (Grandchild) ..... 0.8s               │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 1개의 Trace가 최상위 Span A에서 시작하여 B, C를 거치고, 최종 DB Span D에서 소요된 트리 형태의 지연 폭포수 구조.

| 핵심 구성요소 | 데이터 스키마 역할 | 실무 기술 속성 |
|:---|:---|:---|
| **Trace ID** | **전체 요청 흐름을 묶는 1개의 최상위 글로벌 Key** | `trace_id: 128-bit` |
| **Span ID** | **각 MSA 서비스 내 단위 작업 구간 식별자** | `span_id: 64-bit` |
| **Parent Span ID**| **이전 호출 서비스의 Span ID를 저장 (트리 구조 연결)** | `parent_id` 맵핑 |
| **Span Attributes**| **상세 문맥 (HTTP Method, Status Code, DB 쿼리 문장)**| Key-Value Tag 저장 |

#### 한줄 요약

- 트레이서가 구간 영수증을 만들고 문맥 전파기가 같은 주문 번호와 이전 구간 번호를 넘기면 백엔드가 영수증을 전체 동선으로 조립한다.

## Ⅳ. 흐름도 (HTTP 헤더 기반 Context Propagation 흐름)

<details><summary>핵심 용어</summary>

- **Head Sampling vs Tail Sampling**: 최초 요청 진입 시 10%만 수집 결정(Head)할 것인지, 끝까지 실행 후 에러(500)난 것만 100% 수집(Tail)할 것인지 결정하는 보존 전략.

</details>

```text
[User Request] ──► [Frontend App] (생성: Trace ID=1, Span ID=A)
                           │
                           ▼ (HTTP Header 전파: trace_id=1, parent_id=A)
                   [Backend API] (생성: Trace ID=1, Span ID=B)
                           │
                           ▼ (HTTP Header 전파: trace_id=1, parent_id=B)
                   [Database Query] (생성: Trace ID=1, Span ID=C)
```

### 동작 원리

1. **Initial Inject**: Frontend 앱에서 Trace ID `1`과 자기 Span ID `A` 신규 생성.
2. **Header Propagation**: Backend API 호출 시 HTTP Request Header에 해당 ID를 싣어 `Context Propagation` 수행.
3. **Child Span Extract**: Backend가 헤더를 Extract하여 부모를 `A`로 둔 Span `B`를 생성하고 최종 백엔드(Jaeger)로 전송 (**Distributed Tracing 완결**).

#### 한줄 요약

- 서비스 A가 자신의 스팬 번호를 부모로 넣어 B를 호출하면 두 서비스가 따로 보낸 기록도 백엔드에서 A 다음 B 순서로 연결된다.

## Ⅴ. 종류 및 비교 (Head Sampling 대 Tail Sampling 샘플링 전략 비교)

<details><summary>핵심 용어</summary>

- **Sampling Rate (샘플링 비율)**: 수백만 건의 트래픽을 모두 저장하면 스토리지 비용이 폭증하므로, 1% 또는 10%의 대표 트레이스만 선별 저장하는 아키텍처.

</details>

| 비교 항목 | Head Sampling (헤드 샘플링) | Tail Sampling (테일 샘플링) |
|:---|:---|:---|
| **결정 시점** | **트래픽 진입 시점 (최초 인그레스)**| **요청이 끝까지 모두 완료된 후 후행 판정** |
| **핵심 목적** | 비용 절감을 위해 무작위 1%만 수집 | **정상 1%, 지연/오류(500) 100% 선별 수집** |
| **시스템 부하** | 매우 낮음 (안 뽑힌 요청은 즉시 버림)| 높음 (모든 데이터를 메모리에 들고 있다가 버림) |
| **실무 적용** | OTel SDK 기본 내장 설정 | **OTel Collector 중앙 메모리 버퍼링 필요** |

#### 한줄 요약

- 헤드 샘플링은 입장할 때 임의 관객을 고르고 테일 샘플링은 공연이 끝난 뒤 사고나 지연이 있던 관객 기록을 남기는 차이다.

## Ⅵ. 실무 고려사항 및 대책 (분산 추적 3대 장애 대책)

<details><summary>핵심 용어</summary>

- **Trace Context Broken (문맥 단절)**: Kafka 비동기 큐나 외부 Legacy 시스템을 지날 때 `trace_id` 헤더가 날아가 트레이스가 2동강으로 단절되는 파행.

</details>

| 3대 분산 추적 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Trace Context Broken** | Kafka Message Produce 시 헤더 복사 누락| **Kafka Record Header에 W3C Context 수동 주입** |
| **2. Storage Cost Explosion**| 하루 1억 건 트레이스 100% 저장 (ES 파산)| **Tail Sampling 도입하여 Error 위주 선별 저장** |
| **3. High Cardinality Tags** | Span Attribute에 UUID, 이메일을 난사함 | **PII 정보는 OTel Processor에서 마스킹/Drop 처리**|

> 사례: **카카오 / 당근마켓 Spring Sleuth/Micrometer 연동 및 Kafka 비동기 Trace 연결 아키텍처**

#### 한줄 요약

- 메시지 생산과 소비는 실행 시점이 떨어져 직접 부모 관계가 왜곡될 수 있으므로 전달 문맥과 스팬 링크를 함께 남겨야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Distributed Tracing 수립 기준(Tracing Standards)**: W3C Trace Context 표준, Tail Sampling 최적화, OTel SDK 및 Jaeger/Tempo 시각화에 의거한 체계.

</details>

- **Distributed Tracing 수립 기준**에 따라 Cloud-Native MSA 병목 관제 시 **OpenTelemetry Tracing & Tail Sampling** 필수 적용

#### 한줄 요약

- 동기 호출은 부모·자식 관계를 끝까지 전파하고 비동기 작업은 링크를 사용하며 희귀 장애는 테일 샘플링으로 보존해야 한다.
