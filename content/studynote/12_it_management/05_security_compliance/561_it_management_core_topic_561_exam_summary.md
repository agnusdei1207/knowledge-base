+++
title = "561. IT 경영 관리 핵심 토픽 561번 시험 요약 (IT Management Core Topic 561 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 Topic 561은 COBIT 2019, ITIL 4, ISO/IEC 27001, ISO 20000을 기반으로 한 **IT 거버넌스-전략-포트폴리오-운영-감리**의 End-to-End 라이프사이클 통합 운영 체계로, Balance Score Card(BSC)·Economic Value Added(EVA)·Total Economic Impact(TEI) 등 정량/정성 지표를 연결하여 **"Value Delivery(Resource->Process->Goal)"** 체계를 정립하는 것이 본질이다.
> 2. **가치**: 도입 기업에서 IT 투자 대비 ROI 평균 25~40% 개선, IT 다운타임 60~80% 감소, 정보보안 사고 대응시간(MTTR) 70% 단축, EA 기반 중복투자 제거로 약 15~30% TCO 절감 효과가 보고되며, ISO 27001·ISMS-P 인증 취득을 통한 **규제 컴플라이언스 비용 50% 절감** 효과를 동시에 얻을 수 있다.
> 3. **판단 포인트**: 핵심 의사결정 포인트는 ① **Governance Scope** (전략 vs 운영 vs 컴플라이언스), ② **Framework 조합 전략** (COBIT 단독 vs COBIT+ITIL+ISO 통합), ③ **평가 모델 선택** (재무적 ROI vs 균형성과표 BSC vs EVA), ④ **Maturity Level 목표 설정** (CMMI 2~3 -> 4~5), ⑤ **In-House vs Outsourcing vs Hybrid** 운영 모델 결정이며, 기술사는 **"비용-위험-가치" 3축 트레이드오프**를 정량적으로 증명할 수 있어야 한다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명(AI·BigData·Cloud·IoT·Blockchain) 시대를 맞아 IT는 단순 지원조직(Back-office)에서 **전략적 핵심 동력(Strategic Differentiator)**으로 역할이 전환되었다. 그러나 한국 정보화진흥원의 「국가 정보화 백서」에 따르면 국내 대기업 IT 예산 중 **약 35~50%가 중복·비효율 투자**로 낭비되고, 정보시스템 장애로 인한 매출 손실은 연평균 72조 원 규모에 달한다. 또한 GDPR(2018), 개인정보보호법 개정(2023), AI 기본법(2025 예정), ESG 공시 의무화 등으로 **컴플라이언스·보안·지속가능성** 요구사항이 기하급수적으로 증가하고 있다.

이에 **IT 경영 관리(Information Technology Management)**는 단순한 시스템 운영을 넘어, **① IT 거버넌스·전략 기획 -> ② 투자 우선순위 결정 및 포트폴리오 관리 -> ③ 아키텍처·표준화·솔루션 도입 -> ④ 서비스 운영·성능·보안·컴플라이언스 -> ⑤ 성과 측정·감리·지속적 개선**의 5단계 End-to-End 라이프사이클을 하나의 통합 프레임워크로 관리하는 학문이다. 특히 **ISACA의 COBIT 2019**, **AXELOS의 ITIL 4**, **ISO/IEC 20000(서비스)**, **ISO/IEC 27001(보안)**, **The Open Group의 TOGAF(EA)**, **PMI의 PMBOK 7th(프로젝트)** 등 글로벌 표준을 비즈니스 전략과 IT 실행 간 **Bridging Layer**로 활용한다.

기존 **"기술 중심(Tech-driven)·사일로(Silo)식 운영"** 패러다임은 부서별 중복 구축, 불일치 데이터, 비표준 인터페이스, 책임 소재 불분명 문제를 야기했다. 이를 극복하기 위한 **"거버넌스 중심(Governance-driven)·가치 중심(Value-driven)·표준 기반(Standard-based)·지속적 개선(Continuous Improvement)"** 패러다임이 현대 IT 경영의 핵심이다.

