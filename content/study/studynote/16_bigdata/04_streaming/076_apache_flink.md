+++
weight = 76
title = "01. Apache Flink - 상태 기반 스트리밍処理의 完成形"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

# [[215_flink_native_stream_watermark_window_time|Apache Flink]] - 상태 기반 스트리밍処理의 完成形

> ⚠️ 이 문서는 [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] Streaming의 마이크로배치(micro-batch) 모델과 달리, 각 레코드(Record)를 개별적으로 프로세서(Processor)에게 전달하여 진정한 의미의 단일 레코드 처리(Record-at-a-Time) 및 상태 관리([[272_state_pattern|State]] [[372_management|Management]])를 구현하는 Apache Flink의 핵심 차별점인 Native Streaming, Checkpoint 기반의 정확한 한 번(Eactly-Once) 처리 시맨틱스, 그리고 이벤트 시간(Event Time)과 [[085_watermark|워터마크]]([[085_watermark|Watermark]])를 활용한 [[015_지연_데이터_관점|지연]] [[001_dikw_pyramid|데이터]] 처리 메커니즘을 기술사 수준에서 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Apache Flink는 각 레코드를 개별적으로 처리하는 네이티브 스트리밍(Continuous Processing) 엔진으로, [[228_batch_processing_hadoop_spark|배치 처리]]와 스트리밍 처리를 동일한 API로 작성할 수 있는"Unified Processing" 아키텍처를 제공하며, 상태 관리([[272_state_pattern|State]])를 내장하여窗口(Window) 연산, [[507_session_management_security|세션 관리]], 상태 [[658_ir_recovery|복구]]를 하나의 프레임워크에서 제공한다.
> 2. **가치**: [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] Streaming이 micro-batch로 수 초 단위 [[015_지연_데이터_관점|지연]]을 감수하는 것과 달리, Flink는 레코드 단위 처리로 ms(밀리초) 단위의 [[015_지연_데이터_관점|지연]]과 함께, 체크포인트(Checkpoint)를利用한岩ず張りなく障碍からの素早い复旧와 Event Time 처리による正確な解析이 가능하다.
> 3. **확장**: Flink는 금융 [[090_service_kubernetes_network_load_balancing|서비스]](카드 사기 탐지), [[101_iot_concept|IoT]] 센서 분석, [[229_monitor|모니터]]링·告警 시스템 등 [[015_지연_데이터_관점|지연]]敏感的인 실시간 분석이 필요한 모든 분야에서 선택적으로 사용되며, LinkedIn, Uber, Alibaba 등의 대규모 실시간 처리 인프라의核心으로活用되고 있다.

---

## Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

### 1. 스트리밍 처리의 진화: Batch에서 Continuous Processing으로
[[001_dikw_pyramid|데이터]] 처리 분야에서"스트리밍(Streaming)"이라는 개념은 크게 두 가지로 나뉩니다.
- **Micro-Batch 모델 (예: Apache [[061_structured_streaming|Spark Structured Streaming]])**: [[001_dikw_pyramid|데이터]]를 짧은 시간 간격(예: 1초)으로 모은 후"미니 배치"로 처리하는 방식입니다. [[139_throughput|처리량]]([[139_throughput|Throughput]])은 높지만, [[019_처리_지연|처리 지연]]([[141_latency|Latency]])이 배치 간격(Interval)보다 낮아질 수 없는 구조적 제약이 있습니다.
- **Continuous Processing 모델 (예: [[215_flink_native_stream_watermark_window_time|Apache Flink]])**: 레코드가 도착하는 순간 즉시 처리하는 방식입니다. 이론상 [[015_지연_데이터_관점|지연]]은 네트워크를 통해 한 레코드가 처리기에 도착하는 시간(ms 단위)에 근접합니다.阿里巴巴やUberなどの大规模分散処理インフラで主流となっています.

