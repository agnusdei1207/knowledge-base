+++
title = "428. 정보보호 구현 기법 비교 (Delta, Encryption, Hash, Key Stretching, Obfuscation)"
date = 2026-05-10

[taxonomies]
tags = ["studynote-design-supervision"]

[extra]
tags = ["studynote-design-supervision"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 델타, 암호, 해시, [키 스트레칭](/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/), [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/)는 모두 "[보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)"에 쓰이지만 각각 줄이려는 위험이 다르므로 목적별 구분이 먼저다.
> 2. **가치**: [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)은 암호, [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 해시, 패스워드 저장 강화는 [키 스트레칭](/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/), 코드 [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/) 저항은 [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/)처럼 역할을 분명히 나눌수록 설계 실수가 줄어든다.
> 3. **판단 포인트**: 델타와 [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/)는 단독 보안 통제가 아니며, 해시는 복호화 수단이 아니고, 패스워드 저장에는 암호화보다 해시+[솔트](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)+[키 스트레칭](/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/)이 우선이다.

---

## Ⅰ. 개요 및 필요성

이 주제는 서로 다른 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 기법을 한 번에 묶어 물을 때 자주 등장한다. 시험에서 중요한 것은 각 기법의 정의를 따로 외우는 것보다 <strong>무엇을 <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a>하려는가</strong>를 먼저 구분하는 것이다. 델타(Delta)는 변경분만 저장·전송하여 전체 원본 노출과 전송량을 줄이는 차등 처리이고, 암호(Encryption)는 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/)을, 해시(Hash)는 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을, [키 스트레칭](/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/)([Key Stretching](/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/))은 패스워드 대입 공격 저항성을, [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/)([Obfuscation](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/))는 코드 [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/) 비용 증가를 담당한다.

즉 같은 "[보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)"라도 대상과 효과가 다르다. 여기서 오류가 나면 패스워드를 복호화 가능한 형태로 저장하거나, [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/)만 해 놓고 서버 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 생략하는 식의 치명적 오해가 생긴다. 따라서 감리·설계 답안은 항상 **자산 → 위협 → 적합한 기법** 순으로 구성하는 것이 안전하다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">보호하려는 것 ──▶ 필요한 속성 ──▶ 선택 기법</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">변경분 전송 효율·노출 축소 Delta</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">비밀 데이터 기밀성 확보 Encryption</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 검증 무결성 확인 Hash</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">패스워드 저장 대입 공격 저항 Key Stretching</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">배포 코드 역공학 난이도 상승 Obfuscation</div></div>
</div>
</div>



이 그림은 기술 이름보다 먼저 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 속성을 정해야 올바른 통제 선택이 가능하다는 점을 보여 준다.

- **📢 섹션 요약 비유**: 우산, 자물쇠, 체온계, 금고가 모두 "안전"에 쓰이지만 비를 막는 도구와 도둑을 막는 도구가 다르듯, 보안 기법도 역할이 다르다.

---

## Ⅱ. 아키텍처 및 핵심 원리

핵심 원리는 간단하다. <strong>되돌릴 수 있어야 하는가, <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>만 하면 되는가, 계산 비용을 일부러 높여야 하는가, 코드 분석을 어렵게 해야 하는가</strong>를 먼저 판단하면 된다. 시험 답안에서는 각 기법의 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 목적과 한계를 함께 써야 고득점이 나온다.

| 기법 | [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 목적 | 시험 포인트 |
|:---|:---|:---|
| Delta | 변경분만 전송·저장해 효율과 노출 범위를 줄임 | 단독 보안 통제가 아니므로 암호화와 결합해야 한다 |
| Encryption | 평문을 암호문으로 바꿔 [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 확보 | 키 관리가 부실하면 알고리즘이 좋아도 무력화된다 |
| Hash | 입력의 고정 길이 요약값으로 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 복호화 개념이 없고 충돌 저항성이 중요하다 |
| [Key Stretching](/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/) | 패스워드 해시 계산 비용을 높여 대입 공격 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | [솔트](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)와 함께 써야 하며 PBKDF2, bcrypt, scrypt, Argon2가 대표적 |
| [Obfuscation](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/) | 코드 의미를 읽기 어렵게 만들어 [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/) 비용 증가 | 보안의 보조 수단이지 비밀 저장 수단은 아니다 |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Asset / Data / Code</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1) 변경 배포/백업 ──▶ Delta</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2) 저장·전송 비밀 ──▶ Encryption</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">3) 위변조 검증 ──▶ Hash / MAC</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">4) 패스워드 저장 ──▶ Salt + Key Stretching</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">5) 클라이언트 코드 ──▶ Obfuscation + 서버측 검증</div></div>
</div>
</div>



