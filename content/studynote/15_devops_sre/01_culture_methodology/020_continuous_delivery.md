+++
title = "20. 지속적 전달 (CD, Continuous Delivery) - CI를 통과한 코드를 프로덕션(운영) 환경에 배포할 준비(아티팩트 생성)를 완료하되, 실제 배포는 인간의 수동 승인을 거침"
description = "지속적 통합(CI)을 통과한 코드를 프로덕션 환경으로 안전하게 릴리스할 수 있는 상태로 자동 유지하며, 최종 배포 의사결정을 비즈니스 요구에 맞게 통제하는 파이프라인 아키텍처"
date = 2026-03-04

[taxonomies]
tags = ["devops_sre"]

[extra]
tags = ["devops_sre"]
+++

# 20. 지속적 전달 (CD, [Continuous Delivery](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/))

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))의 연장선으로, 테스트를 통과한 [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)([컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지)가 스테이징(Staging) 환경을 거쳐 프로덕션(Production)에 배포될 준비를 자동으로 마치는 일련의 프로세스다. 단, 최종 운영 배포는 사람의 수동 승인(Manual [Approval Gate](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/097_deployment_approval_gate_automation/))을 거친다.
> 2. **가치**: 배포 주기를 월 단위에서 주/일 단위로 단축시키며, 환경 구성과 릴리스 절차가 완벽히 스크립트화되어 있어, "클릭 한 번으로 언제든 안전하게 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)([Rollback](/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/))과 배포가 가능"한 상태를 만든다.
> 3. **융합**: [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/), [IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)([Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)), ArgoCD 같은 [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 패턴과 융합하여 인프라의 상태 편류를 막고, 블루/그린(Blue-Green) 및 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)([Canary](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)) 배포 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 결합해 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/)를 실현한다.

---

### Ⅰ. 개요 및 필요성 ([Context](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

과거 IT 업계에서는 개발(Dev)이 코드를 완성하고 나면, 이를 넘겨받은 운영(Ops) 부서가 수십 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)에 달하는 엑셀 배포 매뉴얼을 보며 새벽 내내 스크립트를 타이핑하고 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 수정해야 했다. 이러한 수동 배포(Manual [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)) 방식은 인간의 실수(Human Error)를 유발했고, 환경별 세팅 차이로 인해 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)조차 불가능한 끔찍한 주말 장애를 일으키는 근본 원인이었다.

이를 해결하기 위해 등장한 것이 지속적 전달([Continuous Delivery](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/), CD) 패러다임이다. CD는 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)([지속적 통합](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/)) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 무결점 [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)(예: [Docker Image](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/068_docker_image_immutable_package/))를 가져와, 개발망 -> 스테이징망 -> 프로덕션망에 이르기까지 일관된 방식으로 환경 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)([Config](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/))과 조합하여 릴리스 객체를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고 배포하는 과정을 100% 자동화한다. 중요한 것은 "Delivery"와 "[Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)"의 철학적 차이다. [지속적 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/)([Continuous Deployment](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/165_continuous_deployment/))는 코드 푸시부터 상용 서버 배포까지 기계가 전자동으로 처리하지만, <strong>지속적 전달(<a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/">Continuous Delivery</a>)은 프로덕션 배포 직전에 사람(비즈니스 담당자)이 '승인(Approve)' 버튼을 누를 수 있는 통제권(Gate)을 남겨둔다.</strong>

아래 도식은 수동 배포의 병목 지점과 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 기반 자동 배포의 흐름을 대조한다.

```text
이 도식은 코드 커밋 이후의 밸류 스트림(Value Stream)에서 인간 개입에 의한 병목(Waiting Time)이 어떻게 제거되는지를 보여준다.

[과거: 배포 스크립트 수동 실행 (장애 유발)]
CI(빌드 완료) --> [운영자 이메일 수신] --(주말 대기)--> [새벽 SSH 접속 및 명령어 타이핑] --> 💥 (설정 누락 장애)
                   ^ 인간 개입 (병목, 에러)

[현대: 지속적 전달 (Continuous Delivery) 파이프라인]
CI(빌드 완료) --> [Image Registry 업로드] --> [Staging 자동 배포 및 E2E 테스트]
                                                            |
                                  ✅ (테스트 통과) ---------+
                                  |
                  [Manual Approval Gate (Slack 알람/승인)] --> [Prod 무중단 배포]
                                  ^ 비즈니스적 결정만 남음
```

이 흐름의 핵심은 '배포의 기술적 준비'와 '배포의 비즈니스적 의사결정'을 분리(Decoupling)한다는 점이다. 개발과 테스트가 끝났다고 마케팅 이벤트도 안 했는데 상용에 즉시 오픈할 수는 없다. CD는 시스템이 항상 배포 가능한(Always Deployable) 상태로 대기하게 만들고, 버튼 한 번만 누르면 수 초 내에 동일한 자동화 로직으로 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/)를 보장한다.

