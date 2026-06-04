---
title: "560. 클라우드 아키텍처 핵심 토픽 560번 시험 요약 (Cloud Architecture Core Topic 560 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 가상화·컨테이너·오케스트레이션·IaC를 기반으로 한 분산 시스템의 구조적 설계이며, Well-Architected Framework(안정성·보안·성능·비용·운영 우수성·지속가능성 6대 pilares)와 Cloud Native Computing Foundation(CNCF) 생태계가 표준 참조 모델이다.
> 2. **가치**: CapEx->OpEx 전환(평균 30~40% TCO 절감), Auto Scaling으로 트래픽 변동 대응(처리량 10배 확장 시 약 8분 내), Region/AZ 다중화 통해 99.99% SLA 달성, Multi-Cloud로 벤더 락인 제거 및 가용성 99.999% 구현이 가능하다.
> 3. **판단 포인트**: 단일 Cloud vs Multi/Hybrid 선택, Monolith->Microservices->Serverless 진화 단계, 동기·비동기·이벤트 기반 통신 방식, Stateful·Stateless 워크로드 분리, FinOps 기반 비용 최적화 전략이 핵심 의사결정 변수다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-tier 아키텍처는 정적 Capacity Planning, 수직적 확장(Scale-Up), CapEx 중심 투자라는 한계를 가진다. 트래픽 피크 시 유휴 자원 발생, 장애 발생 시 DR(Disaster Recovery) 사이트 별도 구축, HW 수명주기에 따른 갱신 비용(보통 5년 주기) 등의 문제가 누적된다. 2006년 AWS S3·EC2 출시 이후 클라우드는 가상화(KVM/Xen->Firecracker), Software-Defined Networking(SDN), Software-Defined Storage(SDS), API 기반 자원 프로비저닝을 통해 자원 탄력성(Elasticity), 종량제(Pay-per-use), 글로벌 엣지 배포를 실현했다.

```text
+---------------------------------------------------------------------+
|             On-Premise -> Cloud 전환 패러다임 비교                    |
+------------------------------+--------------------------------------+
|  On-Premise (전통)            |  Cloud-Native (현대)                  |
+------------------------------+--------------------------------------+
|  [사용자]                     |  [사용자]                             |
|      |                        |      |                                |
|  [L4 Switch]                  |  [CDN/Edge (CloudFront, Cloudflare)] |
|      |                        |      |                                |
|  [Web/App Server Cluster]     |  [API Gateway + WAF]                 |
|      |   ↕ 고정 Capacity      |      |   ↕ Auto Scaling (HPA/VPA)    |
|  [DBMS + SAN Storage]         |  [Microservices + Service Mesh]      |
|      |                        |      |   ↕ Service Discovery         |
|  [DC 운영인력 / HW 유지보수]  |  [Managed DB + Object Storage]       |
|                              |      |   ↕ IaC (Terraform/CDK)        |
|  CapEx 과다, Scale-Up 한계   |  OpEx 종량제, Scale-Out 무제한       |
|  DR 24~48h, HA Active-Standby|  DR RPO<1분 RTO<분, Multi-AZ Active  |
+------------------------------+--------------------------------------+
```

NIST SP 800-145는 클라우드를 5대 특성(요구 기반 자가서비스, 광범위한 네트워크 접근, 자원 풀링, 빠른 탄력성, 측정 가능한 서비스)과 3대 서비스 모델(IaaS/PaaS/SaaS), 4대 배치 모델(Public/Private/Hybrid/Community)로 정의한다. Gartner는 2025년 기준 전체 IT 지출의 51% 이상이 Public Cloud로 이동할 것으로 예측했으며, 한국 클라우드 시장은 2027년 약 30조 원 규모로 성장 전망된다.

