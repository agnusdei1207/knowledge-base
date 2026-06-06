---
title: "Cloud Architecture Core Topic 703 Exam Summary"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST의 SPI(SaaS/PaaS/IaaS) 모델을 기반으로, 컨테이너 오케스트레이션(Kubernetes), 서버리스 컴퓨팅(Lambda/Cloud Functions), 서비스 메시(Istio) 및 IaC(Terraform/CloudFormation)를 통해 워크로드의 탄력성·가용성·확장성을 코드와 정책으로 선언적으로 제어하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: Auto-Scaling으로 평균 30~70% 인프라 비용 절감, Multi-AZ 배포로 99.99% SLA 확보, 무중단 배포(Blue-Green/Canary)로 배포 다운타임 0초 달성, MTTR 60% 단축, 글로벌 엣지 배포로 사용자 레이턴시 200ms->20ms 수준으로 개선.
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs Multi-Cloud 전략의 TCO 트레이드오프, Stateless Microservices의 일관성·트랜잭션 경계 문제, CAP Theorem 하의 CP/AP 시스템 선택, FinOps 기반 Reserved/On-Demand/Spot 인스턴스 혼용 비율, Zero-Trust 네트워킹과 Egress 비용 최적화 사이의 균형.

---

## Ⅰ. 개요 및 필요성

전통적 온프레미스 아키텍처는 CAPEX(자본 지출) 중심의 수직적 확장(Scale-Up) 방식으로, 비즈니스 트래픽 변동에 유연하게 대응하기 어렵고, IDC 운영·전력·냉각·네트워크 등 비기능 요구사항을 자체 운영팀이 직접 관리해야 했다. 2006년 AWS S3·EC2 출시 이후 등장한 클라우드 컴퓨팅은 NIST SP 800-145 표준에 따라 **"네트워크, 서버, 스토리지, 애플리케이션, 서비스 등 구성 가능한 컴퓨팅 자원의 공유 풀에 대해 어디서나 편리하게 주문형으로 네트워크 접근을 가능하게 하는 모델"**로 정의된다. 기술사 시험에서 703번 토픽은 클라우드 마이그레이션 전략(Rehost/Replatform/Refactor), 12-Factor App 원칙, Well-Architected Framework, 하이브리드/멀티클라우드 거버넌스, 클라우드 네이티브 보안 모델(CNAPP/CSPM/CWPP)을 통합적으로 다루는 영역이다.

```text
+------------------------------------------------------------------+
|              On-Premise vs Cloud Paradigm Shift                  |
+------------------------------------------------------------------+
|                                                                  |
|  [On-Premise Era - 2000s]                                        |
|   +-------------+   +-------------+   +-------------+            |
|   | Physical DC |   |  Over-Provision  |   | Manual Ops |            |
|   | CAPEX Heavy |--->|  18-24개월 도입 |--->| MTTR : Days |            |
|   +-------------+   +-------------+   +-------------+            |
|        |                                                        |
|        v (2006~ AWS S3/EC2, 2010~ OpenStack, 2013~ Docker)       |
|                                                                  |
|  [Cloud Native Era - 2020s]                                      |
|   +-------------+   +-------------+   +-------------+            |
|   |  Multi-AZ   |   | Auto-Scaling|   | GitOps/Argo |            |
|   | OPEX Based  |--->| 분 단위 확장 |--->| MTTR : 분   |            |
|   +-------------+   +-------------+   +-------------+            |
|         |                |                |                      |
|         v                v                v                      |
|   +--------------------------------------------------+           |
|   |   IaC(Terraform)  |  Observability(Prometheus)  |           |
|   |   Policy-as-Code  |  FinOps(비용 최적화)         |           |
|   +--------------------------------------------------+           |
+------------------------------------------------------------------+
```

