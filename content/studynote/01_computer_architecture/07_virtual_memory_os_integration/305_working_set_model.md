+++
title = "305. 워킹 셋 모델 (Working Set Model)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [워킹 셋 모델](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/) ([Working Set Model](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/))은 프로세스가 최근 일정 구간 동안 실제로 자주 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 집합을 기준으로 필요한 메모리 크기를 추정하는 방식이다.
> 2. **가치**: [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) ([Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), OS)는 이 집합을 물리 메모리인 램 (Random Access Memory, RAM)에 유지하려고 함으로써 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 폭증과 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))을 예방한다.
> 3. **판단 포인트**: 핵심은 프레임을 균등 분배하는 것이 아니라, 각 프로세스의 현재 지역성 (Locality)에 맞춰 충분한 프레임을 주고 부족하면 멀티프로그래밍 정도 ([Degree of Multiprogramming](/knowledge-base/studynote/02_operating_system/04_synchronization/258_degree_of_multiprogramming/), DoM) 자체를 낮추는 데 있다.

---

## Ⅰ. 개요 및 필요성

[워킹 셋 모델](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/)은 "프로세스가 지금 당장 부드럽게 실행되려면 어떤 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)들이 메모리에 있어야 하는가"를 정의하는 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 제어 모델이다. 프로그램은 전체 주소 공간을 고르게 쓰지 않고, 짧은 시간 동안 특정 코드와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 주변을 반복해서 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)하는 경향을 보인다. 이 성질을 [참조의 지역성](/knowledge-base/studynote/02_operating_system/04_synchronization/253_locality_of_reference/)이라고 하며, [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)은 그 지역성을 시간 창으로 잘라 가시화한 결과다.

이 개념이 필요한 이유는 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)가 단순히 "오래 안 쓴 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 내보내는 문제"로 끝나지 않기 때문이다. 어떤 프로세스에게 필요한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 묶음 전체가 램에 들어오지 못하면, 한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 읽을 때마다 다른 중요한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 밀어내게 된다. 그러면 CPU (Central Processing Unit)는 계산보다 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 입출력 (Input/Output, I/O) 대기 시간에 더 오래 묶이고, 시스템은 여러 프로세스를 돌리고도 실제 처리량은 오히려 떨어지는 역설에 빠진다.

