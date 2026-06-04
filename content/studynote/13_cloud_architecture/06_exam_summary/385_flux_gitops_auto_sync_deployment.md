---
title: "385. Flux GitOps 자동 동기화 배포 (Flux GitOps Auto Sync Deployment)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Flux v2는 GitRepository/OCIRepository/ HelmRepository 같은 **소스 CRD**를 Kustomize Controller·Helm Controller·Notification/Image-automation Controller가 **Pull 모델로 주기적 Reconciliation(기본 1m, 5m, 10m 가능)**하여 Git 선언 상태와 클러스터 Actual 상태를 **알고리즘적 Drift Detection + SSA(Server-Side Apply)**로 수렴시키는 CNCF Graduated GitOps Operator이다.
> 2. **가치**: 사람이 kubectl을 칠 수 없도록 **"Cluster Immutability"**와 **"Audit Trail"**을 강제하여 평균 MTTR 60%v, 잘못된 운영자의 수동 변경 100% 차단, SOPS/Mozilla SOPS + Age 키 또는 HashiCorp Vault를 통한 **Git 저장소 내 평문 Secret 0건**을 실현한다.
> 3. **판단 포인트**: 기술사적 관점에서는 **ArgoCD(명시적 Sync, App-of-Apps) 대비 "암묵적 reconcile + tenant 격리"**의 차이가 운영 복잡도·RBAC·멀티클러스터 모델 결정의 핵심이며, **Mono-repo vs Multi-repo / Hub-Spoke vs Standalone / Kustomize vs Helm** 조합이 시스템 품질을 좌우한다.

---

## Ⅰ. 개요 및 필요성

기존 Push 기반 CD(Jenkins, GitLab Runner, Spinnaker 등)는 빌드 에이전트가 클러스터의 kubeconfig을 들고 `kubectl apply`/`helm install`을 외부에서 실행하는 **Outbound 443/HTTPS** 위주 통신이다. 이 구조는 ① 클러스터 인증서를 빌드 파이프라인이 평문으로 관리해야 하고, ② Egress 방화벽을 일관되게 모두 개방해야 하며, ③ 누가 무엇을 언제 배포했는지가 **Git 히스토리와 분리된 컨테이너 런타임 로그**에만 남기 때문에 **감사·컴플라이언스·재현성**에서 취약하다. 동시에 마이크로서비스가 50~500개로 증가하면 `helm upgrade --install svc-a ...`을 수십 개 서비스에 수동으로 실행하는 운영 부담이 폭증한다(일반적으로 50개 서비스 이상에서 수동 배포는 인적 오류율 8~12% 발생).

