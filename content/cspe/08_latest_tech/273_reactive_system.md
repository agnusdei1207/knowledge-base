---
title: "리액티브 시스템 (Reactive System)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 273
---

# 📖 【암기용】 개념 완전 이해

> 목적: 리액티브 시스템을 부하 변화와 장애 상황에서도 메시지 기반으로 응답성을 유지하도록 설계하는 아키텍처 원칙으로 이해하게 만든다.

## 한눈에
- **개요**: responsive, resilient, elastic, message-driven 특성을 갖는 비동기 시스템 설계 원칙
- **왜 필요한가**: 동기 호출로 엮인 시스템은 한 서비스 지연이나 장애가 호출 체인 전체로 전파되기 쉽다.
- **핵심 직관**: 모든 창구가 직접 서로를 기다리는 대신 접수함과 담당자 배정을 통해 업무를 흘려보내는 방식이다.

## 깊이 이해
- **배경·문제의식**: 클라우드 서비스는 사용량 급증, 부분 장애, 네트워크 지연을 전제로 설계해야 하며 단순 동기 호출은 장애 격리가 어렵다.
- **작동 원리**: 구성요소는 메시지로 통신하고, 큐와 backpressure로 부하를 조절하며, supervision과 replication으로 장애 범위를 제한한다.
- **비유**: 택배 허브가 물량 급증 시 분류 라인을 늘리고, 한 구역 장애가 전체 배송을 멈추지 않게 우회시키는 구조다.
- **구체 예시**: 주문 요청은 즉시 접수 응답을 반환하고, 결제·재고·배송은 이벤트와 메시지 큐로 비동기 처리해 장애 서비스를 격리한다.
- **흔한 오해·주의점**: 리액티브는 단순히 비동기 API를 쓰는 뜻이 아니다. 응답성, 복원력, 탄력성, 메시지 기반을 동시에 만족해야 한다.

## 연결 개념
- Event-Driven Architecture — 리액티브 시스템을 구현하는 대표 구조
- Backpressure — 생산 속도와 소비 속도를 조절하는 메커니즘
- Virtual Thread — blocking 코드 단순화 관점의 대안

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 리액티브 시스템은 네 가지 특성을 따로 나열하지 말고 메시지 기반 설계가 응답성·복원력·탄력성을 만드는 인과로 설명한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Reactive System은 message-driven 구조로 responsive, resilient, elastic 특성을 달성하는 시스템 설계 원칙임.
> 2. **가치**: 비동기 메시지, backpressure, 장애 격리로 부하 변화와 부분 장애가 전체 응답 지연으로 번지는 것을 제한함.
> 3. **판단 포인트**: 지연 요구, 일관성 요구, 운영 복잡도, 메시지 순서 보장을 기준으로 적용 범위를 정해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 리액티브 원칙 이해 확인 | responsive, resilient, elastic, message-driven | 비동기 프로그래밍과 동일시 |
| 장애·부하 설계 확인 | backpressure, isolation, supervision | 속도 개선 기술로만 설명 |
| 적용 판단 확인 | eventual consistency, ordering, observability | 모든 업무를 비동기로 전환 |

> 요약: 이 문제는 메시지 기반 설계가 부하 조절과 장애 격리를 만드는 구조적 이유를 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: 메시지 기반 반응형 설계 원칙
- 배경: 동기 호출 체인은 한 서비스 지연이 상위 요청 timeout으로 전파될 수 있음.
- 필요성: 부하 변동과 부분 장애 상황에서 응답성, 복원력, 탄력성을 함께 설계해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> API / Command Handler -> Message Channel -> Worker / Actor
Worker / Actor -> State Store / Event Store -> Response / Event
Backpressure / Supervisor -> Queue / Worker Pool -> Observability
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Message Channel | 구성요소 간 비동기 전달 | queue, stream, mailbox |
| Worker/Actor | 메시지 처리와 상태 변경 | 격리된 실행 단위 |
| Backpressure | 생산·소비 속도 조절 | queue depth, demand signal |
| Supervisor | 장애 감지와 재시작 정책 | 실패 범위 제한 |

