+++
title = "111. ALOHA (순수 알로하)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 하와이 대학에서 개발한 최초의 무선 라디오 패킷 통신망으로, 노드가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 원할 때 언제든 즉시 전송하는 '무작위 [다중 접속](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/)(Random [Multiple Access](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/))' 기술의 근원이다.
> 2. **가치**: 채널 감지 기능이 없어 패킷 충돌([Collision](/knowledge-base/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/))에 무방비하게 노출되며, 최대 채널 활용률([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))이 약 18.4%에 불과하지만 현대 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/)([CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CD) 발전의 결정적 모티브를 제공했다.
> 3. **판단 포인트**: 초저전력 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 환경, RFID 태그 인식, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 위성 통신의 접속 제어 등 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 오버헤드를 줄여야 하는 단순 무선 채널 환경에서 여전히 철학적 기반으로 응용되고 있다.

---

## Ⅰ. 개요 및 필요성

순수 알로하 (Pure ALOHA)는 1970년대 초 미국 하와이 대학에서 여러 섬에 흩어진 컴퓨터들을 하나의 중앙 호스트와 무선 라디오 링크로 연결하기 위해 고안된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층의 [매체 접근 제어](/knowledge-base/studynote/03_network/04_data_link_layer_error/183_mac_media_access_control/) ([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/), [Media](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) [Access Control](/knowledge-base/studynote/02_operating_system/09_file_system/547_access_control_rwx/)) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다. 유선망 설치가 물리적으로 불가능한 도서 지역의 환경적 제약을 극복하기 위해, 누구나 원할 때 전파를 쏠 수 있는 파격적이고 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)화된 통신 모델이 요구되었다.
기존 통신망에서 주로 사용하던 주파수 분할(FDM)이나 시분할(TDM) 기반의 고정 할당 방식은 컴퓨터 통신의 버스트(Burst, 간헐적이고 폭발적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 발생) 특성과 맞지 않아 극심한 주파수 낭비를 초래했다. 이에 ALOHA는 '송신 큐에 패킷이 생성되면 채널 상태를 묻지도 따지지도 않고 즉각 쏘아보낸다'는 단순명료한 철학을 도입했다. 이 방식은 복잡한 제어 채널이나 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 인프라를 전혀 요구하지 않아 시스템 복잡도를 극적으로 낮추는 혁신을 이루어냈다. 그러나 상대방의 통신 여부를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하지 않는 맹목적 특성상 패킷 충돌([Collision](/knowledge-base/studynote/05_database/04_transactions_concurrency/563_hash_collision_chaining_linear_probing/))이 필연적으로 발생하며, 트래픽이 증가할수록 기하급수적인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 초래하는 딜레마를 안고 있다.

*기존 방식의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 한계와 ALOHA의 즉각적 접근 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)*
이 도식은 고정 할당([TDMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/089_시분할_다중접속_TDMA/))의 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)과 ALOHA의 즉각 전송 구조가 갖는 본질적 차이를 대조하여 보여준다.

```text
┌────────────────────────────────────────────────────────┐
│ [TDMA 대역 할당: 자원 낭비 및 지연 발생]               │
│ Node A: [비어있음] [A 패킷] [비어있음] [비어있음]      │
│ Node B: [비어있음] [비어있음] [비어있음] [B 패킷]      │
├────────────────────────────────────────────────────────┤
│ [Pure ALOHA 무작위 접근: 즉각 전송 및 충돌 감수]       │
│ Node A:      [A 패킷 전송]                             │
│ Node B:                 [B 패킷 전송]                  │
│ Node C:          [C 패킷 전송] (A와 C의 물리적 충돌!)  │
└────────────────────────────────────────────────────────┘
```
*해설*: 이 그림의 핵심은 ALOHA가 타임 슬롯이라는 정해진 규격을 탈피하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 발생 즉시 전송을 허용한다는 점이다. 이런 배치는 트래픽이 희소할 때 대기 시간([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))을 0에 가깝게 최소화하기 때문이며, 결과적으로 중앙 제어 비용을 없애지만 다중 노드 동시 발송 시 신호가 파괴되는 트레이드오프를 감수해야 한다. 실무에서는 이러한 이유로 트래픽 발생이 매우 간헐적이고 간섭이 적은 특수 환경에 제한적으로 채택된다.

- **📢 섹션 요약 비유**: 마치 불이 꺼진 넓은 강당에서 여러 사람이 귓속말을 하다가 자신이 하고 싶은 말이 생길 때 갑자기 큰 소리로 외치는 것과 같습니다. 아무도 없으면 즉시 전달되지만, 다른 사람이 동시에 소리치면 목소리가 섞여 아무도 알아듣지 못합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

