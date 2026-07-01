---
title: "TLS 1.3 핸드셰이크 (TLS 1.3 Handshake)"
date: "2026-07-01"
tags:
  - "cspe-network"
weight: 37
---

# 📖 【암기용】 개념 완전 이해

> 목적: TLS 1.3 핸드셰이크를 키 교환, 인증, 암호화 시작 시점 중심으로 이해하게 만든다. 시험 답안 양식이 아니라, TLS 1.2와의 차이를 잡기 위한 설명이다.

## 한눈에
- **개요**: TLS 1.3은 1-RTT 기본 핸드셰이크와 제한적 0-RTT 재개를 제공하는 보안 통신 프로토콜
- **왜 필요한가**: TLS 1.2의 다중 RTT, 구식 cipher suite, RSA key exchange를 줄이고 forward secrecy를 기본화함.
- **핵심 직관**: 처음 만날 때는 신분 확인과 임시 열쇠 교환을 한 번에 끝내고, 다시 만날 때는 티켓으로 일부 절차를 줄이는 방식임.

## 깊이 이해
- **배경·문제의식**: HTTPS는 암호화와 인증을 제공하지만, TLS 1.2는 handshake RTT와 취약 알고리즘 선택지가 많았음. TLS 1.3은 협상 범위를 줄이고 ECDHE 기반 forward secrecy를 기본으로 둠.
- **작동 원리**: ClientHello에 supported groups, key share, cipher suites를 포함하고 서버는 ServerHello, 인증서, CertificateVerify, Finished를 전송함. 이후 application data는 handshake에서 파생된 키로 암호화됨.
- **비유**: 손님이 사용 가능한 자물쇠와 임시 열쇠 조각을 먼저 보내고, 서버가 맞는 조각과 신분증을 돌려보내 둘만의 열쇠를 만드는 절차임.
- **구체 예시**: TLS 1.3 cipher suite는 `TLS_AES_128_GCM_SHA256`, `TLS_AES_256_GCM_SHA384`, `TLS_CHACHA20_POLY1305_SHA256`처럼 AEAD 중심임.
- **흔한 오해·주의점**: 0-RTT는 지연을 줄이지만 replay 위험이 있어 결제·상태 변경 요청에는 제한해야 함.

## 연결 개념
- QUIC·HTTP/3: QUIC handshake에 TLS 1.3 통합
- mTLS: 서버 인증에 클라이언트 인증서를 추가
- PKI·인증서: 서버 신원 검증 기반

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: TLS 1.3은 1-RTT, ECDHE, AEAD, forward secrecy, 0-RTT replay 통제를 중심으로 답안을 구성함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TLS 1.3 핸드셰이크는 ClientHello와 ServerHello 단계에서 키 교환·인증·암호 알고리즘을 확정하는 보안 연결 절차이다.
> 2. **가치**: 기본 1-RTT, session resumption 0-RTT, AEAD cipher suite, forward secrecy를 통해 HTTPS 연결 지연과 취약 협상을 줄인다.
> 3. **판단 포인트**: 인증서 체인, cipher suite, ECDHE group, 0-RTT replay, TLS termination 위치를 함께 검토해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TLS 1.3 구조 이해 확인 | 1-RTT, ClientHello key share, ServerHello, Finished | TLS 1.2 절차를 그대로 설명 |
| 보안 속성 확인 | ECDHE, forward secrecy, AEAD, certificate verify | RSA key exchange 허용으로 오기 |
| 운영 적용 판단 확인 | 인증서, ALPN, termination, 0-RTT replay | 0-RTT를 모든 요청에 허용 |

> 요약: TLS 1.3 문제는 핸드셰이크 단축과 보안 알고리즘 정리, 0-RTT 통제 조건을 묻는 문제임.

---

## Ⅰ. 개요 및 필요성

TLS 1.3 핸드셰이크는 보안 채널을 수립하는 절차이다. TLS 1.2 대비 협상 단계를 줄이고 ECDHE와 AEAD cipher suite를 중심으로 정리했다. HTTPS, HTTP/3, API 통신에서 인증·암호화·무결성을 제공한다.

---

## Ⅱ. 구조 및 구성요소

