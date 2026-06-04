---
title: "739. IT 경영 관리 핵심 토픽 739번 시험 요약 (IT Management Core Topic 739 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리의 핵심은 **COBIT 2019, ITIL 4, ISO 38500** 프레임워크를 기반으로 **거버넌스(Governance) ↔ 관리(Management)**를 분리하고, **Value Creation(가치 창출)**을 위해 **Benefits Realization, Risk Optimization, Resource Optimization**의 3대 균형점(Governance Objective)을 IT 투자·운영·성과 전 영역에 체계적으로 적용하는 것이다.
> 2. **가치**: 성숙도 모델 기반(IT-CMF, CMMI-SVC) 도입 시 **IT 투자 대비 ROI 25~40% 개선**(Gartner 2024 기준), **프로젝트 실패율 30% -> 15% 감소**(PMI 2023), **IT 운영 비용 20~35% 절감**(McKinsey ESM Benchmark) 등의 정량적 효과를 거둘 수 있으며, 이사회-경영진-IT조직 간 **RACI 명확화**를 통한 의사결정 지연 50% 단축이 가능하다.
> 3. **판단 포인트**: **Build vs Buy vs Cloud(SaaS)**, **표준 프레임워크 채택 vs 맞춤형 아키텍처**, **중앙집중 거버넌스 vs 분산형 거버넌스(Federated)** 사이의 트레이드오프, 그리고 **Agile/DevOps**와 **Waterfall/Plan-driven**의 혼용 비율(듀얼 운영 모델), 궁극적으로 **EA(Enterprise Architecture)**와 **PPM(Project Portfolio Management)** 통합 수준이 핵심 설계 결정 변수가 된다.

---

## Ⅰ. 개요 및 필요성

정보관리기술사 시험의 739번 토픽은 **"디지털 전환 시대의 IT 거버넌스 및 전략적 가치 실현"**을 다룬다. 4차 산업혁명, 생성형 AI, 클라우드 네이티브 환경으로 패러다임이 전환되면서, 전통적 IT 관리(코스트 센터 -> 프로핏 센터)는 **"Business Technology (BT)"** 관점으로 재정의되어야 한다. IT 조직은 더 이상 비용 절감만을 목표로 하지 않으며, **GF(Governance Framework)**, **Portfolio Management**, **SLA/SLM**, **BCM(사업연속성관리)**, **IT Compliance & Audit**를 통합적으로 운용하여 **가치지향적 아키텍처(Value-Driven Architecture)**를 구축해야 한다.

```text
+------------------------------------------------------------------+
|        디지털 전환 시대의 IT 경영 관리 3-Layer 거버넌스 모델       |
+------------------------------------------------------------------+
|                                                                  |
|   [Layer 1] 의사결정 거버넌스 (Decision Governance)               |
|   +--------------------------------------------------------+     |
|   |  +----------+  +----------+  +----------+  +--------+  |     |
|   |  |이사회/IT  |->|IT 전략   |->|EA 위원회  |->|감사/   |  |     |
|   |  |전략위    |  |위원회    |  |(아키텍처) |  |컴플라  |  |     |
|   |  +----------+  +----------+  +----------+  +--------+  |     |
|   |       |              |              |           |        |     |
|   |       +--------------+------+-------+-----------+        |     |
|   |                             v                             |     |
|   |              IT 전략 & 로드맵 (SISP/ITSP)                  |     |
|   +--------------------------------------------------------+     |
|                              |                                   |
|   [Layer 2] 운영 거버넌스 (Operational Governance)                |
|   +--------------------------------------------------------+     |
|   |  +---------+  +----------+  +----------+  +----------+ |     |
|   |  |PPM      |->|Agile/    |->|DevOps/   |->|SRE/      | |     |
|   |  |Portfolio|  |SAFe      |  |GitOps    |  |Observab. | |     |
|   |  |Mgmt     |  |Scrum     |  |CI/CD     |  |(AIOps)   | |     |
|   |  +---------+  +----------+  +----------+  +----------+ |     |
|   |       |              |              |           |        |     |
|   |       +--------------+------+-------+-----------+        |     |
|   |                             v                             |     |
|   |              Service Value Chain (ITIL 4 SVC)             |     |
|   +--------------------------------------------------------+     |
|                              |                                   |
|   [Layer 3] 통제 거버넌스 (Control Governance)                    |
|   +--------------------------------------------------------+     |
|   |  +----------+  +----------+  +----------+  +--------+  |     |
|   |  |COBIT 2019|->|ISO 38500 |->|ISMS/     |->|내부/   |  |     |
|   |  |(관리목표) |  |(거버넌스) |  |PIMS/PCI  |  |외부감사|  |     |
|   |  +----------+  +----------+  +----------+  +--------+  |     |
|   |       |              |              |           |        |     |
|   |       +--------------+------+-------+-----------+        |     |
|   |                             v                             |     |
|   |            거버넌스 시스템 (Governance System)             |     |
|   +--------------------------------------------------------+     |
|                                                                  |
+------------------------------------------------------------------+
        |              |              |              |
        v              v              v              v
    +--------+    +---------+    +----------+    +----------+
    |Board/  |    |Executive|    |IT Mgmt   |    |Operation |
    |Steering|    |(CxO)    |    |(CIO/CTO) |    |(팀장/실장)|
    +--------+    +---------+    +----------+    +----------+
        E,D,A,C*        E,A          C,I*          C,O*
   *RACI Matrix 기반 책임 할당
```

