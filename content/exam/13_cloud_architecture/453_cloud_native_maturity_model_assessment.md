---
title: "Cloud Native Maturity Model Assessment"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 네이티브 성숙도 모델(CNMM)은 조직의 클라우드 전환을 **5단계(Level 1~5)** 와 **7개 차원**(Infrastructure, Application Architecture, DevOps/CI-CD, Observability, Security, Data, Organization)으로 정량·정성 평가하여 현 위치(As-Is)와 목표 위치(To-Be)의 갭을 정밀 측정하는 진단 프레임워크이다. CNCF, Pivotal, Microsoft CAF, Gartner 등 다수의 벤더별 모델이 존재하며 공통적으로 **12-Factor App** 준수 여부, **Kubernetes** 기반 오케스트레이션, **GitOps** 자동화, **eBPF 기반 Observability** 도입 수준을 핵심 지표로 사용한다.
> 2. **가치**: 성숙도 1단계(Ad-hoc)에서 5단계(Optimizing)로 전환 시 **배포 빈도(Deployment Frequency)는 월 1회에서 일 수십 회(+1,200%)**, **변경 실패율(Change Failure Rate)은 50%에서 5~15%(-70~90%)**, **MTTR(Mean Time To Restore)은 수 시간에서 수 분(-90%)**, **인프라 비용은 FinOps 최적화로 30~45% 절감**하는 정량적 효과를 얻을 수 있다. DORA Report 2023에 따르면 Elite 조직은 Low/Medium 대비 **168배 빠른 배포 주기**를 달성한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① **속도 vs 안정성**(CI/CD 파이프라인 자동화 수준), ② **표준화 vs 자율성**(중앙 Platform Team 제공 셀프서비스 vs 팀별 자유도), ③ **Greenfield vs Brownfield**(신규 시스템은 Level 4~5로 시작, 레거시 시스템은 6R 마이그레이션으로 점진 승격), ④ **기술 부채 vs 혁신 속도**(Microservices 강제 적용 시 "Distributed Monolith" 안티패턴 회피), ⑤ **보안 vs 민첩성**(Zero Trust, Policy-as-Code로 양립)이다. 기술사 시험 관점에서는 **"성숙도 평가 결과에 따른 단계적 로드맵 수립 및 KPI 정량화 역추적"** 능력을 중점 평가한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 패러다임 전환의 시대적 배경

2013년 Pivotal(Matt Stine)에 의해 처음 명명된 "Cloud Native" 개념은 단순한 기술 트렌드를 넘어 **"클라우드 환경에서 최적화된 방식으로 소프트웨어를 구축·운영하는 철학과 방법론의 총체"** 로 자리 잡았다. 2015년 CNCF(Cloud Native Computing Foundation) 설립, 2018년 CNCF가 Kubernetes를 졸업(Graduated) 프로젝트로 지정한 이후 클라우드 네이티브는 컨테이너 오케스트레이션을 중심으로 한 생태계 표준으로 확립되었다.

그러나 **"Cloud First"** 라는 슬로건만으로는 실제 비즈니스 가치를 창출할 수 없다. 많은 기업이 클라우드 마이그레이션을 진행했음에도 ① IaaS 기반 단순 Lift & Shift에 머물러 TCO(Total Cost of Ownership)가 오히려 증가하거나, ② Microservices 도입으로 인해 운영 복잡도가 폭증하는 **"Distributed Monolith"** 함정에 빠지거나, ③ 컨테이너는 도입했으나 **CI/CD·Observability·Security**가 미비하여 안정성 문제로 롤백되는 사례가 빈번하다.

### 1.2 성숙도 평가의 필요성

성숙도 모델이 필요한 기술적 이유는 다음과 같다:

