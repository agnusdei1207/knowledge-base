---
title: "425. 클라우드 ETL 글루 데이터플로 데이터퓨전 (Cloud ETL Glue Dataflow DataFusion)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AWS Glue(서버리스 Spark 기반 ETL + Data Catalog), GCP Dataflow(Apache Beam 기반 통합 배치/스트리밍 처리), GCP DataFusion(CDAP 기반 시각적 파이프라인 설계) — 클라우드 네이티브 데이터 통합의 세 가지 대표 아키텍처 패턴(메타데이터 중심, 범용 스트리밍/배치, GUI 기반 워크플로우)
> 2. **가치**: 서버리스·자동스케일링으로 인프라 운영 부담 제거(Glue DPUs·Dataflow 워커 자동 스케일), 분당 수십만~수백만 이벤트 처리량(Streaming Engine), 코드 기반 IaC(Beam SDK·Glue Job Bookmark) + No-Code(Harness Studio) 양립으로 TTM 50% 이상 단축
> 3. **판단 포인트**: 코드 우선(Glue/Beam) vs. 비즈니스 사용자 친화(Cloud Data Fusion) 트레이드오프, 표준 처리 vs. EII(추상화) 선택, 완전 관리형(Glue/Dataflow) vs. GUI 중심(Data Fusion) 운영 거버넌스 설계, 클라우드 종속성 및 데이터 이그레스 비용(VPC 피어링, Private Service Connect) 검토

---

## Ⅰ. 개요 및 필요성

전통적인 온프레미스 ETL(Informatica PowerCenter, IBM DataStage 등)은 고가의 전용 어플라이언스, 라이선스 비용, 수동 스케일링, 그리고 비대한 운영 조직을 필요로 했다. 2010년대 후반 이후 데이터의 3V(Volume·Velocity·Variety)가 폭증하면서 기존 ETL은 다음과 같은 한계에 부딪혔다.

1. **운영 부담**: 클러스터 프로비저닝, 패치, 용량 계획, 야간 배치 윈도우 관리
2. **이중 모드 분리**: 배치(일 1회)와 스트리밍(실시간)이 별도 도구로 분리되어 운영 복잡도 증가
3. **메타데이터 분산**: 소스 DB, 타겟 DW, 카탈로그가 각기 다른 시스템에 흩어져 거버넌스 공백 발생
4. **확장성 한계**: 데이터 폭증 시 수직/수평 확장에 수일~수주 소요

AWS Glue(2017년 출시), Google Cloud Dataflow(2015년 GA), Google Cloud Data Fusion(2019년 GA, 원래 Qlikeleverage의 CDAP 기반)은 이러한 문제를 해결하기 위해 등장했다. 이 세 서비스는 각각 다른 철학으로 설계되었지만, **"서버리스 + 페타바이트급 + 표준 인터페이스(Apache Spark/Beam/CDAP)"** 라는 공통된 방향성을 갖는다.

```text
+------------------------------------------------------------------------------+
|                  클라우드 네이티브 데이터 통합의 진화 흐름                    |
+------------------------------------------------------------------------------+
|                                                                              |
|   [1990s]                  [2010s 초]                [2017~]                 |
|   전통 ETL          ->      Hadoop 기반 ETL      ->     클라우드 네이티브     |
|   (Informatica,             (Sqoop, Pig,            (Glue, Dataflow,         |
|    DataStage)                Hive, Spark)            DataFusion)            |
|                                                                              |
|   - 전용 하드웨어            - DIY 클러스터           - 완전 관리형           |
|   - 라이선스 과금            - YARN/Mesos 관리        - 사용량 과금           |
|   - 단일 실행                - 스크립트 중심           - 선언적/시각적         |
|   - 야간 배치                - 배치+조금의 스트림      - 배치+스트림 통합     |
|                                                                              |
|   +---------------------------------------------------------------------+    |
|   |   데이터 거버넌스(Glue Catalog, Data Catalog)                       |    |
|   |   v                               v                                  |    |
|   |   코드형 ETL                시각형 ETL                                |    |
|   |   (Glue Studio, Beam SDK)   (Data Fusion Wrangler/Harness)          |    |
|   |   v                               v                                  |    |
|   |   처리엔진 (Spark, Beam)   처리엔진 (Spark/MapReduce via CDAP)     |    |
|   |   v                               v                                  |    |
|   |   Lake/Warehouse (S3, BigQuery, Redshift, BigLake)                  |    |
|   +---------------------------------------------------------------------+    |
|                                                                              |
+------------------------------------------------------------------------------+
```