**Old Paradigm vs New Paradigm 비교**:
- **Old**: IT는 백오피스 지원 조직, CapEx 중심의 HW 구매, ITIL v3 함수형(process) 관리, 연 1회 예산 사이클, **"Run the Business"** 우선
- **New**: BT(Business Technology)로서 전략적 차별화 요소, OpEx/Subscription 기반 FinOps, **ITIL 4 SVC(Service Value Chain)** 34개 실무 활동, 실시간 가치 측정(Observability + VSM), **"Run + Change + Transform"** 동시 추구, **Product-centric 운영**

- **📢 섹션 요약 비유**: IT 거버넌스는 마치 **"도시의 도시계획 + 건축법 + 소방안전 + 감사"를 한꺼번에 운영하는 시청"**과 같습니다. 건물 하나(시스템)만 잘 지으면 되는 것이 아니라, 도시 전체의 토지이용계획(EA), 소방규정(보안·컴플라이언스), 세수/예산(FinOps), 시민 만족도(SLA)까지 조화롭게 운영해야 지속가능한 '스마트시티'가 됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 핵심은 **5개 도메인의 상호운용성**이다. 이 도메인은 **COBIT 2019의 EDM(평가/지시/모니터링) -> APO(정렬/계획/조직) -> BAI(빌드/획득/구현) -> DSS(전달/지원/운영) -> MEA(모니터링/평가/성과)** 의 5개 도메인과 정확히 매핑된다.

