---
title: "Cloud Architecture Core Topic 545 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 퍼블릭/프라이빗/하이브리드 클라우드 환경에서 12-Factor App, MSA, 컨테이너 오케스트레이션(Kubernetes), 서버리스, IaC(Terraform/CloudFormation), Service Mesh(Istio/Linkerd)를 통합한 **Well-Architected Framework** 기반의 Cloud-Native 아키텍처 설계 원리
> 2. **가치**: AWS Well-Architected 기준 적용 시 운영 비용 30~40% 절감, 가용성 99.99% 달성, 배포 빈도 200배 증가(Netflix 사례: 일 1,000회 배포), Time-to-Market 75% 단축, Auto-Scaling을 통한 CAPEX->OPEX 전환
> 3. **판단 포인트**: 단일 클라우드 종속(Vendor Lock-in) vs 멀티/하이브리드, Synchronous API vs Event-Driven(EDA, Kafka/SQS), Stateful(외부 RDB/Redis) vs Stateless Pod, Egress 비용·지연시간 vs 데이터 주권, Sidecar Pattern 도입 시 mTLS overhead 약 8~15%

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 더 이상 단순한 "서버를 빌려 쓰는 것"이 아니라, **탄력성(Elasticity)·탄력적 확장·자가 치유(Self-healing)·관측 가능성(Observability)**을 코드로 구현하는 엔지니어링 패러다임이다. 마이크로서비스(MSA), 컨테이너, IaC, CI/CD, GitOps가 융합되어 **Cloud Native Computing Foundation(CNCF)** 생태계를 형성하며, 전통적 모놀리식 데이터센터 아키텍처와는 설계 철학 자체가 다르다.

### 모놀리식 vs Cloud-Native 패러다임 비교

| 구분 | 모놀리식 On-Premise | Cloud-Native |
|------|---------------------|--------------|
| 배포 단위 | WAR/EAR (월~분기) | 컨테이너/Function (시간~분) |
| 확장성 | 수직 스케일(Scale-Up) | 수평 스케일(Scale-Out) |
| 장애 격리 | 프로세스 단위 격리 불가 | Cell/Pod 단위 격리, Circuit Breaker |
| 변경 영향도 | 전체 시스템 영향 | 서비스 단위 독립 배포 |
| 인프라 관리 | 수동/스크립트 | 선언적 IaC (Terraform/Helm) |
| 비용 모델 | CAPEX (5년 감가상각) | OPEX (사용량 기반 과금) |

```text
[전통 모놀리식 아키텍처 - 3-Tier]
+---------------------------------------------+
| Client (Browser)                            |
+-------------+-------------------------------+
              | HTTP/S
              v
+---------------------------------------------+
| WebLogic/WAS (단일 인스턴스, 수직 확장)        |
|  +---------+  +---------+  +----------+    |
|  |  Web    |  |  Biz    |  |   EJB    |    |
|  | (JSP)   |-> | Logic   |-> | (Entity) |    |
|  +---------+  +---------+  +----------+    |
+-------------+-------------------------------+
              | JDBC
              v
+---------------------------------------------+
| Oracle RAC / SAN Storage (단일 장애점)         |
+---------------------------------------------+

              v 전환 v

[Cloud-Native MSA 아키텍처]
+----------------------------------------------+
| CloudFront / Cloud CDN (Global Edge)         |
+--------------+-------------------------------+
               |
        +------v------+
        |   WAF/ALB   | (L7 로드밸런싱)
        +------+------+
               |
   +-----------+-----------+-------------+
   v           v           v             v
+------+  +------+  +------+      +----------+
|Auth  |  |Order |  |Cata- |      | API      |
|Srv   |  |Srv   |  |log   |  ... | Gateway  |
|(Pod×N|  |(Pod×N|  |Srv   |      |(Kong/    |
| EKS) |  | EKS) |  |      |      | Apigee)  |
+--+---+  +--+---+  +--+---+      +----------+
   |         |         |
   +----+----+----+----+
        v         v
   +--------+  +--------+  +---------+
   |Aurora  |  |DynamoDB|  | Elasti- |
   |MySQL   |  |(NoSQL) |  | cache   |
   |(Multi- |  |Global  |  | Redis   |
   | AZ)    |  | Table  |  | Cluster |
   +--------+  +--------+  +---------+
        |         |         |
        +----+----+----+----+
             v         v
        +-----------------+
        |  S3 / Kafka     |
        |  (Object Store  |
        |   + Event Bus)  |
        +-----------------+
```

### 왜 이제 Cloud-Native인가?

