+++
title = "465. 락스텝 (Lockstep) 아키텍처"
date = 2026-03-22

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 락스텝 아키텍처는 동일한 연산 경로를 2개 이상 동시에 실행하고 결과를 즉시 비교해, CPU (Central Processing Unit) 내부의 조용한 연산 오류를 시스템 밖으로 내보내기 전에 잡아내는 구조다.
> 2. **가치**: [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) (Error Correcting [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/))가 메모리 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류를 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)한다면, 락스텝은 코어 실행·[레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 갱신·[버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 출력처럼 <strong>연산 그 자체</strong>의 이상을 감시하므로 기능 안전 시스템의 마지막 방어선이 된다.
> 3. **판단 포인트**: 락스텝은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상 기법이 아니라 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 투자이므로, 면적·전력 증가와 공통 원인 고장(Common-Mode Failure) 위험까지 감당할 때만 의미가 있다.

---

## Ⅰ. 개요 및 필요성

락스텝 아키텍처 (Lockstep [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/))는 두 개 이상의 동일한 프로세서 코어가 같은 클럭, 같은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 흐름, 같은 입력 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 받아 같은 시점에 같은 결과를 내도록 맞춰 두고, 그 결과를 비교 회로로 대조하는 고신뢰성 설계다. 핵심 목적은 빠르게 계산하는 것이 아니라, 계산 결과가 틀렸을 때 그것을 <strong>즉시 검출</strong>하는 데 있다.

이 구조가 필요한 이유는 모든 오류가 메모리나 저장장치에서만 생기지 않기 때문이다. 방사선에 의한 SEU (Single Event Upset), 전원 흔들림, 제조 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/), 배선 노이즈는 CPU [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)나 연산 경로를 순간적으로 뒤틀 수 있고, 이런 오류는 정상 프로그램 흐름 속에서 조용히 잘못된 제어 명령으로 바뀔 수 있다. 자동차 제동 제어, 철도 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/), 산업용 안전 [PLC](/knowledge-base/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/) ([Programmable Logic Controller](/knowledge-base/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/))처럼 한 번의 오판이 치명적인 시스템에서는 "고장 나면 재시작"이라는 접근이 통하지 않는다.

특히 단일 코어 시스템은 결과가 틀려도 스스로 틀렸다는 사실을 알기 어렵다. 반면 락스텝은 같은 문제를 두 명의 계산기에게 동시에 풀게 한 뒤 답을 대조하므로, 적어도 단일 코어에서 발생한 일시적 오류는 외부 출력 이전에 드러낼 수 있다. 즉 락스텝의 본질은 예비 부품 확보가 아니라 <strong>실행 중 진실성 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>이다.

- **📢 섹션 요약 비유**: 락스텝은 중요한 계약서를 두 명의 변호사가 동시에 읽고 한 줄씩 맞춰 보는 일과 같다. 한 명이 한 글자라도 잘못 읽으면 서명 전에 바로 멈출 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

