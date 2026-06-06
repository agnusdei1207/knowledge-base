---
title: "IT Management Core Topic 600 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 600. IT 경영 관리 핵심 토픽 600번 시험 요약 (IT Management Core Topic 600 Exam Summary)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리(거버넌스+관리)는 COBIT 2019의 EDM(평가·지휘·모니터) 5개 영역과 ITIL 4의 SVS(서비스 가치 시스템) 7개 원리를 통해, 비즈니스 가치(Value Realization)와 리스크 최적화(Resource & Risk Optimizer)를 동시에 달성하기 위한 **3축(Governance-Management-Operation) 상호작용 체계**이다.
> 2. **가치**: 체계 적용 시 IT 투자 대비 ROI 평균 20~35% 개선(Forrester 2022), 인시던트 MTTR 50% 단축, 거버넌스 성숙도 2단계 향상(Level 2->4)이라는 정량적 효과가 입증되었으며, ISO 37000(거버넌스), ISO 27001(정보보호), ISO 20000(서비스) 3대 인증 동시 취득 시 기업 신뢰도 KPI가 78% 상승한다.
> 3. **판단 포인트**: COBIT(거버넌스) ↔ ITIL(서비스 운영) ↔ PMBOK(프로젝트) ↔ ISO(규격) 간 **체계 중복(Silo Overlap)**을 회피하기 위한 "**Governance-Management-Operation Layer 분리 원칙**"과, RACI 매트릭스에서 C(Consult)와 I(Inform)의 경계를 명확히 하는 권한 분장 설계가 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 도입·운영을 넘어, **경영 전략과 IT의 정렬(Strategic Alignment)**, **가치 창출(Value Realization)**, **리스크 관리(Risk Optimization)**, **자원 최적화(Resource Optimization)**를 통합 관리하는 체계가 필요해지면서 IT 경영관리(Information Technology Management)가 기술사 시험의 핵심 토픽으로 부상했다. 2022년 이후 클라우드·AI·제로트러스트 환경으로 패러다임이 전환되면서, 전통적 ITIL v3(2011) -> ITIL 4(2019), COBIT 5(2012) -> COBIT 2019, PMBOK 6th -> PMBOK 7th로 프레임워크가 갱신되었고, **NCSF(국가정보보호기본법)**, **DORA(2024 EU 디지털 운영 복원력법)**, **K-ISMS-P(2024년 개편안)** 등 규제 환경도 함께 진화하고 있다.

기술사 600번 시험은 정보관리·컴퓨터시스템응용 기술사 1차/2차 시험의 근간을 형성하며, 합격자는 기업 CIO·CISO·CDO·PMO Leader로서 거버넌스 구조를 설계하고 5,000억 원 이상의 IT 포트폴리오를 리딩할 수 있는 역량을 입증해야 한다.

```text
  +----------------------------------------------------------------------+
  |              [ 전략·비즈니스 환경 ]  (External Drivers)               |
  |  ESG, AI-Ethics, EU-AI-Act, DORA, ESG-Disclosure, Digital Tax         |
  +------------------------+---------------------------------------------+
                           | 전략 정렬(Strategic Alignment)
                           v
  +----------------------------------------------------------------------+
  |      [ 거버넌스 층 - GOVERNANCE LAYER ]   <- COBIT 2019 / ISO 37000  |
  |  • EDM 5영역(Evaluate, Direct, Monitor)                              |
  |  • 거버넌스 시스템: 원칙·정책·구조·문화·인력·절차 (6 Components)      |
  |  • 의사결정 권한: 이사회 -> IT Steering Committee -> CIO               |
  +------------------------+---------------------------------------------+
                           | 지휘/모니터(Direct/Monitor)
                           v
  +----------------------------------------------------------------------+
  |       [ 관리 층 - MANAGEMENT LAYER ]      <- ITIL 4 / PMBOK 7 / ISO  |
  |  • 7대 ITIL 실무: Service Strategy ~ Continual Improvement          |
  |  • 8개 성능 영역(PMBOK 7): 이해관계자·팀·접근방식·계획·일정·...       |
  |  • 12 원칙(PMBOK 7): 가치·팀·복잡성 적응·리더십·품질 등              |
  +------------------------+---------------------------------------------+
                           | 운영 지시(Operational Direction)
                           v
  +----------------------------------------------------------------------+
  |      [ 운영 층 - OPERATION LAYER ]     <- 4-Process / DevOps / SRE  |
  |  • Service Desk·Incident·Problem·Change·Release·Capacity            |
  |  • Site Reliability Engineering: SLI/SLO/Error Budget 적용            |
  |  • Observability: Metrics·Logs·Traces 3-Pillars                      |
  +----------------------------------------------------------------------+
```

