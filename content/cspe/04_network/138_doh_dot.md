---
title: "DNS over HTTPS·DNS over TLS (DoH DoT)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 138
---

# 📖 【암기용】 개념 완전 이해

> 목적: DoH와 DoT를 DNS 질의 프라이버시, 포트, 운영 통제 차이로 이해하게 만든다.

## 한눈에
- **개요**: DNS 질의를 TLS로 암호화하는 두 방식
- **왜 필요한가**: 전통적 DNS는 UDP/TCP 53에서 질의 도메인이 평문으로 노출된다. DoH·DoT는 클라이언트와 resolver 사이 DNS 내용을 암호화한다.
- **핵심 직관**: 엽서처럼 보이던 DNS 질의를 봉투에 넣어 보내되, DoH는 HTTPS 우편함 443을 쓰고 DoT는 DNS 전용 TLS 우편함 853을 쓴다.

## 깊이 이해
- **배경·문제의식**: 네트워크 중간자는 평문 DNS 질의를 관찰·변조할 수 있다. DNSSEC은 응답 진위 검증에 초점이 있고, 질의 내용 프라이버시를 직접 제공하지 않는다.
- **작동 원리**: DoH는 RFC 8484에 따라 DNS query-response를 HTTPS exchange로 매핑한다. DoT는 RFC 7858에 따라 TLS 연결 위에서 DNS 메시지를 전송하고 주로 TCP 853을 사용한다.
- **비유**: DoH는 일반 웹 트래픽 속에 DNS 편지를 넣는 방식이고, DoT는 DNS 전용 보안 창구를 만드는 방식이다.
- **구체 예시**: 브라우저 DoH는 443 포트로 resolver에 질의해 네트워크 장비가 DNS와 일반 HTTPS를 구분하기 어렵다. 기업망 DoT는 853 정책으로 resolver 통제를 적용하기 쉽다.
- **흔한 오해·주의점**: DoH·DoT는 resolver를 신뢰해야 한다. 암호화 구간은 클라이언트-resolver 사이이며, resolver 이후 authoritative 질의 전체가 자동 보호되는 것은 아니다.

## 연결 개념
- DNSSEC — DNS 응답 데이터 검증 체계
- Encrypted ClientHello — TLS SNI 노출 완화 기술
- Enterprise DNS Policy — 기업 resolver 강제와 로그·감사 정책

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식이다.
> 핵심: DoH·DoT 답안은 프라이버시, 포트, 탐지·통제, DNSSEC과의 역할 차이를 분리해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DoH와 DoT는 클라이언트와 recursive resolver 사이 DNS 질의를 TLS로 보호하는 DNS privacy 기술이다.
> 2. **가치**: DoH는 HTTPS 443에 통합되고 DoT는 TCP 853 전용 포트로 운영 정책 적용 지점이 명확하다.
> 3. **판단 포인트**: 개인 프라이버시, 기업 DNS 통제, resolver 신뢰, 로그 감사, fallback 정책을 함께 판단한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| DNS privacy 이해 확인 | RFC 8484 DoH, RFC 7858 DoT, TLS 암호화 | DNSSEC과 동일 기능으로 오해 |
| DoH·DoT 비교 확인 | 443 vs 853, HTTPS 통합 vs 전용 포트 | 포트와 운영 통제 차이 누락 |
| 보안 운영 판단 확인 | resolver trust, policy bypass, logging | 암호화만으로 모든 위협 제거 단정 |

> 요약: 출제자는 DNS 질의 프라이버시와 기업망 통제의 균형을 DoH·DoT 차이로 설명하길 기대한다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **DNS over HTTPS·DNS over TLS** | DNS over HTTPS·DNS over TLS (DoH DoT)의 핵심 개념 | "이 주제의 본질" |
| **프로토콜** | 통신 규칙의 표준화된 집합 | "공용 언어" |
| **패킷** | 네트워크를 통해 전송되는 데이터의 단위 | "택배 상자" |

---

## Ⅰ. 개요 및 필요성

- 개요: TLS 기반 DNS 프라이버시
- 배경: 전통적 DNS 53번 질의는 도메인 정보가 평문으로 노출되고 중간자 변조 대상이 됨
- 필요성: DoH 443, DoT 853으로 클라이언트-resolver 구간 질의 내용을 암호화함
- 판단 기준: resolver 신뢰, 정책 우회율, DNS latency, fallback to port 53 비율로 검증

---

## Ⅱ. 구조 및 구성요소

