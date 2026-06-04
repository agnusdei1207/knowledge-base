---
title: "797. IT 경영 관리 핵심 토픽 797번 시험 요약 (IT Management Core Topic 797 Exam Summary)"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리 Topic 797은 **COBIT 2019, ITIL 4, ISO/IEC 38500** 기반의 IT 거버넌스 프레임워크와 **TOGAF 10 ADM**, **Zachman Framework 3.2**로 대표되는 엔터프라이즈 아키텍처를 통합하여, **Value Creation (가치 창출)** 관점에서 IT-Portfolio-Business Alignment를 달성하는 종합 관리 체계이다.
> 2. **가치**: 체계 적용 시 **IT 투자 대비 ROI 평균 23~35% 향상**(Gartner 2024 기준), **IT 운영 비용 18~27% 절감**, **프로젝트 실패율 40%->12%로 감소**, **컴플라이언스 감사 소요 시간 65% 단축** 등 정량적 효과를 입증하고 있다.
> 3. **판단 포인트**: 중앙집중형 거버넌스(CoE 기반)와 분산형 거버넌스(Federated 모델) 간의 Trade-off, **RACI 매트릭스**의 책임 소재 명확화, **3 Lines of Defense 모델** 적용 시 1/2/3 Line의 역할 분리, 그리고 **Agile/DevOps** 환경에서의 거버넌스 경량화(GOVERNANCE-as-a-Code) 여부가 핵심 의사결정 포인트이다.

---

## Ⅰ. 개요 및 필요성

정보기술의 단순 지원 역할에서 벗어나 **전략적 비즈니스 동인(Strategic Business Enabler)**으로 전환됨에 따라, IT 자원의 체계적 관리 및 거버넌스에 대한 요구가 폭발적으로 증가하고 있다. 전통적 IT 관리(2000년대 이전)는 **Cost Center** 관점에서 비용 절감에 초점을 맞추었으나, 현재는 **Digital Business Platform**, **AI/ML 기반 의사결정 시스템**, **클라우드 네이티브 아키텍처** 등 복잡한 기술 환경에서 **가치 사슬(Value Chain)** 전반에 걸쳐 IT가 기여하도록 관리 체계를 재설계해야 한다.

Topic 797은 **ISO/IEC 38500:2015 (IT Governance for Organizations)**, **COBIT 2019 (Control Objectives for Information and Related Technologies)**, **ITIL 4 (Information Technology Infrastructure Library)**, **PMI PMBOK 7th**, **TOGAF 10** 등 5대 글로벌 표준 프레임워크를 통합적으로 이해하고, 이를 비즈니스 환경에 맞게 **Cascade(계승·적용)**하는 능력을 평가한다. 특히 **ENISA(유럽 사이버보안청)** 및 **NIST CSF 2.0**과 연계된 보안 거버넌스, **DAMA-DMBOK 2.0** 기반 데이터 거버넌스, 그리고 **ISO 27001:2022** 인증 체계까지 포괄하는 **Multi-Framework Integration**이 핵심이다.

```text
+-------------------------------------------------------------------------+
|                  Topic 797: IT 경영 관리 통합 프레임워크                  |
+-------------------------------------------------------------------------+
|                                                                         |
|   [비즈니스 전략 계층]                                                    |
|      +------------------------------------------+                       |
|      |  Mission/Vision -> 전략적 목표(KPI/OKR)  |                       |
|      |  BCG/Porter Value Chain 분석              |                       |
|      +--------------+---------------------------+                       |
|                     |  Alignment(정렬)                                  |
|   [거버넌스 계층]    v                                                    |
|      +------------------------------------------+                       |
|      |  ISO 38500  ◄--►  COBIT 2019             |                       |
|      |   (6 원칙)        (40 Governance          |                       |
|      |  ·책임성    |      & Management          |                       |
|      |  ·전략     |       Objectives)           |                       |
|      |  ·수행     |  ·EDM(05)·APO(14)           |                       |
|      |  ·적합성   |  ·BAI(11)·DSS(06)           |                       |
|      |  ·규율     |  ·MEA(04)                    |                       |
|      +------+-----------------------+----------+                       |
|             |                       |                                   |
|   [아키텍처 계층]|                       |[서비스 관리 계층]              |
|      +------v--------+         +------v----------+                     |
|      |  TOGAF 10 ADM  |         |   ITIL 4 SVS    |                     |
|      |  (8 Phase:     |         |  ·Service Value |                     |
|      |   A->H Phases)  |         |   System        |                     |
|      |  ·Preliminary  |         |  ·34 Practices  |                     |
|      |  ·A: Vision    |         |  ·Guiding       |                     |
|      |  ·B: Business  |         |   Principles(7) |                     |
|      |  ·C: Info Sys  |         |  ·4 Dimensions  |                     |
|      |  ·D: Tech      |         +------+----------+                     |
|      |  ·E: Opp&Sol   |                |                               |
|      |  ·F: Migration |         +------v----------+                     |
|      |  ·G: Governance|         |  운영/실행 계층  |                     |
|      |  ·H: Change Mgmt|        |  ·Service Desk  |                     |
|      +------+---------+         |  ·Incident Mgmt |                     |
|             |                   |  ·Change Mgmt   |                     |
|             |                   |  ·Problem Mgmt  |                     |
|             |                   |  ·SLM/SLA Mgmt  |                     |
|             |                   +-----------------+                     |
|             |                                                           |
|             v                                                           |
|   [기반 기술 계층]                                                        |
|   +---------------------------------------------------------+           |
|   |  Cloud (AWS/Azure/GCP) | Kubernetes | Microservices     |           |
|   |  Data Lake/Warehouse   | AI/ML Ops  | Zero-Trust Sec    |           |
|   |  API Gateway            | Observability (O11y)            |           |
|   +---------------------------------------------------------+           |
|                                                                         |
+-------------------------------------------------------------------------+
```

