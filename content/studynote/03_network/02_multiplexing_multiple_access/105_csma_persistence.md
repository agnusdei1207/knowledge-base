---
title: "105. 1-Persistent, Non-Persistent, p-Persistent CSMA"
date: "2026-03-04"
description: "CSMA에서 채널이 사용 중일 때 노드가 대기하는 세 가지 전략적 접근 방식(지속 방식)의 동작 원리, 장단점 및 트레이드오프를 심층 분석합니다."
tags:
  - "network"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [CSMA](/studynote/03_network/02_multiplexing_multiple_access/104_csma/) (Carrier Sense [Multiple Access](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/)) 환경에서 통신 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)가 이미 사용 중일 때, 데이터를 전송하려는 노드가 충돌을 최소화하고 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 접근 기회를 획득하기 위해 대기 및 재시도하는 세 가지 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)(지속 방식)이다.
> 2. **가치**: 채널이 비면 즉시 전송하여 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 줄이는 방식(1-Persistent)과, 무작위로 양보하여 충돌을 막는 방식(Non-Persistent) 간의 딜레마를 해결하기 위해, [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) p를 도입하여 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))과 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Delay)의 밸런스를 맞췄다.
> 3. **판단 포인트**: 트래픽이 적은 유선망 환경에서는 1-Persistent가 유리하지만, 무선망이나 고부하 트래픽 상황에서는 p-Persistent 방식과 이진 지수 백오프 (BEB) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 융합하여 네트워크 붕괴를 동적으로 방어해야 한다.

---

## Ⅰ. 개요 및 필요성

[CSMA](/studynote/03_network/02_multiplexing_multiple_access/104_csma/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 핵심 규칙인 "말하기 전에 먼저 들어라(Listen Before Talk)"는 매우 직관적이지만, 치명적인 허점을 가지고 있다. 노드가 채널을 감지(Carrier Sense)했을 때, 채널이 이미 다른 누군가에 의해 사용 중(Busy)이라면 그 다음엔 어떻게 행동해야 하는가에 대한 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 부재다.

만약 채널이 사용 중일 때 모든 노드가 전송이 끝나기만을 끈질기게 기다렸다가 채널이 비자마자 동시에 데이터를 쏘아 보낸다면, 100% 충돌이 발생해 네트워크는 마비된다. 반대로 채널이 쓰이고 있다고 모두가 뒤로 물러나 장시간 쉬어버리면, 채널이 비어 있는 유휴 시간([Idle](/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/) Time)이 늘어나 네트워크 전체의 처리 효율이 바닥으로 추락한다. 따라서 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간을 최소화하려는 '공격적 대기'와 충돌을 회피하려는 '방어적 양보' 사이에서 최적의 균형점을 찾는 수학적이고 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적인 접근 제어 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 필수적으로 요구되었다.

- **📢 섹션 요약 비유**: 사람들이 붐비는 식당에 갔을 때, 앞사람이 나오자마자 무작정 밀고 들어갈 것인지(1-Persistent), 아예 산책을 다녀올 것인지(Non-Persistent), 동전을 던져서 들어갈지 말지 결정할 것인지(p-Persistent)를 정하는 입장 대기 규칙과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

세 가지 지속 방식 (Persistence Methods)은 채널 상태를 감지한 직후의 행동 트리 로직으로 구분된다.

```text
+--------------------------------------------------------------+
|          CSMA 지속 방식의 상태 전이 및 로직 분기 다이어그램  |
+--------------------------------------------------------------+
|                                                              |
| [ Carrier Sense (채널 상태 감지) ]                           |
|        |                                                     |
|        +--> 1. 1-Persistent CSMA                              |
|        |      - 채널 Idle? --(Yes)---> 즉시 데이터 전송 (100%)|
|        |      - 채널 Busy? --(Yes)---> Idle 될 때까지 지속 감시 |
|        |                                                     |
|        +--> 2. Non-Persistent CSMA                            |
|        |      - 채널 Idle? --(Yes)---> 즉시 데이터 전송       |
|        |      - 채널 Busy? --(Yes)---> 감시 중단 후 랜덤 대기 |
|        |                                (Random Backoff)     |
|        |                                                     |
|        +--> 3. p-Persistent CSMA                              |
|               - 채널 Busy? --(Yes)---> Idle 될 때까지 지속 감시 |
|               - 채널 Idle? --(Yes)---> 확률 p 로 전송 시도    |
|                                      확률 1-p 로 다음 슬롯 대기|
|                                      (다음 슬롯에서도 다시 확률)|
+--------------------------------------------------------------+
```

1. **1-Persistent (1-지속)**: 집착도가 가장 높다. 채널이 비면 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 1($100\%$)로 즉시 덤벼든다. 대기 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Delay)이 가장 짧지만, 대기 중이던 2개 이상의 노드가 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)가 비는 순간 동시에 쏘기 때문에 [다중 접속](/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) 환경에서 충돌 가능성이 극도로 높다.
2. **Non-Persistent (비지속)**: 양보의 미덕을 가진다. 누군가 사용 중이면 즉시 채널 감시를 포기하고 임의의 시간(Random Time) 동안 잠들었다가 다시 확인한다. 충돌률은 가장 낮지만, [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)가 비어있어도 아무도 전송하지 않는 낭비 구간이 생겨 전송 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 가장 길다.
3. **p-Persistent (p-지속)**: 타협점이다. 시간을 일정한 슬롯 단위로 쪼개고, [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)가 비었을 때 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) $p$ (예: $0.1$)로만 전송을 시도한다. 남은 $1-p$ (예: $0.9$)의 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)로는 전송을 다음 슬롯으로 양보한다. 충돌을 효과적으로 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)시키면서도 랜덤 대기보다 채널 점유율을 높인다.

