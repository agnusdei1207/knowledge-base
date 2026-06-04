---
title: "75. ACPI (Advanced Configuration and Power Interface)"
date: "2026-03-21"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ACPI (Advanced Configuration and [Power](/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Interface)는 [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/)와 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (OS, [Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)) 사이에서 장치 설명과 전원 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 표준화한 계약이다.
> 2. **가치**: OS가 전원 상태를 직접 제어할 수 있어 절전·재개·열 관리·핫플러그를 플랫폼마다 따로 짤 필요가 없다.
> 3. **판단 포인트**: ACPI 문제는 대개 OS가 못하는 문제가 아니라 BIOS (Basic Input/Output System)·[UEFI](/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) (Unified Extensible [Firmware](/studynote/02_operating_system/01_overview_architecture/032_firmware/) Interface) 테이블이나 드라이버 해석이 어긋난 문제다.

---

## Ⅰ. 개요 및 필요성

ACPI는 하드웨어가 무엇을 할 수 있는지와 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 무엇을 통제할 수 있는지를 합의하는 표준이다. 옛 [APM](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) (Advanced [Power](/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/))처럼 [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/)가 전원을 전부 쥐는 방식이 아니라, OS가 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 갖고 [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/)는 능력을 공개하는 구조로 바뀌었다.

이 표준이 필요했던 이유는 노트북, 서버, 임베디드 장치의 전원과 장치 구성이 너무 다양했기 때문이다. 제조사마다 따로 짠 전원 관리 코드를 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 모두 이해할 수 없으니, 공통 테이블과 이벤트 규칙이 필요했다.

```text
Firmware -> ACPI Tables -> OS Kernel -> Drivers -> Devices
            |             |          |
            +- sleep / wake / thermal / power state
```

결국 ACPI는 "하드웨어 설명서"이면서 동시에 "전원 계약서"다.

- **📢 섹션 요약 비유**: 불을 끄고 켜는 규칙이 같아야 모두가 편하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ACPI는 테이블과 상태로 움직인다. DSDT와 SSDT는 장치와 메서드를 설명하고, FADT는 고정 기능을 알려 주며, 시스템 상태와 CPU 상태는 전원 동작을 나눈다.

| 요소 | 의미 | 실무 포인트 |
| :--- | :--- | :--- |
| DSDT / SSDT | 장치와 제어 메서드 | 공급사별 차이 |
| FADT | 고정 기능 테이블 | 플랫폼의 기본 능력 |
| S-state | 시스템 sleep 상태 | S0~S5 |
| C-state | CPU [idle](/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/) 상태 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) vs 전력 |
| P-state | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 상태 | 주파수/[전압](/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) 조정 |

OS는 이 정보를 읽어 장치 트리와 전원 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 만든다. 그래서 같은 커널이라도 ACPI 구현이 다르면 절전, 팬 제어, 재개 동작이 달라질 수 있다.

- **📢 섹션 요약 비유**: 규칙표가 있으면 모두 같은 순서로 움직인다.

---

## Ⅲ. 비교 및 연결

ACPI와 APM의 차이는 누가 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 결정하느냐에 있다. APM은 [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/) 중심이고, ACPI는 OS 중심이다. 이 차이 때문에 최신 시스템은 더 세밀한 전원 제어를 할 수 있다.

| 비교 축 | ACPI | [APM](/studynote/15_devops_sre/03_sre_observability/162_apm_application_performance_management/) |
| :--- | :--- | :--- |
| [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 주체 | OS | [Firmware](/studynote/02_operating_system/01_overview_architecture/032_firmware/) |
| 표현 방식 | 테이블/메서드 | 단순 이벤트 |
| 강점 | 세밀한 제어 | 단순함 |
| 약점 | 구현 복잡도 | 유연성 부족 |

또 S-state는 시스템 전체 sleep, C-state는 CPU [idle](/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/), P-state는 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 조절이라는 점에서 서로 다르다. 이 셋을 구분해야 전력 문제를 제대로 진단할 수 있다.

- **📢 섹션 요약 비유**: 전체 잠자기와 잠깐 졸기는 같은 잠이 아니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 먼저 BIOS/[UEFI](/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) 업데이트와 로그를 본다. 재개 실패나 배터리 급소모는 커널보다 [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/) 테이블 문제인 경우가 많기 때문이다.

체크 포인트는 다음과 같다.
- sleep/resume 시 장치가 다시 살아나는가.
- thermal throttling과 fan policy가 충돌하지 않는가.
- 서버 전원 관리에서 ACPI와 [BMC](/studynote/01_computer_architecture/15_advanced_topics/710_bmc/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 엇갈리지 않는가.

안티패턴은 드라이버가 ACPI [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 몰래 덮어쓰는 것이다. 전원 관리는 한 군데서 일관되게 해야 진단이 가능하다.

- **📢 섹션 요약 비유**: 전원 스위치를 여러 사람이 동시에 잡으면 불안정해진다.

---

## Ⅴ. 기대효과 및 결론

ACPI는 하드웨어와 OS의 경계를 부드럽게 만든다. 덕분에 절전, 장치 열거, 팬 제어, 핫플러그가 공통 규칙 위에서 움직인다.

기억할 관점은 간단하다. ACPI는 "전원을 누가 마음대로 쓰는가"가 아니라 "누가 어떤 권한을 갖는가"를 정하는 계약이다. 이 계약이 명확할수록 플랫폼 호환성과 진단 가능성이 높아진다.

- **📢 섹션 요약 비유**: 반장과 선생님이 역할을 나누면 교실이 조용해진다.

---

### 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Firmware](/studynote/02_operating_system/01_overview_architecture/032_firmware/) | 하드웨어 능력 공개 |
| ACPI Tables | 장치와 전원 상태 설명 |
| OS [Kernel](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) | 전원 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 결정 |
| Driver | 장치 제어 실행 |
| Sleep / Wake | 전원 상태 전환 |

### 관련 키워드 및 발전 흐름도

```text
Boot
  |
  v
Firmware tables
  |
  v
OS parse
  |
  v
Device enumeration
  |
  v
Runtime power management
  |
  v
Sleep / Resume
```

### 어린이를 위한 3줄 비유 설명

1. 학교에 불을 끄는 시간표가 있어요.
2. 잠깐 쉬는 시간과 하교 시간이 다르듯, 잠자기 종류도 달라요.
3. 규칙이 있으면 선생님과 아이가 다 편해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 75 / 800

<- **이전**: [74. 틱리스 커널 (Tickless Kernel)](/studynote/02_operating_system/01_overview_architecture/074_tickless_kernel/)
**다음**: [76. 시스템 전원 상태 (S-States, S0~S5)](/studynote/02_operating_system/01_overview_architecture/076_s_states/) ->

---
