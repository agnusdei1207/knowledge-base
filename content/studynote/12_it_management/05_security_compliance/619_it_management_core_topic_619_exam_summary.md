+++
title = "619. IT 경영 관리 핵심 토픽 619번 시험 요약 (IT Management Core Topic 619 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019, ITIL 4, ISO 38500, PMBOK 7th** 등 글로벌 거버넌스 프레임워크를 **EA(Enterprise Architecture)·BCM·정보화 사업 평가**와 통합하여, IT 투자 대비 **사업 가치(ROI/NPV)·리스크·적합성**을 정량적으로 통제하는 **IT-비즈니스 정렬(IT-Business Alignment)** 체계이다.
> 2. **가치**: McKinsey & Company 연구에 따르면 효과적인 IT 거버넌스 도입 기업은 **IT 비용 20~30% 절감, 프로젝트 성공률 35% -> 75% 향상, Time-to-Market 40% 단축**, ISO 38500 인증 기업의 경우 **이사회-경영진-현업 간 IT 의사결정 속도 2.3배 개선** 효과를 거둘 수 있다.
> 3. **판단 포인트**: 중앙집중형(COBIT 기반) vs 분산형(DevOps/Agile 거버넌스) 간의 **Governance-Autonomy 트레이드오프**, 단기 ROI 추구 vs 장기 디지털 전환 투자, 정량 KPI(가용성·MTTR·CSAT) vs 정성 효과(혁신·문화), 그리고 **클라우드·AI·제로트러스트** 등 신기술 도입 시 발생하는 Shadow IT·데이터主权 리스크 통제 수준이 핵심 결정 변수가 된다.

---

## Ⅰ. 개요 및 필요성

최근 5년간 국내 기업 환경은 **DX(Digital Transformation), ESG 공시 의무화, 클라우드 전환, 생성형 AI 도입** 등 4대 메가트렌드가 동시에 진행되면서 IT의 역할이 단순 비용센터(Cost Center)에서 **전략적 사업 파트너(Value Center)**로 급격히 전환되었다. 하지만 한국정보화진흥원의 「2023년 국내 정보화 실태조사」에 따르면 국내 대기업의 **58.2%가 IT-비즈니스 정렬 실패를 경험**했고, 정보화 사업의 **37.4%가 예산 초과, 42.1%가 기대 효과 미달** 상태로 종료되었다. 중소·중견기업은 IT 인력 부족(평균 3.2명)과 전문성 한계로 **Shadow IT가 전체 IT 자산의 약 23.7%**까지 자생적으로 확산되어 보안·컴플라이언스 리스크를 야기하고 있다.

이러한 문제의 근본 원인은 **IT 경영 관리 체계의 부재**이다. IT는 더 이상 시스템 운영만으로는 가시적 가치를 증명할 수 없으며, **전략 기획 -> 투자 우선순위화 -> 아키텍처 설계 -> 구현·운영 -> 성과 측정 -> 개선**의 전生命周期(Lifecycle)을 거버넌스 프레임워크로 통제해야 한다. 본 토픽 619번은 기술사 시험이 요구하는 **"IT를 경영의 핵심 동력으로 전환하기 위한 거버넌스·전략·성과·리스크 통합 관리 역량"**을 평가하기 위해 설계된 종합 영역이다.

```text
+----------------------------------------------------------------------+
|           IT 경영 관리 통합 프레임워크 (Topic 619) 전체 구조도         |
+----------------------------------------------------------------------+
|                                                                      |
|   +----------------+         +---------------------+                |
|   | ① IT 전략기획  |◄-------►|  사업전략 / ESG    |                |
|   |  (ISP 수립)    |         |  요구사항 도출      |                |
|   +--------+-------+         +---------------------+                |
|            | SWOT, TOGAF, Balanced Scorecard                         |
|            v                                                         |
|   +----------------+    거버넌스 의사결정 (RACI)                      |
|   | ② IT 거버넌스  |◄---------------------------------+             |
|   |  (COBIT 2019)  |                                   |             |
|   +--------+-------+                                   |             |
|            | Goal Cascade                              |             |
|            v                                           |             |
|   +----------------+    +----------+  +----------+    |             |
|   | ③ EA / 투자   |---►| ④ 구현   |-►| ⑤ 운영   |    |             |
|   |   포트폴리오   |    | (PMBOK,  |  | (ITIL 4, |    |             |
|   |  관리          |    |  Agile)  |  |  AIOps)  |    |             |
|   +--------+-------+    +----------+  +----+-----+    |             |
|            |                                |          |             |
|            |          +---------------------v--+       |             |
|            |          | ⑥ 성과측정·평가         |       |             |
|            +---------►|    (KPI/BSC/BSI)       |-------+             |
|                       +------------------------+                     |
|                                  |                                   |
|                                  v                                   |
|                       +------------------------+                     |
|                       | ⑦ 리스크·컴플라이언스   |                     |
|                       |  (ISO 27001, ISMS-P,    |                     |
|                       |   ISO 38500, BCP/DR)    |                     |
|                       +------------------------+                     |
+----------------------------------------------------------------------+
```

