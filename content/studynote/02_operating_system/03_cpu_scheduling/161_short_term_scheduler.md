---
title: 161. 단기 스케줄러 (Short-term Scheduler) / CPU 스케줄러
date: '2026-05-05'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 단기 [[079_kube_scheduler_pod_placement|스케줄러]] (Short-term Scheduler)는 [[088_ready_queue|준비 큐]] ([[088_ready_queue|Ready Queue]])에서 지금 당장 CPU (Central Processing Unit)를 줄 실행 주체를 고르는 [[001_operating_system_purpose|운영체제]]의 즉시성 판단 모듈이다.
> 2. **가치**: 이 선택은 [[138_response_time|응답 시간]], [[139_throughput|처리량]], 공정성, [[211_context_switch|문맥 교환]] 오버헤드를 동시에 좌우하므로 [[001_operating_system_purpose|운영체제]] 체감 [[282_performance_tactics|성능]]의 중심축이 된다.
> 3. **판단 포인트**: 좋은 단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 단순히 공평한 것이 아니라, 매우 짧은 시간 안에 결정하면서도 워크로드와 코어 구조에 맞게 선점·우선순위·캐시 친화성을 균형 있게 다뤄야 한다.

---

## Ⅰ. 개요 및 필요성

단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 실행 가능한 프로세스나 [[092_thread_lwp|스레드]] 가운데 다음에 CPU를 할당할 대상을 선택하는 [[022_kernel_role|커널]] 구성 요소다. 이름 그대로 아주 짧은 주기로 반복 동작하며, 타이머 [[016_interrupt_mechanism|인터럽트]]나 입출력 완료 같은 사건이 발생할 때마다 개입한다. 즉 단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 [[001_operating_system_purpose|운영체제]]가 "누가 지금 일할 차례인가"를 결정하는 가장 빈번한 판단 장치다.

이 개념이 필요한 이유는 대부분의 시스템에서 runnable 상태의 작업 수가 CPU 코어 수보다 많기 때문이다. [[003_time_sharing_system|시분할 시스템]] ([[003_time_sharing_system|Time-sharing System]])에서는 모두가 잠깐씩 CPU를 나눠 가져야 하므로, 선택이 느리거나 불공정하면 곧바로 응답 지연과 기아 현상이 나타난다. 특히 사용자 체감 속도는 평균 계산 [[282_performance_tactics|성능]]보다도 "얼마나 빨리 다시 CPU를 받는가"에 크게 좌우된다.

단기 [[079_kube_scheduler_pod_placement|스케줄러]]가 없거나 매우 비효율적이면 Ready Queue가 단순 대기열로 남아 장시간 대기, 과도한 [[211_context_switch|문맥 교환]], 캐시 무효화가 늘어난다. 그래서 단기 스케줄링은 단순한 순번 정하기가 아니라 CPU 이용률과 시스템 반응성을 지키는 핵심 운영 [[164_policy|정책]]이다.

- **📢 섹션 요약 비유**: 단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 놀이기구 앞에서 다음 탑승객을 바로바로 들여보내는 운영 요원과 같다. 사람을 늦게 부르거나 엉뚱하게 부르면 줄 전체가 꼬인다.

---

## Ⅱ. 아키텍처 및 핵심 원리

단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 보통 타이머 [[016_interrupt_mechanism|인터럽트]], [[088_ready_queue|준비 큐]], 스케줄링 [[164_policy|정책]], 디스패처가 함께 동작하는 구조로 이해한다. [[079_kube_scheduler_pod_placement|스케줄러]]가 "누구를 선택할지"를 결정하면, 디스패처가 실제 [[211_context_switch|문맥 교환]]인 [[033_context|Context]] Switch를 수행해 CPU 제어권을 넘긴다. 따라서 [[079_kube_scheduler_pod_placement|스케줄러]] 자체의 [[001_algorithm_definition|알고리즘]] 비용과 디스패치 지연은 분리해서 보되, 최종 체감 [[282_performance_tactics|성능]]에서는 함께 평가해야 한다.

### 단기 스케줄링의 핵심 구성

