+++
title = "691. IT 경영 관리 핵심 토픽 691번 시험 요약 (IT Management Core Topic 691 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(토픽 691)는 COBIT 2019 거버넌스 체계, ISO/IEC 38500 IT 거버넌스 표준, BSC-KPI 기반 성과측정, TCO/ROI 분석, 포터의 가치사슬, 디지털 전환(DX) 로드맵을 통합하여 IT 투자 대비 비즈니스 가치 극대화를 추구하는 경영학-정보기술 융합 프레임워크임.
> 2. **가치**: 잘 설계된 IT 거버넌스 체계 도입 시 IT 투자 수익률(ROIT) 20~35% 개선, 프로젝트 실패율 40%->15% 감소, 의사결정 리드타임 60% 단축, 컴플라이언스 위반 비용 연간 25% 절감, 그리고 EA-TOGAF 도입 시 시스템 중복 제거로 TCO 30% 절감 효과 검증됨(Forrester, McKinsey, Gartner 기준).
> 3. **판단 포인트**: 중앙집중형 vs 분산형 거버넌스 모델 선택 시 조직 규모(매출 1조 기준), 산업 규제 강도(금융/의료), 그리고 디지털 성숙도(초기/확장/혁신 단계) 3축 트레이드오프 분석이 핵심이며, BSC 4관점(재무/고객/내부프로세스/학습성장) KPI 가중치 설정, COBIT 2019 Design Factor 11개 요소 매핑, 그리고 PMO-PMOE 단계별 성숙도 평가가 의사결정 분기점임.

---

## Ⅰ. 개요 및 필요성

21세기 기업 환경에서 IT는 단순 비용 중심의 지원 기능을 넘어 **핵심 비즈니스 가치 창출의 동력**으로 자리매김했습니다. 그러나 한국 기업 통계에 따르면 전체 IT 투자의 약 **30~45%가 비즈니스 가치와 명확히 연결되지 못한 채 낭비**(Gartner, 2023 보고서)되고 있으며, IT 프로젝트의 평균 실패율은 여전히 **30~40%** 수준(Standish Group CHAOS Report 2023)에 머물고 있습니다. 이러한 문제를 해결하기 위해 등장한 것이 **IT 경영 관리(Information Technology Management)**라는 통합 프레임워크로, 691번 토픽은 바로 이 영역의 종합적 이해를 평가합니다.

기존의 "IT는 비용이다(Cost Center)"라는 인식에서 탈피하여, "IT는 비즈니스 가치 창출의 전략적 자산(Value Driver)"으로 전환하기 위한 체계적 접근이 필요합니다. 이를 위해 본 토픽에서는 **①IT 거버넌스 ②IT 전략 및 포트폴리오 관리 ③IT 성과 및 위험 관리 ④디지털 전환 전략** 4대 영역을 다룹니다.

```text
+----------------------------------------------------------------------+
|                  IT 경영 관리 통합 프레임워크 (Topic 691)              |
+----------------------------------------------------------------------+
|                                                                      |
|  +-----------------+    +------------------+    +----------------+  |
|  | ① IT 거버넌스   |---->| ② IT 전략·포트폴리오|---->| ③ IT 성과·위험 |  |
|  |  Governance     |    |   Strategy/PMO    |    |  Performance   |  |
|  |                 |    |                    |    |  /Risk Mgmt   |  |
|  | • COBIT 2019    |    | • TOGAF ADM       |    | • BSC/KPI     |  |
|  | • ISO 38500     |    | • 포트폴리오 최적화|    | • TCO/ROI     |  |
|  | • RACI Matrix   |    | • 우선순위 모델링  |    • • ISO 27005 |  |
|  +--------+--------+    +---------+----------+    +-------+-------+  |
|           |                       |                       |          |
|           +-----------------------+-----------------------+          |
|                                   v                                  |
|              +----------------------------------+                    |
|              |  ④ 디지털 전환 전략 (DX)          |                    |
|              |   • McKinsey 3D 모델             |                    |
|              |   • Westerman 5단계 성숙도        |                    |
|              |   • 플랫폼/데이터/AI 역량         |                    |
|              +----------------------------------+                    |
|                                                                      |
+----------------------------------------------------------------------+
```

기존의 IT 관리는 **기술 중심·프로젝트 단위·사후 통제** 방식이었다면, 현대의 IT 경영 관리는 **가치 중심·포트폴리오 단위·사전-사후 통합 통제** 방식으로 패러다임이 전환되었습니다. 이는 1990년대 후반 CobIT(Control Objectives for Information and related Technologies)의 등장, 2000년대 ITIL v2/v3의 서비스 관리 정립, 2010년대 COBIT 5와 TOGAF 9의 통합, 그리고 2019년 이후 COBIT 2019와 TOGAF 10의 클라우드·AI 시대 대응 진화 과정을 거치며 성숙되었습니다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라의 지휘자**와 같습니다. 바이올린(IT 인프라), 첼로(애플리케이션), 트럼펫(데이터), 팀파니(보안) 등 다양한 악기(시스템)가 각자 멋지게 연주하더라도, 이를 하나의 아름다운 교향곡(비즈니스 가치)으로 만들어내려면 통일된 지휘(거버넌스), 악보(전략), 박자(성과), 그리고 조율(위험 관리)이 필수적입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 국제적으로 통용되는 4대 표준/프레임워크를 **상위 거버넌스 -> 중위 관리 -> 하위 운영** 3계층으로 통합한 것입니다.

