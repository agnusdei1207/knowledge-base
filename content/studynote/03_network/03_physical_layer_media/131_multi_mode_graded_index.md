+++
title = "131. 멀티모드 언덕형 광섬유 (Multi-mode Graded-index)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 코어의 [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/)을 중심에서 외곽으로 갈수록 점진적으로 낮아지게 설계하여, 다양한 경로(모드)로 입사된 빛의 도달 시간을 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)하는 광섬유 기술이다.
> 2. **가치**: 기존 계단형(Step-index) 광섬유의 치명적 단점인 모드 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)(Mode [Dispersion](/knowledge-base/studynote/03_network/03_physical_layer_media/133_dispersion_mode_chromatic/))을 극복하여 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 내 10G~100G급 고속 전송을 경제적으로 구현한다.
> 3. **판단 포인트**: 고가의 [단일모드 광섬유](/knowledge-base/studynote/03_network/03_physical_layer_media/132_single_mode_multi_mode_fiber/)([SMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/))와 저렴한 계단형 MMF 사이의 트레이드오프를 해결하며, VCSEL 광원 및 OM3/OM4 표준과 결합해 근거리 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/)망의 근간이 된다.

---

## Ⅰ. 개요 및 필요성

멀티모드 언덕형 광섬유 (Multi-mode Graded-index Fiber, GI-MMF)는 다수의 광 경로(모드)를 허용하면서도 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 왜곡을 억제하기 위해 개발된 전송 매체다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 광통신에 사용된 계단형(Step-index) MMF는 코어의 [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/)이 균일하여, 직선으로 이동하는 빛과 지그재그로 반사되며 이동하는 빛 간의 경로 차이가 발생했다. 이로 인해 수신단에서 빛의 펄스가 퍼지는 <strong>모드 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>(Modal <a href="/knowledge-base/studynote/03_network/03_physical_layer_media/133_dispersion_mode_chromatic/">Dispersion</a>)</strong>이 발생하여 고속 전송이 불가능했다.
이 문제를 해결하기 위해 도입된 GI-MMF는 코어 중심부의 [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/)을 가장 높게, 외곽으로 갈수록 낮게 포물선 형태로 설계했다. 빛의 속도는 [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/)에 반비례하므로($v=c/n$), 외곽으로 우회하는 빛은 빠른 속도로 이동하고 중심을 통과하는 빛은 느리게 이동하여 결국 수신단에 동시에 도착하게 된다. 이는 [단일모드 광섬유](/knowledge-base/studynote/03_network/03_physical_layer_media/132_single_mode_multi_mode_fiber/)([SMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/))의 높은 구축 비용을 회피하면서도 수백 미터 구간에서 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 통신을 가능하게 한 혁신적 패러다임이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">이 도식은 계단형(Step-index) MMF에서 발생하는 모드 분산 한계를 보여준다.</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Step-Index MMF의 한계: 모드 분산</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">입력 펄스 코어 (균일 굴절률 n1)</div><div class="kb-diagram-cell">출력 펄스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">__ /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\</div><div class="kb-diagram-cell">____</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(모드 1) ──&gt; &gt; (빠름)</div><div class="kb-diagram-cell">/ \</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(모드 2) ──&gt;\/\/\/\/\/\/\/\/\/\/\/\/\&gt; (느림)</div><div class="kb-diagram-cell">/ \</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">‾‾‾‾‾‾ 클래딩 (n2)</div><div class="kb-diagram-cell">‾‾‾‾‾‾‾‾‾‾</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">=&gt; 직선 경로와 반사 경로의 거리 차이로 펄스가 겹침(ISI)</div></div>
</div>
</div>


이 그림의 핵심은 코어 내 [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/)이 일정할 경우 물리적 이동 거리가 긴 외곽 경로(모드 2)의 빛이 늦게 도착하여 펄스 폭이 넓어진다는 점이다. 따라서 전송 속도를 높일수록 인접 펄스와 겹치는 [심볼 상호 간섭](/knowledge-base/studynote/03_network/01_data_communication/022_심볼_상호_간섭_ISI/)(ISI)이 발생해 대역폭이 극도로 제한된다. 실무에서는 이러한 한계 때문에 Step-index MMF를 저속 제어망 이외에는 사용하지 않는다.

