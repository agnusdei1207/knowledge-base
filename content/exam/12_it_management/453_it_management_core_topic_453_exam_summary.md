---
title: "IT Management Core Topic 453 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019 거버넌스 체계 + ISO 38500 이사회 책임 원칙 + ITIL 4 서비스 가치사슬(SVC)**을 기반으로, IT-Business Alignment를 통해 기술 자산을 전략적 비즈니스 가치로 전환하는 **엔터프라이즈 거버넌스 통합 체계**이다.
> 2. **가치**: McKinsey 연구에 따르면 성숙한 IT 거버넌스 도입 기업은 **TCO 23~35% 절감, Time-to-Market 40% 단축, IT 투자 ROI 2.7배 향상**, 그리고 ISO 38500 준수 시 **규제 컴플라이언스 위반 62% 감소** 효과를 달성한다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ① **Centralized(CoE 모델) vs Federated(Bimodal IT)**, ② **Standardization(Platform Consolidation) vs Flexibility(Best-of-Breed)**, ③ **Short-term ROI(Quick Win) vs Long-term EA(Strategic Investment)** 간의 균형이며, 기술사는 **Ward & Peppard 전략-역량-포트폴리오 3축 모델**로 의사결정해야 한다.

---

## Ⅰ. 개요 및 필요성

전통적인 IT 관리는 **"비용센터(Cost Center)"** 관점에서 운영 효율성만 추구했다. 그러나 Gartner가 2023년 발표한 조사에 따르면 글로벌 CEO의 **89%가 디지털 트랜스포메이션을 핵심 성장 동력**으로 인식하며, 평균 IT 예산의 **33%**를 디지털 이니셔티브에 편성하고 있다. 이러한 패러다임 전환기에서 IT 경영 관리(IT Management)는 단순한 시스템 운영을 넘어 **거버넌스·전략·포트폴리오·리스크·성과측정**을 통합하는 엔터프라이즈 핵심 역량으로 자리매김했다.

특히 2020년 이후 **COVID-19, 공급망 재편, 생성형 AI(GenAI) 등장, ESG 규제 강화** 등 VUCA 환경이 심화되면서, IT 투자의 정당성을 **재무적 ROI**만이 아닌 **전략적 옵션가치(Real Options Value)**, **비즈니스 민첩성(Business Agility)**, **탄소발자국(Carbon Footprint)**까지 다변화하여 평가해야 하는 시나리오가 일반화되었다. 한국 정보화진흥원의 2023년 국가정보화백서에 따르면, 국내 대기업 IT 실패 프로젝트의 **68.4%**가 **"전략 부재 + 거버넌스 미흡"**이 근본 원인으로 분석되었다.

```text
[ IT 경영 관리 패러다임 전환 ]

  +----------------+         +----------------+         +----------------+
  |   1960-1980s   |         |   1990-2010s   |         |   2020s~       |
  |   Data Proc.   |  ---->   |   IT Strategy  |  ---->   |  Digital Biz   |
  |   (비용중심)    |         |   (효율+전략)   |         |  (가치중심)     |
  +----------------+         +----------------+         +----------------+
        |                            |                            |
        v                            v                            v
  [Mainframe EDP]            [ERP, SCM, CRM]           [Cloud, AI, Data Mesh]
  [시스템 가용성]              [BPR, Six Sigma]           [Platform Engineering]
  [TCO 절감]                  [IT-Business Alignment]   [ESG + AI Ethics]
```

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **자동차의 '운전대(Steering Wheel)'**와 같습니다. 엔진(IT 인프라)이 아무리 강해도, 운전대(거버넌스)와 네비게이션(전략)가 없으면 목적지(비즈니스 가치)에 도달할 수 없고, 연비(TCO)와 안전(보안)도 관리할 수 없습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리는 크게 **5대 계층(Governance -> Strategy -> Portfolio -> Operation -> Performance)**으로 구성되며, 각 계층은 **ISO 38500의 6원칙(책임, 전략, 획득, 성능, 적합성, 인간행동)**과 **COBIT 2019의 40개 거버넌스/관리 목표(Governance & Management Objectives)**로 연결된다.

