---
sidebar:
  order: 6
  label: "006. 전자 서명"
  badge:
    text: "미출 · 50%"
    variant: note
title: "디지털 신원 인증 및 부인방지 : 전자서명"
date: "2026-08-26T14:30:29+09:00"
tags:
  - "notes-security"
weight: 6
extra:
  question_no: "6"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "서명 생성(개인키) 및 검증(공개키), 3대 보안 속성(무결성, 인증, 부인방지), RSA-PSS/ECDSA/Ed25519, PQC ML-DSA"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Digital Signature (전자서명)**: 메시지 해시값을 송신자의 개인키로 암호화하여 작성자 신원과 무결성을 증명하는 기술.
- **Non-Repudiation (부인방지)**: 소유자만의 개인키로 서명되었음이 증명되어 사후에 송신 사실을 부인할 수 없도록 강제하는 법적·기술적 속성.

</details>

- 정의/개념: 개인키 서명으로 **무결성·출처 인증·부인방지** 제공
- 배경/필요성: 단순 해시만으로는 **작성자와 해시값 출처 증명 불가**

#### 한줄 요약
- 개인키 서명과 공개키 검증을 통해 전자문서의 무결성, 인증, 부인방지를 보증한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Ed25519 (EdDSA, RFC 8032)**: Curve25519 기반의 결정론적 전자서명으로, 난수 재사용 취약점을 원천 제거하고 64바이트 초소형 서명을 제공하는 현대 표준.
- **TSA (Time Stamping Authority, RFC 3161)**: 전자문서가 특정 시점에 확실히 존재했음을 공인 시각 인증서로 증명하는 신뢰 기관.

</details>

- **무결성·출처 인증·부인방지** 보안 속성
- RFC 6979·EdDSA 기반 **결정론적 서명**
- TSA와 검증 자료를 보존하는 **LTV** 지원

#### 한줄 요약
- 3대 보안 속성 보증, 결정론적 서명을 통한 개인키 보호, TSA 결합 장기 검증(LTV)을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Canonicalization (C14N, 문서 정규화)**: XML/JSON/PDF의 공백, 인코딩, 줄바꿈을 정형화하여 동일한 해시값이 산출되도록 보장하는 전처리.

</details>

```text
Digital Signature
|-- Canonicalization Module
|-- Hash Engine
|-- HSM Signature Engine
|-- Certificate Repository
`-- TSA
```

선의 의미: 송신자가 정규화된 문서 해시를 개인키로 서명하여 전송하고 수신자가 공개키로 복호화한 해시값과 원문 해시값을 비교 판정하는 구조

| 구성요소 | 책임 |
|:---|:---|
| **Canonicalization Module** | 일관된 해시 입력 생성 |
| **Hash Engine** | 문서 다이제스트 생성 |
| **HSM Signature Engine** | 개인키 내부 서명 연산 |
| **Certificate Repository** | 인증서·CRL·OCSP 제공 |
| **TSA** | 신뢰 시각 토큰 발급 |

#### 한줄 요약
- 정규화 모듈, 해시 엔진, HSM 서명 연산기, X.509 인증서, TSA 타임스탬프가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **PAdES-LTV (PDF Advanced Electronic Signatures LTV)**: PDF 문서 내에 서명 시점의 인증서 체인, OCSP 응답, TSA 토큰을 영구 포함시켜 미래에도 검증을 보장하는 포맷.

</details>

```text
전자서명 생성, TSA 결합, 패키지 전송 및 수학적 검증 파이프라인
        │
   1. [문서 정규화 및 해싱]
        │
   2. [HSM 개인키 서명]
        │
   3. [TSA 타임스탬프 결합]
        │
       [서명 패키지 전송]
        │
   ▼
   4. [인증서 경로 및 폐기 검증]
        │
   5. [공개키 서명 검증]
```

- 1. 문서 정규화 및 해싱
- 2. HSM 개인키 서명
- 3. TSA 타임스탬프 결합
- 4. 인증서 경로 및 폐기 검증
- 5. 공개키 서명 검증

#### 한줄 요약
- C14N 정규화 → 해시 추출 → HSM 개인키 서명 → X.509/OCSP 검증 → 수학적 서명 일치 판정 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **RSA-PSS** vs **ECDSA/Ed25519** vs **ML-DSA (Post-Quantum Dilithium)**.

</details>

| 비교 항목 | RSA-PSS (RFC 8017) | ECDSA / Ed25519 (RFC 8032) | ML-DSA (NIST FIPS 204) |
|:---|:---|:---|:---|
| 수학적 기반 | 소인수분해·PSS | 타원곡선 이산대수 | 모듈 격자 |
| 서명 크기 | 비교적 큼 | 작음 | 비교적 큼 |
| 구현 주의 | PSS 매개변수 | **Nonce 재사용 방지** | 큰 키·서명 처리 |
| 양자 공격 | Shor 알고리즘에 취약 | Shor 알고리즘에 취약 | **PQC** 설계 |
| 주요 적용 | 문서·코드 서명 | TLS·경량 서명 | 장기 전환 대상 |

#### 한줄 요약
- RSA-PSS는 레거시 호환, ECDSA/Ed25519는 고속 경량 표준, ML-DSA는 양자 공격 대비 차세대 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Sony PS3 Incident (ECDSA 난수 재사용 사고)**: 플레이스테이션 3 펌웨어 서명 시 난수 $k$를 고정값으로 사용하여 개인키가 대수적으로 역산 유출된 보안 사고.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| ECDSA 난수 재사용으로 **개인키 유출** | RFC 6979 또는 **Ed25519** | Nonce 결함 방지 |
| 빌드 서버의 서명키 탈취 | **HSM·다중 승인** | 키 반출·오용 제한 |
| 인증서 만료 후 장기 검증 | **TSA·PAdES-LTV** 자료 보존 | 서명 시점 증거 유지 |
| 인코딩 차이로 검증 실패 | 서명 전 **Canonicalization** | 해시 입력 통일 |

#### 한줄 요약
- RFC 6979로 개인키 유출을 막고, HSM/다중 승인으로 공급망을 방어하며, TSA/LTV로 장기 증거력을 보증한다.

## Ⅶ. 결론

- 경량 서명은 **Ed25519**, 장기 양자 대응은 **ML-DSA** 전환

#### 한줄 요약
- 전자서명은 비대칭 개인키 서명과 해시 무결성 및 TSA 타임스탬프를 결합하여 법적 부인방지와 신원 인증을 실현하는 핵심 기술이다.
