---
title: 495. 5G 3대 특성과 네트워크 슬라이싱 (5G eMBB uRLLC mMTC Network Slicing)
date: '2026-05-09'
tags:
- studynote-ict-convergence
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 5G의 핵심 가치는 빠른 속도([[760_embb_enhanced_mobile_broadband_vr_ar|eMBB]])만이 아니라, 1ms 초저지연([[761_urllc_ultra_reliable_low_latency|uRLLC]])과 km²당 100만 기기 동시 접속([[762_mmtc_massive_machine_type_communications|mMTC]])이라는 서로 상충하는 세 가지 요구사항을 단일 물리망 위에서 [[149_network_slicing_5g_architecture|네트워크 슬라이싱]]([[149_network_slicing_5g_architecture|Network Slicing]])으로 동시 충족하는 데 있다.
> 2. **가치**: [[149_network_slicing_5g_architecture|네트워크 슬라이싱]]은 하나의 물리 [[418_5g_embb_urllc_mmtc_slicing|5G]] 인프라를 산업별 맞춤 가상망(NSI)으로 분리함으로써, 통신사는 B2B [[090_service_kubernetes_network_load_balancing|서비스]]를 산업 수요에 맞게 판매하고 기업은 전용 품질([[085_sla|SLA]])을 보장받는다.
> 3. **판단 포인트**: [[767_sa_standalone_5g_core_network|SA]]([[150_5g_sa_standalone_architecture|Standalone]]) 아키텍처는 [[418_5g_embb_urllc_mmtc_slicing|5G]] 코어([[768_5gc_5g_core_network_evolution|5GC]])와 gNB가 완전 분리되어 [[149_network_slicing_5g_architecture|네트워크 슬라이싱]]·[[761_urllc_ultra_reliable_low_latency|URLLC]] 등 [[418_5g_embb_urllc_mmtc_slicing|5G]] 고유 기능을 완전히 지원한다. [[766_nsa_non_standalone_5g_lte_core|NSA]](Non-[[150_5g_sa_standalone_architecture|Standalone]])는 [[752_lte_long_term_evolution_4g|LTE]] 코어를 공유해 전환 비용은 낮지만 [[418_5g_embb_urllc_mmtc_slicing|5G]] 핵심 기능이 제한된다.

---

## Ⅰ. 개요 및 필요성

**[[418_5g_embb_urllc_mmtc_slicing|5G]] ITU-R IMT-2020 표준 3대 [[090_service_kubernetes_network_load_balancing|서비스]]**

| [[090_service_kubernetes_network_load_balancing|서비스]] | 영문 | 핵심 지표 | 주요 사용처 |
|:---:|:---:|:---:|:---:|
| [[760_embb_enhanced_mobile_broadband_vr_ar|eMBB]] | Enhanced Mobile Broadband | 최대 20Gbps | VR·AR·4K 스트리밍 |
| [[761_urllc_ultra_reliable_low_latency|uRLLC]] | Ultra-Reliable Low-Latency | [[015_지연_데이터_관점|지연]] 1ms, [[085_confidence_association_rule_conditional_probability|신뢰도]] 99.999% | 자율주행·원격 수술·공장 제어 |
| [[762_mmtc_massive_machine_type_communications|mMTC]] | massive Machine-Type Communication | 100만 기기/km² | 스마트시티·스마트팜·미터링 |

