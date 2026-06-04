+++
title = "511. SPICE ISO 15504 프로세스 평가 (SPICE ISO 15504 Process Assessment)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ISO/IEC 15504(SPICE)는 소프트웨어 프로세스를 **5단계 능력수준(Level 0~5)**과 **9개 프로세스속성(PA 1.1~5.2)**으로 정량 평가하는 이차원 평가 프레임워크로, Process Reference Model(PRM)과 Process Assessment Model(PAM)을 통해 프로세스 수행역량(Process Capability)을 측정·비개선한다.
> 2. **가치**: 조직의 프로세스 성숙도를 **Capability Level(0~5)**로 수치화하여 프로젝트 선정·발주자 신뢰도 확보·프로세스 개선 ROI 측정이 가능하며, 자동차·의료·방산·금융 등 안전필수(safety-critical) 산업에서 **공급망 평가(Supply Chain Assessment)**의 글로벌 표준으로 자리잡았다.
> 3. **판단 포인트**: 평가자(Assessor) 역량·증거수집 방식(문서/인터뷰/관찰)의 신뢰도 vs 비용 트레이드오프, **Automated SPICE(ASPICE)**와 **CMMI-DEV v1.3/v2.0** 간 매핑 전략, 평가 범위(Scope: 프로젝트 단위 vs 조직 단위) 설정이 ROI를 결정하는 핵심 설계변수이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 등장 배경

1990년대 초반 유럽 각국의 SW 품질 평가 방식이 상이하여 **다국적 SW 거래의 비대칭성**이 심각했다. EC(European Commission)는 1991년 **SPICE 프로젝트(Software Process Improvement and Capability dEtermination)**를 착수하고, 이후 1998년 ISO/IEC JTC1/SC7에 의해 **ISO/IEC TR 15504(기술보고서)**로 표준화되었으며, 2003~2006년 정식 국제표준(International Standard)으로 승격되었다. 2015년 이후 **ISO/IEC 330xx 시리즈**(33001:용어, 33002:PRM, 33003:요구사항, 33004:확장용어, 33020:측정프레임워크, 33030:도입지침)로 전면 개편되었다.

### 1.2 기존 평가 패러다임의 한계

| 시대 | 평가 방식 | 한계점 |
| :--- | :--- | :--- |
| 1980년대 | 체크리스트·숙의적 평가 | 주관성, 평가자 의존도 높음 |
| 1990년대 초 | CMM(Capability Maturity Model) 도입 | 평가 절차·증거 표준 부재 |
| 1990년대 후반~ | ISO 15504 / CMMI 등장 | 프로세스별 능력등급 + 프로세스영역 통합 |
| 2010년대 이후 | ASPICE·CMMI v2.0·ISO 330xx | 자동차 산업, 자동화 측정, 도구 통합 |

```text
[다국적 SW 공급망 평가의 비대칭성 문제]

   발주자(한국)                          공급자(인도)
  +--------------+                     +--------------+
  |  자체 품질 기준 | --계약을 위해--->  | 자체 품질 기준 |
  |  "우리 표준이    |  객관적 증거 부족   |  "우리 표준이    |
  |   최고"라고 주장 |  <--------------->  |   최고"라고 주장 |
  +------+-------+                     +------+-------+
         | 공통 어휘(Common Language)와 측정 기준 부재
         v                                    v
   +--------------------------------------------------+
   |  ISO/IEC 15504 (SPICE) — 세계 공통 평가 어휘    |
   |  +----------+  +----------+  +----------+      |
   |  |  Level 0 |->|  Level 1 |->|  ... 5   |      |
   |  |Incomplete|  |Performed |  |Optimizing|      |
   |  +----------+  +----------+  +----------+      |
   +--------------------------------------------------+
              객관적·반복가능·비교가능한 평가
```

### 1.3 정의 및 핵심 명제

- **Process(프로세스)**: 입력물을 출력물로 변환하기 위해 수행되는 활동 집합
- **Process Capability(프로세스 능력)**: 정의된 프로세스가 현재 달성할 수 있는 능력 범위
- **Process Performance(프로세스 수행)**: 프로세스를 통해 달성된 실제 결과의 정도
- **Assessment(평가)**: PAM에 따라 조직의 프로세스 능력을 측정하는 체계적 활동

- **📢 섹션 요약 비유**: ISO 15504는 마치 **의료 검진 표준**과 같다. 의사(평가자)마다 진단 기준이 달랐는데, 표준 검진 항목(프로세스속성)과 단계(능력수준)를 정해 누구라도 같은 결과를 얻도록 만든 것.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 이차원 평가 구조

ISO 15504의 핵심은 **두 개의 직교 차원**으로 프로세스를 평가하는 것이다.

