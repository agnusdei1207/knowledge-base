---
title: "Secure Context Switching"
date: "2026-05-08"
tags:
  - "studynote-computer-architecture"
weight: 544
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/) (Secure [Context](/studynote/02_operating_system/01_overview_architecture/033_context/) Switching)은 프로세스, 가상 머신 ([Virtual Machine](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)), [TEE](/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) ([Trusted Execution Environment](/studynote/09_security/19_ai_advanced_security/972_tee_based_ml/)) 간 전환을 단순 스케줄링이 아니라 신뢰 경계 이동으로 보고, [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 저장·복원에 더해 남은 [마이크로아키텍처](/studynote/01_computer_architecture/05_control_unit_pipelining/204_microarchitecture/) 상태를 격리·초기화·재태깅하는 절차다.
> 2. **가치**: [Spectre](/studynote/01_computer_architecture/14_hardware_security_trends/483_spectre/), [Meltdown](/studynote/01_computer_architecture/14_hardware_security_trends/482_meltdown/), [MDS](/studynote/01_computer_architecture/15_advanced_topics/764_mds/) ([Microarchitectural Data Sampling](/studynote/09_security/04_endpoint_security/380_mds_attack/)) 계열 공격 이후 캐시, [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)기, [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/)), 벡터 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 남은 흔적이 정보 유출 경로가 됨이 확인되면서, [멀티테넌트](/studynote/05_database/05_distributed_nosql_newsql/310_multi_tenant_database_architecture/) 클라우드와 [기밀 컴퓨팅](/studynote/01_computer_architecture/15_advanced_topics/795_confidential_computing/)의 필수 메커니즘이 되었다.
> 3. **판단 포인트**: 모든 전환에 전체 flush를 거는 것은 비효율적이므로, 보안 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 경계인지 여부에 따라 [ASID](/studynote/02_operating_system/06_memory_management/360_asid/) (Address Space [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/)), VMID ([Virtual Machine](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/)), predictor barrier, [key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) roll, core scheduling을 조합해야 한다.

---

## Ⅰ. 개요 및 필요성

안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 CPU (Central Processing Unit)가 한 실행 주체에서 다른 실행 주체로 넘어갈 때, 단순히 프로그램 카운터와 [범용 레지스터](/studynote/01_computer_architecture/04_instruction_set_architecture/162_gpr/)만 바꾸는 수준을 넘어 이전 실행의 잔류 흔적이 다음 실행에 새지 않도록 보안 처리를 포함하는 전환 기법이다. 전통적인 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 "정확히 이어서 실행할 수 있는가"가 목표였지만, 오늘날에는 "이전 보안 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)의 흔적이 다음 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 보이지 않는가"까지 함께 만족해야 한다.

이 요구가 커진 이유는 현대 CPU가 속도를 위해 캐시, [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)기, 투기 실행 상태, 변환 캐시를 적극적으로 재사용하기 때문이다. 이런 구조는 같은 프로세스 안에서는 효율적이지만, 서로 신뢰하지 않는 테넌트가 한 코어를 공유하는 클라우드나 [TEE](/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) 진입·이탈 경계에서는 오히려 정보 유출 통로가 될 수 있다. 즉 과거에는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화였던 잔류 상태가, 지금은 보안 설계의 핵심 변수가 됐다.

그래서 안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 운영체제의 스케줄링 문제이면서 동시에 하드웨어 보안 문제다. 어떤 상태를 저장할지보다, 어떤 상태를 지울지·격리할지·태그를 바꿀지가 더 중요한 시대가 된 것이다.

- **📢 섹션 요약 비유**: 안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 같은 책상을 여러 사람이 번갈아 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 전에, 공책만 치우는 것이 아니라 메모지와 흔적까지 지우는 절차와 같다. 자리만 바뀌면 된다는 생각으로는 비밀을 지킬 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)의 핵심은 상태를 한 덩어리로 보지 않고 계층별로 다르게 다루는 데 있다. [범용 레지스터](/studynote/01_computer_architecture/04_instruction_set_architecture/162_gpr/)와 제어 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)는 저장·복원이 필요하고, 주소 변환 상태는 태그 교체나 선택적 flush가 필요하며, [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)기나 캐시 잔류 상태는 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 경계에 따라 barrier·scrub·partition이 필요하다. 기밀 VM이나 enclave에서는 여기에 [메모리 암호화](/studynote/01_computer_architecture/15_advanced_topics/796_memory_encryption/) 키 전환까지 포함된다.

