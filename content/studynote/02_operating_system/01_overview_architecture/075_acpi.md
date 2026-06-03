+++
title = "75. ACPI (Advanced Configuration and Power Interface)"
date = 2026-03-21

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ACPI(Advanced Configuration and [Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Interface)는 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)와 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 사이에서 장치 구성 정보와 전원 관리 정책을 표준화한 업계 표준 계약이다.
> 2. **가치**: OS가 전원 상태(S-state, C-state, P-state)를 직접 제어할 수 있어, 플랫폼마다 별도 코드 없이 절전·재개·열 관리·핫플러그를 공통 방식으로 처리한다.
> 3. **판단 포인트**: ACPI 관련 문제는 대개 OS 기능 한계가 아니라 BIOS/[UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) 테이블(DSDT, SSDT) 오류나 드라이버 해석 불일치에서 발생한다.

---

## Ⅰ. 개요 및 필요성

1990년대 중반까지 전원 관리는 APM(Advanced Power Management) 방식이 주류였다. APM에서는 BIOS(펌웨어)가 전원 정책을 모두 결정하고 OS는 수동적으로 따르는 구조였다. 이 방식은 제조사마다 구현이 달라 호환성 문제가 심각했고, OS가 세밀한 전원 제어를 하기 어려웠다.

1996년 Intel, Microsoft, Toshiba가 공동으로 ACPI 표준을 제정했다. ACPI의 혁신은 <strong>"펌웨어는 하드웨어 능력을 공개하고, OS가 정책을 결정한다"</strong>는 역할 역전이다. 펌웨어(BIOS/UEFI)는 ACPI 테이블(DSDT, SSDT, FADT 등)을 통해 하드웨어가 지원하는 전원 상태, 장치 목록, 제어 메서드를 OS에 공개한다. OS는 이 정보를 바탕으로 절전 정책, 팬 제어, 장치 핫플러그 등을 자율적으로 결정한다.

ACPI는 전원 관리를 넘어 장치 열거(Device Enumeration)에도 핵심 역할을 한다. PCI Express로 발견되지 않는 내장 장치(임베디드 컨트롤러, GPIO, I2C 장치 등)는 ACPI 테이블을 통해 OS에 알려진다. 현재 UEFI 포럼에서 관리하는 ACPI 6.x 표준은 PC, 서버, ARM 기반 SoC 등 거의 모든 플랫폼에서 채택되고 있다.

- **📢 섹션 요약 비유**: 학교에서 교장선생님(펌웨어)이 "이 교실에 냉난방기가 있고, 창문이 몇 개다"라고 알려 주면, 담임선생님(OS)이 언제 냉난방을 켜고 창문을 열지 직접 결정한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### ACPI 전체 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">하드웨어 (Hardware)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CPU, 메모리, NIC, 스토리지, 팬, 배터리, GPIO ...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">BIOS / UEFI Firmware</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ACPI 테이블 생성 및 제공</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">RSDP → RSDT/XSDT</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ FADT (Fixed ACPI Description Table)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ DSDT (Differentiated System Desc Table)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ SSDT (Secondary System Desc Table) × N</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ MADT (Multiple APIC Description Table)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ HPET (High Precision Event Timer Table)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ SRAT, SLIT (NUMA 토폴로지)</div></div>
<div class="kb-diagram-note">ACPI 테이블 접근</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">OS 커널</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ACPI 서브시스템 (ACPICA 라이브러리)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 테이블 파싱 (DSDT/SSDT → 장치 트리)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ AML 인터프리터 (ACPI Machine Language)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 이벤트 처리 (버튼, 배터리, 온도)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 전원 상태 전환 (S3, S4, S5 진입/복귀)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">드라이버 (Drivers) ←</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">전원 관리 정책, 팬 제어, 장치 핫플러그</div></div>
</div>
</div>



### 주요 ACPI 테이블

| 테이블 | 전체 이름 | 역할 |
| :--- | :--- | :--- |
| RSDP | Root System Description Pointer | ACPI 테이블 루트 포인터 |
| RSDT/XSDT | Root/Extended System Description Table | 모든 테이블 목록 |
| FADT | Fixed ACPI Description Table | 시스템 고정 기능(전원 버튼, 슬립 레지스터 등) |
| DSDT | Differentiated System Description Table | 장치 및 제어 메서드 정의 (AML 코드) |
| SSDT | Secondary System Description Table | DSDT 보완, 추가 장치 정의 |
| MADT | Multiple APIC Description Table | CPU, APIC 토폴로지 |
| HPET | High Precision Event Timer Table | 고해상도 타이머 정보 |
| SRAT/SLIT | NUMA 관련 | 메모리와 CPU의 물리적 거리 |

### ACPI 전원 상태 체계

