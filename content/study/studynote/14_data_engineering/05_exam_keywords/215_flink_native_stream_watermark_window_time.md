+++
weight = 215
title = "215. 아파치 플링크 (Apache Flink) 네이티브 스트림 워터마크 윈도우"
date = "2026-04-21"
[extra]
categories = "studynote-data-engineering"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Flink는 배치를 스트림의 특수 케이스로 보는 **네이티브 [[229_stream_processing_kafka_flink|스트림 처리]](Native [[229_stream_processing_kafka_flink|Stream Processing]])** 엔진으로, Spark의 마이크로배치(Micro-Batch)와 달리 이벤트 단위로 즉시 처리해 밀리초 단위 [[015_지연_데이터_관점|지연]]을 달성한다.
> 2. **가치**: 이벤트 시간(Event Time) + [[085_watermark|워터마크]]([[085_watermark|Watermark]]) 메커니즘으로 [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]]·순서 역전 문제를 해결하고, 텀블링·슬라이딩·[[160_session_controlling_terminal|세션]] 윈도우로 시계열 집계를 정확하게 수행한다.
> 3. **판단 포인트**: 금융 사기 탐지·실시간 모니터링·IoT처럼 극저지연(Ultra-Low [[141_latency|Latency]])과 이벤트 시간 [[002_bigdata_5v|정확성]]이 동시에 요구될 때 Flink가 최선택이다 — Spark Streaming은 [[015_지연_데이터_관점|지연]]이 수 초 수준이기 때문이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [[229_stream_processing_kafka_flink|스트림 처리]]의 두 가지 접근법

| 항목 | 마이크로배치 ([[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]]) | 네이티브 스트림 (Apache Flink) |
|:---|:---|:---|
| **처리 단위** | 짧은 배치 묶음 (0.1~수 초) | 이벤트 1건씩 즉시 처리 |
| **[[141_latency|지연 시간]]** | 수백 ms ~ 수 초 | 1~수십 ms |
| **상태 관리** | 배치 단위 | 지속적 상태 유지 |
| **이벤트 시간 처리** | 제한적 | 완전 지원 ([[085_watermark|워터마크]]) |
| **체크포인트** | 배치 경계 | 지속적 비동기 체크포인트 |
| **적합 사례** | 준실시간, 배치 혼용 | 진정한 실시간 분석 |

### 1.2 Flink의 "Everything is a [[467_http2_stream_multiplexing_tcp_hol|Stream]]" 철학

Flink는 배치(Batch)를 유한한 스트림(Bounded [[467_http2_stream_multiplexing_tcp_hol|Stream]]), 실시간을 무한한 스트림(Unbounded [[467_http2_stream_multiplexing_tcp_hol|Stream]])으로 통일하여 하나의 엔진으로 처리한다.

```
무한 스트림 (Unbounded Stream):
  Kafka ──► [Flink] ──► 실시간 대시보드
  이벤트가 끊임없이 흘러옴

유한 스트림 (Bounded Stream = 배치):
  HDFS 파일 ──► [Flink] ──► 배치 집계 결과
  데이터가 시작과 끝이 있음
```

📢 **섹션 요약 비유**: Flink는 강(스트림)을 흐르는 물방울 하나하나를 즉시 처리하는 물레방아다 — Spark는 물을 일정량 모아서 한꺼번에 처리하는 물탱크 방식이고, Flink는 방울이 오는 순간 바로 돌아간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Flink 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    Flink 클러스터                             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │             JobManager                               │   │
│  │  - 잡 스케줄링 (Job Scheduling)                      │   │
│  │  - 체크포인트 조율 (Checkpoint Coordination)         │   │
│  │  - 장애 복구 (Fault Recovery)                        │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                          │ 태스크 배분                        │
│    ┌─────────────────────┼─────────────────────────────┐    │
│    ▼                     ▼                             ▼    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ TaskManager  │  │ TaskManager  │  │ TaskManager  │     │
│  │  Slot 1~N    │  │  Slot 1~N    │  │  Slot 1~N    │     │
│  │  실제 처리   │  │  실제 처리   │  │  실제 처리   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
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
                │         │         │         │
네트워크 지연:  정상      지연2초   정상      지연5초
                │         │         │         │
Flink 도착:    10:00:01  10:00:03  10:00:03  10:00:09
                                   ↑          ↑
                               순서 역전!  늦게 도착!
```

### 2.3 [[085_watermark|워터마크]] ([[085_watermark|Watermark]]) 메커니즘

[[085_watermark|워터마크]]([[085_watermark|Watermark]])는 "이 시각 이전의 이벤트는 모두 도착했다고 간주한다"는 시간 [[216_progress_in_synchronization|진행]] [[130_signal|신호]]다.

```
Watermark = max(event_time_seen) - max_out_of_orderness