Flux는 Weaveworks가 2017년 설계한 **GitOps 원칙(https://opengitops.org)**을 구현한 CNCF Graduated(2023.11) 프로젝트로, Git를 **"유일한 진실 공급원(Single Source of Truth)"**으로 두고 클러스터 내부에 상주하는 Operator가 Git을 **Pull**하여 상태를 강제 수렴시킨다. **Push-기반 CI 파이프라인은 "이미지 빌드·테스트·Git 커밋"까지만 관장**하고, 클러스터로의 반영은 Flux가 전담하는 **CI/CD 책임 분리**가 가능해진다.

```text
+------------------------------------------------------------------+
|             Push 기반 CD (Legacy) vs Pull 기반 GitOps (Flux)        |
+------------------------------------------------------------------+

  [Push: Jenkins/Spinnaker]                      [Pull: Flux v2]
  +---------------------+                       +---------------------+
  | Source Build Agent  |                       | Flux Source-Controller|
  | +-----------------+ |                       |  GitRepository CRD   |
  | | kubectl apply --+-+--[Egress 443]--------->|  (Poll/SHA watch)    |
  | | helm install   | |   k8s API Server     |  + HelmRepository     |
  | +-----------------+ |   (직접 호출)          |  + OCIRepository     |
  +---------------------+                       +----------+----------+
           |                                              | sync
           v                                              v
   +--------------+                              +--------------------+
   |  K8s Cluster |                              | Kustomize Controller|
   |  (인증서 노출)|                              |  apply + drift      |
   +--------------+                              |  detect (1m loop)   |
                                                 +----------+---------+
                                                            v
                                                  +--------------------+
                                                  |  K8s Cluster        |
                                                  |  (In-cluster, SAS)  |
                                                  +--------------------+
```

- **📢 섹션 요약 비유**: Push CD는 택배기사가 집 현관문 키를 들고 와서 "문이 어디죠?"라고 묻는 구조이고, Flux GitOps는 집 안에 **거울(Reconciler)**을 두어 자기 상태가 Git의 사진과 다르면 자동으로 옷(리소스)을 갈아입히는 **자동 맞춤 정장 시스템**이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Flux v2는 5개의 Core Controller + 1개의 CLI(`flux`)로 구성되며, 모두 **GitOps Toolkit** 위에 빌드되어 공통 `Reconciler` 인터페이스를 공유한다. 모든 컨트롤러는 **RequeueAfter = (Configured Interval) - (Processing Time)** 알고리즘으로 **Leader Election + Watch + Exponential Backoff**를 결합해 동작한다.

```text
+----------------------------------------------------------------------------+
|                        Flux v2 Multi-Controller Architecture               |
+----------------------------------------------------------------------------+

        +--------------------------------------------------------------+
        |                    Git Repository (Mono/Multi-repo)            |
        |  +----------+  +----------+  +----------+  +--------------+  |
        |  | base/    |  | overlays/|  | infra/   |  | apps/        |  |
        |  | (공통)   |  | dev/prod |  | crosscut |  | helm-values  |  |
        |  +----------+  +----------+  +----------+  +--------------+  |
        +-----------------------+--------------------------------------+
                                |  (1) Git clone / fetch (every 1m~1h)
                                v
   +--------------------------------------------------------------------+
   |  ① source-controller   --- GitRepository / HelmRepository /         |
   |      (events: Normal)        OCIRepository / Bucket                  |
   |                              Artifact { .revision, .metadata }      |
   |                              Checksum Algorithm: SHA256              |
   +--------------------+-----------------------------------------------+
                        |  (2) Artifact event
                        v
   +--------------------------------------------------------------------+
   |  ② kustomize-controller  --- Kustomization CRD                      |
   |      (apply: Server-Side Apply, ForceOwnership, prune=false)        |
   |      HealthChecks: livenessProbe / readinessProbe / .status.healthy |
   |      (Timeout default 60s, retries 5)                              |
   +--------------------+-----------------------------------------------+
                        |  (3) SourceReady / HealthEvent
                        v
   +--------------------------------------------------------------------+
   |  ③ helm-controller  --- HelmRelease CRD                            |
   |      - chart from HelmRepository (OCIRegistry <OCI://>)            |
   |      - values: ./values.yaml + valuesFrom (ConfigMap/Secret)       |
   |      - DriftDetection: { .status.lastDriftObservedAt }              |
   |      - 3-way diff: manifest vs live vs cluster                      |
   +--------------------+-----------------------------------------------+
                        |  (4) status: ready / not-ready / failed
                        v
   +--------------------------------------------------------------------+
   |  ④ notification-controller  --- Provider(Generic/Slack/Teams)       |
   |      Alert / Commit Status (GitHub/GitLab)         |
   |  ⑤ image-automation-controller -- ImageRepository + ImagePolicy     |
   |      (semver / glob / regex)  -> Git write-back commit               |
   +--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Source Controller** | 외부 선언(소스)을 **Artifact**로 추상화 | `GitRepository.spec.interval=1m0s`, `ref: { branch: main }`, **OCI Artifact per Chart**(Helm 4 지원), Git의 `.git/HEAD` SHA를 256-bit fingerprint로 캐시하여 변경 감지 |
| **Kustomize Controller** | Kustomize Overlay를 **서버측 병합·적용** | `Kustomization.spec.sourceRef`, `path: ./overlays/prod`, `prune: true`, `force: true`, `wait: true`, `healthCheckExpr: "..."` (CEL 표기), `targetNamespace` (멀티테넌트) |
| **Helm Controller** | Helm 3 차트를 **3-way Strategic Merge Patch**로 적용 | `chartRef`, `valuesFrom: [{ kind: Secret, name: db-creds }]`, `install.timeout: 5m`, `upgrade.cleanupOnFail: true`, `driftDetection.enabled: true` (default) |
| **Notification Controller** | Git 이벤트 ↔ Receiver 양방향 | `Provider(Slack, GitHub, GitLab)`, `Alert: on-call`, `Receiver: webhook`, GitHub Checks API로 **flux-status-progressive-rollout** 게이트 구현 |
| **Image Automation Controller** | 컨테이너 레지스트리 감시 -> Git PR 생성 | `ImageRepository(regex)` + `ImagePolicy(semver: "^1.2.x")` -> `ImageUpdateAutomation(git: { branch: automations } -> PR/CI)` 조합으로 **CI-Free 자동 버전업** |
| **CLI: flux** | 선언적 설치·검증·부트스트랩 | `flux bootstrap github|gitlab|azure` (≥v2.0, v2.3+는 **OCI Bootstrap** 지원), `flux build kustomization`로 dry-run, **fluxcd/flux-cli**에 정책 검증 내장 |

**핵심 Reconciliation 알고리즘**

```
1. watch Source artifact (revision 변경 감지)
2. compute Diff = Desired(rendered) - Actual(cluster)
3. if diff != ∅  ->  server-side apply(forceOwnership=true, prune=true)
4. wait health = True (timeout 60s × retry 5 = 5m)
5. post Notification Event  ->  emit metrics (Prometheus :9780)
6. requeueAfter = interval - (now - lastHandleStartTime)
```

기술사적 관점에서 **forceOwnership=true + prune=true**는 가장 위험하면서 강력한 옵션이다. `forceOwnership=true`는 Flux가 annotation `kustomize.toolkit.fluxcd.io/name`을 키로 동일 매니페스트의 이전 소유자(kubectl apply, 다른 컨트롤러)를 **무력화**시키므로, 멀티툴 환경 충돌 시 단일 책임 원리를 강제하는 안전장치이자 동시에 권한 분쟁의 원인이 된다.

**GitOps 매니페스트 패턴 — Kustomization CRD 실전 예시**

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata: { name: apps-prod, namespace: flux-system }
spec:
  interval: 5m0s
  sourceRef: { kind: GitRepository, name: apps }
  path: ./overlays/prod
  prune: true
  wait: true
  timeout: 3m0s
  healthChecks:
    - apiVersion: apps/v1
      kind: Deployment
      name: api-gateway
      namespace: prod
  dependsOn: [{ name: cluster-addons }]      # 의존성 DAG
  postBuild:                                    # 이미지 자동 교체
    substituteFrom:
      - kind: ConfigMap
        name: cluster-vars
    substitute:
      cluster_name: prod
      replicas: "8"
```

- **📢 섹션 요약 비유**: Source Controller는 **우체국**이고(택배 분류), Kustomize/Helm Controller는 **요리사**(레시피=Kustomization을 보고 실제 요리=리소스를 만들고, 손님 상태=헬스체크를 확인), Notification Controller는 **식당 매니저**(손님 불만 알림), Image Automation은 **식재료 주문 자동화 로봇**이다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Flux v2 (CNCF Graduated)** | **Argo CD (CNCF Graduated)** | **Jenkins X / Tekton (Push CD)** |
| :--- | :--- | :--- | :--- |
| 동기화 모델 | **암묵적 Pull (default 1m)** | 명시적 `Sync` 버튼 + Webhook Trigger | Push (CI Job에서 kubectl/helm) |
| 상태 수렴 | `Reconciliation loop` 자동 (5m SLA) | 자동(Sync Window 설정) / 수동 하이브리드 | 일회성 apply, 재수렴 없음 |
| 멀티클러스터 | **Hub-Spoke: AppSet + Cluster API**(Flux v2.1+) | **App of Apps + ApplicationSet Generator** | 어려움 (Jenkins slave가 각각 cluster 인증 필요) |
| 렌더링 엔진 | Kustomize + Helm + **SOPS + Age** | Kustomize + Helm + Ksonnet(legacy) | Helm / Kustomize / 자유 |
| Secret 관리 | **SOPS-Age(권장) + Vault CSI / ESO** | Sealed Secrets / SOPS / External Secrets | HashiCorp Vault 외부 호출 |
| SSO / RBAC | **multi-tenancy locking**(0.x 시절의 tena-controller 통합), OIDC | Dex, RBAC ConfigMap, AppProject | Jenkins RBAC + 쿠버네티스 RBAC |
| Drift Detection | **Kustomize/Helm 양쪽 모두 SSA로 감지** | Diff 시각화 UI + 자동 Prune | 없음(apply 후 잊혀짐) |
| Web UI | 없음 (CLI + Grafana + Notifications) | **강력한 Web UI (Tree, Diff, Sync)** | Jenkins 자체 UI |
| App-of-Apps | `Kustomization.dependsOn` DAG | ApplicationSet PR Generator | Jenkinsfile Pipeline |
| 라이선스 | Apache-2.0 (FluxCD 사) | Apache-2.0 (Intuit 사) | Mixed (Jenkins MIT, Tekton Apache) |
| **적합 시나리오** | 50+ 마이크로서비스, 멀티클러스터, GitOps-first 조직 | **소수의 DevOps 엔지니어가 UI로 가시성**을 선호 | 기존 Jenkins 자산 보존 |

**연계 생태계**

- **Sealed Secrets / SOPS / ESO (External Secrets Operator)**: Git에는 Secret 평문을 커밋하지 않기 위한 표준. Flux는 **`flux create secret sops`** + `sops --age` 키 + `Kustomization.spec.decryption.provider=sops`로 **인-메모리 복호화**(평문이 API Server에 디스크로 저장되지 않음).
- **Cluster API (CAPI)**: Flux는 **cluster-api-provider-flux(CAPF)**로 CAPI ControlPlane/WorkerBootstrap 참조 시 **Machine Health Check** 결과를 Git에 자동 commit하여 **GitOps 멀티클러스터 라이프사이클** 전체를 자동화.
- **Argo Rollouts / Flagger**: Progressive Delivery는 별도 CRD로 분리되어 있으며, Flux는 **`postBuild.substitute`**로 카나리 1% -> 10% -> 50% -> 100% 단계의 Image tag를 Git에 단계적 commit -> Helm/Kustomize가 자동 반영.
- **HashiCorp Vault**: `Agent Sidecar Injector` + Flux의 `valuesFrom: Secret` 조합. **CSI Secret Driver**도 동일 패턴.
- **GitHub/GitLab Webhook**: `webhookEnabled: true` + `secretRef`로 Push 즉시 Reconciliation(기본 1m 폴링에서 100~300ms로 단축).

| 통합 대상 | 연결 포인트 | 주의사항 |
| :--- | :--- | :--- |
| Prometheus | `flux-system` Pod `9780/metrics` -> ServiceMonitor | `flux_kustomize_status_condition{status="False"}` 알람 필수 |
| Grafana | `fluxcd/flux2-grafana-dashboards` 공식 | Notification Controller 메트릭은 별도 `9781/metrics` |
| OPA / Kyverno | Kyverno `validateKustomization`로 정책 강제 | CRD 기반 제어가므로 Rego보다 **CEL/CEL-based admission** 사용 권장 |
| OpenCost | Image Automation으로 인한 스케줄링 변경 추적 | `flux_image_policy_last_pushed_image_age_seconds` 메트릭 활용 |

- **📢 섹션 요약 비유**: Argo CD는 **자판기**(버튼 누르면
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 385 / 800

<- **이전**: [384. ArgoCD GitOps 선언적 지속 배포](/studynote/13_cloud_architecture/06_exam_summary/384_argocd_gitops_declarative_continuous_delivery/)
**다음**: [386. 카나리 배포 Flagger 프로그레시브](/studynote/13_cloud_architecture/06_exam_summary/386_canary_deployment_flagger_progressive_deliver/) ->

---
