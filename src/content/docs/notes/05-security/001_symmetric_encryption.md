---
sidebar:
  order: 1
  label: "001. 대칭 암호화"
  badge:
    text: "기출 · 50%"
    variant: note
title: "고속 블록/스트림 데이터 암호화 : 대칭키 암호화"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 1
extra:
  question_no: "1"
  source_status: "기출"
  source_history: "122회"
  priority: 50
  priority_note: "블록 암호(AES-GCM/XTS), 스트림 암호(ChaCha20-Poly1305), AEAD 인증 암호화 및 논스(Nonce) 관리"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Symmetric Encryption (대칭키 암호화)**: 암호화와 복호화에 동일한 단일 비밀키(Secret Key)를 사용하는 암호 알고리즘 체계.
- **AEAD (Authenticated Encryption with Associated Data, RFC 5116)**: 기밀성 암호화와 무결성 인증 태그 생성을 일체형으로 연산하는 운용 모드.

</details>

- 정의/개념: 송수신자가 공유한 단일 비밀키로 **치환과 순열을 반복하여 대용량 데이터의 기밀성과 AEAD 무결성을 초고속 보호하는 암호화 기술**
- 배경/필요성: 공개키 암호의 복잡한 수학 연산으로 인한 **CPU 오버헤드, 대용량 파일/패킷 암호화 시 처리 지연 폭증 및 실시간 통신 적용 불가**

#### 한줄 요약
- 단일 비밀키와 AEAD 모드를 통해 대용량 데이터의 기밀성과 무결성을 하드웨어 가속 속도로 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SPN (Substitution-Permutation Network)**: S-Box(치환)를 통한 혼돈(Confusion)과 P-Box(순열)를 통한 확산(Diffusion)을 반복하는 블록 암호 구조.
- **AES-NI (AES New Instructions)**: x86 CPU 칩셋에 내장되어 AES 암복호화 연산을 1사이클 내외로 가속하는 하드웨어 명령어 셋.

</details>

- **압도적인 초고속 연산 처리율**: 공개키 암호 대비 **1,000배 이상 빠른 속도로 기가비트 라인레이트 암호화 지원**
- **기밀성과 무결성의 동시 보증(AEAD)**: AES-GCM 및 ChaCha20-Poly1305를 통해 **암호화와 동시에 128비트 변조 방지 태그 생성**
- **하드웨어 가속(AES-NI) 최적화**: 최신 CPU 하드웨어 명령어를 활용하여 **CPU 점유율 극소화 및 전력 효율 극대화**

#### 한줄 요약
- 초고속 연산, AEAD 기밀성/무결성 일체형 보증, AES-NI 하드웨어 가속을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Nonce (Number used once)**: 동일 키 환경에서 암호문의 무작위성을 보장하기 위해 매 암호화마다 고유하게 부여하는 96비트 일회용 난수.

</details>

```text
[AEAD 대칭 암호화 및 검증 파이프라인]
|-- Application Plaintext & AAD (평문 데이터 + 헤더 메타데이터)
`-- AEAD Crypto Engine (AES-GCM / ChaCha20-Poly1305)
    |-- 1. Secret Key (128/256bit 대칭키) & Nonce (96bit 고유 난수)
    |-- 2. Confidentiality: CTR 모드 블록 암호화 -> [ Ciphertext ]
    `-- 3. Integrity: GHASH/Poly1305 다항식 연산 -> [ 128bit Auth Tag ]
`-- Receiver Verify-then-Decrypt Engine
    |-- 1. 수신된 Tag와 AAD를 GHASH로 재계산하여 무결성 사전 검증
    |-- [불일치 시] -> 복호화 거부 및 패킷 즉각 폐기 (MAC Error)
    `-- [일치 시] -> CTR 복호화로 평문 완전 복원
```

선의 의미: KMS에서 할당된 키와 논스를 바탕으로 AEAD 모듈이 암호문과 인증 태그를 동시 생성하고 수신단이 태그를 우선 검증한 후 복호화하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **비밀키 (Secret Key)** | 암/복호화에 공통 사용되는 **128/256비트 대칭키 (유출 시 전면 침해)** | NIST SP 800-131A |
| **논스 / IV (Nonce)** | 암호문 무작위성을 부여하는 **96비트 일회용 난수 (재사용 절대 금지)** | RFC 5116 |
| **AEAD 암호 엔진** | 블록/스트림 암호화와 **Galois 필드 기반 GHASH 인증 연산 동시 실행** | AES-GCM / ChaCha20 |
| **인증 태그 (Auth Tag)**| 암호문 및 AAD의 **위변조 여부를 보증하는 128비트 메시지 인증 코드** | GMAC Tag |
| **KMS / HSM 금고** | 대칭키의 생성, 보관, **순환(Rotation), 파기를 안전하게 전담하는 하드웨어** | FIPS 140-3 Level 3 |

#### 한줄 요약
- 비밀키, 논스(IV), AEAD 엔진, 인증 태그, KMS/HSM 키 관리기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Verify-then-Decrypt (인증 후 복호화)**: 암호문을 풀기 전에 반드시 인증 태그를 먼저 검증하여 패딩 오라클 공격과 CPU 자원 낭비를 원천 차단하는 원칙.

</details>

