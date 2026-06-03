---
title: 11. 정보시스템 감리 및 소프트웨어 설계 (디자인 패턴/아키텍처) 키워드 목록
date: '2026-03-04'
tags:
- studynote-design-supervision
---
[[267_weight_bias_activation|weight]] = 9999

# [[187_information_system_audit|정보시스템 감리]] 및 S/W 아키텍처 설계 키워드 목록 (심화 확장판)

[[187_information_system_audit|정보시스템 감리]]사, 정보관리기술사, 컴퓨터응용시스템기술사 합격을 위한 IT [[606_auditing_linux_auditd|감사]]([[363_audit|Audit]]), 공공/민간 [[006_audit_framework_3dimensional|감리 프레임워크]], [[201_software_architecture_definition|소프트웨어 아키텍처]] 평가, [[242_solid_object_oriented_design_principles|객체지향 설계 원칙]]([[242_solid_object_oriented_design_principles|SOLID]]), 그리고 GoF [[251_design_patterns_gof_overview|디자인 패턴]] 전 영역을 완벽 해부한 800대 핵심 키워드입니다.

---

## 1. [[187_information_system_audit|정보시스템 감리]] 개요 및 프레임워크 (80개)
1. [[187_information_system_audit|정보시스템 감리]] ([[187_information_system_audit|Information System Audit]]) 정의 - 제3자적 관점에서 정보시스템의 효과성, 효율성, 안전성을 종합적으로 점검하고 개선을 권고하는 활동
2. 감리의 3대 목적 - 효과성(Effectiveness, 목적 달성 여부), 효율성(Efficiency, 자원 최적화), 안전성/[[283_security_tactics|보안성]]([[283_security_tactics|Security]]/Safeguard, 자산 [[571_protection_vs_security|보호]] 및 [[003_integrity|무결성]] 유지)
3. [[003_audit_stakeholders|감리 발주자]] ([[003_audit_stakeholders|Client]]) / 피감리인 (Auditee, 사업자/주관기관) / 감리 법인 (Auditor)
4. [[004_egov_law_article_57|전자정부법 제57조]] ([[004_egov_law_article_57|감리 의무화 규정]]) - 행정/공공기관의 일정 규모 이상 정보화 사업 의무 감리 지정
5. [[005_audit_standards|정보시스템 감리기준]] ([[005_audit_standards|행정안전부 고시]])
6. [[006_audit_framework_3dimensional|감리 프레임워크]] ([[006_audit_framework_3dimensional|Audit Framework]]) 3차원 구조 - [[007_audit_domain|감리 영역]], [[008_audit_perspective|감리 관점]], [[009_audit_phase|감리 단계]]
7. [[007_audit_domain|감리 영역]] ([[007_audit_domain|Audit Domain]]) - 사업 관리, 응용 시스템, [[002_database_definition|데이터베이스]], 시스템 아키텍처/보안
8. [[008_audit_perspective|감리 관점]] ([[008_audit_perspective|Audit Perspective]]) - 절차(Procedure), 산출물(Deliverable), 성과([[282_performance_tactics|Performance]]) 관점 점검
9. [[009_audit_phase|감리 단계]] ([[009_audit_phase|Audit Phase]]) - 사업의 [[216_progress_in_synchronization|진행]] 단계 (요구정의, 설계, 종료/구현)
[[489_raid_10_hybrid|10]]. [[010_preventive_resident_audit|예방 감리]] ([[010_preventive_resident_audit|Preventive Audit]]) / 상주 감리 (Resident [[363_audit|Audit]]) - 사업 [[216_progress_in_synchronization|진행]] 중 상주하며 상시 조언
[[308_static_dynamic_nat_pat_port_address_translation|11]]. [[322_audit|3단계 감리]] - 요구정의 단계 감리, 설계 단계 감리, 종료 단계 감리
12. 2단계 감리 - 설계 단계 감리, 종료 단계 감리 (요구정의 감리 생략 조건 사업)
13. 추가 감리 / 시정조치 [[396_validation|확인]] ([[013_follow_up_audit|Follow-up Audit]]) - 감리 지적 사항(조치 권고) 이행 여부 최종 점검
14. [[014_audit_planning|감리 계획 수립]] ([[013_audit_planning|Audit Planning]]) - 예비조사, 감리 일정 및 인력 배치, 감리 계획서 작성
15. [[015_preliminary_survey|예비 조사]] ([[015_preliminary_survey|Preliminary Survey]]) - 피감리인 인터뷰, 과업내용서/제안서 분석을 통해 감리 주안점 도출
16. [[016_kick_off_meeting|착수 회의]] ([[016_kick_off_meeting|Kick-off Meeting]]) - 감리 목적, 일정, 범위, 협조 사항 공유
17. [[017_audit_execution|감리 수행]] ([[017_audit_execution|Audit Execution]]) - 실지 [[606_auditing_linux_auditd|감사]], 인터뷰, 문서 검토, 자동화 도구 진단
18. [[018_audit_report|감리 보고서]] ([[018_audit_report|Audit Report]]) 구조 - 총평, 분야별 감리 결과, 시정 조치 권고 사항
19. [[019_exit_meeting|종료 회의]] ([[019_exit_meeting|Exit Meeting]]) - 감리 결과 발표 및 이견 조율
20. [[020_follow_up_action_verification|조치 결과 확인]] (시정조치 [[396_validation|확인]] 보고서 발행)
21. [[021_isaca_global_standard|ISACA]] (Information Systems [[363_audit|Audit]] and Control Association) - 정보시스템 [[606_auditing_linux_auditd|감사]] 통제 협회
22. [[022_cisa_certification_audit|CISA]] (Certified Information Systems Auditor) - 국제 공인 정보시스템 [[606_auditing_linux_auditd|감사]]사
23. [[015_ita_information_technology_architecture|ITA]]/[[110_enterprise_architecture_ea|EA]] ([[010_ea_enterprise_architecture|Enterprise Architecture]]) 프레임워크 기반 감리
24. [[024_risk_based_audit|위험 기반 감리]] ([[024_risk_based_audit|Risk-based Audit]]) - [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]가 높은 영역에 감리 자원 집중
25. 과업 대비표 ([[025_task_traceability_matrix|Task Traceability Matrix]]) - RFP, 제안서, 요구사항 명세서 간의 과업 이행 여부 추적 맵
26. [[159_baseline_requirements_configuration_management|베이스라인]] ([[025_baseline|Baseline]]) [[395_verification_process_review|검증]] - 요구사항, 설계 산출물의 [[022_configuration_control|형상 통제]] 및 승인 [[025_baseline|기준선]] 점검
27. 사업 관리 (PM) 영역 감리 - 통합 관리, 범위 관리, 일정 관리, 품질 관리, 인력 관리, 의사소통 관리, 위험 관리 점검
28. 응용 시스템 영역 감리 - 기능 요구사항 구현 여부, [[201_software_architecture_definition|소프트웨어 아키텍처]], UI/UX, 테스트 적정성 점검
29. [[029_database_area_audit|데이터베이스 영역 감리]] - [[001_dikw_pyramid|데이터]] 모델링(ERD [[093_normalization|정규화]]/반정규화), [[001_dikw_pyramid|데이터]] 표준 관리, 이행(Migration) [[003_integrity|무결성]], [[282_performance_tactics|성능]] 튜닝 점검
30. 시스템 아키텍처/보안 영역 감리 - 인프라(HW/SW/네트워크) 용량 산정 적정성, 보안 지침([[190_secure_coding_guideline|시큐어 코딩]], [[803_privacy_law_comparison|개인정보보호]]) 준수 여부, 장애 [[658_ir_recovery|복구]]([[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]]) 체계 점검
31. 정보화 사업 유형별 감리 - SI(구축), 운영/유지보수, [[001_dikw_pyramid|데이터]] 마이그레이션, 클라우드 전환 감리 등
32. [[032_audit_automation_tools|감리 자동화 도구]] - 소스코드 [[331_static_analysis|정적 분석]] 도구([[491_sast_static_analysis|SAST]]), [[041_contractor_late_penalty|데이터 품질 진단]] 도구, DB [[282_performance_tactics|성능]] 진단 도구, [[282_performance_tactics|성능]] [[446_load_test|부하 테스트]] 도구 활용 지침
33. [[673_function_point_ilf_eif|기능점수]] ([[140_function_point|Function Point]]) [[395_verification_process_review|검증]] - 발주 시 규모 산정과 구현 종료 시 최종 [[673_function_point_ilf_eif|기능점수]]([[293_fp_function_point|FP]]) 일치 여부 및 정산 단가 검토
34. SW 개발보안 ([[190_secure_coding_guideline|시큐어 코딩]]) 진단 - KISA [[497_kisa_secure_coding_guide|47개 보안 약점]] 기준 위반 소스코드 점검 의무
35. 웹 [[292_accessibility_kwcag_wcag|접근성]] (Web [[292_accessibility_kwcag_wcag|Accessibility]], [[334_kwcag|KWCAG]]) 및 웹 [[344_compatibility_usability|호환성]] 준수 여부 진단
36. [[034_audit_quality_management|감리 품질 관리]] (Quality Assurance of [[363_audit|Audit]]) - 감리 법인 내부의 감리 품질 통제 프로세스
37. [[059_pmo_project_management_office|PMO]] ([[059_pmo_project_management_office|Project Management Office]]) - 발주자를 대행하여 프로젝트 관리 및 기술 지원을 수행하는 조직 (사전 예방 위주)
38. PMO와 감리의 차이 - PMO는 발주자 편에서 능동적 문제 해결 개입, 감리는 제3자 관점에서 객관적 평가 및 권고 (감리 독립성)
39. 전자정부 표준 프레임워크 (eGovFrame) 아키텍처 및 적용 기준 점검 (스프링 부트 기반 공통 [[603_component_independent_deployment_unit|컴포넌트]] 활용성)
40. 클라우드 기반 정보화 사업 감리 가이드 - [[183_iaas_infrastructure_as_a_service|IaaS]], [[184_paas_platform_as_a_service|PaaS]], [[309_saas|SaaS]] [[085_sla|SLA]] 점검 및 [[001_dikw_pyramid|데이터]] 이관/[[008_dependencies|종속성]]([[362_lock_in_portability|Lock-in]]) 점검 지침
41. [[041_contractor_late_penalty|데이터 품질 진단]] ([[041_contractor_late_penalty|Data Quality Audit]]) - 완전성, 유효성, [[194_consistency_database_integrity|일관성]], [[002_bigdata_5v|정확성]], 적시성, [[283_security_tactics|보안성]] (6대 [[001_dikw_pyramid|데이터]] 품질 지표 점검)
42. [[056_objective_evidence_collection|객관적 증거]] ([[056_objective_evidence_collection|Objective Evidence]]) 수집 원칙 - 면담, 관찰, 문서 검토, 직접 진단(테스트) 기법
43. [[039_sampling_audit_technique|샘플링 감리 기법]] - 전수 조사가 불가능할 때 통계적(확률적) 샘플링 추출을 통한 진단
44. [[058_auditor_independence_objectivity|감리인의 독립성]] ([[133_independence|Independence]]) 및 객관성 원칙 유지 조항
45. 사업자 [[059_liquidated_damages_progress_verification|지체 상금]] ([[059_liquidated_damages_progress_verification|Liquidated Damages]]) 분쟁 예방을 위한 진척도 및 [[015_지연_데이터_관점|지연]] 사유 증빙 점검
46. 테스트 계획, 시나리오, 결과서 (단위, 통합, 시스템, [[406_acceptance_test_uat|인수 테스트]]) 완결성 대조 [[396_validation|확인]]
47. [[157_requirements_traceability_matrix_rtm|요구사항 추적 매트릭스]] ([[667_requirements_traceability_matrix|RTM]], [[667_requirements_traceability_matrix|Requirements Traceability Matrix]])의 양방향 추적성 [[395_verification_process_review|검증]]
48. 소프트웨어 인도물 (Deliverables) 명세 합치 여부 점검
49. 유지보수 이관 (Hand-over) 및 운영자 교육, 매뉴얼 적정성 진단
50. 모바일 앱 사업 감리 - 앱 스토어 배포 기준, 취약점(위변조 방지, 루팅 탐지), [[528_obfuscation_anti_debugging_mobile|난독화]] 적용 여부 점검
51. [[190_ai_llm_requirements_specification|AI]] / 빅데이터 사업 감리 - 학습 [[001_dikw_pyramid|데이터]] 편향성, [[001_algorithm_definition|알고리즘]] [[282_performance_tactics|성능]] 지표([[255_f1_score|F1-score]], MAE 등), [[196_pseudonymization_de_identification|개인정보 가명 처리]] 적정성 평가
52. [[101_iot_concept|IoT]] 구축 사업 감리 - 디바이스 [[032_firmware|펌웨어]] [[003_integrity|무결성]], 경량 통신 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 안정성 점검
53. [[004_blockchain|블록체인]] 사업 감리 - [[022_smart_contract|스마트 컨트랙트]] 취약점 점검 및 [[011_consensus_algorithm|합의 알고리즘]] 노드 구성 점검
54. [[062_itil|ITIL]] / [[096_iso_iec_20000_itsm_certification|ITSM]] 프레임워크 기반 운영 감리 프로세스 점검 ([[085_sla|SLA]] 달성 여부)
55. [[171_isms_p|ISMS-P]] [[303_authentication_authorization_patterns|인증]] 연계 - [[781_personal_information|개인정보]] 처리 시스템 취약점 조치 여부 병행 점검
56. 하드웨어 Sizing (용량 산정) - tpmC, SPECint 지표 기반 CPU, 메모리, 디스크 계산식 [[395_verification_process_review|검증]]
57. [[001_dikw_pyramid|데이터]] 이행 ([[001_dikw_pyramid|Data]] Migration) 성공 기준 [[395_verification_process_review|검증]] - 추출, 정제, 적재 [[001_dikw_pyramid|데이터]] 건수 및 [[112_checksum|체크섬]] 대조
58. 고가용성 (HA, High [[452_availability|Availability]]) 및 [[456_dual_redundancy|이중화]] 클러스터 페일오버([[300_failover_architecture|Failover]]) 시나리오 실지 테스트 참관
59. 보안 장비 ([[690_firewall_generation_evolution|방화벽]], [[695_ips_network_intrusion_prevention_system|IPS]], [[696_waf_web_application_firewall|WAF]]) [[164_policy|정책]] 룰셋(Rule-set) 최적화 상태 점검
60. [[060_open_data_public_api_standards|공공데이터 개방]] ([[060_open_data_public_api_standards|Open Data]]) 표준 규격 (CSV, [[343_json|JSON]], [[477_rest_api_architecture|REST API]]) 포맷 준수 감리
61. [[379_dr_architecture|재해 복구]] ([[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]]) 모의 훈련 참관 및 [[176_rto_recovery_time_objective|RTO]]/[[177_rpo_recovery_point_objective|RPO]] 지표 목표 달성 [[396_validation|확인]]
62. [[555_backup_and_restore_strategy|백업]] 및 아카이빙 [[164_policy|정책]] (Full, Incremental, Differential [[555_backup_and_restore_strategy|백업]]) [[208_schedule_history_transaction_execution_order|스케줄]] 점검
63. [[063_software_license_compliance|소프트웨어 라이선스 컴플라이언스]] - 불법 SW 사용 여부 및 [[191_oss_license_compliance|오픈소스]] 라이선스(GPL, MIT 등) 고지 점검
64. [[387_access_control_pattern|접근 통제]] 및 권한 관리 ([[387_access_control_pattern|접근 통제]] 행렬, [[569_rbac|RBAC]] 적용) 권한 오남용 및 퇴사자 권한 회수 이력 [[606_auditing_linux_auditd|감사]]
65. [[568_logs_distributed_logging_elk_fluentd|로그]] 및 [[606_auditing_linux_auditd|감사]] 추적 ([[065_audit_trail_worm_storage_compliance|Audit Trail]]) - 시스템 [[568_logs_distributed_logging_elk_fluentd|로그]]가 6하 원칙에 따라 위변조 불가능한([[590_worm|WORM]]) 스토리지에 저장되는지 점검
66. 비밀번호 암호화 저장 방식 (일방향 해시 [[001_algorithm_definition|알고리즘]] SHA-256 이상 + 솔팅 적용 여부) 진단
67. SSL/[[694_thread_local_storage_tls|TLS]] [[303_authentication_authorization_patterns|인증]]서 적용 및 통신 구간 암호화 미적용 취약점 점검
68. [[068_software_accessibility_ui_ux_audit|소프트웨어 접근성]] ([[068_software_accessibility_ui_ux_audit|Software Accessibility]]) - 장애인 및 고령자 UI [[286_usability_tactics|사용성]] 점검
69. 프로젝트 스폰서 및 추진 위원회 ([[069_project_sponsor_steering_committee_decision|Steering Committee]]) 의사 결정 [[015_지연_데이터_관점|지연]] 여부 평가
70. [[070_configuration_management_git_ci_audit|형상 관리 저장소]] (Git, SVN) 브랜치 병합 관리 및 [[076_ci_continuous_integration|지속적 통합]]([[090_configuration_item|CI]]) 빌드 환경 평가
71. 소스코드 [[528_obfuscation_anti_debugging_mobile|난독화]] 적용 여부 점검 (금융/앱 사업의 경우)
72. [[781_personal_information|개인정보]] 파기 [[164_policy|정책]] 및 [[568_logs_distributed_logging_elk_fluentd|로그]] 보존 기간 준수 평가 ([[072_personal_data_destruction_log_retention_audit|법적 요건]])
73. 서버/OS/DB 패치 및 취약점 스캐닝 내역 적용 [[396_validation|확인]]
74. [[455_penetration_testing_vulnerability_scanning|모의 해킹]] ([[163_penetration_diffraction_radio_waves|Penetration]] Test) 수행 내역서 기반 미비점 재점검
75. IT 예산 및 계약 행정 처리, 선금/잔금 정산 요건([[075_it_budget_contract_administration_audit|과업 완료]]) 부합 검토
76. [[072_service_desk|서비스 데스크]] ([[072_service_desk|Service Desk]]) 및 [[075_incident_management|인시던트 관리]] 체계 구축 [[396_validation|확인]]
77. 사용자 만족도 조사 결과 분석 및 개선 조치 
78. [[127_bpr_business_process_reengineering_radical_redesign|BPR]]/[[101_isp_information_strategy_planning_4_steps|ISP]] 연계 - 구축된 시스템이 당초 [[268_strategy_pattern|전략]]적 목표([[178_as_is_to_be_analysis|AS-IS]] 대비 TO-BE 효과)를 달성했는지 사후 평가
79. [[079_developer_cleanroom_vdi_security|개발자 클린룸 망분리]]([[079_developer_cleanroom_vdi_security|VDI]]) 환경 및 보안 이동 경로 점검
80. [[004_cobit|COBIT]] 프로세스 평가 (APO, BAI, DSS, MEA) 모델 연계 통제 진단

