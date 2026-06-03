+++
title = "375. LDP (Label Distribution Protocol), RSVP-TE"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LDP, RSVP-TE는 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)과 경로 제어에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: LDP, RSVP-TE를 이해하면 수렴 속도과 확장성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [MPLS](/knowledge-base/studynote/03_network/07_network_layer_routing/373_mpls_multiprotocol_label_switching_20bit/) 네트워크에서 라우터 간에 레이블(Label)과 목적지 FEC(Forwarding Equivalence Class, IP 대역)의 매핑 정보를 협상, 배포, 유지하여 종단 간 레이블 스위칭 경로([LSP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/245_lsp_liskov_substitution_principle/))를 구축하는 제어 평면(Control Plane)의 시그널링 프로토콜들.
- **필요성**: 라우터 5대가 줄지어 있다. 입구 LER이 "100번 딱지 붙여서 쏠게"라고 마음먹었는데, 다음 LSR이 "난 100번 딱지가 뭔지 배운 적 없는데?" 하면 패킷은 버려진다. **통신이 시작되기 전에 미리, 라우터들끼리 "부산 갈 땐 100번 -> 200번 -> 300번 딱지로 바꿔치기하자"라고 약속(Label [Mapping](/knowledge-base/studynote/05_database/01_db_architecture_relational/010_schema_mapping/))을 쫙 끝내놔야 터널([LSP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/245_lsp_liskov_substitution_principle/))이 뚫린다.** 이 약속을 자동으로 조율해 주는 통신 규약이 필수적이었다.

- **💡 비유**: 라우터([LSR](/knowledge-base/studynote/03_network/07_network_layer_routing/374_lsr_label_switch_router_ler_edge/))들이 스파이라고 칩시다.
  - [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/): "부산 지부로 가려면 1번 기차를 타라"라고 **지도를 알려주는 놈**.
  - <strong>LDP / RSVP-<a href="/knowledge-base/studynote/03_network/07_network_layer_routing/361_ospf_traffic_engineering_te/">TE</a></strong>: 스파이들끼리 접선할 때 쓸 **"암구호(딱지 번호)를 맞춰주는 놈"**. "너 부산 지부 갈 때 검은 넥타이(100번 Label) 매고 와, 그럼 내가 붉은 장미(200번 Label) 건네주며 들여보내 줄게!"라고 사전 모의를 마치는 작업입니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">LSR, LER</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">LDP, RSVP-TE</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">MPLS VPN</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: ** 이 시그널링 프로토콜들은 릴레이 계주에서 **"바통 터치 구간 합의"**와 같습니다. 1번 주자가 "오른손으로 줄게(10번 라벨)", 2번 주자가 "그럼 난 왼손으로 받을게(20번 라벨 교환)"라고 달리기 전에 미리 룰을 정해둬야, 실전에서 0.1초의 낭비 없이 바통이 매끄럽게 전달됩니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

시험과 실무에서 "언제 LDP를 쓰고 언제 RSVP-TE를 쓰느냐"를 구별하는 것은 [MPLS](/knowledge-base/studynote/03_network/07_network_layer_routing/373_mpls_multiprotocol_label_switching_20bit/) 설계의 핵심이다.

