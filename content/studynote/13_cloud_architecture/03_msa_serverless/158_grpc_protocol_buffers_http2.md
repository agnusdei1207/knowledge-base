---
title: "158. gRPC와 프로토콜 버퍼 (gRPC / Protocol Buffers / HTTP2)"
date: "2026-04-21"
tags:
  - "studynote-cloud-architecture"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) (Google [Remote Procedure Call](/studynote/02_operating_system/02_process_thread/126_rpc/))는 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 위에서 [Protocol Buffers](/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) (바이너리 직렬화)를 사용해 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 간 내부 동기 통신을 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)/JSON보다 최대 5~10배 빠르게 처리하는 고성능 [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) 프레임워크다.
> 2. **가치**: 강타입 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)(`.proto` [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)), 다국어 클라이언트 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 양방향 스트리밍 지원으로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 계약을 명확히 하고 개발 생산성을 높인다.
> 3. **판단 포인트**: [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 내부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신에는 gRPC가 최적이나, 브라우저 직접 호출은 [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)-Web 레이어가 필요하고 디버깅이 REST보다 어려워 외부 API에는 여전히 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)/GraphQL이 적합하다.

---

## Ⅰ. 개요 및 필요성

[MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 환경에서 수백 개의 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)가 서로 빈번하게 호출할 때 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1 + [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 방식의 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API는 두 가지 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목을 만든다. 첫째, [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 직렬화·역직렬화 비용이 크다. 둘째, [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1은 요청당 커넥션을 새로 맺거나 Keep-Alive에 의존해 헤더 오버헤드가 크다.

[gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) (Google [Remote Procedure Call](/studynote/02_operating_system/02_process_thread/126_rpc/))는 이 문제를 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 + [Protocol Buffers](/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) ([프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 버퍼) 조합으로 해결한다. [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) Buffers는 [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 대비 3~10배 작은 바이너리 포맷으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 직렬화하며, [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2는 단일 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 연결 위에서 [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)([Multiplexing](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/))·헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)·서버 푸시를 지원한다.

원래 Google이 내부적으로 수십억 건의 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출을 처리하기 위해 개발했으며, 현재는 [CNCF](/studynote/15_devops_sre/04_iac_cloud_native/190_cncf_landscape_observability/) ([Cloud Native](/studynote/06_ict_convergence/03_cloud_infrastructure/199_cloud_native_architecture_msa_cicd_devops/) Computing Foundation) [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 프로젝트로 공개되어 있다. Go, Java, Python, C++, Node.js 등 10개 이상의 언어를 지원한다.

📢 **섹션 요약 비유**: gRPC는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 전용 고속도로 — [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)/JSON이 일반 도로라면, gRPC는 체증 없이 고속으로 달리는 전용 차선이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

| 항목 | [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)/[JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) | [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)/Protobuf |
|:---|:---|:---|
| 전송 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1 | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 포맷 | [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) (텍스트) | [Protocol Buffers](/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) (바이너리) |
| [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 크기 | 100% 기준 | 약 30~50% 수준 |
| 직렬화 속도 | 느림 | 약 5~10배 빠름 |
| [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) | 없음 (문서 의존) | `.proto` 강타입 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) |
| 스트리밍 | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) ([HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2에서 가능) | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/)·서버->클라·양방향 |
| 브라우저 지원 | 직접 | [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)-Web 레이어 필요 |
| 코드 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 없음 (OpenAPI 도구) | `.proto` -> 다국어 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |

```text
+--------------------------------------------------------------------+
|                    gRPC 통신 구조                                  |
|                                                                    |
|  .proto 파일 정의:                                                 |
|  service OrderService {                                            |
|    rpc GetOrder (OrderRequest) returns (OrderResponse);            |
|    rpc StreamOrders (Empty) returns (stream OrderResponse);        |
|  }                                                                 |
|                                                                    |
|  +------------------+          +------------------------------+   |
|  |   gRPC 클라이언트 |          |      gRPC 서버               |   |
|  |                  |          |                              |   |
|  |  Stub (자동생성) |-HTTP/2--►|  Handler                    |   |
|  |  GetOrder(req)   |◄---------|  ProcessOrder(req, res)     |   |
|  |  [Protobuf 직렬화| 바이너리  |  [Protobuf 역직렬화]        |   |
|  +------------------+          +------------------------------+   |
|                                                                    |
|  HTTP/2 멀티플렉싱:                                                |
|  +-----------------------------------------------------------+    |
|  |  단일 TCP 연결                                            |    |
|  |  Stream 1: 주문 조회 ------------------------------►     |    |
|  |  Stream 2: 재고 확인 -------------------------------►    |    |
|  |  Stream 3: 배송 조회 --------------------------------►   |    |
|  +-----------------------------------------------------------+    |
+--------------------------------------------------------------------+
```

📢 **섹션 요약 비유**: [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) Buffers는 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(.zip) — 같은 내용이지만 텍스트([JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)) 대신 바이너리로 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/)해 전송하므로 용량이 훨씬 작고 빠르다.

---

## Ⅲ. 비교 및 연결

| 구분 | Unary [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) | Server Streaming | [Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) Streaming | Bidirectional |
|:---|:---|:---|:---|:---|
| 방향 | 요청 1 -> 응답 1 | 요청 1 -> 응답 N개 스트림 | 요청 N개 -> 응답 1 | 양방향 스트림 |
| 사용 예 | 일반 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 조회 | 실시간 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)/이벤트 구독 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 업로드 청크 | 채팅, 실시간 게임 |
| [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1 대응 | [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) | [SSE](/studynote/03_network/09_application_layer_web_email/481_sse_server_sent_events/) ([Server-Sent Events](/studynote/03_network/09_application_layer_web_email/481_sse_server_sent_events/)) | FormData POST | [WebSocket](/studynote/03_network/09_application_layer_web_email/480_websocket_full_duplex/) |

gRPC의 4가지 통신 패턴은 REST가 Unary에만 자연스럽게 맞는 것과 달리, 스트리밍 워크로드까지 네이티브로 지원한다.

📢 **섹션 요약 비유**: [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 양방향 스트리밍은 전화 통화 — REST가 문자 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지(요청-응답 1:1)라면, [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 양방향은 실시간 대화처럼 양쪽이 동시에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**내부/외부 통신 기술 선택 기준**
- [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 내부 동기 통신 -> [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) ([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)·타입 안전성)
- 외부 공개 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) (파트너·모바일) -> [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) 또는 [GraphQL](/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/)
- 실시간 스트리밍 ([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/), 실시간 대시보드) -> [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) Bidirectional Streaming
- 브라우저 직접 호출 -> [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)-Web 또는 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)

<strong><a href="/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/">gRPC</a> 도입 시 고려사항</strong>
1. `.proto` [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [버전](/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 -> [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) [레지스트리](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) (Buf [Schema](/studynote/05_database/04_transactions_concurrency/505_schema/) [Registry](/studynote/15_devops_sre/05_devsecops/235_registry_immutable_tag/) 등)
2. [Load Balancer](/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/) [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) -> L7 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 지원 여부 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) (AWS ALB 지원)
3. [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) ([Istio](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/), Linkerd) 연동 -> 자동 [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) + 트래픽 관리
4. 디버깅 도구 -> [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 클라이언트(grpcurl), [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) UI 활용

📢 **섹션 요약 비유**: `.proto` [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 공동 작업 계약서 — 모든 팀이 서명한 계약서([스키마](/studynote/05_database/01_db_architecture_relational/005_schema/))에 따라 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지를 주고받으므로 오해(타입 불일치)가 없다.

---

## Ⅴ. 기대효과 및 결론

gRPC는 [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 내부 통신의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제를 원천적으로 해결하는 강력한 도구다. 특히 수십~수백 개의 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)가 초당 수만 건의 RPC를 주고받는 대규모 시스템에서 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) 대비 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 감소·[처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 향상 효과가 명확하다.

한계로는 바이너리 포맷 특성상 Wireshark 등 네트워크 디버깅 도구로 직접 내용을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하기 어렵고, REST에 비해 학습 곡선이 가파르다. 그러나 `.proto` 기반 강타입 계약과 다국어 코드 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)은 팀이 성장할수록 장기적으로 더 큰 생산성 이점을 제공한다.

📢 **섹션 요약 비유**: gRPC는 표준화된 철도 레일 — 처음 레일 놓는 비용(학습 곡선)이 있지만, 한 번 설치되면 어느 열차(언어)도 동일한 속도로 달릴 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 연결 포인트 |
|:---|:---|
| [Protocol Buffers](/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) (Protobuf) | gRPC의 바이너리 직렬화 포맷 |
| [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 | gRPC의 전송 레이어, [다중화](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)·헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/) |
| [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) ([Service Mesh](/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/)) | [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 트래픽을 [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/)·관찰로 관리 |
| [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)-Web | 브라우저에서 [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 사용을 가능하게 하는 레이어 |
| [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) ([Representational State Transfer](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/)) | 외부 API에서 gRPC와 공존 |
| OpenAPI / Swagger | REST용 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 명세, gRPC의 `.proto`와 대응 |

### 👶 어린이를 위한 3줄 비유 설명
1. [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)/JSON은 한글로 편지 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) — 사람이 읽기 쉽지만 길고 느려요.

### 📈 관련 키워드 및 발전 흐름도

```text
REST/JSON (텍스트 기반, 사람 친화)
    |
    v
gRPC: Protocol Buffers + HTTP/2
    +-► 바이너리 직렬화: 10x 빠름, 70% 작은 페이로드
    +-► 스트리밍: Unary · Server · Client · Bidirectional
    +-► IDL 기반 코드 생성: 타입 안전
    |
    v
내부 MSA 통신: gRPC | 외부 API: REST · GraphQL
```
2. [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)/Protobuf는 모스 부호로 통신하기 — 사람은 바로 못 읽지만 훨씬 짧고 빠르게 전달돼요.
3. 두 컴퓨터([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))가 초고속으로 대화해야 할 때는 사람이 읽을 필요가 없으니 모스 부호([gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/))가 훨씬 유리해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 157 / 371

<- **이전**: [157. BFF / GraphQL API 집계 (BFF Pattern / GraphQL)](/studynote/13_cloud_architecture/03_msa_serverless/157_bdi_graphql_api_aggregation/)
**다음**: [159. 결과적 일관성 (Eventual Consistency)](/studynote/13_cloud_architecture/03_msa_serverless/159_eventual_consistency_distributed_systems/) ->

---
