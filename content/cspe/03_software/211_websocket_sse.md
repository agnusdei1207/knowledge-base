---
title: "웹 소켓·Server-Sent Events (WebSocket SSE)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 211
---

# 📖 【암기용】 개념 완전 이해

> 목적: WebSocket과 SSE를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 브라우저와 서버가 HTTP 요청-응답 한계를 넘어 실시간 데이터를 주고받는 통신 방식
- **왜 필요한가**: 채팅, 주식 시세, 알림, 대시보드는 사용자가 새로고침하지 않아도 서버 이벤트가 화면에 도착해야 함
- **핵심 직관**: WebSocket은 양방향 전화, SSE는 서버가 계속 읽어주는 방송 채널임

## 깊이 이해
- **배경·문제의식**: 전통 HTTP Polling은 1초마다 요청하면 3,600req/h가 발생하고 빈 응답이 많다. Long Polling은 요청 수를 줄이나 연결 관리와 타임아웃 처리가 필요하다.
- **작동 원리**: WebSocket은 HTTP Upgrade 후 하나의 TCP 연결에서 클라이언트와 서버가 프레임을 교환한다. SSE는 `text/event-stream` 응답을 닫지 않고 서버가 이벤트를 순차 전송한다.
- **비유**: WebSocket은 서로 말할 수 있는 전화 회선, SSE는 안내 방송처럼 서버가 새 소식을 흘려보내는 구조임
- **구체 예시**: 10,000명 동시 접속 알림 서비스에서 Polling 5초 주기는 2,000req/s를 만들지만, SSE는 연결 10,000개와 이벤트 발생 시 전송으로 부하 축을 바꿈
- **흔한 오해·주의점**: SSE도 HTTP 기반 스트림이므로 단방향 서버 푸시에 적합하며, 클라이언트 명령이 많은 협업 편집은 WebSocket이 맞음

## 연결 개념
- HTTP/2 스트리밍 - 다중화와 헤더 압축 기반 실시간 전송
- 레이트 리미팅 - 연결 수와 메시지 속도 통제
- 로드 밸런싱 - 장기 연결 세션 분산

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 실시간 웹 기술 나열이 아니라, 양방향성·브라우저 지원·연결 수·장애 복구 기준으로 선택한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: WebSocket은 HTTP Upgrade 기반 양방향 전이중 통신, SSE는 HTTP 응답 스트림 기반 서버 단방향 푸시이다.
> 2. **가치**: Polling 요청 폭증을 줄이고 알림·시세·채팅에서 p95 지연 1초 이하 목표를 설계 가능하게 함.
> 3. **판단 포인트**: 양방향 명령은 WebSocket, 서버 이벤트 구독은 SSE, 프록시·재연결·인증 정책을 함께 판단해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 실시간 웹 통신 선택 역량 확인 | WebSocket 양방향, SSE 단방향, Polling 대비 요청 수 차이 | 둘을 모두 "실시간 HTTP"로만 설명하고 선택 기준 누락 |
| 운영 설계 판단 확인 | 장기 연결, LB sticky, heartbeat, reconnect, backpressure | 연결 수 산정 없이 기술명만 나열 |
| 보안·장애 통제 확인 | TLS, Origin 검증, 인증 토큰 갱신, 메시지 속도 제한 | CORS·CSRF·DoS 리스크 누락 |

> 요약: 실시간 요구를 메시지 방향, 연결 유지, 장애 복구, 보안 통제로 나누어 답안을 구성해야 한다.

---

## Ⅰ. 개요 및 필요성

WebSocket과 SSE는 웹 실시간 전송 기술이다. Polling은 요청 빈도만큼 서버 부하가 증가하므로 알림·시세·관측 대시보드에 한계가 있다. 실시간 웹은 p95 전달 지연, 동시 연결 수, 인증 갱신을 함께 설계해야 한다.

---

## Ⅱ. 구조 및 구성요소

