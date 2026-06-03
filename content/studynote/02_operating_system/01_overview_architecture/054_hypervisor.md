+++
title = "54. 하이퍼바이저 (Hypervisor)"
date = 2026-05-01

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 하이퍼바이저 (Hypervisor)는 여러 가상 머신 ([Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))을 직접 관리하는 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 제어 계층이다.
> 2. **가치**: CPU, 메모리, I/O를 분리해 격리와 자원 공유를 동시에 제공한다.
> 3. **판단 포인트**: Type 1과 Type 2의 차이, hardware assist, trap-and-emulate 구조를 구분해야 한다.

---

## Ⅰ. 개요 및 필요성

하이퍼바이저는 물리 하드웨어 위에서 VM을 실행시키는 핵심 소프트웨어다. 하나의 서버를 여러 서버처럼 쓰게 하면서도 각 VM을 서로 격리한다.

클라우드와 데이터센터에서 자원 효율과 보안 격리를 동시에 만족시키려면 하이퍼바이저가 필요하다.

- **📢 섹션 요약 비유**: 하이퍼바이저는 아파트 관리소장처럼 여러 집을 동시에 관리하는 역할이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

하이퍼바이저는 게스트 OS가 직접 하드웨어를 독점하지 못하게 하고, 가상 자원으로 중재한다. VM이 요청하면 CPU는 trap되고, 하이퍼바이저가 이를 처리한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Physical HW</div>
<div class="kb-diagram-connector">▲</div>
<div class="kb-diagram-note">Hypervisor (VMM)</div>
<div class="kb-diagram-tree-item" style="--depth:1">VM1 → Guest OS → Apps</div>
<div class="kb-diagram-tree-item" style="--depth:1">VM2 → Guest OS → Apps</div>
</div>
</div>



| 기능 | 역할 | 포인트 |
| :--- | :--- | :--- |
| CPU [virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/) | 스케줄링 | vCPU |
| Memory [virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/) | 주소 변환 | shadow/EPT/NPT |
| I/O [virtualization](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/) | 장치 공유 | emulation/[passthrough](/knowledge-base/studynote/02_operating_system/10_security/657_vfio_virtual_function_io_passthrough/) |
| [Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/) | 장애 격리 | [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 분리 |

핵심은 하드웨어 접근을 직접 허용하지 않고, 중간 계층이 제어함으로써 안정성과 공유를 얻는 것이다.

- **📢 섹션 요약 비유**: 하이퍼바이저는 여러 사람이 쓰는 주차장 출입증 관리기다.

---

## Ⅲ. 비교 및 연결

Type 1은 하드웨어 위에서 직접 동작하고, Type 2는 호스트 OS 위에서 동작한다. 일반적으로 Type 1이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 안정성에서 유리하다.

| 항목 | Type 1 | Type 2 |
| :--- | :--- | :--- |
| 위치 | bare metal | host OS 위 |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 높음 | 중간 |
| 용도 | 서버/클라우드 | 개발/실습 |

하이퍼바이저는 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 런타임과도 비교된다. VM은 OS까지 분리하고, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 커널을 공유한다.

- **📢 섹션 요약 비유**: Type 1은 땅 위에 바로 세운 건물, Type 2는 기존 건물 안에 얹은 모형 건물이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 메모리 오버커밋, CPU 스케줄링, 장치 패스스루, [라이브 마이그레이션](/knowledge-base/studynote/02_operating_system/10_security/629_live_migration_pre_copy/), 스냅샷을 함께 본다. 보안과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 항상 같이 고려해야 한다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. Type 1/Type 2 선택이 목적에 맞는가?
2. EPT/NPT 같은 하드웨어 지원을 활용하는가?
3. [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 격리와 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 요구를 균형 있게 맞추는가?
4. 스냅샷과 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 정책이 분리되어 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 워크로드를 한 호스트에 과도하게 몰아넣는 경우
- 장치 패스스루만 믿고 장애 대비를 안 하는 경우
- [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)와 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 같은 수준으로 혼동하는 경우

기술사 관점에서는 하이퍼바이저가 단순 [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 실행기가 아니라 자원 중재와 격리의 핵심 계층이라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: 하이퍼바이저는 여러 극장의 무대 장치를 한 명이 조율하는 무대 감독이다.

---

## Ⅴ. 기대효과 및 결론

하이퍼바이저는 서버 자원 활용률을 높이고, 격리와 유연성을 제공한다. 클라우드 인프라의 기본 전제라고 볼 수 있다.

정리하면, 하이퍼바이저는 물리 자원을 논리적으로 쪼개는 중재자다.

- **📢 섹션 요약 비유**: 하이퍼바이저는 큰 케이크를 공평하게 잘라 나누는 칼과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| VMM | 가상 머신 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/) |
| Type 1/2 | 배치 위치 |
| EPT/NPT | 메모리 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) |
| [Passthrough](/knowledge-base/studynote/02_operating_system/10_security/657_vfio_virtual_function_io_passthrough/) | I/O 가속 |
| [Snapshot](/knowledge-base/studynote/02_operating_system/10_security/637_zfs_snapshot_cow_architecture/) | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)/실험 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">물리 서버</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">하이퍼바이저</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">가상 머신</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">클라우드 / 멀티테넌시</div>
</div>
</div>



이 흐름은 단일 서버 운영에서 격리된 다중 서버 운영으로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 하이퍼바이저는 큰 방을 여러 칸으로 나눠 주는 아주 똑똑한 관리자예요.
2. 각 칸은 자기만의 컴퓨터처럼 사용할 수 있어요.
3. 그래서 한 칸이 고장 나도 다른 칸은 덜 흔들려요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 54 / 800

← **이전**: [53. 가상화 아키텍처 (Virtualization Architecture)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/053_virtualization_architecture/)
**다음**: [55. 베어메탈 하이퍼바이저 (Bare Metal Hypervisor)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/055_bare_metal_hypervisor/) →

---