- **📢 섹션 요약 비유**: 마치 트랙의 바깥쪽을 뛰는 육상 선수는 불리하지만, 바깥쪽 트랙의 재질을 고속 우레탄으로 깔아주어 안쪽 트랙 선수와 동시에 결승선에 도착하게 만드는 원리와 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

GI-MMF의 구조적 핵심은 [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/)을 포물선 함수([Parabolic](/knowledge-base/studynote/03_network/03_physical_layer_media/176_antenna_yagi_parabolic_patch/) profile)에 따라 정밀하게 도핑하는 데 있다.

| 구성 요소 | 역할 | 내부 동작 메커니즘 | 비유 |
|:---|:---|:---|:---|
| **Core (코어)** | 주 광로 제공 | 중심 [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/) 최대, 반경에 따라 감소 | 속도가 다른 멀티트랙 |
| **Cladding (클래딩)** | 빛의 외부 이탈 방지 | 코어 최외곽보다 낮은 고정 [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/) 유지 | 트랙의 가드레일 |
| **Dopant (도펀트)** | [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/) 프로파일 형성 | GeO2 등을 농도 구배를 주어 첨가 | 트랙의 마찰력 조절제 |
| <strong><a href="/knowledge-base/studynote/03_network/03_physical_layer_media/176_antenna_yagi_parabolic_patch/">Parabolic</a> Profile</strong> | 도달 시간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) | $n(r) = n_1 \sqrt{1 - 2\Delta (r/a)^2}$ 적용 | [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 타이머 |
| **VCSEL 광원** | 고효율 빛 주입 | 표면 발광형 레이저로 특정 모드만 선택적 활성화 | 최적화된 출발 총성 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">이 도식은 GI-MMF 내부의 포물선 굴절률 분포와 빛의 진행 궤적을 보여준다.</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">Graded-Index MMF의 굴절률과 광경로</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">굴절률(n) 프로파일 코어 내부 진행 궤적</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">클래딩 (n2)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">n2 ─ --------------------------------</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">포물선 __ 궤적 A (중심: n 높음 -&gt; v 느림)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">n1 ─ / \ 궤적 B (외곽: n 낮음 -&gt; v 빠름)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">중심반경</div></div>
</div>
</div>


이 흐름의 핵심은 중심을 지나는 빛(궤적 A)은 거리가 짧은 대신 [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/)이 높아 속도가 느리고, 외곽을 도는 빛(궤적 B)은 거리가 긴 대신 [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/)이 낮아 속도가 빠르다는 점이다. 이를 통해 모든 모드의 빛이 주기적으로 교차하며 수신단에 거의 동시에 도달하게 되어 펄스 퍼짐을 상쇄한다. 따라서 수 GHz·km 이상의 넓은 대역폭을 확보할 수 있게 된다. 실무에서는 제조 공정의 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)가 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 좌우한다.

- **📢 섹션 요약 비유**: 곡선 도로에서 굽은 바깥쪽 길을 달리는 자동차에게는 엑셀을 더 밟게 허용해, 직선으로 달리는 차와 똑같은 시간에 목적지에 도착하게 하는 자동 속도 보정 시스템과 같습니다.

---

## Ⅲ. 비교 및 연결

GI-MMF의 포지셔닝을 명확히 하기 위해 다른 광섬유 규격과 정량적으로 비교한다.

