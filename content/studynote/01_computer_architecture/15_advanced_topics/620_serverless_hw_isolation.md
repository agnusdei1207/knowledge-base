---
title: 620. 서버리스 컴퓨팅 컨테이너 분리 하드웨어 기술
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[150_serverless_computing_faas|서버리스 컴퓨팅]] ([[206_serverless_cold_start|Serverless]] Computing)에서 [[561_container_based_deployment|컨테이너]] 분리 하드웨어 기술은 함수 실행 단위를 마이크로 가상 머신 (Micro [[598_vm_migration_nic|Virtual Machine]], MicroVM)이나 유사 격리 경계로 감싸고, CPU [[015_virtualization|가상화]]·이중 주소 변환·장치 접근 제어를 하드웨어가 맡게 해 공유 [[022_kernel_role|커널]] 위험을 줄이는 방식이다.
> 2. **가치**: [[658_intel_vtx|Intel VT-x]] / [[659_amd_v|AMD-V]], [[661_extended_page_table|확장 페이지 테이블]] (Extended [[286_page_frame|Page]] Tables, EPT) / [[660_nested_page_table|중첩 페이지 테이블]] (Nested [[286_page_frame|Page]] Tables, NPT), 입출력 메모리 관리 장치 (Input/Output [[284_mmu|Memory Management Unit]], [[627_iommu_dma_isolation|IOMMU]]), 경량 virtio 장치, [[637_zfs_snapshot_cow_architecture|snapshot]] 재개 기법을 결합하면 가상 머신 ([[598_vm_migration_nic|Virtual Machine]], [[598_vm_migration_nic|VM]])급 격리와 [[561_container_based_deployment|컨테이너]]급 기동 속도 사이의 균형점을 만들 수 있다.
> 3. **판단 포인트**: [[206_serverless_cold_start|서버리스]] 격리 설계는 시작 지연시간만 볼 일이 아니라 멀티테넌시 신뢰 경계, 장치 공유 방식, [[796_memory_encryption|메모리 암호화]] 비용, [[637_zfs_snapshot_cow_architecture|snapshot]] 위생, 부채널 노출까지 함께 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

[[206_serverless_cold_start|서버리스]]는 사용자가 서버를 직접 관리하지 않고 코드 조각만 올리면, 플랫폼이 필요할 때 실행 환경을 만들어 주는 구조다. 이때 가장 어려운 문제는 낯선 사용자들의 코드를 같은 물리 서버에서 빠르게 실행시키면서도 서로 침범하지 못하게 막는 일이다. 일반 [[561_container_based_deployment|컨테이너]]는 가볍고 빠르지만 [[001_operating_system_purpose|운영체제]] [[022_kernel_role|커널]]을 공유하므로, [[022_kernel_role|커널]] 취약점이 생기면 테넌트 간 경계가 무너질 수 있다.

반대로 전통적인 가상 머신은 경계가 강하지만, [[206_serverless_cold_start|서버리스]]처럼 수천 개의 짧은 실행을 처리하기에는 시작 비용과 장치 에뮬레이션 부담이 크다. 그래서 [[206_serverless_cold_start|서버리스]] 플랫폼은 "[[561_container_based_deployment|컨테이너]]처럼 빠르되 VM처럼 안전한 경계"를 원하게 되었고, 그 결과 마이크로VM, 하드웨어 지원 [[015_virtualization|가상화]], 최소 장치 모델, [[637_zfs_snapshot_cow_architecture|snapshot]] 기반 재개가 결합한 경량 격리 기술이 발전했다.

즉 [[206_serverless_cold_start|서버리스]] [[561_container_based_deployment|컨테이너]] 분리 하드웨어 기술의 핵심은 보안을 위해 무거운 격리를 쓰는 것이 아니라, **하드웨어가 비싼 경계를 빠르게 만들어 주게 하는 것**이다. 이 균형이 맞아야 공용 [[342_faas|FaaS]] (Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) 플랫폼이 경제성과 안전성을 동시에 얻는다.

