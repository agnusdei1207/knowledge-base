+++
title = "168. 템플릿 메서드와 팩토리 메서드 결합 (Template Method + Factory Method)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/) ([Template Method](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/))는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 고정된 순서를 상위 클래스가 통제하고, [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) ([Factory Method](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/))는 그 흐름 안에서 필요한 구체 객체 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 하위 클래스에 위임하는 결합 구조다.
> 2. **가치**: 절차의 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 유지하면서 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지점만 다형적으로 바꿀 수 있어, 프레임워크·[배치 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/)·문서 변환처럼 흐름은 같고 제품만 달라지는 문제에서 중복을 크게 줄인다.
> 3. **판단 포인트**: 처리 순서는 고정되어야 하지만 "어떤 객체를 만들 것인가"만 바뀐다면 이 조합이 적합하다. 반대로 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 전체를 런타임에 바꿔야 한다면 [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/) ([Strategy Pattern](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/))과 합성 기반 설계를 우선 검토해야 한다.

---

## Ⅰ. 개요 및 필요성

[템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)와 [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/)의 결합은 "흐름의 고정"과 "[생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)의 변형"을 동시에 해결하는 객체지향 설계 방식이다. 상위 클래스는 `open → create → process → close` 같은 절차를 [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)로 고정하고, 하위 클래스는 중간의 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 단계를 [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/)로 재정의해 자신에게 맞는 객체를 제공한다. 즉, [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 뼈대는 재사용하고 제품 선택만 확장하는 구조다.

이런 결합이 필요한 이유는 많은 실무 로직이 "순서는 같지만 다루는 객체가 다르다"는 특징을 갖기 때문이다. 예를 들어 보고서 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 메시지 발송, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 변환, 배치 적재는 모두 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)·[생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·처리·정리라는 큰 순서가 비슷하다. 이때 각 경우마다 전체 절차를 복사하면 중복이 커지고, 반대로 모든 분기를 조건문으로 몰아넣으면 상위 로직이 비대해진다.

아래 그림은 왜 두 패턴을 함께 쓰는지 직관적으로 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">같은 절차, 다른 산출물이라는 문제를 해결하는 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">공통 흐름: validate ─▶ create product ─▶ execute ─▶ cleanup</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">변하는 부분: create product</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PDF면 PdfDocument, SMS면 SmsSender, DB면 OracleSession</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">해결: 흐름은 Template Method, 생성은 Factory Method로 분리</div></div>
</div>
</div>



이 구조는 [할리우드 원칙](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/111_hollywood_principle/) ([Hollywood Principle](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/111_hollywood_principle/)), 즉 "Don't [call](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) us, we'll [call](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) you"와도 맞닿아 있다. 하위 클래스가 절차 전체를 주도하지 않고, 상위 클래스가 정한 시점에만 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지점을 열어 준다는 점에서 제어 역전 (IoC, Inversion of Control)의 전형적 형태다.

- **📢 섹션 요약 비유**: 공연 연출가는 리허설 순서를 정해 두고, 필요한 소품만 장면마다 바꿔 끼운다. 장면 순서를 배우가 정하는 것이 아니라, 무대 감독이 정한 흐름 속에서 소품만 갈아 끼우는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리

이 결합 구조의 핵심은 [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)가 전체 실행 순서를 고정하고, [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/)가 그 안의 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 책임만 하위 클래스로 미루는 것이다. 상위 클래스는 공통 전처리·예외 처리·후처리·로깅을 보장할 수 있고, 하위 클래스는 구체 제품과 제품별 처리 규칙만 구현하면 된다. 덕분에 공통 절차는 한 곳에서 관리되고, 변형 지점은 명확하게 제한된다.

아래 구조도는 [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/) 안에 [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/)가 어떻게 들어가는지 보여준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">AbstractProcessor (상위 클래스)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">template run()</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. validate() ── 공통 단계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. createProduct() ── Factory Method</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. process(product) ── 추상/훅 단계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. audit() ── 공통 단계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5. cleanup() ── 공통 단계</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">PdfProcessor</div><div class="kb-diagram-cell">SmsProcessor</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">createProduct() -&gt; PDF</div><div class="kb-diagram-cell">createProduct() -&gt; SMS</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">process(product)</div><div class="kb-diagram-cell">process(product)</div></div>
</div>
</div>



| 지점 | 누가 책임지는가 | 의미 |
| :--- | :--- | :--- |
| [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/) | 상위 클래스 | 실행 순서, 예외 처리, 공통 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 고정 |
| [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) | 하위 클래스 | 구체 제품 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 책임 위임 |
| 추상 단계 | 하위 클래스 | 제품별 핵심 처리 로직 구현 |
| 훅 메서드 (Hook Method) | 상위 또는 하위 클래스 | 선택적 확장 지점 제공 |

이때 [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/)는 [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)의 한 단계로 들어갈 때 가장 강력해진다. [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시점이 흐름 안에 고정되므로, 상위 클래스는 "언제 만들지"를 통제하고 하위 클래스는 "무엇을 만들지"만 결정한다. 그래서 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)과 절차의 관심사가 서로 섞이지 않고, [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/)) 관점에서도 상위 흐름 수정 없이 하위 타입만 추가해 확장할 수 있다.

