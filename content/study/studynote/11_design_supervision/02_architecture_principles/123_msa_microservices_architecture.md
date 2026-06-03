+++
weight = 123
title = "123. 마이크로서비스 아키텍처 (MSA, Microservices Architecture)"
date = "2026-05-10"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[619_msa_traffic_hardware|MSA]] ([[122_msa_microservices_architecture|Microservices Architecture]], [[213_msa_microservices_architecture|마이크로서비스 아키텍처]])는 하나의 대형 모놀리식(monolithic) 시스템을 비즈니스 [[064_relation_domain|도메인]] 기능별로 독립 배포·운영 가능한 소규모 [[090_service_kubernetes_network_load_balancing|서비스]]들로 분해하여, 각 [[090_service_kubernetes_network_load_balancing|서비스]]가 자체 [[002_database_definition|데이터베이스]]를 소유하고 경량 [[295_protocol_field_tcp_udp_icmp|프로토콜]]([[461_http_stateless_connection_oriented|HTTP]] [[156_rest_representational_state_transfer|REST]], [[479_grpc_protobuf_http2|gRPC]])로 통신하는 아키텍처 스타일이다.
> 2. **가치**: 각 [[090_service_kubernetes_network_load_balancing|서비스]]를 독립적으로 개발·배포·확장할 수 있어 대규모 조직에서 팀별 자율성과 기술 다양성을 허용하며, 특정 [[090_service_kubernetes_network_load_balancing|서비스]]만 선택적으로 확장하여 자원 효율성을 높인다.
> 3. **판단 포인트**: MSA의 가장 큰 함정은 [[136_variance|분산]] 시스템의 복잡성(네트워크 장애, [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]], [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]], [[306_service_discovery_pattern|서비스 디스커버리]])을 과소평가하는 것이다. "MSA는 공짜 점심이 없다"는 원칙을 팀 역량과 운영 성숙도로 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

MSA는 마틴 파울러(Martin Fowler)와 제임스 루이스(James Lewis)가 2014년 공식화한 아키텍처 스타일이다. Netflix, Amazon, Uber 같은 대형 기술 기업들이 모놀리식 시스템의 한계를 극복하기 위해 실용적으로 발전시킨 아키텍처가 이론으로 정리되었다.

모놀리식 시스템의 한계는 세 가지다. ① 배포 병목: 하나의 기능 변경에도 전체 시스템 재배포가 필요, ② 확장 제약: 특정 기능만 확장하려 해도 전체를 스케일 아웃해야 함, ③ 기술 잠금: 하나의 언어·프레임워크가 전체 시스템을 구속. MSA는 이 세 문제를 [[090_service_kubernetes_network_load_balancing|서비스]] 독립성으로 해결한다.

```text
┌─────────────────────────────────────────────────────────────┐
│         모놀리식 → MSA 전환 구조 비교                        │
├─────────────────────────────────────────────────────────────┤
│  [모놀리식]                                                 │
│  ┌────────────────────────────────────────────────────┐     │
│  │  주문 | 결제 | 배송 | 회원 | 알림 | 정산 (단일 배포) │     │
│  └────────────────────────────────────────────────────┘     │
│                                                             │
│  [MSA]                                                      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │ 주문 │ │ 결제 │ │ 배송 │ │ 회원 │ │ 알림 │ │ 정산 │   │
│  │ 서비스│ │ 서비스│ │ 서비스│ │ 서비스│ │ 서비스│ │ 서비스│   │
│  │ +DB  │ │ +DB  │ │ +DB  │ │ +DB  │ │ +DB  │ │ +DB  │   │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘   │
│   각각 독립 배포, 독립 확장, 독립 기술 스택                  │
└─────────────────────────────────────────────────────────────┘
```

MSA에서 각 [[090_service_kubernetes_network_load_balancing|서비스]]는 자체 [[002_database_definition|데이터베이스]]([[311_database_per_service_pattern|Database per Service]] 패턴)를 갖는다. 공유 [[002_database_definition|데이터베이스]]는 MSA에서 가장 나쁜 안티패턴으로, [[002_database_definition|데이터베이스]] 수준에서 [[090_service_kubernetes_network_load_balancing|서비스]] 간 강결합이 발생하여 독립 배포가 불가능해진다.