**📢 섹션 요약 비유**: 잘 포장된 물건([아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/))을 택배 창고에 쌓아놓기만 하는 것이 아니라, 물류 시스템(CD)이 이미 고객의 문 앞(스테이징)까지 배송을 마친 상태에서, 고객이 문을 열고(수동 승인) 물건을 집어 들기만 하면 되는 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 유통 시스템과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인은 단순히 스크립트를 실행하는 것이 아니라, 무중단 상태를 유지하며 새로운 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 트래픽을 이동시키고 실패 시 이전 상태로 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/)(Resilience)시키는 복잡한 [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/)을 담당한다.

| 핵심 요소 | 역할 | 내부 동작 메커니즘 | 기술 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 예시 | 비유 |
|:---|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/">아티팩트</a> 저장소</strong> | 불변 객체 보관 | CI가 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한 [도커 이미지](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/068_docker_image_immutable_package/)와 태그, [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 저장하고 CD 도구가 이를 풀(Pull) | AWS ECR, Nexus | 창고 (진열대) |
| **매니페스트 관리** | 상태 정의 선언 | K8s의 배포 스펙(YAML)을 환경별로 오버레이(Overlay)하여 동적으로 렌더링 | [Helm](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/), [Kustomize](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/) | 인테리어 도면 |
| **CD 엔진 (Controller)** | 배포 및 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 수행 | 저장소의 목표 상태([Desired State](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/080_kube_controller_manager_desired_state/))와 클러스터의 [현재 상태](/knowledge-base/studynote/04_software_engineering/03_design_architecture/178_as_is_to_be_analysis/)(Live [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))를 일치시킴 | ArgoCD, [Spinnaker](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/093_spinnaker_multi_cloud_cd_canary_analysis/) | 현장 감리사 |
| <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/">무중단 배포</a> <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong> | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연속성 보장 | 구버전 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)를 하나씩 죽이고 신버전을 띄우거나(Rolling), [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)을 스위칭(Blue/Green)함 | [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) Deploy, [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) | 릴레이 바통 터치 |
| <strong>관측성 및 <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a></strong> | 실패 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) ([MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/)) | 배포 후 에러율(5xx)이 치솟으면 즉각적으로 이전 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 해시로 트래픽을 되돌림 | [Prometheus](/knowledge-base/studynote/15_devops_sre/03_sre_observability/136_prometheus/), Kayenta | 타임머신 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 버튼 |

아래의 계층 구조도는 최근 CD 아키텍처의 사실상 표준(De facto)으로 자리 잡은 <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/088_pull_based_deployment_gitops_argocd_security_auto_healing/">풀 기반</a>(<a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/088_pull_based_deployment_gitops_argocd_security_auto_healing/">Pull-based</a>) <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a> 아키텍처</strong>의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 보여준다.

```text
이 도식은 외부 파이프라인(Jenkins)이 클러스터에 직접 푸시하지 않고, 클러스터 내부의 에이전트(ArgoCD)가 Git의 매니페스트 변화를 스스로 감지하여 동기화하는 가장 안전한 CD 구조를 나타낸다.

+------- CI Pipeline --------+            +------- Git Repository --------+
| 1. 코드 빌드/테스트        |            | [ Manifest Repo (YAML) ]      |
| 2. Docker Image Push       | --(Update) | image: myapp:v2.0 (태그 수정) |
| 3. 매니페스트 Git Repo 수정|            +-------+-----------------------+
+----------------------------+                    | (3) Pull & Sync
                                                  v
                                 +-------- K8s Cluster (Prod) ----------+
  (외부망에서 내부망으로의       |  +-- CD Controller (ArgoCD) ------+  |
   방화벽 오픈 불필요 - 보안성)  |  | 1. Git과 Cluster 상태 차이 감지|  |
                                 |  | 2. K8s API 서버에 v2.0 배포 지시| |
                                 |  +-------------+------------------+  |
                                 |                v                     |
                                 |      [ Web App Pods (v2.0) ]         |
                                 +--------------------------------------+
```

