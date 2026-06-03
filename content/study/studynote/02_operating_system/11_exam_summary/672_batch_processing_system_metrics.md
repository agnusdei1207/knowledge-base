---
title: 672. 일괄 처리 시스템 (Batch Processing System) 성능 지표
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 일괄 처리 시스템([[228_batch_processing_hadoop_spark|Batch Processing]] System)은 사용자와의 상호작용(Interaction) 없이, 비슷한 성격의 작업들을 한데 모아두었다가 컴퓨터가 한가할 때 순차적으로 한 번에 처리하는 가장 고전적이자 대용량 [[001_dikw_pyramid|데이터]] 처리에 특화된 [[001_operating_system_purpose|운영체제]] 방식이다.
> 2. **[[282_performance_tactics|성능]] 지표**: 일괄 처리 시스템의 가장 핵심적인 [[282_performance_tactics|성능]] 지표는 단위 시간당 완료된 작업의 수를 의미하는 **[[139_throughput|처리량]]([[139_throughput|Throughput]])**과, 작업이 제출된 시점부터 완료될 때까지 걸린 총시간인 **[[172_turnaround_waiting_response_time|반환 시간]]([[172_turnaround_waiting_response_time|Turnaround Time]])**이다. [[138_response_time|응답 시간]]([[138_response_time|Response Time]])은 전혀 중요하지 않다.
> 3. **가치**: 1960년대 천공 카드 시절에 탄생했지만, 현재에도 은행의 야간 결제 정산, 통신사 요금 청구, 대규모 [[241_machine_learning_basics|머신러닝]] [[001_dikw_pyramid|데이터]] 전처리([[395_hadoop_mapreduce_disk_bottleneck|Hadoop MapReduce]]) 등 '실시간성'보다는 '대규모 [[001_dikw_pyramid|데이터]]의 완벽한 처리'가 필요한 모든 엔터프라이즈 백엔드의 근간을 이룬다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **일괄 처리 ([[228_batch_processing_hadoop_spark|Batch Processing]])**: 여러 개의 작업(Job)이나 [[001_dikw_pyramid|데이터]]를 모아두었다가, 일정량(Batch)이 되거나 정해진 시간(주로 야간)이 되면 시스템이 개입 없이 자동으로 순차 처리하는 방식.
  - **Job (작업)**: 프로그램, [[001_dikw_pyramid|데이터]], 그리고 제어 정보(JCL: Job Control Language)가 하나로 묶인 일괄 처리의 기본 단위.

- **필요성 (CPU의 유휴 시간 최소화)**: 
  - 1950년대 컴퓨터(메인프레임)는 엄청나게 비쌌다. 사람이 컴퓨터에 펀치 카드를 넣고 결과를 기다린 뒤, 다음 카드를 넣는 방식은 사람이 움직이는 시간 동안 비싼 CPU가 놀게 되는 치명적 낭비를 불렀다.
  - **해결책**: "사람이 하는 일을 모아서 테이프나 디스크에 한 번에 기록해 두자! 그리고 컴퓨터([[229_monitor|모니터]] 프로그램)가 사람이 자는 동안 테이프를 읽어서 알아서 100개의 프로그램을 연속으로 돌리게 만들자!"라는 경제적 아이디어에서 일괄 처리 시스템이 탄생했다.

  - **대화형 시스템 ([[164_pc|PC]])**: 손님이 식당에 와서 햄버거 1개를 시키면 바로 만들어준다. 손님이 먹고 나서 감자튀김을 시키면 또 만들어준다 (주문마다 즉시 대응).
  - **일괄 처리 시스템 (Batch)**: 세탁소. 손님이 옷을 가져올 때마다 세탁기를 1벌씩 돌리지 않는다. 하루 종일 손님들의 옷을 바구니에 모아두었다가, 밤이 되면 세탁기 하나에 옷 수십 벌을 한꺼번에 넣고 돌린다 (효율성 극대화).

