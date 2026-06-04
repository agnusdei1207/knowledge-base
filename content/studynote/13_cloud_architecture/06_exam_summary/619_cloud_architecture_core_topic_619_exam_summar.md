---
title: "619. 클라우드 아키텍처 핵심 토픽 619번 시험 요약 (Cloud Architecture Core Topic 619 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처 619번은 NIST 클라우드 컴퓨팅 참조 모델(서비스/배포 모델 5×3 매트릭스)을 기반으로, **클라우드 네이티브 12-Factor, 마이크로서비스, 컨테이너 오케스트레이션(Kubernetes), IaC, 서버리스, 서비스 메시, 옵저버빌리티, FinOps**를 하나의 통합 참조 아키텍처로 결합한 기술사형 의사결정 프레임워크이다.
> 2. **가치**: 적정 규모 용량(Just-in-Time Provisioning)으로 CapEx를 OpEx로 전환하고(전형적으로 인프라 비용 30~70% 절감), 가용성 99.99%(Four-Nines, 연간 52.56분 다운타임) SLA, 자동 스케일링을 통한 트래픽 변동 흡수, MTTR 단축(블루-그린/카나리 배포로 평균 70% 배포 리스크 감소)을 달성한다.
> 3. **판단 포인트**: 6R 마이그레이션 전략(Rehost/Replatform/Refactor/Repurchase/Retire/Retain) 중 어느 것을 채택할지, **단일 클라우드 vs 멀티/하이브리드**의 트레이드오프(벤더 락인 vs 운영 복잡성), **수직/수평 스케일링**, **강일관성(ACID) vs 최종일관성(BASE)**, **Stateful vs Stateless** 워크로드 분리 기준이 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

클라우드 아키텍처는 단순히 "IDC를 AWS/Azure/GCP로 대체"하는 것이 아니라, **탄력성(Elasticity)**, **확장성(Scalability)**, **무중단 배포(Zero-Downtime Deployment)**, **셀프 서비스 프로비저닝**, **사용량 기반 과금(Usage-Based Pricing)**이라는 5대 NIST 필수 특성(essential characteristics)을 만족하도록 시스템을 재설계하는 엔지니어링 discipline이다.

기존 모놀리식 On-Premise 환경은 물리 서버 도입에 평균 6~12주 소요, 용량 계획(capacity planning) 실패로 인한 과잉 투자(평균 30%) 또는 서비스 장애, 장애 대응을 위한 HA 클러스터 운영 부담(예: Oracle RAC, VMware HA)이라는 한계를 가졌다. 클라우드 아키텍처는 **인프라 추상화(Infrastructure Abstraction)**, **선언적 API(Declarative API)**, **불변 인프라(Immutable Infrastructure)**, **GitOps 기반 운영**을 통해 이를 해소한다.

```text
+---------------------------------------------------------------------+
|          클라우드 아키텍처 패러다임 전환 (On-Premise -> Cloud-Native)   |
+--------------------------+------------------------------------------+
|     On-Premise (전통)      |        Cloud-Native (현대)               |
+--------------------------+------------------------------------------+
|  물리/가상 서버 수동 구성    |   코드형 인프라(IaC: Terraform, CFN)     |
|  수직 스케일링 (Scale-Up)  |   수평 스케일링 (Scale-Out) + Auto-Scale |
|  모놀리식 단일 배포단위     |   마이크로서비스 + 컨테이너 + k8s        |
|  수동 장애조치(DR) Runbook |   셀프힐링(Self-Healing) + SRE           |
|  CapEx 중심 (5년 감가상각) |   OpEx 중심 (Pay-as-you-go)             |
|  Strong Consistency (RDB) |   Eventual Consistency (NoSQL/Streaming)|
|  수동 Capacity Planning   |   Predictive Auto-Scaling (ML 기반)     |
|  VPN/방화벽 경계 보안      |   Zero Trust + mTLS + Workload Identity |
|  MTTR 평균 수십분~수시간   |   MTTR 수십초 (자동 롤백 + 카나리 분석)  |
+--------------------------+------------------------------------------+
                |
                v
   +------------------------------------------+
   |  기술사 시험의 핵심: "왜(Why)", "언제(When)", |
   |  "어떻게(How) 마이그레이션/리팩토링할 것인가"    |
   +------------------------------------------+
```

전통적 아키텍처 대비 클라우드 아키텍처는 **12-Factor App 방법론**, **Cloud Native Computing Foundation(CNCF) Landscape 30+ 카테고리**, **Well-Architected 5대 기둥**(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화, 지속가능성)을 의사결정 기준으로 사용한다. 기술사 시험은 단순 암기가 아닌 **시나리오 기반 트레이드오프 분석**을 요구한다.

- **📢 섹션 요약 비유**: 기존 온프레미스는 **직접 짓고 관리하는 아파트**(건물주 직접 관리, 입주까지 6개월)이고, 클라우드 아키텍처는 **호텔 체인 네트워크**(전 세계 어디서나 클릭 한 번에 체크인, 사용한 일수/객실 수만 결제, 만실이면 자동 증축)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 논리적으로 **4계층 참조 모델(Reference Architecture)**로 분해된다. 각 계층은 독립적으로 진화하며, 명확한 책임 분리(SoC: Separation of Concerns)를 통해 변경 영향도를 최소화한다.

