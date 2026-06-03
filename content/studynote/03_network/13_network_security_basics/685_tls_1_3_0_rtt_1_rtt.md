+++
title = "685. TLS 1.3 업그레이드 변화와 0-RTT/1-RTT 성능 향상 차이"
date = 2026-05-08

[taxonomies]
tags = ["studynote-network"]

[extra]
tags = ["studynote-network"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…는 [네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 기본에서 핵심 동작과 제약을 이해하게 해 주는 개념이다.
> 2. **가치**: [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…를 이해하면 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 사이의 균형을 더 정확히 볼 수 있다.
> 3. **판단 포인트**: 설계 시에는 개념 자체보다 적용 조건, 운영 복잡도, 인접 기술과의 경계를 함께 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

2008년에 나온 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.2는 10년 동안 너무 낡았습니다. 불필요하고 낡은 암호화 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 덕지덕지 붙어있어 해킹 공격(DOWNGRADE, [POODLE](/knowledge-base/studynote/09_security/03_network_security/294_poodle/) 공격 등)의 타겟이 되었고, 스마트폰 [5G](/knowledge-base/studynote/07_enterprise_systems/09_digital_transformation/418_5g_embb_urllc_mmtc_slicing/) 시대에 맞지 않게 연결 속도([지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/))가 너무 느렸습니다. 이에 IETF는 2018년, 뼈대를 완전히 갈아엎은 **[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 (RFC 8446)**을 발표했습니다.

```text
[TLS 전방향 안전성 보장 원리]
    │
    ▼
[TLS 1.3 업그레이드 변화와 0-RTT/…]
    │
    └──▶ [MAC-then-Encrypt 패러다임 /…]
```

- **📢 섹션 요약 비유**: [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…는 왜 필요한지 보여주는 교통 규칙 표지판과 같다. 문제가 생긴 배경을 알면 이후 [선택도](/knowledge-base/studynote/05_database/03_relational_model/170_selectivity_cardinality_distribution_tuning/) 쉬워진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

해커들이 뚫고 들어올 만한 뒷문(낡은 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))을 자비 없이 모조리 삭제했습니다.
- **PFS(전방향 안전성) 강제**: 684번 문서에서 배운 대로, 마스터키가 털려도 안전한 임시 키 교환 방식([DHE](/knowledge-base/studynote/09_security/03_network_security/129_dhe_ephemeral_dh/), [ECDHE](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/))만 남기고, 위험한 고정 [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) 키 교환 방식은 아예 퇴출했습니다.
- **[AEAD](/knowledge-base/studynote/09_security/02_crypto/092_aead/) 강제**: [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 동시에 해치우는 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) [GCM](/knowledge-base/studynote/03_network/13_network_security_basics/659_gcm_galois_counter_mode_aead/), ChaCha20-Poly1305 모드만 남기고, 낡은 [CBC](/knowledge-base/studynote/09_security/02_crypto/089_cbc_mode/) 모드, [RC4](/knowledge-base/studynote/09_security/02_crypto/081_rc4_stream_cipher/) [스트림 암호](/knowledge-base/studynote/03_network/13_network_security_basics/654_stream_cipher_rc4_chacha20/), [MD5](/knowledge-base/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/), SHA-1 해시 함수는 100% 삭제해 버렸습니다.

```text
[TLS 전방향 안전성 보장 원리]
    │
    ▼
[TLS 1.3 업그레이드 변화와 0-RTT/…]
    │
    └──▶ [MAC-then-Encrypt 패러다임 /…]
```

- **📢 섹션 요약 비유**: [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…의 내부 원리는 기계의 톱니바퀴처럼 맞물려 돌아간다. 한 부분이 어긋나면 전체 효과가 떨어진다.

---

## Ⅲ. 비교 및 연결

[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3이 현존 최고의 프로토콜이 된 이유입니다. 왕복 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)([Round Trip Time](/knowledge-base/studynote/03_network/08_transport_layer/441_rtt_round_trip_time_srtt_smoothed/))을 극단적으로 줄였습니다.

### 1. 1-RTT (처음 방문하는 사이트 접속 시)
- **기존 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.2 (2-RTT)**: 클라이언트가 인사(1번) ➜ 서버가 인사 및 신분증 제시(2번) ➜ 클라이언트가 암호키 전달(3번) ➜ 서버가 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)(4번). [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 받기 전까지 무려 2번을 왕복해야 했습니다.
- **[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 (1-RTT)**: **"어차피 요즘 다 [ECDHE](/knowledge-base/studynote/09_security/03_network_security/131_ecdhe_ephemeral_ecdh/) 키 교환 쓰는 거 아니까, 첫 인사([Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) Hello) 할 때 암호키 만들 재료도 아예 같이 몽땅 싸서 한 방에 던질게!"**
- 클라이언트가 첫 패킷에 필요한 걸 다 담아 쏘면, 서버도 즉시 세션키를 뚝딱 만들어서 바로 "오케이, 이제 암호화 통신 시작!" 하며 응답합니다. 딱 **한 번의 왕복(1-RTT)**만으로 0.1초 만에 보안 터널이 뚫립니다.

### 2. 0-RTT (어제 갔던 사이트에 다시 접속 시) 🌟
- **개념**: 어제 접속했던 네이버(재방문)에 다시 접속할 때, 브라우저가 어제 발급받아 쟁여둔 '임시 티켓([PSK](/knowledge-base/studynote/09_security/03_network_security/142_psk_pre_shared_key/))'을 기억해 냅니다.
- **동작**: "어제 썼던 그 티켓으로 암호화할게!"라며, **아예 인사조차 생략하고 첫 번째 패킷([Client](/knowledge-base/studynote/11_design_supervision/01_audit_framework/003_audit_stakeholders/) Hello)에다가 바로 네이버 검색어 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) Payload)를 암호화해서 함께 쑤셔 넣어 쏴버립니다.**
- **효과**: 왕복 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 제로(0-RTT). 일반 [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 평문 접속과 완전히 똑같은 속도로 미친 듯이 렌더링 화면이 뜹니다.
- (※ 단, 0-RTT 패킷을 훔친 해커가 다시 쏘는 [재생 공격](/knowledge-base/studynote/03_network/14_network_security_threats/708_replay_attack_timestamp_nonce/)([Replay Attack](/knowledge-base/studynote/09_security/03_network_security/274_replay_attack/))의 위험이 있어, 은행 계좌 이체 등 치명적인 요청에는 쓰지 않고 단순 웹페이지 조회용으로만 허용합니다.)

[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…를 볼 때는 앞뒤 개념과의 경계를 함께 봐야 전체 흐름이 선명해진다. [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 전방향 안전성 보장 원리가 기반 조건을 만든다면, [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…는 그 위에서 핵심 메커니즘을 구현하고, MAC-then-Encrypt 패러다임 /…는 이를 더 확장된 적용 단계로 연결한다. 따라서 단일 정의보다 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)에 어떤 차이를 만드는지 비교하는 것이 중요하다.

| 관점 | 선행 개념 | 현재 개념 | 확장 개념 |
|:---|:---|:---|:---|
| 초점 | [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 전방향 안전성 보장 원리의 기반 정리 | [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…의 핵심 동작 | MAC-then-Encrypt 패러다임 /…의 확장 적용 |
| 자원 관점 | 기본 조건 확보 | [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 최적화 | 규모와 범위 확대 |
| 판단 포인트 | 도입 가능성 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 현재 메커니즘의 적합성 판단 | 운영·확장 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 연결 |

- **📢 섹션 요약 비유**: [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.2가 택배([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))를 시킬 때 "사장님 계세요? -> 네 -> 무슨 박스 쓰실래요? -> 우체국 5호 박스요 -> 자물쇠 비밀번호는 이걸로 하죠 -> 네 알겠습니다"라고 4번의 편지를 주고받아야(2-RTT) 비로소 택배가 출발하는 피곤한 방식이었다면, [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3(1-RTT)은 "사장님 5호 박스에 비밀번호 1234로 지금 당장 시작합시다!"라고 1번 만에 끝냅니다. 더 놀라운 0-RTT는 어제 샀던 단골집에 말도 안 걸고 "어제 그 비밀번호로 치킨 1마리 바로 쏴주세요!"라고 돈과 주문을 첫 마디에 바로 찔러넣는 궁극의 단골 패스(Fast-pass) 기술입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…를 단독 개념으로 외우기보다 어떤 병목을 줄이기 위한 선택인지 먼저 따져야 한다. 특히 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 전방향 안전성 보장 원리 수준의 기본 대책으로 충분한지, 아니면 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…가 제공하는 메커니즘이 실제로 필요한지 구분해야 한다. 이후 확장 단계에서는 MAC-then-Encrypt 패러다임 /…와 같은 후속 기술, 자동화 체계, 표준 호환성까지 함께 검토해야 한다.

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 현재 문제의 핵심이 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 부족인지, [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 악화인지 먼저 분리한다.
2. [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…가 추가하는 복잡도와 운영 이득이 균형을 이루는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.
3. 도입 후에는 인접 기술인 MAC-then-Encrypt 패러다임 /…와의 연계 방식을 함께 검증한다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…의 장점만 보고 트래픽 패턴이나 운영 비용을 무시한 채 과도 도입하는 설계
- [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 전방향 안전성 보장 원리와의 경계를 정리하지 않아 중복 투자나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 충돌을 만드는 설계

- **📢 섹션 요약 비유**: [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…를 실제로 쓰는 판단은 도구 상자를 고르는 일과 비슷하다. 좋아 보이는 도구보다 지금 문제에 맞는 도구가 중요하다.

---

## Ⅴ. 기대효과 및 결론

[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…는 [네트워크 보안](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) 기본을 이해할 때 핵심 축을 잡아 주는 개념이다. 올바르게 적용하면 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 개선과 구조적 단순화에 기여하지만, 조건을 잘못 잡으면 오히려 복잡도와 운영 부담이 커질 수 있다. 앞으로는 MAC-then-Encrypt 패러다임 /…, 자동화된 신뢰 체계, 자동화 운영과의 결합을 통해 더 정교하게 발전할 가능성이 크다. 따라서 이 개념은 정의 자체보다 “언제 쓰고 언제 다른 방법으로 넘길 것인가”의 관점으로 기억하는 것이 좋다. 향후에는 자동화된 신뢰 체계 같은 자동화 흐름과 결합되어 더 정교한 형태로 확장될 가능성이 크다.

- **📢 섹션 요약 비유**: [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…는 큰 흐름 속에서 기억해야 오래 남는다. 지금의 장점과 다음 확장 방향을 같이 보면 전체 그림이 선명해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 전방향 안전성 보장 원리 | 현재 개념이 등장하기 전에 갖춰야 할 배경이나 인접 선행 개념이다. |
| [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) ([Authentication](/knowledge-base/studynote/02_operating_system/10_security/604_authentication_factors/)) | 통신 상대가 진짜인지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다. |
| 암호화 (Encryption) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽지 못하게 보호한다. |
| MAC-then-Encrypt 패러다임 /… | 현재 개념이 확장되거나 적용 단계로 이어질 때 자주 함께 언급된다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[선행 개념: TLS 전방향 안전성 보장 원리]
    │
    ▼
[현재 개념: TLS 1.3 업그레이드 변화와 0-RTT/…]
    │
    ├──▶ [확장 A: MAC-then-Encrypt 패러다임 /…]
    └──▶ [확장 B: 자동화된 신뢰 체계]
```

[TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 1.3 업그레이드 변화와 0-RTT/…는 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 전방향 안전성 보장 원리에서 출발해 현재 메커니즘을 정교화하고, 이후 MAC-then-Encrypt 패러다임 /…와 자동화된 신뢰 체계 같은 확장 흐름으로 이어진다고 보면 기억이 오래간다.

### 👶 어린이를 위한 3줄 비유 설명

1. 비밀 편지를 보낼 때는 자물쇠와 비밀번호가 필요해요.
2. 이 개념은 누가 진짜 친구인지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, 편지가 바뀌지 않았는지도 살펴봐요.
3. 그래서 나쁜 사람이 중간에 훔쳐보거나 바꾸기 어려워져요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 806 / 1120

← **이전**: [684. TLS 전방향 안전성 (PFS, Perfect Forward Secrecy) 보장 원리 (RSA 직접 복호 문제 해결/임시 세션키)](/knowledge-base/studynote/03_network/13_network_security_basics/684_tls_pfs_perfect_forward_secrecy/)
**다음**: [686. MAC-then-Encrypt 패러다임 / AEAD 전환 보안 구조](/knowledge-base/studynote/03_network/13_network_security_basics/686_mac_then_encrypt_vs_aead/) →

---
