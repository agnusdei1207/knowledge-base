+++
weight = 9999
title = "04. 소프트웨어공학 키워드 목록"
date = "2026-03-04"
[extra]
categories = "studynote-se"
+++
[[267_weight_bias_activation|weight]] = 9999

# 소프트웨어공학 ([[001_software_engineering_definition|Software Engineering]]) 키워드 목록 (심화 확장판)

정보통신기술사·컴퓨터응용시스템기술사 및 전문 SW 엔지니어를 위한 소프트웨어공학 전 영역 핵심 및 심화 키워드 800선입니다.

전통적인 소프트웨어 개발 방법론부터 최신 [[004_agile_relation|애자일]], [[652_devops_calms_culture|DevOps]], [[204_cloud_native_architecture|클라우드 네이티브 아키텍처]], [[190_ai_llm_requirements_specification|AI]] 기반 개발([[263_llm_large_language_model|LLM]]), [[190_secure_coding_guideline|시큐어 코딩]] 및 SW [[374_supply_chain_security|공급망 보안]]까지 폭넓게 다룹니다.

---

## 1. [[001_software_engineering_definition|소프트웨어 공학]] 기초 및 프로세스 모델 (60개)
1. [[001_software_engineering_definition|소프트웨어 공학]] ([[001_software_engineering_definition|Software Engineering]])의 정의 및 목표 ([[642_reliability_mtbf_mttr_mttf_availability|신뢰성]], 효율성, [[346_maintainability_portability|유지보수성]])
2. [[002_software_crisis|소프트웨어 위기]] ([[002_software_crisis|Software Crisis]]) - 비용 초과, 일정 [[015_지연_데이터_관점|지연]], 품질 저하
3. [[003_sdlc|소프트웨어 생명주기]] ([[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]], Software Development Life Cycle)
4. [[004_waterfall_model|폭포수 모델]] ([[004_waterfall_model|Waterfall Model]]) - 순차적, 문서 중심
5. V-모델 ([[132_v_model_sdlc_verification_validation_testing|V-Model]]) - [[395_verification_process_review|검증]]([[395_verification_process_review|Verification]])과 [[396_validation|확인]]([[396_validation|Validation]])의 대응
6. [[006_prototype_model|프로토타입 모델]] ([[006_prototype_model|Prototype Model]]) - 요구사항 명확화, 시제품
7. [[007_spiral_model|나선형 모델]] ([[007_spiral_model|Spiral Model]]) - 위험 분석([[096_risk_non_risk_architecture_evaluation_flaws|Risk]] Analysis) 강조, 점진적 확장
8. 반복적/점진적 모델 (Iterative and Incremental Model)
9. [[009_rad_model|RAD]] ([[009_rad_model|Rapid Application Development]]) 모델 - JAD, CASE 도구 활용
[[489_raid_10_hybrid|10]]. [[010_evolutionary_process_model|진화적 프로세스 모델]] ([[010_evolutionary_process_model|Evolutionary Process Model]])
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[011_cleanroom_software_engineering|클린룸 소프트웨어 공학]] ([[011_cleanroom_software_engineering|Cleanroom Software Engineering]]) - 통계적 품질 제어
12. [[012_agile_methodology|애자일 방법론]] ([[012_agile_methodology|Agile Methodology]]) 개요
13. ISO/IEC 12207 ([[003_sdlc|소프트웨어 생명주기]] 공정 표준) - 기본, 지원, 조직 공정
14. ISO/IEC 15504 ([[139_spice_iso_iec_15504_process_assessment|SPICE]]) - 소프트웨어 프로세스 평가 표준
15. [[133_cmmi_capability_maturity_model_integration_levels|CMMI]] (Capability [[011_maturity_model|Maturity Model]] Integration) - 단계형/연속형 모델
16. [[133_cmmi_capability_maturity_model_integration_levels|CMMI]] 5단계 - [[459_quic_fec_forward_error_correction|초기]], 관리, 정의, 정량적 관리, 최적화
17. [[017_process_assets_osp|프로세스 자산]] ([[017_process_assets_osp|Process Assets]]) 및 조직 표준 프로세스
18. [[018_psp_tsp|PSP]] ([[018_psp_tsp|Personal Software Process]]) / [[106_fenwick_tree|TSP]] (Team Software [[300_process|Process]])
19. [[019_software_product_line|소프트웨어 제품 라인]] ([[187_spl_software_product_line_variability|SPL]], [[019_software_product_line|Software Product Line]]) - [[064_relation_domain|도메인]]/어플리케이션 공학
20. [[020_software_configuration_management|형상 관리]] ([[167_scm_software_configuration_management|SCM]], [[020_software_configuration_management|Software Configuration Management]])
21. [[021_configuration_identification|형상 식별]] ([[021_configuration_identification|Configuration Identification]]) - 형상 항목([[090_configuration_item|CI]]) 선정
22. [[022_configuration_control|형상 통제]] ([[022_configuration_control|Configuration Control]]) - 변경 제어 위원회([[160_change_control_board_ccb_requirements_review|CCB]])
23. [[023_configuration_audit|형상 감사]] ([[023_configuration_audit|Configuration Audit]]) - [[003_integrity|무결성]] [[396_validation|확인]]
24. 형상 기록/보고 ([[024_configuration_status_accounting|Configuration Status Accounting]])
25. [[025_baseline|기준선]] ([[025_baseline|Baseline]]) - 기능적, 설계, 시험, 제품 [[025_baseline|기준선]]
26. [[288_version_ihl_tos_total_length|버전]] 관리 시스템 ([[026_version_control_system|VCS]]) - Centralized (SVN) vs Distributed (Git)
27. [[079_change_enablement|변경 관리]] ([[027_change_management|Change Management]]) 프로세스
28. 소프트웨어 재공학 (Re-engineering) - 분석, 재구성, [[029_reverse_engineering|역공학]], 이관
29. [[029_reverse_engineering|역공학]] ([[780_reverse_engineering|Reverse Engineering]]) - 소스코드에서 설계서 추출
30. 재사용 (Reuse) - 자산의 공유, [[603_component_independent_deployment_unit|컴포넌트]] 기반 개발(CBD)
31. 유지보수 (Maintenance)의 4가지 유형 - 수정, 적응, 완전(개선), 예방
32. [[032_software_obsolescence|소프트웨어 노후화]] ([[032_software_obsolescence|Software Obsolescence]])
33. [[100_technical_debt_monitoring_release_policy|기술 부채]] ([[100_technical_debt_monitoring_release_policy|Technical Debt]]) - 단기적 편의성으로 인한 장기적 비용 증가
34. 레거시 시스템 (Legacy System) 현대화 [[268_strategy_pattern|전략]]
35. 프로젝트 관리 (PM) 10대 지식 영역 ([[147_pmbok_10_knowledge_areas|PMBOK]])
36. [[149_wbs_work_breakdown_structure|WBS]] ([[149_wbs_work_breakdown_structure|Work Breakdown Structure]]) - 작업 분할 구조도
37. [[150_cpm_critical_path_method|CPM]] ([[037_cpm|Critical Path Method]]) - 주공정법, 최장 경로
38. [[151_pert_three_point_estimation|PERT]] (Program Evaluation and [[153_requirements_review_inspection_walkthrough|Review]] Technique) - 낙관, 비관, 기대치 분석
39. [[039_gantt_chart|간트 차트]] ([[039_gantt_chart|Gantt Chart]]) - 일정 [[003_bigdata_7v|시각화]]
40. [[152_evm_earned_value_management|EVM]] ([[040_evm|Earned Value Management]]) - 성과 측정 관리 ([[153_pv_planned_value|PV]], [[154_ev_earned_value|EV]], [[155_ac_actual_cost|AC]], [[157_sv_schedule_variance|SV]], [[156_cv_cost_variance|CV]], [[159_spi_schedule_performance_index|SPI]], [[158_cpi_cost_performance_index|CPI]])
41. 위험 관리 ([[841_iso_27005_risk_management|Risk Management]]) 4단계 - [[655_ir_detection_analysis|식별]], 분석, 대응, 모니터링
42. [[033_risk_response_strategies|위험 대응 전략]] - 회피, 전가, 완화, 수용
43. 품질 보증 (QA) vs 품질 제어 (QC)
44. 소프트웨어 비용 산정 기법 개요
45. 하향식 산정 - 전문가 감정, 델타이 기법
46. 상향식 산정 - LOC (Line of [[082_process_memory_structure|Code]]), 단계별 인월 산정
47. [[145_cocomo_model|COCOMO]] ([[145_cocomo_model|Constructive Cost Model]]) - 유기적, 준분리형, 내장형
48. [[145_cocomo_model|COCOMO]] II - 응용 구성, [[459_quic_fec_forward_error_correction|초기]] 설계, 포스트 아키텍처 모델
49. [[673_function_point_ilf_eif|기능점수]] ([[293_fp_function_point|FP]], [[140_function_point|Function Point]]) 산정 - [[141_fp_data_functions|데이터 기능]](ILF, EIF), [[142_fp_transaction_functions|트랜잭션 기능]](EI, EO, EQ)
50. 간이법 vs 상세법 [[673_function_point_ilf_eif|기능점수]] 산정
51. [[051_delphi_method|델파이 기법]] ([[285_delphi_method|Delphi Method]]) - 전문가 합의 기반 예측
52. [[052_wideband_delphi|와이드밴드 델파이]] ([[052_wideband_delphi|Wideband Delphi]]) - 팀 단위 반복적 리뷰
53. 백파이어링 (Backfiring) 기법 - LOC와 [[293_fp_function_point|FP]] 간 변환
54. 브룩스의 법칙 (Brooks's Law) - 지체된 프로젝트에 인력 투입 시 더 지체됨
55. [[112_zachman_framework|잭맨 프레임워크]] ([[112_zachman_framework|Zachman Framework]]) - 전사적 아키텍처([[110_enterprise_architecture_ea|EA]]) 프레임워크
56. 토가프 ([[113_togaf|TOGAF]]) - [[113_togaf|The Open Group]] [[319_architecture|Architecture]] Framework
57. [[057_mda_model_driven_architecture|모델 주도 아키텍처]] (MDA, Model Driven [[319_architecture|Architecture]]) - [[430_pim|PIM]], PSM 매핑
58. [[058_methodology_tailoring|방법론 테일러링]] ([[058_methodology_tailoring|Tailoring]]) - 표준 프로세스를 조직/프로젝트에 맞게 최적화
59. [[059_pmo_project_management_office|PMO]] ([[059_pmo_project_management_office|Project Management Office]]) - 전사 프로젝트 관리 조직
60. [[060_brainstorming_4_principles|브레인스토밍 4원칙]] (비판금지, 자유분방, 다다익선, 결합개선)

## 2. [[004_agile_relation|애자일]] 개발 및 최신 방법론 (70개)
61. [[061_agile_manifesto|애자일 선언문]] ([[061_agile_manifesto|Agile Manifesto]]) - 4가지 가치, 12가지 원칙
62. [[062_scrum_framework_overview|스크럼]] ([[658_agile_scrum_roles|Scrum]]) 프레임워크 - 역할, 이벤트, 산출물
63. [[063_product_owner_po|제품 책임자]] (Product Owner) - 비즈니스 가치 극대화, 백로그 관리
64. [[064_scrum_master_sm|스크럼 마스터]] ([[064_scrum_master_sm|Scrum Master]]) - 가이드, 장애 제거
65. [[065_development_team_scrum|개발 팀]] ([[065_development_team_scrum|Development Team]]) - 자기 조직화, 다기능 팀
66. [[066_product_backlog_grooming|제품 백로그]] ([[066_product_backlog_grooming|Product Backlog]]) - 요구사항 우선순위 목록
67. [[067_sprint_timebox|스프린트]] ([[067_sprint_timebox|Sprint]]) - 1~4주의 개발 주기
68. [[068_sprint_planning|스프린트 계획 회의]] ([[068_sprint_planning|Sprint Planning]])
69. [[069_daily_standup_scrum|데일리 스탠드업]] ([[069_daily_standup_scrum|Daily Scrum]]) - [[216_progress_in_synchronization|진행]] 상황 공유, 장애 파악
70. [[070_sprint_review_demo|스프린트 리뷰]] ([[070_sprint_review_demo|Sprint Review]]) - 데모 및 피드백
71. [[071_sprint_retrospective|스프린트 회고]] ([[071_sprint_retrospective|Sprint Retrospective]]) - 프로세스 개선
72. [[072_burndown_burnup_chart|번다운 차트]] ([[660_burndown_chart|Burndown Chart]]) / 번업 차트 (Burnup Chart)
73. [[073_xp_extreme_programming|XP]] (e/Xtreme Programming) - 5가지 가치, 12가지 실천 방법
74. 짝 프로그래밍 ([[074_pair_programming_driver_navigator|Pair Programming]]) - 내비게이터와 드라이버
75. [[075_collective_code_ownership|공동 코드 소유]] ([[075_collective_code_ownership|Collective Code Ownership]])
76. [[076_ci_continuous_integration|지속적 통합]] ([[090_configuration_item|CI]], [[019_continuous_integration|Continuous Integration]])
77. [[077_tdd_test_driven_development|테스트 주도 개발]] ([[164_tdd_test_driven_development|TDD]], [[470_tdd_lifecycle|Test Driven Development]]) - Red-Green-[[213_refactoring_cloud_native_rearchitecture|Refactor]]
78. [[213_refactoring_cloud_native_rearchitecture|리팩토링]] ([[078_refactoring_code_smells|Refactoring]]) - 외부 동작 변경 없이 내부 구조 개선
79. [[079_metaphor_xp_practice|메타포]] (Metaphor) - 시스템의 전체적 가이드라인
80. [[080_small_releases|소규모 릴리즈]] ([[080_small_releases|Small Releases]])
81. [[081_user_story_invest|사용자 스토리]] ([[081_user_story_invest|User Story]]) - Who, What, Why 형식
82. [[082_story_point_velocity|스토리 포인트]] ([[082_story_point_velocity|Story Point]]) - 상대적 규모 산정
83. [[083_planning_poker|플래닝 포커]] ([[083_planning_poker|Planning Poker]]) - 다수 전문가 합의 기반 산정
84. [[084_kanban_board_wip_limit|칸반]] ([[084_kanban_board_wip_limit|Kanban]]) - 워크플로우 [[003_bigdata_7v|시각화]], WIP([[661_kanban_wip_limit|Work In Progress]]) 제한
85. [[085_lead_time_cycle_time|리드 타임]] ([[085_lead_time_cycle_time|Lead Time]]) / 사이클 타임 (Cycle Time)
86. [[086_cumulative_flow_diagram_cfd|누적 흐름도]] (CFD, Cumulative Flow Diagram)
87. 린 ([[087_lean_software_development_7_principles|Lean]]) 소프트웨어 개발 - 7대 원칙 (낭비 제거, 학습 증진 등)
88. [[088_value_stream_mapping_vsm|가치 스트림 맵]] ([[088_value_stream_mapping_vsm|Value Stream Mapping]])
89. [[035_lean_startup|린 스타트업]] ([[035_lean_startup|Lean Startup]]) - 구축-측정-학습 [[005_feedback_loop|피드백 루프]]
90. [[090_mvp_minimum_viable_product|최소 존립 제품]] ([[036_mvp|MVP]], [[036_mvp|Minimum Viable Product]])
91. [[037_pivot|피벗]] ([[037_pivot|Pivot]]) - [[268_strategy_pattern|전략]]적 방향 전환
92. [[092_scaled_agile_frameworks_overview|대규모 애자일]] ([[092_scaled_agile_frameworks_overview|Scaled Agile]]) 프레임워크
93. [[093_safe_scaled_agile_framework_art_pi|SAFe]] ([[093_safe_scaled_agile_framework_art_pi|Scaled Agile Framework]]) - 기업용 [[092_scaled_agile_frameworks_overview|대규모 애자일]]
94. [[094_less_large_scale_scrum|LeSS]] ([[094_less_large_scale_scrum|Large-Scale Scrum]]) - 다수 팀 [[062_scrum_framework_overview|스크럼]] 확장
95. Nexus - [[062_scrum_framework_overview|스크럼]] 팀 간 의존성 관리
96. Spotify 모델 - Tribe, Squad, Chapter, Guild
97. [[652_devops_calms_culture|DevOps]] (Development + Operations) - 문화, 자동화, 측정, 공유
98. [[098_iac_infrastructure_as_code_terraform|인프라로서의 코드]] ([[793_iac_idempotency_template|IaC]], [[062_infrastructure_as_code|Infrastructure as Code]])
99. [[099_continuous_deployment_cd|지속적 배포]] (CD, [[165_continuous_deployment|Continuous Deployment]] / Delivery)
100. [[100_sre_site_reliability_engineering_error_budget|SRE]] ([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]]) - 구글의 운영 방식, [[101_error_budget_sre|에러 예산]]
101. [[101_error_budget_sre|에러 예산]] ([[101_error_budget_sre|Error Budget]]) - 안정성 vs 속도 트레이드 오프
102. [[102_sli_slo_service_level_indicator_objective|SLI]] ([[102_sli_slo_service_level_indicator_objective|Service Level Indicator]]) / [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]])
103. [[085_sla|SLA]] ([[085_sla|Service Level Agreement]])
104. [[685_toil_automation_sre|토일]] ([[685_toil_automation_sre|Toil]]) - SRE에서 줄여야 할 단순 반복적 운영 작업
105. [[653_devsecops_shift_left|DevSecOps]] - 보안의 좌측 이동 ([[105_devsecops_shift_left_security|Shift-Left Security]])
106. [[344_finops|FinOps]] - [[227_cloud_cost_optimization|클라우드 비용 최적화]] 및 관리
107. [[348_mlops|MLOps]] - [[241_machine_learning_basics|머신러닝]] 생명주기 관리
108. [[221_llmops_large_language_model_ops|LLMOps]] - [[582_llm_based_code_generation_tools|대규모 언어 모델]] 운영 및 [[133_fine_tuning|미세 조정]] 관리
109. [[109_platform_engineering_cognitive_load|플랫폼 엔지니어링]] ([[109_platform_engineering_cognitive_load|Platform Engineering]]) - 개발자 [[098_self_service_portal_helpdesk_automation|셀프 서비스 포털]] ([[536_idp_identity_provider|IDP]])
110. [[110_idp_internal_developer_platform_backstage|내부 개발자 플랫폼]] ([[536_idp_identity_provider|IDP]], [[200_internal_developer_platform_backstage|Internal Developer Platform]])
111. 가시성 ([[642_observability_telemetry|Observability]]) - [[567_metrics_time_series_prometheus_grafana|Metrics]], [[568_logs_distributed_logging_elk_fluentd|Logs]], Traces (3대 요소)
112. [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] ([[569_distributed_tracing_opentelemetry_jaeger|Distributed Tracing]]) - [[532_microservices_decomposition_patterns|마이크로서비스]] 간 호출 추적
113. [[751_chaos_engineering|카오스 엔지니어링]] ([[751_chaos_engineering|Chaos Engineering]]) - 시스템 회복력 테스트
114. [[576_feature_flag_ab_testing_rollout|피처 플래그]] ([[576_feature_flag_ab_testing_rollout|Feature Flag]] / Toggle) - 런타임 기능 활성/비활성
115. [[115_canary_deployment_gradual_rollout|카나리 배포]] ([[115_canary_deployment_gradual_rollout|Canary Deployment]]) - 점진적 릴리즈
116. 블루/그린 배포 (Blue/Green [[087_deployment_kubernetes_workload_rolling_update|Deployment]]) - [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]] [[268_strategy_pattern|전략]]
117. [[117_rolling_update_deployment|롤링 업데이트]] ([[083_rolling_update_deployment_zero_downtime_version_inconsistency|Rolling Update]])
118. [[575_shadow_deployment_traffic_mirroring|섀도우 배포]] ([[118_shadow_deployment_traffic_mirroring|Shadow Deployment]]) - 실트래픽 [[333_raid_1|미러링]] 테스트
119. [[119_gitops_single_source_of_truth|GitOps]] - Git을 진실의 원천(Source of Truth)으로 하는 운영
120. 선언적 인프라 관리 ([[219_declarative_yaml|Declarative]] Infrastructure)
121. [[090_configuration_item|CI]]/CD 파이프라인 ([[082_pipeline|Pipeline]]) 자동화
122. [[205_kubernetes_container_orchestration|컨테이너 오케스트레이션]] ([[205_kubernetes_container_orchestration|Kubernetes]] 등) 연계
123. [[206_serverless_cold_start|서버리스]] ([[206_serverless_cold_start|Serverless]]) 개발 모델 및 [[342_faas|FaaS]]
124. [[531_cloud_native_architecture|클라우드 네이티브]] 개발 ([[199_cloud_native_architecture_msa_cicd_devops|Cloud Native]] Development)
125. [[006_twelve_factor|12 팩터 앱]] ([[200_12_factor_app_cloud_native_principles|12-Factor App]]) 아키텍처 방법론
126. 행동 주도 개발 ([[165_bdd_behavior_driven_development|BDD]], [[126_bdd_behavior_driven_development_given_when_then|Behavior-Driven Development]])
127. [[064_relation_domain|도메인]] 주도 개발 ([[310_architecture|DDD]])의 [[004_agile_relation|애자일]]적 접근
128. [[038_water_scrum_fall|워터스크럼폴]] ([[128_water_scrum_fall_anti_pattern|Water-Scrum-Fall]]) [[128_water_scrum_fall_anti_pattern|안티패턴]]
129. [[129_spike_agile_technical_investigation|스파이크]] ([[129_spike_agile_technical_investigation|Spike]]) - 기술적 위험 해소를 위한 짧은 조사/프로토타이핑
130. [[165_acceptance_criteria_definition|인수 기준]] ([[165_acceptance_criteria_definition|Acceptance Criteria]]) 명확화 (INVEST 원칙)

