---
sidebar:
  order: 127
  label: "127. Secure Boot 보안 부팅 (Secure Boot)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "부팅 신뢰 체인 및 펌웨어 무결성 검증 : Secure Boot (UEFI 2.11 & TCG TPM 2.0)"
date: "2026-08-26T15:01:02+09:00"
tags:
  - "notes-security"
weight: 127
extra:
  question_no: "127"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "138회 기출, UEFI Secure Boot(보안 부팅), 4대 핵심 키/데이터베이스(PK 플랫폼 키, KEK 키 교환 키, db 허용 서명 DB, dbx 폐기 서명 DB), 부팅 신뢰 사슬(Chain of Trust: Secure Boot vs Trusted Boot vs Measured Boot), TCG TPM 2.0 및 NIST SP 800-193 연계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Secure Boot (UEFI 보안 부팅 / UEFI Specification 2.11)**: PC 및 서버의 전원이 켜지는 부팅 초기 단계에서 부트로더, OS 커널, 시스템 드라이버 등 실행되는 모든 소프트웨어 바이너리의 디지털 서명을 검증하여, 공인된 제조사(OEM/Microsoft)의 신뢰할 수 있는 코드만 실행을 허용하고 악성 부트킷(Bootkit) 및 루트킷(Rootkit)의 로드를 원천 차단하는 하드웨어-펌웨어 연계 보안 메커니즘.
- **부팅 초기 악성코드 선점 및 상위 보안 무력화 결함(Pre-OS Compromise Defect)**: 운영체제(OS) 및 백신이 로드되기 전 펌웨어/부트로더 단계에서 악성 부트킷이 실행될 경우, OS 커널의 메모리 주소와 시스템 콜을 하위 계층에서 조작하여 EDR 및 보안 에이전트의 탐지를 영구적으로 은폐(Stealth)하고 시스템 제어권을 독점하는 구조적 결함.

</details>

- 정의/개념: 변조 불가능한 하드웨어 앵커(PK)를 바탕으로 **플랫폼 키(PK) $\rightarrow$ 키 교환 키(KEK) $\rightarrow$ 서명 데이터베이스(db/dbx) 대조 $\rightarrow$ 부트로더 및 커널 전자서명 검증 $\rightarrow$ 신뢰 사슬(Chain of Trust) 릴레이 확립 $\rightarrow$ TPM 2.0 기반 부팅 측정(Measured Boot)** 을 집행하는 **플랫폼 부팅 무결성 보증 아키텍처**
- 배경/필요성: OS 이전 부트킷은 **EDR 탐지와 재설치로 제거 불가**

#### 한줄 요약
- UEFI Secure Boot는 PK, KEK, db, dbx 키 계층을 통해 전자서명을 검증하여 부트킷을 차단하고 신뢰 사슬을 확립한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **UEFI Secure Boot 4대 핵심 키 및 데이터베이스 구조**:
  - **PK (Platform Key / 플랫폼 키)**: 마더보드 OEM 제조사가 소유하며, KEK를 등록/수정할 수 있는 최상위 소유권 인증 키.
  - **KEK (Key Exchange Key / 키 교환 키)**: OS 벤더(Microsoft 등)가 소유하며, db 및 dbx 데이터베이스를 갱신할 수 있는 중간 관리 키.
  - **db (Authorized Signature Database / 허용 서명 DB)**: 부팅 실행을 허용할 정상적인 디지털 인증서, 전자서명 및 SHA-256 해시 목록.
  - **dbx (Forbidden Signature Database / 폐기 서명 DB)**: 보안 취약점이 발견되어 실행을 영구 금지할 취약/악성 인증서 및 해시 블랙리스트.

</details>

