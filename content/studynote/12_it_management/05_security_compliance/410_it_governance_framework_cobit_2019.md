+++
title = "410. IT 거버넌스 프레임워크 COBIT 2019 (IT Governance Framework COBIT 2019)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019는 ISACA가 발표한 엔터프라이즈 IT 거버넌스 및 관리 프레임워크로, 6개의 거버넌스 시스템 원칙(Governance System Principles)과 40개의 거버넌스/관리 목적(Governance & Management Objectives)을 통해 **이해관계자 가치 창출(Value Creation)**과 **엔드 투 엔드 거버넌스 시스템**을 구현하는 개방형 아키텍처이다.
> 2. **가치**: 11개의 디자인 팩터(Design Factors) 기반의 맞춤형 거버넌스 시스템 설계를 통해 조직의 전략적 목표(예: 비용 20% 절감, 컴플라이언스 위반 50% 감소, IT 서비스 가용성 99.99% 달성)와 거버넌스 컴포넌트(Process, Organizational Structure, Information Flow, People/Skills/Competencies, Policies/Procedures, Culture/Ethics/Behavior, Services/Infrastructure/Applications)를 정렬(Alignment)하여 ROI와 위험 감소를 동시에 달성한다.
> 3. **판단 포인트**: **디자인 팩터 11개**의 가중치 결정, **거버넌스 범위(Scope)**의 설정(엔터프라이즈/엔티티/특정 영역), **중점 영역(Focus Areas: 사이버보안, DevOps, 디지털 윤리, 위험 등)**의 우선순위화, 그리고 기존 거버넌스 체계(ISO 27001, ITIL v4, NIST CSF, COSO ERM)와의 통합 매핑 전략이 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

엔터프라이즈 IT 환경은 클라우드 컴퓨팅, AI/ML, IoT, DevOps, 규제 강화(GDPR, ESG, DORA, CSAP, AI Basic Act)로 인해 **전통적인 COBIT 5(2012년 발표)의 5개 원칙 기반 모놀리식 거버넌스 모델로는 한계**가 명확해졌다. 특히 COBIT 5는 (1) 디자인 팩터가 없어 모든 조직에 동일한 거버넌스 체계를 강제하는 경향, (2) 최신 기술(블록체인, AI, 클라우드 네이티브)에 대한 중점 영역(Focus Area) 부재, (3) Agile/DevOps 환경과의 정렬 미흡이라는 한계를 노출했다.

