---
sidebar:
  order: 2
  label: "002. 비대칭 암호화 (Asymmetric Encryption)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "비대칭 암호화 (Asymmetric Encryption)"
date: "2026-08-13T18:43:10+09:00"
tags:
  - "notes-security"
weight: 2
extra:
  question_no: "002"
  source_status: "기출"
  source_history: "122회"
  priority: 50
  priority_note: "122회 기출이며 PKI•PQC 비교의 기반으로 재사용됨"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **비대칭키 암호(Asymmetric Key Cryptography)**: 공개 키와 개인키라는 수치적으로 연관된 쌍을 사용하여 암호화와 복호화를 분리하는 기법.
- **키 설정(Key Establishment)**: 통신 당사자 간 대칭 암호화에 사용할 공유 비밀 또는 세션키를 안전하게 합의/생성하는 과정.
- **전자서명(Digital Signature)**: 개인키로 데이터에 서명하여 송신자 출처 부인방지 및 무결성을 증명하는 메커니즘.
- **사전 안전 공유 한계(Pre-shared Key Distribution Limit)**: 대칭키 암호 방식에서 키 수량의 폭발적 증가 및 안전한 사전 전달의 어려움.

</details>

- 정의/개념: **공개키•개인키** 쌍으로 키 설정과 **전자서명**을 제공하는 암호 기술
- 배경/필요성: 대칭키에는 **사전 안전 공유 한계**와 키 수 증가 문제가 있다.

#### 한줄 요약

- 키 쌍으로 **키 분배**를 확장하고 **PKI**로 공개키 위조 방지
## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **공개키(Public Key)**: 암호화 또는 서명 검증을 위해 누구에게나 자유롭게 공개 및 배포되는 키.
- **개인키(Private Key)**: 복호화 또는 서명 생성에 사용되며 소유자만 엄격히 비밀로 보관해야 하는 키.
- **인증서(Public Key Certificate)**: 공개키, 소유자 정보, 유효기간 등을 인증기관(CA)의 디지털 서명으로 결합한 전자문서.

</details>

- **키 분리 아키텍처**: 개방형 **공개키(Public Key)** 배포와 폐쇄형 **개인키(Private Key)** 격리 관리의 이원화 구조
- **다목적 암호 연산**: 단일 키 쌍 기반의 암호화(키 설정) 및 부인방지(전자서명) 메커니즘 동시 지원
- **신뢰 체인(Trust Chain)**: **인증서(Public Key Certificate)** 기반의 공개키 소유자 무결성 및 신원 검증 보장

#### 한줄 요약

- 배포된 공개키 무결성 담보를 위한 공인 인증기관(CA) 서명 및 인증서 유효성 검증 절차 필수 적용
## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **공개키 기반구조(Public Key Infrastructure, PKI)**: 인증서 발급, 검증, 폐지 등을 통해 공개키의 신뢰성을 보장하는 신뢰 체계.
- **하드웨어 보안 모듈(Hardware Security Module, HSM)**: 개인키의 외부 유출 없이 내부에 격리하여 암호 연산을 수행하는 보안 전용 하드웨어.
- **키 생성기(Key Pair Generator)**: 수학적 의존성을 가진 공개키 및 개인키 쌍을 안전하게 생성하는 모듈.
- **공개키•인증서 저장소(Public Key Repository)**: 공개키와 소유자 신원, 인증서 유효성을 배포 및 관리하는 저장소.
- **개인키 보호 모듈(Private Key Protection Module)**: 개인키 추출을 금지하고 암호화/서명 연산만 허용하는 보호 장치.
- **키 설정•서명 모듈(Key Establishment & Signature Module)**: 세션키 합의와 전자서명의 생성 및 검증을 담당하는 연산부.

</details>

```text
비대칭 암호 구조
├─ 키 생성기
├─ 공개키•인증서 저장소
├─ 개인키 보호 모듈
└─ 키 설정•서명 모듈
```

가지의 의미: 키 생성, 공개, 보호, 암호 연산 책임을 명확히 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| 키 생성기 | **공개키•개인키 쌍** 생성 |
| 공개키•인증서 저장소 | **공개키 소유자•유효기간** 제공 |
| 개인키 보호 모듈 | **HSM** 기반 개인키 비반출 암호 연산 |
| 키 설정•서명 모듈 | **공유 비밀•전자서명** 생성•검증 |


#### 한줄 요약

- 공개키는 **인증서**로 배포하고 개인키는 **HSM**에 격리
## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **키 캡슐화 메커니즘(Key Encapsulation Mechanism, KEM)**: 수신자의 공개키로 세션키를 암호화(캡슐화)하여 전달하고 개인키로 복구하는 기술.
- **폐기 상태 검증(Revocation Status Verification)**: 인증서가 유효기간 내에 존재하더라도 효력이 정지 또는 폐기되었는지 검증하는 절차.
- **공개•개인키 쌍 생성(Key Pair Generation)**: 공개키 배포와 개인키 격리 보관을 전제로 키 쌍을 발급하는 단계.
- **공개키•인증서 게시(Certificate Publishing)**: 검증된 공개키와 신원 정보를 저장소에 배포하는 단계.
- **인증서•폐기 상태 검증(Certificate & Revocation Verification)**: 서명 무결성, 유효기간 및 폐기 목록(CRL/OCSP)을 대조하는 단계.
- **공유 비밀 캡슐화(Shared Secret Encapsulation)**: 검증된 공개키를 사용하여 난수 기반 공유 비밀과 캡슐화 암호문을 생성하는 과정.
- **공유 비밀 복구(Shared Secret Decapsulation)**: 수신 측 개인키로 캡슐 암호문에서 동일 세션키를 도출하는 과정.

