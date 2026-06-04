---
title: "437. TCP NewReno / SACK (선택적 확인응답 옵션, 블록 다중유실 회복)"
date: "2026-05-08"
tags:
  - "studynote-network"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK는 전송 계층에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK를 이해하면 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 단일 윈도우 내 다중 패킷 손실(Multiple Packet Loss) 발생 시 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) Reno의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하(다중 Fast Recovery로 인한 CWND 급감 및 [Timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/))를 방지하기 위해 개선된 [혼잡 회피](/studynote/03_network/08_transport_layer/432_congestion_avoidance_aimd_algorithm/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(NewReno)과 확장 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 헤더 옵션(SACK).
- **필요성**: 1Gbps 초고속망이 되니까 한 번에 쏘는 윈도우 크기가 1,000개가 넘었다. 해저 케이블에서 노이즈가 살짝 튀면 1,000개 중 5개가 듬성듬성 유실된다. Reno는 이 5개를 잃어버릴 때마다 속도를 1/2, 1/4, 1/8, 1/16, 1/32로 미친 듯이 깎아 먹다가 아예 뻗어버렸다([Timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/)). **"야! 1,000개 보낸 것 중에 5개 잃어버린 건 '한 번의 사고'잖아! 왜 속도를 5번이나 깎아! 그리고 잃어버린 것만 딱딱 집어서 알려주면 내가 한 방에 다 다시 쏴줄 텐데 굳이 누적 ACK로 사람 숨 막히게 할 거야?!"** 이 절규가 SACK과 NewReno를 탄생시켰다.

- **💡 비유**:
  - **Reno (구형)**: 택배 100개를 시켰는데 10번과 20번이 안 왔습니다. 고객은 "10번 안 왔어!"라고 1차 클레임을 겁니다(속도 삭감). 회사가 10번을 보내줍니다. 그제야 고객은 "20번도 안 왔어!"라고 2차 클레임을 겁니다(속도 또 삭감). 배송 회사는 암 걸립니다.
  - **SACK (새로운 유형의)**: 고객이 택배를 받자마자, <strong>"1~9번 오케이, <a href="/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/">11</a>~19번 오케이, 21~100번 오케이!"라고 영수증에 형광펜으로 칠해서(SACK 블록)</strong> 보냅니다. 배송 회사는 영수증을 딱 보고, <strong>"아 10번이랑 20번 2개가 비었네? 한 번에 퀵으로 쏴줄게! (속도 삭감은 1번만)"</strong>라며 눈부신 처리를 보여줍니다.

```text
[TCP Reno 모델]
    |
    v
[TCP NewReno / SACK]
    |
    +---> [TCP BIC / CUBIC]
```

- **📢 섹션 요약 비유**: <strong> SACK(선택적 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a> 응답)은 시험지 채점을 할 때 "너 3번 틀렸어 다시 풀어와" 하고 다시 풀어오면 "7번도 틀렸어 다시 풀어와" 하는 꼰대 선생님(Reno)의 방식을 부수고, </strong>처음부터 "너 3번이랑 7번 틀렸어!"라고 한 번에 채점표를 쥐여주는 1타 강사의 명쾌한 족집게 과외**입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. NewReno의 융통성 (Partial ACK 판별법)
SACK 옵션이 켜져 있지 않은 낡은 PC들 사이에서도 다중 유실을 막기 위해 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 코드를 살짝 고친 것이 NewReno다.
- **Reno의 바보짓**: 유실된 10번을 재전송하고, 수신자가 `ACK 20`을 보내면 "오 10번 잘 갔네! [Fast Recovery](/studynote/03_network/08_transport_layer/434_fast_recovery_skip_slow_start/) 끝! 정상 주행!" 하고 샴페인을 터뜨렸다. 그런데 바로 다음 순간 `20번`이 없다고 징징대면 "헐? 새 사고 터졌네? 또 절반 깎자!"
- **NewReno의 눈치**: 수신자가 `ACK 20`을 보냈다 치자. NewReno는 샴페인을 안 터뜨린다. "잠깐만. 내가 아까 창문(Window) 하나에 100번까지 꽉꽉 채워 보냈는데, 쟤가 왜 100번을 불렀다 안 하고 20번을 부르지? **아! 아까 10번 날아갈 때 20번 놈도 같이 바다에 빠진 거구나 (Partial ACK 감지)!!**"
- **조치**: NewReno는 이 상황을 '새로운 사고'로 안 보고, <strong>'아까 난 사고 수습 중(<a href="/studynote/03_network/08_transport_layer/434_fast_recovery_skip_slow_start/">Fast Recovery</a> <a href="/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/">진행</a> 중)'</strong>으로 간주하여 속도(CWND)를 깎지 않고 20번을 부드럽게 재전송해 준다.

### 2. 궁극의 치트키 SACK (Selective Acknowledgment)
[TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 통신을 처음 맺을 때(SYN [패킷 교환](/studynote/03_network/05_lan_wan_l2_devices/276_packet_switching_vs_circuit_switching_message_switching/)), `Options` 구역에 "나 SACK 지원함!"이라고 합의를 마친다.
- **SACK Block의 구조**: 수신자는 기본 영수증(`ACK=10`)을 보내면서, 헤더 꼬리표(Option)에 4개의 블록을 더 적어 보낼 수 있다.
  - "기본적으로 10번까지 받았어. (근데 11번이 안 왔어)"
  - "[SACK Option]: 근데 나 15~20번은 받았고, 25~30번도 받았어!"
- **송신자의 광속 재전송**: 이 엽서를 받은 송신자는 머리를 1초도 안 굴리고, 뻥 뚫려있는 빈 공간인 <strong><a href="/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/">11</a>~14번과 21~24번 패킷만 핀셋으로 쏙쏙 뽑아내어 한 방에 재전송</strong>해 버린다.
- 결과적으로 [타임아웃](/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)([Timeout](/studynote/02_operating_system/05_deadlock/319_timeout_prevention/)) 따위는 절대 구경할 수 없는 무적의 다운로드 속도가 유지된다.

```text
 +-------------------------------------------------------------+
 |                와이어샤크(Wireshark)에서 SACK 블록 훔쳐보기        |
 +-------------------------------------------------------------+
 |                                                             |
 |   [ 일반 TCP 헤더 영역 ]                                       |
 |   Acknowledgment number: 1000  <-- "나 999까지 받았어! 1000번 내놔!" |
 |                                                             |
 |   [ Options 영역 (SACK 켜짐) ]                                 |
 |   TCP SACK Option:                                          |
 |     - SACK Left Edge: 1500                                  |
 |     - SACK Right Edge: 2000 <-- "근데 1500~1999번은 잘 도착해 있어!" |
 |                                                             |
 |   -> 송신자의 행동: "오케이! 너 1000번부터 1499번까지만 잃어버렸구나!  |
 |                   내가 그 구간만 핀셋으로 뽑아서 지금 당장 쏴줄게!!"  |
 +-------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: ** SACK은 치과 의사가 쓰는 **"충치 파노라마 엑스레이"**입니다. 환자(수신자)가 "이빨 아파요(기본 ACK)"라고 징징댈 때, 의사(송신자)가 이빨을 하나하나 두드려가며 아픈 곳을 찾는 게(Reno) 아니라, 엑스레이(SACK 블록) 사진 한 장 딱 보고 **"아, 왼쪽 어금니 두 개 썩었네" 하고 정확히 그 두 곳만 0.1초 만에 핀셋 치료(재전송)를 끝내버리는 현대 의학의 기적**입니다.

---

## Ⅲ. 비교 및 연결

[TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [TCP Reno](/studynote/03_network/08_transport_layer/436_tcp_reno_fast_retransmit_recovery/) 모델이 기반 조건을 만든다면, [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK는 그 위에서 핵심 메커니즘을 구현하고, [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) BIC / CUBIC는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [TCP Reno](/studynote/03_network/08_transport_layer/436_tcp_reno_fast_retransmit_recovery/) 모델의 기반 정리 | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK의 핵심 동작 | [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) BIC / CUBIC의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [TCP Reno](/studynote/03_network/08_transport_layer/436_tcp_reno_fast_retransmit_recovery/) 모델 수준의 기본 대책으로 충분한지, 아니면 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) BIC / CUBIC와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 부족인지, [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 악화인지 먼저 분리한다.
2. [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) BIC / CUBIC와의 연계 방식을 함께 검증한다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [TCP Reno](/studynote/03_network/08_transport_layer/436_tcp_reno_fast_retransmit_recovery/) 모델와의 경계를 정리하지 않아 중복 투자나 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK는 전송 계층을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) BIC / CUBIC, 적응형 저지연 전송, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 적응형 저지연 전송 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [TCP Reno](/studynote/03_network/08_transport_layer/436_tcp_reno_fast_retransmit_recovery/) 모델 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 세그먼트 ([Segment](/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/)) | 전송 계층이 다루는 기본 단위다. |
| [흐름 제어](/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/) ([Flow Control](/studynote/03_network/08_transport_layer/421_tcp_flow_control_sliding_window_algorithm/)) | 수신자 처리 속도를 넘지 않게 조절한다. |
| [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) BIC / CUBIC | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: TCP Reno 모델]
    |
    v
[현재 개념: TCP NewReno / SACK]
    |
    +---> [확장 A: TCP BIC / CUBIC]
    +---> [확장 B: 적응형 저지연 전송]
```

[TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NewReno / SACK는 [TCP Reno](/studynote/03_network/08_transport_layer/436_tcp_reno_fast_retransmit_recovery/) 모델에서 출발해 현재 메커니즘을 정교화하고, 이후 [TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) BIC / CUBIC와 적응형 저지연 전송 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 물건을 보낼 때 받는 사람이 너무 빨리 받으면 놓칠 수 있어요.
2. 이 개념은 천천히 보낼지, 다시 보낼지, 길이 막히면 멈출지를 정해줘요.
3. 그래서 멀리 보내도 덜 잃어버리고 더 안정적으로 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 558 / 1120

<- **이전**: [436. TCP Reno (빠른 재전송/빠른 회복 지원) 모델](/studynote/03_network/08_transport_layer/436_tcp_reno_fast_retransmit_recovery/)
**다음**: [438. TCP BIC / CUBIC](/studynote/03_network/08_transport_layer/438_tcp_bic_cubic_modern_linux_congestion_control/) ->

---
