+++
title = "173. FCFS (First-Come, First-Served) 스케줄링 - 비선점"
date = 2026-03-22

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FCFS (First-Come, First-Served) 스케줄링은 [준비 큐](/knowledge-base/studynote/02_operating_system/02_process_thread/088_ready_queue/) ([Ready Queue](/knowledge-base/studynote/02_operating_system/02_process_thread/088_ready_queue/))에 먼저 도착한 프로세스를 먼저 실행하고, 스스로 종료하거나 I/O (Input/Output) 대기로 빠질 때까지 CPU (Central Processing Unit)를 빼앗지 않는 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) 정책이다.
> 2. **가치**: [FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) (First-In, First-Out) 큐만으로 구현할 수 있을 만큼 단순하고 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) 오버헤드가 작아, 처리 순서 보장과 구현 안정성이 중요할 때 기본 기준점이 된다.
> 3. **판단 포인트**: 작업 길이 편차가 크면 긴 작업 하나가 뒤의 짧은 작업을 묶어 두는 convoy effect를 일으켜 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)과 평균 대기 시간을 악화시키므로, 대화형 시스템의 주 스케줄러로는 부적합하다.

---

## Ⅰ. 개요 및 필요성

FCFS 스케줄링은 "먼저 온 작업부터 처리한다"는 가장 직관적인 스케줄링 규칙이다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 프로세스가 Ready Queue에 들어온 순서를 유지하고, CPU가 비면 큐의 맨 앞 프로세스를 꺼내 실행한다. 한 번 CPU를 받은 프로세스는 [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) 정책이므로 강제로 중단되지 않고, 종료 또는 I/O 요청 때만 다음 프로세스에게 자리를 넘긴다.

이 방식이 등장한 배경은 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) 시스템이다. 당시에는 빠른 화면 반응보다 "작업을 순서대로 안정적으로 돌리는 것"이 중요했고, 스케줄러가 너무 복잡하면 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 자체 오버헤드가 커졌다. FCFS는 구현이 단순하고, 적어도 큐에 들어온 프로세스가 순서 때문에 굶어 죽는 일은 적다는 점에서 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 운영 환경에 잘 맞았다.

아래 그림은 FCFS의 기본 실행 흐름을 보여준다.

```text
+--------------------------------------------------------------------+
| FCFS ready queue                                                  |
+--------------------------------------------------------------------+
| arrival -> [ P1 ][ P2 ][ P3 ] -> CPU                             |
| running process keeps CPU until exit or I/O wait                 |
| next dispatch always removes queue head                          |
+--------------------------------------------------------------------+
```

이 구조의 장점은 분명하다. 우선순위 계산도, 예상 burst 길이 추정도 필요 없다. 반면 단점도 분명하다. 앞에 선 작업이 오래 걸리면 뒤에 온 짧은 작업들은 아무리 빨리 끝날 수 있어도 그냥 기다려야 한다. 즉 FCFS는 공정한 순서와 나쁜 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 동시에 가질 수 있다.

- **📢 섹션 요약 비유**: FCFS는 식당에서 먼저 주문한 손님부터 끝까지 요리해 주는 방식과 같아서 순서는 공정하지만, 앞손님 주문이 너무 크면 뒤손님은 오래 굶게 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

FCFS의 핵심은 Ready Queue의 선입선출 보존이다. 새 프로세스는 큐 뒤에 붙고, CPU가 비면 맨 앞 프로세스가 dispatch된다. [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)이므로 첫 실행 시점이 곧 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)의 기준이 되고, 한 번 실행되면 종료 또는 차단 시점까지 CPU burst를 모두 소비한다.

아래 예시는 FCFS가 평균 대기 시간을 어떻게 결정하는지 보여 준다.

```text
+--------------------------------------------------------------------+
| Example: P1=10ms, P2=3ms, P3=2ms, all arrive at t=0              |
+--------------------------------------------------------------------+
| 0            10        13      15                                |
| |---- P1 ----|-- P2 ---|-- P3 -|                                 |
| waiting  : P1=0,  P2=10, P3=13                                   |
| response : P1=0,  P2=10, P3=13                                   |
| turnaround: P1=10, P2=13, P3=15                                  |
+--------------------------------------------------------------------+
```

위 예시에서 평균 대기 시간은 `(0 + 10 + 13) / 3 = 7.67ms`다. 중요한 점은 P2와 P3가 매우 짧은 작업이어도, 긴 P1 뒤에 서 있다는 이유만으로 응답과 대기가 모두 늦어진다는 것이다. [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/) FCFS에서는 첫 프로세스의 burst 길이가 뒤 프로세스들의 체감 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 거의 결정한다.

