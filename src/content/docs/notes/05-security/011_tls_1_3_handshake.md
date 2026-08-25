---
sidebar:
  order: 11
  label: "011. TLS 1.3 핸드셰이크"
  badge:
    text: "미출 · 70%"
    variant: note
title: "초저지연 고보안 전송 계층 보안 프로토콜 : TLS 1.3 핸드셰이크"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 11
extra:
  question_no: "11"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "1-RTT 기본 핸드셰이크, 0-RTT 조기 데이터(Early Data) 및 Replay 방어, AEAD 강제 및 Transcript Hash"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **TLS 1.3 (RFC 8446)**: 연결 지연을 1-RTT/0-RTT로 대폭 단축하고 취약한 구형 암호를 전면 퇴출한 전송 계층 보안 프로토콜.
- **AEAD-Only Policy**: CBC 패딩 공격과 정적 RSA 키 교환을 배제하고 오직 안전한 AEAD 암호 스위트만 강제하는 정책.

</details>

- 정의/개념: 첫 왕복 메시지에 ECDHE 공개키를 동봉(Key Share)하여 **1-RTT로 세션키를 수립하고 트랜스크립트 해시와 AEAD로 전송 계층을 보호하는 표준 프로토콜**
- 배경/필요성: TLS 1.2의 2-RTT 연결 지연 및 취약한 CBC/정적 RSA 암호로 인한 **패딩 오라클 공격 노출, 핸드셰이크 평문 도청 및 순방향 비밀성(PFS) 상실**

#### 한줄 요약
- 1-RTT/0-RTT 연결과 AEAD 전용 암호화를 통해 초저지연과 무결점 전송 계층 보안을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Key Share (키 공유 확장)**: ClientHello에 클라이언트의 ECDHE 임시 공개키($g^a$)를 선제 동봉하여 1-RTT 만에 공유 비밀을 도출하는 기법.
- **Transcript Hash Binding**: 핸드셰이크 중 오간 모든 제어 메시지의 해시값을 서버 전자서명에 결합하여 다운그레이드 공격을 원천 차단하는 기법.

</details>

- **압도적인 1-RTT 연결 및 0-RTT 세션 재개**: 키 교환과 인사를 단일 패킷으로 통합하여 **초기 연결 지연시간을 50% 단축**
- **취약한 구형 암호의 전면 퇴출(AEAD 강제)**: 정적 RSA, CBC 모드, RC4, SHA-1을 완전히 삭제하고 **AES-GCM/ChaCha20만 허용**
- **핸드셰이크 메타데이터 전면 암호화**: ServerHello 이후 **인증서, 확장 필드, 신원 정보를 모두 암호화하여 스누핑 차단**

#### 한줄 요약
- 1-RTT/0-RTT 지연 단축, AEAD 전용 강제, 핸드셰이크 메타데이터 암호화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Handshake Secret vs Application Master Secret**: 인증서와 제어 메시지를 암호화하는 임시 키와 핸드셰이크 완료 후 실제 데이터를 암호화하는 세션키.

</details>

```text
[TLS 1.3 1-RTT 핸드셰이크 메시지 흐름 및 키 도출]
|-- Client (1. ClientHello + Key_Share ECDHE 공개키 g^a 전송)
`-- Server (2. ServerHello + Key_Share g^b 응답 -> 양단 공유 비밀 g^ab 도출)
    |-- {EncryptedExtensions} (Handshake Secret으로 암호화)
    |-- {Certificate} (서버 X.509 인증서 체인 암호화 전송)
    |-- {CertificateVerify} (Transcript Hash H_2에 대한 서버 전자서명)
    `-- {Finished} (HKDF로 도출된 무결성 HMAC 검증값)
`-- Client Verify & Application Data (서명 검증 후 Application Master Key로 즉시 데이터 통신)
```

선의 의미: 클라이언트의 첫 패킷에 ECDHE 공개키가 실려 전송되고 서버가 공개키와 암호화된 인증서를 즉시 회신하여 1-RTT 만에 데이터 통신이 개시되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **ClientHello / Key_Share**| 지원 암호 스위트 제시 및 **클라이언트 ECDHE 공개키($g^a$) 선제 전송** | 1-RTT 기반 |
| **ServerHello / Key_Share**| 암호 스위트 확정 및 **서버 ECDHE 공개키($g^b$) 전송으로 공유 비밀 완성** | Shared Secret |
| **Certificate / CertVerify**| 서버 X.509 인증서를 전송하고 **트랜스크립트 해시에 서명하여 신원 증명** | Server Auth |
| **Finished 메시지** | HKDF로 도출된 검증 키를 사용하여 **핸드셰이크의 HMAC 무결성 최종 확정** | Integrity Check |
| **HKDF 키 스케줄러** | 공유 비밀로부터 **Handshake Key와 Application Master Key를 단계별 도출** | RFC 5869 HKDF |

#### 한줄 요약
- ClientHello/Key_Share, ServerHello, CertificateVerify, Finished MAC, HKDF 키 스케줄러가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **HKDF 3단계 키 스케줄**: Early Secret(0-RTT 데이터용) → Handshake Secret(제어 메시지 암호화용) → Master Secret(애플리케이션 데이터 암호화용).

</details>

```text
TLS 1.3 1-RTT 키 교환, 핸드셰이크 암호화 및 데이터 전송 파이프라인
        │
   1. [ClientHello + Key_Share 송출] 클라이언트가 AES-GCM 스위트 및 ECDHE 공개키($g^a$) 동봉 전송
        │
   2. [ServerHello + Key_Share 회신] 서버가 암호를 확정하고 ECDHE 공개키($g^b$) 회신 ➔ 공유 비밀($g^{ab}$) 완성
        │
   3. [핸드셰이크 암호화 전송] 서버가 Handshake Key로 암호화된 Certificate, CertVerify, Finished 전송
        │
   4. [서버 신원 및 MAC 검증] 클라이언트가 서버 인증서 체인과 서명을 검증하고 Finished MAC 대조
        │
   ▼
