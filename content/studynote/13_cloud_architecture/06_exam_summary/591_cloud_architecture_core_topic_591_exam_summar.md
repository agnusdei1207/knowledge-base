---
title: "591. 클라우드 아키텍처 핵심 토픽 591번 시험 요약 (Cloud Architecture Core Topic 591 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 IaaS/PaaS/SaaS/FaaS의 서비스 모델과 Public/Private/Hybrid/Multi의 배치 모델을 12-Factor, Cell-Based, Well-Architected 5대 원칙(운영 우수성·보안·안정성·성능 효율·비용 최적화)으로 결합하여 CAP/ACID/BASE 트레이드오프 위에서 워크로드의 회복탄력성·확장성·관측가능성(Observability)을 동적으로 보장하는 분산 시스템 설계 패러다임이다.
> 2. **가치**: AWS Well-Architected Review 기준 모범 사례 적용 시 가용성 99.99%(연 52.6분 이내 장애), 장애 복구 시간 70% 단축, TCO 30~50% 절감, Auto Scaling을 통한 컴퓨팅 비용 60~80% 절감(개발/테스트 환경 기준) 효과를 달성할 수 있다.
> 3. **판단 포인트**: Lift-and-Shift(Rehost) vs Cloud-Native Refactor(Replatform/Refactor) 선택, 단일 클라우드 종속(Vendor Lock-in) vs Multi-Cloud 간 거버넌스 복잡도, 동적 확장(Ephemerality) vs 운영 복잡도, Stateless vs Stateful 워크로드 분리, FinOps 기반 비용 가시성 확보 여부가 4대 아키텍처 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

전통적인 On-Premise 3-Tier 아키텍처(Presentation-Logic-Data)는 CAPEX 중심의 용량 계획(Capacity Planning) 기반 수직 확장(Scale-Up) 방식으로, 트래픽 피크 대비 30~40%의 과잉 Provisioning과 평균 18~24개월의 HW 조달 리드타임을 수반한다. 2020년 이후 COVID-19 디지털 전환 가속화에 따라 Netflix(2020년 1월 단일 시간 700만 시청 동시접속), 우아한형제들(배민 - 2021년 트래픽 12배 급증 사례) 등 대규모 워크로드의 탄력적 처리가 비즈니스 생존의 핵심 요건이 되었고, IDC 보고서(2023)에 따르면 전 세계 엔터프라이즈 워크로드의 68%가 2025년까지 클라우드 우선(Cloud-First) 전략을 채택할 것으로 전망된다.

클라우드 아키텍처는 이를 해결하기 위해 **선언적 API(Declarative API)**, **불변 인프라(Immutable Infrastructure)**, **인프라 as 코드(IaC)**, **셀 기반 아키텍처(Cell-Based Architecture)**, **가드레일 기반 셀프서비스(Guardrail-based Self-Service)**를 핵심 원리로 채택하며, AWS·Azure·GCP 등 Hyperscaler가 제공하는 200여 종의 관리형 서비스(예: S3 99.999999999% 내구성, DynamoDB Single/Multi-Region Auto Scaling, Aurora Global Database 1초 미만 Cross-Region 복제)를 활용하여 운영 부담을 70% 이상 경감시킨다.

```text
[클라우드 아키텍처 진화 패러다임]
+------------------------------------------------------------------+
|  On-Premise (1990s)  ->  Virtualization (2000s)  ->  Cloud IaaS   |
|  +--------+             +--------------+          +----------+  |
|  |Server  |             |Hypervisor    |          |EC2 VM   |  |
|  |Storage |             |vSphere/KVM   |          |EBS/GP3  |  |
|  |Network |             |vLAN/VXLAN    |          |VPC/Sub  |  |
|  +--------+             +--------------+          +----------+  |
|   물리 HW 의존            Soft-defined              API-Defined  |
|  -------------------------------------------------------------- |
|         v                        v                       v      |
|  Cloud-Native (2015~)    Serverless/Edge (2020~)  AI-Native (2024~)|
|  +--------------+        +--------------+        +-------------+|
|  |K8s/Microsvc  |        |Lambda/Edge   |        |GPU Pool/ML  ||
|  |Service Mesh  |        |Event-Driven  |        |LLM Serving  ||
|  |GitOps/IaC    |        |Pay-per-Use   |        |Vector DB    ||
|  +--------------+        +--------------+        +-------------+|
+------------------------------------------------------------------+
```

