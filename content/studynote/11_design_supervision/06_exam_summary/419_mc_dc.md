+++
title = "419. 화이트박스 변경 조건·결정 독립 커버리지 (MC/DC, Modified Condition/Decision Coverage)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 변경 조건/[결정 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/423_decision_coverage/)(MC/DC, Modified Condition/[Decision Coverage](/knowledge-base/studynote/04_software_engineering/11_testing_validation/423_decision_coverage/))는 각 개별 조건이 다른 조건값 고정 상태에서도 전체 결정 결과를 독립적으로 바꾼다는 사실을 입증하는 [화이트박스 테스트](/knowledge-base/studynote/04_software_engineering/07_object_oriented/420_whitebox_testing/) 기준이다.
> 2. **가치**: 구문·분기 커버리지보다 높은 신뢰도를 제공하면서도 모든 조건 조합을 다 시험하는 [다중 조건 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/427_multiple_condition_coverage/)보다 적은 테스트 수로 핵심 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 오류를 검출할 수 있다.
> 3. **판단 포인트**: 조건 독립성 입증 쌍, 최소 테스트 세트의 타당성, 안전 필수 로직 적용 여부, [요구사항 추적성](/knowledge-base/studynote/04_software_engineering/03_design_architecture/156_requirements_traceability_vertical_horizontal/)이 갖춰져야 MC/DC가 제대로 성립한다.

## Ⅰ. 개요 및 필요성

MC/DC는 단순히 분기문의 참·거짓을 한 번씩 실행하는 수준을 넘는다. 예를 들어 결정식이 `(A and B) or C`라면, A·B·C 각각이 다른 조건은 그대로 둔 채 결과를 바꾸는 사례가 있어야 한다. 즉 “이 조건이 실제로 결과에 영향을 주는가”를 독립적으로 증명하는 것이 핵심이다.

이 기준이 중요한 이유는 항공·자동차·국방처럼 안전 필수 소프트웨어에서 복합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)의 비용이 매우 크기 때문이다. 감리에서는 MC/DC를 단순한 고급 커버리지 용어가 아니라, <strong>복합 조건 <a href="/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a>를 얼마나 엄격하게 통제하는가</strong>를 보여 주는 증거로 본다.

```text
+--------------------+
| 결정식: (A ∧ B) ∨ C |
+---------+----------+
          v
+--------------------+
| A 독립 영향 입증    |
| B 독립 영향 입증    |
| C 독립 영향 입증    |
+--------------------+
```

- **📢 섹션 요약 비유**: 세 개의 스위치가 달린 전등이라면, 각 스위치가 정말 불을 켜고 끄는 데 영향을 주는지 하나씩 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 검사다.

## Ⅱ. 아키텍처 및 핵심 원리

MC/DC 설계의 핵심은 조건 분해, 영향 분석, 테스트 쌍 선정, 실행 증적 확보의 네 단계다. 먼저 결정식을 원자 조건 단위로 분해하고, 각 조건이 전체 결과를 바꾸는 입력 쌍을 찾는다. 이때 다른 조건은 가능한 한 고정해야 독립성이 성립한다. 이후 [테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/)와 요구사항, 코드 라인, 실행 결과를 연결해 추적성을 남긴다.

감리에서는 테스트 수가 적다고 무조건 좋은 것이 아니다. 최소 집합을 만들더라도 각 조건의 독립 영향이 실제로 증명되는지, 도달 불가능한 경로나 단락 평가(short-circuit) 때문에 왜곡된 판정이 없는지를 함께 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다.

```text
+--------------------+
| 조건 분해(A,B,C)    |
+---------+----------+
          v
+--------------------+
| 독립 영향 쌍 선정    |
+---------+----------+
          v
+--------------------+
| 실행·결과 기록       |
+---------+----------+
          v
+--------------------+
| 요구사항 추적성 확인 |
+--------------------+
```

| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 요소 | 설명 | 감리 포인트 |
|:---|:---|:---|
| 조건 분해 | 복합 결정식을 원자 조건으로 분리 | 조건 누락 없이 분해되었는가 |
| 독립성 입증 | 한 조건 변화만으로 결과가 달라지는 쌍 구성 | 다른 조건이 고정되어 있는가 |
| 추적성 관리 | 요구사항-코드-테스트 결과 연결 | 안전 기준과 실행 증적이 연결되는가 |

- **📢 섹션 요약 비유**: 비행기 조종석의 여러 버튼을 점검할 때, 한 버튼만 바꿨을 때 계기 반응이 달라지는지 따로 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 진짜 역할을 알 수 있다.

## Ⅲ. 비교 및 연결

MC/DC의 위치는 다른 화이트박스 커버리지와 비교할 때 명확해진다. [구문 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/422_statement_coverage/)는 문장 실행 여부, [결정 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/423_decision_coverage/)는 분기 참·거짓 여부, [조건 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/424_condition_coverage/)는 개별 조건 참·거짓 여부를 본다. MC/DC는 여기서 한 걸음 더 나아가 각 조건의 독립 영향까지 요구한다.

