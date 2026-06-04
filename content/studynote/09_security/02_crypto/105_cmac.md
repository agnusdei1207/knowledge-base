---
title: "105. CMAC (Cipher-based MAC) — 블록 암호 기반"
date: "2026-04-05"
tags:
  - "studynote-security"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CMAC (Cipher-based [Message Authentication Code](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))은 [해시 함수](/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/) 대신, 기존에 탑재된 대칭키 [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 등)을 [CBC](/studynote/09_security/02_crypto/089_cbc_mode/) 모드로 연쇄 동작시켜 메시지의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)과 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 확보하는 기술이다.
> 2. **가치**: 칩 면적과 메모리가 극도로 제한적인 [스마트 카드](/studynote/09_security/12_identity_threat_advanced/607_smart_card/)나 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 임베디드 기기에서, 별도의 무거운 [해시 함수](/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/) [모듈](/studynote/04_software_engineering/04_testing_quality/192_module_independence/)(SHA)을 추가하지 않고 기존 암호화 엔진 하나로 [기밀성](/studynote/09_security/01_intro_principles/002_confidentiality/)과 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 모두 해결하는 가성비를 제공한다.
> 3. **판단 포인트**: 구형 기술인 [CBC](/studynote/09_security/02_crypto/089_cbc_mode/)-MAC이 가변 길이 메시지에 대해 취약점(길이 확장 위조)을 보이자, 마지막 블록 처리 직전에 비밀 서브 키($K_1, K_2$)를 주입(XOR)하는 수학적 방어 기법을 추가하여 완성된 안전한 공식 표준이다.

---

## Ⅰ. 개요 및 필요성

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 통신 중 변조되지 않았음을 증명([무결성](/studynote/09_security/01_intro_principles/003_integrity/) 및 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))하려면 보통 원본 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 짧은 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 지문을 뽑아내는 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) ([Message Authentication Code](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))을 사용한다. 웹이나 대형 서버 환경에서는 SHA 같은 강력한 [해시 함수](/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/)를 사용하는 HMAC을 쓴다.

