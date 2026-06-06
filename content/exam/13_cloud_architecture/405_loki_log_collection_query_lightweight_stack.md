---
title: "Loki Log Collection Query Lightweight Stack"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Grafana Loki는 Prometheus에서 영감을 받은 **"Log를 위한 시계열 DB"** 철학으로, 로그 본문을 압축하여 Object Storage(S3/GCS/Azure Blob)에 저장하고, **Label(메타데이터) 인덱스만 별도 분리**하여 LogQL로 쿼리하는 수평 확장 가능한 로그 집계 시스템임.
> 2. **가치**: Elasticsearch 대비 **스토리지 비용 약 1/10~1/5, 인덱싱 CPU 1/20 수준**으로 절감되며(공식 Grafana Labs 발표), 단일 바이너리(Loki+Promtail)로 구성 가능하여 **k8s/Edge 환경에서 경량 운영**이 가능함. 1초에 1TB 로그 처리 가능한 수평 확장 구조.
> 3. **판단 포인트**: Full-text 검색 성능(ELK) vs 비용·단순성(Loki)의 트레이드오프, **Chunk 단위 Retention 정책과 Store-gateway 캐싱 전략**, Promtail vs Fluent Bit 에이전트 선택, Multi-tenancy 활성화 여부, **GELK↔Loki+Promtail+Tempo+Mimir** 관측성 스택 통합 판단이 핵심.

---

## Ⅰ. 개요 및 필요성

전통적인 로깅 스택(ELK: Elasticsearch+Logstash+Kibana)은 클러스터 운영 복잡도, JVM 메모리 오버헤드, Full-text 인덱스의 높은 디스크 사용량으로 인해 **소규모~중규모 MSA, Edge 컴퓨팅, IoT 환경**에서는 비용·성능 부담이 컸음. Kubernetes 환경에서 Pod 단위로 폭증하는 로그를 안정적으로 수집·보관하면서도 **Prometheus와 동일한 Label 기반 Mental Model**로 통합 관측성을 구현하려는 요구가 대두됨.

Grafana Labs는 2018년 **"Like Prometheus, but for logs"** 슬로건으로 Loki를 오픈소스 공개(CNCF Incubating 프로젝트, 2020년 기부). 2024년 기준 v2.9까지 출시되었으며, Grafana 10/11과의 완벽 통합, Alertmanager 연동, LogQL 파이프라인을 통한 메트릭 변환 기능을 제공함.

```text
+-------------------------------------------------------------+
|            기존 ELK 스택의 한계와 Loki 등장 배경             |
+-------------------------------------------------------------+
|                                                             |
|  [기존 패러다임: Full-text Index 중심]                       |
|  App --> Fluentd --> Logstash(parse/filter) --> Elasticsearch  |
|                                          (역색인/Inverted)  |
|                                          --> Kibana          |
|  문제점:                                                    |
|   • Elasticsearch JVM Heap = 로그량 비례 급증 (GB/일)       |
|   • Shard rebalancing 비용, Master 노드 SPOF                |
|   • Inverted Index 갱신 IO 병목 -> Write Throughput 저하     |
|   • Kibana Query는 풍부하지만 인프라 운영 난이도 ^           |
|                                                             |
|  [신 패러다임: Label Index + 압축 Chunk]                    |
|  App --> Promtail --> Distributor --> Ingester --> Object Store|
|                              (메모리)    (S3/GCS/Azure)     |
|                              +-> Querier <-- LogQL            |
|  장점:                                                      |
|   • 로그 본문 = gzip/zstd 압축, 원본 그대로 저장             |
|   • 인덱스 = {job, instance, pod, namespace, level} 등      |
|     라벨만 -> 색인 크기 MB/일 수준                           |
|   • Stateless Querier -> Read/Write 완전 분리, 수평확장 용이  |
+-------------------------------------------------------------+
```

Loki의 핵심 철학은 **"High Cardinality는 비싸다(High Cost)"**라는 인식에서 출발함. 사용자ID, IP, 요청ID 같은 비제한 차원(Unbounded Cardinality)을 라벨로 쓰면 안 되며, 이는 Prometheus의 Label 제약과 동일한 사고방식임. 결과적으로 인덱스 크기를 **로그 본문 대비 1% 미만**으로 유지하여 PB급 로그도 단일 Object Storage에 보관 가능.

