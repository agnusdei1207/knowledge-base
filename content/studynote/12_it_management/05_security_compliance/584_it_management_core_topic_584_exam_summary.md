---
title: "584. IT 경영 관리 핵심 토픽 584번 시험 요약 (IT Management Core Topic 584 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(ISO 38500·COBIT 2019)와 전략 기획(ISP·BPR·EA)을 통합한 **"전략-거버넌스-운영-평가" 4축 프레임워크**로, 전사 아키텍처(TOGAF ADM)와 밸런스드 스코어카드(BSC-IT)를 기반으로 IT 투자 수익률(ROIT) 최대화와 디지털 전환 성공률을 결정하는 상위통제 체계이다.
> 2. **가치**: McKinsey & Gartner(2024) 기준, 성숙한 IT 거버넌스 도입 기업은 DX 프로젝트 성공률을 35%->78%로, Shadow IT 비중을 40%->12%로 감소시키며, ISO 38500 인증 기업은 사이버 사고 대응 시간(MTTR)을 평균 62% 단축한다. 정량적으로는 TCO 23% 절감, IT 예산 대비 비즈니스 가치 실현률(Realization Rate) 2.4배 향상을 달성한다.
> 3. **판단 포인트**: 중앙집중형(CoE 모델) vs 분산형(Federated) 거버넌스 모델 선택 시 **조직 규모·산업 규제 강도·M&A 빈도**가 결정 변수이며, COBIT 2019의 40개 거버넌스/관리 목적(Governance & Management Objectives) 중 **EDM( Evaluate, Direct, Monitor) 5개 도메인**과 **APO·BAI·DSS·MEA** 4개 관리 도메인의 우선순위를 산업별 컴플라이언스(PCI-DSS, GxP, 개인정보보호법) 요건에 맞춰 커스터마이징해야 한다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 시험의 **핵심 토픽 584번**은 단순한 IT 운영 관리를 넘어, **"디지털 시대 기업의 생존 전략으로서 IT를 어떻게 통제·조정·최적화할 것인가"**에 대한 종합적 의사결정 프레임워크를 다룬다. 본 토픽은 2018년 제4차 산업혁명 키워드가 기술사 출제 빈도 1위로 부상한 이후, 매년 1~2문항씩 변형 출제되고 있는 **최고 빈출 영역**이다.

기존의 IT 관리는 **"비용 중심의 인프라 운영(Tactical)"**에 머물렀으나, 클라우드·AI·데이터 경제로 패러다임이 전환되면서, **"가치 중심의 전략적 자산 관리(Strategic)"**로 그 본질이 재정의되었다. Gartner(2023) 보고서에 따르면, 글로벌 CEO 1,200명 중 89%가 "IT는 더 이상 지원 기능이 아니라 **경쟁우위의 핵심 동력**"이라 응답했으며, Forbes Global 2000 기업의 76%가 전사 차원의 IT 거버넌스 위원회(Steering Committee)를 운영 중이다.

본 토픽이 다루는 기술적 과제는 ① **전략 정렬(Strategic Alignment)** — Business Strategy ↔ IT Strategy 간 GAP 분석, ② **가치 실현(Value Realization)** — IT 투자 포트폴리오의 ROI 추적·측정, ③ **리스크 통제(Risk Management)** — 사이버·규제·공급망 리스크의 통합 관리, ④ **자원 최적화(Resource Optimization)** — 유휴 자산·중복 시스템의 전사 가시성 확보, ⑤ **성과 측정(Performance Measurement)** — KPI 트리 및 BSC-IT 기반 정량 평가이다.

```text
[ 기업 IT 거버넌스 4축 통합 프레임워크 - 토픽 584 핵심 모델 ]

  +-------------------------------------------------------------+
  |            Board / CEO / CIO Steering Committee             |
  |                  (의사결정 최고 기구)                         |
  +------------------------+------------------------------------+
                           |
            +--------------+--------------+
            |                             |
  +---------v----------+         +---------v----------+
  |  [1] 전략(Strategy) |         |  [2] 거버넌스        |
  |   · ISP 수립        |<--------->|  · ISO 38500        |
  |   · EA(TOGAF ADM)  |         |  · COBIT 2019       |
  |   · BCM/DR 전략     |         |  · 3-Lines Model    |
  |   · 디지털 전환 로드맵|         |  · RACI 매트릭스     |
  +---------+----------+         +---------+----------+
            |                             |
            +--------------+--------------+
                           |
            +--------------+--------------+
            |                             |
  +---------v----------+         +---------v----------+
  |  [3] 운영(Delivery)  |         |  [4] 평가(Evaluate)  |
  |   · ITIL 4         |<--------->|  · BSC-IT           |
  |   · DevOps/Agile   |         |  · KPI/KRI          |
  |   · SRE 관행        |         |  · 내부통제(US-SOX) |
  |   · FinOps         |         |  · 성과감사(ISACA)   |
  +--------------------+         +--------------------+
            |                             |
            +--------------+--------------+
                           v
  +-------------------------------------------------------------+
  |       Value Realization: ROI / ROIT / NPV / Payback        |
  |   + Risk-Adjusted Value: ROSI(Risk-Oriented Value)         |
  +-------------------------------------------------------------+
```

