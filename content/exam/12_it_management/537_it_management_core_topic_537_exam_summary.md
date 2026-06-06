---
title: "IT Management Core Topic 537 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO 27001/20000 등 글로벌 거버넌스 프레임워크를 기반으로 IT 거버넌스-전략-포트폴리오-운영-리스크-컴플라이언스를 End-to-End로 통합 관리하는 체계이며, BSC와 KPI를 통해 정량적 성과 측정이 핵심이다.
> 2. **가치**: 성숙도 Level 3 도달 시 IT 투자 ROI 평균 25% 이상 개선, 인시던트 MTTR 60% 단축, 컴플라이언스 위반 80% 감소, 그리고 EA-TOGAF 기반 Portfolio 우선순위 결정으로 한정된 IT 예산의 30~40% 재배분이 가능하다.
> 3. **판단 포인트**: "Build vs Buy vs Cloud" 의사결정, 내부 역량 확보 vs 외주(SI/ITO) 비율의 7:3 법칙, 사이버보안 Zero-Trust 도입 시 ROI 회수 기간(평균 18개월), 그리고 AGILE 운영 모델과 전통 ITIL 간의 충돌 시 하이브리드 거버넌스 설계가 핵심 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화와 규제 환경의 복잡화(개인정보보호법, GDPR, ESG, AI기본법)로 인해 IT 부서는 단순 비용센터(Cost Center)에서 가치창출센터(Value Center)로 전환되어야 한다. 한국정보화진흥원의 NCS(국가직무능력표준) 20010201(정보기술 전략기획) 및 20010202(정보기술 운영) 영역에서 정의된 "IT 경영 관리"는 단순 시스템 운영을 넘어 **전략-거버넌스-포트폴리오-서비스-리스크-컴플라이언스**를 5축으로 통합 관리하는 영역이다.

특히 2024년 이후 클라우드, 생성형 AI(LLM), 양자컴퓨팅 등 신기술 도입이 가속화되면서, 전사 차원의 **IT 거버넌스 미성숙 기업은 기술 부채(Technical Debt)가 연 15% 이상 누적**되어 사업 경쟁력이 급격히 하락한다. 미국 GAO 보고서에 따르면 Fortune 500 기업의 67%가 IT 거버넌스 부재로 인한 프로젝트 실패(평균 손실 1억 달러)를 경험했다.

```text
[IT 경영 관리 5대 축 통합 프레임워크]
                    +-------------------------+
                    |   IT 거버넌스 (Governance)|  <- COBIT 2019, 이사회/CEO
                    |   - 원칙/정책/의사결정권   |
                    +------------+------------+
                                 |
            +--------------------+--------------------+
            |                    |                    |
   +--------v--------+  +--------v--------+  +-------v--------+
   | IT 전략기획      |  | IT 포트폴리오   |  | IT 서비스 운영  |
   | (Strategy)      |  | (Portfolio)     |  | (Service Ops)  |
   | - BSC/OKR       |  | - PMO           |  | - ITIL 4       |
   | - EA-TOGAF      |  | - 우선순위/예산 |  | - SLA/XLA      |
   | - RFP/발주       |  | - Build/Buy     |  | - ITSM 도구    |
   +--------+--------+  +--------+--------+  +-------+--------+
            |                    |                    |
            +--------------------+--------------------+
                                 |
                    +------------v------------+
                    |  리스크 & 컴플라이언스     |  <- ISO 27001, 20000, ISMS-P
                    |  - 사이버보안, BCP/DR     |     GDPR, 개인정보보호법
                    |  - ESG/내부통제           |
                    +-------------------------+
```

기존 패러다임은 **"시스템 단위 관리(Silo Management)"** 였다면, 신규 패러다임은 **"플랫폼 기반 가치사슬 관리(Platform-based Value Chain)"** 이다. 즉 개별 시스템의 가용성(99.9%)을 추구하던 단계에서, **E2E 비즈니스 프로세스 관점의 서비스 수준(End-user Experience)과 비즈니스 임팩트(Business Impact)** 중심으로 전환되었다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 도시의 "교통관제 시스템"과 같다. 신호등 하나(개별 시스템)가 잘 작동하는 것보다, 도시 전체 차량 흐름(End-to-End 비즈니스 서비스)을 실시간으로 조정하고 사고(인시던트) 발생 시 우회로(DR/BCP)를 즉시 가동하는 것이 핵심이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **상위 의사결정층(Governance) -> 중위 기획층(Strategy/Portfolio) -> 하위 운영층(Service/Risk)** 의 3-tier 구조로, 각 계층은 RACI 매트릭스와 KPI 체인을 통해 연결된다. COBIT 2019의 **Governance System Components(40개) + Focus Areas + Design Factors** 가 이를 체계화한다.

