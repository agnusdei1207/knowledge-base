---
title: "IT 거버넌스 (IT Governance & COBIT/ISO 38500)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-law_policy"
weight: 5
---

# 1. 한눈에 보는 IT 거버넌스
- **정의**: 기업의 IT가 비즈니스 목표를 달성할 수 있도록 이사회와 경영진이 통제하고 지휘하는 일련의 프로세스, 조직 구조, 리더십 체계.
- **필요성**: IT 투자의 낭비 방지, IT 리스크(보안 침해, 장애 등) 관리, IT의 비즈니스 가치 창출(Value Delivery) 극대화.
- **핵심 직관**: "IT의 헌법과 경찰." 개발자가 마음대로 시스템을 고치고, 부서장이 자기 예산으로 아무 SW나 사는 것을 막고, "회사의 방향성에 맞게, 정해진 룰(표준)에 따라 IT를 운영하라"고 통제하는 최고 수준의 관리 체계입니다.

# 2. 깊이 이해하기: IT 거버넌스의 양대 산맥 (ISO 38500 vs COBIT)

IT 거버넌스를 어떻게 구축할 것인가? 백지에서 시작할 수 없으니 글로벌 표준 프레임워크를 가져다 씁니다. 대표적인 두 가지가 ISO 38500(국제 표준)과 COBIT(실무 프레임워크)입니다.

## 2.1 ISO/IEC 38500 (상위 수준의 원칙)
이사회(경영진)가 IT를 어떻게 다뤄야 하는지 알려주는 **'6대 원칙'**과 **'3대 모델'**입니다. (매우 추상적이고 철학적임)
- **3대 모델 (EDM)**: 
  1. **E**valuate (평가): IT 현황과 미래 비전 평가
  2. **D**irect (지시): IT 전략과 정책 수립 및 지시
  3. **M**onitor (모니터링): 지시대로 잘 되는지 성과/위험 모니터링
- **6대 원칙**: 책임(Responsibility), 전략(Strategy), 획득(Acquisition), 성과(Performance), 준거성(Conformance), 행동(Human Behavior).

## 2.2 COBIT (Control Objectives for Information and Related Technology)
ISACA에서 만든 프레임워크로, ISO 38500이 '무엇을 해야 하는지(What)' 알려준다면 COBIT은 '어떻게 구체적으로 통제할 것인지(How)'를 알려주는 방대한 가이드북입니다. 최신 버전은 **COBIT 2019**입니다.

### COBIT 2019의 핵심 (거버넌스와 관리의 분리)
COBIT은 "거버넌스(이사회 역할)"와 "관리(경영진/IT부서 역할)"를 명확히 분리합니다.
1. **거버넌스 영역 (EDM)**: Evaluate, Direct, Monitor (ISO 38500과 동일)
2. **관리 영역 (APO, BAI, DSS, MEA)**:
   - **APO** (Align, Plan, Organize): IT 기획 및 조직화
   - **BAI** (Build, Acquire, Implement): 개발 및 도입
   - **DSS** (Deliver, Service, Support): 서비스 운영 및 지원 (ITIL 영역)
   - **MEA** (Monitor, Evaluate, Assess): 관리적 모니터링 및 평가

> **💡 COBIT 2019의 진화**: 과거 COBIT 5가 고정된(One-size-fits-all) 프레임워크였다면, 2019 버전은 '디자인 팩터(Design Factors)'를 도입하여 기업 규모나 산업 특성에 맞게 거버넌스 체계를 테일러링(Tailoring)할 수 있게 되었습니다.

# 3. 관련 키워드와 연결 서사
- **ITIL / ITSM**: COBIT이 IT 전체를 통제하는 '법률'이라면, ITIL은 IT 서비스를 고객에게 제공하고 운영하는(DSS 영역) '서비스 매뉴얼'입니다.
- **EA (엔터프라이즈 아키텍처)**: 거버넌스가 IT 자산을 통제하기 위해 기준으로 삼는 도면(청사진)이 바로 EA입니다.
- **컴플라이언스 (Compliance)**: 거버넌스가 제대로 작동해야 GDPR, 개인정보보호법 등 외부 법규(준거성)를 어기지 않습니다.

---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **IT 거버넌스** | 이사회·경영진이 IT를 지휘·통제·평가하는 의사결정 프레임워크 | IT의 헌법과 경찰 |
| **COBIT** | ISACA가 만든 IT 통제 목적 실무 프레임워크(Control Objectives for Information and Related Technology) | IT 통제용 상세 법률 시행령 |
| **ISO 38500** | 이사회 관점의 IT 거버넌스 국제 표준(EDM 모델 + 6대 원칙) | IT 헌법의 기본 조항 |
| **EDM** | 평가(Evaluate)→지시(Direct)→모니터링(Monitor) 순환 거버넌스 모델 | 계획-지시-점검의 경영 사이클 |
| **Design Factor** | COBIT 2019에서 기업 특성에 맞게 거버넌스를 맞춤화하는 변수 | 체형에 맞는 맞춤 정장 |

