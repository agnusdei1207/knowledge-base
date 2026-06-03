+++
title = "578. 임의적 접근 제어 (DAC, Discretionary Access Control) - 소유자가 임의로 권한 위임"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: DAC은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 **소유자(Owner)**가 자기 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 대한 접근 권한을 **자유재량(Discretionary)**에 따라 타인에게 부여하거나 회수할 수 있는 방식이다. Unix/Linux의 `chmod` 명령어가 대표적이다.
> 2. **가치**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유 시 관리자의 개입 없이 **소유자가 직접 권한을 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)**하므로, 소규모 환경에서는 유연하고迅速(신속)한 협업이 가능하다.
> 3. **한계**: [Trojan Horse](/knowledge-base/studynote/02_operating_system/10_security/586_trojan_horse_wrapper/)([트로이 목마](/knowledge-base/studynote/02_operating_system/10_security/586_trojan_horse_wrapper/))와 같은 악성코드가 DAC 권한을 악용하면, 시스템 전체가 침해될 수 있다. 따라서 **[강제적 접근 제어](/knowledge-base/studynote/02_operating_system/10_security/579_mac_mandatory_access_control/)([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))와의 이중 구조**가 권장된다.

---

## Ⅰ. 개요 및 필요성

### 1.1 DAC의原理

DAC의 핵심 원칙은 **"자신이 소유한 객체에 대한 권한은 자발적으로 부여/회수 가능"**이다:

```bash
# Alice가 소유한 파일
-rw-r--r--  alice  alice  /home/alice/document.txt

# Alice가 Bob에게 읽기 권한 부여
$ chmod 744 /home/alice/document.txt
# 결과: alice만 읽기/쓰기, others는 읽기만
```

### 1.2 Unix/Linux의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 권한 구조

```text
[ 9비트 구조 ]
所有者(Owner)  Group   Others
   rwx          r-x     r--

[ 예시: chmod 750 ]
rwx r-x --- : Owner는 읽기/쓰기/실행, Group은 읽기/실행, Others는 접근 불가
```

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Trojan Horse의動作

1. 사용자가 악성 프로그램을 실행
2. 프로그램이 사용자의 **DAC 권한을 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)**받음
3. 악성 코드가 사용자 권한으로 시스템 자원에 접근

### 2.2 공격 시나리오

```text
[ 공격 흐름 ]
1. Alice가 malicious_program 실행
2. malicious_program이 Alice의 권한(Root)으로 실행 (DAC 상속)
3. 프로그램이 /etc/shadow 파일에 무단 접근 시도
4. Alice의 권한으로는 /etc/shadow에 접근 가능하므로 -> 공격 성공
```

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

| 구분 | DAC (임의적) | [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) (강제적) |
|:---|:---|:---|
| **권한 결정** | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 소유자가自行(자신) 결정 | 시스템 정책이強制(강제) 결정 |
| **대표 예시** | Unix `chmod`, Windows [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) | [SELinux](/knowledge-base/studynote/02_operating_system/10_security/583_selinux/), [AppArmor](/knowledge-base/studynote/02_operating_system/10_security/584_apparmor/) |
| **[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 관리** | 용이 (소유자 직접 관리) | 어려움 (중앙 관리자 필요) |
| **보안 수준** | 상대적 낮음 | 높음 |
| **유연성** | 높음 | 낮음 |

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **소규모 환경**에서는 DAC만으로 충분한 보안 수준을 달성할 수 있음
- **대규모/고보안 환경**에서는 DAC와 MAC의 이중 방어 체계가 필수적
- **클라우드 환경**에서는 [IAM](/knowledge-base/studynote/09_security/11_iam_access_control/526_iam/)(Identity and Access [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/))을 통해 DAC 원칙을 세밀하게 제어

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

임의적 접근 제어 (DAC, Discretionary [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/))은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [보호와 보안](/knowledge-base/studynote/02_operating_system/01_overview_architecture/043_protection_security/) 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [강제적 접근 제어](/knowledge-base/studynote/02_operating_system/10_security/579_mac_mandatory_access_control/) ([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/), Mandatory [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/))처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [자격 증명 리스트](/knowledge-base/studynote/02_operating_system/10_security/576_capability_list/) ([Capability List](/knowledge-base/studynote/02_operating_system/10_security/576_capability_list/) / Ticket) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 롤 기반 접근 제어 ([RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/), [Role-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [강제적 접근 제어](/knowledge-base/studynote/02_operating_system/10_security/579_mac_mandatory_access_control/) ([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/), Mandatory [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [벨-라파둘라 모델](/knowledge-base/studynote/02_operating_system/10_security/580_bell_lapadula_model/) ([Bell-LaPadula](/knowledge-base/studynote/02_operating_system/10_security/580_bell_lapadula_model/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[롤 기반 접근 제어 (RBAC, Role-Based Access Control)]
    │
    ▼
[임의적 접근 제어 (DAC, Discretionary Access Control)]
    │
    ├──▶ [강제적 접근 제어 (MAC, Mandatory Access Control)]
    └──▶ [벨-라파둘라 모델 (Bell-LaPadula)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. **DAC**는 아파트의 **"자가 관리 시스템"**과 같다. 각 세대의 소유자가 열쇠를 가지고 있고, 원하는 사람에게 열쇠를複製([복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/))하여 줄 수 있다.

2. **보안 문제**는 악의 있는 세입자가 **"집 주인에게 받은 열쇠"**를 악용하여 금고에 침입하는 것과 같다. 열쇠를 받은 입幌(사람)이 악용하면 시스템이 이를 차단할 수 없다.

3. **DAC와 MAC의二重(이중) 방어**는 **"자가 관리 + 건물 전체 경비 시스템"**과 같다. 세대 주인이 열쇠를 줘도, 경비원이 "이 사람은 금고 출입이 불가하다"고 차단할 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 578 / 800

← **이전**: [577. 롤 기반 접근 제어 (RBAC, Role-Based Access Control) - 사용자 대신 역할(Role)에 권한 할당](/knowledge-base/studynote/02_operating_system/10_security/577_rbac_role_based_access_control/)
**다음**: [579. 강제적 접근 제어 (MAC, Mandatory Access Control) - 시스템/보안 관리자가 등급 라벨 기반 강제 통제](/knowledge-base/studynote/02_operating_system/10_security/579_mac_mandatory_access_control/) →

---
