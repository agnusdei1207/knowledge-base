---
title: "123. Soa Vs Msa Comparison"
date: "2026-04-19"
tags:
  - "studynote-cloud-architecture"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/)([Service Oriented Architecture](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/))는 <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/">ESB</a>(<a href="/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/">Enterprise Service Bus</a>) 중심의 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 통합</strong>이고, MSA는 <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/">ESB</a> 없이 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>가 직접 경량 통신(<a href="/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/">REST</a>/<a href="/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/">gRPC</a>/이벤트)</strong>하는 경량 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 아키텍처이다.
> 2. **가치**: SOA의 ESB는 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 변환·라우팅을 중앙에서 처리하지만, <strong>ESB가 <a href="/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">SPOF</a>(<a href="/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">단일 장애점</a>)·병목</strong>이 되며, MSA는 ESB를 제거하고 <strong>스마트 엔드포인트·덤 <a href="/studynote/02_operating_system/02_process_thread/123_pipe/">파이프</a></strong> 원칙으로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자율성을 극대화했다.
> 3. **판단 포인트**: [SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/)->MSA는 "[ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/) 제거 + [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 세분화 + [DevOps](/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 문화"의 진화이며, [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 크기·거버넌스·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권에서 근본적 차이가 있다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    SOA vs MSA                                         |
+-------------------------------------------------------+
|  [SOA]                         [MSA]                  |
|  Service A --+                Service A <--> Service B  |
|  Service B --+-- ESB --       Service C <--> Service D  |
|  Service C --+   (중앙)       (직접 통신, ESB 없음)   |
|                                                       |
|  SOA: 중앙 ESB가 라우팅·변환                         |
|  MSA: 서비스가 직접 REST/gRPC/Kafka                  |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: SOA는 중앙 교환원([ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/))이 모든 전화를 연결하는 시스템이고, MSA는 참가자가 직접 전화하는 시스템이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/) vs [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 비교

| 비교 | [SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/) | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) |
|:---|:---|:---|
| **통합** | <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/">ESB</a> (중앙)</strong> | [API Gateway](/studynote/04_software_engineering/11_testing_validation/934_api_gateway/) + 직접 |
| <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 크기</strong> | 대형 | <strong>소형 (단일 <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a>)</strong> |
| **DB** | 공유 가능 | <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>별 독립</strong> |
| **거버넌스** | 중앙 | <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a></strong> |
| <strong><a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong> | [SOAP](/studynote/07_enterprise_systems/03_eai_esb_msa/153_soap_simple_object_access_protocol/)/XML | <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/">REST</a>/<a href="/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/">gRPC</a>/<a href="/studynote/11_design_supervision/06_exam_summary/343_json/">JSON</a></strong> |
| **배포** | 앱 서버 | <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a></strong> |

- **📢 섹션 요약 비유**: SOA는 대기업 본사(중앙 관리)이고, MSA는 프랜차이즈(각 지점 자율 운영)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 모놀리식 | [SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/) | [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) |
|:---|:---|:---|:---|
| **분리** | 없음 | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | <strong>마이크로 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong> |
| **통합** | 내부 호출 | [ESB](/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/) | **경량 통신** |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong> | 공유 DB | 공유 가능 | <strong><a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>별 DB</strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 선택 기준
- <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/">SOA</a></strong>: 레거시 시스템 통합, 이기종 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 변환 필요 시.
- <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a></strong>: [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/), 빠른 배포, 팀 자율성 필요 시.

---

## Ⅴ. 기대효과 및 결론

[SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/)->MSA는 <strong>"중앙 집중(<a href="/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/">ESB</a>) -> <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 자율(Smart Endpoints)"</strong>의 패러다임 전환이며, 현대 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 환경에서는 MSA가 표준이지만, 레거시 통합에는 [SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/) 접근이 여전히 유효하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/">ESB</a></strong> | SOA의 핵심 통합 미들웨어 |
| <strong><a href="/studynote/04_software_engineering/11_testing_validation/934_api_gateway/">API Gateway</a></strong> | MSA의 외부 진입점 |
| <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/153_soap_simple_object_access_protocol/">SOAP</a>/XML</strong> | SOA의 통신 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| <strong><a href="/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/">REST</a>/<a href="/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/">gRPC</a></strong> | MSA의 경량 통신 |
| <strong><a href="/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/">Service Mesh</a></strong> | MSA의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신 인프라 |

### 📈 관련 키워드 및 발전 흐름도

```text
[모놀리식 (전통)]
    |
    v
[SOA + ESB (2005~) — 서비스 지향, SOAP/XML]
    |
    v
[MSA (2014~) — ESB 제거, REST/gRPC, 컨테이너]
    |
    v
[Service Mesh (Istio, 2018~) — MSA 통신 인프라]
    |
    v
[현재: Modular Monolith — 상황별 최적 선택]
```

### 👶 어린이를 위한 3줄 비유 설명
1. SOA는 <strong>교환원(<a href="/studynote/07_enterprise_systems/03_eai_esb_msa/146_esb_enterprise_service_bus_architecture/">ESB</a>)</strong>이 모든 전화를 연결해주는 거예요. 교환원이 바쁘면 전화가 안 돼요.
2. MSA는 교환원 없이 <strong>직접 전화</strong>하는 거예요. 더 빠르지만 전화번호부([Service Discovery](/studynote/12_it_management/05_security_compliance/946_service_discovery/))가 필요해요.
3. 요즘은 <strong>직접 전화(<a href="/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a>)가 대세</strong>지만, 옛날 전화기(레거시)는 교환원([SOA](/studynote/01_computer_architecture/15_advanced_topics/618_soa_hardware/))이 필요할 때도 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 122 / 371

<- **이전**: [122. MSA (Microservices Architecture) - 서비스별 독립 배포·스케일링 아키텍처](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)
**다음**: [124. API Gateway - MSA 외부 진입점·라우팅·인증·Rate Limiting](/studynote/11_design_supervision/02_architecture_principles/124_api_gateway/) ->

---
