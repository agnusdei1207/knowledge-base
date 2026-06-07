---
title: "Gitops"
date: "2026-03-04"
tags:
  - "cloud_architecture"
  - "studynote-cloud-architecture"
weight: 167
---
## 핵심 인사이트 (3줄 요약)
- **Git이 단일 진실 공급원(SSOT):** 인프라와 애플리케이션의 원하는 상태([Desired State](/studynote/13_cloud_architecture/02_iaas_paas_saas/080_kube_controller_manager_desired_state/))를 Git에 선언적으로 정의하고, 모든 변경은 Git을 통해서만 수행한다.
- <strong>자동화된 <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a>(Reconciliation):</strong> 클러스터 내부의 에이전트가 Git의 상태와 실제 운영 환경의 상태를 지속적으로 비교하여 차이가 발생하면 자동으로 일치시킨다.
- **운영 안정성 및 보안 강화:** 모든 변경 이력이 Git [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 남으므로 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)이 즉각적이며, 사용자가 직접 인프라에 접속할 필요가 없어 보안 사고 리스크가 줄어든다.

### Ⅰ. 개요 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Background)
깃옵스([GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/))는 위브웍스(Weaveworks)가 2017년 제안한 개념으로, [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경(특히 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/))에서 인프라와 배포를 관리하는 최신 방식이다. DevOps의 핵심 원칙인 '자동화'와 '선언적 인프라([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/))'를 Git 워크플로우와 결합하여 배포의 민첩성과 운영의 안정성을 동시에 확보한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
GitOps는 푸시(Push) 기반의 기존 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD와 달리 풀(Pull) 기반의 상태 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 메커니즘을 지향한다.

```text
[ Architecture of GitOps Pipeline ]

    (Developer)         (Git Repository)           (GitOps Agent)
      +-----+             +-------------+          +--------------+
      | Code|--- Push --->| Manifests   |<-- Poll--| ArgoCD / Flux|
      +-----+             | (YAML, Helm)|          +--------------+
                                |                         |
                                |                         v
                                |                 +---------------+
                                +--- Reconcile -->| Kubernetes    |
                                                  | Cluster       |
                                                  +---------------+
                                                  (Actual State)

1. Git Manifests: 쿠버네티스 객체 선언문 (Desired State)
2. Poll & Diff: Git의 최신 커밋과 클러스터 실시간 상태 비교
3. Sync & Deploy: 차이점 발견 시 클러스터에 배포/수정 적용
```

**핵심 메커니즘:**
1. **선언적 정의:** 시스템의 전체 상태를 선언적 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(YAML, [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 등)로 기술한다.
2. <strong><a href="/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/">버전</a> 관리:</strong> 모든 선언문은 Git에서 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리되며 Immutable한 기록으로 남는다.
3. **지속적 감시:** 에이전트(ArgoCD 등)가 Git과 클러스터 사이의 차이(Drift)를 감시한다.
4. **셀프 힐링:** 누군가 수동으로 클러스터 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 변경하면 에이전트가 이를 감지하고 Git의 상태로 강제 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전통적 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD (Push 기반) | [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) (Pull 기반) |
| :--- | :--- | :--- |
| **작동 원리** | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 툴에서 클러스터로 직접 명령 실행 | 클러스터 내 에이전트가 Git을 감시하여 가져옴 |
| **보안** | [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/) 툴에 클러스터 접근 권한(Kubeconfig) 필요 | 클러스터 밖으로 권한을 노출하지 않음 |
| <strong>장애 <a href="/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/">복구</a></strong> | 수동 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 또는 재실행 필요 | Git 이전 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 Revert 시 자동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| **가시성** | 배포 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 중심 | 현재 운영 상태(Sync status) 중심 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) |

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)
**실무 적용 사례:**
- **ArgoCD 활용:** Git 저장소의 YAML 변경 시 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)([Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/))를 자동 롤링 업데이트하고, 대시보드를 통해 싱크 상태를 관리한다.
- **다중 클러스터 관리:** 동일한 Git Manifest를 여러 클러스터에 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)하여 환경 일치성을 보장한다.

**기술사적 판단:**
"GitOps는 단순히 도구의 문제가 아니라 <strong>운영 철학의 전환</strong>이다. '구성은 코드로, 운영은 Git으로'라는 사상을 통해 [구성 편류](/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/)([Configuration Drift](/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/)) 문제를 원천 차단하며, 대규모 클라우드 환경에서 규정 준수([Compliance](/studynote/07_enterprise_systems/01_strategy_governance/058_it_compliance_sox_basel_gdpr_isms/))를 증명하는 강력한 수단이 된다."

### Ⅴ. 기대효과 및 결론 (Future & Standard)
GitOps는 개발자의 운영 개입을 최소화하고 소프트웨어 [공급망](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/)([Supply Chain](/studynote/04_software_engineering/08_security_compliance_devsecops/520_supply_chain_attack_and_ci_cd_security/))의 보안을 강화한다. 최근에는 인프라를 넘어 [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/) [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/), [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/)([OPA](/studynote/15_devops_sre/05_devsecops/237_opa_open_policy_agent_gatekeeper/)) 등 시스템 전 영역으로 [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 사상이 확장되고 있다.

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a> (<a href="/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/">Infrastructure as Code</a>):</strong> [테라폼](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/), [앤서블](/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/) (GitOps의 기반)
- <strong><a href="/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/">Immutable Infrastructure</a>:</strong> [불변 인프라](/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/) (수정 대신 교체)
- <strong>Drift <a href="/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/">Detection</a>:</strong> [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 이탈 감지 및 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)

### 👶 어린이를 위한 3줄 비유 설명
1. 깃옵스는 요리책(Git)에 '피자 1판 만들기'라고 써두면, 로봇 요리사(에이전트)가 그걸 보고 똑같이 만드는 거예요.

### 📈 관련 키워드 및 발전 흐름도

```text
수동 kubectl apply (명령형 배포)
    |
    v
GitOps: Git = Single Source of Truth
    +-► Pull 방식: ArgoCD · Flux (클러스터가 Git 감시)
    +-► Push 방식: Jenkins (CI가 클러스터에 배포)
    |
    v
Progressive Delivery: Argo Rollouts · Flagger
```
2. 만약 누군가 몰래 피자 조각을 훔쳐 가면, 로봇이 요리책과 다르다는 걸 알고 다시 피자를 채워 넣는답니다.
3. 요리책 내용만 잘 적어두면 언제든 똑같은 피자를 맛볼 수 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 166 / 371

<- **이전**: [166. CI/CD 파이프라인 도구 (Jenkins, GitLab CI, GitHub Actions)](/studynote/13_cloud_architecture/04_devops_observability/166_cicd_pipeline_tools/)
**다음**: [168. 푸시 vs 풀 기반 배포 (GitOps Push vs Pull Deployment)](/studynote/13_cloud_architecture/04_devops_observability/168_gitops_push_vs_pull_deployment/) ->

---
