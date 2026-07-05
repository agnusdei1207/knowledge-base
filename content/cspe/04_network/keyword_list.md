---
title: "Keyword List"
date: "2026-07-05"
tags:
  - "cspe-network"
weight: 50
---
<컴퓨터 통신·네트워크 키워드 목록 (150제)>
컴퓨터시스템응용기술사 시험 출제동향 기반으로 엄선한 컴퓨터 통신·네트워크 핵심 키워드입니다.

---

## 1. 네트워크 기초 (12개)
1. OSI 7계층 모델 (OSI 7-Layer Model) — 물리·데이터링크·네트워크·전송·세션·표현·응용 7계층 참조 모델 [출제:120,125,134회]
2. TCP/IP 4계층 모델 (TCP/IP Model) — 네트워크 접근·인터넷·전송·응용 4계층 프로토콜 스택 [출제:120,125,128,129,132회]
3. 네트워크 프로토콜 3요소 (Protocol 3 Elements) — 구문(Syntax)·의미(Semantics)·타이밍(Timing) 3대 구성 요소 [출제:134회]
4. 이더넷 프레임 구조·IEEE 802.3 (Ethernet Frame) — 프리앰블·목적지·출발지·타입·데이터·FCS 구조 [출제:128,129회]
5. MAC 주소 구조 (MAC Address) — 48비트 물리 주소, OUI 및 NIC 고유 식별자
6. ARP·RARP (ARP RARP) — IP↔MAC 주소 변환 프로토콜, 역 ARP 동작 원리
7. VLAN·트렁크·액세스 포트 (VLAN Trunk Access Port) — 가상 LAN 분리, 802.1Q 태깅, 트렁크 포트 동작 [출제:138회]
8. STP·RSTP·PVST+ 루프 방지 (STP RSTP Loop Prevention) — 스패닝 트리 프로토콜, 브리지 루프 방지 메커니즘 [출제:138회]
9. 스위칭 계층 — L2·L3·L4·L7 스위치 (Network Switches) — 계층별 스위칭 원리 및 적용 범위 [출제:129회]
10. DHCP (DHCP) — IP 주소 자동 할당 프로토콜, DORA 과정
11. DNS 구조·동작 (DNS Domain Name System) — 도메인 네임 계층 구조, 반복·재귀 질의 동작
12. NAT·PAT (NAT PAT Network Address Translation) — 사설↔공인 IP 변환, 포트 주소 변환

## 2. IP 및 라우팅 (13개)
13. IP 주소 체계 — IPv4·IPv6 (IP Addressing IPv4 IPv6) — 32비트/128비트 주소 구조, 클래스풀·클래스리스
14. IPv6 전환 기술 (IPv6 Transition) — 듀얼 스택·터널링·변환 3대 전환 메커니즘
15. 서브네팅·CIDR (Subnetting CIDR) — 서브넷 마스크, 가변 길이 서브넷, 클래스리스 라우팅
16. 라우팅 기본 — 정적·동적 라우팅 (Routing Static Dynamic) — 수동 경로 설정 vs 프로토콜 기반 자동 경로 학습
17. 링크 상태 라우팅 — OSPF·OSPFv3 (OSPF Link State Routing) — Dijkstra 알고리즘 기반 최단 경로 라우팅 [출제:137회]
18. 거리 벡터 라우팅 — RIP·BGP (Distance Vector Routing RIP BGP) — 벨만-포드 기반, 홉 카운트 메트릭
19. BGP 경계 게이트웨이 프로토콜 (BGP Border Gateway Protocol) — AS 간 경로 교환, eBGP·iBGP 구분
20. MPLS 레이블 스위칭 (MPLS Label Switching) — 레이블 기반 고속 패킷 전달, LSP 경로 설정
21. ICMP·IGMP (ICMP IGMP) — 인터넷 제어 메시지 프로토콜, 멀티캐스트 그룹 관리 [출제:132회]
22. 로드 밸런서 L4·L7 (Load Balancer L4 L7) — 전송·응용 계층 부하분산, 세션 유지 방식 [출제:129회]
23. 멀티캐스트 — IGMP·PIM (Multicast IGMP PIM) — 그룹 통신, PIM-SM·PIM-DM 라우팅 [출제:132회]
24. 애니캐스트 라우팅 (Anycast Routing) — 동일 IP 다중 서버, 최근접 노드 라우팅
25. 패킷 캡처·프로토콜 분석 (Packet Capture Protocol Analysis) — Wireshark·tcpdump 기반 네트워크 트래픽 분석