아래 그림은 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)이 왜 "[페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 하나"가 아니라 "작업에 필요한 묶음"으로 이해되어야 하는지를 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│        최근 참조 구간으로 보는 워킹 셋: 필요한 책 한 묶음을 남긴다       │
├──────────────────────────────────────────────────────────────────────────┤
│ 시간 흐름 →                                                              │
│ ... 4  8  4  9  8  3  8  9  3  3  9  | 현재 t                           │
│                     <------ Δ (관찰 구간) ------>                        │
│                                                                          │
│ 최근 Δ 동안 등장한 페이지 = {8, 9, 3}                                   │
│                                                                          │
│ 의미: 지금 이 프로세스는 페이지 8·9·3이 함께 있어야 계산 흐름이 끊기지 않음 │
└──────────────────────────────────────────────────────────────────────────┘
```

즉 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)은 "최근에 한 번이라도 쓴 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 목록"이 아니라, 현재 실행 국면을 지탱하는 최소한의 메모리 작업 공간이라는 의미를 가진다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 이 크기를 무시한 채 프로세스를 과도하게 메모리에 올리면, 시스템은 겉으로는 멀티태스킹이지만 실제로는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 운반만 반복하는 상태가 된다.

- **📢 섹션 요약 비유**: 책상 위에 문제집 세 권을 동시에 펼쳐야 공부가 이어지는데, 책상 공간이 두 권 분량밖에 없으면 한 문제 풀 때마다 책을 가방에 넣었다 꺼내야 한다. [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)은 "지금 공부에 꼭 필요한 책 묶음"을 먼저 확보하자는 규칙이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[워킹 셋 모델](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/)의 중심 식은 `W(t, Δ)`다. 이는 시각 `t` 직전의 일정 구간 `Δ` 동안 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)된 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)들의 집합을 뜻한다. `|W(t, Δ)|`는 해당 시점에 프로세스가 원활히 실행되기 위해 필요한 프레임 수의 근사치가 된다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 이 값을 직접 계산하거나 근사하여 각 프로세스의 프레임 할당량을 조정한다.

### 동작 흐름

1. 프로세스의 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 이력을 추적한다.
2. 최근 `Δ` 구간에서 등장한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)으로 묶는다.
3. [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 크기보다 프레임이 적으면 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)가 급증할 위험 신호로 본다.
4. [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)이 충분히 올라와 있으면 해당 프로세스는 높은 적중률로 계속 실행된다.

| 요소 | 의미 | 설계 포인트 |
| :--- | :--- | :--- |
| `Δ` ([윈도우 크기](/knowledge-base/studynote/03_network/08_transport_layer/413_tcp_window_size_flow_control_16bit/)) | 최근성을 어디까지 볼지 정하는 기준 | 너무 작으면 과소추정, 너무 크면 과대추정 |
| `W(t, Δ)` | 최근 구간에서 실제 사용된 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 집합 | 현재 지역성을 반영하는 핵심 지표 |
| `|W(t, Δ)|` | 필요한 프레임 수의 근사치 | 프로세스별 메모리 수요 판단 |
| `Σ|W_i|` | [전체 프로세스](/knowledge-base/studynote/02_operating_system/06_memory_management/337_standard_vs_paging_swapping/) [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)의 총합 | 시스템 과부하와 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 가능성 판단 |

아래 그림은 개별 프로세스의 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 계산과 시스템 수준 판단이 어떻게 연결되는지를 보여준다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                 워킹 셋 모델의 시스템 제어 루프                          │
├──────────────────────────────────────────────────────────────────────────┤
│ 프로세스 A 참조열 ─┐                                                     │
│ 프로세스 B 참조열 ─┼─▶ 최근 Δ 구간 분석 ─▶ 각 W(t, Δ) 계산 ─┐           │
│ 프로세스 C 참조열 ─┘                                       │           │
│                                                            ▼           │
│                                            Σ|W_i| 와 가용 프레임 비교    │
│                                                            │           │
│                           ┌────────────────────────────────┴─────────┐ │
│                           │                                          │ │
│                           ▼                                          ▼ │
│                 충분함: 실행 유지, 지역성 보존         부족함: 프레임 재분배,
│                                                  일부 프로세스 보류/Swap-out │
└──────────────────────────────────────────────────────────────────────────┘
```

여기서 가장 어려운 변수는 `Δ`다. `Δ`가 너무 작으면 아직 필요한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)에서 빠져 실제 필요 메모리를 낮게 잡는다. 반대로 `Δ`가 너무 크면 이미 지나간 작업 단계의 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)까지 포함되어 불필요한 프레임을 붙잡게 된다. 그래서 순수 이론형 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)은 정확하지만 비용이 높고, 실제 시스템은 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)와 주기적 샘플링으로 이를 근사하는 경우가 많다.

- **📢 섹션 요약 비유**: 스포츠 경기에서 선수에게 필요한 장비를 챙길 때, 방금까지 계속 쓴 장비 묶음을 기준으로 가방을 꾸리는 것과 같다. 기준 시간이 너무 짧으면 꼭 필요한 장비를 빼먹고, 너무 길면 이미 안 쓰는 장비까지 들고 다니느라 무거워진다.

---

## Ⅲ. 비교 및 연결

[워킹 셋 모델](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/)을 제대로 이해하려면 "예방형 메모리 제어"라는 관점에서 다른 방식과 경계를 봐야 한다. 특히 [페이지 부재 빈도](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/) ([Page Fault Frequency](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/), [PFF](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/))는 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)과 자주 비교되는 대표 기법이다.

