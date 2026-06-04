---
title: "418. 리소스 최적화 라이트사이징 스팟 (Resource Optimization Rightsizing Spot Instance)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 라이트사이징은 워크로드의 실제 사용률(CPU/Memory/IOPS) 메트릭을 기반으로 인스턴스 타입·사이즈를 과배정에서 적정 수준으로 재조정하는 FinOps 핵심 기법이며, 스팟 인스턴스는 클라우드 사업자의 유휴 용량(평균 60~90% 할인)을 2분 사전 통보 중단(interruption notice) 조건 하에 활용하는 비용 최적화 전략입니다.
> 2. **가치**: EC2 기준 On-Demand 대비 60~90% 비용 절감(스팟) + 30~50% 라이트사이징을 결합 시 총 컴퓨팅 TCO 70% 이상 절감 가능하며, AWS Compute Optimizer/Azure Advisor/GCP Recommender의 ML 기반 권고는 수동 분석 대비 정확도 85%+를 제공합니다.
> 3. **판단 포인트**: 스팟은 **상태 비보존(Stateless)**·**내결함성(Fault-tolerant)**·**유연한 시간(Flexible timing)** 워크로드에만 적용 가능하며, 라이트사이징 시 **버스트성 트래픽의 99th percentile**와 **HPA/VPA 스파이크**를 반드시 고려해 안전 마진(Safety Margin) 30~50%를 유지해야 합니다.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅 환경에서 **리소스 과배정(Over-provisioning)**은 엔터프라이즈가 직면하는 가장 큰 비용 비효율의 원인으로, Flexera 2024 State of the Cloud Report에 따르면 기업의 클라우드 지출 중 **30% 이상이 낭비(wasted spend)**로 분류됩니다. 이는 초기 설계 시 보수적 용량 계획, 마케팅 이벤트 대비 peak 부하 가정, 그리고 "추후 확장 대비"라는 명목하에 발생합니다. 동시에 클라우드 사업자는 데이터센터의 평균 사용률을 40~50% 수준으로 운영하며, 유휴 자원을 **스팟 인스턴스(Spot Instance)** 형태로 최대 90% 할인된 가격에 제공합니다.

**리소스 최적화(Rightsizing) + 스팟 인스턴스(Spot Instance)**는 이 두 가지 과제를 동시에 해결하는 전략적 조합입니다. 라이트사이징은 워크로드의 실제 사용 패턴을 계량적으로 분석하여 적정 사양을 도출하는 **정적 최적화(Static Optimization)**이고, 스팟 인스턴스는 유휴 용량을 활용한 **동적 비용 절감(Dynamic Cost Reduction)** 메커니즘입니다. 기술사 관점에서 이 두 기법은 단순한 비용 절감이 아닌, **용량 계획(Capacity Planning) -> 워크로드 분석(Workload Profiling) -> 인스턴스 매칭(Instance Matching) -> 자동화(Automation) -> 지속적 개선(Continuous Optimization)**으로 이어지는 FinOps 라이프사이클의 핵심 단계입니다.

```text
[기업의 클라우드 비용 지출 구조와 낭비 발생 지점]
+-----------------------------------------------------------------+
|                   Total Cloud Spend (100%)                       |
+------------------+------------------+--------------------------+
|   Used & Paid    |  Over-Provisioned |   Under-Utilized         |
|      (40%)       |       (30%)       |       (30%)              |
|  ████████        |  ████████         |  ████████                |
|  실제 사용 중    |  -> Rightsizing!  |  -> Spot Instance!      |
|                  |  (30~50% 절감)    |  (60~90% 절감)           |
+------------------+------------------+--------------------------+
                            |
                            v
              +-----------------------------+
              |  Rightsizing + Spot 결합 시   |
              |  최대 70% 컴퓨팅 TCO 절감    |
              +-----------------------------+
```

