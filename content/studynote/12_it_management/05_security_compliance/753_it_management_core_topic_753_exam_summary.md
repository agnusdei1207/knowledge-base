+++
title = "753. IT 경영 관리 핵심 토픽 753번 시험 요약 (IT Management Core Topic 753 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019의 40개 관리 목적(Governance & Management Objectives)**을 중심으로, 비즈니스 목표(Strategy)와 IT 자원·리스크·성과를 **EDM(5) -> APO(14) -> BAI(11) -> DSS(6) -> MEA(4)**의 5단계 캐스케이드로 정렬하는 의사결정 체계이며, ITIL 4의 34개 실무 관행(SVS·Service Value Chain)과 ISO 27001의 93개 통제(Annex A 2013->2022 리팩토링)를 **"거버넌스-관리-실무" 3계층**으로 통합 운영하는 것이 핵심이다.
> 2. **가치**: McKinsey(2023) 기준 통합 거버넌스 도입 기업의 **IT 투자 ROI 23% 개선, Time-to-Market 35% 단축, 보안 사고 58% 감소, 컴플라이언스 비용 42% 절감**; K-ISMS 인증 기업의 경우 평균 해킹 침해 비용이 비인증 대비 **2.7배 낮음**(한국인터넷진흥원 2022).
> 3. **판단 포인트**: **① 중앙집중형(CoE) vs 분산형(Federated) 거버넌스**, **② 내부 역량(Insourcing) vs 아웃소싱/클라우드(BaaS/SaaS)**, **③ 표준화(Standardization) vs 유연성(Autonomy)**의 트레이드오프를 RACI 매트릭스·TCO 모델·BABOK v3의 6가지 기법(MoSCoW, BPMN, SWOT, PESTLE, Five Forces, Root Cause)으로 정량 평가해야 한다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 시험에서 **IT 경영 관리**는 단순한 IT 운영을 넘어 **"전략적 의사결정(Strategic Decision Making)"의 체계화**를 평가하는 핵심 영역이다. 과거(2000년대 초)에는 COBIT 4.1/ITIL v2 중심의 프로세스 Maturity 측정이 주류였으나, **클라우드 전환, 생성형 AI(GenAI), ESG 규제, Supply Chain Risk**가 결합된 2024년 현재, 거버넌스의 패러다임은 다음 3가지로 진화했다.

| 패러다임 | 시기 | 핵심 키워드 | 한계 |
| :--- | :--- | :--- | :--- |
| **1세대: 프로세스 중심** | 2000~2010 | COBIT 4.1, ITIL v2, CMM/CMMI | 정성적 maturity 측정, 비즈니스 정렬 미흡 |
| **2세대: 가치 중심** | 2010~2018 | COBIT 5, ITIL 2011, ISO 38500 | Agile/DevOps 속도 따라가지 못함 |
| **3세대: 생태계·지속가능성 중심** | 2018~현재 | **COBIT 2019, ITIL 4, ISO 27001:2022, NIST CSF 2.0** | AI 거버넌스·양자 보안 신규 영역 발생 |

```text
[ 디지털 전환 시대의 IT 경영 관리 5대 트리거 ]

  +--------------+    +--------------+    +--------------+
  | ① 비즈니스  |    | ② 규제·리스크 |    | ③ 기술 복잡도 |
  |   민첩성 요구 |---->|   (ESG,GDPR,  |---->|   (Multi-Cloud,|
  | (Agile/DevOps)|    |   DORA,PIPA) |    |    AI/ML)      |
  +------+-------+    +------+-------+    +------+-------+
         |                    |                    |
         v                    v                    v
  +----------------------------------------------------------+
  |        IT 경영 관리 거버넌스 프레임워크 필요성             |
  |  (COBIT 2019 + ITIL 4 + ISO 27001 + TOGAF + DAMA)        |
  +----------------------------------------------------------+
         ^                    ^                    ^
         |                    |                    |
  +------+-------+    +------+-------+    +------+-------+
  | ④ 투자 효율성 |    | ⑤ 인재·문화  |    | ⑥ 사이버     |
  |  (FinOps, TCO)|    |  (SRE, MLOps)|    |  회복탄력성   |
  +--------------+    +--------------+    +--------------+
         (Source: ISACA State of Cybersecurity 2023, Gartner Hype Cycle 2024)
```

**왜 지금 IT 경영 관리인가?**
- **Statista(2024)**: 글로벌 IT 지출 5.1조 USD, 이중 **31%가 "거버넌스 부재"로 비효율 발생**(중복 투자 평균 18%, Shadow IT 24%)
- **Gartner**: 2026년까지 글로벌 기업의 60%가 디지털 거버넌스 부족으로 **프로젝트 실패 비용 1.4조 USD 예상**
- **한국 상황**: 공공부문 정보시스템 감리 의무화(2022 강화), 클라우드 보안인증制度(CSAP) 확대, AI Basic Act(2026 시행 예정)로 인한 거버넌스 컴플라이언스 요구 급증

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 "통합 차량 제어 시스템(VCS·ADAS)"**과 같다. 엔진(IT 운영), 브레이크(리스크 관리), 내비게이션(전략), 블랙박스(감사)가 **CAN 버스(거버넌스 프레임워크)**로 연결되어야만 안전하고 효율적인 주행이 가능하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019의 5단계 캐스케이드 (Cascade)

