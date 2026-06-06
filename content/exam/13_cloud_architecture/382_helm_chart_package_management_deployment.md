---
title: "Helm Chart Package Management Deployment"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Helm은 Kubernetes의 **YAML 매니페스트를 Go Template + values.yaml 기반의 차트(Chart)로 패키징**하여, 동일 차트를 환경별(dev/stg/prod)로 재현 가능하게 배포하는 **CNCF Graduated 프로젝트 패키지 매니저**이며, `Release` 단위로 버전·롤백·히스토리 관리를 수행한다.
> 2. **가치**: 평균 30~150개에 달하는 K8s 리소스 묶음을 **단일 명령(`helm install/upgrade`)으로 원자적 배포**하고, **3-way Strategic Merge Patch**를 통해 `kubectl apply` 대비 결정론적(Deterministic) 업그레이드와 1초 내 롤백을 보장한다. GitOps(ArgoCD/Flux)와 OCI Registry 연동으로 **배포 자동화 파이프라인의 표준 패키징 레이어**를 형성한다.
> 3. **판단 포인트**: ① **Helm 2(Tiller) vs Helm 3(클라이언트 전용)** 마이그레이션 의사결정, ② **Umbrella Chart(전역 values 상속) vs Standalone Chart(차트별 독립)** 의존성 전략, ③ **Helm(템플릿 엔진) vs Kustomize(오버레이 엔진)** 패러다임 선택, ④ **Chart Signing + OCI Registry + RBAC** 3종 보안 통제 설계가 핵심 평가 항목이다.

---

## Ⅰ. 개요 및 필요성

Kubernetes 클러스터에 실제 서비스를 배포하기 위해서는 **Deployment, Service, ConfigMap, Secret, Ingress, HPA, NetworkPolicy, ServiceAccount, Role/RoleBinding, PDB** 등 최소 10~20종의 리소스를 상호의존적으로 정의해야 한다. 컨테이너 이미지 1개당 평균 12.4개의 K8s 오브젝트가 생성된다는 CNCF Survey(2023) 결과는 이 관리 부담을 정량적으로 뒷받침한다. **Raw YAML 매니페스트(2015~2017 시대)**는 환경별 중복(dev/stg/prod)·버전 누락·롤백 불가·변경 이력 불명이라는 4대 고질적 문제를 안고 있었으며, 이는 12-Factor App의 "Config 분리" 원칙과도 정면으로 충돌했다.

Helm(2016년 Deis의 Matt Butcher가 초기 릴리즈, 2018년 v3.0부터 CNCF 재단 인큐베이팅 -> 2020년 Graduated)은 이를 해결하기 위해 **"Chart = 패키지, Release = 인스턴스, Repository = 카탈로그"** 라는 3축 모델을 도입했다. Go Template의 `range`, `if`, `default`, `toYaml` 같은 함수로 매니페스트를 변수화하고, `values.yaml`로 환경별 오버라이드를 흡수하며, Helm 3부터는 클라이언트-사이드 렌더링 + **3-way Strategic Merge Patch**(last-applied-configuration, current, proposed 3개 스냅샷 비교)로 멱등성을 보장한다.

```text
[Helm 도입 전: Raw YAML 지옥]                   [Helm 도입 후: 차트 기반 패키징]
+-----------------------------+                +-----------------------------+
|  myapp-dev-deployment.yaml  |                |   myapp/                    |
|  myapp-stg-deployment.yaml  |   --->          |   +-- Chart.yaml            |
|  myapp-prod-deployment.yaml |                |   +-- values.yaml (default) |
|  myapp-dev-service.yaml     |                |   +-- values-dev.yaml       |
|  myapp-stg-service.yaml     |                |   +-- values-prod.yaml      |
|  myapp-prod-service.yaml    |                |   +-- templates/            |
|  + 6개 ConfigMap × 3 env    |                |       +-- deployment.yaml   |
|  + 9개 Secret  × 3 env      |                |       +-- service.yaml      |
|                             |                |       +-- _helpers.tpl      |
|  총 약 30+ 파일             |                |       +-- NOTES.txt         |
|  변경 시 30곳 동시 수정      |                |   (단일 차트 = 1개 패키지)  |
+-----------------------------+                +-----------------------------+
```

- **📢 섹션 요약 비유**: Raw YAML이 "공방에서 도자기 하나하나 손으로 빚는 것"이라면, Helm 차트는 **"석고틀(Chart)에 도자기 찰흙(values)을 갈아넣어 똑같은 모양의 그릇(Release)을 무한히 찍어내는 산업용 프레스"** 와 같다. 도자기의 색깔(values-dev/prod)만 바꾸면 형태는 항상 동일하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Helm 3의 클라이언트-사이드 아키텍처는 **Helm Client (v3.x 바이너리)** -> **Kubernetes API Server (kube-apiserver)** 의 2-tier 구조로 단순화되었다. Helm 2의 Tiller(클러스터 내부 컴포넌트)는 RBAC 충돌과 단일 실패점(SPOF) 문제로 제거되었다. 클라이언트는 `~/.kube/config`로 kubeconfig를 직접 읽어 `Create/Update/Patch/Delete` API를 호출하며, 차트 내 모든 리소스를 단일 **Release** 단위로 그룹화하기 위해 `app.kubernetes.io/managed-by=Helm` + `release-name` 레이블과 `secret/helm.sh/release.v1` 시크릿(Secret 기반 상태 저장)을 사용한다.