이 구조는 특히 CPU 바운드 프로세스와 I/O 바운드 프로세스가 섞일 때 convoy effect를 만든다. 긴 CPU 작업이 먼저 CPU를 오래 점유하면, 짧은 I/O 중심 작업들은 Ready Queue에서 대기하다가 늦게 실행된다. 그 결과 I/O 장치는 놀고, 나중에 짧은 작업들이 한꺼번에 몰리면 반대로 CPU가 비는 식으로 자원 이용이 들쭉날쭉해진다.

- **📢 섹션 요약 비유**: 트럭 한 대가 1차선 도로를 오래 막고 있으면, 뒤에 있는 오토바이들이 금방 빠져나갈 수 있어도 줄 전체가 트럭 속도로 움직이는 것과 같다.

---

## Ⅲ. 비교 및 연결

FCFS를 제대로 보려면 다른 스케줄링 정책과 비교해야 한다. FCFS는 도착 순서를 존중하고 오버헤드가 낮지만, 작업 길이를 고려하지 않기 때문에 평균 대기 시간과 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)에서 손해를 보기 쉽다. 반면 [SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/) ([Shortest Job First](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/))는 평균 대기 시간을 줄이는 데 강하고, [RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/) (Round Robin)은 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)을 개선하는 데 유리하다.

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 장점 | 약점 | 잘 맞는 환경 |
| :--- | :--- | :--- | :--- |
| FCFS | 구현 단순, 순서 보장, 오버헤드 작음 | [convoy effect](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/), 느린 응답 | 배치성·유사 크기 작업 |
| [SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/) | 평균 대기 시간 최소화에 유리 | burst 예측 필요, [starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/) 위험 | 작업 길이 예측 가능한 환경 |
| [RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/) | 첫 반응 빠름, 대화형에 유리 | [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 오버헤드 증가 | 시분할, 인터랙티브 환경 |

FCFS는 세 가지 시간 지표와도 직접 연결된다. [비선점](/knowledge-base/studynote/02_operating_system/05_deadlock/285_no_preemption/)이므로 단일 CPU burst만 있다면 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)과 대기 시간이 거의 같은 형태로 움직인다. 따라서 FCFS가 길이가 긴 작업에 약하다는 말은, 결국 뒤에 있는 짧은 작업의 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)과 대기 시간을 함께 악화시킨다는 뜻이다. 반대로 RR은 작은 time quantum으로 첫 응답을 앞당기지만, 반환 시간과 오버헤드가 함께 나빠질 수 있다.

또한 FCFS는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 CPU 스케줄러에서만 쓰이는 개념이 아니다. 프린터 스풀러, 단순 작업 큐, 일부 메시지 처리 파이프라인처럼 "입력 순서 보존"이 중요한 시스템에서는 여전히 자연스러운 기본 전략이다. 다만 이때도 작업 크기 편차가 크면 같은 문제가 반복되므로, FIFO와 FCFS는 늘 workload 분포와 함께 봐야 한다.

- **📢 섹션 요약 비유**: FCFS, [SJF](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/175_sjf_scheduling/), RR의 차이는 은행 창구에서 먼저 온 사람을 끝까지 처리할지, 짧은 용무부터 빨리 끝낼지, 잠깐씩 돌아가며 응대할지의 차이와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 FCFS를 채택할지 말지는 "작업 시간이 얼마나 들쭉날쭉한가"로 먼저 판단하는 것이 좋다. 모든 작업이 짧고 비슷하다면 FCFS는 단순하고 안정적이다. 그러나 1ms 작업과 1초 작업이 같은 큐로 들어오면, FCFS는 긴 작업을 기준으로 전체 체감 품질을 떨어뜨린다.

```text
+--------------------------------------------------------------------+
| When is FCFS acceptable?                                          |
+--------------------------------------------------------------------+
| response time critical?                                           |
|   +- yes -> choose preemptive policy                              |
|   +- no                                                           |
|       |                                                           |
|       v                                                           |
| job sizes similar and bounded?                                    |
|   +- yes -> FCFS/FIFO reasonable                                  |
|   +- no  -> convoy risk; add RR, priority, or class split         |
+--------------------------------------------------------------------+
```

### 실무 판단 기준

