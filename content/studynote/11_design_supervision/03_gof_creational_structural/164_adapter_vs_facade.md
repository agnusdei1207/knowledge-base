+++
title = "164. 어댑터 vs 퍼사드 (Adapter vs Facade)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) ([Adapter](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))는 맞지 않는 인터페이스를 연결하는 변환 패턴이고, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/) ([Facade](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/))는 복잡한 서브시스템을 단순한 진입점으로 감싸는 단순화 패턴이다.
> 2. **가치**: 둘 다 클라이언트를 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)하지만, [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 재사용성과 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 높이고 [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 복잡도와 결합도를 낮춘다.
> 3. **판단 포인트**: "호환되지 않아 못 붙는 문제"면 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)를, "너무 복잡해서 직접 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 힘든 문제"면 [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)를 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

소프트웨어가 커질수록 한 시스템 안에 레거시 코드, 외부 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/), 서로 다른 팀이 만든 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 함께 들어온다. 이때 흔히 부딪히는 문제가 두 가지다. 첫째는 클라이언트가 기대하는 인터페이스와 기존 컴포넌트가 제공하는 인터페이스가 달라 바로 연결할 수 없는 문제다. 둘째는 내부 서브시스템이 너무 많아, 클라이언트가 사용 절차를 모두 알아야만 기능을 호출할 수 있는 문제다.

[어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 첫 번째 문제를 해결한다. 기존 객체를 바꾸지 않고도 원하는 인터페이스처럼 보이게 만들어 재사용을 가능하게 한다. 반면 [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 두 번째 문제를 해결한다. 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 호출 순서, 예외 처리, 초기화 절차를 한곳에 모아 클라이언트는 간단한 고수준 인터페이스만 보게 만든다.

두 패턴이 자주 함께 언급되는 이유는 둘 다 "중간 래퍼"로 보이기 때문이다. 하지만 설계 의도는 다르다. [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)의 중심 질문은 "어떻게 맞출 것인가"이고, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)의 중심 질문은 "어떻게 숨길 것인가"다. 기술사 답안에서는 바로 이 의도 차이를 분리해서 설명해야 높은 점수를 얻는다.

- **📢 섹션 요약 비유**: [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 콘센트 규격이 달라서 꽂을 수 없을 때 쓰는 변환 플러그이고, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 수많은 스위치를 한 버튼으로 묶은 스마트 홈 패널이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 보통 클라이언트가 기대하는 대상 인터페이스 (Target Interface)를 구현하고, 내부에서 기존 객체 (Adaptee)를 호출한다. 즉 외부에는 새 규격처럼 보이지만 내부에서는 기존 규격을 그대로 쓴다. [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 특정 인터페이스를 맞추는 것이 아니라, 여러 서브시스템을 조합한 새 고수준 응용 프로그래밍 인터페이스 ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))를 제공한다.

아래 그림은 두 패턴의 구조 차이를 한눈에 보여준다.

```text
+--------------------------------------------------------------+
|                Adapter vs Facade 구조 비교                  |
+--------------------------------------------------------------+
| [Adapter]                                                   |
| Client --> Target Interface --> Adapter --> Adaptee            |
|          (기대 규격)         (변환)      (기존 규격)        |
|                                                              |
| [Facade]                                                    |
| Client --> Facade -+--> Subsystem A                           |
|                   +--> Subsystem B                           |
|                   +--> Subsystem C                           |
|          (단순 창구)   (복잡한 내부 협력은 내부에 숨김)      |
+--------------------------------------------------------------+
```

[어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 객체 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) (Object [Adapter](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))와 클래스 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) (Class [Adapter](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))로 나눌 수 있다. 실무에서는 상속보다 조합이 유연하므로 객체 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)가 더 많이 쓰인다. 예를 들어 `LegacySmsSender.sendLegacy()`를 `NotificationPort.send()` 형태로 감싸면, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 구체 구현을 모르고 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)만 사용하면 된다. 이는 [헥사고날 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/216_hexagonal_architecture_ports_and_adapters/) ([Hexagonal Architecture](/knowledge-base/studynote/11_design_supervision/06_exam_summary/366_process/))나 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)-[어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) 구조와도 자연스럽게 연결된다.

[퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 여러 컴포넌트의 호출 순서를 캡슐화하는 데 강하다. 예를 들어 주문 처리에서 재고 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/), 결제 승인, 배송 요청, 알림 발송이 순차적으로 필요하다면 `OrderFacade.placeOrder()` 하나로 묶을 수 있다. 이 경우 [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 단순 편의 메서드가 아니라, 업무 흐름의 응집된 경계가 된다. 다만 [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)가 너무 많은 책임을 떠안으면 거대한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 클래스로 비대해질 수 있으므로 하위 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 경계를 유지해야 한다.

| 비교 항목 | [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) ([Adapter](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)) | [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/) ([Facade](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)) |
| :--- | :--- | :--- |
| 해결 문제 | 인터페이스 불일치 | 서브시스템 복잡도 노출 |
| 주 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 1:1 변환 | 1:N 통합 |
| 외부에 보이는 것 | 기존 의도를 유지한 호환 인터페이스 | 새롭게 설계된 단순 인터페이스 |
| 내부 구현 변화 | 기존 객체 호출 방식 변환 | 여러 객체의 협력 흐름 조정 |
| 대표 효과 | 재사용, [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) | 단순성, 경계 명확화 |

- **📢 섹션 요약 비유**: [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 통역사처럼 한 사람의 말을 다른 언어로 바꿔 주고, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 여행사처럼 비행기·호텔·교통 예약을 한 창구에서 대신 처리해 준다.

---

## Ⅲ. 비교 및 연결

[어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)와 [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)를 정확히 구분하려면 비슷한 [구조 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/)과도 비교해야 한다. [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) ([Proxy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))는 같은 인터페이스를 유지한 채 접근 제어, [지연 로딩](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/), 원격 호출을 추가한다. [데코레이터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/) ([Decorator](/knowledge-base/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/))는 같은 인터페이스를 유지하면서 기능을 덧붙인다. 반면 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 인터페이스 자체를 바꾸고, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 고수준 단순 인터페이스를 새로 제시한다.

| 패턴 | 인터페이스 변화 | 핵심 목적 | 주 사용 맥락 |
| :--- | :--- | :--- | :--- |
| [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) | 변경됨 | [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 확보 | 레거시·외부 시스템 연동 |
| [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/) | 새 단순 인터페이스 제공 | 복잡도 은닉 | 서브시스템 묶음 제공 |
| [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) | 동일 | 접근 제어·대리 | 원격 객체, 캐시, 보안 |
| [데코레이터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/) | 동일 | 기능 확장 | 로깅, [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/), 암호화 |

[브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) ([Bridge](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/))와의 차이도 중요하다. [브리지](/knowledge-base/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/)는 처음부터 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)와 구현을 분리해 변화를 대비하는 사전 설계 패턴이다. 반면 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 이미 존재하는 인터페이스 차이를 사후에 봉합하는 패턴이다. 또한 [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 [중재자](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/) ([Mediator](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/))와 달리 구성요소 간 양방향 의사결정을 통제하기보다, 클라이언트 진입점을 단순하게 만드는 데 집중한다.

실제 시스템에서는 두 패턴이 함께 등장하기도 한다. 예를 들어 외부 결제사마다 다른 응용 프로그래밍 인터페이스 ([Application Programming Interface](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/))를 각 결제 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)로 통일한 뒤, 그 위에 주문 [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)가 결제·재고·알림을 한 번에 처리하도록 설계할 수 있다. 이처럼 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 하부 통합, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 상부 단순화에 강하다고 기억하면 실무 구분이 쉬워진다.

- **📢 섹션 요약 비유**: [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 서로 다른 나사를 맞추는 연결 부품이고, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 복잡한 기계의 조작 패널이다. 하나는 맞추는 문제를, 다른 하나는 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 쉽게 만드는 문제를 다룬다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)의 대표 사례는 외부 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 연동이다. 예를 들어 결제 게이트웨이 (Payment Gateway, PG) A사는 `approve(amount, cardInfo)`를 제공하고, B사는 `pay(requestJson)`을 제공한다면 내부 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)은 `PaymentPort.authorize()`만 알도록 하고 각 사별 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)에서 형식을 변환한다. 이렇게 하면 새 결제사를 추가해도 핵심 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 로직은 바꾸지 않아도 된다.

[퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 업무 흐름의 복잡도를 감추는 데 효과적이다. 전자상거래 주문 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)은 재고 예약, 가격 계산, 쿠폰 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 결제 요청, 배송 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 이벤트 발행 순으로 이어질 수 있다. 컨트롤러가 이 절차를 모두 알면 결합도가 급격히 높아진다. 이때 `CheckoutFacade.execute()` 같은 [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)를 두면 상위 계층은 "주문 처리"라는 유스케이스만 이해하면 되고, 세부 협력은 내부에서 관리된다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. **문제의 원인이 인터페이스 차이인가**: 그렇다면 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)가 1순위다.
2. **클라이언트가 호출 절차를 너무 많이 알아야 하는가**: 그렇다면 [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)가 적합하다.
3. <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/">퍼사드</a>가 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 규칙까지 과도하게 흡수하는가</strong>: 그 경우 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 분리와 [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/) 재검토가 필요하다.
4. <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/">어댑터</a>가 변환 이상 책임을 갖는가</strong>: 비즈니스 로직이 들어가면 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 경계가 흐려진다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 모든 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 한 클래스에 몰아 넣은 거대 [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)
- 변환 계층에 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 승인, 정산 등 핵심 비즈니스 로직까지 섞어 넣은 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)
- 내부 복잡도를 숨긴다는 이유로 장애 원인 추적이 안 되게 만든 무분별한 래핑

