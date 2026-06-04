+++
title = "533. IT 경영 관리 핵심 토픽 533번 시험 요약 (IT Management Core Topic 533 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스는 **COBIT 2019의 40개 Governance/Management Objective**를 핵심축으로, **ISO/IEC 38500의 6대 원칙(책임, 전략, 획득, 성과, 적합, 인간행동)**과 **ITIL 4의 34개 Practice**를 계층적으로 통합한 의사결정·책임·통제(DRC) 체계
> 2. **가치**: 정량적으로는 **IT 투자 ROI 평균 25~35% 개선, IT 리스크 발생률 50% 감소, 컴플라이언스 중복 비용 40% 절감**, 정성적으로는 이사회-경영진-IT조직 간 **ESG/디지털 신뢰도(Trust)** 확보
> 3. **판단 포인트**: **①** Federal(미연방 CIO Council) vs **Cooperative**(공공부문-PMoT) vs **Corporate**(민간-CEO 직속) 거버넌스 모델 중 조직 위계와 **매출 1조 원/직원 1,000명** 임계치 기준 선택, **②** COBIT 2019의 11개 Design Factor(조직 전략, 위험 프로파일, 컴플라이언스 요구, IT 역할, 아웃소싱 등)를 통한 거버넌스 시스템 커스터마이징

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX)·클라우드·AI·제로트러스트 환경에서 IT는 **"비용 센터(Cost Center)"에서 "사업 핵심 자산(Business Value Driver)"**으로地位가 격상되었으며, 이에 따라 이사회 차원의 거버넌스 메커니즘이 필수화되었습니다. 전통적 IT 관리(2000년대 ITIL v2/v3)는 **프로세스 중심**이었으나, 2019년 이후 **COBIT 2019, ITIL 4, ISO 38500, CMMI, ISO 27001/27701**이 **통합 거버넌스 체계**로 수렴하면서, 단순 ITIL 프로세스 맵핑만으로는 **감사·내부통제(Internal Control)**와 **규제 준수(Regulatory Compliance)** 요구를 충족할 수 없게 되었습니다.

특히 **전자금융감독규정(금융권), 공공부문 EA(Enterprise Architecture) 표준 v3.1, 개인정보보호법(PIPA)·GDPR, ESG 공시(SASB/ISSB)** 등 다중 규제 환경에서는 **Three Lines Model(3LoM: 1st-사업부, 2nd-리스크/컴플라이언스, 3rd-내부감사)**을 IT 거버넌스에 내재화해야 합니다. 한국정보통신기술협회(TTA)의 **IT 거버넌스 인증제도(KS X ISO/IEC 38500 인증)**가 2021년 도입되어, 공공기관은 **연간 1회 이상 거버넌스 진단** 의무화가 추진되고 있어 실무 적용성이 높아졌습니다.

```text
    ┌──────────────────────────────────────────────────────────────┐
    │         이사회 (Board of Directors) — 최종 책임(E&O)         │
    │                    │                                         │
    │       ┌────────────▼────────────┐                            │
    │       │ IT Steering Committee    │  ← 전략·투자·우선순위 결정 │
    │       │ (CISO, CIO, CDO, CEO)   │                            │
    │       └────────────┬────────────┘                            │
    │                    │                                         │
    │   ┌────────┬───────▼────────┬──────────┐                     │
    │   │ 1st LoM│     2nd LoM     │  3rd LoM │                     │
    │   │ 사업부  │ 리스크/컴플라이언스│ 내부감사  │                  │
    │   │        │  GRC/PMO/EA팀    │  /IA     │                   │
    │   └────┬───┴────────┬────────┴─────┬────┘                    │
    │        │            │              │                         │
    │   ┌────▼────┐  ┌────▼────┐   ┌────▼────┐                     │
    │   │  ITIL 4 │  │ COBIT   │   │ ISO     │                     │
    │   │ 서비스  │  │ 2019    │   │ 38500   │                     │
    │   │ 운영    │  │ 통제/감사│   │ 원칙/거버│                    │
    │   └─────────┘  └─────────┘   └─────────┘                     │
    └──────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **여러 악기가 연주하는 오케스트라의 지휘자**와 같습니다. COBIT은 **악보(설계도)**, ITIL 4는 **악기별 연주법(서비스 운영)**, ISO 38500은 **지휘 원칙**, 3LoM은 **각 악기 섹션의 리더십**에 해당하며, 이사회가 **청중(수익성·규제·신뢰)** 앞에서 조화를 책임지는 구조입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019는 **Governance System**(40개 목표 중 EDM 5개)와 **Management System**(35개 목표)을 **Cascade(연쇄) 메커니즘**으로 연결합니다. **엔터프라이즈 목표 13개 → IT 관련 목표 13개 → 프로세스 목표 → 컴포넌트 목표(실무지표)**로 4단계 분해되며, 각 단계는 **N:M 매트릭스**로 추적 가능합니다. 핵심 원리는 **"Stakeholder Needs → Enterprise Goals → Alignment Goals → Lifecycle"**의 가치 흐름(Value Chain)이며, **6단계 Governance System Workflow(요구사항 분석 → 컴포넌트 선택 → 아키텍처 설계 → 우선순위 결정 → 구현 계획 → 운영 검토)**로 구현됩니다.

```text
   [Stakeholder Needs] ──► (책임·전략·성능·규제·자본·시장)
            │
            ▼
   [Enterprise Goals] ── 13개 (재무 6, 고객 5, 내부 5, 학습 3)
            │  Cascade
            ▼
   [Alignment Goals] ── 13개 (IT전략 4, 가치 4, 리스크 4, 자원 4)
            │  (1:N 매핑)
            ▼
   [Process Goals] ── 40개 (EDM 5 + APO 14 + BAI 11 + DSS 6 + MEA 5)
            │  (1:N)
            ▼
   [Component Level] ── 프로세스/구조/문화/정책/스킬/정보
            │  (Activity, Metric: KGI/KPI)
            ▼
   [Capability Level] ── 0~5 (ISO 15504 PAM 기반, PA 1.1~5.5)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(평가, 지휘, 모니터링)** | 이사회 거버넌스 5개 목표 | EDM01(거버넌스 체계), EDM02(가치 전달), EDM03(리스크 최적화), EDM04(자원 최적화), EDM05(이해관계자 투명성) — **RACI 차트**로 의사결정 권한 명세 |
