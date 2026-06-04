---
title: "788. IT 경영 관리 핵심 토픽 788번 시험 요약 (IT Management Core Topic 788 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 40개 거버넌스/관리 목표(Governance & Management Objectives)와 ISO/IEC 38500의 3계층 원칙(책임·전략·수행), ITIL 4의 34개 서비스 관리 실무(Service Management Practices)를 통합적으로 결합하여, 기업 가치(EV: Enterprise Value) 극대화를 위한 **Evaluate-Direct-Monitor** 의사결정 사이클을 체계화한 경영 시스템이다.
> 2. **가치**: Gartner 2023 보고 기준 효과적인 IT 거버넌스 체계를 갖춘 조직은 IT 예산 대비 ROI가 평균 2.4배, IT 프로젝트 실패율 70%->25%로 감소, 컴플라이언스 위반 비용 60% 절감, 의사결정 속도(Decision Latency) 50% 단축의 정량 효과를 입증했다.
> 3. **판단 포인트**: 기술사 관점의 핵심 트레이드오프는 ①중앙집중형(Federated) vs 분산형(Distributed) 거버넌스 모델 선택, ②COBIT 2019의 11개 Design Factor를 통한 조직 맞춤 설계 시 규제 강도와 기술 복잡성의 균형, ③RACI 매트릭스 설계 시 CIO-CDMO(Chief Data Management Officer)-CISO 간 권한 중첩 방지, ④KGI(Key Goal Indicator)->KPI->CSF의 3단 cascading 시 인과관계 검증이 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX: Digital Transformation)이 가속화되면서 전 세계 기업 IT 지출은 2024년 5조 USD를 돌파했으며, 한국 기업의 IT 예산도 GDP 대비 4.2%(2023 KISA 통계)까지 증가했다. 그러나 McKinsey Global Survey(2023) 결과 응답 기업의 **67%가 "DX로 기대했던 가치 창출에 실패했다"**고 답했으며, 실패 원인 1위가 **"IT-비즈니스 전략 부조화(Strategic Misalignment)"**로 집계됐다. 이러한 배경에서 IT 경영관리의 핵심은 단순한 비용 통제를 넘어, **IT 자산을 기업의 전략적 자산(Strategic Asset)**으로 전환하는 거버넌스 체계의 구축으로 이동했다.

기존 1990년대~2000년대 초의 IT 관리는 **COBOL/메인프레임 중심의 IT 운영 관리(Maintenance-oriented IT Management)**로, 장애 대응(SLA 99.9% uptime)과 예산 통제(Variance ±5%)가 주된 KPI였다. 그러나 2010년대 클라우드, 2020년대 생성형 AI, Web3, 양자컴퓨팅이 등장하면서 **IT 환경의 복잡성(Complexity)과 변동성(Volatility)**이 기하급수적으로 증가했고, 전통적인 ITIL v3의 26개 프로세스 중심 접근만으로는 한계가 드러났다. 이에 ISO/IEC 38500:2015, COBIT 2019, ITIL 4가 **거버넌스-관리(Service)-운영(Operation)**의 3계층 프레임워크로 재정립되었으며, 2024년 ISO/IEC 42001(AI Management System)까지 등장하며 거버넌스 대상이 "IT"에서 "AI·데이터·알고리즘"으로 확장되고 있다.

