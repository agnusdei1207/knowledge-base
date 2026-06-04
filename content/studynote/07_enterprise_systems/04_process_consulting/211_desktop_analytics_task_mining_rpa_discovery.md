---
title: "211. 데스크톱 애널리틱스 (Desktop Analytics) / 작업 마이닝 (Task Mining)"
date: "2026-05-08"
tags:
  - "studynote-enterprise"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데스크톱 애널리틱스 (Desktop Analytics)와 작업 마이닝 ([Task](/studynote/02_operating_system/02_process_thread/150_task/) Mining)은 개인용 컴퓨터 ([PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/), Personal Computer)에서 일어나는 클릭·입력·화면 전환을 수집·분석해, 서버 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 보이지 않는 반복 업무를 발견하는 기술이다.
> 2. **가치**: 자동화 대상을 인터뷰와 추정에 의존하지 않고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 발굴할 수 있어, 로보틱 프로세스 자동화 ([RPA](/studynote/12_it_management/01_governance_strategy/060_rpa_hyperautomation/), [Robotic Process Automation](/studynote/12_it_management/01_governance_strategy/060_rpa_hyperautomation/)) 후보 선정과 투자 타당성 분석의 정확도를 높인다.
> 3. **판단 포인트**: 생산성 분석과 감시의 경계가 얇기 때문에, [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹·동의·목적 제한을 설계하지 않으면 기술적 성과보다 조직 [저항](/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/)이 더 커질 수 있다.

---

## Ⅰ. 개요 및 필요성

작업 마이닝은 사용자의 데스크톱에서 발생하는 업무 행동 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 수집해 반복 작업 패턴을 찾아내는 분석 기법이다. [프로세스 마이닝](/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/) ([Process Mining](/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/))이 정보시스템 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 기반으로 전체 흐름을 본다면, 작업 마이닝은 그 흐름을 만들기 위해 사용자가 화면에서 어떤 세부 작업을 반복하는지 본다. 즉 서버 관점의 망원경이 아니라, 개인 작업 관점의 현미경에 가깝다.

이 기술이 필요한 이유는 많은 비효율이 서버 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 아니라 사람의 손동작 구간에서 발생하기 때문이다. 동일한 승인 버튼을 누르기 위해 엑셀 복사, 메일 열기, 포털 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)인, 값 대조 같은 세부 동작이 반복되더라도 중앙 시스템에는 마지막 결과만 남는 경우가 많다. 이 숨은 노동을 파악해야 자동화 후보와 개선 포인트를 정확히 찾을 수 있다.

- **📢 섹션 요약 비유**: 공장에서 트럭이 늦게 출발한 사실만 보면 어디서 시간이 샜는지 모른다. 작업 마이닝은 상자를 싣기 전에 누가 몇 번 들었다 놨다 했는지까지 가까이서 보는 카메라와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

작업 마이닝 아키텍처는 보통 데스크톱 에이전트, 수집 서버, 분석 엔진, 대시보드로 구성된다. 에이전트는 애플리케이션 전환, 키 입력 유형, 마우스 이벤트, 화면 캡처 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 수집한다. 분석 엔진은 광학 문자 인식 (OCR, Optical Character Recognition), 컴퓨터 비전, 자연어 처리 (NLP, Natural Language Processing)를 이용해 업무 맥락을 추정하고, 반복 시퀀스를 [군집화](/studynote/16_bigdata/05_analysis/105_clustering_analysis/)한다. 이후 대시보드는 빈도, 소요시간, 자동화 가능성, 절감 효과를 보여준다.

| 구성 요소 | 역할 | 실무 포인트 |
| :--- | :--- | :--- |
| 데스크톱 에이전트 | 화면·입력 이벤트 수집 | 수집 범위와 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 기준 필요 |
| 분석 엔진 | 반복 패턴 추출·[군집화](/studynote/16_bigdata/05_analysis/105_clustering_analysis/) | 노이즈 제거와 업무 맥락 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 정확도 중요 |
| [투자수익률](/studynote/07_enterprise_systems/01_strategy_governance/005_it_investment_metrics/) ([ROI](/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/), [Return on Investment](/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/)) 대시보드 | 자동화 가치 산정 | 시간 절감, 빈도, 오류율을 함께 평가 |
| 문서 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)기 | 설계 문서 초안 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 프로세스 설계 문서 (PDD, [Process](/studynote/12_it_management/05_security_compliance/943_process/) Design [Document](/studynote/14_data_engineering/01_infrastructure/037_document/)) 자동화 가능 |

아래 그림은 데스크톱 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 단순 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)가 아니라, 자동화 후보로 정제되는 과정을 보여준다.