| 비교 차원 | 2000년대 이전 (As-Is) | 2020년대 이후 (To-Be) |
| :--- | :--- | :--- |
| **IT 역할** | 비용센터(Cost Center) / Back-office 지원 | 가치 창출(Value Creator) / 전략 동인(Strategic Driver) |
| **아키텍처** | 모놀리식(Monolithic) / Mainframe 중심 | 클라우드 네이티브 / 마이크로서비스 / Event-Driven |
| **거버넌스** | 통제 중심(Control-First) / 수동 감사 | 위험 기반(Risk-Based) / Continuous Compliance |
| **투자 평가** | TCO(Total Cost of Ownership) 위주 | **VRIO + ROIC + NPV + Real Options** 다차원 |
| **조직 문화** | 명령-통제(Waterfall) | Agile + DevOps + SRE + Product-centric |
| **기술 도입** | 3~5년 단위 장기 프로젝트 | 2주 Sprint 단위 점진적 릴리즈 |
| **데이터 관리** | ETL / 데이터베이스 silo | Data Mesh / Data Fabric / Lakehouse |
| **보안 모델** | Castle-and-Moat (Perimeter) | Zero Trust / SASE / Identity-Centric |

- **📢 섹션 요약 비유**: IT 경영 관리는 마치 **도시의 종합 도시계획**과 같다. 토지이용(EA), 교통(거버넌스), 상하수도(IT 운영), 치안(보안·컴플라이언스) 등 각 영역을 별도 설계하되 **도시 기본계획(Master Plan)**이라는 큰 청사진 아래 통합적으로 운영해야 시민(비즈니스)에게 가치를 제공한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Topic 797의 핵심 메커니즘은 **3 Layer Governance Model**(Strategy -> Decision -> Operation)과 **Closed-Loop Control System**으로 구성된다. **PDCA(Deming Cycle)**를 거버넌스 수준에서 확장한 **Direct -> Monitor -> Evaluate -> Direct** 사이클이 ISO 38500의 핵심이며, COBIT 2019에서는 이를 **EDM(평가, 지시, 모니터링) 5개 프로세스**로 구체화한다.

