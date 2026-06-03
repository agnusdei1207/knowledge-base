+++
title = "135. 시계열 데이터베이스 (Time Series DB) — InfluxDB/TimescaleDB/QuestDB"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
- **본질**: 시계열 DB(TSDB, Time Series [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/))는 타임스탬프를 기본 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)로 설계하여 시간 순 추가(Append) 전용 워크로드에서 범용 DB 대비 [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~100배 높은 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률과 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 달성한다.
- **가치**: 자동 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보존 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)([Retention](/knowledge-base/studynote/05_database/04_transactions_concurrency/515_mvcc/) [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))과 다운샘플링(Downsampling)으로 수개월치 원시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 집계 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하여 무한정 증가하는 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)·[모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 비용 효율적으로 관리한다.
- **판단 포인트**: SQL 친숙도가 높으면 TimescaleDB, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·비용 최우선이면 [InfluxDB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/), [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 삽입(수백만 rows/sec)이 필요하면 QuestDB를 선택하는 것이 실무 기준이다.

---

## Ⅰ. 개요 및 필요성

### 시계열 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 특성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">시계열 데이터의 4가지 특성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 시간 순서 (Time-Ordered)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">타임스탬프가 기본 식별자이자 정렬 기준</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 추가 전용 (Append-Only)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">과거 데이터 수정 거의 없음 → 쓰기 최적화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 고빈도 쓰기 (High Write Throughput)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">초당 수천~수백만 개의 센서 포인트 동시 유입</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. 시간 기반 쿼리 (Time-Range Query)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">"지난 1시간 평균 CPU", "어제 최대 온도" 등</div></div>
</div>
</div>



### 범용 DB vs 시계열 DB 비교

| 항목 | RDBMS/[MongoDB](/knowledge-base/studynote/05_database/04_transactions_concurrency/540_mongodb/) | 시계열 DB |
|:---:|:---:|:---:|
| 기본 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | PK (임의 키) | 타임스탬프 |
| [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 패턴 | CRUD | 주로 INSERT (Append) |
| 삭제 방식 | 개별 행 삭제 | [TTL](/knowledge-base/studynote/03_network/06_network_layer_ip/294_ttl_time_to_live_looping_prevention/) 기반 일괄 삭제 |
| [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | 범용 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | [델타 인코딩](/knowledge-base/studynote/05_database/06_dw_olap_trends/379_delta_encoding_gorilla_compression/) + Gorilla [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) |
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 특화 | 범용 SQL | 시간 [집계 함수](/knowledge-base/studynote/05_database/03_relational_model/147_aggregate_function_group_by/) ([rollup](/knowledge-base/studynote/06_ict_convergence/01_blockchain/042_rollup_l2_solution/), downsampling) |
| 저장 효율 | 기준 | 5~30배 효율적 |

📢 **섹션 요약 비유**
> 시계열 DB는 타임랩스 영상을 위한 카메라와 같다. 매 초 같은 각도로 찍는다는 사실([타임스탬프 순서](/knowledge-base/studynote/05_database/07_exam_summary/452_timestamp_ordering/))을 알기 때문에, 일반 카메라보다 훨씬 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)률이 높고 "어제 오전 8시부터 9시 사이"를 빠르게 되감아볼 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [InfluxDB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/) 핵심 개념 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">InfluxDB 데이터 모델</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Measurement (≈ 테이블): "cpu_usage"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Timestamp</div><div class="kb-diagram-cell">Tags (인덱스)</div><div class="kb-diagram-cell">Fields (값)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(ns 정밀도)</div><div class="kb-diagram-cell">host</div><div class="kb-diagram-cell">region</div><div class="kb-diagram-cell">usage_user</div><div class="kb-diagram-cell">idle</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1714550400ns</div><div class="kb-diagram-cell">web1</div><div class="kb-diagram-cell">ap-korea</div><div class="kb-diagram-cell">45.2</div><div class="kb-diagram-cell">54.8</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1714550460ns</div><div class="kb-diagram-cell">web1</div><div class="kb-diagram-cell">ap-korea</div><div class="kb-diagram-cell">47.1</div><div class="kb-diagram-cell">52.9</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1714550400ns</div><div class="kb-diagram-cell">db1</div><div class="kb-diagram-cell">ap-korea</div><div class="kb-diagram-cell">12.3</div><div class="kb-diagram-cell">87.7</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Tags: 인덱싱, 그룹핑 기준 (low cardinality 권장)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Fields: 실제 측정값, 집계 대상 (숫자/문자열/불리언)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Series: Measurement + Tags의 고유 조합</div></div>
</div>
</div>



### [InfluxDB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/) 보존 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) ([Retention](/knowledge-base/studynote/05_database/04_transactions_concurrency/515_mvcc/) [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))과 다운샘플링



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">원시 데이터 (1초 간격, 30일 보관)</div>
<div class="kb-diagram-note">↓ Continuous Query / Task</div>
<div class="kb-diagram-note">1분 집계 (avg, min, max) → 1년 보관</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">1시간 집계 → 5년 보관</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">1일 집계 → 영구 보관</div>
<div class="kb-diagram-note">결과: 스토리지 99% 절약 (1초 × 365일 → 1일 × 365일)</div>
</div>
</div>



### TimescaleDB 구조 (PostgreSQL 확장)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">TimescaleDB 아키텍처</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Hypertable (논리적 단일 테이블)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CREATE TABLE metrics (</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">time TIMESTAMPTZ NOT NULL,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">host TEXT,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">cpu DOUBLE PRECISION</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">);</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SELECT create_hypertable('metrics', 'time');</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Chunks (시간 기반 자동 파티션):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">chunk_2026_04_01</div><div class="kb-diagram-cell">chunk_2026_04_02</div><div class="kb-diagram-cell">...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">* 오래된 Chunk → 저비용 스토리지로 자동 이동(티어링)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">* 풀 SQL 지원: JOIN, Window Function, CTE 모두 가능</div></div>
</div>
</div>



### QuestDB 고성능 인제스션 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">QuestDB 성능 비결:</div>
<div class="kb-diagram-note">1. 열 기반 (Columnar) 저장 → 특정 필드 집계 시 I/O 최소화</div>
<div class="kb-diagram-note">2. 메모리 매핑 파일 (Memory-Mapped Files) → 커널 I/O 우회</div>
<div class="kb-diagram-note">3. SIMD (Single Instruction, Multiple Data) 활용</div>
<div class="kb-diagram-note">4. 파티션 병렬 처리</div>
<div class="kb-diagram-note">성능: 단일 서버 기준 수백만 rows/sec 삽입</div>
</div>
</div>



| DB | [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 | 특징 | 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표 |
|:---:|:---:|:---|:---:|
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/">InfluxDB</a></strong> | Flux / InfluxQL | 네이티브 TSDB, 클라우드 관리형 | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 200K pts/sec |
| **TimescaleDB** | SQL (PostgreSQL) | SQL 호환, Hypertable | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 100K rows/sec |
| **QuestDB** | SQL (방언) | 열 기반, [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 4M rows/sec |
| **VictoriaMetrics** | MetricsQL | [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) 호환, 초경량 | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 수십만 pts/sec |

📢 **섹션 요약 비유**
> 다운샘플링은 긴 회의 영상을 요약본으로 편집하는 것과 같다. 5시간 원본(1초 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 5분 요약본(1분 평균)으로 만들면 찾아보기는 오래 걸리지 않으면서 저장 공간을 95% 절약할 수 있다.

---

## Ⅲ. 비교 및 연결

### [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) vs [InfluxDB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/) 비교

| 항목 | [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) | [InfluxDB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/) |
|:---:|:---:|:---:|
| 수집 방식 | Pull (스크레이핑) | Push (직접 삽입) |
| [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) | 레이블 기반 시계열 | Measurement + Tags |
| 장기 보관 | 취약 (Thanos/Cortex 필요) | 내장 보존 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 | PromQL | Flux / InfluxQL |
| 생태계 | [Grafana](/knowledge-base/studynote/16_bigdata/08_visualization/168_grafana/) 통합 강력 | [InfluxDB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/) Cloud |
| 적합 | [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 | [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), 범용 시계열 |

### 시계열 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 기술 (Gorilla [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))

```text
페이스북 Gorilla 시계열 압축:
  - XOR 기반 델타 인코딩
  - 연속 타임스탬프: 각 시간 차이만 저장
  - 연속 부동소수점: XOR 비트만 저장

예시:
  원시: 23.5, 23.7, 23.6, 23.8  (각 8바이트 = 32바이트)
  압축: 23.5, +0.2, -0.1, +0.2  (델타 2비트 = 0.25바이트)
  압축률: 128:1 까지 가능
```

📢 **섹션 요약 비유**
> Prometheus와 InfluxDB의 차이는 기자(Pull)와 제보자(Push)의 차이다. Prometheus는 정기적으로 각 서버에 찾아가 수치를 읽어오고(스크레이핑), InfluxDB는 각 센서가 직접 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보내준다(Push). 서버가 적으면 Pull이 간편하고, 서버가 수만 대면 Push가 확장성이 높다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 플랫폼 아키텍처 설계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">센서 디바이스</div>
<div class="kb-diagram-note">MQTT/HTTP</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">IoT 브로커(Mosquitto/AWS IoT)</div>
<div class="kb-diagram-note">스트림 처리</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Kafka (버퍼 + 내결함성)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">시계열 DB (InfluxDB/TimescaleDB)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Grafana (시각화 대시보드)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">이상 감지 (ML 모델 → 알람)</div>
</div>
</div>



### 기술사 설계 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

| 항목 | 결정 기준 |
|:---|:---:|
| 카디널리티 관리 | Tags 조합 수 < 수백만 ([InfluxDB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/) High Cardinality 주의) |
| 보존 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 설계 | 원시→1분→1시간 다운샘플링 계층 정의 |
| [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 최적화 | 시간 범위 WHERE 절 항상 포함 |
| [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 시간 기반 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)으로 오래된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 빠른 삭제 |
| 고가용성 | [InfluxDB](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/) Enterprise 클러스터 or 관리형 클라우드 |

📢 **섹션 요약 비유**
> 시계열 DB의 High Cardinality 문제는 도서관 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계가 너무 세밀한 것과 같다. 책 한 권마다 고유한 선반 번호를 붙이면 목록 관리 비용이 도서관보다 더 커진다. Tags는 적당한 범주(호스트명, 리전)로 묶어야 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 효율이 유지된다.

---

## Ⅴ. 기대효과 및 결론

### 도입 효과 비교 ([IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 플랫폼 실사례)

| 항목 | PostgreSQL | TimescaleDB | 개선율 |
|:---:|:---:|:---:|:---:|
| 1주일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) | 55K rows/sec | 110K rows/sec | 2배 |
| 1개월 집계 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) | 45sec | 3sec | 15배 |
| 스토리지([압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 후) | 100GB | 12GB | 8.3배 절약 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 티어링 | 수동 | 자동 | — |

### 결론
시계열 DB는 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)·[모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링·금융 틱 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)처럼 타임스탬프가 핵심이고 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 압도적으로 많은 워크로드의 표준 인프라로 자리잡았다. 기술사 시험에서는 **TSDB의 4가지 특성**, <strong>보존 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>+다운샘플링 설계</strong>, <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/255_time_series_rollup_retention_compression/">InfluxDB</a> <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/">데이터 모델</a>(Tags/Fields/Measurement)</strong>, <strong>Gorilla <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> 원리</strong>가 핵심 논점이다.

📢 **섹션 요약 비유**
> 시계열 DB 도입은 기상청이 기온 기록을 위한 전용 시스템을 도입하는 것과 같다. 일반 스프레드시트(RDBMS)에도 기록할 수 있지만, 매분 전국 수천 곳의 기온을 기록하고 "지난 10년 8월 평균"을 즉시 뽑으려면 기상 전용 시스템이 필요하다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---:|:---:|:---|
| Gorilla [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) | 저장 최적화 | 델타 XOR 인코딩, 시계열 전용 |
| [Retention](/knowledge-base/studynote/05_database/04_transactions_concurrency/515_mvcc/) [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리 | 보존 기간 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 자동 삭제 |
| Downsampling | 집계 최적화 | 원시 → 집계 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계층화 |
| Hypertable | TimescaleDB 구조 | 시간 기반 자동 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 테이블 |
| PromQL | 연관 기술 | [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/) 시계열 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">관계형 DB (RDBMS) — 시계열 저장 시 인덱스 팽창·쓰기 병목 발생</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">시계열 DB (TSDB) — 시간 스탬프 기반 압축·집계 최적화 전문 스토리지</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">InfluxDB / TimescaleDB — 대표 TSDB, 라인 프로토콜·SQL 인터페이스 제공</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">다운샘플링·보존 정책 (Downsampling &amp; Retention) — 오래된 데이터 자동 집계·삭제</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스트리밍 연계 (Kafka → TSDB) — 실시간 지표 수집·저장·알림 파이프라인</div></div>
</div>
</div>



이 흐름은 RDBMS의 시계열 저장 한계를 전문 TSDB가 극복하고, 다운샘플링으로 장기 보관을 최적화하며, 실시간 스트리밍 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인으로 통합되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. 시계열 DB는 온도계 일지와 같아요. 매시간 온도를 기록하고, "이번 주 가장 더웠던 날"을 바로 찾아줘요.
2. 다운샘플링은 긴 노트를 요약본으로 줄이는 것 — 매분 기록 대신 하루 평균만 남겨도 큰 흐름은 보여요.
3. 시계열 DB가 없으면 수백만 개의 센서 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)가 쏟아질 때 일반 DB가 숨이 막혀버리는데, 시계열 DB는 이런 상황에 딱 맞게 만들어진 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 135 / 262

← **이전**: [134. Cypher 쿼리 언어 (Cypher Query Language) — 그래프 패턴 매칭](/knowledge-base/studynote/16_bigdata/06_nosql/134_cypher_query/)
**다음**: [136. 검색 엔진 데이터베이스 (Search Engine DB) — Elasticsearch/OpenSearch](/knowledge-base/studynote/16_bigdata/06_nosql/136_search_engine_db/) →

---
