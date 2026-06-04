+++
title = "552. IT 경영 관리 핵심 토픽 552번 시험 요약 (IT Management Core Topic 552 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: IT 경영 관리는 COBIT 2019의 EDM-APO-BAI-DSS-MEA 5개 도메인과 40개 거버넌스/관리 목표(Governance & Management Objectives) 체계 하에서, RACI 매트릭스(Responsible, Accountable, Consulted, Informed)와 11개 설계 인자(Design Factors)를 통해 비즈니스-IT 정렬(Business-IT Alignment)과 가치 실현(Value Realization)을 달성하는 통합 의사결정 프레임워크임
> 2. **가치**: COBIT 기반 성숙도 Level 2->4 도달 시 IT 투자 ROI 평균 23% 향상(ISACA 2023), IT 프로젝트 성공률 28%->72%(Standish CHAOS 2020), 컴플라이언스 위반 비용 80% 절감 및 SOX/ISMS-P 인증심사 시간 65% 단축, MTTR(Mean Time To Recover) 58% 감소
> 3. **판단 포인트**: 거버넌스 운영 모델(Centralized vs Federated vs Hybrid) 선택 시 조직 규모·산업 규제 강도·사업부 자율성 간의 트레이드오프 분석, 프레임워크 통합(COBIT+ITIL4+ISO 27001+TOGAF) 시 중복 프로세스 제거·아티팩트 매핑·키 인디케이터(KGI/KPI) 연계 전략, 거버넌스 시스템(시스템) vs 거버넌스 프레임워크(템플릿) 경계 설정이 도입 성패 결정

---

## Ⅰ. 개요 및 필요성

정보기술이 경영 핵심 인프라로 자리 잡으면서, IT 투자의 약 30%가 비즈니스 가치 없이 낭비되는 **"IT Value Gap"** 문제가 대두되고 있음(McKinsey 2022). 기술사 관점에서 IT 경영 관리는 단순한 시스템 운영이 아닌 **"IT 의사결정권, 책임구조, 성과측정 체계를 포괄하는 기업 거버넌스의 하위 체계"**로 정의됨. 특히 클라우드 전환(Public/Private/Hybrid), AI/ML 도입, Zero Trust 보안 패러다임, ESG 컴플라이언스 등 복잡성이 기하급수적으로 증가하면서, 단일 부서의 통제를 벗어난 **"Enterprise-wide IT Governance"** 체계가 필수적임.

```text
+------------------------------------------------------------------------------+
|           IT 경영 관리 (IT Management & Governance) 4-Layer 모델            |
+------------------------------------------------------------------------------+
|                                                                              |
|  +--------------------------------------------------------------------+     |
|  | Layer 1: 기업 거버넌스 (Corporate Governance)                       |     |
|  |   +----------+  +----------+  +----------+  +----------+          |     |
|  |   | 이사회   |  | CEO/COO  |  |CFO/CRO   |  |CAO/CHRO  |          |     |
|  |   |(Board)   |  |(집행)     |  |(재무/리스크)|(감사/인사)|         |     |
|  |   +----+-----+  +----+-----+  +----+-----+  +----+-----+          |     |
|  +--------+-------------+-------------+-------------+----------------+     |
|           +-------------+-----+--------+-------------+                      |
|                                v IT 전략 연계                                |
|  +--------------------------------------------------------------------+     |
|  | Layer 2: IT 거버넌스 (IT Governance) - COBIT 2019                  |     |
|  |   +--------------------------------------------------------+       |     |
|  |   | 5개 도메인: EDM(평가·지휘·모니터링) | APO(정렬·계획·조직)|       |     |
|  |   |             BAI(빌드·구축·구현) | DSS(서비스·지원)     |       |     |
|  |   |             MEA(모니터링·평가·자문)                     |       |     |
|  |   | 40개 목표(Governance 5 + Management 35)                |       |     |
|  |   | 11개 설계 인자(Design Factors) - 전략, 목표, 위험, 역할|       |     |
|  |   | 7개 컴포넌트: 원칙, 목표, 목적-계단, 지표, 위험, 인맥 |       |     |
|  |   +--------------------------------------------------------+       |     |
|  +--------------------------------------------------------------------+     |
|                                v                                            |
|  +--------------------------------------------------------------------+     |
|  | Layer 3: IT 관리 (IT Management) - ITIL 4 + PMBOK 7                 |     |
|  |   +----------------+-----------------+--------------------+        |     |
|  |   | Service Value  | 34 Practice      | SVS(서비스 가치    |        |     |
|  |   | Chain(SVC)     | (개념/일반/특화) | 체계) | 4P Model  |        |     |
|  |   +----------------+-----------------+--------------------+        |     |
|  |   +--------------------------------------------------------+       |     |
|  |   | 프로젝트 관리: 5 Process Groups + 10 Knowledge Areas    |       |     |
|  |   | + 8 Performance Domains (PMBOK 7
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 552 / 800

<- **이전**: [551. IT 경영 관리 핵심 토픽 551번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/551_it_management_core_topic_551_exam_summary/)
**다음**: [553. IT 경영 관리 핵심 토픽 553번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/553_it_management_core_topic_553_exam_summary/) ->

---
