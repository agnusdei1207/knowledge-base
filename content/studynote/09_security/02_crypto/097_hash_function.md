---
title: 097. 해시 함수 — 단방향성, 충돌 저항성, Preimage 저항성
date: '2026-04-05'
tags:
- studynote-security
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[667_hash_function_integrity_one_way|해시 함수]] ([[667_hash_function_integrity_one_way|Hash Function]])는 [[501_file_definition_logical_record|파일]] 크기에 상관없이 임의의 길이의 [[001_dikw_pyramid|데이터]]를 입력받아, 고정된 길이(예: 256비트)의 무작위 문자열인 '디지털 지문(Digest)'을 뱉어내는 [[008_단방향_반이중_전이중|단방향]] 수학 함수다.
> 2. **가치**: 입력값이 단 1비트만 달라져도 완전히 다른 해시값이 튀어나오는 눈사태 효과 (Avalanche Effect)를 통해 [[001_dikw_pyramid|데이터]]가 전송 중에 변조되지 않았음([[003_integrity|무결성]])을 완벽하게 증명한다.
> 3. **판단 포인트**: [[667_hash_function_integrity_one_way|해시 함수]] 자체는 기밀성을 보장하는 암호화가 아니며, 패스워드 저장이나 [[675_digital_signature_process_asymmetric_key|전자서명]] 시 발생할 수 있는 해킹 공격(레인보우 테이블)을 막기 위해 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]]) 및 [[109_key_stretching|키 스트레칭]] 기법과 반드시 병행해야 한다.

---

## Ⅰ. 개요 및 필요성

네트워크를 통해 10GB짜리 중요 [[555_backup_and_restore_strategy|백업]] [[501_file_definition_logical_record|파일]]을 전송받았을 때, 이 [[501_file_definition_logical_record|파일]]이 전송 과정에서 1비트라도 깨지진 않았는지, 혹은 해커가 몰래 악성코드를 심어두진 않았는지 어떻게 확신할 수 있을까? 10GB 사본을 원본과 1비트씩 통째로 대조하는 것은 물리적으로 불가능에 가깝다.

이때 필요한 기술이 [[001_dikw_pyramid|데이터]]의 **'고유한 지문(Fingerprint)'**을 추출하는 [[667_hash_function_integrity_one_way|해시 함수]]다. [[667_hash_function_integrity_one_way|해시 함수]]를 통과시키면 거대한 [[501_file_definition_logical_record|파일]]도 고작 256비트 크기의 짧은 고유 값(해시값)으로 압축된다. 수신자는 [[501_file_definition_logical_record|파일]] 전체를 비교할 필요 없이, 전송받은 [[501_file_definition_logical_record|파일]]의 해시값을 직접 돌려본 뒤 송신자가 알려준 원본 해시값과 일치하는지만 확인하면 [[501_file_definition_logical_record|파일]]의 [[003_integrity|무결성]]([[003_integrity|Integrity]])을 100% 확신할 수 있다.

- **📢 섹션 요약 비유**: [[667_hash_function_integrity_one_way|해시 함수]]는 거대한 돼지 한 마리를 통째로 갈아서 고정된 길이의 소시지 하나를 만드는 마법의 고기 분쇄기다. 소시지 맛만 보면 원래 돼지가 건강했는지 알 수 있고, 원래 고기에 소금 1톨만 더 들어가도 소시지 맛이 완전히 달라진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

일반적인 [[112_checksum|체크섬]]([[112_checksum|Checksum]])용 함수와 달리, '암호학적 (Cryptographic)' [[667_hash_function_integrity_one_way|해시 함수]]로 인정받으려면 해커의 공격을 버티는 3가지 강력한 수학적 저항성 ([[003_resistance|Resistance]])을 반드시 갖춰야 한다.