실무적으로는 이 기법들이 경쟁 관계가 아니라 **계층적으로 함께 쓰인다**. 예를 들어 모바일 앱은 소스 [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/)로 [정적 분석](/knowledge-base/studynote/04_software_engineering/06_software_architecture/331_static_analysis/) 난도를 높이고, 통신은 TLS로 암호화하며, 패스워드는 서버에서 [솔트](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)와 [키 스트레칭](/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/)을 적용해 저장한다. 각 층의 역할을 구분해 설명하는 것이 중요하다.

- **📢 섹션 요약 비유**: 성벽, 비밀문, 봉인, 두꺼운 자물쇠, 미로가 각각 다른 침입 경로를 막듯, 이 기법들은 막는 공격이 서로 다르다.

---

## Ⅲ. 비교 및 연결

이 다섯 기법은 모두 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 수단이지만, 복원 가능성·목적·적용 위치가 다르다. 따라서 "무엇이 더 강한가"보다 "어떤 문제에 쓰는가"로 비교해야 한다.

| 기법 | 복원 가능 여부 | 대표 예시 | 적합한 사용처 |
|:---|:---|:---|:---|
| Delta | 원본 기준으로 복원 가능 | delta patch, incremental [backup](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) | 대용량 배포, 변경분 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) |
| Encryption | 키가 있으면 복호화 가능 | [AES](/knowledge-base/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/), [RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/), [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) | 저장 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)·전송 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| Hash | 복원 불가 | SHA-256, [SHA-3](/knowledge-base/studynote/09_security/02_crypto/101_sha_3/) | [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 서명 전처리 |
| [Key Stretching](/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/) | 복원 불가(해시 기반) | bcrypt, scrypt, Argon2 | 패스워드 저장 강화 |
| [Obfuscation](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/) | 실행은 가능하나 이해를 어렵게 함 | [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/), 문자열 암호화 | 모바일 앱, 클라이언트 배포 코드 |

추가로 [HMAC](/knowledge-base/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/), 디지털 서명, 토큰 서명, 코드 서명과도 연결된다. 예를 들어 단순 해시만으로는 송신자 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)이 안 되므로 HMAC이나 전자서명을 써야 하고, [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/)만으로 키를 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)할 수 없으므로 중요한 비밀은 서버나 [HSM](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/475_hsm/) 쪽으로 빼는 것이 정석이다.

- **📢 섹션 요약 비유**: 봉투를 밀봉하는 것, 내용을 암호로 쓰는 것, 글자를 일부러 꼬는 것은 모두 다르듯 "숨김·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)·방해"는 구분해서 써야 한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 기술 이름보다 먼저 자산과 공격 시나리오를 정의해야 한다. 고객 비밀번호인지, 내부 설정값인지, 모바일 앱 코드인지에 따라 선택이 달라진다. 기술사 답안에서는 <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a>/<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a>/<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>/<a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/">역공학</a> 저항성</strong>을 기준으로 분류하고, 보조 통제와 한계를 함께 적는 것이 좋다.

