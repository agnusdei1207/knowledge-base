---
title: "441. 클라우드 마이그레이션 6R 전략 방법론 (Cloud Migration 6R Strategy Methodology)"
date: "2026-05-09"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: AWS가 2016년 정립한 6R(Rehost, Replatform, Repurchase, Refactor, Retire, Retain) 전략은 워크로드의 **기술적 특성(State coupling, 6R 결정 매트릭스)**, **TCO(3년/5년)**, **비즈니스 임팩트(TTM, RTO/RPO)**의 3축으로 분류한 클라우드 마이그레이션 의사결정 프레임워크임.
> 2. **가치**: AWS Migration Acceleration Program(MAP) 적용 시 평균 **TCO 31% 절감, 마이그레이션 속도 3배 향상, 운영 비용(OPEX) 20~50% 감소** 효과가 검증되었으며, Rehost 60% + Replatform 25% + Refactor 15% 비율이 일반적인 최적 포트폴리오임.
> 3. **판단 포인트**: 핵심은 **"Cloud Economics(클라우드 경제성)"** 관점에서 "Lift & Reshape(일단 옮기고 점진적 최적화)" 원칙이며, Big-Bang 마이그레이션 회피, 6R 결정 시 **Application Dependency Mapping(ADM)** 기반의 **Wave Planning**, 그리고 **FinOps** 통합이 기술사적 판단의 핵심임.

---

## Ⅰ. 개요 및 필요성

클라우드 마이그레이션은 단순한 서버 이전이 아닌, **엔터프라이즈 아키텍처(EA)**의 패러다임 전환을 의미함. 2003년 Gartner의 "Five Rs"에서 출발하여 2016년 AWS의 Steve Riley가 6R로 체계화한 이 방법론은, 클라우드 도입 시 **"모든 워크로드를 동일하게 마이그레이션한다"**는 잘못된 접근을 교정하기 위해 등장함.

전통적 온프레미스 환경은 **CapEx(자본 지출)**, **수직적 확장(Scale-Up)**, **Long Lead Time(주문 후 수개월)**의 특성을 가지며, 2019년 Gartner 발표에 따르면 평균 **데이터센터 운영 비용의 60%가 "유지보수 및 유휴 자원"**에 소진됨. 반면 클라우드는 **Pay-as-you-go**, **수평적 확장(Scale-Out)**, **셀프서비스 프로비저닝**을 통해 **Time-to-Market(TTM)을 평균 60~70% 단축**시킴.

COVID-19 이후 원격근무, 전자상거래, 실시간 데이터 분석 수요가 폭증하면서, **IDC 보고서(2023)**에 따르면 전 세계 기업의 **73%가 이미 하이브리드/멀티 클라우드 환경**을 운영 중이며, 이는 6R 전략의 보편적 적용 필요성을 입증함.

```text
+--------------------------------------------------------------------+
|            클라우드 마이그레이션 6R 전략 - 전체 의사결정 흐름       |
+--------------------------------------------------------------------+

    +--------------+
    |  Legacy DC   |  <- 온프레미스: 600+ 서버, 200+ 애플리케이션
    |  (CapEx 60%) |     CapEx 중심, 3~5년 갱신 주기, License Lock-in
    +------+-------+
           | [1단계: Discovery & Assessment]
           v
    +--------------------------------------+
    |  AWS Migration Hub / Application    |
    |  Discovery Service / TSO Logic       |
    |  -> 워크로드 인벤토리(서버, DB, App)   |
    |  -> Dependency Map (네트워크/데이터)   |
    |  -> 6R Decision Matrix 생성           |
    +------+-------------------------------+
           | [2단계: 6R 전략 결정 (Portfolios)]
           v
   +-------+-------+----------+----------+--------+--------+
   |Rehost |Replat-|Repurchase| Refactor | Retire | Retain |
   |(lift) | form  |(drop&shop)|(re-arch) |        |        |
   |  60%  |  20%  |   10%    |   7%     |   2%   |   1%   |
   +---+---+---+---+----+-----+----+-----+---+----+---+----+
       |       |        |          |         |        |
       v       v        v          v         v        v
   +------------------------------------------------------+
   |  AWS Cloud (Region: ap-northeast-2 / 다중 AZ)       |
   |  +--------+ +--------+ +----------+ +------------+ |
   |  |  EC2   | |  RDS   | | SaaS(Git)| | Lambda/ECS | |
   |  +--------+ +--------+ +----------+ +------------+ |
   |  + CloudWatch, IAM, VPC, Transit Gateway            |
   +------------------------------------------------------+
           |
           v
    +----------------------+
    |  Modernization Layer |  <- MSA, Serverless, AI/ML
    |  (점진적 Refactor)   |     FinOps, Well-Architected Review
    +----------------------+
```

