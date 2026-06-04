---
title: "602. IT 경영 관리 핵심 토픽 602번 시험 요약 (IT Management Core Topic 602 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019(목표 계층형 5단계 + 포커스 영역 40개), ISO/IEC 38500(원칙·모형·평가의 3축), ITIL 4(서비스 가치 시스템·34개 실무 가이드)을 통합하여, **이사회-경영진-IT** 3계층의 의사결정 권한·책임·보고 체계(Three Lines Model)를 정렬하는 경영 통제 체계이다.
> 2. **가치**: 글로벌 IDC 조사에서 COBIT 기반 거버넌스 도입 기업은 IT 투자 대비 ROI가 평균 28% 향상되고, IT 리스크 사고 발생률은 35~45% 감소하며, ISO 38500 인증 기업은 규제 준수 비용 22% 절감 효과를 보고한다.
> 3. **판단 포인트**: **거버넌스 vs 관리(Governance vs Management)** 경계(전략적 방향 vs 운영적 활동), **단일 프레임워크 채택 vs 통합 매핑**(COBIT Cascade를 통한 우선순위 도출), **규제 강도(Compliance Intensity)**에 따른 통제 빈도 설계, 그리고 **디지털 전환 환경에서 Agile/DevOps 거버넌스 재설계** 여부가 핵심 트레이드오프다.

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 비용 센터(Cost Center)에서 사업의 핵심 경쟁력(Strategic Differentiator)으로 이동하면서, IT 투자의 의사결정·실행·측정 체계에 대한 **이사회 수준의 통제 메커니즘**이 요구되었다. 1990년대 연방정부 CIO 직제 도입, 2002년 사베인즈-옥슬리법(SOX 404) IT 내부통제 의무화, 2018년 EU GDPR 시행, 2024년 AI Act(고위험 AI 시스템 위험관리 의무화) 등 규제 환경이 강화되면서 IT 거버넌스는 선택이 아닌 **필수의 경영 인프라**가 되었다.

특히 한국 환경에서는 2021년 개정 개인정보보호법, 2022년 정보통신망법 개정(가명정보 도입), 2023년 시행된 데이터 산업법, 그리고 2024년 공공부문 AI 도입·활용 가이드라인이 IT 거버넌스 프레임워크의 통제 항목(Control Objective)을 직접 정의하고 있어, 단순 모범 사례 차원을 넘어 **규제 준수(Regulatory Compliance)** 차원의 거버넌스 설계가 불가결하다.

```text
[IT 거버넌스의 진화: 기술 관리 -> 경영 통제 -> 가치 창출 -> 디지털 신뢰]

  1980s          1990s          2000s          2010s          2020s~
  +------+     +------+     +------+     +------+     +------+
  |  IT  |     |  IS  |     |  IT  |     |  IT  |     |Digital|
  | Mgmt | ---> | Audit| ---> | GOV. | ---> | Value| ---> |Trust |
  |      |     |      |     |      |     |      |     |      |
  +------+     +------+     +------+     +------+     +------+
  (Data Proc)  (COSO/COBIT   (SOX 404,    (BSC/Digital   (AI 거버,
                코빗 4.0/5)    ISO 38500)   Transformation) Zero-Trust,
                                                              ESG·AI윤리
   ※ 기술 관점      ※ 통제 관점     ※ 의사결정 관점    ※ 가치·신뢰 관점
```

IT 거버넌스가 없으면 발생하는 전형적 실패 패턴은 **"Shadow IT"**(전체 IT 지출의 30~40%, Gartner 2023 통계), 이중/삼중 투자(중복 시스템), 이해관계자 간 KPI 충돌(예: 개발팀 속도 vs 운영팀 안정성), 그리고 사후 통제(Powerful Audit) 부재로 인한 대규모 리스크 노출이다. 반대로 적절한 거버넌스는 **IT 투자 우선순위 정렬(Strategic Alignment)**, **위험 가시화(Risk Transparency)**, **자원 최적화(Resource Optimization)**, **성과 측정(Performance Measurement)**의 4대 효과를 통해 IT를 "비용"에서 "전략 자산"으로 전환시킨다.

- **📢 섹션 요약 비유**: IT 거버넌스는 자동차의 **'운전면허 시스템 + 신호등 + 블랙박스'**와 같다. 운전면허(이사회)는 운전 규칙(원칙)을 정하고, 신호등(정책·통제)은 실시간으로 차량(프로젝트·서비스)의 움직임을 통제하며, 블랙박스(모니터링·감사)는 사고 발생 시 원인을追溯한다. 이 세 가지가 없으면 아무리 좋은 차(IT 시스템)도 사고가 끊이지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1) COBIT 2019 — 6단계 거버넌스 시스템 구성

