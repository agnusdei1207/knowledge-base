---
title: 1100. 스위치 포트 미러링 (SPAN/TAP)
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]] [[333_raid_1|미러링]]은 [[282_performance_tactics|성능]] 평가와 고급 분석에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]] [[333_raid_1|미러링]]을 이해하면 측정 정확도과 모델 적합성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- 깡통 [[459_dummy_test_double|더미]] [[152_hub_dummy_switching_intelligent|허브]]([[152_hub_dummy_switching_intelligent|Hub]])는 1번 [[446_port_and_bus|포트]]로 데이터가 들어오면 2~24번 [[446_port_and_bus|포트]]로 몽땅 복사해서 뿌립니다(모든 통신 공유).
- **L2 [[238_switch_operation_principles|스위치]]([[238_switch_operation_principles|Switch]])**: [[673_mac_message_authentication_code|MAC]] 주소록이 있습니다. 철수(1번)가 영희(2번)에게 패킷을 보내면, 기계 내부에서 1번과 2번 [[446_port_and_bus|포트]]만 직통([[070_asic|ASIC]] 스위칭)으로 쾅 묶어버립니다. 
- **문제**: 보안팀이 감시하려고 24번 [[446_port_and_bus|포트]]에 [[601_ids_ips_syscall_tracing|침입 탐지 시스템]]([[601_ids_ips_syscall_tracing|IDS]], 엑스레이)을 꽂아놔도, 철수의 패킷이 24번으로는 단 1비트도 흘러오지 않기 때문에 네트워크 전체가 **완벽한 '감시 사각지대(블랙박스)'**로 변해 해커가 춤을 추게 됩니다.

```text
[VLAN 간 라우팅]
    │
    ▼
[스위치 포트 미러링]
    │
    └──▶ [UTP 배선 카테고리]
```

- **📢 섹션 요약 비유**: [[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]] [[333_raid_1|미러링]]은 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [[170_selectivity_cardinality_distribution_tuning|선택도]] 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

시스코가 만든 이 블랙박스를 깨부수는 흑마법입니다.

- **개념**: [[238_switch_operation_principles|스위치]] 장비의 관리자 화면(소프트웨어)에 명령어를 쳐서, **특정 원본 [[446_port_and_bus|포트]](Source)들로 지나다니는 모든 송수신 패킷의 쌍둥이 복사본을 0.01초 단위로 미친 듯이 찍어내어(Mirroring), 감시 장비가 꽂힌 목적지 [[446_port_and_bus|포트]](Destination) 하나로 모조리 쏟아붓게 만드는 트래픽 스니핑(엿듣기) 코어 기술**입니다.

1. **Local SPAN**: 원본 [[446_port_and_bus|포트]](1번)와 복사본을 받을 [[446_port_and_bus|포트]](24번)가 **'같은 쇳덩어리 [[238_switch_operation_principles|스위치]] 1대 안'**에 있을 때 씁니다. (가장 흔함)
2. **RSPAN (Remote SPAN)**: "감시 장비가 3층 [[238_switch_operation_principles|스위치]]에 있는데, 1층 [[238_switch_operation_principles|스위치]]의 트래픽을 감시하고 싶어!" 
   - 1층 [[238_switch_operation_principles|스위치]]가 패킷을 복사한 뒤, 특수한 **'가짜 [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 방([[224_vlan_virtual_lan_broadcast_domain|VLAN]] 999 등)'**이라는 트렁크 터널에 복사본을 태워 3층 [[238_switch_operation_principles|스위치]]까지 날려 보내는 장거리 릴레이 스니핑 꼼수입니다. (ERSPAN은 L3 라우터를 넘어 [[378_gre_generic_routing_encapsulation|GRE]] 터널로 쏩니다.)

```text
[VLAN 간 라우팅]
    │
    ▼
[스위치 포트 미러링]
    │
    └──▶ [UTP 배선 카테고리]
```

- **📢 섹션 요약 비유**: [[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]] [[333_raid_1|미러링]]의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

돈이 안 들어서 제일 좋지만, 장애가 터지면 형편없는 쓰레기가 됩니다.

- **[[140_bandwidth|대역폭]] [[095_overflow|오버플로우]] 한계**: 1번 [[446_port_and_bus|포트]](1Gbps)와 2번 [[446_port_and_bus|포트]](1Gbps)를 몽땅 복사해서 감시용 24번 [[446_port_and_bus|포트]](1Gbps) 1곳에 욱여넣으려고 합니다.
- **재앙**: $1G + 1G = 2Gbps$의 트래픽이 1Gbps짜리 감시 [[446_port_and_bus|포트]] 구멍으로 쏟아지면? 1기가의 트래픽이 병목에 걸려 바닥에 처참하게 버려집니다(Packet Drop).
- 해커는 이걸 노립니다. 회사망에 엄청난 디도스(트래픽)를 걸어 SPAN 복사본 [[446_port_and_bus|포트]]를 병목으로 뻗게 만든 뒤, 감시 카메라가 안 돌아가는 틈을 타 몰래 기밀문서를 유유히 빼돌립니다(보안 탐지율 떡락).

[[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]] [[333_raid_1|미러링]]을 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 간 [[339_routing_overview_best_path_selection|라우팅]]이 기반 조건을 만든다면, [[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]] [[333_raid_1|미러링]]은 그 위에서 핵심 메커니즘을 구현하고, [[124_unshielded_twisted_pair|UTP]] 배선 카테고리는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 측정 정확도과 모델 적합성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 간 [[339_routing_overview_best_path_selection|라우팅]]의 기반 정리 | [[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]] [[333_raid_1|미러링]]의 핵심 동작 | [[124_unshielded_twisted_pair|UTP]] 배선 카테고리의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 측정 정확도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: [[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]] [[333_raid_1|미러링]]은 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

