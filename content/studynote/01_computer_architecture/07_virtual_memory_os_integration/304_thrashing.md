+++
title = "304. 스래싱 (Thrashing)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))은 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 시스템이 계산보다 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)와 디스크 입출력에 더 많은 시간을 쓰게 되면서, CPU (Central Processing Unit) 이용률과 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 함께 무너지는 메모리 붕괴 상태다.
> 2. **가치**: 이 현상은 멀티프로그래밍 정도 ([Degree of Multiprogramming](/knowledge-base/studynote/02_operating_system/04_synchronization/258_degree_of_multiprogramming/))가 높다고 항상 좋은 것이 아니라, 각 프로세스의 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) ([Working Set](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/))을 담을 최소 물리 메모리를 먼저 보장해야 함을 보여준다.
> 3. **판단 포인트**: CPU 사용률이 낮다고 일을 더 넣는 순간 오히려 악화될 수 있으므로, [페이지 부재율](/knowledge-base/studynote/02_operating_system/07_virtual_memory/389_page_fault_rate_eat/)·스왑 트래픽·디스크 대기를 함께 보고 프로세스 수를 줄이거나 메모리 할당 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 바꿔야 한다.

---

## Ⅰ. 개요 및 필요성

[스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) ([Thrashing](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/))은 물리 메모리보다 동시에 유지해야 할 작업 집합이 커져, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) ([Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))가 유용한 연산보다 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 내보내고 다시 읽어 오는 일에 매달리는 상태를 말한다. 겉으로는 시스템이 살아 있지만, 실제로는 응답 시간이 급격히 늘고 디스크 입출력 (I/O, Input/Output)만 과도하게 바빠지는 것이 특징이다. 즉 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 "메모리가 부족하다"는 단순 경고가 아니라, 메모리 관리 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 전체가 현재 부하를 감당하지 못한다는 구조적 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)다.

이 개념이 중요한 이유는 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)가 원래 "적은 RAM (Random Access Memory)으로도 큰 프로그램을 돌리게 해 주는 기술"이기 때문이다. 하지만 이 장점은 [참조의 지역성](/knowledge-base/studynote/02_operating_system/04_synchronization/253_locality_of_reference/) (Locality)이 유지되고, 각 프로세스가 자주 쓰는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 묶음을 메모리에 붙잡아 둘 수 있을 때만 성립한다. 그 조건이 무너지면 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)는 확장 장치가 아니라 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 증폭기로 바뀌며, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([Solid State Drive](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))나 [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) (Hard Disk Drive)를 임시 RAM처럼 쓰려는 순간 시스템 전체가 급격히 느려진다.

아래 그림은 왜 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)이 "프로세스를 더 돌렸는데 CPU는 더 놀게 되는 역설"로 나타나는지 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│         스래싱의 역설: 프로세스 수를 늘리면 어느 지점 이후 CPU가 더 쉰다      │
├──────────────────────────────────────────────────────────────────────────────┤
│ CPU 이용률                                                                   │
│    ▲                                                                         │
│    │                        최적 구간                                         │
│    │                     ／￣￣￣￣＼                                         │
│    │                  ／              ＼                                      │
│    │               ／                  ＼                                     │
│    │            ／                       ＼____ 스래싱 구간                    │
│    │         ／                                 (Fault / Swap 폭증)           │
│    └────────────────────────────────────────────────────────────────────▶      │
│                     낮은 DoM                          높은 DoM                │
│                                                                              │
│ 핵심: 프로세스 증가 → 프로세스당 프레임 감소 → 페이지 부재 급증 → I/O 대기 증가 │
└──────────────────────────────────────────────────────────────────────────────┘
```

CPU 사용률이 떨어졌다고 해서 여유가 생긴 것은 아니다. 오히려 실행 가능한 프로세스가 부족할 만큼 모두가 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 기다리고 있다는 뜻일 수 있다. 따라서 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 단순한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하가 아니라, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 잘못된 피드백 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 읽기 시작하는 위험 구간으로 이해해야 한다.

- **📢 섹션 요약 비유**: [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 작은 주방에 요리사를 너무 많이 넣은 상황과 같다. 사람은 많아졌지만 요리할 자리가 없어 모두가 재료 창고만 오가니, 불은 켜져 있어도 음식은 오히려 더 늦게 나온다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)의 핵심 메커니즘은 "작업 집합 부족 → [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 연쇄 → 교체 비용 지배"다. 프로세스는 특정 시점마다 자주 쓰는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 묶음, 즉 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)을 가진다. 이 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)이 메모리에 유지되면 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) ([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/))는 드물고 계산이 연속적으로 진행된다. 반대로 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)을 담지 못하면 방금 가져온 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 곧바로 다시 내보내야 하므로, 동일한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)들이 짧은 시간 안에 반복 교체된다.

아래 그림은 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)이 발생할 때 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 내부에서 어떤 고리가 만들어지는지 압축한다.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                    스래싱의 폐쇄 루프: 계산이 I/O 대기로 치환됨              │
├──────────────────────────────────────────────────────────────────────────────┤
│ 프로세스 수 증가                                                              │
│        │                                                                     │
│        ▼                                                                     │
│ 프로세스당 가용 프레임 감소                                                   │
│        │                                                                     │
│        ▼                                                                     │
│ 워킹 셋 미충족                                                                │
│        │                                                                     │
│        ▼                                                                     │
│ 페이지 부재율 상승                                                            │
│        │                                                                     │
│        ▼                                                                     │
│ 희생 페이지 선택 + Swap In/Out 증가                                           │
│        │                                                                     │
│        ▼                                                                     │
│ 디스크 대기 증가, Ready Queue 축소                                            │
│        │                                                                     │
│        ▼                                                                     │
│ CPU 이용률 하락 ──▶ 잘못 해석 시 프로세스 추가 ──┐                            │
│                                                  └──────── 반복               │
└──────────────────────────────────────────────────────────────────────────────┘
```

