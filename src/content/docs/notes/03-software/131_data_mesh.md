---
sidebar:
  order: 131
  label: "131. 데이터 메시 (Data Mesh)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "데이터 메시 (Data Mesh)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 131
extra:
  question_no: "131"
  source_status: "기출"
  source_history: "123회, 135회"
  priority: 70
  priority_note: "123•135회 반복, 도메인 데이터 책임 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Data Mesh (데이터 메시)**: 자막 데그하니(Zhamak Dehghani)가 제안한 탈중앙화(Decentralized) 도메인 중심 빅데이터 조직 패러다임으로, 데이터 소유권을 현업 도메인 팀(Domain-driven)에 부여하고 데이터를 하나의 독립된 제품(Data-as-a-Product)으로 분산 서비스하는 아키텍처.
- **Domain-Oriented Ownership (도메인 중심 데이터 소유권)**: 중앙 데이터팀의 수집/정제 병목을 제거하고, 현업 도메인(주문, 결제, 회원) 팀이 직접 데이터 생성 및 품질을 소유하고 관리하는 사상.
- **Data-as-a-Product (제품으로서의 데이터)**: 데이터를 단순 파일이 아닌 품질 SLA, 스키마, API 문서가 잘 완비된 재사용 가능한 소프트웨어 '제품'으로 취급하는 원칙.

</details>

- 정의/개념: 중앙 데이터팀의 병목을 소멸시키기 위해 도메인 팀이 직접 데이터를 제품(Data Product)으로 개발하여 공유하고, 연합 거버넌스와 셀프서비스 플랫폼으로 통합 관리하는 탈중앙화 아키텍처인 **Data Mesh**
- 배경/필요성: 기존 중앙집중식 DW/Data Lake의 도메인 지식 부재 및 병목 파행 극복, 도메인 주도 설계(DDD)를 빅데이터 파이프라인 영역으로 확장 수용 요구성

#### 한줄 요약

- 자료를 가장 잘 아는 업무 팀이 품질 보증이 붙은 데이터 상품으로 제공한다.

## Ⅱ. 특징 (Data Mesh 4대 핵심 원칙)

<details><summary>핵심 용어</summary>

- **Self-Serve Data Infrastructure Platform**: 각 도메인 팀이 복잡한 인프라 튜닝 없이 클릭 몇 번으로 인프라(S3, Spark, Catalog)를 즉시 자급자족 프로비저닝할 수 있게 만드는 셀프서비스 플랫폼.
- **Federated Computational Governance**: 전사 표준 데이터 규칙, 보안, PII 암호화는 중앙 연합회가 코드(Policy-as-Code)로 자동 강제 및 모니터링.

</details>

- **Domain-Oriented Decentralized Ownership (도메인 중심 소유권)**
- **Data-as-a-Product (SLA, 스키마 문서, Discoverability 보장)**
- **Self-Serve Data Infrastructure Platform & Federated Computational Governance (4대 원칙)**

#### 한줄 요약

- 책임만 팀별로 나누고 공용 공장과 제품 규격을 주지 않으면 중앙 병목이 여러 데이터 섬으로 바뀐다.

## Ⅲ. 구조 및 구성요소 (Data Mesh 4대 기둥 및 아키텍처)

<details><summary>핵심 용어</summary>

- **Data Product Quantum**: 독립된 데이터 제품 단위로 데이터 파이프라인, 메타데이터, 보안 정책, 코드 및 서빙 API가 일체형 패키징된 구조.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Data Mesh Architecture                          │
├────────────────────────────────────────────────────────────────────────┤
│ [Domain A: Order]        [Domain B: Payment]        [Domain C: User]   │
│ ┌──────────────────┐     ┌──────────────────┐       ┌────────────────┐ │
│ │ Data Product A   │     │ Data Product B   │       │ Data Product C │ │
│ └──────────────────┘     └──────────────────┘       └────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ Self-Serve Data Infrastructure Platform (AWS S3, Databricks, Athena)   │
├────────────────────────────────────────────────────────────────────────┤
│ Federated Governance (Policy-as-Code, OpenMetadata, IAM Security)      │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 각각의 현업 도메인이 Data Product를 생성하고, 하단의 셀프서비스 플랫폼 및 연합 거버넌스가 이를 받쳐주는 탈중앙 아키텍처.

| Data Mesh 4대 원칙 | 핵심 개념 및 주요 메커니즘 | 실무 적용 방안 |
|:---|:---|:---|
| **1. Domain Ownership** | **현업 도메인(결제, 유저) 팀이 데이터 소유** | 도메인 전담 Data Engineer 배치 |
| **2. Data-as-a-Product** | **데이터에 SLA, 스키마, 발견 가능성(Findability) 제공**| Data Contract (데이터 계약) 서명 |
| **3. Self-Serve Platform** | **인프라 프로비저닝 자동화 셀프서비스 레이어 제공**| IaC (Terraform) + Databricks 템플릿 |
| **4. Federated Governance**| **전사 공통 보안, PII 암호화 규칙의 코드화 자동 실행**| OpenPolicyAgent (OPA) + Glue |