---

# ✍️ 【답안용】 핵심 골격 및 인사이트

## Ⅰ. 비즈니스 가치 창출과 리스크 통제의 핵심, IT 거버넌스의 개요
- **본질**: 기업의 목표 달성을 위해 이사회 및 경영진이 IT 자원을 지휘(Direct), 통제(Control), 평가(Evaluate)하는 책임 및 의사결정 프레임워크.
- **목적 (5대 영역)**: 비즈니스 연계(Strategic Alignment), 가치 전달(Value Delivery), 리스크 관리(Risk Management), 자원 관리(Resource Management), 성과 측정(Performance Measurement).

## Ⅱ. IT 거버넌스의 글로벌 국제 표준, ISO/IEC 38500
- **개념**: 이사회의 책임을 강조한 IT 거버넌스 최고 지침.
- **3대 모델 (EDM 프레임워크)**: Evaluate(평가) → Direct(지시) → Monitor(모니터링)의 순환 구조.
- **6대 핵심 원칙**:
  1. **책임 (Responsibility)**: IT 결정에 대한 명확한 책임 할당
  2. **전략 (Strategy)**: 비즈니스와 IT 전략의 정렬
  3. **획득 (Acquisition)**: 투명한 IT 투자 및 획득 프로세스
  4. **성과 (Performance)**: 요구되는 IT 서비스 성과 보장
  5. **준거성 (Conformance)**: 법/규제 및 내부 정책 준수
  6. **행동 (Human Behavior)**: 인적 요소 및 문화 존중

## Ⅲ. 실무적 통제 프레임워크, COBIT 2019의 아키텍처
- **변화의 핵심**: 기업 환경(Agile, Cloud 등)에 맞춤화 가능한 동적 거버넌스 시스템(Design Factors & Focus Area 도입).
- **거버넌스와 관리의 명확한 분리 (Governance vs Management)**:
  - **Governance (이사회/주주)**: EDM (평가-지시-모니터링)
  - **Management (CEO/CIO)**: 
    - **APO** (Align, Plan, Organize) - 기획
    - **BAI** (Build, Acquire, Implement) - 구축
    - **DSS** (Deliver, Service, Support) - 운영
    - **MEA** (Monitor, Evaluate, Assess) - 평가

## Ⅳ. COBIT 2019 거버넌스 시스템의 6대 핵심 원칙
1. 이해관계자 가치 제공 (Provide Stakeholder Value)
2. 전체적 접근 (Holistic Approach)
3. 동적 거버넌스 시스템 (Dynamic Governance System)
4. 거버넌스와 관리의 분리 (Governance Distinct from Management)
5. 기업 맞춤형 (Tailored to Enterprise Needs)
6. 종단간 적용 (End-to-End Governance System)

## Ⅴ. IT 거버넌스와 타 프레임워크(EA, ITIL, ISMS) 간의 포지셔닝
```text
[ IT 거버넌스 (COBIT, ISO 38500) ]  ◄─ 이사회/경영진 (방향 제시 및 통제)
                │
                ▼
[ 기획/설계 ]   EA (TOGAF), ISP     ◄─ 아키텍트/기획자 (구조 및 전략)
[ 구축/개발 ]   CMMI, Agile, PMBOK  ◄─ 개발자/PM (품질 및 일정)
[ 서비스/운영 ] ITIL, ITSM          ◄─ 운영자/서비스 데스크 (가용성 및 장애)
[ 보안/통제 ]   ISMS, ISO 27001     ◄─ 보안관리자 (기밀성, 무결성)
```

## Ⅵ. 최신 거버넌스 트렌드 제언
- **Digital Governance로의 확장**: 단순한 IT 인프라 통제를 넘어, AI, 빅데이터, IoT 등 파괴적 기술(Disruptive Tech)의 윤리적 사용과 리스크를 통제하는 디지털(데이터) 거버넌스로 진화 중.
- **Agile 거버넌스 체계**: 무겁고 통제 위주의 승인 프로세스에서 벗어나, DevSecOps 환경을 지원하는 '자동화된 준거성 검사(Compliance as Code)' 도입 필요.

> **💡 작성 팁 (문제 유형별 목차 전환)**
> - **'ISO 38500' 단독 출제**: Ⅱ의 3대 모델(EDM)과 6대 원칙을 상세히 서술하고, 이사회 관점의 철학을 강조.
> - **'COBIT 2019' 단독 출제**: Ⅲ의 5개 도메인(EDM, APO, BAI, DSS, MEA)을 도식화하고, Ⅳ의 6대 원칙(특히 Tailoring, Dynamic)을 부각.
> - **'거버넌스, ITSM, EA 관계'**: Ⅴ의 프레임워크 간 포지셔닝 맵을 그려주면 채점자에게 '숲을 보는 시각'을 강력하게 어필할 수 있음.
