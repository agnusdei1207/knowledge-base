+++
title = "14. 감리 계획 수립 (Audit Planning) - 예비조사, 감리 일정 및 인력 배치, 감리 계획서 작성"
description = "예비조사를 통한 주안점 도출부터 리스크 기반 일정 및 인력 배치까지, 정보시스템 감리의 성공을 좌우하는 감리 계획 수립 아키텍처"
date = 2024-05-20

[taxonomies]
tags = ["design_supervision"]

[extra]
tags = ["design_supervision"]
+++

# 14. 감리 계획 수립 ([Audit Planning](/knowledge-base/studynote/11_design_supervision/01_audit_framework/013_audit_planning/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 감리 계획 수립은 감리 법인이 대상 사업의 범위, 위험 요소([Risk](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)), 제약 사항을 분석하여, 한정된 감리 자원(시간, 인력)을 가장 효과적으로 투입하기 위한 '[전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 청사진'을 설계하는 과정이다.
> 2. **가치**: 맹목적인 전수 검사를 지양하고, [예비 조사](/knowledge-base/studynote/11_design_supervision/01_audit_framework/015_preliminary_survey/)를 통해 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)된 병목 지점과 고위험 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 감리 화력을 집중하는 [위험 기반 감리](/knowledge-base/studynote/11_design_supervision/01_audit_framework/024_risk_based_audit/)([Risk-based Audit](/knowledge-base/studynote/11_design_supervision/01_audit_framework/024_risk_based_audit/))를 통해 감리 품질과 투자 대비 효과([ROI](/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/))를 극대화한다.
> 3. **융합**: 프로젝트 관리([PMBOK](/knowledge-base/studynote/12_it_management/04_sdlc_testing/147_pmbok_10_knowledge_areas/))의 자원 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링([WBS](/knowledge-base/studynote/12_it_management/04_sdlc_testing/149_wbs_work_breakdown_structure/)) 및 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 매니지먼트 기법과 융합하여, 사업의 특성에 최적화된 감리 일정표와 영역별 전문가(DB, 아키텍처, 보안) 할당 매트릭스를 구성한다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

