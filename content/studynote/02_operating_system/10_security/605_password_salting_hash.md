---
title: 605. 비밀번호 솔팅 (Salting) 기반 해시 처리 방어 구조
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 패스워드 솔팅 (Salting)은 사용자의 평문 비밀번호를 [[008_단방향_반이중_전이중|단방향]] 해시(Hash) [[001_algorithm_definition|알고리즘]]으로 변환하기 직전에, 무작위의 고유한 난수 문자열([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])을 덧붙여 해시 결과값을 완전히 뒤섞어버리는 보안 기법이다.
> 2. **가치**: [[002_database_definition|데이터베이스]](DB)가 해커에게 통째로 유출(Breach)되는 최악의 상황에서도, 해커가 미리 계산해둔 거대한 해시 사딕(레인보우 테이블)을 무용지물로 만들어 평문 패스워드 복원을 수학적·물리적으로 불가능하게 만드는 최후의 저지선이다.
> 3. **융합**: [[001_operating_system_purpose|운영체제]]의 `/etc/shadow` [[501_file_definition_logical_record|파일]] 구조와 [[652_cryptography_concept_encryption_decryption|암호학]]([[652_cryptography_concept_encryption_decryption|Cryptography]])의 [[008_단방향_반이중_전이중|단방향]] [[667_hash_function_integrity_one_way|해시 함수]](SHA-256, bcrypt, Argon2) 특성이 융합된 기술로, 단순한 암호화(Encryption)와 해싱(Hashing)의 근본적 차이를 보여주는 아키텍처 설계의 교과서적 사례다.

---

## Ⅰ. 개요 및 필요성

**개념 및 정의**
[[001_operating_system_purpose|운영체제]](OS)와 현대 애플리케이션은 사용자의 패스워드를 저장할 때 '평문(Plain text)'이나 양방향 복호화가 가능한 '암호문(Encryption)'으로 저장하지 않는다. 대신 원래 값으로 되돌릴 수 없는 [[008_단방향_반이중_전이중|단방향]] 암호화인 '해시(Hash)' 값으로 저장한다. 패스워드 솔팅(Salting)은 여기서 한 걸음 더 나아가, 동일한 패스워드라도 사용자마다 각기 다른 무작위 [[001_dikw_pyramid|데이터]]([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])를 추가하여 항상 고유한 해시 결과값이 나오도록 강제하는 메커니즘이다.

**필요성 및 등장 배경**
[[459_quic_fec_forward_error_correction|초기]] 시스템들은 패스워드 해시 저장이 안전하다고 믿었다. 하지만 [[008_단방향_반이중_전이중|단방향]] 해시라도 `123456` 같은 흔한 패스워드의 해시값은 항상 똑같이 나온다는 치명적 맹점이 존재했다. 공격자들은 "어차피 사람들이 쓰는 패스워드는 수천만 개 정도니, 모든 경우의 수의 해시값을 미리 계산해서 표(레인보우 테이블, [[107_rainbow_table|Rainbow Table]])로 만들어 두자"는 발상을 실행에 옮겼다. 서버 DB가 털리면 해커는 이 거대한 엑셀 표(레인보우 테이블)에서 DB의 해시값을 검색(Look-up)하기만 하면 단 1초 만에 원래 패스워드를 알아낼 수 있었다. 이를 파괴하기 위해 소금([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])을 뿌려 해커의 미리 계산된 식단을 망쳐버리는 솔팅 기술이 등장했다.

