---
title: "Cloud Architecture Core Topic 736 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST SP 800-145의 5대 필수 특성(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)과 12-Factor App 원칙, CAP Theorem을 기반으로, 가상화(KVM/Hyper-V)·컨테이너(Docker/containerd)·서버리스(Lambda/Functions/Cloud Run) 등 추상화된 컴퓨팅 자원을 통해 Stateless·API 중심·이벤트 드리븐 설계를 실현하는 분산 시스템 패러다임이다.
> 2. **가치**: CAPEX->OPEX 전환을 통한 초기 투자비 60~80% 절감, Auto-Scaling Group과 Spot Instance로 Peak 트래픽 시 TCO 30~50% 감축, 글로벌 멀티 리전(Region) 배포로 RTO 1분/RPO 0초 달성, Time-to-Market을 6~18개월->2~8주 단축하여 Business Agility 극대화.
> 3. **판단 포인트**: Cloud-Native(Greenfield) vs Lift-and-Shift(Rehost) Migration 전략, Multi-Cloud(이중화) vs Hybrid Cloud(연결성), Stateful(Sticky Session) vs Stateless(Stateless Token), 동기(REST/gRPC) vs 비동기(SQS/Kafka/Pub-Sub) 통신, 그리고 비용-성능-보안-컴플라이언스(CSAP/ISO27001) 4축 트레이드오프의 기술사적 의사결정.

---

## Ⅰ. 개요 및 필요성

전통적 On-Premise 아키텍처는 **고정 CapEx(자본 지출)**, **수동 용량 계획(Capacity Planning)**, **수직적 확장(Scale-Up)**, **단일 장애점(SPOF)**이라는 한계를 지녔다. 2006년 AWS S3(객체 스토리지)와 EC2(IaaS) 출시 이후 컴퓨팅 자원은 "Service as a Software" 형태로 전환되었고, 2013년 Docker(컨테이너), 2014년 Kubernetes(오케스트레이션), 2014년 AWS Lambda(Serverless)가 잇따라 등장하며 **클라우드 네이티브(Cloud-Native)** 시대가 본격 개막했다. COVID-19 이후의 Digital Transformation 가속화와 MSA(Microservices Architecture) 보편화, AI/ML 워크로드의 폭증은 클라우드 아키텍처를 단순한 인프라 대안을 넘어 **비즈니스 혁신의 핵심 엔진**으로 격상시켰다.

특히 국내에서는 **클라우드컴퓨팅법(2023.9.15 시행)**, **클라우드 서비스 보안 인증(CSAP)**, **조달청 나라장터 SaaS 등록제** 등 규제 환경이 정비되면서, 공공·금융권에서도 클라우드 도입이 가속화되고 있다. 기술사 관점에서는 클라우드 아키텍처를 단순히 "AWS 쓰는 것"이 아니라, **도메인 분해(DDD) -> API 설계 -> 데이터 분산 -> 운영 거버넌스**로 이어지는 End-to-End 설계 역량으로 평가한다.

```text
[ 전통 On-Premise 아키텍처 vs Cloud-Native 아키텍처 비교 ]

[전통 On-Premise]                       [Cloud-Native]
+------------------+                    +------------------+
|   Monolith App   |                    |   API Gateway    |
|   (단일 WAR/EAR) |                    |  (Kong/ALB)      |
+------------------+                    +--------+---------+
|  WebLogic/JEUS   |                             | JWT/RBAC
|  (App Server)    |                             v
+------------------+              +--------------------------+
|   Oracle RAC     |              |  Microservices Mesh      |
|  (Shared-Everything)             |  +------+ +------+       |
+------------------+              |  |User | |Order |       |
|   SAN Storage    |              |  |Svc  | |Svc   |  ...  |
|  (LUN/RAID)      |              |  +------+ +------+       |
+------------------+              |   Istio/Linkerd(Envoy)    |
|  수동 Capacity   |              +--------------------------+
|   Planning       |                             |
|  (Peak 기준)     |              +--------------+--------------+
+------------------+              |                             |
        |                  +------v-----+             +-------v----+
        v                  | K8s Cluster|             | Serverless |
  Scale-Up               |  (EKS/AKS)  |             |  (Lambda)  |
  (서버 증설)            |  HPA/VPA/   |             |  Event-    |
  수개월 소요            |  Cluster-   |             |  Driven    |
                        |  Autoscaler |             |            |
                        +-------------+             +------------+
                              |                             |
                        +-----v-----------------------------v-----+
                        |   Multi-Region / Multi-AZ Distribution    |
                        |   S3(11 9s)  |  DynamoDB Global Tables     |
                        |   CloudFront|  Route 53 Latency-based     |
                        +-------------------------------------------+
                              |
                        +-----v-----------------------------+
                        | Observability: Prometheus+Grafana |
                        | Logging: EFK/Loki | Tracing: X-Ray|
                        +-----------------------------------+
```