**On-Premise vs Cloud Paradigm 비교**:

| 구분 | On-Premise (Legacy) | Cloud (6R 적용) |
|:---|:---|:---|
| 비용 모델 | CapEx (3~5년 선투자) | OpEx (Pay-per-use) |
| 확장성 | 수직적 (Scale-Up, 한계 명확) | 수평적 (Auto Scaling, 무제한) |
| 프로비저닝 | 수주~수개월 (HW 발주) | 수분~수초 (API 호출) |
| 가용성 | 99.5% (단일 장애점) | 99.99% (Multi-AZ/Region) |
| 장애 복구 | DR 사이트 별도 구축 (RTO 24h+) | Pilot Light / Warm Standby (RTO 분 단위) |

- **📢 섹션 요약 비유**: 클라우드 마이그레이션은 마치 **"오래된 식당(온프레미스)"**을 새로 짓는 것이 아니라, **"배달의민족(클라우드)"** 플랫폼으로 이전하는 것과 같음. 모든 메뉴를 한 번에 바꾸는 것(Refactor)이 아니라, 배달이 잘 되는 인기 메뉴부터 옮기고(Rehost), 조리도구를 업그레이드(Replatform)하며, 안 팔리는 메뉴는 정리(Retire)하는 전략이 필요함.

---

## Ⅱ. 아키텍처 및 핵심 원리

6R 전략의 핵심은 **"워크로드별 최적 경로"**를 찾는 것이며, AWS Well-Architected Framework의 5대 원칙(운영 우수성, 보안, 안정성, 성능 효율, 비용 최적화)에 따라 각 전략의 기술적 깊이가 결정됨.