```text
ClientHello(key_share) -> ServerHello -> EncryptedExtensions
-> Certificate -> CertificateVerify -> Finished -> Application Data
       / Session Ticket
       / 0-RTT Early Data
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| ClientHello | 지원 버전·cipher·key share 제시 | SNI, ALPN 포함 |
| ServerHello | cipher suite와 key share 선택 | TLS 1.3 확정 |
| Certificate | 서버 신원 증명 | X.509 chain 검증 |
| Finished | handshake transcript 무결성 확인 | 이후 application key 사용 |
| Session Ticket | 재개 연결 정보 | 0-RTT 조건 |

> 요약: TLS 1.3은 key share를 ClientHello에 실어 1-RTT 안에 키 교환과 서버 인증을 완료함.

---

## Ⅲ. 동작원리 및 흐름도

```text
ClientHello -> ServerHello -> Handshake Keys 생성
-> Server Certificate 검증 -> Finished 교환 -> App Data 암호화
-> 재접속 시 PSK/0-RTT 선택
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 클라이언트가 supported_versions, key_share 전송 | TLS 1.3 협상 |
| 2 | 서버가 cipher suite와 key share 선택 | AEAD suite |
| 3 | 서버 인증서와 서명 검증 | chain, SAN, OCSP |
| 4 | Finished 메시지로 transcript 확인 | handshake integrity |
| 5 | application data 암호화 및 session ticket 발급 | resumption rate |

> 요약: TLS 1.3은 키 교환과 인증을 handshake transcript로 묶고 Finished 이후 애플리케이션 데이터를 암호화함.

---

## Ⅳ. 특징

| 구분 | TLS 1.2 | TLS 1.3 | 수치·표준 포인트 |
|:---|:---|:---|:---|
| RTT | 2 RTT 가능 | 기본 1 RTT | 재개 0-RTT 가능 |
| 키 교환 | RSA, DHE, ECDHE | ECDHE/PSK 중심 | RSA key exchange 제거 |
| 암호 | CBC 등 legacy 포함 | AEAD 중심 | AES-GCM, ChaCha20-Poly1305 |
| 보안 속성 | 옵션 의존 | forward secrecy 기본 | RFC 8446 |

> 요약: TLS 1.3은 handshake RTT와 legacy 알고리즘을 줄이고 forward secrecy와 AEAD를 기본 구조로 둠.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | TLS 1.3 | 선택 기준 |
|:---|:---|:---|:---|
| 웹 서버 | TLS 1.2 병행 | TLS 1.3 우선 | 구형 클라이언트 비중 |
| API | 단방향 TLS | mTLS 또는 JWT 병행 | 내부 서비스 신원 확인 |
| 전송 | TCP+TLS | QUIC 내장 TLS 1.3 | HTTP/3 적용 여부 |

> 요약: TLS 1.3 적용은 클라이언트 호환성과 termination 위치, 내부 인증 요구에 따라 설계함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 0-RTT replay | early data 재전송 가능 | 멱등 요청만 허용, replay cache | early data reject |
| 인증서 오류 | 만료·SAN 불일치 | ACME 자동 갱신, CT 모니터링 | cert expiry days |
| 암호 정책 미준수 | legacy suite 허용 | TLS 1.3 suite 제한, scanner | SSL Labs grade |

> 요약: TLS 1.3 운영 리스크는 0-RTT, 인증서 수명, cipher policy이며 자동화와 스캔으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| handshake 지연 | p95 1 RTT 수준 | RUM, server timing |
| TLS 1.3 비율 | 지원 클라이언트 90% 이상 | access log, JA3/JA4 |
| 인증서 만료 | 30일 전 경보 | ACME, monitoring |

> 요약: TLS 1.3 효과는 협상 비율, handshake 지연, 인증서 상태로 측정함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수):**
1. 서버 설정: TLS 1.3 활성화, AEAD cipher suite 제한, OCSP stapling과 HSTS 적용
2. 0-RTT 통제: GET·HEAD 같은 멱등 요청만 early data 허용, POST·결제·상태 변경 API는 차단
3. 인증서 운영: ACME 자동 갱신, SAN 점검, 만료 30/14/7일 경보, CT log 모니터링 구성

**결론 (2줄):**
- 기술사 판단: 인터넷 서비스는 TLS 1.3 우선, 구형 단말 비중이 남은 경우 TLS 1.2 병행 기간을 설정함
- 향후 방향: QUIC, ECH, post-quantum TLS 전환 논의와 함께 핸드셰이크 보안 정책이 계속 진화함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TLS 1.3 핸드셰이크를 설명하시오" | ClientHello부터 Finished까지 절차 | TLS 1.2 대비 RTT·암호 차이 |
| 요구사항 명시형 | "TLS 1.3 적용 방안을 제시하시오" | 인증서·cipher·0-RTT 처리 | replay, 호환성, 모니터링 대응 |

> 요약: 설명형은 핸드셰이크 절차, 보안형은 cipher policy와 0-RTT 통제 중심으로 전환함.
