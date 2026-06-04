---
title: "384. ArgoCD GitOps 선언적 지속 배포 (ArgoCD GitOps Declarative Continuous Delivery)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ArgoCD는 Kubernetes 위에서 Git 저장소를 단일 진실 공급원(Single Source of Truth)으로 활용하여 선언적·풀(Pull) 기반 지속 배포를 구현하는 GitOps 컨트롤러이며, Application Controller(상태 조정기), Repo Server(매니페스트 렌더링), Dex(OIDC SSO) 등 핵심 컴포넌트로 구성된다.
> 2. **가치**: 평균 배포 시간(MTTR 포함)을 기존 CI 파이프라인 대비 약 70% 단축하고, 클러스터 드리프트 자동 감지·복구(Drift Detection & Self-Healing) 통해 감사 가능성(Auditability)과 재현성을 확보하며, 다수 클러스터/다수 환경의 배포 일관성을 보장한다.
> 3. **판단 포인트**: Application Controller 폴링 주기(3분 기본)와 Repo Server 매니페스트 렌더링의 성능 병목, AppProject 다중 테넌시 격리 정책, ApplicationSet을 통한 멀티 클러스터 Fan-out 전략, 그리고 Helm/Kustomize/Plain YAML 렌더러 선택 시 트레이드오프가 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

클라우드 네이티브 환경에서 Kubernetes는 "선언적(Declarative)" API를 통해 인프라와 애플리케이션 상태를 정의한다. 그러나 전통적인 CI/CD 파이프라인(Jenkins, GitLab CI 등)은 **푸시(Push) 방식**으로 `kubectl apply`를 실행하여 배포하므로, 다음 5가지 핵심 문제가 발생한다.

| 기존 파이프라인의 한계 | 구체적 문제점 |
| :--- | :--- |
| **상태 불일치(State Drift)** | 클러스터에서 직접 `kubectl edit`으로 변경 시 Git 저장소와 상태가 어긋남 |
| **자격증명 폭발(Credential Sprawl)** | CI 시스템이 모든 대상 클러스터의 kubeconfig를 관리해야 함 |
| **감사 추적 부재** | 누가, 언제, 어떤 명령으로 배포했는지 추적 불가 |
| **롤백 복잡성** | 배포 이력이 CI 로그에만 남아 재현 어려움 |
| **멀티 클러스터 비대칭** | dev/stg/prod 환경 간 배포 상태 비교·동기화 어려움 |

**GitOps 패러다임**은 Weaveworks가 2017년 정립한 개념으로, "Git을 단일 진실 공급원으로 사용하고, 클러스터 내부의 에이전트가 자율적으로 동기화 상태를 유지"하는 풀(Pull) 모델로 전환한다. ArgoCD는 CNCF Graduated 프로젝트(2022년)로, Kubernetes-native하게 이 원칙을 구현한다.