## 3. 전송 계층 (13개)
26. TCP 3-way handshake (TCP 3-way Handshake) — SYN→SYN-ACK→ACK 연결 설정 과정 [출제:125,128,129,132회]
27. TCP 4-way handshake·연결 해제 (TCP 4-way Handshake) — FIN→ACK→FIN→ACK 연결 종료 과정 [출제:132회]
28. TCP 흐름 제어 — 슬라이딩 윈도우 (TCP Flow Control) — 수신 윈도우 크기 기반 송신 속도 조절 [출제:121,125회]
29. TCP 혼잡 제어 — AIMD·Slow Start (TCP Congestion Control) — 네트워크 혼잡 회피, cwnd 동적 조절 [출제:121회]
30. TCP vs UDP vs SCTP 비교 (TCP UDP SCTP Comparison) — 신뢰성·순서보장·멀티스트리밍 비교 [출제:129회]
31. UDP 특성·활용 사례 (UDP Characteristics) — 비연결형 경량 전송, 실시간 스트리밍·DNS 활용
32. QUIC·HTTP/3 (QUIC HTTP/3) — UDP 기반 전송 프로토콜, 0-RTT 연결 설정 [전망]
33. 오류 제어 — ARQ·Go-Back-N·SR (ARQ Error Control) — 자동 재전송 요청, 프레임 오류 복구 기법 [출제:128회]
34. 흐름 제어 — Slow Start·슬라이딩 윈도우 (Flow Control) — 송수신 속도 불일치 해결 메커니즘 [출제:125회]
35. 포트 번호·소켓 통신 (Port Socket Communication) — Well-known·Registered·Dynamic 포트, 소켓 API
36. TIME_WAIT 상태 (TIME_WAIT State) — TCP 종료 후 대기 상태, 2MSL 타이머 목적 [출제:132회]
37. TLS 1.3 핸드셰이크 (TLS 1.3 Handshake) — 1-RTT 핸드셰이크, 전방 비밀성(PFS) 강제 적용
38. mTLS 상호 인증 (mTLS Mutual TLS) — 서버·클라이언트 양방향 인증서 검증 [출제:136,138회]

## 4. 응용 계층 프로토콜 (5개)
39. HTTP/2·HTTP/3 비교 (HTTP/2 HTTP/3 Comparison) — 멀티플렉싱·서버 푸시·QUIC 기반 차이점 [출제:130회]
40. WebRTC (WebRTC) — 브라우저 간 P2P 실시간 음성·영상·데이터 통신 [출제:122회]
41. gRPC 고성능 RPC (gRPC High Performance RPC) — Protocol Buffers 기반 양방향 스트리밍 RPC [전망]
42. DNS over HTTPS·DNS over TLS (DoH DoT) — DNS 질의 암호화, 프라이버시 보호 프로토콜 [전망]
43. 글로벌 CDN 아키텍처 (Global CDN Architecture) — 콘텐츠 분산 배치, PoP·에지 캐싱 전략 [전망]

