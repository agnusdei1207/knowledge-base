---
title: 15. 데브옵스 (DevOps) 및 SRE 키워드 목록
date: '2026-03-04'
tags:
- studynote-devops-sre
---
[[267_weight_bias_activation|weight]] = 9999

# [[652_devops_calms_culture|데브옵스]] ([[652_devops_calms_culture|DevOps]]) 및 [[100_sre_site_reliability_engineering_error_budget|SRE]] (사이트 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 공학) 키워드 목록 (심화 확장판)

정보관리기술사, 컴퓨터응용시스템기술사 및 클라우드/플랫폼 엔지니어를 위한 [[652_devops_calms_culture|데브옵스]], [[100_sre_site_reliability_engineering_error_budget|SRE]], [[090_configuration_item|CI]]/CD, [[119_gitops_single_source_of_truth|GitOps]], [[513_container_security|컨테이너 보안]]([[653_devsecops_shift_left|DevSecOps]]) 및 [[642_observability_telemetry|옵저버빌리티]]([[642_observability_telemetry|Observability]]) 전 영역 800대 핵심 키워드입니다.

---

## 1. [[652_devops_calms_culture|DevOps]] 문화 및 개발 방법론 (60개)
1. [[652_devops_calms_culture|데브옵스]] ([[652_devops_calms_culture|DevOps]]) 사상 - 개발(Dev)과 운영(Ops) 간의 소통, 협업, 통합을 강조하여 소프트웨어 배포 속도와 안정성을 극대화하는 문화적/기술적 패러다임
2. [[002_silo_hyeonhyung|사일로]] ([[002_silo_hyeonhyung|Silo]]) 현상 타파 - 부서 간 장벽을 허물고 공동의 목표(빠른 배포와 시스템 안정성) 달성
3. [[281_calms|CALMS]] 프레임워크 - [[652_devops_calms_culture|DevOps]] 5대 핵심 가치 (Culture 문화, Automation 자동화, [[087_lean_software_development_7_principles|Lean]] 린 IT, Measurement 측정, Sharing 공유)
4. [[004_agile_relation|애자일]] ([[004_agile_relation|Agile]])과의 [[083_relationship_in_er_model|관계]] - [[004_agile_relation|애자일]]이 개발(기획~코딩)의 속도를 높인다면, DevOps는 [[004_agile_relation|애자일]]의 속도를 운영(배포~[[229_monitor|모니터]]링)까지 확장한 체계
5. [[005_feedback_loop|피드백 루프]] ([[005_feedback_loop|Feedback Loop]]) - 운영 환경의 이슈와 사용자 반응을 즉각적으로 개발 계획에 반영하는 순환 구조
6. [[006_twelve_factor|12 팩터 앱]] ([[006_twelve_factor|The Twelve-Factor App]]) - [[531_cloud_native_architecture|클라우드 네이티브]]([[309_saas|SaaS]]) 애플리케이션 개발을 위한 12가지 베스트 프랙티스 (Heroku 제안)
7. [[007_codebase|코드베이스]] ([[007_codebase|Codebase]]) - [[288_version_ihl_tos_total_length|버전]] 관리되는 하나의 [[007_codebase|코드베이스]]와 다양한 배포(Dev, Staging, Prod) 연계
8. [[008_dependencies|종속성]] ([[008_dependencies|Dependencies]]) 격리 - 모든 [[008_dependencies|종속성]]은 명시적으로 선언(package.[[343_json|json]], pom.xml 등)
9. [[009_config|설정]] ([[009_config|Config]]) - [[156_environment_variables|환경 변수]](Env Vars)에 [[009_config|설정]]을 저장하여 코드와 분리
[[489_raid_10_hybrid|10]]. [[010_backend_services|백엔드 서비스]] ([[010_backend_services|Backing Services]]) - DB, 큐, 캐시 등을 네트워크로 연결된 자원(Attached Resource)으로 취급
[[308_static_dynamic_nat_pat_port_address_translation|11]]. 빌드, 릴리스, 실행 (Build, Release, Run) 단계의 엄격한 분리
12. [[012_stateless_processes|무상태 프로세스]] ([[012_stateless_processes|Stateless Processes]]) - 애플리케이션은 상태를 공유하지 않고 무상태로 실행되며, 상태는 DB 등에 저장
13. [[013_port_binding|포트 바인딩]] ([[013_port_binding|Port Binding]]) - 자체적으로 [[446_port_and_bus|포트]]를 바인딩하여 웹 [[090_service_kubernetes_network_load_balancing|서비스]] 노출
14. [[014_concurrency|동시성]] ([[266_other_transparency|Concurrency]]) - 프로세스 모델을 통한 [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]]([[202_scale_out_distributed_horizontal_expansion|Scale-out]]) 수평 확장
15. [[015_disposability|폐기 가능성]] ([[015_disposability|Disposability]]) - 빠른 시작과 우아한 종료(Graceful Shutdown)를 통한 안정성 극대화
16. 개발/운영 환경 일치 (Dev/Prod Parity) - 개발, 스테이징, 운영 환경의 갭을 최소화
17. [[568_logs_distributed_logging_elk_fluentd|로그]] ([[568_logs_distributed_logging_elk_fluentd|Logs]]) - [[568_logs_distributed_logging_elk_fluentd|로그]]를 이벤트 스트림으로 취급하여 표준 출력(stdout)으로 뿜어냄
18. [[018_admin_processes|관리 프로세스]] ([[018_admin_processes|Admin Processes]]) - 일회성 관리/스크립트 작업도 동일한 환경에서 실행
19. [[076_ci_continuous_integration|지속적 통합]] ([[090_configuration_item|CI]], [[019_continuous_integration|Continuous Integration]]) - 다수 개발자의 코드를 메인 브랜치에 수시로 병합하고 자동 빌드/테스트를 수행해 통합 오류를 조기 발견
20. [[020_continuous_delivery|지속적 전달]] (CD, [[164_continuous_delivery|Continuous Delivery]]) - CI를 통과한 코드를 프로덕션(운영) 환경에 배포할 준비([[075_artifact_management_nexus_docker_registry|아티팩트]] [[087_process_state_transition|생성]])를 완료하되, 실제 배포는 인간의 수동 승인을 거침
21. [[099_continuous_deployment_cd|지속적 배포]] (CD, [[165_continuous_deployment|Continuous Deployment]]) - 수동 승인조차 생략하고 테스트를 통과한 모든 코드를 프로덕션 환경까지 완전 자동으로 릴리스
22. [[523_dhcp_dora_process|DORA]] [[342_routing_metric_hop_bandwidth_delay|메트릭]]스 ([[201_dora_metrics_devops_performance|DORA Metrics]]) - 구글 클라우드가 정의한 소프트웨어 개발/운영 성과 측정 4대 지표
23. 배포 빈도 ([[087_deployment_kubernetes_workload_rolling_update|Deployment]] Frequency) - 프로덕션에 얼마나 자주 배포하는가
24. 변경 [[085_lead_time_cycle_time|리드 타임]] ([[024_lead_time_for_changes|Lead Time for Changes]]) - 코드가 커밋된 후 프로덕션에 배포되기까지 걸리는 시간
25. 변경 실패율 ([[025_change_failure_rate_cfr|Change Failure Rate]]) - 배포 후 장애/버그로 인해 핫픽스나 [[098_rollback_strategy_pipeline_error_threshold|롤백]]이 필요한 비율
26. [[090_service_kubernetes_network_load_balancing|서비스]] [[658_ir_recovery|복구]] 시간 (Time to Restore [[090_service_kubernetes_network_load_balancing|Service]] / [[451_mttr|MTTR]]) - 장애 발생 시 [[658_ir_recovery|복구]]에 걸리는 시간
27. SPACE 프레임워크 - 개발자 생산성을 단순 코드량(LOC)이 아닌 만족도, 성과, 활동, 커뮤니케이션, 효율성 5가지 차원으로 다각화 측정
28. [[109_platform_engineering_cognitive_load|플랫폼 엔지니어링]] ([[109_platform_engineering_cognitive_load|Platform Engineering]]) - 개발자의 [[686_cognitive_load_team_topologies|인지 부하]]([[686_cognitive_load_team_topologies|Cognitive Load]])를 줄이기 위해 전담 플랫폼 팀이 '내부 개발자 포털([[536_idp_identity_provider|IDP]])'을 구축해 툴체인을 셀프 [[090_service_kubernetes_network_load_balancing|서비스]]로 제공하는 최신 [[652_devops_calms_culture|DevOps]] 트렌드
29. 내부 개발자 포털 ([[536_idp_identity_provider|IDP]], Internal Developer Portal) - Backstage 등, 개발자가 인프라/K8s를 몰라도 클릭 몇 번으로 인프라 [[528_provisioning|프로비저닝]] 및 [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 [[087_process_state_transition|생성]]
30. 골든 패스 (Golden Path / Paved Road) - 조직 내에서 권장되는 가장 안전하고 자동화된 표준 개발/배포 경로 (가이드라인)
31. [[224_vsm_value_stream_mapping|가치 흐름 매핑]] ([[030_value_stream_mapping|VSM]], [[088_value_stream_mapping_vsm|Value Stream Mapping]]) - 아이디어 발의부터 고객에게 가치가 전달되기까지의 전체 흐름에서 대기 시간(병목, Muda)을 [[655_ir_detection_analysis|식별]]하고 린([[087_lean_software_development_7_principles|Lean]])하게 제거하는 도식화 기법
32. [[085_lead_time_cycle_time|리드 타임]] ([[085_lead_time_cycle_time|Lead Time]]) vs 사이클 타임 (Cycle Time)
33. 콘웨이의 법칙 (Conway's Law) - "소프트웨어의 구조는 그 소프트웨어를 만드는 조직의 통신 구조를 닮는다"
34. 역 콘웨이 [[268_strategy_pattern|전략]] (Inverse Conway Maneuver) - 원하는 [[532_microservices_decomposition_patterns|마이크로서비스]]([[619_msa_traffic_hardware|MSA]]) 아키텍처 구조에 맞춰 조직 구조(스쿼드, 크로스펑셔널 팀)를 선제적으로 재편하는 [[268_strategy_pattern|전략]]
35. [[652_devops_calms_culture|데브옵스]] 토폴로지 ([[652_devops_calms_culture|DevOps]] Topologies) - [[161_anti_pattern|안티 패턴]] (Dev 팀과 Ops 팀의 완전 분리) vs 모범 패턴 (협력형, 플랫폼 팀 지원형)
36. 비난 없는 포스트모템 ([[206_postmortem_blameless_devops_culture|Blameless Post-mortem]]) - 장애 발생 시 '누가' 잘못했는지가 아니라 '무엇이' 문제였고 시스템이 어떻게 막지 못했는지 시스템적 관점에서 분석하는 회고 문화
37. [[036_psychological_safety|심리적 안전]]감 ([[036_psychological_safety|Psychological Safety]]) - 조직 내에서 실수나 의견을 자유롭게 말해도 불이익을 받지 않는다고 느끼는 믿음 (고성과 팀의 핵심 요소)
38. [[004_agile_relation|애자일]] [[059_pmo_project_management_office|PMO]] ([[037_agile_pmo|Agile PMO]]) - 통제 중심의 기존 PMO에서 [[004_agile_relation|애자일]] 코칭 및 장애물 제거(Servant Leadership) 지원 조직으로 전환
39. 워터-[[062_scrum_framework_overview|스크럼]]-폴 ([[128_water_scrum_fall_anti_pattern|Water-Scrum-Fall]]) [[161_anti_pattern|안티 패턴]] - 개발만 [[062_scrum_framework_overview|스크럼]]으로 하고, 앞단(기획)과 뒷단(배포)은 기존 폭포수(결재) 모델을 유지해 결국 [[085_lead_time_cycle_time|리드 타임]]이 줄지 않는 현상
40. [[576_feature_flag_ab_testing_rollout|피처 플래그]] ([[576_feature_flag_ab_testing_rollout|Feature Flag]]) / [[247_feature_label_variables|피처]] 토글 (Feature Toggle) - 코드 재배포 없이 런타임에 [[009_config|설정]]([[014_api_posix|API]]/DB)을 바꿔 특정 신기능을 켜거나 끄는 기법. ([[040_trunk_based_development|트렁크 기반 개발]]의 핵심 안전망)
41. [[040_trunk_based_development|트렁크 기반 개발]] ([[040_trunk_based_development|Trunk-Based Development]]) - 수명이 긴 [[247_feature_label_variables|피처]] 브랜치(Feature Branch)를 만들지 않고, 모든 개발자가 하루에도 여러 번 메인 트렁크([[172_maas_mobility_as_a_service|마스]]터) 브랜치에 직접 커밋/병합하여 [[068_git_merge_conflict_resolution_rebase|병합 충돌]](Merge Hell)을 방지
42. A/B 테스팅 (A/B Testing) - 두 가지 UI/기능을 동시에 실제 사용자에게 노출하여 [[001_dikw_pyramid|데이터]](전환율 등) 기반으로 의사결정
43. [[197_dark_launching_traffic_shadow|다크 론칭]] ([[197_dark_launching_traffic_shadow|Dark Launching]]) - 사용자 UI에는 노출하지 않고 백그라운드로만 새 코드를 실행시켜 [[282_performance_tactics|성능]] 부하 및 에러를 프로덕션 트래픽으로 사전 [[395_verification_process_review|검증]]
44. [[164_tdd_test_driven_development|TDD]] ([[411_process|Test-Driven Development]]) / [[165_bdd_behavior_driven_development|BDD]] ([[126_bdd_behavior_driven_development_given_when_then|Behavior-Driven Development]])
45. [[242_shift_left_sdlc|시프트 레프트]] ([[242_shift_left_sdlc|Shift-Left]]) - 소프트웨어 개발 수명 주기([[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]])의 오른쪽 끝에 있던 활동(보안 검사, 테스트)을 왼쪽(개발/빌드 [[459_quic_fec_forward_error_correction|초기]])으로 앞당겨 [[352_defect_definition|결함]]을 조기 발견하고 비용을 절감하는 사상
46. [[207_chatops_slack_bot_deployment|챗옵스]] ([[207_chatops_slack_bot_deployment|ChatOps]]) - 슬랙(Slack), MS Teams 등 메신저 내에서 봇(Bot) [[271_command_pattern|커맨드]]를 입력해 배포, [[229_monitor|모니터]]링 알람 [[396_validation|확인]], 장애 [[658_ir_recovery|복구]] 등을 팀과 공유하며 수행
47. 에러 버짓 ([[101_error_budget_sre|Error Budget]]) - 100% [[452_availability|가용성]]의 비현실성을 인정하고, [[181_slo_service_level_objective|SLO]](예: 99.9%)를 뺀 나머지 0.1%를 '합법적으로 허용된 장애 예산'으로 할당하여 신규 배포의 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]를 관리하는 [[100_sre_site_reliability_engineering_error_budget|SRE]] 철학
48. [[348_mlops|MLOps]] ([[220_mlops_machine_learning_operations|Machine Learning Operations]]) - 모델 개발과 운영의 단절 극복
49. [[324_dataops|DataOps]] ([[001_dikw_pyramid|Data]] Operations) - [[645_data_pipeline_acceleration|데이터 파이프라인]] 자동화 
50. BizDevOps - 비즈니스 요구사항 기획부터 운영까지 일체화
51. [[051_agile_maturity_assessment|애자일 성숙도 평가]] 지표 ([[051_agile_maturity_assessment|Agile Maturity Assessment]])
52. [[100_technical_debt_monitoring_release_policy|기술 부채]] ([[100_technical_debt_monitoring_release_policy|Technical Debt]]) [[229_monitor|모니터]]링 시스템
53. 백로그 정제 (Backlog Grooming/Refinement) 
54. [[069_daily_standup_scrum|데일리 스탠드업]] (Daily Standup) 및 [[084_kanban_board_wip_limit|칸반]] 보드 
55. 워크플로우 오케스트레이터 (Workflow Orchestrator)
56. [[652_devops_calms_culture|DevOps]] 툴체인 (Toolchain) 이기종 연동 [[014_api_posix|API]]
57. [[652_devops_calms_culture|데브옵스]] 에반젤리스트 ([[652_devops_calms_culture|DevOps]] Evangelist) 역할 
58. [[058_dx_developer_experience|개발자 경험]] ([[726_platform_engineering_idp_dx|DX]], Developer Experience) 향상 [[268_strategy_pattern|전략]]
59. 번아웃 (Burnout) 방지를 위한 온콜 (On-[[189_subroutine_call_return|call]]) 교대 근무 최적화
60. [[652_devops_calms_culture|DevOps]] [[012_roi_return_on_investment|ROI]] (투자 수익률) 측정 지표

## 2. [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 및 [[119_gitops_single_source_of_truth|GitOps]] (60개)
61. [[020_software_configuration_management|형상 관리]] ([[089_configuration_management|Configuration Management]]) / [[288_version_ihl_tos_total_length|버전]] 관리 시스템 ([[026_version_control_system|VCS]])
62. 중앙 집중형 [[026_version_control_system|VCS]] (SVN) vs [[136_variance|분산]]형 [[026_version_control_system|VCS]] (Git) - Git은 로컬 저장소에 전체 히스토리를 [[016_replication_factor|복제]]하여 오프라인 작업 및 브랜치 병합 속도 극대화
63. Git 브랜치 [[268_strategy_pattern|전략]] ([[052_git_branching_strategies|Git Branching Strategies]])
64. Git Flow - Master, Develop, Feature, Release, Hotfix 5개 브랜치 사용 (안정적이나 복잡, 릴리스 주기 긴 프로젝트 적합)
65. [[054_github_flow|GitHub Flow]] - Master 브랜치와 Feature 브랜치만 사용, 매우 단순하여 [[099_continuous_deployment_cd|지속적 배포]](CD) 및 [[040_trunk_based_development|트렁크 기반 개발]]에 최적화
66. GitLab Flow - 환경([[066_gitlab_flow_environment_branch_strategy|Environment]]) 기반 배포와 연계된 브랜치 [[268_strategy_pattern|전략]]
67. 풀 리퀘스트 ([[067_pull_request_pr_merge_request_code_review|Pull Request]], [[067_pull_request_pr_merge_request_code_review|PR]]) / 머지 리퀘스트 (Merge Request, MR) - 코드 병합 전 [[163_peer_review|동료 검토]]([[330_code_review|Code Review]])를 요청하는 프로세스
68. [[068_git_merge_conflict_resolution_rebase|병합 충돌]] ([[068_git_merge_conflict_resolution_rebase|Merge Conflict]]) 및 해결 방안 (Rebase vs Merge)
69. 커밋 [[389_mesh_topology|메시]]지 컨벤션 (Commit Message Convention) - feat, fix, docs, [[213_refactoring_cloud_native_rearchitecture|refactor]] 등 접두어 표준화
70. [[070_build_tools_maven_gradle_npm|빌드 도구]] ([[070_build_tools_maven_gradle_npm|Build Tools]]) - Maven, Gradle (Java), npm, [[020_yarn|yarn]] (Node.js)
71. [[071_jenkins_ci_cd_pipeline_automation|젠킨스]] ([[071_jenkins_ci_cd_pipeline_automation|Jenkins]]) - 가장 널리 쓰이는 자바 기반 [[191_oss_license_compliance|오픈소스]] [[090_configuration_item|CI]]/CD 자동화 서버 (플러그인 생태계 막강)
72. 선언적 [[123_pipe|파이프]]라인 ([[219_declarative_yaml|Declarative]] [[082_pipeline|Pipeline]]) - Jenkinsfile에 빌드/테스트/배포 단계를 코드로 정의 ([[072_declarative_pipeline_jenkinsfile_as_code|Pipeline as Code]])
73. 깃허브 액션 (GitHub Actions) - GitHub 내장 [[090_configuration_item|CI]]/CD 런너, `.github/workflows/` [[506_directory_structure_symbol_table|디렉터리]]에 YAML로 정의
74. 깃랩 [[090_configuration_item|CI]] (GitLab [[090_configuration_item|CI]]/CD) - 깃랩 내장 도구, `.gitlab-ci.yml` 활용
75. [[075_artifact_management_nexus_docker_registry|아티팩트]] ([[075_artifact_management_nexus_docker_registry|Artifact]]) - 소스코드가 빌드되어 [[087_process_state_transition|생성]]된 최종 실행 가능한 결과물 (JAR, [[068_docker_image_immutable_package|Docker Image]] 등)
76. [[075_artifact_management_nexus_docker_registry|아티팩트]] 리포지토리 ([[075_artifact_management_nexus_docker_registry|Artifact]] Repository) - Nexus, Sonatype, JFrog, AWS ECR ([[068_docker_image_immutable_package|도커 이미지]] 저장소)
77. [[397_unit_test|단위 테스트]] ([[397_unit_test|Unit Test]]) 자동화 (JUnit, PyTest)
78. [[078_code_coverage|코드 커버리지]] ([[078_code_coverage|Code Coverage]]) 분석 도구 (JaCoCo) - 소스코드의 몇 %가 테스트되었는지 측정 (구문, 분기 커버리지)
79. 소스코드 [[331_static_analysis|정적 분석]] 도구 ([[079_sonarqube|SonarQube]]) - 잠재적 버그, [[370_code_smell|코드 스멜]], 보안 취약점([[491_sast_static_analysis|SAST]]) 자동 스캔 및 품질 게이트(Quality Gate) 통제
80. [[080_sca_software_composition_analysis|패키지 취약점 스캐닝]] ([[453_sca|SCA]], [[495_sca_software_composition_analysis|Software Composition Analysis]]) - 의존하는 [[191_oss_license_compliance|오픈소스]] [[336_library_vs_framework|라이브러리]]의 [[409_cve_lifecycle|CVE]] 취약점 검사
81. [[081_cd_continuous_deployment_pipeline_architecture|지속적 배포 파이프라인]] ([[081_cd_continuous_deployment_pipeline_architecture|CD Pipeline]]) 아키텍처
82. [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]] ([[082_zero_downtime_deployment_rolling_blue_green_canary|Zero Downtime Deployment]]) [[268_strategy_pattern|전략]] 3가지
83. [[193_rolling_update_deployment_kubernetes|롤링 배포]] ([[083_rolling_update_deployment_zero_downtime_version_inconsistency|Rolling Update]]) - 구버전 인스턴스를 하나씩 내리고 신버전을 하나씩 올리는 순차적 교체 (K8s 디폴트). 트래픽 [[139_throughput|처리량]]은 유지되나 배포 도중 구/신버전이 혼재됨
84. 블루/그린 배포 (Blue/Green [[087_deployment_kubernetes_workload_rolling_update|Deployment]]) - 구버전(Blue)과 동일한 규모의 신버전(Green) 환경을 완벽히 띄워놓고, 로드밸런서의 [[339_routing_overview_best_path_selection|라우팅]]을 한 번에 스위칭. [[098_rollback_strategy_pipeline_error_threshold|롤백]]이 1초 만에 가능하나 클라우드 자원 일시적 2배 요구
85. [[115_canary_deployment_gradual_rollout|카나리 배포]] ([[195_canary_release_deployment|Canary Release]]) - 신버전으로 [[339_routing_overview_best_path_selection|라우팅]]되는 트래픽 비율을 1% -> [[489_raid_10_hybrid|10]]% -> 100%로 점진적 확장하며 에러율(5xx) [[342_routing_metric_hop_bandwidth_delay|메트릭]]을 [[229_monitor|모니터]]링, 이상 발생 시 즉시 자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]]
86. [[119_gitops_single_source_of_truth|GitOps]] ([[167_gitops|깃옵스]]) 패러다임 - 인프라 및 애플리케이션의 '목표 상태([[080_kube_controller_manager_desired_state|Desired State]])'를 오직 Git 레포지토리에 선언적(YAML)으로 저장하고, K8s 클러스터 내부의 에이전트가 Git의 변화를 감지해 클러스터 상태와 지속적으로 [[212_synchronization_mechanisms|동기화]](Sync)시키는 현대적 CD 방식
87. [[087_push_based_deployment_jenkins_ci_cd_security_risk|푸시 기반]]([[087_push_based_deployment_jenkins_ci_cd_security_risk|Push-based]]) 배포 - [[071_jenkins_ci_cd_pipeline_automation|젠킨스]](외부)가 [[077_kube_api_server_k8s_hub|kubectl]] 명령을 통해 K8s 클러스터에 직접 푸시 (보안 자격증명 유출 위험)
88. [[088_pull_based_deployment_gitops_argocd_security_auto_healing|풀 기반]]([[088_pull_based_deployment_gitops_argocd_security_auto_healing|Pull-based]]) 배포 - [[119_gitops_single_source_of_truth|GitOps]] 방식. 클러스터 '내부'의 에이전트(ArgoCD)가 외부 Git을 [[448_polling_programmed_io|폴링]](Pull)하여 변경사항을 가져와 적용 (외부망에서 클러스터로의 인바운드 [[690_firewall_generation_evolution|방화벽]] 오픈 불필요, 보안 극대화)
89. ArgoCD (아고씨디) - [[196_kubernetes_k8s_container_orchestration|쿠버네티스]]를 위한 대표적인 [[119_gitops_single_source_of_truth|GitOps]] 선언적 [[099_continuous_deployment_cd|지속적 배포]] 도구
90. FluxCD - ArgoCD의 경쟁 [[119_gitops_single_source_of_truth|GitOps]] 솔루션
91. [[091_kustomize_kubernetes_declarative_overlay_manifest|Kustomize]] ([[091_kustomize_kubernetes_declarative_overlay_manifest|커스터마이즈]]) - [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] YAML 매니페스트를 템플릿 엔진 없이(Native) 오버레이(dev, prod) 방식으로 다형성 있게 관리하는 도구
92. [[207_helm_kubernetes_package_manager_chart|Helm]] ([[207_helm_kubernetes_package_manager_chart|헬름]]) 차트 - K8s 패키지 매니저, values.yaml 변수 주입을 통해 복잡한 K8s 리소스를 한 번에 릴리스
93. [[093_spinnaker_multi_cloud_cd_canary_analysis|스핀네이커]] ([[093_spinnaker_multi_cloud_cd_canary_analysis|Spinnaker]]) - 넷플릭스 개발, [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]](AWS, GCP, K8s) 배포 및 [[595_canary_stack_smashing_protector|카나리]] 분석 자동화(Kayenta) 특화 CD 플랫폼
94. [[094_pipeline_security_lock_in_ci_cd|파이프라인 보안 락인]] ([[094_pipeline_security_lock_in_ci_cd|Pipeline Security]]) 
95. [[095_secret_manager_hashicorp_vault_aws|시크릿 매니저]] ([[095_secret_manager_hashicorp_vault_aws|Secret Manager]]) - DB 패스워드, [[014_api_posix|API]] 키를 Git에 하드코딩하지 않고 분리 저장 (HashiCorp [[567_vault|Vault]], AWS Secrets Manager)
96. K8s Sealed Secrets - [[119_gitops_single_source_of_truth|GitOps]] 환경에서 [[514_secret_management_vault_kms|시크릿]]을 비대칭키로 암호화하여 Git에 안전하게 올리고, 클러스터 내부에서 복호화
97. [[097_deployment_approval_gate_automation|배포 승인 게이트]] ([[097_deployment_approval_gate_automation|Approval Gate]]) 수동/자동화 구성
98. [[098_rollback_strategy_pipeline_error_threshold|롤백]] ([[313_rollback|Rollback]]) [[268_strategy_pattern|전략]] - [[123_pipe|파이프]]라인 에러율 [[431_ssthresh_slow_start_threshold|임계치]] 도달 시 이전 안정 [[288_version_ihl_tos_total_length|버전]](이전 커밋)으로 자동 복원
99. [[271_ddl_liquibase|데이터베이스 마이그레이션]] 도구 자동화 (Flyway, Liquibase) - 앱 코드 배포와 DB [[005_schema|스키마]]([[020_ddl|DDL]]) 변경 스크립트 실행의 싱크 처리
100. [[100_multi_region_deployment_pipeline_disaster_recovery|멀티 리전]] ([[100_multi_region_deployment_pipeline_disaster_recovery|Multi-Region]]) 동시 배포 [[123_pipe|파이프]]라인 설계
101. 엣지 디바이스 (Edge Device) OTA ([[523_iot_firmware_ota_security|Over-The-Air]]) 무선 [[032_firmware|펌웨어]] 배포 [[123_pipe|파이프]]라인
102. [[102_air_gapped_cicd_tarball_delivery|에어 갭]] ([[102_air_gapped_cicd_tarball_delivery|Air-gapped]]) 폐쇄망 환경의 [[090_configuration_item|CI]]/CD 패키징 전달 (Tarball)
103. [[090_configuration_item|CI]]/CD [[342_routing_metric_hop_bandwidth_delay|메트릭]] 대시보드 - 배포 성공률, 빌드 소요 시간 병목 분석
104. 모바일 앱 (iOS/Android) 전용 [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인 (Fastlane)
105. 빌드 [[456_caching|캐싱]] (Build [[456_caching|Caching]]) 최적화 - Maven/[[063_docker_architecture|Docker]] 레이어 캐시 활용 속도 단축
106. [[136_variance|분산]] 빌드 (Distributed Build) 워커 노드 [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]]
107. 크론 ([[107_nightly_build_scheduled_cron_pipeline|Cron]]) 배치 기반 나이트 빌드(Nightly Build) 
108. [[444_test_data_management|테스트 데이터]] [[172_maas_mobility_as_a_service|마스]]킹 자동 주입 [[123_pipe|파이프]]라인
109. [[690_sbom_software_supply_chain_security|소프트웨어 자재 명세서]] ([[890_sbom_cyclonedx_spdx|SBOM]]) 추출 의무화 [[123_pipe|파이프]]라인 임베드
110. 무중단 DB [[005_schema|스키마]] 롤아웃 (Expand and Contract 패턴)
111. [[239_micro_frontends_architecture|마이크로 프론트엔드]] ([[239_micro_frontends_architecture|Micro Frontends]]) [[603_component_independent_deployment_unit|컴포넌트]] 단위 개별 배포망
112. [[206_serverless_cold_start|서버리스]] 프레임워크 ([[206_serverless_cold_start|Serverless]] Framework) [[216_lambda_kappa_architecture_batch_realtime|람다]] 배포 [[198_abstraction_control_data_process|추상화]]
113. SAM ([[113_aws_sam_serverless_model|Serverless Application Model]]) 
114. [[595_canary_stack_smashing_protector|카나리]] 분석 도구 (Kayenta) 통계적 [[040_error_detection|오류 탐지]] 
115. [[195_terraform_hashicorp_agnostic_aws_gcp|테라폼]] 클라우드 / [[195_terraform_hashicorp_agnostic_aws_gcp|테라폼]] 엔터프라이즈 [[090_configuration_item|CI]] 연동 (Atlantis)
116. 인프라 배포 시 드리프트 감지 (Drift [[961_deepfake_detection|Detection]]) 
117. 텍스트옵스 (TextOps) 및 DocOps (문서 배포 자동화)
118. [[090_configuration_item|CI]] [[123_pipe|파이프]]라인 러너 (Runner) 인스턴스의 1회용 (Ephemeral) 격리 실행 
119. 프리커밋 훅 (Pre-commit Hook) 로컬 코드 포맷팅 자동 점검 
120. [[561_container_based_deployment|컨테이너]] 이미지 사이닝 (Image Signing / Cosign, Notary) [[003_integrity|무결성]] [[395_verification_process_review|검증]]망

