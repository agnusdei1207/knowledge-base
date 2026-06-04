---
title: "544. IT 경영 관리 핵심 토픽 544번 시험 요약 (IT Management Core Topic 544 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 거버넌스·경영 관리는 **COBIT 2019**(40개 거버넌스/관리 목표), **ITIL 4**(34개 서비스 관리 실무), **ISO/IEC 38500**(6원칙), **CMMI v2.0**(5성숙도 단계)를 통합한 프레임워크 체계로, IT 투자 수익률(ROIT)·TCO·EA 적합도 지표로 의사결정 정당성을 확보하는 경영 시스템입니다.
> 2. **가치**: 정량적 효과로 **IT 비용 15~25% 절감**(Gartner 2023), **인시던트 MTTR 40% 단축**, 프로젝트 성공률 **28%->74% 향상**(PMI 2021 대비), 정성적 효과로 경영진-현업-IT 정렬(Alignment) 달성 및 규제 준수(컴플라이언스) 자동화가 가능합니다.
> 3. **판단 포인트**: 중앙집중형 **CoE(Center of Excellence)** vs 분산형 **Federated 모델**, **Build vs Buy vs Cloud(SaaS)** 의사결정, **Agile vs Waterfall vs Hybrid(SAFe)** 프로세스 선택, 그리고 **Bimodal IT**(Mode 1 안정성 vs Mode 2 민첩성)의 균형점이 핵심 트레이드오프입니다.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX) 가속화로 기업의 IT 예산이 매출 대비 평균 **3.5~7.2%**(업종별 상이, Gartner 2023)까지 확대되었음에도, **"우리는 IT에 충분한 돈을 쓰고 있는가?"**라는 경영진의 의문이 지속되고 있습니다. 이는 **IT Value Gap(IT 가치 격차)**이라 불리며, 한국 정보시스템감사통제협회(ISACA) 및 디지털타임스 조사에서 매년 상위 3대 CEO 관심사로 지목됩니다.

과거(2000년대 이전)에는 IT를 **비용 센터(Cost Center)**로 인식하여 CAPEX 위주의 하드웨어 투자에 집중했으나, 클라우드·AI·데이터 분석이 보편화된 현재에는 IT를 **전략적 자산·价值 동인(Value Driver)**으로 재정의해야 합니다. 이러한 패러다임 전환에 대응하기 위해 **IT 거버넌스(IT Governance)**, **IT 서비스 관리(ITSM)**, **엔터프라이즈 아키텍처(EA)**, **프로젝트 포트폴리오 관리(PPM)** 4대 축을 통합한 **IT 경영 관리 체계**가 요구됩니다.

특히 2024년 기준 **클라우드 비용 폭증(Cloud Cost Sprawl)**, **AI 거버넌스 공백**, **공급망 사이버 리스크(Supply Chain Cyber Risk, 예: SolarWinds·3CX 사건)**가 새로운 화두로 부상하면서, 전통적 IT관리 프레임워크(COBIT·ITIL)에 **AI 거버넌스(ISO/IEC 42001, NIST AI RMF)**와 **제로트러스트(Zero Trust, NIST SP 800-207)** 원칙을 융합한 차세대 거버넌스 모델이 필요합니다.

```text
+---------------------------------------------------------------------+
|         IT 경영 관리 4대 축 통합 프레임워크 (4-Pillar Model)        |
+---------------------------------------------------------------------+
                              |
        +---------------------+---------------------+
        |                     |                     |
   +----v-----+         +-----v-----+        +-----v-----+
   | 거버넌스  |         | 서비스    |        | 아키텍처  |
   |Governance|         | 관리      |        |  (EA)     |
   |          |         | (ITSM)    |        |           |
   |•COBIT'19 |         |•ITIL 4    |        |•TOGAF 10  |
   |•ISO38500 |         |•ISO 20000|        |•Zachman   |
   |•COSO IT  |         |•DevOps   |        |•FEAF/DODAF|
   +----+-----+         +-----+-----+        +-----+-----+
        |                     |                     |
        |       +-------------+------------+        |
        |       |                          |        |
        |  +----v-----+              +----v-----+  |
        |  | 포트폴리오 |              | 리스크·  |  |
        |  |  관리     |              |보안·컴플 |  |
        |  | (PPM)    |              |라이언스  |  |
        |  |          |              |          |  |
        |  |•SAFe     |              |•ISO27001|  |
        |  |•Lean PMO |              |•NIST CSF|  |
        |  |•Stage-Gate|              |•PCI-DSS |  |
        |  +----------+              +----------+  |
        |                                              |
        +----------------------+-----------------------+
                              v
                  +------------------------+
                  |   비즈니스 가치 실현   |
                  |   (Realized Business   |
                  |       Value, RBV)      |
                  +------------------------+
```