**기존 패러다임 vs. 클라우드 ETL 패러다임**

| 측면 | 온프레미스 ETL | 클라우드 ETL (Glue/Dataflow/DataFusion) |
| :--- | :--- | :--- |
| 인프라 | 물리/가상 서버 사전 구매 | 서버리스, 워크로드 기반 자동 할당 |
| 스케일링 | 사전 용량 계획, 야간 배치 | 자동 수평 스케일(수 초~수 분) |
| 라이선스 | 영구 라이선스 + 연간 유지보수 | 초/분/작업 단위 종량제 |
| 개발 도구 | GUI 클라이언트(Designer) | 웹 콘솔 + SDK(Python/Scala/Java) + 시각 캔버스 |
| 메타데이터 | 별도 리포지토리 | Glue Data Catalog / Dataplex / Data Catalog 통합 |
| 배포 방식 | WAR/EAR, JAR 수동 배포 | GitOps, Cloud Build/Composer/Airflow 연동 |
| 장애 대응 | 수동 재시작, 야간 재처리 | Job Bookmark(증분), 자동 재시도, DLQ |

- **📢 섹션 요약 비유**: 종이 도장기(전통 ETL)는 도장 찍을 때마다 잉크 칠하고 손으로 누르지만, 자동 복사기(클라우드 ETL)는 서류만 넣으면 알아서 복사·정리·바인딩까지 해준다. 도장 종류가 바뀌어도(코드 변경) 잉크통을 새로 살 필요가 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. AWS Glue

```text
+----------------------------------------------------------------------------+
|                           AWS Glue 아키텍처                                 |
+----------------------------------------------------------------------------+
|                                                                            |
|  +-----------------+  +-----------------+  +----------------------+        |
|  | Data Sources    |  | Data Targets    |  | 3rd Party Apps       |        |
|  | (S3, RDS, JDBC, |  | (S3, Redshift,  |  | (Athena, Redshift    |        |
|  |  DynamoDB, Kdf) |  |  Glue Table)    |  |  Spectrum, EMR)      |        |
|  +--------+--------+  +--------^--------+  +----------+-----------+        |
|           |                    |                       |                    |
|           v                    |                       v                    |
|  +------------------------------------------------------------------+      |
|  | ① Crawler (Classifier -> Schema Inference)                       |      |
|  |    - JSON/CSV/Parquet/ORC/Kafka 자동 스키마 추론                |      |
|  |    - 정규식 Grok 패턴, 커스텀 Classifier 등록 가능              |      |
|  |    - 주기적 실행(EventBridge Trigger)                            |      |
|  +------------------------+-----------------------------------------+      |
|                           v                                                |
|  +------------------------------------------------------------------+      |
|  | ② Data Catalog (Hive Metastore 호환 메타스토어)                  |      |
|  |    - Database / Table / Partition / Column statistics           |      |
|  |    - Lake Formation으로 세분화 권한(셀 단위/열 단위) 제어       |      |
|  |    - Apache Iceberg/Delta/Hudi 테이블 형식 지원(Glue 4.0+)       |      |
|  +------------------------+-----------------------------------------+      |
|                           | (메타 조회)                                     |
|                           v                                                |
|  +------------------------------------------------------------------+      |
|  | ③ Job System                                                    |      |
|  |   +-------------+ +-------------+ +--------------+              |      |
|  |   | Spark Job   | | Python Shell| | Streaming    |              |      |
|  |   | (Scala/Py)  | | Job         | | ETL (Kdf->Kdf)|              |      |
|  |   +------+------+ +------+------+ +------+-------+              |      |
|  |          +----------------+----------------+                     |      |
|  |                          |                                      |      |
|  |            +-------------+-------------+                        |      |
|  |            v             v             v                        |      |
|  |   +--------------+ +--------------+ +--------------+            |      |
|  |   | Glue Studio  | | Glue Code    | | Workflow     |            |      |
|  |   | (시각적 DAG) | | Generator    | | (Crawler+Job |            |      |
|  |   |              | | (PySpark생성)| |  Orchestr.)  |            |      |
|  |   +--------------+ +--------------+ +--------------+            |      |
|  +------------------------------------------------------------------+      |
|                           |                                                |
|                           v                                                |
|  +------------------------------------------------------------------+      |
|  | ④ Execution Layer (Serverless Spark)                            |      |
|  |    - DPU(worker + driver) 단위 과금                             |      |
|  |    - Glue 4.0: Spark 3.3, Iceberg/Z-Order, 100 DPU까지 자동     |      |
|  |    - Job Bookmark: 마지막 성공 commit 시점 추적 -> 증분 로드      |      |
|  +------------------------------------------------------------------+      |
|                                                                            |
|  부가 서비스: Glue Schema Registry(Avro/JSON Schema 버전 관리)             |
|              Glue DataBrew(시각적 데이터 프로파일링/정제)                    |
|              Glue Elastic Views(여러 스토어의 SQL 뷰 통합, 2022)            |
+----------------------------------------------------------------------------+
```