| 항목 | [워킹 셋 모델](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/) | [PFF](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) ([Page Fault Frequency](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/)) |
| :--- | :--- | :--- |
| 관찰 기준 | 최근 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 패턴 자체 | [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 발생률 |
| 제어 시점 | [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 이전의 예방 중심 | 폴트 증가 후의 피드백 중심 |
| 장점 | 지역성을 직접 반영 | 구현이 단순하고 실용적 |
| 약점 | 추적 비용이 큼 | 반응이 한 박자 늦을 수 있음 |
| 적합한 관점 | 이론적 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/), 정밀 제어 | 운영 현실, 근사 제어 |

또한 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)은 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/), [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/), 선반입 ([Prepaging](/knowledge-base/studynote/02_operating_system/07_virtual_memory/385_prepaging/))과도 연결된다. [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)을 지탱하지 못했을 때 나타나는 붕괴 현상이고, [페이지 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/401_page_replacement_algorithms/)은 주어진 프레임 안에서 어떤 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 남길지 결정하는 미시적 기법이다. 선반입은 문맥 전환 후 다시 실행될 프로세스의 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 일부를 미리 가져와 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)를 줄이는 확장 전략이다.

중요한 점은 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)이 단순한 교체 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 아니라는 사실이다. 이는 "프로세스를 얼마나 동시에 메모리에 유지할 것인가"까지 건드리는 상위 제어 모델이다. 따라서 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 하나의 퇴출 기준보다, 시스템 전체가 감당 가능한 동시 실행 규모를 정하는 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)에 가깝다.

- **📢 섹션 요약 비유**: [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)은 감기 걸리기 전에 체온과 컨디션을 보고 쉬게 하는 예방 진료이고, PFF는 열이 오른 뒤 해열제를 주는 치료에 가깝다. 둘 다 필요하지만, 몸이 망가지기 전에 흐름을 읽는 쪽이 더 근본적인 제어다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 순수한 [워킹 셋 모델](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/)을 그대로 구현하기보다, 그 철학을 근사 기법과 운영 정책에 녹여 쓴다. 핵심 질문은 "이 프로세스가 지금 필요한 메모리를 감당할 수 있는가"이며, 감당하지 못하면 프레임을 더 주거나 아예 동시 실행 수를 줄여야 한다.

### 판단이 필요한 대표 상황

1. **메모리 압박이 높은 서버**
   - [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/), JVM (Java [Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)) 기반 애플리케이션, 분석 배치가 동시에 돌아가면 각 프로세스의 활성 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 집합이 갑자기 커질 수 있다.
   - 이때 CPU 사용률이 낮은데 디스크 스왑 I/O만 치솟는다면, 단순 CPU 병목이 아니라 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 붕괴 가능성을 먼저 의심해야 한다.

2. **[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)·[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 환경**
   - 여러 가상 머신이나 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 한 호스트의 메모리를 공유할 때, 각 워크로드의 활성 구간이 겹치면 총 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 합이 물리 메모리를 넘어선다.
   - 이 경우 단순 평균 사용량보다 피크 시점의 동시 활성 집합이 더 중요하다.

### 기술사 답안형 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- 최근 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 패턴이 급격히 바뀌는 배치성 작업인가, 안정적인 서비스형 작업인가?
- [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)을 정밀 계산할 비용을 감당할 수 있는가, 아니면 PFF나 [Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/) 계열 근사법이 더 적절한가?
- `Σ|W_i| > 가용 프레임` 상황에서 프레임 재할당으로 해결할지, 일부 프로세스를 보류시켜 DoM을 낮출지 정책이 준비되어 있는가?
- [스왑 공간](/knowledge-base/studynote/02_operating_system/07_virtual_memory/390_swap_space/) 증가를 해결책으로 착각하고 있지 않은가? 스왑은 시간을 벌 수는 있어도 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 붕괴 자체를 치료하지는 못한다.

결론적으로 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 관점은 "메모리가 부족한데도 프로세스를 더 넣어보자"라는 유혹을 막아준다. 프레임이 충분하지 않다면 일부 작업을 늦추는 결정이 전체 처리량과 응답시간을 오히려 더 좋게 만든다.

- **📢 섹션 요약 비유**: 엘리베이터 정원이 10명인데 15명을 억지로 태우면 모두가 늦어지고 위험해진다. 차라리 5명을 다음 차로 보내는 판단이 전체 운행을 더 빠르고 안전하게 만든다.

---

## Ⅴ. 기대효과 및 결론

[워킹 셋 모델](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/)의 가장 큰 효과는 메모리 관리의 기준을 "균등 분배"에서 "실제 필요량 보장"으로 바꾼다는 점이다. 이 관점을 적용하면 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)율, 디스크 스왑, 응답시간 악화가 단순 현상이 아니라 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 미충족의 결과로 읽히기 시작한다. 즉 문제를 증상 수준이 아니라 구조 수준에서 해석하게 만든다.

