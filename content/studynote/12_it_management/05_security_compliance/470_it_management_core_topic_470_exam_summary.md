+++
title = "470. IT 경영 관리 핵심 토픽 470번 시험 요약 (IT Management Core Topic 470 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 COBIT 2019의 40개 관리목표(EDM: 5개, Align/Plan/Organize: 14개, Build/Acquire/Implement: 11개, Deliver/Service/Support: 6개, Monitor/Evaluate/4개)를 통해 IT를 전략·전술·운영 3계층으로 정렬(Strategy Alignment)하고, RACI 매트릭스와 Design Factor 11개(기업전략, 거버넌스 시스템, 위험, 관련이슈 등)로 조직별 맞춤 거버넌스 체계를 수립하는 통합 프레임워크임.
> 2. **가치**: Well-governed IT는 기업 평균 대비 운영비용 23% 절감, 프로젝트 실패율 50%↓, ROI 35%↑ 효과를 보이며(ISACA 2022), 거버넌스 성숙도 Level 3→5 도달 시 의사결정 속도 4.2배 향상, 규정 준수 비용 60% 절감 효과가 검증됨.
> 3. **판단 포인트**: 중앙집중형(Federal) vs 분산형(Federated) 거버넌스 모델 선택, BSC 4관점(재무/고객/내부/학습성장) 간 인과관계 맵 작성 시 인과 지연(Lag Indicator) vs 선행 지표(Lead Indicator) 혼재 위험, 그리고 아키텍처의 SOA vs 마이크로서비스 단계에서의 EA-거버넌스-PMO 간 충돌 조정.

---

## Ⅰ. 개요 및 필요성

**배경**: 디지털 전환(DX) 시대에 기업 IT는 단순 비용센터(Cost Center)에서 사업가치 창출의 전략적 자산(Strategic Asset)으로 변화함. 그러나 2023년 McKinsey 조사에 따르면 글로벌 기업의 65%가 DX 실패의 주원인으로 "IT-사업 정렬 부재"를 꼽았으며, 이로 인해 연간 평균 2.3억 달러의 자원이 낭비됨.

**핵심 과제**:
- IT 투자 대비 비즈니스 가치 측정의 어려움(43% 기업이 ROI 산정 불가)
- Shadow IT 확장으로 인한 보안·컴플라이언스 리스크(평균 35%의 IT 지출이 사각지대)
- 레거시 시스템(COBOL, mainframe) 유지보수 비용이 전체 IT 예산의 60% 차지
- 클라우드/AI/IoT 등 신기술 도입에 따른 아키텍처 복잡도 폭증

```text
┌─────────────────────────────────────────────────────────────────┐
│              정보화 전략계획(ISP) - 거버넌스 통합 프레임워크       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [1단계 환경분석]      [2단계 전략수립]      [3단계 실행계획]    │
│  ┌──────────┐         ┌──────────┐         ┌──────────┐        │
│  │ SWOT/CFV │────────▶│  비전·   │────────▶│  EA 4.0  │        │
│  │ 5-Forces │         │  미션·   │         │  (S/A/T/  │        │
│  │ ValueChain│        │ 전략맵   │         │   D-A)   │        │
│  └────┬─────┘         └────┬─────┘         └────┬─────┘        │
│       │                    │                    │               │
│       ▼                    ▼                    ▼               │
│  ┌──────────────────────────────────────────────────────┐       │
│  │         거버넌스 체계 (COBIT 2019 + ITIL 4)          │       │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐      │       │
│  │  │ COBIT  │  │  ITIL  │  │  BSC   │  │  PMO   │      │       │
│  │  │  EDM  │◀─┤ Service│  │   4P   │  │ Center │      │       │
│  │  │ Process│  │ Value  │  │        │  │   of   │      │       │
│  │  │  Model │  │ System │  │        │  │Excell. │      │       │
│  │  └────────┘  └────────┘  └────────┘  └────────┘      │       │
│  └──────────────────────────────────────────────────────┘       │
│                          │                                      │
│                          ▼                                      │
│            [4단계 성과측정/환류 - PDCA Cycle]                    │
│         KPI Dashboard → Gap Analysis → 차기 계획 반영          │
└─────────────────────────────────────────────────────────────────┘
```

**구 vs 신 패러다임 비교**:
- **기존(Era 1.0)**: IT는 Business Support → TCO(총소유비용) 최소화, BPR(업무재설계) 중심
- **신규(Era 4.0)**: IT는 Business Partner → BVM(Business Value Management), 디지털 비즈니스 모델 혁신, 플랫폼 기반 생태계 구축

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **오케스트라의 지휘자**와 같습니다. 바이올린(현업), 드럼(IT), 트럼펫(경영진) 등 각기 다른 악기를 하나의 협주곡(사업 목표)으로 조화롭게 연주시키는 것이 거버넌스의 본질입니다. 지휘봉(거버넌스 체계)이 없으면 각 악기만 자기 연주에 빠지고, 결국 의미 없는 소음(Shadow IT)만 남게 됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**COBIT 2019 Governance System Architecture**:

