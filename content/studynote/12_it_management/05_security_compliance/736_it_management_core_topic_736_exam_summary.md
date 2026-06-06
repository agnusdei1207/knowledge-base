---
title: "IT Management Core Topic 736 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# IT 경영 관리 핵심 토픽 736번 시험 요약 (IT Management Core Topic 736)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(COBIT 2019, ISO/IEC 38500)와 전략(BSC-IT, EA-TOGAF)을 통합하여 비즈니스 가치 실현, 리스크 관리, 자원 최적화를 달성하는 경영 프레임워크 체계
> 2. **가치**: IT 투자 ROI 평균 25% 개선, IT 프로젝트 성공률 40%->75% 향상, 컴플라이언스 위반 비용 60% 절감, 의사결정 속도 3배 향상(ISO 38500 적용 기업 기준)
> 3. **판단 포인트**: 거버넌스-관리-운영 3층 분리 모델의 균형, 중앙화/분권화(Federal/Cooperative/DIT) 모델 선택, KPI 설정 시 Lag/Lead Indicator 비율(70:30), To-Be 아키텍처 전환 시 단계적 vs 빅뱅 접근법

---

## Ⅰ. 개요 및 필요성

정보기술이 기업의 핵심 경쟁력이 되면서 IT와 비즈니스 전략의 정렬(Strategic Alignment)이 경영의 핵심 과제로 부상했습니다. 전통적 IT 관리는 "시스템 가용성"과 "비용 절감"에 집중했으나, 4차 산업혁명(AI, IoT, Cloud, BigData) 시대에는 **디지털 전환(DX, Digital Transformation)** 을 주도하는 **IT 거버넌스(Governance)** 와 **IT 전략 경영(Strategic IT Management)** 이 필수 역량으로 자리잡았습니다.

기술사 시험에서는 단순 암기가 아닌, **현실 기업의 제약 조건 하에서 최적의 IT 경영 모델을 설계하고 그 트레이드오프를 논증할 수 있는 능력** 을 평가합니다. 특히 COBIT 2019의 40개 Governance/Management Objective, ISO 38500의 6원칙(Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior), 그리고 BSC-IT의 4관점(Financial, Customer, Internal Process, Learning & Growth)을 통합적으로 이해하고 있어야 합니다.

```text
+-----------------------------------------------------------------+
|        IT 경영 관리 3대 축 (Tri-Axis of IT Management)          |
+-----------------------------------------------------------------+
|                                                                 |
|   [1] 거버넌스(Governance)    [2] 관리(Management)   [3] 운영    |
|      +----------+            +----------+         +----------+ |
|      | 이사회의  |  ------->   | CIO/CTO  | -------> | IT운영팀 | |
|      | 평가/감독 |            | 계획/조율 |         | 서비스   | |
|      +----------+            +----------+         +----------+ |
|            |                       |                    |      |
|            v                       v                    v      |
|      +-----------------------------------------------------+   |
|      |  COBIT 2019 <----> ISO 38500 <----> ITIL 4 / ISO 20000|   |
|      +-----------------------------------------------------+   |
|                              |                                  |
|                              v                                  |
|      +-----------------------------------------------------+   |
|      |         BSC-IT + EA(TOGAF) + IT Portfolio           |   |
|      +-----------------------------------------------------+   |
|                                                                 |
+-----------------------------------------------------------------+
```

**Why now? (왜 지금 필요한가)**
- 기존(2000년대): **Cost Center** 관점 -> IT는 비용, 시스템 안정성 중심
- 현재(2020년대~): **Value Center / Strategic Asset** 관점 -> IT는 수익 창출, 비즈니스 혁신 주도
- 패러다임 변화: **EAM(Enterprise Architecture Management) -> 디지털 비즈니스 플랫폼 -> AI-Native Enterprise** 로 진화

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자** 와 같습니다. 첼로(현업), 바이올린(개발팀), 트럼펫(영업) 등 다양한 악기가 있을 때, 악보(전략)대로 아름다운 음악(가치)을 만들어내도록 하는 것이 바로 IT 거버넌스입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### A. IT 거버넌스 참조 모델(Governance Reference Model)