정보시스템 구축 사업은 수백억 원의 예산과 수십만 본의 코드가 얽힌 거대한 복잡계(Complex System)이다. 단 며칠, 몇 명의 감리원이 이 모든 산출물을 100% 전수 조사하는 것은 물리적으로 불가능하다. 따라서 감리가 단순한 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 수준의 피상적 행위(Tick-the-box)로 전락하는 것을 막기 위해서는, 사전에 타격해야 할 핵심 표적(Target)을 좁히고 전문 인력을 적재적소에 배치하는 <strong>감리 계획 수립 (<a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/013_audit_planning/">Audit Planning</a>)</strong> 이 절대적으로 필요하다. 이는 전투에 임하기 전 지형([예비 조사](/knowledge-base/studynote/11_design_supervision/01_audit_framework/015_preliminary_survey/))을 살피고 부대(감리원)를 배치하는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 수립과 동일하며, 계획이 실패하면 본 감리에서 치명적 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 놓치거나 엉뚱한 문서만 검토하다가 철수하는 최악의 사태([안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/))를 맞게 된다.

이 도식은 제한된 감리 자원 환경에서 계획 수립이 부재할 경우 발생하는 감리 품질의 병목과, [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 기반 계획을 통한 해결 구조를 비교해 보여준다.

```text
[계획 부재 시: 무차별 평탄화]
(한정된 인력) ──분산배치──> [저위험 영역 검토] (시간 낭비)
                       => [고위험 영역 (DB 성능) >>> 병목/방치] => 치명적 장애 통과

[리스크 기반 감리 계획 (Risk-based Audit)]
(예비 조사 분석) ──식별──> 리스크 High (예: 트랜잭션, 보안) ──집중투입──> [심층 검증]
                       └> 리스크 Low  (예: 단순 UI)        ──샘플링──> [경량 검증]
```

이 흐름의 핵심은 감리 자원의 '비대칭적 할당(Asymmetric Allocation)'이다. 모든 화면과 테이블을 똑같이 1시간씩 검토하는 것은 낭비다. 계획 수립 단계에서 사업의 뼈대가 되는 코어 뱅킹(Core Banking) 로직이나 대량 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이행(Migration) 구간을 고위험으로 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하고, 이곳에 시니어 아키텍트와 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 튜닝 전문가를 집중 투입하여 병목을 깊게 파고들어야 한다. 실무에서는 이 계획의 성패가 감리 보고서의 깊이(Depth)와 직결된다.

📢 **섹션 요약 비유**: 한정된 경찰 병력으로 도시의 치안을 지킬 때, 범죄가 없는 주택가와 범죄 다발 구역(우범 지대)에 똑같이 순찰차를 보내는 대신, 범죄 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(예비조사)를 분석해 우범 지대에 특공대(전문 감리원)를 집중 배치하는 범죄 예방 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

감리 계획 수립 아키텍처는 [예비 조사](/knowledge-base/studynote/11_design_supervision/01_audit_framework/015_preliminary_survey/)에서 수집된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 바탕으로 영역별 통제 주안점을 설정하고, 이를 실행할 감리원들의 작업 분해 구조([WBS](/knowledge-base/studynote/12_it_management/04_sdlc_testing/149_wbs_work_breakdown_structure/))를 매핑하는 파이프라인으로 구성된다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 점검 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) / 산출물 | 비유 |
|:---|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/015_preliminary_survey/">예비 조사</a> (Preliminary)</strong> | 기초 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집 및 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) | 제안서, 과업내용서 문서 검토 및 발주자/사업자 PM 인터뷰를 통한 프로젝트 현황/갈등 파악 | 예비조사 결과서 | 작전 전 정찰병 파견 |
| <strong><a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/007_audit_domain/">감리 영역</a>/관점 정의</strong> | 감리 범위 구조화 | 사업 관리(PM), 아키텍처([SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)), [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(DB) 등 [감리 영역](/knowledge-base/studynote/11_design_supervision/01_audit_framework/007_audit_domain/)을 분할하고 절차/산출물 관점 매핑 | [감리 프레임워크](/knowledge-base/studynote/11_design_supervision/01_audit_framework/006_audit_framework_3dimensional/) 3차원 | 공격 타겟 구역 분할 |
| **감리 주안점 도출** | 집중 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 대상(Target) 확정 | [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)된 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)(예: 잦은 요구 변경, 구형 장비 연동)를 방어하기 위한 필수 검토 항목 선정 | 감리 주안점 명세 | 스나이퍼의 십자선 정렬 |
| **인력 배치 및 일정** | [자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/) ([Resource Allocation](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/)) | 도출된 주안점의 난이도에 맞춰 해당 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전문 감리원을 매핑하고, 실지 감리 일정 수립 | 감리 [WBS](/knowledge-base/studynote/12_it_management/04_sdlc_testing/149_wbs_work_breakdown_structure/), 인력 투입 계획 | 병과별 특수부대 배치 |
| **감리 계획서 확정** | 3자 간 공식 승인 ([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)) | 작성된 계획서를 발주자, 사업자와 공유하는 [착수 회의](/knowledge-base/studynote/11_design_supervision/01_audit_framework/016_kick_off_meeting/)(Kick-off)를 통해 범위와 권한 공식화 | 최종 감리 계획서 | 합동 작전 지시서 하달 |

이 다이어그램은 예비조사부터 최종 계획서 승인까지 이어지는 정보의 가공과 의사결정 시퀀스를 보여준다.

```text
[입력 데이터] (RFP, 인터뷰, 전월 주간보고서)
      ↓ (분석 및 정제)
[리스크 프로파일링] ─(높은 우선순위)─> [핵심 감리 주안점 도출]
      ↓ (자원 매핑)                            ↓ (검증 도구 선택)
[영역별 감리원 할당] <══(상호 결합)══> [자동화 진단 툴 배정 (SAST, APM)]
      ↓ (스케줄링)
[실지 감리 스케줄 보드 (Gantt Chart)] => [감리 계획서 승인 및 착수 회의]
```

이 시퀀스의 핵심은 '[리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) [프로파일링](/knowledge-base/studynote/02_operating_system/10_security/613_profiling_gprof/)'이 인력 할당과 도구 선택의 방향을 완벽하게 지배(Dominate)한다는 점이다. [예비 조사](/knowledge-base/studynote/11_design_supervision/01_audit_framework/015_preliminary_survey/) 결과 기존 레거시 시스템과의 연계 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)에서 빈번한 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)([Timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/)) 장애가 보고되었다고 가정하자. 이 정보는 주안점으로 도출되며, 이에 따라 네트워크/서버 아키텍처 전문가가 해당 영역에 배정되고, 동시에 네트워크 [패킷 스니핑](/knowledge-base/studynote/09_security/03_network_security/272_packet_sniffing/) 도구나 [부하 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/446_load_test/)([Stress Test](/knowledge-base/studynote/04_software_engineering/11_testing_validation/447_stress_test/)) 스크립트를 사전에 준비하도록 계획된다.