**전통적(On-Premise) vs 클라우드 네이티브** 비교:
- **자원 조달**: HW 발주 18~24주 vs API 호출 30초 (EC2 RunInstances)
- **확장 단위**: 물리 서버 수직 확장 vs Horizontal Pod Autoscaler(HPA, 15초 스케일링)
- **장애 대응**: Cold Standby(수동) vs Multi-AZ Auto-Healing(자동, 90초 내 복구)
- **비용 모델**: CapEx(5년 감가상각) vs OpEx(Pay-per-Use, 초/GB 단과금)
- **배포 주기**: 분기 1회 수동 배포 vs GitOps 기반 일 50~100회 배포(Spotify 사례)

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 "모든 전기 기구를 직접 발전기에 연결하던 시절"에서 "전기를 콘센트에서 뽑아 쓰고, 사용량만큼만 요금을 내는 스마트 그리드"로의 전환과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **5계층 참조 모델(Reference Model)** 위에서 설계되며, 각 계층은 명확한 책임 분리(Separation of Concerns)와 느슨한 결합(Loose Coupling)을 통해 진화적 변경(Evolutionary Change)을 가능케 한다.

```text
[5계층 클라우드 참조 아키텍처 (AWS Well-Architected 기반)]
+---------------------------------------------------------------------+
| Layer 5: Application & Data Plane                                    |
| +----------------------------------------------------------------+ |
| | SaaS (Slack/Salesforce) | FaaS (Lambda@Edge) | Microservice    | |
| | BFF/API Gateway(Kong)   | GraphQL Federation | Event Sourcing | |
| +----------------------------------------------------------------+ |
+---------------------------------------------------------------------+
| Layer 4: Platform & Orchestration Plane                              |
| +----------------------------------------------------------------+ |
| | EKS/AKS/GKE | Service Mesh(Istio/Linkerd) | ArgoCD/Flux       | |
| | K8s Operator Pattern | Crossplane | Backstage(IDP)             | |
| +----------------------------------------------------------------+ |
+---------------------------------------------------------------------+
| Layer 3: Data & Messaging Plane                                      |
| +----------------------------------------------------------------+ |
| | RDBMS(Aurora) | NoSQL(DynamoDB/MongoDB) | Kafka/MSK           | |
| | S3/Data Lake | Redis/ElastiCache | Vector DB(Pinecone)         | |
| +----------------------------------------------------------------+ |
+---------------------------------------------------------------------+
| Layer 2: Infrastructure & Network Plane                              |
| +----------------------------------------------------------------+ |
| | VPC/TGW/Cloud WAN | PrivateLink | WAF/Shield | ALB/NLB/GWLB    | |
| | IaC(Terraform/CloudFormation/CDK) | OPA/Kyverno(Policy)        | |
| +----------------------------------------------------------------+ |
+---------------------------------------------------------------------+
| Layer 1: Foundation Plane (Account/Identity/Edge)                    |
| +----------------------------------------------------------------+ |
| | AWS Organizations/SCPs | IAM/IAM Identity Center | KMS/HSM     | |
| | CloudFront/Azure CDN | Route 53/GeoDNS | GuardDuty/Security Hub| |
| +----------------------------------------------------------------+ |
+---------------------------------------------------------------------+
        |              |              |              |
        v              v              v              v
  Observability:  CloudWatch/Prometheus+Grafana/Loki/OTel/Datadog
  FinOps:         Cost Explorer/Vantage/APPTIO/Infracost
  SecOps:         SIEM(Splunk)/CSPM(Wiz)/CWPP
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Service Mesh (Istio/Linkerd)** | 마이크로서비스 간 mTLS, 트래픽 관리, 관측 | Sidecar Envoy Proxy 기반 L7 라우팅(Canary 90/10), Circuit Breaker(5xx 50% 시 자동 차단), 분산 트레이싱(W3C TraceContext, 128-bit TraceID) |
| **API Gateway (Kong/AWS API GW)** | 외부 트래픽 진입점, 인증/인가, 속도 제한 | OAuth 2.0 + JWT 검증, Token Bucket 알고리즘(RPS 기반), OpenAPI 3.0 스펙 자동 임포트, Lambda Authorizer로 OIDC 통합 |
| **Event Bus (Kafka/EventBridge)** | 비동기 이벤트 라우팅, CQRS/Event Sourcing | Kafka: 파티션 키 기반 순서 보장, Exactly-Once Semantics(EOS), ISR(In-Sync Replica) 최소 2, EventBridge: SaaS 통합 35+ 종 대상 |
| **IaC (Terraform/CloudFormation)** | 선언적 인프라 자동화, Drift Detection | HCL/JSON 선언형, State Lock(DynamoDB), Plan/Apply 2단계 승인, 모듈화(Module Registry), OPA로 Policy as Code 검증 |

**핵심 원리 상세**:

1. **12-Factor App (Heroku, 2011)**: Codebase(1), Dependencies(2), Config(4), Backing Services(6), Build/Release/Run(5), Processes(6-factor stateless), Port Binding(7), Concurrency(8), Disposability(9), Dev/Prod Parity(10), Logs(11), Admin Processes(12) — 컨테이너 오케스트레이션 시대의 기본 원칙.

2. **AWS Well-Architected 5 Pillars** (2023 개정):
   - **운영 우수성**: MTTR(평균복구시간) < 15분, 변경 실패율 < 15%
   - **보안**: IAM 최소권한(Least Privilege), Encryption at Rest/Transit(KMS, TLS 1.3), Zero Trust(Strong Identity 기반)
   - **안정성**: RTO(복구시간목표) / RPO(복구시점목표) 워크로드별 정의, Multi-AZ 99.99%, Multi-Region 99.999%
   - **성능 효율**: Compute Right-Sizing(Graviton3 대비 x86 40% 성능/달러 우위), Caching 지연 < 10ms(p99)
   - **비용 최적화**: Reserved/Spot/On-Demand 3-way Mix, Savings Plans 1/3년 약정 40~60% 할인

3. **CAP 정리 (Brewer, 2000)**: 분산 시스템은 Consistency·Availability·Partition tolerance 중 2가지만 보장 가능. RDBMS는 CP(예: Google Spanner, TrueTime API), DynamoDB/Cassandra는 AP, etcd/ZooKeeper는 CP로 분류. 기술사 논술에서는 PACELC(정상 시 Latency vs Consistency 트레이드오프)까지 확장.

4. **장애 도메인 격리 (Cell-Based Architecture)**: AWS 내부에서 사용하는 패턴으로, 사용자를 N개 독립 Cell(예: 100개)로 분할하여 1개 Cell 장애가 전체의 1%만 영향. Netflix는 2019년 Chaos Engineering으로 Cell 단위 장애 주입(GameDay) 운영.

- **📢 섹션 요약 비유**: 클라우드 아키텍처의 5계층은 "건물의 기초(전원·배관)->골조(철근·콘크리트)->배관·전기(설비)->인테리어(내부 구조)->실내 장식(사용자 경험)"처럼, 아래층이 위층을 지탱하면서도 독립적으로 교체 가능한 모듈식 건축과 같다.

---

## Ⅲ. 비교 및 연결

| 구분 | IaaS (EC2) | PaaS (Elastic Beanstalk) | SaaS (Salesforce) | FaaS (Lambda) |
| :--- | :--- | :--- | :--- | :--- |
| **관리 범위** | App/Data/Runtime/미들웨어/OS/가상화/서버/스토리지/네트워크 | App/Data만 (런타임/미들웨어/OS는 CSP 관리) | 모두 CSP 관리 (사용자는 설정/데이터만) | 코드(함수)만 — 트리거 기반 단명 실행(15분) |
| **확장 단위** | Instance 단위 수동/Auto Scaling | Application 단위 Auto Scaling | 사용자 수 자동 확장 | 동시실행(Concurrency) 단위(기본 1000) |
| **콜드 스타트** | 30~60초(AMI 부팅) | 2~5분(환경 프로비저닝) | 즉시 | 100ms~5초(VPC Lambda는 5초, Provisioned Concurrency 시 0) |
| **과금 모델** | 시간/초(per-second, 최소 60초) | 시간당 인스턴스 | 사용자/월 구독 | 요청 수(100만 회 $0.20) + GB-초 |
| **적합 워크로드** | 레거시 Lift&Shift, 커스텀 OS/하이퍼바이저 필요 시 | 표준 웹앱, 빠른 PoC | CRM/ERP 등 범용 업무 | 이벤트 기반, 간헐적·버스트성, Glue 작업 |

**Multi-Cloud vs Hybrid Cloud 비교** (아키텍처 관점):

| 구분 | Single Cloud | Multi-Cloud | Hybrid Cloud |
| :--- | :--- | :--- | :--- |
| **정의** | 1개 CSP(AWS) | 2개 이상 CSP 동시 사용(AWS+Azure) | On-Prem + Public Cloud 혼용 |
| **주 목적** | 운영 단순화, 비용 최적화 | 벤더 종속 회피, Best-of-Breed | 데이터 주권, 레거시 연동 |
| **네트워크** | VPC Peering/Transit GW | Cloud Interconnect + Direct Connect + ExpressRoute | VPN/Direct Connect(평균 8~12ms) |
| **거버넌스 복잡도** | 낮음 | 높음(Terraform Module 분기, IaC 추상화 필요) | 중간 |
| **TCO 영향** | EDP(Enterprise Discount) 5~15% 추가 할인 가능 | +15~25%(학습/도구/이중 운영) | +20~30% |
| **적합 기업** | 스타트업·중견기업 | 글로벌 대기업·규제 산업 | 금융·공공·제조 |

**연계 기술**:
- **IaC 도구 체인**: Terraform(Cross-Provider) + Atlantis(GitOps PR) + Infracost(PR 단위 비용 리포트) + Checkov(Security Scan)
- **관측가능성(Observability) 3요소**: Metrics(Prometheus/Cortex) + Logs(Loki/ELK) + Traces(Jaeger/Tempo) — OpenTelemetry(OTel) SDK로 통합 계측
- **보안**: CSPM(Cloud Security Posture Management) — Wiz/Lacework가 Multi-Cloud 정책 통합 관리, CIEM(Cloud Entitlements Management) — CloudKnox로 권한 남용 탐지

- **📢 섹션 요약 비유**: Single Cloud는 "한 식당의 모든 코스 집중", Multi-Cloud는 "세계 각국 레스토랑 체인 출점(거버넌스 필수)", Hybrid Cloud는 "본사 주방 + 외부 레스토랑 동시 운영"으로 비유할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **워크로드 분류(Workload Profiling)를 수행했는가?** — CPU-bound(이미지처리) vs I/O-bound(DB) vs Network-bound(API Gateway) vs
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 591 / 800

<- **이전**: [590. 클라우드 아키텍처 핵심 토픽 590번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/590_cloud_architecture_core_topic_590_exam_summar/)
**다음**: [592. 클라우드 아키텍처 핵심 토픽 592번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/592_cloud_architecture_core_topic_592_exam_summar/) ->

---
