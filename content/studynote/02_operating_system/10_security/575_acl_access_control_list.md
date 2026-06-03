---
title: 575. 접근 제어 목록 (ACL, Access Control List) - 객체 중심 (해당 객체에 접근 가능한 주체 목록)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[549_acl_access_control_list|ACL]]([[739_access_control_list_acl|접근 제어 목록]])은 [[573_access_matrix|접근 제어 행렬]]을 **객체([[501_file_definition_logical_record|파일]]) 기준**으로 분할하여, 각 [[501_file_definition_logical_record|파일]]에 "누구(Object)가 어떤 권한(Subject)을 가지는지" 목록을 저장하는 방식이다.
> 2. **가치**: [[501_file_definition_logical_record|파일]] 접근 시 해당 [[501_file_definition_logical_record|파일]]의 ACL만 [[396_validation|확인]]하면 되므로 **중앙 테이블 탐색 없이** $O(1)$ 시간에 접근 권한을 검증할 수 있다.
> 3. **한계**: 사용자가 퇴사하거나 권한을 회수할 때, 해당 사용자가 포함된 **모든 [[501_file_definition_logical_record|파일]]의 ACL을 찾아 업데이트**해야 하는 $O(N)$ 작업이 필요하다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [[574_global_table|전역 테이블]]의 한계

[[574_global_table|전역 테이블]]에서는 사용자 퇴사 시:
- 시스템의 **모든 권한 [[063_relation_tuple_cardinality|튜플]]**을 스캔
- 해당 사용자가 포함된 [[063_relation_tuple_cardinality|튜플]]을 모두 삭제

수백만 개 [[501_file_definition_logical_record|파일]] 환경에서 이는 **수시간에서 수일**이 소요될 수 있다.

### 1.2 ACL의 해결책

ACL은 **"[[501_file_definition_logical_record|파일]](Object)ごとに(각각)"** 권한 목록을 저장한다:

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

### 2.1 [[549_acl_access_control_list|ACL]] vs Capability: 두 가지 분할 방식

| 구분 | [[549_acl_access_control_list|ACL]] (행 분할) | Capability (열 분할) |
|:---|:---|:---|
| **분할 기준** | 객체([[501_file_definition_logical_record|파일]]) 기준 | 주체(사용자) 기준 |
| **저장 위치** | [[501_file_definition_logical_record|파일]] inode에 부착 | 프로세스 PCB에 저장 |
| **권한 회수** | [[501_file_definition_logical_record|파일]] ACL에서 삭제 ($O(1)$) | 모든 프로세스 티켓 회수 ($O(N)$) |
| **사용자 조회** | 해당 사용자가 접근 가능한 [[501_file_definition_logical_record|파일]] 탐색 어려움 | 사용자의 티켓 목록만 [[396_validation|확인]] ($O(1)$) |

### 2.2 Unix/Linux의 [[549_acl_access_control_list|ACL]]: 9비트 시스템

전통적인 Unix/Linux의 [[501_file_definition_logical_record|파일]] 권한은 **3group × 3bit = 9bit** 구조다:

```text
[ 예: chmod 755 file.txt ]
rwxr-xr-x (Owner: 7=rwx, Group: 5=r-x, Others: 5=r-x)
```

이는 simplified ACL로, **소유자/그룹/기타** 세 가지 항목만 관리한다.

### 2.3 확장 [[549_acl_access_control_list|ACL]]

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

Windows 탐색기에서 [[501_file_definition_logical_record|파일]] 우클릭 → [[082_attribute_types_er_model|속성]] → 보안 탭에서 보는 것이 바로 **NTFS [[549_acl_access_control_list|ACL]]**이다.

### 3.2 [[549_acl_access_control_list|ACL]] 항目の構造

```text
[ NTFS ACL 항목 ]
 Principal (사용자/그룹) | Access Type (허용/거부) | Permissions (권한)
 alice                    | Allow                   | Read, Write
 NETWORK SERVICE          | Deny                    | Full Control
```

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **권한 회수의 용이성**: 특정 [[501_file_definition_logical_record|파일]]의 권한 변경 시 해당 [[501_file_definition_logical_record|파일]] ACL만 수정
- **[[136_variance|분산]] 관리**: 각 [[501_file_definition_logical_record|파일]] 소유자가 직접 권한을 관리 가능
- **역방향 조회 어려움**: "이 사용자가 접근 가능한 [[501_file_definition_logical_record|파일]] 목록" 조회 시 전체 [[501_file_definition_logical_record|파일]] 스캔 필요

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

[[739_access_control_list_acl|접근 제어 목록]] ([[549_acl_access_control_list|ACL]], [[549_acl_access_control_list|Access Control List]])은 [[001_operating_system_purpose|운영체제]] [[043_protection_security|보호와 보안]] 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [[576_capability_list|자격 증명 리스트]] ([[576_capability_list|Capability List]] / Ticket)처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[573_access_matrix|접근 제어 행렬]] ([[573_access_matrix|Access Matrix]]) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[574_global_table|전역 테이블]] ([[574_global_table|Global Table]]) 방식 구현 (행렬 희소성 문제) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[576_capability_list|자격 증명 리스트]] ([[576_capability_list|Capability List]] / Ticket) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 롤 기반 접근 제어 ([[569_rbac|RBAC]], [[569_rbac|Role-Based Access Control]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

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

1. **[[549_acl_access_control_list|ACL]]**은 각 교실마다 **"이 교실에 출입 가능한 학생 명단"**을 게시하는 것과 같다. 교실 문 앞에 명단이 붙어있어, 학생이 들어올 때 문지기가 명단을 [[396_validation|확인]]하면 된다.

2. **권한 회수**는 퇴사하는 직원이 작업한 모든 [[501_file_definition_logical_record|파일]]의 앞명부를 수정해야 하는 것과 같다. 만약 그가 100개의 [[501_file_definition_logical_record|파일]]에 접근했다면, 100개 모든 명부를 찾아 수정해야 한다.

3. **[[549_acl_access_control_list|ACL]] vs Capability**는 "교실별 명부"와 "학생별 출입증"의 차이와 같다. 교실별 명부는 수정이 쉽지만, "이 학생은 어디 갈 수 있나"를 알려면 모든 명부를 뒤져야 한다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 575 / 800

← **이전**: [[574_global_table|574. 전역 테이블 (Global Table) 방식 구현 (행렬 희소성 문제)]]
**다음**: [[576_capability_list|576. 자격 증명 리스트 (Capability List / Ticket) - 주체 중심 (주체가 가진 권한 리스트 토큰 방식)]] →

---
