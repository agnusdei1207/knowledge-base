---
title: "Decorator vs Proxy"
date: "2026-04-21"
tags:
  - "studynote-design-supervision"
weight: 166
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/) ([Decorator](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/))와 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) ([Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))는 모두 동일 인터페이스로 원본 객체를 감싸는 래퍼 구조를 쓰지만, [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 책임 추가가 목적이고 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/)가 목적이다.
> 2. **가치**: 두 패턴을 구조가 아니라 의도로 구분할 수 있어야 기능 확장, 보안, 캐시, [지연 로딩](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/), 원격 호출 같은 요구사항에 맞는 설계를 선택할 수 있다.
> 3. **판단 포인트**: 클라이언트가 어떤 래퍼를 적용할지 직접 조합하면 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)에 가깝고, 클라이언트가 원본처럼 쓰는 사이 중간에서 제어가 개입하면 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)에 가깝다.

---

## Ⅰ. 개요 및 필요성

[데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)와 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 GoF (Gang of Four) [구조 패턴](/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/)에서 가장 자주 혼동되는 쌍이다. 둘 다 Subject 인터페이스를 구현하고, 내부에 실제 객체를 참조하며, 호출을 위임한다. 클래스 다이어그램만 보면 거의 같은 모양이어서 "둘이 뭐가 다른가"라는 질문이 자연스럽게 나온다.

