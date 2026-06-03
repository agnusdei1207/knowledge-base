---
title: 572. 보호 도메인 (Protection Domain) - 프로세스가 접근할 수 있는 자원(객체)과 권한(Access Right)의
  집합
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[571_protection_vs_security|보호]] [[064_relation_domain|도메인]]은 프로세스가 실행될 때 부여받는 **"접근 가능한 객체와 수행 가능한 연산의 집합"**이다. 크롬 브라우저는 다운로드 폴더에는 접근 가능하지만, 시스템 [[009_config|설정]] [[501_file_definition_logical_record|파일]](`/etc/passwd`)에는 접근 불가하도록 [[064_relation_domain|도메인]]별로 격리된다.
> 2. **가치**: 이 **[[064_relation_domain|도메인]] 격리([[064_relation_domain|Domain]] [[195_isolation_concurrency_control|Isolation]])** 덕분에, 웹 서버 데몬이 해킹당해 미쳐 날뛰더라도, 해당 데몬에 부여된 [[064_relation_domain|도메인]] 권한 외의 시스템 자원에 접근이 차단되어 **[[356_privilege_escalation|권한 상승]]([[356_privilege_escalation|Privilege Escalation]])을 원천 방지**한다.
> 3. **한계**: `sudo` 명령이나 SetUID를 사용하면 프로세스가 일반 권한 [[064_relation_domain|도메인]]에서 관리자(Root) [[064_relation_domain|도메인]]으로 **[[064_relation_domain|도메인]] 전환([[064_relation_domain|Domain]] [[238_switch_operation_principles|Switch]])**하게 되어, 이 전환 경로를 통한 [[356_privilege_escalation|권한 상승]] 공격이 가능해진다.

---

## Ⅰ. 개요 및 필요성

### 1.1 단일 권한의 문제점
과거 MS-DOS와 같은 단일 권한 시스템에서는 프로그램이 하드디스크, 메모리, 그래픽카드 등을 전부 독점적으로 제어했다. 따라서 하나의 프로그램이 오류지면 시스템 전체가 멈추는 문제가 발생했다.

### 1.2 [[571_protection_vs_security|보호]] [[064_relation_domain|도메인]]의 개념
**[[571_protection_vs_security|보호]] [[064_relation_domain|도메인]]([[571_protection_vs_security|Protection]] [[064_relation_domain|Domain]])**은 다음과 같이 정의된다:

```
도메인 D = { <객체 O1, 권한 R1>, <객체 O2, 권한 R2>, ... }
```

예를 들어, 웹 서버 [[064_relation_domain|도메인]](`httpd_t`)에는:
- `<프린터, {가동}>`
- `<문서 폴더, {읽기}>`

만 허용되고, 다른 시스템 [[501_file_definition_logical_record|파일]]에는 접근이 불가하도록 제한된다.

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [[064_relation_domain|도메인]] 할당 방식: 사용자 vs 프로세스

| 방식 | 설명 | 적용 사례 |
|:---|:---|:---|
| **사용자 기반** | UID(사용자 ID)별로 [[064_relation_domain|도메인]] 부여 | 전통 리눅스 (root/일반유저) |
| **프로세스 기반** | 애플리케이션별로 고유 [[064_relation_domain|도메인]] 부여 | Android (앱 [[602_sandboxing_kernel_wrapper|샌드박싱]]) |

### 2.2 [[064_relation_domain|도메인]] 전환([[064_relation_domain|Domain]] Switching)과 [[548_special_permissions_setuid|SetUID]]

일반 사용자가 비밀번호를 변경하려면 `/etc/shadow` [[501_file_definition_logical_record|파일]]에 접근해야 하지만, 일반 사용자에게는 [[289_cqrs_db|쓰기]] 권한이 없다. 이를 해결하기 위해 [[548_special_permissions_setuid|SetUID]] 메커니즘이 사용된다:

1. 사용자가 `passwd` 명령 실행
2. SetUID로 인해 프로세스가 **Root [[064_relation_domain|도메인]]**으로 일시 전환
3. 비밀번호 변경 완료 후 일반 [[064_relation_domain|도메인]]으로 복귀

### 2.3 [[064_relation_domain|도메인]] 전환의 보안 위험

[[548_special_permissions_setuid|SetUID]] 메커니즘은 **[[591_buffer_overflow|버퍼 오버플로우]]** 등을 통한 [[356_privilege_escalation|권한 상승]] 공격의 경로가 된다. 공격자가 `passwd` 프로그램의 취약점을 발견하면 Root [[064_relation_domain|도메인]]으로 전환된 순간 쉘을 획득할 수 있다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 3.1 전통 리눅스와 비교

