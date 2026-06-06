---
title: "IT Management Core Topic 527 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(COBIT 2019, ISO 38500)와 디지털 전환(DX) 전략을 연결하여, **전략(Strategy) -> 포트폴리오(Portfolio) -> 아키텍처(EA/TOGAF) -> 운영(ITIL 4) -> 측정(BSC/KPI)**의 5계층 정렬(Alignment) 체계를 확립하는 것이 핵심이다.
> 2. **가치**: 정량적으로는 IT 투자 ROI를 평균 15~30% 개선하고, Time-to-Market을 40~60% 단축하며, 정성적으로는 **"전략-실행-성과" 갭(Strategy Execution Gap)**을 해소하여 이사회 수준 거버넌스 투명성을 확보한다.
> 3. **판단 포인트**: Build vs. Buy vs. Cloud(Public/Private/Hybrid), 중앙화(Centralized) vs. 분권화(Federated/Bimodal IT), 그리고 **거버넌스 강도(Strict/Lean)** 사이의 균형을 잡아야 하며, 특히 **레거시 잔존률(Legacy Debt Ratio)**과 **혁신 투자 비중(Innovation Ratio: 전체 IT 예산 대비 20~30%)**을 핵심 지표로 관리해야 한다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(Digital Transformation, DX)은 단순히 기술을 도입하는 것이 아니라, **비즈니스 모델·프로세스·조직·문화·기술**을 동시에 재설계하여 데이터 기반 의사결정과 고객 가치 창출을 극대화하는 경영 패러다임의 전환이다. 코로나19(COVID-19) 이후 가속화된 **VUCA(Volatility, Uncertainty, Complexity, Ambiguity) 환경**에서, 한국 정보화진흥원(NIA)의 「2023 디지털 전환 실태조사」에 따르면 국내大中型 기업의 **73%가 DX를 추진 중**이나, 이 중 **성공률은 24% 수준**에 불과하여 전략적 거버넌스 부재가 최대 실패 요인으로 보고되고 있다.

기존의 **전통적 IT 운영 모델(Silo·Project-driven·Capex 중심)**은 부서별 단편적 시스템 투자로 인해 다음 3대 문제에 직면한다:

1. **전략 미스얼라인먼트(Strategic Misalignment)**: CEO는 디지털 혁신을 원하지만, CIO는 레거시 유지보수에 70% 이상의 예산과 인력을 투입
2. **레거시 잠재부채(Technical Debt)**: 15년 이상 운영된 COBOL·EIS 기반의 기간계 시스템이 클라우드·API·데이터 분석과 단절
3. **거버넌스 백서(Governance Vacuum)**: 이사회-경영진-IT 간의 의사결정 구조가 부재하여, DX 실패 시 책임 소재 불명 및 투자 회수 불가

이를 해결하기 위해, **COBIT 2019(Control Objectives for Information and Related Technologies)**의 **거버넌스 시스템(Governance System)**과 **ISO/IEC 38500:2015 IT 거버넌스 표준**을 기반으로, **EA(Enterprise Architecture) -> BPM(Business Process Management) -> ITSM(IT Service Management)**을 통합하는 **"Digital Governance Framework"**가 요구된다.

