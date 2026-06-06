---
title: "IT Management Core Topic 791 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019, ISO/IEC 38500, ITIL 4 등 글로벌 IT 거버넌스 프레임워크를 기반으로 IT 전략·투자·운영·성과·리스크·준수(SPOFC) 6대 영역을 비즈니스 가치(Value Realization)와 정렬시키는 경영 통제 체계이며, 최근에는 ESG·AI 거버넌스·양자 보안까지 확장되는 디지털 시대의 핵심 통제 인프라이다.
> 2. **가치**: McKinsey·Gartner 조사에서 디지털 전환(DX) 성공 기업의 ROI는 평균 2.5배, TCO는 20~30% 절감, IT 투자 의사결정 속도는 40% 향상되며, COBIT 적용 조직의 리스크 대응 시간은 50% 단축되는 정량적 효과가 입증되었다.
> 3. **판단 포인트**: 조직 성숙도(CMM 1~5단계)에 따른 거버넌스-경영-운영 3계층(Govern-Build-Run) 균형, EA(TOGAF/Zachman)와 ITSM(ITIL 4)의 통합, Shadow IT·관료주의·과도한 KPI 등 안티패턴 회피, 그리고 규제 환경(K-ISMS, GDPR, CSAP)에 맞는 통제 설계가 기술사의 핵심 판단 기준이다.

---

## Ⅰ. 개요 및 필요성

**IT 경영 관리(Enterprise IT Governance & Management)**는 단순히 "IT 부서를 잘 관리한다"는 차원을 넘어, **기업의 미션·전략·전술·운영 계층 전체에서 IT 자원과 디지털 역량을 최적의 비즈니스 가치로 변환**하는 경영학적 통제 체계이다. 4차 산업혁명(AI, IoT, 클라우드, 빅데이터, 블록체인, 메타버스)이 가속화되면서 전통적인 "비용 중심의 IT 운영"에서 "데이터·플랫폼·생태계 중심의 가치 중심 IT 경영"으로 패러다임이 근본적으로 전환되었다.

2020년 코로나19 팬데믹 이후 전 세계적으로 **재택근무·비대면 비즈니스·원격 의료·원격 교육**이 보편화되면서, IT는 더 이상 "지원 조직(Back Office)"이 아닌 **"사업 생존의 핵심 동력(Mission Critical)"**이 되었다. 이로 인해 C-Level(CEO, CFO, COO, CDO, CIO, CISO)의 IT 의사결정 참여 비중이 급증하였고, **IT 거버넌스(Governance)와 IT 관리(Management)의 분리**가 필수적인 경영 통제 요구사항으로 대두되었다.

또한 EU GDPR(2018), 한국 개인정보보호법 개정(2023), 클라우드 보안인증(CSAP), EU AI Act(2024) 등 **규제 환경의 급격한 변화**로 인해 IT는 "법적 리스크의 1차 방어선"이 되었으며, ESG(환경·사회·지배구조) 평가에서 **정보보호 및 AI 윤리 지표**가 신규 평가 항목으로 편입되면서 IT 경영의 범위는 지속적으로 확장되고 있다.

```text
+---------------------------------------------------------------------+
|        IT 경영 관리의 진화 패러다임: 4단계 디지털 전환 프레임        |
+---------------------------------------------------------------------+
|                                                                     |
|  [1960s-1980s]      [1990s-2000s]       [2010s]           [2020s+] |
|   EDP 시대         ERP/전산실 시대    클라우드·모바일    AI·플랫폼 시대|
|       |                 |                  |                  |   |
|       v                 v                  v                  v   |
|  +----------+      +----------+       +----------+      +--------+|
|  | Data     |      | Process  |       | Service  |      | Value  ||
|  | Processing| ---> | Autom.   | --->  | Oriented  | --->  | Driven ||
|  | Cost Center|     |Cost->Profit|      |Shared Svcs|      |Digital ||
|  +----------+      +----------+       +----------+      +--------+|
|                                                                     |
|  통제 방식:    수작업       문서/매뉴얼     SLA·ITIL    DevOps·SRE |
|  거버넌스:    무         CobiT v3-v5    COBIT 5/2019  COBIT+ESG |
|  조직:        전산실       SI/IT부서       CDO·CIO     BizDevOps|
|  ROI측정:     무          TCO절감        KPI기반     가치기반  |
+---------------------------------------------------------------------+
```

**기존 패러다임 vs 새로운 패러다임 비교:**