기존의 **Capacity-based Provisioning**(서버 1대를 사고 그 위에 모두 올리는 방식)에서는 워크로드의 피크치 기준으로 HW를 구매했기에 평균 사용률이 10~20%에 불과했습니다. IaaS 기반 On-Demand 환경으로 전환되어도 여전히 "안전 마진"을 두는 관성으로 인해 사용률은 30~40%에 머무릅니다. **라이트사이징 + 스팟 모델**은 관점을 근본적으로 전환하여, "필요한 만큼만" + "남는 자원을 싸게" 라는 이중 전략으로 **사용률을 60~70%**로 끌어올립니다.

- **📢 섹션 요약 비유**: 기존 방식이 마치 평소 손님 10명도 안 오는데 100인용 식당을 통째로 빌리는 것과 같다면, 라이트사이징은 손님 수에 맞춰 20인용으로 바꾸는 것이고, 스팟 인스턴스는 폐업 직전 식당에서 남은 음식을 70% 할인에 사는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. 라이트사이징(Rightsizing) 핵심 원리

라이트사이징은 **"Right instance type, right size, at the right time"** 원칙에 기반합니다. 이를 위해서는 다음 4단계 분석 파이프라인이 필요합니다.

```text
[라이트사이징 4단계 분석 파이프라인]
+--------------+    +--------------+    +--------------+    +--------------+
|  Step 1.     |    |  Step 2.     |    |  Step 3.     |    |  Step 4.     |
|  Metric      |---->|  Workload    |---->|  Instance    |---->|  Validation  |
|  Collection  |    |  Profiling   |    |  Matching    |    |  & Apply     |
|              |    |              |    |              |    |              |
| • CPU/Mem    |    | • P50/P95/   |    | • Family 매칭|    | • Canary     |
| • Network    |    |   P99 사용률 |    | • Gen 비교   |    | • A/B Test   |
| • IOPS/Disk  |    | • Peak 패턴  |    | • 가격/성능  |    | • 모니터링   |
| • 14~30일    |    | • 계절성     |    | • 라이선스   |    | • 롤백 계획  |
+--------------+    +--------------+    +--------------+    +--------------+
  CloudWatch/        Stat 분석           Compute            Auto Scaling
  Azure Monitor      회귀 분석           Optimizer          Group 변경
  GCP Stackdriver
```

### B. 메트릭 수집 및 분석 알고리즘

라이트사이징의 정확도는 **메트릭의 P95/P99 percentile**에 결정됩니다. 단순 평균은 burst성 워크로드를 과소평가하기 때문입니다.

| 지표 | 권장 임계치 (P95 기준) | 의미 | 권고 액션 |
| :--- | :--- | :--- | :--- |
| CPU 사용률 | < 40% | 과배정 | 다운사이징(Downsize) 검토 |
| CPU 사용률 | 40~60% | 적정 | 현재 인스턴스 유지 |
| CPU 사용률 | 60~80% | 위험 | 업사이즈 또는 HPA 조정 |
| CPU 사용률 | > 80% | 과소배정 | 즉시 업사이즈 (성능 risk) |
| Memory 사용률 | < 50% | 과배정 | 메모리 최적화 인스턴스로 변경 검토 |
| Memory 사용률 | > 85% | 위험 | OOM Kill 가능성, 즉시 조치 |
| Network I/O | < 30% 대역폭 | 과배정 | 네트워크 최적화 인스턴스 검토 |
| IOPS (EBS) | P99 < 70% of baseline | 적정 | gp3 -> io2 변경 불필요 |
| IOPS (EBS) | P99 > 90% | throttling | gp3 IOPS 증설 또는 io2 |

### C. 스팟 인스턴스(Spot Instance) 핵심 메커니즘

스팟 인스턴스의 핵심은 **"경매 기반 가격 모델"**과 **"2분 사전 통보(2-minute interruption notice)"**입니다.