- **📢 섹션 요약 비유**: ELK가 "모든 책의 첫 페이지부터 단어를 색인한 두꺼운 사전"이라면, Loki는 **"책장(Storage)에 책은 그대로 꽂아두고, 표지(Label)만 별도 색인 카드함에 정리"**해두는 도서관 시스템과 같음. 책을 찾을 땐 표지(라벨)로 빠르게 위치 파악, 내용은 펼쳐서 읽음.

---

## Ⅱ. 아키텍처 및 핵심 원리

Loki 아키텍처는 **Monolithic 모드(microservices=false)**와 **Microservices 모드** 두 가지로 나뉨. 경량 스택에서는 단일 바이너리(monolith)로 시작하다가, **일일 로그량 100GB 초과 또는 QPS 1,000 초과 시** 서비스 분리(ingester, querier, store-gateway 등)를 권장함. 컴포넌트 간 통신은 **gRPC** 기본, 외부 API는 **HTTP/REST**.

### 2.1 핵심 컴포넌트

```text
+----------------------------------------------------------------------+
|                Loki Lightweight Stack 상세 아키텍처                    |
+----------------------------------------------------------------------+
                            +--------------+
                            | Application  |
                            | (stdout/stderr)|
                            +------+-------+
                                   | /var/log/pods/*/*.log
                                   v
                       +----------------------+
                       |  Promtail / Fluent Bit|  <--- Edge Agent
                       |  (DaemonSet or Sidecar)|     (Service Discovery)
                       |   - Label 추출        |
                       |   - Pipeline stages   |
                       |   - 배치(batch_wait)  |
                       +----------+------------+
                                  | HTTP POST /loki/api/v1/push
                                  | (Protobuf/Snappy 압축)
                                  v
        +-----------------------------------------------------+
        |              LOKI  (Monolith or Microservices)        |
        | +-------------------------------------------------+ |
        | |            Distributor (Frontend)                 | |
        | |  • HMAC Tenants 인증, Ring Hash Sharding          | |
        | |  • Tenant Quota/Rate-limit 적용                  | |
        | |  • gRPC: 100 streams per request, snappy 압축    | |
        | +----------------------+---------------------------+ |
        |                        v                             |
        | +-------------------------------------------------+ |
        | |              Ingester (Stateful)                  | |
        | |  • 스트림(Stream) = {Labels} + Chunk Streams     | |
        | |  • 메모리 내 Chunk 생성 (1MB~1.5MB 기본)          | |
        | |  • WAL(Local BoltDB) -> 재시작 시 복구             | |
        | |  • chunk_id = (tenant, fingerprint, ts)          | |
        | |  • 주기적 flush(예: 2h) -> Object Storage          | |
        | +--------------+-----------------+-----------------+ |
        |                |                 |                   |
        |                v                 v                   |
        | +------------------+   +----------------------+    |
        | |  Object Storage  |   |   Index Store         |    |
        | |  (Chunks/Blobs)  |   |  (TSDB/BoltDBshipper) |    |
        | | • S3 / GCS / AZ  |   |  • 단일 인덱스 파일   |    |
        | | • MinIO(로컬)    |   |  • tsdb-shipper 권장   |    |
        | | • 압축: gzip/snappy/zstd |  • 멀티테넌트 분리  |    |
        | +------------------+   +----------------------+    |
        |                                                     |
        | +-------------------------------------------------+ |
        | |  Querier  <--- HTTP /loki/api/v1/query (LogQL)   | |
        | |  • In-memory merging + tail() 지원              | |
        | |  • LogQL parser -> AST -> Execution plan          | |
        | |  • 최근 데이터 = Ingester, 과거 = Store-gateway  | |
        | +-------------------------------------------------+ |
        |                                                     |
        | +-------------------------------------------------+ |
        | |  Query-frontend (선택)                           | |
        | |  • 쿼리 분할(split by day) + 병렬 실행            | |
        | |  • 결과 캐싱 (Redis/Memcached)                   | |
        | |  • 샘플링(샘플 500/1000)                         | |
        | +-------------------------------------------------+ |
        +-----------------------------------------------------+
                                   |
                                   v
                          +---------------+
                          |  Grafana UI   |
                          |  / Explore    |
                          |  / Dashboards |
                          |  / Alerting   |
                          +---------------+
```