클라우드 전환의 핵심 동인은 **(1) Time-to-Market 단축**(신규 인프라 프로비저닝 4주->5분), **(2) 탄력적 비용 구조**(사용량 기반 종량제), **(3) 글로벌 가용성**(리전 간 자동 페일오버), **(4) 이머징 기술 접근성**(AI/ML·빅데이터·양자컴퓨팅 API)이다. 기술사 답안에서는 단순한 비용 비교가 아니라, 워크로드 특성(상태유무·트래픽 패턴·데이터 중력)에 따른 적합한 클라우드 아키텍처 패턴 선택 근거를 명확히 서술해야 한다.

- **📢 섹션 요약 비유**: 기존 온프레미스는 **자기 소유 호텔**(건물·인테리어·인력 직접 운영)이라면, 클라우드는 **체크인 즉시 이용 가능한 글로벌 호텔 체인**(Hilton/Marriott)과 같다. 예약만 하면 객실·조식·수영장·컨시어지 서비스가 즉시 제공되며, 필요 없어지면 체크아웃하면 그만이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처의 핵심은 **5가지 계층별 책임 분담 모델(Shared Responsibility Model)**과 **7가지 Well-Architected 원칙**(운영 우수성·보안·안정성·성능 효율·비용 최적화·지속 가능성·卓越한 UX)의 결합이다. 아래는 3-Tier 웹 애플리케이션을 AWS·Kubernetes·Terraform 기반으로 구현한 표준 참조 아키텍처(Reference Architecture)이다.