락스텝의 핵심 메커니즘은 단순하다. 같은 입력을 두 코어에 동시에 넣고, 파이프라인의 특정 지점에서 결과를 비교하며, 불일치가 발생하면 즉시 Fault [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 올려 시스템을 [안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/)로 전환한다. 하지만 실제 구현에서는 무엇을 비교할지, 어느 시점에서 비교할지, 불일치 뒤 어떤 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 동작을 수행할지가 함께 설계되어야 한다.

아래 그림은 듀얼 락스텝 (Dual Lockstep)의 대표 흐름을 보여준다.

```text
+----------------------------------------------------------------------+
|                듀얼 락스텝 동작 흐름: 실행과 동시에 검증            |
+----------------------------------------------------------------------+
| 동일 입력(명령어·데이터·인터럽트)                                   |
|                  |                                                   |
|        +---------+---------+                                         |
|        v                   v                                         |
|  +-------------+     +-------------+                                 |
|  | Core A      |     | Core B      |                                 |
|  | same clock  |     | same clock  |                                 |
|  | same state  |     | same state  |                                 |
|  +------+------+     +------+------+                                 |
|         |                   |                                        |
|         +---------+---------+                                        |
|                   v                                                  |
|           +-----------------+                                        |
|           | Comparator      |  레지스터·버스·예외 신호 비교          |
|           +------+----------+                                        |
|                  |                                                   |
|        +---------+---------+                                         |
|        v                   v                                         |
|   Match: 정상 진행     Mismatch: Fault/NMI/Fail-Safe                 |
+----------------------------------------------------------------------+
```

이 그림의 포인트는 락스텝이 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 코어를 나중에 깨우는 구조가 아니라, <strong>주 코어와 그림자 코어가 이미 함께 실행 중</strong>이라는 점이다. 따라서 오류는 장애 후 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 단계가 아니라 실행 단계에서 검출된다.

| 구성 요소 | 역할 | 설계 포인트 | 대표 위험 |
| :--- | :--- | :--- | :--- |
| 주 코어 (Primary Core) | 기준 실행 수행 | [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)·입력 순서 보장 | 내부 연산 오류 |
| 그림자 코어 (Shadow Core) | 동일 작업 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 상태·클럭 정렬 | 동기 어긋남 |
| [비교기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/) ([Comparator](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/)) | 결과 불일치 판정 | 비교 지점 최소화·[지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 관리 | [Comparator](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/) 자체 장애 |
| 오류 처리 로직 | Fault 발생 시 [안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/) 전환 | [NMI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/558_nmi/) ([Non-Maskable Interrupt](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/558_nmi/)), 리셋, 차단 | 과도한 오탐 |

구현 방식은 완전 동시 락스텝과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 락스텝 (Delayed Lockstep)으로 나눠 볼 수 있다. 완전 동시 락스텝은 두 코어가 같은 클럭 에지에서 같은 상태를 갱신하므로 구조가 직관적이고 검출 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 짧다. [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 락스텝은 그림자 코어를 몇 사이클 뒤따라가게 만들어 일시적 전원 노이즈나 타이밍 글리치를 분리해 보기도 하는데, 대신 상태 버퍼와 비교 로직이 더 복잡해진다.

중요한 한계도 분명하다. 듀얼 락스텝은 두 코어 결과가 다를 때 오류를 <strong>탐지</strong>할 수는 있지만, 어느 쪽이 정답인지 스스로 <strong>교정</strong>하지는 못한다. 그래서 락스텝은 오류 은닉보다 오류 검출과 안전 정지에 강한 구조로 이해해야 한다.

- **📢 섹션 요약 비유**: 락스텝은 무대 뒤 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 배우가 아니라, 두 배우가 같은 대사를 동시에 말하고 옆에서 감독이 한 글자씩 맞추는 방식과 같다. 틀린 대사가 나오면 공연을 계속 밀어붙이기보다 바로 멈추는 데 강하다.

---

## Ⅲ. 비교 및 연결

락스텝을 제대로 이해하려면 인접한 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 기법과의 경계를 분명히 봐야 한다. 모두 "안전"을 목표로 하지만, 오류를 다루는 위치와 방식이 서로 다르다. 특히 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) ([Dual Redundancy](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)), [TMR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/455_tmr/) (Triple Modular Redundancy), ECC는 자주 함께 묶이므로 차이를 명확히 기억해야 한다.

| 기법 | [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 대상 | 오류 대응 방식 | 강점 | 한계 |
| :--- | :--- | :--- | :--- | :--- |
| 락스텝 (Lockstep) | CPU 실행 경로 | 동시 실행 후 비교 | 연산 오류 즉시 검출 | 자동 정정 어려움 |
| [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) ([Dual Redundancy](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)) | 시스템 자원 전체 | 장애 시 절체 | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 향상 | 실행 중 계산 진실성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 약함 |
| [TMR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/455_tmr/) (Triple Modular Redundancy) | 연산 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) | 3중 실행 + 다수결 | 오류 탐지와 은닉 가능 | 면적·전력 비용 큼 |
| [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) (Error Correcting [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)) | 메모리 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) | 저장 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정정 | 메모리 오류 대응 효율적 | CPU 계산 오류는 직접 못 잡음 |

[이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)와 락스텝의 차이는 "언제 두 번째 자원을 쓰는가"에 있다. Active-Standby [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)는 평소 예비 장치를 쉬게 두다가 장애가 난 뒤 절체하지만, 락스텝은 예비가 아니라 <strong>동시 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>자</strong>를 항상 함께 돌린다. 그래서 락스텝은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)보다 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)에 더 가깝다.

