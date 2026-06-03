+++
title = "250. 메시지 패싱과 위임 (Message Passing & Delegation)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 메시지 패싱 ([Message Passing](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)) 은 객체지향 (Object-Oriented) 패러다임의 핵심 메커니즘으로, 객체는 서로에게 메시지를 보내 협력하고 수신 객체가 메시지 처리 방법을 스스로 결정한다.
> 2. **가치**: 위임 (Delegation) 은 메시지 패싱의 응용으로, 특정 책임을 다른 객체에게 넘김으로써 런타임 유연성과 [단일 책임 원칙](/knowledge-base/studynote/11_design_supervision/06_exam_summary/355_process/) ([SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/): [Single Responsibility Principle](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/)) 을 동시에 달성한다.
> 3. **판단 포인트**: "이 객체가 직접 처리하는 것보다 더 잘 처리할 수 있는 객체가 있는가?" — Yes라면 위임이 답이다.

---

## Ⅰ. 개요 및 필요성
앨런 케이 (Alan Kay) 는 객체지향의 핵심이 데이터와 함수가 아니라 **메시지 (Message)** 라고 강조했다. 객체는 서로의 내부를 알 필요 없이 메시지(메서드 호출)를 통해서만 협력한다. 수신 객체가 **다형성 (Polymorphism)** 에 따라 메시지 처리 방식을 결정한다.

| 특성 | 설명 |
|:---|:---|
| 캡슐화 (Encapsulation) | 수신자 내부 구현 비공개 |
| 다형성 (Polymorphism) | 동일 메시지, 다른 처리 |
| 느슨한 결합 (Loose [Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)) | 인터페이스(계약)로만 연결 |
| 비동기 가능 | 메시지 큐를 통한 비동기 전달 |

위임 (Delegation) 은 "객체 A가 받은 요청을 처리하기 위해 객체 B에게 처리를 위임하는 것"이다. A는 요청의 존재를 알지만 **실제 처리 로직은 B에 있다**. 이는 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) (Inheritance) 의 대안으로, 구성 (Composition) 을 통한 동작 확장을 가능하게 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Problem</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">Core Idea</div><div class="kb-diagram-cell">──▶</div><div class="kb-diagram-cell">Expected Gain</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 회사 대표가 법무 문제를 처리할 때 직접 법률 공부를 하는 대신 법무팀에 위임하는 것 — 대표는 "법무 처리해줘"라는 메시지만 보낸다.

---

## Ⅱ. 아키텍처 및 핵심 원리


<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">메시지 패싱 기본 구조</div></div>
<div class="kb-diagram-note">메시지(요청)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Sender</div><div class="kb-diagram-cell">▶</div><div class="kb-diagram-cell">Receiver</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">◀</div><div class="kb-diagram-cell">처리 후 응답</div></div>
<div class="kb-diagram-tree-item" style="--depth:0">응답(결과)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">위임 체인 구조</div></div>
<div class="kb-diagram-note">위임 위임</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Client</div><div class="kb-diagram-cell">▶</div><div class="kb-diagram-cell">Handler A</div><div class="kb-diagram-cell">▶</div><div class="kb-diagram-cell">Delegate B</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(책임 일부)</div><div class="kb-diagram-cell">(실제 처리)</div></div>
<div class="kb-diagram-connector">▲</div>
<div class="kb-diagram-note">책임 분산 (Responsibility Distribution)</div>
</div>
</div>





<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">class PrinterManager {</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">private PrintJob job; // 구성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">private PrintQueue queue; // 위임 대상</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">private PrintDevice device; // 위임 대상</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">void print(Document doc) {</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">job = new PrintJob(doc);</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">queue.enqueue(job); // 큐잉 위임</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">device.execute(queue.next()); // 실행 위임</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">}</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">// PrinterManager는 조율만, 실제 처리는 위임</div></div>
</div>
</div>



메서드가 다른 클래스의 데이터에 집착 (Feature Envy 스멜) 하면, 그 메서드를 해당 클래스로 이동 (Move Method) 하거나, 해당 클래스 객체에게 위임하도록 재구성한다.

| 항목 | 설명 | 포인트 |
|:---|:---|:---|
| 핵심 역할 | 입력·상태·출력을 분리하는 책임 경계 | 구현보다 경계를 먼저 본다. |
| 제어 지점 | 조건, 이벤트, 정책이 만나는 곳 | 병목과 결합이 생기는 곳이다. |
| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 포인트 | 테스트·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·모니터링으로 확인할 지점 | 운영 가능성이 설계 품질을 결정한다. |

- **📢 섹션 요약 비유**: 커피숍에서 점원이 직접 원두 로스팅부터 다 하지 않고 "드리퍼에게 추출 위임, 그라인더에게 분쇄 위임"하는 것처럼, 위임은 전문화된 객체에게 일을 맡기는 것이다.

