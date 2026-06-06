---
title: "IT Management Core Topic 693 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 693. IT 경영 관리 핵심 토픽 693번 시험 요약
## — IT 거버넌스 × 전략기획 × 디지털 전환 통합 프레임워크 —

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 693번은 단순한 IT 운영이 아닌, **COBIT 2019 + ISO/IEC 38500 + ISO 38505-2(데이터 거버넌스) + EA(TOGAF/DoDAF) + 거버넌스-리스크-컴플라이언스(GRC)**가 융합된 **"가치창출형 IT경영 체계"**를 평가하는 문제로, IT를 비용중심에서 **전략자산 및 비즈니스 가치 엔진**으로 전환시키는 통합 관리 프레임워크 구축 능력을 검증함.
> 2. **가치**: 정성적으로는 의사결정 투명성·이해관계자 신뢰·규제 대응력 향상, 정량적으로는 **IT 투자 대비 ROI 20~35% 개선, 프로젝트 실패율 40%->15% 이하 감소, TCO 25% 절감, 감사 적발 건수 60% 이상 감소, Time-to-Market 30% 단축** 효과를 기대할 수 있음.
> 3. **판단 포인트**: 핵심은 **①거버넌스-관리-운영의 3계층 분리, ②센터-스포크 모델 vs 페더레이션 모델 선택, ③CSF/KPI/GMI(Goal Monitoring Indicator) 계측구조, ④Agile/DevOps 환경에서의 거버넌스 임베딩 vs 오버헤드, ⑤Data Mesh vs Centralized Data Lake** 간 트레이드오프를 아키텍처 관점에서 명확히 판단하는 것임.

---

## Ⅰ. 개요 및 필요성

전통적 IT관리는 **"시스템 가용성·장애대응·라이선스 준수"**라는 후행적(Reactive) 관점에 머물러 있었다. 그러나 4차 산업혁명, 클라우드 전환, AI/ML 확산, 개인정보보호법·ESG 규제 강화에 따라 IT는 **"비즈니스 코어"**로 재편되었고, 이로 인해 단순 운영 효율성만으로는 경영진과 이사회를 설득할 수 없는 상황이 도래했다. 한국정보화진흥원(KIA) 및 디지털정부 추진에 따라 공공·민간 모두 **"디지털 전환(DX) 성과 가시화"**가 핵심 KPI로 부상했다.

특히 **클라우드 네이티브, SaaS 확산 -> Shadow IT 증가(전통 기업의 평균 30~40%)**, **AI 윤리·알고리즘 편향 이슈**, **공급망 다변화(공급망 리스크 SBOM)**, **ISO 27001·27701·27018·ISMS-P 인증 의무화** 등 규제 환경이 복합화되면서, 단일 표준만으로는 통합 거버넌스가 불가능해졌다. 이에 따라 **COBIT 2019의 Focus Area(46개), NIST CSF 2.0의 Govern 함수, ISO 38500의 6원칙(Evaluate·Direct·Monitor)**, 그리고 **K-ICT 표준프레임워크, EA 참조모델(ARM), 데이터 거버넌스법(데이터 산업법, 2022.3 시행)**까지 통합한 **693번형 통합 거버넌스 모델**이 요구된다.

