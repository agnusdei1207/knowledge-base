---
title: 5. 인증성 (Authenticity) — 신원 확인, PKI, 디지털 서명, 메시지 인증
date: '2023-10-24'
description: 정보 주체의 신원과 정보 출처의 진위 여부를 암호학적으로 증명하는 인증성의 원리, PKI 및 실무 적용 방안
tags:
- security
---

# [[303_authentication_authorization_patterns|인증]]성 (Authenticity)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[303_authentication_authorization_patterns|인증]]성은 시스템에 접근하려는 사용자(주체)가 본인이 맞는지, 또는 수신한 [[001_dikw_pyramid|데이터]](객체)가 신뢰할 수 있는 정확한 출처에서 [[087_process_state_transition|생성]]되었는지를 증명하는 특성이다.
> 2. **가치**: 정보보안 3요소(CIA)만으로는 "누가 정보를 보냈는가"를 확증할 수 없는 한계를 극복하며, 모든 접근 제어([[509_authorization_models_rbac_abac|Authorization]])와 부인방지 통제의 논리적 전제 조건이 된다.
> 3. **융합**: 비밀번호 기반의 단순 [[303_authentication_authorization_patterns|인증]]을 넘어, 비대칭키 기반의 [[676_pki_public_key_infrastructure|공개키 기반 구조]]([[159_pki_public_key_infrastructure|PKI]]), 다중 요소 [[303_authentication_authorization_patterns|인증]]([[552_mfa|MFA]]), 그리고 현대의 FIDO(생체인증) 생태계와 융합되어 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]의 근간을 이룬다.

---

### Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

[[459_quic_fec_forward_error_correction|초기]] 정보보안의 근간은 [[001_cia_triad|CIA Triad]]([[002_confidentiality|기밀성]], [[003_integrity|무결성]], [[452_availability|가용성]])였으나, 인터넷이 글로벌 상거래와 금융의 인프라로 자리 잡으면서 심각한 결함이 발견되었다. 암호화를 통해 [[002_confidentiality|기밀성]]을 지키고 해시를 통해 [[001_dikw_pyramid|데이터]] [[003_integrity|무결성]]을 [[395_verification_process_review|검증]]하더라도, **"그 [[001_dikw_pyramid|데이터]]를 보낸 대상이 과연 내가 신뢰하는 진짜 주체가 맞는가?"**라는 질문에는 답할 수 없었던 것이다.

해커가 은행 시스템 관리자로 위장하여 완벽하게 암호화되고 [[003_integrity|무결성]]이 유지된 정상적인 송금 명령을 보낸다면 시스템은 이를 수행할 수밖에 없다. 이러한 문제를 해결하기 위해 등장한 개념이 바로 [[303_authentication_authorization_patterns|인증]]성(Authenticity)이다. [[303_authentication_authorization_patterns|인증]]성은 단순히 ID/PW를 [[396_validation|확인]]하는 [[655_ir_detection_analysis|식별]]의 단계를 넘어, [[652_cryptography_concept_encryption_decryption|암호학]]적 증명을 통해 발신자의 '진위(True Identity)'와 정보의 '진본성(Origin)'을 수학적으로 담보하는 과정이다.

다음 도식은 [[655_ir_detection_analysis|식별]]([[289_identification_flags_fragmentation_offset|Identification]]), [[303_authentication_authorization_patterns|인증]]([[604_authentication_factors|Authentication]]), [[509_authorization_models_rbac_abac|인가]]([[509_authorization_models_rbac_abac|Authorization]])의 단계를 구분하여 [[303_authentication_authorization_patterns|인증]]성의 위치와 중요성을 보여준다.