| 항목 | 전통적 IT 경영(2000년대) | 디지털 시대 IT 경영(2024~) |
|---|---|---|
| **관점** | IT 비용 절감·효율화 | 데이터·플랫폼·생태계 가치 창출 |
| **구조** | 수직적·계층적(전산실 중심) | 수평적·네트워크형(CoE·BizDevOps) |
| **거버넌스** | ITIL v2/v3, COBIT 4.1 | COBIT 2019, ISO 38500, NIST CSF 2.0 |
| **리더십** | CIO(1인 책임) | CDO·CTO·CISO·CDO·CIO **집단 리더십** |
| **투자 기준** | NPV·IRR·Payback Period | NPV + 플랫폼 외부효과 + ESG 임팩트 |
| **KPI** | 가용성 99.9%, 처리량 TPS | NPS, Time-to-Market, 데이터 자본화율 |
| **리스크** | 시스템 장애·정보유출 | 공급망·AI 편향·딥페이크·양자 해독 |
| **규제** | ISMS, ISO 27001 | K-ISMS, GDPR, DORA, AI Act, CSAP |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"도시의 도시계획(Urban Planning)"**과 같다. 도로·상하수도·전력·통신 인프라를 무작정 짓는 것이 아니라, 인구·경제·환경·안전을 고려한 **종합 마스터플랜** 아래 통합 설계·건설·운영·재개발되어야 시민 삶의 질이 향상된다. IT도 마찬가지로, **전략(도시 마스터플랜) -> 아키텍처(토지이용계획) -> 운영(공공서비스) -> 평가(도시 지표)**가 하나의 통합 체계로 작동해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**COBIT 2019(Control Objectives for Information and Related Technologies)**는 현재 가장 널리 통용되는 IT 거버넌스·관리 통합 프레임워크이다. 핵심은 **"기업의 목적(Enterprise Goals)을 IT 관련 목표(Alignment Goals)로 변환하고, 이를 거버넌스·관리 목표(Governance/Management Objectives)로 분해하여 40개 구성요소(Components) 간의协業을 통해 달성"**하는 것이다.

```text
+--------------------------------------------------------------------+
|                    COBIT 2019 6대 거버넌스 시스템 원칙              |
+--------------------------------------------------------------------+
| ① 각 기업 요구사항에 맞게 시스템 조정 (맞춤형)                      |
| ② 적용 범위는 기업 전체로 포괄 (End-to-End)                       |
| ③ 거버넌스 시스템 적용 (Governance≠Management 분리)               |
| ④ 거버넌스 시스템 요소 간 일관성 (40 Components)                   |
| ⑤ 비즈니스와 IT 간의 동적 상호작용                                |
| ⑥ 가장 중요한 것은 비즈니스 가치(Realization)                      |
+--------------------------------------------------------------------+
            |  ① Principles -> ② Goals Cascade -> ③ Component
            v
+--------------------------------------------------------------------+
|  [1단계] Enterprise Goals  -- 매핑(13개)                          |
|          (재무/고객/내부/성장/규제)                                |
|              |  +---------------------------------+                |
|              v  | Goals Cascade (Top-Down 5단 변환) |              |
|  [2단계] Alignment Goals -- 13개 (AG01~AG13)                       |
|          (IT 전략/서비스/보안/아키텍처/혁신)                       |
|              |  +---------------------------------+                |
|              v  |                                  |                |
|  [3단계] Governance & Mgmt Objectives -- 40개 (EDM01~DSS06)     |
|          EDM(5) / APO(14) / BAI(11) / DSS(6) / MEA(4)            |
|              |  +---------------------------------+                |
|              v  |                                  |              |
|  [4단계] Component Variants -> Organizational Specific Configuration|
|          (Process/Structure/People/Skills/Information/Service/    |
|           Infrastructure/Applications) × N개 기업                 |
+--------------------------------------------------------------------+
            |  운영 시:
            v
  +-----------------+  +-----------------+  +-----------------+
  |  GOVERNANCE     |  |   MANAGEMENT    |  |   OPERATION     |
  |  (이사회·CxO)   |  |  (IT·Biz Middle) |  |  (End User)     |
  |  EDM: Evaluate, |  |  APO/BAI/DSS     |  |  실제 서비스     |
  |  Direct, Monitor|  |  Plan/Build/Run   |  |  사용·개선 제안  |
  +-----------------+  +-----------------+  +-----------------+
```

