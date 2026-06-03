+++
weight = 421
title = "421. 스트리밍 멀티프로세서 (SM)"
date = "2026-03-20"
[extra]
categories = "studynote-computer-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 스트리밍 멀티프로세서 (Streaming [[375_multiprocessor|Multiprocessor]], SM)는 [[418_gpu|GPU]] ([[418_gpu|Graphics Processing Unit]]) 안에서 워프 (Warp)를 실제로 실행하고, [[057_register|레지스터]]·[[118_shared_memory|공유 메모리]]·연산기를 함께 제공하는 **[[430_index_fast_full_scan|병렬]] 실행의 기본 공장 단위**다.
> 2. **가치**: SM은 단일 [[092_thread_lwp|스레드]]를 빠르게 끝내기보다, 대기 중인 워프를 즉시 교체해 메모리 [[015_지연_데이터_관점|지연]]을 가리면서 **[[139_throughput|처리량]] ([[139_throughput|Throughput]])** 을 극대화하도록 설계된다.
> 3. **판단 포인트**: [[418_gpu|GPU]] [[282_performance_tactics|성능]]은 코어 수만이 아니라, SM당 [[057_register|레지스터]] 용량·[[118_shared_memory|공유 메모리]] 사용량·워프 점유율·분기 발산이 어떻게 맞물리느냐에 의해 결정된다.

---

## Ⅰ. 개요 및 필요성

스트리밍 멀티프로세서 (Streaming [[375_multiprocessor|Multiprocessor]], SM)는 NVIDIA GPU에서 [[422_thread_block_and_warp|스레드 블록]] ([[422_thread_block_and_warp|Thread Block]])을 받아 실제 연산을 수행하는 하드웨어 실행 클러스터다. CPU (Central Processing Unit) 코어가 단일 작업의 [[015_지연_데이터_관점|지연]]시간을 줄이는 데 많은 제어 로직을 쓰는 반면, SM은 같은 종류의 연산을 대량으로 흘려보내는 데 면적을 집중한다. 즉, SM은 "똑똑한 소수"보다 "규격화된 다수"를 택한 구조다.

이 구조가 필요해진 이유는 그래픽스와 [[231_ai_turing_test|인공지능]] 연산이 같은 계산을 엄청난 [[001_dikw_pyramid|데이터]]에 반복하는 형태이기 때문이다. 픽셀 셰이딩, 행렬 곱셈, 벡터 연산처럼 [[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]]성이 큰 작업에서는 복잡한 [[231_branch_prediction|분기 예측]]기보다 많은 연산기와 빠른 [[092_thread_lwp|스레드]] 교체가 더 효율적이다. 만약 이런 실행 단위가 없다면 GPU는 수천 개 [[092_thread_lwp|스레드]]를 관리하면서도 실제 메모리 [[015_지연_데이터_관점|지연]]과 자원 경쟁 때문에 연산기를 놀리게 된다.

또한 SM은 GPU를 확장 가능한 구조로 만드는 [[016_replication_factor|복제]] 단위이기도 하다. 칩 설계자는 SM을 여러 개 반복 배치해 전체 연산 [[282_performance_tactics|성능]]을 키우고, 소프트웨어는 그 위에 블록과 워프를 매핑한다. 그래서 SM을 이해하는 것은 GPU를 단순한 "코어 많이 붙인 칩"이 아니라, **[[016_replication_factor|복제]] 가능한 [[139_throughput|처리량]] 엔진의 집합**으로 이해하는 출발점이다.

