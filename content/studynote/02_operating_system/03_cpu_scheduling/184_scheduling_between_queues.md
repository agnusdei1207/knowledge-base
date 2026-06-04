---
title: "184. 큐 간 스케줄링 (고정 우선순위 vs 시간 할당)"
date: "2026-05-06"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 큐 간 스케줄링은 다단계 큐 (Multilevel [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)) 환경에서 여러 [준비 큐](/studynote/02_operating_system/02_process_thread/088_ready_queue/) 가운데 **어느 큐 자체가 먼저 CPU를 받을지** 결정하는 상위 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이다.
> 2. **가치**: 큐 내부의 [RR](/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/) (Round Robin)·[FCFS](/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) (First Come, First Served) 같은 규칙과 분리해, 시스템이 응답성 우선인지 공정성 우선인지를 큐 단위로 설계할 수 있게 한다.
> 3. **판단 포인트**: 고정 우선순위는 최상위 큐의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 강하게 보장하지만 [기아 상태](/studynote/02_operating_system/05_deadlock/314_starvation_prevention/) ([Starvation](/studynote/02_operating_system/05_deadlock/314_starvation_prevention/))를 만들 수 있고, 시간 할당은 최소 지분을 보장하지만 절대적 즉시성은 약해진다.

---

## Ⅰ. 개요 및 필요성

큐 간 스케줄링은 <strong>"큐 안에서 누구를 뽑을까?"보다 한 단계 위에서 "어느 큐의 문을 먼저 열까?"를 정하는 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a></strong>이다. 다단계 큐에서는 시스템 작업, 대화형 작업, 배치 작업이 서로 다른 큐에 배치되므로, 각 큐 내부 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)만 정해서는 충분하지 않다. 어떤 큐가 CPU를 먼저 받는지에 따라 전체 사용자 경험과 자원 배분 철학이 결정되기 때문이다.

이 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 필요한 이유는 작업군마다 요구가 다르기 때문이다. 인터랙티브 작업은 짧은 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) ([Response Time](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/))을 원하고, 배치 작업은 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) ([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))과 긴 실행 기회를 원하며, 실시간 작업은 마감 시한 준수가 더 중요할 수 있다. 큐를 나눠 놓고도 상위 선택 규칙이 없으면, 좋은 내부 스케줄러가 있어도 특정 큐 전체가 굶을 수 있다.

아래 그림은 큐 간 스케줄링이 큐 내부 스케줄링보다 상위 계층에서 동작한다는 점을 보여 준다.

```text
+-------------------------------------------------------------------+
| Two-level scheduling                                              |
+-------------------------------------------------------------------+
| Queue selector                                                    |
|   +--> Q0 : System      --> local scheduler --> process              |
|   +--> Q1 : Interactive --> local scheduler --> process              |
|   +--> Q2 : Batch       --> local scheduler --> process              |
|                                                                   |
| Global question : Which queue gets CPU now?                       |
| Local  question : Which process inside that queue runs next?      |
+-------------------------------------------------------------------+
```

이 구조를 이해하면 다단계 큐가 단순한 줄 나누기가 아니라, <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 등급을 CPU 시간에 반영하는 계층형 제어 모델</strong>이라는 사실이 보인다. 그래서 큐 간 스케줄링은 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)성이 가장 강하게 드러나는 지점이다.

- **📢 섹션 요약 비유**: 큐 간 스케줄링은 대형 병원에서 어느 진료과에 의사를 먼저 배치할지 정하는 운영 규칙과 같다. 각 과 안에서 환자를 부르는 방식보다, 어떤 과에 먼저 의사 시간을 줄지가 전체 대기 체감을 더 크게 바꾼다.

---

## Ⅱ. 아키텍처 및 핵심 원리

큐 간 스케줄링의 대표 방식은 **고정 우선순위 (Fixed-Priority)** 와 <strong>시간 할당 (Time <a href="/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/">Slice</a> between Queues)</strong> 이다. 고정 우선순위는 가장 높은 우선순위의 비어 있지 않은 큐를 항상 선택하며, 하위 큐가 실행 중이어도 상위 큐에 새 작업이 들어오면 즉시 선점될 수 있다. 반면 시간 할당 방식은 각 큐에 CPU 시간 비율이나 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)([weight](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/))를 미리 배분해, 상위 큐가 바쁘더라도 하위 큐가 최소 몫을 보장받게 한다.