```text
[사용자/디바이스] 
       │
       ├─ (1) 식별(Identification) : "나는 Alice입니다" (ID 제시)
       │
       ▼
[인증 모듈 (Authenticity 검증)]
       │  ◀── (2) 인증(Authentication) : "Alice가 맞다는 것을 증명하시오" 
       │          (비밀번호 대조, OTP 검증, 전자서명 확인)
       ▼
[접근 제어 모듈 (IAM)]
       │  ◀── (3) 인가(Authorization) : "Alice는 이 폴더를 읽을 권한이 있는가?"
       │          (RBAC/ACL 검사 후 접근 허용/차단)
       ▼
[최종 데이터 접근]
```

이 그림의 핵심은 [[509_authorization_models_rbac_abac|인가]]([[387_access_control_pattern|접근 통제]])를 수행하기 전에 반드시 [[303_authentication_authorization_patterns|인증]]성이 100% 보장되어야 한다는 점이다. [[303_authentication_authorization_patterns|인증]]성이 뚫리는 순간 뒤에 이어지는 가장 강력한 접근 제어 모델도 완전히 무력화된다. 실무에서는 이 단계를 우회하려는 [[455_credential_stuffing|크리덴셜 스터핑]]([[455_credential_stuffing|Credential Stuffing]])이나 [[707_session_hijacking_tcp_seq_cookie|세션 하이재킹]] 공격이 끊이지 않으므로, [[303_authentication_authorization_patterns|인증]] 메커니즘 자체의 강건성이 전체 시스템 보안의 시작점 역할을 한다.

**📢 섹션 요약 비유**: [[655_ir_detection_analysis|식별]]이 호텔 프론트에 가서 "제 이름은 홍길동입니다"라고 말하는 것이라면, [[303_authentication_authorization_patterns|인증]]은 '주민등록증을 보여주고 지문을 찍어' 진짜 홍길동임을 증명하는 것입니다. 이 증명이 끝나야만 프론트 직원이 객실 열쇠([[509_authorization_models_rbac_abac|인가]])를 건네줍니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

[[303_authentication_authorization_patterns|인증]]성을 보장하는 아키텍처는 주로 주체의 신원을 [[396_validation|확인]]하는 기술과, 메시지의 출처를 [[396_validation|확인]]하는 [[652_cryptography_concept_encryption_decryption|암호학]]적 [[295_protocol_field_tcp_udp_icmp|프로토콜]]로 구성된다.

| 구성 요소 | 역할 및 목적 | 내부 동작 메커니즘 | 핵심 기술/표준 |
|:---|:---|:---|:---|
| **다중 요소 [[303_authentication_authorization_patterns|인증]] ([[552_mfa|MFA]])** | 단일 패스워드 유출 시의 취약점 보완 | 지식(지정된 암호), 소유(스마트폰/토큰), 생체(지문/홍채) 중 2가지 이상 [[250_cross_validation_kfold|교차 검증]] | [[558_totp|TOTP]], FIDO2, WebAuthn |
| **디지털 서명 ([[675_digital_signature_process_asymmetric_key|Digital Signature]])** | 메시지 발신자의 진위 여부 수학적 확증 | 발신자의 '개인키'로 해시를 암호화하고, 수신자가 발신자의 '공개키'로 복호화 [[395_verification_process_review|검증]] | [[110_rsa|RSA]], [[097_ecdsa_schnorr_signature_bitcoin|ECDSA]] |
| **[[159_pki_public_key_infrastructure|PKI]] ([[676_pki_public_key_infrastructure|공개키 기반 구조]])** | 수많은 사용자의 공개키에 대한 신뢰 체계 구축 | 공인된 [[303_authentication_authorization_patterns|인증]]기관([[089_contract_account_smart_contract|CA]])이 개인의 공개키에 서명하여 '[[303_authentication_authorization_patterns|인증]]서' 형태로 발급 | X.509 [[303_authentication_authorization_patterns|인증]]서, Root [[089_contract_account_smart_contract|CA]] |
| **메시지 [[303_authentication_authorization_patterns|인증]] 코드 ([[673_mac_message_authentication_code|MAC]])** | 대칭키 환경에서 메시지의 출처와 [[003_integrity|무결성]] [[396_validation|확인]] | 송수신자 간 사전 공유된 비밀키([[514_secret_management_vault_kms|Secret]] [[067_db_key_uniqueness_minimality|Key]])를 기반으로 해시 [[087_process_state_transition|생성]] | [[674_hmac_hash_based_mac_ipsec|HMAC]], [[105_cmac|CMAC]] |
| **SAML / [[537_oidc_openid_connect|OIDC]] ([[531_sso|SSO]] [[303_authentication_authorization_patterns|인증]])** | 여러 시스템 간의 분산된 [[303_authentication_authorization_patterns|인증]]성 신뢰 연합 | [[581_authentication_server|인증 서버]]([[536_idp_identity_provider|IdP]])가 신원 증명 토큰(Assertion/[[515_id_token_jwt|ID Token]])을 [[090_service_kubernetes_network_load_balancing|서비스]]([[166_sp|SP]])에 전달 | OAuth 2.0, [[549_jwt_json_web_token|JWT]] |