```text
+------------------------------------------------------------------+
|              기존 Push 기반 배포 (전통적 CI/CD)                     |
|                                                                  |
|  Developer -► Git Push -► CI Server --kubectl apply--► K8s      |
|                          (Jenkins)              (자격증명 보유)    |
|                                                  ⚠️  Drift 발생   |
+------------------------------------------------------------------+
                              v 전환
+------------------------------------------------------------------+
|              GitOps Pull 기반 배포 (ArgoCD)                       |
|                                                                  |
|  Developer -► Git Push -► Git Repo (SSOT)                        |
|                              |                                   |
|                              v (3분 주기 polling)                |
|   +------------------------------------------------+             |
|   |           K8s Cluster 내부                      |             |
|   |  Application Controller --► Repo Server         |             |
|   |         |                    |                  |             |
|   |         v                    v                  |             |
|   |  Live State  ◄-- 비교 --►  Desired State       |             |
|   |         |                                       |             |
|   |         +---- 자동 Sync (Self-Heal) ------------+             |
|   +------------------------------------------------+             |
+------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Push 방식은 택배 기사가 각 가정의 비밀번호를 알고 문을 여는 방식이고, GitOps는 각 가정에 자동 잠금장치를 설치해 "이 상태가 정답"이라는 원본 도면을 두고 스스로 맞춰가는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ArgoCD는 Kubernetes Operator 패턴을 따르며, 다음 핵심 Custom Resource Definition(CRD)으로 동작한다.

| CRD | 명칭 | 역할 |
| :--- | :--- | :--- |
| **Application** | 개별 배포 단위 | Git 경로 + 대상 클러스터/네임스페이스 매핑 |
| **AppProject** | 논리적 프로젝트 | RBAC, 허용된 Git 소스, 대상 클러스터/리소스 화이트리스트 |
| **ApplicationSet** | 다중 Application 생성기 | ClusterGenerator, GitGenerator, Matrix Generator 등 |
| **AppOfApps** | 계층적 Application | 상위 Application이 하위 Application을 관리 (deprecated -> ApplicationSet 권장) |

```text
+--------------------------------------------------------------------+
|                      ArgoCD Control Plane                          |
|                                                                    |
|  +----------------+   +-----------------+   +-----------------+  |
|  |  argocd-server |   |   Dex Server     |   |  Notifications  |  |
|  |  (API + UI)    |◄-►|  (OIDC/SSO)      |   |  Controller     |  |
|  |  gRPC/REST     |   |  GitHub, SAML... |   |  Slack, Webhook |  |
|  +--------+-------+   +-----------------+   +-----------------+  |
|           |                                                        |
|           v                                                        |
|  +----------------------------------------------------------+    |
|  |          Application Controller (State Reconciler)         |    |
|  |  • Spec/Status 비교 (desired vs actual)                   |    |
|  |  • Reconcile Loop (default 3분, status reconcile 5초)     |    |
|  |  • OutOfSync 감지 -> Sync Hook 실행                         |    |
|  |  • Health Check (lua script, Resource Hook)              |    |
|  +------------------------+---------------------------------+    |
|                           | gRPC (50051)                          |
|                           v                                       |
|  +----------------------------------------------------------+    |
|  |               Repo Server (Manifest Renderer)              |    |
|  |  • Git fetch (shallow clone)                              |    |
|  |  • Manifest 생성: Helm 3 / Kustomize / Plain YAML / Jsonnet|    |
|  |  • 캐시 (Redis 5분 TTL) -> 2차 reconcile 시 25% 성능 향상  |    |
|  +------------------------+---------------------------------+    |
|                           |                                       |
|                           v                                       |
|                  +-----------------+                              |
|                  |  Redis (cache)  |                              |
|                  +-----------------+                              |
+--------------------------------------------------------------------+
                            |
                            v (선언적 Apply)
+--------------------------------------------------------------------+
|                  대상 Kubernetes Cluster (in-cluster)              |
|  Application CRD, AppProject CRD, ApplicationSet CRD               |
|  + 실제 워크로드(Deployment, Service, ConfigMap, CRD...)           |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Application Controller** | 상태 조정(Reconciler) | `argocd-application-controller` StatefulSet, Informer 패턴으로 K8s 리소스 watch, Spec(Desired)과 Live(Actual) diff 계산, **Self-Heal 옵션**으로 자동 복구 |
| **Repo Server** | 매니페스트 렌더링 | `argocd-repo-server` Deployment, gRPC로 Controller와 통신, Helm values, Kustomize patches, **Sidecar 패턴**으로 커스텀 렌더러(Pulumi, Custom Tool) 주입 가능 |
| **argocd-server** | API Gateway + UI | TLS, gRPC REST gateway (port 443), CLI(`argocd` 명령) 지원, RBAC 정책 적용 (CASL 기반) |
| **Dex / SSO** | 인증/인가 | OIDC 프로토콜, GitHub/GitLab/Google/LDAP/ SAML 연동, **SSO RBAC**으로 사용자/그룹별 정책 |
| **Redis** | 캐시 및 세션 | Repo Server 렌더링 결과 캐싱(5분), argocd-server 세션 저장, HA 구성 시 Sentinel/Cluster 모드 |

### 핵심 동작 메커니즘: Sync Wave와 Hook

