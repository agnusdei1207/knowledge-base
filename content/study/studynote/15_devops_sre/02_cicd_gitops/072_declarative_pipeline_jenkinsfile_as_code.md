+++
weight = 72
title = "72. 선언적 파이프라인 - Jenkinsfile (Pipeline as Code)"
date = "2026-04-10"
[extra]
categories = "studynote-devops"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 선언적 [[123_pipe|파이프]]라인은 Jenkinsfile로 [[090_configuration_item|CI]]/CD 흐름을 코드로 정의하는 방식이다.
> 2. **가치**: 빌드/테스트/배포를 표준화하고 재현성을 높인다.
> 3. **판단**: 선언적 구문과 단계적 실행 구조를 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

UI로만 [[123_pipe|파이프]]라인을 만들면 추적이 어렵다.

Jenkinsfile로 관리하면 [[330_code_review|코드 리뷰]]와 [[288_version_ihl_tos_total_length|버전]] 관리가 가능하다.

- **📢 섹션 요약 비유**: 요리 순서를 종이에 적어 두는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Jenkinsfile
  ↓ declarative pipeline
Stages / Steps
```

| 요소 | 의미 |
| :-- | :-- |
| [[082_pipeline|pipeline]] | 전체 흐름 |
| stage | 단계 |
| agent | 실행 환경 |

선언적 [[123_pipe|파이프]]라인은 구조가 명확하고 읽기 쉬워 표준화에 적합하다.

- **📢 섹션 요약 비유**: 레시피가 깔끔하게 정리된 요리책이다.

---

## Ⅲ. 비교 및 연결

| 구분 | [[219_declarative_yaml|Declarative]] | Scripted |
| :-- | :-- | :-- |
| 구조 | 명확 | 유연 |
| [[333_readability_vs_efficiency|가독성]] | 높음 | 낮을 수 있음 |
| 사용 | 표준화 | 복잡한 제어 |

| 관련 | 의미 |
| :-- | :-- |
| [[082_pipeline|Pipeline]] [[344_as_autonomous_system_asn|as]] [[082_process_memory_structure|Code]] | 코드화 |
| [[090_configuration_item|CI]]/CD | 자동화 |

선언적 [[123_pipe|파이프]]라인은 운영 표준과 협업에 유리하다.

- **📢 섹션 요약 비유**: 약속된 레시피라서 누구나 따라 하기 쉽다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. Jenkinsfile로 관리하는가?
2. stage와 agent를 나눴는가?
3. [[330_code_review|코드 리뷰]]가 가능한가?
4. 재현성이 있는가?
5. 운영 표준과 맞는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- UI에만 의존하는 설계
- scripted와 declarative를 혼동하는 설계
- [[123_pipe|파이프]]라인을 문서처럼만 보는 설계
- [[156_environment_variables|환경 변수]]를 무질서하게 쓰는 설계

기술사 관점에서는 선언적 [[123_pipe|파이프]]라인을 "코드로 정의된 [[090_configuration_item|CI]]/CD 표준"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 순서를 코드로 써 둔 자동 공정표다.

---

## Ⅴ. 기대효과 및 결론

Jenkinsfile은 [[123_pipe|파이프]]라인을 재현 가능하게 만든다.

결론적으로 선언적 [[123_pipe|파이프]]라인은 Jenkinsfile로 정의하는 [[082_pipeline|Pipeline]] [[344_as_autonomous_system_asn|as]] Code다.

- **📢 섹션 요약 비유**: 작업 순서를 코드로 적는 것이다.

---

## 관련 개념 맵

```text
Jenkinsfile
  ↓
Declarative Pipeline
  ↓
Stages / Steps
  ↓
CI/CD
```

---

## 관련 키워드 및 발전 흐름도

```text
Pipeline as Code
  ↓
Jenkinsfile
  ↓
Declarative Pipeline
```

---

## 어린이를 위한 3줄 비유 설명

순서를 코드로 적어요.  
자동으로 따라 해요.  
선언적 [[123_pipe|파이프]]라인은 그런 방식이에요.
