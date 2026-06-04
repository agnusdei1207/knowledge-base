+++
title = "201. 미디에이터 패턴 (Mediator Pattern)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 미디에이터 패턴 ([Mediator Pattern](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/))은 GoF 행위 패턴으로, 객체들이 직접 참조하며 복잡하게 상호작용하는 대신, [중재자](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/)([Mediator](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/)) 객체를 통해 통신하게 하여 객체 간 N:N 결합을 N:1+1:N으로 단순화하는 패턴이다.
> 2. **가치**: [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 간 직접 참조를 제거하여 결합도를 낮추고, 상호작용 로직을 미디에이터에 집중시켜 각 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)를 독립적으로 재사용·테스트할 수 있게 한다. 채팅방, 항공 관제, MVC의 Controller, CQRS의 MediatR가 대표 사례다.
> 3. **판단 포인트**: 미디에이터 패턴은 미디에이터 자체가 '신(God) 객체'가 되어 비대해지는 위험이 있다. 미디에이터가 너무 많은 책임을 가지면 오히려 유지보수가 어려워진다. 도메인별로 미디에이터를 분리하거나, [이벤트 버스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/539_event_bus_stream_processing/)(EventBus)로 대체하는 것을 고려해야 한다.

---

## Ⅰ. 개요 및 필요성

GUI 애플리케이션에서 버튼·체크박스·텍스트필드가 서로 직접 참조하면 N(N-1) 관계가 형성되어 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 재사용·교체가 어렵다. 미디에이터(다이얼로그 클래스)가 모든 상호작용을 중재하면 각 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)는 미디에이터만 알면 된다.

실세계 예시: ① 항공 관제탑([Mediator](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/))이 모든 항공기([컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/))의 통신을 중재, ② 채팅방([Mediator](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/))이 모든 참여자([컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/))의 메시지를 중계, ③ MVC의 Controller가 View와 Model 간의 [중재자](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/), ④ .NET MediatR 라이브러리가 [커맨드](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)·[쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 처리를 중재.

```text
+-------------------------------------------------------------+
|          미디에이터 패턴 구조                                  |
+-------------------------------------------------------------+
|  Before (N:N 결합)          After (미디에이터)               |
|  A <----> B                   A -> Mediator -> B               |
|  A <----> C                   B -> Mediator -> C               |
|  B <----> C                   C -> Mediator -> A               |
|  (모두 직접 참조)            (미디에이터만 참조)              |
|                                                             |
|  Mediator (인터페이스)                                       |
|  + notify(sender: Colleague, event: String): void           |
|       ^                                                     |
|  ConcreteMediator                                           |
|  - colleagues: List<Colleague>                              |
|  + notify(sender, event) { // 중재 로직 }                   |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 항공 관제탑([Mediator](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/))이 모든 항공기([컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/))의 통신을 중재한다. 항공기들이 서로 [직접 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/120_direct_communication/)하면 충돌 위험이 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

.NET의 MediatR 라이브러리가 [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/) 패턴에서 미디에이터를 구현한다. `IMediator.Send(command)`를 호출하면 등록된 `IRequestHandler<TCommand>`가 처리한다. 이를 통해 Controller가 직접 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 호출하는 대신 미디에이터를 통해 느슨하게 통신한다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| MVC Controller | [View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/) ↔ Model 중재 | Spring MVC |
| [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/) [Mediator](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/) | [Command](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)/Query [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) | MediatR (.NET) |
| 채팅방 | 참여자 간 메시지 중계 | ChatRoom 객체 |
| EventBus | 느슨한 이벤트 중재 | Spring ApplicationEventPublisher |

```text
+-------------------------------------------------------------+
|       MediatR CQRS 미디에이터 동작                           |
+-------------------------------------------------------------+
|  Controller -> IMediator.Send(CreateOrderCommand)            |
|       v                                                     |
|  Mediator -> CreateOrderCommandHandler.Handle(command)       |
|       v                                                     |
|  Result -> Controller (Handler가 처리 결과 반환)             |
|                                                             |
|  Controller는 Handler를 직접 알지 못함                       |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 부동산 중개사([Mediator](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/))가 매수자(Controller)와 매도자(Handler)를 중재한다. 매수자는 매도자를 직접 알 필요 없다.

---
## Ⅲ. 비교 및 연결

미디에이터 패턴과 [옵저버 패턴](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/)의 비교: [옵저버](/knowledge-base/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/)는 Subject가 Observer에게 1:N으로 통지하고, 미디에이터는 N:N 통신을 N:1+1:N으로 중재한다.

| 비교 축 | A | B |
|:---|:---|:---|
| 통신 방향 | N:N -> [Mediator](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/) 중재 | 1:N (Subject -> [Observer](/knowledge-base/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/)) |
| 결합 제거 | 모든 참여자 간 결합 | Subject-[Observer](/knowledge-base/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/) 결합 |
| 중앙화 | O (미디에이터 비대화 위험) | Subject [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) |
| 대표 사례 | 채팅방, [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/) [Mediator](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/) | 이벤트 시스템, MVC |

- **📢 섹션 요약 비유**: 미디에이터는 채팅방(모든 참여자 간 통신 중재)이고, [옵저버](/knowledge-base/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/)는 방송국(1개 Subject가 N개 Observer에게 일방적 통지)이다.

---
## Ⅳ. 실무 적용 및 기술사 판단

스프링에서 미디에이터 패턴은 `ApplicationEventPublisher` 기반 이벤트 시스템으로 구현된다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 이벤트를 발행하면 미디에이터([이벤트 버스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/539_event_bus_stream_processing/))가 적절한 핸들러로 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)한다. 이벤트 기반 마이크로서비스에서 Kafka가 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 미디에이터 역할을 한다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 간 N:N 직접 참조를 미디에이터를 통해 N:1+1:N으로 단순화했는가?
2. 미디에이터가 너무 많은 책임을 갖지 않도록(God 객체 방지) 적절히 분리했는가?
3. MVC의 Controller, CQRS의 Mediator가 미디에이터 패턴의 구현임을 이해하는가?
4. [옵저버 패턴](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/)과 미디에이터 패턴의 차이(1:N vs N:N 중재)를 구분하는가?
5. [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), RabbitMQ 등 [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/)를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서의 미디에이터로 이해하는가?

