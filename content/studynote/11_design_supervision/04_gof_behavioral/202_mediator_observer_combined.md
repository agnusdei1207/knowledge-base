---
title: "Mediator and Observer Combined"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 202
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [미디에이터 패턴](/studynote/11_design_supervision/04_gof_behavioral/201_mediator_pattern/)과 [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/)은 상호 보완적이다. [옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/)가 Subject-[Observer](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/) 간 1:N 이벤트 통지를 다루고, 미디에이터가 다수 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 간 N:N 통신을 중재할 때, 두 패턴을 조합하면 이벤트 기반의 느슨하게 결합된 복잡한 시스템을 우아하게 설계할 수 있다.
> 2. **가치**: 미디에이터를 [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/)으로 구현하면: 미디에이터(Subject)가 이벤트를 발행하고 각 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)([Observer](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))가 필요한 이벤트만 구독하여, 미디에이터의 비대화 없이 유연한 중재가 가능하다. 스프링의 ApplicationEvent 시스템이 이 조합의 대표 구현이다.
> 3. **판단 포인트**: 두 패턴 조합의 경계를 명확히 설정해야 한다. 동기 처리가 필요하면 [옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/) 기반 미디에이터, 비동기·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 처리가 필요하면 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)/RabbitMQ 기반 [메시지 브로커](/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/)([분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 미디에이터+[옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))를 선택한다.

---

## Ⅰ. 개요 및 필요성

실무에서 두 패턴을 순수하게 분리하여 적용하기보다, 함께 조합하여 더 강력한 설계를 달성하는 경우가 많다. [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/)(EventBus)가 대표적인 두 패턴의 조합이다.

[이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/) 구조: ① [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)가 이벤트를 EventBus(미디에이터)에 발행(publish), ② EventBus가 해당 이벤트를 구독한 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)([옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))에게 통지(notify), ③ 구독자가 이벤트를 처리. [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)는 서로를 직접 알지 못하고, 이벤트 타입으로만 통신한다.

```text
+-------------------------------------------------------------+
|     미디에이터 + 옵저버 통합 (이벤트 버스)                   |
+-------------------------------------------------------------+
|                                                             |
|  CompA --publish(EventX)--> EventBus(Mediator+Subject)       |
|                                |                            |
|                     notify(EventX) to subscribers          |
|                                |                            |
|                    +-----------+------------+               |
|               CompB(Observer)  CompC        CompD           |
|               handles EventX   handles EventX               |
|                                                             |
|  CompA와 CompB/C/D는 서로를 알지 못함                       |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 공항 방송 시스템(EventBus)이 탑승 안내(EventX)를 방송하면, 해당 항공기 탑승객([옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))만 반응한다. 방송 시스템이 미디에이터이자 Subject 역할을 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

스프링의 `ApplicationEvent` 시스템이 두 패턴의 통합 구현이다. `ApplicationEventPublisher`(미디에이터+Subject)가 이벤트를 발행하면, `@EventListener`([옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))가 해당 이벤트를 처리한다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 스프링 ApplicationEvent | ApplicationEventPublisher / @EventListener | 동기 (기본) |
| Guava EventBus | EventBus / @Subscribe | 동기 |
| 스프링 @Async 이벤트 | ApplicationEventPublisher / @Async @EventListener | 비동기 |
| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) 기반 [EDA](/studynote/12_it_management/02_itsm_itil/064_eda/) | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) Broker / Consumer | 비동기·[분산](/studynote/08_algorithm_stats/08_stats/136_variance/) |

```text
+-------------------------------------------------------------+
|       스프링 두 패턴 통합 구현                               |
+-------------------------------------------------------------+
|  // 발행 (미디에이터 통해 이벤트 발행)                       |
|  @Service class OrderService {                              |
|    applicationEventPublisher.publishEvent(                  |
|      new OrderCompletedEvent(orderId));                     |
|  }                                                          |
|                                                             |
|  // 구독 (옵저버)                                           |
|  @Component class EmailService {                            |
|    @EventListener                                           |
|    void onOrderCompleted(OrderCompletedEvent e) { ... }     |
|  }                                                          |
|                                                             |
|  @Component class InventoryService {                        |
|    @EventListener                                           |
|    void onOrderCompleted(OrderCompletedEvent e) { ... }     |
|  }                                                          |
+-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 쇼핑몰(OrderService)이 주문 완료(이벤트)를 방송하면, 이메일 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 재고 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)([옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))가 각자의 방식으로 처리한다. 쇼핑몰은 두 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 직접 알 필요 없다.

---
## Ⅲ. 비교 및 연결

두 패턴 조합의 발전: 단일 앱 내 [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/)(스프링 ApplicationEvent) -> [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/)([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), RabbitMQ) -> [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)([Event Sourcing](/studynote/12_it_management/05_security_compliance/307_event_sourcing/)) + 두 패턴 통합.

