---
title: "IT Management Core Topic 500 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 COBIT 2019·ITIL 4·ISO 38500 등 글로벌 거버넌스 프레임워크를 기반으로, IT 전략-투자-운영-성능-리스크를 End-to-End로 정렬(Alignment)하여 기업의 가치(Value Realization)를 극대화하는 통합관리 체계이다.
> 2. **가치**: EA 기반 Port-folio 최적화로 IT 투자 대비 ROI를 평균 25~40% 향상시키고, SLA/OLA 미달을 90% 이하로 축소하며, ISMS-P 인증·IT감리 Pass Rate를 95% 이상으로 끌어올려 컴플라이언스 비용을 절감한다.
> 3. **판단 포인트**: 중앙집중형(Centralized) vs 분산형(Distributed/Federated) 거버넌스 모델 선택, Agile-Waterfall-Hybrid 프로젝트 방법론의 프로젝트 특성(규모·불확실성·규제)별 적용, Build vs Buy vs Cloud(SaaS/PaaS/IaaS) 의사결정이 전체 TCO와 Time-to-Market을 결정한다.

---

## Ⅰ. 개요 및 필요성

4차 산업혁명(AI·빅데이터·클라우드·IoT) 시대를 맞아 IT는 단순 비용센터(Cost Center)에서 **전략적 가치센터(Value Driver)**로 그 위상이 변화하였다. 그러나 한국 기업의 IT 예산 중 70% 이상이 운영·유지보수(OpEx)에 편중되어 신규 가치 창출 투자는 30% 미만(한국정보화진흥원 2023년 보고서 기준)이며, 이로 인해 **"IT 성숙도(Gartner CIO Survey 2023 기준 평균 Level 2.8/5)"** 정체 현상이 발생한다. IT 경영관리는 이러한 한계를 돌파하기 위해 거버넌스·전략·프로세스·리스크·자원을 통합적으로 통제·측정·개선하는 **"Plan-Build-Run-Monitor"** 사이클의 4계층 체계를 요구한다.

과거(2000년대)에는 SI(System Integration) 중심의 일회성 프로젝트 관리에 치중했으나, 현재는 **지속적 거버넌스(Continuous Governance)** + **데이터 기반 의사결정(Data-Driven Decision Making)** + **지속가능한 ESG-반영 IT 운영**으로 패러다임이 전환되었다. 기술사 시험에서 IT 경영관리는 단순 암기형이 아니라 **"문제 상황 제시 -> 프레임워크 매핑 -> 의사결정 근거 도출"** 형태의 서술형·사례형으로 출제된다.

```text
[IT 경영관리 4계층 통합 프레임워크]

   +----------------------------------------------------------+
   |  Layer 1: IT 거버넌스 (Governance)                       |
   |  +- 이사회/IT전략위원회 -> COBIT 2019 EDM 도메인         |
   |  +- ISO 38500 원칙(책임·전략·획득·성과·준수·인간행위)  |
   |  +- RACI 매트릭스, 의사결정 권고(Recommend) 구조         |
   +--------------------+-------------------------------------+
                        | KPI 연동 (Strategy -> Performance)
   +--------------------v-------------------------------------+
   |  Layer 2: IT 전략·포트폴리오 관리 (Strategy & Portfolio)|
   |  +- EA(TOGAF ADM 9.2) 기반 Capability Map              |
   |  +- 투자 우선순위: NPV·IRR·Payback·Risk-Adjusted ROI    |
   |  +- Build vs Buy vs Cloud 3원칙 의사결정 매트릭스        |
   |  +- Balanced Scorecard(BSC) 4관점(재무·고객·프로세스·학습)|
   +--------------------+-------------------------------------+
                        | SLA/OLA 연동 (Strategy -> Operation)
   +--------------------v-------------------------------------+
   |  Layer 3: IT 운영·서비스 관리 (Operation & Service)    |
   |  +- ITIL 4 Service Value System (SVS) 34 Practices      |
   |  +- DevOps + SRE (MTTR·Change Failure Rate <15%)        |
   |  +- FinOps: 클라우드 비용 최적화(사용량 기반 과금)       |
   |  +- BCP/DRP: RTO(복구시간)·RPO(복구시점) SLA 정의       |
   +--------------------+-------------------------------------+
                        | Control & Audit (Operation -> Monitor)
   +--------------------v-------------------------------------+
   |  Layer 4: 리스크·컴플라이언스·감리 (Risk & Compliance)  |
   |  +- ISMS-P(정보보호관리체계), PIMS(개인정보)             |
   |  +- ISO 27001:2022(Annex A 93 통제항목)                  |
   |  +- IT감리: 착수->현황분석->종합의견(5단계)               |
   |  +- ESG-ISMS 통합(친환경 데이터센터, 에너지 효율 PUE<1.4)|
   +----------------------------------------------------------+
```