- **📢 섹션 요약 비유**: On-Premise가 "소유한 발전소에서 직접 전기를 만드는 것"이라면, 클라우드는 "전력망에 연결해 필요한 만큼만 콘센트에서 뽑아 쓰는 것"과 같다. 발전소(서버실) 증축 없이도 콘센트(API)만으로 무제한 확장이 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 네이티브 아키텍처는 CNCF의 정의에 따라 **컨테이너, 서비스 메시, 마이크로서비스, 불변 인프라(Immutable Infrastructure), 선언적 API**를 핵심으로 한다. 12-Factor App 원칙(코드베이스 단일화, 의존성 명시, Config 환경변수 분리, 백킹 서비스, 빌드/릴리스/런 분리, Stateless 프로세스, 포트 바인딩, 동시성, Disposable, Dev/Prod 일치, 로그 이벤트 스트림, Admin 프로세스)이 기본 설계 제약이다.

```text
+----------------------------------------------------------------------+
|           Cloud-Native Reference Architecture (4계층)                |
|                                                                      |
|  +--------------------------------------------------------------+    |
|  | Layer 4: Application (Stateless Microservice / Function)     |    |
|  |  - Spring Boot, Node.js, FastAPI, Lambda, Cloud Functions    |    |
|  |  - 비즈니스 로직, API Contract (OpenAPI/gRPC)                |    |
|  +------------------+-------------------------------------------+    |
|                     |  mTLS, gRPC/HTTP2, Circuit Breaker             |
|  +------------------+-------------------------------------------+    |
|  | Layer 3: Service Mesh + API Gateway                          |    |
|  |  - Istio/Linkerd (Sidecar: Envoy) - 트래픽 관리, 관측        |    |
|  |  - Kong/AWS API Gateway - 인증, Rate Limit, Transformation   |    |
|  +------------------+-------------------------------------------+    |
|                     |  Container Networking (CNI)                    |
|  +------------------+-------------------------------------------+    |
|  | Layer 2: Orchestration (Kubernetes)                          |    |
|  |  - Control Plane: API Server, etcd, Scheduler, Controller    |    |
|  |  - Worker Node: kubelet, kube-proxy, Container Runtime       |    |
|  |  - Add-ons: CoreDNS, Ingress, HPA, VPA, Cluster Autoscaler  |    |
|  +------------------+-------------------------------------------+    |
|                     |  OCI Runtime Spec, cgroups, namespaces         |
|  +------------------+-------------------------------------------+    |
|  | Layer 1: Infrastructure (IaaS)                               |    |
|  |  - Hypervisor: KVM/Hyper-V/AWS Nitro/Azure Hyper-V           |    |
|  |  - SDN: VPC, Subnet, Security Group, Transit Gateway         |    |
|  |  - IaC: Terraform, Pulumi, AWS CDK, Ansible                 |    |
|  +--------------------------------------------------------------+    |
|                                                                      |
|  Cross-cutting: Observability(Prom/Grafana/Loki/Tempo)              |
|                 Security(OAuth2/OIDC, Vault, OPA, KMS)               |
|                 CI/CD(ArgoCD/Flux, Tekton, GitHub Actions)           |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **컴퓨트 (Compute)** | 워크로드 실행 환경 제공 | VM(KVM/Nitro), 컨테이너(Docker/containerd), Firecracker microVM(125ms 부팅, 5MB 메모리), Lambda(최대 15분 실행, 10GB 메모리) |
| **스토리지 (Storage)** | 데이터 영속성 및 접근 패턴 최적화 | Block(EBS io2: 256K IOPS, NVMe), Object(S3: 99.999999999% 내구성, 11 9s), File(EFS/FSx for Lustre: GB/s 처리량), Cold(S3 Glacier IR/Deep Archive) |
| **네트워크 (Network)** | 서비스 간 통신 및 트래픽 제어 | VPC/Subnet(IPv4/IPv6 Dual Stack), Transit Gateway(리전 간 최대 50Gbps), PrivateLink(프라이빗 엔드포인트), Global Accelerator(Anycast IP, 엣지 라우팅), Cloud WAN |
| **오케스트레이션 (Orchestration)** | 컨테이너 라이프사이클 관리 | Kubernetes(etcd Raft 합의, Controller Loop), Karpenter(Just-in-time 노드 프로비저닝, 50% 비용 절감), Cluster Autoscaler, Kustomize/Helm |
| **데이터베이스 (Database)** | 트랜잭션·분석·캐시 계층 | RDBMS(Aurora: 5x MySQL, 3x PostgreSQL 성능, 6-way 복제), NoSQL(DynamoDB: 단일 자리수 ms, 10 trillion req/day), Redis(ElastiCache: sub-ms), NewSQL(CockroachDB, Spanner) |
| **보안·거버넌스 (Security)** | 제로 트러스트, 규정 준수, 암호화 | IAM(RBAC/ABAC), KMS(Envelope Encryption, FIPS 140-2 Level 3 HSM), WAF/DDoS(Shield Advanced: L3/L4/L7), Secrets Manager, CloudTrail/Lake |

**핵심 알고리즘 및 파라미터:**
- **Auto Scaling 결정**: `desiredReplicas = ceil[currentReplicas × (currentMetricValue / targetMetricValue)]` (HPA 공식, 30초 폴링, 5분 안정화 윈도우)
- **CAP 정리**: RDBMS는 CA 우선(2PC, Paxos 합의), DynamoDB/Cassandra는 AP 우선(벡터 클럭 + sloppy quorum, `R + W > N` 일관성 튜닝)
- **일관성 해시**: DynamoDB Partition Key 기반 분할, Virtual Node 256개/서버로 키 재분산 최소화
- **Saga 패턴**: 마이크로서비스 분산 트랜잭션 보상 트랜잭션(Camunda/Temporal 워크플로우, Choreography vs Orchestration)
- **Quorum**: `W + R > N` -> 강한 일관성, `W=1, R=1` -> 결과적 일관성(Eventual Consistency, 보통 < 1초)

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "만리장성"과 같다. 외곽(WAF/Edge)->안내소(API Gateway)->초소(Container)->통신로(Service Mesh)->병사(Pod)->지휘부(Control Plane)->물자창고(Storage)가 계층적으로 분리되어, 한 초소가 함락되어도 전체가 무너지지 않는다.

---

## Ⅲ. 비교 및 연결

| 구분 | **IaaS (예: EC2, GCE, Azure VM)** | **PaaS (예: Beanstalk, App Engine, Heroku)** |
| :--- | :--- | :--- |
| **관리 범위** | OS, 미들웨어, 런타임, 데이터, 앱 모두 사용자 관리 | 앱과 데이터만 관리, 나머지 PaaS 제공자가 관리 |
| **유연성** | 매우 높음 (커스텀 AMI, 커널 패치, GPU 패스스루) | 중간 (지원 런타임/미들웨어 제약) |
| **확장성** | 수동/Auto Scaling Group (분 단위) | 자동 (트래픽 기반 즉시, 0->N 스케일링) |
| **적합 워크로드** | 레거시 모놀리식, 특수 HW 요구, HPC | 웹앱 API, 표준 스택, 빠른 배포 |
| **TCO (3년)** | 중간 (관리자 인건비 포함) | 낮음 (운영 부담 절감) |
| **제어 수준** | 네트워크 패킷 단위 제어, SG/NACL/iptables | 플랫폼 제공 인터페이스 내 |

| 구분 | **Monolithic** | **Microservices** | **Serverless (FaaS)** |
| :--- | :--- | :--- | :--- |
| **배포 단위** | 단일 바이너리 (수백 MB~GB) | 컨테이너 이미지 (100~500MB) | 함수 코드 (KB~수 MB) |
| **확장 단위** | 앱 인스턴스 전체 복제 | 서비스별 독립 | 함수 호출 단위 (Concurrency) |
| **장애 격리** | 약함 (메모리/CPU 공유) | 강함 (Process 분리) | 강함 (샌드박스/VM 격리) |
| **Cold Start** | 30~60초 (앱 부팅) | 1~5초 (이미지 풀+시작) | 100ms~5초 (Lambda, 언어별 차이) |
| **상태 관리** | In-memory 가능 | 외부 Store 필수 (DB/Redis) | Stateless 강제, 외부 의존 |
| **적합 시나리오** | 초기 MVP, 소규모 팀 | 중규모 이상, 다기능 도메인 | 이벤트 기반, 간헐적 트래픽 |

**연계 통합 포인트:**
- **CDN/Edge**: CloudFront/Cloudflare가 API Gateway 앞단에서 TLS 종료, 정적 캐시, Lambda@Edge로 엣지 컴퓨팅
- **메시지 브로커**: Kafka(처리량 1M msg/s, Exactly-Once), SQS/SNS(완전 관리형, at-least-once), EventBridge(SaaS 이벤트 버스)
- **관측 가능성**: OpenTelemetry(OTLP 표준) -> Prometheus(Metrics) + Loki(Logs) + Tempo/Jaeger(Traces) 3-Pillar 통합
- **CI/CD**: GitOps(ArgoCD/Flux) -> 매니페스트 Git 동기화, Progressive Delivery(Argo Rollouts: Blue/Green, Canary 1%->10%->50%->100%)
- **IaC 계층**: Terraform(상태 파일 S3+DynamoDB Lock) -> Ansible(설정) -> Helm(K8s 패키지) -> Kustomize(오버레이)

- **📢 섹션 요약 비유**: IaaS는 "빈 셸터(land)만 빌려주는 것", PaaS는 "인테리어까지 마친 오피스텔", Serverless는 "짐만 들고 가면 룸서비스까지 받는 호텔"이다. 비싸지만 손이 안 가는 대신, 묶이는 규격이 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **워크로드 분류를 수행했는가?** 워크로드를 Stateful vs Stateless, Latency-Critical(ms) vs Throughput-Critical, Batch vs Interactive로 분류하고, 각각 Compute/Storage/Network 자원을 매핑했는지 확인. OLTP는 컴퓨트+메모리 최적화, OLAP는 스토리지 I/O+네트워크 대역폭 최적화.
2. **Multi-AZ/Region 가용성 등급을 정의했는가?** RTO/RPO 목표를 SLA(99.9%/99.99%/99.999%)에 맞춰 설정. Active-Active 다중 리전은 비용 2배, Pilot Light는 비용 30%, Warm Standby는 60%. 데이터 복제 방식(Sync/Async) 및 DNS 페일오버( Route53 Health Check, TTL 60초) 결정.
3. **보안 제로 트러스트 원칙을 적용했는가?** 모든 통신에 mTLS, 최소 권한 IAM(IAM Access Analyzer로 정책 검증), 데이터 암호화(At-Rest KMS, In-Transit TLS 1.3), VPC 엔드포인트로 Public Internet 차단, Secrets Manager로 자격증명 회전(90일).
4. **FinOps 비용 최적화 전략을 수립했는가?** Reserved Instance(1~3년, 최대 72% 할인) vs Savings Plan vs Spot Instance(최대 90% 할인, Interrupt 위험). Graviton(ARM64) 인스턴스로 동일 성능 대비 20~40% 비용 절감. S3 Intelligent-Tiering, EBS gp3 마이그레이션. Cost Anomaly Detection 알람 설정.
5. **관측 가능성 3-Pillar를 통합했는가?** RED 메트릭(Rate/Error/Duration), USE 메트릭(Utilization/Saturation/Error), 분산 트레이싱(Span Context 전파 W3C TraceContext), 구조화 로그(OpenTelemetry SDK). MTTR(Mean Time To Recovery) < 15분 목표 SLO 정의.

### 피해야 할 안티패턴

- **"Lift-and-Shift 무분별 적용"**: 단순 VM 이전은 클라우드 이점 미활용. Refactor/Replatform 없이 비용만 30~50% 증가하는 경우 빈번. 6R 전략(Rehost/Replatform/Repurchase/Refactor/Retire/Retain) 중 최소 Replatform 이상 권장.
- **"단일 거대 컨테이너 배포
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 560 / 800

<- **이전**: [559. 클라우드 아키텍처 핵심 토픽 559번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/559_cloud_architecture_core_topic_559_exam_summar/)
**다음**: [561. 클라우드 아키텍처 핵심 토픽 561번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/561_cloud_architecture_core_topic_561_exam_summar/) ->

---
