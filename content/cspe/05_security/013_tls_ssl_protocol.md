---
title: "TLS·SSL 프로토콜 (TLS SSL Protocol)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 13
---

# 📖 【암기용】 개념 완전 이해

> 목적: TLS·SSL을 처음 봐도 웹 주소의 자물쇠가 무엇을 보장하는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: TLS는 TCP 위에서 서버 인증, 키 교환, 암호화, 무결성 검증을 제공하는 보안 프로토콜
- **왜 필요한가**: HTTP·SMTP·IMAP 같은 평문 프로토콜은 도청·변조·세션 탈취에 노출되므로 전송 계층 보안 채널이 필요함
- **핵심 직관**: TLS는 통신 전에 신분증 확인과 일회용 비밀키 합의를 끝내고, 이후 모든 메시지에 봉인과 위변조 검사를 붙이는 절차임

## 깊이 이해
- **배경·문제의식**: SSL 2.0/3.0은 POODLE 등 취약점으로 폐기되었고, TLS 1.2와 TLS 1.3이 실무 기준임. TLS는 인증서 기반 신뢰와 세션키 기반 대칭암호를 결합함
- **작동 원리**: 클라이언트와 서버가 지원 버전·암호군을 협상하고, 서버 인증서를 검증한 뒤 ECDHE 등으로 세션키를 생성함. 이후 Record 계층에서 AES-GCM 또는 ChaCha20-Poly1305로 암호화·인증을 수행함
- **비유**: 처음에는 상대 신분증을 확인하고 비밀 암호표를 함께 만든 뒤, 대화 내용은 그 암호표로 봉인해 주고받는 구조임
- **구체 예시**: TLS 1.2는 ECDHE_RSA_WITH_AES_128_GCM_SHA256 같은 암호군을 사용하고, TLS 1.3은 TLS_AES_128_GCM_SHA256처럼 키교환과 인증을 분리함
- **흔한 오해·주의점**: HTTPS는 콘텐츠 기밀성과 서버 인증을 제공하지만, 서버가 악성 코드를 제공하는지까지 판단하지 않음. WAF·CSP·악성코드 탐지와 역할이 다름

## 연결 개념
- X.509 인증서 - TLS 서버 인증의 핵심 입력
- CA 인증 기관 - 인증서 신뢰사슬을 구성하는 신뢰 앵커
- TLS 1.3 핸드셰이크 - TLS 1.2의 왕복 지연과 취약 암호군을 줄인 버전

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: TLS 답안은 "암호화 프로토콜" 한 줄로 끝내지 않고 인증, 키교환, Record 보호, 버전별 차이, 운영 설정을 분리해야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TLS는 인증서 기반 인증과 (EC)DHE 키교환, AEAD Record 보호로 전송 구간 기밀성·무결성·인증을 제공하는 프로토콜임.
> 2. **가치**: HTTP, API, DB, 메일, mTLS 서비스에서 도청·변조·중간자 공격을 프로토콜 계층에서 통제함.
> 3. **판단 포인트**: TLS 1.2 이상, TLS 1.3 우선, 취약 SSL/TLS 제거, 인증서 검증, HSTS, Perfect Forward Secrecy 적용 여부가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 전송 보안 구조 이해 | Handshake, Record, Alert, ChangeCipherSpec, 인증서 검증 | TLS를 단순 대칭암호로 설명 금지 |
| 보안 속성 구분 | 기밀성, 무결성, 서버 인증, 선택적 클라이언트 인증 | 부인방지를 TLS 채널 전체 속성으로 단정 금지 |
| 운영 설정 판단 | TLS 1.3, AEAD, PFS, HSTS, 취약 버전 차단 | SSL 3.0·TLS 1.0 허용 답안 금지 |

> 요약: TLS는 인증서 검증과 키교환으로 세션키를 만들고 Record 계층에서 AEAD로 메시지를 보호하는 계층형 보안 프로토콜임.

---

## Ⅰ. 개요 및 필요성

- 개요: 전송 구간 보안 프로토콜
- 배경: 인터넷 경유망에서는 패킷 도청·변조·위장 서버 접속이 가능해 애플리케이션 앞단에서 인증된 암호 채널이 필요함.
- 필요성: TLS 1.2/1.3은 HTTPS, API Gateway, VPN, DB 접속, 서비스 간 mTLS에서 기밀성·무결성·인증을 제공함.

---

## Ⅱ. 구조 및 구성요소