1. <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/">배치 처리</a></strong>: 야간 정산, 단순 배치 잡처럼 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)보다 순서와 구현 안정성이 중요한 경우 FCFS가 적합하다.
2. **작업 크기 분포**: 작업 길이 편차가 크면 separate [queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/), priority, [RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/) 같은 보완이 필요하다.
3. <strong>사용자 체감 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong>: 터미널, 웹 서버, 그래픽 사용자 인터페이스 (Graphical User Interface, GUI)처럼 즉각 반응이 중요하면 FCFS는 피하는 편이 맞다.
4. **애플리케이션 큐**: 이벤트 루프나 메시지 소비기도 [FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 자체는 많이 쓰지만, long task를 차단하지 않도록 [timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/)·분할 실행·backpressure를 함께 둬야 한다.

### 자주 나오는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 요청을 하나의 FCFS 큐에 넣고 heavy request와 light request를 구분하지 않는 것
- "순서가 공정하다"는 이유만으로 사용자 [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 악화를 무시하는 것
- FCFS 문제를 CPU만의 문제로 보고, I/O 장치 유휴와 convoy effect를 함께 보지 않는 것

기술사 답안에서는 FCFS를 "가장 단순한 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)"이라고만 쓰면 약하다. <strong>왜 단순성이 장점이 되는지, 그리고 왜 그 대가가 응답성 악화와 convoy effect로 나타나는지</strong>를 함께 설명해야 한다.

- **📢 섹션 요약 비유**: FCFS를 실무에 쓰는 일은 우편물을 접수 순서대로 처리하는 것과 같아서 물건 크기가 비슷하면 좋지만, 냉장고 한 대가 섞이면 작은 봉투들도 같이 늦어진다.

---

## Ⅴ. 기대효과 및 결론

FCFS의 가장 큰 효과는 예측 가능한 순서와 낮은 관리 비용이다. 큐 규칙이 단순하므로 구현과 디버깅이 쉬우며, [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)도 적어 기본 오버헤드가 작다. 또한 작업이 큐에 들어온 뒤 뒤로 밀려 무한정 굶는 상황은 상대적으로 적어, 기본 [baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 정책으로 의미가 있다.

하지만 이 장점은 workload가 균질할 때만 빛난다. 실제 범용 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 짧은 interactive [task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/), 긴 CPU [task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/), 잦은 I/O task가 섞여 있기 때문에 FCFS만으로는 좋은 응답성을 만들기 어렵다. 그래서 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 FCFS를 단독 해답이 아니라, 더 복잡한 스케줄러를 이해하기 위한 출발점 혹은 일부 큐 계층의 기본 규칙으로 사용한다.

결론적으로 FCFS는 "가장 공정해 보이는 순서"와 "가장 좋은 사용자 체감"이 다를 수 있음을 보여 주는 고전적 사례다. 기억할 핵심은 <strong>순서를 지키는 단순성은 강력하지만, 작업 길이를 무시하는 순간 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 비용이 크게 돌아온다</strong>는 점이다.

- **📢 섹션 요약 비유**: FCFS는 줄 세우기 규칙으로는 아주 깔끔하지만, 놀이기구 앞에서 한 팀이 오래 타면 뒤 사람 모두가 같이 지루해지는 상황과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Ready Queue](/knowledge-base/studynote/02_operating_system/02_process_thread/088_ready_queue/) | FCFS가 직접 적용되는 [FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 대기 구조다. |
| [비선점형 스케줄링](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/167_non_preemptive_scheduling/) ([Non-preemptive Scheduling](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/167_non_preemptive_scheduling/)) | FCFS의 핵심 전제다. |
| [convoy effect](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/) | 긴 작업이 뒤의 짧은 작업들을 묶어 두는 대표 부작용이다. |
| 대기 시간 (Waiting Time) | FCFS [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가에서 가장 먼저 악화되는 지표다. |
| [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) ([Response Time](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)) | 대화형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 FCFS가 약한 이유를 설명한다. |
| [RR](/knowledge-base/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/) (Round Robin) | FCFS의 응답성 약점을 보완하는 대표 선점형 정책이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
process arrival
    |
    v
FIFO ready queue
    |
    v
head dispatch
    |
    +---------------> run until exit / I/O wait
    |
    +---------------> long burst first
                           |
                           v
                    convoy effect
```

이 흐름도는 FCFS의 장점인 단순한 head dispatch와, 그 바로 뒤에 붙는 구조적 약점인 convoy effect가 같은 규칙에서 동시에 나온다는 점을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. FCFS는 먼저 줄 선 친구부터 차례대로 놀이기구를 타게 하는 규칙이에요.
2. 그런데 앞 친구가 아주 오래 타면 뒤 친구들은 금방 끝날 수 있어도 계속 기다려야 해요.
3. 그래서 줄 세우기는 쉽지만, 모두를 빨리 만족시키는 방법은 아닐 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 173 / 800

<- **이전**: [172. 반환 시간 (Turnaround Time) / 대기 시간 (Waiting Time) / 응답 시간 (Response Time)](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/172_turnaround_waiting_response_time/)
**다음**: [174. 호위 효과 (Convoy Effect) - FCFS의 단점](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/174_convoy_effect/) ->

---
