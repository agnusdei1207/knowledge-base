+++
title = "270. 시계열 데이터베이스 IoT 모니터링 저장 (Time Series Database InfluxDB Prometheus)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IoT/모니터링 데이터는 *고정 스키마의 append-only 시계열 시계열(Time-Series)* 이므로, 관계형 DB의 B-Tree 인덱스 비용을 회피하기 위해 **LSM-Tree 기반의 시계열 전용 스토리지 엔진**(InfluxDB TSM, Prometheus TSDB)이 필수적이며, **라벨/태그 기반의 다차원 인덱싱과 다운샘플링·리텐션 정책**으로 디스크 I/O와 압축률을 극대화하는 것이 핵심이다.
> 2. **가치**: 동일한 자원 대비 RDBMS 대비 **쓰기 처리량 10~100배**(Prometheus 공식 벤치마크 기준 초당 수백만 샘플 흡수), 8~16byte 정수 시계열의 **Gorilla/DoubleDelta 압축률 90% 이상**, 리텐션 정책 적용 시 **Hot/Warm/Cold 3-Tier 스토리지 자동 계층화**를 통해 1PB/년 규모 데이터의 TCO를 1/5 수준으로 절감 가능하다.
> 3. **판단 포인트**: **InfluxDB는 Push 방식(InfluxDB Line Protocol/HTTP/UDP)** 으로 에이전트 친화적이며 IoT 게이트웨이·금융 틱 데이터에 강하고, **Prometheus는 Pull 방식(OpenMetrics over HTTP)** 으로 서비스 디스커버리·알erting 생태계가 견고하여 쿠버네티스·마이크로서비스 모니터링에 최적이다. 따라서 "**단일 노드 단기 리텐션(<30d)은 Prometheus, 장기간 리텐션+복잡 분석은 InfluxDB+Telegraf, 양방향 통합은 Remote Write**"로 아키텍처를 분기하는 것이 기술사적 핵심 판단이다.

---

## Ⅰ. 개요 및 필요성

전통적인 RDBMS(예: MySQL InnoDB)는 데이터 1건 insert 시 B-Tree 리프 노드 분할·로그 파일 동기화(fsync)·이차 인덱스 갱신이 발생하여 초당 1만~3만 row 수준에서 디스크 IOPS가 포화된다. 반면 IoT/모니터링 워크로드는 **시간이 PK에 가까울 정도로 카디널리티가 낮고(예: `cpu_used,host=web01`)** 데이터가 1차원적으로 append된다는 특징이 있다. 이러한 워크로드에 RDBMS를 그대로 적용하면 인덱스 크기 비대화, 압축 부재, 시간 범위 질의의 full-scan이 발생하여 운영 비용이 기하급수적으로 증가한다. 시계열 데이터베이스(TSDB)는 이를 해결하기 위해 (1) **시간·태그 복합 인덱스를 메모리·디스크 하이브리드로 분리**하고, (2) **블록 단위 압축(Block-Level Compression)·머지 컴팩션**을 적용하며, (3) **시계열 함수·리텐션·다운샘플링을 데이터베이스 커널 차원**에서 제공한다.

```text
[기존 RDBMS vs TSDB 워크로드 비교]

RDBMS (MySQL/PostgreSQL)                TSDB (InfluxDB / Prometheus)
+---------------------------+           +---------------------------+
|  App -INSERT--> Table      |           |  Agent -Line/Pull--> TSDB  |
|  +----------------------+ |           |  +----------------------+  |
|  | B-Tree (Clustered)   | |           |  | TSM/Block Index      |  |
|  | +----++----++----+   | |           |  | +----++----++----+   |  |
|  | | 1  || 2  || 3  |...| |           |  | |sh1 ||sh2 ||sh3 |...|  |  |
|  | +----++----++----+   | |           |  | +----++----++----+   |  |
|  +----------------------+ |           |  |  <- WAL / Mem Table ->  |  |
|  Indexes: PK + 3 sec.idx  |           |  |  <- Compaction   ->     |  |
|  Avg insert: 10k rows/s   |           |  +----------------------+  |
|  Disk: 1B row ≈ 120GB     |           |  Avg insert: 500k+ samples/s|
+---------------------------+           |  Disk: 1B sample ≈ 4~8GB   |
         ^                              |        (Δ-of-Δ + Gorilla)  |
         | 일반 트랜잭션 OLTP            +---------------------------+
         |                                     ^
         +--------- 용도 부적합 -----------------+
                        시계열 워크로드
```

시계열 워크로드의 4대 특징은 (1) **쓰기 95% : 읽기 5%** 비율, (2) **최근 데이터에 대한 조회 집중**(Hot-Window), (3) **데이터는 한 번 쓰여지고 거의 갱신/삭제되지 않음**, (4) **질의 패턴이 시간 범위 + 그룹화 + 집계 함수**(rate, irate, derivative, mean_over_time)라는 점이다. InfluxDB와 Prometheus는 이 네 가지 가정을 하드웨어·알고리즘 차원에서 적극 활용한다. 결과적으로 같은 16코어 64GB RAM 노드에서 InfluxDB는 약 50만~100만 points/s, Prometheus는 약 100만 samples/s 흡수가 가능하며, MySQL 대비 약 **50~100배 쓰기 처리량과 1/10 수준의 디스크 사용량**을 보인다.