```text
   +----------------------------------------------------------+
   |  L4. Application & Data Plane (워크로드 계층)              |
   |  - Microservices, Serverless(FaaS), API                  |
   |  - DB: RDB(PostgreSQL) + NoSQL(DynamoDB, MongoDB)        |
   |  - Cache: Redis, Memcached, ElastiCache                  |
   +----------------------------------------------------------+
   |  L3. Orchestration & Platform (오케스트레이션 계층)        |
   |  - Kubernetes (k8s), EKS/AKS/GKE, Service Mesh(Istio)    |
   |  - API Gateway (Kong, Apigee, AWS API GW)                |
   |  - Service Discovery, ConfigMap, Secret Management        |
   +----------------------------------------------------------+
   |  L2. Infrastructure as Code (IaC) & Provisioning          |
   |  - Terraform, AWS CloudFormation, Pulumi, Crossplane      |
   |  - Immutable AMI / Container Image (Docker, OCI)          |
   |  - GitOps: ArgoCD, Flux                                    |
   +----------------------------------------------------------+
   |  L1. Cloud Provider Foundation (CSP 자원 계층)             |
   |  - Compute(EC2, Lambda), Storage(S3, EBS), Network(VPC)  |
   |  - Region / AZ(가용영역) / Edge Location / PoP            |
   |  - IaaS / PaaS / SaaS / FaaS / CaaS 노출 모델            |
   +----------------------------------------------------------+
                       |
                       v
   +----------------------------------------------------------+
   |   횡단 관심사(Cross-Cutting Concerns)                      |
   |   - Observability(Prometheus+Grafana+Loki+OTel/Tempo)   |
   |   - Security(Zero Trust, KMS, IAM, CSPM, WAF)            |
   |   - FinOps(비용 최적화, Reserved/ Savings Plan)            |
   |   - Compliance(SOC2, ISO27001, PCI-DSS, GDPR-PIPL)       |
   +----------------------------------------------------------+
```

### NIST 클라우드 컴퓨팅 참조 모델(SP 500-292) — 5대 특성 + 3개 서비스/4개 배포 모델

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **5대 필수 특성 (Essential Characteristics)** | 클라우드 정의를 위한 최소 충족 조건 | ① On-demand Self-Service, ② Broad Network Access, ③ Resource Pooling(멀티테넌시), ④ Rapid Elasticity, ⑤ Measured Service(미터링/과금) |
| **3대 서비스 모델 (Service Models)** | 책임 분담 경계(Responsibility Boundary) 정의 | **IaaS**(VM, Network, Storage - OS 이상은 사용자 책임), **PaaS**(런타임/미들웨어/DB 관리형 - 코드만 사용자), **SaaS**(완전 관리형 - 설정/데이터만 사용자), 추가로 **FaaS**(Lambda, Cloud Functions - 이벤트당 실행), **CaaS**(컨테이너 오케스트레이션형) |
| **4대 배포 모델 (Deployment Models)** | 클라우드 위치/거버넌스 결정 | **Public**(AWS/Azure/GCP, 다중 테넌트), **Private**(OpenStack, VMware Cloud on AWS), **Hybrid**(Outposts/Azure Arc/Anthos로 온프레 연결), **Community**(특정 조직군 공동 사용, 의료/정부 컨소시엄) |
| **참조 아키텍처(RA Ver.2)** | 5개 역할(Consumer/Provider/Broker/Carrier/Auditor) | BCC(Business Support), CCC(Cloud Cube: 5축 - 위치/소유/경계/거버넌스/충실도), CCCM(Cloud Consumer/Provider) |
| **12-Factor App** | 클라우드 네이티브 앱 설계 원칙 | ① Codebase, ② Dependencies, ③ Config, ④ Backing Services, ⑤ Build/Release/Run 분리, ⑥ Stateless Process, ⑦ Port Binding, ⑧ Concurrency, ⑨ Disposability(빠른 기동/종료), ⑩ Dev/Prod Parity, ⑪ Logs(Event Stream), ⑫ Admin Processes(1회성 작업도 코드화) |
| **Kubernetes 기본 단위(Pod/Deployment/Service)** | 컨테이너 오케스트레이션 핵심 | Pod(1개 이상 컨테이너, 공유 네트워크/스토리지), Deployment(롤링 업데이트, ReplicaSet 관리), Service(ClusterIP/NodePort/LoadBalancer), Ingress(L7 라우팅), HPA(Horizontal Pod Autoscaler - CPU/Mem/Custom Metric), PDB(PodDisruptionBudget) |

### CAP 정리와 분산 트레이드오프 (기술사 빈출)

