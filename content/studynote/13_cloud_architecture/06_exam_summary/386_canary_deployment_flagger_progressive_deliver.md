---
title: "386. 카나리 배포 Flagger 프로그레시브 (Canary Deployment Flagger Progressive Delivery)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Flagger는 Kubernetes CRD(`Canary` 리소스)와 Istio/Linkerd/App Mesh 등 Service Mesh의 트래픽 분할(Traffic Split) 및 Prometheus 메트릭 분석을 결합하여, 카나리->블루그린->A/B 테스팅->세그먼트 라우팅 등 **단계적 배포 전략을 자동 상태머신(State Machine)으로 오케스트레이션**하는 Progressive Delivery 컨트롤러다.
> 2. **가치**: 배포 실패 시 **자동 롤백(0초~30초 내)**, 정량적 SLO 기반 의사결정(오류율/지연시간/처리량 임계치), 사람 개입 없는 GitOps 친화적 반복 배포, Istio/Linkerd 외 NGINX/Contour/Skipper/Gloo 멀티 메시 어댑터로 **MTTR 70%v, 변경 실패율(CFR) 60%v** 효과를 입증 가능하다.
> 3. **판단 포인트**: 단순 카나리(weight only) vs 자동 분석(Canary+Analysis) vs 세그먼트 라우팅(Match/Retry) 중 조직 성숙도에 맞는 **Stage 선택**, Prometheus 외에 Datadog/CloudWatch/Dynatrace 등 **메트릭 백엔드 종속성**, 그리고 **헤드리스 서비스(headless Service) / PodDisruptionBudget / ResourceQuota** 등 K8s 리소스 사전 검증이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

### 1.1 정의 및 등장 배경

**Progressive Delivery(점진적 전달)**는 Continuous Delivery를 한 단계 진화시킨 개념으로, 2018년 James Governor(RedMonk)이 명명했으며, "**배포(Deploy)와 릴리스(Release)의 분리**"를 핵심 사상으로 한다. 전통적 CD는 모든 사용자에게 **동시에** 신기능을 노출(Release)했지만, Progressive Delivery는 **소수 트래픽부터 단계적으로 노출**하여 비즈니스/기술 KPI를 실시간 검증한다.

**Flagger**는 2018년 Weaveworks(현 Isovalent/Tetrate 측 계열)에서 초기 릴리스, 이후 **Flux CD 프로젝트**의 일부(`flagger-loadtester` 등)로 흡수된 CNCF Sandbox(2020) -> Incubating(2024) 단계의 **Kubernetes Operator**다. GitHub Star 4.7k+, 주간 다운로드 200k+(2024 기준)를 기록하며 카나리 자동화 영역의 **사실상 표준 컨트롤러**로 자리매김했다.

### 1.2 왜 필요한가: 기존 배포 방식의 한계

```text
[기존 Rolling Update의 한계와 Flagger 필요성]

        +-------------------------------------------+
        |   kubectl set image deploy/web web:v2     |  <- v1.0 운영 중
        +--------------------+----------------------+
                             v
        +-------------------------------------------+
        | K8s 기본 RollingUpdate (maxSurge=25%)     |
        |  - 트래픽 100%를 v2로 즉시 점진 교체      |
        |  - 메트릭 기반 의사결정 없음               |
        |  - 에러율 증가 감지 불가                   |
        +--------------------+----------------------+
                             v
              ⚠️ 장애 발생 시 수동 kubectl rollout undo
                 MTTR: 5~30분 (사람이 로그 보고 결정)

        -------- Flagger 도입 후 비교 --------

        +-------------------------------------------+
        |  GitOps Repo(ArgoCD/Flux) -> 변경 감지     |
        +--------------------+----------------------+
                             v
        +-------------------------------------------+
        |  Flagger Canary CRD -> Service Mesh 트래픽 |
        |  1% -> 10% -> 25% -> 50% -> 100% 자동 승급   |
        |  + Prometheus 메트릭 실시간 분석           |
        +--------------------+----------------------+
                             v
              ✅ 에러율 > 1% 시 자동 롤백(2단계 내)
                 MTTR: 10~30초 (머신이 자동 결정)
```

| 구분 | 기존 Rolling Update | 수동 카나리(nginx ingress 가중치) | Flagger Progressive Delivery |
|:---|:---|:---|:---|
| 트래픽 분할 정밀도 | 25%/50% 단위 | 1% 단위 가능 (수동) | 1% 단위 + 자동 스케줄링 |
| 메트릭 기반 의사결정 | ❌ | ❌ (사람이 Grafana 보고 결정) | ✅ Prometheus 임계치 자동 |
| 자동 롤백 | ❌ (alert -> 수동) | ❌ | ✅ 30초 내 자동 |
| CD 분리(Deploy/Release) | ❌ | △ | ✅ (Canary 배포 ≠ 트래픽 전환) |
| 부하 테스트 트래픽 주입 | ❌ | ❌ | ✅ (loadtester 컨테이너) |
| 멀티 클러스터/멀티 메시 | ❌ | △ | ✅ (동일 CRD 패턴) |

