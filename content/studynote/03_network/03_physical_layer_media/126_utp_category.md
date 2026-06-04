+++
title = "126. UTP 카테고리 (Cat 3, Cat 5, Cat 5e, Cat 6, Cat 6a, Cat 7, Cat 8)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) ([Unshielded Twisted Pair](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/)) 케이블은 두 가닥의 구리선을 꼬아 전자기 간섭을 상쇄하는 원리로 작동하며, 카테고리는 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 전송 속도를 결정하는 규격이다.
> 2. **가치**: 10Mbps(Cat 3)에서 40Gbps(Cat 8)까지 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)([Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/))의 물리적 전송 한계를 확장하며, LAN(Local Area Network) 인프라 구축의 경제성과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 좌우한다.
> 3. **판단 포인트**: [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송뿐만 아니라, [PoE](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/265_poe_power_over_ethernet/) ([Power over Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/265_poe_power_over_ethernet/)) 기술과 융합되어 전력과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 동시에 공급하는 스마트 빌딩 인프라의 핵심으로 작용한다.

---

## Ⅰ. 개요 및 필요성

[UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) ([Unshielded Twisted Pair](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/)) 케이블은 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)([Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)) 통신의 가장 기본적인 전송 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)이다. 구리선을 타고 흐르는 전기 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)는 외부 전자기파나 인접한 선에서 발생하는 [누화](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/)([Crosstalk](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/), 혼선)에 취약하다. 이를 극복하기 위해 두 선을 나선형으로 꼬아(Twisted) [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)의 간섭을 물리적으로 상쇄시키는 원리가 도입되었다. 네트워크 환경이 10Mbps에서 기가비트(Gigabit)를 넘어 10Gbps 이상으로 발전함에 따라, 더 높은 주파수 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)([Bandwidth](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))을 수용하고 간섭을 억제하기 위해 피치(Pitch, 꼬임 간격)를 조밀하게 하고 차폐(Shielding) 기술을 더한 카테고리(Category) 등급이 지속적으로 제정되었다.

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 속도의 기하급수적 증가는 단순한 구리선에 한계를 가져왔다. 고주파 대역일수록 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 감쇠(Attenuation)와 간섭이 심해지기 때문이다. 따라서 실무와 시스템에서는 네트워크 장비([스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/), 라우터)의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 병목 없이 종단(End-point)까지 전달하기 위해, [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 요구사항에 맞는 적절한 카테고리의 케이블을 선택하는 것이 필수적이다.

다음은 꼬임선(Twisted Pair)이 어떻게 전자기 간섭을 상쇄하는지 보여주는 원리도이다.

```text
[외부 전자기파 간섭(EMI)]
       v   v   v   v
    +--+---+---+---+---+--+  (선 A: + 신호)
    |   \ /     \ /     \ |
    |    X       X       X|  => 위상이 반대인 두 신호가 꼬인 지점마다 간섭을 스위칭
    |   / \     / \     / |
    +--+---+---+---+---+--+  (선 B: - 신호)
       ^   ^   ^   ^
[인접 선로의 누화(Crosstalk)]
```
*이 그림의 핵심은 평행한 두 선 대신 꼬인 선을 사용함으로써, 외부 간섭이 두 선에 동일하게 미치더라도 수신단에서 두 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)의 차이(Differential Signaling)를 계산할 때 노이즈가 수학적으로 상쇄된다는 점이다. 이러한 배치는 별도의 차폐재 없이도 일정 수준의 노이즈 내성을 제공하며, 꼬임이 촘촘할수록 고주파 간섭을 더 잘 방어한다. 따라서 케이블 등급이 올라갈수록 단위 길이당 꼬임 횟수(Pitch)가 증가하여 제조 단가와 굵기에 영향을 준다.*

- **📢 섹션 요약 비유**: 마치 여러 사람이 떠드는 시끄러운 방에서, 두 귀의 위치 차이를 이용해 잡음을 걸러내고 상대방의 목소리만 명확히 듣는 뇌의 필터링 시스템과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) 케이블 카테고리는 주파수 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)과 꼬임의 조밀도, 차폐재(Shield) 유무에 따라 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 결정된다. 내부적으로는 4쌍(8가닥)의 구리선으로 구성되며, 송신(TX)과 수신(RX)을 담당한다.

