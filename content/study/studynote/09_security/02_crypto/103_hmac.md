---
title: 103. HMAC (Hash-based Message Authentication Code) — 키 혼입 해시
date: '2026-04-05'
tags:
- studynote-security
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[674_hmac_hash_based_mac_ipsec|HMAC]] (Hash-based [[673_mac_message_authentication_code|Message Authentication Code]])은 암호학적 [[667_hash_function_integrity_one_way|해시 함수]]에 송수신자만이 아는 '비밀키([[514_secret_management_vault_kms|Secret]] [[067_db_key_uniqueness_minimality|Key]])'를 결합하여 해시값을 [[087_process_state_transition|생성]]함으로써, 메시지의 [[003_integrity|무결성]]과 송신자의 [[303_authentication_authorization_patterns|인증]]을 동시에 보장하는 기술이다.
> 2. **가치**: 단순 해시는 누구나 값을 변조하고 새로운 해시를 씌울 수 있지만, HMAC은 비밀키가 없으면 유효한 해시 태그를 만들 수 없으므로 [[706_mitm_man_in_the_middle_hsts|중간자 공격]](Man-in-the-Middle)에 의한 [[001_dikw_pyramid|데이터]] 위변조를 완벽하게 차단한다.
> 3. **판단 포인트**: [[674_hmac_hash_based_mac_ipsec|HMAC]] 자체는 [[001_dikw_pyramid|데이터]]를 암호화하여 숨기지 않는다. 따라서 [[002_confidentiality|기밀성]]이 필요 없고 오직 "내용이 바뀌지 않았고, 권한 있는 자가 보낸 것이 맞다"는 증명만 필요한 [[014_api_posix|API]] [[303_authentication_authorization_patterns|인증]]([[549_jwt_json_web_token|JWT]], AWS [[014_api_posix|API]] 등)에서 가장 강력하고 가벼운 수단으로 사용된다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]]를 전송할 때 [[001_dikw_pyramid|데이터]]가 중간에 깨지거나 변조되었는지 [[396_validation|확인]]하기 위해 해시(Hash) 함수(예: SHA-256)를 사용한다. 하지만 일반적인 [[667_hash_function_integrity_one_way|해시 함수]]는 키([[067_db_key_uniqueness_minimality|Key]])가 없는 공개된 알고리즘이므로 심각한 보안 구멍이 발생한다. 해커가 통신을 가로채서 [[001_dikw_pyramid|데이터]]를 조작한 뒤, 조작된 [[001_dikw_pyramid|데이터]]로 해시 믹서기를 다시 돌려 새로운 해시값을 붙여 보내면 수신자는 정상적인 [[001_dikw_pyramid|데이터]]로 착각하게 된다.

이러한 무방비 상태를 해결하기 위해 등장한 개념이 [[673_mac_message_authentication_code|MAC]](메시지 [[303_authentication_authorization_patterns|인증]] 코드)이다. 메시지를 해시할 때 '통신 당사자들만 비밀리에 공유하는 열쇠([[067_db_key_uniqueness_minimality|Key]])'를 함께 넣고 돌리자는 아이디어다. 해커가 [[001_dikw_pyramid|데이터]]를 고치더라도 비밀키를 모르기 때문에 수신자 서버가 요구하는 정확한 해시 결과를 절대 만들어낼 수 없다. 그 [[673_mac_message_authentication_code|MAC]] 구조 중에서 [[667_hash_function_integrity_one_way|해시 함수]]를 엔진으로 사용하는 가장 표준적이고 안전한 방식이 바로 HMAC이다.

- **📢 섹션 요약 비유**: 일반 해시가 서류에 누구나 파서 찍을 수 있는 '막도장'이라면, HMAC은 나랑 은행만 공유하는 '특수 잉크'를 섞어서 찍는 도장이다. 도둑이 서류를 위조해 새 도장을 찍어도 잉크 성분이 달라 바로 들통난다.

---

## Ⅱ. 아키텍처 및 핵심 원리

단순히 `Hash(비밀키 + 메시지)` 형태로 이어 붙이는 [[149_serial_communication_rs232_rs485|직렬]] 연산은 해커가 원본 메시지 뒤에 악성 코드를 덧붙여 정상 해시를 뽑아내는 **길이 연장 공격(Length Extension Attack)**에 매우 취약하다. 이를 방어하기 위해 HMAC은 1996년 고안된 **이중 해싱 샌드위치 구조**를 사용한다.

