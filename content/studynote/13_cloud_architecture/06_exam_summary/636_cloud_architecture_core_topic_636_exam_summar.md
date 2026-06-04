---
title: "636. 클라우드 아키텍처 핵심 토픽 636번 시험 요약 (Cloud Architecture Core Topic 636 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST SP 800-145 기반의 IaaS/PaaS/SaaS 3계층 서비스 모델과 Public/Hybrid/Multi-Cloud 배포 모델 위에서, 컨테이너 오케스트레이션(Kubernetes), 서비스 메시(Istio/Linkerd), 서버리스(MSA), 이벤트 기반 아키텍처(EDA)를 결합하여 워크로드의 탄력성·가용성·확장성을 보장하는 분산 시스템 설계의 총합이다.
> 2. **가치**: SLA 99.99%(Four Nine, 연 52.56분 장애) 기반의 글로벌 서비스를 통해 인프라 CAPEX를 OPEX로 전환(전환율 30~40% 절감), Auto-Scaling으로 Peak 트래픽의 10배 수용, MTTR 평균 70% 단축, 개발 배포 주기(Lead Time)를 월 1회 -> 일 10회 이상으로 단축하는 비즈니스 임팩트를 창출한다.
> 3. **판단 포인트**: Cloud Native vs. Lift & Shift 간의 마이그레이션 전략(6R: Rehost, Replatform, Repurchase, Refactor, Retire, Retain) 선택, 단일 클라우드 종속(Vendor Lock-in) 회피를 위한 Multi-Cloud/Abstraction Layer(Kubernetes, Terraform) 도입 여부, 보안 제로트러스트(Zero Trust) 모델과 데이터 주권/규제 컴플라이언스(K-PIPA, GDPR) 간의 균형점 설계가 핵심 의사결정 사안이다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-Tier 아키텍처(Presentation-Logic-Data)는 CAPEX 기반의 용량 계획(Capacity Planning) 한계, MTTR 평균 4시간, 배포 주기 1개월, 수직 확장(Scale-Up)의 물리적 한계(소켓 수, NUMA 노드 한정)로 인해 디지털 전환 시대의 요구사항을 충족하지 못한다. Netflix, Amazon, Google과 같은 Hyperscaler는 2006년 AWS EC2 출시 이후 컴퓨팅 자원을 Utility(전력·수도처럼 사용량 기반 과금) 모델로 제공하고, 클라우드 아키텍처는 이제 **클라우드 네이티브 12요소(12-Factor App)**, **Well-Architected Framework(5 Pillars)**, **사이트 신뢰성 엔지니어링(SRE)**을 기반으로 재정의되었다.

```text
[전통적 On-Premise vs 클라우드 네이티브 아키텍처 진화]

+-------------------------+        +---------------------------------+
|   On-Premise Monolith   |   ->    |       Cloud Native MSA         |
|  +-------------------+  |        |  +------+ +------+ +------+   |
|  |   Web (Tomcat)    |  |        |  | Auth| |Order | |Pay   |   |
|  +-------------------+  |        |  | MSA | | MSA  | | MSA  |   |
|  |  WAS (Logic)      |  |        |  +--+---+ +--+---+ +--+---+   |
|  +-------------------+  |        |     +--------+--------+        |
|  |  RDBMS (Oracle)   |  |        |       API Gateway / Service Mesh|
|  +-------------------+  |        |              |                  |
|  HW: 수직확장 한계       |        |  +-----------v---------------+  |
|  CAPEX: $1M 선투자      |        |  |  K8s Cluster + Istio Mesh |  |
|  배포주기: 1개월         |        |  +-----------+---------------+  |
+-------------------------+        |  +-----------v---------------+  |
                                  |  | Polyglot Persistence       |  |
                                  |  | (MySQL, Redis, Kafka, S3) |  |
                                  |  +----------------------------+  |
                                  |  HW: Auto-Scaling (10x Peak)     |
                                  |  OPEX: $0.10/hr 과금             |
                                  |  배포주기: 1일 10+ 회             |
                                  +---------------------------------+
```