- **발전 과정**:
  1. **오프라인 [[457_spooling|스풀링]] ([[457_spooling|Spooling]])**: 펀치 카드(느림) $\rightarrow$ 마그네틱 테이프(빠름) $\rightarrow$ CPU. I/O와 연산을 분리.
  2. **JCL (Job Control Language)**: 여러 프로그램을 순서대로 실행시키기 위한 초창기 스크립트 언어.
  3. **현대적 배치 시스템**: [[843_hadoop_rack_awareness_data_replication_topology|Hadoop]], Spark 버치 처리, AWS Batch, Spring Batch 등 대규모 [[136_variance|분산]] [[001_dikw_pyramid|데이터]] 처리 프레임워크로 진화.

- **📢 섹션 요약 비유**: 우편물을 우체통에 한 달 동안 모아두었다가, 우체부 아저씨가 한 번에 수거해서 배달하는 시스템입니다. 당장 답장을 받을 순 없지만, 배달 비용과 시간은 가장 저렴합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 일괄 처리 시스템의 기본 아키텍처

사용자는 프로그램과 [[001_dikw_pyramid|데이터]]를 묶어(Job) OS에 제출하고, 결과를 다음 날 아침에 확인한다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 일괄 처리 시스템 (Batch System) 동작 흐름            │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [사용자 (Users)]                                                   │
  │   - User A: Job 1 제출 (월말 정산)                                    │
  │   - User B: Job 2 제출 (데이터 백업)                                   │
  │   - User C: Job 3 제출 (통계 리포트 생성)                               │
  │            │                                                      │
  │  ==========▼======================================================│
  │  [입력 스풀러 (Input Spooler)]                                       │
  │   - 하드디스크의 Job Queue에 작업들을 순서대로 쌓아둠.                    │
  │                                                                   │
  │     [ Job Queue ] : [ Job 1 ] -> [ Job 2 ] -> [ Job 3 ]           │
  │                                                                   │
  │  ==========▼======================================================│
  │  [운영체제 (Job Scheduler)]                                          │
  │   - CPU가 한가해지면 Job Queue에서 하나씩 꺼내어 메모리에 적재 후 실행.       │
  │                                                                   │
  │   [ CPU 실행 ] :                                                    │
  │   1. Job 1 실행 완료 (1시간 소요) -> 결과 출력                           │
  │   2. 즉시 Job 2 실행 시작 (상호작용 없음) -> 결과 출력                    │
  │   3. 즉시 Job 3 실행 시작 -> 결과 출력                                 │
  │                                                                   │
  │  ==========▼======================================================│
  │  [출력 스풀러 (Output Spooler) 및 프린터]                             │
  │   - 아침에 사용자가 출근하여 프린트된 결과물이나 파일을 확인.                 │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 스케줄러는 사용자의 개입(키보드 입력 등)을 전혀 기다리지 않는다. Job 1이 끝나면 단 1밀리초의 낭비 없이 곧바로 Job 2를 메모리로 끌고 와서 CPU를 태운다. 이 시스템의 목적은 사용자의 편의가 아니라, 수백억짜리 기계(CPU)를 1초도 쉬지 않게 풀가동(100% Utilization)시키는 데 있다.

---

### [[282_performance_tactics|성능]] 지표 1: [[139_throughput|처리량]] ([[139_throughput|Throughput]])

일괄 처리 시스템의 알파이자 오메가인 가장 중요한 지표다.

- **정의**: 단위 시간당 시스템이 처리하여 완료한 작업(Job)의 수. (예: 초당 처리 건수, 시간당 완료된 배치 수)
- **목표**: Throughput을 극대화(Maximize)하는 것.
- **측정 방식**: $[[139_throughput|Throughput]] = \frac{\text{완료된 총 작업 수}}{\text{총 소요 시간}}$
- **비유**: 식당 주방장이 1시간 동안 만들어 낸 햄버거의 총 개수. (손님이 얼마나 기다렸는지는 신경 안 씀. 오직 생산량만 중요)

---

### [[282_performance_tactics|성능]] 지표 2: [[172_turnaround_waiting_response_time|반환 시간]] ([[172_turnaround_waiting_response_time|Turnaround Time]])

사용자 관점에서 일괄 처리 시스템을 평가하는 지표다.

