---
title: "Protection Vs Security"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
weight: 571
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: <strong>보호(Protection)</strong>는 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 내부에서 정상 프로세스들이 서로의 메모리나 자원에 실수로 침범하지 못하게 막는 <strong>내부 교통정리 체계(Internal Mechanism)</strong>이고, <strong>보안(<a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong>은 해커나 [바이러스](/studynote/02_operating_system/10_security/589_virus/) 등 외부 적의 침입을 차단하는 <strong>외곽 방어망(External <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">Policy</a>)</strong>이다.
> 2. **가치**: 이 <strong>이중 방어 체계(Dual Defense <a href="/studynote/12_it_management/05_security_compliance/319_architecture/">Architecture</a>)</strong>덕분에, 비밀번호 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 뚫고 들어온 해커조차도 OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 접근 권한(보호)에 묶여 아무것도 하지 못하고 거부당하는 다층 방어([Defense in Depth](/studynote/09_security/01_intro_principles/012_defense_in_depth/))를 구현할 수 있다.
> 3. **한계**: 보호(Protection) 체계가 아무리 잘 설계되어 있어도, 관리자 계정 탈취와 같은 보안([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) 침해가 발생하면 내부의 모든 보호 장치가 무력화되는 **단일 실패점(Cascading Failure)** 위험을 항상 안고 있다.

---

## Ⅰ. 개요 및 필요성

### 1.1 보호(Protection)의 개념
<strong>보호(Protection)</strong>는 성(OS) 안에서 실행되는 프로세스들 간의 규칙이다. [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) 프로세서가 엑셀 프로세스의 메모리 주소 공간에 무단으로 접근하려고 하면, [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [MMU](/studynote/02_operating_system/06_memory_management/328_mmu/)([Memory Management Unit](/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/))가 이를 차단하여 <strong><a href="/studynote/02_operating_system/06_memory_management/364_segmentation/">세그멘테이션</a> 폴트(<a href="/studynote/02_operating_system/06_memory_management/364_segmentation/">Segmentation</a> Fault)</strong>를 발생시킨다.

### 1.2 보안([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))의 개념
<strong>보안(<a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong>은 성 밖에서 침입하려는 해커나 악성 트래픽을 차단하는 외곽 철조망이다. [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)([Firewall](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)), 패스워드 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 암호화(Encryption), [IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/)/[IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 등이 해당한다.

### 1.3 분리된 경계망의 필요성
1970년대 초반에는 컴퓨터에 사용자가 1명이라 외부 보안만으로 충분했다. 그러나 인터넷과 다중 사용자(Multi-User) 환경이 도입되면서, 이미 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)된 정상 사용자들조차 서로의 디렉터리를 침범하는 문제가 발생했다. 따라서 <strong>외곽 보안(<a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong>과 <strong>내부 보호(Protection)</strong>가 모두 필수적이다.

- **📢 섹션 요약 비유**: 복잡한 창고에서 필요한 물건을 찾기 위해 먼저 구역과 표지판을 세우는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 메커니즘(Mechanism)과 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/))의 분리

[보호와 보안](/studynote/02_operating_system/01_overview_architecture/043_protection_security/)을 구현하기 위해서는 <strong>"기계 장치(메커니즘)"</strong>와 <strong>"그 장치를 조작하는 규칙(<a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>)"</strong>이 분리되어야 한다.

| 구분 | 메커니즘 (Mechanism) | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) ([Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/)) |
|:---|:---|:---|
| **역할** | "어떻게(How) 막을 것인가?" | "무엇을(What/Who) 막을 것인가?" |
| **변경 빈도** | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 재부팅 없이는 변경 불가 | [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 유동적 변경 가능 |
| **예시** | `rwx` [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 해석 및 차단 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 코드 |인사팀 폴더에 대해 인사팀 그룹만 읽기 권한 부여 |

### 2.2 분리 실패 사례: MS-DOS

과거 Windows 95 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에서는 "누가 C드라이브를 지울 수 있는가"가 OS 코드에 하드코딩되어 있었다. 따라서 "외주 직원에게 B드라이브 접근 차단" [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 추가하려면 OS 자체를 재설계해야 하는 극악의 종속성이 발생했다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### 3.1 보안([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))만 믿다가 발생한 사고

주니어 엔지니어가 AWS에 서버를 띄우고 `Security Group`으로 외부 접근을 차단했다. 그러나 내부 프로세스의 [IAM](/studynote/09_security/11_iam_access_control/526_iam/) 권한이 과도하게 부여되어 있어, USB로 감염된 내부 PC가 해킹당했을 때 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 전체가 삭제되는 사고가 발생했다.

### 3.2 이중 방어 체계 적용

| 단계 | 유형 | 적용 기술 |
|:---|:---|:---|
| **1차 방어** | [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) (보안) | [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Group / NACL로 외부 차단 |
| **2차 방어** | Protection (보호) | [Least Privilege](/studynote/09_security/01_intro_principles/010_least_privilege/) 기반 [IAM](/studynote/09_security/11_iam_access_control/526_iam/) Role으로 내부 권한 최소화 |

- **📢 섹션 요약 비유**: 비슷해 보이는 공구를 나란히 놓고 언제 망치를 쓰고 언제 드라이버를 써야 하는지 구분하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- <strong>보호(Protection) 체계</strong>는 내부 프로세스 간 접근을 제어하여,만일(만약) 악성 코드가 시스템에 감염되어도 영향 범위를 제한한다.
- <strong>보안(<a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>) 체계</strong>는 외부 침입을 차단하여, 내부 보호 체계가 무력화되는 것을 방지한다.
- 두 체계의 <strong>분리 설계(Mechanism vs <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">Policy</a>)</strong>는 1970년대 이래로 유닉스 시스템의 핵심 설계 원칙으로 이어져 왔다.

- **📢 섹션 요약 비유**: 운전자가 도로 상황에 따라 기어와 브레이크를 다르게 선택하는 것처럼 조건별 판단이 중요하다.

---

## Ⅴ. 기대효과 및 결론

보호 (Protection) vs 보안 ([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))의 개념 차이은 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [보호와 보안](/studynote/02_operating_system/01_overview_architecture/043_protection_security/) 메커니즘을 이해하는 연결 고리 역할을 한다. 이 개념을 익히면 시스템 동작을 더 예측 가능하게 설명할 수 있지만, 만능 해법은 아니므로 적용 전제와 한계를 함께 기억해야 한다. 앞으로는 [보호 도메인](/studynote/02_operating_system/10_security/572_protection_domain/) ([Protection Domain](/studynote/02_operating_system/10_security/572_protection_domain/))처럼 더 세분화된 기술과 결합되며 자동화·최적화 방향으로 발전한다.

- **📢 섹션 요약 비유**: 도구의 장점만 외우는 것이 아니라 어디까지 믿고 어디서 보완해야 하는지 기억하는 정리 노트와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [스파스 파일](/studynote/02_operating_system/09_file_system/569_sparse_file_holes/) ([Sparse File](/studynote/02_operating_system/09_file_system/569_sparse_file_holes/)) 저장 공간 절약 기술 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [리눅스 inotify 시스템](/studynote/02_operating_system/09_file_system/570_inotify_file_monitoring/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [보호 도메인](/studynote/02_operating_system/10_security/572_protection_domain/) ([Protection Domain](/studynote/02_operating_system/10_security/572_protection_domain/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [접근 제어 행렬](/studynote/02_operating_system/10_security/573_access_matrix/) ([Access Matrix](/studynote/02_operating_system/10_security/573_access_matrix/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[리눅스 inotify 시스템]
    |
    v
[보호 (Protection) vs 보안 (Security)의 개념 차이]
    |
    +---> [보호 도메인 (Protection Domain)]
    +---> [접근 제어 행렬 (Access Matrix)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. <strong>보호(Protection)</strong>는 아파트 건물 내부의 <strong>방문록 시스템</strong>과 같다. 입주민(거주자)끼리 서로의 집에승수(마음대로) 들어가지 못하게 각 문에 자물쇠를 채워두는 것과 같다.

2. <strong>보안(<a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong>는 건물의 <strong>정문 경비 시스템</strong>과 같다.택배 기사로 위장한 도둑이 건물에 들어오지 못하게 1층에서 확인하고 쫓아내는 것과 같다.

3. **둘 다 중요한 이유**: 정문 경비(보안)가 도둑을 막아도,만일(만약) 도둑이 거주자로 위장하여 들어왔다면, 각 집의 자물쇠(보호)가 없으면 금고 속 보석을 털어갈 수 있다. 그래서 <strong>두 가지 시스템이 모두 필요</strong>하다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 571 / 800

<- **이전**: [570. 리눅스 inotify 시스템 (Inotify File Monitoring)](/studynote/02_operating_system/09_file_system/570_inotify_file_monitoring/)
**다음**: [572. 보호 도메인 (Protection Domain) - 프로세스가 접근할 수 있는 자원(객체)과 권한(Access Right)의](/studynote/02_operating_system/10_security/572_protection_domain/) ->

---
