---
sidebar:
  order: 125
  label: "125. 데이터 레이크 (Data Lake)"
  badge:
    text: "기출 • 30%"
    variant: note
title: "데이터 레이크 (Data Lake)"
date: "2026-08-13T23:13:00+09:00"
tags:
  - "notes-software"
weight: 125
extra:
  question_no: "125"
  source_status: "기출"
  source_history: "122회"
  priority: 30
  priority_note: "122회 기출, 원천 데이터 저장 구조의 기본"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Data Lake (데이터 레이크)**: 정형(Structured), 반정형(Semi-Structured), 비정형(Unstructured) 등 다양한 소스의 날것 그대로의 데이터(Raw Data)를 변환 없이 가성비 높은 클라우드 객체 스토리지(S3, GCS)에 대용량 수용하는 빅데이터 집적소.
- **Schema-on-Read**: 데이터 적재(Write) 시점에 스키마를 정의하지 않고 그대로 덤프 저장한 후, 쿼리 조회(Read) 시점에 쿼리 엔진이 분석 목적에 맞춰 읽기 스키마를 해석 및 정의하는 사상.
- **Data Swamp (데이터 늪)**: 메타데이터 관리, 거버넌스, 접근 권한 통제가 없는 상태로 데이터 레이크에 무분별하게 원천 파일만 덤프하여, 아무도 검색 및 재사용을 못 하고 썩어버리는 안티패턴.

</details>

- 정의/개념: 다양한 원천을 객체 스토리지에 보존하는 **데이터 레이크**
- 배경/필요성: 정형 스키마 선적용은 **비정형 수집•재처리 유연성** 제약

#### 한줄 요약

- 문서·로그·사진을 원본 상자째 창고에 보관하고, 꺼내 쓸 때 목적에 맞는 구조로 해석한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Schema-on-Read (읽기 시점 스키마 정립)**: 수집 적재 병목 0%, 자유로운 분석 확장성.
- **Multi-Format Ingestion**: CSV, JSON, Parquet, Image, Video, Audio 등 모든 형태 수용.

</details>

- **객체 스토리지**: 컴퓨팅과 분리된 탄력적 원천 보관
- **Schema-on-Read (읽기 시점 스키마 바인딩)** 및 다형성 데이터 수용
- **Data Catalog & Data Governance 필수 수용 (Data Swamp 방지)**

#### 한줄 요약

- 원천을 많이 모아도 위치·의미·품질·소유자를 찾을 카탈로그가 없으면 재사용할 수 없는 데이터 늪이 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Medallion Architecture (Bronze/Silver/Gold Zone)**: 데이터 레이크의 무분별 데이터 늪 화를 막기 위해 Raw(Bronze) $\rightarrow$ Cleaned(Silver) $\rightarrow$ Curated Business(Gold) 3단계 영역으로 데이터 정제 품질을 계층 분리한 아키텍처.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│               Data Lake Medallion Architecture & Catalog               │
├────────────────────────────────────────────────────────────────────────┤
│  Raw Data Source ──► [Bronze Zone (Raw Ingest)]                        │
│                           │ (ETL / Data Cleansing)                     │
│                           ▼                                            │
│                      [Silver Zone (Filtered & Joined)]                 │
│                           │ (Aggregated Business Logic)                │
│                           ▼                                            │
│                      [Gold Zone (Curated Business Analytics)]          │
├────────────────────────────────────────────────────────────────────────┤
│ Data Catalog & Governance: AWS Glue Data Catalog, Apache Atlas         │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 원천 데이터를 Bronze(Raw) 수집 후 Silver(정제) 및 Gold(분석마트) 3단계 영역으로 정제 관리하는 계층형 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| **Bronze Zone** | 원천 형식과 수집 메타데이터 보존 |
| **Silver Zone** | 중복•오류 정제와 표준 포맷 변환 |
| **Gold Zone** | 검증된 업무 집계•분석 데이터 제공 |
| **Data Catalog** | 스키마•위치•소유자•품질•리니지 관리 |

#### 한줄 요약

