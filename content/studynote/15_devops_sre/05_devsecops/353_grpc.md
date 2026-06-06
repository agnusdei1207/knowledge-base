---
title: "gRPC and Protocol Buffers"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: gRPC는 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 위에서 동작하는 고성능 [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/)([Remote Procedure Call](/studynote/02_operating_system/02_process_thread/126_rpc/)) 프레임워크이며, [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) Buffers는 그 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 계약과 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 형식을 담당한다.
> 2. **가치**: [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 간 내부 통신에서 강한 타입 계약, 양방향 스트리밍, 낮은 오버헤드를 제공해 REST보다 효율적인 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출 구조를 만들 수 있다.
> 3. **판단 포인트**: gRPC는 빠르다고 무조건 쓰는 기술이 아니라, 브라우저 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/), 외부 공개 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 요구, 디버깅 편의, 계약 진화 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 함께 고려해 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

[마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)가 늘어나면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출 횟수와 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 변환 비용이 빠르게 증가한다. [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) 기반 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/) API는 인간이 읽기 쉽고 개방적이지만, 내부 동서(East-West) 트래픽이 많아질수록 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 비용과 계약 불일치 문제가 커질 수 있다. 특히 실시간 스트리밍이나 고빈도 호출이 많은 환경에서는 더 효율적인 통신 방식이 필요하다.

gRPC는 이런 요구에 맞춰 [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) 스타일 호출과 [Protocol Buffers](/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) 기반 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 계약을 제공한다. 개발자는 `.proto` [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지를 정의하고, 각 언어의 [스텁](/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/) 코드를 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)해 일관된 인터페이스를 유지할 수 있다. 따라서 gRPC의 필요성은 단순 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상보다도 “내부 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 계약을 엄격히 관리하면서 빠르게 통신하는 것”에 있다.

- **📢 섹션 요약 비유**: 자유롭게 적는 메모 대신, 모두가 같은 양식의 주문서를 써서 주방과 홀 사이 오해를 줄이는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

gRPC는 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2의 멀티플렉싱, 헤더 [압축](/studynote/02_operating_system/06_memory_management/347_compaction/), 스트리밍 특성을 활용한다. [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) Buffers는 필드 번호 기반의 이진 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화를 사용해 JSON보다 작은 페이로드와 빠른 파싱을 제공한다. [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 호출은 unary, server streaming, [client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) streaming, bidirectional streaming 형태로 확장된다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| `.proto` 계약 | [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지와 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 정의 | backward [compatibility](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/), field numbering |
| [Stub](/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/) / Codegen | 클라이언트·서버 코드 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 언어 간 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) |
| [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 Transport | 고속 전송 계층 | [multiplexing](/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/), streaming |
| [Observability](/studynote/01_computer_architecture/15_advanced_topics/642_observability_telemetry/) | 추적과 오류 분석 | interceptors, trace [context](/studynote/02_operating_system/01_overview_architecture/033_context/) |

```text
+--------------+   proto      +--------------+   codegen    +--------------+
| API Contract | ------------> | Client Stub  | ------------> | Service Call |
+--------------+              +--------------+              +--------------+
        |                              |                             |
        | versioning                   | HTTP/2 stream               | trace
        v                              v                             v
+--------------+              +--------------+              +--------------+
| Message Types| <------------> | Server Stub  | <------------> | Observability|
+--------------+              +--------------+              +--------------+
```

핵심 원리는 계약 우선(Contract-first)과 이진 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화다. 필드 번호를 바꾸지 않고 새 필드를 추가하는 방식으로 하위 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)을 유지해야 하며, 언어별 [스텁](/studynote/04_software_engineering/11_testing_validation/852_stub_test_double/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)을 배포 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인에 녹여야 한다. 내부망에서는 gRPC가 강력하지만, 브라우저 직접 호출이나 외부 파트너 연동은 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)/GraphQL이 더 적합할 수 있다.

- **📢 섹션 요약 비유**: 모두가 같은 악보를 보고 연주하면 합주가 빨라지지만, 관객에게는 악보보다 친절한 설명이 더 필요할 때가 있는 것과 같다.

---

## Ⅲ. 비교 및 연결

gRPC는 REST와 GraphQL과 자주 비교된다. REST는 개방성과 이해 용이성이 좋고, GraphQL은 유연한 조회가 강점이며, gRPC는 내부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 계약 엄격성이 장점이다.