- **📢 섹션 요약 비유**: [[206_serverless_cold_start|서버리스]] 격리는 호텔 객실을 1초 만에 만들어 손님을 들이는 일과 같다. 방은 빨리 준비돼야 하지만, 벽이 얇아서 옆방이 들여다보이면 호텔 자체가 성립하지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

현대 [[206_serverless_cold_start|서버리스]] 격리는 보통 사용자 함수 이미지를 바로 리눅스 프로세스로 띄우지 않고, 최소 장치만 가진 MicroVM 안에서 실행한다. 이때 하이퍼바이저는 매우 얇고, 실제 격리 강도는 CPU의 guest 실행 모드, EPT/NPT 기반 2단계 주소 변환, [[627_iommu_dma_isolation|IOMMU]] 기반 [[746_io_direct_memory_access_dma|DMA]] 차단, [[016_interrupt_mechanism|인터럽트]] [[015_virtualization|가상화]], 최소 virtio 장치 모델이 제공한다. 여기에 미리 준비된 snapshot을 복원해 cold start를 줄이는 방식이 많이 쓰인다.

| 구성 요소 | 역할 | 설계 포인트 |
| :-- | :-- | :-- |
| MicroVM [[229_monitor|모니터]] | 함수 실행 단위를 최소 VM으로 관리 | 장치 수가 적을수록 부팅 경로가 짧아진다. |
| VT-x / [[659_amd_v|AMD-V]] | guest 실행 모드 제공 | 일반 명령은 직접 실행하고 민감 동작만 제어해야 효율적이다. |
| EPT / NPT | 게스트 메모리 주소를 하드웨어가 2단계 변환 | 공유 [[022_kernel_role|커널]]보다 강한 메모리 경계를 낮은 오버헤드로 제공한다. |
| [[627_iommu_dma_isolation|IOMMU]] | 장치 DMA가 다른 테넌트 메모리를 침범하지 못하게 차단 | [[587_nic_offloading|NIC]], 가속기, 스토리지 공유 시 필수적이다. |
| Virtio 최소 장치 모델 | 네트워크·블록 장치를 단순하게 제공 | 복잡한 에뮬레이션을 줄여 시작 지연과 공격면을 함께 낮춘다. |
| [[637_zfs_snapshot_cow_architecture|Snapshot]] / Restore | 미리 초기화한 실행 상태를 재사용 | cold start를 줄이되, [[637_zfs_snapshot_cow_architecture|snapshot]] 오염과 비밀 누설을 막아야 한다. |
| [[796_memory_encryption|메모리 암호화]] 계열 기능 | 호스트 수준 위협까지 완화 | 보안은 높지만 밀집도와 디버깅 비용이 늘 수 있다. |

