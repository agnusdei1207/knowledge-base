---
title: "Kubernetes Operator Custom Resource Definition"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CRD(Custom Resource Definition)는 Kubernetes API 서버에 새로운 리소스 타입(`Kind`)을 등록하는 **OpenAPI v3 Schema 기반의 선언적 확장 메커니즘**이며, Operator는 이를 `Spec`(요청 상태)과 `Status`(관찰 상태)의 차이를 **Reconcile Loop**로 수렴시키는 Control-Loop 패턴이다.
> 2. **가치**: Stateful 워크로드(etcd, PostgreSQL, Kafka 등)의 Day-2 운영(백업, 업그레이드, 페일오버, 스케일링)을 **사람의 개입 없이 코드화(Operator as SRE)**하여 MTTR을 평균 60~80% 단축하고, 도메인 지식을 Operator 코드에 캡슐화하여 팀 간 운영 표준화를 달성한다.
> 3. **판단 포인트**: CRD의 `scope`(Namespaced vs Cluster), `conversion`(v1beta1->v1), `structural schema`, `subresources(status)`, `printColumns` 결정, 그리고 `controller-runtime` vs **Operator SDK(Ansible/Helm/Go)** vs **KOPF** vs **kubebuilder** 프레임워크 선택이 아키텍처의 확장성과 가독성을 좌우한다.

---

## Ⅰ. 개요 및 필요성

기존 Kubernetes는 `Pod`, `Deployment`, `Service` 등 범용 리소스만 제공하여, **Stateful·분산 시스템**(etcd, Redis Cluster, Kafka, Elasticsearch, MySQL, Cassandra)을 배포·복구·업그레이드하려면 운영자가 수십 단계의 kubectl 명령어와 YAML을 직접 조합해야 했다. 이로 인해 *운영자의 휴먼 에러*, *환경 간 Drift*, *Knowledge Silo* 문제가 발생했다.

CRD는 Kubernetes 1.7에서 등장(v1.16에서 `apiextensions.k8s.io/v1` 안정화)하여, **API Aggregation 없이** 사용자가 직접 새로운 API 오브젝트(예: `KafkaCluster`, `Prometheus`, `Certificate`)를 선언적으로 정의하고 `kubectl`로 관리할 수 있게 했다. 여기에 **Reconciliation Controller**를 결합한 **Operator Pattern**이 등장하면서(Kubernetes 1.13 이후 본격화), "코드로 표현된 SRE(Site Reliability Engineering)" 패러다임이 가능해졌다.

```text
[기존 방식: 수동 운영 (Imperative) vs 오퍼레이터 방식 (Declarative + Autonomous)]

  +----------+   수동 명령    +----------------------+
  | Operator | -------------> | etcd-1  etcd-2  etcd-3 |   <- 스케일링/백업/복구를
  | (Human)  |   kubectl ×N  |      (StatefulSet)     |      사람이 수십 번 입력
  +----------+              +----------------------+
         |
         |  + Operator Pattern
         v
  +----------------+  declarative YAML  +-------------------------------+
  | kafkaClusters. | -----------------> | Kafka Operator (Controller)    |
  | kafka.strimzi. |   spec:           |  +- Reconcile Loop             |
  |    io          |    replicas: 5    |  +- PVC / STS 생성             |
  +----------------+   storage: 100Gi |  +- ConfigMap 동적 갱신       |
        (CR)                            |  +- Rolling Upgrade 자동화     |
                                        |  +- Backup/Restore CRD 연동    |
                                        +-------------------------------+
                                                |
                                                v
                                        +-------------------------------+
                                        | HeadlessService + PVC × 5     |
                                        | + PodDisruptionBudget         |
                                        | + NetworkPolicy               |
                                        +-------------------------------+
```

기존 Stateful 워크로드는 **Operator가 없으면** "반쪽짜리 선언형"이었다. CRD는 이 격차를 메워 Kubernetes를 **"어떤 분산 시스템이든 배포 가능한 범용 컨트롤 플레인"**으로 격상시켰다.

