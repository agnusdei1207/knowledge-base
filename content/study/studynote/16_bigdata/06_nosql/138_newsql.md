+++
weight = 138
title = "138. NewSQL — CockroachDB/TiDB/YugabyteDB SQL+수평확장+ACID"
date = "2026-04-21"
[extra]
categories = "studynote-bigdata"
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: NewSQL은 전통 RDBMS의 ACID([[193_atomicity_all_or_nothing|Atomicity]], [[194_consistency_database_integrity|Consistency]], [[195_isolation_concurrency_control|Isolation]], [[196_durability_permanent_storage|Durability]]) 보장과 SQL 인터페이스를 유지하면서 [[035_nosql|NoSQL]] 수준의 수평 확장([[202_scale_out_distributed_horizontal_expansion|Scale-Out]])을 동시에 달성하는 차세대 [[136_variance|분산]] [[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]]다.
- **가치**: 기존 RDBMS 앱을 최소 코드 변경으로 글로벌 [[136_variance|분산]] 환경에 마이그레이션할 수 있으며, NoSQL로 전환 시 포기해야 했던 [[521_join|JOIN]]·[[191_transaction_concept_states|트랜잭션]]·[[072_foreign_key_fk|외래 키]]를 그대로 활용한다.
- **판단 포인트**: [[327_hint_handoff|OLTP]] 워크로드에서 단일 지역 규모를 초과하거나 [[100_multi_region_deployment_pipeline_disaster_recovery|멀티 리전]] 강한 [[194_consistency_database_integrity|일관성]]이 필요할 때 NewSQL이 최적이며, 분석([[316_olap|OLAP]]) 위주는 별도 [[209_data_warehouse_schema_on_write|데이터 웨어하우스]]와 병행해야 한다.

---

## Ⅰ. 개요 및 필요성

### [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] 등장 배경

```text
RDBMS 한계 vs NoSQL 트레이드오프:

┌─────────────────────────────────────────────────────────┐
│  RDBMS (Oracle, PostgreSQL)                             │
│  ✅ ACID 트랜잭션  ✅ SQL  ✅ JOIN                       │
│  ❌ 수직 확장 한계  ❌ 샤딩 복잡성  ❌ 멀티 리전 쓰기     │
└─────────────────────────────────────────────────────────┘
                        ↓ 부족한 것
┌─────────────────────────────────────────────────────────┐
│  NoSQL (Cassandra, MongoDB)                             │
│  ✅ 수평 확장  ✅ 멀티 리전  ✅ 높은 가용성               │
│  ❌ 완전한 ACID  ❌ JOIN  ❌ 복잡한 쿼리                  │
└─────────────────────────────────────────────────────────┘
                        ↓ 해결책
┌─────────────────────────────────────────────────────────┐
│  NewSQL                                                 │
│  ✅ ACID 트랜잭션  ✅ SQL  ✅ JOIN                       │
│  ✅ 수평 확장  ✅ 멀티 리전  ✅ 고가용성                  │
└─────────────────────────────────────────────────────────┘
```

### 대표 [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] 솔루션

| 솔루션 | SQL 호환 | [[011_consensus_algorithm|합의 알고리즘]] | 특화 기능 |
|:---:|:---:|:---:|:---|
| **[[292_etl_process|CockroachDB]]** | PostgreSQL | [[259_raft_paxos|Raft]] | 지역 [[179_table_partitioning_concept|파티셔닝]], 서바이벌 목표 |
| **[[293_elt_process|TiDB]]** | MySQL | [[259_raft_paxos|Raft]] (TiKV) | [[294_oltp_vs_olap|HTAP]](TiFlash), [[531_cloud_native_architecture|클라우드 네이티브]] |
| **YugabyteDB** | PostgreSQL + [[541_cassandra|Cassandra]] CQL | [[259_raft_paxos|Raft]]/Paxos | DocDB 스토리지, [[191_oss_license_compliance|오픈소스]] |
| **Google Spanner** | SQL | TrueTime + Paxos | 글로벌 [[194_consistency_database_integrity|일관성]], 완전 관리형 |
| **VoltDB** | SQL | 없음(단일 노드 ACID) | [[148_5g_embb_urllc_mmtc|초고속]] 인메모리 [[327_hint_handoff|OLTP]] |