- **📢 섹션 요약 비유**: 항공 관제탑이 항공기 수가 늘어도 [직접 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/120_direct_communication/) 없이 안전하게 관리하듯, 미디에이터는 참여자 수에 관계없이 복잡성을 일정하게 유지한다.

---

## Ⅴ. 기대효과 및 결론

미디에이터 패턴을 적용하면 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 간 복잡한 N:N 결합이 N:1로 단순화되어 각 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)를 독립적으로 개발·테스트·재사용할 수 있다. [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/)·MVC·이벤트 주도 아키텍처에서 핵심 패턴으로 활용된다.

한계는 미디에이터가 비대해지면 단일 실패 지점([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))이 되고, 복잡한 중재 로직이 미디에이터에 집중되어 God 객체가 될 수 있다. 도메인별 미디에이터 분리 또는 [이벤트 버스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/539_event_bus_stream_processing/) 활용으로 이를 방지한다.

- **📢 섹션 요약 비유**: 미디에이터 패턴은 오케스트라 지휘자([Mediator](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/))가 각 단원([컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/))을 조율하는 것이다. 지휘자가 없으면 단원들이 서로 박자를 맞추기 어렵다.

---

### 📌 관련 개념 맵

[N:N 결합 문제] -> [미디에이터 패턴] -> [MVC Controller] -> CQRS MediatR] -> [분산 메시지 브로커]

| 개념 | 연결 포인트 |
|:---|:---|
| [옵저버 패턴](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/) | 미디에이터와 대비되는 1:N 통지 패턴 |
| [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/) | MediatR 라이브러리가 미디에이터 역할 |
| [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/) ([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서의 미디에이터 |
| MVC Controller | 가장 익숙한 미디에이터 패턴 구현 |

### 📈 관련 키워드 및 발전 흐름도

[GoF [Mediator](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/)(1994)] -> [MVC Controller] -> CQRS MediatR] -> [이벤트 버스] -> Kafka [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 미디에이터]

### 👶 어린이를 위한 3줄 비유 설명

1. 미디에이터 패턴은 채팅방처럼, 모든 참여자가 채팅방(미디에이터)을 통해 소통해요.
2. 참여자들이 서로 직접 연락처를 알 필요가 없어요.
3. 항공 관제탑, MVC Controller, [CQRS](/knowledge-base/studynote/12_it_management/05_security_compliance/306_cqrs/) MediatR이 모두 이 패턴이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 262 / 530

<- **이전**: [200. 책임 연쇄 패턴 장단점 (Chain of Responsibility Pros and Cons)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/200_chain_of_responsibility_pros_cons/)
**다음**: [202. 미디에이터·옵저버 통합 설계 (Mediator and Observer Combined)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/202_mediator_observer_combined/) ->

---