하지만 설계에서 중요한 것은 모양이 아니라 시스템이 그 래핑을 왜 도입했는가이다. 기능을 덧붙이려는가, 아니면 접근 시점을 감시·[지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)·보호하려는가에 따라 유지보수 방식과 테스트 포인트가 달라진다. 이 차이를 모르면 [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/), [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 로깅, [압축](/studynote/02_operating_system/06_memory_management/347_compaction/), [지연 로딩](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/) 같은 실무 구현을 패턴 이름만 바꿔 부르는 수준에서 멈추게 된다.

```text
+--------------------------------------------------------------------+
|            같은 외형, 다른 질문: "무엇을 위해 감쌌는가?"          |
+--------------------------------------------------------------------+
| Client --> Wrapper --> Real Object                                  |
|                                                                    |
| If goal = add behavior      -> Decorator                           |
| If goal = control access    -> Proxy                               |
|                                                                    |
| Same shape, different intent, different design consequence         |
+--------------------------------------------------------------------+
```

즉 두 패턴의 경계는 코드 문법이 아니라 책임 배치에 있다. [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 원본 기능을 유지한 채 부가 기능을 쌓는 쪽에 초점이 있고, [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 원본에 도달하기 전 단계에서 접근 조건을 조절하는 쪽에 초점이 있다.

- **📢 섹션 요약 비유**: 같은 포장지라도 선물을 꾸미기 위한 리본이면 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)이고, 택배를 열기 전에 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 봉인 스티커면 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)다. 겉모양보다 목적이 다르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)의 핵심은 동일 인터페이스를 유지한 채 기능을 계층적으로 추가하는 것이다. 각 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 [Component](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 인터페이스를 구현하면서 내부에 또 다른 Component를 들고, 호출 전후에 부가 작업을 붙인다. 이 구조는 여러 기능을 순서대로 조합할 수 있어 [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 폭발을 줄인다.

반면 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 실제 객체에 대한 대리자다. 요청을 바로 전달하지 않고, 권한 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)·원격 연결·캐시 조회·[지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 같은 제어 로직을 먼저 수행한다. 클라이언트는 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 특별한 객체로 의식하지 않고, 실제 객체처럼 사용한다는 점이 중요하다.

```text
+-------------------------------+    +-------------------------------+
| Decorator call path           |    | Proxy call path               |
+-------------------------------+    +-------------------------------+
| Client                        |    | Client                        |
|   |                           |    |   |                           |
|   v                           |    |   v                           |
| LoggingDecorator              |    | AccessProxy                   |
|   |                           |    |   | check auth / cache / lazy  |
|   v                           |    |   v                           |
| CompressionDecorator          |    | RealService                   |
|   |                           |    |                               |
|   v                           |    | Transparent to client         |
| FileStream                    |    +-------------------------------+
| Explicit stacking by client   |
+-------------------------------+
```

| 항목 | [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/) ([Decorator](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)) | [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) ([Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)) |
| :--- | :--- | :--- |
| 핵심 의도 | 책임·기능 추가 | 접근 제어·대리 수행 |
| 클라이언트 인지 | 보통 직접 조합함 | 대개 투명하게 사용함 |
| 중첩 패턴 | 여러 겹 조합 빈번 | 보통 한 단계 제어가 많음 |
| 대표 사례 | Java I/O (Input/Output), 미들웨어 체인 | AOP (Aspect-Oriented Programming) [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), [지연 로딩](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/), 원격 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) |
| 설계 위험 | 순서 의존성 증가 | 실제 객체 생명주기 은닉 |

이 표에서 중요한 것은 "같은 인터페이스 유지"라는 공통점보다, 시스템 책임이 어디에 놓이는가이다. [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 기능의 수평 확장에 강하고, [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 보안·[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 환경 제어처럼 원본 접근 조건을 관리하는 데 강하다.

- **📢 섹션 요약 비유**: [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 옷 위에 코트와 머플러를 겹쳐 입는 것이고, [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 건물 입구의 출입 게이트다. 하나는 꾸미고 보강하고, 다른 하나는 들어갈 수 있는지 먼저 판단한다.

---

## Ⅲ. 비교 및 연결

패턴 경계를 더 분명히 하려면 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)와 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 유사 패턴과 함께 봐야 한다. [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) ([Adapter](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/))는 인터페이스를 바꾸고, [퍼사드](/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/) ([Facade](/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/))는 복잡한 하위 시스템을 단순화하며, [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)와 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 인터페이스를 유지한 채 객체 주변에서 역할을 수행한다. 즉 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)와 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 "같은 계약을 유지하면서 무엇을 바꾸는가"의 문제다.

| 패턴 | 인터페이스 변화 | 주목적 | 실무 연결 |
| :--- | :--- | :--- | :--- |
| [Decorator](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/) | 동일 유지 | 기능 추가 | 로깅, [압축](/studynote/02_operating_system/06_memory_management/347_compaction/), 포맷 변환, 미들웨어 |
| [Proxy](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) | 동일 유지 | [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) | [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 캐시, [지연 로딩](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/), 원격 호출 |
| [Adapter](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/) | 변환 | [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 확보 | 레거시 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 연동 |
| [Facade](/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/) | 새 인터페이스 제공 | 복잡도 감춤 | 서브시스템 진입점 단순화 |

또한 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 AOP (Aspect-Oriented Programming)와 자연스럽게 이어진다. [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/), 보안, 로깅 같은 횡단 관심사 (Cross-Cutting Concern)를 원본 코드 밖에서 끼워 넣기 때문이다. 반대로 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 함수형 파이프라인이나 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 미들웨어처럼 "기능을 층층이 조합"하는 구조와 친하다. 구조는 닮았지만 시스템 전체에서 맡는 역할의 결이 다르다.

- **📢 섹션 요약 비유**: [어댑터](/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)는 플러그 모양을 바꾸는 변환기이고, [퍼사드](/studynote/04_software_engineering/04_testing_quality/263_facade_pattern_simplified_interface/)는 복잡한 기계를 대신 조작해 주는 리모컨이다. [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)와 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 둘 다 원래 기계를 그대로 두지만, 하나는 기능을 덧붙이고 다른 하나는 접근을 관리한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)와 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 구분하는 가장 좋은 질문은 "클라이언트가 래핑 사실을 알아야 하는가"이다. 예를 들어 `BufferedInputStream(new FileInputStream(...))`은 개발자가 직접 [버퍼링](/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/) 기능을 선택하므로 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)다. 반면 Spring의 `@Transactional`은 호출자가 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 의식하지 않아도 [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 경계가 자동 적용되므로 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)다.

### 대표 적용 시나리오

1. <strong><a href="/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/">데코레이터</a></strong>: [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) ([Hypertext Transfer Protocol](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)) 응답에 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)·암호화·로깅을 순서대로 붙이는 미들웨어 체인
2. <strong><a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">프록시</a></strong>: 권한 체크 후에만 실제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 메서드를 호출하는 보안 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)
3. <strong><a href="/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">프록시</a></strong>: 대용량 엔티티를 첫 접근 시점에만 불러오는 [지연 로딩](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/) ([Lazy Loading](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/))
4. <strong><a href="/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/">데코레이터</a></strong>: 결제 모듈에 추적 ID 부여, 포맷 변환, 재시도 기능을 계층적으로 부착

### 기술사 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- 기능을 조합 가능한 레이어로 쌓아야 하는가?
- 원본 객체 접근 전 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [캐싱](/studynote/02_operating_system/08_storage_and_io_systems/456_caching/), 원격 연결, [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 필요한가?
- 클라이언트가 어떤 부가 기능이 적용됐는지 알아야 하는가?
- 래퍼 순서가 결과를 바꾸는가, 아니면 단일 관문 역할만 하면 되는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 단순 [접근 통제](/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/)를 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)로 구현해 클라이언트가 불필요하게 래퍼를 알아야 하는 경우
- 기능 추가 요구를 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)로 억지 구현해 책임 이름은 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)인데 실제로는 장식 객체가 되어 버리는 경우
- 여러 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/) 순서를 명확히 정의하지 않아 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) 후 암호화와 암호화 후 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)이 뒤섞이는 경우

