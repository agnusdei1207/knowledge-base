---
title: "TOGAF ADM Architecture Development Method"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

# 413. TOGAF ADM 아키텍처 개발 방법론 (TOGAF ADM Architecture Development Method)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TOGAF ADM은 The Open Group의 엔터프라이즈 아키텍처 프레임워크(EAF) 핵심 절차로, **Preliminary + Phase A~H + Requirements Management**의 10단계 반복적(Iterative) 사이클을 통해 비즈니스·데이터·애플리케이션·기술 4개 도메인의 Baseline/Target/Transition 아키텍처를 도출하고, **Architecture Content Framework(메타모델·산출물·빌딩블록)**, **Enterprise Continuum(Foundation~Architectural~Solutions)**, **Architecture Repository(ADM/Integration/Standards/Governance/Methodology/Landscape/Governance/Development/Transition/Architecture Capability)** 3대 구조로 EA 성숙도를 고도화하는 방법론이다.
> 2. **가치**: 전 세계 **Forbes Global 2000의 80% 이상**(The Open Group 2018 발표)이 채택, ISO/IEC/IEEE 42010 아키텍처 명세 국제 표준 기반, **중복 투자 30~40% 절감, 프로젝트 실패율 50%->15%로 감소, Time-to-Market 평균 25% 단축**(Forrester 2017), EA 성숙도 L2(Opportunistic)에서 L4/5(Integrated/Optimized)로 이행 시 **ROI 5.7배**(McKinsey 2020) 정량 효과 검증.
> 3. **판단 포인트**: 조직의 **EA 성숙도(CMMI-EA Level 1~5)**와 프로젝트의 **Scope(Enterprise/Domain/Capability)·Timebox(Iteration Depth)**에 따라 ADM Cycle 깊이를 결정해야 하며, **Phase B~D의 Architecture Building Block(ABB) -> Solution Building Block(SBB) 매핑 비율**(목표 70% 이상 재사용), **Architecture Repository 거버넌스 체계**(READ-WRITE-DELETE 권한 분리), **ArchiMate 3.1/Open Exchange Standard**와의 매핑 정합성이 기술사 핵심 판단 포인트이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 정의 및 등장 배경

TOGAF(The Open Group Architecture Framework)는 1995년 The Open Group(IBM, HP, Sun, Philips, Nortel 등 5사가 결성한 산업 컨소시엄)의 전신인 **Open Group Architecture Framework(OGAF)**에서 출발하여 2002년 8.0 기업판 출시, 2009년 9.0으로 **ADM 정형화**, 2018년 9.2에서 **Business Capability**와 **Value Stream** 개념 강화, 2022년 **10th Edition(TOGAF Standard)**에서 **Digital Enterprise, Agile EA, Sustainability, Microservices, Risk/Security** 영역 확장이 이루어졌다.

핵심 정체성은 **"EA를 만드는 '방법(How)'을 표준화"**한 점이다. Zachman Framework가 5W1H 기반의 **분류 체계(Ontology)**만 제공한다면, TOGAF는 **개발·관리·거버넌스 절차**를 10단계 사이클로 명시한다.

### 1.2 등장 배경 — 왜 EA 방법론이 필요한가

```text
[기존 아키텍처 접근법의 한계]
  +--------------------------------------------------------------+
  |  부서별 사일로(Department Silo) 아키텍처                       |
  |   +- 영업: 자체 CRM (Siebel/Salesforce)                       |
  |   +- 제조: 자체 MES (Siemens/AVEVA)                           |
  |   +- 물류: 자체 WMS (Manhattan/Blue Yonder)                   |
  |   +- IT 운영: 자체 DC, 자체 표준 (Cisco/VMware)               |
  |                                                              |
  |  -> 비즈니스-IT 정렬(Business-IT Alignment) 부재              |
  |  -> 중복 투자: 동일 고객 데이터가 CRM·ERP·WMS에 분산           |
  |  -> 기술 부채(Technical Debt) 누적: 78% 기업이 핵심시스템 10년+ |
  +--------------------------------------------------------------+
                              |
                              v
[엔터프라이즈 아키텍처 프레임워크(EAF)의 필요성]
  +--------------------------------------------------------------+
  |  표준화된 방법론으로 전체 조직의 아키텍처를 통합 관리             |
  |   +- Business-Driver -> Architecture -> Solution 연계          |
  |   +- Baseline(현황) -> Target(목표) -> Transition(전환)         |
  |   +- Stakeholder Concern을 4개 View(Viewpoint)로 분리 응답    |
  +--------------------------------------------------------------+
                              |
                              v
[TOGAF ADM의 등장 — "어떻게(How) EA를 만들 것인가"]
  +--------------------------------------------------------------+
  |  TOGAF = { ADM (개발방법론) + ACF (Content, 산출물 정의)      |
  |         + Continuum (재사용 분류) + Repository (저장구조)      |
  |         + Capability (조직/역할) + Guidelines(기법) }         |
  |                                                              |
  |  ISO/IEC/IEEE 42010:2011/2017 "Systems and software          |
  |  engineering — Architecture description" 국제 표준 채택       |
  +--------------------------------------------------------------+
```