이 그림은 [[206_serverless_cold_start|서버리스]]에서 하드웨어 격리 경계가 어디에 놓이는지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│            서버리스 하드웨어 격리: 빠른 시작과 강한 경계를 동시에 확보      │
├────────────────────────────────────────────────────────────────────────────┤
│ Function Image / Snapshot Pool                                            │
│             │                                                              │
│             ▼                                                              │
│      [MicroVM Manager / Jailer]                                            │
│         │            │            │                                         │
│         ▼            ▼            ▼                                         │
│     Tenant A      Tenant B      Tenant C                                   │
│     MicroVM       MicroVM       MicroVM                                    │
│         │            │            │                                         │
│         └──────┬─────┴─────┬──────┘                                         │
│                ▼           ▼                                                │
│      VT-x / AMD-V + EPT / NPT + IOMMU + Virtio                             │
│                │                                                            │
│                ▼                                                            │
│      Physical CPU / Memory / NIC / Storage                                 │
│                                                                            │
│ 병목 포인트: cold start · 장치 에뮬레이션 · snapshot 위생 · 부채널 노출     │
└────────────────────────────────────────────────────────────────────────────┘
```

여기서 중요한 것은 하드웨어가 격리를 "자동으로" 완성해 주는 것이 아니라, 소프트웨어가 최소한의 장치 모델과 빠른 재개 경로를 위에 얹어야 진짜 효과가 난다는 점이다. 예를 들어 EPT/NPT가 있어도 불필요한 가상 장치가 많으면 시작 시간이 길어지고, IOMMU가 없으면 장치 직결이 다른 테넌트 메모리 침범 위험을 남길 수 있다.

- **📢 섹션 요약 비유**: 이 구조는 접이식 방탄 방을 펼치는 것과 같다. 벽 재질은 하드웨어가 책임지고, 플랫폼은 그 벽이 가장 적은 부품으로 빠르게 펼쳐지도록 설계해야 한다.

---

## Ⅲ. 비교 및 연결

[[206_serverless_cold_start|서버리스]] 격리를 이해하려면 공유 [[022_kernel_role|커널]] [[561_container_based_deployment|컨테이너]], MicroVM, 그리고 더 강한 기밀 [[598_vm_migration_nic|VM]] / [[478_tee|신뢰 실행 환경]] ([[972_tee_based_ml|Trusted Execution Environment]], [[478_tee|TEE]])을 함께 비교해 보는 것이 좋다. 이 세 방식은 모두 "격리"를 지향하지만, [[571_protection_vs_security|보호]] 경계와 비용이 다르다. [[206_serverless_cold_start|서버리스]] 플랫폼은 보통 이 가운데 MicroVM을 기본 균형점으로 택하고, 필요에 따라 더 강한 [[796_memory_encryption|메모리 암호화]]나 attestation을 얹는다.

| 방식 | 격리 경계 | 시작 속도 | 강점 | 약점 |
| :-- | :-- | :-- | :-- | :-- |
| 공유 [[022_kernel_role|커널]] [[561_container_based_deployment|컨테이너]] | [[061_namespace|네임스페이스]] / cgroup 중심 | 매우 빠름 | 밀집도와 운영 단순성이 좋다 | [[022_kernel_role|커널]] 취약점에 취약하고 [[310_multi_tenant_database_architecture|멀티테넌트]] 경계가 약하다 |
| MicroVM 기반 [[206_serverless_cold_start|서버리스]] | 하드웨어 [[015_virtualization|가상화]] + 최소 장치 | 빠름 | VM급 경계와 짧은 시작 시간의 균형 | 장치 [[015_virtualization|가상화]]와 [[637_zfs_snapshot_cow_architecture|snapshot]] 관리 복잡도가 있다 |
| 기밀 [[598_vm_migration_nic|VM]] / [[478_tee|TEE]] | 하드웨어 격리 + [[796_memory_encryption|메모리 암호화]] / attestation | 상대적으로 느림 | 호스트 운영자 위협까지 줄일 수 있다 | 오버헤드, 디버깅 제약, 장치 지원 한계가 있다 |

이 비교에서 [[206_serverless_cold_start|서버리스]] 하드웨어 기술의 위치는 뚜렷하다. [[561_container_based_deployment|컨테이너]]보다 강한 경계가 필요하지만, 일반 VM처럼 무거우면 함수형 워크로드에 맞지 않는다. 그래서 Firecracker 같은 MicroVM 계열은 [[015_virtualization|가상화]]의 장점을 유지하되, 키보드·그래픽 같은 불필요한 장치를 버리고 네트워크·블록만 남겨 시간을 아낀다.

또한 이 구조는 기밀 컴퓨팅과도 연결된다. 공용 [[206_serverless_cold_start|서버리스]]가 단순 테넌트 분리를 넘어서 플랫폼 운영자 수준의 위협까지 고려하려면, 향후에는 AMD 보안 암호화 [[015_virtualization|가상화]]-보안 중첩 [[286_page_frame|페이지]] (Secure Encrypted Virtualization-Secure Nested [[259_paging|Paging]], SEV-SNP)나 Intel 신뢰 [[064_relation_domain|도메인]] 확장 (Trust [[064_relation_domain|Domain]] Extensions, TDX) 같은 [[796_memory_encryption|메모리 암호화]] 기반 격리가 더 많이 결합될 가능성이 있다.

- **📢 섹션 요약 비유**: 일반 [[561_container_based_deployment|컨테이너]]가 칸막이 책상이라면, MicroVM은 조립식 개인실이고, 기밀 VM은 방 자체를 잠글 뿐 아니라 집주인도 안을 못 들여다보게 하는 금고형 방이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 공개 [[342_faas|FaaS]] 플랫폼, 사용자 플러그인을 받는 [[309_saas|SaaS]], [[310_multi_tenant_database_architecture|멀티테넌트]] 엣지 런타임에서 이 기술의 중요성이 가장 크게 드러난다. 예를 들어 누구나 코드를 올릴 수 있는 [[206_serverless_cold_start|서버리스]] 플랫폼에서 공유 [[022_kernel_role|커널]] [[561_container_based_deployment|컨테이너]]만 사용하면, 한 테넌트의 [[022_kernel_role|커널]] 탈출이 전체 노드 위험으로 번질 수 있다. 반면 MicroVM 기반 격리를 쓰면 시작 시간이 약간 늘더라도 신뢰 경계를 훨씬 명확하게 만들 수 있다.

### 적용 판단 [[435_checklist_based_testing|체크리스트]]

1. 실행 코드가 신뢰되지 않는 [[310_multi_tenant_database_architecture|멀티테넌트]] 환경인가, 아니면 내부 워크로드인가?
2. [[347_cold_start_problem|cold start]] 목표가 수 밀리초인지 수십 밀리초인지에 따라 snapshot과 장치 모델을 어떻게 구성할 것인가?
3. [[587_nic_offloading|NIC]], 그래픽 처리 장치 ([[418_gpu|Graphics Processing Unit]], [[418_gpu|GPU]]), 스토리지 같은 장치를 공유할 때 IOMMU와 안전한 virtio / mediated path가 준비되어 있는가?
4. [[637_zfs_snapshot_cow_architecture|snapshot]] 안에 [[303_authentication_authorization_patterns|인증]] 토큰, 난수 상태, 이전 테넌트 잔재가 섞이지 않도록 위생 관리가 되는가?
5. 캐시 부채널, noisy neighbor, 관찰성 부족 같은 운영 문제를 별도로 다룰 수 있는가?

### 피해야 할 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 공용 [[310_multi_tenant_database_architecture|멀티테넌트]] 코드 실행인데도 단순 shared-kernel [[561_container_based_deployment|컨테이너]]만으로 충분하다고 보는 판단
- 빠른 시작만 생각해 가상 장치를 많이 넣고, 오히려 초기화 경로를 길게 만드는 설계
- 장치 공유를 하면서 [[627_iommu_dma_isolation|IOMMU]] 없이 [[746_io_direct_memory_access_dma|DMA]] 격리를 생략하는 구성
- 하드웨어 격리가 있으니 [[637_zfs_snapshot_cow_architecture|snapshot]] 위생, 이미지 [[395_verification_process_review|검증]], 보안 컴퓨팅 모드 ([[080_seccomp|secure computing mode]], [[080_seccomp|seccomp]]) 같은 상위 [[571_protection_vs_security|보호]]가 불필요하다고 오해하는 운영

기술사 관점에서는 "하드웨어 격리 = 만능 보안"이라는 서술이 가장 위험하다. 실제 답안에서는 격리 강도와 시작 시간, 장치 경로, 운영 복잡도, 비용의 균형을 함께 적어야 설계 현실성이 살아난다.

- **📢 섹션 요약 비유**: [[206_serverless_cold_start|서버리스]] 격리 설계는 놀이공원에서 회전문을 만드는 일과 같다. 손님은 빨리 입장해야 하지만, 표 확인과 안전문이 약하면 공원이 순식간에 위험해진다.

---

## Ⅴ. 기대효과 및 결론

[[150_serverless_computing_faas|서버리스 컴퓨팅]] [[561_container_based_deployment|컨테이너]] 분리 하드웨어 기술이 성숙할수록, 플랫폼은 더 많은 테넌트를 같은 물리 서버에 안전하게 수용할 수 있게 된다. 이는 [[206_serverless_cold_start|서버리스]]의 경제성, [[571_resiliency_fault_tolerance_patterns|탄력성]], 멀티테넌시를 동시에 지탱하는 기반이다. 즉 사용자는 함수 단위의 편의성만 보지만, 그 뒤에는 빠르게 생성되고 빠르게 사라지는 하드웨어 경계가 계속 작동하고 있는 셈이다.

물론 한계는 남는다. 하드웨어 [[015_virtualization|가상화]]가 있어도 이미지 풀, 런타임 초기화, 언어 [[598_vm_migration_nic|VM]] warm-up 같은 [[347_cold_start_problem|cold start]] 원인은 여전히 존재하며, 캐시 기반 부채널이나 관찰성 제약도 완전히 사라지지 않는다. 앞으로는 [[796_memory_encryption|메모리 암호화]], attestation, 안전한 가속기 분할, confidential [[206_serverless_cold_start|serverless]] 같은 방향이 더 중요해질 가능성이 높다.

결론적으로 이 기술은 "[[206_serverless_cold_start|서버리스]]에 개인 방을 제공하는 하드웨어"로 기억하면 된다. 빠른 실행이라는 사용자 경험과 강한 격리라는 운영 요구를 동시에 만족시키려면, [[561_container_based_deployment|컨테이너]]와 VM의 장점을 하드웨어 수준에서 접목해야 한다.

- **📢 섹션 요약 비유**: 좋은 [[206_serverless_cold_start|서버리스]] 격리는 콘서트장에서 관객마다 투명한 방음 부스를 즉시 펼쳐 주는 것과 같다. 모두 같은 건물 안에 있어도, 서로의 소리와 물건이 섞이지 않게 해 주는 것이 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[206_serverless_cold_start|서버리스]] / [[342_faas|FaaS]] (Function [[344_as_autonomous_system_asn|as]] a [[090_service_kubernetes_network_load_balancing|Service]]) | 짧은 실행 단위와 멀티테넌시 때문에 강한 격리가 필요한 운영 모델이다. |
| MicroVM | [[206_serverless_cold_start|서버리스]]가 빠른 시작과 강한 격리를 절충하는 대표 실행 단위다. |
| EPT / NPT | MicroVM 메모리 경계를 낮은 오버헤드로 만드는 핵심 하드웨어 기능이다. |
| [[627_iommu_dma_isolation|IOMMU]] | 장치 DMA가 다른 테넌트 메모리에 접근하지 못하게 막는다. |
| Virtio | 최소한의 장치 모델로 시작 시간을 줄이면서 I/O를 제공한다. |
| Firecracker | MicroVM 기반 [[206_serverless_cold_start|서버리스]] 격리를 대표하는 구현 사례다. |
| AMD 보안 암호화 [[015_virtualization|가상화]]-보안 중첩 [[286_page_frame|페이지]] (Secure Encrypted Virtualization-Secure Nested [[259_paging|Paging]], SEV-SNP) / Intel 신뢰 [[064_relation_domain|도메인]] 확장 (Trust [[064_relation_domain|Domain]] Extensions, TDX) | [[206_serverless_cold_start|서버리스]]를 더 강한 기밀 격리 방향으로 확장하는 최신 하드웨어 기능이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
공유 커널 컨테이너
        │
        ▼
VT-x / AMD-V 기반 경량 가상화
        │
        ▼
EPT / NPT 기반 MicroVM 격리
        │
        ▼
Snapshot / Restore 기반 빠른 재개
        │
        ▼
IOMMU · 최소 virtio 장치 경로
        │
        ▼
Confidential Serverless / 하드웨어 attestation
```

이 흐름은 단순 [[561_container_based_deployment|컨테이너]] 격리에서 출발해, [[527_hardware_assisted_virtualization|하드웨어 보조]] [[015_virtualization|가상화]]와 빠른 재개 기술을 거쳐, 더 강한 기밀 실행 환경으로 나아가는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[206_serverless_cold_start|서버리스]]는 손님이 올 때마다 아주 빨리 작은 방을 만들어 주는 마법 호텔 같아요.
2. 그런데 방이 빨리 생겨도 벽이 약하면 옆방 물건이 섞일 수 있으니, 아주 튼튼한 벽이 필요해요.
3. 이 하드웨어 기술은 방을 빨리 만들면서도 서로 절대 넘나들지 못하게 해 주는 비밀 벽이에요.
