---
sidebar:
  order: 145
  label: "145. 클라우드 공유 책임 모델"
  badge:
    text: "기출 · 70%"
    variant: note
title: "클라우드 공유 책임 모델 (Shared Responsibility Model)"
date: "2026-08-31T10:48:00+09:00"
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
- 배경/필요성: 클라우드 관리 책임을 CSP가 전담할 것으로 오인함에 따른 **보안 설정 오류(Misconfiguration) 및 책임 공백에 의한 데이터 유출 사고 위험 한계**

#### 한줄 요약
- 위탁할 수 있는 것은 통제의 수행이지 책임 자체가 아니므로, 사업자가 맡는 범위가 넓어질수록 고객에게 남는 소수의 항목이 오히려 사고 원인의 대부분을 차지하게 된다.

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
|-- Customer Responsibility (Security IN the Cloud)
|   |-- Customer Data Assets (데이터 분류 및 KMS 암호화)
|   |-- Platform & IAM Management (MFA, RBAC/ABAC 최소 권한 통제)
|   `-- OS / Network Firewall Configuration (OS 보안 패치, Security Group 포트 통제)
`-- CSP Responsibility (Security OF the Cloud)
    |-- Foundation Services (Compute, Storage, Database 인프라 소프트웨어)
    |-- Virtualization Layer (Hypervisor 격리 및 내부 네트워크 인프라)
    `-- Global Physical Infrastructure (리전/AZ 데이터센터 건물 출입, 전력, 공조)
```

선의 의미: 계층 및 상단의 고객 통제 영역과 하단의 CSP 인프라 통제 영역을 서비스 모델별로 분계하는 구조

| 구성요소 | 책임 |
|:---|:---|
| 고객 데이터·IAM | 암호화·접근 통제와 **MFA·최소 권한** |
| 애플리케이션·OS | IaaS의 **패치·취약점 조치** |
| 가상화·플랫폼 | 하이퍼바이저 격리와 **런타임 패치** |
| 물리 데이터센터 | **출입·전력·공조·하드웨어 파기** 통제 |

#### 한줄 요약
- 고객 책임(IN)과 CSP 책임(OF)이 서비스 계층 경계를 중심으로 명확히 분리된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **공유 책임 모델 수립 5단계**: 서비스 모델 식별 $\to$ 관리 계층 분해 $\to$ 책임 주체 배정 $\to$ 통제 도구 매핑 $\to$ 설정 오류(Misconfig) 점검.

</details>

```text
클라우드 신규 서비스 도입 및 보안 거버넌스 수립
        │
   [서비스 모델 식별] 도입 대상이 IaaS(EC2), PaaS(RDS), SaaS(Workspace)인지 분류
        │
   [계층 분해] 시설, 하드웨어, 하이퍼바이저, OS, 미들웨어, 데이터 등 스택 계층 세분화
        │
   [책임 배정 (RACI)] 각 계층의 관리 및 패치 주체를 고객 또는 CSP로 명확히 지정
        │
   [보안 통제 도구 매핑] 고객 책임 영역에 대해 AWS KMS(암호화), GuardDuty(위협 탐지) 연동
        │
   S3 Public Open, Security Group 0.0.0.0/0 등 책임 공백 및 설정 오류를 CSPM으로 상시 점검
```

#### 한줄 요약
- 책임 경계는 서비스 모델이 바뀔 때마다 이동하므로 같은 조직이 IaaS와 SaaS를 함께 쓰면 시스템마다 다른 경계를 관리해야 하고, 그 불일치가 실제 공백이 발생하는 지점이 된다.

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

- 엔터프라이즈 클라우드 보안 아키텍처 및 정보보호 컴플라이언스(ISMS-P, FedRAMP) 준수의 **가장 근본적인 보안 책임 분계 원칙**으로 확립되었으며, 실무 운영 시에는 **S3 Public Open 및 취약한 보안 그룹 설정을 실시간 탐지·교정하는 CSPM(Cloud Security Posture Management) 솔루션 도입, IaaS OS 취약점 자동 패치 파이프라인, 전사 루트 계정 잠금 및 MFA 의무화, 고객 주도 다중 리전 교차 스냅샷 백업 체계**를 결합하여 고객 책임 영역(Security IN the Cloud)의 보안 무결성을 완벽히 보증

#### 한줄 요약
- 클라우드 공유 책임 모델은 CSP와 고객의 보안 책임을 명확히 구분하여 보안 공백을 방지하는 클라우드 거버넌스의 가장 기본적이고 핵심적인 원칙이다.