| 항목 | Step-Index MMF | Graded-Index MMF | Single-Mode Fiber ([SMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/)) |
|:---|:---|:---|:---|
| **코어 직경** | 50 ~ 100 μm | 50 / 62.5 μm | 8 ~ [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) μm |
| <strong><a href="/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/">굴절률</a> 분포</strong> | 균일 (Uniform) | 포물선형 ([Parabolic](/knowledge-base/studynote/03_network/03_physical_layer_media/176_antenna_yagi_parabolic_patch/)) | 균일 (Uniform) |
| <strong>모드 <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a></strong> | 매우 큼 ([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 심함) | 최소화 (자기 보상) | 없음 (단일 모드) |
| **주 사용 광원** | [LED](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/013_led/) | VCSEL (850nm) | LD (1310/1550nm) |
| **구축 비용** | 매우 낮음 | 낮음 (송수신기 저렴) | 높음 (정밀 정렬 필요) |
| **적용 분야** | 구형 저속 LAN | [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) (OM3/OM4) | 통신사 장거리 백본망 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">이 매트릭스는 대역폭과 전송 거리 측면에서 세 가지 광섬유의 실무적 의사결정 경계를 시각화한다.</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">광섬유 규격별 성능/비용 포지셔닝</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">거리/대역폭 ▲</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">100km+</div><div class="kb-diagram-node">SMF</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">장거리 백본망</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(고가 송수신기 필요)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1km</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">GI-MMF (OM4)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터센터 (10G~100G)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">100m</div><div class="kb-diagram-node">SI-MMF</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">구형망</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">저비용 중간비용 고비용</div></div>
</div>
</div>


이 비교도의 핵심은 GI-MMF가 단일모드([SMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/))의 비싼 광 [트랜시버](/knowledge-base/studynote/03_network/03_physical_layer_media/153_transceiver_mau_sfp/)(Laser [Diode](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/) 및 정밀 패키징) 비용을 절감하면서도 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 내 랙 간 통신(수백 미터)에 필요한 대역폭을 완벽히 충족한다는 점이다. 반면 SMF는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)이 아예 없으므로 장거리 통신에 필수적이나, 광원 정렬에 마이크로미터 단위의 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)가 요구되어 비용이 치솟는다. 따라서 실무 환경의 물리적 반경에 따라 매체를 엄격히 분리 설계해야 한다.

- **📢 섹션 요약 비유**: 동네 마실용 자전거(SI-MMF)와 대륙 횡단용 고속열차([SMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/)) 사이에서, 도심 출퇴근에 최적화된 하이브리드 자동차(GI-MMF)를 선택하는 것과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 구축 시 GI-MMF 규격(OM1 ~ OM5)의 선택은 전체 인프라 투자비(CAPEX)와 향후 확장성에 직결된다.

- **실무 시나리오 1**: 클라우드 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 내 Top-of-Rack [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)와 Spine [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 간 100G 연결. 100m 이내 거리이므로 값비싼 [SMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/) 대신 OM4 등급의 GI-MMF와 100GBASE-SR4 규격을 채택하여 [트랜시버](/knowledge-base/studynote/03_network/03_physical_layer_media/153_transceiver_mau_sfp/) 예산을 수십억 원 절감한다.
- <strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>: GI-MMF에 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/)가 떨어지는 구형 [LED](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/013_led/) 광원을 물리거나 반대로 1550nm 장파장 LD를 무리하게 결합하는 행위. 이는 대역폭의 붕괴와 삽입 손실 확대를 초래하여 링크 페일로 이어진다. VCSEL 기반 850nm 광원에 최적화됨을 명심해야 한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">이 도식은 데이터센터 내 광케이블 등급별 대역폭 한계와 적용 100G 마이그레이션 판별 흐름이다.</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">데이터센터 MMF 마이그레이션 의사결정 플로우</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">요구사항: 스위치 간 링크 구축</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">(거리 &gt; 500m?) ── YES ──&gt;</div><div class="kb-diagram-node">SMF 채택 (OS2/100G-LR4)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">NO</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">v</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">(속도 &gt; 40G?) NO &gt;</div><div class="kb-diagram-node">OM3 채택 (충분한 대역폭)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">YES</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">v</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">OM4 또는 OM5 (SWDM 적용) 채택 및 SR4/SR8 광학모듈 연동</div></div>
</div>
</div>


