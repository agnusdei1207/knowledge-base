+++
weight = 434
title = "434. 컴포저블 아키텍처 PBS API 조합 유연 모듈 (Composable Architecture with PBS API)"
date = "2026-05-10"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
1. **본질**: 컴포저블 아키텍처는 패키지드 비즈니스 [[090_service_kubernetes_network_load_balancing|서비스]](Packaged Business [[090_service_kubernetes_network_load_balancing|Service]], PBS)를 작고 의미 있는 업무 단위로 구성하고, 애플리케이션 프로그래밍 인터페이스([[014_api_posix|Application Programming Interface]], [[014_api_posix|API]])로 조합하는 비즈니스 중심 설계 방식이다.
2. **가치**: 업무 변화가 생겨도 전체 시스템을 재개발하지 않고 필요한 [[090_service_kubernetes_network_load_balancing|서비스]] 조합만 바꿔 민첩성, 벤더 유연성, 기능 확장 속도를 높일 수 있다.
3. **판단 포인트**: PBS 경계가 업무 역량 단위로 잘 나뉘었는지, [[014_api_posix|API]] 거버넌스와 [[001_dikw_pyramid|데이터]] 소유권이 명확한지, 조합 복잡성을 운영할 능력이 있는지가 핵심 판단 기준이다.

## Ⅰ. 개요 및 필요성
컴포저블 아키텍처는 거대한 통합 패키지 하나로 모든 기능을 해결하려는 발상에서 벗어나, 업무 의미가 분명한 [[090_service_kubernetes_network_load_balancing|서비스]] 블록을 조립해 전체 시스템을 만드는 방식이다. 실무에서는 패키지드 비즈니스 역량(Packaged Business Capability, PBC)이라는 용어와 유사하게 쓰이기도 하지만, 여기서는 키워드에 맞추어 PBS 중심 조합 구조로 이해하면 된다. 감리 관점에서는 기술 [[192_module_independence|모듈]]보다 “업무 단위가 올바르게 분해되었는가”를 먼저 본다.

이 구조가 필요한 이유는 시장 변화 속도 때문이다. 상품 조합, 채널 확장, 외부 제휴, 규제 변경이 잦은 환경에서는 모놀리식 패키지의 일괄 개편으로는 대응 속도가 나오지 않는다. 컴포저블 아키텍처는 주문, 결제, 추천, 배송, 정산 같은 업무 블록을 조합해 신속하게 새로운 프로세스를 구성하도록 돕는다.

```text
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Web/App  │   │ Partner  │   │ Channel  │
└────┬─────┘   └────┬─────┘   └────┬─────┘
     └──────────┬───┴──────────────┘
                ▼
         ┌──────────────┐
         │ API 조합 계층 │
         └───┬────┬─────┘
             │    │
        ┌────▼┐ ┌─▼────┐ ┌────▼─┐
        │ PBS1│ │ PBS2 │ │ PBS3 │
        └─────┘ └──────┘ └──────┘
```

따라서 필요성의 핵심은 “변화 대응력”과 “업무 중심 분해”다. 기술사 답안에서는 [[014_api_posix|API]] 우선 설계, 조합형 업무 프로세스, 벤더 [[008_dependencies|종속성]] 완화를 함께 써야 논리적 완성도가 높다.
- **📢 섹션 요약 비유**: 도시락을 한 종류만 파는 가게가 아니라, 밥·반찬·국을 따로 고르게 해서 손님마다 다른 도시락을 바로 조합해 주는 식당과 같다.

## Ⅱ. 아키텍처 및 핵심 원리
컴포저블 아키텍처의 핵심 원리는 업무 의미가 있는 PBS를 독립 단위로 설계하고, [[014_api_posix|API]] 우선([[014_api_posix|API]]-First) 계약으로 연결하며, 조합 계층이 채널별 경험을 빠르게 엮도록 만드는 것이다. 이때 조합은 단순 호출 집합이 아니라 [[288_version_ihl_tos_total_length|버전]], 권한, [[001_dikw_pyramid|데이터]] 소유권, [[090_service_kubernetes_network_load_balancing|서비스]] 수준 계약([[085_sla|Service Level Agreement]], [[085_sla|SLA]])까지 포함하는 운영 구조여야 한다.