```text
[3-Tier IT 경영관리 아키텍처 및 정보 흐름]
+------------------------------------------------------------------+
| Tier 1: 거버넌스 (이사회/CIO)                                       |
|  - 거버넌스 시스템: 원칙, 정책, 의사결정권, 모니터링               |
|  - KPI: EBITDA 대비 IT투자비율(3~5%), NPV, ROI, Risk Index        |
|  - 도구: GRC(Governance Risk Compliance) 플랫폼                   |
+--------------------------+---------------------------------------+
                           | (전략적 목표/예산 할당)
                           v
+------------------------------------------------------------------+
| Tier 2: 전략/포트폴리오 (CIO/사업기획)                             |
|  +--------------+  +--------------+  +----------------------+   |
|  | EA-TOGAF ADM |  | BSC/OKR     |  | Portfolio Prioritization|  |
|  | (Phase A~H)  |  | (4관점)     |  | (Weighted Scoring)   |   |
|  +------+-------+  +------+-------+  +----------+-----------+   |
|         |                  |                     |               |
|         +------------------+---------------------+               |
|                            v                                     |
|              +--------------------------+                        |
|              | PMO: 프로젝트 포트폴리오 관리 |                        |
|              | - P3O/PRINCE2/PMBOK 7th  |                        |
|              | - Steering Committee 운영  |                        |
|              +------------+-------------+                        |
+---------------------------+--------------------------------------+
                            | (서비스 카탈로그/SLA)
                            v
+------------------------------------------------------------------+
| Tier 3: 서비스 운영/리스크 (CISO/SRE/ITO)                          |
|  +--------------+  +--------------+  +----------------------+   |
|  | ITIL 4 SVS   |  | SRE/DevOps  |  | 정보보안(ISMS-P)     |   |
|  | (34 Practices)|  | (SLI/SLO/SLI)|  | ISO 27001/20000    |   |
|  +------+-------+  +------+-------+  +----------+-----------+   |
|         |                  |                     |               |
|         +------------------+---------------------+               |
|                            v                                     |
|              +--------------------------+                        |
|              | 통합관제(SoC) + 자동화      |                        |
|              | - ITSM(Jira/SM/Topdesk)   |                        |
|              | - SIEM(Splunk/Sentinel)   |                        |
|              | - AIOps(ServiceNow AIOps) |                        |
|              +--------------------------+                        |
+------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 체계 (Governance System)** | 이사회-CIO-IT조직 간 의사결정/책임 구조 정의 | COBIT 2019의 EDM( Evaluate-Direct-Monitor) 프로세스, RACI 매트릭스, 40개 Governance/Management Objectives |
| **전략 기획 (Strategy & EA)** | 사업전략-IT전략 정렬, To-Be 아키텍처 도출 | TOGAF ADM(Architecture Development Method) Phase A~H, Zachman Framework 6x6 매트릭스, BMM(Business Motivation Model) |
| **포트폴리오 관리 (Portfolio/PMO)** | 한정된 자원 내 최적 투자 조합 결정 | P3O(Portfolio, Programme, Project Office), MoP(Management of Portfolios), Weighted Scoring(전략정합40%/ROI30%/위험20%/준법10%) |
| **서비스 운영 (Service Operations)** | SLA 기반 IT 서비스 제공 및 개선 | ITIL 4 Service Value System(SVS), 34개 Practices, 4D 모델(Design-Transition-Operate-Improve), SLI/SLO/Error Budget |
| **리스크/보안/컴플라이언스** | 정보자산 위협 식별 및 통제 | ISO 27001(Annex A 93 통제항목), ISMS-P(64개 통제), NIST CSF(Identify-Protect-Detect-Respond-Recover), BCP/DR(RTO/RPO) |

**핵심 알고리즘 및 의사결정 공식**:
- **투자 우선순위 점수 = Σ(Wi × Si)**, Wi: 가중치, Si: 점수 (0~100), 일반적으로 **전략정합 40% + ROI 30% + 리스크 20% + 컴플라이언스 10%**
- **SRE 가용성 공식**: 가용성(%) = (1 - Error Budget 소진율) × 100, **99.9%(Three 9s) = 월 43.2분, 99.99%(Four 9s) = 월 4.32분** 허용 장애시간
- **TCO(Total Cost of Ownership)**: CapEx + OpEx(3~5년) + 폐기비용 - 잔존가치, 클라우드 전환 시 OpEx 비중이 60% -> 80% 증가
- **BCP RTO/RPO 결정 매트릭스**: 업무영향도 Level 1(핵심) RTO 1h/RPO 0, Level 2 RTO 4h/RPO 1h, Level 3 RTO 24h/RPO 24h

- **📢 섹션 요약 비유**: IT 경영 관리 아키텍처는 **"병원 응급의료 시스템"** 과 같다. 1층 거버넌스(병원장/이사회)가 정책을 정하고, 2층 진료과(전략/포트폴리오)가 환자를 분류(Triage)하며, 3층 응급실/수술실(서비스 운영)이 실제 치료를 한다. EMR(전사시스템)로 모든 기록이 연결되어야 한다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역은 다수의 글로벌 프레임워크가 상호 보완적으로 사용되며, 이를 잘못 선택하면 **"프레임워크 지옥(Framework Hell)"** 에 빠진다. 기술사 시험에서는 각 프레임워크의 **적용 범위/목적/핵심 산출물** 차이를 명확히 구분해야 한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 27001** | **ISO 20000** | **CMMI** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스/관리 (What) | IT 서비스 관리 (How) | 정보보안 관리체계 | IT 서비스 표준 인증 | 프로세스 성숙도 |
| **적용 범위** | 전사 IT(Strategy~Operation) | 서비스 운영/지원 | 정보보안(ISMS) | IT 서비스(ITSMS) | SW/조직 개발 |
| **핵심 구조** | 40 Governance/Management Objectives | 34 Practices, 4D 모델 | Plan-Do-Check-Act + Annex A 93통제 | Plan-Do-Check-Act + 10 프로세스 그룹 | 5 Level 성숙도 |
| **주 사용자** | CIO, 이사회, 감사 | 서비스 매니저, ITIL 실무자 | CISO, 정보보안팀 | ITSM 팀, 품질팀 | SW개발팀, PMO |
| **인증 가능성** | COBIT 인증서 (개인) | ITIL Foundation~Master (개인) | ISO 27001 (조직 인증) | ISO 20000 (조직 인증) | CMMI Level 1~5 (조직 평가) |
| **DX 시대 한계** | 클라우드/AI 통제 미흡 | DevOps/Agile 통합 보완 필요 | 양자/AI 보안 통제 보완 | 클라우드 네이티브 보완 | Agile/DevOps 반영 |

**연계 통합 패턴**:
1. **상위-하위 구조**: COBIT(거버넌스) -> ITIL(서비스) -> ISO 20000(인증) 순으로 위계를 두어 "한 번의 투자로 3개 효과" 달성
2. **보안-서비스 연동**: ISO 27001(ISMS) + ITIL(SVC) + SIEM 도구 -> Zero-Trust 보안 아키텍처
3. **EA-Togaf + BSC**: TOGAF ADM의 Phase H(Architecture Change Management) -> BSC 4관점(Financial/Customer/Internal/Learning) 매핑
4. **Agile + ITIL 하이브리드**: Spotify Squad 모델 + ITIL 4 Value Stream -> **"IT 운영의 양면성"** 모두 만족
5. **GRC 플랫폼 통합**: Archer / ServiceNow GRC / SAP GRC에서 Risk-Control-Incident를 단일 View로 통합

- **📢 섹션 요약 비유**: COBIT은 "헌법", ITIL은 "민법", ISO 27001은 "형법"과 같다. 헌법(거버넌스 원칙)이 전체를 관장하고, 민법(서비스 운영 절차)이 일상 거래를, 형법(보안/컴플라이언스)이 위반 시 제재를 규정한다. 모두 동시에 작동해야 사회(기업)가 안전하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

기술사 시험은 단순 암기형이 아닌 **"Trade-off 판단"** 을 요구한다. 다음은 실무 의사결정 시 반드시 점검해야 할 핵심 체크리스트와 흔히 저지르는 안티패턴이다.

### 기술사형 판단 체크리스트

1. **거버넌스 성숙도 진단**: 현재 조직의 COBIT 성숙도(Level 0~5) 측정 후, **목표 Level과의 Gap 2단계 이내** 로 로드맵 수립(예: Level 2 -> Level 3 목표)
2. **Build vs Buy vs Cloud 의사결정**: TCO 3년 비교, **핵심 경쟁력 영역은 Build, 비핵심은 SaaS, 변동성 큰 워크로드는 Cloud(Burst)**
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 537 / 800

<- **이전**: [536. IT 경영 관리 핵심 토픽 536번 시험 요약](/studynote/12_it_management/05_security_compliance/536_it_management_core_topic_536_exam_summary/)
**다음**: [538. IT 경영 관리 핵심 토픽 538번 시험 요약](/studynote/12_it_management/05_security_compliance/538_it_management_core_topic_538_exam_summary/) ->

---