📢 **섹션 요약 비유**
> NewSQL은 오프로드 기능을 탑재한 고급 세단과 같다. 도심([[327_hint_handoff|OLTP]])에서는 고급 세단(ACID + SQL)처럼 편안하게 달리고, 산길(대규모 [[136_variance|분산]] 환경)에서도 SUV(수평 확장)처럼 거침없이 주행한다. 이전에는 도심용 세단과 산악용 SUV 중 하나를 선택해야 했다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [[292_etl_process|CockroachDB]] 아키텍처

```text
┌─────────────────────────────────────────────────────────────┐
│              CockroachDB 분산 아키텍처                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │             SQL Layer (모든 노드에서 실행)             │   │
│  │  PostgreSQL 프로토콜 → SQL 파싱 → 실행 계획            │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          Distribution Layer                         │   │
│  │  트랜잭션 코디네이션, 범위(Range) 기반 라우팅            │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Replication Layer (Raft 합의)               │  │
│  │  Range(64MB) 단위 복제 → Raft 그룹 → 과반수 쓰기 확인   │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Storage Layer (Pebble/RocksDB)              │  │
│  │  MVCC 기반 키-값 저장, 타임스탬프로 버전 관리            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  지역 파티셔닝:                                               │
│  PARTITION BY LIST (region) → KR 데이터 → 서울 DC           │
│  → 데이터 주권(Data Sovereignty) 준수                         │
└─────────────────────────────────────────────────────────────┘
```

### [[293_elt_process|TiDB]] [[294_oltp_vs_olap|HTAP]] (Hybrid Transactional/Analytical Processing) 아키텍처

```text
┌──────────────────────────────────────────────────────────────┐
│                  TiDB HTAP 아키텍처                           │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                    TiDB (SQL Layer)                    │  │
│  │            MySQL 호환 SQL 파서 + 옵티마이저              │  │
│  └────────────────────────────────────────────────────────┘  │
│            │ OLTP 쓰기              │ OLAP 분석               │
│            ↓                        ↓                        │
│  ┌──────────────────┐    ┌────────────────────────────────┐  │
│  │  TiKV (행 기반)  │    │    TiFlash (컬럼 기반 복제)     │  │
│  │  Raft 합의       │───→│    실시간 동기화                │  │
│  │  OLTP 최적화     │    │    OLAP/집계 최적화             │  │
│  └──────────────────┘    └────────────────────────────────┘  │
│                                                              │
│  * TiSpark: TiKV/TiFlash에 직접 접근하는 Spark 커넥터         │
│  * 데이터 이동 없이 실시간 OLTP+OLAP 동시 처리                 │
└──────────────────────────────────────────────────────────────┘
```

### [[259_raft_paxos|Raft]] [[011_consensus_algorithm|합의 알고리즘]] 개요

```text
Raft 합의 과정 (쓰기 확인):

1. 클라이언트 → Leader에게 쓰기 요청
2. Leader → 모든 Follower에게 로그 복제 요청
3. 과반수(Quorum) 응답 수신
4. Leader가 Commit 확인 → 클라이언트에 응답
5. 비동기로 남은 Follower에 Commit 전파

특징:
  - 리더 선출: 타임아웃 기반 투표
  - 강한 일관성: Leader만 읽기/쓰기 처리
  - 로그 복제: 엄격한 순서 보장
```

📢 **섹션 요약 비유**
> [[259_raft_paxos|Raft]] 합의는 의장(Leader)이 [[216_progress_in_synchronization|진행]]하는 회의 의결과 같다. 의장이 안건을 내면 과반수가 "찬성"을 표하는 순간 가결되고, 의장이 쓰러지면 새 의장을 투표로 선출한다. 모든 결정이 기록으로 남아 나중에 합류한 위원도 회의 내용을 정확히 따라잡을 수 있다.

---

## Ⅲ. 비교 및 연결

### Google Spanner의 TrueTime과 외부 [[194_consistency_database_integrity|일관성]]

```text
TrueTime API:
  TT.now() → [earliest, latest] 시간 구간 반환
  (GPS + 원자시계로 글로벌 불확실성 수 밀리초 이하)

외부 일관성(External Consistency):
  트랜잭션 T1이 커밋된 후 시작된 T2는
  항상 T1의 변경사항을 반드시 읽음

→ 분산 MVCC 타임스탬프 기반 직렬화 (Serializability)
→ 글로벌 선형화(Global Linearizability) 보장
```