```text
+------------------------------------------------------------------+
|              COBIT 2019 Cascading Goals 메커니즘                  |
+------------------------------------------------------------------+
|                                                                  |
|  +-----------------+                                             |
|  | Stakeholder     |  13개 Enterprise Goals (EG)                 |
|  | Needs & Goals   |  • EG01 포트폴리오 최적화                   |
|  | (Needs)         |  • EG04 정보 및 기술 자산의 품질            |
|  +--------+--------+  • EG11 최적의 IT 운영 위험 관리            |
|           |                                                       |
|           v  +----------------------------------+                |
|  Goals    |  | Alignment Goals (AG) 13개        |                |
|  Cascade  |  | AG01 IT 준수/지원 방안 일치       |                |
|           |  | AG05 IT 비용/이익 실현            |                |
|           |  | AG11 I&T 위험 관리                |                |
|           v  +--------------+-------------------+                |
|  +-----------------+         |                                   |
|  | Enterprise Goals|---------+                                   |
|  | (EG) 13개       |                                             |
|  +--------+--------+                                             |
|           |                                                       |
|           v                                                       |
|  +----------------------------------+                             |
|  | Governance & Management Obj.    | 40개(GO:5, M:35)           |
|  |  • EDM(Governance) 5개         | • APO(Align, Plan, Org) 14 |
|  |  • BAI(Build, Acq, Impl) 11개  | • DSS(Deliver, Service, Spt)|
|  |  • MEA(Monitor, Eval, Assess) 4|                             |
|  +--------+---------------------+                               |
|           |                                                       |
|           v                                                       |
|  +----------------------------------+                             |
|  | Component: Process/Org/Info/    |                             |
|  |  People/Skills/Infrastructure/  |                             |
|  |  Apps & Services (7요소)        |                             |
|  +----------------------------------+                             |
|                                                                  |
+------------------------------------------------------------------+
```

### B. IT 전략 실행 체계(Strategy Execution System)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **BSC-IT (Balanced Scorecard)** | 전략 맵핑, KPI 정량화 | 4관점(Financial 23%, Customer 22%, Internal Process 34%, L&G 21% 가중치) + 17~25개 KPI 설정, Lag/Lead 지표 70:30 비율 |
| **EA(Enterprise Architecture)** | To-Be 아키텍처 청사진 | TOGAF ADM 8단계(Phase A~H: Preliminary->Vision->Business->Info System->Technology->Opportunities->Migration->Impl Govern) |
| **IT Portfolio Management** | 투자 우선순위 결정 | Bubble Chart(위험-가치 2x2), NPV/IRR/Payback 분석, Stage-Gate 프로세스 |
| **Governance Board** | 의사결정 및 감독 | IT Steering Committee 월 1회, IT Architecture Review Board 분기 1회, Change Advisory Board(CAB) 주 1회 |
| **Service Management (ITIL 4)** | 운영 품질 관리 | 34개 Practice, Service Value System(SVS), Value Chain(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support) |

### C. 핵심 원리 및 알고리즘

**1) COBIT 2019 Focus Area + Design Factor 매트릭스**
```
Enterprise Strategy Design Factors:
+- Strategy (Growth/Innovation/Cost Leadership/...)
+- Goals(Enterprise Goals 13개 우선순위)
+- Risk Profile
+- I&T Related Issues
+- Design Factors × 11개 -> Governance System 40목표 우선순위 산출
```

**2) IT 투자 우선순위 결정 모델 (Weighted Scoring Model)**
```
우선순위 = Σ(가중치_i × 점수_i)
   = (전략정합도 0.30 × 10) + (ROI 0.25 × 8) + (위험도 0.15 × 6 역산)
   + (규제준수 0.15 × 9) + (실현가능성 0.15 × 7)
   = 3.0 + 2.0 + 0.9 + 1.35 + 1.05 = 8.30 / 10
```
**허용 기준**: ≥7.0 (투자 승인), 5.0~6.9 (조건부 승인), <5.0 (보류/폐기)

**3) ISO/IEC 38500 EDIM( Evaluate-Direct-Monitor) 3단계 사이클**
- **Evaluate**: IT 사용의 적절성, 효과성 평가
- **Direct**: 책임, 전략, 획득, 성과, 적합, 인간행동 6원칙에 부합하는 지시
- **Monitor**: 지시사항 이행 및 성과 모니터링

- **📢 섹션 요약 비유**: IT 경영 시스템은 **자동차의 계기판과 같습니다**. 속도계(BSC KPI), 연료계(ROI), 엔진 온도계(리스크), 내비게이션(EA)을 통해 운전자가 한눈에 차량 상태를 파악하고 방향을 결정하는 것처럼, IT 거버넌스 체계는 경영진이 IT의 모든 상태를 실시간으로 파악하도록 합니다.

---

## Ⅲ. 비교 및 연결

### A. 거버넌스 프레임워크 비교

