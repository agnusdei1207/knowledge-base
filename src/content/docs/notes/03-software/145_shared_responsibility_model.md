---
sidebar:
  order: 145
  label: "145. 클라우드 공유 책임 모델"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클라우드 공유 책임 모델 (Shared Responsibility Model)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
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

- **공유 책임 모델(Shared Responsibility Model)**: 클라우드 서비스 제공자(CSP)와 고객 간에 보안, 컴플라이언스, 운영 영역에 대한 책임을 명확히 분계한 프레임워크.
- **Security OF the Cloud vs Security IN the Cloud**: CSP의 인프라 자체 보안(OF)과 고객의 클라우드 내부 데이터/설정 보안(IN).

</details>

- 정의/개념: 클라우드 환경에서 보안과 거버넌스 공백을 방지하기 위해 **CSP(Security OF the Cloud)와 고객(Security IN the Cloud)의 역할 및 통제 책임을 규정한 프레임워크**
- 배경/필요성: 클라우드 도입 시 인프라 관리가 위탁됨에 따라 발생하는 **데이터 보호 및 IAM 권한 설정 주체 오인에 따른 보안 통제 사각지대 해결 불가**

#### 한줄 요약
- CSP의 인프라 보안과 고객의 데이터/설정 보안 책임을 명확히 구분하여 보안 사각지대를 방지한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Security OF the Cloud**: CSP가 전담하는 데이터센터 물리 보안, 서버 하드웨어, 스토리지 파기, 하이퍼바이저 가상화 계층.
- **Security IN the Cloud**: 고객이 전담하는 데이터 암호화(KMS), IAM 계정/MFA 통제, OS 보안 패치, 방화벽(Security Group) 설정.

</details>

- 물리 시설과 가상화 계층을 CSP가 전담하는 **Security OF the Cloud 책임**
- 데이터 암호화, 계정 통제, 방화벽을 고객이 전담하는 **Security IN the Cloud 책임**
- IaaS에서 PaaS, SaaS로 갈수록 고객 책임이 CSP로 이관되는 **서비스 모델별 가변 경계**

#### 한줄 요약
- 서비스 모델(IaaS/PaaS/SaaS)에 따라 가변적으로 이동하는 보안 책임 경계를 정밀하게 관리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **공유 책임 계층**: Customer Responsibility(IN: 데이터/IAM/OS), CSP Responsibility(OF: 하드웨어/물리IDC/가상화).

</details>

```text
[클라우드 공유 책임 모델 분계선 구조]
|-- 1. Customer Responsibility (Security IN the Cloud)
|   |-- Customer Data Assets (데이터 분류 및 KMS 암호화)
|   |-- Platform & IAM Management (MFA, RBAC/ABAC 최소 권한 통제)
|   `-- OS / Network Firewall Configuration (OS 보안 패치, Security Group 포트 통제)
`-- 2. CSP Responsibility (Security OF the Cloud)
    |-- Foundation Services (Compute, Storage, Database 인프라 소프트웨어)
    |-- Virtualization Layer (Hypervisor 격리 및 내부 네트워크 인프라)
    `-- Global Physical Infrastructure (리전/AZ 데이터센터 건물 출입, 전력, 공조)
```

선의 의미: 계층 및 상단의 고객 통제 영역과 하단의 CSP 인프라 통제 영역을 서비스 모델별로 분계하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **고객 데이터 및 IAM (IN)**| 데이터 암호화, 접근 통제(RBAC/ABAC), **루트 계정 MFA 및 최소 권한 부여 전담** | 고객 100% 전담 책임 |
| **애플리케이션 및 OS (IN)**| IaaS 가상머신의 **OS 보안 패치, 미들웨어 설정 및 애플리케이션 취약점 조치** | IaaS 환경 고객 책임 |
| **가상화 및 플랫폼 (OF)** | 하이퍼바이저 격리, 관리형 PaaS 런타임, **스토리지 결함 허용성 및 패치 제공** | CSP 전담 책임 |
| **물리 데이터센터 (OF)** | 전 세계 리전 및 가용 영역(AZ)의 **물리 출입 통제, 전력, 공조, 하드웨어 파기** | SOC/ISO 인증 증빙 |

#### 한줄 요약
- 고객 책임(IN)과 CSP 책임(OF)이 서비스 계층 경계를 중심으로 명확히 분리된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **공유 책임 모델 수립 5단계**: 서비스 모델 식별 $\to$ 관리 계층 분해 $\to$ 책임 주체 배정 $\to$ 통제 도구 매핑 $\to$ 설정 오류(Misconfig) 점검.

</details>

```text
클라우드 신규 서비스 도입 및 보안 거버넌스 수립
        │
   1. [서비스 모델 식별] 도입 대상이 IaaS(EC2), PaaS(RDS), SaaS(Workspace)인지 분류
        │
   2. [계층 분해] 시설, 하드웨어, 하이퍼바이저, OS, 미들웨어, 데이터 등 스택 계층 세분화
        │
   3. [책임 배정 (RACI)] 각 계층의 관리 및 패치 주체를 고객 또는 CSP로 명확히 지정
        │
   4. [보안 통제 도구 매핑] 고객 책임 영역에 대해 AWS KMS(암호화), GuardDuty(위협 탐지) 연동
        │
   5. S3 Public Open, Security Group 0.0.0.0/0 등 책임 공백 및 설정 오류를 CSPM으로 상시 점검