### 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 대상이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 패스워드, 코드, 변경분 중 무엇인지 명확한가?
2. [기밀성](/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/) 확보가 목표라면 키 관리와 암호화 구간이 함께 설계되어 있는가?
3. 패스워드 저장에 단순 해시가 아니라 [솔트](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/)와 [키 스트레칭](/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/)이 적용되는가?
4. [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/)나 델타 처리에 과신하지 않고 서버측 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)·[무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 병행되는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 패스워드를 대칭키 암호화로 저장해 복호화 가능 상태로 두는 경우
- [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/)만 적용하고 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 키, 비밀값을 클라이언트 내부에 그대로 넣는 경우
- 델타 패치만 쓰면서 원본·변경분 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 생략하는 경우

- **📢 섹션 요약 비유**: 자물쇠를 달아 놓고 열쇠를 문 옆에 걸어 두면 소용없듯, 기법 선택보다 운영 방식과 조합이 더 중요하다.

---

## Ⅴ. 기대효과 및 결론

이들 기법을 목적별로 올바르게 조합하면 저장·전송·[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·배포 전 구간에서 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 강도를 체계적으로 높일 수 있다. 또한 감리 문서나 설계 답안에서 "왜 이 기술이 여기 들어갔는가"를 명확히 설명할 수 있어 설득력이 커진다.

결론은 단순하다. <strong>암호는 <a href="/knowledge-base/studynote/09_security/01_intro_principles/002_confidentiality/">기밀성</a>, 해시는 <a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a>, <a href="/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/">키 스트레칭</a>은 패스워드 <a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a>, <a href="/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/">난독화</a>는 <a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/">역공학</a> <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a>, 델타는 차등 처리 효율</strong>을 담당한다. 이 구분만 정확히 기억해도 시험에서 오답 가능성을 크게 줄일 수 있다.

- **📢 섹션 요약 비유**: 공구함에서 망치, 드라이버, 줄자, 자물쇠가 모두 필요하듯, 정보보호도 한 도구로 끝나는 것이 아니라 목적별 공구 조합으로 완성된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [Salt](/knowledge-base/studynote/03_network/13_network_security_basics/671_password_hash_salt_pbkdf2_bcrypt_argon2/) | [키 스트레칭](/knowledge-base/studynote/09_security/02_crypto/109_key_stretching/)과 결합해 동일 패스워드의 해시 중복을 막는다 |
| [HMAC](/knowledge-base/studynote/03_network/13_network_security_basics/674_hmac_hash_based_mac_ipsec/) | 해시만으로 부족한 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 기능을 보완한다 |
| [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) | 암호화가 실제 통신 구간에서 구현되는 대표 사례 |
| [Code Signing](/knowledge-base/studynote/09_security/04_endpoint_security/188_code_signing_software_authentication/) | [난독화](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/)와 달리 배포 코드의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)과 출처를 보장한다 |
| Incremental [Backup](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) | Delta 기법이 활용되는 대표 운영 시나리오 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">자산 식별</div>
<div class="kb-diagram-tree-item" style="--depth:2">비밀 보호 ▶ Encryption</div>
<div class="kb-diagram-tree-item" style="--depth:2">위변조 검증 ▶ Hash / HMAC</div>
<div class="kb-diagram-tree-item" style="--depth:2">패스워드 저장 ▶ Salt + Key Stretching</div>
<div class="kb-diagram-tree-item" style="--depth:2">코드 역공학 방어 ─▶ Obfuscation</div>
<div class="kb-diagram-tree-item" style="--depth:2">변경분 전송 최적화 ▶ Delta</div>
</div>
</div>



이 흐름은 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 대상에 따라 통제 수단이 갈라진다는 점을 한눈에 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 비밀 편지는 암호로 쓰고, 편지가 바뀌었는지는 도장을 찍어 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고, 장난감 설명서는 일부러 어렵게 숨길 수 있어요.
2. 또 비밀번호는 쉽게 맞히지 못하게 더 오래 계산하게 만들어요.
3. 이렇게 보안 도구들은 모두 비슷해 보여도 맡은 일이 서로 달라요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 506 / 530

← **이전**: [427. 소프트웨어 개발비 산정과 기능점수 (Simple/Detailed Estimation, Function Point)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/427_metric/)
**다음**: [429. 마이크로 세그멘테이션 기반 제로 트러스트 (Microsegmentation, Zero Trust)](/knowledge-base/studynote/11_design_supervision/06_exam_summary/429_process/) →

---
