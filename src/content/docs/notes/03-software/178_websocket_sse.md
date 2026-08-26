---
sidebar:
  order: 178
  label: "178. 웹 소켓•Server-Sent Events"
  badge:
    text: "미출 · 50%"
    variant: note
title: "웹 소켓•Server-Sent Events (WebSocket SSE)"
date: "2026-08-26T13:22:35+09:00"
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

- **WebSocket**: 단일 TCP 연결 위에서 클라이언트와 서버가 전이중(Full-Duplex)으로 양방향 통신을 수행하는 프로토콜(`ws://`, `wss://`).
- **SSE (Server-Sent Events)**: 표준 HTTP 연결을 통해 서버가 클라이언트에게 단방향으로 텍스트 이벤트를 실시간 푸시하는 HTML5 기술(`text/event-stream`).

</details>

- 정의/개념: 단일 지속 연결 위에서 **양방향 전이중 통신을 제공하는 WebSocket과 서버 단방향 푸시 스트리밍을 제공하는 SSE 실시간 통신 기술**
- 배경/필요성: 주기적 HTTP 폴링(Polling) 방식에서 발생하는 **빈 요청 트래픽 낭비, 서버 연결 오버헤드 및 실시간 갱신 지연 해결 불가**

#### 한줄 요약
- 양방향 상호작용은 WebSocket, 서버 단방향 푸시는 SSE를 적용하여 실시간 웹 서비스를 구현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **101 Switching Protocols**: WebSocket 연결 수립을 위해 HTTP 요청 헤더(`Upgrade: websocket`)를 전송하고 프로토콜을 전환하는 핸드셰이크 응답.
- **text/event-stream**: SSE에서 서버가 연결을 끊지 않고 지속적으로 이벤트를 밀어넣기 위해 사용하는 표준 MIME 타입.

</details>

- 지속 연결에서 프레임 기반 양방향 통신을 지원하는 **WebSocket**
- 표준 HTTP/HTTPS 포트(80/443)를 그대로 재사용하여 방화벽 친화적인 **SSE 단방향 푸시**
- 브라우저 자동 재접속과 서버 구현 기반 **Last-Event-ID 재생**

#### 한줄 요약
- 전이중 양방향 통신(WebSocket)과 HTTP 기반 단방향 스트리밍(SSE)이 각각의 영역을 담당한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **실시간 통신 4대 인프라 요소**: Connection Gateway(연결 관리), Protocol Handler(프레임/이벤트 처리), Message Broker(Redis Pub/Sub), Replay Store(누락 복구).

</details>

```text
[WebSocket 및 SSE 실시간 스트리밍 아키텍처]
├── Client Layer (Browser / Mobile App)
│   ├── WebSocket: ws.send() / ws.onmessage() (양방향 프레임 통신)
│   └── SSE: new EventSource('/stream') (단방향 이벤트 수신)
├── Real-time Gateway & Protocol Handler Layer
│   ├── WebSocket Handler (HTTP Upgrade 101 전환 및 양방향 TCP 소켓 관리)
│   └── SSE Handler (MIME: text/event-stream 청크 응답 유지)
├── Message Broker & Fan-out Layer (Redis Pub/Sub / Apache Kafka)
└── Replay Store Layer (Event ID별 누락 메시지 임시 버퍼링)
```

선의 의미: 계층 및 클라이언트의 연결을 게이트웨이가 수립하고 백엔드 Redis Pub/Sub을 통해 다중 인스턴스 간 실시간 이벤트를 전파하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 연결 게이트웨이 | 핸드셰이크·인증·연결 수명주기 관리 |
| 프로토콜 핸들러 | WebSocket 프레임·**SSE 이벤트** 인코딩 |
| 메시지 브로커 | 인스턴스 간 메시지 Fan-out |
| 재생 저장소 | Last-Event-ID 기준 누락 이벤트 조회 |

#### 한줄 요약
- 연결 게이트웨이, 프로토콜 핸들러, 메시지 브로커, 재생 저장소가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **SSE 재접속**: 스트림 수립, 이벤트 전송, 단절, Last-Event-ID 재접속.

