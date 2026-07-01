---
title: "미들웨어 - ESB·MOM·Message Broker (Middleware ESB MOM)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 299
---

# 📖 【암기용】 개념 완전 이해

> 목적: 미들웨어 ESB·MOM·Message Broker를 처음 봐도 완전히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 서로 다른 애플리케이션 사이에서 메시지 전달, 변환, 라우팅, 비동기 처리를 제공하는 중간 계층
- **왜 필요한가**: 시스템이 직접 1:1로 연결되면 인터페이스 수가 폭증하고 장애가 전파되며 변경 영향 분석이 어려워진다.
- **핵심 직관**: 모든 부서가 서로 직접 전화하지 않고 우편실·교환대·택배 시스템을 통해 문서를 전달하는 구조이다.

## 깊이 이해
- **배경·문제의식**: 기업 시스템은 ERP, CRM, 결제, 물류처럼 플랫폼과 데이터 형식이 다르다. 직접 연동은 `n(n-1)/2` 수준으로 연결 수가 늘어난다.
- **작동 원리**: ESB는 중앙 버스에서 변환·라우팅·오케스트레이션을 수행한다. MOM은 큐 기반 비동기 메시징을 제공한다. Message Broker는 topic·queue로 publish/subscribe와 consumer group 처리를 제공한다.
- **비유**: ESB는 중앙 교환대, MOM은 우편함, Message Broker는 구독자가 있는 뉴스 배포 시스템에 가깝다.
- **구체 예시**: 주문 서비스가 Kafka topic `order.created`에 이벤트를 발행하면 재고, 배송, 알림 서비스가 각자 소비하고 실패 시 retry·DLQ로 분리한다.
- **흔한 오해·주의점**: ESB가 모든 통합 문제의 답은 아니다. 중앙 집중이 심하면 병목과 변경 승인 지연이 생기며, 이벤트 기반 MSA에서는 broker 중심 분산 통합이 더 적합할 수 있다.

## 연결 개념
- EAI - 기업 애플리케이션 통합
- Event-Driven Architecture - 이벤트 발행·구독 기반 비동기 구조
- Saga Pattern - 분산 트랜잭션 보상 처리

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. ESB·MOM·Broker의 역할 차이와 선택 기준을 중심으로 답한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 미들웨어는 이기종 시스템 간 통신·변환·라우팅·비동기 처리를 제공하는 통합 계층이다.
> 2. **가치**: 직접 연동 수를 줄이고 큐·토픽·라우팅으로 장애 격리, 처리량 완충, 변경 영향 축소를 수행한다.
> 3. **판단 포인트**: 중앙 오케스트레이션은 ESB, 비동기 큐는 MOM, 대량 이벤트 스트리밍은 Message Broker를 선택한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 시스템 통합 구조 이해 확인 | ESB, MOM, Message Broker, queue, topic | 미들웨어를 WAS와 혼동 |
| 아키텍처 선택 판단 확인 | 동기/비동기, 중앙/분산, 변환/라우팅 | Kafka와 ESB를 같은 용도로 설명 |
| 운영 위험 통제 확인 | DLQ, retry, idempotency, ordering | 메시지 유실·중복 처리 누락 |

> 요약: 이 문제는 미들웨어 종류 암기가 아니라 통합 패턴과 메시지 신뢰성 판단을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 미들웨어는 애플리케이션 간 통신과 데이터 교환을 중재하는 계층이다.
- 배경: 직접 연동은 인터페이스 수 증가, 장애 전파, 형식 변환 중복을 만든다.
- 필요성: ESB·MOM·Message Broker를 동기성, 신뢰성, 처리량 요구에 맞게 선택해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Producer/System A -> Middleware -> Consumer/System B
                  / Routing
                  / Transformation
                  / Queue/Topic
                  / Monitoring/DLQ
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| ESB | 중앙 라우팅·변환·오케스트레이션 | SOAP/REST, canonical model |
| MOM | 큐 기반 비동기 메시지 전달 | JMS, IBM MQ, ActiveMQ |
| Message Broker | topic·stream 기반 pub/sub | Kafka, RabbitMQ, Pulsar |
| DLQ/Monitoring | 실패 메시지 격리·추적 | 재처리와 알림 기준 필요 |

