---
title: "630. IT 경영 관리 핵심 토픽 630번 시험 요약 (IT Management Core Topic 630 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 630번 토픽은 정보관리 기술사 시험의 **IT 거버넌스·전략·서비스·투자·아웃소싱·EA·보안·조직·컴플라이언스** 9대 영역을 통합한 종합 관리 프레임워크로, COBIT 2019·ITIL 4·ISO 38500·TOGAF·PMP/Agile을 거버넌스-실행-평가 3계층으로 결합한 경영 통제 체계이다.
> 2. **가치**: 정량적으로는 IT 투자 대비 ROI 20~35% 개선, 운영 비용 TCO 15~25% 절감, 계획대비 이행 편차 ±5% 이내 통제, 정성적으로는 CFO·CIO·CEO 간 의사결정 일관성 확보 및 ISO 27001·ISMS-P·PCI-DSS 등 다중 컴플라이언스 단일 창구 통제 효과를 제공한다.
> 3. **판단 포인트**: Build vs. Buy vs. Outsource 의사결정, 중앙집중(CoE) vs. 페데레이션(Federated) IT 거버넌스 모델, Balanced Scorecard의 4관점(재무·고객·내부·학습성장) 가중치 배분, 그리고 Earned Value Management(EVM) CPI/SPI 0.95~1.05 임계치 운영이 핵심 트레이드오프이다.

---

## Ⅰ. 개요 및 필요성

정보관리 기술사 시험의 630번 계열 토픽은 **"IT를 경영 자산으로 통제 가능한 시스템으로 만든다"**는 대전제를 다룬다. 1980년대 이후 데이터센터 자동화, 1990년대 ERP·SCM·CRM 도입, 2000년대 SOA·Web 2.0, 2010년대 클라우드·모바일·빅데이터, 2020년대 AI·MLOps·제로트러스트로 IT가 **Cost Center -> Utility -> Strategic Enabler**로 진화하면서, IT 자체를 경영학의 재무·전략·조직·위험관리 프레임과 결합해야 하는 요구가 폭증했다.

과거 IT 관리는 "시스템 가동률(Availability) 99.9%"라는 기술 KPI 중심이었으나, 현재는 **"IT 투자가 EBITDA에 기여하는 비율(Technology Business Management, TBM Council 기준)"**과 **"사이버 침해로 인한 주가 변동 베타 계수(IBM Ponemon 2024 기준 평균 -7.5%)"** 같은 경영 KPI로 측정된다. ISO 38500(2008 첫 발행, 2015 전면 개정)에서는 **"Direct(지휘) - Evaluate(평가) - Monitor(모니터)"** 3원칙으로 이사회-경영진-IT조직의 책임 분담을 법제도적으로 명시했고, 한국에서는 2022년 전자금융감독규정 개정으로 주요 금융사의 CIO 보고 의무화, 2023년 개인정보보호법 개정으로 DPO(데이터보호책임자) 선임 의무, 2024년 클라우드 데이터센터 안전성 검증 제도로 IT 거버넌스의 법적 구속력이 강화되었다.

```text
[IT 경영관리 9대 영역 통합 프레임워크 - 거버넌스 풀스택]

  +-------------------------------------------------------------------------+
  |        이사회 (Board) - ISO 38500 Principle: Direct / Evaluate         |
  +-------------------------------------------------------------------------+
                                  | 연간 IT 전략 승인
                                  v
  +-------------------------------------------------------------------------+
  |         CISO / CRO / CDO / CPO / CAIO (현대의 C-Suite 통합 거버넌스)   |
  +-------------------------------------------------------------------------+
            |              |              |              |            |
            v              v              v              v            v
   +--------------+ +------------+ +------------+ +----------+ +----------+
   | 1.전략기획   | | 2.거버넌스 | | 3.서비스   | | 4.투자성 과| | 5.아웃소싱|
   | ISP / BSP   | | COBIT2019  | | ITIL 4     | | TCO/ROI  | | SLA/RFP  |
   | 목표 계층화  | | RACI 매트릭| | 34 Practices| | EVA / BSC| | 다단계계약|
   +--------------+ +------------+ +------------+ +----------+ +----------+
            |              |              |              |            |
            +--------------+--------------+--------------+------------+
                                  | 6. EA (TOGAF ADM)
                                  v
   +--------------+ +------------+ +------------+ +----------------------+
   | 7.보안(ISM)  | | 8.조직/HR  | | 9.컴플라이언|  10.프로젝트 PMO      |
   | ISO 27001   | | COE vs Fed | | SOX/ISMS-P |  PMP / SAFe / EVM    |
   | 제로트러스트 | | 직무체계   | |  내부감사  |  WBS / Critical Path  |
   +--------------+ +------------+ +------------+ +----------------------+
                                  |
                                  v
                    +--------------------------+
                    | KPI 대시보드 (Real-time) |
                    | CSF -> KPI -> KPI Tree    |
                    | BSC 4관점 + CSF Top 5    |
                    +--------------------------+
```

