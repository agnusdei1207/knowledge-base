+++
weight = 188
title = "188. 부패 방지 계층 (Anti-Corruption Layer, ACL) 패턴 - 레거시 의미 오염 차단"
date = "2026-05-08"
[extra]
categories = "studynote-enterprise"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 부패 방지 계층 (Anti-Corruption Layer, [[549_acl_access_control_list|ACL]])은 신규 [[064_relation_domain|도메인]] 모델과 레거시 모델 사이에 번역 계층을 두어, 오래된 시스템의 용어와 규칙이 새 [[090_service_kubernetes_network_load_balancing|서비스]] 내부로 스며드는 것을 차단하는 경계 패턴이다.
> 2. **가치**: 신규 시스템은 자기 언어와 설계를 유지한 채 레거시를 이용할 수 있으므로, 이후 레거시 교체나 제거가 훨씬 쉬워지고 [[064_relation_domain|도메인]] 복잡도도 통제된다.
> 3. **판단 포인트**: 단순 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 변환만 필요한지, 아니면 의미 체계 자체가 다를 정도로 깊은 번역이 필요한지 구분해야 하며, 후자일 때 ACL의 투자 가치가 커진다.

---

## Ⅰ. 개요 및 필요성

부패 방지 계층은 [[310_architecture|도메인 주도 설계]] ([[127_ddd_domain_driven_design|Domain-Driven Design]], [[310_architecture|DDD]])에서 서로 다른 [[221_bounded_context_ddd_msa_boundary|바운디드 컨텍스트]] ([[221_bounded_context_ddd_msa_boundary|Bounded Context]]) 사이의 의미 오염을 막기 위한 [[571_protection_vs_security|보호]] 장치다. 엔터프라이즈 현대화에서는 특히 신규 [[090_service_kubernetes_network_load_balancing|서비스]]가 레거시 [[002_database_definition|데이터베이스]], 메인프레임, [[153_soap_simple_object_access_protocol|SOAP]] 인터페이스 ([[153_soap_simple_object_access_protocol|Simple Object Access Protocol]]), 오래된 코드 체계와 연결될 때 이 패턴이 필요해진다. 문제는 통신 그 자체보다, 레거시의 이상한 필드명, 상태 코드, 업무 규칙을 신규 [[090_service_kubernetes_network_load_balancing|서비스]]가 그대로 받아들이기 시작하는 순간 새 [[064_relation_domain|도메인]]도 함께 낡아진다는 점이다.

예를 들어 레거시의 고객 상태가 `A`, `B`, `Z9` 같은 내부 코드로 표현되어 있는데, 신규 [[090_service_kubernetes_network_load_balancing|서비스]]가 이를 직접 퍼뜨리기 시작하면 사용자 [[064_relation_domain|도메인]], 응용 프로그램 프로그래밍 인터페이스 ([[014_api_posix|Application Programming Interface]], [[014_api_posix|API]]) 응답, 테스트 코드까지 모두 레거시 의미에 종속된다. 이렇게 되면 새 시스템은 겉보기만 현대적일 뿐, 내부 개념 구조는 레거시의 그림자를 벗어나지 못한다. ACL은 이 침투를 막아 신규 시스템이 자기 언어를 유지하게 만드는 격리막이다.

- **📢 섹션 요약 비유**: 깨끗한 연구실로 들어오는 외부 물품을 바로 들이지 않고, 입구의 멸균실에서 위험 요소를 걸러내는 과정과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

ACL은 보통 신규 [[090_service_kubernetes_network_load_balancing|서비스]]와 레거시 사이의 경계에 위치하며, 요청 변환, 응답 변환, 오류 코드 번역, 외부 의존성 흡수를 담당한다. 신규 [[090_service_kubernetes_network_load_balancing|서비스]]는 자신의 표준 [[064_relation_domain|도메인]] 모델만 알고, 레거시 호출 세부사항은 [[549_acl_access_control_list|ACL]] 내부로 밀어 넣는다. 이때 ACL은 단순 [[259_adapter_pattern_interface_wrapper|어댑터]] ([[259_adapter_pattern_interface_wrapper|Adapter]])일 수도 있지만, 의미 해석과 규칙 보정이 크면 별도 [[090_service_kubernetes_network_load_balancing|서비스]]나 독립 [[192_module_independence|모듈]]로 운영되기도 한다.

