+++
title = "653. ARM Cortex-A 시리즈 특징"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ARM Cortex-A 시리즈는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) ([Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), OS)와 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)를 전제로, 사용자 공간과 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 공간을 분리해 복잡한 애플리케이션을 안정적으로 실행하는 애플리케이션 프로세서용 코어다.
> 2. **가치**: 메모리 관리 장치 ([Memory Management Unit](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/284_mmu/), [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/)), 다단 캐시, 벡터 연산 엔진, 멀티코어 구성을 통해 스마트폰·태블릿·엣지 서버에서 높은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 전력 효율을 동시에 노린다.
> 3. **판단 포인트**: 리치 OS, 브라우저, 멀티미디어, [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)가 필요하면 Cortex-A가 맞고, 마이크로초 단위 결정적 응답이나 극저전력이 핵심이면 Cortex-R 또는 Cortex-M이 더 적합하다.

---

## Ⅰ. 개요 및 필요성

ARM Cortex-A 시리즈는 ARM의 세 프로파일 중 애플리케이션 영역을 담당하는 코어 계열이다. 여기서 핵심은 "명령을 빨리 실행하는 것"만이 아니라, 여러 앱과 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 서로 격리한 채 큰 메모리 공간에서 동시에 굴리는 능력이다. 그래서 Cortex-A는 스마트폰, 스마트 TV, 차량 인포테인먼트, 네트워크 게이트웨이, 저전력 서버처럼 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 자체가 중요한 장비에 주로 들어간다.

이 계열이 필요해진 이유는 모바일 기기가 단순 전화기에서 작은 PC로 바뀌었기 때문이다. 브라우저, 지도, 카메라 파이프라인, 암호화, 무선 스택이 한 칩에서 동시에 돌아가려면 [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/), 프로세스 분리, 예외 처리, 캐시 계층이 반드시 필요하다. 이런 기능이 없으면 앱 하나의 오류가 시스템 전체를 멈추게 만들고, 대용량 메모리도 효율적으로 다룰 수 없다.

