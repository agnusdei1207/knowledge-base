+++
weight = 167
title = "167. 깃옵스 (GitOps) - 선언적 인프라 및 애플리케이션의 상태 동기화 패러다임"
date = "2026-03-04"
[taxonomies]
tags = ["GitOps", "ArgoCD", "Declarative", "CI/CD", "Kubernetes"]
categories = ["13_cloud_architecture"]
+++

## 핵심 인사이트 (3줄 요약)
- **Git이 단일 진실 공급원(SSOT):** 인프라와 애플리케이션의 원하는 상태([[080_kube_controller_manager_desired_state|Desired State]])를 Git에 선언적으로 정의하고, 모든 변경은 Git을 통해서만 수행한다.
- **자동화된 [[212_synchronization_mechanisms|동기화]](Reconciliation):** 클러스터 내부의 에이전트가 Git의 상태와 실제 운영 환경의 상태를 지속적으로 비교하여 차이가 발생하면 자동으로 일치시킨다.
- **운영 안정성 및 보안 강화:** 모든 변경 이력이 Git [[568_logs_distributed_logging_elk_fluentd|로그]]에 남으므로 [[098_rollback_strategy_pipeline_error_threshold|롤백]]이 즉각적이며, 사용자가 직접 인프라에 접속할 필요가 없어 보안 사고 리스크가 줄어든다.

### Ⅰ. 개요 ([[033_context|Context]] & Background)
깃옵스([[119_gitops_single_source_of_truth|GitOps]])는 위브웍스(Weaveworks)가 2017년 제안한 개념으로, [[531_cloud_native_architecture|클라우드 네이티브]] 환경(특히 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]])에서 인프라와 배포를 관리하는 최신 방식이다. DevOps의 핵심 원칙인 '자동화'와 '선언적 인프라([[793_iac_idempotency_template|IaC]])'를 Git 워크플로우와 결합하여 배포의 민첩성과 운영의 안정성을 동시에 확보한다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
GitOps는 푸시(Push) 기반의 기존 [[090_configuration_item|CI]]/CD와 달리 풀(Pull) 기반의 상태 [[212_synchronization_mechanisms|동기화]] 메커니즘을 지향한다.

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
1. **선언적 정의:** 시스템의 전체 상태를 선언적 [[501_file_definition_logical_record|파일]](YAML, [[343_json|JSON]] 등)로 기술한다.
2. **[[288_version_ihl_tos_total_length|버전]] 관리:** 모든 선언문은 Git에서 [[288_version_ihl_tos_total_length|버전]] 관리되며 Immutable한 기록으로 남는다.
3. **지속적 감시:** 에이전트(ArgoCD 등)가 Git과 클러스터 사이의 차이(Drift)를 감시한다.
4. **셀프 힐링:** 누군가 수동으로 클러스터 [[009_config|설정]]을 변경하면 에이전트가 이를 감지하고 Git의 상태로 강제 [[658_ir_recovery|복구]]한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전통적 [[090_configuration_item|CI]]/CD (Push 기반) | [[119_gitops_single_source_of_truth|GitOps]] (Pull 기반) |
| :--- | :--- | :--- |
| **작동 원리** | [[090_configuration_item|CI]] 툴에서 클러스터로 직접 명령 실행 | 클러스터 내 에이전트가 Git을 감시하여 가져옴 |
| **보안** | [[090_configuration_item|CI]] 툴에 클러스터 접근 권한(Kubeconfig) 필요 | 클러스터 밖으로 권한을 노출하지 않음 |
| **장애 [[658_ir_recovery|복구]]** | 수동 [[098_rollback_strategy_pipeline_error_threshold|롤백]] 또는 재실행 필요 | Git 이전 [[288_version_ihl_tos_total_length|버전]]으로 Revert 시 자동 [[658_ir_recovery|복구]] |
| **가시성** | 배포 [[568_logs_distributed_logging_elk_fluentd|로그]] 중심 | 현재 운영 상태(Sync status) 중심 [[003_bigdata_7v|시각화]] |

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)
**실무 적용 사례:**
- **ArgoCD 활용:** Git 저장소의 YAML 변경 시 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] [[085_pod_kubernetes_container_unit|파드]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])를 자동 롤링 업데이트하고, 대시보드를 통해 싱크 상태를 관리한다.
- **다중 클러스터 관리:** 동일한 Git Manifest를 여러 클러스터에 [[212_synchronization_mechanisms|동기화]]하여 환경 일치성을 보장한다.

**기술사적 판단:**
"GitOps는 단순히 도구의 문제가 아니라 **운영 철학의 전환**이다. '구성은 코드로, 운영은 Git으로'라는 사상을 통해 [[193_configuration_drift|구성 편류]]([[193_configuration_drift|Configuration Drift]]) 문제를 원천 차단하며, 대규모 클라우드 환경에서 규정 준수([[058_it_compliance_sox_basel_gdpr_isms|Compliance]])를 증명하는 강력한 수단이 된다."

### Ⅴ. 기대효과 및 결론 (Future & Standard)
GitOps는 개발자의 운영 개입을 최소화하고 소프트웨어 [[520_supply_chain_attack_and_ci_cd_security|공급망]]([[520_supply_chain_attack_and_ci_cd_security|Supply Chain]])의 보안을 강화한다. 최근에는 인프라를 넘어 [[002_database_definition|데이터베이스]] [[005_schema|스키마]], [[007_security_policy|보안 정책]]([[237_opa_open_policy_agent_gatekeeper|OPA]]) 등 시스템 전 영역으로 [[119_gitops_single_source_of_truth|GitOps]] 사상이 확장되고 있다.

### 📌 관련 개념 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **[[793_iac_idempotency_template|IaC]] ([[062_infrastructure_as_code|Infrastructure as Code]]):** [[195_terraform_hashicorp_agnostic_aws_gcp|테라폼]], [[198_ansible_os_configuration_management_ssh|앤서블]] (GitOps의 기반)
- **[[204_immutable_infrastructure_configuration_drift_prevention|Immutable Infrastructure]]:** [[204_immutable_infrastructure_configuration_drift_prevention|불변 인프라]] (수정 대신 교체)
- **Drift [[961_deepfake_detection|Detection]]:** [[009_config|설정]] 이탈 감지 및 [[658_ir_recovery|복구]]

### 👶 어린이를 위한 3줄 비유 설명
1. 깃옵스는 요리책(Git)에 '피자 1판 만들기'라고 써두면, 로봇 요리사(에이전트)가 그걸 보고 똑같이 만드는 거예요.

### 📈 관련 키워드 및 발전 흐름도

```text
수동 kubectl apply (명령형 배포)
    │
    ▼
GitOps: Git = Single Source of Truth
    ├─► Pull 방식: ArgoCD · Flux (클러스터가 Git 감시)
    └─► Push 방식: Jenkins (CI가 클러스터에 배포)
    │
    ▼
Progressive Delivery: Argo Rollouts · Flagger
```
2. 만약 누군가 몰래 피자 조각을 훔쳐 가면, 로봇이 요리책과 다르다는 걸 알고 다시 피자를 채워 넣는답니다.
3. 요리책 내용만 잘 적어두면 언제든 똑같은 피자를 맛볼 수 있어요!
