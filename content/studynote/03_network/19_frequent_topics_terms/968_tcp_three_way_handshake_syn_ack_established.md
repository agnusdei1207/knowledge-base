+++
title = "968. TCP 쓰리웨이 핸드셰이크"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크는 빈출 주제와 용어에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크를 이해하면 구분 명확성과 설명력 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: TCP는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보내기 전, 반드시 출발지와 목적지 컴퓨터 사이에 가상의 터널(논리적 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 연결)을 먼저 튼튼하게 뚫어놓고 통신을 시작하는 **연결 지향형(Connection-oriented)** 프로토콜입니다.
- 이 터널을 뚫는 작업이 바로 3번 악수하기(3-Way Handshake)이며, 연결을 끊고 터널을 폭파할 때는 4번 악수(4-Way Handshake)를 합니다.

```text
[TCP 슬라이딩 윈도우]
    |
    v
[TCP 쓰리웨이 핸드셰이크]
    |
    +---> [혼잡 윈도우]
```

- **📢 섹션 요약 비유**: [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

클라이언트(내 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))가 네이버 서버 접속 시의 핑퐁 과정입니다. 이 단계에서 헤더의 깃발(Control [Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/): SYN, ACK)이 미친 듯이 활약합니다.

```text
[TCP 슬라이딩 윈도우]
    |
    v
[TCP 쓰리웨이 핸드셰이크]
    |
    +---> [혼잡 윈도우]
```

- **📢 섹션 요약 비유**: [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

- 내 PC가 네이버 웹서버(80번 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))로 첫 패킷을 쏩니다.
- 깃발([Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)): <strong>SYN (Synchronize, <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a>) <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a>를 1로 켭니다.</strong>
- 상태 전달: "나 패킷 번호표(Sequence Number) 100번부터 시작할 테니까 문 열 준비해 줘!"
- 내 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 상태: `SYN_SENT` (보내놓고 콩닥콩닥 기다림)

### 2단계: SYN + ACK (서버 ➜ 클라이언트) - "오케이 들어와! 넌 준비됐니?" 🌟
- 네이버 서버가 문 두드리는 소리를 듣고 반갑게 응답합니다.
- 깃발([Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)): <strong>SYN <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> 1, ACK(응답) <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> 1을 둘 다 켜서 보냅니다.</strong>
- 상태 전달: "네가 보낸 100번 잘 받았어(ACK 101). 내 쪽에서도 너한테 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보낼 건데, 내 번호표는 300번부터 시작할게(SYN 300). 알겠지?"
- 서버 상태: `SYN_RECEIVED` (반쪽짜리 연결 완료)

### 3단계: ACK (클라이언트 ➜ 서버) - "네! 저도 준비됐습니다! 통신 시작!"
- 내 PC가 서버의 응답을 최종 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 사살합니다.
- 깃발([Flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/)): <strong>ACK <a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a>만 1로 켜서 쏩니다.</strong>
- 상태 전달: "네가 말한 300번 잘 알겠어!(ACK 301) 이제 양쪽 다 뚫렸다!"
- 양쪽 컴퓨터 상태: <strong><code>ESTABLISHED (연결 확립 완벽 완료)</code></strong> 🌟
- 이 순간부터 진짜 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/), 웹페이지 등)가 쏟아져 나오기 시작합니다.

이 완벽하고 꼼꼼한 인사가 해커들에게 최악의 무기로 둔갑합니다.

- **해커의 약점 찌르기 (반쪽짜리 연결 상태 고갈)**:
  - 해커(좀비 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))가 네이버 서버로 1단계 `SYN(똑똑!)` 패킷만 1초에 1,000만 개를 무식하게 던집니다.
  - 착한 네이버 서버는 2단계 `SYN+ACK`를 돌려보내고, 3단계 `ACK`가 오기를 메모리 방 하나를 파놓고(`SYN_RECEIVED` 상태) 가만히 하염없이 3분 동안 기다립니다.
  - 하지만 해커는 3단계 `ACK`를 절대 보내주지 않고 도망가버립니다.
  - 네이버 서버는 빈방을 계속 잡고 기다리다가(백로그 큐 꽉 참) 램 메모리가 터져버려, 나중에 쳐들어온 진짜 착한 손님의 `SYN` 접속을 거부해 버립니다(서버 다운). 이게 바로 전설적인 <strong>디도스(DDoS)의 원조, SYN Flooding 공격</strong>입니다.