- 수집 에이전트, 객체 스토리지, 데이터 영역, 카탈로그, 처리 엔진으로 구성된다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Schema-on-Write (DW)**: 데이터를 적재하기 직전에 고정 테이블 스키마에 맞춰 변환하는 방식 (DW).
- **Schema-on-Read (Data Lake)**: 데이터 적재는 파일 그대로 하고, 쿼리 엔진(Athena) 실행 시점에 스키마를 입히는 방식.

</details>

```text
[원천 데이터]
      │
      ▼
1. 원본 객체 적재
      │
      ▼
2. 카탈로그 등록
      │
      ▼
3. 품질•스키마 검증
      │
      ▼
4. 정제 영역 승격
      │
      ▼
5. 조회 스키마 적용
```

### 동작 원리

1. **원본 객체 적재**: 소스•시간•버전 정보와 함께 보존
2. **카탈로그 등록**: 위치•형식•소유자•분류 메타데이터 생성
3. **품질•스키마 검증**: 계약•중복•누락•민감정보 검사
4. **정제 영역 승격**: 검증 수준별 Silver•Gold 데이터 생성
5. **조회 스키마 적용**: 목적별 스키마로 필요한 파티션 해석

#### 한줄 요약

- 원본을 그대로 보존하고 메타데이터·스키마·품질 검증 결과를 등록한 뒤 신뢰 수준별 데이터를 따로 공개한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **DW vs Data Lake**: DW는 고가의 정형 SQL 전용 스토리지, Data Lake는 저가의 가성비 무제한 정형/비정형 스토리지.

</details>

| 비교 항목 | Data Warehouse (DW) | Data Lake |
|:---|:---|:---|
| **수용 데이터 형태** | **정형 데이터 전용 (Structured SQL)** | **정형 + 반정형 + 비정형 (Images, Audio, Logs)** |
| **스키마 바인딩 시점**| **Schema-on-Write (적재 시점)** | **Schema-on-Read (조회 시점)** |
| **스토리지 특성** | 분석 엔진에 최적화된 관리 저장소 | **객체 스토리지 기반 컴퓨팅 분리** |
| **주요 활용 목적** | BI 리포트, 고성능 경영 지표 분석 | **AI/ML 머신러닝 학습 데이터, 대용량 원시 보존** |

#### 한줄 요약

- 레이크는 원본 객체 스토리지, 웨어하우스는 정형 분석 저장소, 레이크하우스는 객체 스토리지 위에 ACID 테이블 메타데이터를 결합한 구조이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Small File Problem in Lake**: S3 내부에 수KB 크기의 자잘한 파일이 수백만 개 쌓여 쿼리 탐색 시 목록 조회(ListBucket) 병목으로 속도가 폭락하는 안티패턴.

</details>

| 위험 요소 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 데이터 레이크가 **Data Swamp (데이터 늪)**으로 파행 | 메타데이터/소유자/보안 통제 없이 무분별 적재| **AWS Glue Data Catalog & IAM Access Policy 강제** |
| **Small File Problem (자잘한 파일)** | 초 단위 로그 파일이 수백만 개 무차별 누적 | **Spark/Compaction Job으로 128MB~512MB 파일 병합** |
| S3 Full Scan으로 쿼리 비용 폭발 | 파티셔닝 구조 없이 전수 파일 스캔 | **S3 Key를 `year=YYYY/month=MM/day=DD` 파티셔닝** |

> 사례: **카카오 / 당근마켓 AWS S3 Data Lake & Presto/Athena 기반 쿼리 엔진 운용**

#### 한줄 요약

- 날짜 서랍과 적당한 파일 묶음을 만들면 필요한 기간만 빠르게 읽을 수 있다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Data Lake 수립 기준(Data Lake Architecture Standards)**: S3 객체 스토리지, Medallion 3대 Zone 분리, Data Catalog 구축 및 Parquet/Athena 연동성에 의거한 체계.

</details>

- 원천 재사용은 **Data Lake**, 정형 지표 성능은 DW 선택

#### 한줄 요약

- 많이 모으는 것보다 무엇인지 찾고 믿고 다시 쓸 수 있게 관리하는 것이 핵심이다.
