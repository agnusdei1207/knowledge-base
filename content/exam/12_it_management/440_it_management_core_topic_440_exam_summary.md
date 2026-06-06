---
title: "IT Management Core Topic 440 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영관리는 **COBIT 2019(거버넌스 목표 40개·관리 목표 40개), ITIL 4(34개 실무 가이드), ISO 27001:2022(93개 통제 항목), PMBOK 7th, CMMI v2.0** 등 글로벌 표준 프레임워크를 **Governance–Strategy–Management–Operation 4계층 아키텍처**로 통합 운영하여, Business-IT Alignment 수준을 정량적으로 통제하는 경영 체계이다.
> 2. **가치**: Gartner·McKinsey 벤치마크 기준으로 **IT 투자 ROI 20~35% 향상, IT 운영 비용(OpEx) 15~28% 절감, 컴플라이언스 위반 리스크 60~75% 감소, MTTR(평균 복구 시간) 40~60% 단축, 정보시스템 감리 지적사항 50% 감소** 등 정량적·정성적 가치를 동시 창출한다.
> 3. **판단 포인트**: **Build vs Buy, On-Premise vs Hybrid/Multi-Cloud, 중앙집중(CoE) vs 분산(Federated) 거버넌스, Waterfall vs Agile vs DevSecOps, Zero Trust vs Perimeter Security** 등 핵심 아키텍처 의사결정에서 **총소유비용(TCO)·위험노출(Risk Exposure)·전략적 유연성(Strategic Agility)**의 3축 트레이드오프를 정량적으로 비교·판단해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 시대적 배경과 기술적 도전

4차 산업혁명·디지털 전환(DX)·ESG 규제 강화·공급망 다변화·AI 기반 사이버 위협의 5중 압력으로, IT 부서는 단순 비용센터(Cost Center)에서 **전략적 가치 창출 센터(Value Center)**로 역할이 전환되었다. 한국 정보화진흥원(KIAT)의 「2024 국내 기업 IT 성숙도 조사」에 따르면 국내 대기업의 **62%가 IT-Business Alignment를 "부분 달성"**, **28%는 "미달성"**으로 응답해, IT 경영 체계의 정비가 시급한 상황이다.

특히 「2023 개정 개인정보보호법」(가명정보·안전조치 강화), 「클라우드컴퓨팅법」(2025.1 시행), EU AI Act, DORA(금융 sector resilience), CSAP(클라우드 보안 인증) 등 **컴플라이언스 체계가 다층화**되면서, IT 경영은 **한 번의 감리/감사로 끝나는 정적 통제(Static Control)**가 아닌 **지속적 모니터링(Continuous Auditing)** 패러다임으로 전환되었다.

```text
+------------------------------------------------------------------+
|         4차 산업혁명 시대 IT 경영 환경의 5대 압력(Forces)         |
+------------------------------------------------------------------+

   +----------+    +----------+    +----------+    +----------+    +----------+
   |  DX 가속 |    | 규제강화 |    |사이버위협|    |  AI/XaaS |    | ESG 패러 |
   |(Cloud·AI)|    |(PIPL·AI |    |(제로데이 |    |(생성형AI |    |  다임    |
   |  확산    |    | Act·DORA)|    | 랜섬웨어)|    |  모델)   |    |(탄소배출 |
   +----+-----+    +----+-----+    +----+-----+    +----+-----+    +----+-----+
        |               |               |               |               |
        +---------------+---------------+---------------+---------------+
                                        |
                                        v
                +------------------------------------------+
                |   IT 부서의 역할 패러다임 전환            |
                |   ------------------------------         |
                |   과거: Cost Center  ->  현재: Value Hub  |
                |   통제: 사후감리       ->  실시간 거버넌스 |
                |   구조: 수직 계층       ->  Agile·DevOps |
                |   보고: 재무중심        ->  가치중심 KPI  |
                +------------------------------------------+
```

### 1.2 IT 경영의 진화 단계(Evolutionary Stages)