아래 그림은 Cortex-A가 "앱 실행 환경 전체"를 품는 코어라는 점을 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│ Apps · Browser · UI · Media · AI Runtime                    │
├──────────────────────────────────────────────────────────────┤
│ Linux / Android / Hypervisor / Device Drivers               │
├──────────────────────────────────────────────────────────────┤
│ Privilege Separation · MMU · Interrupt Control · Security   │
├──────────────────────────────────────────────────────────────┤
│ Cortex-A Core(s) · Vector Engine · Branch Prediction        │
├──────────────────────────────────────────────────────────────┤
│ L1 / L2 / L3 Cache · Coherency · DRAM Controller            │
└──────────────────────────────────────────────────────────────┘
```

Cortex-A는 단순 제어기라기보다 "[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 친화적 계산 플랫폼"으로 이해해야 한다. 즉, 같은 ARM 계열이라도 Cortex-M처럼 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)를 곧바로 돌리는 칩과는 출발점이 다르다.

- **📢 섹션 요약 비유**: Cortex-A는 동네 자전거가 아니라 도심 종합 터미널과 같다. 승객(앱)이 많고 노선(메모리 공간)도 복잡하므로, 차고지 관리와 교통 통제가 함께 있어야 도시가 멈추지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Cortex-A의 설계 중심은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 지원이다. 이를 위해 최근 코어들은 깊은 파이프라인, 공격적 [분기 예측](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/231_branch_prediction/), [비순차 실행](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/238_out_of_order_execution/) (Out-of-Order Execution), 다중 발행 구조를 활용해 단위 시간당 더 많은 명령을 끝내려 한다. 다만 이런 구조는 평균 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 높이는 대신, 최악 응답 시간을 일정하게 맞추는 데는 불리하다.

가장 중요한 블록은 MMU다. MMU는 가상 주소를 물리 주소로 바꾸고, [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 단위 접근 권한을 검사해 프로세스마다 독립된 주소 공간을 제공한다. 이 기능 덕분에 Linux나 Android 같은 OS가 프로세스 격리, [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/), [메모리 매핑 파일](/knowledge-base/studynote/02_operating_system/07_virtual_memory/418_memory_mapped_file_mmap/), 사용자/[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)를 실현할 수 있다.

| 핵심 요소 | 역할 | 설계상 의미 |
| :-------- | :--- | :---------- |
| [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/) | 가상 주소 변환, 권한 검사 | 리치 OS와 앱 격리의 전제 |
| 캐시 계층 | 느린 [DRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 숨김 | 평균 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 변동성 증가 |
| 벡터 엔진 | 이미지·오디오·[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 전처리 가속 | 멀티미디어 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 향상 |
| 멀티코어·[캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) | 여러 코어가 같은 메모리 공유 | 앱 병렬성, 서버 확장성 확보 |
| 동적 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/)·주파수 조절 (Dynamic [Voltage](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/) and Frequency Scaling, [DVFS](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/469_dvfs/)) | 부하에 따라 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/)·클럭 조정 | 발열과 배터리 수명 균형 |

또 하나의 축은 전력 관리다. Cortex-A 기반 시스템 온 칩 ([System on Chip](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/), [SoC](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/))은 고성능 코어와 저전력 코어를 함께 두는 big.LITTLE 또는 DynamIQ 구성을 자주 사용한다. 무거운 전경 작업은 큰 코어가 맡고, 대기·음악 재생·[동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 같은 작업은 작은 코어가 맡아 같은 사용자 경험을 더 적은 전력으로 제공한다.

아래 그림은 Cortex-A가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 전력, 보안을 한 칩 안에서 동시에 조율하는 흐름을 보여준다.

```text
┌──────────────────────────────────────────────────────────────┐
│ Foreground App ───────▶ Big Core Cluster ───────┐           │
│ Background Task ─────▶ Little Core Cluster ───┐ │           │
│ Secure Service  ─────▶ Secure World           │ │           │
│                                                 ▼ ▼           │
│            MMU · Cache Coherency · Scheduler · DVFS          │
│                               │                              │
│                               ▼                              │
│                      Shared Cache / DRAM                     │
└──────────────────────────────────────────────────────────────┘
```

즉 Cortex-A는 "빠른 코어"가 아니라, OS·메모리·전력 정책이 함께 맞물려야 제 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 나는 시스템형 아키텍처다.

- **📢 섹션 요약 비유**: Cortex-A는 큰 주방이 있는 호텔 셰프 팀과 같다. 메인 셰프, 보조 셰프, 냉장 창고, 주문 관리 시스템이 함께 돌아가야 많은 손님을 빠르게 받으면서도 전기와 식재료를 낭비하지 않는다.

---

## Ⅲ. 비교 및 연결

Cortex-A를 정확히 이해하려면 같은 ARM 계열의 Cortex-R, Cortex-M과 경계를 봐야 한다. 셋 다 ARM [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 생태계를 공유하지만, 설계 목표가 다르다. Cortex-A는 평균 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)과 OS 기능이, Cortex-R은 결정적 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)이, Cortex-M은 저전력·저비용 제어가 우선이다.

| 구분 | Cortex-A | Cortex-R | Cortex-M |
| :--- | :------- | :------- | :------- |
| 핵심 목표 | OS 기반 고성능 애플리케이션 | 실시간 제어와 안전 | 초저전력 제어와 MCU |
| 메모리 체계 | [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/), 대형 캐시, 외부 [DRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/) | [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/) 장치 ([Memory Protection](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/) Unit, MPU), 긴밀 결합 메모리 (Tightly Coupled Memory, TCM) | 단순 메모리 맵, 내부 [SRAM](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/250_sram/)/Flash |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 기준 | [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/), [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/) | 최악 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/), 안정성 | [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 반응, 전력 |
| 주 사용 환경 | Linux, Android, [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) | 실시간 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) (Real-Time [Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), RTOS) | [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/), 소형 RTOS |
| 대표 장비 | 스마트폰, TV, Arm 서버 | [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), [모뎀](/knowledge-base/studynote/03_network/03_physical_layer_media/146_modem_modulator_demodulator/), 자동차 제어 | 센서, 웨어러블, 가전 |

x86과의 비교도 중요하다. x86 역시 리치 OS와 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)를 강하게 지원하지만, Cortex-A 계열은 같은 급의 사용자 경험을 더 낮은 전력 예산에서 구현하는 데 강점이 있다. 그래서 모바일에서는 사실상 표준이 되었고, 최근에는 클라우드 서버와 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 영역까지 넓어지고 있다.

정리하면 Cortex-A는 ARM 생태계 안에서 "범용 컴퓨팅"을 담당하는 축이다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/), 그래픽 처리 장치 ([Graphics Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/), [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)), 신경망 처리 장치 ([Neural Processing Unit](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/), [NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/))와 연결될수록 가치가 커진다.

- **📢 섹션 요약 비유**: Cortex-A, R, M은 같은 브랜드의 차라도 용도가 다른 셈이다. A는 승객과 짐을 많이 실은 고속 투어버스, R은 정해진 시간에 꼭 도착해야 하는 구급차, M은 배터리로 오래 달리는 전동 자전거에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 필요하니 무조건 Cortex-A"라는 판단이 가장 위험하다. Cortex-A는 강력하지만, 그 힘은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)·메모리·열 설계·전원 설계가 받쳐줄 때만 나온다. 반대로 리치 OS가 필요한데 Cortex-M을 고르면 [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/), [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템, 복수 프로세스 관리에서 곧 한계를 만난다.

### 적용 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. Linux·Android·[하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/)처럼 OS 중심 소프트웨어 스택이 필요한가?
2. 수백 메가바이트~수기가바이트 메모리와 고해상도 UI, 네트워크, 보안 기능이 필요한가?
3. 작업이 평균 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 중심인가, 아니면 마이크로초 단위 최악 응답 보장이 더 중요한가?
4. 방열판, 배터리, [DVFS](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/469_dvfs/) 정책까지 포함한 전력·열 설계를 감당할 수 있는가?

### 대표 적용 사례

- **스마트 카메라/엣지 게이트웨이**: UI, 웹 서버, 영상 처리, 원격 업데이트를 동시에 돌려야 하므로 Cortex-A 기반 SoC가 적합하다.
- **저전력 Arm 서버**: 웹 프런트엔드, [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/), 캐시 서버처럼 병렬성이 큰 워크로드에서 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 대비 전력 이점이 크다.
- **차량 인포테인먼트**: 지도, 미디어, 앱 실행, 보안 업데이트를 감당하려면 Cortex-A가 사실상 기본 선택이다.

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 브레이크 제어, 에어백, 산업용 안전 루프 같은 하드 실시간 작업을 Cortex-A 단독으로 맡기는 설계
- 코인셀 배터리 센서에 Cortex-A를 써서 부팅 시간과 대기전력을 과도하게 늘리는 설계
- big.LITTLE 구성을 넣고도 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)·열 제어 정책을 설계하지 않아 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 배터리를 둘 다 놓치는 설계

기술사 관점에서 Cortex-A는 "무거운 소프트웨어를 감당하는 두뇌"로 판단해야 한다. 제어기, 센서, 안전 제어 장치 (Electronic [Control Unit](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/206_control_unit/), ECU)까지 한 종류 코어로 통일하려 하기보다, A/R/M을 역할별로 분리하는 것이 보통 더 좋은 아키텍처다.

- **📢 섹션 요약 비유**: Cortex-A는 대형 주방용 인덕션이다. 큰 요리를 빨리 할 수 있지만, 캠핑용 작은 냄비 하나 데우겠다고 들고 나가면 전원도 무겁고 효율도 나빠진다.

---

## Ⅴ. 기대효과 및 결론

Cortex-A를 올바르게 채택하면 사용자 경험과 시스템 유연성이 크게 좋아진다. [멀티태스킹](/knowledge-base/studynote/02_operating_system/11_exam_summary/675_multitasking_terminology_preemptive/), 앱 격리, [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/), 멀티미디어 가속, [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)·[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 같은 현대 소프트웨어 요구를 한 플랫폼에서 처리할 수 있기 때문이다. 또한 같은 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 더 낮은 전력으로 제공하는 경우가 많아 모바일과 클라우드 모두에서 비용 경쟁력을 만든다.

반면 전제 조건도 분명하다. Cortex-A는 단순 제어기보다 보드 설계, 메모리 구성, 부트 체인, 전원 관리, 보안 업데이트 체계가 훨씬 복잡하다. 따라서 "전력 효율 좋은 만능 칩"으로 외우기보다, OS와 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 플랫폼을 올려놓기 위한 계층형 코어로 기억하는 편이 정확하다.

미래 방향은 더 강한 보안 격리, 더 넓은 벡터 연산, 더 세밀한 전력 제어, 그리고 CPU·[GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/)·[NPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/424_npu/) 협업이다. 결국 Cortex-A의 본질은 모바일용 CPU가 아니라, 전력 제약 아래 범용 컴퓨팅을 실현하는 ARM의 주력 실행 플랫폼이다.

- **📢 섹션 요약 비유**: Cortex-A는 작은 발전소가 딸린 복합 쇼핑몰과 같다. 손님이 많아도 공간을 나눠 운영하고, 전기 사용량을 조절하며, 보안 구역을 따로 두어야 오래 안정적으로 장사할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :---------- |
| [MMU](/knowledge-base/studynote/02_operating_system/06_memory_management/328_mmu/) | 프로세스 격리, [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/), 사용자/[커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)의 핵심 |
| [캐시 일관성](/knowledge-base/studynote/01_computer_architecture/11_multicore_synchronization/402_cache_coherence/) (Cache Coherency) | 멀티코어 Cortex-A에서 공유 메모리를 올바르게 유지 |
| TrustZone | 일반 세계와 보안 세계를 분리해 결제·키 관리를 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| big.LITTLE / DynamIQ | 부하별 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·전력 균형을 만드는 대표 전력 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| [하이퍼바이저](/knowledge-base/studynote/02_operating_system/01_overview_architecture/054_hypervisor/) | Cortex-A가 서버·[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 플랫폼으로 확장되는 기반 |

### 📈 관련 키워드 및 발전 흐름도

```text
ARM11 급 애플리케이션 코어
    │
    ▼
Cortex-A8 / A9: 스마트폰 OS 대중화
    │
    ▼
멀티코어 · 대형 캐시 · TrustZone
    │
    ▼
big.LITTLE · 64비트 ARMv8-A · 가상화
    │
    ▼
Arm 서버 · PC · AI/보안 강화형 ARMv9-A
```

이 흐름은 Cortex-A가 "모바일 코어"에서 "범용 저전력 컴퓨팅 플랫폼"으로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Cortex-A는 스마트폰 안에서 여러 앱을 질서 있게 움직이게 하는 큰 도시 시장님 같은 두뇌예요.
2. 게임할 때는 힘을 많이 쓰고, 음악만 들을 때는 살살 일해서 배터리를 아껴요.
3. 하지만 아주 빠르게 반응해야 하는 브레이크 같은 일은 더 전문적인 다른 코어에게 맡기는 게 좋아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 654 / 803

← **이전**: [652. 무정전 전원 장치 (UPS)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/652_ups_architecture/)
**다음**: [654. ARM Cortex-R 시리즈](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/654_arm_cortex_r_series/) →

---