```text
┌────────────────────────────────────────────────────────────┐
│      단순 해시(Unsalted) 시스템의 치명적 한계 (레인보우 테이블)│
├────────────────────────────────────────────────────────────┤
│                                                            │
│  [동일한 패스워드 = 동일한 해시값 생성]                    │
│  사용자 A (PW: apple123) ──(해시 SHA256)──▶ 1a2b3c...      │
│  사용자 B (PW: apple123) ──(해시 SHA256)──▶ 1a2b3c...      │
│                                                            │
│  [해커의 무기: 레인보우 테이블 (미리 계산된 해시 사전)]    │
│    평문 패스워드  │   SHA-256 해시값                       │
│    ─────────────┼─────────────────────────────           │
│    password     │   5e8848...                              │
│    123456       │   8d969e...                              │
│    apple123     │   1a2b3c... ◀─ 빙고! 1초 만에 탈취 성공 │
│                                                            │
│  결과: DB가 유출되면 1a2b3c 해시값을 가진 A와 B의 패스워드는 │
│        복호화(Decryption) 연산 없이 '검색'만으로 털리게 됨. │
└────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 구조도는 "해시(Hash)는 복호화가 불가능하니까 안전하다"는 고정관념을 해커들이 어떻게 박살 냈는지를 보여준다. [[667_hash_function_integrity_one_way|해시 함수]] 자체는 [[008_단방향_반이중_전이중|단방향]]이 맞지만, 수학적 [[099_one_to_one_model|일대일]] 매핑이 성립하므로(동일 입력 = 동일 출력), 해커가 오프라인에서 미리 10테라바이트짜리 거대한 '입력-출력 매핑 테이블([[107_rainbow_table|Rainbow Table]])'을 수년 동안 만들어두면 방어막이 순식간에 뚫린다. 특히 여러 사용자가 동일한 패스워드를 쓰는 경우, 한 명의 패스워드가 풀리면 똑같은 해시값을 가진 수천 명의 패스워드도 동시에 노출되는 군집 붕괴 현상이 발생한다.

- **📢 섹션 요약 비유**: 해커가 세상 모든 열쇠와 자물쇠 모양을 도감(레인보우 테이블)으로 만들어 들고 다녀서 자물쇠 겉모양만 보고도 열쇠를 깎아내는 상황인데, 자물쇠 안에 불규칙하게 튀어나온 소금 알갱이([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])를 뿌려 도감 자체를 휴지 조각으로 만들어버리는 기술입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 구성 요소 (안전한 패스워드 저장 파이프라인)

| 요소명 | 역할 | 내부 동작 | 비유 |
|:---|:---|:---|:---|
| **평문 패스워드 (Plain PW)** | 사용자가 입력한 원래 비밀번호 | `Password123!` | 요리용 기본 식재료 |
| **[[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]] ([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]] 값)** | 사용자마다 다르게 생성되는 긴 난수 | 난수 발생기([[1001_csprng_random_generator|CSPRNG]])로 생성된 고유 문자열 (`Ex: 8fA2#k`) | 음식마다 다르게 치는 양념 |
| **[[667_hash_function_integrity_one_way|해시 함수]] (Hash [[001_algorithm_definition|Algorithm]])** | 평문과 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]의 결합을 섞어 돌림 | `Hash(PW + Salt)` 또는 `Hash(Salt + PW)` 연산 수행 | 강력한 블렌더(믹서기) |
| **[[109_key_stretching|키 스트레칭]] ([[109_key_stretching|Key Stretching]])** | 해커의 브루트 포스 연산을 [[015_지연_데이터_관점|지연]] | 해시 결과값을 다시 [[667_hash_function_integrity_one_way|해시 함수]]에 넣는 과정을 수천~수만 번 반복 | 믹서기를 [[489_raid_10_hybrid|10]],000번 돌리기 |
| **저장소 (ex: `/etc/shadow`)** | 최종 해시 및 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]값, [[001_algorithm_definition|알고리즘]] [[012_metadata|메타데이터]] 보관 | `$알고리즘$솔트값$최종해시값` 형태로 DB/[[501_file_definition_logical_record|파일]]에 기록 | 레시피 결과물 보관소 |

### 심층 동작 원리: 솔팅(Salting)과 [[109_key_stretching|키 스트레칭]]([[109_key_stretching|Key Stretching]])의 융합

