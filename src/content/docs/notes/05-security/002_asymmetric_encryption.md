---
sidebar:
  order: 2
  label: "002. 비대칭 암호화"
  badge:
    text: "기출 · 50%"
    variant: note
title: "공개키 기반 키 교환 및 전자서명 : 비대칭 암호화"
date: "2026-08-26T14:25:20+09:00"
tags:
  - "notes-security"
weight: 2
extra:
  question_no: "2"
  source_status: "기출"
  source_history: "122회"
  priority: 50
  priority_note: "공개키/개인키 분리, 수학적 일방향 난제(소인수분해/타원곡선), KEM(키 캡슐화), PFS(순방향 비밀성) 및 PKI"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Asymmetric Encryption (비대칭 암호화)**: 암호화에 사용하는 공개키와 복호화에 사용하는 개인키가 서로 다른 암호화 방식.
- **KEM (Key Encapsulation Mechanism)**: 수신자의 공개키로 대칭 세션키를 캡슐화하여 안전하게 배송하는 공개키 교환 표준.

</details>

- 정의/개념: **공개키·개인키** 쌍을 사용하는 암호 방식
- 배경/필요성: 대칭키만으로는 **사전 키 배송·서명 검증 제약**

#### 한줄 요약
- 공개키와 개인키의 비대칭 쌍을 통해 사전 비밀키 공유 없는 안전한 키 교환과 전자서명을 실현한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Trapdoor One-Way Function (트랩도어 일방향 함수)**: 순방향 계산(공개키 연산)은 쉬우나 역방향 계산(개인키 없이 평문 복구)은 수학적으로 불가능한 함수.
- **PFS (Perfect Forward Secrecy, 순방향 비밀성)**: 서버의 장기 개인키가 유출되어도 과거 세션의 암호화 트래픽을 소급하여 복호화할 수 없는 속성.

</details>

- 공개키 배포로 **사전 비밀키 공유** 부담 완화
- 개인키 서명으로 **출처 인증·부인방지** 지원
- ECDHE 임시 키로 **순방향 비밀성** 제공

#### 한줄 요약
- 키 배송 문제 해결, 전자서명 부인방지, 임시 키 기반 순방향 비밀성(PFS)을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Public Key vs Private Key**: 암호화 및 서명 검증에 쓰이는 공개키와 복호화 및 서명 생성에 쓰이는 개인키.

</details>

```text
Asymmetric Cryptography
|-- Public Key
|-- Private Key
|-- CA
|-- KEM Engine
`-- Signature Engine
```

선의 의미: 송신자가 수신자의 검증된 공개키로 대칭키를 캡슐화하여 전송하고 수신자가 HSM 내부 개인키로 복호화하여 공통 세션키를 수립하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Public Key** | 암호화·서명 검증 |
| **Private Key** | 복호화·서명 생성 |
| **CA** | 공개키와 신원의 인증서 결합 |
| **KEM Engine** | 공유 비밀 캡슐화·해제 |
| **Signature Engine** | 해시 서명과 검증 |

#### 한줄 요약
- 공개키, 개인키, PKI 인증기관, KEM 엔진, 전자서명 엔진이 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **RSA-OAEP (RFC 8017)**: 평문에 랜덤 패딩과 Feistel 구조를 적용하여 동일 평문이라도 매번 다른 암호문을 생성함으로써 선택 암호문 공격을 방어하는 패딩 기법.

</details>

```text
비대칭 인증서 검증, KEM 키 캡슐화 및 대칭 통신 전환 파이프라인
        │
   1. [인증서 발급 및 게시]
        │
   2. [인증서 신뢰 검증]
        │
   3. [공유 비밀 캡슐화]
        │
       [캡슐 전송]
        │
   ▼
   4. [캡슐 해제 및 대칭 통신]
```

- 1. 인증서 발급 및 게시
- 2. 인증서 신뢰 검증
- 3. 공유 비밀 캡슐화
- 4. 캡슐 해제 및 대칭 통신

#### 한줄 요약
- 인증서 검증 → KEM 세션키 캡슐화 → 암호문 전송 → 개인키 복호화 → 대칭키 하이브리드 통신 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RSA** vs **ECC (ECDH/ECDSA)** vs **ML-KEM (Post-Quantum Kyber)**.

</details>

| 비교 항목 | RSA-OAEP / RSA-PSS | ECC (ECDH / ECDSA) | ML-KEM (Post-Quantum Kyber) |
|:---|:---|:---|:---|
| 난제 | 소인수분해 | 타원곡선 이산대수 | 모듈 격자 MLWE |
| 키·암호문 크기 | 큰 공개키 | 작은 키 | 비교적 큰 캡슐 |
| 순방향 비밀성 | 정적 키 교환은 미지원 | **ECDHE**로 지원 | 임시 KEM 운용에 좌우 |
| 양자 공격 | Shor 알고리즘에 취약 | Shor 알고리즘에 취약 | **PQC** 설계 |
| 주요 적용 | 레거시 암호·서명 | TLS·SSH·서명 | 하이브리드 키 설정 |

#### 한줄 요약
- RSA는 레거시 호환, ECC는 현대 모바일/TLS 1.3 최적화, ML-KEM은 미래 양자 공격 방어 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **SNDL (Store Now, Decrypt Later)**: 현재 암호화된 트래픽을 대규모 수집·저장해 두고 향후 양자컴퓨터로 사후 복호화하는 국가급 도청 위협.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공개키 위조로 **MITM** | PKI 체인·**OCSP Stapling** 검증 | 공개키 출처 확인 |
| 장기 개인키 유출 | 임시 **ECDHE·PFS** 적용 | 과거 세션 노출 완화 |
| **SNDL 양자 위협** | **X25519·ML-KEM 하이브리드** | 전환기 알고리즘 위험 분산 |
| 개인키 파일 유출 | **HSM** 내부 연산 | 개인키 반출 제한 |

#### 한줄 요약
- PKI 인증으로 MITM을 방어하고, ECDHE로 순방향 비밀성을 확보하며, ML-KEM 하이브리드로 양자 위협을 차단한다.

## Ⅶ. 결론

- 현재 세션은 **ECDHE**, 양자 전환은 **ML-KEM 하이브리드** 선택

#### 한줄 요약
- 비대칭 암호화는 공개키/개인키 쌍과 수학적 난제 기반으로 키 배송 문제를 해결하고 PKI 및 PQC와 결합하여 영구적 신뢰성을 제공한다.