### 2.2 LogQL 쿼리 언어

LogQL은 두 가지 쿼리 타입을 제공:

- **Log Query**: `{job="nginx"} |= "error" | json | duration > 5s`
- **Metric Query**: `rate({job="nginx", status="500"}[5m])`

| LogQL 연산자 | 의미 | 예시 |
|:---|:---|:---|
| `|=` | 포함(대소문자 무시) | `\|= "timeout"` |
| `!=` | 미포함 | `!= "healthcheck"` |
| `\|~` / `!~` | 정규식 매치/비매치 | `\|~ "user=\\d+"` |
| `\| json` | 파서 (json/logfmt/regex) | `\| json \| status_code="500"` |
| `\| line_format` | 출력 형식 변환 | `\| line_format "{{.msg}} - {{.status}}"` |
| `rate()` | 초당 카운트 | `rate({job="api"}[1m])` |
| `quantile_over_time()` | 히스토그램 | `quantile_over_time(0.95, {job="api"} \| unwrap latency[5m])` |

### 2.3 데이터 모델 및 저장 원리

**Stream** = 고유한 Label Set + 시간순 정렬된 Log Entry의 시계열. Promtail이 **fingerprint(MD5(sorted labels))**로 스트림을 식별하며, 동일 Label Set의 로그는 같은 스트림에 append됨.

**Chunk** = Ingester가 관리하는 1~1.5MB 단위 압축 블록. 2시간(기본 `chunk_idle_period`) 동안 라벨이 동일하면 묶이고, 시간이 지나거나 크기 임계 도달 시 **Flush**되어 Object Storage에 영구 저장됨. WAL(BoltDB)을 두어 Ingester 재시작 시 메모리 손실 방지.

### 2.4 핵심 파라미터

