---
title: "421. 클라우드 데이터 레이크 S3 ADLS GCS (Cloud Data Lake S3 ADLS GCS)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 데이터 레이크는 **S3(객체 스토리지 + 11개 9s 내구성), ADLS Gen2(Hierarchical Namespace + ABFS 프로토콜), GCS(Strong Consistency + Autoclass)**를 기반으로, 정형/비정형/반정형 데이터를 **스키마-온-리드(Schema-on-Read)** 방식과 **메들리온 아키텍처(Bronze->Silver->Gold)**로 통합 저장·처리하는 분석 중심 스토리지 패러다임이다.
> 2. **가치**: 온프레미스 HDFS 대비 스토리지 비용 **70~90% 절감**(S3 Standard $0.023/GB vs Hadoop 클러스터 TCO), 컴퓨팅·스토리지 분리(Decoupling)로 **탄력적 스케일링**, ACID 트랜잭션(Delta Lake/Iceberg/Hudi) 기반 **레이크하우스** 구현으로 데이터 웨어하우스 대체 가능.
> 3. **판단 포인트**: 3대 객체 스토리지의 **일관성 모델**(S3: 2020년 strong consistency 도입, GCS: 최초 도입, ADLS: strong), **스토리지 클래스 선택**(Hot/Warm/Cold/Archive), **보안 모델**(IAM 정책, ABAC, RBAC, ACL), **파일 포맷**(Parquet, ORC, Delta, Iceberg), **다중 리전 DR 전략**이 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

전통적 데이터웨어하우스(EDW)는 **schema-on-write** 방식으로 ETL 파이프라인을 통해 정제된 데이터만 적재했기 때문에, **비정형 데이터(이미지, 로그, IoT 센서)**, **반정형 데이터(JSON, Avro, Parquet)**, **고속 유입 스트리밍 데이터**를 처리하는 데 근본적 한계가 있었다. 또한 온프레미스 Hadoop HDFS는 **NameNode 단일 장애점(SPOF)**, **용량 확장 시 수 일의 리밸런싱 시간**, **저장·컴퓨팅 강결합(tight coupling)**으로 인한 자원 비효율 문제가 상존했다.

2010년대 들어 **AWS S3**(2006 출시, 2020년 strong consistency 전면 도입), **Azure Data Lake Store Gen1**(2015) -> **ADLS Gen2**(2018, Blob Storage + Hierarchical Namespace 통합), **Google Cloud Storage**(2010, strong consistency 기본 제공)가 등장하면서, 무한 확장 가능한 **객체 스토리지 기반 데이터 레이크**가 새로운 표준으로 자리잡았다. 이러한 객체 스토리지는 **최종 일관성에서 출발해 strong consistency로 진화**했으며, **HTTP/REST API + 멀티파트 업로드 + SDK 기반 직접 접근**이 가능해 Hadoop, Spark, Trino, Databricks, Snowflake, BigQuery 등 다양한 컴퓨팅 엔진과 **loose coupling**으로 통합된다.

```text
[기존 Hadoop 데이터 레이크 vs 클라우드 데이터 레이크 비교]

  +----------- 기존 온프레미스 Hadoop 아키텍처 -----------+
  |                                                       |
  |  +------------+     +--------------------------+      |
  |  | NameNode   |----->|  HDFS DataNode × N       |      |
  |  | (메타)     |     |  - 디스크 직접 마운트      |      |
  |  | 단일SPOF   |     |  - 128MB/256MB 블록       |      |
  |  +------------+     |  - 리플리케이션 3x        |      |
  |        |            +--------------------------+      |
  |        v                                             |
  |  +------------------------------------+              |
  |  | MapReduce/YARN (저장+연산 결합)     |              |
  |  |  -> 야간 배치 한정, 자원 회수 어려움 |              |
  |  +------------------------------------+              |
  +-------------------------------------------------------+

  +----------- 클라우드 데이터 레이크 (S3/ADLS/GCS) ----------+
  |                                                          |
  |  +--------------+     +------------------------------+  |
  |  |   Ingest     |     |   Object Storage (무제한)    |  |
  |  |  - Kafka     |----->|  +------+------+------+      |  |
  |  |  - Kinesis   |     |  |Bronze|Silver| Gold |      |  |
  |  |  - Firehose  |     |  |(원천)|(정제)|(집계)|      |  |
  |  |  - Dataflow  |     |  |  Raw |Parquet| Delta|      |  |
  |  +--------------+     |  +------+------+------+      |  |
  |                       |   s3:// / abfss:// / gs://    |  |
  |                       |   11 9s 내구성, 무한 스케일   |  |
  |                       +------------------------------+  |
  |                              ^      ^      ^           |
  |              +---------------+------+------+---------+  |
  |              |    Compute Layer (Decoupled)           |  |
  |              |  Spark | Trino | Athena | BigQuery     |  |
  |              |  Databricks | Snowflake | EMR | ADF    |  |
  |              |  -> 오토스케일링, 종료 시 자원 해제       |  |
  |              +-----------------------------------------+  |
  +----------------------------------------------------------+
```

