+++
title = "ENQ / ACK / NAK / EOT 제어 문자"
date = 2026-03-03

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

> **핵심 인사이트 3줄**
> 1. ENQ·ACK·[NAK](/knowledge-base/studynote/03_network/04_data_link_layer_error/211_nak_negative_acknowledgement/)·EOT는 [BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/)(Binary [Synchronous](/knowledge-base/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/) Communication) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 핵심 제어 문자로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 링크 계층의 회선 확보·긍정/부정 응답·전송 종료를 담당한다.
> 2. 이 제어 문자 체계는 반이중 통신에서 양방향 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 교환을 위한 기본 핸드셰이킹 메커니즘의 원형이며, 현대 [ARQ](/knowledge-base/studynote/03_network/19_frequent_topics_terms/949_arq_automatic_repeat_request_go_back_n_selective/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)의 직접적 선조다.
> 3. TCP의 SYN/ACK, HTTP의 요청/응답, Modbus [RTU](/knowledge-base/studynote/09_security/18_iot_ot_physical/897_rtu_remote_terminal_unit/) 등 현대 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)에서도 같은 개념이 다른 형태로 살아있다.

---

## Ⅰ. [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 제어 문자 개요

[BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/)(Binary [Synchronous](/knowledge-base/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/) Communication)에서 사용하는 제어 문자는 <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/">ASCII</a> 코드 표준(1963)</strong>으로 정의된 비인쇄 문자들이다.

| 문자  | [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) | 이름                      | 기능        |
|------|-------|--------------------------|------------|
| ENQ  | 0x05  | Enquiry (문의)            | 회선 확보 요청 |
| ACK  | 0x06  | Acknowledgement (긍정 응답) | 수신 성공 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| [NAK](/knowledge-base/studynote/03_network/04_data_link_layer_error/211_nak_negative_acknowledgement/)  | 0x15  | [Negative Acknowledgement](/knowledge-base/studynote/03_network/04_data_link_layer_error/211_nak_negative_acknowledgement/) | 수신 오류, 재전송 요청 |
| EOT  | 0x04  | End of Transmission (전송 종료) | 회선 해제 |
| STX  | 0x02  | Start of Text           | 본문 시작 |
| ETX  | 0x03  | End of Text             | 본문 종료 |
| SYN  | 0x16  | [Synchronous](/knowledge-base/studynote/03_network/01_data_communication/010_동기식_비동기식_전송/) [Idle](/knowledge-base/studynote/02_operating_system/10_security/611_cpu_idle_wait_optimization/)        | 동기 유지 |

📢 **섹션 요약 비유**: 제어 문자는 전화 예절 코드다 — "통화 가능?" (ENQ), "네" (ACK), "잘 못 들었어요" ([NAK](/knowledge-base/studynote/03_network/04_data_link_layer_error/211_nak_negative_acknowledgement/)), "끊을게요" (EOT).

---

## Ⅱ. [BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 전송 시퀀스

### 정상 전송 시나리오



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">송신 측 수신 측</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ENQ →</div><div class="kb-diagram-cell">(회선 확보 요청)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">← ACK</div><div class="kb-diagram-cell">(회선 사용 허가)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">STX</div><div class="kb-diagram-node">데이터</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">(블록 1 전송)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">← ACK</div><div class="kb-diagram-cell">(블록 1 수신 확인)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">STX</div><div class="kb-diagram-node">데이터</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">(블록 2 전송)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">← ACK</div><div class="kb-diagram-cell">(블록 2 수신 확인)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">EOT →</div><div class="kb-diagram-cell">(전송 종료)</div></div>
</div>
</div>



### 오류 발생 시나리오 ([NAK](/knowledge-base/studynote/03_network/04_data_link_layer_error/211_nak_negative_acknowledgement/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-note">STX</div><div class="kb-diagram-node">데이터</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">(블록 전송)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">← NAK</div><div class="kb-diagram-cell">(CRC 오류 감지)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">STX</div><div class="kb-diagram-node">데이터</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">(동일 블록 재전송)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">← ACK</div><div class="kb-diagram-cell">(재전송 성공)</div></div>
</div>
</div>



