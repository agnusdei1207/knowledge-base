---
sidebar:
  order: 127
  label: "127. Secure Boot 보안 부팅 (Secure Boot)"
  badge:
    text: "기출 • 70%"
    variant: note
title: Secure Boot 보안 부팅 (Secure Boot)
date: "2026-08-05T17:44:55+09:00"
tags:
  - notes-security
weight: 127
extra:
  question_no: "127"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "138회 기출이며 부팅 신뢰사슬의 핵심 통제임"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **UEFI(Unified Extensible Firmware Interface)**: 부팅 서비스와 보안 변수를 관리하는 펌웨어 인터페이스이다.
- **Secure Boot**: UEFI의 키•허용 목록•폐기 목록으로 승인된 코드만 실행하는 기술이다.

</details>

- 정의/개념: UEFI 신뢰 정책으로 **부트 이미지 실행을 통제하는 보안 기술**
- 배경/필요성: 운영체제 보안만으로는 선행 부트킷의 **권한 탈취 차단 불가**

#### 한줄 요약

- 컴퓨터가 켜질 때 다음 프로그램의 서명과 금지 목록을 확인해 승인된 코드만 실행함

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **PK(Platform Key)**: 플랫폼 정책의 소유권을 설정하는 키이다.
- **KEK(Key Exchange Key)**: 허용•폐기 데이터베이스의 갱신 권한을 통제하는 키이다.
- **db(Signature Database)**: 실행을 허용할 서명•인증서•해시 목록이다.
- **dbx(Forbidden Signature Database)**: 실행을 금지할 취약•폐기 대상 목록이다.

</details>

- PK•KEK 기반 **정책 소유•갱신 권한**
- db•dbx 기반 **허용•폐기 판정**
- 펌웨어•부트로더의 **연속 신뢰 사슬**

#### 한줄 요약

- 서명이 유효해도 취약성이 발견되면 dbx에 등록해 이후 부팅을 막아야 함

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **신뢰 사슬**: 첫 신뢰 키에서 시작해 다음 부팅 구성요소를 연속 검증하는 구조이다.
- **UEFI 이미지 검증기**: 부트 이미지의 서명 체인과 허용•폐기 정책을 판정한다.

</details>

```text
Secure Boot 신뢰 구조
├─ 플랫폼 키 PK
├─ 키 교환 키 KEK
├─ 허용 데이터베이스 db
├─ 폐기 데이터베이스 dbx
└─ UEFI 이미지 검증기
```

| 구성요소 | 책임 |
|:---|:---|
| 플랫폼 키 PK | **플랫폼 정책 소유권** 설정 |
| 키 교환 키 KEK | **db•dbx 갱신 권한** 검증 |
| 허용 데이터베이스 db | **허용 서명•인증서•해시** 저장 |
| 폐기 데이터베이스 dbx | **취약•폐기 대상** 거부 |
| UEFI 이미지 검증기 | **서명 체인•정책** 판정 |

#### 한줄 요약

- 소유권 키가 목록 변경을 통제하고 허용•폐기 목록이 실제 부트 파일 실행을 결정함

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **TPM(Trusted Platform Module)**: 암호 키와 플랫폼의 부팅 측정값을 보호하는 모듈이다.

</details>

```text
부트 이미지•서명•인증서
   │
   ▼
1. PK•KEK•db•dbx 정책 설정
   │
   ▼
2. 이미지 서명•해시 검증
   │
   ▼
3. db 허용•dbx 폐기 여부 확인
   │
   ▼
4. 실행 허용•거부 판정
   ├─ 미승인•폐기 ──► 실행 거부•복구 전환
   └─ 승인
        │
        ▼
5. 허용 이미지 측정값 생성
   │
   ▼
다음 부팅 단계 실행•TPM 증적 기록
```

**동작 원리**

- **1. PK•KEK•db•dbx 정책 설정**: 소유권•갱신•허용 정책 설정
- **2. 이미지 서명•해시 검증**: 부트로더•드라이버 진위와 무결성 검증
- **3. db 허용•dbx 폐기 여부 확인**: 신뢰 체인과 폐기 여부를 정책에 대조
- **4. 실행 허용•거부 판정**: 미승인 코드 차단•복구 전환
- **5. 허용 이미지 측정값 생성**: 다음 단계 실행과 TPM 증적 기록

#### 한줄 요약

- 허용 목록에 있어도 폐기 목록에 포함되면 실행하지 않고 인증된 복구 경로로 전환함

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **Secure Boot 역할**: 미승인 부트 이미지의 실행을 차단하는 역할이다.
- **OS(Operating System)**: 하드웨어 자원과 응용 실행을 관리하는 운영체제이다.
- **Trusted Boot**: OS 구성요소까지 연속해서 진위를 검증하는 방식이다.
- **Measured Boot**: 부팅 구성요소의 측정값을 TPM에 기록하는 방식이다.

</details>

| 부팅 신뢰 기능 | 역할 | 연계 결과 |
|:---|:---|:---|
| **Secure Boot** | **미승인 부트 이미지 실행 차단** | 최초 실행 경로의 허용 기준 설정 |
| **Trusted Boot** | **OS 구성요소까지 연속 검증** | 앞 단계의 신뢰를 다음 구성요소로 확장 |
| **Measured Boot** | **TPM에 측정값 기록** | 원격 검증자가 실제 부팅 상태를 판정할 증거 제공 |

> 요약: 실행 차단, 연속 검증, 상태 증명을 구분함

#### 한줄 요약

- Secure Boot는 차단하고 Trusted Boot는 이어 검증하며 Measured Boot는 증거를 남김

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **UEFI Specification 2.11**: Secure Boot•드라이버 서명•키 교환 규격이다.
- **NIST(National Institute of Standards and Technology)**: 미국 국립표준기술연구소이다.
- **SP(Special Publication)**: NIST가 발행하는 특별간행물이다.
- **NIST SP 800-193**: 플랫폼 펌웨어의 보호•탐지•복구 지침이다.
- **TCG(Trusted Computing Group)**: 신뢰 컴퓨팅 표준을 개발하는 산업단체이다.
- **TCG TPM 2.0**: 부팅 측정값 보호와 원격 증명의 규격이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 키 소유권이 불명확하면 정책이 변조됨 | **UEFI Specification 2.11 적용** | PK•KEK•db•dbx 표준화 |
| 부팅 차단만으로 장애 복구가 불가능함 | **NIST SP 800-193 적용** | 보호•탐지•복구 확보 |
| 측정값이 위조되면 원격 판정이 오염됨 | **TCG TPM 2.0 Library 적용** | 측정•원격 증명 기반 확보 |

#### 한줄 요약

- 조직이 승인한 부트로더•커널 서명만 db에 두고 취약 서명자는 dbx로 폐기하며 복구 키와 절차를 별도 검증한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **허용•폐기 동시 판정**: 서명이 허용 목록에 있고 폐기 목록에는 없어야 실행하는 원칙이다.

</details>

- db 허용과 dbx 비폐기를 모두 충족한 **부트 이미지만 실행**

#### 한줄 요약

- 서명 기능보다 누구를 신뢰하고 언제 폐기하며 실패를 어떻게 복구할지가 중요함