### [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] vs RDBMS vs [[035_nosql|NoSQL]] 포지셔닝

| 기준 | RDBMS | [[035_nosql|NoSQL]] | [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] |
|:---:|:---:|:---:|:---:|
| SQL | ✅ 완전 | ❌/부분 | ✅ 완전 |
| ACID | ✅ | ❌/부분 | ✅ |
| 수평 확장 | ❌ 제한 | ✅ | ✅ |
| [[100_multi_region_deployment_pipeline_disaster_recovery|멀티 리전]] | ❌ | ✅ | ✅ |
| 기존 앱 호환 | 기준 | 재작성 필요 | 최소 수정 |
| 단순성 | 높음 | 중간 | 중간~낮음 |

📢 **섹션 요약 비유**
> NewSQL과 RDBMS의 [[083_relationship_in_er_model|관계]]는 전기차와 내연기관차의 [[083_relationship_in_er_model|관계]]와 같다. 전기차([[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]])는 기존 도로 인프라(SQL 생태계)를 그대로 이용하면서 새 엔진([[136_variance|분산]] [[259_raft_paxos|Raft]] 합의)으로 구동된다. 기름(수직 확장) 없이도 장거리(대규모 [[136_variance|분산]] 환경)를 달릴 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[292_etl_process|CockroachDB]] 지역 [[179_table_partitioning_concept|파티셔닝]] ([[809_data_sovereignty|데이터 주권]] 준수)

```sql
-- 테이블에 지역 컬럼 추가 + 지역별 파티셔닝
CREATE TABLE user_data (
    id        UUID DEFAULT gen_random_uuid(),
    region    STRING NOT NULL,
    user_info JSONB,
    PRIMARY KEY (region, id)
) PARTITION BY LIST (region) (
    PARTITION kr VALUES IN ('KR'),  -- 한국 데이터 → 서울 DC
    PARTITION us VALUES IN ('US'),  -- 미국 데이터 → 버지니아 DC
    PARTITION eu VALUES IN ('EU')   -- 유럽 데이터 → 아일랜드 DC
);

-- 각 파티션을 특정 지역 존에 고정
ALTER PARTITION kr OF TABLE user_data
CONFIGURE ZONE USING constraints='[+region=ap-northeast-2]';
```

### 기술사 [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] 도입 판단 기준

```text
NewSQL 도입 검토 기준:
  ① 기존 RDBMS 앱이 단일 노드 한계 도달
  ② 멀티 리전 쓰기 + 강한 일관성 동시 필요
  ③ GDPR 등 데이터 주권 규정 준수 필요
  ④ NoSQL 마이그레이션 비용이 너무 높음

계속 RDBMS 유지 기준:
  ① 단일 리전 + 현재 스케일로 충분
  ② 복잡한 분석 쿼리 비중이 높음
  ③ 팀의 NewSQL 운영 역량 부족
```

📢 **섹션 요약 비유**
> CockroachDB의 지역 [[179_table_partitioning_concept|파티셔닝]]은 "한국 고객 [[001_dikw_pyramid|데이터]]는 한국 서버에만"이라는 [[791_gdpr_eu|GDPR]]/[[783_pipa_korea|개인정보보호법]]을 DB 레벨에서 강제하는 것이다. 마치 한국 우편물이 반드시 한국 우체국을 통해서만 보관되도록 법적으로 강제하는 것처럼, [[001_dikw_pyramid|데이터]]가 지정한 지역 밖으로 나가지 않음을 보장한다.

---

## Ⅴ. 기대효과 및 결론

### 글로벌 [[090_service_kubernetes_network_load_balancing|서비스]] 마이그레이션 시나리오

```text
Before: 리전별 독립 PostgreSQL + 애플리케이션 레벨 샤딩
  문제: 리전 간 데이터 불일치, 크로스 리전 트랜잭션 불가,
        샤딩 코드 복잡성

After: TiDB/CockroachDB 글로벌 클러스터
  결과: 단일 SQL 엔드포인트, 자동 리전 간 복제,
        ACID 트랜잭션, 기존 앱 코드 90% 재사용
```