| 구성 요소 | 핵심 원리 | 감리 포인트 |
| --- | --- | --- |
| PBS [[192_module_independence|모듈]] | 주문·결제·배송처럼 [[193_cohesion_levels|응집도]] 높은 업무 단위를 독립 [[090_service_kubernetes_network_load_balancing|서비스]]로 캡슐화한다. | 업무 경계의 적정성, 중복 기능, 재사용성 검토 |
| [[014_api_posix|API]] 계약 | 채널과 타 시스템이 PBS를 안정적으로 호출하도록 표준 인터페이스를 제공한다. | [[288_version_ihl_tos_total_length|버전]] [[164_policy|정책]], [[303_authentication_authorization_patterns|인증]]·[[509_authorization_models_rbac_abac|인가]], 오류 규약, 문서화 [[396_validation|확인]] |
| 조합·[[073_container_orchestration_tools|오케스트레이션]] 계층 | 여러 PBS를 묶어 사용자 여정과 업무 프로세스를 빠르게 구성한다. | 조합 복잡도, 장애 전파, [[191_transaction_concept_states|트랜잭션]] 보상 설계 검토 |
| [[001_dikw_pyramid|데이터]] 소유 구조 | 각 PBS가 자신의 [[001_dikw_pyramid|데이터]]를 책임지고 필요한 정보만 공유한다. | [[539_mdm_master_data_management|마스터 데이터]] [[194_consistency_database_integrity|일관성]], 중복 저장, 정합성 통제 [[396_validation|확인]] |

