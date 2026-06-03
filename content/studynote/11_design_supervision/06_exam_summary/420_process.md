+++
title = "420. 페어와이즈·직교배열 기반 조합 축소 (Pairwise & Orthogonal Array Reduction)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/) 테스트는 입력 인자 간 2-way 상호작용을 최소 케이스로 덮고, 직교 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) (Orthogonal [Array](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/), OA)은 균형성과 대표성을 높여 블랙박스 조합 폭발을 줄이는 기법이다.
> 2. **가치**: 전수 조합이 불가능한 화면·[정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)·환경 매트릭스에서도 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 검출력과 테스트 비용 사이의 균형점을 만들 수 있다.
> 3. **판단 포인트**: 변수 수, 레벨 수, 금지 조합, 위험도가 무엇인지 먼저 구조화한 뒤, “모든 경우”가 아니라 “중요 상호작용이 충분히 커버되는가”를 따져야 한다.

---

## Ⅰ. 개요 및 필요성

[블랙박스 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/412_black_box_testing/)에서 입력 조건이 많아질수록 [테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/) 수는 기하급수적으로 늘어난다. 예를 들어 브라우저, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/), 권한, 결제수단, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 상태를 모두 조합하면 전수 조합은 곧바로 실무 한계를 넘는다. [페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/)와 직교 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)은 바로 이 <strong>조합 폭발</strong>을 통제하기 위한 대표적인 축소 기법이다.

[페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/)의 핵심 가정은 “많은 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)이 두 인자 간 상호작용에서 드러난다”는 점이다. 따라서 모든 조합을 다 시험하지 않더라도, 각 인자 쌍이 적어도 한 번씩 등장하도록 케이스를 구성하면 높은 효율을 얻을 수 있다. 직교 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)은 각 수준이 균형 있게 배치되도록 구성해 편향을 줄이고 분석 가능성을 높인다.

기술사 답안에서는 단순히 “테스트 수를 줄이는 방법”이라고 쓰면 부족하다. 어떤 요인을 분해했고, 어떤 제약 조건을 제외했으며, 어떤 고위험 조합을 추가 보완했는지까지 설명해야 답안이 실무형이 된다.

- **📢 섹션 요약 비유**: 뷔페 전 메뉴를 다 먹어 보는 대신, 재료 조합이 겹치지 않게 대표 메뉴를 골라 맛의 문제를 찾는 방식이 [페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/) 사고와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/)·직교배열 기반 축소는 무작정 케이스를 줄이는 작업이 아니다. 먼저 테스트 대상을 **요인(Factor)** 과 **수준(Level)** 으로 분해하고, 그다음 상호작용을 커버하는 최소 세트를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한 뒤, 마지막으로 업무상 금지 조합과 고위험 예외를 보정한다. 즉 “모델링 → 조합 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) → 위험 보완”의 3단계가 핵심이다.

```text
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│ 요인·수준 식별   │──▶│ Pairwise / OA 생성 │──▶│ 제약 반영·보정 케이스 │
│ Browser, Role… │    │ 2-way 균형 커버    │    │ 금지 조합·고위험 추가 │
└─────────────────┘    └──────────────────┘    └────────────────────┘
```

| 핵심 요소 | 설명 | 기술사 포인트 |
| :--- | :--- | :--- |
| 요인·수준 정의 | 입력 조건을 변수와 값으로 분해 | 분해가 잘못되면 축소 결과도 왜곡된다 |
| [페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/) 커버 | 모든 2개 요인 조합을 최소 세트로 포함 | [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 검출 효율과 비용 균형의 핵심 |
| 직교 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) (OA) | 수준 출현을 균형 있게 배치 | 대표성·통계적 균형 설명에 유리 |
| 제약 조건 처리 | 실제로 불가능한 조합 제거 | 금지 조합 누락 시 무의미한 테스트가 늘어난다 |
| 보정 케이스 추가 | 장애 이력·경계값·업무 중요 조합 보강 | 2-way 가정의 한계를 실무적으로 보완 |

