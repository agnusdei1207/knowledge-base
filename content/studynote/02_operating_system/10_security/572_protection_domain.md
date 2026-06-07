---
title: "572. Protection Domain"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 572
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)은 프로세스가 실행될 때 부여받는 <strong>"접근 가능한 객체와 수행 가능한 연산의 집합"</strong>이다. 크롬 브라우저는 다운로드 폴더에는 접근 가능하지만, 시스템 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(`/etc/passwd`)에는 접근 불가하도록 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)별로 격리된다.
> 2. **가치**: 이 <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 격리(<a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a> <a href="/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/">Isolation</a>)</strong> 덕분에, 웹 서버 데몬이 해킹당해 미쳐 날뛰더라도, 해당 데몬에 부여된 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 권한 외의 시스템 자원에 접근이 차단되어 <strong><a href="/studynote/09_security/04_endpoint_security/356_privilege_escalation/">권한 상승</a>(<a href="/studynote/09_security/04_endpoint_security/356_privilege_escalation/">Privilege Escalation</a>)을 원천 방지</strong>한다.
> 3. **한계**: `sudo` 명령이나 SetUID를 사용하면 프로세스가 일반 권한 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에서 관리자(Root) [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)으로 <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 전환(<a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a> <a href="/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">Switch</a>)</strong>하게 되어, 이 전환 경로를 통한 [권한 상승](/studynote/09_security/04_endpoint_security/356_privilege_escalation/) 공격이 가능해진다.

---

## Ⅰ. 개요 및 필요성

### 1.1 단일 권한의 문제점
과거 MS-DOS와 같은 단일 권한 시스템에서는 프로그램이 하드디스크, 메모리, 그래픽카드 등을 전부 독점적으로 제어했다. 따라서 하나의 프로그램이 오류지면 시스템 전체가 멈추는 문제가 발생했다.

### 1.2 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)의 개념
<strong><a href="/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a> <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a>(<a href="/studynote/02_operating_system/10_security/571_protection_vs_security/">Protection</a> <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a>)</strong>은 다음과 같이 정의된다:

```
도메인 D = { <객체 O1, 권한 R1>, <객체 O2, 권한 R2>, ... }
```

예를 들어, 웹 서버 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)(`httpd_t`)에는:
- `<프린터, {가동}>`
- `<문서 폴더, {읽기}>`

만 허용되고, 다른 시스템 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에는 접근이 불가하도록 제한된다.

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 할당 방식: 사용자 vs 프로세스

| 방식 | 설명 | 적용 사례 |
|:---|:---|:---|
| **사용자 기반** | UID(사용자 ID)별로 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 부여 | 전통 리눅스 (root/일반유저) |
| **프로세스 기반** | 애플리케이션별로 고유 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 부여 | Android (앱 [샌드박싱](/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/)) |

### 2.2 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전환([Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) Switching)과 [SetUID](/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/)

일반 사용자가 비밀번호를 변경하려면 `/etc/shadow` [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 접근해야 하지만, 일반 사용자에게는 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 권한이 없다. 이를 해결하기 위해 [SetUID](/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/) 메커니즘이 사용된다:

1. 사용자가 `passwd` 명령 실행
2. SetUID로 인해 프로세스가 <strong>Root <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a></strong>으로 일시 전환
3. 비밀번호 변경 완료 후 일반 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)으로 복귀

### 2.3 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전환의 보안 위험

[SetUID](/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/) 메커니즘은 <strong><a href="/studynote/02_operating_system/10_security/591_buffer_overflow/">버퍼 오버플로우</a></strong> 등을 통한 [권한 상승](/studynote/09_security/04_endpoint_security/356_privilege_escalation/) 공격의 경로가 된다. 공격자가 `passwd` 프로그램의 취약점을 발견하면 Root [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)으로 전환된 순간 쉘을 획득할 수 있다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 3.1 전통 리눅스와 비교

