---
title: 174. 호위 효과 (Convoy Effect) - FCFS의 단점
date: '2026-03-22'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 호위 효과 (Convoy Effect)는 [[173_fcfs_scheduling|FCFS]] (First-Come, First-Served) 같은 [[285_no_preemption|비선점]] [[261_fifo_page_replacement|FIFO]] (First-In, First-Out) 스케줄링에서 긴 CPU (Central Processing Unit) 바운드 작업 하나가 앞을 막아, 짧은 I/O (Input/Output) 바운드 작업들이 줄줄이 지연되는 현상이다.
> 2. **가치**: 이 현상은 평균 대기 시간만 악화시키는 것이 아니라 CPU와 I/O 장치의 병렬성을 무너뜨려 전체 자원 이용률과 응답성을 함께 떨어뜨린다.
> 3. **판단 포인트**: 작업 길이 편차가 큰 환경, 대화형 [[090_service_kubernetes_network_load_balancing|서비스]], 단일 [[261_fifo_page_replacement|FIFO]] 이벤트 루프에서는 convoy effect를 반드시 경계해야 하며, 선점·작업 분리·다단계 큐가 핵심 완화 수단이다.

---

## Ⅰ. 개요 및 필요성

호위 효과는 느린 선두 차량 뒤에 빠른 차량들이 줄지어 속도를 빼앗기는 상황을 [[001_operating_system_purpose|운영체제]]에 옮긴 개념이다. [[088_ready_queue|Ready Queue]] 맨 앞에 긴 CPU 바운드 프로세스가 있으면, 뒤에 있는 짧은 I/O 바운드 프로세스는 금방 끝낼 수 있어도 CPU를 받을 때까지 기다려야 한다. FCFS는 도착 순서를 지켜 준다는 장점이 있지만, [[090_service_kubernetes_network_load_balancing|서비스]] 시간이 크게 다른 작업을 같은 줄에 세우는 순간 전체 흐름이 가장 느린 작업의 리듬에 묶인다.

이 개념이 중요한 이유는 "공정한 줄서기"가 곧 "좋은 응답성"을 뜻하지 않기 때문이다. [[459_quic_fec_forward_error_correction|초기]] 배치 시스템에서는 구현 단순성이 중요했지만, 대화형 시스템에서는 짧은 작업의 첫 반응 시간이 훨씬 중요하다. 호위 효과는 바로 이 차이를 드러내며, 왜 [[285_no_preemption|비선점]] FCFS가 현대 범용 시스템의 주 [[079_kube_scheduler_pod_placement|스케줄러]]가 되기 어려운지 설명해 준다.

아래 그림은 긴 작업 하나가 어떻게 짧은 작업들과 I/O 장치까지 동시에 묶어 두는지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Convoy effect in one ready queue                                  │
├────────────────────────────────────────────────────────────────────┤
│ CPU        : [ long CPU-bound job P1 ........................... ] │
│ Ready Queue:                      [P2][P3][P4] short jobs wait    │
│ I/O device : idle ----------------------------------------------  │
│ result     : one long burst dictates the pace of everyone         │
└────────────────────────────────────────────────────────────────────┘
```

핵심은 뒤에 있는 작업들이 단지 늦게 끝나는 것에서 그치지 않는다는 점이다. 짧은 작업들이 CPU를 받지 못하니 I/O 요청도 늦게 발생하고, 그동안 I/O 장치는 놀게 된다. 즉 convoy effect는 한 줄이 막히는 현상이 아니라, 시스템 안의 여러 자원을 엇박자로 만드는 구조적 병목이다.

- **📢 섹션 요약 비유**: 호위 효과는 편도 1차선 도로 앞에서 느린 트럭 한 대가 전체 차선의 속도를 결정해 버리는 상황과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

호위 효과의 메커니즘은 간단하다. 첫째, 긴 CPU burst가 큐 맨 앞에 선다. 둘째, 짧은 작업들은 기다리는 동안 I/O를 시작하지 못한다. 셋째, 긴 작업이 끝난 뒤 짧은 작업들이 한꺼번에 CPU를 조금씩 쓰고 다시 I/O로 빠지면, 이번에는 반대로 CPU가 쉬게 된다. 결국 CPU와 I/O 장치가 번갈아 놀면서 전체 처리량이 떨어진다.

예를 들어 P1은 `CPU 20ms`, P2와 P3는 `CPU 1ms + I/O 6ms`라고 하자. 모두 동시에 도착했는데 FCFS가 P1을 먼저 잡으면 다음과 같은 흐름이 나온다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Resource desynchronization caused by convoy effect                │
├────────────────────────────────────────────────────────────────────┤
│ time : 0................20 21 22......27 28                       │
│ CPU  : [P1..............][P2][P3][ idle ][P2][P3]                 │
│ I/O  : [idle............][P2 I/O......][P3 I/O......]             │
│ wait : P2 starts after 20ms, P3 starts after 21ms                 │
└────────────────────────────────────────────────────────────────────┘
```

