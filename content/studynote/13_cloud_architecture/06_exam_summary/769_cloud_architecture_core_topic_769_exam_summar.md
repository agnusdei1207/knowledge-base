---
title: "769. 클라우드 아키텍처 핵심 토픽 769번 시험 요약 (Cloud Architecture Core Topic 769 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 **NIST SP 500-292 참조 모델**(Consumer/Provider/Broker/Auditor/Carrier 역할)과 **Well-Architected 5대 원칙**(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속가능성)을 기반으로, **탄력성(Elasticity)**, **무중단 자동화(Immutable Infrastructure)**, **불변 배포(Declarative API + GitOps)**를 통해 워크로드의 추상화된 리소스 풀링과 온디맨드 자가 서비스를 가능하게 하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: **TCO 30~60% 절감**(IDC 보고서 기준), 배포 주기 **수개월 -> 수시간 단축**, **Auto Scaling을 통한 피크 트래픽 100배 대응**, **Multi-AZ/Region 가용성 99.99%(Four-Nines, 연간 52.56분 이하 장애)** 달성을 통해 CapEx를 OpEx로 전환하고 비즈니스 민첩성을 극대화한다.
> 3. **판단 포인트**: **CAP 정리**(Consistency/Availability/Partition tolerance) 트레이드오프, **동기·비동기 통신 방식**, **Stateful vs Stateless 워크로드 구분**, **Shared Responsibility Model 경계 설정**, **Multi-Cloud 종속성 회피**(Egress 비용, Vendor Lock-in), **FinOps 기반 비용 거버넌스** 여부가 아키텍처 성패를 결정한다.

---

## Ⅰ. 개요 및 필요성

기존 온프레미스 데이터센터는 **CapEx(자본 지출)** 중심의 용량 계획(Over-Provisioning) 방식으로, 트래픽 피크 예측 실패 시 **Brownout/서비스 장애**가 발생하며, 유휴 자원 발생 시 **20~40% 낭비율**을 보였다. 또한 물리적 하드웨어 도입에 **6~12개월 Lead Time**이 소요되어 비즈니스 변화 속도를 따라가지 못하는 **"Velocity Gap"** 문제가 대두되었다.

클라우드 아키텍처는 **Control Plane**(API/Orchestration)과 **Data Plane**(실제 워크로드 실행)을 분리하고, **Software-Defined Everything**(네트워크·스토리지·컴퓨팅)을 통해 **선언적 API**(Declarative API)로 인프라를 코드로 정의(**Infrastructure as Code, IaC**)하며, **Pay-as-you-go** 과금 모델로 **사용한 만큼만 지불**(Per-Second/Per-Request Billing)하는 경제성을 제공한다. 2024년 현재 **전 세계 기업의 94%**가 클라우드를 사용하며(CFlexRight 2024 State of the Cloud), 이는 단순한 호스팅이 아닌 **"비즈니스 차별화를 위한 디지털 트랜스포메이션의 코어 플랫폼"**으로 자리잡았다.

```text
[전통적 아키텍처 -> 클라우드 네이티브 아키텍처 전환 패러다임]

  +--------------------------+                  +--------------------------+
  |  Traditional On-Premise  |                  |   Cloud-Native Arch.     |
  +--------------------------+                  +--------------------------+
  | +----------------------+ |                  | +----------------------+ |
  | |  Monolithic App      | |   -------►       | |  Microservices Mesh  | |
  | |  (EJB, WAR 1개)      | |   Transform      | |  (50+ 독립 서비스)    | |
  | +----------------------+ |                  | +----------------------+ |
  | +----------------------+ |                  | +----------------------+ |
  | | 물리 서버 + 수동 배포 | |                  | |K8s + GitOps 자동배포 | |
  | | (Capacity 10년 계획) | |                  | | (HPA/VPA 실시간)     | |
  | +----------------------+ |                  | +----------------------+ |
  | +----------------------+ |                  | +----------------------+ |
  | | 라이선스 SW + DB     | |                  | | SaaS + Managed DB   | |
  | | (Oracle RAC)         | |                  | | (Aurora/Cosmos)     | |
  | +----------------------+ |                  | +----------------------+ |
  |                          |                  |                          |
  | CapEx 80% / OpEx 20%     |                  | CapEx 20% / OpEx 80%     |
  | 장애복구 RTO 24h+        |                  | RTO 분 단위, RPO 0       |
  | 수직확장(Scale-Up)       |                  | 수평확장(Scale-Out)      |
  +--------------------------+                  +--------------------------+
                  |                                       |
                  +----------- "Lift & Shift" ------------+
                          (단순 이전) vs "Refactor/Re-architect"
                          (클라우드 네이티브 재설계)
```

