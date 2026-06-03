---
title: 116. 헥사고날 아키텍처 (Hexagonal Architecture / Ports and Adapters)
date: '2026-05-10'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[216_hexagonal_architecture_ports_and_adapters|헥사고날 아키텍처]] ([[366_process|Hexagonal Architecture]])는 알리스테어 콕번(Alistair Cockburn)이 제안한 설계 방식으로, 비즈니스 로직([[064_relation_domain|도메인]])을 중심에 두고 외부 시스템(DB, UI, [[014_api_posix|API]])을 [[446_port_and_bus|포트]]([[446_port_and_bus|Port]])와 [[259_adapter_pattern_interface_wrapper|어댑터]]([[259_adapter_pattern_interface_wrapper|Adapter]])를 통해 연결하여 [[064_relation_domain|도메인]]을 외부 기술 변화로부터 완전히 격리한다.
> 2. **가치**: [[064_relation_domain|도메인]] 코드가 [[002_database_definition|데이터베이스]]·프레임워크·외부 API에 의존하지 않으므로, 실제 인프라 없이 순수 [[064_relation_domain|도메인]] 로직만 [[397_unit_test|단위 테스트]]할 수 있으며 인프라 교체 시 [[259_adapter_pattern_interface_wrapper|어댑터]]만 교체하면 된다.
> 3. **판단 포인트**: [[446_port_and_bus|포트]] 앤 [[383_adapter_pattern_summary|어댑터 패턴]]의 핵심은 "의존성 방향"이다. 인프라(DB, 외부 [[014_api_posix|API]])가 [[064_relation_domain|도메인]]에 의존하는 방향이어야 하며, [[064_relation_domain|도메인]]이 인프라 기술의 클래스나 프레임워크 어노테이션을 import하는 순간 원칙이 깨진다.

---

## Ⅰ. 개요 및 필요성

[[216_hexagonal_architecture_ports_and_adapters|헥사고날 아키텍처]]는 2005년 알리스테어 콕번이 "[[446_port_and_bus|포트]] 앤 [[259_adapter_pattern_interface_wrapper|어댑터]] (Ports and Adapters)" 패턴으로 처음 소개했다. 육각형(hexagon)이라는 이름은 구조적 의미가 아니라 "[[064_relation_domain|도메인]] 주변에 여러 외부 연결 포인트가 있다"는 시각적 표현이다.

계층형 아키텍처의 가장 큰 문제는 비즈니스 계층이 퍼시스턴스 계층(JPA 어노테이션, SQL [[298_qkv_attention|쿼리]])에 의존하여 [[064_relation_domain|도메인]] 로직을 단독으로 테스트할 수 없다는 점이다. 헥사고날은 이 의존성을 역전시켜 [[064_relation_domain|도메인]]이 [[196_durability_permanent_storage|영속성]] 기술을 전혀 알지 못하게 한다.

```text
┌─────────────────────────────────────────────────────────────┐
│           헥사고날 아키텍처 구조 (개념도)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [UI Adapter]     [REST API Adapter]     [Test Adapter]   │
│        │                 │                     │           │
│        └─────────────────┴─────────────────────┘           │
│                          │                                  │
│                   [입력 포트 (Inbound Port)]                 │
│                          │                                  │
│              ┌───────────▼───────────┐                     │
│              │     도메인 (Domain)    │                     │
│              │  비즈니스 로직·규칙    │                     │
│              └───────────┬───────────┘                     │
│                          │                                  │
│                  [출력 포트 (Outbound Port)]                 │
│                          │                                  │
│        ┌─────────────────┴─────────────────────┐           │
│        │                 │                     │           │
│  [DB Adapter]   [Kafka Adapter]    [Email Adapter]         │
└─────────────────────────────────────────────────────────────┘
```

[[064_relation_domain|도메인]]은 [[446_port_and_bus|포트]](인터페이스)만 정의하고, 실제 인프라(DB, 메시지 큐, 이메일 서버)는 [[259_adapter_pattern_interface_wrapper|어댑터]]로 구현된다. [[064_relation_domain|도메인]] 코드에는 Spring, JPA, MySQL 같은 인프라 기술의 의존성이 전혀 없다.