- **📢 섹션 요약 비유**: 1-Persistent는 빈자리가 나자마자 가방을 집어 던지는 '무대포 돌격형', Non-Persistent는 자리 없으면 카페나 한 바퀴 돌고 오는 '여유로운 산책형', p-Persistent는 자리가 났을 때 친구와 가위바위보를 해서 이긴 사람만 앉는 '[확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 게임형' 대기 방식입니다.

---

## Ⅲ. 비교 및 연결

네트워크 트래픽의 부하(Load) 상태에 따라 각 방식의 효율성은 극단적으로 역전된다.

| 지속 방식 | 충돌 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) | 채널 낭비([Idle](/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/) 낭비) | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Delay) | 트래픽 고부하 시 효율 | 대표 적용 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
|:---|:---|:---|:---|:---|:---|
| **1-Persistent** | 가장 높음 (동시 접근) | 낮음 | 매우 짧음 | **최악 (네트워크 마비)** | [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [Ethernet](/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) ([CSMA](/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CD) |
| **Non-Persistent**| 낮음 (무작위 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)) | 매우 높음 | 가장 긺 | **우수 (안정적 방어)** | 특정 무선망 기초 |
| **p-Persistent** | 중간 (p값에 비례) | 중간 | 중간 | **최적화 (p 조절 시)** | Wi-Fi ([CSMA](/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CA의 근간) |

밤 시간대처럼 네트워크 접속자가 적은 **저부하(Low Load)** 상황에서는 1-Persistent가 절대적으로 유리하다. 굳이 무작위 대기를 하며 낭비할 시간 없이 바로 쏘는 것이 빠르기 때문이다. 하지만 트래픽이 꽉 차는 **고부하(High Load)** 상황에서는 1-Persistent는 100% 충돌을 일으키며 스스로 붕괴 매커니즘을 작동시킨다. 이때는 차라리 Non-Persistent처럼 무작위 시간으로 각자 흩어져서 덤벼드는 것이 전체 시스템의 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)([Throughput](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))을 방어하는 유일한 길이다.

- **📢 섹션 요약 비유**: 손님이 없는 한산한 도로는 1-Persistent처럼 눈치 안 보고 달리는 게 제일 빠르지만, 명절 귀성길(고부하)에는 앞차가 출발했다고 무작정 꼬리를 물면 교차로 전체가 마비되므로 Non-Persistent처럼 조금씩 양보하며 간격을 두는 것이 결과적으로 모두가 빨리 가는 길입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

p-Persistent 방식의 철학은 현대 네트워크, 특히 무선 랜(Wi-Fi) 장비에서 단순한 고정 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)을 넘어 충돌 상황에 스스로 적응하는 동적 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 발전했다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 판단 포인트
1. <strong>이더넷과 <a href="/studynote/03_network/02_multiplexing_multiple_access/104_csma/">CSMA</a>/CD 판단</strong>: 유선 LAN 환경의 [CSMA](/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CD는 전송 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)(케이블)의 충돌 감지가 매우 빠르고 비용이 적어 1-Persistent 방식을 기본으로 사용했다. 충돌이 나면 즉시 전송을 멈추고 잼(Jam) 신호를 보내면 그만이기 때문에, 일단 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 최소화하기 위해 100% 들이받는 방식을 택한 것이다.
2. **무선망(Wi-Fi) 환경의 동적 적응형 백오프 (BEB)**: 무선 환경에서는 충돌 감지 자체가 어렵고 충돌 시 비용이 너무 크다. 따라서 IEEE 802.[11](/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/) [CSMA](/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/[CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)은 고정된 p-Persistent 대신 이진 지수 백오프 (Binary Exponential Backoff, BEB)를 적용한다. 처음에는 좁은 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 공간(Contention Window)에서 랜덤 값을 뽑지만, 충돌이 연속해서 발생할수록 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 공간을 2배, 4배, 8배로 기하급수적으로 늘려 노드들 스스로 전송 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)을 동적으로 떨어뜨리게 만든다.
3. **네트워크 최적화 튜닝**: 혼잡한 공공 와이파이 망을 설계할 때 잦은 끊김이 발생한다면, 각 단말이 무리하게 채널 점유를 시도하다 충돌이 발생하는 것이다. 실무 엔지니어는 공유기([AP](/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/))의 최소/최대 경쟁 윈도우(CWmin, CWmax) 값을 튜닝하여 고부하 상황에서 노드들이 더 긴 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)로 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 대기(p값을 낮추는 효과)하도록 설정하여 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 붕괴를 막을 수 있다.