```

#### 한줄 요약
- 모델 식별 → 계층 분해 → 책임 배정 → 도구 매핑 → 공백 점검 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IaaS vs PaaS vs SaaS 책임 분계**: IaaS(OS부터 고객), PaaS(코드/데이터만 고객), SaaS(계정/데이터만 고객).

</details>

| 비교 항목 | IaaS (인프라 서비스: EC2) | PaaS (플랫폼 서비스: RDS) | SaaS (소프트웨어: M365) |
|:---|:---|:---|:---|
| 데이터 및 IAM 관리 | **고객 전담 책임** | **고객 전담 책임** | **고객 전담 책임 (계정/데이터)**|
| 애플리케이션 및 코드 | **고객 전담 책임** | **고객 전담 책임** | CSP 전담 제공 |
| OS 보안 패치 및 런타임| **고객 전담 책임** | **CSP 전담 관리** | **CSP 전담 관리** |
| 가상화 및 물리 인프라 | **CSP 전담 관리** | **CSP 전담 관리** | **CSP 전담 관리** |

#### 한줄 요약
- IaaS는 OS부터 고객 책임, PaaS는 코드/데이터만 고객 책임, SaaS는 계정/데이터만 고객 책임이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **CSPM(Cloud Security Posture Management)**: S3 버킷 공개, 과도한 IAM 권한 등 클라우드 보안 설정 오류(Misconfiguration)를 실시간 자동 탐지하고 교정하는 도구.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| S3 버킷 퍼블릭 오픈 설정 실수로 인한 대규모 데이터 유출 | **AWS S3 Block Public Access 전사 강제 및 CSPM(Wiz) 실시간 감시** | 설정 오류 기반 데이터 유출 원천 차단 |
| IaaS EC2 인스턴스 OS 보안 패치 누락으로 인한 악성코드 침투 | **AWS Systems Manager(SSM) Patch Manager 정기 자동화 구축** | 무중단 정기 보안 패치 100% 달성 |
| Root 계정 및 AccessKey 유출로 인한 비인가 리소스 생성 | **Root 계정 사용 금지, 전 임직원 MFA 의무화 및 90일 키 회전** | 비인가 크리덴셜 탈취 무력화 |
| PaaS 백업 주체 오인으로 인한 데이터 유실 사고 | **고객 주도 주기적 스냅샷 백업 및 다중 리전 교차 복제(CRR) 구성** | 규제 SLA 충족 및 무손실 복원 |

#### 한줄 요약
- S3 퍼블릭 차단, SSM 자동 패치, MFA 및 키 회전, 고객 주도 스냅샷 백업으로 고객 책임 영역을 완벽히 통제한다.

## Ⅶ. 결론

- 성공적인 클라우드 보안 거버넌스를 확립하기 위해 **서비스 모델(IaaS/PaaS/SaaS)별 공유 책임 모델의 분계선을 명확히 정의하고 CSPM과 IAM 최소 권한 원칙을 고객 책임 영역에 엄격히 적용**하여 보안 사각지대 없는 클라우드 운영 체계 완성

#### 한줄 요약
- 클라우드 공유 책임 모델은 CSP와 고객의 보안 책임을 명확히 구분하여 보안 공백을 방지하는 클라우드 거버넌스의 가장 기본적이고 핵심적인 원칙이다.