| 저항성 요건 | 개념 (수학적 정의) | 방어하는 해커의 공격 시나리오 |
| :--- | :--- | :--- |
| **제1역상 저항성 ([[008_단방향_반이중_전이중|단방향]]성)** | $y=H(x)$ 에서 결과값 $y$를 알 때 원본 $x$를 구하기 불가능할 것 | 유출된 비밀번호 해시값을 보고 원래 비밀번호 평문을 역추적하려는 공격 |
| **제2역상 저항성 (약한 충돌 저항성)** | $x$와 $H(x)$를 알 때 $H(x) = H(x')$인 가짜 [[001_dikw_pyramid|데이터]] $x'$ 찾기 불가 | 정상 계약서를 해시값이 같은 위조 계약서(금액 변경)로 바꿔치기하려는 공격 |
| **충돌 저항성 (강한 충돌 저항성)** | $H(x_1) = H(x_2)$가 되는 무작위의 두 [[001_dikw_pyramid|데이터]] $(x_1, x_2)$ 쌍을 찾기 불가 | 백신 검증을 우회하기 위해 정상 [[501_file_definition_logical_record|파일]]과 해시값이 똑같은 악성코드를 미리 준비하는 공격 |

```text
┌──────────────────────────────────────────────────────────────┐
│           해시 함수의 단방향성과 눈사태 효과 시각화          │
├──────────────────────────────────────────────────────────────┤
│ [ 원본 데이터 입력 ]                 [ 해시 함수 (SHA-256) ]   │
│   "Hello World"    ───────(믹서기 윙윙)──────▶   3A8B...9F2C   │
│                                                              │
│ [ 1비트 변조 데이터 입력 ]                                     │
│   "Hello World."   ───────(믹서기 윙윙)──────▶   Z9!P...1Q8@   │
│    (마침표 추가)                           (결과가 완벽히 달라짐)│
│                                                              │
│ [ 역산 시도 (해커) ]                                           │
│   3A8B...9F2C      ───────(거꾸로 돌려!)─────▶   🚨 역산 절대 불가 │
└──────────────────────────────────────────────────────────────┘
```

단 1비트의 변화에도 결과물이 단 한 글자도 겹치지 않고 완전히 다른 쓰레기 값이 튀어나온다. 이를 통해 눈사태 효과 (Avalanche Effect)를 달성한다.

- **📢 섹션 요약 비유**: 사과를 갈면 무조건 사과 주스가 나오지만(결정성), 사과 주스를 아무리 뭉쳐도 원래의 사과 모양으로 되돌려 놓을 수는 없는([[008_단방향_반이중_전이중|단방향]]성) 절대 깨지지 않는 요술 믹서기다.

---

## Ⅲ. 비교 및 연결

[[667_hash_function_integrity_one_way|해시 함수]]는 [[365_tde|데이터베이스 암호화]], [[988_digital_signature|전자 서명]], [[004_blockchain|블록체인]] 등 전방위적으로 사용되며 [[001_algorithm_definition|알고리즘]]은 끊임없이 진화해 왔다. 해커들이 컴퓨터 속도를 높여 '생일 공격 (Birthday Attack)' 등으로 충돌을 찾아내면 그 [[667_hash_function_integrity_one_way|해시 함수]]는 사망 선고를 받는다.

| [[001_algorithm_definition|알고리즘]] 구분 | [[073_bit|비트]] 길이 | [[178_as_is_to_be_analysis|현재 상태]] | 보안 평가 |
| :--- | :--- | :--- | :--- |
| **[[668_md5_hash_collision_vulnerability|MD5]]** | 128 [[086_fenwick_tree|bit]] | 사용 금지 (사망) | 1996년 치명적 충돌 [[352_defect_definition|결함]] 발견, [[501_file_definition_logical_record|파일]] [[003_integrity|무결성]] 체크용으로만 일부 남음 |
| **SHA-1** | 160 [[086_fenwick_tree|bit]] | 사용 금지 (사망) | 2017년 구글(SHAttered)이 동일 해시의 충돌 PDF [[501_file_definition_logical_record|파일]] [[087_process_state_transition|생성]] 시연 성공 |
| **SHA-2 (SHA-256)** | 256/512 [[086_fenwick_tree|bit]] | 현재 표준 현역 | [[073_bit|비트]]코인, [[694_thread_local_storage_tls|TLS]] [[303_authentication_authorization_patterns|인증]]서 등 현대 인터넷을 지배하는 가장 완벽한 표준 |
| **[[101_sha_3|SHA-3]] ([[101_sha_3|Keccak]])** | 가변 길이 | 차세대 예비용 | SHA-2가 뚫릴 만일의 사태를 대비해 구조 자체(스폰지)를 갈아엎은 예비 표준 |

특히 [[004_blockchain|블록체인]] [[073_bit|비트]]코인 네트워크에서는 [[014_pow_proof_of_work|작업 증명]] (PoW) 과정에서 특정 조건의 앞자리 '0'이 연속되는 해시값을 무식하게 찾아내는 과정 자체가 채굴(Mining)의 핵심 원리로 연결된다.

- **📢 섹션 요약 비유**: 해시 [[001_algorithm_definition|알고리즘]]은 '금고 다이얼의 자릿수' 진화와 같다. 도둑의 손놀림이 빨라지자 다이얼 3개짜리([[668_md5_hash_collision_vulnerability|MD5]])는 버려졌고, 지금은 우주 나이만큼 돌려도 못 맞추는 다이얼 100개짜리(SHA-256)를 표준으로 쓴다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 개발 환경에서 사용자 비밀번호를 [[002_database_definition|데이터베이스]]에 안전하게 저장하기 위해 [[667_hash_function_integrity_one_way|해시 함수]]를 날것으로 쓰면 대형 보안 사고가 터진다.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]: 빠른 속도가 부르는 재앙
해커들은 `password123`처럼 흔한 비밀번호 10억 개를 미리 [[667_hash_function_integrity_one_way|해시 함수]]로 돌려 만든 **레인보우 테이블 ([[107_rainbow_table|Rainbow Table]])** 쌍을 가지고 있다. DB를 털어서 해시값을 빼내면 이 사전에서 단 몇 초 만에 원래 비밀번호를 찾아낸다. [[667_hash_function_integrity_one_way|해시 함수]]의 연산 속도가 너무 빠르기 때문에 역설적으로 [[456_brute_force|브루트포스]] 공격에 취약한 것이다.