- **객관적 현 위치 측정**: 주관적 판단("우리 회사는 클라우드 잘 써")을 정량 지표로 변환
- **투자 우선순위 결정**: 7개 차원 중 현재 가장 미성숙한 차원을 식별하여 ROI 최대화
- **단계적 로드맵 수립**: 한 번에 Level 5 도달이 불가능하므로 현실적 단계 계획 수립
- **경영진 보고 및 거버넌스**: 기술 지표 -> 비즈니스 KPI(매출, 고객 만족도)로의 번역

```text
[클라우드 네이티브 성숙도 평가의 개념 흐름도]

  +---------------------------------------------------------+
  |         Business Outcomes (매출/TM/혁신 속도)            |
  +----------------------+----------------------------------+
                         ^ (역추적)
  +----------------------+----------------------------------+
  |     Level 5: Optimizing (AIOps, Serverless, FinOps)     |
  |     Level 4: Managed   (Platform Eng, GitOps, eBPF)     |
  |     Level 3: Defined   (K8s, Microservices, CI/CD)      |
  |     Level 2: Repeatable(Virtualization, Basic IaaS)     |
  |     Level 1: Initial   (Bare-metal, Manual Deploy)      |
  +----------------------+----------------------------------+
                         ^ (점진 승격)
  +----------------------+----------------------------------+
  |  Assessment Engine (7개 차원 × 5단계 점수 매트릭스)      |
  |  +-----+-----+-----+-----+-----+-----+-----+           |
  |  |Infra| App |DevOp|Observ| Sec |Data | Org |           |
  |  +-----+-----+-----+-----+-----+-----+-----+           |
  |  | L3  | L2  | L2  | L1  | L2  | L2  | L1  |  <- As-Is  |
  |  | L4  | L4  | L4  | L4  | L4  | L3  | L3  |  <- To-Be  |
  |  +-----+-----+-----+-----+-----+-----+-----+           |
  +----------------------+----------------------------------+
                         ^
  +----------------------+----------------------------------+
  |      Data Collection (CDE, APM, IaC, Git, K8s API)       |
  +---------------------------------------------------------+
```

### 1.3 레거시 vs 클라우드 네이티브 패러다임 비교

| 패러다임 | 레거시(On-Premise) | 클라우드 네이티브 |
|:---|:---|:---|
| **인프라** | Bare-metal, 수동 프로비저닝, Capacity Planning 기반 | 컨테이너, 선언적 API, Auto-scaling |
| **애플리케이션** | Monolith, 야간 배포, Waterfall | Microservices, 지속적 배포, Agile |
| **운영** | Reactive(장애 후 대응), Silo 조직 | Proactive(관측성 기반), SRE/DevOps |
| **비용 모델** | CAPEX(선투자), 3~5년 감가상각 | OPEX(사용량 기반), Pay-per-Use |
| **변경 주기** | 분기 1회, Change Advisory Board | 일 수십 회, Progressive Delivery |
| **장애 허용** | HA(High Availability) 이중화 | Resilience(Chaos Engineering, Circuit Breaker) |

- **📢 섹션 요약 비유**: 성숙도 평가는 마치 **"자동차 정비소의 종합 진단기"** 와 같습니다. 단순히 "차 안에서 소리가 난다"는 증상만 보는 게 아니라, 엔진·브레이크·배터리·타이어 압력 등 7개 부위를 정밀 측정해 **"현재 70점, 목표 90점, 부족한 부위는 타이어 공기압"** 처럼 명확한 처방전을 만들어 주는 것과 같은 원리입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 7개 평가 차원의 구조

클라우드 네이티브 성숙도 평가는 **7개 핵심 차원(Dimension)** 을 독립적으로 측정하되, 차원 간 **의존성 그래프(Dependency Graph)** 를 고려해야 한다. 예를 들어, Microservices(Level 4) 채택은 Service Mesh·Observability·CI/CD가 먼저 성숙되어야 가능하다.