- **시장 요구**: Gartner 2024 보고서 - 신규 디지털 워크로드의 **75%**가 클라우드 네이티브
- **비용 효율**: AWS 사례 - Auto Scaling + Spot Instance로 동일 트래픽 처리 시 비용 60% 절감
- **비즈니스 민첩성**: Capital One - 모놀리식 대비 배포 빈도 **46배**, 장애 복구 시간(MTTR) **5,600배** 단축
- **기술 표준화**: Kubernetes(K8s)가 **CNCF 88%의 프로덕션 환경**에서 컨테이너 오케스트레이션 표준으로 자리매김

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 마치 **"택시 호출 서비스(Kakao T)"**와 같다. 수요가 늘면 차량이 자동으로 배차(오토스케일링)되고, 고장 난 차량은 즉시 다른 차량이 대체(자가 치유)하며, 이용 요금만 정산(사용량 과금)하면 된다. 반면 자가용을 소유(On-Premise)하면 주차장 유지보수, 보험, 정비를 모두 직접 해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Cloud-Native 아키텍처의 핵심은 **4C(Culture, Code, Cloud, Container)** 와 **Cattle vs Pet(가축 vs 애완동물)** 사상이다. Kubernetes가 이를 구현하는 사실상의 표준 런타임이며, 12-Factor App이 설계 원칙을 정의한다.

### 12-Factor App 핵심 원칙 (Heroku, 2011)

| # | Factor | 핵심 구현 | 클라우드 매핑 |
|---|--------|----------|---------------|
| 1 | Codebase | 단일 Git Repo -> 다중 배포 | GitHub/GitLab, Branch per Env |
| 2 | Dependencies | 명시적 의존성 선언 | requirements.txt, package.json, OCI Image |
| 3 | Config | 환경변수 분리, ConfigMap/Secret | Vault, AWS SSM Parameter Store, K8s ConfigMap |
| 4 | Backing Services | DB/Cache를 Attached Resource로 | RDS, ElastiCache, S3 |
| 5 | Build, Release, Run | 3단계 엄격 분리 | Jenkins/ArgoCD + Helm + K8s Rollout |
| 6 | Processes | Stateless 프로세스, Shared Nothing | HPA, Session은 Redis로 외부화 |
| 7 | Port Binding | 자체 포트 바인딩 (외부 웹서버 불요) | 컨테이너의 EXPOSE, Service Port |
| 8 | Concurrency | 프로세스 모델로 수평 확장 | ReplicaSet, Deployment |
| 9 | Disposability | 빠른 시작/정상 종료 (SIGTERM 처리) | PreStop Hook, Grace Period 30s |
| 10 | Dev/Prod Parity | Dev=Prod 환경 일치 | IaC(Terraform)로 동일 스택 |
| 11 | Logs | Stdout/Stderr로 이벤트 스트림 | Fluentd -> CloudWatch/Loki/ELK |
| 12 | Admin Processes | REPL/관리 작업도 동일 환경에서 실행 | kubectl exec, Cloud Shell |

```text
[Kubernetes Pod 내부의 12-Factor Sidecar 패턴]
+--------------- Pod (192.168.1.10) ---------------+
|                                                   |
|  +-----------------+      +------------------+  |
|  | App Container   |      | Sidecar: Envoy   |  |
|  | (User Service)  |◄----►| (Service Mesh)   |  |
|  |                 |      |                  |  |
|  | • Port 8080     |      | • mTLS 자동      |  |
|  | • Env Var:      |      | • Circuit Breaker|  |
|  |   DB_URL=...    |      | • Metrics export |  |
|  | • Log: STDOUT   |      | • Log: STDOUT    |  |
|  +--------+--------+      +---------+--------+  |
|           |                         |           |
|           +------------+------------+           |
|                        |                        |
|              +---------v----------+             |
|              |  Shared Volume     |             |
|              |  /var/log (EmptyDir|             |
|              |   -> Fluentd로 수거)|             |
|              +--------------------+             |
+--------------------------------------------------+
```

### 핵심 구성 요소 테이블

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **API Gateway** | 외부 트래픽 진입점, 라우팅·인증·Rate Limit | Kong(Plugin 기반, Lua JIT), AWS API Gateway(10K RPS 한도), Apigee(Analytics), NGINX Plus(고성능 L7) |
| **Service Mesh** | 서비스 간 mTLS, 트래픽 관리, 관측 | Istio(Envoy 기반, Control Plane xDS API), Linkerd(Linkerd2-proxy Rust, 4x 경량), Consul Connect |
| **Container Orchestrator** | 컨테이너 스케줄링, 자가 치유, 롤링 업데이트 | Kubernetes(K8s) - 93% 점유율, ECS(Fargate), Nomad(HashiCorp) |
| **IaC (Infrastructure as Code)** | 인프라 선언적 프로비저닝, 버전 관리 | Terraform(HCL, 멀티 클라우드), Pulumi(TS/Python), CloudFormation(전용), Ansible(설정 관리) |
| **CI/CD Pipeline** | 지속적 통합/배포 자동화 | GitHub Actions, GitLab CI, Jenkins X, ArgoCD(GitOps), Spinnaker(Netflix) |
| **Observability Stack** | 메트릭·로그·트레이스 통합 | Prometheus + Grafana(메트릭), Loki(로그), Jaeger/Tempo(분산 트레이싱), OpenTelemetry(SDK 표준) |
| **Serverless Platform** | 이벤트 기반 FaaS, Cold Start 이슈 | AWS Lambda(15분 한도), Cloud Run(Knative 기반), Azure Functions, Knative(Event-driven K8s) |
| **Event Streaming** | 비동기 메시징, CQRS, Event Sourcing | Apache Kafka(처리량 100만 msg/s), AWS Kinesis(Shard 기반), Pulsar, NATS(경량) |