```text
+--------------------------------------------------------------------------+
|         IT 경영 관리 패러다임 전환: Tech-Centric -> Governance-Centric    |
+--------------------------------------------------------------------------+
|                                                                          |
|  【AS-IS: 사일로형 수직 통합】          【TO-BE: 거버넌스형 수평 통합】    |
|                                                                          |
|  +----------+  +----------+  +-----+   +-----------------------------+    |
|  | 기획실   |  | 정보화   |  |감사 |   |       IT Steering Committee |    |
|  |(전략)    |  | (운영)   |  |(사후)|   |  (CIO + CFO + CEO + 외부)  |    |
|  +----+-----+  +----+-----+  +--+--+   +--------------+--------------+    |
|       |             |           |                      |                   |
|       v             v           v                      v                   |
|  중복투자 ⨯      단위운영 ⨯   사후제재 ⨯         +--------------+        |
|  비표준 ⨯        KPI부재 ⨯   책임소재 ⨯    ---->  |  Governance  |        |
|  비효율 ⨯        사일로 ⨯     개선부재 ⨯        |  Framework   |        |
|                                                   |(COBIT 2019)  |        |
|  -> 70% 예산낭비, 3배 중복구축                      +------+-------+        |
|                                                             |                |
|                                       +---------------------+---------+     |
|                                       v                     v         v     |
|                                +----------+          +----------+  +------+|
|                                |Strategy  |          |Operation |  |Risk  ||
|                                |(전략)    |          |(운영)    |  |(리스크)|
|                                | BSC/EVA  |          |ITIL 4    |  |ISO   ||
|                                | Portfolio|          |  ISO 2K  |  |27001 ||
|                                |  PMBOK   |          | DevOps   |  | NIST ||
|                                +----+-----+          +----+-----+  +--+---+|
|                                     |                     |            |    |
|                                     +----------+----------+------------+    |
|                                                v                             |
|                                  +--------------------------+                |
|                                  | Continuous Improvement   |                |
|                                  | (PDCA + Kaizen + Lean)   |                |
|                                  +--------------------------+                |
+--------------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **"도시의 통합 관제 시스템"**과 같다. 예전에는 각 구역(부서)이 각자 도로·상하수도·전기를 따로 건설(사일로 운영)했다면, 지금은 **도시계획(거버넌스) -> 표준 도로(EA) -> 통합 관제(운영) -> 시민 안전(보안) -> 성과 측정(KPI) -> 도시 개조(개선)**를 한 번에 조율하는 **"스마트 시티 운영센터"**의 역할이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 4대 핵심 축은 **① IT 거버넌스(Governance)**, **② IT 전략·투자(Strategy & Portfolio)**, **③ IT 운영·서비스(Operation & Service)**, **④ IT 리스크·컴플라이언스(Risk & Compliance)**이며, 이 4축을 **COBIT 2019의 40개 Governance & Management Objectives**로 통합 관리한다. 핵심 메커니즘은 **RACI Matrix**(책임 소재 명확화), **Balanced Scorecard BSC(4 Perspectives)**, **PDCA + Capability Maturity Model Integration(CMMI 5단계)**를 통한 가치 사슬(Value Chain) 정렬이다.

```text
+-----------------------------------------------------------------------+
|         IT 경영 관리 4축 통합 아키텍처 (COBIT 2019 기반)             |
+-----------------------------------------------------------------------+
|                                                                       |
|  【EDM Layer: Evaluate, Direct, Monitor (거버넌스 의사결정)】          |
|  +----------+----------+----------+----------+----------+              |
|  |EDM01    |EDM02    |EDM03    |EDM04    |EDM05    |              |
|  |프레임워크|전략     |리스크    |자원     |이해관계자|              |
|  |설정     |연계     |최적화   |배분     |투명성   |              |
|  +----+-----+----+-----+----+-----+----+-----+----+-----+              |
|       |          |          |          |          |                    |
|       v          v          v          v          v                    |
|  【PBR Layer: Plan, Build, Run (거버넌스 실행)】                       |
|  +----------------------------------------------------------+          |
|  |  Plan(전략)  |  Build(구축)  |  Run(운영)                |          |
|  |  APO(13)     |  BAI(11)      |  DSS(6)  |  MEA(4)       |          |
|  |  전략/포트   |  솔루션 도입  |  서비스  |  모니터링     |          |
|  |  폴리오/EA   |  변경/이행   |  지원    |  평가/감리     |          |
|  |  /혁신/위험  |  /수용/조직  |  운영/관 |  /내부통제     |          |
|  |  /자원/조달  |  /기술/정보  |  리/보안  |  /외부감사     |          |
|  +----------------------------------------------------------+          |
|       |          |          |          |                               |
|       v          v          v          v                               |
|  【Continuous Improvement Loop: PDCA + Maturity Level】                |
|  +----------+   +----------+   +----------+   +----------+            |
|  | Plan     |--->| Do       |--->| Check    |--->| Act      |--+         |
|  | (전략)   |   | (실행)   |   | (측정)   |   | (개선)   |  |         |
|  +----------+   +----------+   +----------+   +----------+  |         |
|       ^------------------------------------------------------+         |
|                                                                       |
|  【Cross-Cutting Concerns: Risk / Security / Compliance】               |
|  Risk Mgmt(ISO 31000)  |  InfoSec(ISO 27001/ISMS-P)  |  Audit          |
+-----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate·Direct·Monitor)** | 이사회의 거버넌스 의사결정 | COBIT 2019의 5개 Governance Objectives, RACI Matrix(Responsible/Accountable/Consulted/Informed) 적용, **이사회의 KPI는 "IT가 비즈니스 목표 달성에 기여했는가"**만 추적 |
| **APO (Align·Plan·Organize)** | IT 전략·포트폴리오·아키텍처·혁신·위험·자원·조달·품질·보안 계획 수립 | 13개 Management Objectives, **BSP(Business Strategic Plan) -> ISP(Information Strategic Plan) -> Project Portfolio** 3단계 연계, **TOGAF ADM(Architecture Development Method)**로 EA 수립, BSC·EVA로 KPI 설계 |
| **BAI (Build·Acquire·Implement)** | 솔루션 식별·요건정의·구축·테스트·변경관리·이행·수용 | 11개 Management Objectives, **PMBOK 7th(10 Knowledge Areas) + PRINCE2** 적용, **CI/CD Pipeline**(GitLab/Jenkins) 기반 DevOps, **Change Advisory Board(CAB)**를 통한 변경 통제, UAT·통합테스트·성능테스트·보안테스트 수행 |
| **DSS (Deliver·Service·Support)** | 서비스 운영·장애·연속성·보안·데이터·FACILITY 관리 | 6개 Management Objectives, **ITIL 4의 34개 Practices**(Service Value System) 적용, **Incident/Problem/Change/Release/Configuration** 5대 프로세스, **SLA 99.9%**(연 8.76시간 이내 다운타임), **MTBF/MTTR** 측정 |
| **MEA (Monitor·Evaluate·Assess)** | 성과 모니터링·내부통제·규제 준수·독립감사 | 4개 Management Objectives, **Balanced Scorecard 4관점**(재무·고객·내부·학습성장), **Maturity Assessment**(CMMI 1~5단계), **SOX 404 IT General Controls**, **내부감사+외부감사(회계법인) 병행** |