**주요 변화 양상**:
- **CapEx -> OpEx**: 선불 인프라 투자 -> 사용량 기반 종량제(Pay-As-You-Go)
- **Waterfall -> DevOps/GitOps**: 6개월 릴리즈 -> 1일 다수 배포(Continuous Deployment)
- **단일 데이터센터 -> Multi-Region**: 자연재해·전쟁 등에도 사업연속성(BCP) 확보
- **수직 확장 -> 수평 확장**: HPA(Horizontal Pod Autoscaler)로 트래픽 1만 RPS 대응
- **MTTR(Mean Time To Repair) 단축**: IaC(Terraform/CloudFormation) + Auto-Remediation

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"호텔식 주거 모델"**이다. 전통 On-Premise는 "자기 집 짓기"(설계·건축·유지보수 모두 직접)라면, 클라우드는 "원하는 방을 필요한 기간만 빌려 쓰고, 퇴거 시 원상복구 불필요"하며, IaaS는 "빈 방(가구는 직접)", PaaS는 "가구 있는 방(인테리어는 직접)", SaaS는 "풀옵션 호텔"(짐만 풀면 됨), FaaS는 "세탁기 1회 사용권"(필요한 순간만 1분 단위 과금)에 해당한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 기술적 핵심은 **"추상화(Abstraction) + 자동화(Automation) + 탄력성(Elasticity)"**의 3축이다. 컴퓨팅 자원은 Hypervisor(KVM/Xen/Hyper-V) -> 컨테이너 런타임(containerd/CRI-O) -> FaaS Runtime(Firecracker/gVisor) 순으로 추상화 수준이 높아지며, 각 계층은 API 기반의 선언적(Declarative) 프로비저닝과 Reconciliation Loop를 통해 Self-Healing을 수행한다.

**핵심 동작 메커니즘**:
1. **요청 수신**: API Gateway(Amazon API Gateway, Kong, NGINX Plus)가 TLS Termination, Rate Limiting, OAuth2.0/JWT 검증
2. **라우팅**: Service Mesh(Istio/Linkerd) Envoy Sidecar가 mTLS(상호 TLS)로 내부 통신 암호화
3. **오케스트레이션**: Kubernetes Control Plane(etcd + kube-scheduler + kube-controller-manager)이 선언된 Desired State와 Actual State의 차이를 Reconcile
4. **확장**: HPA가 CPU/Memory/Custom Metric(예: SQS Queue Depth) 기반으로 Pod 개수 1->100 자동 조절
5. **상태 관리**: StatefulSet + PersistentVolume(Ceph/EBS/EFS) + Operator Pattern(Cassandra Operator)으로 분산 데이터 관리
6. **관측**: OTel(OpenTelemetry) Collector가 Trace·Metric·Log를 수집하여 Prometheus + Tempo/Loki + Grafana로 시각화

```text
[ Cloud-Native 7계층 아키텍처 상세 흐름도 ]

① Edge/CDN Layer
   CloudFlare / CloudFront / Akamai  --- DDoS 방어, WAF, TLS 1.3
   | L7 로드밸런싱 (ALB), L4 (NLB)
   v
② API Gateway Layer
   Kong / Apigee / AWS API Gateway / Spring Cloud Gateway
   - JWT 검증, Rate Limiting (Token Bucket 100 req/s)
   - Circuit Breaker (Resilience4j), Retry, Timeout
   v
③ Service Mesh Layer (Sidecar Pattern)
   +------------------+      +------------------+
   |  Pod (User Svc)  |      |  Pod (Order Svc) |
   |  +------+  +----+|      |+----+  +------+ |
   |  |App.js|◄-+Envoy|+-mTLS+|Envoy|◄-+Go API| |
   |  +------+  +----+|      |+----+  +------+ |
   +------------------+      +------------------+
   - Istio Control Plane (istiod): xDS API로 설정 분배
   v
④ Orchestration Layer (Kubernetes)
   +---------------------------------------------+
   |  Master Node (Control Plane)                |
   |  +------+ +----------+ +-----------------+  |
   |  |etcd  | |Scheduler | |Controller Mgr   |  |
   |  |(Raft)| |(Bin-pk)  | |(Reconcile Loop) |  |
   |  +------+ +----------+ +-----------------+  |
   +---------------------------------------------+
   +----v----+ +----v----+ +----v----+
   |Worker 1 | |Worker 2 | |Worker 3 |  (HPA: 1->100 Pods)
   |(kubelet)| |(kubelet)| |(kubelet)|
   +---------+ +---------+ +---------+
   v
⑤ Serverless/Event Layer
   AWS Lambda / Azure Functions / GCP Cloud Run / Knative
   - Cold Start: 100ms~1s (Provisioned Concurrency로 해결)
   - Event Source: SQS, Kinesis, EventBridge, Kafka
   v
⑥ Data Layer
   +--------------+  +--------------+  +--------------+
   | RDBMS         |  | NoSQL        |  | Cache/Queue  |
   | - Aurora(6-way|  | - DynamoDB   |  | - Redis      |
   |   Replication)|  | - CosmosDB   |  | - ElastiCache|
   | - CockroachDB |  | - Cassandra  |  | - Kafka MSK  |
   +--------------+  +--------------+  +--------------+
   - CQRS: 쓰기(Master) / 읽기(Replica) 분리
   - Event Sourcing: Kafka Append-Only Log
   v
⑦ Observability & SecOps Layer
   +---------------------------------------------+
   | Metrics: Prometheus / CloudWatch / Datadog|
   | Logs:    EFK(Elastic+Filebeat+Kibana) / Loki|
   | Traces:  Jaeger / Zipkin / AWS X-Ray       |
   | SIEM:    Spl
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 736 / 800

<- **이전**: [735. 클라우드 아키텍처 핵심 토픽 735번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/735_cloud_architecture_core_topic_735_exam_summar/)
**다음**: [737. 클라우드 아키텍처 핵심 토픽 737번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/737_cloud_architecture_core_topic_737_exam_summar/) ->

---
