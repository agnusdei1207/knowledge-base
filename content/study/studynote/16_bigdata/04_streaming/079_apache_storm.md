+++
title = "04. Apache Storm"
weight = 79
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[044_apache_storm|아파치 스톰]]([[044_apache_storm|Apache Storm]])은 과거 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]) 중심의 굼벵이 같은 배치(Batch) 처리 시대에 혜성처럼 등장하여, 수백만 건의 트윗이나 센서 [[001_dikw_pyramid|데이터]]를 **메모리 상에서 '이벤트 1건'이 발생할 때마다 1밀리초(ms) 단위의 미친 속도로 즉각 낚아채어 계산해 내는 1세대 진정한 실시간 스트림(Real-time [[467_http2_stream_multiplexing_tcp_hol|Stream]]) 프로세싱 엔진**이다.
> 2. **가치**: [[001_dikw_pyramid|데이터]]를 물고기(Tuple)로 비유하면, 물고기를 강에 풀어놓는 수도꼭지 역할의 **스파우트(Spout)** 와, 물고기를 그물로 낚아채어 요리하고 다음 사람에게 던져주는 **[[236_vault_dynamic_secrets_ttl|볼트]](Bolt)** 라는 직관적인 노드들로 네트워크(토폴로지)를 구성하여, [[645_data_pipeline_acceleration|데이터 파이프라인]]의 복잡한 비즈니스 로직을 완벽한 흐름도([[401_bayesian_network_dag_causality|DAG]])로 [[198_abstraction_control_data_process|추상화]]해 냈다.
> 3. **융합**: 비록 나중에 나온 Flink나 Spark Streaming의 '마이크로 배치' 및 '상태([[272_state_pattern|State]]) 관리' 기능에 밀려 현재 주류 시장에서는 거의 퇴출당했지만, 스트리밍의 개념 자체를 정립하고 [[459_quic_fec_forward_error_correction|초기]] 트위터(Twitter)의 실시간 트렌드를 지배하며 현대 **빅데이터 카파([[235_kappa|Kappa]]) 아키텍처의 위대한 사상적 밑거름**으로 융합된 살아있는 전설이다.

---

## Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

- **개념**: 네이선 마르츠(Nathan Marz)가 트위터(Twitter)에 입사해 [[191_oss_license_compliance|오픈소스]]로 푼 빅데이터 실시간 연산 프레임워크다. [[018_mapreduce|맵리듀스]]([[018_mapreduce|MapReduce]])가 [[001_dikw_pyramid|데이터]]를 거대한 덩어리로 잘라서 한참 뒤에 답을 내놓는 "가마솥"이라면, 스톰은 [[001_dikw_pyramid|데이터]]가 [[123_pipe|파이프]]를 타고 흘러갈 때마다 즉각적으로 불을 쏘아대는 "토치 램프"다. 작업을 한 번 시작하면 끝이 없다(Never-ending). 끊임없이 쏟아지는 물줄기(스트림)를 영원히 쳐다보고 계산만 한다.
- **필요성**: 트위터에서 전 세계 사람들이 "지진 났어!"라고 수백만 건의 트윗을 쏘는데, [[843_hadoop_rack_awareness_data_replication_topology|하둡]]으로 분석하면 내일 아침에서야 "어제 지진 났었네"라는 결과가 나온다. 이건 재앙이다. [[001_dikw_pyramid|데이터]]를 모아두고 돌리는 게 아니라, "[[001_dikw_pyramid|데이터]]가 들어오는 그 0.001초의 찰나에 메모리에 떠 있는 상태에서 바로 해시태그를 카운팅하고 폐기해버리는" 극단적인 초지연(Ultra-low [[141_latency|Latency]]) 아키텍처가 절실했다. 이 요구를 만족하기 위해 디스크 I/O를 완벽하게 배제하고, 수십 대의 서버 메모리(RAM)를 [[123_pipe|파이프]]라인으로 연결해 버린 스톰(Storm)이 탄생했다.
- **💡 비유**: [[843_hadoop_rack_awareness_data_replication_topology|하둡]]([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]]) 배치가 수만 명의 투표용지를 거대한 투표함에 꽉 채운 뒤 밤 12시에 한꺼번에 뜯어서 개표하는 **'전통적 투표 시스템'** 이라면, 스톰(Storm)은 사람들이 출구에서 투표용지를 넣자마자 전자 센서가 표를 인식하고 전광판 숫자가 실시간으로 차르륵 올라가는 **'실시간 전자 개표기'** 다. 기다림 없이 그 순간의 정답(트렌드)을 바로 알 수 있다.