| 구분 | 전통 리눅스 | Android |
|:---|:---|:---|
| <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 단위</strong> | 사용자(UID) 단위 | 애플리케이션 단위 |
| **격리 수준** |조조 (조잡) | **앱마다 고유 UID + 샌드박스** |

### 3.2 Android 앱 [샌드박싱](/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/)의 원리

Android는 Linux [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 기반으로, <strong>설치된 앱마다 고유한 UID</strong>를 부여한다:

```text
[ 카카오톡 앱 ] -> UID 10123 -> 도메인: { 자기 데이터만 읽기/쓰기 }
[ 배달의민족 앱 ] -> UID 10124 -> 도메인: { 자기 데이터만 읽기/쓰기 }
```

앱이 다른 앱의 데이터에 접근하려고 하면, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) VFS가 <strong>크로스-<a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 위반</strong>으로 프로세스를 종료(Kill)시킨다.

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- <strong><a href="/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a> <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 체계</strong>는 프로세스별로 권한을 분리하여,만일(만약) 프로세스가 해킹당해도 영향 범위를 해당 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 내로 제한한다.
- <strong><a href="/studynote/09_security/01_intro_principles/010_least_privilege/">최소 권한 원칙</a>(<a href="/studynote/09_security/01_intro_principles/010_least_privilege/">Least Privilege</a>)</strong>을 구현하는 핵심 기법으로, [Docker](/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/) [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 격리 등 현대 시스템에서도 활용된다.
- <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 전환(<a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a> Switching)</strong>은 기능성과 보안 사이의 트레이드오프를 수반하며, [SetUID](/studynote/02_operating_system/09_file_system/548_special_permissions_setuid/) 메커니즘은 보안 취약점의 원인이 된다.

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

[보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) ([Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/) [Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/))은 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [보호와 보안](/studynote/02_operating_system/01_overview_architecture/043_protection_security/) 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [접근 제어 행렬](/studynote/02_operating_system/10_security/573_access_matrix/) ([Access Matrix](/studynote/02_operating_system/10_security/573_access_matrix/))처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [리눅스 inotify 시스템](/studynote/02_operating_system/09_file_system/570_inotify_file_monitoring/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) ([Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/)) vs 보안 ([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))의 개념 차이 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [접근 제어 행렬](/studynote/02_operating_system/10_security/573_access_matrix/) ([Access Matrix](/studynote/02_operating_system/10_security/573_access_matrix/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [전역 테이블](/studynote/02_operating_system/10_security/574_global_table/) ([Global Table](/studynote/02_operating_system/10_security/574_global_table/)) 방식 구현 (행렬 희소성 문제) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[보호 (Protection) vs 보안 (Security)의 개념 차이]
    |
    v
[보호 도메인 (Protection Domain)]
    |
    +---> [접근 제어 행렬 (Access Matrix)]
    +---> [전역 테이블 (Global Table) 방식 구현 (행렬 희소성 문제)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. <strong><a href="/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a> <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a></strong>은 놀이공원의 <strong>"입장 팔찌"</strong>와 같다. 어떤 색 팔찌를 받았느냐에 따라 탈 수 있는 놀이기구가 결정된다.

2. <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 전환</strong>은 놀이공원에서 <strong>"직급증가표"</strong>를 받는 것과 같다. 일반 손님(일반 사용자)이적원공(일반 프로세스)이고, 점장(관리자)이의 표를 받으면 더 많은 놀이기구를 탈 수 있다.

3. <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 격리</strong>는 놀이기구 관리자가 <strong>"내 영역 외에는 출입 금지"</strong>인 것과 같다. 다른 색 팔찌를 가진 사람이 관리자의 놀이기구에 가려 하면, 문지기가 "여기는 출입 불가"라며 막는다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 572 / 800

<- **이전**: [571. 보호 (Protection) vs 보안 (Security)의 개념 차이](/studynote/02_operating_system/10_security/571_protection_vs_security/)
**다음**: [573. 접근 제어 행렬 (Access Matrix) - 주체(행)와 객체(열) 교차점의 권한 표현 모형](/studynote/02_operating_system/10_security/573_access_matrix/) ->

---
