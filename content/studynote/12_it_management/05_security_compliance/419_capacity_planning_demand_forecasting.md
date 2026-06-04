---
title: "419. 용량 계획 수요 예측 확장 전략 (Capacity Planning Demand Forecasting)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 용량 계획(Capacity Planning)은 Little's Law(L = λ × W)와 M/M/c 큐잉 모델, 그리고 회귀분석·ARIMA·Prophet·LSTM 기반 시계열 예측을 결합하여 SLA(서비스수준협약) 99.95% 이상을 보장하는 최적 자원 산정(Provisioning) 공학이며, 확장 전략(Scale-out/in, Scale-up/down, Predictive/Scheduled/Reactive Scaling)은 워크로드 변동 특성(지수분포 트래픽, 일/월/계절적 주기성, 푸리에 스펙트럼 분석 기반 피크 계수)에 따라 결정되는 트레이드오프 의사결정이다.
> 2. **가치**: 정확한 수요 예측 기반의 Just-In-Time 용량 확보로 CapEx(설비투자비) 20~35% 절감, OpEx(운영비) 40% 이상 절감, Auto Scaling group의 평균 Utilization 65~75% Sweet-spot 유지, 그리고 MTTR(평균복구시간) 단축 및 SLO 위반률 0.1% 미만 달성 — Netflix·Amazon·Coupang·배달의민족 사례에서 입증됨.
> 3. **판단 포인트**: Stateless 웹/API 계층은 Scale-out(수평확장) + HPA(Horizontal Pod Autoscaler)가 표준이지만, Stateful RDBMS·In-Memory Cache·Message Queue는 Scale-up(수직확장) + Sharding/Read-Replica/Partitioning이 필수이며, Spinning Disk에서 NVMe SSD로, On-Premise에서 Hyperscaler(AWS·GCP·Azure)로의 마이그레이션 시 IOPS·Throughput·Latency의 단위가 ms->μs, IOPS 수천->수십만으로 변화하는 것을 반드시 재계산해야 한다.

---

## Ⅰ. 개요 및 필요성

용량 계획 수요 예측 확장 전략은 **클라우드 네이티브 시대의 핵심 운영 거버넌스(Operational Governance)** 이다. 전통적인 온프레미스 환경에서는 3~5년의 자산 교체 주기(Capital Refresh Cycle)에 맞춰 최대 피크 트래픽의 1.5배를 사전 확보(Over-Provisioning)하는 것이 상식이었으나, 클라우드와 컨테이너 오케스트레이션(Kubernetes) 시대에는 **탄력적(Elastic) 자원**이 필요하며, 이는 곧 "예측의 정확도가 곧 비용 효율" 이라는 명제로 귀결된다.

실제로 2023년 Gartner 보고서에 따르면, 클라우드 지출의 **30~35%가 낭비(Waste)** 이며, 이 중 상당 부분이 "예측 실패 + 자동화 미흡" 에서 기인한다. 반대로 Netflix는 1,000개 이상의 마이크로서비스를 50만 개 이상의 EC2 인스턴스로 운영하며, Eureka + Hystrix + Zuul 기반의 초단위(Sub-second) 예측 스케일링으로 1초당 1,000만 건의 API 호출을 처리한다. 배달의민족의 경우 DeepFM + LightGBM 기반의 시간대별·지역별 주문량 예측 모델로 점심/저녁 피크를 5분 단위로 사전 확장한다.

**근본적인 기술적 도전 과제**는 다음과 같다.

1. **비정상 트래픽(Burstiness)**: 단일 이벤트(블랙프라이데이, 11.11, 선거·스포츠 중계, DDoS)에서 평소의 50~500배 급증 — Long-tail 분포(Pareto, Power-law)로 모델링 필요
2. **Cold Start 문제**: 신규 서비스의 경우 Cold Start 시 Historical Data 부재 -> Capping Band(상한/하한) 기반 보수적 운영
3. **예측 불가능한 워크로드**: AI 추론(GPU), 배치 ETL, 트랜잭션 DB는 서로 다른 스케일링 곡선을 가짐
4. **비용-성능-가용성 트레이드오프**: 99.99% SLA -> 연간 downtime 52.6분, 99.999% -> 5.26분 — 비용은 기하급수적 증가

