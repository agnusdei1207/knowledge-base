---
title: "Cloud Architecture Core Topic 729 Exam Summary"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 CAP 정리를 넘어 **12-Factor App, Cell-Based Architecture, Cell-Based Reliability(Netflix), Sidecar/Ambassador Pattern(서비스 메시), SLO/Error Budget 기반 운영**을 통합한 **탄력적 분산 시스템 설계 체계**이며, AWS Well-Architected Framework 6대 축(운영우수성, 보안, 안정성, 성능효율성, 비용최적화, 지속가능성)과 CNCF Cloud Native Trail Map이 시험의 평가 기준선이다.
> 2. **가치**: Auto Scaling + Multi-AZ + Multi-Region 구성을 통해 **단일 리전 가용성 99.99%(연 52분 장애), 글로벌 가용성 99.999%(연 5분 장애)** 달성이 가능하며, Pay-per-Use 모델로 **CapEx 대비 OpEx 전환 시 약 30~40% TCO 절감**, 컨테이너 오케스트레이션 도입 시 배포 주기 **수개월 -> 수시간**, 장애 복구 시간(MTTR) **평균 70% 단축** 효과가 검증되어 있다.
> 3. **판단 포인트**: **단일 클라우드 종속(Vendor Lock-in) vs Multi-Cloud(추상화 계층 비용)**, **Synchronous Replication(낮은 RPO vs 높은 비용) vs Asynchronous(저비용 vs 데이터 손실 가능)**, **Strong Consistency vs Eventual Consistency**, **Serverless(콜드 스타트 vs 무제한 확장) vs Container(상시 워밍 vs 운영 부담)**의 트레이드오프를 **RTO/RPO, 트래픽 패턴, 데이터 주권, 규제 요건**과 함께 의사결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 아키텍처는 **수직 확장(Scale-Up)** 방식의 모놀리식(Monolithic) 애플리케이션을 SAN/NAS 기반 스토리지와 메인프레임급 RDBMS(MySQL, Oracle RAC)에 의존했으며, 트래픽 증가 시 **"예측 과잉 프로비저닝(Over-provisioning)"**으로 인한 유휴 자원률 60~70%, CAPEX 회수 기간 5~7년, 장애 복구 RTO 수 시간~수 일이라는 구조적 한계를 가졌다. 또한 DC 건설/증설에는 평균 12~18개월, 네트워크 회선 증설에는 3~6개월이 소요되어 **"Time-to-Market"** 요구사항을 충족하지 못했다.

클라우드 아키텍처는 AWS(2006년 EC2 출시)를 기점으로 **가상화(KVM, Xen, Hyper-V) -> 컨테이너화(Docker 2013) -> 오케스트레이션(Kubernetes 2015) -> 서버리스(Lambda 2014) -> 서비스 메시(Istio 2017) -> eBPF 기반 관측가능성(Cilium 2021)**로 진화해왔으며, **"Infrastructure as Code(Terraform, Pulumi, CloudFormation)", "Immutable Infrastructure", "Pet vs Cattle 서버"** 패러다임을 통해 **선언적(Declarative) 인프라 관리**와 **자동화된 회복 탄력성(Self-healing)**을 달성한다. 2024년 기준 글로벌 퍼블릭 클라우드 시장 규모는 약 6,800억 USD로 성장했으며, Gartner는 2027년 엔터프라이즈 IT 지출의 **51%**가 퍼블릭 클라우드로 전환될 것으로 전망한다.

```text
+---------------------------------------------------------------------+
|        전통 On-Premise 아키텍처                  Cloud-Native 아키텍처        |
+---------------------------------------------------------------------+
|                                                                     |
|  [사용자]            [사용자]                                       |
|      |                  |                                          |
|      v                  v                                          |
|  +--------+         +--------+     +--------------+                |
|  |L4/L7   |         |  CDN   |----->| Edge/CloudFront|              |
|  |Switch  |         |(CloudF)|     | (Anycast)    |                |
|  +----+---+         +----+---+     +------+-------+                |
|       |                  |                |                        |
|       v                  v                v                        |
|  +---------+       +----------+    +----------+                  |
|  |WebLogic|      |ECS Fargate|    | Lambda   |                    |
|  |(모놀리식)|      |(컨테이너)  |    |(이벤트기반)|                   |
|  +----+----+       +----+-----+    +----+-----+                    |
|       v                  v                v                        |
|  +---------+       +----------+    +----------+                  |
|  |Oracle   |       |Aurora    |    | DynamoDB |                    |
|  |RAC      |       |Multi-Master|   |(NoSQL)   |                   |
|  +----+----+       +----+-----+    +----+-----+                    |
|       v                  v                v                        |
|  +---------+       +----------+    +----------+                  |
|  |SAN/NAS  |       |S3/Glacier|    |S3+RRS    |                    |
|  |(RAID 5) |       |(11 9s)   |    |(99.99%)  |                    |
|  +---------+       +----------+    +----------+                  |
|                                                                     |
|  수직확장(Scale-Up)         수평확장(Scale-Out) + 탄력적 자동화           |
|  CAPEX 중심                  OPEX 중심 (Pay-per-Use)                  |
|  수동 운영                    IaC + GitOps 자동화                       |
+---------------------------------------------------------------------+
```

