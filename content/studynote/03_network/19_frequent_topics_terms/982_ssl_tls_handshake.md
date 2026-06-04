+++
title = "982. SSL/TLS 핸드셰이크"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SSL/[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크는 빈출 주제와 용어에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: SSL/[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크를 이해하면 구분 명확성과 설명력 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: SSL/[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크는 OSI 7계층 중 전송 계층(L4)과 애플리케이션 계층(L7) 사이에서 동작하며, 두 호스트가 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받기 전에 [암호화 알고리즘](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/504_cryptography_algorithms_aes_rsa_sha/) 세트(Cipher Suite)를 결정하고 X.509 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서로 서버의 신원을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한 후, 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 빠르게 암/복호화할 [마스터 시크릿](/knowledge-base/studynote/09_security/03_network_security/141_master_secret/)([Master Secret](/knowledge-base/studynote/09_security/03_network_security/141_master_secret/))을 만들어내는 일련의 과정이다.
- **필요성**: 인터넷은 누구든 지나가는 패킷을 들여다볼 수 있는 '개방형 도로'와 같다. 사용자가 입력한 비밀번호나 신용카드 번호를 보호하려면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 암호화해야 하는데, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 암호화할 '키'를 인터넷으로 그냥 보내면 해커도 그 키를 볼 수 있다는 딜레마(키 분배 문제)가 발생한다. 이를 안전하게 해결하기 위한 정교한 춤사위(Handshake)가 반드시 필요하다.
- **💡 비유**: 핸드셰이크는 낯선 두 [스파이](/knowledge-base/studynote/04_software_engineering/11_testing_validation/853_spy_test_double/)가 광장에서 만나 서로의 암구호 수첩(Cipher Suite)을 맞추고, 본부에서 발급한 신분증([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서)을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한 뒤, 오늘 하루 동안만 사용할 '비밀 무전 주파수([Session Key](/knowledge-base/studynote/09_security/03_network_security/140_session_key/))'를 귓속말로 정하는 은밀한 만남의 과정이다.
- **등장 배경 및 발전 과정**:
  1. **HTTP의 평문 노출 문제**: 초창기 웹([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/))은 평문 통신이어서 [중간자 공격](/knowledge-base/studynote/03_network/14_network_security_threats/706_mitm_man_in_the_middle_hsts/)(MITM, Man-In-The-Middle)에 속수무책이었다.
  2. **넷스케이프의 SSL 발명 (1994)**: 넷스케이프 커뮤니케이션즈가 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) 비대칭키 암호화를 활용하여 SSL 2.0/3.0을 개발, 신원 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)과 키 교환을 분리하는 현대적 개념을 확립했다.
  3. <strong>IETF의 <a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/">TLS</a> 표준화 및 진화</strong>: SSL이 [IETF](/knowledge-base/studynote/03_network/12_iot_wpan_edge/635_ietf_core_working_group_coap/) 표준인 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.0으로 발전했고, 모바일 환경의 속도 요구와 양자 컴퓨터의 위협에 대응하기 위해 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3(2018년)으로 진화하며 불필요한 절차를 과감히 잘라내었다.

평문 통신의 [중간자 공격](/knowledge-base/studynote/03_network/14_network_security_threats/706_mitm_man_in_the_middle_hsts/) 위협과 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크를 통한 방어 메커니즘을 구조도로 시각화하면, 신원 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 왜 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)만큼 중요한지 알 수 있다.

```text
  +-------------------------------------------------------------+
  |              중간자 공격(MITM)과 TLS의 방어 원리               |
  +-------------------------------------------------------------+
  |                                                             |
  |  [HTTP 평문 통신 (공격 노출)]                                   |
  |   클라이언트 ----- (계좌 비밀번호) ------> [해커] ------> 은행 서버    |
  |   * 해커가 중간에서 라우터를 장악하여 데이터를 그대로 읽고 가로챔            |
  |                                                             |
  |  [단순 암호화만 한 경우 (신원 검증 실패)]                          |
  |   클라이언트 <---(해커의 가짜 공개키)-- [해커] <---(은행의 공개키)-- 은행 |
  |   클라이언트 --(해커 키로 암호화)---> [해커] --(은행 키로 암호화)--> 은행 |
  |   * 데이터는 암호화되었지만, 클라이언트는 해커를 은행으로 착각함           |
  |                                                             |
  |  [TLS 핸드셰이크 적용 (인증서 기반 방어)]                          |
  |   클라이언트 <--- (은행의 공인 인증서) -- [해커 통과] <--- 은행 서버    |
  |        |                                                    |
  |    (내장된 Root CA 공개키로 인증서 서명 검증)                       |
  |    ✅ "이 인증서는 진짜 은행 것이 맞다!"                            |
  |        |                                                    |
  |   클라이언트 -- (은행의 공개키로 세션키 암호화) ---> 해커 (해독 불가) |
  |   * 해커는 은행의 '개인키'가 없으므로 세션키를 알아낼 수 없어 공격 실패      |
  +-------------------------------------------------------------+
```

**[다이어그램 해설]** 단순히 암호화를 한다고 해서 보안이 완성되는 것은 아니다. 해커가 중간에서 자신의 공개키를 은행의 공개키인 양 클라이언트에게 건네주면(MITM), 클라이언트는 해커의 키로 암호화하여 통신하게 된다. [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크는 이 문제를 '공인 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 기관([CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/), Certificate Authority)'이 서명한 X.509 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서로 해결한다. 은행 서버는 핸드셰이크 도중 CA의 디지털 서명이 찍힌 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 보낸다. 클라이언트(웹 브라우저)는 내장된 Root CA의 공개키로 이 서명이 위조되지 않았음을 수학적으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다. 해커는 CA의 개인키를 해킹하지 않는 이상 은행의 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 위조할 수 없으므로, 클라이언트는 안전하게 은행 서버의 진짜 공개키를 추출하여 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)키를 암호화해 전달할 수 있다.

- **📢 섹션 요약 비유**: 소개팅 장소에 나온 사람이 진짜 내가 연락하던 사람이 맞는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하기 위해, 국가([CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/))가 발행한 홀로그램 신분증([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서)을 먼저 꼼꼼히 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야만 전화번호([세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)키)를 건네주는 것과 같습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소

| 요소명 | 역할 | 내부 동작 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **Cipher Suite** | [암호화 알고리즘](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/504_cryptography_algorithms_aes_rsa_sha/) 세트 협상 | 키 교환, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/), 대칭키, 해시 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 조합을 제안하고 선택 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | 사용할 언어와 무기 선택 |
| **X.509 Certificate** | 서버 신원 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) ([Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/)) | 서버의 공개키와 CA의 디지털 서명을 포함한 전자 신분증 | [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/), [ECDSA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/097_ecdsa_schnorr_signature_bitcoin/), [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) (Certificate Authority) | 국가 공인 영업 허가증 |
| <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a> Exchange (키 교환)</strong> | 대칭키([Session Key](/knowledge-base/studynote/09_security/03_network_security/140_session_key/)) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 보조 | [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/)(키 직접 암호화) 또는 [DH](/knowledge-base/studynote/09_security/03_network_security/128_dh_diffie_hellman/)/[ECDHE](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/)(키 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 재료 교환)로 키를 안전하게 공유 | [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/), [DHE](/knowledge-base/studynote/09_security/03_network_security/129_dhe_ephemeral_dh/), [ECDHE](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/) | 비밀 금고의 다이얼 번호 합의 |
| <strong><a href="/knowledge-base/studynote/09_security/03_network_security/140_session_key/">Session Key</a> (대칭키)</strong> | 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(Payload) 고속 암호화 | 핸드셰이크 완료 후 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)되며 클라이언트와 서버만 아는 일회용 비밀키 | AES-GCM, ChaCha20 | 오늘 하루만 쓸 마스터 키 |
| <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> (Message Auth <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/">Code</a>)</strong> | 핸드셰이크 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 핸드셰이크 전체 메시지가 중간에 조작되지 않았는지 마지막에 상호 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | [HMAC](/knowledge-base/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/), SHA-256 | 회의록 최종 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 서명 |

### [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.2 기반 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) 핸드셰이크 구조와 흐름

전통적이고 이해하기 쉬운 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.2의 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) 기반 핸드셰이크 과정을 살펴보면, 클라이언트와 서버가 2번의 왕복(2-[RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/))을 통해 보안 채널을 구축하는 물리적 타임라인을 파악할 수 있다.

