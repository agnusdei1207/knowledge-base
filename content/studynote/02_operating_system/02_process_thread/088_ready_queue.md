+++
title = "88. 준비 큐 (Ready Queue)"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Ready [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) (준비 큐)는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 메모리 내에 존재하며, 실행에 필요한 모든 자원을 확보하고 오직 CPU (Central Processing Unit) 할당만을 기다리는 프로세스들의 대기열이다.
> 2. **가치**: [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 다음 실행 대상을 빠르고 효율적으로 선택할 수 있도록 [프로세스 제어 블록](/knowledge-base/studynote/02_operating_system/02_process_thread/090_pcb_tcb/)(PCB)의 포인터들을 체계적으로 연결해 둔다.
> 3. **판단 포인트**: 큐를 단순한 [FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) ([First-In First-Out](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/))로 구성할지, 다단계나 우선순위 트리로 구성할지에 따라 전체 시스템의 응답성과 처리량이 결정되므로 워크로드 성격에 맞춰 정책을 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

Ready Queue는 멀티프로그래밍 환경에서 여러 프로세스가 CPU를 공유하기 위해 필수적인 핵심 자료구조다. 프로세스가 디스크에서 메모리로 적재되거나, `I/O (Input/Output)` 대기를 끝마쳤을 때 즉시 실행할 수 있는 상태가 되지만, CPU는 하나(또는 코어 수만큼)이므로 차례를 기다릴 대기 장소가 필요하다.

이 큐가 없다면 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 실행 가능한 프로세스를 찾기 위해 매번 전체 시스템을 훑어야 하므로 극심한 오버헤드가 발생한다. 따라서 스케줄링 대상을 한곳에 모아두고 빠르게 교체하기 위해 고안되었다.

- 📢 섹션 요약 비유: 요리사가 한 명뿐인 식당에서, 재료 손질을 다 끝내고 프라이팬에 올라가기만을 기다리는 요리들의 대기석과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Ready Queue는 내부에 실제 프로그램 코드가 아니라, 프로세스의 핵심 메타데이터를 담은 `PCB (Process Control Block)`들의 연결 리스트나 트리 형태로 구현된다.

| 요소 | 역할 | 동작 메커니즘 |
| :--- | :--- | :--- |
| Enqueue (진입) | 새 프로세스 추가 | 프로세스가 [New](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 상태나 Waiting 상태에서 Ready 상태로 전환될 때 삽입 |
| Dequeue (선택) | 실행 대상 추출 | CPU Scheduler가 정책에 따라 맨 앞, 또는 가장 적합한 PCB를 선택 |
| [Dispatcher](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/) ([디스패처](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/)) | [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) 실행 | [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)가 고른 프로세스로 [Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) Switch를 수행하여 Running 상태로 변경 |

```text
+-------------------------------------------------------------+
|          프로세스 상태 전이와 Ready Queue의 위치          |
+-------------------------------------------------------------+
|                 [CPU Scheduler]                             |
|                       v (선택)                              |
| [New] ---> +-(Head) Ready Queue (Tail)-+ ---> [Running]     |
|           | PCB_1 --> PCB_4 --> PCB_2   |       |           |
|           +---------------------------+       |           |
|                 ^                             v           |
|                 +------- [Waiting (I/O)] <-----+           |
+-------------------------------------------------------------+
```

CPU를 쓰던 프로세스가 타임 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)를 소진([인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 발생)하면 다시 Ready Queue의 꼬리(또는 적합한 [우선순위 큐](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/))로 되돌아가 대기하는 사이클이 반복된다.

- 📢 섹션 요약 비유: 롤러코스터 대기줄과 같다. 새 손님이나 화장실을 다녀온 손님이 줄을 서고, 차례가 오면 열차(CPU)를 탄 뒤, 더 타고 싶으면 다시 줄 끝으로 돌아간다.

---

## Ⅲ. 비교 및 연결

Ready Queue는 프로세스가 대기하는 다른 큐들과 명확히 다른 목적을 가진다.

| 비교 축 | Ready [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) (준비 큐) | Waiting [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) / Device [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) ([대기 큐](/knowledge-base/studynote/02_operating_system/02_process_thread/089_wait_queue/)) |
| :--- | :--- | :--- |
| 대기 대상 | 오직 CPU (프로세서 연산 주기) | I/O 완료, 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/)) 획득, 네트워크 응답 등 |
| 전환 조건 | [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)의 타임 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) 배분 | 외부 장치의 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)나 이벤트 발생 |
| 관리 주체 | 단일 CPU [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) | 각 디바이스 드라이버나 리소스 관리자 (복수 큐 존재) |