```text
[ISO/IEC 15504 이차원 평가 모델 (PRM × PAM)]

                    +-----------------------------------------+
                    |         Process Dimension               |
                    |  (평가 대상: 무엇을 평가하나)            |
                    |                                         |
   Capability       |  ENG.1  ENG.2  ENG.3  ENG.4 ... MAN.1   |
   Dimension        |  SW요구 SW설계 SW구현 SW테스트  관리    |
   (얼마나 잘하나)   |   |      |      |      |         |     |
                    |   v      v      v      v         v     |
   +-------------+  |  CL=2   CL=3   CL=2   CL=4     CL=3    |
   | Level 5 (L5)|  |                                         |
   | Optimizing  |  |  ░░░░░░░░░░░░░░░░ Process Profile ░░  |
   | Level 4 (L4)|  |  각 프로세스별 능력등급을 점수표로 시각화|
   | Quant.Mng   |  |                                         |
   | Level 3 (L3)|  |  Automotive SPICE:                     |
   | Defined     |  |  SWE.1~6 + MAN.3 + SUP.1~10 = 31프로세스|
   | Level 2 (L2)|  +-----------------------------------------+
   | Managed     |
   | Level 1 (L1)|      ※ ASPICE v3.1 기준 프로세스 카탈로그
   | Performed   |         V-model 기반 31개 프로세스
   | Level 0 (L0)|
   | Incomplete  |
   +-------------+
```

### 2.2 프로세스 차원(Process Dimension) — Process Reference Model (PRM)

ISO/IEC 33002(구 15504-2)는 **5개 카테고리·46개 프로세스**를 정의한다.

| 카테고리 | 코드 | 프로세스 수 | 주요 프로세스 예시 |
| :--- | :--- | :--- | :--- |
| **Customer-Supplier** | CUS | 6 | CUS.1~6 (요구정의, 계약, 인수, 공급) |
| **Engineering** | ENG | 10 | ENG.1~10 (SW요구/설계/구현/테스트/통합 등) |
| **Supporting** | SUP | 9 | SUP.1~9 (문서화, 형상관리, QA, 검증, 확인 등) |
| **Management** | MAN | 9 | MAN.1~9 (프로젝트/품질/리스크/측정/포트폴리오) |
| **Organizational** | ORG | 12 | ORG.1~12 (프로세스배포, 측정, 혁신, 인력 등) |
| **합계** | - | **46개** | Automotive SPICE PAM v3.1은 31개로 축약 |

### 2.3 능력 차원(Capability Dimension) — 5단계 능력수준

```text
[능력수준 5단계 구조와 9개 프로세스속성(PA) 매핑]

   Level 5: Optimizing  -+- PA 5.1 Process Innovation
      |                  +- PA 5.2 Continuous Optimization
      |
   Level 4: Quantitatively Managed -+- PA 4.1 Process Measurement
      |                              +- PA 4.2 Process Control
      |
   Level 3: Defined  -+- PA 3.1 Process Definition
      |               +- PA 3.2 Process Deployment
      |
   Level 2: Managed  -+- PA 2.1 Performance Management
      |               +- PA 2.2 Work Product Management
      |
   Level 1: Performed -+- PA 1.1 Process Performance
      |
   Level 0: Incomplete
      +- (PA 미달성: 프로세스 목적 달성 못함)
```

**핵심 규칙**: 능력수준 L_k가 달성되었다고 판단하려면 L_k의 **모든 프로세스속성(PA)이 100% 달성(Largely Attained 이상)**되어야 한다. 부분 달성 시 능력수준은 한 단계 하락한다.

### 2.4 프로세스속성(PA) 구성요소 — Process Assessment Model (PAM)

각 PA는 다음 요소로 구성되며, ISO/IEC 33003(구 15504-3)에 상세히 정의된다.

| 구성요소 | 약어 | 역할 | 평가 시 활용 |
| :--- | :--- | :--- | :--- |
| **Base Practice** | BP | PA의 핵심 실천항목(예: PA 2.1의 BP 1: 프로세스 수행목표 정의) | 증거수집 체크리스트 |
| **Generic Practice** | GP | 능력수준별 보편적 실천항목 | 평가 척도 |
| **Work Product** | WP | BP 수행 결과물(문서, 기록, 도구 산출물) | 증거(Evidence) |
| **Generic Resource** | GR | BP 수행에 필요한 자원(인력, 도구, 환경) | 증거(Evidence) |
| **Practice Indicator** | PI | BP/GP의 달성 증거 | 평가자 판단 근거 |

### 2.5 평가 척도(Assessment Indicator Rating Scale)

각 PA 또는 BP는 다음 4단계 척도로 평가된다:

```text
[N: Not achieved (0~15%)]   -+
[P: Partially achieved (15~50%)] -+- "L" 미달성 -> 능력수준 미달
[L: Largely achieved (50~85%)]  -+
[F: Fully achieved (85~100%)]   -+  ※ ISO/IEC 33020:2019 기준
```

**합격 기준**: 능력수준 L_k 부여는 **모든 PA가 "L" 이상**이어야 한다(Fully 달성은 아니어도 Largely면 됨).

### 2.6 평가 수행 절차(Assessment Process)

