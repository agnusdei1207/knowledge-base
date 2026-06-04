---
title: "585. GitOps 선언적 인프라 관리 패턴 (GitOps Declarative Infrastructure Pattern)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Git 저장소를 인프라 및 애플리케이션 배포의 **유일한 진실의 원천(Single Source of Truth)**으로 삼고, GitOps Operator(Argo CD, Flux CD 등)가 선언적 상태(Desired State)와 실제 상태(Actual State) 간의 **컨버전스 루프(Convergence Loop)**를 통해 자동으로 동기화하는 운영 패러다임. Kubernetes CRD, Helm, Kustomize, Jsonnet 등 **선언적 매니페스트(Declarative Manifest)**를 Git에 버전 관리하고, **Pull 기반 에이전트 모델**로 클러스터 외부에서 변경을 강제할 수 없는 보안 경계 안에서 운영한다.
> 2. **가치**: 평균 복구 시간(MTTR)을 수동 배포 대비 **60~80% 단축**(Weaveworks, DORA Report 기반), 변경 감사 추적성 100%(Git 커밋 히스토리), 배포 실패율 **평균 50% 감소**, RBAC·SSO·Code Review 등 기존 Git 플랫폼의 보안 통제(Governance)를 인프라 운영에 그대로 적용 가능. 결과적으로 **Mutable Infrastructure -> Immutable + Idempotent** 환경으로 전환되어 "Configuration Drift" 문제를 구조적으로 차단한다.
> 3. **판단 포인트**: ① **Push 모델(CI-CD 파이프라인이 직접 kubectl apply)** vs **Pull 모델(클러스터 내부 에이전트가 Git을 폴링)** 간의 보안·지연시간·멀티클러스터 트레이드오프, ② **Application 정의 방식** (Helm vs Kustomize vs Jsonnet vs CUE) 선택, ③ Sealed Secrets, External Secrets Operator, HashiCorp Vault, SOPS 등 **Secret 관리 전략**, ④ **Repository 구조** (Monorepo vs Polyrepo vs App-of-Apps vs Kustomize Composition), ⑤ 멀티 클러스터/멀티 환경 분리 정책(Base vs Overlay, Git Branch 전략).

---

## Ⅰ. 개요 및 필요성

전통적 인프라 운영은 **명령형(Imperative)** 방식이었다. "이 서버에 SSH로 접속하여, Apache를 설치하고, 설정 파일을 수정하고, 서비스를 재시작하라"는 일련의 절차(Procedure) 중심 운영은 다음과 같은 구조적 문제를 야기했다.

- **Configuration Drift**: 수동 변경이 누적되면서 dev/staging/prod 환경 간 설정이 미세하게 달라지는 현상. 실제 운영 환경은 "누가 언제 어떤 변경을 했는지" 추적 불가능한 Snowflake Server가 된다.
- **Auditability 부재**: 인프라 변경 이력이 Jenkins 로그, Slack 메시지, 개인 노트북의 ~/.bash_history에 분산되어 변경 감사(GitOps Auditability)가 불가능.
- **환경 간 비일관성**: "내 PC에서는 됐는데"라는 문제가 빈번. 로컬에서는 잘 작동하지만 운영 환경에서 오작동하는 현상.
- **롤백 어려움**: 장애 발생 시 이전 상태로 되돌리려면, 어떤 변경이 언제 적용되었는지 파악하는 것 자체가 어려움.
- **불완전한 재현성**: 신규 환경 구성 시 똑같이 만들기 위해 운영자의 암묵지(Tacit Knowledge)에 의존.

DevOps 운동은 2009년 Patrick Debois가 제안한 이래 **CAMS**(Culture, Automation, Measurement, Sharing) 원칙을 통해 자동화를 강조했지만, 초기 자동화는 여전히 **명령형 스크립트**(Ansible Playbook, Shell Script, Jenkins Pipeline) 중심이었다. **Infrastructure as Code(IaC)** 도구(Terraform, CloudFormation, Pulumi)가 등장하면서 선언적 인프라의 기반이 마련되었지만, "IaC 파일을 Git에 저장했더라도, 누군가(또는 어떤 파이프라인)가 그것을 실행해야 한다"는 점에서 **Git과 실제 환경 간의 단방향 동기화**만 가능했다.

**GitOps는 2017년 Weaveworks CEO Alexis Richardson이 처음 명명**한 개념으로, Git을 단순한 코드 저장소가 아니라 **운영 환경(Production Environment) 자체의 진실의 원천**으로 격상시켰다. 핵심 통찰은 다음과 같다: *"운영자가 직접 Kubernetes API Server에 kubectl apply를 실행하는 것이 아니라, Git의 특정 브랜치/태그에 병합(Merge)되는 순간, 클러스터 내부의 에이전트가 이를 감지하여 자동으로 동기화한다."*