- **📢 섹션 요약 비유**: IT 경영관리는 **항공기의 "비행 계기판 + 조종사 매뉴얼 + 관제탑 통신"**이 합쳐진 시스템과 같다. 거버넌스는 관제탑, 전략은 비행계획, 운영은 자동조종, 리스크관리는 비상절차에 해당한다. 어느 하나라도 없으면 추락(사업 실패)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IT 경영관리의 핵심은 **"Value Governance Loop"** 이다. COBIT 2019의 거버넌스 시스템(Governance System)은 5개 도메인(**EDM: Evaluate-Direct-Monitor, APO: Align-Plan-Organize, BAI: Build-Acquire-Implement, DSS: Deliver-Service-Support, MEA: Monitor-Evaluate-Assess**)에 40개 Govern/Manage Objective를 매핑하고, 이를 11개 디자인 팩터(Design Factor)로 조직 상황에 맞게 조정한다.

핵심 측정 체계는 **"CSF(Key Goal Indicator) -> KPI(Key Performance Indicator) -> KRI(Key Risk Indicator)"** 3단계로 구성된다. 예를 들어 "고객만족도(CSF)" -> "SLA 달성률 KPI(99.9% 가용성)" -> "장애발생건수 KRI(월 5건 이하)" 와 같이 인과관계를 형성한다.

