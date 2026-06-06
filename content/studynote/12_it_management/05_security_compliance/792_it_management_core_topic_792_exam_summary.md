---
title: "IT Management Core Topic 792 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019(거버넌스/관리 목표 40개), ITIL 4(SVS 34개 Practice), ISO/IEC 38500(6원칙), ISO 20000(서비스경영시스템) 4대 프레임워크를 통합하여 **전략->전환->운영->수렴** 가치 흐름(Value Chain)으로 IT 자산을 비즈니스 가치로 전환하는 End-to-End 경영 체계이다.
> 2. **가치**: 효과적 IT 거버넌스 적용 시 IT 투자 ROI 20~35% 향상, MTTR 50% 단축, 주요 인시던트 60% 감소, 디지털 전환 프로젝트 성공률 28%->68% 개선(PMI 2023), 컴플라이언스 감사 비용 40% 절감 등 정량적 가치를 창출한다.
> 3. **판단 포인트**: 중앙집중형 거버넌스 vs 페더레이션형, COBIT의 능력수준 0~5(ISO 15504 PAM), ITIL 4의 34개 Practice 우선순위, RACI 매트릭스 설계, Agile/DevOps 문화와 거버넌스 통제의 균형, 그리고 Shadow IT 통제 vs 임직원 혁신 유도 사이의 트레이드오프가 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

현대 기업 환경에서 IT는 단순 비용센터(Cost Center)에서 **전략적 비즈니스 파트너**로 진화했다. McKinsey 2023 보고서에 따르면 Fortune 500 기업의 평균 IT 예산 비중은 매출 대비 8.2%이며, 디지털 강기업(Tech-Savvy)은 12~15%를 투자한다. 그러나 **Standish Group CHAOS Report 2023**은 IT 프로젝트 실패율을 31.7%로 보고하며, 이는 IT 경영 관리 부재가 직접적 원인이다. 또한 **Gartner 2024 CIO Survey**에 따르면 CIO의 78%가 "IT 복잡성 증가"를 최대 과제로 인식하고 있어 체계적 거버넌스 프레임워크 적용이 필수적이다.

특히 **GDPR**(2018), **개인정보보호법**(2023 개정), **ESG 공시 의무화**(2025), **EU AI Act**(2024), **ISMS-P**(2024 인증기준 개편) 등 규제 환경이 급변하면서, IT 투자의 정당성 확보, 리스크 관리, 컴플라이언스, 사이버 회복력(Cyber Resilience)이 경영 핵심 이슈로 부상했다. 기술사 관점에서 IT 경영 관리 토픽은 단순 이론이 아닌 **"어떤 프레임워크를 언제, 어떻게, 어떤 범위로 적용할 것인가"**의 의사결정 능력을 평가한다.

```text
+---------------------------------------------------------------------+
|           IT 경영 관리 4대 프레임워크 통합 참조 모델                  |
|                                                                     |
|  +----------+    +----------+    +----------+    +----------+     |
|  | COBIT    |    | ITIL 4   |    | ISO      |    | ISO/IEC  |     |
|  | 2019     |    | (SVS)    |    | 38500    |    | 20000-1  |     |
|  |          |    |          |    | 2014     |    | 2018     |     |
|  |거버넌스/ |    |서비스    |    |IT거버넌스|    |SMS       |     |
|  |관리목표  |    |가치체계  |    |6원칙     |    |인증체계  |     |
|  |  40EA    |    | 34 Prac. |    |          |    |          |     |
|  +----+-----+    +----+-----+    +----+-----+    +----+-----+     |
|       |               |               |               |            |
|       +---------------+-------+-------+---------------+            |
|                               |                                    |
|                       +-------v--------+                           |
|                       |  통합 거버넌스  |                           |
|                       |   체계 (IGS)   |                           |
|                       +-------+--------+                           |
|                               |                                    |
|            +------------------+------------------+                |
|            |                  |                  |                |
|      +-----v-----+     +-----v-----+     +-----v-----+           |
|      |  Strategy  |     | Portfolio |     |  Risk &   |           |
|      |  & Value   |     |  Mgmt     |     |Compliance |           |
|      +-----------+     +-----------+     +-----------+           |
|                                                                     |
|  Layer:  Governance <----> Management <----> Operations              |
|          (전략/정책)    (전환/실행)      (운영/개선)                |
+---------------------------------------------------------------------+
```

