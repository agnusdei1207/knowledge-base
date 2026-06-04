---
title: "795. IT 경영 관리 핵심 토픽 795번 시험 요약 (IT Management Core Topic 795 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


```markdown
# 795. IT 거버넌스(Governance)와 COBIT 2019 — 정보관리기술사 핵심 토픽

> 본 노트는 정보관리기술사·컴퓨터시스템응용기술사 출제 빈도 최상위 토픽인 **"IT 거버넌스 및 COBIT 2019"**를 795번 시리즈의 핵심 정리로 재구성한 것이다.

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019는 **6개 거버넌스 원칙**, **5개 거버넌스 시스템 구성요소**, **40개 관리목표(Governance/Management Objectives)**를 통해 엔터프라이즈 IT를 **Value Creation(가치창출)** 관점으로 통합 운영하는 ISACA의 글로벌 거버넌스 프레임워크이다.
> 2. **가치**: ISACA 자체 통계상 COBIT 도입 조직은 **IT-Business 미스매치 40%v, 프로젝트 실패율 30%v, 컴플라이언스 비용 25%v** 효과를 보고하며, 11개 **Design Factor** 기반의 맞춤형 거버넌스 시스템 설계로 동일 프레임워크를 다업종·다규모에 적용 가능하다.
> 3. **판단 포인트**: 핵심 의사결정축은 ① **Design Factor 가중치**(예: Risk Profile vs Innovation Profile), ② **Focus Area 선택**(예: DevOps, Cybersecurity, Data Governance), ③ **Agile 운영 모델 채택 여부**, ④ **거버넌스 vs 관리(Governance/Management) 분리 수준**, ⑤ **레거시 ISO 38500·ITIL 4·TOGAF와의 통합(interoperation) 전략**이다.

---

## Ⅰ. 개요 및 필요성

### 1. 시대적 배경 — IT-Business Alignment의 위기
- 2020년대 들어 **클라우드·AI·데이터 거버넌스** 이슈가 폭증하면서 CIO의 **"IT가 비즈니스 가치를 어디서 만드는가"**에 대한 정량적 입증이 필수가 됨
- 단순 ITIL(서비스 운영)·ISO 27001(보안)만으로는 **End-to-End 가치사슬(Value Chain)** 관리가 불가능 -> 상위 거버넌스 레이어 필요
- COVID-19 이후 **원격근무·제로트러스트·SaaS 다중화** 환경에서 **IT 리스크의 가시화(Visibility)**와 **이사회 보고 체계(Board-level Reporting)** 요구 급증

### 2. COBIT 5 -> 2019 진화의 핵심 변화
| 항목 | COBIT 5 (2012) | COBIT 2019 (2018~) |
| :--- | :--- | :--- |
| 원칙 | 5개 원칙(고정) | **6개 원칙 + Open Customization** |
| 프로세스 | 37개 프로세스(Enabler 기반) | **40개 관리목표(목표 중심)** |
| 설계 변수 | Cascade of Goals | **11 Design Factor + Focus Area** |
| 거버넌스/관리 분리 | Enabler 7개로 통합 기술 | **5개 Gov System + 7개 Mgmt Component** 명시 분리 |
| 프레임워크 연계 | 별도 매핑 가이드 | **CMMI, ITIL 4, ISO 27001, TOGAF, NIST CSF** 네이티브 매핑 제공 |
| 도입 난이도 | High(One-Size-Fits-All) | **Tunable(맞춤형 설계)** |

```text
        [ COBIT 2019 도입의 필요성 — 3-Layer 정렬 모델 ]
   +------------------------------------------------------+
   |           Enterprise Strategy & Governance           |  <- Board / CEO
   |     (이사회 KPI, BSC, ESG, Risk Appetite)             |
   +------------------------+-----------------------------+
                            |   Alignment Gap(거버넌스 부재 시)
                            v
   +------------------------------------------------------+
   |       IT Strategy & Portfolio Management            |  <- CIO / CDO
   |  (Demand Mgmt, Benefit Realization, Risk Profile)    |
   +------------------------+-----------------------------+
                            |
                            v
   +------------------------------------------------------+
   |   Service Delivery & Operation (ITIL4 / DevOps)      |  <- COO / CISO
   |  (Incident, Change, SRE, Zero Trust Architecture)    |
   +------------------------------------------------------+
            ^
            |  ※ 3 Layer가 끊어지면 IT 투자가 "비용"이 되고,
            |     COBIT 2019는 이 3 Layer의 "이음새"를 표준화한다.