Ready Queue는 단일 큐가 아니라 현대 OS에서는 `MLFQ (Multi-Level Feedback Queue)`나 `CFS (Completely Fair Scheduler)`의 [Red-Black Tree](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/204_red_black_tree_cfs/) 구조 등 복합적인 자료구조로 진화하여, Waiting Queue의 단순한 대기 방식과 구분되는 정교한 스케줄링 기반 구조를 띤다.

- 📢 섹션 요약 비유: Ready Queue는 당장 무대에 오를 수 있는 주연 배우들의 대기실이고, Waiting Queue는 아직 분장이 덜 끝나서 무대에 오를 수 없는 분장실이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)나 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템 설계 시 대기열 모델은 중대한 판단 기준이 된다.

- 멀티코어 환경에서는 하나의 Global Ready Queue를 쓸 경우 [Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/) 경합(Contention)으로 병목이 발생하므로, 코어별로 Local Ready Queue를 분리(Per-CPU [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))하여 할당하는 아키텍처를 채택해야 한다.
- 코어 간 부하 불균형이 발생하면 `Load Balancing (부하 분산)` 기법 중 하나인 [Work Stealing](/knowledge-base/studynote/02_operating_system/04_synchronization/271_work_stealing/)(작업 훔치기)을 통해 바쁜 큐의 프로세스를 유휴 코어의 큐로 이동시켜야 한다.
- 실시간 처리(RTOS)가 필요한 도메인에서는 철저히 우선순위 기반의 다중 Ready Queue를 두어, 긴급 프로세스가 절대적인 새치기(Preemption) 권한을 갖도록 보장해야 한다.

- 📢 섹션 요약 비유: 계산대가 여러 개일 때 한 줄 서기(Global)를 할지, 계산대마다 따로 서게(Local) 할지 정하고, 줄이 너무 긴 곳의 손님을 빈 곳으로 유도하는 마트의 줄 관리와 같다.

---

## Ⅴ. 기대효과 및 결론

Ready Queue를 효율적으로 관리하면 CPU의 유휴 시간([Idle](/knowledge-base/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/) Time)이 최소화되고, 다수의 프로세스가 동시에 실행되는 것과 같은 반응성 높은 [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/) 환경이 완성된다.

그러나 큐의 크기가 너무 커지거나 탐색 비용이 높은 자료구조를 쓰면 오히려 스케줄링 오버헤드로 인해 시스템 처리량이 저하되는 한계가 존재한다. 결국 Ready Queue는 "스케줄링 정책이 실물 자료구조로 구현된 핵심 공간"으로 이해하고, 최적화에 집중해야 한다.

- 📢 섹션 요약 비유: 어떤 줄 서기 규칙을 만드느냐에 따라 식당의 회전율과 손님들의 만족도가 한 번에 결정되는 시스템의 심장부다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| PCB ([Process](/knowledge-base/studynote/12_it_management/05_security_compliance/943_process/) Control Block) | Ready Queue에 실제로 저장되어 이동하는 프로세스의 정보 덩어리 |
| CPU Scheduler | Ready Queue에서 다음 실행할 PCB를 고르는 [결정자](/knowledge-base/studynote/05_database/02_modeling_normalization/095_determinant_dependent/) |
| [Dispatcher](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/168_dispatcher/) | [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)의 결정에 따라 [문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)을 수행해 프로세스에 CPU를 넘겨주는 실행자 |
| [Context Switch](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/) ([문맥 교환](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) | Running 상태의 프로세스를 큐로 내리고, 큐의 맨 앞 프로세스를 올리는 과정 |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 큐 (FIFO 순서 대기)
    |
    v
우선순위 기반 다중 Ready Queue (우선순위 역전 문제 대두)
    |
    v
MLFQ (Multi-Level Feedback Queue - 상태에 따른 큐 간 이동)
    |
    v
멀티코어 환경 Per-CPU Ready Queue 및 Work Stealing
    |
    v
CFS (Completely Fair Scheduler - Red-Black Tree 기반 대기열)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 게임기(CPU)는 하나뿐인데 놀고 싶은 친구(프로세스)가 많을 때 서로 안 싸우게 줄을 세워야 해요.
2. Ready Queue는 숙제도 다 끝내고 당장 게임기를 켤 준비가 완벽히 끝난 친구들이 모인 대기 줄이에요.
3. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 선생님은 이 줄을 보고 가장 공평하고 빠른 순서대로 친구들에게 게임기를 넘겨준답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 88 / 800

<- **이전**: [87. 생성 (New) -> 준비 (Ready) -> 실행 (Running) -> 대기 (Waiting/Blocked) -> 종료 (Terminated)](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
**다음**: [89. 대기 큐 (Wait Queue / Device Queue)](/knowledge-base/studynote/02_operating_system/02_process_thread/089_wait_queue/) ->

---