가장 범용적이고 강력한 [[303_authentication_authorization_patterns|인증]]성 메커니즘인 [[159_pki_public_key_infrastructure|PKI]]([[984_pki_public_key_infrastructure_ca_ra_certificate|Public Key Infrastructure]]) 기반의 클라이언트-서버 [[303_authentication_authorization_patterns|인증]] 흐름도를 살펴보자.

```text
[클라이언트 (Alice)]                                  [서버 (Bob)]
   │                                                      │
   │  1. "내 공개키가 포함된 인증서 보낼게" (Hello)       │
   ├─────────────────────────────────────────────────────>│
   │                                                      │
   │                                        (인증서 서명 확인) ◀─ "신뢰할 수 있는 CA가
   │                                        (유효기간 검증)      발급한 진짜 Alice가 맞군!"
   │                                                      │
   │  2. "그럼 네 진짜 개인키가 있는지 시험해볼게" (Challenge)│
   │<─────────────────────────────────────────────────────┤ (난수 난제 전송)
   │                                                      │
   │ (자신의 개인키로 난수 암호화 = 디지털 서명)          │
   │  3. "자, 내 개인키로 푼 답(서명)이야" (Response)     │
   ├─────────────────────────────────────────────────────>│
   │                                                      │
   │                                        (Alice의 공개키로 복호화 대조)
   │                                        "답이 맞군! 진짜 Alice로 인증 완료"
```

이 흐름(Challenge-Response)의 핵심은 [[303_authentication_authorization_patterns|인증]] 과정에서 클라이언트가 자신의 비밀번호나 개인키 자체를 네트워크로 절대 전송하지 않는다는 점이다. 오직 "개인키를 소유하고 있다는 수학적 증거"만을 보냄으로써 [[706_mitm_man_in_the_middle_hsts|중간자 공격]](MITM)이나 패킷 스니핑으로부터 [[303_authentication_authorization_patterns|인증]]의 안전성을 완벽히 보장한다. 이 구조는 현재 전 세계 웹의 기반인 [[694_thread_local_storage_tls|TLS]]/SSL 핸드셰이크의 근간이 되는 실무적 표준이다.

**📢 섹션 요약 비유**: 왕이 장군에게 밀서를 보낼 때, 왕만 가지고 있는 고유한 '옥새(개인키)'를 찍어 보냅니다. 장군은 옥새 모양이 그려진 관보(공개키)를 보고 진짜 왕의 명령([[303_authentication_authorization_patterns|인증]]성)임을 [[396_validation|확인]]하는 원리입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

[[303_authentication_authorization_patterns|인증]]성을 확보하는 방식은 요소의 강도와 [[652_cryptography_concept_encryption_decryption|암호학]]적 구조에 따라 각기 다른 장단점과 실무 적용 영역을 가진다.

