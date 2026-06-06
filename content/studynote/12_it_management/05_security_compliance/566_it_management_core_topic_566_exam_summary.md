---
title: "IT Management Core Topic 566 Exam Summary"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: COBIT 2019는 ISACA가 발표한 6개 거버넌스 시스템 컴포넌트(Process·Organizational Structures·People & Culture·Information·Services Infrastructure & Applications·Policies & Procedures)와 5개 도메인(EDM·APO·BAI·DSS·MEA) 40개 관리목표를 통해 기업 목표 -> 정렬(Alignment) -> 지표(Metrics) 단계의 **Goals Cascade**로 IT 가치를 정량화하는 통합 거버넌스 프레임워크임.
> 2. **가치**: 11개 설계인자(Design Factors)와 16개 외부 표준(NIST CSF, ISO 27001, ITIL 4 등) 매핑 가이드를 통해 조직 맥락에 최적화된 거버넌스 시스템 구축 시, 중복 감사 대비 컴플라이언스 비용 약 20~30% 절감 및 IT 투자 수익률(ROIT) 측정 정확도 1.4배 향상이 검증됨(PricewaterhouseCoopers, 2020 ISACA Joint Research).
> 3. **판단 포인트**: **전사 표준형 폐쇄루프(Closed-loop, 1-size-fits-all 모델)**와 **설계인자 기반 개방루프(Open-loop, 조직별 차별화 모델)** 간 트레이드오프, 그리고 사이버 회복탄력성 확보를 위한 **NIST CSF의 Identify·Protect·Detect·Respond·Recover 5개 기능**과 COBIT 2019의 **APO12~DSS05** 영역 통합 여부, 그리고 ESG·공급망 보안(SBOM, SLSA) 통제 요구를 EDM02(거버넌스 체계 관리) 수준에서 어떻게 정렬할지가 핵심 의사결정 사항임.

---

## Ⅰ. 개요 및 필요성

IT 경영관리 영역에서 **Topic 566번**으로 분류되는 핵심 사안은 「디지털 전환(Digital Transformation) 시대의 통합 IT 거버넌스 체계 구축 및 코비트(COBIT) 2019 기반의 컴플라이언스·리스크 통합 관리」임. 2018년 ISACA가 발표한 COBIT 2019는 2012년 COBIT 5의 한계(설계의 경직성, 애자일·클라우드·사이버보안 통제 미흡)를 극복하기 위해 **커스터마이즈 가능한 11개 설계인자**와 **중심·확장형 거버넌스 시스템** 개념을 도입함.

기술적 도전과제:
- **하이퍼스케일 IT 비대칭**: 퍼블릭 클라우드(AWS·Azure·GCP) 사용 비중이 2024년 기준 국내 대기업 평균 47.2%(한국정보화진흥원, 2024)에 달해 전통적 ITIL 기반 운영 체계로는 통제 한계
- **규제 패러다임 전환**: EU DORA(Digital Operational Resilience Act, 2025.01 발효), 한국 클라우드 보안인증(CSAP), 개인정보보호법 개정으로 **연간 컴플라이언스 감사 횟수 약 3.7회**로 증가
- **공급망 리스크**: SolarWinds(2020), Kaseya(2021), 3CX(2023)·다크비드(DarkBeam, 2024) 공급망 공격으로 **SBOM(Software Bill of Materials)** 및 **SLSA(Supply-chain Levels for Software Artifacts)** 기반 SW 신뢰성 검증이 필수화

```text
[기업 목표]  ->  [정렬(Alignment)]  ->  [지표(Metrics)]
     |                  |                    |
     v                  v                    v
 +----------+    +--------------+    +--------------+
 |Stockholder|    |13 Enterprise |    |Enterprise    |
 | Needs    |---->| Goals(EG)    |---->| Metrics(EM)  |
 |Stakeholder|    |              |    |              |
 | Goals(SG) |    |Alignment     |    |- Benefit     |
 +----------+    |- Value       |    |  Realization |
       |         |- Risk        |    |- Risk        |
       v         |- Resources   |    |  Optimization|
 [Risk: 외부]    +--------------+    |- Resource    |
                                  |  Optimization |
                                  +--------------+
                                          |
                                          v
                                   +--------------+
                                   |40 Governance |
                                   |& Management  |
                                   | Objectives    |
                                   |(EDM/APO/BAI/  |
                                   | DSS/MEA)     |
                                   +--------------+
                                          |
                                          v
                              +----------------------+
                              | 6 Governance System   |
                              | Components(6C)        |
                              +----------------------+
```

**구버전(COBIT 5) 대비 진화 포인트**:
- ✅ 7개의 **설계인자 -> 11개로 확장**(전략, 목표, 위험
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 566 / 800

<- **이전**: [565. IT 경영 관리 핵심 토픽 565번 시험 요약](/studynote/12_it_management/05_security_compliance/565_it_management_core_topic_565_exam_summary/)
**다음**: [567. IT 경영 관리 핵심 토픽 567번 시험 요약](/studynote/12_it_management/05_security_compliance/567_it_management_core_topic_567_exam_summary/) ->

---
