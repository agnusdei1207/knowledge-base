+++
title = "672. IT 경영 관리 핵심 토픽 672번 시험 요약 (IT Management Core Topic 672 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019 거버넌스 체계, ITIL 4 서비스 가치 사슬(34개 실무), ISO 38500 IT 거버넌스 표준을 기반으로, IT 전략-아키텍처-투자-운영-성과의 End-to-End 가치 흐름을 정량·정성적으로 통합 관리하는 경영 시스템이다.
> 2. **가치**: BSC 4관점(재무/고객/내부/학습성장) 기반 KPI 체계와 Earned Value Management(EVM), TCO/ROI/TCO-RoI 분석을 통해 IT 투자 효율을 평균 25~40% 개선하며, 거버넌스 성숙도(Level 1~5) 향상을 통한 의사결정 속도 3배 가속, 컴플라이언스 위반 70% 감소 효과를 실현한다.
> 3. **판단 포인트**: 중앙집중형(CoE) vs 분산형(Federated) 거버넌스 모델 선택, Agile-DevOps 환경에서의 ITIL 4 적용 방식(SIAM: Service Integration and Management), 그리고 한국 ISMS-P 인증, 개인정보보호법, 클라우드 이용자 보호 가이드라인 등 규제 준수와 디지털 전환 속도의 균형점이 핵심 결정 요인이다.

---

## Ⅰ. 개요 및 필요성

정보화 시대를 넘어 **디지털 전환(DX: Digital Transformation) 4.0 시대**에 진입하면서, IT는 더 이상 비용 센터(Cost Center)가 아닌 **전략적 가치 창출의 핵심 엔진**으로 재정의되었다. McKinsey(2023)에 따르면 DX 성공 기업은 매출 성장률 2.5배, 영업이익률 1.8배, 주주수익률 2.4배를 달성하지만, 전체 DX 프로젝트의 70%는 목표 미달실패한다(Gartner 2024). 실패의 근본 원인은 기술 부재가 아닌 **IT 경영 관리 체계의 부재**다.

기존 IT 관리는 인프라 가용성(Uptime 99.9%), 헬프데스크 응답시간(SLA), CAPEX/OPEX 예산 통제에 머물렀다. 그러나 클라우드, AI, 데이터 경제가 주도하는 현재 환경에서는 **IT-Business Alignment(전략적 정렬)**, **Value Realization(가치 실현)**, **Risk-Adjusted Performance(리스크 조정 성과)**의 3축 패러다임이 요구된다.

```text
[ IT 경영 관리 패러다임 진화 ]

   +-----------------------------------------------------------------+
   |  1980s-1990s: IT 운영관리 시대                                  |
   |  +-------------+                                                |
   |  | 데이터센터  | --> CAPEX 통제, 시스템 가용성, 배치 스케줄     |
   |  |  Mainframe  |                                                |
   |  +-------------+                                                |
   |         |                                                       |
   |         v  Y2K, ERP, 인터넷 확산                                |
   |  +---------------------------------+                            |
   |  | 2000s: IT 서비스 관리 시대      |                            |
   |  |  +--------+  +--------+  +----+|                            |
   |  |  |Service |  |SLA/OLA |  |CMDB|| --> ITIL v2/v3, ISO 20000|
   |  |  |Desk    |  |관리    |  |    ||                            |
   |  |  +--------+  +--------+  +----+|                            |
   |  +---------------------------------+                            |
   |         |                                                       |
   |         v  클라우드, 모바일, 빅데이터                            |
   |  +------------------------------------------+                   |
   |  | 2010s: IT 거버넌스 시대                  |                   |
   |  |  +------+ +------+ +------+ +------+  |                   |
   |  |  |전략  | |투자  | |위험  | |성과  |  | --> COBIT 5/2019  |
   |  |  |정렬  | |관리  | |관리  | |측정  |  |   ISO 38500       |
   |  |  +------+ +------+ +------+ +------+  |                   |
   |  +------------------------------------------+                   |
   |         |                                                       |
   |         v  AI, 플랫폼, ESG, 디지털 신뢰                         |
   |  +--------------------------------------------------+          |
   |  | 2020s-현재: IT 가치경영 시대 (Value-driven IT)    |          |
   |  |  +------+ +------+ +------+ +------+ +------+  |          |
   |  |  |전략  |->|아키텍|->|투자  |->|운영  |->|가치  |  |          |
   |  |  |(Str) | |처(EA)| |(PMO) | |(ITIL)| |실현  |  |          |
   |  |  +------+ +------+ +------+ +------+ +------+  |          |
   |  |            End-to-End Value Stream               |          |
   |  +--------------------------------------------------+          |
   +-----------------------------------------------------------------+
```

