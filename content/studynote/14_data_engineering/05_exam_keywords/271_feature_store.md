---
title: "271. 피처 스토어 ML 특성 관리 재사용 (Feature Store ML Feature Management Feast)"
date: "2026-05-09"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 피처 스토어(Feature Store)는 ML 파이프라인에서 **특성(Feature)의 등록(Registry) -> 변환(Transformation) -> 오프라인/온라인 서빙(Serving) -> 재사용(Reuse)** 을 통합 관리하는 중앙 집중형 데이터 플랫폼이며, Feast는 CNCF 인큐베이팅 단계의 오픈소스 구현체로 **Low-latency Online Store(Redis/DynamoDB)** + **Offline Store(BigQuery/Snowflake/Parquet)** 기반의 이중 저장소 아키텍처를 채택한다.
> 2. **가치**: 피처 정의-계산-서빙 로직의 일원화로 **Training-Serving Skew 제거**(일반적으로 15~40% 모델 정확도 손실 방지), 피처 재사용으로 **데이터 엔지니어링 중복 작업 60~80% 절감**, Point-in-Time Correctness 보장으로 시계열 누수(Leakage)로 인한 검증 신뢰도 붕괴를 차단한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 **(a) Online Store 선택**(Redis vs DynamoDB vs Bigtable - 일관성·지연시간·비용), **(b) Online-Offline Consistency 전략**(Materialization 주기 vs Streaming ingestion), **(c) Feature Engineering 위치**(ETL 전 단계 vs Feast On-Demand Transform), **(d) 멀티테넌시·거버넌스**(Feature Lineage, Access Control, PII 마스킹)이다.

---

## Ⅰ. 개요 및 필요성

전통적인 ML 운영 환경에서는 **"데이터 과학자 한 명 = 노트북 한 대"** 라는 말이 있을 정도로, 동일한 피처(예: `user_30d_purchase_count`)를 추천 시스템 팀, 사기 탐지 팀, 고객 이탈 예측 팀이 각자 Spark/Airflow로 재계산하면서 다음 4대 문제(TRAINING-SERVING SKEW, FEATURE DUPLICATION, INCONSISTENT COMPUTATION, NO REUSABILITY)가 만성적으로 발생한다.

특히 Production 환경에서 **모델 A는 Pandas로 집계**하고 **모델 B는 SQL로 집계**한 결과를 그대로 사용하면, 통계적 분포(평균, 분산, 백분위)가 미묘하게 달라져 모델은 **offline에서는 잘 맞는데 online에서는 정확도가 20~30% 급락**하는 현상이 발생한다. 여기에 **시계열 데이터의 미래 정보 누수(Leakage)** 문제는 `JOIN` 시점의 시점 정렬을 잘못하면 Backtest AUC 0.92 -> Production AUC 0.65 같은 참사를 일으킨다.

Feast(Feature Store)는 Gojek에서 2019년 시작되어 현재 **Linux Foundation / CNCF Sandbox**(2024 기준) 프로젝트로 운영되며, **Netflix, Uber, Tencent, LINE, 쿠팡** 등 대규모 트래픽 환경에서 검증된 오픈소스이다.

```text
+----------------------------------------------------------------------+
|         BEFORE Feature Store (분산된 피처 관리 - Chaos)              |
|                                                                      |
|   [DS Team A]              [DS Team B]              [DS Team C]      |
|   +----------+             +----------+             +----------+     |
|   |  Pandas  |             |   Spark  |             |    SQL   |     |
|   |  Sklearn |             |  PySpark |             |  Redshift|     |
|   +----+-----+             +----+-----+             +----+-----+     |
|        |                        |                        |          |
|        v                        v                        v          |
|   +----------+             +----------+             +----------+     |
|   | Ad-hoc   |             | Custom   |             | Jupyter  |     |
|   | Pipeline |             | Airflow  |             | Dump CSV |     |
|   +----+-----+             +----+-----+             +----+-----+     |
|        |                        |                        |          |
|        v                        v                        v          |
|   [API Server A]          [API Server B]          [API Server C]    |
|   (서로 다른 피처 계산 결과 -> Training-Serving Skew 빈번)            |
+----------------------------------------------------------------------+

                              ⬇️ Feature Store 도입

+----------------------------------------------------------------------+
|            AFTER Feature Store (Feast 기반 중앙 집중형)              |
|                                                                      |
|   [Data Engineers]  --->  +-----------------------------+             |
|   [DS Team A/B/C]   --->  |       Feast Registry        |             |
|   [Analysts]        --->  |   (FeatureView 정의/버전관리)|             |
|                          +----------+------------------+             |
|                                     |                                |
|         +---------------------------+---------------------------+    |
|         v                           v                           v    |
|  +-------------+            +-------------+            +-------------+|
|  |  Transform  |            |  Offline    |            |  Online     ||
|  | (On-Demand  |            |  Store      |            |  Store      ||
|  |  / Batch)   |            | (Parquet/   |            | (Redis/     ||
|  +-------------+            | BigQuery/   |            | DynamoDB)   ||
|                             | Snowflake)  |            +------+------+|
|                             +------+------+                   |      |
|                                    |                          |      |
|                                    v                          v      |
|                            +--------------------------------------+ |
|                            |   get_historical_features()           | |
|                            |   get_online_features()  (< 10ms)    | |
|                            +--------------------------------------+ |
+----------------------------------------------------------------------+
```