위 도식에서 0~20ms 동안 I/O 장치는 사실상 쉬고 있다. 반대로 22~27ms 구간에는 짧은 작업들이 모두 I/O로 빠져 CPU가 놀게 된다. 즉 시스템은 두 자원을 동시에 잘 쓰는 대신, 한쪽이 바쁘면 다른 쪽이 쉬는 나쁜 리듬에 빠진다.

대기 시간 악화도 수치로 분명하다.

| 실행 순서 | 대기 시간 | 평균 대기 시간 |
| :--- | :--- | :--- |
| `P1 -> P2 -> P3` | `0, 20, 21` | `(0 + 20 + 21) / 3 = 13.67ms` |
| `P2 -> P3 -> P1` | `0, 1, 2` | `(0 + 1 + 2) / 3 = 1.00ms` |

결국 호위 효과의 본질은 "긴 작업 하나의 불이익"이 아니라 "짧은 작업 다수의 지연이 누적되는 총비용"이다. 그래서 [[079_kube_scheduler_pod_placement|스케줄러]]는 단순 순서 공정성보다, 작업 길이와 반응 시간의 분포를 함께 고려해야 한다.

- **📢 섹션 요약 비유**: 마트 계산대에서 카트 가득 담은 손님 한 명이 앞에 서면, 아이스크림 하나 사려는 열 명의 대기 시간이 한꺼번에 폭증하는 것과 같다.

---

## Ⅲ. 비교 및 연결

호위 효과를 이해하려면 FCFS를 다른 스케줄링 [[164_policy|정책]]과 비교해야 한다. FCFS는 가장 단순하지만 긴 burst를 제어하지 못하고, [[834_load_balancing_algorithm_round_robin_least_connection|RR]] (Round Robin)은 time quantum으로 긴 작업을 쪼개 convoy를 완화한다. [[175_sjf_scheduling|SJF]] ([[175_sjf_scheduling|Shortest Job First]])나 [[177_srtf_scheduling|SRTF]] (Shortest Remaining Time First)는 짧은 작업을 먼저 보내 평균 대기 시간을 낮추지만, 대신 burst 예측과 [[314_starvation_prevention|starvation]] 문제가 따라온다.

| [[164_policy|정책]] | 호위 효과 민감도 | 장점 | 대가 |
| :--- | :--- | :--- | :--- |
| [[173_fcfs_scheduling|FCFS]] | 높음 | 구현 단순, 순서 보장 | 긴 작업이 전체 응답성 악화 |
| [[834_load_balancing_algorithm_round_robin_least_connection|RR]] | 낮음 | 첫 반응 시간 개선, 긴 작업 [[136_variance|분산]] | [[211_context_switch|문맥 교환]] 오버헤드 증가 |
| [[175_sjf_scheduling|SJF]] / [[177_srtf_scheduling|SRTF]] | 낮음 | 평균 대기 시간 최소화 경향 | burst 예측 필요, [[314_starvation_prevention|starvation]] 가능 |
| [[691_mlfq_multi_level_feedback_queue|MLFQ]] (Multilevel Feedback [[058_queue|Queue]]) | 낮음 | 짧은 interactive 작업 우대 | [[164_policy|정책]] 튜닝과 구현 복잡도 증가 |

