---
title: "IT Management Core Topic 482 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 5개 도메인(EDM/APO/BAI/DSS/MEA) 40개 관리목표(Governance & Management Objectives)를 기반으로, **이해관계자 Needs -> Enterprise Goals -> Alignment Goals -> IT Goals -> Components**의 Cascade 체계를 통해 기업 전략과 IT를 정렬하는 5단계 위계 구조의 의사결정 프레임워크이다.
> 2. **가치**: ITIL 4 34개 Practice와 COBIT 2019의 통합 적용 시, IT 서비스 가용성 99.95% -> 99.99% 향상(연간 다운타임 약 262분 -> 52분 단축), IT 투자 ROI 평균 30~45% 개선, ISO 27001/ISMS-P 인증 획득을 통한 컴플라이언스 비용 약 40% 절감이 검증된 정량 효과이다.
> 3. **판단 포인트**: 조직의 **Maturity Level 1~5** (Initial/Managed/Defined/Quantitatively Managed/Optimizing) 진단 결과에 따라 Process Capability 목표를 설정하되, **Plan/Build/Run(Monitor) 3-Tier 구조**에서 프로세스 자동화율, RACI 매트릭스 명확성, Single Sign-On 통합 여부, 그리고 BSC(Balanced Score Card) 4관점(Financial/Customer/Internal Process/Learning & Growth) 지표 간 인과관계 정의가 핵심 설계 인자이다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 482번 토픽은 **IT 경영 관리**(IT Management) 영역의 종합적 관리 체계를 다루며, 단순한 시스템 운영을 넘어 **전략적 거버넌스**, **위험 관리**, **가치 창출**, **자원 최적화**의 4대 축을 통합 관리하는 체계를 요구한다. 2020년 이후 가속화된 디지털 전환(DX, Digital Transformation), 클라우드 네이티브 전환, 그리고 생성형 AI 도입으로 인해 IT 부서의 역할이 기존 **Cost Center**에서 **Value Driver**로 전환되었으며, ISO 27001:2022, NIST CSF 2.0, 개인정보보호법 개정(2023.9 시행) 등 규제 환경도 급격히 복잡해졌다.

기존의 ITIL v3(2011) 5단계 Lifecycle 모델(Strategy/Design/Transition/Operation/Continual Improvement)은 2019년 ITIL 4의 **Service Value System(SVS)**으로 진화하였고, COSO ERM 2017과 결합된 **통합 위험 관리(Integrated Risk Management)**가 새로운 표준이 되었다.

```text
[기존 IT 관리 패러다임 vs 현대 IT 경영 패러다임 비교]

+-----------------------------+         +---------------------------------+
|  Pre-2020 IT 관리 (Legacy)   |         |  Post-2020 IT 경영 (Modern)      |
+-----------------------------+         +---------------------------------+
|  - CIO가 단독 의사결정        |   ->     | - CxO 협의체 (CISO/CDO/CTO 합동) |
|  - CapEx 중심 HW 투자        |   ->     | - OpEx 중심 Cloud/SaaS 구독     |
|  - ITIL v3 5단계 Lifecycle    |   ->     | - ITIL 4 SVS + Value Stream     |
|  - ISO 27001:2013 통제항목 114개|   ->     | - ISO 27001:2022 93 통제항목    |
|  - 연 1회 정밀감사            |   ->     | - Continuous Audit (AI 기반)    |
|  - SI(Systems Integrator) 의존|   ->     | - In-house DevSecOps + MSP 혼합 |
|  - 모놀리식 ERP (SAP R/3)    |   ->     | - Microservices (Spring Boot/   |
|                               |         |    MSA) + Composable ERP        |
+-----------------------------+         +---------------------------------+
       v                                              v
   운영 효율성만 추구                    비즈니스 가치·리스크·규제·혁신 동시 최적화
   (총 IT 지출 대비 25~35% 가치가치 창출)        (총 IT 지출 대비 50~65% 가치 창출 - Gartner 2023)
```

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **대형 항공모함의 함교(CIC, Combat Information Center)**와 같습니다. 함교는 5,000명 승무원, 70대 항공기, 10척 호위함의 모든 작전을 단일 화면에서 조율하듯, IT 경영은 IT 인프라·인력·예산·위험을 단일 거버넌스 체계로 통합 운영하는 것입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **COBIT 2019의 Governance System**과 **ITIL 4의 Service Value System(SVS)**을 통합한 4계층 구조로 구성된다. 각 계층은 상위 목표를 하위 실행 메커니즘으로 **Cascading**하는 것이 핵심 원리다.