| 구분 | **COBIT 2019** | **ISO/IEC 38500** | **ITIL 4** | **CMMI** |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스/관리 통합 | IT 의사결정 거버넌스 원칙 | IT 서비스 운영 최적화 | 프로세스 성숙도 평가 |
| **대상** | 이사회~운영 전 계층 | 이사회/경영진 고위층 | IT 운영/서비스팀 | 개발/운영 조직 |
| **구조** | 40 Governance/Management Obj. | 6 원칙 + EDIM 모델 | 34 Practice + SVS | 5단계 성숙도(Initial~Optimizing) |
| **측정** | Capability Level 0~5 / Process Rating | 원칙별 준수율 | KPI/SLA/CSI | Practice Area 별 성숙도 |
| **강점** | 비즈니스-IT 정렬, 컴플라이언스 | 법·규제 준수, 간결성 | 서비스 품질, 고객가치 | 프로세스 개선, 정량적 |
| **약점** | 복잡도, 도입 비용 | 추상적, 실행 가이드 부족 | 거버넌스 측면 약함 | IT 거버넌스 관점 부족 |
| **상호보완** | ISO 38500 원칙 ↔ COBIT 목표 | COBIT 2019와 매핑 | COBIT DSS 도메인과 연결 | COBIT BAI06과 매핑 |

### B. IT 조직 거버넌스 모델 비교

| 구분 | **중앙집중형(Centralized)** | **연방형(Federal/CoIT)** | **분산형(Decentralized)** | **하이브리드(DIT)** |
| :--- | :--- | :--- | :--- | :--- |
| **구조** | CIO 직할 단일 IT 조직 | 본사 IT + 현업 IT 공존 | 현업별 독립 IT | 전략-거버넌스 본사, 운영 분산 |
| **장점** | 표준화, 규모의 경제, 통제 용이 | 현업 대응성, 유연성 | 사업별 최적화, 민첩성 | 거버넌스 일관성 + 운영 민첩성 |
| **단점** | 현업 대응 느림, 병목 | 이원화, 갈등 | 중복투자, 표준 부재 | 거버넌스-운영 경계 모호 |
| **적합 조직** | 규제금융, 공공기관 | 대기업 다사업부 | M&A 다수 그룹사 | 디지털 전환 추진 기업 |
| **비용 효율** | 높음(중복 제거) | 중간 | 낮음(중복 多) | 높음~중간 |

### C. 다른 시스템과의 연결

```text
+--------------------------------------------------------------+
|                IT 경영 관리 통합 아키텍처                     |
+--------------------------------------------------------------+
|                                                              |
|  +-------------+  +-------------+  +------------------+   |
|  | BPM/BPR     |  | ERP(SC      |  | CRM/SFA          |   |
|  | 프로세스 혁신|  | M/HR/FI)    |  | (고객/영업)      |   |
|  +------+------+  +------+------+  +--------+---------+   |
|         +-----------------+-------------------+              |
|                           v                                  |
|              +-----------------------------+                |
|              |   EA(Enterprise Architecture) |               |
|              |   TOGAF / Zachman Framework  |                |
|              +--------------+--------------+                |
|                             v                                 |
|   +-----------------------------------------------------+   |
|   |  IT 거버넌스(COBIT 2019) + 전략(BSC-IT)            |   |
|   |  -------------------------------------              |   |
|   |  • 거버넌스 위원회  • KPI 대시보드                  |   |
|   |  • 투자 포트폴리오  • 위험 관리                    |   |
|   +--------------+--------------------------------------+   |
|                  v                                             |
|   +------------------------------------------------------+  |
|   |  IT 서비스 운영 (ITIL 4 + DevOps + SRE)             |  |
|   |  • Incident/Problem/Change Management               |  |
|   |  • CI/CD Pipeline, AIOps, Observability             |  |
|   +------------------------------------------------------+  |
|                                                              |
+--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: COBIT, ISO 38500, ITIL의 관계는 **헌법-법률-시행령** 의 관계와 같습니다. 헌법(ISO 38500)이 큰 원칙을 정하고, 법률(COBIT)이 구체적 목표를 설정하며, 시행령(ITIL)이 현장의 실행 절차를 다룹니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### A. IT 경영 관리 구축 절차 (Roadmap)

```text
[1단계: 진단] --> [2단계: 설계] --> [3단계: 구축] --> [4단계: 운영]
  4~8주            8~12주         12~24주         지속
   |                 |               |              |
   v                 v               v              v
• As-Is 분석      • To-Be 설계     • 파일럿     • 지속 개선
• Gap Analysis   • KPI/BSC        • 확산       • KPI 모니터링
• Stakeholder   • 거버넌스 체계   • 교육       • 연 1회 평가
  Interview      • RAC
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 736 / 800

<- **이전**: [735. IT 경영 관리 핵심 토픽 735번 시험 요약](/studynote/12_it_management/05_security_compliance/735_it_management_core_topic_735_exam_summary/)
**다음**: [737. IT 경영 관리 핵심 토픽 737번 시험 요약](/studynote/12_it_management/05_security_compliance/737_it_management_core_topic_737_exam_summary/) ->

---