TMR과의 비교도 중요하다. 듀얼 락스텝은 결과가 다르면 "문제가 있다"는 사실을 알려 주지만 정답 선택은 어렵다. 반면 TMR은 세 결과 중 다수결로 하나를 선택하므로 한 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 오류를 가리고 계속 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)할 수 있다. 즉 락스텝이 안전 정지([Fail-Safe](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/459_fail_safe/))에 강하다면, TMR은 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 지속(Fault Masking)에 더 강하다.

또한 락스텝은 소프트웨어 다양성 문제와도 연결된다. 두 코어가 동일한 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)와 동일한 버그를 그대로 실행하면, 설계 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)이나 잘못된 제어 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 같은 공통 원인 고장은 두 코어에서 똑같이 발생할 수 있다. 그래서 기능 안전 시스템은 락스텝만으로 끝내지 않고 [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/), [Watchdog Timer](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/461_watchdog_timer/), [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/803_memory_protection/), 진단 커버리지 계산을 함께 묶어 다층 방어를 만든다.

- **📢 섹션 요약 비유**: 락스텝은 두 명이 같은 답안을 써서 비교하는 방식이고, TMR은 세 명이 써서 다수결로 정답을 고르는 방식이다. 전자는 틀림을 빨리 알아차리는 데 강하고, 후자는 틀린 사람을 끼고도 수업을 계속하는 데 강하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 락스텝은 "중요하니까 일단 넣는다"가 아니라, 잘못된 계산이 외부 세계에 직접 피해를 주는 제어 계통에 우선 적용하는 구조다. 대표적으로 자동차 MCU ([Microcontroller](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/) Unit)의 제동·조향 제어, 항공 전자 장비, 철도 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 제어, 산업 안전 [PLC](/knowledge-base/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/), 우주·방산 제어기에서 많이 채택된다. 이런 환경에서는 몇 밀리초의 재시작 시간보다도 "잘못된 명령을 내보내지 않는 것"이 더 중요하다.

반대로 범용 애플리케이션 서버나 일반 웹 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 보통 락스텝보다 클러스터 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/), 재시도, 체크포인트, 장애 조치가 더 경제적이다. 락스텝은 코어 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)와 [비교기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/) 추가로 면적, 전력, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 비용이 증가하고, 동일 설계 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)에는 취약하므로 비용 대비 효과가 필요한 곳에만 써야 한다. 즉 락스텝은 고가용성의 일반 해법이 아니라, <strong>안전 필수 연산 경로를 위한 특수 해법</strong>이다.

### 설계 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 비교 대상이 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 결과인지, [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 트랜잭션인지, 예외 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)까지 포함하는지 명확한가?
2. 불일치 발생 시 시스템은 리셋, [NMI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/558_nmi/), 출력 차단, 페일세이프 중 무엇으로 전환하는가?
3. 두 코어가 같은 전원·같은 클럭 트리·같은 설계 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)에 동시에 영향을 받는 공통 원인 고장을 어떻게 줄일 것인가?
4. 락스텝 오류를 상위 안전 메커니즘이 진단 로그와 함께 처리할 수 있는가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 락스텝을 적용했으니 소프트웨어 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 덜 중요하다고 생각하는 경우
- Comparator를 추가했지만 오류 후 [안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/) 전환 절차를 설계하지 않은 경우
- 동일 전원 글리치와 동일 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 버그를 무시하고 "코어가 두 개니 안전하다"고 판단하는 경우

기술사 답안에서는 "락스텝은 오류 정정 구조가 아니라 오류 검출 구조"라는 문장을 분명히 쓰는 것이 좋다. 또한 [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/), [Watchdog Timer](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/461_watchdog_timer/), [TMR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/455_tmr/), Fail-Safe와의 관계를 함께 언급하면 설계 계층을 더 입체적으로 설명할 수 있다.

- **📢 섹션 요약 비유**: 락스텝은 비행기 자동조종 장치에 두 개의 계산기를 붙여 서로 감시하게 하는 일과 같다. 중요한 것은 계산기를 두 대 두는 것보다, 둘이 다르면 즉시 안전 모드로 넘기는 규칙까지 준비하는 것이다.

