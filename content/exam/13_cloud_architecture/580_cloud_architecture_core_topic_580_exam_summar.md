---
title: "Cloud Architecture Core Topic 580 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 가상화·컨테이너·서버리스·오케스트레이션을 결합한 **탄력적 컴퓨팅 자원 풀(Elastic Resource Pool)** 위에 API 중심의 마이크로서비스·이벤트 기반·메시 기반 패턴을 적층하여, 장애 격리(Failure Domain) 단위로 SLA를 분해하고 워크로드 특성에 따라 IaaS/PaaS/SaaS/FaaS 계층을 선택적으로 편성하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: Auto-Scaling을 통해 트래픽 피크 시 **3~5배의 컴퓨팅 자원을 수 분 내 확보**하여 응답 지연을 P99 기준 200ms 이하로 유지하고, Pay-as-you-go 모델로 **TCO(총소유비용) 30~60% 절감**, Multi-AZ·Multi-Region 구성을 통해 **연간 가용성 99.99%(Four-Nines, 52.6분/년 장애)** 달성이 가능하다.
> 3. **판단 포인트**: Stateless/Stateful 워크로드 분리, **12-Factor App 준수 여부**, 데이터 일관성 모델(Strong vs Eventual Consistency), **CAP 정리** 하의 가용성·일관성·분단내성 트레이드오프, 그리고 CSP 종속(Vendor Lock-in)과 이식성(Portability) 간 균형이 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스(On-Premise) 아키텍처는 **수직 확장(Scale-Up)** 방식의 모놀리식(Monolithic) 애플리케이션, 고정 용량의 하드웨어, 수동 프로비저닝으로 인해 **Capacity Planning 오차로 인한 자원 낭비(평균 활용률 10~20%)**와 배포 주기 수개월에 달하는 **Change Lead-time** 문제를 야기했다. 클라우드 아키텍처는 이를 **가상화(Hypervisor/KVM) -> 컨테이너화(Docker) -> 오케스트레이션(Kubernetes) -> 서버리스(FaaS/Lambda)** 로 진화시키며, **인프라 추상화(Infrastructure as Code, Terraform/CloudFormation)** 와 **불변 인프라(Immutable Infrastructure)** 원칙을 통해 일관되고 반복 가능한 프로비저닝을 실현한다.

특히 2014년 AWS Lambda를 기점으로 한 **서버리스 컴퓨팅**은 C10K·C10M 문제를 Event-Driven 메시지 큐(SQS/Kafka)와 결합하여 해결하며, 개발자가 VM/Container 관리 없이 **밀리초 단위 콜드 스타트** 후 비즈니스 로직만 작성하는 패러다임으로 전환되었다. 클라우드 네이티브(Cloud Native) 4축인 **컨테이너·CI/CD·MSA·DevOps**가 성숙하면서, 트래픽 폭증 시 **Horizontal Pod Autoscaler(HPA)** 가 CPU/Memory/Queue Lag 메트릭 기반으로 15초 단위로 Pod를 증설하고, **Cluster Autoscaler(CA)** 가 노드 풀을 자동 확장한다.