```text
┌─────────────────────────────────────────────────────────────────┐
│                    COBIT 2019 거버넌스 시스템 구조               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─── 5개 거버넌스 영역 (Domains) ─────────────────────┐       │
│  │                                                      │       │
│  │  EDM(05)    │ EDM01 전략수립, EDM02 혜택공유,        │       │
│  │  Evaluate,  │ EDM03 위험최적화, EDM04 자원관리,       │       │
│  │  Direct,    │ EDM05 투명성확보                       │       │
│  │  Monitor    │                                         │       │
│  ├─────────────┼─────────────────────────────────────────┤       │
│  │  APO(14)    │ BAI01~11(11개) - Build/Acquire/Implement│      │
│  │  Align,     │  ├ 프로젝트/프로그램/투자관리           │       │
│  │  Plan,      │  ├ 솔루션 설계/구축, 변화관리           │       │
│  │  Organize   │  └ 지식관리, 자산관리                   │       │
│  ├─────────────┼─────────────────────────────────────────┤       │
│  │  DSS(06)    │ DSS01~06 - Deliver/Service/Support     │       │
│  │  Deliver,   │  ├ 운영관리, 서비스요청/사고/문제      │       │
│  │  Service,   │  ├ 비즈니스연속성, 보안, 컴플라이언스    │       │
│  │  Support    │  └ 변경/릴리즈 관리                     │       │
│  ├─────────────┼─────────────────────────────────────────┤       │
│  │  MEA(04)    │ MEA01~04 - Monitor/Evaluate/Assess     │       │
│  │  Monitor,   │  ├ 성과/내부통제/컴플라이언스/우려사항   │       │
│  │  Evaluate,  │  └ 관리체계 모니터링                    │       │
│  │  Assess     │                                         │       │
│  └─────────────┴─────────────────────────────────────────┘       │
│                                                                 │
│  ┌─── 7개 거버넌스 컴포넌트 ───────────────────────────┐        │
│  │ ① 프로세스 ② 조직구조 ③ 정보흐름 ④ 인력/역량     │        │
│  │ ⑤ 정책/절차 ⑥ 서비스/인프라/앱 ⑦ 문화/윤리/행동   │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌─── 11개 Design Factor (맞춤형 설계) ───────────────┐        │
│  │ DF1: 기업전략  DF2: 거버넌스시스템목표              │        │
│  │ DF3: 위험 profile  DF4: 관련이슈                    │        │
│  │ DF5: 위협landscape  DF6: 컴플라이언스 요구          │        │
│  │ DF7: IT 역할  DF8: IT 구현방법론                    │        │
│  │ DF9: 기술채택전략  DF10: 조직규모  DF11: 방법론    │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌─── 집중화/연계 모드 결정 ───────────────────────────┐        │
│  │ Federal(중앙) | Federated(혼합) | Decentralized(분산)│        │
│  └────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(5개 프로세스)** | 거버넌스의 지휘탑, 의사결정 권한 | - EDM01: 기업목표-IT전략 정렬도 평가 (Alignment Score)<br>- EDM02: 수익성-위험 균형, Benefit Realization<br>- EDM03: 위험 식별(Risk Register), 5x5 매트릭스<br>- EDM04: IT 자원 포트폴리오 최적화 (ROR)<br>- EDM05: 스테이크홀더 리포팅, 투명성 |
| **APO(14개 프로세스)** | 전략-전술 연결, IT 계획·조직화 | - APO01(IMA): IT 관리체계 정의, GRC 통합<br>- APO04(Innov): 디지털혁신, 신기술 평가 (TRL 6+ 이상)<br>- APO05(Port): IT 투자 포트폴리오, NPV/IRR/Payback 분석<br>- APO12(Risk): 위험관리 Framework, COSO-ERM 연계<br>- APO13(Sec): 정보보안관리체계(ISMS-P) 연계 |
| **BAI(11개 프로세스)** | 솔루션 구축·구현·변화 | - BAI01(Programs): 프로그램/프로젝트 관리, P3O<br>- BAI02(Requir): 요구사항 관리, BABOK v3 연계<br>- BAI03(Sol.Arch): 솔루션 아키텍처 (TOGAF ADM)<br>- BAI05(Change): 변경관리, ADKAR 모델<br>- BAI08(Knowledge): 지식관리, KMS, Lessons Learned |
| **DSS(6개 프로세스)** | IT 서비스 운영·지원 | - DSS01(Ops): 일일운영, SLA 99.9% 이상<br>- DSS02(Incident): MTTR(mean time to repair) ≤ 4h<br>- DSS03(Problem): 근본원인분석(RCA), 5-Why<br>- DSS04(Continuity): BCP/DR, RTO/RPO/MTPD 정의<br>- DSS05(Sec): 정보보안 통제 (ISO 27001/2 114개 통제) |
| **MEA(4개 프로세스)** | 모니터링·평가·환류 | - MEA01(Performance): BSC 4관점 KPI 측정<br>- MEA02(Internal): 내부통제 평가 (SOX 404)<br>- MEA03(Compliance): 컴플라이언스 감사, GDPR/PCI-DSS<br>- MEA04(Issues): 우려사항 관리, Whistleblowing |

**핵심 알고리즘/공식**:
- **IT 정렬도 측정**: SAM(Strategic Alignment Maturity) 모델 - 4단계 × 4영렬 = 16개 셀 평가
- **TCO 계산**: TCO = 직접비용(HW+SW) + 간접비용(교육+다운로스) + 운영비용(전력+인건비) × 할인율
- **TBM(Technology Business Management)**: IT 비용 100% 가시화, $ / IT 서비스 단가 = TCO / 단위
- **BSC 인과관계**: 학습성장 → 내부프로세스 → 고객 → 재무 (시간지연 3-24개월)

- **📢 섹션 요약 비유**: COBIT 2019는 마치 **'기업의 IT 항법 시스템(GPS)'**과 같습니다. EDM이 위성으로부터의 신호(전략방향)를 받고, APO가 경로계획(전술), BAI가 도로 건설(구축), DSS가 운전(운영), MEA가 블랙박스(모니터링) 역할을 합니다. 목적지(사업목표)를 향해 가는 동안의 모든 결정과 동작을 5단계로 끊임없이 검증하는 것이죠.

---

## Ⅲ. 비교 및 연결

**IT 거버넌스/관리 프레임워크 비교**:

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO 38500** | **CMMI** | **TOGAF ADM** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스/관리 통합 | IT 서비스 관리 | IT 거버넌스 국제표준 | 프로세스 성숙도 모델 | EA 개발 방법론 |
| **범위** | End-to-End IT 거버넌스 | 서비스 라이프사이클 | 6개 원칙 기반 거버넌스 | 5단계 성숙도(L1-5) | 아키텍처 4 영역(S/A/T/D) |
| **구조** | 40 프로세스 + 7 컴포넌트 | 34 Practices, 4D 모델 | Principle(6) + Model(6) | 22 PA (Process Area) | ADM 8단계(Phase A-H) |
| **적용대상** | CIO, 이사회, IT 감사팀 | 서비스데스크, IT 운영 | 임원진, 이사 | 프로세스 개선팀 | 아키텍트, BA |
| **성숙도 모델** | CMMI 0-5 (6단계) | Maturity Model 0-5 | 평가 기반 | L1-5 (5단계) | - |
| **연계 도구** | GRC Tool, OpenPages | ServiceNow, Jira SM | Balanced Scorecard | SCAMPI 평가 | 아키텍처 저장소, Avolution |

**핵심 연계 관계**:
- **COBIT × ITIL**: COBIT의 APO 프로세스(서비스 전략) ↔ ITIL의 Strategy Management, DSS 프로세스 ↔ ITIL의 34 Practices 매핑 가능
- **COBIT × ISO 38500**: COBIT 2019가 ISO 38500의 6원칙(책임, 전략, 획득, 성과, 적합, 인적요소)을 100% 커버
- **COBIT × SOX**: MEA02 프로세스가 SOX 404 ITGC(IT General Control) 통제 항목과 직접 매핑
- **BSC × COBIT**: MEA01의 KPI가 BSC 4관점(재무/고객/내부/학습성장)으로 분류되어 측정
- **TOGAF × COBIT**: BAI03(Solution Architecture)가 TOGAF Phase A-H와 1:1 매핑 가능

```text
┌─────────────────────────────────────────────────────────────────┐
│        프레임워크 통합 매핑 (Integrated Framework Map)          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [이사회/경영진]  ──▶ ISO 38500 (6원칙) ──┐                    │
│         │                                  │                    │
│         ▼                                  ▼                    │
│  [전략수립] ──▶ COBIT EDM ──────────▶ COBIT APO                │
│  ┌─────────┐         │                  │                       │
│  │ TOGAF   │◀────────┘                  ▼                       │
│  │ ADM     │                       COBIT BAI ──▶ TOGAF          │
│  │ Phase A-H│                              │   Architecture     │
│  └────┬────┘                              ▼                       │
│       │                            COBIT DSS ──▶ ITIL 4          │
│       │                                  │   34 Practices       │
│       ▼                                  ▼                       │
│  [아키텍처] ──▶ EA Repository ──▶ 서비스 카탈로그               │
│                                          │                       │
│                                          ▼                       │
│                                   COBIT MEA ──▶ BSC KPI         │
│                                          │                       │
│                                          ▼                       │
│                                   성과 리포팅 / Audit           │
└─────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: COBIT·ITIL·ISO 38500·TOGAF의 관계는 **'병원 진료 시스템'**과 같습니다. COBIT은 병원 전체의 경영(원장), ITIL은 진료 프로세스(의사/간호사), ISO 38500은 의료
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 470 / 800

← **이전**: [469. IT 경영 관리 핵심 토픽 469번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/469_it_management_core_topic_469_exam_summary/)
**다음**: [471. IT 경영 관리 핵심 토픽 471번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/471_it_management_core_topic_471_exam_summary/) →

---
