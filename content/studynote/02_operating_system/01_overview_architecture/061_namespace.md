---
title: "61. 네임스페이스 (Namespace) - 자원 격리"
date: "2026-03-21"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 네임스페이스(Namespace)는 Linux [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 PID, Network, [Mount](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 같은 전역 자원을 프로세스별로 다르게 보이게 만드는 자원 격리 기술이다.
> 2. **가치**: 같은 호스트 안에서도 프로세스가 자기만의 세계를 가진 것처럼 보이게 해 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 격리와 [멀티 테넌시](/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/) 운영을 가능하게 한다.
> 3. **융합**: User Namespace와 [cgroups](/studynote/02_operating_system/01_overview_architecture/062_cgroups/)(cgroup)를 함께 써야 Rootless [Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) 같은 현대 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 보안이 완성된다.

---

## Ⅰ. 개요 및 필요성

전통적인 Linux 시스템은 모든 프로세스가 같은 자원 목록을 본다. 그러면 서로 다른 애플리케이션을 같은 호스트에 안전하게 얹기 어렵고, 한 프로세스의 오류가 다른 프로세스에 쉽게 번진다.

네임스페이스는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 보는 전역 자원을 잘라서 각 프로세스 그룹에 따로 보여 준다. 이 덕분에 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 "작은 독립 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)"처럼 보인다.

- **📢 섹션 요약 비유**: 같은 학교 운동장 안에 있어도 반마다 다른 지도와 출석부를 주는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
[ Host Kernel ]
   +- PID Namespace  -> 서로 다른 프로세스 번호
   +- NET Namespace  -> 서로 다른 IP / 라우팅
   +- MNT Namespace  -> 서로 다른 루트 파일 시스템
   +- UTS Namespace  -> 서로 다른 호스트 이름
   +- IPC Namespace  -> 서로 다른 공유 메모리 / 메시지 큐
   +- USER Namespace -> 서로 다른 UID / GID 매핑
```

| 네임스페이스 | 격리 대상 | 의미 |
| :-- | :-- | :-- |
| PID | 프로세스 번호 | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 안에서 PID 1을 따로 가질 수 있음 |
| NET | 네트워크 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) | 인터페이스, IP 주소, [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 분리 |
| MNT | [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 지점 | 서로 다른 [루트 파일 시스템](/studynote/02_operating_system/01_overview_architecture/064_rootfs_overlayfs/) 제공 |
| UTS | 호스트 이름 | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)별 hostname 분리 |
| [IPC](/studynote/02_operating_system/02_process_thread/117_ipc/) | [공유 메모리](/studynote/02_operating_system/02_process_thread/118_shared_memory/)/메시지 | [프로세스 간 통신](/studynote/02_operating_system/02_process_thread/117_ipc/) 공간 분리 |
| USER | UID/GID | root 권한의 보이는 범위를 바꿈 |

네임스페이스는 "같은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/), 다른 시야"를 만드는 기술이다. 같은 물리 자원을 쓰더라도 보여 주는 세계를 분리하므로, 프로세스는 서로를 잘 모르는 것처럼 동작한다.

- **📢 섹션 요약 비유**: 한 건물 안에 여러 개의 VR 고글을 씌워, 각자 다른 방에 있는 것처럼 보이게 만드는 장치다.

---

## Ⅲ. 비교 및 연결

| 항목 | 네임스페이스 | [cgroups](/studynote/02_operating_system/01_overview_architecture/062_cgroups/)(cgroup) | chroot | 가상 머신([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)) |
| :-- | :-- | :-- | :-- | :-- |
| 목적 | 보이는 자원 격리 | 쓰는 양 제한 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 루트 변경 | OS 자체 분리 |
| 강점 | 세밀한 논리적 분리 | CPU/메모리/IO 제어 | 단순함 | 강한 격리 |
| 한계 | 자원 사용량 제한은 아님 | 시야 분리는 아님 | 보안 경계가 약함 | 무거움 |

네임스페이스는 cgroups와 함께 쓰일 때 가장 강하다. 네임스페이스는 "무엇이 보이느냐"를 바꾸고, cgroups는 "얼마나 쓸 수 있느냐"를 제한한다.

- **📢 섹션 요약 비유**: 창문을 가리고 방을 나누는 것이 네임스페이스라면, 각 방에 쓸 전기와 물을 제한하는 것이 cgroups다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)마다 필요한 네임스페이스를 모두 분리했는가?
2. User Namespace를 써서 rootless 구성이 가능한가?
3. cgroups와 함께 리소스 제한도 걸었는가?
4. host PID/NET namespace 공유가 정말 필요한가?
5. `--privileged` 같은 과도한 권한이 없는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 네임스페이스만 믿고 `--privileged` [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 운영하는 설계
- User Namespace 없이 root를 그대로 노출하는 설계
- Host Network / Host PID를 습관적으로 공유하는 설계
- 격리와 자원 제한을 혼동하는 설계

기술사 관점에서는 네임스페이스를 "[컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 보이는 세계를 바꾸는 기술"로 이해해야 한다. 보안 경계는 하나만으로 완성되지 않으므로, 네임스페이스, [cgroups](/studynote/02_operating_system/01_overview_architecture/062_cgroups/), capability, Seccomp를 함께 봐야 한다.

- **📢 섹션 요약 비유**: 방 이름표만 바꾸는 것이 아니라, 문 잠금과 출입 카드까지 같이 챙겨야 진짜 안전하다.

---

## Ⅴ. 기대효과 및 결론

네임스페이스는 Linux를 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 플랫폼으로 바꾼 핵심 기반이다. 같은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 쓰면서도 서로 다른 세계를 제공하므로, 효율과 격리를 동시에 얻는다.

결국 좋은 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 설계는 "보이지 않게 나누기"와 "사용량을 제한하기"를 함께 맞추는 일이다.

- **📢 섹션 요약 비유**: 같은 놀이터를 쓰더라도, 놀이터 안에 투명 울타리와 출입 규칙을 함께 세워 두는 것과 같다.

---

## 관련 개념 맵

```text
Host Kernel
   v
Namespace
   v
Container Isolation
   v
Rootless Container
   v
Secure Multi-tenancy
```

---

## 관련 키워드 및 발전 흐름도

```text
chroot
   v
Mount Namespace
   v
PID / NET / IPC / UTS / USER Namespace
   v
Container Runtime
   v
Rootless Container
```

---

## 어린이를 위한 3줄 비유 설명

같은 집에 살아도 방마다 다른 지도와 이름표를 붙여 주는 거예요.
그래서 한 방에서 하는 일이 다른 방에는 잘 안 보여요.
[컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 이렇게 나눠서 쓰는 똑똑한 방이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 61 / 800

<- **이전**: [60. 컨테이너 가상화 (Container Virtualization) - OS 수준 가상화](/studynote/02_operating_system/01_overview_architecture/060_container_virtualization/)
**다음**: [62. 컨트롤 그룹 (cgroups) - 자원 할당 제어](/studynote/02_operating_system/01_overview_architecture/062_cgroups/) ->

---