**전통적 모델 대비 현대 IT 경영 관리의 차별점**:
- **Before (2000s)**: 비용 절감 중심, 사후 통제(After-the-fact), 부서별 사일로, CAPEX
- **After (2020s~)**: 가치 창출 중심, 사전 예방(Preventive), 엔드투엔드 통합, OPEX/Consumption-based, **AI-Augmented 의사결정**

- **📢 섹션 요약 비유**: IT 경영 관리는 **자동차의 계기판·엔진 제어 모듈(ECU)·내비게이션·보험 시스템**을 한데 통합한 것과 같습니다. 단순히 차를 몰기만 하는 것이 아니라, 주행 데이터를 분석해 가장 효율적인 경로(EA)로 안내하고, 사고 위험(리스크)을 사전에 감지하며, 연비(ROI)를 최적화하도록 돕는 **'지능형 운행 관리 시스템'**입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리 시스템의 핵심은 **PDCA + 가치 흐름(Value Stream)**의 결합입니다. COBIT 2019의 **Governance System(거버넌스 시스템)**는 5개 도메인(EDM: Evaluate-Direct-Monitor + APO/BAI/DSS/MEA) 40개 관리목표로 구성되며, 각 목표는 **Process Capability Indicator(0~5단계)**로 측정됩니다.

### 핵심 작동 메커니즘 (Step-by-Step)

```text
+------------------------------------------------------------------+
|        COBIT 2019 Governance & Management Process Loop          |
+------------------------------------------------------------------+

  [1] 전략 정렬 (Strategy Alignment)
       비즈니스 전략 ↔ IT 전략 양방향 정렬
       +--------------+        +--------------+
       | Business Goal|◄------►|  IT Goal     |
       | (예:매출증대) |        | (예:신속출시)|
       +------+-------+        +------+-------+
              | Goals Cascade (13->13) |
              v                       v
       [2] 평가·지휘 (EDM)
       +-------------------------------------+
       | EDM01: 거버넌스 프레임워크 설정     |
       | EDM02: 가치 전달 보장               |
       | EDM03: 리스크 최적화                |
       | EDM04: 자원 최적화                  |
       | EDM05: 이해관계자 투명성 확보       |
       +--------------+----------------------+
                      v
       [3] 계획·구축·운영·모니터링 (PBRM)
       +-------------------------------------+
       | APO (Align, Plan, Organize)  - 14  |
       | BAI (Build, Acquire, Implement)-11|
       | DSS (Deliver, Service, Support) - 6|
       | MEA (Monitor, Evaluate, Assess) - 4|
       +--------------+----------------------+
                      v
       [4] 측정·개선 (Measure & Improve)
       +-------------------------------------+
       | KPI: TCO, ROIT, MTTR, SLA, CSAT  |
       | Process Cap: ISO 15504 PAM        |
       | Maturity: CMMI v2.0 (1~5)         |
       +-------------------------------------+
                      |
                      +------► [Feedback Loop]
```

### 4대 축별 핵심 구성 요소

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 체계 (COBIT 2019)** | IT 의사결정의 권한·책임·보고 체계 정의 | 5개 도메인(EDM/APO/BAI/DSS/MEA) 40개 목표, **40개 목표 × 5단계 능력**(0~5) = 200개 측정 포인트, **Design Factors 11개**로 조직 맞춤 설계 (예: 전략, 목표, 리스크, 컴플라이언스 이슈 등) |
| **서비스 관리 (ITIL 4)** | IT 서비스의 설계-전환-운영-개선 전주기 관리 | **Service Value System(SVS)**: Opportunity/Demand -> Value -> Guiding Principles(7개) -> Governance -> Practices(34개) -> Continual Improvement, **4D 모델**: Design/Transition/Operation/Improvement |
| **엔터프라이즈 아키텍처 (TOGAF 10)** | 비즈니스·데이터·애플리케이션·기술 4계층 통합 청사진 | **ADM(Architecture Development Method)** 8단계: Preliminary->A->B->C->D->E->F->G->H(요구사항 관리), **ArchiMate 3.2** 표기법으로 전략->전술->운영 3계층 시각화 |
| **포트폴리오 관리 (PPM/SAFe)** | 다수 프로젝트·제품의 투자 우선순위·자원 배분 | **Stage-Gate**(Go/Kill/Hold 결정), **WSJF**(Weighted Shortest Job First = Cost of Delay / Job Duration), **Lean Portfolio Management(LPM)**로 Epic->Feature->Story 계층화 |

### 핵심 측정 지표 및 산식

