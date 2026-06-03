+++
weight = 78
title = "78. 코드 커버리지 (Code Coverage) 분석 도구 (JaCoCo) - 소스코드의 몇 %가 테스트되었는지 측정 (구문, 분기 커버리지)"
description = "소스코드의 몇 퍼센트가 테스트되었는지 측정하는 JaCoCo, Istanbul 등의 커버리지 분석 도구와 구문/분기/조건 커버리지의 차이, 품질 게이트 연동 방법"
date = "2026-04-05"

[taxonomies]
tags = ["DevOps", "CI/CD", "Testing", "Code Coverage", "JaCoCo", "Quality Gate"]
categories = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 코드 커버리지는 테스트가 실행한 코드의 범위를 측정하는 지표다.
> 2. **가치**: statement, branch, condition coverage는 서로 다른 빈틈을 보여 주므로 함께 봐야 한다.
> 3. **판단 포인트**: 커버리지는 품질의 대리 지표일 뿐이므로, 의미 있는 assertion과 함께 써야 한다.

---

## Ⅰ. 개요 및 필요성

[[076_ci_continuous_integration|지속적 통합]]과 [[213_refactoring_cloud_native_rearchitecture|리팩토링]]이 일상인 환경에서는 어느 코드가 테스트되지 않았는지 빨리 알아야 한다. 코드 커버리지는 그 빈틈을 보여 주는 가장 기본적인 계량값이다.
JaCoCo (Java [[082_process_memory_structure|Code]] Coverage)와 Istanbul 같은 도구는 테스트 실행 후 어떤 줄과 분기가 실제로 지나갔는지 기록한다.
```text
테스트 실행 → instrumented code → hit count → coverage report → quality gate
```

- **📢 섹션 요약 비유**: 테스트되지 않은 코드는 배포 시 가장 큰 불확실성이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

커버리지 도구는 보통 계측, 실행, 수집, 보고의 순서로 동작한다. 테스트가 코드를 지나갈 때마다 카운트가 쌓이고, 그 결과가 보고서로 바뀐다.
중요한 점은 "몇 %를 덮었는가"보다 "어디를 못 봤는가"다. 그래서 라인 커버리지보다 분기와 [[424_condition_coverage|조건 커버리지]]가 더 많은 정보를 줄 수 있다.
| 지표 | 보는 것 | 남는 빈틈 |
| --- | --- | --- |
| [[422_statement_coverage|Statement coverage]] | 실행된 문장 비율 | 분기 미실행 |
| Branch coverage | if/else 경로 비율 | 조건 조합 미확인 |
| [[424_condition_coverage|Condition coverage]] | 개별 조건의 참/거짓 | 조건 조합 전체 |
| MC/DC (Modified Condition/[[423_decision_coverage|Decision Coverage]]) | 결정에 영향을 준 조건 | 안전성 [[395_verification_process_review|검증]]의 고급 기준 |

- **📢 섹션 요약 비유**: 계측과 보고를 통해 테스트의 시야를 숫자로 본다.

---

## Ⅲ. 비교 및 연결

커버리지는 품질 그 자체가 아니라 테스트의 시야를 보여 준다. 그래서 높은 커버리지와 높은 품질은 동의어가 아니다.
라인 커버리지는 빠르게 보기 좋고, 분기 커버리지는 더 깊은 분기를 드러내며, mutation testing은 실제 [[395_verification_process_review|검증]]력이 있는지를 [[396_validation|확인]]한다.
| 비교축 | 커버리지 | [[456_mutation_testing|Mutation testing]] |
| --- | --- | --- |
| 목적 | 어디를 실행했는지 본다 | 테스트가 진짜 잡는지 본다 |
| 장점 | 빠르고 직관적이다 | 테스트 품질을 더 잘 드러낸다 |
| 한계 | 실행만 했는지로 끝난다 | 비용이 더 크다 |

- **📢 섹션 요약 비유**: 커버리지는 품질의 대체물이 아니라 품질 점검의 시작이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 전체 커버리지보다 변경된 코드의 diff coverage와 핵심 경로를 더 본다. 숫자를 채우려고 의미 없는 테스트만 늘리면 오히려 유지보수가 어려워진다.
커버리지 목표는 [[192_module_independence|모듈]]별 위험도에 맞춰 다르게 정하고, [[087_process_state_transition|생성]] 코드나 외부 [[336_library_vs_framework|라이브러리]] 코드는 예외를 엄격하게 관리해야 한다.
### [[435_checklist_based_testing|체크리스트]]

1. 커버리지가 변경 범위를 실제로 반영하는가?
2. 테스트에 assertion이 충분한가?
3. 핵심 분기와 예외 경로가 포함됐는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 100% 숫자만 채우는 테스트
- 커버리지 향상을 위해 무의미한 assert-[[094_less_large_scale_scrum|less]] 테스트를 늘리는 것

- **📢 섹션 요약 비유**: 숫자만 높이는 테스트는 오히려 독이 될 수 있다.

---

## Ⅴ. 기대효과 및 결론

커버리지가 있으면 [[213_refactoring_cloud_native_rearchitecture|리팩토링]]과 배포 전에 위험 구간을 빨리 찾을 수 있다. 즉, 커버리지는 테스트 품질의 센서이자 배포 전 경보장치다.
앞으로는 diff 기반 게이팅과 [[190_ai_llm_requirements_specification|AI]] 보조 테스트 [[087_process_state_transition|생성]]이 더 중요해진다.
기술사는 이 주제를 "얼마나 많이 했는가보다 어디를 못 봤는가를 찾는 지표"로 기억하면 된다.

- **📢 섹션 요약 비유**: 커버리지는 [[213_refactoring_cloud_native_rearchitecture|리팩토링]]과 배포의 위험을 낮춘다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| --- | --- |
| [[397_unit_test|Unit test]] | 커버리지의 기본 실행 단위다 |
| Branch coverage | 분기 경로를 보여 준다 |
| [[090_configuration_item|CI]] | 자동으로 게이트를 적용한다 |
| [[456_mutation_testing|Mutation testing]] | 테스트의 진짜 힘을 [[396_validation|확인]]한다 |
| Quality gate | 배포 허용 기준을 정한다 |
| Diff coverage | 변경된 코드만 집중해서 본다 |

### 📈 관련 키워드 및 발전 흐름도

```text
테스트 작성
  │
  ▼
계측 빌드 실행
  │
  ▼
커버리지 수집
  │
  ▼
보고서 확인
  │
  ▼
품질 게이트 통과
```

### 👶 어린이를 위한 3줄 비유 설명

1. 책에 형광펜을 칠한 부분만 보면 어디를 읽었는지 알 수 있는 것과 같다.
2. 하지만 색칠이 많다고 해서 내용을 다 이해한 것은 아니다.
3. 그래서 컴퓨터도 읽은 곳과 진짜 이해한 곳을 따로 봐야 한다.
