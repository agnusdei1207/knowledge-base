+++
title = "641. IT 경영 관리 핵심 토픽 641번 시험 요약 (IT Management Core Topic 641 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 Topic 641은 COBIT 2019, ISO 38500, ITIL 4, PMBOK 7, ISO 31000, ISO 27001 등 글로벌 거버넌스·관리 프레임워크를 BSC(균형성과표)·TCO·ROI·NPV·IRR·BAI·BCM 등 정량 지표와 통합하여, IT 전략 수립-이행-평가-개선(Plan-Do-Check-Act) 전 과정을 Value Delivery·Risk Optimization·Resource Optimization 3대 균형으로 운영 통제하는 종합 영역이다.
> 2. **가치**: McKinsey·Gartner·IDC 통계에 따르면 체계적 IT 거버넌스 도입 기업은 IT 투자 대비 ROI 25~40% 향상, IT 장애로 인한 매출 손실 50%v, 핵심 인력 생산성 30%^, 규제 컴플라이언스 위반 리스크 70%v 효과를 거둘 수 있으며, ISO/IEC 38500·COBIT 인증 기업은 자본시장에서 P/E 배수 평균 1.2~1.8배 프리미엄이 산정된다.
> 3. **판단 포인트**: 기술사 답안 작성 시 (1) 거버넌스-관리-운영 3계층(Governance-Management-Operational) 분리, (2) "One Size Fits All" 회피 및 Design Factor 11개 기반 COBIT 2019 맞춤 설계, (3) Agile/DevOps 환경에서의 ITIL 4 SVS(Service Value System) 적용, (4) 정성·정량 혼합 KPI와 CSF(Critical Success Factor) 도출, (5) Risk Appetite·Tolerance·Capacity 3단계 기준 명확화 여부가 핵심 채점 포인트다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명·클라우드·AI·메타버스 전환기에서 IT는 더 이상 비용 센터(Cost Center)가 아닌 전략적 비즈니스 Enabler이자 Value Creator로 재정의되었다. 그러나 한국 정보화진흥원(2023) 조사에 따르면 국내 대기업의 67%가 "IT-Biz 정렬 부재", 58%가 "IT 투자 효과 미계측", 45%가 "이해관계자 간 거버넌스 충돌"을 고충으로 호소한다. 이는 단순한 기술 부재가 아닌 **경영·관리·운영·감리 4계층을 관통하는 통합 프레임워크 부재**가 근본 원인이다.

Topic 641(IT 경영 관리 종합)은 다음 6대 Pain Point를 해결하기 위해 고안된 시험 영역이다:
- **전략 부재**: CEO/CIO 간 "번아웃·사일로" - IT 전략과 사업 전략 미연계
- **투자 비효율**: 그린필드 IT 프로젝트의 35%가 예산 초과·일정 지연(CHAOS Report 2023, Standish Group)
- **리스크 은폐**: 전사적 리스크 관리(ERM) 부재로 사이버 보안·컴플라이언스 사고 시연 발생
- **서비스 품질 저하**: SLA 미달성률 평균 23%, MTTR 4.2시간, MTTD 28일
- **규제 대응 실패**: 개인정보보호법, ESG, EU AI Act, DORA 등 규제 복잡도 300%^
- **성과 측정 불가**: IT 성과가 CFO·이사회에 정량 보고되지 않아 "Black Box"화

```text
[IT 경영 관리 Topic 641 통합 프레임워크 구조도]

                    +-------------------------------------+
                    |   이사회/CEO (최고 의사결정기구)        |
                    |  +----------+  +----------+         |
                    |  |Risk Comm.|  |Audit Comm.|         |
                    |  +----+-----+  +-----+----+         |
                    +-------+--------------+--------------+
                            |              |
              +-------------v--------------v-------------+
              |  ① IT 거버넌스 계층 (Governance)         |
              |  - ISO 38500 · COBIT 2019 · King IV     |
              |  원칙:책임(R)·전략(S)·취득(A)·성과(P)    |
              |         인적자원(H)·준법(C)              |
              +-------------+----------------------------+
                            |
              +-------------v----------------------------+
              |  ② IT 관리 계층 (Management)             |
              |  - BSC · PMO · PPM · ITFM               |
              |  정렬: 전략->포트폴리오->프로젝트->운영      |
              |  KPI: ROI, EVA, TCO, NPV, BCM RTO/RPO   |
              +-------------+----------------------------+
                            |
              +-------------v----------------------------+
              |  ③ IT 운영 계층 (Operations)             |
              |  - ITIL 4 SVS · DevOps · SRE · AIOps    |
              |  34 Practice · Service Value Chain       |
              +-------------+----------------------------+
                            |
              +-------------v----------------------------+
              |  ④ IT 감리/평가 계층 (Audit/Assurance)   |
              |  - COBIT 2019 Cascade · SSAE 18(SOC)    |
              |  ISACA CISA · 내부통제(ISO 27001)        |
              +------------------------------------------+

[이전 vs 새로운 IT 경영 패러다임]

  Before (1990~2010)              After (2010~현재, VUCA/BANI 시대)
  -----------------              ---------------------------------
  Cost Center                    Value Creator / Business Partner
  IT = Data Processing           IT = Digital Ecosystem Engine
  CapEx 중심 일회성 투자          OpEx + CapEx 혼합, Pay-as-you-go
  Waterfall 일방향              Agile + Bimodal + DevOps + Platform
  내부 시스템 폐쇄                하이퍼컨버지드·멀티클라우드·API화
  ROI/TCO 정량만                 BSC + ESG + CX + Innovation Score
  컴플라이언스 사후 대응          Privacy by Design, Zero Trust
  사업부서 종속                  Co-creation, Citizen Developer
```

