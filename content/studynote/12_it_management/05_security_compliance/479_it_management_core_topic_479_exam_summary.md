---
title: "479. IT 경영 관리 핵심 토픽 479번 시험 요약 (IT Management Core Topic 479 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019(40개 관리목표·5도메인), ITIL 4(34개 실무·SVS), ISO 38500(6원칙)을 통합한 3계층 의사결정-책임-통제 체계로, EDM(평가·지휘·모니터) -> PBR(계획·구축·운영) -> Risk/Security/Compliance 순환 구조를 통해 디지털 자산의 가치 실현과 리스크 최적화를 동시에 달성하는 경영 프레임워크이다.
> 2. **가치**: McKinsey/ISACA 실증 연구 기준으로 IT-Business 전략 정렬도 65%->92% 향상, Shadow IT 비용 18~27% 절감, IT 투자 ROI 2.4배 개선, 정보보안 사고 대응시간(MTTR) 62% 단축, ISMS-P·GDPR·ESG 컴플라이언스 감사 적격성 100% 확보 효과가 입증되었다.
> 3. **판단 포인트**: 중앙집중형 CoE(Center of Excellence) vs 분산형 Federation 모델, Top-down(Mission->Strategy->Portfolio) vs Bottom-up(Service Catalog) KPI 역전 설계, BSC 4관점(재무·고객·내부·학습) 인과관계 사슬의 정합성, 그리고 사이버보안·AI 윤리·ESG를 거버넌스 한 축으로 편입할지 여부가 핵심 의사결정 변수이다.

---

## Ⅰ. 개요 및 필요성

2020년 이후 전 세계 IT 지출은 연간 8.4%씩 성장하여 2026년 5.4조 USD에 도달했으며(Statista, 2025), 코로나19 팬데믹을 기점으로 원격근무, SaaS 전환, 생성형 AI 도입이 폭증하면서 **그림자 IT(Shadow IT)**가 평균 기업의 IT 자산 대비 30~40%에 이른다(Gartner, 2024). 그러나 CEO의 73%만이 IT 투자 효과에 확신을 가지며, CIO의 64%는 비즈니스 요구와 IT 역량 간 갭을 호소한다(Deloitte Global CIO Survey, 2024).

이러한 **전략-실행 갭(Strategy-Execution Gap)**과 **가치-리스크 비대칭(Value-Risk Asymmetry)**이 심화되면서, IT를 단순 비용센터(Cost Center)가 아닌 **전략적 가치 창출 파트너(Value Driver)**로 재정의할 수 있는 통합 거버넌스 체계의 필요성이 대두되었다. 과거(1990~2010)의 ITIL v2/v3 중심 **프로세스 거버넌스**에서 벗어나, 2019년 COBIT 2019 발표를 기점으로 **원칙-목표-컴포넌트 3축의 유연한 거버넌스 시스템**으로 패러다임이 전환되었다.

```text
+--------------------------------------------------------------------------+
|           정보화 시대 (1990~2010)        vs    디지털 시대 (2019~현재)    |
+--------------------------------------------------------------------------+
|  +---------------------+                  +-----------------------------+|
|  | • ITIL v2/v3        |                  | • COBIT 2019 + ITIL 4       ||
|  | • 프로세스 중심      |                  | • 원칙+목표+컴포넌트 3축     ||
|  | • 중앙 통제형        |                  | • 분산형 Federation 지원    ||
|  | • IT 거버넌스 ≒ 보안 |                  | • IT 거버넌스 ≒ 가치경영   ||
|  | • CapEx 중심        |                  | • OpEx + SaaS + AI/ML      ||
|  +---------------------+                  +-----------------------------+|
|   문제: Shadow IT 35%, ROI 측정 불가,           문제: AI 거버넌스, 데이터  |
|         비즈니스 정렬 실패 70%                            주권, ESG 통합  |
+--------------------------------------------------------------------------+
```

기존 **"IT는 비용이다"**라는 인식에서 **"IT는 전략 자산이다"**로의 전환은, 무형자산(Intangible Asset) 비율이 S&P 500 기업의 90%를 넘어선 시대(2020년 Ocean Tomo 연구)에서 더 이상 선택이 아닌 **경영 생존 조건**이 되었다. ISO/IEC 38500(2015)은 IT 거버넌스를 "기관의 이사회가 IT를 어떻게 지휘·감독하는지를 결정하는 시스템"으로 정의하며, 단순한 기술 관리를 넘어 **법적·윤리적 책임(Ethical IT Stewardship)** 영역으로 확장시켰다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **도시의 종합规划设计**와 같다. 상위 도시는 5년/10년/20년 **종합계획(Master Plan)**, 중간은 **용도지역·건축허가(COBIT 목표)**, 하위는 **교통·전기·상하수도 인프라 운영(ITIL 서비스)**이 3층 구조로 맞물려 돌아가야 시민(비즈니스)이 안전하고 효율적인 삶을 누린다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스의 3계층 아키텍처는 국제 표준 3종(COBIT 2019, ITIL 4, ISO 38500)과 BSC/KPI 체계, 그리고 사이버보안 컴플라이언스(ISMS-P, NIST CSF, ISO 27001)가 수직·수평으로 통합된 **메타-거버넌스(Meta-Governance)** 구조이다.

