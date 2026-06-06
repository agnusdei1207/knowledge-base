---
title: "IT Management Core Topic 658 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(658번) 토픽은 **COBIT 2019, ITIL 4, ISO 38500** 등 글로벌 거버넌스 프레임워크를 기반으로 IT 전략-운영-감리 3계층의 정렬(Alignment)을 통해 **가치(Value)·리스크(Risk)·자원(Resource)**의 균형적 최적화를 달성하는 경영과학 영역이다.
> 2. **가치**: 정량적 측면에서 IT 투자 대비 ROI **20~35% 향상**(Gartner 2024), 서비스 인시던트 **MTTR 60% 단축**, 규제 컴플라이언스 비용 **40% 절감**, 정성적 측면에서 이사회-경영진-IT 간 **단일 언어(Single Pane of Glass)** 확보 및 의사결정 속도 제고.
> 3. **판단 포인트**: 프레임워크 채택 시 **규모·업종·규제 환경**에 따라 (1)Governance System vs Management System 분리, (2)CMMI·ITIL·COBIT 통합 레퍼런스 모델(PRM) 적용, (3)BSC 기반 KPI 4관점(재무/고객/내부/학습성장) 매핑 여부, (4)Agile·DevOps 시대에 ITIL 4의 **Service Value System(SVS)** 재해석 필요성을 핵심 트레이드오프로 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 지원(Back-office)에서 **전략 동인(Strategic Enabler)**으로 격상되면서, IT에 대한 의사결정 권한·책무·평가체계를 별도 경영관리 체계로 분리 운영해야 할 필요성이 대두되었다. 한국 정보통신산업진흥원(NIPA)의 「정보시스템 감리기준」과 금융감독원의 「전산감리지침」, 공공부문의 「전자정부법」 등 다양한 규제가 IT 거버넌스의 형태를 결정하며, 글로벌 표준으로 **COBIT(Control Objectives for Information and Related Technologies)**이 ISO/IEC 38500과 함께 사실상의 디팩토 표준으로 자리잡았다. 1980년대 비용중심의 IT관리 -> 1990년대 TQM/TQC · BPR -> 2000년대 ITIL/COBIT 등장 -> 2010년대 디지털전환(Cloud, BigData, AI) -> 2020년대 ESG·제로트러스트·생성형AI 거버넌스로 패러다임이 진화해 왔다.

```text
+---------------------------------------------------------------------+
|              IT 경영 관리 3계층 정렬(Alignment) 모델                 |
|                                                                     |
|  +--------------------------------------------------------------+  |
|  |  Layer 1: IT 거버넌스 (Governance) - 이사회·경영진 책임      |  |
|  |  ----------------------------------------------------------  |  |
|  |  • 전략 정렬(Strategic Alignment)  : 비즈니스 ↔ IT 전략     |  |
|  |  • 가치 전달(Value Delivery)       : ROI, EVA, BNM         |  |
|  |  • 리스크 관리(Risk Management)     : ISO 31000, RMF        |  |
|  |  • 자원 관리(Resource Management)   : IT 예산·인력·아키텍처 |  |
|  |  • 성과 측정(Performance Mgmt)      : BSC, KPI, OKR         |  |
|  |  • 원칙: 책임(R)·전략(S)·취득(A)·성과(P)·준거(C)·인간(B)  |  |
|  |        <- ISO/IEC 38500:2015 6대 원칙                         |  |
|  +--------------------+-----------------------------------------+  |
|                       | 정렬(Align)                                 |
|  +--------------------+-----------------------------------------+  |
|  |  Layer 2: IT 관리 (Management) - CIO·IT조직 책임            |  |
|  |  ----------------------------------------------------------  |  |
|  |  +---------+ +---------+ +---------+ +---------+ +--------+|  |
|  |  |전략기획 | |프로젝트| |서비스  | |인프라  | |정보보안||  |
|  |  |ISP 수립| |PMO     | |ITIL 4  | |DC/Cloud| |ISMS   ||  |
|  |  +---------+ +---------+ +---------+ +---------+ +--------+|  |
|  |                  5대 관리 도메인 (Plan/Build/Run/Monitor/...) |  |
|  +--------------------+-----------------------------------------+  |
|                       | 통제(Control)                               |
|  +--------------------+-----------------------------------------+  |
|  |  Layer 3: IT 운영·감리 (Operation & Audit) - 실무·감리인    |  |
|  |  ----------------------------------------------------------  |  |
|  |  • 일일 운영: 모니터링, incident, change, problem           |  |
|  |  • 컴플라이언스: 개인정보보호법, ISMS-P, PCI-DSS, GDPR      |  |
|  |  • 감리: 정보시스템 감리(연 1회), 전산감리(금융), 내부통제  |  |
|  |  • 측정: SLA(99.9%^), 가용률, 보안지수, CSAT/NPS           |  |
|  +--------------------------------------------------------------+  |
+---------------------------------------------------------------------+
```

