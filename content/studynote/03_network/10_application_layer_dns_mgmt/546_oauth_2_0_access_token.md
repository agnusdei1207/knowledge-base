---
title: "OAuth 2.0"
date: "2026-05-08"
tags:
  - "studynote-network"
weight: 546
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: OAuth 2.0는 이름 해석과 네트워크 관리에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: OAuth 2.0를 이해하면 가시성과 관리 자동화 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

- **개념**: OAuth 2.0은 인터넷 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 특정 애플리케이션([Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/))이 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)(Resource Server)에 저장된 사용자(Resource Owner)의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 접근하기 위해, 사용자 대신 <strong>접근 권한을 부여받는 과정(Access Token 발급)</strong>을 정의한 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)이다.

- **필요성**: 과거에는 새로운 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 앱에서 페이스북 친구 목록을 불러오기 위해 사용자의 페이스북 아이디와 비밀번호를 직접 입력받아야 했다. 이는 극히 위험한 보안 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)(Credential Sharing)이다. [서드파티](/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 앱이 해킹당하면 사용자의 원본 계정까지 통째로 털리게 되며, 앱이 권한을 남용(예: 마음대로 글 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))하는 것을 막을 수 없었다. 이를 해결하기 위해 비밀번호 대신 <strong>용도와 수명이 제한된 '출입증(Access Token)'</strong>만 발급해주는 표준 위임 체계가 필요했다.

- **💡 비유**: 당신(Resource Owner)이 호텔 방(Resource Server)에 친구([Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/))를 들여보낼 때, 친구에게 내 마스터키(비밀번호)를 통째로 주는 대신, 프론트 데스크([Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) Server)에 부탁해서 "수영장은 못 가고 방에만 3시간 동안 들어갈 수 있는 임시 방문증(Access Token)"을 발급받아 친구에게 주는 것과 완벽히 같습니다.