```text
[ISO/IEC 15504 평가 5단계 절차]

  +--------------------------------------------------------+
  | 1. 신탁/사전 준비(Initiation & Planning)                |
  |    - 평가 범위(Scope) 정의: 조직단위/프로젝트단위        |
  |    - 평가 대상 프로세스 선정                             |
  |    - 평가팀(Assessor) 자격 검증: 최소 2인 이상         |
  |    - 평가 모델(Reference Model + Indicator) 확정        |
  +-----------------+--------------------------------------+
                    v
  +--------------------------------------------------------+
  | 2. 데이터 수집(Data Collection)                          |
  |    - 문서 검토(Document Review): QMS 문서, SOP, 지표   |
  |    - 인터뷰(Interview): 실무자·관리자·경영진             |
  |    - 관찰(Observation): 워크샵, 데일리 미팅 참관        |
  |    - 도구 산출물(Artifact): Jira, Git, CI/CD 로그       |
  +-----------------+--------------------------------------+
                    v
  +--------------------------------------------------------+
  | 3. 데이터 검증(Data Validation)                          |
  |    - 다중 증거 교차검증(Triangulation)                   |
  |    - 모순(Contradiction) 해소                            |
  |    - 평가자 합의(Consensus) 도출                         |
  +-----------------+--------------------------------------+
                    v
  +--------------------------------------------------------+
  | 4. 프로세스 속성 등급 부여(Process Attribute Rating)   |
  |    - 각 PA별 N/P/L/F 부여                               |
  |    - Base Practice 별 등급 산출                          |
  |    - 능력수준(Capability Level) 결정                     |
  +-----------------+--------------------------------------+
                    v
  +--------------------------------------------------------+
  | 5. 결과 보고(Reporting)                                  |
  |    - 프로세스 프로파일(Process Profile) 산출             |
  |    - 강점/약점/리스크 식별                                |
  |    - 개선 권고(Recommendation) 도출                      |
  |    - 등록(Register) 및 인증 여부 결정                    |
  +--------------------------------------------------------+
```

### 2.7 결과물: 프로세스 프로파일(Process Profile)

평가 결과는 **방사형 그래프(Radar Chart)** 또는 **막대 그래프**로 표현되어 발주자가 공급자의 능력을 한눈에 비교할 수 있다.

```text
[Automotive SPICE PAM v3.1 평가 결과 예시 - Process Profile]

  Capability Level
   5 |         ★(강점)
   4 |                ★
   3 |  ★        ★
   2 |        ★           ★        ★     (대부분)
   1 |
   0 |
     +----------------------------------------------
     ENG.1  ENG.2  ENG.3  MAN.3  SUP.1  SUP.4  ...
     SWReq  SWDes  SWImp  ProjMg QA     ConfigMng

  ⇒ 발주자 요구: 전체 프로세스 CL=2 이상, ENG/SUP 16개 중 12개는 CL=3 이상
  ⇒ 본 조직: ENG.1, ENG.2, MAN.3가 CL=3, 나머지 CL=2 -> 부분 충족 -> 개선 권고
```

- **📢 섹션 요약 비유**: 능력수준 5단계는 마치 **요리사 등급**과 같다. L1=요리 가능, L2=레시피 관리, L3=표준 레시피 배포, L4=정밀 계량·온도 측정, L5=지속적 신메뉴 개발.

---

## Ⅲ. 비교 및 연결

### 3.1 ISO 15504 vs CMMI-DEV 비교

| 구분 | ISO/IEC 15504 (SPICE) | CMMI-DEV v1.3 / v2.0 |
| :--- | :--- | :--- |
| **정립 시기** | 1993(SPICE)->2003(IS)->2015(330xx) | 1993(SEI)->2002(v1.1)->2010(v1.3)->2018(v2.0) |
| **평가 단위** | **프로세스 단위**(46개, 자유선택) | **프로세스 영역(PA) 단위**(22개, 통합묶음) |
| **능력 vs 성숙도** | **Capability Level**(프로세스별) | **Maturity Level**(조직 전체 5단계) |
| **유연성** | 높음(원하는 프로세스만 평가) | 낮음(ML 달성을 위해 다수 PA 필요) |
| **결과 활용** | 공급망 다차원 비교, 프로젝트 단위 | 조직 전체 성숙도 진단, 1~2년 주기 |
| **산업 적용** | 자동차(ASPICE), 의료, 항공, 국방 | 미국 DoD, SW 조직 일반 |
| **가중치 부여** | 가능(WP의 중요도 가중) | CMMI v2.0에서 단계별 가중치 도입 |
| **인증/등록** | ISO 15504 등록(공인 등록기관) | CMMI Institute 인증(SVC) |
| **상호운용** | CMMI-DEV와 약 70% 매핑 가능(SEI 매핑 보고서) | ISO 15504 PAM과 매핑 가능 |
| **비용** | 평가팀 인건비 + 등록비 | 평가비 + 출장비 + SVC 수수료 |

### 3.2 Automotive SPICE(ASPICE) v3.1 특징

- **31개 프로세스**:
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 511 / 600

<- **이전**: [510. CMMI 프로세스 성숙도 모델](/knowledge-base/studynote/11_design_supervision/06_exam_summary/511_cmmi_process_maturity_model/)
**다음**: [512. PSP TSP 개인 팀 소프트웨어 프로세스](/knowledge-base/studynote/11_design_supervision/06_exam_summary/512_psp_tsp_personal_team_software_process/) ->

---