기존의 **프로젝트 단위 IT 관리(Project-centric)**에서는 각 사업이 silo 형태로 운영되어 **중복 투자(전사 평균 18%), 사일로 시스템(애플리케이션 통합성 32% 수준), 사후 정산 통제(End-of-pipe Control)** 등의 한계를 노출했다. 반면, **포트폴리오·전사 차원의 IT 경영 관리**는 전략·아키텍처·투자·성과·리스크의 5대 축을 **PDCA + Balanced Scorecard** 루프로 통합 운영하여, **사전 예방 거버넌스(Front-end Governance)**와 **데이터 기반 의사결정(Data-Driven Decision Making)**을 가능하게 한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자**와 같다. 첼로, 바이올린, 트럼펫(각 부서·시스템)들이 제각각 연주하면 불협화음만 나지만, COBIT 2019라는 악보와 ITIL 4라는 박자, PMBOK이라는 파트별 주법표를 통해 **지휘자(이사회·CIO)가 통합 리허설을 진행**해야만 하나의 아름다운 symphony(사업 가치)가 완성된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. IT 거버넌스 3대 축: Decision-Making Framework

ISO 38500:2015(Information technology — Governance of IT)는 IT 거버넌스를 **3대 영역(Evaluate, Direct, Monitor)** × **6대 원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior)**의 매트릭스로 정의한다. 이를 실무에 적용할 때 가장 많이 활용되는 구체화 모델이 **COBIT 2019**이다. COBIT 2019는 **40개 Governance & Management Objective(관리 목표)**, **구조화된 메커니즘(원칙, 정책, 프레임워크, 프로세스, 조직구조, 정보, 인적자원, 기술, 시설)**, **Focus Area(중점 영역)** 개념을 도입하여 **클라우드 거버넌스, 사이버보안 거버넌스, DevOps 거버넌스, ESG-IT 거버넌스** 등 50여 개의 산업별·기술별 확장을 지원한다.

```text
+------------------------------------------------------------------+
|                COBIT 2019 Cascading Goals 구조                    |
|                                                                  |
|  +------------------------------------------------------+        |
|  |        Enterprise Goals (13개)                       |        |
|  |  EG01 포트폴리오, EG02 컴플라이언스, EG03 성과, ... |        |
|  +--------------------+---------------------------------+        |
|                       | Alignment Goal Mapping                   |
|                       v                                          |
|  +------------------------------------------------------+        |
|  |   Alignment Goals (13개) - IT-Business 정렬 목표     |        |
|  |   AG01 IT 준거성, AG04 품질, AG09 정보처리혁신...    |        |
|  +--------------------+---------------------------------+        |
|                       | Goal Cascade                             |
|                       v                                          |
|  +------------------------------------------------------+        |
|  |   Management Objectives (40개)                        |        |
|  |   EDM01~05 (Evaluate, Direct, Monitor)               |        |
|  |   APO01~14 (Align, Plan, Organize) - 거버넌스 핵심    |        |
|  |   BAI01~11 (Build, Acquire, Implement)               |        |
|  |   DSS01~06 (Deliver, Service, Support)               |        |
|  |   MEA01~04 (Monitor, Evaluate, Assess)               |        |
|  +--------------------+---------------------------------+        |
|                       | Process Activity Mapping                 |
|                       v                                          |
|  +------------------------------------------------------+        |
|  |  Components: 7가지 메커니즘 (원칙/정책/프로세스/조직/  |        |
|  |  정보/사람/기술/서비스인프라) + Design Factors (10개) |        |
|  +------------------------------------------------------+        |
+------------------------------------------------------------------+
```

### 2. IT 전략 기획 및 EA(Enterprise Architecture) 연계

**TOGAF 10(2023년 Release)**의 ADM(Architecture Development Method) 8단계와 **COBIT 2019의 APO02(Strategy)**를 결합하여, **비즈니스 동기(Business Motivation Model) -> IT 원칙 -> 아키텍처 비전 -> Baseline/Target Architecture -> 이행 로드맵 -> 거버넌스 솔루션**을 도출한다. 특히 **ArchiMate 3.2** 표준 모델링 언어로 **Business Layer–Application Layer–Technology Layer**의 3-Layer 관계를 표현하며, 최신 **TOGAF 10**에서는 **Digital-Business Agility, Sustainability, Data Mesh**를 신규 영역으로 추가했다.