현대 OS와 [[303_authentication_authorization_patterns|인증]] 프레임워크(Spring [[283_security_tactics|Security]], Django 등)는 단순히 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]] 하나만 추가하는 것에 만족하지 않는다. 해커들의 [[418_gpu|GPU]] 연산(초당 수십 억 번 해시 계산)이 너무 빨라졌기 때문이다. 이에 대응하기 위해 해시를 한 번만 하는 것이 아니라 반복 횟수(Work Factor/Cost)를 주어 일부러 계산을 느리게 만드는 **[[109_key_stretching|키 스트레칭]]([[109_key_stretching|Key Stretching]])**을 솔팅과 융합하여 아키텍처를 설계한다. 대표적인 [[001_algorithm_definition|알고리즘]]이 **bcrypt, PBKDF2, Argon2** 이다.

```text
┌────────────────────────────────────────────────────────────┐
│      Bcrypt 알고리즘 기반 솔팅 및 키 스트레칭 파이프라인   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  [1. 계정 생성 시 데이터베이스 저장 과정]                  │
│  사용자 PW : "apple123"                                    │
│  난수 Salt : "xY7#z9Q" (사용자 전용 고유 난수 생성)        │
│                                                            │
│  [2. 키 스트레칭 엔진 (수만 번 반복 연산)]                 │
│  Hash_0 = SHA256 ( "apple123" + "xY7#z9Q" )                │
│  Hash_1 = SHA256 ( Hash_0 + "xY7#z9Q" )                    │
│  Hash_2 = SHA256 ( Hash_1 + "xY7#z9Q" )                    │
│    ...                                                     │
│  Hash_10000 = 최종 다이제스트(Digest) 생성 완료            │
│                                                            │
│  [3. 리눅스 /etc/shadow 또는 DB 저장 포맷 ($ 분리자)]      │
│  db_row: $2b$12$xY7#z9Q.............1a2b3c4d5e6f7g8h9i     │
│          ─── ── ───────             ──────────────────     │
│           │   │    │                        │              │
│  알고리즘(Bcrypt)  │                        └── 최종 해시값│
│        Cost Factor (2^12회 반복)                           │
│                 └── 솔트(Salt) 평문 값 (해커가 봐도 상관없음)│
└────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 구조도는 단순한 암호화가 아닌, 해커의 컴퓨팅 파워를 소모시키기 위한 "의도적 [[015_지연_데이터_관점|지연]](Delay)" 아키텍처를 보여준다. 사용자 계정이 생성될 때마다 새로운 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])가 발급되므로, 두 사용자가 똑같이 `apple123`이라는 패스워드를 쓰더라도 DB에 저장되는 최종 해시값은 완전히 달라진다. [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]] 값 자체는 암호가 아니므로 DB에 해시값과 나란히 평문으로 저장해도 무방하다. ([[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]는 레인보우 테이블을 무력화할 뿐, [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]] 자체가 비밀일 필요는 없다). 여기에 `Cost Factor(12)`가 주어지면, 해시 연산을 $2^{12}$(4,096)번 이상 반복한다. 정상 사용자가 로그인할 때는 0.1초의 [[015_지연_데이터_관점|지연]]만 생기므로 UX에 지장이 없지만, 해커가 DB를 털어가서 1억 개의 패스워드 사전을 브루트 포스(Brute-Force) 공격으로 대입하려 하면, 한 번 시도할 때마다 0.1초가 걸려 해킹에 수천 년이 걸리게 만드는 물리적 방어 체계다.

- **📢 섹션 요약 비유**: 해커가 엄청나게 빠른 헬리콥터([[418_gpu|GPU]])를 타고 도망가려 할 때, [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])가 출발 방향을 수억 갈래로 흐트러뜨리고, [[109_key_stretching|키 스트레칭]]이 헬기에 무거운 모래주머니 수만 개를 매달아 버려 결국 날아오르지 못하게 만드는 물리적 억제술과 같습니다.

---

## Ⅲ. 비교 및 연결

### 패스워드 방어 [[001_algorithm_definition|알고리즘]]의 진화 과정 ([[668_md5_hash_collision_vulnerability|MD5]] -> Bcrypt -> Argon2)

과거 웹 개발자들은 속도가 빠르다는 이유로 MD5나 SHA-1 같은 일반 범용 [[667_hash_function_integrity_one_way|해시 함수]]를 사용했다. 하지만 이들은 [[501_file_definition_logical_record|파일]] [[003_integrity|무결성]]을 빠르게 체크하기 위해 발명된 [[001_algorithm_definition|알고리즘]]일 뿐, 패스워드 [[571_protection_vs_security|보호]]용으로는 최악의 선택이다.

| 해시 [[001_algorithm_definition|알고리즘]] | 개발 목적 | 패스워드 방어 특징 | 한계점 및 보안 수준 |
|:---|:---|:---|:---|
| **[[668_md5_hash_collision_vulnerability|MD5]] / SHA-1** | [[501_file_definition_logical_record|파일]] 다운로드 [[003_integrity|무결성]] [[148_5g_embb_urllc_mmtc|초고속]] [[395_verification_process_review|검증]] ([[112_checksum|Checksum]]) | 연산 속도가 너무 빠름 (GPU로 초당 수백억 번 연산) | **사용 금지**. 해커의 Brute-Force 공격 방어력 0. 충돌 취약점 존재. |
| **PBKDF2** | [[652_cryptography_concept_encryption_decryption|암호학]]적 키 도출 및 [[571_protection_vs_security|보호]] | [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]] 지원 + 수만 번의 반복 해시 연산([[109_key_stretching|키 스트레칭]]) 제공 | 연산이 오직 CPU(연산량)에만 의존하여, 해커가 [[070_asic|ASIC]]/[[418_gpu|GPU]] 팜을 구축하면 뚫릴 위험 있음. |
| **Bcrypt** | **전용 패스워드 해시 암호화** | Cost Factor를 조절하여 컴퓨팅 [[282_performance_tactics|성능]] 발전에 대응 가능 | 리눅스, 스프링 등 현대 IT 인프라의 **글로벌 기본 표준 (De Facto)**. |
| **Argon2** | 차세대 패스워드 해싱 대회(PHC) 우승작 | CPU 연산량 + **메모리(RAM) 요구량** + [[430_index_fast_full_scan|병렬]] 처리 [[092_thread_lwp|스레드]] 수까지 통제 | **최고 보안 등급**. 해커가 [[430_index_fast_full_scan|병렬]] GPU를 써도 막대한 RAM이 필요해 칩을 만들 수 없게 물리적으로 차단. |

가장 최신 표준인 **Argon2**의 핵심은 해시 연산 시 CPU뿐만 아니라 대량의 메모리(Memory-Hard)를 요구한다는 점이다. 해커는 [[418_gpu|GPU]] 안에 수천 개의 코어를 가지고 있지만 RAM 용량은 제한적이므로, Argon2 [[001_algorithm_definition|알고리즘]] 앞에서는 GPU의 장점을 전혀 살릴 수 없다.

```text
┌────────────────────────────────────────────────────────────┐
│      Bcrypt (연산 지연형) vs Argon2 (메모리 의존형) 방어 비교│
├────────────────────────────────────────────────────────────┤
│                                                            │
│  [해커의 GPU 공격 장비 구조]                               │
│  GPU 1개당 4,000개의 연산 코어 보유 (RAM은 상대적으로 적음)│
│                                                            │
│  [Bcrypt 기반 방어 타격 시]                                │
│  CPU 연산만 복잡하게 만듦. 해커는 4,000개의 코어를         │
│  병렬로 돌려 동시에 4,000개의 비밀번호를 대입해버림.       │
│  => 방어력 한계치 봉착 (GPU 팜 앞에서는 뚫림)              │
│                                                            │
│  [Argon2 기반 방어 타격 시 (Memory-Hard Feature)]          │
│  규칙: "이 해시 1개를 계산하려면 반드시 1GB의 RAM을 채워야함"│
│  해커의 시도: 4,000개 코어를 동시에 돌리려 함              │
│  결과: RAM이 4,000GB(4TB)나 필요해짐! GPU 메모리 터짐.💥  │
│  => 해커는 억지로 코어 10개만 돌릴 수밖에 없어 공격 속도가 │
│     1/400로 극단적으로 수렴하여 포기하게 됨.               │
└────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이 비교도는 사이버 창과 방패의 싸움이 단순한 수학 [[001_algorithm_definition|알고리즘]]을 넘어 하드웨어 아키텍처(CPU vs Memory)의 한계를 공략하는 물리전으로 진화했음을 보여준다. Bcrypt나 PBKDF2는 연산 시간을 늘려(Time-cost) 방어하지만, 해커들이 비트코인 채굴에 쓰이는 [[430_index_fast_full_scan|병렬]] 연산 특화 괴물 [[418_gpu|GPU]] 팜을 구성하자 이 시간 [[015_지연_데이터_관점|지연]]이 [[430_index_fast_full_scan|병렬]] 처리로 무력화되었다. 이에 방어자들은 해시 계산 과정에 거대한 [[459_dummy_test_double|더미]] [[001_dikw_pyramid|데이터]]를 메모리에 쓰고 읽기를 반복하게 만드는 Argon2 [[001_algorithm_definition|알고리즘]]을 도입했다. 해커가 [[430_index_fast_full_scan|병렬]] 코어를 돌리려 해도 메모리(Memory-cost) 대역폭과 용량이 발목을 잡아, 하드웨어 확장의 가성비가 최악으로 떨어지게 만들어 브루트 포스 공격의 경제성을 완전히 파괴해버린 예술적 방어 설계다.