```text
[IT 경영 거버넌스 3계층 구조 - Stakeholder Value Chain]

   +------------------------------------------------------------+
   |  Stakeholder Needs (이해관계자 요구)                          |
   |  +----------+ +----------+ +----------+ +----------+       |
   |  | Shareholder| | Customer | | Regulator| | Employee |       |
   |  |  (ROI 18%) | |(CSAT 4.5)| |(컴플라이언스)| |(생산성 30%)|      |
   |  +-----+----+ +-----+----+ +-----+----+ +-----+----+       |
   |        +------------+-----+------+------------+             |
   |                          v                                   |
   |   +------------------------------------------+               |
   |   |   Enterprise Goals (13개)                |               |
   |   |   • 재무: EG01(포트폴리오 ROI)            |               |
   |   |   • 고객: EG04(고객 만족/서비스 가용성)     |               |
   |   |   • 내부: EG09(정보 처리 최적화)           |               |
   |   |   • 학습: EG12(혁신/디지털 제품)           |               |
   |   +------------------+-----------------------+               |
   |                      v                                       |
   |   +------------------------------------------+               |
   |   |   Alignment Goals (13개) - IT 기여도      |               |
   |   |   • AG01(IT 준수 및 지원)                  |               |
   |   |   • AG05(정보 및 처리 인프라 제공)         |               |
   |   |   • AG09(정보 보안 및 개인정보 보호)       |               |
   |   |   • AG13(지식, 전문성 및 비즈니스 이니셔티브) |              |
   |   +------------------+-----------------------+               |
   |                      v                                       |
   |   +------------------------------------------+               |
   |   |   Management Goals (40개)                |               |
   |   |   EDM: 05개 | APO: 14개 | BAI: 11개      |               |
   |   |   DSS: 06개 | MEA: 04개                  |               |
   |   +------------------+-----------------------+               |
   |                      v                                       |
   |   +------------------------------------------+               |
   |   |   Process Goals (40개) + Metrics         |               |
   |   |   KPI/CSF -> RACI -> Capability Level      |               |
   |   +------------------------------------------+               |
   +------------------------------------------------------------+

   📐 COBIT 2019 Goals Cascade (위->아래 Top-Down Decomposition)
```

한국 정보통신산업진흥원(NIPA)의 2023년 보고에 따르면 국내 500대 기업의 **78%가 IT 거버넌스 체계를 도입**했으나, 이 중 **34%만 "성공적으로 운영되고 있다"**고 응답했다. 실패 원인의 60%는 "CEO-이사회-CIO 간 책임 소재 불명확", 25%는 "측정 지표 부재", 15%는 "변화관리(Change Management) 미흡"으로 분석된다. 이는 IT 경영관리가 단순한 프레임워크 도입이 아닌 **조직 문화(Culture)와 거버넌스 성숙도(Governance Maturity)의 동반 성장**이 필수임을 시사한다.

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **배의 키잡이(Helmsman)**와 같습니다. 키잡이는 항로(Strategy)를 정하고, 돛대(RACI)를 세우며, 뱃머리(Dashboard)에서 풍향·조류·깊이(Metrics)를 실시간으로 확인합니다. 폭풍(Disruption)이 칠 때 흔들리지 않는 것은 선체(Framework)가 견고하기 때문이지, 키잡이가 팔이 세서(권력)가 아닙니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019 거버넌스 시스템은 **Governance Objectives(40개) + Components(7개 범주 40요소) + Design Factors(11개) + Focus Areas(선택적)**의 4축 구조로 설계된다. 핵심 동작 원리는 **"Inputs -> Process -> Outputs -> Outcomes"**의 4단 I-P-O-O 사이클이며, 각 단계에서 RACI 매트릭스, Capability Level(NIST 0~5), Risk Level(ISO 31000)을 적용한다.

