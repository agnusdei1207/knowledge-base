+++
title = "409. 거짓 공유 (False Sharing)"
date = 2026-03-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 거짓 공유 (False Sharing)는 서로 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로는 독립된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다뤄도, 물리적으로 같은 캐시 라인 (Cache Line)에 놓여 있으면 [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) ([Cache Coherence](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)) 하드웨어가 같은 공유 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 오인해 무효화 트래픽을 만드는 현상이다.
> 2. **가치**: 이 문제는 락 ([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 경합이 없어도 멀티코어 확장성을 무너뜨리므로, "코드를 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)화했는데 왜 더 느려졌는가"를 설명하는 대표적 병목 원인이다.
> 3. **판단 포인트**: 해결의 핵심은 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 자체보다 메모리 배치다. 핫 필드(hot field)를 분리하고, [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) ([Padding](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/))·정렬 (Alignment)·[스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)별 로컬 집계를 통해 캐시 라인 충돌을 구조적으로 끊어야 한다.

---

## Ⅰ. 개요 및 필요성

거짓 공유 (False Sharing)는 멀티코어 시스템에서 각 코어가 서로 다른 변수를 수정하는데도 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 급격히 나빠지는 현상이다. 원인은 코드의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 관계가 아니라 메모리의 물리 배치에 있다. 하드웨어는 개별 변수보다 캐시 라인 단위로 소유권과 무효화 상태를 관리하므로, 우연히 같은 라인에 붙어 있는 변수들은 서로 간섭하는 것처럼 보인다.

이 문제가 위험한 이유는 개발자가 코드만 봐서는 병목을 알아차리기 어렵기 때문이다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 레이스 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Race)도 없고, 락 경합도 없고, [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 복잡도도 그대로인데 처리량만 비정상적으로 떨어진다. 특히 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), 큐 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), 통계 수집용 구조체처럼 "작고 자주 갱신되는 값"이 나란히 배치되면 코어 수가 늘수록 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 하락이 더 커진다.

아래 그림은 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로는 독립된 두 변수가 왜 하드웨어 입장에서는 같은 자원으로 취급되는지를 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">거짓 공유의 출발점: 변수는 둘이지만 캐시 라인은 하나</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Cache Line 0 (예: 64B)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">counter_A</div><div class="kb-diagram-cell">counter_B</div><div class="kb-diagram-cell">other bytes</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Core 0 write Core 1 write</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">invalidate ping-pong</div></div>
</div>
</div>



핵심은 "공유 변수"가 아니라 "공유 캐시 라인"이 문제라는 점이다. 따라서 멀티코어 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 볼 때는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성뿐 아니라 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 메모리에서 어떤 단위로 붙어 있는지도 함께 설계해야 한다.

- **📢 섹션 요약 비유**: 서로 다른 두 사람이 각자 자기 서랍을 쓰는 줄 알았는데, 실제로는 하나의 큰 서랍을 칸만 나눠 쓰는 상황과 같다. 한 사람이 서랍을 열고 닫을 때마다 다른 사람도 같이 방해받는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

거짓 공유는 캐시 라인 단위 관리와 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 무효화 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 만나서 생긴다. 현대 CPU (Central Processing Unit)는 메모리에서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 가져올 때 보통 수십 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 크기의 캐시 라인 단위로 적재하고, MESI (Modified, Exclusive, Shared, Invalid) 같은 프로토콜로 해당 라인의 소유 상태를 추적한다. 따라서 4바이트 정수 하나만 바꿔도 그 정수가 포함된 캐시 라인 전체가 "수정된 라인"으로 간주된다.

| 요소 | 하드웨어가 보는 단위 | 거짓 공유에서 생기는 일 |
| :--- | :--- | :--- |
| 캐시 라인 (Cache Line) | 메모리 전송과 캐시 적재의 최소 묶음 | 독립 변수도 같은 라인에 있으면 함께 묶임 |
| [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) ([Cache Coherence](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)) | 코어 간 최신값 유지 규칙 | 한 코어의 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 다른 코어 라인을 무효화함 |
| [Write-Invalidate](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/405_write_invalidate/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 전 타 코어 사본 제거 | 실제 공유가 없어도 라인 소유권이 번갈아 이동 |
| 빈번한 갱신 패턴 | 짧은 간격의 반복 write | 캐시 핑퐁으로 지연과 인터커넥트 트래픽 급증 |

아래 그림은 동일한 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 구조가 메모리 배치에 따라 전혀 다른 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 낼 수 있음을 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">메모리 배치에 따른 차이</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">패딩 없음</div><div class="kb-diagram-cell">패딩 적용</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">A</div><div class="kb-diagram-node">B</div><div class="kb-diagram-node">.................</div><div class="kb-diagram-node">A</div><div class="kb-diagram-node">.................</div><div class="kb-diagram-node">B</div><div class="kb-diagram-node">.........</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 같은 Cache Line</div><div class="kb-diagram-cell">─ 서로 다른 Cache Line</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Core 0 write A</div><div class="kb-diagram-cell">Core 0 write A</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Core 1 write B</div><div class="kb-diagram-cell">Core 1 write B</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 라인 소유권 충돌</div><div class="kb-diagram-cell">─ 독립적으로 갱신</div></div>
</div>
</div>



예를 들어 다음 구조체는 보기에는 단순하지만, 멀티스레드 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)에서는 위험하다.

