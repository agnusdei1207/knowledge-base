---
title: "HTTPS·TLS (HTTP Secure/Transport Layer Security)"
date: "2026-06-30"
weight: 69
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> HTTPS는 HTTP(HyperText Transfer Protocol)에 TLS(Transport Layer Security) 보안 계층을 결합하여 기밀성·무결성·인증을 제공하는 암호화 웹 통신 방식이다.

## Ⅱ. 구성요소 / 원리
- TLS 핸드셰이크: 키 교환·암호 스위트 협상·인증서 검증 수행
- 공개키 암호: 핸드셰이크 시 세션키 안전 교환(RSA/ECDHE)
- 대칭키 암호: 협상된 세션키로 실제 데이터 고속 암호화(AES)
- 인증서·PKI(Public Key Infrastructure): CA(인증기관) 서명으로 서버 신원 보증
- 무결성: MAC/AEAD로 변조 탐지

## Ⅲ. 흐름도 / 구조
```text
 Client                       Server
   |--ClientHello------------->|
   |<--ServerHello+Cert--------|  (인증서/공개키)
   |--키교환(ECDHE)----------->|
   |<==대칭키 암호화 채널 수립==>|
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 웹 통신의 기밀성·무결성·서버 인증 보장 |
| 장점 | 공개키로 안전 교환 + 대칭키로 고속 암호화 결합 |
| 한계 | 핸드셰이크 지연, 인증서 관리·CA 신뢰 의존 |

## Ⅴ. 기술사적 적용
- TLS 1.2(2-RTT) vs 1.3(1-RTT, 0-RTT 재개): 지연 단축과 취약 암호 제거
- QUIC/HTTP/3는 TLS 1.3을 전송 계층에 내장
- 전 구간 암호화(HTTPS Everywhere), HSTS로 다운그레이드 공격 방어
