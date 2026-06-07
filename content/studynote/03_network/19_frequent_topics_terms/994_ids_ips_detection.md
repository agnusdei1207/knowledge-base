---
title: "Ids Ips Detection"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 994
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/) / [IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 탐지 차단율은 빈출 주제와 용어에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/) / [IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 탐지 차단율을 이해하면 구분 명확성과 설명력 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/) ([Intrusion Detection System](/studynote/09_security/uncategorized/1090_ids_ips_intrusion_detection_prevention_false_positive/))는 네트워크나 시스템의 트래픽을 모니터링하여 악의적인 활동이나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반을 탐지하고 경고하는 시스템이며, [IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) (Intrusion Prevention System)는 탐지를 넘어 해당 위협 트래픽을 실시간으로 차단(Drop)하는 능동형 보안 솔루션이다. 이 두 시스템의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 정상과 비정상 트래픽을 얼마나 정확하게 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하는가, 즉 탐지 및 차단율로 평가된다.

- **필요성**: 현대 네트워크 환경에서는 하루에도 수백만 건 이상의 사이버 공격과 정상 트래픽이 혼재되어 유입된다. [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)([Firewall](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))이 포트와 IP 기반의 1차 관문 역할을 한다면, IDS와 IPS는 패킷의 페이로드(Payload)를 심층 분석하는 DPI (Deep Packet Inspection)를 수행하여 진화하는 애플리케이션 계층 공격을 막아내야 한다. 이때 탐지 차단율이 낮아 공격을 통과시키거나(미탐), 과도하게 민감하여 정상 고객의 접속을 막아버리면(오탐) 기업에 치명적인 금전적/신뢰적 손실이 발생하므로 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 정량적 평가와 튜닝이 필수적이다.

- **💡 비유**: 마치 공항의 보안 검색대와 같습니다. 경고음만 울리고 요원에게 알려주는 시스템이 IDS라면, 위험물을 엑스레이로 발견 즉시 컨베이어 벨트를 멈추고 압수하는 자동화 게이트가 IPS입니다.