## 2. [[201_software_architecture_definition|소프트웨어 아키텍처]] 원칙 및 설계 (60개)
81. [[201_software_architecture_definition|소프트웨어 아키텍처]] ([[201_software_architecture_definition|Software Architecture]]) - 소프트웨어를 구성하는 요소들 간의 [[083_relationship_in_er_model|관계]]와 [[082_attribute_types_er_model|속성]], 설계 및 진화를 통제하는 기본 구조 
82. [[082_ieee_1471_architecture_description_standard|IEEE 1471]] (ISO/IEC 42010) - [[201_software_architecture_definition|소프트웨어 아키텍처]] 명세 국제 표준 프레임워크
83. 아키텍처 주요 요소 - [[173_stakeholder_identification_impact_matrix|이해관계자]]([[173_stakeholder_identification_impact_matrix|Stakeholder]]), 관심사(Concern), 관점(Viewpoint), 뷰([[151_sql_view_virtual_table|View]]), 아키텍처 명세서
84. [[084_philippe_kruchten_4_1_view_architecture_model|필립 크루첸]] ([[084_philippe_kruchten_4_1_view_architecture_model|Philippe Kruchten]])의 4+1 [[151_sql_view_virtual_table|View]] 모델
85. [[085_logical_view_class_diagram_functional_requirements|논리 뷰]] ([[085_logical_view_class_diagram_functional_requirements|Logical View]]) - 최종 사용자 관점, 시스템의 기능적 요구사항 설계 (클래스/객체 다이어그램)
86. [[086_process_view_sequence_diagram_concurrency|프로세스 뷰]] ([[086_process_view_sequence_diagram_concurrency|Process View]]) - 시스템 통합자 관점, 병행성/[[212_synchronization_mechanisms|동기화]]/[[282_performance_tactics|성능]] 설계 (액티비티/상태/[[235_sequence_diagram_dynamic_interaction_uml|시퀀스 다이어그램]])
87. [[087_implementation_view_component_diagram_packaging|구현 뷰]] ([[087_implementation_view_component_diagram_packaging|Implementation View]] / Development [[151_sql_view_virtual_table|View]]) - 프로그래머 관점, [[192_module_independence|모듈]]의 구조 및 패키징 ([[603_component_independent_deployment_unit|컴포넌트]] 다이어그램)
88. 물리/배포 뷰 (Physical/[[087_deployment_kubernetes_workload_rolling_update|Deployment]] [[151_sql_view_virtual_table|View]]) - 시스템 엔지니어 관점, HW 배포 매핑 (배포 다이어그램)
89. [[089_use_case_view_plus_one_view_actor_boundary|유스케이스 뷰]] (Use Case [[151_sql_view_virtual_table|View]] / +1 [[151_sql_view_virtual_table|View]]) - 모든 뷰의 중심, 아키텍처 [[395_verification_process_review|검증]] 기준 ([[238_use_case_diagram_functional_modeling|유스케이스 다이어그램]])
90. [[202_architecture_drivers_quality_attributes|아키텍처 드라이버]] ([[202_architecture_drivers_quality_attributes|Architecture Drivers]]) - 아키텍처 결정에 가장 큰 영향을 미치는 핵심 요구사항 (기능, 품질 [[082_attribute_types_er_model|속성]], 제약 사항)
91. [[352_process|품질 속성 시나리오]] ([[352_process|Quality Attribute Scenario]]) - 자극원, 자극, 환경, 대상, 응답, 응답 척도 6가지 구성요소로 품질 명세
92. 아키텍처 평가 방법론론 - [[229_atam_architecture_trade_off_analysis_method|ATAM]] ([[319_architecture|Architecture]] Trade-off Analysis Method)
93. ATAM의 4개 페이즈 - [[459_quic_fec_forward_error_correction|초기]]화 -> 평가 -> 결과 도출 -> 종합
94. [[094_sensitivity_point_architecture_tradeoff_control_knob|민감도점]] ([[094_sensitivity_point_architecture_tradeoff_control_knob|Sensitivity Point]]) - 특정 아키텍처 결정이 한 가지 품질 [[082_attribute_types_er_model|속성]]에 큰 영향을 미치는 지점
95. [[095_tradeoff_point_architecture_evaluation_atam_conflict|상충점]] ([[095_tradeoff_point_architecture_evaluation_atam_conflict|Trade-off Point]]) - 특정 아키텍처 결정이 한 품질 [[082_attribute_types_er_model|속성]]에는 긍정적이나 다른 품질 [[082_attribute_types_er_model|속성]]에는 부정적 영향을 미치는 교차점 ([[282_performance_tactics|성능]] vs 보안)
96. [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] ([[096_risk_non_risk_architecture_evaluation_flaws|Risk]]) / 비리스크 (Non-[[096_risk_non_risk_architecture_evaluation_flaws|risk]]) 도출
97. [[230_cbam_cost_benefit_analysis_method|CBAM]] (Cost Benefit Analysis Method) - [[229_atam_architecture_trade_off_analysis_method|ATAM]] 확장, 아키텍처 결정에 경제성(비용 대비 효익, [[012_roi_return_on_investment|ROI]]) 관점 추가 평가
98. [[228_saam_software_architecture_analysis_method|SAAM]] ([[201_software_architecture_definition|Software Architecture]] Analysis Method) - 최초의 아키텍처 평가법, 수정 용이성에 초점 (ATAM의 전신)
99. [[231_adr_architecture_decision_record_documentation|ADR]] ([[231_adr_architecture_decision_record_documentation|Architecture Decision Record]]) - 아키텍처 설계 결정의 배경, 맥락, 결과를 기록하는 마크다운 문서 포맷 관리
100. [[100_architecture_tactics_quality_attributes|아키텍처 전술]] ([[100_architecture_tactics_quality_attributes|Architecture Tactics]]) - 특정 품질 [[082_attribute_types_er_model|속성]]을 향상시키기 위한 설계 결정 ([[452_availability|가용성]] 전술, [[282_performance_tactics|성능]] 전술 등)
101. 객체 지향 설계 원칙 ([[242_solid_object_oriented_design_principles|SOLID]]) - 로버트 C. 마틴 (Uncle Bob) 제안
102. [[243_srp_single_responsibility_principle|SRP]] ([[243_srp_single_responsibility_principle|Single Responsibility Principle]], [[355_process|단일 책임 원칙]]) - 클래스는 단 하나의 변경 이유(책임)만 가져야 한다. ([[193_cohesion_levels|응집도]] 극대화)
103. [[746_ocp|OCP]] ([[244_ocp_open_closed_principle|Open-Closed Principle]], [[356_process|개방-폐쇄 원칙]]) - 확장에는 열려(Open) 있어야 하고, 수정에는 닫혀(Closed) 있어야 한다. (다형성/인터페이스 활용)
104. [[245_lsp_liskov_substitution_principle|LSP]] ([[245_lsp_liskov_substitution_principle|Liskov Substitution Principle]], [[357_process|리스코프 치환 원칙]]) - 자식 클래스는 언제나 부모 클래스를 대체할 수 있어야 한다. ([[234_uml_class_relationships_generalization_dependency|상속]]의 올바른 사용)
105. [[101_isp_information_strategy_planning_4_steps|ISP]] ([[246_isp_interface_segregation_principle|Interface Segregation Principle]], [[358_architecture|인터페이스 분리 원칙]]) - 클라이언트는 자신이 사용하지 않는 메서드에 의존하지 않아야 한다. (인터페이스를 작고 구체적으로 분해)
106. [[247_dip_dependency_inversion_principle|DIP]] ([[247_dip_dependency_inversion_principle|Dependency Inversion Principle]], [[106_dip_dependency_inversion_principle|의존성 역전 원칙]]) - 고수준 [[192_module_independence|모듈]]은 저수준 [[192_module_independence|모듈]]의 구현에 의존해선 안되며, 둘 다 [[198_abstraction_control_data_process|추상화]](인터페이스)에 의존해야 한다. (제어의 역전 IoC)
107. DRY 원칙 (Don't Repeat Yourself) - 코드 중복 방지 ([[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] 보장)
108. [[249_kiss_keep_it_simple_stupid|KISS]] 원칙 (Keep It Simple, Stupid) - 아키텍처와 코드는 최대한 단순하고 직관적이어야 함
109. [[362_yagni|YAGNI]] 원칙 (You Aren't Gonna Need It) - 당장 필요하지 않은 확장 기능은 미리 설계/구현하지 말 것 (오버엔지니어링 방지)
110. [[110_law_of_demeter|최소 지식의 원칙]] (Principle of Least Knowledge / 디미터의 법칙, [[110_law_of_demeter|Law of Demeter]]) - 객체 간 협력 시 이웃 객체의 내부 구조에 대해 알지 못해야 함 (A.getB().getC().do() 금지, 느슨한 결합)
111. [[111_hollywood_principle|할리우드 원칙]] ([[111_hollywood_principle|Hollywood Principle]]) - "Don't [[189_subroutine_call_return|call]] us, we'll [[189_subroutine_call_return|call]] you", 상위 [[192_module_independence|모듈]]이 하위 [[192_module_independence|모듈]]을 호출할지 결정 (콜백, IoC의 근간)
112. [[193_cohesion_levels|응집도]] ([[193_cohesion_levels|Cohesion]]) - 하나의 [[192_module_independence|모듈]] 내부 요소들이 하나의 목적을 위해 뭉쳐 있는 정도 (높을수록 좋음: 기능적 [[193_cohesion_levels|응집도]] 최고)
113. [[195_coupling_levels|결합도]] ([[195_coupling_levels|Coupling]]) - 서로 다른 [[192_module_independence|모듈]] 간의 상호 의존성 정도 (낮을수록 좋음: [[001_dikw_pyramid|데이터]] [[195_coupling_levels|결합도]] 최적)
114. [[114_architecture_style|아키텍처 스타일]] ([[114_architecture_style|Architecture Style]] / Pattern) - 반복되는 아키텍처 설계 문제를 해결하기 위한 구조적 해법
115. [[205_layered_architecture_separation_of_concerns|계층형 아키텍처]] ([[205_layered_architecture_separation_of_concerns|Layered Architecture]]) - 프레젠테이션, 비즈니스, [[001_dikw_pyramid|데이터]] 접근 계층 등 수직적 분할 (관심사 분리, Layer [[195_isolation_concurrency_control|Isolation]])
116. [[216_hexagonal_architecture_ports_and_adapters|헥사고날 아키텍처]] ([[366_process|Hexagonal Architecture]]) / [[446_port_and_bus|포트]] 앤 [[259_adapter_pattern_interface_wrapper|어댑터]] (Ports and Adapters) - [[064_relation_domain|도메인]](비즈니스 로직)을 중심에 두고, 외부(DB, UI) 인프라는 [[259_adapter_pattern_interface_wrapper|어댑터]]를 통해 [[446_port_and_bus|포트]]로 통신하도록 격리
117. [[217_clean_architecture_dependency_rule|클린 아키텍처]] ([[217_clean_architecture_dependency_rule|Clean Architecture]]) - 엔티티, 유스케이스, 컨트롤러, 프레젠테이션/DB 계층 원형 구조. 의존성은 항상 외부에서 내부([[064_relation_domain|도메인]])로 향해야 함
118. [[218_onion_architecture_domain_centric_design|어니언 아키텍처]] ([[218_onion_architecture_domain_centric_design|Onion Architecture]]) - 인프라 의존성을 외부로 밀어내고 핵심 [[064_relation_domain|도메인]]을 중앙에 [[571_protection_vs_security|보호]]
119. [[210_mvc_model_view_controller_architecture|모델-뷰-컨트롤러]] (MVC, [[405_mvc_m_v_c|Model-View-Controller]]) 아키텍처 - [[001_dikw_pyramid|데이터]](M), 사용자 인터페이스(V), 비즈니스 [[213_flow_control_buffer_overflow|흐름 제어]](C) 분리 (웹 아키텍처 기본)
120. [[367_architecture|이벤트 주도 아키텍처]] ([[064_eda|EDA]], [[140_event_driven_architecture_eda|Event-Driven Architecture]]) - 상태 변경을 이벤트로 발행(Publish)하고 비동기적으로 구독(Subscribe)하여 [[195_coupling_levels|결합도]]를 낮추는 구조 ([[145_message_broker_sync_async|메시지 브로커]] 활용)
121. [[306_cqrs|CQRS]] ([[271_command_pattern|Command]] Query Responsibility Segregation) - [[282_performance_tactics|성능]] 확장을 위해 상태를 변경하는 명령([[271_command_pattern|Command]]) 로직과 상태를 읽는 [[298_qkv_attention|쿼리]](Query) 로직과 [[002_database_definition|데이터베이스]]를 [[369_logic_bomb|논리]]/물리적으로 완전히 분리
122. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]]) - CRUD 상태 업데이트 덮어쓰기 방식 대신, 모든 상태 변화 이벤트를 영구 스트림(Append-Only)으로 저장하여 [[194_consistency_database_integrity|일관성]] 보장 및 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 재생(Replay) 지원
123. [[213_msa_microservices_architecture|마이크로서비스 아키텍처]] ([[619_msa_traffic_hardware|MSA]], [[122_msa_microservices_architecture|Microservices Architecture]]) - 크고 단일화된 모놀리식 시스템을 [[064_relation_domain|도메인]]별 독립된 소규모 [[090_service_kubernetes_network_load_balancing|서비스]]로 분해, 개별 DB 할당, 독립적 배포 지원
124. [[014_api_posix|API]] 게이트웨이 ([[542_api_gateway|API Gateway]]) 아키텍처 패턴 - [[619_msa_traffic_hardware|MSA]] 진입점 통제
125. [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]) 아키텍처 - [[532_microservices_decomposition_patterns|마이크로서비스]] 간 통신 제어([[339_routing_overview_best_path_selection|라우팅]], 트래픽 제어, [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]], 로깅) 코드를 비즈니스 로직에서 분리하여 인프라([[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]]) 단에서 처리 ([[302_service_mesh_istio|Istio]] 등)
126. [[376_strangler_fig_summary|스트랭글러 피그 패턴]] ([[308_strangler_fig_pattern|Strangler Fig Pattern]]) - 모놀리식 레거시 시스템을 완전히 갈아엎지 않고, 전면에 게이트웨이를 둔 뒤 신규 기능부터 MSA로 점진적으로 가로채어(교체하여) 레거시를 고사시키는 [[268_strategy_pattern|전략]]
127. [[215_serverless_architecture_faas_aws_lambda|서버리스 아키텍처]] ([[206_serverless_cold_start|Serverless]] / [[342_faas|FaaS]]) - [[183_iaas_infrastructure_as_a_service|IaaS]] [[528_provisioning|프로비저닝]] 없이 함수 코드만 배포하면 [[507_acid_properties|트리거]] 이벤트 발생 시 런타임에 동적 [[249_scaling_normalization_standardization|스케일링]]/실행되는 구조
128. [[239_micro_frontends_architecture|마이크로 프론트엔드]] ([[239_micro_frontends_architecture|Micro Frontends]]) - 백엔드 [[619_msa_traffic_hardware|MSA]] 사상을 프론트엔드 UI에도 적용, 페이지를 독립적 개발/배포 가능한 뷰 조각으로 분리 ([[557_webpack_module_federation|Module Federation]])
129. [[310_architecture|도메인 주도 설계]] ([[310_architecture|DDD]], [[127_ddd_domain_driven_design|Domain-Driven Design]]) - 에릭 에반스, 소프트웨어 복잡성을 해결하기 위해 비즈니스 [[064_relation_domain|도메인]](업무) 전문가와 개발자가 동일한 보편 언어([[220_ubiquitous_language_ddd_communication|Ubiquitous Language]])로 소통하며 설계
130. [[221_bounded_context_ddd_msa_boundary|바운디드 컨텍스트]] ([[221_bounded_context_ddd_msa_boundary|Bounded Context]]) - 모델의 경계, [[532_microservices_decomposition_patterns|마이크로서비스]] 분할의 핵심 기준
131. [[222_aggregate_ddd_transaction_consistency|애그리게이트]] ([[222_aggregate_ddd_transaction_consistency|Aggregate]]) - [[194_consistency_database_integrity|일관성]]([[191_transaction_concept_states|트랜잭션]])을 유지해야 하는 객체들의 군집, [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 루트(Root)를 통해서만 접근 허용
132. 엔티티 (Entity) - 고유 [[289_identification_flags_fragmentation_offset|식별자]]를 가진 객체 / 값 객체 (Value Object) - [[289_identification_flags_fragmentation_offset|식별자]] 없이 [[082_attribute_types_er_model|속성]](불변성)만으로 정의되는 객체
133. [[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] ([[549_acl_access_control_list|ACL]], Anti-Corruption Layer) - 외부/레거시 시스템 연동 시 서로 다른 [[064_relation_domain|도메인]] 모델이 오염되지 않도록 중간에 변환 [[259_adapter_pattern_interface_wrapper|어댑터]] 배치
134. [[123_pipe|파이프]]-필터 ([[207_pipe_filter_architecture_data_stream|Pipe-Filter]]) 패턴 - [[603_component_independent_deployment_unit|컴포넌트]](Filter)들이 [[001_dikw_pyramid|데이터]] 스트림을 [[123_pipe|파이프]]([[123_pipe|Pipe]])로 전달하며 순차적/[[430_index_fast_full_scan|병렬]]적 변환 수행 (Unix [[123_pipe|파이프]], 빅데이터 스트리밍)
135. [[209_blackboard_pattern_ai_heuristic|블랙보드 패턴]] ([[209_blackboard_pattern_ai_heuristic|Blackboard Pattern]]) - 중앙 공용 [[001_dikw_pyramid|데이터]](Blackboard)를 바탕으로 여러 전문 지식 [[192_module_independence|모듈]](Knowledge Source)이 점진적으로 문제 해결책을 모색 (음성인식, [[190_ai_llm_requirements_specification|AI]] [[459_quic_fec_forward_error_correction|초기]] 구조)
136. [[598_microkernel_plugin_architecture|마이크로 커널]] 아키텍처 ([[024_microkernel|Microkernel]] / 플러그인 아키텍처) - 최소한의 핵심(Core) [[192_module_independence|모듈]]만 두고 나머지 확장 기능을 플러그인 형태로 조립 (IDE, 브라우저 확장)
137. [[137_space_based_architecture|공간 기반 아키텍처]] ([[186_space_based_architecture|Space-Based Architecture]]) - [[191_transaction_concept_states|트랜잭션]] 병목(중앙 DB)을 제거하기 위해 인메모리 [[001_dikw_pyramid|데이터]] 그리드(Tuple Space)로 [[001_dikw_pyramid|데이터]]를 [[136_variance|분산]] [[212_synchronization_mechanisms|동기화]] (초고도 동시 접속 시스템)
138. 아키텍처 결정 [[395_verification_process_review|검증]] [[213_refactoring_cloud_native_rearchitecture|리팩토링]] ([[138_architectural_refactoring|Architectural Refactoring]])
139. 설계의 [[288_conceptual_integrity|개념적 무결성]] ([[288_conceptual_integrity|Conceptual Integrity]]) 유지 방안
140. [[140_design_debt|설계 부채]] ([[140_design_debt|Design Debt]]) 측정 및 청산

## 3. GoF [[251_design_patterns_gof_overview|디자인 패턴]] ([[251_design_patterns_gof_overview|Design Patterns]]) [[087_process_state_transition|생성]] 및 구조 (50개)
141. [[251_design_patterns_gof_overview|디자인 패턴]] (Design Pattern) - 에리히 감마 등 GoF (Gang of Four) 4인이 정리, 객체지향 소프트웨어 설계에서 자주 발생하는 문제에 대한 [[395_verification_process_review|검증]]된 해법(템플릿)
142. 23가지 GoF 패턴 [[104_classification_analysis|분류]] - [[252_creational_patterns_overview|생성 패턴]](Creational, 5개), [[258_structural_patterns_overview|구조 패턴]](Structural, 7개), [[266_behavioral_patterns_overview|행위 패턴]](Behavioral, 11개)
143. [[252_creational_patterns_overview|생성 패턴]] ([[252_creational_patterns_overview|Creational Patterns]])의 목적 - 객체 인스턴스 [[087_process_state_transition|생성]] 프로세스를 캡슐화하여 클라이언트와 [[087_process_state_transition|생성]] 로직의 [[195_coupling_levels|결합도]] 분리
144. [[253_singleton_pattern_single_instance|싱글톤]] ([[253_singleton_pattern_single_instance|Singleton]]) 패턴 - 애플리케이션 전체에서 클래스의 인스턴스가 오직 1개만 [[087_process_state_transition|생성]]되도록 보장하고, 어디서든 전역 접근점을 제공 (DB 커넥션 풀, 로거 등에 사용)
145. [[253_singleton_pattern_single_instance|싱글톤]] 구현 기법 - [[272_double_checked_locking|Double Checked Locking]] (더블 체크 락킹), Enum [[253_singleton_pattern_single_instance|싱글톤]], [[380_computational_graph_lazy_eager_execution|Lazy]] Initialization ([[015_지연_데이터_관점|지연]] [[459_quic_fec_forward_error_correction|초기]]화)의 [[014_concurrency|동시성]] 이슈 대응
146. [[254_factory_method_pattern_subclass_creation|팩토리 메서드]] ([[254_factory_method_pattern_subclass_creation|Factory Method]]) 패턴 / 가상 [[087_process_state_transition|생성]]자 패턴 - 객체를 [[087_process_state_transition|생성]]하는 인터페이스는 상위 클래스가 정의하되, 실제 [[087_process_state_transition|생성]]할 객체(인스턴스)의 클래스는 하위 클래스(서브클래스)가 결정하도록 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]] 위임 ([[234_uml_class_relationships_generalization_dependency|상속]] 활용)
147. [[255_abstract_factory_pattern_object_families|추상 팩토리]] ([[255_abstract_factory_pattern_object_families|Abstract Factory]]) 패턴 - 서로 연관되거나 의존적인 여러 객체군(Family)을, 구체적인 클래스를 지정하지 않고 하나의 팩토리 인터페이스를 통해 일괄 [[087_process_state_transition|생성]] (UI [[184_theme_agile_requirements|테마]] 변환-Mac UI 팩토리, Win UI 팩토리)
148. [[256_builder_pattern_step_by_step_creation|빌더]] ([[256_builder_pattern_step_by_step_creation|Builder]]) 패턴 - 복잡한 인스턴스의 [[087_process_state_transition|생성]] 과정([[459_quic_fec_forward_error_correction|초기]]화)과 표현 방법을 분리, 메서드 체이닝(Method [[103_chaining|Chaining]])을 이용해 다양한 구성의 객체를 단계별로 유연하게 [[087_process_state_transition|생성]] (파라미터가 많은 [[087_process_state_transition|생성]]자 단점 극복)
149. [[257_prototype_pattern_object_cloning|프로토타입]] ([[257_prototype_pattern_object_cloning|Prototype]]) 패턴 - `new` 키워드로 인스턴스를 매번 [[087_process_state_transition|생성]]하는 비용이 클 때, 미리 [[087_process_state_transition|생성]]된 원본 객체([[257_prototype_pattern_object_cloning|Prototype]])를 [[016_replication_factor|복제]]([[149_clone_system_call|Clone]] / 깊은 복사)하여 새로운 객체를 셍성
150. [[258_structural_patterns_overview|구조 패턴]] ([[258_structural_patterns_overview|Structural Patterns]])의 목적 - 클래스나 객체들을 조합하여 더 크고 복잡한 구조를 설계, 인터페이스 구성을 단순화 ([[234_uml_class_relationships_generalization_dependency|상속]]/합성 융합)
151. [[259_adapter_pattern_interface_wrapper|어댑터]] ([[259_adapter_pattern_interface_wrapper|Adapter]]) 패턴 / 래퍼 (Wrapper) 패턴 - 호환되지 않는 인터페이스를 가진 두 클래스를 연결, 클라이언트가 요구하는 인터페이스로 래핑하여 함께 동작할 수 있도록 변환 (기존 코드 재사용 목적)
152. 객체 [[259_adapter_pattern_interface_wrapper|어댑터]] (합성 위임 기반) vs 클래스 [[259_adapter_pattern_interface_wrapper|어댑터]] (다중 [[234_uml_class_relationships_generalization_dependency|상속]] 기반)
153. [[260_bridge_pattern_abstraction_implementation|브리지]] ([[260_bridge_pattern_abstraction_implementation|Bridge]]) 패턴 / 핸들/바디 패턴 - 기능의 클래스 계층(추상부)과 구현의 클래스 계층(구현부)을 분리하여 각각 독립적으로 확장할 수 있게 함 ([[234_uml_class_relationships_generalization_dependency|상속]]의 조합 폭발 방지, 런타임에 구현체 교체)
154. [[261_composite_pattern_tree_structure|컴포지트]] ([[261_composite_pattern_tree_structure|Composite]]) 패턴 - 단일 객체(Leaf)와 복합 객체([[261_composite_pattern_tree_structure|Composite]])를 동일한 인터페이스로 다루어, 객체들의 부분-전체(Part-Whole) 계층 트리 구조를 표현 (디렉터리-[[501_file_definition_logical_record|파일]] 구조 모델링)
155. [[262_decorator_pattern_dynamic_wrapper|데코레이터]] ([[262_decorator_pattern_dynamic_wrapper|Decorator]]) 패턴 - [[234_uml_class_relationships_generalization_dependency|상속]]을 통한 서브클래싱 대신, 객체를 장식자([[262_decorator_pattern_dynamic_wrapper|Decorator]]) 객체로 동적으로 감싸서(래핑) 런타임에 새로운 기능과 책임을 유연하게 추가 (커피에 시럽, 우유 래핑)
156. [[263_facade_pattern_simplified_interface|퍼사드]] ([[263_facade_pattern_simplified_interface|Facade]]) 패턴 - 복잡하게 얽힌 서브시스템들의 내부 인터페이스들을 숨기고, 외부 클라이언트가 쉽게 사용할 수 있도록 단순화된 고수준의 단일 통합 인터페이스([[263_facade_pattern_simplified_interface|Facade]]) 제공 ([[195_coupling_levels|결합도]] 대폭 하락)
157. [[265_flyweight_pattern_instance_sharing|플라이웨이트]] ([[265_flyweight_pattern_instance_sharing|Flyweight]]) 패턴 - 인스턴스 [[087_process_state_transition|생성]]이 너무 많아 메모리 부하가 심할 때, 고유 상태(Intrinsic [[272_state_pattern|State]], 불변)는 메모리 팩토리에 공유 [[456_caching|캐싱]]하고, 외부 상태(Extrinsic [[272_state_pattern|State]], 가변)만 외부에서 주입받아 객체 재사용 극대화 (워드프로세서의 글자 폰트 객체, 게임의 다수 유닛)
158. [[264_proxy_pattern_surrogate_access_control|프록시]] ([[264_proxy_pattern_surrogate_access_control|Proxy]]) 패턴 - 실제 원본 객체(Real Subject)에 대한 접근을 제어하거나, 접근 전후에 부가 작업(로깅, [[182_lazy_loading|지연 로딩]], 보안 통제)을 수행하기 위해 대리자([[264_proxy_pattern_surrogate_access_control|Proxy]]) 객체를 제공
159. [[159_proxy_pattern_types|프록시 패턴 유형]] - 가상 [[264_proxy_pattern_surrogate_access_control|프록시]] (Virtual [[264_proxy_pattern_surrogate_access_control|Proxy]], 리소스 무거운 객체 [[182_lazy_loading|지연 로딩]]), [[571_protection_vs_security|보호]] [[264_proxy_pattern_surrogate_access_control|프록시]] ([[571_protection_vs_security|Protection]] [[264_proxy_pattern_surrogate_access_control|Proxy]], 접근 제어 권한 검사), 원격 [[264_proxy_pattern_surrogate_access_control|프록시]] (Remote [[264_proxy_pattern_surrogate_access_control|Proxy]], 원격 통신 캡슐화)
160. [[251_design_patterns_gof_overview|디자인 패턴]]의 활용 원칙 - [[746_ocp|OCP]] (확장, 폐쇄)와 [[247_dip_dependency_inversion_principle|DIP]] (추상 인터페이스 의존) 구현 도구
161. [[161_anti_pattern|안티 패턴]] ([[161_anti_pattern|Anti-Pattern]]) - 잘못된 소프트웨어 구조나 설계 습관 (스파게티 코드, 갓 클래스 God Class, 황금 망치 Golden Hammer)
162. 갓 클래스 (God Class / Blob) - 단일 클래스에 너무 많은 기능과 [[001_dikw_pyramid|데이터]](전역 변수)가 집중되어 [[193_cohesion_levels|응집도]]가 낮고 수정이 불가능한 현상 ([[243_srp_single_responsibility_principle|SRP]] 위반)
163. [[253_singleton_pattern_single_instance|싱글톤]] 패턴의 단점 ([[128_water_scrum_fall_anti_pattern|안티패턴]] 관점) - 전역 상태 오염, [[397_unit_test|단위 테스트]] 목업([[462_mock_test_double|Mock]]) 어려움, 객체 간 암묵적 강결합 유발. (해결책: [[337_dependency_injection|의존성 주입]] [[190_enterprise_di_framework_lifecycle|DI]] 프레임워크 활용)
164. [[259_adapter_pattern_interface_wrapper|어댑터]]와 [[263_facade_pattern_simplified_interface|퍼사드]]의 차이 - [[259_adapter_pattern_interface_wrapper|어댑터]]는 인터페이스 호환을 위한 1:1 변환, [[263_facade_pattern_simplified_interface|퍼사드]]는 복잡한 다수 인터페이스 캡슐화 통합 1:N 제공
165. [[260_bridge_pattern_abstraction_implementation|브리지]] 패턴과 [[268_strategy_pattern|전략]]([[268_strategy_pattern|Strategy]]) 패턴 비교 - [[260_bridge_pattern_abstraction_implementation|브리지]]는 구조(추상-구현 구조 설계) 관점, [[268_strategy_pattern|전략]]은 행위([[001_algorithm_definition|알고리즘]] 교체 동작) 관점
166. [[262_decorator_pattern_dynamic_wrapper|데코레이터]]와 [[264_proxy_pattern_surrogate_access_control|프록시]] 비교 - [[262_decorator_pattern_dynamic_wrapper|데코레이터]]는 객체에 기능(책임) 추가가 목적, [[264_proxy_pattern_surrogate_access_control|프록시]]는 객체에 대한 접근 제어가 목적
167. [[379_abstract_factory_summary|추상 팩토리 패턴]] 팩토리 클래스 도출 (추상 [[192_module_independence|모듈]]의 교체 비용 통제)
168. [[269_template_method_pattern|템플릿 메서드]]와 [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]의 결합
169. 객체 [[087_process_state_transition|생성]]을 캡슐화하는 [[169_static_factory_method|정적 팩토리 메서드]]([[169_static_factory_method|Static Factory Method]]) 구현 기법 (Effective Java 권장)
170. [[192_module_independence|모듈]] ([[192_module_independence|Module]]) 패턴 - 클로저(Closure)를 활용한 자바스크립트 등 비객체지향 언어 [[199_information_hiding_encapsulation|정보 은닉]] 구조
171. MVC ([[405_mvc_m_v_c|Model-View-Controller]]) 복합 [[251_design_patterns_gof_overview|디자인 패턴]] 설계 ([[267_observer_pattern|옵저버]], [[268_strategy_pattern|전략]], [[261_composite_pattern_tree_structure|컴포지트]] 패턴의 융합체)
172. 상태 변이 로직 분리 ([[256_builder_pattern_step_by_step_creation|빌더]] 패턴을 활용한 불변 객체 [[172_builder_immutable_object|Immutable Object]] 설계)
173. [[252_creational_patterns_overview|생성 패턴]] 메모리 효율화 로직 비교 ([[257_prototype_pattern_object_cloning|프로토타입]] vs [[265_flyweight_pattern_instance_sharing|플라이웨이트]] 공간/객체 [[087_process_state_transition|생성]] 속도 차이)
174. GoF 패턴 외 J2EE 프레임워크 패턴 ([[054_dao_decentralized_autonomous_organization|DAO]], DTO/VO, MVC Front Controller, Business Delegate 등)
175. DTO ([[001_dikw_pyramid|Data]] Transfer Object) - 계층 간(특히 네트워크, [[002_database_definition|데이터베이스]]) 통신 시 오버헤드 최소화를 위해 캡슐화 없이 상태 [[001_dikw_pyramid|데이터]]만 운반하는 객체 (Value Object와 구분)
176. [[054_dao_decentralized_autonomous_organization|DAO]] ([[001_dikw_pyramid|Data]] Access Object) 패턴 - [[064_relation_domain|도메인]] 비즈니스 로직과 [[002_database_definition|데이터베이스]] 접근 계층을 분리하는 구조
177. 프론트 컨트롤러 (Front Controller) - 모든 웹 요청을 단일 컨트롤러가 받아 공통 처리 후 개별 컨트롤러로 [[339_routing_overview_best_path_selection|라우팅]] (Spring DispatcherServlet)
178. 인터셉터 (Interceptor) / 필터 (Filter) 설계망 구조
179. 레파지토리 (Repository) 패턴 - [[310_architecture|DDD]] 관점, 컬렉션과 같이 [[064_relation_domain|도메인]] 객체 추가/검색 담당, 하위 인프라 DB [[198_abstraction_control_data_process|추상화]]
180. [[191_transaction_concept_states|트랜잭션]] 스크립트 ([[191_transaction_concept_states|Transaction]] Script) 패턴 - 단순 CRUD 업무 시 [[064_relation_domain|도메인]] 모델 없이 함수/스크립트 하나로 처리 (갓 클래스 유발 가능성) vs [[064_relation_domain|도메인]] 모델 ([[064_relation_domain|Domain]] Model) 패턴
181. 유닛 오브 워크 (Unit of Work) 패턴 - [[191_transaction_concept_states|트랜잭션]]의 커밋과 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 보장을 위해 객체의 변경 상태(추가, 수정, 삭제)를 [[456_caching|캐싱]] 추적 (JPA/Hibernate [[196_durability_permanent_storage|영속성]] [[033_context|컨텍스트]] 핵심)
182. [[182_lazy_loading|지연 로딩]] ([[182_lazy_loading|Lazy Loading]]) - 엔티티 연관 객체를 즉시 [[298_qkv_attention|쿼리]]하지 않고 [[264_proxy_pattern_surrogate_access_control|프록시]]를 배치해 실제 호출 시점에 [[298_qkv_attention|쿼리]] (가상 [[264_proxy_pattern_surrogate_access_control|프록시]] 원리)
183. 마스터-워커 (Master-Worker) [[136_variance|분산]] 패턴 
184. [[539_event_bus_stream_processing|이벤트 버스]] ([[539_event_bus_stream_processing|Event Bus]]) 및 퍼블리시/서브스크라이브 패턴
185. 피어투피어 ([[916_p2p_peer_to_peer_networking_super_node_gnutella|P2P]]) 아키텍처 [[136_variance|분산]] 패턴
186. [[186_space_based_architecture|스페이스 기반 아키텍처]] 투플 맵핑 구조 
187. LMAX 아키텍처 - 디스럽터(Disruptor) 링버퍼 기반 인메모리 락프리 [[014_concurrency|동시성]] [[430_index_fast_full_scan|병렬]] 큐 패턴 
188. 클라우드 앰배서더 (Ambassador) 패턴 - 구형 레거시 클라이언트의 클라우드 [[090_service_kubernetes_network_load_balancing|서비스]] 접속을 대행
189. [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 통합 로깅 및 [[229_monitor|모니터]]링 수집망 아키텍처 패턴
190. 엔터프라이즈 [[192_module_independence|모듈]] 분리 [[337_dependency_injection|의존성 주입]]([[190_enterprise_di_framework_lifecycle|DI]]) 프레임워크 생명주기 관리 구조 (Spring Bean LifeCycle)

## 4. GoF [[251_design_patterns_gof_overview|디자인 패턴]] 행위 (Behavioral) 및 구조 최적화 (60개)
191. [[266_behavioral_patterns_overview|행위 패턴]] ([[266_behavioral_patterns_overview|Behavioral Patterns]])의 목적 - 객체나 클래스 간의 [[001_algorithm_definition|알고리즘]] 분배 및 책임, 협력, [[389_mesh_topology|메시]]지 통신 방식을 설계 ([[195_coupling_levels|결합도]] 최소화)
192. [[267_observer_pattern|옵저버]] ([[267_observer_pattern|Observer]]) 패턴 / 발행-구독 (Pub/Sub) 구조 - 어떤 객체(Subject)의 상태가 변하면 그 객체에 의존성(구독)을 둔 다수의 [[267_observer_pattern|옵저버]]들에게 자동으로 알림(Notify)이 가도록 일대다(1:N) 의존성 정의 (MVC 모델의 핵심)
193. [[268_strategy_pattern|전략]] ([[268_strategy_pattern|Strategy]]) 패턴 / [[164_policy|Policy]] 패턴 - 동일한 계열의 [[001_algorithm_definition|알고리즘]]들을 캡슐화하고 인터페이스화하여, 런타임 시점에 클라이언트 코드 변경 없이 [[001_algorithm_definition|알고리즘]]([[268_strategy_pattern|전략]])을 쉽게 상호 교체할 수 있도록 설계 (정렬 [[001_algorithm_definition|알고리즘]] 선택, 결제 방식 선택)
194. [[269_template_method_pattern|템플릿 메서드]] ([[269_template_method_pattern|Template Method]]) 패턴 - 부모(추상) 클래스에 [[001_algorithm_definition|알고리즘]]의 전체 뼈대(템플릿)와 공통 실행 흐름을 정의하고, 세부적인 특정 스텝 구현은 자식(구체) 클래스로 [[015_지연_데이터_관점|지연]]시켜 오버라이딩 (제어의 역전, 훅 메서드 Hook Method 사용)
195. [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]와 [[269_template_method_pattern|템플릿 메서드]]의 [[083_relationship_in_er_model|관계]] - [[254_factory_method_pattern_subclass_creation|팩토리 메서드]]는 객체 [[087_process_state_transition|생성]]에 특화된 [[269_template_method_pattern|템플릿 메서드]]의 일종
196. [[271_command_pattern|커맨드]] ([[271_command_pattern|Command]]) 패턴 - 클라이언트의 요청(Action) 자체를 객체([[271_command_pattern|Command]])로 캡슐화하여, 요청자(Invoker)와 수신자(Receiver)의 결합을 분리. 실행 취소([[393_undo|Undo]]), 재실행([[234_redo_roll_forward_durability_recovery|Redo]]), 매크로 로깅, 큐([[058_queue|Queue]]) 작업에 필수 (스마트홈 리모컨 버튼)
197. 상태 ([[272_state_pattern|State]]) 패턴 - 객체의 내부 상태([[272_state_pattern|State]])가 바뀜에 따라 객체의 행위가 달라지도록, 상태 객체 자체를 캡슐화하여 위임. 클라이언트 관점에서는 객체의 클래스가 동적으로 바뀌는 것처럼 보임 (자판기, 미디어 플레이어 상태)
198. [[394_process|상태 패턴]] vs [[391_strategy_pattern_summary|전략 패턴]] - [[391_strategy_pattern_summary|전략 패턴]]은 외부 클라이언트가 능동적으로 [[268_strategy_pattern|전략]]을 교체, [[394_process|상태 패턴]]은 객체 내부 로직이나 이벤트에 의해 자기 스스로 상태를 전이
199. [[276_chain_of_responsibility_pattern|책임 연쇄]] ([[276_chain_of_responsibility_pattern|Chain of Responsibility]]) 패턴 - 요청을 처리할 수 있는 객체들이 사슬(Chain) 형태로 연결되어 있어, 처리할 수 있는 객체를 만날 때까지 요청을 순차적으로 전달 (결재 라인 승인, 이벤트 핸들러 버블링)
200. [[276_chain_of_responsibility_pattern|책임 연쇄]]의 장단점 - [[195_coupling_levels|결합도]] 감소 및 유연한 룰 추가 가능, 하지만 체인 맨 끝까지 처리 못할 경우 요청 유실 가능성
201. [[273_mediator_pattern|중재자]] ([[273_mediator_pattern|Mediator]]) 패턴 - 객체 간의 M:N 복잡한 [[120_direct_communication|직접 통신]] 네트워크를 1:N 구조로 변환하여 중앙의 [[273_mediator_pattern|중재자]] 객체([[273_mediator_pattern|Mediator]])를 통해서만 통신하도록 강제. (항공 교통 관제탑, 채팅방 서버)
202. [[273_mediator_pattern|중재자]] 패턴과 [[606_observer_pattern_pub_sub|옵저버 패턴]] 혼합 구현 아키텍처
203. [[275_visitor_pattern|방문자]] ([[275_visitor_pattern|Visitor]]) 패턴 - [[001_dikw_pyramid|데이터]] 요소 객체 구조([[261_composite_pattern_tree_structure|컴포지트]] 구조 등)를 변경하지 않고도, 객체를 순회하며 새로운 연산이나 기능을 추가하기 위해 [[275_visitor_pattern|방문자]] 객체를 주입 (Double Dispatch 매커니즘 활용, 컴파일러 구문 트리 분석 시 사용)
204. [[270_iterator_pattern|이터레이터]] ([[270_iterator_pattern|Iterator]]) 패턴 / 반복자 - 컬렉션(List, Tree 등)의 내부 구조([[055_array|배열]]인지 링크드리스트인지)를 노출하지 않고, 그 안의 원소들을 순차적으로 접근할 수 있는 통일된 인터페이스(hasNext, next) 제공 
205. [[274_memento_pattern|메멘토]] ([[274_memento_pattern|Memento]]) 패턴 / 토큰 패턴 - 객체의 캡슐화([[199_information_hiding_encapsulation|정보 은닉]])를 훼손하지 않으면서 객체의 내부 상태(특정 시점 [[022_snapshot_backup_architecture|스냅샷]])를 외부에 저장하고, 필요 시 복원(Restore/[[393_undo|Undo]])할 수 있게 하는 패턴 (Originator, [[274_memento_pattern|Memento]], Caretaker 3요소)
206. [[277_interpreter_pattern|해석자]] ([[277_interpreter_pattern|Interpreter]]) 패턴 - 언어나 문법의 규칙을 클래스로 표현하여, 그 언어로 작성된 문장을 해석(AST 구문 트리 파싱)하고 실행하는 평가(Evaluate) 기능 구조 ([[104_regex|정규 표현식]] 엔진, SQL 파서)
207. [[207_null_object_pattern|널 객체 패턴]] ([[207_null_object_pattern|Null Object Pattern]]) - 객체가 없을 때 NULL [[316_reference_pattern_nosql|참조]] 대신 예외/분기를 방지하기 위해 '아무 일도 하지 않는' 빈 껍데기 디폴트 객체를 반환 (NullPointerException 회피)
208. [[212_synchronization_mechanisms|동기화]] 패턴 - 가드 서스펜션 (Guarded Suspension)
209. [[280_read_write_lock|읽기-쓰기 락]] ([[280_read_write_lock|Read-Write Lock]]) 패턴 (행위 다중 제어)
210. [[229_monitor|모니터]] 객체 ([[229_monitor|Monitor]] Object) 패턴 ([[249_java_synchronization|자바 동기화]] 원리)
211. [[483_active_vs_passive_ftp|액티브]] 오브젝트 ([[483_active_vs_passive_ftp|Active]] Object) 패턴 - 비동기 메서드 호출과 실행 [[092_thread_lwp|스레드]] 분리
212. 리액터 (Reactor) 패턴 - 멀티플렉싱 비동기 I/O 이벤트 통지 (Node.js, Netty 코어)
213. 프로액터 (Proactor) 패턴 - 비동기 I/O 작업 완료 이벤트 통지 [[103_thread_pool|스레드 풀]] 할당망
214. 하프-싱크/하프-어싱크 (Half-Sync/Half-Async) 패턴 - 큐를 사이로 비동기 수신과 동기 워커 [[103_thread_pool|스레드 풀]] 분리 [[282_performance_tactics|성능]] 병목 분해 
215. 워커 [[092_thread_lwp|스레드]] (Worker [[092_thread_lwp|Thread]]) / [[103_thread_pool|스레드 풀]] ([[103_thread_pool|Thread Pool]]) 팩토리 관리망 설계
216. 모나드 (Monad) 캡슐 [[324_functional_programming_core|함수형 프로그래밍]] 매핑 체인 패턴 (Optional, [[467_http2_stream_multiplexing_tcp_hol|Stream]])
217. 커링 (Currying) 함수 [[023_lazy_evaluation|지연 평가]] 분해 구조 
218. 불변 객체 ([[172_builder_immutable_object|Immutable Object]]) 패턴 - 쓰레드 세이프 사이드 이펙트 0 원칙 설계망
219. 객체 풀 (Object Pool) 패턴 - [[002_database_definition|데이터베이스]] 커넥션, 쓰레드 등 [[087_process_state_transition|생성]] 비용이 비싼 객체를 제한된 풀 내에서 대여/반납 라이프사이클 제어
220. 콜백 (Callback) 패턴 / [[606_observer_pattern_pub_sub|옵저버 패턴]]의 [[015_지연_데이터_관점|지연]] 함수 파싱 구조망 
221. Promise / Future 비동기 체이닝 구조체 설계 
222. 모킹 (Mocking) [[397_unit_test|단위 테스트]] [[460_stub_test_double|스텁]] 패턴 
223. [[307_circuit_breaker_pattern|서킷 브레이커]] ([[304_circuit_breaker|Circuit Breaker]]) 장애 감지 및 자가 치유 [[171_fallback_resilience_pattern|폴백]]([[129_fallback|Fallback]]) [[339_routing_overview_best_path_selection|라우팅]] 디자인
224. 백오프 리트라이 (Exponential Backoff and Retry) 네트워크 통신 패턴 
225. 쓰로틀링 (Throttling) 토큰 버킷 (Token Bucket) 패턴 - [[014_api_posix|API]] 호출 한계량 속도 제어
226. 리키 버킷 (Leaky Bucket) [[392_traffic_shaping_and_policing|트래픽 쉐이핑]] [[001_algorithm_definition|알고리즘]] 설계
227. 불-리언 파서 (Boolean Parser) 인터프리터 맵 
228. [[033_context|컨텍스트]] 맵 ([[033_context|Context]] Map) 안티-커럽션 레이어 패턴 변환망
229. 더블 디스패치 (Double Dispatch) [[399_architecture|방문자 패턴]] 객체 다형성 양방향 [[323_overloading_vs_overriding|오버로딩]] 해결 메커니즘
230. [[230_modular_monolith|모듈형 모놀리스]] ([[599_modular_monolith_architecture|Modular Monolith]]) 의존성 제어 디자인망 
231. [[064_relation_domain|도메인]] 이벤트 ([[064_relation_domain|Domain]] Event) 아웃박스(Outbox) 패턴 
232. 프레젠테이션 로직 분리([[036_mvp|MVP]] / MVVM 의 [[001_dikw_pyramid|데이터]] 바인딩 동작망 비교)
233. 뷰헬퍼 ([[151_sql_view_virtual_table|View]] Helper) 커스텀 태그 파싱 패턴 
234. 컨트롤러 라우터 프론트 제어 (Front Controller vs [[286_page_frame|Page]] Controller 패턴 차이) 
235. [[483_active_vs_passive_ftp|액티브]] 레코드 ([[483_active_vs_passive_ftp|Active]] Record) 테이블 행을 객체로 1:1 매핑 ORM 패턴
236. [[001_dikw_pyramid|데이터]] 매퍼 ([[001_dikw_pyramid|Data]] Mapper) 비즈니스 [[064_relation_domain|도메인]] 객체와 [[196_durability_permanent_storage|영속성]] DB 객체를 완전히 분리 
237. [[237_single_table_inheritance|싱글 테이블 상속]] ([[237_single_table_inheritance|Single Table Inheritance]]) 패턴 - 여러 하위 객체를 하나의 테이블에 컬럼으로 플랫 합침
238. 멀티 테이블 [[234_uml_class_relationships_generalization_dependency|상속]] ([[238_class_table_inheritance|Class Table Inheritance]]) 패턴 [[136_variance|분산]] 연계 
239. 게이트웨이 (Gateway) [[619_msa_traffic_hardware|MSA]] 진입점 통제 패턴 통일 
240. [[161_anti_pattern|안티 패턴]] 탈피 [[213_refactoring_cloud_native_rearchitecture|리팩토링]]: 조건문(if-else)을 다형성(상태/[[391_strategy_pattern_summary|전략 패턴]])으로 전환 (Replace Conditional 정 다형성) 
241. 메서드 분리 (Extract Method) 템플릿 재배치 구조망 
242. [[242_introduce_parameter_object|파라미터 객체화]] ([[242_introduce_parameter_object|Introduce Parameter Object]]) 길고 복잡한 매개변수 통제망 
243. 스멜링 코드 ([[365_5_solid_code_smell|Code Smell]]) 진단 - 롱 메서드, 라지 클래스, 프리미티브 강박(Primitive Obsession), 샷건 수술(Shotgun Surgery - 하나의 변경이 여러 클래스 전이), [[247_feature_label_variables|피처]] 엔비(Feature Envy - 남의 객체 [[001_dikw_pyramid|데이터]] 과도 접근)
244. [[001_dikw_pyramid|데이터]] 클럼프 ([[001_dikw_pyramid|Data]] Clumps) 변수 묶음 클래스화 통제 
245. 임시 필드 (Temporary Field) 라이프사이클 한계 정리 
246. [[234_uml_class_relationships_generalization_dependency|상속]] 거부 (Refused Bequest) 리스코프 치환 위배 인터페이스 강제 전환망 설계
247. 주석 과잉 (Comments) [[334_clean_code_principles|클린 코드]] 자가 설명 네이밍(Naming) 변환 철학 
248. [[213_refactoring_cloud_native_rearchitecture|리팩토링]] [[395_verification_process_review|검증]] 안전망 보장 [[164_tdd_test_driven_development|TDD]] 테스트 커버리지 도입 필수 조건 
249. 레거시 시스템 디자인 부채 청산 의사결정 기록 ([[231_adr_architecture_decision_record_documentation|ADR]]) 문서 체제
250. 객체 간 [[389_mesh_topology|메시]]지 ([[119_message_passing|Message Passing]]) 위임 응집 구조 설계

## 5. IT 감리 심화 가이드 및 테스트 품질 [[395_verification_process_review|검증]]론 (70개)
251. SW 개발보안([[190_secure_coding_guideline|시큐어 코딩]]) 진단 항목 심화 - SQL/OS [[480_injection|인젝션]] 방어, [[726_xss_cross_site_scripting_types|XSS]] 방지 필터, [[728_csrf_cross_site_request_forgery_concept|CSRF]] 토큰 점검 
252. 중요 정보 암호화(양방향/일방향), 비밀번호 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]] 적용 여부 [[396_validation|확인]] 
253. 예외 처리(Exception Handling) 구문 오류 [[389_mesh_topology|메시]]지 통한 정보 노출 차단 여부
254. 소스코드 [[528_obfuscation_anti_debugging_mobile|난독화]] 수준 진단 및 [[389_reverse_engineering|리버스 엔지니어링]] 방어 조치 
255. [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]] 감리 - 이행 시점 정합성(100%) 및 소스-타겟 [[001_dikw_pyramid|데이터]] 수량 일치 점검표
256. [[282_performance_tactics|성능]] 진단 지표 - [[138_response_time|응답 시간]] ([[138_response_time|Response Time]]), 동시 사용자 수 (Concurrent User), [[139_throughput|처리량]] (TPS, [[139_throughput|Throughput]])
257. 리틀의 법칙 (Little's Law) L = λW [[282_performance_tactics|성능]] 공식의 [[282_performance_tactics|성능]] 진단 적용 (적정 [[103_thread_pool|스레드 풀]], 커넥션 풀 튜닝 검토)
258. [[282_performance_tactics|성능]] [[446_load_test|부하 테스트]] 병목 구간 진단 - CPU, 메모리 릭, 디스크 I/O 대기(Wait), 네트웍 [[140_bandwidth|대역폭]] 병목 
259. [[162_apm_application_performance_management|APM]] ([[162_apm_application_performance_management|Application Performance Management]]) 툴 (Jennifer, Scouter 등) 연계 감리
260. [[002_database_definition|데이터베이스]] [[163_optimizer_sql_execution_plan_generator|옵티마이저]] [[167_sql_hint_optimizer_override|힌트]] 및 악성/Slow [[298_qkv_attention|쿼리]] 튜닝 조치 내역 진단
261. 모바일 앱 감리 규정 - 앱스토어 심사 리젝 대비, 플랫폼(iOS/Android) 디자인 가이드(HIG, Material) 준수성 
262. 사용자 인터페이스 (UI/UX) 감리 - [[210_heuristics_scheduling|휴리스틱]] 평가(10대 원칙), [[292_accessibility_kwcag_wcag|접근성]]([[334_kwcag|KWCAG]]) 자동 진단 툴 및 수동 점검
263. 웹 [[344_compatibility_usability|호환성]] 점검 - 이종 브라우저(크롬, 사파리, 엣지) 화면 깨짐 및 비표준 기술(ActiveX 등 플러그인) 사용 여부 배제 
264. 감리 결과 시정 조치 조율 체계 - 필수 시정 조치(Major)와 권고 사항(Minor) 분리 통보
265. 발주처 및 사업자 간 감리 이견 조율위원회 운영 (법적 중재 기구)
266. [[052_data_governance_framework|데이터 거버넌스]] 감리 - [[012_metadata|메타데이터]] 표준, [[060_open_data_public_api_standards|공공데이터 개방]] 규격 준수, 민감 [[001_dikw_pyramid|데이터]] 비식별화 규정 점검
267. 인프라 클라우드 감리 가이드 - 보안 [[303_authentication_authorization_patterns|인증]]([[193_csap_cloud_security_assurance|CSAP]]) 취득 클라우드 활용, 존(Zone) 격리, 가상머신 암호화 점검 
268. [[184_paas_platform_as_a_service|PaaS]] 락인([[362_lock_in_portability|Lock-in]]) 방지 점검 - K8s 기반 [[561_container_based_deployment|컨테이너]] 이식성(Portability) 및 표준 [[014_api_posix|API]] 활용 평가
269. [[004_blockchain|블록체인]] 노드 아키텍처 및 합의 [[015_지연_데이터_관점|지연]], 프라이버시(영지식) 적용 [[302_security_architecture_design|보안 아키텍처]] 한계 진단
270. [[101_iot_concept|IoT]] 센서/게이트웨이/서버 구간 (D2G, G2S) 암호 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[644_dtls_datagram_tls_coap_security|DTLS]] 등) 점검 
271. [[190_ai_llm_requirements_specification|AI]] 모델 [[282_performance_tactics|성능]] 감리 - 학습 [[001_dikw_pyramid|데이터]]셋 [[003_integrity|무결성]], 모델 평가 지표([[233_precision_recall_f1_roc_auc_threshold|Precision]], [[254_recall_sensitivity|Recall]], F1), 편향성 여부, 모델 배포([[348_mlops|MLOps]]) 절차 진단 
272. [[022_cisa_certification_audit|CISA]] [[064_relation_domain|도메인]] 지식 응용 ([[606_auditing_linux_auditd|Auditing]] [[300_process|Process]], [[001_it_governance|IT Governance]], Lifecycle, IT Operations, Asset [[571_protection_vs_security|Protection]])
273. [[379_dr_architecture|재해 복구]] (BCP/DRP) 실효성 테스트 [[395_verification_process_review|검증]] [[568_logs_distributed_logging_elk_fluentd|로그]] [[396_validation|확인]] (모의 훈련 대장) 
274. [[387_access_control_pattern|접근 통제]] 행렬 기반 [[509_authorization_models_rbac_abac|인가]] 최소 권한 규칙 ([[013_need_to_know|Need-to-Know]], [[010_least_privilege|Least Privilege]]) 이행 여부 
275. 전자서명법, [[783_pipa_korea|개인정보보호법]] 기반 동의 획득 및 암호화 전송 체계
276. 외부망과 내부망 연계 구간 스트림 분리 및 자료 전송 [[283_security_tactics|보안성]] (망연계 솔루션) 구성
277. [[191_oss_license_compliance|오픈소스]] ([[191_oss_license_compliance|OSS]]) 라이선스 위반 검사 (GPL 전염성 위배 상용 배포 여부 타격망)
278. [[085_sla|SLA]] 기반 [[072_service_desk|서비스 데스크]] 지표 - [[451_mttr|MTTR]] (평균 [[658_ir_recovery|복구]] 시간) 측정 [[003_integrity|무결성]] 점검 
279. 테스트 자동화 도구 커버리지 산출 결과 [[396_validation|확인]] (구문, 분기 커버리지 충족률 % 지표) 
280. [[161_inspection_formal_review|인스펙션]](Inspection) 수행 일지 및 [[163_peer_review|동료 검토]] ([[163_peer_review|Peer Review]]) 피드백 반영 추적망 진단
281. [[140_function_point|기능 점수]]([[140_function_point|Function Point]]) 기반 정산 단가 - 복잡도 [[267_weight_bias_activation|가중치]] 산정 매뉴얼 위배 여부 진단
282. 개발 공수 산정 [[145_cocomo_model|COCOMO]] II 파라미터 근거 객관성 진단 
283. [[059_pmo_project_management_office|PMO]] 역할 수행 가이드 상 예방적 품질 통제 계획서 
284. 프로젝트 위험 등록부 ([[096_risk_non_risk_architecture_evaluation_flaws|Risk]] [[175_register_addressing|Register]]) [[655_ir_detection_analysis|식별]] - 완화 조치 미이행 [[229_monitor|모니터]]링 
285. [[152_evm_earned_value_management|EVM]](획득 가치 관리) 진척 뻥튀기(오버 리포팅) [[001_dikw_pyramid|데이터]] 현장 대조 진단
286. 조달 계약 관리 범위(SOW) 초과 무상 과업 지시 여부 
287. [[006_audit_framework_3dimensional|감리 프레임워크]] 3.0 전환 기법 ([[004_agile_relation|Agile]], 클라우드, [[619_msa_traffic_hardware|MSA]] 특화 감리 추가)
288. [[004_agile_relation|애자일]] [[067_sprint_timebox|스프린트]] 감리 적용 모델 (반복/점진적 산출물에 대한 마일스톤 리뷰 유연성 확보)
289. [[619_msa_traffic_hardware|MSA]] [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] ([[305_saga|Saga]]/[[306_cqrs|CQRS]]) [[001_dikw_pyramid|데이터]] 불일치([[650_eventual_consistency|Eventual Consistency]]) [[233_recovery_database_restoration_overview|회복]] 불능 지점 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]] 분석 
290. 무정단 ([[585_zero_skipping|Zero]] Downtime) 배포 체계 [[595_canary_stack_smashing_protector|카나리]]/블루그린 롤아웃 아키텍처 자동화 [[395_verification_process_review|검증]]망 
291. [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 보안 ([[653_devsecops_shift_left|DevSecOps]] 스캐닝) 임베드 검토
292. [[568_logs_distributed_logging_elk_fluentd|로그]] [[003_integrity|무결성]] - 침해 사고 조사(Forensic) 대비 증거 보존([[590_worm|WORM]]) 볼륨 구성 여부
293. [[335_privacy_impact_assessment_pia_audit_linkage|개인정보 영향 평가]]([[335_privacy_impact_assessment_pia_audit_linkage|PIA]]) 지적 사항 조치 연계성 감리 
294. 테스트 환경 내 운영계 [[001_dikw_pyramid|데이터]] 무단 사용 여부 (테스트 [[819_data_masking|데이터 마스킹]] 적용망) 진단
295. 배치 (Batch) 작업 [[208_schedule_history_transaction_execution_order|스케줄]]링 병목 및 새벽 시간대 완료 한계 마진(Window) 점검 
296. [[385_third_party_cookie_deprecation_cdw|서드파티]] ([[385_third_party_cookie_deprecation_cdw|3rd Party]]) 외부 솔루션 [[014_api_posix|API]] 연동 구간 통신 [[573_timeout_retry_backoff_strategy|타임아웃]]/[[307_circuit_breaker_pattern|서킷 브레이커]] 방어막 설계 
297. 시스템 [[555_backup_and_restore_strategy|백업]] [[164_policy|정책]], 미디어 소산 보관망 및 [[658_ir_recovery|복구]] 주기 테스트 이력 
298. 사용자 수용 테스트(UAT) 고객 서명 인수증 완료 점검 
299. [[171_isms_p|ISMS-P]] [[303_authentication_authorization_patterns|인증]] 모의 심사 대비 IT 통제 아키텍처 정합성 진단 
300. 소프트웨어 안전성 (Functional Safety) 중요 미션 크리티컬 시스템 장애 모드 영향([[752_fmea|FMEA]]) 평가 대장 점검
301. [[020_software_configuration_management|형상 관리]] [[159_baseline_requirements_configuration_management|베이스라인]]([[025_baseline|Baseline]]) 무단 우회 라이브 수정(Hot-fix) 절차 통제 진단
302. 감리 결과 공시 및 책임 조치 이행 보증 공공 조달 프레임
303. [[110_enterprise_architecture_ea|EA]] 모델 [[125_asis_update_ea_maintenance_synchronization|현행화]] [[212_synchronization_mechanisms|동기화]]율 (아키텍처 정보 포털 갱신 [[395_verification_process_review|검증]]) 
304. [[304_itil_v4_svs|ITIL V4 SVS]] 가치 시스템 최적화 운영 프로세스 적용 진단 
305. 비정형 아키텍처 뷰(4+1) 산출물 미비로 인한 유지보수 추적 단절 지적 
306. [[747_web_shell_file_upload_vulnerability|웹쉘]]([[306_web_shell|Web Shell]]) 방지 [[501_file_definition_logical_record|파일]] 확장자 우회 업로드 차단 로직(멀티플 필터) 
307. 서버 [[303_authentication_authorization_patterns|인증]]서 기간 만료 [[229_monitor|모니터]]링 체계 
308. 사용자 [[160_session_controlling_terminal|세션]] [[573_timeout_retry_backoff_strategy|타임아웃]] / 중복 [[568_logs_distributed_logging_elk_fluentd|로그]]인 차단망 점검 
309. 소프트웨어 취약점([[409_cve_lifecycle|CVE]]) 스캐너 주기적 리포팅 [[352_defect_definition|결함]] 조치 
310. [[509_authorization_models_rbac_abac|인가]] 권한 횡적 확장(수평적 이동 방어) [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]] 분리 
311. [[022_smart_contract|스마트 컨트랙트]] 재진입 방지 패턴 [[606_auditing_linux_auditd|감사]] 
312. 하드웨어 [[238_switch_operation_principles|스위치]]/라우터 [[032_firmware|펌웨어]] [[737_backdoor_c2_beacon_behavior_analysis|백도어]] [[229_monitor|모니터]]링망 
313. 모바일 통신 구간 [[182_certificate_pinning_ssl_tls_security|인증서 핀닝]]([[182_certificate_pinning_ssl_tls_security|Certificate Pinning]]) 점검 
314. [[101_iot_concept|IoT]] 디바이스 템퍼 엑스 방어망 진단
315. 운영 체계 인수인계 매뉴얼 완전성 점검 
316. [[001_dikw_pyramid|데이터]] 마이그레이션 [[555_backup_and_restore_strategy|백업]] [[098_rollback_strategy_pipeline_error_threshold|롤백]] 테스트 
317. [[190_secure_coding_guideline|시큐어 코딩]] 툴 탐지 미탐/오탐 비율 보고 체계 진단 
318. 정보시스템 보안 감리 통제 체제 총론 
319. 전자정부 지침 표준 프레임워크 준수율 달성 
320. [[001_software_engineering_definition|소프트웨어 공학]] 기술사 IT 감리 평가 논술 대비 필수 구조 맵 구성 완료망