- **📢 섹션 요약 비유**: CRD는 마치 **백화점에 새로운 '상품 카테고리'를 등록하는 것**과 같다. 백화점(Kubernetes)은 이미 진열대·재고·결제 시스템(API Server, etcd, RBAC)을 갖추고 있고, "와인 코너", "수제 케이크 코너"라는 새 카테고리(CRD)만 정의해두면 입점 브랜드(Controller)가 알아서 진열·관리를 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
[CRD 등록부터 객체 처리까지의 End-to-End 흐름]

  사용자(또는 GitOps)
       |  kubectl apply -f kafka.yaml
       |  (spec.replicas: 5)
       v
  +----------------------------------------------------------+
  | kube-apiserver (OpenAPI Registry)                        |
  |  +- CRD Schema(OpenAPI v3) 기반으로 spec 검증            |
  |  +- structural schema -> 모든 필드 타입 강제               |
  |  +- x-kubernetes-preserve-unknown-fields: false          |
  |  +- admission webhook(optional: conversion/defaulter)    |
  +----------------------------------------------------------+
       |  저장 (etcd)            Watch(Informer cache)
       v                                                  v
  +-----------------+                       +----------------------+
  | etcd            | <--------- Reconcile --->| Operator Pod          |
  | KafkaCluster/...|          (delta)       |  +- Controller(Go)   |
  | status:         |          ^             |  +- Workqueue        |
  |  readyReplicas:3|          |             |  +- Predicate(filter)|
  |  conditions:    | --Update--+             |  +- Leader Election  |
  +-----------------+                        +----------------------+
                                                       |
                                                       v
                                          +-------------------------+
                                          | 자식 리소스 생성/조절     |
                                          |  StatefulSet, Service,  |
                                          |  ConfigMap, Secret,     |
                                          |  ServiceMonitor, PDB     |
                                          +-------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **CRD (CustomResourceDefinition)** | API 확장 스키마 정의 | `group/versions/names.kind` 등록, `openAPIV3Schema`로 필드 타입·제약·default·enum 강제. `apiextensions.k8s.io/v1` 사용 시 `structural`·`pruning`·`conditions` 자동 활성화. |
| **Custom Resource (CR)** | 사용자 의도(Desired State) 객체 | `metadata.namespace` + `spec`(요청 상태) + `status`(관찰 상태)로 분리. `kubectl get kafka my-kafka -o yaml`로 조회. `kubectl explain kafka.spec.replicas`로 doc 제공. |
| **Controller / Operator** | Reconcile Loop 실행체 | `client-go`의 `Informer/Lister/Workqueue` 패턴. `Reconcile(ctx, req)` 함수가 `Spec`↔`Status` 차이를 **idempotent**(멱등)하게 수렴. 재실행은 객체 변경·`resyncPeriod`·자식 리소스 변경 이벤트에 트리거. |
| **API Server (apiserver)** | 스키마 검증·저장·조회 | CRD 등록 시 OpenAPI 문서가 동적 빌드되어 `kubectl` 자동완성, doc, validation에 활용. `subresources.status` 활성화 시 `spec`/`status`가 별도 URL로 분리되어 `kubectl scale` 등 표준 명령 호환. |
| **Webhook (Admission/Conversion)** | 외부 검증·변환·기본값 | `validatingAdmissionWebhook`(예: 카탈로그 도메인 규칙), `mutatingAdmissionWebhook`(예: `inject sidecar`), `conversionReview`(`v1alpha1`↔`v1` 변환 webhook). |
| **Finalizer Controller** | 비동기 정리 보장 | `metadata.finalizers[]`에 토큰 등록 -> 리소스 삭제 시 컨트롤러가 정리(예: PVC 삭제, 외부 리소스 해제) 후 `finalizers` 제거해야 객체가 사라짐. 누락 시 객체가 영구 terminating. |
| **Operator Lifecycle Manager (OLM)** | 패키징·배포·업그레이드 | `ClusterServiceVersion(CSV)`, `Subscription`, `InstallPlan`, `CatalogSource`로 Operator 자체의 라이프사이클 관리. OLM 1.0(2024+)에서는 `ClusterExtension` API로 단순화. |
| **Controller Runtime / Operator SDK** | 프레임워크 | `controller-runtime`: cache/client/reconcile 추상화. `Operator SDK`: Helm/Go/Ansible 기반 스캐폴드. `KOPF`: Python용. `kubebuilder`: CRD+YAML 자동 생성. |

