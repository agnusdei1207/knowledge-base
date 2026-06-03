+++
title = "123. OCF (Open Connectivity Foundation) - IoT 상호운용성 표준"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: OCF는 <strong>이기종 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 디바이스 간 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/">상호운용성</a>(<a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/084_blockchain_interoperability_polkadot_cosmos/">Interoperability</a>)을 보장</strong>하는 개방형 표준으로, 제조사·[프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)에 관계없이 디바이스가 <strong>자동 발견(Discovery)·통신·보안 연결</strong>될 수 있도록 한다.
> 2. **가치**: [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 디바이스가 제조사마다 독자 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 사용하면 "삼성 냉장고↔LG 에어컨" 연동이 불가능하지만, OCF 표준을 따르면 <strong>브랜드 무관하게 자동 연동</strong>된다.
> 3. **판단 포인트**: OCF는 <strong>IoTivity(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/">오픈소스</a> 구현체)</strong>를 제공하며, [Matter](/knowledge-base/studynote/03_network/12_iot_wpan_edge/612_matter_csa_smart_home_standard/)(2022)와 함께 <strong>스마트 홈 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/">상호운용성</a> 표준 생태계</strong>를 형성한다.

---

## Ⅰ. 개요 및 필요성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">OCF 프레임워크</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">응용 계층</div><div class="kb-diagram-note">— 스마트홈·헬스케어·산업 IoT 앱</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">OCF 서비스 계층</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">디바이스 발견·리소스 관리·보안·데이터 모델</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">전송 계층</div><div class="kb-diagram-note">— CoAP / HTTP / WebSocket</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">네트워크</div><div class="kb-diagram-note">— Wi-Fi / BLE / Thread / Zigbee</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">핵심: 이기종 디바이스 자동 발견 + 표준 데이터 모델</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: OCF는 IoT의 <strong><a href="/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/">USB</a> 표준</strong>이다. [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) 이전에는 프린터마다 다른 케이블이 필요했지만, USB로 통일되면서 아무 프린터나 연결할 수 있게 되었다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### OCF vs [Matter](/knowledge-base/studynote/03_network/12_iot_wpan_edge/612_matter_csa_smart_home_standard/)

| 비교 | OCF | [Matter](/knowledge-base/studynote/03_network/12_iot_wpan_edge/612_matter_csa_smart_home_standard/) |
|:---|:---|:---|
| **범위** | 범용 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) | **스마트 홈 특화** |
| **전송** | [CoAP](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/)/[HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) | [Thread](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/)/Wi-Fi |
| **구현체** | IoTivity | connectedhomeip |
| **지원** | 삼성·Intel | **Apple·Google·Amazon** |

- **📢 섹션 요약 비유**: OCF는 범용 전원 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/), Matter는 스마트홈 전용 [어댑터](/knowledge-base/studynote/04_software_engineering/04_testing_quality/259_adapter_pattern_interface_wrapper/)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | OCF | oneM2M | [Matter](/knowledge-base/studynote/03_network/12_iot_wpan_edge/612_matter_csa_smart_home_standard/) |
|:---|:---|:---|:---|
| **초점** | 디바이스 연동 | **플랫폼** | 스마트 홈 |
| **계층** | 디바이스 | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 디바이스 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### IoTivity
- Linux Foundation [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 프로젝트.
- OCF 스펙의 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 구현체.
- C/C++ 기반, 경량 디바이스 지원.

---

## Ⅴ. 기대효과 및 결론

OCF는 <strong>이기종 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/">상호운용성</a>의 기술 표준</strong>이며, Matter와 함께 스마트 홈·산업 IoT의 표준 생태계를 형성하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **IoTivity** | OCF의 [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 구현체 |
| <strong><a href="/knowledge-base/studynote/03_network/12_iot_wpan_edge/612_matter_csa_smart_home_standard/">Matter</a></strong> | 스마트 홈 [상호운용성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/287_interoperability_tactics/) 표준 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/120_coap_constrained_application_protocol/">CoAP</a></strong> | OCF의 기본 전송 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| **oneM2M** | [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 플랫폼 표준 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/">Thread</a></strong> | 저전력 [메시](/knowledge-base/studynote/01_computer_architecture/10_parallel_processing_architecture/389_mesh_topology/) 네트워크 ([Matter](/knowledge-base/studynote/03_network/12_iot_wpan_edge/612_matter_csa_smart_home_standard/) 전송) |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">독자 IoT 프로토콜 (사일로, 2010s)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">OIC → OCF (2014~2016) — 상호운용성 표준</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">IoTivity 오픈소스 (2015~)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Matter (2022) — 스마트 홈 통합 표준</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재: OCF + Matter + Thread — IoT 표준 생태계</div></div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명
1. OCF는 IoT의 <strong><a href="/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/">USB</a> 표준</strong>이에요. 어떤 회사 제품이든 <strong>같은 규격으로 연결</strong>돼요.
2. [USB](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) 이전에는 프린터마다 <strong>다른 케이블</strong>이 필요했지만, USB로 통일되면서 편리해졌어요.
3. 삼성 냉장고와 LG 에어컨도 OCF를 따르면 <strong>서로 대화</strong>할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 123 / 552

← **이전**: [122. oneM2M IoT 표준 - 글로벌 IoT 서비스 플랫폼 표준 아키텍처](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/122_onem2m_iot_standard/)
**다음**: [124. IoT 봇넷 & Mirai - IoT 디바이스 대상 DDoS 봇넷 공격](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/124_iot_botnet_mirai/) →

---