**기존 vs 신규 패러다임 핵심 차이:**
- **기존 (Pre-Feature-Store)**: 피처 = 코드 안에 묻혀있는 부산물(implicit artifact), 모델과 강결합
- **신규 (Feature-Store)**: 피처 = **1급 시민(first-class citizen)**, 재사용 가능한 데이터 자산, lineage 추적 가능, 카탈로그에서 검색·구독
- **DevOps -> MLOps 진화**의 핵심 축: "Feature as a Service" 개념 도입, DataOps와 MLOps의 가교 역할

- **📢 섹션 요약 비유**: 피처 스토어가 없는 ML 팀은 마치 **각자 다른 만능 레시피로 같은 김치찌개를 끓이는 요리사들**과 같습니다. 손님(모델) 입장에서는 같은 메뉴인데 맛이 다르고, 비법(피처 로직)이 주방장 머릿속에만 있어요. 피처 스토어는 **"공식 레시피북 + 중앙 배달 키친"**을 만들어 모든 셰프가 똑같은 맛을 보장받는 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Feast의 아키텍처는 크게 **5대 핵심 컴포넌트**로 구성된다: **① Registry ② Offline Store ③ Online Store ④ Feature Server(추후 Feast Feature Server) ⑤ Provider(추상화 계층)**. Feast 0.x -> 0.30+ -> 0.50+로 진화하면서 Go에서 Python(0.30+ 임시) -> 다시 Go 기반으로 재작성되어 **Type Safety**와 **CLI/SDK 분리**가 강화되었다.

```text
                  +-------------------------------------------+
                  |           Feast 구성 아키텍처              |
                  +-------------------------------------------+

  +------------------+       +------------------+
  |  Data Source     |       |  Data Source     |
  | (Parquet/        |       |  (Kafka / Kinesis)|
  |  BigQuery/       |       |   Streaming      |
  |  Snowflake)      |       |   Source         |
  +--------+---------+       +---------+--------+
           |                           |
           | Batch Apply               | Stream Apply
           v                           v
  +--------------------------------------------------+
  |              Feast Registry (Git/Local File)      |
  |  +------------------------------------------+     |
  |  |  Entity:  user_id, driver_id, product_id |     |
  |  |  FeatureView: user_30d_features_v3       |     |
  |  |    - features: [purchase_count, avg_amt] |     |
  |  |    - source: parquet://.../user.parquet  |     |
  |  |    - ttl: 86400s                          |     |
  |  |    - online: true                         |     |
  |  +------------------------------------------+     |
  +----------------------+---------------------------+
                         |  feast apply (메타 등록)
                         v
  +--------------------------------------------------+
  |                  Provider Layer                   |
  |   (Local / AWS / GCP / Azure / Snowflake Plugin) |
  +------+--------------------------------+----------+
         |                                |
   +-----v------+                  +-----v------+
   |  Offline   |                  |  Online    |
   |   Store    |                  |   Store    |
   |            |                  |            |
   | • BigQuery |                  | • Redis    |
   | • Redshift |                  | • DynamoDB |
   | • Snowflake|                  | • Bigtable |
   | • Parquet  |                  | • SQLite   |
   | • Trino    |                  | • Postgres |
   |            |                  |            |
   | (History/  |                  | (Low-Lat / |
   |  Training) |                  |  Inference)|
   +-----+------+                  +-----+------+
         |                                |
         | materialize()                  |
         | (incremental/                  |
         |  full)                         |
         +------------+    +--------------+
                      v    v
            +----------------------+
            |   Feast Client SDK   |
            |  (Python / Go / Java)|
            +----------+-----------+
                       |
        +--------------+--------------+
        v              v              v
  +---------+    +----------+    +----------+
  | Training|    | Inference|    | Online   |
  | Pipeline|    | Service  |    | App      |
  | (Spark) |    | (Tensor- |    | (Django) |
  |         |    |  Serving)|    |          |
  +---------+    +----------+    +----------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Entity** | 피처의 조인 키(Primary Key) 정의 | `Entity(name="user_id", value_type=ValueType.INT64)` 형태로 등록. 시계열 분석에서 `event_timestamp`와 함께 **Composite Key** 역할. Feast 0.30+ 에서는 Entity-FeatureView 분리 설계로 **N:M 관계**(여러 FeatureView가 동일 Entity 공유) 지원. |
| **FeatureView** | 동일 데이터 소스에서 파생된 피처 그룹의 논리적 단위 | `name`, `entities`, `schema`(필드 목록), `source`, `ttl`(예: `ttl=timedelta(hours=24)`), `online` 플래그로 구성. **Schema Evolution**을 위해 `name` 변경 시 신규 FeatureView 생성 권장(Immutable). |
| **Offline Store** | 학습/배치 추론용 대용량 시계열 데이터 보관 | BigQuery/Snowflake/Parquet/Redshift. `get_historical_features(entity_df, features)` 호출 시 **ASOF JOIN** 알고리즘으로 **Point-in-Time Correctness** 보장. SQL 엔진의 Window Function(`MAX_BY`, `LAST_VALUE`)을 push-down하여 **Distributed Computing** 활용. |
| **Online Store** | 실시간 추론용 저지연 Key-Value Store | Redis(권장, p99 < 5ms), DynamoDB(서버리스, IAM 통합), Bigtable(Google Cloud), Datastax(Cassandra 호환). `get_online_features(features=[...], entity_rows=[{"user_id": 1234}])` 호출 시 **Batch Read** 지원으로 100개 키를 한 번에 조회 가능. |
| **Registry** | 모든 FeatureView/Entity 메타데이터 저장 | Git(권장, Code-as-Config) 또는 Local File(`registry.db`). `feast apply` 시 YAML/Python 정의 파일을 읽어 **선언적 관리**. 변경 이력 추적(Versioning), RBAC 연동 가능. |
| **Materialization Engine** | Offline -> Online 데이터 동기화 | `feast materialize` 명령으로 **Incremental**(마지막 materialization 시점 이후) 또는 **Full** 모드 실행. Background Worker(Go daemon)가 주기적(예: 1시간) 실행. Push API(`feast push`)로 Streaming 즉시 반영. |
| **On-Demand FeatureView** | 추론 시점 Request Body에서 동적 피처 계산 | Python UDF 등록 -> Inference Service에서 `compute_features(request_dict)`로 즉시 계산. **Online Store 적재 불필요** -> 비용 절감. 변환 로직을 코드로 정의하고 `.feast_odfv` 캐싱 활용. |
| **Provider** | 클라우드 종속성 추상화 | `LocalProvider`, `AwsProvider`, `GcpProvider`, `AzureProvider`. 각 Provider는 해당 클라우드의 IAM/RBAC/네트워크 규칙 준수. |

### 핵심 메커니즘: Point-in-Time Correctness

시계열 피처 조회 시 발생하는 **Data Leakage** 방지 알고리즘은 다음과 같다:

```sql
-- Feast가 내부적으로 생성하는 ASOF JOIN 쿼리 (의사 코드)
SELECT
    entity_df.user_id,
    entity_df.event_timestamp,
    ANY_VALUE(feature_value) AS feature_value
