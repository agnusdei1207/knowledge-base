---
sidebar:
  order: 133
  label: "133. 데이터 카탈로그 (Data Catalog)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "데이터 카탈로그 (Data Catalog)"
date: "2026-08-14T00:09:00+09:00"
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

<details><summary>용어 설명</summary>

- **Data Catalog (데이터 카탈로그)**: 전사 데이터 자산의 위치, 스키마, 소유자, 데이터 계보(Lineage), 품질 지표, 접근 권한 등의 메타데이터를 수집 및 색인(Indexing)하여, 데이터 탐색(Discoverability) 및 거버넌스를 지원하는 중앙 검색 시스템.
- **Data Discoverability (데이터 탐색 용이성)**: 데이터 소비자가 원하는 데이터셋의 위치와 형태를 1초 만에 검색어로 찾아내 활용할 수 있는 상태.
- **OpenMetadata / Apache Atlas**: 전사 데이터 카탈로그 및 메타데이터 자동 크롤링 구축을 위한 표준 오픈소스 솔루션.

</details>

- 정의/개념: 데이터 자산의 검색•책임•정책을 제공하는 **Data Catalog**
- 배경/필요성: 저장소 확장은 **자산 위치•의미•신뢰도 탐색 비용** 증가

#### 한줄 요약

- 여러 데이터 저장소의 자산이 어디에 있고 무엇이며 누가 책임지는지 제공하는 메타데이터 색인이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Automated Metadata Harvesting**: DB, S3, Spark 작업으로부터 스키마 및 Lineage를 에이전트가 자동 수집.
- **Business Glossary & PII Tagging**: 개인정보(PII) 컬럼 자동 태깅 및 비즈니스 용어집(Glossary) 매핑.

</details>

- **Centralized Metadata Search Engine (구글 스타일 데이터 탐색 지원)**
- **Automated Data Lineage & Schema Extraction (데이터 변환 흐름 추적)**
- **Role-Based Access & PII Auto Tagging (보안 및 거버넌스 연동)**

#### 한줄 요약

- 책 목록을 자동으로 모아도 제목·저자·대출 가능 여부가 틀리면 쓸 수 없어 담당자의 검토가 필요하다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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

| 구성요소 | 책임 |
|:---|:---|
| **Metadata Crawler** | 스키마•테이블•파티션•통계 수집 |
| **Lineage Extractor** | 작업•SQL의 입력•출력 관계 추출 |
| **Search Index** | 이름•설명•태그•용어 기반 자산 검색 |
| **Business Glossary** | 업무 용어와 기술 자산 의미 연결 |
| **Ownership•Policy** | 소유자•품질•접근•PII 정책 관리 |

#### 한줄 요약

- 여러 데이터 저장소 자산의 위치·의미·책임자를 검색하는 메타데이터 색인이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Lineage Visualization**: Raw Data $\rightarrow$ Silver $\rightarrow$ Gold $\rightarrow$ Dashboard까지 데이터가 변환되는 이중화 과정을 그래프 노드로 시각화.

</details>

```text
[데이터 자산 변경]
       │
       ▼
1. 기술 메타데이터 수집
       │
       ▼
2. 리니지•프로파일 생성
       │
       ▼
3. 용어•민감도 분류
       │
       ▼
4. 소유자 검토•승인
       │
       ▼
5. 검색 색인•공개
```

### 동작 원리

1. **기술 메타데이터 수집**: 커넥터가 스키마•변경 정보 추출
2. **리니지•프로파일 생성**: 입출력 관계와 품질 통계 계산
3. **용어•민감도 분류**: 업무 의미•PII 후보 자동 태깅
4. **소유자 검토•승인**: 책임자가 의미•정책•신뢰도 확인
5. **검색 색인•공개**: 권한별 검색•계보•품질 정보 제공

#### 한줄 요약

- 데이터 저장소를 자동 크롤링하여 목록화하고, 소유권과 스키마 메타데이터를 정제하여 검색 서비스로 제공한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Comparison of Metadata Tools**: 단순 DB 컬럼 명세서(Dictionary), 현업 단어집(Glossary), 360도 검색/계보/보안 통합 플랫폼(Catalog).

</details>

| 비교 항목 | Data Dictionary (데이터 사전) | Business Glossary (용어집) | Data Catalog (데이터 카탈로그) |
|:---|:---|:---|:---|
| **주요 대상** | 단일 DB 테크니컬 스키마 | 전사 비즈니스 용어 정의 | **전사 하이브리드 멀티 소스 통합** |
| **자동화 수준** | DDL 추출•수동 보완 | 업무 담당자 정의•승인 | **자동 수집과 소유자 검토 결합** |
| **주요 핵심 기능**| 컬럼 타입, PK/FK 제약 조건 | 용어 정의, 단어 표준화 | **검색, Lineage, PII 태깅, SLA 관리** |
| **대표 도메인** | DB Administrator 전용 | 현업 기획자 전용 | **Data Engineer, Scientist, C-Level** |

#### 한줄 요약

- 사전은 책의 항목 설명, 용어집은 공통 단어 뜻, 카탈로그는 여러 책의 위치와 관계를 찾는 목록이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

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

<details><summary>용어 설명</summary>

- **Data Catalog 수립 기준(Data Catalog Standards)**: OpenMetadata 오픈소스, Lineage 자동 추출, PII 태깅 및 Elasticsearch 검색 가속성에 의거한 체계.

</details>

- 기술 구조는 **사전**, 업무 의미는 Glossary, 통합 탐색은 Catalog 선택

#### 한줄 요약

- 책이 몇 권 등록됐는지보다 필요한 책을 믿고 찾아 빌릴 수 있는지가 중요하다.
