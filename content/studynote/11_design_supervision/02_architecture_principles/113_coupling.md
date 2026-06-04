+++
title = "113. 결합도 (Coupling)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) ([Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/))는 서로 다른 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)(클래스·[컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)·[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))이 상호 의존하는 정도를 측정하는 척도로, 낮을수록 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 독립적이고 변경 파급이 제한되어 유지보수가 용이하다.
> 2. **가치**: [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 낮추면 한 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)의 변경이 다른 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)에 미치는 영향을 최소화할 수 있어, 대규모 시스템에서의 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 개발·독립 배포·[단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/)가 가능해진다.
> 3. **판단 포인트**: 콘스탄틴의 6단계 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/))가 최선이며, 내용 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)(Content [Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/))가 최악이다. 실무에서는 "[모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) A를 수정할 때 반드시 B도 수정해야 하는가?"로 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 판단한다.

---

## Ⅰ. 개요 및 필요성

[결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)는 [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/)([Cohesion](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/))와 함께 1974년 콘스탄틴의 연구에서 정립된 소프트웨어 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 설계 품질 지표다. 높은 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)(tight [coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/))는 분산된 코드 변경(shotgun surgery), 연쇄적 테스트 실패, 독립 배포 불가라는 3가지 유지보수 재앙을 유발한다.

[마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/)([MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))의 핵심 목표 중 하나가 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 최소화하여 독립적 배포를 달성하는 것이다. 반대로 모놀리식(Monolithic) 시스템에서 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)가 높아지면 어느 한 부분의 배포가 전체 시스템 재시작을 필요로 하게 된다.

```text
+-------------------------------------------------------------+
|        결합도 6단계: 최악 -> 최선                             |
+-------------------------------------------------------------+
|  1. 내용 결합도 (Content Coupling) <- 가장 나쁨              |
|     +- 다른 모듈의 내부 데이터·코드에 직접 접근             |
|  2. 공통 결합도 (Common Coupling)                           |
|     +- 전역 변수(global variable) 공유                      |
|  3. 외부 결합도 (External Coupling)                         |
|     +- 외부 데이터 형식·통신 프로토콜 공유                  |
|  4. 제어 결합도 (Control Coupling)                          |
|     +- 제어 플래그(flag)를 전달하여 실행 흐름 제어          |
|  5. 스탬프 결합도 (Stamp Coupling)                          |
|     +- 필요 이상의 데이터 구조(객체 전체)를 전달             |
|  6. 데이터 결합도 (Data Coupling) <- 가장 좋음               |
|     +- 필요한 데이터만 매개변수로 전달                       |
+-------------------------------------------------------------+
```

