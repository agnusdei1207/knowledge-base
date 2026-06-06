---
title: "062. Cgroups"
date: "2026-03-21"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: cgroups([Control Groups](/studynote/01_computer_architecture/15_advanced_topics/668_cgroups_hw_resource_allocation/))는 프로세스 그룹별로 CPU, 메모리, I/O 같은 자원 사용량을 제한하고 측정하는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 기능이다.
> 2. **가치**: 한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 자원을 독점하는 것을 막아 멀티 테넌시와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 안정성을 지킨다.
> 3. **융합**: Kubernetes의 requests/limits와 [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) ([Out of Memory](/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 제어는 cgroups 없이는 제대로 동작할 수 없다.

---

## Ⅰ. 개요 및 필요성

네임스페이스가 "무엇이 보이느냐"를 나누는 기술이라면, cgroups는 "얼마나 쓸 수 있느냐"를 나누는 기술이다. 즉, 시야와 자원 제한은 서로 다른 문제다.

한 프로세스가 CPU를 독점하거나 메모리를 과하게 쓰면 시스템 전체가 흔들린다. cgroups는 이런 자원 고갈을 막기 위해 등장했다.

- **📢 섹션 요약 비유**: 각 방에 문을 달아 보이게만 하는 것이 네임스페이스라면, 전기 사용량을 제한하는 차단기가 cgroups다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Root Cgroup
  +- Group A
  |   +- CPU
  |   +- Memory
  |   +- IO
  +- Group B
      +- CPU
      +- Memory
      +- IO
```

| 컨트롤러 | 역할 |
| :-- | :-- |
| CPU | 사용량/우선순위 제어 |
| Memory | 메모리 상한 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| IO | 디스크 I/O 제한 |
| pids | 프로세스 수 제한 |
| cpuacct | 사용량 계측 |

cgroups는 계층 구조를 가진다. 상위 그룹이 전체 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 갖고, 하위 그룹이 세부 자원을 배분받는다. 그래서 운영자는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 단위로 자원을 정밀하게 다룰 수 있다.

- **📢 섹션 요약 비유**: 건물 관리실이 각 세대별 전기, 수도, 인터넷 사용량을 따로 정하는 구조다.

---

## Ⅲ. 비교 및 연결

| 항목 | cgroups | [Namespace](/studynote/02_operating_system/01_overview_architecture/061_namespace/) | Resource [Quota](/studynote/02_operating_system/09_file_system/551_quota_disk_limit/) |
| :-- | :-- | :-- | :-- |
| 목적 | 자원 사용 제한/계측 | 보이는 세계 분리 | 운영 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 수준 제한 |
| 강점 | CPU, 메모리, IO 통제 | 격리와 분리 | 클러스터 전체 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 핵심 | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 핵심 | 상위 운영 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |

Kubernetes의 requests/limits는 결국 cgroups [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)으로 내려간다. 따라서 [오케스트레이션](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) 수준의 숫자가 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준 제어로 이어지는 것이 핵심이다.

- **📢 섹션 요약 비유**: 앱에서 "전기 2칸만 써"라고 말하면, 실제 차단기는 cgroups가 작동하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. CPU, 메모리, I/O 한도가 명확한가?
2. [OOM](/studynote/02_operating_system/02_process_thread/157_oom_killer/) 발생 시 우선순위와 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 전략이 있는가?
3. 요청(request)과 제한(limit)을 구분했는가?
4. 계층 구조가 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 조직도와 맞는가?
5. 사용량 계측을 통해 과금과 운영이 가능한가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 자원 제한을 안 걸어 두는 설계
- requests/limits를 임의로 크게만 잡는 설계
- 계측 없이 "문제 생기면 늘리자"로 가는 설계
- cgroups를 namespace와 혼동하는 설계

기술사 관점에서는 cgroups를 "[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 제한 도구"가 아니라 "운영의 공정성 도구"로 봐야 한다. 제한과 계측이 함께 있어야 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질이 유지된다.

- **📢 섹션 요약 비유**: 운동장에 뛰는 사람 수와 달리는 시간을 정해, 한 명이 다 쓰지 못하게 하는 규칙이다.

---

## Ⅴ. 기대효과 및 결론

cgroups는 Linux를 대규모 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 플랫폼으로 만드는 핵심 기반이다. [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/), 클라우드 과금까지 모두 이 위에서 돌아간다.

결국 cgroups는 "프로세스가 어디 있느냐"보다 "얼마나 쓸 수 있느냐"를 관리하는 현실적인 운영 장치다.

- **📢 섹션 요약 비유**: 같은 놀이터를 쓰더라도, 각 반이 쓸 수 있는 시간과 장비를 정해 주는 것과 같다.

---

## 관련 개념 맵

```text
Process Group
   v
cgroups
   v
Resource Control
   v
Kubernetes requests/limits
   v
Container Scheduling
```

---

## 관련 키워드 및 발전 흐름도

```text
Process Containers
   v
cgroups
   v
Container Resource Control
   v
Kubernetes Limits
```

---

## 어린이를 위한 3줄 비유 설명

누가 전기를 너무 많이 쓰면 건물 전체가 위험해져요.
그래서 방마다 전기 사용량을 정해 두는 거예요.
그 규칙이 cgroups예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 62 / 800

<- **이전**: [61. 네임스페이스 (Namespace) - 자원 격리](/studynote/02_operating_system/01_overview_architecture/061_namespace/)
**다음**: [63. 도커 (Docker) 아키텍처](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) ->

---
