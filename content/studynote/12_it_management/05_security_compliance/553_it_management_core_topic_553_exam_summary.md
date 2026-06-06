---
title: "IT Management Core Topic 553 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(IT Management)는 **IT 거버넌스(COBIT 2019/ISO 38500) -> IT 전략(Portfolio/Roadmap) -> IT 성과관리(BSC/KPI) -> IT 위험관리(Risk Register)**의 4계층 통합 체계이며, 단순 비용 절감이 아닌 **비즈니스 가치(Value) 창출**과 **이해관계자 책임(Accountability) 확보**가 핵심 메커니즘이다.
> 2. **가치**: Gartner(2024) 기준 성숙한 IT 거버넌스 도입 기업은 **IT 투자 ROI 23~35% 향상**, **프로젝트 실패율 40% 감소**, **규제 준수 비용 28% 절감**, **이해관계자 의사결정 속도 2.1배** 개선 효과를 확인하며, ISO 38500 인증 기업은 주가 대비 기업가치 프리미엄이 평균 7~12% 높게 평가된다.
> 3. **판단 포인트**: 기술사 시험의 핵심 판단 축은 ① **거버넌스 프레임워크 선택**(규제 강도와 산업 특성), ② **IT-비즈니스 정렬(Strategic Alignment) 측정 모델**(SAM: Strategic Alignment Model), ③ **투자 우선순위 의사결정**(NPV/IRR/ROA vs. 옵션가치 Real Options), ④ **성과 측정의 4관점 균형**(재무·고객·내부프로세스·학습성장)이며, 무엇보다 **"운영(Operations) ↔ 혁신(Innovation) ↔ 컴플라이언스(Compliance)"의 3중 트레이드오프**를 어떻게 해소할지가 실무 승부처다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX), 클라우드·AI·데이터 거버넌스 규제(데이터산업법, EU AI Act, DORA) 강등으로 인해, IT 부서는 **"비용 센터(Cost Center)"에서 "비즈니스 전략적 파트너(Value Partner)"로** 역할이 전환되었다. 그러나 2024 McKinsey 설문에 따르면 글로벌 CIO의 67%가 "IT 투자와 비즈니스 성과 간의 인과관계를 입증하지 못한다"고 응답하며, **IT-Business Alignment 갭**이 여전히 경영 최대 리스크 중 하나로 분류된다.

기존의 **전통적 IT 관리(Silo·프로젝트 단위·Capex 중심)**는 다음 한계에 부딪힌다:

1. **IT 투자의 사후 검증 부재**: KPI가 "납기 준수율", "결함률" 등 **활동 지표(Activity Metric)**에 머물러 비즈니스 임팩트 측정 실패
2. **거버넌스 부재**: Shadow IT 증가, 중복 투자, 사이버 리스크 통제 실패
3. **전략 부재**: 매년 30~40%의 IT 예산이 레거시 유지보수(Legacy Maintenance)에 잠식(한국정보화진흥원 2023)
4. **규제 대응 지연**: 개인정보보호법, ESG 공시, 클라우드 보안인증(CSAP) 등 다중 규제 동시 대응 한계

**IT 경영 관리(IT Management)**는 위 한계를 해결하기 위해 **"거버넌스-전략-포트폴리오-성과-위험"**의 통합 프레임워크를 적용하는 경영 discipline이다.

```text
[IT 경영 관리 통합 프레임워크: 5계층 구조]
   +--------------------------------------------------------+
   |  L1. 비즈니스 전략 (Business Strategy)                  |
   |      - 사업목표, 시장 positioning, ESG 목표              |
   |      v 정렬(Align) v                                   |
   +--------------------------------------------------------+
   |  L2. IT 거버넌스 (IT Governance)                        |
   |      - 의사결정권한, 책임, 통제구조                      |
   |      - COBIT 2019, ISO 38500, Raci Chart              |
   |      v 정책(Policy) v                                  |
   +--------------------------------------------------------+
   |  L3. IT 전략 및 포트폴리오 (IT Strategy & Portfolio)    |
   |      - Application / Infrastructure / Investment PPM   |
   |      - Run-Grow-Transform (RGT) 분류                    |
   |      v 로드맵(Roadmap) v                               |
   +--------------------------------------------------------+
   |  L4. IT 운영 및 서비스 (IT Operations & Services)       |
   |      - ITIL 4 Service Value System                      |
   |      - SLA, OLA, UC                                    |
   |      v 측정(Measure) v                                 |
   +--------------------------------------------------------+
   |  L5. 성과 및 위험 관리 (Performance & Risk)             |
   |      - BSC KPI, CSF, KGI                               |
   |      - Risk Register, KRI, KRRI                        |
   +--------------------------------------------------------+
   ※ 피드백 루프: L5 -> L2 (성과/위험 데이터 -> 거버넌스 개선)
```

