---
sidebar:
  order: 3
  label: "003. 하이브리드 암호 (Hybrid Cryptography)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "하이브리드 암호 (Hybrid Cryptography)"
date: "2026-08-13T18:43:10+09:00"
tags:
  - "notes-security"
weight: 3
extra:
  question_no: "003"
  source_status: "기출"
  source_history: "122회"
  priority: 30
  priority_note: "122회 기출이나 대칭•비대칭 결합 설명에 흡수됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **하이브리드 암호(Hybrid Cryptography)**: 비대칭키 암호로 임시 세션키를 안전하게 교환하고 대칭키 암호로 대용량 본문을 고속 연산하는 암호 체계.
- **키 캡슐화 메커니즘(Key Encapsulation Mechanism, KEM)**: 공개키를 사용하여 임시 세션키를 암호화(캡슐화) 및 송수신하는 방식.
- **데이터 캡슐화 메커니즘(Data Encapsulation Mechanism, DEM)**: KEM을 통해 합의된 대칭 세션키로 본문 데이터를 암호화하는 메커니즘.
- **KEM 키 설정(KEM Key Establishment)**: KEM을 기반으로 임시 공유 비밀을 생성, 캡슐화, 복구하여 대칭키를 유도하는 연산.
- **DEM 본문 보호(DEM Content Protection)**: 유도된 대칭 세션키를 활용하여 실제 메시지의 기밀성과 무결성을 보장하는 처리.
- **대용량 처리 한계(Bulk Data Encryption Limit)**: 비대칭키 암호 알고리즘의 연산 복잡성으로 대용량 본문의 직접 암호화 시 성능이 급격히 저하되는 한계.

</details>

- 정의/개념: **KEM 키 설정**과 **DEM 본문 보호**를 결합한 복합 암호 체계
- 배경/필요성: 비대칭키에는 대용량 본문의 **처리 성능 한계**가 있다.

#### 한줄 요약

- **KEM•DEM 분리**로 키 분배 안전성과 본문 처리 성능 확보

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **세션키(Session Key)**: 특정 통신 세션 동안에만 본문 암호화에 일회성으로 사용하는 대칭 암호키.
- **키 유도 함수(Key Derivation Function, KDF)**: 하나의 공유 비밀로부터 송수신 방향 및 용도에 적합한 다수의 독립 대칭키를 파생시키는 함수.

</details>

- **비용 최적화**: 고비용 공개키 연산 범위를 **KEM** 키 설정 구간으로 최소화 적용
- **하이브리드 구조**: **DEM** 메커니즘을 통한 **세션키** 기반 대규모 페이로드 고속 처리
- **키 스케줄링**: **KDF(Key Derivation Function)** 기반 송수신 방향 및 용도별 대칭키 독립적 도출

#### 한줄 요약

- 상호 인증(Authentication) 결여된 단순 키 합의는 중간자 공격(MITM)에 취약, PKI 기반 인증서 검증 결합 필수

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **키 스케줄(Key Schedule)**: 공유 비밀에서 파생된 키들을 통신 단계별, 용도별로 순차적 갱신 및 관리하는 절차.
- **연관 데이터 포함 인증 암호(Authenticated Encryption with Associated Data, AEAD)**: 암호문 기밀성과 부가 인증 데이터의 무결성을 동시에 보장하는 대칭 암호 방식.

</details>

```text
하이브리드 암호 구조
├─ 인증 모듈
├─ 키 설정 모듈
├─ KDF•키 스케줄
└─ AEAD 모듈
```

가지의 의미: 신원 인증, 키 설정, 키 파생, 본문 보호 기능을 책임 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| 인증 모듈 | **공개키 소유자•협상 기록** 검증 |
| 키 설정 모듈 | **KEM 공유 비밀** 생성 |
| KDF 및 키 스케줄 | **단계•방향별 대칭키** 분리 |
| AEAD 모듈 | **본문 암호화•인증 태그** 검증 |


#### 한줄 요약

- **KDF•키 스케줄**로 용도와 송수신 방향별 키 분리

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **협상 기록 인증(Transcript Authentication)**: 암호 세션 시작 시 교환한 알고리즘 파라미터를 전자서명에 포함시켜 조작을 검증하는 인증.
- **임시 타원곡선 디피-헬먼(Elliptic Curve Diffie-Hellman Ephemeral, ECDHE)**: 세션마다 임시 타원곡선 키를 생성하여 순방향 비밀성(PFS)을 제공하는 합의 방식.
- **인증서•협상 기록 검증(Certificate & Transcript Verification)**: 상대방 공개키 인증서 유효성과 세션 협상 무결성을 검증하는 과정.
- **ECDHE•KEM 키 설정(ECDHE/KEM Key Establishment)**: ECDHE 키 합의 또는 KEM 캡슐화를 이용해 공유 비밀을 생성하는 처리.
- **공유 비밀•방향별 키 도출(Key Derivation per Direction)**: KDF를 호출하여 송신용, 수신용 및 MAC용 키를 파생하는 처리.
- **AEAD 본문 보호(AEAD Data Protection)**: 파생된 대칭키로 실제 통신 메시지의 기밀성과 무결성을 동시 보장하는 단계.

