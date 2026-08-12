---
sidebar:
  order: 132
  label: "132. 데이터 패브릭 (Data Fabric)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "데이터 패브릭 (Data Fabric)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 132
extra:
  question_no: "132"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "135회 기출, 메타데이터 기반 통합 설계"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Data Fabric (데이터 패브릭)**: Gartner가 선정한 핵심 데이터 아키텍처로, 온프레미스, 클라우드, Multi-Cloud에 파편화된 이종 데이터 원천들을 물리적 이동 없이 Active Metadata(활성 메타데이터), AI/ML 지식 그래프(Knowledge Graph)를 기반으로 하나로 유연하게 직조(Fabric)하여 실시간 가상화 통합을 렌더링하는 기술.
- **Active Metadata (활성 메타데이터)**: 데이터 스크레이핑에 의한 수동 메타데이터(Passive Metadata)가 아닌, 쿼리 패턴, 사용자 접근 로그, 파이프라인 성능 실시간 데이터를 AI로 자동 지속 분석하여 파이프라인 최적화에 능동 반영하는 메타데이터.
- **Knowledge Graph (지식 그래프)**: 전사 데이터 자산 간의 연관 관계, 계보(Lineage), 스키마, 사용자 접근 이력을 노드와 엣지로 그래픽 시각화 및 자동 맵핑하는 메커니즘.

</details>

- 정의/개념: 이종의 분산 클라우드/DB 환경에 산재된 데이터를 물리적으로 복제 이동하지 않고, **Active Metadata**와 AI 지식 그래프를 활용해 실시간으로 유연하게 통합 연결하는 모던 데이터 아키텍처인 **Data Fabric**
- 배경/필요성: Multi-Cloud 및 Hybrid 환경 심화로 인한 데이터 파편화 극복, 전통적 수동 ETL/ELT 파이프라인 이동 구축 비용 폭증 문제 해결 요구성

#### 한줄 요약

- 분산 데이터 저장소의 위치·관계·접근 정책을 활성 메타데이터와 지식 그래프로 관리한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Data Virtualization (데이터 가상화)**: 물리적 데이터 이동 0회로 분산 저장소 데이터를 가상 뷰(Virtual View)로 결합.
- **AI-Driven Data Management**: AI/ML 알고리즘이 추천 데이터셋, 자동으로 보안 PII 마스킹 처리 실행.

</details>

- **Active Metadata & Knowledge Graph-Driven Automation (활성 메타데이터 기반 자동화)**
- **Zero Physical Data Movement (Data Virtualization 가상화 통합)**
- **Unified Security & Automated Pipeline Generation (통합 보안 정책 및 자동 파이프라인 생성)**

#### 한줄 요약

- 자동 안내가 똑똑해도 지도 정보가 낡으면 잘못된 자료를 찾거나 잘못된 문을 열 수 있다.

## Ⅲ. 구조 및 구성요소 (Data Fabric 4대 코어 레이어)

<details><summary>핵심 용어</summary>

- **Data Virtualization Layer (가상화 레이어)**: Trino/Denodo 기반으로 서로 다른 DB(PostgreSQL, S3, Snowflake)를 단일 SQL 인터페이스로 묶어주는 가상 통합 엔진.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Data Fabric Architecture                        │
├────────────────────────────────────────────────────────────────────────┤
│ Consumers: [BI Analytics]  [Data Science / ML]  [Operational Apps]     │
├────────────────────────────────────────────────────────────────────────┤
│ Active Metadata & Knowledge Graph Layer (AI/ML Auto Catalog, Lineage) │
├────────────────────────────────────────────────────────────────────────┤
│ Data Virtualization & Orchestration Layer (Trino / Denodo / Airflow)   │
├────────────────────────────────────────────────────────────────────────┤
│ Hybrid Multi-Cloud Sources: [AWS S3]  [Snowflake]  [MySQL]  [Oracle]   │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 이종의 멀티 클라우드 소스 데이터를 Active Metadata 및 가상화 레이어를 거쳐 단일 패브릭으로 묶어 비즈니스 소비자에게 제공하는 아키텍처.

| 계층 (Layer) | 역할 및 기술 메커니즘 | 실무 핵심 기술 스택 |
|:---|:---|:---|
| **Data Sources** | **온프레미스 RDBMS, 클라우드 DW, S3 객체 스토리지** | **AWS S3, Snowflake, PostgreSQL** |
| **Active Metadata** | **실시간 메타데이터 자동 추출, AI 기반 스키마 감지** | **Atlan, Alation, OpenMetadata** |
| **Knowledge Graph** | **데이터 간 의미적 연관성 및 Lineage 자동 그래프 맵핑**| **Neo4j, Amazon Neptune** |
| **Virtualization** | **물리 데이터 이관 없이 가상 쿼리 파이프라인 실행**| **Trino, Denodo, Starburst** |

