---
title: "589. IT 경영 관리 핵심 토픽 589번 시험 요약 (IT Management Core Topic 589 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, PMBOK 7th 등 글로벌 거버넌스 프레임워크를 기반으로, IT 거버넌스·전략·포트폴리오·프로젝트·운영·리스크를 end-to-end로 통합하여 **기업의 디지털 가치(Value Realization)** 를 극대화하는 경영 체계이다.
> 2. **가치**: BSC·KPI 기반 성과 측정을 도입할 경우 IT 투자 대비 ROI 평균 25~40% 개선, SLA 준수율 95% 이상, 주요 인시던트 MTTR 60% 단축, 정보화 사업의 실패율(전통 60~70% -> 관리형 15% 이하)을 달성할 수 있다.
> 3. **판단 포인트**: **"표준 프레임워크 무조건 도입 vs. 기업 맥락에 맞춘 경량화 적용"**, **"거버넌스 강도(Compliance 우선) vs. 가치창출 우선(Value-Driven)"**, **"내부 역량 중심 vs. 아웃소싱·클라우드 활용"**의 세 가지 축을 사업 특성·조직 성숙도·규제 환경에 따라 균형 있게 결정해야 한다.

---

## Ⅰ. 개요 및 필요성

제4차 산업혁명(AI·클라우드·빅데이터·IoT) 환경에서 IT는 단순 비용(Cost Center)이 아닌 **전략적 가치 창출 동력(Strategic Enabler)** 으로 재정의되었다. 그러나 한국 정보화진흥원의 조사에 따르면 국내 정보화 사업의 약 60%는 예산 초과, 45%는 기대 효과 미달, 30%는 완전 실패(MIS Alignment 실패)로 귀결된다. 이는 IT에 대한 **경영 관점의 통합 거버넌스 부재**가 근본 원인이다.

이에 정부·공공기관은 「정보시스템의 효율적 도입 및 운영에 관한 지침」(2022 개정), ISMS-P, 클라우드 이용자 보호 가이드라인 등을 통해 IT 거버넌스 의무화를 강화하고 있으며, 민간도 DART 공시·ESG 공시 확대로 IT 거버넌스 수준의 재무적·비재무적 가시화가 요구되고 있다. 따라서 기술사는 단순 기술 도입자가 아닌, **"IT-Business Alignment"를 실현하는 경영 컨설턴트**로서 거버넌스·전략·운영·리스크를 통합 설계할 수 있어야 한다.

```text
       +--------------------------------------------------------+
       |          기업 경영 목표 (Vision · Strategy)              |
       |   - 매출 성장  - 비용 절감  - 고객 만족  - ESG        |
       +-----------------------+--------------------------------+
                               |  (Strategic Alignment)
       +-----------------------v--------------------------------+
       |            IT 거버넌스 (IT Governance)                  |
       |  +----------+  +----------+  +----------+  +--------+ |
       |  | 전략(Str) |  | 포트폴리오|  | 프로젝트 |  | 운영/  | |
       |  | ·EA·ISP  |-> | (PfM)   |-> | (PMO)   |-> | 서비스| |
       |  +----------+  +----------+  +----------+  +--------+ |
       |  ^ Decision (의사결정권)        v Accountability        |
       |  | Board -> IT Steering Committee -> CIO -> IT조직      |
       +--------------------------------------------------------+
                               |  (Performance & Risk)
       +-----------------------v--------------------------------+
       |         평가·측정·리스크 (Monitor · Evaluate · Direct)  |
       |   KPI/BSC · TCO/ROI · ISMS · BCP/DR · Compliance        |
       +--------------------------------------------------------+
```

기존 **"프로젝트 단위 관리"** (사일로 방식, CapEx 일회성, 벤더 종속)에서, **"포트폴리오·서비스·가치 중심 관리"** (라이프사이클 통합, OpEx·구독모델, 다중 벤더·클라우드) 패러다임으로 전환되었다. 이는 Zachman EA -> TOGAF, PRINCE2 -> PMBOK Agile, ITIL v3 -> ITIL 4의 프레임워크 진화에서도 확인된다.

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차의 **"운전대·내비게이션·블랙박스·정비 시스템"**이 통합된 *차량 관제 시스템*과 같다. 차체(기술·시스템)는 아무리 좋아도, 운전대(거버넌스)와 내비(전략)가 없으면 목적지에 도달할 수 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리는 **5개 도메인(Strategy · Portfolio · Project · Operation · Risk)** 을 **3개 거버넌스 레이어(Board · Steering · Delivery)** 가 관통하는 **Governance-Management-Performance Loop** 구조로 동작한다.