## 3. 사이트 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 공학 ([[100_sre_site_reliability_engineering_error_budget|SRE]]) 및 [[642_observability_telemetry|옵저버빌리티]] (70개)
121. [[100_sre_site_reliability_engineering_error_budget|SRE]] ([[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]]) - 구글이 제안한 IT 운영 접근법. "SRE는 소프트웨어 엔지니어에게 운영 업무를 맡겼을 때 발생하는 일이다." 
122. [[102_sli_slo_service_level_indicator_objective|SLI]] ([[102_sli_slo_service_level_indicator_objective|Service Level Indicator]]) - [[090_service_kubernetes_network_load_balancing|서비스]] 상태를 보여주는 실제 측정 수치 (예: 지난 1시간 동안의 [[461_http_stateless_connection_oriented|HTTP]] 5xx 에러율 0.05%)
123. [[181_slo_service_level_objective|SLO]] ([[123_slo_service_level_objective|Service Level Objective]]) - 팀 내부적으로 [[009_config|설정]]한 [[090_service_kubernetes_network_load_balancing|서비스]] 지표 목표치 (예: 월간 에러율 0.1% 이하 유지). 비즈니스 목표와 IT 운영의 타협점
124. [[085_sla|SLA]] ([[085_sla|Service Level Agreement]]) - 고객과 맺은 법적/재무적 계약 (SLO보다 느슨하게 [[009_config|설정]]하여 위약금 방어)
125. [[101_error_budget_sre|에러 예산]] ([[101_error_budget_sre|Error Budget]]) - 100% [[452_availability|가용성]]은 불가능하다는 전제하에 허용된 장애 한도. (100% - [[181_slo_service_level_objective|SLO]] 99.9% = 0.1% 예산). 예산 소진 시 신기능 릴리스 동결
126. [[685_toil_automation_sre|토일]] ([[685_toil_automation_sre|Toil]]) - 반복적이고 자동화 가능한 수작업(가치 없는 운영 잡일). SRE는 엔지니어링 시간을 확보하기 위해 [[685_toil_automation_sre|토일]]을 50% 미만으로 [[656_ir_containment|억제]]
127. 온콜 (On-[[189_subroutine_call_return|call]]) 경보 및 교대 근무 프로세스 최적화 (경고 피로 Alert Fatigue 방지)
128. 무비난 포스트모템 ([[206_postmortem_blameless_devops_culture|Blameless Post-mortem]]) - 장애 [[658_ir_recovery|복구]] 후 인적 오류(Human Error)를 탓하지 않고, 시스템 구조적 원인과 예방 프로세스를 문서화하는 장애 회고 문화
129. [[642_observability_telemetry|옵저버빌리티]] ([[642_observability_telemetry|Observability]] / 가시성 / 관측성) - [[532_microservices_decomposition_patterns|마이크로서비스]]([[619_msa_traffic_hardware|MSA]]) 같은 복잡한 [[136_variance|분산]] 시스템 내부에서 문제가 발생했을 때, 외부로 출력되는 텔레메트리(MELT) [[001_dikw_pyramid|데이터]]만 보고도 근본 원인(Root Cause)을 추론할 수 있는 역량
130. [[229_monitor|모니터]]링(이미 아는 문제를 대시보드로 봄) vs [[642_observability_telemetry|옵저버빌리티]](예측 못한 미지의 문제 Unknown-Unknowns 를 탐색/디버깅함)
131. [[184_observability_three_pillars|옵저버빌리티 3대 기둥]] (Three Pillars) - [[342_routing_metric_hop_bandwidth_delay|메트릭]]([[567_metrics_time_series_prometheus_grafana|Metrics]]), [[568_logs_distributed_logging_elk_fluentd|로그]]([[568_logs_distributed_logging_elk_fluentd|Logs]]), [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]](Traces)
132. [[342_routing_metric_hop_bandwidth_delay|메트릭]] ([[567_metrics_time_series_prometheus_grafana|Metrics]]) - 시간에 따른 시스템 자원(CPU, 메모리) 및 [[090_service_kubernetes_network_load_balancing|서비스]] 응답 수치를 [[347_compaction|압축]]한 시계열 [[001_dikw_pyramid|데이터]] (가장 적은 용량, 경고 알람 [[009_config|설정]]용)
133. [[100_sre_site_reliability_engineering_error_budget|SRE]] [[133_four_golden_signals|4대 골든 시그널]] ([[133_four_golden_signals|Four Golden Signals]]) - 트래픽(Traffic, 초당 요청 수), [[141_latency|지연 시간]]([[141_latency|Latency]]), 에러(Errors, 5xx 비율), 포화도(Saturation, 자원 사용률/큐 대기)
134. USE 메서드 (Utilization, Saturation, Errors) - 인프라 자원 분석 방법론
135. RED 메서드 (Rate, Errors, Duration) - 애플리케이션 [[090_service_kubernetes_network_load_balancing|서비스]] 로직 분석 방법론
136. 프로메테우스 ([[136_prometheus|Prometheus]]) - [[531_cloud_native_architecture|클라우드 네이티브]] 환경의 사실상 표준 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 수집 시스템. 에이전트가 밀어주는 방식(Push)이 아니라 서버가 주기적으로 엔드포인트를 당겨오는(Pull) 메커니즘
137. 그라파나 ([[168_grafana|Grafana]]) - 프로메테우스, [[302_cdc|엘라스틱서치]] 등 [[001_dikw_pyramid|데이터]]소스를 연결하여 강력한 [[003_bigdata_7v|시각화]] 대시보드를 제공하는 [[191_oss_license_compliance|오픈소스]] 플랫폼
138. [[568_logs_distributed_logging_elk_fluentd|로그]] ([[568_logs_distributed_logging_elk_fluentd|Logs]]) - 애플리케이션 실행 중 발생하는 특정 이벤트에 대한 상세한 텍스트 기록 (가장 많은 용량 차지, 디버깅의 핵심)
139. [[139_distributed_logging_efk_elk_stack|분산 로깅]] 아키텍처 - Fluentd/Logstash(수집/변환) -> [[179_kafka_flink_watermark_time_window|Kafka]]([[454_buffering|버퍼링]]) -> [[302_cdc|Elasticsearch]](저장/검색) -> [[169_kibana|Kibana]]([[003_bigdata_7v|시각화]]) (EFK / ELK [[057_stack|Stack]])
140. [[568_logs_distributed_logging_elk_fluentd|로그]] 포맷 표준화 - 디버깅 용이성을 위해 [[343_json|JSON]] 형태의 구조화된 [[568_logs_distributed_logging_elk_fluentd|로그]]([[140_structured_logging_json_format|Structured Logging]]) 필수 적용
141. [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] ([[569_distributed_tracing_opentelemetry_jaeger|Distributed Tracing]]) - MSA에서 하나의 사용자 요청이 수많은 [[532_microservices_decomposition_patterns|마이크로서비스]]를 넘나들며 병목이 어디서 발생하는지 구간별로 추적하는 기술
142. 트레이스 (Trace) - 하나의 사용자 요청 전체 흐름
143. 스팬 (Span) - 트레이스 내에서 단일 [[090_service_kubernetes_network_load_balancing|서비스]]가 수행한 작업 구간 (시작/종료 시간 포함). 상위 스팬(부모)과 하위 스팬(자식) 간 계층 구조 형성
144. [[033_context|컨텍스트]] 전파 ([[570_trace_id_span_id_context_propagation|Context Propagation]]) - [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[461_http_stateless_connection_oriented|HTTP]] 호출 시 [[461_http_stateless_connection_oriented|HTTP]] Header에 Trace ID와 부모 Span ID를 주입해 흐름의 연속성을 유지
145. 예거 (Jaeger) / 집킨 (Zipkin) - 대표적인 [[191_oss_license_compliance|오픈소스]] [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] UI/스토리지 백엔드
146. [[190_opentelemetry_cncf_observability_standard|오픈텔레메트리]] ([[146_opentelemetry_otel_observability_standard|OpenTelemetry]], [[146_opentelemetry_otel_observability_standard|OTel]]) - [[190_cncf_landscape_observability|CNCF]] 프로젝트로, 기존 벤더마다 파편화된 [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[568_logs_distributed_logging_elk_fluentd|로그]], 트레이스 수집/계측(Instrumentation) SDK와 표준 명세([[014_api_posix|API]])를 하나로 통합한 관측성 글로벌 표준
147. [[615_ebpf|eBPF]] ([[147_ebpf_kernel_observability_cilium|Extended Berkeley Packet Filter]]) - 리눅스 [[022_kernel_role|커널]] 소스코드를 수정하지 않고도 [[022_kernel_role|커널]] 공간에 샌드박스화된 안전한 코드를 삽입해, 네트워크 트래픽이나 [[294_function_calling_tool_use|함수 호출]] 이벤트를 오버헤드 없이 스니핑/관측하는 혁신적 차세대 기술 ([[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]] 없이도 네트워크 [[642_observability_telemetry|옵저버빌리티]] 구현 가능 - [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] 등)
148. [[751_chaos_engineering|카오스 엔지니어링]] ([[751_chaos_engineering|Chaos Engineering]]) - 시스템이 평상시일 때 고의로 서버 종료, [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]], CPU 폭주 등 '혼돈(장애)'을 주입하여, [[456_dual_redundancy|이중화]]/[[307_circuit_breaker_pattern|서킷 브레이커]] 같은 시스템의 [[233_recovery_database_restoration_overview|회복]] [[571_resiliency_fault_tolerance_patterns|탄력성]]([[571_resiliency_fault_tolerance_patterns|Resiliency]]) 메커니즘이 실제 위기 시 정상 동작하는지 선제적으로 실험하는 엔지니어링 (넷플릭스 [[149_chaos_monkey_chaos_mesh|카오스 몽키]] 기원)
149. [[149_chaos_monkey_chaos_mesh|카오스 몽키]] ([[149_chaos_monkey_chaos_mesh|Chaos Monkey]]) / 카오스 [[389_mesh_topology|메시]] (Chaos [[389_mesh_topology|Mesh]])
150. 장애 영향 반경 (Blast [[541_radius_remote_authentication_aaa|Radius]]) 최소화 - 카오스 실험 시 고객 피해가 없도록 범위를 제한
151. 정상 상태 (Steady [[272_state_pattern|State]]) 가설 수립 및 결과 비교 [[395_verification_process_review|검증]] 
152. [[152_autoscaling_bottleneck_hpa_latency|오토스케일링 병목 현상]] - [[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]] [[507_acid_properties|트리거]] [[015_지연_데이터_관점|지연]]으로 인한 트래픽 유실 방지망 ([[189_custom_metrics|커스텀 메트릭]] 기반 예측 [[249_scaling_normalization_standardization|스케일링]])
153. [[307_circuit_breaker_pattern|서킷 브레이커]] ([[304_circuit_breaker|Circuit Breaker]]) 상태 머신 - Closed (정상), Open (장애 감지 시 빠른 실패 반환), Half-Open (일부 트래픽만 흘려보내 [[658_ir_recovery|복구]] 여부 [[396_validation|확인]])
154. 재시도 (Retry) 폭풍 방지 - 지수적 백오프 (Exponential Backoff, 재시도 간격을 지수 함수로 늘림) 및 지터 (Jitter, 난수를 섞어 동시 재시도 충돌 방지)
155. [[573_timeout_retry_backoff_strategy|타임아웃]] ([[319_timeout_prevention|Timeout]]) [[212_synchronization_mechanisms|동기화]] [[268_strategy_pattern|전략]]
156. [[171_fallback_resilience_pattern|폴백]] ([[129_fallback|Fallback]]) 메커니즘 - 백엔드 장애 시 에러 화면 대신 캐시된 과거 [[001_dikw_pyramid|데이터]] 반환
157. [[157_operational_debt_dark_debt|다크 부채]] ([[157_operational_debt_dark_debt|Dark Debt]]) / 운영 부채 (Operational Debt) 청산 [[268_strategy_pattern|전략]] 
158. [[450_mtbf|MTBF]] (평균 고장 간격) 및 [[451_mttr|MTTR]] (평균 [[658_ir_recovery|복구]] 시간) 최적화 
159. 페일오버 ([[300_failover_architecture|Failover]]) 및 페일백 (Failback) 아키텍처 
160. 능동적 상태 [[396_validation|확인]] (Health Check / [[108_kubernetes_probes_liveness_readiness_startup_health_check|Probes]]) - Liveness, Readiness, Startup
161. [[099_aiops_chatbot_itsm_automation|AIOps]] ([[252_aiops_artificial_intelligence_it_operations_auto_healing|Artificial Intelligence for IT Operations]]) - [[241_machine_learning_basics|머신러닝]]을 활용해 수만 개의 알람 중 연관된 것을 그룹핑(노이즈 감소)하고, 장애 전조를 [[236_anomaly_based_detection_zero_day_false_positive|이상 탐지]]([[111_anomaly_detection|Anomaly Detection]]) 모델로 예측 자동 치유(Auto-remediation)
162. [[162_apm_application_performance_management|APM]] ([[162_apm_application_performance_management|Application Performance Management]]) 인스트루먼테이션 
163. [[163_rum_real_user_monitoring|RUM]] ([[163_rum_real_user_monitoring|Real User Monitoring]]) - 브라우저 기반 실제 사용자 화면 로딩 [[015_지연_데이터_관점|지연]] 추적
164. [[164_synthetic_monitoring_dummy_client|Synthetic Monitoring]] ([[164_synthetic_monitoring_dummy_client|합성 모니터링]]) - [[459_dummy_test_double|더미]] 클라이언트를 띄워 주기적으로 [[568_logs_distributed_logging_elk_fluentd|로그]]인/결제 시나리오를 가상 테스트
165. [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]) 기반 텔레메트리 자동 수집 ([[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 로깅)
166. [[136_variance|분산]] 락 매니저 (Distributed [[510_lock|Lock]]) 병목 관측 
167. [[167_traffic_shadowing_sre_testing|트래픽 섀도잉]] ([[167_traffic_shadowing_sre_testing|Traffic Shadowing]]) 을 이용한 [[100_sre_site_reliability_engineering_error_budget|SRE]] 운영 테스트
168. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 상태 [[658_ir_recovery|복구]] (Replay) [[229_monitor|모니터]]링 
169. 클라우드 비용 [[229_monitor|모니터]]링 ([[344_finops|FinOps]]) 연계 [[100_sre_site_reliability_engineering_error_budget|SRE]] [[164_policy|정책]] (유휴 자원 킬링)
170. 하드웨어 에러 (디스크/메모리 부패) 자가 치유(Self-Healing) [[501_file_definition_logical_record|파일]] 시스템 (ZFS, Btrfs)
171. 용량 계획 (Capacity Planning) 및 [[446_load_test|부하 테스트]] ([[267_load_testing_ci_jmeter_k6|Load Testing]])
172. [[172_cold_start_provisioning_bottleneck|프로비저닝 병목]] ([[347_cold_start_problem|Cold Start]]) 관측 지표
173. 마이크로버스트 (Microburst) 트래픽 - 1초 미만의 찰나에 쏟아져 [[229_monitor|모니터]]링 툴(1분 주기)에 잡히지 않는 [[129_spike_agile_technical_investigation|스파이크]] 트래픽 탐지 기법
174. 런북 (Runbook) / [[637_playbook|플레이북]] ([[637_playbook|Playbook]]) - 장애 발생 시 대응 절차를 체계적으로 정리한 매뉴얼 문서 ([[745_soar_security_orchestration_automation_response|SOAR]] 연동 자동화)
175. 시스템 경계 완충지대 (Buffer/[[058_queue|Queue]]) 텔레메트리 
176. [[136_variance|분산]] DB [[298_qkv_attention|쿼리]] 플랜 [[015_지연_데이터_관점|지연]](Slow Query) 역추적망 
177. [[206_serverless_cold_start|서버리스]]([[342_faas|FaaS]]) 환경의 [[642_observability_telemetry|옵저버빌리티]] 한계 (에이전트 설치 불가) 극복 방안 (AWS X-Ray 등)
178. 그라파나 템플릿([[178_grafana_dashboard_as_code|Grafana Dashboard as Code]]) [[528_provisioning|프로비저닝]]
179. 시계열 DB ([[255_time_series_rollup_retention_compression|InfluxDB]], [[136_prometheus|Prometheus]] TSDB) [[347_compaction|압축]]/[[042_rollup_l2_solution|롤업]] 엔진
180. [[652_devops_calms_culture|DevOps]] 조직 토폴로지와 [[100_sre_site_reliability_engineering_error_budget|SRE]] 팀의 인바운드 대응 비중 (50% 한계) 모델 
181. [[100_sre_site_reliability_engineering_error_budget|SRE]] 임베디드 ([[100_sre_site_reliability_engineering_error_budget|SRE]] Embedded) 운영 모델 
182. [[182_status_page_public_sla|상태 페이지]] ([[182_status_page_public_sla|Status Page]]) 대외 공개 [[085_sla|SLA]] 운영 
183. 고객 [[085_confidence_association_rule_conditional_probability|신뢰도]] 확보를 위한 [[001_dikw_pyramid|데이터]] 손실([[001_dikw_pyramid|Data]] Loss) 제로 아키텍처 
184. [[379_dr_architecture|재해 복구]] ([[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]]) 훈련의 [[751_chaos_engineering|카오스 엔지니어링]] 융합 
185. [[808_network_jitter_delay_variation_storage_sync|네트워크 지터]] ([[185_network_jitter|Network Jitter]]) 및 패킷 손실 관측 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 
186. [[511_dns_hierarchical_distributed_architecture|DNS]] 캐시 중독 및 [[339_routing_overview_best_path_selection|라우팅]] [[365_bgp_border_gateway_protocol_path_vector|BGP]] 하이재킹 [[229_monitor|모니터]]링망 
187. [[157_oom_killer|OOM]] ([[157_oom_killer|Out of Memory]]) 킬러 [[022_kernel_role|커널]] [[568_logs_distributed_logging_elk_fluentd|로그]] 파싱 알람 
188. [[188_perf_iostat_vmstat_tcpdump_sre|리눅스 퍼포먼스 툴]] (perf, iostat, vmstat, tcpdump) [[100_sre_site_reliability_engineering_error_budget|SRE]] 활용 
189. [[189_custom_metrics|커스텀 메트릭]] ([[189_custom_metrics|Custom Metrics]]) 비즈니스 로직(결제 성공률 등) 프로메테우스 연동
190. [[190_cncf_landscape_observability|클라우드 네이티브 생태계]] ([[190_cncf_landscape_observability|CNCF]]) Landscape 진화 방향 ([[642_observability_telemetry|Observability]] 통일화)

## 4. [[207_iac_terraform_immutable_infrastructure|인프라스트럭처 애즈 코드]] ([[793_iac_idempotency_template|IaC]]) 및 [[204_cloud_native_architecture|클라우드 네이티브 아키텍처]] (70개)
191. [[207_iac_terraform_immutable_infrastructure|인프라스트럭처 애즈 코드]] ([[793_iac_idempotency_template|IaC]], [[062_infrastructure_as_code|Infrastructure as Code]]) - 수동 클릭이나 셸 스크립트 대신, 선언적([[219_declarative_yaml|Declarative]]) 코드(YAML, HCL)로 클라우드/인프라 리소스를 [[528_provisioning|프로비저닝]], [[288_version_ihl_tos_total_length|버전]] 관리(Git), 테스트하는 기법
192. [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]] ([[204_immutable_infrastructure_configuration_drift_prevention|Immutable Infrastructure]]) - 서버 구성을 배포 후 런타임에 직접 접속([[538_ssh_vs_telnet_secure_remote|SSH]])해 패치/수정하지 않고, 변경 필요 시 완전히 새 이미지를 빌드해 교체(Replace)하는 패러다임
193. [[193_configuration_drift|구성 편류]] ([[193_configuration_drift|Configuration Drift]]) - 시간이 지나면서 [[793_iac_idempotency_template|IaC]] 코드 스펙과 실제 라이브 인프라의 [[009_config|설정]]이 수동 패치 등으로 인해 불일치하게 되는 장애 유발 원인 (IaC가 이를 방지함)
194. [[171_idempotency_iac_terraform|멱등성]] ([[194_idempotency|Idempotency]]) - [[793_iac_idempotency_template|IaC]] 코드를 한 번 실행하든 천 번 실행하든 최종 결과 인프라 상태는 항상 동일하게 보장되는 특성
195. [[195_terraform_hashicorp_agnostic_aws_gcp|테라폼]] ([[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]) - HashiCorp가 개발한 [[191_oss_license_compliance|오픈소스]] 클라우드 불가지론적(Agnostic, AWS/GCP 모두 지원) 인프라 [[528_provisioning|프로비저닝]] 도구 (HCL 언어 사용)
196. [[196_tfstate_json_s3|테라폼 상태 파일]] ([[196_tfstate_json_s3|tfstate 파일]]) - [[195_terraform_hashicorp_agnostic_aws_gcp|테라폼]]이 현재 실제 인프라 구조를 매핑해 기억해두는 [[012_metadata|메타데이터]] [[343_json|JSON]] [[501_file_definition_logical_record|파일]] (S3 등에 백엔드 잠금 보관 필수)
197. AWS CloudFormation / AWS CDK - AWS 리소스 전용 [[793_iac_idempotency_template|IaC]] 도구
198. [[198_ansible_os_configuration_management_ssh|앤서블]] ([[198_ansible_os_configuration_management_ssh|Ansible]]) - 인프라 '[[087_process_state_transition|생성]]([[528_provisioning|프로비저닝]])'보다는 [[087_process_state_transition|생성]]된 서버 내부의 OS [[009_config|설정]], 패키지 설치를 담당하는 '[[089_configuration_management|구성 관리]]([[089_configuration_management|Configuration Management]])' 자동화 도구. 에이전트 없이 SSH만으로 동작 ([[637_playbook|Playbook]] YAML)
199. [[199_packer_aws_ami_baking|패커]] ([[199_packer_aws_ami_baking|Packer]]) - 동일한 [[009_config|설정]] 스크립트로 [[068_docker_image_immutable_package|도커 이미지]], AWS [[162_ami_advanced_metering_infrastructure|AMI]] 등 다양한 플랫폼의 가상머신 이미지를 일괄 베이킹(Baking)하는 도구
200. [[528_provisioning|프로비저닝]] ([[528_provisioning|Provisioning]]) vs [[089_configuration_management|구성 관리]] ([[089_configuration_management|Configuration Management]]) 
201. [[213_msa_microservices_architecture|마이크로서비스 아키텍처]] ([[619_msa_traffic_hardware|MSA]]) - 모놀리식 단일 덩어리를 비즈니스 [[064_relation_domain|도메인]] 단위로 쪼개어 독립된 DB, 독립 배포 [[123_pipe|파이프]]라인을 갖게 한 구조
202. 컨웨이의 법칙 (Conway's Law) - [[532_microservices_decomposition_patterns|마이크로서비스]] 설계 시 기술이 아닌 비즈니스 팀 조직 구조를 따라야 한다는 원칙
203. [[014_api_posix|API]] 게이트웨이 ([[542_api_gateway|API Gateway]]) - 클라이언트 요청을 받아 [[339_routing_overview_best_path_selection|라우팅]], [[303_authentication_authorization_patterns|인증]], 스로틀링(Throttling)을 단일 진입점에서 통제 (Kong, AWS [[542_api_gateway|API Gateway]])
204. [[543_bff_backend_for_frontend|BFF]] ([[543_bff_backend_for_frontend|Backend For Frontend]]) - 다수 프론트엔드(웹, 모바일)에 맞춰 [[014_api_posix|API]] 게이트웨이를 분리 파편화 제공
205. [[302_service_mesh_istio|서비스 메시]] ([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]) - 애플리케이션 비즈니스 코드와 네트워킹 제어 코드를 분리, 인프라(L7 [[264_proxy_pattern_surrogate_access_control|프록시]]) 단에서 [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신([[339_routing_overview_best_path_selection|라우팅]], [[307_circuit_breaker_pattern|서킷 브레이커]], [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] 암호화)을 전담 ([[302_service_mesh_istio|Istio]], Envoy)
206. [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] ([[546_sidecar_proxy_pattern|Sidecar]]) 패턴 - [[090_service_kubernetes_network_load_balancing|서비스]] [[561_container_based_deployment|컨테이너]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]]) 옆에 [[264_proxy_pattern_surrogate_access_control|프록시]] [[561_container_based_deployment|컨테이너]]를 함께 묶어([[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]처럼) 배포하여 모든 입출력 네트워크 트래픽을 가로채 제어
207. [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] (상호 [[694_thread_local_storage_tls|TLS]]) - [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] 원칙에 따라 내부 [[532_microservices_decomposition_patterns|마이크로서비스]] 간 통신 시에도 발신자/수신자 양방향 [[303_authentication_authorization_patterns|인증]]서 [[395_verification_process_review|검증]] 암호화
208. [[306_cqrs|CQRS]] ([[250_cqrs_command_query_responsibility_segregation_pattern|Command Query Responsibility Segregation]]) - [[282_performance_tactics|성능]] 확장을 위해 상태 변경([[289_cqrs_db|쓰기]]) 모델과 조회(읽기) 모델용 DB 인프라를 [[369_logic_bomb|논리]]적/물리적으로 분리 ([[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]]과 결합)
209. [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] ([[307_event_sourcing|Event Sourcing]]) - RDBMS의 덮어쓰기 로직 대신, 상태가 변경된 모든 '이벤트 이력'을 장부(스트림)에 순차 기록(Append-Only). 언제든 이벤트 리플레이를 통해 [[001_dikw_pyramid|데이터]] [[658_ir_recovery|복구]]/재생 가능
210. [[305_saga|사가 패턴]] ([[305_saga_pattern|Saga Pattern]]) - MSA에서 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] [[549_2pc_two_phase_commit_limitations_msa|2PC]] 락([[510_lock|Lock]]) 병목을 피하기 위해, [[548_local_vs_distributed_transactions|로컬 트랜잭션]]들을 체인처럼 비동기로 연결하고, 실패 시 역순으로 '[[551_compensating_transaction_logical_rollback|보상 트랜잭션]]([[551_compensating_transaction_logical_rollback|Compensating Transaction]])'을 실행하여 [[369_logic_bomb|논리]]적 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 구현 (Choreography vs [[073_container_orchestration_tools|Orchestration]])
211. [[310_strangler_fig_pattern|스트랭글러 피그]] ([[310_strangler_fig_pattern|Strangler Fig]]) 패턴 - 레거시 모놀리식 시스템을 앞단 게이트웨이 [[339_routing_overview_best_path_selection|라우팅]]을 조작해 MSA로 하나씩 갉아먹듯 점진적 교체하는 안전 마이그레이션 기법
212. [[308_pgvector|폴리글랏 퍼시스턴스]] ([[132_polyglot_persistence|Polyglot Persistence]]) - 각 [[532_microservices_decomposition_patterns|마이크로서비스]]의 특성(결제, [[568_logs_distributed_logging_elk_fluentd|로그]], 추천)에 맞춰 RDBMS, [[035_nosql|NoSQL]](키-값, 문서), [[039_graph_db|Graph DB]] 등 다양한 [[002_database_definition|데이터베이스]] 기술을 혼용 아키텍처
213. [[311_database_per_service_pattern|데이터베이스 퍼 서비스]] ([[311_database_per_service_pattern|Database per Service]]) - 다른 [[532_microservices_decomposition_patterns|마이크로서비스]]의 DB에 직접 [[298_qkv_attention|쿼리]](조인) 접근 불가, 오직 API로만 통신 강제 
214. [[367_architecture|이벤트 주도 아키텍처]] ([[064_eda|EDA]], [[140_event_driven_architecture_eda|Event-Driven Architecture]]) - [[090_service_kubernetes_network_load_balancing|서비스]] 간 동기적 [[477_rest_api_architecture|REST API]] 결합을 버리고, [[389_mesh_topology|메시]]지 큐([[179_kafka_flink_watermark_time_window|Kafka]])를 통해 이벤트를 [[017_hardware_interrupt|비동기적]]으로 Pub/Sub 통신하여 극강의 디커플링 보장
215. [[206_serverless_cold_start|서버리스]] ([[206_serverless_cold_start|Serverless]] / [[342_faas|FaaS]]) 아키텍처 - 인프라 [[528_provisioning|프로비저닝]] 없이 '함수 코드'만 클라우드에 올려두면, 특정 이벤트 발생 시 자동으로 [[561_container_based_deployment|컨테이너]]가 확장/실행되고 1밀리초 단위로 과금 (AWS [[216_lambda_kappa_architecture_batch_realtime|Lambda]])
216. [[559_serverless_cold_start_mitigation|콜드 스타트]] ([[347_cold_start_problem|Cold Start]]) - [[206_serverless_cold_start|서버리스]]의 치명적 단점. 장기 휴면 [[294_function_calling_tool_use|함수 호출]] 시 [[561_container_based_deployment|컨테이너]] 이미지를 다운받고 구동하느라 첫 응답 [[015_지연_데이터_관점|지연]] 발생 ([[202_provisioned_concurrency_serverless_cold_start|프로비저닝된 동시성]]으로 예열 해결)
217. [[205_kubernetes_container_orchestration|컨테이너 오케스트레이션]] ([[205_kubernetes_container_orchestration|Kubernetes]]) 아키텍처 
218. [[097_ca_cluster_autoscaler_kubernetes_node_scaling|클러스터 오토스케일러]] ([[089_contract_account_smart_contract|CA]]) / 수평적 [[085_pod_kubernetes_container_unit|파드]] 오토스케일러 ([[095_hpa_horizontal_pod_autoscaler_kubernetes|HPA]]) 연동
219. [[219_declarative_yaml|쿠버네티스 선언적]]([[219_declarative_yaml|Declarative]]) 제어 루프 - 목표 상태(YAML)와 현재 클러스터 상태를 비교하여 일치시키는 무한 [[061_relation_schema_instance|릴레이션]] 메커니즘
220. [[565_operator_pattern_kubernetes_automation|오퍼레이터]] ([[565_operator_pattern_kubernetes_automation|Operator]]) 패턴 - [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] CRD(커스텀 리소스)와 커스텀 컨트롤러 로직을 이용해, DB [[555_backup_and_restore_strategy|백업]]/[[016_replication_factor|복제]] 등 사람이 하던 복잡한 [[064_relation_domain|도메인]] 지식 운영을 K8s 내부 자동화로 편입
221. K8s [[090_service_kubernetes_network_load_balancing|서비스]] 퍼블리싱 (ClusterIP, NodePort, LoadBalancer, [[094_ingress_kubernetes_l7_routing_gateway|Ingress]]) [[339_routing_overview_best_path_selection|라우팅]] 패러다임
222. [[822_cni_container_network_interface_kubernetes|CNI]] ([[100_cni_container_network_interface_flannel_calico|Container Network Interface]]) 플러그인 ([[824_calico_bgp_routing_cni_network_policy|Calico]], [[823_flannel_overlay_cni_vxlan|Flannel]]) [[085_pod_kubernetes_container_unit|파드]] 간 오버레이 통신망
223. [[068_csi|CSI]] ([[099_csi_container_storage_interface_kubernetes_plugin|Container Storage Interface]]) 퍼시스턴트 볼륨([[153_pv_planned_value|PV]]/[[269_pvc_vs_svc_virtual_circuits|PVC]]) 동적 스토리지 할당 
224. [[207_helm_kubernetes_package_manager_chart|헬름]] ([[207_helm_kubernetes_package_manager_chart|Helm]]) 차트 템플릿 엔진 패키지 관리망
225. [[239_micro_frontends_architecture|마이크로 프론트엔드]] ([[239_micro_frontends_architecture|Micro Frontends]]) 아키텍처 - 백엔드 MSA를 프론트 UI 뷰 분할 배포까지 확장 연결
226. [[226_cell_based_architecture|셀 기반 아키텍처]] ([[226_cell_based_architecture|Cell-based Architecture]]) - 장애 반경 격리를 위해 클라우드 리전을 여러 개의 완전 독립된 자급자족 셀(Cell)로 쪼개어 트래픽 [[339_routing_overview_best_path_selection|라우팅]] 
227. [[202_multi_cloud_hybrid_cloud_governance|멀티 클라우드]] ([[202_multi_cloud_hybrid_cloud_governance|Multi-Cloud]]) / [[009_hybrid_cloud|하이브리드 클라우드]] 랜딩 존 (Landing Zone) 설계 네트워크 통제
228. [[631_sddc|SDDC]] ([[858_sddc_software_defined_data_center_infrastructure|소프트웨어 정의 데이터센터]]) [[633_sdn_whitebox|SDN]] 기반 클라우드 [[630_vswitch_vnf_overhead|가상 스위치]] [[817_vxlan_virtual_extensible_lan_mac_in_udp|VXLAN]]
229. [[199_intent_based_networking_ibn_ai_traffic_routing|인텐트 기반 네트워킹]] ([[857_ibn_intent_based_networking_declarative_automation|IBN]]) - 관리자의 비즈니스 '의도'를 선언하면 [[633_sdn_whitebox|SDN]] 컨트롤러가 알아서 네트워크 [[009_config|설정]]/보안 통제 자동 구성 
230. 클라우드 비용 효율 [[344_finops|FinOps]] 프레임워크 최적화 (RI, [[209_spot_instance_cloud_cost_optimization|스팟 인스턴스]], 핫-콜드 [[674_storage_tiering|스토리지 티어링]])
231. [[231_edge_native|엣지 네이티브]] ([[251_edge_native_architecture_distributed_ai_k3s|Edge Native]]) 설계망 [[136_variance|분산]] [[015_지연_데이터_관점|지연]] 단축 
232. [[479_grpc_protobuf_http2|gRPC]] ([[232_grpc_google_rpc_http_2|Google RPC]]) 통신 - [[461_http_stateless_connection_oriented|HTTP]]/2 바이너리 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 버퍼 [[149_serial_communication_rs232_rs485|직렬]]화 기반 [[148_5g_embb_urllc_mmtc|초고속]] [[619_msa_traffic_hardware|MSA]] 동기 통신망
233. [[014_api_posix|API]] First Design 및 Swagger/OpenAPI 명세 기반 컨트랙트 테스팅
234. [[014_multi_tenancy|멀티 테넌시]] ([[014_multi_tenancy|Multi-Tenancy]]) [[309_saas|SaaS]] [[002_database_definition|데이터베이스]] 격리 [[005_schema|스키마]] 아키텍처 ([[369_logic_bomb|논리]] 격리 vs 물리 격리)
235. [[235_registry_immutable_tag|레지스트리]] ([[235_registry_immutable_tag|Registry]]) 태그 불변성 ([[298_immutable|Immutable]] Tag) 운영 이미지 관리망 
236. [[236_vault_dynamic_secrets_ttl|볼트]] ([[567_vault|Vault]]) 기반 동적 [[514_secret_management_vault_kms|시크릿]] (Dynamic Secrets) [[294_ttl_time_to_live_looping_prevention|TTL]] 발급 아키텍처 
237. [[237_opa_open_policy_agent_gatekeeper|OPA]] ([[237_opa_open_policy_agent_gatekeeper|Open Policy Agent]]) / Gatekeeper - 인프라 [[007_security_policy|보안 정책]]을 코드(Rego 언어)로 정의하여 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[085_pod_kubernetes_container_unit|파드]] 배포 시 비인가 [[082_attribute_types_er_model|속성]](루트 권한 등)을 강제 차단하는 규정 준수 자동화
238. 클라우드 마이그레이션 6R (Rehost, Replatform, [[213_refactoring_cloud_native_rearchitecture|Refactor]] 등) 전환 [[268_strategy_pattern|전략]]망
239. [[162_rest_statelessness|무상태성]] ([[239_stateless_redis|Stateless]]) 설계 - 애플리케이션 메모리에 [[160_session_controlling_terminal|세션]]을 남기지 않고 외부 [[542_redis|Redis]] 등에 위임하여 [[202_scale_out_distributed_horizontal_expansion|스케일 아웃]] 확보 
240. [[240_knative_db|서드파티 록인 회피 기술망]] (Knative, [[191_oss_license_compliance|오픈소스]] DB 클러스터링 기반)

## 5. [[653_devsecops_shift_left|DevSecOps]], 사이버 보안, [[090_configuration_item|CI]]/CD 테스트 및 규제 준수 (70개)
241. [[653_devsecops_shift_left|DevSecOps]] 사상 - DevOps의 신속한 배포 [[123_pipe|파이프]]라인([[090_configuration_item|CI]]/CD) 내에 보안([[283_security_tactics|Security]]) [[395_verification_process_review|검증]] 및 차단 프로세스를 자동화 도구로 내재화하여, 배포 속도를 해치지 않으면서 코드 [[352_defect_definition|결함]]을 조기 발견
242. [[242_shift_left_sdlc|시프트 레프트]] ([[242_shift_left_sdlc|Shift-Left]]) - [[131_sdlc_system_development_life_cycle_waterfall_agile|SDLC]] 생명주기 우측(테스트/운영)에 있던 보안 점검을 좌측(기획/개발/빌드)으로 당겨 개발자 책임 하에 조기 예방하여 비용 절감
243. [[243_sast_static_application_security_testing|소스코드 정적 보안 분석]] ([[491_sast_static_analysis|SAST]], [[491_sast_static_analysis|Static Application Security Testing]]) - 코드를 실행하지 않고 구문, [[001_dikw_pyramid|데이터]] 흐름을 분석해 SQL [[480_injection|인젝션]], [[591_buffer_overflow|버퍼 오버플로우]] 등 취약점 룰셋 검사 ([[079_sonarqube|SonarQube]] 등 [[090_configuration_item|CI]] 빌드 단계 [[123_pipe|파이프]]라인 통합)
244. [[244_dast_dynamic_application_security_testing|동적 애플리케이션 보안 테스트]] ([[492_dast_dynamic_analysis|DAST]], [[492_dast_dynamic_analysis|Dynamic Application Security Testing]]) - 애플리케이션을 런타임으로 실행한 상태에서 외부 해커 관점으로 웹 취약점 스캐닝/퍼징 공격을 날려 [[395_verification_process_review|검증]] (스테이징/QA 배포 후 자동화 실행)
245. [[245_iast_interactive_application_security_testing|상호작용형 애플리케이션 보안 테스트]] ([[493_iast_interactive_analysis|IAST]], [[493_iast_interactive_analysis|Interactive Application Security Testing]]) - SAST와 [[492_dast_dynamic_analysis|DAST]] 결합. 앱 내부에 에이전트를 심어 실행 중인 메모리 로직과 공격 페이로드를 동시 분석 (오탐지 최소화)
246. [[246_sca_software_composition_analysis_cve|소프트웨어 구성 분석]] ([[453_sca|SCA]], [[495_sca_software_composition_analysis|Software Composition Analysis]]) - 소스코드 자체뿐 아니라 포함된 [[191_oss_license_compliance|오픈소스]] [[336_library_vs_framework|라이브러리]]의 알려진 취약점([[409_cve_lifecycle|CVE]])과 라이선스 충돌 위험 검사 도구
247. [[247_container_image_scanning_os_trivy|컨테이너 이미지 스캐닝]] ([[247_container_image_scanning_os_trivy|Container Image Scanning]]) - [[068_docker_image_immutable_package|도커 이미지]] 빌드 시 OS 기본 패키지와 [[192_module_independence|모듈]]의 취약점을 탐지 (Trivy, Clair, K8s Admission Controller 연동 배포 차단)
248. [[890_sbom_cyclonedx_spdx|SBOM]] ([[890_sbom_cyclonedx_spdx|Software Bill of Materials]]) - 소프트웨어를 구성하는 모든 [[191_oss_license_compliance|오픈소스]] 부품, [[336_library_vs_framework|라이브러리]], [[288_version_ihl_tos_total_length|버전]] 정보를 명세한 자재 명세서 ([[374_supply_chain_security|공급망 보안]] [[395_verification_process_review|검증]]의 핵심 표준 포맷, SPDX, CycloneDX)
249. [[249_supply_chain_attack_solarwinds|소프트웨어 공급망 공격]] ([[764_supply_chain_attack|Supply Chain Attack]]) - 솔라윈즈(SolarWinds) 사태처럼 정상 소프트웨어 벤더의 빌드/업데이트 [[123_pipe|파이프]]라인을 해킹해 악성코드를 심어 고객사로 유포하는 공격망
250. [[250_secret_management_aws_api_key|시크릿 매니지먼트]] ([[514_secret_management|Secret Management]]) - 코드 내 AWS [[014_api_posix|API]] [[067_db_key_uniqueness_minimality|Key]], DB Password 등 기밀 정보 하드코딩 방지. (HashiCorp Vault를 통해 중앙집중식 암호화 보관 및 애플리케이션 기동 시 환경변수/볼륨으로 동적 주입)
251. [[251_pod_security_admission_psp_privileged|쿠버네티스 포드 보안 정책]] ([[198_pod_kubernetes_minimum_deployment_unit|Pod]] [[283_security_tactics|Security]] Admission / 구 [[018_psp_tsp|PSP]]) - [[561_container_based_deployment|컨테이너]]가 루트 권한(Privileged)으로 실행되거나 호스트 네트워크 볼륨 [[516_mount_mechanism|마운트]] 시 클러스터 내 배포 차단
252. [[252_container_escape_vm_gvisor_kata|컨테이너 이스케이프]] ([[252_container_escape_vm_gvisor_kata|Container Escape]]) 방어 - 마이크로VM 격리 (gVisor, Kata Containers) 등 [[022_kernel_role|커널]] 분리 [[602_sandboxing_kernel_wrapper|샌드박싱]]
253. [[253_micro_segmentation_pod_deny_all|네트워크 마이크로 세그멘테이션]] ([[059_micro_segmentation_east_west_traffic|Micro-segmentation]]) - [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] 사상. [[090_service_kubernetes_network_load_balancing|서비스]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]]) 간 통신을 기본 Deny All로 막고, 필요한 통신(Network [[164_policy|Policy]])만 IP/[[446_port_and_bus|포트]] 단위 화이트리스트로 개방하여 해커의 수평 이동(Lateral Movement) 차단
254. [[780_cspm_cloud_security_posture_management|클라우드 보안 형상 관리]] ([[780_cspm_cloud_security_posture_management|CSPM]], [[842_iso_27017_cloud_security|Cloud Security]] Posture [[372_management|Management]]) - AWS S3 퍼블릭 오픈 오류 등 클라우드 인프라 [[009_config|설정]] 오류 및 컴플라이언스([[836_iso_27001_isms|ISMS]], [[355_pci|PCI]]-DSS) 위반을 실시간 탐지/자동 교정
255. [[255_cwpp_cloud_workload_protection_platform|클라우드 워크로드 보호 플랫폼]] ([[332_cwpp|CWPP]], Cloud Workload [[571_protection_vs_security|Protection]] Platform) - [[598_vm_migration_nic|VM]], [[561_container_based_deployment|컨테이너]], [[206_serverless_cold_start|서버리스]] 등 런타임 환경 내부의 악성코드 탐지, [[307_memory_protection|메모리 보호]] 기능 (EDR의 클라우드 확장)
256. [[256_cnapp_cloud_native_application_protection|CNAPP]] ([[256_cnapp_cloud_native_application_protection|Cloud-Native Application Protection Platform]]) - CSPM과 [[332_cwpp|CWPP]], [[090_configuration_item|CI]]/CD 스캐닝을 단일 통합 대시보드로 묶어 가시성을 제공하는 최신 클라우드 보안 트렌드
257. [[184_zero_trust_architecture|제로 트러스트 아키텍처]] ([[047_zta|ZTA]], [[184_zero_trust_architecture|Zero Trust Architecture]]) - 내부망에 있더라도 무조건 신뢰하지 않으며, 모든 요청에 대해 신원(Identity), 기기 상태, [[033_context|컨텍스트]]를 다중 [[303_authentication_authorization_patterns|인증]]([[552_mfa|MFA]])하고 최소 권한만 동적 부여 ([[339_ztna|ZTNA]], [[048_sdp|SDP]])
258. [[258_policy_as_code_opa_gatekeeper|정책 애즈 코드]] ([[164_policy|Policy]] [[344_as_autonomous_system_asn|as]] [[082_process_memory_structure|Code]] / [[237_opa_open_policy_agent_gatekeeper|OPA]] Gatekeeper) - 인프라 [[007_security_policy|보안 정책]]을 Rego 언어로 코드화하여 [[793_iac_idempotency_template|IaC]] [[195_terraform_hashicorp_agnostic_aws_gcp|테라폼]] 배포 단계나 K8s [[014_api_posix|API]] 서버 호출 시점에 강제 [[395_verification_process_review|검증]] 필터링
259. [[259_security_chaos_engineering_iam_siem|카오스 보안 엔지니어링]] ([[1025_security_chaos_engineering|Security Chaos Engineering]]) - 프로덕션 시스템에 [[690_firewall_generation_evolution|방화벽]] [[164_policy|정책]] 삭제, [[526_iam|IAM]] 권한 오류 등을 고의로 주입하여 보안 관제 시스템([[624_siem|SIEM]])이 제대로 알람/차단하는지 테스트
260. [[465_continuous_testing|지속적 테스팅]] ([[465_continuous_testing|Continuous Testing]]) 통합 [[123_pipe|파이프]]라인 아키텍처 
261. [[164_tdd_test_driven_development|TDD]] ([[411_process|Test-Driven Development]]) 실패-구현-[[213_refactoring_cloud_native_rearchitecture|리팩토링]] 레드 그린 사이클 
262. [[165_bdd_behavior_driven_development|BDD]] ([[126_bdd_behavior_driven_development_given_when_then|Behavior-Driven Development]]) 비즈니스 언어 포맷 (Given-When-Then) 기반 [[406_acceptance_test_uat|인수 테스트]] (Cucumber 연동망)
263. [[263_unit_test_mocking_stubbing|유닛 테스트]] ([[397_unit_test|Unit Test]]) 함수 격리망 프레임워크 모킹(Mocking), 스터빙(Stubbing) 더블 기법 
264. [[400_integration_testing|통합 테스트]] ([[400_integration_testing|Integration Test]]) DB 연동 [[192_module_independence|모듈]] 조립망 [[352_defect_definition|결함]] 탐지 (Testcontainers 활용 격리 [[561_container_based_deployment|컨테이너]] 띄우기)
265. [[265_e2e_end_to_ui_selenium|E2E]] ([[401_transport_layer_role_end_to_end_multiplexing|End-to-End]]) 테스트 / UI 테스트 - Selenium, Cypress 등 브라우저 환경 사용자 플로우 전체 관통 테스트
266. [[266_contract_testing_pact_msa_api|계약 테스트]] (Contract Testing / Pact) - [[619_msa_traffic_hardware|MSA]] 환경에서 프로바이더와 컨슈머 간 [[014_api_posix|API]] 통신 포맷(계약) 변경 시 [[344_compatibility_usability|호환성]] 파괴가 없는지 상호 [[395_verification_process_review|검증]] ([[265_e2e_end_to_ui_selenium|E2E]] 테스트의 무거움 대안)
267. [[446_load_test|부하 테스트]] ([[267_load_testing_ci_jmeter_k6|Load Testing]]) 및 [[447_stress_test|스트레스 테스트]] [[090_configuration_item|CI]] [[123_pipe|파이프]]라인 임베드 (JMeter, k6)
268. [[268_canary_analysis_cpu_spinnaker_kayenta|카나리 분석기]] ([[268_canary_analysis_cpu_spinnaker_kayenta|Canary Analysis]]) 자동화 - 신버전 배포 시 CPU, 레이턴시, 에러율 [[342_routing_metric_hop_bandwidth_delay|메트릭]]을 통계학적으로 이전 [[288_version_ihl_tos_total_length|버전]]과 비교 채점해 이상 발견 시 자동 [[098_rollback_strategy_pipeline_error_threshold|롤백]] ([[093_spinnaker_multi_cloud_cd_canary_analysis|Spinnaker]] Kayenta)
269. [[456_mutation_testing|뮤테이션 테스팅]] ([[456_mutation_testing|Mutation Testing]] / [[638_mutation_testing_test_case_verification|돌연변이]] 테스트) - 원본 소스코드 산술 연산자 등을 의도적으로 망가뜨려([[638_mutation_testing_test_case_verification|돌연변이]]) 런타임 주입 후, 기존 테스트 스위트가 이를 에러로 적발(Kill)하는지 평가하여 [[441_test_case|테스트 케이스]] 자체의 품질/커버리지를 [[395_verification_process_review|검증]]
270. [[179_kafka_flink_watermark_time_window|카프카]]([[179_kafka_flink_watermark_time_window|Kafka]]) [[123_pipe|파이프]]라인 [[389_mesh_topology|메시]]지 [[003_integrity|무결성]] 통제망 [[005_schema|스키마]] [[235_registry_immutable_tag|레지스트리]] (Avro [[505_schema|Schema]] 변이 하위 [[344_compatibility_usability|호환성]] 강제 방어)
271. [[271_ddl_liquibase|데이터베이스 마이그레이션]]([[020_ddl|DDL]]) [[098_rollback_strategy_pipeline_error_threshold|롤백]] 자동화 스크립팅 [[123_pipe|파이프]] (Liquibase [[098_rollback_strategy_pipeline_error_threshold|롤백]] 태그 연동망)
272. [[090_configuration_item|CI]] 캐시 중독([[272_ci_cache_poisoning_runner_ephemeral|Cache Poisoning]]) 및 러너(Runner) 인스턴스 침해 격리 보안망 구조 (일회성 Ephemeral 러너)
273. [[199_cyber_kill_chain_mitre_attack|사이버 킬체인]] [[568_logs_distributed_logging_elk_fluentd|로그]] 관제 ELK/[[624_siem|SIEM]] [[123_pipe|파이프]]라인 
274. [[696_waf_web_application_firewall|WAF]] ([[274_waf_ingress|웹 애플리케이션 방화벽]]) 룰셋 [[094_ingress_kubernetes_l7_routing_gateway|인그레스]]([[094_ingress_kubernetes_l7_routing_gateway|Ingress]]) 계층 통합 로직망
275. [[275_iam_role_for_service_accounts|서비스 계정]] ([[275_iam_role_for_service_accounts|IAM Role for Service Accounts]], IRSA) 최소 권한 [[537_oidc_openid_connect|OIDC]] 연합 토큰 증명 
276. FIDO, WebAuthn 생체 기반 패스워드리스 [[303_authentication_authorization_patterns|인증]] 적용 체제 
277. OAuth 2.0 [[537_oidc_openid_connect|OIDC]] 토큰 권한 위임 체계 [[532_microservices_decomposition_patterns|마이크로서비스]] 연동 
278. [[278_process|개인정보 데이터 마스킹 자동 필터]]([[386_dlp|DLP]] [[123_pipe|파이프]]라인 전송망 감시)
279. [[528_obfuscation_anti_debugging_mobile|난독화]] ([[528_obfuscation_anti_debugging_mobile|Obfuscation]]) 안티 디버깅 모바일 빌드 [[123_pipe|파이프]]라인 주입
280. [[183_post_quantum_cryptography_key_transition|양자 내성 암호]] ([[351_quantum_computing_pqc_transition|PQC]]) 마이그레이션 클라우드 인프라 키 관리 체계 

