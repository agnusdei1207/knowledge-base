---
title: "Watchdog Timer"
date: "2026-03-20"
tags:
  - "studynote-computer-architecture"
---

# 워치독 타이머 (Watchdog [Timer](/studynote/02_operating_system/01_overview_architecture/071_os_timer/))

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 워치독 타이머 (Watchdog [Timer](/studynote/02_operating_system/01_overview_architecture/071_os_timer/))는 메인 처리계가 정해진 시간 안에 "정상 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중"이라는 신호를 보내지 못하면, 하드웨어가 시스템을 강제로 리셋하여 멈춘 상태를 끊어내는 자율 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 장치다.
> 2. **가치**: 사람이 즉시 전원 버튼을 누를 수 없는 임베디드 장비, 차량 전자제어장치, 산업 제어 보드, 원격 서버에서 워치독은 평균 수리 시간인 [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) (Mean Time To Repair)을 기계적으로 줄이는 마지막 안전망이 된다.
> 3. **판단 포인트**: 중요한 것은 워치독을 "켜는 것"이 아니라, 어떤 작업 완료를 생존 신호로 인정할지와 [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)을 얼마나 줄지 정하는 것이다. 잘못 설계하면 장애 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 장치가 오히려 정상 시스템을 반복 재부팅하는 원인이 된다.

---

## Ⅰ. 개요 및 필요성

워치독 타이머는 CPU (Central Processing Unit), 운영체제인 OS ([Operating System](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)), 혹은 애플리케이션이 응답 불능 상태에 빠졌을 때 시스템을 자동으로 재시작시키는 감시용 타이머다. 핵심 아이디어는 단순하다. 메인 시스템이 일정 주기마다 "나는 정상적으로 다음 단계까지 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)했다"는 신호를 보내면 타이머를 다시 채우고, 그 신호가 끊기면 비정상 정지로 판단해 리셋을 수행한다.

이 장치가 필요한 이유는 많은 장애가 완전한 전원 차단보다 더 나쁜 상태를 만들기 때문이다. 무한 루프, [교착 상태](/studynote/02_operating_system/05_deadlock/281_deadlock_definition/), [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 폭주, [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 응답 정지, 드라이버 오류가 발생하면 시스템은 살아 있는 것처럼 보이지만 실제 기능은 수행하지 못한다. 이때 외부 운영자가 바로 개입할 수 없는 환경이라면, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 계속 멎어 있으면서도 스스로 회복하지 못한다.

특히 자동차 전자제어장치, 산업용 [PLC](/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/) ([Programmable Logic Controller](/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/)), 의료 장비, 무인 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) (Internet of Things) 센서 노드처럼 현장 접근 비용이 큰 시스템에서는 워치독이 사실상 필수다. 오류를 "예방"하지는 못해도, 멈춤을 장시간 방치하지 않게 만들어 장애의 지속 시간을 제한한다. 그래서 워치독은 고장 허용보다 더 원초적인 수준의 [페일 세이프](/studynote/01_computer_architecture/13_reliability_power_management/459_fail_safe/) ([Fail-Safe](/studynote/01_computer_architecture/13_reliability_power_management/459_fail_safe/)) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 장치로 이해해야 한다.

📢 섹션 요약 비유: 워치독은 혼자 일하는 야간 경비원에게 달린 자동 신고 장치와 같다. 경비원이 정해진 시간마다 본부에 무전을 보내면 괜찮지만, 무전이 끊기면 본부는 "쓰러졌거나 갇혔다"고 보고 문을 강제로 열고 대응팀을 투입한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

전형적인 워치독 타이머는, 흔히 WDT (Watchdog [Timer](/studynote/02_operating_system/01_overview_architecture/071_os_timer/))라고 줄여 부르는 감시 블록으로서, 독립 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), 리셋 출력선, 그리고 소프트웨어의 주기적 갱신 루틴으로 구성된다. 중요한 설계 원칙은 감시자가 피감시자와 너무 강하게 결합되지 않아야 한다는 점이다. 그래서 많은 마이크로컨트롤러인 MCU ([Microcontroller](/studynote/01_computer_architecture/03_architecture_basics_performance/130_microcontroller/) Unit)나 시스템 온 칩인 [SoC](/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/) ([System on Chip](/studynote/01_computer_architecture/03_architecture_basics_performance/131_soc/))는 메인 코어와 별도 클럭 또는 저전력 도메인에서 워치독을 구동한다.