5. [Application Data 전송] 핸드셰이크 완료 즉시 Application Key로 암호화된 HTTP 데이터 전송 (1-RTT 완결)
```

#### 한줄 요약
- ClientHello/KeyShare 전송 → ServerHello 응답 및 공유 비밀 도출 → 인증서 암호 전송 → 서명 검증 → Application Key 통신 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **TLS 1.2** vs **TLS 1.3**.

</details>

| 비교 항목 | TLS 1.2 핸드셰이크 (Legacy) | TLS 1.3 핸드셰이크 (Modern Standard) |
|:---|:---|:---|
| **기본 연결 지연시간** | **2-RTT (인사 협상 1-RTT + 키 교환 1-RTT)** | **1-RTT (ClientHello에 키 교환 동봉)** |
| **세션 재개 지연시간** | 1-RTT (Session Ticket 기반) | **0-RTT (Early Data 지원, 즉시 전송)** |
| **순방향 비밀성 (PFS)**| 선택적 (정적 RSA 키 교환 시 PFS 미지원) | **필수 보장 (모든 키 교환에 ECDHE/DHE 강제)**|
| **허용 암호 스위트** | 30개 이상 (CBC 모드, RC4, 정적 RSA 허용) | **5개로 단순화 (오직 AEAD 알고리즘만 허용)** |
| **핸드셰이크 패킷 보호**| 인증서 및 서명 평문 노출 (SNI 도청 가능) | **ServerHello 이후 모든 핸드셰이크 암호화** |
| **알고리즘 다운그레이드**| 중간자의 파라미터 변조 공격 위험 존재 | **트랜스크립트 해시 서명으로 완전 차단** |

#### 한줄 요약
- TLS 1.2는 2-RTT에 취약 암호가 혼재되었으나, TLS 1.3은 1-RTT/0-RTT에 AEAD 전용 및 핸드셰이크 암호화를 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **0-RTT Replay Attack**: 0-RTT 조기 데이터는 PFS가 없어 공격자가 네트워크에서 캡처한 패킷을 재전송할 경우 중복 결제나 상태 변경이 발생하는 취약점.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 0-RTT 조기 데이터 재전송으로 인한 **금융 결제 중복 및 트랜잭션 오류** | **0-RTT는 `멱등성(Idempotent)이 보장된 GET 요청에만 한정 허용`** 및 Single-Use Ticket 강제 | 상태 변경 API 재전송 공격 원천 차단 |
| Key Share 그룹 불일치 시 발생하는 **HelloRetryRequest 지연(2-RTT로 증가)** | 서버와 클라이언트의 최우선 타원곡선 그룹을 **`X25519(Curve25519)로 전사 표준화`** | 그룹 불일치 재시도 0% 제거 및 1-RTT 연결률 99.9% 달성 |
| 레거시 L4/L7 방화벽이 TLS 1.3 핸드셰이크를 비정상 트래픽으로 오인하여 **패킷 드롭** | **`미들박스 호환 모드(Middlebox Compatibility Mode)`** 유지 | 구형 네트워크 장비 통과율 100% 확보 및 무중단 전환 |
| 도청 트래픽을 사후 양자컴퓨터로 해독하는 SNDL 위협 | **`X25519 + ML-KEM(Kyber) 결합 PQC 하이브리드 키 교환`** 조기 도입 | 미래 양자 컴퓨팅 해독 위협 원천 차단 |

#### 한줄 요약
- 멱등 GET 요청에만 0-RTT를 허용하고, X25519를 표준화하며, 호환 모드로 미들박스 드롭을 방지한다.

## Ⅶ. 결론

- 글로벌 인터넷 웹 트래픽과 클라우드 네이티브 통신의 기본 보안 표준인 **TLS 1.3 핸드셰이크 아키텍처는 고성능과 고신뢰 보안을 동시에 달성한 핵심 프로토콜**이며, 실무 구축 시 **X25519 기반 1-RTT 연결 최적화, 0-RTT Replay 방어 가드레일 적용, PQC(X25519+ML-KEM) 하이브리드 키 교환의 선제적 도입**을 결합하여 무결점 전송 계층 보안 환경 완성

#### 한줄 요약
- TLS 1.3은 1-RTT 핸드셰이크와 AEAD 전용 암호화 및 0-RTT 재전송 방어를 결합하여 고속 고보안 통신을 실현하는 표준 프로토콜이다.