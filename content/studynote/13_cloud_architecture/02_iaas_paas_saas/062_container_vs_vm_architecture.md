---
title: 62. 컨테이너 vs 가상머신(VM)
date: '2026-04-07'
tags:
- studynote-cloud
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 가상머신([[598_vm_migration_nic|VM]])은 [[054_hypervisor|하이퍼바이저]]([[054_hypervisor|Hypervisor]]) 위에 각자 Guest OS(Guest [[001_operating_system_purpose|Operating System]])를 올려 하드웨어를 [[015_virtualization|가상화]]하고, [[561_container_based_deployment|컨테이너]]([[194_container_virtualization_docker_namespace|Container]])는 Host OS의 [[022_kernel_role|커널]]([[022_kernel_role|Kernel]])을 공유하며 프로세스만 격리하는 OS 수준 [[015_virtualization|가상화]]다.
> 2. **가치**: VM은 격리와 호환성이 강하지만 무겁고 느리며, [[561_container_based_deployment|컨테이너]]는 가볍고 빨라서 [[619_msa_traffic_hardware|MSA]]([[122_msa_microservices_architecture|Microservices Architecture]])와 [[090_configuration_item|CI]]/CD에 유리하다.
> 3. **판단**: 보안 경계, 상태 저장 여부, 시작 속도, 운영 복잡도를 함께 봐야 하며, 실제 클라우드는 VM과 [[561_container_based_deployment|컨테이너]]를 섞는 하이브리드가 기본이다.

---

## Ⅰ. 개요 및 필요성

서버를 한 대 더 쓰는 것이 아니라, "어디까지를 하나의 운영 단위로 볼 것인가"가 핵심이다. VM은 운영체제까지 포함한 완전한 컴퓨터를 복제하고, [[561_container_based_deployment|컨테이너]]는 애플리케이션 실행에 필요한 최소 단위만 묶는다.

클라우드와 [[619_msa_traffic_hardware|MSA]] 시대에는 수 분짜리 부팅보다 초 단위 스케일 아웃이 중요해졌다. 반대로 금융, 공공, 멀티테넌시 환경에서는 [[022_kernel_role|커널]] 공유를 피하는 강한 격리가 여전히 중요하다.

- **📢 섹션 요약 비유**: 단독주택은 비싸고 느리지만 안전하고, 아파트는 빠르고 효율적이지만 공용 설비를 함께 쓴다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
[VM]
App
Guest OS
Hypervisor
Host OS
Hardware

