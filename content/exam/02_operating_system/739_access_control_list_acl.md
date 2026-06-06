---
title: "ACL"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 접근 제어 목록([Access Control List](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/), [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))은 시스템 자원([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 폴더, 네트워크 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 등)에 대해 <strong>"어떤 사용자가, 어떤 권한(읽기/<a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a>/실행)을 가지고 있는가?"를 기록해 둔 명부(List)</strong>로, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 보안 아키텍처의 가장 근본적인 뼈대다.
> 2. **UNIX의 한계 극복**: 전통적인 UNIX의 `rwxrwxrwx` (소유자, 그룹, 기타) 방식은 단 3개의 분류만으로 권한을 퉁치기 때문에 섬세한 제어가 불가능했다. ACL은 이를 확장하여 <strong>"A직원은 읽기만, B직원은 <a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a>만, C그룹은 실행만"</strong> 식으로 무한대에 가까운 정밀한 권한 통제를 가능하게 한다.
> 3. **클라우드의 확장**: 단순히 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 권한을 통제하던 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 레벨의 ACL은 현대에 이르러 AWS S3의 버킷 권한, VPC의 네트워크 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)(NACL) 필터링 규칙 등으로 진화하여 인프라 전체의 트래픽을 거르고 승인하는 범용 보안 모델로 승격되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong>접근 제어 목록 (<a href="/studynote/02_operating_system/09_file_system/549_acl_access_control_list/">ACL</a>)</strong>: 객체(Object, 예: [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))에 부착된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조로, 어떤 주체(Subject, 예: 사용자/프로세스)가 해당 객체에 어떤 연산([Operation](/studynote/05_database/06_dw_olap_trends/329_delta_encoding/))을 수행할 수 있는지 정의한 목록.
  - <strong><a href="/studynote/02_operating_system/10_security/573_access_matrix/">접근 제어 행렬</a> (<a href="/studynote/02_operating_system/09_file_system/547_access_control_rwx/">Access Control</a> Matrix)</strong>: 시스템 전체의 주체와 객체의 권한 관계를 2차원 표(행렬)로 나타낸 이론적 모델. (이를 객체 기준으로 잘라낸 것이 ACL이다.)

- **필요성 (rwx의 낡은 족쇄 탈피)**:
  - 리눅스의 기본 권한 모델(UGO: User, Group, Others)은 너무 단순했다.
  - 내가 만든 `보고서.txt`를 100명의 직원 중 딱 '김 대리(읽기)'와 '이 과장([쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))'에게만 공유하고 싶다.
  - UGO 방식에서는 이걸 구현하려면 '김대리_이과장_그룹'이라는 새 그룹을 OS에 만들어야 했다. 부서 간 협업 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 늘어날수록 OS에 쓰레기 그룹이 수만 개 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 재앙이 터졌다.
  - **해결책**: "[파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 1개에다가 무제한으로 사람 이름과 권한을 계속 추가할 수 있는 유연한 리스트([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))를 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 직접 달아주자!"

  - **UGO (기존 방식)**: 클럽 입장 규칙이 "사장(User) 무료, VIP 회원(Group) 1만 원, 나머지(Others) 5만 원" 3개뿐이다. 사장님 친구 한 명만 무료로 들이려면 그 친구를 강제로 사장으로 만들거나 VIP로 승급시켜야 한다.
  - <strong><a href="/studynote/02_operating_system/09_file_system/549_acl_access_control_list/">ACL</a> (현대 방식)</strong>: 클럽 입구에 아주 긴 '게스트 명단(List)'이 있다. "A는 무료, B는 1만 원, C는 입장 금지..." 몇 명이든 세세하게 명단에 적어서 정확히 통제할 수 있다.

- **발전 과정**:
  1. **UGO (전통적)**: UNIX 시스템의 근간. 9비트(rwxrwxrwx) 체계.
  2. <strong>POSIX <a href="/studynote/02_operating_system/09_file_system/549_acl_access_control_list/">ACL</a></strong>: 리눅스/유닉스 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템에 [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) 규격 확장 (setfacl, getfacl).
  3. <strong>Windows <a href="/studynote/02_operating_system/09_file_system/549_acl_access_control_list/">ACL</a> (NTFS)</strong>: [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)뿐만 아니라 [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/), 프로세스 등 윈도우의 모든 객체에 적용되는 완벽한 객체 지향 [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/).