**기존 대비 핵심 변화**:
- **Moore's Law -> Metcalfe's Law**: 자산 가치 = 노드², 네트워크 효과 극대화
- **CAPEX -> OPEX + Subscription**: Cloud FinOps로 비용 가시성 확보
- **Project-oriented -> Product-oriented**: Spotify Squad·Tribes 모델
- **Annual Planning -> Continuous Adaptive Planning**: OKR 분기별 갱신
- **Risk Avoidance -> Risk Intelligent**: 리스크를 회피가 아니라 활용(예: AI 실험)

- **📢 섹션 요약 비유**: IT 경영 관리를 **"배의 항해"**에 비유하면, IT 거버넌스는 "항해의 목적지·윤리강령", IT 관리는 "선장·항해도", ITIL 운영은 "선원·엔진룸", IT 감리는 "해운안전공단의 정기검사"입니다. 4계층 중 어느 하나라도 무너지면 배는 표류합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 641번 토픽은 **5대 글로벌 표준/프레임워크**를 축으로 구성되며, 각각은 다른 관점(거버넌스·프로세스·서비스·리스크·프로젝트)에서 상호 보완한다.

```text
[Topic 641 5대 프레임워크 상호작용 메커니즘]

       +-----------------------------------------------+
       | ISO/IEC 38500 (IT 거버넌스 국제표준)            |
       |   6 Principles : R·S·A·P·H·C (6원칙)         |
       |   5 Tasks : Evaluate·Direct·Monitor           |
       +--------------------+--------------------------+
                            | (거버넌스 목표 -> 관리 체계로 전환)
       +--------------------v--------------------------+
       | COBIT 2019 (거버넌스·관리 목표 통합체계)         |
       |   40 Governance & Management Objectives       |
       |   11 Design Factors (맞춤형 설계)              |
       |   7 Components (목표/원칙/정책/프로세스/조직/    |
       |                  정보/문화/인력/서비스)         |
       |   Cascading Goals (Enterprise->Alignment->       |
       |                     Component Goals)          |
       +-----+--------------+--------------+-----------+
             |              |              |
   +---------v---+  +-------v------+  +----v---------+
   | PMBOK 7 /   |  |  ITIL 4 SVS  |  |  ISO 31000/  |
   | PRINCE2 /   |  |  (서비스)    |  |  27001/27701 |
   | CMMI /Agile |  |  34 Practice |  |  (리스크·보안)|
   +-------------+  +--------------+  +--------------+
             |              |              |
   +---------v--------------v--------------v-----------+
   |   전사적 KPI 측정 (BSC 4관점)                       |
   |   Financial·Customer·Internal Process·            |
   |   Learning & Growth                              |
   +--------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **ISO/IEC 38500** | IT 거버넌스 최상위 국제표준(ISO/IEC JTC1/SC40) | 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)과 3개 Govern 프로세스(Evaluate, Direct, Monitor)로 이사회-경영진-ICT운영의 책임·권한 명확화. PDCA와 달리 EDM 사이클(Evaluate 의사결정·Direct 실행·Monitor 성과측정) 채택 |
| **COBIT 2019** | 40개 거버넌스·관리 목표(40 GO/MO)와 7개 컴포넌트 기반 통합 모델 | Design Factor 11개(기업전략·윤리문화·위험도·역량·복잡도 등) 입력 시 권장 프로세스·역할·메트릭 자동 산출. Goals Cascade로 전사목표->정렬목표->컴포넌트목표 3단계 위계 정렬. Process Capability 평가는 PAM(Process Assessment Model) 기반 6레벨(0~5) |
| **ITIL 4 SVS** | IT 서비스 관리(Service Management) 최신 프레임워크 | SVS(Service Value System) = Opportunity/Demand->Value<-IT 자산. Service Value Chain(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve) 6활동. **34 Best Practice**(Information Security Management, Change Enablement, Incident Management, Service Desk, Continual Improvement 등) |
| **PMBOK 7 / PRINCE2 / CMMI** | 프로젝트·프로그램·포트폴리오 관리(PPM) 표준 | PMBOK 7은 **8개 Performance Domain**(Stakeholders, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty)과 12개 Principle. PRINCE2는 7 Principle·7 Process·7 Theme. CMMI v2.0은 5 Level·20 Practice Area |
| **ISO 31000/27001/27701** | 리스크·정보보안·프라이버시 관리 국제표준 | ISO 31000은 Risk Framework(원칙·프레임워크·프로세스), 27001은 Annex A 93 통제항목(ISMS), 27701은 PIMS로 27001 확장. Risk = Threat × Vulnerability × Impact(Annual Loss Expectancy = Asset × Exposure × Single Loss Expectancy) |

### 핵심 산식·알고리즘 (기술사 답안 필수 암기)

**1) IT 투자 정량 평가 4종**
```
TCO (Total Cost of Ownership) = 직접비(HW·SW·인건비) + 간접비(교육·Downtime·보안·전력)
ROI (%) = (총이익 - 총비용) / 총비용 × 100, Payback = 초기투자 / 연간현금흐름
NPV = Σ[CFt / (1+r)^t] - 투자금,  NPV > 0 이면 투자 타당
IRR = NPV = 0 되는 할인율 r,  IRR > hurdle rate 이면 승인
EVA = NOPAT - (WACC × 투자자본),  지속 가능 진정한 경제적 부가가치
```

**2) BSC 4관점 -> IT KPI 예시**
```
Financial:  IT 비용/매출, OPEX/CAPEX, ROI, Cost per User
Customer:   CSAT/NPS, First Contact Resolution, 가용성(%), MTTR
Internal:   Deployment Frequency, Change Failure Rate, MTTD, MTTR
L&G:        직원 역량(Skill Index), Innovation Index, Patent 수
```

**3) COBIT 2019 Process Capability 산식 (ISO/IEC 330xx PAM)**
```
Capability Level (0~5): Incomplete(0)->Performed(1)->Managed(2)->Defined(3)
                        ->Quantitatively Managed(4)->Optimizing(5)