```text
Client -> DoH HTTPS 443 / DoT TLS 853 -> Recursive Resolver
       -> Cache / DNSSEC validation -> Authoritative DNS -> Response
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| DoH Client | DNS를 HTTPS request로 전송 | RFC 8484, 443 포트 |
| DoT Client | DNS를 TLS connection으로 전송 | RFC 7858, 853 포트 |
| Recursive Resolver | 캐시·재귀 질의·정책 적용 | resolver 신뢰가 전제 |
| DNSSEC Validator | 응답 데이터 검증 | 프라이버시가 아니라 무결성 검증 |
| Enterprise Policy | 허용 resolver·로그·차단 규칙 | 우회 탐지 필요 |

> 요약: DoH·DoT는 클라이언트와 resolver 사이 암호화 계층이며 DNSSEC·정책 체계와 역할이 다르다.

---

## Ⅲ. 동작원리 및 흐름도

```text
애플리케이션 질의 -> DoH/DoT resolver 선택 -> TLS 연결
-> DNS message 전송 -> resolver cache/DNSSEC 확인 -> 응답 반환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 클라이언트가 resolver 정책 결정 | managed resolver 적용 여부 |
| 2 | DoH는 HTTPS 443, DoT는 TLS 853 연결 | TLS version, cert validation |
| 3 | DNS query를 암호화 채널로 전송 | plaintext DNS fallback 여부 |
| 4 | resolver가 캐시·재귀 질의·DNSSEC 검증 수행 | cache hit, validation result |
| 5 | 응답과 로그·정책 결과 반환 | NXDOMAIN, block reason |

> 요약: DoH·DoT는 resolver 선택, TLS 연결, DNS 메시지 전송, 캐시·검증, 응답 반환 순서로 동작한다.

---

## Ⅳ. 특징

| 구분 | DoH | DoT | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 포트 | HTTPS 443 | TCP 853 | 방화벽 정책 적용성 |
| 트래픽 식별 | 일반 HTTPS와 혼재 | DNS 전용 포트로 식별 | 우회 탐지 난이도 |
| 적용 영역 | 브라우저·앱 단위 채택 | OS·네트워크 resolver 정책 | 기업망 통제 방식 |
| 운영 리스크 | 보안 장비 DNS 가시성 감소 | 853 차단 시 fallback 발생 | fallback to 53 비율 |

> 요약: DoH는 프라이버시와 우회성이 크고 DoT는 기업망 식별·통제 지점이 명확하다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | DoH·DoT | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 평문 DNS 53 | TLS 보호 DNS | 질의 프라이버시 요구 |
| 비용/성능 | 낮은 handshake 비용 | TLS 연결·재사용 필요 | DNS latency, connection reuse |
| 운영/위험 | DNS 보안 장비 가시성 | 정책 우회 가능 | enterprise resolver 강제 가능성 |

> 요약: DoH·DoT는 프라이버시 요구와 보안 운영 가시성 손실을 동시에 평가해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 정책 우회 | 브라우저가 외부 DoH 사용 | managed policy, allowlist resolver | unauthorized DoH count |
| Resolver 집중 | 소수 public resolver 의존 | 내부 resolver, split-horizon 정책 | resolver availability |
| 평문 fallback | DoH/DoT 실패 시 53 사용 | strict mode, fallback alert | fallback query ratio |

> 요약: 운영 리스크는 정책 우회, resolver 집중, 평문 fallback으로 나눠 지표화한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 프라이버시 | plaintext DNS fallback 0건 | endpoint telemetry, firewall log |
| 운영 통제 | unauthorized resolver 0건 | DNS proxy log, CASB |
| 지연 | p95 DNS resolution 50ms 이하 | resolver metric, RUM |

> 요약: DoH·DoT 성공 여부는 암호화 적용률, resolver 정책 준수, DNS 지연으로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 기업 단말은 관리 정책으로 내부 DoH/DoT resolver를 고정하고 외부 public resolver 접근을 탐지한다.
2. DoT 853은 네트워크 경계에서 허용 resolver만 통과시키고, DoH 443은 SNI·IP allowlist와 endpoint 정책으로 관리한다.
3. DNSSEC validation, RPZ, malware domain feed를 resolver에 적용하고 plaintext fallback을 경보화한다.

**결론 (2줄):**
- 기술사 판단: 개인 프라이버시 우선 환경은 DoH, 기업망 정책 통제는 DoT 또는 관리형 DoH를 선택한다.
- 향후 방향: DNS privacy는 ECH, DNSSEC, enterprise resolver governance와 함께 통합 운영된다.

### 🔀 문제 유형별 목차 전환

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "DoH와 DoT를 설명하시오" | TLS 기반 DNS 질의 흐름 | 443과 853 운영 차이 |
| 요구사항 명시형 | "기업 DNS 보안 방안을 제시하시오" | resolver 고정과 fallback 통제 | 정책 우회, 로그, DNSSEC 연계 |

> 요약: 설명형은 표준·포트 차이를, 보안형은 resolver 신뢰와 기업 정책 통제를 중심으로 전환한다.