```
      Consistency (강일관성)
              ^
              |        ✕ CP (e.g., etcd, HBase, Redis)
              |      ╱
              |    ╱
              |  ╱
              |╱
   -------------------------> Availability (가용성)
              |╲
              |  ╲
              |    ╲
              |      ╲
              |        ✕ AP (e.g., DynamoDB, Cassandra, CosmosDB)
              v
      Partition Tolerance (분할 내성)
   ※ 분산 시스템에서 P는 필수 -> 실제 선택지는 C vs A
```

- **CP 선택 시**: 금융 코어(원장, 결제), Zookeeper/etcd 합의 알고리즘
- **AP 선택 시**: 카탈로그, 장바구니, 소셜 피드(읽기 일관성보다 응답성 우선)
- **BASE**(Basically Available, Soft state, Eventually consistent) vs **ACID**(원자성/일관성/격리성/지속성)

### 무중단 배포 전략 (Zero-Downtime Deployment)

| 전략 | 동작 | 트래픽 전환 | 롤백 시간 | 적용 시나리오 |
| :--- | :--- | :--- | :--- | :--- |
| **Rolling Update** | k8s 기본, 점진적 Pod 교체 | 순차 교체 | 분 단위 | 일반 MSA |
| **Blue-Green** | 동일 환경 2세트, 스위치 | DNS/LB 일시 전환 | 초 단위 | DB 호환 중요 |
| **Canary** | 5~10% 트래픽 -> 점진 확대 | 가중치 라우팅 | 즉시 중단 가능 | 신규 기능 검증 |
| **A/B Testing** | 기능 플래그(Feature Flag) | 사용자 속성별 분기 | 즉시 | 실험/UX 검증 |
| **Recreate** | 전체 종료 후 신규 배포 | 다운타임 발생 | N/A | 비운영/배치 |

- **📢 섹션 요약 비유**: 클라우드 4계층은 **만들어진 떡케익**(시트-크림-토핑-장식 각 층이 독립)이고, CAP 정리는 **비 오는 날 우산 vs 우비**(둘 다 챙길 수 없으니 어느 하나 포기) 선택이다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 서비스 모델별 책임 분담 (Shared Responsibility Model)

| 구분 | On-Premise | IaaS (EC2) | PaaS (RDS/Beanstalk) | SaaS (Salesforce/Workday) | FaaS (Lambda) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **데이터** | 사용자 | 사용자 | 사용자 | 사용자 | 사용자 |
| **애플리케이션 코드** | 사용자 | 사용자 | 사용자 | CSP | 사용자 |
| **런타임/미들웨어** | 사용자 | 사용자 | CSP | CSP | CSP |
| **OS** | 사용자 | 사용자 | CSP | CSP | CSP |
| **가상화/하이퍼바이저** | 사용자 | CSP | CSP | CSP | CSP |
| **물리 서버/스토리지/네트워크** | 사용자 | CSP | CSP | CSP | CSP |
| **물리 데이터센터 보안** | 사용자 | CSP | CSP | CSP | CSP |
| **제어 수준(Control Level)** | ★★★★★ | ★★★★ | ★★★ | ★ | ★★ (이벤트 단위) |
| **운영 부담(Operational Overhead)** | 최대 | 높음 | 중간 | 최소 | 최소(0과 1사이) |

### 비교 2: 배포 모델별 트레이드오프

| 구분 | Public Cloud | Private Cloud | Hybrid Cloud | Multi-Cloud |
| :--- | :--- | :--- | :--- | :--- |
| **확장성** | 무제한(Elastic) | 제한적(자체 CapEx) | 하이브리드 | 클라우드별 가용 |
| **초기 비용(TCO)** | 낮음(OpEx) | 높음(CapEx) | 중간 | 중간~높음 |
| **컴플라이언스** | 일반적 양호 | 높음(완전 통제) | 데이터 분류별 | CSP별 상이 |
| **벤더 락인** | 높음 | 없음(OpenStack) | 부분적 | 낮음(추상화 필요) |
| **네트워크 지연** | 리전별 차이(수 ms) | 매우 낮음(로컬) | Interconnect 필요 | 클라우드 간 |
| **DR(재해복구)** | 리전 간 자동 | 자체 DR 사이트 | 클라우드+온프레 | 클라우드 간 |
| **적합 워크로드** | 웹/배치/오버플로우 | 코어/규제/PII | 단계적 전환 | 최고 가용성/이주성 |

### 비교 3: 마이그레이션 전략 6R (AWS 공식 분류)

| 구분 | Rehost (Lift & Shift) | Replatform (Lift & Reshape) | Refactor (Re-architect) | Repurchase (Drop & Shop) | Retire | Retain |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **변경 정도** | 그대로 이동 | 경미 최적화 | 클라우드 네이티브 재설계 | SaaS 교체 | 폐기 | 현상태 유지 |
| **소요 시간** | 2~6주 | 2~3개월 | 6~18개월 | 1~3개월 | 즉시 | 무기한 |
| **비용 절감**
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 619 / 800

<- **이전**: [618. 클라우드 아키텍처 핵심 토픽 618번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/618_cloud_architecture_core_topic_618_exam_summar/)
**다음**: [620. 클라우드 아키텍처 핵심 토픽 620번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/620_cloud_architecture_core_topic_620_exam_summar/) ->

---
