+++
title = "512. IT 경영 관리 핵심 토픽 512번 시험 요약 (IT Management Core Topic 512 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 핵심은 **COBIT 2019 거버넌스 체계**와 **ITIL 4 서비스 가치 시스템(SVS)**을 통합하여, **EA(Enterprise Architecture) - 거버넌스 - 운영 - 측정**의 4계층을 **RACI/DACI 매트릭스** 기반으로 정렬하는 경영 프레임워크
> 2. **가치**: 정성적 가치(의사결정 일관성·리스크 가시화·규제 대응력 향상)와 정량적 가치(ROI 15~30% 개선, IT 비용 대비 비즈니스 가치 2.5배 향상, MTTR 60% 단축, SLA 준수율 99.95% 이상 달성)
> 3. **판단 포인트**: **In-House vs Outsourcing vs Hybrid** 모델 선정, **CapEx vs OpEx** 회계 처리, **Agile vs Waterfall vs Hybrid** 프로젝트 거버넌스, 그리고 **내부 통제(Internal Control)** vs **외부 컴플라이언스(SOX, ISMS-P)** 간의 통제 중복 회피 설계

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 지원 역할에서 벗어나 **전략적 핵심 자산(Strategic Asset)**으로 전환됨에 따라, IT 투자의 정당화, 거버넌스 체계 확립, 서비스 품질 표준화, 그리고 성과 측정이 경영 이슈로 부상. 한국 정보시스템감리사/기술사 시험에서는 **"IT와 비즈니스의 정렬(Business-IT Alignment)"**을 근간으로, 4대 핵심 영역을 통합 관리하는 능력을 평가.

### 📊 IT 경영 관리 4대 핵심 영역 통합 구조도

```text
[전략적 정렬 계층]        [거버넌스 계층]         [운영 관리 계층]      [성과 측정 계층]
+--------------+    +--------------+    +--------------+    +--------------+
| 비즈니스 전략 |---->|  COBIT 2019  |---->|   ITIL 4     |---->|  BSC / KPI  |
|  (Vision)    |    |   거버넌스   |    |  SVS 운영    |    |   Balanced  |
|              |    |   40개 관리목표|    |  34개 Practice|   |  Scorecard  |
+--------------+    +--------------+    +--------------+    +--------------+
| EA (TOGAF)   |    |  RACI 행렬  |    |  Incident    |    | CSF/KPI/PI  |
| Zachman      |    |  Risk Mgmt  |    |  Problem     |    |  CSF 트리    |
| FEAF v2      |    |  Compliance |    |  Change      |    |  ROI/NPV    |
| DoDAF v2     |    |  APO/BAI    |    |  Service Desk|    |  TCO/TVO    |
+--------------+    +--------------+    +--------------+    +--------------+
        |                   |                   |                   |
        +-------------------+-------------------+-------------------+
                                |
                    +-----------v------------+
                    |  정보시스템감리(IS Audit) |
                    |  ISMS-P / PIMS / PCI-DSS|
                    |  ESG-ICT / 클라우드보호법 |
                    +------------------------+
```

### 🏛️ IT 경영 패러다임의 진화

| 시대 | 패러다임 | 핵심 키워드 | 한계점 |
|:---:|:---:|:---|:---|
| 1960~80 | 데이터 처리 자동화 | EDP, MIS | 비용 중심, ROI 부재 |
| 1990 | 정보 시스템 전략 | SSA, BSP | 부서별 사일로(Silo) 발생 |
| 2000 | IT 거버넌스 등장 | COBIT 4, ITIL v2, Sarbanes-Oxley | 통제 중심, Agile 미반영 |
| 2010 | 클라우드·모바일 전환 | COBIT 5, ITIL 2011, BYOD, Agile | DevOps 통합 미흡 |
| 2020~ | 디지털 전환(DX) | COBIT 2019, ITIL 4, SRE, FinOps, AIOps | 가치 측정·AI 거버넌스 부재 |

- **📢 섹션 요약 비유**: IT 경영 관리는 **건축물의 도면(EA) -> 감리(거버넌스) -> 시공(서비스 운영) -> 사용 후 평가(성과측정)**의 4단계가 동시에 돌아가는 **살아있는 빌딩 오퍼레이션 시스템**과 같습니다. 도면 없이 시공하면 무너지고, 감리 없이 운영하면 부패합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 🏗️ COBIT 2019 + ITIL 4 통합 거버넌스 아키텍처