| 방식 | 선택 규칙 | 장점 | 위험/한계 |
| :--- | :--- | :--- | :--- |
| 고정 우선순위 | 가장 높은 비어 있지 않은 큐 선택 | 최상위 큐 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 최소화 | 하위 큐 기아 가능 |
| 큐 간 시간 할당 | 큐별 시간 몫 또는 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 배분 | 최소 CPU 지분 보장 | 상위 큐 즉시성 약화 |

고정 우선순위는 구현이 단순하고, Real-Time [Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (RTOS)처럼 상위 작업의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 절대적으로 중요한 환경에 적합하다. 하지만 상위 큐 유입이 지속되면 하위 큐는 내부 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 RR이든 FCFS든 아예 호출조차 되지 않는다. 즉 하위 큐 문제는 큐 내부 규칙이 아니라 <strong>상위 선택 규칙</strong>에서 시작된다.

시간 할당 방식은 이 문제를 막기 위해 CPU 전체 시간을 큐 단위로 자른다. 예를 들어 Q0에 80%, Q1에 20%를 주면, 긴 관점에서 CPU 사용량은 그 비율을 향하도록 동작한다. 그 안에서 Q0는 자기 큐의 RR로 80%를 다시 나누고, Q1도 자기 몫 안에서 자체 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 적용한다.

```text
+-------------------------------------------------------------------+
| Queue scheduling timeline                                         |
+-------------------------------------------------------------------+
| Case 1: Fixed priority                                            |
| CPU : Q0 | Q0 | Q0 | Q0 | Q0 | Q0 | Q0 | ...                     |
|       Q1 and Q2 may wait forever if Q0 keeps receiving jobs       |
|                                                                   |
| Case 2: Queue time slicing (Q0 80%, Q1 20%)                       |
| CPU : Q0 | Q0 | Q0 | Q0 | Q1 | Q0 | Q0 | Q0 | Q0 | Q1            |
|       Lower queue latency grows, but starvation is prevented      |
+-------------------------------------------------------------------+
```

핵심은 큐 내부 타임 퀀텀 (Time [Quantum](/studynote/02_operating_system/11_exam_summary/690_round_robin_time_quantum/))과 큐 간 시간 할당을 혼동하지 않는 것이다. 전자는 **프로세스 간 분배**, 후자는 <strong>큐 간 분배</strong>다. 따라서 큐 간 스케줄링은 CPU 분배를 한 층 더 높은 수준에서 설계하는 메커니즘이다.

- **📢 섹션 요약 비유**: 고정 우선순위는 우선 고객 줄이 비는 동안에만 일반 줄을 받는 백화점 운영과 같고, 시간 할당은 매시간 우선 창구 시간을 많이 주되 일반 창구 시간도 반드시 남겨 두는 운영과 같다.

---

## Ⅲ. 비교 및 연결

큐 간 스케줄링을 정확히 이해하려면 <strong>고정 우선순위, 시간 할당, 그리고 <a href="/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/">MLFQ</a> (Multilevel Feedback <a href="/studynote/08_algorithm_stats/04_datastructure/058_queue/">Queue</a>)</strong> 의 경계를 함께 봐야 한다. 앞의 두 방식은 "큐 자체의 순서"를 정하는 정적 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이고, MLFQ는 여기에 <strong>큐 이동과 <a href="/studynote/02_operating_system/03_cpu_scheduling/182_aging/">Aging</a></strong> 개념을 더해 장기 기아를 줄이는 진화형이다. 즉 큐 간 스케줄링은 MLFQ를 이해하기 위한 바로 직전 단계다.

| 항목 | 고정 우선순위 | 큐 간 시간 할당 | [MLFQ](/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/) |
| :--- | :--- | :--- | :--- |
| 큐 선택 기준 | 우선순위 서열 | 비율/[가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) | 우선순위 + 동적 이동 |
| 하위 큐 보장 | 없음 | 있음 | 보정 가능 |
| 적응성 | 낮음 | 중간 | 높음 |
| 대표 장점 | 최상위 응답성 | 공정성·격리 | 응답성 + 적응성 |
| 대표 단점 | [starvation](/studynote/02_operating_system/05_deadlock/314_starvation_prevention/) | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 변동 | 복잡한 튜닝 |

또한 이 개념은 CPU 스케줄링 밖으로도 넓게 확장된다. 네트워크 장비의 [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) ([Quality of Service](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/))는 음성 큐와 일반 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 큐 사이에 우선권과 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 비율을 배분하고, 리눅스의 [cgroups](/studynote/02_operating_system/01_overview_architecture/062_cgroups/) ([Control Groups](/studynote/01_computer_architecture/15_advanced_topics/668_cgroups_hw_resource_allocation/))는 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 그룹 간 CPU share를 나누는 방식으로 유사한 원리를 쓴다. 즉 큐 간 스케줄링은 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 내부 알고리즘이면서 동시에 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 등급별 자원 배분 패턴</strong>이기도 하다.

따라서 시험 답안에서는 단순히 "상위 큐 먼저"라고 적는 것보다, <strong>고정 우선순위는 결정론적 보장에 강하고, 시간 할당은 최소 지분 보장에 강하며, MLFQ는 이 둘의 한계를 동적으로 보완한다</strong>고 연결해 주는 것이 좋다.

- **📢 섹션 요약 비유**: 고정 우선순위가 신호등 없는 전용차로라면, 시간 할당은 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 전용차로와 일반차로의 비율을 함께 운영하는 방식이고, MLFQ는 막히는 차선을 보며 차를 옮겨 주는 교통 관제에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "가장 중요한 큐가 빨라야 하는가"와 "모든 큐가 최소 몫을 가져야 하는가"를 먼저 구분해야 한다. 하드 실시간 제어, [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리, 응급 대응처럼 최상위 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 핵심이면 고정 우선순위가 타당할 수 있다. 반면 범용 서버, 데스크톱, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 플랫폼처럼 여러 사용자와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 공존하는 환경에서는 하위 큐의 생존권이 중요하므로 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) 기반 시간 할당이 더 현실적이다.

### 실무 판단 기준

1. **마감 시한을 절대 놓치면 안 되는 큐가 있는가?** 있으면 고정 우선순위가 필요할 수 있다.
2. **하위 큐의 starvation을 허용할 수 있는가?** 안 된다면 시간 할당, [aging](/studynote/02_operating_system/03_cpu_scheduling/182_aging/), MLFQ를 검토해야 한다.
3. **워크로드가 장기간 안정적인가?** 클래스가 자주 바뀌면 정적 큐 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)은 부적합해질 수 있다.
4. <strong>격리와 <a href="/studynote/12_it_management/02_itsm_itil/869_sla/">SLA</a> (<a href="/studynote/12_it_management/02_itsm_itil/869_sla/">Service Level Agreement</a>)가 중요한가?</strong> [멀티테넌트](/studynote/05_database/05_distributed_nosql_newsql/310_multi_tenant_database_architecture/) 환경이면 비율 기반 배분이 더 설명력이 크다.