```text
   +------------------------------------------------------------+
   |       거버넌스 루프 (Evaluate · Direct · Monitor)            |
   |       COBIT 2019  / ISO 38500  /  ISMS-P                    |
   +------------------------------------------------------------+
            |                                        ^
   +--------v--------+  +--------------+  +----------+--------+
   | ① IT 전략       |  | ② IT 포트폴리오|  | ③ IT 프로젝트      |
   |  (ISP/EA)       |  |  (PfM/PPM)     |  |  (PMO/EPM)        |
   |  - 환경분석     |  |  - 수요관리    |  |  - WBS/스케줄     |
   |  - TO-BE 모델   |  |  - 평가/선정   |  |  - 이해관계자     |
   |  - 로드맵       |  |  - 균형/최적화 |  |  - 품질/형상관리  |
   +--------+--------+  +--------+------+  +--------+----------+
            |                    |                  |
            +--------------------+------------------+
                                 v
   +------------------------------------------------------------+
   | ④ IT 운영/서비스 관리 (ITIL 4 Service Value System)         |
   |   - 서비스 전략/설계/전환/운영/개선(SVC)                     |
   |   - SLA/OLA/UC, 인시던트·문제·변경·릴리스 관리             |
   |   - DevOps · SRE · AIOps                                   |
   +------------------------------------------------------------+
                                 |
                                 v
   +------------------------------------------------------------+
   | ⑤ 리스크·컴플라이언스·보안 (GRC)                            |
   |   - ISMS-P · PIPC · ISO 27001 · NIST CSF · BCP/DR          |
   |   - 3Lines Model(1st:운영, 2nd:리스크/컴플, 3rd:내부감사)  |
   +------------------------------------------------------------+
                                 |
                                 v
   +------------------------------------------------------------+
   | 성과 측정(Value Realization)                                |
   |   BSC 4관점(재무·고객·내부·학습성장) × KPI -> IT Scorecard  |
   |   TCO · NPV · IRR · EVA · Payback · NPV/ROI               |
   +------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **IT 거버넌스 위원회 (ITSC)** | 의사결정·감독·자원 배분 | 이사회 산하, CIO·CFO·CBRO·사업본부장 참여, 분기 1회 의사결정, RACI 매트릭스 기반 권한 위임 |
| **EA(전사 아키텍처) / ISP** | 전략 -> 시스템 전이 | TOGAF ADM(8단계) 또는 Zachman 6×6 매트릭스로 BA·DA·AA·TA 4관점 모델링, As-Is/To-Be/Transition Roadmap 도출 |
| **PMO(Project Management Office)** | 프로젝트 통합 통제 | PMBOK 7th(원리 12개 + 8성능영역) 또는 PRINCE2(7원리·7프로세스), EVM(Earned Value), WBS·OBS·RBS 연동, 리스크 등록부 |
| **IT 운영 조직 / SRE** | 서비스 안정성·지속성 | ITIL 4 34개 Practice 중 Incident·Problem·Change·Service Desk 운영, SLO/Error Budget 기반 신뢰성 엔지니어링, MTTR·MTBF·가용률 99.9% 목표 |
| **GRC(거버넌스·리스크·컴플라이언스)** | 리스크·규제 통합 관리 | ISMS-P 인증(연 1회 심사), 3Lines of Defense, Risk Register·Heatmap, BCP/DR RTO/RPO 정의, PIPC 개인정보 영향평가 |
| **성과 측정 시스템 (BSC·KPI)** | IT 가치 정량 입증 | BSC 4관점 × IT BSC(Weill/Ross 모델), KPI Cascade(기업->IT->팀->개인), ROI·TCO·NPV·IRR·EVA·Payback Period·IT Cost Ratio 동시 산출 |
| **아웃소싱·클라우드 거버넌스** | 외부 서비스 통제 | SLA·OLA·UC 3계층, 다중 벤더 관리, Exit Strategy(데이터 이관·Lock-in 방지), 한국 클라우드 보안인증(CSAP) |

**핵심 메커니즘: "Value Realization Loop"**
1. **Plan**: ISP·EA·전략 로드맵 -> KPI 도출
2. **Design**: COBIT 2019 40 Governance/Management Objective 중 해당 도메인 선택
3. **Build/Acquire**: 프로젝트 발주·계약·내/외부 자원 조합
4. **Deliver/Support**: SLA·인시던트·변경·릴리스 운영
5. **Monitor/Evaluate**: KPI·BSC·감사·측정 -> 개선 과제 환류

이 5단계가 끊임없이 순환하며, 각 단계에서 **"누가(Who) · 무엇을(What) · 어떻게(How) · 왜(Why)"** 의 4W가 RACI와 OPA(Organizational Process Assets)로 문서화되어야 한다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **"식당의 주방 운영 시스템"**과 같다. 메뉴 기획(전략) -> 식재료 발주(포트폴리오) -> 요리 진행(프로젝트) -> 서빙(운영) -> 위생·고객불만 점검(리스크) -> 손님 반응(성과) -> 다음 메뉴 개선으로 다시 연결되는 일종의 *서비스 사이클*이다.

---

## Ⅲ. 비교 및 연결

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7th** |
| :--- | :--- | :--- | :--- |
| **목적** | IT 거버넌스·경영 통제 (What) | IT 서비스 운영·가치 (How to deliver) | 프로젝트 단위 성공·임시 조직 관리 |
| **관점** | Board·경영자 (Top-down) | 실무 운영자 (Bottom-up) | 프로젝트 매니저·팀 |
| **구조** | 40 Governance & Management Objectives, 7 Component(원리·정책·프로세스·조직·정보·인력·문화) | 34개 Best Practice, SVS(Service Value System), 4P(Product·Partner·People·Process) | 12 Principles of Project Mgmt, 8 Performance Domain |
| **핵심 산출물** | Cascade of Goals -> IT Goals -> Enabler Goals | Service Value Chain(Plan->Engage->Design->Obtain->Build->Deliver->Support), SLA/SLO | Project Charter, WBS, Risk Register, Lessons Learned |
| **수명주기** | 지속적 거버넌스 (영구) | 서비스 라이프사이클 (운영 중심) | 임시적 (시작~종료) |
| **한국 활용** | ISMS-P, 공공 IT 거버넌스 표준 | 공공 클라우드·공공 SI, SI사업 SLA | 국가 정보화 사업, R&D 과제 |
| **상호보완** | IT 전략·리스크 통제 | IT 운영·서비스 품질 | 프로젝트 단위 실행 |

**다른 표준/제도와의 연결**

- **ISO 38500 (Corporate Governance of IT)**: COBIT의 상위 거버넌스 표준, 이사회 책임성(Accountability) 강조
- **ISO 27001/ISMS-P**: 정보보안 통제, COBIT의 *APO12 Manage Risk*, *DSS05 Manage Security Service*와 매핑
- **NIST CSF / 800-53**: 미국 연방 표준, 글로벌 멀티국가 운영 시 필수, ISMS-P와 1:N 매핑 가능
- **DAMA-DMBOK**: 데이터 거버넌스, COBIT의 *DSS03 Manage Data*와 연계, 데이터 카탈로그·마스터·품질 통제
- **Agile/DevOps/SRE**: PMBOK·ITIL과 통합 (예: ITIL 4 34 Practice 중 "Release Management" ↔ DevOps CI/CD)
- **EA Framework (TOGAF/Zachman)**: ISP·전사아키텍처 단계에서 활용, COBIT의 *APO02 Manage Strategy*와 연결
- **BPM(CBOK)**: 프로세스 거버넌스, *APO04 Manage Innovation* 및 *EDM02 Ensure Benefits Delivery*와 연계

- **📢 섹션 요약 비유**: COBIT은 **"도시계획·법률"**, ITIL은 **"도로·상하수도 관리"**, PMBOK은 **"개별 건물 건축 매뉴얼"**이다. 좋은 도시는 세 가지가 함께 작동할 때 완성된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **거버넌스 설계 검증**: ITSC 운영 현황(RACI 명세, 의사결정 권한 위임 매트릭스), COBIT 2019 7 Component 중 *Process·Organizational Structure·People, Skills and Competencies*가 현 조직에 매핑되는지, ISO 38500 6원칙(Responsibility·Strategy·Acquisition·Performance·Conformance·Human Behavior)이 충족되는지 점검
2. **전략 정렬도 측정**: Enterprise Goal -> IT Goal -> Enabler Goal의 Cascade에서 *IT BSC(Weill/Ross)* 활용, Alignment Maturity (Luftman 5단계) 자가 진단, 사업 전략 변경 시 IT 로드맵 갭 분석
3. **포트폴리오 균형화**: BCG Matrix × Risk-Value 2×
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 589 / 800

<- **이전**: [588. IT 경영 관리 핵심 토픽 588번 시험 요약](/studynote/12_it_management/05_security_compliance/588_it_management_core_topic_588_exam_summary/)
**다음**: [590. IT 경영 관리 핵심 토픽 590번 시험 요약](/studynote/12_it_management/05_security_compliance/590_it_management_core_topic_590_exam_summary/) ->

---
