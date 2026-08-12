---
sidebar:
  order: 133
  label: "133. 데이터 카탈로그 (Data Catalog)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "데이터 카탈로그 (Data Catalog)"
date: "2026-08-10T23:40:00+09:00"
tags:
  - "notes-software"
weight: 133
extra:
  question_no: "133"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "카탈로그는 데이터 검색•책임•정책 기반"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Data Catalog (데이터 카탈로그)**: 전사 데이터 자산의 위치, 스키마, 소유자, 데이터 계보(Lineage), 품질 지표, 접근 권한 등의 메타데이터를 수집 및 색인(Indexing)하여, 데이터 탐색(Discoverability) 및 거버넌스를 지원하는 중앙 검색 시스템.
- **Data Discoverability (데이터 탐색 용이성)**: 데이터 소비자가 원하는 데이터셋의 위치와 형태를 1초 만에 검색어로 찾아내 활용할 수 있는 상태.
- **OpenMetadata / Apache Atlas**: 전사 데이터 카탈로그 및 메타데이터 자동 크롤링 구축을 위한 표준 오픈소스 솔루션.

</details>

- 정의/개념: 이종 데이터 저장소(S3, DW, RDBMS)의 메타데이터를 자동 크롤링/색인하여, 구글 검색창처럼 데이터셋의 위치, 계보, PII 여부, 소유자를 즉시 탐색하게 해주는 시스템인 **Data Catalog**
- 배경/필요성: 빅데이터 저장소 확장에 따른 "데이터 늪(Data Swamp)" 차단, 데이터 엔지니어에게 매번 쿼리를 물어보는 소통 병목 소멸 요구성

#### 한줄 요약

- 여러 데이터 저장소의 자산이 어디에 있고 무엇이며 누가 책임지는지 제공하는 메타데이터 색인이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Automated Metadata Harvesting**: DB, S3, Spark 작업으로부터 스키마 및 Lineage를 에이전트가 자동 수집.
- **Business Glossary & PII Tagging**: 개인정보(PII) 컬럼 자동 태깅 및 비즈니스 용어집(Glossary) 매핑.

</details>

- **Centralized Metadata Search Engine (구글 스타일 데이터 탐색 지원)**
- **Automated Data Lineage & Schema Extraction (데이터 변환 흐름 추적)**
- **Role-Based Access & PII Auto Tagging (보안 및 거버넌스 연동)**

#### 한줄 요약

- 책 목록을 자동으로 모아도 제목·저자·대출 가능 여부가 틀리면 쓸 수 없어 담당자의 검토가 필요하다.

## Ⅲ. 구조 및 구성요소 (Data Catalog 4대 메커니즘 및 아키텍처)

<details><summary>핵심 용어</summary>

- **Metadata Crawler & Profiler**: 데이터베이스 및 S3를 지속 수집하여 컬럼별 Null 비율, Distinct Count 등의 프로파일링 통계 자동 추출 엔진.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Data Catalog Architecture                       │
├────────────────────────────────────────────────────────────────────────┤
│ Target Sources: [MySQL]  [AWS S3]  [Snowflake]  [Apache Spark Engine] │
├────────────────────────────────────────────────────────────────────────┤
│ Ingestion Layer: [Metadata Crawler / Profiler / Lineage Extractor]    │
├────────────────────────────────────────────────────────────────────────┤
│ Core Engine: [Search Engine (Elasticsearch)]  [Graph DB (Lineage)]    │
│              [Business Glossary & PII Auto Tagging Engine]             │
├────────────────────────────────────────────────────────────────────────┤
│ UI Portal: [Data Discovery Search UI]  [Data Lineage Visualizer]       │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 이종의 타깃 소스로부터 메타데이터 크롤러가 수집한 정보를 검색엔진 및 Graph DB로 색인하여 UI 포털에 렌더링하는 아키텍처.

| 구성요소 (Element) | 역할 및 기술 메커니즘 | 대표 기술 스택 |
|:---|:---|:---|
| **Metadata Crawler** | **이종 DB의 스키마, 테이블, 파티션 정보 자동 추출** | **AWS Glue Crawler, OpenMetadata** |
| **Lineage Extractor** | **Spark/SQL 쿼리 파싱하여 테이블 간 입출력 관계 추출**| **OpenLineage, Sqllineage** |
| **Search Engine** | **테이블명, 컬럼명, 설명 텍스트 기반 초고속 검색** | **Elasticsearch, OpenSearch** |
| **Business Glossary** | **'매출', '고객ID' 등 현업 전사 업무 단어 정의 매핑**| Data Governance Portal |