[결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 개념 없이 설계하면 "스파게티 코드(spaghetti [code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/))"가 형성되어, 어디서 어디가 의존하는지 파악할 수 없는 상태가 된다. 이는 새 기능 추가 시 어디를 건드려야 할지 모르는 상황으로 이어진다.

- **📢 섹션 요약 비유**: 기차 객차들이 너무 단단히 연결되어 있으면 하나가 고장 나도 전체를 정지해야 한다. 적절히 느슨한 연결고리가 있어야 특정 객차만 교체할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 낮추는 핵심 기법은 인터페이스(interface)를 통한 간접 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/), 이벤트 기반 비동기 통신, [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/)([message broker](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/))를 통한 중간자 삽입이다. 직접 메서드 호출 대신 이벤트를 발행(publish)하고 구독(subscribe)하면 발행자와 구독자가 서로를 알 필요가 없어진다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 인터페이스 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) | 클래스 수준 | [DIP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/), 팩토리 패턴 |
| 이벤트 기반 통신 | [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/) 수준 | [옵저버 패턴](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/606_observer_pattern_pub_sub/), [이벤트 버스](/knowledge-base/studynote/04_software_engineering/11_testing_validation/931_event_bus_stream_processing/) |
| [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 | [Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), RabbitMQ |
| [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이 | 네트워크 수준 | [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/), [gRPC](/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 표준 인터페이스 |

```text
+-------------------------------------------------------------+
|      이벤트 기반 결합도 감소: 직접 호출 -> 이벤트 발행       |
+-------------------------------------------------------------+
| [강결합 - 직접 호출]                                        |
|  OrderService ---> InventoryService (직접 의존)              |
|  OrderService ---> NotificationService (직접 의존)           |
|                                                             |
| [약결합 - 이벤트 발행]                                      |
|  OrderService ---> EventBus <--- InventoryService (구독)      |
|                       <--- NotificationService (구독)        |
|                                                             |
|  결과: OrderService는 다른 서비스를 전혀 알지 못함           |
+-------------------------------------------------------------+
```

측정 지표로 구심성(Afferent [Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/), [Ca](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/))과 원심성(Efferent [Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/), Ce)이 있다. Ca는 해당 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)을 의존하는 외부 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 수, Ce는 해당 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 의존하는 외부 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 수다. 불안정도(Instability) = Ce / ([Ca](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) + Ce) 공식으로 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)의 변경 취약성을 정량화할 수 있다.

- **📢 섹션 요약 비유**: 음악 앙상블에서 각 악기 연주자가 악보(인터페이스)만 보고 연주하면, 특정 연주자가 바뀌어도 전체 연주는 계속된다. 하지만 연주자들이 서로의 손 동작을 보며 실시간으로 맞추면 한 명이 빠질 때 전체가 멈춘다.

---
## Ⅲ. 비교 및 연결

[결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)는 [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/)([Cohesion](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/))와 반드시 함께 검토해야 하며, 이 둘의 관계는 단순히 "[결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 낮추기 = [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/) 높이기"가 아니다. 둘 다 최적화해야 하는 독립적인 두 차원이다.

| 비교 축 | A | B |
|:---|:---|:---|
| **관찰 대상** | [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 간 연결 | [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 내부 요소들 |
| **목표 방향** | 낮을수록 좋음 | 높을수록 좋음 |
| **위반 증상** | 한 수정이 여러 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 변경을 강제 | 한 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 여러 이유로 변경됨 |
| **개선 기법** | 인터페이스, 이벤트, [메시지 브로커](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/) | [SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/), 기능별 클래스 분리 |

MSA에서 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)의 형태는 두 가지다. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스를 공유하는 "DB 공유 결합(Shared [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) [Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/))"이 가장 나쁜 패턴이고, 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 독립 DB를 가지며 이벤트로만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 동기화하는 "이벤트 결합"이 MSA에서 권장되는 형태다.

- **📢 섹션 요약 비유**: 도미노는 하나가 쓰러지면 전부 쓰러지는 최악의 결합 구조다. 반면 각자 독립적으로 세워진 조각품들은 하나가 쓰러져도 나머지에 영향을 주지 않는다.

---
## Ⅳ. 실무 적용 및 기술사 판단

[결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)([audit](/knowledge-base/studynote/12_it_management/05_security_compliance/363_audit/))는 감리 현장에서 응용 시스템 영역 감리의 핵심 점검 항목이다. 감리인은 클래스 의존성 다이어그램(class dependency diagram), 패키지 의존성 순환(circular dependency), [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 동기 호출 체인([synchronous](/knowledge-base/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/) [call](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) chain) 깊이를 점검한다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) A를 수정할 때 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) B도 반드시 수정해야 하는 경우가 있는가?
2. [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) 시 다른 클래스나 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 실제 구현이 없으면 테스트가 안 되는가?
3. 전역 변수(global [state](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/)) 또는 공유 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스를 통한 통신이 존재하는가?
4. 패키지 간 [순환 의존성](/knowledge-base/studynote/02_operating_system/05_deadlock/316_synchronization_bug_debugging/)(A -> B -> A)이 발생하는가?
5. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 동기 [REST](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) 호출 깊이가 3단계를 초과하는가?

- **📢 섹션 요약 비유**: 전기 콘센트에 멀티탭 하나가 연결되고, 그 멀티탭에 또 멀티탭이, 그 안에 또 멀티탭이 꽂혀 있으면 하나가 차단기를 내려도 전체 가전이 꺼진다. 결합을 분산하고 독립적 회로를 구성해야 한다.

---

## Ⅴ. 기대효과 및 결론

[결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 체계적으로 관리하면 각 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)을 독립적으로 배포할 수 있는 CD ([Continuous Delivery](/knowledge-base/studynote/13_cloud_architecture/04_devops_observability/164_continuous_delivery/), [지속적 배포](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/099_continuous_deployment_cd/)) 파이프라인이 현실화된다. 특히 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서 팀 A가 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) A를 팀 B 승인 없이 독립 배포할 수 있는 조직적 이점(Conway의 법칙 역활용)이 생긴다. 장애 격리(fault [isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))도 강화되어 한 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 장애가 전체 시스템 다운으로 이어지지 않는다.