- SPAN의 패킷 유실과 [[238_switch_operation_principles|스위치]] CPU 부하를 못 견딘 금융권은 '하드웨어'로 승부합니다.
- **TAP 장비**: [[238_switch_operation_principles|스위치]]와 [[238_switch_operation_principles|스위치]]를 잇는 광케이블 선 중간에 가위로 싹둑 잘라서 끼워 넣는 수백만 원짜리 **'물리적 Y자 프리즘 광분배기 기계'**입니다.
- **효과**: 소프트웨어가 복사하는 게 아니라, 빛(패킷)이 지나갈 때 **물리학적인 거울(광 스플리터)**로 빛을 50:50으로 정확히 쪼개서 한 가닥은 원래 길로 보내고, 한 가닥은 엑스레이([[601_ids_ips_syscall_tracing|IDS]])로 쏴줍니다.
- 전기가 나가도 원본 통신은 100% 정상 작동하며([[459_fail_safe|Fail-Safe]]), 트래픽이 100Gbps로 쏟아져도 단 1비트의 복사본 손실도 없이 100% 감시 장비로 복제해 내는 **무결점 트래픽 복사 아키텍처의 끝판왕**입니다.

### 실무 [[435_checklist_based_testing|체크리스트]]

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 기존 **[[238_switch_operation_principles|스위치]] 통신**은 회사의 각 부서 사이를 연결하는 완벽히 독립된 **'밀실 유리관 터널'**입니다. 철수 방과 영희 방 사이에 밀실 [[123_pipe|파이프]]가 연결되어 둘이 비밀 서류를 주고받아도, 24번 방에 있는 경찰([[601_ids_ips_syscall_tracing|IDS]] 보안장비)은 그 [[123_pipe|파이프]] 안이 보이지 않아 꿀 먹은 벙어리가 됩니다. 이를 감시하는 첫 번째 꼼수 **SPAN([[446_port_and_bus|포트]] [[333_raid_1|미러링]])**은 [[238_switch_operation_principles|스위치]] 기계 안에 있는 **'[[933_cctv|CCTV]] 관리자(소프트웨어)'**를 매수하는 것입니다. "관리자야, 철수 방 [[123_pipe|파이프]]로 서류가 지나갈 때마다 복사기에서 쌍둥이 서류를 한 장 더 찍어내서 내 24번 방으로 던져라!" 공짜라 좋지만, 서류가 1초에 1억 장 쏟아지면 관리자가 복사기를 돌리다 지쳐서 서류를 버려버리는 구멍(패킷 드롭)이 터집니다. 완벽한 두 번째 방법 **TAP 장비**는 아예 철수와 영희의 유리관 [[123_pipe|파이프]] 중간에 **'마법의 Y자 거울(물리적 광 스플리터 분배기)'**을 공사해서 꽂아버리는 겁니다. 서류 뭉치가 빛의 속도로 지나가면 거울에 반사되어 원본과 100% 똑같은 빛의 분신술이 만들어져 경찰 방으로 쏙 들어갑니다. [[238_switch_operation_principles|스위치]] CPU나 [[140_bandwidth|대역폭]] 병목에 전혀 구애받지 않고, 해커가 무슨 장난을 쳐도 0.001초의 오차 없이 모든 지문을 투명하게 빨아들이는 궁극의 하드웨어 스니핑 덫입니다.

---

## Ⅴ. 기대효과 및 결론

[[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]] [[333_raid_1|미러링]]은 [[282_performance_tactics|성능]] 평가와 고급 분석을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 측정 정확도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [[124_unshielded_twisted_pair|UTP]] 배선 카테고리, [[190_ai_llm_requirements_specification|AI]] 기반 [[282_performance_tactics|성능]] 예측, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [[190_ai_llm_requirements_specification|AI]] 기반 [[282_performance_tactics|성능]] 예측 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]] [[333_raid_1|미러링]]은 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 간 [[339_routing_overview_best_path_selection|라우팅]] | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [[139_throughput|처리량]] ([[139_throughput|Throughput]]) | 실제 전달 [[282_performance_tactics|성능]]을 나타내는 대표 지표다. |
| [[015_지연_데이터_관점|지연]] ([[141_latency|Latency]]) | 사용자 체감 품질을 좌우한다. |
| [[124_unshielded_twisted_pair|UTP]] 배선 카테고리 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: VLAN 간 라우팅]
    │
    ▼
[현재 개념: 스위치 포트 미러링]
    │
    ├──▶ [확장 A: UTP 배선 카테고리]
    └──▶ [확장 B: AI 기반 성능 예측]
```

[[238_switch_operation_principles|스위치]] [[446_port_and_bus|포트]] [[333_raid_1|미러링]]는 [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 간 [[339_routing_overview_best_path_selection|라우팅]]에서 출발해 현재 메커니즘을 정교화하고, 이후 [[124_unshielded_twisted_pair|UTP]] 배선 카테고리와 [[190_ai_llm_requirements_specification|AI]] 기반 [[282_performance_tactics|성능]] 예측 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 달리기 시합에서 누가 얼마나 빨랐는지 재려면 초시계와 기록표가 필요해요.
2. 이 개념은 네트워크가 어디서 느려졌는지 숫자로 찾아내는 도구예요.
3. 그래서 막연히 고치는 대신 가장 중요한 곳부터 똑똑하게 손볼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 210 / 1120

← **이전**: [[109_RTS_CTS_은닉노드문제|109. RTS/CTS (Request To Send / Clear To Send)]]
**다음**: [[1101_utp_cable_category_cat5_cat6|1101. UTP 배선 카테고리]] →

---
