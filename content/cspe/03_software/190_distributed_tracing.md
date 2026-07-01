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
- **개요**: 하나의 요청이 여러 서비스와 DB를 지나가는 경로를 trace와 span으로 기록하는 관측 기법
- **왜 필요한가**: MSA에서는 사용자가 경험한 지연과 오류가 어느 서비스, 어느 호출, 어느 쿼리에서 발생했는지 요청 단위로 확인해야 한다.
- **핵심 직관**: 택배 송장 번호 하나로 물류센터, 차량, 배송지까지 이동 경로와 체류 시간을 보는 방식이다.

## 깊이 이해
- **배경·문제의식**: 모놀리식은 로그 한곳으로도 요청 흐름을 볼 수 있지만, MSA는 API Gateway, 서비스, 메시지 큐, DB가 분산되어 로그만으로 시간 순서를 맞추기 어렵다.
- **작동 원리**: 최초 요청에서 trace ID를 만들고 각 서비스 호출을 span으로 기록한다. W3C Trace Context의 `traceparent` header가 서비스 간 문맥을 전달한다.
- **비유**: 병원 진료에서 접수, 검사, 진료, 수납 단계마다 같은 접수번호를 찍어 어느 단계에서 대기 시간이 길었는지 보는 구조이다.
- **구체 예시**: 주문 요청 trace에서 `order-api 40ms`, `payment 900ms`, `fraud-db 700ms`가 보이면 결제 서비스 내부 DB span이 p95 지연 원인으로 식별된다.
- **흔한 오해·주의점**: trace가 모든 로그를 대체하지 않는다. trace는 경로와 지연을 보여주고, 로그는 오류 상세와 데이터 맥락을 제공하므로 trace ID로 연결해야 한다.

## 연결 개념
- OpenTelemetry - trace 생성과 전송 표준
- W3C Trace Context - traceparent, tracestate 전파 규격
- SRE - SLO 위반 요청 원인 분석

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

분산 추적은 요청 경로 분석 기법임. MSA와 클라우드 네이티브 환경은 요청이 여러 서비스와 비동기 큐를 통과한다. trace와 span을 통해 어느 구간에서 지연·오류가 발생했는지 요청 단위로 식별해야 한다.

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

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
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