```text
[스팟 인스턴스 라이프사이클 - AWS EC2 기준]

   +--------------------------------------------------------------+
   |  1. 요청 (Request)                                            |
   |     • 인스턴스 타입, AZ, AMI, 가용 용량 요구사항 정의          |
   |     • Launch Template / Launch Specification 등록              |
   +------------------+-------------------------------------------+
                      v
   +--------------------------------------------------------------+
   |  2. 입찰 (Bid) - 현재는 "가격 결정" 방식                       |
   |     • On-Demand 대비 % 단위 또는 절대 가격 지정                |
   |     • 스팟 가격 = 미사용 용량 수요/공급에 따라 동적 변동       |
   |     • 현재 가격이 bid ≥ market price -> 가동                    |
   +------------------+-------------------------------------------+
                      v
   +--------------------------------------------------------------+
   |  3. 가동 (Running)                                            |
   |     • 2분 interruption notice 보장                              |
   |     • CloudWatch Event -> Lambda -> Drain 트리거                |
   +------------------+-------------------------------------------+
                      v
   +--------------------------------------------------------------+
   |  4. 중단 (Interruption)                                       |
   |     • 2분 전 EventBridge 알림 -> "action": "terminate"        |
   |     • 5가지 중단 사유:                                          |
   |       - Spot capacity shortage                                 |
   |       - Price exceeded bid                                    |
   |       - Instance constraint (rare)                           |
   |       - User-initiated termination                            |
   |       - Instance rebalance recommendation (신고 후 5분)        |
   +------------------+-------------------------------------------+
                      v
   +--------------------------------------------------------------+
   |  5. 핸들링 (Handling)                                          |
   |     • Graceful shutdown: SIGTERM 처리 -> connection drain      |
   |     • 상태 저장: EBS snapshot, S3, EFS                        |
   |     • Auto Scaling: Capacity Rebalancing으로 자동 보충         |
   |     • Spot Fleet / Karpenter: 다른 instance type으로 자동 이전  |
   +--------------------------------------------------------------+
```

### D. 핵심 구성 요소 및 기술 매핑

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Compute Optimizer** (AWS) | ML 기반 권고 엔진 | CloudWatch 14일 메트릭 + CloudWatch Logs Insights 분석 -> 244개 인스턴스 타입 중 최적 매칭 추천 (95th percentile 기준, Free) |
| **AWS Auto Scaling Group + Mixed Instances Policy** | 인스턴스 타입 다변화 | Spot + On-Demand 비율(예: 70:30), 5~10개 instance type 분산, 가용성 극대화, capacity-optimized allocation strategy |
| **EC2 Fleet / Spot Fleet** | 다중 스팟 요청 통합 관리 | 단일 API로 수백 개 인스턴스 요청, lowestPrice / diversified / capacityOptimized / capacityOptimizedPrioritized 4가지 전략 |
| **Karpenter** | 차세대 프로비저닝 컨트롤러 | Kubernetes-native, Spot interruption EventBridge를 30~60초 내 감지 -> Spot-to-Spot 자동 마이그레이션, ConsolidatedBinPacking 알고리즘 |
| **Spot Instance Advisor** (AWS) | 과거 중단률 분석 | Region × Instance Type × AZ별 30일/60일/90일 중단 빈도 제공, 안정적 타입 선정에 활용 (예: m5.linux us-east-1a 안정도 4/5) |
| **Spot Placement Score** (AWS 신규) | 사전 스팟 용량 가용성 예측 | 요청 시점의 instance type + AZ 조합별 capacity 가용성을 1~10 스코어로 평가, 실패 가능성 사전 진단 |
| **Azure Spot VM** | Azure 동등 기능 | 최대 90% 할인, 30초 사전 통보, Eviction Policy: Deallocate(기본) / Delete, Spot Priority(Regular/High/Low) |
| **GCP Spot VM (Preemptible)** | GCP 동등 기능 | 최대 80% 할인, 24시간 최대 가동, 30초 사전 통보, Preemption Policy 설정 |
| **EventBridge + Lambda** | 인터럽션 핸들러 | Spot ITN(Interruption Termination Notice) 수신 -> ECS/EKS task drain -> ALB deregistration -> connection draining |
| **Cluster Autoscaler / Karpenter** | K8s 환경 자동 스케일링 | Pending Pod 발생 시 신규 노드 프로비저닝, 스팟 우선 사용 설정 (`spotToSpot: true`) |