이 구조의 핵심은 단일 진실 공급원([Single Source of Truth](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/))을 오직 Git으로 한정하는 것이다. 전통적인 푸시(Push) 방식에서는 해커가 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 서버를 탈취하면 [젠킨스](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)에 저장된 클러스터 접속 키(Kubeconfig)를 이용해 전체 운영망을 날려버릴 수 있었다. 반면 풀(Pull) 기반 [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 방식에서는 클러스터 내부의 에이전트만 Git을 읽기 모드로 당겨오므로(Pull), 크리덴셜([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 정보)이 클러스터 밖으로 절대 유출되지 않아 [제로 트러스트 보안](/knowledge-base/studynote/03_network/14_network_security_threats/738_zero_trust_architecture_least_privilege/) 원칙을 완벽히 준수한다.

코드 수준(YAML)에서 살펴보면 배포의 [멱등성](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/171_idempotency_iac_terraform/)이 어떻게 보장되는지 알 수 있다.
```yaml
# [실무 코드 스니펫] Kustomize를 활용한 스테이징/운영 환경 패리티 유지
# base/deployment.yaml (공통 로직)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: app
        image: mycompany/myapp:latest # (태그는 CD 도구가 덮어씀)

# overlays/prod/kustomization.yaml (운영 전용 설정 덮어쓰기)
resources:
  - ../../base
replicas:
  - name: myapp
    count: 10 # 운영은 파드 10개
images:
  - name: mycompany/myapp
    newTag: v2.0.45 # CI가 자동 업데이트한 해시값
```

**📢 섹션 요약 비유**: 집안의 에어컨 온도를 바꾸기 위해 외부 보일러실 기사([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 서버)가 집 안으로 직접 들어와 벽을 뜯는 것(Push)이 아니라, 내가 스마트폰(Git)에 '22도'라고 희망 온도를 입력해 두면 집 안의 스마트 온도조절기(ArgoCD)가 알아서 목표 온도에 맞게 내부 기기를 세팅(Pull)하는 것과 같습니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

CD 영역에서는 딜리버리(Delivery)와 [디플로이먼트](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/)([Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/))의 철학적 차이, 그리고 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 간의 트레이드오프 분석이 가장 중요하다.

| 항목 | 지속적 전달 ([Continuous Delivery](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/)) | [지속적 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/) ([Continuous Deployment](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/165_continuous_deployment/)) |
|:---|:---|:---|
| **프로세스 종착점** | 스테이징 배포 완료 + **운영 배포 전 수동 대기** | 소스 푸시부터 **운영 배포까지 전자동 (No Gate)** |
| **의사결정 주체** | 비즈니스 팀 (PM, 마케팅)의 승인(Approve) | 기계 (모든 자동화 테스트 통과 시 무조건 릴리스) |
| **주요 적용 기업** | 90% 이상의 일반적인 엔터프라이즈, 금융권 | 넷플릭스, 아마존 등 극단적 [애자일](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 빅테크 |
| **안전망 요구사항** | [E2E](/knowledge-base/studynote/15_devops_sre/05_devsecops/265_e2e_end_to_ui_selenium/) 테스트 및 배포 전 승인 워크플로우 | [카나리 분석기](/knowledge-base/studynote/15_devops_sre/05_devsecops/268_canary_analysis_cpu_spinnaker_kayenta/)(통계 기반 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)), A/B 테스팅 고도화 |

대다수의 기업은 지속적 '전달'을 사용한다. 아무리 테스트를 꼼꼼히 해도, 크리스마스 이벤트 쿠폰 기능을 일주일 전에 미리 병합(Merge)해두었다면 당일 00시에 사람의 통제 하에 오픈해야 하기 때문이다.

아래 다이어그램은 [무중단 배포](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/)([Zero-Downtime](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/110_zero_downtime_db_schema_rollout/) [Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/))를 위한 세 가지 핵심 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)의 트레이드오프를 비교한다.

```text
+----------+-----------------------+-------------------------+----------------------+
| 배포 전략| 롤링 (Rolling Update) | 블루/그린 (Blue/Green)  | 카나리 (Canary)      |
+----------+-----------------------+-------------------------+----------------------+
| 라우팅   | 1대씩 순차 교체       | 전면 스위칭 (100% 이동) | 1% -> 10% 점진 확대  |
| 롤백 속도| 매우 느림             | 1초 (즉시 라우팅 원복)  | 1초 (에러 감지 자동) |
| 자원 요구| 110% (여유분만 필요)  | 200% (동일 환경 2벌 필요)| 110%                 |
| 단점     | 구/신버전 혼재로 DB   | 클라우드 비용(Cost) 2배 | 복잡한 모니터링 메트릭|
|          | 하위호환성 필수       | 일시적 낭비 발생        | 임계치 튜닝 필요     |
+----------+-----------------------+-------------------------+----------------------+
```

이 매트릭스에서 알 수 있듯, 비용과 안전성은 정비례하지 않는다. 최근 대규모 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서는 하드웨어를 2배로 유지해야 하는 블루/그린의 재무적 압박([FinOps](/knowledge-base/studynote/12_it_management/05_security_compliance/344_finops/) 이슈)을 피하기 위해, [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/) 같은 [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/)([Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/))를 활용하여 트래픽의 단 1%만 신버전으로 흘려보내고 에러율 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)(5xx)을 실시간 관측하여 이상이 없으면 100%로 점진 오픈하는 <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/">카나리 배포</a>(<a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/195_canary_release_deployment/">Canary Release</a>)</strong>가 SRE의 가장 이상적인 표준으로 자리매김했다.