📢 **섹션 요약 비유**: [BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/) 전송 시퀀스는 소포 배달 절차다 — 벨 누르기(ENQ), 문 열기(ACK), 소포 전달, 사인(ACK), 영수증 끊기(EOT). 내용물이 파손되면 NAK로 재배송 요청.

---

## Ⅲ. ACK0 / ACK1 — 교대 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 응답

BSC에서는 오류 감지를 위해 <strong>ACK0과 ACK1을 교대로 사용</strong>해 블록 번호를 구분한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">블록 1 전송 → ACK1 수신 (홀수 블록 확인)</div>
<div class="kb-diagram-note">블록 2 전송 → ACK0 수신 (짝수 블록 확인)</div>
<div class="kb-diagram-note">블록 3 전송 → ACK1 수신 (홀수 블록 확인)</div>
<div class="kb-diagram-note">...</div>
</div>
</div>



이는 <strong>Stop-and-Wait ARQ의 1비트 순서번호</strong>와 동일한 원리다.

📢 **섹션 요약 비유**: ACK0/ACK1 교대는 홀수·짝수 수업 시간 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)이다 — 1교시(ACK1), 2교시(ACK0)처럼 번갈아가며 체크해 빠진 수업이 있는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.

---

## Ⅳ. ENQ/ACK에서 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)/IP까지 — 발전 계보



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">BSC ENQ/ACK (1960년대)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">HDLC I-Frame/S-Frame (1970년대) — 더 효율적인 비트 지향</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">TCP SYN/ACK (1974년~) — 연결 지향, 스트림 기반</div>
<div class="kb-diagram-note">3-Way Handshake: SYN → SYN-ACK → ACK</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">QUIC (2018~) — UDP + ACK, 0-RTT, 손실 기반 혼잡 제어</div>
</div>
</div>



### 현대 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)과의 대응

| [BSC](/knowledge-base/studynote/12_it_management/01_governance_strategy/019_bsc/) 제어 문자 | 현대 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 대응            |
|-------------|------------------------------|
| ENQ         | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) SYN / [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 요청           |
| ACK         | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) ACK / [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 200 OK         |
| [NAK](/knowledge-base/studynote/03_network/04_data_link_layer_error/211_nak_negative_acknowledgement/)         | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) NACK / [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 400·500      |
| EOT         | [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) FIN / [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) Connection: close |

📢 **섹션 요약 비유**: ENQ/ACK는 전화 대화의 원형이다 — "여보세요?"(ENQ), "예"(ACK), "못 들었어요"([NAK](/knowledge-base/studynote/03_network/04_data_link_layer_error/211_nak_negative_acknowledgement/)), "끊을게요"(EOT). 인터넷도 결국 같은 대화 구조다.

---

## Ⅴ. Modbus [RTU](/knowledge-base/studynote/09_security/18_iot_ot_physical/897_rtu_remote_terminal_unit/) — 산업 현장의 ENQ/ACK

산업 자동화에서는 <strong>Modbus <a href="/knowledge-base/studynote/09_security/18_iot_ot_physical/897_rtu_remote_terminal_unit/">RTU</a> <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a></strong>이 ENQ/ACK 개념을 계승한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">마스터(PLC) 슬레이브(센서/액추에이터)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">──</div><div class="kb-diagram-node">주소</div><div class="kb-diagram-node">기능코드</div><div class="kb-diagram-node">데이터</div><div class="kb-diagram-node">CRC</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">(ENQ 역할)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">←</div><div class="kb-diagram-node">주소</div><div class="kb-diagram-node">기능코드</div><div class="kb-diagram-node">데이터</div><div class="kb-diagram-node">CRC</div><div class="kb-diagram-note">│ (ACK 역할)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">←</div><div class="kb-diagram-node">주소</div><div class="kb-diagram-node">오류코드</div><div class="kb-diagram-node">CRC</div><div class="kb-diagram-note">│ (NAK 역할: 예외 응답)</div></div>
</div>
</div>



현대 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)·[SCADA](/knowledge-base/studynote/09_security/18_iot_ot_physical/894_scada/)·스마트팩토리에서도 이 원리가 기반이 된다.

