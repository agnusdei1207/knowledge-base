---
sidebar:
  order: 178
  label: "178. 웹 소켓•Server-Sent Events (WebSocket SSE)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "웹 소켓•Server-Sent Events (WebSocket SSE)"
date: "2026-08-10T10:00:00+09:00"
tags:
  - "notes-software"
weight: 178
extra:
  question_no: "178"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "양방향•단방향과 재접속 복구 비교"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **WebSocket (웹 소켓)**: 단일 TCP 연결 위에서 클라이언트와 서버가 비동기적으로 동시에(전이중, Full-Duplex) 양방향 메시지를 주고받는 표준 프로토콜.
- **SSE (Server-Sent Events)**: 서버가 클라이언트에게 단방향으로 텍스트 이벤트를 연속적으로 푸시(Push)하기 위한 HTML5 표준 HTTP 기반 통신 기술.
- **Polling / Long Polling (폴링)**: 클라이언트가 주기적으로 서버에 새 데이터가 있는지 HTTP 요청을 날리는 구형 방식으로, 불필요한 네트워크 트래픽과 서버 부하 유발.

</details>

- 정의/개념: HTTP의 단방향/비지속성 한계를 극복하고 실시간 양방향 통신을 구현하는 **WebSocket**과, 서버의 단방향 데이터 푸시에 최적화된 **SSE** 통신 아키텍처
- 배경/필요성: 주식 호가, 채팅, 실시간 알림 등 즉각적인 상태 갱신이 필요한 서비스에서 전통적인 폴링(Polling) 방식의 오버헤드와 지연 시간 한계성 극복

#### 한줄 요약

- 웹소켓은 서로 말하는 전화이고 SSE는 서버가 번호를 붙여 계속 보내는 방송이라 통신 방향부터 다르다.

## Ⅱ. 특징 (실시간 통신 방식별 핵심 차별성)

<details><summary>핵심 용어</summary>

- **Handshake (핸드셰이크)**: WebSocket 연결 수립 시 클라이언트가 HTTP로 먼저 요청(`Upgrade: websocket`)을 보내고 서버가 수락(101 Switching Protocols)하여 프로토콜을 전환하는 초기화 과정.

</details>

- **WebSocket**: Full-Duplex(전이중 양방향), Binary/Text 데이터 포맷 지원, 독자적 프로토콜(`ws://`, `wss://`)
- **SSE**: Simplex(서버 $\rightarrow$ 클라이언트 단방향), Text(UTF-8) 전용 포맷 지원, HTTP 프로토콜(`http://`, `https://`) 유지
- **Connection Keeping (연결 유지)**: 두 기술 모두 한 번 연결된 TCP 세션을 종료하지 않고 계속 열어두어(Keep-Alive) 패킷 오버헤드 최소화

#### 한줄 요약

- 연결을 오래 유지하면 새 요청을 반복하지 않아도 되지만 끊긴 위치와 느린 수신자의 버퍼를 별도로 관리해야 한다.

## Ⅲ. 구조 및 구성요소 (WebSocket vs SSE 아키텍처 비교)

<details><summary>핵심 용어</summary>

- **Event Stream (이벤트 스트림)**: SSE에서 서버가 내려보내는 데이터 포맷으로, `event: (이름)\n data: (값)\n\n` 형태의 MIME 타입 `text/event-stream` 규칙을 따르는 메시지 구조.

</details>

```text
┌─────────────────────────┐       ┌─────────────────────────┐
│  WebSocket Architecture │  VS   │     SSE Architecture    │
├─────────────────────────┤       ├─────────────────────────┤
│ [Client]      [Server]  │       │ [Client]      [Server]  │
│    │             │      │       │    │             │      │
│    ├─(Handshake)►│      │       │    ├─(HTTP GET)─►│      │
│    │◄─(Upgrade)──┤      │       │    │             │      │
│    │◄──(Msg 1)───┤      │       │    │◄─(Event 1)──┤      │
│    ├───(Msg 2)──►│      │       │    │             │      │
│    │◄──(Msg 3)───┤      │       │    │◄─(Event 2)──┤      │
└─────────────────────────┘       └─────────────────────────┘
```

선의 의미: WebSocket은 업그레이드 후 양방향(화살표 교차)으로 메시지를 자유롭게 교환하며, SSE는 일반 HTTP GET 요청 후 서버가 일방적으로(화살표 단방향) 데이터를 쏟아내는 구조적 차이.

| 구성요소 | WebSocket 메커니즘 | SSE 메커니즘 |
|:---|:---|:---|
| **통신 방향** | **양방향 통신 (클라이언트 ↔ 서버)**| **단방향 통신 (서버 $\rightarrow$ 클라이언트)**|
| **전송 포맷** | **텍스트 및 바이너리(Blob, ArrayBuffer)** | **순수 텍스트(JSON) 전용** |
| **재접속(Reconnect)** | 직접 구현 필요 (라이브러리 의존) | **브라우저 차원의 자동 재접속 내장** |
| **인프라 제약** | 프록시/L7 로드밸런서 설정 복잡 (`Upgrade` 지원 필요) | 일반 HTTP 프록시 및 L7 호환성 우수 |

#### 한줄 요약

- 실시간 게이트웨이가 연결을 받고 핸들러가 통신 방식을 처리하며 브로커는 다른 서버의 사건을 전달하고 재생 저장소는 끊긴 동안의 방송을 보관한다.

## Ⅳ. 흐름도 (SSE 자동 복구 및 WebSocket 메시지 흐름)

<details><summary>핵심 용어</summary>

