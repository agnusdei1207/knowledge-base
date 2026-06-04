---
title: "215. 아파치 플링크 (Apache Flink) 네이티브 스트림 워터마크 윈도우"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Flink는 배치를 스트림의 특수 케이스로 보는 <strong>네이티브 <a href="/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/">스트림 처리</a>(Native <a href="/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/">Stream Processing</a>)</strong> 엔진으로, Spark의 마이크로배치(Micro-Batch)와 달리 이벤트 단위로 즉시 처리해 밀리초 단위 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 달성한다.
> 2. **가치**: 이벤트 시간(Event Time) + [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)([Watermark](/studynote/16_bigdata/04_streaming/085_watermark/)) 메커니즘으로 [네트워크 지연](/studynote/03_network/20_performance_evaluation_advanced/1002_network_delay_rtt_oneway_delay_components/)·순서 역전 문제를 해결하고, 텀블링·슬라이딩·[세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 윈도우로 시계열 집계를 정확하게 수행한다.
> 3. **판단 포인트**: 금융 사기 탐지·실시간 모니터링·IoT처럼 극저지연(Ultra-Low [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))과 이벤트 시간 [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)이 동시에 요구될 때 Flink가 최선택이다 — Spark Streaming은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 수 초 수준이기 때문이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [스트림 처리](/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/)의 두 가지 접근법

| 항목 | 마이크로배치 ([Apache Spark](/studynote/14_data_engineering/05_exam_keywords/206_spark_inmemory_rdd_lazy_evaluation_lineage/)) | 네이티브 스트림 (Apache Flink) |
|:---|:---|:---|
| **처리 단위** | 짧은 배치 묶음 (0.1~수 초) | 이벤트 1건씩 즉시 처리 |
| <strong><a href="/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/">지연 시간</a></strong> | 수백 ms ~ 수 초 | 1~수십 ms |
| **상태 관리** | 배치 단위 | 지속적 상태 유지 |
| **이벤트 시간 처리** | 제한적 | 완전 지원 ([워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)) |
| **체크포인트** | 배치 경계 | 지속적 비동기 체크포인트 |
| **적합 사례** | 준실시간, 배치 혼용 | 진정한 실시간 분석 |

### 1.2 Flink의 "Everything is a [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/)" 철학

Flink는 배치(Batch)를 유한한 스트림(Bounded [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/)), 실시간을 무한한 스트림(Unbounded [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/))으로 통일하여 하나의 엔진으로 처리한다.

```
무한 스트림 (Unbounded Stream):
  Kafka --► [Flink] --► 실시간 대시보드
  이벤트가 끊임없이 흘러옴

유한 스트림 (Bounded Stream = 배치):
  HDFS 파일 --► [Flink] --► 배치 집계 결과
  데이터가 시작과 끝이 있음
```

📢 **섹션 요약 비유**: Flink는 강(스트림)을 흐르는 물방울 하나하나를 즉시 처리하는 물레방아다 — Spark는 물을 일정량 모아서 한꺼번에 처리하는 물탱크 방식이고, Flink는 방울이 오는 순간 바로 돌아간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Flink 아키텍처

```
+-------------------------------------------------------------+
|                    Flink 클러스터                             |
|                                                             |
|  +-----------------------------------------------------+   |
|  |             JobManager                               |   |
|  |  - 잡 스케줄링 (Job Scheduling)                      |   |
|  |  - 체크포인트 조율 (Checkpoint Coordination)         |   |
|  |  - 장애 복구 (Fault Recovery)                        |   |
|  +----------------------+------------------------------+   |
|                          | 태스크 배분                        |
|    +---------------------+-----------------------------+    |
|    v                     v                             v    |
|  +--------------+  +--------------+  +--------------+     |
|  | TaskManager  |  | TaskManager  |  | TaskManager  |     |
|  |  Slot 1~N    |  |  Slot 1~N    |  |  Slot 1~N    |     |
|  |  실제 처리   |  |  실제 처리   |  |  실제 처리   |     |
|  +--------------+  +--------------+  +--------------+     |
+-------------------------------------------------------------+
```

### 2.2 시간 개념 3종

Flink는 이벤트 시간 처리에서 3가지 시간 개념을 엄격히 구분한다.

| 시간 유형 | 정의 | 특징 |
|:---|:---|:---|
| **이벤트 시간 (Event Time)** | 이벤트가 실제 발생한 시각 (로그에 기록) | 정확하지만 순서 역전 가능 |
| **수집 시간 (Ingestion Time)** | Flink 소스가 이벤트를 수신한 시각 | 중간 정확도 |
| **처리 시간 (Processing Time)** | Flink 연산자가 처리하는 시각 | 빠르지만 부정확 |

```
실제 시나리오 (이벤트 시간 역전):

이벤트 발생:   10:00:01  10:00:02  10:00:03  10:00:04
                |         |         |         |
네트워크 지연:  정상      지연2초   정상      지연5초
                |         |         |         |
Flink 도착:    10:00:01  10:00:03  10:00:03  10:00:09
                                   ^          ^
                               순서 역전!  늦게 도착!
```

### 2.3 [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/) ([Watermark](/studynote/16_bigdata/04_streaming/085_watermark/)) 메커니즘

[워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)([Watermark](/studynote/16_bigdata/04_streaming/085_watermark/))는 "이 시각 이전의 이벤트는 모두 도착했다고 간주한다"는 시간 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) [신호](/studynote/02_operating_system/02_process_thread/130_signal/)다.

