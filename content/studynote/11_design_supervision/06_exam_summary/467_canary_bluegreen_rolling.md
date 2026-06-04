+++
title = "467. 카나리 배포 블루 그린 롤링 전략 (Canary Blue Green Rolling Deployment)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 카나리(Canary)·블루그린(Blue/Green)·롤링(Rolling) 배포는 **무중단 배포(Zero-Downtime Deployment)** 를 달성하기 위한 트래픽 라우팅 전략으로, 각각 **부분 노출 + 점진적 확대**, **이중 환경 + 원자적 스위치**, **순차적 인스턴스 교체** 라는 상이한 트래픽 전환 메커니즘을 가지며, 실제 운영에서는 **Istio VirtualService(weight 기반)**, **Kubernetes RollingUpdate Strategy**, **Argo Rollouts(AnalysisTemplate)**, **AWS CodeDeploy** 등을 통해 구현된다.
> 2. **가치**: 배포로 인한 가용성 손실을 99.99% 수준으로 끌어올리고, MTTR(Mean Time To Recovery)을 **수 분 이내로 단축**하며, A/B 테스트 및 점진적 트래픽 천이를 통한 **통계적 유의성 기반 품질 검증**이 가능해져 연간 수십억 원대의 장애 손실을 예방한다.
> 3. **판단 포인트**: 세 전략은 **리소스 2배 비용 vs. 즉각적 롤백**, **부분 노출 리스크 vs. 점진적 안전성**, **세션/DB 호환성** 이라는 상호 배타적 트레이드오프를 가지므로, 서비스의 **상태성 유무, 트래픽 패턴, RTO/RPO 요구사항, DB 마이그레이션 동시성** 을 기준으로 전략을 단독 또는 하이브리드(예: Blue/Green + Canary) 로 조합해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 **In-Place 배포(Recreate Strategy)** 는 옛 버전(Old ReplicaSet)을 모두 종료한 뒤 새 버전을 기동하기 때문에 **배포 구간에서 100% 서비스 중단**이 불가피하며, 롤백 시에도 동일 시간이 소요된다. 마이크로서비스 아키텍처(MSA)와 컨테이너 오케스트레이션(쿠버네티스, ECS)이 보편화되면서 **수 초 단위 컨테이너 기동**과 **선언적 배포 명세(Deployment Manifest)** 가 가능해졌고, 이를 활용하여 **사용자 트래픽을 무중단으로 전환**하는 3대 전략이 사실상 표준으로 자리 잡았다.

```text
[기존 In-Place 배포 (Recreate) vs. 고급 무중단 배포]

  (1) Recreate (전통 방식)              (2) 고급 무중단 배포 (Rolling/Blue-Green/Canary)

  +------------------+                  +------------------+
  |   Old Pod (v1)   |   -- STOP -->    |  Old Pod (v1)   |◄-------+
  |   Old Pod (v1)   |                  |  Old Pod (v1)   |       |
  |   Old Pod (v1)   |                  |  Old Pod (v1)   |       | 트래픽 유지
  +------------------+                  +------------------+       |
            v                              v  ^                    |
  +------------------+                  +------------------+       |
  |   (Service DOWN) |   <-- GAP -->    |  New Pod (v2)   |◄------+ 신규 트래픽 분산
  |  ✗ 5xx Error     |                  |  (점진적 증가)   |
  +------------------+                  +------------------+
  ❌ 다운타임 발생                        ✅ 무중단, 점진적 롤백 가능
```

기존의 **IDC(Internet Data Center) + VM(가상머신) + 수동 배포** 환경은 한 서버의 기동이 5~15분, LB(L4/L7) 설정 변경이 별도 작업 요청으로 처리되어 **하루 1회 배포가 한계**였다. 그러나 **Kubernetes + Helm + ArgoCD** 환경에서는 **롤링 업데이트(기본), Blue/Green, Canary** 가 **kubectl apply 한 줄**, 또는 **GitOps 기반 자동 동기화** 로 수 분 내 실행되며, 이를 통해 **DORA Metrics(배포 빈도·리드 타임·변경 실패율·MTTR)** 의 4대 지표를 모두 개선할 수 있다.

기술사적 관점에서 이 3가지 전략은 단순 배포 기법이 아니라 **릴리스 엔지니어링(Release Engineering)** 의 핵심으로, **가용성·확장성·관측가능성(Observability)·비용** 의 4축을 어떻게 조율할 것인지를 결정짓는 **아키텍처 의사결정 프레임워크** 라고 할 수 있다.

- **📢 섹션 요약 비유**: 옛날 공연(배포)은 무대(서버)를 닫고 새 소품으로 바꿔야 했지만(Recreate), 지금은 **무대를 닫지 않고도 무대 양쪽(Blue/Green)에서 번갈아 공연** 하거나, **관객 일부에게만 먼저 새 공연을 보여주고 반응을 살피는(Canary)** 방식입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 카나리 배포 (Canary Deployment)

