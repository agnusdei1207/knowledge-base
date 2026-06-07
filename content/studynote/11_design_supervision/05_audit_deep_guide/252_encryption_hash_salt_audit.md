---
title: "Encryption Hash Salt Audit"
date: "2026-05-10"
tags:
  - "studynote-design-supervision"
weight: 252
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 중요 정보 보호는 목적에 따라 암호화(Encryption)와 해시(Hash)를 구분 적용해야 하며, 양방향·[단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/)을 혼동하면 보안 설계가 근본적으로 무너진다.
> 2. **가치**: 비밀번호 [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)([Salt](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)) 미적용 시 레인보우 테이블([Rainbow Table](/studynote/09_security/02_crypto/107_rainbow_table/)) 공격으로 전체 사용자 계정이 동시에 탈취되며, [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) 적용만으로 이 위험을 원천 차단한다.
> 3. **판단 포인트**: DB 내 비밀번호 컬럼이 SHA-256 단순 해시인지 vs. BCrypt/PBKDF2처럼 [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)+반복 연산이 적용된 해시인지가 감리 핵심 판단 기준이다.

---

## Ⅰ. 개요 및 필요성
[개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/)([Personal Information](/studynote/09_security/16_data_privacy/781_personal_information/) [Protection](/studynote/02_operating_system/10_security/571_protection_vs_security/) Act)과 정보통신망법은 주민등록번호·비밀번호·바이오정보 등의 암호화 저장을 의무화하고 있다. 공공정보화사업 감리에서 암호화·해시·[솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) 적용 여부는 보안 점검의 최우선 항목이다.

