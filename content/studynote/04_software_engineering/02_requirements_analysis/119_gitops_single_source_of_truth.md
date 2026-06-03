---
title: 119. GitOps (Single Source of Truth) - Git을 단일 진실 원천으로 한 선언적 운영
date: '2026-04-19'
tags:
- studynote-software-engineering
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: GitOps는 **Git 리포지토리를 인프라·애플리케이션의 단일 진실 원천(Single Source of Truth)**으로 삼고, Git에 선언된 상태와 실제 클러스터 상태를 **자동으로 [[212_synchronization_mechanisms|동기화]](Reconciliation)**하는 운영 패러다임이다.
> 2. **가치**: 수동 `kubectl apply`·콘솔 조작은 변경 이력이 없고 리뷰가 불가능하지만, GitOps는 **모든 변경이 [[067_pull_request_pr_merge_request_code_review|PR]]→리뷰→머지→자동 적용** 흐름을 따르므로 [[606_auditing_linux_auditd|감사]] 가능성·재현성·[[098_rollback_strategy_pipeline_error_threshold|롤백]]이 보장된다.
> 3. **판단 포인트**: **Push 방식(CI가 [[077_kube_api_server_k8s_hub|kubectl]] push)** vs **Pull 방식(ArgoCD/Flux가 Git을 감시)**을 구분하고, Pull 방식이 보안(클러스터 외부에 [[077_kube_api_server_k8s_hub|kubectl]] 크레덴셜 불필요)에서 우수하다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    GitOps Pull 방식 워크플로                           │
├───────────────────────────────────────────────────────┤
│  1. 개발자: Git에 K8s manifest 수정 → PR              │
│  2. 리뷰어: 변경 확인 → Approve → 머지               │
│  3. ArgoCD/Flux: Git 변경 감지 (Pull)                │
│  4. 자동 Reconcile: 클러스터 상태 ← Git 선언 상태    │
│  5. 드리프트 발생 시: 자동 복원 (Self-healing)        │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: GitOps는 내비게이션(Git)이 목적지(선언 상태)를 설정하면, 자율주행차(ArgoCD)가 알아서 경로를 따라가고, 이탈(드리프트)하면 자동으로 복귀하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Push vs Pull 방식

| 비교 | Push ([[090_configuration_item|CI]]→[[077_kube_api_server_k8s_hub|kubectl]]) | Pull (ArgoCD/Flux) |
|:---|:---|:---|
| **보안** | CI에 kubeconfig 필요 | **클러스터 내부에서 Pull** |
| **Self-healing** | 없음 | **드리프트 자동 복원** |
| **대표** | [[071_jenkins_ci_cd_pipeline_automation|Jenkins]]+[[077_kube_api_server_k8s_hub|kubectl]] | **ArgoCD, Flux** |

### GitOps 4대 원칙 (OpenGitOps)
1. **선언적**: YAML/HCL로 원하는 상태 선언.
2. **[[288_version_ihl_tos_total_length|버전]] 관리**: Git에 모든 이력 보존.
3. **자동 적용**: 머지 시 자동 배포.
4. **지속 조정**: 드리프트 시 자동 복원.

- **📢 섹션 요약 비유**: GitOps는 "Git에 쓰인 대로 세상이 돌아가야 한다"는 헌법이다. 현실(클러스터)이 헌법(Git)과 다르면 자동으로 바로잡는다.

---

## Ⅲ. 비교 및 연결

| 비교 | 수동 운영 | [[090_configuration_item|CI]]/CD | GitOps |
|:---|:---|:---|:---|
| **변경 추적** | 없음 | 일부 | **Git 100%** |
| **[[098_rollback_strategy_pipeline_error_threshold|롤백]]** | 수동 | 파이프라인 | **git revert** |
| **드리프트** | 방치 | 방치 | **자동 복원** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 리포지토리 구조
- **App Repo**: 소스코드 + [[067_dockerfile_container_image_build_script|Dockerfile]].
- **[[009_config|Config]] Repo**: K8s manifests (GitOps 대상).
- CI가 App Repo 빌드 → [[009_config|Config]] Repo의 이미지 태그 업데이트 → ArgoCD 자동 배포.

---

## Ⅴ. 기대효과 및 결론

| 지표 | 수동 | GitOps | 개선 |
|:---|:---|:---|:---|
| [[606_auditing_linux_auditd|감사]] 추적 | 불가 | **Git 이력** | 100% |
| [[098_rollback_strategy_pipeline_error_threshold|롤백]] | 분 단위 | **git revert (초)** | 즉시 |
| 드리프트 | 방치 | **자동 복원** | 제로 |

GitOps는 **[[531_cloud_native_architecture|클라우드 네이티브]] 운영의 사실상 표준**이며, ArgoCD가 [[190_cncf_landscape_observability|CNCF]] Graduated 프로젝트로 채택되어 생태계가 안정적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ArgoCD** | GitOps Pull 방식의 대표 도구 |
| **Flux** | [[190_cncf_landscape_observability|CNCF]] GitOps 도구 (경량) |
| **Reconciliation** | Git ↔ 클러스터 상태 [[212_synchronization_mechanisms|동기화]] |
| **드리프트 감지** | GitOps의 Self-healing 메커니즘 |
| **[[793_iac_idempotency_template|IaC]]** | [[195_terraform_hashicorp_agnostic_aws_gcp|Terraform]]+GitOps = 인프라 GitOps |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 kubectl apply (2014~)]
    │
    ▼
[CI/CD Push 방식 (Jenkins+kubectl, 2016~)]
    │
    ▼
[GitOps 개념 (Weaveworks, 2017) — Pull 방식 제안]
    │
    ▼
[ArgoCD / Flux (2019~) — CNCF 채택]
    │
    ▼
[현재: OpenGitOps 표준 — 4대 원칙 정립]
```

### 👶 어린이를 위한 3줄 비유 설명
1. GitOps는 **설계도(Git)**를 바꾸면 로봇이 알아서 건물(클러스터)을 **자동으로 고치는** 시스템이에요.
2. 누군가 몰래 건물을 바꾸면(드리프트), 로봇이 설계도를 보고 **원래대로 되돌려놔요**.
3. 설계도 변경은 반드시 **선생님(리뷰어) 승인**을 받아야 해서 안전하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 119 / 973

← **이전**: [[118_shadow_deployment_traffic_mirroring|118. 섀도 배포 (Shadow Deployment) - 트래픽 미러링·무위험 프로덕션 검증]]
**다음**: [[120_declarative_infrastructure_idempotence|120. 선언적 인프라와 멱등성 (Declarative Infrastructure & Idempotence) - IaC 핵심 원칙]] →

---