**AWS Glue 핵심 동작 원리**

1. **Crawler 스키마 추론 알고리즘**
   - 샘플링(기본 1MB 또는 행 1000개) -> 후보 타입 추정 -> Classifier로 후보 매핑
   - 사용자 정의 Classifier: Grok, XML, JSON Path, CSV 헤더 매핑
2. **Job 실행 모델**
   - DPU(Data Processing Unit) = 4 vCPU + 16GB RAM. `NumberOfWorkers × WorkerType(G.025X/2X) + Driver overhead`
   - `GlueVersion 4.0` 기준 Apache Spark 3.3, Ray 2.0(Glue for Ray) 지원
3. **Job Bookmark 메커니즘**
   - `bookmark_keys` 컬럼(예: timestamp) 또는 `range`/`partition_path` 기반으로 마지막 처리 지점 기록
   - `transformation_ctx` 파라미터로 Spark 작업 단위 commit
4. **Streaming ETL**
   - Kafka/Kinesis Data Streams -> Glue Streaming ETL -> S3/Redshift/Kinesis Data Firehose
   - 마이크로 배치(수 초 단위) 기반, Apache Spark Structured Streaming 사용

### B. Google Cloud Dataflow

```text
+----------------------------------------------------------------------------+
|                      GCP Dataflow 아키텍처                                |
+----------------------------------------------------------------------------+
|                                                                            |
|  +--------------------------------------------------------------------+   |
|  |   Apache Beam SDK (Java/Python/Go)                                |   |
|  |   - 통합 모델: ParDo, GroupByKey, Combine, Window, Flatten        |   |
|  |   - Windowing: Fixed, Sliding, Session, Global                    |   |
|  |   - Triggering: Event-time, Processing-time, Watermark 기반      |   |
|  |   - State API / Timer API (상태ful 처리)                          |   |
|  +-----------------------------+--------------------------------------+   |
|                                v                                          |
|  +--------------------------------------------------------------------+   |
|  |   Beam Pipeline Runner (Dataflow Runner)                          |   |
|  |   - Fusion Optimization: 인접 단계를 단일 stage로 묶음             |   |
|  |   - Auto-scaling: backlog/throughput 기반 worker 추가/제거         |   |
|  |   - Dataflow Shuffle: 원격 shuffle 서비스(작업자 재사용)          |   |
|  |   - Streaming Engine: 연속 처리(±100ms latency), 호스팅 Shuffle   |   |
|  +-----------------------------+--------------------------------------+   |
|                                v                                          |
|  +--------------------------------------------------------------------+   |
|  |   Worker Pool (Compute Engine VM, n1/n2 표준)                      |   |
|  |   - Streaming: 수명 장기화 + Streaming Engine 활성화               |   |
|  |   - Batch: 작업 완료 시 자동 종료                                  |   |
|  |   - Custom containers, FlexRS(선점형 VM)                          |   |
|  +-----------------------------+--------------------------------------+   |
|                                v                                          |
|  +--------------------------------------------------------------------+   |
|  |   I/O Connectors (Beam SDK I/O)                                   |   |
|  |   BigQuery, Pub/Sub, GCS, Kafka, Avro, Parquet, JDBC, Spanner,    |   |
|  |   Bigtable, Snowflake, MongoDB 등                                 |   |
|  +--------------------------------------------------------------------+   |
|                                                                            |
|  부가: Dataflow SQL(SELECT 기반 스트리밍 SQL), Prime(Pipeline Status,      |
|       Profiling, Recommended Alerts), Notebooks(JupyterLab 통합)          |
+----------------------------------------------------------------------------+
```