### 실무적 의사결정 (보완책 적용)
1. **[[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]] ([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]]) 추가**: 패스워드 원본 앞뒤에 무작위 문자열(소금)을 뿌려 해시한다. 해커의 기존 레인보우 테이블을 완전한 휴지조각으로 만든다.
2. **[[109_key_stretching|키 스트레칭]] ([[109_key_stretching|Key Stretching]])**: 믹서기를 한 번만 돌리지 않고, 수천 번 반복해서 돌려 연산 시간을 고의로 지연시킨다. 해커가 대입 공격을 시도할 때 컴퓨터가 과부하 걸리게 만든다. 
3. **권장 [[336_library_vs_framework|라이브러리]] 채택**: 실무에서는 단순히 SHA-256을 쓰지 않고, [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]와 스트레칭이 내장된 `Bcrypt`, `PBKDF2`, `Argon2` [[001_algorithm_definition|알고리즘]] 프레임워크를 기본 탑재해야 한다.

- **📢 섹션 요약 비유**: 문이 너무 튼튼하지만 너무 빨리 열린다면 도둑이 수만 개의 열쇠를 순식간에 꽂아볼 수 있다. [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]는 도둑의 만능 열쇠 묶음을 버리게 만드는 것이고, [[109_key_stretching|키 스트레칭]]은 열쇠를 돌리는 데 무조건 1초씩 뻑뻑하게 걸리게 만들어 도둑을 지치게 하는 방어벽이다.

---

## Ⅴ. 기대효과 및 결론

암호화가 남의 눈을 가리는 '마스크'라면, [[667_hash_function_integrity_one_way|해시 함수]]는 남의 위조를 거부하는 '봉인 (Seal)'이다.
[[667_hash_function_integrity_one_way|해시 함수]]는 복호화가 불가능하다는 태생적 [[352_defect_definition|결함]]을 가장 강력한 무기([[003_integrity|무결성]] 증명)로 승화시킨 암호학의 천재적인 발명품이다. 아무리 방대한 [[001_dikw_pyramid|데이터]]라도 짧은 거울에 그 본질을 완벽히 비추어 담아내며, 오늘날 [[303_authentication_authorization_patterns|인증]], [[988_digital_signature|전자 서명]], [[004_blockchain|블록체인]] 등 전산망의 신뢰를 담보하는 가장 단단한 주춧돌로 군림하고 있다.

- **📢 섹션 요약 비유**: [[667_hash_function_integrity_one_way|해시 함수]]는 고대의 '밀랍 인장'이다. 편지 내용을 숨기지는 않지만, 인장이 온전하게 도착했다는 사실 하나만으로 중간에 편지가 뜯어지거나 내용이 조작되지 않았음을 100% 보증하는 신뢰의 징표다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[988_digital_signature|전자 서명]] ([[675_digital_signature_process_asymmetric_key|Digital Signature]])** | 원본 [[001_dikw_pyramid|데이터]]의 해시값을 비대칭키 쌍(개인키)으로 암호화하여 서명자를 증명하는 기술 |
| **레인보우 테이블 ([[107_rainbow_table|Rainbow Table]])** | 해커가 평문과 해시값 쌍을 미리 계산해 둔 거대한 해킹 사전 |
| **[[109_key_stretching|키 스트레칭]] (Bcrypt, PBKDF2)** | 해시 연산을 의도적으로 수천 번 반복하여 무차별 대입 공격을 지연시키는 패스워드 방어 기법 |
| **[[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]] ([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])** | 레인보우 테이블 공격을 무력화하기 위해 평문 암호에 추가하는 난수 문자열 |

### 📈 관련 키워드 및 발전 흐름도

```text
비밀번호 평문 저장 및 통신 위조 위험 대두
    │
    ▼
암호학적 해시 알고리즘 등장 (MD5, SHA-1)
    │
    ▼
무결성 보장 및 단방향 패스워드 저장 실현
    │
    ▼
컴퓨터 성능 향상으로 인한 해시 충돌 및 레인보우 테이블 공격 위협
    │
    ▼
안전한 해시 표준(SHA-256) 채택 및 솔트/키 스트레칭(Bcrypt) 적용 필수화
```

### 👶 어린이를 위한 3줄 비유 설명

1. 100페이지짜리 긴 편지를 보낼 때, 도둑이 중간에 한 글자라도 바꿨는지 확인하고 싶어요.
2. 그래서 편지를 '[[667_hash_function_integrity_one_way|해시 함수]]'라는 믹서기에 넣고 돌렸더니, `A9!#`라는 짧은 4글자 지문이 튀어나와서 편지 겉면에 적어 보냈어요.
3. 도둑이 몰래 편지에서 마침표 하나만 지워도 믹서기에서 `Z8@&`라는 완전히 다른 지문이 나오기 때문에, 단번에 도둑의 장난을 알아채는 거짓말 탐지기랍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 97 / 1108

← **이전**: [[096_ind_cca2|096. IND-CCA2 — 강인한 암호학적 안전성]]
**다음**: [[098_md5|098. MD5 — 128비트 해시, 충돌 공격 실용화 (1996)]] →

---