### 1. LDP (Label Distribution [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) - 흐르는 강물처럼
대부분의 통신사([ISP](/knowledge-base/studynote/12_it_management/03_ea_isp/101_isp_information_strategy_planning_4_steps/))에서 아주 가볍게 팡팡 돌리는 기본 딱지 분배기다 ([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/[UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 646번 사용).
- <strong>특징 (<a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/008_dependencies/">종속성</a>)</strong>: 철저하게 OSPF나 [IS-IS](/knowledge-base/studynote/03_network/07_network_layer_routing/363_is_is_intermediate_system_clnp_telecom/) 같은 밑단 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 프로토콜이 찾아준 <strong>'최단 경로(<a href="/knowledge-base/studynote/05_database/07_exam_summary/547_graph_shortest_path_db_mapping/">Shortest Path</a>)'</strong>에 100% 의존한다.
- **동작**: OSPF가 "A ──▶ B ──▶ C"가 1등 길이라고 정해주면, LDP는 아무 불만 없이 딱 그 길 위에다가 "A야 10번 딱지 써라, B야 넌 20번 써라" 하고 번호표만 나눠주며 터널([LSP](/knowledge-base/studynote/04_software_engineering/04_testing_quality/245_lsp_liskov_substitution_principle/))을 뚫는다.
- **장점**: 설정이 너무 쉽다. 그냥 라우터에 `mpls ip` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 한 줄만 치면 지들끼리 쑥덕거리고 1초 만에 터널이 완성된다.

### 2. RSVP-[TE](/knowledge-base/studynote/03_network/07_network_layer_routing/361_ospf_traffic_engineering_te/) (Resource Reservation [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) - [TE](/knowledge-base/studynote/03_network/07_network_layer_routing/361_ospf_traffic_engineering_te/)) - 운명 거스르기
OSPF가 정해준 1등 길(고속도로)이 트래픽으로 터져나갈 때, 억지로 2등 길(국도)로 우회 터널을 뚫어야 할 때(Traffic Engineering) 투입되는 해결사다.
- **특징 (독립성)**: 기존 [OSPF](/knowledge-base/studynote/03_network/07_network_layer_routing/357_ospf_open_shortest_path_first_overview/) 지도를 대놓고 무시한다. "고속도로 꽉 막혔잖아! 돌아가더라도 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 빵빵한 국도 쪽에다가 딱지 번호 뿌려!"라며 <strong>관리자가 원하는 임의의 길(Explicit Path)로 억지로 터널(<a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/245_lsp_liskov_substitution_principle/">LSP</a>)을 비틀어 뚫어버린다.</strong>
- **동작 (예약)**: 목적지까지 가면서 단순히 딱지만 배분하는 게 아니라, "내가 이 터널로 1Gbps 트래픽 보낼 거니까 너네 라우터 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 1Gbps 치 미리 비워놔!(Resource Reservation)"라고 강제 예약까지 걸어버린다.
- **단점**: 길이 끊기면 OSPF처럼 자동으로 훅훅 복구되는 게 아니라, 터널을 처음부터 다시 파야 해서 관리자 설정이 더럽게 빡세고 라우터 CPU를 많이 잡아먹는다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">LDP vs RSVP-TE의 터널(LSP) 개척 사상 차이</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(위) 고속도로: 10Gbps (현재 9.9G 꽉 참)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">서울 LER</div><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">부산 LER</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">\ ↗</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(아래) 국도: 1Gbps (텅텅 비었음)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">* LDP의 만행: "OSPF님께서 고속도로가 1등이라고 하셨다! 무조건</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">고속도로 위에 딱지(터널) 뚫어!!" ──▶ 망 터짐.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">* RSVP-TE의 지능: "고속도로 꽉 찬 거 안 보여? 텅텅 빈 아래쪽 국도로</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">내가 강제로 1Gbps 예약해서 터널 비틀어 뚫어줄게!"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">──▶ 망이 쾌적하게 로드 밸런싱됨.</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: <strong> LDP가 "내비게이션이 시키는 대로만 아무 생각 없이 표지판(Label)을 꽂고 다니는 </strong>수동적인 알바생<strong>"이라면, RSVP-TE는 차가 막히면 내비게이션을 무시하고, 자기 권력으로 경찰을 동원해 갓길과 샛길의 차들을 다 빼버린 뒤 뻥 뚫린 무정차 호송로(<a href="/knowledge-base/studynote/03_network/07_network_layer_routing/361_ospf_traffic_engineering_te/">TE</a> 터널)를 개척해 내는 </strong>"교통경찰대장"**입니다.

---

## Ⅲ. 비교 및 연결

LDP, RSVP-TE를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [LSR](/knowledge-base/studynote/03_network/07_network_layer_routing/374_lsr_label_switch_router_ler_edge/), LER가 기반 조건을 만든다면, LDP, RSVP-TE는 그 위에서 핵심 메커니즘을 구현하고, [MPLS](/knowledge-base/studynote/03_network/07_network_layer_routing/373_mpls_multiprotocol_label_switching_20bit/) VPN는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 수렴 속도과 확장성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [LSR](/knowledge-base/studynote/03_network/07_network_layer_routing/374_lsr_label_switch_router_ler_edge/), LER의 기반 정리 | LDP, RSVP-TE의 핵심 동작 | [MPLS](/knowledge-base/studynote/03_network/07_network_layer_routing/373_mpls_multiprotocol_label_switching_20bit/) VPN의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 수렴 속도 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: LDP, RSVP-TE는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 LDP, RSVP-TE를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [LSR](/knowledge-base/studynote/03_network/07_network_layer_routing/374_lsr_label_switch_router_ler_edge/), LER 수준의 기본 대책으로 충분한지, 아니면 LDP, RSVP-TE가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [MPLS](/knowledge-base/studynote/03_network/07_network_layer_routing/373_mpls_multiprotocol_label_switching_20bit/) VPN와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 수렴 속도 부족인지, 확장성 악화인지 먼저 분리한다.
2. LDP, RSVP-TE가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [MPLS](/knowledge-base/studynote/03_network/07_network_layer_routing/373_mpls_multiprotocol_label_switching_20bit/) VPN와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- LDP, RSVP-TE의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [LSR](/knowledge-base/studynote/03_network/07_network_layer_routing/374_lsr_label_switch_router_ler_edge/), LER와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: LDP, RSVP-TE를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

LDP, RSVP-TE는 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)과 경로 제어를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 수렴 속도 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [MPLS VPN](/knowledge-base/studynote/03_network/07_network_layer_routing/376_mpls_vpn_l3_vrf_bgp/), 의도 기반 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 의도 기반 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: LDP, RSVP-TE는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [LSR](/knowledge-base/studynote/03_network/07_network_layer_routing/374_lsr_label_switch_router_ler_edge/), LER | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 테이블 ([Routing](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) Table) | 패킷 전달 의사결정의 기준이 된다. |
| [메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/) ([Metric](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)) | 최적 경로를 선택하는 비교 척도다. |
| [MPLS VPN](/knowledge-base/studynote/03_network/07_network_layer_routing/376_mpls_vpn_l3_vrf_bgp/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: LSR, LER</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: LDP, RSVP-TE</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: MPLS VPN</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 의도 기반 라우팅</div></div>
</div>
</div>



LDP, RSVP-TE는 [LSR](/knowledge-base/studynote/03_network/07_network_layer_routing/374_lsr_label_switch_router_ler_edge/), LER에서 출발해 현재 메커니즘을 정교화하고, 이후 [MPLS](/knowledge-base/studynote/03_network/07_network_layer_routing/373_mpls_multiprotocol_label_switching_20bit/) VPN와 의도 기반 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 여러 갈림길이 있는 미로에서 가장 좋은 길을 고르는 게임과 같아요.
2. 이 개념은 길이 막히면 다른 길로 빨리 바꾸는 규칙도 알려줘요.
3. 그래서 인터넷 길찾기가 덜 헤매고 더 똑똑해져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 496 / 1120

← **이전**: [374. LSR (Label Switch Router), LER (Label Edge Router)](/knowledge-base/studynote/03_network/07_network_layer_routing/374_lsr_label_switch_router_ler_edge/)
**다음**: [376. MPLS VPN](/knowledge-base/studynote/03_network/07_network_layer_routing/376_mpls_vpn_l3_vrf_bgp/) →

---
