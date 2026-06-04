+++
title = "480. IT 경영 관리 핵심 토픽 480번 시험 요약 (IT Management Core Topic 480 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

```markdown
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 정보관리기술사 시험의 480번 토픽은 IT 거버넌스(COBIT 2019, ISO 38500), IT 서비스 관리(ITIL 4), 정보기술 투자관리(EA 거버넌스 연계), ISMS-P, BCP/DRP를 통합한 IT 경영관리 총론으로, B2B/B2C/B2G 환경에서 IT가 비즈니스 가치를 창출하도록 정렬(Strategy-Alignment)하는 프레임워크의 총합이다.
> 2. **가치**: NPV/IRR 기반 IT 투자 포트폴리오 최적화로 TCO 20~35% 절감, COBIT 2019의 40개 거버넌스/관리 목적(Governance & Management Objectives)을 통해 감사 대응 시간 50% 단축, ITIL 4의 34개 Practice 운영으로 MTTR 평균 42% 개선 및 First Call Resolution 25% 향상이 가능하다.
> 3. **판단 포인트**: 중앙집중형(Federal) vs 분산형(Devolved) vs 하이브리드(Federated) IT 거버넌스 모델 선택 시 통제력-민첩성 트레이드오프, COBIT의 Design Factor 11개 변수와 ITIL Value Stream별 KPI 충돌 해소, ISO 38500의 6원칙(Evaluate, Direct, Monitor) 적용 시 이사회-경영진-IT조직 간 책임 소재(RACI) 명확화가 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 시험의 480번 토픽(IT 경영 관리 핵심)은 4차 산업혁명 시대를 맞아 IT가 단순 비용센터(Cost Center)에서 가치 창출 센터(Value Center)로 전환되는 과정에서, 기업이 IT 자산을 어떻게 전략적으로 기획·도입·운영·평가·폐기(PI Planning: Plan-Identify-Direct-Monitor)할 것인지를 총괄하는 영역이다. 과거 1990년대까지는 CIO(Chief Information Officer)가 단순 인프라 운영과 ERP(예: SAP R/3, Oracle E-Business Suite) 도입에 집중했다면, 2010년대 이후 클라우드 전환, 데이터 거버넌스(DAMA-DMBOK 2.0), AI 윤리(UNESCO Recommendation on Ethics of AI, 2021) 이슈가 부상하면서 IT 경영관리의 범위와 복잡도가 기하급수적으로 증가했다.

특히 한국 환경에서는 전자정부법(제47조의2에 따른 정보시스템 감리), 클라우드컴퓨팅법(2024년 시행), 개인정보보호법(가명정보 처리 근거), AI 기본법(2026년 시행 예정)에 따라 IT 경영관리 체계의 법적 컴플라이언스가 필수이며, 공공부문의 정보시스템 감리 1·2·3등급 기준(행정안전부 고시 제2023-12호)에 따라 매년 1만여 개 정보시스템이 감리 대상이 된다. 이러한 환경에서 정보관리기술사는 단순히 기술 아키텍처뿐 아니라 IT 가치평가(ROI, EVA, ROA-IT), 리스크 관리(ISO 31000 기반), 서비스 운영 효율성(ITIL 4), 정보보안 통제(ISMS-P 22개 영역, 102개 통제항목)를 통합 설계할 수 있는 역량을 입증해야 한다.

```text
+--------------------------------------------------------------------------+
|              IT 경영관리 4대 핵심 축 (The Four Pillars)                  |
+--------------------------------------------------------------------------+
|                                                                          |
|  [1. 거버넌스]         [2. 서비스관리]      [3. 투자/아키텍처]            |
|  +------------+        +------------+      +------------+              |
|  | COBIT 2019 |◄------►|  ITIL 4    |◄----►|  TOGAF     |              |
|  | ISO 38500  |        |  SIAM      |      |  Zachman   |              |
|  | ISO 27001 |        |  VeriSM    |      |  FEA/FEAR  |              |
|  +-----+------+        +-----+------+      +-----+------+              |
|        |                     |                    |                     |
|        +---------+-----------+--------------------+                     |
|                  v                                                       |
|        [4. 컴플라이언스/리스크]                                           |
|        +----------------------------+                                   |
|        | ISMS-P · PIPA · 전자정부법 |                                   |
|        | ISO 22301(BCP) · ISO 31000 |                                   |
|        | ESG-IT 공시 · IT 감사(ISA) |                                   |
|        +----------------------------+                                   |
+--------------------------------------------------------------------------+
                              |
                              v
              +-------------------------------+
              |   비즈니스 가치(Value Realization)|
              |   Strategy -> Value Chain -> KPI |
              +-------------------------------+