**📢 섹션 요약 비유**: 낡은 다리를 새 다리로 바꿀 때, 기존 다리 옆에 새 다리를 완벽히 지어놓고 바리케이드를 한 번에 옮기면(블루/그린, 비싸지만 안전), 차선을 하나씩만 옮겨 차를 통과시키며 무너지는지 관찰하는 것([카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/), 저렴하고 스마트)의 차이와 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 CD를 적용할 때 시스템 장애를 막고 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)력을 높이기 위해 SRE가 내려야 할 판단 시나리오는 다음과 같다.

1. <strong>배포 직후 <a href="/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/">메모리 누수</a>(<a href="/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/">Memory Leak</a>) 장애 발생</strong>
   - **상황**: 금요일 오후, [롤링 배포](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/193_rolling_update_deployment_kubernetes/)가 정상 완료되었으나 30분 뒤 신버전 [파드](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)들이 순차적으로 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)([Out of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 킬러에 의해 죽으며 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 중단됨.
   - **판단**: 배포 직후 장애 발생 시 "원인 파악(디버깅) 후 수정 코드를 다시 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 태워 재배포(Roll-[forward](/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/))"하는 것은 절대 금지 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)이다. 다운타임을 최소화([MTTR](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/) 1분 이내)하기 위해 즉시 CD 도구(ArgoCD)의 <strong><a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a>(<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/313_rollback/">Rollback</a>)</strong> 버튼을 눌러 이전 해시(Hash) [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 트래픽을 원상복구시킨 후, 격리된 스테이징망에서 천천히 [메모리 누수](/knowledge-base/studynote/02_operating_system/10_security/612_memory_leak_detection/) 원인을 디버깅해야 한다.

2. <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/">카나리</a>(<a href="/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/">Canary</a>) 배포 시 DB <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a> 락(<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/">Lock</a>) 문제</strong>
   - **상황**: 트래픽의 5%만 신버전으로 보내는 [카나리 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/)를 수행했는데, 신버전이 DB [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)의 특정 컬럼을 지워버려(Drop) 구버전(95%)의 트래픽이 몽땅 DB 에러를 뱉음.
   - **판단**: [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)나 [롤링 배포](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/193_rolling_update_deployment_kubernetes/)는 "필연적으로 구버전 코드와 신버전 코드가 동일한 DB를 동시에 바라보는 구간"이 존재한다. 따라서 CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 [데이터베이스 마이그레이션](/knowledge-base/studynote/15_devops_sre/05_devsecops/271_ddl_liquibase/)은 철저히 <strong>확장 후 수축(Expand and Contract) 패턴</strong>을 통해 하위 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 보장하도록 강제해야 한다. 컬럼 삭제는 이번 배포가 아닌 다음번 릴리스(계약 축소)에서 이루어져야 한다.

다음은 배포 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)을 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)할지 결정하는 SRE의 실무 운영 [의사결정 트리](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/)이다.