- **📢 섹션 요약 비유**: 스마트폰은 USB-C [[446_port_and_bus|포트]](표준 인터페이스)만 갖추고 있으면 충전기든, 이어폰이든, 모니터든 [[259_adapter_pattern_interface_wrapper|어댑터]]만 맞으면 연결할 수 있다. 스마트폰([[064_relation_domain|도메인]]) 내부는 어떤 [[259_adapter_pattern_interface_wrapper|어댑터]]가 꽂히든 상관없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[446_port_and_bus|포트]]([[446_port_and_bus|Port]])는 [[064_relation_domain|도메인]]이 외부와 상호작용하는 인터페이스 규약이다. 입력 [[446_port_and_bus|포트]](Inbound [[446_port_and_bus|Port]])는 [[064_relation_domain|도메인]]이 제공하는 유스케이스 인터페이스(예: `OrderUseCase`)이고, 출력 [[446_port_and_bus|포트]](Outbound [[446_port_and_bus|Port]])는 [[064_relation_domain|도메인]]이 요구하는 인프라 인터페이스(예: `OrderRepository`)다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| [[064_relation_domain|도메인]] ([[064_relation_domain|Domain]]) | 핵심 비즈니스 로직·규칙 | OrderService, Order 엔티티 |
| 입력 [[446_port_and_bus|포트]] | 유스케이스 인터페이스 ([[064_relation_domain|도메인]] 제공) | OrderUseCase interface |
| 출력 [[446_port_and_bus|포트]] | 인프라 요구 인터페이스 ([[064_relation_domain|도메인]] 정의) | OrderRepository interface |
| 입력 [[259_adapter_pattern_interface_wrapper|어댑터]] | 외부 입력을 [[446_port_and_bus|포트]] 호출로 변환 | [[156_rest_representational_state_transfer|REST]] Controller, CLI |
| 출력 [[259_adapter_pattern_interface_wrapper|어댑터]] | [[446_port_and_bus|포트]] 구현을 실제 인프라로 연결 | JpaOrderRepository |

```text
┌─────────────────────────────────────────────────────────────┐
│      의존성 방향: 항상 외부 → 도메인 방향                    │
├─────────────────────────────────────────────────────────────┤
│  입력 어댑터(Controller) ──▶ 입력포트(interface) ◀── 도메인  │
│                                                             │
│  도메인 ──▶ 출력포트(interface) ◀── 출력어댑터(JpaRepo)      │
│                                                             │
│  핵심: 도메인은 어댑터를 모른다. 어댑터가 도메인에 의존한다. │
└─────────────────────────────────────────────────────────────┘
```

DIP가 헥사고날의 핵심 원칙이다. [[064_relation_domain|도메인]]이 소유한 출력 [[446_port_and_bus|포트]](인터페이스)를 인프라 [[259_adapter_pattern_interface_wrapper|어댑터]]가 구현하므로 의존성이 역전된다. 이 구조 덕분에 테스트에서 실제 DB 대신 인메모리 [[462_mock_test_double|Mock]] [[259_adapter_pattern_interface_wrapper|어댑터]]를 출력 [[446_port_and_bus|포트]]에 꽂아 순수 [[064_relation_domain|도메인]] 로직을 [[395_verification_process_review|검증]]할 수 있다.

- **📢 섹션 요약 비유**: 표준 규격의 콘센트([[446_port_and_bus|포트]])만 있으면 한국용·미국용·유럽용 [[259_adapter_pattern_interface_wrapper|어댑터]]로 어떤 나라에서도 사용할 수 있다. 콘센트([[064_relation_domain|도메인]]) 자체를 바꿀 필요가 없다.

---
## Ⅲ. 비교 및 연결

헥사고날, [[217_clean_architecture_dependency_rule|클린 아키텍처]]([[217_clean_architecture_dependency_rule|Clean Architecture]]), [[218_onion_architecture_domain_centric_design|어니언 아키텍처]]([[218_onion_architecture_domain_centric_design|Onion Architecture]])는 모두 "[[064_relation_domain|도메인]] 중심, 의존성 안쪽 방향"이라는 동일한 원칙을 다른 표현으로 제시한 것이다.

