---
title: "Cloud Architecture Core Topic 557 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST 참조모델(IaaS/PaaS/SaaS × Public/Private/Hybrid/Community)과 Well-Architected Framework(운영 우수성·보안·안정성·성능 효율·비용 최적화·지속가능성 6대 기둥)를 기반으로, 컨테이너 오케스트레이션(Kubernetes), 서비스 메시(Istio/Linkerd), 선언형 API(Infrastructure as Code), 그리고 분산 시스템 이론(CAP/BASE/Eventually Consistent)을 유기적으로 결합한 아키텍처 청사진이다.
> 2. **가치**: 온프레미스 대비 TCO 30~50% 절감, Auto-Scaling을 통한 트래픽 변동 대응력(평균 8배 Burst 처리), Multi-AZ 가용성 99.99%(52.6분/년 다운타임) 달성, Time-to-Market를 신규 인프라 구성 기준으로 16주->30분으로 단축한다.
> 3. **판단 포인트**: 12-Factor App 준수 여부, 클라우드 락인(Cloud Lock-in) vs Multi-Cloud 전략, 동기식 결합(Strong Coupling) vs 비동기식 이벤트 기반(Event-Driven) 트레이드오프, Stateless 컴포넌트 비율과 데이터 일관성 모델 선택이 아키텍처 성패를 좌우한다.

---

## Ⅰ. 개요 및 필요성

클라우드 컴퓨팅은 2006년 AWS S3와 EC2 출시 이후, 단순한 "외부 호스팅"에서 "분산 시스템의 운영체제"로 진화했다. 4차 산업혁명 시대의 데이터 폭증(전 세계 데이터 생성량 2025년 175ZB 전망), 트래픽 변동성 가속화, 그리고 디지털 트랜스포메이션 압박에 따라, 레거시 모놀리식 아키텍처로는 다음 3가지 핵심 한계에 부딪힌다.

```
[기존 아키텍처의 한계]

   +------------------+    +------------------+    +------------------+
   | Capacity Planning|    |  Scale-out 제약   |    | 운영 오버헤드     |
   |  (수동 용량예측)  |    |  (수직확장 한계)   |    | (OS/미들웨어 패치)|
   +--------+---------+    +--------+---------+    +--------+---------+
            v                       v                       v
   +----------------------------------------------------------------+
   |   Peak Load 기준으로 HW 과다구매 -> 유휴자원 60~70%             |
   |   디스크 추가/RAID 재구성 시 수시간 다운타임                     |
   |   Active-Active 구성 시 세션/DB 동기화 난이도 ^                 |
   +----------------------------------------------------------------+

[클라우드 네이티브 아키텍처로의 전환]

   +------------------+    +------------------+    +------------------+
   | Auto-Scaling     |    |  무한 Scale-out   |    | Managed Service  |
   | (HPA/VPA/CA)     |    | (Pet->Cattle)     |    | (운영 자동화)     |
   +--------+---------+    +--------+---------+    +--------+---------+
            v                       v                       v
   +----------------------------------------------------------------+
   |   선언형 정책 기반 탄력적 확장(예: K8s HPA CPU 70% 기준)        |
   |   API 호출만으로 Region 1분 내 신규 리소스 provisioning          |
   |   콘솔/CLI/IaC(Terraform/Pulumi) 기반 프로비저닝 자동화         |
   +----------------------------------------------------------------+
```

**왜 클라우드 아키텍처인가?**
- **CapEx -> OpEx 전환**: 자산 구매 모델에서 사용량 기반 종량제(Pay-as-you-go)로 재무구조 혁신
- **가용성 SLA**: AWS EC2 단일 인스턴스 SLA 99.5%, Multi-AZ Auto-Scaling Group 적용 시 99.99% 보장
- **글로벌 확장성**: CloudFront/Cloudflare 같은 CDN 엣지 노드를 통해 전 세계 200+ PoP에서 ms 단위 응답
- **기술 민주화**: ML(SageMaker/Bedrock), IoT Core, Quantum(Braket) 등 고가 장비를 API 한 줄로 활용

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "호텔 체인"과 같다. 매번 빌딩을 짓는 게 아니라, 예약 시스템(API)만 호출하면 전 세계 어디서나 객실(컴퓨팅)을 즉시 받고, 체크아웃(인스턴스 종료) 시 자동 정산된다. 호텔 측은 객실 수를 수요에 맞춰 즉시 증축한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **"추상화(Abstraction)"와 "자동화(Automation)"의 결합**이다. 이를 4계층 모델로 분해하면 다음과 같다.