## 5. 무선 및 이동통신 (27개)
44. Wi-Fi 표준 — IEEE 802.11ax·802.11be (Wi-Fi Standards) — 고속 무선 LAN 표준 발전사 [출제:125,134회]
45. Wi-Fi 7 — MLO·6GHz 대역 (Wi-Fi 7) — 다중 링크 운용, 320MHz 채널 폭 [출제:134회]
46. OFDM·OFDMA 다중 접속 (OFDM OFDMA) — 직교 주파수 분할 다중화, 부반송파 할당 [출제:125회]
47. FHSS·DSSS 확산 스펙트럼 (FHSS DSSS) — 주파수 도약·직접 확산 방식 비교 [출제:126회]
48. 5G 핵심 기술 — eMBB·URLLC·mMTC (5G Core Technologies) — 초고속·초저지연·초연결 3대 시나리오 [출제:121,128,136회]
49. 5G SA 독립형·NSA 비독립형 (5G SA NSA) — 독립형 코어 vs 4G 코어 연동 아키텍처 [출제:135회]
50. 5G 코어 네트워크 SBA — AMF·SMF·UPF (5G Core SBA) — 서비스 기반 아키텍처, 네트워크 기능 분리 [출제:135회]
51. 5G 네트워크 슬라이싱 (5G Network Slicing) — 단일 물리망에서 다수 논리 네트워크 분리 운영 [출제:126,136,137회]
52. NSSAI·NSI·NSSI (NSSAI NSI NSSI) — 네트워크 슬라이스 선택 보조 정보 체계 [출제:137회]
53. 5G 특화망·로컬 5G (Private 5G Local 5G) — 기업 전용 5G 네트워크 구축·운영 [출제:126,136회]
54. 6G 핵심 기술 — 테라헤르츠·AI 네이티브 (6G Technologies) — 차세대 이동통신, Tbps급 전송 [출제:128,135회]
55. RIS 지능형 반사 표면 (Reconfigurable Intelligent Surface) — 전파 환경 능동 제어, 반사 빔 최적화 [출제:135회]
56. NTN 비지상 네트워크 — LEO 위성 (Non-Terrestrial Network) — 저궤도 위성 기반 3GPP 네트워크 확장 [출제:137회]
57. Open RAN·O-RAN (Open RAN) — 기지국 장비 개방형 인터페이스, 벤더 독립 [출제:132회]
58. MEC 모바일 엣지 컴퓨팅 (Mobile Edge Computing) — 기지국 인접 컴퓨팅, 초저지연 서비스 제공 [출제:121,132회]
59. 엣지 컴퓨팅 vs 포그 컴퓨팅 (Edge vs Fog Computing) — 데이터 발생지 근접 처리, 계층 구조 비교 [출제:125,126회]
60. 컴퓨팅 컨티뉴엄 — 클라우드·엣지·IoT (Computing Continuum) — 클라우드-엣지-디바이스 연속 컴퓨팅 환경 [출제:126회]
61. CBRS·민간 스펙트럼 (CBRS Private Spectrum) — 3.5GHz 대역 시민광대역 무선 서비스 [전망]
62. V2X 차량사물통신 (V2X Vehicle-to-Everything) — V2V·V2I·V2P·V2N 차량 통신 기술 [출제:138회]
63. C-V2X·DSRC 비교 (C-V2X DSRC) — 셀룰러 V2X vs 전용 단거리 통신 방식 비교 [출제:138회]
64. IEEE 802.11p WAVE (IEEE 802.11p WAVE) — 차량 환경 무선 접속, 고속이동 통신 표준 [출제:138회]
65. FANET 드론 애드혹 네트워크 (FANET Drone Network) — 무인기 간 자율 비행 네트워크 [출제:126회]
66. Ad-hoc 네트워크·AODV 라우팅 (Ad-hoc AODV) — 인프라 없는 자율 구성 네트워크, 반응형 라우팅 [출제:129회]
67. 블루투스 — BLE·Mesh (Bluetooth BLE Mesh) — 저전력 근거리 통신, 메시 네트워크 토폴로지
68. Zigbee·Thread·Matter (Zigbee Thread Matter) — 저전력 IoT 무선 표준, 스마트홈 상호운용 [출제:131회]
69. LoRa·LoRaWAN (LoRa LoRaWAN) — 장거리 저전력 LPWAN, LoRa 변조 기술 [전망]
70. NB-IoT·LTE-M (NB-IoT LTE-M) — 셀룰러 기반 LPWAN, 저전력 광역 IoT 통신 [전망]

