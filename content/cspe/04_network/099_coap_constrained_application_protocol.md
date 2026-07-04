---
title: "CoAP (CoAP Constrained Application Protocol)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 99
---

# 📖 【암기용】 개념 완전 이해

> 목적: CoAP을 제한된 IoT 장치가 UDP 위에서 REST 방식으로 자원을 주고받는 경량 애플리케이션 프로토콜로 이해하게 만든다.

## 한눈에
- **개요**: 저전력·저메모리 장치를 위한 UDP 기반 REST형 IoT 프로토콜
- **왜 필요한가**: 작은 센서가 HTTP/TCP/TLS 전체 스택을 유지하기에는 메모리, 전력, 패킷 크기 부담이 크다.
- **핵심 직관**: HTTP의 GET/POST 구조를 작은 엽서 크기로 줄여 UDP로 보내는 방식이다.

## 깊이 이해
- **배경·문제의식**: 센서 네트워크와 6LoWPAN 환경은 MTU와 전력 제약이 크다. CoAP은 REST 자원 모델을 유지하면서 헤더를 줄이고 UDP 5683을 사용한다.
- **작동 원리**: client가 URI resource에 GET, POST, PUT, DELETE를 보낸다. confirmable 메시지는 ACK로 신뢰성을 보완하고, observe 옵션은 자원 변화 알림을 제공한다. 보안은 DTLS 또는 OSCORE를 사용한다.
- **비유**: 웹 API를 쓰되 택배 상자가 아니라 작은 우편엽서로 주고받는 방식이다.
- **구체 예시**: 온도 센서가 `coap://sensor01/temp`에 GET 요청을 받으면 2.05 Content로 현재 온도를 반환한다. observe를 설정하면 값 변경 시 서버가 알림을 전송한다.
- **흔한 오해·주의점**: CoAP은 UDP라서 무조건 신뢰성이 없는 것이 아니다. confirmable, message ID, retransmission으로 애플리케이션 수준 확인을 제공한다.

## 연결 개념
- MQTT — broker 기반 pub/sub 대안
- 6LoWPAN — 저전력 IPv6 센서망
- DTLS·OSCORE — CoAP 보안 통제

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: CoAP 출제 시 REST 모델, UDP 5683, 메시지 유형, observe, 보안 통제를 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CoAP은 constrained device가 UDP 기반으로 REST 자원을 교환하도록 설계된 경량 애플리케이션 프로토콜이다.
> 2. **가치**: 작은 헤더, confirmable 메시지, observe 옵션으로 저전력 센서망의 요청·응답과 알림을 지원한다.
> 3. **판단 포인트**: UDP 5683, DTLS/OSCORE, confirmable/non-confirmable, HTTP proxy 연계를 함께 판단해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| CoAP 구조 이해 확인 | REST method, resource URI, UDP 5683 | MQTT와 같은 broker 구조로 설명 |
| 신뢰성 보완 이해 확인 | CON, NON, ACK, RST, retransmission | UDP라서 확인 기능 없음으로 단정 |
| 보안·연계 판단 확인 | DTLS, OSCORE, HTTP-CoAP proxy | 암호화와 인증 누락 |

> 요약: 이 문제는 CoAP을 HTTP 축소판이 아니라 constrained REST 프로토콜로 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 제약 장치용 UDP REST 프로토콜
- 배경: 저전력 센서망은 HTTP/TCP 연결 유지와 큰 헤더를 처리하기에 CPU, 메모리, 전력 예산이 제한된다.
- 필요성: CoAP은 GET/POST/PUT/DELETE, confirmable message, observe, DTLS/OSCORE로 요청·응답과 보안 통신을 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
CoAP Client -> UDP 5683/5684 -> CoAP Server Resource
            -> Method / Token / Message ID / Option / Payload
            -> DTLS or OSCORE
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Method | GET, POST, PUT, DELETE 자원 조작 | REST 모델 |
| Message Type | CON, NON, ACK, RST | 신뢰성 선택 |
| Option | URI, Observe, Block-wise 등 확장 | 작은 MTU 대응 |
| Security | DTLS 또는 OSCORE 적용 | UDP 5684, end-to-end 보호 |

