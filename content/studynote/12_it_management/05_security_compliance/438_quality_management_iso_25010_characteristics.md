---
title: "Quality Management ISO 25010 Characteristics"
date: "2026-05-09"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ISO/IEC 25010은 소프트웨어 제품의 품질을 **8대 특성(기능 적합성, 성능 효율성, 호환성, 사용성, 신뢰성, 보안성, 유지보수성, 이식성)**과 그 하위 31개 세부 특성으로 분해하여 정량·정성 측정이 가능한 메트릭 체계로 정의한 국제 표준 품질 모델(SQuaRE 시리즈의 핵심)이다.
> 2. **가치**: 품질 특성을 정형화함으로써 **결함 비용 곡선(1:10:100 규칙)**을 적용한 조기 결함 제거, 계약서/SLA의 객관적 검증 기준 제공, CMMI·SPICE 등 성숙도 모델과의 매핑을 통한 인증·감사 효율성 극대화 효과를 얻는다.
> 3. **판단 포인트**: 측정 가능성(Measurability)과 구현 비용 사이의 **가치-비용 트레이드오프**, 도메인별(임베디드·웹·AI/ML) 가중치 차등 적용, 그리고 "Quality in Use" 5개 특성(효과성·효율성·만족도·위험 회피·상황 완전성)과 "Product Quality" 8개 특성의 균형 있는 통합 설계가 핵심 의사결정 포인트다.

---

## Ⅰ. 개요 및 필요성

소프트웨어 품질은 본질적으로 **다차원(Multi-dimensional)·주관성·맥락 의존성**이라는 세 가지 난제를 갖는다. 1991년 제정된 **ISO/IEC 9126**은 이 문제를 정형화하려는 최초의 시도였으나, "유지보수성"과 "이식성"의 중복, "보안성"의 미반영, 그리고 사용 맥락(Quality in Use) 미고려라는 한계로 2011년 **ISO/IEC 25010:2011(SQuaRE – Systems and software Quality Requirements and Evaluation)**로 전면 개정되었다. 이후 2024년 마이너 개정을 거쳐 보안성·유연성·상호운용성 등 현대 클라우드·AI 환경에 부합하는 **ISO/IEC 25010:2024**가 발표되어 현재 SW 품질 평가의 글로벌 디팩토 표준이 되었다.

기존 패러다임은 "버그가 없으면 좋은 소프트웨어"라는 **결함 중심 관점**이었으나, ISO 25010은 **"사용자의 목표 달성 맥락"**까지 품질의 범위를 확장했다. ISO/IEC 25040(품질 요구사항), 25030(품질 요구사항 엔지니어링), 25020(측정 참조 모델), 25012(데이터 품질)와 함께 **SQuaRE 계열 14개 표준**을 구성하며, 소프트웨어 수명주기(SDLC) 전 단계에서 공통 언어(Common Vocabulary)를 제공한다.

