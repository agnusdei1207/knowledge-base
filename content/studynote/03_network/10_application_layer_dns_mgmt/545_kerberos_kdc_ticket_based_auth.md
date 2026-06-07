---
title: "Kerberos"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 545
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 커버로스는 이름 해석과 네트워크 관리에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: 커버로스를 이해하면 가시성과 관리 자동화 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 커버로스는 MIT의 프로젝트 아테나([Project](/studynote/05_database/01_db_architecture_relational/042_relational_algebra_project/) Athena)에서 개발된 클라이언트-서버 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다([UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 88 사용). 이름의 유래인 그리스 신화 속 지옥 문을 지키는 머리 셋 달린 개(케르베로스)처럼, 클라이언트, 서버, 그리고 이 둘을 중재하는 신뢰 기관인 <strong><a href="/studynote/09_security/12_identity_threat_advanced/583_kdc/">KDC</a> (<a href="/studynote/09_security/12_identity_threat_advanced/583_kdc/">Key Distribution Center</a>)</strong>라는 3개의 주체로 구성된다.
- **필요성**: 수천 명의 대학생과 수백 대의 공용 컴퓨터가 얽힌 네트워크에서, 사용자가 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(예: 프린터 서버)에 접속할 때마다 패스워드를 보내면 스니핑(Sniffing)에 의해 계정이 쉽게 털린다. 서버 입장에서도 "접속 요청자가 진짜 그 학생인지" 믿을 수 없고, 클라이언트 입장에서도 "저 서버가 해커가 만든 가짜 위장 서버가 아닌지" 믿을 수 없다. 따라서 "둘 다 믿을 수 없으니, 우리가 모두 신뢰하는 막강한 제3자([KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/))가 도장을 찍은 보증서(티켓)만 통과시키자"라는 개념이 절실했다.
- **등장 배경**: ① [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 인터넷의 평문 패스워드 전송(Telnet, [FTP](/studynote/03_network/09_application_layer_web_email/482_ftp_file_transfer_protocol/) 등)에 따른 치명적 계정 탈취 빈발 -> ② 대칭키 암호학의 발전 및 티켓 기반 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 도입 -> ③ Windows 2000 이후 [Active](/studynote/03_network/09_application_layer_web_email/483_active_vs_passive_ftp/) Directory의 기본 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로 채택되면서 글로벌 엔터프라이즈 환경의 지배적 표준으로 등극.

```text
+-------------------------------------------------------------+
|             기존 인증 방식의 취약점 vs 커버로스의 철학 시각화       |
+-------------------------------------------------------------+
|                                                             |
|   [과거: 무지성 패스워드 전송]                                   |
|   Client ----- "나 앨리스야, PW: 1234" -------> File Server |
|             (해커가 중간에서 가로채면 끝!)                         |
|                                                             |
|   [혁신: 커버로스 티켓(Ticket) 인증]                           |
|   Client ----- "KDC야, 나 앨리스인데 파일 서버 접속할래" ---+ |
|   Client <----- "앨리스 맞네. 여기 암호화된 [티켓] 가져가" --+ |
|        |                                                    |
|        +------- "나 앨리스야, 이거 KDC가 준 [티켓]!" -----> File Server |
|                                                             |
|   => 클라이언트는 파일 서버에 비밀번호를 절대 보내지 않음! 티켓만 제시함!   |
+-------------------------------------------------------------+
```

**[다이어그램 해설]** 이 도식은 커버로스가 네트워크 스니핑의 근본적인 위험을 어떻게 우회하는지 직관적으로 보여준다. 해커가 네트워크 중간에 숨어 패킷을 가로채더라도, 패킷 안에는 비밀번호가 없다. 오직 KDC라는 중앙 서버가 특정 사용자(앨리스)와 특정 목적지([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버) 사이에서만 제한된 시간 동안 쓸 수 있게 만들어준 고도의 암호화된 '입장권(Ticket)' 덩어리만 돌아다닐 뿐이다. 따라서 비밀번호 노출의 위험이 원천 차단된다.

- **📢 섹션 요약 비유**: 클럽(서버)마다 일일이 신분증과 지문을 대조하지 않고, 믿을 수 있는 중앙 매표소([KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/))에서 한 번 빡세게 신분 검사를 한 뒤 '위조 불가능한 놀이공원 자유이용권 손목 띠(티켓)'를 채워주면, 어느 놀이기구를 타든 손목 띠만 보여주고 바로 타는 것([SSO](/studynote/09_security/11_iam_access_control/531_sso/))과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소 (KDC와 두 가지 티켓)

| 요소명 | 역할 | 내부 구조 및 특징 | 비유 |
|:---|:---|:---|:---|
| <strong><a href="/studynote/09_security/12_identity_threat_advanced/583_kdc/">KDC</a> (<a href="/studynote/09_security/12_identity_threat_advanced/583_kdc/">Key Distribution Center</a>)</strong> | 신뢰할 수 있는 제3자 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 기관 | 사용자/서버의 모든 비밀번호(마스터키)를 저장한 철옹성 | 경찰청 신원 보증 센터 |
| <strong><a href="/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/">AS</a> (<a href="/studynote/09_security/12_identity_threat_advanced/584_as/">Authentication Server</a>)</strong> | [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 신원 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | [KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/) 내의 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/). 최초 로그인 시 아이디/비밀번호를 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하여 TGT를 발급 | 종합 출입증 발급소 |
| <strong><a href="/studynote/09_security/12_identity_threat_advanced/585_tgs/">TGS</a> (<a href="/studynote/09_security/12_identity_threat_advanced/585_tgs/">Ticket Granting Server</a>)</strong> | 개별 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 티켓 발급 | [KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/) 내의 [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/). TGT를 보여주면 특정 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(메일, DB 등) 전용 티켓으로 교환해줌 | 놀이기구 전용 탑승권 교환소 |
| <strong><a href="/studynote/09_security/12_identity_threat_advanced/586_tgt/">TGT</a> (Ticket-Granting Ticket)</strong> | "티켓을 발급받을 수 있는 권한을 증명하는 마스터 티켓" | AS가 KDC의 마스터키로 암호화하여 클라이언트에게 부여. 클라이언트는 내용 해독 불가 | 놀이공원 자유이용권 팔찌 |
| **타임스탬프 (Timestamp)** | [재전송 공격](/studynote/09_security/03_network_security/274_replay_attack/)([Replay Attack](/studynote/09_security/03_network_security/274_replay_attack/)) 방어 | 패킷이 생성된 시간이 암호문에 포함됨. 지정된 오차(보통 5분)를 넘으면 티켓 무효화 처리 | 유효기간이 적힌 버스표 |

### 커버로스 티켓 교환의 6단계 대서사시 (매우 중요)

커버로스 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 과정은 크게 3단계의 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 흐름(총 6번의 메시지 교환)으로 완성된다. 복잡해 보이지만 "안전하게 입장권을 얻어가는 과정"으로 이해하면 된다.

```text
+---------------------------------------------------------------+
|               커버로스 (Kerberos) 티켓 기반 6단계 인증 흐름        |
+---------------------------------------------------------------+
|                                                               |
|   [클라이언트(Client)]                                [KDC 서버] |
|      |                                                    |   |
|      |  ① AS_REQ: "저 앨리스인데요, 놀이공원(KDC) 입장할래요"   |   |
|      +---------------------------------------------------->|   |
|      |  ② AS_REP: "ㅇㅋ, 여기 [TGT 티켓]이랑 [세션키 1] 가져가" |   |
|      |<----------------------------------------------------+   |
|      |                                                    |   |
|      |  ③ TGS_REQ: "[TGT] 제출 + 파일 서버(B) 접근권 좀 주세요" |   |
|      +---------------------------------------------------->|   |
|      |  ④ TGS_REP: "ㅇㅋ, 여기 [파일서버 전용 티켓] + [세션키 2]"|   |
|      |<----------------------------------------------------+   |
|      |                                                    |   |
|      v                                                    |   |
|   [파일 서버(Server B)]                                      |   |
|      |  ⑤ AP_REQ: "나 앨리스야, KDC가 준 [전용 티켓] 여기 있어" |   |
|      |<----------------------------------------------------+   |
|      |  ⑥ AP_REP: "티켓 맞네, 나 가짜 서버 아니니 안심하고 들어와"|   |
|      +---------------------------------------------------->|   |
|      |                                                    |   |
|      |  ==== [인증 완료! 이 순간부터 안전한 데이터 통신 시작] ====   |
+---------------------------------------------------------------+
```

**[다이어그램 해설]** 클라이언트가 최초로 로그인할 때(①, ②), KDC의 [AS](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/)([인증 서버](/studynote/09_security/12_identity_threat_advanced/581_authentication_server/))는 클라이언트의 비밀번호로 해독할 수 있는 암호 상자를 던져준다. 만약 사용자가 진짜 앨리스라면 자신의 비밀번호로 상자를 열어 `TGT(마스터 티켓)`와 `세션키 1`을 획득한다. 이제 앨리스는 특정 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버에 접속하고 싶을 때마다 매번 비밀번호를 칠 필요 없이, 이 `TGT`를 [TGS](/studynote/09_security/12_identity_threat_advanced/585_tgs/)(티켓 발급 서버)에게 보여주어(③, ④) 목적지 전용 티켓을 발급받는다. 최종적으로 앨리스는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버에게 이 전용 티켓을 제시(⑤)하며, 서버 역시 KDC와 공유한 마스터키로 티켓을 열어보고 "음, KDC가 보증한 앨리스가 맞군" 하며 문을 열어준다(⑥). 이 과정에서 서로의 신원이 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)되는 '상호 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Mutual Authentication](/studynote/09_security/12_identity_threat_advanced/588_mutual_authentication/))'이 완성된다.

- **📢 섹션 요약 비유**: 처음 정문에 들어갈 때만 깐깐하게 신분증(비밀번호)을 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)받고 '자유이용권([TGT](/studynote/09_security/12_identity_threat_advanced/586_tgt/))'을 찹니다. 그다음부터는 롤러코스터([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)서버), 범퍼카(메일서버)를 탈 때 자유이용권만 보여주면 놀이기구 관리자(서버)가 의심 없이 바로 태워주는 완벽한 원스톱 시스템입니다.

---

## Ⅲ. 비교 및 연결

네트워크 아키텍트가 가장 많이 헷갈리는 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 기술 간의 포지셔닝을 비교한다.

| 비교 기준 | [NTLM](/studynote/09_security/12_identity_threat_advanced/594_ntlm/) (구형 윈도우) | Kerberos (현대 사내망/AD) | Oauth 2.0 / SAML (웹/클라우드) |
|:---|:---|:---|:---|
| **설계 환경** | 낡은 로컬 LAN (신뢰 수준 낮음) | **거대한 엔터프라이즈 사내망 (AD)** | 개방된 인터넷(Web/[HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)) 및 클라우드 |
| <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> <a href="/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/">중재자</a></strong> | 서버가 직접 사용자 암호 해시 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | <strong>강력한 <a href="/studynote/09_security/12_identity_threat_advanced/583_kdc/">KDC</a>(티켓 발급소)가 중앙 중재</strong> | [IdP](/studynote/09_security/11_iam_access_control/536_idp_identity_provider/) ([Identity Provider](/studynote/09_security/11_iam_access_control/536_idp_identity_provider/), [Okta](/studynote/09_security/11_iam_access_control/551_okta_idaas/)/Google 등) |
| **크리덴셜 릴레이** | 해시 재사용 공격([Pass-the-Hash](/studynote/09_security/12_identity_threat_advanced/592_pth/))에 극도로 취약함 | **티켓 구조 + 타임스탬프로 재전송 원천 차단** | 짧은 수명의 토큰(Access Token) 사용 |
| <strong>상호 <a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> 여부</strong> | 클라이언트만 서버에 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) | **서버도 클라이언트에게 자신이 진짜임을 증명** | 주로 토큰 소지자([Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/)) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)에 특화 |
| **사용처 사례** | 레거시 호환성을 위해 억지로 남겨둠 | 사내 [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 로그인, 공유 폴더(SMB), [하둡](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 클러스터 | 구글 계정으로 다른 사이트 가입하기, 클라우드 [SSO](/studynote/09_security/11_iam_access_control/531_sso/) |

커버로스는 사내 폐쇄망([온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)) 생태계에서 왕이다. [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 컨트롤러(DC)와 단단히 묶인 윈도우 생태계에서는 커버로스 없이 한 발짝도 나아갈 수 없다. 하지만 커버로스는 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 같은 웹 환경이나 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 너머의 외부망에서는 작동하기 어렵기 때문에(엄격한 IP 제한과 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 이슈), 밖으로 나갈 때는 Oauth나 SAML 같은 웹 기반 토큰 아키텍처로 옷을 갈아입어야 한다.

```text
+---------------------------------------------------------------+
|               타임스탬프(Timestamp) 기반 재전송 공격 방어 원리      |
+---------------------------------------------------------------+
|                                                               |
|   [해커의 Replay Attack 시도]                                   |
|   1. 해커가 네트워크에 몰래 숨어 앨리스가 서버로 보내는 [티켓]을 복사함. |
|   2. 30분 뒤, 해커가 복사한 [티켓]을 서버로 그대로 다시 쏘아 로그인 시도!|
|                                                               |
|   [서버의 커버로스 방어 로직 작동]                                 |
|   서버: "티켓 열어보자. 앗? 이 티켓에 찍힌 시간이 30분 전이잖아?"        |
|   서버 정책: [현재 서버 시간]과 [티켓 발급 시간] 오차가 5분 이상이면 차단! |
|   서버: "네놈은 해커구나! 이 티켓은 폐기된 티켓이다!" (접속 거부 --> Drop)|
|                                                               |
|   => 결론: 커버로스 환경에서는 KDC, 클라이언트, 서버 간의 시간(NTP)이 |
|            정확히 일치하지 않으면 정상 사용자도 통신이 거부된다.       |
+---------------------------------------------------------------+
```

**[다이어그램 해설]** 커버로스의 가장 빛나는 아이디어 중 하나는 암호학에 '시간(Time)'이라는 변수를 섞어 넣은 것이다. 해커가 패킷을 스니핑해서 암호문을 가로채더라도 그 안의 내용은 풀 수 없다. 그래서 해커들은 풀기를 포기하고, 그 암호문 덩어리 자체를 그대로 서버에 다시 던지는 '[재전송 공격](/studynote/09_security/03_network_security/274_replay_attack/)([Replay Attack](/studynote/09_security/03_network_security/274_replay_attack/))'을 쓴다. 커버로스는 암호문(티켓과 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)자) 내부에 발급 당시의 '타임스탬프'를 박아 넣었다. 서버는 자신이 받은 패킷의 타임스탬프가 현재 시간과 5분 이상 차이 나면 무조건 폐기해버린다. 따라서 커버로스를 쓰는 인프라에서는 단 1초의 오차도 없애기 위해 [NTP](/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/)([Network Time Protocol](/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/), 536번 문서) 서버와의 엄격한 시간 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)가 절대적인 필수 요건이다.

- **📢 섹션 요약 비유**: 해커가 버려진 영화관 입장권을 주워서 다음 날 다시 몰래 들어가려 했지만, 입장권에 '오늘 오후 2시 발급(유효기간 5분)'이라고 도장이 쾅 찍혀 있어서 입구 컷을 당하는 완벽한 티켓 방어술입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. **상황**: 대기업의 [Active Directory](/studynote/09_security/11_iam_access_control/548_active_directory/) (AD) [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 컨트롤러 서버 관리자 계정이 [피싱](/studynote/09_security/15_malware_attack_vectors/752_phishing/) 메일을 통해 해커에게 넘어갔다. 해커는 AD 내부를 뒤져 커버로스의 심장이라 할 수 있는 '[KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/) 마스터키(krbtgt 계정 해시)'를 통째로 빼돌렸다.
2. **원인 (골든 티켓 공격)**: KDC의 마스터키(krbtgt)를 손에 쥔 해커는, [KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/) 서버를 거치지 않고 자신의 노트북에서 마음대로 '10년짜리 마스터 티켓([TGT](/studynote/09_security/12_identity_threat_advanced/586_tgt/))'을 무한정 찍어낼 수 있게 된다. 이를 <strong>골든 티켓 공격(<a href="/studynote/09_security/12_identity_threat_advanced/590_golden_ticket/">Golden Ticket</a> Attack)</strong>이라 부르며, 이 순간 회사의 모든 서버, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 이메일은 해커의 손아귀에 합법적으로 떨어지게 된다.
3. **의사결정 및 긴급 조치**:
   - 침해가 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)된 즉시, 보안 아키텍트는 AD 환경에서 `krbtgt` 계정의 비밀번호를 <strong>2회 연속으로 강제 변경(Reset)</strong>해야 한다. (비밀번호 히스토리 무효화).
   - 이렇게 하면 기존 마스터키로 만들어진 모든 위조 티켓(골든 티켓)들이 일제히 무효화되어 해커의 연결이 끊긴다.
   - 이후, 권한 있는 관리자가 [KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/)([도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 컨트롤러)에 접근할 때는 반드시 망이 분리된 전용 관리 터미널(PAW, Privileged Access Workstation)에서만 접근하도록 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 정책을 세워 [KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/) 마스터키 탈취의 뿌리를 뽑는다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/">NTP</a> <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a> 아키텍처 필수 점검</strong>: 커버로스 도입 시 가장 빈번하게 발생하는 장애의 90%는 "원인을 알 수 없는 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 실패"다. 이는 서버나 클라이언트 중 한 대의 시계가 메인 [NTP](/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/) 서버의 시간과 <strong>5분 이상(기본 <a href="/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/">임계치</a>)</strong> 어긋나 발생한 타임스탬프 오류다. 인프라 설계 시 모든 노드가 단일 Stratum 2 급 내부 [NTP](/studynote/03_network/10_application_layer_dns_mgmt/536_ntp_network_time_protocol_stratum/) 서버 풀을 바라보도록 강제해야 한다.
- <strong><a href="/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>: 사내망의 커버로스 [KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/) [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)([UDP](/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/)/[TCP](/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 88)를 외부 인터넷망으로 퍼블릭하게 열어버리는 행위. 해커가 외부에서 끊임없이 패스워드 무차별 대입 공격(Brute-Force)이나 패스워드 스프레잉([Password Spraying](/studynote/09_security/05_web_app_security/457_password_spraying/)) 공격을 시도하게 만들어 KDC를 터지게 하거나 계정 잠금을 유발한다. [KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/) 통신은 철저히 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 내부망에서만 이루어지도록 격리([Isolation](/studynote/05_database/04_transactions_concurrency/195_isolation_concurrency_control/))해야 한다.

- **📢 섹션 요약 비유**: 커버로스 세상에서 [KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/) 서버는 지폐를 찍어내는 '한국은행 조폐국'과 같습니다. 조폐국의 금고 열쇠(골든 티켓)를 도둑맞으면 도둑이 맘대로 위조지폐([TGT](/studynote/09_security/12_identity_threat_advanced/586_tgt/))를 찍어 부자가 되므로, 털린 걸 안 즉시 돈의 디자인(비밀번호)을 통째로 바꿔 구형 위조지폐를 종이 쪼가리로 만들어야 합니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 개별 로컬 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 난립 환경 | 커버로스(AD) 기반 [SSO](/studynote/09_security/11_iam_access_control/531_sso/) 환경 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (비용 및 시간)** | 하루 10번 사내 시스템별 중복 로그인 시도 | [TGT](/studynote/09_security/12_identity_threat_advanced/586_tgt/) 한 장으로 모든 사내망 프리패스 ([SSO](/studynote/09_security/11_iam_access_control/531_sso/)) | 임직원 연간 로그인 낭비 시간 **수만 시간 절약** |
| **정량 (보안 사고율)** | 암호화되지 않은 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 혼용으로 [패킷 스니핑](/studynote/09_security/03_network_security/272_packet_sniffing/) 탈취 빈발 | 암호학적 티켓 전송으로 [중간자 공격](/studynote/03_network/14_network_security_threats/706_mitm_man_in_the_middle_hsts/)(MitM) 불가 | 패킷 탈취에 의한 계정 도용 사고율 **0% 도달** |
| <strong>정성 (인프라 <a href="/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/">신뢰성</a>)</strong> | 내가 접속한 서버가 진짜 사내 서버인지 확신할 수 없음 | 클라이언트-서버 간 상호 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)(Mutual Auth) 보장 | [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) [스푸핑](/studynote/02_operating_system/10_security/598_spoofing/) 등으로 가짜 서버에 접속해도 티켓 교환 실패로 차단 |

### 미래 전망 및 진화 방향
- <strong><a href="/studynote/09_security/12_identity_threat_advanced/608_pkinit/">PKINIT</a> 기반 비밀번호 없는 시대(Passwordless)로의 전환</strong>: 전통적인 커버로스는 사용자가 아침에 아이디와 패스워드를 치는 것부터 시작(AS_REQ)했다. 하지만 최근에는 스마트카드, YubiKey, 지문 등 비대칭키([PKI](/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/)) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 방식을 커버로스의 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)에 융합한 <strong><a href="/studynote/09_security/12_identity_threat_advanced/608_pkinit/">PKINIT</a> (Public <a href="/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a> <a href="/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/">Cryptography</a> for Initial <a href="/studynote/02_operating_system/10_security/604_authentication_factors/">Authentication</a>)</strong> 기술이 대세가 되었다. 이를 통해 비밀번호 유출이라는 태생적 한계를 완전히 극복하는 방향으로 진화하고 있다.
- <strong>클라우드 <a href="/studynote/09_security/12_identity_threat_advanced/583_kdc/">KDC</a> (Azure AD Kerberos)</strong>: 물리적 전산실에 있던 [KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/) 서버가 클라우드 상의 [PaaS](/studynote/06_ict_convergence/03_cloud_infrastructure/184_paas_platform_as_a_service/) [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 올라가며, Azure 윈도우 가상 머신들이 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 컨트롤러 없이도 클라우드 KDC와 티켓을 교환하며 동작하는 거대한 인프라 혁신이 [진행](/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 중이다.

### 참고 표준
- **RFC 4120**: The Kerberos Network [Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/) [Service](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) (V5) - 커버로스 5버전의 핵심 기술 규격 표준
- **RFC 4556**: Public [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) [Cryptography](/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/) for Initial [Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/) in Kerberos ([PKINIT](/studynote/09_security/12_identity_threat_advanced/608_pkinit/)) - 비대칭키 결합 표준

네트워크 상의 모든 존재는 거짓말을 할 수 있다. 커버로스는 "아무도 믿지 마라. 오직 우리가 합의한 절대 반지([KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/))가 찍어준 봉인된 티켓만이 진실이다"라는 철학을 완벽한 암호학적 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)로 치환해낸 인류 최고의 네트워크 발명품이다. 패스워드는 사라져가도, 중앙 [중재자](/studynote/04_software_engineering/05_devops_ci_cd/273_mediator_pattern/)를 통한 티켓 기반의 신뢰 교환 아키텍처는 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 시대에도 영원히 그 뼈대를 유지할 것이다.

- **📢 섹션 요약 비유**: 인터넷이라는 어두운 뒷골목에서 서로가 진짜인지 끊임없이 의심하던 시절을 끝내고, 믿음직한 공증인([KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/))이 봉인해 준 위조 불가 증명서(티켓) 하나로 모든 거래를 안심하고 끝내는 가장 과학적이고 위대한 신뢰의 마법입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| AAA 보안 모델 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) ([Domain Name System](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)) | 이름과 주소를 연결해 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 접근성을 만든다. |
| 모니터링 (Monitoring) | 장애 징후를 조기에 발견하기 위한 기초다. |
| OAuth 2.0 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: AAA 보안 모델]
    |
    v