**📢 섹션 요약 비유**: IT 경영관리는 마치 **도시의 행정 시스템**과 같다. 시议会(이사회)가 법·조례(거버넌스)를 만들고, 시청·부청(관리층)이 집행 절차를 운영하며, 동 주민센터·소방서·경찰(운영층)이 시민에게 직접 서비스를 제공한다. 이 세 층이 명확히 분리되어 있지 않으면, 한 부서의 실수가 도시 전체의 혼란으로 번진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 근간이 되는 **COBIT 2019 Governance & Management Objectives(40개 목표)**는 5개 도메인(**EDM·APO·BAI·DSS·MEA**)에 40개 Governance/Management Objective를 배치한 **Cascade Goal Model**로 작동한다. 상위 **Stakeholder Drivers(13개)** -> **Enterprise Goals(13개)** -> **Alignment Goals(13개)** -> **Management Objectives(40개)**로 인과(Causal) 매핑되어, "왜(Why)"라는 비즈니스 목표에서 "무엇을(What)" 관리할 것인지를 도출한다.

```text
    +----------------------------------------------------------+
    |            COBIT 2019 핵심 메타구조 (Core Model)           |
    +----------------------------------------------------------+

    +- Stakeholder Concerns(13) ---- Driver ----+
    |  • 비용절감·품질·敏捷성·신속한 정보 제공                  |
    |  • 컴플라이언스·정보보호·가용성·민첩성                    |
    +------------------+-----------------------+
                       v
    +- Enterprise Goals(13) ----------------------------------+
    |  EG01 포트폴리오·프로그램 합리화    EG06 비즈니스 민첩성  |
    |  EG03 위험 관리 의사결정 최적화      EG08 내부 통제 최적화|
    |  EG11 규제 준수 최적화              EG13 지식·인재 관리  |
    +------------------+--------------------------------------+
                       v  (Cascade Mapping)
    +- Alignment Goals(13, IT측 목표) -------------------------+
    |  AG01 IT 준수 및 지원     AG06 IT 비용 최적화             |
    |  AG05 IT 위험 관리        AG09 정보·기술 인프라·앱 최적화 |
    +------------------+--------------------------------------+
                       v
    +- Governance & Management Objectives(40) ----------------+
    |  EDM: EDM01~05 (5개)  <- 이사회·경영진 관할                |
    |  APO: APO01~14 (14개) <- 기획·조직·전략                    |
    |  BAI: BAI01~11 (11개) <- 구축·이행                         |
    |  DSS: DSS01~06 (6개)  <- 서비스·지원·보안                  |
    |  MEA: MEA01~04 (4개)  <- 모니터링·평가·감사                |
    +------------------+--------------------------------------+
                       v
    +- Component Variants (7대 구성요소 + 40 목표 × 변형) -----+
    |  Principles·Policies·Processes·Org Structures·Culture    |
    |  Information·People·Skills·Services·Infrastructure·Apps  |
    +----------------------------------------------------------+
```

| 구성 요소 (7대) | 역할 | 핵심 기술/방법론·산출물 |
| :--- | :--- | :--- |
| **Principles & Policies** | 거버넌스의 기본 원칙·정책 체계 | COBIT 2019 Governance System Principles(6개): Each Enterprise Needs, Holistic Approach, Dynamic System, Distinct from Mgmt, Customized, Ends-to-End |
| **Processes** | 실무·업무 절차·활동의 집합 | Process Reference Model PRM: 40 Processes × 7단계(Plan-Do-Check-Act + Plan-Do-Check-Act) |
| **Organizational Structures** | 의사결정 권위·계층 구조 | 이사회 -> IT 전략위(ISC) -> CIO -> PMO -> 서비스 운영 조직 (RACI 4분면) |
| **Culture, Ethics & Behavior** | 문화·윤리·행동 양식 | Tone at the Top, Ethical Code, Whistleblowing, CobiT Culture Maturity 5단계 |
| **Information** | 정보 흐름·공유·품질 | Data Governance, Master Data Mgmt, Metadata, ISO 8000(데이터 품질) |
| **People, Skills & Competencies** | 인력·역량·기술 | SFIA v8(Skills Framework for Information Age), Skill Gap Analysis, Learning Path |
| **Services, Infrastructure & Applications** | 서비스·인프라·앱 자산 | CMDB, Service Catalog, Application Portfolio Mgmt(APM), FinOps |

**핵심 산출물 — Goal Cascade & RACI**: COBIT 2019는 단순히 40개 목표를 나열하는 것이 아니라, **Goal Cascade(목표 캐스케이드)**를 통해 "비즈니스 니즈 -> IT 정렬 목표 -> 관리 목표 -> 프로세스 활동"으로 자동 매핑된다. 예컨대 EG13(인재·지식 관리) -> AG09(인프라 최적화) -> APO07(인력 관리) -> KGI(핵심 목표 지표) & KPI(핵심 성과 지표) 식으로 인과 관계를 정의한다. 40개 목표 각각에 대해 7대 구성요소 변형(7 Component Variants)을 정의할 수 있어, **중소·대기업·공공기관**에 맞춘 맞춤화가 가능해졌다.

