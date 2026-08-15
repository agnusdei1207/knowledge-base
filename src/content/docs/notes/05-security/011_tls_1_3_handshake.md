---
sidebar:
  order: 11
  label: "011. TLS 1.3 핸드셰이크 (TLS 1.3 Handshake)"
  badge:
    text: "미출제 • 70%"
    variant: note
title: "TLS 1.3 핸드셰이크 (TLS 1.3 Handshake)"
date: "2026-08-13T18:48:54+09:00"
tags:
  - "notes-security"
weight: 11
extra:
  question_no: "011"
  source_status: "미출제"
  source_history: ""
  priority: 70
  priority_note: "핸드셰이크•0-RTT•키 갱신을 묻는 현대 설계 주제임"
---

## Ⅰ. 개요

<details>
<summary>용어 설명</summary>

- **전송 계층 보안(Transport Layer Security, TLS) 1.3 핸드셰이크**: 서버 인증과 임시 키 합의를 결합하는 연결 설정 절차이다.
- **연관 데이터 포함 인증 암호(Authenticated Encryption with Associated Data, AEAD)**: 트래픽의 기밀성과 무결성을 함께 보호하는 인증 암호 방식이다.

</details>

- 정의/개념: 서버 인증과 임시 키 합의를 결합한 **TLS 1.3 핸드셰이크**
- 배경/필요성: 구형 TLS에는 **다중 왕복•취약 암호스위트** 부담이 있다.

#### 한줄 요약

- **1-RTT•ECDHE•인증서 검증**으로 지연과 순방향 비밀성 확보

## Ⅱ. 특징

<details>
<summary>용어 설명</summary>

- **한 번 왕복 시간(One Round-Trip Time, 1-RTT)**: 단 1회의 왕복 교환만으로 키 합의와 서버 신원 인증을 완료하고 응용 트래픽 암호화를 개시하는 구조.
- **사전 공유키(Pre-Shared Key, PSK)**: 이전 암호 세션에서 파생 및 공유한 비밀값을 재연결 키 재료로 활용하는 세션 재개 기법.
- **0-RTT 조기 데이터(0-RTT Early Data)**: PSK를 기반으로 핸드셰이크 완료 전 첫 번째 패킷에 응용 데이터를 포함하여 즉시 전송하는 기술.
- **멱등 요청(Idempotent Request)**: 동일 요청을 수차례 중복 전송하더라도 시스템 상태가 추가 변동되지 않는 읽기 전용(GET 등) 요청.

</details>

- **1-RTT** 구조로 서버 인증과 임시 키 합의를 통합 완료하여 연결 지연 단축
- **AEAD** 전용 암호스위트 채택으로 트래픽 기밀성과 무결성 결합 보장
- **PSK** 기반 **0-RTT 조기 데이터** 적용 시 재전송 방지를 위한 **멱등 요청** 한정 통제

#### 한줄 요약

- 1-RTT 기본 핸드셰이크 구조 준수 및 PSK 기반 0-RTT 조기 데이터 사용 시 재전송 공격 방지를 위한 멱등 요청 한정 통제

## Ⅲ. 구조 및 구성요소

<details>
<summary>용어 설명</summary>

- **대화 기록 해시(Transcript Hash)**: 현재 단계까지 교환된 모든 핸드셰이크 메시지의 순서와 내용을 연쇄적으로 믹싱한 해시 다이제스트.
- **HKDF 키 스케줄(HMAC-based Extract-and-Expand Key Derivation Function Key Schedule)**: 공유 비밀과 대화 기록 해시를 입력으로 단계/방향별 하위 키를 유도하는 표준 키 파생 아키텍처.
- **CertificateVerify**: 서버가 제출된 인증서의 개인키 소지권(PoP)을 대화 기록 해시 서명을 통해 증명하는 메시지.
- **Finished**: 전체 대화 기록 해시 기반 MAC 값을 교환하여 핸드셰이크 과정 전체의 무결성을 최종 입증하는 메시지.

</details>

```text
TLS 1.3 구조
├─ 협상 메시지
├─ 대화 기록 해시
├─ 인증서 검증기
├─ HKDF 키 스케줄
└─ AEAD 레코드 계층
```

가지의 의미: 암호 협상, 기록 축적, 신원 입증, 키 파생 및 레코드 보호 책임을 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| 협상 메시지 | **버전•암호스위트•키 공유** 교환 |
| 대화 기록 해시 | **협상 순서•메시지 무결성** 축적 |
| 인증서 검증기 | **CertificateVerify•Finished** 검증 |
| HKDF 키 스케줄 | **단계•방향별 트래픽 키** 도출 |
| AEAD 레코드 계층 | **기밀성•인증 태그** 검증 |


#### 한줄 요약

- **대화 기록 해시•HKDF•CertificateVerify•Finished** 검증 구조

## Ⅳ. 흐름도

<details>
<summary>용어 설명</summary>

