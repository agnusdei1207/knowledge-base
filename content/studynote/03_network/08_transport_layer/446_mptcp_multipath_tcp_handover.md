+++
title = "446. MPTCP (Multipath TCP)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MPTCP는 전송 계층에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: MPTCP를 이해하면 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 단일 전송 계층 연결([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) Connection) 내에서 다수의 물리적/논리적 경로(Path)를 동시에 사용하여 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 전송하는 [IETF](/knowledge-base/studynote/03_network/12_iot_wpan_edge/635_ietf_core_working_group_coap/) 표준 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 확장 (RFC 6824).
- **필요성**: 요즘 스마트폰은 와이파이 [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)와 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)를 동시에 켜고 있다. 그런데 일반 TCP는 이 두 개 중 하나만 선택해서 쓴다. (와이파이로 영화를 받으면 5G는 놀고 있다). "아니, 와이파이가 1Gbps고 5G가 1Gbps면, **두 개를 동시에 써서 2Gbps로 받으면 안 돼? 그리고 와이파이 끊길 때마다 넷플릭스 영상 멈추는 거 짜증 나는데, 5G가 백업으로 스무스하게 이어받게 할 수 없나?**" 이런 스마트폰 유저들의 간절한 염원이 MPTCP를 스마트폰 OS(iOS, Android)의 기본 탑재 기술로 만들었다.

