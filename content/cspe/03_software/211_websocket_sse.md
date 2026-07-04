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
- **개요**: 브라우저와 서버가 한 번 맺은 TCP 연결을 계속 유지하는 **지속 연결(Persistent Connection)** 기반으로, HTTP 요청-응답 한계를 넘어 실시간으로 데이터를 주고받는 두 가지 표준 방식
- **왜 필요한가**: 채팅, 주식 시세, 알림, 대시보드는 사용자가 새로고침하지 않아도 서버 이벤트가 즉시 화면에 도착해야 한다. 매번 새 HTTP 요청을 여는 Polling은 헤더 비용과 빈 응답이 누적된다.
- **핵심 직관**: WebSocket은 양쪽이 동시에 말할 수 있는 전화 회선(전이중), SSE는 서버가 일방적으로 계속 읽어주는 방송 채널(단방향)이다

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어 | 의미 | 비유 |
|:---|:---|:---|
| HTTP Upgrade | 기존 HTTP 연결을 다른 프로토콜(WebSocket 등)로 전환하는 핸드셰이크 메커니즘 | 전화를 걸었다가 "이제부터 영상통화로 전환합시다"라고 방식을 바꾸는 것 |
| Persistent Connection(지속 연결) | 한 번 맺은 TCP 연결을 끊지 않고 계속 유지하며 데이터를 주고받는 방식 — WebSocket·SSE의 공통 상위 개념 | 전화를 끊지 않고 계속 통화 상태를 유지 |
| Full-duplex(전이중) | 양쪽이 동시에 보내고 받을 수 있는 통신 — WebSocket의 방식 | 동시에 말하고 들을 수 있는 일반 전화 통화 |
| Frame(WebSocket 프레임) | WebSocket이 메시지를 잘라 보내는 최소 전송 단위 | 소포를 여러 상자로 나눠 보내는 것 |
| text/event-stream | SSE 응답의 MIME 타입 — 연결을 닫지 않고 이벤트를 순차 전송 | 라디오 방송 주파수 — 채널을 유지한 채 계속 방송 |
| EventSource | 브라우저가 SSE를 구독하는 표준 JS API, 끊기면 자동 재연결 | 라디오 수신기 — 전파가 끊기면 자동으로 다시 잡음 |
| Last-Event-ID | 마지막으로 받은 이벤트 번호 — 재연결 시 이 이후 이벤트만 다시 요청 | 방송 재접속 시 "몇 번째 소식부터 들었다"고 알려주는 것 |
| Heartbeat | 연결이 살아있는지 주기적으로 확인하는 핑 메시지 | 무전기로 "여기 이상 무" 주기 보고 |
| Backpressure | 수신 측 처리 속도가 못 따라갈 때 송신 속도를 조절하는 제어 | 하수구가 막히면 수도꼭지를 잠그는 것 |
| Sticky Session | 로드밸런서가 같은 클라이언트를 항상 같은 서버로 보내는 설정 | 같은 손님을 항상 같은 담당 직원에게 배정 |

## 깊이 이해

### Polling의 비용을 숫자로 확인
- 클라이언트 1개가 1초 간격으로 Polling하면 시간당 3,600건의 요청이 발생한다. 매 요청마다 HTTP 헤더(쿠키·인증 토큰 등)가 대략 500바이트씩 오간다고 하면, 사용자 1명당 시간당 약 1.8MB가 "새 소식이 없어도" 낭비된다.
- 10,000명이 동시에 이렇게 폴링하면 시간당 3,600만 건의 요청이 서버에 몰린다 — 대부분 빈 응답인데도 서버는 매번 인증·라우팅·커넥션 생성 비용을 치른다. WebSocket·SSE는 연결을 한 번만 맺고 유지하므로 이 반복 비용이 "이벤트가 실제로 발생했을 때만" 발생하는 구조로 바뀐다.

