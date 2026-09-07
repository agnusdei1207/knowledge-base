---
sidebar:
  order: 127
  label: "127. Secure Boot 보안 부팅 (Secure Boot)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "부팅 신뢰 체인 및 펌웨어 무결성 검증 : Secure Boot (UEFI 2.11 & TCG TPM 2.0)"
date: "2026-09-07T14:00:00+09:00"
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
- 배경/필요성: 운영체제(OS) 및 보안 백신이 로드되기 이전인 부팅 초기 단계에서 악성 부트킷(Bootkit)이나 루트킷이 먼저 실행될 경우, OS 커널 시스템 콜과 메모리를 하위 계층에서 조작하여 EDR의 탐지를 영구적으로 은폐하고 시스템 전체 제어권을 장악하는 치명적 맹점이 존재함에 따라, UEFI 2.11 및 TCG TPM 2.0 표준에 기반하여 마더보드 최상위 플랫폼 키(PK), 키 교환 키(KEK), 허용 서명 DB(db) 및 폐기 서명 DB(dbx) 4대 키 계층을 구축하고, 부트로더 $\rightarrow$ OS 커널 $\rightarrow$ 드라이버로 이어지는 신뢰의 사슬(Chain of Trust) 전자서명 릴레이 검증 및 TPM PCR 기반 측정 부팅(Measured Boot)을 결합하는 Secure Boot 아키텍처를 도입하여 **Pre-OS 구간 악성코드 실행 원천 차단, 부팅 전주기 무결성 보증 및 하드웨어 기반 원격 증명(Remote Attestation) 신뢰성**을 달성할 필요

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
[UEFI Secure Boot 아키텍처]
├── [1. 플랫폼 소유권 계층 (PK)]
│   └── OEM 제조사 키 (KEK 갱신 권한 통제)
├── [2. 키 교환 계층 (KEK)]
│   └── OS 벤더 관리 키 (db/dbx 갱신 승인)
├── [3. 서명 및 폐기 데이터베이스]
│   ├── 허용 서명 DB (db: 실행 허용)
│   └── 폐기 서명 DB (dbx: 실행 차단)
├── [4. 부팅 신뢰 사슬 (Chain of Trust)]
│   ├── UEFI 펌웨어 ── 부트로더(shim)
│   └── OS 커널 ── 드라이버 무결성 검증
└── [5. 하드웨어 측정 계층 (TPM 2.0)]
    └── PCR 레지스터 부팅 해시 누적 기록
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| **플랫폼 키 (PK)** | 하드웨어 OEM 소유, KEK 데이터베이스 쓰기·수정 권한 인증 최상위 키 |
| **키 교환 키 (KEK)** | OS 벤더 소유, db 및 dbx 서명 데이터베이스 갱신 권한 부여 중간 키 |
| **허용 DB (db)** | 부팅 단계에서 실행을 허용할 정상 부트로더 인증서 및 해시 목록 |
| **폐기 DB (dbx)** | 취약점 노출로 폐기된 부트로더 및 악성코드 해시 블랙리스트 |
| **TPM 2.0 (PCR)** | 부팅 전 과정 바이너리 해시를 단계별 누적(Extend) 기록 및 원격 증명 |

#### 한줄 요약
- PK와 KEK는 코드를 직접 검사하지 않고 아래 계층을 갱신할 권한만 쥐므로 신뢰의 근거가 바이너리 내용 판단에서 키 소유권의 상하 관계로 옮겨지며, dbx는 그 사슬이 이미 내준 신뢰를 되돌리는 유일한 통로가 된다.

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
- 시큐어 부팅은 서명되지 않은 코드를 아예 실행하지 않아 확실하지만 부팅 자체를 중단시키므로, 기록만 남기는 측정 부팅과 달리 가용성을 대가로 무결성을 사는 방식이다.

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

- 운영체제 이전(Pre-OS) 최하위 부팅 단계부터 악성 부트킷의 개입을 원천 차단하고 신뢰의 기점을 하드웨어로 확립하는 **플랫폼 부팅 무결성 및 신뢰 사슬(UEFI Secure Boot / PK·KEK·db·dbx / TCG TPM 2.0)의 핵심 방어 표준 아키텍처**로 확고히 자리 잡았으며, 제로 트러스트 기기 신원 검증 및 클라우드 가상 머신(vTPM) 보안으로 확장되는 가운데, 실무 엔터프라이즈 엔드포인트 및 서버 인프라 구축 시에는 **BlackLotus 등 알려진 취약 부트로더 차단을 위한 폐기 서명 DB(dbx) 주기적 최신 갱신 배포, 커스텀 리눅스 커널을 위한 MOK(Machine Owner Key) 보안 프로비저닝, TPM 2.0 PCR 레지스터 기반 측정 부팅(Measured Boot)과 연계한 네트워크 접근 제어(NAC/ZTNA 원격 증명)**를 결합하여 완벽한 하드웨어 부팅 신뢰성을 완성

#### 한줄 요약
- PK/KEK/db/dbx 4대 키 구조와 신뢰 사슬 릴레이 및 TPM Measured Boot를 통해 무결점 Secure Boot를 완성한다.
