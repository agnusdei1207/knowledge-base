---
title: 179. 레파지토리 패턴 (Repository Pattern)
date: '2026-05-06'
tags:
- studynote-design-supervision
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 레파지토리 패턴 (Repository Pattern)은 [[064_relation_domain|도메인]] [[222_aggregate_ddd_transaction_consistency|애그리게이트]]를 메모리 컬렉션처럼 조회·저장하게 만드는 [[198_abstraction_control_data_process|추상화]]로, [[064_relation_domain|도메인]] 모델이 SQL이나 ORM (Object-Relational [[010_schema_mapping|Mapping]]) 세부사항보다 비즈니스 의미에 집중하게 한다.
> 2. **가치**: [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 경계를 지키고 테스트 대역을 쉽게 만들며, 인프라 기술 교체나 [[298_qkv_attention|쿼리]] 최적화가 상위 [[064_relation_domain|도메인]] 코드로 새어 나오는 것을 줄인다.
> 3. **판단 포인트**: 단순 CRUD (Create, Read, Update, Delete) 화면까지 무조건 레파지토리로 감싸면 과잉 [[198_abstraction_control_data_process|추상화]]가 되므로, [[310_architecture|DDD]] ([[127_ddd_domain_driven_design|Domain-Driven Design]]) 수준의 모델과 [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 경계가 실제로 필요한지 먼저 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

레파지토리 패턴은 "[[002_database_definition|데이터베이스]]를 직접 다루지 말고, [[064_relation_domain|도메인]] 객체 집합을 다루듯 설계하자"는 발상에서 출발한다. [[090_service_kubernetes_network_load_balancing|서비스]]가 `SELECT`, `JOIN`, `EntityManager`, `ResultSet` 같은 저장 기술 언어를 알기 시작하면, [[064_relation_domain|도메인]] 규칙은 점점 저장소 구조에 끌려간다. 그 결과 비즈니스 개념보다 테이블 구조가 상위 설계를 지배하게 된다.

DDD에서는 특히 이 문제가 크게 드러난다. 주문, 회원, 결제 같은 [[222_aggregate_ddd_transaction_consistency|애그리게이트]]는 [[194_consistency_database_integrity|일관성]] 경계를 가진 [[064_relation_domain|도메인]] 단위인데, 테이블 단위 접근만 반복하면 [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 내부 규칙이 쉽게 파편화된다. 예를 들어 `OrderItem`만 따로 저장·수정하는 식으로 흐르면, 주문 총액 계산이나 [[632_state_transition_diagram_testing|상태 전이]] 규칙이 여러 곳에 흩어진다.

레파지토리는 이런 문제를 막기 위해 등장했다. [[090_service_kubernetes_network_load_balancing|서비스]]는 "주문을 찾는다", "회원을 저장한다"처럼 [[064_relation_domain|도메인]] 언어로 말하고, 실제 영속화는 레파지토리 구현체가 담당한다. 즉 레파지토리의 필요성은 객체 하나 더 만드는 데 있지 않고, **[[064_relation_domain|도메인]] 언어와 저장 기술 언어 사이에 명확한 번역 경계**를 세우는 데 있다.

- **📢 섹션 요약 비유**: 레파지토리는 창고 구조를 외우게 하는 대신 "필요한 책을 도서관에서 빌린다"는 식으로 업무 언어를 단순하게 만드는 사서 역할과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

레파지토리의 핵심 원리는 두 가지다. 첫째, 인터페이스는 [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 중심 [[064_relation_domain|도메인]] 언어를 사용한다. 둘째, 구현체는 [[196_durability_permanent_storage|영속성]] 기술을 숨기되 [[222_aggregate_ddd_transaction_consistency|애그리게이트]]를 재구성해서 반환한다. 따라서 레파지토리는 보통 [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 루트([[131_aggregate_root|Aggregate Root]]) 기준으로 하나씩 설계되며, 테이블마다 1개씩 자동 생성하는 구조와는 철학이 다르다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| Application [[090_service_kubernetes_network_load_balancing|Service]] | 유스케이스 조합, [[191_transaction_concept_states|트랜잭션]] 시작점 | 레파지토리를 사용하지만 저장 기술은 몰라야 함 |
| Repository Interface | [[064_relation_domain|도메인]] 계층 계약 | `findByOrderId`, `save`처럼 [[064_relation_domain|도메인]] 의도 표현 |
| [[131_aggregate_root|Aggregate Root]] | 저장·복원의 기준 단위 | 내부 불변식과 [[194_consistency_database_integrity|일관성]] 경계 유지 |
| Repository Implementation | JPA, SQL Mapper, [[035_nosql|NoSQL]] 등 실제 영속화 | 매핑, [[298_qkv_attention|쿼리]], 예외 변환 담당 |
| Unit of Work / [[191_transaction_concept_states|Transaction]] | 변경 추적과 커밋 협력 | 저장 시점과 [[194_consistency_database_integrity|일관성]] 관리 |

아래 그림은 레파지토리가 계층 사이에서 어떤 역할을 하는지 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Repository in domain-centered architecture                           │
├──────────────────────────────────────────────────────────────────────┤
│ Application Service                                                  │
│   │  findByOrderId() / save(order)                                   │
│   ▼                                                                  │
│ OrderRepository interface                                            │
│   │  speaks domain language                                          │
│   ▼                                                                  │
│ Repository implementation                                            │
│   ├─ ORM mapping                                                     │
│   ├─ SQL / query builder                                             │
│   └─ transaction / unit-of-work cooperation                          │
│   │                                                                  │
│   ▼                                                                  │
│ Database / cache / external store                                    │
│                                                                      │
│ Returned to service: Aggregate Root + Value Objects                  │
└──────────────────────────────────────────────────────────────────────┘
```

여기서 중요한 규칙이 있다. 레파지토리는 보통 **[[222_aggregate_ddd_transaction_consistency|애그리게이트]] 루트만 외부에 노출**한다. `OrderRepository`는 있어도 `OrderItemRepository`를 따로 두지 않는 식이다. 그래야 [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 내부 규칙이 바깥에서 임의로 깨지지 않는다. 또한 조회 요구가 지나치게 복잡해져 리포트·대시보드·통계 성격이 강해지면, 모든 읽기 작업을 레파지토리에 억지로 넣기보다 Query Service나 [[306_cqrs|CQRS]] ([[271_command_pattern|Command]] Query Responsibility Segregation) 읽기 모델로 분리하는 편이 낫다.

즉 레파지토리는 "모든 [[001_dikw_pyramid|데이터]] 접근의 만능 통로"가 아니라, **[[222_aggregate_ddd_transaction_consistency|애그리게이트]]를 저장하고 다시 살려내는 [[064_relation_domain|도메인]] 경계 장치**로 이해해야 한다.

- **📢 섹션 요약 비유**: 레파지토리는 책 한 장씩 뜯어 건네는 복사실이 아니라, 책 한 권 전체를 제대로 보관하고 다시 빌려주는 도서관 서가와 같다.

---

## Ⅲ. 비교 및 연결

레파지토리를 [[054_dao_decentralized_autonomous_organization|DAO]] ([[001_dikw_pyramid|Data]] Access Object)와 같은 것으로 보면 절반만 이해한 셈이다. 둘 다 저장소 세부사항을 숨기지만, 무엇을 중심에 두는지가 다르다.

| 비교 축 | 레파지토리 패턴 | [[054_dao_decentralized_autonomous_organization|DAO]] 패턴 | [[483_active_vs_passive_ftp|Active]] Record |
| :--- | :--- | :--- | :--- |
| 중심 관점 | [[222_aggregate_ddd_transaction_consistency|애그리게이트]]와 [[064_relation_domain|도메인]] 의미 | 테이블/[[298_qkv_attention|쿼리]]/저장 기술 | 객체가 스스로 저장 |
| 대표 메서드 언어 | `findActiveOrdersByCustomerId()` | `selectByCustomerId()` | `order.save()` |
| 반환 초점 | [[064_relation_domain|도메인]] 객체 집합 | 엔티티 / DTO / 행 [[001_dikw_pyramid|데이터]] | 자기 자신 |
| 적합한 환경 | [[310_architecture|DDD]], [[216_hexagonal_architecture_ports_and_adapters|헥사고날 아키텍처]] | 레거시 DB, 저장 기술 중심 계층화 | 단순 CRUD와 빠른 개발 |
| 주의점 | 과잉 [[198_abstraction_control_data_process|추상화]] 가능 | [[064_relation_domain|도메인]] 의미 약화 가능 | [[064_relation_domain|도메인]]과 저장 결합 심화 |

DAO가 "어떻게 조회할까"에 더 가깝다면, 레파지토리는 "어떤 [[064_relation_domain|도메인]] 대상을 어떤 의미로 다룰까"에 가깝다. 그래서 복잡한 리포팅 [[298_qkv_attention|쿼리]], 대량 배치 조회, 화면 전용 DTO 투영은 DAO나 Query Service가 더 잘 맞을 수 있다. 반대로 [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 규칙을 지키며 상태를 변경해야 하는 [[289_cqrs_db|쓰기]] 모델에는 레파지토리가 더 적합하다.

Spring [[001_dikw_pyramid|Data]] JPA가 제공하는 `JpaRepository`도 이 관점에서 봐야 한다. 프레임워크가 레파지토리 구현을 쉽게 만들어 줄 수는 있지만, 메서드가 전부 테이블 조작 중심이고 [[064_relation_domain|도메인]] 의미가 사라진다면 이름만 레파지토리인 DAO에 가까워질 수 있다.

- **📢 섹션 요약 비유**: DAO가 창고의 선반 번호를 잘 아는 관리인이라면, 레파지토리는 "고객 주문서 묶음" 자체를 어떻게 다뤄야 하는지 이해하는 기록 관리자에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

레파지토리는 풍부한 [[064_relation_domain|도메인]] 모델이 있는 시스템에서 빛난다. 주문 [[632_state_transition_diagram_testing|상태 전이]], 결제 승인, 재고 예약처럼 [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 단위 규칙이 중요한 경우에는 [[090_service_kubernetes_network_load_balancing|서비스]]가 레파지토리를 통해 [[222_aggregate_ddd_transaction_consistency|애그리게이트]]를 불러오고, [[064_relation_domain|도메인]] 메서드로 상태를 바꾼 뒤, 다시 저장하는 흐름이 자연스럽다. 반면 관리 화면의 단순 목록 조회나 복잡한 통계 리포트까지 모두 레파지토리로 밀어 넣으면 인터페이스가 비대해지고 [[064_relation_domain|도메인]] 의미도 흐려진다.

| 적용 상황 | 레파지토리 적합도 | 판단 이유 |
| :--- | :--- | :--- |
| [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 규칙이 강한 주문·결제 [[064_relation_domain|도메인]] | 매우 높음 | [[194_consistency_database_integrity|일관성]] 경계를 지키며 상태를 다뤄야 함 |
| [[216_hexagonal_architecture_ports_and_adapters|헥사고날 아키텍처]] 기반 [[090_service_kubernetes_network_load_balancing|서비스]] | 높음 | 포트로서 인프라 의존성을 잘 분리할 수 있음 |
| 단순 CRUD 백오피스 | 보통 이하 | DAO나 프레임워크 기본 Repository면 충분할 수 있음 |
| 대규모 조회·통계 화면 | 낮음 | Query [[090_service_kubernetes_network_load_balancing|Service]] / 읽기 모델 분리가 더 적합 |

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 레파지토리가 [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 루트 기준으로 설계되어 있는가?
2. 인터페이스 메서드가 [[064_relation_domain|도메인]] 용어를 사용하고 있는가?
3. [[090_service_kubernetes_network_load_balancing|서비스]]가 ORM [[160_session_controlling_terminal|세션]], [[298_qkv_attention|쿼리]] [[256_builder_pattern_step_by_step_creation|빌더]], 테이블 조인 세부사항에 직접 접근하지 않는가?
4. 복잡한 조회 전용 요구는 별도 Query Service로 분리되어 있는가?
5. 테스트에서 In-Memory 구현체나 [[463_fake_test_double|Fake]] Repository로 [[064_relation_domain|도메인]] 규칙을 검증할 수 있는가?

### 자주 발생하는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 모든 엔티티를 `GenericRepository<T>` 하나로 몰아넣어 [[064_relation_domain|도메인]] 의미를 지우는 설계
- 레파지토리 안에서 비즈니스 규칙과 화면용 DTO 조립까지 모두 처리하는 구현
- [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 내부 객체를 별도 레파지토리로 직접 수정해 [[194_consistency_database_integrity|일관성]] 경계를 깨는 구조
- 이름만 레파지토리이고 실제로는 [[090_service_kubernetes_network_load_balancing|서비스]]가 `EntityManager`를 직접 사용하는 반쪽 분리

기술사 답안에서는 **"레파지토리 패턴은 [[222_aggregate_ddd_transaction_consistency|애그리게이트]]를 컬렉션처럼 다루게 해 [[064_relation_domain|도메인]] 모델을 저장 기술로부터 보호하는 패턴이며, 단순 CRUD나 대형 조회에는 [[054_dao_decentralized_autonomous_organization|DAO]]·Query Service와 역할을 분리해야 한다"**라고 정리하면 설계 판단이 분명해진다.

- **📢 섹션 요약 비유**: 레파지토리를 잘 쓰는 것은 서류를 아무 서랍에나 넣는 대신, 한 사건에 속한 서류 묶음을 한 폴더로 관리해 규칙이 흐트러지지 않게 하는 일과 같다.

---

## Ⅴ. 기대효과 및 결론

레파지토리 패턴을 제대로 적용하면 [[064_relation_domain|도메인]] 코드는 저장 방식보다 업무 규칙을 더 선명하게 드러낸다. 테스트에서는 가짜 레파지토리로 비즈니스 규칙을 빠르게 검증할 수 있고, 인프라 계층에서는 ORM 교체, [[298_qkv_attention|쿼리]] 최적화, 저장소 [[136_variance|분산]] 전략을 비교적 독립적으로 조정할 수 있다. 결국 가장 큰 효과는 **변경 비용이 저장 기술 경계 안에 머무르게 만드는 것**이다.

하지만 레파지토리가 모든 [[001_dikw_pyramid|데이터]] 접근 패턴을 대표하지는 않는다. 단순한 화면 조회나 리포팅까지 모두 레파지토리로 묶으면 인터페이스가 비대해지고 책임이 흐려진다. 그래서 레파지토리는 "무조건 한 계층 더"가 아니라, **[[064_relation_domain|도메인]] [[222_aggregate_ddd_transaction_consistency|애그리게이트]]를 보호할 필요가 있을 때 쓰는 선택적 경계**로 기억하는 것이 맞다.

결론적으로 레파지토리 패턴은 [[002_database_definition|데이터베이스]] [[198_abstraction_control_data_process|추상화]] 자체보다, [[064_relation_domain|도메인]] 언어를 보존하는 구조에 더 가깝다. 즉 "테이블을 감추는 도구"가 아니라, "[[222_aggregate_ddd_transaction_consistency|애그리게이트]]를 제대로 다루게 만드는 설계 장치"라고 보는 것이 핵심이다.

- **📢 섹션 요약 비유**: 레파지토리는 부품 창고의 문을 하나 더 만드는 것이 아니라, 완성품을 안전하게 맡기고 다시 꺼내 쓸 수 있게 하는 보관 규칙을 세우는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[310_architecture|DDD]] ([[127_ddd_domain_driven_design|Domain-Driven Design]]) | 레파지토리는 [[222_aggregate_ddd_transaction_consistency|애그리게이트]] 중심 모델을 저장 기술로부터 분리하는 대표 패턴이다. |
| [[131_aggregate_root|Aggregate Root]] | 레파지토리가 외부에 노출하는 기본 저장·조회 단위다. |
| [[054_dao_decentralized_autonomous_organization|DAO]] ([[001_dikw_pyramid|Data]] Access Object) | 저장 기술 중심 계층화 패턴으로, 레파지토리와 초점이 다르다. |
| [[366_process|Hexagonal Architecture]] | 레파지토리를 포트로 두고 구현체를 어댑터로 배치하기 좋은 구조다. |
| Unit of Work | 레파지토리 저장과 함께 변경 추적·[[191_transaction_concept_states|트랜잭션]] 커밋을 협력한다. |
| [[306_cqrs|CQRS]] ([[271_command_pattern|Command]] Query Responsibility Segregation) | 읽기 모델과 [[289_cqrs_db|쓰기]] 모델을 분리해 레파지토리 책임을 과도하게 늘리지 않게 한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
직접 SQL / ORM 노출
    │
    ▼
DAO 수준의 저장 분리
    │
    ▼
DDD에서 애그리게이트 경계 인식
    │
    ▼
Repository interface 도입
    ├─ 도메인 언어 메서드
    ├─ 테스트 대역 교체
    └─ 인프라 구현 은닉
    │
    ▼
CQRS · Query Service · Unit of Work와 결합한 고도화
```

이 흐름은 레파지토리가 단순 저장 래퍼가 아니라, [[064_relation_domain|도메인]] 모델과 [[196_durability_permanent_storage|영속성]] 경계를 더 정교하게 분리하는 방향으로 발전했음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 레파지토리는 장난감을 아무 상자에나 넣지 않고, 같은 세트끼리 한 상자에 잘 모아 두는 정리함이에요.
2. 그래서 꺼낼 때도 부품 하나만 찾는 게 아니라 필요한 세트를 한 번에 가져올 수 있어요.
3. 정리함이 잘 되어 있으면 장난감 만드는 규칙도 덜 헷갈리고 다시 놀기도 쉬워져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 235 / 530

← **이전**: [[178_interceptor_filter_pattern|178. 인터셉터 / 필터 패턴 (Interceptor / Filter Pattern)]]
**다음**: [[180_transaction_script_vs_domain_model|180. 트랜잭션 스크립트 vs 도메인 모델 (Transaction Script vs Domain Model)]] →

---
