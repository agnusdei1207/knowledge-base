---
title: 516. 이종 컴퓨팅 메모리 공유 (Heterogeneous Memory Sharing)
date: '2026-04-20'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 이종 컴퓨팅 메모리 공유는 중앙 처리 장치 (Central Processing Unit, CPU)와 그래픽 처리 장치 ([[418_gpu|Graphics Processing Unit]], [[418_gpu|GPU]]) 같은 서로 다른 장치가 같은 [[001_dikw_pyramid|데이터]]에 대해 공통 주소 체계와 일관된 접근 규칙을 갖도록 만드는 기술이다.
> 2. **가치**: 장치 사이 복사와 재직렬화 비용을 줄여 제로 카피에 가까운 실행을 가능하게 하고, 개발자는 [[001_dikw_pyramid|데이터]]의 "논리적 위치"보다 "누가 더 가까이 쓰는가"에 집중할 수 있다.
> 3. **판단 포인트**: 공유 주소 공간이 곧 동일 [[015_지연_데이터_관점|지연]]시간을 뜻하지는 않으므로, [[286_page_frame|페이지]] 이동 비용·원격 접근 [[015_지연_데이터_관점|지연]]·[[402_cache_coherence|캐시 일관성]] 트래픽을 함께 고려해 소유권과 배치 [[164_policy|정책]]을 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

이종 컴퓨팅 메모리 공유는 CPU와 GPU처럼 구조가 다른 처리 장치가 [[001_dikw_pyramid|데이터]]를 각자 복사본으로 들고 다니는 대신, 하나의 주소 체계 또는 일관된 [[118_shared_memory|공유 메모리]] 뷰를 통해 접근하게 만드는 기술이다. 핵심은 단순히 주소를 같게 보이게 하는 것이 아니라, **누가 어떤 시점에 어떤 버전을 보고 있는지**를 시스템 차원에서 맞추는 데 있다.

이 기술이 중요해진 이유는 장치 간 [[001_dikw_pyramid|데이터]] 이동이 계산 자체보다 더 비싸지는 일이 많아졌기 때문이다. 전처리는 CPU, 학습·추론은 [[418_gpu|GPU]], 후처리는 다시 CPU가 담당하는 [[231_ai_turing_test|인공지능]] 파이프라인에서는 같은 텐서를 여러 번 복사하는 순간 대역폭과 전력이 급격히 낭비된다. 이종 메모리 공유는 이런 복사 왕복을 줄여 [[001_dikw_pyramid|데이터]] 이동을 병목이 아닌 배치 문제로 바꾸려는 시도다.

또한 메모리 용량 관점에서도 장점이 있다. 가속기 로컬 메모리가 부족할 때 시스템 메모리나 외부 [[369_memory_pool|메모리 풀]]을 함께 사용할 수 있고, 장치별로 조각나 있던 메모리를 더 유연하게 활용할 수 있다. 즉 이 기술의 목표는 "복사를 없애는 것"을 넘어, **서로 다른 메모리 계층을 하나의 협력 체계로 묶는 것**이다.

- **📢 섹션 요약 비유**: 이종 메모리 공유는 친구마다 따로 공책을 베껴 쓰는 대신, 모두가 같은 큰 화이트보드를 보며 필요한 자리에서 바로 읽고 쓰는 방식과 같다. 베껴 적는 시간이 줄어들면 진짜 문제 푸는 시간이 늘어난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

실제 구현은 크게 세 층으로 나뉜다. 첫째, 공유 [[381_virtual_memory|가상 메모리]] (Shared [[381_virtual_memory|Virtual Memory]], [[238_svm_margin_kernel_trick_naive_bayes|SVM]])나 통합 [[381_virtual_memory|가상 메모리]] (Unified [[381_virtual_memory|Virtual Memory]], UVM)처럼 같은 포인터를 장치들이 이해할 수 있게 하는 주소 체계가 필요하다. 둘째, 입출력 메모리 관리 장치 (Input/Output [[284_mmu|Memory Management Unit]], [[627_iommu_dma_isolation|IOMMU]])와 주소 변환 [[090_service_kubernetes_network_load_balancing|서비스]] (Address Translation Services, ATS)가 장치 쪽 주소 변환을 가능하게 해야 한다. 셋째, [[286_page_frame|페이지]] 이동과 [[402_cache_coherence|캐시 일관성]]을 다루는 [[164_policy|정책]] 계층이 필요하다. 이때 실제 [[001_dikw_pyramid|데이터]]는 동적 램 (Dynamic Random Access Memory, [[251_dram|DRAM]]), 고대역폭 메모리 ([[495_hbm|High Bandwidth Memory]], [[495_hbm|HBM]]), 컴퓨트 익스프레스 링크 ([[441_cxl|Compute Express Link]], [[441_cxl|CXL]]) 기반 외부 메모리 중 하나에 놓일 수 있다.

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