하지만 스마트 톨게이트 센서, 신용카드 IC칩 같은 초소형 임베디드 환경에서는 문제가 다르다. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 암호화하기 위해 이미 [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 같은 [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/) 칩을 공간을 쪼개어 넣어두었는데, [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 하겠다고 거대한 [해시 함수](/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/)(SHA) 코드를 추가로 밀어 넣으면 칩의 메모리가 초과되고 전력 소모가 극심해진다. 학자들은 "이미 깔려있는 [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 암호화 기계를 믹서기처럼 활용해서 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 지문을 만들어내자"는 아이디어를 냈고, 이것이 [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/) 기반의 CMAC이 탄생한 배경이다.

- **📢 섹션 요약 비유**: 작은 캠핑 텐트([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 기기) 안에서 요리할 때, 고기를 굽는 불판([AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 암호화기)과 라면을 끓이는 버너(SHA 해시)를 따로 챙기면 짐이 너무 무겁다. CMAC은 고기를 다 구운 뒤, 남은 불판의 열기를 그대로 활용해 라면까지 끓여버리는([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)까지 해결하는) 극강의 짐 줄이기 생존술이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CMAC의 동작 원리는 입력 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 블록 단위(예: 128비트)로 쪼갠 뒤, 앞 블록의 암호화 결과가 다음 블록의 평문과 XOR 되는 [CBC](/studynote/09_security/02_crypto/089_cbc_mode/) ([Cipher Block Chaining](/studynote/09_security/02_crypto/089_cbc_mode/)) 모드의 특성을 극단적으로 활용한다.

| 단계 | 처리 과정 (CMAC 메커니즘) | 목적 및 효과 |
| :--- | :--- | :--- |
| <strong>1. 키 <a href="/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong> | 메인 키($K$)에서 수학적 연산으로 서브 키 $K_1$, $K_2$ 도출 | 마지막 블록 락온(Lock-on)을 위한 비밀 무기 준비 |
| **2. 연쇄 암호화** | 첫 블록부터 (N-1)번째 블록까지 [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-[CBC](/studynote/09_security/02_crypto/089_cbc_mode/) 모드로 순차 암호화 | 앞선 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 모든 기운이 쇠사슬을 타고 응축됨 |
| **3. 서브 키 투하** | 마지막 블록 직전에 $K_1$([패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 없음) 또는 $K_2$([패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 있음)를 XOR | 구형 [CBC](/studynote/09_security/02_crypto/089_cbc_mode/)-MAC의 길이 확장 위조 공격을 원천 차단 |
| **4. 태그 추출** | 마지막 블록을 암호화하여 나온 찌꺼기를 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 태그(지문)로 사용 | 중간 암호문은 다 버리고 오직 마지막 1개만 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)에 사용 |

```text
+--------------------------------------------------------------+
|       CMAC의 아키텍처 (마지막 블록에 서브 키 K1 투하)        |
+--------------------------------------------------------------+
|  [평문 블록 1]      [평문 블록 2]       [마지막 평문 블록 N] |
|       |                  |                    |              |
|       v                  v                    v              |
|    ( AES ) --(XOR)---> ( AES ) --(XOR)--->   ( XOR ⊕ ) <--- ★ K1 (또는 K2) |
|                      (중간 찌꺼기 넘김)       |              |
|                                               v              |
|                                            ( AES )           |
|                                               |              |
|                                               v              |
|    (버림)             (버림)           [ CMAC 인증 태그 ]    |
+--------------------------------------------------------------+
```

여기서 중간에 나오는 암호문 블록들을 그냥 버리는 이유는 지금 우리의 목적이 '[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 기밀화(암호화)'가 아니라 '[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 깨짐 방지([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))'이기 때문이다. 모든 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 꼬리를 물고 넘어와 마지막 블록에 농축되므로, 이 마지막 블록 하나만 떼어내도 전체 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 단 1비트라도 조작되었는지 100% 감지해 낼 수 있다.

- **📢 섹션 요약 비유**: 100피스짜리 도미노를 세울 때, 99번째 도미노까지는 그냥 평범하게 세우다가 마지막 100번째 도미노를 놓기 직전에 나만 아는 '특수 강력 접착제(서브 키 K1)'를 발라버리는 것이다. 해커가 몰래 101번째 가짜 도미노를 덧붙이려 해도 접착제 성분이 달라서 위조가 감지된다.

---

## Ⅲ. 비교 및 연결

실무에서 개발자는 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 확보할 때 HMAC과 CMAC 사이에서 트레이드오프를 결정해야 한다.

| 비교 항목 | [HMAC](/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/) (Hash 기반 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)) | CMAC (Cipher 기반 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)) |
| :--- | :--- | :--- |
| **내부 핵심 엔진** | SHA-256, [SHA-3](/studynote/09_security/02_crypto/101_sha_3/) 등 [해시 함수](/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/) | [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/), [DES](/studynote/09_security/02_crypto/086_des_data_encryption_standard/) 등 대칭키 [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| <strong>처리 <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> (대용량)</strong> | 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에서 속도가 빠름 ([병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 해싱 유리) | 순차적으로 [CBC](/studynote/09_security/02_crypto/089_cbc_mode/) 블록을 기다려야 하므로 대용량에 불리함 |
| **메모리(코드) 효율** | 암호화 칩과 해시 칩을 모두 구현/탑재해야 함 | 기존 [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 암호화 칩 하나로 100% 재활용 (초경량) |
| **최적 적용 환경** | 고성능 CPU 서버, 웹 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([JWT](/studynote/03_network/10_application_layer_dns_mgmt/549_jwt_json_web_token/) 등), 클라우드 | [스마트 카드](/studynote/09_security/12_identity_threat_advanced/607_smart_card/), [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 칩, 무선 이어폰 등 초소형 임베디드 |
| **위조 방어 원리** | 2중 해싱 (Inner/Outer [패딩](/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 결합) | 서브 키 주입 (길이 위조 방어) |

CMAC 이전의 구형 [CBC](/studynote/09_security/02_crypto/089_cbc_mode/)-MAC은 메시지가 가변 길이일 때 해커가 정상 태그 뒤에 악성 블록을 붙여 서버를 속이는 '길이 확장 공격(Length Extension Attack)'에 속수무책으로 털렸다. CMAC은 OMAC1이라는 수학적 개선을 수용하여 이 약점을 서브 키 주입으로 완벽히 틀어막은 진화형이다.

- **📢 섹션 요약 비유**: HMAC은 거대한 공장에서 전문 믹서기(해시)를 윙윙 돌려 대량으로 쥬스를 짜내는 방식이고, CMAC은 손바닥만 한 자취방에서 칼([AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)) 하나만 가지고 과일도 깎고 마늘도 다지며 모든 요리를 콤팩트하게 끝내는 다용도 생존 기술이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

1. **설계 시 의사결정 (채택 포인트)**: 스마트 팩토리의 말단 센서, 차량용 통신([V2X](/studynote/06_ict_convergence/02_iot_mobility/141_v2x_vehicle_to_everything_communication/))의 초소형 제어기, 혹은 [ROM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/255_rom/) 용량이 몇 킬로바이트(KB)밖에 안 되는 하드웨어를 설계할 때 "[무결성 보장](/studynote/05_database/07_exam_summary/442_consistency_integrity/)" 요구사항이 들어오면 주저 없이 CMAC을 아키텍처에 박아 넣어야 한다.
2. **보안/운영 주의점**: CMAC은 결국 밑바탕에 AES를 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 때문에 대칭키 기반이다. 즉, 보내는 기기와 받는 서버가 동일한 비밀키($K$)를 안전하게 나눠 가져야 한다(키 분배 문제). 또한, [CBC](/studynote/09_security/02_crypto/089_cbc_mode/) 모드의 특성상 이전 블록이 다 계산되어야 다음 블록을 계산할 수 있어 하드웨어적인 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리(속도 향상)가 불가능하므로, 기가비트급 고속 네트워크 장비에는 부적합하다.

- **📢 섹션 요약 비유**: CMAC은 스위스 아미 나이프(맥가이버칼)다. 좁은 산속(초소형 칩)에서 캠핑할 때는 이것 하나로 다 되니까 최고지만, 대형 레스토랑 주방(대용량 클라우드 서버)에서 고기를 썰 때 맥가이버칼을 쓰면 셰프(CPU)가 속 터져서 쓰러진다. 환경에 맞춰 무기를 골라야 한다.

---

## Ⅴ. 기대효과 및 결론

CMAC은 자원이 극도로 제한된 환경에서도 [기밀성](/studynote/09_security/01_intro_principles/002_confidentiality/)(암호화)과 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))이라는 두 마리 토끼를 단일 엔진으로 잡아내는 효율성의 극치다. 소프트웨어 코드 크기와 하드웨어 게이트 수를 획기적으로 줄여주어 단가 절감이 생명인 대량 생산형 [사물인터넷](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)) 생태계의 보안 표준으로 자리 잡았다.

비록 대용량 [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리에 불리하다는 한계가 있지만, 그 역할(가벼운 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))에 충실한 설계 철학은 "새로운 무거운 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 도입하기보다 기존 자원의 재활용을 극대화한다"는 시스템 공학의 훌륭한 모범 답안으로 평가받는다.

- **📢 섹션 요약 비유**: CMAC은 엔진을 끄고 달릴 때 버려지는 자동차 바퀴의 회전력을 이용해 발전기를 돌려 전기를 만드는 하이브리드 자동차의 회생 제동과 같다. 추가 연료(별도 해시 칩) 없이 기존의 움직임([AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 암호화)만으로 귀중한 에너지([인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 지문) 파워를 얻는 똑똑한 설계다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/studynote/09_security/02_crypto/089_cbc_mode/">CBC</a> 모드 (<a href="/studynote/09_security/02_crypto/089_cbc_mode/">Cipher Block Chaining</a>)</strong> | CMAC이 평문을 엮어내는 기반이 되는 [블록 암호](/studynote/03_network/13_network_security_basics/655_block_cipher_des_3des_feistel/) 운영 모드 (앞 블록이 뒤에 영향을 줌) |
| <strong><a href="/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/">HMAC</a> (<a href="/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/">Hash-based MAC</a>)</strong> | [해시 함수](/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/)를 엔진으로 사용하는 대형/고속 시스템용 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 표준 경쟁자 |
| <strong><a href="/studynote/03_network/13_network_security_basics/653_symmetric_key_cryptography_fast_speed/">대칭키 암호화</a> (<a href="/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/">AES</a>/<a href="/studynote/09_security/02_crypto/086_des_data_encryption_standard/">DES</a>)</strong> | CMAC이 내부적으로 동작시키기 위해 반드시 필요한 기반 암호화 기계 |
| <strong><a href="/studynote/02_operating_system/10_security/668_side_channel_attack_meltdown_spectre_kpti/">부채널 공격</a> (<a href="/studynote/01_computer_architecture/14_hardware_security_trends/481_side_channel_attack/">Side-channel Attack</a>)</strong> | [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 기기가 CMAC을 계산할 때 발생하는 전력/전자파를 분석해 서브 키를 탈취하려는 물리적 해킹 |

### 📈 관련 키워드 및 발전 흐름도

```text
메시지 인증 코드 (MAC) 도입 · 무결성과 발신자 신원 확인
    |
    v
CBC-MAC · 블록 암호를 활용한 가벼운 인증 도입 (단, 고정 길이 메시지만 안전)
    |
    v
길이 확장 위조 공격 (Length Extension Attack) 발생 · 가변 길이 메시지에서 털림
    |
    v
OMAC (One-Key MAC) 및 서브 키 주입 고안 · 위조 방어 수학적 기법 추가
    |
    v
CMAC (Cipher-based MAC) 표준화 · IoT 및 임베디드 기기의 최적량 인증 표준 정립
```

### 👶 어린이를 위한 3줄 비유 설명

1. 편지가 중간에 가짜로 바뀌지 않았는지 도장을 찍으려면 크고 무거운 '도장 기계(해시)'가 필요해요.
2. 하지만 작은 장난감 로봇 안에는 글자를 숨기는 작은 '비밀 상자([AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 암호)'밖에 넣을 공간이 없었죠.
3. CMAC은 똑똑하게도 이 비밀 상자에 편지를 끝까지 밀어 넣고 남은 작은 찌꺼기 하나에만 마법의 풀(서브 키)을 발라서 훌륭한 도장으로 써먹는 발명품이랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 158 / 1108

<- **이전**: [104. NMAC (Nested MAC)](/studynote/09_security/02_crypto/104_nmac/)
**다음**: [106. GMAC (Galois MAC) — GCM의 인증 부분](/studynote/09_security/02_crypto/106_gmac/) ->

---