| 상태 계층 | 무엇을 처리하는가 | 대표 기법 |
| :-- | :-- | :-- |
| 아키텍처 상태 | [범용 레지스터](/studynote/01_computer_architecture/04_instruction_set_architecture/162_gpr/), 제어 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), 예외 상태 | 저장·복원, 민감 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 0화 |
| 주소 변환 상태 | [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/), [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 워크 캐시 | [ASID](/studynote/02_operating_system/06_memory_management/360_asid/)/VMID 교체, 선택적 flush |
| [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) 상태 | 분기 이력, 간접 [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) 정보 | [IBPB](/studynote/01_computer_architecture/15_advanced_topics/579_ibpb/) ([Indirect](/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/) Branch Predictor Barrier), [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 분리 |
| 캐시·버퍼 잔류 상태 | L1 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), fill buffer, load [queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/) 흔적 | flush, [partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/), core [isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) |
| 암호화 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) | [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)/TEE별 [메모리 보호 키](/studynote/02_operating_system/06_memory_management/375_memory_protection_keys/) | [key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) roll, secure world entry/exit |

이 그림은 일반 전환과 보안 경계 전환이 어떻게 갈라지는지 보여 준다.

```text
+----------------------------------------------------------------------+
| 보안 경계 기반 스위치: 저장 이후에 '잔류 상태 처리'가 이어져야 한다     |
+----------------------------------------------------------------------+
| 실행 주체 A                                                        |
|       | 타이머 / 트랩 / 가상 머신 전환                              |
|       v                                                             |
| 레지스터 / 제어 상태 저장                                          |
|       |                                                             |
|       +- 같은 신뢰 도메인 --------> ASID / VMID 재태깅 --> 재개       |
|       |                                                             |
|       +- 교차 도메인 ----------> 예측기 barrier / 키 교체 / 소거      |
|                                         |                            |
|                                         v                            |
|                               실행 주체 B 상태 적재                |
|                                         |                            |
|                                         v                            |
|                                   실행 주체 B 재개                 |
+----------------------------------------------------------------------+
```

중요한 점은 모든 전환이 동일하게 무거울 필요는 없다는 것이다. 같은 보안 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 안의 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 전환은 태그 교체와 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 저장으로 충분할 수 있지만, 다른 테넌트 가상 머신 사이 전환은 predictor barrier와 더 강한 잔류 상태 정리가 필요하다. 즉 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 지키려면 보안 경계의 강도에 따라 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 비용을 계층화해야 한다.

또한 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 저장 ([lazy](/studynote/06_ict_convergence/05_data_science/380_computational_graph_lazy_eager_execution/) save) 전략은 보안 측면에서 재평가가 필요하다. 예전에는 벡터 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 실제로 사용할 때까지 저장을 미루는 방식이 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 유리했지만, 민감 상태가 예상치 못한 경로로 노출될 수 있다는 점이 드러나면서 보안 민감 영역에서는 즉시 저장 (eager save)과 0화가 더 안전한 선택이 된다.

- **📢 섹션 요약 비유**: 안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 병원 수술실 정리와 같다. 같은 의료진끼리 방을 옮길 때는 간단한 정리가 되지만, 다른 환자와 다른 수술로 넘어갈 때는 도구 소독과 환경 교체까지 해야 한다.

---

## Ⅲ. 비교 및 연결

안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 일반 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)의 상위 집합이지만, 실제 구현 방식은 크게 두 갈래로 나뉜다. 하나는 flush 중심 모델이고, 다른 하나는 태그·분할 중심 모델이다. 전자는 강한 격리를 쉽게 설명할 수 있지만 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 크고, 후자는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 좋지만 하드웨어 지원과 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 설계가 더 중요하다.

