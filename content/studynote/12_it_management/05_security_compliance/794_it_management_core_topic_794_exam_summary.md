+++
title = "794. IT 경영 관리 핵심 토픽 794번 시험 요약 (IT Management Core Topic 794 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 794. IT 경영 관리 핵심 토픽 794번 시험 요약 (IT Management Core Topic 794)

> **주제**: IT 거버넌스 및 전략적 IT 관리 (IT Governance & Strategic IT Management)
> **적용 프레임워크**: COBIT 2019, ITIL 4, ISO/IEC 38500, ISO/IEC 20000

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 EDM(평가·지시·모니터링) 5단계 프로세스와 비즈니스 목표(Business Goals) 매핑을 통해 IT 투자 대비 비즈니스 가치 실현(Value Realization)을 정량화하는 의사결정·책임·통제 구조
> 2. **가치**: McKinsey 2023 보고 기준 IT 거버넌스 성숙도 Level 5 도달 시 디지털 전환 성공률 67%->89%, IT 예산 효율성 23% 개선, IT 위험으로 인한 손실 41% 감소
> 3. **판단 포인트**: 중앙집중·연방(Federal)·분산(Federated) 거버넌스 모델의 조직 규모·업종·규제 강도 기반 선택, BOST(Back-of-Sheet-Off-Target-Scorecard) KPI 캔버스 적용, R&R(Raci Matrix) 기반 3 Lines of Defense 모델 설계가 핵심 의사결정 분기점

---

## Ⅰ. 개요 및 필요성

IT 경영 관리는 기업의 **전략적 목표 달성을 위해 IT 자원을 계획(Plan)·조직(Organize)·통제(Control)하는 통합 관리 체계**입니다. 디지털 전환(DX) 가속화로 인해 IT는 단순 비용 센터(Cost Center)에서 가치 창출 센터(Value Center)로 위치가 변화하였으며, 이에 따라 **IT 거버넌스(IT Governance)**는 전사적 의사결정 구조의 핵심으로 부상했습니다.

기존 IT 관리(2000년대 이전)는 시스템 단위의 운영 효율성에 집중했으나, 클라우드·AI·데이터 거버넌스가 보편화된 2020년대는 **전사적 아키텍처 정합성, 컴플라이언스(ISO 27001·PIPL·GDPR), ESG-IT 통합**이 필수 요구사항이 되었습니다. Gartner(2024) 조사에 따르면 Fortune 500 기업의 78%가 IT 거버넌스 체계 미비로 디지털 전환 프로젝트의 ROI 목표 미달성 경험이 있다고 보고되었습니다.

```text
+---------------------------------------------------------------------+
|        IT 경영 관리 3-축 프레임워크 (Tri-Axis Model)                  |
+---------------------------------------------------------------------+

        [비즈니스 가치 축]                  [규제·리스크 축]
              ^                                    ^
              |    +-------------------+          |
              |    |   Steering Com.   |          |
              |    |  (이사회·CISO·CDO)|          |
              |    +---------+---------+          |
              |              |                    |
              |    +---------v---------+          |
              |    |  거버넌스 의사결정 |          |
              |    |   (EDM 5단계)     |          |
              |    +---------+---------+          |
              |              |                    |
   -----------+--------------+--------------------+-----------
              |              v                    |
              |    +-------------------+          |
              |    |  IT 전략 계획     |<--연결---->| 컴플라이언스
              |    |  (ISP/EA 연계)    |          | (ISO/SOX/PIPL)
              |    +---------+---------+          |
              |              |                    |
              |    +---------v---------+          |
              |    |  운영·서비스      |          |
              |    |  (ITIL 4 SVS)     |          |
              |    +---------+---------+          |
              |              |                    |
              v              v                    v
        [기술·아키텍처 축]
       (Cloud·AI·Data·Security)
```

**구 vs 신 패러다임 비교**:

- **구 패러다임 (1990~2010)**: 시스템별 SPOF(Single Point of Failure) 관리, CapEx 중심의 HW 투자, ITIL v2/v3 기반 반응형 운영
- **신 패러다임 (2020~현재)**: E2E 가치 흐름(Value Stream) 관리, OpEx·Subscription 모델, ITIL 4의 SVS(Service Value System) 기반 능동형 운영, FinOps·GreenOps 통합 거버넌스

- **📢 섹션 요약 비유**: IT 거버넌스는 도시의 **종합 도시계획**과 같습니다. 개별 건물(시스템)만 잘 짓는 것이 아니라 상하수도(데이터 흐름)·전기(네트워크)·교통(프로세스)·안전(보안)이 도시 전체의 가치(시민 삶의 질)를 좌우하므로, **종합 설계도·법규·감독 체계**가 필수인 것과 같은 원리입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **COBIT 2019의 Governance & Management Objectives(40개 목표)**를 기반으로, **ITIL 4의 SVS 7대 컴포넌트**, **ISO 38500의 6대 원칙**이 3-Layer 구조로 통합됩니다.