새 버전을 **전체 트래픽의 1~10%** 에 해당하는 일부 인스턴스(또는 특정 사용자 그룹)에게만 노출하고, **에러율·응답시간·비즈니스 KPI** 를 실시간 비교한 뒤 점진적으로 비중을 확대(예: 1% -> 10% -> 25% -> 50% -> 100%)하는 전략이다. 핵심은 **동일 버전의 양쪽 환경이 동시에 운영**되며, **Service Mesh 또는 Ingress Controller** 가 **트래픽 가중치(weight)** 로 라우팅을 제어한다는 점이다.

```text
[Canary 배포 상세 흐름 - Istio VirtualService 기반]

                              [사용자 트래픽]
                                    |
                                    v
                          +---------------------+
                          |  Ingress Gateway /  |
                          |  Istio IngressGW     |
                          +---------------------+
                                    |
                          +---------+----------+
                          |  VirtualService    |
                          |  weight:           |
                          |   v1 -> 90%         |
                          |   v2 -> 10%         |
                          +---------+----------+
                                   |
                  +----------------+----------------+
                  v (90%)                            v (10%)
         +------------------+              +------------------+
         |  Stable (v1)     |              |  Canary (v2)     |
         |  Pod: 9 replica  |              |  Pod: 1 replica  |
         |  Service: stable |              |  Service: canary |
         +------------------+              +------------------+
                  |                                  |
                  +--------------+-------------------+
                                 v
                       +------------------+
                       |  Observability   |
                       |  - Prometheus    |
                       |  - Error Rate    |
                       |  - P99 Latency   |
                       |  - Business KPI  |
                       +------------------+
                                 |
                          +------+-------+
                          v              v
                  [정상] -> weight     [이상] ->
                  증대 (10->50->100)    kubectl argo rollouts abort
                                     -> v2 트래픽 0%로 차단
```

**핵심 파라미터:**
- `maxSurge`: 신규 Pod 최대 동시 기동 수 (예: 25%)
- `maxUnavailable`: 배포 중 정지 가능한 최대 Pod 수 (예: 0% -> 무중단)
- `Traffic Split`: 컨테이너 오케스트레이션 레벨이 아닌 **Mesh/Istio 레벨**에서 가중치 제어
- **AnalysisTemplate (Argo Rollouts)**: PromQL/Grafana 메트릭을 기반으로 자동 승격(automatic promotion) 또는 자동 abort

### 2. 블루/그린 배포 (Blue/Green Deployment)

**물리적으로 동일한 2개의 독립 환경(Blue=현재 운영, Green=신규)** 을 구성하고, 로드밸런서(또는 DNS, Service Mesh) 가 트래픽을 원자적(atomic) 으로 전환한다. 데이터베이스는 **공유(Shared DB) 또는 듀얼 라이트(Dual-Write)** 방식으로 처리한다.

```text
[Blue/Green 배포 상세 흐름]

         [Step 1: 사전 검증]              [Step 2: 스위치]              [Step 3: 롤백 가능 상태]

    사용자 --► L7 LB --► Blue(v1)      사용자 --► L7 LB --► Green(v2)    사용자 --► L7 LB --► Blue(v1)
    트래픽    100%       (Stable)       트래픽    0%   ^     (Stable)     트래픽    100%      (재활성화)
    (Old)                |Green 대기                | v                  (Rollback)
                         v                          v
                       Green(v2)                  Blue(v1)
                       Smoke Test                Warm-standby
                       Integration Test          (즉시 복귀 대기)

    +-------------------------+         +-------------------------+
    |   Blue (v1) - Active    |         |   Blue (v1) - Idle      | <- 즉시 재라우팅 가능
    |   Green (v2) - Standby  |         |   Green (v2) - Active   | <- 신규 운영
    +-------------------------+         +-------------------------+
```

**핵심 동작 원리:**
- **Route 53 / NLB** 의 Weighted Record Set 또는 **ALB Target Group** 의 가중치 변경으로 스위칭
- Green 환경은 **Idle 상태** 로 대기하다가, 1초 이내 모든 트래픽을 흡수할 수 있도록 **Warm Pool** 유지 (AWS에서는 EC2 Warm Pool, K8s에서는 HPA 미리 스케일업)
- **롤백은 1초 이내** (LB 설정만 원복하면 됨) -> 가장 빠른 RTO

### 3. 롤링 배포 (Rolling Deployment)

**인스턴스를 하나씩(또는 배치 단위로) 순차 교체** 하는 가장 보편적인 전략으로, Kubernetes의 `Deployment.spec.strategy.type: RollingUpdate` 가 기본값이다.