```text
[ISO 25010 도입 배경 및 위치도]
                              +-----------------------------+
                              |   사용자/이해관계자 요구사항  |
                              |  (User / Stakeholder Needs)  |
                              +--------------+--------------+
                                             | 25030
                                             v
   +----------------------------------------------------------------+
   |                SQuaRE (ISO/IEC 25000 시리즈)                    |
   |  +--------------+   +--------------+   +--------------------+  |
   |  | 25010 품질   |   | 25040 품질   |   | 25020/25021/25022 |  |
   |  |   모델 정의   |◄--+  요구사항    |--►|   측정 참조 모델   |  |
   |  +------+-------+   +--------------+   +----------+---------+  |
   |         |                                          |            |
   |         | 25012 (데이터 품질) / 25030 (요구사항)   |            |
   |         v                                          v            |
   |   +------------------------------------------------------+     |
   |   |         Quality Model  <-->  Quality Measure            |     |
   |   |   (8대 특성 + 31개 세부특성)    (정량적 측정 항목)        |     |
   |   +------------------------------------------------------+     |
   +---------------------+------------------------------------------+
                         |  25023 / 25024 (측정 절차)
                         v
   +--------------------------------------------------------------+
   |   평가 결과 -> CMMI / SPICE / ISO 9001 / SLA / 계약서 조항     |
   +--------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: ISO 25010은 마치 자동차의 **종합 품질 검진 체크리스트**와 같다. 과거에는 "시동이 걸리면 OK"로 충분했다면, 지금은 "연비·안전성·승차감·소음·내구성·친환경성" 등 8개 카테고리 31개 항목을 표준화된 측정 장비로 점검하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ISO/IEC 25010의 품질 모델은 **두 개의 축**으로 구성된다. 첫 번째는 **Product Quality Model(제품 품질)** 8개 특성과 두 번째 수준의 세부 특성들, 두 번째는 **Quality in Use Model(사용 시 품질)** 5개 특성이다. 이 모델은 ISO/IEC 25010:2024에서 보안성(Security)이 7개 세부 특성으로 확장되고, 상호운용성·유연성·안전성이 강화된 형태로 발전했다.

```text
[ISO/IEC 25010:2011/2024 품질 모델 트리 구조]

ROOT: Software Product Quality
+-- 1. Functional Suitability (기능 적합성)
|   +-- Functional Completeness   (기능 완전성)
|   +-- Functional Correctness    (기능 정확성)
|   +-- Functional Appropriateness(기능 적합성)
|
+-- 2. Performance Efficiency (성능 효율성)
|   +-- Time Behavior        (시간 반응성)
|   +-- Resource Utilization (자원 활용도)
|   +-- Capacity             (용량/처리량)
|
+-- 3. Compatibility (호환성)
|   +-- Co-existence         (공존성)
|   +-- Interoperability     (상호운용성)
|
+-- 4. Usability (사용성)
|   +-- Appropriateness Recognizability (인식 적합성)
|   +-- Learnability         (학습 용이성)
|   +-- Operability          (조작성)
|   +-- User Error Protection(사용자 오류 방지)
|   +-- User Interface Aesthetics (UI 심미성)
|   +-- Accessibility        (접근성)
|
+-- 5. Reliability (신뢰성)
|   +-- Maturity             (성숙도)
|   +-- Availability         (가용성)
|   +-- Fault Tolerance      (결함 허용성)
|   +-- Recoverability       (복구 가능성)
|
+-- 6. Security (보안성)
|   +-- Confidentiality      (기밀성)
|   +-- Integrity            (무결성)
|   +-- Non-repudiation      (부인방지)
|   +-- Authenticity         (진위확인)
|   +-- Accountability       (책임추적성)
|   +-- Resistance (2024)    (저항성)
|   +-- Identity (2024)      (식별성)
|
+-- 7. Maintainability (유지보수성)
|   +-- Modularity           (모듈성)
|   +-- Reusability          (재사용성)
|   +-- Analyzability        (분석 용이성)
|   +-- Modifiability        (수정 용이성)
|   +-- Testability          (시험 용이성)
|
+-- 8. Portability (이식성)
    +-- Adaptability         (적응성)
    +-- Installability       (설치 용이성)
    +-- Replaceability       (대체 용이성)

[Quality in Use Model: 사용 시 품질]
+-- Effectiveness          (효과성)
+-- Efficiency              (효율성)
+-- Satisfaction            (만족도)
|   +-- Usefulness
|   +-- Trust
|   +-- Pleasure
|   +-- Comfort
+-- Freedom from Risk       (위험 회피)
|   +-- Economic Risk
|   +-- Health & Safety Risk
|   +-- Environmental Risk
+-- Context Coverage        (상황 완전성)
    +-- Context Completeness
    +-- Context Flexibility
