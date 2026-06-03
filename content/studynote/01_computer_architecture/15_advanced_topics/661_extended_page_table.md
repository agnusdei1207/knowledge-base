---
title: 661. 확장 페이지 테이블 (Extended Page Table, EPT)
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 확장 [[353_page_table|페이지 테이블]] (Extended [[353_page_table|Page Table]], EPT)은 게스트 [[323_physical_address|물리 주소]]를 호스트 [[323_physical_address|물리 주소]]로 바꾸는 2차 주소 변환을 [[054_hypervisor|하이퍼바이저]] 대신 하드웨어가 수행하게 만든 인텔 메모리 [[015_virtualization|가상화]] 장치다.
> 2. **가치**: 게스트 운영체제가 자신의 [[353_page_table|페이지 테이블]]을 자주 수정해도 [[054_hypervisor|하이퍼바이저]]가 매번 끼어들지 않아, 메모리 집약형 가상 머신의 제어 전환 비용을 크게 줄인다.
> 3. **판단 포인트**: EPT는 관리 오버헤드를 없애는 대신 [[286_page_frame|페이지]] 워크가 길어질 수 있으므로, 주소 변환 캐시 ([[291_tlb|Translation Lookaside Buffer]], [[357_tlb|TLB]]), 대용량 [[286_page_frame|페이지]], 가상 프로세서 [[289_identification_flags_fragmentation_offset|식별자]] (Virtual Processor [[088_identifier_in_er_model|Identifier]], VPID) 같은 보완책까지 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

확장 [[353_page_table|페이지 테이블]] (Extended [[353_page_table|Page Table]], EPT)은 인텔 [[015_virtualization|가상화]] 확장 VT-x (Intel [[190_virtualization_computing_architecture_cloud|Virtualization]] Technology for x86) 환경에서 게스트 가상 주소 (Guest Virtual Address, GVA)가 게스트 [[323_physical_address|물리 주소]] (Guest [[323_physical_address|Physical Address]], GPA)로 바뀐 뒤, 다시 호스트 [[323_physical_address|물리 주소]] (Host [[323_physical_address|Physical Address]], [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]])로 연결되는 과정을 하드웨어가 직접 이어 주는 2차 주소 변환 계층이다. [[015_virtualization|가상화]] 초창기에는 이 두 번째 변환을 [[054_hypervisor|하이퍼바이저]]가 소프트웨어로 관리해야 했고, 게스트 운영체제가 [[353_page_table|페이지 테이블]]을 손볼 때마다 제어권이 계속 밖으로 빠져 [[282_performance_tactics|성능]]이 크게 흔들렸다. 특히 [[002_database_definition|데이터베이스]], 자바 가상 머신, 인메모리 캐시처럼 [[286_page_frame|페이지]] 접근이 많고 [[307_memory_protection|메모리 보호]] [[073_bit|비트]] 변경도 잦은 워크로드에서는 주소 변환 자체보다 “변환 정보를 유지하는 일”이 더 큰 병목이 되었다.