```

기존 패러다임은 ①Waterfall 방식의 대규모 SI(System Integration) 프로젝트 통제(예: 정보화사업 감리법 1999년), ②CAPEX(Capital Expenditure) 중심의 HW 구매, ③부서 단위 정보시스템 운영이었으나, ①현재는 ①Agile·DevOps·DevSecOps 기반의 지속적 배포(Continuous Delivery), ②OPEX(Operational Expenditure) 기반의 클라우드 구독 모델(예: AWS EDP, MS EA, GCP CUD), ③EA(Enterprise Architecture) 기반의 전사 통합 관점으로 패러다임이 전환되었다. 한국정보화진흥원(KIAT)의 2023년 보고서에 따르면 국내 500대 기업의 73%가 IT 거버넌스 체계를 도입했으나, COBIT과 ITIL을 동시에 적용하여 통합 운영하는 비율은 18%에 불과하여 통합 관리 체계 구축이 시급한 상황이다.

- **📢 섹션 요약 비유**: IT 경영관리는 마치 도시의 교통관제 시스템과 같다. 도로(인프라), 차량(애플리케이션), 신호등(거버넌스), 경찰(보안), 비상시 우회도로(BCP) 모두가 동시에 조화롭게 돌아가야 시민(사용자)들이 안전하고 빠르게 목적지(비즈니스 목표)에 도착할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심 메커니즘은 **PDCA(Plan-Do-Check-Act) + Strategy -> Value Chain**의 이중 루프 구조다. 상위 루프는 ISO 38500의 "Evaluate(평가) -> Direct(지시) -> Monitor(감독)"로 이사회-경영진-감사위원회가 참여하는 거버넌스 레벨이고, 하위 루프는 ITIL 4의 "SVS(Service Value System)"가 IT 운영을 담당한다. 이 둘을 잇는 가교(bridge)가 COBIT 2019의 "Goals Cascade" 메커니즘으로, 이해관계자 니즈(Stakeholder Drivers) -> 기업목표(Enterprise Goals) -> 정렬계획(Alignment Goals) -> IT 관련 목표(IT-Related Goals) -> Enabler(프로세스/구조/정보/사람/문화/기술) -> 단위 목표(Process Purpose) -> 메트릭(Metrics & Maturity)로 7단계 인과 체인을 형성한다.

특히 COBIT 2019는 **Design Factor 11개**(Enterprise Strategy, Enterprise Goals, Risk Profile, I&T-Related Issues, Threat Landscape, Compliance Requirements, Role of IT, Sourcing Model for IT, IT Implementation Methods, Technology Adoption Strategy, Enterprise Size & Industry)를 조합하여 거버넌스 시스템의 40개 Governance & Management Objectives 중 어떤 것을 우선 적용할지 결정한다. 이때 우선순위 결정에는 North Star Framework(기업전략->IT전략) + Portfolio Rationalization(중복 IT 자산 제거) + Run-Grow-Transform(RGT) 분석이 결합된다.

```text
  +------------------------------------------------------------+
  |  COBIT 2019 Goals Cascade + ISO 38500 + ITIL 4 통합 흐름  |
  +------------------------------------------------------------+

  [이사회/감사위원회]
        | ISO 38500 6원칙
        | 1)Responsibility 2)Strategy 3)Acquisition
        | 4)Performance 5)Conformance 6)Human Behavior
        v
  +------------------------------------------------+
  |  거버넌스 체계 (Governance System)              |
  |  +------------------------------------------+  |
  |  | EDM(평가/지시/감독) - 5개 프로세스       |  |
  |  |  • EDM01 Governance Framework Setting    |  |
  |  |  • EDM02 Benefits Delivery               |  |
  |  |  • EDM03 Risk Optimization               |  |
  |  |  • EDM04 Resource Optimization           |  |
  |  |  • EDM05 Stakeholder Transparency        |  |
  |  +------------------------------------------+  |
  |  + Design Factor 11개 -> 우선순위 결정            |
  +-------------------+----------------------------+
                      v
  +------------------------------------------------+
  |  관리 체계 (Management System) - 35개 프로세스  |
  |  +------+ +------+ +------+ +------+ +-----+  |
  |  |APO(14)| |BAI(11)| |DSS(6)| |MEA(4)| |  …  |  |
  |  |전략/  | |구축/  | |서비스| |평가/ | |     |  |
  |  |조정  | |변경  | |지원  | |모니터| |     |  |
  |  +--+---+ +--+---+ +--+---+ +--+---+ +-----+  |
  +-----+--------+--------+--------+----------------+
        v        v        v        v
  +------------------------------------------------+
  |  ITIL 4 Service Value System (SVS)              |
  |  • Opportunity/Demand -> Value                   |
  |  • Guiding Principles(7)                       |
  |  • Governance(ISO 38500 연동)                   |
  |  • Practices(34) -> Service Value Chain(6활동)  |
  |    Plan->Engage->Design&Transition->Obtain/Build  |
  |    ->Deliver&Support->Improve                    |
  |  • Continual Improvement(CSI Model 7단계)      |
  +-------------------+----------------------------+
                      v
  +------------------------------------------------+
  |  Enabler Layer (자원/역량)                      |
  |  • People(역량) • Process(절차) • Technology    |
  |  • Information(데이터) • Structure(조직)        |
  |  • Culture(문화)                                |
  +------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스·관리 통합 프레임워크 | 40개 Governance/Management Objectives, Design Factor 11개로 우선순위 결정, Goals Cascade 7단계로 기업목표->IT목표 정렬, 7개 컴포넌트(프로세스/구조/정보 흐름/인력/문화/서비스/기술) 상호작용 모델링 |