- **📢 섹션 요약 비유**: 3가지 사이즈(S, M, L)로만 사람을 나누던 기성복 시대(UGO)에서, 개인의 체형 치수 10군데를 세밀하게 재서 딱 맞춰주는 맞춤형 양복([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) 시대로의 진화입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [접근 제어 행렬](/studynote/02_operating_system/10_security/573_access_matrix/)([Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Matrix)과 ACL의 추출

[운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 교과서에 나오는 완벽한 보안 모델은 거대한 2차원 행렬이다.

| 주체 (Subject) \ 객체 (Object) | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) A (인사기록) | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) B (주간보고) | 프린터 C |
|:---|:---:|:---:|:---:|
| **사용자 1 (CEO)** | `Read`, `Write` | `Read`, `Write` | `Print` |
| **사용자 2 (HR팀)** | `Read` | `Read` | - |
| **사용자 3 (인턴)** | - | `Read` | `Print` |

이 거대한 행렬을 그대로 메모리에 올리면 너무 크고 텅 빈 칸이 많아 낭비다(Sparse Matrix). 이를 구현하는 두 가지 방식이 있다.

1. **객체 관점으로 열(Column)을 자르기 $\rightarrow$ [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) ([Access Control List](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))**
   - `파일 A의 ACL` = [CEO: R/W], [HR팀: R]
   - 각 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(객체)의 i-node나 메타데이터에 명단을 달아둔다. (가장 보편적)
2. **주체 관점으로 행(Row)을 자르기 $\rightarrow$ [Capability List](/studynote/02_operating_system/10_security/576_capability_list/) (자격 증명)**
   - `인턴의 Capability` = [파일 B: R], [프린터 C: Print]
   - 각 사용자(주체)가 놀이공원 자유이용권처럼 자기가 쓸 수 있는 티켓 묶음을 들고 다닌다.

---

### 리눅스 POSIX [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) 동작 메커니즘 (Extended [Attributes](/studynote/02_operating_system/09_file_system/502_file_attributes_metadata/))

"원래 i-node에는 rwxrwxrwx [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)(2바이트)밖에 저장 공간이 없는데 어떻게 길쭉한 ACL을 저장할까?"

```text
  +-------------------------------------------------------------------+
  |                 리눅스 파일 시스템의 ACL 저장 및 검증 아키텍처            |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [ 1. 파일 시스템 (ext4) 구조 ]                                       |
  |   - 파일 `report.txt`의 [i-node] 블록 (기본 권한: `rw- r-- r--`)      |
  |   - i-node 안에 저장 공간이 모자라므로, OS는 **확장 속성(xattr)** 영역이라는 |
  |     숨겨진 별도의 디스크 블록을 할당하여 ACL 데이터를 기록함.                |
  |                                                                   |
  |  [ 2. 권한 검사 (Access Check) 로직 ]                                |
  |   - 유저 '철수'가 `report.txt`에 Write 요청!                        |
  |                                                                   |
  |   ① 철수가 이 파일의 Owner(소유자)인가?                               |
  |      -> 아니오.                                                   |
  |                                                                   |
  |   ② 철수라는 이름이 파일의 [ACL 명단]에 명시적으로 있는가?                |
  |      -> `getfacl` 조회: `user:철수:rw-` 발견!                       |
  |      ★ 통과! (기본 Group이나 Other 권한보다 명시적 ACL을 우선함)          |
  |                                                                   |
  |   ③ 만약 ACL에도 철수가 없다면?                                       |
  |      -> 철수가 속한 그룹이 ACL에 있는지 검사 -> 통과/실패                 |
  |                                                                   |
  |   ④ 그것도 없다면? -> 기본 `Other` 권한(r--)을 적용하여 Write 차단.     |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 리눅스에서 `ls -l`을 쳤을 때 권한 끝에 `+` 기호가 붙어있으면(`-rw-rwxr--+`) 숨겨진 ACL이 존재한다는 뜻이다. [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/)(가상 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템)는 이 `+` 기호를 보면, 단순한 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)마스크 검사를 넘어 무거운 `xattr` 블록을 뒤져 권한을 파싱하는 다단계 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 로직을 타게 된다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### DAC vs [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) vs [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/) (접근 제어 모델 3대장)

ACL은 그저 '목록'일 뿐이다. 이 목록을 누가 통제하느냐에 따라 보안 철학이 갈린다.

| 모델 | 영문 명칭 | 통제 주체 (권한자) | 특징 및 사용처 |
|:---|:---|:---|:---|
| **DAC** | Discretionary [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/) | <strong><a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 소유자 (Creator)</strong> | 소유자가 내 맘대로 남에게 권한을 줌 ([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) 기반). 일반 리눅스/윈도우의 기본 모델. 유연하나 보안 구멍이 많음. |
| <strong><a href="/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a></strong> | Mandatory [Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/) | <strong><a href="/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a> 관리자 (System)</strong> | 소유자조차 남에게 권한을 못 줌. OS가 정해둔 보안 등급(1급 기밀 등) 규칙만 따름 ([SELinux](/studynote/02_operating_system/10_security/583_selinux/), 군사 시스템). |
| <strong><a href="/studynote/09_security/11_iam_access_control/569_rbac/">RBAC</a></strong>| [Role-Based Access Control](/studynote/09_security/11_iam_access_control/569_rbac/) | **역할 (Role)** | 사람(사번)에게 권한을 주지 않고 '회계팀장'이라는 직책에 권한을 줌. 부서 이동 시 권한 관리가 매우 쉬움 (현대 기업 표준). |

### 과목 융합 관점

- **클라우드 / 네트워크 (NACL)**: [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) 개념이 네트워크로 그대로 복사되었다. AWS의 VPC에는 <strong>NACL (<a href="/studynote/09_security/05_web_app_security/226_nac_network_access_control_ieee_802_1x/">Network Access Control</a> List)</strong>이 있다. 서브넷 앞단에 명부(List)를 두고, 패킷이 들어올 때 출발지 IP, [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 번호를 명부와 하나씩 대조하여 Allow/Deny를 결정하는 완벽한 네트워크 층의 ACL이다.
- <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> <a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a> (S3 / <a href="/studynote/09_security/11_iam_access_control/526_iam/">IAM</a>)</strong>: 클라우드 [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)(S3)는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 업로드한 사람 외에 불특정 다수에게 권한을 줄 때, 폴더나 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)마다 S3 Bucket Policy와 Object ACL이라는 거대한 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 형태의 텍스트 명부를 달아 글로벌 인터넷 상의 접근을 통제한다.

- **📢 섹션 요약 비유**: DAC는 내가 산 피자를 누구한테 한 조각 줄지 내 마음대로 결정하는 것이고, MAC은 군대 배식처럼 취사병(OS)이 정해준 정량만 먹고 절대 남에게 덜어줄 수 없는 것입니다. ACL은 보통 내 맘대로 권한을 주는 DAC 모델을 구체화하는 가장 편한 도구입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — 사내 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 서버(Samba/<a href="/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/">NAS</a>)의 권한 파편화 지옥</strong>: 스타트업에서 리눅스 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버를 1대 띄우고 `setfacl` 명령어로 직원 100명에게 폴더마다 개별적으로 ACL을 부여했다. 직원이 퇴사하고 입사할 때마다 서버 관리자가 터미널에서 스크립트를 수십 줄씩 돌리다가 실수로 기밀문서 권한이 뚫림.
   - **원인 분석**: 사용자 1명 1명을 객체의 ACL에 직접 맵핑하는 짓은 사용자 수가 10명을 넘어가는 순간 관리 불가능한 스파게티([Management](/studynote/12_it_management/05_security_compliance/1013_management/) Hell)가 된다.
   - <strong>대응 (<a href="/studynote/09_security/11_iam_access_control/569_rbac/">RBAC</a> 아키텍처 전환)</strong>: [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 ACL에는 사람 이름(홍길동)을 적지 마라. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에는 <strong>'인사팀장(Role)', '재무팀원(Role)'이라는 역할만 ACL에 등록(Group <a href="/studynote/02_operating_system/09_file_system/549_acl_access_control_list/">ACL</a>)</strong>한다. 그리고 OS의 [Active Directory](/studynote/09_security/11_iam_access_control/548_active_directory/)(AD)나 [LDAP](/studynote/03_network/10_application_layer_dns_mgmt/543_ldap_lightweight_directory_access_protocol/) 서버에서 홍길동을 '인사팀장' 그룹에 맵핑시킨다. 홍길동이 퇴사하면 AD 서버에서 체크만 해제하면 끝이다. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 ACL은 단 한 줄도 수정할 필요가 없다 (관심사의 분리).

2. <strong>시나리오 — AWS S3의 퍼블릭 노출 (<a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">Data</a> Breach) 대참사</strong>: 개발자가 S3 버킷에 이미지를 올리면서 "앱에서 이미지가 안 보여요!" 하니까, 귀찮아서 S3 콘솔의 Object ACL을 `Everyone (Public Access) - Read`로 풀어버림. 며칠 뒤 버킷에 있던 1억 명의 고객 개인정보가 인터넷에 전부 털림.
   - **원인 분석**: 클라우드의 ACL은 로컬 PC와 달리 전 세계 해커들이 스캔하고 있다. 특정 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 1개만 열어준다는 의도였으나, 버킷([디렉터리](/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)) 전체의 [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)(Inheritance) [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 때문에 모든 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 ACL이 뚫린 것이다.
   - **기술사적 가이드**: 현대 클라우드 아키텍처에서는 개별 객체의 <strong><a href="/studynote/02_operating_system/09_file_system/549_acl_access_control_list/">ACL</a> 사용을 원칙적으로 금지(ACLs Disabled)</strong>한다. AWS도 최근 S3 버킷 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) 비활성화를 디폴트로 걸어버렸다. 대신, 중앙 통제소인 <strong><a href="/studynote/09_security/11_iam_access_control/526_iam/">IAM</a> (Identity and Access <a href="/studynote/12_it_management/05_security_compliance/1013_management/">Management</a>)</strong> 정책이나 Bucket Policy를 통해서만 권한을 부여하게 하여, 눈에 안 띄는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 하나의 [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) 오작동으로 인한 대형 보안 사고를 원천 차단한다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 엔터프라이즈 접근 제어(Access Control) 모델 설계 플로우   |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [사내 인트라넷, DB, 클라우드 자원에 대한 직원들의 접근 권한을 설계함]          |
  |                |                                                  |
  |                v                                                  |
  |      자원의 소유자(개발자)가 임의로 동료에게 권한을 넘겨주어도 무방한가?       |
  |          +- 예 ------> [DAC 모델 (전통적 ACL / xattr) 허용]           |
  |          |            (개발 편의성 높음. 빠르고 유연한 스타트업 문화에 적합)   |
  |          +- 아니오 (국방망, 금융망, 망분리 환경 등 규제가 엄격한 곳이다)     |
  |                |                                                  |
  |                v                                                  |
  |      중앙 보안팀이 모든 권한을 100% 통제하고 감시해야 하는가?               |
  |          +---> [RBAC (역할 기반) + MAC (강제 접근 제어) 도입 필수]      |
  |          |    결론: 리눅스의 SELinux나 AppArmor를 Enforcing 모드로 켜서, |
  |          |          루트(root)조차도 파일의 ACL을 함부로 바꾸지 못하게 막음. |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** "권한 꼬이면 그냥 `chmod 777` 쳐서 해결하세요"는 주니어 시절에나 용납되는 끔찍한 안티 패턴이다. 아키텍트는 777(UGO)의 몽둥이를 치우고, 정교한 [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) 매스(Scalpel)를 쥐어주어 <strong>'최소 권한의 원칙(Principle of <a href="/studynote/09_security/01_intro_principles/010_least_privilege/">Least Privilege</a>)'</strong>을 시스템이 강제로 지키도록 조각해야 한다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>Default <a href="/studynote/02_operating_system/09_file_system/549_acl_access_control_list/">ACL</a> (<a href="/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/">상속</a>성)</strong>: 리눅스 폴더에 ACL을 걸었는데, 그 안에 새로 만든 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에는 권한이 적용 안 돼서 에러가 난 적이 있는가? `setfacl -d` (Default) 옵션을 주어 부모 폴더의 [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) 명부가 자식 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 태어날 때 자동으로 [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)(Inheritance)되게 세팅해야만 [디렉터리](/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 지옥을 피할 수 있다.

- **📢 섹션 요약 비유**: 수만 명의 직원이 일하는 회사에서 지문 인식기([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))마다 직원들의 지문을 일일이 등록하는 건 바보짓입니다. 사원증(Role)에 출입 권한([RBAC](/studynote/09_security/11_iam_access_control/569_rbac/))을 심어 중앙 컴퓨터(AD)에서 통제하는 것이 현대 접근 제어의 마스터플랜입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 기본 UGO 권한 (rwx) | [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) ([Access Control List](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)) | 개선 효과 |
|:---|:---|:---|:---|
| **정성 (권한 입도)** | 3그룹(소유자,그룹,기타) 거시적 제어 | 개인별/부서별 정밀한([Fine-grained](/studynote/01_computer_architecture/11_multicore_synchronization/399_fine_grained_multithreading/)) 제어 | [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)(PoLP) 완벽 구현 |
| **정성 (보안 사고)** | 권한 부족 시 777 등 전체 권한 남용 | 특정인에게만 Read 허용 | 내부자 위협(Insider Threat) 방어력 극대화 |
| **정량 (OS 오버헤드)**| i-node 내부 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)맵 비교 ([초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/)) | xattr 블록 디스크 탐색 및 리스트 순회 | (트레이드오프) 약간의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 오픈 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Overhead) 발생 |

### 미래 전망
- <strong><a href="/studynote/09_security/11_iam_access_control/572_abac/">ABAC</a> (<a href="/studynote/09_security/11_iam_access_control/572_abac/">Attribute-Based Access Control</a>)로의 진화</strong>: 리스트에 이름을 적는 ACL이나 직책을 적는 RBAC를 넘어, 차세대 보안은 ABAC로 향하고 있다. 사용자의 [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)(현재 접속 위치가 한국인가? 사용 기기가 맥북인가? 현재 시간이 오전 9시인가?)을 종합적으로 평가하는 '[속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) 기반 제어' 모델이다. "홍길동이라도 주말에 집에서 아이패드로 접속하면 DB 접근 불가" 같은 동적 룰이 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 아키텍처의 핵심 심장으로 뛰고 있다.

### 결론
접근 제어 목록([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))은 "모든 것을 열어두면 망하고, 모든 것을 닫아두면 시스템이 아니다"라는 컴퓨터 공학의 모순을 해결하기 위해 짜여진 가장 치밀한 그물망이다. 단순한 9비트의 벽을 허물고 무한한 리스트를 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 꼬리에 매달아 줌으로써, [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 수만 명의 사용자가 하나의 거대한 디스크 위에서 각자의 권리를 안전하게 영위하는 진정한 다중 사용자(Multi-user) 생태계를 완성했다. 클라우드와 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템으로 무대가 옮겨진 지금도, "누구에게 이 문을 열어줄 것인가"를 기록하는 ACL의 명부는 여전히 모든 인프라 보안의 0순위 성역으로 존재한다.

- **📢 섹션 요약 비유**: 성벽의 문지기에게 "우리 성 소속이면 들여보내고, 아니면 쏴라"라고 대충 지시(UGO)하면 스파이가 들어오거나 귀빈이 쫓겨납니다. 문지기에게 두꺼운 얼굴 사진첩과 명부([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))를 쥐여주는 것은 귀찮고 돈이 드는 일이지만, 왕국([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 지키기 위한 절대 타협할 수 없는 보험입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [VFS](/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 가상 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [버퍼 캐시](/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 입출력 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [보호 도메인](/studynote/02_operating_system/10_security/572_protection_domain/) [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [버퍼 오버플로우 공격](/studynote/03_network/14_network_security_threats/731_buffer_overflow_stack_heap_aslr/) [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[버퍼 캐시 파일 입출력 지연]
    |
    v
[접근 제어 목록 (ACL)]
    |
    +---> [보호 도메인 최소 권한 원칙]
    +---> [버퍼 오버플로우 공격 스택]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 철수는 보물상자에 자물쇠를 걸어두고, 평소에는 '가족'만 열 수 있게 비밀번호를 맞췄어요(기본 권한).
2. 그런데 어느 날 단짝 친구인 짱구에게만 딱 하루 보물상자를 열게 해주고 싶어졌어요! 짱구를 가족으로 만들 순 없잖아요?
3. 그래서 철수는 보물상자 옆에 '허락 명단([ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))'이라는 쪽지를 하나 붙이고 "짱구는 열어봐도 됨!"이라고 썼어요. 자물쇠는 이 쪽지를 보고 짱구에게만 특별히 상자를 열어준답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 739 / 800

<- **이전**: [738. 버퍼 캐시 파일 입출력 지연 (Buffer Cache File I/O Delayed Write)](/studynote/02_operating_system/11_exam_summary/738_buffer_cache_file_io_delayed_write/)
**다음**: [740. 보호 도메인 최소 권한 원칙 (Protection Domain Least Privilege)](/studynote/02_operating_system/11_exam_summary/740_protection_domain_least_privilege/) ->

---
