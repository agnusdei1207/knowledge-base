+++
title = "495. 5G 3대 특성과 네트워크 슬라이싱 (5G eMBB uRLLC mMTC Network Slicing)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 5G의 핵심 가치는 빠른 속도([eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/))만이 아니라, 1ms 초저지연([uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/))과 km^당 100만 기기 동시 접속([mMTC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/))이라는 서로 상충하는 세 가지 요구사항을 단일 물리망 위에서 [네트워크 슬라이싱](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)([Network Slicing](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/))으로 동시 충족하는 데 있다.
> 2. **가치**: [네트워크 슬라이싱](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)은 하나의 물리 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 인프라를 산업별 맞춤 가상망(NSI)으로 분리함으로써, 통신사는 B2B [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 산업 수요에 맞게 판매하고 기업은 전용 품질([SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/))을 보장받는다.
> 3. **판단 포인트**: [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/)([Standalone](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/)) 아키텍처는 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 코어([5GC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/))와 gNB가 완전 분리되어 [네트워크 슬라이싱](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)·[URLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/) 등 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 고유 기능을 완전히 지원한다. [NSA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/)(Non-[Standalone](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/))는 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 코어를 공유해 전환 비용은 낮지만 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 핵심 기능이 제한된다.

---

## Ⅰ. 개요 및 필요성

<strong><a href="/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> ITU-R IMT-2020 표준 3대 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a></strong>

| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 영문 | 핵심 지표 | 주요 사용처 |
|:---:|:---:|:---:|:---:|
| [eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/) | Enhanced Mobile Broadband | 최대 20Gbps | VR·AR·4K 스트리밍 |
| [uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/) | Ultra-Reliable Low-Latency | [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 1ms, [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 99.999% | 자율주행·원격 수술·공장 제어 |
| [mMTC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/) | massive Machine-Type Communication | 100만 기기/km^ | 스마트시티·스마트팜·미터링 |

<strong>4G(<a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/">LTE</a>) 한계와 <a href="/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> 등장</strong>: LTE는 단일 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)(단순 고속) 구조로 서로 다른 [QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 요구를 동시에 충족 불가. 5G는 [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)([NFV](/knowledge-base/studynote/03_network/17_sdn_nfv/865_nfv_network_functions_virtualization_architecture/))·소프트웨어 정의([SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)) 기반으로 유연한 다중 [QoS](/knowledge-base/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/) 관리를 실현한다.

- **📢 섹션 요약 비유**: 4G는 단일 도로, 5G는 세 개의 전용 차선이다. eMBB는 고속차선(빠른 차), uRLLC는 앰뷸런스 전용차선(항상 빈 길), mMTC는 오토바이 전용 넓은 갓길. 이 세 차선이 서로 침범하지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
+----------------------------------------------------------+
|           5G 네트워크 슬라이싱 아키텍처                    |
+----------------------------------------------------------+
|  [물리 인프라]  gNB(기지국) + 5G Core(5GC) 하드웨어        |
|        |                                                 |
|  [가상화 계층]  NFV(네트워크 기능 가상화) / SDN             |
|        |                                                 |
|  [슬라이스 관리]  NSSF(Network Slice Selection Function)  |
|  +-------------------------------------------------+    |
|  |  NSI-1 (eMBB 슬라이스)   | 넷플릭스·통신사 서비스  |    |
|  +-------------------------+----------------------+    |
|  |  NSI-2 (uRLLC 슬라이스) | 자율주행·원격 수술     |    |
|  +-------------------------+----------------------+    |
|  |  NSI-3 (mMTC 슬라이스)  | 스마트시티·IoT 센서    |    |
|  +-------------------------+----------------------+    |
|                                                          |
|  [SLA 보장]  각 슬라이스별 독립 QoS 보장                   |
+----------------------------------------------------------+
```

### [네트워크 슬라이싱](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/) 핵심 개념

| 개념 | 설명 |
|:---|:---|
| NSI(Network [Slice](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) Instance) | 특정 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 위해 생성된 독립 가상 네트워크 인스턴스 |
| NSSF(Network [Slice](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) [Selection](/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/) Function) | 단말 요청에 따라 적절한 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)를 선택·배정 |
| S-NSSAI | [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/). SST([슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 유형)+SD(분류자) |
| NF(Network Function) | [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 코어의 기능 단위. [AMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/)·[SMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/)·UPF 등을 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)별 인스턴스화 |

- **📢 섹션 요약 비유**: [네트워크 슬라이싱](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)은 구름 소프트웨어로 도로를 실시간 재배치하는 것이다. 아침(출근 시간, [eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/) 증가)엔 고속차선을 넓히고, 수술 시간([uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/) 급증)엔 앰뷸런스 차선을 더 확보한다. 물리 도로는 그대로인데 소프트웨어로 분배만 바꾼다.

---

## Ⅲ. 비교 및 연결

<strong><a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/">SA</a>(<a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/">Standalone</a>) vs <a href="/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/">NSA</a>(Non-<a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/">Standalone</a>)</strong>

| 항목 | [NSA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/) (Non-[Standalone](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/)) | [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) ([Standalone](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/150_5g_sa_standalone_architecture/)) |
|:---:|:---:|:---:|
| 코어 네트워크 | [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) [EPC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/753_epc_evolved_packet_core_sgw_pgw/) 공용 | [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 전용 코어([5GC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/)) |
| 기지국 | [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) + gNB 앵커링 | gNB 단독 |
| 슬라이싱 지원 | 제한적 | 완전 지원 |
| [uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/) 지원 | 제한적 | 완전 지원 |
| 도입 비용 | 낮음 (기존 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 활용) | 높음 |
| 진화 경로 | 과도기 | [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 최종 목표 |

<strong><a href="/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/">5G</a> <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/">SBA</a>(Service-Based <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/">Architecture</a>)</strong>: [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 코어는 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) 구조로 설계. [AMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/)(접속 관리), [SMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/)([세션 관리](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/507_session_management_security/)), UPF(사용자 평면), [PCF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/772_pcf_policy_control_function_qos/)([정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)), NSSF([슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) 선택) 등 기능별 독립 NF로 분리.

- **📢 섹션 요약 비유**: NSA는 새집([5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 기지국)을 짓되 구형 전기 설비([LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 코어)를 그대로 쓰는 것이다. 돈은 적게 들지만 새 가전제품([uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/)·슬라이싱)을 다 쓸 수 없다. SA는 전기 설비까지 전부 교체한 완성형이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong>산업별 <a href="/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/">슬라이스</a> 설계 예시</strong>

| 산업 | [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) 유형 | 핵심 요구사항 |
|:---|:---:|:---|
| 자율주행 | [uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/) | 1ms [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 99.999% [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) |
| 스마트팩토리 | [uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/) + [private 5G](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/365_5g_tsn/) | 결정론적 통신, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 로컬 처리 |
| 미디어·방송 | [eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/) | 20Gbps, 대용량 |
| 스마트시티 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) | [mMTC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/) | 초저전력, 대량 기기 |

**기술사 핵심 판단**

1. [네트워크 슬라이싱](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)은 동일 물리 망에서 SLA가 다른 다수 고객을 동시 지원하는 <strong>멀티테넌시(<a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/014_multi_tenancy/">Multi-tenancy</a>)</strong> 구현 기술.
2. [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) 격리([Isolation](/knowledge-base/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/)): [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) 간 트래픽 누출 방지 -> 보안 및 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 보장.
3. 프라이빗 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)([Private 5G](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/365_5g_tsn/)): 기업 전용 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 네트워크. [uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/) [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)를 자사 공장 내에서 독점 운용.

- **📢 섹션 요약 비유**: [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) 격리는 아파트 분리벽이다. 옆집(다른 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)) 소음(트래픽)이 내 집(내 [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/))에 들어오지 않도록 벽(격리)을 튼튼하게 세워야 한다.

---

## Ⅴ. 기대효과 및 결론

5G의 3대 특성과 [네트워크 슬라이싱](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)은 통신 산업을 B2C 중심에서 B2B 중심으로 전환하는 핵심 엔진이다. [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 구조 완성과 슬라이싱 상용화가 진행될수록 자율주행·스마트팩토리·의료 등 미션 크리티컬 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)의 무선화가 가속된다.

- **📢 섹션 요약 비유**: [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) + 슬라이싱은 만능 임대 공간이다. 하나의 건물(물리 인프라)에서 식당([eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/))·수술실([uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/))·창고([mMTC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/))를 동시에 운영할 수 있다. 수술실과 식당은 서로 절대 방해받지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| NSSF | [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) 선택 · Network [Slice](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) [Selection](/knowledge-base/studynote/10_ai/01_ai_basics/022_mcts_four_stages/) Function |
| NSI | [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) 인스턴스 · 가상 전용 네트워크 인스턴스 |
| [SBA](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/151_sba_service_based_architecture_5g/)(Service-Based [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/)) | [5GC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/), [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) · [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 코어 기능 분리 구조 |
| [AMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/770_amf_access_mobility_management_function/)/[SMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/)/UPF | [5GC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/768_5gc_5g_core_network_evolution/) NF · 접속·[세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)·사용자평면 관리 |
| 프라이빗 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) | 기업 전용망 · [uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/) [슬라이스](/knowledge-base/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/) 자체 운용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[슬라이스 선택 · Network Slice Selection Function] -> [5G 3대 특성과 네트워크 슬라이싱] -> [기업 전용망 · uRLLC 슬라이스 자체 운용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 5G의 세 가지 특성은 빠른 차선([eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/)), 앰뷸런스 전용차선([uRLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/)), 오토바이 전용도로([mMTC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/))예요.
2. [네트워크 슬라이싱](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)은 하나의 도로를 소프트웨어로 세 개의 전용차선으로 분리하는 마법이에요.
3. [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 아키텍처는 새 건물에 새 전기 설비까지 다 새로 설치하는 것이어서 비싸지만, 5G의 모든 기능을 100% 쓸 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 495 / 552

<- **이전**: [494. V2X 차량 통신과 C-V2X 5G 연계 (V2X Vehicle Communication and C-V2X 5G)](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/494_v2x_c_v2x_5g_vehicle_communication/)
**다음**: [496. 6G 테라헤르츠, NTN, RIS 기술 (6G Terahertz NTN RIS Satellite Communication)](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/496_6g_terahertz_ntn_ris_satellite/) ->

---