```text
  +------------------------------------------------------------------+
  |                 TLS 1.2 RSA 핸드셰이크 파이프라인 (2-RTT)               |
  +------------------------------------------------------------------+
  |                                                                  |
  |   [Client]                                            [Server]   |
  |      |                                                   |       |
  |      | 1. Client Hello                                   |       |
  |      | (지원하는 Cipher Suite, Client Random)-----------> |       |
  |      |                                                   |       |
  |      |                                   2. Server Hello |       |
  |      | <----------(선택한 Cipher Suite, Server Random) -- |       |
  |      |                                                   |       |
  |      |                                    3. Certificate |       |
  |      | <------------------------- (서버의 X.509 공인 인증서) -- |       |
  |      |                                                   |       |
  |      |                                4. Server Hello Done |       |
  |      | <------------------------------------------------- -- |       |
  |      |                                                   |       |
  |  [인증서 검증 완료 및 Pre-Master Secret 생성]                   |       |
  |      |                                                   |       |
  |      | 5. Client Key Exchange                            |       |
  |      | (서버의 공개키로 암호화한 Pre-Master Secret) ----> |       |
  |      |                                                   |       |
  |      | 6. Change Cipher Spec                             |       |
  |      | (이제부터 대칭키로 암호화 시작함) -----------------> |       |
  |      |                                                   |       |
  |      | 7. Finished (핸드셰이크 무결성 해시)              |       |
  |      | --------------------------------------------------> |       |
  |      |                                                   |       |
  |      |                             8. Change Cipher Spec |       |
  |      | <------------------------------------------------- -- |       |
  |      |                                                   |       |
  |      |                                        9. Finished|       |
  |      | <--------------------------- (핸드셰이크 무결성 해시) -- |       |
  |      |                                                   |       |
  |      v       [핸드셰이크 완료. 안전한 Application Data 전송 시작]      v       |
  +------------------------------------------------------------------+
```