```text
┌──────────────── API Composition Layer ────────────────┐
│ 인증 │ 라우팅 │ 오케스트레이션 │ 모니터링 │ 정책 적용 │
└──────┬───────────┬──────────────┬───────────┬────────┘
       │           │              │           │
┌──────▼───┐ ┌─────▼────┐ ┌──────▼───┐ ┌─────▼────┐
│ Order PBS│ │ Pay PBS  │ │ Ship PBS │ │ CRM PBS  │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

설계 핵심은 “잘게 나누는 것”이 아니라 “비즈니스적으로 다시 조립 가능한 단위로 나누는 것”이다. 기술사 답안에서는 [[090_service_kubernetes_network_load_balancing|서비스]] 수가 많다는 사실보다 [[014_api_posix|API]] 표준화, 조합 계층, [[001_dikw_pyramid|데이터]] 경계의 균형을 강조해야 한다.
- **📢 섹션 요약 비유**: 레고 블록이 많다고 좋은 게 아니라, 바퀴·창문·문처럼 의미 있는 부품으로 나뉘어 있어야 자동차든 집이든 다시 조립하기 쉽다.

## Ⅲ. 비교 및 연결
컴포저블 아키텍처는 모놀리식 패키지와 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]] 사이를 비교해 설명하면 이해가 쉽다. 특히 “업무 조합 가능성”을 기준으로 보면 차이가 분명하다.

| 비교 항목 | 컴포저블 아키텍처 | 모놀리식 패키지 | [[213_msa_microservices_architecture|마이크로서비스 아키텍처]] |
| --- | --- | --- | --- |
| 분해 기준 | 업무 역량 단위 PBS | 기능이 한 제품에 결합 | 기술·[[064_relation_domain|도메인]] [[090_service_kubernetes_network_load_balancing|서비스]] 단위 |
| 조합 방식 | API로 [[090_service_kubernetes_network_load_balancing|서비스]] 블록 재조합 | 패키지 설정과 커스터마이징 중심 | [[090_service_kubernetes_network_load_balancing|서비스]] 간 호출과 배포 독립성 |
| 강점 | 비즈니스 민첩성, 채널 확장, 벤더 유연성 | 단순한 도입과 통합 운영 | 독립 배포와 기술 자율성 |
| 주의점 | [[014_api_posix|API]] 거버넌스와 [[001_dikw_pyramid|데이터]] 정합성 관리 필요 | 변화 대응 속도 낮음 | [[090_service_kubernetes_network_load_balancing|서비스]] 난립과 운영 복잡성 가능 |

연결 개념으로는 [[310_architecture|도메인 주도 설계]]([[127_ddd_domain_driven_design|Domain-Driven Design]], [[310_architecture|DDD]]), [[597_headless_cms_architecture|헤드리스]]([[597_headless_cms_architecture|Headless]]) 채널 분리, 저코드·노코드(Low-Code/No-Code, [[238_lowcode_nocode_citizen_developer|LCNC]]) 조합 플랫폼이 있다. 즉 컴포저블 아키텍처는 단순 기술 구조가 아니라 비즈니스 변화에 대응하는 운영 모델이기도 하다.
- **📢 섹션 요약 비유**: 통짜 가구는 한 번 사면 모양을 바꾸기 어렵고, [[532_microservices_decomposition_patterns|마이크로서비스]]는 공방 여러 곳에서 부품을 만드는 방식이며, 컴포저블은 손님이 원하는 모양대로 가구를 조립해 주는 맞춤 가구점에 가깝다.

## Ⅳ. 실무 적용 및 기술사 판단
실무에서 컴포저블 아키텍처는 변화가 잦은 기업에 특히 유리하다. 다만 업무 경계가 애매하거나 [[014_api_posix|API]] 관리 역량이 부족하면 [[090_service_kubernetes_network_load_balancing|서비스]]는 잘게 쪼개졌는데 실제 조합은 더 어려워지는 역효과가 난다. 따라서 설계 원칙과 운영 거버넌스를 함께 봐야 한다.

### 판단 [[435_checklist_based_testing|체크리스트]]
- PBS가 기술 [[192_module_independence|모듈]]이 아니라 실제 업무 역량 단위로 정의되었는가?
- [[014_api_posix|API]] [[288_version_ihl_tos_total_length|버전]], [[303_authentication_authorization_patterns|인증]], 권한, 호출 한도에 대한 거버넌스가 있는가?
- 조합 계층에서 장애 전파와 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 보상 [[164_policy|정책]]이 설계되었는가?
- 각 PBS의 [[001_dikw_pyramid|데이터]] 소유권과 [[051_mdm_master_data_management|마스터 데이터 관리]] 기준이 명확한가?
- 외부 벤더 [[090_service_kubernetes_network_load_balancing|서비스]]까지 포함한 [[090_service_kubernetes_network_load_balancing|서비스]] 수준과 책임 경계가 계약으로 관리되는가?

기술사 답안에서는 “민첩성 향상”만 쓰지 말고 “API와 [[052_data_governance_framework|데이터 거버넌스]] 없이는 복잡성 폭증”까지 함께 기술해야 균형 잡힌 판단이 된다. 또한 조직이 업무를 조합 단위로 생각하는 역량을 갖추지 못했다면 구조만 도입해도 효과가 제한적이라고 적으면 좋다.
- **📢 섹션 요약 비유**: 반찬 가게 재료가 많아도 냉장고 정리와 메뉴판이 없으면 오히려 주문이 꼬이듯, 조합형 구조일수록 규칙이 더 중요하다.

## Ⅴ. 기대효과 및 결론
기대효과는 업무 민첩성, 채널 확장 속도, 벤더 유연성, 기능 재사용성 향상이다. 새 상품이나 [[090_service_kubernetes_network_load_balancing|서비스]]가 등장했을 때 기존 PBS를 다시 엮어 빠르게 시범 [[090_service_kubernetes_network_load_balancing|서비스]]를 내놓을 수 있고, 특정 영역만 교체해도 전체를 재구축하지 않아도 된다.

결론적으로 컴포저블 아키텍처는 시스템을 기술 기능의 집합이 아니라 재조합 가능한 비즈니스 블록의 집합으로 바라보게 만든다. 시험에서는 PBS 단위, [[014_api_posix|API]] 우선, 조합 계층, [[052_data_governance_framework|데이터 거버넌스]], 조건부 채택 판단을 함께 쓰면 실무형 답안이 완성된다.
- **📢 섹션 요약 비유**: 같은 재료 상자에서 오늘은 김밥을, 내일은 비빔밥을 만드는 것처럼 블록을 다시 조합해 다른 [[090_service_kubernetes_network_load_balancing|서비스]]를 빠르게 만들 수 있다.

### 📌 관련 개념 맵
- **[[014_api_posix|API]]-First**: 구현보다 인터페이스 계약을 먼저 설계해 조합 가능성을 높이는 원칙
- **[[597_headless_cms_architecture|헤드리스]] 아키텍처([[597_headless_cms_architecture|Headless]] [[319_architecture|Architecture]])**: 화면 채널과 업무 로직을 분리해 다양한 접점을 빠르게 붙이는 구조
- **[[310_architecture|DDD]]**: 업무 경계를 명확히 나눠 PBS 단위를 정의하는 데 유용한 분석 방법
- **[[238_lowcode_nocode_citizen_developer|LCNC]]**: 현업이 조합 계층을 더 빠르게 구성하도록 돕는 실무 도구군

### 📈 관련 키워드 및 발전 흐름도
```text
모놀리식 패키지 중심 업무 시스템
    ↓
서비스 분리와 API 공개
    ↓
업무 역량 단위 PBS 설계
    ↓
조합 계층 기반 채널 확장
    ↓
컴포저블 엔터프라이즈 운영
```

### 👶 어린이를 위한 3줄 비유 설명
1. 큰 로봇 하나를 통째로 사는 대신, 팔·다리·눈을 따로 사서 붙이는 거예요.
2. 그래서 새 기능이 필요하면 필요한 부품만 바꾸면 돼요.
3. 하지만 부품을 잇는 약속이 없으면 서로 안 맞아서 움직이지 못해요.