```text
+--------------------------------------------------------------------+
|         Cloud-Native Reference Architecture (Multi-AZ)            |
+--------------------------------------------------------------------+
|                                                                    |
|  [Users/CDN]                                                       |
|      |                                                             |
|      v                                                            |
|  +--------------+    +--------------------------------------+      |
|  |  CloudFront  |---->|  Route 53 (Latency-Based Routing)    |      |
|  |  WAF + Shield|    +--------------+-----------------------+      |
|  +--------------+                   v                              |
|                           +------------------+                     |
|                           |   ALB / NLB      |  (L7 Path/Host)     |
|                           +--------+---------+                     |
|                                    v                              |
|            +-----------------------+-------------------+          |
|            v AZ-a                  v AZ-b              v AZ-c     |
|    +--------------+         +--------------+   +--------------+    |
|    |  EKS/ECS Pod |         |  EKS/ECS Pod |   |  EKS/ECS Pod |    |
|    |  (Stateless) |         |  (Stateless) |   |  (Stateless) |    |
|    +------+-------+         +------+-------+   +------+-------+    |
|           |                        |                  |            |
|           +------------+-----------+------------------+            |
|                        v                                          |
|           +--------------------------+                            |
|           |  Service Mesh (Istio)    |  mTLS, Circuit Breaker     |
|           +------------+-------------+                            |
|                        v                                          |
|      +-----------------+-----------------+                        |
|      v                                   v                        |
|  +------------+                  +--------------+                 |
|  |  Aurora    |                  | ElastiCache  |  (Redis 7.x)   |
|  |  MySQL/    |<-----ReadReplica--| Cluster Mode |                 |
|  |  PostgreSQL|                  +--------------+                 |
|  +------------+                                                  |
|                                                                    |
|  [Cross-Cutting]                                                  |
|   • CloudWatch/Prometheus+Grafana (Metrics)                       |
|   • Loki/CloudWatch Logs (Logs)                                   |
|   • Jaeger/Tempo (Distributed Tracing)                            |
|   • Terraform+Pulumi (IaC)                                        |
|   • ArgoCD/FluxCD (GitOps)                                        |
+--------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Edge Layer** | 글로벌 트래픽 라우팅·DDoS 방어·TLS Termination | CloudFront/Cloudflare(Anycast), AWS WAF(SQLi/XSS 룰셋), AWS Shield Advanced(L3/L4/L7 DDoS mitigation, 100Gbps 흡수) |
| **API Gateway** | 인증·인가, Rate Limiting, API 버전 관리, Request Validation | Kong/Ambassador/AWS API Gateway, OAuth 2.0+JWT 검증, Token Bucket 알고리즘(R=1000 req/s, Burst=2000) |
| **Container Orchestration** | 컨테이너 스케줄링·HPA·Self-Healing·Service Discovery | Kubernetes 1.29+ (K8s), Deployment/StatefulSet/Job CRD, HPA(v2 API, CPU 70%/Memory 80%/Custom Metric QPS), Cluster Autoscaler vs Karpenter(노드 프로비저닝 90초->15초) |
| **Service Mesh** | L7 트래픽 관리·mTLS·관찰성·폴트 인젝션 | Istio(Envoy sidecar), Linkerd(보다 가벼움 50MB vs 500MB), eBPF 기반 Cilium Service Mesh(2023+), mTLS STRICT 모드, Traffic Shifting(weight 기반 카나리) |
| **Data Layer** | 트랜잭션·분석·캐싱 분리, CQRS/Event Sourcing | Aurora(MySQL/PostgreSQL 호환, 6-way Replication, 15 Read Replicas), DynamoDB(Single-digit ms, On-Demand/Provisioned), ElastiCache Redis(Cluster Mode, Multi-AZ), S3(11 9s 내구성, IA/Glacier 계층화) |
| **Observability** | Metrics·Logs·Traces 통합 (3 Pillars) | Prometheus(시계열, PromQL, 30일 retention) + Grafana(대시보드), Loki(라벨 기반 로그 인덱싱), Tempo/Jaeger(OpenTelemetry 기반 분산 추적), SLO/SLI·Error Budget 기반 알림 |
| **IaC & GitOps** | 인프라 선언적 정의·상태 동기화·정책 적용 | Terraform 1.6+(HCL, State Lock with DynamoDB), Pulumi(TypeScript/Python 코드형 IaC), ArgoCD(Application CRD, Sync Wave, Prune), OPA/Kyverno(Policy-as-Code) |
| **Security Layer** | Zero-Trust, Secrets 관리, 컴플라이언스 | AWS IAM(Role-Based, Permission Boundary), KMS/HSM(Envelope Encryption, FIPS 140-2 L3), Secrets Manager/Vault(Dynamic Secrets, TTL 1h), GuardDuty(ML 기반 이상 탐지), Security Hub(CIS/NIST 통합), CloudTrail(관리 이벤트 90일->S3 장기 보관) |

**핵심 메커니즘 Deep-Dive:**

1. **Kubernetes HPA 알고리즘 (Horizontal Pod Autoscaler)**
   - `desiredReplicas = ceil[currentReplicas × (currentMetricValue / targetMetricValue)]`
   - stabilizationWindow: Scale Up 0s / Scale Down 300s (Flapping 방지)
   - HPA + VPA + Karpenter 조합으로 Pod·Resource·Node 3단계 자동 스케일링 구현

2. **CQRS + Event Sourcing 패턴**
   - Command(쓰기) -> Event Store(Kafka) -> Projection -> Read Model(별도 DB)
   - 강한 일관성보다 최종 일관성(Eventual Consistency) 수용, 감사 로그 자동 생성

3. **Circuit Breaker 패턴 (Hystrix -> Resilience4j)**
   - Closed -> Open(임계치 초과, e.g., 실패율 50%, 슬라이딩 윈도우 100 req) -> Half-Open(일부 트래픽 허용, e.g., 5 req/min)
   - Fallback: Cache -> Default Value -> Degraded Response

4. **Leader Election (분산 합의)**
   - Raft 알고리즘 기반 etcd/Consul, Quorum = ⌊N/2⌋+1
   - Split-Brain 방지를 위한 Fencing Token, Lease TTL 15s

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **자동화된 오케스트라**(지휘자=API Gateway, 현악=Kubernetes, 화성=Database)와 같다. 한 명의 지휘자가 코드(Composer Score=Terraform)로 악보를 정의하면, 각 악기(서비스)가 자동으로 조율되어 연주하며, 관객(사용자)이 늘면 자동으로 추가 의자가 배치되고(Autoscaling), 한 악기가 고장 나도 다른 악기가 빈자리를 메운다(Self-Healing).

---

## Ⅲ. 비교 및 연결

| 구분 | IaaS (EC2) | PaaS (Beanstalk/Heroku) | SaaS (Salesforce/Slack) | Serverless (Lambda) | FaaS + BaaS (Supabase/Firebase) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | 앱·데이터·런타임·미들웨어·OS | 앱·데이터만 (런타임/미들웨어 자동) | 사용만 (전부 CSP 관리) | 함수 코드만 (Cold Start 이슈) | 함수 + Baa스 SDK (DB/Auth/Storage) |
| **확장 단위** | 인스턴스 | 컨테이너/Process | 사용자 라이선스 | 동시성(Concurrency) | 동시성 + 자동 BaaS |
| **Cold Start** | 없음 (상시 기동) | 10~30초 | 없음 | 100ms~3s (SnapStart로 200msv) | 100ms~1s |
| **Max 실행 시간** | 무제한 | 제한(예: 12h) | 무제한 | 15분 (Lambda) | 15분 + DB 트랜잭션 |
| **과금 단위** | 인스턴스 시간 | 인스턴스 시간 | 사용자/월 | 1ms 단위 + 호출 횟수 | 1ms + BaaS API 호출 |
| **적합 워크로드** | 레거시·상태 유지·장기 배치 | 웹앱·API·표준 스택 | CRM·협업·정형 업무 | Event-Driven·단순 API·ETL | 모바일 BaaS·실시간 앱 |
| **Lock-in 위험** | 중간 (VM 이미지 포팅 가능) | 높음 (Heroku Buildpack) | 매우 높음 | 높음 (벤더 종속 API) | 매우 높음 (Baa스 SDK) |
| **예시** | EC2, GCE, Azure VM | Elastic Beanstalk, App Engine | Office 365, GitHub | Lambda, Cloud Functions | Firebase, Supabase |

**클라우드 마이그레이션 전략 (6R Framework) 비교:**

| 전략 | 변경 정도 | 비용 | 위험도 | 소요 시간 | 적용 사례 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Rehost (Lift & Shift)** | 0% | 낮음 | 낮음 | 1~3개월 | 파일서버, 단순 웹 |
| **Replatform** | 10~20% | 중간 | 중간 | 3~6개월 | DB를 RDS로, WAS를 ECS로 |
| **Repurchase** | 100% 교체 | 초기 높음 | 낮음 | 1~2개월 | CRM -> Salesforce |
| **Refactor / Re-architect** | 50~100% | 높음 | 높음 | 6~18개월 | 모놀리식 -> MSA |
| **Retire** | 폐기 | 회수 | - | 즉시 | 미사용 자산 |
| **Retain** | 유지 | - | - | - | 보안·규제로 온프레미스 유지 |

**연계 기술 스택 맵:**
- **IaC**: Terraform ↔ Ansible ↔ Pulumi ↔ AWS CDK (선언적 ↔ 명령형)
- **Container**: Docker ↔ Podman ↔ containerd ↔ CRI-O
- **Orchestration**: Kubernetes ↔ Nomad ↔ Docker Swarm ↔ Mesos
- **CI/CD**: Jenkins ↔ GitLab CI ↔ GitHub Actions ↔ Argo Workflows
- **Service Mesh**: Istio ↔ Linkerd ↔ Consul Connect ↔ Cilium
- **Observability**: Prometheus+Grafana ↔ Datadog ↔ New Relic ↔ Dynatrace

- **📢 섹션 요약 비유**: IaaS는 **빈 토지**(개발자가 건물·인
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 703 / 800

<- **이전**: [702. 클라우드 아키텍처 핵심 토픽 702번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/702_cloud_architecture_core_topic_702_exam_summar/)
**다음**: [704. 클라우드 아키텍처 핵심 토픽 704번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/704_cloud_architecture_core_topic_704_exam_summar/) ->

---