[현재 개념: 커버로스]
    |
    +---> [확장 A: OAuth 2.0]
    +---> [확장 B: 자율 운영 네트워크]
```

커버로스는 AAA 보안 모델에서 출발해 현재 메커니즘을 정교화하고, 이후 OAuth 2.0와 자율 운영 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터 세상에는 나쁜 해커가 너무 많아서 친구한테 "내 비밀번호 1234야"라고 전해주는 순간 중간에서 무조건 훔쳐봐요.
2. 커버로스는 비밀번호를 보내는 대신, 동네에서 가장 믿음직한 이장님([KDC](/studynote/09_security/12_identity_threat_advanced/583_kdc/))에게 한 번만 비밀번호를 말해서 '특별한 암호 팔찌(티켓)'를 차는 시스템이에요.
3. 그 팔찌를 차면 동네 피시방, 오락실, 빵집 등 어디를 가든 비밀번호를 말할 필요 없이 팔찌만 보여주면 척척 통과시켜주고([SSO](/studynote/09_security/11_iam_access_control/531_sso/)), 해커가 가짜 팔찌를 만들어도 시간이 지나면 펑! 사라져서 매우 안전하답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 666 / 1120

<- **이전**: [544. AAA 보안 모델 (Authentication 인증, Authorization 인가, Accounting 과금/로깅)](/studynote/03_network/10_application_layer_dns_mgmt/544_aaa_security_model_auth_authz_acct/)
**다음**: [546. OAuth 2.0](/studynote/03_network/10_application_layer_dns_mgmt/546_oauth_2_0_access_token/) ->

---