```text
   +----------------------------------------------------------------------+
   |                    클라우드 아키텍처 진화 패러다임                       |
   +----------------------------------------------------------------------+
   |                                                                      |
   |   2000s On-Premise       2010s IaaS/PaaS       2020s Cloud Native   |
   |   +--------------+      +--------------+      +--------------+     |
   |   | Mainframe    |      | VM 기반 가상화 |      | 컨테이너+서버리스|     |
   |   | Scale-Up     |  ->   | Scale-Out    |  ->   | Event-Driven |     |
   |   | 수동 운영     |      | API 자동화    |      | 셀프힐링     |     |
   |   | Monolith     |      | SOA/EAI      |      | MSA+Mesh     |     |
   |   +--------------+      +--------------+      +--------------+     |
   |          |                      |                      |            |
   |     활용률 10-20%          활용률 40-60%          활용률 70-90%      |
   |     배포 주기: 월         배포 주기: 주          배포 주기: 시/분     |
   |     장애복구: 일          장애복구: 시간         장애복구: 분/초      |
   +----------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 진화는 마치 **"정원 가꾸기"** 에 비유할 수 있다. 2000년대에는 정원의 모든 식물을 직접 심고 물을 주어야 했다면(온프레미스), 2010년대에는 자동 관수 시스템이 설치되었고(가상화), 2020년대에는 **AI 기반 스마트 온실**이 날씨·계절·식물 상태를 센싱해 자동으로 물·빛·온도를 조절하는 것과 같다(클라우드 네이티브).

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **5계층 책임 분담 모델(Shared Responsibility Model)** 과 **탄력성(Elasticity)** 메커니즘이다. 물리적 데이터센터·하드웨어·하이퍼바이저는 CSP(Cloud Service Provider)가 책임지고, OS·미들웨어·런타임·데이터·애플리케이션·IAM은 사용자가 책임진다. 트래픽은 **Route 53 / Cloud DNS** -> **CDN(CloudFront/Cloudflare)** -> **API Gateway** -> **Load Balancer(ALB/NLB)** -> **Auto Scaling Group(K8s HPA/ECS Service)** -> **Application Pod(Lambda Function)** 순으로 흐르며, **Circuit Breaker(Resilience4j/Hystrix)** 패턴이 다운스트림 장애를 차단한다.

```text
                클라우드 아키텍처 4계층 + 7개 핵심 컴포넌트
   +----------------------------------------------------------------------+
   |  +--------------------------------------------------------------+   |
   |  | L7: Experience Layer    CDN(CloudFront) + WAF + Static Web   |   |
   |  +--------------------------------------------------------------+   |
   |  | L6: Edge & API Layer    API Gateway(REST/gRPC/WebSocket)      |   |
   |  |     +----------+  +----------+  +----------+                |   |
   |  |     | AuthN/Z  |  | Rate Lim |  | Routing  |                |   |
   |  |     | OAuth2.0 |  | Token Bk |  | Canary   |                |   |
   |  |     +----------+  +----------+  +----------+                |   |
   |  +--------------------------------------------------------------+   |
   |  | L5: Application Layer   MSA Microservices (Spring/Ballerina) |   |
   |  |     +----------+  +----------+  +----------+  +----------+  |   |
   |  |     | Order Svc|  | Pay Svc  |  | Inv Svc  |  | User Svc |  |   |
   |  |     |  Pod x12 |  | Pod x 8  |  | Pod x 6  |  | Pod x 4  |  |   |
   |  |     +-----+----+  +----+-----+  +----+-----+  +----+-----+  |   |
   |  |           +------------+--------------+-------------+        |   |
   |  |                       Service Mesh (Istio/Linkerd)           |   |
   |  |            mTLS | Retries | Circuit | Tracing | Metrics      |   |
   |  +--------------------------------------------------------------+   |
   |  | L4: Data Layer          Polyglot Persistence                 |   |
   |  |     +----------+  +----------+  +----------+  +----------+  |   |
   |  |     |  RDBMS   |  |  NoSQL   |  | Cache    |  | Object   |  |   |
   |  |     | Aurora   |  | DynamoDB |  | Redis    |  | S3/Minio |  |   |
   |  |     |(Strong)  |  |(Eventual)|  | (μs Lat) |  |(11x9 SLA)|  |   |
   |  |     +----------+  +----------+  +----------+  +----------+  |   |
   |  +--------------------------------------------------------------+   |
   |  | L3: Messaging Layer     Event Bus (Kafka/Kinesis/Pub/Sub)    |   |
   |  |     Event Sourcing | CQRS | Saga | Outbox Pattern            |   |
   |  +--------------------------------------------------------------+   |
   +----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | L7 라우팅·인증·트래픽 관리 | Kong/AWS API Gateway/Apigee, **OAuth 2.0 / JWT** 검증, **Rate Limiting(Token Bucket / Leaky Bucket)**, Request/Response 변환, gRPC-Web 트랜스코딩 |