- **📢 섹션 요약 비유**: 옛날 방어법(Bcrypt)이 범인에게 엄청나게 복잡한 수학 문제를 내어 시간을 끌게 했다면, 최신 방어법(Argon2)은 수학 문제를 풀려면 100평짜리 축구장(메모리)을 뛰어다니며 숫자를 주워오도록 강제하여 범인의 체력과 공간 자체를 물리적으로 고갈시키는 전법입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 레거시 [[668_md5_hash_collision_vulnerability|MD5]] 시스템에서 Bcrypt 아키텍처로의 무중단 마이그레이션

1. **상황**: 10년 된 쇼핑몰의 DB를 [[606_auditing_linux_auditd|감사]]([[363_audit|Audit]])해 보니, 200만 명 고객의 패스워드가 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]]) 없이 단순 `MD5`나 `SHA-256`으로 저장되어 있었다. 만약 DB가 털리면 고객의 패스워드가 평문으로 노출되는 치명적 보안 리스크가 발견되었다.
2. **문제점 (딜레마)**: 관리자가 DB 내의 기존 [[668_md5_hash_collision_vulnerability|MD5]] 해시값을 Bcrypt로 일괄 변환하고 싶어도, [[667_hash_function_integrity_one_way|해시 함수]]의 특성상 [[008_단방향_반이중_전이중|단방향]]이므로 원래 패스워드(평문)를 알 수 없어 자체 변환이 불가능하다. 고객들에게 "비밀번호를 일괄 재설정해주세요"라고 공지하면 비즈니스 이탈률(Churn rate)이 심각해진다.
3. **아키텍트의 의사결정 ([[380_computational_graph_lazy_eager_execution|Lazy]]/Wrapping Migration [[268_strategy_pattern|전략]])**:
   - DB 컬럼을 추가하거나 저장 포맷을 변경하여, 이 해시값이 구형([[668_md5_hash_collision_vulnerability|MD5]])인지 신형(Bcrypt)인지 식별할 수 있는 [[288_version_ihl_tos_total_length|버전]] 플래그를 넣는다.
   - 사용자가 로그인을 시도할 때 입력하는 **평문 패스워드가 들어오는 그 찰나의 순간**을 이용한다.
   - 서버 로직: 입력된 평문을 기존 [[668_md5_hash_collision_vulnerability|MD5]] 로직으로 돌려 DB 값과 일치하는지 먼저 확인하여 [[303_authentication_authorization_patterns|인증]]을 통과시킨다.
   - 통과 직후, 서버는 메모리에 들고 있던 그 "평문 패스워드"를 즉시 신형 **Bcrypt ([[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]] + 스트레칭)** 로 다시 해싱하여 DB의 기존 [[668_md5_hash_collision_vulnerability|MD5]] 값을 조용히(백그라운드에서) 덮어씌운다(업데이트).
   - 이 방식으로 사용자가 1번이라도 로그인하는 순간 시스템은 최신 보안 등급으로 투명하게 무중단 마이그레이션된다.

