---
title: "WebSocket 실시간 통신 (WebSocket Real-Time)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 277
---

# 📖 【암기용】 개념 완전 이해

> 목적: 이 개념을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: WebSocket은 **프로토콜**(Protocol) 계층에서 HTTP 연결을 하나의 지속적인 **TCP** 연결로 전환해, 클라이언트와 서버가 **양방향**(Full-Duplex)으로 메시지를 주고받게 하는 표준(RFC 6455)이다.
- **왜 필요한가**: 채팅, 협업 편집, 주식 시세, 게임처럼 서버가 이벤트를 즉시 클라이언트로 밀어줘야 하는 서비스에서, 매번 새 HTTP 요청을 반복하는 polling은 헤더 비용과 지연이 누적되어 부적합하다.
- **핵심 직관**: 매번 문을 두드려 안부를 묻는 HTTP 요청 대신, 전화 통화를 한 번 연결해두고 그 회선으로 서로 아무 때나 말하는 방식이다.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| 프로토콜(Protocol) | 통신 양쪽이 지키기로 약속한 메시지 형식·순서 규칙 — 이 문서의 상위 주제 | 대화의 규칙(누가 먼저 말할지 등) |
| TCP 연결 | 데이터의 순서와 전달을 보장하는 전송 계층 연결 — WebSocket이 이 위에서 그대로 재사용 | 한 번 뚫어놓은 전화선 |
| Handshake(핸드셰이크) | HTTP 요청/응답으로 "이제부터 WebSocket으로 전환하자"를 합의하는 최초 1회 절차 | 통화를 시작하기 전 "여보세요" 주고받기 |
| Upgrade 헤더 | 클라이언트가 보내는 `Upgrade: websocket`, `Connection: Upgrade` — 프로토콜 전환을 요청하는 HTTP 헤더 | "이 통화를 화상통화로 바꾸자"는 요청 |
| 101 Switching Protocols | 서버가 프로토콜 전환 요청을 수락했음을 알리는 HTTP 상태 코드 | "좋아, 바꾸자"는 응답 |
| Frame(프레임) | Handshake 이후 실제 메시지를 담아 주고받는 전송 단위(text/binary/ping/pong/close) | 통화 중 주고받는 한 마디 한 마디 |
| Full-Duplex(전이중) | 송신과 수신이 동시에 가능한 통신 방식(HTTP 응답처럼 한쪽 방향으로 끝나지 않음) | 전화 통화 — 양쪽이 동시에 말할 수 있음 |
| Heartbeat(ping/pong) | 연결이 살아있는지 주기적으로 확인하는 신호 | 통화 중 "듣고 있어?"라고 가끔 확인 |
| Sticky Session | 같은 클라이언트의 연결을 항상 같은 서버 인스턴스로 보내는 라우팅 정책 | 같은 손님을 항상 같은 상담원에게 연결 |
| Fan-out | 한 이벤트를 같은 room·topic을 구독 중인 여러 연결에 동시에 전파하는 것 | 방송 하나를 여러 스피커로 동시에 내보냄 |

## 깊이 이해

### Handshake 절차를 헤더로 직접 따라가기
- 클라이언트가 먼저 일반 HTTP 요청처럼 보낸다: `GET /chat HTTP/1.1`, `Host: example.com`, `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==`, `Sec-WebSocket-Version: 13`.
- 서버가 수락하면 `HTTP/1.1 101 Switching Protocols`, `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Accept: (Key와 고정 GUID를 합쳐 SHA-1 해시 후 Base64 인코딩한 값)`으로 응답한다.
- 이 한 번의 HTTP 왕복(보통 수십~수백ms) 이후로는 **같은 TCP 소켓을 그대로 재사용**해 프레임을 주고받는다 — 메시지마다 HTTP 헤더(수백 바이트)를 반복하지 않는다는 것이 polling과의 결정적 차이다.