---

## Ⅲ. 비교 및 연결
| 구분 | [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) (Inheritance) | 위임 (Delegation) |
|:---|:---|:---|
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 유형 | is-a | has-a / uses-a |
| 결합 시점 | 컴파일 타임 (정적) | 런타임 (동적 교체 가능) |
| [LSP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/245_lsp_liskov_substitution_principle/) 위반 위험 | 있음 | 없음 |
| 코드 재사용 방식 | 부모 코드 자동 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) | 명시적 위임 호출 |
| 유연성 | 낮음 | 높음 |
| 권장 원칙 | is-a [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 확실할 때 | 기본 선택 (GoF 권고) |

GoF (Gang of Four) 의 『[디자인 패턴](/knowledge-base/studynote/04_software_engineering/04_testing_quality/251_design_patterns_gof_overview/) ([Design Patterns](/knowledge-base/studynote/04_software_engineering/04_testing_quality/251_design_patterns_gof_overview/))』 은 "클래스 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)보다 객체 구성을 선호하라"를 핵심 원칙으로 제시한다.

| 패턴 | 위임 활용 방식 |
|:---|:---|
| [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/) ([Strategy Pattern](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 객체에 위임 |
| [데코레이터 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/)) | 책임을 래퍼(Wrapper) 에 순차 위임 |
| [커맨드 패턴](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/196_command_pattern/) ([Command Pattern](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/)) | 실행을 [커맨드](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/) 객체에 위임 |
| [프록시 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/) ([Proxy Pattern](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/158_proxy_pattern/)) | 접근 제어를 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)에 위임 |
| [어댑터 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/383_adapter_pattern_summary/) ([Adapter Pattern](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/151_adapter_pattern/)) | 인터페이스 변환을 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)에 위임 |