### 도입 [[435_checklist_based_testing|체크리스트]] (패스워드 저장 [[164_policy|정책]])
- **Pepper(페퍼)의 추가 적용 유무**: [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])가 DB에 저장되어 DB 유출 시 함께 노출되는 방어의 한계를 극복하기 위해, [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]와 별개로 애플리케이션 서버(소스코드나 환변변수, [[1013_aws_kms|AWS KMS]]) 내부 깊숙이 숨겨둔 고정 비밀키인 **페퍼(Pepper)**를 해싱 과정에 추가로 섞어 넣었는가? (DB와 소스코드가 동시에 털리지 않는 한 해독 불가 상태 구축).
- **[[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])의 고유성 (Uniqueness)**: 하나의 전역 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]](Global [[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])를 모든 유저에게 재사용하는 것은 [[128_water_scrum_fall_anti_pattern|안티패턴]]이다. 1명의 유저당 1개의 고유한 Random Salt가 매번 새로 발급(User-Level [[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])되도록 설계되었는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- **프론트엔드(Client-Side) 해싱 남용**: "서버 부하를 줄이겠다"는 핑계로, 웹 브라우저(JavaScript) 단에서 평문 비밀번호를 해싱한 뒤 서버로 전송하는 아키텍처. 이 경우 네트워크를 타고 넘어가는 해시값 자체가 하나의 '평문 패스워드' 역할을 해버리므로(해시 패스 더 해시 공격), 스니핑이나 DB 유출 발생 시 해커가 그 해시값을 그대로 로그인 API에 던져넣어 즉시 [[303_authentication_authorization_patterns|인증]]을 통과하는 대재앙([[592_pth|Pass-the-Hash]])을 초래한다. 해싱과 솔팅은 반드시 안전한 백엔드 서버에서 이루어져야 한다.

- **📢 섹션 요약 비유**: 낡은 금고([[668_md5_hash_collision_vulnerability|MD5]])를 최신형 티타늄 금고(Bcrypt)로 바꿀 때 억지로 문을 뜯는 게 아니라, 주인이 정당한 열쇠를 들고 와서 금고를 여는 그 찰나의 순간에 관리자가 몰래 새 자물쇠로 교체해두어 아무런 불편 없이 보안을 높이는 지혜로운 전환 [[268_strategy_pattern|전략]]입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과 ([[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]] 및 [[109_key_stretching|키 스트레칭]] 도입 시)

| 구분 | 단순 해시 (SHA-256) 저장 시 | Bcrypt / Argon2 기반 솔팅 적용 시 | 기술적 함의 |
|:---|:---|:---|:---|
| **정량 (방어력)** | 레인보우 테이블로 1시간 내 DB 전체 90% 크랙 | 단일 계정 Brute-Force에 **수천 년~수만 년 소요** | 공격의 물리적/시간적 경제성 완전 파괴 (포기 유도) |
| **운영 장애** | 동일 패스워드 사용자의 군집 붕괴(연쇄 탈취) | 고유 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]]로 인해 1명 털려도 다른 유저에 영향 없음 | 장애 [[064_relation_domain|도메인]] 격리(Blast [[541_radius_remote_authentication_aaa|Radius]]) 최적화 |
| **정성 (컴플라이언스)** | [[171_isms_p|ISMS-P]], [[783_pipa_korea|개인정보보호법]] 위반으로 과징금 철퇴 | 최고 수준의 암호화 보관 의무 준수로 법적 면책 요건 충족 | 기업 [[085_confidence_association_rule_conditional_probability|신뢰도]] 하락 방지 및 보안 감리 무사 통과 |