```text
+---------------------------------------------------------------------+
|           ISO/IEC 38500 IT 거버넌스 6대 원칙 적용 흐름도             |
+---------------------------------------------------------------------+
|                                                                     |
|  +--------+   +--------+   +--------+   +--------+   +--------+    |
|  | 책임성  |--->| 전략   |--->| 수행   |--->| 적합성 |--->| 규율성 |    |
|  |Respnsbl|   |Strategy|   |Perform |   |Conform |   |Discipl.|    |
|  +---+----+   +---+----+   +---+----+   +---+----+   +---+----+    |
|      |            |            |            |            |         |
|      v            v            v            v            v         |
|  +-------------------------------------------------------------+   |
|  |         3 Lines of Defense Model (3LOD)                       |   |
|  |  +------------------------------------------------------+    |   |
|  |  | 1st Line: 운영/사업 (Operational Mgmt - 위험 소유)    |    |   |
|  |  |  ·서비스 데스크, 데브옵스팀, SRE                      |    |   |
|  |  |  ·일상적 위험 식별 및 통제                            |    |   |
|  |  +------------------------------------------------------+    |   |
|  |  +------------------------------------------------------+    |   |
|  |  | 2nd Line: 위험/컴플라이언스 (Risk & Compliance)       |    |   |
|  |  |  ·CISO, GRC, 정보보안, BCP/DR 담당                   |    |   |
|  |  |  ·정책 수립, 모니터링, 자문                          |    |   |
|  |  +------------------------------------------------------+    |   |
|  |  +------------------------------------------------------+    |   |
|  |  | 3rd Line: 내부감사 (Internal Audit)                   |    |   |
|  |  |  ·독립적 assurance 제공                               |    |   |
|  |  |  ·감사위원회(AC) 직보                                |    |   |
|  |  +------------------------------------------------------+    |   |
|  +-------------------------------------------------------------+   |
|                              |                                      |
|                              v                                      |
|   +----------------------------------------------------------+     |
|   |  Continuous Monitoring Loop (Closed-Loop Control)         |     |
|   |  +--------+  +--------+  +--------+  +--------+          |     |
|   |  | Plan   |-->| Do     |-->| Check  |-->| Act    |--+       |     |
|   |  |전략/KPI|  |실행/배포|  |측정/감사|  |개선/시정|  |       |     |
|   |  +--------+  +--------+  +--------+  +--------+  |       |     |
|   |       ^                                          |       |     |
|   |       +------------------------------------------+       |     |
|   +----------------------------------------------------------+     |
|                                                                     |
+---------------------------------------------------------------------+
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **ISO 38500 Council / Board** | 의사결정 거버넌스 최상위 | 6대 원칙(책임·전략·수행·적합·규율·인간요소) 적용; **Board IT Committee**의 **Quarterly Review**; **MFA(Multi-Factor Authentication)** 기반 의사결정 보안 |
| **COBIT 2019 EDM(05)** | 거버넌 시스템의 5개 핵심 프로세스 | EDM01(거버넌스 체계 설정), EDM02(이익 실현 보장), EDM03(위험 최적화), EDM04(자원 최적화), EDM05(투명성 보장); **40 Governance & Management Objectives**의 100% Coverage |
| **TOGAF 10 ADM** | 엔터프라이즈 아키텍처 개발 방법론 | **Preliminary Phase -> A~H 8단계** 반복 사이클; **Architecture Repository**(ABBD, ABBs, ARB, Standards, Landscape); **Content Metamodel**로 산출물 정형화 |
| **ITIL 4 SVS** | 서비스 가치 시스템(34개 Practice) | **Service Value Chain**(Plan->Engage->Design&Transition->Obtain/Build->Deliver&Support); **Guiding Principles(7)**: Focus on value, Start where you are, Progress iteratively, etc. |
| **GRC Platform** | 거버넌스-리스크-컴플라이언스 통합 | **RSA Archer / ServiceNow GRC / SAP GRC**; **Policy->Control->Evidence->Issue** 워크플로우; **SOX, GDPR, PCI-DSS** 매핑 자동화 |
| **KPI/BSC 대시보드** | 성과 측정 및 피드백 | **Balanced Scorecard(4 관점)**: 재무/고객/내부/학습성장; **IT4IT Reference Model**(HP)로 E2E IT 가치 흐름 추적 |

**핵심 알고리즘 및 산식**:
- **IT ROI 산정**: ROI = (총 이익 − 총 비용) / 총 비용 × 100; 보다 정교한 **NPV**는 NPV = Σ [CFₜ / (1+r)ᵗ] − I₀, 여기서 r은 할인율(가중평균자본비용 WACC, 통상 7~12%)
- **Real Options Valuation(ROV)**: IT 투자의 유연성 가치를 반영, **Black-Scholes 모델** 적용: C = S·N(d₁) − K·e⁻ʳᵀ·N(d₂)
- **TCO(Total Cost of Ownership)**: TCO = Acquisition + Implementation + Operation + Maintenance + Decommissioning(전 생애주기 비용)
- **CMMI(통합성숙도)**: Level 1(Initial) -> 2(Managed) -> 3(Defined) -> 4(Quantitatively Managed) -> 5(Optimizing); **Process Area(PA) 16~25개
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 797 / 800

<- **이전**: [796. IT 경영 관리 핵심 토픽 796번 시험 요약](/studynote/12_it_management/05_security_compliance/796_it_management_core_topic_796_exam_summary/)
**다음**: [798. IT 경영 관리 핵심 토픽 798번 시험 요약](/studynote/12_it_management/05_security_compliance/798_it_management_core_topic_798_exam_summary/) ->

---
