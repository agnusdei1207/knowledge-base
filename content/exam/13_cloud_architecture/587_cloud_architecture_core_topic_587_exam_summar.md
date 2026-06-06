---
title: "Cloud Architecture Core Topic 587 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 서비스 모델과 Public/Private/Hybrid/Multi-Cloud 배포 모델의 조합을 통해, **탄력성(Elasticity)**, **확장성(Scalability)**, **가용성(Availability)**을 SLA 기반의 API 인터페이스로 제공하는 분산 시스템 아키텍처임
> 2. **가치**: CAP(Consistency, Availability, Partition tolerance) 정리를 기반으로 한 분산 트랜잭션, 오토스케일링(3분 이내 1000노드 확장), Pay-per-Use 모델로 CAPEX 30~70% 절감, RTO/RPO 분 단위 달성
> 3. **판단 포인트**: 12-Factor App 원칙 준수 여부, Stateless 워크로드 설계, 데이터 일관성(Strong/Eventual) 선택, EKS/AKS/GKE 등 컨테이너 오케스트레이션 도입, FinOps 기반 비용 거버넌스, Zero Trust 보안 모델 적용의 trade-off

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 환경은 초기 CAPEX(설비투자비) 과다, 프로비저닝 시간 수주~수개월 소요, 트래픽 변동에 따른 과잉/과소 투자 문제로 인해 비즈니스 민첩성(Time-to-Market)이 현저히 떨어졌습니다. 2006년 AWS EC2 출시 이후 클라우드는 가상화(KVM, Xen -> Nitro System), 컨테이너화(Docker, 2013), 오케스트레이션(Kubernetes, 2014) 기술의 발전과 함께 컴퓨팅 자원의 **추상화(Abstract)**와 **프로그래머빌리티(Programmability)**를 완성시켰습니다.

NIST SP 800-145 표준에 따라 클라우드는 5대 필수 특성(On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service)을 만족해야 하며, 이는 기술사 시험에서 **클라우드 정의 문제로 단골 출제**됩니다. 4차 산업혁명 시대를 맞아 AI/ML 워크로드, IoT 데이터 처리, 실시간 빅데이터 분석 등에는 GPU 가속, 서버리스, 엣지 컴퓨팅 같은 **클라우드 네이티브(Cloud Native)** 아키텍처가 사실상 표준이 되었습니다.

```text
[클라우드 패러다임 전환 구조도]

   +-------------------------------------------------------------+
   |           전통적 On-Premise -> Cloud Native 전환 흐름          |
   +-------------------------------------------------------------+

   <- 과거(On-Premise, 2000s)              미래(Cloud Native, 2020s) ->
   +--------------+                      +----------------------+
   |  Mainframe   |                      |  Serverless Functions |
   |  + RDBMS     |   -- 전환 ------->   |  + Microservices      |
   |  + 전용 HW   |    (Migration)      |  + K8s + Service Mesh|
   +--------------+                      +----------------------+
         |                                       |
         v                                       v
   +--------------+                      +----------------------+
   |  Monolith    |                      |  API Gateway          |
   |  (단일 거대)  |                      |  -> Service Mesh      |
   |  + EJB/WAS  |                      |  -> Event Bus         |
   |  + 수직확장   |                      |  -> Multi-Region       |
   +--------------+                      +----------------------+
         |                                       |
   CAPEX 과다 (100%)                            v OPEX 30%v, TTM 80%v
   트래픽 대응 불가                        +----------------------+
   장애 전파 (SPOF)                        |  Cloud Native Stack:  |
                                          |  - IaC(Terraform)    |
                                          |  - GitOps(ArgoCD)    |
                                          |  - Observability     |
                                          |    (Prometheus/Grafana)|
                                          +----------------------+
```