**기존 vs. 신규 패러다임 비교**

| 차원 | 1990s (시스템 시대) | 2020s (경영 시대) |
|---|---|---|
| KPI 단위 | 가동률 99.9%, MTTR < 1hr | TCO 회수기간 4.2년, NPS 50+, ROI 28% |
| 책임 주체 | 시스템 운영팀 (실링크) | CDO + CIO + CISO 공동 책임 |
| 통제 방식 | 사후 대응 (Reactive) | 실시간 Risk Score (Predictive) |
| 데이터 흐름 | 내부 ERP 폐쇄망 | API Gateway + Data Mesh 페데레이션 |
| 컴플라이언스 | 연 1회 자체 점검 | 지속적 감시(Continuous Audit) + GRC 통합 |

- **📢 섹션 요약 비유**: 630번 토픽은 **"건물의 소방·전기·엘리베이터·소방차 진입로를 별개로 관리하던 시절에서, IBIS(지능형 빌딩 통합 시스템) 한 화면에서 12개 시스템의 운전상태를 실시간 그래프로 보여주는 중앙관제센터로 전환한 것"**과 같다. 이때 관제 요원은 IT 거버넌스 위원회, 화면은 KPI 대시보드, 센서는 ITIL 이벤트를 의미한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

630번 토픽의 핵심은 **"PDCA(Plan-Do-Check-Act) + CobiT의 4 도메인(EDM/APO/BAI/MEI) + ISO 38500 6원칙 + ITIL 4 SVS(서비스 가치 시스템)"** 의 4중 통합 제어 루프다. 아래 다이어그램은 전략 결정에서 운영 종료까지의 End-to-End 흐름을 보여준다.

