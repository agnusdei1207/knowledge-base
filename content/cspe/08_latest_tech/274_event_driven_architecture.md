---
title: "Event-Driven Architecture 이벤트 기반 아키텍처 (Event-Driven Architecture)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 274
extra:
  question_no: "274"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- EDA는 상태 변화나 사건 자체를 중심으로 시스템을 느슨하게 연결하는 구조임
- 명령 중심 호출과 달리 생산자와 소비자를 시간적으로 분리하는 데 강점이 있음
- 이벤트 정의와 전달 보장과 중복 처리 정책이 설계 핵심임

## Ⅰ. 개요

- **정의/개념**: Event-Driven Architecture는 시스템에서 발생한 사건을 이벤트로 발행하고 다른 컴포넌트가 이를 비동기적으로 구독해 처리하도록 구성하는 느슨한 결합 중심의 아키텍처임
- **배경/필요성**: 분산 서비스가 많아질수록 직접 호출 구조는 결합도와 장애 전파 위험이 커져 이벤트 중심 비동기 연결 방식이 확장성과 유연성을 높이는 대안이 됨

## Ⅱ. 특징

- 생산자와 소비자를 시간적으로 분리해 결합도를 낮춤
- 이벤트 추가 구독으로 기능 확장이 용이함
- 비동기 처리로 순간 부하 완충과 확장이 가능함
- 순서 보장과 중복 처리와 최종 일관성 관리가 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | Event-Driven Architecture | Request-Response Architecture | Batch Integration |
|:---|:---|:---|:---|
| 결합도 | 낮음 | 높음 | 중간 |
| 응답 방식 | 비동기 | 동기 | 지연성 큼 |
| 확장성 | 높음 | 중간 | 낮음 |
| 핵심 과제 | 중복과 일관성 관리 | 지연과 장애 전파 | 신선도 부족 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Event Producer | 주문 생성이나 상태 변경처럼 비즈니스 사건을 이벤트로 발행하는 생산자 컴포넌트임 |
| Event Broker | 이벤트를 저장하거나 전달해 생산자와 소비자 사이를 느슨하게 연결하는 중개 계층임 |
| Event Consumer | 필요한 이벤트를 구독해 독립적으로 후속 처리를 수행하는 소비자 서비스임 |
| Schema and Contract | 이벤트 형식과 버전과 필드를 정의해 서비스 간 해석 일관성을 보장하는 계약 계층임 |
| Reliability Control | 재시도와 중복 제거와 DLQ 같은 메커니즘으로 전달 실패와 오류를 관리하는 안정화 계층임 |

```text
+----------+    +--------------+    +-----------+
| Producer | -> | Event Broker | -> | Consumer A|
+----------+    +--------------+    +-----------+
                                 \-> | Consumer B|
                                     +-----------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 사건 발생    | -> | 이벤트 발행  | -> | 브로커 저장  | -> | 소비자 처리  | -> | 후속 이벤트 발행 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **사건 발생**: 비즈니스 상태 변화가 생김
2. **이벤트 발행**: 생산자가 표준 이벤트를 브로커에 보냄
3. **브로커 저장**: 브로커가 이벤트를 큐나 토픽에 유지함
4. **소비자 처리**: 구독 서비스가 독립적으로 이벤트를 처리함
5. **후속 이벤트 발행**: 필요한 경우 다음 이벤트를 생성함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 이벤트 스키마 변경 관리가 약하면 생산자와 소비자 해석이 어긋나 장애와 데이터 불일치가 발생할 수 있음
   - 해결방안: schema registry와 backward compatibility policy를 적용하고 incompatible schema deployment count와 consumer parse failure rate로 검증함
2. 문제: 최소 한 번 전달 구조에서 중복 이벤트 처리가 미흡하면 비즈니스 로직이 여러 번 수행될 수 있음
   - 해결방안: idempotent consumer와 deduplication key strategy를 적용하고 duplicate processing incident rate와 exactly once simulation success rate로 검증함
3. 문제: 최종 일관성 모델을 이해하지 못하고 즉시 일관성을 기대하면 사용자 경험과 운영 판단이 혼란스러워질 수 있음
   - 해결방안: consistency boundary design과 user facing status model을 적용하고 stale read complaint rate와 eventual consistency convergence time으로 검증함

## Ⅶ. 적용 사례

- 주문 이벤트 플랫폼이 스키마 레지스트리를 운영하며 확인 지표는 incompatible schema deployment count와 consumer parse failure rate임
- 결제 후처리 서비스가 중복 제거 키 전략을 적용하며 확인 지표는 duplicate processing incident rate와 exactly once simulation success rate임
- 재고 동기화 시스템이 일관성 경계 모델을 설계하며 확인 지표는 stale read complaint rate와 eventual consistency convergence time임

## Ⅷ. 결론

EDA는 느슨한 결합과 확장성에 강하지만 스키마 거버넌스와 중복 처리와 일관성 모델 설계를 함께 갖춰야 안정적으로 운영됨.