```text
+-------------------------------------------------------------------------+
|           1계층: 거버넌스(Governance) - WHAT & WHY                        |
|  +------------------+  +------------------+  +----------------------+  |
|  |  COBIT 2019      |  |  ISO/IEC 38500   |  |  ISO/IEC 27014       |  |
|  |  • 40 Governance  |  |  • 6 Principles   |  |  • Governance         |  |
|  |    & Management   |  |    Responsibility, |  |    concepts           |  |
|  |    Objectives     |  |    Strategy,      |  |  • Risk-based         |  |
|  |  • 5 Domains      |  |    Acquisition,   |  |    approach           |  |
|  |  • Design Factors |  |    Performance,   |  |                       |  |
|  |    (11개)         |  |    Conformance,   |  |                       |  |
|  |                   |  |    Human Behavior |  |                       |  |
|  +------------------+  +------------------+  +----------------------+  |
|                              |                                          |
|                              v                                          |
|           2계층: 관리(Management) - HOW & WHEN                          |
|  +------------------+  +------------------+  +----------------------+  |
|  |  TOGAF 10 (ADM)  |  |  PMBOK 7th        |  |  ITIL 4 (SVS)        |  |
|  |  • Phase A~H     |  |  • 8 Performance   |  |  • 34 Practices       |  |
|  |  • ADM Cycle      |  |    Domains         |  |  • 4 Dimensions       |  |
|  |  • ADM Iteration  |  |  • 12 Principles   |  |  • Value Stream       |  |
|  +------------------+  +------------------+  +----------------------+  |
|                              |                                          |
|                              v                                          |
|           3계층: 운영(Operation) - DO & MEASURE                          |
|  +------------------+  +------------------+  +----------------------+  |
|  |  DevOps/Agile    |  |  ITAM / FinOps   |  |  SIEM / GRC 도구      |  |
|  |  • CI/CD Pipeline|  |  • 클라우드 원가  |  |  • Archer / ServiceNow|  |
|  |  • SRE Practices |  |  • 라이선스 관리  |  |  • SAP GRC / SAP EGRC|  |
|  +------------------+  +------------------+  +----------------------+  |
+-------------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** | IT 거버넌스의 **정합성·목표·측정** 체계 제공 | 5개 도메인(EDM: Evaluate/Direct/Monitor, APO: Align/Plan/Organize, BAI: Build/Acquire/Implement, DSS: Deliver/Service/Support, MEA: Monitor/Evaluate/Assess) × 40개 Governance/Management Objective, 11개 Design Factor 기반 시스템 맞춤화, Cascade Goal로 비즈니스 목표와 1:N 매핑, Capability Level 0~5로 프로세스 성숙도 평가 |
| **ISO/IEC 38500** | 이사회·경영진의 **IT 의사결정 표준** | 6대 원칙(책임Responsibility, 전략Strategy, 획득Acquisition, 성과Performance, 적합성Conformance, 인적행동Human Behavior)의 **EDM 패턴**(Evaluate->Direct->Monitor) 준수 의무화, 이사회 직속 IT 전략위원회 거버넌스 구조 권고, PDCA 기반 연간 거버넌스 리뷰 사이클 |
| **TOGAF 10 ADM** | **엔터프라이즈 아키텍처** 수립 및 통합 | Preliminary Phase + Phase A(Architecture Vision) ~ Phase H(Architecture Change Management)의 8단계 사이클, ADM Iteration Cycle로 비순환·부분 반복 지원, Architecture Repository(통합/전략/세그먼트/참조), TRM(Technical Reference Model), III-RM(통합 정보 인프라 참조 모델) |
| **Balanced Scorecard (BSC)** | IT 성과 **4관점 통합 측정** | 재무(Financial) 관점(예: ROIT, IT 비용/매출 비율 ≤ 3%), 고객(Customer) 관점(예: IT 만족도 ≥ 85 NPS), 내부 프로세스(Internal Process) 관점(예: SLA 99.9%, 인시던트 MTTR ≤ 4시간), 학습·성장(Learning & Growth) 관점(예: 직원 IT 역량 등급 ≥ Lv3). 전략맵(Strategy Map)으로 인과관계 시각화 |
| **TCO/ROI 분석 모델** | IT 투자 **경제성 평가** | TCO = 직접비용(하드웨어, SW, 라이선스, 구축) + 간접비용(훈련, 다운타임, 기회비용, 보안 사고 비용, 종량성 클라우드 비용, 갱신 라이선스). ROI = (총 이익 - 총 비용) / 총 비용 × 100. NPV/IRR 적용 시 할인율 WACC 활용. SaaS 전환 시 3년 TCO 30~40% 절감 가능 (Gartner 2023) |

**핵심 산정 알고리즘과 트레이드오프:**

1. **COBIT 2019 Design Factor 11개**: ①Enterprise Strategy, ②Enterprise Goals(13개), ③Risk Profile, ④I&T-Related Issues, ⑤Threat Landscape, ⑥Compliance Requirements, ⑦Role of IT, ⑧IT Implementation Methods, ⑨Technology Adoption Strategy, ⑩Enterprise Size, ⑪M&A Dependency. 이들의 가중치 조합으로 **가장 중요한 Governance Objective 5개를 도출**합니다.

2. **BSC 전략맵의 인과관계**: 학습성장 -> 내부프로세스 -> 고객 -> 재무의 사다리식 인과 연결. 예: "데이터 분석 역량 강화(학습성장)" -> "신속한 의사결정 프로세스(내부)" -> "고객 응답시간 50% 단축(고객)" -> "매출 15% 증가(재무)".

3. **CAPEX vs OPEX 트레이드오프**: CAPEX(설비투자, 감가상각 5년) 방식은 자산 효율성 80% 수준, OPEX(클라우드 종량제) 방식은 자원 효율성 95% 이상 가능하나, 3년 누적 시 역전 현상 발생. 한국 중견기업의 **Break-Even Point는 약 2.7년**(TCO 시뮬레이션 기준).

4. **PMI/PMBOK 7th의 8개 Performance Domain**: 이해관계자, 팀, 개발접근법/생명주기, 계획, 프로젝트 작업, 전달, 측정, 불확실성. 12가지 Principle of Project Management(예: 끊임없는 가치 창출, 학습과 변화 등).

- **📢 섹션 요약 비유**: COBIT는 회사의 **헌법**, TOGAF는 **설계도**, ITIL은 **운영 매뉴얼**, BSC는 **건강검진 차트**와 같습니다. 건강검진을 통해 어떤 질환(병목)이 있는지 파악하고, 헌법에 따라 어떤 가치를 지킬지 정하고, 설계도로 어디를 어떻게 고칠지 계획하고, 매뉴얼로 실제 진료(운영)를 진행하는 것이죠.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 영역에서 자주 혼동되는 유사/대안 프레임워크들의 비교입니다.

| 구분 | COBIT 2019 | ITIL 4 | PMBOK 7th | CMMI v2.0 |
| :--- | :--- | :--- | :--- | :--- |
| **핵심 목적** | IT 거버넌스·관리 목표 달성 | IT 서비스 관리·운영 | 프로젝트 관리 방법론 | 조직/프로세스 성숙도 모델 |
| **개발 주체** | ISACA (1996, 2019 최신) | AXELOS (2019, 2024 업데이트) | PMI (1969, 2021 7th) | ISACA/CMMI Institute (2018) |
| **적용 범위** | 이사회~전사 거버넌스 | 서비스 운영·지원 데스크 | 단일 프로젝트/프로그램 | 프로세스·조직 전반 |
| **구조** | 40 Governance/Management Objective, 5 Domain | 34 Practice, 4 Dimension, Service Value System | 8 Performance Domain, 12 Principle | 5 Maturity Level(Initial->Optimizing) |
| **측정 방식** | Capability Level 0~5, Process Activity Rating | KPI(CSI: Continual Service Improvement) | KPI + Earned Value Management(EVM) | Appraisal(SCAMPI) -> Maturity Level |
| **연계** | 상위 거버넌스, EA, Risk와 직접 연결 | 서비스 데스크, IT 운영, ITSM 도구 | 프로젝트 관리, PMO | 품질 관리, BPM, EA와 연계 |
| **장점** | 비즈니스-IT 정렬, 컴플라이언스 강조 | 서비스 가치·경험 중심 | 프로젝트 정량적 관리 | 점진적 성숙도 향상 |
| **단점** | 구현 복잡도 높음, 학습곡선 큼 | 운영 편향, 거버넌스 연계 약함 | 프로젝트 종료 후 사후관리 한계 | 조직 전체 도입 시 장기 소요 |
| **도입 비용(중견기업)** | 1.5~3억 원, 6~12개월 | 0.8~2억 원, 3~6개월 | 0.5~1.5억 원, 3개월 | 2~5억 원, 12~24개월 |
| **한국 정부 권고** | 행정안전부, 과기정통부 권
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 691 / 800

<- **이전**: [690. IT 경영 관리 핵심 토픽 690번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/690_it_management_core_topic_690_exam_summary/)
**다음**: [692. IT 경영 관리 핵심 토픽 692번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/692_it_management_core_topic_692_exam_summary/) ->

---
