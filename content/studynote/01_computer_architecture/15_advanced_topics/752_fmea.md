+++
title = "752. FMEA (Failure Mode and Effects Analysis)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FMEA (Failure Mode and Effects Analysis)는 시스템의 각 기능이 **어떻게 망가질 수 있는지(Failure Mode), 그 결과 어떤 영향이 번지는지(Effects)** 를 구조적으로 나열하고 우선순위를 매기는 예방적 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 분석이다.
> 2. **가치**: 문제를 출시 후 장애로 만나는 대신 설계 단계에서 미리 계산하게 만들어, 어디에 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)·감시·[보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 회로를 먼저 넣어야 할지 결정하도록 돕는다.
> 3. **판단 포인트**: 고전적인 RPN ([Risk](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) Priority Number) 점수는 유용한 시작점이지만, <strong>심각도와 공통 원인 장애는 별도 판단</strong>이 필요하며, FMEA는 반드시 설계 변경과 후속 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)으로 이어져야 한다.

---

## Ⅰ. 개요 및 필요성

FMEA (Failure Mode and Effects Analysis)는 제품이나 시스템이 수행해야 할 기능을 기준으로, <strong>어떤 방식으로 실패할 수 있는지와 그 파급 효과를 사전에 분석</strong>하는 기법이다. 고장이 난 뒤 원인을 추적하는 사후 분석이 아니라, 설계 도면과 요구사항 단계에서 "무엇이 잘못될 수 있는가"를 먼저 묻는 사전 분석이라는 점이 중요하다. 그래서 항공우주, 자동차, 서버, 전력, 의료기기처럼 실패 비용이 큰 분야에서 널리 쓰인다.

이 기법이 필요한 이유는 복잡한 시스템일수록 개별 부품은 멀쩡해 보여도 조합에서 위험이 발생하기 때문이다. 예를 들어 이중 전원 장치를 넣었더라도 두 전원이 같은 전원분배장치에 매달려 있으면 실제로는 공통 원인 장애가 남는다. FMEA는 이런 숨은 약점을 부품 단위가 아니라 <strong>기능과 영향의 연결</strong>로 보게 만든다.

또한 FMEA의 강점은 막연한 불안을 <strong>행동 가능한 목록</strong>으로 바꾼다는 데 있다. "팬이 멈추면 과열된다", "센서가 침묵하면 잘못된 제어가 이어진다", "메모리 오류가 누적되면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 손상된다"처럼 고장 모드를 구체화하면, 설계자는 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/), 경보, 차단, 안전 정지 중 무엇이 필요한지 판단할 수 있다.

- **📢 섹션 요약 비유**: FMEA는 소풍 가기 전에 "비가 오면? 버스가 늦으면? 아이가 길을 잃으면?"을 하나씩 적어 보고 미리 준비물을 챙기는 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 회의와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

FMEA의 기본 흐름은 <strong>기능 정의 -> 고장 모드 <a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/">식별</a> -> 영향 분석 -> 원인 및 현재 통제 파악 -> 우선순위 평가 -> 개선 조치</strong>다. 여기서 많이 쓰는 지표가 <strong>RPN (<a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">Risk</a> Priority Number)</strong> 이며, 전통적으로 `RPN = Severity × Occurrence × Detection` 으로 계산한다. 즉 심각도 ([Severity](/knowledge-base/studynote/04_software_engineering/06_software_architecture/354_defect_severity_priority/)), 발생도 (Occurrence), 검출도 ([Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/))를 각각 점수화해 어떤 항목을 먼저 처리할지 정한다.

아래 그림은 FMEA가 부품 이름 나열이 아니라, <strong>기능에서 시작해 영향과 조치로 내려가는 <a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/143_structured_analysis_dfd_dd_minispec/">구조적 분석</a></strong>임을 보여 준다.

```text
+----------------------------------------------------------------------+
|                      FMEA reasoning pipeline                        |
+----------------------------------------------------------------------+
| Function                                                            |
|    |                                                                 |
|    v                                                                 |
| Failure mode                                                         |
|    |                                                                 |
|    v                                                                 |
| Local effect --> next higher effect --> system effect                  |
|    |                                                                 |
|    v                                                                 |
| Current controls / detectability                                     |
|    |                                                                 |
|    v                                                                 |
| Severity × Occurrence × Detection                                    |
|    |                                                                 |
|    v                                                                 |
| Action, owner, due date, re-score                                    |
+----------------------------------------------------------------------+
```

예를 들어 서버 플랫폼을 분석한다면 아래처럼 쓸 수 있다.