**Google Cloud Dataflow 핵심 원리**

1. **Apache Beam 통합 프로그래밍 모델**
   - ParDo = 사용자 정의 변환(DoFn), GroupByKey = 셔플, Combine = 결합, Window = 시간 윈도우
   - `Window.into(FixedWindows.of(Duration.standardMinutes(5)))`
   - `Watermark`: 이벤트 시간 진행을 추정, Trigger가 데이터 완성 시점을 판단
2. **Fusion & 자동 최적화**
   - 여러 ParDo를 하나의 직렬 실행 가능한 stage로 융합 -> 셔플 경계 최소화
   - 자동 코드 생성으로 직렬화/역직렬화 비용 절감
3. **Dataflow Shuffle / Streaming Engine**
   - 작업자 로컬 디스크 대신 원격 shuffle 서비스(워크로드와 분리) -> worker 재시작 비용 절감
   - Streaming Engine 활성화 시: <100ms p99 지연, 정확한 exactly-once
4. **자동 스케일링 알고리즘**
   - Horizontal Autoscaling: 병목 단계의 worker 수를 throughput/backlog 기반으로 조정
   - Vertical Autoscaling: 작업자당 처리 능력도 동적 조정(2023 GA)

### C. Google Cloud Data Fusion

```text
+----------------------------------------------------------------------------+
|                  Google Cloud Data Fusion 아키텍처                        |
+----------------------------------------------------------------------------+
|                                                                            |
|  +--------------------------------------------------------------------+   |
|  |  Web UI (CDAP Hue 기반 시각 캔버스)                                |   |
|  |   - Wrangler: 노코드 데이터 정제/프로파일링                       |   |
|  |   - Pipeline Studio: 노드 드래그앤드롭                            |   |
|  |   - Studio 7.0+: AI 기반 추천(Schema Discovery, Auto-Mapping)     |   |
|  +-----------------------------+--------------------------------------+   |
|                                v                                          |
|  +--------------------------------------------------------------------+   |
|  |  CDAP (Cask Data Application Platform) 엔진                       |   |
|  |   - 추상화된 노드 플러그인: Source, Transform, Sink, Action, Spark |   |
|  |   - MapReduce/Spark/Twill 런타임 추상화
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 425 / 800

<- **이전**: [424. 클라우드 스트리밍 카프카 Kinesis 플링크](/studynote/13_cloud_architecture/06_exam_summary/424_cloud_streaming_kafka_kinesis_flink/)
**다음**: [426. 클라우드 ML 세이지메이커 버텍스 AI](/studynote/13_cloud_architecture/06_exam_summary/426_cloud_ml_sagemaker_vertex_ai/) ->

---