| 요소 | 역할 | 병목 포인트 |
| :--- | :--- | :--- |
| [[088_ready_queue|Ready Queue]] | 실행 가능한 작업 집합 보관 | 큐 탐색 비용, 우선순위 관리 |
| Scheduling [[164_policy|Policy]] | 다음 실행 대상을 선택 | 공정성, 응답성, [[139_throughput|처리량]]의 균형 |
| [[072_timer_interrupt|Timer Interrupt]] | 선점 시점 제공 | 너무 잦으면 오버헤드 증가 |
| [[168_dispatcher|Dispatcher]] | 실제 [[211_context_switch|문맥 교환]] 수행 | [[057_register|레지스터]] 저장·복원, [[357_tlb|TLB]] 영향 |

아래 그림은 단기 [[079_kube_scheduler_pod_placement|스케줄러]]가 개입하는 핵심 루프를 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                   short-term scheduling decision loop                      │
├────────────────────────────────────────────────────────────────────────────┤
│ Running task                                                               │
│    │                                                                       │
│    ├─ time slice expires / block / wakeup interrupt                        │
│    ▼                                                                       │
│ Kernel entry ─▶ save context ─▶ Ready Queue ─▶ pick next task              │
│                                                    │                       │
│                                                    ▼                       │
│                                               Dispatcher                   │
│                                                    │                       │
│                                                    ▼                       │
│                                             restore context                │
│                                                    │                       │
│                                                    ▼                       │
│                                                 Running                    │
└────────────────────────────────────────────────────────────────────────────┘
```

이 그림에서 중요한 점은 스케줄링 결정이 길어질수록 사용자 작업이 아니라 [[022_kernel_role|커널]]이 CPU를 쓰는 시간이 늘어난다는 것이다. 그래서 Linux의 CFS (Completely Fair Scheduler)처럼 자료구조를 정교하게 쓰더라도, 호출 빈도가 매우 높다는 사실을 항상 염두에 두어야 한다. 또한 멀티코어 환경에서는 단순히 "다음 프로세스"만 고르는 것이 아니라 어느 코어에 둘지, 캐시 친화성을 유지할지, [[377_numa_allocation|NUMA]] ([[377_numa_allocation|Non-Uniform Memory Access]]) 비용을 줄일지도 함께 고려한다.

선점형 [[164_policy|정책]]에서는 타임 퀀텀 (Time [[690_round_robin_time_quantum|Quantum]])이 너무 짧으면 [[211_context_switch|문맥 교환]]이 많아지고, 너무 길면 대화형 응답성이 떨어진다. 결국 단기 스케줄링의 핵심 원리는 빠른 결정, 적절한 선점, 최소한의 교환 비용을 동시에 맞추는 데 있다.

- **📢 섹션 요약 비유**: 단기 스케줄링은 릴레이 경기에서 다음 주자를 고르고 바통을 넘기는 과정과 같다. 선택이 늦거나 전달이 서툴면 전체 기록이 나빠진다.

---

## Ⅲ. 비교 및 연결

단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 [[163_long_term_scheduler|장기 스케줄러]], [[162_medium_term_scheduler_swapping|중기 스케줄러]]와 역할이 다르다. [[163_long_term_scheduler|장기 스케줄러]]는 시스템에 들어올 작업 수를 조절하고, [[162_medium_term_scheduler_swapping|중기 스케줄러]]는 메모리 혼잡 시 프로세스를 일시적으로 내보내는 [[335_swapping|스와핑]] ([[335_swapping|Swapping]])과 연결된다. 반면 단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 이미 실행 가능한 후보들 사이에서 실시간으로 CPU를 배분한다.

| 구분 | 단기 [[079_kube_scheduler_pod_placement|스케줄러]] | [[162_medium_term_scheduler_swapping|중기 스케줄러]] | [[163_long_term_scheduler|장기 스케줄러]] |
| :--- | :--- | :--- | :--- |
| 주 역할 | Ready → Running 선택 | 메모리 혼잡 완화 | 시스템 진입량 조절 |
| 실행 빈도 | 매우 높음 | 중간 | 낮음 |
| 주요 자원 | CPU 시간 | 메모리 + 디스크 | 전체 시스템 부하 |
| 핵심 지표 | [[138_response_time|응답 시간]], 공정성 | [[257_thrashing|스래싱]] 완화 | [[258_degree_of_multiprogramming|다중 프로그래밍 정도]] |

또한 단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 스케줄링 [[001_algorithm_definition|알고리즘]]과도 직접 연결된다. [[173_fcfs_scheduling|FCFS]] (First-Come, First-Served)는 단순하지만 대화형 응답성이 떨어지고, [[834_load_balancing_algorithm_round_robin_least_connection|RR]] (Round Robin)은 공정하지만 퀀텀 설정에 민감하며, CFS는 가상 실행 시간을 기준으로 균형을 맞춘다. 즉 단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 하나의 개념이 아니라 "어떤 [[164_policy|정책]]으로 CPU를 잘게 배분할 것인가"라는 여러 [[001_algorithm_definition|알고리즘]]의 실행 무대다.

이 주제는 CPU 바운드 (CPU Bound) 작업과 I/O 바운드 (I/O Bound) 작업의 균형, [[754_context_switch_cost|문맥 교환 비용]], 캐시 친화성과도 이어진다. 그래서 단기 스케줄링을 설명할 때는 단순 [[001_algorithm_definition|알고리즘]] 이름 나열보다 "왜 이 선택이 체감 [[282_performance_tactics|성능]] 차이로 이어지는가"를 말하는 것이 중요하다.

- **📢 섹션 요약 비유**: 단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 하루 일정을 분 단위로 짜는 관리자이고, 장기·[[162_medium_term_scheduler_swapping|중기 스케줄러]]는 사람 수와 공간을 조절하는 총괄 운영자와 같다. 시간 축과 관심 자원이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 단기 [[079_kube_scheduler_pod_placement|스케줄러]]를 직접 구현하지 않더라도, 시스템 [[282_performance_tactics|성능]] 문제의 상당수가 스케줄링과 연결된다. 웹 서버에서 [[092_thread_lwp|스레드]]를 과도하게 늘리면 CPU는 실제 업무보다 [[211_context_switch|문맥 교환]]에 더 많은 시간을 쓰게 되고, 실시간 제어 시스템에서는 반대로 우선순위 높은 작업이 즉시 선점되지 않으면 마감 시간을 놓칠 수 있다. 따라서 단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 [[001_operating_system_purpose|운영체제]] 내부 주제이면서 동시에 애플리케이션 아키텍처의 제약 조건이기도 하다.

### 판단 [[435_checklist_based_testing|체크리스트]]

1. **목표가 [[138_response_time|응답 시간]]인가, [[139_throughput|처리량]]인가, 공정성인가?** 우선 목표를 정해야 [[164_policy|정책]] 선택이 가능하다.
2. **[[754_context_switch_cost|문맥 교환 비용]]이 작업 시간 대비 과도하지 않은가?** 짧은 작업이 많을수록 오버헤드가 문제 된다.
3. **멀티코어와 캐시 친화성을 고려하고 있는가?** 코어 사이를 과하게 이동하면 [[282_performance_tactics|성능]]이 떨어진다.
4. **실시간 보장이 필요한가?** 그렇다면 범용 공정성보다 RTOS (Real-Time [[001_operating_system_purpose|Operating System]])형 우선순위 보장이 더 중요하다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 코어 수보다 훨씬 많은 runnable [[092_thread_lwp|스레드]]를 만들어 [[079_kube_scheduler_pod_placement|스케줄러]] 부하를 키우는 경우
- 퀀텀을 지나치게 짧게 잡아 [[211_context_switch|문맥 교환]] 폭증을 유발하는 경우
- 우선순위 [[164_policy|정책]]만 보고 캐시 재사용성과 CPU Affinity를 무시하는 경우
- 대화형 서버에 배치형 스케줄링 관점을 그대로 적용하는 경우

예를 들어 백엔드 서버는 [[092_thread_lwp|스레드]] 수를 무작정 늘리기보다 비동기 I/O와 적절한 워커 수를 통해 runnable 집합을 관리해야 하고, RTOS (Real-Time [[001_operating_system_purpose|Operating System]]) 환경은 평균 [[139_throughput|처리량]]보다 최악 응답 지연을 더 엄격히 봐야 한다. 즉 단기 [[079_kube_scheduler_pod_placement|스케줄러]] 관련 판단은 [[001_operating_system_purpose|운영체제]] 내부 [[164_policy|정책]]만의 문제가 아니라, 애플리케이션 구조와 [[090_service_kubernetes_network_load_balancing|서비스]] 목표를 함께 맞추는 작업이다.

- **📢 섹션 요약 비유**: 단기 [[079_kube_scheduler_pod_placement|스케줄러]] 튜닝은 도로 [[130_signal|신호]] 체계를 조정하는 일과 같다. 차가 많다고 무조건 [[130_signal|신호]]를 자주 바꾸면 오히려 교차로 전체가 막힐 수 있다.

---

## Ⅴ. 기대효과 및 결론

좋은 단기 스케줄링은 CPU를 더 빠르게 만드는 것이 아니라, 한정된 CPU 시간을 더 납득 가능하게 배분한다. 그 결과 응답성이 좋아지고, 대화형 작업의 체감 지연이 줄며, 시스템 전체의 처리 흐름이 안정된다. 특히 [[675_multitasking_terminology_preemptive|멀티태스킹]] 환경에서는 공정성과 예측 가능성이 [[282_performance_tactics|성능]]만큼 중요한 품질이 된다.

앞으로의 단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 단순 공정성에서 더 나아가 이기종 코어, 전력 효율, 캐시 지역성, [[090_service_kubernetes_network_load_balancing|서비스]] 등급을 함께 고려하는 방향으로 발전하고 있다. 따라서 이 주제는 "누구를 실행시킬까"라는 단순 질문이 아니라, "짧은 시간 안에 어떤 기준으로 CPU를 배분해야 전체 시스템이 가장 잘 움직이는가"라는 운영 철학으로 기억하는 것이 좋다.

- **📢 섹션 요약 비유**: 좋은 단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 줄을 세우는 반장이라기보다, 교실 전체가 시끄러워지지 않게 발표 순서를 조정하는 선생님과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[211_context_switch|문맥 교환]] ([[211_context_switch|Context Switch]]) | 단기 스케줄링 결정이 실제 CPU 전환 비용으로 이어지는 핵심 후속 동작이다. |
| [[088_ready_queue|Ready Queue]] | 단기 [[079_kube_scheduler_pod_placement|스케줄러]]의 직접적인 입력 집합이다. |
| CFS (Completely Fair Scheduler) | 현대 범용 [[001_operating_system_purpose|운영체제]]에서 단기 스케줄링 [[164_policy|정책]]을 구현하는 대표 사례다. |
| [[144_cpu_affinity|CPU Affinity]] | 스케줄링 선택이 캐시 적중률과 코어 이동 비용에 미치는 영향을 설명한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
시분할 시스템 (Time-sharing System)
        │
        ▼
Ready Queue + 선점형 스케줄링
        │
        ▼
RR / Priority / CFS
        │
        ▼
멀티코어 · NUMA · CPU Affinity
        │
        ▼
에너지 인지 스케줄링
```

이 흐름은 단기 스케줄링이 단순 순번 결정에서 출발해, 멀티코어와 전력 인지 [[164_policy|정책]]까지 확장되는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 안에는 먼저 일하고 싶어 하는 작은 일거리들이 줄을 서 있어요.
2. 단기 [[079_kube_scheduler_pod_placement|스케줄러]]는 그중에서 지금 누구 차례인지 아주 빨리 정해 주는 반장이에요.
3. 반장이 똑똑해야 모두가 오래 기다리지 않고 차례대로 잘 일할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 161 / 800

← **이전**: [[160_session_controlling_terminal|160. 세션 (Session) 및 제어 터미널 (Controlling Terminal)]]
**다음**: [[162_medium_term_scheduler_swapping|162. 중기 스케줄러 (Medium-term Scheduler) - 스와핑 (Swapping)]] →

---