아래 그림은 워치독이 "시간 초과 감지 -> [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 실행"까지 이어지는 경로를 보여준다.

```text
+----------------------------------------------------------------------+
|               워치독 타이머의 기본 감시-복구 흐름                   |
+----------------------------------------------------------------------+
|  정상 경로                                                           |
|  애플리케이션 진행 ---> 상태 확인 ---> 워치독 갱신(kick) --> 카운터 재시작 |
|      ^                                                              |
|      +-------------- 주기 내 완료되면 반복 --------------------------+
|                                                                      |
|  장애 경로                                                           |
|  무한 루프/교착/버스 정지 ---> 워치독 갱신 실패 ---> 타임아웃 만료      |
|                                                   |                  |
|                                                   v                  |
|                                   인터럽트/로그 저장(선택)           |
|                                                   |                  |
|                                                   v                  |
|                                        하드웨어 리셋 또는 전원 재인가 |
+----------------------------------------------------------------------+
```

이 메커니즘의 핵심은 "단순 주기"가 아니라 "의미 있는 진전"이다. 예를 들어 메인 루프가 센서 읽기, 제어 계산, 출력 반영까지 끝냈을 때만 워치독을 갱신해야 실제 시스템 건강을 검증할 수 있다. 반대로 타이머 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 자동으로 계속 갱신해 버리면, 애플리케이션이 죽어도 워치독은 정상으로 오판한다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 독립 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) | 시간을 감소시키며 만료 여부 판단 | 메인 코어 정지와 분리된 클럭/전원 필요 |
| 갱신 동작 (Kick/Pet) | 정상 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/)을 증명하고 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) 재시작 | 단순 생존이 아니라 실제 작업 완료 후 수행 |
| [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 값 | 허용 가능한 최대 정지 시간 정의 | 정상 최악 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)보다 길고, 장애 방치 시간보다 짧아야 함 |
| 리셋 동작 | 시스템 상태 초기화 | 리셋 원인 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), 덤프 저장과 연계하면 분석성 향상 |
| 윈도우 워치독 | 너무 늦어도, 너무 빨라도 오류로 판정 | 폭주 루프가 무의미하게 연속 갱신하는 우회 차단 |

고급형 워치독은 윈도우 모드를 제공한다. 이는 "최대 시간"만 보는 것이 아니라 "허용된 시간 창" 안에서만 갱신을 받는다. 너무 늦으면 멈춤, 너무 빠르면 비정상 폭주로 간주한다. 따라서 단순한 무한 루프뿐 아니라 잘못된 빠른 반복 루프까지 잡아낼 수 있다.

또한 일부 시스템은 [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 직전에 경고 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)를 먼저 보내 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 남길 기회를 준다. 이를 통해 리셋 직전 [프로그램 카운터](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/), 센서 값, 큐 적체량을 저장하면 원인 분석이 쉬워진다. 즉 워치독은 단순 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 장치이면서 동시에 장애 관찰 장치가 될 수 있다.

📢 섹션 요약 비유: 워치독은 모래시계와 비상 차단기가 합쳐진 장치다. 담당자가 정해진 업무를 마칠 때마다 모래시계를 뒤집으면 계속 일할 수 있지만, 모래가 끝나도록 아무 진전이 없으면 차단기가 내려가서 설비를 처음 상태로 되돌린다.

---

## Ⅲ. 비교 및 연결

워치독을 제대로 이해하려면 하드웨어 워치독, 소프트웨어 워치독, 그리고 플랫폼 수준 헬스체크를 구분해야 한다. 셋 다 "응답 없으면 재시작"이라는 공통점을 가지지만, 감시 범위와 신뢰 경계가 다르다. 이 차이가 곧 어느 계층의 장애를 잡을 수 있는지 결정한다.