| 상태 종류 | 단계 | 의미 |
| :--- | :--- | :--- |
| **S-State** (시스템) | S0~S5 | 전체 시스템 전원 상태 |
| **C-State** (CPU) | C0~C10 | CPU 유휴 절전 상태 |
| **P-State** (CPU) | P0~Pn | CPU 성능/주파수 수준 |
| **D-State** (장치) | D0~D3 | 개별 장치 전원 상태 |
| **T-State** (CPU) | T0~Tn | 열 조절(쓰로틀링) |

### AML(ACPI Machine Language)

DSDT/SSDT는 AML이라는 바이트코드 언어로 작성된다. 커널의 AML 인터프리터가 이를 실행하여 하드웨어를 제어한다. AML은 ASL(ACPI Source Language)로 작성한 후 컴파일한다.

```aml
/* ASL 예시: 팬 제어 메서드 */
Method (_FAN, 0) {
    If (LGreater (\_TZ.TMP, 3500)) { /* 온도 > 35도 */
        Store (One, \_SB.FAN) /* 팬 켜기 */
    } Else {
        Store (Zero, \_SB.FAN) /* 팬 끄기 */
    }
}
```

- **📢 섹션 요약 비유**: ACPI는 하드웨어와 OS 사이의 공통 계약서다. 이 계약서에는 "어떤 장치가 있고, 어떻게 끄고 켤 수 있는지"가 적혀 있다.

---

## Ⅲ. 비교 및 연결

### ACPI vs APM 비교

| 비교 항목 | ACPI | APM |
| :--- | :--- | :--- |
| 전원 정책 주체 | OS (적극적 제어) | 펌웨어 (BIOS 주도) |
| 표현 방식 | 테이블 + AML 메서드 | 단순 이벤트/콜백 |
| 장치 제어 세밀도 | D0~D3 개별 장치 | 전체 시스템 위주 |
| 멀티코어 지원 | 우수 (CPU별 C/P-state) | 부족 |
| 플랫폼 독립성 | 높음 (ARM, x86 통합) | x86 중심 |
| 현황 | 현재 표준 | 사용 중단 |

### ACPI와 관련 기술 연결

| 관련 기술 | ACPI와의 관계 |
| :--- | :--- |
| UEFI | ACPI 테이블을 UEFI가 생성하고 제공 |
| Linux cpufreq | P-State 제어의 OS 프레임워크 |
| Linux cpuidle | C-State 제어의 OS 프레임워크 |
| Tickless Kernel | ACPI C-State와 연계하여 절전 극대화 |
| 가상화(KVM/Xen) | 게스트 VM에 가상 ACPI 테이블 제공 |
| BMC(서버) | ACPI와 별개의 하드웨어 관리 채널 |

### ACPI 없을 때의 문제

- 새로운 플랫폼마다 OS 전원 관리 코드를 별도 작성 필요
- 펌웨어가 전원을 강제 제어 → OS의 세밀한 절전 불가
- 내장 장치 발견 불가 (PCI 열거만으로는 부족)
- 플랫폼 간 이식성 극도로 낮음

- **📢 섹션 요약 비유**: 전체 잠자기와 잠깐 졸기는 같은 잠이 아니다. ACPI는 잠의 종류(S3, C3, P2 등)를 세밀하게 정의한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 설계 판단 체크리스트

1. sleep/resume 시 모든 장치가 정상 복귀하는가? (D-state 전환 확인)
2. BIOS/UEFI 버전 업데이트가 전원 문제를 해결했는가? (DSDT 수정 여부 확인)
3. thermal throttling과 팬 정책이 ACPI 메서드를 통해 올바르게 동작하는가?
4. 서버 환경에서 ACPI와 BMC 전원 관리가 충돌하지 않는가?
5. 가상화 환경에서 게스트 VM에 올바른 가상 ACPI 테이블이 제공되는가?
6. Linux에서 `acpidump`, `acpiexec`, `iasl`로 ACPI 테이블을 분석했는가?
7. Wake-on-LAN, 타이머, 전원 버튼 등 wake source가 정확히 설정되어 있는가?
8. Modern Standby(S0ix) 전환 시 드라이버 ACPI D-state 지원이 검증됐는가?

### 안티패턴

