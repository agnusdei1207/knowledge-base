---
title: "765. FR2 주파수 (mmWave 24Ghz~ 밀리미터파 직진성 극한, 장애물 회절 약화 대형 스몰셀 조밀 구성 기술 체계 대역)"
date: "2026-05-08"
tags:
  - "studynote-network"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: FR2 주파수는 차세대 통신 아키텍처에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: FR2 주파수를 이해하면 유연성과 확장성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- [3GPP](/studynote/03_network/15_nextgen_communication_architecture/751_3gpp_3rd_generation_partnership_project/) [5G NR](/studynote/03_network/15_nextgen_communication_architecture/763_5g_nr_new_radio_scalable_numerology/) 표준의 두 번째 주파수 대역으로, <strong>24.25 GHz부터 52.6 GHz 사이의 극도로 높은 초고주파 대역</strong>을 의미합니다. (한국은 28 GHz 대역을 할당했었습니다.)
- <strong><a href="/studynote/03_network/03_physical_layer_media/156_mmwave_millimeter_wave/">밀리미터파</a>(<a href="/studynote/03_network/03_physical_layer_media/156_mmwave_millimeter_wave/">mmWave</a>)</strong>: 전파의 파장 길이가 1mm ~ 10mm 정도로 매우 짧다고 해서 붙여진 이름입니다.

```text
[FR1 주파수]
    |
    v
[FR2 주파수]
    |
    +---> [NSA]
```

- **📢 섹션 요약 비유**: FR2 주파수는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 빛을 발하는 장점: 무한한 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) ([초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) [eMBB](/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/) 달성)
- 이 높은 주파수 동네는 아무도 살지 않는 '광활한 텍사스 평야'입니다.
- 통신사들이 800MHz 폭이라는 어마어마하게 넓은 초대형 차선을 통째로 가져다 쓸 수 있습니다. 덕분에 5G의 3대 목표 중 하나인 <strong><a href="/studynote/03_network/15_nextgen_communication_architecture/760_embb_enhanced_mobile_broadband_vr_ar/">eMBB</a>(최대 20Gbps 속도)</strong>를 물리적으로 100% 뽑아내어, 수만 명이 모인 경기장에서 8K VR 홀로그램 영상을 끊김 없이 볼 수 있는 마법을 부립니다.

### 2. 최악의 단점: 끔찍한 투과력과 짧은 사거리
- 파장이 짧은 초고주파 전파는 물리적으로 완벽하게 <strong>빛(레이저)과 같은 '직진성'</strong>을 가집니다.
- **경로 손실 (Path Loss)**: 허공을 날아가는 동안 공기 중의 산소와 수분에 에너지를 뺏겨 순식간에 소멸합니다. 기지국에서 100m~200m만 벗어나도 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)가 떨어집니다.
- **회절성 제로 (장애물 붕괴)**: 건물 콘크리트 벽은 절대 못 뚫습니다. 심지어 길거리 나무의 나뭇잎, 비 오는 날씨, 사용자가 폰을 쥔 손가락에 가려져도 전파가 막혀 통신이 끊깁니다.

```text
[FR1 주파수]
    |
    v
[FR2 주파수]
    |
    +---> [NSA]
```

- **📢 섹션 요약 비유**: FR2 주파수의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

1. <strong>대형 <a href="/studynote/03_network/03_physical_layer_media/178_small_cell_macro_femto/">스몰셀</a> (<a href="/studynote/03_network/03_physical_layer_media/178_small_cell_macro_femto/">Small Cell</a>) 조밀 구성 (네트워크 토폴로지)</strong>
   - 옥상에 거대한 기지국(매크로 셀) 하나 세워봐야 200m 밖으론 전파가 안 갑니다.
   - **대책**: 도시의 모든 가로등, 전봇대, 신호등, 지하철 천장마다 반경 50m를 커버하는 공유기 크기의 소형 기지국([스몰셀](/studynote/03_network/03_physical_layer_media/178_small_cell_macro_femto/))을 수십만 개씩 도배(Densification)해야만 FR2를 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)할 수 있습니다. (천문학적 구축 비용 발생)

