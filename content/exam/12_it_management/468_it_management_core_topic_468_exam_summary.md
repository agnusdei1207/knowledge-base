---
title: "IT Management Core Topic 468 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 토픽 468번은 COBIT 2019, ITIL 4, ISO 27001/38500, NIST CSF, BSC for IT 등 글로벌 IT 거버넌스·서비스 관리 프레임워크를 통합적으로 이해하고, IT 투자 대 IT 성과 간의 인과관계(Value Realization Chain)를 입증할 수 있는 역량을 평가하는 종합 응용형 문항이다.
> 2. **가치**: IT-Business Alignment 성숙도(Level 1~5)를 1단계 향상시킬 경우 ROI가 평균 18~27%(Gartner 2023) 상승하고, IT 다운타임 40% 감소, 컴플라이언스 감사 비용 35% 절감이 가능하여, 경영진 의사결정 정당화와 규제 대응력 강화라는 정성적 가치까지 산출한다.
> 3. **판단 포인트**: "거버넌스(누가 결정) ↔ 관리(어떻게 실행) ↔ 통제(어떻게 검증)"의 3-layer 분리, Push형 중앙집권 모델 vs. Pull형 연방(Federated) 모델 선택, 그리고 CSF(Critical Success Factor) -> KPI -> KGI 인과모델에서 Leading vs. Lagging 지표의 비율(권장 60:40) 설계가 답안의 핵심 차별화 요소다.

---

## Ⅰ. 개요 및 필요성

정보기술이 단순 지원(Support) 기능을 넘어 **전략적 차별화(Strategic Differentiation)** 와 **운영 필수 인프라(Utility)** 의 양면성을 갖게 됨에 따라, IT 투자의 약 70%(IDC, 2023)가 실패하거나 기대 미달 상태로 회수되는 'IT Productivity Paradox'가 반복되고 있다. 토픽 468번은 이러한 모순을 해소하기 위해 **IT 거버넌스·서비스 관리·컴플라이언스·리스크·성과측정** 을 하나의 통합된 메타 프레임워크로 재구성하는 능력을 평가한다.

기존의 siloed 접근(예: 보안팀은 ISO 27001만, 운영팀은 ITIL만, 재무팀은 TCO만)은 동일 사안에 대해 상이한 KPI를 산출하여 C-Level의 의사결정 마비(Decision Paralysis)를 야기했다. 이를 해결하기 위해 등장한 **통합 거버넌스 체계(Integrated Governance Stack)** 가 본 토픽의 핵심이다.

```text
        +--------------------------------------------------------------+
        |           Board / CEO / CISO / CIO Steering Committee       |
        |                  (의사결정 및 책임 소재)                       |
        +------------------------+-------------------------------------+
                                 | 전략적 방향 (RACI Matrix)
                                 v
        +--------------------------------------------------------------+
        |   [Layer 1: GOVERNANCE]                                       |
        |   COBIT 2019  ·  ISO/IEC 38500  ·  ISO 27001 Annex A          |
        |   -> "무엇을(What) · 왜(Why) · 누가(Who)" 정의                  |
        +------------------------+-------------------------------------+
                                 | 정책 -> 통제 목표 -> 관리实践
                                 v
        +--------------------------------------------------------------+
        |   [Layer 2: MANAGEMENT]                                      |
        |   ITIL 4 Service Value System  ·  PMBOK 7  ·  PRINCE2 7.0    |
        |   -> "어떻게(How) · 언제(When) · 어디서(Where)" 실행            |
        +------------------------+-------------------------------------+
                                 | 운영 데이터 / 메트릭
                                 v
        +--------------------------------------------------------------+
        |   [Layer 3: CONTROLS]                                        |
        |   NIST CSF 2.0  ·  CIS Controls v8  ·  K-ISMS  ·  PCI-DSS    |
        |   -> "검증(Verify) · 측정(Measure) · 보고(Report)"              |
        +--------------------------------------------------------------+
                                 |
                                 v
        +--------------------------------------------------------------+
        |   성과 피드백 루프: KPI -> CSF -> KGI -> Strategy Refresh        |
        +--------------------------------------------------------------+
```

기존(As-Is) : 각 부서가 자체 표준 적용 -> 중복 통제(Redundant Controls) 평균 32%, 감사 비용 중복 28% 발생
목표(To-Be) : 단일 통제 맵(Unified Control Map) 기반 자동화 -> SOX·GDPR·PIPA 동시 준수 1-Pass 감사 실현

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라 지휘자** 와 같습니다. 바이올린(ITIL), 첼로(COBIT), 트럼펫(ISO 27001) 등 각 악기(프레임워크)가 제 소리를 내지만, 지휘자(거버넌스)가 없으면 불협화음만 남고, 지휘봉(CSF/KPI) 없이는 박자를 맞출 수 없습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

