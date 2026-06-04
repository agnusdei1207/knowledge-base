---
title: "314. 인터럽트 구동 I/O (Interrupt-driven I/O)"
date: "2026-03-26"
tags:
  - "studynote-computer-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구동 I/O ([Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)-driven I/O)는 CPU (Central Processing Unit)가 장치를 계속 감시하지 않고, 장치가 준비 완료 시점에만 CPU를 깨우는 방식이다.
> 2. **가치**: 이 방식은 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) ([Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/))의 [바쁜 대기](/studynote/02_operating_system/04_synchronization/227_busy_waiting/) ([Busy Waiting](/studynote/02_operating_system/04_synchronization/227_busy_waiting/))를 줄여 CPU 시간을 계산, 스케줄링, 다른 장치 처리에 재투입하게 만든다.
> 3. **판단 포인트**: [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 "항상 최고 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)"이 아니라, 이벤트 빈도와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 크기에 따라 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)·[DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/))와 역할을 나눌 때 가장 효율적이다.

---

## Ⅰ. 개요 및 필요성

[인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구동 I/O는 입력/출력 장치가 작업 완료, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 도착, 오류 발생 같은 사건을 스스로 알리고 CPU가 그때만 개입하는 I/O 제어 방식이다. 핵심은 CPU가 시간을 기준으로 장치를 묻는 것이 아니라, 장치가 사건을 기준으로 CPU를 호출한다는 점이다. 그래서 이 개념은 단순한 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 기술이 아니라, CPU 시간을 희소 자원으로 보는 컴퓨터 구조의 관점 전환이다.

[폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) 방식에서는 CPU가 [상태 레지스터](/studynote/01_computer_architecture/04_instruction_set_architecture/167_status_register/)를 반복적으로 읽으며 "준비되었는가"를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다. 저속 키보드처럼 이벤트가 드문 장치에 이 방식을 쓰면, 대부분의 사이클은 아무 의미 없는 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 작업에 소비된다. 반면 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구동 I/O는 장치가 실제로 준비된 순간에만 CPU를 중단시키므로, 평균 대기 시간보다 CPU 낭비를 크게 줄인다.

아래 그림은 같은 I/O 대기 상황에서 CPU 시간이 어떻게 쓰이는지 보여준다.

```text
+----------------------------------------------------------------------+
|          CPU 시간 사용 비교: 묻고 기다릴 것인가, 알림만 받을 것인가 |
+-----------------------+----------------------------------------------+
| 폴링 (Polling)        | 계산 -+- 확인 -+- 확인 -+- 확인 -+- 확인    |
|                       |       +-------- 대부분이 바쁜 대기 --------+ |
+-----------------------+----------------------------------------------+
| 인터럽트 구동 I/O     | 계산 ----- 계산 ----- 계산 ------> 인터럽트 처리 |
|                       |                  필요 시점에만 개입            |
+-----------------------+----------------------------------------------+
```

이 차이는 시스템 전체 설계에도 영향을 준다. CPU가 장치 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)에 매달리지 않으면 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 더 많은 프로세스를 스케줄링할 수 있고, 고가의 연산 자원을 낭비하지 않게 된다. 즉 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구동 I/O는 단순히 "편한 알림"이 아니라, 범용 컴퓨터가 다수의 장치와 작업을 동시에 다루게 만든 기본 전제다.