이 그림은 "같은 주소"와 "같은 물리 위치"가 다르다는 점을 강조한다. 프로그래머는 같은 포인터를 보더라도, 실제 [[001_dikw_pyramid|데이터]]는 CPU 가까운 동적 램, [[418_gpu|GPU]] 가까운 고대역폭 메모리, 혹은 컴퓨트 익스프레스 링크 ([[441_cxl|Compute Express Link]], [[441_cxl|CXL]]) 기반 [[369_memory_pool|메모리 풀]] 가운데 하나에 놓일 수 있다.

| 메커니즘 | 역할 | 주의점 |
| :-- | :-- | :-- |
| [[238_svm_margin_kernel_trick_naive_bayes|SVM]] / UVM | 장치들이 같은 가상 주소를 이해하게 함 | 주소가 같아도 접근 비용은 다를 수 있음 |
| [[627_iommu_dma_isolation|IOMMU]] / ATS | 장치 측 주소 변환과 [[571_protection_vs_security|보호]] 수행 | [[286_page_frame|페이지]] 워크와 변환 캐시 미스 비용 존재 |
| [[286_page_frame|페이지]] 마이그레이션 | [[001_dikw_pyramid|데이터]]를 더 자주 쓰는 장치 쪽으로 이동 | 핑퐁 이동이 발생하면 오히려 느려짐 |
| [[194_consistency_database_integrity|일관성]] 링크 | 캐시 간 최신 상태를 맞춤 | 트래픽과 [[015_지연_데이터_관점|지연]]이 증가할 수 있음 |
| [[442_memory_pooling|메모리 풀링]] | 장치 로컬 메모리 부족을 외부 용량으로 보완 | 원격 메모리 [[015_지연_데이터_관점|지연]] 관리 필요 |

즉 이종 메모리 공유의 핵심 원리는 "복사하지 않고 접근한다"가 아니라, **복사·원격 접근·마이그레이션 중 무엇이 가장 싼지 동적으로 고르는 것**에 더 가깝다.

- **📢 섹션 요약 비유**: 이 구조는 같은 주소가 적힌 택배 상자를 중앙 창고, 가까운 창고, 임시 보관소 중 어디에 둘지 계속 조정하는 물류 시스템과 같다. 상자 이름은 같아도 꺼내 오는 거리는 다르다.

---

## Ⅲ. 비교 및 연결

이종 컴퓨팅 메모리 공유를 이해할 때 가장 중요한 비교는 명시적 복사 모델, 관리형 통합 메모리, 완전 [[194_consistency_database_integrity|일관성]] [[118_shared_memory|공유 메모리]]의 차이다. 세 방식은 모두 "장치 간 [[001_dikw_pyramid|데이터]] 사용"을 다루지만, [[282_performance_tactics|성능]] 특성과 프로그래밍 비용이 다르다.

| 모델 | [[001_dikw_pyramid|데이터]] 이동 방식 | 장점 | 한계 |
| :-- | :-- | :-- | :-- |
| 명시적 복사 모델 | 애플리케이션이 직접 복사 | 동작이 예측 가능하고 디버깅이 쉬움 | 코드 복잡도와 복사 오버헤드 큼 |
| 관리형 통합 메모리 | 런타임이 [[286_page_frame|페이지]] 이동 수행 | 프로그래밍 생산성 높음 | [[286_page_frame|페이지]] [[257_thrashing|스래싱]] 가능성 |
| 완전 [[194_consistency_database_integrity|일관성]] [[118_shared_memory|공유 메모리]] | 하드웨어가 [[402_cache_coherence|캐시 일관성]] 유지 | 세밀한 상호작용, 포인터 공유 용이 | 트래픽·[[015_지연_데이터_관점|지연]]·복잡도 증가 |

