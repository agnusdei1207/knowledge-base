+++
title = "766. NSA (Non-Standalone 코어는 LTE EPC / 기지국 제어 무선 NR 결합 구축 진보 비용 최소 고속도 망 적용 구조 융합 통신 모델)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NSA는 차세대 통신 아키텍처에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: NSA를 이해하면 유연성과 확장성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 무선 기지국(gNB)을 독자적으로 쓰지 않고, **기존에 구축되어 있던 4G [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 코어망([EPC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/753_epc_evolved_packet_core_sgw_pgw/))과 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 기지국(eNodeB)에 기대어(종속되어) [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 제공하는 혼합형 네트워크 아키텍처**입니다.
- **[3GPP](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/751_3gpp_3rd_generation_partnership_project/) 표준 (Option 3 계열)**: [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 시장 선점을 위해 3GPP가 가장 먼저 승인해 준 현실적인 타협안입니다. 대한민국이 2019년 세계 최초 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 상용화를 타이틀을 땄을 때 썼던 방식이 바로 100% 이 NSA 방식입니다.

```text
[FR2 주파수]
    │
    ▼
[NSA]
    │
    └──▶ [SA 풀 전환 클라우드 네이티브 슬라이싱 전…]
```

- **📢 섹션 요약 비유**: NSA는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 스마트폰이 전원을 켜면 4G와 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 양다리를 걸칩니다. (EN-DC, E-UTRA-NR Dual Connectivity)

1. **제어 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) (Control Plane) ➜ 무조건 4G [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 뇌를 거침**: 
   - 폰이 켜져서 "나 인터넷 연결해 줘, 요금제 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해 줘" 하는 깐깐한 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/제어 요청은 **100% 4G [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 기지국을 거쳐 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 코어망([MME](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/754_mme_mobility_management_entity/)) 서버**로 보냅니다. LTE가 여전히 모든 통신망의 '마스터(Master)' 역할을 굳건히 쥡니다.
2. **사용자 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) (User Plane) ➜ [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)로 고속 다운로드**: 
   - [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이 끝나고 넷플릭스 영화 다운로드(무거운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 시작하면, 제어는 LTE가 쥐고 있으면서 **"[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 저기 옆에 세워둔 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 기지국(gNB) [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)로 엄청 빠르게 쏟아부어라!"**라고 지시합니다.
   - 단말기는 LTE와 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 기지국 두 군데에서 동시에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 받아 합칩니다(Dual Connectivity 속도 뻥튀기).

```text
[FR2 주파수]
    │
    ▼
[NSA]
    │
    └──▶ [SA 풀 전환 클라우드 네이티브 슬라이싱 전…]
```

- **📢 섹션 요약 비유**: NSA의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

- **최소 비용, 최고 속도 구축**: 통신사는 수십조 원을 들여 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 코어 서버를 새로 지을 필요가 없습니다. 그냥 건물 옥상에 올라가서 기존 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 철탑 옆에 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 무선 [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)만 덜렁 달아놓고 랜선만 꼽으면 즉시 그 동네를 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 존으로 만들 수 있었습니다. 전 세계 통신사들이 열광하며 이 방식을 택했습니다.
- **[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 끊김 없는 커버리지 보장**: [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 전파가 닿지 않는 골목길에 들어가도 걱정 없습니다. 베이스가 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 망이므로 자연스럽게 LTE로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 1초 만에 넘어가며 끊김이 발생하지 않습니다.

NSA를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. FR2 주파수가 기반 조건을 만든다면, NSA는 그 위에서 핵심 메커니즘을 구현하고, [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 풀 전환 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 슬라이싱 전…는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 유연성과 확장성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | FR2 주파수의 기반 정리 | NSA의 핵심 동작 | [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 풀 전환 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 슬라이싱 전…의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 유연성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: NSA는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

결국 반쪽짜리 5G라는 욕을 먹는 이유입니다.
- 무선 속도([eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/))는 분명 5G처럼 빠르지만, 네트워크 뒤에 있는 두뇌(서버)가 구형 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)([EPC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/753_epc_evolved_packet_core_sgw_pgw/)) 장비입니다. 
- 따라서 5G의 진짜 혁명인 **"1ms 초저지연([URLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/))과 수백만 개 사물통신([mMTC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/762_mmtc_massive_machine_type_communications/)), [네트워크 슬라이싱](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)" 기능은 구형 [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 서버가 처리하지 못하기 때문에 절대 구현할 수 없습니다.** 결국 자율주행이나 [스마트 팩토리](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/) 같은 B2B 산업용 5G를 하려면 반드시 다음 767번의 **[SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) (단독 모드)**로 넘어가야만 합니다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: NSA(비단독 모드)는 구형 소나타([LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 코어망) 차체 위에다가 포르쉐 엔진([5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 무선 [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/))만 얹어놓은 하이브리드 프랑켄슈타인 튜닝카입니다. 엔진이 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 포르쉐니까 직진 도로(다운로드 속도)에서는 엄청난 속도로 빵빵하게 잘 달립니다([eMBB](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/) 달성). 하지만 브레이크나 핸들 조향장치, 중앙 통제 컴퓨터(제어망)는 여전히 구형 낡은 소나타의 부품을 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 때문에, 코너를 1ms 만에 초저지연으로 돌아나가는 정밀 자율주행([URLLC](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/761_urllc_ultra_reliable_low_latency/)) 제어 같은 고급 기술은 죽었다 깨어나도 구사할 수 없는 반쪽짜리 슈퍼카입니다.

---

## Ⅴ. 기대효과 및 결론

NSA는 차세대 통신 아키텍처를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 유연성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 풀 전환 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 슬라이싱 전…, [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 네트워크 최적화, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 네트워크 최적화 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: NSA는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| FR2 주파수 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 기반 구조 (Service-Based [Architecture](/knowledge-base/studynote/12_it_management/05_security_compliance/319_architecture/)) | 기능을 느슨하게 결합해 유연성을 높인다. |
| [네트워크 슬라이싱](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/) ([Network Slicing](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)) | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 요구사항을 논리적으로 분리한다. |
| [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 풀 전환 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 슬라이싱 전… | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: FR2 주파수]
    │
    ▼
[현재 개념: NSA]
    │
    ├──▶ [확장 A: SA 풀 전환 클라우드 네이티브 슬라이싱 전…]
    └──▶ [확장 B: AI 기반 네트워크 최적화]
```

NSA는 FR2 주파수에서 출발해 현재 메커니즘을 정교화하고, 이후 [SA](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) 풀 전환 [클라우드 네이티브](/knowledge-base/studynote/04_software_engineering/11_testing_validation/531_cloud_native_architecture/) 슬라이싱 전…와 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 네트워크 최적화 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 장난감 도시를 여러 구역으로 나누고 필요한 규칙만 골라 쓰는 것과 같아요.
2. 이 개념은 빠른 길, 안전한 길, 많은 사람이 쓰는 길을 각각 다르게 꾸미게 해줘요.
3. 그래서 미래 통신망이 더 똑똑하고 유연해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 887 / 1120

← **이전**: [765. FR2 주파수 (mmWave 24Ghz~ 밀리미터파 직진성 극한, 장애물 회절 약화 대형 스몰셀 조밀 구성 기술 체계 대역)](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/765_fr2_mmwave_28ghz_small_cell_beamforming/)
**다음**: [767. SA (Standalone 코어까지 5G Core(5GC) 풀 전환 클라우드 네이티브 슬라이싱 전체 통제 네트워크 지연 해결](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/767_sa_standalone_5g_core_network/) →

---
