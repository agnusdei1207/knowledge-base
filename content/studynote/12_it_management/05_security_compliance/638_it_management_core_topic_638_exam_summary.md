+++
title = "638. IT 경영 관리 핵심 토픽 638번 시험 요약 (IT Management Core Topic 638 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스(Governance)는 COBIT 2019의 5개 도메인(EDM·APO·BAI·DSS·MEA)·40개 관리 목표와 ISO/IEC 38500의 6원칙(책임·전략·획득·성과·준합·인적)을 결합하여, 이사회-경영진-IT조직 간 의사결정·책임·감독 체계를 제도화한 통합 경영 프레임워크이다.
> 2. **가치**: 글로벌 조사(IBM·ISACA 공동, 2023)에 따르면 성숙한 IT 거버넌스 체계 보유 기업은 IT 투자 ROI가 평균 28% 높고, 보안사고 발생 시 복구비용이 35% 감소하며, IT-Business 전략 정렬도(Alignment Index)가 4.2/5.0 수준으로 비성숙 기업(2.4) 대비 1.75배 우수하다.
> 3. **판단 포인트**: 핵심 트레이드오프는 ①**중앙집중형(Federated) vs 분산형** 거버넌스 모델 선택, ②**규범 통제(Compliance-First) vs 가치창출(Value-First)** 비중, ③**워터폴(연 1회) vs 애자일(분기) 거버넌스 사이클**이며, 조직 규모·업종·규제 환경에 따라 3대 변수 균형점을 산정해야 한다.

---

## Ⅰ. 개요 및 필요성

디지털 트랜스포메이션(DX), 생성형 AI(LLM) 도입, 클라우드 마이그레이션, ESG 공시 의무화 등 IT가 기업 핵심 경쟁력의 중심축으로 이동하면서, **"IT는 더 이상 비용센터(Cost Center)가 아니라 전략적 자산(Strategic Asset)"** 이라는 경영학적 대전환이 일어났다. 그러나 한국정보화진흥원(NIA) 조사(2023) 결과, 국내大中型 기업 64%가 IT 투자 회수·성과 측정에 어려움을 겪고 있으며, IDC 보고서(2024)에서도 글로벌 IT 지출의 약 30%(약 4.7조 달러)가 가치 미창출 구간("Digital Drag")에서 낭비되는 것으로 나타났다. 이는 곧 **"IT 거버넌스 부재"** 가 기업 가치를 잠식하는 구조적 문제로 부상했음을 의미한다.

기존의 IT 관리는 ITIL 기반의 서비스 운영(SLA, Incident·Change Management)에 머물러 **"운영 효율"** 만을 추구했다. 그러나 2000년대 이후 스톡법(SOX Act)·EU GDPR·한국 개인정보보호법 등 규제 강화와 COVID-19 이후의 가속화된 디지털 전환으로 인해, **"IT가 만들어내는 비즈니스 가치의 측정·최적화·위험 통제"** 라는 보다 거시적·전략적 차원의 관리 체계를 요구하게 되었다. 이러한 시대적 요구에 부응하여 등장한 것이 **COBIT(Control Objectives for Information and Related Technologies)** 과 **ISO/IEC 38500 IT Governance Standard** 이며, 본 토픽은 이 두 표준을 중심으로 IT 경영 관리의 근간을 다룬다.

```text
[기존 IT 관리 → IT 거버넌스로의 패러다임 전환]
┌─────────────────────────────────┐    ┌─────────────────────────────────┐
│   IT 운영 관리 (Operation-Led)   │    │   IT 거버넌스 (Governance-Led)    │
├─────────────────────────────────┤    ├─────────────────────────────────┤
│  • ITIL v3/v4 (서비스 라이프사이클)│    │  • COBIT 2019 (40 관리목표+5도메인)│
│  • SLA / Incident Mgt            │    │  • ISO 38500 (6원칙, E-D-M 모델)  │
│  • 비용·일정·품질 (3P)            │    │  • 거버넌스 시스템·프레임워크·구조  │
│  • CIO + IT조직 중심              │    │  • 이사회·경영진·CIO·사업부 공동책임│
│  • Reactive (장애 대응)            │    │  • Proactive (리스크 사전 식별·통제)│
│  • Back-office Cost Center        │    │  • Strategic Value Driver (가치동인)│
└─────────────────────────────────┘    └─────────────────────────────────┘
                  │                                       │
                  └────────────── 패러다임 점프 ───────────┘
                       (COBIT 2019 발표 2018, ISO 38500:2015 갱신)
```

- **📢 섹션 요약 비유**: 기존 IT 관리가 **"건물의 설비·소방·청소를 관리하는 건물 관리사(BMS)"** 라면, IT 거버넌스는 **"건물의 위치·층수·임차 전략·투자 수익률까지 결정하는 부동산 펀드 매니저"** 이다. 단순 유지보수가 아니라, 건물 자체가 창출하는 가치를 극대화하는 의사결정 체계이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 거버넌스의 핵심 아키텍처는 **COBIT 2019** 의 계층 구조와 **ISO/IEC 38500:2015** 의 3단 모델(Evaluate-Direct-Monitor) 로 설명할 수 있다.

