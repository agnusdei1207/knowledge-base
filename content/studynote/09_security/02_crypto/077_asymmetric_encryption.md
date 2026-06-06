---
title: "077. Asymmetric Encryption"
date: "2026-03-26"
description: "공개키와 개인키 쌍을 사용하여 암호화와 복호화를 수행하는 공개키 암호 시스템"
tags:
  - "studynote-software-engineering"
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 비대칭키 암호는 공개키로 암호화/[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하고 개인키로 복호화/서명하는 키 쌍 기반 구조다.
> 2. **가치**: PKC (Public-[Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) [Cryptography](/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/))는 키 배포 문제를 해결하고, 디지털 서명까지 함께 제공한다.
> 3. **판단 포인트**: 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 비대칭키로 직접 처리하지 말고, 하이브리드 방식으로 세션키만 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하는 것이 일반적이다.

---

## Ⅰ. 개요 및 필요성
[대칭키 암호](/studynote/09_security/02_crypto/076_symmetric_encryption/)는 빠르지만 키를 안전하게 나눠 가져야 한다는 문제가 있다. 처음 만나는 두 주체가 비밀키를 어떻게 공유할지 모르면, 암호화 자체가 시작되지 않는다. 비대칭키 암호는 이 키 배포 문제를 해결하기 위해 등장했다.

공개키를 널리 배포하고 개인키를 비밀로 유지하면, 누구나 암호화는 할 수 있지만 복호화는 소유자만 할 수 있다. 동시에 전자서명으로 "누가 보냈는지"도 증명할 수 있다.

📢 섹션 요약 비유: 누구나 넣을 수 있지만 열쇠를 가진 사람만 열 수 있는 우편함과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리
키 쌍은 공개키와 개인키로 나뉜다. 공개키는 배포용, 개인키는 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)용이다. 암호화와 서명은 방향이 서로 반대다. 암호화는 공개키로 시작해 개인키로 풀고, 서명은 개인키로 만들고 공개키로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한다.

