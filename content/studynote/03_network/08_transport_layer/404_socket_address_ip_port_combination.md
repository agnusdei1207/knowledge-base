+++
title = "404. 소켓 주소 (Socket Address) = IP 주소 + 포트 번호"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)는 전송 계층에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)를 이해하면 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: IP 주소(네트워크 호스트 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/))와 [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)(호스트 내 프로세스 [식별](/knowledge-base/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/))를 결합하여 종단 간([End-to-End](/knowledge-base/studynote/03_network/08_transport_layer/401_transport_layer_role_end_to_end_multiplexing/)) 애플리케이션 통신 인터페이스를 정의하는 논리적 구조체.
- **필요성**: 우체국(라우터)은 IP 주소(집 주소)만 본다. 하지만 편지를 받는 사람 입장에서는, 엄마한테 온 건지 아빠한테 온 건지 [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)(수취인)가 필요하다. 만약 개발자가 네트워크 프로그램을 짤 때마다 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)이 어쩌고 [이더넷](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/230_ethernet_structure_and_principles_ieee_802_3/) 헤더가 어쩌고를 다 코딩해야 한다면 개발자들은 미쳐버릴 것이다. <strong>"야! 복잡한 1~3계층 통신 원리는 윈도우 OS가 다 알아서 해줄 테니까, 개발자 너희들은 그냥 'IP주소랑 <a href="/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/">포트 번호</a>(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/">소켓</a>)' 두 개만 딱 적어서 그 구멍으로 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 쑤셔 넣어! 그럼 우리가 알아서 포장해서 던져줄게!"</strong>라는 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)([Abstraction](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/))의 극한이 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소다.

- **💡 비유**: [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)([Socket](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)) 주소는 말 그대로 전기 벽면의 <strong>"돼지코 콘센트"</strong>와 같습니다.
  - 발전소(인터넷 망)에서 복잡한 전선(IP, [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/))을 타고 전기가 옵니다.
  - 하지만 집 안에서 선풍기(프로그램)를 켜려면, 그냥 벽에 뚫린 동그란 <strong>콘센트 구멍(<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/">소켓</a>)</strong>에 플러그([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))만 딱 꽂으면 끝입니다.
  - 이 220V 콘센트 구멍의 이름표가 바로 <strong><code>우리아파트(IP) : 거실 1번 구멍(Port)</code></strong>인 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소입니다. 선풍기(프로그램)는 발전소가 어딨는지 몰라도 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)에만 꽂으면 전기가 통합니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">Well-Known 포트, Registere…</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">소켓 주소 = IP 주소 + 포트 번호</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">TCP</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: <strong> <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/">소켓</a> 주소는 우편물 겉면에 적힌 </strong>"서울특별시 강남구 테헤란로 123 (IP 주소), 101동 502호 ([포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/))"**라는 풀네임(완전체) 주소입니다. 이 두 개가 합쳐져야만 택배 기사가 아파트 경비실(라우터)을 거쳐 내 방문 앞(프로그램)까지 물건을 정확히 내려놓을 수 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 5-Tuple (통신의 5가지 지문)
네트워크 장비나 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)이 하나의 대화 흐름([세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/))을 완벽하게 특정하기 위해 지문처럼 검사하는 5가지 요소의 묶음이다. 이 중 4개가 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소의 결합이다.

1. **출발지 IP 주소** (`10.1.1.1` - 내 [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/))
2. <strong>출발지 <a href="/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/">포트 번호</a></strong> (`50001` - 내 크롬 창)
   ▶ *(1+2) 합쳐서 = 나의 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소*
3. **목적지 IP 주소** (`8.8.8.8` - 구글 서버)
4. <strong>목적지 <a href="/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/">포트 번호</a></strong> (`443` - 구글 암호화 웹서버)
   ▶ *(3+4) 합쳐서 = 너의 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소*
5. <strong><a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong> (`TCP` 또는 `UDP` - 전송 방식)

[방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)(Stateful [Firewall](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))은 이 5개의 숫자를 테이블에 메모해 두고, 이 숫자가 완벽히 똑같은 패킷들이 1시간 동안 왔다 갔다 하면 "아, 얘네 아까부터 계속 수다 떨고 있는 1개의 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/))이구나!"라고 판단하여 검사 없이 프리패스로 통과시켜 준다.