| 방식 | 핵심 아이디어 | 장점 | 약점 |
| :-- | :-- | :-- | :-- |
| 일반 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/) | 아키텍처 상태만 저장·복원 | 빠르고 단순 | 잔류 마이크로상태 누출에 취약 |
| flush 중심 보안 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) | 경계마다 예측기·캐시·버퍼를 적극 소거 | 설명이 명확하고 강한 격리 | cold cache, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 증가, [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 저하 |
| 태그·분할 중심 보안 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) | [ASID](/studynote/02_operating_system/06_memory_management/360_asid/)/VMID, core scheduling, [partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 활용 | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 손실을 줄이기 좋음 | 하드웨어 의존성과 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 복잡성 증가 |

이 차이는 TEE나 [기밀 컴퓨팅](/studynote/01_computer_architecture/15_advanced_topics/795_confidential_computing/)과 직접 연결된다. 예를 들어 TrustZone 같은 보안 세계 전환은 보안 경계가 분명하므로 더 강한 정리가 필요하고, 같은 애플리케이션의 사용자 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 전환은 그 정도까지 필요하지 않을 수 있다. 따라서 안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 "항상 다 지우기"가 아니라 "어떤 경계를 넘는가에 따라 무엇을 지울지 정하기"가 핵심이다.

또한 [SMT](/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) (Simultaneous [Multithreading](/studynote/02_operating_system/02_process_thread/095_multithreading_benefits/)) 환경에서는 같은 코어의 형제 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/)가 동시에 다른 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 공유할 수 있어 문제가 더 복잡해진다. 문맥 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 아무리 잘해도, 같은 순간에 옆 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 코어가 민감 상태를 관찰할 수 있다면 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)가 반쪽이 될 수 있기 때문이다. 그래서 core scheduling이나 [SMT](/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) 비활성화 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 함께 논의된다.

- **📢 섹션 요약 비유**: 일반 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 교실 자리 바꾸기라면, 안전한 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 시험지 교체와 감독 규칙까지 포함한 시험장 운영이다. 단순 이동과 기밀 유지의 규칙은 같은 일이 아니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 대표적인 적용처는 [멀티테넌트](/studynote/05_database/05_distributed_nosql_newsql/310_multi_tenant_database_architecture/) 클라우드다. 서로 다른 고객 가상 머신이 같은 물리 코어를 공유할 수 있는 환경에서는, 하이퍼바이저가 가상 머신 전환 시 predictor barrier, core scheduling, 민감 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 초기화, [메모리 암호화](/studynote/01_computer_architecture/15_advanced_topics/796_memory_encryption/) [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 교체를 함께 고려해야 한다. 특히 TDX (Trust [Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) Extensions)나 SEV-SNP (Secure Encrypted Virtualization-Secure Nested [Paging](/studynote/02_operating_system/04_synchronization/259_paging/)) 같은 기밀 가상 머신 기술은 단순 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 전환을 넘어 키 경계까지 다룬다.

또 다른 적용처는 [TEE](/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) 진입과 이탈이다. 보안 세계로 들어갈 때 일반 세계의 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)와 공유 버퍼를 정리하지 않으면, 오히려 보안 환경이 이전 문맥의 흔적을 받아들이는 역류가 생길 수 있다. 따라서 [TEE](/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) 경계에서는 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 정리, [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/) 규약, 예외 처리 경로까지 포함한 엄격한 전환 설계가 필요하다.

### 적용 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 이번 전환이 같은 신뢰 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 내부인지, 다른 테넌트나 특권 경계를 넘는 전환인지 구분했는가?
2. 어떤 상태는 [ASID](/studynote/02_operating_system/06_memory_management/360_asid/)/VMID 같은 태그로 격리하고, 어떤 상태는 실제로 소거해야 하는지 분류했는가?
3. [SMT](/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) 형제 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 공유 문제를 core scheduling 또는 비활성화 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 통제하고 있는가?
4. 벡터 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), 암호 키 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), 공유 버퍼를 lazy하게 남겨 두지 않고 필요한 시점에 즉시 정리하는가?
5. 보안 강화로 늘어난 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 측정하고, 스케줄링 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)에 반영하고 있는가?

### 피해야 할 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 스케줄링 이벤트에 동일한 전면 flush를 적용해 시스템 전체 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 불필요하게 떨어뜨리는 설계
- [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/)만 바꾸고 [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/)기·버퍼·공유 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)는 그대로 두는 설계
- 기밀 VM은 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하면서도 호스트-게스트 사이 공유 메일박스나 bounce buffer는 정리하지 않는 설계

기술사 답안에서는 "보안을 위해 flush한다" 수준을 넘어, 어떤 경계에서 왜 flush가 필요하고, 왜 어떤 경우에는 태깅이 더 합리적인지까지 구분해야 한다. 결국 안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)의 본질은 모든 것을 비우는 기술이 아니라, 위험한 잔류 상태만 정확히 겨냥해 신뢰 경계를 유지하는 기술이다.

- **📢 섹션 요약 비유**: 안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/) 운영은 호텔 객실 청소와 같다. 손님이 완전히 바뀔 때는 침구와 비품까지 교체해야 하지만, 같은 손님의 짧은 외출마다 대청소를 하면 운영이 마비된다.

