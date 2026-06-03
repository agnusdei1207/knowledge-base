+++
title = "575. 접근 제어 목록 (ACL, Access Control List) - 객체 중심 (해당 객체에 접근 가능한 주체 목록)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)([접근 제어 목록](/knowledge-base/studynote/02_operating_system/11_exam_summary/739_access_control_list_acl/))은 [접근 제어 행렬](/knowledge-base/studynote/02_operating_system/10_security/573_access_matrix/)을 **객체([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)) 기준**으로 분할하여, 각 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 "누구(Object)가 어떤 권한(Subject)을 가지는지" 목록을 저장하는 방식이다.
> 2. **가치**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 접근 시 해당 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 ACL만 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하면 되므로 **중앙 테이블 탐색 없이** $O(1)$ 시간에 접근 권한을 검증할 수 있다.
> 3. **한계**: 사용자가 퇴사하거나 권한을 회수할 때, 해당 사용자가 포함된 **모든 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 ACL을 찾아 업데이트**해야 하는 $O(N)$ 작업이 필요하다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [전역 테이블](/knowledge-base/studynote/02_operating_system/10_security/574_global_table/)의 한계

[전역 테이블](/knowledge-base/studynote/02_operating_system/10_security/574_global_table/)에서는 사용자 퇴사 시:
- 시스템의 **모든 권한 [튜플](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/)**을 스캔
- 해당 사용자가 포함된 [튜플](/knowledge-base/studynote/05_database/02_modeling_normalization/063_relation_tuple_cardinality/)을 모두 삭제

수백만 개 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 환경에서 이는 **수시간에서 수일**이 소요될 수 있다.

### 1.2 ACL의 해결책

ACL은 **"[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(Object)와/과에(각각)"** 권한 목록을 저장한다:

```text
[ 파일 A의 ACL ]
- 사용자A: {Read, Write}
- 사용자B: {Read}

[ 파일 B의 ACL ]
- 사용자B: {Read, Write}
- 사용자C: {Read}
```

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) vs Capability: 두 가지 분할 방식

| 구분 | [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) (행 분할) | Capability (열 분할) |
|:---|:---|:---|
| **분할 기준** | 객체([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)) 기준 | 주체(사용자) 기준 |
| **저장 위치** | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) inode에 부착 | 프로세스 PCB에 저장 |
| **권한 회수** | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) ACL에서 삭제 ($O(1)$) | 모든 프로세스 티켓 회수 ($O(N)$) |
| **사용자 조회** | 해당 사용자가 접근 가능한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 탐색 어려움 | 사용자의 티켓 목록만 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) ($O(1)$) |

### 2.2 Unix/Linux의 [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/): 9비트 시스템

전통적인 Unix/Linux의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 권한은 **3group × 3bit = 9bit** 구조다:

```text
[ 예: chmod 755 file.txt ]
rwxr-xr-x (Owner: 7=rwx, Group: 5=r-x, Others: 5=r-x)
```

이는 simplified ACL로, **소유자/그룹/기타** 세 가지 항목만 관리한다.

### 2.3 확장 [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)

현대 시스템에서는 세밀한 ACL을 지원한다:

```bash
# Linux 확장 ACL 설정
setfacl -m u:alice:rw /data/report.txt
# 사용자 alice에게 report.txt에 읽기/쓰기 권한 부여
```

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 3.1 Windows 보안 탭

Windows 탐색기에서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 우클릭 → [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/) → 보안 탭에서 보는 것이 바로 **NTFS [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)**이다.

### 3.2 [ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) 항의구조

```text
[ NTFS ACL 항목 ]
Principal (사용자/그룹) | Access Type (허용/거부) | Permissions (권한)
alice | Allow | Read, Write
NETWORK SERVICE | Deny | Full Control
```

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **권한 회수의 용이성**: 특정 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 권한 변경 시 해당 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) ACL만 수정
- **[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 관리**: 각 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 소유자가 직접 권한을 관리 가능
- **역방향 조회 어려움**: "이 사용자가 접근 가능한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 목록" 조회 시 전체 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스캔 필요

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

[접근 제어 목록](/knowledge-base/studynote/02_operating_system/11_exam_summary/739_access_control_list_acl/) ([ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/), [Access Control List](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/))은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [보호와 보안](/knowledge-base/studynote/02_operating_system/01_overview_architecture/043_protection_security/) 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [자격 증명 리스트](/knowledge-base/studynote/02_operating_system/10_security/576_capability_list/) ([Capability List](/knowledge-base/studynote/02_operating_system/10_security/576_capability_list/) / Ticket)처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [접근 제어 행렬](/knowledge-base/studynote/02_operating_system/10_security/573_access_matrix/) ([Access Matrix](/knowledge-base/studynote/02_operating_system/10_security/573_access_matrix/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [전역 테이블](/knowledge-base/studynote/02_operating_system/10_security/574_global_table/) ([Global Table](/knowledge-base/studynote/02_operating_system/10_security/574_global_table/)) 방식 구현 (행렬 희소성 문제) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [자격 증명 리스트](/knowledge-base/studynote/02_operating_system/10_security/576_capability_list/) ([Capability List](/knowledge-base/studynote/02_operating_system/10_security/576_capability_list/) / Ticket) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 롤 기반 접근 제어 ([RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/), [Role-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[전역 테이블 (Global Table) 방식 구현 (행렬 희소성 문제)]
│
▼
[접근 제어 목록 (ACL, Access Control List)]
│
├──▶ [자격 증명 리스트 (Capability List / Ticket)]
└──▶ [롤 기반 접근 제어 (RBAC, Role-Based Access Control)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. **[ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/)**은 각 교실마다 **"이 교실에 출입 가능한 학생 명단"**을 게시하는 것과 같다. 교실 문 앞에 명단이 붙어있어, 학생이 들어올 때 문지기가 명단을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하면 된다.

2. **권한 회수**는 퇴사하는 직원이 작업한 모든 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 앞명부를 수정해야 하는 것과 같다. 만약 그가 100개의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 접근했다면, 100개 모든 명부를 찾아 수정해야 한다.

3. **[ACL](/knowledge-base/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) vs Capability**는 "교실별 명부"와 "학생별 출입증"의 차이와 같다. 교실별 명부는 수정이 쉽지만, "이 학생은 어디 갈 수 있나"를 알려면 모든 명부를 뒤져야 한다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 575 / 800

← **이전**: [574. 전역 테이블 (Global Table) 방식 구현 (행렬 희소성 문제)](/knowledge-base/studynote/02_operating_system/10_security/574_global_table/)
**다음**: [576. 자격 증명 리스트 (Capability List / Ticket) - 주체 중심 (주체가 가진 권한 리스트 토큰 방식)](/knowledge-base/studynote/02_operating_system/10_security/576_capability_list/) →

---