동작 원리를 살펴보면, 총괄 감리원은 투입 가능한 총 감리 맨먼스(Man-Month)를 산정하고, 이를 기능적 [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/)(Functional [Cohesion](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/))가 높은 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 단위로 쪼개어 개별 감리원에게 분배한다. 이때 어떤 감리원은 DB 모델링 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)에 70%의 시간을 쏟도록 계획되고, 어떤 감리원은 UI 웹 [접근성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/) 자동화 진단에 100%를 쏟도록 철저히 역할(Role)이 격리된다.

📢 **섹션 요약 비유**: 대형 종합병원의 수술 계획(감리 계획)을 세울 때, 환자의 사전 문진표와 엑스레이(예비조사)를 보고 종양의 위치(주안점)를 파악한 뒤, 마취과, 외과, 신경외과 전문의(감리원)의 투입 시간과 사용할 수술 도구(자동화 툴)를 치밀하게 조율하는 과정과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

감리 계획을 수립할 때 채택할 수 있는 접근 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)은 크게 '전통적 전수 기반 계획'과 '위험 기반 계획([Risk](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)-based Planning)'으로 나뉜다.

| 항목 | 전수 검사 기반 감리 계획 (Traditional) | [위험 기반 감리](/knowledge-base/studynote/11_design_supervision/01_audit_framework/024_risk_based_audit/) 계획 ([Risk](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)-based) | 품질/비용 트레이드오프 |
|:---|:---|:---|:---|
| **검토 대상 산정** | 시스템의 모든 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)과 문서를 N분의 1로 기계적 분할 분배 | [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 점수([Risk](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) Score)에 따라 검토 시간과 깊이를 차등 분배 | 자원 활용의 효율성 (낭비 방지) |
| **샘플링 기법** | 무작위/단순 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 표본 추출 | 고위험 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), 복잡한 [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 위주의 유의적([가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)) 표본 추출 | 치명적 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)의 적발 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 극대화 |
| **운영 유연성** | 계획된 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)를 경직되게 수행 | 현장에서 새로운 위험 발견 시 타 영역 자원을 즉각 차출/전환 | 실지 감리 시 변동성(Volatility) 대응 |
| **발주처 만족도**| 보고서는 두꺼우나 뻔한 오타 지적 위주 | 핵심 병목과 아키텍처 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 해결책 제시에 따른 높은 컨설팅 가치 | 감리의 비즈니스 파급력 (Impact) |

이 매트릭스는 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 강도와 시스템 복잡도에 따라 감리 자원을 어떻게 배치하는 것이 최적인지를 보여주는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 매트릭스다.

```text
┌──────────────┬────────────────────────┬────────────────────────┐
│ 리스크/영향도│ 복잡도 Low (단순 UI/CRUD)│ 복잡도 High (분산/코어) │
├──────────────┼────────────────────────┼────────────────────────┤
│ High (높음)  │ 자동화 툴 집중 스캐닝  │ 시니어 감리원 밀착 심층 분석 │
│              │ (웹 접근성, 시큐어코딩)│ (락 경합, 데이터 정합성) │
├──────────────┼────────────────────────┼────────────────────────┤
│ Low (낮음)   │ 통계적 샘플링 (10% 추출)│ 구조적 패턴 점검 (경량) │
│              │ (주니어 감리원 할당)   │ (코드 리뷰 생략)        │
└──────────────┴────────────────────────┴────────────────────────┘
```

이 표에서 가장 주의해야 할 영역은 '[리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) High / 복잡도 High' 영역이다. 이곳은 대량의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)이 발생하는 결제 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이나, 외부 기관 연계망([API Gateway](/knowledge-base/studynote/04_software_engineering/11_testing_validation/542_api_gateway/)) 구간이다. 이곳에 주니어 감리원이나 단순 문서 검토를 계획하면 시스템이 붕괴하는 원인을 잡을 수 없다. 반면 '단순 CRUD 화면' 같은 Low/Low 영역은 자동화 진단 도구([SonarQube](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/079_sonarqube/) 등)를 활용하거나 주니어 감리원이 통계적 샘플링으로 빠르게 훑고 지나가도록 계획하여 감리 오버헤드를 낮추는 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)([Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)) 최소화 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 써야 한다.