---

## Ⅴ. 기대효과 및 결론

안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)의 기대효과는 명확하다. 서로 신뢰하지 않는 실행 주체가 같은 CPU 자원을 공유하더라도, 이전 문맥의 잔류 흔적을 통해 비밀이 새어 나갈 가능성을 크게 줄일 수 있다. 이는 클라우드 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/), [기밀 컴퓨팅](/studynote/01_computer_architecture/15_advanced_topics/795_confidential_computing/), 보안 세계 전환, 고가치 워크로드 격리의 기반이 된다.

반면 비용도 있다. predictor barrier와 flush는 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 늘리고, cold cache는 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 낮춘다. 따라서 미래 방향은 무조건적인 소거보다, 더 정교한 태깅, 하드웨어 분할, [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 예측기·캐시 격리, 자동 키 교체처럼 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 보안을 동시에 잡는 방향으로 갈 가능성이 크다.

결론적으로 안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 "[레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 저장의 확장판"이 아니다. 그것은 CPU가 스케줄링 순간을 신뢰 경계 전환으로 인식하고, 남은 흔적까지 관리하기 시작했다는 뜻이다.

- **📢 섹션 요약 비유**: 안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 칠판의 글씨만 지우는 것이 아니라 분필 가루까지 닦아 내는 일과 같다. 다음 사람이 무엇을 보게 될지까지 책임지는 것이 진짜 보안이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Context Switch](/studynote/02_operating_system/03_cpu_scheduling/211_context_switch/)) | 안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)의 기본이 되는 스케줄링 전환 행위다. |
| [ASID](/studynote/02_operating_system/06_memory_management/360_asid/) (Address Space [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/)) | 주소 변환 상태를 전환해도 전체 flush를 줄이는 대표 태깅 기법이다. |
| VMID ([Virtual Machine](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/)) | 가상 머신 단위 주소 공간과 캐시/[TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) 식별에 쓰인다. |
| [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/)) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 핵심 구조이면서 잘못 다루면 잔류 정보 누출 경로가 된다. |
| [IBPB](/studynote/01_computer_architecture/15_advanced_topics/579_ibpb/) ([Indirect](/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/) Branch Predictor Barrier) | [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 경계에서 [분기 예측](/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/) 상태를 끊어 주는 대표 barrier다. |
| Core Scheduling | [SMT](/studynote/01_computer_architecture/11_multicore_synchronization/400_smt/) 환경에서 같은 코어를 공유하는 주체를 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)적으로 제한한다. |
| [TEE](/studynote/01_computer_architecture/14_hardware_security_trends/478_tee/) ([Trusted Execution Environment](/studynote/09_security/19_ai_advanced_security/972_tee_based_ml/)) | 일반 세계와 보안 세계 사이의 엄격한 전환이 필요한 대표 환경이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
기본 레지스터 저장·복원 중심 컨텍스트 스위치
                     |
                     v
ASID / VMID 기반 주소 공간 태깅
                     |
                     v
Spectre · Meltdown 이후 predictor barrier · buffer flush
                     |
                     v
기밀 VM · TEE 진입/이탈 · core scheduling
                     |
                     v
도메인별 분할 캐시 · 예측기 격리 · 자동 키 교체
```

이 흐름은 "정확한 재개" 중심의 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가, 점차 "잔류 상태 격리"와 "신뢰 경계 유지" 중심의 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)로 진화하는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터는 여러 친구가 한 책상을 돌려 쓸 때, 앞 친구의 비밀 메모가 남지 않게 정리해야 해요.
2. 그냥 의자만 바꾸면 되는 게 아니라, 책상 위 종이와 가루와 힌트까지 치워야 다음 친구가 몰래 보지 못해요.
3. 그래서 안전한 [컨텍스트 스위칭](/studynote/02_operating_system/01_overview_architecture/034_context_switch/)은 "자리 바꾸기"가 아니라 "비밀 청소까지 포함한 자리 바꾸기"예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 544 / 803

<- **이전**: [543. 양자 내성 암호 가속기 (PQC Accelerator)](/studynote/01_computer_architecture/15_advanced_topics/543_pqc_accelerator/)
**다음**: [545. 인터럽트 지연 시간 (Interrupt Latency) 최소화](/studynote/01_computer_architecture/15_advanced_topics/545_interrupt_latency/) ->

---
