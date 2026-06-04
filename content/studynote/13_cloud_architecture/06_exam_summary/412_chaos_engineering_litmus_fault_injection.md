---
title: "412. 카오스 엔지니어링 리트머스 장애 주입 (Chaos Engineering Litmus Fault Injection)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 리트머스(Litmus)는 CNCF 인큐베이팅 프로젝트로서 Kubernetes CRD(ChaosEngine, ChaosExperiment, ChaosResult)를 선언적으로 활용하여 Pod·Node·Application·Cloud Platform 4계층에 걸쳐 Pod Delete, CPU/Memory Hog, Network Latency/Loss/Corruption, DNS, Disk I/O Stress, JVM Stress 등 약 50여 종의 표준화된 Fault를 주입하고, Probe(httpreq, k8sExec, prometheus, cmdProbe, dataplane, logGql) 메커니즘으로 정상 상태(Steady State)를 자동 검증·판정하는 Cloud-Native 카오스 실험 프레임워크이다.
> 2. **가치**: 사전(Pre-mortem) 장애 시뮬레이션을 통해 MTTR(Mean Time To Recovery)을 평균 30~50% 단축시키고, SLO(Service Level Objective) 침해 시나리오를 Production-like 환경에서 자동 회귀 테스트하여 Resilience-as-Code를 실현하며, 조직 차원의 Game Day 운용을 통해 Incident Response 절차의 실효성을 검증·개선할 수 있다.
> 3. **판단 포인트**: CRD 의존성으로 인한 초기 학습 곡선 및 Helm Chart/Custom Resource 버전 업그레이드 호환성, ChaosHub 외부 의존 시 Hub可靠性(Reliability) 확보 문제, 멀티 클러스터 환경에서 Litmus Portal의 Self-signed 인증서/SSO 통합 정책, Blast Radius·Probe Threshold 임계치 부적절 설정 시 Production Cascade Failure 위험, eBPF 기반 커널 레벨 침투 실험(Litmus 2.x의 libNetwork/Network Chaos 정밀화) 시 성능 오버헤드를 종합적으로 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

카오스 엔지니어링(Chaos Engineering)은 Netflix가 2011년 AWS 인프라 이전 직후 발생했던 연쇄 장애를 계기로, 단순한 Reactive 사고 대응에서 벗어나 **사전에 시스템의 회복탄력성(Resilience)을 과학적으로 검증**하기 위해 도입한 방법론이다. 카오스 엔지니어링의 4대 원칙(CNCF Chaos Engineering White Paper 기준)은 ① 정상 상태(Steady State) 정의, ② 가설(Hypothesis) 수립, ③ 실험 변수 격리, ④ Production 환경 실험이다. 2024년 CNCF Survey에 따르면 응답 기업의 47%가 이미 카오스 엔지니어링을 운영 환경 일부에 적용하고 있으며, Kubernetes 기반 클라우드 네이티브 환경의 보편화로 인해 컨테이너·Pod·Service Mesh 레이어까지 침투 가능한 도구의 수요가 폭증했다.

기존의 전통적 장애 테스트(Disaster Recovery Test, Load Test)와 결정적으로 다른 점은, **"시스템이 어떻게 실패하는가"를 시스템 운영 중 능동적으로 탐색**한다는 것이다. 전통적 테스트가 미리 정의된 시나리오(스크립트 기반)를 검증하는 데 그쳤다면, 카오스 엔지니어링은 **알려지지 않은 실패 모드(Unknown-Unknowns)**를 발견하기 위한 탐색적 실험이다. 예컨대, 2020년 Cloudflare大规模 장애 사례 분석에서 보면, 단순한 Pod Delete 실험만으로도 ReplicaSet이 5분 이상 Pending 상태에 머무르는 케이스, DNS Resolver 캐시 오염으로 인한 503 폭증, Service Mesh Sidecar 메모리 누수 시나리오 등이 사전에 탐지될 수 있다.

리트머스(Litmus)는 2017년 MayaData(VARaaS로 출발, 후 CNCF에 기증)에서 개발을 시작하여 2020년 CNCF Sandbox로, 2024년 현재 Incubating 단계로 승격된 **Cloud-Native 카오스 엔지니어링 플랫폼**이다. Gremlin(상용 SaaS), Chaos Monkey(Netflix, 단순 인스턴스 종료만 가능)와 달리, 리트머스는 **Kubernetes Operator 패턴 + CRD**를 채택하여 GitOps 친화적이며, 약 50여 종의 Pre-built Experiment를 **ChaosHub**(Git 기반 카탈로그)를 통해 버전 관리·배포한다. 한국 시장에서는 금융권의 Kubernetes 전환 가속화, 공공 클라우드 MSA 전환 사업에 발맞추어 리트머스를 활용한 회복탄력성 검증 사례가 2023~2024년 사이 급증하고 있다.

