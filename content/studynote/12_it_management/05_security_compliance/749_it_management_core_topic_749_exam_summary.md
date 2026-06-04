+++
title = "749. IT 경영 관리 핵심 토픽 749번 시험 요약 (IT Management Core Topic 749 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(749번 토픽)는 COBIT 2019 거버넌스 체계, ITIL 4 서비스 가치 체계(SVS), ISO/IEC 38500 이사회 거버넌스 원칙을 통합하여 **IT 전략-포트폴리오-운영-평가**를 End-to-End로 정렬하는 메타 프레임워크
> 2. **가치**: McKinsey 2023 보고에 따르면 성숙한 IT 거버넌스 도입 시 IT 투자 ROI 평균 23% 향상, 프로젝트 실패율 41% 감소, Time-to-Market 35% 단축, 사이버 사고 대응시간(MTTR) 67% 개선
> 3. **판단 포인트**: 중앙집중형(CoE) vs 분산형(Bimodal IT) 거버넌스, Agile/DevOps의 자율성과 거버넌스 통제 강도 간 균형점, 규제 준수(CSA, GDPR, 개인정보보호법)와 비즈니스 민첩성 간 트레이드오프가 핵심 의사결정 변수

---

## Ⅰ. 개요 및 필요성

정보관리 기술사 시험의 749번 토픽은 단순한 IT 운영 관리가 아닌, **"IT가 비즈니스 가치를 어떻게 창출하고 그 가치를 어떻게 측정·통제·최적화할 것인가"**에 대한 메타-관리(Management of Management) 체계를 다룬다. 이는 2010년대의 데이터센터/시스템 통합 중심 관리에서 2020년대의 클라우드·AI·데이터 경제 시대에 맞춰 재정의된 영역으로, 한국 정보통신산업진흥원(NIPA)의 2023년 ICT 경쟁력 조사에서 한국 대기업의 IT 성숙도(Levels 3-5)가 38%에 불과하다는 점이 본 토픽의 학습 필요성을 직접 시사한다.

핵심 문제는 세 가지다. 첫째, **전략-실행 갭(Strategy-Execution Gap)**: BCG 2022 보고에 따르면 CEO의 72%가 디지털 전환을 최우선 과제로 인식하나 실제 EBITDA 개선 효과는 26%만 달성. 둘째, **투자 대비 가치(Val-IT) 미측정**: IT 부서의 60% 이상이 KPI를 가용성·장애건수 같은 운영 지표에만 의존, 비즈니스 가치 기여도 비가시. 셋째, **규제-민첩성 충돌**: 개인정보보호법, EU AI Act, NIST CSF 2.0 등 규제 요구가 증가하면서 DevOps·Agile의 빠른 배포 사이클과 충돌.

```text
[IT 경영 관리의 5대 도메인 통합 구조]

  ┌─────────────────────────────────────────────────────────────┐
  │              이사회 / 경영진 (Board Oversight)              │
  │         ISO/IEC 38500: 6 Principles (책임, 전략, 인수,    │
  │         성과, 적합, 인적요소) — Evaluate, Direct, Monitor │
  └──────────────────────────┬──────────────────────────────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
  ┌─────────┐          ┌──────────┐          ┌──────────┐
  │  거버   │          │   포트   │          │   서비   │
  │  넌스   │          │  폴리오  │          │   스     │
  │ (Govern)│          │  (Plan)  │          │(Deliver) │
  │         │          │          │          │          │
  │ COBIT   │          │ TOGAF    │          │ ITIL 4   │
  │ 2019    │          │ ADM      │          │ SVS      │
  │ 40 Obj. │          │ Zachman  │          │ 34 Prac. │
  └────┬────┘          └────┬─────┘          └────┬─────┘
       │                    │                     │
       └──────────┬─────────┴──────────┬──────────┘
                  ▼                    ▼
            ┌──────────┐         ┌──────────┐
            │  측정    │         │  위험/   │
            │(Measure) │         │ 컴플라이│
            │          │         │  언스    │
            │ BSC+KPI  │         │          │
            │ Val IT   │         │ ISO 27001│
            │ DMMM     │         │ NIST CSF │
            └──────────┘         └──────────┘
                  │                    │
                  └─────────┬──────────┘
                            ▼
                  [비즈니스 가치 창출 + 리스크 통제]
```

