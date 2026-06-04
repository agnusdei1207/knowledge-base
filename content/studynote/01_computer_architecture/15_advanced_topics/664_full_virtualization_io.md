+++
title = "664. 전가상화 (Full Virtualization) I/O"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) ([Full Virtualization](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/)) I/O는 게스트 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)를 수정하지 않고도 실행할 수 있도록, 하이퍼바이저가 익숙한 하드웨어 장치를 소프트웨어로 흉내 내는 방식이다.
> 2. **가치**: 오래된 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), 설치 프로그램, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 부팅 환경처럼 전용 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 드라이버가 없거나 넣기 어려운 상황에서 가장 높은 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 제공한다.
> 3. **판단 포인트**: 장치 접근마다 [트랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)과 에뮬레이션 비용이 누적되므로, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로의 기본 선택지가 아니라 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)과 부트스트랩을 위한 안전망으로 보는 것이 맞다.

---

## Ⅰ. 개요 및 필요성

[전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O는 게스트 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 자신이 가상 환경에 있다는 사실을 전혀 모르게 하려는 접근이다. [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 네트워크 카드, 디스크 컨트롤러, 그래픽 장치 같은 익숙한 하드웨어가 실제로 존재한다고 믿고 그 규약에 맞춰 명령을 내린다. 그러면 하이퍼바이저는 해당 장치가 진짜 있는 것처럼 반응하는 소프트웨어 장치 모델을 제공한다. 덕분에 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)나 드라이버를 손대지 않아도 실행이 가능하다.

이 그림은 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O가 왜 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)은 높고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 불리한지를 한눈에 보여준다.

```text
+----------------------------------------------------------------------------+
|              전가상화 I/O의 기본 구조: 가짜 장치를 진짜처럼 연기          |
+----------------------------------------------------------------------------+
| Guest Driver --> I/O Port 또는 메모리 매핑 입출력 접근                      |
|                  |                                                         |
|                  v                                                         |
|             Trap 발생                                                      |
|                  |                                                         |
|                  v                                                         |
|        Hypervisor / Device Model --> Host Driver --> Physical Device         |
|                  |                                                         |
|                  +-------------- Interrupt Injection <----------------------+
+----------------------------------------------------------------------------+
```

이 방식이 필요했던 이유는 간단하다. 현실의 시스템에는 최신 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) 드라이버를 절대 설치할 수 없는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 많기 때문이다. 구형 윈도우, 오래된 산업 제어 시스템, 설치 미디어, 기본 입출력 시스템 (Basic Input/Output System, BIOS) 단계는 가상 환경에 최적화된 장치 모델을 기대하지 않는다. 그래서 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O는 느리더라도 “무조건 부팅되게 하는 기술”로서 계속 필요하다.