순수 알로하 아키텍처는 극단적으로 단순화된 송수신 [스테이트](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) 머신([State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Machine)과 충돌 후 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 위한 타이머/백오프 로직으로 구성된다.

| 핵심 요소 | 역할 | 내부 동작 메커니즘 | 관련 파라미터/[프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
|:---|:---|:---|:---|
| 전송 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) (Transmitter) | 무작위 채널 접근 | 상위 계층 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 캡슐화 즉시 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)로 브로드캐스트 | Random Access 모드 |
| 응답 대기 (ACK [Timer](/knowledge-base/studynote/02_operating_system/01_overview_architecture/071_os_timer/)) | 충돌 여부 판단 | 전송 완료 시점부터 [RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/)(왕복 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) 기준 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 대기 | [Timeout](/knowledge-base/studynote/02_operating_system/05_deadlock/319_timeout_prevention/) (T_prop * 2) |
| 취약 시간 (Vulnerable Time) | 프레임 파괴 임계 영역 | 한 프레임 전송에 대해 앞뒤로 겹치는 전송을 허용하지 않는 시간대 | $2 \times T_f$ (프레임 [전송 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/)) |
| 백오프 제어 (Backoff) | 재충돌 방지 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 충돌(ACK 미수신) 감지 시 임의의 난수 시간 추출 후 대기 | 이진 지수 백오프 기반 |

*알로하 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 취약 시간 (Vulnerable Time) 분석*
이 도식은 순수 알로하에서 기준 패킷이 온전히 살아남기 위해 다른 패킷이 침범해서는 안 되는 '취약 시간'이 왜 프레임 시간의 2배가 되는지 증명한다.

```text
       |<─── Vulnerable Time (2 × T_f) ───>|
       |                                   |
Node B | [패킷 B]                          |  <-- A의 앞부분과 충돌
Node A |           [패킷 A (기준 프레임)]  |
Node C |                           [패킷 C]|  <-- A의 뒷부분과 충돌
       |                                   |
Time ──┴───────────┴───────────────┴───────┴───────>
     t_0 - T_f    t_0            t_0 + T_f
```
*해설*: 이 도식의 핵심은 기준 프레임(Node A)이 시간 $t_0$부터 $t_0 + T_f$까지 전송될 때, 다른 노드의 프레임이 단 1비트라도 겹치면 전체 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 깨진다는 것을 나타낸다. 이런 배치는 채널 센싱 로직이 부재하기 때문이며, A보다 약간 먼저 시작한 패킷 B나 A가 끝나기 직전에 시작한 패킷 C 모두 A 프레임을 파괴한다. 따라서 순수 알로하의 총 취약 시간은 프레임 [전송 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/)의 2배($2T_f$)가 되며, 이는 전체 네트워크 [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)의 수학적 상한선을 억누르는 가장 큰 병목 지점이 된다.

내부 동작 프로세스는 다음과 같이 흐른다.
1. **상태 감지 없음**: 노드는 채널이 사용 중인지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하지 않고 패킷 송신을 개시한다.
2. <strong>응답 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>: 프레임 전송을 마친 송신자는 수신자(중앙 호스트)로부터의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 응답(ACK)을 기다린다.
3. **오류 인지**: 설정된 [타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/) 타이머가 만료되거나 훼손된 패킷에 대한 NAK를 수신하면 충돌 발생을 인지한다.
4. <strong>난수 <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a></strong>: 재전송 시 각 노드가 똑같은 시간에 다시 시도하면 또 충돌하므로, 노드별로 독립적인 난수(Random Number)를 생성하여 해당 시간만큼 대기 상태로 전환한다.
5. **재전송 한계**: 일정 횟수 이상 재전송 시도가 실패하면 시스템 혼잡을 막기 위해 상위 계층에 전송 실패 오류를 보고하고 프레임을 파기한다.

- **📢 섹션 요약 비유**: 교차로에 신호등도 반사경도 없이 무작정 진입하는 자동차와 같습니다. 운 좋게 통과하면 가장 빠르지만, 부딪히면 사고를 수습하고 주사위를 던져 나온 시간만큼 기다린 뒤 다시 무작정 진입을 시도하는 무모하고도 단순한 규칙입니다.

---

## Ⅲ. 비교 및 연결

순수 알로하는 시스템 [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/) 모델링의 고전적 사례이다. 패킷 생성률이 포아송 분포(Poisson Distribution)를 따른다고 가정할 때, 트래픽 부하 $G$ (채널 시간당 생성되는 평균 패킷 수)에 따른 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) $S$ ([Throughput](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))는 수학적으로 $S = G \times e^{-2G}$로 도출된다.