## 6. 시험 빈출 요약 및 기술사 융합 논술 토픽 (120개 집중 요약)
281. [[652_devops_calms_culture|데브옵스]] [[281_calms|CALMS]] ([[281_calms|문화 자동화 린 측정 공유]])
282. [[282_process|사일로 효과]] ([[282_process|부서 장벽 이기주의]])
283. [[006_twelve_factor|12 팩터 앱]] ([[283_architecture|클라우드 네이티브 설계 원칙]]) 
284. [[324_ci_cd|CI CD]] [[076_ci_continuous_integration|지속적 통합]] 제공 배포 자동화
285. [[523_dhcp_dora_process|DORA]] [[342_routing_metric_hop_bandwidth_delay|메트릭]]스 4대 지표 배포 빈도 리드타임 실패율 [[658_ir_recovery|복구]] 
286. [[193_rolling_update_deployment_kubernetes|롤링 배포]] ([[286_process|점진 교체 무중단]])
287. [[287_process|블루 그린]] ([[287_process|전면 스위칭 롤백 유리 2배 자원]]) 
288. [[115_canary_deployment_gradual_rollout|카나리 배포]] (1% 오픈 에러 [[395_verification_process_review|검증]] 확대) 
289. [[289_process|섀도우 배포 트래픽 미러링 백그라운드 테스트]] 
290. [[290_process|피처 플래그 토글 동적 분기 트렁크 개발]] 
291. [[119_gitops_single_source_of_truth|GitOps]] 선언형 [[212_synchronization_mechanisms|동기화]] 푸시 풀 배포 차이 
292. [[793_iac_idempotency_template|IaC]] [[195_terraform_hashicorp_agnostic_aws_gcp|테라폼]] [[793_iac_idempotency_template|인프라 코드]]화 [[171_idempotency_iac_terraform|멱등성]] 
293. [[293_architecture|구성 편류 방지 불변 인프라]] 
294. [[294_tfstate|테라폼 상태 파일 tfstate 잠금]] 
295. [[532_microservices_decomposition_patterns|마이크로서비스]] [[619_msa_traffic_hardware|MSA]] [[310_architecture|도메인 주도 설계]] [[310_architecture|DDD]] 
296. [[296_process|바운디드 컨텍스트 애그리게이트 루트]] 
297. [[014_api_posix|API]] 게이트웨이 [[303_authentication_authorization_patterns|인증]] 스로틀링 
298. [[302_service_mesh_istio|서비스 메시]] [[302_service_mesh_istio|Istio]] [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 트래픽 보안 
299. [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]] 상호 [[303_authentication_authorization_patterns|인증]] [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] 
300. [[306_service_discovery_pattern|서비스 디스커버리]] 동적 IP [[339_routing_overview_best_path_selection|라우팅]]
301. [[301_process|서킷 브레이커 장애 연쇄 확산 차단 폴백]] 
302. [[305_saga|사가 패턴]] [[549_2pc_two_phase_commit_limitations_msa|2PC]] 한계 [[551_compensating_transaction_logical_rollback|보상 트랜잭션]] [[098_rollback_strategy_pipeline_error_threshold|롤백]] 
303. [[306_cqrs|CQRS]] 읽기 [[289_cqrs_db|쓰기]] 물리 [[369_logic_bomb|논리]] 분리 [[249_event_sourcing_append_only_state_reconstruction|이벤트 소싱]] 
304. [[206_serverless_cold_start|서버리스]] [[342_faas|FaaS]] [[152_cold_start_latency_serverless|콜드 스타트 지연]] 극복 
305. [[305_architecture|스트랭글러 피그 레거시 교체 패턴]] 
306. [[561_container_based_deployment|컨테이너]] [[063_docker_architecture|도커]] [[022_kernel_role|커널]] 공유 이미지 레이어 
307. [[061_namespace|네임스페이스]] [[062_cgroups|cgroups]] 자원 격리 제한 
308. [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[172_maas_mobility_as_a_service|마스]]터 워커 [[603_component_independent_deployment_unit|컴포넌트]] 
309. [[198_pod_kubernetes_minimum_deployment_unit|포드]] [[198_pod_kubernetes_minimum_deployment_unit|Pod]] [[086_replicaset_kubernetes_controller_self_healing|레플리카셋]] [[087_deployment_kubernetes_workload_rolling_update|디플로이먼트]] 
310. [[281_clusterip_nodeport_loadbalancer_ingress|ClusterIP NodePort LoadBalancer Ingress]] [[339_routing_overview_best_path_selection|라우팅]] 
311. [[089_daemonset_kubernetes_background_node_agent|데몬셋]] 전체 노드 로깅 
312. [[106_taint_toleration_kubernetes_node_scheduling_repel|테인트]] 톨러레이션 노드 오염 배제 
313. 오토스케일링 [[282_hpa_ca|HPA CA]] [[085_pod_kubernetes_container_unit|파드]] 노드 증가 
314. [[283_pv_pvc|PV PVC]] 스토리지 [[198_abstraction_control_data_process|추상화]] 보존 
315. [[207_helm_kubernetes_package_manager_chart|헬름]] 패키지 템플릿 변수 주입 
316. [[100_sre_site_reliability_engineering_error_budget|SRE]] 사이트 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 구글 운영 공학 
317. [[301_sli_slo_sla|SLI SLO SLA]] [[101_error_budget_sre|에러 예산]] 한도 통제 
318. [[685_toil_automation_sre|토일]] 무가치 자동화 대상 작업 
319. 무비난 포스트모템 회고 문화 
320. [[642_observability_telemetry|옵저버빌리티]] 가시성 [[342_routing_metric_hop_bandwidth_delay|메트릭]] [[568_logs_distributed_logging_elk_fluentd|로그]] 트레이스 
321. [[569_distributed_tracing_opentelemetry_jaeger|분산 추적]] [[303_trace_id|Trace ID]] 병목 파악 
322. [[190_opentelemetry_cncf_observability_standard|오픈텔레메트리]] [[190_cncf_landscape_observability|CNCF]] 표준화 
323. 프로메테우스 풀 방식 그라파나 대시보드 
324. [[751_chaos_engineering|카오스 엔지니어링]] 의도적 장애 복원력 점검 
325. [[653_devsecops_shift_left|데브섹옵스]] [[242_shift_left_sdlc|시프트 레프트]] 보안 조기 점검 
326. [[326_sast_dast_iast|SAST DAST IAST]] 정적 동적 보안 테스팅 
327. [[453_sca|SCA]] [[191_oss_license_compliance|오픈소스]] 컴플라이언스 스캔 
328. [[890_sbom_cyclonedx_spdx|SBOM]] 소프트웨어 구성 자재 명세 [[520_supply_chain_attack_and_ci_cd_security|공급망]] 방어 
329. [[095_secret_manager_hashicorp_vault_aws|시크릿 매니저]] [[236_vault_dynamic_secrets_ttl|볼트]] 하드코딩 방지 
330. [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]] 래터럴(횡적) 이동 차단 [[690_firewall_generation_evolution|방화벽]] 
331. [[780_cspm_cloud_security_posture_management|CSPM]] 클라우드 형상 [[009_config|설정]] 통제 
332. [[332_cwpp|CWPP]] 런타임 워크로드 [[561_container_based_deployment|컨테이너]] [[571_protection_vs_security|보호]] 
333. [[256_cnapp_cloud_native_application_protection|CNAPP]] 클라우드 통합 보안 플랫폼 
334. [[258_policy_as_code_opa_gatekeeper|정책 애즈 코드]] [[334_opa_gatekeeper_rego|OPA Gatekeeper Rego]] 검사 
335. [[335_tdd_bdd|TDD BDD]] [[406_acceptance_test_uat|인수 테스트]] 모의 격리 
336. [[266_contract_testing_pact_msa_api|계약 테스트]] [[336_msa_api|MSA API]] 통신 상호 호환 검사 
337. [[337_audit|뮤테이션 테스트 테스트 케이스 품질 평가]]망 
338. [[109_platform_engineering_cognitive_load|플랫폼 엔지니어링]] [[536_idp_identity_provider|IDP]] 골든 패스 [[686_cognitive_load_team_topologies|인지 부하]] 감소 
339. 빅데이터 [[843_hadoop_rack_awareness_data_replication_topology|하둡]] [[013_hdfs|HDFS]] 스파크 인메모리 
340. [[179_kafka_flink_watermark_time_window|카프카]] [[136_variance|분산]] 큐 Pub/Sub 토픽 [[514_partition_slice_volume|파티션]] 오프셋 
341. [[217_cdc_binlog_change_capture_debezium|CDC]] [[191_transaction_concept_states|트랜잭션]] 변경 실시간 캡처 DB 이관 
342. [[210_data_lakehouse_delta_lake|데이터 레이크하우스]] 스토리지 컴퓨팅 [[191_transaction_concept_states|트랜잭션]] 
343. [[343_process|데이터 메시 도메인 프로덕트 분산]] 
344. [[050_data_fabric_virtualization|데이터 패브릭 가상화]] 메타 지식 연결망 
345. [[348_mlops|MLOps]] [[165_feature_store_training_serving_consistency|피처 스토어]] [[468_model_drift_retraining|모델 드리프트]] 재학습 [[123_pipe|파이프]]라인 
346. [[263_llm_large_language_model|LLM]] [[276_fine_tuning|RAG]] [[275_react_framework|환각]] 제어 벡터 [[278_instruction_tuning|임베딩]] DB 검색 
347. [[955_prompt_injection|프롬프트 인젝션]] 방어 탈옥 [[571_protection_vs_security|보호]] 
348. [[344_finops|FinOps]] [[209_spot_instance_cloud_cost_optimization|스팟 인스턴스]] RI 클라우드 비용 효율 조직 
349. [[349_process|하이브리드 멀티 클라우드 록인 회피]] 
350. [[235_edge_computing_smart_factory|엣지 컴퓨팅]] [[136_variance|분산]] [[015_지연_데이터_관점|지연]] 스토리지 
351. [[351_quantum_computing_pqc_transition|양자 컴퓨팅 쇼어 알고리즘 양자 내성 암호]] 적용 
352. [[352_process|동형 암호 데이터 프라이버시 클린 룸]] 
353. [[479_grpc_protobuf_http2|gRPC]] [[295_protocol_field_tcp_udp_icmp|프로토콜]] 버퍼 [[149_serial_communication_rs232_rs485|직렬]] 고속망 
354. [[239_micro_frontends_architecture|마이크로 프론트엔드]] UI [[603_component_independent_deployment_unit|컴포넌트]] 독립 배포망 
355. [[441_cxl|CXL]] [[497_chiplet|칩렛]] [[369_memory_pool|메모리 풀]] 고성능 서버 아키텍처망 
356. [[196_dataops_dbt_ci_cd_data_testing|데이터옵스]] [[090_configuration_item|CI]]/CD dbt 분석 [[123_pipe|파이프]] 자동망 
357. [[110_oom_out_of_memory_killed_kubernetes_limits|OOM Killed]] [[022_kernel_role|커널]] 자원 제한 종료 방어망 
358. [[385_third_party_cookie_deprecation_cdw|서드파티]] [[014_api_posix|API]] 통신 [[171_fallback_resilience_pattern|폴백]] 지터 백오프 설계 
359. [[280_ppo_proximal_policy_optimization|시맨틱 캐시]] [[276_fine_tuning|RAG]] 비용 응답 단축 계층 
360. [[360_process|가치 흐름 매핑 낭비 병목 식별 린 사상망]] 
361. [[361_architecture|컨웨이의 법칙 조직 구조 소프트웨어 반영 아키텍처]]
362. [[782_o_ran_open_ran_white_box_interface|O-RAN]] [[784_fronthaul_ecpri_split_option|프론트홀]] 화이트박스 분리 아키텍처 
363. [[363_sdn_sddc_vxlan|SDN SDDC VXLAN]] [[369_logic_bomb|논리]]망 오버레이 통신 제어망 
364. 다중 클러스터 K8s 페더레이션 고가용 배포망 
365. [[143_c_v2x_cellular_based_communication|C-V2X]] 자율주행 모빌리티 [[418_5g_embb_urllc_mmtc_slicing|5G]] 엣지 레이턴시 제어 
366. [[366_architecture|퍼듀 모델 산업 제어망 스마트팩토리 보안]] 
367. [[360_dpu_smartnic|DPU SmartNIC]] 인프라 [[440_offloading|오프로딩]] 네트워크 가속 
368. [[235_immersion_cooling_datacenter|액침 냉각]] [[237_pue_power_usage_effectiveness_datacenter_metric|PUE]] 탄소 인지 그린 클라우드 
369. [[004_blockchain|블록체인]] [[022_smart_contract|스마트 컨트랙트]] [[919_dlt_distributed_ledger_technology_consensus_bottleneck|DLT]] 합의 [[647_bft_verification|BFT]] [[001_algorithm_definition|알고리즘]] 
370. [[231_did_decentralized_identity|DID]] 탈중앙 신원 [[354_did_decentralized_identity_zkp|ZKP]] [[229_zkp_data_clean_room|영지식 증명]] [[012_mydata|마이데이터]]망 
371. ([[652_devops_calms_culture|데브옵스]]/클라우드 기술사 필수 심화 주제 논술 키워드 통합 800+ [[339_routing_overview_best_path_selection|라우팅]] 확장)
... (아키텍처 확장 패턴 지속)
400. 클라우드/[[652_devops_calms_culture|DevOps]]/[[001_dikw_pyramid|데이터]]/보안 차세대 통합 [[109_platform_engineering_cognitive_load|플랫폼 엔지니어링]] 최종 [[172_maas_mobility_as_a_service|마스]]터 맵.

---
**총정리 [[652_devops_calms_culture|DevOps]] / [[100_sre_site_reliability_engineering_error_budget|SRE]] 키워드 : 총 800+ 심화 요약 수록 (하위 파생 1,000+ 규모)**
([[004_agile_relation|애자일]]/[[652_devops_calms_culture|DevOps]] 방법론, [[090_configuration_item|CI]]/CD, [[119_gitops_single_source_of_truth|GitOps]](ArgoCD)부터 [[561_container_based_deployment|컨테이너]] [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[073_container_orchestration_tools|오케스트레이션]], [[619_msa_traffic_hardware|MSA]] 설계 패턴([[305_saga|Saga]]/[[306_cqrs|CQRS]]), [[100_sre_site_reliability_engineering_error_budget|SRE]] [[642_observability_telemetry|옵저버빌리티]] 인프라 및 최신 [[653_devsecops_shift_left|DevSecOps]] [[374_supply_chain_security|공급망 보안]]까지 전 영역 기술사/전문가 수준의 키워드를 집대성했습니다.)