이 그림은 EPT가 왜 중요한지, 그리고 어떤 책임을 하드웨어로 넘겼는지를 보여준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                EPT가 해결한 문제: 소프트웨어 개입 없는 2차 변환           │
├────────────────────────────────────────────────────────────────────────────┤
│ GVA ──▶ Guest Page Table ──▶ GPA ──▶ EPT ──▶ HPA ──▶ 실제 메모리          │
│       (게스트 운영체제 관리)        (Hypervisor가 정의, MMU가 실행)       │
│                                                                            │
│ 기존 방식: GPA→HPA를 Hypervisor 코드가 계산                               │
│ EPT 방식 : GPA→HPA를 MMU (Memory Management Unit)가 직접 계산             │
└────────────────────────────────────────────────────────────────────────────┘
```

핵심은 역할 분리다. 게스트 운영체제는 원래 하던 대로 자신의 주소 공간만 관리하고, [[054_hypervisor|하이퍼바이저]]는 실제 메모리를 어느 GPA에 연결할지만 정의한다. 그러면 메모리 관리 장치 ([[284_mmu|Memory Management Unit]], [[328_mmu|MMU]])는 두 장의 지도를 이어 읽어 최종 주소를 만든다. 결과적으로 [[015_virtualization|가상화]]의 본질은 유지하면서도, 주소 변환을 위해 [[054_hypervisor|하이퍼바이저]]가 매번 호출되는 비효율을 줄일 수 있다.

- **📢 섹션 요약 비유**: EPT는 아파트 단지 안내도와 도시 지도를 한 번에 겹쳐 보는 내비게이션과 같다. 입주민은 자기 동만 알면 되고, 내비게이션이 실제 도로 주소까지 자동으로 이어 준다.

---

## Ⅱ. 아키텍처 및 핵심 원리

EPT의 핵심 구성은 게스트 [[353_page_table|페이지 테이블]], EPT 포인터 (Extended [[353_page_table|Page Table]] Pointer, EPTP), EPT 계층 엔트리, 그리고 이 결과를 기억하는 TLB로 나뉜다. 게스트 운영체제는 여전히 GVA→GPA 변환용 [[353_page_table|페이지 테이블]]을 관리한다. [[054_hypervisor|하이퍼바이저]]는 GPA→[[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] 관계를 담은 EPT를 만들고, 해당 루트 주소를 가상 머신 제어 구조 ([[598_vm_migration_nic|Virtual Machine]] Control Structure, [[529_vmcs|VMCS]])에 있는 EPTP에 기록한다. 이후 중앙 처리 장치 (Central Processing Unit, CPU)는 주소 변환이 필요할 때 게스트 테이블과 EPT를 연쇄적으로 따라간다.

| 구성요소 | 역할 | [[282_performance_tactics|성능]]상 의미 |
| :-- | :-- | :-- |
| 게스트 [[353_page_table|페이지 테이블]] | GVA를 GPA로 변환 | 게스트 운영체제가 자유롭게 관리 |
| EPTP | EPT 루트 주소 지정 | 가상 머신 전환 시 어떤 EPT를 쓸지 결정 |
| EPT 엔트리 | GPA를 HPA와 권한으로 매핑 | 읽기/[[289_cqrs_db|쓰기]]/실행 권한을 하드웨어가 즉시 검사 |
| [[357_tlb|TLB]] | GVA→[[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] 결과 캐시 | 긴 [[286_page_frame|페이지]] 워크 비용을 숨기는 핵심 |
| 대용량 [[286_page_frame|페이지]] | 2 메비바이트, 1 기비바이트 단위 매핑 | 단계 수와 [[357_tlb|TLB]] 미스를 함께 줄임 |

주소 변환 흐름은 단순하지만 내부 비용은 결코 가볍지 않다. 게스트 [[353_page_table|페이지 테이블]]의 각 단계를 읽기 위해서도 해당 테이블 [[286_page_frame|페이지]]의 GPA를 다시 EPT로 번역해야 하기 때문이다. 그래서 TLB가 비어 있고 4단계 테이블을 모두 따라가야 하는 최악의 경우에는 20회가 넘는 메모리 참조가 연쇄적으로 발생할 수 있다. EPT가 빠른 이유는 “워크가 짧아서”가 아니라, 이 긴 경로를 [[054_hypervisor|하이퍼바이저]] 개입 없이 하드웨어가 직접 처리하고, 그 결과를 TLB가 재사용하기 때문이다.

또한 EPT 엔트리에는 읽기, [[289_cqrs_db|쓰기]], 실행 권한이 분리되어 있어 [[054_hypervisor|하이퍼바이저]]가 특정 게스트 [[286_page_frame|페이지]]를 읽기 전용이나 실행 금지로 지정할 수 있다. 이 덕분에 단순한 메모리 매핑뿐 아니라 메모리 감시, 격리 강화, [[629_live_migration_pre_copy|라이브 마이그레이션]]용 변경 추적과도 연결된다. 인텔 플랫폼에서는 [[286_page_frame|페이지]] 수정 로깅 ([[286_page_frame|Page]] Modification [[526_security_logging_and_monitoring_failures|Logging]], PML) 같은 기능과 결합해 “어떤 [[286_page_frame|페이지]]가 바뀌었는가”를 하드웨어가 보조 기록하도록 만들 수 있다.

- **📢 섹션 요약 비유**: EPT는 도서관 사서가 서가 위치표와 창고 위치표를 동시에 읽는 일과 같다. 찾는 과정은 길어 보여도, 사서가 직접 바로 찾아주니 매번 관장실에 문의하러 갈 필요가 없다.

---

## Ⅲ. 비교 및 연결

EPT를 제대로 이해하려면 [[662_shadow_page_table|그림자 페이지 테이블]] ([[626_shadow_page_table_vs_ept|Shadow Page Table]])과 [[660_nested_page_table|중첩 페이지 테이블]] ([[660_nested_page_table|Nested Page Table]], NPT)을 함께 봐야 한다. [[662_shadow_page_table|그림자 페이지 테이블]]은 [[054_hypervisor|하이퍼바이저]]가 GVA→[[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] 결과를 미리 합성해 두는 방식이라, 한 번 주소가 정리되면 단일 [[286_page_frame|페이지]] 워크로 끝날 수 있다. 하지만 게스트가 [[353_page_table|페이지 테이블]]을 바꾸는 순간 [[054_hypervisor|하이퍼바이저]]가 다시 [[212_synchronization_mechanisms|동기화]]해야 하므로 유지 비용이 매우 크다. 반면 EPT와 NPT는 워크 자체는 길어도 [[212_synchronization_mechanisms|동기화]] 부담을 하드웨어 설계로 바꾸어 대규모 클라우드에 더 적합한 구조를 만든다.

| 비교 항목 | [[662_shadow_page_table|그림자 페이지 테이블]] | EPT | NPT |
| :-- | :-- | :-- | :-- |
| 구현 주체 | [[054_hypervisor|하이퍼바이저]] 소프트웨어 | 인텔 프로세서 하드웨어 | Advanced Micro Devices (AMD) 플랫폼 하드웨어 |
| 주소 변환 방식 | 합성된 GVA→[[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] 단일 테이블 | GVA→GPA→[[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] 2단계 | GVA→GPA→[[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] 2단계 |
| 게스트 [[353_page_table|페이지 테이블]] 수정 | 자주 [[677_trap_based_system_call_implementation|트랩]] 발생 | 게스트가 비교적 자유롭게 수정 | 게스트가 비교적 자유롭게 수정 |
| 유지 복잡도 | 매우 높음 | 중간 | 중간 |
| 대표 강점 | 강한 관찰성과 구형 CPU [[344_compatibility_usability|호환성]] | 범용 서버 [[015_virtualization|가상화]] 표준 | AMD 환경 최적화 |

연결 개념으로는 입출력 메모리 관리 장치 (Input/Output [[284_mmu|Memory Management Unit]], [[627_iommu_dma_isolation|IOMMU]])를 함께 기억하면 좋다. EPT가 CPU가 사용하는 주소 변환을 가속한다면, IOMMU는 장치의 [[450_dma_direct_memory_access|직접 메모리 접근]] ([[318_dma|Direct Memory Access]], [[746_io_direct_memory_access_dma|DMA]]) 경로를 격리하고 번역한다. 즉 CPU 쪽 메모리 [[015_virtualization|가상화]]는 EPT, 장치 쪽 메모리 [[015_virtualization|가상화]]는 IOMMU가 맡는 셈이다. 둘이 함께 있어야 가상 머신이 메모리와 장치를 모두 안전하게 공유할 수 있다.

- **📢 섹션 요약 비유**: [[662_shadow_page_table|그림자 페이지 테이블]]이 손으로 그린 맞춤 지름길이라면, EPT는 자동 경로 계산기다. 매번 새 길을 다시 그릴 필요는 없지만, 계산기를 빠르게 쓰려면 캐시와 축약 경로가 중요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 EPT는 “켜면 끝”인 옵션이 아니라, 메모리 [[164_policy|정책]] 전체와 함께 봐야 하는 토대 기술이다. 예를 들어 가상 머신 밀도를 높이려고 메모리 오버커밋을 과도하게 걸면, EPT가 빨라도 호스트 스와핑이 시작되는 순간 전체 이점이 무너진다. 반대로 대용량 [[286_page_frame|페이지]]를 정렬해 주고 VPID를 활성화하며, EPT 변경이 잦은 기능을 최소화하면 같은 하드웨어에서도 [[141_latency|지연 시간]] 분산이 눈에 띄게 줄어든다.

### [[435_checklist_based_testing|체크리스트]]

1. 메모리 집약형 워크로드라면 EPT와 대용량 [[286_page_frame|페이지]]를 함께 적용했는가?
2. 자주 재배치되는 [[286_page_frame|페이지]]가 많다면 PML, Accessed/Dirty [[073_bit|비트]], 마이그레이션 [[164_policy|정책]]을 같이 설계했는가?
3. VPID와 [[357_tlb|TLB]] 플러시 [[164_policy|정책]]을 확인해 가상 머신 전환 때 캐시 이점을 잃지 않는가?
4. 보안 감시 목적으로 EPT 위반을 활용한다면, 감시 정확도와 추가 [[015_지연_데이터_관점|지연]]을 함께 계산했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 디버깅 편의를 위해 [[662_shadow_page_table|그림자 페이지 테이블]]로 되돌려 놓고 [[282_performance_tactics|성능]] 저하 원인을 EPT 탓으로 돌리는 것
- 게스트는 대용량 [[286_page_frame|페이지]]를 쓰는데 호스트 EPT는 잘게 쪼개어 [[357_tlb|TLB]] 도달 범위를 스스로 줄이는 것
- 메모리 벌루닝과 잦은 EPT 무효화가 동시에 일어나는 환경에서 [[141_latency|지연 시간]] 급증을 무시하는 것

기술사 관점의 판단은 명확하다. 범용 서버 [[015_virtualization|가상화]], 클라우드, 경량 가상 머신에서는 EPT가 사실상 기본값이다. 다만 보안 감시나 특수 디버깅처럼 “[[282_performance_tactics|성능]]보다 관찰 가능성”이 중요한 일부 경우에는 일부러 더 느린 방법을 선택할 수도 있다. 결국 질문은 “EPT가 좋은가?”가 아니라 “EPT의 장점을 살릴 메모리 운영 [[164_policy|정책]]을 갖췄는가?”다.

- **📢 섹션 요약 비유**: EPT는 잘 설계된 고속도로다. 도로 자체가 좋아도 톨게이트를 자주 세우고 진출입로를 어지럽게 만들면 막히는 것처럼, 주변 운영 [[164_policy|정책]]이 [[282_performance_tactics|성능]]을 결정한다.

---

## Ⅴ. 기대효과 및 결론

EPT의 가장 큰 기대효과는 메모리 [[015_virtualization|가상화]]를 소프트웨어 장부 관리에서 하드웨어 [[286_page_frame|페이지]] 워킹으로 옮긴 데 있다. 이 전환 덕분에 게스트 운영체제는 자신의 메모리 [[164_policy|정책]]을 거의 그대로 유지하면서도, 호스트는 다수의 가상 머신을 비교적 낮은 오버헤드로 수용할 수 있다. 특히 웹 서버, [[002_database_definition|데이터베이스]], [[561_container_based_deployment|컨테이너]] 호스트처럼 메모리 접근 패턴이 다양하고 가상 머신 수가 많은 환경에서 EPT는 [[282_performance_tactics|성능]]뿐 아니라 운영 안정성까지 높인다.

물론 한계도 있다. [[357_tlb|TLB]] 미스가 잦은 랜덤 접근, 중첩 [[015_virtualization|가상화]], 과도한 메모리 압박 상황에서는 EPT도 분명히 비용을 드러낸다. 그래서 EPT를 기억할 때는 “마법 같은 가속 기능”이 아니라, “메모리 [[015_virtualization|가상화]]의 병목 위치를 [[054_hypervisor|하이퍼바이저]] 코드에서 MMU와 캐시 계층으로 옮긴 기술”로 이해하는 것이 정확하다.

- **📢 섹션 요약 비유**: EPT는 계산을 대신해 주는 숙련된 계산원과 같다. 사람이 장부를 일일이 맞추는 시대는 끝났지만, 계산원이 빨라지려면 계산표와 메모장도 잘 정리되어 있어야 한다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[529_vmcs|VMCS]] ([[598_vm_migration_nic|Virtual Machine]] Control Structure) | 현재 가상 머신이 사용할 EPTP를 보관하는 제어 구조 |
| [[357_tlb|TLB]] | 긴 2차 [[286_page_frame|페이지]] 워크 결과를 캐시해 EPT의 실효 [[282_performance_tactics|성능]]을 좌우 |
| 대용량 [[286_page_frame|페이지]] | EPT 단계 수와 [[357_tlb|TLB]] 미스를 줄여 메모리 집약형 VM에 유리 |
| PML | 수정된 [[286_page_frame|페이지]]를 추적해 [[629_live_migration_pre_copy|라이브 마이그레이션]] 효율을 높임 |
| [[627_iommu_dma_isolation|IOMMU]] | CPU 쪽 EPT와 짝을 이루어 장치의 메모리 접근을 [[015_virtualization|가상화]] |

### 📈 관련 키워드 및 발전 흐름도

```text
그림자 페이지 테이블
    │  (소프트웨어 합성)
    ▼
2차 주소 변환 하드웨어화
    │
    ▼
EPT · NPT
    │
    ▼
TLB 최적화 · 대용량 페이지 · VPID
    │
    ▼
PML · IOMMU · 보안 감시형 메모리 가상화
```

이 흐름은 메모리 [[015_virtualization|가상화]]가 “소프트웨어 [[212_synchronization_mechanisms|동기화]]”에서 “하드웨어 가속과 운영 최적화”로 중심축이 이동한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. EPT는 컴퓨터가 두 장의 지도를 겹쳐서 진짜 집 주소를 찾게 해 주는 똑똑한 길찾기예요.
2. 예전에는 선생님이 매번 옆에서 주소를 다시 적어줘야 했지만, 이제는 컴퓨터가 스스로 길을 찾아요.
3. 다만 길찾기 책이 너무 두껍다면, 자주 쓰는 길은 따로 기억해 두어야 더 빨라진답니다.
