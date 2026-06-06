---
title: "IT Management Core Topic 618 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 618. IT 경영 관리 핵심 토픽 618번 시험 요약 (IT Management Core Topic 618 Exam Summary)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO 38500, TOGAF 10 등 글로벌 거버넌스 프레임워크를 기반으로 **전략(Strategy) -> 거버넌스(Governance) -> 아키텍처(Architecture) -> 운영(Operations) -> 가치(Value)** 의 5계층 가치사슬(Value Chain)을 통합 관리하는 경영학문이다.
> 2. **가치**: McKinsey & Company(2023) 연구에 따르면 체계적 IT 거버넌스 도입 기업은 **IT 투자 대비 ROI 25~40% 향상**, 디지털 트랜스포메이션 성공률 **35% -> 70%** 로 증가하며, COBIT 2019 도입 시 **IT 리스크 사고 60% 감소** 효과가 검증되었다.
> 3. **판단 포인트**: 기술사형 의사결정에서 가장 중요한 것은 **BAPV(Build After Provide Vendor) vs BPMS(Business Process Management Suite)**, **Bimodal IT vs 단일 거버넌스**, **EA 도입 범위(전사 vs 부분)**, **클라우드 네이티브 전환 시 To-Be 거버넌스 모델 설계**, 그리고 **정보보안 통제(예방/탐지/대응) 균형** 이다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명 시대에 기업의 IT는 단순한 비용센터(Cost Center)에서 **전략적 가치 창출 센터(Strategic Value Creator)** 로 전환되었다. 그러나 한국정보화진흥원(2023) 조사에 따르면 국내 대기업의 **62%** 가 "IT-Biz 정렬(Alignment)" 실패를 경험했으며, CIO의 **48%** 가 CEO와 IT 성과 측정 기준에 대한 시각차를 호소한다. 이는 곧 **IT 거버넌스 부재 -> IT 투자 실패 -> 디지털 전환 지연** 의 악순환으로 이어진다.

이에 본 토픽은 **기술사 1교시(단답형) 및 2교시(서술형)**, **3교시(실무형)·4교시(논문형)** 에서 매년 출제되는 **IT 전략, 거버넌스, EA, 투자평가, 서비스관리, 보안 거버넌스, 컴플라이언스, 디지털전환** 의 8대 축을 통합적으로 다룬다.

```text
+-----------------------------------------------------------------+
|              IT 경영관리 5계층 통합 프레임워크                    |
+-----------------------------------------------------------------+
|                                                                 |
|   [1] 전략(Strategy) --------------------------------------+   |
|      • 디지털 전환 로드맵 / IT 전략계획(ISP)                 |   |
|      • 비즈니스 역량 모델링(BMM)                              |   |
|   +------------------------------------------------------+   |   |
|   |  [2] 거버넌스(Governance) --------------------------+ |   |   |
|   |    • COBIT 2019 / ISO 38500 / ITIL 4               | |   |   |
|   |    • RACI 매트릭스 / 의사결정 권한 위임(Delegation)  | |   |   |
|   |  +----------------------------------------------+  | |   |   |
|   |  |  [3] 아키텍처(Architecture) --------------+  |  | |   |   |
|   |  |    • TOGAF 10 ADM / Zachman 6×6           |  |  | |   |   |
|   |  |    • 업무/데이터/응용/기술 4계층 모델      |  |  | |   |   |
|   |  |  +--------------------------------------+ |  |  | |   |   |
|   |  |  |  [4] 운영(Operations) ------------+ |  |  | |   |   |
|   |  |  |    • ITIL 4 Service Value System |  |  | |   |   |
|   |  |  |    • DevOps / SRE / AIOps         |  |  | |   |   |
|   |  |  |  +------------------------------+ |  |  | |   |   |
|   |  |  |  |  [5] 가치(Value) --------+  | |  |  | |   |   |
|   |  |  |  |    • KPI/OKR 측정       |  | |  |  | |   |   |
|   |  |  |  |    • ROI/NPV/IRR       |  | |  |  | |   |   |
|   |  |  |  |    • TCO/TVO 분석      |  | |  |  | |   |   |
|   |  |  |  +------------------------------+ |  |  | |   |   |
|   |  |  +--------------------------------------+ |  |  | |   |   |
|   |  +----------------------------------------------+  |  | |   |   |
|   +------------------------------------------------------+   |   |   |
|   +------------------------------------------------------+   |   |   |
|                                                                 |
|   -> 하위 계층은 상위 계층의 결정사항을 구현, 상위는 하위의       |
|     피드백을 받아 지속적으로 개선(Plan-Do-Check-Act)              |
+-----------------------------------------------------------------+
```

**기존 vs 새로운 패러다임 비교**