- **📢 섹션 요약 비유**: 손님이 직접 토핑을 골라 피자를 쌓으면 [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)이고, 입구에서 예약자만 들여보내는 안내 데스크면 [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)다. 선택권이 손님 쪽에 있느냐, 통제권이 입구 쪽에 있느냐가 핵심이다.

---

## Ⅴ. 기대효과 및 결론

[데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)를 올바르게 쓰면 [상속](/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 없이 기능 조합이 가능해지고, [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 올바르게 쓰면 핵심 비즈니스 로직을 건드리지 않고 보안·[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 제어를 삽입할 수 있다. 두 패턴 모두 [OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) ([Open-Closed Principle](/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/), [개방-폐쇄 원칙](/studynote/11_design_supervision/06_exam_summary/356_process/))를 실천하는 데 유용하지만, 그 가치는 서로 다른 종류의 변경을 흡수한다는 데 있다. [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 기능 변화를, [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 접근 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 변화를 흡수한다.

한계도 분명하다. [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 계층이 많아질수록 호출 흐름이 복잡해지고, [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 실제 호출 주체가 숨겨져 디버깅이 어려워질 수 있다. 따라서 이 둘을 기억할 때는 "같은 모양"이 아니라 "같은 인터페이스를 유지한 채 무엇을 바꾸려는가"라는 질문으로 정리하는 것이 가장 정확하다.

- **📢 섹션 요약 비유**: [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 기존 가방에 주머니를 더 다는 방식이고, [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 가방 보관소의 출입 관리인이다. 둘 다 가방 자체는 바꾸지 않지만, 하나는 기능을 늘리고 다른 하나는 접근을 통제한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [구조 패턴](/studynote/04_software_engineering/04_testing_quality/258_structural_patterns_overview/) (Structural Pattern) | 두 패턴이 속한 GoF 패턴 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| [OCP](/studynote/01_computer_architecture/15_advanced_topics/746_ocp/) ([Open-Closed Principle](/studynote/04_software_engineering/04_testing_quality/244_ocp_open_closed_principle/)) | 기존 객체 수정 없이 기능 추가 또는 제어 삽입 |
| AOP (Aspect-Oriented Programming) | [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)를 활용한 횡단 관심사 분리 |
| Middleware | [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)식 기능 체인의 대표 구현 |
| [Lazy Loading](/studynote/11_design_supervision/10_patterns_antipatterns/182_lazy_loading/) | [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)가 실체 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)하는 대표 사례 |

### 📈 관련 키워드 및 발전 흐름도

```text
객체 래핑 (Object Wrapping)
        |
        v
동일 인터페이스 유지
        |
        +---------------> Decorator: responsibility extension
        |
        +---------------> Proxy: access mediation
                               |
                               v
AOP · Lazy Loading · Remote Proxy · Middleware
```

이 흐름은 래핑 구조가 "기능 추가"와 "접근 제어"라는 두 갈래로 분기되고, 이후 프레임워크 수준 구현으로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [데코레이터](/studynote/04_software_engineering/04_testing_quality/262_decorator_pattern_dynamic_wrapper/)는 기본 장난감 자동차에 스티커, 불빛, 날개를 하나씩 붙이는 거예요.
2. [프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 장난감 보관함 앞에서 "이건 지금 꺼내도 되는지" [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해 주는 문지기예요.
3. 둘 다 자동차를 직접 바꾸지는 않지만, 하나는 더 멋지게 만들고 다른 하나는 사용을 관리해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 222 / 530

<- **이전**: [165. 브리지 vs 전략 패턴 (Bridge vs Strategy Pattern)](/studynote/11_design_supervision/03_gof_creational_structural/165_bridge_vs_strategy/)
**다음**: [167. 추상 팩토리 팩토리 클래스 도출 (Abstract Factory Derivation)](/studynote/11_design_supervision/03_gof_creational_structural/167_abstract_factory_factory_derivation/) ->

---
