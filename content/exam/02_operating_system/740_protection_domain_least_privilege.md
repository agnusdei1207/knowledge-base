---
title: "Protection Domain Least Privilege"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [보호 도메인](/studynote/02_operating_system/10_security/572_protection_domain/) ([Protection Domain](/studynote/02_operating_system/10_security/572_protection_domain/))은 프로세스가 접근할 수 있는 자원(객체)과 그에 대한 권한(Access Right)의 집합을 정의하는 개념적 영역이며, [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/) (Principle of [Least Privilege](/studynote/09_security/01_intro_principles/010_least_privilege/), PoLP)은 특정 작업을 수행하는 데 필요한 '딱 그만큼의 권한'만 부여해야 한다는 시스템 보안의 대전제다.
> 2. **가치**: 불필요한 권한을 제거함으로써 특정 프로세스가 악성코드에 감염되거나 취약점이 노출되더라도, 해당 프로세스의 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 넘어 시스템 전체로 장애나 해킹 피해가 확산(Lateral Movement)되는 것을 구조적으로 차단한다.
> 3. **융합**: 과거에는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 링(Ring) 아키텍처나 UNIX의 프로세스 사용자 권한([SetUID](/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/)) 수준에 머물렀으나, 현대에는 클라우드 [IAM](/studynote/09_security/11_iam_access_control/526_iam/) (Identity and Access [Management](/studynote/12_it_management/05_security_compliance/1013_management/)), [컨테이너 보안](/studynote/04_software_engineering/11_testing_validation/905_container_security/) [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/), [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)) 아키텍처를 지탱하는 가장 기초적인 철학으로 자리 잡았다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong><a href="/studynote/02_operating_system/10_security/572_protection_domain/">보호 도메인</a> (<a href="/studynote/02_operating_system/10_security/572_protection_domain/">Protection Domain</a>)</strong>: 시스템 내의 객체([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 메모리 세그먼트, 프린터 등)에 대해 주체(프로세스, 사용자)가 가질 수 있는 접근 권한의 묶음. [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)은 $\langle 객체, 권한\_집합 \rangle$의 쌍으로 정의된다.
  - <strong><a href="/studynote/09_security/01_intro_principles/010_least_privilege/">최소 권한 원칙</a> (PoLP)</strong>: 어떤 주체가 작업을 수행할 때, 그 작업을 완수하기 위한 최소한의 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서만 실행되어야 한다는 보안의 기본 원칙.

- **필요성**:
  - 과거 단일 사용자 시스템에서는 모든 프로그램이 시스템의 모든 자원에 접근할 수 있었다. 그러나 다중 사용자, [다중 프로그래밍](/studynote/02_operating_system/11_exam_summary/673_multiprogramming_bottleneck_resource/) 환경에서는 하나의 버그나 악의적인 코드가 시스템 전체를 마비시킬 위험이 크다.
  - "만능 열쇠"를 가진 프로세스가 해킹당하면, 해커도 "만능 열쇠"를 쥐게 된다. 따라서 프로세스의 권한을 목적에 맞게 잘게 쪼개고 한정하는 메커니즘이 필수적이다.

  - <strong><a href="/studynote/09_security/01_intro_principles/010_least_privilege/">최소 권한 원칙</a></strong>: 회사 건물에서 '화장실 청소부'의 출입 카드에는 화장실과 청소 도구실 문만 열리는 권한을 주고, 서버실이나 사장실 문은 열리지 않게 설정하는 것과 같다.
  - 만약 편의를 위해 모든 문이 열리는 '마스터 키'를 주었다가 그 키를 도둑맞으면 회사 전체가 위험해진다.

- **등장 배경**:
  - 초기의 조잡한 권한 관리(예: root가 아니면 아무것도 못하는 시스템)의 한계 $\rightarrow$ 권한 위임과 전이([Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) Switching)의 필요성 대두 $\rightarrow$ Multics의 Ring [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 구조 및 UNIX의 [SetUID](/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/) 체계 도입 $\rightarrow$ 오늘날의 정교한 [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) 및 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 권한 제어로 진화.

```text
  +-------------------------------------------------------------+
  |                 보호 도메인 적용 전후의 시스템 침해 반경             |
  +-------------------------------------------------------------+
  |                                                             |
  |  [적용 전: 단일 거대 도메인 (Root 권한 남용)]                    |
  |   웹 서버 프로세스 (Root) ---(침해)---> [DB 파일 접근] (허용)    |
  |                                     +---> [비밀번호 변경] (허용)  |
  |       ^                             +---> [시스템 종료] (허용)   |
  |     해커 침투                                                |
  |  (웹 취약점 악용)                                             |
  |                                                             |
  |  [적용 후: 엄격하게 분리된 보호 도메인 (최소 권한)]                |
  |   웹 서버 도메인 (www-data) --(침해)---> [DB 파일 접근] (차단)    |
  |     |                                +---> [비밀번호 변경] (차단)  |
  |     +-- [웹 경로 읽기] (허용)            +---> [시스템 종료] (차단)   |
  |                                                             |
  |   결과: 해커가 웹 서버를 장악해도 그 도메인을 벗어날 수 없음.           |
  +-------------------------------------------------------------+
```

**[다이어그램 해설]** 이 그림은 [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)이 부재할 때 발생하는 '과잉 권한(Over-privileged)'의 위험성을 시각화한 것이다. 적용 전에는 웹 서버가 루트(Root) 권한으로 실행되어 공격자가 취약점을 통해 시스템 전체를 장악(Total Compromise)할 수 있다. 적용 후에는 웹 서버 프로세스를 오직 웹 문서만 읽을 수 있는 `www-data`라는 제한된 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 실행함으로써, 공격 성공 시에도 피해 반경(Blast [Radius](/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/))을 해당 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 내로 격리시킨다. 실무에서는 이를 가리켜 '가두리 양식([Sandboxing](/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/))'의 효과라고 부른다.

- **📢 섹션 요약 비유**: 은행 창구 직원이 자신의 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/) 화면([도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/))에서 고객의 입출금 업무만 할 수 있을 뿐, 은행 금고 자체를 여는 권한(최소 권한의 경계)은 없는 것과 같습니다. 이를 통해 직원이 협박을 받더라도 금고 전체가 털리는 일은 방지됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [보호 도메인](/studynote/02_operating_system/10_security/572_protection_domain/)의 구성 및 표현

[보호 도메인](/studynote/02_operating_system/10_security/572_protection_domain/)은 구조적으로 시스템 내 객체들의 접근 권한 매트릭스의 행(Row)으로 볼 수 있다.
[도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)은 프로세스의 신분(Identity)에 결속되며, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 주체가 어떤 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 실행되고 있는지 지속적으로 추적한다.

| 요소명 | 역할 | 내부 동작 | 기술적 예시 | 비유 |
|:---|:---|:---|:---|:---|
| <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 아이디 (<a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a> ID)</strong> | 프로세스가 속한 현재의 권한 영역 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | [프로세스 제어 블록](/studynote/02_operating_system/02_process_thread/090_pcb_tcb/)(PCB)에 UID/GID 형태로 저장 | UNIX의 `UID` (User ID), `EUID` (Effective UID) | 사원증의 부서 표시 |
| **객체 (Object)** | [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)되어야 할 시스템의 자원 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 메모리 영역, [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), 하드웨어 기기 등 | `/etc/passwd` [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 특정 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) | 금고, 문서 보관함 |
| **접근 권한 (Access Right)** | 해당 객체에 수행 가능한 연산의 종류 | Read, Write, Execute, Delete, Print 등 | `r-x`, `rw-` 등의 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)마스크 | 열람, 수정, 파기 권한 |
| <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 전환 (<a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a> <a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">Switch</a>)</strong> | 실행 중 일시적으로 다른 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)의 권한 획득 | 특정 조건을 만족할 때 시스템 콜을 통해 권한 레벨 변경 | UNIX의 `SetUID` 실행 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | 일일 임시 출입증 발급 |

### UNIX 환경에서의 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전환 원리 ([SetUID](/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/))

시스템을 운영하다 보면, 일반 사용자가 자신의 권한을 벗어나는 작업을 "제한적으로, 안전하게" 수행해야 할 때가 있다. 예를 들어, 일반 사용자가 자신의 비밀번호를 변경하려면 시스템의 중요 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)인 `/etc/shadow`를 수정해야 하지만, 이 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 오직 Root만 쓸 수 있다. 이 딜레마를 해결하는 것이 UNIX의 <strong><a href="/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/">SetUID</a> (Set User ID)</strong> 메커니즘을 통한 동적 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전환이다.

