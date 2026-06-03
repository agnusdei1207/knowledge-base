---
title: 584. 1X (PNAC, Port Based Network Access Control) 인증 및 EAP/RADIUS 체계
date: '2026-05-08'
tags:
- studynote-network
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 1X [[303_authentication_authorization_patterns|인증]] 및 [[229_eap_extensible_authentication_protocol|EAP]]/[[541_radius_remote_authentication_aaa|RADIUS]] 체계는 무선·이동통신에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: 1X [[303_authentication_authorization_patterns|인증]] 및 [[229_eap_extensible_authentication_protocol|EAP]]/[[541_radius_remote_authentication_aaa|RADIUS]] 체계를 이해하면 스펙트럼 효율과 이동성 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: IEEE 802.1X는 네트워크 [[446_port_and_bus|포트]](물리적 랜선 [[446_port_and_bus|포트]] 또는 무선 AP의 논리적 연결)에 대한 [[303_authentication_authorization_patterns|인증]] 메커니즘을 정의한 표준으로, **PNAC (Port-Based [[226_nac_network_access_control_ieee_802_1x|Network Access Control]])**이라 부른다. 세 가지 주요 역할(Supplicant(폰), Authenticator(공유기), [[584_as|Authentication Server]]([[541_radius_remote_authentication_aaa|RADIUS]] 서버))로 나뉘어 대화하는 아키텍처다.
- **필요성**: [[582_wpa2_aes_ccmp_personal_enterprise|WPA2]]-Personal ([[142_psk_pre_shared_key|PSK]]) 모드는 가정집에선 좋지만, 직원 1,000명의 대기업에서는 재앙이다. 공용 와이파이 비밀번호를 한 명이 외부에 유출하거나 퇴사하면, 도둑이 회사 밖 주차장 봉고차에서 사내망에 마음껏 접속해 버린다. 이를 막으려면 비번을 바꿔야 하는데 1,000대의 노트북 [[009_config|설정]]을 다시 쳐주는 것은 물리적으로 불가능하다. 즉, **"비밀번호 하나를 공유하지 말고, 직원 1,000명 각각의 아이디와 사원증을 중앙(DB)에서 통제하는 깐깐한 스피드 게이트"**가 무선망에 절실했다.
- **등장 배경**: ① 무선랜의 기업 도입 확대로 [[142_psk_pre_shared_key|PSK]] 기반의 막장 [[283_security_tactics|보안성]](유출 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]) 대두 → ② 유선 [[238_switch_operation_principles|스위치]]에서 훌륭히 작동하던 802.1X 표준을 WPA-Enterprise 규격으로 무선에 이식([[229_eap_extensible_authentication_protocol|EAP]] over LAN, EAPoL) → ③ [[541_radius_remote_authentication_aaa|RADIUS]] 서버와 다양한 [[229_eap_extensible_authentication_protocol|EAP]] [[303_authentication_authorization_patterns|인증]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]([[229_peap_protected_eap_tls_tunnel_authentication|PEAP]], [[694_thread_local_storage_tls|TLS]] 등)의 결합을 통한 엔터프라이즈 인프라 혁신.