| 구성 요소 | 역할 | 내부 동작 | [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 지원 | 비유 |
|:---|:---|:---|:---|:---|
| **Cat 5e** | 기가비트 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 대중화 | 100MHz 주파수 대역 사용, 4쌍 모두 활용 | [1000BASE-T](/knowledge-base/studynote/03_network/03_physical_layer_media/139_1000base_t_gigabit_ethernet/) | 왕복 4차선 일반 국도 |
| **Cat 6** | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 10G [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 지원 | 250MHz 주파수, 내부 십자형(Cross-web) 개재 삽입 | [1000BASE-T](/knowledge-base/studynote/03_network/03_physical_layer_media/139_1000base_t_gigabit_ethernet/), 10GBASE-T (단거리) | 왕복 8차선 고속도로 |
| **Cat 6a** | 완벽한 10G [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 지원 | 500MHz 주파수, 에일리언 크로스토크(AXT) 방어 강화 | 10GBASE-T (100m) | 방음벽이 설치된 고속도로 |
| **Cat 7** | 차폐([STP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/)) 강제, 고대역폭 | 600MHz 주파수, 개별 쌍마다 호일 차폐(S/[FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/)) 적용 | 10GBASE-T, 전용 규격 | 터널로 보호된 특수 철도 |
| **Cat 8** | 25G/40G [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 전송 | 2000MHz(2GHz) 주파수, 극한의 차폐, 최대 30m | 25GBASE-T, 40GBASE-T | 단거리 자기부상열차 |

다음은 케이블 등급 상향에 따른 내부 물리적 구조의 진화 과정을 나타낸 구조도이다.

```text
+-----------------+ +-----------------+ +-----------------+
|     Cat 5e      | |      Cat 6      | |   Cat 7 / 8     |
|  (UTP 구조)     | |  (Cross-web)    | |   (S/FTP 구조)  |
+-----------------+ +-----------------+ +-----------------+
|                 | |                 | | +-[외곽 편조 Shield]-+
|  (쌍 1)  (쌍 2) | | (쌍 1) | (쌍 2) | | | [F]|[F] |
|                 | | --- 십자 개재 --| | | ---+--- |
|  (쌍 3)  (쌍 4) | | (쌍 3) | (쌍 4) | | | [F]|[F] |
|                 | |                 | | +---------------+
+-----------------+ +-----------------+ +-----------------+
 * F = Foil Shield (개별 쌍 호일 차폐)
```
*이 구조도의 핵심은 주파수 대역이 높아질수록 내부 선간의 [누화](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/)(NEXT)를 방지하기 위해 십자 개재(Cross-web)를 넣거나(Cat 6), 개별 쌍을 호일로 감싸는(S/[FTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/), Cat 7/8) 물리적 격리가 추가된다는 점이다. 이런 배치는 전기적 간섭을 물리적으로 차단하기 때문이며, 따라서 케이블의 굵기가 두꺼워지고 유연성이 떨어져 곡률 반경(Bending [Radius](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/541_radius_remote_authentication_aaa/)) 확보가 어려워져 포설 작업의 난이도에 영향을 준다. 실무에서는 제한된 배관 공간 내에 다수의 선을 매설해야 할 때 UTP와 STP의 외경 차이를 반드시 고려해야 한다.*

고주파 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)를 전송할 때 발생하는 주요 물리적 감쇠 요인은 다음과 같다:
1. <strong>NEXT (Near-End <a href="/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/">Crosstalk</a>)</strong>: 송신 측에서 인접한 쌍으로 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)가 유도되어 발생하는 근단 [누화](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/).
2. <strong>FEXT (Far-End <a href="/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/">Crosstalk</a>)</strong>: 수신 측에서 측정되는 원단 [누화](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/).
3. <strong>AXT (Alien <a href="/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/">Crosstalk</a>)</strong>: 다발로 묶인 다른 케이블에서 넘어오는 외인성 [누화](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/) (Cat 6a 이상에서 주요 방어 대상).

- **📢 섹션 요약 비유**: 좁은 차선에서 차들이 빨리 달릴수록 바람(전자기장)이 서로 영향을 미치는데, 이를 막기 위해 중앙분리대(십자 개재)를 세우고 방음 터널(차폐 호일)을 덮는 과정과 같습니다.

---

## Ⅲ. 비교 및 연결

현대 엔터프라이즈 환경에서 주로 고려되는 Cat 5e, Cat 6, Cat 6a의 정량적 비교이다.

| 항목 | Cat 5e | Cat 6 | Cat 6a | 판단 포인트 |
|:---|:---|:---|:---|:---|
| **최대 속도** | 1 Gbps | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) Gbps (단거리) / 1 Gbps | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) Gbps | 미래 트래픽 요구량 |
| <strong>최대 <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a></strong> | 100 MHz | 250 MHz | 500 MHz | [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 한계 |
| **10G 전송 거리**| 불가 | 최대 37~55m | 최대 100m | 서버룸 vs 사무실 포설 |
| **차폐 구조** | [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) | [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) (십자 개재 포함) | [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) / F/[UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) | 공사 난이도 및 굵기 |
| **도입 비용** | 매우 낮음 | 낮음 | 중간 | 전체 인프라 예산 |

**Cat 7 vs Cat 8 관점**
| 항목 | Cat 7 | Cat 8 | 판단 포인트 |
|:---|:---|:---|:---|
| **최대 속도** | [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) Gbps | 25/40 Gbps | [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 간 연결 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a></strong> | 600 MHz | 2000 MHz (2GHz) | 초고주파 감쇠 제어 |
| **최대 거리** | 100m | 30m | 랙(Rack) 간 통신(ToR) 여부 |
| **커넥터** | GG45 / TERA 권장 | RJ45 하위호환 가능 | [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 규격 일치 |

Cat 6 방식은 저렴하게 1Gbps를 구성할 수 있으나, 향후 10Gbps로 증속 시 55m라는 거리 제한이 걸려 층간 연결에서 병목이 발생할 수 있다. 반면 Cat 6a는 100m까지 10Gbps를 보장하여 인프라 수명을 늘려주지만, 케이블 외경이 두꺼워 기존 배관(Conduit)에 수용 가능한 케이블 가닥 수가 줄어드는 오버헤드가 발생한다.

- **📢 섹션 요약 비유**: 시내 주행용 소형차(Cat 5e), 국도 범용 중형차(Cat 6), 고속도로 전용 대형차(Cat 6a), 단거리 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 로켓(Cat 8)을 목적과 도로 폭에 맞춰 고르는 것과 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 네트워크 인프라 설계 시 케이블 카테고리 선정은 장비보다 교체 주기가 긴 물리 계층(L1)의 결정이므로 매우 신중해야 한다.

다음은 신규 사무실/[데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 구축 시 케이블 등급을 선택하는 실무 의사결정 트리이다.

```text
[구축 대상 및 용도 확인]
           |
           +--> (데이터센터 내 랙(Rack) 간 25G/40G 단거리 연결인가?) -- Yes ---> [Cat 8 또는 DAC/광케이블 선택]
           |
           No
           |
           v
[10Gbps 보장 및 수명 요구사항]
           |
           +--> (10년 이상 사용하며 10G 완벽 보장이 필요한가?) -- Yes ---> [Cat 6a 선택] (※ 배관 내경 20% 이상 여유 확인)
           |
           No
           |
           v
[단말기 특성 및 예산]
           |
           +--> (AP, CCTV, 일반 PC 위주이며 가성비가 중요한가?) -- Yes ---> [Cat 6 선택]
           |
           v
[PoE (Power over Ethernet) 고려]
 * 60W 이상 고전력 PoE++ 인가 시, 발열로 인한 저항 증가 방지를 위해 최소 Cat 6 이상 권장
```
*이 흐름의 핵심은 케이블 선택이 단순히 속도의 문제가 아니라, 전송 거리(100m vs 30m)와 물리적 배관 크기, 발열([PoE](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/265_poe_power_over_ethernet/))을 종합적으로 고려한 결과물이어야 한다는 점이다. 특히 [PoE](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/265_poe_power_over_ethernet/)++를 사용할 경우 저사양 케이블(Cat 5e)은 발열로 인해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 패킷 손실([저항](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance/) 증가)이라는 치명적인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 유발한다. 실무에서는 "무조건 높은 등급"이 정답이 아니며, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 업링크 구간은 광케이블로 분리하고 액세스 구간만 UTP로 구성하는 하이브리드 전략이 자원 효율 측면에서 가장 유리하다.*

<strong>실무 <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a> (치명적 <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/">결함</a> 사례)</strong>
- <strong>Cat 6a <a href="/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/">UTP</a> 케이블을 좁은 배관에 억지로 쑤셔 넣기</strong>: 케이블 꺾임(Bending) 한계를 초과하여 내부 꼬임이 풀리고 NEXT가 급증, 10Gbps 링크가 1Gbps로 [폴백](/knowledge-base/studynote/07_enterprise_systems/03_eai_esb_msa/171_fallback_resilience_pattern/)([Fallback](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/129_fallback/))되는 현상 발생.
- **RJ45 플러그 규격 불일치**: Cat 6a 케이블에 Cat 5e용 RJ45 플러그를 집을 경우, 커넥터 접점부에서 [임피던스](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/004_impedance/) 불일치([Impedance](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/004_impedance/) Mismatch)가 발생하여 전체 링크 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 Cat 5e 수준으로 하향 동기화됨.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 수도관을 묻을 때 당장 쓸 물의 양만 보고 얇은 관(Cat 5e)을 묻으면 나중에 수압(트래픽)을 올릴 때 땅을 다시 파야 하지만, 너무 굵은 관(Cat 6a)은 기존 하수도 배관에 들어가지 않아 공사비가 폭증하는 딜레마와 같습니다.

---

## Ⅴ. 기대효과 및 결론

[UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) 케이블은 카테고리 진화를 통해 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 표준(IEEE 802.3)과 함께 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 한계를 꾸준히 극복해왔다.

| 지표 | 도입 전 (Legacy Cat 5e 위주) | 도입 후 (Cat 6a / Cat 8 활용) |
|:---|:---|:---|
| <strong>내부망 <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/">대역폭</a></strong> | 1 Gbps 병목으로 대용량 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [전송 지연](/knowledge-base/studynote/03_network/01_data_communication/017_전송_지연/) | 10G/40G 인프라로 원활한 클라우드 및 스토리지 접근 |
| <strong>설비 수명 (<a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/807_roi_return_on_investment/">ROI</a>)</strong> | 3~5년 후 케이블 재포설 비용 발생 | 10년 이상 추가 공사 없이 네트워크 장비만 교체하여 업그레이드 |
| <strong><a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/265_poe_power_over_ethernet/">PoE</a> <a href="/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/">호환성</a></strong> | 고전력 장비(PTZ 카메라, 최신 [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/)) 발열 문제 | 굵은 심선을 통한 안정적인 전력 공급([PoE](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/265_poe_power_over_ethernet/)++) 및 장애율 감소 |

**미래 전망**
구리선을 이용한 40Gbps(Cat 8)는 물리적 주파수 한계(2GHz)와 거리 한계(30m)에 도달했다. 향후 더 높은 속도(100Gbps 이상)는 종단간 [광섬유 케이블](/knowledge-base/studynote/03_network/03_physical_layer_media/128_optical_fiber_cable/)(Fiber-to-the-Desk)로 대체되거나, 단일 랙 내에서는 DAC ([Direct](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) Attach Copper) 케이블이 주류가 될 것이다. 그러나 설치의 편의성과 PoE를 통한 전원 통합 공급 능력 때문에, 말단 액세스망(Access Network)에서 [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) 케이블(Cat 6/6a)의 지위는 향후 10년 이상 흔들리지 않을 것이다.

- **📢 섹션 요약 비유**: 비록 우주선(광케이블) 시대가 열렸어도, 집 문 앞까지 택배를 배달하는 것은 여전히 튼튼하고 실용적인 트럭([UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) 케이블)인 것과 같습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) ([Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)) | [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) 케이블을 물리적 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)로 사용하는 IEEE 802.3 기반의 LAN 핵심 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
| 크로스토크 ([Crosstalk](/knowledge-base/studynote/03_network/01_data_communication/030_누화_크로스토크/)) | 인접한 구리선 간의 전자기적 간섭 현상으로 카테고리 진화의 주된 극복 대상 |
| [PoE](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/265_poe_power_over_ethernet/) ([Power over Ethernet](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/265_poe_power_over_ethernet/)) | [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) 케이블의 남는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 선이나 동일 선에 직류 전력을 실어 보내는 기술 |
| [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) Address) | [UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) 케이블을 통해 프레임을 전송할 때 사용하는 2계층 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 주소 체계 |
| [광섬유 케이블](/knowledge-base/studynote/03_network/03_physical_layer_media/128_optical_fiber_cable/) (Optical Fiber) | UTP의 전송 거리와 속도 한계를 극복하기 위해 빛을 이용하는 백본망 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: STP / FTP]
    |
    v
[현재 개념: UTP 카테고리]
    |
    +---> [확장 A: 동축 케이블]
    +---> [확장 B: 고속 광전송 최적화]
```

[UTP](/knowledge-base/studynote/03_network/03_physical_layer_media/124_unshielded_twisted_pair/) 카테고리는 [STP](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/570_stp_vs_mtp/) / FTP에서 출발해 현재 메커니즘을 정교화하고, 이후 동축 케이블와 고속 광전송 최적화 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 인터넷 선 안에는 구리선들이 머리 땋듯이 꼬여 있는데, 이렇게 꼬아놓으면 주변의 나쁜 전기파 잡음을 스스로 막아낼 수 있어요.
2. 옛날 선(Cat 5)은 헐겁게 꼬여 있어서 조금만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 많이 보내면 막혔지만, 최신 선(Cat 8)은 아주 촘촘하게 꼬여 있고 은박지 이불까지 덮고 있어서 엄청나게 빨리 보낼 수 있어요.
3. 하지만 최신 선은 너무 두껍고 뻣뻣해서 좁은 구멍에 넣기 힘들기 때문에, 우리가 컴퓨터를 어디서 얼마나 빨리 쓸지에 맞춰서 알맞은 두께의 선을 골라야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 247 / 1120

<- **이전**: [125. STP (Shielded Twisted Pair) / FTP (Foil Twisted Pair)](/knowledge-base/studynote/03_network/03_physical_layer_media/125_shielded_foil_twisted_pair/)
**다음**: [127. 동축 케이블 (Coaxial Cable)](/knowledge-base/studynote/03_network/03_physical_layer_media/127_coaxial_cable/) ->

---
