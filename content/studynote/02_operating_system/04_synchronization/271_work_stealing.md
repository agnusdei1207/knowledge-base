+++
title = "271. 스레드 풀 스케줄링 락 경합 (Work Stealing)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 멀티 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 프로그래밍에서 모든 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 단 하나의 전역 큐(Global [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))에서 작업을 꺼내가려 하면 '큐 락([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))' 경합 때문에 시스템 전체가 느려지는데, Work Stealing은 <strong>각 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">스레드</a>에게 독립적인 로컬 큐를 부여하여 <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/">락 경합</a>을 원천적으로 회피</strong>하는 아키텍처다.
> 2. **가치**: 자신의 큐에 일이 다 떨어져서 놀고 있는 잉여 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(Thief)가, 바쁘게 일하고 있는 다른 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)(Victim)의 큐 뒷부분에서 작업을 몰래 훔쳐옴(Steal)으로써, <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a> 오버헤드 없이 완벽한 <a href="/knowledge-base/studynote/03_network/16_data_center_cloud/833_load_balancing_l4_l7_switch_traffic_distribution/">로드 밸런싱</a>(부하 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>)</strong>을 달성한다.
> 3. **융합**: Java의 `ForkJoinPool`, C++의 TBB, Go, Rust의 [고루틴](/knowledge-base/studynote/02_operating_system/02_process_thread/140_goroutine/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 등 현대의 모든 고성능 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 프레임워크의 심장부에 기본 탑재되어 매니코어(Many-core) 시대의 성능을 극한으로 끌어올리고 있다.

---

## Ⅰ. 개요 및 필요성

> ⚠️ 이 문서는 멀티코어 환경에서 여러 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 하나의 작업 대기열([Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))에 동시에 접근하려다 발생하는 심각한 병목 현상을 해결하기 위해, 각 코어마다 전용 대기열을 두고 남의 큐에서 몰래 작업을 훔쳐오는 기발하고 혁신적인 부하 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 알고리즘인 'Work Stealing(작업 훔치기)'을 다룹니다.

우리가 흔히 아는 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)([Thread Pool](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/))의 기본 구조는 단순하다. 중앙에 거대한 '할 일 목록(Global [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))'이 하나 있고, 100명의 일꾼([Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))이 달려들어 일을 하나씩 빼간다.

* <strong>최악의 병목 (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/">Lock Contention</a>)</strong>: 
  - 큐([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))는 여러 명이 동시에 빼가면 엉키기 때문에, 누군가 하나 뺄 때마다 전체 큐에 <strong>락(<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a>)</strong>을 걸어야 한다. 
  - 100개의 코어가 일을 빼가려고 동시에 큐에 달려들면, 1개 코어만 일하고 99개 코어는 락이 풀리길 기다리며 줄을 서서 논다. (배보다 배꼽이 더 큰 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 오버헤드)

이 문제를 해결하기 위한 발상의 전환이 <strong>"전체 큐를 쪼개서 각 일꾼의 책상(Local <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a>)에 나눠주자!"</strong> 였다. 각자 자기 책상에서만 일을 빼가면 락을 걸 필요가 없어진다.
그런데 여기서 새로운 문제가 발생한다. "만약 A 일꾼은 책상에 일이 산더미고, B 일꾼은 5분 만에 일을 다 끝내서 놀고 있다면?"
이 불균형을 극적으로 해결한 천재적인 알고리즘이 바로 <strong>Work Stealing (작업 훔치기)</strong>이다.

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Work Stealing을 완벽하게 구현하기 위해, 큐([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/)) 대신 양쪽에서 다 빼낼 수 있는 <strong>덱(<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/084_deque/">Deque</a>, Double-Ended <a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a>)</strong> 자료구조를 사용한다.

#### 1. 정상 작업 모드 (LIFO: 나 혼자 일할 때)
- 일꾼([스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/))은 자기 책상(로컬 덱)의 <strong>앞쪽(Top)</strong>에서만 일을 넣고 뺀다. 
- 이것은 마치 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/))과 같아서, 가장 최근에 들어온 일을 가장 먼저 처리(LIFO)한다. CPU 캐시 히트율(Cache [Hit](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/263_cache_hit_miss/) Rate)이 극대화되어 엄청나게 빠르며, 자기 혼자 쓰므로 <strong>락(<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a>)이 아예 필요 없다</strong>.

#### 2. 도둑질 모드 ([FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/): 남의 일을 훔칠 때)
- 일꾼 B가 자기 책상의 일을 다 끝내고 놀게 되었다. ([Idle](/knowledge-base/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/) 상태)
- 놀고 있는 일꾼 B(도둑)는 바쁜 일꾼 A(희생자)의 책상으로 몰래 다가간다.
- 도둑 B는 희생자 A가 일하고 있는 앞쪽(Top)을 건드리지 않고, 덱의 반대편인 <strong>뒤쪽(Bottom)</strong>에서 오래된 작업을 슬쩍 빼간다. ([FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/))
- 희생자는 앞쪽에서 놀고, 도둑은 뒤쪽에서 빼가기 때문에 서로 손이 부딪힐 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)([락 경합](/knowledge-base/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/))이 획기적으로 낮아진다!



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Work Stealing (작업 훔치기)의 Deque(덱) 기반 동기화 회피 시각화</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">바쁜 스레드 A의 책상 (Local Deque)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">작업 5</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">A는 가장 최근 일부터 뺌)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">작업 4</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">작업 3</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">작업 2</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">작업 1</div><div class="kb-diagram-connector">←</div><div class="kb-diagram-note">B는 뒤에서 오래된 일부터 훔침!)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">★ 핵심: 주인은 Top에서, 도둑은 Bottom에서 빼가기 때문에 서로 영역이</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">겹치지 않아 락(Lock)을 걸 필요가 거의 없다!</div></div>
</div>
</div>