#### 한줄 요약

- 여러 데이터 저장소 자산의 위치·의미·책임자를 검색하는 메타데이터 색인이다.

## Ⅳ. 흐름도 (Data Catalog 메타데이터 자동 추출 및 시각화 흐름)

<details><summary>핵심 용어</summary>

- **Lineage Visualization**: Raw Data $\rightarrow$ Silver $\rightarrow$ Gold $\rightarrow$ Dashboard까지 데이터가 변환되는 이중화 과정을 그래프 노드로 시각화.

</details>

```text
[Source DB Schema Change] ──► [Crawler Auto Scanning] ──► [Metadata Graph Update]
                                                                  │
                                                                  ▼
 [Client Data Discovery UI] ◄── [Search Indexing] ◄── [PII Tagging & Glossary Mapping]
```

### 동작 원리

1. **Auto Scanning**: 주기적 크롤러가 소스 DB를 스캔하여 신규 컬럼 `phone_number` 감지.
2. **PII Tagging**: AI 태거가 `phone_number` 패턴을 분석하여 `PII_CONFIDENTIAL` 태그 자동 부착.
3. **Discovery Render**: 유저가 검색창에 "전화번호" 입력 시 해당 테이블과 Lineage 그래프가 즉시 서빙 표출.

#### 한줄 요약

- 데이터 저장소를 자동 크롤링하여 목록화하고, 소유권과 스키마 메타데이터를 정제하여 검색 서비스로 제공한다.

## Ⅴ. 종류 및 비교 (Data Dictionary vs Business Glossary vs Data Catalog)

<details><summary>핵심 용어</summary>

- **Comparison of Metadata Tools**: 단순 DB 컬럼 명세서(Dictionary), 현업 단어집(Glossary), 360도 검색/계보/보안 통합 플랫폼(Catalog).

</details>

| 비교 항목 | Data Dictionary (데이터 사전) | Business Glossary (용어집) | Data Catalog (데이터 카탈로그) |
|:---|:---|:---|:---|
| **주요 대상** | 단일 DB 테크니컬 스키마 | 전사 비즈니스 용어 정의 | **전사 하이브리드 멀티 소스 통합** |
| **자동화 수준** | 수동 입력 또는 DDL 추출 | 수동 문서 정리 중심 | **크롤러 기반 100% 자동 수집** |
| **주요 핵심 기능**| 컬럼 타입, PK/FK 제약 조건 | 용어 정의, 단어 표준화 | **검색, Lineage, PII 태깅, SLA 관리** |
| **대표 도메인** | DB Administrator 전용 | 현업 기획자 전용 | **Data Engineer, Scientist, C-Level** |

#### 한줄 요약

- 사전은 책의 항목 설명, 용어집은 공통 단어 뜻, 카탈로그는 여러 책의 위치와 관계를 찾는 목록이다.

## Ⅵ. 실무 고려사항 및 대책 (Data Catalog 구축 실무 3대 지침)

<details><summary>핵심 용어</summary>

- **Metadata Stored Stale Danger**: 크롤링 주기가 너무 길 경우 실제 소스 DB의 삭제된 테이블을 카탈로그가 여전히 안내하는 갱신 지연 현상.

</details>

| 3대 구축 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Metadata Stale** | 크롤링 배치 주기가 일주일로 길어 갱신 지연 | **Debezium DDL 이벤트 감지 즉시 실시간 갱신** |
| **2. Lineage Disconnect**| SQL 쿼리가 파이프라인 외부에서 수동 수정됨 | **OpenLineage 에이전트 Spark/Airflow 전면 탑재** |
| **3. Low User Adoption** | 사용자들이 여전히 쿼리를 개발자에게 물어봄 | **Slack/Teams 챗봇과 카탈로그 검색 API 연동** |

> 사례: **카카오 / 당근마켓 OpenMetadata 기반 전사 데이터 카탈로그 및 Lineage 구축**

#### 한줄 요약

- 목록을 열어 본 횟수보다 맞는 자료를 찾아 실제로 썼는지를 재야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Data Catalog 수립 기준(Data Catalog Standards)**: OpenMetadata 오픈소스, Lineage 자동 추출, PII 태깅 및 Elasticsearch 검색 가속성에 의거한 체계.

</details>

- **Data Catalog 수립 기준**에 따라 전사 데이터 거버넌스구축 시 **OpenMetadata 기반 데이터 카탈로그** 필수 적용

#### 한줄 요약

- 책이 몇 권 등록됐는지보다 필요한 책을 믿고 찾아 빌릴 수 있는지가 중요하다.
