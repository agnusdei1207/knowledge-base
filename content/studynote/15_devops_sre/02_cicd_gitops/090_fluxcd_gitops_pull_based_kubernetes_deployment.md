---
title: "090. Fluxcd Gitops Pull Based Kubernetes Deployment"
date: "2026-04-10"
tags:
  - "studynote-devops"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: FluxCD는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)(K8s) 클러스터 내부에서 동작하며, Git 저장소의 매니페스트(YAML) 상태를 읽어와 클러스터에 강제로 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)([Pull-based](/studynote/15_devops_sre/02_cicd_gitops/088_pull_based_deployment_gitops_argocd_security_auto_healing/) Sync)하는 [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 기반 [지속적 배포](/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/)(CD) 에이전트다.
> 2. **가치**: 모놀리식 구조인 ArgoCD와 달리, 독립된 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)(Controller)들로 구성된 '[GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) Toolkit' 아키텍처를 채택하여 리소스 소비가 극도로 적고 [멀티 테넌시](/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/)([Multi-tenancy](/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/)) 환경에 유리하다.
> 3. **판단 포인트**: 시각적인 대시보드가 중요한 대규모 개발 조직에는 ArgoCD가 적합하지만, CLI(명령줄) 친화적이고 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 네이티브(CRD) 방식의 강력한 확장성과 자동화를 원한다면 FluxCD가 최적의 선택이다.

---

### Ⅰ. 개요 및 필요성
기존의 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인(Push 기반)은 [젠킨스](/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)([Jenkins](/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)) 같은 외부 서버가 K8s 클러스터의 관리자 권한을 탈취해 밖에서 명령을 밀어넣는 구조였다. 이는 보안 취약점과 클러스터 상태 불일치(Drift) 문제를 야기했다.

이를 해결하기 위해 Weaveworks가 창안한 [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 철학에 따라, 클러스터 내부에서 Git 저장소를 쳐다보고 있다가 변경사항을 스스로 당겨와(Pull) 배포하는 FluxCD가 탄생했다. FluxCD는 Git을 시스템의 유일한 진실의 원천(SSOT, [Single Source of Truth](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/))으로 만들어, 인프라의 [버저닝](/studynote/05_database/05_distributed_nosql_newsql/317_versioning_data_model_design/)([Versioning](/studynote/05_database/05_distributed_nosql_newsql/317_versioning_data_model_design/))과 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([Audit](/studynote/12_it_management/05_security_compliance/363_audit/)), 그리고 즉각적인 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)을 가능하게 한다.

- **📢 섹션 요약 비유**: 외부에서 성문을 부수고 짐을 밀어 넣는 것(Push 방식)이 아니라, 성 안의 똑똑한 파수꾼(FluxCD)이 정해진 우체통(Git)만 감시하다가 편지가 오면 스스로 성 안의 배치도를 바꾸는(Pull 방식) 철통 보안 시스템이다.

---

### Ⅱ. 아키텍처 및 핵심 원리
[초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) Flux v1은 단일 덩어리였으나, Flux v2부터는 <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a> Toolkit</strong>이라는 5개의 초경량 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)(Controller) 연합체로 재설계되었다. 모든 동작은 철저히 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 순정 CRD(Custom Resource Definition)를 통해 제어된다.

| 핵심 컨트롤러 | 역할 (동작 원리) |
| :--- | :--- |
| **Source Controller** | Git, [Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/), [OCI](/studynote/13_cloud_architecture/05_data_engineering/333_process/) 저장소를 주기적으로 [폴링](/studynote/02_operating_system/08_storage_and_io_systems/448_polling_programmed_io/)하여 [아티팩트](/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)([압축](/studynote/02_operating_system/06_memory_management/347_compaction/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))로 캡처 |
| <strong><a href="/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/">Kustomize</a> Controller</strong> | 캡처된 [아티팩트](/studynote/15_devops_sre/02_cicd_gitops/075_artifact_management_nexus_docker_registry/)를 기반으로 [Kustomize](/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/) 빌드를 수행하고 클러스터에 배포(Apply) |
| <strong><a href="/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/">Helm</a> Controller</strong> | [Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/) 차트를 렌더링하고 릴리스의 수명주기를 선언적으로 관리 |
| **Notification Controller** | 배포 성공/실패 이벤트를 Slack, Teams 등으로 전송 |
| **Image Automation Controller** | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 저장소의 새 이미지를 감지하고 Git 저장소의 YAML을 스스로 자동 커밋 |

