---
sidebar:
  order: 20
  label: "020. 키 관리 - HSM•KMS (Key Management HSM KMS)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "키 관리 - HSM•KMS (Key Management HSM KMS)"
date: "2026-08-13T18:48:54+09:00"
tags:
  - "notes-security"
weight: 20
extra:
  question_no: "020"
  source_status: "미출제"
  source_history: ""
  priority: 50
  priority_note: "키 생성•보관•회전•폐기는 모든 암호 답안의 기반임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **키 관리(Key Management)**: 암호키의 전 수명주기(생성, 보관, 배포, 회전, 폐기)를 계층화된 인프라 및 정책 기반으로 통제하는 메커니즘.
- **루트 키(Root Key)**: 하위 암호키(KEK 등)의 기밀성을 보호하고 조직 전체 암호 체계의 최상위 신뢰점(Trust Anchor) 역할을 담당하는 무작위 키.

</details>

- 정의/개념: 암호키의 생성•보관•배포•회전•폐기를 통제하는 **키 관리**
- 배경/필요성: 키 하드코딩과 메모리 잔존은 **암호키 유출**을 유발한다.

#### 한줄 요약

- 루트 키(Root Key) 기준 암호키의 전 수명주기(생성-보관-회전-폐기)를 하드웨어 및 인프라 정책 기반으로 통제하는 암호 관리 체계

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **데이터 암호화 키(Data Encryption Key, DEK)**: 실제 평문 데이터(DB 레코드, 파일 등)를 대칭 암호화(AES 등)할 때 사용하는 하위 암호키.
- **키 암호화 키(Key Encryption Key, KEK)**: DEK를 암호화(Key Wrapping)하여 안전하게 보관·전송하기 위한 상위 암호키.
- **하드웨어 보안 모듈(Hardware Security Module, HSM)**: 템퍼 저항성(Tamper Resistance)을 갖춘 전용 물리 장비로, 내부에서만 키를 생성 및 연산하고 키 추출을 차단함 (FIPS 140-3 인증).
- **키 관리 시스템(Key Management System, KMS)**: 키 사용 권한 정책, 수명주기, 자동 회전(Rotation) 및 감사 로그를 중앙 집중식으로 통제하는 소프트웨어/서비스 플랫폼.

</details>

- **KEK**와 **DEK**의 계층화(Envelope Encryption)를 통해 키 노출 및 대규모 재암호화 오버헤드 최소화
- **HSM** 장비 내부 격리 연산을 통한 비밀키 반출 원천 차단
- **KMS** 통제판을 통한 접근 권한(IAM), 키 회전 주기 및 감사 로그(Audit Log) 일괄 관리

#### 한줄 요약

- KEK/DEK 계층적 봉투 암호화(Envelope Encryption), HSM의 하드웨어 물리적 기밀성 및 KMS 기반 중앙 수명주기·감사 통제

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **신원•접근 관리(Identity and Access Management, IAM)**: 키에 대한 접근 권한(Encrypt, Decrypt, Generate)을 요청 주체별로 세분화 통제하는 보안 체계.
- **키 래핑(Key Wrapping)**: 상위 KEK를 사용하여 하위 DEK를 대칭/비대칭 암호화하여 기밀성과 무결성을 동시 제공하는 기술 (RFC 3394 등).

</details>

```text
키 관리 구조
├─ KMS•IAM
├─ HSM•KEK
├─ DEK
├─ 키 메타데이터
```

가지의 의미: 정책·IAM 권한 통제, HSM 물리 보안, DEK 암호화 및 메타데이터 이력 관리 책임을 분리한 구조

| 구성요소 | 책임 |
|:---|:---|
| KMS•IAM | IAM 연동 기반 키 접근 정책 승인, 자동 회전 및 감사 로그 기록 |
| HSM•KEK | **KEK 생성•암호 연산•템퍼 탐지** 수행 |
| DEK | 실제 대용량 데이터를 암호화하기 위한 고속 대칭 세션키 |
| 키 메타데이터 | 키 버전, 사용 목적, 활성화/폐기 상태 및 수명주기 이력 관리 |


#### 한줄 요약

- IAM 권한 통제, KMS 수명주기 엔진, HSM(KEK) 물리 격리 및 DEK 데이터 암호화 구조

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **봉투 암호화(Envelope Encryption)**: 평문 데이터를 DEK로 암호화하고, 사용된 DEK를 KEK로 암호화(Wrapping)하여 데이터 암호문과 암호화된 DEK를 함께 보관하는 방식.
- **제로화(Zeroization)**: 메모리 상에 존재하는 평문 DEK 사용 직후 해당 RAM 주소를 무작위 비트로 완전 덮어쓰기 소거하는 처리 (NIST SP 800-88).
- **IAM•키 정책 검증**: 키 발급/사용 요청 주체에 대한 IAM 롤 및 키 상태(Enabled) 대조 검증 단계.
- **DEK 생성•KEK 래핑**: HSM/KMS에서 난수 DEK 생성 후 KEK 기반 래핑 DEK 도출 단계.
- **데이터 암호화**: RAM 임시 메모리 내 평문 DEK를 통한 데이터 암호문 생성 단계.
- **암호문•래핑 DEK 저장**: 암호화 데이터 패킷과 래핑된 DEK(Wrapped DEK)를 영구 저장소에 바인딩 저장 단계.
- **평문 DEK 제로화**: 연산 완결 후 RAM 메모리 내 평문 DEK 잔재를 완전 제로화 소거하는 단계.

