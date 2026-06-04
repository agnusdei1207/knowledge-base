---
title: "516. 위험 관리 프레임워크 리스크 평가 (Risk Management Framework Assessment)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


# 516. 위험 관리 프레임워크 리스크 평가 (RMF Risk Assessment)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NIST SP 800-37 Rev.2의 7단계 사이클(Prepare -> Categorize -> Select -> Implement -> Assess -> Authorize -> Monitor)에서 **Step 4(Assess)** 와 **Step 6(Monitor)** 의 핵심 절차로, SP 800-53A Rev.5가 정의한 **Examine(검토) / Interview(인터뷰) / Test(시험)** 3대 검증 기법과 SP 800-30 Rev.1의 **위험 결정 알고리즘(Threat × Likelihood × Impact)** 을 결합하여, 약 1,000여 개의 보안·프라이버시 통제 항목의 구현 적합성과 운영 효과성을 객관적 증거(CVE, SCAP 결과, 로그, 정책 문서) 로 정량 측정하는 **Risk Determination 및 Authorization Decision 지원 프로세스**이다.
> 2. **가치**: FISMA/FedRAMP/DoD RMF/CMMC/ISO 27001 등 다중 컴플라이언스 환경에서 **평가 결과의 상호 인용(Reciprocity)** 을 통해 한 번의 평가로 70~80% 의 중복 감사 비용을 절감하며, POA&M(Plan of Action & Milestones) 기반의 위험 기반 의사결정으로 **연간 취약점 노출 시간(MEAN TIME TO REMEDIATE, MTTR)** 을 평균 40~60% 단축시킨다.
> 3. **판단 포인트**: **통제 상속(Inheritance)** 및 **공통 통제(Common Controls)** 의 활용도 결정, **eMASS·Xacta·CSAM** 등 GRC 도구의 자동화 범위 설정, **침투 테스트(Red Team / Purple Team)** 와 문서·인터뷰 기반 평가 간의 가중치 균형, 그리고 잔여 위험(Residual Risk)에 대한 **인가 담당 임원(AO)** 의 위험 수용(Risk Acceptance) 의사결정 프레임워크 설계가 핵심 Trade-off 이다.

---

## Ⅰ. 개요 및 필요성

NIST Risk Management Framework(RMF)는 미국 연방정부의 FISMA(Federal Information Security Modernization Act of 2014) 이행 및 국방부 정보 시스템 인증·인가(Authorization) 절차의 표준 토대로, 2010년 SP 800-37 Rev.1(6단계)에서 2018년 SP 800-37 Rev.2(7단계)로 발전하면서 **Prepare 단계**가 신설되어 조직 차원의 위험 관리 거버넌스가 강화되었다. 특히 **Assessment 단계(Step 4)** 는 단순한 "감사(audit)" 가 아니라, 시스템의 보안 태세(Security Posture)에 대한 **정량적 증거 수집과 위험 결정(Risk Determination)** 을 통해 ATO(Authorization To Operate) 발급을 기술적으로 정당화하는 핵심 단계이다.

기존 C&A(Certification & Accreditation) 패러다임은 "3년 주기 재인증" 방식의 정적이고 스냅샷(Snapshot) 중심 평가였으나, RMF Rev.2 및 SP 800-137의 **ISCM(Information Security Continuous Monitoring)** 패러다임은 **"Assess Once, Reuse Many Times"** 와 **"Continuous -> Ongoing Authorization"** 으로 전환되어, **NIST SP 800-53A Rev.5** 가 정의한 **Assessment Object(명세·메커니즘·활동·개인·그룹)** 단위로 평가 객체를 표준화하고, SP 800-30 Rev.1의 **Tolerable Risk / Moderate Risk / High Risk** 3단계 등급 체계를 통해 비즈니스 영향도(BIA)와 연계한 위험 기반 의사결정을 가능하게 한다.

또한 2020년 SP 800-53 Rev.5에서 **20개 통제 패밀리(AC, AT, AU, CM, IA, IR, MA, MP, PE, PL, PM, PS, PT, RA, SA, SC, SI, SR, PM, SI)** 가 17개 -> 20개로 확장되고 **Privacy Controls(Appendix J -> 본편 통합)** 와 **Supply Chain Risk Management(SR 패밀리)** 가 추가되면서, 평가 대상 통제가 기존 ~450개에서 약 **1,000여 개(Base + Tailoring)** 로 증가하여 **자동화 도구(SCAP, eMASS, Nessus, Qualys)** 와의 통합이 필수적 요소가 되었다.

