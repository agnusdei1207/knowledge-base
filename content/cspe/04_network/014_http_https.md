---
title: "HTTP/HTTPS (HyperText Transfer Protocol / Secure)"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 14
---

## Ⅰ. 개요
- **정의**: 웹 자원을 요청·응답 방식으로 전송하는 L7 프로토콜이며, HTTPS는 TLS 암호화를 적용한 확장임
- **배경/필요성**: 분산된 하이퍼텍스트 문서를 표준화된 방식으로 교환할 체계가 필요하며, 평문 전송의 도청 위험으로 암호화가 요구됨
- **비유**: HTTP는 엽서(내용 노출), HTTPS는 봉인된 편지(내용 보호)와 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| HTTP 동작 원리와 HTTPS 보안 계층 | 요청/응답 구조, 상태 코드, TLS 핸드셰이크 | HTTP/1.1 Keep-Alive와 HTTP/2 멀티플렉싱 차이 (015 참조) |

> 요약: 웹 자원 전송의 표준 프로토콜이며, HTTPS는 TLS로 기밀성·무결성을 보장함

## Ⅱ. 구성요소
```text
Client --- HTTP Request ---> Server
  |    (Method/URI/Headers/Body)   |
  |                                |
  |<-- HTTP Response -------------|
       (Status/Headers/Body)
       
HTTPS: Client <--TLS Tunnel--> Server 위에 HTTP 동작
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Request Method | GET, POST, PUT, DELETE 등 자원 조작 동사 | 주문서의 행동 지시란 |
| Status Code | 1xx~5xx 범위의 처리 결과 코드 (200 OK, 404 Not Found 등) | 주문 접수 결과 알림 |
| Header | 메타데이터 전달 (Content-Type, Cache-Control 등) | 편지 봉투의 부가 정보 |
| TLS 계층 | 인증서 기반 암호화·서버 인증을 제공 (017 참조) | 편지를 봉인하는 밀봉 장치 |

> 요약: 요청 메서드-상태 코드-헤더-TLS의 4요소로 웹 통신을 구성함

## Ⅲ. 절차
```text
Client          Server
  |--TCP 3-way Handshake-->|
  |--TLS Handshake-------->|  (HTTPS만)
  |--HTTP Request--------->|
  |<-HTTP Response---------|
  |--Connection Close----->|  (또는 Keep-Alive 유지)
```
- 1단계: TCP 3-way Handshake로 전송 계층 연결 수립
- 2단계: HTTPS인 경우 TLS Handshake로 암호화 채널 수립 (017 참조)
- 3단계: 클라이언트가 HTTP Request(메서드, URI, 헤더, 바디) 전송
- 4단계: 서버가 요청 처리 후 HTTP Response(상태 코드, 헤더, 바디) 반환

> 요약: TCP 연결-TLS 협상-요청-응답의 4단계로 웹 자원을 교환함

## Ⅳ. 문제점
- Head-of-Line Blocking: 하나의 요청 지연이 후속 요청을 차단함 — HTTP/1.1은 파이프라이닝을 지원하나 순서 보장 제약으로 실효성 부족
- 평문 전송 위험: HTTP는 데이터가 평문으로 노출됨 — 중간자 공격(MITM)으로 도청·변조가 가능
- 연결 오버헤드: 요청마다 TCP+TLS 핸드셰이크가 반복됨 — 지연 시간(latency)이 누적되어 사용자 체감 성능 저하

> 요약: 순차 처리 병목, 평문 노출, 연결 반복 비용이 주요 한계임

## Ⅴ. 개선방안
1. 단기: HTTP/2 멀티플렉싱 도입으로 HOL Blocking 완화 (015 참조)
2. 중기: 전 사이트 HTTPS 전환 및 HSTS 정책 적용으로 평문 전송 제거
3. 장기: HTTP/3(QUIC) 전환으로 0-RTT 연결 수립 및 TCP 의존 제거 (015, 016 참조)

> 요약: 멀티플렉싱, HTTPS 강제화, QUIC 전환의 단계적 개선이 필요함

## Ⅵ. 전망
- 발전 방향: HTTP/3 표준화 완료로 QUIC 기반 웹 통신이 확산되는 추세임
- 기술사적 판단: HTTPS는 선택이 아닌 기본값이 되었으며 인증서 자동화(ACME)가 보편화됨
- 기술사 제언: 프로토콜 버전별 특성을 이해하고 서비스 요구에 맞는 선택이 필요함
