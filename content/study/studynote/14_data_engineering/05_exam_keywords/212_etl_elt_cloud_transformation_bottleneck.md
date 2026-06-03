+++
weight = 212
title = "212. ETL vs ELT (Extract-Transform-Load vs Extract-Load-Transform) 클라우드 전이"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ETL(Extract, Transform, Load)은 중간 변환 서버에서 먼저 정제 후 DW에 적재하지만, ELT(Extract, Load, Transform)는 원본 데이터를 클라우드 DW에 먼저 적재 후 DW 내부의 막대한 컴퓨팅 파워로 변환한다.
> 2. **가치**: 클라우드 DW(Snowflake, BigQuery, Redshift)의 분리 스토리지-컴퓨팅 구조 덕분에 ELT는 변환 병목(Bottleneck)이 사라지고, dbt(Data Build Tool)로 SQL 기반 변환 파이프라인을 코드로 관리할 수 있다.
> 3. **판단 포인트**: 온프레미스·레거시 환경은 ETL이 여전히 적합하나, 클라우드 네이티브·비정형 대용량 데이터에는 ELT가 압도적으로 유리하다 — 변환 로직의 위치가 아키텍처 선택의 핵심이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 ETL의 탄생과 한계

ETL(Extract, Transform, Load)은 1970~80년대 온프레미스(On-Premise) 데이터 웨어하우스 시대에 탄생했다. 소스 시스템에서 데이터를 추출(Extract)하고, 중간 서버에서 정제·변환(Transform)한 뒤, 최종 DW에 적재(Load)하는 순서다.

```
┌───────────┐    ┌──────────────────────┐    ┌─────────────┐
│  소스 DB  │───►│  ETL 서버 (변환)     │───►│  DW/목적지  │
│  ERP/CRM  │    │  데이터 정제         │    │  Teradata   │
│  파일/API │    │  타입 변환           │    │  Oracle DW  │
└───────────┘    │  비즈니스 룰 적용    │    └─────────────┘
                 └──────────────────────┘
                   ↑ 병목 지점 (Bottleneck)
                   처리 용량 = ETL 서버 CPU/메모리
```

**ETL의 병목 문제**: 모든 변환이 중간 ETL 서버를 통과하므로, 데이터 볼륨이 늘어날수록 ETL 서버가 단일 장애점(SPOF, Single Point of Failure)이자 성능 병목이 된다.

### 1.2 클라우드가 바꾼 패러다임

클라우드 DW는 스토리지와 컴퓨팅을 분리하여, 컴퓨팅 노드를 탄력적으로 확장한다. 이 환경에서는 변환을 DW 내부에서 수행하는 것이 훨씬 효율적이다.

📢 **섹션 요약 비유**: ETL은 공장 밖 작업장에서 철을 깎아 완제품으로 만들어 공장에 들여놓는 방식이고, ELT는 철을 통째로 공장에 들여놓고 공장 안의 최신 자동화 설비로 가공하는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 ETL vs ELT 아키텍처 비교

| 항목 | ETL (Extract-Transform-Load) | ELT (Extract-Load-Transform) |
|:---|:---|:---|
| **변환 위치** | 중간 ETL 서버 (외부) | 목적지 DW 내부 |
| **적재 데이터** | 정제된 최종 데이터 | 원시(Raw) 데이터 |
| **스케일링** | ETL 서버 수직/수평 확장 필요 | DW 컴퓨팅 탄력적 확장 |
| **지연 시간** | 변환 완료 후 적재 → 지연 큼 | 즉시 적재 → 변환은 별도 |
| **원본 보존** | 변환 후 원본 불일치 발생 가능 | Raw 데이터 항상 보존 |
| **적합 환경** | 온프레미스, 레거시 DW | 클라우드 DW (Snowflake, BigQuery) |
| **대표 도구** | Informatica, Talend, SSIS | dbt, Spark SQL, BigQuery TRANSFORM |

### 2.2 ELT 상세 흐름

