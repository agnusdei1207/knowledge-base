+++
title = "466. HTTP/2 특징"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 특징은 응용 계층과 웹/메일에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 특징을 이해하면 응답 시간과 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

### 1. [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1의 절망과 꼼수 (Pain Point)
웹 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 하나를 띄우기 위해 100개의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 필요해지자, [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1의 파이프라이닝 기술은 앞선 요청이 늦어지면 뒤의 모든 요청이 꽉 막혀버리는 <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/">HOL</a>(<a href="/knowledge-base/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/">Head-of-Line</a>) 블로킹</strong>이라는 치명적 결함을 드러냈습니다.
- **개발자들의 고통**: 프론트엔드 개발자들은 이 막힘을 피하기 위해 100개의 작은 아이콘을 1개의 거대한 통짜 이미지 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 합치고(Image Sprite), CSS와 JS [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 억지로 한 줄로 병합(Concatenation)하는 등 <strong>'네트워크 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a>의 멍청함을 인간의 노가다(꼼수)로 커버하는 <a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/">기술 부채</a>'</strong>를 짊어져야만 했습니다.

### 2. 구글 SPDY와 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2의 탄생
구글(Google) 엔지니어들은 "이딴 꼼수를 쓰게 만들 바엔 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 심장 자체를 뜯어고치자"라며 자체적으로 <strong>SPDY(스피디)</strong>라는 실험적 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 만들었습니다.
- **필요성**: SPDY의 압도적인 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)에 충격을 받은 [IETF](/knowledge-base/studynote/03_network/12_iot_wpan_edge/635_ietf_core_working_group_coap/)(인터넷 표준화 기구)는 이를 그대로 가져와 다듬어서 <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/2 표준</strong>으로 공표했습니다. [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2는 기존의 `GET`, `POST`, 상태 코드 `200 OK` 등 개발자에게 익숙한 문법은 완벽히 유지하면서, 네트워크 선을 타는 '전송 방식'만 마법처럼 바꿔버린 혁명입니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">HTTP 1.1 HOL 블로킹</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">HTTP/2 특징</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">HTTP/2 스트림 다중화</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1은 "사람이 쓴 편지(텍스트)를 통째로 봉투에 넣어 보내는 방식"이어서, 앞사람의 택배 상자(용량이 큰 이미지)가 길을 막으면 뒤의 가벼운 편지들은 꼼짝없이 막혔습니다. [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2는 "모든 편지와 택배를 아주 작은 레고 블록(바이너리 프레임)으로 분해해서 파이프에 와르르 쏟아붓고, 도착지에서 다시 조립하는 방식"으로 진화하여 교통 체증을 완전히 없앴습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 바이너리 [프레이밍](/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/) 계층 (Binary [Framing](/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/) Layer)
[HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 아키텍처의 가장 위대한 발명품은 애플리케이션 계층 하단에 삽입된 '바이너리 [프레이밍](/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/) 계층'입니다. 여기서 두 가지 혁신적 개념이 등장합니다.
*   **메시지 (Message)**: 논리적인 하나의 요청(Request)이나 응답(Response). (예: `index.html` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))
*   **프레임 (Frame)**: 메시지를 잘게 쪼갠 이진수 덩어리. 각 프레임은 머리에 "나는 1번 메시지 출신이야"라는 고유 태그([Stream](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) ID)를 달고 있습니다.

### 2. 멀티플렉싱 ([Multiplexing](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)) 메커니즘
이 레고 블록(프레임)들을 섞어서 보내는 기술이 멀티플렉싱입니다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">HTTP/1.1 vs HTTP/2 멀티플렉싱 (Multiplexing) 아키텍처</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">HTTP/1.1 (HOL 블로킹 발생)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ 순서대로, 하나가 끝나야 다음 것을 보낼 수 있음 (기차 형태)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">====== 영상 응답 (크고 느림) ======</div><div class="kb-diagram-node">CSS 응답</div><div class="kb-diagram-node">JS 응답</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(CSS와 JS는 영상이 다 지나갈 때까지 대기실에서 무한 대기)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">HTTP/2 (멀티플렉싱 도입)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ 단 1개의 TCP 커넥션 안에서, 데이터를 '프레임'으로 쪼개서 뒤섞어버림!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">영상(3)</div><div class="kb-diagram-node">CSS(2)</div><div class="kb-diagram-node">영상(3)</div><div class="kb-diagram-node">JS(1)</div><div class="kb-diagram-node">영상(3)</div><div class="kb-diagram-node">CSS(2)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(수신지 브라우저의 조립 과정)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 어? 스트림 ID 1번 프레임이네? 모아서 JS 완성!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 어? 스트림 ID 2번 프레임이네? 모아서 CSS 완성!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 3번 영상 프레임은 천천히 조립 중... (하지만 CSS/JS는 이미 완료!)</div></div>
</div>
</div>



**[다이어그램 해설]** [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2에서는 큰 영상 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 작은 [CSS](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/110_unlicensed_lpwan_lorawan_sigfox/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 조각(프레임)들이 한 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/) 안에서 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 뒤섞여 날아갑니다(Interleaving). 따라서 무거운 영상이 통로를 독점하지 못하며, 가벼운 텍스트 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들이 먼저 도착해 브라우저에 렌더링되므로 <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a> 계층의 <a href="/knowledge-base/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/">HOL</a> 블로킹이 완벽하게 해결</strong>됩니다.

- **📢 섹션 요약 비유**: [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 특징의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

| 혁신 기술 포인트 | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1 | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 | 아키텍처적 가치 |
| :--- | :--- | :--- | :--- |
| **전송 방식** | 평문 (Text-based) | <strong>바이너리 (Binary <a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/">Framing</a>)</strong> | 파싱 오류 감소, 기계 친화적 고속 처리 |
| **요청/응답 방식** | 1 커넥션 = 1 요청 (파이프라이닝 실패) | <strong>1 커넥션 = 무제한 <a href="/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/">병렬</a> 요청 (<a href="/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/">Multiplexing</a>)</strong> | 수십 개의 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)을 뚫는 꼼수([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/)) 불필요 |
| <strong>헤더(Header) <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a></strong>| [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 없음 (매번 수백 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 낭비) | <strong>HPACK <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> (허프만 인코딩 및 중복 제거)</strong> | 모바일 환경 [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 극강 절약 |
| **클라이언트 개입** | 클라이언트가 무조건 먼저 요청해야 함 | <strong>서버 푸시 (<a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/469_http2_server_push/">Server Push</a>)</strong> | `index.html` 요청 시 서버가 알아서 `style.css`까지 쑤셔 넣어줌 |

### 치명적 트레이드오프 ([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [HOL](/knowledge-base/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) 블로킹의 잔존)
멀티플렉싱은 완벽해 보이지만, [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2도 피하지 못한 최악의 <strong>트레이드오프(Trade-off)</strong>가 있습니다. 바로 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2가 여전히 낡은 <strong>'<a href="/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a> <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a>'</strong> 위에 지어졌다는 사실입니다.
- <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a> <a href="/knowledge-base/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/">HOL</a> 블로킹의 재앙</strong>: [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 위해 단 1개의 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)만 씁니다. 그런데 무선망이 끊겨서 1만 개의 프레임 중 딱 <strong>1개의 프레임 패킷이 공중에서 유실(Loss)</strong>되면 어떻게 될까요?
- TCP의 스펙상, 잃어버린 1개 패킷이 재전송되어 도착할 때까지 <strong>나머지 9,999개의 프레임은 브라우저 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/">운영체제</a>(OS) <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 버퍼에 갇혀서 위로(앱으로) 올라가지 못하고 블로킹</strong>됩니다.
- 즉, 네트워크가 불안정한 환경(Wi-Fi <-> [LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/) 스위칭)에서는 오히려 [소켓](/knowledge-base/studynote/02_operating_system/02_process_thread/125_socket/)을 6개씩 뚫어 쓰던 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1보다 <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/2가 더 심하게 버벅거리는 치명적인 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 역전 현상</strong>이 발생합니다.

- **📢 섹션 요약 비유**: [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2는 "트럭([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)) 한 대에 모든 승객(수십 개의 요청)을 다 태우는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 시스템"입니다. 트럭 타이어에 펑크(패킷 유실)가 나면, 안에 탄 승객 수십 명이 한꺼번에 지각([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [HOL](/knowledge-base/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) 블로킹)하는 참사가 벌어집니다. 과거엔 택시 6대에 나눠 타서 1대가 펑크 나도 5대는 무사히 도착했지만 말입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

| 고려 사항 | 세부 내용 | 주요 아키텍처 의사결정 |
|:---|:---|:---|
| **도입 환경** | 기존 레거시 시스템과의 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 분석 | 마이그레이션 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 및 단계별 전환 계획 수립 |
| <strong>비용(<a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/012_roi_return_on_investment/">ROI</a>)</strong> | [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구축 비용(CAPEX) 및 운영 비용(OPEX) | [TCO](/knowledge-base/studynote/12_it_management/01_governance_strategy/016_tco/) 관점의 장기적 효율성 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| **보안/위험** | 컴플라이언스 준수 및 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성 보장](/knowledge-base/studynote/05_database/07_exam_summary/442_consistency_integrity/) | [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 기반 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/[인가](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 체계 연계 |

*(추가 실무 적용 가이드 - 프론트엔드 개발 패턴의 전면 수정)*
- [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2가 서버(Nginx, ALB)에 적용되면, 프론트엔드 개발자는 과거 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1 시절에 습관처럼 하던 꼼수들을 전부 제거([Refactoring](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/078_refactoring_code_smells/))해야만 합니다.
- **실무 의사결정**:
  1. **이미지 스프라이트(Image Sprite) 폐기**: 이미지를 합치지 말고 아이콘 100개를 잘게 쪼개서 그대로 둡니다. [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2는 멀티플렉싱으로 100개를 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 1초 만에 가져오며, 개별 이미지는 CDN에 완벽히 캐싱됩니다.
  2. <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/">샤딩</a>(<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">Domain</a> <a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/">Sharding</a>) 금지</strong>: 에셋을 `img1.com`, `img2.com`으로 분산시킬 필요가 없습니다. [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 나누면 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) Handshake 오버헤드만 증가합니다. 모든 에셋을 하나의 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 몰아넣어 단 1개의 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 커넥션 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 극대화해야 합니다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: 실무 적용은 "집을 지을 때 터를 다지고 자재를 고르는 과정"과 같이, 환경과 예산에 맞춘 최적의 선택이 필요합니다. "고속도로([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2)가 새로 뚫렸는데도 여전히 비포장도로 시절에 쓰던 산악용 지프차([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/))를 타고 덜컹거리며 달리는 것은 바보짓입니다. 고속도로에는 매끄러운 스포츠카(단일 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)/잘게 쪼갠 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))를 올려야 최고 속도가 나옵니다."

---

## Ⅴ. 기대효과 및 결론

1. <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/">gRPC</a> 인프라의 글로벌 표준화</strong>
   구글이 만든 현대 [MSA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/)([마이크로서비스 아키텍처](/knowledge-base/studynote/04_software_engineering/04_testing_quality/213_msa_microservices_architecture/))의 핵심 통신 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)인 <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/">gRPC</a></strong>는 내부적으로 완벽하게 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2를 엔진으로 사용합니다. [JSON](/knowledge-base/studynote/11_design_supervision/06_exam_summary/343_json/) 대신 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 버퍼([Protocol Buffers](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/535_sync_communication_rest_grpc/))로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)하고, [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2의 멀티플렉싱과 스트림 통신을 융합하여 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신 지연을 [REST API](/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) 대비 10배 이상 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)시킨 차세대 서버 통신 규격으로 세상을 지배하고 있습니다.

2. <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/3 (<a href="/knowledge-base/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/">QUIC</a>)으로의 필연적 이탈</strong>
   [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2가 TCP의 한계([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) [HOL Blocking](/knowledge-base/studynote/03_network/19_frequent_topics_terms/971_hol_blocking_head_of_line_tcp_http_delay/)) 때문에 펑크 난 트럭 신세가 되는 것을 견디지 못한 구글은, 아예 무거운 TCP를 버리고 UDP를 기반으로 새로운 통신 규격인 <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/">QUIC</a></strong>을 창조하여 <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/3</strong>를 선포했습니다. [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/3는 스트림마다 완전히 분리된 터널을 보장하여, 1번 프레임이 허공에서 날아가도 2번 프레임은 무사히 브라우저 화면에 도착하는 '진정한 무결점 멀티플렉싱' 시대를 완성했습니다.


## 🧠 지식 맵 ([Knowledge Graph](/knowledge-base/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))

*   <strong><a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/2 (RFC 7540) 핵심 혁신 요소</strong>
    *   <strong>바이너리 <a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/">프레이밍</a> 계층 (Binary <a href="/knowledge-base/studynote/03_network/04_data_link_layer_error/184_framing_mechanism/">Framing</a> Layer)</strong>: 텍스트([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1) -> 이진 프레임([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2)
    *   <strong>멀티플렉싱 (<a href="/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/">Multiplexing</a>)</strong>: 단일 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 내 논리적 스트림 기반 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 전송 ([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [HOL](/knowledge-base/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) 블로킹 타파)
    *   <strong>헤더 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a> (HPACK)</strong>: 상태 정보를 유지(Stateful)하는 허프만 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)
    *   <strong>서버 푸시 (<a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/469_http2_server_push/">Server Push</a>)</strong>: 클라이언트 요청 전 사전 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 캐시 전송
*   <strong><a href="/knowledge-base/studynote/11_design_supervision/03_gof_creational_structural/161_anti_pattern/">안티 패턴</a> (폐기해야 할 <a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/1.1 꼼수)</strong>
    *   [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [샤딩](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/280_sharding/) ([Domain](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [Sharding](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/243_sharding_horizontal_scaling_database/))
    *   에셋 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 병합 ([CSS](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/110_unlicensed_lpwan_lorawan_sigfox/)/JS Concatenation) 및 이미지 스프라이트
*   **아키텍처 한계 및 발전**
    *   한계: 패킷 유실 시 발생하는 <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/">TCP</a> <a href="/knowledge-base/studynote/03_network/19_frequent_topics_terms/971_hol_blocking_head_of_line_tcp_http_delay/">HOL Blocking</a></strong> 잔존
    *   발전: [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 기반의 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/3 ([QUIC](/knowledge-base/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/)) 등장 향후에는 지능형 애플리케이션 전달 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2는 기존의 낡은 철로([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)) 위에서 기차([프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/))만 초음속 KTX로 바꾼 위대한 과도기적 혁명이었습니다. 하지만 철로 자체가 낡았다는 사실을 깨달은 인류는, 이제 철로마저 자기부상([UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)/[QUIC](/knowledge-base/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/))으로 통째로 바꿔버리는 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/3 시대로 위대한 도약을 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 1.1 [HOL](/knowledge-base/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) 블로킹 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) ([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)) | 사용자 상태 유지와 요청 흐름을 묶는다. |
| 캐시 (Cache) | 응답 속도와 백엔드 부하에 직접 영향을 준다. |
| [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 스트림 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">선행 개념: HTTP 1.1 HOL 블로킹</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">현재 개념: HTTP/2 특징</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 A: HTTP/2 스트림 다중화</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">확장 B: 지능형 애플리케이션 전달</div></div>
</div>
</div>



[HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 특징는 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 1.1 [HOL](/knowledge-base/studynote/03_network/08_transport_layer/456_quic_hol_head_of_line_blocking_resolution/) 블로킹에서 출발해 현재 메커니즘을 정교화하고, 이후 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/2 스트림 [다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/071_다중화_Multiplexing/)와 지능형 애플리케이션 전달 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 이 기술은 마치 우리가 매일 사용하는 "스마트폰"과 같아요.
2. 복잡한 기계 장치들이 숨어 있지만, 우리는 화면만 터치하면 쉽게 원하는 것을 할 수 있죠.
3. 이처럼 보이지 않는 곳에서 시스템이 잘 돌아가도록 돕는 멋진 마법 같은 기술이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 587 / 1120

← **이전**: [465. HTTP 1.1 HOL 블로킹 (선행 응답 대기 지연)](/knowledge-base/studynote/03_network/09_application_layer_web_email/465_http_1_1_hol_blocking/)
**다음**: [467. HTTP/2 스트림 (Stream) 다중화 (Multiplexing)](/knowledge-base/studynote/03_network/09_application_layer_web_email/467_http2_stream_multiplexing_tcp_hol/) →

---