COBIT 2019는 **Governance and Management Objectives**(40개)로 재구성되었고, **핵심 모델(Core Model)**과 **포커스 영역(Focus Area)** 개념이 추가되어 상황별 확장이 가능하다.

```text
[COBIT 2019 Governance System 구축 프로세스]

  ① 비즈니스 drivers/dangers   ->   ② 전략적 목표 연계(Goals Cascade)
        |                                       |
        v                                       v
  ③ 초기 거버넌스 시스템 설계   <---   ④ 위험 요인 식별(Risk Factors)
        |                                       |
        |      +------------------+             |
        |      | 40개 Governance  |             |
        |      |    Objectives    |             |
        |      |  +------+------+ |             |
        |      |  | EDM  |  5개 | |  Evaluate, Direct, Monitor
        |      |  +------+------+ |  (이사회 수준)
        |      |  | Align |Plan | |
        |      |  |  &    | Org | |  4개 영역
        |      |  |Organ.+------+ |  × 6~7개 관리 목적
        |      |  +------+------+ |
        |      |  | Build | Run  | |
        |      |  +------+------+ |
        |      |  | Monitor|     | |
        |      |  +------+------+ |
        v      +------------------+
  ⑤ 거버넌스/관리 목표 우선순위 결정
        |
        v
  ⑥ Components 설계
        +- Process (40)
        +- Organizational Structures
        +- Information Flows
        +- People, Skills, Competencies
        +- Policies & Procedures
        +- Culture, Ethics, Behavior
        +- Services, Infrastructure, Applications
        +- People, Technology, Facilities

  +------------------------------------------------+
  |  N: 발생 횟수 | COBIT 2019 = Σ (40목표 × 7구성) |
  |  통제 강도 = f(리스크, 컴플라이언스, 복잡도)   |
  +------------------------------------------------+
```

### 2) ISO/IEC 38500:2015 — IT 거버넌스 국제 표준

ISO 38500은 6대 **원칙(Principles)**, **모형(Model)**, **평가(Evaluation)**의 3축으로 구성되며, 모든 IT 의사결정이 이 원칙을 준수해야 함을 명시한다.

```text
[ISO 38500:2015 6대 원칙 - "R.A.R.C.I.C"]

  +---------------------------------------------------------+
  |  1. Responsibility  (책무성)   - 개인·조직의 책임 명확화 |
  |  2. Accountability  (의무성)   - 이사회 보고·승인 체계   |
  |  3. Strategy        (전략성)   - 비즈니스 전략 정렬      |
  |  4. Acquisition     (획득성)   - 합리적 의사결정          |
  |  5. Performance     (성과성)   - 서비스·가치 측정         |
  |  6. Conformance     (준수성)   - 법·내부규정 준수         |
  +---------------------------------------------------------+

        +----------------+         +------------------+
        |  Board/Owner   | -------> |   6 Principles   |
        | (이사회/경영진) |         |   기반 판단      |
        +--------+-------+         +--------+---------+
                 |                          |
                 v                          v
        +----------------------------------------+
        |   Evaluate -> Direct -> Monitor (E-D-M)  |
        |   (Cycle: Plan-Do-Check-Act 기반)       |
        +----------------------------------------+
                          |
        +-----------------+-----------------+
        v                 v                 v
   Current State       Future State     Transition Plan
   (As-Is 진단)        (To-Be 목표)     (단계별 실행)
```

### 3) Three Lines Model (IIA, 2020) — 통제 역할 분담

