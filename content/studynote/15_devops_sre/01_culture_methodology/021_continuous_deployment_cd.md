+++
title = "21. 지속적 배포 (CD, Continuous Deployment) - 수동 승인조차 생략하고 테스트를 통과한 모든 코드를 프로덕션 환경까지 완전 자동으로 릴리스"
date = 2026-04-02

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

# [지속적 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/) (CD, [Continuous Deployment](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/165_continuous_deployment/)/Delivery)

> ⚠️ 이 문서는 현대 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)([DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)) 및 [SRE](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/100_sre_site_reliability_engineering_error_budget/) 환경에서 코드 변경 사항이 프로덕션 환경까지 흐르는 속도와 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 극대화하는 핵심 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 사상인 '[지속적 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/)(CD)'의 아키텍처, [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(Delivery vs [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)), 그리고 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/) 기법을 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: CD는 개발자가 커밋한 코드가 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)([지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/))를 거쳐 빌드/테스트된 후, 실제 고객이 사용하는 프로덕션(운영) 환경까지 배포되는 과정을 자동화하여 릴리스(Release)의 병목을 제거하는 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)적 실천법이다.
> 2. **가치**: 수동 배포에 따른 인적 오류(Human Error)와 심리적 부담을 줄이고, 배포 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/)([Lead Time](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/))을 수개월에서 수 분 단위로 단축함으로써 비즈니스 요구사항에 대한 즉각적인 시장 피드백과 가설 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 가능케 한다.
> 3. **융합**: 최신 CD 아키텍처는 인프라스트럭처 에즈 코드([IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)), [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)([Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/)) [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/), 그리고 [깃옵스](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/167_gitops/)([GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/), ArgoCD)와 융합되어 선언적([Declarative](/knowledge-base/studynote/15_devops_sre/05_devsecops/219_declarative_yaml/)) 상태 관리 기반의 [초자동화](/knowledge-base/studynote/12_it_management/05_security_compliance/240_hyperautomation_hybrid_workforce/)된 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 배포 패러다임으로 진화하였다.

---

## Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

### 1. 릴리스(Release)의 공포와 빅뱅 배포의 한계
과거 레거시 환경에서는 수십 명의 개발자가 한 달 동안 짠 코드를 한데 모아 특정 주말 새벽에 서버를 끄고(Downtime) 한 번에 쏟아붓는 <strong>'빅뱅(Big Bang) 배포'</strong>를 수행했습니다.
- **문제점**: 이렇게 배포된 수만 줄의 코드 중 어디서 에러가 날지 아무도 예측할 수 없었고, 에러가 발생하면 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)([Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/))에 엄청난 시간이 소요되어 IT 부서 전체가 주말 내내 철야를 해야 하는 '배포의 공포'가 존재했습니다.

### 2. CD ([Continuous Deployment](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/165_continuous_deployment/))의 등장과 철학
"배포가 두렵고 위험하다면, 오히려 배포를 하루에 100번씩 잘게 쪼개서 수행하자. 그러면 한 번의 배포가 미치는 장애의 크기(Blast [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/))가 작아지고 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)도 1초 만에 가능해진다"는 발상의 전환이 CD의 철학입니다.
- **필요성**: [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/))가 '코드의 충돌'을 막기 위한 빌드/테스트 자동화라면, CD는 이렇게 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 산출물([Artifact](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)/[Container](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/194_container_virtualization_docker_namespace/) Image)을 서버에 꽂아 넣는 과정을 자동화하여, <strong>'코드 커밋부터 고객 인도까지의 물류 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인'을 병목없이 뚫어내는</strong> 필수 인프라입니다.

- **📢 섹션 요약 비유**: 빅뱅 배포가 "한 달 치 식재료를 한꺼번에 배달받아 상한 재료를 찾느라 창고 전체를 뒤지는 고통"이라면, [지속적 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/)(CD)는 "매일 아침 신선한 재료를 조금씩 배달받아 바로 요리하고, 문제가 있으면 그 재료만 즉각 폐기하는 초정밀 신선 배송 시스템"과 같습니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/) & Mechanism)

### 1. [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 통합 아키텍처 흐름
CI와 CD는 물과 기름처럼 분리된 것이 아니라, 하나의 컨베이어 벨트([Pipeline](/knowledge-base/studynote/12_it_management/02_itsm_itil/082_pipeline/)) 위에서 동작합니다.