| 구분 | 전통적 IT 관리 (2000년대 이전) | 현대 IT 경영관리 (2020년대 이후) |
|:---|:---|:---|
| IT의 위치 | 비용센터 (Cost Center) | 가치센터 (Value Center) |
| 의사결정 | CIO 독단적 예산 배분 | CDO·CxO 이사회 거버넌스 |
| 아키텍처 | 사일로(Silo) 시스템 | EA 기반 통합·플랫폼화 |
| 운영 모델 | Waterfall, ITIL v3 | Agile + DevOps + SRE, ITIL 4 |
| 투자 평가 | 재무적 ROI 위주 | 재무+전략+비재무(OKR) 통합 |
| 보안 대응 | 사후 대응 (Perimeter) | Zero Trust, 예방/탐지/대응 균형 |
| 규제 대응 | 컴플라이언스 Check-box | Risk-Based + Continuous Compliance |
| 데이터 활용 | 보고용 정형 데이터 | 데이터 거버넌스 + DataOps + AI/ML |

- **📢 섹션 요약 비유**: IT 경영관리는 마치 **대형 항공모함의 함교(CIO Office)** 와 같다. 함교는 항공기(프로젝트), 함재기(시스템), 탑승원(임직원), 탄약(데이터)뿐 아니라 적함(리스크), 기상(시장변화), 진로(전략)까지 통합 관리하여 하나의 작전(비즈니스 목표)을 수행한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 거버넌스 시스템 (Governance System)

COBIT 2019는 **ISACA(Information Systems Audit and Control Association)** 가 2018년 12월 발표(2019년 정식 업데이트)한 글로벌 IT 거버넌스 프레임워크로, **40개의 관리목표(Management Objective)** 와 **5개 도메인(EDM: Evaluate/Direct/Monitor, APO: Align/Plan/Organize, BAI: Build/Acquire/Implement, DSS: Deliver/Service/Support, MEA: Monitor/Evaluate/Assess)** 으로 구성된다.

```text
+--------------------------------------------------------------------+
|              COBIT 2019 거버넌스 시스템 5개 도메인                  |
+--------------------------------------------------------------------+
|                                                                    |
|  +------+  +------+  +------+  +------+  +------+                |
|  | EDM  |-> | APO  |-> | BAI  |-> | DSS  |-> | MEA  |-> (피드백)      |
|  |  5개 |  | 14개 |  | 11개 |  |  6개 |  |  4개 |                |
|  | 목표 |  | 목표 |  | 목표 |  | 목표 |  | 목표 |                |
|  +--+---+  +--+---+  +--+---+  +--+---+  +--+---+                |
|     |         |         |         |         |                      |
|     +----+----+----+----+----+----+----+----+                      |
|          v         v         v         v                           |
|      +-------------------------------------+                       |
|      |  Enablers(촉진자) 7개 구성요소       |                       |
|      |  1. Principles/Polices/Frameworks   |                       |
|      |  2. Processes (40개)                 |                       |
|      |  3. Organizational Structures        |                       |
|      |  4. Information Flow & Items         |                       |
|      |  5. People, Skills, Competencies     |                       |
|      |  6. Culture, Ethics, Behavior        |                       |
|      |  7. Services, Infra, Applications    |                       |
|      +-------------------------------------+                       |
|                                                                    |
|  <- 7단계 핵심특성(Cascade of Goals) 연계:                            |
|   Stakeholder Needs -> Enterprise Goals -> Alignment Goals ->         |
|   -> Management Objectives -> Component Goals -> IT Goals              |
+--------------------------------------------------------------------+
```

### 2. TOGAF 10 ADM (Architecture Development Method)

**The Open Group** 의 TOGAF 10(2022년 발간)은 EA 구축의 사실상 표준(global de-facto standard)이며, **ADM(Architecture Development Method)** 이라는 8단계(Phase A~H) 반복적 방법론을 제공한다. 9.x에서 10으로의 주요 변화는 **마이크로서비스·클라우드 네이티브 반영**, **Agile/Lean 통합**, **NaVic (NAvigation through the VIrtual Campus) 확장** 이다.