```text
+--------------------------------------------------------------+
|              6R 전략별 기술 아키텍처 상세 매핑                 |
+--------------------------------------------------------------+

  [1] Rehost (Lift & Shift) ----------------------- 60%
  +----------+    +------------------+    +--------------+
  | Source   |    | AWS Application  |    |    EC2       |
  | VMware/  |---->| Migration Service|---->| (m5/c5/r5)   |
  | Hyper-V  |    | (CloudEndure)    |    | AMI 변환     |
  +----------+    | Continuous Repl. |    +--------------+
                  | RPO < 1분        |
                  +------------------+
                  AWS Server Migration Service (SMS) -> EC2
                  AWS Database Migration Service (DMS) -> RDS

  [2] Replatform --------------------------------- 20%
  +----------+    +------------------+    +--------------+
  | Oracle   |    | Schema Convert.  |    |  Aurora      |
  | EE 11g   |---->| + DMS CDC       |---->| (MySQL/PG)   |
  +----------+    +------------------+    +--------------+
                  +- OS: Windows->Linux (40% 절감)
                  +- Container: ECS/EKS
                  +- DB: Self-managed -> RDS Multi-AZ
                  +- Cache: Redis -> ElastiCache

  [3] Repurchase (Drop & Shop) ------------------- 10%
  +----------+    +------------------+    +--------------+
  | Custom   |    | License 종료 +   |    |   SaaS       |
  | CRM      |---->| 데이터 마이그레이션|---->| (Salesforce) |
  +----------+    +------------------+    +--------------+
                  +- Email 서버 -> SES / WorkMail
                  +- Jenkins -> GitHub Actions / CodePipeline
                  +- SharePoint -> SharePoint Online
                  +- ERP -> SaaS ERP (예: SAP S/4HANA Cloud)

  [4] Refactor / Re-architect ------------------- 7%
  +----------+    +------------------+    +--------------+
  | Monolith |    | Strangler Fig    |    |  Microsvc.   |
  | (Java EE)|---->| Pattern + API GW|---->|  + Lambda    |
  +----------+    +------------------+    +--------------+
                  +- Lambda + API Gateway + DynamoDB
                  +- Step Functions (Orchestration)
                  +- EventBridge (Event-Driven)
                  +- S3 + Athena (Data Lake)

  [5] Retire ----------------------------------- 2%
  - 사용되지 않는 워크로드 제거
  - 라이선스 비용 절감
  - 보안 공격면(Attack Surface) 축소

  [6] Retain ----------------------------------- 1%
  - 규정 준수 (금융, 의료 데이터 주권)
  - 기술 부채가 매우 큰 Legacy (예: AS/400)
  - 최근 투자한 HW (감가상각 미종료)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **AWS Migration Hub** | 마이그레이션 오케스트레이션 | 11개 AWS/3rd Party 도구(CloudEndure, RiverMeadow, TSO Logic) 통합 대시보드, 진행 상태 추적, **Migration Strategy Recommendations (ML 기반)** 제공 |
| **Application Discovery Service** | 워크로드 자동 식별 | Agentless(VMware vCenter API)/Agent 방식, **OS, CPU, Memory, Network, Process Inventory** 자동 수집, **30일 무료 사용**으로 TCO 분석 |
| **AWS Application Migration Service (CloudEndure 기반)** | Rehost 자동화 | **블록 수준 Continuous Replication**, RPO < 1분, RTO 분 단위, 무차별 복제(Bare-Metal, VMware, Hyper-V) -> EC2 자동 변환 |
| **AWS Database Migration Service (DMS)** | DB 이관 | **Homogeneous(Oracle->Oracle) / Heterogeneous(Oracle->Aurora)** 모두 지원, **CDC(Change Data Capture)** 기반 무중단 마이그레이션, **SCT(Schema Conversion Tool)**로 90% 자동 변환 |
| **AWS Well-Architected Tool** | 아키텍처 검증 | 5대 영역 60+ 질문 기반 자동 평가, **Lenses(SAP, Serverless, ML, Financial Services)** 적용, 개선 항목(High/Medium Risk) 시각화 |
| **AWS Migration Acceleration Program (MAP)** | 비즈니스 지원 | **3-Tier 구조(Assess -> Mobilize -> Migrate & Modernize)**, AWS 전문가 컨설팅 + 서비스 크레딧(평균 $300K), **Wave별 비용 보전** 모델 |
| **Cloud Economics** | TCO 산정 | **3년/5년 TCO 모델**, 서버당 $10K/yr 절감 목표(전형적), **FinOps Foundation** 가이드라인, **CUDOS(Cloud Unit Economics Dashboard)** |

**6R 결정 매트릭스의 핵심 파라미터**:

1. **비즈니스 임팩트 점수(BIS)** = (TTM 가중치 × 0.4) + (ROI 가중치 × 0.3) + (위험도 가중치 × 0.3)
2. **기술적 복잡도(TC)**: 결합도(Coupling) / 응집도(Cohesion) / 기술 부채(Technical Debt)
3. **TCO 공식**: `TCO = CapEx(전환) + OpEx × N년 + 라이선스 + 인력(역량) - 절감(OpEx 절감, 라이선스 절감)`

**핵심 알고리즘**: 6R 결정 시 AWS는 **"8가지 일반적 Anti-Pattern"**을 사전 점검하도록 권고함 (예: Refactor 욕심, 무계획 Rehost, 단일 클라우드 종속 등).

- **📢 섹션 요약 비유**: 6R 전략은 마치 **"이사 짐 분류"**와 같음. **Rehost**는 박스째 옮기기(빠르지만 무거움), **Replatform**은 짐을 새로운 서랍장(RDS)에 알맞게 정리, **Repurchase**는 가구를 새로 사기(SaaS), **Refactor**는 방을 완전히 리모델링, **Retire**는 버리기, **Retain**은 아직 쓸 수 있는 물건은 기존 위치에 두는 것.

---

## Ⅲ. 비교 및 연결

| 구분 | **AWS 6R (2016)** | **Gartner 5R (2016)** | **Azure 5R (Microsoft)** | **Google 4R (GCP)** |
|:---|:---|:---|:---|:---|
| 전략 수 | 6개 (Rehost, Replatform, Repurchase, Refactor, Retire, Retain) | 5개 (Rehost, Relocate, Refactor, Replace, Retire) | 5개 (Rehost, Refactor, Rearchitect, Rebuild, Replace) | 4개 (Repurchase, Replatform, Refactor, Retain) |
| Replatform | ✅ 독립 전략 | ❌ Rehost에 포함 | ❌ Refactor에 포함 | ✅ 독립 전략 |
| Repurchase | ✅ SaaS 전환 강조 | ✅ "Replace" | ✅ "Replace" | ✅ "Repurchase" |
| Retire | ✅ 명시 | ✅ 명시 | ❌ 암묵적 | ❌ 명시 없음 |
| Retain | ✅ 명시 | ❌ 없음 | ❌ 없음 | ✅ 명시
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 441 / 800

<- **이전**: [440. 클라우드 로드밸런서 ALB NLB GLB](/studynote/13_cloud_architecture/06_exam_summary/440_cloud_load_balancer_alb_nlb_glb/)
**다음**: [442. 리호스트 리프트 앤 시프트 마이그레이션](/studynote/13_cloud_architecture/06_exam_summary/442_rehost_lift_and_shift_migration/) ->

---