```cpp
struct Counters {
    std::atomic<int> a;
    std::atomic<int> b;
};
```

`a`와 `b`를 서로 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 계속 증가시키면 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로는 독립이지만 물리적으로는 같은 캐시 라인을 놓고 경쟁할 수 있다. 이를 줄이려면 아래처럼 정렬을 강제해 캐시 라인 경계를 분리한다.

```cpp
struct alignas(64) PaddedCounter {
    std::atomic<int> value;
};

struct Counters {
    PaddedCounter a;
    PaddedCounter b;
};
```

단, [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)은 만능이 아니다. 캐시 라인 크기는 아키텍처에 따라 다를 수 있고, 과도한 [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)은 캐시 점유량을 늘려 다른 지역성(Locality)을 해칠 수 있다. 그래서 거짓 공유는 "메모리를 얼마나 아낄까"가 아니라 "핫 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)끼리 얼마나 멀리 둘까"의 문제로 봐야 한다.

- **📢 섹션 요약 비유**: 작은 물건 두 개를 한 상자에 넣어 배송하면 포장은 절약되지만, 서로 다른 고객이 번갈아 상자를 가져가면 계속 회수와 재배송이 반복된다. 상자를 나누면 포장재는 더 들지만 물류는 훨씬 빨라진다.

---

## Ⅲ. 비교 및 연결

거짓 공유를 제대로 이해하려면 진짜 공유(True Sharing), 그리고 공유가 전혀 없는 경우와 구분해야 한다. 진짜 공유는 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 정말 같은 변수 하나를 읽고 쓰는 상황이고, 거짓 공유는 변수는 다르지만 캐시 라인이 같아 충돌하는 상황이다. 반면 물리적으로도 라인이 분리되어 있으면 서로 독립적으로 진행된다.

| 구분 | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 공유 여부 | 물리적 캐시 라인 | 대표 현상 | 주된 해결 방향 |
| :--- | :--- | :--- | :--- | :--- |
| 진짜 공유 (True Sharing) | 있음 | 같음 | [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) 확보를 위한 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 비용 | 락 축소, 원자 연산 최소화, [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 변경 |
| 거짓 공유 (False Sharing) | 없음 | 같음 | 불필요한 무효화와 캐시 핑퐁 | [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/), 구조 분리, [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)별 로컬화 |
| 독립 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 없음 | 다름 | 코어별 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성 유지 | 현재 구조 유지 |

이 비교가 중요한 이유는 해결책이 서로 다르기 때문이다. 진짜 공유는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 의미가 겹치므로 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 핵심이지만, 거짓 공유는 의미가 겹치지 않으므로 물리 배치를 바꾸는 것이 더 직접적이다. 락을 제거했다고 거짓 공유가 사라지는 것도 아니고, 원자 연산 (Atomic [Operation](/knowledge-base/studynote/05_database/06_dw_olap_trends/329_delta_encoding/))을 쓴다고 해서 자동으로 해결되는 것도 아니다.

또한 거짓 공유는 컴퓨터구조만의 문제가 아니다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 관점에서는 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 스케줄링과 CPU 친화도 ([CPU Affinity](/knowledge-base/studynote/02_operating_system/02_process_thread/144_cpu_affinity/)), [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 관점에서는 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)([sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/)), 애플리케이션 관점에서는 `LongAdder` 같은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 누적 구조로 연결된다. 즉, 하드웨어의 캐시 라인 제약이 소프트웨어 설계 패턴까지 밀어 올리는 사례다.

- **📢 섹션 요약 비유**: 진짜 공유는 두 사람이 같은 펜 하나를 같이 쓰는 문제이고, 거짓 공유는 펜은 따로 있는데 둘 다 같은 필통 뚜껑을 계속 열어야 하는 문제다. 겉보기엔 비슷한 지연이지만, 고치는 방법은 전혀 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 거짓 공유는 "멀티스레드로 바꿨는데 CPU 사용률은 높은데 처리량은 안 오른다"는 형태로 자주 나타난다. 특히 통계 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), 생산자-소비자 큐의 head/tail [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), 워커별 상태 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/), [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 집계 버퍼처럼 자주 갱신되는 작은 필드가 위험하다. 이때는 코드의 락 유무보다 해당 필드들이 같은 캐시 라인에 모여 있는지부터 의심해야 한다.

### 실무 판단 체크포인트

1. 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 같은 구조체의 서로 다른 필드를 매우 자주 갱신하는가?
2. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하가 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 수 증가와 함께 더 심해지는가?
3. `perf c2c`의 HITM ([Hit](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/) Modified) 같은 지표에서 특정 라인이 과도하게 관찰되는가?
4. 필드 분리나 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)별 로컬 집계 후 마지막에 병합하는 구조로 바꿀 수 있는가?