```text
+-------------------------------------------------------------------------+
|                    용량 계획의 3대 영역 (Capacity Triangle)             |
+-------------------------------------------------------------------------+
|                                                                         |
|                        +----------------------+                          |
|                        |   📈 수요 예측       |                          |
|                        |   (Demand Forecast)  |                          |
|                        |                      |                          |
|                        |  • 시계열 분석       |                          |
|                        |  • ARIMA / Prophet   |                          |
|                        |  • LSTM / Transformer|                          |
|                        |  • 푸리에 변환       |                          |
|                        +----------+-----------+                          |
|                                   |                                      |
|                                   v                                      |
|    +------------------+    +------------------+    +------------------+|
|    | 📊 용량 산정     |<---->| ⚙️ 확장 전략     |---->| 💰 비용 최적화   ||
|    | (Capacity Sizing)|    | (Scaling Strategy|    | (FinOps)         ||
|    |                  |    |                  |    |                  ||
|    |• Little's Law    |    |• Reactive        |    |• Reserved/       ||
|    |• M/M/c Queueing  |    |• Scheduled       |    |  Spot Instance   ||
|    |• Utilization 70% |    |• Predictive      |    |• RI/SP/CUD       ||
|    |• Headroom 30%    |    |• Burst(Buffer)   |    |• Auto Stop/Start ||
|    +------------------+    +------------------+    +------------------+|
|                                                                         |
|   핵심 공식: Required Capacity = (Peak_RPS × Avg_Latency_SLA) / (Target |
|   Utilization × Concurrency_Factor) + Safety_Buffer(20~30%)            |
+-------------------------------------------------------------------------+
```

**기존(전통적) vs 신규(클라우드 네이티브) 패러다임 비교**

- **전통적(2010 이전)**: 수동 용량 산정 -> Excel 시트 + 6개월 주기 -> Over-Provisioning 1.5배 -> 3-tier 모놀리식 아키텍처
- **전통적(2010~2015)**: 초기에 가상화(VMware vSphere)로 CapEx -> OpEx 전환, 그러나 여전히 Capacity Pool은 정적
- **클라우드 네이티브(2015~현재)**: 마이크로서비스 + 컨테이너 + HPA/VPA/Cluster Autoscaler + KEDA + Karpenter, **초단위(Sub-second) 탄력성** 실현
- **AIOps 시대(2023~)**: AWS Predictive Scaling, GCP Managed Instance Group Predictive Autoscaling, Azure Autoscale with ML — 과거 14일치 데이터를 LSTM으로 학습하여 24시간 후 예측

- **📢 섹션 요약 비유**: 용량 계획은 마치 **대형마트의 생수 재고 관리**와 같다. 폭염이 오면(트래픽 피크) 평소의 5배가 필요하지만, 한 번 팔고 나면 창고 비용(Idle Capacity)이 나간다. 그래서 "내일 비가 올지 안 올지"를 기상청처럼 정확히 예측해서, 딱 맞춰 들여놓는 것이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

용량 계획의 4계층 아키텍처는 **① 데이터 수집 -> ② 예측 모델링 -> ③ 의사결정 엔진 -> ④ 액추에이터(확장 실행)** 로 구성된다. 각각의 계층은 Prometheus, Grafana, TensorFlow, Argo CD, AWS Auto Scaling API 등 구체적인 오픈소스/상용 솔루션으로 구현된다.

