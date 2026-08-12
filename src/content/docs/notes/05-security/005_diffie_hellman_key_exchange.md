---
sidebar:
  order: 5
  label: "005. 디피-헬만 키 교환 (Diffie-Hellman Key Exchange)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "디피-헬만 키 교환 (Diffie-Hellman Key Exchange)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-security"
weight: 5
extra:
  question_no: "005"
  source_status: "기출"
  source_history: "128회"
  priority: 30
  priority_note: "128회 기출이나 키 교환 단독 반복 흐름은 제한적임"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **디피-헬만 키 교환(Diffie-Hellman Key Exchange, DH 키 교환)**: 비밀값을 직접 전송하지 않고 공개값 교환만으로 동일한 공유 비밀을 안전하게 합의하는 암호 알고리즘.
- **DH 키 합의(DH Key Agreement)**: 도청 가능한 채널에서 공개 매개변수와 각자의 개인값을 결합하여 대칭 세션키의 원재료를 도출하는 기법.
- **통신 경로 직접 전송 위험(In-Transit Direct Transmission Risk)**: 네트워크상에 대칭키를 직접 평문 전송 시 도청 및 유출이 발생하는 보안 위험.

</details>

- 정의/개념: 공개값 교환을 통하여 송수신자가 비밀키 공유를 도출하는 **DH 키 합의** 메커니즘
- 배경/필요성: 네트워크상 비밀키 직접 전송 시 발생하는 도청 및 유출 위험(In-Transit Key Exposure)을 완벽히 차단

#### 한줄 요약

- 비밀값 직접 전송 없이 공개값 교환과 모듈러 지수 연산으로 공유 비밀을 합의하는 비대칭 키 교환 메커니즘

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **공유 비밀(Shared Secret)**: 송수신 당사자가 각자의 개인값과 상대의 공개값을 조합하여 독립적으로 산출하는 동질의 암호값.
- **순방향 비밀성(Perfect Forward Secrecy, PFS)**: 세션마다 일회성 임시 키를 사용하여 향후 장기 키가 노출되더라도 이전 통신 내용을 복호화할 수 없게 하는 성질.
- **중간자 공격(Man-In-The-Middle Attack, MITM)**: 공격자가 통신 중간에서 공개값을 가로채고 자신의 공개값으로 교체하여 양단 간 키를 각각 합의하는 위협.

</details>

- 비밀키 직접 전송 없는 안전한 **공유 비밀** 도출
- 세션별 일회성 임시 키 기반 **순방향 비밀성** 보장
- 전자서명/인증서 결합을 통한 **중간자 공격** 차단

#### 한줄 요약

- 중간자 공격(MITM) 방지를 위해 PKI 기반 서명 인증서와 임시 DH(ECDHE) 결합을 통한 순방향 비밀성 확보 필수

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **도메인 매개변수(Domain Parameters)**: DH 연산에 사용되는 소수 $p$ 및 생성원 $g$ 등 사전 정의된 공개 그룹 정보.
- **개인값(Private Value)**: 각 당사자가 난수로 생성하여 외부에 절대 공개하지 않는 무작위 비밀값 $a, b$.
- **공개값(Public Value)**: 개인값과 도메인 매개변수를 바탕으로 연산하여 상대방에게 전달하는 지수승 값 $g^a \bmod p$.
- **키 유도 함수(Key Derivation Function, KDF)**: 도출된 공유 비밀을 암호학적 엔트로피 확장 과정을 거쳐 세션키로 변환하는 함수.
- **임시 키 생성기(Ephemeral Key Generator)**: 세션 개설 시마다 안전한 일회성 개인키 및 공개키 쌍을 난수로 발급하는 연산부.
- **공유 비밀 계산기(Shared Secret Calculator)**: 수신된 상대 공개값과 본인의 개인값을 모듈러 지수 연산하여 동일 공유 비밀을 도출하는 모듈.

</details>

```text
DH 키 합의 구조
├─ 도메인 매개변수
├─ 임시 키 생성기
├─ 공유 비밀 계산기
└─ 키 유도 함수
```

가지의 의미: 도메인 설정, 키 발급, 공유 비밀 연산, 세션키 파생 책임을 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| 도메인 매개변수 | 검증된 그룹 및 생성원 정보 제공 |
| 임시 키 생성기 | 세션별 개인값 및 공개값 생성 |
| 공유 비밀 계산기 | 상대 공개값과 본인 개인값 연산 |
| 키 유도 함수 | 공유 비밀 기반 세션키 파생 |


#### 한줄 요약

- 도메인 매개변수 공유, 임시 키쌍 생성, 모듈러 지수 연산 기반 공유 비밀 도출 및 KDF를 통한 세션키 파생 구조

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **공개값 검증(Public Value Validation)**: 전달받은 공개값이 지정된 군(Group) 내 유효한 범위에 존재하는지 검증하여 소분군 공격 방어.
- **협상 기록 인증(Transcript Authentication)**: 세션 시작 시 교환한 DH 파라미터와 공개값에 대해 전자서명을 부가하여 무결성을 증명함.
- **공유 비밀 계산(Shared Secret Computation)**: 상대의 공개값과 나의 개인값을 조합하여 $g^{ab} \bmod p$ 형태의 공유 비밀을 연산하는 단계.
- **세션키 도출(Session Key Derivation Stage)**: 도출된 공유 비밀을 KDF의 입력으로 사용하여 실제 본문 암호화키를 파생하는 연산.
- **임시 키쌍 생성(Ephemeral Keypair Generation)**: 세션별 독립적인 개인값 및 공개값을 새로 난수 생성하는 단계.
- **공개값•기록 검증(Public Value & Transcript Verification)**: 상대방의 서명과 공개값의 유효 범위를 종합 검증하는 단계.

