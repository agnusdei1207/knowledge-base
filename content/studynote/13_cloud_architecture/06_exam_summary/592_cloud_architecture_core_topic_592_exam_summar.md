---
title: "592. 클라우드 아키텍처 핵심 토픽 592번 시험 요약 (Cloud Architecture Core Topic 592 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 퍼블릭/프라이빗/하이브리드 클라우드 환경에서 워크로드 분산, 오토스케일링, 무중단 배포, 다중 가용 영역(MAZ) 기반 장애격리, IaC(Infrastructure as Code) 및 GitOps를 통한 선언적 인프라 운영이 클라우드 아키텍처의 4대 기둥이다.
> 2. **가치**: CAPEX->OPEX 전환으로 초기 인프라 투자비 60~80% 절감, Auto Scaling Group과 Spot Instance 결합 시 컴퓨팅 비용 40~70% 추가 절감, Multi-AZ + Multi-Region 구성으로 RTO 5분·RPO 0~수 초 달성, 글로벌 트래픽 라우팅으로 사용자 체감 지연 시간 평균 200~400ms 단축.
> 3. **판단 포인트**: 5개 아키텍처 결정 포인트(가용성 99.95% vs 99.99% SLA, 동기식 Strong Consistency vs eventual consistency, 단일 리전 vs 액티브-액티브 멀티리전, Stateless vs Stateful 워크로드, EKS/AKS/GKE vs 자체 Kubernetes) 간의 트레이드오프를 워크로드 특성(트래픽 패턴, 데이터 일관성 요구 수준, 규제 컴플라이언스)에 따라 정량적으로 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 더 이상 단순한 "서버를 빌려 쓰는 것"이 아니라, **탄력성(Elasticity)**, **회복탄력성(Resilience)**, **관측 가능성(Observability)**, **자동화(Automation)**를 코어 역량으로 삼는 분산 시스템 설계 철학이다. 2024년 기준 국내 대기업 약 78%, 공공기관 약 65%가 이미 멀티클라우드 또는 하이브리드 전략을 채택(KISA 클라우드 컴퓨팅 이용 통계)하고 있으며, 클라우드 네이티브(CNCF 정의: 컨테이너·서비스 메시·마이크로서비스·불변 인프라·API 기반 자동화를 활용하는 접근 방식) 기반 아키텍처 전환이 디지털 전환의 핵심 동력으로 자리 잡았다.

기술사 시험에서 592번 토픽은 다음 5가지 배경에서 절대적으로 필요하다:
- **기술 격차**: 레거시 3-Tier(웹-WAS-DB) 모놀리식 아키텍처는 트래픽 10배 증가 시 수평확장 시 4~8주 소요되지만, 클라우드 네이티브 HPA(Horizontal Pod Autoscaler) + Karpenter 기반 구조는 평균 90초 내 신규 노드 자동 할당.
- **비용 압박**: 24/7 On-Premise 대비 Cloud + Reserved Instance + Spot 혼용 모델은 동일 성능에서 TCO 35~55% 절감이 일반적.
- **규제/컴플라이언스**: 클라우드 보안인증 제도(CSAP), ISMS-P, PCI-DSS, GDPR 등 데이터 주권·상주 리전·암호화 키 관리(KMS BYOK/HYOK) 요건이 아키텍처 패턴을 강제함.
- **AI/ML 워크로드 폭증**: GPU 자원의 스파스 워크로드 특성은 Spot Instance + Auto Scaling 조합 없이는 비용 최적화가 불가능.
- **장애 대응**: 단일 AZ 장애 발생 시 자동 페일오버 보장 아키텍처(예: Aurora Multi-AZ, EFS One Zone->Standard 전환, DynamoDB Global Tables)가 비즈니스 연속성 필수 요건으로 부상.

```text
+---------------- 클라우드 아키텍처 진화 패러다임 비교 ----------------+
|                                                                       |
|  전통적 아키텍처 (2010 이전)         클라우드 네이티브 (2020 이후)   |
|  +-----------------+               +----------------------------+   |
|  |  Monolith App   |               |  Microservices (수십~수백) |   |
|  |  +------------+ |               |  +--++--++--++--++--+    |   |
|  |  |  Web       | |               |  |M1||M2||M3||M4||M5|    |   |
|  |  +------------+ |               |  +--++--++--++--++--+    |   |
|  |  |  App/WAS   | |   ------►     |  Service Mesh (Istio)     |   |
|  |  +------------+ |    Cloud     |  Container (K8s)           |   |
|  |  |  DB        | |    Native    |  Multi-AZ / Multi-Region   |   |
|  |  +------------+ |               |  IaC + GitOps              |   |
|  |  물리서버 (1~10) |               |  분산 노드 (수백~수만)     |   |
|  +-----------------+               +----------------------------+   |
|                                                                       |
|  - 수직확장(Scale-Up)                  - 수평확장(Scale-Out)            |
|  - 수동 장애대응                       - 셀프힐링(Self-Healing)        |
|  - 야간 수동 배포                      - 무중단 Canary/Blue-Green      |
|  - CAPEX 위주                         - OPEX + FinOps                 |
|  - MTTR 평균 4~24시간                 - MTTR 평균 5~30분              |
+-----------------------------------------------------------------------+
```