```text
┌─────────────────────────────────────────────────────────────┐
│             PSK(동네 카페 방식) vs 802.1X(대기업 방식) 권한 구조 시각화 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [과거: WPA2-Personal (PSK) - "공용 마스터 키의 비극"]              │
│   인사팀 직원 ─▶ (비번: Company123!) ──▶ [공유기(AP)가 혼자 판단] │
│   퇴사한 해커 ─▶ (비번: Company123!) ──▶ [공유기: "오 비번 맞네 패스!"]│
│   => 결과: 문지기(AP)가 권한이 너무 쎄서 멍청함. 비번 한 번 새면 회사가 털림!│
│                                                             │
│   [혁신: WPA2-Enterprise (802.1X) - "중앙 집중형 제로 트러스트"]       │
│                                                             │
│   인사팀 직원 ─▶ (ID/PW 던짐) ──▶ [AP: "난 몰라, 본사에 물어볼게!"]  │
│                                    │  (Radius 통신)          │
│   퇴사한 해커 ─▶ (퇴사ID 던짐) ─▶ [본사 RADIUS 서버 (인사 DB 연결)]  │
│                                    │                        │
│   RADIUS 판단: "인사팀 직원은 통과! 퇴사자는 ID 정지 상태니까 컷(차단)!!" │
│   RADIUS 지시: "AP야! 인사팀 직원만 문 열어주고 개인 전용 암호키 던져줘!" │
│                                                             │
│   => 결과: 공유기(AP)는 그저 무전기 역할(Authenticator)만 할 뿐, 똑똑한 │
│            판단과 암호키 생성은 본사 깊숙한 RADIUS가 도맡아 통제력 극대화! │
└─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 802.1X 아키텍처의 미학은 철저한 **'역할 분리(Decoupling)'**에 있다. [[142_psk_pre_shared_key|PSK]] 시절엔 공유기([[572_ap_access_point_ds_distribution_system|AP]]) 한 대가 무선 전파도 쏘고, 비밀번호도 저장하고, 판단도 내리는 독재자였다. 802.1X는 공유기를 단순한 깡통 문지기(Authenticator)로 강등시켰다. 폰(Supplicant)이 ID를 던지면, 깡통 공유기는 열어보지도 않고 봉투 그대로 본사 서버실의 진짜 왕([[584_as|Authentication Server]], [[541_radius_remote_authentication_aaa|RADIUS]])에게 패스한다. RADIUS는 사내 인사시스템(AD/[[543_ldap_lightweight_directory_access_protocol|LDAP]])과 대조해 정상 직원이면 승인 도장과 함께 "이 직원만을 위한 랜덤 마스터 키(PMK)"를 발급해 폰과 공유기에 뿌려준다. 이것이 퇴사자가 발생했을 때 인사팀 클릭 한 번으로 모든 사내 접근 권한을 0초 만에 소멸시키는 마법의 구조다.

- **📢 섹션 요약 비유**: 개인용 와이파이([[142_psk_pre_shared_key|PSK]])는 아파트 1층 공동 현관문의 비밀번호를 주민 500명이 다 같이 쓰는 겁니다. 비번이 소문나면 끝장이죠. 802.1X(엔터프라이즈)는 호텔 스피드 게이트입니다. 문고리에는 비번을 치는 구멍이 아예 없고, 무조건 각자의 사원증(ID)을 대야만 문이 열립니다. 누가 나쁜 짓을 하면 그 사람의 사원증만 정지시키면 호텔 전체가 다시 안전해집니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

802.1X가 작동하려면 이 세 가지 플레이어가 완벽한 삼각편대를 이뤄 통신해야 한다.

| [[603_component_independent_deployment_unit|컴포넌트]] 이름 | 실체 (누구인가?) | 수행 역할 및 행동 (Role) |
|:---|:---|:---|
| **1. Supplicant (요청자)** | 직원의 폰, 노트북 안의 네트워크 소프트웨어 (Windows 내장 등) | 사원증을 내미는 손님. 깡통 AP에게 **EAPoL ([[229_eap_extensible_authentication_protocol|EAP]] over LAN)**이라는 무선 [[295_protocol_field_tcp_udp_icmp|프로토콜]]로 자신의 아이디와 패스워드, [[303_authentication_authorization_patterns|인증]]서를 포장해서 던짐. |
| **2. Authenticator ([[303_authentication_authorization_patterns|인증]]자)**| 회사 천장에 달린 무선 공유기([[572_ap_access_point_ds_distribution_system|AP]]) 또는 무선 컨트롤러(WLC) | 똑똑한 척하지만 판단 능력이 0인 바보 문지기. 폰이 던진 암호 봉투를 까보지 않고 그대로 뒷구멍의 유선망([[541_radius_remote_authentication_aaa|RADIUS]] [[295_protocol_field_tcp_udp_icmp|프로토콜]])으로 본사 서버에 토스(Relay)함. |
| **3. [[584_as|Authentication Server]] ([[581_authentication_server|인증 서버]])**| 사내 서버실의 **[[541_radius_remote_authentication_aaa|RADIUS]] 서버** ([[539_netflow_sflow_traffic_monitoring|Cisco]] ISE, Microsoft NPS 등) | 무소불위의 최종 권력자. 사내 인사 DB([[548_active_directory|Active Directory]])와 연동하여 폰이 보낸 ID/[[303_authentication_authorization_patterns|인증]]서를 깐깐히 검사하고 합격(Accept)/불합격(Reject) 도장을 찍음. |

### [[229_eap_extensible_authentication_protocol|EAP]] ([[229_eap_extensible_authentication_protocol|Extensible Authentication Protocol]])의 융합과 3대 대장 [[295_protocol_field_tcp_udp_icmp|프로토콜]]

802.1X는 껍데기(프레임워크)일 뿐이다. 그 안에서 "아이디/비번을 쓸 거냐? [[303_authentication_authorization_patterns|인증]]서를 쓸 거냐? 심 카드를 쓸 거냐?"를 결정하는 실제 내용물 규격이 바로 **[[229_eap_extensible_authentication_protocol|EAP]]**다. 기업 아키텍트들은 회사 보안 수준에 맞춰 이 [[229_eap_extensible_authentication_protocol|EAP]] 종류를 세팅해야 한다.

```text
┌───────────────────────────────────────────────────────────────┐
│               엔터프라이즈 802.1X의 3대 EAP 프로토콜 진검승부          │
├───────────────────────────────────────────────────────────────┤
│   [위험한 해킹: 허공에서 평문 ID/비번 훔쳐보기 스니핑!]                 │
│                                                               │
│   🛡️ 1. EAP-TLS (군사/금융권 끝판왕 방어)                           │
│   - 조건: 사내 직원 노트북 '안에' 회사가 발급한 찐 인증서가 깔려있어야 함. │
│   - 작동: 공유기가 묻지도 따지지도 않고 노트북 안의 칩셋(인증서)과 통신해  │
│          알아서 열림. 아이디/비번을 칠 필요가 없음. 완벽한 철벽 방어!      │
│   - 딜레마: 직원 1천 명 노트북에 인증서 파일 다 깔아주려면 IT 부서 죽어남.  │
│                                                               │
│   🛡️ 2. PEAP (가장 대중적인 일반 대기업 방식)                       │
│   - 조건: 회사(RADIUS) 쪽에만 인증서가 딱 1장 있으면 됨!              │
│   - 작동: 폰과 서버가 통신할 때 뒷구멍으로 몰래 암호화 터널(TLS 터널)을     │
│          먼저 뻥 뚫어놓고, 그 깜깜한 터널 안으로 폰이 ID/비번을 안전하게    │
│          던짐. 해커가 밖에서 백날 쳐다봐도 훔쳐볼 수 없음! (갓성비 최고)   │
│                                                               │
│   🛡️ 3. EAP-TTLS (PEAP의 사촌 동생)                              │
│   - 작동: PEAP이랑 거의 똑같이 터널 뚫고 던지는데, 옛날 통신 장비들(구형)도│
│          알아들을 수 있게 융통성 있게 규격을 맞춘 버전임.                │
└───────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** EAP의 진화는 "해커(Evil Twin)의 낚시 공격을 어떻게 막을 것인가"에 초점이 맞춰져 있다. 해커가 가짜 공유기를 켜놓고 "나 회사 공유기야! ID/비번 줘!"라고 폰을 속일 때, 무식한 [[228_eap_md5_vulnerable_authentication|EAP-MD5]] 같은 규격은 속아서 비번을 허공에 날려버린다(탈탈 털림). 
이를 막기 위해 **[[229_peap_protected_eap_tls_tunnel_authentication|PEAP]] ([[229_peap_protected_eap_tls_tunnel_authentication|Protected EAP]])**가 탄생했다. PEAP은 직원이 비번을 치기 전에, 폰이 먼저 회사 서버의 '디지털 서명([[303_authentication_authorization_patterns|인증]]서)'을 검사해 "진짜 우리 본사 서버 맞네!"를 [[396_validation|확인]]한 후 안전한 비밀 터널([[694_thread_local_storage_tls|TLS]])을 뚫어 그 안으로 비번을 쏜다. 가장 극단적인 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]는 **[[230_eap_tls_mutual_authentication_pki|EAP-TLS]]**다. 아예 비번 창 자체를 없애고, 기기 안에 심어진 하드웨어 [[303_authentication_authorization_patterns|인증]]서끼리 수학적으로 부딪쳐 문을 여는 방식으로, 사내망 무단 접속을 물리적으로 박살 내는 현존 최강의 융합 방패다.