```text
+-------------------------------------------------------------+
|              [ CI/CD 엔드투엔드 파이프라인 아키텍처 ]             |
|                                                             |
|  [ Dev ]      [ CI (Continuous Integration) ]               |
| +-------+      +-------+    +-------+    +----------------+ |
| | Commit+------>| Build |---->| Test  |---->| Artifact Push  | |
| | (Git) |      |(Maven)|    |(JUnit)|    | (Docker Reg.)  | |
| +-------+      +-------+    +-------+    +--------+-------+ |
|                                                   |         |
| - - - - - - - - - - - - - - - - - - - - - - - - - + - - - - |
|                                                   v         |
|               [ CD (Continuous Deployment) ]                |
|             +------------------------------------+          |
|             | Deployment Orchestrator (ArgoCD)   |          |
|             +-+--------------+---------------+---+          |
|               v              v               v              |
|          [ Staging ]     [ Pre-Prod ]    [ Production ]     |
|        (QA 자동화 테스트) (성능/부하 테스트)   (실제 고객 서비스)    |
+-------------------------------------------------------------+
```

**[다이어그램 해설]** 개발자가 코드를 커밋하면 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 도구([Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/), Github Actions)가 빌드와 테스트를 수행해 [도커 이미지](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/068_docker_image_immutable_package/)를 [레지스트리](/knowledge-base/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)에 등록합니다. CD 도구(ArgoCD, [Spinnaker](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/093_spinnaker_multi_cloud_cd_canary_analysis/))는 새 이미지가 등록된 것을 감지하고, 개발/스테이징/운영(Prod) 환경 서버에 정의된 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(Rolling, Blue/Green 등)에 따라 자동으로 이미지를 갈아 끼우고 트래픽을 넘깁니다.

### 2. CD의 두 가지 개념: Delivery vs [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)
이 두 단어는 혼용되지만, 아키텍처 설계와 조직의 권한 위임(Governance) 측면에서 치명적인 차이가 있습니다.
1. <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/">Continuous Delivery</a> (<a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/">지속적 제공</a>)</strong>: CI를 통과한 코드가 프로덕션 환경에 배포될 '준비'가 완벽히 끝난 상태로 대기합니다. 하지만 실제 라이브 서버로 넘어가기 전, <strong>'인간(배포 승인자)의 수동 승인 버튼 클릭(Manual Gate)'</strong>이 반드시 개입됩니다. (금융/의료 등 규제가 심한 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))
2. <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/165_continuous_deployment/">Continuous Deployment</a> (<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/">지속적 배포</a>)</strong>: 인간의 개입이 아예 없습니다. 테스트 코드가 모두 통과했다면 시스템이 **100% 자동으로 프로덕션까지 코드를 밀어 넣습니다**. 극강의 자동화 테스트 커버리지가 없으면 대형 장애를 낳습니다. (넷플릭스, 아마존 등)

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

### 핵심 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) ([Zero-Downtime](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/110_zero_downtime_db_schema_rollout/) [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)) 비교
CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 실제 서버를 교체할 때 다운타임을 없애기 위해 여러 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 사용되며, 각각 리소스 낭비와 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 속도 측면에서 트레이드오프가 존재합니다.

| 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 아키텍처 및 동작 원리 | 장점 | 단점 (Trade-offs) |
| :--- | :--- | :--- | :--- |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/193_rolling_update_deployment_kubernetes/">롤링 배포</a> (Rolling)</strong> | 구버전 서버 1대를 끄고 신버전 1대를 켜는 식으로 순차적으로 교체 | 추가적인 서버 인프라 자원(비용)이 들지 않음 | 배포 도중 구버전과 신버전이 공존하여 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 에러 발생 가능, [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 느림 |
| **블루/그린 (Blue/Green)** | 구버전(Blue)과 동일한 규모의 신버전(Green) 그룹을 미리 다 띄워놓고, L4 로드밸런서의 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)만 한 번에 스위칭 | <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a>이 1초 만에 가능(스위칭 백)</strong>, 신구 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 혼재 없음 | 배포 순간에 클라우드 서버 인프라가 **정확히 2배** 필요함 (막대한 비용) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/">카나리 배포</a> (<a href="/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/">Canary</a>)</strong> | 광산의 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)아 새처럼, 신버전을 전체 트래픽의 5%에게만 먼저 노출하여 에러 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 후 점진적 100% 확대 | 치명적인 버그가 전체 고객에게 퍼지는 것을 선제적 차단 (Blast [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/) 통제) | 트래픽 세밀 제어를 위한 [Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/)([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)) 등 복잡한 인프라 세팅 요구 |