```

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Quality Model (품질 모델)** | 8대 특성·31개 세부 특성을 계층적으로 정의하여 품질의 **분해 구조(WBS)** 제공 | McCall·Boehm·FURPS를 통합한 트리 구조, 가중치·평점 스케일(0~5 또는 0~1) 부여 |
| **Quality Measure (품질 측정)** | 각 세부 특성을 **정량 메트릭**으로 변환 (예: MTBF, 응답시간 p95, Cyclomatic Complexity) | ISO/IEC 25021·25022·25023 표준이 측정 함수(Measure Function)와 측정 방법 제공, GQM(Goal-Question-Metric) 패턴 활용 |
| **Quality Requirement (품질 요구사항)** | 사용자·이해관계자 니즈를 SQuaRE 형식의 **측정 가능한 요구사항**으로 변환 | ISO/IEC 25030(품질 요구사항 엔지니어링), SMART 원칙 + Stekeholder-Priority 매트릭스 |
| **Quality Evaluation (품질 평가)** | 측정값을 기반으로 점수 산출·등급 판정·인증 | ISO/IEC 25040(평가 프로세스), AHP(Analytic Hierarchy Process)를 통한 가중치 산정, 베이지안 네트워크로 불확실성 모델링 |

**핵심 원리: 측정 가능성(Measurability) 원칙**
- 모든 품질 특성은 **측정 함수(Measure Function)**: M = f(x₁, x₂, ..., xₙ)으로 표현 가능해야 한다.
- 예: "신뢰성·가용성(Availability)" -> M = MTBF / (MTBF + MTTR), 목표치: 99.95% (연간 다운타임 ≤ 4.38시간)
- "유지보수성·분석 용이성" -> 평균 결함 분석 시간, Cyclomatic Complexity(≤10 권장)
- "보안성·기밀성" -> OWASP Top 10 매핑 결함 수, CVSS 점수 가중 평균
- "성능 효율성·시간 반응성" -> 응답시간 p50, p95, p99 백분위 수(예: p95 < 200ms)

**가중치 산정 모델**: 도메인별로 특성 가중치가 다르다. 금융 시스템은 보안성·신뢰성·기능적합성이, 게임/모바일은 성능효율성·사용성·이식성이, 항공/의료 SW는 신뢰성·안전성이 압도적으로 높다.

- **📢 섹션 요약 비유**: ISO 25010은 마치 **학교의 종합 성적표**와 같다. "국어·수학·영어·과학·체육" 등 8개 과목(특성)이 있고, 각 과목 안에 세부 단원(세부 특성)이 있으며, 학기말 시험(측정)으로 점수가 매겨진다. 다만 과목별 반영 비율(가중치)이 진로에 따라 다르게 책정된다.

---

## Ⅲ. 비교 및 연결

| 구분 | ISO/IEC 9126 (1991~2006) | ISO/IEC 25010 (2011) | ISO/IEC 25010:2024 |
| :--- | :--- | :--- | :--- |
| **개정 시기** | 1991년 제정, 2001년 개정 | 2011년 전면 개정 (SQuaRE 시리즈의 일부) | 2024년 마이너 개정 (현대 기술 반영) |
| **특성 수** | 6대 특성 (Functionality, Reliability, Usability, Efficiency, Maintainability, Portability) | 8대 특성 (보안성·호환성 분리/추가) | 8대 특성 유지, 보안성·유연성 강화 |
| **보안성** | 없음 (Functionality의 일부) | 독립된 1대 특성 (5개 세부) | 7개 세부 특성으로 확장 (식별성·저항성) |
| **호환성** | Portability에 포함 | 독립 (Co-existence + Interoperability) | 상호운용성 강화, API·클라우드 네이티브 반영 |
| **Quality in Use** | 미포함 | 5개 특성 신규 도입 (Effectiveness, Efficiency 등) | AI 윤리·접근성 항목 추가 |
| **측정 지원** | ISO 14598 (별도) | ISO 25020~25024 통합 (측정 참조 모델·절차) | 자동 측정·DevSecOps 통합 강화 |
| **연결 생태계** | IEEE 830, CMMI v1.x | CMMI v2.0, TMMi, ISO 9001, SPICE | SAFe, DevSecOps, ISO/IEC 42001(AI거버넌스) |

**연결 통합 포인트**:
- **CMMI(능력성숙도통합모델)**: ISO 25010의 8대 특성을 CMMI v2.0의 **PAM(Process Area Model)**과 1:1 매핑하여 성숙도 레벨 2~5의 평가 증거로 활용
- **ISTQB 테스트 인증**: ISO 25010의 31개 세부 특성을 테스트 커버리지 기준의 **비기능 요구사항(Non-functional Requirements) 테스트 항목**으로 변환
- **IEEE 830 / 29148 SRS**: 품질 요구사항을 SRS의 Non-functional Requirements 섹션에 정량적 목표로 기술
- **OWASP / NIST SSDF**: 보안성 5~7개 세부 특성을 **OWASP ASVS(Application Security Verification Standard) 레벨 1~3** 및 NIST SP 800-218(SSDF 1.1)와 매핑
- **ISO/IEC 5055** (Automated Source Code Quality Measures): 코드 수준의 Cyclomatic Complexity, 결합도 등을 유지보수성 메트릭으로 자동 측정

- **📢 섹션 요약 비유**: ISO 9126이 **"기능 vs 비기능"으로 나누던 흑백 TV**였다면, 25010:2011은 **8K UHD 컬러 TV**, 2024년판은 **HDR·Dolby Atmos·AI 업스케일링이 추가된 스마트 TV**라고 할 수 있다. 기본 채널(특성)은 같지만 지원하는 콘텐츠(기술)와 측정 도구(원단위)가 압도적으로 진화했다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사형 판단 체크리스트

1. **품질 목표치의 정량화**: 각 세부 특성에 대해 **측정 가능한 임계값(Threshold)**을 정의했는가? 예: "응답시간이 빨라야 한다(X)" -> "API p95 응답시간 < 200ms, p99 < 500ms, 동시접속 10,000명(O)". Stekeholder Workshop에서 **GQM(Goal-Question-Metric)** 패턴으로 도출했는가?
2. **도메인 특화 가중치 적용**: 시스템 도메인에 따라 **8대 특성의 가중치 벡터**를 AHP(Analytic Hierarchy Process) 또는 Delphi 기법으로 산정했는가? 예: 의료기기 SW(전자의무기록) -> 신뢰성 30%, 보안성 25%, 기능적합성 20%, 사용성 10%, 성능 10%, 기타 5%
3. **자동 측정·수집 체계**: CI/CD 파이프라인(Jenkins/GitHub Actions/GitLab CI)에 **정적 분석(SonarQube, Checkstyle) + 동적 분석(JMeter, Gatling) + 보안 스캔(Snyk, OWASP ZAP)**을 통합하여 매 빌드마다 품질 메트릭을 자동 수집하는가? SonarQube의 Quality Gate와 ISO 25010 메트릭 매핑이 필수
4. **사용 시 품질(Quality in Use) UX 평가**: NPS(Net Promoter Score), SUS(System Usability Scale), SUS ≥ 80점 목표, A/B 테스트, 휴리스틱 평가(Nielsen 10 원칙)를 통해 **사용자 만족도·효과성·효율성**을 실측했는가? 계량형 휴리스틱 평가(MoMo – Heuristic Evaluation Modality)로 자동화
5. **리스크 기반 우선순위 결정**: **Bow-tie 분석, F
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 438 / 800

<- **이전**: [437. 비용 산정 FP COCOMO COSMIC](/studynote/12_it_management/05_security_compliance/437_cost_estimation_fp_cocomo_cosmic/)
**다음**: [439. SW 아키텍처 평가 ATAM CBAM](/studynote/12_it_management/05_security_compliance/439_sw_architecture_evaluation_atam_cbam/) ->

---