- **📢 섹션 요약 비유**: 대형 백화점(모놀리식)을 상가([[619_msa_traffic_hardware|MSA]])로 전환하는 것과 같다. 각 매장([[090_service_kubernetes_network_load_balancing|서비스]])은 독립적으로 영업 시간, 인테리어, 재고(DB)를 관리하며 상가 건물(인프라)만 공유한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MSA의 12가지 핵심 패턴은 [[065_service_design|서비스 설계]], 통신, [[001_dikw_pyramid|데이터]], 운영으로 분류된다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| [[065_service_design|서비스 설계]] | [[221_bounded_context_ddd_msa_boundary|바운디드 컨텍스트]]([[310_architecture|DDD]]) | [[090_service_kubernetes_network_load_balancing|서비스]] 경계 결정 |
| 통신 | [[014_api_posix|API]] 게이트웨이, [[302_service_mesh_istio|서비스 메시]] | 외부·내부 통신 관리 |
| [[001_dikw_pyramid|데이터]] | [[311_database_per_service_pattern|Database per Service]], [[306_cqrs|CQRS]] | [[004_data_independence|데이터 독립성]] |
| [[571_resiliency_fault_tolerance_patterns|탄력성]] | [[307_circuit_breaker_pattern|서킷 브레이커]], 재시도 | 장애 격리 |
| 운영 | [[306_service_discovery_pattern|서비스 디스커버리]], 중앙 로깅 | [[136_variance|분산]] 시스템 관리 |

```text
┌─────────────────────────────────────────────────────────────┐
│       MSA 핵심 운영 인프라 구성                               │
├─────────────────────────────────────────────────────────────┤
│  클라이언트                                                  │
│       │                                                     │
│  [API Gateway] ─── 인증·라우팅·로드밸런싱                   │
│       │                                                     │
│  [Service Mesh (Istio)] ── mTLS·트래픽 제어·관찰성          │
│       │                                                     │
│  [서비스들] ── [서비스 디스커버리(Consul/Eureka)]            │
│       │                                                     │
│  [분산 트레이싱(Jaeger)] + [중앙 로깅(ELK)] + [메트릭(Prometheus)]│
└─────────────────────────────────────────────────────────────┘
```

[[307_circuit_breaker_pattern|서킷 브레이커]]([[304_circuit_breaker|Circuit Breaker]]) 패턴은 MSA에서 장애 전파를 차단하는 핵심 [[571_resiliency_fault_tolerance_patterns|탄력성]] 패턴이다. 외부 [[090_service_kubernetes_network_load_balancing|서비스]] 호출 실패율이 임계치를 초과하면 회로를 "열어" 즉각 실패(fail-fast)를 반환하고, 일정 시간 후 반개방 상태로 전환하여 [[090_service_kubernetes_network_load_balancing|서비스]] 복구를 시험한다.

- **📢 섹션 요약 비유**: 집의 전기 회로 차단기([[307_circuit_breaker_pattern|서킷 브레이커]])처럼, 특정 회선에 과부하가 걸리면 차단하여 전체 전기 시스템이 타는 것을 막는다. MSA에서도 한 [[090_service_kubernetes_network_load_balancing|서비스]] 장애가 전체로 번지는 것을 [[307_circuit_breaker_pattern|서킷 브레이커]]가 차단한다.

---
## Ⅲ. 비교 및 연결

[[619_msa_traffic_hardware|MSA]] 채택 결정에서 가장 중요한 비교는 모놀리식 대비 이점이 운영 복잡성 비용을 정당화하는지 여부다.