</details>

```text
DEK 생성 요청
        │
        ▼
1. IAM•키 정책 검증
        ├─ 실패: 키 사용 거부
        └─ 성공
             │
             ▼
     2. DEK 생성•KEK 래핑
             │
             └── 평문 DEK 임시 제공
                         │
                         ▼
                  3. 데이터 암호화
                         │
                         ▼
                  4. 암호문•래핑 DEK 저장
                         │
                         ▼
                  5. 평문 DEK 제로화
```

### 동작 원리

1. **IAM•키 정책 검증**: KMS 엔진이 요청 주체의 IAM 권한(kms:GenerateDataKey) 및 키 유효 상태 검증
2. **DEK 생성•KEK 래핑**: HSM 내 KEK 기반으로 난수 DEK 생성 및 래핑 DEK(Wrapped DEK) 동시 발급
3. **데이터 암호화**: 애플리케이션 RAM 임시 구역에서 평문 DEK 기반 고속 대칭 암호화 수행
4. **암호문•래핑 DEK 저장**: 데이터 암호문과 KEK 래핑 DEK를 스토리지에 합성 보관
5. **평문 DEK 제로화**: 연산 즉시 RAM 상의 평문 DEK 메모리를 무작위 비트로 덮어써 **제로화** 소거


#### 한줄 요약

- IAM 권한 검증, KEK 기반 DEK 봉투 암호화(Envelope Encryption), 메모리 평문 DEK 제로화(Zeroization) 및 감찰 기록 흐름

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **비밀 관리기(Secret Manager)**: DB 접속 패스워드, API 토큰, OAuth 시크릿 등 텍스트 기반 응용 자격증명 배포 및 회전에 특화된 중앙 서비스.

</details>

| 키 관리 수단 | **HSM** | **KMS** | **Secret Manager** |
|:---|:---|:---|:---|
| 적용 기준 | 최상위 루트 키 및 서명 물리 보호 | 암호키 전 수명주기 중앙 통제 | DB 접속용 비밀번호·API 토큰 관리 |
| 핵심 특징 | 하드웨어 템퍼 응답 및 키 외부 추출 불가 | IAM 권한 바인딩 및 자동 키 회전 | 애플리케이션 자격증명 동적 인젝션 |
| 한계 | 고비용 구축 및 확장성 제약 | 클라우드 벤더 종속성 위험 | 대용량 데이터 직접 암호화 불리 |

> 요약: 보관 대상 형태(루트키 vs 키 수명주기 vs 자격증명) 및 보안 수준에 따른 선택 결합

#### 한줄 요약

- 루트 키 물리 보호용 HSM, 서비스 수명주기 통제용 KMS, 앱 자격증명 배포용 Secret Manager의 역할별 비교 결합

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **이중 통제(Dual Control)**: 루트 키 생성/복구 등 치명적 키 관리 작업 시 2인 이상의 독립 관리자 동시 승인을 강제하는 원칙.
- **분할 지식(Split Knowledge)**: 암호키 조각을 분할하여 어느 누구도 단독으로 키 전체를 파악할 수 없도록 격리하는 원칙.
- **NIST SP 800-57 Part 1 Rev. 5(NIST SP 800-57 Standard)**: 암호키 수명주기 관리 및 권장 키 길이를 명시한 국제 지침.
- **FIPS 140-3(FIPS 140-3 Standard)**: 암호 모듈의 물리적/소프트웨어적 보안 레벨(Level 1~4)을 검증하는 미국 연방 표준.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 키 수명주기 통제 표준 미비 | **NIST SP 800-57** 지침 준수 | 키 생성, 사용, 회전, 폐기 일관적 관리 |
| 물리적 암호 모듈 탈취 | **FIPS 140-3 (Level 3/4)** HSM 검증 | 물리적 탬퍼 감지 시 키 자동 소거(Zeroization) |
| 내부자 권한 남용/유출 | **이중 통제(Dual Control) 및 분할 지식(Split Knowledge)** | 단일 관리자 독단적 키 유출 방지 |
| 잔재 키를 통한 복구 | **RAM 및 저장매체 제로화(Zeroization)** | 키 폐기 후 잔재 데이터를 통한 소급 해독 차단 |

#### 한줄 요약

- NIST SP 800-57 / FIPS 140-3 준수, 이중 통제(Dual Control) 및 분할 지식(Split Knowledge) 적용, 완전 제로화 통제

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **키 관리 체계 설계(Key Management Design)**: 데이터 중요도, 규제 준수(Compliance), HSM/KMS 하이브리드 결합 및 감사 체계를 통합 반영하는 권고 지침.

</details>

- 루트 및 최상위 서명키는 **HSM**, 대규모 서비스 데이터키 수명주기는 **KMS**, 자격증명은 **Secret Manager** 선택 적용

#### 한줄 요약

- **KEK•DEK 봉투 암호화•HSM•KMS•제로화**를 함께 적용
