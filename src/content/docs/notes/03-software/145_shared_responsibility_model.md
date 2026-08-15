---
sidebar:
  order: 145
  label: "145. 클라우드 공유 책임 모델 (Shared Responsibility Model)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "클라우드 공유 책임 모델 (Shared Responsibility Model)"
date: "2026-08-14T01:31:00+09:00"
tags: ["notes-software"]
weight: 145
extra:
  question_no: "145"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "서비스별 공급자•사용자 책임 경계가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **Shared Responsibility Model (공유 책임 모델)**: CSP(클라우드 사업자, 예: AWS)와 고객(Customer) 간의 보안, 법적 준수, 시스템 운영 영역에 대한 책임 경계를 가시화한 규정.
- **Security OF the Cloud vs Security IN the Cloud**: CSP는 클라우드 자체의 하드웨어/물리/가상화 보안(Security OF the Cloud)을 책임지고, 고객은 클라우드 내부의 데이터/OS/계정/권한 설정(Security IN the Cloud)을 100% 책임지는 원칙.

</details>

- 정의/개념: CSP와 고객의 통제 경계를 정하는 **Shared Responsibility Model**
- 배경/필요성: 서비스 추상화로 **보안 책임 주체** 오인과 통제 공백 발생

#### 한줄 요약

- 건물주가 건물 설비를 관리해도 입주자가 출입 권한과 내부 자료를 맡듯, 클라우드 서비스가 대신 관리하는 계층과 이용자에게 남은 통제를 구분한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Security OF the Cloud (CSP 책임)**: 데이터센터 물리 보안, 서버 하드웨어, 스토리지, Hypervisor 가상화 레이어.
- **Security IN the Cloud (고객 책임)**: 고객 데이터, IAM 계정 권한, OS 보안 패치, S3 퍼블릭 방화벽 설정.

</details>

- CSP는 물리•가상화 계층의 **Cloud 자체 보안** 책임
- 고객은 데이터•계정•설정의 **Cloud 내부 보안** 책임
- IaaS•PaaS•SaaS별 **책임 경계** 이동

#### 한줄 요약

- 추상화 수준이 높은 서비스 모델일수록 인프라 통제 책임은 공급자에게 이전되지만, 접근 관리와 데이터 보호는 이용자에게 남으며 서비스 모델에 따라 책임 경계만 이동한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CSP SOC Artifacts**: AWS SOC 1, 2, 3 보고서를 다운로드받아 CSP 담당 영역의 물리 통제 및 감사 이력을 확인하는 프로세스.

</details>

```text
┌──────────── 고객 책임 ────────────┐
│ 데이터•계정•애플리케이션•구성     │
├──────── 서비스별 이동 경계 ───────┤
│ 물리 시설•하드웨어•가상화         │
└──────────── CSP 책임 ─────────────┘
```

| 구성요소 | 책임 |
|---|---|
| 고객 책임 | **데이터•IAM**과 애플리케이션 설정 통제 |
| 서비스별 이동 경계 | 모델별 **관리 계층**과 책임 주체 구분 |
| CSP 책임 | **물리 시설•하드웨어**와 가상화 통제 |

#### 한줄 요약

- 건물주와 입주자가 공동 점검표에서 시설·출입·자료 항목의 담당자를 나누듯, 통제 카탈로그의 경계를 책임 매트릭스와 설정 검사로 이어 준다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Responsibility Shift (책임 이동)**: 서비스 모델에 따라 공급자가 관리하는 계층이 달라지는 현상.

</details>

```text
[서비스 도입]
      │
      ▼
1. 서비스 모델 식별
      │
      ▼
2. 관리 계층 분해
      │
      ▼
3. 책임 주체 배정
      │
      ▼
4. 통제•증적 연결
      │
      ▼
5. 책임 공백 점검
      │
      ▼
 [책임표 확정]
```

### 동작 원리

1. **서비스 모델 식별**: IaaS•PaaS•SaaS 유형 확인
2. **관리 계층 분해**: 시설부터 데이터까지 통제 분리
3. **책임 주체 배정**: CSP•고객•공동 책임 명시
4. **통제•증적 연결**: 담당자와 검사 자료 지정
5. **책임 공백 점검**: 미배정•중복 통제 보완

#### 한줄 요약

- 건물주 점검표에서 맡아 주는 항목을 지운 뒤 남은 출입·자료 항목에 담당자와 검사 기록을 붙이듯, 상속 통제와 잔여 통제를 나눠 책임 공백을 찾는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Cloud Security Misconception**: "클라우드로 옮기면 알아서 데이터 보안도 다 해결되겠지"라는 치명적 착각 안티패턴.

</details>

| 3대 오해 사례 | 실상 (Actual Truth) | 해결책 및 책임 주체 |
|:---|:---|:---|
| **"AWS 쓰니까 백업도 알아서 되겠지"** | S3/RDS 백업 설정 및 주기는 **고객 책임** | **고객이 AWS Backup 정책 설정 수립** |
| **"S3 버킷 유출은 AWS 책임이다"** | S3 퍼블릭 오픈 클릭은 **고객 책임** | **고객이 S3 Block Public Access 설정** |
| **"EC2 바이러스 감염은 AWS 탓이다"** | EC2 OS 패치 및 백신 탑재는 **고객 책임** | **고객이 SSM Patch Manager 작동** |

#### 한줄 요약

- 빈 건물인 서비스형 인프라에서 완성 사무실인 서비스형 소프트웨어로 갈수록 공급자가 맡는 계층은 늘지만, 이용자의 계정·데이터·설정 책임은 사라지지 않는다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **CSPM (Cloud Security Posture Management)**: 클라우드 고객 측의 설정 오류(퍼블릭 S3, Root AccessKey)를 실시간 자동으로 감지하여 차단해 주는 클라우드 보안 형상 관리 도구.

</details>

| 3대 고객 책임 구현 지침 | 주요 장애/사고 예방책 | 실무 핵심 도입 도구 |
|:---|:---|:---|
| **1. CSPM 형상 관리** | S3 버킷/Security Group 설정 실수로 유출 | **Wiz, Palo Alto Prisma Cloud (CSPM)** |
| **2. IAM MFA & Key Rotation**| Root AccessKey 유출로 코인 채굴기 도난 | **MFA 강제 및 90일 주기 AccessKey 자동 파기** |
| **3. Data Encryption** | S3 저장 데이터 암호화 미적용 | **AWS KMS (KMS Customer Managed Key) 적용** |

> 사례: **카카오 / 당근마켓 / 금융사 AWS 공유 책임 모델 기반 CSPM 보안 적용**

#### 한줄 요약

- 서비스별 책임 매트릭스와 실제 운영 설정 증적을 대조하여 담당자가 없는 통제를 찾아낸다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Shared Responsibility 수립 기준(Shared Responsibility Standards)**: AWS/GCP 책임 분리 표, CSPM 설정 검증, KMS 데이터 암호화 및 IAM MFA 강제성에 의거한 체계.

</details>

- 모델별 경계를 기준으로 **잔여 통제** 담당자•증적 지정

#### 한줄 요약

- 공급자의 통제 상속 증적을 확인한 뒤에도 이용자에게 남는 계정·데이터 통제의 담당자와 검사 방법을 정한다.