COBIT 2019는 2018년 11월 발표되어 **2019년 12월 정식 출간**되었으며, ISACA의 25년 거버넌스 노하우와 100개국 이상 사용자 피드백을 반영한 **"개방형 아키텍처(Open Architecture)"** 패러다임으로 전환되었다. 핵심 변화는 **"One-size-fits-all"에서 "맞춤형 거버넌스 시스템(Customized Governance System)"**으로의 패러다임 전환이다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│              COBIT 2019 도입의 배경 및 필요성 (As-Is → To-Be)              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  AS-IS (COBIT 5 기반 거버넌스)              TO-BE (COBIT 2019)          │
│  ─────────────────────────────              ──────────────────          │
│  ┌─────────────────────┐                    ┌─────────────────────┐    │
│  │ ❌ 5개 고정 원칙     │                    │ ✅ 6개 시스템 원칙    │    │
│  │ ❌ 37개 프로세스     │      ───►         │ ✅ 40개 거버넌스/    │    │
│  │ ❌ 단일 레퍼런스     │     COBIT          │     관리 목적        │    │
│  │    아키텍처          │      2019          │ ✅ 디자인 팩터 11개  │    │
│  │ ❌ 디자인 팩터 부재  │                    │ ✅ 중점 영역 시스템   │    │
│  │ ❌ Agile/DevOps 미흡 │                    │ ✅ 포커스 영역        │    │
│  └─────────────────────┘                    │ ✅ 개방형 표준 매핑   │    │
│             │                              └─────────────────────┘    │
│             ▼                                          │                  │
│  ┌─────────────────────┐                    ┌─────────────────────┐    │
│  │ 문제점:              │                    │ 해결:                │    │
│  │ - 거버넌스 형식화    │                    │ - 맥락 기반 설계     │    │
│  │ - 비즈니스 가치 미실현│                    │ - 비즈니스 목표 연동 │    │
│  │ - 기술 변화 대응실패  │                    │ - 유연한 컴포넌트 조합│    │
│  └─────────────────────┘                    └─────────────────────┘    │
│                                                                          │
│  핵심 변화: "거버넌스 시스템의 설계 → 운영 → 모니터링"의 사이클화         │
└──────────────────────────────────────────────────────────────────────────┘
```

**왜 COBIT 2019가 필요한가?**

| 환경 변화 | COBIT 5의 한계 | COBIT 2019의 해결 |
|:---|:---|:---|
| 디지털 전환(DX) 가속 | 비즈니스 전략-IT 정렬 프레임 부재 | **Goals Cascade**로 13개 Enterprise Goals → 13개 Alignment Goals → 40개 Governance/Management Objectives 정렬 |
| 사이버보안 위협 증가 (랜섬웨어, APT) | 정보 보안 중점 영역 없음 | **Information Security Focus Area** 별도 제공 |
| 클라우드/Agile/DevOps 확산 | 전통적 프로세스 중심 | **DevOps, Cloud, Cybersecurity** 등 중점 영역 추가 |
| 규제 환경 다변화 (GDPR, DORA, CSAP) | 컴플라이언스 매핑 불명확 | NIST CSF, ISO 27001, ITIL v4와의 명확한 매핑 표 제공 |
| 조직별 거버넌스 성숙도 차이 | 일률적 적용 | **11개 디자인 팩터**로 조직별 맞춤형 설계 |

- **📢 섹션 요약 비유**: COBIT 5가 "모든 가게에 같은 사이즈 옷을 파는 옷가게"였다면, COBIT 2019는 "고객의 체형, 직업, 취향을 측정해 맞춤옷을 제작하는 양복점"입니다. 디자인 팩터가 바로 그 "재단사의 자"입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

COBIT 2019는 **6개의 거버넌스 시스템 원칙**, **40개의 거버넌스/관리 목적**, **5개 도메인**, **7개 컴포넌트**, **11개 디자인 팩터**, **40개 중점 영역**으로 구성된 다층 아키텍처이다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                    COBIT 2019 핵심 아키텍처 (6계층 구조)                   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Layer 1: 거버넌 시스템 원칙 (6개 Governance System Principles)         │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ ① Each Enterprise has different needs (맞춤형 설계)                │  │
│  │ ② Enterprise Governance System should cover E2E (엔드투엔드)       │  │
│  │ ③ Apply a Single Integrated Framework (단일 통합 프레임워크)      │  │
│  │ ④ Enabling a Holistic Approach (총체적 접근)                        │  │
│  │ ⑤ Distinguish Governance from Management (거버넌스와 관리 분리)    │  │
│  │ ⑥ Tailoring the System to Enterprise Needs (조직 맞춤 조정)       │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                   │                                      │
│                                   ▼                                      │
│  Layer 2: 디자인 팩터 (11개 Design Factors)                              │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ D1~D11: 전략, 목표, 위험, 문제, 위협, 컴플라이언스, 역할,           │  │
│  │ IT 채택, 기술 채택, 방법론 채택, 규모/역량 → 거버넌스 초기 설계    │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                   │                                      │
│                                   ▼                                      │
│  Layer 3: 5개 도메인 (Domains)                                           │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ EDM(5) │ APO(14) │ BAI(11) │ DSS(6) │ MEA(4) = 총 40개 목적        │  │
│  │ Evaluate│ Align  │ Build   │ Deliver│ Monitor                       │  │
│  │ Direct  │ Plan   │ Acquire │ Service│ (거버넌스 5 + 관리 35)       │  │
│  │ Monitor │ Organ. │ Implem. │ Support│ Assess                        │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                   │                                      │
│                                   ▼                                      │
│  Layer 4: 7개 거버넌스/관리 컴포넌트 (Components)                        │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ ① Process Processes              ⑤ Policies & Procedures           │  │
│  │ ② Organizational Structures       ⑥ Culture, Ethics & Behavior      │  │
│  │ ③ Information Flows               ⑦ Services, Infrastructure & Apps │  │
│  │ ④ People, Skills & Competencies                                    │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                   │                                      │
│                                   ▼                                      │
│  Layer 5: 40개 중점 영역 (Focus Areas: 2019 Update 02 추가)               │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ 사이버보안, DevOps, 클라우드, AI, 디지털 윤리, ESG, 위기관리,       │  │
│  │ 개인정보보호, 사물인터넷, BCM, 중소기업 거버넌스 등                  │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                   │                                      │
│                                   ▼                                      │
│  Layer 6: 목표 캐스케이드 (Goals Cascade)                                 │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ Stakeholder Needs → Enterprise Goals(13) → Alignment Goals(13)    │  │
│  │ → Governance/Management Objectives(40)                              │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  **거버넌스 vs 관리 구분**                                                │
│  ┌──────────────────┐         ┌──────────────────┐                       │
│  │   거버넌스        │         │      관리        │                       │
│  │   (Governance)    │         │  (Management)    │                       │
│  │ ─────────────    │         │ ─────────────    │                       │
│  │ EDM 도메인 5개   │         │ APO, BAI, DSS,   │                       │
│  │ (평가/지시/모니터)│         │ MEA 도메인 35개   │                       │
│  │ 이사회/경영진     │         │ 임원/관리자      │                       │
│  │ "무엇을/언제/     │         │ "어떻게"         │                       │
│  │  누가"            │         │ (계획/실행/제어) │                       │
│  └──────────────────┘         └──────────────────┘                       │
└──────────────────────────────────────────────────────────────────────────┘
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **거버넌스 시스템 원칙 6개** | COBIT 2019의 철학적 기반 | "각 조직은 다른 needs를 가진다"는 것이 제1원칙이며, 이를 통해 디자인 팩터의 정당성을 확보. 6개 원칙 중 **3, 4, 5, 6번은 COBIT 5의 5원칙을 계승**하고 **1, 2번이 신규 추가**됨 |
| **5개 도메인 (EDM/APO/BAI/DSS/MEA)** | 거버넌스/관리 활동의 계층적 분류 | **EDM(Evaluate, Direct, Monitor)**: 거버넌스 5개 목적(EDM01~05). **APO(Align, Plan, Organize)**: 14개. **BAI(Build, Acquire, Implement)**: 11개. **DSS(Deliver, Service, Support)**: 6개. **MEA(Monitor, Evaluate, Assess)**: 4개. **총 40개 목적** 중 EDM 5개를 제외한 35개가 "관리" 영역 |
| **7개 거버넌스 컴포넌트** | 거버넌스 시스템의 구성 단위 | **Process(활동/절차)**, **Organizational Structures(RACI 차트)**, **Information Flows(데이터 흐름)**, **People/Skills/Competencies(역량 모델)**, **Policies/Procedures(정책 체계)**, **Culture/Ethics/Behavior(조직 문화)**, **Services/Infrastructure/Applications(기술 스택)**. 모든 목적(40개)은 7개 컴포넌트 전부와 연결됨 |
| **11개 디자인 팩터 (D1~D11)** | 거버넌스 시스템의 맞춤 설계 변수 | **D1**: Enterprise strategy, **D2**: Enterprise goals, **D3**: Risk profile, **D4**: I&T-related issues, **D5**: Threat landscape, **D6**: Compliance requirements, **D7**: Role of IT, **D8**: IT adoption, **D9**: Technology adoption, **D10**: Methodology adoption, **D11**: Size/structure/capability. 각 팩터는 3~5단계 척도로 평가하여 거버넌스 우선순위 도출 |
| **40개 거버넌스/관리 목적 (Objectives)** | 실질적 거버넌스/관리 활동 단위 | EDM01: 프레임워크 설정/유지, EDM02: 이익배분 보장, EDM03: 위험 최적화, EDM04: 자원 최적화, EDM05: 이해관계자 투명성. APO01: 관리 프레임워크 정의/유지, DSS01: 운영관리, MEA01: 성능/컨폼런스 모니터링 등 |
| **40개 중점 영역 (Focus Areas)** | 특정 주제에 대한 거버넌스 가이드 | **Information Security Focus Area**(사이버보안), **DevOps Focus Area**, **Cloud Governance**, **AI Governance**(최근 추가), **Digital Ethics**, **ESG**, **Privacy**, **BCM(사업연속성)**, **Risk**, **Small/Mid-size Enterprise** 등. 2019 Update 02부터 본격 제공 |
| **목표 캐스케이드 (Goals Cascade)** | 비즈니스-IT 정렬 메커니즘 | **단계 1**: Stakeholder Drivers/Needs → **단계 2**: 13개 Enterprise Goals(EG01~13, 재무/고객/내부/성장 4관점 BSC) → **단계 3**: 13개 Alignment Goals(AG01~13, IT 목표) → **단계 4**: 40개 Governance/Management Objectives. 각 단계 간 **Primary/Secondary 매핑** 관계 존재 |

**핵심 원리 - Goals Cascade 정렬 메커니즘 (예시)**:

```text
Stakeholder Needs: "우리는 경쟁사보다 빨리 신제품을 출시하고 싶다"
        │
        ▼