```text
                 +---------------------------------+
                 |  Tier 1: 전략 거버넌스 (ISO 38500) | <- 이사회/CEO
                 |  R-S-A-P-C-H 6원칙                |
                 |  • Responsibility (책임)          |
                 |  • Strategy (전략)                |
                 |  • Acquisition (획득)             |
                 |  • Performance (성과)             |
                 |  • Conformance (준수)             |
                 |  • Human Behavior (인간행동)      |
                 +---------------------------------+
                                     | EDM (Evaluate, Direct, Monitor)
                                     v
                 +---------------------------------+
                 |  Tier 2: 코어 거버넌스 (COBIT 2019)| <- CIO/CDO/CISO
                 |  • 5도메인 × 40관리목표 × 7컴포넌트|
                 |  • EDM(05)  APO(14)  BAI(11)      |
                 |  • DSS(06)   MEA(04)              |
                 +---------------------------------+
                                     | PBR (Plan/Build/Run)
                                     v
                 +---------------------------------+
                 |  Tier 3: 운영 거버넌스 (ITIL 4)   | <- 서비스매니저/엔지니어
                 |  • 34 실무 × SVS(Value Chain)    |
                 |  • 7 Guiding Principles          |
                 |  • 4 Dimension Model             |
                 +---------------------------------+
                                     |
              +----------------------+----------------------+
              v                                              v
   +----------------------+                    +------------------------+
   | 보안·컴플라이언스 거버넌스|                    |  데이터·AI 거버넌스    |
   | • ISMS-P, ISO 27001   |                    |  • DAMA-DMBOK          |
   | • NIST CSF 2.0        |                    |  • AI Act (EU 2024)    |
   | • GDPR/PIPA           |                    |  • 개인정보보호법       |
   +----------------------+                    +------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate-Direct-Monitor)** | 전략 거버넌스의 3단계 의사결정 사이클 | COBIT 2019 EDM 도메인의 5개 관리목표(EDM01~05)로 이사회 책임을 분해; OCEG GRC(Governance-Risk-Compliance) RedBook과 연계하여 3개월 단위 의사결정 사이클 운영 |
| **APO (Align-Plan-Organize)** | IT 전략-비즈니스 정렬 및 포트폴리오 관리 | 14개 관리목표(APO01~14); Strategic Fit 분석, TOGAF ADM(Architecture Development Method)과 결합하여 EA(Enterprise Architecture) 매핑 |
| **BAI (Build-Acquire-Implement)** | 솔루션 도입 및 변경 관리 | 11개 관리목표(BAI01~11); DevSecOps 파이프라인, SAFe 스케일링 방법론, 발주자 관점 SW사업관리 가이드(2024) 적용 |
| **DSS (Deliver-Service-Support)** | 서비스 운영 및 사용자 지원 | 6개 관리목표(DSS01~06); AIOps, Observability(OpenTelemetry), SRE 4 Golden Signals |
| **MEA (Monitor-Evaluate-Assess)** | 성과 측정 및 감사 | 4개 관리목표(MEA01~04); CMMI v2.0 평가, BSC 4관점 KPI, GRC 대시보드(SAP GRC, ServiceNow IRM) |
| **ITIL 4 SVS (Service Value System)** | 가치 창출 운영 체계 | 7 Guiding Principles(Focus on value, Start where you are, Progress iteratively...); Service Value Chain(Plan->Engage->Design->Obtain->Build->Deliver->Improve) |
| **BSC 4관점 KPI** | 전략-운영 지표 연결 | 재무(ROI, TCO), 고객(NPS, SLA 준수율), 내부프로세스(MTTR, Change Success Rate), 학습·성장(직원 역량, Innovation Index) — **인과관계 사슬** 검증 필수 |
| **Risk & Compliance 엔진** | 리스크 정량화 및 컴플라이언스 | ISO 31000 리스크 프로세스(식별->분석->평가->처리->모니터링), VaR(Value at Risk)·ALE(Annual Loss Expectancy) 정량화, K-Risk(국가망), DORA(EU 2025) 대응 |

COBIT 2019의 **7가지 컴포넌트(7 Components of a Governance System)**는 거버넌스 시스템 설계 시 반드시 검토해야 할 차원으로, ① Process(프로세스), ② Organizational Structures(조직구조), ③ Information Flow(정보흐름), ④ People, Skills, Competencies(인재역량), ⑤ Policies and Procedures(정책절차), ⑥ Culture, Ethics, Behavior(문화윤리), ⑦ Services, Infrastructure, Applications(서비스인프라)로 구성된다. 이 중 ④·⑥번은 정량 측정이 어려워 **CSF(Critical Success Factor)와 KGI(Key Goal Indicator)** 설계를 별도 수립해야 한다.

**BSC 인과관계 사슬의 예시**:
```
학습·성장: AI 역량 보유 엔지니어 +20%
        v
내부프로세스: AIOps 기반 MTTR 단축 -> 4시간->1.5시간
        v
고객: SLA 99.9%->99.99% 달성, NPS +15pt
        v
재무: 다운타임 비용 -$2.3M/년, IT ROI 2.4배
```

- **📢 섹션 요약 비유**: 3계층 거버넌스는 **국가 운영 체제**와 같다. 국회(이사회)가 법률(원칙)을 제정하고, 행정부(CIO)가 정책(목표)을 수립하며, 각 부처(서비스매니저)가 민원(서비스)을 처리한다. 그리고 감사원(MEA)과 법원(컴플라이언스)이 이를 감독한다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **PMBOK 7** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | IT 거버넌스·관리 통합 프레임워크 | IT 서비스 관리 최적화 | IT 거버넌스 6원칙 | 프로젝트 관리 지식체계 | EA(엔터프라이즈 아키텍처) |
| **구조** | 5도메인
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 479 / 800

<- **이전**: [478. IT 경영 관리 핵심 토픽 478번 시험 요약](/studynote/12_it_management/05_security_compliance/478_it_management_core_topic_478_exam_summary/)
**다음**: [480. IT 경영 관리 핵심 토픽 480번 시험 요약](/studynote/12_it_management/05_security_compliance/480_it_management_core_topic_480_exam_summary/) ->

---