```text
[ NIST RMF 7-Step Lifecycle & Assessment Integration ]

     +--------------------------------------------------------------+
     |  Step 0 |  Step 1   |  Step 2  |  Step 3  | ★Step 4★  | Step 5 | Step 6 |
     | PREPARE | CATEGORIZE|  SELECT  |IMPLEMENT |  ASSESS    |AUTHORIZE| MONITOR |
     |         | (FIPS199) |(800-53b) | (구축)   |(800-53A)  |(ATO)    |(800-137)|
     +----+----+-----+------+----+-----+----+-----+-----+------+----+----+----+----+
          |          |           |          |           |           |         |
          v          v           v          v           v           v         v
       조직/시스템| H/M/L      |  Baseline |  SSP      | SAP/SAR   | ATO      | ISCM
       위험전략  |  영향도    |  Tailoring|  구현 증빙|  POA&M     | 결정     | 재평가
       설정      | 분류      |  결정     |  수집     | 위험 결정  | 발급     | 자동화
                  |           |           |           |           |         |
                  +-----------+-----------+-----------+-----► 재사용 ◄------+
                                              (Reciprocity & Inheritance)
```

```text
[ Step 4 Assess 핵심 절차 흐름 ]

   +----------------+   +----------------+   +----------------+
   | 1. SAP 작성    |--->| 2. Assessor    |--->| 3. 3-E 평가    |
   |  (Security     |   |  선정 및       |   |  Examine       |
   |  Assessment    |   |  독립성 확보   |   |  Interview     |
   |  Plan)         |   |  (Conflict of |   |  Test          |
   |                |   |   Interest)    |   |                |
   +----------------+   +----------------+   +-------+--------+
                                                       |
                                                       v
   +----------------+   +----------------+   +----------------+
   | 6. POA&M 작성  |<---| 5. 위험 결정   |<---| 4. SAR 작성    |
   |  완화 계획     |   |  Risk Determ.  |   |  Security      |
   |  (Milestone    |   |  (800-30 Rev.1)|   |  Assessment    |
   |   + Resources) |   |  Threat×Like×  |   |  Report        |
   |                |   |  Impact        |   |                |
   +----------------+   +----------------+   +----------------+
```

**📢 섹션 요약 비유**: RMF 평가 프로세스는 **항공기 인증(airworthiness certification)** 과 같다. 항공기 한 대가 비행에 적합한지(ATO) 판단하기 위해 정비사(Assessor)가 설계 도면·정비 기록·시험 비행 데이터를 면밀히 검토(Examine)하고, 조종사·정비사 인터뷰(Interview) 후, 풍동 시험·엔진 시동 시험(Test)을 통해 다층적 증거를 확보하여 항행 안전 증명서(Airworthiness Certificate)를 발급하는 일련의 과정과 정확히 같은 구조이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

RMF Risk Assessment 의 핵심은 **SP 800-53A Rev.5** 가 정의한 **평가 절차(Assessment Procedure)** 의 5개 필드 구조와 **SP 800-30 Rev.1** 의 위험 결정 알고리즘, 그리고 **SP 800-137** 의 ISCM 자동화 아키텍처의 3대 축으로 구성된다.

```text
[ SP 800-53A Assessment Procedure 구조 (5-Field Format) ]

   +--------------------------------------------------------------+
   | AC-2(1)  ACCOUNT MANAGEMENT | Identifier | Automated        |
   +--------------------------------------------------------------+
   | (1) 객체: SP-구성요소, 정책문서                                |
   | (2) 속성: 정확성, 완전성, 일관성, 유효성                       |
   | (3) 방법:  E=Examine  I=Interview  T=Test                    |
   | (4) 조치: -DETERMINE / -VERIFY / -CONFIRM                    |
   | (5) 증거:  정책 PDF, 인터뷰 노트, AD 스크립트 결과            |
   +--------------------------------------------------------------+

   v 평가 결과 산출 v

   +--------------------------------------------------------------+
   |  Finding Code  |  Meaning         |  Required Action         |
   +----------------+------------------+--------------------------+
   |  Satisfied (S) |  적합            |  -                       |
   |  Other Than    |  부분 적합       |  POA&M 또는 Risk-Based   |
   |  Satisfied(O)  |  (보완 필요)     |  Decision                |
   |  Not Satisfied|  부적합          |  즉시 시정 + Risk Accept |
   |  Not Applicable|  적용 제외       |  Tailoring 근거 명시     |
   +--------------------------------------------------------------+
```

### SP 800-30 Rev.1 위험 결정 알고리즘 (Risk Determination)

위험 등급은 단순 합산이 아니라 **Threat × Likelihood × Impact** 의 3축 벡터 곱(Semi-quantitative 곱셈 매트릭스) 으로 산출된다.

```
Risk = f(Threat, Vulnerability, Likelihood, Impact, Predisposing Conditions)
                                                    |
        +-------------------------------------------+
        v
   +---------------------------------------------------------+
   |   Likelihood    |  Low(1)  Med(2)   High(3)  VeryHigh(5)|
   +-----------------+-----------------------------------------+

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 516 / 600

<- **이전**: [515. COSMIC 기능 크기 측정](/studynote/11_design_supervision/06_exam_summary/516_cosmic_functional_size_measurement/)
**다음**: [517. PMBOK 프로젝트 관리 지식 체계](/studynote/11_design_supervision/06_exam_summary/517_pmbok_project_management_body_of_knowled/) ->

---