| **Service Mesh (Istio/Linkerd)** | 서비스 간 통신·관찰성·보안 | **Envoy Sidecar** Proxy가 mTLS 1.3 암호화, **L7 Retries(지수 백오프)**, **Circuit Breaker(연결 풀 격리)**, **Distributed Tracing(OpenTelemetry/Jaeger)** 자동 주입 |
| **Container Orchestrator (K8s/ECS)** | 컨테이너 라이프사이클·스케줄링 | **Control Plane(API Server/etcd)** + Worker Node, **HPA**: CPU>70% 시 30초마다 Pod 증설, **VPA**: 리소스 권장값 재계산, **Cluster Autoscaler**: Pending Pod 발생 시 Node Pool 확장(보통 2~5분 소요) |
| **Object Storage (S3/GCS/Azure Blob)** | 비정형 데이터·정적 콘텐츠·백업 | **11x9 내구성(99.999999999%)** 보장, **Lifecycle Policy**: IA(30일)->Glacier(90일)->Deep Archive(365일), **Pre-signed URL** 로 임시 접근 권한 위임 |
| **Serverless (Lambda/Functions/Cloud Run)** | 이벤트 기반·단기 실행 워크로드 | **Cold Start**: 100ms~2s(런타임별 차이), **Warm Pool**: Provisioned Concurrency로 상시 워밍, **Event Source Mapping**: SQS/Kafka/DynamoDB Streams를 폴링/푸시 트리거 |
| **Message Broker (Kafka/RabbitMQ/SQS)** | 비동기·디커플링·백프레셔 처리 | **Kafka**: Partition 기반 순서 보장, **Consumer Group** 별 Offset 관리, **Exactly-Once Semantics(EOS)**: 트랜잭션 Producer + Idempotent Consumer 결합 |
| **Observability Stack (Prometheus/Grafana/ELK)** | 메트릭·로그·트레이스 3박자 | **RED Method**(Rate/Errors/Duration), **USE Method**(Utilization/Saturation/Errors), **SLI/SLO/SLA** 연계, SLO Error Budget 기반 배포 게이팅 |

**핵심 알고리즘 및 파라미터 심화:**

- **Auto-Scaling 결정 메커니즘**: K8s HPA는 `desiredReplicas = ceil[currentReplicas × (currentMetricValue / targetMetricValue)]` 공식으로 산출하며, **`--horizontal-pod-autoscaler-sync-period`(기본 15초)**, **`--horizontal-pod-autoscaler-upscale-delay`(기본 3분)**, **`--horizontal-pod-autoscaler-downscale-delay`(기본 5분)** 의 3개 안정화 윈도우가 플래핑(Flapping)을 방지한다.
- **Karpenter**: AWS에서 K8s Cluster Autoscaler 대비 **20배 빠른 노드 프로비저닝** (90초->45초), 70+ EC2 인스턴스 타입 중 Spot 우선 스케줄링, NodePool CRD로 가용 영역 분산.
- **Consensus Algorithm**: 분산 데이터스토어(etcd/Consul/DynamoDB)는 **Raft Consensus** 로 Leader Election + Log Replication, Quorum 크기 `2F+1` (F=허용 장애 노드 수).

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"항공 관제 시스템"** 과 같다. 탑승객(트래픽)이 늘면 활주로(컴퓨팅 자원)를 즉시 증설하고, 비행기(서비스)에 이상이 생키면 **자동 우회(라우팅)** 시키며, 모든 항공편의 **위치·고도·연료(메트릭)** 를 실시간 추적해 **충돌 방지(장애 격리)** 한다.