| 구성 요소 (COBIT 2019 40대 Component) | 역할 | 핵심 기술·동작 방식 |
| :--- | :--- | :--- |
| **① Process (프로세스)** | 거버넌스·관리 활동의 절차 정의 | EDM/APO/BAI/DSS/MEA 5도메인 40목표, RACI Chart, 입력->활동->출력->메트릭 |
| **② Organizational Structures (조직구조)** | 의사결정 권한과 보고 체계 | 이사회(Board) -> CISO/CIO/CFO -> IT Steering Committee -> PMO -> 운영팀, **3 Lines of Defense(3 LoD)** 모델 |
| **③ Information (정보 항목)** | 의사결정에 필요한 데이터 자산 | Goals Cascade 메트릭, KRI(핵심리스크지표), KPI(핵심성과지표), CSF(핵심성공요인) 4계층 매트릭스 |
| **④ People, Skills & Competencies** | 역량 정의·검증 | SFIA(Skills Framework for Information Age) 7레벨, SF v6 기반 직무기술서(JD), e-CF(European e-Competence Framework) 5레벨 |
| **⑤ Policies & Procedures** | 정책·절차 표준화 | IT Policy Hierarchy: Charter->Policy->Standard->Guideline->Procedure 5계층, RACI 매트릭스 |
| **⑥ Culture, Ethics & Behavior** | 거버넌스 문화 | 윤리강령(Code of Ethics), 톤 앳 더 탑(Tone at the Top), **행동 규범(Behavioral Norms)** |
| **⑦ Services, Infrastructure & Applications** | 기술적 지원 수단 | 클라우드(AWS/Azure/GCP), ITSM 플랫폼(ServiceNow, Jira SM), GRC 도구(Archer, SAP GRC) |
| **⑧ People (사람)** | 역할·책무 담당자 | RACI(Responsible/Accountable/Consulted/Informed), **Three Lines of Defense** (1st: 운영, 2nd: 리스크·컴플라이언스, 3rd: 내부감사) |

**COBIT 2019 5개 도메인 상세 (총 40개 관리목표):**
- **EDM (Evaluate, Direct, Monitor) - 5개**: 거버넌스 의사결정 (EDM01~05)
- **APO (Align, Plan, Organize) - 14개**: 전략·계획·조직 (APO01~14)
- **BAI (Build, Acquire, Implement) - 11개**: 솔루션 도입·구축 (BAI01~11)
- **DSS (Deliver, Service, Support) - 6개**: 운영·지원 (DSS01~06)
- **MEA (Monitor, Evaluate, Assess) - 4개**: 성과 평가·측정 (MEA01~04)

**BSC(Balanced Scorecard) 기반 IT 성과관리 4관점:**
1. **재무관점(Financial)**: IT 예산 준수율, IT 투자 ROI, IT 운영비용/매출 비율
2. **고객관점(Customer)**: SLA 준수율, 사용자 만족도(NPS), 인시던트 해결시간(MTTR)
3. **내부 프로세스(Internal Process)**: 변경 성공률, 결함 누출률, 프로세스 자동화율
4. **학습·성장(Learning & Growth)**: 직원 역량지수, 교육 이수시간, 혁신 아이디어 수

**IT 투자 평가 핵심 수식:**
- **TCO(Total Cost of Ownership)**: `TCO = 직접비용(HW/SW) + 간접비용(운영·교육·다운타임) + 기회비용(잠재손실)`
- **ROI(Return on Investment)**: `ROI = (총이익 - 총비용) / 총비용 × 100%`
- **NPV(Net Present Value)**: `NPV = Σ[CF_t / (1+r)^t] - 초기투자` (r=할인율, CF=현금흐름)
- **IRR(Internal Rate of Return)**: `NPV=0`이 되는 할인율 r (투자안 의사결정 시 NPV>0, IRR>자본비용)
- **Payback Period(회수기간)**: `ΣCF_t ≥ 초기투자`가 되는 최소 t
- **EVA(Economic Value Added)**: `EVA = NOPAT - (WACC × 투자
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 791 / 800

<- **이전**: [790. IT 경영 관리 핵심 토픽 790번 시험 요약](/studynote/12_it_management/05_security_compliance/790_it_management_core_topic_790_exam_summary/)
**다음**: [792. IT 경영 관리 핵심 토픽 792번 시험 요약](/studynote/12_it_management/05_security_compliance/792_it_management_core_topic_792_exam_summary/) ->

---
