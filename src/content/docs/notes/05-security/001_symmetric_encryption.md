---
sidebar:
  order: 1
  label: "001. 대칭 암호화"
  badge:
    text: "기출 · 50%"
    variant: note
title: "고속 블록/스트림 데이터 암호화 : 대칭키 암호화"
date: "2026-08-26T14:24:06+09:00"
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

- 정의/개념: 동일 **비밀키**로 암호화·복호화하는 암호 방식
- 배경/필요성: 공개키 연산만으로는 **대용량 처리량 제약**

#### 한줄 요약
- 단일 비밀키와 AEAD 모드를 통해 대용량 데이터의 기밀성과 무결성을 하드웨어 가속 속도로 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SPN (Substitution-Permutation Network)**: S-Box(치환)를 통한 혼돈(Confusion)과 P-Box(순열)를 통한 확산(Diffusion)을 반복하는 블록 암호 구조.
- **AES-NI (AES New Instructions)**: x86 CPU 칩셋에 내장되어 AES 암복호화 연산을 1사이클 내외로 가속하는 하드웨어 명령어 셋.

</details>

- 공개키 암호보다 낮은 연산 비용과 **높은 처리량**
- **AEAD**로 기밀성과 무결성을 함께 제공
- **AES-NI** 기반 블록 암호 연산 가속

#### 한줄 요약
- 초고속 연산, AEAD 기밀성/무결성 일체형 보증, AES-NI 하드웨어 가속을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Nonce (Number used once)**: 동일 키 환경에서 암호문의 무작위성을 보장하기 위해 매 암호화마다 고유하게 부여하는 96비트 일회용 난수.

</details>

```text
AEAD
|-- Secret Key
|-- Nonce
|-- AEAD Engine
|-- Authentication Tag
`-- KMS and HSM
```

선의 의미: KMS에서 할당된 키와 논스를 바탕으로 AEAD 모듈이 암호문과 인증 태그를 동시 생성하고 수신단이 태그를 우선 검증한 후 복호화하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Secret Key** | 암호화·복호화 공통 키 |
| **Nonce** | 키별 암호화 입력의 유일성 제공 |
| **AEAD Engine** | 암호문과 인증 태그 생성 |
| **Authentication Tag** | 암호문·AAD 무결성 검증 |
| **KMS and HSM** | 키 생성·보관·순환·폐기 |

#### 한줄 요약
- 비밀키, 논스(IV), AEAD 엔진, 인증 태그, KMS/HSM 키 관리기가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Verify-then-Decrypt (인증 후 복호화)**: 암호문을 풀기 전에 반드시 인증 태그를 먼저 검증하여 패딩 오라클 공격과 CPU 자원 낭비를 원천 차단하는 원칙.

</details>

```text
대칭키 암호화, GHASH 태그 생성, 패킷 전송 및 수신 검증 파이프라인
        │
   1. [키 및 논스 할당]
        │
   2. [암호문 및 태그 생성]
        │
       [보안 패키지 전송]
        │
   3. [수신 태그 검증]
        │
   ├─ [불일치: 폐기]
   ▼
   4. [검증 후 복호화]
```

- 1. 키 및 논스 할당
- 2. 암호문 및 태그 생성
- 3. 수신 태그 검증
- 4. 검증 후 복호화

#### 한줄 요약
- 키/논스 할당 → CTR 암호화 및 GMAC 태그 생성 → 패킷 전송 → 태그 사전 검증 → 안전한 평문 복원 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AES-GCM (블록 AEAD)** vs **ChaCha20-Poly1305 (스트림 AEAD)** vs **AES-XTS (스토리지 섹터 전용)**.

</details>

| 비교 항목 | AES-GCM (블록 기반 AEAD) | ChaCha20-Poly1305 (스트림 AEAD) | AES-XTS (섹터 단위 스토리지) |
|:---|:---|:---|:---|
| 암호 구조 | AES 블록 암호 | ARX 스트림 암호 | XEX 기반 블록 암호 |
| 무결성 인증 | **GCM 태그** | **Poly1305 태그** | 미지원 |
| 가속 특성 | AES 명령 활용 | 소프트웨어 구현에 유리 | AES 명령 활용 |
| 주요 적용 | TLS·IPsec | TLS·WireGuard | 디스크 섹터 암호화 |

#### 한줄 요약
- AES-GCM은 서버/TLS 1.3 표준, ChaCha20은 모바일/WireGuard 표준, AES-XTS는 스토리지 전용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Nonce Reuse Catastrophe**: 동일 대칭키에서 동일 Nonce를 2회 이상 사용 시 두 암호문의 XOR 차분으로 GHASH 인증키($H$)가 노출되어 임의 위조가 가능해지는 치명적 결함.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 논스 재사용으로 **키스트림·태그 위조 위험** | 단조 카운터 또는 **XChaCha20 논스** | 키별 논스 중복 방지 |
| 태그 검증 전 평문 사용 | **Verify-then-Decrypt** 강제 | 위조 평문 처리 방지 |
| 소스에 마스터키 하드코딩 | KMS 기반 **Envelope Encryption** | DEK·KEK 분리 관리 |
| 양자 탐색으로 키 강도 저하 | **AES-256** 적용 검토 | Grover 공격 여유 확보 |

#### 한줄 요약
- 단조 증가 카운터로 논스 충돌을 막고, Verify-then-Decrypt로 변조를 차단하며, KMS 엔벨로프로 키를 보호한다.

## Ⅶ. 결론

- 통신은 **AEAD**, 디스크 섹터는 **AES-XTS** 선택

#### 한줄 요약
- 대칭키 암호화는 표준 AEAD 운용 모드와 엄격한 논스 관리 및 KMS 기반 수명주기 통제를 통해 초고속 고신뢰 데이터 보호를 실현하는 핵심 암호 기술이다.