### 대표 대응 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

- <strong><a href="/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/">패딩</a>과 정렬 적용</strong>: `alignas(64)` 또는 언어별 [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 기법으로 핫 필드를 분리한다.
- <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>별 로컬 <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/">카운터</a></strong>: 즉시 공유 갱신 대신 각 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 로컬 값에 누적 후 주기적으로 합산한다.
- **구조체 분해**: 자주 쓰는 필드와 거의 읽기 전용인 필드를 분리해 구조체를 재배치한다.
- **언어 기능 활용**: Java (Java [Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))의 `@Contended`, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) 클래스 등을 활용한다.

반대로 무조건 [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)을 넣는 것도 좋은 설계는 아니다. 읽기 중심 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)까지 과도하게 벌리면 캐시 효율이 떨어지고, 메모리 사용량도 커진다. 따라서 "자주 쓰는 작은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)에 의해 독립적으로 갱신되는가"를 먼저 확인한 뒤 적용해야 한다.

- **📢 섹션 요약 비유**: 병목 진단은 교통 체증을 보는 것과 같다. 자동차가 부족한 게 아니라 톨게이트 차로가 잘못 붙어 있으면, 차를 더 늘릴수록 더 막힌다. 이때 필요한 것은 차를 더 세게 모는 것이 아니라 차로를 다시 나누는 일이다.

---

## Ⅴ. 기대효과 및 결론

거짓 공유를 해소하면 멀티코어 확장성이 눈에 띄게 좋아진다. 코어 수를 늘릴수록 처리량이 자연스럽게 증가하고, 캐시 무효화로 낭비되던 인터커넥트 대역폭도 줄어든다. 특히 짧은 원자 연산을 반복하는 시스템에서는 코드 한 줄보다 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치 한 번이 더 큰 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 개선을 만들 수 있다.

하지만 전제조건도 분명하다. 첫째, 실제 병목이 거짓 공유인지 측정으로 확인해야 한다. 둘째, 캐시 라인 크기와 런타임 특성을 고려하지 않은 과도한 [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)은 오히려 역효과를 낼 수 있다. 셋째, 거짓 공유는 메모리 배치 문제이므로, 구조체 수정·컴파일러 정렬·런타임 객체 배치까지 함께 봐야 한다.

결국 이 개념은 "[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 독립성과 물리적 독립성은 다르다"는 사실로 기억하면 된다. 멀티코어 시대의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)를 많이 만드는 데서 끝나지 않고, 그 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)들이 어떤 캐시 라인을 밟고 지나가는지까지 설계할 때 비로소 나온다.

- **📢 섹션 요약 비유**: 좋은 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 설계는 사람 수만 늘리는 것이 아니라 작업 공간까지 따로 마련해 주는 것이다. 각자 책상은 따로 있어야 동시에 일해도 서로 팔꿈치가 부딪히지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 캐시 라인 (Cache Line) | 거짓 공유가 발생하는 최소 물리 단위 |
| [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) ([Cache Coherence](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)) | 코어 간 최신값 유지를 위해 무효화가 발생하는 배경 |
| MESI (Modified, Exclusive, Shared, Invalid) | 캐시 라인의 상태 전이를 통해 소유권 충돌을 설명하는 기본 모델 |
| [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) ([Padding](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)) / 정렬 (Alignment) | 거짓 공유를 줄이는 대표적 메모리 배치 기법 |
| HITM ([Hit](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/) Modified) | 다른 코어가 수정한 라인 때문에 발생하는 충돌 징후를 찾는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지표 |
| [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/) ([Non-Uniform Memory Access](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/)) | 원격 노드 접근까지 겹치면 거짓 공유 비용이 더 커질 수 있는 시스템 구조 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">공간 지역성 (Spatial Locality)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">캐시 라인 (Cache Line) 단위 적재</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">캐시 일관성 (Cache Coherence) · MESI</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Write-Invalidate 기반 무효화 충돌</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">거짓 공유 (False Sharing)</div>
<div class="kb-diagram-tree-item" style="--depth:4">패딩 (Padding) · 정렬 (Alignment)</div>
<div class="kb-diagram-tree-item" style="--depth:4">스레드별 로컬 집계 · 샤딩 카운터</div>
</div>
</div>



이 흐름은 하드웨어의 지역성 최적화가, 멀티코어에서는 오히려 소프트웨어 레이아웃 최적화 과제를 낳는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 두 친구가 다른 숙제를 해도 같은 작은 책상을 같이 쓰면 자꾸 팔이 부딪혀요.
2. 컴퓨터도 서로 다른 숫자를 고치는데 같은 캐시 상자에 있으면 계속 "내 거야" 하며 싸워요.
3. 그래서 숫자들을 조금 떨어뜨려 놓으면 친구들이 각자 자기 자리에서 훨씬 빨리 숙제를 끝낼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 410 / 803

← **이전**: [408. MOESI 프로토콜](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/408_moesi_protocol/)
**다음**: [410. 메모리 일관성 모델 (Memory Consistency Model)](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/410_memory_consistency_model/) →

---
