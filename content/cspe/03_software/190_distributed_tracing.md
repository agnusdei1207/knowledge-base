---
title: "분산 추적 (Distributed Tracing)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 190
---

# 📖 【암기용】 개념 완전 이해

> 목적: 분산 추적을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: **분산 추적(Distributed Tracing)**은 하나의 요청이 여러 서비스·DB를 거치는 경로를 **trace**와 **span**으로 기록해 지연·오류 발생 지점을 요청 단위로 찾는 관측 기법이다.
- **왜 필요한가**: 모놀리식은 로그 한 곳만 봐도 요청 흐름을 알 수 있지만, MSA는 API Gateway→서비스→큐→DB로 호출이 흩어져 로그 타임스탬프만으로는 어느 서비스가 병목인지 알 수 없다.
- **핵심 직관**: 택배 송장 번호 하나로 물류센터·차량·배송지 각 구간의 체류 시간을 이어붙여 보는 것과 같다.

## 핵심 용어 정리

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 분산 추적(Distributed Tracing) | 요청 경로를 서비스 경계를 넘어 추적하는 기법 — 이 개념의 정체성 | 송장 번호로 전체 배송 경로 조회 |
| Trace | 하나의 요청 전체를 나타내는 컨테이너(span들의 집합) | 배송 전체 여정 |
| Span | trace 안의 한 작업 구간(시작·종료 시각, 속성 포함) | 여정 중 한 구간(집하→터미널) |
| root span | 요청이 시작된 최초 span(보통 Gateway) | 최초 접수 지점 |
| child span / parent span | 상위 span이 호출한 하위 span, 그 상위 span | 상위 물류센터가 하위 배송기사에게 위탁 |
| trace_id | trace 전체를 식별하는 공통 키 | 송장 번호 |
| span_id / parent_id | span 자신의 ID와 자신을 호출한 span의 ID | 구간 코드와 이전 구간 코드 |
| Context Propagation | trace_id 등을 다음 서비스로 넘기는 것 | 환승할 때도 같은 송장 번호를 넘김 |
| traceparent(W3C Trace Context) | context propagation을 위한 표준 HTTP 헤더 형식 | 송장에 인쇄된 표준 바코드 |
| Sampling | 전체 trace 중 저장할 것을 고르는 정책 | 전수조사 대신 표본 조사 |
| Critical Path | 전체 지연을 결정하는, 병렬이 아닌 순차 구간의 합 | 여러 줄 중 가장 늦게 끝나는 줄 |

## 깊이 이해

### 로그만으로 부족한 이유 — 수치로 이해
- 주문 요청이 order-api → payment → fraud-db를 거친다고 하자. 각 서비스 로그의 타임스탬프만 보면 이 세 로그가 같은 요청에서 나왔는지 알 방법이 없다. 초당 수백 건이 겹치면 시간 순서로 짝짓는 것 자체가 불가능하다.
- trace_id라는 공통 키로 세 로그(정확히는 세 span)를 묶으면, 이 요청 하나에 대해 `order-api 40ms → payment 900ms → fraud-db 700ms`처럼 구간별 소요 시간을 정확히 재구성할 수 있다.

### span 계층 구조 — parent-child로 병목 찾기
- payment span(900ms) 안에 fraud-db span(700ms)이 child로 들어있다면, payment 자체 로직은 900-700=200ms만 쓰고 나머지 700ms는 DB 호출을 기다린 것이다. 즉 병목은 payment 서비스 코드가 아니라 fraud-db 쿼리다.
- 이런 부모-자식 관계를 시간축으로 늘어놓은 그림이 waterfall이며, 여러 서비스의 span을 노드로 그린 것이 service map이다.

### Critical Path — 병렬 구간은 지연에 안 더해진다
- 만약 payment가 fraud-db 조회와 inventory 조회를 병렬로 동시에 호출한다면(fraud-db 700ms, inventory 300ms), 전체 지연은 700+300=1000ms가 아니라 둘 중 더 오래 걸리는 700ms만 더해진다.
- Critical Path는 "병렬로 겹치는 구간을 제외하고, 실제로 전체 지연을 늘리는 순차 구간만 합산한 경로"다. 최적화 우선순위는 span 개수가 아니라 이 critical path 위에 있는 span부터 잡아야 한다.

