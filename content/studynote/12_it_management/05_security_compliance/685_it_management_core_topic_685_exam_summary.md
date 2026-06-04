+++
title = "685. IT 경영 관리 핵심 토픽 685번 시험 요약 (IT Management Core Topic 685 Exam Summary)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019는 ISACA가 발표한 차세대 IT 거버넌스 프레임워크로, **40개의 거버넌스/관리 목표를 5개 도메인(EDM·APO·BAI·DSS·MEA) × 7개 컴포넌트(원리·정책·프로세스·조직·정보·인력·문화·기술)** 의 2차원 매트릭스로 구조화하고, **11개 설계 요인(Design Factors)** 을 통해 조직 상황에 맞게 목표 우선순위와 적용 범위를 동적으로 조정하는 컴플라이언스 기반 통합 거버넌스 체계.
> 2. **가치**: (정량) IT 투자 대비 가치 실현률 평균 **20~30% 향상**(ISACA 2022 Survey), 중대 IT 리스크 발생률 **40% 감소**, 감사 지적사항 **60% 감소** / (정성) 이사회-경영진-IT의 3자 정렬(Strategic Alignment), ISO 27001·ISO 20000·NIST CSF·ITIL 4·TOGAF 등 타 프레임워크와 매핑 가능한 **Single Pane of Glass** 제공.
> 3. **판단 포인트**: ①조직의 거버넌스 성숙도(Level 1~5)에 따른 **단계적 로드맵** 수립, ②클라우드·AI·DevOps 등 **신기술 적용 시 영향받는 목표(예: BAI03 Manage Solutions, DSS04 Manage Continuity)** 의 우선 도출, ③Outsourcing/IaaS/PaaS/SaaS **소싱 모델별 RACI 재정의**, ④규제 환경(개인정보보호법, DORA, AI Act)에 따른 **Focus Area 커스터마이징** 여부.

---

## Ⅰ. 개요 및 필요성

COBIT(Control Objectives for Information and Related Technologies)은 1996년 ISACA에서 처음 발표된 이후 COBIT 1.0 -> 2.0 -> 3.0 -> 4.1 -> 5(2012) -> **2019(2018년 11월)** 로 진화해 왔다. 기존 COBIT 5가 **5원리·5도메인·32프로세스·7 Enablers** 구조였다면, COBIT 2019는 **6원리·40 Governance/Management Objectives·11 Design Factors·Focus Areas** 구조로 재설계되어 **유연성·확장성·실용성**을 대폭 강화했다.

배경이 되는 기술적·경영적 과제는 다음과 같다.

- **이중 책임(Gap)의 심화**: 이사회는 IT 거버넌스 책임을 지지만, 실제 IT 의사결정은 전사 산하 IT 조직에 분산되어 있음 (Tractica 2023, IT 의사결정자 평균 17명).
- **규제 복잡도 폭증**: 금융권의 DORA(EU), 바젤 III, 국내 전자금융감독규정, 개인정보보호법, ESG 공시, AI 거버넌스 가이드라인 등 **단일 프레임워크로 매핑 불가**한 규제 다중 적용.
- **클라우드·AI 전환**: 기존 5 Enablers 모델은 IaaS·PaaS·SaaS·MLaaS 환경의 **공유 책임 모델(Shared Responsibility Model)** 과 3rd Party Risk를 명시적으로 다루지 못함.
- **사이버 리스크 정량화**: 평균 침해 비용 **USD 4.45M**(IBM 2023), 랜섬웨어 평균 다운타임 **21일** -> 정량적 Risk Optimization 필요.

```text
       [Before: COBIT 5]                  [After: COBIT 2019]
   +----------------------+         +------------------------------+
   |  • 5 도메인 고정 매핑 |         |  • 11 Design Factors 동적 선정 |
   |  • 32 프로세스 일률   |   ---►  |  • 40 Obj. 중 우선순위 산출   |
   |  • 7 Enablers        |         |  • 7 Components × N 커스텀    |
   |  • 프로세스 중심     |         |  • 목표·컴플라이언스 중심      |
   |  • 1회성 스냅샷 평가  |         |  • Continuous Improvement     |
   |  • 제한된 Focus Area |         |  • DevOps·Cloud·Risk·AI Focus |
   +----------------------+         +------------------------------+
              |                                  |
              v                                  v
       [Limited Adoption]                 [Enterprise-wide GRC]
```

- **📢 섹션 요약 비유**: COBIT 5는 **"정해진 코스 메뉴가 있는 레스토랑"** 이었다면, COBIT 2019는 **"11가지 손님 취향(설계 요인)을 물어보고 40가지 요리(목표) 중 코스를 짜주는 오마카세 셰프"** 와 같다. 손님(조직)이
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 685 / 800

<- **이전**: [684. IT 경영 관리 핵심 토픽 684번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/684_it_management_core_topic_684_exam_summary/)
**다음**: [686. IT 경영 관리 핵심 토픽 686번 시험 요약](/knowledge-base/studynote/12_it_management/05_security_compliance/686_it_management_core_topic_686_exam_summary/) ->

---
