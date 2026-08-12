---
sidebar:
  order: 1
  label: "001. 대칭 암호화 (Symmetric Encryption)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "대칭 암호화 (Symmetric Encryption)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-security"
weight: 1
extra:
  question_no: "001"
  source_status: "기출"
  source_history: "122회"
  priority: 50
  priority_note: "122회 비교 기출이나 최신 독립 재출제 축은 약함"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **대칭키 암호(Symmetric Key Cryptography)**: 송신자와 수신자가 동일한 비밀키로 평문의 암·복호화를 수행하는 기법.
- **비밀키(Secret Key)**: 암호화와 복호화에 공통으로 사용하며 외부에 노출하지 않아야 하는 핵심 통제값.
- **저비용•고속 암호화(Low-cost High-speed Encryption)**: 공개키 연산 대비 적은 계산 비용으로 대용량 평문을 신속하게 보호하는 특성.

</details>

- 정의/개념: 송수신자가 동일한 **비밀키(Secret Key)**로 평문을 변환하여 기밀성을 확보하는 **대칭키 암호(Symmetric Key Cryptography)** 방식
- 배경/필요성: 비대칭키 암호의 높은 연산 복잡도 한계를 극복하고 대용량 데이터의 실시간 전송 구간 암호화 처리 비용 절감 요구 증대

#### 한줄 요약

- 단일 비밀키 기반의 고속 암·복호화 구조이므로, 키 유출 시 시스템 전체 기밀성이 즉각 붕괴되는 치명적 단일장애점(SPOF) 내재
## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **블록 암호(Block Cipher)**: 평문을 고정 길이 블록으로 나누어 비밀키로 변환하는 암호 기술.
- **스트림 암호(Stream Cipher)**: 키스트림과 평문을 연속적으로 비트/바이트 단위 결합하는 암호화 기법.
- **연관 데이터 포함 인증 암호(Authenticated Encryption with Associated Data, AEAD)**: 평문의 기밀성과 부가 인증 데이터의 무결성을 동시에 보장함.
- **초기화 벡터(Initialization Vector, IV)**: 동일 키 사용 시에도 암호문 난수성을 보장하기 위한 초기화 난수값.
- **논스(Number Used Once, Nonce)**: 특정 키 범위 내에서 재사용을 금지하는 일회성 입력값.

</details>

![대칭키 길이에 따라 지수적으로 증가하는 전수조사 시간](/study/diagrams/symmetric-key-search.svg)

> 요약: 키 1비트 증가 시 전수조사 연산량 2배 증가

- **대칭키 암호(Symmetric Cipher)**: 단일 비밀키 기반 고속 연산으로 대규모 데이터 보호에 최적화
- **블록/스트림 암호(Block/Stream Cipher)**: 데이터 크기와 처리 방식(블록 단위 분할 vs 연속 비트열 결합)에 따른 유연한 운용 지원
- **AEAD(Authenticated Encryption)**: IV와 논스(Nonce) 연계로 평문 기밀성과 부가 데이터 무결성을 동시 검증하여 위변조 원천 차단

#### 한줄 요약

- 강력한 암호 알고리즘이라도 동일 키와 논스 재사용 시 암호문 규칙이 노출되므로, 엄격한 논스 유일성 통제 필수
## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **부가 인증 데이터(Additional Authenticated Data, AAD)**: 암호화하지 않지만 인증 태그 계산에 포함하여 무결성을 검증하는 데이터.
- **인증 태그(Authentication Tag)**: 암호문과 AAD의 변조 여부를 수신 측에서 검증하기 위한 데이터인증값.
- **키 관리 시스템(Key Management System, KMS)**: 암호키의 생성•보관•배포•교체•폐기를 수명주기 전반에서 통제하는 관리 체계.

</details>

```text
대칭 암호 구조
├─ 응용
├─ AEAD 암호 모듈
└─ 키 관리 시스템
```

가지의 의미: 데이터 처리, 암호 연산, 키 통제 책임을 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| 응용 | 평문•**AAD**•암호화 정책 전달 |
| AEAD 암호 모듈 | 암호문•**인증 태그** 생성•검증 수행 |
| 키 관리 시스템 | **KMS**가 비밀키 수명주기•접근권한 통제 |


#### 한줄 요약

- 응용 계층의 키 직접 보관을 배제하고 KMS 기반 키 위임과 암호 모듈의 암호문·MAC 동시 생성 구조 적용
## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **키 핸들(Key Handle)**: 원문 키를 외부에 노출하지 않고 암호 모듈이 허가된 키를 사용하게 하는 참조값.
- **AEAD 암호•태그 생성(AEAD Encryption and Tag Generation)**: 평문 암호화와 동시에 AAD 기반 무결성 인증 태그를 일괄 생성하는 연산 과정.
- **인증 후 복호문 공개(Decrypt After Verification)**: 태그 검증에 성공한 경우에만 평문을 응용에 전달하는 보안 원칙.
- **키•논스 할당(Key and Nonce Allocation)**: 용도별 비밀키와 키마다 유일한 논스를 생성 및 배정하는 단계.
- **키 핸들 전달(Key Handle Passing)**: 원문 키 노출 없이 암호 모듈에 키 참조와 권한을 제공하는 처리.
- **인증 태그 검증(Authentication Tag Verification)**: 수신 암호문과 AAD로 재계산한 태그의 일치 여부를 검증하여 변조 차단.

