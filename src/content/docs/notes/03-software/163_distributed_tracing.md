---
sidebar:
  order: 163
  label: "163. 분산 추적"
  badge:
    text: "기출 · 50%"
    variant: note
title: "분산 추적 (Distributed Tracing)"
date: "2026-08-25T11:00:00+09:00"
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

- **분산 추적(Distributed Tracing)**: 사용자 요청이 마이크로서비스 간에 이동하는 전 과정을 Trace ID와 Span 계층 트리로 추적하는 기술.
- **Trace & Span**: 단일 요청 전체를 관통하는 고유 식별자(Trace)와 각 서비스 내부의 개별 작업 구간 단위(Span).

</details>

- 정의/개념: 분산 환경에서 단일 요청의 전체 이동 경로를 **Trace ID와 스팬(Span) 계층 트리로 시각화하여 지연 구간과 장애 병목을 추적하는 기술**
- 배경/필요성: 수십 개 마이크로서비스 간 비동기 RPC 호출 환경에서 **단일 서버 로컬 로그 기반의 트랜잭션 흐름 추적 불가 및 병목 식별 불가 해결 불가**

#### 한줄 요약
- Trace ID와 부모-자식 Span 계층 구조를 통해 마이크로서비스 간 호출 흐름과 지연 병목을 시각화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **W3C Trace Context**: `traceparent` HTTP 헤더를 통해 서비스 경계를 넘어 Trace ID와 Parent Span ID를 전파하는 표준 규격.
- **Context Propagation**: 스레드, 프로세스, 네트워크 경계를 넘어 트레이스 문맥을 주입(Inject)하고 추출(Extract)하는 메커니즘.

</details>

- 단일 트랜잭션 전체를 관통하는 **글로벌 고유 Trace ID 기반 상관 추적**
- 서비스 간 호출 선후 관계 및 실행 시간을 나타내는 **Parent-Child Span 계층 트리**
- W3C 표준 HTTP 헤더를 통해 비동기 큐와 RPC를 넘나드는 **문맥 전파(Context Propagation)**

#### 한줄 요약
- 분산 서비스 간의 호출 인과관계와 밀리초 단위 지연시간을 투명하게 시각화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Span 트리 5대 메타데이터**: Trace ID(트랜잭션 고유값), Span ID(현재 작업 ID), Parent Span ID(호출자 ID), Attributes(Key-Value 속성), Events(타임스탬프 로그).

</details>

```text
[분산 추적 Trace 및 계층형 Span 트리 구조]
|-- Trace ID: `4bf92f3577b34da6a3ce929d0e0e4736` (전체 트랜잭션 고유 UUID)
|   |-- 1. [Root Span: API Gateway (200ms)] -> Parent ID: null
|   |   |-- 2. [Child Span A: Order Service (180ms)] -> Parent ID: Gateway
|   |   |   |-- 3. [Child Span A-1: Payment Service (120ms)] -> Parent ID: Order
|   |   |   |   `-- [Child Span A-1-a: DB Query Call (100ms)]
|   |   |   `-- 4. [Child Span A-2: Inventory Service (20ms)] -> Parent ID: Order
|   |   |       `-- [Child Span A-2-a: Redis Get (5ms)]
|   `-- Span Attributes: `http.method=POST`, `http.status_code=200`, `db.statement`
```

선의 의미: 계층 및 Root Span에서 W3C 헤더를 전달받아 Payment와 Inventory가 각각 자식 Span을 생성하여 트리를 완성하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **트레이스 식별자 (Trace ID)**| 클라이언트 최초 요청부터 종료까지 **전체 분산 트랜잭션을 묶어주는 고유 UUID** | 전 구간 공유 |
| **스팬 (Span)** | 마이크로서비스 내부의 **단일 작업 단위(HTTP 핸들러, DB 쿼리)의 시작/종료 시간 측정**| 시작/종료 ms 타임스탬프 |
| **부모 스팬 식별자 (Parent ID)**| 호출자-피호출자 간의 **선후 인과관계를 정의하여 계층형 트리 그래프 조립** | DAG 트리 구성 |
| **스팬 속성 (Attributes)** | `http.status_code`, `db.statement` 등 **디버깅에 필요한 세부 문맥 메타데이터 보관** | Key-Value 태그 |
| **스팬 링크 (Span Links)** | Kafka 비동기 큐처럼 **직접적 부모-자식이 아닌 다대다 메시지 연관 관계 연결** | 비동기 연계 |