### 미래 전망
현재 패스워드 저장의 궁극적 도달점은 Argon2 프로토콜의 정착이다. 그러나 보안 업계의 궁극적인 비전은 "해시를 어떻게 안전하게 짤 것인가"를 넘어 **"패스워드 자체를 없애는 것(Passwordless)"** 이다. FIDO2 [[303_authentication_authorization_patterns|인증]]이나 WebAuthn(패스키, [[562_passkey|Passkey]]) 같은 비대칭 키([[159_pki_public_key_infrastructure|PKI]]) 아키텍처가 전면 도입되면, 사용자 서버 DB에는 해시값이 아닌 오직 '공개키(Public [[067_db_key_uniqueness_minimality|Key]])'만이 평문으로 저장된다. 이 시대가 도래하면 해커가 DB를 통째로 유출해 가더라도, 서버엔 [[395_verification_process_review|검증]]용 껍데기만 있을 뿐 로그인할 수 있는 권한(개인키)은 사용자의 스마트폰 보안 칩(TrustZone) 내부에만 존재하므로, 수십 년간 이어져 온 평문-해시 변환의 역사 자체가 자연스럽게 종말을 맞이하게 될 것이다.

### 참고 표준
- **[[853_nist_sp_800_63b|NIST SP 800-63B]]**: 패스워드 저장소 관리 (Salting 및 [[109_key_stretching|Key Stretching]](반복 최소 [[489_raid_10_hybrid|10]],000회 이상) 강제)
- **OWASP Password Storage Cheat Sheet**: 현대 웹 애플리케이션의 패스워드 저장 권고안 (Argon2id > Bcrypt 선호)
- **개인정보의 안전성 확보조치 기준 (KISA)**: 제7조(비밀번호 암호화) 관련 [[671_password_hash_salt_pbkdf2_bcrypt_argon2|솔트]] 적용 필수 법제도

