---
sidebar:
  order: 11
  label: "011. TLS 1.3 핸드셰이크 (TLS 1.3 Handshake)"
  badge:
    text: "미출 · 70%"
    variant: note
title: "초저지연 고보안 전송 계층 보안 프로토콜 : TLS 1.3 핸드셰이크 (RFC 8446)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 11
extra:
  question_no: "011"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "1-RTT 기본 핸드셰이크, 0-RTT 조기 데이터(Early Data) 및 Replay 방어, AEAD 강제 및 Transcript Hash"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **TLS 1.3(RFC 8446)**: 전송 계층 통신의 기밀성, 무결성, 인증을 제공하는 IETF 표준 보안 프로토콜로, 레거시 TLS 1.2의 2-RTT 연결 지연을 1-RTT(신규 연결) 및 0-RTT(세션 재개)로 대폭 단축하고 취약한 구형 암호 스위트를 전면 퇴출한 차세대 전송 계층 보안 규격.
- **AEAD 전용 암호화(AEAD-Only Cipher Suites)**: AES-GCM, ChaCha20-Poly1305, AES-CCM 등 기밀성과 무결성 검증 태그 생성을 단일 연산으로 결합한 암호 모드만을 강제하여 취약한 CBC 모드와 정적 RSA 키 교환을 배제한 보안 정책.

</details>

- 정의/개념: 첫 번째 왕복 메시지(ClientHello / ServerHello)에 ECDHE 공개키 파라미터를 동시 교환(Key Share)하여 **1-RTT로 세션키를 즉각 수립**하고, 전체 협상 패킷을 해싱하는 **트랜스크립트 해시(Transcript Hash)** 기반 상호 서명을 수행하는 **초저지연 보안 통신 아키텍처**
- 배경/필요성: TLS 1.2의 2-RTT 지연으로 인한 모바일/웹 응답성 저하와 정적 RSA 키 교환(PFS 미지원) 및 CBC 패딩 오라클(POODLE, Lucky 13) 취약점을 근본적으로 제거할 요구

#### 한줄 요약
- 1-RTT로 키 교환과 인증을 완결하고 취약 암호를 전면 배제하여 속도와 보안성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **1-RTT 기본 연결(Full Handshake)**: 클라이언트가 ClientHello에 지원 가능한 키 교환 파라미터(Key Share)를 선제적으로 동봉하여 단 1회의 왕복만으로 암호화 데이터 전송을 개시하는 메커니즘.
- **0-RTT 조기 데이터(Early Data / PSK)**: 이전에 접속했던 서버와의 사전 공유 키(PSK)를 활용하여 핸드셰이크 완료 전 첫 번째 패킷(ClientHello)에 암호화된 애플리케이션 데이터를 즉시 실어 보내는 초고속 연결 기법.

</details>

- **연결 지연시간 50% 단축 (1-RTT & 0-RTT)**: TCP 핸드셰이크 직후 단 1회 왕복으로 보안 세션을 완결하고 직전 접속 서버와는 0-RTT 통신 지원
- **구형 취약 암호 및 알고리즘 완전 퇴출**: 정적 RSA 키 교환, DH 정적 파라미터, CBC 블록 모드, RC4, SHA-1을 배제하고 오직 ECDHE/DHE + AEAD만 허용
- **핸드셰이크 암호화 범위 확대**: ServerHello 이후의 모든 메시지(서버 인증서, CertificateVerify, Finished)를 핸드셰이크 단계에서 생성된 임시 키로 암호화 전송

#### 한줄 요약
- 1-RTT/0-RTT 고속 연결, AEAD 전용 강제, 순방향 비밀성(PFS) 보장, 핸드셰이크 메시지 암호화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **트랜스크립트 해시(Transcript Hash)**: ClientHello부터 Finished까지 오간 모든 핸드셰이크 패킷의 바이트열을 SHA-256/384로 누적 해싱하여, 중간자(MITM)의 매개변수 변조(다운그레이드)를 100% 검출하는 상태 해시값.
- **CertificateVerify**: 서버가 보유한 X.509 개인키로 트랜스크립트 해시값을 전자서명하여 자신이 해당 공개키의 정당한 소유자임을 입증하는 인증 메시지.