**과목 융합 관점**:
- <strong>프로젝트 관리 (<a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/147_pmbok_10_knowledge_areas/">PMBOK</a>) 연계</strong>: 감리 계획 수립은 PMBOK의 '위험 관리([Risk Management](/knowledge-base/studynote/09_security/17_framework_compliance/841_iso_27005_risk_management/))' 프로세스인 [위험 식별](/knowledge-base/studynote/09_security/01_intro_principles/027_risk_identification/) → 정성적/정량적 분석 → 대응 계획 수립의 사이클을 정확히 차용한다. 감리원은 프로젝트의 이슈 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)(Issue [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/))를 분석하여 감리 계획의 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/) [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/)(Schedule [Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/))을 조정한다.
- <strong><a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/">소프트웨어 공학</a> (품질 보증) 연계</strong>: 감리 주안점을 도출할 때 ISO/IEC 25010 (기능성, [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/), [사용성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/286_usability_tactics/), [성능 효율성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/343_performance_efficiency/) 등 8대 품질 특성) 프레임워크를 기반으로 각 특성별로 점검할 세부 지표를 계획서에 매핑하여 누락 없는 전방위 품질(QA) 커버리지를 구성한다.

📢 **섹션 요약 비유**: 수능 시험 공부 계획을 짤 때, 1단원부터 무식하게 똑같은 시간으로 정독하는 것(전통적 계획)이 아니라, 내가 자주 틀리는 취약 과목과 배점이 높은 킬러 문항(고위험/고복잡도) 영역에 공부 시간의 80%를 몰아 쓰는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적 학습 플래너([위험 기반 감리](/knowledge-base/studynote/11_design_supervision/01_audit_framework/024_risk_based_audit/) 계획)와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무 감리 총괄은 예비조사에서 포착한 미세한 시그널(징후)을 바탕으로, 감리원 투입과 방어선을 재구축하는 고도의 정치적/기술적 의사결정을 내려야 한다.

1. **시나리오 1: 프로젝트 진척도 뻥튀기(오버 리포팅) 포착**
   - **상황**: 사업자의 주간보고서상 진척률은 90%이나, 예비조사 인터뷰 시 핵심 개발자들이 야근과 피로를 호소하며 [통합 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/400_integration_testing/) 시나리오조차 작성되지 않은 징후가 포착되었다.
   - **판단**: 전형적인 '진척률 조작([EVM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/) 왜곡)' [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)다. 총괄 감리원은 감리 계획을 전면 수정하여, 문서 검토 비중을 극단적으로 낮추고 실제 동작하는 '소프트웨어 인도물(Executable Software)'을 직접 구동해 보는 실증 테스트(Demonstration) 비중을 80% 이상으로 끌어올리도록 일정과 주안점을 재편해야 한다.

2. <strong>시나리오 2: 초정밀 DB 이행(Migration) <a href="/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/">리스크</a> 감지</strong>
   - **상황**: 기존 10년 치 레거시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 새로운 클라우드 DB로 이관하는 사업인데, 예비조사에서 [데이터 정제](/knowledge-base/studynote/07_enterprise_systems/05_data_bi/266_data_cleansing/)(Cleansing) 룰이 불명확하다는 발주처의 불만이 접수되었다.
   - **판단**: 마이그레이션 실패는 오픈 당일 재앙([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Loss/Corruption)으로 이어진다. 감리 계획 수립 시, UI/UX 디자인 감리원을 축소하는 대신 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 모델링 및 SQL 튜닝 특급 기술자를 추가 투입하도록 인력 배치([Resource Allocation](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/)) 매트릭스를 강제로 변경하고, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [체크섬](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/)([Checksum](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/)) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 최우선 주안점으로 선언해야 한다.

3. <strong>시나리오 3: <a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/016_kick_off_meeting/">착수 회의</a>(Kick-off) 시 사업자의 비협조</strong>
   - **상황**: 감리 계획서를 발표하는 [착수 회의](/knowledge-base/studynote/11_design_supervision/01_audit_framework/016_kick_off_meeting/)에서 사업자 PM이 "소스코드 접근 권한(Repository)은 보안상 감리단에 줄 수 없다"며 엑셀 출력물만 보라고 버틴다.
   - **판단**: 소스코드 없는 감리는 '맹인 모드'에 불과하다([안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/): Blind [Audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/)). 감리 총괄은 즉각 [감리 수행](/knowledge-base/studynote/11_design_supervision/01_audit_framework/017_audit_execution/) 보류(Block)를 선언하고, 발주처를 압박하여 '읽기 전용(Read-only) 계정 및 [VDI](/knowledge-base/studynote/11_design_supervision/01_audit_framework/079_developer_cleanroom_vdi_security/) [망분리](/knowledge-base/studynote/12_it_management/05_security_compliance/182_network_separation_model/) 접근 권한'을 제공받는 것을 실지 감리 진입의 선행 조건(Pre-condition)으로 감리 계획서에 명시하여 강행해야 한다.

이 의사결정 트리는 예비조사의 입력값에 따라 감리 총괄이 계획을 동적으로 변경하는 의사결정 라우팅을 보여준다.

```text
[예비조사 시그널 수집] ──(리스크 분석)
                         ├─> (일정 지연 심각) => [실지 가동 테스트 비중 ⇧, 문서 검토 ⇩]
                         │
                         ├─> (보안/데이터 위협) => [해당 도메인 특급 기술자 차출 및 툴 세팅]
                         │
                         └─> (요구사항 분쟁 중) => [과업대비표/RTM 추적성 검증에 인력 50% All-in]
```

이 플로우의 핵심은 감리 계획이 템플릿(문서 껍데기)을 채우는 작업이 아니라, 시스템의 '가장 아픈 곳'을 정밀 타격하기 위해 포메이션(Formation)을 짜는 동적 반응 체계라는 점이다. 실무 감리 총괄의 역량은 이 계획 단계에서 사업의 지뢰밭을 얼마나 정확히 예측하고 방어막(감리 인력)을 두텁게 쌓느냐에 달려 있다.

📢 **섹션 요약 비유**: 축구 국가대표팀 감독이 상대 팀의 전력 분석 영상(예비조사)을 보고 상대 에이스 공격수의 위치(위험 요소)를 파악한 뒤, 그 선수를 집중 마크할 최고의 수비수(전문 감리원)를 맞춤형으로 선발 출전(인력 배치)시키는 전술 보드 설계와 같습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

치밀하게 수립된 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 기반 감리 계획은 감리 법인의 내부 자원 낭비를 막고, 발주처에게는 프로젝트 생존을 위한 최고의 컨설팅을 제공하는 선순환 구조를 완성한다.

| 구분 | 계획 수립 부실 (형식적 템플릿 사용) | [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 기반 계획 수립 (정밀 타격) | 기대 효과 및 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/">결함</a> 적발 품질</strong> | 단순 오탈자 및 화면 깨짐 등 마이너 지적 | DB 락업, 메모리 릭, 보안 취약점 등 크리티컬 버그 적발 | 시스템 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 비용의 획기적 사전 차단 |
| **감리원 업무 부하** | 검토 범위가 방대하여 야근 및 품질 저하 | 타겟이 명확해 심층 분석 및 대안 제시에 집중 | 감리원의 업무 집중도([Cohesion](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/)) 극대화 |
| **사업자 수용성** | 핵심을 벗어난 지적으로 사업자 반발 심화 | 뼈를 때리는 근본적 아키텍처 지적으로 기술적 승복 | 감리 결과 시정 조치 이행률 상승 |

**미래 전망 (Future Standard)**:
향후 감리 계획 수립 과정에는 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)) 기반의 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 예측 모델이 융합될 것이다. 과거 수만 건의 감리 보고서와 프로젝트 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 학습한 AI가 대상 사업의 제안서와 [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) 커밋 빈도(Commit Frequency), 이슈 트래커(Jira)의 티켓 체류 시간 등을 자동으로 분석하여, 어느 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)에서 장애가 발생할 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이 높은지 히트맵(Heatmap)을 생성해 줌으로써, 인간의 직관을 넘어선 '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기반의 초정밀 감리 계획([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)-Driven [Audit Planning](/knowledge-base/studynote/11_design_supervision/01_audit_framework/013_audit_planning/))' 시대가 열릴 것이다.

