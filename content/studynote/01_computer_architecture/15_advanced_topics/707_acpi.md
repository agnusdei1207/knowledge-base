---
title: 707. ACPI (Advanced Configuration and Power Interface)
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[075_acpi|ACPI]] (Advanced Configuration and [[069_type_1_2_error_statistical_power|Power]] Interface)는 [[032_firmware|펌웨어]]가 하드웨어의 전력·열·장치 정보를 표준 테이블로 제공하고, [[001_operating_system_purpose|운영체제]]가 이를 해석해 [[164_policy|정책]]을 결정하도록 만든 인터페이스다.
> 2. **가치**: 절전 모드, CPU [[611_cpu_idle_wait_optimization|idle]] 상태, 배터리 보고, 열 제어, 장치 hotplug를 [[001_operating_system_purpose|운영체제]] 주도로 일관되게 처리할 수 있어, 현대 노트북과 서버의 전력 효율을 크게 높인다.
> 3. **판단 포인트**: ACPI의 성패는 기능 유무보다 테이블 품질에 달려 있으므로, DSDT/SSDT 오류나 잘못된 sleep [[272_state_pattern|state]] 설계는 [[282_performance_tactics|성능]] 저하보다 더 치명적인 절전·복귀 장애를 만든다.

---

## Ⅰ. 개요 및 필요성

ACPI는 하드웨어 [[009_config|설정]]과 전력 관리를 [[001_operating_system_purpose|운영체제]]가 주도하도록 만든 표준이다. [[075_acpi|ACPI]] 이전의 [[162_apm_application_performance_management|APM]] (Advanced [[069_type_1_2_error_statistical_power|Power]] [[372_management|Management]]) 시대에는 BIOS가 언제 절전에 들어가고 언제 깨어날지 많은 결정을 독점했다. 이 방식은 단순했지만, [[675_multitasking_terminology_preemptive|멀티태스킹]] [[001_operating_system_purpose|운영체제]]와 복잡한 모바일 전력 [[164_policy|정책]]을 감당하기에는 너무 둔했다.

문제는 [[164_policy|정책]]을 가장 잘 아는 쪽이 BIOS가 아니라 [[001_operating_system_purpose|운영체제]]라는 데 있다. 노트북에서 지금 사용자가 영상을 보는지, 백그라운드 다운로드 중인지, 배터리가 급한지, 서버에서 [[141_latency|지연 시간]] 민감한 워크로드가 도는지는 OS가 가장 잘 안다. 그런데 [[032_firmware|펌웨어]]가 독단적으로 전원 상태를 바꾸면 응용 프로그램 상태와 장치 전원 상태가 어긋나기 쉽다.

그래서 ACPI는 역할을 나눴다. [[032_firmware|펌웨어]]는 "이 장치가 어떤 상태를 지원하는지"와 "어떤 제어 메서드가 있는지"를 테이블로 설명하고, [[001_operating_system_purpose|운영체제]]는 그 정보를 바탕으로 실제 [[164_policy|정책]]을 결정한다. 즉 ACPI의 핵심은 전원 관리의 주도권을 BIOS에서 OSPM (Operating System-directed configuration and [[069_type_1_2_error_statistical_power|Power]] [[372_management|Management]])으로 넘긴 데 있다.

- **📢 섹션 요약 비유**: ACPI는 건물 경비원이 불을 마음대로 끄는 체계가 아니라, 건물 관리실이 전체 상황을 보고 조명과 냉난방을 결정하는 체계다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ACPI의 시작점은 테이블이다. [[032_firmware|펌웨어]]는 RSDP (Root System Description Pointer)를 제공하고, [[001_operating_system_purpose|운영체제]]는 이를 따라 XSDT (Extended System Description Table)나 RSDT를 찾는다. 그 아래에 FADT (Fixed [[075_acpi|ACPI]] Description Table), DSDT (Differentiated System Description Table), SSDT (Secondary System Description Table) 같은 세부 테이블이 연결된다. [[001_operating_system_purpose|운영체제]]는 이 정보를 읽어 장치 구조와 제어 메서드를 파악한다.