```

### 3. 왜 COBIT 2019인가 — 4대 Pain Point 해결
1. **Shadow IT 가시화**: SaaS 스프레드시트(보안사고 70% 원인) 추적
2. **이중 프레임워크 부담**: ISO 27001 + ITIL + NIST 중복 통제 통합
3. **규제 대응(컴플라이언스)**: GDPR·개인정보보호법·ESG 공시 -> **단일 거버넌스 대시보드** 요구
4. **Agile/DevOps 시대**: 폭포수(Waterfall) 시대의 프로세스 모델을 **반복적(Iterative)** 거버넌스로 전환

- **📢 섹션 요약 비유**: IT 거버넌스 없는 조직은 **교향곡 단원에게 악보 없이 연주하라고 하는 것**과 같다. COBIT 2019는 "지휘자(Governance) + 악보(Framework) + 파트별 세션(Management Objective)"이 모두 갖춰진 **풀 오케스트라 악보**다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. COBIT 2019 3대 기둥(Three Pillars)

```text
   +--------------------------------------------------------------+
   |                 COBIT 2019 CORE MODEL 구조                   |
   +--------------------------------------------------------------+
   |                                                              |
   |  +----------------------+    +----------------------+        |
   |  |  6 Principles        |    |  40 Governance &     |        |
   |  |  (Governance System) |    |  Management          |        |
   |  |                      |    |  Objectives          |        |
   |  |  P1. Stakeholder     |---->|  EDM(05) + APO(14)   |        |
   |  |      Value           |    |  + BAI(11) + DSS(06) |        |
   |  |  P2. Holistic        |    |  + MEA(04)           |        |
   |  |      Approach        |    |  = 40개 목표         |        |
   |  |  P3. Dynamic          |    +----------+-----------+        |
   |  |      Governance Sys. |               |                    |
   |  |  P4. Governance       |               v                    |
   |  |      Distinct from   |    +----------------------+        |
   |  |      Management      |    |  5 Components of     |        |
   |  |  P5. Tailored to     |    |  Governance System   |        |
   |  |      Enterprise Need |    |  (원리 실현 장치)     |        |
   |  |  P6. End-to-End      |    |  C1~C5               |        |
   |  |      Governance      |    +----------------------+        |
   |  +----------+-----------+                                    |
   |             |                                                |
   |             v                                                |
   |  +--------------------------------------------------+        |
   |  |  11 Design Factors  ->  Focus Area  ->  Customized |        |
   |  |  (맞춤형 거버넌스 시스템 설계)                    |        |
   |  +--------------------------------------------------+        |
   +--------------------------------------------------------------+
```

### 2. 6 Principles of the Governance System (거버넌스 시스템 6원칙)

| 번호 | 원칙 | 핵심 의미 | 실무 적용 |
| :---: | :--- | :--- | :--- |
| **P1** | **Stakeholder Value(이해관계자 가치)** | Benefit Realization·Risk Optimization·Resource Optimization의 **3-Point Value Balancing** | BSC 4관점(Financial/Customer/Internal/Learning) 매핑 |
| **P2** | **Holistic Approach(총체적 접근)** | 거버넌스는 단일 부서가 아닌 **Enterprise 전체 시스템** | CISO·CIO·CDO·CFO·CRO 합동 거버넌스 위원회 |
| **P3** | **Dynamic Governance System(동적 거버넌스)** | 외부 환경 변화에 따라 **연속적 갱신** | 디자인 팩터 재평가 주기(연 1회 이상) |
| **P4** | **Governance Distinct from Management(거버넌스의 관리 분리)** | **Evaluate(E), Direct(D), Monitor(M)** = 거버넌스 / **Plan(P), Build(B), Run(R), Monitor(M)** = 관리 | EDM 도메인 5개 목표가 핵심 분리선 |
| **P5** | **Tailored to Enterprise Needs(기업 맞춤)** | One-Size-Fits-All 거부, 11 Design Factor로 조정 | 자체 거버넌스 시스템 빌더(Online Tool) 사용 |
| **P6** | **End-to-End Governance(전 구간 거버넌스)** | Strategy -> Portfolio -> Project -> Operation -> Value Realization의 End-to-End 커버 | **Value Office(가치관리실)** 신설 권장 |

### 3. 5 Components of a Governance System (거버넌스 시스템 5대 구성요소)

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **C1. Process(프로세스)** | 실무 운영 절차 | **40개 관리목표별 Practice(상위/하위)** 정의, **RACI 차
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 795 / 800

<- **이전**: [794. IT 경영 관리 핵심 토픽 794번 시험 요약](/studynote/12_it_management/05_security_compliance/794_it_management_core_topic_794_exam_summary/)
**다음**: [796. IT 경영 관리 핵심 토픽 796번 시험 요약](/studynote/12_it_management/05_security_compliance/796_it_management_core_topic_796_exam_summary/) ->

---