```text
[IT 경영관리 End-to-End 제어 루프 (EDM -> APO -> BAI -> MEI)]

   +------------------- 전략 계층 (연 1회) -----------------------+
   |  ① EDM (Evaluate, Direct, Monitor) - COBIT 2019            |
   |  • 이사회 승인 : IT 전략목표 5개, KPI 임계치               |
   |  • Risk Appetite Statement: 가용 중단시간 4hr/year 이내     |
   |  • 전략 포트폴리오: Build 60% / Buy 30% / Outsource 10%    |
   +-------------------------------------------------------------+
                                  | Charter 승인
                                  v
   +------------------- 기획 계층 (분기 1회) ---------------------+
   |  ② APO (Align, Plan, Organize) - 14개 관리목표             |
   |  • APO01 : 관리 프레임워크 유지보수                        |
   |  • APO05 : 포트폴리오 결정 (PMF / Net Present Value)       |
   |  • APO12 : 위험 관리 (위험 등록부 + KRI 12개)              |
   |  • APO13 : 보안 관리 (제로트러스트 로드맵)                 |
   +-------------------------------------------------------------+
                                  | 프로젝트 헌장
                                  v
   +------------------- 실행 계층 (월/주 단위) ------------------+
   |  ③ BAI (Build, Acquire, Implement) - 11개 관리목표          |
   |  • BAI01 : 프로그램/프로젝트 관리 (EVM: CPI, SPI)          |
   |  • BAI03 : 솔루션 도입 (RFP -> PoC -> 계약)                 |
   |  • BAI06 : 변경 관리 (CAB, CR 승인 SLA 4hr)               |
   |  • BAI10 : 구성 관리 (CMDB 자산 정확도 ≥ 95%)             |
   +-------------------------------------------------------------+
                                  | 운영 핸드오프
                                  v
   +------------------- 운영/모니터링 계층 (실시간) -------------+
   |  ④ MEI (Monitor, Evaluate, Assess) - 4개 관리목표          |
   |  • MEA01 : 성능 및 적합성 모니터링 (BSC 점수)             |
   |  • MEA02 : 내부 통제 시스템 (SOX 404 매핑)                |
   |  • MEA03 : 외부 컴플라이언스 (ISO 27001, ISMS-P)          |
   |  • MEA04 : 감사 (연 1회 위험기반 감사, RBIA)              |
   +-----------------------------------------------------------------+
                                  | 피드백 (CSF -> EDM 재투입)
                                  +--------+
                                           v
                              [연간 거버넌스 보고서 + ISACA 감사]
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **① EDM 거버넌스 (Evaluate-Direct-Monitor)** | 이사회·CEO·CIO의 의사결정 통제 | COBIT 2019의 5개 Governance System Component(원리/방침/프로세스/조직구조/정보)와 7개 정보 흐름(원천->목적지)을 40개 관리목표(40 Governance & Management Objectives)와 매핑. 매년 Risk Appetite를 재설정하고 전략목표 CSF(Critical Success Factor) 5개를 도출한다. |
| **② APO 기획(Align-Plan-Organize)** | IT-비즈니스 정렬, 포트폴리오 최적화 | 14개 프로세스로 구성. APO05(Managed Portfolio)는 PMF(Project Management Framework)와 NPV·IRR·Payback Period를 사용해 우선순위화하고, APO13(Managed Security)는 NIST CSF(Identify-Protect-Detect-Respond-Recover) 5단계와 제로트러스트 5대 원칙(Verify Explicitly, Least Privilege, Assume Breach, Micro-segmentation, Continuous Diagnostics)을 결합한다. |
| **③ BAI 실행(Build-Acquire-Implement)** | 솔루션 도입, 프로젝트 완료, 변경 적용 | BAI01(Managed Programs)는 PMI/PMBOK 7th의 8 Performance Domains(Team/Planning/Work/Delivery/Measurement/Uncertainty/Complexity/Engagement)로, Earned Value Management(EVM) 지표 EV·AC·PV를 사용해 CPI(비용 성과) = EV/AC, SPI(일정 성과) = EV/PV를 실시간 산출한다. CPI ≥ 0.95, SPI ≥ 0.95를 그린 존으로 정의한다. |
| **④ MEI 모니터링(Monitor-Evaluate-Assess)** | 성과 측정, 통제, 감사, 컴플라이언스 | MEA01은 ITSM 도구(Jira Service Management, ServiceNow ITSM)에서 SLA·MTTR·MTBF를 추출하고 BSC 4관점(Financial 25%, Customer 25%, Internal Process 25%, Learning & Growth 25%)으로 가중 평균을 산정한다. MEA02는 SOX 404 ITGC(Change Mgmt, Logical Access, Ops) 3개 영역을 12개 통제로 매핑한다. |
| **⑤ ITIL 4 Service Value System (SVS)** | 운영 단계 서비스 가치 창출 | 5개 핵심 컴포넌트(서비스 가치체인, 관행 34개, 원칙 7개, 거버넌스, 지속적 개선)로 구성. Incident -> Problem -> Change -> Release 흐름을 Value Stream으로 매핑하고, SLO(Service Level Objective) 99.9% 미달 시 Continual Improvement(Kaizen) 트리거가 자동 발화된다. |
| **⑥ ISO 38500 거버넌스 평가 모델** | 외부 표준 적합성 검증 | 6원칙(책임·전략·획득·성과·규정·인간행태)에 대해 Maturity Model 5단계(0 비존재~5 최적화)로 자가진단한다. ISO/IEC 38500:2015는 의무(Shall)가 아닌 권고(Should)이나, EU DORA(2025.1 시행)와 한국 전자금융감독규정 31조가 참조 표준으로 인용하고 있다. |

**핵심 산식 및 임계치**

1. **EVM (Earned Value Management)**
   - `BAC (Budget At Completion)`: 프로젝트 총 승인 예산
   - `EV (Earned Value) = BAC × % Complete` (실제 진척률 반영)
   - `AC (Actual Cost)`: 실제 투입 비용
   - `PV (Planned Value) = BAC × Planned % Complete`
   - `CPI = EV / AC` (≥ 0.95 그린, 0.85~0.95 옐로우, < 0.85 레드)
   - `SPI = EV / PV` (≥ 0.95 그린, 0.85~0.95 옐로우, < 0.85 레드)
   - `EAC (Estimate At Completion) = BAC / CPI`
   - `VAC (Variance At Completion) = BAC - EAC`

2. **TCO (Total Cost of Ownership) - Gartner TCO 모델 5계층**
   - `직접비 (HW+SW+네트워크) : 간접비 (전력·냉각·공간) : 인력비 (FTE 5.5인/年) : 교육비 (연봉 7%) : 기회비용 = 4 : 1.5 : 3 : 0.8 : 0.7` 비율이 일반적
   - 클라우드 전환 시 `TCO 회수기간 = CapEx - OpEx
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 630 / 800

<- **이전**: [629. IT 경영 관리 핵심 토픽 629번 시험 요약](/studynote/12_it_management/05_security_compliance/629_it_management_core_topic_629_exam_summary/)
**다음**: [631. IT 경영 관리 핵심 토픽 631번 시험 요약](/studynote/12_it_management/05_security_compliance/631_it_management_core_topic_631_exam_summary/) ->

---
