---
sidebar:
  order: 163
  label: "163. 분산 추적 (Distributed Tracing)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "분산 추적 (Distributed Tracing)"
date: "2026-08-14T02:44:00+09:00"
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

- **분산 추적(Distributed Tracing)**: 요청 경로의 모든 구간을 단일 ID로 묶어 지연(Latency)과 에러 지점을 추적하는 기술.
- **Trace & Span**: **Trace**는 1개 요청의 전체 라이프사이클 식별자이며, **Span**은 서비스 내부의 실행 구간 단위.
- **문맥 전파(Context Propagation)**: A가 B를 호출할 때 헤더에 `trace_id`를 실어 추적 고리를 연결하는 기술.

</details>

- 정의/개념: 요청의 Service별 Span을 연결하는 **Distributed Tracing**
- 배경/필요성: 분산 호출은 단일 Log만으로 **호출 경로•지연 구간** 식별 불가

#### 한줄 요약

- 주문 하나에 같은 추적 번호를 붙이면 결제와 재고 서비스에 흩어진 처리 기록을 한 이동 경로로 이어 가장 오래 멈춘 구간을 찾을 수 있다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Parent-Child Span Relationship**: Span 간의 선후 종속 관계를 나타내는 구조로, 부모 Span이 여러 자식 Span(병렬 쿼리)을 품는 트리(Tree) 토폴로지.

</details>

- **추적 ID 주입(Trace ID Injection)**: 모든 요청에 글로벌 고유 식별자 주입.
- **문맥 전파**: HTTP 헤더 기반 W3C Trace Context 규약 전파.
- **계층 시각화**: Jaeger/Tempo 기반 계층형 트리 지연 시각화.

#### 한줄 요약

- 같은 추적 번호만으로는 순서를 알 수 없으므로 각 스팬의 부모 정보를 함께 기록하고 비동기 작업은 스팬 링크로 인과관계를 남긴다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **W3C Trace Context**: HTTP 헤더 표준 규약(`traceparent: 00-4bf92f3...-01`)으로 벤더 종속 없이 추적 문맥을 호환 이관하는 W3C 글로벌 표준.

</details>

```text
[Trace]
 ├── [Trace ID]
 └── [Span]
      ├── [Span ID•Parent Span ID]
      └── [Span Attributes]
```

| 구성요소 | 책임 |
|---|---|
| Trace ID | 전체 요청의 **공통 상관 Key** 제공 |
| Span ID | Service 내 **작업 구간** 식별 |
| Parent Span ID | 동기 호출의 **부모•자식 관계** 연결 |
| Span Attributes | Protocol•상태•지연 등 **진단 문맥** 기록 |

#### 한줄 요약

- 트레이서가 구간 영수증을 만들고 문맥 전파기가 같은 주문 번호와 이전 구간 번호를 넘기면 백엔드가 영수증을 전체 동선으로 조립한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Head Sampling vs Tail Sampling**: 최초 요청 진입 시 10%만 수집 결정(Head)할 것인지, 끝까지 실행 후 에러(500)난 것만 100% 수집(Tail)할 것인지 결정하는 보존 전략.

</details>

```text
[분산 요청]
    │
    ▼
1. Trace•Root Span 생성
    │
    ▼
2. Context Header 주입
    │
    ▼
3. 다음 Service에서 추출
    │
    ▼
4. Child Span 생성•전파
    │
    ▼
5. Span 종료•전송
    │
    ▼
[Trace 조립 결과]
```

### 동작 원리

1. **Trace•Root Span 생성**: 최초 요청의 Trace Context 시작
2. **Context Header 주입**: W3C Trace Context를 호출에 포함
3. **다음 Service에서 추출**: 전달된 Trace•Parent 정보 복원
4. **Child Span 생성•전파**: 현재 작업 기록과 하위 호출 연결
5. **Span 종료•전송**: 상태•지연을 기록해 Backend 전달

#### 한줄 요약

- 서비스 A가 자신의 스팬 번호를 부모로 넣어 B를 호출하면 두 서비스가 따로 보낸 기록도 백엔드에서 A 다음 B 순서로 연결된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Sampling Rate (샘플링 비율)**: 수백만 건의 트래픽을 모두 저장하면 스토리지 비용이 폭증하므로, 1% 또는 10%의 대표 트레이스만 선별 저장하는 아키텍처.

</details>

| 비교 항목 | Head Sampling (헤드 샘플링) | Tail Sampling (테일 샘플링) |
|:---|:---|:---|
| 결정 시점 | **트래픽 진입 시점 (최초 인그레스)**| **요청이 끝까지 모두 완료된 후 후행 판정** |
| 핵심 목적 | 비용 절감을 위해 무작위 1%만 수집 | **정상 1%, 지연/오류(500) 100% 선별 수집** |
| 시스템 부하 | 매우 낮음 (안 뽑힌 요청은 즉시 버림)| 높음 (모든 데이터를 메모리에 들고 있다가 버림) |
| 실무 적용 | OTel SDK 기본 내장 설정 | **OTel Collector 중앙 메모리 버퍼링 필요** |

#### 한줄 요약

- 헤드 샘플링은 입장할 때 임의 관객을 고르고 테일 샘플링은 공연이 끝난 뒤 사고나 지연이 있던 관객 기록을 남기는 차이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Trace Context Broken (문맥 단절)**: Kafka 비동기 큐나 외부 Legacy 시스템을 지날 때 `trace_id` 헤더가 날아가 트레이스가 2동강으로 단절되는 파행.

</details>

| 3대 분산 추적 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Trace Context Broken | Kafka Message Produce 시 헤더 복사 누락| **Kafka Record Header에 W3C Context 수동 주입** |
| 2. Storage Cost Explosion | 하루 1억 건 트레이스 100% 저장 (ES 파산)| **Tail Sampling 도입하여 Error 위주 선별 저장** |
| 3. High Cardinality Tags | Span Attribute에 UUID, 이메일을 난사함 | **PII 정보는 OTel Processor에서 마스킹/Drop 처리**|

> 사례: **카카오 / 당근마켓 Spring Sleuth/Micrometer 연동 및 Kafka 비동기 Trace 연결 아키텍처**

#### 한줄 요약

- 메시지 생산과 소비는 실행 시점이 떨어져 직접 부모 관계가 왜곡될 수 있으므로 전달 문맥과 스팬 링크를 함께 남겨야 한다.

## Ⅶ. 결론

- 저비용 예측 Sampling은 **Head**, 오류 보존은 Tail 선택

#### 한줄 요약

- 모든 동기•비동기 경계에서 문맥을 전파하고 오류•지연 Trace가 남도록 Sampling한다.
