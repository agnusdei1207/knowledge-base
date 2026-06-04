+++
title = "632. IT 경영 관리 핵심 토픽 632번 시험 요약 (IT Management Core Topic 632 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019, ITIL 4, ISO/IEC 38500 등 글로벌 거버넌스 프레임워크를 기반으로 IT 거버넌스(Governance)·전략(Strategy)·포트폴리오(Portfolio)·서비스(Service)·리스크(Risk)·성과(Performance)를 end-to-end로 통합 관리하는 경영 체계이며, 5대 핵심 영역(전략-거버넌스-아키텍처-운영-혁신)의 상호의존성을 이해하는 것이 합격의 핵심입니다.
> 2. **가치**: BS 15000/ISO 20000 인증 기업 대비 IT 서비스 가용성 99.95%->99.99%(연간 장애시간 263분->52분), COBIT 기반 프로세스 성숙도 Level 2->Level 4 시 IT 비용 20~30% 절감, EA 도입 시 중복 투자 40% 제거 및 Time-to-Market 35% 단축 효과가 검증된 정량적 가치를 창출합니다.
> 3. **판단 포인트**: Balance Score Card(BSC) 4관점(재무·고객·내부 프로세스·학습성장) × 7대 거버넌스 책임(POCD-RM) × 5단계 성숙도(Level 0~5) × TOGAF ADM 8단계 사이클을 **Trade-off Matrix**로 판단하며, "Build vs Buy", "In-house vs Outsourcing", "단일 표준 vs 다중 프레임워크" 같은 아키텍처 의사결정에서 ROI, TCO, Risk-adjusted NPV를 종합적으로 산정해야 합니다.

---

## Ⅰ. 개요 및 필요성

**기술사 시험 출제 배경**: 정보관리기술사(기술사 제76호) 4교시 논술형은 632번 대분류(정보시스템 구축·관리) 아래에서 (가)정보시스템 기획, (나)정보시스템 분석·설계, (다)정보시스템 구축·운영, (라)정보시스템 감리·진단의 4개 중분류가 출제되며, IT 경영 관리 토픽은 2022년 이후 디지털전환(DX), AI 거버넌스, ESG-ICT, 공급망 보안(SBOM) 이슈와 결합되어 매년 1~2문항씩 출제되고 있습니다.

**산업 패러다임 전환**: 전통적 IT 운영(2000년대)은 ITIL v2/v3 기반 "프로세스 중심 안정성"이 핵심이었으나, 2020년 이후로는 (1) Cloud-Native(쿠버네티스, 서비스 메시), (2) Data-Driven(데이터 거버넌스, 데이터 패브릭), (3) AI-Native(MLOps, AIOps, LLM 거버넌스), (4) Zero-Trust(마이크로 세그멘테이션), (5) Platform Engineering(InnerSource, Golden Path) 등 **5대 패러다임**으로 전환되어 이를 통합 관리할 수 있는 새로운 거버넌스 역량이 요구됩니다.

**도입 필요성**:
- **규제 준수**: 개인정보보호법(PIPA), 정보통신망법, 클라우드컴퓨팅법, AI 기본법(2026.1 시행), EU AI Act(2024.8 공표), DORA(2025.1 시행) 등 규제 준수(Compliance) 요구 증대
- **투자 정당화**: Gartner 보고 기준 Fortune 500 기업의 **평균 IT 예산 4.6% 매출 대비**이나 효과적 거버넌스 부재 시 30% 낭비, IT 비용 가시성 확보 시 ROI 280% 개선
- **사이버 리스크**: 랜섬웨어 공격 평균 복구 비용 2023년 USD 1.85M -> 2024년 USD 2.73M(IBM 보고), 제로트러스트 아키텍처 및 BCM(사업연속성관리) 의무화
- **ESG-ICT**: Scope 3 GHG 배출의 50% 이상이 디지털 인프라에서 발생, Green IT/Software Carbon Intensity(SCI) 측정 의무화