</details>

```text
[ 클라이언트 (Client: Browser) ]                                   [ 서버 (TLS Web Server) ]
 ├─ 지원 암호 스위트 목록 (AEAD)                                      ├─ X.509 인증서 및 개인키 (HSM 보관)
 └─ 임시 키 생성 (ECDHE X25519)                                       └─ 임시 키 생성 (ECDHE X25519)
           │                                                                   ▲
           ▼ [ 1. ClientHello + Key_Share (ECDHE 공개키 $g^a$) ] ──────────────┘
           │ (누적 Transcript Hash $H_1$ 기록)
           │
           │                                                                   │
           │ ┌─────────────────────────────────────────────────────────────────┘
           │ ▼ [ 2. ServerHello + Key_Share ($g^b$) ] ──▶ (양단 간 Handshake Key 도출)
           │ ├─ {EncryptedExtensions}
           │ ├─ {Certificate} (서버 인증서 체인 - 암호화 전송)
           │ ├─ {CertificateVerify} (Transcript Hash $H_2$에 대한 서버 전자서명)
           │ └─ {Finished} (HKDF로 도출된 무결성 MAC 검증값)
           ▼
[ 3. 클라이언트 검증 및 암호 통신 개시 ]
 ├─ 서버 서명(CertificateVerify) 및 Finished MAC 일치 확인
 └─ [ 4. Application Data (AES-GCM 암호화) 전송 ] ──▶ [ 1-RTT 만에 전송 완료 ]
```

선의 의미: 클라이언트의 첫 패킷에 ECDHE 공개키가 실려 전송되고, 서버가 공개키와 암호화된 인증서를 즉시 회신하여 1-RTT 만에 애플리케이션 데이터 전송이 개시되는 구조

| 구성요소 | 핵심 책임 및 역할 | 비고 |
|:---|:---|:---|
| **ClientHello / Key_Share**| 지원 암호 스위트 제시 및 클라이언트의 ECDHE 임시 공개키($g^a$) 선제 전송 | 1-RTT 기반 |
| **ServerHello / Key_Share**| 선택 암호 스위트 확정 및 서버의 ECDHE 임시 공개키($g^b$) 전송 ➔ 공유 비밀 완성 | Shared Secret |
| **Certificate / CertVerify**| 서버의 X.509 인증서를 전송하고, 트랜스크립트 해시에 서명하여 신원 증명 | Server Auth |
| **Finished 메시지** | HKDF로 도출된 검증 키를 사용하여 전체 핸드셰이크의 HMAC 무결성 최종 확정 | Integrity Check |
| **HKDF 키 스케줄 엔진** | 공유 비밀로부터 Handshake Key와 Application Master Key를 단계별 도출 | RFC 5869 HKDF |

#### 한줄 요약
- ClientHello/Key_Share, ServerHello, CertificateVerify, Finished MAC, HKDF 키 스케줄러가 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **HKDF 3단계 키 도출(Key Schedule)**:
  1. **Early Secret**: 0-RTT 조기 데이터를 암호화하기 위한 사전 공유 키(PSK) 기반 도출
  2. **Handshake Secret**: Certificate, CertificateVerify, Finished 메시지를 암호화하기 위한 임시 키 도출
  3. **Master Secret**: 핸드셰이크 완료 후 실제 애플리케이션 데이터를 양방향 암호화하기 위한 메인 세션키 도출

</details>

```text
1. 클라이언트가 지원 암호(AES-256-GCM) 및 ECDHE 공개키($g^a$)를 담은 ClientHello 송출
            │
            ▼
2. 서버가 지원 암호를 선택하고 자신의 ECDHE 공개키($g^b$)를 담은 ServerHello 회신 ➔ 양단 공유 비밀($g^{ab}$) 도출
            │
            ▼
3. [핸드셰이크 암호화 활성화] 서버가 Handshake Key로 암호화된 Certificate, CertificateVerify, Finished 전송
            │
            ▼
4. 클라이언트가 서버 인증서 체인 및 CertificateVerify 전자서명을 검증하고 Finished MAC 대조
            │
            ▼
5. [핸드셰이크 완료] 클라이언트가 Application Key로 암호화된 HTTP 요청(Application Data)을 전송 (1-RTT 완결)
```