### WebSocket 핸드셰이크 원리 — 실제 규격으로 이해
- WebSocket은 일반 HTTP 요청으로 시작해 서버가 동의하면 프로토콜을 전환(Upgrade)한다. 클라이언트는 헤더에 `Upgrade: websocket`, `Connection: Upgrade`, 그리고 무작위 16바이트를 base64 인코딩한 `Sec-WebSocket-Key`(예: `dGhlIHNhbXBsZSBub25jZQ==`)를 담아 보낸다.
- 서버는 이 키 뒤에 고정 GUID `258EAFA5-E914-47DA-95CA-C5AB0DC85B11`을 이어붙여 SHA-1 해시를 구하고 base64로 인코딩한 값을 `Sec-WebSocket-Accept` 헤더로 돌려준다(RFC 6455 규격 예제 기준 결과값은 `s3pPLMBiTxaQ9kYGzzhZRbK+xOo=`). 이 계산이 맞으면 상태코드 `101 Switching Protocols`로 응답하고, 이후로는 HTTP가 아니라 WebSocket 프레임 형식으로 같은 TCP 연결 위에서 데이터를 주고받는다.
- 이 한 번의 핸드셰이크 이후로는 매 메시지마다 HTTP 헤더를 다시 보낼 필요가 없어, 짧은 메시지를 자주 주고받는 채팅·게임 입력에서 오버헤드가 크게 줄어든다.

### SSE 포맷 원리 — 텍스트 스트림 그대로 이해
- SSE는 새 프로토콜이 아니라 평범한 HTTP 응답을 `Content-Type: text/event-stream`으로 열어두고 닫지 않는 방식이다. 서버는 이벤트가 생길 때마다 `data: {"price":100}\n\n`처럼 한 이벤트를 개행 두 번으로 구분해 흘려보낸다.
- 재연결 안정성을 위해 `id: 1024\n`처럼 이벤트 번호를 함께 보내면, 브라우저의 `EventSource`는 연결이 끊겼다 재접속할 때 `Last-Event-ID: 1024` 헤더를 자동으로 담아 보낸다 — 서버는 이 번호 이후의 이벤트만 다시 전송해 유실 없이 이어붙일 수 있다.
- `retry: 3000\n`으로 재연결 대기시간(ms)도 서버가 지정할 수 있다. 텍스트 프로토콜이라 curl이나 브라우저 개발자도구로 그대로 읽을 수 있어 WebSocket보다 디버깅이 쉽다.

### 왜 WebSocket이 운영 부담이 더 큰가 — 판별 원리
- SSE는 순수 HTTP 응답 스트림이라 기존 프록시·로드밸런서·CDN 인프라를 그대로 활용할 수 있고, 재연결도 브라우저가 자동 처리한다.
- WebSocket은 양방향 상태를 서버가 계속 들고 있어야 하고(연결마다 세션·인증 상태 보관), 로드밸런서도 같은 클라이언트를 같은 서버로 유지해야(Sticky Session) 프레임 순서가 깨지지 않는다. 그래서 "클라이언트가 서버로 보내는 데이터가 얼마나 되는가"가 선택 기준이 된다 — 클라이언트 발화 비율이 낮으면(알림 구독처럼 거의 0%) SSE로 충분하고, 협업 편집처럼 양쪽이 계속 주고받으면 WebSocket이 필요하다.

### 비유와 흔한 오해
- 비유: WebSocket은 서로 자유롭게 말할 수 있는 전화 통화, SSE는 라디오처럼 방송국(서버)만 계속 말하고 청취자(클라이언트)는 듣기만 하는 채널이다.
- 오해: "SSE는 오래된 기술이라 WebSocket보다 열등하다"가 아니다. 서버 → 클라이언트 단방향 푸시만 필요한 상황(알림, 시세, 로그 tail)에서는 자동 재연결·Last-Event-ID·HTTP 인프라 재사용이라는 장점 때문에 오히려 SSE가 더 단순하고 안정적인 선택이다.

## 연결 개념
- HTTP/2 스트리밍 - 다중화와 헤더 압축 기반 실시간 전송을 보완하는 대안 계층
- 레이트 리미팅(Rate Limiting) - 연결 수와 메시지 속도를 통제하는 안전장치
- 로드 밸런싱(Sticky Session) - 장기 연결 세션을 분산하는 운영 기법

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

- 개요: 웹 실시간 전송 기술
- 배경: Polling은 요청 빈도만큼 서버 부하가 증가하므로 알림·시세·관측 대시보드에 한계가 있다.
- 필요성: p95 전달 지연, 동시 연결 수, 인증 갱신 기준을 함께 설계해야 한다.

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

| 구분 | 기존/대안 | WebSocket·SSE | 선택 기준 |
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