```text
[IT 경영 관리 5대 핵심 영역 통합 프레임워크 - 632번 출제 영역]

  +--------------------------------------------------------------------+
  |                    [전략-거버넌스-아키텍처-운영-혁신]                  |
  |                       Top-Down Alignment                            |
  +--------------------------------------------------------------------+
       |             |             |             |             |
       v             v             v             v             v
  +---------+  +----------+  +----------+  +----------+  +---------+
  | I.전략   |  |II.거버넌스|  |III.아키텍처|  |IV.운영    |  | V.혁신  |
  |Strategy |  |Governance |  |Architecture|  |Operation |  |Innovation|
  |         |  |          |  |          |  |          |  |         |
  |•ISP     |  |•COBIT    |  |•TOGAF    |  |•ITIL 4   |  |•DX전략  |
  |•BSA     |  |•ISO38500 |  |•Zachman  |  |•DevOps   |  |•AI거버  |
  |•EA      |  |•ISO27001 |  |•FEAF     |  |•SRE      |  |•Platform|
  |•PI     |  |•ISMS-P   |  |•ArchiMate|  |•ITSM     |  |•DataOps |
  +----+----+  +-----+----+  +-----+----+  +-----+----+  +----+----+
       |             |             |             |             |
       +-------------+------+------+-------------+-------------+
                            v
                +--------------------------+
                |   [성과 측정 및 가치 실현] |
                |  BSC(BSC 4관점) + KPI    |
                |  ROI / TCO / NPV / EVA   |
                |  CSF(CSF) / GQM          |
                +--------------------------+
                            |
                            v
                +--------------------------+
                |  [리스크·컴플라이언스]     |
                | ISO31000 / NIST CSF 2.0  |
                | PIPA / DORA / AI기본법   |
                +--------------------------+

   ※ 출제 키워드: 거버넌스 체계, ISP 수립, EA 도입, ITSM 운영, DX혁신
```

**기존 패러다임 vs 신규 패러다임 비교**:

| 구분 | 기존(2000~2015) | 신규(2020~현재) |
| :--- | :--- | :--- |
| 거버넌스 프레임워크 | COBIT 5, ITIL v3, PMBOK 5 | COBIT 2019, ITIL 4, PMBOK 7, SAFe 6 |
| 인프라 운영 | On-Premise, Virtualization | Multi/Hybrid Cloud, Container, Serverless |
| 서비스 모델 | IaaS 중심, ITIL Service Desk | PaaS/SaaS, SRE, GitOps, AIOps |
| 보안 모델 | Castle-Moat, 방어적 보안 | Zero-Trust, SASE, DevSecOps, SBOM |
| 데이터 관리 | 데이터베이스 중심, RDBMS | Data Lake, LakeHouse, Data Mesh, Vector DB |
| 조직 문화 | Dev-Ops 사일로 | Platform Engineering, InnerSource, FinOps |
| 성과 측정 | 가용성(Uptime), 처리량(TPS) | MTTR, Change Failure Rate, DORA 4 Metrics, SLO |

- **📢 섹션 요약 비유**: IT 경영 관리는 **항공우주 산업의 ILS(Integrated Logistic Support, 통합후勤지원)**와 같습니다. 비행기(시스템) 한 대를 운영하려면 정비·연료·조종사 훈련·예약 발권·연락 체계가 모두 맞물려야 하듯, IT도 5대 영역이 동시에 돌아가야 기업이 안전하게 "비행"할 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**IT 경영 관리 시스템의 4-Layer 아키텍처**:

```text
[IT 경영 관리 4-Layer 아키텍처 및 정보 흐름]

   +---------------------------------------------------------------+
   | Layer 4: 의사결정 및 전략 (Strategic Layer)                     |
   | +-------------+ +-------------+ +-------------+ +----------+  |
   | |이사회/경영층 | | IT steering | |사업-IT 연계 | | CIO Office|  |
   | | (Board)     | | Committee   | | (BPM)       | |          |  |
   | +------+------+ +------+------+ +------+------+ +-----+----+  |
   +--------+---------------+---------------+--------------+-------+
            +---------------+--------+------+--------------+
                                     v
   +---------------------------------------------------------------+
   | Layer 3: 거버넌스 및 관리 (Governance & Management Layer)        |
   |  +------------------------------------------------------+    |
   |  |  COBIT 2019 - 40 Governance & Mgmt Objectives        |    |
   |  |  +------+ +------+ +------+ +------+ +------+         |    |
   |  |  |EDM  | |APO   | |BAI   | |DSS   | |MEA   |         |    |
   |  |  | 5개 | | 14개 | | 11개 | | 6개  | | 4개  |         |    |
   |  |  +------+ +------+ +------+ +------+ +------+         |    |
   |  |  Evaluate | Align | Build | Deliver | Monitor        |    |
   |  |  Direct   | Plan  | Run   | Service |                |    |
   |  |  Monitor  | Organ |                       |  +------+         |    |
   |  +------------------------------------------------------+    |
   +--------+------------------------------------------------------+
            v
   +---------------------------------------------------------------+
   | Layer 2: 프로세스 및 서비스 (Process & Service Layer)            |
   |  +--------------+ +--------------+ +----------------------+   |
   |  |  ITIL 4 SVS  | |  ISO 20000  | |  PMBOK 7 / PRINCE2  |   |
   |  |  34 Practices| |  Service Mgmt| |  프로젝트/프로그램    |   |
   |  |              | |  10 Sections | |  Portfolio Mgmt      |   |
   |  | • Incident   | | • Service    | | • 8 Performance     |   |
   |  | • Problem    | |   Request   | |   Domains            |   |
   |  | • Change     | | • Relation   | | • 12 Principles      |   |
   |  | • Release    | | • Delivery   | | • Tailoring          |   |
   |  | • Service    | | • Control    | |                      |   |
   |  |   Level      | | • Resolution | |                      |   |
   |  +--------------+ +--------------+ +----------------------+   |
   +--------+------------------------------------------------------+
            v
   +---------------------------------------------------------------+
   | Layer 1: 기술 및 인프라 (Technology & Infrastructure Layer)     |
   |  +----------+ +----------+ +----------+ +------------------+  |
   |  | Multi-   | |Container | |Data      | |Security &        |  |
   |  |Cloud     | |& K8s     | |Platform  | |Compliance Stack   |  |
   |  |AWS/AZ/GCP| |Istio     | |Lake/House| |ZTNA / SASE / SIEM |  |
   |  +----------+ +----------+ +----------+ +------------------+  |
   +---------------------------------------------------------------+

   [측정 및 피드백 루프]
   <----------- BSC(BSC 4관점) + DORA + KPI Dashboard --------------
```