```text
+----------------------------------------------------------------------+
|            디지털 전환 거버넌스 프레임워크 (DGF) 전체 구조            |
+----------------------------------------------------------------------+
                              |
   +--------------------------v--------------------------+
   |        1) 전략 정렬 (Strategy Alignment Layer)       |
   |   - ESG/DX Vision & Roadmap  - BSC(균형성과표)        |
   |   - McKinsey 3 Horizons  - BCG/Porter 전략 모델      |
   +--------------------------+--------------------------+
                              |  (정량 KPI 연결: NPV, ROI, NPS)
   +--------------------------v--------------------------+
   |        2) 포트폴리오 관리 (Portfolio Layer)           |
   |   - 3-년 IT 투자 로드맵  - 우선순위 매트릭스         |
   |   - Run/Grow/Transform (RGT) 비율 관리               |
   |   - Innovation Ratio ≥ 20%, Legacy ≤ 30%            |
   +--------------------------+--------------------------+
                              |  (선정/의사결정: Stage-Gate)
   +--------------------------v--------------------------+
   |        3) 아키텍처 거버넌스 (EA Layer)               |
   |   - TOGAF 10 ADM  - Zachman Framework 6×6           |
   |   - SOA -> Microservices -> Cloud-Native 진화         |
   |   - API Gateway, Service Mesh, Data Mesh             |
   +--------------------------+--------------------------+
                              |  (설계/표준화: Reference Model)
   +--------------------------v--------------------------+
   |        4) 운영 및 서비스 (IT Operations Layer)        |
   |   - ITIL 4 (34 Practices)  - DevOps + SRE           |
   |   - SLA 99.9%, MTTR < 30min, Change Success ≥ 95%   |
   |   - FinOps, Observability (OpenTelemetry)           |
   +--------------------------+--------------------------+
                              |  (서비스 전달/모니터링)
   +--------------------------v--------------------------+
   |        5) 측정 및 개선 (Measurement Layer)           |
   |   - KPI 대시보드  - CSF(Critical Success Factor)     |
   |   - COBIT 2019 Cascade Goals  - PDCA + OODA Loop    |
   +------------------------------------------------------+
                              |
                              v
              [지속적 혁신 및 피드백 루프 -> 전략 재조정]
```

- **📢 섹션 요약 비유**: DX 거버넌스는 마치 **"건물의 내진설계(Seismic Design)"**와 같다. 지진(DX 변동)이 발생해도 1층(전략)부터 5층(측정)까지의 기둥-보 구조가 일체로 흔들려도 무너지지 않도록, 모든 층을 동일한 강도(Governance Strength)로 설계해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 거버넌스 시스템의 5개 도메인

COBIT 2019는 **EDM(평가, 지시, 모니터링) + 4개 도메인(APO, BAI, DSS, MEA)** 총 **40개 관리 목표(Management Objective)**로 구성되며, **"Governance System Principles(거버넌스 시스템 6원칙)"**와 **"Governance Framework Principles(프레임워크 5원칙)"**을 통해 고객별 맞춤화가 가능하다.

```text
+--------------------------------------------------------------------+
|                  COBIT 2019 Core Model 상세 흐름도                  |
+--------------------------------------------------------------------+
+--------------------------------------------------------------------+
|  EDM: Evaluate, Direct and Monitor (거버넌스 영역, 5개 목표)        |
|  ----------------------------------------------------------------  |
|  EDM01  거버넌스 프레임워크 수립 및 유지                             |
|  EDM02  혜택 실현(Delivery of Benefits)                             |
|  EDM03  위험 최적화(Risk Optimization)                              |
|  EDM04  자원 최적화(Resource Optimization)                          |
|  EDM05  이해관계자 투명성 확보(Stakeholder Transparency)            |
+--------------------------------+-----------------------------------+
                                 |  (전략 의도 -> 실무 지시)
   +-----------------------------v-----------------------------+
   |  APO: Align, Plan and Organize (정렬/계획, 14개 목표)      |
   |  APO01~14  전략, 포트폴리오, 예산, 인적자원, 위험, 보안 등  |
   +-----------------------------+-----------------------------+
                                 |
   +-----------------------------v-----------------------------+
   |  BAI: Build, Acquire and Implement (구축, 11개 목표)        |
   |  BAI01~11  솔루션 선정, 설계, 구축, 시험, 변경, 이행 등      |
   +-----------------------------+-----------------------------+
                                 |
   +-----------------------------v-----------------------------+
   |  DSS: Deliver, Service and Support (운영, 6개 목표)          |
   |  DSS01~06  SLA, 보안, 문제, 데이터, 인시던트, 연속성         |
   +-----------------------------+-----------------------------+
                                 |
   +-----------------------------v-----------------------------+
   |  MEA: Monitor, Evaluate and Assess (측정, 4개 목표)          |
   |  MEA01~04  성과, 내부통제, 외부감사, 준수                      |
   +-------------------------------------------------------------+
```