### traceparent 형식과 전파 원리
- W3C Trace Context 표준 헤더 형식은 `버전-traceid(32자리 16진수)-spanid(16자리 16진수)-flags(2자리)`다. 예: `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`.
- order-api가 이 헤더를 만들어 payment 호출 시 HTTP 헤더로 실어 보내고, payment는 이를 받아 자신의 새 span_id를 만들되 같은 trace_id를 유지한 채 fraud-db 호출에도 실어 보낸다. 이 헤더가 큐(Kafka 등)를 거치는 비동기 구간에서 누락되면 trace가 그 지점에서 끊긴다(broken trace).

### Sampling — head vs tail, 왜 정책이 다른가
- head-based sampling: 요청이 시작되는 순간(root span 생성 시점)에 예컨대 1% 확률로 저장을 결정한다. 구현은 간단하지만, 문제가 된 느린 요청이 99% 확률로 우연히 누락될 수 있다.
- tail-based sampling: 요청이 끝난 뒤 "에러였다", "p95 300ms를 넘었다" 같은 조건을 보고 그 trace만 우선 저장한다. 초당 10,000건 중 정상 요청은 1%만 남기고, 문제 있는 요청은 100% 남기는 식으로 저장 비용은 줄이면서 정작 필요한 trace는 놓치지 않는다. 대신 요청이 끝날 때까지 Collector가 span을 버퍼링해야 해서 자원 부담이 더 크다.

### 비유와 흔한 오해
- **비유**: 병원 진료에서 접수번호 하나로 접수·검사·진료·수납 각 단계의 대기 시간을 모두 조회할 수 있는 것과 같다. 각 부서 기록을 따로 보면 어느 단계에서 환자가 오래 기다렸는지 맞추기 어렵다.
- **오해**: 트레이스가 로그를 대체하지 않는다. 트레이스는 "어디서, 얼마나" 걸렸는지(경로와 시간)를 보여줄 뿐, 실패의 구체적 원인(에러 메시지, 스택트레이스)은 여전히 trace_id로 연결된 로그에서 찾아야 한다.

## 연결 개념
- OpenTelemetry — trace/span을 생성하고 전파하는 표준 SDK·프로토콜(189에서 상세)
- Cloud Native Observability — 트레이스가 메트릭·로그와 함께 이루는 3대 신호 중 하나(188에서 상세)
- SRE — SLO 위반 요청을 trace로 원인 분석하는 운영 활용(191에서 상세)

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 분산 추적 답안은 trace/span 구조, context propagation, sampling, 로그 상관, SLO 분석을 연결해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Distributed Tracing은 하나의 요청을 trace ID로 묶고 서비스별 처리 구간을 span으로 기록해 분산 호출 경로와 지연을 분석하는 기법임.
> 2. **가치**: p95 latency와 error trace를 서비스·DB·외부 API span으로 분해해 장애 원인 탐색 시간을 30분에서 10분 이하로 줄이는 근거를 제공함.
> 3. **판단 포인트**: W3C Trace Context, sampling 전략, span attribute, trace-log correlation, coverage, 저장 비용을 기준으로 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 분산 시스템 장애 분석 이해 확인 | trace, span, parent-child, propagation | 로그 수집과 동일시 |
| 표준 적용 확인 | traceparent, tracestate, OpenTelemetry | proprietary header만 언급 |
| 운영 판단 확인 | sampling, coverage, storage cost, PII | 모든 요청 100% 저장 주장 |

> 요약: 이 문제는 요청 경로 분석 구조와 비용·개인정보 통제를 함께 제시해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 요청 경로 분석 기법
- 배경: MSA와 클라우드 네이티브 환경은 요청이 여러 서비스와 비동기 큐를 통과한다.
- 필요성: trace_id, span_id, parent_id로 지연·오류 발생 구간을 요청 단위로 식별한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client Request -> Trace Context -> Service Span -> DB/External Span -> Trace Backend
  / Correlation: trace_id, span_id, parent_id
  / Control: sampling, attribute, retention
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Trace | 요청 전체 경로 식별 | trace_id로 묶음 |
| Span | 서비스 또는 작업 단위 구간 | start/end time, attribute |
| Context Propagation | 서비스 간 문맥 전달 | W3C traceparent |
| Trace Backend | 저장, 검색, service map 제공 | Jaeger, Tempo, Zipkin |