```yaml
# loki config 핵심 튜닝
limits_config:
  ingestion_rate_mb: 10           # Tenant당 초당 MB
  ingestion_burst_size_mb: 20
  max_query_parallelism: 32
  max_streams_per_user: 100000    # High Cardinality 방지
  retention_period: 744h          # 31일

ingester:
  chunk_idle_period: 2h           # 스트림 idle 임계
  chunk_target_size: 1572864      # 1.5MB
  max_chunk_age: 2h               # 강제 flush 주기
  wal:                            # Write-Ahead Log
    enabled: true
    dir: /loki/wal

storage_config:
  tsdb_shipper:
    active_index_directory: /loki/tsdb-index
  aws:
    s3: s3://ap-northeast-2/loki-chunks
    s3forcepathstyle: true

query_range:
  results_cache:
    cache: embedded-cache         # LRU 인메모리
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Promtail / Agent** | 로그 수집, 라벨 부착, 파이프라인 | `service.kubernetes` API로 Pod 메타데이터 자동 라벨링. `scrape_configs`는 File/Pod/Journal/Windows Event. Pipeline stages = `regex`, `json`, `template`, `metrics` |
| **Distributor** | 인증, 라우팅, 복제 | TenantID HMAC 검증 -> Ring(Consistent Hash) 기반 Ingester 3개 복제. gRPC Snappy 압축으로 10MB/req 제한 |
| **Ingester** | 스트림->Chunk 변환, 영구화 | 메모리에서 Fingerprint별 청크 생성, 주기 flush, WAL(BoltDB)로 재시작 보장, **Lifecycler**가 Ring 멤버십 관리 |
| **Object Storage** | Chunk 영구 저장 | S3 API 호환 (S3/GCS/Azure Blob/MinIO/IBM COS), gzip/chunks 압축, lifecycle 정책으로 Glacier 이동 |
| **Index Store** | 라벨-스트림-청크 매핑 | BoltDBshipper(단일 노드 OK) / TSDB(권장, v2.8+). 인덱스 = `{Tenant, Labels, Fingerprint, ChunkRefs}` |
| **Querier** | LogQL 실행 | `IngesterTail`(실시간) + `Store-gateway(과거)` 결합. Worker pool 동시성 제한 |
| **Query-Frontend** | 쿼리 분할/캐싱/샘플링 | `split_queries_by_interval: 24h`로 대용량 쿼리 병렬화, 1,000라인 샘플링 |
| **Store-Gateway** (MSA) | 인덱스/청크 캐시, 캐시 무효화 | Boltdb-shipper/TSDB 인덱스 캐싱, ingester의 6시간 미만 데이터는 querier가 직접 fetch |
| **Compactor** (MSA) | 중복 제거, Retention | 인덱스 머지, **Deletion Marker** 기반 GDPR/Retention 적용, TSDB 인덱스 컴팩션 |

- **📢 섹션 요약 비유**: Ingester는 **"우체국 집배함"** — 우편물(로그)이 들어오면 같은 주소(라벨)별로 쌓고, 우편함(Chunk)이 차면 택배 차량(Object Storage)에게 한꺼번에 인계함. 우편함 위치표(Index)는 색인 카드함에 따로 보관.

---

## Ⅲ. 비교 및 연결

### 3.1 로깅 스택 비교

| 구분 | **ELK (Elasticsearch + Logstash + Kibana)** | **EFK (Fluentd + ES + Kibana)** | **Grafana Loki + Promtail** |
|:---|:---|:---|:---|
| **인덱스 방식** | Inverted Index (Full-text) | Inverted Index (Full-text) | Label-based Index (메타데이터만) |
| **저장소** | 자체 JVM 노드 (디스크) | 자체 JVM 노드 (디스크) | Object Storage (S3/GCS, 무제한) |
| **디스크 비용(GB/일)** | 100% (기준) | 80~90% | 10~20% |
| **쿼리 속도 (정확 매칭)** | ★★★★★ | ★★★★★ | ★★★★☆ |
| **쿼리 속도 (부분 검색)** | ★★★★★ (와일드카드/구문) | ★★★★★ | ★★★☆☆ (grep은 느림) |
| **운영 복잡도** | 높음 (JVM/마스터/샤드) | 중간~높음 | 낮음 (단일 바이너리 가능) |
| **수평확장** | 데이터 노드 추가, 리밸런싱 | 동일 | Distributor/Ingester 단순 추가 |
| **Multi-tenancy** | Index Pattern, X-Pack 유료 | 약함 | **네이티브 (`X-Scope-OrgID`)** |
| **Alerting** | ElastAlert/Watcher | 동일 | Grafana Alerting (LogQL) |
| **k8s 친화성** | 보통 (PV 관리) | 보통 | 매우 높음 (Service Discovery) |
| **적합 환경** | 보안 로그, 감사 로그, 검색 필수 | 동일 | MSA/Edge/IoT/비용 민감 |
| **약점** | 비용·운영 부담 | 동일 | High Cardinality 약함 |

### 3.2 통합 생태계

```text
+---------------------------------------------------------+
|         Grafana 관측성 스택 (LGTM+ Stack)                 |
+---------------------------------------------------------+
|                                                         |
|  +----------+  +----------+  +----------+  +--------+ |
|  |  Mimir   |  |   Loki   |  |  Tempo   |  |Pyroscope| |
|  |(Metrics) |  |  (Logs)  |  | (Traces) |  |(Profiles)|
|  +----+-----+  +----+-----+  +----+-----+  +----+----+ |
|       |             |             |             |       |
|       +--------
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 405 / 800

<- **이전**: [404. 예거 분산 추적 서비스 맵 분석](/studynote/13_cloud_architecture/06_exam_summary/404_jaeger_distributed_tracing_service_map/)
**다음**: [406. ELK 스택 로그 분석 검색 시각화](/studynote/13_cloud_architecture/06_exam_summary/406_elk_stack_log_analysis_search_visualization/) ->

---