- **엄격한 2중 교차 검증 (db 일치 & dbx 부재)**: 실행 대상 파일의 전자서명이 `db`에 존재해야 함과 동시에 `dbx`에 등록되어 있지 않아야만 실행 허용
- **신뢰의 사슬(Chain of Trust) 연속성**: 하드웨어 펌웨어 $\rightarrow$ 부트로더(shim/grub) $\rightarrow$ OS 커널 $\rightarrow$ 드라이버로 이어지는 단계별 상호 검증 릴레이
- **보안 부팅과 측정 부팅(Measured Boot)의 상호보완**: Secure Boot가 악성 코드의 실행을 차단(Prevent)한다면, Measured Boot는 TPM PCR 레지스터에 부팅 구성요소의 해시값을 기록하여 원격 증명(Remote Attestation)을 제공

#### 한줄 요약
- PK/KEK/db/dbx 계층 구조, db/dbx 2중 검증, 신뢰 사슬 확립, TPM 2.0 측정 부팅 연동을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Secure Boot 4대 핵심 아키텍처 컴포넌트**:
  1. **Platform Firmware (UEFI Core)**: NVRAM 내 PK, KEK, db, dbx 변수를 안전하게 보관 및 검증.
  2. **Signature Database (db & dbx)**: 화이트리스트 및 블랙리스트 암호학적 해시 테이블.
  3. **Signed Bootloader (bootx64.efi / shim)**: 제조사 및 OS 벤더의 공개키로 서명된 부트로더.
  4. **TPM 2.0 (Trusted Platform Module)**: 플랫폼 설정 레지스터(PCR 0~7)에 부팅 해시 측정값을 불변 기록.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 1. 플랫폼 소유권 계층 (Platform Key: PK) ]                           │
│  └─ 마더보드 OEM 제조사 공개키 ➔ [ KEK 갱신 권한 통제 (최상위 Root) ]    │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (KEK 관리 및 갱신 승인)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 2. 키 교환 계층 (Key Exchange Key: KEK) ]                             │
│  └─ OS 벤더(Microsoft, Canonical) 공개키 ➔ [ db / dbx 서명 DB 갱신 승인]│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (db / dbx 갱신 명령 전달)
                                     ▼
┌────────────────────────────────────┴────────────────────────────────────┐
│ [ 3. 서명 및 폐기 데이터베이스 계층 (Signature Databases: db & dbx) ]   │
├───────────────────────────────────┬─────────────────────────────────────┤
│ [ db (허용 화이트리스트 DB) ]      │ [ dbx (폐기 블랙리스트 DB) ]        │
│ ├─ 정상 OS 부트로더 전자서명      │ ├─ 취약 부트로더(BlackLotus 등) 해시│
│ └─ [ 실행 허용(Allow) 목록 ]      │ └─ [ 1초 컷 강제 실행 차단(Deny) ]  │
└───────────────────────────────────┴─────────────────────────────────────┘
                                     │ (부트 바이너리 로드 시 교차 검증)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 4. 부팅 신뢰 사슬 릴레이 계층 (Chain of Trust Execution) ]             │
│  ├─ [ UEFI 펌웨어 ] ➔ (검증 성공) ➔ [ OS 부트로더(shim / bootmgr) ]     │
│  ├─ [ OS 부트로더 ] ➔ (검증 성공) ➔ [ OS 커널 (vmlinuz / ntoskrnl) ]    │
│  └─ [ OS 커널 ] ➔ (검증 성공) ➔ [ 시스템 드라이버 및 백신 로드 ]        │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (부팅 해시 측정값 기록)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ 5. 하드웨어 증적 박제 계층 (TCG TPM 2.0 Measured Boot) ]               │
│  └─ [ TPM PCR 레지스터에 부팅 단계별 SHA-256 해시 기록 ➔ 원격 증명 활용 ] │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: PK가 KEK를 통제하고, KEK가 db/dbx를 관리하며, db/dbx를 기준으로 부팅 신뢰 사슬을 검증하고 TPM에 측정값을 기록하는 구조