Process Attribute Achievement = Σ(Practice Fulfillment + Generic Resource)
Target Capability ≥ 3 (Defined) 권장, 전체 40 Objective 평균 산정
```

**4) Risk Quantification 3종**
```
ALE(Annual Loss Expectancy) = SLE × ARO,  SLE = AV(Asset Value) × EF(Exposure Factor)
RPN(Risk Priority Number) = S(심각도) × O(발생빈도) × D(탐지율),  RPN > 100 즉시 대응
CVSS 3.1 = Base(8.0) × Temporal × Environmental, 9.0^ Critical
```

- **📢 섹션 요약 비유**: 5대 프레임워크는 **"오케스트라 악기"**에 비유할 수 있습니다. ISO 38500은 "지휘자(거버넌스)", COBIT 2019는 "악보(통합관리 체계)", ITIL 4는 "바이올린(서비스 품질)", PMBOK은 "드럼(프로젝트 리듬)", ISO 31000/27001은 "방음벽(리스크 차단)". 지휘자 없이 악기만 있으면 불협화음, 지휘자만 있고 악기 없으면 침묵.

---

## Ⅲ. 비교 및 연결

### Framework 간 상세 비교

| 구분 | ISO/IEC 38500 | COBIT 2019 | ITIL 4 SVS | PMBOK 7 | ISO 31000 |
|:---|:---|:---|:---|:---|:---|
| **발행/주관** | ISO(2015, 2nd) | ISACA(2018, evolved) | AXELOS(2019) | PMI(2021) | ISO(2018) |
| **주 대상** | 이사회·경영진 | 거버넌스·관리자 | IT 실무자·운영 | PM·PgM·PfM | 전사 리스크 관리자 |
| **계층** | 거버넌스(상위) | 거버넌스+관리 | 운영·서비스 | 프로젝트·프로그램 | 전사 리스크 |
| **핵심 구조** | 6 Principle / 3 Task | 40 GO/MO / 7 Component / 11 Design Factor | SVS / 34 Practice / Value Chain | 8 Domain / 12 Principle | Framework
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 641 / 800

<- **이전**: [640. IT 경영 관리 핵심 토픽 640번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/640_it_management_core_topic_640_exam_summary/)
**다음**: [642. IT 경영 관리 핵심 토픽 642번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/642_it_management_core_topic_642_exam_summary/) ->

---