```text
[이해관계자(Stakeholders) Needs]
            |
            v
+----------------------------------------------------------+
|         거버넌스 시스템 (Governance System)               |
|  +--------------------------------------------------+    |
|  | ① 거버넌스 목적 5대 원칙                          |    |
|  |    - 이해관계자 가치 실현                          |    |
|  |    - Holistic Approach (40목표 전체 조망)         |    |
|  |    - Dynamic Governance System (요인별 설계)     |    |
|  |    - 분리된 거버넌스 vs 관리 (Govern/Manage)     |    |
|  |    - 의사결정, 조정, 통제 일원화                  |    |
|  +--------------------------------------------------+    |
|            |                                              |
|            v                                              |
|  +--------------------------------------------------+    |
|  | 40개 관리목표 (Management Objectives) 5개 도메인 |    |
|  |  EDM: Evaluate, Direct, Monitor (5개)           |    |
|  |  APO: Align, Plan, Organize (14개)              |    |
|  |  BAI: Build, Acquire, Implement (11개)          |    |
|  |  DSS: Deliver, Service, Support (6개)            |    |
|  |  MEA: Monitor, Evaluate, Assess (4개)            |    |
|  +--------------------------------------------------+    |
|            |                                              |
|            v                                              |
|  +--------------------------------------------------+    |
|  | 7대 구성요소 (Components of Governance System)  |    |
|  |  ① 프로세스  ② 조직구조  ③ 정보 흐름             |    |
|  |  ④ 사람/역량  ⑤ 정책/원칙  ⑥ 문화/윤리           |    |
|  |  ⑦ 서비스/인프라/애플리케이션 (SIA)              |    |
|  +--------------------------------------------------+    |
|            |                                              |
|            v                                              |
|  +--------------------------------------------------+    |
|  | Focus Area (집중영역) : 사이버보안, DevOps,        |    |
|  |  클라우드, RPA, ESG, 디지털윤리, AI 거버넌스     |    |
|  +--------------------------------------------------+    |
+----------------------------------------------------------+
            |
            v
[ITIL 4 Service Value System (SVS)]
   Opportunity/Demand -> Value -> Plan & Improve -> Engage ->
   Design & Transition -> Obtain/Build -> Deliver & Support
```

### 📋 핵심 구성요소 매트릭스

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **EDM (Evaluate/Direct/Monitor)** | 이사회/IT 거버넌스 위원회 의사결정 | EDM01: 거버넌스 프레임워크 수립, EDM02: Benefit Delivery, EDM03: Risk Optimization, EDM04: Resource Optimization, EDM05: Stakeholder Transparency - **분기 1회 Benefit Realization Review** 수행 |
| **APO (Align/Plan/Organize)** | 전략-전술 정렬 | APO01~14: 전략관리(STRATIS), 포트폴리오 관리, 아키텍처 관리(TOGAF ADM 연동), 혁신 관리, BCM(ISO 22301), 정보보안 관리(ISO 27001), 위험관리(COSO ERM) |
| **BAI (Build/Acquire/Implement)** | 솔루션 Lifecycle | BAI01~11: 프로젝트 관리(PMBOK 7/Agile), 변경관리(CAB 회의 주 1회), 릴리즈관리, 수용성 테스트(UAT), 지식관리(KM) |
| **DSS (Deliver/Service/Support)** | 일일 운영 | DSS01~06: 운영관리, 서비스요청, 인시던트(KEDB 활용), 문제관리(RCA 5 Whys, Ishikawa), 연속성관리(RTO/RPO 정의) |
| **MEA (Monitor/Evaluate/Assess)** | 통제 및 감사 | MEA01: 성과/규제 모니터링, MEA02: 내부통제, MEA03: 외부컴플라이언스(SOX, ISMS-P, PIPC), MEA04: 감리지향(GAP 분석) |
| **ITIL 4 SVS 34개 Practice** | 운영 레이어 실무 | ① 일반경영 9개(자기관리, 워크로드, 지속개선 등) ② 서비스관리 17개(인시던트, 변경, 릴리즈, 자산, 모니터링 등) ③ 기술관리 3개 ④ 일반 5개 |
| **SLA / OLA / UC** | 서비스 수준 계약 | SLA(고객사), OLA(내부부서간), UC(외부업체간) 3계층, **가용성 99.9% / 응답시간 4시간 / 해결시간 8시간 / 만족도 4.5/5.0** 등 정량 목표 |