Application 내 리소스 배포 순서는 `argocd.argoproj.io/sync-wave` 어노테이션으로 제어한다. Wave 번호 오름차순으로 적용되며, 동일 wave 내에서는 자동 정렬된다. Hook 타입은 다음 5종류다.

```text
Sync Wave 0 (Pre-Sync)    ->  Wave 1 (Normal)  ->  Wave 2 (Post-Sync)  ->  Wave 3 (Sync-Fail)
   |                              |                       |                     |
   v                              v                       v                     v
DB Schema 변경              Deployment, Service       Smoke Test         Rollback Hook
Job: PreSync                (기본 배포)               Job: PostSync       (실패 시 실행)
```

- **PreSync Hook**: 마이그레이션, 스키마 적용
- **Sync Hook**: 기본 배포 순서를 가로채는 작업
- **PostSync Hook**: 배포 후 검증, 캐시 무효화, 알림
- **SyncFail Hook**: Sync 실패 시 자동 롤백

### 비교 가능한 Application 상태

| 상태 | 의미 | UI 색상 |
| :--- | :--- | :--- |
| **Healthy / Synced** | 리소스 정상 + Git과 일치 | 🟢 Green |
| **Healthy / OutOfSync** | 리소스 정상이나 Git과 차이 | 🟡 Yellow |
| **Progressing** | 배포/롤아웃 진행 중 | 🔵 Blue |
| **Degraded / Suspended** | 리소스 비정상 | 🔴 Red / ⚪ Gray |
| **Missing** | 대상 리소스 부재 | 🟣 Purple |

- **📢 섹션 요약 비유**: ArgoCD는 학생(클러스터)이 항상 정답지(Git)를 보며 답안을 작성하는 시험 감독관이고, Repo Server는 정답지를 깔끔하게 풀어 써주는 조수, Application Controller는 채점관이다.

---

## Ⅲ. 비교 및 연결

### ArgoCD vs 유사 GitOps 도구 / 전통 CI 도구

| 구분 | **ArgoCD** | **FluxCD** | **Jenkins X** | **Spinnaker** |
| :--- | :--- | :--- | :--- | :--- |
| **아키텍처** | 중앙집중형(Hub-Spoke 가능) | GitOps Toolkit 모듈형 (분산) | Jenkins + Tekton 기반 | 마이크로서비스 MSA |
| **배포 모델** | Pull (Agent in cluster) | Pull (Operator per cluster) | Push (Tekton) | Push (Clouddriver) |
| **렌더러** | Helm, Kustomize, Jsonnet, Plugin | Kustomize, Helm, Kustomize-controller | Helm, Kustomize | Cloud Foundry 스타일 |
| **UI/UX** | Web UI + CLI + API | CLI 중심 (Weave GitOps UI 별도) | Jenkins UI 상속 | 자체 Web UI 강력 |
| **진행적 배포** | **Argo Rollouts** (Canary, Blue-Green, A/B) | Flagger 통합 | Spinnaker 스타일 | Canary, Traffic Shadowing |
| **다중 클러스터** | **ApplicationSet Hub-Spoke** | Mono/Multi-repo | 제한적 | 강력(Fiat RBAC) |
| **확장성** | CRD 기반 무제한 | Toolkit 컴포저블 | Jenkins 빌드 수 확장 | 수천 파이프라인 검증 |
| **학습 곡선** | 중간 (CRD, AppProject) | 중상 (Toolkit 조합) | 상 (Jenkins 생태계) | 상 (Halyard 설정) |
| **CNCF 상태** | Graduated (2022) | Graduated (2023) | Archived (대안 권장) | Incubating |
| **적합 시나리오** | 멀티 클러스터 K8s, 시각적 운영 | GitOps 원칙 순수 준수, Edge K8s | 기존 Jenkins 사용자 전환 | VM/베어메탈 + K8s 하이브리드 |

### 다른 시스템과의 연결 (Ecosystem)