```text
Application Data -> TLS Record -> TCP
Handshake -> 인증서 검증/키교환 -> 세션키 생성
Record -> AEAD 암호화/무결성 -> Alert -> 오류/종료 통지
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Handshake Protocol | 버전·암호군 협상, 인증, 키교환 | TLS 1.2는 2-RTT, TLS 1.3은 1-RTT 기본 |
| Record Protocol | 애플리케이션 데이터 보호 | AES-GCM, ChaCha20-Poly1305 등 AEAD |
| Certificate | 서버·클라이언트 신원 검증 | X.509, SAN, EKU, 체인 검증 |
| Key Schedule | 세션키 생성·분리 | ECDHE 기반 PFS, HKDF |
| Alert Protocol | 오류·종료 통지 | close_notify, handshake_failure |

> 요약: TLS는 Handshake에서 신뢰와 키를 만들고 Record에서 데이터를 보호하는 이중 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
ClientHello -> ServerHello -> Certificate/Verify -> Finished
-> 세션키 확정 -> HTTP 요청 Record 암호화 -> 응답 Record 복호화 -> close_notify
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | ClientHello로 버전·암호군·확장 제안 | TLS 1.2 이상, SNI, ALPN |
| 2 | ServerHello로 선택값 확정 | TLS 1.3 우선, 약한 암호군 제외 |
| 3 | 인증서 체인 검증 | Root 신뢰, SAN 일치, CRL/OCSP |
| 4 | 키교환과 Finished 검증 | ECDHE, transcript hash, MAC 일치 |
| 5 | Record 보호 통신 | AEAD tag 검증, 재전송·변조 차단 |

> 요약: TLS 연결은 협상, 인증서 검증, 키교환, Finished 검증, Record 보호 순서로 동작함.

---

## Ⅳ. 특징

| 구분 | SSL/TLS 구버전 | TLS 1.2/1.3 | 수치·표준 판단 |
|:---|:---|:---|:---|
| 버전 | SSL 3.0, TLS 1.0/1.1 | TLS 1.2, TLS 1.3 | RFC 5246, RFC 8446 |
| 암호 방식 | CBC, RC4, RSA key transport | AEAD, ECDHE, HKDF | AES-128-GCM, AES-256-GCM, ChaCha20-Poly1305 |
| 인증 | 서버 인증 중심 | 서버 인증 + mTLS 선택 | X.509 SAN, EKU ServerAuth/ClientAuth |
| 운영 통제 | 약한 cipher 허용 가능 | HSTS, OCSP Stapling, ALPN | SSL Labs A 등급 기준 점검 |

> 요약: TLS 운영 판단은 버전 차단, AEAD 암호군, PFS, 인증서 검증, HSTS 적용 여부로 수행함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | TLS 적용 | 선택 기준 |
|:---|:---|:---|:---|
| 평문 통신 | HTTP, Telnet, FTP | HTTPS, SMTPS, LDAPS | 개인정보·인증정보 포함 시 TLS 필수 |
| 인증 방식 | 서버 인증만 | mTLS 양방향 인증 | 서비스 간 호출, 관리자 API는 mTLS |
| 비용/성능 | 암호화 없음 | CPU·핸드셰이크 비용 발생 | TLS 1.3, session resumption, HW AES-NI |

> 요약: TLS는 민감정보 통신의 기본 통제이며, 내부 서비스 인증이 필요하면 mTLS를 선택함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 다운그레이드 | 구버전 허용, 협상 취약점 | TLS 1.2 이상, TLS 1.3 우선, HSTS | SSL/TLS 스캔 취약 0건 |
| 인증서 오류 | 만료, SAN 불일치, 폐지 미확인 | ACME 자동 갱신, OCSP Stapling | 만료 14일 이하 0개 |
| 중간자 공격 | CA 오발급, 클라이언트 검증 생략 | CT 모니터링, hostname 검증 강제 | hostname 검증 우회 0건 |

> 요약: TLS 리스크는 구버전 허용, 인증서 운영, 검증 생략에서 발생하므로 자동화와 스캔으로 관리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 프로토콜 | TLS 1.2 이상 100%, TLS 1.3 우선 | nmap ssl-enum-ciphers, sslyze |
| 암호군 | AEAD+PFS만 허용 | 서버 설정, SSL Labs, 보안 게이트 |
| 성능/운영 | handshake p95 100ms 이하, 실패율 0.1% 이하 | APM, LB 로그, synthetic test |

> 요약: TLS 도입 효과는 프로토콜 버전, 암호군, 핸드셰이크 지연·실패율로 검증함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 인터넷 공개 서비스: TLS 1.3 우선, TLS 1.2 호환, SSL 3.0/TLS 1.0/1.1 차단, HSTS max-age 31536000 적용
2. API·마이크로서비스: mTLS, SPIFFE/SPIRE 또는 Private CA, 인증서 수명 24시간~90일, RBAC 발급권한 분리
3. 운영 점검: ACME 자동 갱신, OCSP Stapling, cipher 스캔, handshake p95·실패율·만료일 대시보드 구성

**결론 (2줄):**
- 기술사 판단: 외부 서비스는 TLS 1.3+HSTS+공인 CA, 내부 서비스 간 인증은 mTLS+Private CA 조합이 적합함
- 향후 방향: PQC 하이브리드 키교환, 인증서 자동화, 서비스 메시 기반 mTLS로 암호 민첩성 확보 필요

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TLS를 설명하시오", "SSL과 TLS를 기술하시오" | Handshake와 Record 동작 원리 | SSL/TLS 버전·암호군 비교 |
| 요구사항 명시형 | "HTTPS 보안 설정 방안을 제시하시오", "mTLS를 설계하시오" | 인증서 검증, 키교환, 운영 흐름 | HSTS, OCSP, mTLS, 지표 기반 선택 |

> 요약: 설명형은 프로토콜 계층을, 설계·방안형은 버전 차단과 인증서 운영, mTLS 적용 기준을 중심으로 작성함.