| **APO(Align, Plan, Organize)** | 전략 정렬·계획·조직화 14개 | APO12(리스크 관리), APO13(보안), APO04(혁신), APO05(포트폴리오), APO06(예산·원가), APO02(아키텍처) — **ISO 31000 Risk Register** 연동 |
| **BAI(Build, Acquire, Implement)** | 구축·획득·도입 11개 | BAI03(솔루션 도입), BAI04(가용성·용량), BAI09(자산), BAI11(프로젝트) — **PMBOK 7th + PRINCE2** 통합 PMO 운영 |
| **DSS(Deliver, Service, Support)** | 서비스 전달·지원 6개 | DSS02(인시던트), DSS03(문제), DSS04(연속성), DSS05(보안 운영) — **ITIL 4 Service Value System(SVS)**과 직접 매핑 |
| **MEA(Monitor, Evaluate, Assess)** | 모니터링·평가 5개 | MEA01(성과), MEA02(내부통제), MEA03(외부준수), MEA04(감사) — **KPI 대시보드 + eGRC 도구** (Archer/ServiceNow GRC/RSA Archer) |
| **Components (7개)** | 거버넌스/관리 시스템 설계 변수 | ① 프로세스 ② 조직구조 ③ 정보 흐름 ④ 인력·역량 ⑤ 정책·원칙 ⑥ 문화·윤리 ⑦ 서비스·인프라·애플리케이션 — **11개 Design Factor**의 조합으로 우선순위 결정 |
| **Focus Area(중점영역)** | 시나리오별 적용 영역 | 2022년 **DevOps, Risk, Information Security, Privacy, Cloud, Sustainability(ESG)** 등 21개 사전정의 + 커스텀 가능 |

**핵심 알고리즘/원리 — Capability Level Assessment (ISO 15504 PAM)**

Process Attribute(PA)는 **0(Incomplete) ~ 5(Optimizing)**의 6단계 척도이며, **PA 1.1(Process Purpose) → PA 2.1~2.2(Performance Mgmt) → PA 3.1~3.2(Work Product Mgmt) → PA 4.1~4.2(Measurement) → PA 5.1~5.2(Innovation)** 순으로 **NPLF(Nine Process Level Framework)** 평가합니다. 예: **APO12(리스크 관리)** 목표 Capability 4 달성을 위해 **AHP(Analytic Hierarchy Process)** 기반 **위험도 = 확률(1~5) × 영향도(1~5) × 통제효율(역수)** 매트릭스를 활용해 연간 200개 이상 리스크를 정량 평가합니다.

**Cascade of Goals 핵심 공식:**
```
Mapping Strength = (Stakeholder Driver Coverage) × (Enterprise Goal Relevance) × (IT Goal Realization)
Primary 관계(●): 1:1 직접 기여
Secondary 관계(○): 1:N 부분 기여
"방
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 533 / 800

← **이전**: [532. IT 경영 관리 핵심 토픽 532번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/532_it_management_core_topic_532_exam_summary/)
**다음**: [534. IT 경영 관리 핵심 토픽 534번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/534_it_management_core_topic_534_exam_summary/) →

---