| 구분 | 하드웨어 워치독 | 소프트웨어 워치독 | 플랫폼 헬스체크 |
| :--- | :--- | :--- | :--- |
| 감시 주체 | 칩 내부 독립 타이머 | OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)/데몬/별도 [스레드](/studynote/02_operating_system/02_process_thread/092_thread_lwp/) | [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) (K8s) 같은 오케스트레이터 |
| 잘 잡는 장애 | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 정지, [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 정지, 전체 시스템 멈춤 | 프로세스 교착, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 응답 정지 | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 비정상, 인스턴스 비가용 |
| 약점 | 세밀한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 품질 판별은 어려움 | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 전체가 멈추면 함께 멈출 수 있음 | 노드 내부 하드웨어 정지까지는 직접 못 봄 |
| 대표 목적 | 보드/장치 자율 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 프로세스 단위 자기 치유 | 클러스터 단위 자동 재배치 |

하드웨어 워치독은 가장 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)이 높지만 가장 거칠다. 이유를 따지기보다 시스템을 리셋해 "다시 시작"시키는 데 집중한다. 반면 소프트웨어 워치독은 더 정교한 조건을 볼 수 있지만, 자신도 같은 운영 환경에 의존하므로 더 아래 계층의 장애에는 취약하다.

이 개념은 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 하트비트 (Heartbeat), [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 장애 조치, 네트워크 Keepalive와도 연결된다. 결국 모두 "정해진 시간 안에 의미 있는 응답이 없으면 죽은 것으로 본다"는 동일한 철학을 공유한다. 컴퓨터구조의 워치독이 보드 수준 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 장치라면, 클라우드의 Liveness Probe는 그 철학을 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준으로 확장한 형태다.

따라서 워치독은 단순한 임베디드 기능이 아니라, [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 공학 전반의 기본 패턴이다. 감시 대상만 CPU, 프로세스, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), 노드로 달라질 뿐 본질은 동일하다.

📢 섹션 요약 비유: 하드웨어 워치독은 건물 전체 전기를 내리는 차단기이고, 소프트웨어 워치독은 층별 분전반 차단기이며, 플랫폼 헬스체크는 관리실에서 특정 호실만 비워 새 입주자를 들이는 조치에 가깝다. 어디까지 끊을지에 따라 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 범위와 부작용이 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 중요한 판단은 [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)과 갱신 지점을 실제 작업 주기와 맞추는 것이다. 예를 들어 제어 루프가 평소 20ms, 최악 80ms 안에 끝난다면 워치독 [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)을 30ms로 두는 것은 위험하고, 5초로 두는 것은 너무 느리다. 일반적으로는 정상 최악 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)에 통신 지터와 일시적 부하를 더한 뒤, 시스템이 멈춘 채 버텨도 되는 최대 시간을 넘지 않도록 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)한다.

### 설계 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. **갱신 기준**: 단순 타이머 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)가 아니라 실제 업무 완료 후에 갱신하는가?
2. <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/">타임아웃</a> 여유</strong>: 최악의 정상 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), [가비지 컬렉션](/studynote/02_operating_system/06_memory_management/380_garbage_collection/), 플래시 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 통신 재시도 시간을 반영했는가?
3. **리셋 원인 기록**: 부팅 후 워치독 리셋 여부를 진단 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 남기는가?
4. <strong><a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a> 계층 분리</strong>: 프로세스 재시작으로 충분한지, 보드 리셋이 필요한지 단계별 정책이 있는가?
5. **윈도우 모드 필요성**: 폭주 루프까지 잡아야 하는 안전 시스템인가?

### 대표 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 가장 높은 우선순위 [인터럽트](/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/)에서 무조건 워치독을 갱신하는 설계
- [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장이나 액추에이터 정지 절차 없이 즉시 리셋해 상태 불일치를 키우는 설계
- 장애 원인 분석 장치 없이 재부팅만 반복하여 재현 불가능한 오류를 만드는 설계
- 정상적으로 오래 걸리는 작업을 고려하지 않아 멀쩡한 시스템을 오진하는 설계

실제 운영에서는 단계적 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 효과적이다. 먼저 프로세스 재시작, 그다음 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 재기동, 마지막에 보드 리셋으로 escalation을 두면 불필요한 전체 초기화를 줄일 수 있다. 그러나 사람 생명이나 설비 안전이 걸린 시스템에서는 복잡한 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)보다 확실한 리셋이 더 우선일 수 있다. 기술사 관점에서는 "[가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 손실"과 "안전 확보" 중 무엇을 우선해야 하는지 도메인별로 판단해야 한다.

📢 섹션 요약 비유: 워치독 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)은 응급실 자동 제세동기처럼 너무 예민해도 문제이고 너무 둔해도 문제다. 정상 환자를 충격하면 사고가 나고, 실제 심정지 환자를 늦게 살리면 치명적이므로 기준과 타이밍을 정확히 맞춰야 한다.

---

## Ⅴ. 기대효과 및 결론

