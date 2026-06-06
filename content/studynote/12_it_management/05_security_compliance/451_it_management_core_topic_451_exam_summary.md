---
title: "IT Management Core Topic 451 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 5대 원칙(Principle), 7개 구성요소(Component), 40개 관리목표(Management Objective)를 기반으로, **이사회-경영진-IT**의 3계층 책임 구조(Three Lines Model, IIA 2020)에서 IT 의사결정의 정렬(Alignment), 가치제공(Value Delivery), 리스크관리(Risk Management), 자원관리(Resource Management), 성과측정(Performance Measurement) 5대 영역을 통합 운영하는 경영 체계이다.
> 2. **가치**: McKinsey(2021) 조사에서成熟的 IT 거버넌스 도입 기업은 **Time-to-Market 37% 단축, IT 비용 대비 비즈니스 가치 2.4배 증가, 디지털 전환 성공률 3.1배 향상**, ISACA(2022) 보고에 따르면 COBIT 2019 도입 후 감사 발견사항(Internal Audit Finding) 평균 **42% 감소**, 사이버 보안 사고 대응시간(MTTR) **68% 단축** 효과를 입증했다.
> 3. **판단 포인트**: 중앙집중형(Centralized, CoE 기반) vs 분산형(Decentralized, Federal 모델) 거버넌스 구조 선택, **RACI 매트릭스**를 활용한 역할 분장 명확화, **Balanced Scorecard(BSC) 4관점**과 **IT Scorecard**의 KPI 연계 전략, 그리고 **Bimodal IT(Mode 1 안정성 + Mode 2 민첩성)** 환경에서의 거버넌스 이중 트랙 운영이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명(AI·빅데이터·클라우드·IoT) 시대에 기업 IT는 단순 비용센터(Cost Center)에서 **전략적 비즈니스 인에이블러(Strategic Business Enabler)**로 역할이 전환되었다. 그러나 한국정보화진흥원(NIA, 2022) 조사에 따르면 국내 대기업의 **67%가 IT-Business 정렬 실패**를 경험했고, CIO의 **54%가 이사회와의 IT 전략 커뮤니케이션 부재**를 핵심 애로사항으로 지적했다. 또한 Gartner(2023) 보고는 전 세계 IT 프로젝트의 **평균 실패율 31.7%**(Standish Group CHAOS Report 2020 기준 31.1%, 2023년 추정 31.7%), 예산 초과율 평균 **189%**를 제시하며, 거버넌스 부재가 직접적 원인임을 지적했다.

이러한 배경에서 **ISO/IEC 38500:2015 IT 거버넌스 국제표준**, **COBIT(Control Objectives for Information and Related Technologies) 2019**, **ITIL 4(Service Value System)**, **CMMI(Capability Maturity Model Integration) v2.0**, **Val IT 2.0**, **Risk IT 2.0** 등의 프레임워크가 등장했다. 특히 COBIT 2019는 과거 COBIT 5(2012)의 5개 원칙을 **6개 원칙 + 40개 관리목표**로 확장하고, **Focus Area**(예: 사이버보안, DevOps, 디지털윤리, ESG, 클라우드 컴플라이언스)를 도입하여 산업별·이슈별 맞춤 거버넌스 설계를 가능케 했다.

```text
+---------------------------------------------------------------------+
|          IT 거버넌스 3계층 책임구조 (Three Lines Model, IIA 2020)   |
+---------------------------------------------------------------------+
|                                                                     |
|   [1계층: 1st Line - Operational Management]                       |
|   +---------------------------------------------------------+      |
|   |  사업부서/IT운영팀 자체 통제(First Line of Defense)      |      |
|   |  • SLA 준수, IT 서비스 데일리 운영                       |      |
|   |  • DevOps팀 배포 책임 (CI/CD 파이프라인 거버넌스)       |      |
|   |  • 클라우드 FinOps 비용 최적화 실행                      |      |
|   +---------------------------------------------------------+      |
|                          |                                          |
|                          v                                          |
|   [2계층: 2nd Line - Risk & Compliance]                            |
|   +---------------------------------------------------------+      |
|   |  리스크관리·컴플라이언스·정보보안 조직                    |      |
|   |  • ISMS-P 인증, GDPR/개인정보보호법 준수                 |      |
|   |  • COBIT 2019 EDM(Evaluate, Direct, Monitor) 5개 목표   |      |
|   |  • 내부통제 시스템(SOX 404 ITGC) 운영                    |      |
|   +---------------------------------------------------------+      |
|                          |                                          |
|                          v                                          |
|   [3계층: 3rd Line - Internal Audit]                               |
|   +---------------------------------------------------------+      |
|   |  내부감사위원회(IA) - 독립적 assurance 제공              |      |
|   |  • IT 감사 (ITGC, 애플리케이션 통제 검증)                |      |
|   |  • COBIT maturity assessment (5단계 평가)                |      |
|   |  • 외부감사인(공인회계사) 협조                            |      |
|   +---------------------------------------------------------+      |
|                          |                                          |
|                          v                                          |
|   +---------------------------------------------------------+      |
|   |  [Board/이사회 + 외부 감독] - 거버넌스 최종 책임         |      |
|   |  • ISO 38500 Principle 1: Responsibility                  |      |
|   |  • IT전략위원회(STEERING COMMITTEE) 운영                  |      |
|   +---------------------------------------------------------+      |
+---------------------------------------------------------------------+
```