**왜 지금 IT 경영 관리가 필수적인가?**

- **규제 강화**: 개인정보보호법(2023 전면개정), AI 기본법(2026 시행예정), EU AI Act, DORA(금융), CSAP(클라우드 보안인증) 등 컴플라이언스 요구 폭증
- **투자 규모 증가**: 글로벌 IT 지출 2024년 5.1조 USD, 한국 IT 시장 98조 원 돌파, 그러나 IT 프로젝트 성공률은 31% 미만(Standish Group CHAOS Report 2023)
- **사이버 리스크 증대**: 랜섬웨어 피해年均 200% 증가, 평균 다운타임 비용 분당 5,600~9,000 USD(IBM 2023)
- **가치 증명 요구**: CFO/CSuite가 IT 투자의 정량적 ROI/TCO를 요구, IT 부서의 "Cost Center"에서 "Value Center"로 전환 압력

- **📢 섹션 요약 비유**: IT 경영 관리는 자동차의 **통합 계기판(클러스터)**과 같습니다. 속도계(성과 KPI), 연료계(TCO), 엔진 온도계(리스크), 네비게이션(전략 정렬) 모두를 한 화면에서 보여주어, 운전자인 CEO/CIO가 실시간으로 정확한 판단을 내리게 합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. IT 경영 관리 5대 핵심 영역(COBIT 2019 기반)

```text
[ IT 경영 관리 5대 영역 통합 아키텍처 ]

                        +---------------------+
                        |   거버넌스 목표     |
                        |  (Stakeholder Needs)|
                        |  • Value Delivery   |
                        |  • Risk Optimization|
                        |  • Resource Opt.    |
                        |  • Stakeholder Trans|
                        +----------+----------+
                                   | Cascade
            +----------------------+----------------------+
            v                      v                      v
   +----------------+    +----------------+    +----------------+
   |  1. 전략 정렬   |    | 2. 아키텍처    |    | 3. 투자 관리   |
   |   (Align)      |    |   (Architecture)|   |   (Portfolio)  |
   |                |    |                |    |                |
   | • 전략 맵       |    | • TOGAF ADM    |    | • Stage-Gate   |
   | • BSC 4관점    |    | • FEAF         |    | • TCO/ROI/Pay. |
   | • OKR/KPI      |    | • Zachman      |    | • EVM          |
   | • SAMM         |    | • DoDAF        |    | • APQC PCF     |
   +--------+-------+    +--------+-------+    +--------+-------+
            |                     |                     |
            +--------------+------+--------------+------+
                           v                     v
                  +----------------+    +----------------+
                  | 4. 운영/서비스 |    | 5. 성과/리스크  |
                  |   (Deliver)    |    |   (Measure)    |
                  |                |    |                |
                  | • ITIL 4 SVS   |    | • BSC + KPI    |
                  | • DevOps/SRE  |    | • RACI Matrix  |
                  | • SIAM        |    | • ISMS-P/ISO   |
                  | • SLA/OLA/UC |    | • BCM/DR       |
                  +----------------+    +----------------+
                           |                     |
                           +----------+----------+
                                      v
                          +----------------------+
                          |  지속적 개선 루프     |
                          |  (PDCA + OODA)        |
                          |  Maturity Assessment  |
                          +----------------------+
```