**기존 패러다임 대비 신규 패러다임의 차별점**은 다음과 같다:

| 구분 | 전통적 IT 관리(1990~2010) | 전략적 IT 거버넌스(2020~현재) |
|:---|:---|:---|
| **관점** | Cost Center (비용 센터) | Value Center (가치 센터) |
| **조직 구조** | CIO 직할, 계층적 | CDO·CTO·CISO와 평행, CoE·Federated |
| **의사결정** | Top-Down, 사일로 기반 | 데이터 기반, 거버넌스 위원회 합의 |
| **투자 기준** | TCO 최소화, 예산 통제 | ROIT·옵션 가치·리스크 조정 수익 |
| **규제 대응** | 사후 통제, 컴플라이언스 체크리스트 | By-Design, Privacy by Default, Zero Trust |
| **측정 체계** | 시스템 가용성(Uptime) | 비즈니스 임팩트·사용자 경험·탄소 배출 |

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **"도시의 도시계획(Urban Planning) + 헌법(Constitution) + 회계 감사(Audit)"**가 합쳐진 것과 같다. 무분별한 개발(Shadow IT)을 막고, 헌법(ISO 38500)으로 권력 분립을 정하며, 감사(COBIT)로 시민(사용자)에게 가치를 증명하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

본 토픽의 기술적 핵심은 **"3-Lines Model + COBIT 2019 + ITIL 4 + ISO 38500"의 4중 통합 아키텍처**이며, 각 계층은 다음과 같은 프로토콜·메커니즘으로 동작한다.