| 구분 | 전통 리눅스 | Android |
|:---|:---|:---|
| **[[064_relation_domain|도메인]] 단위** | 사용자(UID) 단위 | 애플리케이션 단위 |
| **격리 수준** |粗糙 (조잡) | **앱마다 고유 UID + 샌드박스** |

### 3.2 Android 앱 [[602_sandboxing_kernel_wrapper|샌드박싱]]의 원리

Android는 Linux [[022_kernel_role|커널]] 기반으로, **설치된 앱마다 고유한 UID**를 부여한다:

```text
[ 카카오톡 앱 ] -> UID 10123 -> 도메인: { 자기 데이터만 읽기/쓰기 }
[ 배달의민족 앱 ] -> UID 10124 -> 도메인: { 자기 데이터만 읽기/쓰기 }
```

앱이 다른 앱의 데이터에 접근하려고 하면, [[022_kernel_role|커널]] VFS가 **크로스-[[064_relation_domain|도메인]] 위반**으로 프로세스를 종료(Kill)시킨다.

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **[[571_protection_vs_security|보호]] [[064_relation_domain|도메인]] 체계**는 프로세스별로 권한을 분리하여,万一(만약) 프로세스가 해킹당해도 영향 범위를 해당 [[064_relation_domain|도메인]] 내로 제한한다.
- **[[010_least_privilege|최소 권한 원칙]]([[010_least_privilege|Least Privilege]])**을 구현하는 핵심 기법으로, [[063_docker_architecture|Docker]] [[561_container_based_deployment|컨테이너]] 격리 등 현대 시스템에서도 활용된다.
- **[[064_relation_domain|도메인]] 전환([[064_relation_domain|Domain]] Switching)**은 기능성과 보안 사이의 트레이드오프를 수반하며, [[548_special_permissions_setuid|SetUID]] 메커니즘은 보안 취약점의 원인이 된다.

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

[[571_protection_vs_security|보호]] [[064_relation_domain|도메인]] ([[571_protection_vs_security|Protection]] [[064_relation_domain|Domain]])은 [[001_operating_system_purpose|운영체제]] [[043_protection_security|보호와 보안]] 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [[573_access_matrix|접근 제어 행렬]] ([[573_access_matrix|Access Matrix]])처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[570_inotify_file_monitoring|리눅스 inotify 시스템]] | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[571_protection_vs_security|보호]] ([[571_protection_vs_security|Protection]]) vs 보안 ([[283_security_tactics|Security]])의 개념 차이 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[573_access_matrix|접근 제어 행렬]] ([[573_access_matrix|Access Matrix]]) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[574_global_table|전역 테이블]] ([[574_global_table|Global Table]]) 방식 구현 (행렬 희소성 문제) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[보호 (Protection) vs 보안 (Security)의 개념 차이]
    │
    ▼
[보호 도메인 (Protection Domain)]
    │
    ├──▶ [접근 제어 행렬 (Access Matrix)]
    └──▶ [전역 테이블 (Global Table) 방식 구현 (행렬 희소성 문제)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. **[[571_protection_vs_security|보호]] [[064_relation_domain|도메인]]**은 놀이공원의 **"입장 팔찌"**와 같다. 어떤 색 팔찌를 받았느냐에 따라 탈 수 있는 놀이기구가 결정된다.

2. **[[064_relation_domain|도메인]] 전환**은 놀이공원에서 **"직급증가표"**를 받는 것과 같다. 일반 손님(일반 사용자)이的员工(일반 프로세스)이고, 점장(관리자)이의 표를 받으면 더 많은 놀이기구를 탈 수 있다.

3. **[[064_relation_domain|도메인]] 격리**는 놀이기구 관리자가 **"내 영역 외에는 출입 금지"**인 것과 같다. 다른 색 팔찌를 가진 사람이 관리자의 놀이기구에 가려 하면, 문지기가 "여기는 출입 불가"라며 막는다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 572 / 800

← **이전**: [[571_protection_vs_security|571. 보호 (Protection) vs 보안 (Security)의 개념 차이]]
**다음**: [[573_access_matrix|573. 접근 제어 행렬 (Access Matrix) - 주체(행)와 객체(열) 교차점의 권한 표현 모형]] →

---