```text
1) 총소유비용(TCO) 산식:
   TCO = 직접비(하드웨어+S/W+네트워크) + 간접비(인건비+교육+전력+공간)
       + 기회비용(다운타임+보안사고) + 폐기비용(EOL)
   ※ Gartner 2023: 온프레미스 TCO 대비 Public Cloud TCO는 3년 기준 32% 저렴

2) IT투자수익률(ROIT):
   ROIT = (IT 투자로 인한 정량적 가치 - IT 투자비용) / IT 투자비용 × 100
   ※ Value = 비용절감 + 매출증가 + 리스크 회피 + 전략적 옵션 가치

3) MTTR / MTBF (서비스 가용성):
   MTTR = Σ(장애복구시간) / 장애발생횟수
   MTBF = Σ(가동시간) / 장애발생횟수
   가용성(%) = MTBF / (MTBF + MTTR) × 100
   ※ 99.99% (Four-Nine) = 연간 downtime 52.6분

4) NIST CSF TIER (사이버보안 성숙도):
   Tier 1: Partial(부분적) -> Tier 2: Risk-Informed(위험 인지) ->
   Tier 3: Repeatable(반복 가능) -> Tier 4: Adaptive(적응형)
```

- **📢 섹션 요약 비유**: 4대 축은 **병원 운영 시스템**과 같습니다. **COBIT(거버넌스) = 병원 행정·이사회**, **ITIL(서비스관리) = 진료·간호 프로세스**, **TOGAF(아키텍처) = 병원 건물·병동 배치도**, **PPM(포트폴리오) = 진료 과목별 우선순위 배분**. 이 4개가 동시에 돌아가야 환자가 최적의 치료(비즈니스 가치)를 받습니다.

---

## Ⅲ. 비교 및 연결

### 프레임워크 간 비교

| 구분 | **COBIT 2019** | **ITIL 4** | **ISO/IEC 38500** | **CMMI v2.0** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스(의사결정·책임) | IT 서비스 관리 실무 | IT 거버넌스 국제표준 | 프로세스 성숙도 평가 |
| **적용 범위** | 전사 거버넌스 (End-to-End) | 서비스 라이프사이클 | 이사회·경영진 의사결정 | 개발·운영 프로세스 |
| **구성** | 5도메인 40목표 | 34 Practices | 6원칙 (Responsibility 등) | 5성숙도 (Initial->Optimizing) |
| **측정** | Process Capability 0~5 | 4D 모델 + KPI | Maturity Model (보조) | Appraisal(SCAMPI) |
| **강점** | 컴플라이언스·리스크 통합 | 실용적·도구 풍부 | 글로벌 표준 인지도 | 정량적 측정·벤치마킹 |
| **약점** | 구현 복잡도 높음 | 거버넌스 관점 약함 | 추상적·측정 도구 부족 | 비개발 영역 적용 한계 |
| **적합 조직** | 대기업·금융·공공 | 서비스 중심·ISP | 글로벌 다국적기업 | SW 공장·SI·핀테크 |

### 다른 시스템·도구와의 통합

```text
+----------------------------------------------------------+
|        IT 경영 관리 ↔ 실무 도구 통합 스택                 |
+----------------------------------------------------------+

[상위] 거버넌스·전략
   +-- ServiceNow GRC / Archer / SAP GRC
   +-- Planview / Clarity PPM (포트폴리오)
   +-- LeanIX / MEGA HOPEX (EA)
              |
              v
[중위] 서비스·프로세스 관리
   +-- ServiceNow ITSM / Jira Service Mgmt
   +-- BMC Helix / Cherwell
   +-- Freshservice / Ivanti
              |
              v
[하위] 개발·운영 (DevOps/SRE)
   +-- GitLab / GitHub + Jenkins / ArgoCD
   +-- Datadog / New Relic / Dynatrace
   +-- Terraform / Ansible (IaC)
   +-- Prometheus / Grafana / ELK
              |
              v
[기반] 클라우드·플랫폼
   +-- AWS Well-Architected / Azure CAF
   +-- FinOps (Cloudability, Vantage)
   +-- Zero Trust (ZIA/ZPA, Wiz, Snyk)
```

**연계 시 고려사항**:
- **Gartner Magic Quadrant 2024**: ITSM 도구 시장은 ServiceNow 선두, JSM·Ivanti 추격. 한국은 **BMC Helix·이담스(EAMS)·가비아 GI** 등 로컬 솔루션도 강세
- **데이터 통합**: CMDB(Configuration Management DB)를 중심으로 **ITIL 구성 항목(CI)** ↔ **COBIT 평가 단위** ↔ **TOGAF 아티팩트** 간 매핑 필요
- **자동화**: RPA(UiPath, Automation Anywhere) + AI Ops(Datadog AI) + AIOps(Moogsoft) 융합으로 ITSM 티켓 자동 분류·처리(70% 자동화 목표)

- **📢 섹션 요약 비유**: 4개 프레임워크는 **건강검진 항목**과 같습니다. **COBIT**은 종합검진(전신),
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 544 / 800

<- **이전**: [543. IT 경영 관리 핵심 토픽 543번 시험 요약](/studynote/12_it_management/05_security_compliance/543_it_management_core_topic_543_exam_summary/)
**다음**: [545. IT 경영 관리 핵심 토픽 545번 시험 요약](/studynote/12_it_management/05_security_compliance/545_it_management_core_topic_545_exam_summary/) ->

---
