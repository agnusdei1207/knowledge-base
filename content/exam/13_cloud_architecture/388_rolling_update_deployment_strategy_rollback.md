---
title: "Rolling Update Deployment Strategy Rollback"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 롤링 업데이트(Rolling Update)는 k8s `Deployment.spec.strategy.rollingUpdate`의 `maxSurge`/`maxUnavailable` 파라미터 제어를 통해 구버전 ReplicaSet(Pod)을 점진적으로 Terminate하면서 신버전 ReplicaSet의 Pod을 1개씩 Ready 상태로 투입하는 무중단 배포 전략이며, 롤백(Rollback)은 이를 `kubectl rollout undo`, `RevisionHistoryLimit`에 저장된 이전 ReplicaSet 스냅샷으로 복원하거나 ArgoCD/FluxCD의 Sync Wave와 GitOps 기반 선언적 복원으로 수행하는 SRE 핵심 역량이다.
> 2. **가치**: Zero-Downtime 배포를 달성하면서 클라우드 비용을 Blue-Green 대비 50% 절감(별도 풀 환경 불필요), 롤백 MTTR을 30초~2분 이내로 단축(RevisionHistoryLimit=10 기본값, Helm revision=10), Progressive Delivery(Istio VirtualService weight 10%->50%->100%)를 결합 시 배포 실패로 인한 사용자 영향률을 0.01% 이하로 억제 가능.
> 3. **판단 포인트**: `maxSurge`/`maxUnavailable` 비율(절대값 vs 퍼센트), Readiness Probe 실패 시 트래픽 차단 지연, DB Schema와 애플리케이션 하위 호환성(Expand-Contract Pattern), StatefulSet의 `partition` 기반 순차적 롤백 vs Deployment의 비순차적 일괄 롤백, GitOps 환경에서 `syncPolicy.automated`의 self-healing vs 수동 override의 trade-off가 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 배포는 단순히 코드를 서버에 복사하는 행위가 아니라, **트래픽 라우팅**, **상태 보존**, **데이터 정합성**, **관측 가능성**이 동시에 만족되어야 하는 분산 시스템의 핵심 거버넌스 행위다. 전통적인 Recreate 전략(전체 인스턴스 동시 종료 후 재기동)은 100% 다운타임을 유발하여 MSA(Microservices Architecture) 환경에서 절대 사용할 수 없으며, 이를 대체하기 위해 등장한 것이 **롤링 업데이트(Rolling Update)**다.

롤링 업데이트는 N개의 인스턴스 중 일부(`maxUnavailable`)만 종료하고, 동시에 초과 가용 가능한 인스턴스(`maxSurge`)만큼 신버전 Pod을 투입해 전체 가용 용량(Capacity)을 유지하는 전략이다. 그러나 배포 자체보다 더 중요한 것이 **문제 발생 시 이전 안정 버전으로 되돌리는 롤백(Rollback) 메커니즘**이다. 기술사 관점에서 롤링 업데이트 롤백은 "단순 `kubectl rollout undo` 한 줄"이 아니라, **컨트롤러의 ReplicaSet 관리 모델**, **etcd의 리소스 버전 관리**, **Service의 Endpoints 셀렉터 일관성**, **Ingress Controller의 트래픽 재분배**, **DB 스키마 마이그레이션과의 결합도**, **GitOps Repository의 선언적 상태 복원**이 유기적으로 맞물린 복합 시스템 공학 문제다.