- **📢 섹션 요약 비유**: 스톰은 거대한 공장의 컨베이어 벨트입니다. 부품([[001_dikw_pyramid|데이터]]) 100개가 모일 때까지 기다렸다 작업하는 게 아니라, 부품 1개가 눈앞에 지나가면 망치 든 사람(Bolt)이 깡! 치고 바로 다음 사람에게 넘기는, 세상에서 가장 성질 급하고 쉴 틈 없이 돌아가는 실시간 조립 라인입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 스톰의 심장: 스파우트(Spout)와 [[236_vault_dynamic_secrets_ttl|볼트]](Bolt)의 토폴로지(Topology)

스톰 개발자는 코드를 짤 때 `if-else` 만 짜는 게 아니라, 물이 흘러갈 [[123_pipe|파이프]]의 배관(Topology) 도면을 그려야 한다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 Apache Storm의 파이프라인(Topology) 배관도             │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ Apache Kafka 등 원본 소스 ]                                       │
  │          │                                                        │
  │          ▼ (데이터 튜플 1건씩 꿀꺽!)                                  │
  │  ┌─────────────────┐                                              │
  │  │   Spout (수도꼭지)│ ──▶ Storm의 시작점. 외부에서 데이터를 퍼 올려서      │
  │  └─────────────────┘      파이프라인 안으로 뿜어내는 역할을 전담함.           │
  │          │                                                        │
  │          ▼ (단어 자르기)                                             │
  │  ┌─────────────────┐                                              │
  │  │ Bolt 1 (필터/변환)│ ──▶ "오늘 강남에 불 났네" 문장을 받아 단어로 쪼갬.    │
  │  └─────────────────┘      ('오늘', '강남', '불')                     │
  │          │                                                        │
  │          ▼ (단어별로 길을 나눠서 던짐: Field Grouping)                    │
  │  ┌─────────────────┐    ┌─────────────────┐                       │
  │  │ Bolt 2-A (카운트) │    │ Bolt 2-B (카운트) │ ──▶ 쪼개진 단어를 받아서  │
  │  └─────────────────┘    └─────────────────┘      +1씩 더하는 집계기. │
  │          │                      │                                 │
  │          ▼                      ▼                                 │
  │   [ Redis / 대시보드 화면 ] (최종 뷰 출력)                               │
  │                                                                   │
  │  ▶ 핵심 원리: 하둡의 맵리듀스(Job)는 한 번 끝나면 프로그램이 종료된다.          │
  │             하지만 스톰의 Топология(Topology)는 끄지 않는 이상 1년이고       │
  │             10년이고 메모리에 둥둥 떠서 영원히 데이터가 지나가길 기다린다.      │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 스톰 클러스터 안에는 [[075_kubernetes_k8s_cluster_architecture|마스터 노드]]인 **Nimbus(님버스)** 가 전체를 지휘하고, 워커 노드인 **Supervisor(수퍼바이저)** 들이 Spout와 Bolt라는 일꾼([[092_thread_lwp|Thread]])들을 뱃속에 품고 24시간 미친 듯이 일한다. 이 구조의 묘미는 **유연한 튜닝(Parallelism)** 이다. 만약 [[001_dikw_pyramid|데이터]]가 너무 많이 들어와서 Bolt 1(자르기)이 버거워하면, 개발자는 코드 수정 없이 [[009_config|설정]] [[501_file_definition_logical_record|파일]] 하나만 건드려 Bolt 1을 [[016_replication_factor|복제]]해 10명으로 늘려버릴 수 있다. 병목이 생기는 배관(Bolt)만 골라서 굵기를 수백 배로 늘려주는 클라우드 확장의 미학이다.