워치독 타이머의 가장 큰 효과는 장애를 "영구 정지"가 아니라 "제한된 시간의 중단"으로 바꾼다는 점이다. 이를 통해 무인 장비의 자율 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 능력이 높아지고, 운영자의 출동 비용과 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 중단 시간이 줄어든다. 특히 재부팅만으로 상당수 일시적 오류가 해소되는 시스템에서는 매우 비용 대비 효과가 크다.

하지만 워치독은 근본 원인 제거 장치가 아니다. [메모리 누수](/studynote/02_operating_system/10_security/612_memory_leak_detection/), [경쟁 조건](/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/), 전원 품질 문제, 드라이버 결함이 계속 남아 있으면 시스템은 단지 더 빨리 반복 재부팅할 뿐이다. 따라서 워치독은 [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) ([Error-Correcting Code](/studynote/01_computer_architecture/13_reliability_power_management/463_ecc_memory/)) 메모리, 오류 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), [이중화](/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/), 전원 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 설계와 함께 써야 진짜 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)이 올라간다.

앞으로는 안전 아일랜드(Safety Island)나 관리 코어가 메인 코어를 감시하는 구조가 더 중요해질 것이다. 자율주행, 로봇, 엣지 인공지능인 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) ([Artificial Intelligence](/studynote/10_ai/01_ai_basics/001_artificial_intelligence/)) 장비처럼 소프트웨어 규모가 커질수록 "멈춤을 감지하고 안전하게 초기화하는 마지막 하드웨어"의 가치가 오히려 커진다. 따라서 워치독은 단순 타이머가 아니라, 복잡한 시스템이 스스로 무너짐을 통제하는 최소한의 헌법으로 기억하는 것이 맞다.

📢 섹션 요약 비유: 워치독은 넘어질 때 무릎을 완전히 부러뜨리지 않게 막아 주는 보호대와 같다. 넘어짐 자체를 없애지는 못하지만, 다시 일어설 수 있을 정도로 피해를 제한해 준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [페일 세이프](/studynote/01_computer_architecture/13_reliability_power_management/459_fail_safe/) ([Fail-Safe](/studynote/01_computer_architecture/13_reliability_power_management/459_fail_safe/)) | 잘못된 동작을 계속 두느니 강제 정지·리셋으로 안전 상태를 확보하는 철학 |
| [MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) (Mean Time To Repair) | 워치독이 자동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 통해 직접 줄이는 운영 지표 |
| 하트비트 (Heartbeat) | 시간 내 응답 여부로 생존을 판단하는 상위 계층의 동일 패턴 |
| 윈도우 워치독 (Windowed Watchdog) | 늦은 응답뿐 아니라 비정상적으로 빠른 반복까지 감시하는 확장형 워치독 |
| 리셋 원인 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) | 재부팅 후 워치독 발동 여부를 추적해 원인 분석을 돕는 보조 장치 |

### 📈 관련 키워드 및 발전 흐름도

```text
단순 타임아웃 감시
    |
    v
워치독 타이머 (Watchdog Timer)
    |
    +---> 윈도우 워치독 (Windowed Watchdog)
    |
    +---> 리셋 원인 기록 · 프리타임아웃 인터럽트
    |
    v
보드 수준 자율 복구 · MTTR 단축
    |
    v
소프트웨어 워치독 · 하트비트 · Liveness Probe
    |
    v
안전 아일랜드 기반 자율주행 · 산업 제어 감시 구조
```

이 흐름은 단순한 시간 초과 검출이 시스템 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 헬스체크, 그리고 안전 제어 아키텍처로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 워치독은 컴퓨터 옆에서 "잘 움직이고 있니?"를 계속 확인하는 알람시계예요.
2. 컴퓨터가 제때 "응, 잘하고 있어!"라고 말하면 괜찮지만, 너무 오래 대답이 없으면 알람이 크게 울리며 다시 시작하게 해요.
3. 그래서 멀리 있는 기계도 완전히 잠들어 버리지 않고, 스스로 다시 일어날 기회를 얻어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 462 / 803

<- **이전**: [460. 페일 소프트 (Fail-Soft)](/studynote/01_computer_architecture/13_reliability_power_management/460_fail_soft/)
**다음**: [462. 소프트 에러 (Soft Error)와 하드 에러 (Hard Error)](/studynote/01_computer_architecture/13_reliability_power_management/462_soft_error_hard_error/) ->

---
