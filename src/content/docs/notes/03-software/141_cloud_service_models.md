---
sidebar:
  order: 141
  label: "141. 클라우드 서비스 모델: IaaS•PaaS•SaaS (Cloud Service Models)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "클라우드 서비스 모델: IaaS•PaaS•SaaS (Cloud Service Models)"
date: "2026-08-14T01:05:00+09:00"
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

<details><summary>용어 설명</summary>

- **Cloud Service Models (클라우드 서비스 모델)**: NIST(미국 표준기술연구소)에서 정의한 클라우드 컴퓨팅 자원의 자율 제어 및 책임 범위에 따른 3대 서비스 분류 체계 (IaaS, PaaS, SaaS).
- **IaaS (Infrastructure as a Service)**: 서버, 디스크, 네트워크 등 물리 하드웨어 인프라 자원만 렌탈받고, OS부터 미들웨어, 앱까지 소비자가 직접 구축하는 모델 (AWS EC2, Compute Engine).
- **PaaS (Platform as a Service)**: OS, 런타임, 미들웨어 환경까지 CSP가 제공하고, 소비자는 개발 코드와 데이터만 배포 관리하는 모델 (AWS Elastic Beanstalk, Heroku).
- **SaaS (Software as a Service)**: 완전한 응용 소프트웨어 애플리케이션 형태로 서비스되어, 소비자는 단순 계정 사용과 데이터만 입력하는 모델 (Salesforce, Google Workspace, Slack).

</details>

- 정의/개념: 고객•사업자 책임 경계의 **IaaS•PaaS•SaaS** 분류
- 배경/필요성: 책임 경계가 불명확하면 **패치•설정•데이터 보호** 누락

#### 한줄 요약

- 건물만 빌릴지, 조리 시설까지 빌릴지, 완성된 식사를 받을지 정하는 선택이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Shared Responsibility Model (공동 책임 모델)**: IaaS $\rightarrow$ PaaS $\rightarrow$ SaaS로 이동할수록 인프라 관리 부담이 CSP(클라우드 제공자)에게 대거 이관.

</details>

- **IaaS (최대 제어권 & OS/패치/네트워크 보안의 사용자 직접 관리)**
- **PaaS (인프라/OS 관리 소멸, 개발 코드 및 비즈니스 로직 집중)**
- **SaaS (Zero Infrastructure Maintenance, 즉시 사용 가능 완제품 소프트웨어)**

#### 한줄 요약

- 맡기는 층이 많을수록 손은 덜 가지만 직접 바꿀 수 있는 범위도 줄어든다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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

| 구성요소 | 책임 |
|:---|:---|
| **IaaS** | 고객은 OS 이상, 사업자는 가상화 이하 관리 |
| **PaaS** | 고객은 코드•데이터, 사업자는 런타임 이하 관리 |
| **SaaS** | 고객은 계정•설정•데이터 사용, 사업자는 앱 운영 |
| **Shared Responsibility** | 계층별 보안•가용성•백업 책임 명시 |

#### 한줄 요약

- 건물만 빌릴지 조리 시설이나 완성된 식사까지 받을지 정한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Control vs Efficiency Tradeoff**: IaaS는 자유도와 제어권 최상(운영 비용 증가), SaaS는 제어권 최하(즉시 개발 민첩성 극대화).

</details>

```text
[서비스 요구]
      │
      ▼
1. 제어 필요 계층 식별
      │
      ▼
2. 고객 운영 역량 평가
      │
      ▼
3. 규제•데이터 책임 확인
      │
      ▼
4. 서비스 모델 선택
      │
      ▼
5. 책임 매트릭스 검증
```

### 동작 원리

1. **제어 필요 계층 식별**: 커널•런타임•앱 설정 범위 결정
2. **고객 운영 역량 평가**: 패치•관측•복구 담당 능력 확인
3. **규제•데이터 책임 확인**: 위치•암호화•백업 의무 대조
4. **서비스 모델 선택**: 제어•민첩성•비용으로 후보 결정
5. **책임 매트릭스 검증**: 장애•보안 시나리오별 담당 확인

#### 한줄 요약

- 공급자가 운영할 층을 만든 뒤 소비자가 맡은 설정과 데이터를 넣고 양쪽의 상태를 함께 감시한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Vendor Lock-in (베트종속성)**: PaaS/SaaS는 서비스 이전 시 특유의 API에 묶이는 베어 종속성(Lock-in) 발생 위험.

</details>

| 비교 항목 | IaaS (Infrastructure) | PaaS (Platform) | SaaS (Software) |
|:---|:---|:---|:---|
| **시스템 제어권** | **OS•런타임•앱 제어** | 앱•데이터 제어 | 계정•제품 설정 중심 |
| **운영 인력 오버헤드**| **높음 (OS 보안 패치, 미들웨어 관리)**| 낮음 (인프라 관리 자동화) | **최저 (전혀 관리 불필요)** |
| **개발 민첩성** | 보통 (인프라 프로비저닝 필요) | **높음 (코드만 push 하면 배포)** | **최고 (계정 생성 즉시 사용)** |
| **Vendor Lock-in** | 낮음 (다른 Cloud VM으로 이관 쉬움) | 중간 (특정 Cloud API 종속) | **높음 (타 SaaS 전환 시 데이터 이관 난제)**|

#### 한줄 요약

- 서비스형 인프라는 운영체제부터, 서비스형 플랫폼는 앱부터 관리하고 서비스형 소프트웨어는 완성된 앱의 사용자와 데이터를 관리한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

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

<details><summary>용어 설명</summary>

- **Cloud Service Model 수립 기준(Cloud Standards)**: NIST 서비스 분류, Shared Responsibility Matrix 및 CASB 보안 통제성에 의거한 체계.

</details>

- OS 제어는 **IaaS**, 코드 집중은 PaaS, 완제품 사용은 SaaS 선택

#### 한줄 요약

- 직접 고칠 범위와 직접 책임질 일을 함께 감당할 수 있는 모델을 골라야 한다.
