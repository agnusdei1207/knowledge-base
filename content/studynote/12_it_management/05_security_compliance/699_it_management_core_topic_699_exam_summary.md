+++
title = "699. IT 경영 관리 핵심 토픽 699번 시험 요약 (IT Management Core Topic 699 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 699. IT 경영 관리 핵심 토픽 699번 시험 요약
## (IT Management Core Topic 699 — Professional Engineer Exam Summary)

---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 **COBIT 2019 거버넌스 체계, ITIL 4 서비스 가치사슬(SVC), ISO/IEC 38500 이사회 책임 원칙**을 기반으로, **ISP(정보화전략계획) -> EA(엔터프라이즈 아키텍처) -> BPR(업무프로세스 재설계) -> IT 포트폴리오 관리 -> SLA/BSC 기반 성과측정**으로 이어지는 5단계 가치사슬을 통해 **TCO 절감, ROI 극대화, EVA(경제적부가가치) 창출**을 달성하는 경영과학이다.
> 2. **가치**: 정량적으로는 **TCO 20~40% 절감, ROI 15% 이상 확보, MTTR 50% 단축, SLA 가용률 99.95% 이상 달성**, 정성적으로는 **이사회-경영진-현업-IT 정렬(Alignment)**, **규제 준수(Compliance: 개인정보보호법, ISMS-P, GDPR)**, **디지털전환(Industry 4.0) 대응력** 확보.
> 3. **판단 포인트**: **Build vs Buy vs Cloud(Public/Private/Hybrid)**, **Make vs Buy(IaaS/PaaS/SaaS)**, **내부 운영 vs BPO/ITO 아웃소싱**, **단일 거버넌스 프레임워크(COBIT 단독) vs 통합 프레임워크(COBIT+ITIL+ISO38500+PMBOK+ISO27001)**, **Waterfall vs Agile vs DevOps/SRE**, **Capital Expenditure(CapEx) vs Operational Expenditure(OpEx)** 간의 트레이드오프를 **EA 참조모델(TOGAF ADM)**, **거버넌스 설계(람다 아키텍처: EDW+Speed Layer)**, **포트폴리오 다이어그램(Bubble Chart: Value x Risk)** 으로 의사결정한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 시대적 배경과 등장 배경

**1960년대 데이터처리(EDP) -> 1980년대 MIS/DSS -> 1990년대 ERP/EDI/ISP -> 2000년대 SOX Act/BS7799/COBIT -> 2010년대 클라우드/모바일/빅데이터 -> 2020년대 AI/Generative AI/플랫폼 경영/ESG/지속가능경영**으로 IT의 역할이 **"비용센터(COE: Center of Excellence for cost)" -> "전략적 동인(Strategic Enabler)" -> "경영 자체의 운영체제(Business OS)"**로 변화함에 따라, IT를 **단순 자산(asset)이 아닌 서비스 가치사슬(Value Chain)**로 바라보는 패러다임 전환이 필수적이다.

특히 **2024년 이후**에는 **①AI 거버넌스(AI Act/EU, AI 기본계획/한국)**, **②FinOps(클라우드 비용 거버넌스)**, **③제로트러스트(Zero Trust) 보안**, **④ESG 공시(CSRD/ISSB S2)**, **⑤플랫폼 비즈니스 모델(API 경제)** 등 새로운 의사결정 축이 등장하면서, **전통적 IT 관리(코스트센터 관점)** 에서 **데이터·AI·플랫폼 기반의 지능형 경영(Intelligent Enterprise Management)** 으로의 전환이 요구된다.

### 1.2 핵심 문제점(Legacy Paradigm의 한계)

| 구분 | 전통적 IT 관리(Legacy) | 현대적 IT 경영 관리(Modern) |
| :--- | :--- | :--- |
| 관점 | IT = 비용(cost) | IT = 가치(value) & 투자(investment) |
| 구조 | 수직 계층(CEO->CFO->CIO) | 수평 가치사슬(Board->Gov.->EA->PMO->SMO) |
| 방법론 | 수동·정성적·연 1회 | 실시간·정량적·KPI/BSC 대시보드 |
| 아키텍처 | 모놀리식·온프레미스 | 클라우드 네이티브·API·마이크로서비스 |
| 거버넌스 | IT 부서 독점 | COBIT 2019(40 governance/management objectives) 기반 전사 거버넌스 |
| 측정 | 가용성·장애건수 | **Val IT** 기반 포트폴리오 ROI/NPV/IRR, BSC 4관점 |
| 규제 | 컴플라이언스 사후 대응 | ISO 27001/27701/31000/38500 선제적 통합 |

### 1.3 ASCII 아키텍처 다이어그램 — IT 경영 관리 5계층 프레임워크