```text
[ IT 거버넌스 4-Layer 상세 아키텍처 ]

Layer 0: 외부 환경 / 규제 / 이해관계자
   +------------------------------------------+
   | · 정보통신망법 / 개인정보보호법(PIPA)     |
   | · EU GDPR / DORA(2024) / EU AI Act      |
   | · ISMS-P / PCI-DSS / GxP / ISO 27001    |
   | · ESG 공시 / CSRD(2024) / TCFD           |
   +------------------+-----------------------+
                      | (규제·시장 신호)
Layer 1: 거버넌스 헌장(Charter) — 의사결정 원리
   +------------------------------------------+
   |   ISO 38500 EDMP 원칙 (6대 원칙)         |
   |   Responsibility · Strategy · Acquisition|
   |   Performance · Conformance · Human      |
   |   Behavior                              |
   |                                          |
   |   3-Lines Model (IIA 2020)              |
   |   1st: Operational Mgmt (비즈니스)        |
   |   2nd: Risk·Compliance·IT (통제·지원)    |
   |   3rd: Internal Audit (독립 검증)         |
   +------------------+-----------------------+
                      |
Layer 2: 통제 프레임워크 — COBIT 2019 (40개 목표)
   +------------------------------------------+
   |  EDM(5): Evaluate, Direct, Monitor      |
   |   +- EDM01: 거버넌스 프레임워크 설정·유지|
   |   +- EDM02: 가 delivery&지원 감독       |
   |   +- EDM03: 리스크 최적화 감독           |
   |   +- EDM04: 자원 관리 감독              |
   |   +- EDM05: 투명성·이해관계자 참여 감독  |
   |                                          |
   |  Align/Plan/Organize(APO) · Build/Acquire|
   |  /Implement(BAI) · Deliver/Service/DSS ·|
   |  Monitor/Evaluate/Assess(MEA) = 35개     |
   |                                          |
   |  Cascading Goals: Stakeholder->            |
   |  Enterprise->IT-Goals->Enabler Goals       |
   +------------------+-----------------------+
                      |
Layer 3: 운영 관리 체계 — ITIL 4 Service Value System
   +------------------------------------------+
   |  · Opportunity/Demand -> Value            |
   |  · 7 Guiding Principles                  |
   |  · 34 Practices (전통 26 + 신규 8)       |
   |  · Service Value Chain (Plan->Engage->     |
   |    Design&Transition->Obtain/Build->       |
   |    Deliver&Support->Improve)              |
   |  · SVS Components:        Guiding,        |
   |    Governance, Practices, Value Chain,    |
   |    Continual Improvement                 |
   +------------------+-----------------------+
                      |
Layer 4: 측정 및 피드백 — BSC-IT / KPI 트리
   +------------------------------------------+
   |  4 Perspectives:                         |
   |   · Financial: TCOv, ROIT^, Run-rate v  |
   |   · Customer: NPS, FCR, CSAT             |
   |   · Internal Process: SLA, MTTR, MTBF   |
   |   · Learning/Growth: 직원 인증, 자동화율 |
   |  + ESG: Scope 2 에너지(Green IT)         |
   +------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **ISO 38500 EDMP** | 거버넌스의 헌법·최상위 원칙 | 6대 원칙(Responsibility, Strategy, Acquire, Performance, Conformance, Human Behavior)을 거버넌스 위원회가 이행하며, 3단계 사이클(Plan->Acquire->Monitor)을 통해 이사회가 IT 의사결정에 직접 관여. 이사회와 임원진의 **"모델(Model)·감독(Supervise)·평가(Evaluate)"** 책임 명시. |
| **COBIT 2019** | 통제 목표(Control Objective)·성숙도 측정 | **40개 거버넌스/관리 목표**를 5개 도메인(EDM 5 + APO/BAI/DSS/MEA 35)으로 분류. 핵심은 **Goals Cascade**(Stakeholder Needs -> Enterprise Goals -> IT-related Goals -> Enabler Goals)와 11개 디자인 팩터(기업 전략·위험·컴플라이언스·IT 이슈·역할·기술·M&A 등)로 맞춤형 거버넌스 시스템 설계. 능력 성숙도 0~5 레벨(CMMI 기반) 측정. |
| **3-Lines Model (IIA 2020)** | 리스크·통제 책임의 명확화 | 1st Line(Operational Mgmt)이 리스크의 **소유**, 2nd Line(Risk·Compliance·IT·HR·법무)이 **전문 지원·모니터링**, 3rd Line(Internal Audit)이 **독립적 assurance** 제공. 2nd Line의 경우 1st Line에 대한 **challenge** 역할 수행. 2020년 개정으로 사이버보안·ESG·AI Ethics 등 신 리스크 대응 강화. |
| **ITIL 4 SVS** | 서비스 운영·가치 창출 실행 체계 | 7대 Guiding Principles(Focus on Value, Start Where You Are, Progress Iteratively, etc.), **Service Value Chain**의 6개 활동(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve), 34개 Practice(예: Incident Mgmt, Change Enablement, Service Desk, SLO/SLI 기반 측정). **SLO·Error Budget** 개념으로 DevOps와 통합. |
| **BSC-IT (Balanced Scorecard)** | 전략·성과의 정량 연결 | Kaplan-Norton 4관점(Financial·Customer·Internal Process·Learning/Growth)에 IT 고유 지표 매핑. Strategy Map으로 인과관계(CSF->KPI->Initiative) 시각화. **Cause-and-Effect Chain** 검증 필수(예: "직원 역량^ -> 프로세스 효율^ -> 고객 만족^ -> 매출^"). |
| **EA (TOGAF ADM)** | 전사 아키텍처 통합 설계 | 8단계 ADM(Architecture Development Method): Preliminary->A(비전)->B/C/D(비즈니스·데이터·애플리케이션·기술)->E(기회·해결책)->F(마이그레이션 계획)->G(구현 거버넌스)->H(아키텍처 변경 관리). **ArchiMate 3.2** 표준 표기법으로 Business·Application·Technology 3 Layer 모델링. |
| **KRI/KPI 트리** | 실시간 위험·성과 가시화 | KRI(Key Risk Indicator)는 Leading Indicator로 임계치 설정 시 자동 경보(예: 침해 시도 일평균 1,000건^, 패치 지연 30일^). KPI는 Lagging·Leading 혼합. **대시보드**: Grafana·Power BI·Tableau 기반 실시간 모니터링. 임계치 4단계(정상·주의->경계->심각->위기). |

**핵심 알고리즘 및 수학적 모델**:

IT 투자 평가의 정량적 의사결정은 다음 4가지 모델을 활용한다.

1. **NPV (Net Present Value)**: `NPV = Σ[CFt / (1+r)^t] - I₀` — 할인율(r) 적용 현금흐름의 합. 보통 5~7년 프로젝트의 IRR ≥ 12% 기준.
2. **Total Economic Impact (TEI) 모델**: Gartner Forrester 방식. Benefits (+PV) − Costs (−PV) − Risk (PV×확률) + Flexibility Value.
3. **Real Options Valuation (ROV)**: IT 투자의 유연성 가치. `ROV = NPV(기본) + Σ[옵션 가치 × 조정 확률]`. 단계적 투자·중도 포기 가능 시 가치^.
4.
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 584 / 800

<- **이전**: [583. IT 경영 관리 핵심 토픽 583번 시험 요약](/studynote/12_it_management/05_security_compliance/583_it_management_core_topic_583_exam_summary/)
**다음**: [585. IT 경영 관리 핵심 토픽 585번 시험 요약](/studynote/12_it_management/05_security_compliance/585_it_management_core_topic_585_exam_summary/) ->

---