```text
대칭키 암호화, GHASH 태그 생성, 패킷 전송 및 수신 검증 파이프라인
        │
   1. [키/논스 발급] 송신 앱이 KMS로부터 256비트 AES 키 핸들 및 고유 96비트 Nonce 획득
        │
   2. [CTR 암호화 및 태그 생성] AES-GCM 엔진이 CTR 모드로 암호화하고 128비트 GMAC 태그 생성
        │
   3. [보안 패키지 전송] 네트워크를 통해 [Nonce + AAD + Ciphertext + Tag] 전송
        │
   4. [수신단 태그 사전 검증] 수신단 AEAD 엔진이 AAD와 Nonce로 GHASH를 재계산하여 수신 Tag와 대조
        │
   ├─ [Tag 불일치 시] ➔ 복호화 즉시 중단 및 에러 반환 (패킷 폐기)
   ▼
5. [안전한 복호화] 무결성 검증 완료 후 CTR 복호화 연산을 실행하여 원본 평문 복원
```

#### 한줄 요약
- 키/논스 할당 → CTR 암호화 및 GMAC 태그 생성 → 패킷 전송 → 태그 사전 검증 → 안전한 평문 복원 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AES-GCM (블록 AEAD)** vs **ChaCha20-Poly1305 (스트림 AEAD)** vs **AES-XTS (스토리지 섹터 전용)**.

</details>

| 비교 항목 | AES-GCM (블록 기반 AEAD) | ChaCha20-Poly1305 (스트림 AEAD) | AES-XTS (섹터 단위 스토리지) |
|:---|:---|:---|:---|
| **암호화 분류** | **128비트 블록 암호 (Rijndael 기반)** | **256비트 스트림 암호 (ARX 연산)** | **블록 암호 (XEX 기반 트위크 모드)** |
| **무결성 인증 (AEAD)**| **지원 (128bit GMAC 태그 생성)** | **지원 (128bit Poly1305 태그 생성)** | **미지원 (기밀성 전용, 태그 오버헤드 없음)** |
| **하드웨어 가속** | **AES-NI 명령어 필수 (서버 최적화)** | **소프트웨어 순수 연산 최적화 (모바일)**| AES-NI 하드웨어 가속 지원 |
| **주요 장점** | x86 서버 환경에서 압도적 속도 | CPU 가속기 없는 환경에서 3배 빠름 | 섹터 크기 불변 (BitLocker 표준) |
| **주요 적용 영역** | **TLS 1.3, IPsec, 클라우드 DB 암호화**| **모바일 TLS 1.3, WireGuard VPN** | **NVMe SSD, 하드디스크 전영역 암호화**|

#### 한줄 요약
- AES-GCM은 서버/TLS 1.3 표준, ChaCha20은 모바일/WireGuard 표준, AES-XTS는 스토리지 전용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Nonce Reuse Catastrophe**: 동일 대칭키에서 동일 Nonce를 2회 이상 사용 시 두 암호문의 XOR 차분으로 GHASH 인증키($H$)가 노출되어 임의 위조가 가능해지는 치명적 결함.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 동일 대칭키 환경에서 Nonce 재사용으로 인한 **인증 키($H$) 노출 및 암호문 위조** | **결정론적 64비트 단조 증가 카운터 기반 Nonce 또는 `XChaCha20(192bit)`** 채택 | Nonce 충돌 확률 0% 보장 및 키스트림 노출 원천 차단 |
| 수신단에서 무결성 검증 전 복호화로 인한 **패딩 오라클(Padding Oracle) 공격** | **반드시 AEAD 태그 검증 통과 후에만 복호화를 허용하는 `Verify-then-Decrypt`** 강제 | 위조된 악성 페이로드 연산 거부 및 사이드채널 방어 |
| 소스 코드나 환경 변수 파일에 대칭 마스터키 하드코딩으로 인한 키 유출 | **`KMS/Vault 연동 기반 키 엔벨로프(Envelope Encryption: DEK/KEK)`** 적용 | 소스 유출 시에도 마스터키 보호 및 자동 키 순환 보장 |
| TLS 통신 중 양자컴퓨터의 미래 해독 위협(Store Now, Decrypt Later) | **AES-128을 폐기하고 `양자 내성을 갖춘 AES-256 / 256비트 대칭키`로 상향** | Grover 알고리즘 공격에 대해 128비트 양자 보안 강도 유지 |

#### 한줄 요약
- 단조 증가 카운터로 논스 충돌을 막고, Verify-then-Decrypt로 변조를 차단하며, KMS 엔벨로프로 키를 보호한다.

## Ⅶ. 결론

- 초연결 디지털 인프라에서 대규모 데이터의 기밀성과 무결성을 보장하기 위해 **대칭키 암호화 아키텍처를 핵심 기반으로 채택**하되, 실무 구축 시 **AES-GCM 및 ChaCha20-Poly1305 등 표준 AEAD 모드 필수 적용, 엄격한 Nonce 유일성 통제, KMS/HSM 기반 엔벨로프 암호화(DEK/KEK) 수명주기 관리**를 통합 구현하여 완결성 높은 고신뢰 데이터 보호 환경 완성

#### 한줄 요약
- 대칭키 암호화는 표준 AEAD 운용 모드와 엄격한 논스 관리 및 KMS 기반 수명주기 통제를 통해 초고속 고신뢰 데이터 보호를 실현하는 핵심 암호 기술이다.