</details>

```text
1. 임시 키쌍 생성
        │
        └── 인증된 공개값 상호 교환
                    │
                    ▼
2. 공개값•기록 검증
        ├─ 실패: 키 합의 중단
        └─ 성공
              │
              ▼
     3. 공유 비밀 계산
              │
              ▼
     4. 세션키 도출
```

### 동작 원리

1. **임시 키쌍 생성**: 안전한 도메인 매개변수 기반 임시 키쌍 생성 수행
2. **공개값•기록 검증**: 서명 검증 및 공개값 유효성 검증 처리
3. **공유 비밀 계산**: 상대 공개값과 내 개인값을 연산하는 공유 비밀 계산 수행
4. **세션키 도출**: KDF 연산 기반 본문 암호화용 세션키 도출 완료


#### 한줄 요약

- 소분군 공격 방지를 위한 공개값 유효성 검증 및 상대 신원 인증 후 공유 비밀 연산 수행

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **정적 디피-헬만(Static Diffie-Hellman, Static DH)**: 개인값을 영구적/장기적으로 재사용하여 순방향 비밀성이 결여된 무인증 키 합의.
- **임시 디피-헬만(Diffie-Hellman Ephemeral, DHE)**: 유한체 상에서 세션마다 새로운 개인값을 생성하여 순방향 비밀성을 보장함.
- **타원곡선 임시 디피-헬만(Elliptic Curve Diffie-Hellman Ephemeral, ECDHE)**: 타원곡선 암호(ECC) 알고리즘을 결합하여 적은 키 길이로 고속 DHE를 제공하는 방식.

</details>

| DH 키 교환 방식 | **정적 DH** | **DHE** | **ECDHE** |
|:---|:---|:---|:---|
| 적용 기준 | 기존 정적 DH 호환 | TLS의 유한체 임시 합의 | 작은 키의 임시 합의 요구 |
| 핵심 특징 | 장기 DH 개인값 재사용 | 세션별 유한체 개인값 | 세션별 타원곡선 개인값 |
| 한계 | 장기키 유출 시 과거 노출 | 큰 매개변수 처리 비용 | 곡선•공개값 검증 누락 |

> 요약: 순방향 비밀성 및 연산 효율성을 고려한 DHE/ECDHE 중심 적용

#### 한줄 요약

- 정적 DH의 장기키 유출 위험을 극복하기 위해 세션별 일회성 키를 생성하는 DHE 및 연산 효율성이 뛰어난 ECDHE 채택

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **IETF(Internet Engineering Task Force)**: 인터넷 관련 기술 표준(RFC)을 제정하는 국제 표준화 기구.
- **RFC 7919(RFC 7919 Standard)**: TLS 전송 시 취약한 DH 그룹 사용을 금지하고 검증된 FFDHE 안전 그룹을 규정한 표준.
- **FFDHE(Finite Field Diffie-Hellman Ephemeral)**: RFC 7919에서 정의된 검증된 안전 유한체 그룹 기반의 DHE 교환 방식.
- **TLS(Transport Layer Security)**: 인터넷 통신 시 신원 인증, 기밀성, 무결성을 보장하는 암호화 프로토콜.
- **IRTF(Internet Research Task Force)**: 장기적인 암호학 및 인터넷 기술을 연구하는 IETF 산하 연구 기구.
- **RFC 7748(RFC 7748 Standard)**: X25519 및 X448 타원곡선 DH 연산과 안전 구현 가이드를 명시한 문건.
- **X25519(Curve25519 Key Exchange)**: Curve25519 기반의 고속 및 소분군 공격 면역 타원곡선 DH 알고리즘.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 임의 유한체 그룹 | **IETF RFC 7919 FFDHE** 표준 적용 | 매개변수 공격 억제 |
| 곡선•공개값 구현 오류 | **IRTF RFC 7748 X25519** 표준 적용 | 상호운용성 확보 |
| **중간자 공격** | **TLS** 인증서•협상 기록 서명 | 상대 신원 보장 |

#### 한줄 요약

- RFC 7919(FFDHE) 및 RFC 7748(X25519) 검증 그룹 사용과 TLS 서명 연계로 중간자 공격 및 매개변수 공격 차단

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **인증된 임시 키 합의(Authenticated Ephemeral Key Agreement)**: 공개키 인증서로 신원을 입증하고 세션별 일회성 DH 키로 PFS를 확보하는 표준 형태.
- **DH 키 교환 방식 선택(DH Key Exchange Selection)**: 시스템 성능, 연산 자원 및 보안 요구수준에 맞춘 정적/DHE/ECDHE 방식의 결정.

</details>

- 순방향 비밀성 보장을 위한 **인증된 임시 키 합의** 아키텍처 및 **ECDHE** 기반의 **DH 키 교환 방식 선택** 필수

#### 한줄 요약

- PKI 기반 서명 인증, 검증된 도메인 그룹 사용, 세션별 일회성 ECDHE 적용을 통한 안전한 임시 키 합의 체계 구축 필수