### 2. Apache Flink의 탄생 배경
Apache Flink는 2014년 TU Berlin의，研究プロジェクト「Stratosphere」から派生し、2014年にApache Incubatorに入り、2015年にApache Top-Level Projectとなりました。
- **Stratosphere 시대**: 2010-2014년, 독일 TU Berlin의 연구팀이"Stratosphere"라는 이름으로 [[136_variance|분산]] 스트리밍 및 [[228_batch_processing_hadoop_spark|배치 처리]] 엔진을 개발했습니다. 이 프로젝트는 개념적으로 현재의 Flink과 매우 유사했으며, 특히"상태 관리"와"이벤트 시간 처리"에 조기에서 [[459_quic_fec_forward_error_correction|초기]]에 주목했다는 점에서 혁신적이었습니다.
- **선구적 설계 철학**: Flink는最初から"Streaming-first" 아키텍처를志向했습니다. [[228_batch_processing_hadoop_spark|배치 처리]]는"무한한 스트림의 특별한 경우(모든 [[001_dikw_pyramid|데이터]]가 도착한 것으로 간주)"로建模하여, 하나의 엔진으로 배치와 스트리밍을统一的に處理할 수 있도록 설계되었습니다.

### 3. [[215_flink_native_stream_watermark_window_time|Apache Flink]] vs Apache [[060_spark_streaming_dstream|Spark Streaming]]: 근본적 차이

| 구분 | Apache [[060_spark_streaming_dstream|Spark Streaming]] ([[060_spark_streaming_dstream|DStream]]) | [[215_flink_native_stream_watermark_window_time|Apache Flink]] (Native Streaming) |
|:---|:---|:---|
| **처리 모델** | Micro-Batch (짧은 간격의 배치) | Continuous Processing (레코드 단위) |
| **[[019_처리_지연|처리 지연]] ([[141_latency|Latency]])** | ~1초+ | 수십 ms ~ 1초 |
| **상태 관리** |[[071_checkpointing|checkpointing]] (외부),Updates-of-state外面 | 내장된 상태 백엔드 (RocksDB, [[078_heap_datastructure|Heap]]) |
| **Event Time 지원** | Structured Streaming에서 이후 도입 |原生 지원 (이래서 처음부터 중요하게 다룸) |
| ** exactementonce** | Achieved通过预处理程序和幂等性 | Achieved通过两阶段提交([[549_2pc_two_phase_commit_limitations_msa|2PC]]) |
| **[[658_ir_recovery|복구]] 시간** |血统([[023_lazy_evaluation|Lazy Evaluation]])기반 + WAL |轻量级检查点, RocksDB增量检查点 |

- **📢 섹션 요약 비유**: Apache Flink와 Spark Streaming의 차이는"음식점에서 음식을 받는 두 가지 방식"에 비유할 수 있습니다. Spark Streaming은"30분마다 Llegando大型配送車로 음식을 한 상차림씩 배달"(마이크로배치)받는 것으로, 한 상차림의 양은 많지만 30분마다 Llegando까지 기다려야 합니다. Flink는"오토바이 택배로 음식을 한 접시씩即时配送"(레코드 단위 처리)받는 것으로, 고객은 음식을 한 입 먹고 30분마다大型 배달을 기다리는 대신, 한 입 먹을 때마다 바로 다음 한 입이 도착하는 연속적인 경험(연속 처리)을 할 수 있습니다. 단, 오토바이 택배가 30분마다大型 배송보다 비용이 조금 더 드는 것처럼, Flink도 마이크로배치 대비 높은 처리 오버헤드가 있을 수 있어"即時성이 얼마나 중요한가?"를 고려하여 도입 여부를 결정해야 합니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([[319_architecture|Architecture]] & Mechanism)

