---
title: "MQTT 경량 메시징 (MQTT)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 98
---

# 📖 【암기용】 개념 완전 이해

> 목적: MQTT를 IoT 장치가 broker를 통해 topic 기반으로 메시지를 주고받는 경량 publish/subscribe 프로토콜로 이해하게 만든다.

## 한눈에
- **개요**: 저전력·저대역폭 환경에서 topic 기반 메시지를 발행·구독하는 IoT 메시징 프로토콜
- **왜 필요한가**: 수천 장치가 서버와 직접 연결하면 연결 관리와 재전송 부담이 커진다. broker가 중간에서 메시지를 분배한다.
- **핵심 직관**: 게시판(topic)에 글을 붙이면 관심 있는 사람(subscriber)에게 자동 전달되는 방식이다.

## 깊이 이해
- **배경·문제의식**: IoT 장치는 네트워크가 끊기고 배터리와 메모리가 제한된다. HTTP polling은 header가 크고 반복 연결 비용이 발생한다.
- **작동 원리**: client는 broker에 TCP로 연결하고 topic에 publish한다. subscriber는 topic filter를 등록한다. QoS 0/1/2가 전달 보장 수준을 조절하고 retained message, last will이 상태 전달을 보완한다.
- **비유**: 각 센서가 중앙 우체국에 편지를 맡기면, 우체국이 구독자 목록에 따라 복사해 배달한다.
- **구체 예시**: `factory/line1/temp` topic에 센서가 5초마다 publish하고, dashboard와 rule engine이 동시에 subscribe한다. 제어 명령은 `factory/line1/cmd`로 전달한다.
- **흔한 오해·주의점**: QoS 2가 항상 적합한 것은 아니다. 메시지 왕복이 늘어 latency와 broker 부하가 증가하므로 telemetry는 QoS 0/1, 결제성 명령은 QoS 2로 구분한다.

## 연결 개념
- IoT Architecture — MQTT가 장치와 플랫폼을 연결
- CoAP — REST형 constrained protocol 대안
- TLS·mTLS — broker 접속 인증과 암호화

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: MQTT 출제 시 pub/sub 구조, QoS 0/1/2, topic 설계, broker 운영 리스크를 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MQTT는 broker 중심 publish/subscribe 모델로 IoT 장치와 애플리케이션 간 메시지를 경량 전송하는 프로토콜이다.
> 2. **가치**: topic, QoS 0/1/2, retained message, last will로 불안정한 네트워크에서도 telemetry와 명령을 분리 처리한다.
> 3. **판단 포인트**: QoS 선택, topic namespace, session persistence, TLS/mTLS, broker HA를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| MQTT 구조 이해 확인 | client, broker, topic, publish/subscribe | HTTP request/response로 설명 |
| 전달 보장 판단 확인 | QoS 0 at most once, QoS 1 at least once, QoS 2 exactly once | QoS 숫자 의미 누락 |
| IoT 운영 역량 확인 | retained, last will, session, TLS/mTLS | broker 장애·topic 권한 누락 |

> 요약: 이 문제는 MQTT를 경량 프로토콜 소개가 아니라 IoT 메시징 운영 설계로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

MQTT는 IoT용 경량 publish/subscribe 메시징 프로토콜이다. 장치가 broker에 연결해 topic에 메시지를 발행하면 구독자가 비동기로 수신한다. 저대역폭·불안정한 네트워크에서 연결 유지, 전달 보장, 장치 상태 통지가 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Publisher Device -> MQTT Broker -> Subscriber App
                 -> Topic Tree / QoS / Session / Retained / Last Will
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Client | publish 또는 subscribe 수행 | device, gateway, app |
| Broker | topic 기반 라우팅과 세션 관리 | ACL, persistence, cluster |
| Topic | 계층형 메시지 주소 | `factory/line1/temp` |
| QoS | 메시지 전달 보장 수준 | QoS 0/1/2 |

> 요약: MQTT는 broker가 topic과 QoS를 기준으로 publisher와 subscriber를 분리하는 구조다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Client Connect -> Subscribe Topic -> Publish Message
-> Broker Match -> QoS Handshake -> Subscriber Deliver -> Ack/Store
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | TCP 1883 또는 TLS 8883으로 broker 연결 | TLS 1.2 이상 |
| 2 | clientId, username, certificate 인증 | mTLS 또는 token |
| 3 | topic publish와 wildcard subscribe 처리 | `+`, `#` 권한 제한 |
| 4 | QoS 0/1/2 handshake 수행 | duplicate flag 처리 |
| 5 | retained, last will, persistent session 관리 | offline queue 길이 제한 |

> 요약: MQTT는 연결 인증 후 topic 매칭과 QoS handshake로 메시지를 전달한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | MQTT | 수치 컬럼 |
|:---|:---|:---|:---|
| 통신 모델 | HTTP polling | publish/subscribe | TCP 1883, TLS 8883 |
| 전달 보장 | 단순 요청 응답 | QoS 0/1/2 선택 | telemetry QoS 0/1 |
| 상태 전달 | 별도 heartbeat | retained, last will | keep alive 60초 |
| 제약 | payload 자유 | topic 설계·broker 의존 | topic depth 관리 |

> 요약: MQTT는 저대역폭 IoT에 맞지만 broker HA와 topic 권한 설계가 운영 품질을 좌우한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 메시징 | HTTP polling | MQTT pub/sub | 장치 수 1,000대 이상 |
| 전달 보장 | fire-and-forget | QoS 0/1/2 | telemetry vs command 구분 |
| 연결 관리 | 서버 직접 연결 | broker session | intermittent network |

> 요약: MQTT는 다수 장치의 비동기 telemetry와 명령 분배에 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| broker 병목 | topic fan-out, QoS 2 증가 | cluster, shared subscription | broker CPU 70% 이하 |
| 중복 메시지 | QoS 1 재전송 | messageId, idempotent consumer | duplicate rate 1% 이하 |
| 권한 오남용 | wildcard topic 허용 | topic ACL, mTLS | unauthorized subscribe 0건 |

> 요약: MQTT 운영 리스크는 broker 부하, 중복 처리, topic 권한에서 발생한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전달 품질 | publish success 99.9%, duplicate 1% 이하 | broker metric |
| 지연 | p95 end-to-end latency 1초 이하 | timestamp 비교 |
| 보안 운영 | TLS 8883 사용, 인증 실패 추적 | broker auth log |

> 요약: MQTT 도입 효과는 전달 성공률, p95 지연, 인증·권한 로그로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. topic namespace를 `site/line/device/metric` 형식으로 표준화하고 wildcard `#` 권한을 관리자 전용으로 제한
2. telemetry는 MQTT QoS 0 또는 1, 제어 명령은 QoS 1 또는 2로 분리하고 consumer idempotency 적용
3. broker cluster, TLS 8883, mTLS, persistent session, retained message를 운영 정책으로 정의

**결론 (2줄):**
- 기술사 판단: 저전력 장치의 다대다 telemetry는 MQTT가 적합하나 broker HA와 topic ACL이 필수임
- 향후 방향: MQTT 5.0의 reason code, user property, shared subscription을 활용한 대규모 fleet 운영으로 확장

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | connect, publish, subscribe, QoS 흐름 | HTTP·CoAP 대비 MQTT 특성 |
| 요구사항 명시형 | "비교하시오", "방안을 제시하시오", "설계하시오" | topic·QoS·broker HA 설계 | 중복·권한·지연 대응 |

> 요약: 포괄형은 pub/sub 원리, 요구사항 명시형은 topic과 QoS 운영 설계를 중심으로 작성한다.