- **등장 배경 및 발전 과정**:
  [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 네트워크 방어는 IP와 Port를 필터링하는 L3/L4 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)에 의존했으나, [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)([Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 80) 등 허용된 포트를 타고 들어오는 SQL 인젝션이나 [버퍼 오버플로우](/studynote/02_operating_system/10_security/591_buffer_overflow/) 공격을 막을 수 없었다. 이를 해결하기 위해 패킷의 내용을 검사하는 IDS가 등장했다. 그러나 IDS는 경고만 발생할 뿐 실제 공격 패킷은 이미 대상 서버에 도달해버리는 물리적 한계가 존재했다. 이러한 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 방어의 한계를 극복하기 위해 네트워크 트래픽 흐름 자체에 개입하여 선제적으로 패킷을 폐기하는 인라인(Inline) 방식의 IPS가 필수적인 솔루션으로 자리 잡게 되었다.

이러한 역사적 배경을 이해하기 위해서는 IDS와 IPS의 근본적인 네트워크 위치와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름의 차이를 파악해야 한다.

```text
  +---------------------------------------------------------+
  |              IDS vs IPS 네트워크 위치 및 데이터 흐름            |
  +---------------------------------------------------------+
  |                                                         |
  |  [미러링 기반 IDS (Intrusion Detection System)]           |
  |                                                         |
  |  Internet --- [Router] --+-- [Switch] --- 내부 서버        |
  |                          |    (SPAN/Mirror)             |
  |                          +---> [IDS] (경고만 발생, 차단 불가) |
  |                                                         |
  |  [인라인 기반 IPS (Intrusion Prevention System)]          |
  |                                                         |
  |  Internet --- [Router] ---> [IPS] ---> [Switch] --- 내부 서버|
  |                          (패킷 심사 및 차단)               |
  |                                                         |
  |  * IDS는 트래픽의 복사본을 분석하므로 네트워크 지연이 없음         |
  |  * IPS는 실제 경로에 위치하므로 고성능 처리 병목 관리 필수          |
  +---------------------------------------------------------+
```

**[다이어그램 해설]** 이 도식은 IDS와 IPS의 아키텍처적 근본 차이를 보여준다. IDS는 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)의 SPAN (Switched [Port](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) Analyzer) 기능이나 광 탭(Tap)을 통해 패킷의 '복사본'을 받아 분석한다. 따라서 장애가 나도 전체 네트워크 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)에는 영향을 주지 않지만, 이미 서버로 향하는 원본 패킷을 물리적으로 막을 수 없다. 반면 IPS는 라우터와 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 사이의 주 경로(Inline)에 위치한다. IPS가 패킷을 허용해야만 내부 [스위치](/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)로 전달되므로 공격을 완벽히 차단할 수 있지만, [IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 자체가 병목 지점(Choke Point)이 되거나 장애 발생 시 전체 네트워크가 단절되는 [단일 장애점](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/studynote/01_computer_architecture/13_reliability_power_management/454_spof/), Single Point of Failure)이 될 수 있다. 따라서 [IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 도입 시에는 Fail-Open(장애 시 트래픽 무조건 통과) 설계와 하드웨어 바이패스(Bypass) 기능이 필수적으로 요구된다.

- **📢 섹션 요약 비유**: 수질 검사소가 강물 일부를 떠서 오염을 사후에 알리는 것([IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/))과 정수기가 수도관 중간에 설치되어 오염 물질을 직접 걸러내는 것([IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/))의 차이와 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **트래픽 수집기 (Packet Sniffer)** | 네트워크 패킷 수집 및 캡처 | Promiscuous 모드로 모든 프레임 복사 | Libpcap, [DPDK](/studynote/01_computer_architecture/15_advanced_topics/671_dpdk/) ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Plane Development Kit) | 도로의 [CCTV](/studynote/09_security/18_iot_ot_physical/933_cctv/) |
| **전처리기 (Preprocessor)** | 패킷 디코딩, 파편화 재조합, [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) | IP [Fragmentation](/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/) 재조립, 인코딩 해제 | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [Stream](/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) Reassembly | 퍼즐 맞추기 및 번역 |
| <strong>탐지 엔진 (<a href="/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/">Detection</a> 엔진)</strong> | 분석 모델 및 룰과 대조하여 위협 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 패턴 매칭, 통계적 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [Snort](/studynote/03_network/13_network_security_basics/694_snort_suricata_misuse_anomaly_detection/) 규칙, [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) 분류기 | 지명수배 전단지 대조 |
| **시그니처/룰 DB (Rule Base)** | 알려진 공격 패턴 저장소 | [CVE](/studynote/09_security/04_endpoint_security/409_cve_lifecycle/) 취약점 기반 [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 시퀀스 매칭 | YARA, 정규표현식 ([Regex](/studynote/08_algorithm_stats/05_string/104_regex/)) | 범죄자 지문 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) |
| <strong>대응 <a href="/studynote/04_software_engineering/04_testing_quality/192_module_independence/">모듈</a> (Response <a href="/studynote/04_software_engineering/04_testing_quality/192_module_independence/">Module</a>)</strong> | 탐지 결과에 따른 경보, 로깅, [세션](/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 차단 | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) RST 전송, [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) [ACL](/studynote/02_operating_system/09_file_system/549_acl_access_control_list/) 동적 연동 | [SIEM](/studynote/09_security/13_secops_ir_forensics/624_siem/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 전송, [SNMP Trap](/studynote/03_network/10_application_layer_dns_mgmt/534_snmp_trap_inform/) | 비상벨 작동 및 출입문 차단 |

### 탐지 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 4가지 상태 ([혼동 행렬](/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/))

보안 시스템의 탐지 정확성을 평가할 때는 단순히 "몇 개를 잡았는가"가 아니라, 실제 상태와 시스템의 판단이 엇갈리는 4가지 교차 영역을 엄밀히 측정해야 한다. 이를 [혼동 행렬](/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/) ([Confusion Matrix](/studynote/14_data_engineering/02_math_mining/089_confusion_matrix_tp_fp_fn_tn/))이라고 한다.

```text
  +----------------------------------------------------------+
  |             혼동 행렬 (Confusion Matrix) 및 성능 지표         |
  +----------------------------------------------------------+
  |                                                          |
  |                      [시스템의 예측/판단]                    |
  |                  탐지함 (Positive)    통과시킴 (Negative)     |
  |                +------------------+------------------+   |
  |      실제 공격   | True Positive(TP)| False Negative(FN) |   |
  |  [실제  (True)   | (정상 탐지/차단)   | (미탐 - 보안 사고)   |   |
  |   상태]         +------------------+------------------+   |
  |      정상 트래픽 | False Positive(FP)| True Negative(TN)  |   |
  |       (False)  | (오탐 - 가용성 저하)| (정상 통과)         |   |
  |                +------------------+------------------+   |
  |                                                          |
  |  [핵심 수식]                                               |
  |  * 재현율(Recall) = TP / (TP + FN) : 실제 공격 중 탐지 비율  |
  |  * 정밀도(Precision) = TP / (TP + FP) : 탐지된 것 중 실제 공격|
  |  * FPR (오탐률) = FP / (FP + TN) : 정상 중 잘못 차단된 비율  |
  +----------------------------------------------------------+
```

**[다이어그램 해설]** 이 표는 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)과 보안 분석에서 가장 핵심이 되는 평가 모델이다. 'True/False'는 시스템의 판단이 맞았는지 틀렸는지를 의미하고, 'Positive/Negative'는 시스템이 공격이라고 판단하여 경고를 띄웠는지(Positive), 아니면 정상으로 보고 무시했는지(Negative)를 의미한다. 실무에서 가장 치명적인 것은 False Negative (미탐)와 False Positive (오탐)이다. FN은 실제 공격(True)을 시스템이 정상(Negative)으로 착각해 통과시킨 것이므로 시스템 침해 사고로 직결된다. FP는 정상 트래픽(False)을 시스템이 공격(Positive)으로 오해해 차단한 것으로, 합법적인 고객의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 이용을 막아버리는 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 장애를 유발한다. 따라서 보안 관리자는 [Precision](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)([정밀도](/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/))과 [Recall](/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/)([재현율](/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/))을 동시에 모니터링하여 탐지 룰을 지속적으로 튜닝해야 한다.