```text
이 도식은 배포 후 카나리 분석기(Spinnaker Kayenta 등)가 실시간 메트릭을 평가하여 배포를 승격(Promote)시킬지 롤백할지 자동 판단하는 흐름이다.

[ CD Pipeline: 카나리 파드 생성 (트래픽 5% 할당) ]
   |
   +- [5분간 관측 (Prometheus Metics)]
   |       v
   +- Q1. HTTP 5xx 에러율이 이전 버전(Baseline) 대비 증가했는가?
   |   +- Yes --> ❌ 카나리 파괴 및 자동 롤백 (안전망 가동)
   |   +- No ---> v
   |
   +- Q2. P99 Latency(응답 지연 시간)가 임계치(예: 500ms)를 초과했는가?
   |   +- Yes --> ❌ 메모리 병목 의심, 자동 롤백 및 슬랙 경보
   |   +- No ---> v
   |
   +- ✅ 통계적 검증 통과 (Confidence Score 95%+)
          v
   [ 트래픽 100% 점진 전환 및 구버전 파드 삭제 (Success) ]
```

이러한 자동화된 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 분석(Automated [Canary Analysis](/knowledge-base/studynote/15_devops_sre/05_devsecops/268_canary_analysis_cpu_spinnaker_kayenta/))은 CD의 궁극적 지향점이다. 사람이 대시보드를 뚫어져라 쳐다보며 식은땀을 흘리는 것이 아니라, [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)을 비교 채점하여 장애 반경(Blast [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/))이 전체 고객의 5% 미만일 때 선제적으로 폭발을 차단하고 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)하는 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/) [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/)([Resiliency](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/))을 시스템에 부여한다.

**📢 섹션 요약 비유**: 신제품 화장품을 전국 1,000개 매장에 동시에 풀기 전에, 강남점([카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/) 매장) 한 곳에만 먼저 진열해보고 고객 [클레임](/knowledge-base/studynote/09_security/11_iam_access_control/539_claims/)(에러 [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/))이 단 1건이라도 들어오면 즉각 회수하여 브랜드 이미지 타격을 막는 똑똑한 출시 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과 같습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