*무작위 [매체 접근 제어](/knowledge-base/studynote/03_network/04_data_link_layer_error/183_mac_media_access_control/)(Random Access) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 비교 매트릭스*
이 도식은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통신 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 계층의 진화 단계에서 순수 알로하가 갖는 구조적 한계와 개선 모델의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 차이를 정량적으로 분석한다.

```text
┌──────────┬─────────────────┬─────────────────┬─────────────────┐
│ 항목     │ Pure ALOHA      │ Slotted ALOHA   │ CSMA/CD (이더넷)│
├──────────┼─────────────────┼─────────────────┼─────────────────┤
│ 전송 기준│ 데이터 생성 즉시│ 다음 슬롯 경계시│ 채널 유휴 감지후│
│ 취약 시간│ 2 × T_f         │ 1 × T_f         │ 전파 지연 수준  │
│ 최대 효율│ 18.4% (G=0.5일때) 36.8% (G=1.0일때) 80~90% 이상     │
│ 동기화   │ 불필요 (비동기) │ 필수 (클럭 동기)│ 불필요 (동적)   │
│ 운영 복잡│ 매우 낮음       │ 보통            │ 높음            │
└──────────┴─────────────────┴─────────────────┴─────────────────┘
```
*해설*: 이 그림의 핵심은 채널 효율을 18.4%에서 36.8%로 올리기 위해 Slotted ALOHA가 시간 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)라는 복잡성을 추가했다는 점이다. 순수 알로하는 아무런 룰이 없어 효율이 가장 낮지만, 그만큼 구현 하드웨어가 극도로 저렴해진다. 반면 [CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CD는 남이 송신 중인지 물리적으로 귀를 기울이는(Carrier Sense) 회로가 추가되어 충돌 시간을 [전파 지연](/knowledge-base/studynote/03_network/01_data_communication/016_전파_지연/) 수준으로 대폭 단축시켰다. 실무에서는 망 구축 예산과 노드의 컴퓨팅 파워 한계에 따라 이 세 가지 철학 중 하나를 선택하거나 변형하여 적용한다.

- **📢 섹션 요약 비유**: 순수 알로하가 1차선 도로에 무작위로 끼어드는 '비포장 도로'라면, 슬롯 알로하는 차단기가 10초마다 열리는 '신호등 도로'이고, CSMA는 멀리서 차가 오는지 쳐다보고 들어가는 '스마트 교차로'와 같습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

현대의 주력 고속 네트워크([LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/), [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/), Wi-Fi)의 메인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 트래픽 채널에는 순수 알로하 방식이 절대 쓰이지 않는다. 그러나 기지국에 처음 붙기 위해 시그널링을 하는 접속 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 단계에서는 여전히 이 철학이 변형되어 사용된다.

*ALOHA 아키텍처 기반 실무 [의사결정 트리](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/124_decision_tree/)*
이 도식은 네트워크 엔지니어가 무선/[IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 망 구축 시 채널 접근 제어 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 선정하는 논리적 판단 구조를 보여준다.

```text
[요구사항: 수만 개의 분산 노드가 무선 채널 1개를 공유]
         │
         ├─> 고정 지연 보장 및 고대역폭 데이터 전송이 필요한가?
         │    ├─ (Yes) ─> 중앙 통제형 MAC (TDMA, Polling, 토큰 패싱) 도입
         │    └─ (No)  ─> 초저전력 및 산발적인 센싱 데이터 전송인가? (IoT/RFID)
         │                 │
         │                 ├─> 노드 간 초정밀 시간 동기화(비콘 등) 지원이 가능한가?
         │                 │    ├─ (Yes) ─> Slotted ALOHA 채택 (성능 향상)
         │                 │    └─ (No)  ─> Pure ALOHA 기반 초경량 설계 (가장 저렴)
```
*해설*: 이 흐름의 핵심은 비용([동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 전력, 하드웨어)과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)(채널 효율) 사이의 트래픽 트레이드오프를 결정하는 것이다. 중앙 제어나 클럭 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)는 센서 노드의 배터리를 빠르게 갉아먹는다. 실무에서는 수동형 RFID 태그나 해저/지하 깊숙이 매설된 1회용 센서 등에서 구현 비용을 0으로 만들어야 할 때 순수 알로하 기반의 충돌 회피 변형 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 설계한다.

<strong>실무 <a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a> 및 실패 시나리오</strong>:
1. **트래픽 오버로드로 인한 붕괴**: 초당 채널 수용량(G)이 0.5를 넘어가는 설계 구간에서 순수 알로하를 고집하면, 재전송 횟수가 기하급수적으로 증가하는 '재전송 폭풍(Retransmission Storm)' 큐잉 병목이 발생하여 시스템 가용성이 완전히 0으로 수렴하게 된다.
2. <strong><a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a> 오류</strong>: 슬롯 알로하를 구현하려 했으나 클럭 오차가 발생해 사실상 순수 알로하처럼 동작해버리며 패킷 절단이 발생하는 아키텍처 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/).

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 순수 알로하를 고속망에 쓰는 것은 최첨단 물류 센터에서 작업자들에게 아무런 무전기를 주지 않고 각자 알아서 택배를 던지라고 지시하는 것과 같은 끔찍한 병목 설계입니다.