### 3. IT 투자·포트폴리오 관리 (PfM)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ISP(Information System Plan)** | 3~5년 IT 중장기 로드맵 | BSC 4관점(재무/고객/내부/학습성장) 기반 KPI 도출, 총 IT 예산 100% 항목화 |
| **APP(Application Portfolio)** | 레거시 현대화 의사결정 | **TIME 모델**(Tolerate/Invest/Migrate/Eliminate), Gartner Magic Quadrant, 기술 부채 정량화(Technical Debt = `복잡도 × 영향도 / 코드 품질`) |
| **IT 거버넌스 위원회** | 투자 우선순위 의결 | **RACI 매트릭스**(Responsible, Accountable, Consulted, Informed), 월 1회 사이클, 포트폴리오 균형(70-20-10 법칙: 운영 70% / 개선 20% / 혁신 10%) |
| **EA Repository** | 아키텍처 자산 통합 관리 | **ArchiMate, BPMN 2.0, UML 2.5** 모델 통합, **LeanIX / MEGA HOPEX / BOC ADOIT** 도구 활용, 메타데이터 카탈로그 자동화 |
| **성과 측정 체계(BSI)** | IT 서비스·프로젝트 성과 정량화 | BSC, KPI Tree, OKR(Objective-Key Results), NPV/IRR, Payback Period, TCO 모델링 |
| **리스크·컴플라이언스** | 정보보안·규제 준수 통합 | **ISO 27001(정보보안), ISO 37301(컴플라이언스), ISMS-P, PCI-DSS, GDPR/개인정보보호법**, 3Lines of Defense(1LoD: 현업, 2LoD: IT/보안, 3LoD: 내부감사) |

### 4. 핵심 알고리즘·수식

**(1) IT 투자 우선순위화 점수화 모델**:
```
Priority Score = w1 × StrategicFit + w2 × RiskReduction
                + w3 × FinancialBenefit + w4 × ImplementationFeasibility
                + w5 × RegulatoryCompliance
where Σwi = 1.0, weighted AHP(Analytic Hierarchy Process) 기반
```

**(2) 레거시 시스템 기술부채 정량화**:
```
Technical Debt (TD) = ∑(Code Smell × Remediation Cost)
                    + Architectural Debt (Cyclomatic Complexity > 15 기준)
                    + Test Coverage Deficit (목표 80% 미만분)
```

**(3) IT 서비스 가용성·신뢰성 지표**:
```
Availability = (MTBF / (MTBF + MTTR)) × 100
SLA Compliance = Σ(Uptime / Contracted Uptime) / 측정 기간
MTTR = Mean Time To Repair
MTBF = Mean Time Between Failures
RPO(Recovery Point Objective) = 허용 가능한 데이터 손실 시점
RTO(Recovery Time Objective) = 허용 가능한 서비스 중단 시간
```

**(4) 정보화 사업 성과 종합 평가(BSI 점수)**:
```
성과점수 = 0.3 × 전략성공도 + 0.3 × 사업성공도 + 0.4 × 결과성공도(DeLone & McLean IS Success Model 확장)
```

- **📢 섹션 요약 비유**: IT 거버넌스 3대 축(평가-지휘-감시)은 마치 **자동차의 브레이크-액셀러레이터-미러**와 같다. COBIT이 미러(현실), ITIL이 액셀러레이터(속도), ISO 27001이 브레이크(안전)인데, 기술사는 이 셋을 **한 발판 위에서 동시에 밟는 전문 운전자**여야 한다.

---

## Ⅲ. 비교 및 연결

### 1. 글로벌 IT 거버넌스·관리 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **PMBOK 7th** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | IT 거버넌스·관리 목표 달성 | IT 서비스 운영·관리 표준 | 이사회 수준 IT 거버넌스 원칙 | 프로젝트 관리 지식체계 | 전사 아키텍처 개발 방법론 |
| **주 사용자** | CIO, 거버넌스 위원회, 감사 | IT 운영팀, 서비스 데스크 | 이사회, CEO, CIO | 프로젝트 관리자(PM) | EA 아키텍트, CIO |
| **구성 요소** | 40개 관리목표 + 7 메커니즘 | 34개 Service Practice | 3
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 619 / 800

<- **이전**: [618. IT 경영 관리 핵심 토픽 618번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/618_it_management_core_topic_618_exam_summary/)
**다음**: [620. IT 경영 관리 핵심 토픽 620번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/620_it_management_core_topic_620_exam_summary/) ->

---
