---
title: "HTTP/2·HTTP/3 비교 (HTTP/2 HTTP/3 Comparison)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 135
---

# 📖 【암기용】 개념 완전 이해

> 목적: HTTP/2와 HTTP/3의 차이를 TCP 기반 다중화와 QUIC 기반 다중화의 관점에서 이해하게 만든다.

## 한눈에
- **개요**: HTTP/2는 TCP 위의 프레임 다중화, HTTP/3는 QUIC 위의 프레임 다중화
- **왜 필요한가**: 웹은 많은 리소스를 동시에 내려받는다. HTTP/2는 연결 수를 줄였지만 TCP packet loss가 모든 stream에 영향을 주는 문제가 남았다.
- **핵심 직관**: HTTP/2는 한 도로의 여러 차선이 같은 도로 사고에 막히는 구조이고, HTTP/3는 QUIC stream별로 손실 영향을 분리한다.

## 깊이 이해
- **배경·문제의식**: HTTP/1.1은 connection당 요청 처리 제약 때문에 head-of-line blocking과 다중 연결 비용이 있었다. HTTP/2는 multiplexing·HPACK으로 개선했지만 TCP 계층 HOL은 남았다.
- **작동 원리**: HTTP/2는 TLS/TCP 연결 위에 binary frame과 stream을 올린다. HTTP/3는 UDP 기반 QUIC 연결 위에 HTTP semantics를 매핑하고 QPACK을 사용한다.
- **비유**: HTTP/2는 큰 컨테이너 트럭 하나에 여러 화물을 싣는 방식이고, HTTP/3는 화물별 추적·복구가 가능한 전용 운송 단위를 만든 방식이다.
- **구체 예시**: RFC 9114는 HTTP/3를 QUIC transport 위의 HTTP semantics 매핑으로 규정한다. QUIC RFC 9000은 stream, 0-RTT, connection migration을 제공한다.
- **흔한 오해·주의점**: HTTP/3가 모든 환경에서 HTTP/2를 대체한다고 단정하면 안 된다. UDP 차단, middlebox, observability, fallback 정책을 같이 검토해야 한다.

## 연결 개념
- QUIC — UDP 기반 multiplexed secure transport
- HPACK/QPACK — HTTP header 압축 방식
- TLS 1.3 — QUIC handshake와 보안 기반

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식이다.
> 핵심: HTTP/2·HTTP/3 비교는 전송 계층, HOL blocking, handshake, 운영 fallback을 축으로 써야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: HTTP/2는 TCP 위 binary framing, HTTP/3는 QUIC 위 HTTP semantics 매핑이다.
> 2. **가치**: HTTP/3는 QUIC stream으로 TCP 계층 HOL 영향을 줄이고 0-RTT·connection migration을 지원한다.
> 3. **판단 포인트**: UDP 허용률, CDN 지원, fallback 성공률, p95 TTFB, packet loss 환경을 함께 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| HTTP 진화 이해 확인 | HTTP/1.1 -> HTTP/2 -> HTTP/3 구조 변화 | HTTP/3를 단순 버전업으로 설명 |
| 프로토콜 비교 역량 확인 | TCP vs QUIC, HPACK vs QPACK, HOL blocking | QUIC을 UDP 그대로라고만 표현 |
| 운영 적용 판단 확인 | ALPN, Alt-Svc, fallback, UDP 차단 | 모든 환경에서 HTTP/3 우위로 단정 |

> 요약: 출제자는 HTTP/2와 HTTP/3를 전송 계층 차이와 운영 적용 조건으로 비교하길 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: TCP HTTP와 QUIC HTTP 비교
- 배경: HTTP/2 multiplexing은 연결 수를 줄였지만 TCP packet loss가 같은 연결의 stream에 영향을 줌
- 필요성: HTTP/3는 QUIC stream, TLS 1.3, connection migration으로 모바일·손실망의 지연을 통제함
- 판단 기준: UDP success rate, h3 adoption, p95 TTFB, fallback rate로 도입 효과 검증

---

## Ⅱ. 구조 및 구성요소

```text
HTTP/2: Browser -> TLS -> TCP -> HTTP/2 Frames -> Server
HTTP/3: Browser -> QUIC/TLS 1.3 -> UDP -> HTTP/3 Frames -> Server
```

| 구성요소 | HTTP/2 | HTTP/3 |
|:---|:---|:---|
| 전송 계층 | TCP | QUIC over UDP |
| 표준 | RFC 9113 계열 | RFC 9114, QUIC RFC 9000 |
| 헤더 압축 | HPACK | QPACK |
| 연결 광고 | ALPN h2 | ALPN h3, Alt-Svc |