**[다이어그램 해설]** 왜 하필 도둑은 가장 오래된 작업(Bottom)을 훔쳐갈까? [분할 정복](/knowledge-base/studynote/08_algorithm_stats/01_basics/005_divide_and_conquer/)(Divide & Conquer) 알고리즘에서 가장 오래된 작업(Bottom)일수록 쪼개지지 않은 엄청나게 큰 덩어리의 작업일 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이 높기 때문이다. 도둑이 이 큰 덩어리를 훔쳐 가서 자기 책상에서 잘게 쪼개어 처리하면 전체 시스템의 [로드 밸런싱](/knowledge-base/studynote/03_network/16_data_center_cloud/833_load_balancing_l4_l7_switch_traffic_distribution/) 효율이 폭발적으로 상승한다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

Work Stealing 알고리즘을 가장 널리 유행시킨 것은 Java 7에 도입된 <strong><code>ForkJoinPool</code></strong>이다. 

* **Fork (쪼개기)**: 큰 작업을 작은 작업으로 계속 쪼개서 자기 로컬 덱의 Top에 푸시(Push)한다.
* <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">Join</a> (합치기)</strong>: 쪼개진 작업들의 결과가 나오면 병합한다.
* 일반적인 [스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/)(ExecutorService)은 네트워크 I/O처럼 오래 기다리는 작업에 적합하지만, 수억 개의 데이터를 정렬하거나 이미지 픽셀을 변환하는 것 같은 <strong>CPU 집약적인 거대 연산</strong>을 할 때는 글로벌 큐 락 때문에 엄청 느려진다. 
* 이때 개발자가 `ForkJoinPool`을 적용하면, 각 코어가 100% 쉬지 않고 남의 일을 훔쳐 가며 계산을 때려 부수므로 다중 코어의 성능을 극한까지 끌어올릴 수 있다.

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

"남의 밥그릇을 훔치는 것이, 시스템 전체를 살찌우는 가장 빠른 길이다."
Work Stealing(작업 훔치기) 알고리즘은 중앙 집중화된 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 제어가 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성의 가장 큰 적임을 깨달은 컴퓨터 공학의 눈부신 통찰이다. 각자 독립된 환경에서 자유를 누리되, 누군가 노는 순간이 발생하면 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 충돌을 최소화하는 방향으로 부하를 재분배하는 이 우아한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 아키텍처는, 코어 개수가 수십 수백 개로 늘어나는 현대 클라우드 및 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 환경에서 성능을 지탱하는 핵심 척추로 자리 잡았다.

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

[스레드 풀](/knowledge-base/studynote/02_operating_system/02_process_thread/103_thread_pool/) 스케줄링 [락 경합](/knowledge-base/studynote/02_operating_system/04_synchronization/275_lock_contention_monitoring/) (Work Stealing)은 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)와 [상호 배제](/knowledge-base/studynote/02_operating_system/05_deadlock/283_mutual_exclusion/) 제어을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [더블 체크드 락킹](/knowledge-base/studynote/02_operating_system/04_synchronization/272_double_checked_locking/) ([Double-Checked Locking](/knowledge-base/studynote/02_operating_system/04_synchronization/272_double_checked_locking/)) [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) 및 해결 (volatile)처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [하드웨어 트랜잭셔널 메모리](/knowledge-base/studynote/02_operating_system/04_synchronization/269_htm_intel_tsx/) ([HTM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/513_htm/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [락 엘리전](/knowledge-base/studynote/02_operating_system/04_synchronization/270_lock_elision/) ([Lock Elision](/knowledge-base/studynote/02_operating_system/04_synchronization/270_lock_elision/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [더블 체크드 락킹](/knowledge-base/studynote/02_operating_system/04_synchronization/272_double_checked_locking/) ([Double-Checked Locking](/knowledge-base/studynote/02_operating_system/04_synchronization/272_double_checked_locking/)) [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) 및 해결 (volatile) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 세큐어 코딩에서의 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 약점 ([TOCTOU](/knowledge-base/studynote/02_operating_system/04_synchronization/273_toctou/): Time of Check to Time of Use) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">락 엘리전 (Lock Elision)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스레드 풀 스케줄링 락 경합 (Work Stealing)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">더블 체크드 락킹 (Double-Checked Locking) 안티패턴 및 해결 (volatile)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">세큐어 코딩에서의 동기화 약점 (TOCTOU: Time of Check to Time of Use)</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 10명이 김밥을 마는데, 김밥 재료가 가운데 한 통에만 있으면 재료를 꺼낼 때마다 서로 손이 부딪히고 엄청 기다려야 해요 (글로벌 큐 락).
2. 그래서 각자 자기 책상에 재료를 다 나눠주고 혼자서 빨리빨리 만들게 했죠. 그런데 내 책상에 재료가 먼저 다 떨어져서 놀게 되면 어떡하죠?
3. 놀고 있는 사람이, 일이 엄청 많이 남은 옆 친구 책상 뒤로 몰래 다가가서 김밥 재료를 슬쩍 훔쳐 와서(Work Stealing) 자기 자리에서 만듭니다! 서로 부딪히지 않고 엄청 빨리 김밥 1,000줄을 완성할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 271 / 800

← **이전**: [270. 락 엘리전 (Lock Elision) - 하드웨어 지원 락 우회](/knowledge-base/studynote/02_operating_system/04_synchronization/270_lock_elision/)
**다음**: [272. 더블 체크드 락킹 (Double-Checked Locking) 안티패턴 및 해결 (volatile)](/knowledge-base/studynote/02_operating_system/04_synchronization/272_double_checked_locking/) →

---