- **정의**: 특정 작업(Job)을 시스템에 **제출(Submit)한 시점부터 작업이 완료(Completion)되어 결과를 받을 때까지 걸린 총시간**.
- **구성**: $[[172_turnaround_waiting_response_time|Turnaround Time]] = \text{대기 시간 (Queue에서 대기)} + \text{실행 시간 (CPU 연산)} + \text{I/O 시간}$
- **목표**: Turnaround Time을 최소화(Minimize)하는 것. (또는 예측 가능하게 만드는 것)
- **비유**: 세탁소에 옷을 맡긴 날부터, 세탁이 다 되었다고 옷을 찾아간 날까지 걸린 총일수.

---

### [[282_performance_tactics|성능]] 지표 비교 (대화형 시스템 vs 일괄 처리 시스템)

왜 [[138_response_time|응답 시간]]([[138_response_time|Response Time]])은 일괄 처리에서 안 중요할까?

| [[282_performance_tactics|성능]] 지표 | 일괄 처리 시스템 (Batch) | 대화형(시분할) 시스템 (Interactive) | 설명 |
|:---|:---|:---|:---|
| **[[139_throughput|처리량]] ([[139_throughput|Throughput]])**| **가장 중요함 (1순위)** | 보통 (사용자 만족이 우선) | 1초에 몇 개의 [[001_dikw_pyramid|데이터]]를 쳐내는가? |
| **[[172_turnaround_waiting_response_time|반환 시간]] (Turnaround)**| 중요함 (2순위) | 중요함 | 작업을 던지고 결과가 나올 때까지의 시간 |
| **[[138_response_time|응답 시간]] ([[138_response_time|Response Time]])**| **전혀 고려 안 함** | **가장 중요함 (1순위)** | 키보드를 쳤을 때 화면에 글자가 뜨기까지의 시간 |
| **CPU 활용률 (Utilization)**| 항상 100%에 가깝게 유지 | 변동 큼 (사용자 생각할 때 쉼) | 시스템 자원의 경제성 지표 |

- **📢 섹션 요약 비유**: 넷플릭스 영화 재생(대화형)은 재생 버튼을 눌렀을 때 1초 만에 화면이 뜨는 것([[138_response_time|응답 시간]])이 생명입니다. 하지만 10년 치 영화 [[001_dikw_pyramid|데이터]]를 백업하는 작업(일괄 처리)은 당장 1초 뒤에 시작하든 1시간 뒤에 시작하든 상관없고, 내일 아침까지 1만 편이 다 백업되는가([[139_throughput|처리량]])가 훨씬 중요합니다.

---

## Ⅲ. 비교 및 연결

### 일괄 처리와 [[673_multiprogramming_bottleneck_resource|다중 프로그래밍]]([[673_multiprogramming_bottleneck_resource|Multiprogramming]])의 결합

[[459_quic_fec_forward_error_correction|초기]] 일괄 처리 시스템은 한 번에 하나의 Job만 메모리에 올려서 실행했다(Uniprogramming). 
- **문제점**: Job 1이 하드디스크에서 [[001_dikw_pyramid|데이터]]를 읽어오는(I/O) 동안 CPU는 할 일이 없어서 그냥 쉬었다.
- **해결 (Multiprogrammed Batch)**: 메모리에 Job 1, 2, 3을 다 올려둔다. Job 1이 I/O를 하러 가면, OS가 즉시 Job 2에게 CPU를 준다. 이로 인해 CPU 활용률이 100%에 근접하게 되며, [[139_throughput|처리량]]([[139_throughput|Throughput]])이 기하급수적으로 폭발했다.

### 과목 융합 관점

- **소프트웨어공학 (SE)**: Spring Batch 구조를 보면 `Reader -> Processor -> Writer`의 파이프라인(Chunk 지향 처리)으로 이루어져 있다. 이는 메모리에 [[001_dikw_pyramid|데이터]]를 왕창 올려서 한 번에 DB에 밀어 넣음으로써(Batch Insert), 네트워크 I/O 횟수를 줄이고 시스템의 전체 **[[139_throughput|Throughput]]**을 극대화하는 전형적인 배치 철학의 소프트웨어적 구현이다.
- **[[052_cloud_computing_os|클라우드 컴퓨팅]] (Cloud)**: AWS Spot Instance나 AWS Batch 서비스는, 당장 결과를 볼 필요가 없는 대용량 렌더링이나 [[190_ai_llm_requirements_specification|AI]] 학습(Batch Job)을 클라우드의 잉여 컴퓨팅 자원이 남을 때 매우 싼 값에 밀어 넣어 처리하는 현대적 일괄 처리 비즈니스 모델이다.