```text
  +-------------------------------------------------------------------+
  |                 UNIX SetUID 기반 보호 도메인 전환 흐름도                |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [사용자 도메인: UID=1000 (일반 사용자)]                                |
  |        |                                                          |
  |        | `$ passwd` 명령어 실행                                      |
  |        v                                                          |
  |  [파일 시스템 확인]                                                   |
  |  `/usr/bin/passwd` 파일 권한: `-rwsr-xr-x` (소유자: root)            |
  |   ※ 's' 비트(SetUID) 활성화 확인!                                     |
  |        |                                                          |
  |        v (도메인 전환 발생 - Domain Switch)                          |
  |  [프로세스 권한 일시 승격]                                              |
  |  - 실제 사용자(RUID) = 1000                                          |
  |  - 유효 사용자(EUID) = 0 (root) <-- 프로세스는 이제 root 도메인에서 실행!|
  |        |                                                          |
  |        v                                                          |
  |  [비밀번호 변경 로직 수행]                                             |
  |  `/etc/shadow` 파일 쓰기 작업 시도 -> OS가 EUID(0)를 보고 승인          |
  |        |                                                          |
  |        v (도메인 전환 복귀)                                           |
  |  [프로세스 종료]                                                     |
  |  EUID=0 상태가 해제되고, 시스템은 다시 안전 상태 유지                     |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 흐름도는 일반 사용자가 어떻게 시스템 권한을 잠시 빌려 작업을 수행하는지([Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) [Switch](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) 보여준다. `passwd` 실행 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 설정된 [SetUID](/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/) [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)(`s`)는, 이 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 실행될 때 프로세스의 유효 사용자 ID(EUID)를 프로그램을 실행한 사람이 아닌 프로그램의 '소유자(Root)'로 일시적으로 변경하라는 OS 차원의 특별한 약속이다. 따라서 사용자는 프로세스가 살아있는 동안만 좁은 범위의 미리 정의된 절차(비밀번호 암호화 후 저장)에 한해서만 Root의 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 진입할 수 있다. 만약 해커가 `passwd` 프로그램의 [버퍼 오버플로우](/studynote/02_operating_system/10_security/591_buffer_overflow/) 취약점을 발견하면, EUID가 0인 상태에서 셸([Shell](/studynote/02_operating_system/01_overview_architecture/044_shell/))을 실행시켜 완전한 Root 권한을 탈취하게 되므로 [SetUID](/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/) 프로그램은 극도로 엄격하게 작성되어야 한다.

- **📢 섹션 요약 비유**: 일반 직원이 금고에 직접 들어갈 수 없도록 막아두고, 대신 금고 문앞에 '비밀번호 변경 전용 로봇([SetUID](/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/) 프로그램)'을 배치해 직원들이 그 로봇을 통해서만 제한적으로 금고 내용을 업데이트할 수 있게 하는 구조입니다.

---

## Ⅲ. 비교 및 연결

### 권한 통제 메커니즘 비교 (링 구조 vs Capabilities)

[보호 도메인](/studynote/02_operating_system/10_security/572_protection_domain/)을 구현하고 통제하는 방식은 컴퓨터 아키텍처와 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 설계 철학에 따라 다양하게 발전했다.

| 비교 항목 | [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 링 ([Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/) Rings) 아키텍처 | 자격 증명 (Capabilities) 기반 시스템 | [접근 제어 목록](/studynote/02_operating_system/11_exam_summary/739_access_control_list_acl/) ([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) |
|:---|:---|:---|:---|
| **설계 사상** | 계층적 동심원 (하드웨어 레벨) | 주체 중심 (티켓 방식) | 객체 중심 (문지기 방식) |
| **작동 방식** | 권한이 높은 안쪽 링(Ring 0)과 낮은 바깥쪽 링(Ring 3)으로 분리, 안으로 갈수록 모든 권한 획득 | 프로세스가 특정 객체에 접근할 수 있는 암호화된 '토큰'을 소유함 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이나 객체에 접근 가능한 사용자 명단을 붙여둠 |
| **최소 권한 충족** | 낮음 (Ring 0에 들어가면 모든 것을 할 수 있어 남용 발생) | 매우 높음 (필요한 티켓만 배분 가능) | 높음 (명단에서 세밀하게 권한 분리 가능) |
| **적용 사례** | Intel x86 CPU의 User/[Kernel](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 모드 격리 | 미시적 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템, 객체 지향 OS | 리눅스/윈도우 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템, 클라우드 (S3) |

[보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 링 아키텍처의 구조적 한계를 통해 왜 현대 시스템이 더 세분화된 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 요구하는지 매트릭스를 넘어서 시각화할 수 있다.

```text
  +---------------------------------------------------------+
  |              보호 링(Protection Rings)의 계층적 구조         |
  +---------------------------------------------------------+
  |                                                         |
  |     +---------------------------------------------+     |
  |     | Ring 3: User Applications (일반 앱, 텍스트 에디터) |     |
  |     |   +-------------------------------------+   |     |
  |     |   | Ring 2: Device Drivers (디바이스 드라이버) |   |     |
  |     |   |   +-----------------------------+   |   |     |
  |     |   |   | Ring 1: OS Services         |   |   |     |
  |     |   |   |   +---------------------+   |   |   |     |
  |     |   |   |   | Ring 0: Kernel      |   |   |   |     |
  |     |   |   |   | (최고 권한, 무제한)    |   |   |   |     |
  |     |   |   |   +---------------------+   |   |   |     |
  |     |   |   +-----------------------------+   |   |     |
  |     |   +-------------------------------------+   |     |
  |     +---------------------------------------------+     |
  |                                                         |
  |  문제점: 바깥쪽 링에서 안쪽 링의 자원을 직접 접근할 수 없음.         |
  |         시스템 콜(System Call)을 통한 제한적 문(Gate)만 통과 가능.|
  |         그러나 Ring 0에 들어가면 다시 '단일 거대 도메인'이 되어 버림.|
  +---------------------------------------------------------+
