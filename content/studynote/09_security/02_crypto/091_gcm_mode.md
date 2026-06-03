+++
title = "091. GCM (Galois/Counter Mode) — AEAD, 인증 암호화"
date = 2026-04-05

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [GCM](/knowledge-base/studynote/03_network/13_network_security_basics/659_gcm_galois_counter_mode_aead/) (Galois/[Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) Mode)은 [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) 모드의 '[초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 암호화' 능력에, 갈루아 체(Galois Field) 수학을 이용한 '[초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)([GMAC](/knowledge-base/studynote/09_security/02_crypto/106_gmac/))'을 하나로 융합한 [AEAD](/knowledge-base/studynote/09_security/02_crypto/092_aead/) ([인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 암호화) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
> 2. **가치**: 데이터를 암호화([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 보장)하면서 동시에 변조 여부를 확인하는 태그([무결성 보장](/knowledge-base/studynote/05_database/07_exam_summary/442_consistency_integrity/))를 매우 가벼운 CPU 연산만으로 뽑아내어, 전력 소모와 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 시간을 획기적으로 줄였다.
> 3. **판단 포인트**: [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 보안이 완벽해 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 통신 등 현대 인터넷의 절대적 표준으로 쓰이지만, 초기화 벡터([Nonce](/knowledge-base/studynote/09_security/05_web_app_security/519_oidc_nonce/))를 단 한 번이라도 재사용할 경우 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)키가 털려 시스템 전체가 붕괴되는 치명적인 제약 조건을 갖는다.

---

## Ⅰ. 개요 및 필요성

네트워크 통신에서 데이터를 보호할 때 가장 중요한 두 축은 "아무도 못 보게 감추는 것([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/))"과 "중간에 내용이 바뀌지 않았음을 증명하는 것([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 및 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/))"이다. 
과거에는 블록 암호를 돌려 암호문을 만들고, 그 위에 SHA-256 같은 무거운 [해시 함수](/knowledge-base/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/)를 한 번 더 돌려 [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)(메시지 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 코드)을 붙이는 방식을 썼다. 이 방식은 보안성은 좋으나 암호화 엔진과 해시 엔진을 두 번 돌려야 하므로 처리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 서버 과부하를 유발했다.

특히 [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) ([Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)) 모드는 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리가 가능해 엄청난 속도를 자랑했지만, 해커가 암호문을 몰라도 특정 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 뒤집어 내용을 조작하는 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 플리핑(Bit-Flipping) 공격, 즉 연성(Malleability)의 취약점을 갖고 있었다. 이를 방어하면서도 CTR의 속도를 갉아먹지 않을 새로운 수학적 돌파구가 절실했고, 그 해답으로 등장한 것이 두 가지 연산을 한 큐에 끝내는 **[AEAD](/knowledge-base/studynote/09_security/02_crypto/092_aead/) (Authenticated Encryption with Associated [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))**의 최고봉, [GCM](/knowledge-base/studynote/03_network/13_network_security_basics/659_gcm_galois_counter_mode_aead/) 모드다.

- **📢 섹션 요약 비유**: 과거에는 금고([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/))를 잠근 다음, 밖에서 경비원([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 검사)을 따로 고용해 두 번 지켜야 해서 돈과 시간이 많이 들었다. GCM은 금고 문을 닫는 순간 지문 인식 봉인 테이프가 자동으로 철컥 붙는 일체형 최첨단 스마트 금고다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[GCM](/knowledge-base/studynote/03_network/13_network_security_basics/659_gcm_galois_counter_mode_aead/) 모드는 두 개의 강력한 엔진을 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 돌려 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 동시에 달성한다. 핵심은 암호문을 만들자마자 바로 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 태그 믹서기로 던져 넣는 파이프라인 구조에 있다.

| 핵심 엔진 | 역할 및 동작 원리 | 처리 특징 |
| :--- | :--- | :--- |
| **[기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 엔진 ([CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) 파트)** | [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)([Nonce](/knowledge-base/studynote/09_security/05_web_app_security/519_oidc_nonce/)+순서)를 AES로 암호화한 난수열과 평문을 XOR(배타적 논리합)하여 암호문을 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 앞 블록을 기다릴 필요 없는 완벽한 **[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리** |
| **[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 엔진 ([GMAC](/knowledge-base/studynote/09_security/02_crypto/106_gmac/) 파트)** | [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)된 암호문들을 $GF(2^{128})$ 이라는 갈루아 체(Galois Field) 교실로 가져와, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)용 서브키(H)와 누적 곱셈/덧셈 수행 | [해시 함수](/knowledge-base/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/) 대신 가벼운 **수학적 곱셈**으로 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 태그(Tag) 128비트를 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/)으로 추출 |

```text
┌──────────────────────────────────────────────────────────────┐
│           GCM (Galois/Counter Mode)의 쌍발 엔진 메커니즘          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ [ 1. CTR 암호화: 병렬로 쏜다 ]                                   │
│  평문 블록 1 ──(XOR)──▶ [ 암호문 1 ] ─────────┐                   │
│         (난수)                          │                   │
│  평문 블록 2 ──(XOR)──▶ [ 암호문 2 ] ─────────┤                   │
│         (난수)                          │                   │
│                                         ▼                   │
│ [ 2. GMAC 인증: 눈덩이처럼 굴린다 ]                               │
│  (AAD 평문) ──▶ (갈루아 곱셈 ✖) ──▶ (결과 누적)                    │
│   암호문 1 ──▶ (갈루아 곱셈 ✖) ──▶ (결과 누적)                     │
│   암호문 2 ──▶ (갈루아 곱셈 ✖) ──▶ (결과 누적) ──▶ [ 인증 태그 ]    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

다이어그램의 하단 [GMAC](/knowledge-base/studynote/09_security/02_crypto/106_gmac/) 파트가 혁신적인 이유는, 무거운 암호학적 해시를 버리고 CPU가 하드웨어 차원(예: 인텔 PCLMULQDQ [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/))에서 0.001초 만에 끝낼 수 있는 '유한체 곱셈'을 채택했기 때문이다. 최종적으로 수신자는 **`[ 암호문 + 인증 태그 ]`** 를 받아, 태그를 먼저 검증하여 단 1비트라도 깨졌다면 아예 암호문을 열어보지 않고 통신을 차단(Drop)해버린다.

- **📢 섹션 요약 비유**: 컨베이어 벨트에서 과자(평문)를 상자에 담는 속도([CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/))도 빠른데, 상자가 지나가는 즉시 기계가 특수 형광 스티커(갈루아 태그)를 1초 만에 찍어 출고시킨다. 배달원이 상자를 살짝만 긁어도 스티커 색이 변해서 불량임을 바로 알 수 있다.

---

## Ⅲ. 비교 및 연결

GCM은 암호화할 데이터뿐만 아니라, 통신 구조상 암호화하면 안 되지만 변조는 막아야 하는 데이터까지 한 번에 지켜내는 AAD 기능으로 차별화된다.

| 항목 | 일반 [CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) 모드 | [GCM](/knowledge-base/studynote/03_network/13_network_security_basics/659_gcm_galois_counter_mode_aead/) (Galois/[Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) Mode) |
| :--- | :--- | :--- |
| **제공 기능** | [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) (암호화) | [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) + [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) + [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) ([AEAD](/knowledge-base/studynote/09_security/02_crypto/092_aead/)) |
| **AAD 지원 여부** | 불가능 | **가능** (헤더 정보까지 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 태그 계산에 포함) |
| **[비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 플리핑 공격**| 매우 취약 (수신자 조작 인지 불가) | 완벽 방어 (조작 시 Tag 불일치로 폐기) |
| **계산 오버헤드** | 매우 낮음 | 낮음 (갈루아 곱셈의 하드웨어 가속 덕분) |

IP 패킷의 헤더나 목적지 주소는 라우터가 읽어야 하므로 평문이어야 한다. GCM은 이 **AAD (Additional Authenticated [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))**를 [GMAC](/knowledge-base/studynote/09_security/02_crypto/106_gmac/) 믹서기의 맨 앞단에 함께 집어넣는다. 따라서 해커가 IP 헤더를 변조하면 최종 산출물인 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 태그 값이 틀려지게 되어 완벽한 네트워크 캡슐 보호가 완성된다.

- **📢 섹션 요약 비유**: 편지 봉투(헤더, AAD)와 편지 내용(평문)이 있을 때, 편지 내용만 암호화하는 게 일반 모드라면, GCM은 내용물 암호화는 물론이고 봉투 겉면 글씨를 누가 몰래 고쳐 쓰면 봉투에서 사이렌이 울리도록 봉투와 내용물 전체에 마법(태그)을 거는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 보안을 모두 잡은 GCM은 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3, [IPsec](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 등 모든 최신 프로토콜의 사실상 표준(De facto standard)이다. 그러나 실무 적용 시 개발자의 사소한 실수가 파멸적인 결과를 초래한다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/) 및 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

1. **[Nonce](/knowledge-base/studynote/09_security/05_web_app_security/519_oidc_nonce/) (초기화 벡터) 절대 재사용 금지 (Never Reuse)**
   - **가장 치명적인 급소다.** 만약 똑같은 암호키 하에서 96비트 [Nonce](/knowledge-base/studynote/09_security/05_web_app_security/519_oidc_nonce/) 값을 한 번이라도 중복 사용하면, XOR 연산의 맹점으로 인해 평문이 유출될 뿐만 아니라, 갈루아 곱셈의 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 서브키(H)를 수학적으로 역산해 낼 수 있게 된다.
   - [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)키가 노출되면 해커는 마음대로 가짜 메시지에 완벽하게 들어맞는 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 태그(Tag)를 위조하여 서버를 유린할 수 있다.
2. **순차적 [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) 설계**
   - 개발 시 Nonce를 단순 난수(Random)로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하면 충돌(생일 역설) 위험이 있으므로, 하드웨어가 재부팅되어도 절대 겹치지 않는 순서 번호표(Sequence Number) 방식과 결합하여 철저히 통제해야 한다.

### 실무 판단 포인트

- **채택 시점**: [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 대용량 트래픽을 처리하는 동영상 스트리밍 서버, 금융권 통신 채널 등 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목을 최소화하면서도 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 필수적인 모든 모던 웹 아키텍처에 1순위로 채택해야 한다.

- **📢 섹션 요약 비유**: GCM은 최고의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 내는 포뮬러 원(F1) 레이싱카다. 하지만 "똑같은 출발 번호판([Nonce](/knowledge-base/studynote/09_security/05_web_app_security/519_oidc_nonce/))을 달고 두 번 출전하면 엔진이 폭발한다"는 절대적인 룰이 있다. 이 룰을 어기는 드라이버(개발자)는 경기장을 잿더미로 만든다.

---

## Ⅴ. 기대효과 및 결론

[GCM](/knowledge-base/studynote/03_network/13_network_security_basics/659_gcm_galois_counter_mode_aead/) (Galois/[Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) Mode)은 현대 암호학이 도달한 궁극의 융합 기술이다. 블록을 잘게 쪼개어 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)로 처리하는 혁신([CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/))과, 무거운 해시 대신 CPU 친화적인 유한체 수학(Galois Field)을 사용해 변조를 잡아내는 혁신이 결합되었다. 

이러한 혁신 덕분에 스마트폰의 배터리를 아끼면서도 구글, 넷플릭스 등 전 세계 막대한 트래픽의 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 없이 완벽하게 수호하고 있다. 결론적으로 GCM은 단순한 암호화 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 아니라, "가볍고 빠른 연산만으로도 완벽한 신뢰를 담보할 수 있다"는 [AEAD](/knowledge-base/studynote/09_security/02_crypto/092_aead/) 보안 패러다임의 가장 찬란한 승리다.

- **📢 섹션 요약 비유**: GCM은 눈보라 속에서도 길을 잃지 않는 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) KTX 열차다. 승객을 안전하게 감추고([기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)) 미친 듯이 달리면서도([CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/)), 선로에 돌멩이 하나만 누군가 올려두어도 즉시 감지해 멈추는([GMAC](/knowledge-base/studynote/09_security/02_crypto/106_gmac/)) 완벽한 센서까지 갖추고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[AEAD](/knowledge-base/studynote/09_security/02_crypto/092_aead/) (Authenticated Encryption with Associated [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))** | 암호화와 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)/[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 동시에 수행하며 공개된 헤더(AAD)까지 보호하는 암호 체계 |
| **[CTR](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/) 모드 ([Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) Mode)** | GCM의 뼈대가 되는 [스트림 암호](/knowledge-base/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/) 방식의 블록 운영 모드 ([초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 암호화 담당) |
| **[GMAC](/knowledge-base/studynote/09_security/02_crypto/106_gmac/) (Galois [Message Authentication Code](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))** | 갈루아 유한체 곱셈을 이용해 고속으로 메시지 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 태그를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| **[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 (Transport Layer [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))** | 웹 통신의 절대적 표준 규격으로, 기존 취약한 암호들을 폐기하고 [GCM](/knowledge-base/studynote/03_network/13_network_security_basics/659_gcm_galois_counter_mode_aead/) 등 안전한 AEAD만 허용함 |

### 📈 관련 키워드 및 발전 흐름도

```text
블록 암호 기본 모드 (ECB, CBC)의 한계와 성능 저하
    │
    ▼
카운터 도입 및 병렬 처리 혁신 (CTR 모드의 등장)
    │
    ▼
비트 플리핑(Bit-Flipping) 공격 등 연성 취약점 발견
    │
    ▼
암호화 + 해시 함수를 이중으로 돌리는 과부하 발생 (MAC-then-Encrypt 등)
    │
    ▼
수학적 곱셈(GMAC)과 CTR을 일체화시킨 GCM (AEAD 표준 완성)
```

이 흐름도는 단순 암호화의 속도 개선에서 시작해 변조 공격을 막기 위한 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 추가, 그리고 최종적으로 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하 없이 두 마리 토끼를 잡은 AEAD로의 진화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 암호화는 비밀일기장을 자물쇠로 잠그는 거예요. 그런데 나쁜 친구가 자물쇠를 못 열어도 일기장을 밖에서 발로 밟아 망가뜨릴 수 있었어요.
2. 그래서 GCM이라는 마법의 봉인 테이프를 일기장 겉에 촥! 붙였어요.
3. 이제 누가 일기장을 몰래 밟기만 해도 테이프 색깔이 시뻘겋게 변해서, 우리가 열어보기도 전에 "앗! 누가 건드렸구나!" 하고 바로 알아챌 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 91 / 1108

← **이전**: [090. CTR (Counter) — 난수 대신 카운터, 병렬 처리 가능](/knowledge-base/studynote/09_security/02_crypto/090_ctr_mode/)
**다음**: [092. AEAD (Authenticated Encryption with Associated Data) — 암호화+인증 동시](/knowledge-base/studynote/09_security/02_crypto/092_aead/) →

---