이 주제는 비균일 메모리 접근 ([[377_numa_allocation|Non-Uniform Memory Access]], [[377_numa_allocation|NUMA]])과도 연결된다. NUMA가 "같은 CPU 메모리라도 거리에 따라 다르다"는 사실을 알려 줬다면, 이종 메모리 공유는 그 범위를 CPU와 가속기 전체로 확장한 셈이다. 따라서 [[118_shared_memory|공유 메모리]]를 채택했다고 해서 [[282_performance_tactics|성능]]이 자동으로 좋아지는 것이 아니라, **어느 장치가 주 사용자(owner)[[509_authorization_models_rbac_abac|인가]]**를 정하는 [[164_policy|정책]]이 더 중요해진다.

또한 [[441_cxl|CXL]] 같은 표준은 외부 장치와 [[369_memory_pool|메모리 풀]]까지 이 그림에 포함시킨다. 즉 과거에는 CPU-장치 간 복사 최적화가 핵심이었다면, 이제는 장치·장치·[[369_memory_pool|메모리 풀]] 사이를 아우르는 시스템 수준 공유 모델이 중요해지고 있다.

- **📢 섹션 요약 비유**: 명시적 복사는 종이를 복사해서 나눠 주는 회의이고, 관리형 통합 메모리는 비서가 알아서 자료를 옮겨 놓는 회의이며, 완전 [[194_consistency_database_integrity|일관성]] [[118_shared_memory|공유 메모리]]는 모두가 같은 전자칠판을 보는 회의와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [[118_shared_memory|공유 메모리]] 자체보다 접근 패턴을 먼저 봐야 한다. CPU가 한 번 준비하고 GPU가 오래 읽기만 하는 일방향 파이프라인이면 명시적 복사나 핀 고정이 오히려 더 예측 가능할 수 있다. 반대로 CPU와 GPU가 [[070_graph_datastructure|그래프]] 구조나 인덱스를 번갈아 세밀하게 만지는 경우에는 공유 주소 공간과 [[194_consistency_database_integrity|일관성]] 지원이 큰 이점을 준다.

### 적용 [[435_checklist_based_testing|체크리스트]]

1. **[[286_page_frame|페이지]] 이동률**: 동일 [[286_page_frame|페이지]]가 장치 사이를 계속 왕복하는가?
2. **주 사용자 결정**: 읽기 위주인지, [[289_cqrs_db|쓰기]] 위주인지, 어느 장치가 주 소유자인가?
3. **원격 접근 허용치**: 이동 대신 원격 접근을 허용할 때 [[015_지연_데이터_관점|지연]]시간이 감당 가능한가?
4. **[[571_protection_vs_security|보호]]와 격리**: [[627_iommu_dma_isolation|IOMMU]] [[164_policy|정책]]으로 장치 오작동이나 악성 접근을 차단하는가?
5. **장애 범위**: 외부 [[369_memory_pool|메모리 풀]]이나 링크 장애 시 [[282_performance_tactics|성능]] 저하와 [[658_ir_recovery|복구]] 전략이 준비돼 있는가?

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[118_shared_memory|공유 메모리]]를 켰다는 이유만으로 모든 [[001_dikw_pyramid|데이터]] 구조를 무차별적으로 공동 사용하게 만드는 설계
- CPU와 GPU가 같은 [[286_page_frame|페이지]]를 번갈아 쓰게 만들어 마이그레이션 [[257_thrashing|스래싱]]을 유발하는 접근 패턴
- 원격 메모리 계층을 로컬 메모리와 동일한 [[282_performance_tactics|성능]]으로 가정하는 용량 중심 설계

대표적인 구현으로는 온패키지 통합 메모리, CPU-[[418_gpu|GPU]] 고속 코히어런트 링크, [[441_cxl|CXL]] 기반 [[442_memory_pooling|메모리 풀링]]이 있다. 하지만 어떤 구현이든 공통된 판단 기준은 같다. **공유 가능성보다 [[001_dikw_pyramid|데이터]] 배치와 소유권 [[164_policy|정책]]이 [[282_performance_tactics|성능]]을 좌우한다**는 점이다.