> 요약: HTTP/2와 HTTP/3는 HTTP semantics는 유사하나 전송 계층과 헤더 압축, 연결 협상 방식이 다르다.

---

## Ⅲ. 동작원리 및 흐름도

```text
Client 요청 -> ALPN/Alt-Svc 확인 -> h3 가능 시 QUIC 연결
-> stream별 frame 교환 -> 손실 복구 -> h2 fallback 지표 수집
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 클라이언트가 ALPN 또는 Alt-Svc로 프로토콜 선택 | h2/h3 negotiation rate |
| 2 | HTTP/2는 TCP+TLS handshake 수행 | handshake RTT, TLS version |
| 3 | HTTP/3는 QUIC handshake와 TLS 1.3 키 교환 수행 | QUIC success rate |
| 4 | stream별 frame을 전송하고 흐름제어 적용 | packet loss, stream reset |
| 5 | 실패 시 HTTP/2로 fallback | fallback rate, error code |

> 요약: HTTP/3는 QUIC 협상 후 stream 단위 전송을 수행하고, 실패 시 HTTP/2 fallback을 운영 지표로 관리한다.

---

## Ⅳ. 특징

| 구분 | HTTP/2 | HTTP/3 | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 전송 기반 | TCP | UDP 기반 QUIC | UDP 443 허용률 |
| HOL blocking | TCP 손실이 연결 전체 영향 | QUIC stream 단위 영향 축소 | packet loss 1% 이상 환경 |
| 연결 재개 | TLS session resumption | QUIC 0-RTT 가능 | replay risk 검토 |
| 이동성 | IP 변경 시 연결 재수립 | connection migration 지원 | 모바일 handover |

> 요약: HTTP/3는 손실망과 이동 환경에서 장점이 있으나 UDP 차단과 운영 가시성 제약을 같이 검토해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | HTTP/3 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | HTTP/2 over TCP | HTTP/3 over QUIC | 모바일·무선 손실률, CDN 지원 |
| 비용/성능 | 기존 L7 장비 활용 | QUIC termination 필요 | p95 TTFB 개선과 장비 교체 비용 |
| 운영/위험 | TCP 관측 도구 활용 | QUIC 암호화로 관측 지점 변경 | 로그·trace·packet capture 전략 |

> 요약: HTTP/3는 프로토콜 교체보다 CDN, L7 보안장비, 관측 체계까지 포함한 전환으로 판단한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| UDP 차단 | 방화벽·통신사 정책 | h2 fallback, gradual rollout | h3 failure rate |
| 0-RTT 재전송 공격 | replay 가능한 요청 처리 | GET 한정, idempotency key | replay rejected count |
| 관측 공백 | QUIC payload 암호화 | edge log, qlog, synthetic test | unknown error ratio |

> 요약: HTTP/3 리스크는 UDP 접근성, 0-RTT replay, 관측성으로 분리해 rollout 지표로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 도입률 | h3 negotiated request 비율 50% 이상 | CDN log, browser RUM |
| 지연 | p95 TTFB·LCP 지역별 감소 | RUM, synthetic test |
| 복구 | fallback error rate 1% 이하 | edge log, QUIC error code |

> 요약: HTTP/3 도입은 협상률, p95 지연, fallback 오류율을 함께 확인해야 한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. CDN 또는 edge proxy에서 HTTP/3를 canary로 활성화하고 h3 negotiation rate와 fallback rate를 수집한다.
2. 0-RTT는 GET·HEAD 등 멱등 요청에 한정하고 결제·변경 API는 0-RTT를 차단한다.
3. qlog, edge access log, RUM 지표를 연결해 TCP 기반 지표와 QUIC 기반 지표를 분리한다.

**결론 (2줄):**
- 기술사 판단: 모바일·글로벌 사용자와 packet loss가 큰 서비스는 HTTP/3를 우선 검토하고, 기업 내부망·UDP 차단 환경은 HTTP/2 fallback을 유지한다.
- 향후 방향: 웹 전송은 HTTP semantics 유지와 QUIC 전송 최적화가 분리되는 구조로 발전한다.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "HTTP/2와 HTTP/3를 설명하시오" | ALPN, QUIC handshake, stream 흐름 | TCP vs QUIC 비교 |
| 요구사항 명시형 | "HTTP/3 도입 방안을 제시하시오" | rollout, fallback, 0-RTT 통제 | UDP 허용률, TTFB, qlog 지표 |

> 요약: 비교형은 전송 계층 차이를, 방안형은 도입·fallback·관측 지표를 중심으로 전환한다.
