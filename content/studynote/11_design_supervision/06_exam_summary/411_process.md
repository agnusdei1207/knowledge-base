+++
title = "411. 테스트 주도 개발 (Test-Driven Development)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)
1. **본질**: [테스트 주도 개발](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/077_tdd_test_driven_development/) (Test-Driven Development, [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/))은 테스트를 먼저 작성해 요구사항을 실행 가능한 명세로 고정한 뒤 구현을 진행하는 개발 방식이다.
2. **가치**: [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)을 조기에 드러내고 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) ([Refactoring](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/))의 안전망을 제공해 설계 품질과 변경 대응력을 높인다.
3. **판단 포인트**: 테스트 단위의 적절성, 실패 원인의 명확성, 과도한 [목 객체](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/399_mock_object/) ([Mock Object](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/399_mock_object/)) 의존 여부를 함께 봐야 한다.

## Ⅰ. 개요 및 필요성
TDD는 레드-그린-리팩터 (Red-Green-[Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/)) 사이클로 대표된다. 먼저 실패하는 테스트를 만들고, 그 테스트를 통과하는 최소 구현을 작성한 뒤, 마지막에 중복 제거와 구조 개선을 수행한다. 이 순환은 코드를 나중에 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 방식이 아니라, 요구사항을 작은 단위로 쪼개며 설계를 진화시키는 방식이라는 점이 중요하다.

설계감리나 기술사 서술에서는 “TDD는 품질보증 활동이면서 설계 유도 기법”이라는 관점이 핵심이다. 테스트가 먼저 존재하면 인터페이스가 지나치게 복잡한지, 결합도가 높은지, 의존성이 숨겨져 있는지를 구현 전에 발견할 수 있다. 특히 변경이 잦은 업무 시스템에서는 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구현 속도보다 장기 유지보수성이 더 중요하므로 TDD의 효과가 커진다.

```text
+------------+   +------------+   +------------+
| 실패 테스트 |--->| 최소 구현   |--->| 구조 개선   |
+------------+   +------------+   +------------+
```

따라서 시험 답안에서는 “테스트를 많이 만드는 기법”이라고 좁게 정의하지 말고, 요구사항을 빠르게 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능한 단위로 분해하는 설계 절차라고 써야 한다.
- **📢 섹션 요약 비유**: 퍼즐 그림을 먼저 보고 조각을 맞추면 어디가 비었는지 빨리 알 수 있다.

## Ⅱ. 아키텍처 및 핵심 원리
TDD의 핵심 원리는 짧은 [피드백 루프](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/), 자동화된 회귀 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 그리고 설계 단순화다. 테스트가 통과하지 못하면 구현이 끝난 것이 아니며, 테스트가 과하게 복잡하면 설계가 틀어졌다는 신호로 읽어야 한다. 실무에서는 [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) ([Unit Test](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/)), [목 객체](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/399_mock_object/), [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/) ([Test Double](/knowledge-base/studynote/04_software_engineering/11_testing_validation/458_test_double/)), 연속적 통합 ([Continuous Integration](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/019_continuous_integration/), [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/))과 함께 운영된다.