#### 한줄 요약
- Trace ID, Span, Parent Span ID, Attributes, Span Links가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **분산 추적 문맥 전파 5단계**: Root Span 생성 $\to$ W3C 헤더 주입 $\to$ 타깃 서비스 헤더 추출 $\to$ Child Span 생성 $\to$ 백엔드 전송.

</details>

```text
외부 클라이언트의 주문 API 호출 발생
        │
   1. [Root Span 생성] API Gateway가 최초 진입점에서 Trace ID와 Root Span ID 생성
        │
   2. [헤더 주입 (Inject)] Order Service 호출 HTTP 헤더에 `traceparent` 규격 주입
        │
   3. [헤더 추출 (Extract)] Order Service가 수신한 패킷의 헤더에서 Trace ID와 부모 ID 파싱
        │
   4. [Child Span 생성] Order 내부 비즈니스 로직을 위한 Child Span을 생성하고 부모 ID 연결
        │
   5. 작업 종료 후 Span 실행 시간(180ms)을 기록하고 OTel Collector를 거쳐 Tempo로 비동기 전송
```

#### 한줄 요약
- Root Span 생성 → 헤더 주입 → 헤더 추출 → Child Span 생성 → 백엔드 전송 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Head Sampling vs Tail Sampling**: 요청 진입 시점 단순 확률 샘플링(Head)과 요청 완료 후 에러/지연 기반 조건부 선별 샘플링(Tail).

</details>

| 비교 항목 | 헤드 기반 샘플링 (Head Sampling) | 테일 기반 샘플링 (Tail Sampling) |
|:---|:---|:---|
| 샘플링 결정 시점 | **최초 요청 진입 시점 (Ingress/SDK)** | **전체 트랜잭션 요청 완료 시점 (Collector)** |
| 핵심 동작 방식 | **무작위 1% 확률 기반 수집 결정** | **응답 코드(500) 및 P99 지연시간 기준 선별** |
| 에러 트레이스 보존 | 실제 장애 에러 요청이 누락될 위험 존재 | **에러 및 비정상 지연 트레이스 100% 보존** |
| 인프라 오버헤드 | **최소 (수집기 메모리 버퍼링 불필요)** | 중간 (수집기 메모리에 트레이스 임시 버퍼링) |

#### 한줄 요약
- 초저부하는 헤드 샘플링, 장애 분석 정확도는 테일 샘플링을 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Context Loss**: 멀티 스레드 비동기 처리나 Kafka 메시지 큐 통신 시 `traceparent` 헤더 전달이 누락되어 트레이스가 끊어지는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Kafka 메시지 브로커 경유 시 Trace ID 유실로 트레이스 단절 | **Kafka Producer/Consumer Record Header에 W3C Context 수동 주입** | 비동기 메시징 전 구간 E2E 추적 보장 |
| 하루 수억 건 트레이스 전량 저장으로 인한 스토리지 비용 폭증 | **OTel Collector Tail Sampling (정상 1%, 에러 100% 저장)** | 저장소 비용 85% 이상 절감 |
| 비동기 멀티스레드(`CompletableFuture`) 전환 시 ThreadLocal 유실 | **`Context.wrap()` 또는 OTel Context 전파 래퍼(Wrapper) 적용** | 스레드 전환 시 문맥 유지 100% 달성 |
| 수십 개 서비스 간 시계 불일치로 인한 스팬 순서 왜곡 | **NTP(Chrony) 클러스터 동기화로 노드 간 시간 오차 1ms 이내 유지** | 스팬 인과관계 정확도 100% 확보 |

#### 한줄 요약
- Kafka 헤더 연동, 테일 샘플링 도입, 비동기 스레드 문맥 래핑, NTP 동기화로 정합성을 확보한다.

## Ⅶ. 결론

- 마이크로서비스 아키텍처의 분산 지연과 에러 병목을 신속히 규명하기 위해 **W3C Trace Context 기반의 OpenTelemetry 분산 추적을 전사 표준으로 구축**하고, **Grafana Tempo와 Tail-based Sampling**을 결합하여 고효율·저비용의 엔드투엔드 분산 가시성 완성

#### 한줄 요약
- 분산 추적은 W3C Trace Context와 계층형 Span 트리를 통해 마이크로서비스 간 호출 흐름과 지연 병목을 투명하게 시각화하는 핵심 관측성 기술이다.