**[다이어그램 해설]** [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.2 핸드셰이크는 크게 4단계로 요약된다. 첫째, 서로 인사하며 사용할 암호화 방식과 난수(Random)를 교환한다(Hello). 둘째, 서버가 자신의 신분증([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서)을 보낸다. 셋째, 클라이언트는 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 안의 서버 공개키를 꺼내어, 앞으로 쓸 대칭키의 재료가 될 'Pre-[Master Secret](/knowledge-base/studynote/09_security/03_network_security/141_master_secret/)'을 암호화해서 서버에 보낸다. 서버는 자신의 개인키로 이를 복호화한다. 이제 양쪽은 [Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) Random, Server Random, Pre-Master Secret이라는 3가지 동일한 재료를 가지게 되었고, 이를 조합하여 최종 '[Master Secret](/knowledge-base/studynote/09_security/03_network_security/141_master_secret/) ([세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 대칭키)'을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)해낸다. 마지막 넷째, [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 대칭키가 서로 똑같은지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하기 위해 지금까지 주고받은 메시지의 해시값을 대칭키로 암호화하여 교환(Finished)함으로써 핸드셰이크를 성공적으로 마친다.

### 심층 동작 원리: RSA의 한계와 [ECDHE](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/)(타원 곡선 디피-헬만)로의 진화

앞서 설명한 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) 방식은 서버의 '개인키' 하나로 모든 Pre-Master Secret을 복호화한다. 이는 심각한 보안 결함을 낳는다. 만약 해커가 오늘 오간 모든 암호화된 통신을 저장해두었다가, 3년 뒤에 어떻게든 서버의 개인키를 탈취해 낸다면? 과거에 저장해둔 모든 Pre-Master Secret을 복호화하여 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/)키를 알아내고, 모든 통신 내용을 풀어버릴 수 있다.