## 3. 요구공학 및 비즈니스 분석 (60개)
131. 요구공학 ([[131_requirements_engineering|Requirements Engineering]]) 정의 및 필요성
132. 요구사항의 유형 - 기능적 요구사항 vs 비기능적 요구사항
133. [[133_non_functional_requirements|비기능 요구사항]] ([[279_quality_attributes_scenario|Quality Attributes]]) - [[282_performance_tactics|성능]], 보안, [[452_availability|가용성]], [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 등
134. 요구공학 프로세스 - 도출, 분석, 명세, [[396_validation|확인]], 관리
135. 요구사항 도출 (Elicitation) 기법 - 인터뷰, 설문, 워크숍, 관찰
136. 브레인스토밍 (Brainstorming) / JAD (Joint Application Design)
137. 페르소나 (Persona) 분석 - 가상 사용자 모델링
138. 사용자 여정 지도 (User Journey Map)
139. 프로토타이핑 (Prototyping) - Low-fidelity vs High-fidelity
140. 섀도잉 (Shadowing) - 사용자 업무 환경 직접 관찰
141. [[141_focus_group_interview_fgi|포커스 그룹 인터뷰]] ([[141_focus_group_interview_fgi|FGI]])
142. 요구사항 분석 (Analysis) - 모순 해결, 범위 확정
143. [[143_structured_analysis_dfd_dd_minispec|구조적 분석]] ([[143_structured_analysis_dfd_dd_minispec|Structured Analysis]]) - [[144_dfd_data_flow_diagram|DFD]], [[509_data_dictionary|Data Dictionary]], [[145_1_mini_spec|Mini-Spec]]
144. 자료 흐름도 ([[144_dfd_data_flow_diagram|DFD]], [[144_dfd_data_flow_diagram|Data Flow Diagram]]) - [[300_process|Process]], [[001_dikw_pyramid|Data]] Flow, [[001_dikw_pyramid|Data]] Store, Terminator
145. 자료 사전 ([[769_architecture|DD]], [[509_data_dictionary|Data Dictionary]]) - =, +, { }, [ ], ( ), * *
146. [[146_ooa_object_oriented_analysis|객체지향 분석]] ([[146_ooa_object_oriented_analysis|OOA]], Object-Oriented Analysis)
147. [[238_use_case_diagram_functional_modeling|유스케이스 다이어그램]] ([[147_use_case_diagram|Use Case Diagram]]) - 액터, 유스케이스, [[083_relationship_in_er_model|관계]](포함, 확장)
148. [[148_requirements_specification_formal_informal|요구사항 명세]] ([[148_requirements_specification_formal_informal|Specification]]) - 정형 명세 vs 비정형 명세
149. [[149_software_requirements_specification_srs|소프트웨어 요구사항 명세서]] (SRS, Software Requirements [[148_requirements_specification_formal_informal|Specification]])
150. SRS의 품질 특성 - [[002_bigdata_5v|정확성]], 명확성, 완전성, [[194_consistency_database_integrity|일관성]], 수정 용이성, 추적 가능성
151. 요구사항 [[396_validation|확인]] 및 [[395_verification_process_review|검증]] (V&V, [[395_verification_process_review|Verification]] & [[396_validation|Validation]])
152. [[153_requirements_review_inspection_walkthrough|요구사항 검토]] ([[153_requirements_review_inspection_walkthrough|Review]]) - [[161_inspection_formal_review|인스펙션]], 워크쓰루
153. [[161_inspection_formal_review|인스펙션]] (Inspection) - 공식적 검토, [[273_mediator_pattern|중재자]], [[435_checklist_based_testing|체크리스트]]
154. 워크쓰루 (Walkthrough) - 비공식적, 지식 공유 위주
155. [[163_peer_review|동료 검토]] ([[163_peer_review|Peer Review]])
156. [[156_requirements_traceability_vertical_horizontal|요구사항 추적성]] ([[228_blockchain_smart_contract_traceability|Traceability]]) - 수직적/수평적 추적성
157. [[157_requirements_traceability_matrix_rtm|요구사항 추적 매트릭스]] ([[667_requirements_traceability_matrix|RTM]], [[667_requirements_traceability_matrix|Requirements Traceability Matrix]])
158. [[158_requirements_management_change_control|요구사항 관리]] ([[372_management|Management]]) - 변경 통제, [[288_version_ihl_tos_total_length|버전]] 관리
159. [[159_baseline_requirements_configuration_management|베이스라인]] ([[025_baseline|Baseline]]) [[009_config|설정]] 및 관리
160. [[160_change_control_board_ccb_requirements_review|형상 통제 위원회]] ([[160_change_control_board_ccb_requirements_review|CCB]]) 요구사항 변경 심사
161. [[161_scope_creep_requirements_inflation_prevention|범위 크리프]] ([[161_scope_creep_requirements_inflation_prevention|Scope Creep]]) - 무분별한 요구사항 확장 방지
162. [[162_gold_plating_anti_pattern|골드 플래팅]] ([[162_gold_plating_anti_pattern|Gold Plating]]) - 요구사항에 없는 기능 임의 추가 ([[128_water_scrum_fall_anti_pattern|안티패턴]])
163. [[163_bpmn_business_process_modeling_notation|비즈니스 프로세스 모델링]] ([[163_bpmn_business_process_modeling_notation|BPMN]])
164. [[164_use_case_scenario_flows|유스케이스 시나리오]] ([[164_use_case_scenario_flows|Use Case Scenario]]) - 기본 흐름, 대안 흐름, 예외 흐름
165. [[165_acceptance_criteria_definition|인수 기준]] ([[165_acceptance_criteria_definition|Acceptance Criteria]]) 정의
166. MoSCoW 기법 - Must, Should, Could, Won't 우선순위 결정
167. [[167_kano_model_quality_attributes|카노 모델]] ([[167_kano_model_quality_attributes|Kano Model]]) - 당연적, 일원적, 매력적 품질
168. [[168_qfd_quality_function_deployment|품질 기능 전개]] (QFD, Quality Function [[087_deployment_kubernetes_workload_rolling_update|Deployment]])
169. [[169_hoq_house_of_quality_matrix|품질의 집]] (HoQ, House of Quality) 매트릭스
170. [[170_domain_analysis|도메인 분석]] ([[170_domain_analysis|Domain Analysis]])
171. [[171_requirements_consistency_checking|요구사항 일관성 검사]] ([[171_requirements_consistency_checking|Consistency Checking]])
172. [[172_business_case_roi_analysis|비즈니스 케이스]] ([[172_business_case_roi_analysis|Business Case]]) 및 [[012_roi_return_on_investment|ROI]] 분석
173. [[173_stakeholder_identification_impact_matrix|이해관계자]] ([[173_stakeholder_identification_impact_matrix|Stakeholder]]) [[655_ir_detection_analysis|식별]] 및 영향도 매트릭스
174. [[174_pairwise_comparison_priority_matrix|페어와이즈]] ([[174_pairwise_comparison_priority_matrix|Pairwise]]) 우선순위 결정 기법
175. [[175_formal_informal_specification_languages|요구사항 명세 언어]] (Z, VDM 등 정형 언어)
176. [[176_petri_net_concurrent_system_specification|페트리 넷]] ([[176_petri_net_concurrent_system_specification|Petri Net]]) - 병행 시스템 명세
177. [[177_requirements_management_tools_jira_doors|요구사항 도구]] (Jira, DOORS 등) 활용 [[268_strategy_pattern|전략]]
178. [[178_as_is_to_be_analysis|AS-IS]] ([[178_as_is_to_be_analysis|현재 상태]]) / TO-BE (미래 상태) 분석
179. SWOT 분석, 3C/4C 분석 연계 요구 도출
180. [[180_mind_map_affinity_diagram|마인드 맵]] ([[180_mind_map_affinity_diagram|Mind Map]]) 및 친화도 ([[778_process_affinity_scheduling_pinning|Affinity]] Diagram)
181. [[029_reverse_engineering|역공학]]을 통한 요구사항 추출
182. [[182_epic_agile_requirements|에픽]] ([[244_epic|Epic]]) - 거시적 스토리 집합
183. [[183_user_story_mapping|유저 스토리 맵]] ([[183_user_story_mapping|User Story Mapping]])
184. [[184_theme_agile_requirements|테마]] ([[184_theme_agile_requirements|Theme]]) - [[182_epic_agile_requirements|에픽]]들의 상위 카테고리
185. [[185_lean_canvas_business_model|린 캔버스]] ([[185_lean_canvas_business_model|Lean Canvas]]) 1페이지 비즈니스 모델
186. [[186_value_proposition_canvas|가치 제안 캔버스]] ([[186_value_proposition_canvas|Value Proposition Canvas]])
187. [[019_software_product_line|소프트웨어 제품 라인]] ([[187_spl_software_product_line_variability|SPL]]) 요구사항 가변성(Variability) 분석
188. [[188_feature_model_variability_tree|피쳐 모델]] ([[188_feature_model_variability_tree|Feature Model]]) 가변성 트리
189. BDD의 Given-When-Then 문법을 이용한 명세
190. [[190_ai_llm_requirements_specification|AI]]([[263_llm_large_language_model|LLM]]) 기반 [[148_requirements_specification_formal_informal|요구사항 명세]]서 초안 자동 [[087_process_state_transition|생성]] 지원

## 4. 소프트웨어 설계 및 아키텍처 (80개)
191. 소프트웨어 설계 원칙 - [[198_abstraction_control_data_process|추상화]], 캡슐화, [[192_module_independence|모듈]]화, [[199_information_hiding_encapsulation|정보 은닉]]
192. [[192_module_independence|모듈]] ([[192_module_independence|Module]]) - 독립적 기능을 수행하는 단위
193. [[193_cohesion_levels|응집도]] ([[193_cohesion_levels|Cohesion]]) - [[192_module_independence|모듈]] 내부 요소들의 연관 정도 (높을수록 좋음)
194. [[193_cohesion_levels|응집도]] 단계 - 우연적, [[369_logic_bomb|논리]]적, 시간적, 절차적, 통신적, 순차적, 기능적 [[193_cohesion_levels|응집도]]
195. [[195_coupling_levels|결합도]] ([[195_coupling_levels|Coupling]]) - [[192_module_independence|모듈]] 간 상호 의존 정도 (낮을수록 좋음)
196. [[195_coupling_levels|결합도]] 단계 - 내용, 공통, 제어, 스탬프, 자료 [[195_coupling_levels|결합도]]
197. [[197_fan_in_fan_out|팬인]] ([[197_fan_in_fan_out|Fan-in]]) / 팬아웃 (Fan-out) - [[192_module_independence|모듈]] 복잡도 지표
198. [[198_abstraction_control_data_process|추상화]] ([[198_abstraction_control_data_process|Abstraction]]) - 제어, 자료, 과정 [[198_abstraction_control_data_process|추상화]]
199. [[199_information_hiding_encapsulation|정보 은닉]] ([[199_information_hiding_encapsulation|Information Hiding]]) - 내부 구현 상세를 숨김
200. [[200_divide_and_conquer_software_design|분할과 정복]] ([[005_divide_and_conquer|Divide and Conquer]])
201. [[201_software_architecture_definition|소프트웨어 아키텍처]] ([[201_software_architecture_definition|Software Architecture]]) 정의
202. [[202_architecture_drivers_quality_attributes|아키텍처 드라이버]] ([[202_architecture_drivers_quality_attributes|Architecture Drivers]]) - 비즈니스 목표, 제약, 품질 [[082_attribute_types_er_model|속성]]
203. [[203_4_plus_1_view_model_architecture|아키텍처 뷰 모델]] (4+1 [[151_sql_view_virtual_table|View]]) - [[369_logic_bomb|논리]], 구현, 프로세스, 배치 + [[089_use_case_view_plus_one_view_actor_boundary|유스케이스 뷰]]
204. [[114_architecture_style|아키텍처 스타일]] 및 패턴 개요
205. [[205_layered_architecture_separation_of_concerns|계층형 아키텍처]] ([[205_layered_architecture_separation_of_concerns|Layered Architecture]]) - 관심사 분리 (Presentation, Business, [[001_dikw_pyramid|Data]])
206. [[206_client_server_architecture_model|클라이언트-서버 아키텍처]] ([[206_client_server_architecture_model|Client-Server]])
207. [[207_pipe_filter_architecture_data_stream|파이프-필터 아키텍처]] ([[207_pipe_filter_architecture_data_stream|Pipe-Filter]]) - [[001_dikw_pyramid|데이터]] [[229_stream_processing_kafka_flink|스트림 처리]]
208. [[208_broker_pattern_distributed_systems_message|브로커 패턴]] ([[208_broker_pattern_distributed_systems_message|Broker Pattern]]) - [[136_variance|분산]] 시스템 메세지 중계
209. [[209_blackboard_pattern_ai_heuristic|블랙보드 패턴]] ([[209_blackboard_pattern_ai_heuristic|Blackboard Pattern]]) - 음성/패턴 인식, 공용 [[001_dikw_pyramid|데이터]]소스를 여러 지식 [[192_module_independence|모듈]]이 [[316_reference_pattern_nosql|참조]]
210. [[210_mvc_model_view_controller_architecture|모델-뷰-컨트롤러]] (MVC, [[405_mvc_m_v_c|Model-View-Controller]])
211. [[036_mvp|MVP]] ([[211_mvp_mvvm_architecture_frontend|Model-View-Presenter]]) / MVVM (Model-[[151_sql_view_virtual_table|View]]-ViewModel)
212. [[212_soa_service_oriented_architecture_esb|서비스 지향 아키텍처]] ([[618_soa_hardware|SOA]], [[618_soa_hardware|Service Oriented Architecture]]) - [[146_esb_enterprise_service_bus_architecture|ESB]] 기반
213. [[213_msa_microservices_architecture|마이크로서비스 아키텍처]] ([[619_msa_traffic_hardware|MSA]], [[122_msa_microservices_architecture|Microservices Architecture]])
214. [[214_eda_event_driven_architecture_async|이벤트 드리븐 아키텍처]] ([[064_eda|EDA]], [[140_event_driven_architecture_eda|Event-Driven Architecture]])
215. [[215_serverless_architecture_faas_aws_lambda|서버리스 아키텍처]] ([[558_serverless_architecture|Serverless Architecture]] / [[342_faas|FaaS]])
216. [[216_hexagonal_architecture_ports_and_adapters|헥사고날 아키텍처]] ([[366_process|Hexagonal Architecture]] / Ports and Adapters)
217. [[217_clean_architecture_dependency_rule|클린 아키텍처]] ([[217_clean_architecture_dependency_rule|Clean Architecture]]) - Robert C. Martin (Uncle Bob)
218. [[218_onion_architecture_domain_centric_design|어니언 아키텍처]] ([[218_onion_architecture_domain_centric_design|Onion Architecture]])
219. [[310_architecture|도메인 주도 설계]] ([[310_architecture|DDD]], [[127_ddd_domain_driven_design|Domain-Driven Design]]) - 에릭 에반스
220. [[220_ubiquitous_language_ddd_communication|유비쿼터스 언어]] ([[220_ubiquitous_language_ddd_communication|Ubiquitous Language]]) - 비즈니스와 기술의 공통 언어
221. [[221_bounded_context_ddd_msa_boundary|바운디드 컨텍스트]] ([[221_bounded_context_ddd_msa_boundary|Bounded Context]]) - 경계가 명확한 [[033_context|컨텍스트]]
222. [[222_aggregate_ddd_transaction_consistency|애그리게이트]] ([[222_aggregate_ddd_transaction_consistency|Aggregate]]) - [[001_dikw_pyramid|데이터]] 변경의 단위가 되는 객체 묶음
223. [[223_context_mapping_bounded_context_integration|컨텍스트 매핑]] ([[223_context_mapping_bounded_context_integration|Context Mapping]]) - [[033_context|컨텍스트]] 간의 연동 [[083_relationship_in_er_model|관계]] 정의
224. [[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] ([[549_acl_access_control_list|ACL]], Anti-Corruption Layer)
225. [[306_cqrs|CQRS]] ([[271_command_pattern|Command]] Query Responsibility Segregation) - 명령과 조회 모델 분리
226. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]]) - 상태 변경 이력을 이벤트 스트림으로 저장
227. 아키텍처 평가 기법 개요
228. [[228_saam_software_architecture_analysis_method|SAAM]] ([[201_software_architecture_definition|Software Architecture]] Analysis Method)
229. [[229_atam_architecture_trade_off_analysis_method|ATAM]] ([[319_architecture|Architecture]] Trade-off Analysis Method) - 품질 [[082_attribute_types_er_model|속성]] 간 상충 [[083_relationship_in_er_model|관계]] 분석
230. [[230_cbam_cost_benefit_analysis_method|CBAM]] (Cost Benefit Analysis Method) - 경제적 관점의 평가
231. [[231_adr_architecture_decision_record_documentation|ADR]] ([[231_adr_architecture_decision_record_documentation|Architecture Decision Record]]) - 아키텍처 결정 기록
232. [[232_uml_unified_modeling_language_overview|UML]] ([[232_uml_unified_modeling_language_overview|Unified Modeling Language]]) - OMG 표준 객체지향 모델링 언어
233. [[233_class_diagram_static_structure_uml|클래스 다이어그램]] ([[233_class_diagram_static_structure_uml|Class Diagram]]) - 정적 구조 표현
234. 클래스 간 [[083_relationship_in_er_model|관계]] - 일반화([[234_uml_class_relationships_generalization_dependency|상속]]), 실체화(인터페이스), 의존, 연관, 집합, 합성
235. [[235_sequence_diagram_dynamic_interaction_uml|시퀀스 다이어그램]] ([[235_sequence_diagram_dynamic_interaction_uml|Sequence Diagram]]) - 시간 흐름에 따른 상호작용 (동적)
236. [[236_state_machine_diagram_uml_dynamic|상태 다이어그램]] ([[236_state_machine_diagram_uml_dynamic|State Machine Diagram]]) - 객체의 상태 변화 (동적)
237. [[237_activity_diagram_dynamic_workflow_uml|액티비티 다이어그램]] ([[237_activity_diagram_dynamic_workflow_uml|Activity Diagram]]) - 처리 로직 및 워크플로우 (동적)
238. [[238_use_case_diagram_functional_modeling|유스케이스 다이어그램]] (정적/기능)
239. [[603_component_independent_deployment_unit|컴포넌트]] 다이어그램 / 배치 다이어그램 ([[239_component_deployment_diagram_uml|Deployment Diagram]]) (정적/물리)
240. [[240_communication_collaboration_diagram_uml|통신 다이어그램]] (Communication Diagram / Collaboration Diagram)
241. 패키지 다이어그램 / 복합 구조 다이어그램
242. [[242_solid_object_oriented_design_principles|객체지향 설계 원칙]] ([[242_solid_object_oriented_design_principles|SOLID]])
243. [[243_srp_single_responsibility_principle|SRP]] ([[243_srp_single_responsibility_principle|Single Responsibility Principle]]) - [[355_process|단일 책임 원칙]]
244. [[746_ocp|OCP]] ([[244_ocp_open_closed_principle|Open-Closed Principle]]) - [[356_process|개방-폐쇄 원칙]] (확장엔 열려있고 변경엔 닫혀있음)
245. [[245_lsp_liskov_substitution_principle|LSP]] ([[245_lsp_liskov_substitution_principle|Liskov Substitution Principle]]) - [[357_process|리스코프 치환 원칙]] (자식은 부모를 대체 가능)
246. [[101_isp_information_strategy_planning_4_steps|ISP]] ([[246_isp_interface_segregation_principle|Interface Segregation Principle]]) - [[358_architecture|인터페이스 분리 원칙]]
247. [[247_dip_dependency_inversion_principle|DIP]] ([[247_dip_dependency_inversion_principle|Dependency Inversion Principle]]) - [[359_process|의존 역전 원칙]] ([[198_abstraction_control_data_process|추상화]]에 의존)
248. DRY (Don't Repeat Yourself) 원칙
249. [[249_kiss_keep_it_simple_stupid|KISS]] (Keep It Simple, Stupid) 원칙
250. [[362_yagni|YAGNI]] (You Aren't Gonna Need It) 원칙
251. [[251_design_patterns_gof_overview|디자인 패턴]] ([[251_design_patterns_gof_overview|Design Patterns]]) 개요 - GoF (Gang of Four) 23가지
252. [[252_creational_patterns_overview|생성 패턴]] ([[252_creational_patterns_overview|Creational Patterns]]) - 객체 [[087_process_state_transition|생성]] 메커니즘
253. [[253_singleton_pattern_single_instance|싱글톤]] ([[253_singleton_pattern_single_instance|Singleton]]) - 오직 하나의 인스턴스
254. [[254_factory_method_pattern_subclass_creation|팩토리 메서드]] ([[254_factory_method_pattern_subclass_creation|Factory Method]]) - 서브클래스가 [[087_process_state_transition|생성]]할 객체 결정
255. [[255_abstract_factory_pattern_object_families|추상 팩토리]] ([[255_abstract_factory_pattern_object_families|Abstract Factory]]) - 구체적인 클래스 지정 없이 연관 객체군 [[087_process_state_transition|생성]]
256. [[256_builder_pattern_step_by_step_creation|빌더]] ([[256_builder_pattern_step_by_step_creation|Builder]]) - 복잡한 객체를 단계별로 [[087_process_state_transition|생성]]
257. [[257_prototype_pattern_object_cloning|프로토타입]] ([[257_prototype_pattern_object_cloning|Prototype]]) - 원본 객체를 복사하여 [[087_process_state_transition|생성]]
258. [[258_structural_patterns_overview|구조 패턴]] ([[258_structural_patterns_overview|Structural Patterns]]) - 클래스/객체 조합
259. [[259_adapter_pattern_interface_wrapper|어댑터]] ([[259_adapter_pattern_interface_wrapper|Adapter]]) - 인터페이스 [[344_compatibility_usability|호환성]] 제공
260. [[260_bridge_pattern_abstraction_implementation|브리지]] ([[260_bridge_pattern_abstraction_implementation|Bridge]]) - 구현부에서 추상층을 분리
261. [[261_composite_pattern_tree_structure|컴포지트]] ([[261_composite_pattern_tree_structure|Composite]]) - 부분-전체 트리 구조 (단일 객체/복합 객체 동일 취급)
262. [[262_decorator_pattern_dynamic_wrapper|데코레이터]] ([[262_decorator_pattern_dynamic_wrapper|Decorator]]) - 동적으로 책임(기능) 추가
263. [[263_facade_pattern_simplified_interface|퍼사드]] ([[263_facade_pattern_simplified_interface|Facade]]) - 서브시스템에 대한 단순한 단일 인터페이스 제공
264. [[264_proxy_pattern_surrogate_access_control|프록시]] ([[264_proxy_pattern_surrogate_access_control|Proxy]]) - 대리 객체를 통한 접근 제어
265. [[265_flyweight_pattern_instance_sharing|플라이웨이트]] ([[265_flyweight_pattern_instance_sharing|Flyweight]]) - 인스턴스 공유로 메모리 절약
266. [[266_behavioral_patterns_overview|행위 패턴]] ([[266_behavioral_patterns_overview|Behavioral Patterns]]) - [[001_algorithm_definition|알고리즘]] 및 책임 할당
267. [[267_observer_pattern|옵저버]] ([[267_observer_pattern|Observer]]) - 상태 변화 시 구독자에게 자동 알림
268. [[268_strategy_pattern|전략]] ([[268_strategy_pattern|Strategy]]) - [[001_algorithm_definition|알고리즘]]을 캡슐화하여 동적으로 교체 가능
269. [[269_template_method_pattern|템플릿 메서드]] ([[269_template_method_pattern|Template Method]]) - 상위 클래스는 뼈대, 하위 클래스는 세부 구현
270. [[270_iterator_pattern|이터레이터]] ([[270_iterator_pattern|Iterator]]) - 내부 표현 노출 없이 순차 접근

## 5. 설계 심화 및 시스템 품질 (50개)
271. [[271_command_pattern|커맨드]] ([[271_command_pattern|Command]]) - 요청을 객체로 캡슐화 ([[393_undo|Undo]]/[[234_redo_roll_forward_durability_recovery|Redo]] 지원)
272. [[272_state_pattern|스테이트]] ([[272_state_pattern|State]]) - 상태에 따라 객체 행위 변경
273. [[273_mediator_pattern|중재자]] ([[273_mediator_pattern|Mediator]]) - 객체 간의 복잡한 상호작용을 캡슐화하여 [[195_coupling_levels|결합도]] 저하
274. [[274_memento_pattern|메멘토]] ([[274_memento_pattern|Memento]]) - 객체 상태 저장 및 복원
275. [[275_visitor_pattern|방문자]] ([[275_visitor_pattern|Visitor]]) - 객체 구조 변경 없이 새로운 연산 추가
276. [[276_chain_of_responsibility_pattern|책임 연쇄]] ([[276_chain_of_responsibility_pattern|Chain of Responsibility]]) - 요청을 처리할 수 있는 객체를 찾을 때까지 고리 전달
277. [[277_interpreter_pattern|해석자]] ([[277_interpreter_pattern|Interpreter]]) - 문법 규칙을 정의하고 해석
278. [[278_concurrency_patterns|동시성 패턴]] ([[278_concurrency_patterns|Concurrency Patterns]]) - [[483_active_vs_passive_ftp|Active]] Object, [[229_monitor|Monitor]] Object, [[103_thread_pool|Thread Pool]]
279. [[279_quality_attributes_scenario|아키텍처 품질 속성]] ([[279_quality_attributes_scenario|Quality Attributes]]) - 시나리오 기반 정의
280. 품질 시나리오 요소 - 자극원, 자극, 환경, 대상, 응답, 응답 척도
281. [[452_availability|가용성]] ([[452_availability|Availability]]) - [[352_defect_definition|결함]] 탐지, [[658_ir_recovery|복구]], 예방 전술
282. [[282_performance_tactics|성능]] ([[282_performance_tactics|Performance]]) - 자원 요구 관리, 자원 관리, 스케줄링 전술
283. [[283_security_tactics|보안성]] ([[283_security_tactics|Security]]) - 공격 탐지, 방어, [[658_ir_recovery|복구]] 전술
284. [[346_maintainability_portability|유지보수성]]/변경용이성 ([[284_modifiability_tactics|Modifiability]]) - 국소화, 결합 방지, 의존성 [[015_지연_데이터_관점|지연]]
285. [[285_testability_tactics|시험 용이성]] ([[285_testability_tactics|Testability]]) - 관찰 가능성, 제어 가능성 향상 전술
286. [[286_usability_tactics|사용성]] ([[286_usability_tactics|Usability]]) - 사용자 인터페이스 설계 전술
287. [[287_interoperability_tactics|상호운용성]] ([[084_blockchain_interoperability_polkadot_cosmos|Interoperability]]) - 시스템 간 정보 교환 전술
288. [[288_conceptual_integrity|개념적 무결성]] ([[288_conceptual_integrity|Conceptual Integrity]]) - 아키텍처 전반의 [[194_consistency_database_integrity|일관성]]
289. UI/UX 설계 원칙 - 직관성, 유효성, 학습성, 유연성
290. [[290_nielsen_norman_10_heuristics|니코보코]] ([[290_nielsen_norman_10_heuristics|Nielsen-Norman]]) 10대 [[210_heuristics_scheduling|휴리스틱]] 원칙
291. [[291_information_architecture|정보 아키텍처]] ([[291_information_architecture|Information Architecture]]) 설계
292. [[292_accessibility_kwcag_wcag|접근성]] ([[292_accessibility_kwcag_wcag|Accessibility]]) - [[334_kwcag|KWCAG]], WCAG 웹 [[292_accessibility_kwcag_wcag|접근성]] 지침
293. [[293_responsive_web_design|반응형 웹 디자인]] ([[293_responsive_web_design|Responsive Web Design]])
294. [[294_dark_pattern_avoidance|다크 패턴]] ([[294_dark_pattern_avoidance|Dark Pattern]]) 회피 설계
295. 시스템 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 모델링 - [[149_serial_communication_rs232_rs485|직렬]] 모델, [[430_index_fast_full_scan|병렬]] 모델
296. [[296_fault_tolerance_architecture|결함 허용]] ([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]]) 시스템 설계
297. N-[[288_version_ihl_tos_total_length|버전]] 프로그래밍 ([[297_n_version_programming|N-Version Programming]]) [[071_다중화_Multiplexing|다중화]] 설계
298. [[459_fail_safe|페일 세이프]] ([[459_fail_safe|Fail-Safe]]) - 고장 시 안전한 상태로 유지
299. [[460_fail_soft|페일 소프트]] ([[460_fail_soft|Fail-Soft]]) - 고장 시 기능은 저하되나 시스템 자체는 유지
300. [[300_failover_architecture|페일 오버]] ([[300_failover_architecture|Failover]]) - 장애 시 예비 시스템으로 자동 전환
301. [[301_fault_avoidance_techniques|결함 회피]] ([[301_fault_avoidance_techniques|Fault Avoidance]]) 기법
302. [[302_security_architecture_design|보안 아키텍처]] ([[302_security_architecture_design|Security Architecture]]) 설계
303. [[303_authentication_authorization_patterns|인증]] ([[604_authentication_factors|Authentication]]) 및 [[509_authorization_models_rbac_abac|인가]] ([[509_authorization_models_rbac_abac|Authorization]]) 패턴
304. [[001_dikw_pyramid|데이터]] 암호화 전송 및 저장 패턴
305. [[532_microservices_decomposition_patterns|마이크로서비스]] 설계 - [[014_api_posix|API]] 게이트웨이 패턴
306. [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]]) 패턴
307. [[307_circuit_breaker_pattern|서킷 브레이커]] ([[304_circuit_breaker|Circuit Breaker]]) 패턴 - 연쇄 장애 방지
308. [[308_bulkhead_pattern|벌크헤드]] ([[308_bulkhead_pattern|Bulkhead]]) 패턴 - [[103_thread_pool|스레드 풀]] 격리로 장애 전파 차단
309. [[309_bff_backend_for_frontend_pattern|백엔드 포 프론트엔드]] ([[543_bff_backend_for_frontend|BFF]], [[543_bff_backend_for_frontend|Backend For Frontend]]) 패턴
310. [[310_strangler_fig_pattern|스트랭글러 피그]] ([[310_strangler_fig_pattern|Strangler Fig]]) 패턴 - 레거시를 점진적으로 MSA로 마이그레이션
311. [[311_database_per_service_pattern|데이터베이스 퍼 서비스]] ([[311_database_per_service_pattern|Database per Service]]) 패턴
312. [[312_saga_pattern_choreography_orchestration|사가]] ([[305_saga|Saga]]) 패턴의 코레오그래피 (Choreography) vs [[073_container_orchestration_tools|오케스트레이션]] ([[073_container_orchestration_tools|Orchestration]])
313. [[313_log_aggregation_pattern|로그 취합 아키텍처]] ([[313_log_aggregation_pattern|Log Aggregation Pattern]])
314. [[314_transactional_outbox_pattern|트랜잭셔널 아웃박스]] ([[314_transactional_outbox_pattern|Transactional Outbox]]) 패턴
315. [[239_micro_frontends_architecture|마이크로 프론트엔드]] ([[239_micro_frontends_architecture|Micro Frontends]]) 아키텍처
316. [[316_ssr_vs_csr|서버 사이드 렌더링]] ([[316_ssr_vs_csr|SSR]]) vs 클라이언트 사이드 렌더링 ([[169_pkcs10_csr|CSR]])
317. [[317_spa_single_page_application|단일 페이지 애플리케이션]] (SPA, Single [[286_page_frame|Page]] Application) 설계
318. [[318_pwa_progressive_web_app|프로그레시브 웹 앱]] ([[702_pwa_progressive_web_app_service_worker|PWA]], [[702_pwa_progressive_web_app_service_worker|Progressive Web App]]) 아키텍처
319. [[319_webassembly_architecture|웹어셈블리]] ([[319_webassembly_architecture|WebAssembly]]) 적용 아키텍처
320. [[235_edge_computing_smart_factory|엣지 컴퓨팅]] ([[235_edge_computing_smart_factory|Edge Computing]]) [[136_variance|분산]] 아키텍처 설계