데이터 폭발(data explosion) 시대를 맞아, IDC는 2025년 전 세계 데이터가 **180ZB 이상**에 이를 것으로 예측하며, 그 중 **비정형 데이터가 80% 이상**을 차지한다. 클라우드 데이터 레이크는 이러한 페타~엑사바이트급 데이터에 대해 **스토리지는 영구 보존하면서 컴퓨팅만 탄력적으로 할당**하는 경제적 구조를 제공한다. 또한 **ACID 트랜잭션(Iceberg, Delta Lake, Hudi)**, **시간여행(Time Travel)**, **스키마 진화(Schema Evolution)**, **DML(DELETE/UPDATE/MERGE)** 지원으로 데이터레이크하우스(Lakehouse) 진화가 빠르게 진행되고 있다.

- **📢 섹션 요약 비유**: 기존 Hadoop이 **'자체 발전소 + 송배전망을 직접 짓는 방식'**이었다면, 클라우드 데이터 레이크는 **'국가 전력망(객체 스토리지)에 연결만 하면 전기(컴퓨트)를 자유롭게 켜고 끌 수 있는 방식'**이다. 발전소(스토리지)는 항시 가동되지만, 집(분석 워크로드)에 전기를 얼마나 쓸지는 실시간으로 조절 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 데이터 레이크의 핵심은 **객체 스토리지(Object Storage)**의 분산 아키텍처에 있다. 모든 객체 스토리지는 본질적으로 **키-값(Key-Value) 저장소** 위에 구현되며, **Flat namespace + Metadata index + Erasure Coding(EC)** 또는 **Replication**을 통해 11 9s(99.999999999%)의 내구성을 달성한다. 데이터는 **버킷(Bucket) / 컨테이너(Container)** 단위로 관리되며, 객체는 **Key(prefix + filename)**로 식별된다.

```text
[클라우드 데이터 레이크 내부 아키텍처 및 데이터 흐름]

                    +-------------------------------------+
                    |       다중 소스 데이터 인제스트       |
                    |  RDBMS | 로그 | IoT | API | 스트림   |
                    +----------------+--------------------+
                                     |
                  +------------------+------------------+
                  v                  v                  v
            +----------+       +----------+       +----------+
            | AWS S3   |       | ADLS Gen2|       |   GCS    |
            |          |       | (HNS ON) |       |          |
            | +------+ |       | +------+ |       | +------+ |
            | |Bronze| |       | |Bronze| |       | |Bronze| |
            | |/raw/ | |       | |/raw/ | |       | |/raw/ | |
            | +------+ |       | +------+ |       | +------+ |
            | |Silver| |       | |Silver| |       | |Silver| |
            | |/clea | |       | |/clea | |       | |/clea | |
            | +------+ |       | +------+ |       | +------+ |
            | | Gold | |       | | Gold | |       | | Gold | |
            | |/mart | |       | |/mart | |       | |/mart | |
            | +------+ |       | +------+ |       | +------+ |
            +----+-----+       +----+-----+       +----+-----+
                 |                  |                  |
                 |  +---------------v------------------v-------------+
                 +-->|  카탈로그 & 메타데이터 (Hive Metastore / Glue   |
                    |  Catalog / Unity Catalog / Polaris / BigLake)  |
                    +-----------------------+------------------------+
                                            |
                  +-------------------------+-------------------------+
                  v                         v                         v
          +---------------+         +---------------+         +---------------+
          |  SQL 엔진     |         |  ML/AI 엔진   |         |  BI/리포팅    |
          |  Athena       |         |  SageMaker    |         |  QuickSight   |
          |  Trino        |         |  Vertex AI    |         |  Power BI     |
          |  BigQuery     |         |  Databricks ML|         |  Looker       |
          |  Synapse      |         |  EMR + Spark  |         |  Tableau      |
          +---------------+         +---------------+         +---------------+
                  |                         |                         |
                  +-------------------------+-------------------------+
                                            v
                                    +---------------+
                                    | 거버넌스 계층  |
                                    | Lake Formation|
                                    | Purview       |
                                    | Data Catalog  |
                                    | (리인/ABAC/   |
                                    |  PII 마스킹)   |
                                    +---------------+
```

### 메들리온 아키텍처 (Medallion: Bronze -> Silver -> Gold)