이 현상은 [[001_operating_system_purpose|운영체제]] 안에만 갇혀 있지 않다. 네트워크에서는 [[456_quic_hol_head_of_line_blocking_resolution|HOL]] ([[456_quic_hol_head_of_line_blocking_resolution|Head-of-Line]]) Blocking으로 나타나고, 멀티스레드에서는 [[510_lock|lock]] convoy로, 단일 [[092_thread_lwp|스레드]] 이벤트 루프에서는 long [[150_task|task]] blocking으로 나타난다. 공통점은 하나다. **[[090_service_kubernetes_network_load_balancing|서비스]] 시간이 긴 항목이 FIFO의 머리를 차지하면, 뒤에 있는 짧은 항목들이 구조적으로 손해 본다**는 점이다.

그래서 convoy effect는 스케줄링 이론의 옛 사례가 아니라, 오늘날 큐 기반 시스템을 설계할 때도 반복해서 등장하는 경고문이다. 웹 요청 큐, 메시지 소비기, 배치 작업 [[123_pipe|파이프]]라인 모두 같은 패턴에 취약할 수 있다.

- **📢 섹션 요약 비유**: 호위 효과는 [[123_pipe|파이프]] 입구를 큰 돌이 막아 뒤의 물줄기가 다 함께 느려지는 현상과 같아서, 분야만 달라질 뿐 원인은 비슷하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 convoy effect를 잘 쓰는 핵심은 업무 성격이 다른 작업을 같은 단일 [[261_fifo_page_replacement|FIFO]] 경로에 태우지 않는 것이다. 웹 서버의 사용자 요청과 백그라운드 배치, 단일 [[092_thread_lwp|스레드]] 이벤트 루프의 짧은 콜백과 긴 CPU 연산, 데이터베이스의 짧은 트랜잭션과 장기 보고서 쿼리는 서로 다른 차선을 가져야 한다. 사용자는 단지 응답이 느리다고 느끼지만, 내부에서는 긴 작업 하나가 짧은 작업 다수를 묶고 있는 경우가 많다.