</details>

```text
1. 공개•개인키 쌍 생성
        │
        ▼
2. 공개키•인증서 게시
        │
        └── 인증서•폐기 상태 조회
                    │
                    ▼
3. 인증서•폐기 상태 검증
        ├─ 실패: 키 설정 중단
        └─ 성공
              │
              ▼
     4. 공유 비밀 캡슐화
              │
              └── 캡슐화 암호문 전달
                          │
                          ▼
                  5. 공유 비밀 복구
```

### 동작 원리

1. **공개•개인키 쌍 생성**: 공개키 배포와 개인키 격리를 위한 키 쌍 생성
2. **공개키•인증서 게시**: **PKI**에 공개키와 신원 인증서 게시
3. **인증서•폐기 상태 검증**: 서명•유효기간과 **CRL•OCSP** 상태 검증
4. **공유 비밀 캡슐화**: 검증된 공개키로 **KEM** 공유 비밀 캡슐화
5. **공유 비밀 복구**: 수신자 개인키로 동일한 **세션키** 복구


#### 한줄 요약

- **인증서•폐기 상태** 검증 뒤 공유 비밀을 설정해 **MITM** 차단
## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **최적 비대칭 암호 패딩(Optimal Asymmetric Encryption Padding, OAEP)**: RSA 암호화 시 무작위 패딩을 결합하여 결정론적 패턴 노출을 차단함.
- **임시 타원곡선 디피-헬먼(Elliptic Curve Diffie-Hellman Ephemeral, ECDHE)**: 세션마다 일회성 키 쌍을 생성하여 순방향 비밀성(PFS)을 제공하는 합의 방식.
- **모듈 격자 기반 키 캡슐화 메커니즘(Module-Lattice-Based Key-Encapsulation Mechanism, ML-KEM)**: 격자 기반 난해 수학 문제를 적용하여 양자 컴퓨터 공격을 방어하는 표준 KEM.
- **RSA-OAEP(RSA Optimal Asymmetric Encryption Padding)**: RSA 알고리즘에 OAEP 패딩을 적용하여 보안성을 향상시킨 키 설정 기술.

</details>

| 공개키 키 설정 방식 | **RSA-OAEP** | **ECDHE** | **ML-KEM** |
|:---|:---|:---|:---|
| 적용 기준 | 기존 RSA 키 전송 호환 | 순방향 비밀성이 필요한 TLS | 양자 공격 대비 키 설정 |
| 핵심 특징 | **OAEP** 무작위 패딩 | 임시 키 공유 비밀 합의 | 모듈 격자 KEM |
| 한계 | 개인키 유출 시 과거 복호화 | 인증 없으면 중간자 공격 | 키•암호문 크기 증가 |

> 요약: 호환성, 순방향 비밀성, 양자 내성 요구사항별 적절한 알고리즘 선택

#### 한줄 요약

- 호환성은 **RSA-OAEP**, 순방향 비밀성은 **ECDHE**, 양자 내성은 ML-KEM 선택
## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **순방향 비밀성(Perfect Forward Secrecy, PFS)**: 장기 개인키가 노출되더라도 과거 교환된 세션키 및 암호문이 복호화되지 않는 성질.
- **HSM 격리(HSM Isolation)**: 개인키의 외부 추출을 기계적으로 금지하고 내부 전용 암호 연산만 허용하는 보호 구조.
- **FIPS 203(FIPS 203 Standard)**: 양자 내성 키 캡슐화 알고리즘인 ML-KEM을 표준화한 NIST 표준 문서.
- **암호 민첩성(Crypto Agility)**: 보안 위협 및 표준 변경에 맞춰 암호 알고리즘을 가연성 있게 교체 및 혼용할 수 있는 아키텍처 능력.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공개키 바꿔치기 | **인증서 및 폐기 상태 검증** | 중간자 공격 차단 |
| 장기 개인키 노출 | **HSM 격리 및 ECDHE** 적용 | **순방향 비밀성** 확보 |
| 양자 위협 전환 | **FIPS 203 ML-KEM** 병행 시험 | **암호 민첩성** 확보 |

#### 한줄 요약

- **인증서 검증•HSM 격리**와 **ML-KEM** 전환 시험 적용
## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **공개키 방식 선택**: 호환성•순방향 비밀성•양자 내성에 따라 RSA-OAEP•ECDHE•ML-KEM을 결정하는 판단이다.

</details>

- 기존 호환은 **RSA-OAEP**, 순방향 비밀성은 **ECDHE**, 양자 내성은 **ML-KEM** 선택

#### 한줄 요약

- **PKI•키 수명주기**와 **양자 내성 전환**을 함께 운영