토픽 468번의 기술적 핵심은 **"Value Realization Chain"** 이다. 입력(Input)인 IT 투자·자원·위험이 어떤 메커니즘을 통해 사업 가치(Outcomes)로 변환되는지의 **인과관계(Inferential Causality)** 를 입증해야 한다.

```text
            [INPUT]              [PROCESS]                [OUTPUT]          [OUTCOME]
        +-------------+      +----------------+       +----------+      +--------------+
        | • CapEx     |      | 1. Portfolio   |       | • Service|      | • KGI        |
        | • OpEx      | ----> |    Selection   | -----> |   Output | ----> |   (사업성과)  |
        | • HR        |      | 2. Architecture|       | • Project|      | • Mission    |
        | • Knowledge |      |    Design      |       |   Output|      |   Achievement|
        +-------------+      | 3. Service     |       | • Change |      +--------------+
                             |    Delivery    |       |   Output |
                             | 4. Risk Mgmt   |       +----------+
                             +----------------+
                                     |
                                     v
                          +--------------------+
                          | Feedback & Learning | <--- CSF가 미흡 시 루프 복귀
                          +--------------------+
```

### COBIT 2019 Governance System 구성요소(40개 관리 목표 중 핵심 발췌)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(Evaluate, Direct, Monitor) — 5개** | 최고 거버넌스 의사결정 | 거버넌스 시스템 자체의 설계·운영·평가, EDM01(거버넌스 프레임워크) ~ EDM05(투명성 보장) |
| **APO(Align, Plan, Organize) — 14개** | 전략->전술 정렬 | APO01(관리 프레임워크), APO04(혁신), APO05(포트폴리오), APO12(리스크), APO13(보안) |
| **BAI(Build, Acquire, Implement) — 11개** | 솔루션 도입·구축 | BAI01(관리 프로그램), BAI02(요구사항 정의), BAI03(투자 결정), BAI11(프로젝트 관리) |
| **DSS(Deliver, Service, Support) — 6개** | 운영·서비스·보안 | DSS01~DSS06(운영, 서비스 요청, 장애, 연속성, 보안 운영, 비즈니스 통제) |
| **MEA(Monitor, Evaluate, Assess) — 4개** | 통제·측정·평가 | MEA01(성과·동시 모니터링), MEA02(내부 통제), MEA03(외부 요구사항), MEA04(감사) |

### ITIL 4 Service Value Chain (SVC) — 6개 활동의 인과 흐름

```text
        Demand ---> [Plan] ---> [Engage] --+
                                          v
        Value <--- [Obtain/Build] <--- [Design & Transition] <--- [Deliver & Support]
                          ^                                    |
                          +---------- [Improve] <---------------+
                                       (지속적 개선)
```

| 활동 | 핵심 입력 | 핵심 산출 | 연계 프레임워크 |
| :--- | :--- | :--- | :--- |
| Plan | 전략, 포트폴리오, 아키텍처 | 가치네트워크 설계, SLO | COBIT APO05 |
| Engage | 이해관계자 니즈 | SLA, 경험지표(XLA) | ISO 38500 |
| Design & Transition | 요구사항 | 카탈로그, 릴리스 | PMBOK 7, DevOps |
| Obtain/Build | 공급망, 계약 | 컴포넌트, 용량 | SIAM, COBIT BAI03 |
| Deliver & Support | 티켓, 이벤트 | 안정적 서비스 | ITSM, AIOps |
| Improve | 메트릭, 인시던트 데이터 | 개선 백로그 | Kaizen, Lean IT |

### 핵심 정량 파라미터 (Value Realization 수식)

**ROI 산식**:
> `IT ROI = (Tangible Benefits + Intangible Benefits) - Total Cost of Ownership`
> 여기서 `TCO = CapEx + OpEx + Hidden Cost(Shadow IT 8~15% 가산)`

**CSF -> KPI -> KGI 인과 매트릭스 (예시)**:

| CSF (Critical Success Factor) | KPI (Leading) | KGI (Lagging) |
| :--- | :--- | :--- |
| 인시던트 예방 역량 | MTTD ≤ 15분, 패치 적용률 ≥ 98% | 시스템 가용성 ≥ 99.95%, 고객 이탈률 v 1.2%p |
| 프로젝트 성공률 | 단계별 Gate 통과율, 요구사항 변경률 ≤ 5% | Go-Live 후 6개월 ROI ≥ 15% |
| 보안 거버넌스 | 취약점 평균 폐쇄시간 ≤ 7일 | 데이터 유출 사고 0건, MTTR ≤ 4시간 |
| IT-Business 정렬 | 전략적 프로젝트 비율 ≥ 70% | 매출 대비 IT기여도 4.2% (산업 평균 대비 +0.8%p) |