📢 섹션 요약 비유: SM은 대형 물류센터의 작업 구역과 같다. 구역 하나가 컨베이어벨트, 작업대, 인력을 모두 갖추고 있어야 택배 상자들이 끊기지 않고 흘러간다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SM 내부를 볼 때 핵심은 "무엇이 계산하고, 무엇이 기다림을 숨기며, 무엇이 [[001_dikw_pyramid|데이터]] 재사용을 돕는가"를 구분하는 것이다. 일반적으로 SM은 워프 [[079_kube_scheduler_pod_placement|스케줄러]], [[420_cuda|CUDA]] 코어 (Compute Unified Device [[319_architecture|Architecture]] Core), [[427_tensor_core|텐서 코어]] ([[427_tensor_core|Tensor Core]]), [[057_register|레지스터]] [[501_file_definition_logical_record|파일]] ([[175_register_addressing|Register]] [[501_file_definition_logical_record|File]]), [[118_shared_memory|공유 메모리]] ([[118_shared_memory|Shared Memory]]), 로드/스토어 유닛을 포함한다. 세대마다 구성 비율은 달라지지만, 설계 철학은 일관된다. **많은 워프를 올려두고, 준비된 워프를 골라, 연산기를 쉬지 않게 한다**는 점이다.

| 구성 요소 | 역할 | [[282_performance_tactics|성능]]에 미치는 영향 |
| :--- | :--- | :--- |
| 워프 [[079_kube_scheduler_pod_placement|스케줄러]] (Warp Scheduler) | 실행 가능한 워프를 선택해 명령 발행 | 메모리 [[015_지연_데이터_관점|지연]] 은닉, 발행 효율 결정 |
| [[420_cuda|CUDA]] 코어 | 정수·[[087_floating_point|부동소수점]] 기본 연산 수행 | 범용 [[430_index_fast_full_scan|병렬]] 연산 [[139_throughput|처리량]] 결정 |
| [[427_tensor_core|텐서 코어]] | 행렬 곱셈 누산 (Matrix [[428_mac_operation|Multiply-Accumulate]]) 가속 | [[190_ai_llm_requirements_specification|AI]] 학습·추론 [[139_throughput|처리량]] 급증 |
| [[057_register|레지스터]] [[501_file_definition_logical_record|파일]] | [[092_thread_lwp|스레드]]별 상태와 중간값 저장 | 점유율 (Occupancy), 문맥 교체 비용에 영향 |
| [[118_shared_memory|공유 메모리]] / L1 캐시 | 블록 내부 [[001_dikw_pyramid|데이터]] 재사용, 저지연 협업 | 메모리 병목 감소, 타일링 최적화 핵심 |
| 로드/스토어 유닛 | 전역 메모리 접근 처리 | 코얼레싱 여부에 따라 [[140_bandwidth|대역폭]] 차이 발생 |