- **📢 섹션 요약 비유**: 오케스트라 지휘자는 악기를 직접 연주하지 않고 각 악기 섹션에 위임한다 — 위임이 없으면 100인조 오케스트라가 아니라 혼자서 모든 악기를 연주해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단
[이벤트 주도 아키텍처](/knowledge-base/studynote/11_design_supervision/06_exam_summary/367_architecture/) ([EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/): [Event-Driven Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/140_event_driven_architecture_eda/)) 는 메시지 패싱의 비동기 버전이다. [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 직접 메서드 호출 대신 **이벤트 브로커 (Event Broker)** ([Kafka](/knowledge-base/studynote/14_data_engineering/04_mlops/179_kafka_flink_watermark_time_window/), RabbitMQ) 를 통해 메시지를 전달한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">동기 메시지 패싱</div><div class="kb-diagram-node">비동기 메시지 패싱 (EDA)</div></div>
<div class="kb-diagram-note">OrderService OrderService</div>
<div class="kb-diagram-note">→ PaymentService.pay() → Kafka.publish(OrderCreated)</div>
<div class="kb-diagram-note">→ InventoryService.reserve() ← PaymentService 구독·처리</div>
<div class="kb-diagram-note">← InventoryService 구독·처리</div>
</div>
</div>



[책임 연쇄 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/395_process/) ([Chain of Responsibility](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/276_chain_of_responsibility_pattern/) Pattern) 은 메시지를 처리할 수 있는 핸들러를 체인으로 연결해 적합한 핸들러에게 위임하는 구조다. [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 미들웨어 체인, 예외 처리 체인, 로깅 파이프라인 등에 활용된다.

- <strong><a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/">응집도</a>와 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/">결합도</a></strong>: 위임은 클래스 [응집도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/) ([Cohesion](/knowledge-base/studynote/04_software_engineering/04_testing_quality/193_cohesion_levels/)) 를 높이고 클래스 간 [결합도](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) ([Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)) 를 낮추는 핵심 수단임을 수치로 표현
- <strong><a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/">마이크로서비스</a> (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">Microservices</a>)</strong>: [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신이 메시지 패싱이며, 각 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 단일 책임 ([SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/)) 을 가져야 함을 논거로 활용
- **테스트 용이성**: 위임 대상 객체를 목([Mock](/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/)) 으로 교체해 격리 테스트 가능

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 해결하려는 변화 축이 분명한가?
2. [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 비용보다 변경 절감 효과가 큰가?
3. 테스트·[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)·운영 가시성이 확보되는가?
4. 팀이 이 구조를 일관되게 유지할 수 있는가?

- **📢 섹션 요약 비유**: 물류 센터에서 "소포 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)"는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 컨베이어에, "배송 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)"은 GPS 시스템에, "고객 알림"은 SMS 시스템에 위임하면 각 시스템이 독립적으로 개선될 수 있다.

---

## Ⅴ. 기대효과 및 결론
| 지표 | [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 중심 설계 | 위임 중심 설계 |
|:---|:---:|:---:|
| 런타임 동작 교체 가능 여부 | 불가 | 가능 ([전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 교체) |
| [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) 깊이 (최대) | 5~7단 | 1~2단 |
| [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) 격리 용이성 | 낮음 | 높음 ([Mock](/knowledge-base/studynote/04_software_engineering/11_testing_validation/462_mock_test_double/) 주입) |
| 새 기능 추가 수정 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수 | 많음 | 적음 (위임 객체 1개) |

메시지 패싱 ([Message Passing](/knowledge-base/studynote/02_operating_system/02_process_thread/119_message_passing/)) 과 위임 (Delegation) 은 객체지향 설계의 <strong>두 기둥</strong>이다. 메시지 패싱은 객체 간 협력의 언어이고, 위임은 책임을 적합한 전문가에게 분배하는 조직 원리다. "[상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)보다 구성, 직접 처리보다 위임"이라는 GoF (Gang of Four) 의 격언은 지금도 유효하며, [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)와 [이벤트 주도 아키텍처](/knowledge-base/studynote/11_design_supervision/06_exam_summary/367_architecture/) ([EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/)) 시대에 더욱 중요해지고 있다.

확장 방향은 ① 선언형 API와의 결합, ② [관측 가능성](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/111_observability_metrics_logs_traces/)([Observability](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/)) 내장, ③ [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 환경에 맞는 변형 패턴 적용이다.

- **📢 섹션 요약 비유**: 훌륭한 리더는 모든 일을 직접 하지 않고, 적합한 팀원에게 적합한 일을 맡기며 "결과 보고해줘"라는 메시지만 보낸다 — 이것이 위임과 메시지 패싱의 조직적 본질이다.

---

### 📌 관련 개념 맵
| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [객체지향 프로그래밍](/knowledge-base/studynote/04_software_engineering/06_software_architecture/322_oop_4_characteristics/) ([OOP](/knowledge-base/studynote/04_software_engineering/06_software_architecture/322_oop_4_characteristics/): Object-Oriented Programming) | 메시지 패싱의 토대 |
| 핵심 원칙 | 구성 우선 (Composition over Inheritance) | 위임의 철학적 근거 |
| 연관 개념 | [전략 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/391_strategy_pattern_summary/) ([Strategy Pattern](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)) | [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 위임의 전형 |
| 연관 개념 | [데코레이터 패턴](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/) ([Decorator Pattern](/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/155_decorator_pattern/)) | 순차 위임 체인 |
| 연관 개념 | [책임 연쇄 패턴](/knowledge-base/studynote/11_design_supervision/06_exam_summary/395_process/) ([Chain of Responsibility](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/276_chain_of_responsibility_pattern/)) | 메시지 위임 체인 |
| 연관 개념 | [EDA](/knowledge-base/studynote/12_it_management/02_itsm_itil/064_eda/) ([Event-Driven Architecture](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/140_event_driven_architecture_eda/)) | 비동기 메시지 패싱 |
| 연관 개념 | 느슨한 결합 (Loose [Coupling](/knowledge-base/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/)) | 위임의 결과 |
| 연관 개념 | [단일 책임 원칙](/knowledge-base/studynote/11_design_supervision/06_exam_summary/355_process/) ([SRP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/243_srp_single_responsibility_principle/)) | 위임을 통해 달성 |

### 📈 관련 키워드 및 발전 흐름도
객체 협력 → 메시지 패싱과 위임 → actor/event message

### 👶 어린이를 위한 3줄 비유 설명
1. 숙제할 때 수학은 수학 선생님, 과학은 과학 선생님, 글짓기는 국어 선생님께 각각 도움을 청하는 것이 위임이다.
2. "도와주세요"라고 말하는 것이 메시지 패싱이고, 선생님이 각자 방법으로 도와주는 것이 다형성이다.
3. 위임을 잘 하면 혼자 모든 걸 알 필요 없이, 전문가에게 맡겨서 더 좋은 결과를 얻을 수 있다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 311 / 530

← **이전**: [249. 레거시 설계 부채와 ADR (Legacy Design Debt & Architecture Decision Record)](/knowledge-base/studynote/11_design_supervision/04_gof_behavioral/249_legacy_design_debt_adr/)
**다음**: [251. 시큐어 코딩 SQL/XSS/CSRF 진단 (Secure Coding SQL/XSS/CSRF Audit)](/knowledge-base/studynote/11_design_supervision/05_audit_deep_guide/251_secure_coding_sql_xss_csrf/) →

---
