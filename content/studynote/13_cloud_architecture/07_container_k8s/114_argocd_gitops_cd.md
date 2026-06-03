---
title: 114. Argo CD (ArgoCD GitOps CD) - K8s 선언적 지속 배포·Git 단일 진실 원천
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Argo CD는 **Git 레포지토리를 단일 진실 원천(Single Source of Truth)**으로 삼아, Git의 매니페스트와 K8s 클러스터 상태를 **실시간 비교(Diff)하고 자동 [[212_synchronization_mechanisms|동기화]](Sync)**하는 [[190_cncf_landscape_observability|CNCF]] 졸업 [[119_gitops_single_source_of_truth|GitOps]] CD 도구다.
> 2. **가치**: 전통 [[090_configuration_item|CI]]/CD([[071_jenkins_ci_cd_pipeline_automation|Jenkins]])가 "Push 기반(파이프라인이 클러스터에 적용)"이라면, Argo CD는 **"Pull 기반(클러스터가 Git을 감시하여 스스로 [[212_synchronization_mechanisms|동기화]])"**하므로, 클러스터 접근 권한을 [[090_configuration_item|CI]] 시스템에 노출하지 않아 **보안이 강화**된다.
> 3. **판단 포인트**: Argo CD는 K8s 매니페스트(YAML/[[207_helm_kubernetes_package_manager_chart|Helm]]/[[091_kustomize_kubernetes_declarative_overlay_manifest|Kustomize]])를 관리하며, Argo Rollouts와 결합하여 **[[595_canary_stack_smashing_protector|카나리]]·블루/그린 배포를 선언적으로** 수행한다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Push 기반 CD vs Pull 기반 GitOps (Argo CD)         │
├───────────────────────────────────────────────────────┤
│  [Push: Jenkins]                                      │
│   개발자 → Git Push → Jenkins → kubectl apply → K8s  │
│   Jenkins에 클러스터 kubeconfig 필요 (보안 위험)      │
│                                                       │
│  [Pull: Argo CD]                                      │
│   개발자 → Git Push → (끝)                            │
│   Argo CD (클러스터 내부) → Git 감시 → 자동 Sync     │
│   Jenkins에 클러스터 권한 불필요 (보안 강화)          │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Push CD는 택배([[071_jenkins_ci_cd_pipeline_automation|Jenkins]])가 집까지 직접 배달하는 것이고, Pull CD(Argo CD)는 집 앞 우편함(Git)에 넣으면 집주인(클러스터)이 스스로 가져가는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Argo CD 핵심 개념

| 개념 | 설명 |
|:---|:---|
| **Application** | Git 레포 경로 + 타겟 클러스터/[[061_namespace|네임스페이스]] 매핑 |
| **Sync** | Git 상태 → K8s 클러스터 적용 |
| **Diff** | Git vs 클러스터 상태 차이 감지 |
| **Health** | [[198_pod_kubernetes_minimum_deployment_unit|Pod]]/[[087_deployment_kubernetes_workload_rolling_update|Deployment]] 건강 상태 모니터링 |
| **Prune** | Git에서 삭제된 리소스를 클러스터에서도 삭제 |

### 지원 매니페스트 형식
- **Plain YAML**, **[[056_helm_chart|Helm Chart]]**, **[[091_kustomize_kubernetes_declarative_overlay_manifest|Kustomize]]**, **Jsonnet**

- **📢 섹션 요약 비유**: Argo CD는 냉장고(클러스터)와 장보기 목록(Git)을 항상 일치시키는 [[190_ai_llm_requirements_specification|AI]] 비서다. 목록에서 우유를 지우면 냉장고에서도 우유를 꺼낸다(Prune).

---

## Ⅲ. 비교 및 연결