### 핵심 원리 ① — Reconcile Loop과 Level/Pod/Edge Triggered 트레이드오프

```text
    [이벤트 소스별 트리거 강도]

    Level-Triggered (kubectl apply 변경)        Edge-Triggered (Re-sync timer)
    +----------+                                +----------+
    | Spec 변경 |--- Reconcile() 호출 ----->      |  주기적   |--- Reconcile() 호출
    +----------+                                | 재동기화  |  (보통 10h)
                                               +----------+
       + 자식 리소스 변경 / Watches() / Indexer 기반 predicate
```

Operator는 **"level-triggered"(상태 기반)** 이어야 한다. 이벤트가 유실되어도 다음 reconcile에서 `Get()`으로 현재 상태를 재관찰하므로 자가 치유(self-healing)가 보장된다. 반대로 `Edge-Triggered`(이벤트 기반)만 의존하면 informer 재시작 시 이벤트 손실 -> Drift.

### 핵심 원리 ② — Spec / Status 분리 및 subresource 설계

```text
  apiVersion: kafka.strimzi.io/v1beta2     <-- group/version/kind
  kind: KafkaCluster                       <-- Plural: kafkaclusters, Short: kc
  metadata:
    name: my-cluster
    namespace: kafka
    finalizers: [kafkacluster.strimzi.io]  <-- 삭제 가드
  spec:                                     <-- 사용자가 "원함"
    kafka:
      replicas: 5
      version: 3.7.0
      storage:
        type: persistent-claim
        size: 100Gi
        class: gp3
    zookeeper:
      replicas: 3
  status:                                   <-- 컨트롤러가 "관측함"
    replicas: 3                              <-- subresource.status
    conditions:
      - type: Ready
        status: "True"
        lastTransitionTime: 2025-01-15T...
        reason: AllReplicasReady
    observedGeneration: 1
    phase: Recovering
```

`subresources.status`를 활성화하면 사용자가 `status`를 직접 변경하는 것을 차단하고(권한 분리), `kubectl scale`과 같은 표준 명령이 호환된다. `observedGeneration`은 컨트롤러가 마지막으로 본 `metadata.generation`(spec 변경 시 증가)을 기록하여 **drift 감지의 기준점** 역할을 한다.

### 핵심 원리 ③ — OpenAPI v3 Structural Schema 제약

| 제약 키워드 | 의미 | CRD에서의 효과 |
| :--- | :--- | :--- |
| `type: object` + `properties` | 구조 명세 | `pruning`이 자동으로 켜짐. 미선언 필드는 etcd 저장 시 제거(엄격). |
| `x-kubernetes-preserve-unknown-fields: true` | 알 수 없는 필드 보존 | `pruning` 비활성. 호환성 확보용, 사용 자제 권장. |
| `x-kubernetes-int-or-string` | `int`/`string` 모두 허용 | `quantity`, `replicas`에 자주 사용. |
| `x-kubernetes-validations: [...]`(CEL) | Common Expression Language 규칙 | Kubernetes 1.25+ `AdmissionReview`에서 **사이드카 없이** 자체 검증. 예: `self <= 100`. |
| `required: [replicas]` | 필수 필드 | 미입력 시 `kubectl apply` 거부. |
| `enum: [3.6, 3.7, 3.7.0]` | 허용 값 화이트리스트 | OpenAPI v3 검증으로 즉시 거부. |
| `default: 3` | 미입력 시 기본값 | admission 시 주입. |
| `format: int64`, `format: byte`, `format: date-time` | 직렬화 형식 | spec 상관없이 일관된 표현. |
| `additionalProperties: false` | 추가 키 금지 | schema에 정의되지 않은 key 차단. |
| `nullable: true` | null 허용 | Kubernetes 1.21+ 지원, 기존 호환 위해 신중히 사용. |

