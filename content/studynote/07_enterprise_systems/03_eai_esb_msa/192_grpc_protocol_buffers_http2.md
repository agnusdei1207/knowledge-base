---
title: "Grpc Protocol Buffers Http2"
date: "2026-05-08"
tags:
  - "studynote-enterprise-systems"
weight: 192
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) (Google [Remote Procedure Call](/studynote/02_operating_system/02_process_thread/126_rpc/))은 `.proto` 계약서를 기준으로 클라이언트와 서버 코드를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, [Protocol Buffers](/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) 바이너리 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지를 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 위에서 주고받는 고성능 원격 호출 프레임워크다.
> 2. **가치**: 내부 [마이크로서비스 아키텍처](/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/) ([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/), [Microservices Architecture](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/))에서 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) (JavaScript Object Notation) 기반 REST보다 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 크기와 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 비용을 줄여, 낮은 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 높은 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)을 동시에 노릴 수 있다.
> 3. **판단 포인트**: gRPC는 "모든 API의 정답"이 아니라, 강한 계약·다중 언어 코드 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·스트리밍이 중요한 내부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신에서 특히 강하고, 공개 API나 브라우저 친화성은 별도 보완이 필요하다.

---

## Ⅰ. 개요 및 필요성

gRPC는 네트워크 너머의 함수를 로컬 메서드처럼 호출하게 해 주는 [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) ([Remote Procedure Call](/studynote/02_operating_system/02_process_thread/126_rpc/)) 계열 기술을 현대적인 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 환경에 맞게 정교화한 방식이다. 핵심은 "어떤 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지를 어떤 형식으로 주고받는가"를 먼저 계약으로 고정하고, 그 계약을 바탕으로 통신 코드를 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다는 점이다. 그래서 gRPC는 단순 전송 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이 아니라 <strong>계약 중심 통신 체계</strong>로 이해해야 한다.

이 방식이 필요해진 이유는 내부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 호출량이 폭증했기 때문이다. 전자상거래나 금융 플랫폼에서는 주문, 결제, 재고, 추천 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 요청 하나를 처리하는 동안 서로 수십 번씩 호출한다. 이때 텍스트 기반 JSON과 반복적인 파싱 비용이 누적되면 p95 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 CPU 사용량이 빠르게 증가하고, 언어가 다른 팀끼리 DTO ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Transfer Object) 정의가 어긋나며 통합 비용도 커진다.

특히 gRPC는 사람이 읽기 쉬운 문서보다 <strong>기계가 일관되게 이해할 수 있는 계약</strong>을 우선한다. 그래서 외부 공개용 API보다 백엔드 간 동기 호출, 실시간 스트리밍, 다중 언어 SDK [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)이 중요한 환경에서 더 큰 의미를 가진다.

- **📢 섹션 요약 비유**: gRPC는 사내 메신저에 자유 형식으로 글을 남기는 방식이 아니라, 모든 부서가 같은 양식의 바코드 운송장을 붙여 자동 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)기에 바로 태우는 내부 물류 체계와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

gRPC의 출발점은 인터페이스 정의 언어 (IDL, Interface Definition Language) 역할을 하는 `.proto` [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이다. 개발자는 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 구조와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 메서드를 정의하고, 컴파일러가 각 언어용 [스텁](/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/) ([Stub](/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/)) 코드를 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다. 호출 시 클라이언트 [스텁](/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/)은 객체를 [Protocol Buffers](/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) 형식으로 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화하고, [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 스트림에 실어 보내며, 서버 [스텁](/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/)은 이를 역직렬화해 실제 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구현체에 전달한다.

아래 표는 gRPC가 제공하는 대표 호출 방식을 보여준다.

| 호출 방식 | 요청/응답 형태 | 적합한 사례 | 설계 포인트 |
| :--- | :--- | :--- | :--- |
| Unary | 요청 1건 / 응답 1건 | 회원 조회, 결제 승인 | 가장 단순하며 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) 대체에 적합 |
| Server Streaming | 요청 1건 / 응답 다건 | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) tail, 실시간 시세 구독 | 수신 측 처리 속도와 backpressure 고려 |
| [Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) Streaming | 요청 다건 / 응답 1건 | 센서 업로드, 대량 이벤트 적재 | 전송 완료 시점과 버퍼 관리 중요 |
| Bidirectional Streaming | 요청 다건 / 응답 다건 | 채팅, 협업 편집, 실시간 제어 | 연결 유지, 순서, 취소 전파 설계 필요 |

이 그림은 gRPC가 계약에서 실행까지 어떻게 이어지는지 보여준다.