#### 한줄 요약

- 분산 데이터 저장소를 활성 메타데이터와 통합 정책으로 연결한다.

## Ⅳ. 흐름도 (Data Fabric 대 Data Mesh 아키텍처 사상 비교)

<details><summary>핵심 용어</summary>

- **Data Fabric vs Data Mesh**: Fabric은 기술/AI/메타데이터 중심의 통합 자동화 접근(Technology-centric), Mesh는 조직/도메인 팀 중심의 분산 책임 접근(People & Process-centric).

</details>

```text
[1. Data Fabric (Technology Centric)]
 Distributed Sources ──► [Active Metadata + AI Knowledge Graph] ──► Virtual Layer ──► User (기술 중심 자동화)

[2. Data Mesh (People & Process Centric)]
 Domain Team A/B/C ──► [Data Product (Data Contract)] ──► Self-Serve Platform ──► User (도메인 조직 분산)
```

### 동작 원리

1. **Data Fabric**: AI 기반 활성 메타데이터를 사용하여 물리 데이터 이동 없이 기술적으로 자동 통합 가상화 달성.
2. **Data Mesh**: 데이터 기술이 아닌 조직적 도메인 소유권을 현업에 위임하여 도메인 단위로 데이터 상품 분산 제공.

#### 한줄 요약

- 지도를 계속 갱신하고 목적과 권한에 맞는 길만 열며 통행 결과로 지도를 다시 고친다.

## Ⅴ. 종류 및 비교 (전통적 ETL DW vs Data Fabric)

<details><summary>핵심 용어</summary>

- **Data Virtualization Efficiency**: 가상화 쿼리를 사용함으로써 ETL 개발 수개월 단축 및 스토리지 중복 비용 0원 달성.

</details>

| 비교 항목 | Traditional Data Warehouse / ETL | Data Fabric Architecture |
|:---|:---|:---|
| **데이터 이동 방식** | **물리적 ETL 데이터 추출 및 이관 복제** | **Zero Movement (Data Virtualization 가상화)** |
| **메타데이터 활용** | Passive Metadata (수동 단순 등록) | **Active Metadata (AI 기반 실시간 추적)** |
| **통합 구축 속도** | 느림 (ETL 파이프라인 구축 수개월) | **매우 빠름 (가상 뷰 생성으로 수일 내 연동)** |
| **아키텍처 중심** | 중앙집중식 모놀리식 스토리지 | **하이브리드 멀티클라우드 가상 통합** |

#### 한줄 요약

- 패브릭은 도로와 교통 규칙, 메시는 각 상점의 상품 책임에 가깝다.

## Ⅵ. 실무 고려사항 및 대책 (Data Fabric 실무 3대 난제 대책)

<details><summary>핵심 용어</summary>

- **Virtualization Query Performance Latency**: 물리 데이터 이관이 없으므로, 서로 다른 멀티 클라우드 간 `JOIN` 실행 시 네트워크 렌더링 지연 발생 위험.

</details>

| 3대 구축 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Query Latency 병목** | 가상화 쿼리로 이종 DB 간 `JOIN` 시 네트워크 폭주 | **Trino Pushdown Predicate & 결과 Caching 적용** |
| **2. Active Metadata 지연** | 메타데이터 크롤링 지연으로 낡은 맵핑 전파 | **Debezium CDC 기반 실시간 메타 동기화 훅** |
| **3. Multi-Cloud Security**| AWS와 Azure 간 IAM 보안 정책 불일치 | **Immuta / Privacera 통합 데이터 거버넌스 적용** |

> 사례: **삼성전자 / 현대자동차 글로벌 멀티 클라우드 하이브리드 Data Fabric 가상화 구축**

#### 한줄 요약

- 지도에 장소가 많다는 것보다 위치와 통행 제한이 실제와 맞는지 계속 확인해야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Data Fabric 수립 기준(Data Fabric Architecture Standards)**: Active Metadata, Knowledge Graph, Data Virtualization (Trino) 및 Unified Security에 의거한 체계.

</details>

- **Data Fabric 수립 기준**에 따라 하이브리드 멀티 클라우드 통합 구축 시 **Data Fabric & Active Metadata & Trino** 필수 적용

#### 한줄 요약

- 연결망의 가치는 선의 개수가 아니라 지도가 정확하고 잘못 연 문을 바로 찾아 닫을 수 있는지에 달려 있다.