**왜 필요한가?** 기존 IT관리는 "기술 중심(Technology-centric)"으로 단일 프로젝트의 TCO·일정·품질만을 관리했다. 그러나 디지털 시대에는 **사이버리스크, 개인정보보호, ESG, 공급망(Supply Chain) 리스크** 등 비기술 리스크가 IT 가치를 잠식하고, **Cloud·SaaS·API 경제**로 IT 자원이 외부화됨에 따라 내부 통제만으로는 한계가 있다. 이에 이사회 차원의 거버넌스, 경영층의 관리, 실무의 운영이 **One-Company-View**로 통합되어야 한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판(대시보드)**과 같다. 엔진(기술)이 아무리 좋아도 속도계·연료계·경고등(거버넌스) 없이는 운전자가 차를 안전하게 몰 수 없듯, IT 기술이 아무리 발전해도 경영 의사결정 계기판 없이는 기업을 안전한 목적지(가치)로 데려갈 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **COBIT 2019의 거버넌스/관리 목표 체계**와 **ITIL 4의 Service Value Chain**을 이중축으로, **ISO 38500의 6대 원칙**을 최상위 헌법(Constitution)처럼 운용하는 3-Layer 구조다. 이 셋은 상호보완적이며, 기술사 답안에서는 **"거버넌스=이사회, 관리=CIO, 운영=실무"**의 위계로 명확히 구분 표현해야 한다.