2. <strong><a href="/studynote/03_network/02_multiplexing_multiple_access/101_beamforming/">빔포밍</a> (<a href="/studynote/03_network/02_multiplexing_multiple_access/101_beamforming/">Beamforming</a>)과 빔 트래킹 (<a href="/studynote/03_network/03_physical_layer_media/177_smart_antenna_phased_array/">스마트 안테나</a>)</strong>
   - 허공으로 흩어지는 전파의 힘을 한데 모아, 레이저 포인터처럼 가입자(스마트폰)의 위치로만 정밀하게 쏘아 보내어 짧은 사거리를 억지로 늘리고 장애물을 피하게 만드는 필수 [안테나](/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/) 기술입니다. (777번 문서에서 상세히 다룸)

FR2 주파수를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. FR1 주파수가 기반 조건을 만든다면, FR2 주파수는 그 위에서 핵심 메커니즘을 구현하고, NSA는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 유연성과 확장성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | FR1 주파수의 기반 정리 | FR2 주파수의 핵심 동작 | NSA의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 유연성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: FR2 주파수는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

미국은 야구장이나 광장 위주로 조금 깔았지만, 한국 통신사(SKT, KT, LGU+)들은 수만 개의 가로등에 [스몰셀](/studynote/03_network/03_physical_layer_media/178_small_cell_macro_femto/)을 도배할 투자비(조 단위)를 감당하지 못하고 결국 <strong>정부에 28GHz 주파수를 반납(포기)해 버리는 사태</strong>가 발생했습니다. 현재 한국의 일반 스마트폰 사용자는 이 20Gbps짜리 '진짜 [5G](/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)(FR2)'를 사실상 쓸 수 없으며, B2B 공장 전용망(이음5G) 등에서만 제한적으로 부활을 노리고 있습니다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: FR2([mmWave](/studynote/03_network/03_physical_layer_media/156_mmwave_millimeter_wave/) 28GHz)는 칠흑 같은 어둠 속에서 목표물을 비추는 '초강력 레이저 포인터'입니다. 레이저 불빛은 엄청나게 강하고 선명해서(20Gbps [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/)) 한 번에 엄청난 정보를 보낼 수 있습니다. 하지만 치명적인 단점이 있습니다. 누군가 내 앞을 스윽 지나가거나, 벽 뒤에 숨거나, 심지어 종이 한 장만 앞에 대도 레이저 빛이 완전히 차단되어 아무것도 안 보입니다. 이 툭하면 끊기는 레이저로 통신하려면 온 동네 구석구석, 벽마다(가로등마다) 수백만 개의 레이저 발사기([스몰셀](/studynote/03_network/03_physical_layer_media/178_small_cell_macro_femto/))를 달아놔야 하는 돈 먹는 하마입니다.

---

## Ⅴ. 기대효과 및 결론

FR2 주파수는 차세대 통신 아키텍처를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 유연성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [NSA](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/), [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 네트워크 최적화, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 네트워크 최적화 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: FR2 주파수는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| FR1 주파수 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 기반 구조 (Service-Based [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/)) | 기능을 느슨하게 결합해 유연성을 높인다. |
| [네트워크 슬라이싱](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/) ([Network Slicing](/studynote/06_ict_convergence/02_iot_mobility/149_network_slicing_5g_architecture/)) | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)별 요구사항을 논리적으로 분리한다. |
| [NSA](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: FR1 주파수]
    |
    v
[현재 개념: FR2 주파수]
    |
    +---> [확장 A: NSA]
    +---> [확장 B: AI 기반 네트워크 최적화]
```

FR2 주파수는 FR1 주파수에서 출발해 현재 메커니즘을 정교화하고, 이후 NSA와 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 네트워크 최적화 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 큰 장난감 도시를 여러 구역으로 나누고 필요한 규칙만 골라 쓰는 것과 같아요.
2. 이 개념은 빠른 길, 안전한 길, 많은 사람이 쓰는 길을 각각 다르게 꾸미게 해줘요.
3. 그래서 미래 통신망이 더 똑똑하고 유연해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 886 / 1120

<- **이전**: [764. FR1 주파수 (Sub-6GHz 대역, 기존 호환 및 중간 광역/보편 속도 모델 적용 제어)](/studynote/03_network/15_nextgen_communication_architecture/764_fr1_sub_6ghz_5g_coverage/)
**다음**: [766. NSA (Non-Standalone 코어는 LTE EPC / 기지국 제어 무선 NR 결합 구축 진보 비용 최소 고속도 망 적용](/studynote/03_network/15_nextgen_communication_architecture/766_nsa_non_standalone_5g_lte_core/) ->

---