```

**[다이어그램 해설]** 이 계층 구조도는 가장 전통적인 하드웨어 기반 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 격리 방식인 링 구조를 보여준다. 바깥쪽 링(Ring 3)에서 안쪽 링(Ring 0)의 메모리나 하드웨어 자원에 마음대로 접근하려 하면 하드웨어([MMU](/studynote/02_operating_system/06_memory_management/328_mmu/))가 [트랩](/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)([Trap](/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/))을 발생시켜 차단한다. 하지만 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부(Ring 0)로 들어가는 순간 [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)은 깨진다. 비디오 드라이버의 작은 버그 하나가 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 패닉을 일으켜 전체 시스템을 죽이는 현상(블루스크린)이 대표적인 예다. 이 때문에 현대 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 링 구조에만 의존하지 않고, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 기능을 최소화하는 [마이크로커널](/studynote/02_operating_system/01_overview_architecture/024_microkernel/)([Microkernel](/studynote/02_operating_system/01_overview_architecture/024_microkernel/)) 기법이나 소프트웨어 레벨의 강제 접근 제어([MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))를 덧붙여 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 더 잘게 쪼갠다.

### 과목 융합 관점

- <strong><a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> (DB)</strong>: [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 내에서도 계정(User)별로 특정 테이블, 특정 열(Column)에 대해서만 `SELECT`, `UPDATE` 권한을 부여하는 GRANT/REVOKE 메커니즘이 [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)의 완벽한 적용이다.
- **클라우드 (Cloud)**: AWS [IAM](/studynote/09_security/11_iam_access_control/526_iam/) (Identity and Access [Management](/studynote/12_it_management/05_security_compliance/1013_management/))의 철학은 처음부터 PoLP다. EC2 인스턴스에 S3 접근 권한을 줄 때 전체 관리자(AdministratorAccess) 권한을 주지 않고, 특정 S3 버킷의 읽기(s3:GetObject) 권한만 명시한 [IAM](/studynote/09_security/11_iam_access_control/526_iam/) Role([도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/))을 생성하여 부여한다.

- **📢 섹션 요약 비유**: 건물 전체를 겹겹이 두른 성벽(Ring 구조)만으로는 성 안의 스파이를 막을 수 없으므로, 각 방문마다 개별 자물쇠([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))를 달고 방문자에게 특정 방문만 열리는 맞춤형 열쇠(Capability)를 나누어 주는 방식으로 보안이 정교해지는 것입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — <a href="/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">Docker</a> <a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a>의 루트 권한 남용 (Privileged Escalation)</strong>: 개발팀이 배포 편의성을 위해 [도커](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 `--privileged` 옵션으로 실행했다. 이는 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 내부의 프로세스에게 호스트 시스템([커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))의 모든 권한을 열어주는 치명적 행위다. 애플리케이션의 원격 코드 실행(RCE) 취약점을 뚫은 해커가 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)를 탈출([Container](/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) Breakout)하여 호스트 머신 전체를 장악했다.
   - **아키텍트 판단 (PoLP 적용)**: `--privileged` 옵션 사용을 전면 금지하고, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)가 특정 호스트 기능(예: 네트워크 패킷 캡처)만 필요로 한다면 Linux Capabilities (예: `CAP_NET_ADMIN`)만을 선택적으로 추가 부여(add)해야 한다. 또한 호스트 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 마운트는 반드시 읽기 전용(Read-Only)으로 제한하여 [보호 도메인](/studynote/02_operating_system/10_security/572_protection_domain/)을 격리해야 한다.

2. <strong>시나리오 — 백그라운드 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>(Daemon)의 권한 축소</strong>: 전통적으로 Nginx나 Apache 같은 웹 서버는 80번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(Well-known [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))를 바인딩하기 위해 Root 권한으로 시작되었다. 그러나 웹 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 코드가 계속 Root로 돌면 해킹 시 서버 전체가 털린다.
   - <strong>아키텍트 판단 (<a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 전환 활용)</strong>: 데몬은 최초 실행 시에만 Root [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 80번 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 바인딩하고, 초기화가 끝나면 즉시 `setuid()`, `setgid()` 시스템 콜을 호출하여 권한이 제한된 `nobody` 또는 `www-data` 사용자의 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)으로 자발적으로 권한을 버리고 강등(Drop privileges)시켜야 한다.

안전한 백그라운드 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 설계의 권한 강등(Privilege Drop) 프로세스를 흐름도로 나타내면, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 시스템 콜이 어떻게 [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)을 실현하는지 알 수 있다.

```text
  +-------------------------------------------------------------------+
  |              데몬 프로세스의 자발적 권한 강등 (Privilege Drop) 플로우   |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [실행 초기: Root 도메인 (UID=0)]                                    |
  |         |                                                         |
  |         v                                                         |
  |   1. 소켓 생성 및 80/443 포트 바인딩 (Root만 가능)                     |
  |         |                                                         |
  |         v                                                         |
  |   2. 환경 설정 파일 읽기, 로그 파일 핸들 오픈 (Root 소유 파일)           |
  |         |                                                         |
  |         v                                                         |
  |   3. [보호 도메인 전환 실행 (자발적 강등)]                             |
  |      `setgid(www-data)` -> 그룹 권한 축소                           |
  |      `setuid(www-data)` -> 유저 권한 축소                           |
  |         |                                                         |
  |         v                                                         |
  |   [실행 중기~종료: www-data 도메인 (제한된 권한)]                       |
  |         |                                                         |
  |         v                                                         |
  |   4. 클라이언트의 HTTP 요청 수신 및 응답 처리                           |
  |      (이 상태에서 해킹당해도, 해커는 시스템의 주요 파일을 건드릴 수 없음)   |
  |                                                                   |
  |   핵심: "필요한 권한을 다 쓰고 나면, 프로세스 스스로 권한을 버려야 한다."      |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 다이어그램은 리눅스 환경에서 데몬 프로그램들이 [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)을 준수하기 위해 사용하는 표준적인 [시큐어 코딩](/studynote/12_it_management/05_security_compliance/190_secure_coding_guideline/) 패턴을 보여준다. 초기화 단계에서는 강력한 권한이 필요하지만, 지속적으로 요청을 처리하는 반복 구간에서는 공격에 노출될 위험이 크므로 권한을 버리는 것이다. 이는 한 번 낮춘 권한([도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/))은 다시 Root로 되돌릴 수 없는 UNIX의 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 보안 철학을 영리하게 이용한 아키텍처다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **운영·보안적**: 모든 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)가 고유의 [IAM](/studynote/09_security/11_iam_access_control/526_iam/) Role이나 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 어카운트([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Account)를 가지고 구동되는가? 특정 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 하나가 뚫려도 DB 전체를 삭제할 수 없는가?
- **관리자 권한 분리**: 시스템 관리자라고 해서 하나의 'Admin' 계정으로 모든 작업을 수행하지 않고, 일상 업무용 계정과 보안 설정용 계정으로 역할(Role)이 분리되어 있는가? ([망분리](/studynote/12_it_management/05_security_compliance/182_network_separation_model/) 원칙의 근간)

- **📢 섹션 요약 비유**: 요리사가 칼질을 할 때(초기화)는 위험하고 예리한 식칼(Root 권한)을 쓰지만, 칼질이 끝나면 즉시 칼을 보관함에 넣고 플라스틱 스푼(강등된 권한)으로만 요리를 섞는 것과 같습니다. 이는 요리 중 넘어지더라도 큰 상처를 입지 않게 하는 예방책입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 적용 전 (과잉 권한 환경) | 적용 후 ([최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/) 준수) | 개선 효과 |
|:---|:---|:---|:---|
| **정성 (장애 격리)** | 버그 발생 시 시스템 전역의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 훼손될 위험 | 버그나 악성 행위가 해당 프로세스의 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 내로 국한 | 수평적 확산(Lateral Movement) 차단 |
| <strong>정량 (<a href="/studynote/02_operating_system/10_security/606_auditing_linux_auditd/">감사</a> 로깅)</strong>| 수천 개의 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 중 원인 파악 불가 | [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 간의 경계를 넘는 비정상적 시도 탐지 (접근 거부 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)) | 침해 사고 분석(Forensics) 속도 대폭 단축 |
| **정성 (보안 컴플라이언스)**| [ISMS](/studynote/09_security/17_framework_compliance/836_iso_27001_isms/), ISO27001 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 심사 실패 위험 | [직무 분리](/studynote/09_security/11_iam_access_control/578_sod_segregation_of_duties/) 및 PoLP 입증으로 보안 심사 통과 보장 | 기업 [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 상승 및 규제 준수 |

### 미래 전망
- <strong><a href="/studynote/12_it_management/05_security_compliance/184_zero_trust_architecture/">제로 트러스트 아키텍처</a> (<a href="/studynote/12_it_management/05_security_compliance/184_zero_trust_architecture/">Zero Trust Architecture</a>)</strong>: 과거에는 "사내망(내부 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/))에 들어오면 신뢰한다"는 경계 기반 보안이 주류였으나, 이제는 "아무도 신뢰하지 말고 (Never Trust), 매 접근마다 최소 권한을 지속적으로 검증하라 (Always Verify)"는 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)로 진화했다.
- <strong><a href="/studynote/09_security/11_iam_access_control/568_jit_access/">JIT</a> (<a href="/studynote/09_security/11_iam_access_control/568_jit_access/">Just-In-Time</a>) 권한 부여</strong>: 개발자가 시스템에 접근할 때 상시적인 권한을 주는 대신, 작업이 필요한 정확히 그 시간(예: 1시간) 동안만 일시적으로 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 편입시켜주는 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 임시 권한 관리 시스템이 엔터프라이즈의 표준으로 정착하고 있다.

### 참고 표준
- <strong><a href="/studynote/09_security/17_framework_compliance/850_nist_sp_800_207/">NIST SP 800-207</a></strong>: [Zero Trust Architecture](/studynote/12_it_management/05_security_compliance/184_zero_trust_architecture/) 모델 및 최소 권한 적용 지침
- **ISO/IEC 27001**: 정보보호 관리체계([ISMS](/studynote/09_security/17_framework_compliance/836_iso_27001_isms/))의 접근 제어 및 [직무 분리](/studynote/09_security/11_iam_access_control/578_sod_segregation_of_duties/) 요구사항

[보호 도메인](/studynote/02_operating_system/10_security/572_protection_domain/)과 [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)은 귀찮은 제약이 아니라, 고도화된 IT 환경에서 거대한 시스템이 한 번의 실수로 산산조각 나는 것을 막아주는 격벽([Bulkhead](/studynote/04_software_engineering/05_devops_ci_cd/308_bulkhead_pattern/))이다. 권한을 섬세하게 분할하고 통제하는 인프라 설계 능력이 곧 아키텍트의 가장 중요한 역량이다.

- **📢 섹션 요약 비유**: 크루즈 여객선의 하단 선체가 여러 개의 독립된 방수 구획(격벽)으로 나뉘어 있어, 암초에 부딪혀 배의 한쪽이 찢어지더라도 해당 구역에만 물이 차고 배 전체는 침몰하지 않는 것과 완벽히 동일한 구조적 안정성입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [버퍼 캐시](/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 입출력 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [접근 제어 목록](/studynote/02_operating_system/11_exam_summary/739_access_control_list_acl/) ([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [버퍼 오버플로우 공격](/studynote/03_network/14_network_security_threats/731_buffer_overflow_stack_heap_aslr/) [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [스푸핑](/studynote/02_operating_system/10_security/598_spoofing/), [백도어](/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/) 악성코드 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[접근 제어 목록 (ACL)]
    |
    v
[보호 도메인 최소 권한 원칙 (Protection Domain Least Privilege)]
    |
    +---> [버퍼 오버플로우 공격 스택]
    +---> [스푸핑, 백도어 악성코드]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 세상에는 문을 열 수 있는 다양한 열쇠(권한)가 있어요.
2. 예전에는 편하다고 모든 문이 다 열리는 '마스터 키'를 사용했는데, 도둑이 이 열쇠를 훔치면 집 전체가 털리는 큰일이 났어요.
3. 그래서 이제는 '[최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)'이라는 규칙을 만들어서, 화장실 청소 로봇에게는 화장실 문만 열리는 열쇠를 주고 창고 로봇에게는 창고 열쇠만 주어서, 하나가 고장 나도 다른 곳은 안전하게 지키는 거랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 740 / 800

<- **이전**: [739. 접근 제어 목록 (ACL)](/studynote/02_operating_system/11_exam_summary/739_access_control_list_acl/)
**다음**: [741. 버퍼 오버플로우 공격 스택 (Buffer Overflow Attack Stack)](/studynote/02_operating_system/11_exam_summary/741_buffer_overflow_attack_stack/) ->

---
