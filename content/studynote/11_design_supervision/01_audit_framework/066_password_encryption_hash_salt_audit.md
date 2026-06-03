+++
title = "66. 비밀번호 암호화 저장 방식 (단방향 해시 및 솔팅) 감리"
date = 2026-04-10

[taxonomies]
tags = ["studynote-design"]

[extra]
tags = ["studynote-design"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 비밀번호는 암호화(encryption)보다 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 해시(hash)와 [솔트](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)([salt](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/))로 저장해야 한다.
> 2. **가치**: [솔트](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)는 같은 비밀번호라도 서로 다른 해시를 만들고, 레인보우 테이블 공격을 어렵게 한다.
> 3. **판단**: 감리에서는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 선택, [salt](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 반복 횟수, 저장 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 모두 확인해야 한다.

---

## Ⅰ. 개요 및 필요성

비밀번호는 복구할 필요가 없으므로 복호화 가능한 암호화가 아니라 해시가 맞다. 이 차이를 모르고 설계하면 보안 사고로 이어진다.

그래서 감리에서는 비밀번호가 "읽을 수 없는 방향"으로 저장되는지 확인해야 한다.

- **📢 섹션 요약 비유**: 비밀 메모는 다시 읽을 수 있게 보관하는 게 아니라, 아예 원문을 못 보게 바꾸는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Password</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Salt</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Hash Function</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Stored Digest</div>
</div>
</div>



| 구성 요소 | 역할 |
| :-- | :-- |
| [Salt](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) | 같은 비밀번호의 해시를 다르게 함 |
| Hash | [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 변환 |
| Iteration / [KDF](/knowledge-base/studynote/09_security/03_network_security/144_hkdf_tls_1_3/) | 계산 비용 증가 |

비밀번호 저장에서 중요한 것은 복원 가능성이 아니라 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능성이다. 따라서 비교는 원문이 아니라 해시 결과로 해야 한다.

- **📢 섹션 요약 비유**: 원래 글을 숨기고, 비교할 수 있는 도장만 남겨 두는 셈이다.

---

## Ⅲ. 비교 및 연결

| 방식 | 특징 | 적합성 |
| :-- | :-- | :-- |
| Encryption | 복호화 가능 | 비밀번호 저장 부적합 |
| Hash + [Salt](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) | [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) | 권장 |
| Plain Text | 그대로 저장 | 금지 |

| 공격 | 대응 |
| :-- | :-- |
| [Rainbow Table](/knowledge-base/studynote/09_security/02_crypto/107_rainbow_table/) | [Salt](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) |
| [Brute Force](/knowledge-base/studynote/09_security/05_web_app_security/456_brute_force/) | 느린 [KDF](/knowledge-base/studynote/09_security/03_network_security/144_hkdf_tls_1_3/) |
| [Credential Stuffing](/knowledge-base/studynote/09_security/05_web_app_security/455_credential_stuffing/) | [MFA](/knowledge-base/studynote/09_security/11_iam_access_control/552_mfa/) / [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |

감리에서는 저장 방식만이 아니라, 해시 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 느린 KDF인지, [솔트](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)가 충분히 무작위인지도 확인해야 한다.

- **📢 섹션 요약 비유**: 같은 이름표를 쓰면 안 되고, 각자 다른 표식을 붙여야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 비밀번호를 암호화가 아닌 해시로 저장하는가?
2. 사용자마다 고유한 salt를 사용하는가?
3. 느린 KDF를 사용하는가?
4. 원문 재조회가 필요 없는 구조인가?
5. 재설정/[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 분리되어 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 비밀번호를 복호화 가능한 방식으로 저장하는 설계
- 모든 사용자에 같은 salt를 쓰는 설계
- 너무 빠른 해시를 쓰는 설계
- 감리 없이 [라이브러리](/knowledge-base/studynote/04_software_engineering/06_software_architecture/336_library_vs_framework/) 기본값만 믿는 설계

기술사 관점에서는 "암호화 저장"이라는 표현 자체를 경계해야 한다. 비밀번호는 복호화보다 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 중요하기 때문이다.

- **📢 섹션 요약 비유**: 열쇠를 다시 여는 게 아니라, 맞는지 확인만 하는 자물쇠다.

---

## Ⅴ. 기대효과 및 결론

올바른 해시와 [솔트](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)는 비밀번호 유출 사고의 피해를 크게 줄인다. 그래서 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 보안의 기본이다.

결론적으로 비밀번호는 암호화가 아니라 [단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 해시와 [솔트](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)로 보호해야 한다.

- **📢 섹션 요약 비유**: 비밀은 읽을 수 없게 보관하고, 맞는지만 확인하면 된다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Password</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Salt</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Hash / KDF</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Verification</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Plain Text</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Hash + Salt</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">KDF</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Password Security</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

비밀번호는 다시 꺼내 읽으면 안 돼요.  
대신 특별한 표식을 붙여서 확인만 해요.  
이게 해시와 [솔트](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 100 / 530

← **이전**: [65. 로그 및 감사 추적 (Audit Trail) - 위변조 방지 컴플라이언스 점검](/knowledge-base/studynote/11_design_supervision/01_audit_framework/065_audit_trail_worm_storage_compliance/)
**다음**: [66. 비밀번호 암호화 저장 방식 진단 (Password Hash and Salt Audit)](/knowledge-base/studynote/11_design_supervision/01_audit_framework/066_password_hash_salt_audit/) →

---