| 비교 축 | A | B |
|:---|:---|:---|
| **배포 단위** | 전체 시스템 | [[090_service_kubernetes_network_load_balancing|서비스]]별 독립 |
| **[[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]]** | 즉각적 (ACID [[191_transaction_concept_states|트랜잭션]]) | 최종 [[194_consistency_database_integrity|일관성]] |
| **팀 구조** | 기술 조직 (DB팀·개발팀) | 비즈니스 조직 (주문팀·결제팀) |
| **운영 복잡도** | 단순 | 높음 ([[136_variance|분산]] 시스템) |
| **최소 권장 팀** | 소규모 | "피자 두 판 팀" (5~8명) 이상 |

MSA에서 Conway의 법칙은 "조직 구조가 시스템 아키텍처를 결정한다"는 방향으로 작동한다. 팀 구조를 [[090_service_kubernetes_network_load_balancing|서비스]] 단위로 맞추지 않으면 MSA의 이점을 실현하기 어렵다. 역 Conway [[268_strategy_pattern|전략]](Inverse Conway Maneuver)은 원하는 아키텍처에 맞게 먼저 조직 구조를 변경하는 접근이다.

- **📢 섹션 요약 비유**: 군대 편제처럼 소규모 특수 부대([[532_microservices_decomposition_patterns|마이크로서비스]] 팀)가 각각의 임무를 독립적으로 수행하는 구조다. 대규모 정규군(모놀리식)은 집중력은 있지만 특정 임무만을 위해 부분 파견이 어렵다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[[619_msa_traffic_hardware|MSA]] 도입 실패의 가장 흔한 원인은 "조직과 운영 준비 없이 기술만 도입"하는 것이다. [[090_configuration_item|CI]]/CD 파이프라인, [[561_container_based_deployment|컨테이너]]([[063_docker_architecture|Docker]]), [[073_container_orchestration_tools|오케스트레이션]]([[205_kubernetes_container_orchestration|Kubernetes]]), [[112_distributed_tracing_microservices|분산 트레이싱]], 중앙 로깅이 모두 갖춰져야 MSA가 관리 가능한 복잡성 수준이 된다.

### 판단 [[435_checklist_based_testing|체크리스트]]
1. 팀이 충분히 크고 [[064_relation_domain|도메인]]별로 독립 팀 구성이 가능한가?
2. [[090_configuration_item|CI]]/CD, [[561_container_based_deployment|컨테이너]], [[205_kubernetes_container_orchestration|Kubernetes]] 운영 역량이 준비되어 있는가?
3. [[090_service_kubernetes_network_load_balancing|서비스]] 간 [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]] 문제([[305_saga|사가 패턴]], [[549_2pc_two_phase_commit_limitations_msa|2PC]] 등)에 대한 [[268_strategy_pattern|전략]]이 있는가?
4. [[112_distributed_tracing_microservices|분산 트레이싱]]·중앙 로깅·모니터링 인프라가 구축되어 있는가?
5. 모놀리식에서 MSA로 전환 시 [[376_strangler_fig_summary|스트랭글러 피그 패턴]] 같은 점진적 전환 계획이 있는가?

- **📢 섹션 요약 비유**: MSA는 도시(모놀리식)를 여러 독립 마을([[532_microservices_decomposition_patterns|마이크로서비스]])로 나누는 것이다. 마을마다 시청·경찰서·소방서(운영 인프라)가 필요하므로, 작은 인구에는 낭비가 되고 충분히 큰 인구일 때 효율적이다.

---

## Ⅴ. 기대효과 및 결론

MSA를 올바르게 적용하면 특정 [[090_service_kubernetes_network_load_balancing|서비스]]만 수평 확장하여 자원 효율성이 높아지고, 각 팀이 독립적으로 배포하여 출시 주기가 빨라진다. 특정 [[090_service_kubernetes_network_load_balancing|서비스]] 장애가 전체 시스템 장애로 이어지지 않는 격리(fault [[195_isolation_concurrency_control|isolation]])가 달성된다. 언어·프레임워크를 [[090_service_kubernetes_network_load_balancing|서비스]]별로 최적 선택하는 폴리글랏(polyglot) [[268_strategy_pattern|전략]]도 가능하다.