**📢 섹션 요약 비유**: COBIT 2019는 **오케스트라의 악보**와 같다. 지휘자(이사회)가 BPMN으로 작곡한 40악장(40목표)을 보고, 제1바이올린(기획팀)·제2바이올린(구축팀)·비올라(서비스팀)·첼로(모니터팀)가 각자 정확한 빠르기와 음색(Component)으로 연주해야, 관객(Stakeholder)이 원하는 하모니(가치)를 들을 수 있다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7th** | **ISO 27001:2022** | **ISO 20000-1:2018** |
|:---|:---|:---|:---|:---|:---|
| **주 목적** | 거버넌스·전사 IT 정렬 | 서비스 운영·가치 창출 | 프로젝트 관리 | 정보보호 관리체계(ISMS) | 서비스 관리체계(SMS) |
| **관할 범위** | 5 도메인 × 40 목표 | SVS(서비스 가치 시스템) 7원리 | 8성능영역 + 12원칙 | Annex A 통제 항목 93개(2022 개편) | 10 프로세스 클러스터 |
| **적용 층위** | 거버넌스(전략) | 관리(운영) | 프로젝트(일시성) | 통제(컴플라이언스) | 통제(서비스) |
| **핵심 키워드** | Cascade Goal, EDM, I&T, Maturity | Value Stream, Practice 34, SVS | Principle, Domain, Tailoring | Statement of Applicability, Risk Treatment | Service Catalog, SLA, OLA, UC |
| **인증 가능성** | 없음(자격증만) | ITIL 4 Foundation/MP/SL | PMP/PfMP 자격증 | 인증 가능(BSI/LRQA) | 인증 가능(BVC/LRQA) |
| **상호 연계** | 프로세스 정의를 ITIL에 위임 | COBIT 2019와 상호보완 | BAI 도메인에서 사용 | APO12·DSS05에서 통제 | DSS 도메인과 일치 |
| **측정 KPI** | 거버넌스 성숙도(5단계) | CSI(Value Stream Efficiency) | Schedule/Cost/Scope 트라이어드 | RPO/RTO/MTPD 기반 BIA | First-Contact Resolution, MTRS |
| **갱신 주기** | 6~8년(2019->2025?) | 6~8년(2019->2025?) | 4~6년(2021) | 5~7년(2013->2022) | 5~7년(2011->2018) |
| **주 적용 대상** | 임원·CIO·이사회 | 서비스매니저·인시던트매니저 | PM·PMO·스폰서 | CISO·보안담당 | IT 서비스 매니저 |

**상호 연계 아키텍처 — "3-Layer Integration"**: 실전에서는 이 4~5개 프레임워크가 **계층적으로 통합**된다. (1) **전략·거버넌스 층**에서는 COBIT 2019 EDM 영역 + PMBOK 7th 원칙(특히 "Steward, Tailor, Focus on Value")을 사용하고, (2) **관리 층**에서는 PMBOK 7th 8개 성능영역(Stakeholder, Team, Planning, Work, Delivery, Measurement, Uncertainty, Project Work) + ITIL 4의 34개 Practice 중 적절한 것을 활용하며, (3) **운영 층**에서는 ITIL 4의 Incident·Change·Service Desk Practice + ISO 27001 Annex A 통제(예: A.5.24 Incident Management Planning, A.5.25 Assessment of Security Events) + ISO 20000의 Service Delivery Process를 적용한다.

**📢 섹션 요약 비유**: 4대 프레임워크는 **의료 시스템**의 분업과 같다. 의사(COBIT·거버넌스)가 진단과 치료 방향을 결정하고, 간호사·물리치료사(PMBOK·프로젝트)가 처방에 따라 치료를 진행하며, 약사·검사기사(ITIL·운영)가 매일 정해진 투약·검사를 수행하고, 안전관리팀(ISO·통제)이 부작용·안전성을 끊임없이 감시한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 IT 경영관리 체계를 도입할 때, **"거버넌스 먼저(Bottom-up 함정 회피) -> 관리체계 정착 -> 운영 자동화**"의 순서가 원칙이다. 1,000억 원 규모 IT 조직을 운영한다고 가정하면, 1단계에서 1~2년은 COBIT 2019 EDM 시스템 + 거버넌스 헌장(Charter)을 수립하고, 2단계에서 2~3년은 ITIL 4 SVS + 34개 Practice 중 핵심 10개를 선정·도입, 3단계에서 매년 CSI(지속적 개선)를 통해 성숙도 1단계를 향상시킨다.

### 기술사형 판단 체크리스트

1. **거버넌스 성숙도 진단(CMM 5단계)**: ① 계획·정책 수립 여부(Level 1->2),
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 600 / 800

<- **이전**: [599. IT 경영 관리 핵심 토픽 599번 시험 요약](/studynote/12_it_management/05_security_compliance/599_it_management_core_topic_599_exam_summary/)
**다음**: [601. IT 경영 관리 핵심 토픽 601번 시험 요약](/studynote/12_it_management/05_security_compliance/601_it_management_core_topic_601_exam_summary/) ->

---
