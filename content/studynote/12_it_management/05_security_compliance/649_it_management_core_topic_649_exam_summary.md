---
title: "649. IT 경영 관리 핵심 토픽 649번 시험 요약 (IT Management Core Topic 649 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리(Technology Governance)는 **COBIT 2019**(제어·측정), **ITIL 4**(서비스 가치 사슬), **PMBOK 7th**(프로젝트 거버넌스), **TOGAF/Zachman EA**(아키텍처 정렬)를 통합하여 **비즈니스 전략 ↔ IT 투자 ↔ 운영 성과**의 3축 피드백 루프를 구축하는 경영 체계이다.
> 2. **가치**: McKinsey(2023) 보고에 따르면 디지털 전환(DX) 성숙도 상위 25% 기업은 EBITDA 마진이 **5.4%p**, 매출 성장률이 **2.7배** 높으며, COBIT 기반 거버넌스 도입 시 **IT 예산 대비 ROI가 평균 23%** 개선된다.
> 3. **판단 포인트**: 핵심 의사결정 트레이드오프는 ① **표준 프레임워크 채택 vs. 자체 거버넌스 모델**(ISO 38500·COBIT 매핑 강도) ② **중앙 집중(CoE) vs. 분산형 거버넌스**(Federated) ③ **정량 KPI 우선(BSC·CSF) vs. 정성 거버넌스 원칙**이며, 기술사 답안에서는 **"통제-유연성(Control-Flexibility) 균형"**과 **"성숙도 단계별 점진 적용(Staged Rollout)"** 관점을 명시해야 한다.

---

## Ⅰ. 개요 및 필요성

IT 경영 관리(Information Technology Management, 이하 IT-Mgmt)는 단순한 "IT 부서 운영"이 아니라, **전사적 차원에서 IT 자원을 전략·조직·프로세스·기술 4가지 관점으로 통제·가치화**하는 경영 과학이다. 한국 정보시스템감사 통제기준(전자금융거래법 제21조, 개인정보보호법 제29조)과 ISO 38500(2015 개정) 모두 "IT에 대한 의사결정, 책임, 평가의 프레임워크"를 사업주·이사회 차원에서 요구하고 있다.

**기술적 배경과挑战**:
- 2010년대 이후 **클라우드(AWS·Azure·GCP), AI/ML, IoT, 블록체인**이 보편화되며 IT 자원의 **경계가 흐려지고(Boundaryless IT)**, SaaS·PaaS·IaaS 다중 벤더 환경에서 통제 범위 정의가 핵심 이슈로 부상
- **NIS2(유럽, 2024)**, **개인정보보호법 개정(2023, 가명정보 도입)**, **AI 기본법(2025 제정 추진)** 등 컴플라이언스 요구사항이 폭증하여, **GRC(Governance-Risk-Compliance) 통합 플랫폼**이 필수
- **생성형 AI(GenAI)** 도입으로 Shadow IT가 LLM API 키·SaaS Copilot 단위로 분산화 -> 중앙 가시성(Visibility) 확보가 기술사 논점

**Old vs New Paradigm 비교**:
| 구분 | 구(Old) 패러다임 | 신(New) 패러다임 |
|---|---|---|
| **관점** | IT는 비용(Cost Center) | IT는 가치 창출(Value Driver) |
| **구조** | 수직 사일로(Dev-Ops-Biz 분리) | DevSecOps + Platform Engineering + SRE |
| **측정** | 가동률·장애건수 | DORA(배포빈도·변경리드타임·MTTR·변경실패율) + 비즈니스 KPI |
| **거버넌스** | 사후 통제(After-the-fact) | 지속적 인증(Continuous Assurance, e.g., SOC 2 Type II) |
| **계약** | 일괄 라이선스(CAPL) | FinOps 기반 사용량 과금 + FinOps Foundation |

```text
[IT 경영 관리 4P 통합 프레임워크 (Governance 4P Model)]

                    +----------------------------------+
                    |   Board / CEO / 이사회 거버넌스     |
                    |   (전략 의사결정·책무성·리스크)     |
                    +--------------+-------------------+
                                   | 위임
                    +--------------v-------------------+
                    |   IT Steering Committee (ISC)     |
                    |   - CIO / CDO / CFO / CISO       |
                    +--------------+-------------------+
                                   | 통제
        +--------------------------+--------------------------+
        |                          |                          |
+-------v--------+         +-------v--------+         +-------v--------+
| 1. Portfolio   |         | 2. Program     |         | 3. Project     |
|    Management  |         |    Management  |         |    Management  |
|  (투자 포트폴리오)|         |   (프로그램)   |         |   (PMBOK/Agile)|
+-------+--------+         +-------+--------+         +-------+--------+
        |                          |                          |
        +--------------------------+--------------------------+
                                   | 성과·가치
                    +--------------v-------------------+
                    | 4. Performance & Value Mgmt      |
                    |   BSC / OKR / FinOps / VRIO      |
                    +--------------+-------------------+
                                   | 보고
                    +--------------v-------------------+
                    |  Continuous Monitoring & Audit   |
                    |  (ISO 38500 · COBIT · 내부감사)  |
                    +----------------------------------+
```

