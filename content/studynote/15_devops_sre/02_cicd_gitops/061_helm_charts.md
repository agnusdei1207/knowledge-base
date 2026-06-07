---
title: "061. Helm Charts"
date: "2026-04-05"
tags:
  - "studynote-devops-sre"
weight: 61
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/) Charts는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 매니페스트를 템플릿과 값 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 묶어 재사용 가능한 패키지로 만드는 방식이다.
> 2. **가치**: 환경별 차이를 values.yaml로 분리해 개발/스테이징/프로덕션 배포를 같은 차트로 관리할 수 있다.
> 3. **판단**: Chart는 단순 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 묶음이 아니라 Release 이력과 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)을 포함한 운영 단위다.

---

## Ⅰ. 개요 및 필요성

[쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 애플리케이션은 [Deployment](/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/), [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), [ConfigMap](/studynote/13_cloud_architecture/02_iaas_paas_saas/102_configmap_secret_kubernetes_12_factor_app/), [Secret](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/), Ingress처럼 여러 리소스로 구성된다. 환경이 늘수록 YAML 복사가 폭발한다.

Helm은 이런 문제를 패키지화로 푼다. 템플릿은 재사용하고, 환경 차이는 values.yaml로 뺀다.

- **📢 섹션 요약 비유**: 같은 레시피를 쓰되, 설탕과 소금 양만 바꿔 여러 나라 음식에 맞추는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Chart
  +- templates/
  +- values.yaml
  +- Chart.yaml
        v render
Rendered Kubernetes YAML
        v install / upgrade
Kubernetes Cluster
```

| 구성 요소 | 역할 |
| :-- | :-- |
| Chart | 배포 패키지 단위 |
| values.yaml | 환경별 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 값 |
| templates | 동적 매니페스트 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| Release | 설치된 차트의 상태와 이력 |
| Repository | 차트 저장과 공유 |

[Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/) v3에서는 Release 정보가 클러스터 안에 저장되고, 차트 저장소는 [OCI](/studynote/13_cloud_architecture/05_data_engineering/333_process/) ([Open Container Initiative](/studynote/06_ict_convergence/03_cloud_infrastructure/205_container_image_layer_oci_standard/)) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/)나 ChartMuseum 같은 저장소와 연동될 수 있다.

- **📢 섹션 요약 비유**: 같은 금형으로 찍되, 페인트 색만 바꿔 다른 장난감을 만드는 공장이다.

---

## Ⅲ. 비교 및 연결

| 방식 | 장점 | 한계 |
| :-- | :-- | :-- |
| [Raw](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) YAML | 단순함 | 복사/중복 많음 |
| [Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/) | 템플릿화, [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리, [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) | 템플릿 복잡도 증가 |
| [Kustomize](/studynote/15_devops_sre/02_cicd_gitops/091_kustomize_kubernetes_declarative_overlay_manifest/) | 오버레이에 강함 | 패키징/릴리스 개념은 약함 |

Helm은 "[쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 앱을 배포 가능한 단위로 묶는 것"에 강하고, Kustomize는 "기존 YAML을 환경별로 덧씌우는 것"에 강하다. 둘은 경쟁이라기보다 서로 다른 운영 스타일이다.

- **📢 섹션 요약 비유**: 옷을 새로 짓는 것은 차트, 기존 옷에 패치를 덧대는 것은 Kustomize다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 환경 차이를 values.yaml로 분리했는가?
2. 템플릿에 비즈니스 로직을 과도하게 넣지 않았는가?
3. Secrets가 안전하게 관리되는가?
4. Release [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)과 히스토리가 가능한가?
5. 차트 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)과 앱 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 분리되어 관리되는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 템플릿 안에 복잡한 조건문을 쌓아 [가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/)을 잃는 설계
- Secret을 평문 values에 넣는 설계
- 차트 하나로 모든 앱을 억지로 우겨 넣는 설계
- release history와 테스트 없이 곧바로 운영에 넣는 설계

기술사 관점에서 Helm은 "YAML을 줄이는 도구"가 아니라 "배포와 운영을 표준화하는 도구"다. 차트 구조와 배포 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 함께 관리되어야 한다.

- **📢 섹션 요약 비유**: 부품 상자에 라벨을 붙여 놓아야 조립과 수리가 쉬워지는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

[Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/) Charts는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 애플리케이션을 재사용 가능하고 관리 가능한 운영 단위로 바꾼다. 덕분에 배포 자동화와 환경 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)이 좋아진다.

결국 Helm의 핵심은 "배포 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)"이 아니라 "운영 가능한 패키지"를 만드는 데 있다.

- **📢 섹션 요약 비유**: 흩어진 부품을 한 상자에 모아, 언제든 다시 조립할 수 있게 하는 것이다.

---

## 관련 개념 맵

```text
Chart
   v
Templates / values.yaml
   v
Rendered Manifest
   v
Kubernetes Release
   v
Rollback / Versioning
```

---

## 관련 키워드 및 발전 흐름도

```text
Raw YAML
   v
Helm Chart
   v
Release Management
   v
OCI Registry
   v
GitOps
```

---

## 어린이를 위한 3줄 비유 설명

[Helm](/studynote/06_ict_convergence/03_cloud_infrastructure/207_helm_kubernetes_package_manager_chart/) Charts는 레고 설명서처럼 부품과 순서를 묶어 둔 거예요.
색깔만 바꿔 여러 [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)을 만들 수 있어요.
그래서 같은 모양을 여러 곳에 쉽게 설치할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 61 / 373

<- **이전**: [60. ChatOps (Chat + Operations) 협업 운영 모델](/studynote/15_devops_sre/01_culture_methodology/060_chatops/)
**다음**: [62. 인프라스트럭처 애즈 코드 (Infrastructure as Code, IaC)](/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/) ->

---