물론 한계도 분명하다. 정확한 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)을 실시간으로 계산하는 비용은 작지 않고, `Δ` 선택에 따라 결과가 흔들릴 수 있다. 그래서 현대 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)의 철학을 유지하되, [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 기반 근사, 적응형 프레임 재할당, [PFF](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) 같은 보조 기법과 함께 사용한다.

결국 [워킹 셋 모델](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/)은 "프로세스가 살아 움직이는 현재 작업 맥락을 메모리에 보존하라"는 원칙으로 기억하면 된다. [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)를 잘하는 것만으로는 충분하지 않고, 시스템 전체가 동시에 품을 수 있는 작업량까지 함께 조절해야 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 없는 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)가 성립한다.

- **📢 섹션 요약 비유**: 좋은 도서관 운영은 모든 학생에게 똑같은 책상 크기를 주는 것이 아니라, 지금 프로젝트를 수행하는 데 필요한 자료를 안정적으로 펼칠 공간을 보장하는 일과 같다. [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)은 그 "공부가 실제로 굴러가게 하는 최소 작업 공간"을 지키는 생각법이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [참조의 지역성](/knowledge-base/studynote/02_operating_system/04_synchronization/253_locality_of_reference/) (Locality) | [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)이 의미를 가지게 만드는 전제이며, 최근 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 패턴이 미래 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)를 예측하게 해준다. |
| [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)) | [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)을 유지하지 못할 때 나타나는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 붕괴 현상이다. |
| [페이지 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/401_page_replacement_algorithms/) ([Page Replacement Algorithm](/knowledge-base/studynote/02_operating_system/07_virtual_memory/395_page_replacement_algorithm/)) | 제한된 프레임 안에서 어떤 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 남길지 결정하는 하위 기법이다. |
| [PFF](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) ([Page Fault Frequency](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/)) | [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 철학을 더 단순한 피드백 제어로 근사하는 운영 기법이다. |
| 선반입 ([Prepaging](/knowledge-base/studynote/02_operating_system/07_virtual_memory/385_prepaging/)) | 재실행 시 예상 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 일부를 미리 적재해 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 폴트를 줄이는 확장 전략이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
참조의 지역성 (Locality)
        │
        ▼
가상 메모리 (Virtual Memory) · 페이지 교체
        │
        ▼
워킹 셋 모델 (Working Set Model)
        │
        ├──▶ 스래싱 제어 · DoM 조절
        │
        └──▶ PFF (Page Fault Frequency) · 근사형 운영 정책
```

이 흐름은 "지역성 이해 → [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 관리 → [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 기반 수요 추정 → 시스템 수준 제어"로 확장되는 맥락을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터는 공부할 때 책상 위에 자주 보는 책들만 먼저 꺼내 놓고 싶어 해요.
2. 그 책들이 다 올라가 있으면 공부가 술술 되지만, 한 권 볼 때마다 다른 책을 치워야 하면 시간만 낭비해요.
3. [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)은 "지금 꼭 필요한 책 묶음은 책상 위에 남겨 두자"라고 정하는 약속이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 305 / 803

← **이전**: [304. 스래싱 (Thrashing)](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/304_thrashing/)
**다음**: [306. PFF (Page Fault Frequency)](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) →

---