### 1.3 핵심 트리거 시나리오

- **잘못된 기능 출시**: 결제 모듈의 회귀 버그 -> 1% 사용자에게만 노출 -> 자동 차단
- **DB 스키마 호환성 검증**: 무중단 마이그레이션(deploy+expand+contract) 패턴과 결합
- **AI/ML 모델 A/B**: 추천 모델 v1 vs v2의 CTR을 5% 구간에서 비교
- **리스크 기반 컴플라이언스**: 금융권에서 "변경 영향도" 증빙을 Prometheus/ArgoCD 로그로 자동 산출

### 📢 섹션 요약 비유
> "옛날에는 다리 위에서 차를 전부 한 번에 정지시키고 포장(개발자 수동 배포)했다면, Flagger는 **먼저 자전거 한 대만 새 포장으로 달리게 하고, 1,000km를 무사히 달리면 트럭으로 바꿔주는 자동 도로 시험 감독관**과 같다."

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 Flagger 컴포넌트 아키텍처

```text
[Flagger v1.36+ 아키텍처 및 Control Loop]

   +--------------------------------------------------------------+
   |                    GitOps Repository                          |
   |  apps/web/canary.yaml  (spec.provider: istio, step: 5% etc.)  |
   +-----------------------------+--------------------------------+
                                 | ArgoCD / Flux Sync
                                 v
   +--------------------------------------------------------------+
   |                Kubernetes API Server                          |
   |  Canary CRD -------------+                                   |
   |  (kind: Canary)          | watches                           |
   |  (targetRef: Deployment/web)                                |
   +--------------------------+-----------------------------------+
                              |
                              v
   +--------------------------------------------------------------+
   |                  flagger (Deployment)                         |
   |  +---------------------------------------------------------+  |
   |  |         Canary Controller (State Machine)               |  |
   |  |  Init -> Progressing -> Promoting -> Finalising -> Succeeded|  |
   |  +----+-------------------+----------------------+--------+  |
   |       |                   |                      |           |
   |       v                   v                      v           |
   |  +---------+       +----------+         +--------------+     |
   |  | Primary |       | Canary   |         |   Metric     |     |
   |  | Deploy  |       | Deploy   |         |   Server     |     |
   |  | (v1.0)  |       | (v1.1)   |         | (Prometheus) |     |
   |  +----+----+       +----+-----+         +------+-------+     |
   |       |                 |                      |             |
   |       +--------+--------+                      |             |
   |                v                               |             |
   |  +--------------------------+                  |             |
   |  |   Service Mesh (Istio)   |                  |             |
   |  |  VirtualService: web     |  <---- 트래픽 ----|             |
   |  |  weight: 95/5 -> 50/50    |       가중치     |             |
   |  +--------------------------+                  |             |
   +--------------------------------------------------------------+
                                                  |
                                                  v
                                       +------------------+
                                       |  Query:          |
                                       |  istio_requests_total|
                                       |  {destination=...}|
                                       |  status_code~"5xx"|
                                       +------------------+
```

### 2.2 핵심 구성 요소

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Canary CRD** | 사용자 선언(Declarative) 입력 | `apiVersion: flagger.app/v1`, `kind: Canary`. `spec.provider`, `spec.metrics`, `spec.analysis` 섹션으로 의도(Intent) 표현. GitOps 친화적이며 Kustomize/Helm 파라미터화 가능 |
| **Canary Controller** | 상태머신 오케스트레이터 | 5개 스테이트(Initialize->Progressing->Promoting->Finalising->Succeeded/Failed) + 3개 분석 모드(Canary/BLueGreen/A-B Testing). `analysisInterval`(기본 60s), `threshold`(기본 분석 10회 중 5회 실패 시 롤백) |
| **Metric Server** | 분석용 메트릭 수집기 | `spec.metrics` 정의 -> Prometheus PromQL, Datadog API, CloudWatch, Dynatrace, New Relic, K8s Probes 7종 백엔드 어댑터 내장. `interval`, `count`, `failureCondition`, `successCondition` 4-tuple |
| **Router Provider** | 트래픽 분할 실행기 | Istio(`VirtualService`), Linkerd(`ServiceProfile` + SMI), AWS App Mesh(`VirtualRouter`), NGINX(`VirtualServer`+`TrafficSplit`), Contour(`HTTPProxy`), Gloo(`Upstream`), Skipper(`Route`), SMI TrafficSplit |
| **Load Tester** | 합성 트래픽 주입기 | `flagger-loadtester` 사이드카 컨테이너로 `/bin/flagger-loadtester` RPC 수행. 카나리 Pod가 idle할 때(외부 트래픽 0%) 메트릭 의미를 보정하기 위해 5~10 RPS 강제 호출 |
| **Alert Manager Hook** | 사후 통지 | `spec.alerts[].provider: slack/pagerduty/discord/teams/msteams/webhook`. 롤백/승급/체크실패 이벤트 발생 시 즉시 전송 |

### 2.3 상태머신 전이(State Transition) 상세