> 요약: 분산 추적은 trace, span, context propagation, backend로 요청 경로와 지연을 구조화함.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> trace_id 생성/추출 -> root span 생성 -> child span 전파 -> backend export -> service map 분석
  / 오류 발생 -> error span 표시
  / sampling 제외 -> metric만 유지
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | gateway 또는 첫 서비스가 trace ID 생성 | traceparent 생성률 |
| 2 | 서비스 호출마다 child span 생성 | span attribute 표준 준수 |
| 3 | HTTP/gRPC/Queue header로 context 전파 | propagation success |
| 4 | Collector가 sampling 후 backend 저장 | sampled trace 비율 |
| 5 | waterfall과 service map으로 병목 분석 | p95 span latency |

> 요약: 분산 추적은 문맥 전파와 span 계층을 통해 서비스별 지연과 오류를 요청 단위로 분석함.

---

## Ⅳ. 특징

| 구분 | 로그 중심 분석 | 분산 추적 | 수치/판단 포인트 |
|:---|:---|:---|:---|
| 분석 단위 | 이벤트 행 | 요청 경로 | trace_id 기반 |
| 시간 관계 | 수동 정렬 | span waterfall | critical path 확인 |
| 적용 범위 | 서비스별 로그 | 서비스 간 호출 | trace coverage 95% |
| 비용 | 로그량 중심 | span 수와 sampling | tail sampling 정책 |

> 요약: 분산 추적은 로그보다 요청 경로와 시간 관계를 파악하는 데 적합하며 sampling과 저장 비용을 설계해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 중앙 로그 분석 | trace/span graph | MSA 호출 깊이 3단계 이상 |
| 비용/처리 | 전체 로그 보관 | head/tail sampling | 월 span 저장 예산 |
| 운영/위험 | 장애 후 수동 추정 | SLO 위반 trace 분석 | MTTR 단축 목표 |

> 요약: 서비스 호출 깊이가 깊고 SLO 위반 원인 분석이 필요하면 분산 추적을 우선 적용함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 추적 단절 | header 전파 누락 | W3C Trace Context 표준화 | broken trace 비율 |
| 비용 증가 | 모든 요청 저장 | tail sampling, retention | ingest span count |
| 개인정보 노출 | span attribute 과다 | attribute denylist, masking | PII 검출 0건 |

> 요약: 분산 추적 리스크는 전파 단절, 저장 비용, 개인정보 노출을 기준으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 적용 | trace coverage 95% 이상 | backend service map |
| 품질 | broken trace 1% 이하 | trace validation |
| 운영 | MTTR 10분 이하 | incident record |

> 요약: 분산 추적 품질은 coverage, broken trace, MTTR로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 전파 표준화: HTTP, gRPC, Kafka 메시지에 W3C `traceparent`를 적용하고 gateway에서 trace ID를 생성
2. 계측 적용: OpenTelemetry auto instrumentation으로 기본 span을 만들고 결제, 주문, 인증은 manual span attribute를 추가
3. 비용·보안 통제: tail sampling, 30일 retention, PII attribute denylist, trace coverage 95% 이상을 운영 기준으로 설정

**결론 (2줄):**
- 기술사 판단: MSA 호출 깊이 3단계 이상이고 p95 지연 원인 분석이 필요하면 분산 추적을 필수 관측 신호로 채택함
- 향후 방향: OpenTelemetry, eBPF auto-instrumentation, exemplars가 metric과 trace 상관 분석을 확장함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "분산 추적을 설명하시오", "기술하시오" | trace ID, span, context propagation 흐름 | 로그 중심 분석 대비 요청 경로 분석 |
| 요구사항 명시형 | "MSA 장애 분석 방안을 제시하시오", "설계하시오" | W3C 전파, sampling, backend 설계 | coverage, broken trace, MTTR 기준 |

> 요약: 설명형은 trace/span 원리, 운영형은 장애 분석 지표와 비용 통제 중심으로 전환함.