아래 판단 흐름은 언제 convoy effect를 적극적으로 의심해야 하는지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ When to suspect convoy effect                                     │
├────────────────────────────────────────────────────────────────────┤
│ mixed heavy and light jobs in one FIFO queue?                     │
│   ├─ yes ─▶ split queues or add preemption                        │
│   └─ no                                                           │
│        │                                                          │
│        ▼                                                          │
│ response time critical?                                           │
│   ├─ yes ─▶ RR / MLFQ / priority scheduling                       │
│   └─ no  ─▶ FCFS acceptable for bounded batch jobs                │
└────────────────────────────────────────────────────────────────────┘
```

### 실무 판단 기준

1. **작업 분포 [[396_validation|확인]]**: heavy job과 light job이 한 큐에 섞여 있는지 먼저 본다.
2. **선점 가능성 확보**: CPU scheduler라면 time [[690_round_robin_time_quantum|quantum]], 애플리케이션이라면 cooperative yield나 worker 분리를 검토한다.
3. **자원별 지표 동시 관찰**: CPU 사용률만 보지 말고 I/O 대기, [[058_queue|queue]] wait, response time을 함께 본다.
4. **클래스 분리**: 사용자 요청과 배치 작업, interactive task와 background task를 서로 다른 큐로 분리한다.
5. **긴 임계구역 경계**: 락을 오래 쥐거나 단일 [[092_thread_lwp|스레드]]를 길게 점유하는 코드가 있는지 [[396_validation|확인]]한다.

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 대화형 요청과 장기 배치 작업을 하나의 [[261_fifo_page_replacement|FIFO]] 워커 큐에 섞어 넣는 것
- 단일 이벤트 루프에서 CPU 집약 작업을 동기적으로 실행하는 것
- FCFS의 단순함만 보고 작업 길이 편차와 [[138_response_time|응답 시간]] 목표를 무시하는 것

기술사 답안에서는 호위 효과를 단순히 "긴 프로세스 때문에 짧은 프로세스가 기다리는 현상"이라고만 쓰기보다, CPU와 I/O의 병렬성이 어떻게 깨지는지, 어떤 [[164_policy|정책]]이 이를 완화하는지, 애플리케이션 큐에도 어떻게 재현되는지까지 연결해야 깊이가 생긴다.

- **📢 섹션 요약 비유**: 출근길 승용차와 야간 화물차를 같은 1차선 도로에 몰아넣으면 결국 모두 느려지듯, 실무에서도 성격이 다른 작업은 처음부터 차선을 분리해야 한다.

---

## Ⅴ. 기대효과 및 결론

호위 효과를 인지하고 큐 구조를 조정하면 [[138_response_time|응답 시간]]과 자원 이용률이 함께 좋아진다. 짧은 작업은 빨리 CPU를 받아 빠르게 I/O로 넘어가고, 긴 작업도 선점이나 별도 큐를 통해 시스템 전체를 붙잡아 두지 못한다. 그 결과 사용자는 더 빠른 첫 반응을 얻고, 운영자는 CPU와 I/O가 동시에 일하는 건강한 리듬을 확보할 수 있다.

물론 convoy effect를 없애겠다고 무조건 quantum을 작게 줄이거나 우선순위를 과하게 주면 [[211_context_switch|문맥 교환]] 비용과 [[314_starvation_prevention|starvation]] 같은 다른 문제가 생길 수 있다. 따라서 목표는 "긴 작업을 벌주는 것"이 아니라 "긴 작업이 전체를 묶지 못하게 하는 것"이어야 한다. 이 균형이 바로 현대 [[079_kube_scheduler_pod_placement|스케줄러]] 설계의 핵심이다.

정리하면 convoy effect는 도착 순서 기반 공정성이 [[090_service_kubernetes_network_load_balancing|서비스]] 시간 분포를 만나면서 생기는 구조적 실패다. 기억할 핵심은 단순하다. **작업 길이 편차가 큰데도 하나의 [[285_no_preemption|비선점]] FIFO에 모두 태우면, 가장 느린 작업의 속도가 시스템 전체의 체감 속도가 된다.**

- **📢 섹션 요약 비유**: 호위 효과를 막는 일은 느린 차를 없애는 것이 아니라, 느린 차 한 대가 모든 차의 평균 속도를 결정하지 못하게 도로를 설계하는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[173_fcfs_scheduling|FCFS]] (First-Come, First-Served) | convoy effect가 가장 대표적으로 발생하는 [[285_no_preemption|비선점]] [[164_policy|정책]]이다. |
| CPU 바운드 / I/O 바운드 | 긴 계산형 작업과 짧은 입출력형 작업의 혼합이 문제의 출발점이다. |
| 대기 시간 (Waiting Time) | convoy effect가 직접 악화시키는 핵심 [[282_performance_tactics|성능]] 지표다. |
| [[138_response_time|응답 시간]] ([[138_response_time|Response Time]]) | 대화형 시스템에서 사용자 체감 품질 저하로 이어진다. |
| [[834_load_balancing_algorithm_round_robin_least_connection|RR]] (Round Robin) | 긴 burst를 잘라 convoy effect를 완화하는 대표 [[164_policy|정책]]이다. |
| [[456_quic_hol_head_of_line_blocking_resolution|HOL]] ([[456_quic_hol_head_of_line_blocking_resolution|Head-of-Line]]) [[122_sync_async_communication|Blocking]] | 큐의 머리에서 느린 항목이 전체를 막는 다른 분야의 유사 현상이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
mixed job lengths
    │
    ▼
long job at FIFO head
    │
    ├──────────────▶ short jobs wait in ready queue
    ├──────────────▶ I/O devices stay idle
    ▼
bursty release of short jobs
    │
    ▼
CPU / I/O imbalance · poor response time
    │
    ▼
preemption · class separation · MLFQ
```

이 흐름도는 convoy effect가 단순 대기열 문제를 넘어 자원 활용 불균형까지 만들어 내고, 그래서 현대 시스템이 선점과 다중 큐 구조로 진화했음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 아주 느린 코끼리가 골목길 맨 앞을 막고 걸으면 뒤의 토끼들도 함께 천천히 가야 해요.
2. 토끼들은 금방 갈 수 있는데도 코끼리 차례가 끝날 때까지 기다리느라 답답해져요.
3. 그래서 길을 나누거나 잠깐씩 번갈아 가게 해야 모두가 더 빨리 움직일 수 있어요.