| 비교 축 | A | B |
|:---|:---|:---|
| **중심 개념** | 기술 계층 분리 | [[064_relation_domain|도메인]] 격리 |
| **의존성 방향** | 위에서 아래 ([[064_relation_domain|도메인]] → 인프라) | 항상 [[064_relation_domain|도메인]] 방향 (인프라 → [[064_relation_domain|도메인]]) |
| **DB 교체 영향** | 비즈니스 계층 수정 필요 | 출력 [[259_adapter_pattern_interface_wrapper|어댑터]]만 교체 |
| **[[397_unit_test|단위 테스트]]** | 인프라 [[462_mock_test_double|Mock]] 필요 | 순수 [[064_relation_domain|도메인]]만 테스트 가능 |

계층형이 [[064_relation_domain|도메인]]이 인프라를 향해 의존하는 반면, 헥사고날은 이 방향을 완전히 뒤집어 인프라가 [[064_relation_domain|도메인]] 쪽을 향해 의존한다. 이 차이가 테스트 용이성과 기술 독립성에서 극명한 결과를 낳는다.

- **📢 섹션 요약 비유**: 계층형은 왕([[064_relation_domain|도메인]])이 신하(인프라)의 집으로 직접 찾아가는 구조, 헥사고날은 신하(인프라)가 왕궁([[064_relation_domain|도메인]])으로 찾아오는 구조다. 왕은 궁전을 벗어날 필요가 없다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[[216_hexagonal_architecture_ports_and_adapters|헥사고날 아키텍처]] 도입 시 가장 흔한 실수는 [[259_adapter_pattern_interface_wrapper|어댑터]] 코드가 [[064_relation_domain|도메인]] 내부에 의존 역전 없이 직접 침투하는 것이다. `@Entity`, `@Table` 같은 JPA 어노테이션이 [[064_relation_domain|도메인]] 엔티티 클래스에 붙거나, [[064_relation_domain|도메인]] [[090_service_kubernetes_network_load_balancing|서비스]]가 Spring의 `@Autowired`를 사용하면 헥사고날의 원칙이 깨진다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. [[064_relation_domain|도메인]] 클래스에 인프라 프레임워크(Spring, JPA, [[179_kafka_flink_watermark_time_window|Kafka]])의 어노테이션이나 클래스가 없는가?
2. 출력 [[446_port_and_bus|포트]]가 [[064_relation_domain|도메인]] 패키지에 정의된 인터페이스인가?
3. 테스트에서 실제 DB 없이 [[064_relation_domain|도메인]] 로직만 [[395_verification_process_review|검증]]할 수 있는가?
4. 새로운 UI 채널([[156_rest_representational_state_transfer|REST]] → [[246_graphql_query_language_overfetching_solution|GraphQL]]) 추가 시 [[064_relation_domain|도메인]] 코드 수정이 없는가?
5. [[002_database_definition|데이터베이스]] 교체 시 수정되는 코드가 출력 [[259_adapter_pattern_interface_wrapper|어댑터]] 하나뿐인가?

- **📢 섹션 요약 비유**: 좋은 식당은 홀 직원(입력 [[259_adapter_pattern_interface_wrapper|어댑터]])과 배달 플랫폼(다른 입력 [[259_adapter_pattern_interface_wrapper|어댑터]])이 바뀌어도 주방([[064_relation_domain|도메인]])의 레시피는 변하지 않는다. 주방장은 주문 방식을 신경 쓰지 않는다.

---

## Ⅴ. 기대효과 및 결론

[[216_hexagonal_architecture_ports_and_adapters|헥사고날 아키텍처]]를 올바르게 적용하면 [[064_relation_domain|도메인]] 로직의 [[397_unit_test|단위 테스트]] 속도가 획기적으로 빨라진다. 실제 DB 연결 없이 인메모리 [[259_adapter_pattern_interface_wrapper|어댑터]]로 수천 건의 테스트를 초 단위로 실행할 수 있다. 인프라 기술 교체(관계형 DB → 문서 DB)도 [[259_adapter_pattern_interface_wrapper|어댑터]] 교체로 국한되어 핵심 비즈니스 코드는 보호된다.

