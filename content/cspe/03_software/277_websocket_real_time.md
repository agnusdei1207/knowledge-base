---
title: "WebSocket 실시간 통신 (WebSocket Real-Time)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 277
---

# 📖 【암기용】 개념 완전 이해

> 목적: WebSocket을 HTTP 연결을 업그레이드해 양방향 실시간 메시지를 주고받는 프로토콜로 이해하게 만든다.

## 한눈에
- **개요**: WebSocket은 하나의 TCP 연결에서 클라이언트와 서버가 양방향 메시지를 교환하는 프로토콜이다.
- **왜 필요한가**: 채팅, 협업 편집, 주식 시세, 게임처럼 서버가 즉시 이벤트를 밀어줘야 하는 서비스에 필요하다.
- **핵심 직관**: 매번 문을 두드리는 HTTP 요청 대신 전화 통화를 연결해 두고 서로 말하는 방식이다.

## 깊이 이해
- **배경·문제의식**: HTTP polling은 요청을 반복해 헤더 비용과 지연이 누적된다. WebSocket은 최초 handshake 후 연결을 유지해 서버 push를 가능하게 한다.
- **작동 원리**: 클라이언트가 HTTP `Upgrade: websocket`을 보내고 서버가 `101 Switching Protocols`로 응답하면 이후 frame 단위로 메시지를 교환한다.
- **비유**: 택배 조회를 계속 새로고침하는 대신 기사와 무전기를 연결해 위치 변경 때마다 듣는 구조다.
- **구체 예시**: 협업 문서에서 사용자 입력 이벤트를 50ms 단위로 전송하고, 서버는 같은 room의 연결들에게 변경 delta를 broadcast한다.
- **흔한 오해·주의점**: WebSocket은 메시지 브로커가 아니다. 접속 관리, 인증 갱신, heartbeat, 수평 확장 시 세션 라우팅과 fan-out 설계가 별도로 필요하다.

## 연결 개념
- HTTP Upgrade — WebSocket 연결 시작 절차
- Server-Sent Events — 서버 단방향 push 대안
- Pub/Sub — 다중 서버 환경의 메시지 fan-out

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: WebSocket을 handshake, frame, connection lifecycle, 확장 운영 구조로 답안화한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: WebSocket은 HTTP handshake 후 TCP 연결을 유지하여 클라이언트·서버 양방향 메시지를 frame 단위로 교환하는 프로토콜이다.
> 2. **가치**: polling의 반복 요청 비용을 줄이고 서버 이벤트를 낮은 지연으로 전달한다.
> 3. **판단 포인트**: 실시간 요구, 연결 수, 인증·권한, heartbeat, fan-out 구조를 함께 설계해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 실시간 프로토콜 이해 확인 | HTTP Upgrade, 101 응답, frame, full-duplex | HTTP와 완전히 별도 프로토콜로 오해 |
| 대안 비교 판단 확인 | polling, SSE, WebSocket 선택 기준 | 실시간이면 무조건 WebSocket 단정 |
| 운영 설계 역량 확인 | connection state, heartbeat, auth, scale-out | 메시지 전송만 쓰고 연결 관리 누락 |

> 요약: WebSocket 문제는 프로토콜 절차와 수평 확장 운영을 함께 써야 한다.

---

## Ⅰ. 개요 및 필요성

- 개요: WebSocket은 지속 TCP 연결 기반 양방향 통신 기술이다.
- 배경: 반복 polling은 요청마다 헤더 비용과 지연이 발생하므로 채팅·시세·협업 서비스에 부적합하다.
- 필요성: HTTP Upgrade, 서버 push, heartbeat, 연결 상태 관리로 실시간 메시지 전달을 구현해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client -> HTTP Upgrade -> WebSocket Server -> Session Registry
  -> Message Handler -> Pub/Sub Broker -> Other Nodes
  -> Heartbeat/Auth/Monitoring
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Handshake | HTTP Upgrade 및 101 응답 | TLS 사용 시 WSS |
| Frame | text/binary/ping/pong/close 메시지 | fragmentation 가능 |
| Session Registry | 연결·room·user 매핑 | 수평 확장 시 외부 저장 검토 |
| Pub/Sub Broker | 노드 간 fan-out | Redis, Kafka, NATS |