```text
[Rolling Update 상세 동작 (maxSurge=25%, maxUnavailable=25%)]

  [초기 상태: v1 4개]              [1단계: v2 1개 생성, v1 1개 종료]      [2단계: v2 2개, v1 2개]

  +----------+                    +----------+                          +----------+
  | v1 Pod-1 | (Old, 유지)        | v1 Pod-1 |                          | v2 Pod-1 |
  +----------+                    +----------+                          +----------+
  | v1 Pod-2 |                    | v2 Pod-2 |  ◄- 신규 생성            | v2 Pod-2 |
  +----------+                    +----------+                          +----------+
  | v1 Pod-3 |                    | v1 Pod-3 |                          | v1 Pod-3 |
  +----------+                    +----------+                          +----------+
  | v1 Pod-4 |                    | v1 Pod-4 |                          | v1 Pod-4 |
  +----------+                    +----------+                          +----------+

  (ReplicaSet: 4)                 (Old:3, New:1)                        (Old:2, New:2)

  +--------------------------->  시간 경과 (N+1 단계마다 진행) --------------------------->+

  [최종 상태: v2 4개]
  +----------+
  | v2 Pod-1 |
  +----------+
  | v2 Pod-2 |
  +----------+
  | v2 Pod-3 |
  +----------+
  | v2 Pod-4 |
  +----------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Deployment Controller** | ReplicaSet 교체 및 Pod 라이프사이클 관리 | K8s의 `Deployment.spec.strategy.rollingUpdate.maxSurge / maxUnavailable` 적용, 기본값 `maxSurge=25%, maxUnavailable=25%` |
| **Readiness Probe** | 트래픽 수신 가능 시점 결정 | `httpGet`, `tcpSocket`, `exec` 으로 헬스체크 후 `ready` 상태가 되어야만 Service Endpoint 에 등록 |
| **Pre-stop Hook + terminationGracePeriodSeconds** | 안전 종료 보장 | SIGTERM 수신 후 in-flight 요청 드레이닝(보통 30~60s), K8s 기본 30s |
| **Service Mesh (Istio/Linkerd)** | 트래픽 가중치 세분화 제어 | VirtualService `weight` 필드, DestinationRule 의 subset 정의로 버전별 라우팅 |

**핵심 파라미터 및 공식:**

- **가용성 보장**: `available_replicas = desired - maxUnavailable`
- **롤링 속도**: `rollout_duration ≈ ceil(desired / maxSurge) × (image_pull + probe_wait + grace_period)`
- **PDB (PodDisruptionBudget)**: 배포 중에도 `minAvailable` 이상 유지하도록 강제 (예: `minAvailable: 50%`)
- **Database 마이그레이션 시 호환성 규칙**: **Expand-Contract Pattern** (Backward-Compatible 스키마) — 컬럼 추가는 v1/v2 동시 호환, 컬럼 삭제는 v1 완전 폐기 후

- **📢 섹션 요약 비유**: 롤링은 **콘서트 좌석을 한 줄씩 새 좌석으로 바꾸는 것** 이고, Blue/Green 은 **옛 공연장과 새 공연장을 미리 다 만들어두고 관객을 한 번에 이동**시키는 것이며, Canary 는 **관객 1,000명 중 10명에게만 먼저 새 공연을 보여주고 "괜찮죠?" 라고 묻는 것** 입니다.

---

## Ⅲ. 비교 및 연결

### 1. 3대 전략 상세 비교

| 구분 | **Rolling Update** | **Blue/Green** | **Canary** |
| :--- | :--- | :--- | :--- |
| **리소스 사용량** | 1배 (in-place 교체) | 2배 (이중 환경) | 1.1~1.25배 (소수 신규 + 다수 기존) |
| **롤백 소요 시간** | 느림 (Rollout undo, 5~10분) | **즉시** (1초 이내 LB 스위치) | **빠름** (weight를 0%로, 1초) |
| **다운타임** | 없음 (maxUnavailable=0%) | 없음 (Green 사전 Warm-up) | 없음 |
| **버전 혼재 구간** | 장시간 (전체 교체까지) | 매우 짧음 (스위치 순간) | 장시간 (점진적 확대) |
| **DB 스키마 변경** | 양방향 호환 필수 (Expand-Contract) | 양방향 호환 또는 듀얼 라이트 | 양방향 호환 필수 |
| **세션/상태 처리** | Sticky Session 필요, In-Flight 처리 | 신규 세션은 Green, 진행 중 세션은 Blue 유지 | 카나리 사용자 세션 분리 필요 |
| **적합 시나리오** | Stateless API, 일반 MSA | DB 마이그레이션, Major Release | UI/UX 변경, ML 모델, 신규 기능 |
| **대표 도구** | K8s Deployment, ECS Rolling | Spinnaker Pipeline, CloudFormation, Argo Rollouts (Blue/Green) | Istio + Argo Rollouts, LaunchDarkly, Flagger |
| **리스크 레벨** | 중간 (부분 노출, 자동 롤백 어려움) | 낮음 (즉시 롤백) | 매우 낮음 (단계적 검증) |
| **테스트 가능성** | 낮음 (점진적 교체) | **높음** (Green에서 검증
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 467 / 600

<- **이전**: [466. 컨슈머 주도 계약 테스트](/knowledge-base/studynote/11_design_supervision/06_exam_summary/467_consumer_driven_contract/)
**다음**: [468. 피처 플래그 토글 점진적 릴리스](/knowledge-base/studynote/11_design_supervision/06_exam_summary/468_feature_flag_toggle/) ->

---