---

### 스톰의 [[296_fault_tolerance_architecture|결함 허용]]([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]])과 XOR 마법

메모리 상에서 1건씩 핑핑 날리다가 서버 전원 코드가 뽑히면 그 1건의 [[001_dikw_pyramid|데이터]]는 공중에서 증발한다. 스톰은 이 치명적 단점을 방어하기 위해 엄청난 추적 시스템을 구축했다.

- Spout가 물고기(Tuple A)를 하나 뿜어낼 때, 그 꼬리에 ID를 단다.
- 이 [[063_relation_tuple_cardinality|튜플]]이 Bolt 1을 거쳐 쪼개지고, Bolt 2를 거쳐 최종 DB에 도달할 때까지 수많은 자식 [[063_relation_tuple_cardinality|튜플]]들을 낳는다. 스톰은 내부의 비밀 요원(Acker)을 시켜 이 [[063_relation_tuple_cardinality|튜플]] 가계도의 모든 족보(Tree)를 추적한다.
- 족보 추적에 메모리가 너무 많이 드는 걸 막기 위해, 마법의 수학 연산인 **XOR [[073_bit|비트]] 연산** 을 쓴다. (A XOR B XOR A XOR B = 0 이 되는 원리). [[063_relation_tuple_cardinality|튜플]]이 출발할 때와 무사히 끝났을 때의 ID를 XOR 쳐서 `0` 이 딱 떨어지면 "아, 이 [[001_dikw_pyramid|데이터]] 1건은 무사히 [[123_pipe|파이프]]라인을 통과했군!"이라며 완전 종료(Ack)를 때린다.
- 만약 중간 서버가 터져서 XOR 결과가 0으로 안 떨어지고 [[573_timeout_retry_backoff_strategy|타임아웃]]이 나면? **Spout가 똑같은 원본 [[001_dikw_pyramid|데이터]]를 1초 뒤에 쿨하게 다시 뿜어낸다(Replay).**

- **📢 섹션 요약 비유**: 택배([[063_relation_tuple_cardinality|튜플]])를 보낼 때 중간 집하장에서 물건을 잃어버리면 낭패입니다. 스톰은 택배 상자가 각 지역을 통과할 때마다 본사에 "삐빅! 통과!" 하고 [[130_signal|신호]]를 보냅니다(XOR 연산). 만약 10초가 지났는데 도착 [[130_signal|신호]]가 완성(0)되지 않으면, 출발지(Spout)에서 무자비하게 새 물건을 다시 복사해서 쏴버리는 지독한 배달 [[396_validation|확인]] 시스템입니다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 실시간 스트림 3대 천왕 결전: Storm vs [[060_spark_streaming_dstream|Spark Streaming]] vs Flink

스톰이 왕좌에서 물러나고 3세대(Flink)로 권력이 넘어간 아키텍처의 패러다임 시프트다.

| 비교 척도 | [[044_apache_storm|Apache Storm]] (1세대) | [[060_spark_streaming_dstream|Spark Streaming]] (2세대) | **[[215_flink_native_stream_watermark_window_time|Apache Flink]] (3세대 대세)** |
|:---|:---|:---|:---|
| **[[001_dikw_pyramid|데이터]] 처리 사상** | **진짜 스트리밍 (Native [[467_http2_stream_multiplexing_tcp_hol|Stream]])**<br>들어오는 즉시 1건 단위(Event)로 쳐냄. | **마이크로 배치 (Micro-batch)**<br>스트리밍인 척하지만, 사실 1초 치 [[001_dikw_pyramid|데이터]]를 모았다가 미니 [[018_mapreduce|맵리듀스]]로 침. | **진짜 스트리밍 (Native [[467_http2_stream_multiplexing_tcp_hol|Stream]])**<br>스톰의 1건 처리 + 스파크의 안정성을 모두 훔쳐 온 끝판왕. |
| **[[141_latency|지연 시간]] ([[141_latency|Latency]])**| **Sub-ms (1밀리초 미만, [[148_5g_embb_urllc_mmtc|초고속]] 1위)** | 1초 ~ 수초 (약간의 버벅거림 존재) | Sub-ms (스톰과 맞먹는 1위) |
| **정확도 보장 (Semantics)**| **At-Least-Once** (최소 1번 이상. 서버 죽으면 2번 처리될 수도 있어 정합성 꼬임) | **Exactly-Once** (정확히 단 1번 처리 보장) | **Exactly-Once** (정확히 단 1번 처리 완벽 보장) |
| **상태 관리 ([[272_state_pattern|State]])** | 멍청함. "1시간 동안 집계해 줘" 같은 윈도우(Window) 함수를 짜려면 개발자가 피똥 쌈. | 훌륭함. 배치(Batch) 엔진 뼈대라 그룹핑 연산에 능함. | **신의 경지.** 자체 내장 DB(RocksDB)를 품고 있어 과거 상태를 기가 막히게 기억함. |

