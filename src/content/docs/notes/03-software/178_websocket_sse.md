---
sidebar:
  order: 178
  label: "178. 웹 소켓•Server-Sent Events (WebSocket SSE)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "웹 소켓•Server-Sent Events (WebSocket SSE)"
date: "2026-08-14T03:44:00+09:00"
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

<details><summary>용어 설명</summary>

- **WebSocket (웹 소켓)**: 단일 TCP 연결 위에서 클라이언트와 서버가 비동기적으로 동시에(전이중, Full-Duplex) 양방향 메시지를 주고받는 표준 프로토콜.
- **SSE (Server-Sent Events)**: 서버가 클라이언트에게 단방향으로 텍스트 이벤트를 연속적으로 푸시(Push)하기 위한 HTML5 표준 HTTP 기반 통신 기술.
- **Polling / Long Polling (폴링)**: 클라이언트가 주기적으로 서버에 새 데이터가 있는지 HTTP 요청을 날리는 구형 방식으로, 불필요한 네트워크 트래픽과 서버 부하 유발.

</details>

- 정의/개념: 양방향 **WebSocket**과 Server 단방향 **SSE** 실시간 통신
- 배경/필요성: 반복 Polling은 **빈 요청 Traffic•갱신 지연** 발생

#### 한줄 요약

- 웹소켓은 서로 말하는 전화이고 SSE는 서버가 번호를 붙여 계속 보내는 방송이라 통신 방향부터 다르다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Handshake (핸드셰이크)**: WebSocket 연결 수립 시 클라이언트가 HTTP로 먼저 요청(`Upgrade: websocket`)을 보내고 서버가 수락(101 Switching Protocols)하여 프로토콜을 전환하는 초기화 과정.

</details>

- **WebSocket**: Full-Duplex(전이중 양방향), Binary/Text 데이터 포맷 지원, 독자적 프로토콜(`ws://`, `wss://`)
- **SSE**: Simplex(서버 $\rightarrow$ 클라이언트 단방향), Text(UTF-8) 전용 포맷 지원, HTTP 프로토콜(`http://`, `https://`) 유지
- **Connection Keeping (연결 유지)**: 두 기술 모두 한 번 연결된 TCP 세션을 종료하지 않고 계속 열어두어(Keep-Alive) 패킷 오버헤드 최소화

#### 한줄 요약

- 연결을 오래 유지하면 새 요청을 반복하지 않아도 되지만 끊긴 위치와 느린 수신자의 버퍼를 별도로 관리해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Event Stream (이벤트 스트림)**: SSE에서 서버가 내려보내는 데이터 포맷으로, `event: (이름)\n data: (값)\n\n` 형태의 MIME 타입 `text/event-stream` 규칙을 따르는 메시지 구조.

</details>

```text
[Real-time Delivery]
 ├── [Connection Gateway]
 ├── [Protocol Handler]
 ├── [Message Broker]
 └── [Replay Store]
```

| 구성요소 | 책임 |
|---|---|
| Connection Gateway | Handshake•인증과 **장기 연결 수명주기** 관리 |
| Protocol Handler | WebSocket Frame 또는 **SSE Event** 처리 |
| Message Broker | Server 간 **실시간 Event Fan-out** 제공 |
| Replay Store | Event ID별 **누락 Message 재생** 지원 |

#### 한줄 요약

- 실시간 게이트웨이가 연결을 받고 핸들러가 통신 방식을 처리하며 브로커는 다른 서버의 사건을 전달하고 재생 저장소는 끊긴 동안의 방송을 보관한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Last-Event-ID (마지막 이벤트 식별자)**: SSE 연결이 끊겼다가 자동 재접속할 때, 브라우저가 HTTP 헤더에 담아 보내는 마지막 수신 메시지 번호로 유실된 데이터의 재전송을 요청하는 메커니즘.

</details>