### E. 스팟 가격 결정 알고리즘

스팟 가격은 **미사용 용량(Unused Capacity) 수요/공급 모델**로 결정됩니다.

```
P_spot(t) = f(미사용 용량 공급, 미사용 용량 수요, 입찰 분포, 시간대, Region/AZ)

• P_spot ≤ P_ondemand × 0.3 (70% 이상 할인 보편적)
• P_spot > bid -> 자동 reclaim (중단 통보)
• P_spot = bid -> 가용
• Steadiness: 동일 instance type × AZ의 90일간 변동성
```

### F. Capacity Rebalancing & Spot-to-Spot 마이그레이션

2022년 AWS가 도입한 **Capacity Rebalancing Recommendation**은 중단 위험을 사전 감지합니다.

```text
[Capacity Rebalancing 동작 흐름]
+--------------------+
| Spot Instance 가동 |
+----------+---------+
           v
+--------------------------------------+
| CloudWatch 5분 후 rebalance signal    |
| "인스턴스 타입 X의 중단 위험 80%"     |
+----------+---------------------------+
           v (EC2 API: 'rebalance' event)
+--------------------------------------+
| Lambda Triggered                     |
| 1. 해당 인스턴스 connection drain     |
| 2. Spot Fleet에 신규 인스턴스 요청    |
| 3. (Capacity Optimized) 가장 안정적  |
|    타입으로 자동 할당                  |
| 4. 기존 인스턴스 terminate           |
+--------------------------------------+
```

- **📢 섹션 요약 비유**: 라이트사이징은 자동차의 적정 연비에 맞춰 **타이어 공기압과 기어를 조정**하는 것이고, 스팟 인스턴스는 **빈 차(택시)을 70% 할인가에 빌려 타는** 것과 같습니다. 택시가 갑자기 필요한 손님에게 회수당해도, **다른 빈 차를 빠르게 잡을 수 있는 시스템**(Karpenter/Auto Scaling)이 있으면 무중단으로 운행할 수 있습니다.

---

## Ⅲ. 비교 및 연결

### A. 클라우드 비용 절감 모델 비교

| 구분 | On-Demand | Reserved Instance (RI) | Savings Plans | **Spot Instance** | Preemptible (GCP) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **할인율** | 0% (기준) | 30~60% | 27~72% | **60~90%** | 60~80% |
| **계약 기간** | 없음 | 1~3년 | 1~3년 | 없음 | 없음 |
| **중단 가능성** | 없음 | 없음 | 없음 | **있음 (2분 통보)** | 있음 (24h max) |
| **적합 워크로드** | 모든 워크로드 | Steady-state | 유연한 컴퓨팅 | Stateless, Batch | Batch, Dev |
| **예측 가능성** | 높음 | 높음 | 높음 | 낮음 | 낮음 |
| **라이트사이징 시너지** | 중간 | 낮음 (lock-in) | 중간 | **매우 높음** | 높음 |

### B. 스팟 vs 스팟 유사 서비스 비교

| 구분 | AWS Spot | Azure Spot VM | GCP Spot (Preemptible) | Alibaba preemptible |
| :--- | :--- | :--- | :--- | :--- |
| 최대 할인 | 90% | 90% | 80% |
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 418 / 800

<- **이전**: [417. FinOps 클라우드 비용 최적화 태깅](/studynote/13_cloud_architecture/06_exam_summary/417_finops_cloud_cost_optimization_tagging/)
**다음**: [419. 예약 인스턴스 세이빙 플랜 비용 절감](/studynote/13_cloud_architecture/06_exam_summary/419_reserved_instance_savings_plan_cost_reduction/) ->

---