</details>

```text
클라이언트의 실시간 피드 구독 요청
        │
   1. [Event Stream 수립] 클라이언트가 `GET /events` 요청 후 서버가 `text/event-stream` 응답 유지
        │
   2. [이벤트 푸시] 서버가 단조 증가 `id: 101`을 포함한 JSON 이벤트를 지속 전송
        │
   3. [네트워크 단절] 모바일 음영지역 진입으로 TCP 연결 일시 단절 발생
        │
   4. [자동 재접속] 브라우저 EventSource가 헤더에 `Last-Event-ID: 101`을 담아 자동 재연결
        │
   서버가 재생 저장소에서 `id: 102~105` 누락분을 즉시 회신하고 라이브 스트림으로 복귀
```

동작 원리:

1. Event Stream 수립: text/event-stream 연결 유지
2. 이벤트 푸시: Event ID와 데이터 전송
3. 네트워크 단절: 연결 종료 감지
4. 자동 재접속: Last-Event-ID와 다시 연결

#### 한줄 요약
- Stream 수립 → 이벤트 푸시 → 단절 발생 → Last-Event-ID 재접속 → 누락 재생 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **WebSocket vs SSE**: 통신 방향, 프로토콜, 데이터 포맷, 방화벽 통과, 자동 재접속 비교.

</details>

| 비교 항목 | 웹 소켓 (WebSocket) | Server-Sent Events (SSE) |
|:---|:---|:---|
| 통신 방향성 | **전이중 양방향 (Full-Duplex: Bidirectional)** | **서버 $\rightarrow$ 클라이언트 단방향 (Simplex: Push)**|
| 프로토콜 및 포트 | **독자 프로토콜 (`ws://`, `wss://`)** | **표준 HTTP/HTTPS 프로토콜 (`http://`, `https://`)**|
| 지원 데이터 포맷 | **텍스트(UTF-8) 및 바이너리(Binary) 데이터** | **텍스트(UTF-8) 전용 포맷 (`text/event-stream`)**|
| 자동 재접속 지원 | 직접 수동 구현 (라이브러리 필요) | **브라우저 네이티브 기본 내장 (자동 재연결)** |
| 프록시 호환성| Upgrade·타임아웃 설정 필요 | **HTTP 스트리밍·버퍼링 설정** 필요 |
| 최적 적용 사례 | **실시간 채팅, 다중 멀티플레이 게임, 화상 협업** | **주식 실시간 시세 호가창, 알림 피드, AI 응답 스트리밍**|

#### 한줄 요약
- 양방향 상호작용과 바이너리는 WebSocket, 서버 단방향 텍스트 푸시와 AI 스트리밍은 SSE를 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Idle Timeout**: L4/L7 로드밸런서가 일정 시간 트래픽이 없는 유휴 커넥션을 강제로 종료하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 로드밸런서 Idle Timeout 연결 종료 | **하트비트·타임아웃 정합** | 유휴 연결 종료 빈도 감소 |
| 다중 서버 스케일아웃 시 특정 서버 접속자에게 메시지 미전달 | **Redis Pub/Sub 또는 Kafka를 활용한 백엔드 메시지 브로드캐스트** | 전 서버 접속자에게 실시간 전파 |
| 서버 재배포 시 수만 개 클라이언트 동시 재접속 폭풍(Thundering Herd)| **Connection Draining(점진 종료) 및 재접속 시 Jitter(난수 지연) 부여** | 서버 과부하 및 다운타임 방지 |
| HTTP/1.1의 SSE 연결 수 제약 | **HTTP/2 다중화** 적용 | 연결별 스트림 운용 범위 확대 |

#### 한줄 요약
- Ping-Pong 하트비트, Redis Pub/Sub, Jitter 분산 재접속, HTTP/2 다중화로 운영한다.

## Ⅶ. 결론

- 양방향·바이너리는 **WebSocket**, 단방향 텍스트는 **SSE** 선택

#### 한줄 요약
- 재접속·재생·하트비트 정책을 프록시 타임아웃과 함께 설계한다.