**4G([[752_lte_long_term_evolution_4g|LTE]]) 한계와 [[418_5g_embb_urllc_mmtc_slicing|5G]] 등장**: LTE는 단일 [[123_pipe|파이프]](단순 고속) 구조로 서로 다른 [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 요구를 동시에 충족 불가. 5G는 [[015_virtualization|가상화]]([[865_nfv_network_functions_virtualization_architecture|NFV]])·소프트웨어 정의([[633_sdn_whitebox|SDN]]) 기반으로 유연한 다중 [[388_qos_quality_of_service_best_effort_intserv_diffserv|QoS]] 관리를 실현한다.

- **📢 섹션 요약 비유**: 4G는 단일 도로, 5G는 세 개의 전용 차선이다. eMBB는 고속차선(빠른 차), uRLLC는 앰뷸런스 전용차선(항상 빈 길), mMTC는 오토바이 전용 넓은 갓길. 이 세 차선이 서로 침범하지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────┐
│           5G 네트워크 슬라이싱 아키텍처                    │
├──────────────────────────────────────────────────────────┤
│  [물리 인프라]  gNB(기지국) + 5G Core(5GC) 하드웨어        │
│        │                                                 │
│  [가상화 계층]  NFV(네트워크 기능 가상화) / SDN             │
│        │                                                 │
│  [슬라이스 관리]  NSSF(Network Slice Selection Function)  │
│  ┌─────────────────────────────────────────────────┐    │
│  │  NSI-1 (eMBB 슬라이스)   │ 넷플릭스·통신사 서비스  │    │
│  ├─────────────────────────┤──────────────────────┤    │
│  │  NSI-2 (uRLLC 슬라이스) │ 자율주행·원격 수술     │    │
│  ├─────────────────────────┤──────────────────────┤    │
│  │  NSI-3 (mMTC 슬라이스)  │ 스마트시티·IoT 센서    │    │
│  └─────────────────────────┴──────────────────────┘    │
│                                                          │
│  [SLA 보장]  각 슬라이스별 독립 QoS 보장                   │
└──────────────────────────────────────────────────────────┘
```

### [[149_network_slicing_5g_architecture|네트워크 슬라이싱]] 핵심 개념

| 개념 | 설명 |
|:---|:---|
| NSI(Network [[331_neuromorphic_ai_db|Slice]] Instance) | 특정 [[090_service_kubernetes_network_load_balancing|서비스]]를 위해 생성된 독립 가상 네트워크 인스턴스 |
| NSSF(Network [[331_neuromorphic_ai_db|Slice]] [[022_mcts_four_stages|Selection]] Function) | 단말 요청에 따라 적절한 [[331_neuromorphic_ai_db|슬라이스]]를 선택·배정 |
| S-NSSAI | [[331_neuromorphic_ai_db|슬라이스]] [[289_identification_flags_fragmentation_offset|식별자]]. SST([[331_neuromorphic_ai_db|슬라이스]] [[090_service_kubernetes_network_load_balancing|서비스]] 유형)+SD(분류자) |
| NF(Network Function) | [[418_5g_embb_urllc_mmtc_slicing|5G]] 코어의 기능 단위. [[770_amf_access_mobility_management_function|AMF]]·[[771_smf_upf_session_management_user_plane|SMF]]·UPF 등을 [[331_neuromorphic_ai_db|슬라이스]]별 인스턴스화 |

- **📢 섹션 요약 비유**: [[149_network_slicing_5g_architecture|네트워크 슬라이싱]]은 구름 소프트웨어로 도로를 실시간 재배치하는 것이다. 아침(출근 시간, [[760_embb_enhanced_mobile_broadband_vr_ar|eMBB]] 증가)엔 고속차선을 넓히고, 수술 시간([[761_urllc_ultra_reliable_low_latency|uRLLC]] 급증)엔 앰뷸런스 차선을 더 확보한다. 물리 도로는 그대로인데 소프트웨어로 분배만 바꾼다.

---

## Ⅲ. 비교 및 연결

**[[767_sa_standalone_5g_core_network|SA]]([[150_5g_sa_standalone_architecture|Standalone]]) vs [[766_nsa_non_standalone_5g_lte_core|NSA]](Non-[[150_5g_sa_standalone_architecture|Standalone]])**

| 항목 | [[766_nsa_non_standalone_5g_lte_core|NSA]] (Non-[[150_5g_sa_standalone_architecture|Standalone]]) | [[767_sa_standalone_5g_core_network|SA]] ([[150_5g_sa_standalone_architecture|Standalone]]) |
|:---:|:---:|:---:|
| 코어 네트워크 | [[752_lte_long_term_evolution_4g|LTE]] [[753_epc_evolved_packet_core_sgw_pgw|EPC]] 공용 | [[418_5g_embb_urllc_mmtc_slicing|5G]] 전용 코어([[768_5gc_5g_core_network_evolution|5GC]]) |
| 기지국 | [[752_lte_long_term_evolution_4g|LTE]] + gNB 앵커링 | gNB 단독 |
| 슬라이싱 지원 | 제한적 | 완전 지원 |
| [[761_urllc_ultra_reliable_low_latency|uRLLC]] 지원 | 제한적 | 완전 지원 |
| 도입 비용 | 낮음 (기존 [[752_lte_long_term_evolution_4g|LTE]] 활용) | 높음 |
| 진화 경로 | 과도기 | [[418_5g_embb_urllc_mmtc_slicing|5G]] 최종 목표 |

**[[418_5g_embb_urllc_mmtc_slicing|5G]] [[151_sba_service_based_architecture_5g|SBA]](Service-Based [[319_architecture|Architecture]])**: [[418_5g_embb_urllc_mmtc_slicing|5G]] 코어는 [[532_microservices_decomposition_patterns|마이크로서비스]] 구조로 설계. [[770_amf_access_mobility_management_function|AMF]](접속 관리), [[771_smf_upf_session_management_user_plane|SMF]]([[507_session_management_security|세션 관리]]), UPF(사용자 평면), [[772_pcf_policy_control_function_qos|PCF]]([[164_policy|정책]]), NSSF([[331_neuromorphic_ai_db|슬라이스]] 선택) 등 기능별 독립 NF로 분리.

- **📢 섹션 요약 비유**: NSA는 새집([[418_5g_embb_urllc_mmtc_slicing|5G]] 기지국)을 짓되 구형 전기 설비([[752_lte_long_term_evolution_4g|LTE]] 코어)를 그대로 쓰는 것이다. 돈은 적게 들지만 새 가전제품([[761_urllc_ultra_reliable_low_latency|uRLLC]]·슬라이싱)을 다 쓸 수 없다. SA는 전기 설비까지 전부 교체한 완성형이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**산업별 [[331_neuromorphic_ai_db|슬라이스]] 설계 예시**

| 산업 | [[331_neuromorphic_ai_db|슬라이스]] 유형 | 핵심 요구사항 |
|:---|:---:|:---|
| 자율주행 | [[761_urllc_ultra_reliable_low_latency|uRLLC]] | 1ms [[015_지연_데이터_관점|지연]], 99.999% [[085_confidence_association_rule_conditional_probability|신뢰도]] |
| 스마트팩토리 | [[761_urllc_ultra_reliable_low_latency|uRLLC]] + [[365_5g_tsn|private 5G]] | 결정론적 통신, [[001_dikw_pyramid|데이터]] 로컬 처리 |
| 미디어·방송 | [[760_embb_enhanced_mobile_broadband_vr_ar|eMBB]] | 20Gbps, 대용량 |
| 스마트시티 [[101_iot_concept|IoT]] | [[762_mmtc_massive_machine_type_communications|mMTC]] | 초저전력, 대량 기기 |

**기술사 핵심 판단**

1. [[149_network_slicing_5g_architecture|네트워크 슬라이싱]]은 동일 물리 망에서 SLA가 다른 다수 고객을 동시 지원하는 **멀티테넌시([[014_multi_tenancy|Multi-tenancy]])** 구현 기술.
2. [[331_neuromorphic_ai_db|슬라이스]] 격리([[195_isolation_concurrency_control|Isolation]]): [[331_neuromorphic_ai_db|슬라이스]] 간 트래픽 누출 방지 → 보안 및 [[282_performance_tactics|성능]] 보장.
3. 프라이빗 [[418_5g_embb_urllc_mmtc_slicing|5G]]([[365_5g_tsn|Private 5G]]): 기업 전용 [[418_5g_embb_urllc_mmtc_slicing|5G]] 네트워크. [[761_urllc_ultra_reliable_low_latency|uRLLC]] [[331_neuromorphic_ai_db|슬라이스]]를 자사 공장 내에서 독점 운용.

- **📢 섹션 요약 비유**: [[331_neuromorphic_ai_db|슬라이스]] 격리는 아파트 분리벽이다. 옆집(다른 [[331_neuromorphic_ai_db|슬라이스]]) 소음(트래픽)이 내 집(내 [[331_neuromorphic_ai_db|슬라이스]])에 들어오지 않도록 벽(격리)을 튼튼하게 세워야 한다.

---

## Ⅴ. 기대효과 및 결론

5G의 3대 특성과 [[149_network_slicing_5g_architecture|네트워크 슬라이싱]]은 통신 산업을 B2C 중심에서 B2B 중심으로 전환하는 핵심 엔진이다. [[767_sa_standalone_5g_core_network|SA]] 구조 완성과 슬라이싱 상용화가 진행될수록 자율주행·스마트팩토리·의료 등 미션 크리티컬 [[090_service_kubernetes_network_load_balancing|서비스]]의 무선화가 가속된다.

- **📢 섹션 요약 비유**: [[418_5g_embb_urllc_mmtc_slicing|5G]] + 슬라이싱은 만능 임대 공간이다. 하나의 건물(물리 인프라)에서 식당([[760_embb_enhanced_mobile_broadband_vr_ar|eMBB]])·수술실([[761_urllc_ultra_reliable_low_latency|uRLLC]])·창고([[762_mmtc_massive_machine_type_communications|mMTC]])를 동시에 운영할 수 있다. 수술실과 식당은 서로 절대 방해받지 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| NSSF | [[331_neuromorphic_ai_db|슬라이스]] 선택 · Network [[331_neuromorphic_ai_db|Slice]] [[022_mcts_four_stages|Selection]] Function |
| NSI | [[331_neuromorphic_ai_db|슬라이스]] 인스턴스 · 가상 전용 네트워크 인스턴스 |
| [[151_sba_service_based_architecture_5g|SBA]](Service-Based [[319_architecture|Architecture]]) | [[768_5gc_5g_core_network_evolution|5GC]], [[532_microservices_decomposition_patterns|마이크로서비스]] · [[418_5g_embb_urllc_mmtc_slicing|5G]] 코어 기능 분리 구조 |
| [[770_amf_access_mobility_management_function|AMF]]/[[771_smf_upf_session_management_user_plane|SMF]]/UPF | [[768_5gc_5g_core_network_evolution|5GC]] NF · 접속·[[160_session_controlling_terminal|세션]]·사용자평면 관리 |
| 프라이빗 [[418_5g_embb_urllc_mmtc_slicing|5G]] | 기업 전용망 · [[761_urllc_ultra_reliable_low_latency|uRLLC]] [[331_neuromorphic_ai_db|슬라이스]] 자체 운용 |

### 📈 관련 키워드 및 발전 흐름도

```text
[슬라이스 선택 · Network Slice Selection Function] → [5G 3대 특성과 네트워크 슬라이싱] → [기업 전용망 · uRLLC 슬라이스 자체 운용]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 5G의 세 가지 특성은 빠른 차선([[760_embb_enhanced_mobile_broadband_vr_ar|eMBB]]), 앰뷸런스 전용차선([[761_urllc_ultra_reliable_low_latency|uRLLC]]), 오토바이 전용도로([[762_mmtc_massive_machine_type_communications|mMTC]])예요.
2. [[149_network_slicing_5g_architecture|네트워크 슬라이싱]]은 하나의 도로를 소프트웨어로 세 개의 전용차선으로 분리하는 마법이에요.
3. [[767_sa_standalone_5g_core_network|SA]] 아키텍처는 새 건물에 새 전기 설비까지 다 새로 설치하는 것이어서 비싸지만, 5G의 모든 기능을 100% 쓸 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 495 / 552

← **이전**: [[494_v2x_c_v2x_5g_vehicle_communication|494. V2X 차량 통신과 C-V2X 5G 연계 (V2X Vehicle Communication and C-V2X 5G)]]
**다음**: [[496_6g_terahertz_ntn_ris_satellite|496. 6G 테라헤르츠, NTN, RIS 기술 (6G Terahertz NTN RIS Satellite Communication)]] →

---
