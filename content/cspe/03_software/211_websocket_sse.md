---
title: "WebSocket SSE (WebSocket SSE)"
date: "2026-07-05"
tags:
  - "cspe-software"
weight: 211
---

## Ⅰ. 개요
- **정의**: 서버-클라이언트 간 실시간 양방향 또는 단방향 푸시 통신 프로토콜
- **배경/필요성**: HTTP 폴링은 불필요한 요청을 반복하여 지연과 자원 낭비를 유발하므로 서버가 능동적으로 데이터를 전송하는 방식이 필요함
- **비유**: WebSocket은 전화 통화(양방향), SSE는 라디오 방송(서버→클라이언트 단방향)

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 두 기술의 차이와 적용 시나리오 구분 | 통신 방향성·프로토콜 차이 | SSE는 HTTP 기반, WebSocket은 별도 프로토콜임을 혼동하지 않을 것 |

> 요약: HTTP 폴링의 한계를 극복하는 실시간 푸시 통신 기술임

## Ⅱ. 구성요소
```text
Client --HTTP Upgrade--> Server
  |                        |
  |<== WebSocket(TCP) ===>|  (양방향 전이중)
  |                        |
  |<-- SSE(HTTP Stream) --|  (서버->클라이언트 단방향)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| WebSocket | TCP 위 전이중 프레임 프로토콜, `ws://` 스킴 사용 | 양쪽이 말하는 전화 |
| SSE | HTTP/1.1 `text/event-stream` 응답으로 서버가 이벤트를 스트리밍함 | 일방향 라디오 수신 |
| Heartbeat | 연결 유지 확인용 주기적 핑/퐁 메시지 | 생존 신호 |

> 요약: WebSocket은 전이중 TCP 채널, SSE는 HTTP 스트림 기반 단방향 푸시임

## Ⅲ. 절차
```text
Handshake --> Connection --> Data Transfer --> Close
```
- 1단계: Handshake — WebSocket은 HTTP 101 Upgrade, SSE는 표준 HTTP GET 요청
- 2단계: Connection — 지속 연결 수립, WebSocket은 TCP 프레이밍, SSE는 chunked 응답
- 3단계: Data Transfer — 메시지 송수신(WebSocket) 또는 이벤트 수신(SSE)
- 4단계: Close — 명시적 종료 프레임 전송 또는 연결 해제

> 요약: 핸드셰이크 후 지속 연결을 통해 데이터를 실시간 전송하고 종료하는 4단계임

## Ⅳ. 문제점
- 연결 유지 비용: 다수 클라이언트의 상시 연결이 서버 소켓 자원을 점유함
- 로드밸런서 호환성: L7 장비가 장기 연결을 유휴로 판단하여 강제 종료할 수 있음
- 방화벽 차단: 기업 네트워크에서 WebSocket 포트나 Upgrade 헤더를 차단하는 경우 존재함

> 요약: 상시 연결 유지에 따른 자원·인프라 호환성 문제가 핵심임

## Ⅴ. 개선방안
1. 단기: 연결 풀링과 idle timeout 조정으로 소켓 자원 효율화
2. 중기: WebSocket 인지 로드밸런서(L7 sticky) 도입으로 연결 안정성 확보
3. 장기: HTTP/2 기반 SSE 또는 gRPC 스트리밍으로 방화벽 친화적 전환

> 요약: 자원 관리, 인프라 호환, 프로토콜 현대화 순으로 개선함

## Ⅵ. 전망
- 발전 방향: HTTP/3(QUIC) 위 스트리밍이 WebSocket을 점진적으로 대체할 가능성 존재
- 기술사적 판단: 채팅·알림은 WebSocket, 대시보드·피드는 SSE로 용도별 선택이 합리적임
- 기술사 제언: 서비스 특성에 맞는 프로토콜 선택 기준을 아키텍처 설계 단계에서 수립할 필요