| 단계 | 핵심 활동 | 기술사 답안 포인트 |
|:---|:---|:---|
| Red | 실패 테스트 작성, 기대 결과 명시 | 요구사항을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능한 문장으로 바꾸었는지 설명 |
| Green | 최소 코드 구현, 테스트 통과 | 과잉 설계 없이 가장 단순한 해결을 택했는지 제시 |
| [Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) | 중복 제거, 구조 개선, 회귀 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 테스트가 [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 안전망으로 기능하는지 정리 |

```text
+------+   +------+   +----------+
| 요구  |--->| 테스트 |--->| 구현/개선 |
+------+   +--+---+   +----+-----+
              |            |
              +----회귀 검증+----반복
```

여기서 중요한 설계 원리는 [의존성 주입](/knowledge-base/studynote/04_software_engineering/06_software_architecture/337_dependency_injection/) ([Dependency Injection](/knowledge-base/studynote/04_software_engineering/06_software_architecture/337_dependency_injection/)), 순수 함수화, 경계 분리다. 테스트하기 어려운 코드는 대개 책임이 과도하게 섞여 있고, 외부 자원 의존성이 강하다. 즉 TDD는 테스트 기술이면서 동시에 좋은 객체지향 설계를 강제하는 장치다.
- **📢 섹션 요약 비유**: 블록을 한 칸씩 쌓아 보고 흔들리지 않으면 다음 칸을 올리는 방식과 같다.

## Ⅲ. 비교 및 연결
시험에서는 TDD를 선구현 후테스트, [행위 주도 개발](/knowledge-base/studynote/11_design_supervision/06_exam_summary/412_process/) ([Behavior-Driven Development](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/126_bdd_behavior_driven_development_given_when_then/), [BDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/165_bdd_behavior_driven_development/)), 테스트 자동화 전반과 구분해 써야 한다. TDD는 개발자 관점의 내부 설계 품질 확보에 강하고, BDD는 사용자 행위와 비즈니스 언어 정렬에 강하다. 따라서 둘은 대체 관계보다 상호 보완 관계에 가깝다.

| 비교 항목 | [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) | 선구현 후테스트 | [BDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/165_bdd_behavior_driven_development/) |
|:---|:---|:---|:---|
| 출발점 | 실패 테스트 | 기능 구현 | 시나리오와 행위 |
| 주된 목적 | 설계 개선, [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 예방 | 사후 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 공통 언어와 수용 기준 정렬 |
| 장점 | 빠른 피드백, [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 안전성 | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 개발 체감 속도 | [이해관계자](/knowledge-base/studynote/04_software_engineering/03_design_architecture/173_stakeholder_identification_impact_matrix/) 소통 용이 |
| 주의점 | 테스트 유지비, 과도한 [목 객체](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/399_mock_object/) | [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)이 늦게 발견됨 | 문서화만 남고 자동화가 약해질 수 있음 |

또한 TDD는 테스트 피라미드 (Test Pyramid), [회귀 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/410_regression_test/), [지속적 전달](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/020_continuous_delivery/) ([Continuous Delivery](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/), CD)과 연결된다. [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/)가 촘촘해야 상위 통합 테스트와 [인수 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/406_acceptance_test_uat/) 수를 합리적으로 유지할 수 있다.
- **📢 섹션 요약 비유**: 매일 받아쓰기를 하는 것은 TDD이고, 학기 말 시험만 보는 것은 선구현 후테스트에 가깝다.

## Ⅳ. 실무 적용 및 기술사 판단
TDD는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 규칙이 복잡하고 변경이 잦은 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 계산 로직, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 엔진, 정산 기능에서 특히 강하다. 반면 화면 중심 [프로토타입](/knowledge-base/studynote/04_software_engineering/04_testing_quality/257_prototype_pattern_object_cloning/), 짧은 일회성 스크립트, 외부 시스템 의존이 지나치게 강한 영역에서는 비용 대비 효과가 낮을 수 있다. 따라서 적용 범위를 계층별로 나누어 판단하는 것이 좋다.

기술사 답안에서는 TDD의 성공 조건도 함께 써야 한다. 테스트 실행 속도가 느리면 개발자는 사이클을 포기하고, [목 객체](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/399_mock_object/)가 지나치면 실제 통합 문제를 숨긴다. 또한 테스트 코드도 제품 자산이므로 중복과 취약한 단정문을 지속적으로 정리해야 한다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- 실패 테스트가 요구사항을 명확히 설명하는가?
- 테스트가 너무 구현 세부사항에 종속되어 있지 않은가?
- 외부 연계는 계약 테스트나 통합 테스트와 함께 보완되고 있는가?
- 테스트 실행 시간이 짧아 개발 [피드백 루프](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/005_feedback_loop/)를 유지하는가?
- [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 이후에도 테스트가 의미 있는 회귀 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 역할을 하는가?

최종적으로 TDD는 “테스트 우선”이 아니라 “[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능성 우선”의 문화로 봐야 한다. 이 점을 적으면 실무적 설득력이 높다.
- **📢 섹션 요약 비유**: 연필로 먼저 스케치를 그려 두면 지우고 고치기가 쉬워 큰 그림을 망치지 않는다.

## Ⅴ. 기대효과 및 결론
TDD를 정착시키면 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 발견 시점이 앞당겨지고, 설계가 작은 책임 단위로 정리되며, 변경 시 회귀 위험이 낮아진다. 결과적으로 코드 품질뿐 아니라 개발팀의 의사결정 속도와 자신감도 높아진다. 특히 조직 차원에서는 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 기반 자동 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 문화와 결합될 때 효과가 극대화된다.

결론적으로 기술사 답안의 핵심은 “TDD가 코드를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다”가 아니라 “TDD가 설계를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능하게 만든다”는 문장에 있다. 테스트 작성 비용과 유지 비용도 인정하되, 장기 총비용 절감 효과를 균형 있게 제시하는 것이 바람직하다.
- **📢 섹션 요약 비유**: 건물 모형을 먼저 검토하고 본공사에 들어가면 큰 실수를 훨씬 줄일 수 있다.

### 📌 관련 개념 맵
- [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) -> 실패 테스트 -> 요구사항 명세화
- 실패 테스트 -> 최소 구현 -> 과잉 설계 [억제](/knowledge-base/studynote/09_security/13_secops_ir_forensics/656_ir_containment/)
- 테스트 자동화 -> 회귀 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) -> [리팩토링](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/) 안전망
- [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 파이프라인 -> 빠른 피드백 -> 품질 문화 정착

### 📈 관련 키워드 및 발전 흐름도
수동 테스트 -> [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) 자동화 -> [TDD](/knowledge-base/studynote/12_it_management/04_sdlc_testing/164_tdd_test_driven_development/) -> [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/) 연계 -> 테스트 피라미드 최적화 -> [지속적 전달](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/020_continuous_delivery/) 기반 품질관리

- 핵심 키워드: Red-Green-[Refactor](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/213_refactoring_cloud_native_rearchitecture/), [회귀 테스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/410_regression_test/), [목 객체](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/399_mock_object/), [테스트 더블](/knowledge-base/studynote/12_it_management/05_security_compliance/367_test_double_isolation/), 설계 단순화

### 👶 어린이를 위한 3줄 비유 설명
1. 레고를 만들기 전에 설명서 그림 한 칸을 먼저 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 게 TDD예요.
2. 그림대로 한 칸을 맞추고 나서 흔들리지 않으면 다음 칸으로 넘어가요.
3. 그래서 마지막에 큰 성을 만들 때도 어디가 잘못됐는지 금방 찾을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 489 / 530

<- **이전**: [410. 프로미스·퓨처 기반 비동기 처리 설계 (Promise/Future)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/410_process/)
**다음**: [412. 행위 주도 개발 (Behavior-Driven Development)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/412_process/) ->

---