[Container]
App
Bins / Libs
Container Runtime
Namespace + cgroups
Host Kernel
Hardware
```

| 항목 | [[598_vm_migration_nic|VM]] | [[194_container_virtualization_docker_namespace|Container]] |
| :-- | :-- | :-- |
| [[015_virtualization|가상화]] 대상 | Hardware | OS [[022_kernel_role|Kernel]] |
| 부팅 속도 | 느림 | 빠름 |
| 디스크/메모리 오버헤드 | 큼 | 작음 |
| 이종 OS 실행 | 가능 | 제한적 |
| 격리 수준 | 매우 높음 | 상대적으로 낮음 |

[[561_container_based_deployment|컨테이너]]는 Namespace로 보이는 세계를 나누고, [[062_cgroups|cgroups]]([[668_cgroups_hw_resource_allocation|Control Groups]])로 자원 사용량을 제한한다. 그래서 "가볍다"는 말은 단순히 크기가 작다는 뜻이 아니라, OS를 통째로 복제하지 않는다는 뜻이다.

- **📢 섹션 요약 비유**: VM은 방마다 수도와 전기까지 따로 놓는 집이고, [[561_container_based_deployment|컨테이너]]는 한 건물의 공용 설비를 공유하면서 방만 나누는 구조다.

---

## Ⅲ. 비교 및 연결

| 구분 | [[598_vm_migration_nic|VM]] | [[194_container_virtualization_docker_namespace|Container]] | MicroVM |
| :-- | :-- | :-- | :-- |
| 시작 시간 | 수 분 | 수 초~밀리초 | 수 초 |
| 격리 | 강함 | 중간 | 강함 |
| 자원 효율 | 낮음 | 높음 | 중간 |
| 대표 사용처 | 레거시, 강한 격리 | [[619_msa_traffic_hardware|MSA]], [[090_configuration_item|CI]]/CD, 웹 [[090_service_kubernetes_network_load_balancing|서비스]] | [[206_serverless_cold_start|서버리스]], 멀티테넌시 |
| 대표 기술 | [[713_kvm_over_ip|KVM]], VMware | [[063_docker_architecture|Docker]], containerd | Firecracker, Kata |

VM과 [[561_container_based_deployment|컨테이너]]는 대체 관계라기보다 역할 분담 관계다. 신뢰 경계가 분명한 시스템은 VM으로 나누고, 그 안에서 빠르게 변하는 업무는 [[561_container_based_deployment|컨테이너]]로 쪼개는 식으로 같이 쓴다.

- **📢 섹션 요약 비유**: 큰 창고 건물은 VM처럼 단단하게 짓고, 그 안의 선반은 [[561_container_based_deployment|컨테이너]]처럼 빠르게 바꿔 끼우는 셈이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 선택 기준

1. 강한 격리와 OS 이질성이 필요하면 VM을 우선한다.
2. 빠른 배포, 자동 확장, 동일 OS 계열 배포가 필요하면 [[561_container_based_deployment|컨테이너]]를 쓴다.
3. [[310_multi_tenant_database_architecture|멀티테넌트]] [[206_serverless_cold_start|서버리스]]나 보안 강화를 원하면 MicroVM을 검토한다.
4. 상태 저장형 데이터베이스와 핵심 거래 시스템은 섣불리 [[561_container_based_deployment|컨테이너]]에 몰지 않는다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 서로 신뢰 수준이 다른 워크로드를 같은 [[022_kernel_role|커널]]에 얹는 설계
- 상태를 가진 [[090_service_kubernetes_network_load_balancing|서비스]]까지 무조건 [[561_container_based_deployment|컨테이너]]화하는 설계
- 격리 수준보다 배포 편의만 보는 설계
- VM과 [[561_container_based_deployment|컨테이너]]의 역할을 혼동하는 설계

기술사 관점에서는 "어떤 기술이 더 새롭냐"보다 "어떤 경계가 필요한가"를 먼저 묻는 것이 맞다. 안정성과 기동성은 동시에 최대화되지 않으므로, 워크로드별로 다른 층을 써야 한다.

- **📢 섹션 요약 비유**: 냉장고가 필요한 음식과 실온 보관해도 되는 음식을 같은 상자에 넣지 않는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

VM은 보안과 호환성의 바닥을 맡고, [[561_container_based_deployment|컨테이너]]는 배포 속도와 자원 효율을 맡는다. 그래서 현대 클라우드는 둘 중 하나를 고르는 게 아니라 둘을 조합한다.

결국 중요한 것은 "VM이냐 [[561_container_based_deployment|컨테이너]]냐"가 아니라 "업무를 어디서 끊고 어떻게 격리할 것인가"다.

- **📢 섹션 요약 비유**: 튼튼한 건물 위에 빠르게 바꾸는 가구를 올리는 것이 가장 현실적인 선택이다.

---

## 관련 개념 맵

```text
Hypervisor
  ↓
Virtual Machine
  ↓
Guest OS
  ↓
Workload Isolation

Namespace + cgroups
  ↓
Container
  ↓
Kubernetes / CI-CD
```

---

## 관련 키워드 및 발전 흐름도

```text
Bare Metal
  ↓
Virtualization
  ↓
Containerization
  ↓
MicroVM / Serverless
```

---

## 어린이를 위한 3줄 비유 설명

VM은 집을 통째로 빌리는 것처럼 무겁지만 안전해요.  
[[561_container_based_deployment|컨테이너]]는 방만 빌리는 것처럼 가볍고 빨라요.  
둘을 잘 섞어 쓰면 빠르면서도 안전하게 만들 수 있어요.