```
[클라우드 아키텍처 4계층 + Cross-cutting Concerns]

   +--------------------------------------------------------------------+
   |  L4. Application Layer  (Stateless Microservice, API Gateway)      |
   |      +-> 12-Factor App, BFF, Saga Pattern, Event Sourcing         |
   +--------------------------------------------------------------------+
   |  L3. Platform Layer     (Container Orchestration, Service Mesh)   |
   |      +-> Kubernetes, Istio, ArgoCD, KEDA, Knative                 |
   +--------------------------------------------------------------------+
   |  L2. Infrastructure Layer (IaC, Multi-Cloud, Edge)                |
   |      +-> Terraform, Pulumi, Crossplane, Vagrant                   |
   +--------------------------------------------------------------------+
   |  L1. Resource Layer      (Compute/Storage/Network Managed Service)|
   |      +-> EC2/EKS, S3/EBS, VPC/CloudFront, Lambda/Functions       |
   +--------------------------------------------------------------------+

   +------------------------------------------------------------------+
   | Cross-Cutting: Observability(Prometheus/Grafana/OpenTelemetry)   |
   |                Security(Zero-Trust/IAM/OAuth2.0/mTLS)             |
   |                Governance(OPA/Kyverno/FinOps)                    |
   +------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | L7 트래픽 라우팅/인증/속도제어 | AWS API Gateway, Kong, Envoy Gateway, Apigee — OAuth 2.0/JWT 검증, Rate Limiting(예: 1000 RPS per key), Circuit Breaker 통합 |
| **Service Mesh** | 서비스 간 통신·관찰성·정책 주입 | Istio(Envoy sidecar), Linkerd, Consul Connect — mTLS 자동 적용, 카나리 배포(10%->50%->100%), 분산 트레이싱 전파 |
| **Container Orchestrator** | 컨테이너 스케줄링·자기치유·롤링 업데이트 | Kubernetes(K8s) 1.30+, ECS Fargate, Nomad — Control Plane(etcd)+Worker Node, Deployment/ReplicaSet/HPA 구조, Pod 단위 IP 할당 |
| **Object Storage / Data Lake** | 비정형 데이터·정적 콘텐츠·백업 | S3, GCS, Azure Blob, MinIO — 11 9s 내구성(99.999999999%), Lifecycle Policy 기반 자동 계층화(Standard->IA->Glacier), Pre-signed URL 임시 권한 |
| **Event Bus / Streaming** | 비동기 메시징·이벤트 라우팅 | Kafka, AWS Kinesis, EventBridge, Pub/Sub, NATS — Exactly-Once Semantics, Dead Letter Queue, Consumer Group 기반 병렬 처리 |
| **IaC Engine** | 인프라 선언적 프로비저닝 | Terraform(HCL), Pulumi(TypeScript/Python), AWS CDK, Ansible — State 관리(원격 Lock), Plan/Apply 분리, Module 재사용 |
| **Observability Stack** | 메트릭·로그·트레이스 통합 | Prometheus(메트릭 수집)+Loki(로그)+Tempo(트레이스) + Grafana(시각화), OpenTelemetry SDK, USE/RED 메서드 적용 |

### 핵심 메커니즘: Kubernetes를 중심으로

```text
[K8s 클러스터 내부 구조 + Control Loop]

   kubectl apply -f deployment.yaml
            |
            v
   +------------------+    watch   +----------------------+
   |  kube-apiserver  |◄----------►|  etcd (분산 KV 저장)  |
   +--------+---------+            +----------------------+
            | 인증/인가 (RBAC, OIDC)
            v
   +------------------+
   |  kube-scheduler  | ◄-- 노드 리소스, Affinity, Taint/Toleration
   +--------+---------+
            v
   +------------------+    reconcile loop   +--------------------+
   |  kubelet (Agent) |◄--------------------|  Controller Manager|
   |  on Worker Node  |                     |  (Deployment, HPA) |
   +--------+---------+                     +--------------------+
            v
   +--------------------------------------------------+
   | Pod(1~N Container) -> Pause Container + App Image |
   |   +-> sidecar(Envoy), init container, main app   |
   +--------------------------------------------------+

[Auto-Scaling 메커니즘 3종]
   HPA(Horizontal): CPU/Memory/Custom Metric(QPS, Queue Length) 기반 Replica 증감
   VPA(Vertical):   Pod의 requests/limits 자동 조정 (OOM 방지)
   CA(Cluster):     노드 풀 자체 확장 (AWS EKS Managed Node Group / Karpenter)