- **📢 섹션 요약 비유**: 일괄 처리와 [[673_multiprogramming_bottleneck_resource|다중 프로그래밍]]의 만남은, 양손에 프라이팬을 들고 요리하는 것과 같습니다. 한쪽 팬에서 고기가 익는(I/O 대기) 동안 노는 것이 아니라, 다른 팬에 계란을 굽는(CPU 연산) 식으로 주방장의 쉬는 시간을 0으로 만드는 것입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — 은행의 야간 결제 대사(정산) 시스템 병목**: 매일 자정 12시에 1,000만 건의 카드 결제 [[001_dikw_pyramid|데이터]]를 정산하는 배치(Batch) 프로그램이 돈다. 그런데 [[001_dikw_pyramid|데이터]]가 늘어나 아침 6시까지 배치가 안 끝나서 출근 시간 은행 앱 서비스에 장애가 생김 ([[172_turnaround_waiting_response_time|Turnaround Time]] 초과).
   - **원인 분석**: 단일 스레드로 한 건씩 DB에서 읽어와 계산하고 다시 쓰는 낡은 Uniprogramming 방식이라 Throughput이 1,000 TPS에 불과했다.
   - **대응 (기술사적 가이드)**: 
     - 1) **Chunk Size 조절**: [[001_dikw_pyramid|데이터]]를 1건씩 처리하지 않고, [[489_raid_10_hybrid|10]],000건 단위의 묶음([[346_batch_size_generalization|Batch Size]])으로 메모리에 올려 한 번에 Insert 하도록 쿼리를 튜닝한다 (I/O 병목 제거).
     - 2) **[[430_index_fast_full_scan|병렬]] 처리 (Parallel [[179_table_partitioning_concept|Partitioning]])**: 1,000만 건의 [[001_dikw_pyramid|데이터]]를 10개의 [[514_partition_slice_volume|파티션]](100만 건씩)으로 쪼개고, 10개의 멀티스레드(또는 멀티 노드)가 동시에 배치를 돌리도록 아키텍처를 개편하여 Throughput을 [[489_raid_10_hybrid|10]],000 TPS로 10배 끌어올린다. (결과적으로 Turnaround Time이 6시간 $\rightarrow$ 30분으로 단축됨)