| 단계 | 시대 | 핵심 키워드 | 대표 프레임워크 | 한계 |
|:---:|:---:|:---:|:---:|:---:|
| 1단계 | 1970~80 | Data Processing | IBM BIS, I/S Planning | 전략 부재, 부서간 사일로 |
| 2단계 | 1990 | IT Alignment | Henderson & Venkatraman(1993) SAMM | 정적·연간 단위 정렬 |
| 3단계 | 2000 | IT Governance | COBIT 4/5, ISO 38500, ITIL v3 | 통제 위주, 혁신 저해 |
| 4단계 | 2010 | Digital & Agile | COBIT 2019, ITIL 4, DevOps, SAFe | 거버넌스-애자일 충돌 |
| 5단계 | 2020~ | AI-Native & ESG | COBIT 2019(+Focus Areas), NIST CSF 2.0, ISO 42001, ESG-Gov | 윤리·지속가능성·AI 거버넌스 통합 |

### 1.3 왜 IT 경영관리 체계가 필요한가?

- **투자 정당성 확보**: 한국정보화진흥원의 IT 성숙도 모델에 따르면 체계적 IT 거버넌스 도입 기업은 IT 투자 수익률(ROIT)이 평균 23% 더 높음
- **규제 준수 자동화**: ISMS-P, ISO 27001, PCIDSS, HIPAA, GDPR 등 다중 인증을 통합 GRC(Governance·Risk·Compliance) 플랫폼으로 운영 시 인증 유지 비용 35% 절감
- **사이버 회복탄력성**: NIST CSF 2.0의 Identify-Protect-Detect-Respond-Recover 5함수 기반 운영 시 MTTR 45% 단축
- **전략적 민첩성**: Business-IT Alignment 성숙도 Level 3 이상 확보 시 신규 비즈니스 런칭 시간(Lead Time) 40% 단축

- **📢 섹션 요약 비유**: IT 경영관리는 **자동차의 '통합 차량 제어 시스템(Vehicle Dynamics Control)'**과 같습니다. 과거에는 엔진·브레이크·조향이 각자 작동했다면, 현대 차량은 ECU가 모든 시스템을 실시간 모니터링하며 ABS·ESC·TCS를 통합 제어합니다. IT 경영관리 체계가 바로 이 ECU 역할이며, COBIT은 통신 프로토콜, ITIL은 운영 매뉴얼, ISO 27001은 보안 모듈에 해당합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 IT 경영관리 4계층 아키텍처

IT 경영관리는 **Governance(거버넌스) -> Strategy(전략) -> Management(관리) -> Operation(운영)**의 4계층 구조로, 각 계층은 상위 정책을 하위 실행으로 cascading하고, 하위 계층의 성과/리스크를 상위로 reporting하는 **양방향 피드백 루프**로 작동한다.

```text
+---------------------------------------------------------------------+
|         IT 경영관리 4계층 아키텍처 (4-Layer Architecture)            |
+---------------------------------------------------------------------+

+---------------------------------------------------------------------+
| Layer 1: GOVERNANCE (거버넌스 계층) - 정책·원칙·의사결정 구조        |
| +-----------------------------------------------------------------+ |
| |  • 이사회 IT위원회(ITC) — CIO/CDO/CTO 보고 체계                  | |
| |  • COBIT 2019 EDM( Evaluate, Direct, Monitor) 5개 도메인         | |
| |  • ISO 38500 IT 거버넌스 원칙: 책임·전략·수행·규율·윤리·적합성  | |
| |  • RACI Matrix(Responsible, Accountable, Consulted, Informed)    | |
| +-----------------------------------------------------------------+ |
+------------------------------+--------------------------------------+
                               |  Cascade: 정책·목표 전파
                               v
+---------------------------------------------------------------------+
| Layer 2: STRATEGY (전략 계층) — 중장기 방향·포트폴리오·로드맵      |
| +-----------------------------------------------------------------+ |
| |  • IT 전략계획(ISP, 3~5년) -> IT 거버넌스 프레임워크(EA·PMO·IRM)  | |
| |  • 포트폴리오 관리: BCG 2x2(Star/Cash Cow/Q./Dog) × TOGAF ADM    | |
| |  • Balance Scorecard(재무·고객·프로세스·학습성장)                | |
| |  • Value Realization: Benefits Realization Plan(BRP)             | |
| +-----------------------------------------------------------------+ |
+------------------------------+--------------------------------------+
                               |  Translate: 전략->프로젝트·서비스
                               v
+---------------------------------------------------------------------+
| Layer 3: MANAGEMENT (관리 계층) — 프로세스·서비스·리스크 통제       |
| +-----------------------------------------------------------------+ |
| |  • ITIL 4 SVS(서비스 가치 시스템) — 34개 실무, 3축(계획·개선·CX) | |
| |  • PMBOK 7th 12원칙 + 8성능도메인 — 애자일·예측·하이브리드      | |
| |  • ISO 27001:2022(ISMS) — 93 통제항목(Annex A)                   | |
| |  • NIST CSF 2.0 — Govern + ID·PR·DE·RS·RC 6함수                 | |
| |  • ISO 31000 Risk Mgmt — Context·Assessment·Treatment·Monitoring | |
| +-----------------------------------------------------------------+ |
+------------------------------+--------------------------------------+
                               |  Execute: 일상 프로세스·도구
                               v
+---------------------------------------------------------------------+
| Layer 4: OPERATION (운영 계층) — 인프라·애플리케이션·데이터          |
| +-----------------------------------------------------------------+ |
| |  • 인프라: IaC(Terraform·Ansible) · Container(K8s) · Observability| |
| |  • 애플리케이션: DevSecOps Pipeline · API Gateway · Service Mesh | |
| |  • 데이터: DataOps · Data Catalog · Data Quality · Data Lineage  | |
| |  • 보안: SIEM·SOAR·EDR·Zero Trust · CSPM·CWPP·CIEM              | |
| |  • ITSM: Incident·Problem·Change·CMDB · AIOps                    | |
| +-----------------------------------------------------------------+ |
+------------------------------+--------------------------------------+
                               |  Feedback: KPI·KRI·메트릭
                               v
                  +------------------------------+
                  |  Continuous Improvement Loop  |
                  |  (PDCA + OODA + ITIL CSI)    |
                  +------------------------------+
```