한계는 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 낮출수록 시스템 전체의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) 관리가 어려워진다는 점이다. 이벤트 기반 비동기 통신은 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([eventual consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/))을 수용해야 하며, 이는 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 보장이 필수인 금융 거래 같은 도메인에서 설계 트레이드오프를 요구한다.

미래 방향으로는 ① [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)([Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/))를 통한 런타임 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 가시화, ② [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/)(extended [Berkeley Packet Filter](/knowledge-base/studynote/02_operating_system/01_overview_architecture/069_ebpf/)) 기반 실시간 의존성 추적, ③ DDD의 [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/) 자동 경계 도출 도구가 발전하고 있다.

[결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)는 "변경할 수 있는 자유도"의 척도다. 낮은 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)는 팀이 두려움 없이 코드를 변경할 수 있는 환경을 만들며, 이것이 소프트웨어 진화 속도를 결정한다.

- **📢 섹션 요약 비유**: [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)식 가구는 각 부품이 표준 나사 하나로 연결되어 있어 원하는 부분만 교체하거나 재배치할 수 있다. 모든 부품이 용접된 가구는 하나가 망가지면 전체를 버려야 한다.

---

### 📌 관련 개념 맵

[스파게티 코드] -> [결합도 측정] -> [인터페이스 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)·이벤트] -> [낮은 결합도] -> MSA 독립 배포]

| 개념 | 연결 포인트 |
|:---|:---|
| [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/) ([Cohesion](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/)) | [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)와 함께 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 설계 품질의 양대 축 |
| [DIP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/247_dip_dependency_inversion_principle/) ([의존성 역전 원칙](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/106_dip_dependency_inversion_principle/)) | [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 낮추기 위한 인터페이스 기반 설계 원칙 |
| [EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/) ([이벤트 주도 아키텍처](/knowledge-base/studynote/11_design_supervision/06_exam_summary/367_architecture/)) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)를 이벤트로 낮추는 아키텍처 |
| [바운디드 컨텍스트](/knowledge-base/studynote/04_software_engineering/04_testing_quality/221_bounded_context_ddd_msa_boundary/) | DDD의 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 경계 설계 기준 |

### 📈 관련 키워드 및 발전 흐름도

[강결합 스파게티 코드] -> [결합도 6단계 정립] -> [인터페이스·[DI](/knowledge-base/studynote/11_design_supervision/10_patterns_antipatterns/661_enterprise_di_framework_lifecycle/) 도입] -> [이벤트 기반 비동기 통신] -> MSA [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 독립 배포] -> [서비스 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/) [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 가시화]

### 👶 어린이를 위한 3줄 비유 설명

1. 레고 블록은 똑같은 모양의 구멍으로 연결되어 있어서 원하는 블록만 빼고 다른 것을 끼울 수 있어요.
2. 만약 모든 블록이 접착제로 붙어 있다면 하나를 바꾸려면 다 뜯어야 해요.
3. [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)가 낮다는 건 레고처럼 쉽게 끼우고 뺄 수 있는 구조를 뜻해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 168 / 530

<- **이전**: [112. 응집도 (Cohesion)](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/112_cohesion/)
**다음**: [113. 결합도 (Coupling)](/knowledge-base/studynote/11_design_supervision/02_architecture_principles/113_coupling/) ->

---