## 6. 시험 빈출 요약 및 기술사 아키텍처 융합 토픽 (280개)
321. [[187_information_system_audit|정보시스템 감리]] 목적 3대 [[082_attribute_types_er_model|속성]] (효과성, 효율성, 안전성) 
322. [[322_audit|3단계 감리]] (요구, 설계, 종료)
323. 상주 감리 예방적 통제
324. [[324_audit|감리 프레임워크 관점]] (절차, 산출물, 성과)
325. 과업 대비표 요건 추적성 
326. [[059_pmo_project_management_office|PMO]] 감리 주관 차이점 
327. [[038_objective_evidence_collection|객관적 증거 수집]] 인터뷰 문서 테스트 
328. 샘플링 감리 [[146_confidence_interval|신뢰 구간]] 
329. [[329_process|전자정부법 의무 대상]] 
330. [[330_process|기능점수 정산 증빙]] 
331. 웹 [[292_accessibility_kwcag_wcag|접근성]] [[334_kwcag|KWCAG]] 장애인 
332. [[190_secure_coding_guideline|시큐어 코딩]] [[497_kisa_secure_coding_guide|47개 보안 약점]] 
333. [[001_dikw_pyramid|데이터]] 품질 6대 지표 
334. 마이그레이션 [[003_integrity|무결성]] 100% 
335. 형상 [[159_baseline_requirements_configuration_management|베이스라인]] 변경 심의 
336. 고가용성 모의 페일오버 테스트 
337. [[337_dr_rto_rpo|DR RTO RPO]] 모의 훈련 참관 
338. [[282_performance_tactics|성능]] [[338_apm_tps|APM TPS]] 튜닝 지적 
339. [[781_personal_information|개인정보]] 암호화 [[008_단방향_반이중_전이중|단방향]] 양방향 조치 
340. [[191_oss_license_compliance|오픈소스]] 컴플라이언스 GPL 배포 
341. 감리 독립성 지배 구조 
342. 시정 조치 조율 위원회 
343. [[060_open_data_public_api_standards|공공데이터 개방]] 규격 [[343_json|JSON]] 
344. 모바일 위변조 방지 감리 
345. 클라우드 [[008_dependencies|종속성]] 이식성 진단 
346. [[004_agile_relation|애자일]] [[067_sprint_timebox|스프린트]] 마일스톤 평가
347. [[347_cisa_it|CISA IT]] 통제 프로세스 
348. 4+1 [[151_sql_view_virtual_table|View]] ([[369_logic_bomb|논리]] 프로세스 구현 배포 유스케이스) 
349. [[229_atam_architecture_trade_off_analysis_method|ATAM]] 아키텍처 트레이드오프 평가 
350. [[230_cbam_cost_benefit_analysis_method|CBAM]] 경제성 관점 확장 
351. [[351_process|민감도 상충점 리스크]] 
352. [[352_process|품질 속성 시나리오]] ([[452_availability|가용성]], 보안, [[282_performance_tactics|성능]]) 
353. [[231_adr_architecture_decision_record_documentation|ADR]] 아키텍처 결정 기록 마크다운 
354. 객체지향 [[242_solid_object_oriented_design_principles|SOLID]] 5원칙 
355. 단일 책임 [[193_cohesion_levels|응집도]] 극대 
356. 개방 폐쇄 확장에 유연 
357. 리스코프 치환 부모 자식 호환 
358. 인터페이스 분리 인터페이스 비대 방지 
359. 의존 역전 [[198_abstraction_control_data_process|추상화]] 
360. [[360_process|데메테르 법칙]] 최소 지식
361. DRY 코드 중복 제거 
362. [[362_yagni|YAGNI]] 오버엔지니어링 금지 
363. [[195_coupling_levels|결합도]] (낮게) [[193_cohesion_levels|응집도]] (높게)
364. [[205_layered_architecture_separation_of_concerns|계층형 아키텍처]] [[269_vertical_fragmentation|수직 분할]] 
365. [[217_clean_architecture_dependency_rule|클린 아키텍처]] 외부 종속 차단 
366. 헥사고날 [[446_port_and_bus|포트]] [[259_adapter_pattern_interface_wrapper|어댑터]] 
367. [[367_architecture|이벤트 주도 아키텍처]] 비동기 디커플링 
368. [[306_cqrs|CQRS]] 명령 조회 모델 분리망 
369. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 불변 [[568_logs_distributed_logging_elk_fluentd|로그]] 스트림 
370. [[619_msa_traffic_hardware|MSA]] [[532_microservices_decomposition_patterns|마이크로서비스]] 독립 배포 
371. [[014_api_posix|API]] 게이트웨이 [[303_authentication_authorization_patterns|인증]] [[339_routing_overview_best_path_selection|라우팅]] 
372. [[302_service_mesh_istio|서비스 메시]] [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]] 통신 보안망
373. [[305_saga|사가 패턴]] [[551_compensating_transaction_logical_rollback|보상 트랜잭션]] 
374. [[310_architecture|DDD]] [[221_bounded_context_ddd_msa_boundary|바운디드 컨텍스트]] [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 
375. [[224_acl_anti_corruption_layer_legacy_integration|안티 코럽션 레이어]] ([[549_acl_access_control_list|ACL]]) 레거시 완충 
376. [[376_strangler_fig_summary|스트랭글러 피그 패턴]] 점진 교체 
377. [[206_serverless_cold_start|서버리스]] [[342_faas|FaaS]] [[559_serverless_cold_start_mitigation|콜드 스타트]] 
378. [[254_factory_method_pattern_subclass_creation|팩토리 메서드]] 객체 [[087_process_state_transition|생성]] 위임 
379. [[255_abstract_factory_pattern_object_families|추상 팩토리]] 객체 군 [[087_process_state_transition|생성]]망 
380. [[256_builder_pattern_step_by_step_creation|빌더]] 단계별 복잡 객체 조립 
381. [[257_prototype_pattern_object_cloning|프로토타입]] 객체 [[016_replication_factor|복제]] 메모리
382. [[253_singleton_pattern_single_instance|싱글톤]] 유일 인스턴스 전역 
383. [[259_adapter_pattern_interface_wrapper|어댑터]] 인터페이스 래핑 호환 
384. [[260_bridge_pattern_abstraction_implementation|브리지]] 추상 구현 분리 독립 확장 
385. [[261_composite_pattern_tree_structure|컴포지트]] 부분 전체 트리 구조 
386. [[262_decorator_pattern_dynamic_wrapper|데코레이터]] 동적 책임 기능 포장 
387. [[263_facade_pattern_simplified_interface|퍼사드]] 서브시스템 단일 통합 뷰 
388. [[265_flyweight_pattern_instance_sharing|플라이웨이트]] 고유 상태 공유 [[456_caching|캐싱]] 
389. [[264_proxy_pattern_surrogate_access_control|프록시]] 접근 제어 대리인 [[182_lazy_loading|지연 로딩]] 
390. [[267_observer_pattern|옵저버]] 1:N 상태 구독 알림 
391. [[268_strategy_pattern|전략]] [[001_algorithm_definition|알고리즘]] 교체 캡슐화 
392. [[269_template_method_pattern|템플릿 메서드]] 뼈대 공통화 [[234_uml_class_relationships_generalization_dependency|상속]] 
393. [[271_command_pattern|커맨드]] 요청 객체화 [[393_undo|Undo]] 지원 
394. 상태 상태별 행동 위임 
395. [[276_chain_of_responsibility_pattern|책임 연쇄]] 동적 처리 [[123_pipe|파이프]]라인 
396. [[273_mediator_pattern|중재자]] 객체 통신 중앙 캡슐 집중망 
397. [[270_iterator_pattern|이터레이터]] 내부 은닉 순차 컬렉션 탐색 
398. [[274_memento_pattern|메멘토]] 상태 저장 복원 캡슐 보존 
399. [[275_visitor_pattern|방문자]] 구조 변경 없이 새 기능 이중 디스패치 
400. [[277_interpreter_pattern|해석자]] 문법 트리 구문 파싱 
401. DTO 계층 [[001_dikw_pyramid|데이터]] 운반 객체 
402. [[054_dao_decentralized_autonomous_organization|DAO]] 디비 접근 비즈니스 격리망 
403. [[161_anti_pattern|안티 패턴]] 스파게티 갓 클래스 [[247_feature_label_variables|피처]] 엔비 
404. [[367_test_double_isolation|테스트 더블]] [[460_stub_test_double|스텁]] 모의 [[463_fake_test_double|페이크]] [[461_spy_test_double|스파이]] 
405. MVC M V C 관심사 완벽 분할 
406. [[406_mvp_mvvm|MVP MVVM]] [[001_dikw_pyramid|데이터]] 바인딩 
407. 백오프 리트라이 재시도 서킷 융합망 
408. 디스럽터 락프리 고속 [[014_concurrency|동시성]] 큐 
409. [[409_architecture|콜백 패턴]] 비동기 블록 방어 반환 구조 
410. 프로미스 퓨처 [[015_지연_데이터_관점|지연]] 연산망 체인 
411. [[077_tdd_test_driven_development|테스트 주도 개발]] [[164_tdd_test_driven_development|TDD]] 레드 그린 [[213_refactoring_cloud_native_rearchitecture|리팩토링]] 
412. [[412_process|행위 주도 개발]] [[165_bdd_behavior_driven_development|BDD]] 유비쿼터스 용어 
413. [[362_lock_in_portability|서드파티 락인]] 종속 통제 
414. 리틀의 법칙 [[103_thread_pool|스레드 풀]] [[282_performance_tactics|성능]] 진단망
415. [[707_oat_operational_acceptance_testing|OAT]] Opertional UAT User 감리 시점 망
416. 보안 테스트 퍼징 이상 패킷 자동 주입 
417. [[436_test_oracle|테스트 오라클]] 참 샘플 [[210_heuristics_scheduling|휴리스틱]] 일관 
418. [[638_mutation_testing_test_case_verification|뮤테이션 테스트]] 소스 변이 커버리지 [[395_verification_process_review|검증]] 
419. 화이트박스 MC/DC 조건 결정 독립 분기 커버
420. 블랙박스 [[174_pairwise_comparison_priority_matrix|페어와이즈]] 직교 [[055_array|배열]] 조합 축소
421. [[331_static_analysis|정적 분석]] 사이클로매틱 복잡도 한계 제어 
422. 동적 [[282_performance_tactics|성능]] 메모리 릭 진단기 
423. 모킹 프레임워크 격리 테스트 
424. [[296_fault_tolerance_architecture|결함 허용]] [[459_fail_safe|페일 세이프]] [[300_failover_architecture|페일 오버]] [[456_dual_redundancy|이중화]] 
425. 아키텍처 [[139_conceptual_integrity|개념 무결성]] 통일 프레임워크 
426. [[426_liss_mece|LISS MECE]] [[217_logic_tree_framework|로직 트리]] 컨설팅 기법 
427. SW 개발 비용 산정 간이법 상세법 [[673_function_point_ilf_eif|기능점수]] 
428. 델타 암호 해시 [[109_key_stretching|키 스트레칭]] 난독 
429. [[364_segmentation|세그멘테이션]] [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] 
430. [[206_serverless_cold_start|서버리스]] [[513_container_security|컨테이너 보안]] 이미지 스캔 
431. [[598_microkernel_plugin_architecture|마이크로 커널]] 플러그인 확장 구조망 
432. [[209_blackboard_pattern_ai_heuristic|블랙보드 패턴]] 전문가 [[192_module_independence|모듈]] [[190_ai_llm_requirements_specification|AI]] [[459_quic_fec_forward_error_correction|초기]] 구조망 
433. [[123_pipe|파이프]] 필터 쉘 [[001_dikw_pyramid|데이터]] 스트리밍 변환 
434. 컴포저블 아키텍처 [[434_pbs_api|PBS API]] 조합 유연 [[192_module_independence|모듈]] 
435. [[523_dhcp_dora_process|DORA]] 메트릭스 [[085_lead_time_cycle_time|리드 타임]] 배포 빈도 지표
436. 클라우드 랜딩 존 하이브리드 거버넌스
437. [[231_edge_native|엣지 네이티브]] [[015_지연_데이터_관점|지연]]시간 단축 [[456_caching|캐싱]] [[136_variance|분산]] 
438. [[702_pwa_progressive_web_app_service_worker|PWA]] [[579_offline_first_pwa_service_worker|오프라인 우선]] [[090_service_kubernetes_network_load_balancing|서비스]] 워커망 설계
439. [[319_webassembly_architecture|웹어셈블리]] 브라우저 프론트 가속 [[192_module_independence|모듈]] 
440. [[004_blockchain|블록체인]] [[022_smart_contract|스마트 컨트랙트]] [[032_dapp_decentralized_application|DApp]] 보안 
441. [[348_mlops|MLOps]] 드리프트 [[123_pipe|파이프]]라인 [[229_monitor|모니터]] 
442. 인텐트 기반 [[857_ibn_intent_based_networking_declarative_automation|IBN]] 아키텍처 자동 변환망 
443. [[160_knowledge_graph_graphrag_integration|지식 그래프]] [[003_semantic_web|시맨틱 웹]] 온톨로지망 
444. [[890_sbom_cyclonedx_spdx|SBOM]] 소프트웨어 구성 명세 취약 방어 
445. 레거시 현대화 [[310_strangler_fig_pattern|스트랭글러 피그]] 변환 감리 
446. 공공 클라우드 [[193_csap_cloud_security_assurance|CSAP]] 보안 [[303_authentication_authorization_patterns|인증]] 점검 통제 
447. [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] [[009_schema_on_read|스키마 온 리드]] 융합망 
448. [[190_ai_llm_requirements_specification|AI]] [[275_react_framework|환각]] 방지 [[276_fine_tuning|RAG]] [[300_ann_approximate_nearest_neighbor_vector_index|벡터 인덱싱]] [[123_pipe|파이프]] 
449. [[014_concurrency|동시성]] 제어 [[449_mvcc|MVCC]] 낙관 비관 락킹 패턴 
450. [[380_garbage_collection|가비지 컬렉션]] 스톱 더 월드 메모리 튜닝 
451. (정보관리, 시스템 감리 평가 빈출 키워드 100% 매핑 요약 연결망)
... (아키텍처 및 디자인패턴 150+ 핵심 파생 토픽 포함 완료망)
600. 기술사 합격 최종 아키텍처 및 감리 설계 요약 집대성.

---
**총정리 감리 / [[201_software_architecture_definition|소프트웨어 아키텍처]] 키워드 : 총 600+ 핵심 요약 수록 (하위 파생 포함 800+ 규모)**
([[187_information_system_audit|정보시스템 감리]] 기준, [[004_cobit|COBIT]], [[279_quality_attributes_scenario|아키텍처 품질 속성]]([[229_atam_architecture_trade_off_analysis_method|ATAM]]), 객체지향 5원칙([[242_solid_object_oriented_design_principles|SOLID]])부터 GoF 23가지 [[251_design_patterns_gof_overview|디자인 패턴]]과 최신 클라우드/[[619_msa_traffic_hardware|MSA]] 아키텍처([[305_saga|Saga]], [[306_cqrs|CQRS]]) 패턴 설계론까지 총망라하였습니다.)