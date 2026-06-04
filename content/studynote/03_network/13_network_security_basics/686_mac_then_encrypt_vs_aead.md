+++
title = "686. MAC-then-Encrypt 패러다임 / AEAD 전환 보안 구조"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 패러다임 /…는 [네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 기본에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 패러다임 /…를 이해하면 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

[네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/)([TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/), [IPsec](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/589_ipsec_offload/) 등)에서 원본 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(평문)에 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)(암호)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 도장)을 적용하는 순서는 역사적으로 3가지가 있었습니다.

1. <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a>-and-Encrypt</strong>: 원본 편지에 도장([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))을 쾅 찍어 따로 두고, 원본 편지를 암호화한 뒤 두 개를 나란히 묶어서 보냅니다. ([보안성](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) 취약, [SSH](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/538_ssh_vs_telnet_secure_remote/) [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 모델)
2. <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a>-then-Encrypt (MtE) 🌟</strong>: 원본 편지 뒤에 도장([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))을 찰싹 붙인 다음, <strong>[편지+도장] 전체를 커다란 암호화 자물쇠(<a href="/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/">AES</a>-CBC 등)로 통째로 잠가서 보냅니다.</strong> (과거 SSL/[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.2까지의 기본 표준 방식이었습니다.)
3. <strong>Encrypt-then-<a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a> (EtM)</strong>: 원본 편지부터 먼저 꽁꽁 암호화(잠그기)를 한 다음, <strong>그 겉면 암호문 껍데기 위에다가 도장(<a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a>)을 쾅 찍어 보냅니다.</strong> (IPsec에서 쓰는 가장 안전한 방식입니다.)

```text
[TLS 1.3 업그레이드 변화와 0-RTT/…]
    |
    v
[MAC-then-Encrypt 패러다임 /…]
    |
    +---> [세션 재개 기능 구성]
```

- **📢 섹션 요약 비유**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 패러다임 /…는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 통신에서 10년 넘게 써오던 MtE 방식이 해커들에게 와르르 무너졌습니다. 그 이유는 <strong>'<a href="/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/">패딩</a>(<a href="/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/">Padding</a>)'</strong> 때문이었습니다.
- **약점 원리**: [AES](/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 블록 암호는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 16바이트 단위로 딱딱 맞게 잘라야 하므로, 끄트머리에 빈자리가 생기면 쓰레기 값([Padding](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/))을 채워 넣습니다. [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 방식은 [편지+도장]을 먼저 묶고 [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)을 채운 뒤 암호화를 합니다.
- <strong>해커의 꼼수 (<a href="/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/">Padding</a> <a href="/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/">Oracle</a> Attack)</strong>: 해커가 암호문 끄트머리 비트를 살짝 조작해서 서버로 툭툭 던져봅니다. 서버가 에러 메시지를 뱉을 때 "[패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)이 깨졌네!" 에러와 "도장([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/))이 틀렸네!" 에러를 다르게 뱉어주는 것을(오라클) 악용하여, 수천 번 찔러보며 수학적 역산을 통해 암호문을 통째로 해독(평문 추출)해 버리는 대재앙([POODLE](/knowledge-base/studynote/09_security/03_network_security/294_poodle/), [BEAST](/knowledge-base/studynote/09_security/03_network_security/295_beast/) 공격 등)이 터졌습니다.

```text
[TLS 1.3 업그레이드 변화와 0-RTT/…]
    |
    v
[MAC-then-Encrypt 패러다임 /…]
    |
    +---> [세션 재개 기능 구성]
```

- **📢 섹션 요약 비유**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 패러다임 /…의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

도장을 먼저 찍네 마네, [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)을 어디 채우네 하는 구조적 [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 때문에 털리는 것을 본 암호학자들은 결단을 내립니다.
- **해결책**: "아예 암호화와 도장([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)) 찍는 과정을 분리하지 말고, <strong>하나의 거대한 수학 공식(블랙박스) 안에 집어넣어 단 한 번의 연산으로 <a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">암호화 + [무결성</a> 도장]을 동시에 완벽하게 찍어내는 <a href="/knowledge-base/studynote/09_security/02_crypto/092_aead/">AEAD</a>(<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>된 암호화)</strong> 구조로 완전히 갈아타자!"
- **AEAD의 위력**: 659번 문서에서 배운 <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/659_gcm_galois_counter_mode_aead/">GCM</a>(Galois/<a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/">Counter</a> Mode)</strong>이나 <strong>ChaCha20-Poly1305</strong>가 바로 이 AEAD의 대표 주자입니다.
  - [패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/) 오라클 공격이 물리적으로 불가능해집니다.
  - 두 번 돌리던 연산을 한 번에 끝내므로 속도(CPU 효율)가 미친 듯이 빨라집니다.

[MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 패러다임 /…를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…가 기반 조건을 만든다면, [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 패러다임 /…는 그 위에서 핵심 메커니즘을 구현하고, [세션 재개](/knowledge-base/studynote/03_network/13_network_security_basics/687_tls_session_resumption_ticket/) 기능 구성은 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…의 기반 정리 | [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 패러다임 /…의 핵심 동작 | [세션 재개](/knowledge-base/studynote/03_network/13_network_security_basics/687_tls_session_resumption_ticket/) 기능 구성의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 패러다임 /…는 비슷한 기술들 사이의 차선을 구분하는 분기점과 같다. 어디서 갈라지는지 알아야 헷갈리지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

최신 웹 브라우저 통신 표준인 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3은, 해킹당할 여지가 있는 과거의 구질구질한 <strong><a href="/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/">MAC</a>-then-Encrypt 조합(예: <a href="/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/">AES</a>-CBC + <a href="/knowledge-base/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/">HMAC</a>) 방식을 법으로 완전히 폐지(삭제)</strong>해 버렸습니다. 현재 인터넷은 오직 무결점이 입증된 <strong><a href="/knowledge-base/studynote/09_security/02_crypto/092_aead/">AEAD</a> 구조의 암호 알고리즘만 쓰도록 강제</strong>되어 있습니다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 요구사항과 병목 지점을 먼저 수치화한다.
2. 운영 복잡도와 도입 효과를 함께 검증한다.
3. 인접 기술과의 연계를 배포 전에 점검한다.

- **📢 섹션 요약 비유**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt는 편지지에 도장을 찍고([MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)), 빈 공간에 신문지를 구겨 넣어([패딩](/knowledge-base/studynote/10_ai/01_ai_basics/098_padding_convolutional_neural_network_same_valid/)) 금고에 잠그는 방식입니다. 해커가 금고를 살짝 흔들어 신문지 부스럭거리는 소리(오라클 에러)를 힌트로 금고 번호를 맞춰버렸습니다. 빡친 보안 업계는 이 허술한 방식을 다 갖다 버리고, 아예 편지지를 집어넣자마자 기계가 알아서 내용물을 완벽히 숨김과 동시에 절대 변조 불가능한 특수 홀로그램 코팅을 한 방에 입혀 뱉어내는 최첨단 일체형 기계([AEAD](/knowledge-base/studynote/09_security/02_crypto/092_aead/), [GCM](/knowledge-base/studynote/03_network/13_network_security_basics/659_gcm_galois_counter_mode_aead/))로 시스템을 100% 전면 교체했습니다.

---

## Ⅴ. 기대효과 및 결론

[MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 패러다임 /…는 [네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 기본을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 [세션 재개](/knowledge-base/studynote/03_network/13_network_security_basics/687_tls_session_resumption_ticket/) 기능 구성, 자동화된 신뢰 체계, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 자동화된 신뢰 체계 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 패러다임 /…는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/… | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) ([Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/)) | 통신 상대가 진짜인지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다. |
| 암호화 (Encryption) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽지 못하게 보호한다. |
| [세션 재개](/knowledge-base/studynote/03_network/13_network_security_basics/687_tls_session_resumption_ticket/) 기능 구성 | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: TLS 1.3 업그레이드 변화와 0-RTT/…]
    |
    v
[현재 개념: MAC-then-Encrypt 패러다임 /…]
    |
    +---> [확장 A: 세션 재개 기능 구성]
    +---> [확장 B: 자동화된 신뢰 체계]
```

[MAC](/knowledge-base/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/)-then-Encrypt 패러다임 /…는 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…에서 출발해 현재 메커니즘을 정교화하고, 이후 [세션 재개](/knowledge-base/studynote/03_network/13_network_security_basics/687_tls_session_resumption_ticket/) 기능 구성와 자동화된 신뢰 체계 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 비밀 편지를 보낼 때는 자물쇠와 비밀번호가 필요해요.
2. 이 개념은 누가 진짜 친구인지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, 편지가 바뀌지 않았는지도 살펴봐요.
3. 그래서 나쁜 사람이 중간에 훔쳐보거나 바꾸기 어려워져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 807 / 1120

<- **이전**: [685. TLS 1.3 업그레이드 변화와 0-RTT/1-RTT 성능 향상 차이](/knowledge-base/studynote/03_network/13_network_security_basics/685_tls_1_3_0_rtt_1_rtt/)
**다음**: [687. 세션 재개 (Session Resumption / TLS Ticket) 기능 구성](/knowledge-base/studynote/03_network/13_network_security_basics/687_tls_session_resumption_ticket/) ->

---