**기존 패러다임(Before)**:
- IT 거버넌스 부재 -> 부서별 IT 투자 중복, 그림자 IT(Shadow IT) 만연, 평균 ROI 0.7배
- 사후 통제(Ex-post Control) 중심 -> 사고 발생 후 사후 감사 및 시정
- CFO/CEO가 IT 비용을 **OpEx(운영비)**로만 인식

**신규 패러다임(After)**:
- **Value-Driven IT Governance**: IT를 **전략적 투자(Strategic Investment)**로 인식, IT 투자 대비 비즈니스 가치(Business Value Realization) 측정
- **사전예방 통제(Ex-ante Control) + 실시간 통제(Real-time)**: GRC(Governance, Risk, Compliance) 플랫폼 기반 연속 통제 모니터링(Continuous Control Monitoring, CCM)
- **Digital Business Governance**: BCG(2022) 기준 디지털 전환 기업의 78%가 **Digital Steering Committee**를 이사회 산하에 설치

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **도시의 종합계획(都市計劃)**과 같습니다. 건물(프로젝트) 하나하나가 멋져도, 상하수도·전기·교통·녹지 등 도시 인프라(거버넌스 체계)가 정비되지 않으면 도시는 무너집니다. COBIT 2019는 도시기본계획이고, ITIL 4는 상하수도 운영 매뉴얼이며, ISO 38500는 도시계획법입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스 프레임워크의 핵심은 **COBIT 2019의 Cascade System(연쇄 시스템)**이다. 상위 **Stakeholder Needs & Goals(13개)** -> **Enterprise Goals(13개)** -> **Alignment Goals(13개)** -> **Management Objectives(40개)** -> **Component Variants** -> **Focus Area Specific Guidance**의 연쇄 구조로, 기업 목표에서 IT 관리 항목까지 추적 가능(Traceable)하다.