기존 패러다임(Pre-2010)은 **ITIL v3**의 26개 프로세스 + **COBIT 5**의 37개 프로세스를 silo(독립 운영) 방식으로 적용했으나, Agile/DevOps/Cloud Native 환경에서는 변화 속도를 따라가지 못했다. 새로운 패러다임(2020~)은 **ITIL 4의 Service Value Chain(SVC) 6개 활동 + 34개 Practice**를 Agile/DevOps와 통합하고, **COBIT 2019**의 Focus Area(예: DevOps, Cybersecurity, Digital Transformation) 커스터마이징을 통해 유연한 거버넌스를 구현한다. 또한 **TOGAF 10**(2022 개정) + **ArchiMate 3.2**로 EA(Enterprise Architecture)와 거버넌스를 통합 관리하는 것이 트렌드이다.

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **오케스트라 지휘자**와 같다. 바이올린(ITIL: 운영), 첼로(COBIT: 거버넌스), 트럼펫(ISO 20000: 인증), 팀파니(ISO 38500: 원칙)라는 각 악기(프레임워크)가 제때 정확한 음(관리 활동)을 연주해야 하나의 아름다운交響曲(비즈니스 가치)이 완성된다. 지휘봉 없이 연주하면 각 악기는 자기 멋대로 연주하여 불협화음(Shadow IT, 프로젝트 실패, 감사 실패)이 발생한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심 아키텍처는 **상위 거버넌스(Governance) -> 중위 관리(Management) -> 하위 운영(Operations)**의 3계층 구조로, 각 계층은 명확한 RACI(Responsible, Accountable, Consulted, Informed) 매트릭스로 책임을 분담한다. **COBIT 2019**는 이 구조를 40개의 관리목표(Governance & Management Objectives, GMO)로 세분화하며, 각 목표는 **프로세스(Process)** + **구성원/구조(People/Skills) + 정보흐름(Flows) + 서비스/인프라/앱(Application) + 사람/스킬/역량(People/Skills)**의 7가지 구성요소(Components of Governance System)로 정의한다.

**ITIL 4 Service Value System(SVS)**은 ITIL v3의 26개 프로세스를 **34개 Practice**로 재편하고, **Opportunity/Demand -> Value** 흐름을 **Service Value Chain(SVC) 6개 활동**(Plan, Improve, Engage, Design & Transition, Obtain/Build, Deliver & Support)으로 재구성했다. 핵심 변화는 **"프로세스 중심 -> 가치 중심"**으로, **Service Desk**(이전 Incident/Request Fulfillment 통합), **Incident Management**(P1~P4 우선순위, SLA 기반), **Change Enablement**(CAB -> CAB Lite -> Emergency Change 3-tier), **Problem Management**(RCA, Known Error DB), **Service Level Management**(SLI/SLO/SLA 트리플릿) 등 핵심 Practice가 SVC 흐름에 매핑된다.

**ISO/IEC 38500:2014**는 IT 거버넌스의 6대 원칙(Evaluate, Direct, Monitor)을 제시하며, 이사회(Board) 수준의 의사결정 프레임워크를 제공한다. **ISO/IEC 20000-1:2018**은 서비스경영시스템(SMS) 인증 체계로, 10개 클러스터(서비스 관리 프로세스 그룹)에 걸쳐 PIMS(Process Implementation Maturity) 0~5 등급을 평가한다.