**레거시 대비 클라우드 네이티브의 본질적 차이**는 "고정 자원 계획"에서 "동적 용량 조정"으로의 전환이다. 기존 아키텍처는 1년 단위 용량 계획(예: 블랙프라이데이 대비 5배 트래픽 -> 평소 5배 인프라 상시 운영)으로 자원 낭비율이 70~80%에 달했으나, 클라우드 네이티브는 수요 기반 자동 스케일링으로 평균 이용률 40~60% 유지가 가능하다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "호텔의 객실 관리 시스템"과 같다. 레거시 방식은 손님이 늘면 호텔을 통째로 증축해야 하지만(Monolith Scale-Up), 클라우드 네이티브는 룸서비스 호출 버튼 하나(HPA Trigger)로 빈 객실만 즉시 배정해주는(Container Spin-up) 똑똑한 호텔이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **7계층 참조 모델**(Well-Architected Framework 기반)로 분해된다: ① 글로벌/엣지 계층 -> ② 로드밸런싱·API Gateway 계층 -> ③ 컨테이너 오케스트레이션 계층 -> ④ 서비스 메시/마이크로서비스 계층 -> ⑤ 데이터/상태 계층 -> ⑥ 관측·보안 계층 -> ⑦ IaC/GitOps 자동화 계층.