스톰이 버림받은 결정적 이유는 두 가지다. 첫째, 네트워크 에러 시 [[001_dikw_pyramid|데이터]]를 2번 중복해서 더해버리는 **'At-Least-Once'의 저주** 때문에 은행 결제 시스템(돈 계산)에는 절대 쓸 수 없었다. 둘째, "최근 5분 동안 가장 많이 나온 단어"를 구하려면 지난 5분간의 [[001_dikw_pyramid|데이터]](상태/[[272_state_pattern|State]])를 기억해야 하는데, 스톰은 건망증이 심해서 개발자가 외부 DB([[542_redis|Redis]])를 끌고 와 억지로 구현해야 했다(개고생). 결국 이 모든 걸 프레임워크 자체에서 완벽하게 제공해 버리는 Flink에게 천하를 내어주고 말았다.

- **📢 섹션 요약 비유**: 스톰(Storm)은 엄청 발이 빠른 10대 배달부입니다. 1건 들어오면 미친 듯이 빨리 뛰어가지만, 가끔 물건을 2개 줘버리거나(중복) 자기가 어제 뭘 배달했는지 다 까먹어 버립니다. Flink는 발도 똑같이 빠른데 꼼꼼한 수첩([[272_state_pattern|State]])까지 들고 다니며 절대 중복 배달(Exactly-Once)을 안 하는 엘리트 프로 택배 기사라 세대교체가 된 것입니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 구형 스톰 아키텍처의 중복 집계(Duplicate Count) 사고와 [[087_trie|트라이]]던트(Trident)의 한계**: 한 금융사에서 5년 전 구축한 스톰 [[123_pipe|파이프]]라인으로 '실시간 사기 탐지([[267_gnn_fraud_detection_knowledge_graph|FDS]])' 지표를 집계했다. 서버가 재부팅될 때마다 특정 유저의 거래 시도 횟수가 스톰의 Replay(다시 쏘기) 기능 때문에 2번, 3번씩 중복으로 합산(At-least-once)되었고, 멀쩡한 유저를 사기꾼으로 오인해 계좌를 블록 시키는 참사가 났다.
   - **기술사적 판단**: 스톰의 고질병인 **[[001_dikw_pyramid|데이터]] 중복 오염 사태**다. 과거 스톰 진영은 이를 막기 위해 [[087_trie|트라이]]던트(Trident)라는 확장판을 만들어 [[191_transaction_concept_states|트랜잭션]] 개념(Exactly-once)을 억지로 우겨넣었다. 하지만 [[087_trie|트라이]]던트를 쓰면 스톰 특유의 "1밀리초 [[148_5g_embb_urllc_mmtc|초고속]]" 장점이 박살 나고 스파크처럼 느린 배치형으로 퇴보해 버렸다. 아키텍트는 낡은 스톰+[[087_trie|트라이]]던트 코드를 끌어안고 침몰하지 말고, **상태([[272_state_pattern|State]]) 체크포인트 [[022_snapshot_backup_architecture|스냅샷]] 기능을 코어 레벨에서 완벽하게 지원하는 [[215_flink_native_stream_watermark_window_time|Apache Flink]] [[123_pipe|파이프]]라인으로 전면 마이그레이션([[213_refactoring_cloud_native_rearchitecture|Refactor]])** 하는 결단을 내려야 금융 사고를 끊어낼 수 있다.