```text
+------------------------------------------------------------------+
|        롤링 업데이트 및 롤백의 3단계 거버넌스 라이프사이클         |
+------------------------------------------------------------------+
|                                                                  |
|  +--------------+    +--------------+    +--------------+        |
|  |  Stage 1     |    |  Stage 2     |    |  Stage 3     |        |
|  |  선언적 정의  |---->| 점진적 전개  |---->| 상태 검증    |        |
|  | (Declarative)|    | (Progressive)|    | & 롤백       |        |
|  +--------------+    +--------------+    +--------------+        |
|         |                    |                   |              |
|         v                    v                   v              |
|   +----------+         +----------+         +----------+         |
|   | Helm     |         | ReplicaSet|         | Probe/   |         |
|   | values   |         | maxSurge  |         | Metrics  |         |
|   | Git      |         | maxUnavail|         | Rollback |         |
|   | Manifest |         | Ready     |         | Trigger  |         |
|   +----------+         +----------+         +----------+         |
|                                                                  |
|  ① Helm Release  --->  ② k8s Controller  --->  ③ SRE/ArgoCD       |
|     (v1.2.0)              (Rolling)              (undo/sync)      |
+------------------------------------------------------------------+
```

기존 패러다임(CAPEX 중심의 물리 서버 + 수동 rsync 배포 + 야간 배포 윈도우 02:00~06:00) 대비, 현재의 롤링 업데이트/롤백 패러다임은 **(1) 선언적 인프라(Declarative Infra)**, **(2) 컨트롤러 루프(Reconciliation Loop)**, **(3) 불변 인프라(Immutable Infra + Container Image)** 라는 세 가지 패러다임 전환 위에 성립한다. 이로 인해 배포는 더 이상 "작업(Task)"이 아니라 "상태(State)"로 다루어지며, 롤백은 별도 작업이 아니라 "원하는 상태로의 회귀"로 자동화된다.

- **📢 섹션 요약 비유**: 레스토랑의 코스요리처럼, 앞접시(N=2개 테이블)는 아직 구메뉴를 먹고 있을 때 뒤편 주방에서는 신메뉴를 1테이블씩 준비해 살짝 들이밀고, 손님이 "이건 너무 짜다"(에러율 5% 초과)고 하면 재빨리 이전 메뉴로 바꾸는 셰프의 손길과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Kubernetes Deployment의 롤링 업데이트는 **Deployment Controller**가 `Deployment.spec.strategy.type=RollingUpdate`를 감지하면, 기존 ReplicaSet(구버전)의 `replicas`를 줄이고 신규 ReplicaSet(신버전)의 `replicas`를 늘리는 **비례 조정(Proportional Scaling)**을 통해 수행된다. 핵심 알고리즘은 다음과 같다:

```
for each iteration (Rollout):
  desired_newRS = min(desired_newRS + maxSurge, total_replicas)
  old_terminated = total_replicas - (oldRS.replicas - maxUnavailable)
  ① maxSurge 만큼 신규 Pod 생성 (Pending -> ContainerCreating -> Running)
  ② Readiness Probe 통과 시 Service Endpoints에 등록
  ③ maxUnavailable 만큼 구버전 Pod Terminate (SIGTERM -> gracePeriod 30s)
  ④ 진행률(rollout status) = newRS.ReadyReplicas / total_replicas
  ⑤ 100% 도달 시 Rollout Complete, 이전 ReplicaSet 보존(revisionHistoryLimit)
```

롤백 트리거는 크게 **(a) 자동(Auto)**과 **(b) 수동(Manual)**으로 나뉜다. 자동 트리거는 `progressDeadlineSeconds`(기본 600s = 10분) 내에 Rollout이 완료되지 않거나, `backoffLimit` 초과 시 Deployment Controller가 자동으로 `Progressing=False` 상태로 전환되며, Prometheus + Alertmanager의 `kube_deployment_status_observed_generation < spec_generation` 룰 기반 Slack PagerDuty 알림이 SRE의 롤백 의사결정을 유도한다. 수동 롤백은 `kubectl rollout undo deployment/<name> --to-revision=N`이 핵심이다.