## 6. SDN·NFV 및 네트워크 가상화 (10개)
71. SDN 소프트웨어 정의 네트워킹 (Software Defined Networking) — 제어 평면·데이터 평면 분리, 중앙 집중 제어 [출제:129,131회]
72. NFV 네트워크 기능 가상화 (Network Functions Virtualization) — 네트워크 장비 기능 소프트웨어화, NFVI 인프라 [출제:129,131회]
73. SDN 컨트롤러 — OpenFlow (SDN Controller OpenFlow) — 사우스바운드 인터페이스, 플로우 테이블 관리 [출제:129,131회]
74. VXLAN 오버레이 네트워크 (VXLAN Overlay) — 24비트 VNI 기반 L2 over L3 가상 네트워크 [출제:123회]
75. NaaS 네트워크서비스화 (Network as a Service) — 네트워크 기능 서비스형 제공, 온디맨드 프로비저닝 [출제:131회]
76. 오버레이·언더레이 네트워크 (Overlay Underlay Network) — 물리·논리 네트워크 분리, 터널 기반 통신 [전망]
77. EVPN·BGP EVPN (EVPN BGP) — 이더넷 VPN, 데이터센터 패브릭 L2/L3 통합 [전망]
78. 네트워크 자동화 — Ansible·RESTCONF·NETCONF (Network Automation) — IaC 기반 네트워크 설정 자동화
79. Intent-Based Networking (Intent-Based Networking) — 의도 기반 네트워킹, 정책 자동 해석·적용 [전망]
80. 쿠버네티스 네트워킹 — CNI·Ingress (Kubernetes Networking) — 파드 네트워크, 서비스 메시, Ingress 라우팅 [출제:127,137회]

## 7. VPN 및 네트워크 보안 (15개)
81. 방화벽 — 패킷 필터·상태기반·NGFW (Firewall Types) — 1~7세대 방화벽 발전, 차세대 방화벽 기능 [출제:129,137회]
82. IDS·IPS — 탐지 vs 차단 (IDS IPS) — 침입탐지·차단 시스템, 오용·이상 탐지 기법 [출제:129,134회]
83. 네트워크 스푸핑 — ARP·IP·DNS (Network Spoofing) — 주소 위조 공격 유형 및 대응 방안 [출제:128,134회]
84. DDoS 공격 기법·대응 — SYN Flood·증폭 (DDoS Attack Mitigation) — 분산 서비스 거부, 증폭·반사 공격 대응 [출제:125회]
85. 망분리 — 물리적·논리적 (Network Separation) — 업무망·인터넷망 분리, CBC 망분리 [출제:125회]
86. VPN — IPsec·SSL·WireGuard (VPN) — 터널링 기반 가상 사설망, 암호화 프로토콜 비교 [전망]
87. ZTNA vs VPN 비교 (ZTNA vs VPN) — 제로 트러스트 네트워크 접근 vs 전통 VPN 비교 [출제:130회]
88. SDP 소프트웨어 정의 경계 (Software Defined Perimeter) — 인가 전 연결 차단, 블랙 클라우드 모델 [출제:124회]
89. SASE — SD-WAN·CASB·SWG·ZTNA (SASE) — 네트워크+보안 통합 클라우드 서비스 프레임워크 [출제:135,136회]
90. SSE 보안 서비스 엣지 (Security Service Edge) — SASE 보안 기능 분리, SWG·CASB·ZTNA 통합 [출제:136회]
91. WAF 웹 애플리케이션 방화벽 (WAF Web Application Firewall) — SQL Injection·XSS 등 웹 공격 차단 [출제:129,137회]
92. CASB 클라우드 접근 보안 브로커 (CASB) — 클라우드 서비스 가시성·제어·보호 [출제:122,137회]
93. 융합 보안 관제 SIEM (SIEM Security Information Event Management) — 로그 수집·상관 분석·이벤트 관리 [출제:128,129,138회]
94. SOAR 보안 오케스트레이션 자동화 대응 (SOAR) — 보안 운영 자동화, 플레이북 기반 대응 [출제:127,138회]
95. SIEM vs SOAR 비교 (SIEM vs SOAR Comparison) — 탐지 중심 vs 대응 자동화, 상호보완 관계 [출제:138회]