```text
                          +------------------- Global Edge -------------------+
                          |  CloudFront / Azure CDN / Cloud CDN              |
                          |  + WAF (OWASP Top 10 차단) + DDoS Shield         |
                          |  + Lambda@Edge / Cloud Functions (Edge Compute)  |
                          +------------------------+------------------------+
                                                   | TLS 1.3, HTTP/3
                          +------------------------v------------------------+
                          |        L7 Load Balancer / API Gateway           |
                          |  ALB / Application Gateway / Cloud Load Balancer |
                          |  +-----------------+  +------------------+      |
                          |  | Path-based 라우팅|  | JWT Auth + Rate  |      |
                          |  | /api/* -> Svc A  |  | Limiting (100rps)|      |
                          |  | /pay/* -> Svc B  |  +------------------+      |
                          |  +-----------------+                             |
                          +------------------------+------------------------+
                                                   |
              +------------------------------------+------------------------------------+
              |                                    |                                    |
   +----------v----------+            +------------v------------+         +------------v------------+
   | EKS / AKS / GKE    |            |  EKS / AKS / GKE        |         |  EKS / AKS / GKE        |
   |  Cluster (Region A)|            |  Cluster (Region B)     |         |  Cluster (Region C)     |
   |                    |            |                         |         |                         |
   | +----------------+ |            |  +-----------------+    |         |  +-----------------+    |
   | | Istio Service  | |            |  | Istio Service   |    |         |  | Istio Service   |    |
   | | Mesh (mTLS)    | |            |  | Mesh (mTLS)     |    |         |  | Mesh (mTLS)     |    |
   | | +--++--++--+  | |            |  | +--++--++--+   |    |         |  | +--++--++--+   |    |
   | | |P1||P2||P3|  | |            |  | |P1||P2||P3|   |    |         |  | |P1||P2||P3|   |    |
   | | +--++--++--+  | |            |  | +--++--++--+   |    |         |  | +--++--++--+   |    |
   | | HPA/VPA/Karpenter|            |  | HPA/VPA/Karpenter|    |         |  | HPA/VPA/Karpenter|    |
   | +----------------+ |            |  +-----------------+    |         |  +-----------------+    |
   |  AZ-a, AZ-b, AZ-c  |            |   AZ-d, AZ-e, AZ-f     |         |   AZ-g, AZ-h, AZ-i     |
   +----------+----------+            +------------+------------+         +------------+------------+
              |                                    |                                    |
              +------------------------------------+------------------------------------+
                                                   |
                          +------------------------v------------------------+
                          |      Observability + Security Layer            |
                          |  +----------+  +----------+  +----------+       |
                          |  |Prometheus|  | Loki     |  | Tempo    |       |
                          |  | (Metric) |  | (Log)    |  | (Trace)  |       |
                          |  +----------+  +----------+  +----------+       |
                          |  + Falco (Runtime Security) + OPA (Policy)    |
                          |  + Vault (Secret) + cert-manager (mTLS)       |
                          +------------------------+------------------------+
                                                   |
                          +------------------------v------------------------+
                          |          Data / Stateful Layer                  |
                          |  +--------------+  +--------------+              |
                          |  | Multi-AZ RDS |  | DynamoDB /   |              |
                          |  | (Strong Con.)|  | CosmosDB     |              |
                          |  |  + Read Repl.|  | (Eventual)   |              |
                          |  +--------------+  +--------------+              |
                          |  + S3 / Blob (Object) + ElastiCache (Cache)     |
                          |  + Kafka / Kinesis / Pub/Sub (Event Stream)   |
                          +-------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Global Edge / CDN** | 정적·동적 콘텐츠 캐싱, DDoS 방어, TLS 종료, 지리적 라우팅 | CloudFront/Azure CDN/Cloud CDN — 엣지 로케이션 200~600+ 곳, Anycast IP 기반 BGP 라우팅, Lambda@Edge로 응답 커스터마이징(예: A/B 테스트 헤더 주입) |
| **L7 Load Balancer + API Gateway** | 트래픽 분산, SSL 오프로딩, Path/Header 기반 라우팅, 인증/인가 | ALB(Application Load Balancer) — 라운드로빈·최소 연결·해시 알고리즘 지원, OIDC/OAuth2.0 통합, WebSocket·HTTP/2·gRPC 처리, WAF 룰(560+ Managed Rule Group) 연동 |
| **Container Orchestrator** | 컨테이너 라이프사이클 관리, 스케줄링, 셀프힐링, 롤링 업데이트 | Kubernetes 1.30+ / EKS / AKS / GKE — 선언적 YAML(Helm/Kustomize), Deployment ReplicaSet 기반 점진적 배포, PDB(Pod Disruption Budget)로 가용성 보장, Karpenter로 노드 프로비저닝 30~60초 단축 |
| **Service Mesh** | 마이크로서비스 간 mTLS, 트래픽 관리(Canary/Mirror), 관측, 정책 | Istio / Linkerd / Consul — 사이드카 프록시(Envoy) 기반, control plane이 xDS API로 설정 분배, AuthorizationPolicy로 L7 RBAC, OpenTelemetry trace 자동 수집 |
| **Auto Scaling** | 부하 변동에 따른 Pod/Node 자동 증감 | HPA(Metric 기반, 기본 30초 주기) + VPA(Resource 권고) + Karpenter(Bin-packing 최적화) + KEDA(이벤트 기반, Kafka/SQS 트리거) — Scale-down 안정화 윈도우 5분, Scale-up은 즉시 |
| **Storage / Database** | 영속 데이터 저장, 캐싱, 백업, 복제 | OLTP: Aurora Multi-Master(쓰기 6개 노드, 동기 복제), DynamoDB Global Tables(멀티리전 active-active) / OLAP: Redshift/Snowflake/BigQuery / Cache: ElastiCache(Redis Cluster, Cluster Mode), Memcached / Object: S3(11 9s 내구성), Glacier(장기 아카이빙) |
| **Observability Stack** | 메트릭·로그·트레이스 통합 수집 및 알림 | Prometheus + Grafana(Metric), Loki + Grafana(Log), Tempo/Jaeger(Trace), OpenTelemetry SDK 표준화, Alertmanager + PagerDuty/Opsgenie 연동, SLO 기반 에러 버닝(에러 예산) 알림 |
| **IaC + GitOps** | 인프라 선언적 코딩, Git을 Single Source of Truth로 사용 | Terraform(멀티클라우드, HCL 언어, State Lock) / Pulumi(코드로 IaC) + ArgoCD/FluxCD(Git 변경 감지 -> 자동 Sync), Atlantis(Terraform PR 자동화), OPA(Kubernetes Admission Control) |

**핵심 동작 메커니즘 — HPA + Karpenter 결합 스케일링**:
- HPA가 매 15초마다 Metric Server에서 CPU/메모리/커스텀 메트릭(Kafka Lag, SQS ApproximateNumberOfMessages) 조회
- 임계치 초과 시 `targetReplicas = ceil(currentReplicas × currentMetricValue / targetMetricValue)` 공식으로 신규 Pod 수 산출
- 신규 Pod 스케줄링 시 Karpenter가 기존 노드 Bin-packing 실패를 감지하면 `NodeClass` CRD 기반으로 노드 프로비저닝 (예: `c7g.4xlarge` ARM64 인스턴스, 90초 내 Ready)
- Scale-down 시 stabilizationWindow(기본 5분) 적용으로 flapping 방지, PodDisruptionBudget으로 minAvailable 보장
- Cold Start 단축을 위해 **Pre-warmed Warm Pool**(AWS) 또는 **Spot Fleets with Diversification**(Azure VMSS) 활용 가능

**보안 및 컴플라이언스 핵심 메커니즘**:
- Zero Trust: 모든 트래픽을 기본 차단, mTLS(상호 TLS) 필수, BeyondCorp/Zero Trust Access 모델
- 키 관리: AWS KMS / Azure Key Vault / GCP KMS + BYOK(Bring Your Own Key) + HYOK(Hold Your Own Key) + External Key Store
- 데이터 암호화: At-rest (AES-256), In-transit (TLS 1.3), In-use (Confidential Computing: AWS Nitro Enclaves, Azure Confidential VMs)
- 네트워크: VPC/Subnet 분리, Security Group(Stateful) vs NACL(Stateless) 이중 방화벽,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 592 / 800

<- **이전**: [591. 클라우드 아키텍처 핵심 토픽 591번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/591_cloud_architecture_core_topic_591_exam_summar/)
**다음**: [593. 클라우드 아키텍처 핵심 토픽 593번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/593_cloud_architecture_core_topic_593_exam_summar/) ->

---