```text
+----------------------------------------------------------------------+
|         Capacity Planning 4-Layer Reference Architecture              |
+----------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------+      |
|  | Layer 1: 데이터 수집 계층 (Telemetry Ingestion)            |      |
|  |  +------+  +------+  +------+  +------+  +------+         |      |
|  |  |Metric |  | Log  |  |Trace |  |Event |  |SLA   |         |      |
|  |  |Promet.|  |Loki  |  |Tempo |  |Kafka |  |Service|         |      |
|  |  +---+--+  +---+--+  +---+--+  +---+--+  |Now   |         |      |
|  |      +--------+-----+----+---------+     +--+---+         |      |
|  |                     v                       |              |      |
|  |            +------------------+             |              |      |
|  |            | Time-Series DB  |             |              |      |
|  |            |  (Thanos/Mimir) |             |              |      |
|  |            +--------+---------+             |              |      |
|  +---------------------+-----------------------+--------------+      |
|                        v                       v                     |
|  +------------------------------------------------------------+      |
|  | Layer 2: 예측 모델링 계층 (Forecasting Engine)             |      |
|  |  +------------+  +------------+  +--------------------+   |      |
|  |  | Statistical |  | ML Models  |  |  Anomaly Detection |   |      |
|  |  | • ARIMA    |  | • Prophet  |  |  • Isolation Forest|   |      |
|  |  | • SARIMA   |  | • LSTM     |  |  • 3-Sigma Rule    |   |      |
|  |  | • Holt-    |  | • TFT      |  |  • Prophet changep.|   |      |
|  |  |   Winters  |  | • N-BEATS  |  |                    |   |      |
|  |  +------+-----+  +------+-----+  +--------+-----------+   |      |
|  |         +----------------+-----------------+                |      |
|  |                          v                                  |      |
|  |            +--------------------------+                      |      |
|  |            | Forecast: ŷ(t+h) ± CI    |                      |      |
|  |            | (h-step ahead, 95% CI)   |                      |      |
|  |            +----------+---------------+                      |      |
|  +-----------------------+--------------------------------------+      |
|                          v                                             |
|  +------------------------------------------------------------+      |
|  | Layer 3: 의사결정 엔진 (Decision Engine)                    |      |
|  |  +------------+  +------------+  +--------------------+    |      |
|  |  | Scaling    |  | Cost-Aware |  |  SLO-Aware        |    |      |
|  |  | Policy     |  | Optimizer  |  |  Controller        |    |      |
|  |  |            |  |            |  |  (e.g., HPA)       |    |      |
|  |  |desired=    |  |Spot/On-    |  | target=            |    |      |
|  |  |ceil(pred/  |  |demand mix  |  | min(metric,        |    |      |
|  |  | capacity)  |  |            |  |     SLA_bound)     |    |      |
|  |  +------+-----+  +------+-----+  +--------+-----------+    |      |
|  |         +----------------+-----------------+                |      |
|  |                          v                                  |      |
|  |            +--------------------------+                      |      |
|  |            | target_replicas = f(     |                      |      |
|  |            |  forecast, headroom,     |                      |      |
|  |            |  headroom_buffer)        |                      |      |
|  |            +----------+---------------+                      |      |
|  +-----------------------+--------------------------------------+      |
|                          v                                             |
|  +------------------------------------------------------------+      |
|  | Layer 4: 액추에이터 계층 (Execution & Resource Provision) |      |
|  |  +------------+  +------------+  +--------------------+    |      |
|  |  | HPA / VPA  |  | Cluster    |  |  Cloud Provider    |    |      |
|  |  | (K8s)      |  | Autoscaler |  |  Auto Scaling API  |    |      |
|  |  |            |  | Karpenter  |  |  ASG / MIG / VMSS  |    |      |
|  |  +------------+  +------------+  +--------------------+    |      |
|  |                                                              |      |
|  |   물리 자원: EC2/EKS, GKE/GCE, AKS, Bare-metal, On-Prem   |      |
|  +------------------------------------------------------------+      |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **데이터 수집 (Telemetry)** | CPU/Memory/Network/Disk IOPS, RPS, p99 Latency, GC Pause, Connection Pool 사용률 등 핵심 메트릭을 15초~1분 단위로 수집 | Prometheus(스크랩 방식), Telegraf/Vector(에이전트 푸시), OpenTelemetry(벤더 중립), eBPF(커널 레벨 관측) |
| **시계열 DB (TSDB)** | 초당 수백만 시계열을 1년 이상 보관, 다운샘플링(1m->5m->1h) 자동 수행 | Prometheus + Thanos(장기 보관), InfluxDB, TimescaleDB, VictoriaMetrics, Grafana Mimir |
| **예측 모델 (Forecasting)** | 과거 패턴 학습 -> 미래 트래픽 예측값(ŷ)과 신뢰구간(CI) 산출 | ARIMA(p,d,q)/SARIMA(계절성), Facebook Prophet(휴일·추세·계절 분해), LSTM/GRU/RNN, N-BEATS(M4 챔피언), Temporal Fusion Transformer(TFT) |
| **의사결정 엔진 (Policy)** | 예측값 + 정책(Headroom, Burst Buffer) -> 목표 replica 수 산출 | K8s HPA 공식 `desiredReplicas = ceil[currentReplicas × (currentMetricValue / desiredMetricValue)]`, VPA(리소스 권장), Karpenter(Just-In-Time 노드 프로비저닝, 30초 이내), KEDA(이벤트 기반) |
| **액추에이터 (Executor)** | 실제 인프라 생성/삭제, 로드밸런서 재구성, Warm Pool 활용 | AWS Auto Scaling Group, GCP Managed Instance Group, Azure VMSS, Spot Instance(70~90% 할인) + Spot Fleet, Warm Pool(미리 AMI 부팅) |
| **FinOps 게이트웨이** | 비용 임계치 초과 시 스케일 차단/알림, RI/SP 활용 최적화 | Kubecost, OpenCost, CloudHealth, Vantage — **단위**: USD/vCPU-hour, USD/GB-month |
| **Anomaly Detector** | DDoS, Hot Key, Memory Leak, GC 폭증 등 비정상 패턴 조기 탐지 | Prometheus Alertmanager, Datadog Watchdog, Dynatrace Davis, AWS DevOps Guru |

### 핵심 수학적 모델 (Deep Dive)

**1. Little's Law (L = λ × W)**
- L = 시스템 내 평균 요청 수, λ = 단위 시간당 도착률(RPS), W = 평균 체류시간(latency)
- 예: RPS 10,000, 평균 응답 200ms -> 동시 처리 2,000 vCPU 필요
- 이를 Utilization(ρ = λ/(c×μ))과 결합 -> c = ceil
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 419 / 800

<- **이전**: [418. 서비스 디자인 서비스 블루프린트](/studynote/12_it_management/05_security_compliance/418_service_design_service_blueprint/)
**다음**: [420. 가용성 관리 MTBF MTTR 고가용성](/studynote/12_it_management/05_security_compliance/420_availability_management_mtbf_mttr_ha/) ->

---