| 항목 | [구문 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/422_statement_coverage/) | [결정 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/423_decision_coverage/) | [조건 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/424_condition_coverage/) | MC/DC |
|:---|:---|:---|:---|:---|
| 초점 | 모든 문장 실행 | 분기 참/거짓 실행 | 각 조건 참/거짓 실행 | 각 조건의 독립 영향 입증 |
| 강도 | 낮음 | 중간 | 중간 | 높음 |
| 테스트 수 | 적음 | 적음~중간 | 중간 | 중간~높음 |
| 대표 장점 | 기본 실행 누락 탐지 | 분기 로직 점검 | 조건별 값 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 복합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 탐지력 우수 |
| 대표 한계 | [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 품질 보장 부족 | 내부 조건 영향은 미흡 | 전체 결정 영향 입증 부족 | 설계·증적 관리가 복잡 |

- **📢 섹션 요약 비유**: 길을 한 번 걸어 봤는지, 갈림길을 둘 다 가 봤는지, 표지판을 다 봤는지, 그리고 각 표지판이 길 선택에 진짜 영향을 줬는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 단계가 점점 엄격해지는 셈이다.

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 MC/DC는 모든 시스템에 무조건 적용하기보다, 안전 필수 기능이나 규제 준수 대상 로직에 우선 적용한다. 예를 들어 항공 제어, 제동 제어, 의료 알람, 원전 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 로직처럼 잘못된 의사결정이 큰 피해를 일으키는 영역에서 특히 중요하다. 감리는 이런 적용 범위가 위험도 기반으로 선정되었는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 한다.

또한 MC/DC는 도구 결과만 믿으면 안 된다. 자동 산출된 커버리지 수치가 독립성 증거를 충분히 설명하지 못할 수 있으므로, [테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/) 쌍과 요구사항 매핑을 함께 검토해야 한다. 기술사 답안에서도 안전 표준 맥락과 추적성까지 적어야 완성도가 높다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- 복합 결정식이 원자 조건 단위로 정확히 분해되었는가?
- 각 조건이 다른 조건 고정 상태에서 결과를 바꾸는 테스트 쌍이 존재하는가?
- 단락 평가나 도달 불가 경로가 독립성 판정에 영향을 주지 않는가?
- MC/DC 적용 범위가 안전도·위험도 기준으로 선정되었는가?
- 요구사항, 코드, 테스트 결과, 커버리지 보고서가 서로 추적 가능한가?

- **📢 섹션 요약 비유**: 중요한 기계의 버튼을 검사할 때 “아무거나 눌러 봤다”가 아니라 “이 버튼 때문에 결과가 바뀌었다”를 하나씩 증명해야 한다.

## Ⅴ. 기대효과 및 결론

MC/DC를 적용하면 복합 조건식에 숨어 있는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 더 체계적으로 찾아낼 수 있고, 안전 필수 소프트웨어의 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 신뢰도도 높아진다. [다중 조건 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/427_multiple_condition_coverage/)보다 현실적인 테스트 수로 높은 보증 수준을 확보할 수 있다는 점이 실무적 장점이다. 다만 설계와 추적성 관리가 부족하면 형식적 수치로 전락할 위험이 있다.

결론적으로 MC/DC의 핵심은 높은 커버리지 숫자가 아니라 <strong>조건 독립성의 증명</strong>이다. 답안에서는 조건 분해, 독립 영향 쌍, 다른 커버리지와의 비교, 안전 표준 적용 맥락을 함께 제시해야 한다.

- **📢 섹션 요약 비유**: 자전거 브레이크를 점검할 때 바퀴가 멈췄다는 사실만 보는 게 아니라, 앞브레이크와 뒷브레이크가 각각 따로 멈추게 만드는지도 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 것과 같다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [결정 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/423_decision_coverage/) | 분기 참/거짓 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)에 그치며 조건 독립성까지는 보장하지 않는다. |
| [조건 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/424_condition_coverage/) | 개별 조건 값 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 제공하지만 전체 결정 영향은 별도 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)이 필요하다. |
| [다중 조건 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/427_multiple_condition_coverage/) | 모든 조합을 보지만 테스트 수 폭증 문제가 있다. |
| 안전 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 기준 | 고신뢰 시스템에서 MC/DC 적용 필요성을 강화한다. |
| [요구사항 추적성](/knowledge-base/studynote/04_software_engineering/03_design_architecture/156_requirements_traceability_vertical_horizontal/) | MC/DC 증적이 규제 대응 문서와 연결되도록 해 준다. |

### 📈 관련 키워드 및 발전 흐름도

- 관련 키워드: [화이트박스 테스트](/knowledge-base/studynote/04_software_engineering/07_object_oriented/420_whitebox_testing/), [결정 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/423_decision_coverage/), [조건 커버리지](/knowledge-base/studynote/04_software_engineering/11_testing_validation/424_condition_coverage/), MC/DC, 단락 평가, 안전 필수 소프트웨어
- 발전 흐름: 구문 실행 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) -> 분기 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) -> 조건 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) -> 조건/결정 결합 -> MC/DC 독립성 입증 -> 다중 조건 완전 조합 검토

```text
구문 커버리지
      |
      v
결정 커버리지
      |
      v
조건 커버리지
      |
      v
조건/결정 커버리지
      |
      v
MC/DC
```

### 👶 어린이를 위한 3줄 비유 설명

1. 불이 켜지는 방에 스위치가 여러 개 있다면, 각 스위치가 진짜로 영향을 주는지 따로 봐야 해요.
2. MC/DC는 버튼 하나만 바꿨을 때 결과도 달라지는지를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 시험이에요.
3. 그래서 중요한 기계가 복잡한 규칙대로 움직여도 더 믿고 쓸 수 있게 도와줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 497 / 530

<- **이전**: [418. 뮤테이션 테스트의 소스 변이 커버리지 검증 (Mutation Testing)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/418_audit/)
**다음**: [420. 페어와이즈·직교배열 기반 조합 축소 (Pairwise & Orthogonal Array Reduction)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/420_process/) ->

---