```text
+----------------------------------------------------------------------+
| gRPC 호출 경로: 계약 -> 스텁 -> 바이너리 스트림 -> 서비스          |
+----------------------------------------------------------------------+
| Client App                                                          |
|    |                                                                |
|    v                                                                |
| Client Stub -> Protobuf -> HTTP/2 Stream -> Server Stub -> Service  |
|    ^                                                     |          |
|    +------------ Response Metadata <- Protobuf <- Result +          |
+----------------------------------------------------------------------+
```

[HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2는 하나의 연결에서 여러 스트림을 멀티플렉싱하고, 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)과 [흐름 제어](/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/)를 제공한다. 여기에 [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) Buffers의 태그 기반 바이너리 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화가 결합되면, 동일한 의미의 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지를 더 작은 크기와 더 적은 CPU 비용으로 전달할 수 있다. 또한 [deadline](/studynote/02_operating_system/11_exam_summary/766_realtime_scheduling_deadline/), status [code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), [metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/), interceptor 같은 메커니즘이 함께 제공되어 단순 속도뿐 아니라 운영 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)도 확보한다.

- **📢 섹션 요약 비유**: gRPC는 택배를 보낼 때 내용물을 자유롭게 적는 종이 메모가 아니라, 규격 상자와 자동 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 라인을 함께 쓰는 고속 물류센터와 같다. 상자가 규격화되어 있어야 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)기와 배송차가 빠르게 움직인다.

---

## Ⅲ. 비교 및 연결

gRPC를 이해하려면 [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) ([Representational State Transfer](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) [Application Programming Interface](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))와 [메시지 브로커](/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/) 기반 비동기 연동을 함께 봐야 한다. gRPC는 동기 호출의 응답성, [메시지 브로커](/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/)는 시간적 분리, REST는 범용성과 가시성에 강하다. 결국 어떤 통신을 택할지는 "누가 소비하는가"와 "응답이 즉시 필요한가"에 달려 있다.

| 항목 | [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) | [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) | [메시지 브로커](/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/) 기반 이벤트 |
| :--- | :--- | :--- | :--- |
| 통신 성격 | 동기 [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) 중심 | 동기 요청/응답 중심 | 비동기 발행/구독 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형식 | [Protocol Buffers](/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) | 주로 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) | [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/), Avro, Protobuf 등 다양 |
| 장점 | 저지연, 강한 타입, 코드 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 브라우저 친화성, 디버깅 용이 | [결합도](/studynote/04_software_engineering/04_testing_quality/195_coupling_levels/) 완화, 재시도·[버퍼링](/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/) 용이 |
| 약점 | 브라우저 제약, 사람이 읽기 어려움 | 오버헤드 큼, 계약 드리프트 가능 | 즉시 응답 부적합, 운영 복잡성 증가 |
| 대표 활용 | 내부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출 | 외부 공개 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [BFF](/studynote/04_software_engineering/11_testing_validation/935_bff_backend_for_frontend/) | 주문 이벤트, 비동기 후처리 |

연결 관점에서도 중요하다. gRPC는 [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) ([Service Mesh](/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/))와 결합하면 [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) (Mutual Transport Layer [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)), 재시도, 관측성을 인프라 계층으로 위임하기 쉽다. 반면 외부 클라이언트와 직접 연결할 때는 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) Gateway나 [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)-Web 같은 중간 계층이 필요해지며, 그 지점에서 OpenAPI 기반 REST와 혼합 운용되는 경우가 많다.