```text
[Layer 5]  +----------------------------------------------------------+
   거버넌스   |  이사회(Board) -> IT거버넌스위(ITC) -> CISO/CDO/CAIO            |
  (Govern.)  |  표준: ISO/IEC 38500, COBIT 2019 EDM Domain(5개 목표)         |
            +-------------------------+------------------------------------+
                                      | 정책·예산·리스크 한도 배분
                                      v
[Layer 4]  +----------------------------------------------------------+
   전략기획   |  ISP(정보화전략계획) -> EA(TOGAF ADM) -> IT 포트폴리오              |
  (Strategy)|  방법론: Balanced Scorecard, Porters Value Chain, Wardley Maps  |
            |  투자평가: NPV/IRR/EVA/Payback/TCO/ROIC                          |
            +-------------------------+------------------------------------+
                                      | 아키텍처 청사진·RFP·예산 배분
                                      v
[Layer 3]  +----------------------------------------------------------+
   구축·전환   |  BPR(Business Process Reeng.) -> SI/SM(시스템 구축/구축)         |
 (Transform) |  방법론: SDLC, PMBOK 7th, PRINCE2, SAFe, Agile(Scrum)         |
            |  표준: DMBOK, 데이터 거버넌스(데이터 카탈로그/품질/계보)            |
            +-------------------------+------------------------------------+
                                      | SLA 기반 운영 인계
                                      v
[Layer 2]  +----------------------------------------------------------+
   서비스운영  |  ITIL 4 SVS(Service Value System) - 34 Practices                |
  (Operation)|  SLO/SLI/SLA: 가용성 99.95%, MTTR < 30분, MTBF > 720h           |
            |  자동화: AIOps, SRE(Golden Signals: Latency/Traffic/Errors/Saturation)|
            |  클라우드: FinOps·Well-Architected Framework(5 pillars)            |
            +-------------------------+------------------------------------+
                                      | KPI/메트릭 수집·모니터링
                                      v
[Layer 1]  +----------------------------------------------------------+
   측정·개선  |  BSC 4관점(재무/고객/내부/학습성장) + KPI Tree + OKR               |
  (Measure)  |  COBIT 2019: 40 Governance & Management Objectives                |
            |  감사: ISO 27001/27701(정보보호/개인정보), ISMS-P, SOC2 Type II      |
            +----------------------------------------------------------+
```

### 1.4 왜 IT 경영 관리가 필수적인가 (Old vs New Paradigm)

- **Old Paradigm(1990~2010)**: IT는 "**지원부서**"로, 연간 CapEx 예산으로 HW/SW를 구매·유지. **ROI 측정 불가**, 비즈니스 성과와의 **인과관계(causal link) 부재**, **Shadow IT**(현업 우회 구매) 만연 -> **IT 지출의 30~40%가 중복/낭비**(Gartner 2018 리포트).
- **New Paradigm(2010~현재)**: IT는 "**전략적 파트너**"로, **TTM(Time-to-Market)**, **고객 경험(CX/NPS)**, **데이터 기반 의사결정**의 핵심. **클라우드·API·AI**가 **자본적 지출(CapEx)을 운영적 지출(OpEx)**, 그리고 **사용량 기반(consumption-based)** 모델로 전환 -> **FinOps** 등장.
- **필수성**: ①**ISO 38500** 이사회 거버넌스 의무화, ②**클라우드 전환**(2025년 글로벌 SaaS 시장 $200B) -> **표준 거버넌스·비용통제·보안 필수**, ③**규제 강화**(GDPR 위반 과징금 20M€ 또는 매출의 4%, 개인정보보호법 위반 5억원 이하 과징금), ④**생성형 AI**로 인한 **AI 거버넌스·윤리·저작권** 리스크 -> **AI Risk Management Framework(ISO/IEC 42001, NIST AI RMF)** 필요.

### 📢 섹션 요약 비유

> IT 경영 관리는 **"스마트시티의 도시계획"**과 같다. 도로·상하수도·전력·통신(인프라) -> 건물 배치·용도지역(아키텍처) -> 시민 서비스·치안·소방(운영) -> 민원·교통량·환경 데이터(측정) -> 도시 재개발·마스터플랜(거버넌스)이 **상호 연결된 메타시스템**이듯, IT도 **5계층(거버넌스·전략·구축·운영·측정)**이 끊김 없이 흘러야 **도시(기업)**가 정상 작동한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 IT 경영 관리의 5대 핵심 구성 요소

```text
+----------------------------------------------------------------------+
|                       IT 경영 관리 5대 구성요소                        |
+----------------------------------------------------------------------+
                                |
        +-----------------------+-----------------------+
        v                       v                       v
  +----------+            +----------+            +----------+
  | 거버넌스   |            | 전략 기획  |            | 서비스   |
  |Governance|            | Strategy  |            | 운영      |
  |          |            |          |            | Operation|
  +-----+----+            +-----+----+            +-----+----+
        |                       |                       |
        | COBIT 2019            | ISP(정보화전략)        | ITIL 4 SVS
        | ISO 38500            | TOGAF ADM             | SRE Practices
        | ISO 27001            | BSC/Val IT            | FinOps Framework
        |                      | Zachman EA            | AIOps
        |                      |                      |
        +----------+-----------+-----------+-----------+
                   v                       v
              +----------+            +----------+
              |  아키텍처  |            |  성과측정  |
              |   EA     |            |Measuremnt|
              +----------+            +----------+
                   |                       |
                   | TOGAF, FEAF,         | BSC, KPI, OKR
                   | DoDAF, Zachman
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 699 / 800

<- **이전**: [698. IT 경영 관리 핵심 토픽 698번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/698_it_management_core_topic_698_exam_summary/)
**다음**: [700. IT 경영 관리 핵심 토픽 700번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/700_it_management_core_topic_700_exam_summary/) ->

---