- **📢 섹션 요약 비유**: 레시피는 요리 순서를 고정하고, "재료 꺼내기" 단계에서 한식 셰프는 된장, 양식 셰프는 치즈를 꺼내는 식이다. 언제 재료를 넣을지는 레시피가 정하고, 어떤 재료를 꺼낼지는 셰프가 정한다.

---

## Ⅲ. 비교 및 연결

이 조합을 이해하려면 단독 [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/), 단독 [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/), 그리고 [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)과 비교해야 한다. 단독 [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)는 절차의 골격만 재정의하게 해 주지만, 제품 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)이 복잡해지면 결국 `new`나 조건문이 상위 클래스에 남기 쉽다. 단독 [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/)는 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 다형성은 제공하지만, [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 이후의 실행 순서와 공통 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 별도로 보장하지 못한다.

| 비교 항목 | Template + Factory | [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/) 단독 | [Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) + [Abstract Factory](/knowledge-base/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/) |
| :--- | :--- | :--- | :--- |
| 주된 변화 축 | 흐름 고정 + [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 가변 | 흐름 고정 | 런타임 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)·[생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 모두 가변 |
| 결합 방식 | [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 중심 | [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 중심 | 합성 중심 |
| 장점 | 절차 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)과 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 확장 동시 확보 | 구조 단순 | 런타임 교체와 테스트 유연성 우수 |
| 약점 | 계층 깊어지면 취약한 기반 클래스 위험 | [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 책임이 새기 쉬움 | 객체 수와 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 복잡도 증가 |
| 적합 상황 | 프레임워크, 배치, 문서/채널 처리 | 단순 공통 로직 | 동적 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 변경이 잦은 시스템 |

또한 이 조합은 [추상 팩토리](/knowledge-base/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/) ([Abstract Factory](/knowledge-base/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/))와도 연결된다. [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/) 안에서 단일 제품이 아니라 "연관된 제품군"을 만들어야 한다면, [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) 하나 대신 [추상 팩토리](/knowledge-base/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/)를 주입하는 편이 더 적합하다. 즉 변화 축이 한 제품인지, 제품군 전체인지에 따라 결합 패턴도 달라진다.

프레임워크 관점에서는 스프링 (Spring)의 일부 추상 클래스나 배치 템플릿 구조에서 유사한 아이디어를 자주 볼 수 있다. 초기화 순서·[트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/)·예외 처리 같은 공통 골격은 프레임워크가 쥐고, 실제 리소스 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)과 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 처리는 확장 클래스가 담당하는 방식이다.

- **📢 섹션 요약 비유**: 템플릿+팩토리 조합은 정해진 여행 일정표에 맞춰 도시마다 다른 호텔만 예약하는 것이고, [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/)은 아예 여행 코스 자체를 그날그날 바꾸는 것에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 이 조합이 잘 맞는 대표 사례는 "처리 파이프라인은 같지만 채널별 자원만 다른" 시스템이다. 예를 들어 알림 플랫폼이 `요청 검증 → 발송 객체 생성 → 발송 실행 → 결과 감사 → 정리` 흐름을 공통으로 갖고, 이메일·문자·푸시마다 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 발송 객체와 처리 세부가 다르다고 하자. 이때 상위 클래스는 재시도, 로깅, [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 통일하고, 하위 클래스는 `EmailSender`, `SmsSender`, `PushSender` [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 책임지면 된다.

중요한 판단 포인트는 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)의 깊이와 변화 방향이다. 변형이 두세 종류이고 실행 순서가 장기간 안정적이라면 이 조합이 매우 깔끔하다. 하지만 고객별 규칙, 국가별 규칙, 채널별 규칙이 한꺼번에 늘어나면 하위 클래스가 폭증하고, 상위 클래스 변경이 연쇄 영향을 주는 취약한 기반 클래스 (Fragile Base Class) 문제가 나타날 수 있다.

### 적용 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 공통 절차의 순서를 상위 클래스가 반드시 통제해야 하는가?
2. 달라지는 핵심이 "객체 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)"[인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/), 아니면 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 전체인가?
3. 런타임에 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 교체가 필요한가, 아니면 컴파일 타임 확장으로 충분한가?
4. 테스트에서 가짜 제품([Fake](/knowledge-base/studynote/04_software_engineering/11_testing_validation/463_fake_test_double/) Product) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)으로 흐름 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 가능한가?

### 대표 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 상위 클래스 안에 `if-else`로 제품 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 남겨 [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) 의미를 없애는 설계
- 템플릿 단계가 너무 많아 하위 클래스가 무엇을 구현해야 하는지 불명확한 설계
- 런타임 교체가 필요한 문제를 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 계층으로만 해결하려는 설계

기술사 답안에서는 "흐름의 표준화"와 "[생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)의 다형화"를 동시에 얻지만, [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 기반이므로 계층 폭발과 유연성 한계를 함께 언급해야 완성도가 높다. 즉 이 조합은 좋은 기본틀이지만, 변화 축이 커지면 합성 기반 전환 시점을 판단해야 한다.

- **📢 섹션 요약 비유**: 회사 표준 업무 절차는 본사가 정해 두고, 각 지점은 자기 지역에 맞는 물품만 조달하는 방식과 같다. 다만 지점 규칙이 너무 많아지면 매뉴얼보다 현장 재량 체계가 더 나을 수도 있다.

---

## Ⅴ. 기대효과 및 결론

[템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)와 [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/)를 함께 쓰면 공통 절차를 한 번만 정의하면서도, [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되는 객체와 처리 세부를 제품별로 유연하게 분기할 수 있다. 이는 코드 중복 감소, [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 확보, 테스트 단위 분리, 프레임워크 확장점 제공 측면에서 큰 장점이 있다. 특히 공통 전처리와 예외 처리를 상위 클래스에 묶어 두면 운영 품질을 표준화하기 쉽다.

반면 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 기반인 만큼 계층이 깊어질수록 수정 비용이 커질 수 있고, 런타임 조합이 필요한 현대 애플리케이션에는 다소 경직될 수 있다. 그래서 이 조합은 "흐름은 안정적이고 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)만 달라지는 문제"에서 가장 빛난다. 변화 축이 커지는 순간에는 [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/), [의존성 주입](/knowledge-base/studynote/04_software_engineering/06_software_architecture/337_dependency_injection/) ([Dependency Injection](/knowledge-base/studynote/04_software_engineering/06_software_architecture/337_dependency_injection/)), [추상 팩토리](/knowledge-base/studynote/04_software_engineering/04_testing_quality/255_abstract_factory_pattern_object_families/) 등 합성 기반 도구로 넘어가는 것이 더 바람직하다.

결론적으로 이 패턴 조합은 "상위 클래스가 박자를 잡고, 하위 클래스가 필요한 도구를 꺼내는 구조"로 기억하면 된다. [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 순서를 지키면서도 제품별 확장을 열고 싶을 때 가장 교과서적인 선택이다.

- **📢 섹션 요약 비유**: 오케스트라 지휘자는 곡의 순서를 바꾸지 않지만, 연주할 악기 편성은 곡에 따라 달라질 수 있다. 곡의 흐름은 고정하고 필요한 악기만 바꾸는 것이 바로 이 조합의 핵심이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [템플릿 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/) ([Template Method](/knowledge-base/studynote/04_software_engineering/04_testing_quality/269_template_method_pattern/)) | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 고정된 순서와 공통 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 제공하는 상위 틀 |
| [팩토리 메서드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/) ([Factory Method](/knowledge-base/studynote/04_software_engineering/04_testing_quality/254_factory_method_pattern_subclass_creation/)) | 템플릿 안의 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 지점을 하위 타입별로 확장 |
| 훅 메서드 (Hook Method) | 필수 단계와 선택 단계의 경계를 조절하는 보조 확장점 |
| [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/)) | 상위 클래스 수정 없이 하위 타입 추가로 확장 가능 |
| [Strategy Pattern](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 자체를 런타임 교체해야 할 때의 합성 기반 대안 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">중복된 절차 로직 발견</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Template Method로 공통 흐름 고정</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">생성 지점 분리 필요</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Factory Method 결합</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">제품군 확장 시 Abstract Factory · DI</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">동적 정책 전환 시 Strategy 중심 구조</div>
</div>
</div>



이 흐름도는 클래스 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 기반 재사용이 점차 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 추상화와 합성 기반 설계로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 선생님은 "준비하기 → 만들기 → 검사하기 → 정리하기" 순서를 항상 똑같이 정해 둬요.
2. 그런데 만들기 시간에 종이비행기를 만들지, 종이배를 만들지는 반마다 달라요.
3. 순서는 선생님이 지키게 하고, 무엇을 만들지는 각 반이 정하게 한 것이 이 패턴 조합이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 224 / 530

← **이전**: [167. 추상 팩토리 팩토리 클래스 도출 (Abstract Factory Derivation)](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/167_abstract_factory_factory_derivation/)
**다음**: [169. 정적 팩토리 메서드 (Static Factory Method)](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/169_static_factory_method/) →

---