**왜 필요한가?**: "We have 47 different SaaS subscriptions and no one knows who pays for what" — Forbes(2024)에 따르면 **대기업의 평균 SaaS 낭비가 30%**에 달하며, 이는 **FinOps + ITAM(IT Asset Management) + 거버넌스 위원회** 부재의 직접적 결과이다.

- **📢 섹션 요약 비유**: IT 경영 관리는 **대형 호텔의 총괄 매니저**와 같다. 프런트(서비스·고객), 주방(개발·운영), 구매(조달·계약), 회계(예산·감사) 부서를 동시에 보되, 단일 손님(사업부·고객)에게 일관된 경험(서비스·보안·품질)을 제공하도록 시스템을 통합하는 역할이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영 관리의 4대 핵심 표준은 **상호 보완적 관계**를 가지며, 각각 **전략-전술-운영-측정**의 다른 추상화 레벨을 담당한다.

```text
[IT 거버넌스 표준 프레임워크 매핑 - 계층적 통합 구조]

   추상화 레벨            표준 프레임워크              적용 대상
   -------------------------------------------------------------
   ① 전략 (Strategy)      ISO 38500 (2015)           이사회·경영진
        |                  COBIT 2019 EDM (Evaluate, Direct, Monitor)
        |                  Zachman / TOGAF 10         EA 아키텍처
        v
   ② 전술 (Tactical)      COBIT 2019 (전체 40 Governance/Management Obj.)
        |                  ITIL 4 Service Value System
        |                  PMBOK 7th (8 Performance Domains)
        v
   ③ 운영 (Operational)   ITIL 4 Practices (34개)    서비스 데스크·운영팀
        |                  DevOps/DevSecOps 파이프라인
        |                  ISO 27001 (ISMS) / NIST CSF
        v
   ④ 측정 (Measurement)   COBIT 2019 Cascade (Goals -> Process -> Metrics)
                          Balanced Scorecard (BSC)
                          DORA / SPACE / OKR
   -------------------------------------------------------------

   [연계 메커니즘: COBIT Cascade]
   Stakeholder Needs -> Enterprise Goals -> Alignment Goals ->
       -> Governance/Management Objectives -> Process Activities ->
           -> Process Capability (CMMI 0-5 or PAM ISO 15504)
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **COBIT 2019** (Control Objectives for Information and Related Technologies) | **전사 IT 거버넌스·관리**의 40개 목표(EDM 5 + APO 14 + BAI 11 + DSS 6 + MEA 4) 제공 | **EDM 사이클**: Evaluate(현황 평가) -> Direct(방향·정책 수립) -> Monitor(성과 측정). 설계 팩터 11개(전략·목표·위험·역할·문제·문화·역량 등)로 **커스터마이즈된 거버넌스 시스템** 설계. PAM(Process Assessment Model)으로 **프로세스 성숙도 0~5 척도 측정** |
| **ITIL 4** (Information Technology Infrastructure Library) | **서비스 가치 사슬(SVC, Service Value Chain)** 중심의 운영 우수성 프레임워크 | **34개 Practice**(변경관리·인시던트·문제·릴리스 등) + **7개 guiding principle**(Focus on value, Start where you are, Progress iteratively, etc.). **Four Dimensions Model**: 조직·사람·정보·기술·공급자·가치사슬(Products 포함) |
| **PMBOK 7th** (Project Management Body of Knowledge, PMI) | 프로젝트 거버넌스의 8개 **Performance Domain** | **8 Domains**: Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty. **12 Principle of Project Management** + Tailoring 가이드 |
| **TOGAF 10 / Zachman** (Enterprise Architecture) | **비즈니스-데이터-애플리케이션-기술** 4계층 아키텍처 정렬 | **ADM(Architecture Development Method)**: Preliminary->A(비즈니스)->B/D(데이터)->C(애플리케이션)->D(기술)->E,F,G 구현·마이그레이션. **EA Repository**(ArchiMate 3.2 모델링 언어) |
| **Balanced Scorecard (BSC)** | **재무·고객·내부프로세스·학습성장** 4관점 KPI | **Strategy Map**(인과관계 다이어그램) + **CSF/KPI/PPI 3단 계층**. 예: ITSM 운영에서 "평균복구시간(MTTR)" -> "서비스 가용성" -> "고객만족도(CSAT)" -> "매출 유지율" |
| **DORA Metrics** | DevOps 성과 4대 지표 | **배포빈도(DF)** · **변경리드타임(MLT)** · **평균복구시간(MTTR)** · **변경실패율(CFR)**. Elite: 1일 1배포+ MLT<1일+ MTTR<1시간+ CFR 0-15% |
| **FinOps Foundation** | 클라우드 비용 거버넌스 | **Inform->Optimize->Operate** 3단계. **TBM(Tech Business Management)** taxonomy + Showback/Chargeback 모델. **Reserved Instance/ Savings Plan** 최적화 |
| **ISO 38500 (2015)** | **이사회·경영진**의 IT 거버넌스 6원칙 | **6 Principle**: Responsibility, Strategy, Acquisition, Performance, Conformance, Human Behavior. **Governance Model**: Direct(지시) -> Evaluate(평가) -> Monitor(모니터) |

**핵심 메커니즘: COBIT Cascade + Capability Level**
1. **이해관계자 니즈 식별**: 13개 Enterprise Goal 중 관련 목표 선정 (예: "AG01: IT 준수 및 지원", "AG04: 위험 관리")
2. **Alignment Goal 매핑**: Enterprise Goal -> Alignment Goal (예: AG01 -> "EDM01: 거버넌스 프레임워크 설정")
3. **Management Process 도출**: Alignment Goal -> Process (예: EDM01 -> EDM01.01 "비즈니스 원칙 준수 평가")
4. **Capability 평가**: PAM(Process Assessment Model, ISO/IEC 33020 기반) 6레벨(0:불완전~5:최적화) 측정
5. **KPI 연결**: RACI Matrix + Process Goal Metric (예: EDM01 -> "% of governance issues resolved within agreed timeframe ≥ 95%")

**거버넌스 운영 주기**: 일반적으로 **Quarterly IT Steering Committee + Monthly Operational Review + Annual Independent Audit**의 3단 리듬을 사용한다.

- **📢 섹션 요약 비유**: COBIT는 **"건축법"**(설계도·규격), ITIL은 **"건물 운영 매뉴얼"**(실제 서비스 절차), PMBOK은 **"건축 공사 관리법"**(프로젝트 일정·품질·리스크), TOGAF는 **"도시계획도"**(전체 부지 배치)다. 좋은 도시는 4가지가 모두 정렬되어야 한다.

---

## Ⅲ. 비교 및 연결

IT 경영 관리 표준들은 **경쟁 관계가 아니라 상호 보완적**이며, 통합 적용 시 가장 큰 효과를 발휘한다.

| 구분 | **COBIT 2019** | **ITIL 4** | **PMBOK 7th** | **ISO 27001 (ISMS)** |
|---|---|---|---|---|
| **주 목적** | 거버넌스·관리 목표 통제 | 서비스 가치 창출 | 프로젝트 성공 달성 | 정보보안 경영체계 |
| **추상화 레벨** | 전략+전술+운영 (Full) | 전술+운영 (Service Focus) | 전술 (Project Focus) | 운영+통제 (보안) |
| **핵심 산출물** | 40개 목표 + PAM 평가 | 34 Practice + SVC | 8 PD + 12 Principle | 93 Annex A 통제 + 7 Clause |
| **측정 체계** | Maturity 0-5 (PAM) | Maturity Model (Service) | Domain Performance | 114 Statement of Applicability |
| **인증 체계** | COBIT Certified (ISACA) | ITIL Foundation/MP/SL | PMP/PfMP (PMI) | ISO 27001 Lead Auditor |
| **강점** | 이사회 보고·컴플라이언스·측정 | 실용적 운영 노하우·Agile 친화 | 프로젝트 범위·일정·리스크 | 보안 통제·위험평가 |
| **약점** | 구현 복잡도 높음·도구화 어려움 | 거버넌스 부분 빈약 | 운영 단계 이후 미흡 | 거버넌스·전략 연계 부족 |
| **적합 조직** | 금융·공공·대기업 | IT 서비스 조직 전체 | 프로젝트 중심 조직 | 정보보안 의무화 조직 |
| **Agile 친화도** | 중간 (EDM은 Agile과 충돌 가능) | 높음 (Practices는 Agile화 가능) | 높음 (PMBOK 7th이 Agile 통합) | 중간 (ISMS는 변형 가능) |
| **비용 (연간 도입)** | 고 (컨설팅 5,000만원+) | 중 (2,000-3,000만원) | 중 (2,000만원+) | 중-고 (3,000-5,000만원) |

**다른 프레임워크와의 연결**:
1. **COBIT
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 649 / 800

<- **이전**: [648. IT 경영 관리 핵심 토픽 648번 시험 요약](/studynote/12_it_management/05_security_compliance/648_it_management_core_topic_648_exam_summary/)
**다음**: [650. IT 경영 관리 핵심 토픽 650번 시험 요약](/studynote/12_it_management/05_security_compliance/650_it_management_core_topic_650_exam_summary/) ->

---
