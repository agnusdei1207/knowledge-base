+++
title = "242. 스위칭 방식"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 컷스루 (Cut-through) 스위칭은 들어오는 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 프레임을 끝까지 다 받기도 전에, 프레임 맨 앞의 <strong>목적지 <a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> 주소(앞 6바이트)만 딱 읽고 곧바로 포워딩을 시작하는 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/">초고속</a> 전송 방식</strong>이다.
> 2. **가치**: 프레임 전체가 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 내부 버퍼로 들어오길 기다릴 필요가 없으므로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)를 통과할 때 발생하는 [전송 지연](/knowledge-base/studynote/03_network/01_data_communication/017_전송_지연/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))이 3가지 [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/) 중 가장 짧다(가장 빠르다).
> 3. **판단 포인트**: 에러가 발생했는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 FCS 필드가 프레임 맨 끝에 있기 때문에, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 에러 여부를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하기도 전에 이미 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 밖으로 쏘아버린 상태가 된다. 즉, 깨진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(에러)까지도 그대로 전달해 버리는 치명적 단점이 있다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 입력 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에서 출력 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 넘겨줄 때(Switching), "얼마만큼 읽어보고 넘길 것인가?"를 결정하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 중 하나다. 컷스루 방식은 목적지 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소까지만 수신하면 즉시 내보내기 시작한다.
- **필요성**: 금융권의 초단타 매매(HFT) 네트워크나 고성능 컴퓨팅([HPC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/)) 환경에서는 0.001초(밀리초) 단위의 레이턴시 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)도 막대한 손실로 이어진다. 이런 환경에서는 프레임 전체를 메모리에 담는 시간조차 아까우므로, 무조건 1순위로 "빨리 넘기는 것"이 필요했다.

- **💡 비유**: 컷스루는 <strong>"수업 시간 쪽지 전달"</strong>과 같습니다. 뒤에서 넘어온 쪽지를 펼쳐서 내용이 맞는지 틀린지 끝까지 다 읽어보지 않고, 겉면에 적힌 <strong>"철수에게"라는 이름만 보고 즉시 앞자리 철수에게 휙 던져주는 것</strong>입니다. 속도는 제일 빠르지만, 쪽지 내용이 찢어져 있어도 그대로 전달하고 맙니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">에이징 / 포트 미러링</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스위칭 방식</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">스위칭 방식</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: <strong> 컷스루 <a href="/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/">스위치</a>는 물류 창고에서 택배 박스의 </strong>"송장(목적지 주소)만 스캔하자마자 컨베이어 벨트를 멈추지 않고 바로 배송 트럭으로 밀어 넣는 초스피드 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 시스템"**입니다. 내용물 파손 여부는 아예 검사하지 않습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 최소 대기 시간: 14 Bytes
[이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 프레임의 맨 앞은 Preamble(8B) → 목적지 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)(6B) → 출발지 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)(6B) 순으로 들어온다.
- 컷스루 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)는 Preamble로 박자를 맞추고, 바로 뒤따라오는 <strong>목적지 <a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> 주소 6바이트만 읽자마자</strong> 자신의 CAM 테이블을 뒤져 출력 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)(예: 3번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))를 찾아낸다.
- 그리고 나머지 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(출발지 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/), 페이로드, FCS)가 아직 [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 안으로 질금질금 들어오고 있는 와중에, 앞머리를 이미 3번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 뿜어내기 시작한다(Streaming).



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">컷스루 (Cut-through) 동작 도식</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. 프레임이 스위치로 들어옴 (오른쪽에서 왼쪽으로 이동)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">FCS(4B) | Payload(1500B) | 출발지 MAC(6B) | 목적지 MAC(6B)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">이만큼만</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스위치가 수신</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. 목적지 MAC(6B)을 읽은 직후 (스위치 내부)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">스위치: "오케이, 목적지 확인 완료. 에러 검사 안 함. 바로 출발시켜!"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. 프레임이 출력 포트로 나가기 시작 (동시 진행)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">들어오는 중인 꼬리부분 ──▶ 스위치 ──▶ 이미 나가고 있는 머리부분</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">FCS | Payload ...             ... 출발지 MAC | 목적지 MAC</div></div>
</div>
</div>



### 2. 레이턴시([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))와 에러율의 Trade-off
- <strong>장점 (가장 낮은 <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>시간)</strong>: 프레임 크기가 최소 64바이트든 최대 1518바이트든 상관없이, [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)가 묶어두는 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간은 목적지 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소를 읽는 짧은 시간에 불과하여 항상 일정하고 빠르다.
- **단점 (오류 확산)**: 회선 품질이 나빠 충돌 찌꺼기(Runt)가 날아오거나 [CRC](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/113_crc/) 에러(FCS 검사 실패)가 발생한 쓰레기 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)라도 목적지까지 배달해 버린다. 이는 최종 수신자인 PC가 직접 에러를 계산하고 버려야 하므로, 전체 네트워크 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/)([Bandwidth](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/))을 헛되게 낭비하는 결과를 낳는다.

- **📢 섹션 요약 비유**: ** 컷스루 방식은 **"속도(Speed)를 위해 품질 검수(QA)를 완전히 포기한 공장"**입니다. 물건이 빛의 속도로 출고되지만 불량품 찌꺼기까지 섞여 나가기 때문에, 회선 자체가 튼튼하고 깨끗한 환경(광케이블 등)에서만 쓸 수 있는 극단적인 세팅입니다.

---

## Ⅲ. 비교 및 연결

[스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [에이징](/knowledge-base/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)이 기반 조건을 만든다면, [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)은 그 위에서 핵심 메커니즘을 구현하고, [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [에이징](/knowledge-base/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)의 기반 정리 | [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)의 핵심 동작 | [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)을 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [에이징](/knowledge-base/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/) 수준의 기본 대책으로 충분한지, 아니면 [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)이 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 스위칭 효율 부족인지, 브로드캐스트 범위 악화인지 먼저 분리한다.
2. [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [에이징](/knowledge-base/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)을 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)은 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/), 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [에이징](/knowledge-base/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 식별하는 기본 주소다. |
| [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)로 전달하는 핵심 장비다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: 에이징 / 포트 미러링</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: 스위칭 방식</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: 스위칭 방식</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 지능형 캠퍼스 패브릭</div></div>
</div>
</div>



[스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)는 [에이징](/knowledge-base/studynote/02_operating_system/07_virtual_memory/411_aging_algorithm/) / [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [미러링](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/333_raid_1/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/)와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 363 / 1120

← **이전**: [241. 에이징 (Aging) / 포트 미러링 (Port Mirroring)](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/241_aging_and_port_mirroring/)
**다음**: [243. 스위칭 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/243_switching_method_store_and_forward/) →

---