중요한 것은 [페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/)가 전능한 해법이 아니라는 점이다. 보안 권한, 계산 로직, 복잡한 상태 전이처럼 3개 이상 조건의 상호작용이 중요한 영역은 3-way 이상 조합, [경계값 분석](/knowledge-base/studynote/04_software_engineering/11_testing_validation/414_boundary_value_analysis/), 위험 기반 테스트를 함께 써야 한다. 따라서 시험 답안에서는 “축소”와 함께 “보완”을 반드시 짝지어 써야 한다.

- **📢 섹션 요약 비유**: 여행 일정 표를 짤 때 모든 도시 조합을 다 가 볼 수는 없으니, 서로 다른 노선이 최소 한 번씩 만나도록 대표 경로를 짜는 것과 같다.

---

## Ⅲ. 비교 및 연결

[페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/)와 직교 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)은 전수 조합의 대체재이지만, 목표가 완전히 같지는 않다. 전수 조합은 누락이 없지만 비용이 급격히 커지고, [페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/)는 실무 효율이 높으며, 직교 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)은 균형성과 대표성을 강조한다. 따라서 상황에 따라 선택 기준이 달라진다.

| 비교 항목 | 전수 조합 테스트 | [페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/) 테스트 | 직교 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) (OA) 기반 테스트 |
| :--- | :--- | :--- | :--- |
| 기본 목적 | 모든 경우 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 2개 인자 상호작용 커버 | 균형 있는 조합 축소 |
| 테스트 수 | 가장 많음 | 크게 감소 | 감소하되 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 제약 고려 |
| 장점 | 누락 최소화 | 비용 대비 효율 우수 | 대표성·분석 가능성 우수 |
| 한계 | 시간·인력 부담 큼 | 3-way 이상 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 누락 가능 | 수준 수가 맞지 않으면 적용 제약 |
| 적합 영역 | 안전·규제상 전수 필요 구간 | 화면·[설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)·환경 조합 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 반복 실험형 조합 설계, 품질 비교 |

이 기법은 [동등 분할](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/630_equivalence_partitioning_boundary_value_analysis/), [경계값 분석](/knowledge-base/studynote/04_software_engineering/11_testing_validation/414_boundary_value_analysis/), 의사결정 테이블 테스트와 자연스럽게 연결된다. [동등 분할](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/630_equivalence_partitioning_boundary_value_analysis/)과 [경계값 분석](/knowledge-base/studynote/04_software_engineering/11_testing_validation/414_boundary_value_analysis/)으로 각 수준을 잘 정의한 뒤, [페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/)나 직교 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)로 조합 수를 줄이면 훨씬 실무적인 테스트 설계가 된다. 즉 축소 기법은 독립 기법이 아니라 <strong>다른 <a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/412_black_box_testing/">블랙박스 테스트</a> 기법을 운영 가능하게 만드는 결합 기술</strong>이다.

