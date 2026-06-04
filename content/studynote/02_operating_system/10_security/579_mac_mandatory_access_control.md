+++
title = "579. 강제적 접근 제어 (MAC, Mandatory Access Control) - 시스템/보안 관리자가 등급 라벨 기반 강제 통제"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MAC은 시스템 관리자가 모든 <strong>주체(프로세스)</strong>와 <strong>객체(<a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>)</strong>에 <strong>보안 등급 라벨(<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a> Label)</strong>을 부여하고, 이 라벨 간 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 기반으로 접근을 <strong>강제(Mandatory)</strong>로 통제하는 방식이다.
> 2. **가치**: 사용자가 `chmod 777`로 권한을 열어버려도, [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)에 의해 <strong>최고 비밀 등급 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>에는 접근이 차단</strong>되어,만일(만약) 침해가 발생해도 손실 범위가 제한된다.
> 3. **한계**: [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)이 복잡하여 <strong>관리 오버헤드</strong>가 크고, [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 오류 시 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 장애가 발생할 수 있다.

---

## Ⅰ. 개요 및 필요성

### 1.1 DAC의 한계: [Trojan Horse](/knowledge-base/studynote/02_operating_system/10_security/586_trojan_horse_wrapper/)

DAC([임의적 접근 제어](/knowledge-base/studynote/02_operating_system/10_security/578_dac_discretionary_access_control/))에서는 사용자가 악성 프로그램을 실행하면, 그 프로그램이 사용자의 권한을 상속받는다. 따라서 사용자가 Root 권한으로 실행 중이었다면, 악성 프로그램도 Root 권한을 획득하게 된다.

### 1.2 MAC의 해결책

MAC에서는 **소유자나 사용자의 의사와 무관하게** 시스템 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 접근을 차단한다:

```
[ DAC 정책 ]
소유자가 "모든 사람에게 열기"로 설정 -> 접근 허용

[ MAC 정책 ]
시스템이 "최고 비밀 등급 사용자가 아니면 접근 불가"로 설정 -> 소유자여도 접근 차단
```

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 보안 등급 라벨 ([Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Label)

MAC에서는 모든 주체와 객체에 <strong>보안 등급 라벨</strong>을 부여한다:

```text
[ 주체(프로세스) 라벨 ]
system_u:system_r:httpd_t:s0

[ 객체(파일) 라벨 ]
system_u:object_r:shadow_t:s0
```

### 2.2 격자 모델 (Lattice Model)

보안 등급은 <strong>격자(Lattice) 구조</strong>를 형성한다:

```text
[ 보안 등급 격자 ]
        TOP SECRET
       /        \
   SECRET    CLASSIFIED
       \        /
     CONFIDENTIAL
          |
      UNCLASSIFIED
```

### 2.3 [Bell-LaPadula](/knowledge-base/studynote/02_operating_system/10_security/580_bell_lapadula_model/) 모델과의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

MAC의 구체적인 접근 규칙을 정의하는 대표적인 모델:

| 규칙 | 설명 |
|:---|:---|
| **No Read Up (NRU)** | 자기 등급보다 높은 문서를 읽을 수 없음 |
| **No Write Down (NWD)** | 자기 등급보다 낮은 등급에 문서를 쓸 수 없음 |

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 3.1 [SELinux](/knowledge-base/studynote/02_operating_system/10_security/583_selinux/) 개요

SELinux는 Linux 커널에 구현된 <strong>MAC의 대표적 구현</strong>이다:

```bash
[ 확인 방법 ]
$ ls -Z /etc/shadow
-rw-r-----. root root system_u:object_r:shadow_t:s0 /etc/shadow

[ 웹 서버 컨텍스트 ]
$ ps auxZ | grep httpd
system_u:system_r:httpd_t:s0 httpd
```

### 3.2 [SELinux](/knowledge-base/studynote/02_operating_system/10_security/583_selinux/) 동작 모드

| 모드 | 설명 |
|:---|:---|
| **Enforcing** | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반 시 접근 차단 |
| **Permissive** | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반 시 로그만 기록 |

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **강제적 통제**: 사용자의 의사와 무관하게 보안 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 적용되어, [Trojan Horse](/knowledge-base/studynote/02_operating_system/10_security/586_trojan_horse_wrapper/) 등 내부 위협으로부터 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)
- **세밀한 통제**: 프로세스와 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 단위의 접근 제어가 가능
- **관리 복잡성**: [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)과 관리에 전문 지식과 노력이 필요

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

강제적 접근 제어 ([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/), Mandatory [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/))은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [보호와 보안](/knowledge-base/studynote/02_operating_system/01_overview_architecture/043_protection_security/) 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [벨-라파둘라 모델](/knowledge-base/studynote/02_operating_system/10_security/580_bell_lapadula_model/) ([Bell-LaPadula](/knowledge-base/studynote/02_operating_system/10_security/580_bell_lapadula_model/))처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 롤 기반 접근 제어 ([RBAC](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/), [Role-Based Access Control](/knowledge-base/studynote/09_security/11_iam_access_control/569_rbac/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [임의적 접근 제어](/knowledge-base/studynote/02_operating_system/10_security/578_dac_discretionary_access_control/) (DAC, Discretionary [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [벨-라파둘라 모델](/knowledge-base/studynote/02_operating_system/10_security/580_bell_lapadula_model/) ([Bell-LaPadula](/knowledge-base/studynote/02_operating_system/10_security/580_bell_lapadula_model/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [비바 모델](/knowledge-base/studynote/02_operating_system/10_security/581_biba_model/) ([Biba Model](/knowledge-base/studynote/02_operating_system/10_security/581_biba_model/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[임의적 접근 제어 (DAC, Discretionary Access Control)]
    |
    v
[강제적 접근 제어 (MAC, Mandatory Access Control)]
    |
    +---> [벨-라파둘라 모델 (Bell-LaPadula)]
    +---> [비바 모델 (Biba Model)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a></strong>은 병원의 <strong>"접종 증명 시스템"</strong>과 같다. 어떤 환자가선Drop(권한)이 있다고 주장해도, 시스템에 등록된 등급과 맞지 않으면 진찰을 받을 수 없다.

2. <strong>보안 라벨</strong>은 놀이공원의 <strong>"입장 등급표"</strong>와 같다. Silver 등급은 Silver 놀이기구만, Gold 등급은 Gold 놀이기구만 탈 수 있다. 등급표가 없으면 아무 놀이기구도 탈 수 없다.

3. <strong>관리 복잡성</strong>은 입장 등급표를 <strong>"새로 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a>하거나 변경하려면 병원 전체의 규정을 수정해야"</strong> 하는 것과 같다. 한 명의 등급을 바꾸어도 전체 시스템에 영향을 미칠 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 579 / 800

<- **이전**: [578. 임의적 접근 제어 (DAC, Discretionary Access Control) - 소유자가 임의로 권한 위임](/knowledge-base/studynote/02_operating_system/10_security/578_dac_discretionary_access_control/)
**다음**: [580. 벨-라파둘라 모델 (Bell-LaPadula) - 기밀성 위주 보안 정책 (No Read Up, No Write Down)](/knowledge-base/studynote/02_operating_system/10_security/580_bell_lapadula_model/) ->

---