```text
+--------------------------------------------------------------+
|             FluxCD의 GitOps Toolkit 동작 아키텍처             |
+--------------------------------------------------------------+
| [Git Repository] <---(감시)-- [Source Controller]            |
|       ^                            | (Artifact 생성)         |
|       | 자동 커밋                    v                       |
|       |                 [Kustomize/Helm Controller]          |
| [Image Automation]                 | (Sync & Apply)          |
|       | 감시                       v                       |
| [Docker Registry]         [Kubernetes Cluster]               |
+--------------------------------------------------------------+
```

이 구조의 핵심은 봇들이 철저히 분업화되어 있다는 점이다. 이미지가 새로 등록되면 Image Automation 봇이 Git을 업데이트하고, Source 봇이 이를 퍼오면, [Kustomize](/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/) 봇이 배포를 실행하는 톱니바퀴 같은 자동화가 이루어진다.

- **📢 섹션 요약 비유**: FluxCD는 만능 로봇 한 대가 아니라, 재료를 가져오는 봇, 요리를 하는 봇, 메뉴판을 고치는 봇으로 철저히 나뉜 초경량 마이크로 요리사 팀과 같다. 각자 맡은 일만 하므로 자원을 아주 적게 먹는다.

---

### Ⅲ. 비교 및 연결
[GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 생태계의 영원한 라이벌인 ArgoCD와 비교할 때 그 철학의 차이가 명확하게 드러난다.

| 비교 항목 | FluxCD | ArgoCD |
| :--- | :--- | :--- |
| **아키텍처 구조** | [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) ([분산](/studynote/08_algorithm_stats/08_stats/136_variance/)형) | 모놀리식 (통합형) |
| **UI 및 조작** | CLI 중심 (기본 UI 없음) | 강력하고 직관적인 웹 대시보드 |
| <strong><a href="/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/">멀티 테넌시</a></strong> | 가벼워서 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)별 개별 배포 용이 | 하나의 중앙 서버에서 권한 분리([RBAC](/studynote/09_security/11_iam_access_control/569_rbac/)) 관리 |
| **리소스 사용량** | CPU/RAM 소비 극도로 적음 | 상대적으로 무거움 |
| <strong>K8s <a href="/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/">결합도</a></strong> | 뼛속까지 K8s CRD 중심 | 자체적인 AppProject 등 독자 개념 혼용 |

Flux는 [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/)보다 터미널 조작과 자동화 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 연계에 집중하며, K8s의 선언적([Declarative](/studynote/15_devops_sre/05_devsecops/219_declarative_yaml/)) 철학을 가장 순수하게 구현한다.

- **📢 섹션 요약 비유**: ArgoCD는 화려한 계기판과 자동 변속기가 달린 대중적인 세단이고, FluxCD는 계기판은 투박하지만 가볍고 커스텀 개조가 자유로워 진흙탕도 거침없이 빠져나가는 수동 오프로드 짚차다.

---

### Ⅳ. 실무 적용 및 기술사 판단
인프라 책임자는 조직의 역량과 클러스터 환경에 따라 CD 도구를 선택해야 구성을 해야 한다.