| 방식 | 강점 | 한계 |
| :--- | :--- | :--- |
| [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)/[JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) | 범용성, 디버깅 편의, 브라우저 친화 | 오버헤드, 계약 약화 가능 |
| [GraphQL](/studynote/06_ict_convergence/03_cloud_infrastructure/246_graphql_query_language_overfetching_solution/) | 클라이언트 중심 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 선택 | 복잡한 운영/캐시 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) | [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 타입 안정성, 스트리밍 | 브라우저 직접 사용 제약, 학습 곡선 |

또한 gRPC는 [Service Mesh](/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/), [OpenTelemetry](/studynote/15_devops_sre/03_sre_observability/146_opentelemetry_otel_observability_standard/), [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/), protobuf [schema](/studynote/05_database/04_transactions_concurrency/505_schema/) registry와도 연결된다. 내부 통신을 gRPC로 표준화하더라도 외부 공개 API는 REST로 제공하는 혼합 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이 일반적이다.

- **📢 섹션 요약 비유**: 사내 전용 엘리베이터는 빠르고 효율적이지만, 방문객을 위한 안내 데스크까지 대체하지는 못하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 호출량이 많고 계약 변화가 잦은 내부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에 gRPC가 잘 맞는다. 반면 모바일 브라우저나 외부 파트너가 직접 호출하는 API는 REST가 더 현실적일 수 있다. 또한 gRPC는 바이너리 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이므로 로깅, 디버깅, [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/) 배포, 인터셉터 기반 추적을 같이 갖추지 않으면 운영 난도가 올라간다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 내부 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출 빈도와 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간 요구가 [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 도입을 정당화하는가?
2. `.proto` [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)의 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 규칙과 코드 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인이 마련되어 있는가?
3. [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 추적, 재시도, [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 인터셉터/[프록시](/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)로 표준화되어 있는가?
4. 외부 공개 API와 내부 [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) API의 경계를 명확히 구분했는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 외부 웹 브라우저 API까지 무리하게 gRPC로 통일하려는 경우
- 필드 번호와 reserved [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 없이 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/)를 자주 깨뜨리는 경우
- [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 장점만 보고 observability와 debugging 체계를 준비하지 않는 경우

기술사 답안에서는 gRPC를 “내부 고성능 계약형 통신”으로 정의하고, REST와의 역할 분담을 설명하면 좋다.

- **📢 섹션 요약 비유**: 빠른 고속열차를 만들었어도, 표지판과 시간표가 없으면 승객은 오히려 더 헤매게 된다.

---

## Ⅴ. 기대효과 및 결론

gRPC를 적절히 적용하면 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 호출 효율과 계약 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 크게 높일 수 있다. 특히 대규모 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/), 실시간 스트리밍, 다중 언어 환경에서 생산성과 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 동시에 얻기 쉽다.

다만 모든 API를 gRPC로 몰아가면 [접근성](/studynote/04_software_engineering/05_devops_ci_cd/292_accessibility_kwcag_wcag/)과 운영 편의가 희생될 수 있다. 따라서 기억해야 할 핵심은 “내부 고성능 통신에는 [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/), 외부 개방성과 단순성에는 [REST](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/)/기타 방식”이라는 역할 분담이다.

- **📢 섹션 요약 비유**: 빠른 전용도로는 화물 운송에 좋지만, 동네 골목길까지 모두 고속도로로 만들 필요는 없는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [Protocol Buffers](/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/) | [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) [메시](/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/)지 계약과 이진 [직렬](/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)화 |
| [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 | 스트리밍과 멀티플렉싱 기반 전송 계층 |
| Interceptor | [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 추적, 로깅을 공통화하는 지점 |
| [Service Mesh](/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/) | [gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) 트래픽 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 관측을 지원 |

### 📈 관련 키워드 및 발전 흐름도

```text
REST/JSON APIs
   |
   v
Contract-first Schema
   |
   v
gRPC + Protocol Buffers
   |
   v
Streaming / Service Mesh / OpenTelemetry Integration
```

이 흐름은 “개방형 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) -> 계약 명세 강화 -> 고성능 [RPC](/studynote/02_operating_system/02_process_thread/126_rpc/) -> 운영 통합”으로 내부 통신이 성숙하는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. gRPC는 친구들끼리 약속된 비밀 양식으로 아주 빠르게 편지를 주고받는 방법이에요.
2. 모두 같은 양식을 쓰니 오해가 적고 빨라요.
3. 하지만 처음 보는 손님에게는 쉬운 말로 적힌 안내문이 더 필요할 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 353 / 373

<- **이전**: [352. 동형 암호 데이터 프라이버시 클린 룸 (Homomorphic Encryption)](/studynote/12_it_management/05_security_compliance/993_process/)
**다음**: [354. 마이크로 프론트엔드 UI 컴포넌트 독립 배포망 (Micro Frontend)](/studynote/13_cloud_architecture/05_data_engineering/354_process/) ->

---