| 기능/항목 | 고장 모드 | 시스템 영향 | 현재 통제 | 우선 대응 |
| :--- | :--- | :--- | :--- | :--- |
| 냉각 팬 | 회전 정지 | 열 폭주, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하, 셧다운 | 회전 속도 센서, [과열 보호](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/748_otp/) (Over [Temperature](/knowledge-base/studynote/10_ai/05_data_science_ml/386_llm_temperature/) [Protection](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/), [OTP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/748_otp/)) | 팬 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/), 경보 강화 |
| 메모리 채널 | 다중 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 오류 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손상, 프로세스 중단 | 오류 정정 코드 (Error Correcting [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/)), 오류 검출/수정 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) ([Error Detection](/knowledge-base/studynote/02_operating_system/01_overview_architecture/040_error_detection/) and Correction, [EDAC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/718_edac/)) | 채널 분리, 고장 DIMM 격리 |
| 스토리지 컨트롤러 | [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 응답 정지 | 입출력 정지, [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 이중 컨트롤러, 감시 타이머 ([Watchdog Timer](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/461_watchdog_timer/)) | [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 자동 절체 |
| 전원 경로 | 공통 전원분배장치 ([Power Distribution Unit](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/651_server_rack_pdu/), PDU) 상실 | 전체 셧다운 | 이중 전원 공급 장치 ([Power](/knowledge-base/studynote/14_data_engineering/02_math_mining/069_type_1_2_error_statistical_power/) Supply Unit, PSU) | 전원 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 분리 |

다만 RPN은 만능이 아니다. 심각도 10이면서 발생 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이 낮은 항목과, 자주 발생하지만 영향이 작은 항목이 같은 RPN을 가질 수 있다. 그래서 최근 실무에서는 RPN과 함께 **심각도가 높은 항목의 별도 관리**, 또는 <strong>행동 우선순위 (Action Priority, <a href="/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/">AP</a>)</strong> 개념을 함께 적용한다. 즉 숫자는 우선순위를 돕는 도구일 뿐, 공학적 판단을 대체하지 못한다.

- **📢 섹션 요약 비유**: FMEA는 병원 응급실의 분류표와 같다. 열이 나는 환자, 크게 다친 환자, 숨쉬기 어려운 환자를 같은 줄에 세워 놓고 누가 먼저 처치받아야 하는지 기준을 세우는 과정이다.

---

## Ⅲ. 비교 및 연결

FMEA를 이해할 때 가장 자주 비교되는 것은 <strong>고장수목분석 (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/753_fta/">Fault Tree Analysis</a>, <a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/753_fta/">FTA</a>)</strong> 이다. FMEA는 아래에서 위로 올라가는 <strong>귀납적(<a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/403_bottom_up_integration/">Bottom-Up</a>)</strong> 분석이고, FTA는 "시스템 정지" 같은 최상위 사고에서 출발해 원인을 내려가는 <strong>연역적(<a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/402_top_down_integration/">Top-Down</a>)</strong> 분석이다. 둘은 경쟁 기법이 아니라 서로 다른 질문에 답한다.

| 기법 | 출발점 | 주된 질문 | 장점 |
| :--- | :--- | :--- | :--- |
| FMEA | 기능·부품 | 무엇이 어떤 방식으로 실패할 수 있는가 | 설계 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 우선순위화 |
| [FTA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/753_fta/) | 최상위 사고 | 이 사고는 어떤 조합으로 발생하는가 | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 구조·[확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 계산 |
| [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 블록도 ([Reliability](/knowledge-base/studynote/04_software_engineering/06_software_architecture/345_reliability_security/) Block Diagram, [RBD](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/754_rbd/)) | 시스템 경로 | 어떤 중복 구성이 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)를 높이는가 | [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 구조 파악 |
| [결함 주입 테스트](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/750_fault_injection_test/) | 실제 시스템 | [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 메커니즘이 실제로 작동하는가 | 실험 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |

FMEA는 또 **설계 FMEA (Design FMEA, DFMEA)** 와 <strong>공정 FMEA (<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/943_process/">Process</a> FMEA, PFMEA)</strong> 로 나뉜다. DFMEA는 제품 구조와 기능 자체의 위험을 보고, PFMEA는 제조·조립·시험 공정에서 생길 위험을 본다. 서버나 보드 설계에서는 DFMEA가 먼저 이루어지고, 양산 단계로 가면 PFMEA가 뒤따르는 경우가 많다.

현대 컴퓨터구조 관점에서 보면, [ECC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/), 핫스왑, 이중 전원, 감시 타이머, 안전 정지 로직 같은 많은 설계 요소가 사실상 FMEA의 결과물이다. 즉 "왜 여기에 예비 경로가 필요한가"에 대한 설득력을 주는 문서가 바로 FMEA다.

- **📢 섹션 요약 비유**: FMEA가 "이 부품이 아프면 어디가 문제일까"를 먼저 묻는 건강 검진표라면, FTA는 "왜 쓰러졌을까"를 역추적하는 사건 조사 보고서에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 FMEA가 형식 문서로 전락하는 순간 효과가 급격히 떨어진다. 중요한 것은 표를 채우는 것이 아니라, <strong>고위험 항목이 실제 설계 변경과 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 계획으로 이어지도록 만드는 것</strong>이다. 예를 들어 듀얼 PSU를 넣었다고 끝내지 말고, 공통 전원분배장치·공통 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)·공통 냉각 같은 공통 원인 장애까지 같이 봐야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 기능 경계를 명확히 나누고, 시스템·보드·[모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 수준을 혼동하지 않았는가?
2. 현장 장애 이력과 반품 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 발생도 점수에 반영되었는가?
3. 심각도 9~[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 항목은 RPN과 별개로 즉시 관리 대상에 올렸는가?
4. 개선 조치 후 재점수화와 실제 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 시험이 이루어지는가?
5. 하드웨어뿐 아니라 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/)·운영 절차·사람의 개입 오류까지 포함했는가?

### 피해야 할 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- **점수 만능주의**: RPN 숫자만 믿고 심각한 안전 항목을 뒤로 미루는 경우다.
- **공통 원인 장애 누락**: [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 부품이 같은 버그나 같은 전원 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 공유하면 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 효과가 줄어든다.
- **업데이트 없는 FMEA**: 설계 변경, 필드 장애, 테스트 결과가 나와도 표를 고치지 않으면 빠르게 구식 문서가 된다.

기술사 답안에서는 FMEA를 "고장 유형 나열표"로 적는 것보다, <strong>우선순위 결정 도구이자 설계·시험·운영을 연결하는 <a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> 관문</strong>으로 설명하는 것이 중요하다. 특히 FMEA -> 설계 보강 -> [결함 주입 테스트](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/750_fault_injection_test/) -> 현장 피드백 -> FMEA 갱신의 닫힌 루프를 보여 주면 더 설득력 있다.

- **📢 섹션 요약 비유**: FMEA는 시험 전 오답 노트를 만드는 과정과 같다. 틀릴 만한 문제를 미리 적어 놓아야, 정말 중요한 약점을 먼저 고칠 수 있다.

---

## Ⅴ. 기대효과 및 결론

FMEA를 잘 수행하면 설계 변경 비용이 가장 싼 시점에 위험을 제거할 수 있다. 실제 제품이 나온 뒤 발견되는 장애는 회수·정지·재배포·평판 손실까지 동반하지만, 설계 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에 찾은 문제는 센서 하나 추가, 전원 경로 분리, [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 로직 보강처럼 상대적으로 작은 비용으로 해결될 수 있다. 그래서 FMEA의 경제적 가치도 매우 크다.

물론 한계도 있다. 분석 품질이 팀의 경험과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 크게 좌우되고, 복잡한 상호작용이나 소프트웨어 동적 행위는 표만으로 완전히 포착하기 어렵다. 따라서 FMEA는 정적 문서 한 장으로 끝나는 것이 아니라, [FTA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/753_fta/), [RBD](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/754_rbd/), [결함 주입 테스트](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/750_fault_injection_test/), 운영 텔레메트리와 결합할 때 가장 강해진다.

결론적으로 FMEA는 "고장을 미리 상상하는 훈련"이다. 시스템이 커질수록 모든 위험을 제거할 수는 없지만, <strong>어떤 위험을 먼저 제거해야 하는지</strong>를 조직적으로 합의하게 만드는 힘이 있다. 그래서 FMEA는 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 문서가 아니라, <strong>설계 우선순위를 만드는 의사결정 도구</strong>로 기억하는 것이 맞다.

- **📢 섹션 요약 비유**: 여행 가방을 쌀 때 모든 물건을 다 넣을 수는 없지만, 비상약과 여권부터 챙기듯 FMEA는 가장 치명적인 위험부터 먼저 준비하게 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| RPN ([Risk](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) Priority Number) | 심각도·발생도·검출도를 곱해 우선순위를 정하는 전통적 FMEA 지표다. |
| DFMEA | 제품 구조와 기능 설계의 위험을 다루는 FMEA 형태다. |
| PFMEA | 제조·조립·검사 공정의 위험을 다루는 FMEA 형태다. |
| [FTA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/753_fta/) | FMEA 결과를 보완하며 최상위 사고의 원인 조합을 추적하는 분석 기법이다. |
| [RBD](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/754_rbd/) | [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/)와 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)/[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 구성이 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)에 미치는 구조를 표현하는 도구다. |
| [결함 주입 테스트](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/750_fault_injection_test/) | FMEA가 도출한 고위험 항목을 실제로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 후속 실험이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
요구사항 · 기능 정의
    |
    v
FMEA (Failure Mode and Effects Analysis)
: failure mode · effect · cause · control
    |
    v
우선순위 결정
: RPN / severity / action priority
    |
    +---> 설계 보강
    |     : ECC · redundancy · hot swap · watchdog
    |
    +---> 정량 분석 확장
    |     : FTA · RBD
    |
    +---> 실험 검증
          : fault injection test · burn-in test
```

### 👶 어린이를 위한 3줄 비유 설명

1. FMEA는 장난감을 만들기 전에 "바퀴가 빠지면? 건전지가 닳으면? 버튼이 안 눌리면?"을 미리 적어 보는 거예요.
2. 그리고 어떤 문제가 가장 위험한지 순서를 정해서 먼저 고쳐요.
3. 그래서 장난감이 나온 뒤에 큰 고장이 나는 일을 줄일 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 753 / 803

<- **이전**: [751. 카오스 엔지니어링 (Chaos 엔진ering) HW 모의](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/751_chaos_engineering/)
**다음**: [753. FTA (Fault Tree Analysis)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/753_fta/) ->

---