```text
+--------------------------------------------------------------------+
|           Chaos Engineering의 4단계 실험 사이클 (실시간)             |
|                                                                    |
|  +----------+    +----------+    +----------+    +----------+     |
|  | ①Steady  | -> | ②Hypoth- | -> | ③Inject  | -> | ④Verify  |     |
|  |  State   |    |  esis    |    |  Fault   |    | Outcome  |     |
|  | 정의     |    |  수립    |    |  주입    |    |  검증    |     |
|  +----+-----+    +----+-----+    +----+-----+    +----+-----+     |
|       |               |               |               |            |
|  HTTP RPS,       "Pod N개 삭제       ChaosEngine   Probe(HTTP,   |
|  P99 Latency,    후에도 RPS가         CR 적용        K8s, Prom,   |
|  Error Rate      5% 이내 감소"     (kubectl apply)   SLO) 자동    |
|                                       kubectl     판정 -> Pass/    |
|                                       delete CR     Fail 기록     |
+--------------------------------------------------------------------+
              |
              v
   (반복) <----- 결과 분석 후 다음 실험 가설 갱신 --------+
```

- **📢 섹션 요약 비유**: 카오스 엔지니어링은 자동차 제조사가 출시 전에 충돌 테스트로 인명사고를 미리 재현·분석하는 것과 같다. 리트머스는 이 충돌 테스트 장비를 표준화·자동화하여, 클라우드 운영자가 매주 금요일마다 Production 차량으로 시험 주행을 돌리는 "Game Day"를 가능하게 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

리트머스 2.x는 두 개의 명확한 플레인(Plane)으로 분리된다. **Chaos Control Plane**(Litmus Portal, MongoDB/PostgreSQL, GraphQL API Server, SSO/Keycloak Auth)은 멀티 클러스터/멀티 테넌트 실험 오케스트레이션을 담당하고, **Chaos Execution Plane**(Chaos-Operator, ChaosRunner Sidecar, CRD Registry, ChaosEngine/ChaosExperiment/ChaosResult CRD)은 대상 클러스터 내 Fault 주입·Probe 검증·결과 수집을 수행한다. **ChaosHub**는 Git 저장소(github.com/litmuschaos/chaos-charts) 기반의 Experiment 카탈로그로, 약 50여 종의 Fault Template(lib.go, env.go, experiment.yaml)을 Helm Chart 형태로 제공한다.

**CRD(CRD = CustomResourceDefinition) 3종**의 역할은 다음과 같다. ① **ChaosExperiment CR**은 단일 실험의 정의(예: `pod-delete`)이며, Pod에 Mount되는 ChaosEngine에서 참조한다. ② **ChaosEngine CR**은 "어떤 App(APP_LABEL/APP_NAMESPACE)에 어떤 Experiment를 어떤 강도(TUNABLES: TOTAL_CHAOS_DURATION, CHAOS_INTERVAL, FORCE, PODS_AFFECTED_PERC)로, 어떤 Probe를 적용해 실행할지"를 정의하는 **결합 바인더(Binder)**이다. ③ **ChaosResult CR**은 Probe Pass/Fail 상태, 이벤트 로그, Steady State 검증 결과를 cluster-scoped로 저장한다.

**Probe 시스템**은 카오스 엔지니어링의 "성공/실패 판정"을 자동화하는 핵심 메커니즘으로, 5가지 타입을 제공한다. ① **httpProbe / httpsProbe**: Endpoint HTTP Status/응답 본문 검증, ② **k8sExecProbe**: 대상 Pod에서 임의 명령 실행 후 exit code 검증, ③ **promProbe**: Prometheus PromQL 질의 결과 임계치 판정, ④ **cmdProbe**: 외부 시스템(netcat, curl 등) 통한 TCP/HTTP 헬스 체크, ⑤ **dataplaneProbe**(Istio/Linkerd) / **logGqlProbe**(Grafana Loki 통합). **ProbeMode**는 `SOT`(Steady of Things, 실험 전 정상상태 확인), `EOT`(End of Things, 실험 후 회복 확인), `Edge`(실험 중 지속 검증), `Continuous`(지속 모니터링), `OnChaos`(Fault 주입 시점에만 검증) 등 5가지로, **SOT Pass -> Chaos Inject -> EOT Pass** 흐름이 정상 판정 조건이다.