특히 DSDT와 SSDT에는 AML ([[075_acpi|ACPI]] Machine Language) 코드가 담길 수 있다. [[022_kernel_role|커널]] 안의 [[075_acpi|ACPI]] 인터프리터는 이 코드를 실행해 팬 속도, 배터리 보고, GPIO (General-Purpose Input/Output) 기반 이벤트, 장치 on/off 같은 동작을 제어한다. 또한 SCI (System Control [[016_interrupt_mechanism|Interrupt]])와 GPE (General Purpose Event)를 통해 뚜껑 닫힘, 전원 버튼, 배터리 변화 같은 이벤트를 [[001_operating_system_purpose|운영체제]]에 알린다.

| 구성 요소 | 역할 | 실무적으로 중요한 이유 |
| :--- | :--- | :--- |
| RSDP / XSDT | [[075_acpi|ACPI]] 테이블 발견과 [[154_database_index_b_tree_search_optimization|인덱스]] | 잘못되면 OS가 전체 ACPI를 못 읽음 |
| FADT | 전원 관리의 고정 특성 설명 | sleep 지원 범위와 [[016_interrupt_mechanism|인터럽트]] 정보에 영향 |
| DSDT | 핵심 장치·메서드 정의 | 절전·팬·배터리 오류의 주요 원인 |
| SSDT | 추가 장치·CPU 상태 확장 | 동적 CPU/P-[[272_state_pattern|state]] 정보에 자주 사용 |
| AML | 제어 로직 표현 언어 | [[032_firmware|펌웨어]] 버그가 OS 동작 오류로 직결 |
| SCI / GPE | 전원·장치 이벤트 전달 | 뚜껑 닫힘, 전원 버튼, wake-up 처리 기반 |

아래 그림은 ACPI의 제어 경로를 단순화한 것이다.

