---
title: 369. SISD (단일 명령어 단일 데이터)
date: '2026-03-20'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SISD (Single [[158_instruction|Instruction]] [[467_http2_stream_multiplexing_tcp_hol|stream]], Single [[001_dikw_pyramid|Data]] [[467_http2_stream_multiplexing_tcp_hol|stream]])는 한 시점에 하나의 [[158_instruction|명령어]] 흐름이 하나의 [[001_dikw_pyramid|데이터]] 흐름을 순차적으로 처리하는, 가장 기본적인 프로그램 실행 모델이다.
> 2. **가치**: 구조가 단순해 제어 흐름 예측, 디버깅, 실시간 응답 보장이 쉬우며, 오늘날에도 제어 중심 작업과 단일 [[092_thread_lwp|스레드]] [[282_performance_tactics|성능]]의 기준점이 된다.
> 3. **판단 포인트**: SISD는 [[139_throughput|처리량]] 확장에는 약하지만, [[001_dikw_pyramid|데이터]] 의존성이 강하고 순서 보장이 중요한 문제에서는 [[430_index_fast_full_scan|병렬]] 구조보다 더 안전하고 경제적인 선택이 될 수 있다.

---

## Ⅰ. 개요 및 필요성

SISD (Single [[158_instruction|Instruction]] [[467_http2_stream_multiplexing_tcp_hol|stream]], Single [[001_dikw_pyramid|Data]] [[467_http2_stream_multiplexing_tcp_hol|stream]])는 플린의 [[104_classification_analysis|분류]]법 (Flynn's Taxonomy)에서 가장 단순한 컴퓨터 구조로, 하나의 제어 흐름이 하나의 [[001_dikw_pyramid|데이터]] 항목을 차례대로 처리하는 방식이다. 저장 프로그램 방식의 [[459_quic_fec_forward_error_correction|초기]] 컴퓨터와 전통적인 단일 코어 실행 모델은 대부분 이 관점으로 이해할 수 있다. 즉, 프로세서는 "[[158_instruction|명령어]] 하나를 읽고, 필요한 [[001_dikw_pyramid|데이터]]를 가져오고, 연산하고, 결과를 저장한다"는 순서를 반복하며 동작한다.

이 구조가 오래 살아남은 이유는 빠르기보다 **이해 가능성**과 **예측 가능성**이 높기 때문이다. [[001_dikw_pyramid|데이터]] 간 의존성이 강한 계산, 분기문이 많은 제어 로직, 순서를 바꾸면 의미가 깨지는 [[191_transaction_concept_states|트랜잭션]] 처리에서는 여러 연산기를 억지로 동시에 돌리는 것보다 순차 실행 모델이 오히려 안정적이다. [[430_index_fast_full_scan|병렬]] 처리가 강력한 시대에도 SISD가 기준 모델로 남는 이유는, 다른 모든 [[430_index_fast_full_scan|병렬]] 구조가 결국 "무엇을 순서대로 남겨야 하는가"를 SISD와 비교해 설명되기 때문이다.

아래 그림은 SISD가 본질적으로 **한 줄짜리 실행 흐름**이라는 점을 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│              SISD의 기본 실행 흐름: 한 번에 한 단계씩        │
├──────────────────────────────────────────────────────────────┤
│ Program Counter ─▶ Fetch ─▶ Decode ─▶ Execute ─▶ Write Back │
│                         │                    │               │
│                         └───── 명령어 1개 ───┘               │
│                                              │               │
│ Data Memory/Register ───────── 데이터 1개 ───┘               │
└──────────────────────────────────────────────────────────────┘
```

핵심은 연산 장치가 아예 하나뿐이라는 뜻이 아니라, **[[369_logic_bomb|논리]]적으로 한 [[158_instruction|명령어]] 흐름이 한 [[001_dikw_pyramid|데이터]] 흐름을 책임진다**는 점이다. 그래서 SISD는 [[430_index_fast_full_scan|병렬]] 처리의 반대말이라기보다, [[430_index_fast_full_scan|병렬]] 처리의 필요성과 한계를 판단하는 출발점이다.

- **📢 섹션 요약 비유**: SISD는 계산대 직원 한 명이 손님을 번호표 순서대로 받는 방식과 같다. 한 번에 한 사람만 처리하니 줄은 길어질 수 있지만, 누가 먼저 왔고 어떤 주문을 받았는지 헷갈릴 일은 거의 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SISD를 구성하는 핵심 요소는 [[164_pc|프로그램 카운터]] (Program [[059_counter|Counter]]), 제어 장치 ([[206_control_unit|Control Unit]]), 산술논리장치 ([[117_alu|ALU]], [[117_alu|Arithmetic Logic Unit]]), [[057_register|레지스터]] ([[175_register_addressing|Register]]), 주기억장치 (Main Memory)다. [[164_pc|프로그램 카운터]]가 다음 [[158_instruction|명령어]] 주소를 가리키고, 제어 장치가 이를 해독해 연산 종류를 정하며, ALU가 실제 계산을 수행한다. 이때 한 사이클 또는 한 명령 단위에서 핵심 관심사는 "다음에 무엇을 실행할지" 하나뿐이므로 제어가 단순하고 검증이 쉽다.

| 구성 요소 | 역할 | SISD에서 중요한 이유 |
| :--- | :--- | :--- |
| [[164_pc|프로그램 카운터]] | 다음 [[158_instruction|명령어]] 위치 지정 | 순차 실행의 기준점 제공 |
| 제어 장치 | [[158_instruction|명령어]] 해독 및 제어 [[130_signal|신호]] [[087_process_state_transition|생성]] | 실행 흐름이 단일하므로 제어 충돌이 적음 |
| [[117_alu|ALU]] | 산술·[[369_logic_bomb|논리]] 연산 수행 | [[158_instruction|명령어]] 단위 결과가 명확하게 귀결됨 |
| [[057_register|레지스터]] | 중간 값 저장 | 직전 결과를 다음 단계에 안정적으로 전달 |
| 주기억장치 | [[158_instruction|명령어]]·[[001_dikw_pyramid|데이터]] 저장 | 메모리 지연이 전체 [[282_performance_tactics|성능]]을 직접 지배 |

이 그림은 SISD에서 [[282_performance_tactics|성능]] 병목이 어디서 생기는지 압축해 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│                 SISD의 병목: 순서는 단순하지만 대기는 길다   │
├──────────────────────────────────────────────────────────────┤
│ [Instruction Cache] ─▶ [Decode] ─▶ [ALU] ─▶ [Register]       │
│        │                                 │                   │
│        └─ 명령어 미스 발생 시 대기       └─ 결과 의존성 대기  │
│                                                              │
│ [Data Cache / Memory] ───────────────▶ [Load / Store]        │
│        └─ 메모리 지연 발생 시 전체 흐름 정체                 │
└──────────────────────────────────────────────────────────────┘
```

SISD의 약점은 [[139_throughput|처리량]]이 [[158_instruction|명령어]] 한 줄의 흐름에 묶인다는 점이다. [[158_instruction|명령어]] 사이에 [[001_dikw_pyramid|데이터]] 의존성이 생기거나 메모리 접근이 느려지면 뒤따르는 작업이 함께 멈춘다. 그래서 현대 중앙처리장치 (CPU, Central Processing Unit)는 파이프라이닝 (Pipelining), 슈퍼스칼라 ([[236_superscalar|Superscalar]]), [[238_out_of_order_execution|비순차 실행]] (Out-of-Order Execution) 같은 기법으로 내부 [[430_index_fast_full_scan|병렬]]성을 끌어오지만, 프로그래머에게는 여전히 **순차 프로그램처럼 보이도록** 설계한다. 즉 현대 CPU는 "외부적으로는 SISD 친화적 인터페이스"를 유지하면서 내부에서만 [[158_instruction|명령어]] 수준 [[430_index_fast_full_scan|병렬]]성 (ILP, [[158_instruction|Instruction]] Level Parallelism)을 숨겨 활용하는 셈이다.

- **📢 섹션 요약 비유**: SISD는 한 명의 요리사가 주문서를 순서대로 처리하는 주방과 같다. 요리사는 손놀림을 더 빨리 하거나 도마를 두 개 쓸 수는 있지만, 손님 입장에서는 여전히 자기 주문이 차례대로 나오는 것이 중요하다.

---

## Ⅲ. 비교 및 연결

SISD를 제대로 이해하려면 [[370_simd|SIMD]] (Single [[158_instruction|Instruction]] [[467_http2_stream_multiplexing_tcp_hol|stream]], Multiple [[001_dikw_pyramid|Data]] [[467_http2_stream_multiplexing_tcp_hol|stream]]), [[371_misd|MISD]] (Multiple [[158_instruction|Instruction]] [[467_http2_stream_multiplexing_tcp_hol|stream]], Single [[001_dikw_pyramid|Data]] [[467_http2_stream_multiplexing_tcp_hol|stream]]), [[372_mimd|MIMD]] (Multiple [[158_instruction|Instruction]] [[467_http2_stream_multiplexing_tcp_hol|stream]], Multiple [[001_dikw_pyramid|Data]] [[467_http2_stream_multiplexing_tcp_hol|stream]])와의 경계를 봐야 한다. SISD는 제어 흐름도 하나, [[001_dikw_pyramid|데이터]] 흐름도 하나이므로 **순서 보장**과 **단순 제어**에 강하다. 반면 SIMD는 같은 연산을 여러 [[001_dikw_pyramid|데이터]]에 동시에 적용해 [[139_throughput|처리량]]을 키우고, MIMD는 여러 코어가 서로 다른 [[158_instruction|명령어]]와 [[001_dikw_pyramid|데이터]]를 [[430_index_fast_full_scan|병렬]] 처리해 범용성을 확장한다.

| 비교 축 | SISD | [[370_simd|SIMD]] | [[372_mimd|MIMD]] |
| :--- | :--- | :--- | :--- |
| [[158_instruction|명령어]] 흐름 | 1개 | 1개 | 여러 개 |
| [[001_dikw_pyramid|데이터]] 흐름 | 1개 | 여러 개 | 여러 개 |
| 강한 영역 | 분기 많은 제어 로직, 순차 의존 계산 | [[055_array|배열]]·벡터·행렬 연산 | 서버 처리, [[675_multitasking_terminology_preemptive|멀티태스킹]], [[136_variance|분산]] 처리 |
| 약한 영역 | [[139_throughput|처리량]] 확장 | 분기 발산 | [[212_synchronization_mechanisms|동기화]]·[[194_consistency_database_integrity|일관성]] 비용 |
| 대표 관점 | 단일 [[092_thread_lwp|스레드]] 기준 모델 | [[001_dikw_pyramid|데이터]] [[430_index_fast_full_scan|병렬]] 가속 | 작업 [[430_index_fast_full_scan|병렬]] 확장 |

여기서 중요한 연결 고리는 암달의 법칙 (Amdahl's Law)이다. 전체 프로그램 중 순차 구간이 [[489_raid_10_hybrid|10]]%만 남아 있어도, [[430_index_fast_full_scan|병렬]]화로 얻을 수 있는 최대 [[282_performance_tactics|성능]] 향상은 결국 그 [[489_raid_10_hybrid|10]]%에 묶인다. 즉 SISD는 낡은 구조가 아니라, [[430_index_fast_full_scan|병렬]] 시스템 전체의 [[282_performance_tactics|성능]] 천장을 정하는 **기준 병목 구간**으로 계속 남아 있다. 또한 운영체제의 [[013_system_call|시스템 호출]], [[001_dikw_pyramid|데이터]]베이스의 직렬화 구간, 실시간 제어 루프는 여전히 SISD적 사고로 설계해야 예측 가능한 동작을 얻을 수 있다.

- **📢 섹션 요약 비유**: SISD는 한 권의 책을 처음부터 끝까지 읽는 방식이고, SIMD는 같은 페이지를 여러 권에서 동시에 읽는 방식이며, MIMD는 여러 사람이 각자 다른 책을 읽는 방식이다. 어떤 방식이 좋은지는 책의 종류가 아니라 읽어야 할 일의 성격이 결정한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 SISD를 선택해야 하는 대표 상황은 **상태 의존성이 강한 로직**이다. 예를 들어 계좌 잔액 갱신, 재고 차감, [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 기반 [[632_state_transition_diagram_testing|상태 전이]], 하드 실시간 제어 루프는 앞선 결과가 다음 계산의 입력이 된다. 이런 구간은 [[430_index_fast_full_scan|병렬]]화 자체보다 순서 보장과 재현 가능성이 훨씬 중요하므로, 단일 [[092_thread_lwp|스레드]] 또는 강한 직렬화 큐 기반 SISD형 처리 모델이 더 적합하다.

반대로 대규모 이미지 필터, 행렬 곱셈, [[568_logs_distributed_logging_elk_fluentd|로그]] 배치 분석처럼 동일 연산을 독립 [[001_dikw_pyramid|데이터]] 묶음에 반복하는 작업은 SISD로 밀어붙이면 비효율이 커진다. 이 경우는 SIMD나 MIMD로 넘겨야 하며, SISD는 오히려 병목이 된다. 따라서 기술사 관점의 핵심은 "SISD가 단순해서 좋다"가 아니라, **의존성·지연시간·디버깅 비용을 함께 보고 어디까지 순차로 남길지 판단하는 것**이다.

### 실무 판단 [[435_checklist_based_testing|체크리스트]]

1. 앞선 계산 결과가 다음 계산의 입력으로 직접 연결되는가?
2. 실행 순서가 바뀌면 의미가 달라지거나 오류가 발생하는가?
3. [[139_throughput|처리량]]보다 응답 예측 가능성과 재현성이 더 중요한가?
4. [[430_index_fast_full_scan|병렬]]화 이득보다 락, [[212_synchronization_mechanisms|동기화]], [[402_cache_coherence|캐시 일관성]] 비용이 더 큰가?

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 순서 의존 로직을 무리하게 멀티스레드화하여 [[213_race_condition|경쟁 조건]] ([[213_race_condition|Race Condition]])만 늘리는 설계
- 단일 [[092_thread_lwp|스레드]] 병목을 분석하지 않고 코어 수만 늘리면 해결된다고 믿는 설계
- 벡터화 가능한 반복 계산을 끝까지 SISD 루프에 남겨 CPU 자원을 낭비하는 설계

- **📢 섹션 요약 비유**: SISD는 한 줄로 줄 선 등산객을 좁은 외줄다리 위로 보내는 방식과 같다. 다리를 넓히지 않은 채 여러 사람을 한꺼번에 올리면 빨라지기는커녕 다리만 흔들리고 사고 위험만 커진다.

---

## Ⅴ. 기대효과 및 결론

SISD의 가장 큰 효과는 **단순성에서 오는 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]**이다. 프로그램 흐름이 명확하므로 디버깅이 쉽고, 특정 입력에서 어떤 결과가 나오는지 추적하기 쉽다. 또한 [[402_cache_coherence|캐시 일관성]], [[092_thread_lwp|스레드]] [[212_synchronization_mechanisms|동기화]], [[119_message_passing|메시지 전달]] 같은 [[430_index_fast_full_scan|병렬]] 시스템의 부가 복잡도가 작아, 작은 시스템이나 제어 중심 시스템에서는 오히려 총비용이 낮다.

물론 SISD만으로는 현대 서비스의 대규모 [[139_throughput|처리량]] 요구를 감당할 수 없다. 그래서 현실의 시스템은 제어가 복잡한 핵심 경로는 SISD적으로 유지하고, 대량 반복 계산이나 독립 작업만 [[370_simd|SIMD]]·[[372_mimd|MIMD]]·가속기로 분리하는 하이브리드 구성을 택한다. 결국 SISD는 "옛날 방식"이 아니라, [[430_index_fast_full_scan|병렬]]화 시대에도 반드시 남겨야 할 **순차 실행의 계약**으로 기억하는 것이 정확하다.

- **📢 섹션 요약 비유**: 좋은 도시 교통도 모든 길을 고속도로로 만들지 않는다. 골목길은 천천히지만 안전하게 두고, 멀리 가는 차들만 큰 도로로 보내야 도시 전체가 잘 굴러간다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 플린의 [[104_classification_analysis|분류]]법 (Flynn's Taxonomy) | SISD를 [[370_simd|SIMD]]·[[371_misd|MISD]]·MIMD와 함께 해석하는 기본 [[104_classification_analysis|분류]] 체계 |
| 파이프라이닝 (Pipelining) | SISD 외형을 유지한 채 처리 단계를 겹쳐 [[282_performance_tactics|성능]]을 높이는 방법 |
| 슈퍼스칼라 ([[236_superscalar|Superscalar]]) | 단일 명령 흐름 내부에서 여러 연산 장치를 활용하는 현대 CPU 기법 |
| 암달의 법칙 (Amdahl's Law) | [[430_index_fast_full_scan|병렬]]화 이후에도 순차 구간인 SISD가 전체 속도 상한을 결정함 |
| [[009_real_time_system|실시간 시스템]] ([[009_real_time_system|Real-Time System]]) | 예측 가능성과 순서 보장이 중요해 SISD적 설계가 자주 선택됨 |
| 벡터화 (Vectorization) | SISD 루프 중 독립 반복 구간을 SIMD로 넘기는 최적화 방법 |

### 📈 관련 키워드 및 발전 흐름도

```text
저장 프로그램 방식의 순차 실행
    │
    ▼
SISD (Single Instruction stream, Single Data stream)
    │  단일 제어 흐름 기반
    ▼
파이프라이닝 (Pipelining) · 슈퍼스칼라 (Superscalar)
    │  SISD 외형 유지 + 내부 병렬화
    ▼
SIMD (Single Instruction stream, Multiple Data stream)
    │  데이터 병렬 구간 분리
    ▼
MIMD (Multiple Instruction stream, Multiple Data stream)
    │  작업 병렬 확장
    ▼
멀티코어 · 가속기 · 이종 병렬 컴퓨팅
```

이 흐름은 컴퓨터 구조가 SISD를 버리고 대체했다기보다, SISD를 기준축으로 두고 내부 [[430_index_fast_full_scan|병렬]]화와 외부 [[430_index_fast_full_scan|병렬]]화를 단계적으로 확장해 왔음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. SISD는 선생님이 한 번에 학생 한 명씩 불러서 숙제를 확인하는 방식이에요.
2. 느려 보일 수 있지만, 누가 무엇을 틀렸는지 바로 알 수 있어서 실수 찾기가 쉬워요.
3. 그래서 아주 복잡하게 순서를 지켜야 하는 일은 아직도 이렇게 차근차근 하는 게 더 안전하답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 370 / 803

← **이전**: [[368_flynns_taxonomy|368. 플린의 분류법 (Flynn's Taxonomy)]]
**다음**: [[370_simd|370. SIMD (단일 명령어 다중 데이터)]] →

---