</details>

```text
암호화 요청
        │
        ▼
1. 키•논스 할당
        │
        ▼
2. 키 핸들 전달
        │
        ▼
3. AEAD 암호•태그 생성
        │
        └── 암호문•태그 전송
                    │
                    ▼
4. 인증 태그 검증
        ├─ 실패: 평문 폐기
        └─ 성공: 검증된 평문 반환
```

### 동작 원리

1. **키•논스 할당**: 용도별 비밀키 및 유일 논스 배정 수행
2. **키 핸들 전달**: **키 핸들** 기반 참조 및 접근 권한 전달
3. **AEAD 암호•태그 생성**: 평문 및 AAD 기반 인증 태그 일괄 생성
4. **인증 태그 검증**: 인증 태그 검증 성공 시에만 **인증 후 복호문 공개** 적용


#### 한줄 요약

- 암호문 복호화 전 인증 태그(MAC) 검증을 선행하여, 위변조된 데이터의 복호화 연산 자체를 차단하는 검증 후 복호화 원칙 준수
## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **고급 암호화 표준(Advanced Encryption Standard, AES)**: 128비트 블록과 128/192/256비트 키를 사용하는 대표적 블록 암호 표준.
- **갈루아/카운터 모드(Galois/Counter Mode, GCM)**: 카운터 암호화와 갈루아 인증을 결합한 병렬 처리 가능 AEAD 운용 모드.
- **AES-GCM(AES Galois/Counter Mode)**: AES 블록 암호에 GCM을 적용한 고속 인증 암호 방식.
- **ChaCha20-Poly1305(ChaCha20-Poly1305 AEAD)**: ChaCha20 스트림 암호와 Poly1305 인증자를 결합한 고효율 AEAD 방식.
- **배타적 논리합-암호화-배타적 논리합(XOR-Encrypt-XOR, XEX)**: 블록 위치를 반영하는 조정값 기반 암호 구조.
- **조정 코드북 모드와 암호문 훔치기(XEX-based Tweaked-codebook mode with Ciphertext Stealing, XTS)**: 저장장치 블록 위치별로 독자적 변환을 적용하는 모드.
- **AES-XTS(AES XEX-based Tweaked-codebook mode with Ciphertext Stealing)**: AES에 XTS를 적용한 디스크 암호화 표준.

</details>

| 대칭 암호 방식 | **AES-GCM** | **ChaCha20-Poly1305** | **AES-XTS** |
|:---|:---|:---|:---|
| 적용 기준 | AES 가속 통신•저장 데이터 | AES 가속 없는 통신 환경 | 디스크 섹터 암호화 |
| 핵심 특징 | **AES**와 **GCM** 기반 AEAD | 스트림 기반 AEAD | **XEX** 기반 **XTS** 적용 |
| 한계 | 논스 재사용 시 기밀성 훼손 | 논스 재사용 시 기밀성 훼손 | 무결성 별도 통제 |

> 요약: 통신 영역은 AEAD, 디스크 섹터 영역은 XTS 선택

#### 한줄 요약

- 네트워크 통신은 위조 방지를 포함한 AEAD 모드를, 디스크 저장은 섹터별 기밀성을 위한 XTS 모드를 적용하는 등 보호 대상 맞춤형 운용 전략 필수
## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **연방 정보 처리 표준 197(Federal Information Processing Standards 197, FIPS 197)**: AES의 블록 길이와 키 연산 규격을 명시한 정부 표준.
- **NIST SP 800-38D(NIST Special Publication 800-38D)**: AES-GCM의 인증 암호화 동작과 논스 조건을 정의한 기술 지침.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 같은 키의 **논스** 재사용 | 키별 논스 유일성 강제 | 평문•인증키 노출 방지 |
| 암호문 변조 뒤 평문 사용 | **인증 후 복호문 공개** | 위조 자료 처리 차단 |
| 알고리즘 구현 간 불일치 | **FIPS 197**•**SP 800-38D** 시험 | 암호 상호운용 확보 |

#### 한줄 요약

- 용도별 독립된 키와 논스 공간 할당 및 인증 태그 검증 성공 시에만 평문을 반환하는 무결성 중심 암호 통제 구현
## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **보호 대상별 암호 선택(Target-specific Cipher Selection)**: 통신 데이터에는 무결성을 포함한 AEAD를, 디스크 섹터에는 위치별 기밀성을 제공하는 AES-XTS를 적용하는 설계 기준.

</details>

- 환경 특성을 반영하여 통신 구간은 **AEAD**, 저장 매체는 **AES-XTS**를 선택하는 **보호 대상별 암호 선택** 아키텍처 수립

#### 한줄 요약

- 단순 알고리즘 선정을 넘어, 보호 환경에 최적화된 운용 모드 적용 및 논스 유일성 등 수명주기 전반의 엄격한 키 관리 체계 확립 필수