아래 그림은 ACL이 의미 체계를 어떻게 격리하는지 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Domain protection with ACL                                           │
├──────────────────────────────────────────────────────────────────────┤
│ New Service -> Canonical Model -> ACL -> Legacy API / DB            │
│                   ▲                │                                  │
│                   │                ├─ request mapping                │
│                   │                ├─ response mapping               │
│                   │                └─ error / code translation       │
│                   └──── domain purity preserved                      │
└──────────────────────────────────────────────────────────────────────┘
```

| 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 표준 [[064_relation_domain|도메인]] 모델 | 신규 [[090_service_kubernetes_network_load_balancing|서비스]] 내부 언어 유지 | 레거시 필드명을 내부 모델로 끌어들이지 않는다 |
| 요청 매퍼 | 신규 명령을 레거시 형식으로 변환 | 필드명, 단위, 상태 코드 해석 필요 |
| 응답 매퍼 | 레거시 결과를 신규 의미로 재구성 | 누락값, 코드값, 날짜 형식 차이 보정 |
| 오류 번역기 | 레거시 오류를 업무 의미로 치환 | 기술 오류와 업무 오류를 분리해야 한다 |
| [[266_contract_testing_pact_msa_api|계약 테스트]] | 변환 [[002_bigdata_5v|정확성]] [[395_verification_process_review|검증]] | 레거시 변경이 신규 [[090_service_kubernetes_network_load_balancing|서비스]]에 미치는 영향을 조기 탐지 |

핵심 원리는 "레거시를 이해하는 책임"을 신규 [[090_service_kubernetes_network_load_balancing|서비스]]가 아니라 ACL이 전담하는 것이다. 따라서 신규 [[090_service_kubernetes_network_load_balancing|서비스]]는 `Customer`, `Order`, `Active` 같은 자기 개념만 다루고, 레거시의 `CUST_TP=03`이나 `STAT_FLG=Y` 같은 표현은 [[549_acl_access_control_list|ACL]] 내부에만 머문다. 이 구조는 이후 레거시 뒤편을 다른 시스템으로 바꿀 때도 신규 [[090_service_kubernetes_network_load_balancing|서비스]]의 코드를 최소 수정으로 유지하게 해 준다.

- **📢 섹션 요약 비유**: 외국어 계약서를 회사 전체 직원이 각자 해석하지 않고, 전문 통역팀이 한 번 번역해 표준 문서로 배포하는 것과 같다.

---

## Ⅲ. 비교 및 연결

ACL은 직접 연동, 공유 [[022_kernel_role|커널]] (Shared [[022_kernel_role|Kernel]]), [[014_api_posix|API]] 게이트웨이와 비슷해 보이지만 목적이 다르다. 직접 연동은 구현이 빠르지만 신규 [[090_service_kubernetes_network_load_balancing|서비스]]가 레거시 용어에 오염되기 쉽다. 공유 [[022_kernel_role|커널]]은 공통 모델을 함께 쓰는 방식이어서, 양쪽의 의미 차이가 크지 않을 때는 유용하지만 레거시와 신규 간 사고방식이 크게 다르면 오히려 결합을 강화한다. [[014_api_posix|API]] 게이트웨이는 주로 외부 진입 트래픽을 통제하는 계층이지, 내부 [[064_relation_domain|도메인]] 번역 책임을 대신하지 않는다.

| 방식 | 목적 | 장점 | 주의점 |
| :--- | :--- | :--- | :--- |
| 직접 연동 | 빠른 연결 | [[459_quic_fec_forward_error_correction|초기]] 구현이 가장 단순 | 레거시 모델이 신규 코드에 침투 |
| [[549_acl_access_control_list|ACL]] | 의미 번역과 [[571_protection_vs_security|보호]] | [[064_relation_domain|도메인]] 순수성, 교체 용이성 확보 | 매핑 비용과 추가 홉 발생 |
| 공유 [[022_kernel_role|커널]] | 공통 모델 재사용 | 중복 모델 감소 | 개념 차이가 크면 강결합 심화 |
| [[014_api_posix|API]] 게이트웨이 | 외부 트래픽 제어 | [[303_authentication_authorization_patterns|인증]], [[339_routing_overview_best_path_selection|라우팅]], [[164_policy|정책]] 중앙화 | 내부 의미 번역을 대체하지 못함 |

[[376_strangler_fig_summary|스트랭글러 피그 패턴]]과의 연결도 중요하다. 점진적 마이그레이션 [[459_quic_fec_forward_error_correction|초기]]에 신규 [[090_service_kubernetes_network_load_balancing|서비스]]가 당분간 레거시 기능을 활용해야 한다면 ACL이 경계 오염을 막아 준다. 반대로 [[538_event_driven_architecture_eda|이벤트 기반 아키텍처]]에서는 ACL이 레거시 이벤트를 신규 이벤트 [[005_schema|스키마]]로 변환하는 역할을 맡을 수 있다. 즉 ACL은 단순 통신 기술이 아니라, **새 시스템의 언어를 지키는 아키텍처 [[690_firewall_generation_evolution|방화벽]]**이다.

- **📢 섹션 요약 비유**: 집 현관문, 인터폰, 보안문이 모두 다르듯, ACL은 "누가 들어오나"보다 "안으로 들어온 것이 우리 집 규칙에 맞는가"를 검사하는 장치다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 레거시와 신규의 개념 차이가 큰 지점부터 ACL을 배치하는 것이 효과적이다. 고객 상태, 상품 [[104_classification_analysis|분류]], 권한 모델, 금액 계산 규칙처럼 의미가 어긋나기 쉬운 영역은 직접 연동할수록 버그와 오해가 누적된다. 반면 단순 조회 배치처럼 의미 변환이 거의 없고 생명주기가 짧은 연동은 과한 ACL보다 가벼운 [[259_adapter_pattern_interface_wrapper|어댑터]]가 더 현실적일 수 있다.

### 기술사 판단 [[435_checklist_based_testing|체크리스트]]

1. 레거시 용어와 신규 [[064_relation_domain|도메인]] 용어 사이에 의미 불일치가 명확히 존재하는가?
2. 신규 [[090_service_kubernetes_network_load_balancing|서비스]]가 레거시 필드명, 코드값, 예외 체계를 직접 알지 않도록 경계를 강제했는가?
3. ACL이 변환 규칙만 담당하고, 새로운 비즈니스 [[164_policy|정책]] 엔진으로 비대해지지 않도록 통제하고 있는가?
4. [[266_contract_testing_pact_msa_api|계약 테스트]]와 모의 객체를 통해 레거시 변경에 대한 회귀 [[395_verification_process_review|검증]]이 가능한가?
5. 나중에 레거시를 교체할 때 [[549_acl_access_control_list|ACL]] 뒤편만 바꾸면 되도록 의존 방향이 정리되어 있는가?

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 신규 [[090_service_kubernetes_network_load_balancing|서비스]]가 ACL을 우회해 레거시 [[002_database_definition|데이터베이스]]를 직접 조회하는 구조
- [[549_acl_access_control_list|ACL]] 안에 신규 [[090_service_kubernetes_network_load_balancing|서비스]]의 핵심 비즈니스 로직까지 넣어 또 다른 레거시를 만드는 구조
- 레거시와 신규가 같은 [[064_relation_domain|도메인]] 클래스를 공유해 경계가 흐려지는 구조
- 오류 번역 없이 레거시 예외 [[389_mesh_topology|메시]]지를 그대로 외부 API에 노출하는 구조

기술사 관점에서는 "ACL을 뒀다"보다 "무엇을 지키기 위해 뒀는가"를 설명해야 한다. 핵심은 연결 자체가 아니라, [[064_relation_domain|도메인]] 의미의 독립성과 교체 가능성을 유지하는 설계 판단이다.

- **📢 섹션 요약 비유**: 병원 응급실의 [[104_classification_analysis|분류]]실처럼, 외부에서 들어온 정보를 바로 병동으로 보내지 않고 환자 상태에 맞게 [[104_classification_analysis|분류]]·정리해 안쪽 체계를 지키는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

ACL이 잘 설계되면 신규 [[090_service_kubernetes_network_load_balancing|서비스]]는 자신의 언어와 테스트 [[268_strategy_pattern|전략]]을 유지할 수 있고, 레거시 변경 충격도 경계에서 흡수된다. 이는 코드 [[333_readability_vs_efficiency|가독성]], 변경 용이성, 장애 분석 속도를 모두 높인다. 특히 레거시가 폐기되는 순간 ACL만 제거하거나 뒤편 구현만 교체하면 되므로, 현대화 프로그램의 후반 비용이 크게 줄어든다.

반대로 ACL은 번역 계층인 만큼 추가 [[015_지연_데이터_관점|지연]], 추가 코드, 추가 운영 대상이라는 비용을 만든다. 또한 경계를 너무 넓게 잡으면 ACL이 거대한 중계 시스템으로 비대해질 수 있다. 따라서 ACL은 "모든 연동의 기본값"이 아니라, **의미 오염이 비즈니스 위험으로 이어지는 경계에 선택적으로 배치하는 [[571_protection_vs_security|보호]]막**으로 기억해야 한다.

- **📢 섹션 요약 비유**: 좋은 공기청정기는 바람을 막기 위한 장치가 아니라, 바깥 공기를 안쪽 공간 규칙에 맞게 정제해 주는 장치와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[310_architecture|DDD]] ([[127_ddd_domain_driven_design|Domain-Driven Design]]) | [[221_bounded_context_ddd_msa_boundary|바운디드 컨텍스트]] 간 의미 차이를 명시적으로 다루는 출발점이다. |
| [[383_adapter_pattern_summary|어댑터 패턴]] ([[151_adapter_pattern|Adapter Pattern]]) | [[295_protocol_field_tcp_udp_icmp|프로토콜]]과 인터페이스 변환을 구현하는 기본 기법이다. |
| [[387_facade_pattern_summary|퍼사드 패턴]] ([[156_facade_pattern|Facade Pattern]]) | 복잡한 레거시 호출을 단순한 인터페이스로 감싸는 데 쓰인다. |
| [[376_strangler_fig_summary|스트랭글러 피그 패턴]] | 점진적 전환 과정에서 신규 [[090_service_kubernetes_network_load_balancing|서비스]]와 레거시 사이 [[571_protection_vs_security|보호]]막으로 ACL이 배치된다. |
| [[266_contract_testing_pact_msa_api|계약 테스트]] (Contract Test) | [[116_mapping_rule_erd_to_relation|매핑 규칙]]이 깨졌는지 자동으로 [[395_verification_process_review|검증]]하는 핵심 수단이다. |
| 표준 모델 (Canonical Model) | 여러 외부 시스템과 연결될 때 내부 표현을 일관되게 유지하게 해 준다. |

### 📈 관련 키워드 및 발전 흐름도

```text
레거시 직접 연동의 의미 오염
        │
        ▼
어댑터 / 퍼사드 기반 인터페이스 정리
        │
        ▼
ACL을 통한 도메인 번역 계층 도입
        │
        ▼
계약 테스트 · 표준 모델 정착
        │
        ▼
레거시 교체 시 경계만 유지하고 뒤편 교체
```

이 흐름은 "연결"에서 출발해 "의미 [[571_protection_vs_security|보호]]"를 거쳐, 최종적으로 레거시 교체 유연성까지 확보하는 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 새로 지은 집은 깨끗한 규칙대로 꾸미고 싶어요.
2. 그래서 바깥에서 들어오는 낡은 물건은 문 앞에서 정리하고 이름표도 새로 붙여요.
3. 그러면 집 안은 늘 같은 규칙을 지키고, 나중에 바깥 창고가 바뀌어도 집 안은 그대로 쓸 수 있어요.