```
Watermark = max(event_time_seen) - max_out_of_orderness

예: max_out_of_orderness = 5초 설정 시
이벤트 도착: 10:00:10
워터마크   : 10:00:05

-> 10:00:05 이전 이벤트는 더 이상 기다리지 않고 윈도우 닫음
-> 10:00:05 이후 늦게 도착하는 이벤트는 '지연 데이터'로 처리

+---------------------------------------------------------+
|  이벤트 스트림:  ●●●●●●●●●●●●●●●●●●●●●●●●●           |
|  워터마크:       -------------WM--------------►         |
|                              ^                          |
|                         WM 통과 -> 이전 윈도우 닫힘       |
+---------------------------------------------------------+
```

### 2.4 윈도우 유형 3종

| 윈도우 유형 | 설명 | 예시 |
|:---|:---|:---|
| **텀블링 윈도우 (Tumbling Window)** | 고정 크기, 겹침 없음 | 1분마다 매출 집계 |
| **슬라이딩 윈도우 (Sliding Window)** | 고정 크기, 슬라이드 간격 | 1분 집계, 30초마다 갱신 |
| <strong><a href="/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/">세션</a> 윈도우 (<a href="/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/">Session</a> Window)</strong> | 비활성 구간으로 경계 결정 | 사용자 [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 분석 |

```
텀블링 (Tumbling):
[--1분--][--1분--][--1분--]

슬라이딩 (Sliding, 1분 크기, 30초 슬라이드):
[----1분----]
      [----1분----]
            [----1분----]

세션 (Session, 비활성 30초):
[--활동--]  [---활동---]  [--활동--]
         30초           30초
         갭(Gap)        갭(Gap)
```

📢 **섹션 요약 비유**: [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)는 '마감 시간 알림'이다 — "지금부터 이 시간 이전 데이터는 기다리지 않겠습니다"라는 선언으로, 늦은 학생을 하염없이 기다리지 않고 시험을 시작하게 해준다.

---

## Ⅲ. 비교 및 연결

### 3.1 Flink vs [Spark Streaming](/studynote/16_bigdata/03_spark/060_spark_streaming_dstream/)

| 항목 | Apache Flink | [Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) |
|:---|:---|:---|
| **처리 모델** | 네이티브 스트림 | 마이크로배치 |
| <strong><a href="/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a></strong> | < 10ms | 수백 ms ~ 수 초 |
| **이벤트 시간** | 완전 지원 | 지원 (제한적) |
| **상태 관리** | RocksDB 기반 대규모 상태 | 메모리 기반 |
| **체크포인트** | Chandy-Lamport [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 배치 경계 저장 |
| **SQL 지원** | Flink SQL (완전 지원) | [Spark SQL](/studynote/16_bigdata/03_spark/056_spark_sql/) |

### 3.2 Flink의 상태 관리 (Stateful [Stream Processing](/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/))

Flink는 상태([State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))를 RocksDB(디스크) 또는 메모리에 저장하고, 비동기 체크포인트(Asynchronous Checkpoint)로 장애 복구를 지원한다.

```
상태 유형:
- ValueState<T>    : 단일 값 상태 (예: 사용자별 누적 합계)
- ListState<T>     : 리스트 상태 (예: 최근 N개 이벤트)
- MapState<K,V>    : 맵 상태 (예: 제품별 카운터)
- ReducingState<T> : 누적 집계 상태
```

📢 **섹션 요약 비유**: Flink의 윈도우는 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 정류장이다 — 텀블링은 5분마다 출발하는 정기버스, 슬라이딩은 1분마다 새 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 오되 5분치 승객을 태우는 것, [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)은 손님이 없으면 30분 뒤 출발하는 수요 응답형 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 실시간 사기 탐지 파이프라인 (Fraud [Detection](/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/))

```
신용카드 거래 --► Kafka --► Flink --► 이상 거래 알림
  Event Time      토픽      워터마크
                           세션 윈도우 (5분)
                           상태: 사용자별 거래 패턴
                           룰: 1분 내 5회 초과 -> 사기 의심
```

### 4.2 체크포인트 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 가이드

| [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 항목 | 권장값 | 설명 |
|:---|:---|:---|
| `checkpointing.interval` | 1분~5분 | 체크포인트 주기 |
| `state.backend` | RocksDB | 대규모 상태 처리 |
| `checkpoint.timeout` | 10분 | [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 초과 시 중단 |
| `tolerable-checkpoint-failures` | 3 | 연속 실패 허용 횟수 |

📢 **섹션 요약 비유**: Flink의 체크포인트는 게임의 '세이브 포인트'다 — 중간중간 저장해두면 장애가 발생해도 마지막 세이브 지점부터 다시 시작할 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 Flink 도입 효과

| 효과 | 내용 |
|:---|:---|
| **극저지연** | 이벤트 단위 처리로 < 10ms 응답 달성 |
| <strong><a href="/studynote/16_bigdata/01_intro/002_bigdata_5v/">정확성</a></strong> | 이벤트 시간 + [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)로 순서 역전 데이터도 정확 집계 |
| **확장성** | TaskManager 추가로 선형 확장 |
| **내결함성** | Chandy-Lamport 체크포인트로 Exactly-Once 보장 |

### 5.2 결론 — 기술사 작성 포인트

기술사 답안에서는 <strong>"이벤트 시간(Event Time) + <a href="/studynote/16_bigdata/04_streaming/085_watermark/">워터마크</a>가 순서 역전 문제를 해결하는 메커니즘"</strong>을 구체적으로 서술해야 한다. 처리 시간(Processing Time) 기반은 빠르지만 부정확하고, 이벤트 시간은 정확하지만 늦게 도착하는 이벤트 처리가 필요하다 — [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)가 이 딜레마를 해결하는 핵심 장치임을 강조하면 고득점이다.

📢 **섹션 요약 비유**: Flink는 세계 최고 속도의 도서 분류기다 — 날짜가 섞여서 오는 우편물(이벤트)을 받을 때, [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)라는 '마감 시간'까지만 기다렸다가 날짜순(이벤트 시간)으로 정확히 분류한다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 처리 모델 | 네이티브 스트림 (Native [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/)) | 이벤트 단위 즉시 처리 |
| 시간 처리 | 이벤트 시간 (Event Time) | 실제 발생 시각 기반 처리 |
| [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 처리 | [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/) ([Watermark](/studynote/16_bigdata/04_streaming/085_watermark/)) | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 허용 한계선 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) |
| 시계열 집계 | 텀블링·슬라이딩·[세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 윈도우 | 시간 범위 기반 집계 |
| 상태 관리 | RocksDB [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Backend | 대규모 키-값 상태 저장 |
| 내결함성 | 체크포인트 (Checkpoint) | 비동기 상태 [스냅샷](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/) |
| 비교 대상 | [Spark Structured Streaming](/studynote/16_bigdata/03_spark/061_structured_streaming/) | 마이크로배치 [스트림 처리](/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) |

### 👶 어린이를 위한 3줄 비유 설명

1. Flink는 편지(이벤트)가 오는 즉시 읽는 우체부야 — Spark는 편지를 10통씩 모아서 한꺼번에 읽어서 조금 느려.

### 📈 관련 키워드 및 발전 흐름도

```text
배치 처리 (MapReduce · Spark)
    |
    v
마이크로 배치 (Spark Structured Streaming)
    |
    v
네이티브 스트리밍: Apache Flink
    +-► Event Time + Watermark: 지연 이벤트 허용
    +-► Window: Tumbling · Sliding · Session
    +-► Exactly-Once: Checkpoint + 2PC Sink
    |
    v
Flink SQL · Table API -> 통합 배치/스트리밍
```
2. [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/)는 "이 날짜 전 편지는 다 도착했겠지"라고 판단하는 기준이야 — 그래야 늦게 도착하는 편지를 하염없이 기다리지 않아도 되거든.
3. 텀블링 윈도우는 '10분마다 정리하는 서랍', [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 윈도우는 '손님이 없으면 문 닫는 가게' — 어떻게 묶어서 볼지 결정하는 방법이야.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 215 / 258

<- **이전**: [214. 아파치 카프카 (Apache Kafka) Pub-Sub 토픽 파티션 오프셋 브로커](/studynote/14_data_engineering/05_exam_keywords/214_kafka_pubsub_topic_partition_offset_broker/)
**다음**: [216. 람다 (Lambda) vs 카파 (Kappa) 아키텍처 배치·실시간](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/) ->

---
