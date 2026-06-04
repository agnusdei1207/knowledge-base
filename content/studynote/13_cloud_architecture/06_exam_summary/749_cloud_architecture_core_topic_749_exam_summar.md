---
title: "749. 클라우드 아키텍처 핵심 토픽 749번 시험 요약 (Cloud Architecture Core Topic 749 Exam Summary)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 4계층 추상화 위에 **AWS Well-Architected 5대 기둥**(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화)과 **6R 마이그레이션 전략**(Rehost/Replatform/Repurchase/Refactor/Retire/Retain)을 적용하여, Multi-AZ·Multi-Region 기반의 탄력적·분산 시스템으로 CAP·PACELC 일관성 모델을 만족시키는 설계 체계이다.
> 2. **가치**: Well-Architected 적용 시 **가용성 99.99%(연 52.6분 장애)**, TCO 40~70% 절감, Auto Scaling을 통한 트래픽 100배 변동 흡수, MTTR 4시간->4분 단축, 배포 주기 월 1회->일 10회+ 달성, Carbon Footprint 80% 감소(리전별 재생에너지 사용).
> 3. **판단 포인트**: 핵심 트레이드오프는 ① Stateful vs Stateless(클러스터 vs Lambda), ② 동기 RPC vs 비동기 이벤트(Kafka/SQS/SNS Saga), ③ 강한 일관성 vs 결과적 일관성(CP vs AP), ④ 단일 클라우드 깊이 vs 멀티 클라우드 폭, ⑤ Lift&Shift vs Cloud-Native Refactoring ⑥ Centralized(API Gateway+Egress) vs Distributed Mesh 사이의 균형점 결정이다.

---

## Ⅰ. 개요 및 필요성

전통적 3-Tier On-Premise 아키텍처(웹-WAS-DB)는 정적 capacity planning, 수직 확장(Scale-Up) 한계, 수동 장애 대응, CapEx 중심의 5~7년 갱신 주기라는 구조적 한계를 가진다. 2020년 이후 COVID-19를 기점으로 한 Digital Transformation 가속, AI/ML 워크로드 폭증, 글로벌 사용자 트래픽의 예측 불가능성, 그리고 DORA Metrics(배포 빈도/리드타임/MTTR/변경 실패율) 기반의 DevOps 성숙도 요구로 인해, 클라우드 네이티브 아키텍처는 선택이 아닌 필수로 자리 잡았다.

핵심 기술적 과제는 다음과 같다: ① **분산 시스템의 8가지 오해**(Fallacies of Distributed Computing: 네트워크는 신뢰할 수 있다/지연은 0/대역폭은 무한/보안은 당연/NIC 구성은 불변/토폴로지는 고정/관리자는 1명/비용은 0) ② **CAP Theorem** 하의 일관성·가용성·분단 허용 트레이드오프 ③ **Shared Responsibility Model** 경계 변경(클라우드 사업자가 Infra 책임, 고객은 데이터/IAM/애플리케이션 책임) ④ **FinOps**를 통한 비용 거버넌스 ⑤ **Zero Trust**(BeyondCorp) 보안 모델 전환.

기존 On-Premise 방식 대비 클라우드는 **"Pay-per-Use" OpEx 모델, API 기반의 Programmable Infrastructure, 27개 리전·400+ 엣지 로케이션의 글로벌 팜플레인, 관리형 서비스(Managed Service) 200여 종**을 통해 비즈니스 차별화 기능을 1주일 이내에 조립식으로 도입 가능케 한다.

```text
   [Legacy 3-Tier On-Premise]                    [Cloud-Native Architecture]
   +-------------------------+                  +----------------------------------+
   |  Client (Browser/App)   |                  |  Edge (CloudFront/Akamai CDN)    |
   +------------+------------+                  +------------+---------------------+
                | HTTPS                                       | WAF + Shield (DDoS)
   +------------v------------+                  +------------v---------------------+
   |  L4/L7 LB (F5)         |                  |  Route 53 (Latency-Based DNS)     |
   |  고정 Capacity          |                  |  + API Gateway (Throttle/Cache)  |
   +------------+------------+                  +------------+---------------------+
                | Sticky Session                              | mTLS, JWT
   +------------v------------+                  +------------v---------------------+
   |  WAS (WebLogic/JBoss)  |                  |  EKS/ECS Fargate (HPA+VPA)       |
   |  Scale-Up (수직)        |                  |  Pod: 0->1000 (30초 내)            |
   |  라이선스 과금          |                  |  Service Mesh: Istio/Linkerd     |
   +------------+------------+                  +------------+---------------------+
                | JDBC Pool 50                                | gRPC/HTTP2
   +------------v------------+                  +------------v---------------------+
   |  Oracle RAC (Active/    |                  |  Aurora Global (R/W 분리)        |
   |   Active - 비쌈)        |                  |  + DynamoDB Global Tables        |
   |  수동 Failover          |                  |  + ElastiCache (Redis)           |
   +------------+------------+                  |  + S3 Multi-AZ + Intelligent-    |
                | SAN 이중화                              Tiering
   +------------v------------+                  +------------+---------------------+
   |  SAN Storage (EMC)     |                               |
   |  수동 백업              |                  +------------v---------------------+
   |  DR: Cold Site (수일)  |                  |  Cross-Region Replication        |
   +-------------------------+                  |  Multi-AZ (99.99%)              |
                                                |  DR: Pilot Light (수 분)         |
   RTO: 4~24시간 / RPO: 1~24시간                +----------------------------------+
   TCO: CapEx 100% / LeadTime: 6개월
                                                RTO: 1~5분 / RPO: 0~수 초
                                                TCO: OpEx 종량제 / LeadTime: 1일
```