### 탐지 엔진의 수학적 매커니즘 (ROC 곡선과 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/))

침입 탐지는 본질적으로 확률적 판단의 연속이다. 시스템 내부적으로 특정 트래픽의 '위협 점수(Threat Score)'를 계산하고, [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)된 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)(Threshold)를 넘으면 공격으로 판단한다. 이 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 어떻게 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)하느냐에 따라 탐지율과 오탐률이 극적으로 변한다.

```text
  +----------------------------------------------------------+
  |            탐지 임계치(Threshold)에 따른 FP와 FN의 트레이드오프  |
  +----------------------------------------------------------+
  |                                                          |
  |  정상 트래픽 분포                 공격 트래픽 분포             |
  |        \                         /                       |
  |         \        [임계치 A]     /                        |
  |   #######\           |         /@@@@@@@                  |
  |  #########\          |        /@@@@@@@@@                 |
  | ###########\   [FN]  |  [FP] /@@@@@@@@@@@                |
  | ------------\--------+------/------------- 위협 점수      |
  |               \      |     /                             |
  |                \     |    /                              |
  |                  겹치는 구간 (판단 모호)                     |
  |                                                          |
  |  * 임계치 A 이동:                                          |
  |    - 왼쪽으로 이동(민감도 증가): FN(미탐) 감소, FP(오탐) 급증  |
  |    - 오른쪽으로 이동(보수적):   FP(오탐) 감소, FN(미탐) 급증  |
  +----------------------------------------------------------+
```

**[다이어그램 해설]** 이 그래프는 정상 트래픽과 공격 트래픽의 특징(위협 점수)이 완벽히 분리되지 않고 일부분 겹쳐 있음(Overlapping)을 시각적으로 보여준다. 공격자들은 의도적으로 정상 트래픽과 유사하게 패킷을 위장(Evasion)하므로 이 겹치는 구간은 필연적으로 발생한다. 보안 관리자가 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)하는 '[임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)'는 이 x축 위의 수직선이다. [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 왼쪽으로 당기면 아주 작은 의심만 있어도 족족 잡아내므로 실제 공격을 놓치는 FN(미탐)은 줄어들지만, 선 오른쪽에 속하게 되는 억울한 정상 트래픽 즉 [FP](/studynote/12_it_management/05_security_compliance/293_fp_function_point/)(오탐)가 폭발적으로 증가한다. 반대로 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 오른쪽으로 밀면 오탐은 줄지만 정교한 공격이 그대로 통과하게 된다. 실무에서는 이 트레이드오프를 수치화한 ROC (Receiver Operating Characteristic) 곡선의 밑면적(AUC, Area Under Curve)을 넓히기 위해 탐지 모델 자체의 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)력을 고도화해야 한다.

- **📢 섹션 요약 비유**: 양치기 소년이 늑대를 경계할 때, 바스락거리는 소리만 나도 소리치면(오탐 증가) 마을 사람들의 피로도가 높아지고, 늑대가 확실히 보일 때만 소리치면(미탐 증가) 양을 잃을 위험이 커지는 것과 같은 딜레마입니다.