```text
[693번 통합 IT경영 거버넌스 아키텍처 개요]

                  +----------------------------------------+
                  |   이사회 / 경영진 (Steering Committee) |
                  |   - IT전략위원회 / 디지털혁신위 / CISO  |
                  +--------------+-------------------------+
                                 | (Evaluate / Direct / Monitor)
                                 v
        +----------------------------------------------------+
        |      거버넌스 계층 (Governance Layer)               |
        |  +------------+  +------------+  +--------------+  |
        |  | COBIT 2019 |  | ISO 38500  |  | ISO 38505-2  |  |
        |  |   40 Obj.  |  | 6 Principles|  | Data Gov.    |  |
        |  +------------+  +------------+  +--------------+  |
        |       +  ISO 27001/27701 (정보/개인정보 보호)        |
        |       +  ISO 31000 / ISO 37301 (리스크·컴플라이언스) |
        +--------------------+-------------------------------+
                             |
                             v
        +----------------------------------------------------+
        |      관리 계층 (Management Layer)                   |
        |  +------------+  +------------+  +--------------+  |
        |  | 전략기획   |  |  EA/표준화 |  | 포트폴리오/  |  |
        |  | (ISP/ISP-  |  | (TOGAF ADM |  | 프로그램/    |  |
        |  |  BPM)      |  |  /DoDAF2)  |  | 프로젝트관리 |  |
        |  +------------+  +------------+  +--------------+  |
        |  + 데이터 거버넌스(Data Mesh/Fabric), IT재무(OpEx/CapEx)
        +--------------------+-------------------------------+
                             |
                             v
        +----------------------------------------------------+
        |      운영 계층 (Operations Layer)                  |
        |  +----------+ +----------+ +--------+ +--------+ |
        |  |ITIL 4    | |DevOps    | |AIOps   | |FinOps  | |
        |  |(SVS 34)  | |(SAFe/    | |(SRE)   | |(CSP)   | |
        |  |          | |LeSS)     | |        | |        | |
        |  +----------+ +----------+ +--------+ +--------+ |
        |  + K-ICS, ISMS-P, 클라우드 보안인증(CSAP)         |
        +----------------------------------------------------+
                             |
                             v
        +----------------------------------------------------+
        |     성과·측정 계층 (Measurement & Value Layer)     |
        |  CSF -> KPI -> KGI -> GMI -> Balanced Scorecard(BSC) |
        |  +  데이터품질지수(DQI),  IT성숙도(CMMI 2.0)        |
        +----------------------------------------------------+
```

**구시대의 패러다임(CMMI·ITIL v3 중심, CapEx 무한투자, IT=비용센터)** 대비, 693번이 요구하는 신패러다임은 **①가치지향(Value-Driven), ②표준간 매핑(Harmonization), ③실시간 측정(Real-time GMI), ④민첩성(Adaptive), ⑤지속가능성(ESG·Green IT)** 이다. 즉, IT를 **"기술 사일로"가 아닌 "전략 무기"**로 재정의하는 것이다.

- **📢 섹션 요약 비유**: 거버넌스 체계는 마치 **국제공항의 관제탑(Control Tower)**과 같다. 비행기(프로젝트·서비스·데이터)가 수도 없이 이착륙하는 혼잡한 활주로 위에서, 관제탑은 **단일 레이더(CSF), 다층 관제사 거버넌스, 자동 충돌방지 시스템(컴플라이언스)**, **활주로 운영 매뉴얼(EA/표준)**을 종합 운용하여, **모든 비행기가 안전·정시·경제적으로 목적지에 도달**하도록 만든다.

---

## Ⅱ. 아키텍처 및 핵심 원리

693번의 핵심은 **"이해관계자 니즈 -> 전략 -> 포트폴리오 -> 아키텍처 -> 구현 -> 측정 -> 개선"**의 폐루프(Closed-loop)를 어떻게 설계하느냐이다. 이를 COBIT 2019의 **Governance & Management Objectives(40개)**와 **핵심 모델(Governance System Components 7개: Process/Organizational Structures/Information/Flows/People·Skills·Competencies/Principles·Policies·Frameworks/Culture·Ethics·Behavior)** 으로 구체화한다.