- **📢 섹션 요약 비유**: On-Premise는 자가용(자가 소유, 주유/보험 자비, 사고 시 견인 1주)이고, 클라우드는 UBER(필요 시 호출, 분당 요금, 사고 시 즉시 대체 차량)이다. 핵심은 "차량 관리"가 아니라 "이동 서비스"에 집중하는 것.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심 원리는 **"모든 것은 실패한다(Design for Failure)"**라는 전제하에, ① 무상태(Stateless) 컴퓨팅, ② 비동기 메시징 기반 결합도 완화, ③ 다층 방어(Defense in Depth), ④ 불변 인프라(Immutable Infrastructure), ⑤ IaC(IaC: Terraform/CloudFormation) + GitOps(ArgoCD/Flux) 선언적 운영의 5대 원리 위에 성립한다.

전형적인 3-Tier -> Modern Cloud Architecture 매핑은 다음과 같다:

| 계층 | Legacy 3-Tier | Modern Cloud Architecture | 비고 |
| :--- | :--- | :--- | :--- |
| **Edge** | 하드웨어 L7 LB | CloudFront + WAF + Shield Advanced | 엣지 캐싱, L7 DDoS 방어 |
| **Gateway** | F5/APM | API Gateway(REST->gRPC 변환, Rate Limit) | OAuth2.1, mTLS, OpenAPI 검증 |
| **Application** | Java EE/WebLogic on Bare Metal | EKS(Managed K8s) + Spring Boot 3 / Quarkus | HPA: CPU/Mem/QueueLag/RPS |
| **Service Mesh** | EJB/SOAP | Istio(Envoy Sidecar) mTLS 자동화 | L7 Traffic Mgmt + Observability |
| **Data (OLTP)** | Oracle RAC | Aurora MySQL/PostgreSQL (Writer/Reader 분리) | 6-way 복제, 1초 내 Failover |
| **Data (NoSQL)** | MySQL Vertical | DynamoDB (Single-digit ms) / Cassandra | 무한 확장, 99.999% SLA |
| **Cache** | Redis Cluster (직접) | ElastiCache for Redis (Multi-AZ) | 자동 Failover, RPO 0 |
| **Object Storage** | NAS (NFS) | S3 (11 9's 99.999999999%) | Glacier로 라이프사이클 자동화 |
| **Message** | RabbitMQ (관리) | SQS Standard/FIFO + Kafka MSK (MSK Serverless) | 처리량 무제한 vs 순서 보장 |
| **CI/CD** | Jenkins on VM | GitHub Actions + ArgoCD(CD) + Tekton | GitOps, Progressive Delivery |
| **Observability** | Nagios + Splunk | CloudWatch + X-Ray + OpenTelemetry + Grafana | 3-pillar: Logs/Metrics/Traces |

아래는 Multi-Region Active-Active 클라우드 아키텍처의 표준 패턴이다:

```text
   +-------------------------------------------------------------------------+
   |                  Global Users (200+ Countries)                          |
   +----------------------------------+--------------------------------------+
                                      | GeoDNS (Latency/Geolocation)
                  +-------------------+-------------------+
                  v                                       v
   +--------------------------+         +--------------------------+
   |  us-east-1 Region        |         |  ap-northeast-2 Region   |
   |  +--------------------+  |         |  +--------------------+  |
   |  | CloudFront Edge    |  |         |  | CloudFront Edge    |  |
   |  | (Lambda@Edge)      |  |         |  | (Lambda@Edge)      |  |
   |  +---------+----------+  |         |  +---------+----------+  |
   |  +---------v----------+  |         |  +---------v----------+  |
   |  | API Gateway        |  |         |  | API Gateway        |  |
   |  | + WAF + Cognito   |  |         |  | + WAF + Cognito   |  |
   |  +---------+----------+  |         |  +---------+----------+  |
   |  +---------v----------+  |<---VPN--->|  +---------v----------+  |
   |  | EKS Cluster (AZ×3) |  |         |  | EKS Cluster (AZ×3) |  |
   |  | - Istio Service    |  |  Saga   |  | - Istio Service    |  |
   |  |   Mesh (mTLS)      |  |  Coord  |  |   Mesh (mTLS)      |  |
   |  +---------+----------+  |         |  +---------+----------+  |
   |  +---------v----------+  |         |  +---------v----------+  |
   |  | Aurora Writer      |  |<---Binlog->|  | Aurora Reader      |  |
   |  | + ElastiCache      |  |         |  | + ElastiCache      |  |
   |  +---------+----------+  |         |  +---------+----------+  |
   |  +---------v----------+  |         |  +---------v----------+  |
   |  | DynamoDB Global    |  |<---Last--->|  | DynamoDB Global    |  |
   |  | Table (Multi-Region)|  |  Writer |  | Table               |  |
   |  +---------+----------+  |  Wins   |  +---------+----------+  |
   |  +---------v----------+  |         |  +---------+----------+  |
   |  | S3 (CRR: S3 IA->GL)|  |<---------->|  | S3 (CRR)           |  |
   |  +--------------------+  |         |  +--------------------+  |
   +--------------------------+         +--------------------------+
                  |                                       |
                  +-------------------+-------------------+
                                      v
              +------------------------------------------+
              |  CloudWatch + X-Ray + CloudTrail         |
              |  + Security Hub + GuardDuty              |
              |  + AWS Config (Compliance as Code)       |
              +------------------------------------------+
                                      |
                                      v
              +------------------------------------------+
              |  Central
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 749 / 800

<- **이전**: [748. 클라우드 아키텍처 핵심 토픽 748번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/748_cloud_architecture_core_topic_748_exam_summar/)
**다음**: [750. 클라우드 아키텍처 핵심 토픽 750번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/750_cloud_architecture_core_topic_750_exam_summar/) ->

---