기존 패러다임(2010년대)에서는 ITIL v3의 **서비스 라이프사이클(SS- SD-DR-ST-SO)** 중심의 운영 관리가 주였고, COBIT 5는 거버넌스와 관리의 분리(Governance vs Management) 및 7가지 Enabler(원동력) 개념을 도입했으나 클라우드·DevOps 환경의 분산·자동화 특성을 충분히 반영하지 못했다. 2024년 현재의 패러다임은 **COBIT 2019의 40 Governance & Management Objectives + Focus Areas(DevOps, Cybersecurity, Privacy, AI)**, **ITIL 4의 Service Value Chain(SVC) 6개 활동 + 34개 Practice**, **ISO 38500의 EDM(Evaluate-Direct-Monitor) 3-블록 모델**을 통합해 **양적 측정 가능하고 자동화 가능한 거버vernance 2.0**으로 진화했다.

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차 산업의 **'통합 차량 관리 시스템(Vehicle Dynamics Management)'**과 같다. 엔진 출력(운영 효율), 핸들링(거버넌스), 브레이크(리스크 통제), 내비게이션(전략 정렬) 4가지를 ECU(Electronic Control Unit)로 통합 제어하지 않으면 아무리 좋은 부품(기술)도 사고(실패)로 이어진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 거버넌스 코어 프레임워크 3-레이어

IT 경영 관리의 기술적 핵심은 **"누가(Who), 무엇을(What), 어떻게(How) 결정하고 통제하는가"**를 계층적으로 분리하는 것이다. COBIT 2019의 계층 구조는 다음과 같다.

```text
[3-레이어 거버넌스 아키텍처와 결정 흐름]

 ┌──────────────────────────────────────────────────────────────┐
 │  Layer 1: Governance (전략적 의사결정)                       │
 │  ─────────────────────────────────────────                    │
 │  • 이사회 / IT 전략 위원회 (ITSC)                             │
 │  • 역할: Evaluate(평가) → Direct(지시) → Monitor(모니터)     │
 │  • 주기: 분기 / 반기                                          │
 │  • 산출물: IT 전략 청사진, 거버넌스 시스템 章程(Charter)        │
 │                                                              │
 │   [Decision Rights Matrix: RACI 적용]                         │
 │   ┌────────────┬──────┬──────┬──────┬──────┐                 │
 │   │ 결정 영역  │ 이사 │ CEO  │ CIO  │ 사업 │                 │
 │   ├────────────┼──────┼──────┼──────┼──────┤                 │
 │   │ IT 원칙    │  A   │  C   │  R   │  I   │                 │
 │   │ 포트폴리오 │  I   │  A   │  R   │  C   │                 │
 │   │ 아키텍처   │  I   │  A   │  R   │  C   │                 │
 │   │ 투자 >100억│  A   │  R   │  C   │  I   │                 │
 │   │ 인시큐리티 │  A   │  I   │  R   │  C   │                 │
 │   └────────────┴──────┴──────┴──────┴──────┘                 │
 └──────────────────────────┬───────────────────────────────────┘
                            │  (지시/통제 흐름 ↓)
 ┌──────────────────────────┴───────────────────────────────────┐
 │  Layer 2: Management (전술적 계획·조정)                      │
 │  ─────────────────────────────────────────                    │
 │  • CIO / IT-PMO / EA 팀 / CISO                               │
 │  • 도메인: EDM, APO(Align-Plan-Org), BAI(Build-Acquire-Impl),│
 │           DSS(Deliver-Service-Support), MEA(Monitor-Eval-Ass)│
 │  • 주기: 월간 / 프로젝트 단위                                 │
 │  • 도구: Jira Align, ServiceNow SPM, Apptio, LeanIX         │
 └──────────────────────────┬───────────────────────────────────┘
                            │  (실행 위임 ↓)
 ┌──────────────────────────┴───────────────────────────────────┐
 │  Layer 3: Operations (일상적 실행)                            │
 │  ─────────────────────────────────────────                    │
 │  • 서비스 데스크 / DevOps 팀 / SRE / 데이터 엔지니어          │
 │  • 자동화: Ansible, Terraform, ArgoCD, AIOps 플랫폼          │
 │  • 측정: SLI/SLO/SLA, Four Golden Signals (Latency,         │
 │           Traffic, Errors, Saturation) — Google SRE 모델    │
 │  • 주기: 실시간 / 일간                                       │
 └──────────────────────────────────────────────────────────────┘
```

### 2-2. 구성 요소별 역할 및 핵심 기술

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Governance System (거버넌스 체계)** | IT 의사결정의 권리·책임·절차 정의 | COBIT 2019의 40 Governance/Management Objectives, Design Factors 11종(전략, 목표, 위험, 규모, 컴플라이언스 등), **Capability/Maturity Level(0-5)** 평가 |
| **Strategy & Portfolio** | IT 투자 우선순위화 및 가치 극대화 | TOGAF ADM 8-Phase, **Stage-Gate(G0~G7)** 거버넌스, BCG/Porter 가치사슬 연계, NPV/IRR/Payback 분석 + **Real Options Valuation** |
| **Service Value System** | IT 서비스의 End-to-End 가치 전달 | ITIL 4 SVC의 6개 Activity(Plan→Engage→Design&Transition→Obtain/Build→Deliver&Support→Improve), **34 Practices(General+Service+Management)** |
| **Risk & Security** | 사이버/운영/규제 리스크의 통합 관리 | ISO 27001:2022 93 Annex A 통제항목, **NIST CSF 2.0의 6 Function(GV-ID-PR-DE-RS-RC)**, FAIR 모델(요인분석 리스크 정량화) |
| **Performance & Value** | IT 성과와 비즈니스 가치의 정량 측정 | **IT BSC 4관점(Financial-Customer-Internal Process-Learning)**, Val IT의 5단계(value governance-process), DMM(Data Management Maturity) 6단계 |