```text
+---------------------------------------------------------------------+
|         COBIT 2019 Cascade System (Goals Cascade)                  |
+---------------------------------------------------------------------+
|                                                                     |
|  [Stakeholder Needs]                                                |
|      |  (13개: Shareholder, Regulator, Customer, Employee 등)        |
|      v                                                              |
|  [Enterprise Goals]  ---- 13개 ----  (예: EG01 Portfolio Mgmt)     |
|      |                                                              |
|      v  (M: Primary / S: Secondary 매핑)                            |
|  [Alignment Goals]  ---- 13개 ----  (예: AG04 Managed Quality)     |
|      |                                                              |
|      v                                                              |
|  [Management Objectives] -- 40개 -- (5개 도메인)                    |
|      |   EDM: 05개  (Evaluate/Direct/Monitor)                       |
|      |   APO: 14개  (Align/Plan/Organize)                           |
|      |   BAI: 11개  (Build/Acquire/Implement)                       |
|      |   DSS: 06개  (Deliver/Service/Support)                       |
|      |   MEA: 04개  (Monitor/Evaluate/Assess)                       |
|      v                                                              |
|  [Process Activity -> Component -> Focus Area]                       |
|      |                                                              |
|      v                                                              |
|  [IT 구현/운영 실행]                                                 |
+---------------------------------------------------------------------+

+---------------------------------------------------------------------+
|        COBIT 2019 7대 구성요소 (Components of Governance System)    |
+---------------------------------------------------------------------+
|                                                                     |
|  ① Principles, Policies, Frameworks (원칙·정책·프레임워크)          |
|      |  예: "모든 클라우드 도입은 ISO 27017 통제 항목 충족"        |
|      v                                                              |
|  ② Processes (40개 관리목표/프로세스)                              |
|      |  예: APO12 Managed Risk, DSS02 Managed Service Requests     |
|      v                                                              |
|  ③ Organizational Structures (조직구조)                             |
|      |  예: IT Steering Committee, Architecture Review Board(ARB)  |
|      v                                                              |
|  ④ Information Flows & Items (정보 흐름)                          |
|      |  예: BSC Scorecard, IT 투자 포트폴리오 리포트                |
|      v                                                              |
|  ⑤ People, Skills & Competencies (인력·역량)                       |
|      |  예: SFIA(Skills Framework for the Information Age) Level   |
|      v                                                              |
|  ⑥ Services, Infrastructure & Applications (서비스·인프라·앱)      |
|      |  예: GRC 플랫폼(SAP GRC, ServiceNow GRC, Archer)            |
|      v                                                              |
|  ⑦ Culture, Ethics & Behavior (문화·윤리·행동)                     |
|      |  예: 코드오브컨덕트, 정보보호 인식교육 이수율 95% 이상       |
|                                                                     |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① EDM(evaluate/direct/monitor) 도메인** | 이사회·경영진의 거버넌스 책임 영역 | 5개 관리목표: EDM01 거버넌스 프레임워크 설정, EDM02 이익배분, EDM03 리스크최적화, EDM04 자원최적화, EDM05 이해관계자 투명성. 연간 분기별 **Portfolio Review Board**에서 IT 투자 포트폴리오 평가, **Stage-Gate** 프로세스로 프로젝트 단계별 Go/Kill 결정 |
| **② APO(align/plan/organize) 도메인** | 전략->전술 연결, IT 계획·조직 설계 | 14개 관리목표: APO01~14. 핵심 산출물: **IT 전략 로드맵(3~5년)**, **EA Reference Model(TOGAF 10 ADM)**, **FinOps 거버넌스 모델**(예: AWS Cost Explorer + Cloudability 통합), **정보화 사업 예비타당성조사(KISTEP, B/C 분석)**. RACI 매트릭스 25개 역할 정의 필수 |
| **③ BAI(build/acquire/implement) 도메인** | 솔루션 도입·구축·변화관리 | 11개 관리목표: BAI01~11. **SAFe(Scaled Agile Framework)** 4단계(Team/Program/Large Solution/Portfolio) 적용, **DevSecOps 파이프라인**(SAST: SonarQube, DAST: OWASP ZAP, IaC: Terraform Sentinel), **Change Advisory Board(CAB)** 운영, 배포 실패율 5% 이하 목표 |
| **④ DSS(deliver/service/support) 도메인** | 운영·서비스 데일리 | 6개 관리목표: DSS01~06. **ITIL 4 Service Value System(SVS)** 통합, **AIOps**(예: Splunk ITSI, Moogsoft) 통한 인시던트 MTTR 30% 단축, **SLA 99.95%**(연간 다운타임 4.38시간) 관리, **지식관리 시스템(KMS)** 내재화율 80% 이상 |
| **⑤ MEA(monitor/evaluate/assess) 도메인** | 모니터링·평가·감사 | 4개 관리목표: MEA01~04. **COBIT Maturity Model(NBR 5단계: Initial->Managed->Defined->Quantitatively Managed->Optimizing)** 적용, **KPI 대시보드**(예: Power BI, Grafana), **내부감사 Cycle**(연 1회 Risk-Based Audit), **Continuous Audit** 자동화 도구(ACL, IDEA) 활용 |

**핵심 알고리즘 및 산식**:

1. **TCO(Total Cost of Ownership) 산정**:
   `TCO = CapEx + (OpEx × 기간) + Hidden Cost(훈련·통합·중단비용)`
   예: SAP ERP 5년 TCO = 초기 도입비 50억 + 연간 운영비 12억 × 5 + 통합·교육 8억 = **118억 원**

2. **NPV(순현재가치) 기반 IT 투자 의사결정**:
   `NPV = Σ [CF_t / (1+r)^t] - 초기투자`
   할인율 r = WACC(Weighted Average Cost of Capital) 7.5%, NPV > 0일 때 투자 승인

3. **ROI(Return on Investment) 정량화**:
   `ROI(%) = (비용절감 + 매출증대) / IT투자액 × 100`
   TBM(Technology Business Management) 프레임워크의 **$ per FTE**, **$ per Transaction** 등 4대 KPI로 측정

4. **COBIT Maturity 산정 공식** (ISACA PAM: Process Assessment Model):
   `Process Capability = Σ(PA×%) / 100`
   PA1~PA5(Process Attribute) 가중평균 -> Level 0~5(0:Incomplete, 1:Performed, 2:Managed, 3:Established, 4:Predictable, 5:Optimizing)

5. **Risk Score 계산** (ISO 27005 / NIST SP 800-30):
   `Risk = Likelihood(1~5) × Impact(1~5)`
   예: 랜섬웨어 공격(가능성 4 × 영향 5) = **20점** -> 즉시 통제 필요(Heat Map 상위 5%)

- **📢 섹션 요약 비유**: COBIT 2019는 **자동차
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 451 / 800

<- **이전**: [450. IT 경영 관리 핵심 토픽 450번 시험 요약](/studynote/12_it_management/05_security_compliance/450_it_management_core_topic_450_exam_summary/)
**다음**: [452. IT 경영 관리 핵심 토픽 452번 시험 요약](/studynote/12_it_management/05_security_compliance/452_it_management_core_topic_452_exam_summary/) ->

---