2. **시나리오 — [[001_dikw_pyramid|데이터]] 엔지니어링의 [[215_etl_vs_elt_pipeline|ETL]](Extract, Transform, Load) 파이프라인**: 수백 개의 앱에서 쏟아지는 [[568_logs_distributed_logging_elk_fluentd|로그]]를 [[001_dikw_pyramid|데이터]] 웨어하우스에 넣어야 한다. 실시간(Streaming)으로 넣으려니 DB가 과부하로 뻗어버렸다.
   - **아키텍처 적용 (Micro-Batching)**: 완전한 실시간(Real-time)을 포기하고 일괄 처리의 미덕을 가져온다. Kafka나 Spark Streaming을 이용해 5초 단위, 1분 단위로 [[568_logs_distributed_logging_elk_fluentd|로그]] [[001_dikw_pyramid|데이터]]를 모아두었다가 덩어리(Micro-batch)로 묶어서 DB에 밀어 넣는다. [[138_response_time|응답 시간]]([[138_response_time|Response Time]])은 5초 늦어지지만, 시스템의 전체 [[001_dikw_pyramid|데이터]] [[139_throughput|처리량]]([[139_throughput|Throughput]])은 마비 없이 안정적으로 유지된다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 대용량 데이터 시스템 (Batch vs Real-time) 설계 플로우        │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [수백만 건의 데이터를 처리해야 하는 비즈니스 로직 개발]                     │
  │                │                                                  │
  │                ▼                                                  │
  │      사용자가 화면(UI)에서 요청 버튼을 누르고 그 자리에서 결과를 기다리는가?  │
  │          ├─ 예 (송금, 결제, 검색) ──▶ [대화형(Online) 시스템 아키텍처]     │
  │          │                        - 지표: Response Time(응답 시간) 최우선│
  │          │                        - 동기식 API 통신 및 빠른 인덱싱 DB 사용  │
  │          └─ 아니오 (통계, 정산, 마이그레이션, 메일 대량 발송)               │
  │                │                                                  │
  │                ▼                                                  │
  │      데이터의 양이 수 기가바이트 이상이며, 몇 시간 뒤에 끝나도 괜찮은가?      │
  │          ├─ 예 ─────▶ [일괄 처리(Batch Processing) 시스템 도입]      │
  │          │            - 지표: Throughput 극대화, Turnaround Time 준수  │
  │          │            - 스케줄러(Quartz, Airflow, Cron) 기반 심야 구동  │
  │          │                                                        │
  │          └─ 아니오 ──▶ 메시지 큐(RabbitMQ/Kafka) 기반 비동기 스트리밍 처리│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "배치가 느리다"고 불평하는 것은 배치의 목적을 이해하지 못한 것이다. 배치는 빠르려고 고안된 것이 아니라 "무거운 것을 무너지지 않고 확실하게 옮기려고" 고안된 것이다. 기술사는 비즈니스 오너에게 "이 작업은 실시간으로 하면 시스템이 죽습니다. 익일 오전 2시 배치로 돌려서 [[139_throughput|처리량]]([[139_throughput|Throughput]])을 보장하는 구조로 가야 합니다"라고 설득할 수 있어야 한다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **[[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]])**: 배치 작업이 돌다가 정전으로 새벽 3시에 죽었다. 다시 켰을 때(재처리), 이미 처리된 [[001_dikw_pyramid|데이터]]가 중복으로 두 번 처리(돈이 2번 송금됨)되지 않고 안전하게 이어서 처리되도록 [[171_idempotency_iac_terraform|멱등성]] 설계가 되어 있는가?
- **자원 격리 (Resource [[195_isolation_concurrency_control|Isolation]])**: 야간에 배치가 돌 때 CPU와 디스크 I/O를 100% 점유하여, 24시간 도는 대국민 웹 서비스에 장애(Noisy Neighbor)를 유발하지 않도록 배치 전용 DB(Read Replica)나 [[561_container_based_deployment|컨테이너]] 자원 제한([[062_cgroups|cgroups]])을 걸어두었는가?

- **📢 섹션 요약 비유**: 덤프트럭(배치 시스템)으로 흙을 나를 때, 트럭이 시속 100km로 달리는지([[138_response_time|응답 시간]])는 안 중요합니다. 한 번에 10톤의 흙을 싣고([[139_throughput|Throughput]]), 하루 안에 흙 1,000톤을 다 옮길 수 있는지(Turnaround)가 핵심입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 대화형 시스템 억지 적용 | 일괄 처리(Batch) 시스템 적용 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 ([[139_throughput|Throughput]])**| 잦은 I/O 락으로 초당 100건 한계 | 메모리 모아 쓰기로 **초당 [[489_raid_10_hybrid|10]],000건 달성**| 대용량 [[001_dikw_pyramid|데이터]] 처리 속도 수십 배 향상 |
| **정량 (자원 활용도)**| 낮에만 바쁘고 밤에는 서버 휑함 | 심야 유휴 시간에 배치 작업 몰아넣기 | 24시간 CPU 활용률(Utilization) 90% 이상 유지 |
| **정성 (운영 안정성)**| 실시간 트래픽 폭주 시 서버 다운 | 큐에 쌓아두고 여유 될 때 순차 처리 | 트래픽 [[129_spike_agile_technical_investigation|스파이크]] 방어 및 시스템 안정성 극대화 |