아래 그림은 하나의 [[422_thread_block_and_warp|스레드 블록]]이 SM에 올라와 워프로 쪼개지고, 메모리 [[015_지연_데이터_관점|지연]]이 생기면 다른 워프로 교체되는 흐름을 보여준다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                SM 내부 실행 흐름: "멈춘 워프 대신 다른 워프"       │
├─────────────────────────────────────────────────────────────────────┤
│ Thread Block 배치                                                  │
│      │                                                             │
│      ▼                                                             │
│ Warp 0   Warp 1   Warp 2   Warp 3  ...                             │
│   │        │        │        │                                     │
│   └────────┴────┬───┴────────┘                                     │
│                 ▼                                                   │
│        Warp Scheduler / Issue Logic                                │
│          ├─ Ready Warp ───────────────▶ CUDA Core / Tensor Core    │
│          └─ Waiting Warp (DRAM) ──────▶ 보류                        │
│                                    ▲                                │
│                                    │                                │
│                 Shared Memory / Register File                       │
└─────────────────────────────────────────────────────────────────────┘
```

이 구조의 핵심은 CPU식 문맥 교체를 하지 않는다는 점이다. 워프의 상태는 이미 SM 내부 [[057_register|레지스터]]에 머물러 있으므로, 어떤 워프가 전역 메모리인 [[251_dram|DRAM]] (Dynamic Random Access Memory)을 기다리면 [[079_kube_scheduler_pod_placement|스케줄러]]는 다른 워프로 넘어가면 된다. 이때 필요한 조건이 바로 충분한 점유율이다. [[057_register|레지스터]]를 너무 많이 쓰거나 [[118_shared_memory|공유 메모리]]를 과도하게 예약하면 SM에 동시에 올릴 수 있는 워프 수가 줄어들고, 결국 [[015_지연_데이터_관점|지연]]을 숨길 대기열이 얇아진다.

즉 SM [[282_performance_tactics|성능]]은 단순히 "코어 몇 개냐"보다 "준비된 워프를 얼마나 많이 유지하느냐"에 달려 있다. 그래서 [[418_gpu|GPU]] 최적화는 종종 계산식 자체보다 자원 배치 문제에 가깝다. 블록 크기, [[092_thread_lwp|스레드]]당 [[057_register|레지스터]] 수, [[118_shared_memory|공유 메모리]] 타일 크기가 모두 SM 내부 수용 능력과 직접 연결된다.

📢 섹션 요약 비유: SM은 손님이 줄 서 있는 식당 주방과 같다. 한 요리가 오븐에서 기다리는 동안, 요리사는 바로 다음 주문을 잡아 조리해 불을 꺼뜨리지 않는다.

---

## Ⅲ. 비교 및 연결

SM의 성격을 선명하게 보려면 CPU 코어와 비교하는 것이 가장 빠르다. CPU 코어는 낮은 [[015_지연_데이터_관점|지연]]시간, 높은 [[570_stp_vs_mtp|단일 스레드 성능]], 복잡한 제어 흐름 처리에 강하다. 반면 SM은 많은 [[092_thread_lwp|스레드]]가 대체로 같은 명령 흐름을 따를 때 강하며, 복잡한 분기보다 대량의 반복 연산에서 진가를 발휘한다. 같은 "코어"라는 말을 써도 설계 목표가 다르다.

| 항목 | CPU 코어 | SM |
| :--- | :--- | :--- |
| 우선 목표 | [[015_지연_데이터_관점|지연]]시간 최소화 | [[139_throughput|처리량]] 최대화 |
| 제어 구조 | [[231_branch_prediction|분기 예측]], Out-of-Order 실행 중심 | 단순 제어 + 대량 워프 관리 |
| [[092_thread_lwp|스레드]] 처리 | 적은 수의 강한 [[092_thread_lwp|스레드]] | 많은 수의 가벼운 [[092_thread_lwp|스레드]] |
| [[015_지연_데이터_관점|지연]] 대응 | 캐시 계층·투기 실행 | 워프 교체·점유율 확보 |
| 취약점 | 코어 수 확장 비용 큼 | 분기 발산·비정형 접근에 약함 |

또한 SM은 [[423_simt|SIMT]] (Single [[158_instruction|Instruction]] Multiple Threads) 실행 모델의 실제 무대다. 워프 내부 [[092_thread_lwp|스레드]]는 같은 명령 흐름을 공유하므로, `if-else` 분기가 갈라지면 워프 분기 발산 (Warp Divergence)이 생겨 유휴 연산기가 늘어난다. 이는 422번의 [[422_thread_block_and_warp|스레드 블록]]/워프, 423번의 SIMT와 직접 이어지고, 427번의 [[427_tensor_core|텐서 코어]]와는 "SM 안에 특화 연산기를 추가해 특정 연산의 밀도를 더 끌어올린다"는 방향으로 연결된다.

나아가 SM은 범용 GPU와 전용 가속기 사이의 경계도 보여준다. [[424_npu|NPU]] ([[424_npu|Neural Processing Unit]])나 [[425_tpu|TPU]] ([[425_tpu|Tensor Processing Unit]])는 특정 연산 패턴에 맞춰 [[001_dikw_pyramid|데이터]] 흐름을 더 강하게 고정함으로써 효율을 높인다. 반대로 SM은 여전히 범용성을 유지해 그래픽스, 과학 계산, 딥러닝, [[001_dikw_pyramid|데이터]] 분석을 폭넓게 처리한다. 즉 SM은 CPU보다 훨씬 [[430_index_fast_full_scan|병렬]] 친화적이면서도, 완전한 전용기보다는 덜 경직된 중간 지점에 있다.

📢 섹션 요약 비유: CPU 코어가 다재다능한 소수 정예 셰프라면, SM은 동일 메뉴를 빠르게 찍어내는 대형 조리 라인이다. 메뉴가 자주 바뀌면 셰프가 유리하고, 같은 주문이 몰리면 조리 라인이 압도한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 SM을 이해한다는 것은 "GPU를 샀다"가 아니라 "SM 자원을 얼마나 효율적으로 채웠는가"를 묻는 일이다. 예를 들어 블록 크기를 32의 배수로 맞추지 않으면 워프가 부분적으로만 차서 연산기가 빈자리를 안고 실행된다. 반대로 블록을 무작정 크게 잡으면 [[118_shared_memory|공유 메모리]]와 [[057_register|레지스터]]를 과점해 동시에 상주할 수 있는 블록 수가 줄어든다. 결국 [[282_performance_tactics|성능]] 튜닝은 최대 점유율과 충분한 [[001_dikw_pyramid|데이터]] 재사용 사이의 균형 문제다.

### 실무 체크포인트

1. **점유율 [[396_validation|확인]]**: SM당 활성 워프 수가 너무 낮지 않은가?
2. **[[057_register|레지스터]] 압박 [[396_validation|확인]]**: [[092_thread_lwp|스레드]]당 [[057_register|레지스터]] 사용량이 지나쳐 상주 워프 수를 깎지 않는가?
3. **[[118_shared_memory|공유 메모리]] [[268_strategy_pattern|전략]] [[396_validation|확인]]**: 타일링으로 [[251_dram|DRAM]] 왕복을 줄였지만, 뱅크 충돌 (Bank Conflict)은 만들지 않았는가?
4. **분기 패턴 [[396_validation|확인]]**: 워프 내부 조건 분기가 커서 SIMD형 실행 효율을 해치지 않는가?
5. **메모리 코얼레싱 [[396_validation|확인]]**: 인접 [[092_thread_lwp|스레드]]가 인접 주소를 읽도록 [[001_dikw_pyramid|데이터]] 배치를 설계했는가?

### 채택이 유리한 경우

- 대규모 행렬 연산, 컨볼루션, 벡터화 가능한 수치 계산
- 동일 [[022_kernel_role|커널]]을 많은 [[001_dikw_pyramid|데이터]]에 반복 적용하는 [[228_batch_processing_hadoop_spark|배치 처리]]
- 타일링과 재사용을 통해 [[118_shared_memory|공유 메모리]] 이득을 얻을 수 있는 문제

### 회피가 필요한 경우

- 포인터 추적, 트리 순회, [[070_graph_datastructure|그래프]] 탐색처럼 분기와 불규칙 접근이 심한 문제
- [[001_dikw_pyramid|데이터]] 크기가 작아 [[022_kernel_role|커널]] 실행 및 전송 오버헤드가 더 큰 문제
- 실시간 제어처럼 최악 [[015_지연_데이터_관점|지연]]시간 보장이 더 중요한 문제

기술사 답안 관점에서는 "SM 개수 증가 = 무조건 빠름"이라고 쓰면 부족하다. SM 수가 늘어도 메모리 [[140_bandwidth|대역폭]], 인터커넥트, L2 캐시, [[022_kernel_role|커널]] 구조가 받쳐주지 않으면 확장 효율은 떨어진다. 따라서 SM은 [[282_performance_tactics|성능]]의 원인이자 동시에 병목을 드러내는 측정 단위로 봐야 한다.

📢 섹션 요약 비유: SM 튜닝은 호텔 객실 수만 늘리는 일이 아니다. 객실 청소 인력, 엘리베이터, 수건 재고가 함께 맞아야 손님을 많이 받아도 운영이 무너지지 않는다.

---

## Ⅴ. 기대효과 및 결론

SM 아키텍처의 가장 큰 효과는 GPU를 대규모 [[430_index_fast_full_scan|병렬]] 처리에 맞는 모듈형 구조로 만들었다는 점이다. 동일한 실행 단위를 반복 배치함으로써 칩 설계는 확장성을 확보하고, 소프트웨어는 블록과 워프 추상화로 이를 활용할 수 있게 되었다. 그 결과 그래픽스뿐 아니라 고성능 컴퓨팅 ([[226_hpc_supercomputing_infrastructure|High Performance Computing]], [[548_automotive_hpc|HPC]])과 [[231_ai_turing_test|인공지능]] 학습까지 하나의 생태계 위에서 돌아가게 되었다.

다만 SM은 모든 문제의 만능 열쇠가 아니다. 분기 발산, 메모리 불규칙성, 낮은 점유율, 제한된 [[118_shared_memory|공유 메모리]] 용량은 언제든 효율을 무너뜨릴 수 있다. 그래서 최신 GPU는 독립 [[092_thread_lwp|스레드]] 스케줄링, 더 유연한 [[118_shared_memory|공유 메모리]] 구성, [[427_tensor_core|텐서 코어]] 통합, SM 간 협업 기능을 넣으며 한계를 완화해 왔다.

결국 SM은 "[[418_gpu|GPU]] 안의 코어 묶음"으로 외우기보다, **[[015_지연_데이터_관점|지연]]을 워프 교체로 숨기고 [[001_dikw_pyramid|데이터]] 재사용으로 끌어올리는 [[139_throughput|처리량]] 지향 실행 단위**로 기억해야 한다. 이 관점을 잡으면 [[418_gpu|GPU]] [[282_performance_tactics|성능]] 문제도 코어 수 경쟁이 아니라 자원 배치와 실행 패턴의 문제로 읽히기 시작한다.

📢 섹션 요약 비유: SM은 같은 설비를 여러 개 [[016_replication_factor|복제]]한 공장 라인이다. 라인이 많아도 자재 흐름과 작업 순서가 맞지 않으면 멈추지만, 균형이 맞으면 엄청난 생산량을 낸다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[422_thread_block_and_warp|스레드 블록]] ([[422_thread_block_and_warp|Thread Block]]) | 하나의 SM에 배치되는 소프트웨어 작업 단위 |
| 워프 (Warp) | SM이 실제로 스케줄링하는 최소 실행 묶음 |
| [[423_simt|SIMT]] (Single [[158_instruction|Instruction]] Multiple Threads) | SM이 대량 [[092_thread_lwp|스레드]]를 실행하는 기본 제어 모델 |
| [[118_shared_memory|공유 메모리]] ([[118_shared_memory|Shared Memory]]) | SM 내부에서 블록 구성원이 협업하는 저지연 저장소 |
| 점유율 (Occupancy) | SM 자원 사용량이 활성 워프 수로 이어지는 지표 |
| [[427_tensor_core|텐서 코어]] ([[427_tensor_core|Tensor Core]]) | 최신 SM 내부에 통합된 [[190_ai_llm_requirements_specification|AI]] 특화 연산기 |

### 📈 관련 키워드 및 발전 흐름도

```text
그래픽 셰이더용 병렬 실행
        │
        ▼
SM (Streaming Multiprocessor)
        │
        ├─ 워프 (Warp) · SIMT (Single Instruction Multiple Threads)
        │
        ├─ 공유 메모리 (Shared Memory) · 점유율 (Occupancy)
        │
        ▼
텐서 코어 (Tensor Core) 통합
        │
        ▼
AI·HPC 중심의 이기종 가속 아키텍처
```

이 흐름은 SM이 단순 그래픽 실행 단위를 넘어, 범용 [[430_index_fast_full_scan|병렬]] 처리와 [[231_ai_turing_test|인공지능]] 가속의 중심 단위로 확장된 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. SM은 큰 계산 공장 안에 있는 작은 작업반 한 팀이에요.
2. 어떤 친구가 재료를 가지러 잠깐 멈추면, 반장은 바로 다른 친구에게 일을 시켜서 기계를 쉬지 않게 해요.
3. 그래서 같은 계산을 아주 많이 해야 할 때 SM이 모여 있는 GPU가 엄청 빠르게 일할 수 있어요.