클라우드 네이티브의 핵심은 단순한 "클라우드 사용"이 아니라 **"애플리케이션이 클라우드 환경의 특징(탄력성, 분산, 자동화)을 최대한 활용하도록 설계"**되는 것이다. CNCF(Cloud Native Computing Foundation)는 **"Containers, Service Mesh, Microservices, Immutable Infrastructure, Declarative APIs"**를 5대 핵심 요소로 정의하며, Google은 **"Borg -> Omega -> Kubernetes"** 15년의 운영 노하우를 오픈소스로 공개했다.

- **📢 섹션 요약 비유**: 온프레미스가 "자기 집을 짓고 가구까지 사서 사는" 것이라면, 클라우드 아키텍처는 "전 세계 호텔 체인의 회원권으로 어디서든 필요한 방만 골라 쓰고, 짐은 호텔이 알아서 보관해주는" 시스템이다. 호텔이 붐비면 자동으로 더 빌려주고(탄력성), 호텔 화재 시 다른 호텔로 즉시 옮겨준다(장애 대응).

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **NIST SP 500-292 참조 모델**(5대 역할: Cloud Consumer, Provider, Auditor, Broker, Carrier)을 기반으로, **다층 계층(Multi-Tier) 아키텍처**, **Cell-Based Architecture**, **Sharded Architecture** 등 다양한 패턴이 존재한다. 현대 클라우드 네이티브 아키텍처의 핵심은 **"12-Factor App(Heroku 2011) + Beyond the 12-Factor(AppDynamics) + 15-Factor App(Kubernetes 최적화)"** 원칙을 준수하는 것이다.