## 8. 네트워크 관리·성능 (11개)
96. 위협 인텔리전스 — STIX·TAXII (Threat Intelligence STIX TAXII) — 사이버 위협 정보 표준화·자동 공유 체계 [출제:123,138회]
97. 네트워크 포렌식 증거 수집 (Network Forensics) — 네트워크 트래픽 기반 디지털 증거 분석 [출제:128,129회]
98. QoS — DiffServ·IntServ (QoS DiffServ IntServ) — 차별화·통합 서비스 품질 보장 모델
99. 트래픽 셰이핑·폴리싱 (Traffic Shaping Policing) — 토큰 버킷·리키 버킷 기반 트래픽 제어
100. 네트워크 성능 지표 — 지연·지터·대역폭·패킷 손실 (Network KPI) — 네트워크 품질 측정 핵심 메트릭
101. 네트워크 모니터링 — SNMP·NetFlow·sFlow (Network Monitoring SNMP NetFlow) — 장비 상태·트래픽 흐름 실시간 감시
102. 네트워크 관리 시스템 NMS (Network Management System) — FCAPS 모델 기반 통합 네트워크 관리
103. TCAM 삼진 CAM 고속 검색 (TCAM) — 0·1·X 매칭, 라우팅 테이블 고속 룩업 [출제:132회]
104. 네트워크 슬라이싱 가상화 자원 관리 (Network Slice Resource Management) — 슬라이스별 SLA 보장, 자원 격리 [출제:137회]
105. 5G SLA 보장 슬라이싱 (5G SLA Slicing) — 슬라이스 단위 SLA 정의·모니터링·보장 [전망]
106. 네트워크 접근 제어 NAC (Network Access Control) — 단말 인증·정책 기반 접근 제어 [전망]

## 9. 데이터 전송·통신 이론 (13개)
107. 채널 코딩 — 해밍·Reed-Solomon·터보 (Channel Coding) — 오류 검출·정정 부호화 기법 [출제:129회]
108. 소스 코딩 — 허프만·산술 (Source Coding) — 데이터 압축, 엔트로피 기반 부호화 [출제:129회]
109. 채널 용량 — 섀넌 한계 (Shannon Channel Capacity) — 섀넌-하틀리 정리, 최대 데이터 전송률 [출제:135회]
110. 변조 방식 — AM·FM·QAM·QPSK (Modulation Methods) — 아날로그·디지털 변조 기법 비교
111. MIMO·대규모 MIMO (MIMO Massive MIMO) — 다중 안테나 기술, 공간 다중화·빔포밍
112. 빔포밍 (Beamforming) — 지향성 안테나 빔 형성, 5G mmWave 핵심 기술 [전망]
113. 맨체스터 인코딩 (Manchester Encoding) — 비트 중앙 신호 천이, 자체 클럭 동기화 [출제:132회]
114. PDH·SDH·SONET 디지털 계위 (PDH SDH SONET) — 동기식 디지털 전송 계위, 프레임 구조 [출제:134회]
115. WDM·DWDM 광 다중화 (WDM DWDM) — 파장 분할 다중화, 광섬유 대역폭 확장
116. 광 인터넷 (Optical Internet) — 전광 교환 네트워크, OXC·OADM 기술 [전망]
117. HDLC 프레임 구조·동작 모드 (HDLC) — 비트 지향 데이터링크 프로토콜, NRM·ARM·ABM [출제:134회]
118. X.25·프레임 릴레이 (X.25 Frame Relay) — 패킷 교환 WAN 프로토콜, 가상 회선
119. ATM 비동기 전송 모드 (ATM Asynchronous Transfer Mode) — 53바이트 셀 기반, QoS 보장 전송

