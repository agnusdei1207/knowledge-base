---
title: "671. 클라우드 아키텍처 핵심 토픽 671번 시험 요약 (Cloud Architecture Core Topic 671 Exam Summary)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 아키텍처는 NIST SP 800-145의 5대 필수 특성(온디맨드 셀프서비스·광범위한 네트워크 접근·자원 풀링·빠른 탄력성·측정 가능 서비스)과 4종 배치 모델(Public/Private/Hybrid/Community), 3계층 서비스 모델(IaaS/PaaS/SaaS)을 결합하여, 가상화·컨테이너·오케스트레이션·서버리스·서비스 메시로 대표되는 클라우드 네이티브 기술 스택을 통해 자원을 추상화·자동화·분산 처리하는 컴퓨팅 패러다임이다.
> 2. **가치**: CAPEX를 OPEX로 전환하여 3년 TCO 기준 약 30~65% 절감, Auto Scaling·Multi-AZ 배포를 통해 가용성 99.99% SLA와 글로벌 평균 응답 지연 100ms 이하 달성, Well-Architected 5대 기둥(운영 우수성·보안·안정성·성능 효율·비용 최적화) 기반의 지속적 개선 사이클을 통한 MTTR 50% 단축 효과가 검증되어 있다.
> 3. **판단 포인트**: 워크로드의 상태 유지 특성·콜드 스타트 허용치·트래픽 패턴(정적/버스티/예측불가)에 따라 VM·컨테이너·서버리스(FaaS)를 합리적으로 선택하고, CAP 정리 트레이드오프 하에서 일관성 vs 가용성 중 무엇을 우선할지 결정하며, Shared Responsibility Model 경계 설정, Vendor Lock-in 회피(추상화 레이어·Terraform IaC·Open API)와 운영 복잡성 간 균형, FinOps 기반 비용 가시성 확보가 핵심 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 환경은 2006년 AWS S3·EC2 출시 이후 20여 년간 **Mainframe → x86 Server 가상화 → 클라우드 IaaS → 컨테이너 오케스트레이션 → 서버리스/엣지 컴퓨팅**으로 급격히 진화했다. 기존 온프레미스 환경은 **프로비저닝 리드타임(주 단위)**, **피크 트래픽 기반의 과잉 용량 설계(평균 활용률 15~25%)**, **수동 패치/장애 대응(MTTR 평균 4시간 이상)**, **CAPEX 중심의 투자 회수 불확실성**이라는 4대 구조적 한계를 내포하고 있었다.

클라우드 아키텍처는 이러한 한계를 **API 기반 선언적 프로비저닝**, **Horizontal Auto Scaling**, **Immutable Infrastructure**, **Pay-per-use 과금 모델**로 근본적으로 해결한다. 특히 12-Factor App 방법론(2011, Heroku)과 CNCF(Cloud Native Computing Foundation)의 성숙으로 stateless 프로세스·설정 외부화·CI/CD 일관성·Disposable 백엔드 원칙이 표준화되었으며, Kubernetes 1.0(2015) 출시 이후 컨테이너 오케스트레이션이 클라우드 네이티브的事实上의 표준(de facto standard)으로 자리 잡았다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                  전통 온프레미스 vs 클라우드 네이티브 아키텍처         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [On-Premise: 수직 확장·수동 운영]                                     │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐                     │
│  │ Web Tier │────▶│ App Tier │────▶│ DB Tier  │   ← 강결합(Monolith)  │
│  │  (Nginx) │     │ (WAS)    │     │ (Oracle) │   ← 수동 장애 대응    │
│  └────┬─────┘     └────┬─────┘     └────┬─────┘   ← 피크 기반 과설계 │
│       │                │                │                            │
│       ▼                ▼                ▼                            │
│  ┌─────────────────────────────────────────────────┐                │
│  │   전용 하드웨어 (Dell PowerEdge, HP ProLiant)     │                │
│  │   활용률 15~25% / 수동 패치 / 주 단위 프로비저닝   │                │
│  └─────────────────────────────────────────────────┘                │
│                                                                      │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│                                                                      │
│  [Cloud-Native: 수평 확장·자동화·관측가능]                             │
│       ┌──────────────────────────────────────────┐                  │
│       │   Edge / CDN (CloudFront, Cloudflare)    │ ← 글로벌 캐시     │
│       └──────────────────┬───────────────────────┘                  │
│                          ▼                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │  API Gateway │─▶│  ALB/NLB     │─▶│  Service A   │ ← 마이크로서비스│
│  │  (Kong,AGW)  │  │  Layer-7 LB  │  │  (Pod x N)   │   독립 배포·확장│
│  └──────────────┘  └──────┬───────┘  └──────────────┘               │
│                           │           ┌──────────────┐               │
│                           ├──────────▶│  Service B   │               │
│                           │           │  (Pod x N)   │               │
│  ┌────────────────────────┴───────────┴──────────────┐               │
│  │  Service Mesh (Istio/Linkerd) - mTLS, Canary, RBAC│               │
│  └────────────────────────┬───────────────────────────┘               │
│                           ▼                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │ RDS Aurora   │  │ DynamoDB     │  │ S3 / ElastiC │ ← Managed Service│
│  │ Multi-AZ     │  │ Global Table │  │ Redis        │   자동 백업·HA  │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                           ▲                                           │
│  ┌────────────────────────┴───────────────────────────┐               │
│  │  EKS / ECS Fargate / Lambda - 선언적 오케스트레이션│               │
│  └────────────────────────────────────────────────────┘               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