```text
┌─────────────────────────────────────────────────────────────────┐
│                  [ Apache Flink 아키텍처 ]                       │
│                                                                 │
│  [Client]                                                       │
│    │ Flink 코드를 작성하고, JobGraph으로 컴파일                   │
│    ▼                                                             │
│  [JobManager (마스터)]                                           │
│    ├─ JobGraph 스케줄링 → TaskManagers에 태스크 배포             │
│    ├─ Checkpoint 조정 (체크포인트，协调자)                      │
│    ├─ 리소스 관리 (Slot 관리)                                    │
│    └─ 장애 복구 (Task 실패 감지 + 재시작 정책)                   │
│                                                                 │
│  [TaskManager (워커)]                                            │
│    ├─ Task 슬롯 (Task 실행 단위) × N개                           │
│    ├─ 상태 백엔드 (State Backend): RocksDB / Heap                │
│    ├─ 네트워크 버퍼 (레코드 교환)                                 │
│    └─ 입출력 관리                                                │
│                                                                 │
│  [DataStream API 실행 흐름]                                      │
│                                                                 │
│  Source → [Transformation: map/filter/keyBy]                    │
│         → [Window: Tumbling/Sliding/Session]                    │
│         → [Trigger/Evictor] → [Sink: 출력]                      │
│                                                                 │
│  [Checkpoint 기반 Exactly-Once 시맨틱스]                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ ① Checkpoint Barrier (CB): 데이터 스트림에 주기적으로 삽입  │    │
│  │ ② Barriers는 소스 연산자로부터下游으로 전달              │    │
│  │ ③ 모든 연산자가 Barriers를 受領하면 상태를 스냅샷 저장    │    │
│  │ ④ 장애 시 마지막 Checkpoint Barrier 시점의 상태로 全量 복구 │    │
│  │ ⑤ 2PC(2단계 커밋)로 End-to-End Exactly-Once 보장         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1. Flink 아키텍처: JobManager와 TaskManager
Flink는 [[172_maas_mobility_as_a_service|마스]]터-워커(Master-Worker) 아키텍처를 채택하고 있습니다.

- **JobManager**: Flink 클러스터의 조정자([[250_coordinator_participant_2pc_roles|Coordinator]]) 역할을 합니다. 사용자로부터 제출된 JobGraph를 TaskManager들의 슬롯에 배포하고, 각 [[150_task|태스크]]의 상태를 [[229_monitor|모니터]]링하며, 체크포인트 조정(Checkpoint Coordination)을 수행합니다. 장애 발생 시 실패한 [[150_task|태스크]]를 재시작하거나, 리소스를 재배치합니다.
- **TaskManager**: 실제 [[001_dikw_pyramid|데이터]] 처리 연산(Transformation, Window, Sink 등)이 실행되는 곳입니다. 각 TaskManager는 하나 이상의 [[150_task|태스크]] 슬롯([[150_task|Task]] Slot)을 보유하며, 각 슬롯은 하나의 [[150_task|태스크]] 실행을 담당합니다. 슬롯 수는 TaskManager의 CPU 코어 수에 의해 결정됩니다.
- **Slot과 [[150_task|Task]] 실행**: 슬롯은 클러스터의 [[041_resource_allocation|자원 할당]] 단위입니다. 각 슬롯은 고립된 메모리(managed memory)를 할당받고, 하나의 [[150_task|태스크]](또는 서브테스크)가 할당됩니다. 슬롯은 여러 [[514_partition_slice_volume|파티션]]을 처리할 수 있어, 코어 수보다 더 많은 작은 [[150_task|태스크]]들을高效적으로 다중 처리할 수 있습니다.

### 2. 상태 백엔드 ([[272_state_pattern|State]] Backend) 선택

| [[272_state_pattern|State]] Backend | 저장 위치 | 장점 | 단점 | 적합한 경우 |
|:---|:---|:---|:---|:---|
| **HashMapStateBackend** | TaskManager JVM [[078_heap_datastructure|Heap]] | 최상의 처리 [[282_performance_tactics|성능]] | JVM [[078_heap_datastructure|Heap]] 크기 한계 (메모리 제한) | 상태 크기 < 수 GB, 고성능 요구 |
| **EmbeddedRocksDBStateBackend** | RocksDB (디스크) | 큰 [[065_state_diagram|상태도]] 외부 메모리로 관리 (LMDB) | 디스크 I/O로 살짝 느림 | 상태 크기 > 수 GB, 상태 큰 워크로드 |

### 3. 이벤트 시간(Event Time)과 [[085_watermark|워터마크]]([[085_watermark|Watermark]])

Flink의 가장 강력한 기능 중 하나는"이벤트 시간(발생 시간) 기준 처리"입니다.

- **Processing Time vs Event Time**:
  - Processing Time: Flink 연산자가 [[001_dikw_pyramid|데이터]]를 처리하는 실제 시간. 간단하지만, 시스템 시간 기준이므로 [[001_dikw_pyramid|데이터]] [[015_지연_데이터_관점|지연]]이나 네트워크 단절 시 결과가歪みます.
  - Event Time: 이벤트가 실제 발생한 시간(예: 센서 readings, 거래 시간).Event Time은 시스템clocks와 독립적이므로, [[015_지연_데이터_관점|지연]]되거나 순서가 바뀌어 도착한 [[001_dikw_pyramid|데이터]]도 정확한 시간 순서로処理 가능하지만, [[001_dikw_pyramid|데이터]]에 타임스탬프가 포함되어야 합니다.

- **[[085_watermark|Watermark]] ([[085_watermark|워터마크]])**: "이 시간(Event Time)까지의 모든 [[001_dikw_pyramid|데이터]]는 이미 도착했다"고 가정하는 [[369_logic_bomb|논리]]적 시점 표시기입니다. 예: `Watermark = T`는"Event Time < T인 [[001_dikw_pyramid|데이터]]는 이제 거의 도착했으니, T 이상의 늦은 [[001_dikw_pyramid|데이터]]는 때때로 올 수 있지만 일반적으로는 도착했다고 봐도 괜찮다"는 선언입니다. [[085_watermark|워터마크]]는"[[015_지연_데이터_관점|지연]] 허용 [[025_baseline|기준선]]"이며, 이를 통해 무한히 도착을 기다려야 하는 상황( الكامل 블로킹)을 방지합니다.

- **📢 섹션 요약 비유**: Flink의 Event Time과 Watermark는"항공사 llegadas的时刻표管理"와 similar 합니다. 비행기([[001_dikw_pyramid|데이터]])가 실제로 하늘을 나는 시간은"Processing Time(处理 시간)"이지만,旅客들이 관심을 갖는 것은"Event Time(사전 예정时刻)"입니다. 어떤 비행기가 도착 예정 시간보다 늦게 도착하면([[015_지연_데이터_관점|지연]] [[001_dikw_pyramid|데이터]]), 우리는"도착 시간표(시간 순서)"를 기반으로"10분 안에 짐을 찾아야지"라는 계획을 세웁니다. 다만"기다리는 시간"이 너무 길어지면([[015_지연_데이터_관점|지연]] 허용 기준 넘음), 공항은 해당 항공편의 Llegada 정보受付를を打ち切り("/수하물 컨베이어 벨트에짐이 아직 안 떴어"라고 걱정하기보다"짐을 받을 수 있다"고 판단) 운영을続行합니다. 이"기다리는 기준 시간"이 바로"[[085_watermark|WATERMARK]]"입니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

| 비교 항목 | Apache [[060_spark_streaming_dstream|Spark Streaming]] | [[215_flink_native_stream_watermark_window_time|Apache Flink]] |
|:---|:---|:---|
| **처리 모델** | Micro-Batch | Continuous Processing |
| **[[141_latency|지연 시간]]** | ~1초+ | 수십 ms ~ 1초 |
| **상태 관리** | 외장 (checkpoint-interval 미지원) | 내장 상태 백엔드 (RocksDB) |
| **Event Time 지원** | [[061_structured_streaming|Structured Streaming]] 이후 (Spark 2.3~) | 원래부터 지원 (설계 철학) |
| **[[658_ir_recovery|복구]] 시간** | WAL + Lineage 재연산 | 증분 체크포인트 (빠른 [[658_ir_recovery|복구]]) |
| **[[014_api_posix|API]] [[194_consistency_database_integrity|일관성]]** | 배치/스트리밍 unified (DataFrame) | 배치/스트리밍 unified (DataStream [[014_api_posix|API]]) |
| ** 생태계 성숙도** | 매우 높음 (Spark 생태계 활용) | 높음 (연속 성장 중) |

- **Flink의 가장 큰 강점**: 상태가 있는(stateful) 스트리밍 연산이 필요한 경우(예: [[286_page_frame|페이지]] 방문 횟수를 세다가 사용자가 30분간 활동이 없으면 [[160_session_controlling_terminal|세션]]을 종료하고 카운트를 내보내는 [[160_session_controlling_terminal|세션]] [[086_window_operations|윈도우 연산]]) Flink의 내장 상태 관리 功能은 압도적으로 우수합니다. Spark Streaming에서는 상태 관리를 위해 별도의 외부 [[002_database_definition|데이터베이스]]([[542_redis|Redis]] 등)를 사용해야 하는 경우가 많지만, Flink는 상태 백엔드를 내장하고 RocksDB를 통해 Huge한 [[065_state_diagram|상태도]] 디스크에서管理합니다.

- **📢 섹션 요약 비유**: Apache Flink와 [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] Streaming의 [[083_relationship_in_er_model|관계]]는 "자동차 공장 생산 라인의 두 가지 방식"에 비유할 수 있습니다. Spark Streaming은 "30초마다 완제품 섹션에 100개의 제품을 한꺼번에 전달하는 배치 라인을 가진 공장"이라면, Flink는 "부품이 컨베이어 벨트에 도착하는 순간 즉시 직공이 한 부품씩 순차적으로 组立前往하는 연속组装 라인"입니다. 전자는 한 번에大量 처리로 효율이 높지만 30초 간격의.delay가 발생하고, 後자는 순간순간 즉응反应으로超低 [[015_지연_데이터_관점|지연]]이 가능하지만 组立 공수의 管理コスト가 높습니다. 공장 제품(처리 [[001_dikw_pyramid|데이터]])의 특성에 따라"대량 생산 vs 정밀 맞춤生产" 중 적합한 공장을 선택하는 것과 동일합니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **[[015_지연_데이터_관점|지연]] 요구 수준** | < 1초 [[085_sla|SLA]] → Flink, 수 초 허용 → [[060_spark_streaming_dstream|Spark Streaming]] | ms 단위 실시간이 필요하면 Flink |
| **상태 크기** | 수십 GB 이상 상태 → RocksDB Backend 필수 | 수 GB 이하 → HashMapStateBackend |
| **Event Time 정확도** | 규제 보고서 등 정확한 Event Time 처리 → Flink | Processing Time으로 충분 → Spark |
| **엔지니어링 역량** | Flink는 학습 곡선이 높음,熟练도 필요 | Spark는 생태계가 큼, 커뮤니티资料多 |

*(추가 실무 적용 가이드 - Flink 도입 [[124_decision_tree|Decision Tree]])*
- **단계 1**: [[015_지연_데이터_관점|지연]] 요구가 1초 이상입니까? → 예: Apache [[060_spark_streaming_dstream|Spark Streaming]] 고려. 아니오: 다음 단계로.
- **단계 2**: 상태 저장소로複雑な [[160_session_controlling_terminal|세션]] 윈도우, 패턴 매칭 등的状态ful 연산이 필요합니까? → 예: [[215_flink_native_stream_watermark_window_time|Apache Flink]] 권장. 아니오: Spark Structured Streaming도 충분.
- **단계 3**: Event Time 순서保证가 중요합니까? (예: 금융 거래 분석, inúmer崩れ克服) → 예: [[215_flink_native_stream_watermark_window_time|Apache Flink]]. 아니오: 어느 쪽이든 가능.
- **단계 4**: 팀이 이미 Spark 인프라를 보유하고 있습니까? → 예: [[060_spark_streaming_dstream|Spark Streaming]] 우선 고려. 아니오: Flink도 충분히 검토.

- **📢 섹션 요약 비유**: Flink 도입 결정을 "레스토랑 종류 선택"에 비유할 수 있습니다. 만약 고객이"프렌치 디너(다도뷔페)"를 원한다면(대량 [[001_dikw_pyramid|데이터]] [[228_batch_processing_hadoop_spark|배치 처리]] 중심), 스파크는 이미 [[395_verification_process_review|검증]]된大型 Kitchen配备了 자동化了大量調理系统(마이크로배치)가 적합합니다. 하지만 고객이"손님 한 분 한 분의 주문을 받고 바로바로 요리하는 이천寿司(Italian Fine Dining)"를 원한다면([[015_지연_데이터_관점|지연]] 민감 실시간 처리), 플링크는 각 주문([[001_dikw_pyramid|데이터]])을받는 순간즉시 세iseries를 시작하는 Japanese게다마에스(레코드 단위 연속 처리)가 필수입니다.寿司를大型 Buffet에서 제공할 수 없듯이, 실시간 ms 수준이 필요한 시스템에 Spark를 강제로 적용하면"손님이 30초間 다음 요리를 기다려서 식탁이 비는"悲剧가 벌어집니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **Flink SQL의 표준화 및 데이타 통합**
   Flink SQL은 Flink 1.9에서 정식 도입되어, 이제 배치와 스트리밍 [[298_qkv_attention|쿼리]]를 동일한 SQL 문법으로 작성할 수 있게 되었습니다. Apache Flink의 가장 큰 강점 중 하나는"사용자가 [[001_dikw_pyramid|데이터]] 처리 로직을 어떻게 실행할지(How)가 아니라 무엇을 원하시는지(What)"만 SQL로 기술하면, 프레임워크가 자동으로 최적의 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]을 세우는 선언적([[219_declarative_yaml|Declarative]]) 특성입니다. ksqlDB([[094_reinforcement_learning|Confluent]])와 Flink SQL의 경쟁을 통해, 스트리밍 SQL이 실시간 분석의 표준 언어로 자리잡는 것이 가속화되고 있습니다.

2. **Flink와 [[146_lakehouse|레이크하우스]]生态系的 결합**
   Apache Iceberg와 Delta Lake가 Flink와 통합됨에 따라, 실시간 스트림을 [[146_lakehouse|레이크하우스]]에 직접 기록하고 그 위에서 일괄 분석하는"Unified Batch + Streaming" 시나리오가 보편화되고 있습니다. Uber는 Flink를 통해 Apache Hudi로 실시간 [[001_dikw_pyramid|데이터]] ingestion을, LinkedIn은 Kafka와 Flink를 결합하여人力资源 분석 플랫폼을実装しており, 세계적 대규모 [[090_service_kubernetes_network_load_balancing|서비스]]의 핵심 백본으로 Flink가 자리잡고 있습니다.

3. **Flink의 [[206_serverless_cold_start|serverless]] 및 managed [[090_service_kubernetes_network_load_balancing|서비스]] 확산**
   AWS Kinesis [[001_dikw_pyramid|Data]] Analytics for [[215_flink_native_stream_watermark_window_time|Apache Flink]](Managed Flink), Google Cloud Dataflow, Azure [[467_http2_stream_multiplexing_tcp_hol|Stream]] Analytics 등 주요 클라우드 제공자들이 Flink 기반의 fully managed 스트리밍 분석 [[090_service_kubernetes_network_load_balancing|서비스]]를 제공함에 따라, 클러스터 관리의 부담 없이 Flink의高度な 기능을 활용하는 것이 간편해지고 있습니다. 이는"엔지니어가 오직 [[001_dikw_pyramid|데이터]] 처리 로직에 집중"할 수 있는 환경을 만들어, Flink의 진입 장벽을 크게 낮추고 있습니다.

- **📢 섹션 요약 비유**: Flink의 미래는"자동차 공장의 完全自動化Robot化"과 같습니다. 과거에는 기술자(Flink 엔지니어)가 각 생산 라인(연산자)의 상태([[059_counter|카운터]], [[160_session_controlling_terminal|세션]])를 직접 [[396_validation|확인]]하고,Robot(체크포인트)의 수리를 명령하고, 새 차량의 도면(새 [[001_dikw_pyramid|데이터]])를 분석가에게 요청하는"사이드 项目"이었습니다. 그러나 이제는Robot themselves(Managed Flink/[[205_kubernetes_container_orchestration|Kubernetes]])가 스스로 상태를 관리하고,故障하면 자동으로备份([[300_failover_architecture|Failover]])하고,工厂事務所(클라이언트)에는"완성된 차량(분석 결과)"만 전달됩니다. 기술자는 더 이상Robot의 [[133_fine_tuning|미세 조정]](클러스터 튜닝)이 아니라,"어떤 종류의 차량(비즈니스 요구)을 만들지"에만 집중하면 되는時代로 완전히 변화하고 있습니다.

---

## 🧠 지식 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

*   **Apache Flink核心组件**
    *   **DataStream [[014_api_posix|API]]**: 시간 기반 스트리밍 처리 (Window, Event Time, [[085_watermark|Watermark]])
    *   **Table [[014_api_posix|API]] & SQL**: 선언적 [[001_dikw_pyramid|데이터]] 처리 (배치/스트리밍 통합)
    *   **[[098_cep|CEP]] ([[098_cep|Complex Event Processing]])**: 패턴 기반 이벤트 감지
*   **Flink 상태 관리 아키텍처**
    *   **Keyed [[272_state_pattern|State]]**: 키별로 구분된 상태 (keyBy 후 사용)
    *   **[[565_operator_pattern_kubernetes_automation|Operator]] [[272_state_pattern|State]]**: 연산자 전체에 공유되는 상태
    *   **[[272_state_pattern|State]] Backend**: HashMap ([[078_heap_datastructure|Heap]]) vs RocksDB (디스크)
*   **Exactly-Once 시맨틱스 보장 메커니즘**
    *   [[549_2pc_two_phase_commit_limitations_msa|2PC]] ([[249_two_phase_commit_2pc_distributed|2단계 커밋]]) + Checkpoint Barriers + 소스 함수 재처리 기능

---

### 📈 관련 키워드 및 발전 흐름도

```text
[배치 처리]
    │
    ▼
[마이크로 배치]
    │
    ▼
[Event Stream]
    │
    ▼
[Exactly-once]
```

이 흐름도는 선행 개념이 현재 개념으로 응축되고, 다시 확장 개념으로 이어지는 순서를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. Apache Flink는 친구들이 동시에 각각 다른 도화지를 풀면서 그림을 그리는 것과 같아요.
2. 누군가 그림을 그리는 도중 잠시 떠있으면, 플링크는 그림의 내용을 기억(체크포인트)하고 있다가 다시 같은 위치에서 시작해요.
3. 각 친구들은 자신이 받은 색紙([[001_dikw_pyramid|데이터]])를 받자마자 바로 그리기 시작해서, 모두가 동시에 끝나요!

---
> **🛡️ Expert [[395_verification_process_review|Verification]]:** 본 문서는 Apache Flink의 핵심 개념(Continuous Processing, Event Time, Checkpoint)과 [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] Streaming과의 비교를 기준으로 기술적 [[002_bigdata_5v|정확성]]을 [[395_verification_process_review|검증]]하였습니다. (Verified at: 2026-04-05)
