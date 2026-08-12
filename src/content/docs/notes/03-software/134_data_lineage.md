---
sidebar:
  order: 134
  label: "134. 데이터 계보 (Data Lineage)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "데이터 계보 (Data Lineage)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 134
extra:
  question_no: "134"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "계보는 영향 분석•감사•품질 추적 핵심"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Data Lineage (데이터 계보)**: 소스 데이터베이스부터 최종 BI 대시보드 및 AI/ML 모델에 이르기까지, 데이터가 이동, 가공, 변환되는 전체 라이프사이클 흐름을 시각적인 방향성 그래프(DAG)로 추적하여 파이프라인 변경 영향도 분석(Impact Analysis) 및 데이터 장애 원인을 추적하는 기법.
- **OpenLineage**: Spark, Airflow, Flink 등의 파이프라인 프레임워크로부터 데이터 계보 이벤트를 자동 수집하는 표준 오픈소스 사상.
- **Column-Level Lineage (컬럼 레벨 계보)**: 테이블 단위 추적을 넘어, 특정 `sales_amount` 컬럼이 어떤 소스 테이블의 어느 컬럼들 연산(`price * qty`)으로부터 기인했는지 핀포인트 추적하는 정교한 계보.

</details>

- 정의/개념: 데이터의 최초 발생 원천부터 최종 집계 보고서까지의 흐름, 변환(Transformation) 파이프라인 및 의존성을 시각적 방향성 그래프로 추적 관리하는 메커니즘인 **Data Lineage**
- 배경/필요성: 소스 DB 컬럼 변경 시 연결된 100개 파이프라인 및 대시보드의 연쇄 장애 방지, 금융/의료 규제 준수(Compliance Audit) 수용 요구성

#### 한줄 요약

- 보고서 숫자가 어느 원료와 공정을 거쳐 만들어졌는지 보여 주는 추적 지도이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Impact Analysis (영향도 분석)**: 특정 소스 테이블 변경 시 하류(Downstream) 시스템의 영향을 1초 만에 시각적으로 파악.
- **Root Cause Analysis (원인 분석)**: 대시보드 지표 수치 파행 시 상류(Upstream) 연산 노드 오류 지점을 역추적.

</details>

- **End-to-End Pipeline Traceability (Upstream / Downstream 상하류 추적)**
- **Column-Level Fine-Grained Lineage (컬럼 레벨의 세밀한 핀포인트 매핑)**
- **Automated OpenLineage Parsing & Impact Analysis (자동화된 영향도 분석)**

#### 한줄 요약

- 설계 계보는 예정 노선, 실행 계보는 실제 이동 기록이며 둘 다 빠진 길이 없는지 확인해야 한다.

## Ⅲ. 구조 및 구성요소 (Data Lineage DAG 그래프 메커니즘)

<details><summary>핵심 용어</summary>

- **Upstream & Downstream**: 특정 데이터 노드를 기준으로 상류 원천 데이터를 Upstream, 하류 소비처 데이터를 Downstream이라 칭함.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Data Lineage Graph Architecture                 │
├────────────────────────────────────────────────────────────────────────┤
│ [Upstream Source DB] ──► [Spark ETL Job] ──► [Silver Delta Table]     │
│   • MySQL: orders         • Sql Parsing        • orders_cleaned        │
│                                                     │                  │
│                                                     ▼                  │
│ [Downstream BI Portal] ◄── [Trino View Engine] ◄── [Gold Sales Mart]   │
│   • Tableau Dashboard       • Column Aggregation  • sales_summary     │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터가 소스부터 마트, 쿼리 엔진, 최종 BI 포털로 이어지는 유기적 상하류 흐름 그래프.

| 구성요소 (Element) | 역할 및 기술 메커니즘 | 실무 핵심 이점 |
|:---|:---|:---|
| **Upstream Node** | **데이터가 유입되는 상류 원천 데이터셋 노드 (Input)** | 원천 장애 파악 |
| **Downstream Node** | **데이터를 최종 소비하는 하류 대시보드/ML 노드 (Output)**| 파급 효과 영향도 분석 |
| **Transformation Code**| **SQL `JOIN`, `GROUP BY` 구문 파싱하여 변환식 추적** | 컬럼 매핑 로직 시각화 |
| **OpenLineage Standard**| **Spark, Airflow, Dbt 연동으로 계보 이벤트 자동 송신** | 100% 수동 작업 자동화 |

