---
title: "754. IT 경영 관리 핵심 토픽 754번 시험 요약 (IT Management Core Topic 754 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


# 📘 정보관리기술사 핵심 토픽 754번: IT 거버넌스 기반 통합 IT 경영관리 프레임워크

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019/ISO 38500 기반 **IT 거버넌스-전략-아키텍처-운영-성과** 5계층 정렬(Alignment) 모델로, ISP(정보전략계획)·EA·BSC·ITIL·ISO 27001을 하나의 가치사슬(Value Chain)로 통합한 경영관리 체계.
> 2. **가치**: McKinsey(2023) 보고 기준 체계적 IT 거버넌스 도입 기업은 **DX 성공률 2.6배**, IT 예산 대비 비즈니스 성과 ROI 평균 **34% 향상**, 그리고 감사 지적사항 **52% 감소** 효과를 달성.
> 3. **판단 포인트**: **집중식(Centralized) vs 분산식(Federated) 거버넌스**, **Top-down ISP vs Middle-out EA**, **BSC 4관점 균형 vs 6-Tier 디지털 성과지표**, 그리고 **규제 준수(Compliance) vs 혁신 속도(Agility)** 사이의 트레이드오프를 조직 성숙도와 산업 규제 강도에 따라 결정.

---

## Ⅰ. 개요 및 필요성

디지털 전환(DX)·AI·클라우드·제로트러스트 환경에서 IT는 더 이상 "비용 센터(Cost Center)"가 아닌 **"전략적 비즈니스 인에이블러(Strategic Business Enabler)"**로 재정의되었다. 그러나 한국 정보시스템감리원의 2023년 통계에 따르면 국내 500대 기업의 **62%가 IT-Biz 정렬(Alignment)에 실패**, 정보화 사업의 **41.7%가 ROI 미달**, 그리고 CIO 리포트에 따르면 **73%의 IT 투자 의사결정이 비즈니스 전략과 단절된 채** 진행된다.

이러한 문제를 해결하기 위해 본 토픽은 **"IT 거버넌스 -> ISP -> EA -> IT 운영/서비스 -> 성과측정 -> 개선"**으로 이어지는 **폐루프(Closed-loop) IT 경영관리 프레임워크**를 다룬다. 이는 단순히 개별 방법론(COBIT, ITIL, BABOK, TOGAF, BSC, ISO 27001, ISO 22301)을 따로 적용하는 것이 아니라, **5단계 가치사슬 위에서 통합 정렬(Integrated Alignment)**시키는 데 핵심이 있다.

```text
+----------------------------------------------------------------------+
|           IT 경영관리 통합 프레임워크 (5-Layer Value Chain)           |
+----------------------------------------------------------------------+
|                                                                      |
|  +-------------------------------------------------------------+     |
|  | Layer 1: IT 거버넌스 (Governance)                            |     |
|  |  - 이사회/CIO 의사결정구조, 정책·표준, 위험·컴플라이언스      |     |
|  |  - 프레임워크: COBIT 2019, ISO 38500, COSO ERM, ISO 37000    |     |
|  +-------------------------------------------------------------+     |
|                              |                                       |
|                              v (전략 연계)                            |
|  +-------------------------------------------------------------+     |
|  | Layer 2: 정보전략계획 (ISP - Information Strategy Planning)  |     |
|  |  - 비전/미션 -> SWOT/TOWS -> CSF/KPI -> 정보화 투자 포트폴리오   |     |
|  |  - 방법론: PEST, Five Forces, Value Chain, McFarlan 전략그리드|     |
|  +-------------------------------------------------------------+     |
|                              |                                       |
|                              v (아키텍처 구현)                        |
|  +-------------------------------------------------------------+     |
|  | Layer 3: EA (Enterprise Architecture)                        |     |
|  |  - BA/DA/AA/TA/SA 5개 영역, TOGAF ADM, FEAF, DoDAF, ARCON    |     |
|  |  - 현행(As-Is) -> 목표(To-Be) -> 전환 로드맵(Gap Analysis)      |     |
|  +-------------------------------------------------------------+     |
|                              |                                       |
|                              v (서비스 전달)                          |
|  +-------------------------------------------------------------+     |
|  | Layer 4: IT 운영·서비스 (IT Service & Operations)            |     |
|  |  - ITIL 4 Service Value System, DevOps, SRE, FinOps          |     |
|  |  - SLA/OLA/UC, ITSM, 변경·사고·문제·요청 관리                |     |
|  +-------------------------------------------------------------+     |
|                              |                                       |
|                              v (성과 측정)                            |
|  +-------------------------------------------------------------+     |
|  | Layer 5: 성과측정·개선 (Performance & Continuous Improvement) |     |
|  |  - BSC 4관점(재무/고객/내부/학습성장), KPI/KRI, OKR           |     |
|  |  - ISO 33000(CMMI), TQM, Six Sigma, BPI, BPM                |     |
|  +-------------------------------------------------------------+     |
|                              |                                       |
|                              +--> (Feedback Loop to Layer 1)         |
+----------------------------------------------------------------------+
```