```text
              [ Chaos Control Plane (중앙 관리 클러스터) ]
   +------------------------------------------------------------+
   |  +----------+  GraphQL  +----------+   JWT  +----------+  |
   |  | Litmus   | <------>  |  Litmus  | <--->  |  Auth    |  |
   |  | Portal   |  Apollo   |  Backend |        | Provider |  |
   |  | (React)  |  WS       |  (Go)    |        | (Keycloak|  |
   |  +----+-----+           +----+-----+        |  /Dex)   |  |
   |       |                      |               +----------+  |
   |       |                +-----v-----+                         |
   |       |                | MongoDB / |                         |
   |       |                |  Postgres |                         |
   |       |                +-----------+                         |
   +-------+----------------------------------------------------+
           |  Self-signed CA, ClusterScope Token
           v
   [ Chaos Execution Plane (대상 Target Cluster) ]
   +------------------------------------------------------------+
   |  +------------------+                                       |
   |  | Chaos-Operator   |  Watch CRs (Engine/Exp/Result)        |
   |  |  (Deployment)    |  -> Spawn Job                          |
   |  +--------+---------+                                       |
   |           |                                                 |
   |  +--------v---------+  mount  +--------------------+        |
   |  |  ChaosEngine CR  | <-----> |  ChaosRunner Pod   |        |
   |  |  + ChaosResult   |         |  (lib Litmus SDK)  |        |
   |  +--------+---------+         +---------+----------+        |
   |           |                             |                   |
   |           |  Ref ->                      | Fault APIs        |
   |  +--------v---------+         +---------v----------+        |
   |  | ChaosExperiment  | ------> |  Targets (Pods/    |        |
   |  |   CR (Helm)      |  Pull   |  Nodes/Apps/Infra) |        |
   |  +------------------+         +---------+----------+        |
   |                                          |                   |
   |                                +---------v----------+        |
   |                                |  Probes: http/k8s/ |        |
   |                                |  prom/cmd/dataplane|        |
   |                                +--------------------+        |
   +------------------------------------------------------------+
                                    |
                       +------------v-------------+
                       |  ChaosHub (Git Repo)      |
                       |  litmuschaos/chaos-charts |
                       |  - pod-delete, pod-cpu-   |
                       |  hog, pod-memory-hog,     |
                       |  pod-network-* (8종),     |
                       |  node-*, aws-*, gcp-*,    |
                       |  azure-*, kube-*, app-*   |
                       +--------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Litmus Portal (Frontend)** | 멀티 클러스터/멀티 실험 통합 대시보드, RBAC, 스케줄링 UI | React + Apollo Client, GraphQL WebSocket Subscription, Workflow Designer로 DAG 기반 실험 파이프라인 구성 |
| **Litmus Backend** | API/CRUD/워크플로우 실행 엔진, Probe 결과 집계 | Go + gqlgen GraphQL Server, MongoDB(Chaos Workflows·Schedules) / PostgreSQL 호환, ResultArchive로 ChaosResult 영구 저장 |
| **Auth Provider** | SSO/OAuth2/통합 인증, 멀티 테넌트 격리 | Keycloak·Dex·Okta·Auth0 플러그인, Image Registry Pull Secret과 Cluster Scope Token을 JWT로 안전하게 교환 |
| **Chaos-Operator** | CRD 라이프사이클 컨트롤러, ChaosEngine/Experiment 감시 | kubebuilder 기반 Operator SDK, Reconcile Loop에서 ChaosEngine Spec -> Job(ChaosRunner) 생성·삭제, Finalizer로 Result Cleanup |
| **ChaosRunner Pod** | 실제 Fault 주입 및 Probe 실행 주체, Experiment Driver | litmus-go Library(Lib/Custom Pod, Go v1.21+), Init
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 412 / 800

<- **이전**: [411. 포스트모템 장애 분석 재발 방지](/studynote/13_cloud_architecture/06_exam_summary/411_postmortem_failure_analysis_prevention/)
**다음**: [413. SRE 토일 자동화 운영 효율](/studynote/13_cloud_architecture/06_exam_summary/413_sre_toil_automation_operational_efficiency/) ->

---