**1. [[303_authentication_authorization_patterns|인증]] 요소([[604_authentication_factors|Authentication Factors]]) 비교 매트릭스**

```text
┌────────────┬────────────────────────┬─────────────────────┬───────────────────┐
│ 인증 요소  │ 사례                   │ 취약점 (보안 위험)  │ 실무적 특성       │
├────────────┼────────────────────────┼─────────────────────┼───────────────────┤
│ 지식 기반  │ 패스워드, 핀(PIN) 번호,│ 키보드 해킹, 숄더   │ 구현 비용이 가장  │
│ (Knowledge)│ 보안 질문              │ 서핑, 무차별 대입   │ 저렴하고 범용적임 │
├────────────┼────────────────────────┼─────────────────────┼───────────────────┤
│ 소유 기반  │ 스마트폰 SMS, OTP 기기,│ 기기 분실 도난, SMS │ 보안성은 높으나   │
│ (Possession)│ 스마트 카드, USB 토큰  │ 하이재킹(SIM 스와핑)│ 물리적 관리 필요  │
├────────────┼────────────────────────┼─────────────────────┼───────────────────┤
│ 내재 기반  │ 지문, 홍채, 정맥,      │ 복제된 생체 정보,   │ 사용성이 뛰어나며 │
│ (Inherence)│ 안면 인식, 목소리      │ 유출 시 변경 불가능 │ FIDO 표준 확산 중 │
└────────────┴────────────────────────┴─────────────────────┴───────────────────┘
```

이 매트릭스의 핵심은 단일 요소만으로는 현대의 [[303_authentication_authorization_patterns|인증]]성 파괴 공격([[752_phishing|피싱]], [[756_smishing|스미싱]] 등)을 방어할 수 없다는 점이다. 패스워드는 쉽게 털리고, SMS [[748_otp|OTP]] 역시 복제된 유심칩에 의해 우회될 수 있다. 따라서 금융 및 주요 IT 실무에서는 반드시 성질이 다른 두 개의 요소(예: 지식+소유, 소유+생체)를 결합하는 다중 요소 [[303_authentication_authorization_patterns|인증]]([[552_mfa|MFA]])을 시스템 아키텍처에 강제한다.

**2. [[673_mac_message_authentication_code|MAC]](메시지 [[303_authentication_authorization_patterns|인증]] 코드) vs 디지털 서명 비교**
[[001_dikw_pyramid|데이터]]의 출처를 [[303_authentication_authorization_patterns|인증]]하는 두 [[652_cryptography_concept_encryption_decryption|암호학]] 기술을 비교하면 명확한 차이가 존재한다.
- **[[673_mac_message_authentication_code|MAC]] (대칭키 기반)**: 송신자와 수신자가 동일한 비밀키를 공유한다. 처리 속도가 빠르기 때문에 [[014_api_posix|API]] 통신([[549_jwt_json_web_token|JWT]] 토큰 서명 등)에 유리하다. 하지만 양쪽 모두 같은 키를 가지므로, A가 보낸 메시지를 B가 자신이 만들지 않았다고 법적으로 주장할 때 "부인방지(Non-repudiation)" 효과를 제공하지 못한다.
- **디지털 서명 (비대칭키 기반)**: 개인키는 오직 송신자만 소유한다. 따라서 발신자가 "나는 서명하지 않았다"고 발뺌하는 것을 완벽히 차단(부인방지 보장)한다. 법적 효력이 필요한 전자계약이나 공공 시스템에 필수적이다.

**📢 섹션 요약 비유**: 집 열쇠(대칭키 [[673_mac_message_authentication_code|MAC]])는 가족 누구나 가지고 있어서 거실에 놓인 물건을 누가 가져다 놓았는지 정확히 증명할 수 없지만, 주민등록증(개인키 [[675_digital_signature_process_asymmetric_key|전자서명]])은 오직 나만 발급받을 수 있어 은행 대출 시 내가 했다는 것을 완벽히 증명(부인방지)할 수 있습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([[268_strategy_pattern|Strategy]] & Decision)