**동작 원리**

1. **선제적 키 공유**: 클라이언트가 예측되는 타원곡선 그룹(X25519)의 공개키를 첫 메시지에 동봉
2. **공유 비밀 합성**: 서버가 자신의 공개키를 응답하는 즉시 양측에서 $g^{ab}$ 도출 완료
3. **암호화 채널 즉시 가동**: 서버 인증서 전송 단계부터 스누핑이 불가능하도록 Handshake Secret으로 암호화
4. **트랜스크립트 무결성 고정**: 오간 모든 메시지 해시에 서버 개인키 서명을 수행하여 다운그레이드 방어
5. **어플리케이션 키 확정**: Finished 교환 완료 즉시 Master Key로 전환하여 라인 레이트 데이터 전송

#### 한줄 요약
- ClientHello/KeyShare 전송, ServerHello 응답 및 공유 비밀 도출, 인증서 암호 전송, 서명 검증, Application Key 통신 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **TLS 1.2 vs TLS 1.3 핸드셰이크 비교**: 왕복 시간(RTT), 보안성, 암호 스위트, 순방향 비밀성(PFS)의 비교.

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

- **0-RTT 재전송 공격(Replay Attack)**: 0-RTT Early Data는 순방향 비밀성이 없고 핸드셰이크 완료 전에 전송되므로, 공격자가 네트워크 상에서 0-RTT 패킷을 캡처하여 서버로 여러 번 재전송할 경우 결제 요청이나 비밀번호 변경과 같은 상태 변경 작업이 중복 실행되는 취약점.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 0-RTT 조기 데이터 캡처 후 재전송으로 인한 **금융 결제 중복 및 상태 변경 트랜잭션 오류** | **0-RTT는 멱등성(Idempotent)이 보장된 GET 요청에만 한정 허용** 및 Single-Use Ticket 강제 | 상태 변경 API 재전송 공격 원천 차단 및 금융 트랜잭션 무결성 보장 |
| 클라이언트가 제시한 Key Share 그룹과 서버 지원 그룹 불일치 시 **HelloRetryRequest 발생(2-RTT로 지연)** | 서버와 클라이언트의 최우선 타원곡선 그룹을 **X25519(Curve25519)로 전사 표준화** | 그룹 불일치 재시도 0% 제거 및 순수 1-RTT 연결률 99.9% 달성 |
| 레거시 L4/L7 방화벽이 TLS 1.3 핸드셰이크 암호화를 비정상 트래픽으로 오인하여 **패킷을 드롭하는 장애** | **미들박스 호환 모드(Middlebox Compatibility Mode: 가짜 ChangeCipherSpec)** 유지 | 구형 네트워크 장비 통과율 100% 확보 및 무중단 TLS 1.3 전환 |

#### 한줄 요약
- 멱등 GET 요청에만 0-RTT를 허용하고, X25519를 표준화하며, 호환 모드로 미들박스 드롭을 방지한다.

## Ⅶ. 결론

- 글로벌 인터넷 웹 트래픽과 클라우드 네이티브 통신의 기본 보안 표준인 **TLS 1.3 핸드셰이크 아키텍처**는 고성능과 고신뢰 보안을 동시에 달성한 핵심 프로토콜이며, 실무 구축 시 **X25519 기반 1-RTT 연결 최적화**, **0-RTT Replay 방어 가드레일 적용**, **PQC(X25519+ML-KEM) 하이브리드 키 교환의 선제적 도입**을 결합하여 무결점 전송 계층 보안 환경을 완성

#### 한줄 요약
- 1-RTT 핸드셰이크와 AEAD 전용 암호화 및 0-RTT 재전송 방어를 결합하여 고속 고보안 통신을 실현한다.