802.1X의 심장인 [[584_as|Authentication Server]] 역할을 수행하는 **[[541_radius_remote_authentication_aaa|RADIUS]]** [[295_protocol_field_tcp_udp_icmp|프로토콜]]의 설계 철학을 해부한다. 이름에 Dial-In(전화 접속)이 들어간 이유는 1990년대 PC통신 전화선 시절에 만들어진 규격이기 때문이다.

| 비교 기준 | 깡통 공유기 ([[572_ap_access_point_ds_distribution_system|AP]] / Authenticator) | 위대한 [[541_radius_remote_authentication_aaa|RADIUS]] 서버 |
|:---|:---|:---|
| **네트워크 위치** | 천장에 대충 매달려 있거나 복도 끝에 있음. 도둑이 뜯어가기 쉬움. | 본관 지하 3층 항온항습실 서버 랙 깊숙이 철창 안에 처박혀 있음. |
| **정보의 저장 상태** | 직원들의 패스워드나 [[303_authentication_authorization_patterns|인증]] 정보가 **단 1바이트도 저장되어 있지 않음.** (State-less 깡통). | 10만 명 직원의 암호 화시값과 인사 DB([[548_active_directory|Active Directory]])가 **통째로 물려있음.** |
| **통신 [[295_protocol_field_tcp_udp_icmp|프로토콜]] 융합**| 무선 허공에서는 폰과 **EAPoL ([[229_eap_extensible_authentication_protocol|EAP]] over LAN)** 규격으로 대화함. | 유선 랜선을 타고 뒷구멍으로 AP와 **[[541_radius_remote_authentication_aaa|RADIUS]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]([[406_udp_user_datagram_protocol_connectionless_fast|UDP]] 1812)**로 암호화 대화함. |