예: max_out_of_orderness = 5초 설정 시
이벤트 도착: 10:00:10
워터마크   : 10:00:05

→ 10:00:05 이전 이벤트는 더 이상 기다리지 않고 윈도우 닫음
→ 10:00:05 이후 늦게 도착하는 이벤트는 '지연 데이터'로 처리

┌─────────────────────────────────────────────────────────┐
│  이벤트 스트림:  ●●●●●●●●●●●●●●●●●●●●●●●●●           │
│  워터마크:       ─────────────WM──────────────►         │
│                              ↑                          │
│                         WM 통과 → 이전 윈도우 닫힘       │
└─────────────────────────────────────────────────────────┘
```

### 2.4 윈도우 유형 3종

| 윈도우 유형 | 설명 | 예시 |
|:---|:---|:---|
| **텀블링 윈도우 (Tumbling Window)** | 고정 크기, 겹침 없음 | 1분마다 매출 집계 |
| **슬라이딩 윈도우 (Sliding Window)** | 고정 크기, 슬라이드 간격 | 1분 집계, 30초마다 갱신 |
| **[[160_session_controlling_terminal|세션]] 윈도우 ([[160_session_controlling_terminal|Session]] Window)** | 비활성 구간으로 경계 결정 | 사용자 [[160_session_controlling_terminal|세션]] 분석 |

```
텀블링 (Tumbling):
[──1분──][──1분──][──1분──]

슬라이딩 (Sliding, 1분 크기, 30초 슬라이드):
[────1분────]
      [────1분────]
            [────1분────]

세션 (Session, 비활성 30초):
[──활동──]  [───활동───]  [──활동──]
         30초           30초
         갭(Gap)        갭(Gap)
```

📢 **섹션 요약 비유**: [[085_watermark|워터마크]]는 '마감 시간 알림'이다 — "지금부터 이 시간 이전 데이터는 기다리지 않겠습니다"라는 선언으로, 늦은 학생을 하염없이 기다리지 않고 시험을 시작하게 해준다.

---

## Ⅲ. 비교 및 연결

### 3.1 Flink vs [[060_spark_streaming_dstream|Spark Streaming]]

| 항목 | Apache Flink | [[061_structured_streaming|Spark Structured Streaming]] |
|:---|:---|:---|
| **처리 모델** | 네이티브 스트림 | 마이크로배치 |
| **[[015_지연_데이터_관점|지연]]** | < 10ms | 수백 ms ~ 수 초 |
| **이벤트 시간** | 완전 지원 | 지원 (제한적) |
| **상태 관리** | RocksDB 기반 대규모 상태 | 메모리 기반 |
| **체크포인트** | Chandy-Lamport [[001_algorithm_definition|알고리즘]] | 배치 경계 저장 |
| **SQL 지원** | Flink SQL (완전 지원) | [[056_spark_sql|Spark SQL]] |

### 3.2 Flink의 상태 관리 (Stateful [[229_stream_processing_kafka_flink|Stream Processing]])

Flink는 상태([[272_state_pattern|State]])를 RocksDB(디스크) 또는 메모리에 저장하고, 비동기 체크포인트(Asynchronous Checkpoint)로 장애 복구를 지원한다.

```
상태 유형:
- ValueState<T>    : 단일 값 상태 (예: 사용자별 누적 합계)
- ListState<T>     : 리스트 상태 (예: 최근 N개 이벤트)
- MapState<K,V>    : 맵 상태 (예: 제품별 카운터)
- ReducingState<T> : 누적 집계 상태
```

📢 **섹션 요약 비유**: Flink의 윈도우는 [[344_bus|버스]] 정류장이다 — 텀블링은 5분마다 출발하는 정기버스, 슬라이딩은 1분마다 새 [[344_bus|버스]]가 오되 5분치 승객을 태우는 것, [[160_session_controlling_terminal|세션]]은 손님이 없으면 30분 뒤 출발하는 수요 응답형 [[344_bus|버스]]다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 실시간 사기 탐지 파이프라인 (Fraud [[961_deepfake_detection|Detection]])

```
신용카드 거래 ──► Kafka ──► Flink ──► 이상 거래 알림
  Event Time      토픽      워터마크
                           세션 윈도우 (5분)
                           상태: 사용자별 거래 패턴
                           룰: 1분 내 5회 초과 → 사기 의심