특히 **하이퍼스케일러(Hyperscaler)**인 AWS, Azure, GCP가 제공하는 200여 종의 관리형 서비스(Managed Service)를 활용하면, 인프라 운영 부담을 줄이고 비즈니스 로직에 집중할 수 있습니다. 기술사 시험에서는 클라우드 도입 필요성을 **기술적/경제적/전략적 관점**에서 논술할 수 있어야 합니다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"전기 공급망(電力) 모델"**과 같습니다. 과거에는 각 가정/공장이 직접 발전소를 짓고(전통적 서버실) 연료(전력)를 생산해 썼지만, 클라우드 시대에는 중앙 발전소(클라우드 데이터센터)가 전기를 만들어 그리드(API/네트워크)로 공급하고, 우리는 사용량(kWh)만큼만 요금을 지불합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **가상화 계층**과 **오케스트레이션 계층**의 분리, 그리고 **제어 평면(Control Plane)**과 **데이터 평면(Data Plane)**의 분리에 있습니다. AWS의 경우 Region(25개+) -> Availability Zone(AZ, 통상 3개) -> Edge Location(400+개) 계층 구조로 설계되어, 단일 AZ 장애가 발생해도 다른 AZ에서 서비스가 지속됩니다.

```text
[클라우드 아키텍처 4계층 구조 - AWS 기준 상세화]

   +--------------------------------------------------------------+
   |  Layer 4: 사용자 접점 (Edge & Delivery)                        |
   |  - CloudFront(CDN), Route 53(DNS), WAF, Shield(DDoS)         |
   |  - Global Accelerator (Anycast IP)                             |
   +--------------------------------------------------------------+
   |  Layer 3: 제어 평면 (Control Plane)                            |
   |  - API Gateway, Service Catalog, IAM, CloudTrail, Config     |
   |  - IaC: Terraform/CloudFormation, GitOps: ArgoCD/Flux         |
   |  - 정책 관리: OPA(Open Policy Agent), SCP(Service Control)    |
   +--------------------------------------------------------------+
   |  Layer 2: 서비스 평면 (Service/Application Plane)              |
   |  - 컴퓨팅: EC2/EKS/Lambda/Fargate                             |
   |  - 스토리지: S3(객체)/EBS(블록)/EFS(파일)/Glacier(아카이브)    |
   |  - 데이터: RDS/Aurora/DynamoDB/Redshift/Neptune               |
   |  - 메시징: SQS/SNS/EventBridge/Kinesis/MSK(Kafka)            |
   |  - AI/ML: SageMaker/Bedrock/Textract/Rekognition              |
   +--------------------------------------------------------------+
   |  Layer 1: 인프라 평면 (Infrastructure Plane)                  |
   |  - 리전(Region) -> AZ -> Edge Location 계층                     |
   |  - 베어메탈: AWS Nitro System, Azure Boost, GCP Titanium     |
   |  - 네트워킹: VPC/Subnet/Transit Gateway/PrivateLink          |
   |  - SDN: VPC 라우터, Security Group, NACL                      |
   +--------------------------------------------------------------+
                                   |
                                   v
   +--------------------------------------------------------------+
   |           12-Factor App + Cloud Native 원칙                    |
   |  ① Codebase  ② Dependencies  ③ Config  ④ Backing Services     |
   |  ⑤ Build/Release/Run  ⑥ Processes  ⑦ Port Binding             |
   |  ⑧ Concurrency  ⑨ Disposability  ⑩ Dev/Prod Parity           |
   |  ⑪ Logs  ⑫ Admin Processes                                    |
   +--------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Region / AZ** | 지리적 격리(Geographic Isolation) | Region 간 데이터 전송은 전용선(DX, ExpressRoute, Interconnect) 사용, AZ 간 지연시간 1~2ms, 자동 장애 분리(Fault Domain) |
| **컴퓨팅 서비스** | 워크로드 실행 환경 | EC2(IaaS)/EKS(컨테이너)/Lambda(FaaS, 콜드 스타트 100~300ms)/Fargate(서버리스 컨테이너); 인스턴스 타입: 범용(M), 컴퓨트 최적화(C), 메모리 최적화(R), GPU(P/G) |
| **스토리지 3계층** | 데이터 영속성 및 접근성 | S3(11 9s=99.999999999% 내구성, 객체 스토리지)/EBS(블록, 단일 AZ)/EFS(NFS v4, 다중 AZ); Glacier Deep Archive는 $0.00099/GB/월 |
| **네트워크** | 통신 경로 분리 | VPC(Virtual Private Cloud) CIDR(/16)/Public/Private Subnet, NAT Gateway, Transit Gateway(Hub-Spoke), VPC Peering(1:1) vs Transit Gateway(N:N) |
| **Auto Scaling** | 탄력적 자원 조정 | **3가지 스케일링**: ① Reactive(임계치 기반, CPU 70%) ② Scheduled(예약형, Batch) ③ Predictive(ML 기반, AWS Auto Scaling); 스케일링 쿨다운 기본 300초 |
| **관리/관측** | 가시성 및 거버넌스 | **3가지 관측 신호**: Metrics(Prometheus/CloudWatch) + Logs(Loki/CloudWatch Logs) + Traces(Jaeger/X-Ray, OpenTelemetry 표준); SLO/SLI/SLA 정의 |

핵심 알고리즘 및 고려사항:
- **Consistent Hashing**: DynamoDB, Cassandra가 사용하는 데이터 분산 알고리즘으로, 노드 추가/제거 시 재해시(rehash)되는 키 비율을 1/n로 최소화
- **Raft Consensus**: etcd, CockroachDB의 분산 합의 알고리즘; Leader Election + Log Replication로 강한 일관성 제공, 5초 이내 Leader 선출
- **수평적 확장(Horizontal Scaling)**: Stateless 서비스는 ALB/NLB 뒤에 인스턴스 풀을 구성하고, 상태(Session)는 Redis/ElastiCache 또는 JWT 토큰으로 외부화
- **Circuit Breaker 패턴**: Hystrix(레거시) -> Resilience4j(현재), Closed/Open/Half-Open 3상태로 전파 장애 차단, 임계치 초과 시 Fallback 처리
- **Saga 패턴**: 분산 트랜잭션을 로컬 트랜잭션 체인으로 분리, 보상 트랜잭션(Compensating Transaction)으로 일관성 보장, Choreography vs Orchestration

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"현대적 호텔 운영 시스템"**과 같습니다. ① 예약 시스템(API Gateway)이 손님 요청을 받고, ② 룸매니저(Orchestrator)가 적절한 층/방(인스턴스)을 배정하며, ③ 청소/식사/교통 등 전문 서비스(Managed Service)들이 분리되어, 손님이 늘면 자동으로 룸을 늘리고(오토스케일링), 룸에 문제가 생기면 다른 룸으로 즉시 이동(자가 치유)시킵니다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처에서 가장 빈번하게 비교되는 핵심 개념들을 명확히 구분해야 합니다. 기술사 시험에서는 **개념 비교형 문제**(예: "IaaS와 PaaS의 차이", "수직확장과 수평확장의 차이")가 단골로 출제됩니다.

| 구분 | IaaS vs PaaS | 수평확장(Scale-Out) vs 수직확장(Scale-Up) | Public Cloud vs Private Cloud |
| :--- | :--- | :--- | :--- |
| **관리 범위** | IaaS: OS~미관리 / PaaS: 런타임~관리 | Scale-Out: 노드 수 증가 / Scale-Up: 단일 노드 성능^ | Public: CSP 완전관리 / Private: 자사 직접관리 |
| **유연성** | IaaS: 높음(OS 자유도) / PaaS: 낮음(제약 있음) | Scale-Out: 무한 확장 가능 / Scale-Up: HW 한계 도달 | Public: 즉시 프로비저닝 / Private: 사전 용량 계획 |
| **대표 서비스** | IaaS: EC2, Azure VM / PaaS: Beanstalk, App Engine | Scale-Out: 웹서버, 마이크로서비스 / Scale-Up: DB 서버 | Public: AWS, Azure, GCP / Private: OpenStack, VMware |
| **비용 모델** | IaaS: 인스턴스 과금(시간/초) / PaaS: 요청/실행 단위 과금 | Scale-Out: 라이선스 비례^ / Scale-Up: HW 비용^ (선형) | Public: Opex(운영비) / Private: Capex(설비투자비) |
| **적용 시나리오** | IaaS: 레거시 리프트앤시프트 / PaaS: 신규 개발, 빠른 출시 | Scale-Out: Stateless 웹/API / Scale-Up: 관계형 DB, 메모리 DB | Public: 변동 워크로드, 스타트업 / Private: 규제 산업(금융/공공) |
| **장애 도메인** | IaaS: AZ 단위 격리 / PaaS: 더 세분화된 격리 | Scale-Out: 일부 노드 장애 시 부분 서비스 / Scale-Up: 단일 장애시 전체 중단 | Public: 글로벌 / Private: 온프레미스 범위 |

**Hybrid Cloud 및 Multi-Cloud 통합 패턴**:
- **Hybrid Cloud**: On-Premise + Public Cloud의 연동, AWS Outposts/Azure Stack/Google Anthos로 일관된 운영 환경 제공, Direct Connect/VPN으로 전용선 연결
- **Multi-Cloud**: 2개 이상 CSP 동시 사용, 클라우드 폭발력(Cloud Bursting) 시나리오, 종속성 회피(Vendor Lock-in 방지), Terraform/Pulumi로 IaC 추상화
- **Inter-Cloud Networking**: Transit Gateway + RAM(Resource Access Manager)로 다계정/다리전 네트워크 통합, VPC Endpoint로 SaaS 서비스 프라이빗 접속

**MSA(Microservices Architecture)와의 연결**:
- 클라우드 네이티브의 핵심 구현 패턴으로, 12-Factor App + MSA + Container + DevOps + Continuous Delivery의 5요소가 결합
- **Service Mesh**(Istio/Linkerd): Sidecar 프록시(Envoy)로 서비스 간 통신 추상화, mTLS 보안, Traffic Management(Canary 90:10), Telemetry 자동 수집
- **API Gateway**(Kong, Apigee, AWS API Gateway): 외부 진입점 일원화, 라우팅, 인증/인가, Rate Limiting, Request/Response 변환

- **📢 섹션 요약 비유**: IaaS와 PaaS의 차이는 **"렌터카 vs 패키지 여행"**의 차이와 같습니다. 렌터카(IaaS)는 차종, 운전, 경로를 모두 직접 정하지만, 패키지 여행(PaaS)은 이동수단, 숙소, 식사, 일정까지 모두 제공되어 우리는 비즈니스(여가 활동) 자체에만 집중할 수 있습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **워크로드 특성 분석**: 트래픽 패턴(Steady-State vs Bursty), 동시 사용자 수(CCU), 응답시간 SLA(P50/P95/P99), 데이터 처리량(Throughput, RPS) 및 I/O 특성(Read-Heavy vs Write-Heavy)을 정량적으로 측정했는가? 3개월 이상의 실측 데이터 기반으로 인스턴스 타입/오토스케일링 정책 결정
2. **Well-Architected Framework 6대 축 검토**: ① Operational Excellence(운영 우수성) ② Security(보안) ③ Reliability(신뢰성) ④ Performance Efficiency(성능 효율) ⑤ Cost Optimization(비용 최적화) ⑥ Sustainability(지속 가능성)를 모두 검토했는가? AWS Well-Architected Tool/Azure Well-Architected Review로 정기 자가 진단
3.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 587 / 800

<- **이전**: [586. 클라우드 아키텍처 핵심 토픽 586번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/586_cloud_architecture_core_topic_586_exam_summar/)
**다음**: [588. 클라우드 아키텍처 핵심 토픽 588번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/588_cloud_architecture_core_topic_588_exam_summar/) ->

---