- <strong>방어책 (SYN <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/">Cookie</a>)</strong>: 서버가 "야, 3단계 대답(ACK) 확실히 오기 전까지는 내 소중한 메모리 빈방(상태 정보) 절대 내어주지 마!"라며 암호화된 쿠키만 던져주고 메모리를 아예 안 쓰는 꼼수([방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 차단망 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/))로 공격을 무력화시킵니다.

[TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 슬라이딩 윈도우가 기반 조건을 만든다면, [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크는 그 위에서 핵심 메커니즘을 구현하고, [혼잡 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/429_cwnd_congestion_window_concept/)는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 구분 명확성과 설명력에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 슬라이딩 윈도우의 기반 정리 | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크의 핵심 동작 | [혼잡 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/429_cwnd_congestion_window_concept/)의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 구분 명확성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: TCP의 3-Way Handshake는 무전기로 대화를 시작하는 <strong>'군대의 삼중 암구호 통신 의식'</strong>입니다. 김 병장(클라이언트)이 사령부(서버)에 다짜고짜 보고를 때리지 않습니다. **1단계(SYN)**: "사령부, 여기는 김 병장, 내 무전기 주파수 100번 맞췄다, 송신하라 오버!" **2단계(SYN+ACK)**: 사령부가 응답합니다. "김 병장, 100번 수신 양호하다. 나도 주파수 300번 맞췄다, 300번 들리는지 넌 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하라 오버!" **3단계(ACK)**: 김 병장이 마지막 쐐기를 박습니다. "사령부, 300번 쩌렁쩌렁하게 잘 들린다 오버! 양방향 통신 준비 완료(ESTABLISHED)!" 이 숨 막히게 답답한 3번의 암구호 교환(왕복 핑퐁)을 완벽하게 끝낸 뒤에야 비로소 진짜 기밀문서([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 입 밖으로 내뱉는, 속도보다는 100% 생존율([신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/))에 영혼을 바친 통신계의 절대 헌법입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 슬라이딩 윈도우 수준의 기본 대책으로 충분한지, 아니면 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 [혼잡 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/429_cwnd_congestion_window_concept/)와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 구분 명확성 부족인지, 설명력 악화인지 먼저 분리한다.
2. [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 [혼잡 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/429_cwnd_congestion_window_concept/)와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 슬라이딩 윈도우와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크는 빈출 주제와 용어를 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 구분 명확성 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [혼잡 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/429_cwnd_congestion_window_concept/), [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 슬라이딩 윈도우 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 정의 (Definition) | 용어의 시작점을 분명하게 만든다. |
| 비교 (Comparison) | 헷갈리는 개념의 경계를 드러낸다. |
| [혼잡 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/429_cwnd_congestion_window_concept/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: TCP 슬라이딩 윈도우]
    |
    v
[현재 개념: TCP 쓰리웨이 핸드셰이크]
    |
    +---> [확장 A: 혼잡 윈도우]
    +---> [확장 B: 컨텍스트 기반 용어 해석]
```

[TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 쓰리웨이 핸드셰이크는 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 슬라이딩 윈도우에서 출발해 현재 메커니즘을 정교화하고, 이후 [혼잡 윈도우](/knowledge-base/studynote/03_network/08_transport_layer/429_cwnd_congestion_window_concept/)와 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 비슷한 이름의 장난감을 헷갈리지 않게 표를 붙이는 것과 같아요.
2. 이 개념은 무엇이 어떻게 다른지 쉽게 구별하게 도와줘요.
3. 그래서 시험에서도 실무에서도 말을 더 정확하게 쓸 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 1089 / 1120

<- **이전**: [967. TCP 슬라이딩 윈도우](/knowledge-base/studynote/03_network/19_frequent_topics_terms/967_tcp_sliding_window_flow_control_buffer_management/)
**다음**: [969. 혼잡 윈도우 (Congestion Window)](/knowledge-base/studynote/03_network/19_frequent_topics_terms/969_congestion_window_cwnd_tcp_network_overload/) ->

---