- **📢 섹션 요약 비유**: 해커의 슈퍼컴퓨터가 아무리 빨라지더라도, ನಾವು 믹서기([[109_key_stretching|키 스트레칭]])를 돌리는 횟수를 만 번에서 십만 번으로 늘리고 소금([[671_password_hash_salt_pbkdf2_bcrypt_argon2|Salt]])에 후추(Pepper)까지 뿌려버리는 방식으로 무조건 이길 수밖에 없는 방어의 체스를 두는 것과 같습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[603_rootkit_syscall_hooking|루트킷]] ([[603_rootkit_syscall_hooking|Rootkit]]) [[022_kernel_role|커널]] [[192_module_independence|모듈]] 감염 방식 (시스템 콜 테이블 후킹) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [[604_authentication_factors|사용자 인증]] ([[604_authentication_factors|Authentication]]) 요소 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[606_auditing_linux_auditd|감사]] ([[606_auditing_linux_auditd|Auditing]]) 로깅 프레임워크 (Linux Auditd) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 물리적 보안 및 [[475_hsm|하드웨어 보안 모듈]] ([[476_tpm|TPM]], [[476_tpm|Trusted Platform Module]]) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[사용자 인증 (Authentication) 요소]
    │
    ▼
[비밀번호 솔팅 (Salting) 기반 해시 처리 방어 구조]
    │
    ├──▶ [감사 (Auditing) 로깅 프레임워크 (Linux Auditd)]
    └──▶ [물리적 보안 및 하드웨어 보안 모듈 (TPM, Trusted Platform Module)]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 컴퓨터는 우리 비밀번호(예: 1234)를 그대로 저장하지 않고, 믹서기에 갈아서 알 수 없는 모양의 과일 주스(해시)로 만들어 보관해요.
2. 하지만 나쁜 도둑이 '1234를 갈면 무슨 주스가 되는지' 미리 백과사전(레인보우 테이블)으로 만들어두고 주스 색깔만 보고도 1234인 걸 맞춰버렸어요.
3. 그래서 우리는 믹서기에 갈기 직전에 사람마다 각기 다른 무작위 **소금(솔팅)** 을 한 움큼 섞어 넣어서 주스 색깔을 완전히 다르게 만들고, 도둑의 백과사전을 엉망진창으로 만들어 방어한답니다!