핵심 원리는 비밀키를 각기 다른 상수(ipad, opad)와 XOR 연산하여 두 개의 다른 열쇠 껍질을 만든 뒤, 안쪽과 바깥쪽에서 두 번 해시를 수행하는 것이다.

| 연산 요소 | 설명 및 역할 |
| :--- | :--- |
| **비밀키 ($K$)** | 송수신자가 사전 공유한 비밀값. 길이가 길면 해시하고, 짧으면 0으로 [[098_padding_convolutional_neural_network_same_valid|패딩]] |
| **$ipad$ / $opad$** | 내부 [[098_padding_convolutional_neural_network_same_valid|패딩]](0x36)과 외부 [[098_padding_convolutional_neural_network_same_valid|패딩]](0x5C). 하나의 키를 두 개의 독립적인 키처럼 변형시킴 |
| **내부 해시 (Inner Hash)** | `Hash((K ⊕ ipad) || Message)` $\rightarrow$ 메시지를 1차적으로 키와 비벼서 [[571_protection_vs_security|보호]] |
| **외부 해시 (Outer Hash)** | `Hash((K ⊕ opad) || Inner_Hash_Result)` $\rightarrow$ 길이 연장 공격을 수학적으로 차단 |

```text
┌──────────────────────────────────────────────────────────────┐
│           HMAC의 이중 샌드위치 방어 아키텍처 (XOR & Hash)    │
├──────────────────────────────────────────────────────────────┤
│ [1차: 내부 방어벽]                                           │
│  ( 비밀키 ⊕ ipad )  +  [ 원본 메시지 ] ──▶ [ Hash 엔진 ]     │
│                                                 │            │
│                                                 ▼            │
│ [2차: 외부 방어벽]                        (1차 해시 덩어리)  │
│  ( 비밀키 ⊕ opad )  +  [ 1차 해시 덩어리 ] ──▶ [ Hash 엔진 ] │
│                                                 │            │
│                                                 ▼            │
│                                         ★ [ 최종 HMAC 태그 ] │
└──────────────────────────────────────────────────────────────┘
```

이 기묘한 이중 구조 덕분에 내부에 사용된 해시 엔진([[668_md5_hash_collision_vulnerability|MD5]] 등)에 다소 취약점이 발견되더라도, 밖을 감싼 두 번째 껍질 구조가 방어선을 유지하여 전체 HMAC의 안전성이 훼손되지 않는 기적 같은 방어력을 발휘한다.

- **📢 섹션 요약 비유**: 독가스(해킹)를 막기 위해, 고기를 유리 상자(내부 해시)에 넣고 특수 열쇠로 잠근 뒤, 그 상자를 통째로 다시 강철 금고(외부 해시)에 넣고 또 다른 열쇠로 잠그는 이중 포장 기법이다.

---

## Ⅲ. 비교 및 연결

HMAC은 [[003_integrity|무결성]]과 [[303_authentication_authorization_patterns|인증]]을 제공하지만, '[[002_confidentiality|기밀성]](암호화)'은 제공하지 않는다. 따라서 유사한 암호학적 도구들과 정확히 구분하여 사용해야 한다.

| 비교 항목 | 일반 해시 (SHA-256) | [[674_hmac_hash_based_mac_ipsec|HMAC]] ([[674_hmac_hash_based_mac_ipsec|Hash-based MAC]]) | [[076_symmetric_encryption|대칭키 암호]] ([[656_aes_advanced_encryption_standard_rijndael|AES]]-256) | [[675_digital_signature_process_asymmetric_key|전자서명]] ([[110_rsa|RSA]] Sign) |
| :--- | :--- | :--- | :--- | :--- |
| **주요 목적** | [[442_consistency_integrity|무결성 보장]] ([[501_file_definition_logical_record|파일]] [[112_checksum|체크섬]]) | [[003_integrity|무결성]] + 송신자 [[303_authentication_authorization_patterns|인증]] | [[002_confidentiality|기밀성]] 보장 (내용 숨김) | [[003_integrity|무결성]] + [[303_authentication_authorization_patterns|인증]] + **부인 방지** |
| **사용 키([[067_db_key_uniqueness_minimality|Key]])** | 없음 | 송수신자 공유 비밀키 (대칭) | 송수신자 공유 비밀키 (대칭) | 송신자의 개인키/공개키 (비대칭) |
| **조작/위조 방어**| 불가능 (누구나 해시 [[087_process_state_transition|생성]]) | 완벽 방어 | 방어 불가능 ([[001_dikw_pyramid|데이터]] 깨짐 [[396_validation|확인]] 불가) | 완벽 방어 |
| **속도** | 매우 빠름 | 빠름 (해시 2번 수행) | [[001_dikw_pyramid|데이터]] 크기에 비례 | 매우 느림 (수학적 연산 복잡) |