실제 엔터프라이즈 환경에서는 수만 명의 임직원과 분산된 애플리케이션 사이에서 [[303_authentication_authorization_patterns|인증]]성을 효율적으로 통제해야 하는 거대한 과제에 직면한다.

1. **시나리오 1: 사내 수십 개의 업무 시스템 간 [[303_authentication_authorization_patterns|인증]] 연동 ([[531_sso|SSO]])**
   - **상황**: 임직원이 메일, HR, 회계 시스템에 접속할 때마다 각기 다른 ID/PW를 입력해야 하여 편의성이 극도로 저하되고 비밀번호 메모 등으로 인한 유출 리스크가 증가함.
   - **판단**: 각 애플리케이션이 개별적으로 [[303_authentication_authorization_patterns|인증]]성을 판단하는 구조를 폐기해야 한다. 대신, 중앙 집중화된 신원 제공자([[536_idp_identity_provider|Identity Provider]], [[536_idp_identity_provider|IdP]])를 구축하고 **SAML 2.0 또는 [[537_oidc_openid_connect|OIDC]]([[548_openid_connect|OpenID Connect]])** 기반의 [[531_sso|SSO]]([[531_sso|Single Sign-On]]) 아키텍처를 도입한다. 사용자는 아침에 한 번만 강력한 MFA를 거쳐 [[303_authentication_authorization_patterns|인증]] 토큰을 발급받고, 이후 시스템들은 해당 토큰의 '디지털 서명'만을 [[395_verification_process_review|검증]]하여 [[303_authentication_authorization_patterns|인증]]성을 위임받는다.

2. **시나리오 2: [[532_microservices_decomposition_patterns|마이크로서비스]]([[619_msa_traffic_hardware|MSA]]) 환경에서의 [[014_api_posix|API]] [[303_authentication_authorization_patterns|인증]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]])**
   - **상황**: 내부망에 배포된 [[561_container_based_deployment|컨테이너]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]]) A가 [[561_container_based_deployment|컨테이너]] B의 API를 호출할 때, 내부망이라는 이유로 [[303_authentication_authorization_patterns|인증]] 없이 IP만 믿고 허용해옴.
   - **판단**: 내부망을 신뢰하는 접근은 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]]([[667_zero_trust_runtime_integrity_measurement|Zero Trust]]) 철학에 완전히 위배된다. 해커가 A를 장악하면 B로 무혈입성(Lateral Movement)하게 된다. 따라서 **[[831_mtls_mutual_tls_microservices_zero_trust|mTLS]]([[187_mtls_mutual_tls_authentication|Mutual TLS]])**를 적용하여야 한다. [[090_service_kubernetes_network_load_balancing|서비스]] 메쉬([[828_service_mesh_microservice_communication_infrastructure|Service Mesh]]) 환경에서 A와 B는 통신할 때 상호 간에 [[159_pki_public_key_infrastructure|PKI]] [[303_authentication_authorization_patterns|인증]]서를 교환하여 기계 간(Machine-to-Machine)의 강력한 상호 [[303_authentication_authorization_patterns|인증]]성(Mutual Authenticity)을 실시간으로 [[396_validation|확인]]해야 한다.

다음은 현대 비밀번호 없는(Passwordless) [[303_authentication_authorization_patterns|인증]]의 표준인 FIDO2(WebAuthn)의 동작 플로우다.

```text
[스마트폰/PC (Authenticator)]              [웹 서비스 (Relying Party)]
 (내부의 안전한 저장소 Secure Enclave)
          │                                           │
          │ ◀──────── 1. 로그인 요청 (Challenge 난수) ┤
          │                                           │
 2. 사용자 지문 인식 (로컬 생체 검증)                 │
          │                                           │
 3. 잠금 해제된 '개인키'로 난수 서명                  │
          │                                           │
          ├────── 4. 서명된 데이터 전송 ─────────────>│
                                                      │
                                   5. 서버에 보관된 '공개키'로 서명 검증
                                   6. (인증성 통과!) 로그인 승인
```