- **📢 섹션 요약 비유**: [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O는 배우가 실제 직업인처럼 완전히 역할을 연기하는 연극과 같다. 관객은 속기 쉽지만, 배우는 계속 힘을 써야 하니 오래 지속하면 피곤해진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O의 중심은 [트랩](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/) 앤 에뮬레이트 ([Trap](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)-and-Emulate)다. 게스트가 입출력 포트나 메모리 매핑 입출력 (Memory-Mapped I/O, MMIO) 영역에 접근하면 중앙 처리 장치 (Central Processing Unit, CPU)가 이를 잡아 하이퍼바이저로 넘긴다. 하이퍼바이저는 어떤 장치의 어떤 레지스터에 어떤 값이 들어왔는지 해석하고, 소프트웨어로 장치 상태를 갱신하거나 실제 호스트 장치 동작으로 변환한다. 이후 처리 결과가 준비되면 가상 [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 주입해 게스트에게 완료를 알린다.

| 구성요소 | 역할 | 비용 포인트 |
| :-- | :-- | :-- |
| 장치 모델 | 가상 네트워크 카드와 디스크 컨트롤러 등의 동작 모사 | 장치가 복잡할수록 소프트웨어 부담 증가 |
| [Trap](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/) | 게스트의 장치 접근 가로채기 | 접근 빈도만큼 제어 전환 발생 |
| MMIO / [Port](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) I/O | 장치 명령 전달 통로 | 작은 접근도 모두 해석 대상 |
| [Interrupt](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [Injection](/knowledge-base/studynote/04_software_engineering/11_testing_validation/872_injection/) | 완료 사실을 게스트에 알림 | [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리까지 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 필요 |
| Host Backend | 실제 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/), 디스크와 연결 | 사용자 공간 왕복 시 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 확대 |

현대 리눅스 기반 환경에서는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 기반 가상 머신 (Kernel-based [Virtual Machine](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), [KVM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/))과 큐뮬레이터 (Quick Emulator, QEMU)가 함께 이 일을 나누어 맡는 경우가 많다. KVM은 CPU와 메모리 실행을 가속하고, QEMU는 각 장치의 세부 동작을 구현한다. 문제는 장치 접근이 잦을수록 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)과 사용자 공간을 오가는 경로가 반복되어 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 커진다는 점이다. 즉 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O의 병목은 디스크나 네트워크 대역폭보다 “장치 접근을 해석하는 절차적 비용”에서 먼저 드러나는 경우가 많다.

[전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O가 여전히 중요한 이유는 바로 이 복잡함 덕분이기도 하다. 하이퍼바이저가 오래된 장치 규격을 완전히 흉내 내면, 게스트 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 익숙한 드라이버를 그대로 쓸 수 있다. 그래서 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O는 느린 대신 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)이 넓고, 가상 환경의 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 단계나 예외적인 레거시 운영에 매우 강하다.

- **📢 섹션 요약 비유**: [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O는 수작업 민원 창구와 같다. 모든 요청을 직접 받아서 처리하니 누구나 이용할 수 있지만, 창구 직원이 하나씩 응대하므로 줄이 길어질 수밖에 없다.

---

## Ⅲ. 비교 및 연결

[전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)만 놓고 보면 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/)나 장치 패스스루보다 불리하다. 하지만 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/), 설치 편의, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 부팅 지원 면에서는 여전히 강하다. 그래서 실제 시스템에서는 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O와 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O를 순차적으로 함께 쓰는 경우도 많다. 예를 들어 가상 머신 설치 단계에서는 에뮬레이션 디스크와 네트워크 장치로 부팅하고, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 올라온 뒤 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) 드라이버를 설치해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로를 바꾸는 식이다.

| 비교 항목 | [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O | [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O | 장치 패스스루 |
| :-- | :-- | :-- | :-- |
| 게스트 수정 여부 | 불필요 | 전용 드라이버 필요 | 드라이버와 하드웨어 지원 필요 |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 낮음 | 높음 | 매우 높음 |
| [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) | 매우 높음 | 중간 | 낮음 |
| [라이브 마이그레이션](/knowledge-base/studynote/02_operating_system/10_security/629_live_migration_pre_copy/) | 쉬움 | 쉬움 | 어려움 |
| 대표 사용 시점 | 부팅, 레거시, 설치 | 일반 [서비스 운영](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_service_operation/) | 초저지연 특수 워크로드 |

여기서 기억할 연결점은 “[전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/)는 사라진 기술이 아니라 역할이 재정의된 기술”이라는 사실이다. 예전에는 전체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경로를 담당했다면, 지금은 부트스트랩, 레거시 유지, 안전한 [fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/) 경로를 담당하는 경우가 많다. 즉 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 주인공 자리에서는 내려왔지만, [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)의 최후 보루라는 의미는 여전히 크다.

- **📢 섹션 요약 비유**: [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O가 만능 어댑터라면 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/)는 고속 충전기다. 평소에는 고속 충전기를 쓰더라도, 낯선 콘센트 앞에서는 결국 만능 어댑터가 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O를 선택하는 대표 장면은 두 가지다. 첫째, 오래된 시스템을 물리 서버에서 가상 서버로 옮기는 물리-가상 전환 (Physical-to-Virtual, P2V) 프로젝트다. 오래된 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 최신 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) 드라이버를 알지 못하므로, 에뮬레이션 장치가 있어야 일단 부팅이 된다. 둘째, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 설치 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)나 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 환경이다. 아직 전용 드라이버가 올라오기 전에도 디스크와 화면, 키보드가 동작해야 설치와 유지보수가 가능하다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 게스트 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) 드라이버 없이도 반드시 동작해야 하는가?
2. 설치 단계 이후 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/)나 다른 고성능 경로로 전환할 계획이 있는가?
3. 에뮬레이션 장치 선택이 게스트 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 내장 드라이버와 맞는가?
4. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로가 에뮬레이션 위에 남아 병목이 되지 않는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) 설치가 끝났는데도 에뮬레이션 네트워크 카드와 디스크를 그대로 운영 경로에 두는 것
- 고성능 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스나 패킷 처리 서버에 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O를 기본 구성으로 채택하는 것
- 중첩 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 환경에서 다시 에뮬레이션 장치를 겹쳐 사용해 제어 전환 비용을 폭증시키는 것