2. **시나리오 — 그럼에도 스톰(Storm)이 필요한 초극단 [[141_latency|지연 시간]](Ultra-low [[141_latency|Latency]]) [[064_relation_domain|도메인]]**: 초고주파 트레이딩(HFT, High-Frequency Trading)을 하는 퀀트 헤지펀드. 호가 창 [[001_dikw_pyramid|데이터]]가 변하는 순간 0.001초 만에 "사라!" 또는 "팔아라!"라는 시그널을 던져야 한다. 0.5초의 [[015_지연_데이터_관점|지연]]([[141_latency|Latency]])이 발생하는 Spark Streaming은 아예 명함도 못 내미는 판국이다.
   - **기술사적 판단**: 이 극단의 마이크로초(Microsecond) [[064_relation_domain|도메인]]에서는 무겁고 거대한 Flink조차 오버헤드가 될 수 있다. 가장 멍청하지만 구조가 가장 단순무식하게 가볍고 1건 단위의 이벤트 [[123_pipe|파이프]]라인(Tuple-by-Tuple)을 직관적으로 제공하는 **오리지널 [[044_apache_storm|Apache Storm]](또는 Heron)** 만이 정답이 될 수 있다. 스톰은 중간에 [[001_dikw_pyramid|데이터]]를 뭉치거나(Windowing) 상태를 저장하느라 머리를 쓰지 않고 오직 `Input ➔ Output` 으로 뚫려있어, 복잡한 상태 관리가 필요 없는 순수 "[[148_5g_embb_urllc_mmtc|초고속]] 룰 엔진(Rule Engine)" 아키텍처에서는 여전히 누구도 따라올 수 없는 면도날 같은 [[282_performance_tactics|성능]]을 자랑한다.

### 레거시 스트리밍 엔진 유지보수 아키텍트 [[435_checklist_based_testing|체크리스트]]
- **[[179_kafka_flink_watermark_time_window|Kafka]]-Spout 오프셋(Offset) 관리의 주도권**: 스톰이 [[179_kafka_flink_watermark_time_window|카프카]]에서 [[568_logs_distributed_logging_elk_fluentd|로그]]를 빨아들일 때, 자기가 어디까지 읽었는지 북마크(Offset)를 [[179_kafka_flink_watermark_time_window|카프카]] 안의 `__consumer_offsets` 쪽에 적고 있는가, 아니면 스톰의 님버스([[798_distributed_lock_zookeeper_consensus|Zookeeper]]) 쪽에 적고 있는가? 옛날 방식대로 주키퍼에 적어두면 장애 시 북마크가 꼬여 대량 유실이 일어날 [[130_probability|확률]]이 높다. 최신 [[179_kafka_flink_watermark_time_window|카프카]] 스펙에 맞는 KafkaSpout [[288_version_ihl_tos_total_length|버전]] 업그레이드가 필수적이다.
- **Bolt 튜닝의 예술 (병목 구간 탐지)**: 토폴로지가 느려질 때, 무턱대고 모든 Bolt의 [[092_thread_lwp|스레드]]를 2배로 늘리지 마라. `자르기 Bolt` 는 널널한데, DB에 넣는 `저장 Bolt` 쪽의 큐([[058_queue|Queue]])가 100% 꽉 차서 목이 막히는 현상(Back-pressure)이 원인일 수 있다. 스톰 UI 대시보드에서 `Capacity` 지표가 1.0(100%)에 육박하는 병목 Bolt 하나만 골라서 [[092_thread_lwp|스레드]]([[150_task|Task]])를 수평 확장([[202_scale_out_distributed_horizontal_expansion|Scale-out]])해 주는 정밀 타격 튜닝 능력이 요구된다.