---

## Ⅴ. 기대효과 및 결론

락스텝의 가장 큰 효과는 CPU 내부에서 생긴 잘못된 계산이 시스템 외부 제어 명령으로 번지기 전에 잡아낼 수 있다는 점이다. 그 결과 안전 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), 진단 커버리지, 장애 분석 가능성이 높아지고, 기능 안전 인증에서 요구하는 하드웨어 진단 메커니즘을 설계하기 쉬워진다. 특히 [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/803_memory_protection/)와 결합하면 저장 오류와 실행 오류를 서로 다른 층위에서 동시에 방어할 수 있다.

하지만 락스텝은 비용 없는 안전장치가 아니다. 코어 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), 비교 로직, 추가 배선, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 범위 확장으로 면적과 소비전력이 증가하며, 동일 설계 버그나 동일 환경 교란에는 여전히 취약하다. 따라서 락스텝은 "절대 고장 나지 않는 구조"가 아니라, <strong>단일 실행 오류를 빨리 드러내고 안전하게 멈추게 하는 구조</strong>로 기억해야 한다.

앞으로는 단순 동기 비교를 넘어, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 락스텝, 부분 락스텝, 소프트웨어 진단과 결합한 하이브리드 안전 아키텍처로 발전하는 흐름이 강화될 가능성이 크다. 결국 락스텝의 핵심은 하나다. 더 빠른 컴퓨터를 만드는 기술이 아니라, 틀린 계산을 그대로 믿지 않게 만드는 기술이다.

- **📢 섹션 요약 비유**: 락스텝은 달리기 선수를 더 빠르게 만드는 훈련이 아니라, 결승선 판정 사진을 한 장 더 찍어 오심을 막는 장치에 가깝다. 속도보다 판정의 신뢰를 높이는 데 가치가 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) ([Dual Redundancy](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)) | 자원 절체 중심 구조이며, 락스텝과 달리 실행 중 결과 비교보다 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 지속성에 초점을 둔다. |
| [TMR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/455_tmr/) (Triple Modular Redundancy) | 락스텝보다 비용이 크지만 다수결로 오류를 은닉할 수 있어 지속 운용에 유리하다. |
| [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) (Error Correcting [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/)) | 메모리 계층 오류를 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)하며, 락스텝과 결합해 저장·실행 양쪽을 방어한다. |
| [Watchdog Timer](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/461_watchdog_timer/) | 락스텝이 놓친 소프트웨어 정지·무한 루프를 감시하는 보완 진단 장치다. |
| [Fail-Safe](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/459_fail_safe/) | 락스텝 불일치가 감지됐을 때 시스템을 [안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/)로 이행시키는 운영 원칙이다. |
| 기능 안전 (Functional Safety) | 락스텝을 채택하는 대표 배경이며, 하드웨어 진단 커버리지 확보와 직접 연결된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 코어 실행
    |
    v
오류 검출 한계 인식
    |
    v
이중화 (Dual Redundancy)
    |   +- 장애 후 절체 중심
    v
락스텝 (Lockstep) 비교 실행
    |   +- CPU 연산 오류 즉시 검출
    v
TMR (Triple Modular Redundancy)
    |   +- 다수결 기반 오류 은닉
    v
ECC · Watchdog Timer · Fail-Safe 결합
    |
    v
기능 안전 중심 하이브리드 진단 아키텍처
```

이 흐름은 단순 예비 자원 확보에서 시작해, 실행 결과 비교와 다중 진단 계층을 더하는 방향으로 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 설계가 진화함을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 아주 중요한 계산을 할 때 친구 한 명만 풀면, 몰래 틀려도 아무도 모를 수 있어요.
2. 그래서 똑같은 친구 둘이 동시에 풀고 답을 바로 비교하면, 누군가 실수했는지 금방 알 수 있어요.
3. 락스텝은 컴퓨터가 "틀린 답을 그냥 믿지 않도록" 옆에서 같이 확인해 주는 짝꿍 같은 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 466 / 803

<- **이전**: [464. 메모리 미러링 (Memory Mirroring)](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/464_memory_mirroring/)
**다음**: [466. 전력 소모 (Power Consumption)](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/466_power_consumption/) ->

---