---

## Ⅴ. 기대효과 및 결론

순수 알로하는 네트워크 이론사에서 가장 아름다운 통계적 도전이었다. 효율은 처참하지만 복잡한 시스템의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 통제 메커니즘이 어떻게 진화해야 하는지 방향을 제시했다.

| 설계 철학적 의의 | 정량적 가치 | 정성적 가치 (영향력) |
|:---|:---|:---|
| [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/) [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/) 접근 | [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)(트래픽 낮을 때) 최저 | 제어 노드나 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 장애로부터 완전히 독립적 |
| 백오프 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 탄생 | 충돌 해소용 난수 로직 발명 | 이후 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) [CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CD의 필수 충돌 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 스탠다드로 발전 |

미래의 [6G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/419_6g_ntn_thz_ris_next_gen/) 환경 및 Massive [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) (초거대 [사물인터넷](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)) 시대에서는 수억 개의 디바이스가 동시에 신호를 뿜어낸다. 최근 학계에서는 순수 알로하의 극단적 단순함을 부활시키되, 딥러닝 기반으로 노드 스스로 패턴을 학습하여 충돌 없는 타이밍에 패킷을 쏘게 만드는 지능형 ALOHA(AI-enhanced ALOHA) 구조로 진화시키려는 연구가 활발히 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중이다. 순수 알로하는 결코 죽지 않고 가장 단순한 형태의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 통신 코어로 영원히 남을 것이다.

- **📢 섹션 요약 비유**: 순수 알로하는 컴퓨터 네트워크의 구석기 시대 '주먹도끼'입니다. 볼품없고 비효율적이었지만 이 도구가 있었기에 현대 통신망이라는 거대한 철기 시대가 도래할 수 있었습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 슬롯 알로하 ([Slotted ALOHA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/112_slotted_aloha/) | [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 타이밍을 통해 ALOHA의 취약 시간을 절반으로 줄인 기술) |
| [CSMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/104_csma/)/CD (Carrier Sense [Multiple Access](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/087_다중접속_Multiple_Access/) with [Collision Detection](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/106_CSMA_CD_유선이더넷_충돌감지/) | ALOHA에서 [반송파](/knowledge-base/studynote/03_network/01_data_communication/054_반송파_Carrier_Wave/) 감지와 충돌 검출 능력을 더한 유선 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 표준) |
| 이진 지수 백오프 (Binary Exponential Backoff | 충돌 시 대기 시간의 범위를 2의 지수승으로 늘려 혼잡을 완화하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) |
| 프레임 [전송 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/) ([Transmission Delay](/knowledge-base/studynote/03_network/01_data_communication/017_전송_지연/) | 취약 시간을 산정하는 절대적 기준이 되는 물리적 [전송 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/326_transfer_time/)) |
| [NOMA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/095_NOMA_비직교_다중_접속/) ([Non-Orthogonal Multiple Access](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/095_NOMA_비직교_다중_접속/) | 차세대 통신에서 충돌을 감수하면서 전력차를 이용해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 복원하는 비직교 다중접속) |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 노출 노드 문제]
    │
    ▼
[현재 개념: ALOHA]
    │
    ├──▶ [확장 A: Slotted ALOHA]
    └──▶ [확장 B: 지능형 자원 스케줄링]
```

ALOHA는 노출 노드 문제에서 출발해 현재 메커니즘을 정교화하고, 이후 [Slotted ALOHA](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/112_slotted_aloha/) 및 지능형 자원 스케줄링로 확장되는 흐름 속에서 이해하면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 아무런 규칙 없는 넓은 들판에서 여러 명의 친구가 갑자기 소리를 지르며 메시지를 전달하는 놀이예요.
2. 아무도 말 안 할 때 혼자 말하면 한 번에 전달되지만, 동시에 말하면 목소리가 부딪혀서 아무도 못 알아들어요.
3. 많이 부딪히면 효율이 뚝 떨어지지만, 누군가 허락해줄 때까지 기다릴 필요가 없어서 아주 빠르고 단순하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 231 / 1120

← **이전**: [1119. 6G 융합 테라헤르츠 예측 지표망](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1119_6g_convergence_terahertz_thz_network_indicators/)
**다음**: [1120. 위성 기반 도심항공교통(UAM) 라우팅 통신 구조 모델](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1120_uam_urban_air_mobility_satellite_routing/) →

---
