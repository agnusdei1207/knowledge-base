---
title: "743. 가상화 하이퍼바이저 (Virtualization Hypervisor)"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) ([Hypervisor](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/), 또는 VMM: [Virtual Machine](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) [Monitor](/studynote/02_operating_system/04_synchronization/229_monitor/))는 단일 물리 서버(하드웨어)의 CPU, 메모리, I/O 자원을 논리적으로 쪼개어 여러 개의 독립된 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(가상 머신, [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))가 동시에 실행될 수 있게 조율하는 핵심 시스템 소프트웨어다.
> 2. **가치**: [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~20%에 머물던 물리 서버의 자원 활용률을 극대화하고, 하드웨어와 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 종속성을 완전히 분리(Decoupling)함으로써 오늘날의 [IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/) (Infrastructure [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) a [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 기반 [클라우드 컴퓨팅](/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/) 혁명을 탄생시킨 1등 공신이다.
> 3. **융합**: [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 소프트웨어 에뮬레이션의 심각한 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 극복하기 위해, CPU 제조사가 Ring -1(루트 모드)을 신설한 [하드웨어 보조 가상화](/studynote/02_operating_system/01_overview_architecture/059_hardware_assisted_virtualization/)([Intel VT-x](/studynote/01_computer_architecture/15_advanced_topics/658_intel_vtx/))와 메모리 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)(EPT) 기술이 OS 아키텍처와 완벽히 융합하여 네이티브 머신에 근접한 속도를 달성했다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong><a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a> (<a href="/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/">Virtualization</a>)</strong>: 컴퓨터 리소스의 물리적 특징을 숨기고, 사용자(OS나 앱)에게 논리적으로 분할되거나 통합된 가상의 자원을 제공하는 기술.
  - <strong><a href="/studynote/02_operating_system/01_overview_architecture/054_hypervisor/">하이퍼바이저</a> (<a href="/studynote/02_operating_system/01_overview_architecture/054_hypervisor/">Hypervisor</a>)</strong>: [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)를 구현하여 가상 머신([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))을 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 스케줄링, 모니터링하는 플랫폼 관리자. Guest OS 입장에서는 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 마치 진짜 물리 하드웨어처럼 보인다.

- **필요성(문제의식)**:
  - 과거 기업들은 DB용 서버, 웹 서버, 메일 서버를 각각 별도의 물리 서버 장비(베어메탈)로 샀다. 서로의 오류가 간섭하지 않게 하기 위해서였다.
  - 하지만 대부분의 서버는 CPU를 15%도 쓰지 않은 채 전력과 공간만 낭비했다 (Server Sprawl 문제).
  - **해결책**: "강력한 서버 1대를 사서 10대로 쪼갠 뒤, 각각 독립된 OS를 올려서 100% 꽉 채워 쓰자!" $\rightarrow$ 이를 조율할 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 필요해짐.

  - 물리 서버 1대에 1개의 OS만 돌리는 것은, 넓은 100평짜리 땅(물리 하드웨어)에 1인 가구(OS) 하나만 덩그러니 집을 짓고 사는 것이다.
  - <strong><a href="/studynote/02_operating_system/01_overview_architecture/054_hypervisor/">하이퍼바이저</a></strong>는 이 땅 위에 10층짜리 고층 아파트를 짓고, 층마다 완벽히 방음·단열된 10개의 독립된 집(가상 머신)을 만들어 10가구가 효율적으로 모여 살게 해주는 <strong>건물 관리 소장</strong>과 같다.

- **등장 배경**:
  - 1960년대 IBM 메인프레임에서 [시분할 시스템](/studynote/02_operating_system/01_overview_architecture/003_time_sharing_system/) 용도로 최초 등장.
  - 1990년대 후반 VMware가 x86 환경 아키텍처의 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 난제를 소프트웨어적 이진 변환(Binary Translation)으로 풀어내며 x86 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 시장이 폭발.
  - 이후 Intel/AMD가 하드웨어 차원의 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 추가하며 클라우드 시대로 폭발적 성장.

```text
  +-------------------------------------------------------------+
  |                 물리 서버 환경 vs 하이퍼바이저 가상화 환경            |
  +-------------------------------------------------------------+
  |                                                             |
  |  [ 전통적 물리 서버 (1:1 매핑) ]      [ 가상화된 서버 환경 (1:N 매핑) ]|
  |  +-------------+               +------+  +------+  +------+ |
  |  | App         |               | App  |  | App  |  | App  | |
  |  +-------------+               +------+  +------+  +------+ |
  |  | Windows OS  |               | Win  |  | Linux|  | UNIX | |
  |  +-------------+               +------+  +------+  +------+ |
  |  |             |                   ^         ^         ^      |
  |  | 하드웨어     |                   |         |         |      |
  |  | (CPU 15%사용)|               +---------------------------+ |
  |  +-------------+               |       하이퍼바이저 (VMM)     | |
  |                                +---------------------------+ |
  |  서버 1대당 OS 1개, 낭비 심함         |         물리 하드웨어        | |
  |                                |         (CPU 90% 활용)   | |
  |                                +---------------------------+ |
  |                                하이퍼바이저가 하드웨어 자원을 쪼개 배분 |
  +-------------------------------------------------------------+
```

**[다이어그램 해설]** [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경에서는 하드웨어 바로 위(또는 Host OS 위)에 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 계층이 삽입된다. [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)는 각 가상 머신(Guest OS)에게 "너 혼자 물리 CPU와 물리 메모리를 다 쓰고 있어"라는 환상(Illusion)을 심어준다. 여러 Guest OS가 동시에 특정 하드웨어(예: 네트워크 카드)를 쓰려고 할 때 발생하는 충돌을 트래픽 패킷 큐잉과 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 스위칭을 통해 투명하게 중재하는 것이 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)의 핵심 역할이다. 자원 낭비가 획기적으로 줄고, VM을 하나의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(이미지) 형태로 [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)/이동할 수 있어 인프라 관리가 소프트웨어 영역으로 편입되었다.

- **📢 섹션 요약 비유**: 하나의 큰 피자(하드웨어)를 한 사람이 먹다 남겨 버리던 것에서, 피자 자르기 달인([하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/))이 조각을 정확히 나누어 여러 사람([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))이 각자 취향에 맞는 토핑(OS)을 올려 배불리 나눠 먹게 된 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)의 2가지 아키텍처 타입

[하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 하드웨어 위 어느 계층에 위치하느냐에 따라 타입 1과 타입 2로 나뉜다.

| 구분 | Type 1 (Bare-metal / Native) | Type 2 (Hosted) |
|:---|:---|:---|
| **개념** | 물리 하드웨어 바로 위에 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 설치 (OS 역할 겸임) | 기존 일반 OS(Host OS) 위에 애플리케이션처럼 설치 |
| **구조** | 하드웨어 $\rightarrow$ [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) $\rightarrow$ Guest OS | 하드웨어 $\rightarrow$ Host OS $\rightarrow$ [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) $\rightarrow$ Guest OS |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>/오버헤드</strong>| 뛰어남 (오버헤드 매우 낮음, 직접 H/W 제어) | 상대적으로 낮음 (Host OS를 한 번 더 거치므로 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 발생) |
| **주 사용처** | 기업용 엔터프라이즈 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/), 클라우드 (AWS, Azure) | 개인용 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) (개발/테스트 환경) |
| **대표 솔루션** | VMware ESXi, Microsoft Hyper-V, Xen, [KVM](/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/) | VMware Workstation, [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) VirtualBox |

```text
  +-------------------------------------------------------------------+
  |                 Type 1 vs Type 2 하이퍼바이저 아키텍처 비교도         |
  +-------------------------------------------------------------------+
  |                                                                   |
  |      [Type 1 (Bare-metal 방식)]          [Type 2 (Hosted 방식)]     |
  |                                                                   |
  |    +-----+  +-----+  +-----+         +-----+  +-----+  +-----+    |
  |    | App |  | App |  | App |         | App |  | App |  | App |    |
  |    +-----+  +-----+  +-----+         +-----+  +-----+  +-----+    |
  |    | G.OS|  | G.OS|  | G.OS|         | G.OS|  | G.OS|  | G.OS|    |
  |    +--+--+  +--+--+  +--+--+         +--+--+  +--+--+  +--+--+    |
  |       |        |        |               |        |        |       |
  | +-----------------------------+  +-----------------------------+  |
  | |      하이퍼바이저 (ESXi)       |  |        하이퍼바이저 S/W      |  |
  | +--------------+--------------+  |        (VirtualBox)         |  |
  |                |                 +--------------+--------------+  |
  |                |                 +--------------+--------------+  |
  |                |                 |          Host OS            |  |
  |                v                 +--------------+--------------+  |
  | +-----------------------------+  +--------------+--------------+  |
  | |          Hardware           |  |          Hardware           |  |
  | +-----------------------------+  +-----------------------------+  |
  |   엔터프라이즈 서버 성능 최적화                개발자 데스크탑 테스트용          |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** Type 1은 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 자체가 얇은 특수 목적 OS처럼 동작하여 하드웨어 제어권을 100% 장악한다. 하드웨어 스케줄링이 직접 일어나므로 AWS EC2 같은 클라우드 인프라의 뼈대가 된다. 반면 Type 2는 윈도우나 맥 맥([Mac](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)) 같은 평범한 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(Host OS) 위에서 응용 프로그램 형태로 돈다. Guest OS가 메모리를 요구하면 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 Host OS에 다시 요청해야 하므로 병목(Overhead) 층이 하나 더 생긴다. (※ KVM의 경우 리눅스 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 자체가 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 모듈로 승격되므로 Type 1의 특성과 Type 2의 유연성을 겸비한 1.5 타입으로 불리기도 한다.)

---

### x86 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)의 난제와 진화 ([전가상화](/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) $\rightarrow$ [반가상화](/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) $\rightarrow$ [하드웨어 보조 가상화](/studynote/02_operating_system/01_overview_architecture/059_hardware_assisted_virtualization/))

CPU는 치명적인 특권 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(예: [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 비활성화, 메모리 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/))를 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드(Ring 0)에서만 실행한다. Guest OS는 자기가 진짜 OS인 줄 알고 Ring 0 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 날리지만, 실제 Ring 0는 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 차지하고 있고 Guest OS는 Ring 1에 밀려나 있다. 이 <strong>"권한 불일치(Privilege Deprivileging)"</strong>를 해결하는 기술의 진화가 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)의 핵심이다.

1. <strong><a href="/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/">전가상화</a> (<a href="/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/">Full Virtualization</a>) - Binary Translation</strong>: Guest OS가 날린 특권 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 실행 직전에 낚아채서([Trap](/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)), 소프트웨어적으로 안전한 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)로 번역(Translation)하여 재실행한다.
   - **장점**: Guest OS (예: Windows)를 1비트도 수정할 필요 없이 그대로 설치 가능.
   - **단점**: 소프트웨어 번역 과정의 엄청난 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 오버헤드.

2. <strong><a href="/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/">반가상화</a> (<a href="/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/">Paravirtualization</a>)</strong>: Guest OS의 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 소스코드를 수정하여, 특권 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 호출할 때 아예 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)에게 "나 이거 해줘"라고 부탁하는 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)(Hypercall)로 바꿔버린다.
   - **장점**: 번역을 안 하므로 네이티브에 가까운 고성능 (Xen 아키텍처).
   - **단점**: 소스코드를 깔 수 없는 Windows 같은 OS는 적용 불가 ([오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 리눅스만 개조 가능).

3. <strong><a href="/studynote/02_operating_system/01_overview_architecture/059_hardware_assisted_virtualization/">하드웨어 보조 가상화</a> (<a href="/studynote/13_cloud_architecture/01_virtualization/021_hardware_assisted_virtualization/">Hardware-Assisted Virtualization</a>)</strong>: CPU 제조사([Intel VT-x](/studynote/01_computer_architecture/15_advanced_topics/658_intel_vtx/), [AMD-V](/studynote/01_computer_architecture/15_advanced_topics/659_amd_v/))가 칩 설계를 바꿔서 근본적으로 해결함.
   - 기존 Ring 0 구조에 <strong>Root 모드(<a href="/studynote/02_operating_system/01_overview_architecture/054_hypervisor/">하이퍼바이저</a>용)</strong>와 <strong>Non-Root 모드(Guest OS용)</strong>를 신설함.
   - Guest OS는 Non-Root의 Ring 0에서 작동하며 자기가 진짜 OS인 줄 앎. 특권 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 날리면 CPU 하드웨어가 빛의 속도로 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)(Root 모드)로 제어권을 넘겨줌([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) Exit).
   - **현재 클라우드의 궁극적 표준** (수정 없는 OS + 하드웨어 가속 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)).

- **📢 섹션 요약 비유**:
  - [전가상화](/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/): 한국어(Guest OS)를 할 줄 모르는 미국인 사장(하드웨어) 옆에 통역사([하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/))가 붙어 모든 말을 번역해주는 방식 (느림).
  - [반가상화](/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/): 직원이 사장과 대화하기 위해 미리 사내 공용어(Hypercall)를 배워서 직접 소통하는 방식 (빠르지만 학습 비용 발생).
  - HW 보조 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/): 사장이 뇌에 '동시 통역 칩([Intel VT-x](/studynote/01_computer_architecture/15_advanced_topics/658_intel_vtx/))'을 이식해서 어떤 언어든 바로 알아듣게 만든 궁극적 해결책.

---

## Ⅲ. 비교 및 연결

### [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) ([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)) vs [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) ([Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)) 아키텍처 비교

[가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)의 거대한 라이벌이자 상호보완적 관계인 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)와 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 구조적 차이다.

| 비교 항목 | [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 기반 가상 머신 ([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)) | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) ([Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) - [Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/)) |
|:---|:---|:---|
| <strong><a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a> 수준</strong> | 하드웨어 수준 (Hardware-level) | [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준 (OS-level) |
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> 공유</strong> | 각 VM마다 독립된 무거운 Guest OS 부팅 | Host OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 1개를 모든 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 공유 |
| **부팅 속도/크기**| 수 분 소요 / 수 GB~수십 GB (무거움) | 수 초 이내 / 수십 MB (가벼움) |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/">격리성</a>/보안</strong> | 하드웨어 기반으로 완벽에 가까운 격리 (높음) | [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) 기반의 논리적 격리 ([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 뚫리면 다 뚫림) |
| **적합한 워크로드**| 완벽히 분리된 이기종 환경, 전통적 Monolithic DB | [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/), [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)), [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD |

```text
  +-------------------------------------------------------------------+
  |                 VM 아키텍처 vs 컨테이너 아키텍처의 격리성 차이           |
  +-------------------------------------------------------------------+
  |                                                                   |
  |     [VM (하이퍼바이저 가상화)]             [Container (OS 레벨 가상화)] |
  |    +-----++-----++-----+            +-----++-----++-----+       |
  |    | App || App || App |            | App || App || App |       |
  |    | Bins|| Bins|| Bins|            | Bins|| Bins|| Bins|       |
  |    +-----++-----++-----+            +-----++-----++-----+       |
  |    |G.OS ||G.OS ||G.OS |                (독립 OS 없음)            |
  |    +--+--++--+--++--+--+            +--------------------+       |
  |       |      |      |               |   Container Engine |       |
  |  +------------------------+         |     (Docker)       |       |
  |  |      Hypervisor        |         +--------------------+       |
  |  +------------------------+         |    Host OS Kernel  | <- 공유 |
  |  |   Hardware (서버)      |         +--------------------+       |
  |  +------------------------+         |   Hardware (서버)  |       |
  |                                     +--------------------+       |
  |  VM은 벽돌로 지은 완전히 분리된 3개의 집    컨테이너는 큰 집안에 친 3개의 커튼 방 |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 아키텍처는 격리를 위해 각 앱마다 수 기가바이트짜리 게스트 OS를 통째로 올려야 한다. 보안은 뛰어나지만 메모리 낭비가 심하다. [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 아키텍처는 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)와 게스트 OS를 완전히 도려내고, Host OS의 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(리눅스) 하나를 여럿이 공유한다. 앱 실행에 필요한 빈 공간(Bins/Libs)만 패키징하므로 초경량, [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 배포가 가능하다. 최근에는 VM의 강력한 [격리성](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/)과 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 가벼움을 합친 **마이크로VM (AWS Firecracker, Kata Containers)** 기술이 대세로 떠오르고 있다.

### 과목 융합 관점

- **컴퓨터 구조 (메모리)**: [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)는 메모리 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)의 병목을 없애기 위해 이중 [페이지 테이블](/studynote/02_operating_system/06_memory_management/353_page_table/) 번역을 해야 했다(가상 $\rightarrow$ 물리 $\rightarrow$ 머신 메모리). 이를 하드웨어로 가속하는 기술이 <strong>EPT (<a href="/studynote/01_computer_architecture/15_advanced_topics/661_extended_page_table/">Extended Page Table</a>) / NPT (<a href="/studynote/01_computer_architecture/15_advanced_topics/660_nested_page_table/">Nested Page Table</a>)</strong>이며, 이 덕분에 [TLB](/studynote/02_operating_system/06_memory_management/357_tlb/) 플러시 오버헤드가 극단적으로 줄었다.
- <strong>네트워크/I/O <a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a></strong>: 여러 VM이 하나의 물리 랜카드를 공유할 때 발생하는 병목을 해결하기 위해, [SR-IOV](/studynote/02_operating_system/08_storage_and_io_systems/497_sr_iov_pcie_mapping/) (Single Root I/O [Virtualization](/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/)) 기술을 사용해 물리 랜카드를 여러 개의 가상 인터페이스로 쪼개어 VM에 직접 패스스루([Direct](/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) [Passthrough](/studynote/02_operating_system/10_security/657_vfio_virtual_function_io_passthrough/))시켜 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)의 소프트웨어 개입을 없앤다.

