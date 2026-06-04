---
title: "510. CMMI 프로세스 성숙도 모델 (CMMI Process Maturity Model)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CMMI(Capability Maturity Model Integration)는 SEI(Software Engineering Institute)가 개발한 **소프트웨어/시스템/서비스 개발 프로세스의 성숙도를 5단계 레벨(Level 1~5)**로 평가·개선하는 프레임워크로, **22개 프로세스 영역(Process Area, PA)**, **5개 범주(카테고리)**, **목표(SG/GG) 및 실행プラクティ스(GP/SP)**의 계층적 구조로 프로세스 정량화·최적화를 달성한다.
> 2. **가치**: 통계적으로 **Level 2 도달 시 결함률 약 50% 감소, Level 3 도달 시 일정 준수율 65% -> 80%로 향상, Level 4/5에서는 PPM(Process Performance Model) 기반 변동성 1σ 이내 통제**가 가능하며, 글로벌 SW 발주처(DoD, NASA, 한전 등)의 **공급사 자격심사(Acquisition Gate)** 및 한국 SW진흥법의 **SW사업 대가산정 및 검증**의 핵심 평가척도로 활용된다.
> 3. **판단 포인트**: **Staged Representation(단계적 표현)** vs **Continuous Representation(연속적 표현)**의 조직 적합성 판단, **CMMI-DEV/SVC/ACQ/PPL** 4개 모델 중 도메인 매칭, **Agile(Scrum/XP)·DevOps·ISO 9001·ITIL v4**와의 **Harmonization 전략**, 그리고 **SCAMPI A/B/C** 중 비용-기간-신뢰도 트레이드오프에 따른 인증 등급 결정이 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

CMMI는 1980년대 후반 미국 국방성(DoD)의 SW 납품 품질 문제(Standish Group CHAOS Report 기준 **31% 프로젝트 완전 실패**)를 해결하기 위해 SEI의 Watts Humphrey 등이 CMM(Capability Maturity Model, 1991)을 발전시켜 **2002년 v1.0, 2006년 v1.2, 2010년 v1.3, 2018년 v2.0**으로 통합·발전시킨 모델이다. 기존 CMM은 SW-CMM, SE-CMM, IPD-CMM 등 **파편화된 도메인별 모델**을 CMMI로 통합하여 **DEV(개발), SVC(서비스), ACQ(조달), PPL(인력)** 4개 콘스턴트(constant)로 재편, **중복 제거와 통합성(integration)**을 달성했다.

```text
[ CMMI 진화 계보도: 파편화 -> 통합 -> v2.0 ]

   (1987)        (1991~2000)              (2002)              (2010)             (2018)
    SPA -+         SW-CMM v1.1 --+
         +- CMM --+              +-- CMMI v1.0 -- CMMI v1.2 -- CMMI v1.3 -- CMMI v2.0
    DoD -+         SE-CMM -------+    (통합)         (확장)        (개선)         (Biz Value)
                   IPD-CMM -----+
                   SSA-CMM(SVC)-+
                                            |
                                  +---------+----------+----------+
                                  v         v          v          v
                              CMMI-DEV  CMMI-SVC   CMMI-ACQ   CMMI-PPL
                              (개발)     (서비스)   (조달)     (인력)
                                  |         |          |          |
                                  +---------+----------+----------+
                                              |
                                              v
                                  22개 PA / 5개 카테고리 / 5단계 레벨
```

**기존 패러다임 vs CMMI 패러다임 비교**

| 패러다임 | 접근 방식 | 한계점 |
| :--- | :--- | :--- |
| **SW-CMM(1991)** | SW 개발 프로세스만 평가 | 도메인 파편화(SW, 시스템, 인력 중복) |
| **ISO 9001(2000)** | 범용 품질경영시스템(QMS) | **"무엇(What)"만 규정, "어떻게(How)" 부재** -> 프로세스 역량 측정 불가 |
| **CMMI v1.x(2002~2010)** | **SW+시스템+서비스+조달 통합** | 문서화 부담, Agile과 충돌, 적용 비용 과다 |
| **CMMI v2.0(2018)** | **Business Performance Integration** | Agile/DevOps/Lean 친화, 4개 콘스턴트 단순화, **Practice Area 단위 평가** 도입 |

한국에서는 **SW진흥법(2013년 시행)**, **정보시스템 감리**, **SW사업 대가산정 가이드**, **공공기관 SW사업 검증**에서 CMMI 레벨을 발주사격 평가지표로 활용하며, 2024년 기준 국내 인증기업 약 **300여 개사(한국SW기술인협회 집계)**가 분포한다.