#### 한줄 요약

- 보고서 숫자가 어떤 원료와 공정을 거쳤는지 보여 준다.

## Ⅳ. 흐름도 (Column-Level Lineage 핀포인트 추적 흐름)

<details><summary>핵심 용어</summary>

- **SQL AST (Abstract Syntax Tree) Parser**: SQL 문장을 파싱하여 어떤 컬럼이 결합(`col_A + col_B AS total`)되었는지 계보 노드로 분해.

</details>

```text
[Source: order_amount] ────┐
                           ├──► [SQL AST Parser] ──► [Target: total_sales = sum(order_amount - discount)]
[Source: discount] ────────┘
```

### 동작 원리

1. **SQL Parsing**: `dbt` 또는 Spark SQL 구문을 AST Parser가 읽어 컬럼 단위 매핑 관계 추출.
2. **Graph Storage**: Graph DB(Neo4j) 또는 OpenMetadata 카탈로그에 `order_amount -> total_sales` 엣지 기록.
3. **Impact Render**: `order_amount` 컬럼 타입 변경 시 `total_sales`를 소비하는 모든 대시보드에 경고 전파 (**Column-Level Lineage 완결**).

#### 한줄 요약

- 작업이 실제로 읽고 쓴 자료와 열 계산식을 운행 기록처럼 모아 관계 지도에 합친다.

## Ⅴ. 종류 및 비교 (Design-Time vs Runtime Lineage)

<details><summary>핵심 용어</summary>

- **Design-Time vs Runtime Lineage**: 설계 시점 계보는 코드/DDL 기반 예상 경로, 런타임 계보는 실제 실행 로그 기반 실제 가동 경로.

</details>

| 비교 항목 | Design-Time Lineage (설계 시점 계보) | Runtime Lineage (런타임 계보) |
|:---|:---|:---|
| **수집 원천** | **소스 코드, SQL 파일, DDL 명세서** | **Spark, Airflow 실제 실행 런타임 로그** |
| **장점** | 배포 전 사전 영향도 파악 가능 | **실제 실행된 100% 실체 데이터 흐름 보장** |
| **단점** | 동적 쿼리(`EXECUTE IMMEDIATE`) 미반영 위험 | 파이프라인이 실행되어야만 계보 생성 |
| **적용 시점** | CI/CD 배포 파이프라인 검증 | 실시간 관제 및 장애 원인 추적 |

#### 한줄 요약

- 공사 전 영향은 설계도, 사고 후 원인은 실제 운행 기록이 더 잘 보여 준다.

## Ⅵ. 실무 고려사항 및 대책 (Data Lineage 실무 3대 활용 대책)

<details><summary>핵심 용어</summary>

- **Lineage Disruption Danger**: 파이프라인 중간에 Python 스크립트나 외부 API호출이 섞여 계보 연결고리가 끊어지는 현상.

</details>

| 실무 난제 및 유스케이스 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Lineage Disconnect** | 외부 API나 수동 파이썬 코드로 연결고리 소멸| **OpenLineage Custom Emitter 에이전트 코드 이식** |
| **2. Impact Analysis** | 소스 DB 컬럼 `user_id` 삭제 예고 | **Lineage Downstream 탐색으로 파급 대시보드 3개 사전 조치**|
| **3. Root Cause Analysis** | CEO 보고서 수치가 전일 대비 -90% 급락 | **Lineage Upstream 역추적으로 3단계 전 Spark Job 에러 발견**|

> 사례: **토스 / 당근마켓 OpenLineage & OpenMetadata 기반 전사 Data Lineage 시각화**

#### 한줄 요약

- 열 하나를 바꾸기 전에 그 열을 쓰는 보고서와 작업을 찾아 고칠 순서를 정한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Data Lineage 수립 기준(Data Lineage Standards)**: Column-Level Lineage, OpenLineage 프레임워크, OpenMetadata 그래프 시각화 및 영향도 분석성에 의거한 체계.

</details>

- **Data Lineage 수립 기준**에 따라 전사 데이터 파이프라인 구축 시 **OpenLineage & Column-Level Data Lineage** 필수 수용

#### 한줄 요약

- 예쁜 지도가 아니라 빠진 길 없이 영향과 원인을 빨리 찾는 지도가 필요하다.
