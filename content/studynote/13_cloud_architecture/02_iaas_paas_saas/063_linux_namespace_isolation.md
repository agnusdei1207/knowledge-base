+++
title = "63. 리눅스 네임스페이스 (Namespace) - PID, Net, Mount, User 등 자원 분리"
date = 2026-04-07

[taxonomies]
tags = ["studynote-cloud"]

[extra]
tags = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Linux Namespace는 프로세스가 보는 PID, 네트워크, [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/), 사용자 등의 시야를 분리하는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 격리 기능이다.
> 2. **가치**: Namespace는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 서로 다른 시스템처럼 보이게 만들고, 위험한 프로세스 충돌을 줄인다.
> 3. **판단**: Namespace는 자원 사용량을 제한하지 않으므로 cgroups와 함께 봐야 완전한 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 격리가 된다.

---

## Ⅰ. 개요 및 필요성

하나의 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 여러 서비스가 함께 쓰면, 서로의 프로세스나 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 보이는 문제가 생긴다. Namespace는 "보이는 세계"를 나눠서 이런 충돌을 줄인다.

[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 가볍게 느껴지는 이유도 결국 이 때문이다. 각 프로세스가 자기만의 작은 우주를 가진 것처럼 보이게 만들기 때문이다.

- **📢 섹션 요약 비유**: 같은 건물 안에서도 각 방의 창문에 보이는 풍경을 다르게 바꿔 주는 장치와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Process
  ├─ PID Namespace
  ├─ NET Namespace
  ├─ MNT Namespace
  ├─ UTS Namespace
  ├─ IPC Namespace
  ├─ USER Namespace
  └─ CGROUP Namespace
```

| [Namespace](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) | 분리 대상 | 효과 |
| :-- | :-- | :-- |
| PID | 프로세스 ID | 각 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 자기 PID 1을 가짐 |
| NET | 네트워크 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) | 인터페이스, [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 분리 |
| MNT | [마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 공간 | 서로 다른 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 보기 |
| UTS | 호스트명 | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)별 hostname 분리 |
| [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) | [프로세스 간 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/) | [공유 메모리](/knowledge-base/studynote/02_operating_system/02_process_thread/118_shared_memory/)/[세마포어](/knowledge-base/studynote/02_operating_system/04_synchronization/224_semaphore/) 분리 |
| USER | 사용자/권한 | root 매핑과 권한 격리 |

Namespace는 "누가 무엇을 볼 수 있느냐"를 바꾸고, cgroups는 "얼마나 쓸 수 있느냐"를 바꾼다. 둘은 역할이 다르다.

- **📢 섹션 요약 비유**: 커튼으로 시야를 가리고, 차단기로 전기 사용량을 제한하는 것이 서로 다른 일이다.

---

## Ⅲ. 비교 및 연결

| 구분 | [Namespace](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) | [cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) | chroot |
| :-- | :-- | :-- | :-- |
| 목적 | 시야 분리 | 자원 제한 | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 경로 제한 |
| 강점 | 프로세스/네트워크/[마운트](/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 격리 | CPU, 메모리, I/O 통제 | 단순하고 가벼움 |
| 한계 | 자원 사용량 제한은 못함 | 보이는 세계 분리는 못함 | 보안 격리가 약함 |

Namespace는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 기반이지만, 단독으로는 충분하지 않다. 보안과 운영 안정성을 위해서는 권한, [cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/), 보안 모듈까지 함께 설계해야 한다.

- **📢 섹션 요약 비유**: 방을 따로 나누는 것만으로는 충분하지 않고, 사용 전기와 출입 권한도 함께 관리해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 필요한 [Namespace](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) 종류를 모두 적용했는가?
2. USER Namespace로 권한 매핑을 분리했는가?
3. NET Namespace와 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 정책이 함께 설계되었는가?
4. cgroups와 같이 자원 한도가 설정되었는가?
5. unshare/setns/[clone](/knowledge-base/studynote/02_operating_system/02_process_thread/149_clone_system_call/) 기반 흐름을 이해하고 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- Namespace만 믿고 리소스 고갈을 방치하는 설계
- root 권한 공유를 그대로 두는 설계
- 네트워크 Namespace와 보안 그룹을 혼동하는 설계
- [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 분리만 하고 프로세스 격리는 놓치는 설계

기술사 관점에서는 Namespace를 "[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 기능"으로만 보지 말고, 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 격리 메커니즘으로 이해해야 한다. 그래야 보안과 운영을 동시에 설명할 수 있다.

- **📢 섹션 요약 비유**: 같은 놀이터라도 구역표와 출입증이 함께 있어야 정말 안전해진다.

---

## Ⅴ. 기대효과 및 결론

Namespace는 리눅스 한 개를 여러 개의 작은 리눅스처럼 보이게 만든다. 이 덕분에 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), 샌드박스, 프로세스 분리가 모두 가능해졌다.

결국 핵심은 "보이는 세상"을 분리하는 능력이며, 이것이 현대 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 첫 번째 벽이다.

- **📢 섹션 요약 비유**: 같은 집에서도 각자 자기 방만 보이게 해 주는 벽과 같다.

---

## 관련 개념 맵

```text
Linux Kernel
  ↓
Namespaces
  ↓
Container Isolation
  ↓
Docker / Kubernetes
```

---

## 관련 키워드 및 발전 흐름도

```text
chroot
  ↓
Namespace
  ↓
cgroups
  ↓
Container Runtime
```

---

## 어린이를 위한 3줄 비유 설명

같은 집에서도 방마다 보이는 창문이 다르면 서로 덜 헷갈려요.
네임스페이스는 리눅스 안에서 보이는 세상을 나눠 줘요.
그래서 여러 프로그램이 함께 있어도 서로 덜 부딪혀요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 62 / 371

← **이전**: [62. 컨테이너 vs 가상머신(VM)](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/062_container_vs_vm_architecture/)
**다음**: [64. cgroups (Control Groups) - 컨테이너가 사용할 수 있는 CPU, 메모리 자원의 상한선을 제한(Limit)하고](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/064_cgroups_control_groups_resource_limit/) →

---