```text
+----------------------------------------------------------------------+
|        COBIT 2019 Governance & Management Objectives 계층도          |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  |  EDM: Evaluate, Direct, Monitor (5목표) <- 거버넌스 영역     |   |
|  |   EDM01 프레임워크 보장 | EDM02 이득 전달 | EDM03 리스크 최적 |   |
|  |   EDM04 자원 관리 | EDM05 투명성 보장                          |   |
|  +-------------------------+------------------------------------+   |
|                            | 연계                                   |
|  +-------------------------+------------------------------------+   |
|  |  Align, Plan, Organize (APO) - 14목표  <- 관리 영역          |   |
|  |   APO01 관리 프레임워크 | APO02 전략 | APO04 조직 | ...      |   |
|  +--------------------------------------------------------------+   |
|  |  Build, Acquire, Implement (BAI) - 11목표                    |   |
|  |   BAI01 프로그램 | BAI02 요구사항 | BAI03 변경 ...           |   |
|  +--------------------------------------------------------------+   |
|  |  Deliver, Service, Support (DSS) - 6목표                     |   |
|  |   DSS01 운영 | DSS02 인시던트 | DSS03 문제 ...               |   |
|  +--------------------------------------------------------------+   |
|  |  Monitor, Evaluate, Assess (MEA) - 4목표                     |   |
|  |   MEA01 성과평가 | MEA02 내부통제 | MEA03 컴플라이언스 ...   |   |
|  +-------------------------+------------------------------------+   |
|                            | 활동(Activity) 매핑                    |
|  +-------------------------+------------------------------------+   |
|  |  ITIL 4 Service Value Chain (SVC) - 운영 실무 활동            |   |
|  |   Plan->Engage->Design&Transition->Obtain/Build->Deliver&       |   |
|  |   Support->Improve (34개 Practice, 9개 가치사슬 활동)         |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  ★ 모든 목표는 7대 컴포넌트(원리/정책/프로세스/조직구조/정보/        |
|    인력·역량/서비스·인프라·앱)로 분해되어 Design Factor별로         |
|    우선순위(Importance)와 Rating(H/N/L)으로 적용된다.               |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(평가·지시·모니터)** | 이사회·감사위원회 책임, 거버넌스 의사결정 | COBIT 2019의 5개 목표, 의사결정 RACI 차트, ISACA의 GEIT(Governance of Enterprise IT) 모델 기반 분기별 1회 의사결정 사이클 운영 |
| **APO(정렬·계획·조직)** | CIO·전략기획 책임, IT전략-비즈니스 정렬 | SWOT·TOWS 분석, ISP(정보화전략계획) 수립 5단계(현황분석->목표설정->전략수립->실행계획->모니터링), Critical Success Factor(CSF) 도출, Key Goal Indicator(KGI)·Key Performance Indicator(KPI) 2단 계층화 |
| **BAI(구축·획득·구현)** | 프로젝트·개발조직 책임 | PMBOK 7th·PRINCE2·Agile(Scrum, SAFe) 혼합(하이브리드) 방식, 단계별 게이트 검토(Gate Review), Benefit Realization Plan(BRP), V-Model·워터폴-애자일 혼합 |
| **DSS(전달·서비스·지원)** | 서비스운영·인프라조직 책임, ITIL 4 Practice 14개 영역 | Incident Management(P1~P4 SLA), Problem Management(RCA: 5 Why, Fishbone, Fault Tree), Change Enablement(ECAB), Service Desk(FCR≥75%, AHT≤8분), Knowledge Management |
| **MEA(모니터링·평가·감사)** | 내부감사·컴플라이언스 책임, PDCA 폐쇄루프 | COBIT 목표별 **Maturity Model(0~5단계)**, 내부통제(미비점 식별->권고->조치->재발방지), 외부감리(연 1회 종합감리, 수시감리), KPI 대시보드(PowerBI·Grafana·Tableau), Capacity Mgmt·Availability Mgmt·BCM(ISO 22301) |
| **컴포넌트 7요소** | 40개 거버넌스/관리 목표의 구성단위 | Process·Organizational Structures·Information Flow·People, Skills & Competencies·Policies & Procedures·Culture, Ethics & Behavior·Services, Infrastructure & Applications — **7가지 Design Factor**(전략·목표·리스크·문제·위기·컴플라이언스·IT역량)에 따라 우선순위 산정 |
| **Focus Area(집중영역)** | 산업·사안에 특화된 거버넌스 적용 | 「DevOps」「사이버보안」「디지털윤리」「ESG」「위험관리」「중소기업」 등 ISACA 제공 — 핵심 40목표에 추가 목표를 동적으로 연결 |

**핵심 메커니즘 심화**:
- **Maturity Level 산정 공식**: GAPP(Model)(CMMI 기반) 0(Incomplete)~5(Optimizing)단계. 판정 기준은 **PA(Process Attribute) 6개**(Purpose, Focus, Capability, Performance, Manageability, Work Product) + **Process Purpose Outcomes(PPO)** 충족도.
- **Risk Appetite -> Risk Tolerance -> Risk Capacity** 3단계로 분해: COBIT EDM03은 연간 Risk Appetite Statement를 이사회 의결로 확정(예: "주요 정보시스템 장애 시 4시간 이내 복구, 연간 데이터 손실 허용 한도 0분").
- **BSC 4관점 KPI 매핑 예시**: ①재무(ROI, EVA, TCO 절감률), ②고객(CSAT≥4.5/5, NPS≥40), ③내부프로세스(SLA 준수율≥99.9%, Change 성공률≥98%, MTTR≤60분), ④학습성장(직원 인증 보유율, DevOps 성숙도).
- **IT 투자평가 3대 모델**: (1) **재무적 NPV/IRR**(5년 Discount Rate 8%), (2) **포괄적 TCO/ROI**(Gartner TCO 모델, 4계층: 하드웨어·소프트웨어·운영·인력), (3) **균형성과 BRT(Benefit Realization Tracking)** — 정성적/비재무적 효과까지 점수화.
- **BIA(Business Impact Analysis)** 산정식: RTO(Recovery Time Objective) < MTPD(Maximum Tolerable Period of Disruption) < RPO(Recovery Point Objective), 핵심 업무 등급 1~4등급 분류.

- **📢 섹션 요약 비유**: COBIT의 EDM-APO-BAI-DSS-MEA 5도메인은 **"회사 운영 매뉴얼의 목차"**와 같다. EDM은 주주총회, APO는 임원진 회의, BAI는 제품 출시, DSS는 고객센터, MEA는 감사팀 — 이 5개가 같은 KPI를 공유할 때 비로소 한 회사처럼 일관되게 움직인다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 유사/대안 프레임워크를 명확히 구분하는 것이 기술사 답안의 결정적 차등점이다. 같은 "IT 관리"라 해도 **접근축(거버
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 658 / 800

<- **이전**: [657. IT 경영 관리 핵심 토픽 657번 시험 요약](/studynote/12_it_management/05_security_compliance/657_it_management_core_topic_657_exam_summary/)
**다음**: [659. IT 경영 관리 핵심 토픽 659번 시험 요약](/studynote/12_it_management/05_security_compliance/659_it_management_core_topic_659_exam_summary/) ->

---