```text
+----------------------------------------------------------------+
|              작업 마이닝 흐름: 데스크톱 행동에서 후보 발굴      |
+----------------------------------------------------------------+
| 사용자 PC 이벤트 --> 수집·마스킹 --> 패턴 군집화 --> ROI 평가      |
|  클릭·입력·창전환        |               |            |         |
|                          v               v            v         |
|                     개인정보 보호     반복 작업 묶음   RPA 후보 |
+----------------------------------------------------------------+
```

핵심 원리는 세 가지다. 첫째, 의미 없는 개인 활동과 실제 업무를 구분해야 한다. 둘째, 한 사람의 예외 행동보다 다수 사용자에게 반복되는 패턴을 찾는 것이 중요하다. 셋째, 발견된 작업은 자동화 가능성과 업무 중요도를 함께 따져야 한다. 많이 반복된다고 해서 모두 자동화 가치가 높은 것은 아니다.

- **📢 섹션 요약 비유**: 긴 영상을 통째로 보는 대신, 같은 장면만 묶어서 하이라이트로 편집하는 것과 같다. 그래야 어떤 동작이 정말 자주 반복되는지 한눈에 보인다.

---

## Ⅲ. 비교 및 연결

작업 마이닝은 데스크톱 애널리틱스, [프로세스 마이닝](/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/)과 함께 비교해야 경계가 선명해진다. 데스크톱 애널리틱스는 주로 애플리케이션 사용 현황, 생산성 지표, 작업 시간 분포를 보는 넓은 범주의 관찰이다. 작업 마이닝은 그중에서도 반복 시퀀스를 구조화해 자동화 후보를 뽑는 데 더 초점이 있다. [프로세스 마이닝](/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/)은 시스템 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반이라 범위는 넓지만 세부 손동작은 잘 보지 못한다.

| 항목 | 데스크톱 애널리틱스 | 작업 마이닝 | [프로세스 마이닝](/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/) |
| :--- | :--- | :--- | :--- |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 원천 | [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 사용 기록 전반 | PC의 반복 작업 시퀀스 | [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/) ([Enterprise Resource Planning](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/))·[CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) ([C고객](/studynote/12_it_management/01_governance_strategy/820_three_c_analysis/) [Relationship](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/))·업무시스템 이벤트 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) |
| 분석 초점 | 사용 현황·생산성 | 자동화 후보 발굴 | [전체 프로세스](/studynote/02_operating_system/06_memory_management/337_standard_vs_paging_swapping/) 흐름 |
| 산출물 | 앱 사용 리포트 | 반복 작업 묶음·PDD 초안 | [AS-IS](/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/) 흐름·병목·편차 |
| 대표 활용 | 업무 패턴 이해 | [RPA](/studynote/12_it_management/01_governance_strategy/060_rpa_hyperautomation/) 발굴 | 프로세스 개선·통제 |

실무에서는 이 셋을 연결해 써야 효과가 커진다. [프로세스 마이닝](/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/)이 "승인 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 2일"이라고 알려 주면, 작업 마이닝은 그 2일 중 실제로 어떤 데스크톱 작업이 시간을 잡아먹는지 보여 준다. 이렇게 거시 흐름과 미시 행동이 연결되면, 자동화 범위를 더 정확하게 정하고 개선 우선순위도 설계하기 쉬워진다.

- **📢 섹션 요약 비유**: [프로세스 마이닝](/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/)이 도시 전체 교통지도를 보여 준다면, 작업 마이닝은 한 교차로에서 사람들이 실제로 어떻게 움직이는지 슬로모션으로 보여 주는 장면과 같다. 둘을 합쳐야 막히는 이유가 잘 보인다.

---

## Ⅳ. 실무 적용 및 기술사 판단

작업 마이닝 도입에서 가장 중요한 판단은 "무엇을 보기 위해 수집하는가"다. 자동화 후보 발굴과 업무 개선이 목적이라면, 수집 범위, 보존 기간, [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 처리 기준을 명확히 해야 한다. 목적이 불분명하면 직원은 감시 도구로 받아들이고, 결과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)도 떨어진다.