이 플로우의 핵심은 지문이나 얼굴 등 사용자의 '생체 정보'가 절대 네트워크를 타고 서버로 넘어가지 않는다는 점이다. 생체 정보는 오직 내 기기 안에서 개인키의 잠금을 푸는 열쇠 역할만 한다. 이를 통해 대규모 서버 해킹이 발생하더라도 해커가 얻을 수 있는 것은 쓸모없는 '공개키'뿐이므로 [[303_authentication_authorization_patterns|인증]] 정보 유출 위험을 원천적으로 제거한 혁신적인 설계다.

**📢 섹션 요약 비유**: 은행 지점에 내 인감도장(개인키/생체정보)을 맡겨두는 과거의 위험한 방식이 아니라, 도장은 철저히 내 금고에 보관하고 은행에는 도장이 찍힌 모양의 사본(공개키)만 등록해 두어, 매번 내가 서류에 직접 도장을 찍어 제출하는 안전한 방식과 같습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

견고한 [[303_authentication_authorization_patterns|인증]]성 아키텍처는 조직 내부의 보안 수준을 비약적으로 끌어올리는 동시에 법적 책임을 명확히 분리하는 기반이 된다.

| 기대효과 구분 | 단순 ID/PW [[303_authentication_authorization_patterns|인증]] 환경 | [[159_pki_public_key_infrastructure|PKI]] 및 [[552_mfa|MFA]] 적용 환경 | 보안적/비즈니스적 혜택 |
|:---|:---|:---|:---|
| **계정 탈취 방어** | [[752_phishing|피싱]] 공격 시 100% 탈취 및 악용 | FIDO/[[552_mfa|MFA]] 적용 시 [[752_phishing|피싱]]에 의한 탈취 원천 무력화 | 크리덴셜 관련 침해 사고 [[784_zeroization_circuit|제로화]] |
| **디지털 [[606_auditing_linux_auditd|감사]]([[363_audit|Audit]])**| 행위자의 부인(치명적 책임 전가) | [[675_digital_signature_process_asymmetric_key|전자서명]] 기록으로 완벽한 부인방지 및 추적성 제공 | 법적/재무적 분쟁 시 완벽한 증거 효력 |
| **운영 표준화** | 각 시스템별 파편화된 [[303_authentication_authorization_patterns|인증]] [[164_policy|정책]] | 중앙화된 [[526_iam|IAM]]/SSO로 신원 생명주기(Lifecycle) 통합 관리| 보안 운영 비용 감소 및 입퇴사자 관리 자동화 |

미래의 [[303_authentication_authorization_patterns|인증]]성 패러다임은 중앙 기관이 내 신원을 보증하는 모델에서, 정보 주체 스스로 신원을 증명하고 관리하는 **[[052_did_architecture_issuer_holder_verifier_vc_vp|탈중앙화 신원증명]]([[231_did_decentralized_identity|DID]], Decentralized Identity)**으로 급격히 진화하고 있다. [[004_blockchain|블록체인]] 기반의 [[231_did_decentralized_identity|DID]] 체계에서는 기업이나 정부가 나의 [[303_authentication_authorization_patterns|인증]] [[001_dikw_pyramid|데이터]]를 독점하지 않으며, 내가 필요할 때 필요한 [[082_attribute_types_er_model|속성]](예: 성인 [[303_authentication_authorization_patterns|인증]] 시 나이 정보만)만을 선별적으로 제공([[229_zkp_data_clean_room|영지식 증명]])할 수 있다. 정보보안 기술사적 관점에서 볼 때, [[303_authentication_authorization_patterns|인증]]성은 단순한 방패를 넘어 모든 디지털 경제 거래의 신뢰를 창출하는 사회적 인프라로 격상되고 있다.