| 계층 | 데이터 특성 | 포맷 | 처리 방식 | 예시 |
|:---|:---|:---|:---|:---|
| **Bronze (Raw)** | 원본 그대로, append-only | JSON, Avro, CSV, Parquet | 스키마 강제 없음, 중복 허용 | `s3://dl-bronze/orders/2024/01/01/*.json` |
| **Silver (Cleansed)** | 정제·중복제거·조인, schema 강제 | Delta/Iceberg/Parquet | CDC 적용, 데이터 품질 규칙 | `s3://dl-silver/orders_dedup/` |
| **Gold (Curated)** | 비즈니스 집계, KPI | Delta/Iceberg 컬럼형 | 집계·뷰, 머신러닝 피처 | `s3://dl-gold/dm_daily_sales/` |

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **S3 (Simple Storage Service)** | AWS의 객체 스토리지 (2006 출시, 사실상 업계 표준) | • **버킷(Bucket)** 단위, Key = `s3://bucket/prefix/object` <br>• 2020년 12월 **strong consistency** 전면 도입 (read-after-write 보장) <br>• **스토리지 클래스**: S3 Standard($0.023/GB) / Intelligent-Tiering(자동 계층) / Standard-IA / One Zone-IA / Glacier Instant(밀리초) / Glacier Flexible(분) / Glacier Deep Archive(12hr, $0.00099/GB) <br>• **S3 Express One Zone**(2023): 단일 AZ 기반 지연시간 10배v, 디렉토리 버킷 <br>• **S3 Tables**(2024): Apache Iceberg 네이티브, 자동 압축·통계 <br>• **Erasure Coding**: 99.999999999% (11 9s) 내구성 |
| **ADLS Gen2 (Azure Data Lake Storage Gen2)** | Azure의 데이터 레이크 전용 스토리지 | • **Blob Storage + Hierarchical Namespace(HNS)** 통합 (2018) <br>• **ABFS(Azure Blob File System) 드라이버**: `abfss://filesystem@account.dfs.core.windows.net/path` <br>• **HNS**: 디렉토리/파일 트리 구조, 디렉토리 단위 ACL(Access Control List) 지원 <br>• **스토리지 계층**: Hot(빈번, $0.0184/GB) / Cool(30일+, $0.01/GB) / Cold(90일+, $0.0036/GB) / Archive(180일+, $0.00099/GB) <br>• **Azure RBAC + POSIX ACL** 이중 보안 모델 <br>• **ADLS Gen1은 2024년 2월 서비스 종료**(Gen2로 통합) |
| **GCS (Google Cloud Storage)** | GCP의 객체 스토리지 (2010 출시) | • **버킷 단위**, 객체 키 = `gs://bucket/object` <br>• **strong consistency 기본 제공**(최초 출시부터) <br>• **스토리지 클래스**: Standard / Nearline(30일+) / Coldline(90일+) / Archive(365일+, $0.0012/GB) <br>• **Autoclass**(2022): 객체별 접근 패턴 자동 분석 후 클래스 이동 <br>• **Turbo Replication**(Dual-Region/Bi-Region): 동기적·지리적 RPO=0 가능 <br>• **Object Versioning, Object Hold, IAM Conditions(ABAC)** 지원 <br>• **Erasure Coding**: Reed-Solomon 코드 기반, 11 9s 내구성 |
| **Iceberg / Delta Lake / Hudi** | 오픈 테이블 포맷(Open Table Format) | • **Apache Iceberg**: Hive 메타스토어 비의존, hidden partitioning, snapshot 격리, **REST 카탈로그 표준화**(2024) <br>• **Delta Lake**: Databricks 주도, **txn log + 체크포인트**, Z-Order 클러스터링 <br>• **Apache Hudi**: **Upsert/Delete** 특화, Copy-on-Write vs Merge-on-Read <br>• 세 포맷 모두 **ACID 트랜잭션 + 스키마 진화 + 시간여행** 지원 |
| **메타데이터 & 카탈로그** | 데이터 발견·계보(lineage)·거버넌스 | • AWS: **Glue Data Catalog / Lake Formation** <br>• Azure: **Microsoft Purview (구 Data Catalog)** <br>• GCP: **Dataplex Universal Catalog / BigLake Metastore** <br>• 중립: **Apache Hive Metastore, Apache Polaris(incubating, 2024)** |
| **쿼리 엔진** | 데이터 레이크 직접 SQL 질의 | • **AWS Athena**(Trino/Presto 기반, 서버리스, $5/TB 스캔) <br>• **Azure Synapse Serverless SQL / Serverless Spark** <br>• **BigQuery**(GCS 네이티브, 컬럼형
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 421 / 800

<- **이전**: [420. 클라우드 비용 거버넌스 예산 알림](/studynote/13_cloud_architecture/06_exam_summary/420_cloud_cost_governance_budget_alerting/)
**다음**: [422. 데이터 레이크하우스 델타 아이스버그](/studynote/13_cloud_architecture/06_exam_summary/422_data_lakehouse_delta_iceberg_architecture/) ->

---