### 2. COBIT 2019 거버넌스 시스템 핵심 컴포넌트

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **거버넌스 & 관리 목표(40개)** | EDM: Evaluate, Direct, Monitor + 4 도메인(APO, BAI, DSS, MEA) | Align-Plan-Organize(APO) 14개, Build-Acquire-Implement(BAI) 11개, Deliver-Service-Support(DSS) 6개, Monitor-Evaluate-Assess(MEA) 4개, EDM 5개로 총 40개 목표. 각 목표는 Process, Structure, People, Skill, Information, Service, Technology 7요소로 구성 |
| **디자인 팩터(11개)** | 거버넌스 시스템 맞춤 설계 | 전략(Strategy), 목표(Goals), 리스크 프로파일, 리스크 이슈, 위협 환경, 컴플라이언스 요건, 역할(IT 역할), IT 구현 방식, 기술 채택 전략, 산업, 기업 크기/규모. **71가지 우선순위 조합**으로 맞춤형 거버넌스 시스템 생성 |
| **핵심 모델 & 참조 모델** | 표준화·벤치마킹 기반 | CMMI(능력성숙도 5단계), CMMI v3.0(2024): Maturity Level 1-5 (Initial->Managed->Defined->Quantitatively Managed->Optimizing). COSO ERM 2017(리스크 관리), ISO/IEC 33000(프로세스 평가) |
| **거버넌스/관리 성숙도** | 역량 측정·개선 | Capability Level 0-5: Incomplete->Performed->Managed->Established->Predictable->Optimizing. Level 3 이상에서 PA(Process Attribute) 5개(Attribute ID, Work Product Management, Work Product Definition, Process Deployment, Quantitative Analysis)로 측정 |
| **포커스 영역 & 이슈/워크** | 실무 적용 패키지 | Cybersecurity, DevOps, Digital Transformation, ESG, Privacy, Risk, Small Medium Enterprise 7개 핵심 Focus Area. 60+ 개의 Guide 참조 가능 |

### 3. ITIL 4 서비스 가치 시스템(SVS) 상세

```text
[ ITIL 4 Service Value System (SVS) ]

  +-------------------------------------------------------------+
  |  Opportunity/Demand ◄--> Value (Co-Creation)              |
  +---------------------------+---------------------------------+
                              |
                              v
  +----------------------------------------------------------+
  |  GUIDING PRINCIPLES (7대 지침원칙)                        |
  |  1. Focus on value        5. Think and work holistically |
  |  2. Start where you are   6. Keep it simple and practical |
  |  3. Progress iteratively  7. Collaborate and promote     |
  |  4. Collaborate and promote visibility   visibility      |
  +----------------------------------------------------------+
                              |
                              v
  +----------------------------------------------------------+
  |  GOVERNANCE                                                  |
  |  • Direction (전략) • Evaluation (평가) • Monitoring (모니터)|
  +----------------------------------------------------------+
                              |
                              v
  +----------------------------------------------------------+
  |  SERVICE VALUE CHAIN (서비스 가치 사슬, 6개 활동)          |
  |                                                            |
  |   +----+    +----+    +----+    +----+    +----+    +----+|
  |   |Plan|--->|Eng |--->|Desi|--->|Obta|--->|Dely|--->|Supp||
  |   |    |    |age |    |gn  |    |in  |    |    |    |ort ||
  |   +----+    +----+    +----+    +----+    +----+    +----+|
  |                                                            |
  |   34개 실무 프로세스가 이 6개 활동에 매핑                   |
  |   (예: Change Enablement->Engage, Service Desk->Deliver/Support)|
  +----------------------------------------------------------+
                              |
                              v
  +----------------------------------------------------------+
  |  PRACTICES (34개 실무 + 3개 일반 관리 = 37개)             |
  |  +-------------+-------------+-------------+              |
  |  | 일반 관리    | 서비스 관리  | 기술 관리    |              |
  |  | • Strategy  | • Incident  | • Deploy-   |              |
  |  | • Portfolio | • Problem   |   ment Mgmt |              |
  |  | • Workforce | • Service   | • Infra &   |              |
  |  | • Archi-    |   Request   |   Platform  |              |
  |  |   tecture   | • Change    | • Software  |              |
  |  | • Risk      | • Release   |   Dev & Mgmt|              |
  |  | • Finan-    | • Continual |             |              |
  |  |   cial      |   Improve   |             |              |
  |  +-------------+-------------+-------------+              |
  +----------------------------------------------------------+
                              |
                              v
  +----------------------------------------------------------+
  |  CONTINUAL IMPROVEMENT (지속적 개선)                       |
  |  7단계 모델: Vision->Where->Where->Gaps->Targets->Actions->Review|
  +----------------------------------------------------------+
```

### 4. 핵심 정량 모델 및 지표

**A. TCO(T
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 672 / 800

<- **이전**: [671. IT 경영 관리 핵심 토픽 671번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/671_it_management_core_topic_671_exam_summary/)
**다음**: [673. IT 경영 관리 핵심 토픽 673번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/673_it_management_core_topic_673_exam_summary/) ->

---