**📢 섹션 요약 비유**: IT 경영 관리는 마치 **"건물의 설계-시공-유지관리-안전점검을 통합하는 건축 프로젝트 관리 시스템"**과 같다. 설계도면(거버넌스) 없이 현장(운영)만 관리하면 무너지고, 점검이 없으면(성과관리) 붕괴 위험을 인지하지 못한다. 5계층이 모두 연결되어야 튼튼한 건물(기업)이 유지된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **"Decision Rights + Accountability + Value Measurement"**의 3요소를 **5개 핵심 프로세스**로 구현하는 것이다. 아래는 국제 표준(COBIT 2019 + ISO 38500)을 기반으로 한 참조 아키텍처이다.

```text
[IT 경영 관리 프로세스 흐름도]
   +--------------+     +--------------+     +--------------+
   | ① 평가      | ---> | ② 지휘      | ---> | ③ 모니터    |
   | Evaluate     |     | Direct       |     | Monitor      |
   | (현재 진단)  |     | (의사결정)   |     | (측정)       |
   +--------------+     +--------------+     +--------------+
         ^                                          |
         |                                          v
   +--------------+                          +--------------+
   | ④ 보고       | <----------------------- | ⑤ 평가환류  |
   | Report       |                          | Re-evaluate  |
   | (이해관계자) |                          | (개선)        |
   +--------------+                          +--------------+
   [출처: ISO/IEC 38500:2015 Govern IT Model — 6 principles]
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① 거버넌스 의사결정 기구 (Governance Board)** | IT 투자·우선순위·위험 최종 의사결정 | 이사회 산하 IT 전략위원회 + CIO + CDO + CISO + 사업부 대표로 구성, RACI 매트릭스(Responsible/Accountable/Consulted/Informed)로 권한 명확화. 분기 1회 이상 정례 회의, 안건은 **IT 인베스트먼트 카운슬(Investment Council)** 통해 사전 검토 |
| **② IT 전략 및 포트폴리오 관리(PPM)** | IT 투자 포트폴리오 최적화, RGT 분류 | **Run-Grow-Transform 분류**: 유지보수(60~70%) / 경쟁력 강화(20~30%) / 혁신(5~10%)로 예산 배분. **Stage-Gate 프로세스**(아이디어->검토->계획->실행->종료 5단계), **NPV(순현재가치)·IRR(내부수익률)·Payback Period** + **Real Options Valuation(옵션가치)** 혼용 |
| **③ IT 서비스 운영 (IT Service Management)** | 서비스 가치 제공, SLA 관리 | **ITIL 4 Service Value System(SVS)**: Opportunity/Demand -> Value -> Service Value Chain(Plan/Engage/Design & Transition/Obtain/Build/Deliver & Support) -> Value. **SLA 99.9%** 등급별 정의, OLA(운영수준합의)·UC(내부계약서) 3단 위계 |
| **④ 성과 측정 체계 (Performance Measurement)** | KPI/CSF/KGI 도출 및 추적 | **BSC(Balanced Scorecard) 4관점**: ① 재무(ROI, Cost Ratio), ② 고객(NPS, CSAT), ③ 내부프로세스(릴리스리드타임, MTTR), ④ 학습성장(스킬인덱스, 직원만족도). **CSF(Critical Success Factor) -> KPI(Key Performance Indicator) -> KGI(Key Goal Indicator)**의 3단 인과 사슬 |
| **⑤ 위험 및 컴플라이언스 (Risk & Compliance)** | IT 리스크 식별·평가·대응·모니터링 | **ISO 27005 / COBIT 2019 EDM(evaluate-direct-monitor)** Risk Map(Likelihood × Impact 5×5 매트릭스), **KRI(Key Risk Indicator)** 5단계 임계치, **K-Risk-Register** 등록·모니터링. 컴플라이언스 매핑(개인정보보호법, ISMS-P, PCI-DSS, ESG) |

### 핵심 알고리즘/산식

1. **IT 투자 우선순위 점수화 모델(Weighted Scoring Model)**
   `Priority Score = Σ(Wi × Si)`
   - W_i: 가중치(전략적필요성 0.3, ROI 0.25, 리스크감소 0.2, 규제준수 0.15, 기술적타당성 0.1)
   - S_i: 각 평가 기준의 점수(1~5점)

2. **SAM (Strategic Alignment Model, Henderson & Venkatraman 1993)**
   - **Strategy Fit**(사업전략 ↔ IT전략 정합성) + **Functional Integration**(비즈니스 ↔ IT 조직 통합) = 4×4 매트릭스
   - IT-Business Alignment 성숙도 5단계: **Ad-hoc -> Committed -> Established -> Managed -> Optimized**(Luftman 2003 갱신본)

3. **TCO (Total Cost of Ownership) 산정**
   `TCO = 직접비(HW+SW+인건비) + 간접비(교육·다운타임·복구·보안·컴플라이언스)`
   - Gartner 벤치마크: 일반 엔터프라이즈 IT TCO 중 **간접비가 약 45~60%** 차지 (관리되지 않을 시)

4. **BSC 인과 사슬(Strategy Map)**
   ```
   학습성장(스킬^) -> 내부프로세스(효율^) -> 고객만족(가치^) -> 재무성과(ROI^)
   ```
   - 이 4관점 간 인과관계가 깨지면 KPI는 "공허한 숫자"가 됨 (Kaplan & Norton)

**📢 섹션 요약 비유**: IT 경영 관리의 5요소는 **"자동차의 5륜 시스템"**과 같다. 거버넌스(운전대) -> 전략(엔진) -> 운영(구동계) -> 성과(주행계기판) -> 위험관리(브레이크/에어백). 어느 하나만 갖춰도 사고는 막을 수 없으며, 5륜이 동시에 작동해야 목적지(비즈니스 가치)에 안전하게 도착한다.

---

## Ⅲ. 비교 및 연결

### 1) IT 거버넌스 프레임워크 비교

| 구분 | **COBIT 2019** (ISACA) | **ITIL 4** (AXELOS) | **ISO/IEC 38500:2015** |
| :--- | :--- | :--- | :--- |
| **핵심 목적** | IT 거버넌스·경영 통제 프레임워크 | IT 서비스 관리(Service Management) | IT 거버넌스 국제 표준(원칙 기반) |
| **구조** | 5도메인 40개 거버넌스/관리 목적(EDM/Align/Plan/Build/Run/Monitor) | 34개 Practice + Service Value Chain | 6 Principles + 5 Model + Governance Cycle |
| **적용 범위** | 전체 IT 거버넌스(전략~운영 통합) | 주로 IT 운영·서비스 영역 | 이사회의 IT 의사결정 거버넌스 |
| **성숙도 모델** | OGC CMMI 5단계(0~5) | ITIL Maturity Model | 자체 평가 체크리스트(원칙별) |
| **주 사용자** | CIO, 감사인, 컨설턴트, 리스크 관리자 | IT 운영팀, 서비스 데스크, DevOps | 이사회, 임원, 감사위원회 |
| **강점** | ① 40개 통제목표 상세 ② Risk/Compliance 매핑 탁월 ③ 11개 디자인 팩터 맞춤화 | ① 서비스 가치 중심(Value Co-Creation) ② Agile/DevOps 친화 ③ 실용적 운영 노하우 | ① 표준(글로벌 벤치마크) ② 원칙 6개 단순 명료 ③ 모든 조직에 적용 가능 |
| **약점** | 상대적으로 무겁고 복잡(700+ 페이지) | 거버넌스 상위 의사결정 내용은 약함 | 구체적 구현 가이드 부재(원칙만 제시) |
| **한국 활용** | ISMS-P, 클라우드 보안인증 매핑 | 공기업·대기업 IT운영 표준 | 공공부문(행정안전부), 대기업 |

### 2) IT 관리 vs. IT 거버넌스 vs. IT 운영 비교

| 구분 | **IT 경영 관리(Management)** | **IT 거버넌스(Governance)** | **IT 운영(Operations)** |
| :--- | :--- | :--- | :--- |
| **핵심 질문** | 어떻게 IT를 경영하는가? | 누가, 무엇을 결정하는가? | 매일 어떻게 서비스하는가? |
| **범위** | 전략 + 거버넌스 + 운영 통합 | 의사결정권·책임·통제 | 일상적 서비스 제공 |
| **시간축** | 중장기(1~5년) | 분기~연 단위 | 일~주 단위 |
| **주체** | CIO, IT전략팀 | 이사회, IT위원회 | IT운영팀, 헬프데스크 |
| **산출물** | IT전략맵, 포트폴리오, KPI | 정책, RACI, 통제기준 | 인시던트, 변경, 릴리스 |

### 3) 관련 시스템·도구 연계

| 연계 영역 | 연결 포인트 | 대표 도구/표준 |
| :--- | :--- | :--- |
| **EA(Enterprise Architecture)** | IT전략 ↔ 아키텍처 정렬 | TOGAF 10, ArchiMate 3.2, FEAF |
| **프로젝트 관리** | IT포트폴리오 ↔ 개별 프로젝트 | PMBOK 7, PRINCE2, MSP |
| **Agile/DevOps**
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 553 / 800

<- **이전**: [552. IT 경영 관리 핵심 토픽 552번 시험 요약](/studynote/12_it_management/05_security_compliance/552_it_management_core_topic_552_exam_summary/)
**다음**: [554. IT 경영 관리 핵심 토픽 554번 시험 요약](/studynote/12_it_management/05_security_compliance/554_it_management_core_topic_554_exam_summary/) ->

---