```text
[ IT 경영 관리 5계층 아키텍처 및 데이터/결재 흐름 ]

                    +-------------------------------------+
                    |   Layer 1: 이사회/IT거버넌스위원회   |  <- 전략 방향
                    |   (Board / IT Steering Committee)    |     KPI 승인
                    +-----------------+-------------------+
                                      | 정책/지침 Cascade
                                      v
                    +-------------------------------------+
                    |   Layer 2: IT 전략 기획              |  <- McFarlan Grid
                    |   (CIO Office, EA Team)              |     TOGAF ADM
                    +-----------------+-------------------+
                                      | Strategic Roadmap
                                      v
                    +-------------------------------------+
                    |   Layer 3: IT 포트폴리오 관리        |  <- NPV/IRR/ROO
                    |   (PPM Tool: ServiceNow, Clarity)    |     분산형/거점형
                    +-----------------+-------------------+
                                      | 프로젝트/서비스 출시
                                      v
        +-------------------------------------------------------------+
        |   Layer 4: IT 운영 및 서비스 관리 (ITIL 4 SVC)              |
        |   +----------+  +----------+  +----------+  +----------+   |
        |   |Plan      |  |Design    |  |Deliver   |  |Support   |   |
        |   |(전략)    |-->|(설계)    |-->|(전환)    |-->|(운영)    |   |
        |   +----------+  +----------+  +----------+  +----------+   |
        +-------------------------+-----------------------------------+
                                  | SLA, XLA, Metrics
                                  v
                    +-------------------------------------+
                    |   Layer 5: 성과 측정 및 개선          |  <- BSC 4관점
                    |   (BSC, OKR, KPI 대시보드)            |     PDCA
                    +-------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회/ITSC (IT Steering Committee)** | IT 거버넌스 최고 의사결정 기구 | **ISO 38500 6원칙** 적용, 분기별 **IT Balanced Scorecard** 리뷰, 사이버 리스크 한도 승인, CIO KPI 평가 |
| **CIO Office + EA Team** | IT 전략 수립 및 아키텍처 거버넌스 | **TOGAF ADM 8단계**(Preliminary->Vision->Business Architecture->IS->Tech->Opportunity->Migration->Governance Cycle), **Henderson의 4EA 모델**(Business, App, Data, Tech) 정렬 |
| **IT-PMO (Project/Portfolio Mgmt Office)** | 다수 프로젝트 우선순위 결정·자원 배분 | **Clarity PPM, ServiceNow SPM, Planview** 등 도구로 **NVP(Negative Value Portfolio)** 제거, **Stage-Gate Process** 적용, **Nudge Theory**로 이해관계자 정렬 |
| **ITIL Service Value Chain (SVC)** | IT 서비스 라이프사이클 운영 | **ITIL 4의 6활동**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve)을 **Value Stream** 단위로 재설계, **Shift-Left**와 **Automation**으로 Incident MTTR 50%v |
| **KPI/BSC 대시보드** | 성과 측정 및 피드백 | **Kaplan & Norton BSC 4관점**(재무/고객/내부/학습성장) + **Gartner IT Score** (2023년 출시, AI 기반 IT 성숙도 측정), **Power BI / Tableau / Grafana** 시각화 |

### 핵심 알고리즘 및 정량 모델

- **IT 투자 우선순위 결정**: **McFarlan Strategic Grid**(High/Support/Factory/Turnaround 4사분면) × **NVP(Net Present Value) ≥ 0** 이중 필터링
- **TCO 산정**: TCO = 직접비(서버·라이선스·전력) + 간접비(교육·다운타임·이직) + **OpEx(클라우드 종량제)** − CapEx(감가상각)
- **Real Options Valuation (ROV)**: 전략적 IT 투자 시 **Black-Scholes 옵션 모델**을 적용해 확장·중단·유보 의사결정의 유연성 가치(Strategic Option Value) 산정
- **BSC 4관점 인과지도(Cause-Effect Map)**: "학습성장 -> 내부프로세스 -> 고객 -> 재무"로 이어지는 16~25개 KPI 연결, **Lagging/Leading Indicator** 4:6 비율 유지

- **📢 섹션 요약 비유**: IT 경영 관리 5계층은 **의료 시스템**과 같습니다. Layer 1(이사회)은 **의료 윤리위원회**, Layer 2(전략)는 **진단·수술 계획**, Layer 3(포트폴리오)는 **수술 우선순위 결정**, Layer 4(운영)는 **수술실·회복실**, Layer 5(성과측정)는 **퇴원 후 추적 관찰**에 해당합니다. 각 층이 유기적으로 연결되어야 환자가 건강해지듯, IT 시스템이 비즈니스 가치를 창출합니다.

---

## Ⅲ. 비교 및 연결

### 프레임워크 비교 분석

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500:2015** | **TOGAF 10 (2022)** | **CMMI v2.0** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 목표 | IT 서비스 관리(SM) | IT 이사회 거버넌스 | 엔터프라이즈 아키텍처 | 프로세스 성숙도 모델 |
| **대상 범위** | 전사 IT End-to-End | IT 서비스 라이프사이클 | 이사회·경영진 의사결정 | EA 4개 도메인 | SW/서비스 개발조직 |
| **구조** | 40 Governance & Mgmt Objectives | 34 Practices, SVC | 6 원칙(Principle) | ADM 8단계 + Content | 5 Maturity Level (1~5) |
| **강점** | Risk/Control 정량 측정, Audit 친화 | Agile·DevOps·SIAM 통합 | 이사회 책임 명확화 | BIZ/DATA/APP/TECH 정합 | 성숙도 단계별 로드맵 |
| **약점** | 구현 복잡도 높음, 도구 의존 | 거버넌스 측면 약함 | 추상적 원칙 위주, 측정 KPI 부족 | 도구/방법론이 아닌 프레임워크 | 인증 비용·기간 부담 |
| **적용 시점** | 거버넌스 수립·감사 시 | 일일 운영·SLA 관리 | 이사회 정책·컴플라이언스 | EA 기반 표준화 시 | 조직 역량 진단 시 |
| **상호 보완** | **ITIL과 매핑** (Process->Practice) | **ISO 20000 인증** 기반 | **COBIT 2019 EDM** 영역과 매핑 | **ArchiMate 3.2** 모델링 | **Agile/DevOps** 와 통합 가능 |

### 중앙집중 vs 분산형 IT 조직 모델

| 구분 | **Centralized (CoE: Center of Excellence)** | **Federated (Bimodal IT, Fusion Team)** | **Decentralized (Shadow IT)** |
| :--- | :--- | :--- | :--- |
| **지휘 계통** | CIO 단일 권한, 통합 표준 | 이중 모드(1:안정/예측, 2:민첩/탐색) | 사업부 독립 예산/시스템 |
| **표준화** | ★★★★★ (Platform, API 거버넌스) | ★★★☆☆ (Mode1만 표준) | ★☆☆☆☆ |
| **민첩성** | ★★☆☆☆ | ★★★★★ (Mode 2는 LoB 자율) | ★★★★★ |
| **TCO 효율** | ★★★★★ (볼륨 디스카운트) | ★★★☆☆ | ★☆☆☆☆
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 453 / 800

<- **이전**: [452. IT 경영 관리 핵심 토픽 452번 시험 요약](/studynote/12_it_management/05_security_compliance/452_it_management_core_topic_452_exam_summary/)
**다음**: [454. IT 경영 관리 핵심 토픽 454번 시험 요약](/studynote/12_it_management/05_security_compliance/454_it_management_core_topic_454_exam_summary/) ->

---