- **📢 섹션 요약 비유**: 컨베이어 벨트가 밀린다고 일꾼 10명을 전부 2배로 늘리면 인건비만 날립니다. 사과를 자르는 일꾼 1번은 팽팽 노는데, 사과를 상자에 예쁘게 담는 일꾼 10번 쪽만 사과 산더미가 쌓여있다면, 오직 일꾼 10번(병목 Bolt) 자리에만 사람을 3명 더 투입하는 것이 스톰 [[430_index_fast_full_scan|병렬]]성 튜닝의 핵심 지혜입니다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과
- **실시간(Real-Time) 분석 시대의 개막**: '배치(Batch)의 시대'에서 '스트리밍(Streaming)의 시대'로 넘어가는 인류 빅데이터 역사의 1막을 가장 화려하게 열어젖혔다. "지금 이 순간 세상에서 가장 인기 있는 트윗이 뭐야?"라는 질문에 단 1초 만에 대답을 뱉어내며 비즈니스의 심박수를 극한으로 끌어올렸다.
- **개발 [[198_abstraction_control_data_process|추상화]]([[198_abstraction_control_data_process|Abstraction]])의 예술**: 복잡한 네트워크 통신, 멀티 [[092_thread_lwp|스레드]] 프로그래밍, 큐([[058_queue|Queue]]) 연동 등 수만 줄의 [[136_variance|분산]] 처리 코드를 다 숨기고, 개발자는 오직 "물 뽑아라(Spout)"와 "물고기 요리해라(Bolt)" 단 2개의 클래스(Interface)만 짜면 수백 대의 서버가 알아서 [[136_variance|분산]] 계산을 끝내주는 위대한 프레임워크 뼈대를 완성했다.

### 미래 전망 ([[531_cloud_native_architecture|클라우드 네이티브]]와 Flink/Beam으로의 왕좌 양보)
Apache Storm은 훌륭했지만 너무 늙었다. 현재 스트리밍 시장의 제왕 자리는 완벽한 '상태 관리(Stateful)'와 '[[083_cross_validation|정확히 한 번]](Exactly-once)'을 보장하는 **[[215_flink_native_stream_watermark_window_time|Apache Flink]]** 가 굳건히 지키고 있으며, 구글(Google)이 주도하는 **Apache Beam** 은 "네가 짠 코드가 스톰에서 돌든, 플링크에서 돌든, 스파크에서 돌든 똑같이 돌아가게 해 줄게!"라며 아예 스트림 엔진의 상위 [[198_abstraction_control_data_process|추상화]](Unified [[014_api_posix|API]]) 표준으로 생태계를 집어삼켰다. 스톰은 이 거대한 혁명의 징검다리로서 찬란했던 사명을 다하고 역사의 뒤안길로 명예롭게 퇴장 중이다.

### 결론
[[044_apache_storm|아파치 스톰]]([[044_apache_storm|Apache Storm]])은 [[843_hadoop_rack_awareness_data_replication_topology|하둡]]이 쌓아놓은 묵직한 문서 보관소 한가운데 나타나 "세상은 지금 이 순간에도 빛의 속도로 변하고 있다!"라고 외치며 폭풍우(Storm)처럼 몰아쳤던 빅데이터의 반항아였다. Spout와 Bolt라는 기막힌 토폴로지 철학을 통해, 우리는 거대한 [[123_pipe|파이프]]라인의 물줄기를 눈으로 보고 조립할 수 있게 되었다. 비록 그 후배들(Flink, Spark)의 화려한 스펙에 밀려 더 이상 트렌드의 중심에 서지 못하지만, 오늘날 당신이 스마트폰 앱에서 "현재 실시간 검색어 1위"나 "1초 전 터진 나의 카드 결제 알람"을 당연하다는 듯이 누리고 있는 그 이면에는, 태초에 빅데이터의 시간 축을 "내일"에서 "지금 당장(Real-time)"으로 멱살 잡고 끌고 왔던 스톰의 위대한 개척 정신이 숨 쉬고 있음을 [[001_dikw_pyramid|데이터]] 엔지니어들은 결코 잊지 말아야 한다.

---

## 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