이 전환의 의미는 근본적이다. 인프라 변경을 위한 **승인 워크플로우(PR Review, CODEOWNERS)** 가 코드 변경과 동일해지고, 모든 인프라 상태가 Git 커밋 해시로 식별 가능해지며, "재해 복구(DR)"는 단순히 Git 저장소를 복구하는 것만으로 완료된다.

```text
[기존 명령형 인프라 운영 vs GitOps 선언적 운영의 구조적 차이]

  ◆ 전통적 명령형/반자동화 운영 ◆                  ◆ GitOps 선언적 운영 ◆

   개발자 --+                                       개발자 --+
            | PR/MR                                       | PR/MR (선언적 YAML)
   운영자 --+                                             |
            v                                             v
        Git Repo                              +----------------------+
   (IaC 스크립트)                             |     Git Repository   |
            |                                 |  (Source of Truth)   |
            | Jenkins/Ansible 실행            |  +--------------+   |
            v                                 |  | manifests/   |   |
   +--------------+                          |  |  + app1.yaml |   |
   | 운영 환경    | <- 직접 변경(Snowflake)    |  |  + app2.yaml |   |
   | (불일치)     | <- 콘솔에서 수동 변경       |  |  + secrets/  |   |
   |  서버 A,B,C  | <- 절차 기억 의존         |  +--------------+   |
   +--------------+                          +----------+-----------+
   ❌ Drift 발생                                +-------+--------+
   ❌ 변경 추적 불가                            |   Pull Agent   |
   ❌ 롤백 어려움                              | (ArgoCD/Flux)  |
                                               |  in Cluster    |
                                               +-------+--------+
                                                       | Reconcile Loop
                                                       v
                                                +--------------+
                                                | 클러스터     |
                                                | (Desired=    |
                                                |  Actual)     |
                                                +--------------+
                                                ✅ Drift 자동 교정
                                                ✅ 모든 변경 Git 추적
                                                ✅ 재해복구 = Git 복구
```

- **📢 섹션 요약 비유**: 기존 인프라 운영이 "건물 관리인의 머릿속 청소 루틴"이었다면, GitOps는 **"건물의 도면(Git)만 바꾸면 자동으로 시공·수선이 일어나는 BIM(Building Information Modeling) 시스템"**과 같다. 관리인은 도면만 수정하고, 그 외 모든 작업은 자동화된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

GitOps 아키텍처는 **4개의 핵심 구성 요소**로 이루어진다: ① 진실의 원천(SoT)인 Git Repository, ② 선언적 IaC 매니페스트, ③ GitOps Operator(에이전트), ④ 관측/드리프트 감지(Observability).

핵심 동작 원리는 **컨버전스 루프(Convergence Loop)**이다. 이는 제어 이론의 폐루프 제어(Closed-Loop Control)에서 유래한 개념으로, **Desired State(Git)와 Actual State(클러스터)** 의 차이(Delta)를 주기적으로 측정하고, 차이가 발견되면 이를 보정하는 알고리즘이다.