</details>

```text
알고리즘 제안•선택•인증서 수신
        │
        ▼
1. 인증서•협상 기록 검증
        ├─ 실패: 연결 중단
        └─ 성공
              │
              ▼
     2. ECDHE•KEM 키 설정
              │
              ▼
     3. 공유 비밀•방향별 키 도출
              │
              ▼
     4. AEAD 본문 보호
              │
              └── 보호된 레코드 전송
```

### 동작 원리

1. **인증서•협상 기록 검증**: 인증서와 서명된 **협상 기록**의 무결성 검증
2. **ECDHE•KEM 키 설정**: **ECDHE** 합의 또는 KEM 캡슐화로 공유 비밀 생성
3. **공유 비밀•방향별 키 도출**: **KDF**로 송신•수신•인증 키 분리
4. **AEAD 본문 보호**: 파생 키로 본문의 **기밀성•무결성** 보호


#### 한줄 요약

- **협상 기록 인증**으로 취약 알고리즘 강제 **다운그레이드** 차단

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **순방향 비밀성(Perfect Forward Secrecy, PFS)**: 장기 개인키가 유출되더라도 과거 세션의 세션키와 암호문이 유출되지 않는 암호학적 특성.
- **RSA 키 전송(RSA Key Transport)**: 수신자의 RSA 공개키로 세션키를 암호화하여 직접 전달하는 역사가 오랜 방식.
- **양자 내성 암호(Post-Quantum Cryptography, PQC)**: 양자 컴퓨터의 쇼어 알고리즘 공격에 견디도록 수학적으로 설계된 차세대 암호.
- **PQC KEM 결합(PQC-Classical Hybrid KEM)**: 양자 위협에 대비하여 고전 암호(ECDHE)와 PQC KEM 비밀을 동시 도출 및 결합하는 방식.
- **ECDHE 기반(ECDHE-based Hybrid Encryption)**: 임시 타원곡선 키 교환을 기반으로 세션키를 안전하게 합의하는 방식.

</details>

| 하이브리드 키 설정 | **ECDHE 기반** | **RSA 키 전송** | **PQC KEM 결합** |
|:---|:---|:---|:---|
| 적용 기준 | **순방향 비밀성**이 필요한 통신 | 기존 RSA 키 전송 호환 | **PQC** 전환기 통신 |
| 핵심 특징 | 임시 키 합의 후 AEAD | RSA 공개키 세션키 암호화 | 두 비밀의 KDF 결합 |
| 한계 | 인증 없으면 중간자 공격 | 개인키 유출 시 과거 복호화 | 실패 시 자동 약화 위험 |

> 요약: 인증 여부, 과거 암호문 보호, 양자 내성 요구에 따른 적합 기술 선택

#### 한줄 요약

- PQC 전환은 **ECDHE•PQC KEM 결합**과 취약 폴백 차단

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **다운그레이드 공격(Downgrade Attack)**: 중간자가 암호 협상 과정을 조작하여 취약한 예전 암호 방식으로 강제 전환시키는 공격.
- **영역 분리(Domain Separation)**: 동일 공유 비밀에서 파생된 키들이 용도별, 방향별로 혼용되지 않도록 컨텍스트를 분리하는 규칙.
- **RFC 9180(RFC 9180 Standard)**: 하이브리드 공개키 암호(HPKE)의 KDF 영역 분리와 표준 키 스케줄을 명시한 IETF 문서.
- **하이브리드 공개키 암호(Hybrid Public Key Encryption, HPKE)**: KEM, KDF, DEM(AEAD)을 모듈화하여 단순하게 결합한 공개키 암호화 표준.
- **전송 계층 보안(Transport Layer Security, TLS)**: 네트워크 통신 시 기밀성, 무결성, 상대방 신원 인증을 제공하는 상위 보안 프로토콜.
- **RFC 9846(RFC 9846 Standard)**: TLS 1.3 내 양자 내성 하이브리드 키 교환 방식을 명시한 인터넷 표준 문서.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 협상 조작 | **협상 기록 인증**으로 **다운그레이드 공격** 차단 | 약한 조합 선택 방지 |
| 키 설정과 본문 키 재사용 | **RFC 9180 KDF 영역 분리 및 HPKE** 적용 | 키 용도 혼용 방지 |
| 구형 TLS 설계 잔존 | **RFC 9846 기준** 전환 | 순방향 비밀성 확보 |

#### 한줄 요약

- **RFC 9180 HPKE**의 영역 분리와 **AEAD** 본문 보호 적용

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **하이브리드 키 설정 선택(Hybrid Key Establishment Selection)**: 순방향 비밀성과 양자 내성 전환 시점을 종합 판단하여 알고리즘을 결정하는 기법.

</details>

- 현재 통신은 **ECDHE 기반**, 양자 전환기는 **PQC KEM 결합** 선택

#### 한줄 요약

- **신원 인증•키 캡슐화•키 파생•AEAD** 전 주기 검증