실무에서는 메시지의 내용을 숨길 필요 없이 빠른 [[303_authentication_authorization_patterns|인증]]이 필요할 때 HMAC을 단독으로 쓴다. 만약 내용도 숨기고 [[303_authentication_authorization_patterns|인증]]도 해야 한다면 '[[656_aes_advanced_encryption_standard_rijndael|AES]]-GCM' 같은 [[303_authentication_authorization_patterns|인증]] 암호화([[092_aead|AEAD]]) 모드를 사용하거나, [[656_aes_advanced_encryption_standard_rijndael|AES]] 암호문 뒤에 HMAC을 붙이는 [[673_mac_message_authentication_code|MAC]]-then-Encrypt 방식을 혼합하여 사용하게 된다.

- **📢 섹션 요약 비유**: [[656_aes_advanced_encryption_standard_rijndael|AES]] 암호화가 편지 내용을 못 읽게 '암호문'으로 쓰는 거라면, HMAC은 편지를 '투명한 유리'로 보내되 누가 보냈는지만 투명한 '보증 수표'를 붙이는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

오늘날 [[477_rest_api_architecture|REST API]] 통신이나 모바일 앱 백엔드에서 서버 간 권한 [[395_verification_process_review|검증]]을 할 때 HMAC은 가장 널리 쓰이는 표준이다.

### 실무 적용 사례 및 의사결정 포인트
1. **[[549_jwt_json_web_token|JSON Web Token]] ([[549_jwt_json_web_token|JWT]]) 서명**: 클라이언트가 서버에 로그인 상태를 증명할 때 쓰는 JWT의 마지막 `Signature` 부분이 주로 [[674_hmac_hash_based_mac_ipsec|HMAC]]-SHA256(HS256)으로 만들어진다. 서버의 비밀키가 털리지 않는 한 토큰 위조는 불가능하다.
2. **[[247_open_api_gateway_security_throttling_rate_limiting|Open API]] [[303_authentication_authorization_patterns|인증]] (AWS 서명 등)**: AWS나 결제 게이트웨이에 API를 호출할 때, 개발자는 발급받은 `Secret Key`를 이용해 요청 파라미터와 타임스탬프를 HMAC으로 말아서 보낸다. 서버는 비밀키를 통해 "이 요청이 우리 고객이 쏜 게 맞다"고 [[509_authorization_models_rbac_abac|인가]]([[509_authorization_models_rbac_abac|Authorization]])한다.
3. **보안 [[128_water_scrum_fall_anti_pattern|안티패턴]] 주의**: HMAC을 구현할 때 태그 비교 시 일치하는 바이트까지만 비교하고 틀리면 바로 리턴하는 방식은 '타이밍 공격(Timing Attack)'에 털린다. 반드시 모든 바이트를 끝까지 다 비교하는 `constant-time compare` 함수를 사용해야 한다.

- **📢 섹션 요약 비유**: HMAC은 클럽 입장 시 보여주는 야광 스탬프와 같다. 얼굴이나 이름을 가릴 필요는 없지만, 오직 클럽 가드(서버)만이 그날의 야광 잉크(비밀키)를 알고 있어 가짜 손님을 완벽하게 걸러낼 수 있다.

---

## Ⅴ. 기대효과 및 결론