```text
Client Browser -> HTTP Handshake
  / WebSocket Upgrade -> Persistent TCP -> Frame Send/Receive
  / SSE Response Stream -> EventSource -> Event Dispatch
Server -> Auth -> Session Registry -> Message Broker -> Observability
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| WebSocket Endpoint | Upgrade 후 양방향 프레임 송수신 | 채팅·협업 편집·게임 입력 |
| SSE Endpoint | `text/event-stream`으로 서버 이벤트 전송 | 알림·로그 tail·시세 구독 |
| Message Broker | Redis Pub/Sub, Kafka로 이벤트 팬아웃 | 파티션·순서·재전송 정책 필요 |
| Connection Registry | 사용자-연결 매핑 저장 | 노드 장애 시 재연결 유도 |

> 요약: WebSocket/SSE 구조는 장기 연결, 이벤트 중계, 연결 상태 관측으로 구성된다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Client Connect -> Auth Validate -> Channel Subscribe
-> Event Publish -> Connection Lookup -> Frame/Stream Send
-> Ack/Retry or Reconnect -> Metric Collect
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 연결 수립 및 토큰 검증 | TLS 1.3, JWT 만료 시 재인증 |
| 2 | 채널 구독과 권한 필터링 | 사용자별 topic ACL |
| 3 | 이벤트 전송과 backpressure 처리 | 큐 길이, send buffer 임계치 |
| 4 | 끊김 감지와 재연결 | heartbeat 30초, retry interval 3초 |

> 요약: 실시간 전송은 연결 수립보다 끊김 감지, 재구독, 버퍼 초과 통제가 품질을 좌우한다.

---

## Ⅳ. 특징

| 구분 | WebSocket | SSE | 판단 수치 |
|:---|:---|:---|:---|
| 통신 방향 | 클라이언트-서버 양방향 | 서버-클라이언트 단방향 | 클라이언트 명령 비율 20% 이상이면 WebSocket |
| 프로토콜 | HTTP Upgrade 후 WS 프레임 | HTTP 응답 스트림 | 프록시 호환성은 SSE가 단순 |
| 복구 | 애플리케이션 재연결 구현 | EventSource 자동 재연결 | Last-Event-ID로 누락 보정 |
| 운영 부담 | 연결 상태·스케일아웃 설계 필요 | HTTP 인프라 활용 가능 | 동시 연결 10만 단위면 커널 튜닝 필요 |

> 요약: WebSocket은 상호작용, SSE는 서버 푸시 구독에 맞고, 선택 기준은 메시지 방향과 복구 방식이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | WebSocket·SSE | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | Polling, Long Polling | 장기 연결 기반 이벤트 전송 | 빈 응답 비율 50% 이상이면 전환 |
| 비용/성능 | 요청당 헤더·인증 반복 | 연결 유지 후 이벤트만 전송 | p95 지연 1초 이하, req/s 70% 감소 목표 |
| 운영/위험 | Stateless LB 중심 | sticky 또는 connection-aware LB | 노드 재시작 시 재연결 폭주 통제 |

> 요약: 전환 여부는 실시간 지연 요구와 Polling 요청 낭비를 수치화해 판단한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 연결 고갈 | 동시 연결·파일 디스크립터 부족 | ulimit, epoll, connection quota | active connections, fd usage 80% 이하 |
| 메시지 유실 | 노드 장애 중 이벤트 전송 | broker offset, Last-Event-ID, idempotency | 재전송 성공률 99.9% |
| DoS | 연결 유지 후 메시지 폭주 | token bucket, per-IP connection cap | 차단 건수, p99 queue delay |

> 요약: 운영 리스크는 연결 자원, 유실 복구, 메시지 속도 제한으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 전달 지연 | p95 1초 이하, p99 3초 이하 | APM span, client timestamp |
| 연결 품질 | 재연결율 1%/min 이하 | gateway metric, browser log |
| 보안/운영 | Origin 검증 100%, 인증 실패 로그 | WAF, access log, SIEM |

> 요약: 도입 후 성공 여부는 지연, 재연결율, 인증·접근 로그로 판정한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 요구 분류: 채팅·협업 편집은 WebSocket, 알림·시세·대시보드는 SSE로 분리하고 p95 지연 1초 목표 설정
2. 운영 설계: Nginx idle timeout 60초 이상, heartbeat 30초, Redis Pub/Sub 또는 Kafka로 노드 간 fan-out 구성
3. 보안 통제: TLS 1.3, Origin allowlist, JWT 재발급, 사용자별 topic ACL, token bucket 100msg/min 적용

**결론 (2줄):**
- 기술사 판단: 양방향 상호작용이면 WebSocket, 서버 이벤트 구독이면 SSE, 대규모 단방향 알림이면 SSE+broker 구조 선택
- 향후 방향: HTTP/2·HTTP/3 스트리밍과 WebTransport가 저지연 전송 선택지를 확대하므로 프록시 호환성 검증 필요

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "실시간 웹 통신을 설명하시오" | Handshake, stream, reconnect 흐름 | WebSocket·SSE·Polling 비교 |
| 요구사항 명시형 | "채팅/알림 방안을 제시하시오" | 메시지 방향, 재연결, backpressure | 기술 선택 기준과 운영 지표 |

> 요약: 설명형은 프로토콜 원리, 방안형은 요구별 기술 선택과 운영 통제를 중심으로 전개한다.