| 비교 축 | A | B |
|:---|:---|:---|
| 단일 앱 (인프로세스) | 스프링 ApplicationEvent | 동기, [트랜잭션](/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 공유 |
| [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) (비동기) | [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), RabbitMQ | 비동기, 느슨한 결합 |
| [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) 통합 | 이벤트 스토어 + 구독 | 이벤트 히스토리 보존 |

- **📢 섹션 요약 비유**: 사내 이메일(인프로세스 이벤트)이 회사 내부 소통이라면, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [메시지 브로커](/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/)([Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/))는 다른 회사([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))와의 공식 우편 시스템이다.

---
## Ⅳ. 실무 적용 및 기술사 판단

설계사 시험에서 두 패턴의 통합 설계를 서술할 때 핵심 포인트: ① 단일 앱 내에서 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 결합도를 낮추기 위해 스프링 ApplicationEvent 사용, ② [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 간 통신에서 Kafka가 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 미디에이터+Subject 역할, ③ [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)에서 이벤트 스토어가 모든 상태 변경의 [옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/)-미디에이터 조합.

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 이벤트 발행자(미디에이터)와 구독자([옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))가 인터페이스로 분리되어 서로를 알지 못하는가?
2. 동기 처리(스프링 ApplicationEvent)와 비동기 처리(@Async EventListener, [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/))를 요구사항에 맞게 선택했는가?
3. [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/)가 비대해지지 않도록 도메인별로 이벤트 채널을 분리했는가?
4. [미디에이터 패턴](/studynote/11_design_supervision/04_gof_behavioral/201_mediator_pattern/)(중재)과 [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/)(1:N 통지)의 역할이 명확히 구분되는가?
5. [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 이벤트 중복 처리, 순서 보장, 재처리(Retry) 전략을 설계했는가?

- **📢 섹션 요약 비유**: 도서관(미디에이터)이 새 책 입고(이벤트)를 공지하면, 관심 분야 등록 회원([옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))에게만 알림이 간다. 도서관은 회원들이 어떻게 책을 이용하는지 알 필요 없다.

---

## Ⅴ. 기대효과 및 결론

[미디에이터 패턴](/studynote/11_design_supervision/04_gof_behavioral/201_mediator_pattern/)과 [옵저버 패턴](/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/)의 통합은 [이벤트 기반 아키텍처](/studynote/04_software_engineering/09_cloud_native_ai_architecture/538_event_driven_architecture_eda/)([EDA](/studynote/12_it_management/02_itsm_itil/064_eda/))의 핵심 설계 원리다. 두 패턴을 조합하면 [컴포넌트](/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 간 결합도를 최소화하고, 이벤트 기반으로 유연하게 확장 가능한 시스템을 구축할 수 있다.

결론: 단일 앱에서는 스프링 ApplicationEvent로 두 패턴을 통합하고, [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)에서는 [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/)/RabbitMQ로 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 이벤트 미디에이터를 구현하라. [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/)과 결합하면 완전한 [이벤트 기반 아키텍처](/studynote/04_software_engineering/09_cloud_native_ai_architecture/538_event_driven_architecture_eda/)가 완성된다.

- **📢 섹션 요약 비유**: 두 패턴의 조합은 공항 관제 시스템(미디에이터)과 승객 안내 방송([옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/))을 통합하여, 복잡한 공항 운영을 각 부서가 독립적으로 처리하면서도 전체가 조화롭게 동작하게 한다.

---

### 📌 관련 개념 맵

[두 패턴 조합의 필요성] -> [이벤트 [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)(EventBus)] -> [스프링 ApplicationEvent] -> Kafka [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 이벤트] -> [이벤트 소싱+[CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/)]

| 개념 | 연결 포인트 |
|:---|:---|
| [이벤트 주도 아키텍처](/studynote/11_design_supervision/06_exam_summary/367_architecture/)([EDA](/studynote/12_it_management/02_itsm_itil/064_eda/)) | 두 패턴 조합의 아키텍처 수준 적용 |
| [이벤트 소싱](/studynote/06_ict_convergence/03_cloud_infrastructure/249_event_sourcing_append_only_state_reconstruction/) | 이벤트를 영구 저장하는 [EDA](/studynote/12_it_management/02_itsm_itil/064_eda/) 확장 |
| [Kafka](/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/) | [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에서 미디에이터+Subject 역할 |
| 스프링 ApplicationEvent | 단일 앱에서의 두 패턴 통합 구현 |

### 📈 관련 키워드 및 발전 흐름도

[GoF 두 패턴 조합] -> [스프링 ApplicationEvent] -> [Guava EventBus] -> Kafka [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 이벤트 버스] -> [이벤트 소싱+[CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) 완전 통합]

### 👶 어린이를 위한 3줄 비유 설명

1. 미디에이터(채팅방)와 [옵저버](/studynote/04_software_engineering/04_testing_quality/267_observer_pattern/)(구독 알림)를 합치면 [이벤트 버스](/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/)가 돼요!
2. 쇼핑몰이 주문 완료 이벤트를 발행하면, 이메일·재고·포인트 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 각자 처리해요.
3. 스프링 ApplicationEvent와 Kafka가 바로 이 두 패턴의 통합 구현이에요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 263 / 530

<- **이전**: [201. 미디에이터 패턴 (Mediator Pattern)](/studynote/11_design_supervision/04_gof_behavioral/201_mediator_pattern/)
**다음**: [203. 방문자 패턴 (Visitor Pattern)](/studynote/11_design_supervision/04_gof_behavioral/203_visitor_pattern/) ->

---