### 핵심 원리 ④ — Controller-Runtime Reconcile 구현 골격 (Go)

```go
func (r *KafkaClusterReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)

    // 1) Get CR (level-triggered: 항상 최신 상태로 Get)
    cr := &kafkav1.KafkaCluster{}
    if err := r.Get(ctx, req.NamespacedName, cr); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // 2) Finalizer 처리
    if !controllerutil.ContainsFinalizer(cr, finalizerName) {
        controllerutil.AddFinalizer(cr, finalizerName)
        return ctrl.Result{}, r.Update(ctx, cr)
    }
    if !cr.DeletionTimestamp.IsZero() {
        return r.cleanupExternalResources(ctx, cr)
    }

    // 3) 관측(Observation): 현재 실제 상태 수집
    actual, err := r.observeState(ctx, cr)
    if err != nil { return ctrl.Result{}, err }

    // 4) 비교(Compare): spec vs actual diff
    desired := r.desiredState(cr)

    // 5) 조치(Act): 자식 리소스 idempotent 생성/갱신
    if err := r.reconcileChildren(ctx, cr, desired, actual); err != nil {
        return ctrl.Result{RequeueAfter: 30*time.Second}, err
    }

    // 6) Status 업데이트 (subresource)
    cr.Status.Replicas = actual.ReadyReplicas
    cr.Status.ObservedGeneration = cr.Generation
    meta.SetStatusCondition(&cr.Status.Conditions, ...)
    return ctrl.Result{}, r.Status().Update(ctx, cr)
}
```

**핵심 기법**: ❶ 모든 reconcile은 **idempotent**(재실행 안전), ❷ 외부 시스템 호출은 **지수 백오프 + jitter**로 retry, ❸ `reconcile.Result{Requeue: true}` 또는 `RequeueAfter`로 다음 시도 예약, ❹ `predicate.GenerationChangedPredicate`로 spec 변경만 감지하여 불필요한 reconcile 폭주 방지.

- **📢 섹션 요약 비유**: Operator는 **"온도 조절기(thermostat)"**와 같다. 사용자가 25℃(spec)를 원하면, 조절기는 매 순간 현재 온도(status)를 측정하고 차이(delta)가 있으면 히터를 켜거나 끄는 것을 멈추지 않는다(Reconcile Loop). `Finalizer`는 "히터가 꺼지기 전 반드시 발열체를 식혀라"는 안전 절차다.

---

## Ⅲ. 비교 및 연결

| 구분 | **CRD (CustomResourceDefinition)** | **API Service (Aggregator)** | **Helm Chart (Templating)** | **Kustomize (Overlay)** |
| :--- | :--- | :--- | :--- | :--- |
| **API 확장 여부** | yes (네이티브) | yes (aggregation layer, e.g. metrics-server) | no (kubectl + go template) | no (kubectl + patch) |
| **상태(State) 보관** | `status` subresource로 명시적 보관 | 동일 | 없음 (릴리스 단위) | 없음 |
| **제어 루프(Reconcile)** | Operator 결합 시 가능 | 동일 | 없음(설치·업그레이드만) | 없음 |
| **검증 메커니즘** | OpenAPI v3 + CEL(1.25+) | OpenAPI 임의 | `helm template` 후 `kubectl apply
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 376 / 800

<- **이전**: [375. 쿠버네티스 시크릿 관리 볼트 연동](/studynote/13_cloud_architecture/06_exam_summary/375_kubernetes_secret_management_vault_integratio/)
**다음**: [377. 쿠버네티스 스케줄링 노드 어피니티 테인트](/studynote/13_cloud_architecture/06_exam_summary/377_kubernetes_scheduling_affinity_taint_tolerati/) ->

---