### 2-3. 핵심 메커니즘: 거버넌스 시스템의 Design Factor 매핑

COBIT 2019의 핵심 혁신은 **"One-size-fits-all 거버넌스"를 거부**하고, 기업의 11가지 Design Factor(전략, 목표, 위험, 컴플라이언스, IT 역할, 시스템, 기술, 문화, 원칙, 역할, 의사결정)에 따라 거버넌스 시스템의 **Scope, Focus, 목표 우선순위**가 동적으로 결정된다는 점이다.

```text
[Design Factor 기반 거버넌스 시스템 자동 설계 알고리즘 의사코드]

  Input: DF1..DF11 (기업 컨텍스트 변수)

  Step1: 각 DF에 가중치 할당 (예: DF7_기술=0.3, DF4_컴플라이언스=0.25)
  Step2: 40개 Objective별 관련성 점수 계산
          Score(o) = Σ (DF_i × Relevance_i_o)
  Step3: 목표 관리 Target Capability Level 산출
          Target_L(o) = ⌈ Σ (Score × Industry_Benchmark) ⌉  [0..5]
  Step4: Priority-Goal Matrix(P0~P3) 산출
          P0 = Regulatory 필수, P1 = 전략 핵심, P2 = 차별화, P3 = 옵션
  Step5: Resource Allocation: Budget ∝ (Target_L × Object_Width)
  Step6: Continuous Monitoring: Δ(현재 측정값 - Target) → 재조정

  Output: ① 커스터마이즈된 거버넌스 시스템 ② 투자배분 ③ KPI 셋
```

**핵심 측정 공식**:
- **IT ROI** = (IT 기인 수익 − IT 총비용) / IT 총비용 × 100
- **NPV of IT Investment** = Σ [CF_t / (1+r)^t] − Initial Investment (r = WACC + IT risk premium 3~5%)
- **Val IT Business Score**: 5개 차원(전략 정렬, 투자 포트폴리오, 역량, 가치 실현, 위험관리) × 각 5점 척도
- **CISO 효율 지표**: MTTR(평균복구시간) ≤ 4시간, MTTD(평균탐지시간) ≤ 30분, CVE 패치율 ≥ 95% within 30 days

### 2-4. Agile/DevOps 환경에서의 거버넌스 융합 패턴

전통 거버넌스는 **Stage-Gate** 중심이지만, DevOps 환경에서는 **"Governance as Code"**가 등장했다.

- **Policy as Code**: Open Policy Agent(OPA), HashiCorp Sentinel로 배포 시점 통제
- **Continuous Compliance**: SOC 2/ISO 27001 통제를 CI/CD 파이프라인에 자동 검증(예: Terraform의 tfsec, Checkov)
- **Risk-Based Sprint Planning**: User Story별 위험 등급(Low/Med/High) 자동 산정, High 등급은 추가 거버넌스 게이트 적용

- **📢 섹션 요약 비유**: 거버넌스의 3-레이어는 **'항공우주국의 미션 통제(Mission Control)'**와 같다. 발사대(전략)→비행감독관(전술)→우주비행사(운영)로 권한을 위임하되, 텔레메트리(측정)와 Go/No-Go(통제) 신호는 끊임없이 교환된다. DevOps의 자율 로켓(자동화)이 미션의 본질(전략)으로부터 분리되면 임무는 실패한다.

---

## Ⅲ. 비교 및 연결

### 3-1. 주요 거버넌스/관리 프레임워크 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500:2015** | **CMMI 2.0** | **TOGAF 10** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **주 목적** | 거버넌스+관리 통합 프레임워크 | IT 서비스 관리(Service Mgmt) | 이사회 수준 IT 거버넌스 원칙 | 프로세스/조직 성숙도 | EA 개발 방법론 |
| **대
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 749 / 800

← **이전**: [748. IT 경영 관리 핵심 토픽 748번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/748_it_management_core_topic_748_exam_summary/)
**다음**: [750. IT 경영 관리 핵심 토픽 750번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/750_it_management_core_topic_750_exam_summary/) →

---