> 요약: CoAP은 REST 메서드와 UDP 메시지 유형을 결합해 작은 장치의 자원 통신을 처리한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Resource 요청 생성 -> UDP 전송 -> CON/NON 처리
-> Server 처리 -> ACK/Response -> Observe/Block-wise 후속 처리
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | URI와 method로 요청 구성 | `coap://host/temp` |
| 2 | CON 또는 NON 메시지 선택 | 신뢰성 요구 반영 |
| 3 | UDP 5683으로 전송하고 message ID 부여 | 중복 검출 |
| 4 | ACK와 response code 수신 | 2.05 Content, 4.04 Not Found |
| 5 | observe, block-wise, DTLS/OSCORE 처리 | 알림·대용량 분할 |

> 요약: CoAP은 URI 기반 요청을 UDP 메시지로 전송하고 ACK·토큰·옵션으로 신뢰성과 확장을 보완한다.

---

## Ⅳ. 특징

| 구분 | 기존/대안 | CoAP | 수치 컬럼 |
|:---|:---|:---|:---|
| 전송 | HTTP over TCP | CoAP over UDP | UDP 5683, DTLS 5684 |
| 통신 모델 | 무거운 연결 | REST + 경량 헤더 | 4-byte base header |
| 신뢰성 | TCP 재전송 | CON/ACK retransmission | message ID 16-bit |
| 알림 | polling | Observe option | 센서 변화 push |

> 요약: CoAP은 REST 호환성을 유지하면서 UDP 기반 경량화와 선택적 신뢰성을 제공한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| IoT 메시징 | MQTT broker | CoAP REST resource | device-to-device REST 필요 |
| 전송 계층 | TCP | UDP | 저전력·작은 MTU 환경 |
| 보안 | TLS | DTLS 또는 OSCORE | proxy 통과와 E2E 보호 요구 |

> 요약: CoAP은 broker보다 REST 자원 접근이 자연스럽고 저전력 IPv6 센서망에 적합하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 패킷 손실 | UDP 기반 무선 품질 저하 | CON, retransmission tuning | timeout rate 1% 이하 |
| 보안 취약 | DTLS 미적용·키 관리 미흡 | DTLS 1.2, OSCORE, PSK 관리 | 미암호화 요청 0건 |
| 단편화 부담 | 큰 payload | block-wise transfer | fragmentation rate |

> 요약: CoAP 운영은 손실 보완, 보안 키 관리, 작은 MTU 대응이 핵심 통제 대상이다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전달 품질 | CON timeout 1% 이하 | CoAP client metric |
| 지연 | p95 response latency 500ms 이하 | request timestamp |
| 보안 | DTLS/OSCORE 적용률 100% | gateway log, key inventory |

> 요약: CoAP 도입 효과는 timeout, 응답 지연, 보안 적용률로 검증한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 센서 resource URI를 `/device/{id}/metric/{name}` 형식으로 표준화하고 GET/PUT 의미를 고정
2. 상태 조회는 NON, 제어 명령은 CON으로 구분하고 retransmission timeout을 무선 품질에 맞춰 조정
3. DTLS 1.2 또는 OSCORE를 적용하고 HTTP-CoAP proxy에서 인증·권한·로그를 통합

**결론 (2줄):**
- 기술사 판단: constrained device에서 REST 자원 모델과 낮은 전송 오버헤드가 필요하면 CoAP을 선택함
- 향후 방향: OSCORE와 LwM2M 결합으로 장치 관리, 보안 업데이트, 관측 알림을 통합하는 방향

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "설명하시오", "기술하시오" | REST 요청·CON/ACK 흐름 | HTTP·MQTT 대비 특성 |
| 요구사항 명시형 | "비교하시오", "방안을 제시하시오", "설계하시오" | 무선 손실·보안·proxy 설계 | DTLS/OSCORE와 block-wise 대응 |

> 요약: 포괄형은 CoAP 구조, 요구사항 명시형은 제한 장치의 신뢰성·보안 설계를 중심으로 전환한다.