### 대표 적용 예시

- **RTOS**: 제어 루프와 일반 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 처리를 분리하고, 제어 큐에 절대 우선권을 준다.
- **범용 OS**: 포그라운드와 배치 작업을 나누되, 하위 큐에 최소 CPU를 남겨 응답성과 공정성을 절충한다.
- <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a> 플랫폼</strong>: cgroups의 CPU shares처럼 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 그룹 간 비율을 강제해 noisy neighbor를 줄인다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 상위 큐 부하가 항상 높은데도 하위 큐 보호책 없이 고정 우선순위만 쓰는 설계
- 큐 간 share를 설정했지만, 큐 내부 quantum과 혼동해 실제 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 잘못 해석하는 운영
- [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중요도보다 단순히 "먼저 만든 큐" 순서대로 우선권을 주는 임시 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)

기술사 관점에서는 큐 간 스케줄링을 <strong>다단계 큐의 상위 제어 규칙</strong>으로 정의하고, 고정 우선순위와 시간 할당의 장단점, [starvation](/studynote/02_operating_system/05_deadlock/314_starvation_prevention/) 문제, 현대 시스템에서의 share·[isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) 적용까지 연결해야 답안 밀도가 높다.

- **📢 섹션 요약 비유**: 회사 예산을 배정할 때 연구소에는 빠른 의사결정권을 주고, 운영부서에도 최소 예산은 남겨야 회사가 돌아간다. 큐 간 스케줄링도 같은 자원 정치다.

---

## Ⅴ. 기대효과 및 결론

큐 간 스케줄링을 명확히 설계하면 다단계 큐가 단순 분류표가 아니라 <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>이 살아 있는 자원 배분 구조</strong>가 된다. 중요한 큐의 응답성을 보장할 수도 있고, 모든 큐에 최소 몫을 줘 장기 공정성을 확보할 수도 있다. 즉 큐를 나누는 것만으로는 충분하지 않고, 그 위에 어떤 배분 철학을 얹느냐가 시스템 성격을 완성한다.

