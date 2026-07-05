---
title: 웹 소켓 및 실시간 통신 (Web Socket)
date: 2026-07-05
tags: ["cspe-software"]
weight: 58
---

## Ⅰ. 개요
- 정의: 단일 TCP 연결을 통해 클라이언트와 서버 간 풀 듀플렉스(Full-duplex) 통신을 제공하는 규격.
- 출제 의도: HTTP의 단방향/무상태 한계를 극복한 실시간 양방향 데이터 전송 메커니즘 이해도 측정.

## Ⅱ. 구성요소
- ASCII 구조도
  [ Client ] <--- HTTP Upgrade Request ---> [ Server ]
     |                                          |
     | <========= WebSocket Connection ======== > |
     |          (Bi-directional, Binary/Text)   |
- 구성요소 표
| 구성요소 | 설명 | 비유 |
| :--- | :--- | :--- |
| Handshake | HTTP를 통해 연결을 시작하고 프로토콜을 전환하는 단계 | 통화 시작 벨소리 |
| Framing | 데이터를 작은 프레임 단위로 나누어 전송하는 방식 | 대화의 문장 단위 |
| Full-duplex | 서버와 클라이언트가 동시에 데이터를 주고받는 상태 | 전화 대화 |
> 요약: 연결을 한 번 맺으면 명시적으로 닫을 때까지 상시 통로를 유지함.

## Ⅲ. 절차
- ASCII 흐름도
  [HTTP GET Upgrade] -> [101 Switching] -> [Data Streaming] -> [Close]
- 4단계 설명
1. 클라이언트가 특정 헤더(Upgrade: websocket)를 담아 HTTP 요청을 보냄.
2. 서버가 동의하면 `101 Switching Protocols` 응답으로 연결을 승격함.
3. 이후 HTTP 헤더 없이 경량화된 프레임 형태로 양방향 데이터 교환함.
4. 주기적인 Ping/Pong 프레임을 통해 연결의 생존 여부(Keep-alive) 확인함.
> 요약: 오버헤드가 적은 지속적 연결을 통해 실시간성 보장함.

## Ⅳ. 문제점
- 연결 유지 비용: 수많은 동시 접속 발생 시 서버의 메모리 및 소켓 자원 고갈됨.
- 프록시 호환성: 일부 보안 장비나 프록시가 웹소켓의 지속 연결을 차단하거나 끊을 수 있음.

## Ⅴ. 개선방안
- 로드밸런싱 최적화: L7 로드밸런서에서 웹소켓 지원 설정 및 Sticky Session 활용함.
- Fallback 메커니즘: 연결 실패 시 Long Polling이나 SSE(Server-Sent Events)로 자동 전환함.

## Ⅵ. 전망
- HTTP/3(QUIC)의 등장으로 스트림 기반의 더 빠르고 안정적인 양방향 통신으로 발전 중임.
- 메타버스, 클라우드 게이밍 등 초저지연 데이터 동기화가 핵심인 산업의 근간 기술로 활용됨.
- WebTransport 등 웹소켓의 한계를 개선한 새로운 차세대 전송 표준과의 경쟁 및 공존 예상됨.