```text
[IT 거버넌스 통합 참조 모델 (COBIT 2019 + ISO 38500)]
┌──────────────────────────────────────────────────────────────────┐
│  Layer 1: 거버넌스 원칙 (ISO 38500 6원칙 + COBIT 5원칙)         │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 1.Responsibility  2.Strategy  3.Acquisition                │ │
│  │ 4.Performance     5.Conformance 6.Human Behavior            │ │
│  └─────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────┤
│  Layer 2: 거버넌스 시스템 (COBIT 2019, 5개 도메인·40개 목표)    │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────┐  │
│  │ EDM      │ APO      │ BAI      │ DSS      │ MEA          │  │
│  │ Governance│ Align    │ Build    │ Deliver  │ Monitor      │  │
│  │ (5 목표) │ (14 목표)│ (11 목표)│ (6 목표) │ (4 목표)     │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────────┘  │
├──────────────────────────────────────────────────────────────────┤
│  Layer 3: 3단 의사결정 사이클 (E-D-M)                            │
│  Evaluate(평가) → Direct(지시) → Monitor(감독) → (반복)         │
├──────────────────────────────────────────────────────────────────┤
│  Layer 4: 컴포넌트 (목표-메트릭-실무-역할)                       │
│  • Process RACI Matrix (R/A/C/I)                                 │
│  • Capability/Maturity Level (0~5)                               │
│  • Information Flow + People + Skill                            │
└──────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM (Evaluate, Direct, Monitor)** | 거버넌스의 최상위 의사결정 계층. 이사회·경영진이 IT 투자 포트폴리오, 리스크 허용 한도, 의사결정 구조를 결정 | 5개 관리 목표: EDM01(거버넌스 체계 수립), EDM02(가치 전달 보장), EDM03(리스크 최적화), EDM04(자원 최적화), EDM05(이해관계자 투명성) |
| **APO (Align, Plan, Organize)** | 전략 정렬·계획·조직 설계. IT 전략이 비즈니스 목표와 어떻게 연결되는지 정의 | 14개 관리 목표: APO01~14. 예) APO02(전략), APO05(포트폴리오), APO12(리스크), APO13(보안) |
| **BAI (Build, Acquire, Implement)** | 솔루션 설계·구축·전환 관리. SDLC, Agile, DevOps를 거버넌스 통제 하에 배치 | 11개 관리 목표: BAI01(프로그램), BAI03(솔루션), BAI05(전환), BAI11(프로젝트 종료 관리) |
| **DSS (Deliver, Service, Support)** | 운영·서비스 지원. ITIL·SIAM과 연계되며 실질적 서비스 제공 단계 | 6개 관리 목표: DSS01(운영), DSS02(서비스 요청·사고), DSS03(문제), DSS04(연속성), DSS05(보안 운영), DSS06(비즈니스 프로세스 통제) |
| **MEA (Monitor, Evaluate, Assess)** | 성과 측정·내부통제·감사. BSC·KPI·컴플라이언스 검증 | 4개 관리 목표: MEA01(성과·준수 모니터), MEA02(내부 통제 시스템), MEA03(외부 요구사항 준수), MEA04(감사) |

핵심 알고리즘적 관점에서 COBIT 2019는 **"목표 계단식 연쇄(Cascading Goals)"** 메커니즘을 채택한다. 이는 ①13개의 **기업 목표(Enterprise Goals)** → ② 연계된 **IT 관련 목표(Alignment Goals)** → ③ 40개의 **관리 목표(Process Goals)** → ④ ④**메트릭(Process Metrics)** 로 4단계 인과 사슬을 구성하며, 각 단계 간 "P(primary)/S(secondary)" 영향도를 정의하여 **Balanced Scorecard(BSC)** 의 4관점(재무·고객·내부·학습성장)에 매핑한다. 이 모델은 Kaplan-Norton BSC + Henderson Venkatraman IT-Business Alignment Matrix의 통합 일반화로 이해할 수 있다.

- **📢 섹션 요약 비유**: COBIT의 5개 도메인은 **"배구 경기의 5개 포지션"** 과 같다. EDM이 **감독·코치** 라면 APO는 **세트 위 전략**(어디에 공을 내려칠지), BAI는 **공격수(점수 만들기)**, DSS는 **수비(상대 공격 차단)**, MEA는 **비디오 판독(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 638 / 800

← **이전**: [637. IT 경영 관리 핵심 토픽 637번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/637_it_management_core_topic_637_exam_summary/)
**다음**: [639. IT 경영 관리 핵심 토픽 639번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/639_it_management_core_topic_639_exam_summary/) →

---