- **📢 섹션 요약 비유**: 일반 가계부(RDBMS)는 항목 하나 적을 때마다 항목을 가나다순으로 다시 정렬해 서랍에 넣는 셈이고, 시계열 DB는 **"날짜별 돈봉투"**에 통째로 던져 넣은 뒤, 필요할 때 봉투째 꺼내 계산하는 방식이라 속도 차이가 압도적이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

InfluxDB와 Prometheus는 **공통적으로 LSM(Log-Structured Merge) 계열의 시계열 스토리지**를 사용하지만 세부 구현은 상이하다. InfluxDB v1은 **TSM(Time-Structured Merge) 엔진**, v2/v3는 **InfluxDB IOx (Apache Arrow + Parquet 기반)** 으로 진화했고, Prometheus는 자체 **TSDB(on-disk) + Gorilla 압축 + WAL** 구조를 채택한다. 두 시스템 모두 **시계열(series)** 이라는 추상화 위에 **샘플(샘플 = 하나의 measurement/sample)** 을 append 한다.

```text
[InfluxDB v2 / Prometheus 공통 데이터 흡수-저장-질의 파이프라인]

   IoT/Service                               +---------------+
  +----------+                               |  Visualization|
  | Sensor   |  HTTP/UDP/Line Proto          |  (Grafana)    |
  | /App     | -------------+                +-------^-------+
  +----------+              v                         | PromQL/Flux
                       +-----------------+            |
                       |  Ingest Layer   |            |
                       |  - Influx: HTTP |            |
                       |  - Prom: Pull   |            |
                       +--------+--------+            |
                                v                     |
              +----------------------------------+    |
              |   In-Memory  (Hot / Write Path)  |    |
              |  • WAL (Prometheus Head Block)   |    |
              |  • Mem Table (InfluxDB Cache)    |    |
              |  • LastCache / MaxValue Tracker  |    |
              +-------------+--------------------+    |
                            v flush @ 2h or 1GB     |
              +----------------------------------+    |
              |   On-Disk (Cold / Read Path)     |    |
              |  • Block (.blk) + Index (.idx)  |    |
              |  • TSM File = Data+Meta+CRC      |    |
              |  • Tombstone (.tomb)             |    |
              +-------------+--------------------+    |
                            v compaction              |
              +----------------------------------+    |
              |   Compactor / Merger             |    |
              |  • L0->L1 merge                   |    |
              |  • 1h->3h->12h block rollup        |    |
              |  • Out-of-order sample repair    |    |
              +-------------+--------------------+    |
                            v                         v
              +----------------------------------------------+
              |   Query Engine  (InfluxQL/Flux / PromQL)     |
              |   • Parallel scan across shards              |
              |   • Vectorized execution (IOx)               |
              |   • Downsample: aggregateWindow / <aggr>_over_time
              +----------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :---|
| **Ingest Endpoint** (Line Protocol `: measurement,tag=v field=f 1717654321000000000`) | 데이터 흡수 게이트웨이 | HTTP/2 + TCP 8086, UDP 8089(구), `Content-Encoding: gzip` 권장, 단일 라인 64KB 제한, 라인의 정렬은 *시계열 키(measurement + sorted tag set) + 시간* 순으로 결정 |
| **Write-Ahead Log (WAL)** | 디스크 플러시 전 휘발성 보호 | Prometheus는 128MB 청크로 WAL 페이지 기록(mmap), 헤드 블록은 메모리+디스크 하이브리드. InfluxDB는 `wal/` 디렉터리에 `.wal` 파일로 WAL flush.  |
| **TSM / Block File** | 컬럼형 블록 단위 디스크 저장 | InfluxDB TSM = `[CRC | FooterIndex (BlockOffset+Size per Series) | Block Data]`, Block Data는 *float64/int64/bool/string* 컬럼 단위 인코딩(실제 값+CRC 8B). Prometheus는 Gorilla 인코딩(XOR-based) 사용 |
| **Time-Structured Index (`.idx`)** | 시계열 키 -> 블록 오프셋 매핑 | in-memory `series_id -> {min_time, max_time, offset, size}` 맵. Prometheus는 postings list(`tag=value -> series id`)를 머메마이드 컴팩션으로 디스크 인덱싱 |
| **Compactor** | 다단계 머지·다운샘플링 | Level 0(1h)->Level 1(3h)->Level 2(12h) 블록 롤업. InfluxDB는 Retention Policy 하위 `shard group duration` 단위로 자동 다운샘플링. Prometheus는 5분 윈도우 컴팩션(블록 3개->1개 머지) |
| **Query Engine** | PromQL / InfluxQL / Flux | PromQL: `rate(metric[5m])` 같은 벡터/스칼라 함수, 룰 평가기 분리. InfluxDB IOx: Apache Arrow RecordBatch 기반 SIMD 벡터화 실행, 멀티 코어 CPU 활용 90% 이상 |
| **Retention / DLP** | 데이터 수명 관리 | InfluxDB는 `retention_policy` 별 `duration`(예: 30d), Prometheus는 `--storage.tsdb.retention.time=30d` + `--storage.tsdb.retention.size=50GB` 이중 정책 |

**Gorilla / Delta-of-Delta 압축 상세**: Prometheus는 Facebook Gorilla(2015) 논문의 XOR 인코딩을 차용한다. 첫 샘플은 그대로 저장(8B), 이후 샘플은 (1) **시간 차이**를 *Delta-of-Delta*(이전 시간 차이의 변화량) 로 인코딩, (2) **값**을 *이전 값과 XOR* 한 결과의 leading/trailing zero count만 저장한다. 상온 모니터링 데이터(CPU 20~80%, 온도 18~26℃)의 경우 평균 **1.37 bytes/sample** 까지 압축되어, 일반적인 RDBMS 대비 12배 이상 압축률을 보인다. InfluxDB는 기본적으로 **단순 인코딩 + 블록 단위 Snappy/Zstd 압축**을 사용하며, 사용자가 직접 `tag-value` 카디널리티를 낮춰 압축률을 향상시켜야 한다.

**시계열 식별과 카디널리티 폭발(High Cardinality)** : 시계열 키 = `measurement` + `tag set`이다. 태그 카디널리티가 폭증(예: `user_id=1,000,000`를 태그로 사용)하면 series 수가 폭증하여 메모리·인덱스 비용이 천문학적으로 증가한다. InfluxDB는 `max-series-per-database=1,000,000` 같은 하드 리미트, Prometheus는 `Active Series` 메트릭으로 1M series 초과 시 경고를 발생시킨다. **카디널리티를 100만 이하로 유지**하는 것이 실무 운영의 황금률이다.

- **📢 섹션 요약 비유**: 시계열 DB는 **"도서관 사서"** 와 같다. 책(샘플)이 들어올 때마다 `책장 위치 표(인덱스)`를 갱신하는데, 일반 DB는 모든 책을 가나다순으로 재배치하지만 시계열 DB는 **"들어온 순서대로 큰 박스에 담고, 박스마다 라벨만 붙여 사물함에 넣는다."** 나중에 누가 "어제 오후 책들"을 찾으면 사물함 키만 열어 박스째 가져오면 끝이라 검색이 압도적으로 빠르다.

---

## Ⅲ. 비교 및 연결

InfluxDB와 Prometheus는 **사용자 인터랙션 모델**이 가장 큰 차이이며, 그 외 다운샘플링·생태계·리텐션 등에서 각각 강점을 보인다. 또한 **OpenTelemetry, Grafana, Kafka, M3DB, TimescaleDB** 등 주변 솔루션과의 연결을 통해 하이브리드 모니터링 스택이 구성된다.

| 구분 | **InfluxDB v2 / v3(IOx)** | **Prometheus v2.5x** |
| :--- | :--- | :--- |
| **데이터 수집 모델** | **Push 중심** (Telegraf, HTTP API, UDP, MQTT Plugin) — IoT·에이전트 환경 친화 | **Pull 중심** (HTTP scrape, `targets` 명시) + Pushgateway(배치/스크립트 한정) — K8s·서비스 디스커버리 친화 |
| **질의 언어** | InfluxQL(SQL-like) + **Flux**(함수형 파이프라인, v2) / **SQL**(v3 IOx) | **PromQL**(시계열 함수 특화, `rate/irate/increase/quantile/histogram_quantile`) |
| **저장 엔진** | TSM(v1) -> **IOx(Arrow+Parquet) v3** | 자체 TSDB + WAL, **Thanos/Cortex/Mimir** 확장으로 객체 스토리지 통합 |
| **태그/라벨 인덱싱** | Tag: 키=값 다차원, 자동 inverted index | Label: `__name__`, `job`, `instance` 등 사용자 정의 라벨, postings list 머메마이드 압축 |
| **다운샘플링/리텐션** | **Continuous Query(v1)** / **Task(v2)** / **Retention Policy 다중 계층** (예: `autogen` 7d raw, `downsample_1h` 90d, `downsample_1d` 5y) | Recording Rule(`avg:metric:5m` 형태로 사전 계산) + 외부 Remote Write로 다운샘플링 위임 |
| **알람/통합** | InfluxDB UI Alerting + **Grafana Alerting + Kapacitor** | **Alertmanager**(메일/Slack/PagerDuty/Webhook, 4단계 라벨 라우팅·inhibit·
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 270 / 300

<- **이전**: [269. 그래프 데이터베이스 관계 모델링 지식 그래프 (Graph Database Knowledge Graph Neo4j)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/269_graph_database/)
**다음**: [271. 피처 스토어 ML 특성 관리 재사용 (Feature Store ML Feature Management Feast)](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/271_feature_store/) ->

---
