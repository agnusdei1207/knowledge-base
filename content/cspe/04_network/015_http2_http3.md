---
title: "HTTP/2, HTTP/3"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 15
---

## Ⅰ. 개요
- **정의**: HTTP/1.1의 성능 한계를 해결하기 위한 차세대 웹 전송 프로토콜(HTTP/2: TCP 멀티플렉싱, HTTP/3: QUIC 기반)
- **배경/필요성**: 웹 페이지당 수십 개 자원을 요청하는 환경에서 HTTP/1.1의 순차 처리·다중 연결 비용이 병목이 됨
- **비유**: HTTP/1.1은 1차선 도로, HTTP/2는 다차선 고속도로, HTTP/3은 비행 경로(지상 정체 회피)와 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 버전별 구조 차이와 성능 개선 원리 | 바이너리 프레이밍, 스트림 멀티플렉싱, QUIC | HTTP/2도 TCP 기반이라 TCP HOL Blocking은 잔존 |

> 요약: HTTP/2는 TCP 위 멀티플렉싱, HTTP/3은 QUIC 위 독립 스트림으로 웹 성능을 개선함

## Ⅱ. 구성요소
```text
HTTP/1.1: TCP --> Request1 --> Response1 --> Request2 --> Response2
HTTP/2  : TCP --> [Stream1 + Stream2 + Stream3] (바이너리 프레임)
HTTP/3  : QUIC(UDP) --> [Stream1 | Stream2 | Stream3] (독립 스트림)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Binary Framing | HTTP/2에서 텍스트 대신 바이너리 프레임으로 메시지 분할 전송 | 택배를 규격 박스로 포장 |
| Stream Multiplexing | 단일 연결에서 여러 요청/응답을 동시 교환 | 다차선 도로의 병렬 주행 |
| Server Push | 서버가 클라이언트 요청 없이 관련 자원을 선제 전송 (HTTP/2) | 주문 전 사이드 메뉴 제공 |
| QUIC Transport | UDP 위에 신뢰성·암호화를 내장한 전송 계층 (016 참조) | 전용 비행 경로 |

> 요약: 바이너리 프레이밍, 멀티플렉싱, QUIC의 조합으로 HTTP 성능을 개선함

## Ⅲ. 절차
```text
[HTTP/2]                         [HTTP/3]
Client        Server             Client        Server
  |--TCP+TLS----->|                |--QUIC(0/1-RTT)->|
  |--SETTINGS---->|                |--SETTINGS------>|
  |--HEADERS(S1)->|                |--HEADERS(S1)--->|
  |--DATA(S1)+    |                |--DATA(S1)+      |
  |  HEADERS(S2)->|                |  HEADERS(S2)--->|
  |<-HEADERS+DATA-|                |<-HEADERS+DATA---|
```
- 1단계: 연결 수립 — HTTP/2는 TCP+TLS, HTTP/3은 QUIC 핸드셰이크(0-RTT 가능)
- 2단계: SETTINGS 프레임 교환으로 최대 동시 스트림 수 등 파라미터 협상
- 3단계: HEADERS+DATA 프레임을 스트림 단위로 인터리빙하여 동시 전송
- 4단계: 서버가 각 스트림별 응답을 독립적으로 반환, 클라이언트가 스트림별 재조립

> 요약: 연결수립-파라미터협상-병렬전송-스트림별응답의 4단계로 동작함

## Ⅳ. 문제점
- TCP HOL Blocking 잔존: HTTP/2는 TCP 계층에서 패킷 손실 시 전체 스트림이 대기함 — 멀티플렉싱이 TCP 신뢰성 위에서 동작하기 때문
- Server Push 실효성 부족: 클라이언트 캐시 상태를 모르고 전송하여 대역폭 낭비 발생 — 실사용률 저조로 크롬에서 비활성화됨
- 중간 장비 호환성: 일부 방화벽·프록시가 QUIC(UDP 443)을 차단함 — 기존 인프라가 TCP 기반으로 설계되어 UDP 허용 정책 부재

> 요약: TCP 의존 병목, Push 비효율, UDP 차단이 주요 제약임

## Ⅴ. 개선방안
1. 단기: HTTP/3(QUIC) 전환으로 TCP HOL Blocking을 근본 제거 (016 참조)
2. 중기: 103 Early Hints 등 대안 메커니즘으로 Server Push 대체
3. 장기: 네트워크 장비의 QUIC 인식·허용 정책 표준화 및 인프라 갱신

> 요약: QUIC 전환, Push 대체, 인프라 호환성 확보의 단계적 적용이 필요함

## Ⅵ. 전망
- 발전 방향: 주요 CDN·브라우저의 HTTP/3 지원이 보편화되어 트래픽 비중이 지속 증가 중임
- 기술사적 판단: 전송 계층 혁신(QUIC)이 응용 계층 프로토콜 설계에 영향을 미치는 전환점임
- 기술사 제언: 서비스 특성(지연 민감도, 패킷 손실률)에 따라 HTTP/2·3 혼용 전략을 수립할 필요가 있음