이 과정에서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 급락하는 이유는 시간 단위가 완전히 다르기 때문이다. RAM 접근은 대략 수십~수백 ns (nanosecond) 수준이지만, [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 접근은 수십~수백 μs (microsecond), [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 기반 스왑은 ms (millisecond) 단위까지 커진다. 즉 한 번의 Major Fault가 수만 배 이상의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 만들 수 있고, 이런 부재가 연속되면 CPU는 계산 장치가 아니라 I/O 완료를 기다리는 대기 장치가 된다.

| 단계 | 정상 상태 | [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 상태 | 병목 포인트 |
| :--- | :--- | :--- | :--- |
| [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) | 대부분 메모리 히트 | 연속적인 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) | [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 미충족 |
| [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) | 가끔 발생 | 거의 매 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)마다 발생 가능 | Victim 선택·[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 비용 |
| CPU 상태 | 계산 지속 | 대기와 문맥 전환 증가 | [Ready Queue](/knowledge-base/studynote/02_operating_system/02_process_thread/088_ready_queue/) 고갈 |
| 저장장치 | 보조 역할 | [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 지배 요소 | Swap I/O 포화 |

결국 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 "메모리가 부족해서 느리다"보다 더 정확히 말해 "현재 메모리 배치가 지역성을 유지하지 못해, 저장장치 왕복이 주 작업이 된 상태"다. 그래서 해결 역시 단순 캐시 튜닝이 아니라, 프로세스 수·[프레임 할당](/knowledge-base/studynote/02_operating_system/07_virtual_memory/397_frame_allocation/)·[워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 보장이라는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 영역에서 이뤄져야 한다.

- **📢 섹션 요약 비유**: 책상 위에 꼭 필요한 책 다섯 권을 펴놔야 공부가 되는데, 책상에 두 권만 둘 수 있으면 학생은 문제를 푸는 대신 책을 넣었다 뺐다 하는 일만 하게 된다. [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 바로 그 "공부가 아니라 책 정리만 하는 상태"다.

---

## Ⅲ. 비교 및 연결

[스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)을 제대로 이해하려면 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 자체, [워킹 셋 모델](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/) ([Working Set Model](/knowledge-base/studynote/02_operating_system/07_virtual_memory/416_working_set_model/)), [페이지 부재 빈도](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/) ([PFF](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/), [Page Fault Frequency](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/))를 함께 봐야 한다. [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 요구 페이징에서 자연스러운 현상일 수 있지만, [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 그 빈도와 비용이 임계점을 넘어 시스템 전체 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 무너뜨리는 상태다. 즉 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)는 사건이고, [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 그 사건들이 누적돼 만들어진 붕괴 국면이다.

| 비교 항목 | 일반적인 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) | [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) | [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) / PFF의 역할 |
| :--- | :--- | :--- | :--- |
| 발생 빈도 | 간헐적, 예측 가능 | 지속적, 폭발적 | 상한선을 넘기기 전에 제어 |
| 시스템 반응 | 일시적 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 후 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/) | 전체 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 붕괴 | 프레임 추가·프로세스 축소 |
| CPU 이용률 | 비교적 유지 | 오히려 하락 가능 | 잘못된 증설 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 차단 |
| 저장장치 영향 | 보조적 읽기 | 스왑 I/O 포화 | 작업 집합 안정화 |

또한 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 데드락 ([Deadlock](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/))과도 구별해야 한다. 데드락은 잠금이나 [자원 선점](/knowledge-base/studynote/02_operating_system/05_deadlock/311_resource_preemption/) 순서가 꼬여 모두가 멈춘 상태이고, [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 모두가 움직이기는 하지만 유효한 진전이 거의 없는 상태다. 전자는 논리적 교착이고, 후자는 메모리 압박이 만든 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)적 교착이다. 이 차이를 구분해야 장애 원인을 락 설계에서 찾을지, 메모리 압박과 스왑 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)에서 찾을지 판단할 수 있다.

[스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 캐시 미스와도 계층이 다르다. 캐시 미스는 보통 하드웨어 내부에서 짧게 복구되지만, [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 개입하는 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)와 저장장치 접근이 반복되므로 비용 차원이 훨씬 크다. 따라서 "미스가 많다"는 표현만으로는 부족하며, 어느 계층의 미스인지가 설계 판단의 핵심이 된다.

- **📢 섹션 요약 비유**: [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)가 가끔 창고를 다녀오는 일이라면, [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 매 손님마다 창고를 뛰느라 매장 업무가 마비된 상태다. 데드락은 아예 문이 잠겨 못 움직이는 상황이고, [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 계속 뛰지만 정작 물건을 못 파는 상황에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 CPU 사용률 하락을 곧바로 "여유"로 해석하면 안 된다. 메모리 압박 환경에서는 CPU가 한가한 것이 아니라, 프로세스들이 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 기다리느라 실행 준비 상태에 들어오지 못할 수 있다. 이때 `vmstat`, `sar`, `iostat`, `top`, `/proc/meminfo` 같은 지표에서 스왑 인/아웃, major fault, `wa` (I/O wait), 메모리 압박을 함께 봐야 한다. CPU만 보면 증상이 아니라 결과만 보게 된다.

대표적인 판단 사례는 두 가지다. 첫째, 웹 애플리케이션 서버에서 워커 수를 늘렸더니 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 오르지 않고 응답 시간이 급증하며 스왑 트래픽이 늘어나는 경우다. 이때는 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/) 확대가 아니라 워커 축소, 캐시 크기 조정, RAM 증설이 우선이다. 둘째, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석 노드에서 대규모 조인이나 무작위 접근이 많은 작업을 동시에 여러 개 돌릴 때다. 이 경우 작업당 메모리 상한을 두지 않으면 각 작업이 서로의 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)을 밀어내며 전체 클러스터가 느려질 수 있다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. CPU 사용률이 낮을 때 `iowait`와 swap in/out도 함께 확인했는가?
2. [페이지 부재 빈도](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/) 증가가 일시적 시작 구간인지, 지속적인 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 붕괴인지 구분했는가?
3. 멀티프로그래밍 정도를 낮추거나 일부 프로세스를 suspend 했을 때 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 오히려 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/)되는가?
4. [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)·가상머신 환경이라면 메모리 limit이 실제 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)보다 작게 잡혀 있지 않은가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- CPU가 놀아 보인다는 이유만으로 프로세스 수를 더 늘리는 것
- 스왑이 있으니 메모리 부족을 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 알아서 흡수할 것이라 가정하는 것
- [페이지 부재율](/knowledge-base/studynote/02_operating_system/07_virtual_memory/389_page_fault_rate_eat/)만 보고, 저장장치 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 작업 특성의 지역성 붕괴를 함께 보지 않는 것

기술사 답안 관점에서는 "[스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)가 많다는 현상이 아니라, 시스템의 유효 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)이 메모리 교체 비용에 잠식된 상태"라고 정리하면 좋다. 대응은 프레임 추가, [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) 보장, [PFF](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) 기반 제어, 프로세스 수 감소, 메모리 증설 순으로 연결해서 설명하면 논리가 선명해진다.

- **📢 섹션 요약 비유**: 매장이 한산해 보여 직원을 더 부르는 것이 항상 정답은 아니다. 창고 통로가 막혀 모두가 박스만 들고 서 있다면, 사람을 더 넣는 대신 통로를 비우고 재고를 줄여야 장사가 다시 돌아간다.

---

## Ⅴ. 기대효과 및 결론

[스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)을 정확히 이해하면 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 메모리 관리 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 단순 용량 관점이 아니라 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 안정성 관점에서 볼 수 있다. [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)을 유지할 만큼만 [동시성](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/014_concurrency/)을 허용하면 CPU는 연산에 집중하고, 저장장치는 보조 계층으로 남으며, 응답 시간의 변동폭도 크게 줄어든다. 즉 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 제어는 평균 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)뿐 아니라 최악 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간을 다루는 안정성 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다.

물론 한계도 있다. 모든 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 문제를 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)만으로 해결할 수는 없으며, 작업 자체가 메모리 집약적이거나 지역성이 나쁘면 결국 더 큰 물리 메모리, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조 개선, 접근 패턴 재설계가 필요하다. 또한 SSD가 빨라졌다고 해도 RAM을 대체할 수준은 아니므로, "빠른 저장장치가 있으니 스왑 의존을 감수해도 된다"는 판단은 여전히 위험하다.

결국 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)의 실패가 아니라, [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)를 현실 제약 없이 쓸 수 있다고 착각했을 때 나타나는 경계 조건이다. 이 개념은 "CPU가 놀면 일을 더 시켜도 된다"가 아니라, "시스템이 감당할 작업 집합을 먼저 맞춰야 한다"는 관점으로 기억하는 것이 가장 정확하다.

- **📢 섹션 요약 비유**: 좋은 지휘자는 연주자가 숨이 차는데 템포만 더 올리지 않는다. 먼저 악단이 지금 악보를 소화할 수 있는지 보고, 필요하면 인원과 박자를 조정해 전체 합주를 살린다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/) ([Working Set](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)) | 프로세스가 당장 원활히 실행되기 위해 메모리에 유지해야 할 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 묶음 |
| [페이지 부재](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) ([Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/)) | [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)을 구성하는 직접 사건이며, 과도해지면 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 붕괴의 전조가 됨 |
| [PFF](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/306_pff/) ([Page Fault Frequency](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/)) | [페이지 부재 빈도](/knowledge-base/studynote/02_operating_system/04_synchronization/266_page_fault_frequency/)를 기준으로 프레임 수를 조정해 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)을 제어하는 실무형 기법 |
| 멀티프로그래밍 정도 ([Degree of Multiprogramming](/knowledge-base/studynote/02_operating_system/04_synchronization/258_degree_of_multiprogramming/)) | 동시에 메모리에 올려 두는 프로세스 수로, 과도하면 [워킹 셋](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/)이 깨짐 |
| [참조의 지역성](/knowledge-base/studynote/02_operating_system/04_synchronization/253_locality_of_reference/) (Locality) | 최근 사용한 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 다시 쓰인다는 성질로, [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 방지의 이론적 전제 |

### 📈 관련 키워드 및 발전 흐름도

```text
가상 메모리 (Virtual Memory)
    │
    ▼
요구 페이징 (Demand Paging)
    │
    ▼
페이지 부재 (Page Fault)
    │
    ▼
페이지 교체 알고리즘 (Page Replacement)
    │
    ├─▶ 워킹 셋 모델 (Working Set Model)
    │
    ├─▶ PFF (Page Fault Frequency)
    │
    ▼
스래싱 (Thrashing) 제어와 DoM 최적화
```

이 흐름은 "가상 주소 제공 → 필요 시 적재 → 부재 발생 → 교체 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 선택 → 작업 집합 제어"로 이어지는 메모리 관리의 발전 축을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)은 책상이 너무 좁아서 숙제보다 책을 가방에서 꺼냈다 넣는 데 더 오래 걸리는 상태예요.
2. 친구를 더 많이 앉힌다고 공부가 빨라지는 게 아니라, 각자 필요한 책을 펼칠 자리부터 있어야 해요.
3. 그래서 컴퓨터는 너무 붐비면 친구 수를 줄이거나 책상을 넓혀서, 다시 진짜 공부를 하게 만들어야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 304 / 803

← **이전**: [303. NUR (Not Used Recently)](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/303_nur/)
**다음**: [305. 워킹 셋 모델 (Working Set Model)](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/305_working_set_model/) →

---