```

**핵심 파라미터와 알고리즘**:
- **Consistent Hashing**: 오브젝트 스토리지·CDN 캐시 노드 선택 알고리즘, 가상 노드(Virtual Node) 256개로 키 분산 시 편향 최소화
- **Quorum 기반 합의**: etcd/ZooKeeper는 Raft 알고리즘으로 N=3(쓰기 2 필요)/N=5(쓰기 3 필요) 구성
- **Split-Brain 방지**: AWS DynamoDB는 Vector Clock + Sloppy Quorum + Hinted Handoff로 일시적 네트워크 단절 대응
- **Graceful Shutdown**: K8s Pod 종료 시 `preStop` hook -> SIGTERM -> `terminationGracePeriodSeconds`(기본 30s) -> SIGKILL

- **📢 섹션 요약 비유**: K8s 클러스터는 "오케스트라"다. 단일 악기(컨테이너)는 약하지만, 지휘자(Control Plane)가 악보(IaC)를 읽고, 각 연주자(노드)가 정확한 박자(ReplicaSet)에 맞춰 연주하면, 한 명이 아프면(preStop) 대기자가 즉시 들어와(Cordon/Drain) 끊김 없는 공연이 가능하다.

---

## Ⅲ. 비교 및 연결

### A. 배포 모델(Deployment Model) 비교

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **소유권** | Hyperscaler(AWS/Azure/GCP) | 자체 IDC/Hosting | Public + Private | 2개 이상 Public |
| **규제 준수** | 일반 컴플라이언스 | 금융/공공 데이터 주권 | 데이터 분류별 분리 | 베endor 종속 회피 |
| **확장성** | 무제한(탄력적) | 물리적 한계 | Burst 시 Public 활용 | 워크로드별 최적 CSP |
| **TCO** | OPEX 종량제 | CAPEX+OPEX | 양쪽 합산 | 통합 비용 20~30% ^ |
| **대표 사례** | Netflix, Airbnb | Banks, Defense | Banking Core(Private) + Web(Public) | Netflix(AWS+GCP) |
| **지연 시간** | 리전별 5~50ms | 인접 IDC 1~5ms | 전용선(DX/Interconnect) 10~20ms | 리전 간 50~200ms |
| **마이그레이션 난이도** | 낮음(친화적) | 높음(OpenStack 학습) | 중간 | 매우 높음 |

### B. 서비스 모델(Service Model) 비교

| 구분 | On-Premise | IaaS | PaaS | SaaS | FaaS(Serverless) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | 전체 직접 관리 | OS까지 사용자 | App까지 사용자 | 모두 CSP | 코드만 사용자 |
| **확장 단위** | Server | VM | Container/App | 사용자 단위 | Event/요청 단위 |
| **콜드 스타트** | N/A | N/A | N/A | N/A | 100ms~3s(Lambda) |
| **장점** | 완전한 통제권 | 유연성 ^ | 개발 생산성 ^ | 즉시 사용 | 사용량 기반 과금(0->N) |
| **단점** | 운영 부담 큼 | IaaS Lock-in | 이식성 v | 커스터마이징 한계 | 콜드 스타트·상태 관리 |

### C. 기존 분산 시스템과의 연결

| 패러다임 | 연관 기술 | 클라우드 아키텍처로의 진화 |
| :--- | :--- | :--- |
| **SOA(2000s)** | ESB, WSDL, SOAP | -> API Gateway + Microservice + REST/gRPC |
| **모놀리식(2010s)** | 3-Tier, WAR/EAR | -> 컨테이너화(Docker) -> Strangler Fig Pattern |
| **전통 RDBMS** | Oracle RAC, MySQL Replication | -> Managed Service(RDS/Aurora/Cloud SQL) + Read Replica + Sharding |
| **전통 메시지 큐** | ActiveMQ, RabbitMQ | -> Event Streaming(Kafka/MSK) + EventBridge |
| **전통 캐시** | Memcached/Redis 단독 | -> ElastiCache + DAX(DynamoDB Accelerator) + Global Datastore |

### D. CAP Theorem과 일관성 모델

```
   [CAP Triangle]
                          Consistency
                            ^
                           ╱|╲
                          ╱ | ╲
                         ╱  |  ╲
                        ╱   |   ╲
                       ╱ CP | AP ╲
                      ╱  (RDBMS)|  ╲
                     ╱          |   ╲
                    ╱-----------+----╲
            Availability -----►Partition
                                Tolerance

   * AP 예: DynamoDB, Cassandra — Eventual Consistency + Sloppy Quorum
   * CP 예: etcd, ZooKeeper, HBase — 쓰기 가용성 v, 강한 일관성
   * CA 예: 전통 RDBMS (단
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 557 / 800

<- **이전**: [556. 클라우드 아키텍처 핵심 토픽 556번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/556_cloud_architecture_core_topic_556_exam_summar/)
**다음**: [558. 클라우드 아키텍처 핵심 토픽 558번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/558_cloud_architecture_core_topic_558_exam_summar/) ->

---