📢 **섹션 요약 비유**: Modbus는 공장 무전기 통신이다 — "1번 로봇, 현재 온도 알려줘"(마스터 요청), "온도 75도"(슬레이브 응답). ENQ/ACK 구조가 공장 자동화에 살아있다.

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">ENQ / ACK / NAK / EOT</div>
<div class="kb-diagram-tree-item" style="--depth:0">프로토콜 컨텍스트</div>
<div class="kb-diagram-note">── BSC (Binary Synchronous Communication)</div>
<div class="kb-diagram-tree-item" style="--depth:0">기능</div>
<div class="kb-diagram-note">── ENQ: 회선 확보 요청</div>
<div class="kb-diagram-note">── ACK (ACK0/ACK1): 긍정 응답</div>
<div class="kb-diagram-note">── NAK: 부정 응답, 재전송 요청</div>
<div class="kb-diagram-note">── EOT: 전송 종료, 회선 해제</div>
<div class="kb-diagram-tree-item" style="--depth:0">발전 계보</div>
<div class="kb-diagram-note">── HDLC I/S/U 프레임</div>
<div class="kb-diagram-note">── TCP SYN/ACK/FIN</div>
<div class="kb-diagram-note">── HTTP Request/Response</div>
<div class="kb-diagram-tree-item" style="--depth:0">산업 응용</div>
<div class="kb-diagram-tree-item" style="--depth:2">Modbus RTU</div>
<div class="kb-diagram-tree-item" style="--depth:2">SCADA 프로토콜</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">ENQ/ACK/NAK/EOT 발전 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1960년대</div><div class="kb-diagram-cell">BSC·ASCII 정의</div><div class="kb-diagram-cell">제어 문자 체계 표준화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1970년대</div><div class="kb-diagram-cell">HDLC 비트 지향</div><div class="kb-diagram-cell">ACK→RR, NAK→REJ 으로 발전</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1974년</div><div class="kb-diagram-cell">TCP 등장</div><div class="kb-diagram-cell">SYN/ACK 3-Way Handshake</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1980년대</div><div class="kb-diagram-cell">Modbus RTU</div><div class="kb-diagram-cell">산업 자동화에 ENQ/ACK 계승</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2000년대</div><div class="kb-diagram-cell">HTTP/SMTP</div><div class="kb-diagram-cell">요청/응답 패러다임 지배적</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2018년</div><div class="kb-diagram-cell">QUIC/HTTP3</div><div class="kb-diagram-cell">ACK 최적화, 0-RTT 핸드셰이크</div></div>
<div class="kb-diagram-note">핵심 키워드 연결:</div>
<div class="kb-diagram-note">ENQ → 회선 확보 → ACK → 데이터 전송 → EOT</div>
<div class="kb-diagram-note">오류 폴링 긍정응답 NAK 재전송</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">TCP 3-way → HTTPS → REST API 요청/응답</div>
</div>
</div>



---

## 👶 어린이를 위한 3줄 비유 설명

1. ENQ는 "지금 전화해도 돼?"라는 문자다 — 통화를 시작하기 전에 상대방이 받을 수 있는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
2. ACK는 "잘 받았어", NAK는 "다시 보내줘"다 — 편지가 제대로 도착했는지(ACK) 또는 찢어졌는지([NAK](/knowledge-base/studynote/03_network/04_data_link_layer_error/211_nak_negative_acknowledgement/))를 알려준다.
3. EOT는 "이제 끊을게"다 — 전화 통화를 마치고 회선을 끊겠다고 정중하게 알리는 신호다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 33 / 1120

← **이전**: [회선 제어 규약 (Line Control Protocol)](/knowledge-base/studynote/03_network/01_data_communication/032_회선_제어_규약/)
**다음**: [에러 검출 방식 — 패리티·CRC·해밍코드](/knowledge-base/studynote/03_network/01_data_communication/034_에러_검출율/) →

---