---

## Ⅲ. 비교 및 연결

| 비교 항목 | 오용 탐지 (시그니처 기반) | [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) (행위 기반) |
|:---|:---|:---|
| **기본 원리** | 알려진 공격 패턴(시그니처) [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/)와 1:1 매칭 | 정상적인 네트워크 [베이스라인](/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)(프로필)을 벗어나는 행위 탐지 |
| <strong>장점 (<a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>)</strong> | 오탐률([FP](/studynote/12_it_management/05_security_compliance/293_fp_function_point/))이 매우 낮음. 매칭 속도가 빠르고 분석이 명확함 | [제로데이](/studynote/09_security/15_malware_attack_vectors/761_zero_day/)([Zero-Day](/studynote/02_operating_system/10_security/597_zero_day_exploit/)) 공격 등 알려지지 않은 신종 공격 방어 가능 |
| **단점 (한계)** | 미탐률(FN) 위험. 시그니처에 없는 새로운 변종 공격은 탐지 불가 | 오탐률([FP](/studynote/12_it_management/05_security_compliance/293_fp_function_point/))이 상대적으로 높음. [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 학습 기간([Training](/studynote/04_software_engineering/09_cloud_native_ai_architecture/588_mlops_pipeline_automation/)) 필요 |
| **실무 적용** | [Snort](/studynote/03_network/13_network_security_basics/694_snort_suricata_misuse_anomaly_detection/) 룰을 활용한 명확한 SQLi, [XSS](/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 등 대중적 공격 즉각 차단 | ML/[AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델을 이용한 비정상적인 트래픽 폭증, C&C 서버 통신 감지 |

최근의 보안 장비는 단일 방식을 고집하지 않고, 1차적으로 고속 시그니처 매칭을 거친 후 2차적으로 샌드박스와 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [이상 탐지](/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/)를 수행하는 융합 아키텍처를 채택하여 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 탐지율의 균형을 맞춘다.

### 과목 융합 관점

- <strong><a href="/studynote/10_ai/03_llm_nlp/231_ai_turing_test/">인공지능</a> (<a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> &amp; Machine <a href="/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/">Learning</a>)</strong>: 기존의 정규표현식 기반 룰셋은 유지보수에 한계가 명확하다. 최근에는 [랜덤 포레스트](/studynote/06_ict_convergence/05_data_science/353_random_forest/)([Random Forest](/studynote/06_ict_convergence/05_data_science/353_random_forest/))나 [LSTM](/studynote/10_ai/04_ai_ops_ethics/292_lstm/) ([Long Short-Term Memory](/studynote/10_ai/04_ai_ops_ethics/292_lstm/)) 딥러닝 모델을 활용해 시계열 네트워크 플로우 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 분석함으로써, 기존 시그니처로는 잡지 못하는 Slow read/write DDoS 공격 등을 높은 [재현율](/studynote/14_data_engineering/02_math_mining/092_recall_sensitivity_hit_rate/)([Recall](/studynote/10_ai/03_llm_nlp/254_recall_sensitivity/))로 탐지하는 추세다.
- <strong>클라우드 아키텍처 (<a href="/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/">Cloud Computing</a>)</strong>: 퍼블릭 클라우드에서는 물리적인 인라인 [IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 장비를 구성하기 어렵다. 이에 따라 AWS Network Firewall이나 Azure [Firewall](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) IDPS처럼 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 형태로 [IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/)/IPS가 제공되며, 트래픽을 GWLB (Gateway [Load Balancer](/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/))를 통해 가상 어플라이언스로 라우팅하여 검사하는 [서비스 체이닝](/studynote/03_network/17_sdn_nfv/872_service_chaining_sfc_vnf_traffic_steering/)([Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [Chaining](/studynote/12_it_management/03_ea_isp/887_chaining/)) 구조가 활용된다.

- **📢 섹션 요약 비유**: 지명수배자의 얼굴(시그니처)만 보고 잡는 경찰과, 평소와 다르게 지나치게 땀을 흘리거나 눈치를 보는 행동(행위 기반)을 포착해 불심검문하는 경찰이 함께 순찰하는 것과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- **상황**: 블랙 프라이데이 등 대규모 할인 행사 시, 평소보다 10배 이상의 트래픽이 유입된다. 이때 IPS가 평소의 행위 기반([Anomaly](/studynote/05_database/04_transactions_concurrency/530_anomaly/)) [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)나 과도하게 빡빡한 시그니처를 유지하고 있다면, 정상 고객들의 대량 접속 시도를 DDoS나 비정상 접근으로 간주하여 [FP](/studynote/12_it_management/05_security_compliance/293_fp_function_point/)(오탐)가 폭증하게 된다.
- **의사결정**:
  1. <strong><a href="/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/">임계치</a> 완화 및 프로파일 재학습</strong>: 이벤트 시작 전 예상되는 트래픽 패턴으로 시스템을 사전 학습시켜 정상 [베이스라인](/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/)을 높인다.
  2. <strong>Fail-Open <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 점검</strong>: [IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 장비의 CPU나 메모리가 병목에 도달했을 때 패킷 처리가 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)되어 전체 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 다운되는 것을 막기 위해, 검사를 포기하고 트래픽을 통과시키는 하드웨어 바이패스를 활성화한다. (보안보다 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)이 우선되는 시나리오)
  3. **시그니처 최적화 (Tuning)**: 자사에 존재하지 않는 취약점(예: Linux 환경에서 IIS 서버 취약점 룰)이나 오래된 레거시 룰셋을 비활성화하여 검사 엔진의 부하를 줄인다.

### 도입 시 의사결정 플로우

IPS와 IDS를 어디에, 어떻게 배치할지 결정하는 것은 비즈니스의 성격에 따라 극명하게 갈린다.

```text
  +-------------------------------------------------------------------+
  |             IDS/IPS 배치 및 임계치 설정 실무 의사결정 트리            |
  +-------------------------------------------------------------------+
  |                                                                   |
  |      [비즈니스의 최우선 가치는 무엇인가?]                             |
  |                |                                                  |
  |                v                                                  |
  |      가용성과 서비스 연속성 (예: 포털, 이커머스)                      |
  |          +- [배치] 미러링 기반 IDS 운영 또는 보수적 차단 IPS 구성       |
  |          +- [정책] FP(오탐) 최소화 위주 튜닝, 경고 위주 모니터링        |
  |                                                                   |
  |                v                                                  |
  |      기밀성과 무결성 (예: 금융 망, 국방 인프라, 망분리 내부망)           |
  |          +- [배치] 인라인 기반 IPS 및 망 연계 구간 필수 검사 적용       |
  |          +- [정책] FN(미탐) 최소화, 의심스러우면 차단(Zero Trust)     |
  |                                                                   |
  |   * 기술사적 핵심 판단: 방어 장비의 도입보다 '지속적인 룰 튜닝과        |
  |     예외 처리 프로세스(Exception Handling)' 확립이 더 중요하다.        |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 의사결정 트리는 보안 장비의 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)이 단순히 기술적인 문제가 아니라 비즈니스 [위험 수용](/studynote/09_security/01_intro_principles/037_risk_acceptance/) 모델([Risk](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) Appetite)과 직결됨을 보여준다. 이커머스 쇼핑몰에서 1명의 정상 고객 결제를 오탐으로 막아버리면 즉각적인 매출 손실과 브랜드 이미지 하락으로 이어진다. 따라서 차단(Prevention)에는 매우 보수적으로 접근해야 한다. 반면, 폐쇄망이나 방산 업체 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) 앞단에서는 단 1개의 공격 패킷(미탐)이라도 유입되면 국가적 재난이나 치명적 기밀 유출이 발생하므로 다소간의 업무 불편(오탐)을 감수하더라도 공격적으로 차단 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 한다. 실무에서는 이 양극단 사이에서 '모니터링 모드'로 한 달 이상 운영하며 오탐을 솎아내는 과정이 필수적이다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **기본 룰셋(Default Rule) 방치**: 제조사에서 제공하는 수만 개의 시그니처를 환경에 맞춘 튜닝 없이 전체 On(활성화) 상태로 운영하는 것. 이는 불필요한 탐지로 인한 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하와 쏟아지는 오탐 경고(Alert Fatigue)를 유발하여 보안 관제 요원들이 진짜 위협을 무시하게 만드는 최악의 결과를 낳는다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 맞춤 양복을 사놓고 가봉(튜닝)을 하지 않으면 입을 수 없는 것처럼, 강력한 IPS를 도입하고도 자사 환경에 맞게 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 조율하지 않으면 오히려 업무의 숨통을 조이는 족쇄가 됩니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 최적화 전 | 최적화 후 (지속적 룰 튜닝 적용) | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 일일 오탐 이벤트 수만 건 발생 | 오탐 이벤트 90% 이상 감소 | 관제 요원의 대응 리드타임([MTTR](/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/)) 대폭 단축 |
| **정량** | CPU 사용률 80% 상회, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 증가 | 불필요한 시그니처 비활성화로 40% 유지 | 검사 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)) 및 네트워크 속도 개선 |
| **정성** | 보안 경고 불감증 발생 | 유효한 고위험 알람에 집중 | 진짜 침해 시도에 대한 가시성 및 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 진압력 강화 |

### 미래 전망
- **복호화 검사의 한계와 극복**: 인터넷 트래픽의 90% 이상이 [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 기반으로 암호화되면서, 기존 페이로드 검사 방식의 [IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/)/IPS는 암호화된 트래픽을 볼 수 없는 '장님'이 되어가고 있다. 향후에는 인증서를 연동한 SSL/[TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 가시성 장비 전진 배치나, 암호화된 상태 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 자체의 패턴을 AI로 분석하는 ETA (Encrypted Traffic Analytics) 기술이 핵심 경쟁력이 될 것이다.
- <strong><a href="/studynote/03_network/14_network_security_threats/745_soar_security_orchestration_automation_response/">SOAR</a> 연동</strong>: 단일 장비의 탐지에 그치지 않고, [EDR](/studynote/09_security/04_endpoint_security/325_edr/) (Endpoint [Detection](/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/) and Response)과 연동하여 침해 단말을 자동으로 네트워크에서 격리하는 [SOAR](/studynote/03_network/14_network_security_threats/745_soar_security_orchestration_automation_response/) ([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) [Orchestration](/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/), Automation and Response) [플레이북](/studynote/09_security/13_secops_ir_forensics/637_playbook/) 기반의 자율 방어 체계로 진화하고 있다.

### 참고 표준
- <strong>NIST <a href="/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/">SP</a> 800-94</strong>: 침입 탐지 및 방어 시스템 가이드
- <strong><a href="/studynote/09_security/04_endpoint_security/407_cvss_scoring/">CVSS</a> (Common Vulnerability Scoring System)</strong>: 취약점 위험도 평가 표준 (시그니처 우선순위 산정에 활용)

보안은 완벽한 차단이라는 환상에서 벗어나, 위협을 얼마나 빠르고 정확하게 인지하여 [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 훼손하지 않는 선에서 통제할 것인가의 문제다. 탐지율과 오탐률 사이의 수학적 줄다리기를 비즈니스 요구에 맞게 조율하는 아키텍트의 통찰이 요구된다.

- **📢 섹션 요약 비유**: 기술의 발전으로 탐지 레이더([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))는 점점 예민해지지만, 결국 그 레이더 화면을 보고 미사일을 요격할지 말지 결정하는 교전 수칙([임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 튜닝 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/))을 다듬는 것이 전쟁의 승패를 가릅니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 정의 (Definition) | 용어의 시작점을 분명하게 만든다. |
| 비교 (Comparison) | 헷갈리는 개념의 경계를 드러낸다. |
| [네트워크 슬라이싱](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: WAF]
    |
    v
[현재 개념: IDS / IPS 탐지 차단율]
    |
    +---> [확장 A: 네트워크 슬라이싱]
    +---> [확장 B: 컨텍스트 기반 용어 해석]
```

[IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/) / [IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 탐지 차단율는 WAF에서 출발해 현재 메커니즘을 정교화하고, 이후 [네트워크 슬라이싱](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)와 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 정보의 바다를 지키는 해적 탐지기([IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/)/[IPS](/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/))가 있어요. 해적(해킹 공격)을 얼마나 잘 찾아내는지, 일반 어선(정상 사용자)을 억울하게 공격하지 않는지가 탐지/차단율의 핵심이에요.
2. 만약 탐지기가 너무 예민해서 낚싯대만 봐도 대포를 쏜다면 진짜 어부들이 고기를 잡을 수 없게 되고(오탐), 반대로 너무 둔감해서 대포를 숨긴 해적을 못 본 척하면 마을이 약탈당해요(미탐).
3. 그래서 똑똑한 보안 전문가들은 이 탐지기를 아주 정교하게 조절해서, 진짜 해적만 쏙쏙 골라내 바다의 평화를 유지한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 1115 / 1120

<- **이전**: [993. WAF (웹 방화벽)](/studynote/03_network/19_frequent_topics_terms/993_waf_web_application_firewall/)
**다음**: [995. 네트워크 슬라이싱](/studynote/03_network/19_frequent_topics_terms/995_network_slicing/) ->

---