| 개념 명칭 | [[083_relationship_in_er_model|관계]] 및 시너지 설명 |
|:---|:---|
| **[[214_kafka_pubsub_topic_partition_offset_broker|Apache Kafka]] ([[214_kafka_pubsub_topic_partition_offset_broker|아파치 카프카]])** | 스톰(Storm)의 영혼의 단짝. 스톰은 기억력이 없어서 [[001_dikw_pyramid|데이터]]가 날아가면 끝인데, [[179_kafka_flink_watermark_time_window|카프카]]가 앞에 버티고 서서 [[001_dikw_pyramid|데이터]]를 무한 보존해 줌으로써 스톰의 Spout가 언제든 맘 편히 [[001_dikw_pyramid|데이터]]를 다시 빨아들일 수 있게 해 준다. |
| **[[215_flink_native_stream_watermark_window_time|Apache Flink]] ([[215_flink_native_stream_watermark_window_time|아파치 플링크]])** | 스톰을 역사 속으로 밀어낸 3세대 스트리밍 제왕. 스톰의 장점(1건씩 처리)을 훔치면서도, 치명적 약점이던 '중복 처리(At-least-once)'와 '건망증([[239_stateless_redis|Stateless]])'을 내장 DB로 완벽하게 극복한 끝판왕이다. |
| **[[095_lambda_architecture|람다 아키텍처]] ([[095_lambda_architecture|Lambda Architecture]])** | [[843_hadoop_rack_awareness_data_replication_topology|하둡]](Batch)과 스톰(Speed)을 양손에 쥐고 [[001_dikw_pyramid|데이터]]를 2번씩 듀얼로 굽던 빅데이터 [[123_pipe|파이프]]라인. 스톰이 이 아키텍처의 오른쪽 엔진([[092_GPT_NLP|Speed Layer]])으로서 가장 화려하게 타올랐던 무대다. |
| **[[401_bayesian_network_dag_causality|DAG]] ([[255_apache_airflow_dag|Directed Acyclic Graph]])** | 물이 위에서 아래로 흐를 뿐 거꾸로 거슬러 올라가 빙빙 돌지(Cycle) 않게 [[123_pipe|파이프]]를 짜는 수학적 방향 [[070_graph_datastructure|그래프]]로, 스톰의 Spout ➔ Bolt 연결 뼈대(Topology)가 바로 이 100% [[401_bayesian_network_dag_causality|DAG]] 구조다. |
| **Back-pressure (백프레셔 / 배압)** | Spout가 너무 미친 듯이 물을 뿜어서 뒤쪽 Bolt가 소화를 못 하고 터지기 직전일 때, 뒤에서 "야 좀 천천히 뿜어!"라고 역으로 압력 [[130_signal|신호]]를 보내 스로틀링(속도 조절)을 거는 [[136_variance|분산]] 시스템의 필수 방어막이다. |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[:---]
    │
    ▼
[Apache Kafka (아파치 카프카)]
    │
    ▼
[Apache Flink (아파치 플링크)]
    │
    ▼
[람다 아키텍처 (Lambda Architecture)]
    │
    ▼
[DAG (Directed Acyclic Graph)]
    │
    ▼
[Back-pressure (백프레셔 / 배압)]
```

이 흐름도는 :---에서 출발해 Back-pressure (백프레셔 / 배압)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

## 👶 어린이를 위한 3줄 비유 설명
1. 엣날에는 산더미처럼 쌓인 밀린 숙제([[001_dikw_pyramid|데이터]])를 밤새도록 한꺼번에 푸는 굼벵이 선생님([[843_hadoop_rack_awareness_data_replication_topology|하둡]])밖에 없었어요.
2. [[044_apache_storm|아파치 스톰]](Storm)은 엄청 발이 빠른 '택배 릴레이 기사님들'이에요. 숙제([[001_dikw_pyramid|데이터]])가 딱 1장 들어오자마자 수도꼭지 기사(Spout)가 받아서 요리 기사(Bolt)에게 던지면 1초 만에 답이 딱 나와요.
3. 1초도 쉬지 않고 공중에 물건을 띄워놓고 서로 핑퐁 치며 정답을 만들어내기 때문에, 지금 이 순간 사람들이 트위터에서 무슨 얘기를 제일 많이 하는지 0.01초 만에 알아낼 수 있는 번개 같은 발명품이랍니다!