설계 답안에서는 "[어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 재사용을 위한 호환 계층, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 단순 사용을 위한 진입 계층"이라고 정리한 뒤, 실제 적용 예를 하나씩 붙이면 설득력이 높다. 특히 [객체지향 설계 원칙](/knowledge-base/studynote/04_software_engineering/04_testing_quality/242_solid_object_oriented_design_principles/) 중 [개방-폐쇄 원칙](/knowledge-base/studynote/11_design_supervision/06_exam_summary/356_process/) ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/)), [의존성 역전 원칙](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/106_dip_dependency_inversion_principle/) ([Dependency Inversion Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/), [DIP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/))과 연결하면 더 좋다.

- **📢 섹션 요약 비유**: [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 다른 회사 문서를 우리 양식으로 바꿔 주는 번역 담당자이고, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 여러 부서를 대신 돌며 일을 한 번에 접수해 주는 총무 창구다.

---

## Ⅴ. 기대효과 및 결론

[어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)를 잘 쓰면 기존 자산을 폐기하지 않고도 새로운 시스템에 편입할 수 있다. 이는 레거시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/), 외부 의존성 격리, 테스트 용이성 향상으로 이어진다. [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)를 잘 쓰면 상위 계층이 내부 구조를 몰라도 되므로 응용 계층이 단순해지고, 변경 영향도 특정 경계 안으로 가둘 수 있다.

하지만 두 패턴 모두 남용하면 오히려 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)만 늘어난다. [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)가 너무 많아지면 호출 경로가 길어져 디버깅이 어려워지고, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)가 과도하면 내부 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)보다 더 큰 비대 클래스로 변질된다. 따라서 패턴 적용의 기준은 "멋있어 보이는 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)"가 아니라 실제로 결합도와 변경 비용을 줄이는지 여부다.

결론적으로 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 연결의 문제를, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 노출의 문제를 해결한다. 둘의 차이를 의도로 기억하면, 레거시 통합과 계층 설계에서 훨씬 안정적인 판단을 할 수 있다.

- **📢 섹션 요약 비유**: [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 맞지 않는 부품을 연결해 기계를 살리고, [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 복잡한 기계 앞에 쉬운 버튼판을 붙여 누구나 쓸 수 있게 만든다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [구조 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/) (Structural Pattern) | 객체 조합으로 유연성을 높이는 Gang of Four (GoF) 패턴 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)-[어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) 아키텍처 (Ports and Adapters [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/)) | 외부 시스템을 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)로 격리하는 대표 설계 |
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 레이어 ([Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) Layer) | [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)처럼 유스케이스 진입점을 단순화하는 계층 |
| [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) ([Proxy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)) | 동일 인터페이스를 유지하며 접근을 제어하는 비교 대상 |
| [데코레이터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/) ([Decorator](/knowledge-base/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)) | 동일 인터페이스에 기능을 추가하는 비교 대상 |
| [OCP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) ([Open-Closed Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/)) | 변경 없이 확장 가능한 구조를 만드는 설계 원칙 |

### 📈 관련 키워드 및 발전 흐름도

```text
레거시 통합 · 외부 API 연동
    |
    v
어댑터 (Adapter)
    |
    +--> 포트-어댑터 아키텍처
    |
    v
서브시스템 증가 · 호출 절차 복잡화
    |
    v
퍼사드 (Facade)
    |
    v
서비스 레이어 · API 게이트웨이 · 유스케이스 경계 강화
```

이 흐름은 "[호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 해결"에서 시작해 "복잡도 은닉과 계층 경계 설계"로 확장되는 [구조 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/)의 활용 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 모양이 다른 장난감 배터리를 끼울 수 있게 도와주는 연결 부품이에요.
2. [퍼사드](/knowledge-base/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 버튼이 너무 많은 기계를 "시작" 버튼 하나로 쉽게 쓰게 해 주는 도우미예요.
3. 하나는 서로 안 맞는 것을 맞춰 주고, 다른 하나는 너무 복잡한 것을 쉽게 보여줘요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 220 / 530

<- **이전**: [163. 싱글톤 패턴의 단점과 DI (Singleton Drawbacks & Dependency Injection)](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/163_singleton_pattern_drawbacks/)
**다음**: [165. 브리지 vs 전략 패턴 (Bridge vs Strategy Pattern)](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/165_bridge_vs_strategy/) ->

---