```text
+------------------------------------------------------------------+
|                   TOGAF 10 ADM 8단계 사이클                       |
|                                                                  |
|  +----+                                                          |
|  |Pre | (Architecture Capability)                                |
|  +-+--+                                                          |
|    v                                                             |
|  +----+  Preliminary Phase                                        |
|  | A  | Architecture Vision         +                              |
|  |    | Stakeholder concerns/Goals  |                              |
|  +--+-+                            |                              |
|     v                              |                              |
|  +----+                            |                              |
|  | B  | Business Architecture       |  Architecture                |
|  +--+-+                            |  Continuum                   |
|     v                              |  (Foundation->                 |
|  +----+                            |   Common Systems->            |
|  | C  | Information Systems         |   Industry->                  |
|  |    |   - Data Architecture       |   Organization->              |
|  |    |   - Application Architecture|   Specific Architecture)     |
|  +--+-+                            |                              |
|     v                              |                              |
|  +----+                            |                              |
|  | D  | Technology Architecture     |                              |
|  |    |   (HW/SW/Network/Middleware)|                              |
|  +--+-+                            |                              |
|     v                              |                              |
|  +----+                            |                              |
|  | E  | Opportunities & Solutions   |                              |
|  |    | (구현 마이그레이션 계획)    |                              |
|  +--+-+                            |                              |
|     v                              |                              |
|  +----+                            |                              |
|  | F  | Migration Planning          |                              |
|  |    | (전환 로드맵, TCO/ROI)      |                              |
|  +--+-+                            |                              |
|     v                              |                              |
|  +----+                            |                              |
|  | G  | Implementation Governance   |                              |
|  |    | (아키텍처 준수 통제)        |                              |
|  +--+-+                            |                              |
|     v                              |                              |
|  +----+                            |                              |
|  | H  | Architecture Change Mgmt   +                              |
|  +--+-+     (변경관리, 마이크로서비스 진화)                       |
|     |                                                            |
|     +-------- ADM Cycle 반복 -----------+                        |
|                                          v                        |
|                          +----------------------+                |
|                          | Requirements Mgmt    |                |
|                          | (모든 Phase 공통)     |                |
|                          +----------------------+                |
+------------------------------------------------------------------+
```

### 3. ITIL 4 Service Value System (SVS)

**ITIL 4** 는 2019년 AXELOS(현재 PeopleCert)가 발표하여, **서비스 가치 사슬(Service Value Chain, SVC)** 의 6개 활동(Plan/Improve/Engage/Design & Transition/Obtain/Build & Deliver/Deliver & Support)과 **34개 모범사례(Practice)** 로 구성된다. ITIL v3의 **함수-프로세스 모델 -> 가치-스트림 모델** 로의 패러다임 전환이 핵심이다.

### 4. ISO 38500 IT 거버넌스 국제표준

**ISO/IEC 38500:2015** 는 이사회(Board)가 IT를 **Evaluate -> Direct -> Monitor** 하는 3원칙 모델을 제시하며, 한국에서는 **TTA(한국정보통신기술협회)** 의 KS X 38500으로 동일하게 제정되어 있다.

### 5. IT 투자평가 방법론

| 평가 방법 | 수식 / 핵심 지표 | 적용 상황 | 한계 |
|:---|:---|:---|:---|
| **NPV (순현재가치)** | Σ (CF_t / (1+r)^t) - I_0 | 5년 이상 대규모 프로젝트 | 할인율(r) 산정 주관성 |
| **IRR (내부수익률)** | NPV=0이 되는 r | 복수 프로젝트 우선순위 | 상호배타적 프로젝트 시 오류 |
| **ROI (투자수익률)** | (이익-비용)/비용 × 100 | 단년/단순 투자 | 무형 효과 미반영 |
| **TCO (총소유비용)** | 직접비(초기+운영) + 간접비(생산성손실) | 하드웨어·S/W 선정 | 기회비용 미반영 |
| **TVO (총가치소유)** | TCO + 혜택(재무+비재무) | EA/거버넌스 투자 | 비재무 가치 정성화 어려움 |
| **BEA (Business Economics for IT)** | 정보경제학 기반 정량 모델 | Gartner 권장 (1990s~) | 모델 복잡성 |
| **CBA (비용편익분석)** | B/C 비율 | 공공/정부 IT사업 | 사회적 가치 환산 어려움 |

### 구성 요소 표

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **이사회(Board) / IT전략위원회** | 거버넌스 최상위 의사결정 | ISO 38500 EDM 모델, RACI 매트릭스, 연 4회 정기회의 + 수시 |
| **CIO (Chief Information Officer)** | IT 부서장 + 전략파트너 | IT 전략기획(ISP) 수립, 비즈니스-기술 정렬, 이사회 보고 |
| **CDO (Chief Data Officer)** | 데이터·AI 거버넌스 | 데이터 카탈로그, 마스터데이터관리(MDM), AI윤리, DataOps |
| **CISO (Chief Information Security Officer)** | 정보보안 총괄 | ISO 27001/27002, NIST CSF 2.0, Zero Trust, GRC 통합 |
| **EA(Enterprise Architecture) 팀** | 아키텍처 표준화·거버넌스 | TOGAF ADM, ArchiMate 3.2, EA Repository, Architecture Review Board |
| **PMO (Project Management Office)** | 프로젝트 포트폴리오 관리 | P3O(Portfolio/Programme/Project Office), MSP, PRINCE2 |
| **서비스 운영팀** | 일관된 IT 서비스 제공 | ITIL 4 SVS, SRE(Site Reliability Engineering), SLO/SLI/SLI |
|
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 618 / 800

<- **이전**: [617. IT 경영 관리 핵심 토픽 617번 시험 요약](/studynote/12_it_management/05_security_compliance/617_it_management_core_topic_617_exam_summary/)
**다음**: [619. IT 경영 관리 핵심 토픽 619번 시험 요약](/studynote/12_it_management/05_security_compliance/619_it_management_core_topic_619_exam_summary/) ->

---