## 10. IoT 및 산업용 네트워크 (11개)
120. IoT 아키텍처 — 디바이스·게이트웨이·클라우드 (IoT Architecture) — IoT 3계층 참조 구조, 센서-게이트웨이-플랫폼
121. MQTT 경량 메시징 (MQTT) — Pub/Sub 기반 경량 IoT 메시징, QoS 3단계 [전망]
122. CoAP (CoAP Constrained Application Protocol) — RESTful 제약 환경 프로토콜, UDP 기반 [전망]
123. OPC UA 산업 표준 통신 (OPC UA) — 산업 자동화 상호운용성 프레임워크 [출제:137회]
124. Industrial IoT — IIoT (Industrial IoT) — 산업용 사물인터넷, 스마트 팩토리 네트워크 [출제:137회]
125. CAN 버스 자동차 통신 (CAN Bus) — 차량 내부 직렬 통신 버스, ECU 간 데이터 교환 [출제:129회]
126. SOME/IP 차량 이더넷 (SOME/IP Automotive Ethernet) — 차량용 서비스 지향 미들웨어, 이더넷 통신 [출제:138회]
127. TSN 시간 민감 네트워킹 (Time-Sensitive Networking) — IEEE 802.1 기반 실시간 이더넷, 결정적 지연 보장 [전망]
128. Profinet·EtherCAT (Profinet EtherCAT) — 산업용 실시간 이더넷 프로토콜 [전망]
129. 스마트 미터 AMI (Advanced Metering Infrastructure) — 원격 검침 인프라, 양방향 에너지 통신 [출제:126회]
130. 촉각 인터넷 (Tactile Internet) — 1ms 이내 초저지연, 원격 촉감 전달 기술 [출제:134회]

## 11. 차세대 네트워크 기술 (20개)
131. AI 네이티브 네트워킹 (AI-Native Networking) — AI/ML 기반 네트워크 자율 운영·최적화 [전망]
132. 네트워크 디지털 트윈 (Network Digital Twin) — 네트워크 가상 복제·시뮬레이션·예측 분석 [전망]
133. 위성 인터넷 — Starlink·저궤도 LEO (Satellite Internet LEO) — 저궤도 위성 군집 기반 글로벌 인터넷 [전망]
134. 양자 통신 네트워크 (Quantum Communication Network) — 양자 역학 기반 무조건 안전 통신 채널 [전망]
135. QKD 양자 키 분배 (Quantum Key Distribution) — 양자 채널 기반 암호키 분배, BB84 프로토콜 [출제:126회]
136. 분산 클라우드 네트워킹 (Distributed Cloud Networking) — 멀티 리전 분산 클라우드 네트워크 연결 [전망]
137. RDMA 원격 직접 메모리 접근 (RDMA) — CPU 바이패스 제로카피 네트워크 데이터 전송 [출제:138회]
138. RoCE — RDMA over Converged Ethernet (RoCE) — 이더넷 기반 RDMA, 데이터센터 고속 전송 [전망]
139. InfiniBand 클러스터 인터커넥트 (InfiniBand Cluster) — HPC·AI 클러스터 고대역폭 인터커넥트 [출제:138회]
140. NVLink 고대역폭 인터커넥트 (NVLink) — GPU 간 초고속 직접 연결, AI 학습 가속 [출제:138회]
141. 집합 통신 All-Reduce (All-Reduce Collective Communication) — 분산 학습 그래디언트 동기화 통신 패턴 [출제:138회]
142. 네트워크 기능 분리 — CU·DU·RU (Network Function Disaggregation) — 기지국 기능 중앙·분산·무선 유닛 분리 [출제:132회]
143. 가상 기지국 vRAN (Virtual RAN) — 범용 서버 기반 가상화 기지국, 클라우드 RAN [출제:132회]
144. Private LTE 전용망 (Private LTE) — 기업 전용 LTE 네트워크, 주파수 할당 [전망]
145. 스마트 홈 네트워크 통합 — Matter (Smart Home Network Matter) — IoT 기기 상호운용 표준, Thread 기반 [출제:131회]
146. 에너지 효율 네트워킹 — Green Networking (Green Networking) — 네트워크 장비 전력 절감, 탄소 중립 [전망]
147. RPKI 라우팅 보안 (RPKI Routing Security) — BGP 경로 원점 인증, ROA 검증 체계 [전망]
148. BGP 하이재킹 방지 (BGP Hijacking Prevention) — BGP 경로 탈취 공격 탐지·방어 기법 [전망]
149. 802.1X EAP 인증 (802.1X EAP Authentication) — 포트 기반 네트워크 접근 제어, RADIUS 연동 [출제:134회]
150. 포트 보안 — MAC Filtering (Port Security MAC Filtering) — 스위치 포트별 MAC 주소 제한, 비인가 차단