**📢 섹션 요약 비유**: 기존 데이터센터는 **"주차장 면적을 10년 후 피크 때 기준으로 짓는 백화점"** 같고, 클라우드는 **"손님이 몰리면 즉시 인근 주차장도 연계 사용하는 스마트 모빌리티"**와 같다. 수요 예측이 틀려도 유연하게 자원을 끌어다 쓴다.

---

## Ⅱ. 아키텍처 및 핵심 원리

NIST SP 500-292 표준 참조 모델을 기반으로 클라우드 아키텍처는 **5대 핵심 역할(Consumer, Provider, Broker, Auditor, Carrier)**과 **3계층(서비스 소비·제공·중재)** 구조로 설계된다. 핵심 동작 원리는 **추상화·자동화·탄력성·가시성**의 4대 속성을 코드와 정책으로 실현하는 것이다.

```text
[NIST SP 500-292 클라우드 컴퓨팅 참조 아키텍처 - 5대 역할 상호작용]

   +---------------------------------------------------------------------+
   |                      Cloud Consumer (서비스 소비자)                  |
   |  +-------------+  +-------------+  +-------------+  +------------+ |
   |  |   SaaS User |  |   PaaS Dev  |  |  IaaS Admin |  |  FaaS Dev  | |
   |  +------+------+  +------+------+  +------+------+  +-----+------+ |
   +---------+----------------+----------------+---------------+--------+
             |                |                |               |
             v                v                v               v
   +---------------------------------------------------------------------+
   |                  Cloud Broker (중재자/통합자)                       |
   |  • Service Intermediation (보안 강화, 성능 향상)                     |
   |  • Service Aggregation (여러 서비스 통합: AWS+Datadog+Twilio)        |
   |  • Service Arbitrage (성능/가격 비교 후 최적 선택)                   |
   +---------------------------------------------------------------------+
             |                |                |               |
             v                v                v               v
   +---------------------------------------------------------------------+
   |                Cloud Provider (클라우드 제공자)                      |
   |  +-------------------------------------------------------------+    |
   |  |  Physical Layer: 서버/스토리지/네트워크/Datacenter/Region    |    |
   |  +-------------------------------------------------------------+    |
   |  |  Abstraction Layer: 가상화(KVM/Hyper-V), 컨테이너(ctr),   |    |
   |  |                     SDS(vSAN/Ceph), SDN(OVS/VXLAN)         |    |
   |  +-------------------------------------------------------------+    |
   |  |  Service Layer:   EC2/S3/RDS/Lambda/SQS/EKS (200+ 서비스)  |    |
   |  +-------------------------------------------------------------+    |
   +---------------------------------------------------------------------+
             ^                ^                ^               ^
             |                |                |               |
   +---------+----------------+----------------+---------------+--------+
   |  Cloud Carrier (통신사업자) - AWS DX, Azure ER, GCP Interconnect  |
   |  • 네트워크 전송 보장 (QoS, Bandwidth Commit)                      |
   |  • Cross-Region/VPC Peering, Transit Gateway                       |
   +---------------------------------------------------------------------+
             ^                                          ^
             |                                          |
   +---------+----------------+            +------------+-----------------+
   |   Cloud Auditor          |            |    Security/Compliance        |
   | (감사/인증: ISO 27001,    |            | (K-ISMS, PCI-DSS,             |
   |  SOC 2 Type II, CSAP)    |            |  Privacy Act, GDPR)           |
   +--------------------------+            +------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Control Plane (제어 평면)** | API Gateway, Orchestrator, IaC 엔진 | Terraform/CloudFormation/CDK으로 선언적 정의, **Reconciliation Loop**(현재 상태 ↔ 목표 상태)로 자동 보정, **GitOps**(ArgoCD/Flux) 기반 Pull 방식 배포 |
| **Data Plane (데이터 평면)** | 실제 워크로드 실행, 데이터 처리 | **Multi-AZ/Region 복제**, eBPF/XDP 기반 고성능 패킷 처리, **Sidecar Pattern**(Envoy Proxy)을 통한 L4/L7 트래픽 제어 |
| **Service Mesh (서비스 메시)** | 마이크로서비스 간 통신·관찰·보안 | **Istio/Linkerd/Cilium Service Mesh**가 mTLS(상호 TLS), Circuit Breaker, Retry/Timeout, 분산 트레이싱(OpenTelemetry)을 **앱 코드 변경 없이** 제공 |
| **Storage Tier (스토리지 계층)** | 데이터 영속성·일관성·내구성 관리 | **Hot(S3 Standard, 99.999999999% 11 9's) / Warm(S3 IA) / Cold(S3 Glacier, $0.00099/GB) / Archive(Glacier Deep Archive)** 티어링, **EBS gp3(3,000 IOPS, 125MB/s)** vs **io2 Block Express(256,000 IOPS, 4GB/s)** |
| **Identity & Access (인증/인가)** | 최소 권한 원칙(Zero Trust) | **IAM Role + OIDC Federation**(K8s Service Account ↔ AWS Role), **ABAC**(Attribute-Based), **PIM**(Privileged Identity Management) Just-In-Time 권한 상승, **SCP(Service Control Policy)**로 계정 단위 가드레일 |
| **Observability Stack** | 3대 신호(Metrics/Logs/Traces) 통합 | **Prometheus + Grafana + Loki + Tempo + OpenTelemetry Collector**, **RED 메트릭**(Rate/Error/Duration), **USE 메트릭**(Utilization/Saturation/Error), **SLI/SLO/Error Budget** 기반 SRE 운영 |

### 12-Factor App 핵심 원리 (클라우드 네이티브 필수 조건)

1. **Codebase**: 단일 코드베이스, 다중 배포 (Git Monorepo/Polyrepo)
2. **Dependencies**: 명시적 의존성 선언 (`requirements.txt`, `package.json`, **SBOM** 활용 CycloneDX/SPDX)
3. **Config**: 환경 변수로 외부화 (**Vault/AWS Secrets Manager** 연동, **12가지 항목** 모두 코드에 하드코딩 금지)
4. **Backing Services**: DB/큐/캐시를 **"Attached Resources"**로 취급, 연결 정보는 Config로 주입
5. **Build, Release, Run**: 3단계 엄격 분리, **Immutable Artifact**(Docker Image, SHA Pinning)
6. **Processes**: Stateless 프로세스, 세션 상태는 **Redis/ElastiCache/DynamoDB** 외부화 (Sticky Session 회피)
7. **Port Binding**: 자체 포트 바인딩, 외부 WAS 의존 제거 (Tomcat 임베디드)
8. **Concurrency**: 프로세스 모델로 수평 확장 (**HPA**: CPU 70% or RPS/Custom Metric 기반)
9. **Disposability**: 빠른 시작(< 5s), **Graceful Shutdown**(SIGTERM 처리, **PreStop Hook**으로 In-flight 요청 완료 대기)
10. **Dev/Prod Parity**: 개발/운영 환경 동일성 (**Docker**, **Vagrant**, **K8s Manifest** 통합)
11. **Logs**: 표준 출력(STDOUT/STDERR)으로 스트리밍, **Fluentd/Fluent Bit** -> OpenSearch/Loki 집적
12. **Admin Processes**: 일회성 작업을 별도 프로세스로 실행 (**Kubernetes Job/CronJob**)

### 핵심 알고리즘 및 이론

- **CAP 정리**: 분산 시스템은 **Consistency / Availability / Partition Tolerance** 중 2가지만 보장 가능. **CP 시스템**(etcd, HBase, MongoDB Replica Set with Write Concern majority) vs **AP 시스템**(Cassandra, DynamoDB, Riak). 클라우드에서는 **P는 필연**(네트워크 장애 불가피)이므로 C와 A를 비즈니스 요구사항에 맞게 선택.
- **Consensus 알고리즘**: **Raft**(etcd, Consul, CockroachDB 채택) - Leader Election + Log Replication, **Paxos**의 이해 용이한 대안. **Quorum(과반수)** = 2f+1 노드 중 f개 장애 허용.
- **부하 분산 알고리즘**: **L4 Round Robin / Least Connections / Consistent Hashing**(Memcached, AWS NLB), **L7 Content-Based Routing**(ALB, Envoy), **Maglev Hashing**(Google LB - O(1) Lookup, 5-Tuple Hash).
- **자동 확장 정책**: **Predictive Scaling**(ML 기반 예측, 12시간 전 학습), **Target Tracking**(CPU 60% 유지), **Step Scaling**(Δ 값 임계치), **Scheduled Scaling**(정시 이벤트), **KEDA**(Event-Driven Autoscaling, Kafka Lag -> K8s Pod Scale).

**📢 섹션 요약 비유**: 12-Factor App은 **"이사 가기 전 짐을 똑같이 표준 박스에 똑똑히 분류해두는 12가지 규칙"**과 같다. 새 집(클라우드 환경)이 어디든 박스 내용물만 알면 그대로 풀 수 있다. Control Plane은 이사 감독관, Data Plane은 실제 짐을 나르는 일꾼이다.

---

## Ⅲ. 비교 및 연결

| 구분 | **IaaS** (EC2, Azure VM, GCE) | **PaaS** (Elastic Beanstalk, App Engine, Heroku) | **SaaS** (Office 365, Salesforce, Slack) | **FaaS/Serverless** (Lambda, Cloud Functions) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | 앱 + 데이터 + 런타임 + 미들웨어 +
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 769 / 800

<- **이전**: [768. 클라우드 아키텍처 핵심 토픽 768번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/768_cloud_architecture_core_topic_768_exam_summar/)
**다음**: [770. 클라우드 아키텍처 핵심 토픽 770번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/770_cloud_architecture_core_topic_770_exam_summar/) ->

---
