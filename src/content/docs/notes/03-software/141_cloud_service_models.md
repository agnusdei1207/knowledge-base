---
sidebar:
  order: 141
  label: "141. 클라우드 서비스 모델: IaaS•PaaS•SaaS (Cloud Service Models)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "클라우드 서비스 모델: IaaS•PaaS•SaaS (Cloud Service Models)"
date: "2026-08-10T10:30:00+09:00"
tags:
  - "notes-software"
weight: 141
extra:
  question_no: "141"
  source_status: "기출"
  source_history: "120회, 125회, 131회, 132회"
  priority: 70
  priority_note: "서비스별 운영 책임 경계가 반복 출제됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Cloud Service Models (클라우드 서비스 모델)**: NIST(미국 표준기술연구소)에서 정의한 클라우드 컴퓨팅 자원의 자율 제어 및 책임 범위에 따른 3대 서비스 분류 체계 (IaaS, PaaS, SaaS).
- **IaaS (Infrastructure as a Service)**: 서버, 디스크, 네트워크 등 물리 하드웨어 인프라 자원만 렌탈받고, OS부터 미들웨어, 앱까지 소비자가 직접 구축하는 모델 (AWS EC2, Compute Engine).
- **PaaS (Platform as a Service)**: OS, 런타임, 미들웨어 환경까지 CSP가 제공하고, 소비자는 개발 코드와 데이터만 배포 관리하는 모델 (AWS Elastic Beanstalk, Heroku).
- **SaaS (Software as a Service)**: 완전한 응용 소프트웨어 애플리케이션 형태로 서비스되어, 소비자는 단순 계정 사용과 데이터만 입력하는 모델 (Salesforce, Google Workspace, Slack).

</details>

- 정의/개념: 클라우드 컴퓨팅 환경에서 프로비저닝되는 자원과 관리 주체(CSP vs Customer)의 책임 한계에 따라 인프라, 플랫폼, 소프트웨어 3단계로 구분한 체계인 **Cloud Service Models (IaaS, PaaS, SaaS)**
- 배경/필요성: 서비스 계층별 관리 책임(Shared Responsibility) 명확화, 인프라 구축 비용 절감 및 개발 민첩성 극대화 요구성

#### 한줄 요약

- 건물만 빌릴지, 조리 시설까지 빌릴지, 완성된 식사를 받을지 정하는 선택이다.

## Ⅱ. 특징 (서비스 모델 3대 레이어 및 책임 범위)

<details><summary>핵심 용어</summary>

- **Shared Responsibility Model (공동 책임 모델)**: IaaS $\rightarrow$ PaaS $\rightarrow$ SaaS로 이동할수록 인프라 관리 부담이 CSP(클라우드 제공자)에게 대거 이관.

</details>

- **IaaS (최대 제어권 & OS/패치/네트워크 보안의 사용자 직접 관리)**
- **PaaS (인프라/OS 관리 소멸, 개발 코드 및 비즈니스 로직 집중)**
- **SaaS (Zero Infrastructure Maintenance, 즉시 사용 가능 완제품 소프트웨어)**

#### 한줄 요약

- 맡기는 층이 많을수록 손은 덜 가지만 직접 바꿀 수 있는 범위도 줄어든다.

## Ⅲ. 구조 및 구성요소 (IaaS vs PaaS vs SaaS 스택 및 책임 매트릭스)

<details><summary>핵심 용어</summary>

- **Cloud Service Stack Matrix**: Application, Data, Runtime, Middleware, OS, Virtualization, Compute, Storage, Networking 9개 스택별 관리 주체 매핑.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│               Cloud Service Model Shared Responsibility Matrix         │
├─────────────────┬───────────────────┬───────────────────┬──────────────┤
│ Layer Stack     │ IaaS (Infrastructure)| PaaS (Platform)   │ SaaS (Soft)  │
├─────────────────┼───────────────────┼───────────────────┼──────────────┤
│ Applications    │  Customer Managed │  Customer Managed │ CSP Managed  │
│ Data            │  Customer Managed │  Customer Managed │ Customer/CSP │
│ Runtime / MW    │  Customer Managed │  CSP Managed      │ CSP Managed  │
│ OS (Operating System) | Customer Managed | CSP Managed    │ CSP Managed  │
│ Virtualization  │  CSP Managed      │  CSP Managed      │ CSP Managed  │
│ Hardware/Net    │  CSP Managed      │  CSP Managed      │ CSP Managed  │
└─────────────────┴───────────────────┴───────────────────┴──────────────┘
```

선의 의미: 클라우드 9대 인프라 스택 레이어별로 고객(Customer)과 제공자(CSP)가 맡는 관리 경계선 매트릭스.

| 서비스 모델 | 고객(Customer) 관리 영역 | 클라우드 사업자(CSP) 관리 영역 | 대표 예시 서비스 |
|:---|:---|:---|:---|
| **IaaS** | **OS, 패치, 미들웨어, 런타임, 앱, 데이터** | **물리 하드웨어, 가상화(Hypervisor), 네트워크** | **AWS EC2, GCP Compute Engine** |
| **PaaS** | **애플리케이션 코드, 데이터** | **OS, 패치, 미들웨어, 런타임, 하드웨어** | **AWS Elastic Beanstalk, Vercel** |
| **SaaS** | **유저 계정 및 입력 데이터** | **앱 전체, 런타임, OS, 하드웨어 일체** | **Slack, Notion, Salesforce** |

#### 한줄 요약

- 건물만 빌릴지 조리 시설이나 완성된 식사까지 받을지 정한다.

## Ⅳ. 흐름도 (클라우드 서비스 모델 선택 의사결정 흐름)

<details><summary>핵심 용어</summary>

- **Control vs Efficiency Tradeoff**: IaaS는 자유도와 제어권 최상(운영 비용 증가), SaaS는 제어권 최하(즉시 개발 민첩성 극대화).

</details>

```text
[서비스 요구사항 분석]
  ├── OS / 커널 수준 커스텀 제어 필수? ─────────────► [IaaS 선택 (AWS EC2)]
  ├── 개발 코드는 작성하되 인프라 관리 0% 원함? ─────► [PaaS 선택 (Elastic Beanstalk)]
  └── 기존 검증된 SW 완제품 즉시 도입 원함? ────────► [SaaS 선택 (Salesforce)]