```
┌────────────┐   Extract   ┌──────────────────────────────────────┐
│  소스 시스템│──────────►│            클라우드 DW               │
│  MySQL/API │             │                                      │
│  S3/Kafka  │   Load      │  ┌──────────┐   Transform            │
│            │──────────►│  │ RAW 레이어│──────────────►  │
└────────────┘             │  └──────────┘                │       │
                           │                              ▼       │
                           │                    ┌──────────────┐  │
                           │                    │ STAGING 레이어│  │
                           │                    └──────┬───────┘  │
                           │                           │ dbt/SQL  │
                           │                           ▼          │
                           │                    ┌──────────────┐  │
                           │                    │ MART 레이어   │  │
                           │                    └──────────────┘  │
                           └──────────────────────────────────────┘
```

### 2.3 dbt (Data Build Tool)를 활용한 ELT

dbt(Data Build Tool)는 ELT의 Transform 단계를 SQL 파일과 YAML 설정으로 코드화하는 오픈소스 프레임워크다.

```yaml
# dbt 모델 예시: models/staging/stg_orders.sql
SELECT
  order_id,
  customer_id,
  CAST(order_date AS DATE)   AS order_date,
  amount / 100.0             AS amount_usd  -- 센트→달러 변환
FROM {{ source('raw', 'orders') }}
WHERE status != 'cancelled'
```

**dbt 장점**:
- SQL 기반이라 데이터 분석가도 변환 로직 작성 가능
- 계보(Lineage) 자동 추적 — 어떤 테이블이 어디서 왔는지 시각화
- 테스트(not_null, unique, accepted_values) 내장
- Git 기반 버전 관리로 CI/CD(Continuous Integration/Deployment) 파이프라인 통합

### 2.4 Apache Spark를 활용한 대규모 ELT

대용량 비정형 데이터의 경우 Spark가 ELT의 Transform 엔진으로 동작한다.

```python
# Spark ELT Transform 예시
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

spark = SparkSession.builder.appName("ELT-Transform").getOrCreate()

# RAW 데이터 로드 (Load 단계에서 이미 S3에 저장된 데이터)
raw_df = spark.read.parquet("s3://data-lake/raw/orders/")

# Transform: 타입 변환, 필터, 집계
transformed_df = (
    raw_df
    .withColumn("order_date", to_date(col("order_date_str")))
    .filter(col("amount") > 0)
    .groupBy("customer_id", "order_date")
    .agg({"amount": "sum"})
)

# 결과를 DW 또는 데이터 마트(Data Mart)에 저장
transformed_df.write.mode("overwrite").parquet("s3://data-lake/mart/daily_orders/")
```

📢 **섹션 요약 비유**: dbt는 DW 안에서 일하는 '정리 정돈 전문가'다 — 이미 창고에 들어온 물건들을 SQL이라는 도구로 분류하고, 어디서 왔는지 꼬리표까지 붙여준다.

---

## Ⅲ. 비교 및 연결

### 3.1 변환 병목 위치 이동의 의미

ETL에서 ELT로의 전환은 단순한 순서 변경이 아니라 **책임의 이동**이다.

```
ETL 시대:
  소스 ──► [ETL 서버가 모든 책임] ──► DW
           ↑ 병목, 단일 실패점

ELT 시대:
  소스 ──► DW RAW ──► [DW 컴퓨팅이 책임] ──► DW MART
                      ↑ 탄력적 확장, 원본 보존
```

### 3.2 데이터 메시(Data Mesh)와의 연계

현대 데이터 아키텍처에서 ELT는 데이터 메시(Data Mesh) 패턴과 결합된다. 각 도메인 팀이 자신의 RAW 데이터를 DW에 적재(Load)하고, 도메인별 dbt 프로젝트로 변환(Transform)하여 데이터 프로덕트(Data Product)를 생성한다.

### 3.3 Reverse ETL (역방향 ETL)

최근에는 DW에서 분석한 결과를 운영 시스템(CRM, 이메일 마케팅)으로 다시 내보내는 **Reverse ETL** 패턴도 주목받는다. Census, Hightouch 같은 도구가 이를 담당한다.

📢 **섹션 요약 비유**: ELT에서 dbt는 DW라는 거대 주방의 레시피 북이다 — 재료(Raw 데이터)는 이미 주방에 있고, 레시피(SQL 모델)만 바꾸면 언제든 새 요리(데이터 마트)를 만들 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 ETL vs ELT 선택 기준