```text
[ COBIT 2019 40개 관리 목적의 계층 구조 ]

  +-----------------------------------------+
  | Stakeholder Needs (이해관계자 니즈)      |  <- "13가지 기업 목표(Enterprise Goals)"
  |  - 수익성, 고객 경험, 규제 준수 등       |     + 13가지 정렬 목표(Alignment Goals)
  +----------------+------------------------+
                   v
  +-----------------------------------------+
  | Enterprise Goals (기업 목표 13개)        |  <- BSC 4관점 (재무/고객/내부/학습성장)
  +----------------+------------------------+
                   v
  +-----------------------------------------+
  | Alignment Goals (IT 정렬 목표 13개)      |  <- "IT가 무엇을 달성해야 하는가"
  +----------------+------------------------+
                   v
  +-----------------------------------------+
  | Management Objectives (관리 목적 40개)   |  <- EDM(5) + APO(14) + BAI(11) + DSS(6) + MEA(4)
  +----------------+------------------------+
                   v
  +-----------------------------------------+
  | Component Variants (구성요소 변형 7개)   |  <- 프로세스/구조/정보/문화/스킬/서비스/인프라
  +----------------+------------------------+
                   v
  +-----------------------------------------+
  | Focus Areas (포커스 영역 - 가변)         |  <- DevOps, Risk, Privacy, AI, ESG, Cloud
  +-----------------------------------------+
```

### 2. COBIT 2019 핵심 영역별 40개 관리 목적

| 영역 | 개수 | 대표 관리 목적 (번호·이름) | 핵심 KPI |
| :--- | :--- | :--- | :--- |
| **EDM** (Evaluate, Direct, Monitor) | 5 | EDM01 거버넌스 체계 수립, EDM02 이익 실현, EDM03 리스크 최적화, EDM04 자원 최적화, EDM05 이해관계자 투명성 | 이사회 의사결정 주기(평균 12일->4일), IT 투자 수익률 |
| **APO** (Align, Plan, Organize) | 14 | APO01 관리 프레임워크, APO02 전략, APO03 엔터프라이즈 아키텍처, **APO04 혁신**, APO05 포트폴리오, **APO12 리스크 관리**, APO13 보안 | EA 준수율, 혁신 도입률, 보안 KPI |
| **BAI** (Build, Acquire, Implement) | 11 | BAI01 관리 프로그램, BAI02 요구사항 정의, **BAI03 솔루션 선정 (RFP)**, BAI09 자산 관리, BAI11 품질 관리 | 프로젝트 정시 완료율, 결함 밀도 |
| **DSS** (Deliver, Service, Support) | 6 | **DSS01 운영**, DSS02 서비스 요청, **DSS04 연속성**, DSS05 보안 운영, DSS06 비즈니스 프로세스 통제 | SLA 준수율 99.9%, MTTR, MTTD |
| **MEA** (Monitor, Evaluate, Assess) | 4 | MEA01 성과/준수 모니터링, MEA02 내부 통제, MEA03 외부 요구사항 준수, MEA04 Assurance | 감사 발견사항, 통제 실패율 |

### 3. ITIL 4 Service Value System (SVS) 통합 구조

```text
[ ITIL 4 SVS - Service Value System ]

                    +-----------------------+
                    | Opportunity/Demand    |  <- 외부 입력
                    | (기회/수요)            |
                    +----------+------------+
                               v
                    +-----------------------+
                    |   Value (가치)        |  <- 최종 산출물
                    |  - 유용성·적합성·효용  |     (Co-Creation)
                    +----------^------------+
                               |
  +----------------------------+-----------------------------+
  |                                                           |
  |  +----------------------------------------------------+   |
  |  |  Guiding Principles (7대 지침 원칙)                 |   |
  |  |  ① Focus on value, ② Start where you are,         |   |
  |  |  ③ Progress iteratively with feedback,             |   |
  |  |  ④ Collaborate and promote visibility,            |   |
  |  |  ⑤ Think and work holistically,                   |   |
  |  |  ⑥ Keep it simple and practical,                  |   |
  |  |  ⑦ Optimize and automate                          |   |
  |  +----------------------------------------------------+   |
  |                                                           |
  |  +----------------------------------------------------+   |
  |  |  Governance (거버넌스 조직·정책)                     |   |
  |  |  ---------------------------------                  |   |
  |  |  Service Value Chain (SVC) - 6개 활동                |   |
  |  |  Plan -> Improve -> Engage -> Design&Transition       |   |
  |  |        -> Obtain/Build -> Deliver&Support            |   |
  |  |  (34 Practices: 14 General + 17 Service + 3 Tech)   |   |
  |  +----------------------------------------------------+   |
  |                                                           |
  |  +----------------------------------------------------+   |
  |  |  Continual Improvement (지속적 개선)                 |   |
  |  |  - 7단계 모델, 4차원(CCTV: Culture-Tech            |   |
  |  |    -Value-Value stream)                             |   |
  |  +----------------------------------------------------+   |
  |                                                           |
  |  +----------------------------------------------------+   |
  |  |  Practices (34개
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 753 / 800

<- **이전**: [752. IT 경영 관리 핵심 토픽 752번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/752_it_management_core_topic_752_exam_summary/)
**다음**: [754. IT 경영 관리 핵심 토픽 754번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/754_it_management_core_topic_754_exam_summary/) ->

---