```text
+------------------------------------------------------------------+
|  Layer 1: 의사결정 계층 (Decision Layer)                         |
|  +------------+  +------------+  +------------+                 |
|  |董事会/이사회|  |Steering    |  |IT Strategy  |                 |
|  | (Board)    |  |Committee   |  |Committee   |                 |
|  +------+-----+  +------+-----+  +------+-----+                 |
|         |               |               |                       |
|  -------+---------------+---------------+-------- (BOST 매트릭스)|
|         v               v               v                       |
|  Layer 2: 거버넌스·관리 계층 (Governance & Management)           |
|  +------------------------------------------------------+       |
|  |  EDM (Eval/Direct/Monitor) ---> RAM (Resp/Acc/Consult) |       |
|  |  APO  | BAI  | DSS  | MEA  (40 Process)              |       |
|  +----------------------+-------------------------------+       |
|         +---------------+---------------+                       |
|         v                               v                       |
|  Layer 3: 운영 계층 (Operational Layer)                          |
|  +------------------+  +------------------+  +--------------+  |
|  |ITIL 4 SVS:       |  |Agile/DevOps      |  |AIOps/FinOps  |  |
|  |Service Value Chain|  |SRE/SLC           |  |GreenOps      |  |
|  +------------------+  +------------------+  +--------------+  |
+------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 거버넌스 의사결정 사이클 | COBIT 2019의 5단계 사이클(EDM01~05), 의사결정 권위·책임 할당, ISO 38500의 책임 모델 매핑 |
| **RAM (Responsibility Assignment Matrix)** | 역할·책임 정의 | RACI 매트릭스, 3 Lines of Defense 모델(운영·준법·내부감사), R&O(Responsible/Owner) 구분 |
| **ITIL 4 SVS (Service Value System)** | 서비스 가치 창출 | 7대 컴포넌트(가치·원리·Governance·실천·가치사슬·관행·개선), 34개 Service Practice |
| **KPI/CSF (Critical Success Factor)** | 성과 측정 | BOST 캔버스(Back-of-Sheet-Off-Target-Scorecard), BSC(Balanced Scorecard) 4관점(재무·고객·프로세스·학습) |
| **Risk & Compliance Engine** | 리스크·규제 관리 | ISO 27001 ISMS, NIST CSF 2.0, COBIT 2019 MEA03(Manage Compliance) 연계 |

### 핵심 알고리즘·산식

**① IT 투자 우선순위 결정 모델 (Weighted Scoring Model)**:
```
Priority Score = Σ (Wi × Si) × Alignment_Factor × Risk_Factor
where:
  Wi = 가중치 (0~1, ΣW=1)
  Si = 전략적 중요도 (1~5)
  Alignment_Factor = 비즈니스 목표 연계도 (0.5~1.5)
  Risk_Factor = (1 - 프로젝트 실패확률) = 0.6~1.0
```

**② COBIT 2019 Process Capability 산식 (ISO/IEC 33000 PAM)**:
```
Capability Level (0~5) = Σ(Attribute_Level_Score) / Number_of_Attributes
  - Level 0: Incomplete
  - Level 1: Performed (Process attribute: PA 1.1)
  - Level 2: Managed (PA 2.1~2.2)
  - Level 3: Established (PA 3.1~3.2)
  - Level 4: Predictable (PA 4.1~4.2)
  - Level 5: Optimizing (PA 5.1~5.2)
```

**③ BOST KPI 캔버스 구조 (예: IT 운영 안정성)**:
- **B**(Back-of-sheet): 비재무적 핵심 지표 -> MTTR(Mean Time To Repair), Change Failure Rate
- **O**(Off-Target): 목표 미달성 시 임계치 -> MTTR > 30분, Change Failure > 15%
- **S**(Scorecard): 재무적 결과 -> 다운타임 비용 절감액, SLA Penalty 회피액
- **T**(Trend): 시계열 추세 -> 분기별 5% 개선 추세, MTTD < 5분

- **📢 섹션 요약 비유**: COBIT 2019의 EDM 사이클은 자동차의 **운전-내비게이션-계기판 시스템**과 같습니다. **Evaluate(내비게이션)**로 목적지(목표) 확인, **Direct(운전)**로 핸들·악셀 조작, **Monitor(계기판)**로 속도·연료·엔진 상태를 실시간 확인하여 **폐루프(Closed-Loop) 제어**를 구현하는 메커니즘입니다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 자주 혼동되는 핵심 프레임워크들의 비교는 기술사 시험에서 빈출되는 주제입니다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **PMBOK 7** |
| :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·관리 목표 체계 | IT 서비스 운영·개선 체계 | IT 의사결정 책임·원칙 | 프로젝트 관리 원칙·도메인 |
| **적용 범위** | 전사 IT 거버넌스(End-to-End) | IT 서비스 운영(Service Operation) | 이사회·최고 의사결정층 | 프로젝트 단위 |
| **핵심 구조** | 40개 Governance/Management 목표 | 34개 Practice + SVS | 6대 원칙 + 모델 | 12 Principle + 8 Domain |
| **평가 방법** | ISO/IEC 33000 PAM(0~5) | CMMI 기반 Maturity | Self-assessment Maturity | Process Assessment Model |
| **연계 프레임워크** | ITIL, TOGAF, PRINCE2 | COBIT, DevOps, SIAM | COBIT, ISO 27001 | COBIT, PRINCE2, SAFe |
| **핵심 KPI 예시** | Goal Cascade 일치율 ≥ 90% | First Call Resolution ≥ 80% | 원칙 준수율 100% | SPI/CPI ≥ 1.0 |

**다른 시스템과의 연결**:

- **EA(Enterprise Architecture)와의 연결**: TOGAF ADM(Architecture Development Method) 8단계와 COBIT
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 794 / 800

<- **이전**: [793. IT 경영 관리 핵심 토픽 793번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/793_it_management_core_topic_793_exam_summary/)
**다음**: [795. IT 경영 관리 핵심 토픽 795번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/795_it_management_core_topic_795_exam_summary/) ->

---
