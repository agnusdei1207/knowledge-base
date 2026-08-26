---
sidebar:
  order: 3
  label: "003. 하이브리드 암호"
  badge:
    text: "기출 · 30%"
    variant: note
title: "키 교환과 대용량 데이터 전송의 결합 : 하이브리드 암호"
date: "2026-08-26T14:26:36+09:00"
tags:
  - "notes-security"
weight: 3
extra:
  question_no: "3"
  source_status: "기출"
  source_history: "122회"
  priority: 30
  priority_note: "KEM(키 캡슐화 메커니즘) + DEM(데이터 캡슐화 메커니즘), KDF 키 스케줄링, RFC 9180 HPKE 표준"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Hybrid Cryptography**: 비대칭키의 안전한 키 교환과 대칭키의 고속 대용량 암호화를 결합한 현대 실용 암호체계.
- **KEM & DEM (RFC 9180 HPKE)**: 비대칭키로 세션키를 안전하게 교환하는 KEM 계층과 대칭키로 페이로드를 암호화하는 DEM 계층.

</details>

- 정의/개념: **KEM·KDF·DEM**을 결합한 복합 암호 방식
- 배경/필요성: 단일 암호 방식으로 **키 배송·대용량 성능 양립 제약**

#### 한줄 요약
- 비대칭 KEM 키 교환과 대칭 DEM 고속 암호화를 결합하여 성능과 보안성을 동시에 충족한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **HKDF (HMAC-based Key Derivation Function, RFC 5869)**: KEM에서 교환된 공유 비밀(Shared Secret)로부터 암호학적으로 독립된 방향별 대칭키를 유도하는 표준 키 유도 함수.

</details>

- 비대칭 **KEM**과 대칭 **DEM**의 역할 분리
- **HKDF 도메인 분리**로 방향·용도별 키 도출
- 임시 ECDHE 사용 시 **순방향 비밀성** 제공

#### 한줄 요약
- 보안/성능 양립, KEM+DEM 2계층 분업화, ECDHE 기반 순방향 비밀성(PFS)을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Client/Server Write Key**: 단일 공유 비밀로부터 HKDF를 통해 클라이언트 송신용과 서버 송신용으로 각각 독립 유도된 256비트 대칭키.

</details>

```text
Hybrid Cryptography
|-- Authentication Module
|-- KEM Module
|-- KDF Module
`-- DEM Module
```

선의 의미: KEM 계층에서 비대칭 암호화로 공유 비밀을 교환하고 KDF 계층에서 방향별 대칭키를 도출한 후 DEM 계층에서 대용량 데이터를 초고속 AEAD 암호화하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Authentication Module** | 인증서·트랜스크립트 검증 |
| **KEM Module** | 공유 비밀 캡슐화·합의 |
| **KDF Module** | **HKDF** 기반 방향·용도별 키 도출 |
| **DEM Module** | **AEAD** 본문 암호화·인증 |

#### 한줄 요약
- 신원 인증 모듈, KEM 키 캡슐화, KDF 키 도출기, DEM AEAD 데이터 엔진이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Transcript Hash Binding**: 암호 협상 과정에서 공격자가 약한 알고리즘으로 다운그레이드하는 것을 막기 위해 모든 제어 메시지의 해시값을 최종 서명에 결합하는 기법.

</details>

```text
하이브리드 암호 스위트 협상, KEM 키 교환, KDF 유도 및 DEM 암호화 파이프라인
        │
   1. [암호 스위트 협상 및 인증]
        │
   2. [KEM 공유 비밀 수립]
        │
   3. [KDF 방향별 키 도출]
        │
   4. [DEM 본문 암호화]
        │
   ▼
   5. [AEAD 검증 및 복호화]
```

- 1. 암호 스위트 협상 및 인증
- 2. KEM 공유 비밀 수립
- 3. KDF 방향별 키 도출
- 4. DEM 본문 암호화
- 5. AEAD 검증 및 복호화

#### 한줄 요약
- 파라미터 협상 → KEM 공유 비밀 생성 → HKDF 방향별 키 도출 → DEM 대칭 암호화 → AEAD 태그 검증 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **정적 RSA (레거시)** vs **ECDHE (현재 표준)** vs **PQC KEM 결합 (미래 양자내성)**.

</details>

| 비교 항목 | 정적 RSA 키 전송 (Legacy) | ECDHE 기반 하이브리드 (Current) | PQC KEM 결합 하이브리드 (Future) |
|:---|:---|:---|:---|
| 키 설정 | RSA 키 전송 | **ECDHE** | ECDHE와 **ML-KEM** 결합 |
| 순방향 비밀성 | 미지원 | 임시 키 폐기 시 지원 | 구성과 키 폐기에 좌우 |
| 양자 공격 | Shor 알고리즘에 취약 | Shor 알고리즘에 취약 | PQC KEM 포함 |
| 크기·연산 | RSA 연산 부담 | 작은 키와 빠른 연산 | 캡슐 크기·연산 증가 |
| 주요 적용 | 레거시 TLS | TLS 1.3·SSH·IKEv2 | 전환기 하이브리드 TLS |

#### 한줄 요약
- RSA는 PFS 미지원으로 폐기되었으며, 현재는 ECDHE가 표준이고, 미래 양자 방어를 위해 PQC 하이브리드가 채택된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Cipher Downgrade Attack**: 중간자 공격자가 협상 패킷을 변조하여 취약한 레거시 암호 스위트(TLS 1.0/DES)를 강제 선택하게 만드는 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 협상 변조로 **다운그레이드 공격** | **트랜스크립트 인증** | 협상 무결성 검증 |
| 컨텍스트 누락으로 **키 충돌** | HPKE Label 기반 **도메인 분리** | 키 용도 독립성 확보 |
| **SNDL 양자 위협** | X25519와 **ML-KEM 하이브리드** | 고전·PQC 위험 분산 |
| 세션 티켓 키 노출 | **STEK 자동 순환** | 노출 시간 범위 제한 |

#### 한줄 요약
- 트랜스크립트 서명으로 다운그레이드를 방어하고, HPKE 도메인 분리로 키 충돌을 막으며, PQC KEM으로 양자 위협을 차단한다.

## Ⅶ. 결론

- 현재는 **ECDHE-KEM**, 양자 전환은 **하이브리드 KEM** 선택

#### 한줄 요약
- 하이브리드 암호는 비대칭 KEM 키 교환과 대칭 DEM 고속 암호화 및 PQC 하이브리드 전환을 결합하여 고효율 보안 통신을 실현하는 표준 아키텍처다.