```

### 동작 원리

1. **IaaS Selection**: 커스텀 OS 환경이 필요한 금융 코어 서비스 개발 시 IaaS 선택.
2. **PaaS Selection**: 빠른 모바일 백엔드 개발 및 오토스케일링 원할 시 PaaS 선택.
3. **SaaS Selection**: 전사 이메일 및 메신저 구축 시 인프라 개발 없이 SaaS 즉시 도입.

#### 한줄 요약

- 공급자가 운영할 층을 만든 뒤 소비자가 맡은 설정과 데이터를 넣고 양쪽의 상태를 함께 감시한다.

## Ⅴ. 종류 및 비교 (IaaS 대 PaaS 대 SaaS 종합 비교)

<details><summary>핵심 용어</summary>

- **Vendor Lock-in (베트종속성)**: PaaS/SaaS는 서비스 이전 시 특유의 API에 묶이는 베어 종속성(Lock-in) 발생 위험.

</details>

| 비교 항목 | IaaS (Infrastructure) | PaaS (Platform) | SaaS (Software) |
|:---|:---|:---|:---|
| **시스템 제어권** | **최상 (OS Root 권한 및 커널 제어)** | 중간 (애플리케이션 영역 제어) | **최하 (설정 및 계정 제어만 가능)** |
| **운영 인력 오버헤드**| **높음 (OS 보안 패치, 미들웨어 관리)**| 낮음 (인프라 관리 자동화) | **최저 (전혀 관리 불필요)** |
| **개발 민첩성** | 보통 (인프라 프로비저닝 필요) | **높음 (코드만 push 하면 배포)** | **최고 (계정 생성 즉시 사용)** |
| **Vendor Lock-in** | 낮음 (다른 Cloud VM으로 이관 쉬움) | 중간 (특정 Cloud API 종속) | **높음 (타 SaaS 전환 시 데이터 이관 난제)**|

#### 한줄 요약

- 서비스형 인프라는 운영체제부터, 서비스형 플랫폼는 앱부터 관리하고 서비스형 소프트웨어는 완성된 앱의 사용자와 데이터를 관리한다.

## Ⅵ. 실무 고려사항 및 대책 (클라우드 서비스 모델 실무 3대 난제 대책)

<details><summary>핵심 용어</summary>

- **Misconfiguration Risk**: IaaS/PaaS 도입 시 고객 측의 Security Group/S3 Bucket 설정 미숙으로 인한 개인정보 유출 사고.

</details>

| 3대 구축 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. IaaS OS Patch Overhead**| OS 보안 패치를 안 해서 랜섬웨어 감염 | **CSP의 Systems Manager (SSM) 자동 패치 구축** |
| **2. PaaS Vendor Lock-in** | 특정 Cloud PaaS 런타임 종속 발생 | **Docker 컨테이너화(CaaS / K8s)로 이식성 확보** |
| **3. SaaS Data Security** | SaaS 서비스 해킹 시 기업 데이터 유출 | **CASB (Cloud Access Security Broker) 도입 통제** |

> 사례: **삼성전자 / 현대자동차 하이브리드 Cloud IaaS-PaaS-SaaS 혼용 아키텍처**

#### 한줄 요약

- 가상 서버를 빌려도 그 안의 운영체제 업데이트는 대개 사용자가 해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Cloud Service Model 수립 기준(Cloud Standards)**: NIST 서비스 분류, Shared Responsibility Matrix 및 CASB 보안 통제성에 의거한 체계.

</details>

- **Cloud Service Model 수립 기준**에 따라 기업 클라우드 전환 시 **IaaS + PaaS + SaaS 적재적소 혼용 아키텍처** 필수 적용

#### 한줄 요약

- 직접 고칠 범위와 직접 책임질 일을 함께 감당할 수 있는 모델을 골라야 한다.