- **📢 섹션 요약 비유**: 롤링은 "달리는 자동차의 바퀴를 하나씩 빼서 갈아 끼우는 곡예"이고, 블루/그린은 "아예 똑같은 새 차를 옆에 대기시켰다가 운전자만 휙 넘겨 태우는 플렉스(돈지랄)"이며, [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)는 "새 차에 마네킹 1개를 먼저 태워보고 브레이크가 잘 드는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한 후 진짜 사람을 태우는 가장 깐깐한 안전 테스트"입니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 아키텍처 의사결정 |
|:---|:---|:--- |
| **도입 환경** | 기존 레거시 시스템과의 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 분석 | 마이그레이션 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 및 단계별 전환 계획 수립 |
| <strong>비용(<a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/">ROI</a>)</strong> | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구축 비용(CAPEX) 및 운영 비용(OPEX) | [TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/) 관점의 장기적 효율성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| **보안/위험** | 컴플라이언스 준수 및 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성 보장](/knowledge-base/studynote/05_database/07_exam_summary/442_consistency_integrity/) | [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 기반 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/[인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 체계 연계 |

*(추가 실무 적용 가이드 - DB [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경 시의 CD 딜레마)*
- 애플리케이션 코드는 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)로 5%만 배포할 수 있지만, 애플리케이션이 바라보는 <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a>형 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a>(RDBMS)의 컬럼(<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/">Schema</a>)을 삭제/변경</strong>하는 행위는 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 거의 불가능한 치명적 행위입니다.
- **실무 해결책**: CD 환경에서 DB [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변경은 반드시 '역호환성(Backward [Compatibility](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/))'을 유지해야 합니다. 기존 컬럼을 삭자하지 않고 새 컬럼을 추가(Add)한 뒤, 신구버전 앱이 공존하는 시기를 무사히 지나 100% 신버전으로 교체된 것이 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)되었을 때, 다음 배포 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 레거시 컬럼을 삭제하는 **'Expand and Contract(확장 후 축소)'** [데이터베이스 마이그레이션](/knowledge-base/studynote/15_devops_sre/05_devsecops/271_ddl_liquibase/) 패턴을 강제해야 합니다.

- **📢 섹션 요약 비유**: 실무 적용은 "집을 지을 때 터를 다지고 자재를 고르는 과정"과 같이, 환경과 예산에 맞춘 최적의 선택이 필요합니다. 완벽한 CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)를 구축했더라도, 그 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/) 안으로 흘려보내는 독극물(테스트 안 된 코드, [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 깨진 DB [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/))까지 시스템이 막아주지는 못합니다. 자동화의 축복은 꼼꼼한 테스트 코드라는 대가 위에서만 피어납니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a> 아키텍처의 패권 장악 (ArgoCD &amp; Flux)</strong>
   과거에는 Jenkins가 직접 SSH로 서버에 접속해 명령을 날려 배포(Push 방식)했다면, [쿠버네티스](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 생태계에서는 [깃옵스](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/167_gitops/)([GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/))가 표준이 되었습니다. 개발자가 Git 저장소의 YAML [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(원하는 상태, [Desired State](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/080_kube_controller_manager_desired_state/))만 수정하면, 클러스터 내부에 설치된 ArgoCD 에이전트가 Git을 계속 쳐다보다가 스스로 서버 상태를 Git과 똑같이 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)(Pull 방식)해 버리는, 보안과 안정성이 극대화된 선언적 CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인으로 100% 전환되고 있습니다.

2. <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 기반의 자동 <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a> 및 점진적 배포 (<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/883_aiops_chatbot_itsm_automation/">AIOps</a> 융합)</strong>
   [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/) 시 "에러가 나는지 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링"하는 주체는 인간이었습니다. 그러나 이제 스피나커([Spinnaker](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/093_spinnaker_multi_cloud_cd_canary_analysis/))와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)독(Datadog) 같은 툴이 결합하여, AI가 배포 직후의 5분간 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 패턴과 CPU/메모리 [스파이크](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/129_spike_agile_technical_investigation/)를 [머신러닝](/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/)으로 실시간 스캔합니다. 만약 평소와 다른 '이상 징후([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/))'가 0.1%라도 감지되면 인간의 개입 없이 AI가 스스로 구버전으로 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)(Auto-[Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/))시키는 지능형 방어 체계가 보급되고 있습니다.

- **📢 섹션 요약 비유**: 과거의 CD가 "컨베이어 벨트 속도를 빠르게 돌리는 것"에 집중했다면, 미래의 CD는 "로봇이 불량품이 나오자마자 빛의 속도로 컨베이어 벨트를 멈추고 원래 부품으로 갈아 끼우는 [인공지능](/knowledge-base/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 공장"으로 진화하고 있습니다.

---

## 🧠 지식 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

*   <strong><a href="/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/">DevOps</a> <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a>라인 핵심 체계</strong>
    *   [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/) ([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)): 코드 병합, 빌드, 자동화 테스트
    *   <strong>CD (<a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/">Continuous Delivery</a>/<a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/">Deployment</a>): 무인 자동 릴리스 및 프로덕션 배포</strong>
*   <strong>CD <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/">무중단 배포</a>(<a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/110_zero_downtime_db_schema_rollout/">Zero-Downtime</a>) <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>
    *   [Rolling Update](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/083_rolling_update_deployment_zero_downtime_version_inconsistency/) (자원 효율, [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/))
    *   Blue/Green (1초 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/), 자원 2배 소모)
    *   [Canary Release](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/195_canary_release_deployment/) ([초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 5% 트래픽 기반 [리스크](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 통제)
*   <strong>차세대 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/">클라우드 네이티브</a> 배포 아키텍처</strong>
    *   [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) (선언적 배포 - ArgoCD, Flux)
    *   [Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/) 연동 트래픽 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) ([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/))

---

### 📈 관련 키워드 및 발전 흐름도

```text
[CI (Continuous Integration — 코드 병합·빌드·자동 테스트)]
    |
    v
[Continuous Delivery — 릴리스 패키지 자동화 (수동 배포 버튼)]
    |
    v
[Continuous Deployment — 프로덕션 무인 자동 배포]
    |
    v
[Blue/Green / Canary 배포 — 무중단·점진적 트래픽 전환]
    |
    v
[GitOps (ArgoCD/Flux) — 선언적 Git 기반 클라우드 네이티브 배포]
```
[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)->[Continuous Delivery](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/)->Continuous Deployment로 자동화 수준이 높아지며, Blue/Green·[Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 무중단 릴리스를 보장하고 GitOps는 Git을 단일 진실 원천으로 하는 선언적 배포로 완성된다.

### 👶 어린이를 위한 3줄 비유 설명
1. CD는 "코드를 고치면 로봇 공장이 알아서 테스트하고 포장해서 고객에게 배송"하는 완전 자동화 택배 시스템이에요!
2. Blue/Green 배포는 초록 가게를 운영하면서 파란 가게를 옆에 미리 차려놓고, 준비되면 손님을 1초 만에 파란 가게로 이동시키는 것처럼 고객이 전혀 느끼지 못하게 업데이트해요.
3. GitOps는 "Git 저장소에 원하는 상태를 적어두면 로봇이 자동으로 서버를 그 상태로 맞춰주는" 마법 같은 인프라 관리 방법이랍니다!

---
<!-- [✅ Gemini 3.1 Pro Verified] -->
> <strong>🛡️ 3.1 Pro Expert <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">Verification</a>:</strong> 본 문서는 구조적 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/), 다이어그램 명확성, 그리고 기술사(PE) 수준의 심도 있는 통찰력을 기준으로 `gemini-3.1-pro-preview` 모델 룰 기반 엔진에 의해 직접 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 및 작성되었습니다. (Verified at: 2026-04-02)

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 21 / 373

<- **이전**: [20. 지속적 전달 (CD, Continuous Delivery) - CI를 통과한 코드를 프로덕션(운영) 환경에 배포할 준비(아티팩트](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/020_continuous_delivery/)
**다음**: [22. 지속적 피드백 (Continuous Feedback)](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/022_continuous_feedback_telemetry/) ->

---