RADIUS의 핵심 가치는 **"최전방([[572_ap_access_point_ds_distribution_system|AP]])이 털려도 본진(비밀번호)은 절대 안 털리는 중앙 집중 아키텍처"**다. 도둑이 천장의 AP를 뜯어서 집에 가져가 기판을 분해해 봐도 그 안에는 아무 데이터가 없다. AP는 그저 폰이 보낸 [[229_eap_extensible_authentication_protocol|EAP]] 봉투를 [[238_switch_operation_principles|스위치]] 유선망을 타고 [[541_radius_remote_authentication_aaa|RADIUS]] 서버로 택배 배달해 주는 멍청한 중계기일 뿐이다. 

```text
┌───────────────────────────────────────────────────────────────┐
│               802.1X 기반 동적 VLAN 할당의 인프라 마법 시각화        │
├───────────────────────────────────────────────────────────────┤
│   [상황: 임원과 인턴이 똑같이 로비의 1번 공유기(AP)에 접속함]            │
│                                                               │
│   [본사 RADIUS 서버의 무소불위 통제]                                │
│                                                               │
│   1. 임원 로그인 성공 ─▶ RADIUS ─▶ AP에 지시:                      │
│      "AP야! 방금 인증 성공한 폰은 사장님(VLAN 10) 폰이다.               │
│       얘는 접속하자마자 방화벽 다 열려있는 사장님 전용 무선망에 꽂아!"       │
│                                                               │
│   2. 알바생 로그인 성공 ─▶ RADIUS ─▶ AP에 지시:                      │
│      "AP야! 방금 인증 성공한 폰은 일용직 알바(VLAN 99) 폰이다.           │
│       얘는 사내 서버 접속 완전 차단하고 오직 인터넷만 되게 망을 분리해!"     │
│                                                               │
│   => 결과: 와이파이 이름(SSID)을 부서별로 수십 개씩 파놓을 필요가 없음!      │
│            하나의 와이파이 이름으로 1,000명이 붙어도, RADIUS가 신분에 따라 │
│            유선 방화벽망(VLAN)을 알아서 쫙쫙 찢어 꽂아버리는 궁극의 자동화!  │
└───────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 엔터프라이즈 환경에서 802.1X의 끝판왕 응용 기술인 **동적 [[224_vlan_virtual_lan_broadcast_domain|VLAN]] 할당(Dynamic [[224_vlan_virtual_lan_broadcast_domain|VLAN]] Assignment)**이다. 옛날에는 임원용 와이파이(`Boss_WiFi`)와 일반용 와이파이(`Staff_WiFi`) 이름을 따로 파고 비밀번호를 따로 관리해야 했다. 802.1X/[[541_radius_remote_authentication_aaa|RADIUS]] 환경에서는 그럴 필요가 없다. 온 회사의 와이파이 이름은 오직 1개(`Company_Corp`)다. 직원이 로그인하는 순간, [[541_radius_remote_authentication_aaa|RADIUS]] 서버가 인사 DB를 조회해 "부서/직급 태그([[224_vlan_virtual_lan_broadcast_domain|VLAN]] ID)"를 발급하여 공유기에 던진다. 공유기는 그 직원의 패킷을 해당 태그가 달린 유선망 파이프로 직행시킨다. 사장님이 화장실에서 접속하든 회의실에서 접속하든, 로그인하는 순간 즉시 사장님 전용([[224_vlan_virtual_lan_broadcast_domain|VLAN]] [[489_raid_10_hybrid|10]]) 망으로 마법처럼 [[339_routing_overview_best_path_selection|라우팅]] 되는 진정한 무선 모빌리티 융합(Mobility Fusion)이 완성된다.

- **📢 섹션 요약 비유**: 옛날엔 사장님 전용 엘리베이터와 일반 엘리베이터를 아예 따로 만들었습니다(와이파이 분리). 802.1X 동적 VLAN은 아주 똑똑한 [[190_ai_llm_requirements_specification|AI]] 엘리베이터입니다. 사장님이 타서 사원증을 대면 자동으로 VIP 라운지 층이 눌러지고, 알바생이 사원증을 대면 일반 사무실 층만 눌러져서 절대 남의 층으로 갈 수 없게 막아버리는 완벽한 출입 통제기입니다.

---

## Ⅲ. 비교 및 연결

1X [[303_authentication_authorization_patterns|인증]] 및 [[229_eap_extensible_authentication_protocol|EAP]]/[[541_radius_remote_authentication_aaa|RADIUS]] 체계를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. WPA3가 기반 조건을 만든다면, 1X [[303_authentication_authorization_patterns|인증]] 및 [[229_eap_extensible_authentication_protocol|EAP]]/[[541_radius_remote_authentication_aaa|RADIUS]] 체계는 그 위에서 핵심 메커니즘을 구현하고, [[585_captive_portal_guest_web_auth|캡티브 포털]]은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 스펙트럼 효율과 이동성에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | WPA3의 기반 정리 | 1X [[303_authentication_authorization_patterns|인증]] 및 [[229_eap_extensible_authentication_protocol|EAP]]/[[541_radius_remote_authentication_aaa|RADIUS]] 체계의 핵심 동작 | [[585_captive_portal_guest_web_auth|캡티브 포털]]의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 스펙트럼 효율 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [[396_validation|확인]] | 현재 메커니즘의 적합성 판단 | 운영·확장 [[268_strategy_pattern|전략]] 연결 |

- **📢 섹션 요약 비유**: 1X [[303_authentication_authorization_patterns|인증]] 및 [[229_eap_extensible_authentication_protocol|EAP]]/[[541_radius_remote_authentication_aaa|RADIUS]] 체계는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. **상황**: 회사 앞 카페에 앉아있던 직원의 스마트폰에 평소 회사에서 쓰던 `Company_Secure`라는 와이파이가 떴다. 직원이 클릭하고 ID/PW([[229_peap_protected_eap_tls_tunnel_authentication|PEAP]])를 입력했는데 연결이 안 되었다. 며칠 뒤 그 직원의 아이디로 사내 기밀 서버가 해킹당했다.
2. **원인 (Rogue [[572_ap_access_point_ds_distribution_system|AP]] 및 [[303_authentication_authorization_patterns|인증]]서 무시 [[128_water_scrum_fall_anti_pattern|안티패턴]])**: 해커가 카페에서 라즈베리 파이(해킹툴)로 회사 와이파이와 100% 똑같은 이름(SSID)의 가짜 공유기와 가짜 [[541_radius_remote_authentication_aaa|RADIUS]] 서버를 구동시킨 것이다 (**Evil Twin Attack**). 직원이 무심코 아이디/비번을 치고 들어갔을 때, 폰 화면에 "서버 [[303_authentication_authorization_patterns|인증]]서를 신뢰할 수 없습니다"라는 경고창이 떴다. 하지만 귀찮은 직원이 **[계속/신뢰함]** 버튼을 꾹 눌러버리는 치명적 실수를 저질렀고, 해커가 쳐놓은 가짜 암호화 터널 안으로 회사 비밀번호를 그대로 헌납해 버렸다.
3. **의사결정 및 아키텍처 조치 ([[539_mdm_master_data_management|MDM]] 기반 Root [[089_contract_account_smart_contract|CA]] 핀 고정)**:
   - 통신 및 보안 아키텍트는 "사용자의 판단에 보안을 맡기는 것은 죄악"이라고 선언한다.
   - 회사에서 지급하는 모든 스마트폰과 노트북에 [[539_mdm_master_data_management|MDM]](모바일 기기 관리) 정책을 밀어 넣어, 사내 와이파이 연결 프로파일을 수정하지 못하게 잠가버린다.
   - 이 프로파일 [[009_config|설정]] 안에 **"우리 회사 [[541_radius_remote_authentication_aaa|RADIUS]] 서버의 공인 루트 [[303_authentication_authorization_patterns|인증]]서(Root [[089_contract_account_smart_contract|CA]])가 아니면, 아예 경고창도 띄우지 말고 접속을 0.001초 만에 튕겨버려라!" (Server Certificate [[396_validation|Validation]] Force)**라는 옵션을 하드코딩한다.
   - **결과**: 해커가 회사 밖에서 100억짜리 가짜 공유기를 켜도, 임직원 스마트폰은 서버 [[303_authentication_authorization_patterns|인증]]서 서명이 다름을 감지하고 아예 아이디/비번 전송 단계(Phase 2)로 진입하지 않고 연결을 끊어버려 완벽한 [[752_phishing|피싱]] 방어가 달성된다.

### 도입 [[435_checklist_based_testing|체크리스트]] 및 [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **엔터프라이즈 802.1X 도입의 매몰 비용 (인프라 병목)**: 동네 병원이나 직원 30명짜리 중소기업이 "보안 좀 올려볼까?" 하고 무턱대고 802.1X를 도입하면 파산한다. 802.1X를 돌리려면 Windows Server [[483_active_vs_passive_ftp|Active]] Directory를 구축해야 하고, [[541_radius_remote_authentication_aaa|RADIUS]] 서버(NPS/ISE) 라이선스를 사야 하며, 공인 [[303_authentication_authorization_patterns|인증]]서 체계([[159_pki_public_key_infrastructure|PKI]])까지 관리해야 하는 엄청난 서버 관리(Admin) 인건비가 터져 나온다. 소규모 사업장에서는 802.1X 대신 공유기 자체에서 [[673_mac_message_authentication_code|MAC]] 주소와 다중 PSK를 버무려 관리하는 **[[583_wpa3_sae_owe_enhanced_open|WPA3]]-SAE (Personal) 기반의 MPSK(Multi-[[142_psk_pre_shared_key|PSK]])** 같은 경량 솔루션으로 타협하는 것이 현명한 아키텍처 의사결정이다.
- **[[128_water_scrum_fall_anti_pattern|안티패턴]] ([[228_eap_md5_vulnerable_authentication|EAP-MD5]] 같은 구형 규격 맹신)**: 사내 무선망을 세팅하며 [[229_eap_extensible_authentication_protocol|EAP]] 종류를 고를 때, 속도가 빠르다는 이유로 20년 전 기술인 [[229_eap_extensible_authentication_protocol|EAP]]-MD5를 고르는 것은 회사 문을 활짝 열어두는 미친 짓이다. MDM은 안전한 [[694_thread_local_storage_tls|TLS]] 터널을 뚫지 않고 해시만 돌려서 보내기 때문에 패킷을 가로채서 딕셔너리 공격을 돌리면 반나절 만에 비번이 털린다. 무조건 터널을 뚫는 **[[229_peap_protected_eap_tls_tunnel_authentication|PEAP]]-MSCHAPv2, [[229_eap_extensible_authentication_protocol|EAP]]-TTLS, 또는 무적의 [[230_eap_tls_mutual_authentication_pki|EAP-TLS]]** 중 하나만 골라야 무선망이 생존한다.

- **📢 섹션 요약 비유**: 해커가 가짜 경찰 복장(Evil Twin 공유기)을 입고 길에서 "신분증(비밀번호) 내놔!"라고 합니다. 착한 직원은 속아서 줍니다. 802.1X의 [[303_authentication_authorization_patterns|인증]]서 강제 [[396_validation|확인]] 기능은, 직원에게 "경찰 배지 홀로그램(서버 [[303_authentication_authorization_patterns|인증]]서)이 없는 가짜 경찰에겐 묵비권을 행사해라!"라고 교육을 빡세게 시켜놔서, 가짜 경찰 앞에서는 아예 입을 꾹 닫아버리게 만드는 최고의 방어 훈련입니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | [[582_wpa2_aes_ccmp_personal_enterprise|WPA2]]-Personal (일반 암호 모드) | [[582_wpa2_aes_ccmp_personal_enterprise|WPA2]]/3-Enterprise (802.1X 융합 모드) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (비밀번호 유출 피해 반경)** | 마스터 비번 털리면 사내 **100% 털림** | 털려도 해당 사원 1명의 권한(1%)만 털림 | 퇴사자/빌런 발생 시 무선망 전면 교체(블랙아웃) 비용 **100% 절감 (피해 반경 최소화)** |
| **정량 (인프라 통합 관리)** | [[572_ap_access_point_ds_distribution_system|AP]] 50대 비밀번호 바꾸려면 50번 로그인 | 중앙 [[541_radius_remote_authentication_aaa|RADIUS]] 서버 DB 하나만 수정하면 끝 | 대규모 캠퍼스 망의 계정 [[212_synchronization_mechanisms|동기화]] 및 관리 공수(Admin Overhead) **수십 배 단축** |
| **정성 (망 분리 [[292_accessibility_kwcag_wcag|접근성]])**| 영업/개발망을 물리적 와이파이(SSID)로 찢어둠 | 동적 VLAN으로 SSID 하나로 몽땅 통합 | 임직원 신분에 따라 자동으로 꽂히는 진정한 **[[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Network Access ([[339_ztna|ZTNA]]) 달성** |

### 미래 전망 및 진화 방향
- **클라우드 RADIUS와 IDaaS의 부상**: 과거엔 802.1X를 하려면 본사 전산실에 거대한 서버 컴퓨터를 둬야 했지만, 지금은 클라우드 시대다. [[551_okta_idaas|Okta]], [[539_netflow_sflow_traffic_monitoring|Cisco]] Meraki, Google Workspace 같은 거대한 **[[551_okta_idaas|IDaaS]] (Identity-as-a-Service)** 클라우드가 통째로 [[541_radius_remote_authentication_aaa|RADIUS]] 역할을 대신해 준다. 스타트업도 복잡한 서버 구축 없이 1만 원만 내면 클라우드 RADIUS를 쏴주어, 구글 아이디 로그인 한 번으로 사내 802.1X 최고급 와이파이에 접속하게 만드는 클라우드 융합 인프라가 대세가 되었다.
- **[[673_mac_message_authentication_code|MAC]] 랜덤화(Randomization) 정책과의 충돌**: 최신 아이폰이나 안드로이드폰은 [[781_personal_information|개인정보]] 보호를 위해 와이파이에 붙을 때마다 자신의 기기 고유번호([[673_mac_message_authentication_code|MAC]] 주소)를 임의로 휙휙 바꿔버린다([[673_mac_message_authentication_code|MAC]] Randomization). 이로 인해 기존 [[673_mac_message_authentication_code|MAC]] 주소 기반으로 직원 기기를 걸러내던 허접한 기업망들은 대혼란에 빠졌다. 802.1X([[230_eap_tls_mutual_authentication_pki|EAP-TLS]] [[303_authentication_authorization_patterns|인증]]서 기반)는 폰의 [[673_mac_message_authentication_code|MAC]] 주소가 100번 바뀌든 말든 기기 안의 암호화 칩셋 서명을 검사하므로 이 거대한 프라이버시 충돌을 가장 우아하게 우회하며 통과해 낸 궁극의 생존자 규격이 되었다.

### 참고 표준
- **IEEE 802.1X**: 원래 유선 [[238_switch_operation_principles|스위치]]용 [[446_port_and_bus|포트]] 접근 제어(PNAC) 표준으로 만들어졌으나 무선(Wi-Fi)의 WPA-Enterprise로 융합되며 역사상 가장 위대한 확장성을 증명한 문서.
- **RFC 3748 ([[229_eap_extensible_authentication_protocol|Extensible Authentication Protocol]], [[229_eap_extensible_authentication_protocol|EAP]])**: 802.1X라는 뼈대 안에서 ID/비번을 쓸지 카드 키를 쓸지 그 내용물 규격을 정의하는 거대한 [[303_authentication_authorization_patterns|인증]] 확장 포맷의 국제 인터넷 규격.

802.1X (PNAC)와 [[229_eap_extensible_authentication_protocol|EAP]]/[[541_radius_remote_authentication_aaa|RADIUS]] 연동 아키텍처는 무선랜 역사상 가장 훌륭한 "권력 분산과 중앙 통제"의 교과서다. 전파를 쏘는 더러운 최전방 일선([[572_ap_access_point_ds_distribution_system|AP]])에는 권력을 1도 주지 않고 바보 문지기로 만들고, [[303_authentication_authorization_patterns|인증]]과 판단의 뇌(Brain)는 안전한 지하 요새의 [[541_radius_remote_authentication_aaa|RADIUS]] 서버로 완벽히 분리해 내었다. 그 결과 기업들은 1,000개의 공유기를 깔고 수만 명의 직원이 돌아다니는 대형 공장이나 캠퍼스에서도, 단 한 명의 [[303_authentication_authorization_patterns|인증]] 도용 없이 완벽한 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]([[667_zero_trust_runtime_integrity_measurement|Zero Trust]]) 무선 모빌리티 융합을 이룩할 수 있게 되었다.

- **📢 섹션 요약 비유**: 802.1X는 깡통 문지기 로봇([[572_ap_access_point_ds_distribution_system|AP]])입니다. 문지기는 아무것도 몰라서, 내가 "나 김 대리야!"라고 사원증([[229_eap_extensible_authentication_protocol|EAP]])을 주면 본사 사장님([[541_radius_remote_authentication_aaa|RADIUS]])에게 무전으로 팩스를 보냅니다. 사장님이 CCTV로 내 얼굴과 사원증을 [[396_validation|확인]]하고 "문 열어줘라([[224_vlan_virtual_lan_broadcast_domain|VLAN]])!"라고 텔레파시 암호키를 쏴주면 그제야 찰칵하고 문을 열어주는, 절대로 뇌물을 먹일 수 없는 완벽한 원격 3단 콤보 검문 시스템입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[583_wpa3_sae_owe_enhanced_open|WPA3]] | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 셀 (Cell) | 무선 [[090_service_kubernetes_network_load_balancing|서비스]] 범위를 나누는 기본 단위다. |
| [[556_handover_handoff_types_concept|핸드오버]] ([[556_handover_handoff_types_concept|Handover]]) | 이동 중에도 연결을 유지하게 만든다. |
| [[585_captive_portal_guest_web_auth|캡티브 포털]] | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: WPA3]
    │
    ▼
[현재 개념: 1X 인증 및 EAP/RADIUS 체계]
    │
    ├──▶ [확장 A: 캡티브 포털]
    └──▶ [확장 B: 지능형 무선 자원 제어]
```

