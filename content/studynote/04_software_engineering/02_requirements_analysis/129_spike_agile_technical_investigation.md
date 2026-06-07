---
title: "129. Spike Agile Technical Investigation"
date: "2026-04-19"
tags:
  - "studynote-software-engineering"
weight: 129
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Spike는 Agile에서 <strong>기술적 불확실성·위험을 해소하기 위한 시간 제한(Timebox) 조사·실험 활동</strong>이며, 스토리 추정이 불가능할 때 "먼저 조사해보자"로 수행된다.
> 2. **가치**: 기술적 불확실성(새 [라이브러리](/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/)·[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 한계·아키텍처 선택)이 있으면 <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/082_story_point_velocity/">스토리 포인트</a> 추정이 불가능</strong>하고 스프린트가 예측 불가능해지므로, Spike로 사전 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하여 <strong>리스크를 제거</strong>한다.
> 3. **판단 포인트**: Spike는 <strong>산출물이 코드가 아니라 "지식(결정·판단)"</strong>이며, 타임박스(보통 1~2일)를 반드시 설정하여 무한 탐구를 방지한다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Spike 프로세스                                     |
+-------------------------------------------------------+
|  1. 불확실성 식별: "이 라이브러리가 요건을 충족할까?"|
|  2. Spike 생성: 타임박스 2일, 목표 명확히            |
|  3. 조사·PoC: 프로토타입·성능 테스트                 |
|  4. 결과 공유: "A 라이브러리 사용 결정, 이유는..."   |
|  5. 원래 스토리: 이제 추정 가능 -> 스프린트 투입      |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Spike는 <strong>정찰대</strong>이다. 본대(개발팀)가 진격하기 전에 정찰대가 먼저 가서 "이 길이 안전한지" [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Spike 유형

| 유형 | 목적 | 예 |
|:---|:---|:---|
| **기술 Spike** | 기술 가능성 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | PoC, [성능 테스트](/studynote/04_software_engineering/11_testing_validation/837_performance_test_types/) |
| **기능 Spike** | 요구사항 명확화 | 사용자 인터뷰, [프로토타입](/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/) |

- **📢 섹션 요약 비유**: 기술 Spike는 "다리가 무게를 견딜까?" 테스트, 기능 Spike는 "이 다리가 필요한가?" [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 일반 스토리 | Spike |
|:---|:---|:---|
| **산출물** | 작동하는 코드 | **지식·결정** |
| **추정** | [스토리 포인트](/studynote/04_software_engineering/02_requirements_analysis/082_story_point_velocity/) | **타임박스** |
| **목적** | 가치 전달 | **불확실성 제거** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### Spike 규칙
1. 타임박스 필수 (1~2일, 최대 1스프린트).
2. 목표·질문을 명확히 정의.
3. 결과를 팀에 공유 (문서·데모).
4. Spike 후 원래 스토리를 추정·계획.

---

## Ⅴ. 기대효과 및 결론

Spike는 <strong>Agile에서 기술 리스크를 사전 제거하는 유일한 공식 메커니즘</strong>이며, "모르는 것을 인정하고 조사한다"는 [Agile](/studynote/15_devops_sre/01_culture_methodology/004_agile_relation/) 투명성 원칙의 실천이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Spike** | 기술 불확실성 조사 |
| **타임박스** | Spike의 시간 제한 |
| **PoC** | 기술 Spike의 산출물 |
| <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/082_story_point_velocity/">스토리 포인트</a></strong> | Spike 후 추정 가능 |
| <strong><a href="/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">Technical Debt</a></strong> | Spike 없이 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 시 발생 |

### 📈 관련 키워드 및 발전 흐름도

```text
[XP (Extreme Programming, 1999) — Spike 개념 도입]
    |
    v
[Scrum + Spike (2005~)]
    |
    v
[SAFe Spike (2015~) — 대규모 Agile에서의 Spike]
    |
    v
[PoC as Code (2020~) — Spike 산출물 재사용]
    |
    v
[현재: AI Spike — LLM으로 기술 조사 자동화]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Spike는 <strong>정찰대</strong>예요. 본대(개발팀)가 가기 전에 <strong>먼저 가서 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>해요.
2. "이 길이 안전한가?" "이 도구가 쓸만한가?" <strong>조사하고 보고</strong>해요.
3. 정찰 결과를 보고 본대가 <strong>안전하게 진격</strong>할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 129 / 973

<- **이전**: [128. Water-Scrum-Fall (안티패턴) - 하이브리드 Agile의 함정](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
**다음**: [130. 인수 기준 vs 완료 정의 (Acceptance Criteria vs Definition of Done)](/studynote/04_software_engineering/02_requirements_analysis/130_acceptance_criteria_vs_dod/) ->

---