- **ClientHello**: 지원 암호스위트, 그룹 및 클라이언트 ECDHE 키 공유 파라미터를 동시 제출하는 메시지.
- **ServerHello**: 선택된 암호스위트와 서버 ECDHE 키 공유 파라미터를 반환하는 메시지.
- **임시 타원곡선 디피-헬먼(Elliptic Curve Diffie-Hellman Ephemeral, ECDHE)**: 세션별 일회성 키를 생성하여 순방향 비밀성(PFS)을 담보하는 키 교환.
- **핸드셰이크 키(Handshake Traffic Key)**: 핸드셰이크 구간의 암호화 메시지(Certificate, CertificateVerify)를 보호하는 중간 임시 키.
- **응용 트래픽 키(Application Traffic Key)**: 검증 완결 후 양방향 실제 응용 데이터를 보호하는 최종 대칭 세션키.
- **ClientHello 전송**: 클라이언트 키 공유 파라미터 및 암호 스위트를 제안하는 단계.
- **ServerHello 반환**: 서버 키 공유 파라미터를 반환하고 공유 비밀 연산에 진입하는 단계.
- **핸드셰이크 키 도출**: ECDHE 공유 비밀과 대화 기록 해시를 HKDF에 입력하여 핸드셰이크 키를 도출하는 단계.
- **인증서•Finished 검증**: CA 신뢰 경로, CertificateVerify 서명 및 Finished MAC을 판정하는 단계.
- **Finished•응용 트래픽 키 전환**: 클라이언트 Finished 검증 완료 후 응용 트래픽 키로 전환하는 단계.

</details>

```text
1. ClientHello 전송
        │
        ▼
2. ServerHello 반환
        │
        ▼
3. 핸드셰이크 키 도출
        │
        └── CertificateVerify•Finished 수신
                    │
                    ▼
4. 인증서•Finished 검증
        ├─ 실패: 연결 중단
        └─ 성공
             │
             ▼
     5. Finished•응용 트래픽 키 전환
             │
             └── 보호된 응용 데이터 전송
```

### 동작 원리

1. **ClientHello 전송**: 키 공유 파라미터와 지원 암호스위트 제안
2. **ServerHello 반환**: 서버 키 공유와 선택 암호스위트 반환
3. **핸드셰이크 키 도출**: ECDHE 비밀•기록 해시로 **HKDF 키** 도출
4. **인증서•Finished 검증**: 인증서 서명과 Finished MAC 검증
5. **Finished•응용 트래픽 키 전환**: 검증 뒤 양방향 응용 키 활성화


#### 한줄 요약

- **Hello 교환•ECDHE•인증서 검증•응용 키 전환** 수행

## Ⅴ. 종류 및 비교

<details>
<summary>용어 설명</summary>

- **완전 순방향 비밀성(Perfect Forward Secrecy, PFS)**: 장기 개인키가 침해되더라도 과거 생성된 세션키 및 데이터가 복호화되지 않는 특성.
- **전체 1-RTT(Full 1-RTT Handshake)**: 인증서 신원 검증과 새 ECDHE 키 합의를 포함하여 완벽한 PFS를 제공하는 신규 연결.
- **PSK 재개 1-RTT(PSK Resumption 1-RTT)**: 이전 세션의 PSK를 통해 신원 검증을 대체하고 선택적 ECDHE를 수행하는 세션 재개.

</details>

| TLS 1.3 연결 방식 | **전체 1-RTT** | **PSK 재개 1-RTT** | **0-RTT 조기 데이터** |
|:---|:---|:---|:---|
| 적용 기준 | 최초 접속•신규 서버 인증 | 세션 재개 및 고속 연결 | 멱등 조회(GET) 요청 적용 |
| 핵심 특징 | **ECDHE 및 인증서** 종합 검증 | **PSK** 기반 고속 재개 | 핸드셰이크 전 조기 전송 |
| 한계 | 인증서 서명 검증 연산 비용 | 키 미갱신 시 **PFS** 약화 | 재전송 공격(Replay Attack) 위협 |

> 요약: 세션 재개 지연, PFS 및 재전송 공격 위험성을 고려한 연결 방식 선택

#### 한줄 요약

- 최초 접속은 **전체 1-RTT**, 재개는 **PSK 1-RTT**, 멱등 조회만 0-RTT

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>용어 설명</summary>

- **KeyUpdate**: 단일 연결 내에서 레코드 카운터 만료 전 송수신 트래픽 키를 갱신하는 TLS 1.3 전용 메시지.
- **재전송 방지 정책(Anti-Replay Policy)**: Single-use 티켓, 타임스탬프 윈도우 등을 통해 0-RTT 패킷의 중복 재생 공격을 차단하는 통제.
- **RFC 8446(RFC 8446 Standard)**: TLS 1.3 프로토콜 명세 및 키 스케줄 아키텍처를 정의한 IETF 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 프로토콜 구현 불일치 | **RFC 8446** 준수 | 암호 협상•키 스케줄 일관성 확보 |
| 0-RTT 재전송 공격 | **재전송 방지 정책** 적용 | 중복 실행 및 비멱등 요청 침해 차단 |
| 트래픽 키 수명 초과 | **KeyUpdate** 메시지 적용 | 키•논스 재사용에 따른 기밀성 훼손 억제 |

#### 한줄 요약

- **RFC 8446•재전송 방지•KeyUpdate**로 키 수명 통제

## Ⅶ. 결론

<details>
<summary>용어 설명</summary>

- **연결 방식 선택(Connection Mode Selection)**: 트랜잭션의 멱등성 여부 및 PFS 제공 필요성을 기준으로 연결 모드를 결정하는 설계 지침.

</details>

- 상태 변경 요청은 **전체 1-RTT**, 멱등 조회 요청은 **0-RTT 조기 데이터**로 분류하는 연결 정책 수립

#### 한줄 요약

- **ECDHE•HKDF•AEAD•0-RTT 재전송 방지**를 결합