> 요약: 미들웨어는 통신 중재, 변환, 큐·토픽, 실패 격리를 제공하며 유형별 중심 기능이 다르다.

---

## Ⅲ. 동작원리 및 흐름도

```text
메시지 생성 -> 라우팅/변환 -> 큐 또는 토픽 저장 -> 소비자 전달 -> ACK/Retry -> DLQ/모니터링
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Producer가 표준 메시지 생성 | schema registry 적용 |
| 2 | Middleware가 라우팅·변환 수행 | 변환 실패율 1% 이하 |
| 3 | Queue/Topic에 메시지 저장 | replication factor 3 |
| 4 | Consumer가 처리 후 ACK·재시도 | DLQ 비율 0.1% 이하 |

> 요약: 동작은 메시지 생성, 변환·라우팅, 저장, 소비, 실패 격리 순서로 신뢰성 있는 통합을 수행한다.

---

## Ⅳ. 특징

| 구분 | 직접 연동 | ESB·MOM·Broker | 수치·판단 기준 |
|:---|:---|:---|:---|
| 연결 구조 | n:n 직접 호출 | 중간 계층으로 결합도 완화 | 인터페이스 수 30% 이상 감소 |
| 처리 방식 | 동기 호출 중심 | 비동기·버퍼링 가능 | p95 지연·lag 측정 |
| 장애 영향 | 호출자까지 전파 | 큐·DLQ로 격리 | DLQ 0.1% 이하 |
| 한계 | 구조 단순 | 운영 복잡도 증가 | broker cluster 운영 필요 |

> 요약: 미들웨어는 결합도와 장애 전파를 줄이지만, 메시지 중복·순서·운영 지표를 설계해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Point-to-Point | ESB/MOM/Broker | 시스템 5개 이상 통합 |
| 비용/성능 | 초기 구성 단순 | 클러스터·모니터링 필요 | TPS, 지연, 메시지 보존 기간 |
| 운영/위험 | 변경 영향 직접 전파 | 스키마·DLQ·재처리 통제 | 중복 처리 허용 여부 |

> 요약: 시스템 수와 비동기 요구가 증가하면 직접 연동보다 미들웨어 기반 통합이 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 메시지 중복 | 재시도·ACK 실패 | idempotency key, dedup store | 중복 처리 건수 |
| 순서 역전 | 병렬 consumer | partition key, single consumer | out-of-order 비율 |
| 적체 | consumer 처리 지연 | autoscaling, backpressure | consumer lag |

> 요약: 메시징 리스크는 중복, 순서, 적체이며 idempotency와 lag 관리가 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 처리량 | 목표 TPS 대비 120% 용량 | load test |
| 신뢰성 | DLQ 0.1% 이하 | broker metric |
| 운영 지연 | p95 end-to-end latency 목표 충족 | tracing, lag monitor |

> 요약: 성공 여부는 처리량, DLQ 비율, end-to-end 지연으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 중앙 변환·오케스트레이션이 필요한 레거시 EAI는 ESB, 서비스 간 비동기 이벤트는 Kafka·RabbitMQ 기반 broker 선택
2. 메시지 schema registry, idempotency key, retry policy, DLQ 재처리 절차를 표준 인터페이스 계약에 포함
3. broker lag, DLQ, p95 latency, throughput을 Prometheus·Grafana로 관측하고 장애 시 circuit breaker와 backpressure 적용

**결론 (2줄):**
- 기술사 판단: 레거시 표준 통합은 ESB, 트랜잭션성 큐는 MOM, 대량 이벤트 스트리밍은 Kafka형 broker를 선택
- 향후 방향: 중앙 ESB 의존을 줄이고 이벤트 기반 통합과 API 관리, schema governance를 결합하는 방향 필요

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | 메시지 생성, 라우팅, 큐·토픽, ACK 흐름 | 직접 연동과 미들웨어 차이 |
| 요구사항 명시형 | "비교하시오", "설계하시오", "방안을 제시하시오" | ESB·MOM·Broker 선택 기준 | 중복·순서·적체 리스크와 지표 |

> 요약: 설명형은 통합 원리, 비교형은 ESB·MOM·Broker의 목적별 선택 기준으로 전환한다.
