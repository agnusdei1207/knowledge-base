---
sidebar:
  order: 11
  label: "011. TLS 1.3 핸드셰이크"
  badge:
    text: "미출 · 70%"
    variant: note
title: "초저지연 고보안 전송 계층 보안 프로토콜 : TLS 1.3 핸드셰이크"
date: "2026-08-26T14:24:08+09:00"
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

- 정의/개념: Key Share로 **1-RTT·AEAD·Transcript Hash**를 제공하는 TLS
- 배경/필요성: TLS 1.2는 암호 스위트를 먼저 합의한 뒤에야 키를 교환하느라 연결마다 2-RTT를 치르고 그 협상 폭 안에 CBC·정적 RSA 같은 취약 선택지를 남겨 두었으므로, 선택지를 AEAD·ECDHE로 좁혀 협상 자체를 없애고 첫 패킷에 키를 실어 왕복 한 번을 통째로 걷어낼 필요

#### 한줄 요약
- 1-RTT/0-RTT 연결과 AEAD 전용 암호화를 통해 초저지연과 무결점 전송 계층 보안을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Key Share (키 공유 확장)**: ClientHello에 클라이언트의 ECDHE 임시 공개키($g^a$)를 선제 동봉하여 1-RTT 만에 공유 비밀을 도출하는 기법.
- **Transcript Hash Binding**: 핸드셰이크 중 오간 모든 제어 메시지의 해시값을 서버 전자서명에 결합하여 다운그레이드 공격을 원천 차단하는 기법.

</details>

- **1-RTT·0-RTT**: Key Share로 연결 왕복 지연 단축
- **AEAD 전용**: AES-GCM·ChaCha20만 허용
- **핸드셰이크 암호화**: ServerHello 이후 인증 정보 보호

#### 한줄 요약
- 지연 단축은 클라이언트가 서버 응답을 듣기 전에 키와 데이터를 미리 던지는 데서 오므로, 그만큼 재전송 방어를 프로토콜이 아닌 애플리케이션 멱등성에 떠넘긴 결과다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Handshake Secret vs Application Master Secret**: 인증서와 제어 메시지를 암호화하는 임시 키와 핸드셰이크 완료 후 실제 데이터를 암호화하는 세션키.

</details>

```text
[TLS 1.3 정적 구성]
|-- ClientHello / Key_Share
|-- ServerHello / Key_Share
|-- Certificate / CertVerify
|-- Finished 메시지
`-- HKDF 키 스케줄러
```

선의 의미: 클라이언트의 첫 패킷에 ECDHE 공개키가 실려 전송되고 서버가 공개키와 암호화된 인증서를 즉시 회신하여 1-RTT 만에 데이터 통신이 개시되는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| ClientHello / Key_Share | **클라이언트 ECDHE 키 전송** | 1-RTT |
| ServerHello / Key_Share | **서버 키·공유 비밀 확정** | Shared Secret |
| Certificate / CertVerify | **Transcript Hash 서명** | Server Auth |
| Finished 메시지 | **핸드셰이크 HMAC 검증** | Integrity Check |
| HKDF 키 스케줄러 | **Handshake·Application 키 도출** | RFC 5869 |

#### 한줄 요약
- Key Share를 첫 메시지에 얹어 협상과 키 교환을 한 왕복으로 합친 대신, 클라이언트가 서버가 지원할 곡선을 미리 찍어야 해 빗나가면 재시도 왕복이 되돌아온다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **HKDF 3단계 키 스케줄**: Early Secret(0-RTT 데이터용) → Handshake Secret(제어 메시지 암호화용) → Master Secret(애플리케이션 데이터 암호화용).

</details>

```text
클라이언트 연결 요청
    |
1. ClientHello·Key Share 송출
    |
2. ServerHello·Key Share 회신
    |
3. 핸드셰이크 암호화 전송
    |
4. 서버 신원·MAC 검증
    |
5. Application Data 전송
    |
암호화 통신
```

- 1. ClientHello·Key Share 송출
- 2. ServerHello·Key Share 회신
- 3. 핸드셰이크 암호화 전송
- 4. 서버 신원·MAC 검증
- 5. Application Data 전송

#### 한줄 요약
- 공유 비밀이 2단계에서 이미 서고 인증은 그 뒤에 붙으므로, 인증서와 신원 정보를 평문으로 노출하던 구간이 사라지는 대신 서명 검증 실패는 이미 암호화된 채널 안에서 판정된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **TLS 1.2** vs **TLS 1.3**.

</details>

| 비교 항목 | TLS 1.2 핸드셰이크 (Legacy) | TLS 1.3 핸드셰이크 (Modern Standard) |
|:---|:---|:---|
| 기본 연결 지연시간 | **2-RTT** | **1-RTT** |
| 세션 재개 지연시간 | 1-RTT | **0-RTT** |
| 순방향 비밀성 | 선택 | **ECDHE·DHE 필수** |
| 허용 암호 스위트 | CBC·RC4·정적 RSA 포함 | **AEAD 전용** |
| 핸드셰이크 패킷 보호 | 인증 정보 평문 | **ServerHello 이후 암호화** |
| 알고리즘 다운그레이드 | 변조 위험 | **Transcript Hash 차단** |

#### 한줄 요약
- TLS 1.2는 2-RTT에 취약 암호가 혼재되었으나, TLS 1.3은 1-RTT/0-RTT에 AEAD 전용 및 핸드셰이크 암호화를 제공한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **0-RTT Replay Attack**: 0-RTT 조기 데이터는 PFS가 없어 공격자가 네트워크에서 캡처한 패킷을 재전송할 경우 중복 결제나 상태 변경이 발생하는 취약점.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 0-RTT 재전송으로 중복 결제 | **멱등 GET·Single-Use Ticket** | Replay 차단 |
| Key Share 불일치로 재시도 | **X25519 표준화** | 1-RTT 성공률 향상 |
| 미들박스 오인으로 패킷 드롭 | **Middlebox 호환 모드** | 구형 장비 통과 |
| SNDL 양자 해독 위협 | **X25519·ML-KEM 하이브리드** | 장기 기밀성 확보 |

#### 한줄 요약
- 멱등 GET 요청에만 0-RTT를 허용하고, X25519를 표준화하며, 호환 모드로 미들박스 드롭을 방지한다.

## Ⅶ. 결론

- 일반 연결은 **1-RTT·X25519**, 멱등 재개만 **0-RTT** 허용

#### 한줄 요약
- TLS 1.3은 1-RTT 핸드셰이크와 AEAD 전용 암호화 및 0-RTT 재전송 방어를 결합하여 고속 고보안 통신을 실현하는 표준 프로토콜이다.