FROM entity_df
ASOF JOIN (
    SELECT user_id, event_timestamp AS feature_ts, feature_value
    FROM feature_view_source
) features
ON entity_df.user_id = features.user_id
   AND features.feature_ts <= entity_df.event_timestamp  -- ⭐ 핵심: 미래 데이터 차단
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY entity_df.user_id, entity_df.event_timestamp
    ORDER BY features.feature_ts DESC
) = 1
```

**TTL(Tile-Based Materialization)** 정책:
- `ttl=86400`(24시간): 24시간 이전 데이터는 Online Store에서 자동 만료(EVICTION)
- Offline Store는 무제한 보관(또는 클라우드 스토리지 정책 따름)
- `feature_name` 단위 TTL도 가능(예: `purchase_count`만 1일, `user_lifetime_value`는 30일)

### Gojek/Feast 진화 히스토리 핵심 이벤트
- **v0.10(2020)**: Python 중심, 기본 Online Store = SQLite
- **v0.20(2022)**: Provider 패턴 정착, Snowflake/BigQuery Online Store 지원
- **v0.30(2023)**: **Go Engine** 실험적 도입, Type Safety 강화, Feature Server 분리 시작
- **v0.40+(2024)**: **Native Online Transform** 도입으로 Python UDF 의존도 축소, ODFV(Online-DFS Feature View) 통합

- **📢 섹션 요약 비유**: Feast의 Point-in-Time 조회는 **"학생 시절 시험 성적표"**를 떠올리게 합니다. 6월 30일 시험에 대한 성적은 7월 1일 이후의 성적표를 보면 안 되듯, **`event_timestamp` 이후의 데이터는 절대 보이지 않도록** 자동으로 필터링해줍니다. 그리고 **TTL**은 "1년 이상 된 기록은 자동 폐기"라는 도서관 규정과 같습니다.

---

## Ⅲ. 비교 및 연결

Feature Store 생태계는 **① 오픈소스(Feast, Hopsworks) ② 상용 SaaS(Tecton, Databricks, AWS SageMaker) ③ DIY(내부 구축)** 3가지 트랙으로 나뉜다. 기술사 시험 관점에서는 "왜 Feast를 선택했는가?", "상용 대비
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 271 / 300

<- **이전**: [270. 시계열 데이터베이스 IoT 모니터링 저장 (Time Series Database InfluxDB Prometheus)](/studynote/14_data_engineering/05_exam_keywords/270_time_series_database/)
**다음**: [272. 데이터 레이블링 어노테이션 능동 학습 (Data Labeling Annotation Active Learning)](/studynote/14_data_engineering/05_exam_keywords/272_data_labeling/) ->

---
