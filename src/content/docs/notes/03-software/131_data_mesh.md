---
sidebar:
  order: 131
  label: "131. 데이터 메시 (Data Mesh)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "데이터 메시 (Data Mesh)"
date: "2026-08-13T23:55:00+09:00"
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

<details><summary>용어 설명</summary>

- **Data Mesh (데이터 메시)**: 자막 데그하니(Zhamak Dehghani)가 제안한 탈중앙화(Decentralized) 도메인 중심 빅데이터 조직 패러다임으로, 데이터 소유권을 현업 도메인 팀(Domain-driven)에 부여하고 데이터를 하나의 독립된 제품(Data-as-a-Product)으로 분산 서비스하는 아키텍처.
- **Domain-Oriented Ownership (도메인 중심 데이터 소유권)**: 중앙 데이터팀의 수집/정제 병목을 제거하고, 현업 도메인(주문, 결제, 회원) 팀이 직접 데이터 생성 및 품질을 소유하고 관리하는 사상.
- **Data-as-a-Product (제품으로서의 데이터)**: 데이터를 단순 파일이 아닌 품질 SLA, 스키마, API 문서가 잘 완비된 재사용 가능한 소프트웨어 '제품'으로 취급하는 원칙.

</details>

- 정의/개념: 도메인이 데이터 상품을 소유하는 **Data Mesh**
- 배경/필요성: 중앙 데이터팀은 **도메인 지식 부족•요청 적체** 발생

#### 한줄 요약

- 자료를 가장 잘 아는 업무 팀이 품질 보증이 붙은 데이터 상품으로 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Self-Serve Data Infrastructure Platform**: 각 도메인 팀이 복잡한 인프라 튜닝 없이 클릭 몇 번으로 인프라(S3, Spark, Catalog)를 즉시 자급자족 프로비저닝할 수 있게 만드는 셀프서비스 플랫폼.
- **Federated Computational Governance**: 전사 표준 데이터 규칙, 보안, PII 암호화는 중앙 연합회가 코드(Policy-as-Code)로 자동 강제 및 모니터링.

</details>

- **Domain-Oriented Decentralized Ownership (도메인 중심 소유권)**
- **Data-as-a-Product (SLA, 스키마 문서, Discoverability 보장)**
- **Self-Serve Data Infrastructure Platform & Federated Computational Governance (4대 원칙)**

#### 한줄 요약

- 책임만 팀별로 나누고 공용 공장과 제품 규격을 주지 않으면 중앙 병목이 여러 데이터 섬으로 바뀐다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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

| 구성요소 | 책임 |
|:---|:---|
| Domain Ownership | 도메인 팀이 데이터 품질•변경•지원 소유 |
| Data-as-a-Product | 계약•SLO•문서•발견성 있는 상품 제공 |
| Self-Serve Platform | 공통 수집•저장•품질•관측 기능 자동화 |
| Federated Governance | 전사 규칙과 도메인 정책을 코드로 집행 |

#### 한줄 요약

- 업무 팀이 공용 설비와 규칙으로 데이터 상품을 만든다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Data Contract (데이터 계약)**: Data Product 생산자와 소비자 간에 주고받는 데이터의 형태, 타입, SLA, 변경 파기 조건을 정식 규약으로 체결하는 계약서.

</details>

```text
[데이터 상품 요구]
      │
      ▼
1. 도메인 경계 지정
      │
      ▼
2. 데이터 계약 정의
      │
      ▼
3. 셀프서비스 파이프라인 구성
      │
      ▼
4. 정책•품질 자동 검증
      │
      ▼
5. 카탈로그•출력 포트 공개
```

### 동작 원리

1. **도메인 경계 지정**: 생산자•소비자•소유 팀 확정
2. **데이터 계약 정의**: 스키마•의미•SLO•변경 정책 명시
3. **셀프서비스 파이프라인 구성**: 표준 템플릿으로 수집•저장 배포
4. **정책•품질 자동 검증**: 보안•호환성•품질 게이트 실행
5. **카탈로그•출력 포트 공개**: 문서•리니지와 접근 방법 제공

#### 한줄 요약

- 업무 팀이 제품을 만들고 공용 공장이 규격을 검사하며 소비자는 카탈로그에서 품질표를 보고 고른다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Centralized Bottleneck vs Decentralized Domain**: 중앙 Data Lake는 과부하 병목 지점이 발생하는 반면, Data Mesh는 도메인 팀 분산 처리로 스케일아웃.

</details>

| 비교 항목 | Centralized Data Lake / DW | Data Mesh Architecture |
|:---|:---|:---|
| 데이터 소유권 | **중앙 데이터 엔지니어링 팀 총괄** | **각 현업 도메인 팀(Payment, Order) 개별 소유** |
| 병목 형태 | 중앙 요청 큐 적체 가능 | 도메인별 역량•우선순위 편차 가능 |
| 도메인 지식 | 중앙팀으로 전달 과정 필요 | **생산 도메인이 의미•품질 직접 소유** |
| 인프라 관리 방식 | 중앙 통합 클러스터 운영 | **Self-Serve 플랫폼 기반 자급자족 생성** |

#### 한줄 요약

- 중앙형은 한 주방이 모두 만들고 메시형은 공용 설비를 쓰는 분야별 주방이 각 메뉴를 책임진다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Data Silo Danger (데이터 파편화 위험)**: 연합 거버넌스 통제 없이 도메인 팀 자율권만 주면 각 도메인이 자신만의 데이터 섬(Silo)으로 고립되는 안티패턴.

</details>

| 3대 Data Mesh 위험 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Data Silo (데이터 파편화) | 연합 거버넌스 정책 없이 각 팀이 낭비 적재 | **전사 메타데이터 카탈로그 (OpenMetadata) 자동 갱신**|
| 2. Domain Cost Explosion | 도메인별로 엉성하게 인프라 중복 띄움 | **Self-Serve 플랫폼의 중앙 비용 통제 (FinOps) 모니터링**|
| 3. Data Quality Failure | 도메인 팀의 데이터 품질 무관심 | **Data Contract 체결 및 Violation 자동 감지 훅 설정** |

> 사례: **토스 / 당근마켓 / Netflix 전사 Data Mesh 도메인 아키텍처 및 OpenMetadata 도입**

#### 한줄 요약

- 주문 팀이 상품 설명서와 품질 목표를 공개하고 문제가 생기면 직접 알리고 고친다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Data Mesh 수립 기준(Data Mesh Architecture Standards)**: Domain Ownership, Data-as-a-Product, Data Contract, Self-Serve Platform 및 Federated Governance에 의거한 체계.

</details>

- 도메인 규모•역량이 충분하면 **Data Mesh**, 작으면 중앙형 유지

#### 한줄 요약

- 팀 이름만 바꾸는 것이 아니라 책임 있는 상품 팀, 공용 공장, 자동 규칙이 함께 작동해야 한다.