**📢 섹션 요약 비유**: [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)은 아이가 버스가 왔는지 10초마다 정류장 밖을 내다보는 것이고, [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 버스가 도착하면 기사님이 벨을 눌러 알려주는 방식이다. 밖을 계속 볼 필요가 없으니 그 시간에 숙제를 할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구동 I/O는 보통 장치 컨트롤러, [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러, CPU, [인터럽트 벡터](/studynote/02_operating_system/01_overview_architecture/019_interrupt_vector/), [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) ([Interrupt Service Routine](/studynote/01_computer_architecture/08_io_storage_systems/317_isr/)) 순으로 이어진다. 장치가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 준비하면 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 요청을 올리고, [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러는 우선순위를 정해 CPU에 전달한다. CPU는 현재 문맥을 저장한 뒤 해당 벡터가 가리키는 ISR로 분기하고, 필요한 최소 처리 후 원래 작업으로 복귀한다.

이 흐름의 핵심은 "즉시 반응"이 아니라 "안전하게 끊고 다시 이어 붙이기"다. [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 발생했을 때 [프로그램 카운터](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) (Program [Counter](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)), [상태 레지스터](/studynote/01_computer_architecture/04_instruction_set_architecture/167_status_register/), 범용 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 적절히 저장하지 않으면, I/O는 처리하더라도 원래 실행 중이던 프로그램이 깨진다. 그래서 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구조는 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 전달 구조이면서 동시에 문맥 보존 구조다.

아래 그림은 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리의 제어 경로를 요약한다.

```text
+----------------------------------------------------------------------+
|               인터럽트 구동 I/O의 제어 흐름                         |
+----------------------------------------------------------------------+
| 장치 컨트롤러 --> 인터럽트 컨트롤러 --> CPU                           |
|      |                    |                 |                         |
|      | 작업 완료          | 우선순위 판정   | 현재 문맥 저장          |
|      v                    v                 v                         |
| 상태 레지스터        인터럽트 벡터 번호 --> ISR 실행 --> 복귀 명령      |
|                                                |                     |
|                                                +- 데이터 읽기/ACK    |
+----------------------------------------------------------------------+
```

실제 설계에서는 ISR을 짧게 유지하는 것이 중요하다. [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) 안에서 오래 계산하면 다른 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)되고, 전체 응답성이 무너진다. 그래서 일반적으로 ISR은 장치 상태 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 버퍼 이동 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/), 하위 작업 예약 정도만 처리하고, 무거운 처리는 이후의 소프트웨어 경로로 넘긴다.

| 구성 요소 | 역할 | 설계 포인트 |
| :-- | :-- | :-- |
| 장치 컨트롤러 (Device Controller) | 작업 완료·오류 상태 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 상태 비트와 버퍼 상태 [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/) |
| [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 컨트롤러 ([Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) Controller) | 요청 수집, 우선순위 판정, [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | 마스킹, 중첩, 코어 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |
| [인터럽트 벡터](/studynote/02_operating_system/01_overview_architecture/019_interrupt_vector/) ([Interrupt Vector](/studynote/02_operating_system/01_overview_architecture/019_interrupt_vector/)) | [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) 진입 주소 결정 | 빠른 분기와 정확한 매핑 |
| [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) ([Interrupt Service Routine](/studynote/01_computer_architecture/08_io_storage_systems/317_isr/)) | 최소한의 즉시 처리 | 짧은 실행 시간, 재진입성 |
| 복귀 절차 (Return Path) | 원래 [태스크](/studynote/02_operating_system/02_process_thread/150_task/) 재개 | 문맥 손상 방지 |

현대 시스템에서는 PIC (Programmable [Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) Controller)보다 APIC (Advanced Programmable [Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) Controller), 그리고 [PCI Express](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 장치의 [MSI](/studynote/01_computer_architecture/15_advanced_topics/561_msi/) (Message Signaled [Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/))가 더 중요하다. 이는 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 전달을 더 세밀하게 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)하고, 멀티코어 환경에서 특정 코어에 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)하기 위한 진화다. 결국 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구동 I/O의 핵심 원리는 변하지 않지만, 그 전달 방식은 병렬성과 확장성을 위해 계속 고도화되고 있다.

**📢 섹션 요약 비유**: [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리는 호텔 프런트가 호출을 받으면 객실 번호를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, 담당 직원에게 바로 연결한 뒤 기록을 남기고 원래 업무로 돌아가는 과정과 같다. 벨 소리만 듣고 뛰는 것이 아니라, 누구 요청인지 정확히 분기해야 전체 운영이 꼬이지 않는다.

---

## Ⅲ. 비교 및 연결

[인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구동 I/O를 제대로 이해하려면 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/), [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/), DMA를 같은 축에서 비교해야 한다. 세 방식은 단순히 "좋고 나쁨"의 관계가 아니라, CPU 개입 빈도와 전송 단위가 다른 선택지다. 작은 이벤트가 가끔 발생하면 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 유리하지만, 대용량 연속 전송에서는 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)마다 CPU를 깨우는 비용이 누적되어 DMA가 더 적합해진다.

| 항목 | [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) ([Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/)) | [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구동 I/O | [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) |
| :-- | :-- | :-- | :-- |
| CPU 개입 방식 | 계속 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 사건 발생 시 개입 | [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)과 완료 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)만 수행 |
| 장점 | 구조 단순, 예측 가능 | CPU 낭비 감소, 반응성 양호 | 대용량 전송에서 CPU 부담 최소 |
| 약점 | [바쁜 대기](/studynote/02_operating_system/04_synchronization/227_busy_waiting/) 낭비 | [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 폭주 가능 | 하드웨어 복잡도 증가 |
| 적합한 상황 | 매우 단순 장치, 짧은 대기 | 중간 빈도의 비동기 이벤트 | 디스크·네트워크 대량 전송 |

여기서 중요한 비교 포인트는 응답성과 처리량의 균형이다. [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 첫 반응이 빠르지만, 이벤트가 너무 자주 오면 CPU가 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리기 자체가 되어 버린다. 반대로 DMA는 효율적이지만 작은 이벤트 하나하나에 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)에는 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 비용이 상대적으로 크다.

[운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 관점에서도 연결점이 뚜렷하다. 타이머 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 선점형 스케줄링을 가능하게 하고, 네트워크 카드 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 패킷 수신 경로를 깨운다. 저장장치에서는 완료 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 I/O 요청 큐의 다음 작업을 진행시키므로, [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 장치 제어 메커니즘이면서 커널의 이벤트 구동 모델을 떠받치는 기반이다.

또 하나의 경계는 "저속 장치에는 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 좋다"라는 단순화의 한계다. [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 네트워크 인터페이스 카드인 [NIC](/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/) (Network Interface Card)에서는 초당 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 수가 너무 많아 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 폭주가 생길 수 있다. 그래서 현대 네트워크 스택은 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 코얼레싱 ([Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) Coalescing), NAPI ([New](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) 같은 혼합 전략으로 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)와 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)의 경계를 동적으로 조절한다.

**📢 섹션 요약 비유**: [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 손님이 필요할 때만 벨을 누르는 식당 운영과 같고, DMA는 큰 연회 주문을 아예 카트째 옮기는 방식이다. 손님 한 명의 물 한 잔은 벨로 처리해도 되지만, 수백 접시를 한 번에 옮길 때는 다른 운반 방식이 더 낫다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구동 I/O는 "써야 하는가"보다 "어디까지 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)에 맡길 것인가"가 더 중요한 판단 문제다. 예를 들어 키보드, 마우스, 센서, 제어 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)처럼 이벤트 발생 빈도는 낮고 즉시 반응이 중요한 장치에는 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 매우 적합하다. 반면 고속 스토리지나 40GbE 이상 네트워크처럼 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)량이 큰 장치에서는 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)만으로 처리하면 문맥 전환 비용과 캐시 교란이 커질 수 있다.

설계자는 특히 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간과 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)율을 함께 봐야 한다. 응답 시간이 중요한 실시간 제어 시스템에서는 높은 우선순위, 짧은 [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/), [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 마스킹 최소화가 핵심이다. 반대로 처리량이 중요한 서버에서는 코얼레싱, 큐 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/), 멀티큐 기반 [MSI](/studynote/01_computer_architecture/15_advanced_topics/561_msi/)-X 구성으로 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 횟수를 조절하는 편이 더 효과적이다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 장치 이벤트가 희소한가, 아니면 초당 수만~수백만 건 수준으로 빈번한가?
2. ISR이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사·[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 출력 같은 무거운 작업을 품고 있지 않은가?
3. 멀티코어에서 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 특정 코어에만 몰려 병목을 만들지 않는가?
4. 대용량 전송이라면 DMA와 완료 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 조합으로 바꿀 수 있는가?
5. [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 폭주 상황에서 코얼레싱, [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/), [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) 전환 전략이 준비되어 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 장치 이벤트 빈도를 측정하지 않고 무조건 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 기반으로 설계하는 것
- [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) 안에서 긴 루프, 메모리 할당, 블로킹 호출을 수행하는 것
- 고속 장치에서도 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)당 패킷 1개 처리 모델을 고집하는 것

기술사 답안에서는 "[인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 CPU 효율을 높인다"에서 멈추면 부족하다. 반드시 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 오버헤드, 문맥 전환 비용, 고속 I/O에서의 폭주 문제, DMA와의 역할 분담까지 같이 언급해야 판단력이 드러난다. 좋은 답안은 장점 소개가 아니라, 어떤 조건에서 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 최적이고 어떤 조건에서 보조 기법이 필요한지까지 제시한다.

**📢 섹션 요약 비유**: [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 필요한 순간에만 호출하는 비상벨과 같지만, 공장 전체가 동시에 벨을 누르면 관리자도 아무 일도 못 한다. 그래서 좋은 운영은 벨의 존재보다 벨을 언제·얼마나 울리게 할지를 조절하는 데 있다.

---

## Ⅴ. 기대효과 및 결론

[인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구동 I/O의 가장 큰 효과는 CPU를 장치 감시자에서 사건 처리자로 바꾼다는 점이다. 이 전환 덕분에 하나의 CPU는 계산, 스케줄링, 메모리 관리, 여러 장치 서비스를 번갈아 수행할 수 있게 되었고, 범용 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 [멀티태스킹](/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/) 효율도 함께 높아졌다. 즉 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 단순한 I/O 최적화가 아니라, 컴퓨터가 "동시에 많은 일을 하는 것처럼 보이게" 만드는 핵심 토대다.

다만 한계도 분명하다. [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)는 발생 빈도가 높아질수록 오히려 CPU 부하의 원인이 되고, 멀티코어 시스템에서는 [라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)과 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 문제도 생긴다. 그래서 현대 시스템은 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)만 고집하지 않고 [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/), [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/), 코얼레싱, 적응형 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)을 결합해 전체 효율을 맞춘다.

정리하면 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 구동 I/O는 "CPU를 덜 일하게 하는 기술"이 아니라 "CPU가 더 중요한 일에 집중하게 만드는 기술"로 기억하는 것이 맞다. 저빈도 비동기 이벤트에는 날카로운 도구이고, 고빈도 대량 전송에서는 다른 메커니즘과 조합될 때 가장 강하다. 이 관점을 잡으면 시험에서도 실무에서도 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)·[인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)·DMA의 경계를 흔들리지 않고 설명할 수 있다.

**📢 섹션 요약 비유**: 좋은 비서는 사장이 모든 메일함을 계속 열어보게 하지 않고, 정말 처리할 일만 골라 알려준다. 하지만 메일이 초당 수천 통 오기 시작하면 알림만으로는 감당이 안 되므로, [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 일괄 처리까지 함께 써야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/) ([Polling](/studynote/02_operating_system/11_exam_summary/747_io_polling_overhead/)) | [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 해결하려는 [바쁜 대기](/studynote/02_operating_system/04_synchronization/227_busy_waiting/)의 직접 비교 대상 |
| [인터럽트 벡터](/studynote/02_operating_system/01_overview_architecture/019_interrupt_vector/) ([Interrupt Vector](/studynote/02_operating_system/01_overview_architecture/019_interrupt_vector/)) | 어떤 ISR로 분기할지 결정하는 주소 체계 |
| [ISR](/studynote/02_operating_system/01_overview_architecture/020_isr/) ([Interrupt Service Routine](/studynote/01_computer_architecture/08_io_storage_systems/317_isr/)) | [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 발생 직후 실행되는 최소 처리 코드 |
| [DMA](/studynote/02_operating_system/11_exam_summary/746_io_direct_memory_access_dma/) ([Direct Memory Access](/studynote/01_computer_architecture/08_io_storage_systems/318_dma/)) | 대용량 전송에서 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)와 역할을 분담하는 핵심 메커니즘 |
| APIC (Advanced Programmable [Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) Controller) | 멀티코어에서 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 효율적으로 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)·[라우팅](/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)하는 장치 |
| [MSI](/studynote/01_computer_architecture/15_advanced_topics/561_msi/) (Message Signaled [Interrupt](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)) | 핀 기반 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 메모리 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 기반 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)로 확장한 현대 방식 |

### 📈 관련 키워드 및 발전 흐름도

```text
프로그램 제어 I/O
    |
    v
폴링 (Polling)
    |  CPU 낭비 문제 노출
    v
인터럽트 구동 I/O (Interrupt-driven I/O)
    |  이벤트 기반 반응 확보
    +---------------+
    v               v
APIC / MSI          DMA (Direct Memory Access)
    |               |
    | 멀티코어·고속화 | 대용량 전송 분리
    +-------+-------+
            v
인터럽트 코얼레싱 · 적응형 폴링 · 고성능 I/O 스택
```

이 흐름은 "계속 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)"에서 "필요 시 알림"으로, 다시 "알림도 과하면 묶어서 처리"하는 방향으로 I/O 제어가 진화했음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터는 장치가 끝났는지 매초 물어보지 않고, 끝나면 "나 다 했어!" 하고 알려 달라고 약속할 수 있어요.
2. 그래서 컴퓨터는 기다리는 동안 다른 숙제를 하다가, 진짜 필요할 때만 잠깐 달려가요.
3. 하지만 친구들이 너무 자주 동시에 부르면 정신없어지니까, 큰일은 한꺼번에 옮기거나 알림 횟수를 줄여야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 315 / 803

<- **이전**: [313. 폴링 (Polling)](/studynote/01_computer_architecture/08_io_storage_systems/313_polling/)
**다음**: [315. 인터럽트 (Interrupt)](/studynote/01_computer_architecture/08_io_storage_systems/315_interrupt/) ->

---