이 흐름도의 요지는 500m 미만의 구간에서는 무조건 GI-MMF 계열이 채택되며, 속도에 따라 OM3/OM4/OM5의 코어 [정밀도](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/233_precision_recall_f1_roc_auc_threshold/) 등급을 선택해야 한다는 점이다. 특히 100G 이상의 속도에서는 단일 파장으로 한계가 있어 OM5 광섬유에 SWDM(단파장 분할 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) 기술을 얹어 케이블 가닥 수를 줄이는 전략이 실무적으로 권장된다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 배달 거리가 5km 이내인 치킨 배달에 굳이 값비싼 10톤 트럭([SMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/))을 사지 않고, 기동성 좋고 가성비 뛰어난 고속 오토바이(OM4 GI-MMF)를 배차하는 실무적 원가 절감 전략입니다.

---

## Ⅴ. 기대효과 및 결론

GI-MMF는 광통신의 대중화와 [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 패브릭 확장을 견인한 일등 공신이다. 향후 OM5 광대역 멀티모드 광섬유(WBMMF) 규격으로 진화하여 850nm~950nm 파장 대역에서 WDM을 적용, 기존 MMF 한 가닥으로 4배 이상의 용량을 전송하는 방향으로 발전하고 있다. 이는 400G 및 800G [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 환경에서 광케이블 포화 문제를 해결할 핵심 표준(IEEE 802.3cm)으로 자리매김했다.

- **📢 섹션 요약 비유**: 좁은 2차선 도로(OM3)를 넓히지 않고도 자율주행 군집 주행(OM5+SWDM)을 도입해 차량 통행량을 4배로 늘린 교통 혁명과 같습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 모드 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) (Modal [Dispersion](/knowledge-base/studynote/03_network/03_physical_layer_media/133_dispersion_mode_chromatic/)) | GI-MMF가 해결하고자 하는 핵심 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 왜곡 현상 |
| VCSEL 광원 | GI-MMF에 최적화된 표면 발광 레이저 [다이오드](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/011_diode/) |
| OM 규격 (Optical Multimode) | ISO/IEC 11801 기준 MMF [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 등급 |
| 단파장 분할 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) (SWDM) | OM5 GI-MMF에서 용량을 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)하는 융합 기술 |
| [단일모드 광섬유](/knowledge-base/studynote/03_network/03_physical_layer_media/132_single_mode_multi_mode_fiber/) ([SMF](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/771_smf_upf_session_management_user_plane/)) | 모드 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)이 원천 배제된 장거리 전송 경쟁 기술 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: 멀티모드 계단형 광섬유</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: 멀티모드 언덕형 광섬유</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: 단일모드 광섬유 / 다중모드 광섬유</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 고속 광전송 최적화</div></div>
</div>
</div>



멀티모드 언덕형 광섬유는 멀티모드 계단형 광섬유에서 출발해 현재 메커니즘을 정교화하고, 이후 [단일모드 광섬유](/knowledge-base/studynote/03_network/03_physical_layer_media/132_single_mode_multi_mode_fiber/) / 다중모드 광섬유와 고속 광전송 최적화 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 빛의 경주를 하는데, 안쪽 트랙은 거리가 짧고 바깥쪽 트랙은 거리가 길어요.
2. 그냥 달리면 늦게 도착하는 빛 때문에 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)가 뒤죽박죽 엉켜버려요.
3. 그래서 바깥쪽 트랙에 '[초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 매끄러운 바닥(낮은 [굴절률](/knowledge-base/studynote/03_network/03_physical_layer_media/129_refractive_index_tir/))'을 깔아서 모두가 결승선에 똑같이 도착하게 만든 똑똑한 유리관이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 252 / 1120

← **이전**: [130. 멀티모드 계단형 광섬유 (Multi-mode Step-index)](/knowledge-base/studynote/03_network/03_physical_layer_media/130_multimode_step_index_fiber/)
**다음**: [132. 단일모드 광섬유 (Single-mode Fiber, SMF) / 다중모드 광섬유 (MMF)](/knowledge-base/studynote/03_network/03_physical_layer_media/132_single_mode_multi_mode_fiber/) →

---