- **Last-Event-ID (마지막 이벤트 식별자)**: SSE 연결이 끊겼다가 자동 재접속할 때, 브라우저가 HTTP 헤더에 담아 보내는 마지막 수신 메시지 번호로 유실된 데이터의 재전송을 요청하는 메커니즘.

</details>

```text
[SSE 흐름 (단방향 푸시 & 자동 복구)]
[Client]                                [Server (SSE Handler)]
   ├─ 1. HTTP GET /stream ──────────────►│
   │◄─ 2. 응답 (text/event-stream) ─────┤
   │◄─ 3. data: {"msg":"A"} id: 1 ──────┤
   │  (네트워크 단절)
   │
   ├─ 4. HTTP GET (Last-Event-ID: 1) ───►│
   │◄─ 5. data: {"msg":"B"} id: 2 ──────┤ (2번부터 재전송)

[WebSocket 흐름 (양방향 상태 동기화)]
[Client]                                [Server (WS Handler)]
   ├─ 1. HTTP GET (Upgrade: websocket) ─►│
   │◄─ 2. HTTP 101 Switching Protocols ─┤
   ├─ 3. [Frame] 텍스트 입력 "Hello" ───►│ (수신 및 가공)
   │◄─ 4. [Frame] 텍스트 수신 "Hello!" ─┤
```

### 동작 원리

1. **WebSocket**: 연결(101 Upgrade)이 수립되면 양측은 커넥션이 유지되는 한 상대방에게 언제든 프레임(Frame) 단위로 데이터를 푸시.
2. **SSE**: 클라이언트가 스트림을 열면 서버가 데이터를 계속 밀어내며, 연결이 끊기면 클라이언트는 브라우저 내부 동작으로 `Last-Event-ID`를 들고 재접속 시도.
3. **Recovery**: SSE 서버는 `Last-Event-ID` 이후의 이벤트를 큐에서 꺼내어 내려줌 (**재접속 상태 복구 완결**).

#### 한줄 요약

- 클라이언트가 마지막 방송 번호를 보내면 서버는 누락분을 먼저 재생하고 이후 새 사건을 같은 연결로 이어 보낸다.

## Ⅴ. 종류 및 비교 (도입 시나리오별 기술 비교)

<details><summary>핵심 용어</summary>

- **Socket.io (소켓 아이오)**: 순수 WebSocket API의 복잡한 재접속, 폴링 폴백(Fallback), 네임스페이스 등을 추상화하여 제공하는 강력한 Node.js 기반 실시간 통신 라이브러리.

</details>

| 시나리오 | WebSocket 우선 | SSE 우선 |
|:---|:---|:---|
| **채팅 / 다중 멀티플레이 게임** | **O (클라이언트의 잦은 데이터 송신 필수)** | X (단방향 푸시만 가능) |
| **주식 호가창 / 실시간 피드** | $\triangle$ (오버스펙 및 프록시 설정 복잡) | **O (단방향 텍스트 전송 최적화)** |
| **바이너리 파일(이미지) 스트리밍**| **O (이진 데이터 프레임 완벽 지원)** | X (텍스트 전용) |
| **푸시 알림 (Push Notification)** | $\triangle$ | **O (자동 재접속 기능 강력)** |

#### 한줄 요약

- 공동 편집처럼 양쪽이 자주 보내면 웹소켓을, 진행률 알림처럼 서버가 보내기만 하면 SSE를 우선 선택한다.

## Ⅵ. 실무 고려사항 및 대책 (실시간 통신 3대 실무 난제 대책)

<details><summary>핵심 용어</summary>

- **Heartbeat / Ping-Pong (하트비트)**: L4/L7 로드밸런서 장비들이 오랫동안 데이터가 없는 유휴(Idle) TCP 커넥션을 강제로 끊는 것을 방지하기 위해 클라이언트와 서버가 주고받는 생존 확인 신호.

</details>

| 3대 실무 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 유휴 연결 강제 종료** | LB/Proxy 장비의 Idle Timeout 설정 | **서버/클라이언트 간 주기적인 Ping-Pong (하트비트) 발송** |
| **2. 다중 서버 상태 공유** | 로드밸런싱으로 인해 접속 서버가 다름 | **Redis Pub/Sub 또는 Kafka를 활용한 백엔드 메시지 버스 구축**|
| **3. 재배포 시 트래픽 폭주**| 배포 시 전체 연결이 끊기며 동시 접속 시도| **Connection Draining(점진 종료) 및 재접속 시 Jitter(지연 난수) 적용**|

> 사례: **Slack 채팅 시스템의 WebSocket 기반 양방향 버스 아키텍처 및 토스증권의 호가창 SSE 기반 단방향 푸시 적용**

#### 한줄 요약

- 서버 배포 전에 기존 연결을 천천히 비우고 재접속 시간을 분산해야 수천 개 클라이언트가 동시에 새 서버를 압박하지 않는다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Backpressure (역압)**: 통신 과정에서 데이터를 수신하는 측이 처리할 수 있는 양보다 데이터를 보내는 측의 전송 속도가 너무 빠를 때, 서버/클라이언트 메모리 고갈(OOM)을 막기 위해 흐름을 제어하는 기법.

</details>

- **실시간 통신 기준**에 따라 **메시지 흐름 방향(양/단방향)** 및 **바이너리 취급 여부**를 기준으로 WebSocket과 SSE를 전략적으로 분리 도입 필수

#### 한줄 요약

- 양방향·이진 교환은 웹소켓으로, 서버 텍스트 알림은 SSE로 구성하고 둘 다 ID·하트비트·역압 정책을 마련해야 한다.