> 요약: WebSocket 운영 구조는 연결 수명, 메시지 처리, 노드 간 fan-out, 관측성으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Client Connect -> HTTP Upgrade Request -> 101 Response
  -> Frame Exchange -> Heartbeat Ping/Pong
  -> Broadcast/Direct Message -> Close/Reconnect
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | TLS 및 HTTP Upgrade 요청 | WSS, origin 검증 |
| 2 | 서버가 연결 승인·세션 등록 | auth token, user mapping |
| 3 | frame 송수신 및 room broadcast | message ack, ordering |
| 4 | heartbeat·close·reconnect 처리 | idle timeout, reconnect rate |

> 요약: WebSocket은 handshake 후 frame 교환과 heartbeat로 연결 생존을 관리한다.

---

## Ⅳ. 특징

| 구분 | HTTP Polling/SSE | WebSocket | 정량·기술 포인트 |
|:---|:---|:---|:---|
| 통신 방향 | polling 양방향 흉내, SSE 단방향 | full-duplex | TCP 연결 유지 |
| 지연 | polling interval 의존 | event 즉시 전송 | p95 message latency 측정 |
| 비용 | 요청 헤더 반복 | handshake 후 frame | 연결당 메모리 필요 |
| 운영 | stateless 처리 용이 | connection state 관리 | sticky session 또는 broker |

> 요약: WebSocket은 양방향 지연 요구에 적합하지만 연결 상태와 fan-out 비용을 설계해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| Polling | 구현 단순 | WebSocket | 업데이트 주기 1초 이하, 양방향 필요 |
| SSE | 서버 단방향 | WebSocket | 클라이언트 입력 이벤트 빈번 |
| gRPC Stream | 내부 서비스 | WebSocket | 브라우저 호환 실시간 UI |

> 요약: 브라우저 기반 양방향 실시간 서비스는 WebSocket, 서버 단방향 알림은 SSE가 선택 기준이다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 연결 폭증 | 장시간 연결 유지 | connection limit, autoscaling | active connection count |
| 인증 만료 | 장기 세션에서 토큰 갱신 누락 | re-auth message, short token refresh | auth failure rate |
| 메시지 유실 | 노드 장애·broker 장애 | ack, replay, reconnect sync | delivery failure count |

> 요약: 연결 수, 인증 갱신, 메시지 전달 보장을 운영 리스크로 관리한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 지연 | p95 message latency 100ms 이하 | tracing, synthetic test |
| 연결 | node당 connection limit 80% 이하 | gateway metric |
| 복구 | reconnect success 99% 이상 | client metric, server log |

> 요약: WebSocket 품질은 메시지 지연, 연결 사용률, 재연결 성공률로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. WSS, origin check, JWT 재검증, room 권한 검사를 handshake와 message handler 양쪽에 배치함.
2. 수평 확장은 sticky session 또는 Redis/NATS pub-sub을 적용하고 active connection과 fan-out rate를 노드별로 측정함.
3. heartbeat interval 30초, idle timeout, reconnect backoff, message ack를 정의해 모바일 네트워크 변동에 대응함.

**결론 (2줄):**
- 기술사 판단: 양방향 실시간성이 필요하면 WebSocket, 서버 단방향 알림이면 SSE, 단순 상태 조회면 polling 선택.
- 향후 방향: WebTransport, HTTP/3, edge pub-sub과 결합해 브라우저 실시간 통신의 지연·복구 지표가 세분화됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "WebSocket을 설명하시오" | handshake와 frame 교환 흐름 | polling, SSE 대비 특징 |
| 요구사항 명시형 | "실시간 통신을 설계하시오", "비교하시오" | 인증, heartbeat, fan-out 흐름 | 연결 수, 지연, 재연결 리스크 |

> 요약: 설명형은 프로토콜 절차, 설계형은 연결 운영과 확장 구조 중심으로 전환한다.
