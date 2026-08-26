---
sidebar:
  order: 5
  label: "005. 디피-헬만 키 교환"
  badge:
    text: "기출 · 30%"
    variant: note
title: "안전한 대칭키 합의 프로토콜 : 디피-헬만 키 교환"
date: "2026-08-26T14:29:08+09:00"
tags:
  - "notes-security"
weight: 5
extra:
  question_no: "5"
  source_status: "기출"
  source_history: "128회"
  priority: 30
  priority_note: "이산대수(DLP) 및 타원곡선(ECDHE), 순방향 비밀성(PFS), 중간자 공격(MITM) 방어 및 RFC 7919 FFDHE"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Diffie-Hellman Key Exchange (DH)**: 안전하지 않은 채널에서 사전 비밀키 없이 공개값 교환만으로 동일한 대칭키를 도출하는 키 합의 알고리즘.
- **Discrete Logarithm Problem (이산대수 문제, DLP)**: $Y = g^X \bmod p$에서 $p, g, Y$가 주어졌을 때 지수 $X$를 역산하는 것이 수학적으로 불가능한 난제.

</details>

- 정의/개념: 공개값 교환으로 **공유 비밀**을 도출하는 키 합의
- 배경/필요성: 공용망에서 **대칭키 직접 배송은 도청 위험**

#### 한줄 요약
- 이산대수 난제와 공개값 교환을 통해 비밀키 전송 없이 안전한 대칭 세션키를 양단에서 합의한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ECDHE (Elliptic Curve DHE)**: 유한체 지수 연산 대신 타원곡선 스칼라 곱셈($Q = d \cdot G$)을 사용하여 256비트 키로 초고속 키 합의를 수행하는 현대 표준.
- **MITM Vulnerability (중간자 취약점)**: DH 자체에는 인증(Authentication) 메커니즘이 없어 단독 사용 시 중간자 공격에 노출되므로 전자서명 결합이 필수적인 특성.

</details>

- 비밀값을 보내지 않는 **공개값 기반 키 합의**
- 임시 키 폐기 시 **순방향 비밀성** 제공
- **ECDHE·X25519** 기반 작은 키와 효율적 연산

#### 한줄 요약
- 키 직접 전송 배제, ECDHE 기반 순방향 비밀성(PFS), 타원곡선 초고속 최적화를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Domain Parameters ($p, g$)**: 유한체 모듈러 연산의 기준이 되는 2048비트 이상 안전한 소수($p$)와 원시근 생성원($g$).

</details>

```text
Diffie-Hellman
|-- Domain Parameters
|-- Ephemeral Private Values
|-- Public Values
|-- Signature Engine
`-- HKDF Module
```

선의 의미: Alice와 Bob이 각각 임시 난수를 뽑아 공개값을 계산하고 전자서명을 첨부하여 상호 교환한 후 양단에서 동일한 $g^{ab} \bmod p$를 도출하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Domain Parameters** | 유한체·곡선 연산 기준 제공 |
| **Ephemeral Private Values** | 세션별 비공개 난수 제공 |
| **Public Values** | 상대와 교환할 좌표 제공 |
| **Signature Engine** | 공개값과 신원 결합 |
| **HKDF Module** | 공유 비밀에서 세션키 도출 |

#### 한줄 요약
- 도메인 매개변수($p, g$), 임시 개인값($a, b$), 교환 공개값($A, B$), 전자서명 엔진, HKDF 모듈이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Curve25519 (X25519, RFC 7748)**: 몽고메리 곡선 상에서 타이밍 부채널 공격에 면역이며 극도로 빠른 스칼라 곱셈 연산을 제공하는 표준 타원곡선.

</details>

```text
ECDHE 타원곡선 파라미터 합의, 좌표 연산 및 공유 비밀 도출 파이프라인
        │
   1. [곡선 파라미터 합의]
        │
   2. [임시 개인값 생성]
        │
   3. [공개 좌표 산출]
        │
   4. [서명된 공개 좌표 교환]
        │
   ▼
   5. [공유 비밀 및 세션키 도출]
```

- 1. 곡선 파라미터 합의
- 2. 임시 개인값 생성
- 3. 공개 좌표 산출
- 4. 서명된 공개 좌표 교환
- 5. 공유 비밀 및 세션키 도출

#### 한줄 요약
- 곡선 파라미터 합의 → 임시 개인값 생성 → 공개 좌표 산출 및 서명 교환 → 스칼라 곱셈 → 공통 세션키 수렴 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Static DH** vs **DHE (유한체)** vs **ECDHE (타원곡선)**.

</details>

| 비교 항목 | 정적 DH (Static DH) | 임시 유한체 DH (DHE / FFDHE) | 타원곡선 임시 DH (ECDHE) |
|:---|:---|:---|:---|
| 수학적 기반 | 유한체 DLP | 유한체 DLP | 타원곡선 ECDLP |
| 개인값 수명 | 장기 재사용 | 세션별 생성·폐기 | 세션별 생성·폐기 |
| 순방향 비밀성 | 미지원 | 임시 키 폐기 시 지원 | 임시 키 폐기 시 지원 |
| 키 크기·연산 | 장기 유한체 키 | 큰 유한체 매개변수 | 작은 곡선 키 |
| 적용 | 레거시 환경 | **RFC 7919 FFDHE** | **TLS 1.3 ECDHE** |

#### 한줄 요약
- 정적 DH는 PFS 미지원으로 폐기되었으며, DHE는 연산이 무겁고, ECDHE(X25519)가 현대 초고속 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Logjam Attack**: 1024비트 이하의 취약한 공용 소수 매개변수를 사용하는 DH 서버에 대해 사전 연산 테이블로 실시간 이산대수를 해독하는 공격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 인증 없는 공개값의 **MITM** | PKI 기반 **서명 검증** | 공개값과 신원 결합 |
| 약한 DH 그룹의 **Logjam** | RFC 7919 FFDHE 또는 **X25519** | 검증된 매개변수 사용 |
| 비표준 곡선의 **Invalid Curve** | **P-256·X25519** 제한 | 곡선 입력 위험 완화 |
| **SNDL 양자 위협** | ECDHE와 **ML-KEM 하이브리드** | 고전·PQC 위험 분산 |

#### 한줄 요약
- PKI 서명으로 MITM을 방어하고, RFC 7919/X25519로 Logjam을 차단하며, 표준 곡선으로 파라미터 변조를 방지한다.

## Ⅶ. 결론

- 현대 세션은 **인증 ECDHE**, 양자 전환은 **ML-KEM 결합**

#### 한줄 요약
- 디피-헬만 키 교환은 ECDHE와 PKI 전자서명 및 PQC 하이브리드를 결합하여 순방향 비밀성이 보장된 안전한 키 합의를 실현하는 암호 기술이다.