- **📢 섹션 요약 비유**: 모든 옷 조합을 다 입어 보는 건 전수 조합이고, 상의·하의·신발이 적어도 한 번씩 어울리게 입어 보는 건 [페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/)에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 먼저 입력 공간을 표로 정리한 뒤, 업무적으로 말이 안 되는 조합을 제거하고, [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 테스트 세트가 요구사항 추적표와 연결되는지 확인해야 한다. 특히 로그인 권한, 결제 통화, 기기 유형처럼 장애 영향이 큰 조건은 [페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/) 결과에만 의존하지 말고 별도 보강 케이스를 둬야 한다.

또한 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 도구를 썼더라도 결과를 그대로 신뢰하면 안 된다. 축소된 케이스가 실제 사용자 시나리오와 맞는지, [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 이력이 있던 조합이 빠지지 않았는지, 금지 조합 때문에 커버 공백이 생기지 않았는지를 사람이 검토해야 한다. 기술사 관점에서는 이 “모델 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)” 단계가 특히 중요하다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 테스트 대상을 요인과 수준으로 명확히 분해했는가?
2. 금지 조합과 의존 제약을 사전에 정리했는가?
3. 고위험 업무 조합은 별도 보정 케이스로 추가했는가?
4. 축소된 케이스가 요구사항·[결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 이력과 연결되는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 도구 결과를 검토 없이 그대로 수용하는 경우
- 2-way만으로 충분하다고 단정해 고위험 3-way 상호작용을 놓치는 경우
- 수준 정의가 부정확해 의미 없는 조합만 많이 남는 경우

- **📢 섹션 요약 비유**: 시험 범위를 줄여 준다고 핵심 단원을 빼 버리면 안 되듯, 조합 축소도 중요한 경우를 남겨 둔 채 줄여야 진짜 효율이 된다.

---

## Ⅴ. 기대효과 및 결론

[페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/)와 직교 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)을 올바르게 적용하면 테스트 설계 시간이 짧아지고, 실행 가능한 범위 안에서 상호작용 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 효과적으로 찾을 수 있다. 특히 다중 환경, 옵션 조합, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 테이블이 많은 서비스에서 비용 절감 효과가 크다. 또한 [테스트 케이스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/441_test_case/) 수가 줄어들면 자동화 유지보수 부담도 함께 낮아진다.

다만 축소는 품질을 희생하는 절감이 아니라, <strong>위험을 관리 가능한 범위로 재배치하는 설계 행위</strong>여야 한다. 따라서 기술사 답안의 결론은 “전수 조합의 대안”에서 끝나지 않고, “위험 기반 보완과 함께 쓰는 실무형 조합 최적화 기법”으로 정리하는 것이 적절하다.

- **📢 섹션 요약 비유**: 짐이 많다고 여행 가방을 무작정 줄이는 것이 아니라, 꼭 필요한 물건을 남기고 겹치는 물건만 빼는 일이 조합 축소의 본질이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [동등 분할](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/630_equivalence_partitioning_boundary_value_analysis/) ([Equivalence Partitioning](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/630_equivalence_partitioning_boundary_value_analysis/)) | 요인별 수준 정의의 출발점 |
| [경계값 분석](/knowledge-base/studynote/04_software_engineering/11_testing_validation/414_boundary_value_analysis/) ([Boundary Value Analysis](/knowledge-base/studynote/04_software_engineering/11_testing_validation/414_boundary_value_analysis/)) | 축소 전후에 고위험 경계 케이스를 보강 |
| 의사결정 테이블 테스트 | 규칙 조합을 구조화하는 상위 기법 |
| t-way 조합 테스트 | 3-way 이상 상호작용 보완 방향 |
| [요구사항 추적성](/knowledge-base/studynote/04_software_engineering/03_design_architecture/156_requirements_traceability_vertical_horizontal/) | 축소된 케이스와 요구사항 연결 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 위험 기반 테스트 | [페어와이즈](/knowledge-base/studynote/04_software_engineering/03_design_architecture/174_pairwise_comparison_priority_matrix/)의 누락 가능성을 보완 |

### 📈 관련 키워드 및 발전 흐름도

```text
동등 분할 · 경계값 분석
        │
        ▼
입력 요인·수준 모델링
        │
        ▼
페어와이즈 (2-way) 조합 축소
        │
        ▼
직교 배열 (OA) 기반 균형 설계
        │
        ▼
제약 처리 · 고위험 조합 보강 · t-way 확장
```

이 흐름은 [블랙박스 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/412_black_box_testing/) 기초 기법에서 시작해, 조합 폭발을 줄이고, 다시 위험 기반 보완으로 확장되는 실무 적용 순서를 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 맛이 다른 아이스크림이 많아도 모든 섞는 법을 다 먹어 볼 수는 없어요.
2. 그래서 두 가지 맛이 적어도 한 번씩은 만나게 대표 조합만 골라 보는 거예요.
3. 대신 알레르기처럼 꼭 확인해야 하는 특별한 조합은 따로 더 시험해 봐야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 498 / 530

← **이전**: [419. 화이트박스 변경 조건·결정 독립 커버리지 (MC/DC, Modified Condition/Decision Coverage)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/419_mc_dc/)
**다음**: [421. 정적 분석 기반 사이클로매틱 복잡도 제어 (Static Analysis Cyclomatic Complexity Control)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/421_process/) →

---
