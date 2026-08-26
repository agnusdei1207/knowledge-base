---
sidebar:
  order: 12
  label: "012. 양자내성암호 PQC"
  badge:
    text: "기출 · 85%"
    variant: note
title: "양자 컴퓨터 저항성 공개키 암호 표준 : PQC"
date: "2026-08-26T14:25:33+09:00"
tags:
  - "notes-security"
weight: 12
extra:
  question_no: "12"
  source_status: "기출"
  source_history: "126회, 129회, 135회"
  priority: 85
  priority_note: "Shor/Grover 알고리즘 위협, NIST FIPS 표준(ML-KEM/ML-DSA/SLH-DSA), SNDL 공격 방어 및 CBOM/Crypto-Agility"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **PQC (Post-Quantum Cryptography)**: 대규모 양자컴퓨터의 쇼어 알고리즘 공격에도 해독되지 않는 격자/해시 기반 수학적 난제의 차세대 공개키 암호.
- **Shor Algorithm (쇼어 알고리즘)**: 양자 푸리에 변환으로 소인수분해와 이산대수를 다항식 시간 내에 풀어 RSA/ECC를 붕괴시키는 양자 알고리즘.

</details>

- 정의/개념: 격자·해시 난제의 **ML-KEM·ML-DSA** 공개키 암호
- 배경/필요성: Shor 알고리즘으로 **RSA·ECC 붕괴와 SNDL 위협** 발생

#### 한줄 요약
- 격자 및 해시 수학적 난제를 통해 양자컴퓨터 환경에서도 안전한 키 교환과 전자서명을 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **MLWE (Module Learning With Errors)**: 다항식 환 상에서 노이즈가 더해진 연립일차방정식을 역산하기 불가능하다는 PQC의 핵심 수학적 난제.
- **Crypto-Agility (암호 민첩성)**: 암호 알고리즘 교체 시 비즈니스 애플리케이션 코드를 수정하지 않고 설정 변경만으로 핫스왑할 수 있는 아키텍처.

</details>

- **MLWE 격자 난제**: Shor 알고리즘의 역산 공격 저항
- **FIPS 203·204·205**: KEM과 서명 표준화
- **하이브리드 KEM**: 현재 통신의 SNDL 위협 완화

#### 한줄 요약
- 양자 공격 면역, NIST 공식 표준화(FIPS 203/204/205), SNDL 위협 선제 차단을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CBOM (Cryptography Bill of Materials)**: 인프라 및 소프트웨어 내에 사용된 모든 암호 알고리즘, 키 길이, 인증서 자산을 목록화한 암호 명세서.

</details>

```text
[PQC 전환 정적 구성]
|-- 암호 자산 대장
|-- 암호 민첩성
|-- ML-KEM
|-- ML-DSA
`-- SLH-DSA
```

선의 의미: CBOM 분석을 통해 암호 민첩성 정책을 수립하고 키 교환(ML-KEM)과 전자서명(ML-DSA/SLH-DSA)으로 영역을 나누어 PQC 전환을 수행하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 암호 자산 대장 | **RSA·ECC 의존성·위험 목록화** | CycloneDX CBOM |
| 암호 민첩성 | **설정 기반 알고리즘 교체** | RFC 9180 HPKE |
| ML-KEM | **MLWE 기반 키 캡슐화** | FIPS 203 |
| ML-DSA | **격자 기반 전자서명** | FIPS 204 |
| SLH-DSA | **해시 기반 백업 서명** | FIPS 205 |

#### 한줄 요약
- CBOM 자산 대장, 암호 민첩성 인터페이스, ML-KEM 키 교환, ML-DSA/SLH-DSA 전자서명이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **ML-KEM Decapsulation (격자 디캡슐화)**: 수신자가 자신의 비밀 격자 벡터($sk$)를 곱하여 암호문에 주입된 오차를 상쇄시키고 원본 공유 비밀을 복구하는 연산.

</details>

```text
키 교환 요청
    |
1. 격자 키 쌍 생성
    |
2. KEM 캡슐화
    |
3. 암호문 전송
    |
4. KEM 디캡슐화
    |
5. 대칭 통신 개시
    |
보안 세션
```

- 1. 격자 키 쌍 생성
- 2. KEM 캡슐화
- 3. 암호문 전송
- 4. KEM 디캡슐화
- 5. 대칭 통신 개시

#### 한줄 요약
- 격자 키 쌍 생성 → KEM 캡슐화 전송 → 격자 개인키 디캡슐화 → 공유 비밀 복구 → 대칭키 통신 전환 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **FIPS 203 (ML-KEM)** vs **FIPS 204 (ML-DSA)** vs **FIPS 205 (SLH-DSA)**.

</details>

| NIST 표준 | FIPS 203 (ML-KEM) | FIPS 204 (ML-DSA) | FIPS 205 (SLH-DSA) |
|:---|:---|:---|:---|
| 원천 알고리즘 | **Kyber** | **Dilithium** | **SPHINCS+** |
| 수학적 난제 | **MLWE** | **MLWE·MSIS** | **상태 비저장 해시** |
| 주요 암호 용도 | **KEM** | **범용 서명** | **백업 서명** |
| 공개키 크기 | **1,184바이트** | **1,952바이트** | **64바이트** |
| 암호문/서명 크기 | **1,088바이트** | **3,293바이트** | **17,088바이트** |
| 핵심 장점 및 적용 | **TLS 키 교환** | **인증서·코드 서명** | **격자 붕괴 대비** |

#### 한줄 요약
- ML-KEM은 TLS 키 교환용, ML-DSA는 범용 서명용, SLH-DSA는 격자 난제 붕괴에 대비한 해시 기반 백업용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **PQC Packet Fragmentation**: PQC 키와 서명 크기(수 KB)가 RSA 대비 5~10배 증가하여 네트워크 MTU(1500B)를 초과함으로써 발생하는 패킷 드롭 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| SNDL로 장기 기밀 사후 해독 | **X25519·ML-KEM 하이브리드** | 장기 기밀성 확보 |
| PQC 크기로 MTU·단편화 증가 | **ML-KEM·MSS·QUIC 최적화** | 패킷 드롭 완화 |
| 암호 자산 미파악으로 전환 지연 | **CBOM·HPKE 추상화** | 알고리즘 교체 가속 |
| Grover로 대칭키 강도 저하 | **AES-256·SHA-384/512** | 128비트 이상 강도 |

#### 한줄 요약
- 하이브리드 KEM으로 SNDL을 방어하고, MSS 튜닝으로 단편화를 방지하며, CBOM/추상화로 전환을 완성한다.

## Ⅶ. 결론

- SNDL 구간은 **하이브리드 ML-KEM**, 서명은 **ML-DSA·SLH-DSA** 선택

#### 한줄 요약
- PQC는 NIST 표준 ML-KEM/ML-DSA와 하이브리드 전환 및 CBOM/암호 민첩성을 결합하여 양자 안전 인프라를 실현하는 차세대 공개키 암호 체계다.