- **ACPI 문제를 OS 버그로 오인**: 재개(Resume) 실패, 배터리 급소모, 팬 오동작은 대부분 BIOS/UEFI의 DSDT/SSDT 오류다. OS 커널을 의심하기 전에 BIOS 업데이트와 ACPI 테이블 검증이 우선이다.
- **드라이버가 ACPI 정책을 임의로 덮어쓰는 설계**: 전원 관리는 ACPI 서브시스템이 중앙에서 관리해야 한다. 드라이버가 직접 레지스터를 건드리면 ACPI와 충돌하여 진단이 어렵다.
- **ACPI 없이 임베디드 시스템 설계**: ARM SoC 기반 시스템에서 ACPI를 쓰지 않으면 장치 트리(Device Tree)와의 역할 혼란이 생긴다. 서버급 ARM은 ACPI, 임베디드 ARM은 DT를 사용하는 기준을 명확히 해야 한다.
- **AML 오류를 무시하는 설계**: 커널 부팅 로그에서 AML 실행 오류를 무시하면 장치 초기화 실패나 절전 문제가 잠재한다. `dmesg | grep ACPI`로 오류를 확인해야 한다.

기술사 관점에서는 ACPI를 "펌웨어와 OS 간 전원/장치 관리 표준 계약"으로 설명하되, S-state/C-state/P-state의 계층 구조, DSDT/SSDT의 역할, APM과의 차별화 포인트를 함께 언급해야 한다.

- **📢 섹션 요약 비유**: 전원 스위치를 여러 사람이 동시에 잡으면 불안정해진다. ACPI는 OS가 전원의 주도권을 갖되 펌웨어의 하드웨어 지식을 활용하는 역할 분담이다.

---

## Ⅴ. 기대효과 및 결론

ACPI 표준의 가장 큰 기여는 전원 관리의 주도권을 OS에 돌려주어 세밀하고 지능적인 절전이 가능해졌다는 점이다. 노트북에서는 배터리 수명이 수 시간 연장되었고, 서버에서는 유휴 상태에서의 전력 소비가 획기적으로 줄었다. 클라우드 데이터센터의 에너지 효율화(PUE 개선)에도 ACPI 기반 전력 관리가 핵심 역할을 한다.

장치 열거 측면에서는 ACPI 덕분에 PCI/USB로 발견되지 않는 온보드 장치들(임베디드 컨트롤러, 배터리 관리 IC, 온도 센서, GPIO 등)이 표준 방식으로 OS에 노출되어 드라이버 개발이 표준화되었다.

미래에는 ACPI가 AI 기반 전원 예측(OS가 워크로드 패턴을 학습하여 최적 C/P-state 선택), ARM 서버 생태계 확대(SBSA 표준과 ACPI 결합), IoT 엣지 장치까지 확장될 전망이다. 결론적으로 ACPI는 "전원을 누가 마음대로 쓰는가"가 아니라 "누가 어떤 권한으로 제어하는가"를 명확히 정하는 업계 표준으로, 플랫폼 호환성과 에너지 효율의 기반이다.

- **📢 섹션 요약 비유**: 반장(펌웨어)이 교실 정보를 알려 주면 선생님(OS)이 냉난방 정책을 결정하듯, ACPI는 하드웨어 정보 공개와 OS 정책 결정을 분리하여 효율적인 협력을 가능하게 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 펌웨어(BIOS/UEFI) | ACPI 테이블을 생성·제공 |
| DSDT/SSDT | AML 코드로 장치 및 메서드 정의 |
| OS 커널 | ACPI 테이블 파싱, AML 실행, 전원 정책 결정 |
| S-State | ACPI가 정의한 시스템 전원 단계 |
| C-State | ACPI가 정의한 CPU 유휴 절전 단계 |
| P-State | ACPI가 정의한 CPU 성능/주파수 단계 |
| D-State | ACPI가 정의한 장치별 전원 상태 |
| cpufreq/cpuidle | Linux에서 ACPI P/C-State를 제어하는 프레임워크 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">APM (BIOS 주도 전원관리, 1992)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ACPI 1.0 표준 제정 (Intel/Microsoft/Toshiba, 1996)</div>
<div class="kb-diagram-note">→ OS 주도 전원 정책 전환</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ACPI 2.0 (64비트 지원, 2000)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ACPI 3.0/4.0 (전원 상태 세분화, 2007-2009)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ACPI 5.0 (ARM 지원 확대, 2011)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">ACPI 6.x (현재, UEFI 포럼 관리, NVMe/PCIe 통합)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Modern Standby (S0ix): S3 대체 저전력 대기 모드</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">AI 기반 전원 예측, IoT 확장 전망</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 학교에 불을 끄는 시간표가 있어요. 언제 켜고 끄는지 미리 정해두면 모두가 편해요.
2. 잠깐 쉬는 시간(C-state)과 하교(S5, 완전 종료)가 다르듯, 컴퓨터도 절전의 깊이가 달라요.
3. ACPI는 그 모든 규칙을 정해 둔 표준 시간표예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 75 / 800

← **이전**: [74. 틱리스 커널 (Tickless Kernel)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/074_tickless_kernel/)
**다음**: [76. 시스템 전원 상태 (S-States, S0~S5)](/knowledge-base/studynote/02_operating_system/01_overview_architecture/076_s_states/) →

---