- **CAPEX -> OPEX 전환**: 초기 CapEx $5M -> OpEx 월 $50K (TCO 36% 절감, Gartner 2023)
- **탄력성(Elasticity)**: 트래픽 Peak 100K RPS -> Auto-Scale 1,000 Pods, 종료 후 자동 50 Pods로 축소
- **글로벌 가용성**: Multi-Region Active-Active로 RTO 1분, RPO 0초 가능
- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **수도 요금처럼 쓰는 전기**와 같다. 사용한 만큼만 과금되고(OPEX), 폭염에 에어컨을 틀면 자동으로 전력이 증량(탄력성)되며, 정전 시(장애) 비상 발전기(Failover)가 즉시 가동되어 집안 전체가 멈추지 않는다(고가용성).

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 5대 계층(Edge -> Network -> Compute -> Storage -> Data/AI)으로 구성되며, **Well-Architected Framework의 5 Pillars**(Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization)를 모든 계층에 횡단적으로 적용한다.

```text
[클라우드 아키텍처 5계층 + 5 Pillars 횡단 구조]

                       +----------------------------------+
                       |   5 Pillars (Well-Architected)   |
                       |  OpEx | Sec | Rel | Perf | Cost  |
                       +----------------------------------+
   +---------+    +-------------+   +------------------+
   | Edge    |---->|   Network   |--->|     Compute      |
   | Layer   |    |   Layer     |   |     Layer        |
   |         |    |             |   |                  |
   | CloudFront|   | VPC/Subnet |   | EC2, Lambda,     |
   | CDN, WAF |    | ALB/NLB,   |   | EKS/ECS, Fargate |
   | Route 53|    | TGW, DX     |   | Auto Scaling Grp |
   +---------+    +-------------+   +--------+---------+
   +---------+    +-------------+            |
   | Data/AI |<----|  Storage    |<------------+
   | Layer   |    |   Layer     |
   |         |    |             |
   | Athena, |    | S3, EBS,    |
   | Redshift|    | EFS, FSx,   |
   | SageMake|    | Glacier     |
   +---------+    +-------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway & Service Mesh** | 외부 트래픽 진입점 + 내부 서비스 간 통신 제어 | Kong/AWS API Gateway(Throttling 10K RPS), Istio Sidecar(Envoy Proxy)로 mTLS, Circuit Breaker, Canary 배포 수행. 트래픽 100%를 v1 -> 95:5 -> 50:50 -> 0:100 단계적 라우팅 |
| **Container Orchestrator (Kubernetes)** | 컨테이너 라이프사이클 관리 + 셀프힐링 | K8s Control Plane(API Server, etcd, Scheduler, kubelet)이 Deployment 선언형(Desired State=3 replicas) -> ReplicaSet 3개 유지. HPA는 CPU 70% 임계치로 10초 주기 스케일링, PDB(Disruption Budget)로 `maxUnavailable: 1` 보장 |
| **Observability Stack (3 Pillars)** | 메트릭·로그·트레이스 통합 관측 | **Metrics**: Prometheus(15초 스크랩) + Grafana(P99 latency 200ms 알람) / **Logs**: Loki/ELK(Fluentd Sidecar로 수집) / **Traces**: Jaeger/Zipkin(OpenTelemetry SDK, TraceID 전파) -> SLI/SLO 기반 에러 버닝(Burn Rate) 모니터링 |
| **IaC & GitOps** | 인프라를 코드로 선언적 관리 + Git을 Single Source of Truth로 | Terraform으로 AWS 리소스 선언(`main.tf`, `state file`을 S3+DynamoDB Lock으로 관리) -> ArgoCD가 Git Repo와 Live Cluster의 **Drift Detection** 후 3-way Reconciliation(Head/Live/Desired) 수행. PR 승인 시 자동 Sync |
| **Event-Driven Backbone** | 비동기 이벤트 스트리밍 + CQRS/Event Sourcing | Apache Kafka 3.5(KRaft 모드, Zookeeper 제거)로 Partition 100개, ISR(In-Sync Replica) 3개, Exactly-Once Semantics(EOS) 보장. Producer는 `acks=all`, Consumer는 Manual Commit + DLQ(Dead Letter Queue) 패턴 |

### 핵심 알고리즘·파라미터

- **Consistent Hashing**: K8s Service의 iptables/IPVS 로드밸런싱, DynamoDB/Cassandra의 데이터 분할(파티션 키 128-bit MD5 해시 -> Ring 위의 0~2^32 슬롯)
- **CAP Theorem**: 분산 시스템은 일관성(C), 가용성(A), 분단 내성(P) 중 2가지만 선택. CP 시스템(Etcd, HBase) vs AP 시스템(DynamoDB, Cassandra)
- **SLO 계산식**: `Error Budget = 1 - SLO = 1 - 0.999 = 0.001 = 월 43.2분 허용 장애시간` -> Burn Rate 14.4x 알람 시 1시간 내 조치
- **📢 섹션 요약 비유**: 5계층 아키텍처는 **우체국 시스템**과 같다. 우편물(요청)이 우체통(Edge) -> 집배국(Network) -> 분류센터(Compute) -> 보관함(Storage) -> 주소록 DB(Data) 순서로 흘러가며, 품질감사원(5 Pillars)이 모든 단계에서 우편물 품질을 점검한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **Monolith** | **Microservices (MSA)** | **Serverless (FaaS)** |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/EAR (수 GB) | 컨테이너 이미지 (100~500MB) | 함수 코드 (수 KB) |
| **확장성** | Scale-Up (수직, 64 vCPU 한계) | Scale-Out (수평, K8s Node 5,000개) | 동시 실행 1,000개 (기본), Burst 가능 |
| **장애 격리** | 전 서비스 장애 (Blast Radius 100%) | Pod 단위 격리 (Hystrix Bulkhead 패턴) | 함수 단위 격리, DLQ로 분리 |
| **Cold Start** | 해당 없음 | Image Pull 30초 (Init Container로 단축) | Lambda 200ms~5초 (Provisioned Concurrency로 해결) |
| **적합 워크로드** | 단순 CRUD, 레거시 시스템 | 복잡한 도메인, 100+ RPS 이상 | 간헐적 트래픽, 이벤트 처리 (예: 이미지 리사이징) |
| **TCO (100만 RPS 기준)** | $80K/월 (피크 용량 상시) | $35K/월 (Auto-Scaling 평균) | $5K/월 (실행 시간 ms 과금) |

### 통합 연계

- **CI/CD 파이프라인**: GitHub PR -> Jenkins/GitHub Actions -> SonarQube(코드 품질) -> Trivy(컨테이너 취약점 스캔, CVE 7.0+ 차단) -> ArgoCD Sync -> Canary 분석(Argo Rollouts + Prometheus 메트릭) -> 자동 Promote
- **보안 통합**: Istio mTLS(서비스 간 상호 TLS) + OPA(Open Policy Agent, Rego 정책) + Vault(동적 Secret, 1시간 TTL) + Falco(런타임 침입 탐지, syscall 기반)
- **데이터 계층 통합**: CDC(Change Data Capture) — Debezium으로 MySQL Binlog 캡처 -> Kafka로 변경 이벤트 발행 -> Elasticsearch/ClickHouse로 동기화 (Dual Write 문제 해결)
- **📢 섹션 요약 비유**: Monolith는 **대형 유람선**(한 번 침몰하면 전원 위험), MSA는 **카풀 차량 여러 대**(한 차 사고나도 다른 차 운행), Serverless는 **택시**(필요할 때만 부르고 안 쓰면 안 옴)와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **마이그레이션 전략(6R) 선정**: 워크로드별 Rehost(단순 LAMP) / Replatform(DB를 Aurora로) / Refactor(Java -> Spring Native GraalVM) / Retire(중복 시스템 폐기) / Retain(규제상 On-Prem 유지) / Repurchase(SaaS 전환) 결정. **판단 기준**: TCO 회수 기간 3년, ROI 25% 이상 시 Refactor 추진
2. **Multi-Region DR 설계**: Active-Passive(비용 1.5x, RTO 30분) vs Active-Active(비용 2.5x, RTO 1분, RPO 0). 금융/의료처럼 RTO/RPO가 핵심인 경우 DynamoDB Global Tables(다중 리전 동기 복제) + Route 53 Health Check(30초 폴링) 필수
3. **보안 제로트러스트(Zero Trust) 적용**: 네트워크 위치(IP, VLAN) 신뢰 폐기 -> ID/Context 기반(NIST SP 800-207). 모든 요청은 mTLS + JWT 검증, 최소 권한(Just-in-Time Access), 마이크로 세그멘테이션. AWS IAM Identity Center + Azure AD Conditional Access
4. **FinOps (클라우드 비용 최적화)**: Reserved Instance(1~3년 약정, 40%v) / Savings Plan / Spot Instance(최대 90%v, Fault-Tolerant 배치 작업) / Right-Sizing(CloudHealth, Kubecost 분석). 미사용 리소스 자동 종료(Lifecycle Policy, S3 Intelligent-Tiering)
5. **관측 가능성(Observability) 확보**: SLI 정의(Latency, Error Rate, Saturation) -> SLO 설정(99.9% 가용) -> Error Budget 추적. OpenTelemetry로 Trace 표준화, Grafana Tempo/Loki/Cortex 통합. **핵심**: USE 방법론(Utilization, Saturation, Errors) + RED 방법론(Rate, Errors, Duration) 적용

### 피해야 할 안티패턴

- **Distributed Monolith**: MSA로 분리했으나 공유 DB(하나의 Schema) 사용 -> 결합도 상승, 배포 독립성 상실. **해결**: Database per Service + Saga Pattern
- **Snowflake Server**: 클릭 Ops로 만든 서버(수동 구성, IaC 미적용) -> 재현 불가, 장애 복구 시간 증가. **해결**: 100% IaC화, Immutable Infrastructure(AMI/Golden Image)
- **Chatty Microservices**: 마이크로서비스 간 동기 HTTP 호출 10회+ -> Latency 500ms, 장애 전파. **해결**: 비동기 이벤트 기반(Kafka), BFF(Backend for Frontend) 패턴, GraphQL DataLoader 배치
- **📢 섹션 요약 비유**: 안티패턴은 **자동차를 수동으로 조립하는 것**과 같다. 설계도(IaC) 없이 손으로 만든 차는 똑같은 차를 다시 만들 수 없고(Snowflake), 나사가 어긋나면(장애) 수리공이 기억으로 복구해야 하므로 시간이 오래 걸린다.

---

## Ⅴ. 기대효과 및 결론

| 항목 | 정량/정성 효과 |
| :--- | :--- |
| **배포 빈도** | 월 1회 -> 일 10회+ (DORA 4-Key Metrics 중 Elite 단계) |
| **MTTR** | 평균 4시간 -> 12분 (Runbook 자동화, ChatOps 기반) |
| **Change Failure Rate** | 30% -> 5% (Canary, Feature Flag, 자동 롤백) |
| **TCO 5년
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 636 / 800

<- **이전**: [635. 클라우드 아키텍처 핵심 토픽 635번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/635_cloud_architecture_core_topic_635_exam_summar/)
**다음**: [637. 클라우드 아키텍처 핵심 토픽 637번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/637_cloud_architecture_core_topic_637_exam_summar/) ->

---