```text
+--------------------------------------------------------------------+
|                          Ecosystem                                  |
|                                                                    |
|   +----------+    +----------+    +----------+    +----------+   |
|   |   Git    |    |  CI/CD   |    |  Secrets |    | Monitoring|   |
|   |  Repo    |    |  Build   |    |  Vault   |    | Prometheus|   |
|   |(GitHub,  |    |(Tekton,  |    | ESO,     |    | Grafana,  |   |
|   | GitLab)  |    |  Jenkins)|    | Sealed   |    |  Datadog  |   |
|   +----+-----+    +----+-----+    | Secret   |    +----+-----+   |
|        |               |          +----+-----+         |         |
|        | 이미지 푸시   |               |                |         |
|        v               v               v                v         |
|   +----------------------------------------------------------+   |
|   |              Image Registry (Harbor, ECR, GCR)            |   |
|   +--------------------------+-------------------------------+   |
|                              |                                     |
|                              v                                     |
|   +----------------------------------------------------------+   |
|   |   ArgoCD Sync <- Helm/Kustomize 매니페스트 + git revision  |   |
|   +--------------------------+-------------------------------+   |
|                              |                                     |
|                              v                                     |
|   +----------------------------------------------------------+   |
|   |   Kubernetes (Production Clusters)                        |   |
|   |   + Argo Rollouts (Canary) + Istio/NGIN✗ (Traffic Split) |   |
|   +----------------------------------------------------------+   |
+--------------------------------------------------------------------+
```

- **CI(빌드) ↔ CD(배포) 분리**: Tekton/GitHub Actions가 이미지 빌드 -> 태그 업데이트 커밋 -> ArgoCD가 이를 감지하여 배포 (진정한 GitOps)
- **External Secrets Operator**: Vault/AWS Secrets Manager의 비밀을 K8s Secret으로 동기화 후 ArgoCD로 배포
- **Argo Rollouts**: 카나리 배포 중 Prometheus 메트릭으로 자동 승격/롤백
- **Sealed Secrets / SOPS**: Git 저장소 내 비밀값 암호화

- **📢 섹션 요약 비유**: ArgoCD는 "요리사"이고, Git은 "레시피", CI는 "재료 손질", Sealed Secrets는 "보안 요원", Argo Rollouts는 "테스트 셰프"와 같다. 각자 역할이 분리되어 있어 교체가 쉽다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **렌더러 선택**: Helm(복잡한 values 재사용·조건부 렌더링), Kustomize(경량 오버레이, GitOps 친화), 또는 Plain YAML(가장 투명) 중 어떤 것을 채택할지? Helm은 차트 의존성과 templating 버그 위험, Kustomize는 복잡한 변환 한계, Plain YAML은 DRY 원칙 위배.
2. **Sync 정책과 Self-Heal**: `automated.selfHeal: true`로 자동 복구할 것인지? 운영 중 임시 패치는 Git에 커밋되어야 하는데, 이를 강제하면 현장 대응력이 떨어진다. Kustomize의 `Strategic Merge Patch`로 환경별 오버레이 분리.
3. **다중 클러스터 전략**: Hub-Spoke(ApplicationSet ClusterGenerator) vs Repo-per-Cluster. **Hub-Spoke는 단일 장애점(SPOF)**, Repo-per-Cluster는 **확장성·독립성 우수하지만 정책 일관성 관리 어려움**.
4. **보안·컴플라이언스**: AppProject의 `clusterResourceWhitelist`, `namespaceResourceWhitelist`로 테넌시 격리, Git의 Signed Commit 검증, ArgoCD Image Updater 권한 최소화, **암호화 통신(TLS 1.3, mTLS)**, Audit Log 중앙화.
5. **성능·확장성 한계**: Application Controller의 동시 reconcile 수(`--status-processors`, `--kubectl-parallelism-limit` 기본 10), Repo Server의 `--max-connections` 기본
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 384 / 800

<- **이전**: [383. Kustomize 선언적 설정 관리 오버레이](/studynote/13_cloud_architecture/06_exam_summary/383_kustomize_declarative_config_overlay_manageme/)
**다음**: [385. Flux GitOps 자동 동기화 배포](/studynote/13_cloud_architecture/06_exam_summary/385_flux_gitops_auto_sync_deployment/) ->

---
