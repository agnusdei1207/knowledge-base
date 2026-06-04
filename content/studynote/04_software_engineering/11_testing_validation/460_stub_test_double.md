+++
title = "460. Stub (스텁)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-software-engineering"]

[extra]
tags = ["studynote-software-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Stub (스텁)은(는) [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)의 핵심 개념으로, 복잡한 시스템을 체계적으로 설계·관리하기 위한 원칙과 기법이다.
> 2. **가치**: 이 개념을 올바르게 적용하면 소프트웨어의 품질·[유지보수성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/346_maintainability_portability/)·재사용성이 향상되고, 개발 생산성과 팀 협업 효율이 높아진다.
> 3. **판단 포인트**: 도입 시에는 비용·복잡도·조직 성숙도를 함께 고려해야 하며, 맹목적 적용보다 프로젝트 특성에 맞는 선택적 적용이 핵심이다.

---

## Ⅰ. 개요 및 필요성

Stub은 "대답만 하는 대역"이다. 테스트 대상이 외부 시스템의 응답을 필요로 할 때 사용한다.

네트워크, DB, API처럼 느리거나 불안정한 의존성을 끊는 데 유용하다.

- **📢 섹션 요약 비유**: 질문에 정해진 대답만 하는 녹음기와 같다.

---

다음은 Stub (스텁)의 핵심 구조와 흐름을 보여주는 다이어그램이다.

```text
+-------------------------------------------------------------+
|                  Stub (스텁)                                   |
+-------------------------------------------------------------+
|                                                             |
|  [입력/요구사항] ---> [핵심 처리 과정] ---> [출력/결과물]  |
|       |                    |                    |          |
|       v                    v                    v          |
|   요구 분석           설계·적용           품질 검증        |
|                                                             |
+-------------------------------------------------------------+
```

이 다이어그램은 Stub (스텁)가 입력 요구사항을 받아 핵심 처리 과정을 거쳐 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 결과물을 산출하는 흐름을 보여준다.

---

---

---

## Ⅱ. 아키텍처 및 핵심 원리

Stub은 상태를 바꾸지 않고 준비된 응답을 준다. 그래서 상태 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 중심 테스트에 잘 맞는다.

| 특징 | 설명 |
|:---|:---|
| 역할 | 응답 제공 |
| 동작 | 고정 반환 |
| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 상태 중심 |

```text
호출 -> Stub 응답 반환 -> 테스트 진행
```

Stub은 동작을 기록하지 않으므로 행위 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)에는 적합하지 않다.

- **📢 섹션 요약 비유**: 자동응답 전화처럼 미리 정해진 말만 한다.

---

---

---

---

## Ⅲ. 비교 및 연결

Stub은 Dummy보다 적극적이고, Mock보다 덜 엄격하다. 반환값이 필요할 때 딱 맞는다.

| 구분 | [Dummy](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/) | Stub | [Mock](/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/) |
|:---|:---|:---|:---|
| 역할 | 자리 채움 | 값 반환 | 호출 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 사용 | 없음 | 있음 | 있음 |
| 초점 | 존재 | 상태 | 행위 |

상태 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)용 단위 테스트에서 매우 흔하다.

- **📢 섹션 요약 비유**: 빈 상자, 답변하는 상자, 검사까지 받는 상자의 차이다.

---

---

---

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 로그인 응답, 환율 조회, 결제 승인 응답처럼 외부 결과를 고정할 때 쓴다. 덕분에 테스트가 반복 가능해진다.

체크 포인트는 다음과 같다.
1. 필요한 값만 반환한다.
2. 테스트 외부 의존을 끊는다.
3. 복잡한 행위 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 Mock으로 넘긴다.

- **📢 섹션 요약 비유**: 연습용 음성 안내가 필요한 상황에 맞다.

---

---

---

---

## Ⅴ. 기대효과 및 결론

Stub은 테스트를 빠르고 안정적으로 만든다. 외부 응답이 흔들려도 내부 로직을 확인할 수 있다.

결론적으로 이 개념은 "대답만 준비된 대역"이다. 상태 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)에 좋은 기본 도구다.

- **📢 섹션 요약 비유**: 질문에 매번 같은 답을 주는 연습 파트너다.

---

---

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/) ([Software 엔진ering](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)) | Stub (스텁)의 상위 학문 체계이며 품질·생산성 향상의 공통 목표를 공유한다 |
| [소프트웨어 생명주기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/003_sdlc/) ([SDLC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/131_sdlc_system_development_life_cycle_waterfall_agile/), Software Development Life Cycle) | Stub (스텁)은 SDLC의 특정 단계에서 핵심적으로 적용된다 |
| 품질 보증 (QA, Quality Assurance) | Stub (스텁) 적용 결과는 QA 활동을 통해 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)되고 측정된다 |
| [형상 관리](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) ([SCM](/knowledge-base/studynote/12_it_management/04_sdlc_testing/167_scm_software_configuration_management/), [Software Configuration Management](/knowledge-base/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/)) | Stub (스텁)에서 생성된 산출물은 SCM을 통해 체계적으로 관리된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
소프트웨어 위기 (Software Crisis) 인식
    |
    v
Stub (스텁) 개념 정립
    |
    v
표준화 및 방법론 체계화 (ISO, CMMI, Agile)
    |
    v
클라우드 네이티브·AI 기반 확장 적용
    |
    v
지속적 개선 및 DevOps·MLOps 통합
```

이 흐름은 [소프트웨어 위기](/knowledge-base/studynote/04_software_engineering/01_overview_principles/002_software_crisis/) 인식 -> 체계적 방법론 개발 -> 표준화 -> 현대적 플랫폼 적용으로 이어지는 발전 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Stub (스텁)은 레고 블록으로 성을 만들 때처럼, 규칙을 정하고 역할을 나누어 함께 작업하는 방법이에요.
2. 혼자서 막 만들면 나중에 무너지거나 고치기 어렵지만, 약속을 지키면 누구나 쉽게 고치고 더 크게 만들 수 있어요.
3. 그래서 [소프트웨어 공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/)은 프로그래머들이 좋은 프로그램을 빠르고 안전하게 만들 수 있게 도와주는 '규칙 모음집'이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 511 / 973

<- **이전**: [459. Dummy (더미) - 인자 채우기용, 실제 사용 안됨](/knowledge-base/studynote/04_software_engineering/11_testing_validation/459_dummy_test_double/)
**다음**: [460. Stub (스텁) - 호출 시 준비된 답변만 반환 (상태 검증용)](/knowledge-base/studynote/04_software_engineering/11_testing_validation/460_stub_test_double/) ->

---