| 구분 | 목적 | 복호화 가능 여부 | 대표 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
|:---|:---|:---|:---|
| 양방향 암호화 | 저장 후 원본 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 필요 | 가능 (키 보유 시) | [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-256, [3DES](/studynote/09_security/02_crypto/087_3des/) |
| [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 해시 | 원본 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 불필요, 일치 검증만 | 불가 | SHA-256, BCrypt, PBKDF2 |

| 정보 유형 | 권장 방식 | 근거 |
|:---|:---|:---|
| 비밀번호 | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 해시 + [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) | 복호화 자체가 필요 없음 |
| 주민등록번호 | [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-256 양방향 암호화 | 업무상 복호화 필요 |
| 카드번호, 계좌번호 | [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-256 + 별도 키 관리 서버 | PCI-DSS(Payment Card Industry [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Standard) 요건 |
| 생체 정보 | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 해시 (템플릿 비교) | 원본 저장 금지 |

```text
+--------------+    +--------------+    +--------------+
| Problem      |--->| Core Idea    |--->| Expected Gain |
+--------------+    +--------------+    +--------------+
```

- **📢 섹션 요약 비유**: 비밀번호를 양방향 암호화로 저장하는 것은 "금고에 열쇠와 돈을 같이 넣어두는 것"이다. [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 해시만이 유일한 안전한 선택이다.

---

## Ⅱ. 아키텍처 및 핵심 원리
```
+------------------------------------------------------------+
|              비밀번호 해시 + 솔트 저장 흐름                  |
|                                                            |
|  사용자 입력: "password123"                                  |
|       |                                                    |
|       v                                                    |
|  +----------------------------------+                      |
|  |  솔트 생성 (16바이트 난수)         |                      |
|  |  Salt = "a8f3c2e1b7d9f4a2..."    |                      |
|  +--------------+-------------------+                      |
|                 |                                          |
|                 v                                          |
|  +----------------------------------+                      |
|  |  Hash( "password123" + Salt )    |                      |
|  |  또는 BCrypt(password, salt, 12) |  <- 반복 횟수(Cost) 12  |
|  +--------------+-------------------+                      |
|                 |                                          |
|                 v                                          |
|  DB 저장: { salt: "a8f3c2...", hash: "9b2f4a..." }         |
|                                                            |
|  검증 시: Hash( 입력값 + 저장된 Salt ) == 저장된 Hash?       |
+------------------------------------------------------------+
```

```
+---------------------------------------------+
|  솔트 미적용 (취약)                           |
|                                             |
|  "password123" -> SHA-256 -> 0x5baa61...      |
|  "password123" -> SHA-256 -> 0x5baa61...      |
|  (동일 비밀번호 = 동일 해시 -> 테이블 조회 가능) |
+---------------------------------------------+

+---------------------------------------------+
|  솔트 적용 (안전)                             |
|                                             |
|  "password123" + Salt_A -> 0x9b2f4a...       |
|  "password123" + Salt_B -> 0xc7d3e8...       |
|  (동일 비밀번호도 다른 해시 -> 테이블 무효화)   |
+---------------------------------------------+
```

| [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 유형 | 키 길이 / 반복 | 보안 수준 | 감리 판정 |
|:---|:---|:---|:---|:---|
| [MD5](/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/) | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 해시 | - | ❌ 취약 (충돌 발견) | 사용 금지 |
| SHA-1 | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 해시 | - | ❌ 취약 | 사용 금지 |
| SHA-256 | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 해시 | 256bit | ⚠ [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) 없으면 취약 | [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) 필수 |
| BCrypt | 적응형 해시 | Cost [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)~14 | ✅ 권장 | 권장 |
| PBKDF2 | 적응형 해시 | 반복 100,000+ | ✅ 권장 | 권장 |
| [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-128 | 양방향 암호화 | 128bit | ⚠ 최소 기준 | 256bit 권장 |
| [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-256 | 양방향 암호화 | 256bit | ✅ 권장 | 권장 |
| [3DES](/studynote/09_security/02_crypto/087_3des/) | 양방향 암호화 | 168bit | ⚠ 레거시 | [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/) 전환 권고 |

- **📢 섹션 요약 비유**: BCrypt의 반복 연산(Cost)은 "금고를 열려면 열쇠를 만 번 돌려야 하는" 구조다. 공격자 입장에서는 수십억 번 시도가 수천 년이 걸린다.

---

## Ⅲ. 비교 및 연결
| 법령 | 대상 정보 | 요구 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 감리 근거 |
|:---|:---|:---|:---|
| [개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/) | 비밀번호, 주민번호, 바이오정보 | 암호화 필수 ([알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 미지정) | 제29조 안전조치 의무 |
| 정보통신망법 | 비밀번호 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 암호화 | [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 해시 명시 | 제28조 |
| 전자금융거래법 | 금융 정보 | [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-256 이상 | 금감원 [전자금융감독규정](/studynote/09_security/17_framework_compliance/888_electronic_financial_supervision_regulation/) |
| [ISMS-P](/studynote/12_it_management/05_security_compliance/171_isms_p/) | 전체 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) | 암호화 수준 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 기준 | 2.6.4 항목 |

```
+------------------------------------------------------------+
|              암호화 키 관리 3계층 구조                       |
|                                                            |
|  +----------------------------+                            |
|  |  마스터 키 (Master Key)     |  <- HSM/KMS 관리            |
|  +-------------+--------------+                            |
|                | 암호화                                     |
|                v                                           |
|  +----------------------------+                            |
|  |  데이터 암호화 키 (DEK)     |  <- 애플리케이션 레이어      |
|  +-------------+--------------+                            |
|                | 암호화                                     |
|                v                                           |
|  +----------------------------+                            |
|  |  실제 데이터 (암호문)        |  <- DB 저장                 |
|  +----------------------------+                            |
|                                                            |
|  HSM: Hardware Security Module                             |
|  KMS: Key Management Service                               |
+------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 암호화 키를 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 같은 DB에 저장하는 것은 "금고 비밀번호를 금고 안에 넣어두는 것"이다. 키는 반드시 분리된 [HSM](/studynote/01_computer_architecture/14_hardware_security_trends/475_hsm/)([Hardware Security Module](/studynote/09_security/03_network_security/157_hsm_hardware_security_module/))에 보관해야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단
1. <strong>DB <a href="/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a> <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: 비밀번호 컬럼의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 길이 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)
   - [MD5](/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/): 32자, SHA-256: 64자, BCrypt: 60자 ($2a$ 접두사 포함)
   - 컬럼 길이가 32자이면 [MD5](/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/) 사용 의심 -> 즉시 지적

2. <strong>소스코드 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>: `MessageDigest.getInstance("MD5")` 등 취약 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 탐색

3. **실제 비밀번호 테스트**: 알려진 평문("admin1234")의 해시 값이 레인보우 테이블에 존재하는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)

4. <strong><a href="/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/">솔트</a> 저장 위치</strong>: [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)가 해시 값과 같은 필드에 저장되는지, 별도 컬럼에 저장되는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) (BCrypt는 해시에 [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)를 포함하여 저장)

| 지적 사항 | 위험도 | 조치 방법 |
|:---|:---|:---|
| [MD5](/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/)/SHA-1 사용 | Critical | BCrypt/PBKDF2로 전환 후 기존 해시 마이그레이션 |
| [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) 미적용 SHA-256 | High | [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 배포 전 [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) 재적용 필수 |
| 비밀번호 평문 저장 | Critical | 즉시 중단, [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 해시로 변환 |
| 암호화 키 소스 하드코딩 | High | 환경변수 또는 KMS로 분리 |
| [3DES](/studynote/09_security/02_crypto/087_3des/) 사용 | Medium | [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-256 전환 계획 수립 |

### 판단 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 위험 시나리오와 점검 범위가 문서로 합의되었는가?
2. 지표·증적·로그가 재현 가능하게 수집되는가?
3. 예외 상황과 오탐·미탐 처리 절차가 있는가?
4. 재시험 또는 후속 조치 기준이 수치로 정의되었는가?

- **📢 섹션 요약 비유**: [MD5](/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/) 해시를 사용하는 것은 "자물쇠 제조사가 폐업한 구형 자물쇠"를 쓰는 것이다. 이미 열쇠 복제법이 공개된 만큼 즉시 교체가 필요하다.

---

## Ⅴ. 기대효과 및 결론
체계적인 암호화·해시·[솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) 감리를 통해 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 침해 시에도 피해를 최소화하고 법적 의무를 이행할 수 있다. 특히 BCrypt/PBKDF2 적용은 무차별 대입([Brute Force](/studynote/09_security/05_web_app_security/456_brute_force/)) 공격 비용을 기하급수적으로 높여 현실적 공격을 불가능하게 만든다. 국내 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 침해 사고의 약 30%가 평문 또는 취약 해시 저장에서 기인하며, [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)+적응형 해시 적용만으로도 대부분의 대규모 유출 피해를 방지할 수 있다.

확장 방향은 ① [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/) [as](/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/studynote/02_operating_system/02_process_thread/082_process_memory_structure/), ② Continuous [Audit](/studynote/12_it_management/05_security_compliance/363_audit/), ③ [인공지능](/studynote/10_ai/03_llm_nlp/231_ai_turing_test/)([AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), [Artificial Intelligence](/studynote/10_ai/01_ai_basics/001_artificial_intelligence/)) 기반 이상 탐지와 결합하는 것이다.

- **📢 섹션 요약 비유**: BCrypt는 "금고를 열 때마다 퍼즐을 풀어야 하는 구조"다. 정상 사용자는 1번만 풀면 되지만, 공격자는 수억 번을 풀어야 하므로 현실적으로 포기하게 된다.

---

### 📌 관련 개념 맵
| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | [개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/) | 암호화 의무 법적 근거 |
| 상위 개념 | [ISMS-P](/studynote/12_it_management/05_security_compliance/171_isms_p/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 기준 2.6.4 | 암호화 적용 요건 |
| 하위 개념 | BCrypt / PBKDF2 | 비밀번호용 적응형 해시 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| 하위 개념 | [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-256 | 양방향 대칭 암호화 표준 |
| 하위 개념 | [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) ([Salt](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)) | 레인보우 테이블 방어용 난수 |
| 연관 개념 | [HSM](/studynote/01_computer_architecture/14_hardware_security_trends/475_hsm/) / [KMS](/studynote/07_enterprise_systems/02_erp_systems/127_kms_knowledge_management_system/) | 암호화 키 [하드웨어 보안 모듈](/studynote/01_computer_architecture/14_hardware_security_trends/475_hsm/) |
| 연관 개념 | 레인보우 테이블 ([Rainbow Table](/studynote/09_security/02_crypto/107_rainbow_table/)) | 해시 역산 사전 공격 기법 |

### 📈 관련 키워드 및 발전 흐름도
비밀 관리 -> 암호화 해시 [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) 감리 -> [KDF](/studynote/09_security/03_network_security/144_hkdf_tls_1_3/)·[HSM](/studynote/01_computer_architecture/14_hardware_security_trends/475_hsm/) 운영

### 👶 어린이를 위한 3줄 비유 설명
1. 비밀번호를 그냥 저장하는 건 일기장에 "내 비밀번호는 1234야"라고 쓰는 것과 같아.
2. [솔트](/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)는 음식에 소금을 넣듯 비밀번호에 랜덤 재료를 섞어서 같은 비밀번호도 완전히 다른 맛이 나게 하는 거야.
3. BCrypt는 그 섞은 음식을 만 번 더 끓이는 것처럼, 해커가 맛을 알아내려면 엄청난 시간이 걸려서 포기하게 만들어.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 313 / 530

<- **이전**: [251. 시큐어 코딩 SQL/XSS/CSRF 진단 (Secure Coding SQL/XSS/CSRF Audit)](/studynote/11_design_supervision/05_audit_deep_guide/251_secure_coding_sql_xss_csrf/)
**다음**: [253. 예외 처리 정보 노출 감리 (Exception Handling Info Leak Audit)](/studynote/11_design_supervision/05_audit_deep_guide/253_exception_handling_info_leak/) ->

---