| **ITIL 4** | IT 서비스 운영·개선 프레임워크 | 34개 Practice(General Management·Service·Technical Management), Service Value Chain 6개 활동, 7개 Guiding Principle(Focus on Value, Start Where You Are, Progress Iteratively 등), CSI(Continual Service Improvement) 7단계 모델 |
| **ISO 38500:2015** | IT 거버넌스 국제표준 | 6원칙(RSDCRH), 3개 주요 프로세스(Evaluate/Direct/Monitor), 이사회 의무 명시, 2008년 초판 후 2015년 전면 개정 |
| **EA (TOGAF 10 / Zachman)** | 전사 아키텍처 설계·통합 | TOGAF ADM(Architecture Development Method) 8단계 Phases(Pre-Req->A->B->C->D->E->F->G->Req Mgmt), Zachman 6×6 매트릭스(What/How/Where/Who/When/Why × Scope/Enterprise/System/Technology/Detail/Substantive) |
| **ISMS-P (2024 인증기준)** | 정보보안 경영체계 | 13개 영역, 84개 통제항목(2024년 개편), 정보통신망법·개인정보보호법·전자금융거래법 컴플라이언스 통합 인증, K-ISMS 인증 의무화(공공기관, 2021~) |
| **IT 투자관리 프레임워크** | IT 포트폴리오 가치 최적화 | 3단계 의사결정(①Project Portfolio Mgmt -> ②Program Mgmt -> ③Project Mgmt), 정량평가 모델(NPV/IRR/EVA/Payback Period), 정성평가 모델(Strategic Fit Score, Risk Score), Balanced Scorecard for IT(Kaplan-Norton 4관점) |
| **BCP/DRP (ISO 22301)** | 사업연속성 관리 | BIA(Business Impact Analysis) -> RTO/RPO 산출 -> DR 전략(Active-Active/Hot/Warm/Cold) -> 리허설(Test: Tabletop/Simulation/Parallel/Full Interruption), MTPD/MBCO/RTO/RPO 4대 지표 |

**핵심 메트릭 및 산식**:
- IT 투자 ROI: `ROI = (
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 480 / 800

<- **이전**: [479. IT 경영 관리 핵심 토픽 479번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/479_it_management_core_topic_479_exam_summary/)
**다음**: [481. IT 경영 관리 핵심 토픽 481번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/481_it_management_core_topic_481_exam_summary/) ->

---
