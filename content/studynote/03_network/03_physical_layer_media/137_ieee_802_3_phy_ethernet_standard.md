+++
title = "137. 이더넷 물리 계층 표준 (IEEE 802.3 PHY)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 물리 계층 표준은 물리 계층과 전송 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 물리 계층 표준을 이해하면 감쇠과 전송 거리 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

<strong>IEEE 802.3</strong>은 유선 LAN(Local Area Network)의 대표적인 기술인 <strong><a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">이더넷</a>(<a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">Ethernet</a>)</strong>의 물리 계층(Physical Layer)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층의 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 서브계층을 정의하는 국제 표준입니다. 

네트워크에서 장비들이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받으려면 전기적 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)의 [전압](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/), 케이블의 핀 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/), 빛의 파장 등이 정확히 일치해야 하는데, 이를 통일시켜 서로 다른 제조사의 장비(시스코 라우터와 인텔 랜카드 등)가 완벽히 호환되도록 만드는 것이 PHY 표준의 역할입니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">자유 공간 광통신 / 레이저 통신</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">이더넷 물리 계층 표준</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">10BASE-T, 100BASE-TX</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 물리 계층 표준은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 물리 계층의 표준 이름은 직관적인 규칙에 따라 작성됩니다.  
규칙: <strong><code>[속도] [전송 방식] - [매체 또는 거리]</code></strong>



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">100 BASE - TX</div>
<div class="kb-diagram-note">① 속도(Speed) ② 전송 방식 ③ 매체 특성 (Medium)</div>
</div>
</div>



### 1. 속도 (Speed)
숫자는 기본적으로 **Mbps(Megabits per second)** 단위입니다.
- `10` : [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) Mbps
- `100` : 100 Mbps ([Fast Ethernet](/knowledge-base/studynote/03_network/03_physical_layer_media/138_10base_t_100base_tx_fast_ethernet/))
- `1000` : 1,000 Mbps = 1 Gbps ([Gigabit Ethernet](/knowledge-base/studynote/03_network/03_physical_layer_media/139_1000base_t_gigabit_ethernet/))
- `10G` : [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) Gbps

### 2. 전송 방식 (Signaling)
- `BASE` : <strong><a href="/knowledge-base/studynote/03_network/19_frequent_topics_terms/940_baseband_line_coding_nrz_rz_manchester/">Baseband</a> (<a href="/knowledge-base/studynote/03_network/19_frequent_topics_terms/940_baseband_line_coding_nrz_rz_manchester/">기저대역</a>)</strong> 전송. 디지털 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 변조하지 않고 원래 주파수 그대로 케이블에 싣는 방식입니다. [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)은 대부분 BASE를 사용합니다.
- `BROAD` : Broadband (대역통과) 전송 (과거 [동축 케이블](/knowledge-base/studynote/03_network/03_physical_layer_media/127_coaxial_cable/) 등에서 사용, 현재 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)에선 거의 안 씀).

### 3. [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 또는 거리 특성 (Medium / Distance)
어떤 케이블을 쓰는지, 얼마나 멀리 가는지 나타냅니다.
- `T` (Twisted Pair): [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) 등 [꼬임 쌍선 케이블](/knowledge-base/studynote/03_network/03_physical_layer_media/123_twisted_pair_cable/) (예: 10BASE-T)
- `X` : 8B/10B 또는 4B/5B 같은 블록 인코딩을 사용하는 케이블 (예: 100BASE-TX)
- `C` (Coaxial): 구형 [동축 케이블](/knowledge-base/studynote/03_network/03_physical_layer_media/127_coaxial_cable/) (예: 10BASE2, 여기서 2는 약 200m)
- `S` (Short): 단파장 광케이블, 단거리 (예: 1000BASE-SX)
- `L` (Long): 장파장 광케이블, 장거리 (예: 1000BASE-LX)
- `E` (Extended): 초장거리 광케이블 (예: 1000BASE-ZX)

- **📢 섹션 요약 비유**: <strong> <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/">이더넷</a> 명명법은 </strong>"100km/h로(100), 일반도로를(BASE), 트럭(T)으로 달린다"**처럼 차량의 제원표를 읽는 것과 같아, 이름만 보고도 연결 방식을 단번에 알 수 있습니다.

---

## Ⅲ. 비교 및 연결

네트워크 카드([NIC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/587_nic_offloading/)) 내부에는 <strong>PHY 칩</strong>과 <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> 칩</strong>이 존재합니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">NIC (Network Interface Card)</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MII/GMII</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MAC Chip</div><div class="kb-diagram-cell">◀ ▶</div><div class="kb-diagram-cell">PHY Chip</div><div class="kb-diagram-cell">◀ ▶</div><div class="kb-diagram-cell">RJ-45 / SFP</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(Layer 2)</div><div class="kb-diagram-cell">Interface</div><div class="kb-diagram-cell">(Layer 1)</div><div class="kb-diagram-cell">MDI</div><div class="kb-diagram-cell">Connector</div></div>
<div class="kb-diagram-note">UTP / 광케이블</div>
</div>
</div>