```

### 4.2 체크포인트 [[009_config|설정]] 가이드

| [[009_config|설정]] 항목 | 권장값 | 설명 |
|:---|:---|:---|
| `checkpointing.interval` | 1분~5분 | 체크포인트 주기 |
| `state.backend` | RocksDB | 대규모 상태 처리 |
| `checkpoint.timeout` | 10분 | [[573_timeout_retry_backoff_strategy|타임아웃]] 초과 시 중단 |
| `tolerable-checkpoint-failures` | 3 | 연속 실패 허용 횟수 |

📢 **섹션 요약 비유**: Flink의 체크포인트는 게임의 '세이브 포인트'다 — 중간중간 저장해두면 장애가 발생해도 마지막 세이브 지점부터 다시 시작할 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 Flink 도입 효과

| 효과 | 내용 |
|:---|:---|
| **극저지연** | 이벤트 단위 처리로 < 10ms 응답 달성 |
| **[[002_bigdata_5v|정확성]]** | 이벤트 시간 + [[085_watermark|워터마크]]로 순서 역전 데이터도 정확 집계 |
| **확장성** | TaskManager 추가로 선형 확장 |
| **내결함성** | Chandy-Lamport 체크포인트로 Exactly-Once 보장 |

### 5.2 결론 — 기술사 작성 포인트

기술사 답안에서는 **"이벤트 시간(Event Time) + [[085_watermark|워터마크]]가 순서 역전 문제를 해결하는 메커니즘"**을 구체적으로 서술해야 한다. 처리 시간(Processing Time) 기반은 빠르지만 부정확하고, 이벤트 시간은 정확하지만 늦게 도착하는 이벤트 처리가 필요하다 — [[085_watermark|워터마크]]가 이 딜레마를 해결하는 핵심 장치임을 강조하면 고득점이다.

📢 **섹션 요약 비유**: Flink는 세계 최고 속도의 도서 분류기다 — 날짜가 섞여서 오는 우편물(이벤트)을 받을 때, [[085_watermark|워터마크]]라는 '마감 시간'까지만 기다렸다가 날짜순(이벤트 시간)으로 정확히 분류한다.

---

### 📌 관련 개념 맵

| [[083_relationship_in_er_model|관계]] | 개념 | 설명 |
|:---|:---|:---|
| 처리 모델 | 네이티브 스트림 (Native [[467_http2_stream_multiplexing_tcp_hol|Stream]]) | 이벤트 단위 즉시 처리 |
| 시간 처리 | 이벤트 시간 (Event Time) | 실제 발생 시각 기반 처리 |
| [[015_지연_데이터_관점|지연]] 처리 | [[085_watermark|워터마크]] ([[085_watermark|Watermark]]) | [[015_지연_데이터_관점|지연]] 허용 한계선 [[130_signal|신호]] |
| 시계열 집계 | 텀블링·슬라이딩·[[160_session_controlling_terminal|세션]] 윈도우 | 시간 범위 기반 집계 |
| 상태 관리 | RocksDB [[272_state_pattern|State]] Backend | 대규모 키-값 상태 저장 |
| 내결함성 | 체크포인트 (Checkpoint) | 비동기 상태 [[022_snapshot_backup_architecture|스냅샷]] |
| 비교 대상 | [[061_structured_streaming|Spark Structured Streaming]] | 마이크로배치 [[229_stream_processing_kafka_flink|스트림 처리]] |

### 👶 어린이를 위한 3줄 비유 설명

1. Flink는 편지(이벤트)가 오는 즉시 읽는 우체부야 — Spark는 편지를 10통씩 모아서 한꺼번에 읽어서 조금 느려.

### 📈 관련 키워드 및 발전 흐름도

```text
배치 처리 (MapReduce · Spark)
    │
    ▼
마이크로 배치 (Spark Structured Streaming)
    │
    ▼
네이티브 스트리밍: Apache Flink
    ├─► Event Time + Watermark: 지연 이벤트 허용
    ├─► Window: Tumbling · Sliding · Session
    └─► Exactly-Once: Checkpoint + 2PC Sink
    │
    ▼
Flink SQL · Table API → 통합 배치/스트리밍
```
2. [[085_watermark|워터마크]]는 "이 날짜 전 편지는 다 도착했겠지"라고 판단하는 기준이야 — 그래야 늦게 도착하는 편지를 하염없이 기다리지 않아도 되거든.
3. 텀블링 윈도우는 '10분마다 정리하는 서랍', [[160_session_controlling_terminal|세션]] 윈도우는 '손님이 없으면 문 닫는 가게' — 어떻게 묶어서 볼지 결정하는 방법이야.
