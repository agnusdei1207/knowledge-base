---
sidebar:
  order: 6
  label: "006. 전자 서명 (Digital Signature)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "전자 서명 (Digital Signature)"
date: "2026-08-13T18:45:57+09:00"
tags:
  - "notes-security"
weight: 6
extra:
  question_no: "006"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "PKI와 PQC 서명 전환을 잇는 독립 기반 주제임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **전자서명(Digital Signature)**: 개인키로 서명값을 생성하고 공개키로 메시지 무결성 및 송신자 신원을 검증하는 비대칭키 기반 기술.
- **승인 주체•변경 여부 확인 한계(Limits of Unsigned Document Assurance)**: 서명이 없는 전자문서에서 작성자 신원 인증 및 사후 위변조 여부를 증명하기 어려운 한계.

</details>

- 정의/개념: 개인키로 생성하고 공개키로 검증하는 **전자서명**
- 배경/필요성: 무서명 문서에는 **승인 주체•변경 여부 확인 한계**가 있다.

#### 한줄 요약

- **무결성•인증•부인방지**와 **PKI 신원 증명** 제공

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **서명 생성(Signature Generation)**: 원본 문서의 해시 다이제스트를 개인키로 암호화/연산하여 디지털 서명값을 도출하는 절차.
- **서명 검증(Signature Verification)**: 공개키를 사용하여 서명값과 원본 문서 다이제스트의 연관 일치 여부를 판정하는 연산.
- **무결성(Integrity)**: 서명 생성 시점 이후 메시지가 인가되지 않은 방법으로 변경되지 않았음을 보장하는 특성.
- **인증(Authentication)**: 검증된 공개키의 실제 소유자가 해당 메시지를 서명했음을 입증하는 성질.
- **부인방지(Non-Repudiation)**: 서명자 신원, 키 통제, 타임스탬프 증거를 결합하여 서명 사실의 사후 부인을 법적으로 차단함.
- **정규화(Canonicalization)**: 동일한 의미의 문서가 유일한 바이트열로 변환되도록 공백, 인코딩, 필드 순서를 규격화하는 처리.

</details>

- 개인키 기반 **서명 생성**과 공개키 기반 **서명 검증**의 비대칭 구조
- **무결성**, **인증**, **부인방지** 보장 (원문 기밀성 미제공)
- 문서 서명 전 포맷 유일성을 확보하는 **정규화** 처리 필수

#### 한줄 요약

- 서명 생성과 검증의 비대칭 구조로 무결성·인증·부인방지를 보장하며, 데이터 유일성 확보를 위한 문서 정규화(Canonicalization) 처리 필수

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **하드웨어 보안 모듈(Hardware Security Module, HSM)**: 개인키 외부 유출 없이 내부에 격리하여 전자서명 연산을 고속으로 수행하는 전용 장비.
- **공개키 인증서(Public Key Certificate)**: 공개키와 소유자 신원을 인증기관(CA)의 디지털 서명으로 결합한 표준 전자문서.
- **정규화(Canonicalization, C14N)**: 이종 시스템 간 서명 대조 시 동일 바이트열을 보장하는 표준화 과정.

</details>

```text
전자서명 구조
├─ 문서 정규화
├─ HSM 서명 연산
├─ 인증서·신뢰 저장소
└─ 서명 검증
```

가지의 의미: 문서 규격화, 서명 생성, 신뢰성 제공, 서명 검증 책임을 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| 문서 정규화 | **문서 바이트열·서명 문맥** 확정 |
| HSM 서명 연산 | **HSM** 기반 개인키 비반출 서명 생성 |
| 인증서·신뢰 저장소 | **인증서 주체·유효 상태** 제공 |
| 서명 검증 | **서명·다이제스트·신뢰 경로** 검증 |


#### 한줄 요약

- **문서 정규화·HSM 서명·PKI 검증**의 통합 구조

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **서명 문맥(Signature Context)**: 서명 목적, 타임스탬프, 업무 범위를 서명 연산에 바인딩하여 재사용 공격을 방어하는 파라미터.
- **인증서 폐기 검증(Certificate Revocation Verification)**: 서명 시점 기준 인증서가 효력 정지 또는 폐기 상태인지를 대조하는 검증.
- **권한•서명 문맥 확인(Authorization & Context Check)**: 서명 주체가 해당 문서 및 용도에 적합한 인가 권한을 보유했는지 파악하는 단계.
- **서명값 생성(Signature Generation Stage)**: HSM 내부의 격리된 개인키를 사용하여 정규화 해시값 기반 서명을 도출하는 단계.
- **인증서 상태 검증(Certificate Status Verification)**: 신뢰 경로, 유효기간 및 CRL/OCSP 상태를 종합 판정하는 단계.
- **다이제스트•서명 검증(Digest & Signature Verification)**: 수신된 문서 해시와 공개키 기반 서명값의 수학적 일치성을 검증하는 단계.