기술사 판단은 “[호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 우선인지, 운영 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 우선인지”를 선명하게 나누는 데 있다. 낡은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)를 살려야 한다면 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O는 정답일 수 있다. 반대로 일반적인 [서비스 운영](/knowledge-base/studynote/12_it_management/02_itsm_itil/067_service_operation/) 경로라면 가급적 설치 단계까지만 쓰고, 이후에는 [반가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/)나 다른 최적화 경로로 옮겨야 한다.

- **📢 섹션 요약 비유**: [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O는 비상 발전기와 같다. 정전 때는 반드시 필요하지만, 공장 전체를 계속 비상 발전기만으로 돌리면 비용과 효율이 모두 나빠진다.

---

## Ⅴ. 기대효과 및 결론

[전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O의 기대효과는 최고 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 아니라 최고 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)이다. 어떤 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 들어오더라도 비교적 익숙한 장치 규격을 제공해 일단 실행시키고, 설치와 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 마이그레이션 같은 운영 절차를 안정적으로 시작할 수 있게 만든다. 그래서 이 기술은 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 인프라의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 엔진이라기보다, 시스템을 반드시 살려 내는 안전장치에 가깝다.

한계 역시 분명하다. 장치 접근 해석, 문맥 전환, [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 재주입 비용이 겹치면 처리량과 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 모두 불리해진다. 따라서 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O를 기억할 때는 “느린 구식 기술”이 아니라, “[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)에서 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)과 부트스트랩을 담당하는 기반 기술”로 이해하는 편이 정확하다. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 경로의 주인공은 아니어도, 없으면 곤란한 장면이 분명히 존재한다.

- **📢 섹션 요약 비유**: [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O는 오래된 열쇠도 대부분 맞게 만드는 만능 자물쇠와 같다. 빠른 자동문은 아니지만, 열리지 않는 문을 줄여 주는 값어치가 있다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [Trap](/knowledge-base/studynote/02_operating_system/11_exam_summary/677_trap_based_system_call_implementation/)-and-Emulate | [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O의 기본 실행 모델 |
| MMIO | 현대 장치 접근을 가로채는 대표 경로 |
| [Interrupt](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) [Injection](/knowledge-base/studynote/04_software_engineering/11_testing_validation/872_injection/) | 에뮬레이션 완료를 게스트에 되돌리는 장치 |
| QEMU | 소프트웨어 장치 모델을 구현하는 대표 구성요소 |
| [Paravirtualization](/knowledge-base/studynote/02_operating_system/01_overview_architecture/058_paravirtualization/) I/O | [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) 이후 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 경로를 맡는 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
무수정 게스트 실행 요구
    |
    v
장치 에뮬레이션 기반 전가상화 I/O
    |
    v
Trap-and-Emulate · MMIO 가로채기
    |
    v
설치/부팅 단계 호환성 확보
    |
    v
반가상화 I/O · 패스스루로 운영 경로 분화
```

이 흐름은 [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O가 “전체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 경로”에서 “[호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)과 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구동을 담당하는 기반 경로”로 역할이 이동한 배경을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [전가상화](/knowledge-base/studynote/02_operating_system/01_overview_architecture/057_full_virtualization/) I/O는 진짜 장난감처럼 보이는 가짜 장난감을 만들어 주는 방법이에요.
2. 그래서 오래된 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)도 익숙한 장난감이라고 생각하고 바로 놀 수 있어요.
3. 하지만 뒤에서 누군가 계속 장난감을 움직여 줘야 해서 오래 쓰면 힘이 많이 든답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 665 / 803

<- **이전**: [663. 반가상화 (Paravirtualization) I/O](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/663_paravirtualization_io/)
**다음**: [665. Virtio 드라이버 모델](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/665_virtio_driver_model/) ->

---