> 요약: 리액티브 시스템은 메시지 채널과 격리 실행 단위가 부하 조절과 장애 범위 제한을 담당한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
요청 수신 -> 명령 메시지 생성 -> 큐 적재
-> 소비자 처리 -> 상태 저장 / 이벤트 발행
-> 부하 증가 시 backpressure -> 장애 시 supervisor 복구
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 요청을 command 또는 event로 변환 | schema validation |
| 2 | 메시지를 channel에 적재 | queue depth |
| 3 | worker가 메시지를 처리하고 상태 변경 | processing latency |
| 4 | backpressure와 supervisor가 부하·장애 제어 | retry count, failure rate |

> 요약: 리액티브 시스템은 요청을 메시지 흐름으로 바꾸고 부하와 장애를 channel·worker 단위로 제어한다.

---

## Ⅳ. 특징

| 구분 | 동기 호출 중심 | Reactive System | 판단 기준 |
|:---|:---|:---|:---|
| 통신 | 요청-응답 대기 | 메시지 기반 비동기 | 업무 독립성 |
| 장애 처리 | 호출 체인 전파 | 격리·재시작·우회 | 장애 반경 |
| 부하 조절 | thread pool·timeout | backpressure·queue | queue depth |
| 일관성 | 즉시 일관성 용이 | eventual consistency 고려 | 트랜잭션 요구 |

> 요약: 리액티브 시스템은 장애와 부하를 흡수하지만 즉시 일관성이 필요한 업무에는 경계 설정이 필요하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | REST 동기 호출 | message-driven | 호출 체인 길이 |
| 비용/성능 | 단순 트랜잭션 | queue·broker 운영 | 지연 허용 범위 |
| 운영/위험 | 원인 추적 단순 | 분산 추적 필요 | observability 성숙도 |

> 요약: 응답 즉시성이 중요하고 처리 후속 작업이 분리 가능하면 리액티브 구조가 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 메시지 적체 | 소비 처리량 부족 | autoscaling, backpressure | queue lag |
| 중복 처리 | retry와 at-least-once 전달 | idempotency key | duplicate count |
| 추적 단절 | 비동기 경로 분산 | trace context propagation | trace completeness |

> 요약: 리액티브 리스크는 적체, 중복, 추적 단절이며 lag·idempotency·trace로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 응답성 | API p95 SLA 이내 | APM |
| 탄력성 | lag 기준 HPA 반응 | queue metric |
| 복원력 | 실패 메시지 재처리 가능 | DLQ replay test |

> 요약: 리액티브 시스템은 API 지연, queue lag, DLQ 재처리로 운영 가능성을 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 주문 접수와 후속 처리처럼 사용자 응답과 내부 처리를 분리할 수 있는 업무부터 메시지 기반으로 전환함.
2. queue lag, retry count, DLQ depth를 HPA와 알림 기준에 연결해 backpressure를 운영 지표로 관리함.
3. correlation id와 trace context를 메시지 헤더에 포함해 비동기 경로의 원인 추적을 보장함.

**결론 (2줄):**
- 기술사 판단: 부하 변동과 부분 장애 격리가 핵심이면 리액티브 시스템을 선택하고, 즉시 일관성 트랜잭션은 동기 경계로 유지함.
- 향후 방향: 리액티브 설계는 EDA, stream processing, cloud-native autoscaling과 결합되어 대규모 서비스의 기본 패턴으로 확장됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "리액티브 시스템을 설명하시오" | 메시지 처리와 backpressure 흐름 | 동기 호출 대비 차이 |
| 요구사항 명시형 | "장애 격리 아키텍처를 설계하시오" | supervisor·DLQ·autoscaling 절차 | 일관성·중복·추적 리스크 |

> 요약: 설명형은 4대 원칙을, 설계형은 장애·부하 통제 지표를 중심으로 작성한다.