EG01: 포트폴리오 경쟁 제품/서비스 (Portfolio of competitive products)
        │
        ▼ (Primary)
AG03: 확정된 요구사항 (Confirmed requirements) - 75% 매핑
        │
        ▼ (Primary)
BAI02: 요구사항 관리 (Manage Requirements Definition)
        │
        ▼
컴포넌트 매핑:
  - Process: BAI02 프로세스 (RACI: R=Product Owner, A=PM, C=BA, I=Steering)
  - Org Structure: Architecture Review Board
  - Info Flow: 요구사항 추적 매트릭스(RTM)
  - People: Certified Scrum Product Owner, IIBA CBAP
  - Policy: 요구사항 변경 관리 정책
  - Culture: 애자일 마인드셋
  - Services: Jira, Azure DevOps, Confluence
```

**디자인 팩터 D1(전략) → 거버넌스 시스템 설계 매핑 예시**:

```text
D1. Enterprise Strategy (조직 전략)
  ├─ Growth/Acquisition → 우선순위: APO04(혁신), BAI03(투자관리)
  ├─ Innovation/Disruption → 우선순위: APO12(위험관리), BAI05(변경관리)
  ├─ Cost Leadership      → 우선순위: APO05(원가관리), BAI09(자산관리)
  └─ Client Service/Excellence → 우선순위: DSS01(운영), DSS02(서비스요청/사고)
```

- **📢 섹션 요약 비유**: COBIT 2019는 **"거버넌스 운영체제(G-OS)"**와 같습니다. 6원칙이 **커널(Kernel)**, 5개 도메인이 **시스템 콜**, 40개 목적이 **프로세스**, 7개 컴포넌트가 **하드웨어 드라이버**,
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 410 / 800

← **이전**: [409. 양자 내성 암호 PQC 전환 계획](/knowledge-base/studynote/12_it_management/05_security_compliance/409_post_quantum_cryptography_pqc_transition/)
**다음**: [411. IT 전략 수립 ISP BPR ISP 방법론](/knowledge-base/studynote/12_it_management/05_security_compliance/411_it_strategy_planning_isp_bpr_methodology/) →

---