클라우드 도입의 핵심 동인은 ① **비즈니스 민첩성** (Time-to-Market 단축), ② **글로벌 확장성** (리전 간 부하 분산), ③ **재해 복구 자동화** (Cross-Region DR), ④ **데이터 기반 의사결정** (S3 Data Lake + Athena/Redshift Spectrum), ⑤ **AI/ML 서비스 즉시 활용** (Bedrock, SageMaker, Vertex AI)이다. Gartner 2024 보고서에 따르면 글로벌 클라우드 시장 규모는 약 6,790억 USD이며, 한국 공공·금융·제조 전 부문으로 확산 중이다.

- **📢 섹션 요약 비유**: 클라우드 아키텍처는 **"전기를 자체 발전소(온프레미스)에서 생산하지 않고 한전(공급자)에서 필요할 때만 kWh당 요금을 내며 쓰는 모델"**이다. 발전기 구매·유지보수·연료 걱정 없이 콘센트만 꽂으면 되며, 에어컨을 더 돌리면 자동으로 전력량이 늘어나듯 Auto Scaling이 수행된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라우드 아키텍처는 **Global Infrastructure Layer → Foundation Services Layer → Platform Services Layer → Application Services Layer → Observability & Governance Layer**의 5계층 참조 모델(RAM, Reference Architecture Model)로 구성된다. AWS Well-Architected Framework, Azure Architecture Center, Google Cloud Architecture Framework가 사실상 업계 표준이다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│           Cloud Reference Architecture (5-Layer RAM)                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ L5: Observability & Governance                                   │ │
│  │   CloudWatch · X-Ray · CloudTrail · Prometheus · Grafana · OPA   │ │
│  │   FinOps(CloudHealth) · AWS Config · Security Hub                │ │
│  └────────────────────────────┬──────────────────────────────────────┘ │
│                               │ Telemetry / Policy                     │
│  ┌────────────────────────────▼──────────────────────────────────────┐ │
│  │ L4: Application Services                                          │ │
│  │   API Gateway · App Mesh · Step Functions · EventBridge · SQS/SNS │ │
│  │   Cognito · SES · Cognito · Pinpoint                              │ │
│  └────────────────────────────┬──────────────────────────────────────┘ │
│                               │ Event-driven / Sync API               │
│  ┌────────────────────────────▼──────────────────────────────────────┐ │
│  │ L3: Platform & Data Services                                      │ │
│  │   EKS · ECS · Lambda · Fargate · Beanstalk · RDS · Aurora        │ │
│  │   DynamoDB · ElastiCache · Redshift · S3 · Athena · EMR · Glue   │ │
│  └────────────────────────────┬──────────────────────────────────────┘ │
│                               │ Managed Runtime                        │
│  ┌────────────────────────────▼──────────────────────────────────────┐ │
│  │ L2: Foundation Compute · Storage · Network                        │ │
│  │   EC2 · EBS · EFS · FSx · VPC · Subnet · RTB · NACL · SG · NAT    │ │
│  │   Direct Connect · Transit Gateway · ELB · NLB · ALB              │ │
│  └────────────────────────────┬──────────────────────────────────────┘ │
│                               │ IaaS API                               │
│  ┌────────────────────────────▼──────────────────────────────────────┐ │
│  │ L1: Global Infrastructure                                         │ │
│  │   Regions (30+) · Availability Zones (3+) · Edge Locations (400+) │ │
│  │   Wavelength (5G MEC) · Local Zones · Outposts (On-Prem)          │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **L1 글로벌 인프라** | 물리적 데이터센터의 지리적 분산 | Region(지리, 30+개) → AZ(독립 전원·네트워크, AZ당 1개 이상 DC, AZ 간 100km 이내 1ms RTT) → Edge Location(PoP 400+개, CDN 캐싱) → Wavelength(5G MEC, 10ms 이하 지연) → Outposts(고객 온프레미스 랙) → Local Zones(대도시 근접, 5~15ms) |
| **L2 네트워크·컴퓨트·스토리지** | IaaS 가상 자원 풀 | VPC(10.0.0.0/16, RFC 1918) → Subnet(Public/Private/TGW Attach, /24 권장) → Route Table(0.0.0.0/0 → IGW/NAT GW) → Security Group(Stateful, Instance-Level, 5-tuple) vs NACL(Stateless, Subnet-Level) → EC2 인스턴스 타입(M5/C5/R5/G5/Inf1, vCPU·메모리·네트워크 대역폭 매트릭스) → EBS(gp3: 3,000 IOPS baseline, 125 MiB/s, io2 Block Express: 256,000 IOPS) → S3(11 9s 내구성, eventual consistency for overwrite) |
| **L3 플랫폼·데이터 서비스** | 관리형 런타임·Managed Database | EKS(Kubernetes 1.29+, CNCF, Control Plane by
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 671 / 800

<- **이전**: [670. 클라우드 아키텍처 핵심 토픽 670번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/670_cloud_architecture_core_topic_670_exam_summar/)
**다음**: [672. 클라우드 아키텍처 핵심 토픽 672번 시험 요약](/studynote/13_cloud_architecture/06_exam_summary/672_cloud_architecture_core_topic_672_exam_summar/) ->

---