```text
[Flagger Canary 상태 전이도 - 단계별 트래픽 비율 및 검증]

   (Git 변경 감지)
        |
        v
   +------------+
   | Initialize |  -- 카나리 Deployment/Service/PodMonitor 생성 (k8s 리소스 Ready 대기)
   +-----+------+
         | (모든 리소스 Ready)
         v
   +------------------+
   |   Progressing    |  <--- 반복 분석 (analysisInterval=60s)
   |  +------------+  |      +--------------------------------------+
   |  | step 1: 1% |--+------>| 메트릭 체크: error_rate, p99, req/s   |
   |  | step 2: 2% |--+------>| threshold(5/10) 초과 시 -> Failed    |
   |  | step 3: 5% |--+------>| 부하테스트: loadtester hooks 실행     |
   |  | ...        |--+------>| (webhooks 명령: smoke/load/chaos)    |
   |  | step N:100%|--+      +--------------------------------------+
   |  +------------+
   +-----+------------+
         | (모든 step 성공)
         v
   +------------+
   |  Promoting |  -- Primary Deployment 이미지 업데이트 + 트래픽 100% 전환
   +-----+------+
         |
         v
   +--------------+
   |  Finalising  |  -- 카나리 Deployment 제거, 분석 후 메트릭 보존 (cacheTTL=24h)
   +-----+----------+
         |
         v
   +--------------+
   |  Succeeded   |  -- (상태 머신 완료)   ⚠️ Failed 시 자동 롤백
   +--------------+         (Primary를 이전 버전으로 scale)
```

### 2.4 Canary CRD 핵심 스펙

```yaml
# 예시: Istio + Prometheus 기반 카나리 정의
apiVersion: flagger.app/v1
kind: Canary
metadata:
  name: web
  namespace: prod
spec:
  provider: istio:v1.20    # 메시/라우터 어댑터 버전
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web               # Primary를 가리킴
  progressDeadlineSeconds: 600
  analysis:
    interval: 30s           # 메트릭 수집 주기
    threshold: 5            # 10회 중 5회 실패 시 롤백
    maxWeight: 50           # 카나리 최대 트래픽 비율
    stepWeight: 5           # 1 step당 증가율
    canaryWeight: 0
    metrics:
    - name: error-rate
      templateRef:
        name: error-rate-template   # AnalysisTemplate CRD 참조
      interval: 30s
      thresholdRange:
        max: 1                       # 에러율 1% 이하
    - name: latency-p99
      templateRef:
        name: latency-template
      thresholdRange:
        max: 500                     # p99 500ms 이하
    webhooks:
    - name: smoke-test
      type: pre-rollout
      url: http://flagger-loadtester.prod:8080/
      timeout: 15s
      metadata:
        type: smoke
        cmd: "hey -z 10m -q 10 http://web-canary.prod/"
```

### 2.5 핵심 알고리즘: 임계치 의사결정 로직

Flagger는 **N회(`count`) 연속 검사 중 K회(`threshold`) 실패 시 롤백**을 채택한다. 이는 단순 평균(mean) 기반이 아닌 **윈도우 카운터**로, 일시적 스파이크(예: 배포 시점 GC pause)에 둔감하면서도 지속적 회귀에 민감하다.

```
판정식:
  failed = Σ (i=1..count) [ metric_result_i == FAIL ]
  if failed ≥ threshold:
      Canary.status.phase = "Failed" -> 트리거 Rollout
  else if metric_result_i == PASS for all i:
      Canary.status.phase = "Succeeded" -> 단계 승급
```

**추가로 `primaryLoadBalancing`(weight vs header), `mirrorTraffic`(샤도 트래픽), `sessionAffinity`(쿠키/헤더 기반 고정)** 등 고급 옵션으로 BFF/Edge 시나리오에 대응한다.

### 2.6 Progressive Delivery의 3대 Deployment 모드

| 모드 | 트래픽 분할 방식 | 활용 사례 | YAML 키 |
|:---|:---|:---|:---|
| **Canary(Weight)** | 비율 기반 0->100% 점진 | 일반 stateless API | `analysis.canaryWeight/stepWeight/maxWeight` |
| **Blue/Green** | 0% / 100% 스왑(원자적) | DB 마이그레이션, 결제 | `analysis.canaryWeight: 0`, `primaryReadyThreshold` |
| **A/B Testing(Header)** | `x-user-tier: premium` 등 헤더 매칭 | 기능 플래그, 카나리 신규벽 | `analysis.match[*].headers`, `iterations` |
| **Session Affinity** | 쿠키/헤더 고정 사용자 | 채팅, 트랜잭션 상태 | `analysis.sessionAffinity.cookie` |

### 📢
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 386 / 800

<- **이전**: [385. Flux GitOps 자동 동기화 배포](/studynote/13_cloud_architecture/06_exam_summary/385_flux_gitops_auto_sync_deployment/)
**다음**: [387. 블루그린 배포 무중단 전환 전략](/studynote/13_cloud_architecture/06_exam_summary/387_blue_green_deployment_zero_downtime_switch/) ->

---