- **📢 섹션 요약 비유**: VM이 아예 건물이 다른 '독채 펜션'이라 완벽히 프라이버시가 보장된다면, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)는 대형 체육관 안에 쳐놓은 '칸막이 텐트'라서 설치 철거는 순식간이지만 옆 텐트의 소음(보안/[커널 패닉](/studynote/02_operating_system/01_overview_architecture/036_kernel_panic/))에 영향을 받을 수 있는 트레이드오프가 존재합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — 클라우드 서버의 시끄러운 이웃 (Noisy Neighbor) 문제**: [퍼블릭 클라우드](/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)([IaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/183_iaas_infrastructure_as_a_service/))에서 우리가 임대한 VM의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 갑자기 뚝 떨어졌다. 분석 결과, 같은 물리 하드웨어에 입주한 다른 회사의 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)(이웃)이 CPU 캐시나 디스크 I/O를 독식하여 우리 VM까지 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)되는 현상 발생.
   - **아키텍트 판단 (자원 격리 튜닝)**: [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 단에서 논리적 분할만으로는 CPU L3 캐시나 메모리 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 대역폭의 물리적 경합을 100% 막을 수 없다. 중요도가 높은 DB 서버라면 퍼블릭 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 대신 <strong>베어메탈 인스턴스(Bare-metal Instance)나 전용 호스트(Dedicated Host)</strong>를 선택하여 하드웨어 레벨의 독점권을 확보하는 아키텍처 결정을 내려야 한다.

2. <strong>시나리오 — <a href="/studynote/11_design_supervision/01_audit_framework/079_developer_cleanroom_vdi_security/">VDI</a> (데스크톱 <a href="/studynote/13_cloud_architecture/01_virtualization/015_virtualization/">가상화</a>) 환경의 메모리 병목</strong>: 사내망 보안을 위해 1,000명의 직원에게 물리 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 대신 서버의 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 화면만 전송해주는 [VDI](/studynote/11_design_supervision/01_audit_framework/079_developer_cleanroom_vdi_security/) 환경 구축 중, 서버 메모리(RAM) 용량 한계에 부딪힘. (1000명 $\times$ 4GB OS = 4TB 메모리 필요).
   - **아키텍트 판단 (KSM 메모리 오버커밋)**: 1,000개의 윈도우 VM은 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 코드나 시스템 DLL [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 등 70% 이상의 메모리 내용이 완전히 똑같다. [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)의 <strong>메모리 중복 제거 기술 (KSM, <a href="/studynote/02_operating_system/10_security/631_ksm_kernel_samepage_merging/">Kernel Samepage Merging</a>)</strong>을 활성화하여, 똑같은 내용의 메모리 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 물리 메모리에 1개만 남기고 나머지는 포인터(Link)로 연결([COW](/studynote/02_operating_system/09_file_system/542_cow_file_system/) 상태)시킨다. 이를 통해 실제 물리 메모리보다 훨씬 많은 수의 VM을 구동하는 오버커밋(Overcommit) 효율을 달성한다.

```text
  +-------------------------------------------------------------------+
  |                 하이퍼바이저의 고급 메모리 관리 : KSM 원리               |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [가상 머신들의 논리 메모리]             [서버의 물리 메모리 (RAM)]       |
  |                                                                   |
  |   VM 1 (Windows)                                                  |
  |   +-- [kernel32.dll (블록 A)] ----+                               |
  |   +-- [엑셀 데이터 (블록 B)]     |                               |
  |                                  +-------> [물리 블록 A (공유)]   |
  |   VM 2 (Windows)                 |         (70% 중복 데이터 통합) |
  |   +-- [kernel32.dll (블록 A)] ----+                               |
  |   +-- [웹 브라우저 (블록 C)]     |                               |
  |                                  |                                |
  |   VM 3 (Windows)                 |                                |
  |   +-- [kernel32.dll (블록 A)] ----+                               |
  |   +-- [워드 데이터 (블록 D)]                                        |
  |                                                                   |
  |  ※ 만약 VM 1이 블록 A를 수정하려고 하면?                                |
  |     -> Copy-on-Write(COW) 발동: 수정 순간 새로운 물리 블록으로 복제하여 할당|
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 메커니즘은 클라우드 사업자의 이윤 창출 비밀 무기다. KSM 스레드는 백그라운드에서 VM들의 메모리 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 해시값을 비교하여 동일한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록을 찾아낸다. 그리고 물리 메모리에 단 하나만 남기고 병합해버린다. 결과적으로 사용자는 4GB 램을 할당받았다고 생각하지만, 클라우드 업체는 1GB의 물리 램만으로도 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 가능해져 서버 집적도(Density)가 극적으로 올라간다. 단, CPU가 메모리를 스캔하는 비용(오버헤드)이 발생하므로 적절한 튜닝이 필수다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong><a href="/studynote/02_operating_system/10_security/629_live_migration_pre_copy/">라이브 마이그레이션</a> (<a href="/studynote/02_operating_system/10_security/629_live_migration_pre_copy/">Live Migration</a>) 설계</strong>: 물리 서버 A에서 장애 징후가 보일 때, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 없이(Downtime < 1초) VM을 물리 서버 B로 실시간 이동시킬 수 있는 아키텍처(VMware vMotion)를 구성했는가? 이를 위해 양쪽 서버는 반드시 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/)/[NAS](/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/) 같은 공유 스토리지를 바라보고 있어야 한다.

- **📢 섹션 요약 비유**: 비행기 오버부킹처럼 클라우드([하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/))도 모든 승객([VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/))이 동시에 모든 자원을 쓰지 않는다는 통계적 사실을 믿고, 100석짜리 비행기에 150명의 표를 팔아 수익(자원 효율)을 극대화하는 교묘한 마법입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 레거시 물리 서버 인프라 | [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 기반 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (자원 활용률)** | 평균 CPU/RAM 사용률 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~15% | 워크로드 통합으로 평균 70~80% 달성 | 하드웨어 구매/유지보수 비용 대폭 절감 |
| <strong>정량 (<a href="/studynote/09_security/11_iam_access_control/528_provisioning/">프로비저닝</a>)</strong> | 서버 발주, 입고, OS 설치에 수 주 소요 | [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 이미지 복제로 5분 이내 인스턴스 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 타임 투 마켓(Time to Market) 가속 |
| <strong>정성 (장애 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a>)</strong> | 메인보드 고장 시 동일 하드웨어 수급 전까지 멈춤 | 하드웨어 비종속적. 다른 서버에서 즉시 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 재시작 | 고가용성(HA) 및 [재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/)([DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/)) 혁신 |

### 미래 전망
- <strong>마이크로 <a href="/studynote/02_operating_system/01_overview_architecture/054_hypervisor/">하이퍼바이저</a> (Micro-<a href="/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/">VM</a>)</strong>: [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)의 보안 약점을 해결하기 위해 AWS에서 개발한 Firecracker가 대표적이다. 전통적인 무거운 디바이스 드라이버 에뮬레이션을 싹 걷어내고 10밀리초(ms) 만에 부팅되는 초경량 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)로, [서버리스](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/)([Serverless](/studynote/12_it_management/05_security_compliance/206_serverless_cold_start/), AWS [Lambda](/studynote/14_data_engineering/05_exam_keywords/216_lambda_kappa_architecture_batch_realtime/)) 컴퓨팅의 폭발적 성장을 견인하고 있다.
- <strong>스마트 <a href="/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/">NIC</a> / <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/436_dpu/">DPU</a> <a href="/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/">오프로딩</a></strong>: [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)가 담당하던 네트워크 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)([vSwitch](/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/)), 패킷 보안, 스토리지 I/O 처리의 막대한 CPU 부하를 서버의 [DPU](/studynote/01_computer_architecture/12_accelerators_ai_hardware/436_dpu/)([Data Processing Unit](/studynote/06_ict_convergence/03_cloud_infrastructure/229_dpu_ipu_infrastructure_accelerator_offloading/)) 칩으로 [오프로딩](/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)하여, 서버 CPU의 100%를 오로지 사용자의 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 연산에만 쏟을 수 있게 하는 차세대 하드웨어 가속 아키텍처(AWS Nitro 시스템)가 글로벌 스탠다드로 자리 잡았다.

### 참고 표준
- <strong>OVM (Open <a href="/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/">Virtualization</a> Format)</strong>: 가상 머신 이미지를 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) 벤더(VMware, Xen, MS)에 상관없이 이식 가능하게 패키징하는 국제 표준 포맷(DMTF 제정).
- **libvirt**: 리눅스에서 다양한 [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)([KVM](/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/), QEMU 등)를 단일한 API로 관리할 수 있게 해주는 C 언어 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/). OpenStack, CloudStack의 토대.

[가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)는 컴퓨터 공학 역사상 "[추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)([Abstraction](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/))"의 힘을 가장 극적으로 증명한 기술이다. 하드웨어의 물리적 족쇄를 소프트웨어의 유연함으로 끊어냄으로써 자원의 무한 확장이 가능해졌고, 이 얇은 소프트웨어 계층 하나가 수십조 원 규모의 글로벌 클라우드 경제를 탄생시켰다.

- **📢 섹션 요약 비유**: 하드웨어라는 무거운 '점토'로 직접 빚어 만들던 서버 인프라가, [하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)라는 3D 프린터를 만나 언제든 복제하고 찍어내고 수정할 수 있는 무한한 '디지털 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)' 모델로 승격한 문명의 전환입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [버퍼 오버플로우 공격](/studynote/03_network/14_network_security_threats/731_buffer_overflow_stack_heap_aslr/) [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [스푸핑](/studynote/02_operating_system/10_security/598_spoofing/), [백도어](/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/) 악성코드 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [컨테이너 네임스페이스 격리](/studynote/02_operating_system/11_exam_summary/744_container_namespace_isolation/) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 시스템 클럭 타이머 틱 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[스푸핑, 백도어 악성코드]
    |
    v
[가상화 하이퍼바이저 (Virtualization Hypervisor)]
    |
    +---> [컨테이너 네임스페이스 격리]
    +---> [시스템 클럭 타이머 틱]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 옛날에는 컴퓨터 1대에 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)(윈도우) 1개만 깔 수 있어서, 능력이 엄청 좋은 컴퓨터가 매일 놀고 있었어요.
2. 그래서 똑똑한 기술자들이 '[하이퍼바이저](/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)'라는 마법의 방 쪼개기 기술을 만들었어요. 이 마법사가 컴퓨터 1대 안에 보이지 않는 방 10개를 만들어서 각자 윈도우, 리눅스를 따로 깔 수 있게 해줬죠.
3. 덕분에 비싼 컴퓨터를 10명이 나눠 쓰게 되어서 돈도 아끼고, 방 전체를 복사해서 다른 컴퓨터로 순식간에 이사(마이그레이션) 갈 수도 있게 되었답니다! 클라우드 세상의 일등 공신이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 743 / 800

<- **이전**: [742. 스푸핑, 백도어 악성코드 (Spoofing Backdoor Malware)](/studynote/02_operating_system/11_exam_summary/742_spoofing_backdoor_malware/)
**다음**: [744. 컨테이너 네임스페이스 격리 (Container Namespace Isolation)](/studynote/02_operating_system/11_exam_summary/744_container_namespace_isolation/) ->

---