한계는 [[459_quic_fec_forward_error_correction|초기]] 설계 복잡도와 [[446_port_and_bus|포트]]·[[259_adapter_pattern_interface_wrapper|어댑터]] 코드의 증가다. 작은 CRUD 중심 시스템에서는 오히려 오버엔지니어링이 될 수 있다. 비즈니스 규칙이 복잡하거나 인프라 기술을 자주 교체해야 하는 환경에서 그 가치가 극대화된다.

미래 방향으로는 ① DDD와의 결합으로 [[064_relation_domain|도메인]] 이벤트 기반 [[446_port_and_bus|포트]] 설계, ② 헥사고날 패키지 구조를 강제하는 아키텍처 [[395_verification_process_review|검증]] 도구(ArchUnit), ③ 마이크로서비스에서 각 [[090_service_kubernetes_network_load_balancing|서비스]]가 내부적으로 헥사고날 구조를 채택하는 패턴이 확산되고 있다.

[[216_hexagonal_architecture_ports_and_adapters|헥사고날 아키텍처]]는 "[[064_relation_domain|도메인]]이 중심에서 세상을 지배하고, 기술은 언제든 교체 가능한 플러그인"이라는 관점으로 기억해야 한다.

- **📢 섹션 요약 비유**: 심장([[064_relation_domain|도메인]])은 혈액을 펌프질하는 핵심 기능만 한다. 혈관([[259_adapter_pattern_interface_wrapper|어댑터]])이 어디로 연결되든, 신체 어느 부분(인프라)에 붙어 있든 심장의 역할은 바뀌지 않는다.

---

### 📌 관련 개념 맵

[[[247_dip_dependency_inversion_principle|DIP]] 원칙] → [포트 앤 [[259_adapter_pattern_interface_wrapper|어댑터]] 패턴] → [헥사고날 아키텍처] → [[[310_architecture|DDD]] [[064_relation_domain|도메인]] 격리] → [[[619_msa_traffic_hardware|MSA]] 내부 구조]

| 개념 | 연결 포인트 |
|:---|:---|
| [[247_dip_dependency_inversion_principle|DIP]] (의존성 역전) | 헥사고날의 핵심 원리: 인프라가 [[064_relation_domain|도메인]]에 의존 |
| [[217_clean_architecture_dependency_rule|클린 아키텍처]] | 헥사고날과 동일 원칙을 원형 계층으로 표현 |
| [[310_architecture|DDD]] | [[064_relation_domain|도메인]] 격리 목표를 공유하는 설계 방법론 |
| ArchUnit | 헥사고날 의존성 규칙을 자동 [[395_verification_process_review|검증]]하는 도구 |

### 📈 관련 키워드 및 발전 흐름도

[계층형 [[064_relation_domain|도메인]]-인프라 결합 문제] → [포트 앤 [[259_adapter_pattern_interface_wrapper|어댑터]] 패턴] → [헥사고날 아키텍처] → [클린·어니언과 수렴] → [[[310_architecture|DDD]]+헥사고날 결합] → [[[619_msa_traffic_hardware|MSA]] [[090_service_kubernetes_network_load_balancing|서비스]] 내부 헥사고날 표준화]

### 👶 어린이를 위한 3줄 비유 설명

1. 스마트폰의 USB-C 구멍([[446_port_and_bus|포트]])은 충전기, 이어폰, 외부 모니터를 다 연결할 수 있어요.
2. 스마트폰([[064_relation_domain|도메인]]) 자체는 어떤 선이 꽂혔는지 신경 쓰지 않아요.
3. [[216_hexagonal_architecture_ports_and_adapters|헥사고날 아키텍처]]는 핵심 기능([[064_relation_domain|도메인]])을 이런 표준 [[446_port_and_bus|포트]]로 보호하는 방법이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 172 / 530

← **이전**: [[115_layered_architecture|115. 계층형 아키텍처 (Layered Architecture)]]
**다음**: [[117_clean_architecture|117. 클린 아키텍처 (Clean Architecture)]] →

---