```text
   COBIT 2019 Governance & Management Objectives (40개 목표)
   +--------------------------------------------------------------+
   |                                                              |
   |  +-[EDM]-------------------------------------------------+  |
   |  | EDM01 거버넌스 프레임워크 설정 및 유지                 |  |
   |  | EDM02 가치 전달 보장(Benefits Delivery)               |  |
   |  | EDM03 위험 최적화(Risk Optimization)                   |  |
   |  | EDM04 자원 최적화(Resource Optimization)               |  |
   |  | EDM05 이해관계자 투명성(Stakeholder Transparency)      |  |
   |  +--------------------------------------------------------+  |
   |                          <-> RACI 매핑                         |
   |  +-[APO]--------------+  +-[BAI]--------------+             |
   |  | APO01 관리 프레임웍 |  | BAI01 관리 프로그램 |             |
   |  | APO02 전략 관리     |  | BAI02 요구사항 정의 |             |
   |  | APO03 엔터프라이즈  |  | BAI03 솔루션 식별/  |             |
   |  |       아키텍처(EA)  |  |       빌드         |             |
   |  | APO04 혁신 관리     |  | BAI04 가용성/용량  |             |
   |  | APO05 포트폴리오    |  | BAI05 조직 변화     |             |
   |  | APO06 예산/비용     |  | BAI06 IT 변화       |             |
   |  | APO07 인력 관리     |  | BAI07 변경 수용     |             |
   |  | APO08 관계 관리     |  | BAI08 지식 관리     |             |
   |  | APO09 SLA 관리      |  | BAI09 자산 관리     |             |
   |  | APO10 벤더 관리     |  | BAI10 구성 관리     |             |
   |  | APO11 품질 관리     |  | BAI11 프로젝트 관리 |             |
   |  | APO12 위험 관리     |  |                     |             |
   |  | APO13 보안 관리     |  |                     |             |
   |  +--------------------+  +---------------------+             |
   |                          <->                                   |
   |  +-[DSS]--------------+  +-[MEA]--------------+             |
   |  | DSS01 운영 관리     |  | MEA01 성과/순응     |             |
   |  | DSS02 서비스 요청/  |  |       모니터링      |             |
   |  |       사고 관리     |  | MEA02 내부 통제     |             |
   |  | DSS03 문제 관리     |  | MEA03 외부 컴플     |             |
   |  | DSS04 연속성 관리   |  |       라이언스       |             |
   |  | DSS05 보안 서비스   |  | MEA04 Assurance     |             |
   |  | DSS06 비즈니스 통제 |  +---------------------+             |
   |  +--------------------+                                       |
   +--------------------------------------------------------------+
                  <->                <->               <->
            +---------+      +----------+    +----------+
            |ITIL 4   |      |ISO 38500 |    |ISO 27001|
            |34 SVC   |      |6원칙     |    |Annex A   |
            |Practices|      |(Responsib|    |93 통제  |
            |         |      |ility 등) |    |         |
            +---------+      +----------+    +----------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **전략/거버넌스 위원회** | 의사결정 및 정렬 | **이사회-경영진-IT** 간 RACI 매트릭스 적용, **OKR/KPI** 연계, 분기별 Value Realization Review(VRR), 의사결정 SLA(예: 5영업일 이내 결정) |
| **EA(Enterprise Architecture)** | 기술-비즈니스-정보-응용 4개 영역 통합 | **TOGAF 10 ADM(Architecture Development Method)**: Preliminary->A(비전)->B(비즈니스)->C(데이터/응용)->D(기술)->E(기회/솔루션)->F(마이그레이션)->G(구현거버넌스)->H(변경관리), **ArchiMate 3.2** 모델링 언어, **Zachman Framework 6x6 매트릭스** |
| **PPM(Project Portfolio Mgmt)** | 투자 우선순위화 및 성과 측정 | **NPV(순현재가치), IRR(내부수익률), Payback Period, ROI, B/C Ratio** 5대 재무지표 + **Strategic Fit Score(가중치 30%) + Risk Score(20%) + Resource Availability(20%) + Urgency(15%) + Compliance(15%)** 의 다기준 의사결정(MCDA) |
| **Service Management** | SLA/ITIL 기반 운영 | **ITIL 4 SVC**: Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve 의 6개 활동 체인, **SLA 계층화**: OLAs(내부)->SLAs(고객)->UCs(외부 벤더), **OLA 충족률 ≥ 95%** 목표 |
| **Risk & Compliance** | 거버넌스 통제 | **ISO 27005 Risk = Threat × Vulnerability × Asset Value**, **ISO 31000 Risk Treatment(회피/완화/전가/수용)**, **ISMS-P**, **개인정보보호법(한국)** + **GDPR(EU)** + **SOX(미국)** 매핑, **3 Lines of Defense Model** |

**핵심 공식 및 파라미터**:

1. **IT 투자 우선순위 점수 (Priority Score)**:
   $$PS = \sum_{i=1}^{n} (W_i \times S_i)$$
   여기서 $W_i$는 i번째 기준의 가중치($\sum W_i = 1.0$), $S_i$는 1~10 점수. 일반적 가중치: 전략정합(0.30), 재무성과(0.25), 위험관리(0.20), 자원가용성(0.15), 규제준수(0.10).

2. **Total Cost of Ownership (TCO) 5년 모델**:
   $$TCO_{5yr} = \sum_{t=0}^{5} \left( C_{HW}(t) + C_{SW}(
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 739 / 800

<- **이전**: [738. IT 경영 관리 핵심 토픽 738번 시험 요약](/studynote/12_it_management/05_security_compliance/738_it_management_core_topic_738_exam_summary/)
**다음**: [740. IT 경영 관리 핵심 토픽 740번 시험 요약](/studynote/12_it_management/05_security_compliance/740_it_management_core_topic_740_exam_summary/) ->

---