- **📢 섹션 요약 비유**: 동적 백오프 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 대화할 때 처음 말이 겹치면 1초 기다렸다 말하고, 또 겹치면 2초, 그다음엔 4초를 기다리게 하여 사람이 많아질수록 서로 조심스럽게 입을 여는 똑똑한 [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/) 토론 규칙과 같습니다.

---

## Ⅴ. 기대효과 및 결론

CSMA의 세 가지 지속 방식은 네트워크 참여자들이 공용 자원([매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/))을 어떻게 공정하게 나누어 쓸 것인가에 대한 근원적인 해답을 제시했다.

[지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Delay)을 극단적으로 없애려다 충돌에 빠지는 1-Persistent의 한계와, 충돌을 피하려다 [매체](/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 유휴 시간 낭비에 빠지는 Non-Persistent의 단점을 결합하여 탄생한 p-Persistent 모델은 컴퓨팅 과학에서 트레이드오프(Trade-off) 최적화의 골드 스탠다드다. 오늘날 순수한 형태의 p-Persistent가 그대로 쓰이진 않지만, 채널의 혼잡도에 따라 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 대기 시간을 조절한다는 이 본질적 철학은 현대 와이파이(Wi-Fi)와 무선 통신 기기 수십억 대가 허공에서 서로 충돌하지 않고 데이터를 주고받게 만드는 눈에 보이지 않는 질서가 되었다.

- **📢 섹션 요약 비유**: 이 세 가지 방식은 신호등이 없는 교차로에서 자동차들이 어떻게 눈치를 보며 건너야 덜 사고가 나고 가장 많은 차가 빠져나갈 수 있는지를 연구한 과거 학자들의 교통 규칙이며, 지금은 스마트 자율주행 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 뇌 속에 스며들어 있습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/03_network/02_multiplexing_multiple_access/104_csma/">CSMA</a>/CD (Carrier Sense <a href="/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/">Multiple Access</a> with <a href="/studynote/03_network/02_multiplexing_multiple_access/106_CSMA_CD_유선이더넷_충돌감지/">Collision Detection</a>)</strong> | 주로 유선망에서 쓰이며, 빠른 충돌 감지가 가능해 공격적인 1-Persistent 방식을 뼈대로 채택한 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/). |
| <strong><a href="/studynote/03_network/02_multiplexing_multiple_access/104_csma/">CSMA</a>/<a href="/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a> (Carrier Sense <a href="/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/">Multiple Access</a> with <a href="/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/">Collision</a> Avoidance)</strong> | 충돌을 사전에 회피해야 하는 무선망 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로, [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 접근인 p-Persistent와 랜덤 대기 철학을 결합함. |
| **BEB (Binary Exponential Backoff)** | 충돌 시마다 경쟁 대기열(Contention Window)의 범위를 2배씩 늘려 전송 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) p를 동적으로 낮추는 충돌 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/). |
| **Contention Window (CW)** | 노드가 전송을 시도하기 전 대기할 슬롯 수를 결정하기 위해 난수를 뽑는 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 범위 공간. |

### 📈 관련 키워드 및 발전 흐름도

```text
ALOHA (눈치 안 보고 무조건 전송 ---> 잦은 충돌)
    |
    v
CSMA (전송 전 채널 감시 시작, 지속 방식의 필요성 대두)
    |
    v
지속 방식 분화 (1-Persistent, Non-Persistent, p-Persistent)
    |
    v
이더넷 CSMA/CD (유선망: 1-Persistent 채택 및 충돌 시 즉각 중단)
    |
    v
무선랜 CSMA/CA 및 BEB (무선망: p-Persistent 진화형 동적 백오프 알고리즘)
```

### 👶 어린이를 위한 3줄 비유 설명

1. 마이크가 하나뿐인 교실에서, 친구가 말을 끝내자마자 무조건 내가 먼저 마이크를 잡으려고 달려드는 게 '1-Persistent(끈질긴 방식)'에요.
2. 앞 친구가 말하고 있으면 아예 자리에 엎드려 한참 자다가 일어나는 게 'Non-Persistent(포기하는 방식)'에요.
3. 'p-Persistent([확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 방식)'는 마이크가 비었을 때 주사위를 굴려서 짝수가 나온 사람만 말을 하도록 정해, 서로 소리치며 싸우는 일 없이 공평하게 발표하는 가장 똑똑한 방법이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 165 / 1120

<- **이전**: [1059. 디지털 트윈 및 관제 시스템 연동](/studynote/03_network/20_performance_evaluation_advanced/1059_digital_twin_network_management_simulation/)
**다음**: [1060. 양자 암호 키 분배 (QKD 인프라 기반망)](/studynote/03_network/20_performance_evaluation_advanced/1060_qkd_quantum_key_distribution_network/) ->

---