```text
[SSE 연결 요청]
      │
      ▼
1. Event Stream 설정
      │
      ▼
2. ID 포함 Event 전송
      │
   [연결 단절]
      │
      ▼
3. Last-Event-ID로 재접속
      │
      ▼
4. 누락 Event 재생
      │
      ▼
5. Live Stream 전환
      │
      ▼
[SSE 전달 지속]
```

### 동작 원리

1. Event Stream 설정: HTTP 응답을 지속 Stream으로 유지
2. ID 포함 Event 전송: 재생 가능한 단조 Event ID 부여
3. Last-Event-ID로 재접속: 마지막 수신 위치 전달
4. 누락 Event 재생: 저장된 다음 ID부터 순서대로 전송
5. Live Stream 전환: Backlog 소진 후 신규 Event 전달

#### 한줄 요약

- 클라이언트가 마지막 방송 번호를 보내면 서버는 누락분을 먼저 재생하고 이후 새 사건을 같은 연결로 이어 보낸다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Socket.io (소켓 아이오)**: 순수 WebSocket API의 복잡한 재접속, 폴링 폴백(Fallback), 네임스페이스 등을 추상화하여 제공하는 강력한 Node.js 기반 실시간 통신 라이브러리.

</details>

| 시나리오 | WebSocket 우선 | SSE 우선 |
|:---|:---|:---|
| 채팅 / 다중 멀티플레이 게임 | **O (클라이언트의 잦은 데이터 송신 필수)** | X (단방향 푸시만 가능) |
| 주식 호가창 / 실시간 피드 | $\triangle$ (오버스펙 및 프록시 설정 복잡) | **O (단방향 텍스트 전송 최적화)** |
| 바이너리 파일(이미지) 스트리밍 | **O (이진 데이터 프레임 완벽 지원)** | X (텍스트 전용) |
| 푸시 알림  | $\triangle$ | **O (자동 재접속 기능 강력)** |

#### 한줄 요약

- 공동 편집처럼 양쪽이 자주 보내면 웹소켓을, 진행률 알림처럼 서버가 보내기만 하면 SSE를 우선 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Heartbeat / Ping-Pong (하트비트)**: L4/L7 로드밸런서 장비들이 오랫동안 데이터가 없는 유휴(Idle) TCP 커넥션을 강제로 끊는 것을 방지하기 위해 클라이언트와 서버가 주고받는 생존 확인 신호.

</details>

| 3대 실무 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. 유휴 연결 강제 종료 | LB/Proxy 장비의 Idle Timeout 설정 | **서버/클라이언트 간 주기적인 Ping-Pong (하트비트) 발송** |
| 2. 다중 서버 상태 공유 | 로드밸런싱으로 인해 접속 서버가 다름 | **Redis Pub/Sub 또는 Kafka를 활용한 백엔드 메시지 버스 구축**|
| 3. 재배포 시 트래픽 폭주 | 배포 시 전체 연결이 끊기며 동시 접속 시도| **Connection Draining(점진 종료) 및 재접속 시 Jitter(지연 난수) 적용**|

> 사례: **Slack 채팅 시스템의 WebSocket 기반 양방향 버스 아키텍처 및 토스증권의 호가창 SSE 기반 단방향 푸시 적용**

#### 한줄 요약

- 서버 배포 전에 기존 연결을 천천히 비우고 재접속 시간을 분산해야 수천 개 클라이언트가 동시에 새 서버를 압박하지 않는다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Backpressure (역압)**: 통신 과정에서 데이터를 수신하는 측이 처리할 수 있는 양보다 데이터를 보내는 측의 전송 속도가 너무 빠를 때, 서버/클라이언트 메모리 고갈(OOM)을 막기 위해 흐름을 제어하는 기법.

</details>

- 양방향•Binary는 **WebSocket**, Server Text Push는 SSE 선택

#### 한줄 요약

- 양방향·이진 교환은 웹소켓으로, 서버 텍스트 알림은 SSE로 구성하고 둘 다 ID·하트비트·역압 정책을 마련해야 한다.