- **📢 섹션 요약 비유**: 이 기술을 잘 쓰려면 여러 사람이 같은 냉장고를 쓰더라도 누가 자주 꺼내는 음식은 앞칸에 두고, 가끔 쓰는 음식은 뒤칸에 두는 정리가 필요하다. 냉장고를 같이 쓴다고 아무 데나 넣으면 오히려 더 불편해진다.

---

## Ⅴ. 기대효과 및 결론

이종 컴퓨팅 메모리 공유가 잘 설계되면 장치 간 복사 비용이 줄고, 메모리 활용률이 높아지며, 개발자는 [[001_dikw_pyramid|데이터]] [[016_replication_factor|복제]] 코드보다 연산 구조 자체에 더 집중할 수 있다. 특히 대규모 [[231_ai_turing_test|인공지능]], [[114_graph_analytics|그래프 분석]], 스트리밍 추론처럼 [[001_dikw_pyramid|데이터]]셋이 크고 장치 간 협력이 잦은 환경에서 효과가 크다.

하지만 "공유"는 공짜가 아니다. [[194_consistency_database_integrity|일관성]] 유지, [[286_page_frame|페이지]] 이동, 원격 접근, [[571_protection_vs_security|보호]] [[164_policy|정책]]이 모두 추가 비용이며, 잘못 설계하면 명시적 복사보다 더 나쁜 [[282_performance_tactics|성능]]을 낼 수도 있다. 따라서 앞으로의 방향은 모든 것을 완전 공유로 만드는 것보다, **공유 주소 공간 위에서 [[001_dikw_pyramid|데이터]] 배치와 소유권을 더 똑똑하게 제어하는 것**에 가깝다.

결론적으로 이종 컴퓨팅 메모리 공유는 "메모리를 하나로 합치는 기술"이 아니라, **여러 메모리 계층을 하나의 [[164_policy|정책]] 체계 안에서 다루게 만드는 기술**로 기억해야 한다.

- **📢 섹션 요약 비유**: 이 기술은 창고를 하나로 합치는 공사가 아니라, 여러 창고를 한 지도 위에서 보고 가장 가까운 곳에서 물건을 꺼내 쓰게 만드는 물류 운영 시스템과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| 공유 [[381_virtual_memory|가상 메모리]] (Shared [[381_virtual_memory|Virtual Memory]]) | 장치가 같은 포인터를 이해하게 만드는 주소 체계의 기반이다. |
| 통합 [[381_virtual_memory|가상 메모리]] (Unified [[381_virtual_memory|Virtual Memory]]) | 런타임이 [[286_page_frame|페이지]] 이동과 접근을 자동화하는 대표 모델이다. |
| [[627_iommu_dma_isolation|IOMMU]] | 장치의 주소 변환, 접근 제한, 격리를 담당한다. |
| 주소 변환 [[090_service_kubernetes_network_load_balancing|서비스]] (Address Translation Services) | 장치가 호스트 주소 변환 정보를 직접 활용하게 해 준다. |
| [[286_page_frame|페이지]] 마이그레이션 | [[001_dikw_pyramid|데이터]]를 더 자주 쓰는 쪽으로 옮겨 평균 접근 비용을 줄인다. |
| [[441_cxl|CXL]] | [[194_consistency_database_integrity|일관성]] 공유와 [[442_memory_pooling|메모리 풀링]]을 외부 장치까지 확장하는 표준 연결이다. |

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

이 흐름은 "복사 중심 모델 → 주소 통합 → [[194_consistency_database_integrity|일관성]]·[[285_pooling_layer|풀링]] 확장"으로 이종 시스템 메모리 구조가 진화하는 방향을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 이 기술은 여러 친구가 같은 장난감 상자를 같이 쓰되, 굳이 자기 자리로 매번 옮기지 않아도 되게 해 주는 방법이에요.
2. 누가 자주 쓰는 장난감은 그 친구 가까이에 두고, 모두가 보는 이름표는 똑같이 붙여 둬요.
3. 그래서 장난감을 옮기느라 힘을 빼지 않고, 진짜 놀 시간에 더 많이 놀 수 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 516 / 803

← **이전**: [[515_hardware_task_scheduling|515. 작업 스케줄링 하드웨어 지원 (Hardware Support for Task Scheduling)]]
**다음**: [[517_huge_page|517. 거대 페이지 (Huge Page)]] →

---