한계는 [[136_variance|분산]] 시스템의 본질적 복잡성이다. [[1002_network_delay_rtt_oneway_delay_components|네트워크 지연]], 부분 실패, [[001_dikw_pyramid|데이터]] [[194_consistency_database_integrity|일관성]], [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]]([[305_saga|사가 패턴]])은 모두 새로운 엔지니어링 도전이다. "[[136_variance|분산]] 시스템의 오류는 단일 시스템 오류보다 훨씬 찾기 어렵다"는 사실을 운영팀이 수용해야 한다.

미래 방향으로는 ① [[701_webassembly_wasm_frontend_performance|Wasm]] ([[319_webassembly_architecture|WebAssembly]]) 기반 초경량 [[090_service_kubernetes_network_load_balancing|서비스]], ② [[615_ebpf|eBPF]] 기반 [[302_service_mesh_istio|서비스 메시]]의 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 없는 구현, ③ [[190_ai_llm_requirements_specification|AI]] 기반 [[090_service_kubernetes_network_load_balancing|서비스]] 경계 자동 최적화가 발전하고 있다.

MSA는 기술이 아니라 "조직 역량과 운영 성숙도의 표현"이다. 기술만 도입하고 조직과 운영이 따라오지 못하면 "[[136_variance|분산]] 모놀리식([[537_anti_pattern_distributed_monolith|Distributed Monolith]])"이라는 최악의 결과가 된다.

- **📢 섹션 요약 비유**: 프랜차이즈 식당 브랜드처럼, 각 지점([[532_microservices_decomposition_patterns|마이크로서비스]])은 독립적으로 운영하되 공통 레시피([[014_api_posix|API]] 계약)와 브랜드 기준(아키텍처 표준)을 따른다.

---

### 📌 관련 개념 맵

[모놀리식 한계] → [[[619_msa_traffic_hardware|MSA]]] → [[[014_api_posix|API]] 게이트웨이·[[090_service_kubernetes_network_load_balancing|서비스]] 메시] → [[[310_architecture|DDD]] 바운디드 컨텍스트] → [[[205_kubernetes_container_orchestration|Kubernetes]] 운영]

| 개념 | 연결 포인트 |
|:---|:---|
| [[310_architecture|DDD]] [[221_bounded_context_ddd_msa_boundary|바운디드 컨텍스트]] | [[619_msa_traffic_hardware|MSA]] [[090_service_kubernetes_network_load_balancing|서비스]] 경계 결정의 핵심 원칙 |
| [[014_api_posix|API]] 게이트웨이 | [[619_msa_traffic_hardware|MSA]] 외부 진입점 단일화 |
| [[307_circuit_breaker_pattern|서킷 브레이커]] | [[619_msa_traffic_hardware|MSA]] [[090_service_kubernetes_network_load_balancing|서비스]] 간 장애 격리 [[571_resiliency_fault_tolerance_patterns|탄력성]] 패턴 |
| [[305_saga|사가 패턴]] ([[305_saga_pattern|Saga Pattern]]) | MSA에서 [[248_distributed_transaction_multiple_nodes|분산 트랜잭션]] 처리 방법 |

### 📈 관련 키워드 및 발전 흐름도

[모놀리식 배포 병목] → [[[618_soa_hardware|SOA]] ([[212_soa_service_oriented_architecture_esb|서비스 지향 아키텍처]])] → [[[619_msa_traffic_hardware|MSA]] 정립(파울러·루이스)] → [컨테이너·[[205_kubernetes_container_orchestration|Kubernetes]]] → [서비스 [[389_mesh_topology|메시]]·[[615_ebpf|eBPF]]] → [[[701_webassembly_wasm_frontend_performance|Wasm]] 초경량 서비스]

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 레고 세트(모놀리식) 대신 작은 레고 팩([[532_microservices_decomposition_patterns|마이크로서비스]]) 여러 개를 각자 조립하는 것이에요.
2. 한 팩을 바꾸거나 추가해도 나머지 팩에 영향을 주지 않아요.
3. 하지만 팩들이 너무 많아지면 어떤 팩이 어디에 있는지 관리하는 일이 더 중요해져요!
