---
title: "웹 소켓·Server-Sent Events (WebSocket SSE)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 211
extra:
  question_no: "211"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- WebSocket은 HTTP Handshake 후 하나의 연결에서 Client·Server가 Text·Binary Frame을 양방향 전송하는 프로토콜임
- SSE는 Server가 `text/event-stream` 응답에 UTF-8 Event를 계속 기록하고 Browser `EventSource`가 수신하는 단방향 방식임
- WebSocket은 Ping·Pong·Close와 응용 재연결·메시지 복구를 설계해야 함
- SSE는 연결 종료 후 재접속하고 `Last-Event-ID`로 마지막 수신 지점 이후 Event를 요청할 수 있음
- 둘 다 장기 연결 수·메시지 적체·인증 만료·Proxy Timeout을 연결 수명주기와 함께 관리해야 함

## 작성 근거(검토용)

- WebSocket·SSE는 통신 방향, 연결 설정, 메시지 형식, 재연결, 상태 복구, 중계 계층, 적합 조건으로 비교함
- 구조와 절차는 Handshake·Stream·Heartbeat·재접속·종료에서 프로토콜별 상태를 설명함
- 공동 편집과 배포 로그는 왕복 지연·연결 수·재접속 시간·Event 누락 건수로 검증함

## Ⅰ. 개요

- **정의/개념**: WebSocket은 HTTP 호환 Handshake 뒤 양방향 Message Frame을 교환하고, SSE는 HTTP 응답 Stream으로 Server Event를 Client에 지속 전달하는 실시간 웹 통신 방식임
- **배경/필요성**: Polling의 반복 요청·응답 없이 상호 입력을 교환할지, Server 상태만 연속 통지할지에 따라 연결 방향·복구·중계 정책을 선택해야 함

## Ⅱ. 특징

- WebSocket은 `101 Switching Protocols` 후 Text·Binary·Continuation·Ping·Pong·Close Frame을 교환함
- Client와 Server가 독립 전송하므로 채팅·편집·제어처럼 양방향 Event가 같은 연결에 필요할 때 사용함
- SSE는 `data`·`event`·`id`·`retry` Field와 빈 줄로 Event 경계를 표현함
- `EventSource`가 연결을 재시도하고 마지막 `id`를 `Last-Event-ID`에 전달하므로 Server는 재생 보존 범위를 정해야 함
- WebSocket 메시지 순번과 SSE Event ID를 응용 상태에 연결해 재접속 후 중복·누락을 판정함
- Load Balancer의 Idle Timeout·Connection Draining과 인증 갱신을 장기 연결 종료·재접속 정책에 반영함

## Ⅲ. 종류 및 비교

| 판단 기준 | WebSocket | Server-Sent Events |
|:---|:---|:---|
| 통신 방향 | Client·Server 양방향 | Server -> Client 단방향 |
| 연결 설정 | HTTP Upgrade Handshake 후 WebSocket 연결 | HTTP GET의 `text/event-stream` 응답 유지 |
| 메시지 형식 | Text·Binary·Control Frame | UTF-8 `event`·`data`·`id`·`retry` Field |
| 연결 감지 | Ping·Pong·Close와 응용 Heartbeat | Comment Heartbeat·HTTP 연결 종료 감지 |
| 재접속·복구 | 재접속·순번·미수신 Message 처리를 응용이 정의 | EventSource 재접속과 `Last-Event-ID` 사용 |
| 중계 계층 | WebSocket Upgrade·장기 연결 지원 필요 | HTTP Streaming·Buffering 비활성화 필요 |
| 적합 조건 | 채팅·공동 편집·양방향 제어 | 알림·진행 상태·로그·Server 상태 통지 |

> 요약: WebSocket은 한 연결의 양방향 Frame, SSE는 HTTP 응답의 단방향 Event Stream과 Event ID 복구를 제공함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Handshake·HTTP Stream | WebSocket Upgrade 또는 SSE `text/event-stream` 연결을 설정함 |
| Session·Connection Registry | 사용자·연결·구독 대상·인증 만료와 소유 노드를 관리함 |
| Message·Event Encoder | WebSocket Frame 또는 SSE Field·Event ID를 직렬화함 |
| Broker·Backplane | 여러 Server Instance 사이 구독 Event와 대상 연결을 전달함 |
| Heartbeat·Timeout | 단절 연결을 감지하고 Proxy·Server Idle 종료를 방지함 |
| Replay Buffer·Sequence | 재접속 Client가 받지 못한 Message·Event 범위를 복구함 |

```text
WebSocket: Client <==== Text|Binary Frames ====> Server
SSE:       Client <---- text/event-stream ------- Server
```

> 요약: 연결 Registry와 Backplane이 대상 Session을 찾고 Frame·Event Encoder와 재생 Buffer가 전송·복구를 담당함.

## Ⅴ. 원리 및 절차 흐름도

| 처리 단계 | WebSocket | SSE |
|:---|:---|:---|
| 연결 요청 | Upgrade Header·Key·Origin·Subprotocol 전송 | `EventSource`가 HTTP GET 전송 |
| 연결 승인 | Server가 Accept·Subprotocol과 101 응답 | Server가 `text/event-stream` 응답 시작 |
| 데이터 전달 | 양쪽이 Message Frame을 독립 전송 | Server가 Event Field와 빈 줄을 순차 기록 |
| 연결 유지 | Ping·Pong·응용 Heartbeat | Comment Heartbeat·Retry 값 |
| 단절 복구 | 재접속 후 응용 Sequence로 미수신 범위 복구 | `Last-Event-ID` 이후 Event 재생 |

> 요약: 두 방식은 장기 연결을 유지하지만 WebSocket은 양방향 Frame, SSE는 Event ID가 있는 Server Stream으로 복구함.

## Ⅵ. 실무 사례

1. 공동 편집 화면은 WebSocket 순번·Heartbeat를 적용하고 p99 왕복 지연·활성 연결 수를 확인함
2. 배포 로그 화면은 SSE Event ID·재생 Buffer를 적용하고 재접속 시간·Event 누락 건수를 확인함

## Ⅶ. 결론

- 웹 실시간 통신은 양방향 입력 여부·Binary 전송·재접속 복구·장기 연결 운영 조건으로 WebSocket과 SSE를 선택해야 함