### 2. 핵심 구성 요소 및 동작 방식

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회(Board) / CDO·CIO** | 거버넌스 의사결정 주체 | **COBIT EDM01**: 거버넌 시스템의 최종 책임, 비전·원칙·정책 승인, 정량 목표(NPV ≥ 12%, NPS ≥ 30) 설정 |
| **전략기획팀(SPM)** | DX 로드맵 수립 | **McKinsey 3 Horizons 모델** 적용: H1(현 사업 강화) 70%, H2(신규 사업) 20%, H3(미래 씨앗) 10% 자원 배분 |
| **PMO(Project Mgmt Office)** | 포트폴리오 관리 | **Stage-Gate 프로세스**: Idea -> Business Case -> Plan -> Build -> Deploy -> Close, 각 게이트에서 ROI 재검증 |
| **EA(Enterprise Architecture) 팀** | 아키텍처 표준·통제 | **TOGAF 10 ADM(Architecture Development Method)** 8단계(Phase A~H) 적용, As-Is -> To-Be 갭 분석, **ArchiMate 3.2** 모델링 언어 사용 |
| **IT 운영(Ops) / SRE** | 서비스 제공·개선 | **ITIL 4 Service Value System(SVS)**: 34개 Best Practice 중 Incident(9%), Change(11%), Problem(7%) 관리, **MTTR < 30분, 가용성 99.95%** |
| **보안·컴플라이언스(GRC)** | 통제 및 위험 관리 | **ISO 27001:2022**(93개 통제 항목), **ISO 38500**, **개인정보보호법(PIPA)**, **ESG 공시 기준(TCFD/SASB)** 적용 |
| **데이터 거버넌스 위원회** | 데이터 자산 관리 | **Data Catalog + Lineage + Quality(Fit-for-Purpose)** + **DAMA-DMBOK 2.0** 11개 지식 영역 적용 |
| **측정·감사팀** | 성과 측정 및 보고 | **BSC 4관점(재무/고객/프로세스/학습) + COBIT Cascade Goals + GRC 대시보드**로 통합 리포팅 |

### 3. 핵심 알고리즘 및 의사결정 공식

- **RGT(Resource) 배분 비율** (Gartner 권장):
  $$\text{Run : Grow : Transform} = 60 : 25 : 15 \sim 50 : 30 : 20$$
  - Run(운영): 60% 이하로 압축 (legacy 자동화·클라우드 전환 시 절감)
  - Grow(현 사업 강화): 25~30%
  - Transform(혁신): 15~20% 이상 확보 (매년 5%씩 증액 목표)

- **DX 투자 NPV(Net Present Value)**:
  $$NPV = \sum_{t=1}^{n} \frac{(B_t - C_t)}{(1+r)^t} - I_0$$
  - $B_t$: 디지털화로 인한 매출/비용 절감, $C_t$: 운영비, $r$: WACC(8~12%), $I_0$: 초기 투자
  - **Hurdle Rate**: NPV ≥ 0, IRR ≥ WACC + 3%, payback ≤ 5년

- **플랫폼 전환 ROI(예: SAP -> S/4HANA Cloud)**:
  $$ROI = \frac{(\text{TCO 절감} + \text{비즈니스 기회 가치}) \times 0.7 - \text{전환 비용}}{\text{전환 비용}} \times 100$$
  - 실제 사례: 현대자동차의 SAP S/4HANA 전환 시 **TCO 28% 절감, 프로세스 처리 속도 65% 향상**

- **COBIT 2019 Maturity 모델(0~5등급)**:
  - L0(Incomplete) -> L1(Initial) -> L2(Managed) -> L3(Defined) -> L4(Quantitative) -> L5(Optimizing)
  - 목표: 핵심 도메인(EDM/BA
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 527 / 800

<- **이전**: [526. IT 경영 관리 핵심 토픽 526번 시험 요약](/studynote/12_it_management/05_security_compliance/526_it_management_core_topic_526_exam_summary/)
**다음**: [528. IT 경영 관리 핵심 토픽 528번 시험 요약](/studynote/12_it_management/05_security_compliance/528_it_management_core_topic_528_exam_summary/) ->

---