**성숙도 모델 (CMMI 기반 5단계)**:
Level 1 Initial -> Level 2 Managed -> Level 3 Defined -> Level 4 Quantitatively Managed -> Level 5 Optimizing.
기술사 답안에서는 "현재 Lv.2 Managed, 목표 Lv.4 Quantitatively Managed, 18개월 로드맵" 같은 **정량적 단계 표시** 가 고득점 요소.

- **📢 섹션 요약 비유**: Value Realization Chain은 **씨앗을 심어 열매를 거두는 농사** 와 같습니다. 씨앗(투입) -> 물·비료(프로세스) -> 꽃(산출) -> 열매(성과)의 4단계를 건너뛰면 아무리 좋은 씨앗이라도 거둘 것이 없듯, 거버넌스도 Input->Outcome의 인과 고리를 끊지 않아야 합니다.

---

## Ⅲ. 비교 및 연결

토픽 468번은 여러 유사 프레임워크의 **경계(Boundary)** 와 **적용 시나리오** 를 명확히 구분할 수 있어야 한다.

| 구분 | COBIT 2019 | ITIL 4 | ISO 27001/38500 | PMBOK 7 | NIST CSF 2.0 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **핵심 초점** | 거버넌스 & 관리 목표 40개 | 서비스 가치 사슬 (SVC) | 통제 목표 / 거버넌스 원칙 6개 | 프로젝트 관리 원칙 12개 | 보안 기능 6개 (GV, ID, PR, DE, RS, RC) |
| **주 사용자** | CIO, 이사감사, 내부감사 | ITSM 담당자, 서비스 매니저 | CISO, 컴플라이언스 | PMO, 프로젝트 매니저 | SOC, CIRT |
| **출력물** | Maturity Profile, RACI | Service Value Chain Map | Statement of Applicability (SoA) | Project Charter, WBS | Tier별 보안 프로파일 |
| **측정 관점** | Process Capability (0~5) | 34 Practices Maturity | 93 Annex A 통제 항목 적합성 | Project Performance Domain | Function/Category/Subcategory |
| **결합 방식** | 상위 정책 | 하위 실행 매뉴얼 | 횡단 통제 | 프로젝트별 적용 | 보안 운영 KPI |
| **한계** | 기술 구현 가이드 부재 | 거버넌스 의사결정 모델 약함 | 인증 비용 부담, 갱신 3년 | 운영·서비스 영역 미포함 | 미국 규제 친화적 (한국 K-ISMS와 매핑 필요) |

### 다른 기술 영역과의 연결

| 연계 영역 | 연결 포인트 | 통합 시 효과 |
| :--- | :--- | :--- |
| **EA (TOGAF 10 / DoDAF 2.02)** | COBIT APO02(아키텍처 관리)와 직접 매핑 | BCM(비즈니스 능력 모델) -> IT Capability -> 서비스 카탈로그 트레이서빌리티 확보 |
| **DevOps / SRE** | ITIL DSS04~06(장애·문제) ↔ SRE Error Budget | MTTR 40% v, 변경 실패율 25% v (DORA 2023) |
| **Zero Trust Architecture** | NIST CSF PR.AC-1~7 ↔ ISO 27001 A.5.15~A.8.20 | 마이크로세그멘테이션과 IAM 통제 통합, 횡이동(Lateral Movement) 80% 차단 |
| **ESG / 지속가능경영** | COBIT EDM02(위험 최적화) ↔ GRI Standards | Green IT 지표(kWh per transaction) 도입, Scope 3 배출량 산출 |
| **공급망 보안 (C-SCRM)** | NIST SP 800-161 ↔ COBIT APO10(공급업체) | SBOM 기반 취약점 가시화, 4th-party risk까지 추적 |

- **📢 섹션 요약 비유**: 각 프레임워크는 **의료 진료과** 와 같습니다. COBIT은 내과(전체 진단), ITIL은 외과(서비스 시술), ISO 27001은 감염내과(보안), PMBOK은 정형외과(프로젝트 구조), NIST CSF는 응급의학과(보안 사고 대응) — 단일 과 진료만으로는 병을根治할 수 없듯, 5개과 통합 진료(Integrated Governance)가 필수입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **현재 거버넌스 성숙도 측정**: COBIT 2019 PAM(Process Assessment Model) 기반으로 EDM/APO/BAI/DSS/MEA 40개 프로세스 중 **최소 15개 핵심 프로세스** 의 Capability Level(0~5)을 객관 측정하고
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 468 / 800

<- **이전**: [467. IT 경영 관리 핵심 토픽 467번 시험 요약](/studynote/12_it_management/05_security_compliance/467_it_management_core_topic_467_exam_summary/)
**다음**: [469. IT 경영 관리 핵심 토픽 469번 시험 요약](/studynote/12_it_management/05_security_compliance/469_it_management_core_topic_469_exam_summary/) ->

---