### 2.2 핵심 구성 요소 및 메커니즘

| 계층 | 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---:|:---|:---|:---|
| L1 거버넌스 | **이사회 IT 위원회(ITC)** | IT 의사결정 최종 승인·감독 | 분기 1회 정례, CIO KPI 보고(전략적 정렬·가치·리스크·자원) |
| L1 거버넌스 | **COBIT 2019 EDM** | 거버넌스 목표 5개·관리 목표 35개 체계 | EDM(평가·지시·모니터) -> APO(정렬·계획·조직) -> BAI(구축·도입) -> DSS(배달·지원·보안) -> MEA(모니터·평가·감사) **5도메인·40 governance/management objective** |
| L2 전략 | **EA(Enterprise Architecture)** | 비즈니스·데이터·애플리케이션·기술 4계층 통합 | TOGAF ADM(Architecture Development Method) 8단계 Phase A~H, **ArchiMate 3.2** 표기법 |
| L2 전략 | **IT 포트폴리오 관리** | 투자 우선순위·자원 배분 최적화 | BCG 매트릭스 + ROI·NPV·옵션가치(Real Options) 분석, Stage-Gate® |
| L3 관리 | **ITIL 4 SVS** | 서비스 가치 사슬(Value Chain) 운영 | **Service Value Chain 6활동**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support->Improve), 34개 실무 |
| L3 관리 | **PMBOK 7th** | 프로젝트 8성능도메인 관리 | **팀·개발방식·계획·프로젝트작업·배달·측정·불확실성·복잡성**, 12원칙 기반 애자일/예측/하이브리드 적응 |
| L3 관리 | **ISO 27001:2022** | 정보보안 ISMS 93통제 운영 | **Annex A 4그룹**(Organizational·People·Physical·Technological), PDCA 6.1~10.2, Statement of Applicability(SOA) |
| L3 관리 | **ISO 31000:2018** | 리스크 관리 통합 프레임워크 | **원칙·프레임워크·프로세스**(Context->Risk Assessment->Treatment->Monitoring->Communication) 6단계 |
| L3 관리 | **NIST CSF 2.0** | 사이버보안 운영 프레임워크 | **6함수(Govern·Identify·Protect·Detect·Respond·Recover)** + Tier 1~4 성숙도 + Profile |
| L4 운영 | **DevSecOps** | 개발-보안-운영 통합 파이프라인 | SAST·DAST·SCA·IaC Scan, GitOps(Argo CD), Policy as Code(OPA) |
| L4 운영 | **AIOps/SRE** | 운영 자동화·관측성(Observability
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 440 / 800

<- **이전**: [439. SW 아키텍처 평가 ATAM CBAM](/studynote/12_it_management/05_security_compliance/439_sw_architecture_evaluation_atam_cbam/)
**다음**: [441. IT 경영 관리 핵심 토픽 441번 시험 요약](/studynote/12_it_management/05_security_compliance/441_it_management_core_topic_441_exam_summary/) ->

---