```text
+------------------------------------------------------------------------+
|           Kubernetes Rolling Update + Rollback 상세 아키텍처            |
+------------------------------------------------------------------------+
|                                                                        |
|  +--------------+         +---------------------------------+           |
|  | Helm Chart   |         |  kube-apiserver (etcd backend)  |           |
|  | values.yaml  |----+    |  +--------------------------+   |           |
|  | image: v1.2  |    |    |  | Deployment Object        |   |           |
|  | replicas: 6  |    |    |  |  - spec.strategy         |   |           |
|  +--------------+    |    |  |  - status.observedGen    |   |           |
|                      v    |  |  - metadata.annotations  |   |           |
|               +----------+|  |    deployment.kubernetes |   |           |
|               | ArgoCD   ||  |    .io/revision: 5       |   |           |
|               | Sync     ||  +--------------------------+   |           |
|               | (GitOps) ||            |                    |           |
|               +----------+|            v                    |           |
|                      |    |  +--------------------------+   |           |
|                      |    |  | Deployment Controller    |   |           |
|                      |    |  |  (control-loop, 5s sync) |   |           |
|                      |    |  +--------------------------+   |           |
|                      |    |       |           |             |           |
|                      |    |       v           v             |           |
|                      |    |  +---------+ +---------+        |           |
|                      |    |  | RS v1.1 | | RS v1.2 |        |           |
|                      |    |  | (old)   | | (new)   |        |           |
|                      |    |  | pods: 4 | | pods: 2 |        |           |
|                      |    |  +---------+ +---------+        |           |
|                      |    +---------------------------------+           |
|                      |                    |                            |
|                      v                    v                            |
|         +----------------------------------------------+                |
|         |            Cluster & Data Plane              |                |
|         |  +------+ +------+ +------+ +------+         |                |
|         |  |Pod-1 | |Pod-2 | |Pod-3 | |Pod-4 |         |                |
|         |  |v1.1  | |v1.1  | |v1.2  | |v1.2  |         |                |
|         |  |Termin| |Ready | |Probe | |Ready |         |                |
|         |  |ating | |      | |Pass  | |      |         |                |
|         |  +--+---+ +--+---+ +--+---+ +--+---+         |                |
|         |     |        |        |        |             |                |
|         |     v        v        v        v             |                |
|         |  +----------------------------------+        |                |
|         |  |  Service (ClusterIP)             |        |                |
|         |  |  selector: app=payment, tier=fe  |        |                |
|         |  |  Endpoints: [Pod-2, Pod-3, Pod-4]|        |                |
|         |  +----------------------------------+        |                |
|         |                    |                        |                |
|         |                    v                        |                |
|         |         +----------------------+            |                |
|         |         |  Istio VirtualService|            |                |
|         |         |  weight: 90/10       |            |                |
|         |         +----------------------+            |                |
|         +----------------------------------------------+                |
+------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Deployment Controller** | 롤링 업데이트 오케스트레이션 | `client-go`의 Informer가 Deployment 오브젝트 watch, `desired = oldRS.replicas - x; newRS.replicas += x` 알고리즘으로 매 sync loop(기본 5~10초)마다 reconcile, `progressDeadlineSeconds=600` 초과 시 `Progressing=False` |
| **ReplicaSet (구버전/신버전)** | Pod 그룹 관리 및 revision 보존 | `pod-template-hash` 라벨로 각 버전 격리, `RevisionHistoryLimit=10`까지 보존(이전 10개 버전의 PodTemplate 스냅샷), `kubectl rollout history`로 확인 가능 |
| **Service + Endpoints Controller** | 트래픽 라우팅 게이트 | Endpoints Controller가 Readiness Probe `Ready=true`인 Pod만 Endpoints 객체에 등록, **Probe 실패 시 5~10초 지연** 발생 -> `initialDelaySeconds`, `periodSeconds` 튜닝 필수 |
| **Probe 시스템 (Liveness/Readiness/Startup)** | Pod 헬스 검증 | Liveness 실패 시 kubelet이 컨테이너 재시작, Readiness 실패 시 Service Endpoints에서 제거, Startup Probe는 초기화 시간이 긴 앱(WAS, ML 모델) 보호용 |
| **Helm / ArgoCD / FluxCD** | 선언적 배포 + GitOps 롤백 | Helm `helm rollback <release> <revision>`, ArgoCD `argocd app rollback <app> --revision=<git-sha>`, FluxCD는 Git Repository의 `HEAD~1`로 자동 sync |
| **Istio / Linkerd Service Mesh** | 트래픽 분할 (Canary) | VirtualService의 `weight: 90/10` 설정으로 신규 버전 10% 트래픽 -> 메트릭 분석 -> 50% -> 100% 단계적 이동, **mTLS 헤더 기반 세션 고정** 가능 |
| **CI/CD Pipeline (Jenkins/GitHub Actions)** | 자동화 게이트 | Argo Rollouts의 AnalysisTemplate + Prometheus 쿼리로 에러율 1% 초과 시 자동 abort, `kubectl argo rollouts abort` -> `kubectl argo rollouts undo` 체인 실행 |
| **Observability (Prometheus/Grafana/Loki)** | 배포 검증 데이터 | `http_requests_total{status=~"5.."}` / `histogram_quantile(0.99, ...)` 기반 SLO 검증, Tempo/Jaeger로 Trace 비교(v1.1 vs v1.2 latency) |

**핵심 파라미터 딥다이브**:
- `maxSurge`: 신규 Pod이 뜨는 동안 일시적으로 허용되는 초과 replicas. 기본 25%. 절대값(예: `2`) 또는 퍼센트(예: `25%`) 지정. **Node 자원(HPA, PDB)이 충분한지** 사전 확인 필수.
- `maxUnavailable`: 배포 중 허용되는 unavailable Pod 수. 기본 25%. **이 값을 0으로 두면 maxSurge만큼 무조건 두 배 자원이 필요**하므로 클러스터 용량 계획이 핵심.
- `progressDeadlineSeconds`: 기본 600초(10분). 신버전 Pod이 Ready가 되지 않거나 신규 ReplicaSet이 progress를 못 하면 DeploymentCondition `Progressing=False`로 마킹되어 향후 자동 롤백 트리거의 시그널이 됨.
- `revisionHistoryLimit`: 보존할 이전 ReplicaSet 수. 기본 10. 이 값만큼 `kubectl rollout undo --to-revision=N` 가능. 너무 크면 etcd 메모리 압박, 너무 작으면 롤백 옵션이 줄어듦.
- `terminationGracePeriodSeconds`: SIGTERM 후 SIGKILL까지 대기 시간. 기본 30초. 롤백 시 in-flight 요청이 `preStop hook`(`sleep 15; nginx -s quit`)으로 안전하게 drain되도록 튜닝.
- `Argo Rollouts`: `pause.duration`으로 단계별 휴면, `analysis.successCondition: result[0] < 0.01` 조건으로 자동 승격/중지, **`abortScaleDownDeadlineSeconds`**로 abort 시 이전 ReplicaSet 즉시 scale-down 또는 보존 결정.

**알고리즘 핵심 — Reconciliation 수식**:
```
if (newRS.replicas < desired) && (availableReplicas + maxSurge >= desired) {
    create new Pod;
} else if (oldRS.replicas > 0) && (availableReplicas > desired - maxUnavailable) {
    delete old Pod;
}
```

- **📢 섹션 요약 비유**: 자동변속기 차량의 기어 변속처럼, 한 번에 1단씩 부드럽게(v1.1 -> v1.2) 바꾸면서 엔진 RPM(트래픽)은 절대 멈추지 않게 하고, 승차감이 좋지 않으면(에러율 증가) 즉시 이전 기어로 복귀(롤백)하는 ECU(Electronic Control Unit, =Deployment Controller)의 정밀 제어와 같다.

---

## Ⅲ. 비교 및 연결

롤링 업데이트 롤백은 단독 기술이 아니라 **Progressive Delivery**라는 큰
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 388 / 800

<- **이전**: [387. 블루그린 배포 무중단 전환 전략](/studynote/13_cloud_architecture/06_exam_summary/387_blue_green_deployment_zero_downtime_switch/)
**다음**: [389. A/B 테스팅 트래픽 분할 실험](/studynote/13_cloud_architecture/06_exam_summary/389_ab_testing_traffic_splitting_experiment/) ->

---
