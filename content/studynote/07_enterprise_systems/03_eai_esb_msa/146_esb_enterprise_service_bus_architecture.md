---
title: 146. ESB (Enterprise Service Bus) - 엔터프라이즈 서비스 버스
date: '2026-04-19'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ESB는 **[[152_hub_dummy_switching_intelligent|Hub]]-and-Spoke의 Hub를 [[136_variance|분산]] [[389_mesh_topology|메시]]징 [[344_bus|버스]]로 확장**한 통합 미들웨어이며, [[389_mesh_topology|메시]]지 변환·[[339_routing_overview_best_path_selection|라우팅]]·[[073_container_orchestration_tools|오케스트레이션]]·[[295_protocol_field_tcp_udp_icmp|프로토콜]] 중재·보안을 **표준화된 [[344_bus|버스]] 인프라**에서 수행한다.
> 2. **가치**: Hub의 [[454_spof|SPOF]] 문제를 **[[136_variance|분산]] [[344_bus|버스]]**로 해결하고, [[618_soa_hardware|SOA]]([[618_soa_hardware|Service Oriented Architecture]])의 **[[090_service_kubernetes_network_load_balancing|서비스]] 연결 백본**으로 기능하며, [[152_wsdl_web_services_description_language|WSDL]]·[[153_soap_simple_object_access_protocol|SOAP]]·XML 기반 표준 통합을 제공한다.
> 3. **판단 포인트**: MuleSoft·TIBCO·IBM Integration Bus가 대표이며, [[619_msa_traffic_hardware|MSA]] 시대에는 **ESB의 무거운 중앙 집중이 [[128_water_scrum_fall_anti_pattern|안티패턴]]**으로 간주되어 [[179_kafka_flink_watermark_time_window|Kafka]]·이벤트 기반으로 전환 중이다.

---

## Ⅰ. 개요 및 필요성

```text
ESB 핵심 기능:
  메시지 변환: XML↔JSON, SOAP↔REST
  라우팅: 콘텐츠 기반·규칙 기반
  오케스트레이션: BPEL 워크플로
  프로토콜 중재: HTTP·MQ·FTP·JDBC
```

- **📢 섹션 요약 비유**: ESB는 **고속도로 인터체인지**이다. 다양한 방향([[295_protocol_field_tcp_udp_icmp|프로토콜]])의 차량([[389_mesh_topology|메시]]지)을 자동으로 안내한다.

---

## Ⅱ~Ⅴ. 결론

ESB는 **[[618_soa_hardware|SOA]] 시대의 통합 표준**이지만, MSA에서는 [[179_kafka_flink_watermark_time_window|Kafka]]·이벤트 기반이 주류이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **ESB** | [[136_variance|분산]] [[090_service_kubernetes_network_load_balancing|서비스]] [[344_bus|버스]] |
| **[[618_soa_hardware|SOA]]** | [[212_soa_service_oriented_architecture_esb|서비스 지향 아키텍처]] |
| **MuleSoft** | 대표 ESB |
| **[[153_soap_simple_object_access_protocol|SOAP]]/[[152_wsdl_web_services_description_language|WSDL]]** | 표준 [[295_protocol_field_tcp_udp_icmp|프로토콜]] |
| **[[179_kafka_flink_watermark_time_window|Kafka]]** | [[619_msa_traffic_hardware|MSA]] 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Hub-and-Spoke (2000s)] → [ESB (TIBCO·MuleSoft, 2005~)]
    → [SOA + ESB (전성기, 2008~)]
    → [MSA + Kafka (ESB 대체, 2015~)]
    → [현재: iPaaS — 클라우드 통합 플랫폼]
```

### 👶 어린이를 위한 3줄 비유 설명
1. ESB는 **고속도로 인터체인지**예요. 여러 방향의 차를 **자동 안내**해요.
2. 서울→부산, 대전→광주 차들이 **인터체인지에서 방향**을 바꿔요.
3. 하지만 너무 **복잡해져서** 요즘은 [[179_kafka_flink_watermark_time_window|Kafka]](우편함)로 바꾸고 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 146 / 482

← **이전**: [[145_message_broker_sync_async|145. 메시지 브로커 (Message Broker) - 동기·비동기 통합]]
**다음**: [[147_data_application_process_integration_etl_api_bpm|147. 데이터·애플리케이션·프로세스 통합 (ETL / API / BPM)]] →

---
