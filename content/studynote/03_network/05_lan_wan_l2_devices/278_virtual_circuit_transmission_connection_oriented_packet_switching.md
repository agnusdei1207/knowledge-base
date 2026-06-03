+++
title = "278. 가상 회선 전송 방식 (연결형 패킷 교환"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 가상 회선 전송 방식 (연결형 패킷 교환은 LAN/WAN과 2계층 장비에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: 가상 회선 전송 방식 (연결형 패킷 교환을 이해하면 스위칭 효율과 브로드캐스트 범위 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 패킷 교환의 세부 방식 중 하나로, 송신자와 수신자 사이에 논리적 연결(가상 회선, VC)을 확립(Setup)한 뒤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전송하고 연결을 해제(Teardown)하는 통신 방식. 
- **필요성**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)그램 방식으로 패킷을 마구잡이로 뿌리면 도착 순서가 뒤죽박죽되어, 동영상을 실시간으로 보거나 화상 전화를 할 때 화면이 깨지고 말이 끊기는 참사가 벌어진다. 패킷을 쪼개서 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 효율은 살리되, **"모든 패킷이 이탈하지 않고 순서대로 줄 맞춰서 차례대로 도착하게 만드는 컨베이어 벨트"**가 필요했다.

- **💡 비유**: 
  - **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)그램**: 100명의 아이들이 각자 알아서 목적지 공원에 찾아오는 **"개인 행동"** (누가 먼저 올지, 길을 잃을지 모름).
  - **가상 회선**: 100명의 아이들이 앞사람 어깨에 손을 올리고 선생님이 파놓은 한 줄짜리 길만 따라가는 **"유치원 기차놀이"** (길을 잃지 않고 1번부터 100번까지 무조건 순서대로 도착함).

```text
[데이터그램 전송 방식]
    │
    ▼
[가상 회선 전송 방식 (연결형 패킷 교환]
    │
    └──▶ [브로드밴드통신망]
```

- **📢 섹션 요약 비유**: ** 가상 회선은 패킷이라는 수많은 지하철 객차들이 임시로 놓인 **"논리적인 철로(가상 회선)"**라는 하나의 궤도 위를 이탈 없이 차례대로 주행하는 안전한 통행 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 3단계 통신 프로세스
가상 회선 망은 예전 아날로그 전화기(회선 교환망)의 3단계 룰을 패킷 세상에 그대로 가져왔다.

1. **호 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) ([Call](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) Setup)**: "나 너한테 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보낼 건데 길 하나 파자!"라고 [Call](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) Request 패킷을 던져서 망 내부 라우터들이 가상의 길(VC 번호)을 하나 확정 짓게 만든다.
2. **[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Transfer)**: 길이 뚫리면 1번 패킷부터 수백만 번째 패킷까지 몽땅 아까 뚫어놓은 그 길(같은 번호표)만 쳐다보고 줄지어 쏜살같이 날아간다.
3. **호 해제 ([Call](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/189_subroutine_call_return/) Teardown)**: 볼일이 끝나면 "길 없애도 돼"라고 알려 자원(라우터의 맵핑 테이블)을 반환한다.

### 2. [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/): VCI, [DLCI](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/270_dlci_data_link_connection_identifier/), LCN
[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)그램의 IP 패킷은 매 패킷마다 목적지 전체 IP 주소(예: `192.168.1.100`)를 길게 적어야 했다.
하지만 가상 회선의 패킷들은 목적지 주소를 적을 필요가 없다. 어차피 1번 패킷이 뚫어놓은 길 번호만 적어 내면 된다. 이 짧은 번호표를 프레임 릴레이에서는 **[DLCI](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/270_dlci_data_link_connection_identifier/)**, ATM에서는 **VPI/VCI**, X.25에서는 **LCN(Logical Channel Number)**이라고 부르며, 이로 인해 헤더 오버헤드가 극적으로 줄어든다.

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                가상 회선 (Virtual Circuit) 순서 보장 도식      │
 ├─────────────────────────────────────────────────────────────┤
 │                                                             │
 │   [ 라우터 A ] ───(경로 1)──▶ [ 라우터 B ] ───(경로 2)──▶ [ 라우터 D ] │
 │        │                                             ▲      │
 │        └────────(경로 3)──▶ [ 라우터 C ] ───(경로 4)──┘      │
 │                                                             │
 │   1) 호 설정 단계: 라우터 A와 라우터 D가 협상하여               │
 │      "A -> B -> D"를 우리의 가상 회선(VC 100)으로 낙점함!      │
 │                                                             │
 │   2) 데이터 전송 단계: 패킷 1, 2, 3이 무조건 라우터 B만 거쳐서 직진! │
 │      (설령 밑의 경로 3, 4가 아무리 뻥뻥 뚫려 있어도 쳐다보지 않음)     │
 │                                                             │
 │   ▶ 결과: 순서가 1-2-3으로 완벽하게 보장되어 목적지에 도착함.        │
 └─────────────────────────────────────────────────────────────┘