```text
┌────────────────────────────────────────────────────────────────────┐
│                      ACPI control loop                            │
├────────────────────────────────────────────────────────────────────┤
│ Firmware tables : RSDP -> XSDT -> DSDT / SSDT / FADT             │
│                                  │                                │
│                                  ▼                                │
│                     ACPI interpreter in OS kernel                 │
│                                  │                                │
│      ┌──────────────┬────────────┼──────────────┬──────────────┐  │
│      ▼              ▼            ▼              ▼              │  │
│   S-state        C-state      P-state       Thermal zone       │  │
│      │              │            │              │              │  │
│      └──────────────┴──── SCI / GPE events ────┴──────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

상태 체계도 함께 봐야 한다. 시스템 전반의 S-state는 S0 동작, S3 suspend-to-RAM, S4 hibernation, S5 soft off처럼 이해할 수 있고, CPU는 C-state로 [[611_cpu_idle_wait_optimization|idle]] 깊이를, [[282_performance_tactics|성능]]은 P-state로 동작 수준을 조절한다. 장치별 전원은 D-state로 관리한다. 즉 ACPI는 단일 절전 버튼 규격이 아니라, 시스템·CPU·장치를 함께 다루는 계층형 제어 모델이다.

- **📢 섹션 요약 비유**: ACPI는 건물 관리 메뉴얼과 자동 제어 스크립트를 함께 넣어 둔 책장과 같다. 관리실은 그 책을 읽고 어느 층 조명을 줄이고 어느 방 환기를 켤지 결정한다.

---

## Ⅲ. 비교 및 연결

ACPI를 이해할 때 자주 헷갈리는 대상이 APM과 SMBIOS다. APM은 BIOS가 전력 [[164_policy|정책]]을 주도하던 옛 모델이고, SMBIOS는 시스템 인벤토리를 알려 주는 설명용 테이블이다. 반면 ACPI는 설명만 하는 것이 아니라 [[001_operating_system_purpose|운영체제]]가 상태 전환과 제어 메서드를 실행하게 해 주는 "[[164_policy|정책]] 실행 인터페이스"다.

| 항목 | [[162_apm_application_performance_management|APM]] | [[075_acpi|ACPI]] | [[708_nvme_queue_management|SMBIOS]] |
| :--- | :--- | :--- | :--- |
| [[164_policy|정책]] 주체 | BIOS 중심 | [[001_operating_system_purpose|운영체제]] 중심 | [[164_policy|정책]] 없음, 정보 제공 중심 |
| 주 용도 | 단순 절전 | 전력·열·장치 [[009_config|설정]] 통합 | 시스템 [[655_ir_detection_analysis|식별]]·인벤토리 |
| 표현 방식 | [[032_firmware|펌웨어]] 로직 중심 | 테이블 + AML + 이벤트 | 구조화된 [[001_dikw_pyramid|데이터]] 테이블 |
| 현대 활용성 | 제한적 | 매우 높음 | 자산관리·진단에 높음 |

또한 ACPI는 임베디드의 Device Tree와도 비교된다. Device Tree는 주로 정적 하드웨어 기술에 강하고, ACPI는 동적 메서드와 전력 [[164_policy|정책]] 인터페이스에 강하다. 그래서 x86 노트북·서버에서는 ACPI가 사실상 표준이고, 많은 임베디드 ARM 시스템에서는 Device Tree가 더 흔했다. 다만 최근에는 ARM 서버와 Windows on ARM 환경에서도 [[075_acpi|ACPI]] 활용 범위가 커지고 있다.

연결 관점에서 보면, UEFI가 [[075_acpi|ACPI]] 테이블을 [[001_operating_system_purpose|운영체제]]에 전달하고, [[001_operating_system_purpose|운영체제]]는 ACPI를 통해 suspend, [[473_thermal_throttling|thermal throttling]], battery reporting, processor idle을 조절한다. 즉 UEFI가 "부팅의 문"이라면 ACPI는 "부팅 후 [[164_policy|정책]] 제어의 문법"이다.

- **📢 섹션 요약 비유**: APM이 경비원이 알아서 불을 끄는 규칙이라면, ACPI는 관리실이 건물 도면과 제어판을 받아 직접 운영하는 방식이고, SMBIOS는 그 건물의 주소와 층수만 적힌 안내문에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [[075_acpi|ACPI]] 문제는 대개 "절전이 안 된다"보다 더 복잡하게 나타난다. 뚜껑을 닫으면 팬이 계속 도는 현상, suspend 후 USB가 사라지는 현상, 배터리 퍼센트가 갑자기 튀는 현상, CPU가 깊은 C-state에 못 들어가 유휴 전력이 높게 나오는 현상 등이 모두 [[075_acpi|ACPI]] 테이블과 드라이버 상호작용에서 생길 수 있다. 즉 [[282_performance_tactics|성능]] 튜닝 문제처럼 보여도 실제 원인은 [[032_firmware|펌웨어]] 기술서일 수 있다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 해당 플랫폼이 S3, S0ix, S4 중 무엇을 실제 지원하는지 확인한다.
2. DSDT/SSDT 변경 이력이 있는 [[032_firmware|펌웨어]] 업데이트 후 suspend/resume 회귀 테스트를 수행한다.
3. 배터리, 열 센서, 팬 제어, wake source 로그를 [[001_operating_system_purpose|운영체제]]에서 함께 확인한다.
4. 서버 환경에서는 processor [[611_cpu_idle_wait_optimization|idle]] 제한이 [[141_latency|지연 시간]] 요구와 충돌하지 않는지 검토한다.
5. 테이블 override는 마지막 수단으로만 사용하고, 가능하면 [[032_firmware|펌웨어]] 수정으로 해결한다.

### 대표 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 모든 절전 장애를 [[001_operating_system_purpose|운영체제]] 문제로만 보는 진단
- 최신 플랫폼에서도 S3가 항상 존재한다고 가정하는 설계
- 벤더별 [[075_acpi|ACPI]] 테이블 편차를 무시하고 일괄 이미지를 배포하는 운영

기술사 답안에서는 선택 기준을 분명히 적는 것이 중요하다. 배터리 수명과 발열이 핵심인 노트북은 깊은 C-state와 Modern Standby가 중요하지만, [[141_latency|지연 시간]] 민감한 서버는 지나친 [[611_cpu_idle_wait_optimization|idle]] 진입이 오히려 [[282_performance_tactics|성능]] 꼬리를 악화시킬 수 있다. 따라서 ACPI는 "절전을 많이 쓰는 기술"이 아니라 "시스템 목적에 맞게 전력 [[164_policy|정책]]을 조율하는 기술"로 설명해야 정확하다.

- **📢 섹션 요약 비유**: [[075_acpi|ACPI]] 튜닝은 냉난방 자동 제어 [[009_config|설정]]과 같다. 무조건 가장 세게 아끼는 것이 아니라, 사람이 있는 방과 비어 있는 방을 구분해 맞춤형으로 조절해야 쾌적함과 비용을 같이 잡는다.

---

## Ⅴ. 기대효과 및 결론

ACPI가 잘 구현되면 [[001_operating_system_purpose|운영체제]]는 하드웨어 상태를 더 세밀하게 다룰 수 있다. 그 결과 노트북에서는 배터리 수명과 resume 경험이 좋아지고, 서버에서는 유휴 전력과 발열을 줄이며, 클라이언트 장치에서는 팬 소음과 표면 온도를 안정적으로 관리할 수 있다. 특히 하드웨어마다 제각각이던 전원 관리 방식을 공통 인터페이스로 묶는다는 점이 큰 효과다.

반대로 테이블 품질이 나쁘면 ACPI는 문제의 진원지가 되기도 한다. AML 버그, 잘못된 wake source, 모호한 sleep 선언은 [[001_operating_system_purpose|운영체제]]만으로 우회하기 어렵다. 따라서 ACPI는 규격의 존재보다 구현 완성도가 중요하며, [[032_firmware|펌웨어]]·[[022_kernel_role|커널]]·드라이버를 함께 검증해야 한다.

정리하면 ACPI는 [[032_firmware|펌웨어]]와 [[001_operating_system_purpose|운영체제]]의 "전력 협상 언어"다. 하드웨어가 무엇을 할 수 있는지 설명하고, [[001_operating_system_purpose|운영체제]]가 무엇을 할지 결정하게 만드는 구조라는 관점으로 기억하면 절전·열·장치 제어가 한 프레임으로 묶인다.

- **📢 섹션 요약 비유**: ACPI는 컴퓨터 안의 에너지 교통경찰과 같다. 누가 쉬고, 누가 달리고, 언제 신호를 바꿀지 중앙에서 조율해 전체 흐름을 안정적으로 만든다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| OSPM | [[075_acpi|ACPI]] [[164_policy|정책]]의 최종 결정권이 [[001_operating_system_purpose|운영체제]]에 있음을 보여주는 개념이다 |
| DSDT / SSDT | 장치 제어 메서드와 전력 상태 정의가 담기는 핵심 테이블이다 |
| AML | [[001_operating_system_purpose|운영체제]]가 해석하는 [[075_acpi|ACPI]] 제어 언어다 |
| S-[[272_state_pattern|state]] | 시스템 전체의 절전·종료 상태를 표현한다 |
| C-[[272_state_pattern|state]] / P-[[272_state_pattern|state]] | CPU [[611_cpu_idle_wait_optimization|idle]] 깊이와 [[282_performance_tactics|성능]] 수준을 조절하는 기준이다 |
| SCI / GPE | 전원 버튼, 뚜껑 닫힘, wake-up 같은 이벤트 전달 경로다 |

### 📈 관련 키워드 및 발전 흐름도

```text
BIOS 중심 APM 전력 관리
    │
    ▼
펌웨어 테이블 기반 하드웨어 기술
    │
    ▼
OSPM 중심 ACPI 제어 모델
    │
    ▼
S-state · C-state · thermal 통합
    │
    ▼
Modern Standby · hotplug · 서버 전력 최적화
```

이 흐름은 전력 관리의 주도권이 [[032_firmware|펌웨어]]에서 [[001_operating_system_purpose|운영체제]]로 이동하며 더 정교해진 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 안에는 누가 자고 누가 일할지 정해야 전기를 아낄 수 있어.
2. ACPI는 "램프는 잠깐 쉬고, 선풍기는 조금만 돌고, 중요한 친구는 계속 일해"라고 알려 주는 규칙표야.
3. 그래서 컴퓨터가 덜 뜨겁고 덜 배고프면서도 필요한 일은 계속할 수 있어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 708 / 803

← **이전**: [[706_uefi|706. UEFI (Unified Extensible Firmware Interface)]]
**다음**: [[708_nvme_queue_management|708. SMBIOS (System Management BIOS)]] →

---
