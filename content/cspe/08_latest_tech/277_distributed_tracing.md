---
title: "Distributed Tracing 분산 추적 (Distributed Tracing)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 277
extra:
  question_no: "277"
  exam_status: "기출"
  exam_history: "135회"
---

## 미리 알고가기

- 분산 추적은 하나의 사용자 요청이 여러 서비스와 인프라를 거치는 경로를 연결해 보는 관측 기법임
- trace와 span 관계를 이해하면 구조가 단순해짐
- 단순 로그 수집과 달리 인과 관계와 지연 기여도를 함께 보여준다는 점이 핵심임

## Ⅰ. 개요

- **정의/개념**: Distributed Tracing은 하나의 요청이나 트랜잭션이 여러 서비스와 데이터 저장소와 외부 시스템을 거치는 전 과정을 trace와 span 단위로 연결해 지연과 오류와 병목 경로를 추적하는 관측 기술임
- **배경/필요성**: 마이크로서비스 환경에서는 장애가 여러 서비스 경로에 분산되어 단일 로그나 단일 메트릭만으로 사용자 요청의 전체 흐름을 파악하기 어려워짐

## Ⅱ. 특징

- 요청 경로 전체를 시간 순서와 계층 구조로 시각화함
- 병목 서비스와 느린 구간을 빠르게 식별할 수 있음
- trace context 전파가 정확해야 분석 품질이 높아짐
- 모든 요청을 다 저장하면 비용과 저장량이 급증해 샘플링이 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Distributed Tracing | Logging | Metrics |
|:---|:---|:---|:---|
| 주 관심사 | 요청 경로와 인과 관계 | 상세 이벤트 기록 | 집계 수치 |
| 병목 위치 파악 | 높음 | 중간 | 낮음 |
| 저장 비용 | 중간 이상 | 높음 | 낮음 |
| 문맥 연결 | trace context 기반 | 로그 상관 필요 | 제한적 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Trace | 하나의 사용자 요청이나 작업 전체를 나타내는 최상위 추적 단위임 |
| Span | 각 서비스 호출이나 DB 질의처럼 trace 내부의 개별 작업 구간을 나타내는 세부 단위임 |
| Context Propagation | trace id와 span id를 서비스 간에 전달해 경로를 연결하는 문맥 전달 메커니즘임 |
| Tracing Backend | span을 저장하고 검색하고 시각화해 운영자가 병목을 분석하게 하는 백엔드 계층임 |
| Sampling Policy | 비용과 신호 품질을 균형화하기 위해 어떤 trace를 저장할지 결정하는 수집 정책임 |

```text
Trace A
  |
  +-- Span 1: API Gateway
  +-- Span 2: Service A
  |      +-- Span 3: DB Query
  +-- Span 4: Service B
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 요청 시작    | -> | context 생성 | -> | span 전파     | -> | backend 저장 | -> | 병목 분석    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **요청 시작**: 진입점에서 trace id를 생성함
2. **context 생성**: 첫 span과 메타데이터를 기록함
3. **span 전파**: 각 서비스 호출에 context를 전달함
4. **backend 저장**: 수집된 span을 저장소에 보냄
5. **병목 분석**: 호출 경로와 지연 구간을 시각화해 분석함

## Ⅵ. 문제점 및 해결 방안

1. 문제: trace context가 중간 서비스에서 끊기면 전체 호출 경로가 단절되어 병목 원인 분석 품질이 크게 떨어질 수 있음
   - 해결방안: propagation standard enforcement와 middleware instrumentation을 적용하고 trace continuity rate와 broken trace count로 검증함
2. 문제: 전량 수집은 저장 비용과 탐색 부하를 키워 오히려 운영 효율을 낮출 수 있음
   - 해결방안: adaptive sampling과 error priority retention을 적용하고 trace storage cost ratio와 critical trace retention rate로 검증함
3. 문제: 비동기 메시지와 배치 작업이 섞인 환경에서는 span 관계 모델이 모호해져 잘못된 경로 해석이 생길 수 있음
   - 해결방안: async trace model standard와 workflow correlation design을 적용하고 async trace reconstruction accuracy와 investigation lead time으로 검증함

## Ⅶ. 적용 사례

- API 플랫폼이 문맥 전파 표준을 강제하며 확인 지표는 trace continuity rate와 broken trace count임
- 대규모 서비스가 적응형 샘플링을 운영하며 확인 지표는 trace storage cost ratio와 critical trace retention rate임
- 이벤트 기반 시스템이 비동기 상관 설계를 적용하며 확인 지표는 async trace reconstruction accuracy와 investigation lead time임

## Ⅷ. 결론

분산 추적은 마이크로서비스 병목을 가장 직접적으로 보여주지만 문맥 전파와 샘플링과 비동기 경로 모델이 제대로 설계되어야 실효성이 높음.