| 항목 | 공개키 | 개인키 |
| :--- | :--- | :--- |
| 암호화 | 가능 | 복호화 필요 |
| 서명 | [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| 배포 | 널리 공개 | 엄격히 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| 역할 | 신뢰의 출발점 | 비밀의 근원 |

```text
송신자 -- 공개키로 암호화 ---> 수신자
   |                           |
   +-- 개인키는 숨김           +-- 개인키로 복호화

서명: 개인키로 생성 ---> 공개키로 검증
```

실제 시스템에서는 [PKI](/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) ([Public Key Infrastructure](/studynote/09_security/uncategorized/1080_pki_public_key_infrastructure_ca_ra_certificate/))와 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 공개키의 진짜 주인을 증명한다. [RSA](/studynote/09_security/03_network_security/110_rsa/) ([Rivest-Shamir-Adleman](/studynote/09_security/03_network_security/110_rsa/)), [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) ([Elliptic Curve Cryptography](/studynote/09_security/03_network_security/119_ecc_elliptic_curve_cryptography/)) 같은 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 서로 다른 수학적 기반을 쓰지만, 키 쌍 구조라는 큰 원리는 같다.

📢 섹션 요약 비유: 누구나 볼 수 있는 자물쇠 설명서와, 절대 남에게 주면 안 되는 진짜 열쇠가 따로 있는 구조다.

---

## Ⅲ. 비교 및 연결
대칭키는 빠르고 간단하지만 키 교환이 어렵고, 비대칭키는 키 교환과 신뢰 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)에 강하지만 느리다. 그래서 [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) (Transport Layer [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) 같은 실제 프로토콜은 비대칭키로 세션키를 주고받고, 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 대칭키로 암호화하는 하이브리드 방식을 쓴다.

| 구분 | [대칭키 암호](/studynote/09_security/02_crypto/076_symmetric_encryption/) | 비대칭키 암호 |
| :--- | :--- | :--- |
| 속도 | 빠름 | 느림 |
| 키 관리 | 공유가 어려움 | 공개/비공개 분리 |
| 대표 용도 | 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 암호화 | 키 교환, 서명 |

해시(hash)는 암호화가 아니라 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 요약값이고, 디지털 서명은 해시값에 개인키 서명을 더해 진위를 보장한다. 즉 암호화, 해시, 서명은 겹쳐 보이지만 목적이 다르다.

📢 섹션 요약 비유: 대칭키는 같은 열쇠를 나눠 쓰는 문, 비대칭키는 자물쇠는 공개하고 열쇠는 숨기는 문이다.

---

## Ⅳ. 실무 적용 및 기술사 판단
실무에서는 비대칭키를 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 암호화의 주역"으로 쓰기보다, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)·서명·세션키 교환의 주역으로 쓴다. 개인키 유출은 곧 신뢰 붕괴이므로, [HSM](/studynote/01_computer_architecture/14_hardware_security_trends/475_hsm/) ([Hardware Security Module](/studynote/09_security/03_network_security/157_hsm_hardware_security_module/))이나 키 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 정책이 중요하다.

- 채택: 키 배포가 어렵고, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)과 서명이 필요한 환경
- 회피: 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 비대칭키로 직접 암호화하는 경우
- [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
  1. 개인키를 안전하게 저장하고 있는가?
  2. [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서와 [PKI](/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) ([Public Key Infrastructure](/studynote/09_security/uncategorized/1080_pki_public_key_infrastructure_ca_ra_certificate/))가 올바르게 운영되는가?
  3. 대칭키와 하이브리드 구조로 성능을 확보했는가?
  4. [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 수명과 키 길이 정책이 최신 위협에 맞는가?

비대칭키 암호는 편리하지만, 느리기 때문에 역할을 분리해서 써야 한다. "모든 것을 비대칭으로"는 좋은 설계가 아니다.

📢 섹션 요약 비유: 손님은 누구나 들일 수 있지만, 금고 열쇠는 주인만 가져야 하는 집이다.

---

## Ⅴ. 기대효과 및 결론
비대칭키 암호는 키 배포 문제를 풀고, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)과 [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 증명을 가능하게 한다. 결국 이 개념은 "공개는 넓게, 비밀은 좁게" 유지하는 보안 구조로 기억하면 된다.

📢 섹션 요약 비유: 누구나 우편함을 볼 수 있어도, 열어 보는 사람은 한 명뿐이어야 한다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| PKC (Public-[Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) [Cryptography](/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/)) | 공개키 암호 체계 |
| [PKI](/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) ([Public Key Infrastructure](/studynote/09_security/uncategorized/1080_pki_public_key_infrastructure_ca_ra_certificate/)) | 공개키 신뢰 관리 |
| [RSA](/studynote/09_security/03_network_security/110_rsa/) ([Rivest-Shamir-Adleman](/studynote/09_security/03_network_security/110_rsa/)) | 대표적인 공개키 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) ([Elliptic Curve Cryptography](/studynote/09_security/03_network_security/119_ecc_elliptic_curve_cryptography/)) | 효율적인 공개키 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) |
| [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) (Transport Layer [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) | 하이브리드 암호 사용 예 |

### 📈 관련 키워드 및 발전 흐름도

```text
키 배포 문제
    |
    v
비대칭키 암호(PKC)
    |
    v
PKI (Public Key Infrastructure) / 인증서
    |
    v
하이브리드 암호(TLS)
    |
    v
안전한 통신과 전자서명
```

### 👶 어린이를 위한 3줄 비유 설명

1. 누구나 편지를 넣을 수 있는 상자가 있어요.
2. 하지만 상자를 여는 열쇠는 주인만 가지고 있어요.
3. 그래서 모르는 사람이 함부로 내용을 볼 수 없어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 77 / 1108

<- **이전**: [76. 대칭키 암호 (Symmetric Encryption) — 동일한 키로 암호화/복호화](/studynote/09_security/02_crypto/076_symmetric_encryption/)
**다음**: [78. 하이브리드 암호 — 대칭+비대칭 결합 (키 교환+데이터 암호화)](/studynote/09_security/02_crypto/078_hybrid_encryption/) ->

---