이를 방어하기 위한 필수 메커니즘이 <strong>PFS (Perfect <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/">Forward</a> Secrecy, 완전 순방향 <a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a>)</strong>이며, 이를 구현하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 바로 <strong><a href="/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/">ECDHE</a> (Elliptic Curve Diffie-Hellman Ephemeral)</strong>이다.

① **파라미터 교환**: [Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) Exchange 단계에서, 클라이언트가 키를 만들어 서버 공개키로 암호화해 보내는 대신, 양쪽이 각각 임시(Ephemeral)로 사용할 공개키/개인키 쌍을 즉석에서 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다.
② **서버 서명**: 서버는 자신의 임시 공개키를 전송할 때, 클라이언트가 이를 믿을 수 있도록 기존의 공인 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 개인키로 '서명'하여 보낸다 (Server [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) Exchange 메시지 추가).
③ **독립적 대칭키 계산**: 양쪽은 타원 곡선 수학을 이용해 상대방의 임시 공개키와 자신의 임시 개인키를 결합 연산하여 동일한 Pre-Master Secret을 도출해낸다.
④ **임시 키 파기**: 핸드셰이크가 끝나면 양쪽은 이 임시 개인키를 즉시 메모리에서 삭제(파기)한다.
⑤ **PFS 달성**: 이제 대칭키를 만들었던 수학적 재료(임시 개인키)가 세상에서 영원히 사라졌다. 훗날 서버의 영구적인 개인키가 털리더라도, 이미 파기된 임시 키를 복원할 수 없으므로 과거의 통신 내역은 절대 해독할 수 없다.


[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3은 10년 만에 이루어진 메이저 업데이트로, [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)([Latency](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) 감소와 낡은 암호화 방식 폐기라는 두 가지 엄청난 혁신을 가져왔다.

| 비교 항목 | [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.2 | [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 | 판단 포인트 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/">Round Trip Time</a> (<a href="/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/">RTT</a>)</strong> | 2-[RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/) (총 4번 왕복) | <strong>1-<a href="/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/">RTT</a></strong> (총 2번 왕복) | 모바일 등 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 큰 네트워크 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) |
| **키 교환 방식** | [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/), [DHE](/knowledge-base/studynote/09_security/03_network_security/129_dhe_ephemeral_dh/), [ECDHE](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/) 혼용 | [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) 폐기, <strong>오직 <a href="/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/">ECDHE</a>/DHE만 허용</strong> | PFS (완전 순방향 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)) 강제 여부 |
| <strong>0-<a href="/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/">RTT</a> 지원 (재접속 시)</strong> | 미지원 (항상 1-[RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/) 이상) | 지원 ([초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 즉시 전송) | [세션 재개](/knowledge-base/studynote/03_network/13_network_security_basics/687_tls_session_resumption_ticket/) 속도 극대화 |
| **보안 강도 (Cipher Suite)** | 수십 개의 복잡한 조합, 취약 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 포함 | 안전성이 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 5개([AEAD](/knowledge-base/studynote/09_security/02_crypto/092_aead/))로 대폭 축소 | [보안 설정 오류](/knowledge-base/studynote/04_software_engineering/11_testing_validation/874_security_misconfiguration/)(Misconfiguration) 원천 차단 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>서 페이로드 암호화</strong> | 평문으로 전송됨 | Server Hello 이후 **모든 메시지 암호화** | 스니핑에 의한 서버 신원 노출([SNI](/knowledge-base/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/)) 방어 |

핸드셰이크 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 절반으로 줄인 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3의 1-[RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/) 파이프라인 변화를 시각화하면 그 혁신성을 명확히 이해할 수 있다.

```text
  +------------------------------------------------------------------+
  |                 TLS 1.2 vs TLS 1.3 핸드셰이크 지연(Latency) 비교        |
  +------------------------------------------------------------------+
  |                                                                  |
  | [TLS 1.2 : 2-RTT]                                                |
  | Client                      Server                               |
  |   |--- Client Hello ---------->| (1) 알고리즘 제안                     |
  |   |<--- Server Hello ---------| (2) 알고리즘 확정, 인증서 전달            |
  |   |--- Key Exchange ---------->| (3) 키 교환 재료 전송                  |
  |   |<--- Finished -------------| (4) 검증 완료. 데이터 전송 준비 끝         |
  |   |--- HTTP GET (Data) ------->| (5) 이제야 실제 데이터 요청              |
  |                                                                  |
  | [TLS 1.3 : 1-RTT]                                                |
  | Client                      Server                               |
  |   |--- Client Hello + Key ---->| (1) 암호 제안 + "내 키 재료도 일단 받아!"  |
  |   |<--- Server Hello + Cert --| (2) 암호 확정 + 인증서 + "내 키 재료 여깄다!"|
  |   |--- HTTP GET (Data) ------->| (3) 즉시 대칭키 계산 후 데이터 전송 시작     |
  |                                                                  |
  | 결과: TLS 1.3은 클라이언트가 처음 인사를 할 때, 아예 자신이 계산한 임시 공개키 |
  |      (Key Share)를 먼저 던져버린다. 왕복 1번(1-RTT)을 완전히 제거했다.       |
  +------------------------------------------------------------------+
```

**[다이어그램 해설]** 과거 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.2에서는 클라이언트가 서버가 무슨 암호화 방식을 고를지 몰랐기 때문에 일단 인사(Hello)만 하고 서버의 대답을 기다려야 했다. [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3에서는 허용되는 암호화 방식이 단 5개로 줄어들었다. 클라이언트는 "네가 최신 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 고를 확률이 매우 높으니, 아예 내 임시 공개키([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) Share)를 처음 인사할 때 같이 보낼게!"라며 선제적으로 재료를 전송해버린다. 서버는 이를 받자마자 자신의 키를 조합해 대칭키를 만들고, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서와 자신의 키 재료를 클라이언트에게 보낸다. 클라이언트는 이를 받는 즉시(1-[RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/) 만에) 대칭키를 완성하여 바로 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 암호화해 쏠 수 있다. 이 1-RTT의 단축은 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 심한 모바일 네트워크([LTE](/knowledge-base/studynote/03_network/15_nextgen_communication_architecture/752_lte_long_term_evolution_4g/)/[5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/))에서 웹페이지 로딩 속도를 혁신적으로 끌어올린 원동력이다.

### 과목 융합 관점

- <strong>시스템 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> 및 로드밸런싱 (L7 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">Proxy</a>)</strong>: 수백만 명의 사용자가 동시에 접속하는 대형 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) 비대칭키 복호화 연산은 웹 서버 CPU의 가장 큰 병목([Bottleneck](/knowledge-base/studynote/02_operating_system/10_security/617_io_bottleneck/))이다. 실무에서는 웹 서버 대신 앞단의 Nginx, HAProxy나 AWS ALB(Application [Load Balancer](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/))가 핸드셰이크를 전담하여 풀고 내부로는 평문 HTTP로 넘겨주는 SSL Termination ([Offloading](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/)) 아키텍처를 반드시 구성한다.
- <strong>최신 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">프로토콜</a> (<a href="/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/">HTTP</a>/3 및 <a href="/knowledge-base/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/">QUIC</a>)</strong>: 구글이 주도한 최신 웹 표준인 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/3는 [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 기반의 [QUIC](/knowledge-base/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/) [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)을 사용한다. QUIC은 전송 계층([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/))의 연결 수립(3-way Handshake)과 보안 계층의 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 핸드셰이크를 하나로 병합하여, 완전한 0-[RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/)/1-[RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/) 통신을 극대화하는 형태로 융합 발전했다.

- **📢 섹션 요약 비유**: 예전에는 상대방의 언어를 묻고(1왕복), 그 언어로 번역기를 가져와 대화하는(2왕복) 답답한 방식이었다면, 최신 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3은 전 세계 공통어(통일된 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) 하나만 쓰기로 합의하고 첫 만남부터 바로 본론으로 들어가는 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 회의와 같습니다.

---

## Ⅲ. 비교 및 연결

SSL/[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. ESP가 기반 조건을 만든다면, SSL/[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크는 그 위에서 핵심 메커니즘을 구현하고, VPN는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 구분 명확성과 설명력에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | ESP의 기반 정리 | SSL/[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크의 핵심 동작 | VPN의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | 구분 명확성 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: SSL/[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. **시나리오 — 구형 단말 호환성과 보안 컴플라이언스의 충돌**: 금융권 인프라 담당자가 보안 감사를 통과하기 위해 서버의 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.0, 1.1, 1.2를 모두 끄고 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3만 강제(Enforce)했다. 다음날 구형 안드로이드 기기와 오래된 Java 기반 B2B 연동 서버들이 접속 불가(Handshake Failure) 장애를 일으켰다. 아키텍트는 하위 호환성을 위해 <strong><a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/">TLS</a> 1.2를 허용하되, 취약한 Cipher Suite(<a href="/knowledge-base/studynote/09_security/02_crypto/081_rc4_stream_cipher/">RC4</a>, <a href="/knowledge-base/studynote/09_security/02_crypto/087_3des/">3DES</a>, <a href="/knowledge-base/studynote/09_security/02_crypto/089_cbc_mode/">CBC</a> 모드 등)를 서버 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a>에서 완전히 제거(Disable)</strong>하고 강력한 [ECDHE](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/)-[RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/)-AESGCM 조합만 우선 협상되도록(Server Cipher Order Preference) 타협점을 설계해야 한다.
2. <strong>시나리오 — 내부망 보안 장비(<a href="/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/">IPS</a>/<a href="/knowledge-base/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/">WAF</a>)의 가시성 상실 문제</strong>: 사내 직원들이 악성코드 사이트에 접속하는지 감시해야 하는 보안팀. 하지만 모든 통신이 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3으로 강력하게 암호화되어 [차세대 방화벽](/knowledge-base/studynote/09_security/05_web_app_security/216_ngfw_next_generation_firewall_dpi/)([NGFW](/knowledge-base/studynote/03_network/13_network_security_basics/698_ngfw_next_generation_firewall/))이나 [IPS](/knowledge-base/studynote/03_network/13_network_security_basics/695_ips_network_intrusion_prevention_system/) 장비가 페이로드를 열어볼 수 없게 되었다(가시성 맹인화). 이를 해결하기 위해 아키텍트는 사내 PC에 <strong>사설 Root <a href="/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/">CA</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>서를 강제 배포</strong>하고, [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)이 중간에서 클라이언트와 서버 양쪽으로 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크를 맺어 패킷을 열어보는 <strong>SSL Decryption (SSL Inspection / <a href="/knowledge-base/studynote/10_ai/03_llm_nlp/235_forward_backward_chaining/">Forward</a> <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">Proxy</a>)</strong> 기능을 활성화하는 실무적 판단을 내린다.
3. <strong>시나리오 — <a href="/knowledge-base/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/">SNI</a> (<a href="/knowledge-base/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/">Server Name Indication</a>) 미설정으로 인한 다중 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>서 오류</strong>: 하나의 물리적 Nginx 서버 (IP 1개)에 a.com과 b.com 두 개의 웹사이트를 호스팅 중이다. 클라이언트가 b.com에 접속했는데 자꾸 a.com의 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 떨어지며 보안 경고가 뜬다. 원인은 구형 클라이언트가 핸드셰이크의 첫 단계인 [Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) Hello 메시지에 자신이 접속하려는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이름([SNI](/knowledge-base/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/))을 넣지 않았기 때문이다. 아키텍트는 서버 측에서 여러 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 라우팅할 수 있도록 <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/">SNI</a> 확장을 필수로 요구</strong>하고, 이를 지원하지 않는 낡은 클라이언트의 접속을 차단해야 한다.

웹 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 운영에서 가장 많이 겪는 병목인 'CPU 과부하'를 해결하는 SSL [Offloading](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/) (Termination) 아키텍처를 시각화하면 대규모 트래픽 처리의 정석을 이해할 수 있다.

```text
  +------------------------------------------------------------------+
  |                 대규모 시스템의 SSL Offloading 아키텍처                  |
  +------------------------------------------------------------------+
  |                                                                  |
  | [클라이언트]                 [DMZ 구역]                 [내부 사설망]       |
  |                                                                  |
  |      ----- HTTPS ------> +--------------+ --- HTTP ----> [Web Server 1] |
  |    (TLS Handshake)    |  L7 Load     |                (연산 부하 없음) |
  |                       |  Balancer    |                               |
  |      ----- HTTPS ------> | (Nginx/ALB)  | --- HTTP ----> [Web Server 2] |
  |   (무거운 RSA 복호화)     |              |                (연산 부하 없음) |
  |                       +--------------+                               |
  |                          ^                                       |
  |                          | 인증서(Cert) 및 개인키 탑재 지점             |
  |                                                                  |
  | 판단: WAS(Web Application Server) 수십 대에 일일이 인증서를 설치하고 갱신하는 |
  |      운영 지옥을 피하고, 웹 서버의 CPU를 비즈니스 로직(DB 쿼리 등)에만 100%   |
  |      집중시키기 위해 프록시 단에서 핸드셰이크를 종료(Terminate)시키는 것이 정석.|
  +------------------------------------------------------------------+
```

**[다이어그램 해설]** 핸드셰이크 과정 중 서버가 클라이언트가 보낸 난수(Pre-[Master Secret](/knowledge-base/studynote/09_security/03_network_security/141_master_secret/))를 자신의 개인키로 푸는 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) 복호화 연산은 일반 대칭키 연산보다 수십~수백 배의 CPU 사이클을 잡아먹는다. 초당 수천 명의 접속이 몰리면 일반 웹 서버는 버티지 못한다. 따라서 실무 아키텍처는 가장 앞단의 L7 로드밸런서(또는 전용 [SSL VPN](/knowledge-base/studynote/09_security/03_network_security/283_ssl_vpn/) 장비, [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/))에 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 몰아서 설치한다. 로드밸런서는 클라이언트와 무거운 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크를 끝내고 페이로드를 복호화한 뒤, 안전한 내부 사설망([VPC](/knowledge-base/studynote/03_network/16_data_center_cloud/836_vpc_virtual_private_cloud_subnet_isolation/) 등) 안에 있는 백엔드 웹 서버로는 가벼운 평문 HTTP로 요청을 넘겨준다. 이를 통해 엄청난 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 향상과 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 관리의 중앙화를 동시에 이뤄낸다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **기술적**: Nginx/Apache [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)에서 `ssl_prefer_server_ciphers`가 On으로 되어 있어, 클라이언트의 취약한 암호 제안을 무시하고 서버의 안전한 암호군을 강제하고 있는가? [HSTS](/knowledge-base/studynote/09_security/05_web_app_security/1031_hsts/) ([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) Strict Transport [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) 헤더를 적용하여 평문 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 접속 시도를 브라우저 단에서 원천 차단하고 있는가?
- **운영·보안적**: Let's Encrypt 등을 이용해 90일 주기의 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 갱신 자동화(Certbot)가 구축되어 있는가? ([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 만료는 대형 IT 장애의 가장 흔한 원인 중 하나다). 낡은 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.0, 1.1은 완전히 비활성화(Disable)되어 컴플라이언스를 준수하고 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/knowledge-base/studynote/09_security/03_network_security/110_rsa/">RSA</a> 키 교환 방식 고집</strong>: 과거의 관성대로 PFS(완전 순방향 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/))를 지원하지 않는 TLS_RSA 암호군을 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)이나 서버에서 계속 허용하는 것. 만약 개인키가 유출되면 과거 수년 치의 사내 통신 덤프가 전부 해독되는 대참사로 이어진다. 무조건 [ECDHE](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/) 계열을 최우선으로 해야 한다.
- <strong>개발 환경에서의 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>서 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 무시</strong>: 개발자들이 로컬 환경에서 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 연동 시 에러를 피하기 위해 코드에 `rejectUnauthorized: false`나 `TrustAllCerts` 로직을 넣어 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 끄는 짓. 이 코드가 실수로 상용(Prod) 서버에 배포되면 핸드셰이크의 핵심인 '신원 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)'이 무력화되어 MITM 공격의 자동문이 열린다.

- **📢 섹션 요약 비유**: 수만 명의 방문객(트래픽)이 몰리는 놀이공원에서, 매표소 직원이 일일이 신분증을 검사하고 열쇠를 나눠주는 일(핸드셰이크)을 전담 부서(로드밸런서)로 완전히 분리해야만 놀이기구(웹 서버)가 멈추지 않고 신나게 돌아갈 수 있습니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 최적화 전 ([TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.2 / [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/)) | 최적화 후 ([TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 / [ECDHE](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/)) | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 2-[RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/) 핸드셰이크 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 발생 | 1-[RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/) 적용 (첫 연결 시간 반토막) | 모바일 및 글로벌 접속 환경에서 <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a>(TTFB) 30~50% 단축</strong> |
| **정성** | 개인키 유출 시 과거 트래픽 해독 위험 | PFS(완전 순방향 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)) 강제 적용 | 시스템 침해 사고 발생 시에도 <strong>과거 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> <a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a> 100% 보존</strong> |
| **정성** | 복잡한 수백 개의 취약 암호군 방치 | 안전성이 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)된 5개 [AEAD](/knowledge-base/studynote/09_security/02_crypto/092_aead/) 암호군 강제 | [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 오류로 인한 보안 사고 원천 차단 및 컴플라이언스 즉시 충족 |

### 미래 전망
- <strong>ECH (Encrypted <a href="/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/">Client</a> Hello)의 도입</strong>: [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3에서도 핸드셰이크 첫 단계의 [SNI](/knowledge-base/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/) ([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 이름)는 평문으로 노출되어, ISP나 국가 기관이 사용자가 어느 사이트에 접속하는지 감시하고 차단할 수 있었다. 이를 막기 위해 [Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) Hello 메시지 전체를 DNS에서 얻어온 서버의 공개키로 미리 암호화해버리는 ECH 기술이 점차 브라우저 표준으로 자리 잡으며 완벽한 프라이버시를 완성해 나갈 것이다.
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/">PQC</a> (<a href="/knowledge-base/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/">Post-Quantum Cryptography</a>) 적용 가속화</strong>: 양자 컴퓨터의 쇼어 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(Shor's [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))이 실용화되면, 핸드셰이크의 근간인 RSA와 ECDHE의 이산대수 문제가 단숨에 풀리게 된다. 이를 대비해 구글 크롬 등은 이미 [X25519](/knowledge-base/studynote/09_security/03_network_security/127_x25519/)(기존)와 Kyber(양자 내성) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 결합한 하이브리드 키 교환 방식을 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 핸드셰이크에 시범 적용하고 있다.

### 참고 표준
- **RFC 8446**: The Transport Layer [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) ([TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/)) [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) Version 1.3 (기존 구조를 갈아엎은 혁신적 표준)
- **RFC 5246**: The Transport Layer [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) ([TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/)) [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) Version 1.2
- **FIPS 140-2 / 140-3**: 미국 연방 정보 처리 표준 (허용되는 안전한 암호 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 규격)

SSL/[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크는 암호학의 가장 아름다운 응용이자, 신뢰할 수 없는 인터넷이라는 바다 위에 유일하게 안전한 다리를 놓아준 인류의 지적 자산이다. 앞으로도 더 가볍게, 더 빠르게, 더 안전하게 진화할 것이다.

마지막으로 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/1.1부터 최신 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/3에 이르기까지 핸드셰이크 오버헤드가 어떻게 압축되어 왔는지를 진화 로드맵으로 정리하면, 속도를 향한 집념을 엿볼 수 있다.

```text
  +------------------------------------------------------------------+
  |                 네트워크 핸드셰이크 진화 로드맵 (연결 속도 최적화)          |
  +------------------------------------------------------------------+
  |                                                                  |
  |  [HTTP/1.1 + TLS 1.2 (과거)] : 총 3-RTT                          |
  |   TCP 3-way Handshake (1-RTT) + TLS 1.2 Handshake (2-RTT)        |
  |   = 엄청난 왕복 지연 비용 (해외 망 접속 시 치명적)                       |
  |                                                                  |
  |  [HTTP/2 + TLS 1.3 (현재 주력)] : 총 2-RTT                        |
  |   TCP 3-way Handshake (1-RTT) + TLS 1.3 Handshake (1-RTT)        |
  |   = 암호화 협상 과정을 절반으로 줄여 속도 대폭 개선                       |
  |                                                                  |
  |  [HTTP/3 (QUIC) + TLS 1.3 (미래/최신)] : 총 1-RTT                 |
  |   UDP 기반 QUIC (연결+보안 통합 Handshake) (1-RTT)                 |
  |   * 심지어 이전에 접속했던 사이트는 0-RTT로 데이터 즉시 전송 가능             |
  |                                                                  |
  |  초점 이동: "보안은 무겁다"는 편견을 깨고, TCP의 한계를 벗어나 보안과 통신 연결을|
  |           하나의 동작으로 완전히 융합(Convergence)하는 방향으로 진화 중.    |
  +------------------------------------------------------------------+
```

**[다이어그램 해설]** 초창기 웹 통신은 문을 두드려 연결을 맺는 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 핸드셰이크(1번 왕복)가 끝나야만, 비로소 보안 협상을 위한 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크(2번 왕복)를 시작했다. 총 3번을 왕복해야 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보낼 수 있어 레이턴시가 컸다. [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3은 보안 왕복을 1번으로 줄였지만 TCP의 물리적 제약은 어쩔 수 없었다. 이 병목을 완전히 깨버린 것이 구글의 [QUIC](/knowledge-base/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/) ([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/3)이다. QUIC은 무거운 [TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/) 대신 가벼운 [UDP](/knowledge-base/studynote/03_network/08_transport_layer/406_udp_user_datagram_protocol_connectionless_fast/) 위에 독자적인 연결 제어를 구현하여, '연결 수립'과 '[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 키 교환'을 패킷 하나에 뭉쳐서(Piggyback) 동시에 쏴버린다. 결국 단 한 번의 왕복(1-[RTT](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/))만에 보안 채널이 뚫리는 기적을 만들어냈으며, 이는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 최적화의 극치를 보여준다.

- **📢 섹션 요약 비유**: 옛날에는 통신사 교환원을 거쳐 연결을 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고([TCP](/knowledge-base/studynote/03_network/08_transport_layer/405_tcp_transmission_control_protocol_connection_oriented/)), 상대방과 암호 책을 맞춘 뒤에야([TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.2) 대화가 가능했다면, 미래의 통신([QUIC](/knowledge-base/studynote/03_network/08_transport_layer/454_quic_quick_udp_internet_connections/)+[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3)은 수화기를 들자마자 0.1초 만에 비밀 암호로 다이렉트 통화가 연결되는 최첨단 핫라인(Hotline)으로 진화했습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [ESP](/knowledge-base/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| 정의 (Definition) | 용어의 시작점을 분명하게 만든다. |
| 비교 (Comparison) | 헷갈리는 개념의 경계를 드러낸다. |
| [VPN](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: ESP]
    |
    v
[현재 개념: SSL/TLS 핸드셰이크]
    |
    +---> [확장 A: VPN]
    +---> [확장 B: 컨텍스트 기반 용어 해석]
```

SSL/[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 핸드셰이크는 ESP에서 출발해 현재 메커니즘을 정교화하고, 이후 VPN와 [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 기반 용어 해석 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 핸드셰이크는 [스파이](/knowledge-base/studynote/04_software_engineering/11_testing_validation/853_spy_test_double/) 두 명이 처음 만나서 진짜 우리 편이 맞는지 신분증([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서)을 꼼꼼히 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하는 비밀 접선 과정이에요.
2. 신분이 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)되면, 둘은 아주 복잡한 퀴즈를 풀어서 오늘 하루만 쓸 '비밀번호(대칭키)'를 짠! 하고 만들어내죠.
3. 이 인사가 끝나고 나면, 두 [스파이](/knowledge-base/studynote/04_software_engineering/11_testing_validation/853_spy_test_double/)는 아무리 나쁜 악당이 엿듣고 있어도 그 비밀번호로만 해석할 수 있는 외계어로 대화하며 안전하게 정보를 주고받을 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 1103 / 1120

<- **이전**: [981. ESP (Encapsulating Security Payload)](/knowledge-base/studynote/03_network/19_frequent_topics_terms/981_esp_encapsulating_security_payload/)
**다음**: [983. VPN (가상 사설망)](/knowledge-base/studynote/03_network/19_frequent_topics_terms/983_vpn_virtual_private_network/) ->

---