1. **MAC과 PHY의 분리**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 칩은 프레임을 조립/분해하는 논리적 작업(L2)을 하고, PHY 칩은 이 프레임을 1과 0의 전기적/광학적 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)로 바꾸는 물리적 작업(L1)을 수행합니다.
2. **MII / GMII 인터페이스**: MAC과 PHY 칩 사이의 통신 규격입니다. ([Media](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) Independent Interface)
3. <strong>MDI (<a href="/knowledge-base/studynote/03_network/03_physical_layer_media/142_mdi_mdix_interface/">Medium Dependent Interface</a>)</strong>: PHY 칩에서 랜선이 꽂히는 RJ-45 포트로 나가는 최종 물리적 인터페이스입니다.

- **📢 섹션 요약 비유**: [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 물리 계층 표준은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

| 규격 이름 | 속도 | 케이블 타입 | 주요 특징 |
| :--- | :--- | :--- | :--- |
| **10BASE-T** | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) Mbps | Cat 3 [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) | 최초로 RJ-45와 [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) 케이블을 대중화시킨 스타 토폴로지 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/). |
| **100BASE-TX** | 100 Mbps | Cat 5 [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) | <strong><a href="/knowledge-base/studynote/03_network/03_physical_layer_media/138_10base_t_100base_tx_fast_ethernet/">Fast Ethernet</a></strong>. 4B/5B 인코딩과 MLT-3 스킴을 사용하여 100Mbps 달성. |
| <strong><a href="/knowledge-base/studynote/03_network/03_physical_layer_media/139_1000base_t_gigabit_ethernet/">1000BASE-T</a></strong> | 1 Gbps | Cat 5e [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) | <strong><a href="/knowledge-base/studynote/03_network/03_physical_layer_media/139_1000base_t_gigabit_ethernet/">Gigabit Ethernet</a></strong>. 4쌍(8가닥)의 선을 모두 양방향으로 동시 송수신. PAM-5 변조 사용. |
| **10GBASE-T** | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) Gbps | Cat 6a [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) | 구리선 한계 극복을 위해 복잡한 DSP와 PAM-16을 사용, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 센터 위주 도입. |

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: ** [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)은 과거 1차선 흙길([동축 케이블](/knowledge-base/studynote/03_network/03_physical_layer_media/127_coaxial_cable/))에서 시작해, 이제는 16차선 고속도로(10GBASE-T)와 빛의 속도로 달리는 텔레포트 게이트(광 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))로 끝없이 진화하고 있는 도로망 건설의 역사입니다.

---

## Ⅴ. 기대효과 및 결론

[이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 물리 계층 표준은 물리 계층과 전송 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 감쇠 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 10BASE-T, 100BASE-TX, 고속 광전송 최적화, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 고속 광전송 최적화 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 물리 계층 표준은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [자유 공간 광통신](/knowledge-base/studynote/03_network/03_physical_layer_media/136_fso_free_space_optics_laser/) / 레이저 통신 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 감쇠 (Attenuation) | 거리 증가에 따라 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 세기가 줄어드는 문제다. |
| 변조 (Modulation) | [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 특성에 맞춰 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 실어 나르는 방법이다. |
| 10BASE-T, 100BASE-TX | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: 자유 공간 광통신 / 레이저 통신</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: 이더넷 물리 계층 표준</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: 10BASE-T, 100BASE-TX</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 고속 광전송 최적화</div></div>
</div>
</div>



[이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 물리 계층 표준는 [자유 공간 광통신](/knowledge-base/studynote/03_network/03_physical_layer_media/136_fso_free_space_optics_laser/) / 레이저 통신에서 출발해 현재 메커니즘을 정교화하고, 이후 10BASE-T, 100BASE-TX와 고속 광전송 최적화 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 실을 통해 전화기를 만들 때 실이 길거나 약하면 목소리가 잘 안 들려요.
2. 이 개념은 어떤 실이나 파이프가 말을 더 멀리 잘 보내는지 알려줘요.
3. 덕분에 상황에 맞는 선과 장비를 골라 더 멀리, 더 빠르게 보낼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 258 / 1120

← **이전**: [136. 자유 공간 광통신 (FSO, Free Space Optics) / 레이저 통신](/knowledge-base/studynote/03_network/03_physical_layer_media/136_fso_free_space_optics_laser/)
**다음**: [138. 10BASE-T, 100BASE-TX (Fast Ethernet)](/knowledge-base/studynote/03_network/03_physical_layer_media/138_10base_t_100base_tx_fast_ethernet/) →

---