```text
+----------------------------------------------------------------------+
|             IT 경영 관리 3계층 아키텍처 (상세)                        |
|                                                                      |
|  +-------------------------------------------------------------+    |
|  | Tier 1: Governance Layer (이사회 / IT Steering Committee)   |    |
|  |  -- ISO 38500: Evaluate -> Direct -> Monitor                  |    |
|  |  -- COBIT 2019: EDM(5개 목표)                               |    |
|  |     • EDM01: 거버넌스 체계 설정                             |    |
|  |     • EDM02: 혜택 실현 보장                                  |    |
|  |     • EDM03: 리스크 최적화                                   |    |
|  |     • EDM04: 자원 최적화                                     |    |
|  |     • EDM05: 이해관계자 투명성                               |    |
|  |  -- 주기: 분기/반기, KPI: TCO, ROI, NPV, IRR              |    |
|  +---------------------+---------------------------------------+    |
|                        |                                             |
|  +---------------------v---------------------------------------+    |
|  | Tier 2: Management Layer (CIO / IT 관리자)                  |    |
|  |  -- COBIT 2019: Align/Plan/Organize(APO, 14목표)            |    |
|  |  -- ITIL 4 SVC 6개 Activity:                                |    |
|  |     1) Plan         -> 전략/포트폴리오/아키텍처               |    |
|  |     2) Improve      -> CSI(Continual Service Improvement)   |    |
|  |     3) Engage       -> 관계/공급자/계약                      |    |
|  |     4) Design&Trans.-> 서비스 설계/전환/테스트                |    |
|  |     5) Obtain/Build -> 조달/개발                             |    |
|  |     6) Deliver&Sup. -> 운영/지원/인시던트                    |    |
|  |  -- PMBOK 7th: 8개 Performance Domain + 12 Principles      |    |
|  +---------------------+---------------------------------------+    |
|                        |                                             |
|  +---------------------v---------------------------------------+    |
|  | Tier 3: Operations Layer (DevOps / Service Ops / ITOps)    |    |
|  |  -- Build/Run: CI/CD(Jenkins, GitLab, GitHub Actions)       |    |
|  |  -- Run: AIOps, Observability(Prometheus, Grafana, ELK)    |    |
|  |  -- SRE: SLO/Error Budget(Google SRE Book)                  |    |
|  |  -- FinOps: 클라우드 비용 최적화                            |    |
|  |  -- RACI: R(Dev) A(Owner) C(Sec/Ops) I(사용자)             |    |
|  +-------------------------------------------------------------+    |
|                                                                      |
|  ★ 횡단(Cross-cutting) 요소:                                        |
|     [Risk Mgmt] [Security] [Compliance] [EA] [BCM/DR]              |
+----------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT Steering Committee** | Tier 1 의사결정 | 분기별 회의, IT 투자 승인(>임계값), 전략 정렬 평가, **KGI**(예: 매출 5% 디지털 기여도) 정의, **RACI**에서 A(Accountable) |
| **COBIT 2019 Cascade** | 목표-프로세스 계층화 | **Goals Cascade**: Stakeholder Needs->Enterprise Goals(13개)->Alignment Goals(13개)->Governance/Management Objectives(40개)->Components. 예: "고객 만족" Enterprise Goal->AG02(Managed I&T Compliance)->APO04(Managed Innovation) |
| **ITIL 4 SVC** | 가치 창출 흐름 | 6개 Activity를 Guiding Principles(7개: Focus on value, Start where you are, Progress iteratively, etc.)와 **4 dimensions**(Organizations, Information, Value Streams, Partners) 기반으로 운영 |
| **RACI Matrix** | 책임 분배 | 프로젝트/프로세스별 R/A/C/I 지정, 1A-1R 원칙(Accountable 1인, Responsible 복수 가능), C=10% 이내 권장 |
| **CSI Register** | 지속적 개선 | ITIL 7단계 개선 프로세스(1.비전 정의 -> 2.현 상태 -> 3.목표 -> 4.우선순위 -> 5.상세분석 -> 6.실행 -> 7.지표측정), PDCA + DMAIC 융합 |
| **Risk Register** | 리스크 관리 | ISO 31000 기반 **Likelihood × Impact** 매트릭스(5×5), Risk Treatment: 회피/전가/완화/수용, **KRIs**(Key Risk Indicators) 모니터링 |
| **Service Catalog** | 서비스 포트폴리오 | 비즈니스 서비스/기술 서비스/지원 서비스 3계층, Service Pipeline -> Catalog -> Retired 4단계 라이프사이클 |
| **EA Repository** | 아키텍처 자산 | **ArchiMate 3.2** 모델(BMM/AMM/TM), **TOGAF ADM**(Architecture Development Method) Phase A~H, **Ardoq/LeanIX/ABACUS** 도구 활용 |

**핵심 산식 및 알고리즘**:
- **Total Cost of Ownership(TCO)**: TCO = 직접비(하드웨어+SW+인건비) + 간접비(교육+다운타임+관리비) - 잔존가치. 일반적으로 4년 TCO에서 **클라우드(34%v)** vs 온프레미스 비교 시 3년 BP(break-even) 분석 필수.
- **NPV/IRR**: NPV = Σ[CFₜ/(1+r)ᵗ] - 초기투자. **Hurdle Rate**(할인율) 8~12% 일반적. **NPV > 0, IRR > Hurdle Rate** 시 투자 승인.
- **TBM(Technology Business Management)**: IT 비용을 Tower/Cost Pool 단위(예: 서버, 스토리지, 네트워크, 애플리케이션, 지원)로 분류, **IT Spend Benchmark**(매출 대비 IT 지출 비중)와 비교하여 **Run(70%)/Grow(20%)/Transform(10%)** 비율 최적화(Gartner 권장 60/30/10 -> 40/40/20 전환 트렌드).
- **능력수준(Capability Level, ISO 15504 PAM)**: Level 0(Incomplete) -> 1(Performed) -> 2(Managed) -> 3(Established) -> 4(Predictable) -> 5(Optimizing). Level 3 이상을 **체계적 거버넌스**로 간주.

- **📢 섹션 요약 비유**: 3계층 아키텍처는 마치 **빌딩 관리 시스템**과 같다. Tier 1은 빌딩 주인(소유주/이사회)이 결정하는 "임대 정책과 용도 변경", Tier 2는 빌딩 관리소장(CIO)의 "시설 운영 계획", Tier 3는 청소/경비/전기 기술자(DevOps/ITOps)의 "일상 운영"이다. 빌딩 주인(거버넌스)이 전략을 정해야 관리소장(관리)이 계획을 세우고, 기술자(운영)가 실행한다. 이 세 계층의 책임이 뒤섞이면(예: 기술자가 임대를 결정) 빌딩 전체가 무너진다(Shadow IT, 감사 실패).

---

## Ⅲ. 비교 및 연결

IT 경영 관리의 4대 프레임
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 792 / 800

<- **이전**: [791. IT 경영 관리 핵심 토픽 791번 시험 요약](/studynote/12_it_management/05_security_compliance/791_it_management_core_topic_791_exam_summary/)
**다음**: [793. IT 경영 관리 핵심 토픽 793번 시험 요약](/studynote/12_it_management/05_security_compliance/793_it_management_core_topic_793_exam_summary/) ->

---