📢 **섹션 요약 비유**: 과거에는 어부가 감으로 그물을 넓게 던져 물고기를 잡았다면(전수/형식적 감리), 미래의 감리 계획은 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 어군 탐지기가 짚어준 물고기 떼의 정확한 좌표([리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 스코어링)에만 그물을 던져 시간 낭비 없이 만선을 이루는 최첨단 스마트 어업과 같습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- <strong><a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/024_risk_based_audit/">위험 기반 감리</a> (<a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/024_risk_based_audit/">Risk-based Audit</a>)</strong> : 시스템의 모든 요소를 동등하게 보지 않고, 비즈니스 중단 영향도와 발생 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이 높은 고위험 영역에 감리 자원을 집중하는 핵심 아키텍처 철학.
- <strong>작업 분해 구조 (<a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/149_wbs_work_breakdown_structure/">WBS</a>, <a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/149_wbs_work_breakdown_structure/">Work Breakdown Structure</a>)</strong> : [감리 수행](/knowledge-base/studynote/11_design_supervision/01_audit_framework/017_audit_execution/) 범위를 세부 검토 항목 단위로 쪼개고, 각 항목에 담당 감리원과 소요 시간(Man-Hour)을 할당하는 [스케줄](/knowledge-base/studynote/05_database/04_transactions_concurrency/208_schedule_history_transaction_execution_order/)링 기법.
- <strong>과업 대비표 (<a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/025_task_traceability_matrix/">Task Traceability Matrix</a>)</strong> : 발주처의 제안요청서(RFP)와 사업자의 제안서 요구사항이 빠짐없이 목록화된 표로, 감리 계획 시 검토 범위를 획정하는 절대적 [베이스라인](/knowledge-base/studynote/04_software_engineering/03_design_architecture/159_baseline_requirements_configuration_management/).
- <strong><a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/016_kick_off_meeting/">착수 회의</a> (<a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/016_kick_off_meeting/">Kick-off Meeting</a>)</strong> : 수립된 감리 계획서를 발주자 및 피감리인(사업자)과 공식적으로 공유하고, 감리 범위, 보안 협조, 인터뷰 일정을 확정 짓는 3자 간의 공식 합의 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/).
- <strong><a href="/knowledge-base/studynote/12_it_management/04_sdlc_testing/152_evm_earned_value_management/">EVM</a> (<a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/040_evm/">Earned Value Management</a>, 획득 가치 관리)</strong> : 프로젝트의 계획 대비 실제 완료된 작업량(가치)을 비용과 일정 지표([SPI](/knowledge-base/studynote/12_it_management/04_sdlc_testing/159_spi_schedule_performance_index/), [CPI](/knowledge-base/studynote/12_it_management/04_sdlc_testing/158_cpi_cost_performance_index/))로 수치화하는 기법으로, 예비조사 시 진척률 왜곡(조작) 여부를 탐지하는 핵심 척도.


### 📈 관련 키워드 및 발전 흐름도

```text
[감리 요청 — 발주자·감리 의뢰, 감리 범위·목적 정의]
    │
    ▼
[예비조사 (Preliminary Survey) — 개발 계획·산출물·리스크 사전 파악]
    │
    ▼
[감리 계획 수립 (Audit Planning) — 일정·인력·방법론·점검 항목 확정]
    │
    ▼
[감리 수행 — 인터뷰·문서 검토·테스트·현장 확인]
    │
    ▼
[감리 보고서 — 결함·개선 권고·사후 조치 계획 작성 및 제출]
```

이 흐름은 감리 요청에서 출발해 예비조사로 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/)를 파악하고, 계획 수립→수행→보고서 제출로 이어지는 IT 감리 생애 주기의 전 과정을 보여주며, 계획 수립이 성공적 감리의 품질 기반임을 강조한다.


### 👶 어린이를 위한 3줄 비유 설명
1. **개념**: 감리 계획 수립은 보물찾기 탐험을 떠나기 전에 무작정 땅을 파는 게 아니라, 지도를 먼저 꼼꼼히 살펴보고 어디를 먼저 팔지 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 짜는 시간이에요.
2. **원리**: 숲 전체를 다 파보려면 시간이 부족하니까, 동굴이나 늪지대처럼 가장 위험하지만 보물이 있을 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)이 높은 곳(위험 영역)을 골라 힘센 대원(전문가)을 보내기로 작전을 세우는 거죠.
3. **효과**: 이렇게 똑똑하게 계획을 세워두면, 엉뚱한 곳에서 헤매며 힘을 빼지 않고 가장 중요한 진짜 보물(숨은 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/))을 빠르고 정확하게 찾아낼 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 15 / 530

← **이전**: [013. 확인 감리 (Follow-up Audit)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/013_follow_up_audit/)
**다음**: [15. 예비 조사 (Preliminary Survey) - 피감리인 인터뷰, 과업내용서/제안서 분석을 통해 감리 주안점 도출](/knowledge-base/studynote/11_design_supervision/01_audit_framework/015_preliminary_survey/) →

---