## 6. 구현, 품질 관리 및 유지보수 (70개)
321. 프로그래밍 패러다임 - 절차적, 객체지향, 함수형, [[369_logic_bomb|논리]]형
322. [[322_oop_4_characteristics|객체지향 프로그래밍]] ([[322_oop_4_characteristics|OOP]])의 4대 특징 - 캡슐화, [[234_uml_class_relationships_generalization_dependency|상속]], 다형성, [[198_abstraction_control_data_process|추상화]]
323. [[323_overloading_vs_overriding|오버로딩]] ([[323_overloading_vs_overriding|Overloading]]) vs 오버라이딩 (Overriding)
324. [[324_functional_programming_core|함수형 프로그래밍]] ([[324_functional_programming_core|Functional Programming]]) - 일급 객체, 순수 함수, 불변성
325. [[325_higher_order_function_closure|고차 함수]] ([[325_higher_order_function_closure|Higher-Order Function]]) 및 클로저 (Closure)
326. [[023_lazy_evaluation|지연 평가]] ([[023_lazy_evaluation|Lazy Evaluation]])
327. [[327_reactive_programming|반응형 프로그래밍]] ([[327_reactive_programming|Reactive Programming]]) - [[001_dikw_pyramid|데이터]] 스트림과 변화 전파
328. [[328_coding_convention_style_guide|코딩 컨벤션]] ([[328_coding_convention_style_guide|Coding Convention]]) 및 스타일 가이드
329. [[190_secure_coding_guideline|시큐어 코딩]] ([[190_secure_coding_guideline|Secure Coding]]) 원칙
330. [[330_code_review|코드 리뷰]] ([[330_code_review|Code Review]]) - [[163_peer_review|동료 검토]] ([[163_peer_review|Peer Review]]), 풀 리퀘스트 ([[067_pull_request_pr_merge_request_code_review|PR]]) 기반 검토
331. [[331_static_analysis|정적 분석]] ([[331_static_analysis|Static Analysis]]) - 실행하지 않고 소스코드의 [[352_defect_definition|결함]] 탐지
332. [[332_dynamic_analysis|동적 분석]] ([[332_dynamic_analysis|Dynamic Analysis]]) - 실행 중 [[612_memory_leak_detection|메모리 누수]], [[282_performance_tactics|성능]] 병목 탐지
333. [[333_readability_vs_efficiency|가독성]] ([[333_readability_vs_efficiency|Readability]]) vs 효율성 (Efficiency) 트레이드오프
334. [[334_clean_code_principles|클린 코드]] ([[334_clean_code_principles|Clean Code]]) 원칙 - 의미 있는 이름, 작고 단일 역할의 함수, 주석의 최소화
335. [[100_technical_debt_monitoring_release_policy|기술 부채]] ([[100_technical_debt_monitoring_release_policy|Technical Debt]])의 관리 및 상환 [[268_strategy_pattern|전략]]
336. [[336_library_vs_framework|라이브러리]] ([[336_library_vs_framework|Library]]) vs 프레임워크 (Framework) - 제어의 역전 (IoC, Inversion of Control) 차이
337. [[337_dependency_injection|의존성 주입]] ([[190_enterprise_di_framework_lifecycle|DI]], [[337_dependency_injection|Dependency Injection]]) - 객체 [[195_coupling_levels|결합도]] 감소
338. [[338_aspect_oriented_programming|관점 지향 프로그래밍]] (AOP, [[338_aspect_oriented_programming|Aspect Oriented Programming]]) - 횡단 관심사(Cross-cutting Concern) 분리
339. [[339_software_quality_definition|소프트웨어 품질]] ([[339_software_quality_definition|Software Quality]])의 정의 (명시적, 묵시적 요구사항 충족)
340. ISO/IEC 9126 품질 특성 - 기능성, [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]], [[286_usability_tactics|사용성]], 효율성, [[346_maintainability_portability|유지보수성]], 이식성
341. ISO/IEC 25010 ([[341_iso_iec_25010|SQuaRE]]) - 9126의 진화 모델 ([[283_security_tactics|보안성]], [[344_compatibility_usability|호환성]] 추가)
342. [[342_functional_suitability|기능 적합성]] ([[342_functional_suitability|Functional Suitability]])
343. [[343_performance_efficiency|성능 효율성]] ([[343_performance_efficiency|Performance Efficiency]])
344. [[344_compatibility_usability|호환성]] ([[344_compatibility_usability|Compatibility]]) / [[286_usability_tactics|사용성]] ([[286_usability_tactics|Usability]])
345. [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] ([[345_reliability_security|Reliability]]) / [[283_security_tactics|보안성]] ([[283_security_tactics|Security]])
346. [[346_maintainability_portability|유지보수성]] ([[346_maintainability_portability|Maintainability]]) / 이식성 (Portability)
347. [[347_quality_in_use|사용 품질]] ([[347_quality_in_use|Quality in Use]]) - 유효성, 생산성, 만족도, [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 완화
348. [[348_mccall_quality_model|맥콜]]([[348_mccall_quality_model|McCall]])의 품질 모델 - 제품 운영, 제품 수정, 제품 전이 관점
349. [[349_cost_of_quality|품질 비용]] (COQ, [[349_cost_of_quality|Cost of Quality]]) - 예방 비용, 평가 비용, 내부 실패 비용, 외부 실패 비용
350. [[350_total_quality_management|전사적 품질 관리]] (TQM, [[350_total_quality_management|Total Quality Management]])
351. [[351_six_sigma|식스 시그마]] ([[351_six_sigma|6 Sigma]]) - DMAIC (Define, Measure, Analyze, Improve, Control)
352. [[352_defect_definition|결함]]([[352_defect_definition|Defect]])의 정의 - 오류(Error/Mistake), 결점(Fault/Bug), 고장/실패(Failure)
353. [[352_defect_definition|결함]] 생명주기 - 발생, 등록, 분석, 할당, 수정, 조치 [[396_validation|확인]], 종료
354. [[354_defect_severity_priority|결함 심각도]] ([[354_defect_severity_priority|Severity]]) vs [[352_defect_definition|결함]] 우선순위 (Priority)
355. [[355_defect_density|결함 밀도]] ([[355_defect_density|Defect Density]]) - 코드 규모(KLOC) 대비 [[352_defect_definition|결함]] 수
356. [[356_software_reliability_growth_model|신뢰성 성장 모델]] (SRGM, Software [[345_reliability_security|Reliability]] Growth Model) - 고장 시간, 고장 간격 모델링
357. [[452_availability|가용성]] ([[452_availability|Availability]]) 계산 = [[450_mtbf|MTBF]] / ([[450_mtbf|MTBF]] + [[451_mttr|MTTR]])
358. [[450_mtbf|MTBF]] (Mean Time Between Failures) - [[450_mtbf|평균 무고장 시간]]
359. [[451_mttr|MTTR]] (Mean Time To Repair) - [[451_mttr|평균 수리 시간]]
360. [[360_mttf|MTTF]] (Mean Time To Failure) - 평균 고장 시간
361. 소프트웨어 복잡도 측정 - 맥케이브 순환 복잡도 (McCabe's Cyclomatic Complexity, V(G) = e - n + 2)
362. [[362_halstead_complexity|할스테드]] ([[362_halstead_complexity|Halstead]]) 복잡도 - 연산자([[565_operator_pattern_kubernetes_automation|Operator]])와 [[160_operand|피연산자]]([[160_operand|Operand]]) 수 기반 측정
363. [[363_ck_metrics|객체지향 메트릭]] (CK [[342_routing_metric_hop_bandwidth_delay|메트릭]]스) - WMC, DIT, [[367_noc|NOC]], CBO, RFC, LCOM
364. [[647_ftr_formal_technical_review_inspection_walkthrough|정형 기술 검토]] ([[647_ftr_formal_technical_review_inspection_walkthrough|FTR]], [[364_formal_technical_review|Formal Technical Review]]) 의 지침
365. [[365_sqa|소프트웨어 품질 보증]] ([[365_sqa|SQA]], [[339_software_quality_definition|Software Quality]] Assurance) 조직 및 활동
366. [[366_gqm|골-질문-메트릭]] ([[366_gqm|GQM]], Goal-Question-Metric) 접근법 - 측정 지표 도출 기법
367. [[367_quality_dashboard|품질 대시보드]] ([[367_quality_dashboard|Quality Dashboard]]) 구축
368. [[368_spc|통계적 공정 관리]] ([[203_spc_signed_public_key_challenge|SPC]], Statistical [[300_process|Process]] Control) 및 정량적 관리
369. [[369_spi_ideal_model|소프트웨어 프로세스 개선]] ([[159_spi_schedule_performance_index|SPI]]) 프레임워크 - IDEAL 모델
370. [[370_code_smell|코드 스멜]] ([[365_5_solid_code_smell|Code Smell]]) - [[213_refactoring_cloud_native_rearchitecture|리팩토링]]의 징후 (코드 중복, 거대 클래스, 긴 파라미터 목록)
371. [[371_technical_fragmentation|기술적 단편화]] ([[371_technical_fragmentation|Technical Fragmentation]]) 문제
372. [[372_cots|상용 소프트웨어]] ([[372_cots|COTS]], Commercial Off-The-Shelf) 통합 및 품질
373. [[373_oss_governance|오픈 소스 소프트웨어]] ([[191_oss_license_compliance|OSS]]) 거버넌스 - 라이선스(GPL, MIT, Apache 등) 컴플라이언스
374. [[374_supply_chain_security|공급망 보안]] ([[374_supply_chain_security|Supply Chain Security]]) - [[191_oss_license_compliance|오픈소스]] 취약점 관리
375. [[890_sbom_cyclonedx_spdx|SBOM]] (Software [[124_bom_bill_of_materials|Bill of Materials]]) - 소프트웨어 구성 요소 명세서 의무화 동향
376. 소프트웨어 빌드 및 배포 자동화의 품질 [[395_verification_process_review|검증]] 단계
377. [[112_checksum|체크섬]]([[112_checksum|Checksum]]), 서명(Signature)을 통한 [[003_integrity|무결성]]([[003_integrity|Integrity]]) [[395_verification_process_review|검증]]
378. [[378_software_documentation|소프트웨어 문서화]] ([[378_software_documentation|Documentation]]) 표준 및 지식 관리 (Wiki, Confluence)
379. [[379_dr_architecture|재해 복구]] ([[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]]) 아키텍처 - [[176_rto_recovery_time_objective|RTO]] ([[176_rto_recovery_time_objective|Recovery Time Objective]]), [[177_rpo_recovery_point_objective|RPO]] ([[177_rpo_recovery_point_objective|Recovery Point Objective]])
380. 소프트웨어 유지보수의 종류 - 수정([[380_maintenance_types|Corrective]]), 적응(Adaptive), 완전/개선(Perfective), 예방(Preventive)
381. 메이먼의 법칙 (Lehman's Laws of Software Evolution) - 지속적 변경, 복잡도 증가의 법칙
382. [[382_defensive_programming|방어적 프로그래밍]] ([[382_defensive_programming|Defensive Programming]]) - 예외 처리, Assertion 적극 활용
383. [[383_data_centric_architecture|데이터 중심]]([[383_data_centric_architecture|Data-Centric]]) 아키텍처의 품질 보증
384. [[190_ai_llm_requirements_specification|AI]] 기반 코드 [[087_process_state_transition|생성]]기(Copilot 등) 산출물의 품질 평가 한계
385. [[206_serverless_cold_start|서버리스]] 환경의 [[559_serverless_cold_start_mitigation|콜드 스타트]]([[347_cold_start_problem|Cold Start]]) 모니터링 및 튜닝
386. [[386_sustainability_green_coding|지속 가능성]] ([[386_sustainability_green_coding|Sustainability]]) 및 그린 코딩 (Green Coding) - 탄소 배출 저감 코드
387. [[387_access_control_pattern|접근 통제]] ([[547_access_control_rwx|Access Control]]) 패턴 로직 구현
388. [[388_design_by_contract|디자인 바이 컨트랙트]] ([[388_design_by_contract|Design by Contract]]) - 사전조건, 사후조건, 불변조건 명시
389. [[389_reverse_engineering|리버스 엔지니어링]] ([[780_reverse_engineering|Reverse Engineering]]) 툴을 통한 [[528_obfuscation_anti_debugging_mobile|난독화]] 코드 분석
390. [[390_application_lifecycle_management|애플리케이션 라이프사이클 관리]] ([[390_application_lifecycle_management|ALM]]) 시스템 도입

## 7. 소프트웨어 테스팅 및 [[395_verification_process_review|검증]] 심화 (80개)
391. 소프트웨어 테스팅의 7가지 원리 ([[352_defect_definition|결함]] 발견, 완벽한 테스트 불가능, 조기 테스트, [[352_defect_definition|결함]] 집중, [[392_pesticide_paradox_test_renewal|살충제 패러독스]], 정황 의존, [[393_absence_of_errors_fallacy|오류 부재의 궤변]])
392. [[392_pesticide_paradox_test_renewal|살충제 패러독스]] ([[392_pesticide_paradox_test_renewal|Pesticide Paradox]]) 극복을 위한 [[441_test_case|테스트 케이스]] 주기적 갱신
393. [[393_absence_of_errors_fallacy|오류 부재의 궤변]] (Absence of Errors Fallacy) - 요구사항 미충족 시 [[352_defect_definition|결함]]이 없어도 무용지물
394. V-모델의 매핑 (요구사항-인수테스트, 기본설계-시스템테스트, 상세설계-통합테스트, 코딩-단위테스트)
395. [[395_verification_process_review|검증]] ([[395_verification_process_review|Verification]]) - 제품을 올바르게 만들고 있는가 (과정, 산출물 리뷰)
396. [[396_validation|확인]] ([[396_validation|Validation]]) - 올바른 제품을 만들었는가 (결과, 실행 테스트)
397. [[397_unit_test|단위 테스트]] ([[397_unit_test|Unit Test]]) - 최소 단위([[192_module_independence|모듈]]/함수) 기능 [[395_verification_process_review|검증]], 화이트박스 위주
398. [[398_unit_test_framework_xunit|단위 테스트 프레임워크]] (JUnit, pytest, NUnit 등)
399. [[399_mock_object|목 객체]] ([[399_mock_object|Mock Object]]) 기반 격리 테스트
400. [[400_integration_testing|통합 테스트]] ([[400_integration_testing|Integration Test]]) - [[192_module_independence|모듈]] 간 인터페이스 및 상호작용 [[395_verification_process_review|검증]]
401. [[401_big_bang_integration|빅뱅 통합]] ([[401_big_bang_integration|Big Bang Integration]]) - 한 번에 모두 결합 (오류 추적 어려움)
402. [[402_top_down_integration|하향식 통합]] ([[402_top_down_integration|Top-down]] Integration) - 깊이/넓이 우선, 하위 [[192_module_independence|모듈]] 대체용 [[460_stub_test_double|스텁]]([[460_stub_test_double|Stub]]) 사용
403. [[403_bottom_up_integration|상향식 통합]] ([[403_bottom_up_integration|Bottom-up]] Integration) - 클러스터 결합, 상위 제어 [[192_module_independence|모듈]] 대체용 드라이버(Driver) 사용
404. [[404_sandwich_integration|샌드위치 통합]] (Sandwich / Hybrid Integration) - 주요 [[192_module_independence|모듈]] 중심 상/하향 병행
405. [[405_system_test|시스템 테스트]] ([[405_system_test|System Test]]) - 전체 시스템의 기능 및 [[133_non_functional_requirements|비기능 요구사항]] [[395_verification_process_review|검증]]
406. [[406_acceptance_test_uat|인수 테스트]] ([[406_acceptance_test_uat|Acceptance Test]]) - 사용자(고객)가 요구사항 충족 여부 최종 [[396_validation|확인]]
407. [[407_alpha_test|알파 테스트]] ([[407_alpha_test|Alpha Test]]) - 개발자 환경에서 통제된 사용자 테스트
408. [[408_beta_test|베타 테스트]] ([[408_beta_test|Beta Test]]) - 실제 환경에서 다수 사용자가 수행 (필드 테스트)
409. [[707_oat_operational_acceptance_testing|OAT]] ([[409_operational_acceptance_testing_oat|Operational Acceptance Testing]]) - 운영 전환 전 [[555_backup_and_restore_strategy|백업]], [[456_dual_redundancy|이중화]] 등 [[395_verification_process_review|검증]]
410. [[410_regression_test|회귀 테스트]] ([[410_regression_test|Regression Test]]) - 코드 수정 후 기존 기능에 예기치 않은 [[352_defect_definition|결함]](사이드 이펙트) 발생 [[396_validation|확인]]
411. 리그레션 테스트 자동화 및 선택적 수행 (Retest All vs Selective)
412. [[412_black_box_testing|블랙박스 테스트]] ([[412_black_box_testing|Black-box Test]] / 명세 기반 테스트) - 내부 구조를 보지 않고 입력/출력 기반 [[395_verification_process_review|검증]]
413. [[630_equivalence_partitioning_boundary_value_analysis|동등 분할]] ([[630_equivalence_partitioning_boundary_value_analysis|Equivalence Partitioning]]) - 입력 영역을 유효/무효 클래스로 분할하여 대푯값 테스트
414. [[414_boundary_value_analysis|경계값 분석]] ([[414_boundary_value_analysis|Boundary Value Analysis]]) - 경계 부분에서 [[352_defect_definition|결함]]이 많다는 점 이용 (분할의 가장자리 값)
415. [[415_decision_table|의사 결정 테이블]] ([[631_decision_table_logical_combination|Decision Table]]) - 복잡한 [[369_logic_bomb|논리]]적 조건들의 조합을 표로 구성하여 테스트
416. [[416_state_transition_testing|상태 전이 테스트]] ([[416_state_transition_testing|State Transition Testing]]) - 객체의 상태 변화 시나리오 [[395_verification_process_review|검증]]
417. [[417_use_case_testing|유스케이스 테스팅]] ([[417_use_case_testing|Use Case Testing]]) - 액터와의 상호작용 흐름 기반
418. [[418_pairwise_testing|페어와이즈 테스팅]] ([[418_pairwise_testing|Pairwise Testing]]) - 변수 값들의 모든 쌍(Pair) 조합이 최소 한 번 테스트되도록 최적화 (조합 폭발 방지)
419. [[419_cause_effect_graphing|원인-결과 그래프]] ([[419_cause_effect_graphing|Cause-Effect Graphing]])
420. [[420_whitebox_testing|화이트박스 테스트]] (White-box Test / 구조 기반 테스트) - 소스코드의 내부 [[369_logic_bomb|논리]] 구조를 모두 [[395_verification_process_review|검증]]
421. [[421_control_flow_testing|제어 흐름 테스트]] ([[421_control_flow_testing|Control Flow Testing]])
422. [[422_statement_coverage|구문 커버리지]] ([[422_statement_coverage|Statement Coverage]]) - 코드의 모든 문장을 최소 한 번 실행
423. [[423_decision_coverage|결정 커버리지]] ([[423_decision_coverage|Decision Coverage]] / 분기 커버리지) - 분기문(If, While 등)의 참/거짓을 최소 한 번씩 실행
424. [[424_condition_coverage|조건 커버리지]] ([[424_condition_coverage|Condition Coverage]]) - 분기문 내의 각 개별 조건식이 참/거짓을 한 번씩 가짐
425. 조건/[[423_decision_coverage|결정 커버리지]] (Condition/[[423_decision_coverage|Decision Coverage]]) - 개별 조건과 전체 결정이 모두 참/거짓을 가짐
426. 변경 조건/[[423_decision_coverage|결정 커버리지]] (MC/DC, Modified Condition/[[423_decision_coverage|Decision Coverage]]) - 각 개별 조건이 독립적으로 전체 결과에 영향을 미침을 증명 (DO-178B/C 항공/안전 표준)
427. [[427_multiple_condition_coverage|다중 조건 커버리지]] ([[427_multiple_condition_coverage|Multiple Condition Coverage]]) - 개별 조건의 모든 가능한 진리값 조합 (2^N)
428. [[428_path_coverage|경로 커버리지]] ([[428_path_coverage|Path Coverage]]) - 가능한 모든 실행 경로를 테스트
429. [[429_data_flow_testing|데이터 흐름 테스팅]] ([[429_data_flow_testing|Data Flow Testing]]) - 변수의 정의(Define)와 사용(Use) 경로 (DU 경로) 기반 [[395_verification_process_review|검증]]
430. [[430_static_testing|정적 테스팅]] ([[430_static_testing|Static Testing]]) - 코드를 실행하지 않고 리뷰나 도구를 통해 [[395_verification_process_review|검증]] ([[161_inspection_formal_review|인스펙션]], [[331_static_analysis|정적 분석]])
431. [[431_dynamic_testing|동적 테스팅]] ([[431_dynamic_testing|Dynamic Testing]]) - 코드를 직접 컴파일하고 실행하여 [[395_verification_process_review|검증]]
432. [[432_risk_based_testing|리스크 기반 테스팅]] ([[432_risk_based_testing|Risk-based Testing]]) - 비즈니스 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]가 높은 [[192_module_independence|모듈]]에 테스트 자원 집중
433. [[433_exploratory_testing|탐색적 테스팅]] ([[433_exploratory_testing|Exploratory Testing]]) - 명세서 없이 테스터의 직관과 경험을 바탕으로 테스트 설계와 수행을 동시 [[216_progress_in_synchronization|진행]] (차터, 타임박스 활용)
434. [[434_error_guessing|오류 추정]] ([[434_error_guessing|Error Guessing]]) - 테스터의 경험을 바탕으로 [[352_defect_definition|결함]]이 발생할 만한 곳을 추정하여 테스트
435. [[435_checklist_based_testing|체크리스트]] ([[435_checklist_based_testing|Checklist]]) 기반 테스팅
436. [[436_test_oracle|테스트 오라클]] ([[436_test_oracle|Test Oracle]]) - 테스트 결과의 참/거짓을 판단하기 위한 기준
437. [[437_true_oracle|참 오라클]] ([[437_true_oracle|True Oracle]]) - 모든 입력에 대해 기대 결과 제공 (현실적 적용 어려움)
438. [[438_sampling_oracle|샘플링 오라클]] ([[438_sampling_oracle|Sampling Oracle]]) - 특정 몇몇 입력 값에 대해서만 결과 제공
439. [[439_heuristic_oracle|휴리스틱 오라클]] ([[439_heuristic_oracle|Heuristic Oracle]]) - 샘플링에 직관적/경험적 판단 추가
440. [[440_consistent_oracle|일관성 오라클]] ([[440_consistent_oracle|Consistent Oracle]]) - 변경 전/후의 결과가 동일한지 [[396_validation|확인]] ([[410_regression_test|회귀 테스트]]에 유용)
441. [[441_test_case|테스트 케이스]] ([[441_test_case|Test Case]]) 구조 - [[289_identification_flags_fragmentation_offset|식별자]], 전제조건, 입력 [[001_dikw_pyramid|데이터]], 기대 결과
442. [[442_test_scenario|테스트 시나리오]] ([[442_test_scenario|Test Scenario]]) - [[441_test_case|테스트 케이스]]들을 흐름에 따라 묶은 집합
443. [[443_test_procedure|테스트 절차]] ([[443_test_procedure|Test Procedure]]) / 테스트 스크립트 (Test Script)
444. [[444_test_data_management|테스트 데이터]] ([[444_test_data_management|Test Data]]) [[087_process_state_transition|생성]] 및 익명화 관리 ([[444_test_data_management|Test Data Management]], TDM)
445. [[445_performance_test_types|성능 테스트]] ([[445_performance_test_types|Performance Test]]) 4가지 유형
446. [[446_load_test|부하 테스트]] ([[446_load_test|Load Test]]) - 시스템의 임계점(목표치)까지 부하를 증가시키며 상태 [[396_validation|확인]]
447. [[447_stress_test|스트레스 테스트]] ([[447_stress_test|Stress Test]]) - 임계점 이상의 과부하 상태에서 시스템 붕괴 및 [[658_ir_recovery|복구]] 반응 [[396_validation|확인]]
448. [[448_spike_test|스파이크 테스트]] ([[448_spike_test|Spike Test]]) - 갑작스럽게 사용자가 급증할 때의 반응 [[396_validation|확인]]
449. [[449_endurance_soak_test|내구성 테스트]] (Endurance / Soak Test) - 장시간 부하를 주어 [[612_memory_leak_detection|메모리 누수]](Leak) 등 [[396_validation|확인]]
450. [[450_benchmark_test|벤치마크 테스트]] ([[624_bmt_procedure|BMT]], [[450_benchmark_test|Benchmark Test]]) - 동일한 환경에서 여러 제품의 [[282_performance_tactics|성능]]을 비교
451. [[451_usability_test|사용성 테스트]] ([[451_usability_test|Usability Test]]) - 사용자가 시스템을 얼마나 쉽게 다룰 수 있는지 UI/UX 관점 평가
452. A/B 테스트 - 두 가지 UI/기능을 실 사용자에게 노출하여 반응 비교
453. [[453_compatibility_test|호환성 테스트]] ([[453_compatibility_test|Compatibility Test]]) - OS, 브라우저, 기기(모바일) 등 이기종 환경 동작 [[396_validation|확인]]
454. [[454_portability_test|이식성 테스트]] ([[454_portability_test|Portability Test]]) - 다른 환경으로 시스템을 이전했을 때의 동작 [[396_validation|확인]]
455. [[455_penetration_testing_vulnerability_scanning|모의 해킹]] ([[676_penetration_testing|Penetration Testing]]) 및 취약점 스캐닝
456. [[456_mutation_testing|뮤테이션 테스팅]] ([[456_mutation_testing|Mutation Testing]] / [[638_mutation_testing_test_case_verification|돌연변이]] 테스팅) - 원본 코드에 고의로 에러([[638_mutation_testing_test_case_verification|돌연변이]])를 주입하여 기존 [[441_test_case|테스트 케이스]]가 이를 잡아내는지(Kill) [[395_verification_process_review|검증]] ([[441_test_case|테스트 케이스]]의 품질 평가)
457. [[457_fuzz_testing|퍼즈 테스팅]] ([[457_fuzz_testing|Fuzz Testing]] / Fuzzing) - 무작위 또는 기형적인 [[001_dikw_pyramid|데이터]]를 입력하여 크래시(Crash)나 예외 상황 유발
458. [[367_test_double_isolation|테스트 더블]] ([[458_test_double|Test Double]]) 5가지 개념 (xUnit 테스트 패턴)
459. [[459_dummy_test_double|Dummy]] ([[459_dummy_test_double|더미]]) - 인자 채우기용, 실제 사용 안됨
460. [[460_stub_test_double|Stub]] ([[460_stub_test_double|스텁]]) - 호출 시 준비된 답변만 반환 (상태 [[395_verification_process_review|검증]]용)
461. [[461_spy_test_double|Spy]] ([[461_spy_test_double|스파이]]) - [[460_stub_test_double|스텁]] 역할 + 호출 정보 기록
462. [[462_mock_test_double|Mock]] (목) - 행위(Behavior) [[395_verification_process_review|검증]]을 위해 예상되는 호출 명세가 프로그래밍된 객체
463. [[463_fake_test_double|Fake]] ([[463_fake_test_double|페이크]]) - 실제 동작하지만 프로덕션에는 적합하지 않은 축소판 (인메모리 DB 등)
464. [[464_service_virtualization|서비스 가상화]] ([[464_service_virtualization|Service Virtualization]]) - [[619_msa_traffic_hardware|MSA]] 환경에서 외부 의존 API를 모사하는 [[460_stub_test_double|스텁]] 서버
465. [[465_continuous_testing|지속적 테스팅]] ([[465_continuous_testing|Continuous Testing]]) - [[090_configuration_item|CI]]/CD 파이프라인 전 과정에 테스트 자동화 통합
466. [[466_shift_left_testing|시프트 레프트 테스팅]] ([[466_shift_left_testing|Shift-Left Testing]]) - 테스트 활동을 개발 [[459_quic_fec_forward_error_correction|초기]](왼쪽) 단계로 당겨 [[352_defect_definition|결함]] 조기 발견
467. [[467_shift_right_testing|시프트 라이트 테스팅]] ([[467_shift_right_testing|Shift-Right Testing]]) - 운영 환경(오른쪽)에서의 테스트 ([[595_canary_stack_smashing_protector|카나리]], [[751_chaos_engineering|카오스 엔지니어링]])
468. [[468_testing_in_production|운영 환경 테스트]] ([[468_testing_in_production|Testing in Production]] / TiP)
469. [[469_model_based_testing_mbt|모델 기반 테스팅]] (MBT, Model-Based Testing) - 시스템 모델([[232_uml_unified_modeling_language_overview|UML]] 등)에서 [[441_test_case|테스트 케이스]] 자동 [[087_process_state_transition|생성]]
470. [[164_tdd_test_driven_development|TDD]] ([[470_tdd_lifecycle|Test Driven Development]]) 생명주기 - 실패하는 테스트 작성(Red) -> 통과하는 최소 코드 작성(Green) -> [[213_refactoring_cloud_native_rearchitecture|리팩토링]]([[213_refactoring_cloud_native_rearchitecture|Refactor]])

## 8. SW 보안 ([[653_devsecops_shift_left|DevSecOps]]) 및 컴플라이언스 (60개)
471. [[471_secure_sdlc|소프트웨어 개발 보안]] ([[471_secure_sdlc|Secure SDLC]]) - 기획, 설계, 구현, 테스트 전 단계 보안 활동
472. [[472_bsimm_maturity_model|BSIMM]] (Building [[283_security_tactics|Security]] In [[011_maturity_model|Maturity Model]]) - SW 보안 성숙도 평가 모델
473. [[473_ms_sdl|Microsoft SDL]] ([[473_ms_sdl|Security Development Lifecycle]]) - 7단계 보안 생명주기
474. [[611_threat_modeling|위협 모델링]] ([[611_threat_modeling|Threat Modeling]]) 아키텍처 보안 분석
475. [[097_stride_convolutional_neural_network_downsampling|STRIDE]] 모델 - [[598_spoofing|Spoofing]], Tampering, Repudiation, Information Disclosure, Denial of [[090_service_kubernetes_network_load_balancing|Service]], Elevation of Privilege
476. DREAD 모델 - 위협 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 산정 지표 (Damage, Reproducibility, Exploitability, Affected users, Discoverability)
477. [[416_owasp_top_10|OWASP Top 10]] ([[477_owasp_top_10_2021|2021]] 기준 주요 취약점)
478. [[417_broken_access_control|Broken Access Control]] ([[417_broken_access_control|취약한 접근 제어]])
479. [[424_cryptographic_failures|Cryptographic Failures]] ([[479_cryptographic_failures|암호화 실패]] / 민감 [[001_dikw_pyramid|데이터]] 노출)
480. [[480_injection|Injection]] ([[480_injection|인젝션]] / SQLi, OS [[271_command_pattern|Command]], [[035_nosql|NoSQL]] 등)
481. [[440_insecure_design|Insecure Design]] ([[481_insecure_design|안전하지 않은 설계]])
482. [[412_security_misconfiguration|Security Misconfiguration]] ([[482_security_misconfiguration|보안 설정 오류]])
483. Vulnerable and Outdated Components ([[483_vulnerable_and_outdated_components|취약하고 만료된 컴포넌트]])
484. [[289_identification_flags_fragmentation_offset|Identification]] and [[454_authentication_failures|Authentication Failures]] ([[303_authentication_authorization_patterns|인증]] 및 [[507_session_management_security|세션 관리]] 실패)
485. Software and [[001_dikw_pyramid|Data]] [[461_integrity_failures|Integrity Failures]] (소프트웨어 및 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] 실패)
486. [[526_security_logging|Security Logging]] and Monitoring Failures ([[526_security_logging_and_monitoring_failures|보안 로깅]] 및 모니터링 실패)
487. [[468_ssrf|SSRF]] ([[487_ssrf_server_side_request_forgery|Server-Side Request Forgery]]) - 서버 측 요청 위조
488. [[410_cwe_taxonomy|CWE]] ([[410_cwe_taxonomy|Common Weakness Enumeration]]) - 보안 약점 사전
489. [[409_cve_lifecycle|CVE]] (Common Vulnerabilities and Exposures) - 공개된 보안 취약점 목록
490. [[407_cvss_scoring|CVSS]] (Common Vulnerability Scoring System) - 취약점 위험도 평가 점수 (0~[[489_raid_10_hybrid|10]])
491. [[491_sast_static_analysis|SAST]] (Static Application [[283_security_tactics|Security]] Testing) - 소스코드 [[331_static_analysis|정적 분석]] 도구 (보안 룰셋 기반)
492. [[492_dast_dynamic_analysis|DAST]] (Dynamic Application [[283_security_tactics|Security]] Testing) - 런타임 환경에 공격 페이로드 주입 분석 (블랙박스)
493. [[493_iast_interactive_analysis|IAST]] (Interactive Application [[283_security_tactics|Security]] Testing) - SAST와 [[492_dast_dynamic_analysis|DAST]] 결합, 에이전트 기반 내부 메모리/흐름 분석
494. [[494_rasp_runtime_protection|RASP]] ([[494_rasp_runtime_protection|Runtime Application Self-Protection]]) - 실행 환경 내부에서 공격 실시간 방어
495. [[453_sca|SCA]] ([[495_sca_software_composition_analysis|Software Composition Analysis]]) - [[191_oss_license_compliance|오픈소스]] [[336_library_vs_framework|라이브러리]] 취약점 및 라이선스 스캔
496. [[890_sbom_cyclonedx_spdx|SBOM]] (Software [[124_bom_bill_of_materials|Bill of Materials]]) 포맷 - SPDX, CycloneDX
497. 행정안전부/KISA [[471_secure_sdlc|소프트웨어 개발 보안]] 가이드 ([[497_kisa_secure_coding_guide|47개 보안 약점]])
498. 입력 [[001_dikw_pyramid|데이터]] [[395_verification_process_review|검증]] 및 표현 ([[601_input_validation|Input Validation]]) 원칙
499. SQL [[480_injection|인젝션]] 방어 - Prepared Statement ([[499_sql_injection_defense|파라미터화된 쿼리]]), ORM 프레임워크 사용
500. [[500_xss_defense_escaping_csp|크로스 사이트 스크립팅]] ([[726_xss_cross_site_scripting_types|XSS]]) 방어 - 입/출력값 인코딩, [[475_csp|CSP]]([[475_csp|Content Security Policy]]) 헤더 [[009_config|설정]]
501. [[726_xss_cross_site_scripting_types|XSS]] 유형 - [[471_reflected_xss|Reflected XSS]], [[472_stored_xss|Stored XSS]], [[473_dom_xss|DOM-based XSS]]
502. 크로스 사이트 요청 위조 ([[728_csrf_cross_site_request_forgery_concept|CSRF]]) 방어 - Anti-[[728_csrf_cross_site_request_forgery_concept|CSRF]] 토큰 발급, SameSite [[475_cookie_local_state|쿠키]] [[082_attribute_types_er_model|속성]]
503. [[503_security_features_design|보안 기능]] ([[503_security_features_design|Security Features]])의 설계
504. [[504_cryptography_algorithms_aes_rsa_sha|암호화 알고리즘]] (대칭키-AES, 비대칭키-RSA/[[554_ecc_circuit|ECC]], 일방향-SHA) 적용 기준
505. 비밀번호 저장 방식 - [[144_hkdf_tls_1_3|KDF]]([[505_password_storage_kdf_salt|Key Derivation Function]]) 활용 (PBKDF2, bcrypt, scrypt, Argon2) 및 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]]) 적용
506. [[183_post_quantum_cryptography_key_transition|양자 내성 암호]] ([[351_quantum_computing_pqc_transition|PQC]]) 전환 대비 SW 아키텍처 검토
507. [[507_session_management_security|세션 관리]] ([[507_session_management_security|Session Management]]) 보완 - 만료 시간, 재사용 방지, [[160_session_controlling_terminal|세션]] ID 추측 난해성
508. [[303_authentication_authorization_patterns|인증]] ([[604_authentication_factors|Authentication]]) 트렌드 - [[552_mfa|MFA]], FIDO, WebAuthn, 패스워드리스(Passwordless)
509. [[509_authorization_models_rbac_abac|인가]] ([[509_authorization_models_rbac_abac|Authorization]]) 모델 - [[569_rbac|RBAC]](역할 기반), [[572_abac|ABAC]]([[082_attribute_types_er_model|속성]] 기반, 조건부 규칙)
510. [[014_api_posix|API]] 보안 관리 - OAuth 2.0 (Access Token [[509_authorization_models_rbac_abac|인가]]), [[537_oidc_openid_connect|OIDC]]([[303_authentication_authorization_patterns|인증]]), [[549_jwt_json_web_token|JWT]]([[549_jwt_json_web_token|JSON Web Token]]) 서명/만료 [[395_verification_process_review|검증]]
511. [[511_api_rate_limiting_throttling|API Rate Limiting]] ([[511_api_rate_limiting_throttling|비율 제한]]) 및 Throttling (스로틀링) - DDoS 및 크롤링 방어
512. [[512_mtls_service_to_service_security|마이크로서비스 간 보안]] ([[512_mtls_service_to_service_security|Service-to-Service Security]]) - [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] (상호 [[694_thread_local_storage_tls|TLS]] [[303_authentication_authorization_patterns|인증]])
513. [[513_container_security|컨테이너 보안]] - 이미지 스캐닝, 루트 권한 실행 금지 ([[513_container_security|Non-root user]]), [[061_namespace|네임스페이스]] 샌드박스
514. [[514_secret_management_vault_kms|시크릿]]([[514_secret_management_vault_kms|Secret]]) 관리 도구 - 하드코딩 금지, HashiCorp [[567_vault|Vault]], AWS Secrets Manager 활용
515. [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] ([[205_kubernetes_container_orchestration|Kubernetes]]) 보안 - [[569_rbac|RBAC]], Network [[164_policy|Policy]], [[198_pod_kubernetes_minimum_deployment_unit|Pod]] [[283_security_tactics|Security]] Admission
516. [[781_personal_information|개인정보]] [[571_protection_vs_security|보호]] 중심 설계 ([[060_privacy_by_design|Privacy by Design]] - [[060_privacy_by_design|PbD]]) 7원칙
517. [[001_dikw_pyramid|데이터]] 3법 및 [[791_gdpr_eu|GDPR]] 컴플라이언스 대응 SW 기능 (잊혀질 권리, 동의 철회 기능)
518. 가명 처리 및 비식별화 기술 (K-익명성, L-다양성, T-근접성) SW 적용
519. [[519_cyber_resilience_architecture|사이버 레질리언스]] ([[519_cyber_resilience_architecture|Cyber Resilience]]) 아키텍처
520. [[520_supply_chain_attack_and_ci_cd_security|공급망]] ([[520_supply_chain_attack_and_ci_cd_security|Supply Chain]]) 공격 사례 및 서명된 커밋(Signed Commit), [[090_configuration_item|CI]] 파이프라인 [[571_protection_vs_security|보호]]
521. [[231_ai_turing_test|인공지능]] 모델 공격 방어 - [[942_adversarial_example|적대적 예제]]([[942_adversarial_example|Adversarial Example]]), [[947_data_poisoning|데이터 포이즈닝]] 방어 설계
522. [[004_blockchain|블록체인]]/[[022_smart_contract|스마트 컨트랙트]] ([[022_smart_contract|Smart Contract]]) [[527_security_audit_trail|보안 감사]] (Reentrancy 공격 방어 등)
523. [[101_iot_concept|IoT]] 기기 [[032_firmware|펌웨어]] [[003_integrity|무결성]] [[395_verification_process_review|검증]]망 및 OTA ([[523_iot_firmware_ota_security|Over-The-Air]]) 안전 배포
524. 클라우드 보안 [[020_software_configuration_management|형상 관리]] ([[780_cspm_cloud_security_posture_management|CSPM]]) 연동 개발 프로세스
525. [[525_compliance_as_code_automation|컴플라이언스 애즈 코드]] ([[048_compliance_as_code|Compliance as Code]]) 자동화
526. [[526_security_logging_and_monitoring_failures|보안 로깅]] ([[526_security_logging_and_monitoring_failures|Logging]]) - 6하 원칙 기록, 중앙 집중식 보관(ELK), 위변조 방지 ([[590_worm|WORM]] 스토리지)
527. [[527_security_audit_trail|보안 감사]] ([[363_audit|Audit]]) 트레일 추적 기능
528. [[528_obfuscation_anti_debugging_mobile|난독화]] ([[528_obfuscation_anti_debugging_mobile|Obfuscation]]) 및 안티 디버깅 (Anti-debugging) 적용 (모바일 앱 보안)
529. [[529_memory_safety_rust_go|메모리 안전성]]([[529_memory_safety_rust_go|Memory Safety]]) 보장을 위한 [[782_memory_safety_rust_compiler_verification|Rust]], Go 언어 도입 동향
530. 보안 조직 분리 [[164_policy|정책]] 위반(SoD, Segregation of Duties)의 SW 통제 로직