### 2. 서버의 동시 접속 마법 (Fork)
네이버 서버 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)는 `80번` 하나뿐이다. 그런데 한국 사람 1,000만 명이 동시에 접속한다. [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)가 1개인데 어떻게 충돌이 안 날까?
- [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)의 정의 때문이다. 터널은 "출발지 + 목적지"의 조합으로 이루어진다.
- 유저 A: `1.1.1.1:50000` ────▶ `네이버IP:80` (1번 터널)
- 유저 B: `2.2.2.2:40000` ────▶ `네이버IP:80` (2번 터널)
- 유저 A가 탭을 하나 더 엶: `1.1.1.1:50001` ────▶ `네이버IP:80` (3번 터널)
- **결과**: 네이버 웹서버(80번)는 가만히 앉아있지만, 들어오는 놈들의 "출발지 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소"가 전부 다르기 때문에, 운영체제는 1,000만 개의 각기 다른 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)([소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/))를 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)(Fork)해서 하나하나 독립적으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쏴준다. 절대로 A의 카톡이 B에게 잘못 가는 일은 없다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">소켓 프로그래밍(코딩)의 극단적 요약 흐름</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">서버 개발자</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. socket() : "OS야 빈 콘센트 구멍 하나 만들어줘"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. bind(80) : "이 콘센트에 80번 이라는 이름표를 붙일게"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3. listen() : "이제 손님 올 때까지 귀 열고 대기 탄다!"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4. accept() : "오! 손님 왔다! 1:1 비밀 통로 파서 대화 시작!"</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">클라이언트(유저)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1. socket() : "나도 빈 콘센트 하나 줘"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2. connect(네이버IP:80) : "저쪽 80번 콘센트로 냅다 전기 꽂아버려!!"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ "이 6줄의 코드로 전 세계 수십억 대의 컴퓨터가 인터넷을 한다!"</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: <strong> <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/">소켓</a> 주소 묶음(5-Tuple)은 은행의 </strong>"1:1 창구 상담표"**입니다. 내 주민번호(출발지 IP), 대기표 번호(출발지 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)), 창구 직원 이름(목적지 IP), 창구 창구 번호(목적지 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/))가 완벽히 매칭되어야만 두 사람만의 프라이빗한 상담([세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/))이 시작되며, 옆 창구 사람과 절대 대화가 섞이지 않습니다.

---

## Ⅲ. 비교 및 연결

[소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. Well-Known [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), Registere…가 기반 조건을 만든다면, [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)는 그 위에서 핵심 메커니즘을 구현하고, TCP는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | Well-Known [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), Registere…의 기반 정리 | [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)의 핵심 동작 | TCP의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 Well-Known [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), Registere… 수준의 기본 대책으로 충분한지, 아니면 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 TCP와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 부족인지, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 악화인지 먼저 분리한다.
2. [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 TCP와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- Well-Known [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), Registere…와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)는 전송 계층을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/), 적응형 저지연 전송, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 적응형 저지연 전송 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Well-Known [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), Registere… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 세그먼트 ([Segment](/knowledge-base/studynote/03_network/08_transport_layer/407_tcp_segment_header_structure_20_60_bytes/)) | 전송 계층이 다루는 기본 단위다. |
| [흐름 제어](/knowledge-base/studynote/03_network/04_data_link_layer_error/213_flow_control_buffer_overflow/) ([Flow Control](/knowledge-base/studynote/03_network/08_transport_layer/421_tcp_flow_control_sliding_window_algorithm/)) | 수신자 처리 속도를 넘지 않게 조절한다. |
| [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: Well-Known 포트, Registere…</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: 소켓 주소 = IP 주소 + 포트 번호</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: TCP</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 적응형 저지연 전송</div></div>
</div>
</div>



[소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 주소 = IP 주소 + [포트 번호](/knowledge-base/studynote/03_network/08_transport_layer/402_port_number_16bit_application_process_identification/)는 Well-Known [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/), Registere…에서 출발해 현재 메커니즘을 정교화하고, 이후 TCP와 적응형 저지연 전송 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 물건을 보낼 때 받는 사람이 너무 빨리 받으면 놓칠 수 있어요.
2. 이 개념은 천천히 보낼지, 다시 보낼지, 길이 막히면 멈출지를 정해줘요.
3. 그래서 멀리 보내도 덜 잃어버리고 더 안정적으로 도착해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 525 / 1120

← **이전**: [403. Well-Known 포트 (0~1023), Registered 포트 (1024~49151), Dynamic 포트 (49152~65535)](/knowledge-base/studynote/03_network/08_transport_layer/403_port_categories_well_known_registered_dynamic/)
**다음**: [405. TCP (Transmission Control Protocol)](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) →

---