HMAC은 공개키 기반의 [[675_digital_signature_process_asymmetric_key|전자서명]]([[110_rsa|RSA]] 등)에 비해 연산 속도가 압도적으로 빨라, [[101_iot_concept|IoT]] 기기나 초당 수만 건을 처리하는 [[014_api_posix|API]] 서버의 부하를 극적으로 줄이면서도 강력한 [[303_authentication_authorization_patterns|인증]]을 제공한다. 부인 방지(Non-repudiation) 기능이 없다는 것이 유일한 약점이지만, 통신 당사자끼리 서로를 전적으로 신뢰하는 폐쇄망이나 1:1 세션에서는 전혀 문제가 되지 않는다.

결론적으로 HMAC은 암호학의 가장 성공적인 융합 사례 중 하나다. 빠르고 가벼운 [[667_hash_function_integrity_one_way|해시 함수]]의 특성을 그대로 살리면서도, 수학적 약점을 구조적 이중 샌드위치 기법으로 보완하여 현대 네트워크 [[303_authentication_authorization_patterns|인증]]의 척추 역할을 훌륭히 수행하고 있다. 

- **📢 섹션 요약 비유**: 튼튼하지만 손잡이가 없어 [[289_cqrs_db|쓰기]] 불편했던 방패([[667_hash_function_integrity_one_way|해시 함수]])에, 나와 내 편만 잡을 수 있는 특수 손잡이(비밀키 구조)를 완벽하게 용접하여 세상에서 가장 가볍고 단단한 방어구를 만들어낸 것이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[667_hash_function_integrity_one_way|해시 함수]] ([[667_hash_function_integrity_one_way|Hash Function]])** | 임의의 길이를 고정 길이로 압축하여 [[003_integrity|무결성]]을 제공하는 HMAC의 핵심 엔진 (SHA-256 등) |
| **길이 연장 공격 (Length Extension Attack)** | 단순 `Hash(Key + Message)` 구조를 붕괴시키는 해킹 수법. HMAC이 이중 구조를 채택한 원인 |
| **[[549_jwt_json_web_token|JWT]] ([[549_jwt_json_web_token|JSON Web Token]])** | 웹과 모바일 환경에서 무상태([[239_stateless_redis|Stateless]]) [[303_authentication_authorization_patterns|인증]]을 구현할 때 HMAC을 서명 알고리즘으로 사용하는 대표적 기술 |
| **[[675_digital_signature_process_asymmetric_key|전자서명]] ([[675_digital_signature_process_asymmetric_key|Digital Signature]])** | HMAC과 목적은 같으나 비대칭키를 사용하여 송신자가 부인할 수 없는 증거(부인 방지)까지 제공하는 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
단방향 해시 함수 (SHA-1, SHA-2) · 무결성 제공, 위조에 무방비
    │
    ▼ (비밀키 결합 시도 및 취약점 발견)
단순 결합 MAC · `Hash(K||M)` 시도, 길이 연장 공격에 붕괴
    │
    ▼ (안전한 키 혼입 구조의 발명)
HMAC (Hash-based MAC) · XOR 패딩과 이중 해시 샌드위치 구조로 완벽 방어
    │
    ▼ (실무 플랫폼 적용)
JWT 서명 / AWS API 인증 · 현대 웹/클라우드 환경의 표준 인증 매커니즘으로 안착
```

이 흐름도는 단순한 [[001_dikw_pyramid|데이터]] [[395_verification_process_review|검증]] 기술이 해커의 공격을 방어하기 위해 수학적 구조를 고도화하고, 최종적으로 산업 표준 [[303_authentication_authorization_patterns|인증]] 기술로 자리 잡는 궤적을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구한테 보물지도([[001_dikw_pyramid|데이터]])를 보낼 때, 그냥 지문(해시)만 찍으면 나쁜 해적이 자기 지문을 덮어찍어 엉뚱한 지도로 바꿀 수 있어요.
2. HMAC은 지문을 찍을 때 우리 둘만 아는 '마법의 반짝이 가루(비밀키)'를 섞어서 두 번이나 덧칠해서 꾹 찍는 거랍니다.
3. 해적이 훔쳐서 새 지문을 찍어봐야 이 반짝이 가루를 몰라서, 친구는 "어? 반짝이가 없네? 이건 가짜 지도야!"라고 바로 알아채고 버릴 수 있어요.