| 비교 | [[071_jenkins_ci_cd_pipeline_automation|Jenkins]] CD | Argo CD | Flux |
|:---|:---|:---|:---|
| **방식** | Push | **Pull ([[119_gitops_single_source_of_truth|GitOps]])** | Pull ([[119_gitops_single_source_of_truth|GitOps]]) |
| **보안** | CI에 클러스터 권한 | **클러스터 내부** | 클러스터 내부 |
| **UI** | [[071_jenkins_ci_cd_pipeline_automation|Jenkins]] 대시보드 | **리소스 트리 [[003_bigdata_7v|시각화]]** | CLI 중심 |
| **[[190_cncf_landscape_observability|CNCF]]** | - | **Graduated** | Graduated |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 도입 [[435_checklist_based_testing|체크리스트]]
1. **Git 레포 분리**: 앱 코드 레포 + 매니페스트 레포 분리 ([[009_config|Config]] Repo 패턴).
2. **[[569_rbac|RBAC]]**: Argo CD 프로젝트별 접근 제어.
3. **Argo Rollouts**: [[595_canary_stack_smashing_protector|카나리]]·블루/그린 배포 선언적 관리.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **[[077_kube_api_server_k8s_hub|kubectl]] apply 수동 실행 병행**: Git과 클러스터 상태 불일치 → [[119_gitops_single_source_of_truth|GitOps]] 원칙 파괴.

---

## Ⅴ. 기대효과 및 결론

| 지표 | [[071_jenkins_ci_cd_pipeline_automation|Jenkins]] CD | Argo CD | 개선 |
|:---|:---|:---|:---|
| 클러스터 권한 노출 | CI에 kubeconfig | **클러스터 내부만** | 보안 강화 |
| 상태 드리프트 감지 | 불가 | **실시간 Diff** | 즉시 감지 |
| [[098_rollback_strategy_pipeline_error_threshold|롤백]] | 파이프라인 재실행 | **Git Revert → 자동 Sync** | 30초 |

Argo CD는 멀티클러스터 [[119_gitops_single_source_of_truth|GitOps]]·Argo Workflows([[090_configuration_item|CI]]) 통합으로 **[[090_configuration_item|CI]]/CD 전체를 [[119_gitops_single_source_of_truth|GitOps]] 패러다임**으로 통합하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[119_gitops_single_source_of_truth|GitOps]]** | Argo CD가 구현하는 배포 패러다임 |
| **Argo Rollouts** | [[595_canary_stack_smashing_protector|카나리]]·블루/그린 배포 확장 |
| **Flux** | 경쟁 [[119_gitops_single_source_of_truth|GitOps]] CD 도구 ([[190_cncf_landscape_observability|CNCF]]) |
| **[[207_helm_kubernetes_package_manager_chart|Helm]] / [[091_kustomize_kubernetes_declarative_overlay_manifest|Kustomize]]** | Argo CD가 지원하는 매니페스트 형식 |
| **[[009_config|Config]] Repo 패턴** | 앱 코드와 매니페스트 레포 분리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Jenkins CD (2010s) — Push 기반 파이프라인 배포]
    │
    ▼
[GitOps 개념 (2017, Weaveworks) — Git = 단일 진실 원천]
    │
    ▼
[Argo CD v1 (2018) — K8s Pull 기반 CD]
    │
    ▼
[CNCF Graduated (2022) — 생태계 표준화]
    │
    ▼
[현재: Argo CD + Argo Workflows — CI/CD 전체 GitOps 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 옛날에는 택배 아저씨([[071_jenkins_ci_cd_pipeline_automation|Jenkins]])가 집까지 와서 직접 물건을 놓아줬어요.
2. Argo CD는 **우편함(Git)에 넣으면 집주인(클러스터)이 알아서 가져가는** 시스템이에요.
3. 택배 아저씨에게 **집 열쇠를 안 줘도 돼서** 더 안전하고, 물건이 잘못 왔으면 **우편함만 바꾸면** 돼요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 113 / 371

← **이전**: [[113_kubeflow_mlops_orchestration|113. Kubeflow MLOps 오케스트레이션 - K8s 네이티브 ML 파이프라인·실험 관리]]
**다음**: [[115_terraform_infrastructure_provisioning|115. Terraform 인프라 프로비저닝 - IaC 선언적 다중 클라우드 관리]] →

---