```text
[693번 핵심 폐루프: Cascading Goals -> Value Realization]

    Stakeholder         Enterprise           IT-Related
   Needs (Drivers) ---► Goals (KGI)  ---►   Goals (KGI)
   ----------------    ------------        --------------
   • 고객만족도^        • 신사업매출 30%^   • DX 프로젝트 5건
   • 규제 준수          • ESG 점수 A        • 클라우드 전환 60%
   • 시장점유율 5%^     • 운영비 15%절감    • ISMS-P 인증 유지
   • 인재 확보                              • DevOps 배포 주기 1일
                        |                    |
                        +----+---------------+
                             v
              +------------------------------+
              |  IT CSF(핵심성과지표)        |
              |  - Sourcing Strategy (CSF)   |
              |  - Architecture (CSF)        |
              |  - Innovation (CSF)          |
              |  - Risk Optimization (CSF)   |
              +--------------+---------------+
                             v
              +------------------------------+
              |  KPI -> Process Metric        |
              |  (예: 배포실패율, MTTR, NPS) |
              +--------------+---------------+
                             v
              +------------------------------+
              |  GMI(Goal Monitoring Indic.) |
              |  +  BSC 4관점(재무/고객/     |
              |    내부프로세스/학습성장)     |
              +--------------+---------------+
                             v
              +------------------------------+
              |  Value Realization (성과환류)|
              |  -> 차기전략·예산 재반영       |
              +------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **전략기획 체계(ISP)** | 기업목표 -> IT목표 -> IT전략 -> IT투자의 연결 | 정보화전략계획(ISP) 수립 5단계(현황분석->비전수립->목표정의->전략과제->실행계획), ISP-BPM 기반 BPI, ISP와 EA간 양방향 피드백, **ISP-수립시 5개년 로드맵 + Balanced Scorecard 4관점 동시 도출** |
| **EA(Enterprise Architecture)** | 비즈니스-데이터-애플리케이션-기술 4계층 정합성 확보 | **TOGAF ADM 8단계 Phase( Preliminary->A~H)**, **ArchiMate 3.2 표기법**, **DoDAF 2.02 Viewpoint(8종)**, **FEAF(연방EA) RM-ODP 5관점**, **갭분석 / SBB(Solution Building Block) 재사용률 측정**, 한국정부의 **EA 참조모델(ARM) 4종(업무/데이터/애플리케이션/기술)** |
| **거버넌스 체계(COBIT)** | 거버넌스-관리(40 Obj.)-운영 3계층 통합 | **COBIT 2019**: 5 Governance Components, 7 Component(Process, Org, Info, Flows, People, Principles, Culture), **Design Factors 11개(전략, 컴플라이언스, 리스크 등)**로 시스템 가중치 동적 산정, **COBIT 2019 + NIST CSF 2.0 1:1 매핑(상세 매핑표)**, **COBIT 2019의 46개 Focus Area**에서 필요한 것만 발췌해 운영 |
| **리스크/컴플라이언스(GRC)** | 리스크 통합관리·규제 준수·내부통제 일원화 | **ISO 31000:2018 7단계 리스크관리 프로세스**, **ISO 37301:2021 컴플라이언스경영**, **3 Lines of Defense(3LoD) 모델**(1LoD: 사업부, 2LoD: 리스크·컴플라이언스, 3LoD: 내부감사), **RSA(Risk-Scenario-Assessment) 매트릭스(영향도×가능성)**, **Bow-tie 분석, Monte-Carlo 시뮬레이션** |
| **IT서비스 운영(ITIL/DevOps)** | 서비스 카탈로그 기반 운영 + 지속적 배포 | **ITIL 4 SVS(Service Value System) 34개 Practice**, **Service Value Chain(Engage->Design->Transition->Obtain->Deliver->Support)**, **DevOps 4 메트릭(배포빈도/리드타임/변경실패율/MTTR) - DORA Metrics**, **SRE Error Budget 25% 가용성 보장**, **AIOps(Anomaly Detection, RCA 자동화)** |
| **데이터 거버넌스** | 데이터 품질·마스터·메타·보안·수명주기 통합관리 | **DAMA-DMBOK 2.0 11개 지식영역**, **데이터 거버넌스법(2022.3)**, **마이데이터 사업자·가명정보 처리**, **데이터 메쉬(Data Mesh) - 도메인 자율성 4원칙**, **데이터 패브릭(데이터 카탈로그 + 가상화)**, **메타데이터 관리: Active/Working/Asset 메타 3계층**, **DQI(Data Quality Index) = 완전성×정합성×정확성×적시성 가중평균** |
| **정보보안 거버넌스** | CIA(기밀성·무결성·가용성) + 개인정보 + 사이버 회복력 | **ISMS-P 104개 통제항목(2024개정)**, **ISO 27001:2022 Annex A 93개 통제(4개 영역 23개 카테고리)**, **NIST CSF 2.0 6함수(GV/ID/PR/RC/DE/RS)**, **제로트러스트(SDP + MFA + L7 마이크로세그먼테이션 + BeyondCorp)**, **SBOM(SPDX/CycloneDX) + SLSA Lv.3 + 코드서명**, **CRA(EU Cyber Resilience Act) 대응** |

**핵심 산식 및 파라미터 (기술사 빈출)**:

```
[1] ROI 산식 (정보화사업)
   ROI = (Total Benefit - Total Cost) / Total Cost × 100 (%)
   총편익(B) = Tangible Benefit(직접) + Intangible Benefit(간접, 가중치 0.3~0.5)
   총비용
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 693 / 800

<- **이전**: [692. IT 경영 관리 핵심 토픽 692번 시험 요약](/studynote/12_it_management/05_security_compliance/692_it_management_core_topic_692_exam_summary/)
**다음**: [694. IT 경영 관리 핵심 토픽 694번 시험 요약](/studynote/12_it_management/05_security_compliance/694_it_management_core_topic_694_exam_summary/) ->

---