**핵심 알고리즘/원리 상세:**

**1) RACI Matrix (책임 소재 명확화)**
```
         R(Responsible:실행) | A(Accountable:책임) | C(Consulted:자문) | I(Informed:통보)
   --------------------------------------------------------------------------
   IT 투자 의사결정:   CEO      |    CIO    |  CFO, 외부자문   |  전 임원
   EA 표준 승인:       EA팀     |    CIO    |  사업부, ISAC    |  임원진
   보안사고 대응:      CISO     |    CEO    |  법무, 외부법무   |  IR, BOD
   SLA 위반 평가:      서비스팀  |   COO     |  사업부, 법무    |  이사
   -> RACI를 1개라도 빠뜨리면 "책임 공백(Accountability Gap)" 발생
```

**2) BSC (Balanced Scorecard) 4관점 + EVA(경제부가가치)**
```
   재무(F)    : ROI ≥ 15%, EVA > 0, IT투자당 매출 4원
   고객(C)    : 사용자만족도 ≥ 4.2/5, SLA 준수율 99.5%+
   내부(I)    : 프로젝트 성공률 80%+, 결함밀도 < 0.5/KLOC
   학습(L)    : 직원 교육시간 ≥ 60h/년, 핵심인력 유지율 90%+

   EVA = NOPAT(세후영업이익) - (투하자본 × WACC)
   -> EVA > 0: 가치창출 / EVA < 0: 가치파괴
```

**3) IT 투자 우선순위 모델 (4-Quadrant Portfolio)**
```
   고 | +----------+----------+
     | | Quick Win| Strategic|
   영| | (즉시투자)|  (전략)  |
   향| +----------+----------+
   성| |  Avoid   | Selective|
   저| | (중단/축소)|(조건부) |
     | +----------+----------+
     +-------------------------->
       저        고
       위험도/비용
```

**4) PDCA + Maturity Model (CMMI 5단계)**
```
   Level 1 (Initial)     : 작업자 능력 의존, 통제 불가
   Level 2 (Managed)     : 프로젝트별 관리, 기본 재현성
   Level 3 (Defined)     : 조직 표준 프로세스 정립
   Level 4 (Quantitatively Managed) : 정량 데이터 기반 통제
   Level 5 (Optimizing)  : 지속적 혁신 및 최적화
```

- **📢 섹션
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 561 / 800

<- **이전**: [560. IT 경영 관리 핵심 토픽 560번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/560_it_management_core_topic_560_exam_summary/)
**다음**: [562. IT 경영 관리 핵심 토픽 562번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/562_it_management_core_topic_562_exam_summary/) ->

---