- **📢 섹션 요약 비유**: CMMI는 **요리사 양성 시스템**과 같다. 초보(Level 1)->조리사(Level 2: 레시피 준수)->셰프(Level 3: 자신만의 시스템 정립)->마스터 셰프(Level 4: 정량적 맛 분석)->요리 거장(Level 5: 끊임없는 혁신)처럼 **요리하는 능력의 단계적 성장**을 체계적으로 진단·개선하는 프레임워크다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CMMI의 핵심 아키텍처는 **3계층 계층구조(Layered Architecture)**로 구성된다. 최상위 **Maturity Level(5단계)** 또는 **Capability Level(6단계)**, 중간 **Process Area(PA, 22개)**, 최하위 **Goal(목표) + Practice(실행 관행)**이 위계적으로 연결된다.

```text
[ CMMI v1.3 Staged Representation: 5단계 성숙도 모델 ]

                            +-----------------------------+
                Level 5 --- | Optimizing        (최적화)   |  <- CAR, OID 등 2 PA
                            +-----------------------------+
                Level 4 --- | Quantitatively    (정량적   |  <- OPP, QPM 등 2 PA
                            |  Managed           관리)    |
                            +-----------------------------+
                Level 3 --- | Defined           (정의)    |  <- REQM, RD, TS, PI,
                            |                                VER, VAL, PI, PP,
                            |                                SAM, IPM, RSKM,
                            |                                DAR, CM, MA, OEI 등
                            |                                16~18 PA
                            +-----------------------------+
                Level 2 --- | Managed           (관리)    |  <- REQM, PP, SAM, MA,
                            |                                CM, PMC, PPQA, IPM 등
                            |                                7~8 PA
                            +-----------------------------+
                Level 1 --- | Initial           (초기)    |  <- (성공 요인 미정의)
                            |  - Heroic Effort               |
                            +-----------------------------+

[ 프로세스 영역(PA) 계층구조 ]

    Maturity Level (1~5)
        |
        +-- Process Area (PA, 22개)  - e.g., "Requirements Management (REQM)"
        |       |
        |       +-- Specific Goal (SG) - e.g., "SG 1: Requirements are managed"
        |       |       |
        |       |       +-- Specific Practice (SP) - e.g., "SP 1.1: Obtain an understanding of requirements"
        |       |
        |       +-- Generic Goal (GG) - e.g., "GG 2: The process is managed"
        |               |
        |               +-- Generic Practice (GP) - e.g., "GP 2.1: Establish an organizational policy"
        |
        +-- Work Product / Subprocess (산출물 / 하위프로세스)
                - Process Asset Library (PAL)
                - Measurement Repository
                - Process Performance Model (PPM)
                - Defect Repository
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Maturity Level (5단계)** | 조직 단위 성숙도 측정 척도 | L1=Initial / L2=Managed / L3=Defined / L4=Quantitatively Managed / L5=Optimizing. **누적성(Cumulativeness)**: 상위 레벨 달성은 하위 레벨의 모든 PA 충족을 전제 |
| **Process Area (PA, 22개)** | 핵심 프로세스 영역 (e.g., REQM, PP, SAM, IPM, RSKM, CM, PMC, PPQA, MA, OEI) | 각 PA별로 **1~3개 SG(Specific Goal)**와 **다수의 SP(Specific Practice)** 보유. **5개 카테고리**: Process Management / Project Management / Engineering / Support / Cross-cutting |
| **Goal (목표)** | SG(특정 목표) + GG(공통 목표) | SG는 PA별 **필수 달성 목표(Must)**, GG2~GG5는 **레벨별 공통 필수(Institutionalization)**: GG2=관리, GG3=정의, GG4=정량관리, GG5=최적화 |
| **Practice (실행 관행)** | SP(특정 관행) + GP(공통 관행) | SP 1.1~3.x: PA별 상세 실행항목, **GP 2.1~5.2**: 정책 수립, 계획, 자원, 책임, 측정, 통제, 혁신 등 7개 영역의 **공통 프레임워크** |
| **Appraisal Method** | 평가 방법론 | **SCAMPI(Standard CMMI Appraisal Method for Process Improvement)** A/B/C 3단계: **Class A**(리더 1+팀원 2~4, 4~7일, 공식 인증, **$80K~$150K** 비용) / **Class B**(내부 진단, 공식 인증 불가) / **Class C**(간이 평가, 1~3일) |
| **CMMI v2.0의 Practice Area (PA, 25개)** | v2.0에서 재편된 영역 | **4 Performance Domain**(Doing, Managing, Enabling, Improving) × **Practice Area** 구조. **8개 핵심 PA**(`ESTIM, PLAN, MON, REQM, RD, TS, VAL, VER`) + 추가 영역 |

**CMMI 5단계 성숙도의 핵심 메커니즘 상세**

1. **Level 1 (Initial/초기단계)**: 프로세스 정의 부재, **Heroic Effort(영웅적 노력)**에 의존. SEI 통계에서 L1 조직의 **예산 초과율 89%, 결함 밀도 1.5 defects/KLOC** 기록.
2. **Level 2 (Managed/관리단계)**: 프로젝트 단위 기본 프로세스 수립. **7개 PA 필수**: REQM, PP, SAM, MA, CM, PMC, PPQA (CMMI-DEV v1.3). 핵심 관행: **Commit to Plan(계획 수립 및 커밋먼트)**, **Manage Configurations(형상 통제)**, **Track Performance(성과 추적)**.
3. **Level 3 (Defined/정의단계)**: 조직 표준 프로세스(OSP) **Process Asset Library(PAL)** 구축. **16개 추가 PA**: RD(Requirements Development), TS(Technical Solution), PI(Product Integration), VER(Verification), VAL(Validation), IPM(Integrated Project Management), RSKM(Risk Management), OEI(Organizational Environment for Integration) 등. **Tailoring Guidelines**로 프로젝트별 맞춤.
4. **Level 4 (Quantitatively Managed/정량적 관리)**: **Process Performance Model(PPM)**, **Process Performance Baseline(PPB)** 수립. **통계적 기법(SPC, Statistical Process Control)** 적용: **Six Sigma 개념 통합**. 2개 PA: **OPP(Organizational Process Performance)**, **QPM(Quantitative Project Management)**. **σ-Level 측정**: **2σ(95.5%) -> 4σ(99.99%)** 수준 변동성 통제.
5. **Level 5 (Optimizing/최적화)**: **지속적 혁신 프로세스(CAR/Causal Analysis and Resolution)** 및 **Organizational Innovation and Deployment(OID)**. **Defect Causal Analysis(DCA)**, **PIL(Process Improvement Lead)** 통한 **PDCA 사이클 가속화**.

**CMMI v2.0의 핵심 변화(v1.3 -> v2.0)**

- **평가 단위 변경**: PA 22개 -> **Practice Area 25개** + **Practice Group 76개** + **Practice 411개**로 세분화
- **3-Pillar 구조**: **Practice(관행) + Performance(성과) + Skill(역량)** 통합 평가
- **Burst 평가**: 프로젝트 단위 **단기/반복적** 평가 지원 (Agile 친화)
- **CMMI Model Foundation**: 모든 콘스턴트의 **공통 베이스 12개 PA** 통합
- **가격 정책 단순화**: ~$4,950/평가팀 + $1,650/사이트 (v2.0)

- **📢 섹션 요약 비유**: CMMI의 5단계는 **운전면허 단계**와 같다. L1은 **도로 위 첫 차량**(무면허 위험), L2는 **응急運転免許(기본 운전 가능)**, L3는 **1종 보통면허(정통 운전 스킬)**, L4는 **1종 대형/특수면허(고속도로 장거리 안전 운전)**, L5는 **경찰·레이서(사고 시 즉각 원인 분석 및 예방)**에 비유할 수 있다.

---

## Ⅲ. 비교 및 연결

CMMI는 유사한 프로세스 개선 프레임워크와 **상호 보완적 관계**이거나 **경쟁/대체 관계**에 있다. 기술사 시험에서는 이들의 차이를 정확히 구분하고 **조직 상황에 맞는 통합 전략**을 제시해야 한다.

| 구분 | **CMMI** | **ISO 9001 / ISO/IEC 33001~33099** | **ITIL v4** | **Agile (Scrum/XP)** | **DevOps (CALMS)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **목적** | 프로세스 **역량/성숙도** 측정 | QMS 인증(전사 품질경영) | **IT 서비스 운영** 개선 | **반복적·적응적** 제품 개발 | **개발+운영 통합** 자동화 |
| **구조** | 5단계 / 22 PA | 7 원칙 / 10개 조항(Clause) | 4 차원 / 34 Practice | Sprint / Ceremony | C-A-L-M-S 5개 축 |
| **측정** | 정성(목표 달성) + 정량(PPM) | 정성(절차 준수) | 정성(Practice 채택) | **Velocity, Burn-down** | **DORA 4 Metrics**(배포빈도, 리드타임, MTTR, 변경실패율) |
| **인증** | SCAMPI Class A (공식 인증, 3년 유효) | ISO 인증 (3년 유효, 매년 감시) | PeopleCert 공식 인증 (자격증) | Scrum.org, SAFe 등 (자격증) | DORA Assessment |
| **적합 조직** | 중·대규모 SW/SI 사업체 | 전 산업군 | IT 운영/서비스 조직 | 스타트업·SW 제품 개발 | 클라우드 네이티브, MSA |
| **한계** | 문서화 부담, 변화 대응 지연 | SW 프로세스 역량 미측정 | 개발 프로세스 미포함 | 스케일링·거버넌스 약점 | 측정 도구 의존 |
| **통합** | **CM
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 510 / 600

<- **이전**: [509. ISO 25010 소프트웨어 품질 모델](/studynote/11_design_supervision/06_exam_summary/510_iso_25010_software_quality_model/)
**다음**: [511. SPICE ISO 15504 프로세스 평가](/studynote/11_design_supervision/06_exam_summary/511_spice_iso_15504_process_assessment/) ->

---