```text
[GitOps 상세 아키텍처 및 컨버전스 루프 데이터 흐름]

  +--------------------------------------------------------------------+
  |                      Git Repository (SoT)                          |
  |  +--------------+  +--------------+  +------------------------+    |
  |  | main branch  |  |  PR Review   |  |  Signed Commits (GPG)  |    |
  |  | (production) |  |  CODEOWNERS  |  |  Branch Protection     |    |
  |  +------+-------+  +------+-------+  +----------+-------------+    |
  +---------+-----------------+---------------------+------------------+
            |                 | PR Merge            | Webhook (선택)
            |                 |                     v
  +---------+-----------------+--------------------------------------+
  |                   CI Pipeline (선택적)                            |
  |  +----------+ +----------+ +----------+ +--------------------+   |
  |  |  Lint    | |  Test    | |  Build   | |  Sign/OIDC Token   |   |
  |  |(kubeconform)| |(kuttl, | |(OCI image)| | (cosign, sigstore)|   |
  |  |          | |conftest) | |          | |                    |   |
  |  +----------+ +----------+ +----------+ +--------------------+   |
  |         |             |             |             |                |
  |         +-------------+------+------+-------------+                |
  +----------------------------+--------------------------------------+
                               | Image Push
                               v
                    +----------------------+
                    |  OCI Registry        |
                    |  (Harbor, ECR, GHCR) |
                    |  + Image Signature   |
                    +----------+-----------+
                               | Pull
       +-----------------------+--------------------------+
       |                       |                          |
       v                       v                          v
  +------------------+ +------------------+ +------------------+
  |  Cluster A       | |  Cluster B       | |  Cluster C       |
  |  +------------+  | |  +------------+  | |  +------------+  |
  |  | GitOps     |  | |  | GitOps     |  | |  | GitOps     |  |
  |  | Operator   |--+-+--| Operator   |  | |  | Operator   |  |
  |  | (ArgoCD/   |  | |  | (ArgoCD/   |  | |  | (ArgoCD/   |  |
  |  |  Flux CD)  |  | |  |  Flux CD)  |  | |  |  Flux CD)  |  |
  |  +-----+------+  | |  +-----+------+  | |  +-----+------+  |
  |        | Poll    | |        | Poll    | |        | Poll    |
  |        | 3~5min  | |        | 3~5min  | |        | 3~5min  |
  |        v         | |        v         | |        v         |
  |  +----------+    | |  +----------+    | |  +----------+    |
  |  |Desired   |    | |  |Desired   |    | |  |Desired   |    |
  |  |State     |    | |  |State     |    | |  |State     |    |
  |  |(Git)     |    | |  |(Git)     |    | |  |(Git)     |    |
  |  +----+-----+    | |  +----+-----+    | |  +----+-----+    |
  |       | Compare  | |       | Compare  | |       | Compare  |
  |       v          | |       v          | |       v          |
  |  +----------+    | |  +----------+    | |  +----------+    |
  |  |Actual    |    | |  |Actual    |    | |  |Actual    |    |
  |  |State     |    | |  |State     |    | |  |State     |    |
  |  |(K8s API) |    | |  |(K8s API) |    | |  |(K8s API) |    |
  |  +----+-----+    | |  +----+-----+    | |  +----+-----+    |
  |       | Apply    | |       | Apply    | |       | Apply    |
  |       v          | |       v          | |       v          |
  |  +----------+    | |  +----------+    | |  +----------+    |
  |  |Workloads |    | |  |Workloads |    | |  |Workloads |    |
  |  |(Pods,    |    | |  |(Pods,    |    | |  |(Pods,    |    |
  |  | Services)|    | |  | Services)|    | |  | Services)|    |
  |  +----------+    | |  +----------+    | |  +----------+    |
  +------------------+ +------------------+ +------------------+
        |                     |                     |
        +-------------+-------+----------+----------+
                      | Telemetry       |
                      v                  v
            +----------------------------------+
            |  Observability Layer             |
            |  (Prometheus, Grafana,          |
            |   ArgoCD Notifications,          |
            |   SealedSecrets, Vault)          |
            +----------------------------------+
```

**컨버전스 루프 알고리즘 (의사코드):**

```python
def reconciliation_loop(interval_sec=180):
    while True:
        desired = git_pull(revision="HEAD", path="manifests/")
        actual  = k8s_api.list_all_resources()

        diff = compute_diff(desired, actual)
        # diff = (Missing, Modified, Orphaned, Healthy)

        if diff.has_drift():
            if self_heal_enabled:
                apply(desired)         # GitOps 에이전트가 자동 교정
                log_audit(diff, actor="gitops-operator")
            else:
                notify(diff)           # Slack/Alertmanager 알림

        if diff.has_orphaned():
            prune(orphaned)            # Git에서 사라진 리소스 정리

        sleep(interval_sec)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Git Repository (SoT)** | 모든 선언적 상태의 진실의 원천. 인프라, 애플리케이션, 정책, Secret 템플릿의 **유일한 마스터**. | GitOps의 핵심은 Git의 **불변성(Immutability)**과 **분기 모델(Branching Model)** 활용. `main` -> staging, `release/x.y` -> production 같은 **Environment Branching**, 또는 `main` 단일 + Argo CD **ApplicationSet**의 `environment` 오버레이 패턴. Branch Protection Rule로 **필수 리뷰어(CODEOWNERS)**, **서명된 커밋(Signed Commits, GPG/SSH Sigstore)**, **상태 체크(Status Check, OPA/Gatekeeper, Conftest) 통과** 필수화. |
| **GitOps Operator (Agent)** | 클러스터 내부에서 동작하며 Git Repository를 주기적으로 **Polling**(기본 3분) 또는 **Webhook**으로 감지하여, 선언적 상태를 클러스터에 **Apply/Sync**하고 **Drift**를 자동 교정(Self-heal)한다. | **Argo CD** (CNCF Graduated): Application CRD 기반으로 다중 클러스터 동기화, Web UI 제공, SSO/OIDC 통합, App of Apps 패턴. **Flux CD** (CNCF Graduated): GitOps Toolkit 모듈화(Helm Operator, Kustomize Controller, Notification Controller,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 585 / 600

<- **이전**: [584. AIOps 지능형 IT 운영 자동화](/studynote/11_design_supervision/06_exam_summary/585_aiops_intelligent_it_operations/)
**다음**: [586. 서비스 메시 관측성 트래픽 제어](/studynote/11_design_supervision/06_exam_summary/586_service_mesh_observability_traffic_contr/) ->

---