```text
                 +------------------------------------------+
                 |   Global Edge / Multi-Region Active-Active |
                 |   (Route 53 Latency-Based / Cloudflare)  |
                 +----------------+-------------------------+
                                  |
              +-------------------+-------------------+
              v                   v                   v
        +----------+         +----------+       +----------+
        | Region A |         | Region B |       | Region C |
        | (Seoul)  |         | (Tokyo)  |       | (Virginia)|
        +----+-----+         +----+-----+       +----+-----+
             |                    |                   |
   +---------+---------+         ...                 ...
   v         v         v
+-----+  +-----+   +-----+
| AZ-a|  | AZ-b|   | AZ-c|  (Availability Zone: 독립 DC)
+--+--+  +--+--+   +--+--+
   |        |         |
   v        v         v
+----------------------------------+
|  L7 ALB / NLB / API Gateway     |
|  (WAF + Shield + Cognito 인증)   |
+----------------+-----------------+
                 |
   +-------------+--------------+
   v             v              v
+--------+  +--------+     +--------+
|ECS/EKS |  |Lambda  |     |Step    |
|Service |  |Function|     |Functions|
|(Fargate)| |(이벤트) |     |(워크플로)|
+---+----+  +---+----+     +----+---+
    |           |                |
    +-----------+----------------+
                v
      +---------------------+
      | Service Mesh (Istio)|
      | mTLS + Circuit Break|
      +----------+----------+
                 |
   +-------------+-------------+
   v             v              v
+--------+  +--------+     +--------+
|Aurora  |  |DynamoDB|    | Elasti-|
|Global   |  |Global  |     |Cache   |
|Database |  |Tables  |     |Redis   |
+--------+  +--------+     +--------+
                 |
                 v
      +---------------------+
      | Observability Stack |
      | (Prometheus+Grafana | + Loki + Tempo + Jaeger)
      +---------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge / CDN 계층** | 글로벌 정적 콘텐츠 캐싱, DDoS 방어, TLS Termination | CloudFront(50+ Edge Location), Cloudflare(Aquara Network), Fastly(Varnish VCL). **Anycast Routing**으로 사용자 근접 노드 자동 라우팅, 캐시 적중률(Cache Hit Ratio) 90% 이상 시 Origin 부하 90% 감소 |
| **Global Load Balancer** | DNS 기반 멀티 리전 트래픽 분배, Active-Active/Active-Passive 페일오버 | AWS Route 53 Latency-Based/Geolocation/Weighted, GCP Cloud DNS, Azure Traffic Manager. **TTL 관리**(60초~300초)와 **Health Check**로 자동 페일오버, **RTO 30초 이내** 달성 |
| **Application Load Balancer(ALB)** | L7 라우팅(Path/Host/Header 기반), WebSocket 지원, gRPC | AWS ALB(50% 더 낮은 비용 vs Classic), Envoy Proxy 기반. **Sticky Session**(쿠키), **Weighted Target Group**으로 카나리/블루그린 배포. Connection Draining으로 무중단 배포 |
| **컨테이너 오케스트레이션** | 선언적 배포, 자동 스케일링, 자가 치환(Self-healing) | Kubernetes 1.30+, EKS/GKE/AKS. **HPA**(CPU/Memory/RPS 기반), **VPA**(Pod 리소스 자동 조정), **KEDA**(이벤트 기반 0->N 스케일링), **Cluster Autoscaler**, **Karpenter**(서버리스 노드 프로비저닝, 30초 내 신규 노드) |
| **서비스 메시(Service Mesh)** | 마이크로서비스 간 mTLS, 트래픽 관리, 관측가능성 | Istio 1.22, Linkerd 2.15, Consul Connect. **Sidecar Envoy**로 L4/L7 정책 주입, **Circuit Breaker**(5xx 50% 시 자동 차단), **Retry/Timeout**, **Traffic Mirroring**(Shadow Traffic) |
| **데이터 계층** | RDBMS(트랜잭션), NoSQL(대규모), Object Storage(파일) | Aurora(MySQL/PostgreSQL 호환, 6-way Replication), DynamoDB(99.999% SLA, 10ms 미만 latency), S3(11 9s 내구성, 99.99% 가용성), RDS Multi-AZ(동기 복제, RPO 0) |
| **캐시 계층** | Read-Through, Write-Behind, Session 저장 | ElastiCache Redis 7.2(클러스터 모드, 500 노드, 68.2GB/노드), Memcached, Hazelcast. **Cache Stampede** 방지(Lazy Loading + Async Refresh) |
| **메시지 큐/이벤트 스트림** | 비동기 처리, 이벤트 드리븐, Pub/Sub | Apache Kafka(파티션 순서 보장, exactly-once), Amazon SQS(Standard/FIFO), SNS(Push), EventBridge(450+ SaaS 통합), RabbitMQ(AMQP 0-9-1) |
| **관측가능성(Observability)** | Metrics/Logs/Traces 통합, AIOps | **3 Pillars**: Prometheus(메트릭), Loki(로그), Tempo/Jaeger(분산 트레이싱). OpenTelemetry SDK 표준. **RED Method**(Rate, Error, Duration), **USE Method**(Utilization, Saturation, Errors) |
| **IaC / GitOps** | 인프라 선언적 정의, Git 기반 배포 자동화 | Terraform 1.7+(State Lock with DynamoDB), Pulumi(TS/Python/Go), AWS CDK, ArgoCD/Flux(GitOps). **Policy as Code**: OPA/Conftest, **SBOM**: CycloneDX/SPDX |

**핵심 알고리즘/수식:**

1. **가용성(Availability) 계산식**: `A = MTBF / (MTBF + MTTR)`
   - 99.9%(Three-9) = 연 8.76시간 장애
   - 99.95% = 연 4.38시간
   - 99.99%(Four-9) = 연 52.56분
   - 99.999%(Five-9) = 연 5.26분 (통신사 등급)

2. **CAP 정리 (Brewer's Theorem)**: 분산 시스템은 **Consistency(일관성), Availability(가용성), Partition Tolerance(파티션 내성)** 중 최대 2가지만 보장 가능. 클라우드는 P는 필수이므로 C와 A 사이에서 선택. -> **PACELC 확장**: 평상시에도 Latency vs Consistency 트레이드오프 존재

3. **Amdahl's Law(암달의 법칙)**: `Speedup = 1 / ((1-P) + P/N)` (P: 병렬화 가능 비율, N: 프로세서 수). 병렬화 가능한 부분이 90%여도 N->∞일 때 최대 10배 성능 향상 한계

4. **Little's Law**: `L = λ × W` (시스템 내 평균 요청 수 = 도착률 × 평균 체류시간). 동시 사용자 10,000명, 평균 응답 200ms라면 처리량 λ = 50,000 RPS 필요

5. **Queueing Theory (M/M/c)**: Erlang C 공식으로 콜센터/요청 큐의 대기 확률 계산. **PoC(Probability of Call Waiting)**, **ASA(Average Speed of Answer)** 도출

6. **Auto Scaling 알고리즘**: AWS Target Tracking(예: CPU 60% 목표), Step Scaling(임계값 기반 단계별), Scheduled Scaling(예측 가능 패턴), Predictive Scaling(ML 기반 2일 전 예측)

7. **분산 합의
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 729 / 800

<- **이전**: [728. 클라우드 아키텍처 핵심 토픽 728번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/728_cloud_architecture_core_topic_728_exam_summar/)
**다음**: [730. 클라우드 아키텍처 핵심 토픽 730번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/730_cloud_architecture_core_topic_730_exam_summar/) ->

---