```

### 3. 치명적인 단점 (라우터 파괴 시 단절)
가상 회선의 가장 큰 약점은 **"[단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)([SPOF](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/))"**이다.
만약 합의해 둔 가상 회선 길목에 있는 중간 라우터(라우터 B)가 갑자기 정전으로 죽어버리면 어떻게 될까? [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)그램 방식이었다면 라우터 A가 1초 만에 우회로(라우터 C)로 돌려보냈겠지만, 가상 회선 방식은 **길이 박살 난 순간 기존에 가던 모든 패킷이 버려지고, 다시 처음부터 호 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)(Setup)을 맺어 새로운 가상 회선을 뚫을 때까지 통신이 완전히 마비**된다.

- **📢 섹션 요약 비유**: ** 가상 회선은 안전하게 목적지까지 깔아둔 **"기찻길"**과 같습니다. 앞 기차를 뒤 기차가 절대 추월할 수 없어서 순서가 꼬이지 않지만, 중간에 선로 하나가 붕괴되면 우회전할 수 없어서 기차 운행이 전면 중단되는 치명적 약점을 가졌습니다.

---

## Ⅲ. 비교 및 연결

가상 회선 전송 방식 (연결형 패킷 교환을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [데이터그램 전송 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/277_datagram_transmission_connectionless_packet_switching/)이 기반 조건을 만든다면, 가상 회선 전송 방식 (연결형 패킷 교환은 그 위에서 핵심 메커니즘을 구현하고, [브로드밴드통신망](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/279_b_isdn_broadband_integrated_services_digital_network/)은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스위칭 효율과 브로드캐스트 범위에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [데이터그램 전송 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/277_datagram_transmission_connectionless_packet_switching/)의 기반 정리 | 가상 회선 전송 방식 (연결형 패킷 교환의 핵심 동작 | [브로드밴드통신망](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/279_b_isdn_broadband_integrated_services_digital_network/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스위칭 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: 가상 회선 전송 방식 (연결형 패킷 교환은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 가상 회선 전송 방식 (연결형 패킷 교환을 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [데이터그램 전송 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/277_datagram_transmission_connectionless_packet_switching/) 수준의 기본 대책으로 충분한지, 아니면 가상 회선 전송 방식 (연결형 패킷 교환이 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [브로드밴드통신망](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/279_b_isdn_broadband_integrated_services_digital_network/)와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 스위칭 효율 부족인지, 브로드캐스트 범위 악화인지 먼저 분리한다.
2. 가상 회선 전송 방식 (연결형 패킷 교환가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [브로드밴드통신망](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/279_b_isdn_broadband_integrated_services_digital_network/)와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 가상 회선 전송 방식 (연결형 패킷 교환의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [데이터그램 전송 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/277_datagram_transmission_connectionless_packet_switching/)와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: 가상 회선 전송 방식 (연결형 패킷 교환을 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

가상 회선 전송 방식 (연결형 패킷 교환은 LAN/WAN과 2계층 장비를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 스위칭 효율 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [브로드밴드통신망](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/279_b_isdn_broadband_integrated_services_digital_network/), 지능형 캠퍼스 패브릭, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 지능형 캠퍼스 패브릭 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: 가상 회선 전송 방식 (연결형 패킷 교환은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [데이터그램 전송 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/277_datagram_transmission_connectionless_packet_switching/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 주소 ([Media](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/) Address) | 2계층 전달 대상을 식별하는 기본 주소다. |
| [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) ([Switch](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 프레임을 적절한 포트로 전달하는 핵심 장비다. |
| [브로드밴드통신망](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/279_b_isdn_broadband_integrated_services_digital_network/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 데이터그램 전송 방식]
    │
    ▼
[현재 개념: 가상 회선 전송 방식 (연결형 패킷 교환]
    │
    ├──▶ [확장 A: 브로드밴드통신망]
    └──▶ [확장 B: 지능형 캠퍼스 패브릭]
```

가상 회선 전송 방식 (연결형 패킷 교환는 [데이터그램 전송 방식](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/277_datagram_transmission_connectionless_packet_switching/)에서 출발해 현재 메커니즘을 정교화하고, 이후 [브로드밴드통신망](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/279_b_isdn_broadband_integrated_services_digital_network/)와 지능형 캠퍼스 패브릭 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 학교 우편함에 이름표가 붙어 있어야 편지가 엉뚱한 곳에 가지 않아요.
2. 이 개념은 어느 교실로 보내야 할지 알아보는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 규칙과 같아요.
3. 그래서 같은 건물 안에서도 편지가 더 빠르고 질서 있게 움직여요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 399 / 1120

← **이전**: [277. 데이터그램 전송 방식 (비연결형 패킷 교환)](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/277_datagram_transmission_connectionless_packet_switching/)
**다음**: [279. 브로드밴드통신망 (B-ISDN)](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/279_b_isdn_broadband_integrated_services_digital_network/) →

---