- **💡 비유**: MPTCP는 <strong>"듀얼 배송 시스템"</strong>과 같습니다.
  - <strong>기존 <a href="/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a></strong>: 오토바이 1대만 써서 피자 10판을 배달합니다. 오토바이가 고장 나면 배달은 완전히 망합니다.
  - **MPTCP**: 오토바이(와이파이)와 트럭([5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)) 2대를 동시에 부릅니다. 피자 10판 중 5판은 오토바이에, 5판은 트럭에 나눠 싣습니다(서브플로우). 배달 속도가 2배로 빨라집니다. 만약 오토바이가 고장 나도 트럭에 남은 5판을 몰아 실으면 되니까 배달이 절대 취소([세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 끊김)되지 않습니다.

```text
[영 윈도우 탐색]
    │
    ▼
[MPTCP]
    │
    └──▶ [SCTP]
```

- **📢 섹션 요약 비유**: ** MPTCP는 **"양손잡이의 서류 작성"**입니다. 한 손(단일 경로)으로만 글씨를 쓰다가 손에 쥐가 나면 펜을 놓아야 했던 과거와 달리, 양손(다중 경로)에 펜을 쥐고 글씨를 써서 속도도 2배로 올리고 한쪽 손을 다쳐도 남은 손으로 멈춤 없이 글을 써 내려가는 궁극의 멀티태스킹입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

MPTCP는 기존의 낡은 방화벽이나 멍청한 라우터들을 속이기 위해, 겉보기엔 완벽한 일반 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 패킷인 척 위장한다.

### 1. 첫 번째 길 뚫기 (Primary Subflow)
통신을 시작할 때 스마트폰은 구글 서버에 똑같이 3-Way Handshake를 건다.
단, `SYN` 패킷의 빈칸(Option)에 <strong><code>MP_CAPABLE</code></strong> 이라는 비밀 암호를 적어 보낸다.
- 스마트폰: "나 와이파이(IP: `192.168.0.5`)로 통신 건다! 덧붙여서 나 MPTCP 할 줄 알아! (MP_CAPABLE)"
- 구글 서버: "오 나도 MPTCP 할 줄 알아! 일단 와이파이 길(Subflow 1)로 통신 시작하자!"

### 2. 두 번째 길 뚫기 (Secondary Subflow)
이제 스마트폰이 숨겨뒀던 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) [안테나](/knowledge-base/studynote/03_network/03_physical_layer_media/171_antenna_basic_dipole_resonance/)(IP: `211.x.x.x`)를 켠다.
- 스마트폰은 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) IP를 출발지로 삼아 구글 서버에 또 다른 3-Way Handshake를 건다.
- 이때 옵션 칸에는 `MP_CAPABLE`이 아니라 <strong><code>MP_JOIN</code></strong> 이라고 적어 보낸다.
- 스마트폰: "구글아, 나 아까 와이파이로 접속했던 그놈인데, 이번엔 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 길(Subflow 2)로 들어왔어. <strong>이 길도 아까 그 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/">세션</a>에 합류(<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/521_join/">Join</a>)시켜 줘!</strong>"
- 구글 서버: "오케이 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)! 이제 너랑 나 사이에는 길이 2개(와이파이, [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/)) 뚫렸다!"

### 3. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스케줄링과 조립 ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Sequence Number)
이제 구글은 1GB짜리 영화를 스마트폰에 쏜다.
- 구글은 1GB를 잘게 쪼개서, 500MB는 와이파이 길(Subflow 1)로, 나머지 500MB는 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 길(Subflow 2)로 동시에 쏟아붓는다 ([대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 결합).
- 스마트폰은 양쪽 길로 미친 듯이 들어오는 조각들을 받는다.
- **조립의 마법**: 1번 길로 온 조각과 2번 길로 온 조각의 순서가 섞이면 안 된다. 그래서 MPTCP는 기존 TCP의 `Seq Number` 위에 <strong><code>DSN (Data Sequence Number)</code></strong>라는 왕 대가리 번호표를 옵션 칸에 하나 더 붙여서 날린다. 이 DSN 덕분에 스마트폰은 두 길로 들어온 조각들을 100% 완벽하게 원상 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)(Reassembly)해 낸다.

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                MPTCP의 무단절 핸드오버 (Handover) 시나리오        │
 ├─────────────────────────────────────────────────────────────┤
 │                                                             │
 │   [ 내 스마트폰 ]                                 [ 넷플릭스 서버 ] │
 │                                                             │
 │   (Subflow 1: Wi-Fi) ════════(1Gbps 쌩쌩)════════▶        │
 │   (Subflow 2: 5G/LTE) ──────(대기 중 or 보조)──────▶        │
 │                                                             │
 │   * 상황: 내가 집을 나서서 엘리베이터를 탔다! (Wi-Fi 툭 끊김!!)        │
 │                                                             │
 │   * 일반 TCP: Wi-Fi 세션 터짐 ──▶ 넷플릭스 영상 멈춤 (로딩 뱅글뱅글)   │
 │                                                             │
 │   * MPTCP의 기적:                                            │
 │     "Wi-Fi 터졌어? 괜찮아! 이미 5G 터널(Subflow 2)이 묶여있잖아!   │
 │      넷플릭스야! 5G 터널 쪽으로 데이터 100% 다 돌려 쏴!!"             │
 │                                                             │
 │   ▶ 결과: 사용자는 화면의 끊김을 0.001초도 느끼지 못한 채 영상을 본다.│
 └─────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: ** MPTCP는 물탱크(서버)에 꽂힌 **"투 갈래 호스"**입니다. 원래는 굵은 정수기 호스(와이파이) 하나만 썼는데, 그 옆에 얇은 수도 호스([5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/))를 하나 더 꽂아 물통을 두 배 빨리 채웁니다. 그러다 정수기 호스가 꼬여서 막혀도, 남은 수도 호스에서 계속 물이 나오기 때문에 물통 채우기(다운로드) 작업이 중단되는 일은 절대 없습니다.

---

## Ⅲ. 비교 및 연결

MPTCP를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [영 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/445_zero_window_probe_persist_timer/) 탐색이 기반 조건을 만든다면, MPTCP는 그 위에서 핵심 메커니즘을 구현하고, SCTP는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [영 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/445_zero_window_probe_persist_timer/) 탐색의 기반 정리 | MPTCP의 핵심 동작 | SCTP의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: MPTCP는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 MPTCP를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [영 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/445_zero_window_probe_persist_timer/) 탐색 수준의 기본 대책으로 충분한지, 아니면 MPTCP가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 SCTP와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 부족인지, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 악화인지 먼저 분리한다.
2. MPTCP가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 SCTP와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- MPTCP의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [영 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/445_zero_window_probe_persist_timer/) 탐색와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: MPTCP를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

MPTCP는 전송 계층을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [SCTP](/knowledge-base/studynote/03_network/08_transport_layer/447_sctp_multi_stream_multi_homing_4way_handshake/), 적응형 저지연 전송, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 적응형 저지연 전송 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: MPTCP는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [영 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/445_zero_window_probe_persist_timer/) 탐색 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 세그먼트 ([Segment](/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/)) | 전송 계층이 다루는 기본 단위다. |
| [흐름 제어](/knowledge-base/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/) ([Flow Control](/knowledge-base/studynote/03_network/08_transport_layer/421_tcp_flow_control_sliding_window_algorithm/)) | 수신자 처리 속도를 넘지 않게 조절한다. |
| [SCTP](/knowledge-base/studynote/03_network/08_transport_layer/447_sctp_multi_stream_multi_homing_4way_handshake/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 영 윈도우 탐색]
    │
    ▼
[현재 개념: MPTCP]
    │
    ├──▶ [확장 A: SCTP]
    └──▶ [확장 B: 적응형 저지연 전송]
```

MPTCP는 [영 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/445_zero_window_probe_persist_timer/) 탐색에서 출발해 현재 메커니즘을 정교화하고, 이후 SCTP와 적응형 저지연 전송 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 물건을 보낼 때 받는 사람이 너무 빨리 받으면 놓칠 수 있어요.
2. 이 개념은 천천히 보낼지, 다시 보낼지, 길이 막히면 멈출지를 정해줘요.
3. 그래서 멀리 보내도 덜 잃어버리고 더 안정적으로 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 567 / 1120

← **이전**: [445. 영 윈도우 (Zero Window) 탐색](/knowledge-base/studynote/03_network/08_transport_layer/445_zero_window_probe_persist_timer/)
**다음**: [447. SCTP (Stream Control Transmission Protocol)](/knowledge-base/studynote/03_network/08_transport_layer/447_sctp_multi_stream_multi_homing_4way_handshake/) →

---