```text
[Helm 3 클라이언트 사이드 아키텍처]
                                  (1) helm install/upgrade
                                          |
                                          v
   +----------------------------------------------------------+
   |  Helm Client (helm CLI 3.13+)                             |
   |  +------------+  +--------------+  +------------------+  |
   |  | Chart      |  | Values Loader|  | Renderer         |  |
   |  | Loader     |-->| (override &  |-->| (Go template +   |  |
   |  | (OCI/HTTP) |  |  merge)      |  |  Sprig functions)|  |
   |  +------------+  +--------------+  +--------+---------+  |
   +---------------------------------------------+------------+
                                                | (2) kubeconfig 기반
                                                v
   +----------------------------------------------------------+
   |  Kubernetes API Server (kube-apiserver)                   |
   |   - 인증: ServiceAccount Token / kubeconfig               |
   |   - 인가: RBAC (Role/ClusterRole)                         |
   |   - Admission: OPA/Gatekeeper, PodSecurityAdmission       |
   +------------------+---------------------------------------+
                      | (3) etcd 트랜잭션 commit
                      v
   +----------------------------------------------------------+
   |  Cluster State (etcd)                                     |
   |   + Secret: sh.helm.release.v1.<release>.v<N> (상태저장) |
   |   + OwnerReference / Label: app.kubernetes.io/managed-by  |
   +----------------------------------------------------------+
                      ^                       ^
                      | (4) Release Read      | (5) Watch Loop
                      |                       |
   +------------------+-----------------------+---------------+
   |  helm list / helm history / helm rollback (Read-Only API) |
   +----------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Chart** | 패키지 단위 (디렉터리 or `.tgz`) | `Chart.yaml`(메타데이터: `apiVersion: v2`, `name`, `version: 0.1.0` SemVer), `values.yaml`(기본값), `templates/`(Go Template로 렌더링되는 K8s YAML), `charts/`(서브 차트 의존성), `files/`(raw 리소스), `templates/_helpers.tpl`(재사용 스니펫). OCI 1.1 표준(`oci://ghcr.io/org/charts`)을 통해 컨테이너 이미지와 동일 레지스트리에 차트 저장 가능. |
| **Release** | 클러스터에 배포된 Chart의 인스턴스 | Helm 3부터 `Secret` 오브젝트 `sh.helm.release.v1.<release>.v<revision>`에 **3-way merge 입력 3종**(original manifest, last-applied, current state) + 렌더링된 manifest를 JSON으로 직렬화 저장. 최대 히스토리 10개(기본, `--history-max`로 조정) 보관으로 `helm rollback`이 단순 Secret 읽기로 1초 내 완료. |
| **Repository** | 차트 카탈로그/배포 채널 | HTTP 서버 + `index.yaml`(차트 목록, URL, SHA256, version 매트릭스). `helm repo add stable https://...` 형태로 등록. OCI 전환 시 `oras`/`helm push`로 OCI Registry에 push. 예: Harbor 2.x, AWS ECR, GHCR 모두 OCI Helm 지원. |
| **Renderer** | Go Template + Sprig 함수 엔진 | `{{ .Values.replicaCount \| default 3 }}`, `{{- range .Values.ingress.hosts }}`, `{{ include "mychart.fullname" . }}` 등으로 K8s YAML 생성. `toYaml`, `b64enc`, `quote`, `nindent` 등 **150+ Sprig 함수** 사용 가능. `helm template ./mychart`로 로컬 렌더링 결과 미리보기 지원. |
| **Dependency (의존성)** | 다른 차트 재사용/합성 | `Chart.yaml`의 `dependencies: - name: postgresql version: "12.1.2" repository: https://charts.bitnami.com/bitnami`로 선언, `helm dependency update`로 `charts/`에 락파일(`Chart.lock`) 기반 다운로드. **Umbrella Chart**(전역 `values.yaml` -> 서브 차트 values 상속)와 **Library Chart**(`type: application` 대신 `library`, 템플릿만 export) 두 가지 고급 패턴 제공. |
| **Hooks** | 배포 lifecycle 특정 시점 개입 | `pre-install`, `post-install`, `pre-upgrade`, `post-upgrade`, `pre-delete`, `post-delete`, `test` 어노테이션(`helm.sh/hook-weight`, `helm.sh/hook-delete-policy: before-hook-creation`)으로 Job/Pod 실행. 예: DB 마이그레이션, ConfigMap 리로드 트리거, Chaos 테스트. |
| **3-way Strategic Merge** | 멱등성 보장 업그레이드 | kubectl의 2-way(현재 vs 신규) 대비, Helm 3는 ① original(첫 install manifest) ② last-applied(직전 manifest) ③ current(실제 클러스터 상태) **3개 스냅샷**을 비교해 사용자가 직접 수정한 필드는 보존, Helm이 배포한 필드만 업데이트, 삭제된 필드만 제거. |

