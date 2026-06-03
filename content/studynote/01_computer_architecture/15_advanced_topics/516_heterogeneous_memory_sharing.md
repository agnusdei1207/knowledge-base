+++
title = "516. 이종 컴퓨팅 메모리 공유 (Heterogeneous Memory Sharing)"
date = 2026-04-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 이종 컴퓨팅 메모리 공유는 중앙 처리 장치 (Central Processing Unit, CPU)와 그래픽 처리 장치 ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)) 같은 서로 다른 장치가 같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 대해 공통 주소 체계와 일관된 접근 규칙을 갖도록 만드는 기술이다.
> 2. **가치**: 장치 사이 복사와 재직렬화 비용을 줄여 제로 카피에 가까운 실행을 가능하게 하고, 개발자는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 "논리적 위치"보다 "누가 더 가까이 쓰는가"에 집중할 수 있다.
> 3. **판단 포인트**: 공유 주소 공간이 곧 동일 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간을 뜻하지는 않으므로, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 이동 비용·원격 접근 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·[캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 트래픽을 함께 고려해 소유권과 배치 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

이종 컴퓨팅 메모리 공유는 CPU와 GPU처럼 구조가 다른 처리 장치가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 각자 복사본으로 들고 다니는 대신, 하나의 주소 체계 또는 일관된 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 뷰를 통해 접근하게 만드는 기술이다. 핵심은 단순히 주소를 같게 보이게 하는 것이 아니라, <strong>누가 어떤 시점에 어떤 버전을 보고 있는지</strong>를 시스템 차원에서 맞추는 데 있다.

이 기술이 중요해진 이유는 장치 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동이 계산 자체보다 더 비싸지는 일이 많아졌기 때문이다. 전처리는 CPU, 학습·추론은 [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), 후처리는 다시 CPU가 담당하는 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 파이프라인에서는 같은 텐서를 여러 번 복사하는 순간 대역폭과 전력이 급격히 낭비된다. 이종 메모리 공유는 이런 복사 왕복을 줄여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동을 병목이 아닌 배치 문제로 바꾸려는 시도다.

또한 메모리 용량 관점에서도 장점이 있다. 가속기 로컬 메모리가 부족할 때 시스템 메모리나 외부 [메모리 풀](/knowledge-base/studynote/02_operating_system/06_memory_management/369_memory_pool/)을 함께 사용할 수 있고, 장치별로 조각나 있던 메모리를 더 유연하게 활용할 수 있다. 즉 이 기술의 목표는 "복사를 없애는 것"을 넘어, <strong>서로 다른 메모리 계층을 하나의 협력 체계로 묶는 것</strong>이다.

- **📢 섹션 요약 비유**: 이종 메모리 공유는 친구마다 따로 공책을 베껴 쓰는 대신, 모두가 같은 큰 화이트보드를 보며 필요한 자리에서 바로 읽고 쓰는 방식과 같다. 베껴 적는 시간이 줄어들면 진짜 문제 푸는 시간이 늘어난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

실제 구현은 크게 세 층으로 나뉜다. 첫째, 공유 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) (Shared [Virtual Memory](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/), [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/))나 통합 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) (Unified [Virtual Memory](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/), UVM)처럼 같은 포인터를 장치들이 이해할 수 있게 하는 주소 체계가 필요하다. 둘째, 입출력 메모리 관리 장치 (Input/Output [Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/), [IOMMU](/knowledge-base/studynote/02_operating_system/10_security/627_iommu_dma_isolation/))와 주소 변환 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (Address Translation Services, ATS)가 장치 쪽 주소 변환을 가능하게 해야 한다. 셋째, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 이동과 [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/)을 다루는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 계층이 필요하다. 이때 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 동적 램 (Dynamic Random Access Memory, [DRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/)), 고대역폭 메모리 ([High Bandwidth Memory](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/), [HBM](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/495_hbm/)), 컴퓨트 익스프레스 링크 ([Compute Express Link](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/), [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) 기반 외부 메모리 중 하나에 놓일 수 있다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ Shared address, different physical homes                                │
├──────────────────────────────────────────────────────────────────────────┤
│ App pointer 0x7f...                                                     │
│      │                                                                   │
│      ├─ CPU page walk  -> host page table                               │
│      └─ GPU ATS request -> same mapping                                 │
│                                                                          │
│ Shared virtual view                                                      │
│   0x7f... -> DRAM page        (CPU-local)                                │
│   0x80... -> HBM page         (GPU-local)                                │
│   0x90... -> CXL pool page    (shared capacity tier)                     │
│                                                                          │
│ Policy                                                                   │
│   page fault -> migrate / map remote / pin read-mostly                   │
│   coherence  -> invalidate or update peer caches                         │
└──────────────────────────────────────────────────────────────────────────┘
```

이 그림은 "같은 주소"와 "같은 물리 위치"가 다르다는 점을 강조한다. 프로그래머는 같은 포인터를 보더라도, 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 CPU 가까운 동적 램, [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 가까운 고대역폭 메모리, 혹은 컴퓨트 익스프레스 링크 ([Compute Express Link](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/), [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/)) 기반 [메모리 풀](/knowledge-base/studynote/02_operating_system/06_memory_management/369_memory_pool/) 가운데 하나에 놓일 수 있다.

| 메커니즘 | 역할 | 주의점 |
| :-- | :-- | :-- |
| [SVM](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/238_svm_margin_kernel_trick_naive_bayes/) / UVM | 장치들이 같은 가상 주소를 이해하게 함 | 주소가 같아도 접근 비용은 다를 수 있음 |
| [IOMMU](/knowledge-base/studynote/02_operating_system/10_security/627_iommu_dma_isolation/) / ATS | 장치 측 주소 변환과 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 수행 | [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 워크와 변환 캐시 미스 비용 존재 |
| [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 마이그레이션 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 더 자주 쓰는 장치 쪽으로 이동 | 핑퐁 이동이 발생하면 오히려 느려짐 |
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 링크 | 캐시 간 최신 상태를 맞춤 | 트래픽과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 증가할 수 있음 |
| [메모리 풀링](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/442_memory_pooling/) | 장치 로컬 메모리 부족을 외부 용량으로 보완 | 원격 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 관리 필요 |

즉 이종 메모리 공유의 핵심 원리는 "복사하지 않고 접근한다"가 아니라, <strong>복사·원격 접근·마이그레이션 중 무엇이 가장 싼지 동적으로 고르는 것</strong>에 더 가깝다.

- **📢 섹션 요약 비유**: 이 구조는 같은 주소가 적힌 택배 상자를 중앙 창고, 가까운 창고, 임시 보관소 중 어디에 둘지 계속 조정하는 물류 시스템과 같다. 상자 이름은 같아도 꺼내 오는 거리는 다르다.

---

## Ⅲ. 비교 및 연결

이종 컴퓨팅 메모리 공유를 이해할 때 가장 중요한 비교는 명시적 복사 모델, 관리형 통합 메모리, 완전 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)의 차이다. 세 방식은 모두 "장치 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 사용"을 다루지만, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 특성과 프로그래밍 비용이 다르다.

| 모델 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 방식 | 장점 | 한계 |
| :-- | :-- | :-- | :-- |
| 명시적 복사 모델 | 애플리케이션이 직접 복사 | 동작이 예측 가능하고 디버깅이 쉬움 | 코드 복잡도와 복사 오버헤드 큼 |
| 관리형 통합 메모리 | 런타임이 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 이동 수행 | 프로그래밍 생산성 높음 | [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/) 가능성 |
| 완전 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) | 하드웨어가 [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) 유지 | 세밀한 상호작용, 포인터 공유 용이 | 트래픽·[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·복잡도 증가 |

이 주제는 비균일 메모리 접근 ([Non-Uniform Memory Access](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/), [NUMA](/knowledge-base/studynote/02_operating_system/06_memory_management/377_numa_allocation/))과도 연결된다. NUMA가 "같은 CPU 메모리라도 거리에 따라 다르다"는 사실을 알려 줬다면, 이종 메모리 공유는 그 범위를 CPU와 가속기 전체로 확장한 셈이다. 따라서 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)를 채택했다고 해서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 자동으로 좋아지는 것이 아니라, <strong>어느 장치가 주 사용자(owner)<a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a></strong>를 정하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 더 중요해진다.

또한 [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 같은 표준은 외부 장치와 [메모리 풀](/knowledge-base/studynote/02_operating_system/06_memory_management/369_memory_pool/)까지 이 그림에 포함시킨다. 즉 과거에는 CPU-장치 간 복사 최적화가 핵심이었다면, 이제는 장치·장치·[메모리 풀](/knowledge-base/studynote/02_operating_system/06_memory_management/369_memory_pool/) 사이를 아우르는 시스템 수준 공유 모델이 중요해지고 있다.

- **📢 섹션 요약 비유**: 명시적 복사는 종이를 복사해서 나눠 주는 회의이고, 관리형 통합 메모리는 비서가 알아서 자료를 옮겨 놓는 회의이며, 완전 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)는 모두가 같은 전자칠판을 보는 회의와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/) 자체보다 접근 패턴을 먼저 봐야 한다. CPU가 한 번 준비하고 GPU가 오래 읽기만 하는 일방향 파이프라인이면 명시적 복사나 핀 고정이 오히려 더 예측 가능할 수 있다. 반대로 CPU와 GPU가 [그래프](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) 구조나 인덱스를 번갈아 세밀하게 만지는 경우에는 공유 주소 공간과 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 지원이 큰 이점을 준다.

### 적용 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. <strong><a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a> 이동률</strong>: 동일 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 장치 사이를 계속 왕복하는가?
2. **주 사용자 결정**: 읽기 위주인지, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 위주인지, 어느 장치가 주 소유자인가?
3. **원격 접근 허용치**: 이동 대신 원격 접근을 허용할 때 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간이 감당 가능한가?
4. <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a>와 격리</strong>: [IOMMU](/knowledge-base/studynote/02_operating_system/10_security/627_iommu_dma_isolation/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 장치 오작동이나 악성 접근을 차단하는가?
5. **장애 범위**: 외부 [메모리 풀](/knowledge-base/studynote/02_operating_system/06_memory_management/369_memory_pool/)이나 링크 장애 시 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하와 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 전략이 준비돼 있는가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)를 켰다는 이유만으로 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 무차별적으로 공동 사용하게 만드는 설계
- CPU와 GPU가 같은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 번갈아 쓰게 만들어 마이그레이션 [스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)을 유발하는 접근 패턴
- 원격 메모리 계층을 로컬 메모리와 동일한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)으로 가정하는 용량 중심 설계

대표적인 구현으로는 온패키지 통합 메모리, CPU-[GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) 고속 코히어런트 링크, [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) 기반 [메모리 풀링](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/442_memory_pooling/)이 있다. 하지만 어떤 구현이든 공통된 판단 기준은 같다. <strong>공유 가능성보다 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 배치와 소유권 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>이 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 좌우한다</strong>는 점이다.

- **📢 섹션 요약 비유**: 이 기술을 잘 쓰려면 여러 사람이 같은 냉장고를 쓰더라도 누가 자주 꺼내는 음식은 앞칸에 두고, 가끔 쓰는 음식은 뒤칸에 두는 정리가 필요하다. 냉장고를 같이 쓴다고 아무 데나 넣으면 오히려 더 불편해진다.

---

## Ⅴ. 기대효과 및 결론

이종 컴퓨팅 메모리 공유가 잘 설계되면 장치 간 복사 비용이 줄고, 메모리 활용률이 높아지며, 개발자는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 코드보다 연산 구조 자체에 더 집중할 수 있다. 특히 대규모 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/), [그래프 분석](/knowledge-base/studynote/16_bigdata/05_analysis/114_graph_analytics/), 스트리밍 추론처럼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋이 크고 장치 간 협력이 잦은 환경에서 효과가 크다.

하지만 "공유"는 공짜가 아니다. [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 유지, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 이동, 원격 접근, [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 모두 추가 비용이며, 잘못 설계하면 명시적 복사보다 더 나쁜 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 낼 수도 있다. 따라서 앞으로의 방향은 모든 것을 완전 공유로 만드는 것보다, <strong>공유 주소 공간 위에서 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 배치와 소유권을 더 똑똑하게 제어하는 것</strong>에 가깝다.

결론적으로 이종 컴퓨팅 메모리 공유는 "메모리를 하나로 합치는 기술"이 아니라, <strong>여러 메모리 계층을 하나의 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a> 체계 안에서 다루게 만드는 기술</strong>로 기억해야 한다.

- **📢 섹션 요약 비유**: 이 기술은 창고를 하나로 합치는 공사가 아니라, 여러 창고를 한 지도 위에서 보고 가장 가까운 곳에서 물건을 꺼내 쓰게 만드는 물류 운영 시스템과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| 공유 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) (Shared [Virtual Memory](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)) | 장치가 같은 포인터를 이해하게 만드는 주소 체계의 기반이다. |
| 통합 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) (Unified [Virtual Memory](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)) | 런타임이 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 이동과 접근을 자동화하는 대표 모델이다. |
| [IOMMU](/knowledge-base/studynote/02_operating_system/10_security/627_iommu_dma_isolation/) | 장치의 주소 변환, 접근 제한, 격리를 담당한다. |
| 주소 변환 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (Address Translation Services) | 장치가 호스트 주소 변환 정보를 직접 활용하게 해 준다. |
| [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 마이그레이션 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 더 자주 쓰는 쪽으로 옮겨 평균 접근 비용을 줄인다. |
| [CXL](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/441_cxl/) | [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 공유와 [메모리 풀링](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/442_memory_pooling/)을 외부 장치까지 확장하는 표준 연결이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
장치별 분리 메모리 + 명시적 복사
    │
    ▼
공유 주소 공간
    │
    ▼
관리형 페이지 마이그레이션
    │
    ▼
코히어런트 CPU-GPU 링크
    │
    ▼
CXL 기반 메모리 풀링
    │
    ▼
정책 중심 이종 메모리 계층화
```

이 흐름은 "복사 중심 모델 → 주소 통합 → [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)·[풀링](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/) 확장"으로 이종 시스템 메모리 구조가 진화하는 방향을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 이 기술은 여러 친구가 같은 장난감 상자를 같이 쓰되, 굳이 자기 자리로 매번 옮기지 않아도 되게 해 주는 방법이에요.
2. 누가 자주 쓰는 장난감은 그 친구 가까이에 두고, 모두가 보는 이름표는 똑같이 붙여 둬요.
3. 그래서 장난감을 옮기느라 힘을 빼지 않고, 진짜 놀 시간에 더 많이 놀 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 516 / 803

← **이전**: [515. 작업 스케줄링 하드웨어 지원 (Hardware Support for Task Scheduling)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/515_hardware_task_scheduling/)
**다음**: [517. 거대 페이지 (Huge Page)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/517_huge_page/) →

---