조직이 고도화된 지속적 전달(CD) [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인과 [GitOps](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 체계를 갖추게 되면, 소프트웨어 개발 생태계는 완전히 다른 차원의 속도와 안정성을 확보하게 된다.

| 가치 영역 | 기존 시스템 (수동 배포) | CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 정착 후 | 비즈니스 파급력 |
|:---|:---|:---|:---|
| <strong>배포 빈도 (<a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/">Deployment</a> Frequency)</strong> | 분기별 / 월별 1회 (빅뱅) | 주별 / 일별 수십 회 (Micro) | 고객 피드백에 즉각 대응하는 시장 경쟁력(TTM) 우위 |
| <strong>변경 실패율 (<a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/025_change_failure_rate_cfr/">Change Failure Rate</a>)</strong> | 30% 이상 (인적 오류 빈번) | 1% 미만 ([검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인) | 운영팀 밤샘 작업([Toil](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/685_toil_automation_sre/)) 소멸, 엔지니어 이직률 감소 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/">재해 복구</a> 시간 (<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/451_mttr/">MTTR</a>)</strong> | 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)에 수 시간 소요 | 클릭 한 번으로 1분 내 [롤백](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 완료 | 대고객 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)([가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) 준수 및 금전적 손실 방어 |

앞으로의 CD 표준은 [멀티 클라우드](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/)([Multi-Cloud](/knowledge-base/studynote/12_it_management/05_security_compliance/202_multi_cloud_hybrid_cloud_governance/)) 배포 및 [엣지 컴퓨팅](/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)([Edge Computing](/knowledge-base/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/)) 연계로 확장될 것이다. KubeVela, ArgoCD 등은 단일 클러스터를 넘어 전 세계에 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 수천 개의 노드에 동일한 상태를 파동처럼 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)하는 도구로 진화 중이다. 또한, 내부 개발자 포털([IDP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/), Backstage 등)과 결합하여 개발자가 인프라 지식 없이도 UI 클릭 한 번으로 K8s 환경부터 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인, [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링까지 골든 패스(Golden Path)를 셀프 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 [프로비저닝](/knowledge-base/studynote/09_security/11_iam_access_control/528_provisioning/)하는 <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/">플랫폼 엔지니어링</a>(<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/109_platform_engineering_cognitive_load/">Platform 엔진ering</a>)</strong> 사상으로 완벽히 융합될 것이다.

**📢 섹션 요약 비유**: 과거에는 배를 띄우기 위해 수백 명의 노잡이가 땀을 흘려야 했다면, 이제는 완벽히 프로그래밍된 자동항법장치(CD)를 통해 선장(비즈니스)이 목적지만 누르면 거친 풍랑(장애) 속에서도 알아서 궤도를 수정하며 부드럽게 항해하는 자율 운항 시대가 열린 것입니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- <strong><a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a> (<a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/">Continuous Integration</a>)</strong> (CD의 선행 조건으로, 지속적인 빌드와 자동화 테스트를 통해 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)를 만들어내는 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인)
- <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a> (ArgoCD / Flux)</strong> (모든 클러스터 상태를 선언적 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 Git에 저장하고, 에이전트가 이를 Pull하여 무중단 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)를 보장하는 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) CD 표준)
- <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/201_dora_metrics_devops_performance/">DORA Metrics</a></strong> (구글이 제시한 고성과 [데브옵스](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 조직의 4대 지표: 배포 빈도, 변경 [리드 타임](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/085_lead_time_cycle_time/), 변경 실패율, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간. CD가 직접적으로 개선하는 수치)
- <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/576_feature_flag_ab_testing_rollout/">Feature Flag</a> (<a href="/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/">피처</a> 토글)</strong> (CD [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 타서 코드는 운영에 배포되었으나, 비즈니스 요건에 맞춰 실제 UI 노출 여부를 런타임 변수로 켜고 끄는 기술)
- <strong><a href="/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/195_canary_release_deployment/">Canary Release</a> (<a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/115_canary_deployment_gradual_rollout/">카나리 배포</a>)</strong> (광산의 [카나리](/knowledge-base/studynote/02_operating_system/10_security/595_canary_stack_smashing_protector/)아 새처럼, 소수의 트래픽만 신버전에 노출시켜 에러를 관측한 후 점진적으로 전체를 배포하는 가장 진보된 무중단 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))

### 📈 관련 키워드 및 발전 흐름도

```text
[CI (Continuous Integration) — 자동 빌드·테스트·아티팩트 생성]
    |
    v
[CD (Continuous Delivery) — 배포 가능 상태 유지, 수동 최종 승인]
    |
    v
[CD (Continuous Deployment) — 승인 없이 운영 자동 배포]
    |
    v
[GitOps (ArgoCD / Flux) — Git을 단일 진실 원천으로 선언적 클러스터 동기화]
    |
    v
[DORA Metrics — 배포 빈도·변경 리드 타임·실패율·복구 시간으로 성과 측정]
```
CI로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 [아티팩트](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)를 CD(Delivery/[Deployment](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/))로 자동화하고, GitOps로 선언적 관리를 구현한 뒤 [DORA](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/523_dhcp_dora_process/) Metrics로 조직의 배포 역량을 측정한다.

### 👶 어린이를 위한 3줄 비유 설명
1. 공장에서 장난감(앱 코드)을 잘 만들었는지 꼼꼼히 검사하는 과정이 CI라면, 그 장난감을 트럭에 싣고 마트 진열대 앞까지 가져다 놓는 과정이 CD예요.
2. 예전에는 아저씨들이 상자를 하나하나 직접 뜯어서 힘들게 진열하느라(수동 배포) 장난감이 부서지는 사고가 많았어요.
3. 하지만 지금은 CD라는 똑똑한 로봇 트럭이 가게 진열대에 장난감을 마술처럼 짠! 하고 예쁘게 교체해 주어서(자동화 릴리스), 아이들이 언제나 새 장난감을 안전하게 가지고 놀 수 있게 되었답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 20 / 373

<- **이전**: [19. 지속적 통합 (CI, Continuous Integration) - 다수 개발자의 코드를 메인 브랜치에 수시로 병합하고 자동 빌드/테스트를](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/)
**다음**: [21. 지속적 배포 (CD, Continuous Deployment) - 수동 승인조차 생략하고 테스트를 통과한 모든 코드를 프로덕션](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/021_continuous_deployment_cd/) ->

---