---

## Ⅲ. 비교 및 연결

클라우드 아키텍처 설계 시 유사 개념 간 정확한 구분이 시험 출제 빈도가 높다.

| 구분 | **Monolith** | **Microservice (MSA)** | **Serverless (FaaS)** | **Container (CaaS)** |
| :--- | :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 WAR/JAR/EAR | 독립 서비스별 컨테이너 | 함수(Function) 단위 | 컨테이너 이미지 단위 |
| **확장 단위** | 애플리케이션 전체 복제 | 서비스별 독립 확장 | 동시 실행 수(Concurrency) | Pod/ReplicaSet 단위 |
| **장애 격리** | 프로세스 단위(연쇄 장애) | 서비스 단위(완전 격리) | 함수 단위(자동 격리) | 컨테이너 단위(격리) |
| **State 관리** | In-Memory 공유 | 외부 DB/Redis 분리 | **반드시 Stateless** (외부 저장소 필수) | StatefulSet/PVC로 관리 가능 |
| **Cold Start** | 없음 | 이미지 pull 시간(수 초) | **100ms~2s** (런타임 의존) | **수 초~수십 초** (이미지 크기 의존) |
| **적합 워크로드** | 소규모·CRUD 단순 앱 | 복잡 도메인·대규모 트래픽 | **Event-Driven·간헐적·예측 불가** | **장기 실행·일관성 있는 워크로드** |
| **DevOps 복잡도** | 낮음 | 높음(Service Mesh/CI-CD) | 매우 높음(Event 분산 추적) | 중간(K8s 운영 필요) |
| **비용 모델** | 상시 과금(고정 인스턴스) | 사용량 기반(Pod·CPU·Mem) | **호출 횟수+GB-Second** 종량제 | 노드 시간 과금 |
| **Vendor Lock-in** | 없음 | 부분 종속(Lib/Lang) | 높음(CSP별 트리거·런타임) | 낮음(K8s 표준) |
| **대표 사례** | 전통 SI 프로젝트 | Netflix·Amazon·우아한형제들 | AWS Lambda·Cloud Functions | Docker Swarm·K8s/ECS |

**다른 시스템 컴포넌트와의 연결 관계:**

- **SDN(Software Defined Network)** ↔ 클라우드: AWS VPC는 **Overlay 네트워크(VXLAN/Geneve)** 로 논리적 L2/L3 분리, Transit Gateway로 VPC Peering의 N×(N-1)/2 메시 한계 극복.
- **DevSecOps** ↔ 클라우드: IaC 스캔(Terraform `tfsec`/`checkov`), 컨테이너 이미지 스캔(Trivy/Snyk), 정책 코드화(OPA/Gatekeeper), 시크릿 관리(AWS Secrets Manager/Vault).
- **DBA 영역** ↔ 클라우드: RDS Proxy로 커넥션 풀링, Aurora Global Database로 **1초 미만 RTO·RPO** 멀티리전 복제, DynamoDB DAX로 마이크로초 캐싱.

- **📢 섹션 요약 비유**: 이 4가지 아키텍처는 **"식당 운영 방식"** 에 비유된다. Monolith는 **단일 셰프가 모든 요리**를 만드는 정통 레스토랑, MSA는 **요리별 전문 셰프** 가 협업하는 풀서비스 레스토랑, Container는 **셰프가 정해진 레시피(컨테이너)대로 움직이는 키친**, Serverless는 **고객이 주문할 때만 잠깐 일하는 출장 셰프**와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

클라우드 아키텍처 설계는 **비기능 요건(가용성·확
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 580 / 800

<- **이전**: [579. 클라우드 아키텍처 핵심 토픽 579번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/579_cloud_architecture_core_topic_579_exam_summar/)
**다음**: [581. 클라우드 아키텍처 핵심 토픽 581번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/581_cloud_architecture_core_topic_581_exam_summar/) ->

---