```text
[7개 차원의 의존성 및 아키텍처]

                    +----------------------+
                    |   Organization(조직) |  <- DevOps Culture, SRE, Platform Team
                    |      [L1~L5]        |
                    +----------+-----------+
                               | (문화/스킬)
        +----------------------+----------------------+
        v                      v                      v
+--------------+    +------------------+    +------------------+
| Infrastructure|    |Application Arch  |    |   DevOps/CI-CD   |
|   [L1~L5]    |◄--►|     [L1~L5]      |◄--►|     [L1~L5]      |
| VM->Container |    | Monolith->MSA     |    | Manual->GitOps    |
| ->Serverless  |    | ->Event-driven    |    |                  |
+------+-------+    +--------+---------+    +--------+---------+
       |                     |                       |
       |            +--------+---------+             |
       +-----------►|   Observability  |◄------------+
                    |     [L1~L5]      |
                    | Log->Metric+Trace |
                    | ->AIOps(eBPF)     |
                    +--------+---------+
                             |
              +--------------+--------------+
              v              v              v
       +-------------+ +----------+ +-------------+
       |  Security   | |   Data   | |  FinOps     |
       |  [L1~L5]    | | [L1~L5]  | |  [L1~L5]    |
       | Perimeter->  | | RDB->     | | CapEx->      |
       | Zero Trust  | | Polyglot | | Showback->   |
       | ->Confident. | | ->Mesh    | | Chargeback  |
       +-------------+ +----------+ +-------------+
```

### 2.2 5단계 성숙도 레벨의 정의

| 레벨 | 명칭 | 인프라 | 애플리케이션 | DevOps | 관측성 | 보안 | 데이터 | 조직 |
|:---:|:---|:---|:---|:---|:---|:---|:---|:---|
| **L1** | **Initial** | 물리 서버, 수동 설치 | Monolith, 야간 배포 | 수동 스크립트, FTP 배포 | 로그 파일, `grep` | 방화벽, ID/PW | RDBMS 단일 | 기능별 Silo, ITOps |
| **L2** | **Repeatable** | VM, IaaS(CAPEX) | 모놀리식 + 일부 분리, 주간 배포 | Jenkins, Basic CI | SNMP, 단순 알람 | VPN, ACL | RDBMS+캐시, Read Replica | Dev/Ops 분리, SLA 정의 |
| **L3** | **Defined** | 컨테이너(Docker), K8s 도입, IaC(Terraform) | Microservices, API Gateway, 일 배포 | GitOps(ArgoCD/Flux), Blue-Green/Canary | Metrics+Logs+Traces(3-Pillars), Prometheus/Grafana | mTLS, RBAC, Secrets Management | Polyglot(DB 다변화), Kafka | DevOps 팀, 공유 온콜 |
| **L4** | **Managed** | Multi-Cluster K8s, Service Mesh(Istio/Linkerd), Cluster API | Event-driven(EDA), CQRS/Saga, 수시 배포 | Progressive Delivery(Flagger), 정책 기반 자동화 | OpenTelemetry, AIOps, SLI/SLO 자동 측정 | Zero Trust, Policy-as-Code(OPA/Kyverno) | Data Lakehouse(Iceberg/Delta), Streaming(CDC) | Platform Engineering, IDP |
| **L5** | **Optimizing** | Serverless(Knative), Wasm, Spot/Preemptible 최적화 | Cell-based Architecture, Autonomous Systems | AIOps 자가 치유, Chaos Engineering常态化 | PagerDuty ML, 자동 Root Cause Analysis | Confidential Computing(SEV/TDX), Post-Quantum | Data Mesh, Federated Learning | BizDevOps, Product-oriented Team |

### 2.3 핵심 구성 요소 및 평가 메커니즘

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 453 / 800

<- **이전**: [452. 클라우드 네이티브 12팩터 앱 설계](/studynote/13_cloud_architecture/06_exam_summary/452_cloud_native_12_factor_app_design/)
**다음**: [454. CNCF 프로젝트 생태계 기술 지형도](/studynote/13_cloud_architecture/06_exam_summary/454_cncf_project_ecosystem_technology_landscape/) ->

---