### 미래 전망
- **스트리밍과 배치의 경계 붕괴 ([[216_lambda_kappa_architecture_batch_realtime|Lambda]] / [[235_kappa|Kappa]] 아키텍처)**: 과거에는 낮에는 실시간(Online), 밤에는 배치(Batch)로 완전히 분리되었다. 현대 빅데이터 생태계에서는 [[215_flink_native_stream_watermark_window_time|Apache Flink]] 나 Spark Streaming을 통해, [[001_dikw_pyramid|데이터]]가 흐르는 즉시(실시간) 아주 작은 배치(Micro-batch) 단위로 끝없이 쪼개어 처리하는 스트리밍-배치 통합 아키텍처가 표준이 되었다.
- **[[206_serverless_cold_start|서버리스]] 배치 ([[206_serverless_cold_start|Serverless]] Batch)**: 1달에 한 번 도는 정산 배치를 위해 서버를 1달 내내 켜두는 낭비를 막기 위해, AWS Batch나 K8s CronJob처럼 배치가 도는 그 1시간 동안만 [[561_container_based_deployment|컨테이너]] 수천 대를 띄워서 연산을 끝내고 자원을 반납하는 비용 최적화 클라우드 아키텍처가 발전하고 있다.

### 결론
일괄 처리([[228_batch_processing_hadoop_spark|Batch Processing]]) 시스템은 천공 카드 시절에 태어난 가장 낡은 [[001_operating_system_purpose|운영체제]] 개념이지만, 역설적으로 초거대 [[001_dikw_pyramid|데이터]]가 쏟아지는 현대 AI와 클라우드 시대에 가장 필수적인 아키텍처로 환생했다. "[[139_throughput|처리량]]([[139_throughput|Throughput]])과 [[172_turnaround_waiting_response_time|반환 시간]]([[172_turnaround_waiting_response_time|Turnaround Time]])"이라는 지표는 단순히 과거의 이론이 아니라, 오늘날 [[001_dikw_pyramid|데이터]] 파이프라인을 설계하는 [[001_dikw_pyramid|데이터]] 엔지니어들이 시스템의 병목을 진단하고 아키텍처의 성공을 측정하는 변하지 않는 나침반이다.

- **📢 섹션 요약 비유**: 빠름(응답 속도)을 쫓는 세상에서, 묵묵히 거대한 짐을 한 번에 쓸어 담아 다음 날 아침 완벽하게 정리해 놓는 일괄 처리는 IT 인프라의 가장 든든하고 우직한 청소부입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[670_fault_injection_chaos_testing_kernel|소프트웨어 오류 주입]] ([[670_fault_injection_chaos_testing_kernel|Fault Injection]]) 카오스 테스팅 시스템 [[022_kernel_role|커널]] [[192_module_independence|모듈]] 활용법 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 시스템 프로그램과 응용 프로그램의 차이 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[673_multiprogramming_bottleneck_resource|다중 프로그래밍]] ([[673_multiprogramming_bottleneck_resource|Multiprogramming]]) 한계 자원 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[003_time_sharing_system|시분할 시스템]] [[138_response_time|응답 시간]] 최적화 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[시스템 프로그램과 응용 프로그램의 차이]
    │
    ▼
[일괄 처리 시스템 (Batch Processing System) 성능 지표]
    │
    ├──▶ [다중 프로그래밍 (Multiprogramming) 한계 자원]
    └──▶ [시분할 시스템 응답 시간 최적화]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 식당에 손님이 와서 햄버거 1개를 시킬 때마다 바로바로 만들어 주는 것을 '대화형 시스템'이라고 해요. 속도는 빠르지만 주방장이 너무 바쁘죠.
2. '일괄 처리 시스템'은 학교 급식실이에요! 학생들이 배고프다고 소리쳐도 바로 주지 않아요. 점심시간이 될 때까지 기다렸다가, 거대한 솥에 카레 500인분을 한꺼번에 끓인답니다.
3. 내가 원할 때 바로 밥을 먹을 수 없어서 기다리는 시간([[172_turnaround_waiting_response_time|반환 시간]])은 길지만, 한 번에 500명을 먹일 수 있는 엄청난 요리량([[139_throughput|처리량]])을 자랑하는 최고의 시스템이에요!