| 컴포넌트 | 핵심 역할 및 기능 | 소유 및 관리 주체 | 비고 |
|:---|:---|:---|:---|
| **플랫폼 키 (PK)** | KEK 데이터베이스에 대한 쓰기/수정 권한을 인증하는 최상위 마스터 키 | 하드웨어 OEM 제조사 | Root Key |
| **키 교환 키 (KEK)** | db 및 dbx 데이터베이스에 대한 갱신 권한을 부여하는 중간 관리 키 | OS 벤더 (Microsoft, Linux 배포판) | Intermediate|
| **허용 DB (db)** | 부팅 단계에서 실행을 허용할 정상 부트로더 인증서 및 해시 목록 | UEFI Forum, OS 벤더 | Whitelist |
| **폐기 DB (dbx)** | 취약점 노출로 폐기된 부트로더 및 악성코드 해시 블랙리스트 | Microsoft, UEFI Forum | Blacklist |
| **TPM 2.0 (PCR)** | 부팅 전 과정의 실행 바이너리 해시값을 단계별로 누적(Extend) 기록 | 하드웨어 보안 칩 | Measurement |

#### 한줄 요약
- PK(최상위 소유권), KEK(DB 갱신권), db(허용 서명), dbx(폐기 블랙리스트), TPM PCR(측정값 기록)로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Secure Boot 5단계 실행 시퀀스**:
  1. 시스템 전원 인가 및 UEFI 펌웨어 초기화
  2. 부트 장치에서 EFI 부트로더 바이너리 메모리 로드
  3. db 및 dbx 데이터베이스 대조 전자서명 무결성 검증
  4. 검증 결과에 따른 부트로더 실행 승인 또는 차단
  5. OS 커널로 신뢰 사슬 릴레이 및 TPM 2.0 측정값 기록

</details>

```text
1. [전원 인가] 하드웨어 전원 ON ➔ UEFI 펌웨어 자가 진단(POST) 및 Secure Boot 활성화 확인
            │
            ▼
2. [부트로더 로드]
    ├─ SSD/NVMe EFI 시스템 파티션(ESP)에서 `bootx64.efi` 바이너리 로드
    └─ [바이너리 내장 디지털 서명 및 인증서 체인 파싱]
            │
            ▼
3. [db / dbx 2중 교차 검증]
    ├─ 1차: 바이너리 해시/서명이 폐기 목록(dbx)에 존재하는지 확인 ➔ 존재 시 즉시 차단
    └─ 2차: 바이너리 서명이 허용 목록(db)에 유효하게 등록되어 있는지 확인
            │
            ▼
4. [실행 판정 및 분기]
    ├─ [검증 실패 / dbx 일치] ➔ "Security Boot Violation" 에러 출력 및 부팅 강제 중단
    └─ [검증 성공 (db 일치 & dbx 불일치)] ➔ 부트로더 실행 권한 부여
            │
            ▼
5. [커널 릴레이 및 TPM 측정]
    ├─ 부트로더가 OS 커널 서명 검증 ➔ OS 커널이 디바이스 드라이버 서명 검증 (릴레이)
    └─ [각 단계 바이너리 SHA-256 해시를 TPM PCR 0~7 레지스터에 기록 (Measured Boot)]
```

**동작 원리**

1. **사전 실행 차단**: 악성 코드가 단 1개의 명령어라도 실행되기 전에 서명 유효성을 판별하여 차단
2. **동적 취약점 무효화**: BlackLotus 등 과거 정식 서명되었으나 취약점이 발견된 부트로더를 `dbx` 업데이트로 즉각 무력화
3. **단계적 신뢰 확장**: 하위 계층이 상위 계층을 차례로 검증하여 전체 운영체제 로딩 과정의 무결성 보장
4. **변조 불가능한 감사 증적**: TPM의 Hash Extension 방식을 통해 부팅 과정의 변조 여부를 외부 서버가 검증 가능
5. **다중 OS 상호운용성**: Microsoft 3rd Party UEFI CA를 통해 다양한 Linux 배포판(Ubuntu, RHEL)의 안전한 부팅 지원