**📢 섹션 요약 비유**: 과거의 [[303_authentication_authorization_patterns|인증]]이 동네 슈퍼 주인이 단골 손님 얼굴을 알아보고 외상을 주는 수준이었다면, 미래의 [[303_authentication_authorization_patterns|인증]]성은 위조가 불가능한 글로벌 [[004_blockchain|블록체인]] 여권을 통해 전 세계 어디서나 나임을 완벽하게 증명하는 디지털 시민권 체계와 같습니다.

---

### 📌 관련 개념 부록 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])
- **부인방지 (Non-repudiation)** | [[303_authentication_authorization_patterns|인증]]성과 [[003_integrity|무결성]]이 결합되어, 특정 주체가 특정 행위를 했음을 법적으로 부인하지 못하게 하는 보안 요건
- **[[159_pki_public_key_infrastructure|PKI]] ([[984_pki_public_key_infrastructure_ca_ra_certificate|Public Key Infrastructure]])** | [[303_authentication_authorization_patterns|인증]]성의 신뢰 근간이 되는 [[303_authentication_authorization_patterns|인증]]서(Certificate)를 발급, 폐지, 관리하는 광범위한 체계
- **[[526_iam|IAM]] (Identity and Access [[372_management|Management]])** | 조직 내 수많은 사용자의 [[655_ir_detection_analysis|식별]], [[303_authentication_authorization_patterns|인증]], [[509_authorization_models_rbac_abac|인가]] 사이클을 중앙에서 통합 관리하는 보안 프레임워크
- **OAuth 2.0 / [[537_oidc_openid_connect|OIDC]]** | [[303_authentication_authorization_patterns|인증]]성과 권한 위임을 안전하게 타사 [[090_service_kubernetes_network_load_balancing|서비스]]와 연동하기 위한 현대적인 [[014_api_posix|API]] [[509_authorization_models_rbac_abac|인가]]/[[303_authentication_authorization_patterns|인증]] [[295_protocol_field_tcp_udp_icmp|프로토콜]]
- **[[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]])** | 내부망이라도 무조건 의심하며, 모든 요청에 대해 강력한 [[033_context|컨텍스트]] 기반의 [[303_authentication_authorization_patterns|인증]]성을 매번 요구하는 보안 철학

### 📈 관련 키워드 및 발전 흐름도

```text
[부인방지 (Non-repudiation)]
    │
    ▼
[PKI (Public Key Infrastructure)]
    │
    ▼
[IAM (Identity and Access Management)]
    │
    ▼
[OAuth 2.0 / OIDC]
    │
    ▼
[제로 트러스트 (Zero Trust)]
```

이 흐름도는 부인방지 (Non-repudiation)에서 출발해 [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]])까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. **[[303_authentication_authorization_patterns|인증]]성**: 방문을 두드리는 사람이 진짜 엄마인지, 아니면 엄마 목소리를 흉내 내는 나쁜 늑대인지 [[396_validation|확인]]하는 방법이에요.
2. **원리**: 단순히 엄마 목소리만 듣고 여는 게 아니라, 엄마와 나만 아는 비밀 암호([[303_authentication_authorization_patterns|인증]]서)를 대답하게 하거나 얼굴을 보여달라고 하는 거예요.
3. **효과**: 이렇게 꼼꼼하게 [[396_validation|확인]]하면 아무리 똑똑한 나쁜 늑대라도 절대 속이고 집 안으로 들어올 수 없게 된답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 5 / 1108

← **이전**: [[004_availability|4. 가용성 (Availability) — HA 설계, RAID, 부하 분산, DDoS 방어, SLA]]
**다음**: [[006_security_governance|6. 보안 거버넌스 (Security Governance)]] →

---
