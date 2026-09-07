---
sidebar:
  order: 1
  label: "001. 대칭 암호화"
  badge:
    text: "기출 · 50%"
    variant: note
title: "고속 블록/스트림 데이터 암호화 : 대칭키 암호화"
date: "2026-09-07T14:00:00+09:00"
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

- 정의/개념: 동일 비밀키로 암호화·복호화하는 **대칭키 암호화** 방식
- 배경/필요성: 네트워크 트래픽, 클라우드 스토리지 및 대용량 데이터베이스를 암호화할 때, 복잡한 수학적 난제에 기반한 공개키(비대칭키) 암호는 데이터 크기에 비례하여 기하급수적인 CPU 연산 부하와 처리 지연을 유발하여 대용량 실시간 암호화에 부적합한 한계를 가짐에 따라, 송수신자가 동일한 비밀키(Secret Key)를 공유하고 SPN/Feistel 구조 및 CPU 하드웨어 명령어(AES-NI)를 활용하여 초고속으로 암복호화를 수행하는 대칭키 암호화(Symmetric Encryption) 기술을 도입하여 기가비트급 와이어 스피드(Wire-Speed) 암호화 성능 확보, 기밀성과 무결성을 동시 검증하는 AEAD(AES-GCM/ChaCha20-Poly1305) 기반 안전성 및 대용량 데이터 전 구간 보안을 달성할 필요

#### 한줄 요약
- 단일 비밀키와 AEAD 모드를 통해 대용량 데이터의 기밀성과 무결성을 하드웨어 가속 속도로 보장한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **SPN (Substitution-Permutation Network)**: S-Box(치환)를 통한 혼돈(Confusion)과 P-Box(순열)를 통한 확산(Diffusion)을 반복하는 블록 암호 구조.
- **AES-NI (AES New Instructions)**: x86 CPU 칩셋에 내장되어 AES 암복호화 연산을 1사이클 내외로 가속하는 하드웨어 명령어 셋.

</details>

- 공개키 암호보다 낮은 연산 비용과 높은 처리량
- **AEAD**로 기밀성과 무결성을 함께 제공
- **SPN** 구조 블록 암호(AES)를 **AES-NI**로 연산 가속

#### 한줄 요약
- 대칭키는 양단이 이미 같은 비밀을 공유하고 있다는 전제를 대가로 처리량을 얻으므로, 키 배송 문제는 스스로 풀지 못하고 공개키 계층에 위임한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Nonce (Number used once)**: 동일 키 환경에서 암호문의 무작위성을 보장하기 위해 매 암호화마다 고유하게 부여하는 96비트 일회용 난수.

</details>