#### 한줄 요약
- 전원 인가, 부트로더 로드, db/dbx 2중 검증, 실행 판정/차단, 커널 릴레이 및 TPM 기록 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **부팅 보안 3대 체계 비교**:
  - Secure Boot (보안 부팅): 미서명/변조 코드의 실행을 차단(Prevent).
  - Trusted Boot (신뢰 부팅): 펌웨어부터 커널/드라이버까지 신뢰 사슬을 연속 확장(Chain of Trust).
  - Measured Boot (측정 부팅): 부팅 구성요소 해시를 TPM에 기록하여 원격 증명 제공(Attestation).

</details>

| 비교 항목 | Secure Boot (보안 부팅) | Trusted Boot (신뢰 부팅) | Measured Boot (측정 부팅) |
|:---|:---|:---|:---|
| **핵심 목적** | **악성 부트로더의 실행 '차단 (Prevent)'**| **부팅 전 과정의 '신뢰 사슬 확장 (Chain)'**| **부팅 상태의 무결성 '기록 및 증명 (Prove)'**|
| **수행 주체** | **UEFI 펌웨어 (Secure Boot Engine)** | **부트로더 및 OS 커널** | **TPM 2.0 칩셋 및 하드웨어 모듈** |
| **검증 메커니즘** | PK/KEK/db/dbx 서명 대조 | 드라이버/서비스 서명 순차 검증 | **PCR(Platform Configuration Register) 해시 누적**|
| **실패 시 동작** | **부팅 즉시 중단 (Boot Blocked)** | 취약 드라이버 로드 거부 | 부팅은 계속되나 원격 증명 시 격리 |
| **주요 방어 위협** | **Bootkit, 부트로더 변조 공격** | **Rootkit, 취약 커널 드라이버** | **은폐된 시스템 변조, 원격 무결성 검증**|

#### 한줄 요약
- Secure Boot는 미서명 차단, Trusted Boot는 커널 드라이버 신뢰 연장, Measured Boot는 TPM 증적 기록이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **UEFI Specification 2.11 및 TCG TPM 2.0**: 보안 부팅 아키텍처 및 신뢰 플랫폼 모듈 국제 표준 규격.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 과거 정식 서명된 취약한 부트로더(BlackLotus)를 이용해 **Secure Boot를 우회하고 커널 권한을 탈취하는 취약점 공격(BYOVD) 발생** | **Microsoft 및 UEFI Forum의 취약 부트로더 해시를 최신 폐기 데이터베이스(dbx)에 실시간 갱신 배포** | 기지 취약 부트로더를 악용한 Secure Boot 우회 공격 100% 원천 차단 |
| 리눅스 커스텀 커널 또는 독자 드라이버 사용 시 제조사 기본 서명이 없어 **Secure Boot 활성화 상태에서 정상 부팅이 차단되는 장애 발생** | **MOK(Machine Owner Key)를 등록하여 자체 서명 키를 db에 안전하게 추가하거나 Shim 부트로더 아키텍처 활용** | 사용자 정의 OS의 가용성 유지 및 보안 부팅 무결성 동시 확보 |
| 부팅 중 디스크 상의 로그만 확인하여 **공격자가 런타임에 부팅 로그를 위조하고 침해 사실을 은폐하는 감사 실패 발생** | **TCG TPM 2.0 기반 Measured Boot를 적용하여 부팅 바이너리 해시를 PCR 레지스터에 기록하고 원격 증명(Remote Attestation) 수행** | 부팅 상태 위·변조 0% 및 제3자 원격 무결성 신뢰 검증 달성 |

#### 한줄 요약
- dbx 최신화로 취약 부트로더를 차단하고, MOK로 자체 커널을 지원하며, TPM Measured Boot로 무결성을 증명한다.

## Ⅶ. 결론

- 실행 차단은 **Secure Boot**, 원격 증명은 **Measured Boot** 적용

#### 한줄 요약
- PK/KEK/db/dbx 4대 키 구조와 신뢰 사슬 릴레이 및 TPM Measured Boot를 통해 무결점 Secure Boot를 완성한다.