| 계층 | 구성 요소 | 역할 | 핵심 기술/방법론 및 동작 방식 |
| :--- | :--- | :--- | :--- |
| **L4 의사결정** | 이사회/ITSC | IT 전략 의결, 예산 승인, Risk Appetite 설정 | ISO 38500 6원칙(책임, 전략, 취득, 성능, 적합성, 인간행태), RACI 매트릭스, Portfolio Prioritization (NVP, Strategic Fit) |
| **L4 의사결정** | CIO/CDO/CTO | 중장기 로드맵, ROI 의사결정, EA 거버넌스 | Strategy Map(BSC), OKR(목표-핵심지표), Wardley Maps, 기술 트레이드오프 분석 |
| **L3 거버넌스** | COBIT 2019 | IT 거버넌스 목표(40개)와 관리 목표(40개) 정렬 | EDM(5) + APO(14) + BAI(11) + DSS(6) + MEA(4), Cascade Goals, Design Factors 11종 |
| **L3 거버넌스** | ISO 27001/ISMS-P | 정보보호 경영체계 | Plan-Do-Check-Act(PDCA), 93개 통제 항목(Annex A 2022), 위험평가 방법론(HLPR, OWASP) |
| **L3 거버넌스** | NIST CSF 2.0 | 사이버 보안 프레임워크 | Govern / Identify / Protect / Detect / Respond / Recover 6개 Function, Tier 1~4 |
| **L2 프로세스** | ITIL 4 SVS | IT 서비스 관리 | 34개 Practice, 4차원 모델(조직·정보·기술·파트너), Service Value Chain 6단계, 7 Guiding Principles |
| **L2 프로세스** | PMBOK 7 | 프로젝트 관리 | 8개 Performance Domain(팀, 개발방식, 계획, 프로젝트작업, 전달, 측정, 불확실성, 측정), 12 Principle |
| **L2 프로세스** | DevOps & SRE | 소프트웨어 전달 및 안정성 | CALMS(문화·자동화·리니어·측정·공유), DORA 4 Metrics(배포빈도·변경리드타임·변경실패율·복구시간), Error Budget |
| **L1 기술** | Cloud Native | 인프라 추상화 | CNCF Landscape 30+ 카테고리, Multi-Cloud 관리 도구(Terraform, Crossplane, Pulumi) |
| **L1 기술** | Container | 배포 표준화 | Kubernetes(1.30+, 1000+ API), Istio/Linkerd(서비스 메시), ArgoCD/Flux(GitOps), OPA(Kubernetes Policy) |
| **L1 기술** | Data Platform | 데이터 거버넌스 | Data Fabric(Gartner), Data Mesh(Zhamak Dehghan
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 632 / 800

<- **이전**: [631. IT 경영 관리 핵심 토픽 631번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/631_it_management_core_topic_631_exam_summary/)
**다음**: [633. IT 경영 관리 핵심 토픽 633번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/633_it_management_core_topic_633_exam_summary/) ->

---
