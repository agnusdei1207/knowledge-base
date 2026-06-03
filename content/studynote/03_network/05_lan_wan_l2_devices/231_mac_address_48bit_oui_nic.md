+++
title = "231. MAC 주소 (Media Access Control Address)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소는 LAN/WAN과 2계층 장비에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소를 이해하면 스위칭 효율과 브로드캐스트 범위 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층(OSI 2계층)에서 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/), Wi-Fi, [블루투스](/knowledge-base/studynote/03_network/12_iot_wpan_edge/605_bluetooth_ieee_802_15_1_piconet_scatternet/) 등 통신 매체에 접근하는 장비를 유일하게 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하기 위해 사용하는 물리적 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)자다. 16진수 12자리(예: `00:1A:2B:3C:4D:5E`)로 표기된다. [BIA](/knowledge-base/studynote/07_enterprise_systems/04_process_consulting/212_bia_business_impact_analysis_rto_rpo_dr/)(Burned-In Address)라고도 불린다.

- **필요성**: 같은 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)(또는 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/))에 연결된 수십 대의 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 중 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 받아야 할 '진짜 수신자'가 누구인지 알려면 이름표가 필요하다. 만약 이름표가 제조사마다 중첩되거나 사용자가 마음대로 바꾸면 통신 대혼란이 발생하므로, 전 세계 제조사들이 합의하여 겹치지 않는 고정된 번호 체계를 만든 것이 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소다.

- **💡 비유**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소는 자동차의 <strong>"차대 번호(VIN)"나 사람의 "주민등록번호"</strong>와 같습니다. 내가 태어나거나 차가 생산될 때 변하지 않게 부여되는 고유 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/) 번호입니다. 반면 IP 주소는 내가 이사 갈 때마다 바뀌는 "집 주소"나 "우편번호"와 같아서, 우체부(라우터)는 집 주소(IP)를 보고 동네까지 찾아온 뒤, 마지막에 그 집에 사는 사람의 주민등록번호([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고 편지를 줍니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">이더넷 구조 및 원리</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">MAC 주소</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">멀티캐스트 MAC 주소 / 브로드캐스트 MA…</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: <strong> <a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> 주소는 공장에서 찍혀 나오는 </strong>"전자 기기의 지문"**입니다. [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)라는 지문 인식기는 이 지문을 보고 정확히 그 기기에게만 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 택배를 건네줍니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 48비트 구조의 분할
IEEE가 관리하는 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소의 48비트(6바이트)는 정확히 절반으로 나뉘어 관리된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">MAC 주소 48비트 구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">16진수 표기: 00 : 1A : 2B : 3C : 4D : 5E</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">24 bit 24 bit</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">의미:</div><div class="kb-diagram-node">OUI (제조사 번호)</div><div class="kb-diagram-node">NIC 특정 일련번호</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- OUI (Organizationally Unique Identifier):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">IEEE가 애플, 인텔, 삼성 등 각 제조사에게 돈을 받고 할당함.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- NIC Specific (UAA: Universally Administered Address):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">제조사가 생산 라인에서 1씩 증가시키며 찍어내는 고유 시리얼.</div></div>
</div>
</div>



### 2. 주소의 관리와 고갈 문제
- 24비트 일련번호는 $2^{24}$ = 약 1,677만 개의 기기를 생산할 수 있다. 큰 제조사는 1,677만 대를 넘게 생산하므로, OUI를 여러 개 구매하여 사용한다. (예: 애플은 수십 개의 OUI를 보유)
- 전체 48비트는 $2^{48}$ = 약 281조 개의 주소 공간을 가지므로, IPv4와 달리 당분간 고갈될 우려는 없다.

### 3. I/G (Individual/Group) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)와 U/L [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)
[MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소의 가장 첫 번째 바이트를 이진수로 풀었을 때, 첫 번째와 두 번째 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)는 특별한 용도로 쓰인다.
- <strong>I/G <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> (최하위 <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a>, b0)</strong>: 0이면 단일 기기(Unicast), 1이면 다수 기기(Multicast)를 의미한다. (예: 브로드캐스트 `FF:FF...`는 모두 1이므로 1이다)
- <strong>U/L <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> (b1)</strong>: 0이면 전 세계 고유(Universally Administered), 1이면 로컬 관리자(사용자)가 임의로 바꾼 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)(Locally Administered)을 의미한다.

- **📢 섹션 요약 비유**: <strong> <a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> 주소의 OUI는 </strong>"자동차 브랜드 마크(현대, 벤츠)"**이고, 뒤의 24비트는 공장에서 찍어낸 **"순서 번호"**입니다. 이 두 개를 조합하면 지구상의 어떤 자동차도 완벽하게 구별해 낼 수 있습니다.

---

## Ⅲ. 비교 및 연결

[MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 구조 및 원리가 기반 조건을 만든다면, [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소는 그 위에서 핵심 메커니즘을 구현하고, [멀티캐스트](/knowledge-base/studynote/03_network/06_network_layer_ip/298_ip_classes_a_b_c_d_multicast_e_experimental/) [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 / 브로드캐스트 MA…는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 구조 및 원리의 기반 정리 | [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소의 핵심 동작 | [멀티캐스트](/knowledge-base/studynote/03_network/06_network_layer_ip/298_ip_classes_a_b_c_d_multicast_e_experimental/) [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 / 브로드캐스트 MA…의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 구조 및 원리 수준의 기본 대책으로 충분한지, 아니면 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [멀티캐스트](/knowledge-base/studynote/03_network/06_network_layer_ip/298_ip_classes_a_b_c_d_multicast_e_experimental/) [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 / 브로드캐스트 MA…와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 스위칭 효율 부족인지, 브로드캐스트 범위 악화인지 먼저 분리한다.
2. [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [멀티캐스트](/knowledge-base/studynote/03_network/06_network_layer_ip/298_ip_classes_a_b_c_d_multicast_e_experimental/) [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 / 브로드캐스트 MA…와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 구조 및 원리와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소는 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [멀티캐스트](/knowledge-base/studynote/03_network/06_network_layer_ip/298_ip_classes_a_b_c_d_multicast_e_experimental/) [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 / 브로드캐스트 MA…, 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 구조 및 원리 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/)하는 기본 주소다. |
| [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 포트로 전달하는 핵심 장비다. |
| [멀티캐스트](/knowledge-base/studynote/03_network/06_network_layer_ip/298_ip_classes_a_b_c_d_multicast_e_experimental/) [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 / 브로드캐스트 MA… | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: 이더넷 구조 및 원리</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: MAC 주소</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: 멀티캐스트 MAC 주소 / 브로드캐스트 MA…</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 지능형 캠퍼스 패브릭</div></div>
</div>
</div>



[MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소는 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 구조 및 원리에서 출발해 현재 메커니즘을 정교화하고, 이후 [멀티캐스트](/knowledge-base/studynote/03_network/06_network_layer_ip/298_ip_classes_a_b_c_d_multicast_e_experimental/) [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 / 브로드캐스트 MA…와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 352 / 1120

← **이전**: [230. 이더넷 (Ethernet) 구조 및 원리 (IEEE 802.3)](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)
**다음**: [232. 멀티캐스트 MAC 주소 / 브로드캐스트 MAC 주소 (FF:FF:FF:FF:FF:FF)](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/232_multicast_broadcast_mac_address/) →

---