1X [[303_authentication_authorization_patterns|인증]] 및 [[229_eap_extensible_authentication_protocol|EAP]]/[[541_radius_remote_authentication_aaa|RADIUS]] 체계는 WPA3에서 출발해 현재 메커니즘을 정교화하고, 이후 [[585_captive_portal_guest_web_auth|캡티브 포털]]와 지능형 무선 자원 제어 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 집에서 쓰는 와이파이는 비밀번호 `1234`를 온 가족이 돌려써서 나쁜 도둑이 알아내면 집 전체가 다 털려요.
2. 하지만 802.1X라는 대기업 와이파이는 비밀번호 구멍이 없고, 무조건 내 이름과 회사 신분증 카드(ID)를 찍어야만 문지기 로봇(공유기)이 본사 사장님([[541_radius_remote_authentication_aaa|RADIUS]] 서버)한테 물어보고 문을 열어줘요.
3. 그래서 직원이 나쁜 맘을 먹고 도망가도 사장님이 "저 신분증 정지시켜!" 버튼만 누르면, 다른 사람들 와이파이는 멀쩡한데 그 나쁜 사람만 인터넷이 영원히 끊겨버리는 아주 똑똑한 시스템이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 705 / 1120

← **이전**: [[583_wpa3_sae_owe_enhanced_open|583. WPA3]]
**다음**: [[585_captive_portal_guest_web_auth|585. 캡티브 포털 (Captive Portal)]] →

---