```text
[Three Lines Model - IIA 2020 개정]

  +---------------------------------------------+
  |  외부 이해관계자 (Regulator, Shareholder)   |
  +------------------+--------------------------+
                     | 신뢰/보고
  +------------------v--------------------------+
  |   1st Line: 운영 부서 (Owns & Manages Risk) |
  |   - 사업 owner, IT 운영팀, 개발팀           |
  |   - 일상의 리스크 식별·관리·통제            |
  +------------------+--------------------------+
                     | 정보 제공/지원
  +------------------v--------------------------+
  |   2nd Line: 리스크/컴플라이언스/보안        |
  |   - CRO, CISO, 데이터 거버넌스 오피스       |
  |   - 정책·표준·모니터링·자문                |
  +------------------+--------------------------+
                     | 독립적 보증
  +------------------v--------------------------+
  |   3rd Line: 내부감사 (Internal Audit)       |
  |   - 독립적 assurance 제공                   |
  |   - 이사회 감사위원회 보고                  |
  +---------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **이사회 / IT 전략위원회** | IT 거버넌스의 최고 의사결정 기구 | COBIT EDM(5개 목표: 프레임워크, 가치 전달, 리스크 최적화, 자원 관리, 투명성 보장) 준수, 분기별 의사결정 사이클, RACI 매트릭스로 권한 위임 명확화 |
| **거버넌스 사무국 / PMO** | 거버넌스 시스템 운영·통합·표준화 | COBIT 2019 7개 구성요소(Components) 통합 관리, GRC(Governance-Risk-Compliance) 플랫폼 운영, **Governance Health Check** 분기별 수행 |
| **Risk & Compliance Office** | 리스크 식별·평가·대응·보고 | ISO 31000 연계 리스크 등록부(Risk Register), **KRI(Key Risk Indicators)** 모니터링, 컴플라이언스 매핑(개인정보보호법, ISMS-P, PCI-DSS) |
| **내부감사 / 외부감사** | 통제 효과성 독립 검증 | **Risk-Based Audit Plan** 수립, COBIT Process Assessment Model(PAM) 기반 성숙도 평가(Maturity Level 0~5), 발견사항(Action Plan) 후속조치 관리 |
| **서비스 운영 / ITSM** | 일상의 IT 서비스·프로젝트 거버넌스 적용 | ITIL 4 34개 실무 가이드 활용, **SLA/SLO/SLI** 3단 구조로 서비스 수준 통제, Agile/SAFe 거버넌스(PI Planning, RTE) 통합 |
| **모니터링·보고 체계** | 성과 측정 및 의사결정 지원 | **IT-Balanced Scorecard** 4관점(사용자, 운영, 미래, 재무), 대시보드(BMC Helix, ServiceNow GRC, Archer) 통한 실시간 KPI 추적 |

### 핵심 파라미터 및 산식

**① COBIT 성숙도 평가 (Process Maturity Level)**
$$M = \frac{\sum_{i=1}^{n} (P_i \times W_i)}{\sum_{i=1}^{n} W_i}$$
- $P_i$: 각 프로세스 평가 점수 (0~5), $W_i$: 비즈니스 중요도 가중치
- Level 0(Incomplete) ~ Level 5(Optimizing) 6단계

**② ISO 38500 준수율 (Governance Compliance Rate)**
$$GCR(\%) = \frac{\text{준수 통제 수}}{\text{전체 필수 통제 수}} \times 100 \times (1 - \text{Risk Factor})$$

**③ Three Lines 효과성 지수**
$$ELI = \alpha \cdot L1_{effect} + \beta \cdot L2_{effect} + \gamma \cdot L3_{assurance}$$
- 일반적으로 α=0.4, β=0.3, γ=0.3 (가중 평균)

- **📢 섹션 요약 비유**: COBIT는 **"도요타 생산 방식의 IT 버전"**이라고 할 수 있다. 표준화된 7개 부품(Components)으로 모든 차종(기업)을 조립할 수 있고, ISO 38500은 **"국제 운전면허"**, Three Lines는 **"경찰·보험·블랙박스 3중 안전망"**이다. 이 셋이 맞물려야 사고 없는 IT 운영이 가능하다.

---

## Ⅲ. 비교 및 연결

### 1) 주요 거버넌스/관리 프레임워크 비교

| 구분 | COBIT 2019 | ISO 38500 | ITIL 4 | COSO 2013 (ERM) | PMBOK 7 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스/관리 통합 프레임 | IT 의사결정 원칙·평가 표준 | IT 서비스 운영·관리 | 전사 리스크 관리·내부통제 | 프로젝트 관리 지식 체계 |
| **대상 계층** | 이사회 ~ 실무 (전 계층) | 이사회/경영진 중심 | 실무 운영/서비스 팀 | 전사 + IT 부서 | PM/프로젝트 실무 |
| **핵심 구성** | 40 Objectives × 7 Components | 6 Principles + EDM Cycle | 34 Practices + SVS | 5 Components × 17 Principles | 12 Principles + 8 Domains |
| **강점** | 목표 계층화, 포커스 영역 확장성 | 국제 표준, 간결성·원칙 중심 | 서비스 가치·실무 가이드 풍부 | 리스크·통제·재무 연계 | 프로젝트 라이프사이클 |
| **한계** | 학습 곡선 높음, 운영·기술 통제 빈약
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 602 / 800

<- **이전**: [601. IT 경영 관리 핵심 토픽 601번 시험 요약](/studynote/12_it_management/05_security_compliance/601_it_management_core_topic_601_exam_summary/)
**다음**: [603. IT 경영 관리 핵심 토픽 603번 시험 요약](/studynote/12_it_management/05_security_compliance/603_it_management_core_topic_603_exam_summary/) ->

---