기존의 **"프로젝트 단위(Siloed) IT 관리"**는 부서별 이기주의, 중복 투자(평균 23%), 그리고 사후 평가 부재로 인해 **TCO(Total Cost of Ownership)** 폭증을 야기했다. 반면 **"포트폴리오 기반 통합 IT 경영관리"**는 거버넌스 -> 전략 -> 아키텍처 -> 운영 -> 성과의 **5단계 폐루프**를 통해 **투자 효율성(Return on IT Investment, ROII)**을 극대화한다.

- **📢 섹션 요약 비유**: IT 경영관리는 **"건물의 구조·전기·배관·환기·에너지관리 시스템"**을 하나의 BIM(Building Information Modeling)으로 통합 설계하는 것과 같다. 도면(EA) 없이 현장에서 배관만 고치면 다른 공사가 무너진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 5계층 통합 모델의 데이터·의사결정 흐름

```text
                    [이사회 / 전략위원회]
                              |
                  +-----------+-----------+
                  |  Layer 1: IT 거버넌스  |
                  |  ------------------- |
                  | • 정책·표준·가이드라인 |
                  | • RACI 매트릭스        |
                  | • 위험 appetite 설정   |
                  +-----------+-----------+
                              | (전략적 의사결정)
                              v
                  +-----------------------+
                  |  Layer 2: ISP         |
                  |  ------------------- |
                  | • 환경분석(PEST/5F)   |
                  | • SWOT/TOWS           |
                  | • CSF/KPI 도출        |
                  | • 정보화 사업 포트폴리오|
                  +-----------+-----------+
                              | (우선순위, To-Be 청사진)
                              v
                  +-----------------------+
                  |  Layer 3: EA          |
                  |  ------------------- |
                  | • BA: 업무/프로세스    |
                  | • DA: 데이터/정보모델  |
                  | • AA: 응용/서비스      |
                  | • TA: 기술/플랫폼      |
                  | • SA: 보안/거버넌스    |
                  +-----------+-----------+
                              | (구현/전환 로드맵)
                              v
                  +-----------------------+
                  |  Layer 4: IT 운영     |
                  |  ------------------- |
                  | • ITIL 4 SVS          |
                  | • DevOps/SRE/FinOps   |
                  | • ITSM(인시던트/변경)  |
                  +-----------+-----------+
                              | (운영 데이터/메트릭)
                              v
                  +-----------------------+
                  |  Layer 5: 성과측정    |
                  |  ------------------- |
                  | • BSC 4관점 KPI       |
                  | • OKR 정렬도          |
                  | • PDCA/CMMI 평가      |
                  +-----------+-----------+
                              |
                              +--> [Layer 1로 피드백]
```

### 2. 핵심 구성 요소별 기술·원리

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **L1. IT 거버넌스 (Governance)** | IT 의사결정의 권한·책무·통제 체계 확립, 이사회-경영진-IT간 정렬 | **COBIT 2019**의 40개 거버넌스/관리 목표(Objective) + **ISO/IEC 38500** 6원칙(책임·전략·취득·성과·규칙·인간행태) + **3단계 체계**(Direction->Oversight->Evaluation). RACI 매트릭스로 의사결정 권한 분배, Risk Appetite Statement로 위험 허용도 정량화. |
| **L2. 정보전략계획 (ISP)** | 비즈니스 전략 ↔ IT 전략 정렬, 투자 우선순위 결정 | **McFarlan 전략 그리드**(Strategic/High Potential/Factory/Support) 적용, **CSF-Model**(Rockart 1979)로 Critical Success Factor 도출, **CSF -> KPI -> SLA -> OLA** 4단계 캐스케이딩. ISP 5단계(현황분석->목표설정->전략수립->사업계획->이행관리). |
| **L3. EA (Enterprise Architecture)** | 현업·데이터·응용·기술·보안의 5관점 청사진, To-Be vs As-Is Gap 분석 | **TOGAF ADM**(Architecture Development Method) 8단계(Phase A~H): Preliminary->A(비전)->B(비즈니스)->C(데이터·응용)->D(기술)->E(기회·솔루션)->F(전환계획)->G(거버넌스)->H(변경관리). **Zachman Framework** 6×6 매트릭스, **ArchiMate 3.2** 표기법, **ArgoUML/EA Sparx/BiZZdesign** 도구 활용. |
| **L4. IT 운영·서비스 (IT Service & Ops)** | 서비스 설계-전이-운영-개선 가치창출, SLA 기반 서비스 품질 보장 | **ITIL 4 Service Value System(SVS)**: 7가지 guiding principle + Service Value Chain(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve). **DevOps** 파이프라인(CI/CD), **SRE**의 SLO/Error Budget, **FinOps**로 클라우드 비용 최적화, ITSM 도구(ServiceNow, Jira Service Management) 활용. |
| **L5. 성과측정·개선 (Performance Mgmt)** | 정량적 KPI 모니터링, BSC 균형점수표, 지속적 개선 | **BSC(Kaplan·Norton 1992)** 4관점: 재무(ROI, ROA)·고객(NPS, CSAT)·내부프로세스(처리속도, 가용률)·학습성장(역량지수, 직원만족). **OKR**(Objectives & Key Results) 계층 정렬. **CMMI** 5단계(Initial->Managed->Defined->Quantitatively Managed->Optimizing). Six Sigma DMAIC. |