다만 정적 큐 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)에는 한계도 있다. 실제 워크로드는 시간에 따라 성격이 바뀌고, 사용자 기대도 "즉시성"과 "공정성"을 동시에 요구한다. 그래서 현대 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 큐 간 시간 할당에 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/), [aging](/studynote/02_operating_system/03_cpu_scheduling/182_aging/), 피드백 이동을 더해 더 적응적인 스케줄러로 발전해 왔다.

정리하면 큐 간 스케줄링은 <strong>"다단계 큐에서 CPU의 큰 파이를 어떤 큐에 얼마만큼 줄지 정하는 상위 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>"</strong> 으로 기억하면 된다. 내부 스케줄링이 미시적 순서를 정한다면, 큐 간 스케줄링은 시스템 전체의 자원 철학을 정한다.

- **📢 섹션 요약 비유**: 같은 피자를 나누더라도 누구에게 먼저 줄지, 각 테이블에 몇 조각씩 보장할지가 다르면 식탁 분위기가 완전히 달라진다. 큐 간 스케줄링은 그 피자 배분 규칙이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 다단계 큐 (Multilevel [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)) | 큐 간 스케줄링이 동작하는 기본 구조다 |
| [RR](/studynote/03_network/16_data_center_cloud/834_load_balancing_algorithm_round_robin_least_connection/) (Round Robin) | 선택된 큐 내부에서 자주 쓰이는 프로세스 분배 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이다 |
| [FCFS](/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) (First Come, First Served) | 배치 큐 내부 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 자주 연결된다 |
| [Starvation](/studynote/02_operating_system/05_deadlock/314_starvation_prevention/) | 고정 [우선순위 큐](/studynote/08_algorithm_stats/04_datastructure/083_priority_queue/) 간 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)의 대표적 부작용이다 |
| [Aging](/studynote/02_operating_system/03_cpu_scheduling/182_aging/) | 오래 기다린 하위 큐를 보정하는 완화 전략이다 |
| [MLFQ](/studynote/02_operating_system/11_exam_summary/691_mlfq_multi_level_feedback_queue/) (Multilevel Feedback [Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/)) | 큐 이동을 허용해 정적 큐 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 한계를 보완한다 |
| [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) ([Quality of Service](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/)) | 네트워크 큐에 같은 원리를 적용한 사례다 |
| [cgroups](/studynote/02_operating_system/01_overview_architecture/062_cgroups/) ([Control Groups](/studynote/01_computer_architecture/15_advanced_topics/668_cgroups_hw_resource_allocation/)) | 현대 리눅스에서 그룹 간 CPU share를 구현하는 실무 예다 |

### 📈 관련 키워드 및 발전 흐름도

```text
Single ready queue limits
        |
        v
Multilevel queue classification
        |
        v
Scheduling between queues
        |
        +---------------> Fixed priority
        +---------------> Queue time slicing / weighted share
        +---------------> Starvation and aging concerns
        +---------------> MLFQ · QoS · cgroups isolation
```

이 흐름도는 단일 [준비 큐](/studynote/02_operating_system/02_process_thread/088_ready_queue/)의 한계를 해결하려고 다단계 큐가 등장했고, 다시 큐 간 배분 문제를 낳아 고정 우선순위·시간 할당·피드백형 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 발전하는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 여러 줄이 서 있을 때 선생님이 어느 줄에 먼저 장난감을 줄지 정하는 규칙이 바로 큐 간 스케줄링이에요.
2. 제일 급한 줄만 계속 먼저 주면 다른 줄은 너무 오래 기다릴 수 있어요.
3. 그래서 어떤 때는 급한 줄을 더 많이 챙기면서도, 다른 줄에도 꼭 조금씩 나눠 주는 방법을 쓰는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 184 / 800

<- **이전**: [183. 다단계 큐 스케줄링 (Multilevel Queue Scheduling)](/studynote/02_operating_system/03_cpu_scheduling/183_multilevel_queue_scheduling/)
**다음**: [185. 다단계 피드백 큐 스케줄링 (Multilevel Feedback Queue, MLFQ) - 프로세스의 큐 이동 허용](/studynote/02_operating_system/03_cpu_scheduling/185_mlfq_scheduling/) ->

---