#### 한줄 요약

- 업무 팀이 공용 설비와 규칙으로 데이터 상품을 만든다.

## Ⅳ. 흐름도 (Data Product 내부 3대 레이어 파이프라인)

<details><summary>핵심 용어</summary>

- **Data Contract (데이터 계약)**: Data Product 생산자와 소비자 간에 주고받는 데이터의 형태, 타입, SLA, 변경 파기 조건을 정식 규약으로 체결하는 계약서.

</details>

```text
[Input Ports (Source Ingest)] ──► [Internal Pipeline Engine (Spark/Flink)]
                                            │
                                            ▼
   [Client App] ◄── [Output Ports (REST API, SQL Port, S3 Parquet Port)]
```

### 동작 원리

1. **Input Ports**: 도메인 소스 시스템 CDC 및 모바일 로그 이벤트를 수입 port로 수용.
2. **Internal Code**: 도메인 파이프라인 엔진이 가공 및 정제 연산 수행.
3. **Output Ports**: 소비자가 쉽게 읽어갈 수 있도록 SQL 인터페이스, REST API, Parquet 파일 등 표준화된 Output Port로 공개 (**Data Product 완결**).

#### 한줄 요약

- 업무 팀이 제품을 만들고 공용 공장이 규격을 검사하며 소비자는 카탈로그에서 품질표를 보고 고른다.

## Ⅴ. 종류 및 비교 (Monolithic Data Lake vs Data Mesh)

<details><summary>핵심 용어</summary>

- **Centralized Bottleneck vs Decentralized Domain**: 중앙 Data Lake는 과부하 병목 지점이 발생하는 반면, Data Mesh는 도메인 팀 분산 처리로 스케일아웃.

</details>

| 비교 항목 | Centralized Data Lake / DW | Data Mesh Architecture |
|:---|:---|:---|
| **데이터 소유권** | **중앙 데이터 엔지니어링 팀 총괄** | **각 현업 도메인 팀(Payment, Order) 개별 소유** |
| **병목 발생 여부** | **중앙 팀 쿼리 요청 큐 적체 (병목 폭발)** | **도메인 별 독립 스케일아웃 (병목 소멸)** |
| **도메인 데이터 이해도**| 낮음 (중앙팀이 비즈니스 맥락을 모름) | **극상 (현업 개발자가 직접 데이터 튜닝)** |
| **인프라 관리 방식** | 중앙 통합 클러스터 운영 | **Self-Serve 플랫폼 기반 자급자족 생성** |

#### 한줄 요약

- 중앙형은 한 주방이 모두 만들고 메시형은 공용 설비를 쓰는 분야별 주방이 각 메뉴를 책임진다.

## Ⅵ. 실무 고려사항 및 대책 (Data Mesh 실무 3대 파행 요소 해결책)

<details><summary>핵심 용어</summary>

- **Data Silo Danger (데이터 파편화 위험)**: 연합 거버넌스 통제 없이 도메인 팀 자율권만 주면 각 도메인이 자신만의 데이터 섬(Silo)으로 고립되는 안티패턴.

</details>

| 3대 Data Mesh 위험 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Data Silo (데이터 파편화)**| 연합 거버넌스 정책 없이 각 팀이 낭비 적재 | **전사 메타데이터 카탈로그 (OpenMetadata) 자동 갱신**|
| **2. Domain Cost Explosion** | 도메인별로 엉성하게 인프라 중복 띄움 | **Self-Serve 플랫폼의 중앙 비용 통제 (FinOps) 모니터링**|
| **3. Data Quality Failure** | 도메인 팀의 데이터 품질 무관심 | **Data Contract 체결 및 Violation 자동 감지 훅 설정** |

> 사례: **토스 / 당근마켓 / Netflix 전사 Data Mesh 도메인 아키텍처 및 OpenMetadata 도입**

#### 한줄 요약

- 주문 팀이 상품 설명서와 품질 목표를 공개하고 문제가 생기면 직접 알리고 고친다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Data Mesh 수립 기준(Data Mesh Architecture Standards)**: Domain Ownership, Data-as-a-Product, Data Contract, Self-Serve Platform 및 Federated Governance에 의거한 체계.

</details>

- **Data Mesh 수립 기준**에 따라 대규모 조직의 탈중앙화 데이터 파이프라인 구축 시 **Data Mesh & OpenMetadata & Data Contract** 필수 적용

#### 한줄 요약

- 팀 이름만 바꾸는 것이 아니라 책임 있는 상품 팀, 공용 공장, 자동 규칙이 함께 작동해야 한다.