```text
[대칭키 암호화 체계]
  │
  ├─ [키 및 난수 관리]
  │    ├─ Secret Key (공유 비밀키)
  │    ├─ Nonce (일회용 고유 난수)
  │    └─ KMS / HSM (키 수명주기)
  │
  └─ [AEAD 암복호화 엔진]
       ├─ 암호화 엔진 (AES-GCM)
       └─ 인증 태그 (GHASH 무결성)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| Secret Key | 암호화·복호화 공통 키 |
| **Nonce** | 키별 암호화 입력의 유일성 제공 |
| AEAD Engine | 암호문과 인증 태그 생성 |
| Authentication Tag | 암호문·AAD 무결성 검증 |
| KMS and HSM | 키 생성·보관·순환·폐기 |

#### 한줄 요약
- 비밀키 하나에 신뢰 전부가 얹히므로 보관 책임은 KMS·HSM 계층으로 옮기고, 알고리즘이 보장하지 못하는 입력 유일성은 논스 관리라는 운영 책임으로 남는다.

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
- 태그 검증을 복호화 앞에 두어 위조 패킷을 값싼 태그 비교 한 번으로 걸러내므로, 공격자가 통제하는 암호문을 복호화 경로에 태우는 비용 자체가 발생하지 않는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ARX (Add-Rotate-XOR)**: 덧셈·비트 회전·XOR 세 정수 연산만으로 라운드를 구성해 S-Box 조회 테이블 없이 캐시 타이밍 부채널을 피하고, AES 명령어가 없는 CPU에서도 소프트웨어만으로 빠르게 동작하는 스트림 암호 설계 방식.
- **XTS (XEX-based Tweaked-codebook mode with ciphertext Stealing, IEEE 1619)**: 섹터 번호를 트윅(tweak)으로 넣어 같은 평문 블록도 섹터마다 다른 암호문이 되게 하는 디스크 암호화 전용 블록 모드로, 인증 태그를 붙일 자리가 없는 고정 길이 저장 장치를 위해 무결성 검증을 포기하고 기밀성만 제공.

</details>

| 비교 항목 | AES-GCM (블록 기반 AEAD) | ChaCha20-Poly1305 (스트림 AEAD) | AES-XTS (섹터 단위 스토리지) |
|:---|:---|:---|:---|
| 암호 구조 | AES 블록 암호 | **ARX** 스트림 암호 | **XTS** 모드 블록 암호 |
| 무결성 인증 | GCM 태그 | Poly1305 태그 | 미지원 |
| 가속 특성 | AES 명령 활용 | 소프트웨어 구현에 유리 | AES 명령 활용 |
| 주요 적용 | TLS·IPsec | TLS·WireGuard | 디스크 섹터 암호화 |

#### 한줄 요약
- AES-GCM은 서버/TLS 1.3 표준, ChaCha20은 모바일/WireGuard 표준, AES-XTS는 스토리지 전용이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Nonce Reuse Catastrophe**: 동일 대칭키에서 동일 Nonce를 2회 이상 사용 시 두 암호문의 XOR 차분으로 GHASH 인증키($H$)가 노출되어 임의 위조가 가능해지는 치명적 결함.
- **XChaCha20**: 192비트 확장 논스 중 128비트를 HChaCha20에 넣어 서브키를 먼저 파생하고 나머지 64비트로 ChaCha20을 돌리는 변형으로, 논스를 난수로 뽑아도 충돌 확률이 무시할 수준이어서 카운터 동기화 없이 재사용을 피함.
- **Envelope Encryption (봉투 암호화)**: 데이터는 DEK로 암호화하고 그 DEK를 KMS 안의 KEK로 다시 암호화해 암호문 옆에 저장하는 2계층 방식으로, 마스터키(KEK)가 KMS/HSM 밖으로 나오지 않게 하면서 DEK 교체만으로 재암호화 비용을 줄임.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 논스 재사용에 따른 **Nonce Reuse Catastrophe** | 단조 카운터 또는 **XChaCha20** 확장 논스 | 키별 논스 중복 방지 |
| 태그 검증 전 평문 사용 | **Verify-then-Decrypt** 강제 | 위조 평문 처리 방지 |
| 소스에 마스터키 하드코딩 | KMS 기반 **Envelope Encryption** | DEK·KEK 분리 관리 |
| 양자 탐색으로 키 강도 저하 | AES-256 적용 검토 | Grover 공격 여유 확보 |

#### 한줄 요약
- 네 대책 모두 알고리즘이 아니라 운영이 깨뜨리는 지점을 막는 것이므로, 대칭 암호의 실제 약점은 AES 자체가 아니라 논스와 키를 다루는 손에 있다.

## Ⅶ. 결론

- 초고속 하드웨어 가속(AES-NI)을 바탕으로 전 세계 인터넷 통신(TLS 1.3/IPsec) 및 스토리지(FDE/SED)의 대용량 데이터 기밀성을 지탱하는 현대 암호학의 가장 기본적이면서도 대체 불가능한 고속 암호화 표준 기술로 확고히 안착하였으며, 양자 컴퓨터 그로버(Grover) 알고리즘에 대응하는 256비트 키 확장(AES-256)으로 진화하는 가운데, 실무 대칭 암호 시스템 구축 시에는 동일 Nonce 재사용으로 인한 인증키 노출(Catastrophe)을 원천 방지하는 단조 증가 카운터 기반 Nonce 관리, 패딩 오라클 공격을 차단하는 Verify-then-Decrypt 원칙의 AEAD(AES-GCM / ChaCha20-Poly1305) 필수 적용, 마스터키 노출을 방지하는 KMS/HSM 기반 봉투 암호화(Envelope Encryption: KEK/DEK)를 결합하여 완벽한 데이터 암호 무결성을 완성

#### 한줄 요약
- 대칭키가 속도를, 공개키가 키 배송을 맡는 분업이 표준이므로, 키 배송 계층 없이 대칭키만으로 세운 설계는 미완성으로 본다.