**핵심 알고리즘: 3-way Strategic Merge Patch 의사코드**

```text
function threeWayMerge(original, lastApplied, current, proposed):
    for each field in proposed:
        if field not in lastApplied:        # Helm이 관리하지 않던 필드
            KEEP current[field]            # 사용자 수동 변경 보존
        else if field not in current:      # 사용자가 리소스에서 제거
            DELETE from proposed
        else if deepEqual(lastApplied[field], proposed[field]):
            APPLY proposed[field]          # Helm 의도 반영
        else if not deepEqual(current[field], proposed[field]):
            KEEP current[field]            # 사용자 드리프트 보존
            LOG warning
    return patched manifest
```

- **📢 섹션 요약 비유**: 3-way merge는 **"교과서(original)", "학생이 펜으로 밑줄 친 책(last-applied)", "수정본이 적힌 칠판(current)", "교사가 새로 짠 강의안(proposed)"** 4권을 비교해 **칠판에 적힌 정답은 건드리지 않고, 교사가 새로 짠 부분만 업데이트하는** 스마트한 채점 방식이다. 학생이 칠판에 쓴 오답은 보존된다.

---

## Ⅲ. 비교 및 연결

Helm은 단독으로 쓰이기보다 **GitOps(ArgoCD/Flux)**, **Kustomize**, **Terraform**, **Operator 패턴**과 경쟁/보완 관계를 형성한다. 기술사 시험 관점에서는 **"왜 이 프로젝트에 Helm을 도입하는가?"** 의 정당화를 위해 비교 분석 능력이 필수다.

| 구분 | **Helm (v3)** | **Kustomize** | **Kubectl + Shell** | **Operator (CRD+Controller)** |
| :--- | :--- | :--- | :--- | :--- |
| **패러다임** | 템플릿 엔진 (Templating) | 오버레이 엔진 (Patch 누적) | 명령형 절차 스크립트 | Custom Controller + CRD |
| **환경 분리** | `values-{env}.yaml` + `--values` / `--set` | `overlays/dev/`, `overlays/prod/` 디렉터리 분기 | `if [ "$ENV" = "prod" ]; then sed -i ...` | CRD Spec의 `env` 필드 |
| **패키지 단위** | Chart (1개 디렉터리/`.tgz`) | kustomization.yaml 루트 | 없음 (수동 묶음) | CRD (Kubernetes-native) |
| **롤백/히스토리** | `helm rollback` (Secret 기반, N개 보관) | Git revert (속도 느림) | 수동 백업 필요 | Controller의 status에 의존 |
| **의존성 관리** | `Chart.yaml dependencies` + `helm dependency update` | 없음 (Base는 직접 import) | 없음 | CRD 참조로 표현 |
| **학습 곡선** | 중간 (Go Template 문법 필요) | 낮음 (YAML 패치) | 낮음 (그러나 멱등성 깨짐) | 높음 (Go/Rust 코딩) |
| **적합 시나리오** | 멀티 서비스/멀티 환경 패키지 배포 | 단순 환경별 오버레이, K8s 리소스 보강 | 일회성 PoC, 학습용 | Stateful/도메인 특화 자동화 (DB, MQ) |
| **GitOps 통합** | ArgoCD/Flux 모두 Helm Application/Source 지원 | Kustomize 네이티브, Helm보다 가벼움 | 약함 | Operator SDK 자체가 자동화 |
| **보안** | Chart Provenance (GPG), OCI Registry RBAC | 순수 YAML (서명 별도) | 없음 | ADMISSION WEBHOOK으로 자체 통제 |

**연계 생태계 상세**

1. **Helm + ArgoCD**: ArgoCD는 `Application.spec.source.helm` 필드로 Helm 차트를 직접 해석한다. `valueFiles: ["values-prod.yaml"]`, `parameters: [{name: replicaCount, value: "5"}]`로 GitOps의 선언적 모델과 Helm의 패키징을 결합. Helm Hook는 ArgoCD가 `PreSync/Sync/PostSync` 단계로 매핑.
2. **Helm + OCI Registry**: Helm 3.8+부터 `helm registry login ghcr.io` -> `helm push myapp-1.0.0.tgz oci://ghcr.io/myorg/charts`로 컨테이너 이미지 저장소와 통합. 이미지 스캔(Trivy, Grype) 도구 재활용 가능.
3. **Helm + Terraform**: Terraform의 `helm_release` 리소스(`hashicorp/helm` provider)로 K8s 클러스터 provisioning(Terraform) -> 차트 배포(H
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 382 / 800

<- **이전**: [381. 쿠버네티스 서비스 디스커버리 DNS CoreDNS](/studynote/13_cloud_architecture/06_exam_summary/381_kubernetes_service_discovery_dns_coredns/)
**다음**: [383. Kustomize 선언적 설정 관리 오버레이](/studynote/13_cloud_architecture/06_exam_summary/383_kustomize_declarative_config_overlay_manageme/) ->

---