### Kubernetes 아키텍처 핵심 동작 원리

```text
[Kubernetes Control Plane + Worker Node 상세]
+------------------- Control Plane ---------------------+
|                                                        |
|  +----------+  +----------+  +----------+  +------+ |
|  | kube-api |  |etcd      |  |scheduler |  |control| |
|  | server   |  |(분산     |  |(리소스   |  |manager| |
|  | (REST    |  | KV Store)|  | 기반     |  |(상태  | |
|  | 6443)    |  | Raft)    |  | binpack) |  | 조정) | |
|  +----+-----+  +----------+  +----------+  +------+ |
+-------+----------------------------------------------+
        | gRPC / HTTP
        v
+-------------------- Worker Node ---------------------+
|                                                        |
|  +----------+  +----------+  +------------------+   |
|  | kubelet  |  |kube-proxy|  | Container Runtime |   |
|  |(Pod 관리,|  |(iptables/|  | (containerd,      |   |
|  | Liveness |  | IPVS로   |  |  CRI-O)           |   |
|  | Probe)   |  | Service  |  |                   |   |
|  |          |  | 라우팅)  |  |                   |   |
|  +----------+  +----------+  +------------------+   |
|       |                                               |
|       v                                               |
|  +---- Pod1 -----+  +---- Pod2 -----+               |
|  | App + Sidecar |  | App Container |               |
|  +---------------+  +---------------+               |
+--------------------------------------------------------+

[Auto-Scaling 결정 흐름]
HPA: CPU/Mem/Custom Metric -> metrics-server -> kube-apiserver
   v (30초 주기)
Desired Replicas = ceil(currentReplicas × currentMetricValue / targetMetricValue)
   예: 현재 5 Pod, CPU 80%, 목표 50% -> ceil(5 × 80/50) = 8 Pod
   v
HPA Controller가 Deployment.spec.replicas 업데이트
   v
Deployment Controller가 신규 Pod 생성 (Rolling Update)
```

### Well-Architected Framework 6대 Pilar (AWS 기준)

| Pilar | 핵심 질문 | 주요 모범 사례 |
|------|----------|----------------|
| **Operational Excellence** | 운영을 잘 하고 있는가? | IaC, GitOps, Observability, Runbook 자동화 |
| **Security** | 안전한가? | Zero Trust, mTLS, KMS, IAM 최소권한, Secrets 관리 |
| **Reliability** | 장애 대비가 되어 있는가? | Multi-AZ/Region, Circuit Breaker, Chaos Engineering (Chaos Monkey) |
| **Performance Efficiency** | 성능 최적화? | 캐싱(CDN/Redis), DB 인덱싱, Right-Sizing, GPU 가속 |
| **Cost Optimization** | 비용 효율? | Spot Instance, Reserved/Savings Plan, S3 Intelligent-Tiering |
| **Sustainability** | 환경 영향 최소화? | 리전별 탄소 발자국, Auto Scaling으로 유휴 자원 제거 |

- **📢 섹션 요약 비유**: 12-Factor App은 **"출장 가이드북"**과 같다. 호텔은 어디서든(Config), 짐은 가볍게(Stateless), 여권은 본인 확인(API Key), 영수증은 기록(Log)하는 원칙이다. 클라우드 환경 어디서든 같은 방식으로 동작하도록 만드는 매뉴얼인 셈이다.

---

## Ⅲ. 비교 및 연결

### 모놀리식 vs MSA vs Serverless 비교

| 구분 | Monolith | Microservice (MSA) | Serverless (FaaS) |
|------|----------|---------------------|-------------------|
| **배포 단위** | 단일 WAR/E
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 545 / 800

<- **이전**: [544. 클라우드 아키텍처 핵심 토픽 544번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/544_cloud_architecture_core_topic_544_exam_summar/)
**다음**: [546. 클라우드 아키텍처 핵심 토픽 546번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/546_cloud_architecture_core_topic_546_exam_summar/) ->

---