- **등장 배경 및 발전 과정**:
  1. **비밀번호 공유의 딜레마**: [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 웹에서는 [서드파티](/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 앱이 구글, 야후 등의 API를 호출하려면 사용자 비밀번호를 직접 받아야 했으나, 이는 심각한 보안 위협을 초래했다.
  2. **OAuth 1.0a의 등장과 한계 (2010년)**: 암호학적 서명(Signature) 기반으로 매우 안전했지만, 구현이 너무 복잡했고 모바일 기기나 데스크톱 앱에서 사용하기 어려웠다.
  3. **OAuth 2.0의 제정 (RFC 6749, 2012년)**: 서명 과정을 [HTTPS](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/)([TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/))에 전적으로 의임하여 구조를 대폭 단순화하고, 모바일, 웹, 브라우저리스 기기 등 다양한 환경에 맞는 4가지 권한 부여 방식(Grant Type)을 제공함으로써 폭발적으로 보급되었다.

```text
[커버로스]
    |
    v
[OAuth 2.0]
    |
    +---> [SAML 2.0]
```

- **📢 섹션 요약 비유**: 집주인(사용자)이 청소 업체([서드파티](/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 앱)에 현관문 비밀번호(패스워드)를 알려주는 대신, 경비실([인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 서버)을 통해 2시간만 유효한 임시 비밀번호(토큰)를 발급받아 주는 안전한 권한 위임 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소 (OAuth 2.0의 4대 역할)

| 요소명 | 역할 | 비유 |
|:---|:---|:---|
| **Resource Owner (자원 소유자)** | 정보의 주인이자 권한 위임의 승인자 (일반 사용자) | 호텔 방을 예약한 실제 투숙객 |
| <strong><a href="/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/">Client</a> (클라이언트)</strong> | 자원 소유자를 대신해 보호된 자원에 접근하려는 [서드파티](/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 애플리케이션 | 투숙객을 방문하려는 친구 |
| <strong><a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">Authorization</a> Server (<a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a> 서버)</strong> | 사용자를 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)하고 클라이언트에게 접근 권한(Access Token)을 발급하는 서버 (예: 구글 로그인 창) | 권한을 확인하고 임시 출입증을 만들어주는 프론트 데스크 |
| **Resource Server (자원 서버)** | 사용자의 보호된 자원([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/))을 호스팅하고, Access Token을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하여 응답하는 서버 (예: 구글 캘린더 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)) | 실제 출입증을 찍어야 열리는 호텔 방의 잠금장치 |

### [Authorization Code Grant](/studynote/09_security/05_web_app_security/508_authorization_code_grant/) (권한 부여 코드 승인 방식) 플로우

OAuth 2.0에서 가장 범용적이고 안전한 방식인 '[Authorization Code Grant](/studynote/09_security/05_web_app_security/508_authorization_code_grant/)'의 동작 흐름을 시각화하면, 왜 Access Token이 클라이언트 브라우저에 직접 노출되지 않고 안전하게 전달되는지 직관적으로 이해할 수 있다.

```text
  +------------------------------------------------------------------------+
  |         OAuth 2.0 : Authorization Code Grant (권한 부여 코드 방식)         |
  +------------------------------------------------------------------------+
  |                                                                        |
  |   [Resource Owner]             [Client]             [Authorization     |
  |       (사용자)                 (서드파티 앱)              Server]        |
  |          |                        |                        |           |
  |          | 1. "카카오로 로그인" 클릭 |                        |           |
  |          +------------------------>|                        |           |
  |          |                        | 2. 권한 부여 요청 (Redirect) |           |
  |          |<------------------------+------------------------>|           |
  |          |     (Client ID, Redirect URI 등 포함)           |           |
  |          |                        |                        |           |
  |          | 3. ID/PW 입력 및 권한 승인                       |           |
  |          +------------------------------------------------->|           |
  |          |                        |                        |           |
  |          | 4. 권한 부여 코드(Authorization Code) 전달 (Redirect) |           |
  |          |<------------------------+<------------------------+           |
  |          |                        |                        |           |
  |          | 5. Code 전달            |                        |           |
  |          +------------------------>|                        |           |
  |          |                        | 6. Token 요청 (Code + Client Secret) |
  |          |                        |------------------------>|           |
  |          |                        |                        |           |
  |          |                        | 7. Access Token 발급    |           |
  |          |                        |<------------------------+           |
  |          |                        |                        |           |
  |          |                        | 8. API 요청 (+Access Token)        |
  |          |                        |------------------------------> [Resource]
  |          |                        |                                 [Server]
  |          |                        | 9. 보호된 데이터 응답             |
  |          |                        |<------------------------------      |
  |          |                        |                                    |
  +------------------------------------------------------------------------+
```

**[다이어그램 해설]** 이 방식의 핵심은 토큰을 발급받기 전에 짧은 수명을 가진 `Authorization Code`를 먼저 발급받는다는 점이다. 사용자가 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 서버(예: 구글)에 로그인하여 승인하면, [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 서버는 사용자의 브라우저를 통해 클라이언트(앱)로 `Code`를 전달한다(단계 4, 5). 클라이언트는 이 `Code`를 자신의 백엔드 서버로 가져가, 클라이언트 비밀키([Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) [Secret](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/))와 함께 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 서버로 직접 전송하여 최종 `Access Token`을 교환받는다(단계 6, 7). 이렇게 하면 브라우저(Front-end)에는 수명이 짧은 `Code`만 노출되고, 실제 중요한 `Access Token`과 `Client Secret`은 안전한 백엔드 서버 간 통신(Back-channel)으로만 전달되므로 탈취 위험이 극도로 낮아진다.

- **📢 섹션 요약 비유**: OAuth 2.0의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

OAuth 2.0은 환경에 따라 4가지의 토큰 발급 방식을 제공한다.

| Grant Type (권한 부여 방식) | 특징 및 원리 | 주요 사용 환경 | [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) |
|:---|:---|:---|:---|
| <strong><a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">Authorization</a> <a href="/studynote/02_operating_system/02_process_thread/082_process_memory_structure/">Code</a></strong> | Code를 먼저 받고, 서버 단에서 Token으로 교환. [Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) [Secret](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/) 사용. | 웹 백엔드가 있는 일반적인 웹/모바일 앱 | **가장 높음** (표준 권장) |
| **Implicit** | [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) 교환 과정 없이 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 서버가 브라우저로 Token을 즉시 반환. | SPA (React, Vue) 등 백엔드가 없는 순수 프론트 앱 | **낮음** (토큰 노출 위험, 현재 사용 비권장) |
| **Resource Owner Password Credentials** | 사용자가 앱에 ID/PW를 직접 입력하고, 앱이 이를 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 서버로 전달해 Token 획득. | [1st Party](/studynote/12_it_management/05_security_compliance/928_cdp_first_party/) 앱 (자사 앱) 내부 환경 | **최하** (비밀번호 노출, 레거시) |
| <strong><a href="/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/">Client</a> Credentials</strong> | 사용자 개입 없이, 클라이언트가 자신의 자격증명만으로 Token 발급. | [M2M](/studynote/03_network/12_iot_wpan_edge/602_m2m_machine_to_machine_telemetry/) (Machine to Machine), 백엔드 서버 간 배치 작업 | 높음 (사용자 [컨텍스트](/studynote/02_operating_system/01_overview_architecture/033_context/) 없음) |

*※ 최근에는 보안 강화를 위해 SPA 환경에서도 Implicit 방식 대신 [PKCE](/studynote/09_security/05_web_app_security/509_pkce_public_client/) (Proof [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) for [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) Exchange)를 결합한 [Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) 방식을 사용하는 것이 산업 표준(BCP)이 되었다.*


### 1. OAuth 2.0 vs [OIDC](/studynote/09_security/11_iam_access_control/537_oidc_openid_connect/) ([OpenID Connect](/studynote/03_network/10_application_layer_dns_mgmt/548_openid_connect/)) vs SAML 2.0

| 비교 항목 | OAuth 2.0 | [OpenID Connect](/studynote/03_network/10_application_layer_dns_mgmt/548_openid_connect/) ([OIDC](/studynote/09_security/11_iam_access_control/537_oidc_openid_connect/)) | SAML 2.0 |
|:---|:---|:---|:---|
| **핵심 목적** | <strong><a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a> (<a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">Authorization</a>)</strong> - "무엇을 할 수 있는가" | <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> (<a href="/studynote/02_operating_system/10_security/604_authentication_factors/">Authentication</a>)</strong> - "누구인가" | <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a> 및 <a href="/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/">인가</a> (기업용 <a href="/studynote/09_security/11_iam_access_control/531_sso/">SSO</a>)</strong> |
| **토큰 형식** | Access Token (보통 Random String 또는 [JWT](/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/)) | [ID Token](/studynote/09_security/05_web_app_security/515_id_token_jwt/) (반드시 [JWT](/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/) 형식) | XML 기반 Assertion |
| **페이로드 내용** | 권한 범위 ([Scope](/studynote/09_security/05_web_app_security/512_oauth_scope/)), 만료 시간 | 사용자 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/) (sub), 프로필 정보 | 사용자 [식별자](/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/), [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/), 권한 등 상세 정보 |
| **주요 사용처** | [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 접근 권한 위임, [서드파티](/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 연동 | 소셜 로그인, 모바일/웹 [사용자 인증](/studynote/02_operating_system/10_security/604_authentication_factors/) | B2B 엔터프라이즈 환경, 레거시 [SSO](/studynote/09_security/11_iam_access_control/531_sso/) 연동 |

```text
  +-------------------------------------------------------------+
  |         OAuth 2.0 기반 OIDC (OpenID Connect) 계층 구조          |
  +-------------------------------------------------------------+
  |                                                             |
  |        +------------------------------------------+         |
  |        |          OpenID Connect (OIDC)           |         |
  |        |  (인증: ID Token, UserInfo 엔드포인트 추가)   |         |
  |        +------------------------------------------+         |
  |        |                OAuth 2.0                 |         |
  |        |    (인가: Access Token, Grant Types)      |         |
  |        +------------------------------------------+         |
  |        |             HTTP / TLS (HTTPS)           |         |
  |        +------------------------------------------+         |
  |                                                             |
  |  ※ OIDC는 OAuth 2.0의 Authorization Code 플로우를 그대로 사용하되, |
  |     결과물로 Access Token과 함께 JWT 형태의 **ID Token**을 추가로 |
  |     발급하여 클라이언트가 사용자의 '신원'을 검증하게 해준다.         |
  +-------------------------------------------------------------+
```

**[다이어그램 해설]** [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에 개발자들은 OAuth 2.0의 Access Token을 이용해 "구글 API를 호출할 수 있으니, 이 사람은 구글 회원이 맞겠지"라는 식으로 편법 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)(Pseudo-[Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/))을 구현했다. 그러나 Access Token은 '누구'인지 증명하는 용도가 아니어서 보안 취약점(토큰 치환 공격 등)이 발생했다. 이를 해결하기 위해 OAuth 2.0 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 위에 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/)) 목적의 표준 레이어인 OIDC를 얹었다. OIDC는 사용자 정보가 암호학적으로 서명된 `ID Token (JWT)`을 발급함으로써, "이 토큰은 진짜 구글이 발행했고, 로그인한 사람은 홍길동이 맞다"는 것을 애플리케이션이 독자적으로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있게 해준다.

### 과목 융합 관점
- <strong><a href="/studynote/04_software_engineering/01_overview_principles/001_software_engineering_definition/">소프트웨어 공학</a> (SE)</strong>: [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) ([Microservices Architecture](/studynote/13_cloud_architecture/03_msa_serverless/122_msa_microservices_architecture/)) 환경에서 각 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간의 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출 권한을 중앙 집중형 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 서버(예: Keycloak)를 통한 OAuth 2.0 체계로 분리하여 결합도를 낮추고 [보안성](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)을 높인다.
- <strong>보안 (<a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong>: OAuth 2.0 토큰 탈취 방지를 위한 [PKCE](/studynote/09_security/05_web_app_security/509_pkce_public_client/) (Proof [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) for [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) Exchange) 기법, [JWT](/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/) 서명 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(RS256)의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 필수 적용 등 암호학과 네트워크 보안의 종합판이다.

- **📢 섹션 요약 비유**: OAuth 2.0이 "수영장에 들어갈 수 있는 팔찌([인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/))"라면, OIDC는 그 팔찌 옆에 붙어있는 "사진이 박힌 주민등록증([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))"과 같아서 용도가 명확히 다릅니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. <strong>시나리오 — 모바일 앱에서의 보안 취약점과 <a href="/studynote/09_security/05_web_app_security/509_pkce_public_client/">PKCE</a> 적용</strong>: 네이티브 모바일 앱에서 [Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) 방식으로 카카오 로그인을 연동했다. 그러나 모바일 OS 특성상 딥링크(Custom URL Scheme)를 가로채는 악성 앱이 존재할 경우, 반환되는 `Code`를 탈취당할 위험이 있다. 클라이언트 [시크릿](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/)([Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) [Secret](/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/))을 앱에 하드코딩하는 것도 디컴파일 시 노출되므로 불가능하다.

   이러한 네이티브/SPA 환경의 태생적 취약점을 해결하기 위해 <strong><a href="/studynote/09_security/05_web_app_security/509_pkce_public_client/">PKCE</a> (Proof <a href="/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a> for <a href="/studynote/02_operating_system/02_process_thread/082_process_memory_structure/">Code</a> Exchange)</strong> 확장이 필수로 적용되어야 한다.

```text
  +-------------------------------------------------------------------+
  |             PKCE (Proof Key for Code Exchange) 원리                |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  1. 앱이 임의의 난수(Code Verifier) 생성                          |
  |  2. 난수를 해시 함수로 돌림 (Code Challenge)                       |
  |                                                                   |
  |  [Client (Mobile App)]                [Authorization Server]      |
  |          |                                      |                 |
  |          | 3. 로그인 요청 + Code Challenge 포함    |                 |
  |          |-------------------------------------->| (Challenge 저장)|
  |          |                                      |                 |
  |          | 4. Authorization Code 반환             |                 |
  |          |<--------------------------------------+                 |
  |          |                                      |                 |
  |          | 5. Token 요청 (Code + Code Verifier)   |                 |
  |          |-------------------------------------->| (Hash 검증)     |
  |          |                                      | Verifier를 해시해서|
  |          | 6. 검증 성공 시 Access Token 발급        | Challenge와 비교 |
  |          |<--------------------------------------+                 |
  |                                                                   |
  |  ※ 악성 앱이 4번에서 Code를 가로채도, 원본 난수(Verifier)를 모르기     |
  |     때문에 5번 토큰 교환 단계에서 인가 서버에 의해 거부된다.           |
  +-------------------------------------------------------------------+
```

2. <strong>시나리오 — Access Token 탈취 대비 및 <a href="/studynote/09_security/05_web_app_security/505_refresh_token/">Refresh Token</a> <a href="/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>: Access Token이 네트워크 스니핑이나 [XSS](/studynote/03_network/14_network_security_threats/726_xss_cross_site_scripting_types/) 공격으로 브라우저 단에서 탈취되면, 해커는 토큰 만료 전까지 피해자 행세를 할 수 있다. 이를 방어하기 위해 아키텍트는 <strong>1) Access Token의 수명을 극단적으로 짧게(예: 15분) <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>하고, <strong>2) 수명이 긴 <a href="/studynote/09_security/05_web_app_security/505_refresh_token/">Refresh Token</a>(예: 14일)을 HTTPOnly Secure <a href="/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/">쿠키</a>로 격리</strong>하여 발급하는 투트랙 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 설계해야 한다. Access Token이 만료되면 클라이언트는 백그라운드에서 Refresh Token을 이용해 조용히 새 Access Token을 재발급(Silent Refresh) 받는다. Refresh Token이 사용될 때마다 토큰 회전(Token Rotation) 기법을 적용해 훔친 Refresh Token의 재사용을 탐지하고 무효화해야 한다.

### 도입 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- **기술적**: SPA 환경에서 암묵적 방식(Implicit Grant)을 금지하고 [Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) + [PKCE](/studynote/09_security/05_web_app_security/509_pkce_public_client/) 방식을 채택했는가? Token 탈취를 막기 위해 Refresh Token은 HTTPOnly [속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)으로 보호되는가?
- **운영·보안적**: [Scope](/studynote/09_security/05_web_app_security/512_oauth_scope/)(권한 범위)를 [최소 권한 원칙](/studynote/09_security/01_intro_principles/010_least_privilege/)([Least Privilege](/studynote/09_security/01_intro_principles/010_least_privilege/))에 따라 세분화했는가? (예: `profile_read`와 `feed_write` 분리). [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 서버와의 모든 통신에 [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/)([HTTPS](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/))가 강제 적용되어 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>Access Token으로 <a href="/studynote/02_operating_system/10_security/604_authentication_factors/">사용자 인증</a> 시도</strong>: Access Token의 존재만으로 로그인 성공을 판단하는 행위. 반드시 OIDC의 ID Token을 서명 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하거나, 별도의 UserInfo API를 호출해 토큰의 유효성과 소유자를 확인해야 한다.
- <strong><a href="/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/">Client</a> <a href="/studynote/04_software_engineering/08_security_compliance_devsecops/514_secret_management_vault_kms/">Secret</a> 프론트엔드 하드코딩</strong>: React 앱이나 모바일 앱 소스 코드에 [Client](/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) Secret을 하드코딩하는 행위. 리버스 엔지니어링으로 즉시 탈취되어 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) [할당량](/studynote/02_operating_system/09_file_system/551_quota_disk_limit/)([Quota](/studynote/02_operating_system/09_file_system/551_quota_disk_limit/)) 도용 및 대규모 정보 유출로 이어진다.

- **📢 섹션 요약 비유**: 임시 방문증(Access Token)을 잃어버려도 도둑이 오래 못 쓰도록 유효기간을 15분으로 줄이고, 새 방문증을 발급받을 수 있는 진짜 신분증([Refresh Token](/studynote/09_security/05_web_app_security/505_refresh_token/))은 금고(HTTPOnly [쿠키](/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/))에 깊숙이 숨겨두는 설계의 지혜입니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 자체 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 시스템 유지 | OAuth 2.0 / [OIDC](/studynote/09_security/11_iam_access_control/537_oidc_openid_connect/) 위임 도입 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 가입자 전환율 (Conversion) 20% | 소셜 로그인 버튼 클릭으로 전환율 60% | 가입 마찰 감소로 **전환율 3배 증가** |
| **정량** | 회원 비밀번호 암호화 보관 및 정기 점검 비용 (연 1천만 원) | 비밀번호 저장 불필요 (비용 0) | 보안 관리 오버헤드 **100% 절감** |
| **정성** | [서드파티](/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 앱 연동 시 비밀번호 노출 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) 상존 | 제한적 권한 위임([Scope](/studynote/09_security/05_web_app_security/512_oauth_scope/))으로 사고 범위 축소 | 엔터프라이즈급 [제로 트러스트](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)) 연동 기반 확보 |

### 미래 전망
- <strong>FAPI (Financial-grade <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a>)</strong>: 기존 OAuth 2.0보다 보안 요건을 극도로 강화하여 상호 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([MTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/))과 토큰 바인딩(Token Binding)을 강제하는 금융권 특화 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 보안 표준으로, [마이데이터](/studynote/16_bigdata/01_intro/012_mydata/) 및 오픈뱅킹의 핵심 규격으로 정착하고 있다.
- **DPoP (Demonstrating Proof-of-Possession)**: Access Token 탈취 시 재사용을 막기 위해, 토큰 자체를 클라이언트의 공개키와 암호학적으로 결합(바인딩)시켜 '소유를 증명'한 클라이언트만 사용할 수 있게 하는 차세대 OAuth 2.0 보안 확장이 도입되고 있다.

### 참고 표준
- **RFC 6749**: The OAuth 2.0 [Authorization](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) Framework (기본 규격)
- **RFC 7636**: Proof [Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) for [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) Exchange by OAuth Public Clients ([PKCE](/studynote/09_security/05_web_app_security/509_pkce_public_client/))
- <strong><a href="/studynote/03_network/10_application_layer_dns_mgmt/548_openid_connect/">OpenID Connect</a> Core 1.0</strong>: OAuth 2.0 기반의 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([Authentication](/studynote/02_operating_system/10_security/604_authentication_factors/)) 확장 규격

과거의 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이 "성을 높게 쌓고 비밀번호를 지키는 것"이었다면, 클라우드와 [MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/) 시대의 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)은 "수많은 성문 사이를 안전하게 오가는 출입증(토큰)의 표준 유통망"을 구축하는 것이다. OAuth 2.0은 이 유통망의 전 세계 공통 인프라 역할을 하며, 기술사는 단순히 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 흐름을 외우는 것을 넘어 [PKCE](/studynote/09_security/05_web_app_security/509_pkce_public_client/), Token Rotation, FAPI 등 끊임없이 진화하는 취약점 방어 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)을 아키텍처에 적절히 배치할 수 있어야 한다.

```text
  +------------------------------------------------------------------+
  |               인증/인가 아키텍처 패러다임 변화                       |
  +------------------------------------------------------------------+
  |                                                                  |
  |   [과거: Monolithic & Silo]         [현재/미래: API & Federation]    |
  |                                                                  |
  |  +------------+                    +------------------------+      |
  |  | App A      | 사용자 ID/PW 입력  | Central Auth Server    |      |
  |  |(인증+비즈니스)|<----------+      | (OAuth 2.0 / OIDC)     |      |
  |  +------------+          |      +------------------------+      |
  |                          |                 | Token 발급           |
  |  +------------+          |                 v                    |
  |  | App B      | 사용자 ID/PW 입력  +--------+-------+-------+      |
  |  |(인증+비즈니스)|<----------+      | MSA A  | MSA B | App C |      |
  |  +------------+                 |(Resource Server API 군)|      |
  |                                 +--------+-------+-------+      |
  |                                                                  |
  |  • 계정 정보 중복 저장/유출 위험         • 비밀번호는 중앙 서버만 관리      |
  |  • 앱 간 권한 공유 불가능              • Token 기반 안전한 API 위임       |
  +------------------------------------------------------------------+
```

**[다이어그램 해설]** 과거의 [사일로](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)([Silo](/studynote/15_devops_sre/01_culture_methodology/002_silo_hyeonhyung/)) 아키텍처에서는 각 애플리케이션이 자체적으로 회원 DB를 가지고 ID/PW를 직접 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)했다. 이는 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 늘어날수록 보안 취약점(어느 한 곳이 뚫리면 크리덴셜 스터핑으로 전파)과 사용자 불편을 야기했다. 반면, 현재의 연합([Federation](/studynote/09_security/11_iam_access_control/543_federation/)) 아키텍처에서는 중앙 집중화된 [인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 서버(Central Auth Server)가 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 전담하고, 수많은 [마이크로서비스](/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/)([MSA](/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/))와 [서드파티](/studynote/05_database/06_dw_olap_trends/385_third_party_cookie_deprecation_cdw/) 앱들은 발급받은 Token만으로 권한을 상호 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다. OAuth 2.0은 이처럼 현대 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 컴퓨팅 환경을 떠받치는 가장 핵심적인 신뢰(Trust) 파이프라인이다.

- **📢 섹션 요약 비유**: 각 상점마다 회원 카드를 따로 파서 들고 다니던 과거에서 벗어나, 국가가 보증하는 '모바일 운전면허증(OAuth 2.0/[OIDC](/studynote/09_security/11_iam_access_control/537_oidc_openid_connect/))' 하나로 모든 상점을 빠르고 안전하게 이용하는 디지털 신분증 혁명과 같습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [커버로스](/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/) | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) ([Domain Name System](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)) | 이름과 주소를 연결해 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 접근성을 만든다. |
| 모니터링 (Monitoring) | 장애 징후를 조기에 발견하기 위한 기초다. |
| SAML 2.0 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: 커버로스]
    |
    v
[현재 개념: OAuth 2.0]
    |
    +---> [확장 A: SAML 2.0]
    +---> [확장 B: 자율 운영 네트워크]
```

OAuth 2.0는 [커버로스](/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/)에서 출발해 현재 메커니즘을 정교화하고, 이후 SAML 2.0와 자율 운영 네트워크 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구 이름을 전화번호부에서 찾는 것처럼 컴퓨터도 이름과 번호를 연결해요.
2. 이 개념은 누가 아픈지 살펴보는 건강검진표와 운영일지 역할도 해요.
3. 그래서 문제가 나도 빨리 찾고 고칠 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 667 / 1120

<- **이전**: [545. 커버로스 (Kerberos)](/studynote/03_network/10_application_layer_dns_mgmt/545_kerberos_kdc_ticket_based_auth/)
**다음**: [547. SAML 2.0 (Security Assertion Markup Language)](/studynote/03_network/10_application_layer_dns_mgmt/547_saml_2_0_security_assertion_markup_language/) ->

---