## 9. SW 아키텍처 심화, [[531_cloud_native_architecture|클라우드 네이티브]] 및 [[190_ai_llm_requirements_specification|AI]] (80개)
531. [[204_cloud_native_architecture|클라우드 네이티브 아키텍처]] ([[204_cloud_native_architecture|Cloud Native Architecture]]) 철학
532. [[532_microservices_decomposition_patterns|마이크로서비스]] ([[619_msa_traffic_hardware|Microservices]]) 분해 패턴
533. 비즈니스 능력에 따른 분해 (Decompose by Business Capability)
534. 하위 [[064_relation_domain|도메인]]에 따른 분해 (Decompose by Subdomain - [[310_architecture|DDD]] 기반)
535. [[090_service_kubernetes_network_load_balancing|서비스]] 간 동기 통신 - [[477_rest_api_architecture|REST API]], [[479_grpc_protobuf_http2|gRPC]] ([[535_sync_communication_rest_grpc|Protocol Buffers]])
536. [[090_service_kubernetes_network_load_balancing|서비스]] 간 비동기 통신 - [[389_mesh_topology|메시]]지 큐 (RabbitMQ, [[179_kafka_flink_watermark_time_window|Kafka]]), AMQP [[295_protocol_field_tcp_udp_icmp|프로토콜]]
537. [[128_water_scrum_fall_anti_pattern|안티패턴]]: [[537_distributed_monolith_antipattern|분산 모놀리스]] ([[537_anti_pattern_distributed_monolith|Distributed Monolith]]) - 독립 배포 불가능한 [[619_msa_traffic_hardware|MSA]]
538. [[538_event_driven_architecture_eda|이벤트 기반 아키텍처]] ([[064_eda|EDA]]) - 이벤트 생산자, 브로커, 소비자 
539. [[539_event_bus_stream_processing|이벤트 버스]] ([[539_event_bus_stream_processing|Event Bus]]) 및 스트림 프로세싱
540. [[306_service_discovery_pattern|서비스 디스커버리]] ([[303_service_discovery|Service Discovery]]) - 동적 IP/[[446_port_and_bus|Port]] [[235_registry_immutable_tag|레지스트리]] (Eureka, Consul)
541. [[169_client_side_vs_server_side_discovery|클라이언트 사이드 디스커버리]] vs 서버 사이드 디스커버리
542. [[014_api_posix|API]] 게이트웨이 ([[542_api_gateway|API Gateway]]) - [[303_authentication_authorization_patterns|인증]], [[339_routing_overview_best_path_selection|라우팅]], 로드밸런싱, 통합(Aggregation)
543. [[543_bff_backend_for_frontend|BFF]] ([[543_bff_backend_for_frontend|Backend For Frontend]]) - 모바일, 웹 등 클라이언트 전용 맞춤형 게이트웨이
544. [[544_externalized_configuration|외부화된 구성 관리]] ([[544_externalized_configuration|Externalized Configuration]]) - [[009_config|Config]] Server (Spring Cloud [[009_config|Config]] 등)
545. [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]) - 애플리케이션 외부(인프라 계층)에서 통신 제어
546. [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] ([[546_sidecar_proxy_pattern|Sidecar]]) [[158_proxy_pattern|프록시 패턴]] - [[302_service_mesh_istio|Istio]], Envoy, Linkerd
547. 트래픽 [[339_routing_overview_best_path_selection|라우팅]], [[115_canary_deployment_gradual_rollout|카나리 배포]] 제어 ([[090_service_kubernetes_network_load_balancing|Service]] Mesh의 역할)
548. [[548_local_vs_distributed_transactions|로컬 트랜잭션]] ([[548_local_vs_distributed_transactions|Local Transaction]]) vs [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] ([[248_distributed_transaction_multiple_nodes|Distributed Transaction]])
549. [[549_2pc_two_phase_commit_limitations_msa|2PC]] ([[549_2pc_two_phase_commit_limitations_msa|Two-Phase Commit]])의 [[619_msa_traffic_hardware|MSA]] 적용 한계
550. [[305_saga|사가 패턴]] ([[305_saga_pattern|Saga Pattern]]) - [[548_local_vs_distributed_transactions|로컬 트랜잭션]]들의 연속된 체인
551. [[551_compensating_transaction_logical_rollback|보상 트랜잭션]] ([[551_compensating_transaction_logical_rollback|Compensating Transaction]]) - [[098_rollback_strategy_pipeline_error_threshold|롤백]]을 [[369_logic_bomb|논리]]적으로 수행하는 역방향 연산
552. [[552_orchestration_saga_centralized_control|오케스트레이션 사가]] ([[552_orchestration_saga_centralized_control|Orchestration Saga]]) - 중앙 통제기가 [[213_flow_control_buffer_overflow|흐름 제어]]
553. [[553_choreography_saga_event_driven|코레오그래피 사가]] ([[553_choreography_saga_event_driven|Choreography Saga]]) - 이벤트 구독 기반의 자율적 흐름
554. [[306_cqrs|CQRS]] (명령과 조회 책임 분리) - [[289_cqrs_db|쓰기]] DB와 읽기 DB 분리, [[212_synchronization_mechanisms|동기화]] 문제 해결 ([[650_eventual_consistency|Eventual Consistency]])
555. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]]) - CRUD 대신 상태 변경 이력(Event) 자체를 추가(Append-only) 저장
556. [[239_micro_frontends_architecture|마이크로 프론트엔드]] ([[239_micro_frontends_architecture|Micro Frontends]]) - 모놀리식 프론트엔드를 독립적 팀 단위 [[603_component_independent_deployment_unit|컴포넌트]]로 분할
557. [[557_webpack_module_federation|모듈 페더레이션]] ([[557_webpack_module_federation|Module Federation]]) (Webpack) 
558. [[215_serverless_architecture_faas_aws_lambda|서버리스 아키텍처]] ([[206_serverless_cold_start|Serverless]] / [[342_faas|FaaS]])
559. [[559_serverless_cold_start_mitigation|콜드 스타트]] ([[347_cold_start_problem|Cold Start]]) [[015_지연_데이터_관점|지연]] 문제 및 극복 방안 ([[202_provisioned_concurrency_serverless_cold_start|Provisioned Concurrency]] 등)
560. [[211_data_mesh_domain_ownership|데이터 메시]] ([[320_data_mesh|Data Mesh]]) - [[001_dikw_pyramid|데이터]] 소유권의 [[010_decentralization|탈중앙화]] ([[064_relation_domain|도메인]] 중심)
561. [[561_container_based_deployment|컨테이너]] ([[194_container_virtualization_docker_namespace|Container]]) 기반 배포 아키텍처
562. [[063_docker_architecture|도커]]([[063_docker_architecture|Docker]]) 이미지 계층(Layer) 최소화 기법
563. [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] ([[205_kubernetes_container_orchestration|Kubernetes]]) 오브젝트 아키텍처 ([[198_pod_kubernetes_minimum_deployment_unit|Pod]], [[090_service_kubernetes_network_load_balancing|Service]], [[087_deployment_kubernetes_workload_rolling_update|Deployment]], [[094_ingress_kubernetes_l7_routing_gateway|Ingress]])
564. [[207_helm_kubernetes_package_manager_chart|헬름]] ([[207_helm_kubernetes_package_manager_chart|Helm]]) 차트를 이용한 SW 패키지 관리
565. [[565_operator_pattern_kubernetes_automation|오퍼레이터]] ([[565_operator_pattern_kubernetes_automation|Operator]]) 패턴 - [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 사용자 정의 컨트롤러 확장을 통한 복잡한 앱 관리 자동화
566. [[642_observability_telemetry|옵저버빌리티]] ([[642_observability_telemetry|Observability]] / 가시성) 아키텍처
567. [[342_routing_metric_hop_bandwidth_delay|메트릭]] ([[567_metrics_time_series_prometheus_grafana|Metrics]]) - 시계열 [[001_dikw_pyramid|데이터]] 수집 ([[136_prometheus|Prometheus]], [[168_grafana|Grafana]])
568. [[568_logs_distributed_logging_elk_fluentd|로그]] ([[568_logs_distributed_logging_elk_fluentd|Logs]]) - [[136_variance|분산]] [[626_log_collection|로그 수집]] (ELK [[057_stack|Stack]] - [[302_cdc|Elasticsearch]], Logstash, [[169_kibana|Kibana]] / Fluentd)
569. [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] ([[569_distributed_tracing_opentelemetry_jaeger|Distributed Tracing]]) - [[191_transaction_concept_states|트랜잭션]] 경로 추적 ([[146_opentelemetry_otel_observability_standard|OpenTelemetry]], Jaeger, Zipkin)
570. Trace ID와 Span ID의 전파 ([[570_trace_id_span_id_context_propagation|Context Propagation]])
571. [[571_resiliency_fault_tolerance_patterns|탄력성]] ([[571_resiliency_fault_tolerance_patterns|Resiliency]]) 및 [[296_fault_tolerance_architecture|결함 허용]] ([[800_system_architecture_fault_tolerance_dual|Fault Tolerance]]) 패턴
572. [[307_circuit_breaker_pattern|서킷 브레이커]] ([[304_circuit_breaker|Circuit Breaker]]) - 상태(Closed, Open, Half-Open) 기반 장애 확산 차단 (Resilience4j)
573. [[573_timeout_retry_backoff_strategy|타임아웃]] ([[319_timeout_prevention|Timeout]]) 및 재시도 (Retry) 백오프(Backoff) [[268_strategy_pattern|전략]]
574. [[308_bulkhead_pattern|벌크헤드]] ([[308_bulkhead_pattern|Bulkhead]]) - [[103_thread_pool|스레드 풀]] 격리로 일부 장애가 전체 리소스 고갈로 이어지는 현상 방지
575. [[575_shadow_deployment_traffic_mirroring|섀도우 배포]] ([[118_shadow_deployment_traffic_mirroring|Shadow Deployment]] / 트래픽 [[333_raid_1|미러링]]) - 실운영 트래픽을 복제하여 신규 [[288_version_ihl_tos_total_length|버전]]에 테스트
576. [[576_feature_flag_ab_testing_rollout|피처 플래그]] ([[576_feature_flag_ab_testing_rollout|Feature Flag]]) 기반 A/B 테스트 및 점진적 롤아웃
577. [[316_ssr_vs_csr|서버 사이드 렌더링]] ([[316_ssr_vs_csr|SSR]]) [[603_component_independent_deployment_unit|컴포넌트]] 아키텍처 (Next.js, Nuxt.js)
578. [[578_ssg_and_isr_architecture|정적 사이트 생성]] ([[578_ssg_and_isr_architecture|SSG]]) / 증분 정적 재생성 ([[020_isr|ISR]]) 패턴
579. [[579_offline_first_pwa_service_worker|오프라인 우선]] ([[579_offline_first_pwa_service_worker|Offline-first]]) 아키텍처 ([[702_pwa_progressive_web_app_service_worker|PWA]], [[784_pwa_service_worker_caching_network|Service Worker]], IndexedDB)
580. [[319_webassembly_architecture|웹어셈블리]] ([[319_webassembly_architecture|WebAssembly]], [[701_webassembly_wasm_frontend_performance|WASM]]) 아키텍처 - 브라우저 내 고성능 네이티브 코드 실행
581. [[581_ai4se_ai_software_engineering_paradigm|AI4SE]] ([[190_ai_llm_requirements_specification|AI]] for [[001_software_engineering_definition|Software Engineering]]) - AI를 활용한 SW 엔지니어링 패러다임 변화
582. [[263_llm_large_language_model|LLM]]([[582_llm_based_code_generation_tools|대규모 언어 모델]]) 기반 코드 [[087_process_state_transition|생성]] 지원 도구 (GitHub Copilot, Cursor 등)
583. [[190_ai_llm_requirements_specification|AI]] 어시스턴트 코드 산출물의 라이선스 충돌([[583_ai_code_license_security_threats|저작권]]) 이슈 및 보안 위협 ([[345_llm_foundation_model_hallucination|Hallucination]] 버그)
584. [[149_prompt_engineering_cot_few_shot|프롬프트 엔지니어링]] ([[224_prompt_engineering_guideline|Prompt Engineering]]) 가이드라인 설계
585. [[276_fine_tuning|RAG]] ([[585_rag_retrieval_augmented_generation|Retrieval-Augmented Generation]]) 패턴 아키텍처 통합 설계
586. [[586_langchain_ai_pipeline_framework|랭체인]] ([[586_langchain_ai_pipeline_framework|LangChain]]) 프레임워크 기반 [[190_ai_llm_requirements_specification|AI]] 파이프라인 설계
587. 에이전틱 [[190_ai_llm_requirements_specification|AI]] ([[587_agentic_ai_autonomous_tools|Agentic AI]]) 시스템 - 도구(Tool)를 직접 호출하는 자율형 SW [[192_module_independence|모듈]] 설계
588. [[348_mlops|MLOps]] 파이프라인 - [[001_dikw_pyramid|데이터]] 수집, 모델 학습([[588_mlops_pipeline_automation|Training]]), 서빙(Serving), 모니터링 자동화
589. [[468_model_drift_retraining|모델 드리프트]] ([[468_model_drift_retraining|Model Drift]] / [[163_data_drift_statistical_distribution_shift|Data Drift]]) 모니터링 및 재학습 루프 설계
590. 엣지 [[190_ai_llm_requirements_specification|AI]] ([[174_edge_ai_on_device_ai|Edge AI]]) / 온디바이스 [[190_ai_llm_requirements_specification|AI]] ([[635_on_device_ai|On-Device AI]]) - 모델 경량화 ([[434_quantization|양자화]], [[435_pruning_hardware|가지치기]], [[252_knowledge_distillation_quantization_edge_slm_diffusion|지식 증류]]) 아키텍처
591. [[236_quantum_computing_pqc|양자 컴퓨팅]] ([[236_quantum_computing_pqc|Quantum Computing]]) [[001_algorithm_definition|알고리즘]] (쇼어 [[001_algorithm_definition|알고리즘]] 등)에 대비한 하이브리드 아키텍처 연구
592. [[004_blockchain|블록체인]] [[032_dapp_decentralized_application|DApp]] ([[592_blockchain_dapp_architecture_ipfs|Decentralized Application]]) 아키텍처 - 프론트엔드 + [[022_smart_contract|스마트 컨트랙트]] + [[055_ipfs_interplanetary_file_system|IPFS]]
593. [[126_digital_twin_concept|디지털 트윈]] ([[126_digital_twin_concept|Digital Twin]]) 소프트웨어 통합 통신 아키텍처
594. [[594_metaverse_realtime_sync_rendering_offloading|메타버스]] ([[594_metaverse_realtime_sync_rendering_offloading|Metaverse]]) 실시간 [[212_synchronization_mechanisms|동기화]] 아키텍처 및 렌더링 [[440_offloading|오프로딩]]
595. [[060_rpa_hyperautomation|RPA]] ([[060_rpa_hyperautomation|Robotic Process Automation]]) 봇 결합 아키텍처
596. 로우코드/노코드 (Low-[[082_process_memory_structure|Code]] / No-[[082_process_memory_structure|Code]]) 플랫폼 아키텍처 한계와 확장성 제어
597. [[597_headless_cms_architecture|헤드리스]] ([[597_headless_cms_architecture|Headless]]) CMS 아키텍처 - 프론트엔드와 백엔드 분리 유연성 제공
598. [[598_microkernel_plugin_architecture|마이크로 커널]] ([[024_microkernel|Microkernel]] / 플러그인) 아키텍처 - 이클립스, VS [[082_process_memory_structure|Code]] 확장 구조
599. [[599_modular_monolith_architecture|모듈러 모놀리스]] ([[599_modular_monolith_architecture|Modular Monolith]]) 아키텍처 - [[619_msa_traffic_hardware|MSA]] 전환 전 단계, [[192_module_independence|모듈]] 간 강결합 방지 아키텍처
600. [[600_architecture_runway_agile_foundation|아키텍처 런웨이]] ([[600_architecture_runway_agile_foundation|Architecture Runway]]) - 비즈니스 요구 수용을 위해 사전에 마련하는 기술적 기반 구조

## [[489_raid_10_hybrid|10]]. 최신 트렌드 및 프로젝트 관리/품질 심화 (200개 요약)
601. 객체지향 5원칙 [[242_solid_object_oriented_design_principles|SOLID]] 완벽 매핑
602. [[199_information_hiding_encapsulation|정보 은닉]]([[199_information_hiding_encapsulation|Information Hiding]]) 캡슐화 연계
603. [[603_component_independent_deployment_unit|컴포넌트]]([[603_component_independent_deployment_unit|Component]]) 독립 배포 단위
604. [[251_design_patterns_gof_overview|디자인 패턴]] 23가지 구조적 [[104_classification_analysis|분류]]
605. [[382_singleton_summary|싱글톤 패턴]] 메모리/쓰레드 세이프 설계
606. [[606_observer_pattern_pub_sub|옵저버 패턴]] (Pub/Sub 연계)
607. [[254_factory_method_pattern_subclass_creation|팩토리 메서드]] vs [[255_abstract_factory_pattern_object_families|추상 팩토리]] 
608. [[391_strategy_pattern_summary|전략 패턴]] [[001_algorithm_definition|알고리즘]] 교체 용이성
609. [[609_pipe_and_filter_architecture|파이프-필터 아키텍처 스트림]] 
610. MVC, [[036_mvp|MVP]], MVVM 프론트엔드 패턴 진화
611. [[217_clean_architecture_dependency_rule|클린 아키텍처]] 의존성 규칙 ([[611_clean_architecture_dependency_rule|내부로만 향함]])
612. 헥사고날 [[446_port_and_bus|포트]]와 [[259_adapter_pattern_interface_wrapper|어댑터]] 외부 격리
613. [[310_architecture|도메인 주도 설계]] ([[310_architecture|DDD]]) 기본 구성 (엔티티, VO, 리포지토리)
614. [[221_bounded_context_ddd_msa_boundary|바운디드 컨텍스트]] [[532_microservices_decomposition_patterns|마이크로서비스]] [[655_ir_detection_analysis|식별]] 기준
615. [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 루트 [[191_transaction_concept_states|트랜잭션]] 경계
616. [[532_microservices_decomposition_patterns|마이크로서비스]] [[014_api_posix|API]] 게이트웨이 [[303_authentication_authorization_patterns|인증]] 통합 
617. [[306_service_discovery_pattern|서비스 디스커버리]] Eureka 
618. [[307_circuit_breaker_pattern|서킷 브레이커]] 장애 연쇄 차단 메커니즘
619. [[312_saga_pattern_choreography_orchestration|사가]] ([[305_saga|Saga]]) 패턴 [[549_2pc_two_phase_commit_limitations_msa|2PC]] 한계 극복 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]
620. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 상태 재생 가능성 보장
621. [[306_cqrs|CQRS]] 읽기 [[289_cqrs_db|쓰기]] 분리 [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]]
622. [[599_modular_monolith_architecture|모듈러 모놀리스]] [[619_msa_traffic_hardware|MSA]] 대안적 접근 
623. [[377_serverless_cold_start|서버리스 콜드 스타트]] 이슈
624. [[531_cloud_native_architecture|클라우드 네이티브]] 12 Factor App 
625. [[367_test_double_isolation|테스트 더블]] Mock과 Stub의 차이 
626. V-모델 개발-테스트 매핑 구조
627. [[410_regression_test|회귀 테스트]] 커버리지 도구 
628. [[392_pesticide_paradox_test_renewal|살충제 패러독스]] 테스트 갱신
629. [[393_absence_of_errors_fallacy|오류 부재의 궤변]] 요구사항 미달 
630. [[630_equivalence_partitioning_boundary_value_analysis|동등 분할]] ([[630_equivalence_partitioning_boundary_value_analysis|Equivalence Partitioning]]) [[414_boundary_value_analysis|경계값 분석]] 
631. [[631_decision_table_logical_combination|결정 테이블]] ([[631_decision_table_logical_combination|Decision Table]]) [[369_logic_bomb|논리]] 조합 
632. [[632_state_transition_diagram_testing|상태 전이]] ([[632_state_transition_diagram_testing|State Transition]]) 다이어그램 
633. [[174_pairwise_comparison_priority_matrix|페어와이즈]] ([[174_pairwise_comparison_priority_matrix|Pairwise]]) 직교 [[055_array|배열]] (Orthogonal [[055_array|Array]]) 
634. 구문, 분기, [[424_condition_coverage|조건 커버리지]] 포함 [[083_relationship_in_er_model|관계]] 
635. MC/DC 항공/자동차 안전 표준 조건
636. 탐색적 테스트 차터 기반 [[210_heuristics_scheduling|휴리스틱]]
637. 퍼즈 테스트 보안 취약점 발견 
638. [[638_mutation_testing_test_case_verification|뮤테이션 테스트]] ([[638_mutation_testing_test_case_verification|돌연변이]]) [[441_test_case|테스트 케이스]] [[395_verification_process_review|검증]] 
639. A/B 테스팅 
640. [[445_performance_test_types|성능 테스트]] 부하/스트레스/[[129_spike_agile_technical_investigation|스파이크]]/인듀어런스 
641. ISO 25010 [[339_software_quality_definition|소프트웨어 품질]] 모델 
642. [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] ([[450_mtbf|MTBF]], [[451_mttr|MTTR]], [[360_mttf|MTTF]]) [[452_availability|가용성]] 공식
643. [[355_defect_density|결함 밀도]] 측정 및 프로세스 통제
644. [[100_technical_debt_monitoring_release_policy|기술 부채]] 마틴 파울러 사분면 
645. [[645_refactoring_code_smell|리팩토링 악취]]([[365_5_solid_code_smell|Code Smell]]) 제거 
646. [[330_code_review|코드 리뷰]] [[074_pair_programming_driver_navigator|페어 프로그래밍]]
647. [[647_ftr_formal_technical_review_inspection_walkthrough|FTR]] ([[647_ftr_formal_technical_review_inspection_walkthrough|정형 기술 검토]]) [[161_inspection_formal_review|인스펙션]]/[[162_walkthrough_informal_review|워크스루]] 
648. [[648_ccb_configuration_control_board|소프트웨어 형상 관리]] ([[167_scm_software_configuration_management|SCM]]) 통제 위원회 [[160_change_control_board_ccb_requirements_review|CCB]] 
649. [[025_baseline|기준선]] ([[025_baseline|Baseline]]) 수립 변경 통제 
650. [[090_configuration_item|CI]]/CD [[076_ci_continuous_integration|지속적 통합]], 배포 파이프라인
651. [[115_canary_deployment_gradual_rollout|카나리 배포]] / [[194_blue_green_deployment_strategy|블루-그린 배포]] 무중단 
652. [[652_devops_calms_culture|데브옵스]] ([[652_devops_calms_culture|DevOps]]) [[281_calms|CALMS]] 문화 
653. [[653_devsecops_shift_left|데브섹옵스]] ([[653_devsecops_shift_left|DevSecOps]]) [[242_shift_left_sdlc|시프트 레프트]] 
654. [[100_sre_site_reliability_engineering_error_budget|SRE]] [[102_sli_slo_service_level_indicator_objective|SLI]], [[181_slo_service_level_objective|SLO]], [[085_sla|SLA]] [[101_error_budget_sre|에러 예산]]
655. [[751_chaos_engineering|카오스 엔지니어링]] [[149_chaos_monkey_chaos_mesh|카오스 몽키]] 복원력 
656. [[119_gitops_single_source_of_truth|GitOps]] 인프라 선언적 관리 
657. [[642_observability_telemetry|옵저버빌리티]] [[568_logs_distributed_logging_elk_fluentd|로그]], [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]]([[657_observability|Tracing]]) 
658. [[658_agile_scrum_roles|애자일 스크럼]] ([[658_agile_scrum_roles|Scrum]]) 역할 분담 
659. [[067_sprint_timebox|스프린트]] 백로그 / 프로덕트 백로그 
660. [[072_burndown_burnup_chart|번다운 차트]] 작업 진척도 
661. [[084_kanban_board_wip_limit|칸반]] WIP ([[661_kanban_wip_limit|Work In Progress]]) 제한 
662. [[073_xp_extreme_programming|XP]] [[077_tdd_test_driven_development|테스트 주도 개발]] ([[164_tdd_test_driven_development|TDD]]) [[213_refactoring_cloud_native_rearchitecture|리팩토링]] 
663. [[082_story_point_velocity|스토리 포인트]] [[083_planning_poker|플래닝 포커]] 합의 
664. [[092_scaled_agile_frameworks_overview|대규모 애자일]] [[093_safe_scaled_agile_framework_art_pi|SAFe]], [[094_less_large_scale_scrum|LeSS]] 
665. [[035_lean_startup|린 스타트업]] [[036_mvp|MVP]] [[037_pivot|피벗]] 사이클 
666. 요구사항 도출 JAD 페르소나
667. 요구사항 [[395_verification_process_review|검증]] 추적성 매트릭스 ([[667_requirements_traceability_matrix|RTM]])
668. [[133_non_functional_requirements|비기능 요구사항]] [[202_architecture_drivers_quality_attributes|아키텍처 드라이버]] 
669. [[144_dfd_data_flow_diagram|DFD]] 자료 흐름도 4요소 
670. [[670_use_case_include_extend|유스케이스 포함]]([[670_use_case_include_extend|Include]]) 확장(Extend) 
671. [[232_uml_unified_modeling_language_overview|UML]] 클래스, 시퀀스, [[237_activity_diagram_dynamic_workflow_uml|액티비티 다이어그램]] 
672. 소프트웨어 비용 산정 [[145_cocomo_model|COCOMO]] 
673. [[673_function_point_ilf_eif|기능점수]] ([[293_fp_function_point|FP]]) 내부논리파일(ILF) 외부연계파일(EIF) 
674. [[051_delphi_method|델파이 기법]] 전문가 합의 
675. 프로젝트 관리 [[149_wbs_work_breakdown_structure|WBS]], [[150_cpm_critical_path_method|CPM]], [[151_pert_three_point_estimation|PERT]] 
676. [[152_evm_earned_value_management|EVM]] ([[040_evm|Earned Value Management]]) [[159_spi_schedule_performance_index|SPI]], [[158_cpi_cost_performance_index|CPI]] 계산 
677. [[133_cmmi_capability_maturity_model_integration_levels|CMMI]] 성숙도 5단계 ([[677_cmmi_5_levels_maturity|초기-관리-정의-정량-최적]])
678. [[139_spice_iso_iec_15504_process_assessment|SPICE]] 프로세스 역량 평가 
679. [[679_software_reengineering_reverse|소프트웨어 재공학 역공학]] 
680. 역 콘웨이 [[268_strategy_pattern|전략]] 아키텍처에 맞춘 조직 구성 
681. [[681_monorepo_vs_multirepo|모노레포 vs 멀티레포]] 
682. [[239_micro_frontends_architecture|마이크로 프론트엔드]] 웹팩 연계 
683. [[014_api_posix|API]] 게이트웨이 [[543_bff_backend_for_frontend|BFF]] ([[543_bff_backend_for_frontend|Backend for Frontend]])
684. 스트랭글러 패턴 레거시 분할 
685. [[685_toil_automation_sre|토일]] ([[685_toil_automation_sre|Toil]]) 자동화 축소 대상 작업 
686. [[686_cognitive_load_team_topologies|인지 부하]] ([[686_cognitive_load_team_topologies|Cognitive Load]]) 팀 토폴로지 
687. [[190_secure_coding_guideline|시큐어 코딩]] 입력값 [[395_verification_process_review|검증]] [[726_xss_cross_site_scripting_types|XSS]] SQLi 방어 
688. [[491_sast_static_analysis|SAST]] / [[492_dast_dynamic_analysis|DAST]] / [[493_iast_interactive_analysis|IAST]] 보안 테스팅 도구 비교 
689. [[494_rasp_runtime_protection|RASP]] 런타임 자체 [[571_protection_vs_security|보호]] 
690. [[690_sbom_software_supply_chain_security|소프트웨어 자재 명세서]] ([[890_sbom_cyclonedx_spdx|SBOM]]) [[374_supply_chain_security|공급망 보안]] 
691. [[191_oss_license_compliance|오픈소스]] 컴플라이언스 GPL 카피레프트 
692. [[611_threat_modeling|위협 모델링]] [[097_stride_convolutional_neural_network_downsampling|STRIDE]] 
693. [[184_zero_trust_architecture|제로 트러스트 아키텍처]] [[010_least_privilege|최소 권한 원칙]] 
694. [[795_confidential_computing|기밀 컴퓨팅]] [[001_dikw_pyramid|데이터]] 인 유즈([[694_confidential_computing_data_in_use|In Use]]) [[571_protection_vs_security|보호]] 
695. [[519_cyber_resilience_architecture|사이버 레질리언스]] 시스템 생존성 
696. [[190_ai_llm_requirements_specification|AI]] 기반 코드 [[087_process_state_transition|생성]] 코파일럿 프롬프트 
697. [[263_llm_large_language_model|LLM]] [[275_react_framework|환각]] 방지 [[276_fine_tuning|RAG]] 아키텍처 
698. [[348_mlops|MLOps]] [[163_data_drift_statistical_distribution_shift|데이터 드리프트]] 모니터링 
699. [[211_data_mesh_domain_ownership|데이터 메시]] 탈중앙 [[064_relation_domain|도메인]] 오너십 
700. [[206_serverless_cold_start|서버리스]] [[342_faas|FaaS]] 아키텍처 제약 
701. [[319_webassembly_architecture|WebAssembly]] ([[701_webassembly_wasm_frontend_performance|Wasm]]) 프론트 [[282_performance_tactics|성능]] 가속 
702. [[702_pwa_progressive_web_app_service_worker|PWA]] ([[702_pwa_progressive_web_app_service_worker|Progressive Web App]]) 오프라인 워커 
703. 백파이어링 [[293_fp_function_point|FP]] LOC 역산 
704. 피쳐 [[186_character_stuffing_dle_stx_etx|플래그]] 런타임 기능 토글 
705. [[302_service_mesh_istio|서비스 메시]] ([[302_service_mesh_istio|Istio]]) [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 통신 제어 
706. [[314_transactional_outbox_pattern|트랜잭셔널 아웃박스]] 이벤트 유실 방지 
707. [[707_oat_operational_acceptance_testing|OAT]] ([[707_oat_operational_acceptance_testing|운영 인수 테스트]]) [[555_backup_and_restore_strategy|백업]] [[658_ir_recovery|복구]] [[395_verification_process_review|검증]] 
708. [[209_blackboard_pattern_ai_heuristic|블랙보드 패턴]] 비결정적 문제 해결 
709. [[208_broker_pattern_distributed_systems_message|브로커 패턴]] [[136_variance|분산]] 시스템 미들웨어 
710. [[710_atdd_acceptance_test_driven_development|ATDD]] (인수 [[077_tdd_test_driven_development|테스트 주도 개발]]) [[165_bdd_behavior_driven_development|BDD]] 연계 
711. [[334_kwcag|KWCAG]] 웹 [[292_accessibility_kwcag_wcag|접근성]] 지침 
712. [[294_dark_pattern_avoidance|다크 패턴]] 기만적 UX 방지 
713. 기능 안전 ISO 26262 ASIL 등급 
714. [[752_fmea|FMEA]] / [[753_fta|FTA]] [[352_defect_definition|결함]] 분석망 
715. N-[[288_version_ihl_tos_total_length|버전]] 프로그래밍 이종 [[071_다중화_Multiplexing|다중화]] 
716. [[459_fail_safe|페일 세이프]] / [[460_fail_soft|페일 소프트]] 비교 
717. [[531_cloud_native_architecture|클라우드 네이티브]] 스토리지 컴퓨팅 분리 
718. [[004_blockchain|블록체인]] [[032_dapp_decentralized_application|DApp]] [[022_smart_contract|스마트 컨트랙트]] 구조 
719. [[236_quantum_computing_pqc|양자 컴퓨팅]] 대비 [[351_quantum_computing_pqc_transition|PQC]] 소프트웨어 구조 전환 
720. [[196_dataops_dbt_ci_cd_data_testing|데이터옵스]] ([[324_dataops|DataOps]]) 자동화 
721. [[217_clean_architecture_dependency_rule|클린 아키텍처]] Usecase Interactor 설계 
722. [[218_onion_architecture_domain_centric_design|어니언 아키텍처]] [[064_relation_domain|도메인]] 코어 격리 
723. [[372_cots|COTS]] 상용 기성품 통합 테스팅 
724. [[207_iac_terraform_immutable_infrastructure|인프라스트럭처 애즈 코드]] ([[793_iac_idempotency_template|IaC]]) [[195_terraform_hashicorp_agnostic_aws_gcp|테라폼]] 
725. 선언적 인프라 상태 일치 루프 
726. [[109_platform_engineering_cognitive_load|플랫폼 엔지니어링]] [[536_idp_identity_provider|IDP]] 포털 [[058_dx_developer_experience|개발자 경험]]([[726_platform_engineering_idp_dx|DX]])
727. [[523_dhcp_dora_process|DORA]] [[342_routing_metric_hop_bandwidth_delay|메트릭]]스 4대 지표 ([[727_dora_metrics_4_indicators|배포 빈도 등]]) 
728. SPACE 프레임워크 생산성 다각화 
729. [[729_oo_coupling_types|객체지향 결합도]] (내용, 공통, 제어, 스탬프, 자료) 
730. [[730_oo_cohesion_types|객체지향 응집도]] (우연, [[369_logic_bomb|논리]], 시간, 절차, 통신, 순차, 기능) 
731. [[229_atam_architecture_trade_off_analysis_method|ATAM]] 트레이드오프 분석 평가 트리 
732. TQM [[350_total_quality_management|전사적 품질 관리]] 예방 위주 
733. [[366_gqm|GQM]] 지표 측정 골 기반 구조 
734. [[382_defensive_programming|방어적 프로그래밍]] Assertion 계약 기반 설계 
735. [[388_design_by_contract|디자인 바이 컨트랙트]] 불변 조건 
736. [[568_logs_distributed_logging_elk_fluentd|로그]] 6하 원칙 [[590_worm|WORM]] 스토리지 [[003_integrity|무결성]] 
737. [[890_sbom_cyclonedx_spdx|SBOM]] 규격 SPDX CycloneDX 
738. [[247_container_image_scanning_os_trivy|컨테이너 이미지 스캐닝]] 권한 통제 
739. [[552_mfa|MFA]] [[303_authentication_authorization_patterns|인증]] [[537_oidc_openid_connect|OIDC]] [[509_authorization_models_rbac_abac|인가]] 보안 구조 
740. [[014_api_posix|API]] 스로틀링 Rate Limit DDoS 방어 
741. [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] 상호 [[303_authentication_authorization_patterns|인증]] [[090_service_kubernetes_network_load_balancing|서비스]] 간 보안 
742. K-익명성 프라이버시 디자인([[060_privacy_by_design|PbD]]) 설계 
743. [[819_data_masking|데이터 마스킹]] [[822_fpe|FPE]] 암호 유지 
744. [[235_edge_computing_smart_factory|엣지 컴퓨팅]] [[001_dikw_pyramid|데이터]] 로컬 최적화 
745. [[126_digital_twin_concept|디지털 트윈]] [[212_synchronization_mechanisms|동기화]] 인터페이스 모델 
746. [[924_metaverse_network_qos_rendering_offload_mec|메타버스 네트워크]] 렌더링 [[015_지연_데이터_관점|지연]] 단축 기술 
747. 탄소 인지적 소프트웨어 그린 코딩 
748. 로우코드/노코드 섀도우 IT 거버넌스 
749. [[598_microkernel_plugin_architecture|마이크로 커널]] 아키텍처 플러그인 확장 
750. [[600_architecture_runway_agile_foundation|아키텍처 런웨이]] 기술적 기반 조기 확보 
751. [[002_software_crisis|소프트웨어 위기]] 비용 [[015_지연_데이터_관점|지연]] 품질 문제 
752. [[257_prototype_pattern_object_cloning|프로토타입]] 버리기 모델 vs 진화적 모델 
753. 나선형 위험 분석 4단계 루프 
754. 테일러링 프로젝트 맞춤형 프로세스 재단 
755. [[059_pmo_project_management_office|PMO]] 전사 품질 통제 및 [[606_auditing_linux_auditd|감사]] 조직 
756. [[112_zachman_framework|잭맨 프레임워크]] 6x6 매트릭스 
757. MoSCoW 요구사항 우선순위 판별 
758. Kano 모델 매력적, 당연적 품질 요소 [[104_classification_analysis|분류]] 
759. QFD [[168_qfd_quality_function_deployment|품질 기능 전개]] 요구사항 변환 기법 
760. [[760_inspection_moderator_formal_review|인스펙션 중재자]]([[760_inspection_moderator_formal_review|Moderator]]) 주도 공식 검토 
761. [[162_walkthrough_informal_review|워크스루]] 비공식 기술 검토 회의 
762. [[004_agile_relation|애자일]] [[182_epic_agile_requirements|에픽]], 스토리, [[184_theme_agile_requirements|테마]], [[150_task|태스크]] 계층 
763. 지속적 [[400_integration_testing|통합 테스트]] 빌드 자동화 서버 
764. [[085_lead_time_cycle_time|리드 타임]] 프로세스 시작부터 배포 완료 
765. [[086_cumulative_flow_diagram_cfd|누적 흐름도]] 병목 지점 병목 분석 
766. [[032_software_obsolescence|소프트웨어 노후화]] [[100_technical_debt_monitoring_release_policy|기술 부채]] 연계 
767. 객체지향 [[198_abstraction_control_data_process|추상화]] 자료/제어/과정 분리 
768. [[768_rumbaugh_omt_object_dynamic_functional|럼바우 객체 모델링]] (객체/동적/기능 모델) 
769. [[143_structured_analysis_dfd_dd_minispec|구조적 분석]] 도구 [[393_data_dictionary|데이터 사전]]([[769_architecture|DD]]) 표기법 
770. [[176_petri_net_concurrent_system_specification|페트리 넷]] 병행/비동기 시스템 정형 명세 
771. [[165_bdd_behavior_driven_development|BDD]] Given-When-Then 행동 명세 테스트 
772. [[710_atdd_acceptance_test_driven_development|ATDD]] 인수 [[077_tdd_test_driven_development|테스트 주도 개발]] 구조 
773. 테스트 하네스 [[460_stub_test_double|스텁]], 드라이버, 슈트 포괄 환경 
774. 소프트웨어 안전성 [[459_fail_safe|Fail-Safe]], [[460_fail_soft|Fail-Soft]] 
775. [[187_information_system_audit|정보시스템 감리]] 절차 모델 
776. [[339_software_quality_definition|소프트웨어 품질]] 비용 통제 [[070_graph_datastructure|그래프]] 최적점 
777. 정량적 프로젝트 관리 [[159_spi_schedule_performance_index|SPI]] 통제 한계선 
778. 소프트웨어 테스트 성숙도 모델 ([[778_tmmi_test_maturity_model_integration|TMMi]]) 
779. ISO/IEC/IEEE 29119 소프트웨어 테스팅 국제 표준 
780. 클라우드 보안 [[020_software_configuration_management|형상 관리]] ([[780_cspm_cloud_security_posture_management|CSPM]]) [[652_devops_calms_culture|데브옵스]] 결합 
781. 안티 디버깅 코드 [[528_obfuscation_anti_debugging_mobile|난독화]] 리버스엔지니어링 차단 
782. [[782_memory_safety_rust_compiler_verification|메모리 안전성 언어]] ([[782_memory_safety_rust_compiler_verification|Rust]]) 컴파일러 [[395_verification_process_review|검증]] 차용 
783. [[316_ssr_vs_csr|서버 사이드 렌더링]]([[316_ssr_vs_csr|SSR]]) 하이드레이션(Hydration) 
784. [[784_pwa_service_worker_caching_network|웹 프로그레시브 서비스워커]]([[784_pwa_service_worker_caching_network|Service Worker]]) 연계망 
785. [[532_microservices_decomposition_patterns|마이크로서비스]] [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] [[650_eventual_consistency|결과적 일관성]] 확보 
786. [[136_variance|분산]] 시스템 [[642_observability_telemetry|옵저버빌리티]] [[303_trace_id|Trace ID]] 상관관계 분석 
787. [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 루트 외부 접근 단일 진입점 설계 
788. [[216_hexagonal_architecture_ports_and_adapters|헥사고날 아키텍처]] [[259_adapter_pattern_interface_wrapper|어댑터]] [[446_port_and_bus|포트]] 매핑 구조 
789. [[217_clean_architecture_dependency_rule|클린 아키텍처]] 엔티티 유스케이스 프레젠테이션 계층 분리 
790. [[790_event_bus_kafka_asynchronous|이벤트 버스 카프카]]([[179_kafka_flink_watermark_time_window|Kafka]]) 비동기 내결함성 설계 
791. [[212_soa_service_oriented_architecture_esb|서비스 지향 아키텍처]]([[618_soa_hardware|SOA]]) [[146_esb_enterprise_service_bus_architecture|ESB]] [[282_performance_tactics|성능]] 병목 한계 
792. [[014_api_posix|API]] 게이트웨이 [[303_authentication_authorization_patterns|인증]] 및 [[339_routing_overview_best_path_selection|라우팅]] 병목 관리망 
793. [[793_iac_idempotency_template|인프라 코드]] ([[793_iac_idempotency_template|IaC]]) [[171_idempotency_iac_terraform|멱등성]] 보장 템플릿 기술 
794. [[099_continuous_deployment_cd|지속적 배포]] [[098_rollback_strategy_pipeline_error_threshold|롤백]] 자동화 [[164_policy|정책]] 파이프라인 구성 
795. 린 개발 7원칙 낭비 제거 전체 최적화 배포망 
796. [[796_retrospective|스크럼 스프린트 회고]]([[796_retrospective|Retrospective]]) 개선 액션 도출 
797. [[073_xp_extreme_programming|XP]] 실천 방법 [[164_tdd_test_driven_development|TDD]] 페어 지속 통합 코드 공동 소유 
798. [[022_configuration_control|형상 통제]] [[159_baseline_requirements_configuration_management|베이스라인]] 변경 심의 이력 추적 
799. [[145_cocomo_model|COCOMO]] 비용 산정 모드 (Organic, Semi, Embedded) 
800. [[001_software_engineering_definition|소프트웨어 공학]] 기술사 10개년 기출 핵심 융합 토픽 결론 정리 

---
**총합 요약 : 총 800개 핵심 키워드 수록**
(소프트웨어공학의 전통적 이론부터 객체지향/아키텍처/테스트를 거쳐, 최근 핫트렌드인 [[004_agile_relation|애자일]], [[652_devops_calms_culture|DevOps]], [[531_cloud_native_architecture|클라우드 네이티브]]([[619_msa_traffic_hardware|MSA]]), [[190_ai_llm_requirements_specification|AI]] 코드생성, [[190_secure_coding_guideline|시큐어 코딩]]까지 정보관리기술사 수준의 방대한 지식 체계를 800개의 키워드로 집대성하였습니다.)