```
데이터가 민감하고 정제 전 적재가 불가한가?
       ↓ YES
       ETL (금융·의료 컴플라이언스 환경)

       ↓ NO
클라우드 DW를 사용하고 대용량인가?
       ↓ YES
       ELT + dbt (BigQuery, Snowflake, Redshift)

       ↓ NO (온프레미스, 소규모)
       ETL (Informatica, Talend, SSIS)
```

### 4.2 ELT 적용 시 주의사항

| 항목 | 주의점 |
|:---|:---|
| **데이터 품질** | RAW 적재 후 변환 실패 시 오염 데이터가 DW에 체류 |
| **비용 관리** | 클라우드 DW 쿼리 비용 — 비효율 SQL이 과금 폭탄 |
| **보안** | 민감 데이터가 RAW 레이어에 노출 → 컬럼 마스킹 필수 |
| **거버넌스** | dbt Lineage + 데이터 카탈로그(Data Catalog)로 계보 관리 |

📢 **섹션 요약 비유**: ELT는 반죽(raw 데이터)을 그대로 냉장고에 넣고 나중에 요리하는 방식이라 편리하지만, 냉장고 안이 지저분해지지 않도록 정리 규칙(거버넌스)이 필요하다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 ELT 전환 효과

| 효과 | 정량적 지표 |
|:---|:---|
| **파이프라인 구축 속도** | 전통 ETL 대비 개발 기간 40~60% 단축 |
| **유연성** | 비즈니스 룰 변경 시 dbt 모델만 수정 (재ETL 불필요) |
| **비용** | ETL 전용 서버 운영 비용 제거 |
| **신뢰성** | RAW 보존으로 어떤 시점으로든 재처리 가능 |

### 5.2 결론 — 기술사 작성 포인트

기술사 답안에서는 **"변환 병목의 위치가 아키텍처 선택을 결정한다"**는 관점에서 서술해야 한다. ETL은 데이터 품질과 컴플라이언스 우선, ELT는 속도와 유연성 우선의 설계 철학이며, 현대 클라우드 환경에서는 ELT + dbt + 데이터 카탈로그의 조합이 표준 스택으로 자리잡고 있다.

📢 **섹션 요약 비유**: ETL에서 ELT로의 전환은 '문 앞에서 신발 청소 후 입장'에서 '신발 신고 입장 후 안에서 청소'로 바뀐 것이다 — 입장은 빠르지만 안을 깨끗하게 유지하는 규칙이 더 중요해졌다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| ETL 변환 도구 | Informatica / Talend / SSIS | 전통 온프레미스 ETL 도구 |
| ELT 변환 도구 | dbt (Data Build Tool) | SQL 기반 ELT Transform 프레임워크 |
| ELT 엔진 | Apache Spark | 대규모 분산 변환 처리 |
| 클라우드 DW | Snowflake / BigQuery / Redshift | ELT 변환을 내부에서 수행 |
| 데이터 계층 | RAW → STAGING → MART | ELT의 3단계 레이어 구조 |
| 역방향 | Reverse ETL | DW → 운영 시스템으로 역방향 이동 |

### 👶 어린이를 위한 3줄 비유 설명

1. ETL은 도서관에 책을 넣기 전에 밖에서 먼지를 털고 분류해서 넣는 방식이야.

### 📈 관련 키워드 및 발전 흐름도

```text
ETL: Extract → Transform → Load (DW 외부 변환)
    │ 클라우드 컴퓨팅 저렴화
    ▼
ELT: Extract → Load → Transform (DW 내부 변환)
    ├─► dbt: SQL 기반 변환 자동화
    └─► BigQuery · Snowflake 컴퓨팅 활용
    │
    ▼
실시간 ETL/ELT: Kafka + Flink 스트리밍 변환
```
2. ELT는 책을 일단 도서관에 다 가져다 넣고, 도서관 안에 있는 빠른 기계로 분류하는 방식이야.
3. 어느 게 더 좋냐고? 도서관(클라우드)이 크고 빠르다면 ELT가 훨씬 편리해 — 책을 기다리게 하지 않아도 되거든!