### 1.3 패러다임 비교 — 구세대 vs 신세대

| 구분 | 구(舊) 아키텍처 접근법 | TOGAF ADM 신(新) 접근법 |
|:---|:---|:---|
| **범위** | 단일 프로젝트/시스템 | Enterprise-Wide(전사) + Capability/Capability Increment 단위 분할 |
| **방법론** | Waterfall, 문서 중심 | Iterative Cycle, 단계별 **Iteration Declaration**(수행 깊이 명시) |
| **산출물** | 자유 양식, PPT/Word | **Architecture Content Framework**(메타모델·델리버러블·빌딩블록 표준) |
| **거버너** | 사후 검토 | **Phase G Implementation Governance + Phase H Change Mgmt** 상시 |
| **표준 연계** | 사내 표준 | ISO/IEC/IEEE 42010, ArchiMate 3.1, BPMN 2.0, UML 2.5 |
| **변화 대응** | 3~5년 단위 갱신 | **Architecture Change Management**(실시간 변경 영향 분석) |

- **📢 섹션 요약 비유**: ADM은 도시의 **종합도시계획(Comprehensive Urban Plan)**과 같다. 한 채의 집만 짓는 게 아니라 도시 전체(Enterprise)의 토지이용·교통·환경·에너지 계획을 **설계(Phase A~D) -> 시행계획(Phase E~F) -> 감리(Phase G) -> 변경관리(Phase H)**로 반복하며 점진적으로 고도화한다. 종합계획 없이 개별 건물을 짓는 것이 옛 방식, TOGAF ADM은 도시계획을 통해 50~100년 도시의 지속가능성을 확보하는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 ADM 10단계 사이클 전체 구조

```text
                       [ Preliminary Phase ]
                       Architecture Capability 정의
                       TOGAF Library, Repository 초기화
                                |
                                v
   +--------------------------------------------------------------+
   |  Phase A : Architecture Vision                              |
   |   - Architecture Vision 작성, 이해관계자 매핑                  |
   |   - Statement of Architecture Work(SOW) 승인 요청            |
   |   - Iteration/Capellation 범위 확정                            |
   +----------------+---------------------------------------------+
                    v
   +--------------------------------------------------------------+
   |  Phase B : Business Architecture                             |
   |   - 조직·역할·기능·프로세스 Baseline/Target                    |
   |   - Business Capability Map, Value Stream, Heat Map         |
   |   - TOGAF 표준: Business Scenarios, Event/Org/Func Decompose |
   +----------------+---------------------------------------------+
                    v
   +--------------------------------------------------------------+
   |  Phase C : Information Systems Architectures                 |
   |   +----------------------+-------------------------------+   |
   |   | C1. Data Architecture| C2. Application Architecture  |   |
   |   | - 논리/물리 데이터    | - 논리/물리 앱 컴포넌트       |   |
   |   | - Data Entity, LDS   | - App Portfolio, Interface    |   |
   |   | - Master/Reference   | - Application Function Matrix |   |
   |   | - 데이터 거버넌스     | - API/Service Catalog         |   |
   |   +----------------------+-------------------------------+   |
   +----------------+---------------------------------------------+
                    v
   +--------------------------------------------------------------+
   |  Phase D : Technology Architecture                           |
   |   - 하드웨어/소프트웨어/네트워크 플랫폼 Baseline/Target        |
   |   - TOGAF 표준: TRM(Technical Reference Model) 매핑           |
   |   - 클라우드/컨테이너/IoT/Edge 컴퓨팅 등 신기술 반영         |
   +----------------+---------------------------------------------+
                    v
   +--------------------------------------------------------------+
   |  Phase E : Opportunities & Solutions                         |
   |   - Gap Analysis -> Work Package, Project List                |
   |   - 솔루션 후보 평가(비용·위험·편익 ROI/IRR/NPV)              |
   |   - Architecture Building Block(ABB) -> Solution BB(SBB) 매핑 |
   +----------------+---------------------------------------------+
                    v
   +--------------------------------------------------------------+
   |  Phase F : Migration Planning                                |
   |   - Implementation & Migration Strategy                      |
   |   - Architecture Roadmap + Transition Architecture          |
   |   - 마일스톤·의존성·리스크 일정 수립                            |
   +----------------+---------------------------------------------+
                    v
   +--------------------------------------------------------------+
   |  Phase G : Implementation Governance                         |
   |   - 이행 프로젝트 감시·제어                                   |
   |   - Architecture Contract, Compliance
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 413 / 800

<- **이전**: [412. EA 엔터프라이즈 아키텍처 프레임워크](/studynote/12_it_management/05_security_compliance/412_ea_enterprise_architecture_framework/)
**다음**: [414. ArchiMate 아키텍처 모델링 언어](/studynote/12_it_management/05_security_compliance/414_archimate_architecture_modeling_language/) ->

---