- **도입 권장 (FluxCD 채택)**: [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 숙련도가 높은 엔지니어 중심 조직이거나, 에지 컴퓨팅([Edge Computing](/studynote/12_it_management/05_security_compliance/235_edge_computing_smart_factory/))처럼 제한된 리소스 환경에서 다수의 작은 클러스터를 관리해야 할 때 Flux의 저전력 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 구조가 빛을 발한다.
- **도입 주의 (ArgoCD 권장)**: 개발자(Dev)가 직접 배포 상태를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고 디버깅해야 하거나, 비개발 직군(PM, QA)에게 직관적인 시각적 대시보드가 반드시 필요한 조직이라면 ArgoCD가 압도적으로 유리하다.
- **이미지 자동 업데이트 고려**: Flux의 Image Automation 기능은 Git 커밋 이력을 자동으로 덮어써서 인프라 엔지니어의 수작업을 줄여주지만, Git 이력이 봇의 커밋으로 도배될 수 있으므로 배포 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 [감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 추적([Audit Trail](/studynote/11_design_supervision/01_audit_framework/065_audit_trail_worm_storage_compliance/)) 규칙과 충돌하지 않는지 사전에 판단해야 한다.

- **📢 섹션 요약 비유**: 시각적인 설명서 없이는 일하기 힘든 초보자 비율이 높다면 ArgoCD를 도입해야 하고, 설명서 없이도 터미널만으로 자유자재로 기계를 다루는 숙련된 장인들만 있다면 가볍고 빠른 FluxCD가 최고의 무기가 된다.

---

### Ⅴ. 기대효과 및 결론
FluxCD를 도입하면 보안 위험을 안고 있던 외부 연동 방식(Push)을 버리고, 클러스터가 스스로 자생력을 갖추는 진정한 [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 환경을 구축할 수 있다. [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)된 아키텍처는 클러스터 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 부담을 주지 않으며, CLI 기반의 높은 자동화 연계성은 인프라 관리를 완벽한 코드([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/))의 영역으로 끌어올린다.

단일 UI의 부재라는 단점은 있으나, 이는 K8s 네이티브 철학에 타협하지 않은 결과다. 결론적으로 FluxCD는 빠르고 가볍게 [스케일 아웃](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)하는 현대적 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 배포 환경에서, '가장 순수한 형태의 K8s 배포 엔진'으로 그 가치를 굳건히 지킬 것이다.

- **📢 섹션 요약 비유**: FluxCD는 요란하게 소리 내지 않고 묵묵히 백그라운드에서 완벽하게 창고 정리를 끝내놓는, 보이지 않지만 가장 신뢰할 수 있는 수석 창고 관리인이다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/">GitOps</a></strong> | FluxCD가 실현하고자 하는 핵심 철학 (Git이 진실의 원천) |
| **ArgoCD** | FluxCD와 [GitOps](/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/) 시장을 양분하는 가장 강력한 라이벌 |
| **CRD (Custom Resource Definition)** | Flux가 K8s의 기본 기능을 확장하여 사용하는 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 방식 |
| **Pull 기반 배포** | 클러스터가 외부(Git)를 주도적으로 조회하여 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)하는 보안 지향적 배포 모델 |
| <strong><a href="/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/">Kustomize</a> / <a href="/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/">Helm</a></strong> | Flux가 Git에서 가져온 템플릿을 실제 매니페스트로 렌더링할 때 쓰는 도구 |

### 📈 관련 키워드 및 발전 흐름도
```text
Push 기반 배포 (Jenkins 외부 스크립트)
    |
    v
보안 취약점 및 상태 불일치(Drift) 문제 대두
    |
    v
GitOps 개념 탄생 (Weaveworks) 및 Flux v1 도입
    |
    v
Flux v2 재설계 (GitOps Toolkit 마이크로서비스화)
    |
    v
Image Automation 및 멀티 테넌시 분산 배포 고도화
```

### 👶 어린이를 위한 3줄 비유 설명
1. 예전에는 택배 기사 아저씨가 우리 집 비밀번호를 직접 누르고 들어와서(Push) 물건을 놓고 갔어요.
2. Flux는 우리 집 안에 있는 똑똑한 로봇강아지예요. 이 강아지가 수시로 문을 열고 우체통(Git)을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해서 물건을 물어와요(Pull).
3. 남에게 집 비밀번호를 안 알려줘도 되니 도둑 걱정도 없고, 강아지 5마리가 일을 나눠서 하니까 엄청 빠르답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 90 / 373

<- **이전**: [89. ArgoCD - 쿠버네티스를 위한 GitOps 선언적 배포 도구](/studynote/15_devops_sre/02_cicd_gitops/089_argocd_gitops_continuous_delivery_kubernetes/)
**다음**: [91. Kustomize (커스터마이즈) - K8s 오버레이 선언적 템플릿 관리](/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/) ->

---
