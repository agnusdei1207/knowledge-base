+++
title = "368. 플린의 분류법 (Flynn's Taxonomy)"
date = 2026-03-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법 (Flynn's Taxonomy)은 컴퓨터를 빠르기 자체가 아니라, <strong><a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a> 흐름 (<a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">Instruction</a> <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/">Stream</a>)</strong> 과 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 흐름 (<a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/">Stream</a>)</strong> 을 몇 갈래로 처리하느냐로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 구조의 기준표다.
> 2. **가치**: 이 기준을 알면 중앙처리장치 (CPU, Central Processing Unit), 그래픽처리장치 ([GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)), [벡터 프로세서](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/373_vector_processor/), [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 클러스터가 왜 서로 다른 방식으로 강한지 한 번에 연결된다.
> 3. **판단 포인트**: 같은 계산을 대량 반복하면 단일 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 다중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ([SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/), Single [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 유리하고, 작업마다 제어 흐름이 다르면 다중 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 다중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ([MIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/372_mimd/), Multiple [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 유리하다.

---

## Ⅰ. 개요 및 필요성

플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법 (Flynn's Taxonomy)은 컴퓨터 시스템을 <strong><a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a> 스트림 수</strong>와 <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 스트림 수</strong>라는 두 축으로 나누는 아키텍처 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 컴퓨터는 대체로 하나의 제어 흐름이 하나의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 순차 처리하는 구조였지만, 과학 계산·그래픽 처리·대규모 서버 운영이 늘어나면서 "무엇을 동시에 처리할 것인가"가 핵심 문제가 되었다. 이때 필요한 것은 단순한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 수치가 아니라, [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성이 <strong>어디에 존재하는지</strong>를 설명하는 공통 언어였다.

플린은 이 문제를 복잡한 회로 세부가 아니라 추상화된 두 흐름으로 정리했다. 덕분에 하드웨어 설계자는 [제어 유닛](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/206_control_unit/)을 몇 개 둘지 판단할 수 있고, 소프트웨어 설계자는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성인지 작업 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성인지 구분해 적절한 프로그래밍 모델을 선택할 수 있다. 이 기준이 없으면 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 같은 구조를 단순히 "코어가 많다"로 오해하게 되고, 실제로는 제어 방식이 완전히 다르다는 중요한 차이를 놓치게 된다.

플린 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)는 단일 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 단일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ([SISD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/369_sisd/), Single [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Single [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)), 단일 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 다중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ([SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/), Single [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)), 다중 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 단일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ([MISD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/371_misd/), Multiple [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Single [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)), 다중 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 다중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) ([MIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/372_mimd/), Multiple [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))로 정리된다.

아래 그림은 플린 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)의 핵심을 2×2 축으로 압축한 것이다.

```text
┌──────────────────────────────────────────────────────────────┐
│        플린의 분류법: 명령어 흐름 × 데이터 흐름 매트릭스     │
├───────────────────────┬──────────────────┬───────────────────┤
│                       │ 단일 데이터      │ 다중 데이터       │
│                       │ Single Data      │ Multiple Data     │
├───────────────────────┼──────────────────┼───────────────────┤
│ 단일 명령어           │ SISD             │ SIMD              │
│ Single Instruction    │ 한 명령 + 한 데이터 │ 한 명령 + 여러 데이터 │
├───────────────────────┼──────────────────┼───────────────────┤
│ 다중 명령어           │ MISD             │ MIMD              │
│ Multiple Instruction  │ 여러 명령 + 한 데이터 │ 여러 명령 + 여러 데이터 │
└───────────────────────┴──────────────────┴───────────────────┘
```

중요한 점은 이 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 순위를 매기는 표가 아니라는 것이다. 같은 문제를 어느 방식으로 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화하느냐에 따라 적합한 구조가 달라지므로, 플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법은 "어떤 구조가 더 우월한가"보다 "어떤 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성에 맞는가"를 판단하는 출발점이 된다.

- **📢 섹션 요약 비유**: 플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법은 주방을 보는 기준과 같다. 요리 지시를 한 셰프가 모두 내리는지, 여러 셰프가 각자 내리는지, 그리고 재료를 한 접시씩 다루는지 대량으로 다루는지를 보면 주방의 운영 방식이 바로 드러난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법에서 핵심은 제어 흐름과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름이 어떻게 결합되는지다. [제어 유닛](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/206_control_unit/) ([Control Unit](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/206_control_unit/))이 하나면 여러 연산 장치가 있더라도 같은 명령을 따라야 하고, [제어 유닛](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/206_control_unit/)이 여러 개면 각 처리 요소가 서로 다른 프로그램 카운터를 기반으로 독립 실행할 수 있다. 따라서 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성은 단순히 연산기 개수보다 <strong>제어의 공유 여부</strong>에서 결정된다.

| [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) | 제어 구조 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 방식 | 대표 사례 | 핵심 병목 |
| :--- | :--- | :--- | :--- | :--- |
| [SISD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/369_sisd/) (Single [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Single [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) | [제어 유닛](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/206_control_unit/) 1개 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 1개씩 순차 처리 | 전통적 단일 코어 실행 모델 | 명령 수준 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 한계 |
| [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) (Single [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) | [제어 유닛](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/206_control_unit/) 1개가 다수 연산기에 브로드캐스트 | 같은 연산을 여러 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 동시 적용 | 벡터 연산, [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 셰이더, 벡터 확장 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) | 분기 발산, 메모리 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) |
| [MISD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/371_misd/) (Multiple [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Single [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) | 여러 제어 흐름 | 하나의 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 중복 처리 | [결함 허용](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/296_fault_tolerance_architecture/) 시스템, 일부 파이프라인 해석 | 범용성 부족 |
| [MIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/372_mimd/) (Multiple [Instruction](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) Multiple [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)) | [제어 유닛](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/206_control_unit/) 다수 | 각자 다른 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 다른 명령 처리 | 멀티코어 CPU, 서버 클러스터 | [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/), [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) |

아래 그림은 왜 SIMD와 MIMD가 실제로 다르게 느껴지는지 보여준다. 둘 다 연산기는 여러 개일 수 있지만, 명령을 배포하는 방식이 다르다.

```text
┌──────────────────────────────────────────────────────────────┐
│              제어 공유 여부에 따른 실행 방식 차이            │
├──────────────────────────────┬───────────────────────────────┤
│ SIMD                         │ MIMD                          │
│ 하나의 제어가 동일 명령 전파 │ 각 처리기가 독립 제어 보유    │
├──────────────────────────────┼───────────────────────────────┤
│        [Control]             │ [P1] [P2] [P3] [P4]          │
│            │                 │  │    │    │    │            │
│     ┌──────┼──────┐          │ I1   I2   I3   I4            │
│     ▼      ▼      ▼          │ D1   D2   D3   D4            │
│   [처리기1][처리기2][처리기3]        │ 독립 명령·독립 데이터 처리   │
│    D1     D2     D3          │                               │
│ 같은 명령을 각 데이터에 적용 │ 작업별 분기와 비동기 실행 가능│
└──────────────────────────────┴───────────────────────────────┘
```

이 구조 차이는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 특성으로 바로 이어진다. 예를 들어 행렬 덧셈처럼 `A[i] + B[i]`를 대량 반복하는 문제는 SIMD가 매우 강하다. 반면 웹 서버처럼 요청마다 조건문, 입출력, [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 접근이 달라지는 문제는 제어 흐름이 제각각이므로 MIMD가 유리하다. MISD는 교과서에서는 중요하지만 범용 컴퓨터에서는 드물며, 동일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 방식으로 교차 검증하는 안전 시스템에서 주로 의미를 가진다.

- **📢 섹션 요약 비유**: SIMD는 방송국의 단체 체조 방송처럼 한 구령에 모두가 같은 동작을 하는 구조이고, MIMD는 여러 택시 기사가 각자 다른 승객을 태우고 다른 길로 가는 구조다.

---

## Ⅲ. 비교 및 연결

플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법을 제대로 이해하려면 네 가지를 독립 항목으로 외우기보다, <strong><a href="/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/369_sisd/">SISD</a>→<a href="/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/">SIMD</a>→<a href="/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/372_mimd/">MIMD</a></strong>로 확장되는 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성의 방향을 봐야 한다. SISD는 제어와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 모두 하나라서 가장 단순하지만, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 확장은 주로 파이프라이닝 (Pipelining)이나 슈퍼스칼라 ([Superscalar](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/236_superscalar/)) 같은 내부 최적화에 의존한다. SIMD는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 하나로 유지한 채 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 갈래로 넓혀 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 올리고, MIMD는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 흐름 자체를 분리해 범용성을 확보한다.

| 비교 축 | [SISD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/369_sisd/) | [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) | [MIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/372_mimd/) |
| :--- | :--- | :--- | :--- |
| [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성의 원천 | 거의 없음 또는 제한적 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 | 작업 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 + [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 |
| 잘 맞는 문제 | 순차 로직, 제어 중심 코드 | [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)·행렬·영상·[신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 처리 | 서버, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리 |
| 약한 지점 | [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 확장 한계 | 분기 많은 코드 | [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 비용 |
| 대표 소프트웨어 모델 | 단일 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) | 벡터화, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 실행 | 멀티스레드, 멀티프로세스, 메시지 패싱 |

현대 시스템은 이 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)를 혼합해서 사용한다. 예를 들어 멀티코어 CPU는 큰 틀에서 MIMD지만, 각 코어 내부에는 [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) 확장 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 들어 있다. [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 역시 외형적으로는 수천 개 연산기를 가진 [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) 계열로 설명할 수 있지만, 실제 프로그래밍 모델은 단일 프로그램 다중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (SPMD, Single Program Multiple [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))처럼 보이는 경우가 많다. 즉 플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법은 현실을 100% 세밀하게 묘사하는 지도라기보다, 복잡한 구조를 읽기 위한 첫 번째 좌표축이다.

[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)시스템 관점에서도 연결이 선명하다. MIMD는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 스케줄링, 락, [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/), 메시지 패싱 같은 주제를 자연스럽게 끌고 오고, SIMD는 메모리 정렬, 벡터 길이, 워프 분기 같은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 이슈를 만든다. 플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법은 결국 하드웨어 과목 안의 정의가 아니라, 소프트웨어 구조와 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝 방식까지 이어지는 공통 프레임이다.

- **📢 섹션 요약 비유**: SISD는 한 사람이 한 줄씩 책을 읽는 방식, SIMD는 여러 사람이 같은 페이지를 각자 다른 책에서 동시에 읽는 방식, MIMD는 독서실에서 모두가 각자 다른 책과 다른 진도를 갖는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법은 시험용 암기표보다 <strong>아키텍처 선택 기준</strong>으로 더 중요하다. 먼저 워크로드가 동일 연산 반복형인지, 아니면 요청마다 흐름이 달라지는지 구분해야 한다. 이 판단을 틀리면 비싼 하드웨어를 도입하고도 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 기대만큼 나오지 않는다.

예를 들어 딥러닝 학습, 영상 필터링, 과학 계산처럼 동일한 수학 연산을 대량 반복하는 업무는 [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) 계열 자원이 유리하다. 이 경우 핵심은 [부동소수점](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)뿐 아니라 메모리 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치 구조다. 반대로 온라인 거래 처리, [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/), [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 서버는 각 요청의 제어 흐름이 달라서 [MIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/372_mimd/) 계열 CPU와 충분한 캐시, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 스케줄링 정책이 더 중요하다.

### 실무 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 동일한 명령을 수천~수백만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 반복하는가?
2. 분기문과 예외 경로가 많아 처리 요소별 실행 경로가 자주 갈리는가?
3. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 공유가 많은가, 아니면 노드별 독립 처리가 가능한가?
4. 병목이 연산량인가, 메모리 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)인가, 통신 지연인가?

### 자주 나오는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- GPU가 코어 수가 많다는 이유만으로 분기 많은 업무를 [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) 자원에 억지로 올리는 경우
- 멀티코어면 무조건 빠르다고 보고 락 경합과 공유 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 무시하는 경우
- [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) 최적화를 하면서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정렬과 연속 메모리 접근을 고려하지 않는 경우

기술사 관점에서는 "[분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)를 말하라"보다 "왜 그 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)가 이 문제에 맞는가"까지 설명해야 답안이 완성된다. 즉 플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법은 정의 4개를 적는 문제라기보다, <strong>문제의 <a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a>성 유형을 진단하고 적합한 구조를 고르는 사고 틀</strong>로 써야 점수가 난다.

- **📢 섹션 요약 비유**: 같은 모양의 박스를 끝없이 나르는 창고라면 컨베이어벨트형 조직이 좋지만, 매번 다른 손님 요구를 받는 상담센터라면 각 직원이 자율적으로 대응하는 조직이 더 맞다.

---

## Ⅴ. 기대효과 및 결론

플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법을 기준으로 시스템을 바라보면 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 구조를 막연한 "고성능"이 아니라 <strong>제어 방식과 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 처리 방식의 조합</strong>으로 이해하게 된다. 그 결과 하드웨어 선정, [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 설계, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 분석에서 왜 특정 구조가 강한지 일관되게 설명할 수 있다. 특히 CPU와 GPU의 차이를 단순 클럭이나 코어 개수로 보지 않고, 제어 공유 여부와 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 종류로 해석할 수 있다는 점이 크다.

다만 현대 아키텍처는 하이브리드화가 심해져서 플린의 네 칸만으로 세부 구조를 모두 설명할 수는 없다. 벡터 길이 가변 구조, 이종 가속기, CPU+[GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)+[NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) ([Neural Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/)) 결합 시스템처럼 실제 제품은 여러 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)를 겹쳐 가진다. 따라서 플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법은 최종 설계도라기보다, 복잡한 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 시스템을 처음 읽을 때 사용하는 <strong>기본 좌표계</strong>로 기억하는 것이 가장 정확하다.

결론적으로 이 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법의 가치는 오래된 이론이라는 데 있지 않다. 오늘날에도 "이 문제는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성인가, 작업 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성인가"를 먼저 묻게 만들며, 바로 그 질문이 좋은 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 아키텍처 설계의 시작점이 된다.

- **📢 섹션 요약 비유**: 지도는 도시의 모든 골목을 다 보여주지 못해도, 어느 방향으로 가야 하는지는 정확히 잡아준다. 플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법도 현대 컴퓨터의 모든 세부를 담지는 못하지만, [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 구조를 읽는 방향 감각은 분명하게 준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 파이프라이닝 (Pipelining) | SISD의 한계를 내부 단계 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화로 보완하는 대표 기법 |
| [벡터 프로세서](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/373_vector_processor/) ([Vector Processor](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/373_vector_processor/)) | [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) 철학을 길게 늘인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 연산 장치 |
| [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)) | 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리에 강한 [SIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/370_simd/) 계열 대표 사례 |
| 멀티코어 CPU (Multi-Core CPU) | [MIMD](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/372_mimd/) 구조를 범용 시스템에 적용한 대표 형태 |
| 메시지 패싱 ([Message Passing](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)형 MIMD에서 노드 간 협업을 가능하게 하는 통신 방식 |
| [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) ([Cache Coherence](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)) | [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) MIMD에서 반드시 관리해야 하는 핵심 문제 |

### 📈 관련 키워드 및 발전 흐름도

```text
SISD (Single Instruction Single Data)
    │  순차 실행의 기본 모델
    ▼
파이프라이닝 (Pipelining) · 슈퍼스칼라 (Superscalar)
    │  단일 흐름 내부의 성능 확장
    ▼
SIMD (Single Instruction Multiple Data)
    │  데이터 병렬성 확대
    ▼
MIMD (Multiple Instruction Multiple Data)
    │  독립 제어 흐름 확장
    ▼
멀티코어 · 클러스터 · 이종 가속기 하이브리드
```

이 흐름은 "순차 처리 최적화 → [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 → 작업 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화 → 혼합형 시스템"으로 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 아키텍처가 확장되는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 플린의 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)법은 컴퓨터가 일을 시키는 선생님 수와, 일을 맡는 학생 수를 보고 팀을 나누는 방법이에요.
2. 모두가 같은 숙제를 한꺼번에 하면 SIMD이고, 각자 다른 숙제를 하면 MIMD예요.
3. 그래서 어떤 컴퓨터가 그림 그리기에 좋은지, 어떤 컴퓨터가 여러 일을 동시에 잘하는지 쉽게 알 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 369 / 803

← **이전**: [367. NoC (Network on Chip)](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/367_noc/)
**다음**: [369. SISD (단일 명령어 단일 데이터)](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/369_sisd/) →

---