- **📢 섹션 요약 비유**: gRPC는 사내 전용 고속 직통전화이고, REST는 누구나 읽을 수 있는 안내 데스크이며, [메시지 브로커](/studynote/07_enterprise_systems/03_eai_esb_msa/145_message_broker_sync_async/)는 답장이 늦어도 되는 사내 우편함과 같다. 셋은 경쟁자라기보다 쓰임새가 다른 통신 채널이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "속도가 빠르다"보다 "어느 경계 안에서 표준으로 삼을 것인가"가 더 중요하다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출이 잦고, Java·Go·Python처럼 다중 언어가 공존하며, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)이 중요하다면 [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 채택 이점이 크다. 반대로 공개 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [CDN](/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) 캐시 활용, 브라우저 개발자 도구 중심 디버깅이 중요하다면 REST가 더 자연스럽다.

### 채택 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 내부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출량이 많아 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 파싱 비용과 네트워크 오버헤드가 병목인가?
2. `.proto` [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)를 중앙 거버넌스로 관리하고 하위 호환 규칙을 지킬 수 있는가?
3. [timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/) 대신 [deadline](/studynote/02_operating_system/11_exam_summary/766_realtime_scheduling_deadline/), retry, circuit breaker를 호출 규약으로 표준화했는가?
4. 필드 번호 재사용 금지, optional/oneof [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), 에러 코드 체계를 팀 공통 규칙으로 문서화했는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 공개 모바일/웹 API까지 무조건 [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 하나로 통일하려는 설계
- 장기 스트리밍을 쓰면서 keepalive, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 갱신, 취소 전파를 설계하지 않는 경우
- [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 없이 필드 삭제·번호 재사용을 반복하는 경우

따라서 기술사 관점의 답안은 "gRPC는 내부 MSA의 고성능 표준" 정도로 외우는 데서 끝나면 부족하다. <strong>어떤 경계는 <a href="/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/">gRPC</a>, 어떤 경계는 <a href="/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/">REST</a>, 어떤 경계는 비동기 이벤트</strong>로 나누는 계층적 통신 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)까지 제시해야 설계력이 드러난다.

- **📢 섹션 요약 비유**: [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 도입은 도시 전체 도로를 모두 고속도로로 바꾸는 일이 아니다. 물동량이 큰 산업 단지 사이에만 [전용선](/studynote/03_network/05_lan_wan_l2_devices/266_leased_line_basics_e1_t1_t3/) 도로를 깔아야 투자 대비 효과가 난다.

---

## Ⅴ. 기대효과 및 결론

gRPC를 잘 도입하면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출의 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 사용량을 줄이고, 코드 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)으로 클라이언트/서버 계약 불일치를 크게 줄일 수 있다. 스트리밍이 필요한 실시간 분석, 채팅, 대량 업로드 시나리오에서도 단일 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로 일관된 통신 모델을 확보할 수 있다. 즉 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)뿐 아니라 개발 생산성과 계약 안정성까지 함께 얻는다는 점이 핵심 효과다.

다만 전제조건도 분명하다. `.proto` [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 거버넌스, 관측성, 에러 표준화, 게이트웨이 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 없으면 gRPC는 단순히 "빠르지만 다루기 어려운 바이너리 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)"로 전락한다. 따라서 이 주제는 <strong>REST의 대체재</strong>가 아니라 <strong>내부 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 통신을 정형화하는 고속 계약 체계</strong>로 기억하는 것이 가장 정확하다.

- **📢 섹션 요약 비유**: gRPC는 손님이 보는 쇼윈도보다 창고와 공장을 잇는 자동 컨베이어 벨트에 가깝다. 보이지 않는 내부 동선을 정리할 때 가장 큰 힘을 발휘한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Protocol Buffers](/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) | [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화와 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 계약의 핵심 |
| [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 | 멀티플렉싱, 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/), 스트리밍을 제공하는 전송 기반 |
| [스텁](/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/) ([Stub](/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/)) | 원격 호출을 로컬 메서드처럼 보이게 하는 코드 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 결과물 |
| [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) | [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 트래픽의 보안·재시도·관측성을 인프라에서 보완 |
| [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)-Web | 브라우저 환경에서 gRPC를 우회적으로 사용하게 하는 호환 계층 |

### 📈 관련 키워드 및 발전 흐름도

```text
RPC (Remote Procedure Call)
    |
    v
`.proto` 계약 정의
    |
    v
Protocol Buffers 직렬화
    |
    v
HTTP/2 멀티플렉싱 · 스트리밍
    |
    v
서비스 메시 · 게이트웨이 혼합 운용
```

이 흐름은 "원격 호출 개념 -> 계약 정의 -> 고속 전송 -> 운영 계층 확장"으로 gRPC의 성숙 단계를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. gRPC는 컴퓨터 친구들끼리 같은 약속 종이를 보고 아주 짧은 암호말로 대화하는 방법이에요.
2. 그래서 길게 설명하지 않아도 빨리 알아듣고 바로 일을 할 수 있어요.
3. 하지만 처음 약속 종이를 잘 만들어 두지 않으면 모두가 헷갈릴 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 192 / 482

<- **이전**: [191. 컨슈머 그룹 (Consumer Group) - Kafka 파티션 병렬 처리와 부하 분산](/studynote/07_enterprise_systems/03_eai_esb_msa/191_consumer_group_kafka_partition_load_balancing/)
**다음**: [193. OpenAPI Specification - Swagger 기반 API 계약 표준](/studynote/07_enterprise_systems/03_eai_esb_msa/193_openapi_specification_swagger_api_design/) ->

---