```text
[IT 거버넌스 운영 사이클 - ISO 38500:2015 E-D-M Model]

   +------------------- EVALUate (평가) ------------------+
   |  +----------------------------------------------+    |
   |  | ① IT 전략과 비즈니스 목표 정합성 평가            |    |
   |  |    - Strategic Alignment Score (SAS) 측정     |    |
   |  |    - Portfolio ROI Gap Analysis               |    |
   |  |    - 외부 벤치마크 (Gartner Magic Quadrant)    |    |
   |  +----------------------------------------------+    |
   |                          |                            |
   |                          v                            |
   +------------------- DIRECT (지시) --------------------+
   |  +----------------------------------------------+    |
   |  | ② 이사회-경영진-CIO 간 책임·권한 위임 구조 설정 |    |
   |  |    - RACI Matrix (Responsible, Accountable)    |    |
   |  |    - IT Strategy Committee 구성               |    |
   |  |    - 의사결정 권한 매트릭스 (DA - Decision Auth)|   |
   |  |    - 정책(Policy)·표준(Standard)·절차(Procedure)|   |
   |  +----------------------------------------------+    |
   |                          |                            |
   |                          v                            |
   +------------------- MONITOR (모니터) -----------------+
   |  +----------------------------------------------+    |
   |  | ③ 성과·위험·규제 준수 여부 지속 측정·보고       |    |
   |  |    - Balanced Scorecard (재무/고객/내부/학습)  |    |
   |  |    - KRI (Key Risk Indicator) 대시보드         |    |
   |  |    - 내부감사 (IIA Standard 2110)              |    |
   |  |    - 외부감사 (ISAE 3402 Type II)              |    |
   |  |    - PDCA: Plan-Do-Check-Act Cycle            |    |
   |  +----------------------------------------------+    |
   |                          |                            |
   |                          +-------> (반복·개선) <-------+|
   +-------------------------------------------------------+

   📊 5개 도메인 × 40개 관리목표 매핑
   EDM (Evaluate, Direct, Monitor) --- 거버넌스 (5)
   APO (Align, Plan, Organize) -------- 계획/조직 (14)
   BAI (Build, Acquire, Implement) ---- 구축/구현 (11)
   DSS (Deliver, Service, Support) ---- 서비스/지원 (6)
   MEA (Monitor, Evaluate, Assess) ---- 모니터/평가 (4)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(거버넌스 시스템)** | Evaluate-Direct-Monitor 의사결정 사이클 | 이사회·IT Steering Committee가 KPI 대시보드(Tableau, Power BI) 기반 분기별 검토. **EDM01(거버넌스 프레임워크 수립)**, EDM02(가치 전달 보장), EDM03(위험 최적화), EDM04(자원 최적화), EDM05(이해관계자 투명성) 5개 목표 |
| **APO(계획·조직·정렬)** | IT 전략-비즈니스 전략 정렬 및 자원 배분 | **APO02(전략 관리)**에서 BCG/Gartner Matrix로 IT 포트폴리오 분류 - Run-the-Business(60%), Grow-the-Business(30%), Transform-the-Business(10%)의 황금 비율 적용. APO12(위험 관리)는 ISO 31000 Risk Appetite Statement와 연계 |
| **BAI(구축·획득·구현)** | 솔루션 개발·도입·변경 관리 | **BAI03(솔루션 아키텍처 관리)**에서 TOGAF 10 ADM(Architecture Development Method) 적용. BAI11(프로젝트 관리)는 PMBOK 7th의 8개 성능 영역 + 애자일 하이브리드(Scrumban/Kanban) 활용. 변경 관리 시 CAB(Change Advisory Board) 승인 필수 |
| **DSS(서비스·지원·전달)** | IT 서비스 운영·사용자 지원·보안 운영 | **DSS02(서비스 요청 및 인시던트 관리)**에서 ITIL 4 Incident Management Practice 적용 - P1(1시간 내), P2(4시간), P3(24시간), P4(72시간) SLA 단계화. DSS05(보안 운영)는 SIEM(Splunk, QRadar) 24×7 모니터링 |
| **MEA(모니터·평가·감사)** | 거버넌스 성과 측정 및 개선 | **MEA01(성과 및 컨FORMANCE 모니터링)**에서 BSC 4관점 + COBIT Capability Level(0: Incomplete, 1: Initial, 2: Managed, 3: Defined, 4: Quantitative, 5: Optimizing) PAM(Process Assessment Model) 활용. MEA04(내부 통제)는 SOX 404 또는 내부회계관리제도 연계 |

COBIT 2019의 **11개 Design Factor**는 조직별로 거버넌스 시스템을 맞춤 설계하기 위한 핵심 파라미터다: ①Enterprise Strategy, ②Enterprise Goals, ③Risk Profile, ④I&T-related Issues, ⑤Threat Landscape, ⑥Compliance Requirements, ⑦IT Role in IT-related Role, ⑧IT Outsourcing Strategy, ⑨IT Implementation Methods, ⑩Technology Adoption Strategy, ⑪Enterprise Size. 예를 들어 금융사는 ③(위험 프로파일), ⑥(규제 준수: Basel III, 전자금융감독규정) 가중치를 높게, 스타트업은 ①(전략: 차별화), ⑩(기술 도입: First Mover) 가중치를 높게 설정한다.

**Capability Level 측정**은 PAM(Process Assessment Model) 기반으로 7개 속성(PA 1.1~7.1)별 점수를 산출한다. 주요 산식은 다음과 같다:

```
Process Capability Level = Σ(PA
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 788 / 800

<- **이전**: [787. IT 경영 관리 핵심 토픽 787번 시험 요약](/studynote/12_it_management/05_security_compliance/787_it_management_core_topic_787_exam_summary/)
**다음**: [789. IT 경영 관리 핵심 토픽 789번 시험 요약](/studynote/12_it_management/05_security_compliance/789_it_management_core_topic_789_exam_summary/) ->

---