### 3. 핵심 정량 공식 및 알고리즘

**(1) IT 투자 가치 평가 3대 지표**
- **NPV (순현재가치):** `NPV = Σ [CF_t / (1+r)^t] - C₀` (CF: 현금흐름, r: 할인율, t: 기간)
- **IRR (내부수익률):** NPV = 0이 되는 r 값
- **TCO (총소유비용):** `TCO = Acquisition + Operating + Support + End-of-Life`
  - 운영비가 5년간 총 TCO의 약 **60~75%** 차지 (Gartner 2022)
- **ROII (IT 투자 수익률):** `ROII = (IT 투자로 인한 수익 - IT 투자 비용) / IT 투자 비용 × 100`

**(2) BSC 4관점 가중치 산정 (AHP, Analytic Hierarchy Process)**
- AHP 일관성 비율(CR) < 0.1 일 때 유효한 가중치로 인정
- 4관점 표준 가중치 예: 재무 25% + 고객 25% + 내부 30% + 학습성장 20%

**(3) IT 위험 정량화 (FAIR 모델)**
- `위험 = 발생확률(Loss Event Frequency) × 영향도(Loss Magnitude)`
- 연간 손실예상(ALE) = SLE × ARO (단일손실예상 × 연간발생률)

**(4) CMMI 성숙도 5단계**
- Level 1 Initial -> Level 2 Managed(프로젝트 단위) -> Level 3 Defined(조직 표준) -> Level 4 Quantitatively Managed(정량 관리) -> Level 5 Optimizing(지속 최적화)

- **📢 섹션 요약 비유**: 5계층 모델은 **"자동차의 ECU(Electronic Control Unit) 네트워크"**와 같다. 거버넌스(차량 제어 ECU) -> 전략(내비게이션) -> EA(샤시 설계도) -> 운영(엔진/변속기) -> 성과(계기판) — 이 중 하나라도 통신이 끊기면 차량 전체가 정상 작동하지 않는다.

---

## Ⅲ. 비교 및 연결

### 1. 거버넌스 프레임워크 비교

| 구분 | **COBIT 2019** | **ISO/IEC 38500** | **ITIL 4** | **CMMI v2.0** |
| :--- | :--- | :--- | :--- | :--- |
| **주 목적** | IT 거버넌스·관리 목표 체계 | IT 의사결정 6원칙 가이드 | IT 서비스 가치창출 | 프로세스 성숙도 평가 |
| **관리 범위** | 40 Governance/Management Objectives | 이사회·경영진 의사결정 원칙 | 34개 서비스 관행(Practice) | 5성숙도, 20 Practice Area |
| **적용 계층** | Layer 1 (거버넌스) | Layer 1 (거버넌스) | Layer 4 (운영) | Layer 5 (성과) |
| **표준화 기구** | ISACA | ISO/IEC JTC 1/SC 40 | AXELOS(PeopleCert) | ISACA |
| **강점** | 상세 통제 목표·메트릭 | 간결한 6원칙, 글로벌 표준 | 서비스 가치사슬·고객경험 | 정량적 성숙도 측정 |
| **약점** | 학습 곡선 가파름, 운영 디테일 부족 | 추상적, 실행 가이드 부족 | 거버넌스 측면 약함 | 거버넌스-전략 연계 약함 |
| **적합 조직** | 대규모·규제 산업(금융·공공) | 모든 조직 (최상위 정책) | 서비스 중심 조직 | SW 개발·운영 조직 |

### 2. EA 프레임워크 비교

| 구분 | **TOGAF** | **Zachman** | **FEAF** | **DoDAF** |
| :--- | :--- | :--- | :--- | :--- |
| **개발사** | The Open Group | Zachman Intl. | 미국 연방정부
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 754 / 800

<- **이전**: [753. IT 경영 관리 핵심 토픽 753번 시험 요약](/studynote/12_it_management/05_security_compliance/753_it_management_core_topic_753_exam_summary/)
**다음**: [755. IT 경영 관리 핵심 토픽 755번 시험 요약](/studynote/12_it_management/05_security_compliance/755_it_management_core_topic_755_exam_summary/) ->

---