</details>

```text
다이제스트 서명 요청
        │
        ▼
1. 권한•서명 문맥 확인
        ├─ 실패: 서명 거부
        └─ 성공
              │
              ▼
     2. 서명값 생성
              │
              └── 문서•서명•인증서 전달
                          │
                          ▼
                  3. 인증서 상태 검증
                          ├─ 실패: 서명 무효
                          └─ 성공
                               │
                               ▼
                       4. 다이제스트•서명 검증
                               │
                               └── 서명 판정 반환
```

### 동작 원리

1. **권한•서명 문맥 확인**: 서명 목적•업무 범위와 주체 권한 검증
2. **서명값 생성**: HSM 내부 개인키로 정규화 다이제스트에 서명
3. **인증서 상태 검증**: 신뢰 경로•유효기간과 **CRL•OCSP** 검증
4. **다이제스트•서명 검증**: 문서 다이제스트와 공개키 서명의 일치 판정


#### 한줄 요약

- **권한•서명 문맥•인증서 상태•다이제스트** 순차 검증

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **확률적 서명 방식(Probabilistic Signature Scheme, PSS)**: RSA 알고리즘에 솔트 및 무작위 난수 패딩을 도입하여 동일 메시지당 매번 다른 서명을 생성하는 기술.
- **타원곡선 전자서명 알고리즘(Elliptic Curve Digital Signature Algorithm, ECDSA)**: 타원곡선 연산을 적용하여 짧은 키 길이로 높은 보안 강도를 제공하는 서명 표준.
- **모듈 격자 기반 전자서명 알고리즘(Module-Lattice-Based Digital Signature Algorithm, ML-DSA)**: 모듈 격자 문제를 사용하여 양자 컴퓨터의 해독 연산을 차단하는 표준 PQC 서명.
- **RSA-PSS(RSA Probabilistic Signature Scheme)**: 기존 RSA 서명의 결정론적 취약점을 보완한 최신 안전 규격.

</details>

| 전자서명 방식 | **RSA-PSS** | **ECDSA** | **ML-DSA** |
|:---|:---|:---|:---|
| 적용 기준 | 기존 RSA 인증서•코드 서명 | 작은 키가 필요한 인증서 | 양자 대응 신규 서명 체계 |
| 핵심 특징 | **PSS** 확률적 서명 | 작은 키의 타원곡선 서명 | 격자 기반 양자내성 서명 |
| 한계 | 큰 키•서명 연산 비용 | 논스 오류 시 개인키 노출 | 큰 서명•인증서 크기 |

> 요약: 기존 호환성 RSA-PSS, 모바일/IoT 경량성 ECDSA, 양자 내성 ML-DSA 선택

#### 한줄 요약

- 기존 호환은 **RSA-PSS**, 작은 키는 **ECDSA**, 양자 내성은 ML-DSA 선택

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **FIPS 186-5(FIPS 186-5 Standard)**: RSA, ECDSA 및 EdDSA 전자서명 연산과 검증 메커니즘을 정의한 미국 정부 표준.
- **FIPS 204(FIPS 204 Standard)**: 양자 내성 모듈 격자 전자서명 알고리즘(ML-DSA)을 규정한 NIST 표준.
- **타임스탬프(Time Stamp)**: 신뢰할 수 있는 시각 제공 기관(TSA)이 특정 데이터의 존재 시점을 시각 서명으로 증명하는 기술.
- **승인 산출물 통제(Approved Artifact Control)**: 무단/변조 빌드 파일에 대한 서명을 방지하기 위해 검증된 산출물에만 HSM 서명 권한을 부여하는 조치.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 기존 전자서명 | **FIPS 186-5** 준수 | 검증 알고리즘 일관화 |
| 양자내성 전환 | **FIPS 204** 기반 ML-DSA | 양자 공격 대비 |
| 서명키 유출 | **HSM 기반 승인 산출물 서명 통제** | 위조 서명 차단 |
| 장기 증거의 시각 부재 | **타임스탬프 및 폐기 정보(CRL/OCSP) 증거 보존** | 부인방지 강화 |

#### 한줄 요약

- **FIPS 186-5•204**, **HSM•타임스탬프**로 장기 증거 확보

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **장기 서명 증거(Long-Term Signature Validation Evidence)**: 서명 시점의 타임스탬프, CRL/OCSP 폐기 증거를 결합 보관하여 사후 검증을 보장하는 체계.
- **전자서명 방식 선택(Digital Signature Scheme Selection)**: 호환성, 성능, 키 크기 및 양자 내성을 종합 고려한 전자서명 규격 채택.

</details>

- 기존 호환은 **RSA-PSS**, 경량은 **ECDSA**, 양자 전환은 **ML-DSA** 선택

#### 한줄 요약

- **PKI•HSM•타임스탬프**로 장기 서명 증거 보존