### 결론
NewSQL은 "SQL 또는 확장성" 이분법을 극복한 현대 OLTP의 새 표준이다. 특히 글로벌 [[090_service_kubernetes_network_load_balancing|서비스]]와 [[809_data_sovereignty|데이터 주권]] 규정이 중요한 엔터프라이즈 환경에서 RDBMS 마이그레이션 경로로 주목받는다. 기술사 시험에서는 **[[259_raft_paxos|Raft]] [[011_consensus_algorithm|합의 알고리즘]] 원리**, **[[294_oltp_vs_olap|HTAP]]([[293_elt_process|TiDB]] TiFlash)의 행/컬럼 이중 저장 구조**, **지역 [[179_table_partitioning_concept|파티셔닝]]과 [[809_data_sovereignty|데이터 주권]]**, **[[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] vs RDBMS vs [[035_nosql|NoSQL]] 포지셔닝**이 핵심 논점이다.

📢 **섹션 요약 비유**
> [[058_newsql_google_spanner_truetime_distributed_transaction|NewSQL]] 도입은 기존 아파트(RDBMS)를 허물지 않고 지하에 새 기초([[136_variance|분산]] [[259_raft_paxos|Raft]] 엔진)를 놓아 건물을 통째로 들어 올리는 리모델링이다. 입주자(애플리케이션)는 같은 집 구조(SQL)를 그대로 쓰면서, 건물이 갑자기 옆에 증축(수평 확장)되는 마법을 경험하게 된다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---:|:---:|:---|
| [[259_raft_paxos|Raft]] | [[011_consensus_algorithm|합의 알고리즘]] | [[136_variance|분산]] [[568_logs_distributed_logging_elk_fluentd|로그]] [[016_replication_factor|복제]]·리더 선출 |
| [[449_mvcc|MVCC]] | [[014_concurrency|동시성]] 제어 | 타임스탬프 기반 다버전 관리 |
| [[294_oltp_vs_olap|HTAP]] | 처리 모델 | [[191_transaction_concept_states|트랜잭션]]+분석 동시 처리 |
| TrueTime | Google 기술 | GPS 기반 글로벌 시간 [[212_synchronization_mechanisms|동기화]] |
| 지역 [[179_table_partitioning_concept|파티셔닝]] | [[809_data_sovereignty|데이터 주권]] | [[001_dikw_pyramid|데이터]] 저장 지역 강제 |


### 📈 관련 키워드 및 발전 흐름도

```text
[전통 RDBMS (MySQL/PostgreSQL) — ACID 보장, 수직 확장 한계]
    │
    ▼
[NoSQL (Cassandra / MongoDB) — 수평 확장·고가용성, 일관성 타협(BASE)]
    │
    ▼
[NewSQL (CockroachDB / TiDB / YugabyteDB) — ACID + 수평 확장, SQL 인터페이스 유지]
    │
    ▼
[분산 트랜잭션 프로토콜 (Raft / Paxos + 2PC) — 분산 환경에서도 직렬화 일관성 보장]
    │
    ▼
[HTAP (Hybrid Transactional/Analytical Processing) — 트랜잭션·분석을 단일 엔진에서 처리]
```
이 흐름은 RDBMS와 NoSQL의 양립 불가능해 보이던 확장성-[[194_consistency_database_integrity|일관성]] 트레이드오프를 NewSQL이 [[136_variance|분산]] [[011_consensus_algorithm|합의 알고리즘]]으로 해소하고, 나아가 HTAP으로 [[191_transaction_concept_states|트랜잭션]]과 분석을 통합하는 [[002_database_definition|데이터베이스]] 패러다임의 진화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. NewSQL은 슈퍼히어로 [[002_database_definition|데이터베이스]] — 기존 DB(RDBMS)의 정확함과 NoSQL의 힘을 동시에 가졌어요.
2. [[259_raft_paxos|Raft]] 합의는 학급 반장 선거와 같아요. 과반수가 찬성하면 결정이 확정되고, 반장이 자리를 비우면 바로 새 반장을 뽑아요.
3. TiDB는 [[327_hint_handoff|OLTP]](거래 처리)와 [[316_olap|OLAP]](통계 분석)을 같은 DB에서 동시에 할 수 있어서, 음식점에서 주문도 받고 매출 보고서도 실시간으로 뽑을 수 있는 것 같아요.