### 적용 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 수집 대상 업무와 제외 대상 업무가 명확히 정의되어 있는가?
2. [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)·[민감정보](/studynote/09_security/16_data_privacy/782_sensitive_information/) 화면에 대한 [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 있는가?
3. 자동화 후보 선별 시 빈도뿐 아니라 예외율, 오류율, 규칙 명확성을 함께 보는가?
4. 결과를 [RPA](/studynote/12_it_management/01_governance_strategy/060_rpa_hyperautomation/), 프로세스 개선, 교육 중 어떤 조치로 연결할지 정해져 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 관리자 감시 목적으로 도구를 도입해 조직 불신을 키우는 경우
- 한 사람의 작업 녹화만 보고 전사 표준 업무라고 일반화하는 경우
- 수집은 많이 했지만 PDD나 자동화 설계로 이어지지 않는 경우

기술사 답안에서는 "자동화 발굴 도구"이면서 동시에 "프라이버시와 조직문화 고려가 필요한 기술"이라는 양면성을 함께 쓰면 좋다. 즉 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질과 윤리적 통제가 함께 설계되어야 실제 성과가 난다.

- **📢 섹션 요약 비유**: 공부 습관을 알려면 하루 종일 옆에서 쳐다보는 것이 아니라, 필요한 장면만 공정하게 기록하고 무엇을 고칠지 같이 이야기해야 한다. 관찰이 감시가 되면 협력이 깨진다.

---

## Ⅴ. 기대효과 및 결론

작업 마이닝의 기대효과는 자동화 후보 발굴 정확도 향상, 숨은 수작업 [식별](/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/), 표준 작업 문서 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시간 단축, 개선 과제 우선순위 명확화다. 특히 현업 인터뷰만으로는 놓치기 쉬운 반복 작업을 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 드러내기 때문에, RPA와 프로세스 개선의 투자 설득력이 높아진다. 또한 발견된 작업 시퀀스는 교육, 업무 표준화, 화면 개선에도 활용할 수 있다.

반면 수집 범위가 과도하거나 [마스](/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)킹이 약하면 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 이슈와 조직 [저항](/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/)이 빠르게 커진다. 또 화면상 행동만으로 업무의 진짜 맥락을 완전히 이해할 수는 없기 때문에, 인터뷰와 현장 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 반드시 병행해야 한다. 즉 작업 마이닝은 만능 감시가 아니라, 정교한 보조 관찰 도구로 써야 한다.

결론적으로 이 개념은 "직원 화면을 보는 기술"이 아니라, 자동화와 개선이 숨어 있는 세부 작업을 드러내는 분석 기술로 기억하는 것이 맞다. 망원경 같은 [프로세스 마이닝](/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/)과 함께 쓸 때 가장 큰 효과가 난다.

- **📢 섹션 요약 비유**: 큰 숲을 보는 지도와 나뭇잎을 보는 돋보기가 함께 있어야 숲을 제대로 돌볼 수 있다. 작업 마이닝은 그 돋보기 역할을 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 데스크톱 애널리틱스 (Desktop Analytics) | [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 사용 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 폭넓게 관찰하는 상위 범주 |
| 작업 마이닝 ([Task](/studynote/02_operating_system/02_process_thread/150_task/) Mining) | 반복 작업 시퀀스를 뽑아 자동화 후보로 구조화함 |
| [프로세스 마이닝](/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/) ([Process Mining](/studynote/12_it_management/03_ea_isp/913_process_mining_bpr_event_log_bottleneck_analysis/)) | 시스템 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 기반 거시 프로세스 가시화 기법 |
| PDD ([Process](/studynote/12_it_management/05_security_compliance/943_process/) Design [Document](/studynote/14_data_engineering/01_infrastructure/037_document/)) | [RPA](/studynote/12_it_management/01_governance_strategy/060_rpa_hyperautomation/) 설계를 위한 문서 산출물로 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 가능 |
| [RPA](/studynote/12_it_management/01_governance_strategy/060_rpa_hyperautomation/) ([Robotic Process Automation](/studynote/12_it_management/01_governance_strategy/060_rpa_hyperautomation/)) | 작업 마이닝 결과를 실제 자동화 구현으로 연결함 |

### 📈 관련 키워드 및 발전 흐름도

```text
데스크톱 이벤트 수집
        |
        v
데스크톱 애널리틱스 (Desktop Analytics)
        |
        v
작업 마이닝 (Task Mining)
        |
        +- 반복 패턴 군집화
        +- ROI 분석
        +- PDD 생성
        |
        v
RPA 발굴 · 프로세스 개선 · 하이퍼오토메이션
```

이 흐름도는 단순한 사용 통계가 자동화 후보 발굴과 문서화로 발전하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구가 숙제할 때 같은 칸을 자꾸 옮겨 적는다면, 그건 로봇이 대신할 수 있는 일이에요.
2. 작업 마이닝은 그런 반복 동작을 찾아서 "이건 기계가 해도 되겠네"라고 알려줘요.
3. 하지만 친구의 비밀 노트는 가려 주고 꼭 필요한 장면만 봐야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 211 / 482

<- **이전**: [210. RPA (Robotic Process Automation) - Attended Bot과 Unattended Bot](/studynote/07_enterprise_systems/04_process_consulting/210_rpa_robotic_process_automation_attended_unattended/)
**다음**: [212. BIA (Business Impact Analysis) 평가 지표 분석 기법](/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/) ->

---