### 🎯 핵심 알고리즘 및 수식

**① COBIT 목표 성숙도 모델 (Maturity Model)**

```
성숙도 = Σ(실제 수행도 Level_i × 가중치_i) / Σ(가중치_i)
   Level 0: Incomplete       (실행 안됨)
   Level 1: Initial          (요구 시 비공식 수행)
   Level 2: Managed          (계획 추적됨)
   Level 3: Defined          (표준 프로세스 적용)
   Level 4: Quantitative     (정량 측정 가능)
   Level 5: Optimizing       (지속 개선, 예측 가능)

목표 성숙도(Target) - 현재 성숙도(Current) = 갭(Gap)
-> 갭 분석 후 우선순위 프로젝트 도출
```

**② IT 투자 ROI / NPV 산정**

```
ROI (%) = (총效益 - 총비용) / 총비용 × 100
NPV = Σ [CF_t / (1+r)^t] - 초기투자비
   CF_t: t년도 현금흐름
   r: 할인율 (WACC, 통상 7~12%)
IRR: NPV = 0 이 되는 r 값
Payback Period = 초기투자비 / 연평균현금흐름
TCO(Total Cost of Ownership) = CapEx + 5년 OpEx
TVO(Total Value of Opportunity) = TCO + 전략적 옵션 가치
```

**③ SLA 기반 가용성 계산**

```
가용성(%) = (총 서비스 시간 - 장애 시간) / 총 서비스 시간 × 100
   99.9% (Three-Nines) = 월 43.2분, 연 8.76시간
   99.95%              = 월 21.6분, 연 4.38시간
   99.99% (Four-Nines) = 월 4.32분, 연 52.6분
SLA 위반 패널티 = (계약 SLA - 실측치) × 서비스단가 × 패널티배율
```

- **📢 섹션 요약 비유**: COBIT 2019는 **건물의 설계도·법규·감리 체크리스트**이고, ITIL 4는 **건물 관리 매뉴얼·민원센터 운영 규칙**이며, BSC는 **건물의 종합 운영 평가표**입니다. 세 문서가 한꺼번에 굴러가야 진정한 IT 경영이 됩니다.

---

## Ⅲ. 비교 및 연결

### 🆚 COBIT 2019 vs ITIL 4 vs ISO 38500 vs PMBOK 7

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **PMBOK 7** |
|:---|:---|:---|:---|:---|
| **주 목적** | IT 거버넌스 및 관리 프레임워크 | IT 서비스 운영 최적화 | IT 의사결정 거버넌스 표준 | 프로젝트 관리 지식체계 |
| **개발 주체** | ISACA (미국감사통제협회) | AXELOS / PeopleCert | ISO/IEC JTC1 | PMI (미국) |
| **대상** | 전체 IT (전략->운영) | 서비스 운영 레이어 | 이사회·경영진 | 프로젝트 매니저 |
| **구조** | 5도메인 / 40관리목표 / 7구성요소 | SVS / 34 Practice / 4D 모델 | 6원칙(책임, 전략, 취득, 성과, 준수, 인간행위) | 12원칙 / 8성능영역 |
| **핵심 산출물** | Maturity Model, RACI, Design Factor | Value Stream, Service Value Chain | Governance Charter | Project Charter, WBS |
| **측정 지표** | Process Capability (0~5) | SLA, KPI, CSAT | KPI/PRINCE2 | SPI, CPI, PV, EV |
| **컴플라이언스** | SOX 404, ISMS-P 연계 | ISO 20000, ISO 27001 | ISO 38500 자체 | 자체 표준 |
| **한계** | 구체적 운영 Tool 부재 | 거버넌스 의사결정 약함 | 실행 절차 미흡 | 운영 단계 미포함 |
| **상호보완** | ITIL과 1:1 매핑 (DSS↔Service Practice) | COBIT APO/BAI/DSS와 매핑 | COBIT EDM과 1:1 매
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 512 / 800

<- **이전**: [511. IT 경영 관리 핵심 토픽 511번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/511_it_management_core_topic_511_exam_summary/)
**다음**: [513. IT 경영 관리 핵심 토픽 513번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/513_it_management_core_topic_513_exam_summary/) ->

---