```text
[IT 경영 관리 통합 참조 모델(IRG, Integrated Reference Governance)]

    +-----------------------------------------------------------+
    | Layer 1: Strategic (Strategy & Governance)                 |
    |  +------------------------------------------------------+ |
    |  |  Enterprise Goals (13개, BSC 4관점)                  | |
    |  |  +-> Stakeholder Needs                                | |
    |  |     +-> Enterprise Goals Mapping                      | |
    |  |        +-> Alignment Goals (13개)                     | |
    |  |           +-> IT Goals (13개)                          | |
    |  |              +-> Process Goals (40개 M-O)              | |
    |  +------------------------------------------------------+ |
    +----------------------+------------------------------------+
                           | (Cascade Mapping)
    +----------------------v------------------------------------+
    | Layer 2: Tactical (Management Objectives)                  |
    |  EDM: Evaluate, Direct and Monitor (5개)                  |
    |   +- EDM01 - Governance Framework                         |
    |   +- EDM02 - Benefits Delivery                           |
    |   +- EDM03 - Risk Optimization                            |
    |   +- EDM04 - Resource Optimization                        |
    |   +- EDM05 - Stakeholder Transparency                     |
    |  APO: Align, Plan and Organize (14개)                     |
    |  BAI: Build, Acquire and Implement (11개)                 |
    |  DSS: Deliver, Service and Support (6개)                  |
    |  MEA: Monitor, Evaluate and Assess (4개)                  |
    +----------------------+------------------------------------+
                           |
    +----------------------v------------------------------------+
    | Layer 3: Operational (ITIL 4 Practices)                    |
    |  General Mgmt(14): Strategy, Portfolio, Risk, Finance...  |
    |  Service Mgmt(17): Incident, Problem, Change, SLA...      |
    |  Technical Mgmt(3):  Infra/Platform/Software Dev Mgmt     |
    +----------------------+------------------------------------+
                           |
    +----------------------v------------------------------------+
    | Layer 4: Foundation (Components)                           |
    |  7 Components: Process / Structure / People / Skill/Info   |
    |                / Service/Infrastructure/Application       |
    |  Focus Areas: DevOps, Cybersecurity, Cloud, AI/ML, Privacy |
    |  + 7 Component Variations (Design Factors)                 |
    +-----------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate/Direct/Monitor)** | 거버넌스 의사결정 | 이사회·경영진 단위. RACI 매트릭스에서 **A(Accountable)**을 보유. 의사결정 주기 평균 90일. 주요 도구: Diligent, Boardvantage, 자체 GRC 플랫폼 |
| **APO (Align/Plan/Organize)** | 전략 정렬·계획 | TOGAF 10 ADM(Architecture Development Method) Phase A~H와 연계. 포트폴리오 관리(PPM) 도구: Planview, ServiceNow SPM, Microsoft Project Online |
| **BAI (Build/Acquire/Implement)** | 솔루션 도입·구축 | DevSecOps 파이프라인(SAST/DAST/SCA) 통합, CI/CD 평균 배포 시간(MTTR) 4시간 이내 목표. IaC(Terraform/Ansible) 90% 이상 적용 권고 |
| **DSS (Deliver/Service/Support)** | 서비스 운영·지원 | ITIL 4 17개 Service Management Practices 운영. AIOps 플랫폼(Datadog, Dynatrace, Splunk ITSI) 기반 Event Correlation, 자동 Incident 분류(ML 모델) 적용 |
| **MEA (Monitor/Evaluate/Assess)** | 성과 측정·감사 | KPI/CSI(Critical Success Indicator)·KGI(Key Goal Indicator)·CSF(Critical Success Factor) 3단 계층. ISO 27001/20000/SOC 2 Type II 인증 감사 대응. CMMI 2.0 Maturity Level 평가 |
| **Component: Process** | 실행 절차 | 40개 Management Objective별 RAG(Red/Amber/Green) Status Reporting. Process Capability는 ISO/IEC 33020 PAM(Process Assessment Model) 기준 6단계(L0~L5) 측정 |
| **Component: Information** | 의사결정 데이터 | Data Quality Dimension 7종(Accuracy/Completeness/Consistency/Timeliness/Validity/Unique-ness/Integrity) 측정. Master Data Management(SAP MDG/Informatica) 활용 |
| **Component: Infrastructure & Application** | 기술 토대 | 하이브리드 클라우드(Public 60% / Private 30% / On-prem 10% - Gartner 2024 권고 비율). Kubernetes, Service Mesh(Istio/Linkerd), API Gateway(Kong/Apigee) |

- **📢 섹션 요약 비유**: COBIT의 40개 관리목표는 마치 **병원 진료과목 40개**(내과·외과·신경과 등)와 같습니다. 환자의 증상(기업 요구사항)에 따라 진료과를 선택하듯, IT 과제별로 적절한 관리목표를 매핑하고, EDM은 **진료위원회**, APO는 **진단계획**, BAI는 **수술/시술**, DSS는 **입원·회복 관리**, MEA는 **퇴원 후随访(Follow-up)**에 해당합니다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001:2022** | **CMMI 2.0** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 체계 | IT 서비스 운영 우수성 | 정보보안 관리체계(ISMS) | 조직 프로세스 성숙도 |
| **구조** | 5 Domain / 40 Obj. | 34 Practice (3 카테고리) | 93 통제항목 (4장) / Annex A | 5 Category / 20 PA |
| **성숙도 모델** | ISO/IEC 33020 PAM (L0~L5) | 4-Tier Maturity | ISO/IEC 33020 (L1~L5) | 5 Maturity Level (1~5) |
| **적용 범위** | Enterprise 전체 IT | IT Service 중심 | 정보보안 통제 전 영역 | SW·시스템 통합·서비스 |
| **인증** | COBIT Certified (개인) | ITIL 4 Foundation~Master | ISO 27001 인증 (조직) | CMMI Appraisal (조직) |
| **연계/통합** | APO/BAI/DSS ↔ ITIL Practices | DSS ↔ COBIT DSS | COBIT DSS05/DSS06 ↔ Annex A | CMMI RDM/CAR ↔ COBIT BAI/MEA |

**상호 연계 패턴:**
- **COBIT APO12(위험 관리)** ↔ **ISO 27001 Clause 6.1(위험 평가)** ↔ **ISO 31000:2018 ERM**
- **COBIT BAI03(솔루션 도입)** ↔ **CMPI 2.0 PI(Process Integration)** ↔ **TOGAF ADM Phase E-F**
- **COBIT DSS02(서비스 요청·사고)** ↔ **ITIL 4 Incident Mgmt Practice** ↔ **ISO 20000:2018**
- **COBIT MEA01(성과 모니터)** ↔ **BSC 4관점** ↔ **CSF(CyberSecurity Framework) DE.CM**

```text
[4대 프레임워크 통합 매핑 예시: '사고 관리(Incident Management)' 한 사례]

  +- 기업 목표 -----------------------------------------+
  |  "IT 서비스 중단으로 인한 매출 손실 50% 감축"        |
  +-----------+------------------------------------------+
              | (Cascade)
  +-----------v------------------------------------------+
  |  Alignment Goal: 정보보안 사고 0건, 가용성 99.99%     |
  +-----------+------------------------------------------+
              |
  +-----------v------------------------------------------+
  |  IT Goal: MTTR(평균 복구시간) 4시간 -> 30분 단축       |
  +-----------+------------------------------------------+
              |
  +- COBIT DSS02(서비스 요청·사고관리) -+
  +- ITIL 4 Incident Mgmt Practice ----+--> 3프레임워크 동시 매핑
  +- ISO 27001 A.5.24~26(사고관리) ----+
  +-------------------------------------+
              |
  +-----------v------------------------------------------+
  |  구현 도구: PagerDuty + ServiceNow ITSM + Splunk     |
  |  + Datadog APM + Slack/Teams Pager 연동              |
  |  SLA: P1 15분, P2 1시간, P3 4시간, P4 24시간         |
  +------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 4대 프레임워크는 **자동차의 4륜 서스펜션**와 같습니다. COBIT은 **핸들**(방향·전략), ITIL은 **엔진**(서비스 실행), ISO 27001은 **브레이크**(안전 통제), CMMI는 **휠 밸런스**(성숙도 균형)에 각각
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 482 / 800

<- **이전**: [481. IT 경영 관리 핵심 토픽 481번 시험 요약](/studynote/12_it_management/05_security_compliance/481_it_management_core_topic_481_exam_summary/)
**다음**: [483. IT 경영 관리 핵심 토픽 483번 시험 요약](/studynote/12_it_management/05_security_compliance/483_it_management_core_topic_483_exam_summary/) ->

---