### Polling과 비교한 비용 — 수치로 확인
- 1초 간격 short polling을 쓰면 연결된 클라이언트마다 매초 새 HTTP 요청이 발생하고, 헤더만 요청당 약 500바이트~1KB다. 클라이언트가 10,000명이면 초당 10,000건의 요청과 약 5~10MB/s의 헤더 오버헤드가 반복해서 발생한다.
- WebSocket은 최초 handshake 1회 이후로는 순수 payload와 최소 프레임 헤더(2~14바이트)만 오간다. 메시지가 초당 1건뿐이라도 handshake 재수행 없이 곧바로 전송되므로, 체감 지연은 편도 네트워크 왕복시간(RTT, 보통 수십ms) 수준으로 줄어든다.

### Frame 구조와 분할(fragmentation)
- 각 프레임은 opcode로 종류를 표시한다: text(0x1), binary(0x2), close(0x8), ping(0x9), pong(0xA). 하나의 큰 메시지는 여러 프레임으로 쪼개 보낼 수 있고(fragmentation), 마지막 프레임에만 FIN 비트가 켜져 "이 메시지는 여기서 끝"임을 알린다.

### Heartbeat가 필요한 이유 — 수치로 확인
- 중간의 NAT나 프록시는 트래픽이 없는 연결을 보통 60~300초 사이에 강제로 끊어버린다. 그래서 30초 간격으로 ping을 보내고 pong을 받아 "이 연결은 아직 살아있다"는 신호를 주기적으로 만들어준다.
- pong이 일정 시간(예: 10초) 안에 안 돌아오면 죽은 연결로 판단해 서버가 자원을 정리한다 — 그렇지 않으면 죽은 연결이 계속 메모리를 점유한다.

### 수평 확장의 핵심 난제 — 세션 라우팅과 fan-out
- WebSocket 연결은 상태를 가진다(stateful) — 연결 정보가 특정 서버 프로세스의 메모리에 있다. 서버가 여러 대라면, A 서버에 연결된 클라이언트에게 B 서버가 받은 이벤트를 어떻게 전달할지가 문제가 된다.
- 해법은 두 가지다. ① sticky session으로 같은 사용자를 항상 같은 서버에 고정시키거나, ② Redis Pub/Sub·Kafka·NATS 같은 메시지 브로커를 노드 사이에 두고 이벤트를 모든 노드에 fan-out한 뒤 각 노드가 자기 소켓에 연결된 클라이언트에게만 broadcast한다.
- 예: 노드 5대, 노드당 최대 20,000 연결이면 총 100,000 동시 접속을 수용할 수 있다. 특정 room에 메시지가 발행되면 브로커가 5개 노드 모두에 전달하고, 각 노드는 자신에게 연결된 그 room 멤버에게만 최종 전송한다.

### 비유
- 택배 조회 페이지를 계속 새로고침하는 대신, 기사와 무전기를 연결해두고 위치가 바뀔 때마다 바로 듣는 것과 같다 — 한 번 연결(handshake)하면 그 회선으로 계속 대화(frame 교환)할 수 있다.

### 흔한 오해·주의점
- WebSocket 자체는 메시지 브로커나 Pub/Sub 시스템이 아니다 — 단일 연결의 전송 프로토콜일 뿐이며, 여러 서버 사이의 메시지 전파는 Redis/Kafka 같은 별도 인프라가 있어야 한다.
- "HTTP와 완전히 다른 프로토콜"이라는 것도 부정확하다 — 시작(handshake)은 HTTP 요청·응답 형식을 그대로 쓰고, 전환 이후에만 별도의 프레임 형식으로 바뀐다.

## 연결 개념
- HTTP Upgrade — WebSocket 연결을 시작시키는 절차 그 자체
- Server-Sent Events(SSE) — 서버→클라이언트 단방향 push만 필요할 때의 더 가벼운 대안
- Pub/Sub(Redis, Kafka, NATS) — 다중 서버 환경에서 WebSocket 메시지를 fan-out하는 데 쓰이는 기반 인프라

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

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
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