```text
[COBIT 2019 Governance & Management Objectives 매핑 흐름]

   +--------------+
   | 비즈니스 목표|  (예: 신규서비스 출시 6개월 내 시장점유율 15%)
   +------+-------+
          | Cascading (CSF: Time-to-Market)
   +------v-------------------------------+
   | IT 목표 (예: Agile 전사 확대,        |
   |          DevOps 파이프라인 자동화)    |
   +------+-------------------------------+
          | Mapping
   +------v-------------------------------+
   | Enabler: 프로세스·정보·구조·사람·    |
   |          서비스&인프라·정책(7대 촉진자)|
   +------+-------------------------------+
          | Process
   +------v-------------------------------+
   | Governance/Management Objective       |
   | EDM01: 거버넌스 프레임워크 수립/유지  |
   | APO04: 관리혁신(Agile/DevOps 도입)    |
   | BAI03: 솔루션 선정(Build/Buy)         |
   | DSS02: 서비스 요청·사고 관리          |
   | MEA01: 성과·준수 모니터링            |
   +------+-------------------------------+
          | KPI 측정
   +------v-------------------------------+
   | 측정: 배포빈도(Deploy Freq)·변경실패율|
   |       MTTR(Mean Time To Restore)      |
   |       NRR(Net Revenue Retention)      |
   +--------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **EDM(Evaluate-Direct-Monitor)** | 이사회·IT전략위원회 의사결정 지원 | Benefit Realization·Risk Optimization·Resource Optimization 3대 의사결정, 연 4회 의사결정 사이클, 의사결정권한 매트릭스(RACI) 적용 |
| **APO(Align-Plan-Organize)** | 전략-포트폴리오-아키텍처 정렬 | TOGAF ADM 9.2(Phase A~F), Capability-Based Planning, BCM(비지니스연속성관리) BIA(Business Impact Analysis) |
| **BAI(Build-Acquire-Implement)** | 프로젝트·변화·이행 통제 | PMBOK 7th(8개 Performance Domain), PRINCE2(7 Principle/7 Process), SAFe(Scaled Agile) 4-step Iteration |
| **DSS(Deliver-Service-Support)** | 서비스 운영·SLA 관리 | ITIL 4 34개 Practice 중 Incident·Problem·Change·Service Desk·SLA, Site Reliability Engineering(SRE) Error Budget 99.9~99.99% |
| **MEA(Monitor-Evaluate-Assess)** | 성과측정·내부감사·IT감리 | CSF/KPI/KRI 3-tier, ISO 27001 내부감사, COBIT 2019 Maturity(Rating 0~5), 외부 IT감리(5단계: 착수/현황/분석/평가/종합의견) |

**핵심 정량 파라미터**:
- **NPV(순현재가치)**: NPV = Σ(CF_t / (1+r)^t) − 초기투자. IT 투자 의사결정 시 할인율(WACC) 8~12% 적용.
- **TCO(Total Cost of Ownership)**: CapEx(하드웨어/소프트웨어) + OpEx(인건비·전력·라이선스) 5년 합계. 클라우드 전환 시 평균 30~40% 절감(McKinsey 2023).
- **PUE(Power Usage Effectiveness)**: PUE = 총시설전력/IT전력. 그린데이터센터 기준 1.4 이하(에너지이용합리화법).
- **MTTR / MTBF / MTRS**: 평균복구시간 / 평균고장간격 / 평균복구서비스시간. KPI 연동: MTTR < 30분, MTBF > 720시간 목표.
- **ROI / Payback Period**: ROI(%) = (편익−비용)/비용×100. Payback(개월) = 초기투자/월현금흐름. SaaS 전환 시 보통 18~24개월 회수.

- **📢 섹션 요약 비유**: COBIT 5개 도메인은 **자동차의 "핸들(EDM) - 네비게이션(APO) - 엔진(BAI) - 바퀴(DSS) - 계기판(MEA)"**로, 운전자가 목적지(사업목표)까지 안전·경제적·신속하게 도달하도록 돕는 5대 장치다.

---

## Ⅲ. 비교 및 연결

IT 경영관리의 핵심 의사결정 영역에서 자주 혼동되는 개념들을 명확히 비교한다. 기술사 시험에서는 "A와 B의 차이점 + 우리 조직에 적합한 것은?" 형태의 비교 문제가 빈출한다.

| 구분 | 중앙집중 거버넌스(CoE) | 분산형 거버넌스(Federated) | 하이브리드(Two-Tier) |
| :--- | :--- | :--- | :--- |
| **의사결정 권한** | CIO 산하 CoE(Center of Excellence)에 집중 | 현업 BU(Business Unit)별 IT 권한 위임 | 전략/표준은 본사, 실행은 사업부 |
| **적합 조직** | 금융·공공·규제 산업(은행·정부) | 다국적·다품종(글로벌 IT기업) | 중견~대기업(가장 보편적) |
| **장점** | 표준 준수·비용 통제 용이, 보안 일관성 | 시장 대응 속도, 현업 요구 즉시반영 | 균형 - 통제와 민첩성 양립 |
| **단점** | Time-to-Market 저조, 부서간 사일로 | 이중투자(중복 시스템), 통제 취약 | 거버넌스 복잡도^, RACI 명확화 필수 |
| **적용 프레임워크** | COBIT 5 EDM 엄격 적용 | Agile-First, Product-centric 운영 | 상위 COBIT + 하위 Scrum/SAFe |
| **KPI 사례** | 표준 준수율 98% 이상, TCO 절감률 15% | Time-to-Market 6개월 이내, NPS 70+ | 통합 ROI + 현업별 속도지표 병행 |

**연계 기술·도구 스택**:
- **상위(거버넌스)**: COBIT 2019, ISO 38500, ISO 27001:2022, ISMS-P 인증
- **중위(전략·프로세스)**: TOGAF 9.2 EA, BPMN 2.0, ARIS/Egineer EA 플랫폼, SAP LeanIX
- **하위(운영·자동화)**: ITIL 4(ServiceNow/BMC Helix), Jira+Confluence(Agile), Terraform/Ansible(IaC), Prometheus+Grafana(모니터링)
- **보안·컴플라이언스**: NIST CSF 2.0, PCI-DSS, GDPR/개인정보보호법, DORA(금융)

- **📢 섹션 요약 비유**: 중앙집중 거버넌스는 **"국립중앙도서관처럼 모든 책을 한 곳에서 관리"**하는 방식이고, 분산형은 **"각 학교 도서관이 자율 운영"**하는 방식이다. 하이브리드는 **"교과서는 본사가, 참고서는 학교가 결정"**하는 두 단계 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **CSF/KPI 인과관계 검증**: 모든 KPI가 상위 CSF(고객만족·매출·리스크)와 1:1 매핑되어 있는가? "측정되지 않으면 관리되지 않는다(If you can't measure it, you can't manage it)" 원칙에 따라 7±2개 이내의 핵심 KPI만 유지(예: IT 운영 KPI 5개: 가용성 99.95% / MTTR <30분 / CSAT 4.2/5 / SLA 위반 <2건/월 / TCO YoY -8%).
2. **Build vs Buy vs Cloud 의사결정**: 다음 6개 가중치를 적용한 점수화 모델을 사용하라. (①핵심경쟁력 ②Time-to-Market ③총소유비용TCO ④규제·보안 ⑤확장성 ⑥핵심인력 보유). 예: "규제 산업 + 핵심 비핵심 = SaaS", "핵심 차별화 + 민첩성 필요 = Build(Internal Platform)".
3. **프로젝트 방법론 선택**: 프로젝트 특성(규모·복잡도·불확실성·규제)에 따라 (a)Predictive(Waterfall)/공공 SI 80% 이상, (b)Agile/SaaS·앱개발 6개월 이내, (c)Hybrid(공공 Agile-Fixed) 적용. 한국 공공 SI는 **"공공정보화 사업 Agile 도입 가이드라인(2022, 행정안전부)"**에 따라 단계적 Hybrid(설계는 Waterfall, 개발은 Sprint) 적용.
4. **SLA 단계화(다층화)**: ①내부 SLA(사업부↔IT) ②외부 SLA(고객↔사업부)
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 500 / 800

<- **이전**: [499. IT 경영 관리 핵심 토픽 499번 시험 요약](/studynote/12_it_management/05_security_compliance/499_it_management_core_topic_499_exam_summary/)
**다음**: [501. IT 경영 관리 핵심 토픽 501번 시험 요약](/studynote/12_it_management/05_security_compliance/501_it_management_core_topic_501_exam_summary/) ->

---
