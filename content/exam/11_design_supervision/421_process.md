---
title: "Static Analysis Cyclomatic Complexity Control"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 사이클로매틱 복잡도는 제어 흐름 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) ([Control Flow](/studynote/01_computer_architecture/04_instruction_set_architecture/186_control_flow_instructions/) [Graph](/studynote/12_it_management/03_ea_isp/888_graph/), CFG) 상의 독립 경로 수를 나타내는 지표로, [정적 분석](/studynote/04_software_engineering/06_software_architecture/331_static_analysis/)을 통해 테스트 난이도와 유지보수 위험을 조기에 드러낸다.
> 2. **가치**: 복잡도 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 두면 “코드가 돌아가느냐”를 넘어 “변경 가능한 구조인가”를 지속적으로 관리할 수 있다.
> 3. **판단 포인트**: 복잡도 수치 자체보다 왜 높아졌는지, [테스트 케이스](/studynote/04_software_engineering/11_testing_validation/833_test_case/) 수와 리뷰 비용에 어떤 영향을 주는지, [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 초과 시 어떤 조치를 취하는지가 더 중요하다.

---

## Ⅰ. 개요 및 필요성

[정적 분석](/studynote/04_software_engineering/06_software_architecture/331_static_analysis/)에서 사이클로매틱 복잡도는 조건문, 반복문, 분기문이 만들어 내는 경로 수를 정량화하는 대표 지표다. 일반적으로 값이 커질수록 코드 이해가 어려워지고, 독립 경로를 모두 검증하기 위한 테스트 수가 늘어나며, 예외 흐름 누락 가능성도 함께 커진다. 그래서 이 지표는 단순한 “숫자 장식”이 아니라 설계 위험의 조기 경보 역할을 한다.

실무에서는 기능이 급하게 누적될수록 메서드 하나에 규칙과 예외가 몰리기 쉽다. 처음에는 if 문 몇 개 추가로 끝나는 것처럼 보이지만, 시간이 지나면 승인 조건, 권한 분기, 장애 우회 로직이 뒤엉켜 수정 자체가 두려운 코드가 된다. 사이클로매틱 복잡도는 이러한 구조적 비대화를 가장 먼저 드러내는 [신호](/studynote/02_operating_system/02_process_thread/130_signal/) 중 하나다.

기술사 답안에서는 복잡도 정의만 외우는 것으로는 부족하다. [정적 분석](/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 도구로 측정하고, [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)하며, 초과 시 [리팩토링](/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)과 테스트 보강으로 이어지는 <strong>통제 체계</strong>까지 써야 감리·품질관리 관점의 답안이 된다.

- **📢 섹션 요약 비유**: 골목길이 너무 많이 갈라진 동네는 길을 외우기 어렵듯, 분기가 많아질수록 코드도 길 잃기 쉬운 구조가 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

사이클로매틱 복잡도는 보통 제어 흐름 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)에서 계산하며, 실무적으로는 “결정점 수 + 1”로 이해해도 충분하다. [정적 분석](/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 도구는 소스 코드를 읽어 분기 구조를 식별하고, 함수·메서드·[파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 단위로 복잡도를 산출한 뒤, [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 초과 여부를 품질 게이트로 연결한다. 즉 <strong>측정 -> 판정 -> 조치</strong>가 핵심 메커니즘이다.

```text
+--------------+   +--------------+   +--------------+   +--------------+
| 소스 코드     |--->| CFG 생성      |--->| 복잡도 계산   |--->| 임계치 판정   |
| if / for / case|   | 경로·분기 모델 |   | M 값 산출     |   | 리팩토링 여부 |
+--------------+   +--------------+   +--------------+   +--------------+
```

복잡도는 보통 `M = E - N + 2P`로 표현한다. 여기서 `E`는 간선 수, `N`은 노드 수, `P`는 연결 요소 수다. 시험에서는 수식을 길게 전개하기보다 “독립 경로 수를 나타내며, [테스트 케이스](/studynote/04_software_engineering/11_testing_validation/833_test_case/) 최소 수와 밀접하다”는 의미를 정확히 쓰는 편이 실전적이다.

| 핵심 요소 | 설명 | 기술사 포인트 |
| :--- | :--- | :--- |
| 제어 흐름 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (CFG) | 코드의 분기·합류 구조를 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/)로 표현 | 분기 누락 없이 구조를 모델링해야 한다 |
| 사이클로매틱 복잡도 | 독립 경로 수를 나타내는 지표 | 테스트 수·이해 난이도와 직접 연결된다 |
| [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) | 허용 가능한 최대 복잡도 기준 | 공통 기준 없이 수치만 보면 실효성이 떨어진다 |
| 품질 게이트 | 빌드·리뷰 단계의 자동 경고 또는 차단 | 경고만 쌓이고 조치가 없으면 통제 실패다 |
| [리팩토링](/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 조치 | 메서드 분리, [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)화, 조기 반환 등 | 수치 감소와 [가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/) 개선이 함께 가야 한다 |

중요한 점은 복잡도가 높다고 무조건 나쁜 코드라고 단정할 수는 없다는 것이다. 규칙 엔진, 파서, 상태기계처럼 본질적으로 분기가 많은 영역도 있기 때문이다. 따라서 복잡도 지표는 절대 판결이 아니라, <strong>설명 책임을 요구하는 위험 지표</strong>로 해석해야 한다.

- **📢 섹션 요약 비유**: 갈림길이 많은 지하상가일수록 안내판이 더 필요하듯, 복잡도가 높은 코드는 더 강한 분해와 설명 장치가 필요하다.

---

## Ⅲ. 비교 및 연결

사이클로매틱 복잡도는 널리 쓰이지만, 모든 복잡성을 완벽히 설명하지는 못한다. 코드 길이, 중첩 깊이, 사람이 느끼는 이해 난이도는 다른 지표와 함께 봐야 한다. 따라서 기술사 답안에서는 “복잡도 지표 하나로 모든 품질을 판정하지 않는다”는 균형감이 중요하다.

| 비교 항목 | 라인 수 (Lines of [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), LOC) | 사이클로매틱 복잡도 | 인지 복잡도 (Cognitive Complexity) |
| :--- | :--- | :--- | :--- |
| 보는 대상 | 코드 양 | 독립 경로 수 | 사람이 읽는 난이도 |
| 강점 | 계산이 단순 | 테스트 경로 수와 연계 가능 | 중첩·[가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/) 문제에 민감 |
| 한계 | 짧아도 복잡할 수 있음 | 중첩의 심리적 부담을 충분히 반영 못함 | 도구·기준 차이가 존재 |
| 활용 포인트 | 규모 추정 | 품질 게이트, 테스트 계획 | [리팩토링](/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 우선순위 판단 |

또한 이 지표는 화이트박스 테스트의 분기 커버리지, [코드 스멜](/studynote/04_software_engineering/06_software_architecture/370_code_smell/) 탐지, [리팩토링](/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)과도 연결된다. 복잡도가 높으면 분기 커버리지 목표 달성이 어려워지고, 긴 메서드·조건문 중첩 같은 [코드 스멜](/studynote/04_software_engineering/06_software_architecture/370_code_smell/)과 함께 나타나는 경우가 많다. 결국 사이클로매틱 복잡도는 테스트와 설계를 이어 주는 <strong>중간 관리 지표</strong>다.

- **📢 섹션 요약 비유**: 책의 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 수가 많다고 어렵다고 단정할 수는 없지만, 갈래가 많은 추리소설은 줄거리를 따라가기 더 힘든 것과 비슷하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 함수 단위로 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)를 두고, [정적 분석](/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 결과를 코드 리뷰와 [지속적 통합](/studynote/04_software_engineering/02_requirements_analysis/076_ci_continuous_integration/) ([Continuous Integration](/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/), [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)) 파이프라인에 연결하는 방식이 일반적이다. 예를 들어 일반 업무 로직은 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) 이하, 핵심 계산 모듈은 15 이하처럼 기준을 두고, 초과 시 빌드 경고·리뷰 강화·테스트 보강을 요구할 수 있다. 중요한 것은 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 수치보다 <strong>예외 승인 절차와 후속 조치</strong>다.

복잡도 개선의 대표 방법으로는 메서드 분리, 조건식 명명, [전략 패턴](/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/) 적용, 조기 반환, 상태 객체 분리 등이 있다. 다만 수치만 낮추려다 함수만 잘게 쪼개고 문맥 이해는 더 어려워지는 경우도 있으므로, [가독성](/studynote/04_software_engineering/06_software_architecture/333_readability_vs_efficiency/)과 책임 분리가 함께 좋아졌는지 반드시 확인해야 한다.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 함수·메서드 단위 복잡도 [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)가 문서화되어 있는가?
2. [임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/) 초과 시 리뷰 강화 또는 [리팩토링](/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 절차가 있는가?
3. 복잡도 높은 코드에 대응하는 [테스트 케이스](/studynote/04_software_engineering/11_testing_validation/833_test_case/) 수가 충분한가?
4. 예외 승인 모듈이라면 사유와 대체 통제가 기록되는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 경고를 계속 무시해 복잡도 리포트가 장식물로 전락하는 경우
- 분기 로직을 감추기만 하고 책임 분리는 하지 않는 경우
- 단순 수치 하향만 노려 함수 분할 후 오히려 추적성이 나빠지는 경우

- **📢 섹션 요약 비유**: 교차로가 많아진 도시는 [신호](/studynote/02_operating_system/02_process_thread/130_signal/)체계와 우회로가 필요하듯, 분기가 많은 코드는 기준과 정리가 없으면 사고가 늘어난다.

---

## Ⅴ. 기대효과 및 결론

사이클로매틱 복잡도 통제를 제대로 운영하면 테스트 계획 수립이 쉬워지고, 리뷰 대상 우선순위가 분명해지며, 장애가 잦은 코드를 조기에 식별할 수 있다. 또한 신규 인력이 코드를 이해하는 데 필요한 시간이 줄어들어 유지보수 생산성도 높아진다. 즉 복잡도 관리는 개발 품질과 운영 안정성을 동시에 개선하는 관리 수단이다.

결론적으로 [정적 분석](/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 기반 복잡도 제어는 “복잡한 코드를 벌주는 규칙”이 아니라, 변경 비용을 감당 가능한 수준으로 유지하기 위한 설계 통제다. 기술사 답안에서는 정의·계산식·[임계치](/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/)·조치 체계를 함께 제시해 <strong>측정 가능한 품질 관리 프레임</strong>으로 정리하는 것이 핵심이다.

- **📢 섹션 요약 비유**: 길찾기 앱이 복잡한 길을 미리 알려 주면 막히기 전에 우회하듯, 복잡도 지표는 코드가 막히기 전에 구조를 손보게 해 준다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 제어 흐름 [그래프](/studynote/08_algorithm_stats/04_datastructure/070_graph_datastructure/) (CFG) | 복잡도 계산의 구조적 기반 |
| 분기 커버리지 (Branch Coverage) | 독립 경로 검증과 직접 연결 |
| [코드 스멜](/studynote/04_software_engineering/06_software_architecture/370_code_smell/) ([Code Smell](/studynote/12_it_management/05_security_compliance/365_5_solid_code_smell/)) | 긴 메서드·중첩 조건의 조기 징후 |
| [리팩토링](/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) ([Refactoring](/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/)) | 복잡도 초과 시 대표 개선 수단 |
| [정적 분석](/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 도구 | 자동 측정과 품질 게이트 구현 |
| 인지 복잡도 | 사람이 느끼는 이해 난이도 보완 지표 |

### 📈 관련 키워드 및 발전 흐름도

```text
코드 리뷰 경험칙
      |
      v
정적 분석 자동 측정
      |
      v
사이클로매틱 복잡도 임계치 관리
      |
      v
리팩토링 · 테스트 보강 · CI 품질 게이트
      |
      v
유지보수성 향상 · 장애 예방 · 설계 단순화
```

이 흐름은 사람의 감각적 리뷰에서 출발해, 자동 측정과 품질 게이트를 거쳐, 다시 설계 개선으로 이어지는 [정적 분석](/studynote/04_software_engineering/06_software_architecture/331_static_analysis/)의 관리 순환을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 길이 한 갈래면 쉽게 가지만, 갈림길이 많으면 길을 헷갈리기 쉬워요.
2. 코드도 갈림길이 많아질수록 시험해 볼 길이 늘어나고 실수하기 쉬워져요.
3. 그래서 너무 복잡해지기 전에 길을 단순하게 다시 나누는 거예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 499 / 530

<- **이전**: [420. 페어와이즈·직교배열 기반 조합 축소 (Pairwise & Orthogonal Array Reduction)](/studynote/11_design_supervision/06_exam_summary/420_process/)
**다음**: [422. 동적 성능 메모리 누수 진단 (Dynamic Performance Memory Leak Diagnostics)](/studynote/11_design_supervision/06_exam_summary/422_audit/) ->

---
