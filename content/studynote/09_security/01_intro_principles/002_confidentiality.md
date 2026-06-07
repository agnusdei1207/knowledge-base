---
title: "Confidentiality"
date: "2023-10-24"
tags:
  - "security"
  - "studynote-security"
weight: 2
---
#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기밀성은 '알 권리([Need-to-Know](/studynote/09_security/01_intro_principles/013_need_to_know/))'가 없는 주체로부터 정보 자산을 숨기고 유출을 차단하는 정보보안의 1차 방어선이다.
> 2. **가치**: [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/), 기업 영업비밀, 국가 기밀 등 민감 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)함으로써 컴플라이언스 준수와 비즈니스 신뢰도를 확보한다.
> 3. **융합**: 단순한 암호화를 넘어, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 생명주기(생성-저장-전송-사용-폐기) 전반에 걸쳐 [IAM](/studynote/09_security/11_iam_access_control/526_iam/)(신원 및 접근 관리) 및 [DRM](/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/)(디지털 [저작권](/studynote/04_software_engineering/09_cloud_native_ai_architecture/583_ai_code_license_security_threats/) 관리)과 융합되어 구현된다.

---

### Ⅰ. 개요 및 필요성 ([Context](/studynote/02_operating_system/01_overview_architecture/033_context/) & Necessity)

기밀성 (Confidentiality)은 정보보안 3요소 중 가장 직관적이면서도 역사적으로 오래된 개념이다. 군사 및 외교 통신에서 출발한 기밀성은 현대에 이르러 고객의 [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)와 기업의 핵심 기술 자산을 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하는 필수적인 법적, 윤리적 의무로 자리 잡았다.

네트워크가 폐쇄적이었던 과거에는 물리적인 출입 통제만으로도 기밀성 유지가 가능했다. 그러나 클라우드 컴퓨팅과 원격 근무가 일상화된 현대 환경에서는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 국경과 네트워크 경계를 자유롭게 넘나든다. 이로 인해 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 담고 있는 물리적 매체를 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하는 것 이상으로, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체에 논리적인 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)막을 씌우는 암호화와 엄격한 신원 기반의 접근 제어가 필수적으로 요구된다.

다음 도식은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 상태([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [State](/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/))에 따라 기밀성을 위협하는 요인과 방어 메커니즘이 어떻게 달라지는지 보여준다.

```text
+----------------- Data States -----------------+
|                                               |
|  [저장 중 (Data at Rest)]                     |
|  위협: 디스크 도난, DB 해킹, 백업 유출        |
|  방어: 디스크 암호화(TDE), 접근 통제(ACL)     |
|           |                                   |
|           v                                   |
|  [전송 중 (Data in Transit)]                  |
|  위협: 패킷 스니핑, 중간자 공격(MITM)         |
|  방어: TLS/SSL 암호화, IPsec VPN              |
|           |                                   |
|           v                                   |
|  [사용 중 (Data in Use)]                      |
|  위협: 메모리 덤프, 화면 캡처, 무단 복제      |
|  방어: 동형 암호화, TEE(Secure Enclave), DRM  |
+-----------------------------------------------+
```

이 그림의 핵심은 기밀성이 단일한 솔루션으로 달성되는 것이 아니라, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 머무르고 이동하는 모든 생명주기 상태에 맞춰 각기 다른 기술이 톱니바퀴처럼 맞물려야 한다는 점이다. 전송 구간을 완벽히 암호화하더라도 메모리에 평문으로 올라온 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 탈취당하면 기밀성은 즉시 파괴된다. 따라서 실무에서는 모든 상태의 취약점을 분석하고 [End-to-End](/studynote/03_network/08_transport_layer/401_transport_layer_role_end_to_end_multiplexing/) [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 체계를 설계해야 한다.

**📢 섹션 요약 비유**: 마치 현금을 운반할 때, 은행 금고(저장), 방탄 현금수송차(전송), 그리고 [ATM](/studynote/03_network/05_lan_wan_l2_devices/272_atm_asynchronous_transfer_mode_53byte_cell/) 기기 내부의 특수 카세트(사용)가 모두 갖춰져야만 돈을 안전하게 지킬 수 있는 것과 같습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

기밀성을 보장하는 아키텍처는 크게 '수학적 [난독화](/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/)(암호화)'와 '논리적 격리(접근 제어)'라는 두 가지 축으로 구성된다.

| 구성 요소 | 역할 및 목적 | 내부 동작 메커니즘 | 핵심 기술/[프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |
|:---|:---|:---|:---|
| <strong>접근 제어 (<a href="/studynote/02_operating_system/09_file_system/547_access_control_rwx/">Access Control</a>)</strong> | 인가된 사용자만 자원에 접근하도록 격리 | 주체(Subject)의 신원을 확인하고 객체(Object)에 대한 권한 매트릭스 검사 | [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/), [ABAC](/studynote/09_security/11_iam_access_control/572_abac/), [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/), DAC |
| <strong><a href="/studynote/03_network/13_network_security_basics/653_symmetric_key_cryptography_fast_speed/">대칭키 암호화</a> (Symmetric)</strong> | 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 빠른 기밀성 확보 | 동일한 키로 평문을 암호문으로, 암호문을 평문으로 변환 | [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/)-256, ChaCha20 |
| <strong><a href="/studynote/09_security/02_crypto/077_asymmetric_encryption/">비대칭키 암호</a>화 (Asymmetric)</strong> | 안전한 키 교환 및 신원 증명 | 공개키로 암호화하고 개인키로만 복호화 (수학적 일방향성 활용) | [RSA](/studynote/09_security/03_network_security/110_rsa/), [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/) (Elliptic Curve) |
| <strong><a href="/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/">DRM</a> (Digital Rights Mgt.)</strong> | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 외부로 유출된 이후에도 기밀성 통제 | 문서 자체를 래핑(Wrapping)하여 열람, 인쇄, 캡처 권한을 동적으로 제어 | Enterprise [DRM](/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/), [워터마크](/studynote/16_bigdata/04_streaming/085_watermark/) |
| <strong><a href="/studynote/09_security/16_data_privacy/819_data_masking/">데이터 마스킹</a> (Masking)</strong> | 비인가자에게 민감 정보의 일부만 노출 | 정규표현식을 통해 주민번호, 카드번호 등의 일부를 '*'로 치환 | Dynamic [Data Masking](/studynote/09_security/16_data_privacy/819_data_masking/) |

다음은 클라이언트가 기밀 문서에 접근할 때, 접근 제어와 암호화가 결합되어 동작하는 순차 흐름도이다.

```text
[Client]                      [IAM Server]                 [File Server]
   |                               |                            |
   +- 1. 인증 요청 (ID/PW) ------->|                            |
   |                               |                            |
   |<- 2. 세션 토큰 & 공개키 발급 -+                            |
   |                               |                            |
   +- 3. 데이터 요청 (토큰 첨부) --+--------------------------->|
   |                               |                            |
   |                               | <- 4. 토큰 권한 검증 (RBAC)+
   |                               |                            |
   |                               |    [권한 확인 완료]        |
   |                               |                            |
   |                               |    5. 대칭키로 파일 암호화 |
   |<- 6. 암호화된 파일 전송 ------+----------------------------+
   |                               |                            |
   | 7. 클라이언트 개인키로 복호화 |                            |
```

이 흐름도의 핵심은 암호화가 단순히 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 숨기는 데 그치지 않고 [IAM](/studynote/09_security/11_iam_access_control/526_iam/)([신원 관리](/studynote/09_security/11_iam_access_control/527_identity_management/)) 체계와 강하게 결합되어 있다는 점이다. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버는 무조건 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 보내는 것이 아니라, IAM을 통해 주체의 '알 권리'를 먼저 검증한다(논리적 격리). 검증이 완료된 후에도 전송 중 탈취를 막기 위해 암호화(수학적 [난독화](/studynote/04_software_engineering/08_security_compliance_devsecops/528_obfuscation_anti_debugging_mobile/))를 수행한다. 실무에서는 이러한 이중 통제 구조가 레이턴시를 발생시키므로, 대칭키와 비대칭키를 결합한 하이브리드 암호 방식을 사용하여 성능과 보안을 모두 잡는다.

**📢 섹션 요약 비유**: 건물에 들어갈 때 경비원이 신분증을 검사하는 것(접근 제어)과, 회의실 안에서 외국어로만 대화하여 도청을 막는 것(암호화)을 동시에 적용하는 보안 시스템입니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

기밀성을 구현하는 핵심 기술인 [암호화 알고리즘](/studynote/04_software_engineering/08_security_compliance_devsecops/504_cryptography_algorithms_aes_rsa_sha/)과 접근 제어 모델을 다각도로 비교 분석한다.

<strong>1. <a href="/studynote/04_software_engineering/08_security_compliance_devsecops/504_cryptography_algorithms_aes_rsa_sha/">암호화 알고리즘</a> 방식 비교</strong>

| 비교 항목 | [대칭키 암호화](/studynote/03_network/13_network_security_basics/653_symmetric_key_cryptography_fast_speed/) (Symmetric) | [비대칭키 암호](/studynote/09_security/02_crypto/077_asymmetric_encryption/)화 (Asymmetric) | 실무 판단 포인트 |
|:---|:---|:---|:---|
| **키의 구조** | 암호화 ↔ 복호화 키 동일 | 공개키(암호화) ≠ 개인키(복호화) | 키 관리의 복잡도 여부 |
| **처리 속도** | 매우 빠름 (비대칭키 대비 100~1000배) | 매우 느림 (복잡한 수학 연산 필요) | 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 가능성 |
| **키 분배 문제** | 키를 안전하게 전달하기 매우 어려움 | 공개키는 누구나 열람 가능하므로 쉬움 | 원격지와의 안전한 채널 형성 |
| <strong>주요 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong> | [AES](/studynote/03_network/13_network_security_basics/656_aes_advanced_encryption_standard_rijndael/), [DES](/studynote/09_security/02_crypto/086_des_data_encryption_standard/), ARIA, ChaCha20 | [RSA](/studynote/09_security/03_network_security/110_rsa/), [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/), ElGamal | 암호화 강도 및 규제 표준 |

대규모 시스템에서는 두 방식의 장점을 섞어, '비대칭키를 이용해 대칭키를 안전하게 교환하고, 실제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 대칭키로 빠르게 암호화'하는 하이브리드 방식을 사용한다(예: [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/)/SSL).

<strong>2. 접근 제어 모델(<a href="/studynote/02_operating_system/09_file_system/547_access_control_rwx/">Access Control</a>) 비교 매트릭스</strong>

```text
+------------+-----------------------------+---------------------------+
| 통제 모델  | 권한 부여 기준 및 특징      | 운영 복잡도 및 적용 환경  |
+------------+-----------------------------+---------------------------+
| DAC (임의) | 객체의 '소유자'가 권한 결정 | 복잡도 낮음. 유닉스 파일  |
|            | (Read/Write/Execute) 부여   | 시스템, 소규모 조직에 적합|
+------------+-----------------------------+---------------------------+
| MAC (강제) | 시스템의 보안 레이블(등급)과| 복잡도 매우 높음. 군사,   |
|            | 주체의 신원 등급을 강제 비교| 정부 등 극도의 기밀성 요구|
+------------+-----------------------------+---------------------------+
| RBAC (역할)| 주체가 속한 '역할(Role)'에  | 복잡도 중간. 일반적인 기업|
|            | 따라 권한을 일괄 부여/회수  | 전산망, 대규모 권한 관리에|
|            |                             | 가장 널리 쓰이는 표준     |
+------------+-----------------------------+---------------------------+
```

이 매트릭스의 핵심은 접근 제어 모델이 '유연성'과 '중앙 통제력' 사이의 트레이드오프를 가진다는 점이다. DAC는 사용자에게 자율성을 주지만 정보 유출 통제가 어렵고, MAC는 완벽한 기밀성을 제공하지만 업무 효율이 극도로 저하된다. 따라서 실무에서는 부서 이동이나 퇴사가 잦은 기업 환경의 특성을 반영하여 유지보수가 용이한 [RBAC](/studynote/09_security/11_iam_access_control/569_rbac/)(역할 기반 접근 제어)를 기본으로 채택하고, 극비 문서에 대해서만 제한적으로 [MAC](/studynote/03_network/13_network_security_basics/673_mac_message_authentication_code/) 모델을 혼용하는 전략을 취한다.

**📢 섹션 요약 비유**: 대칭키/비대칭키의 혼용은 무거운 짐을 실은 화물차(대칭키)를 목적지까지 보내기 위해 먼저 튼튼한 다리(비대칭키)를 놓는 것과 같고, 접근 제어 모델은 회사의 직급 체계에 따라 출입증 색깔을 다르게 발급하는 것과 같습니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 ([Strategy](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) & Decision)

실무에서 기밀성 통제를 적용할 때 흔히 마주하는 문제 상황과 판단 기준은 다음과 같다.

1. **시나리오 1: 퇴사자에 의한 영업비밀 유출 방지**
   - **상황**: 핵심 개발자가 퇴사 시 로컬 PC에 저장된 도면과 코드를 USB로 빼돌리려 한다.
   - **판단**: 네트워크 통제나 단순 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버 암호화([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) at [Rest](/studynote/07_enterprise_systems/03_eai_esb_msa/156_rest_representational_state_transfer/))만으로는 로컬로 다운로드된 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 막을 수 없다. 이 경우 문서 자체가 실행되는 환경을 통제하는 <strong>Enterprise <a href="/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/">DRM</a></strong>을 도입해야 한다. DRM은 문서를 암호화하고, 열람 시 라이선스 서버와 실시간 통신하여 권한(퇴사자 계정 정지 여부)을 확인하므로 오프라인 유출을 무력화한다.

2. <strong>시나리오 2: 클라우드 환경에서의 암호화 키 관리 (<a href="/studynote/07_enterprise_systems/02_erp_systems/127_kms_knowledge_management_system/">KMS</a>)</strong>
   - **상황**: [퍼블릭 클라우드](/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)(AWS, Azure)에 민감 고객 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 저장해야 한다.
   - **판단**: 클라우드 제공자가 제공하는 기본 암호화(SSE-S3)는 편리하지만, 클라우드 관리자가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 볼 수 있는 잠재적 위험이 있다. 진정한 기밀성을 확보하려면 기업이 직접 암호화 키를 생성하고 관리하는 <strong><a href="/studynote/09_security/20_extra_exam_prep/1014_byok_bring_your_own_key/">BYOK</a> (Bring Your Own <a href="/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a>)</strong> 또는 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) HSM과 연동하는 구조를 채택해야 한다.

다음은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출 사고 발생 시, 암호화와 키 관리 실패가 어떻게 연쇄적인 재앙으로 이어지는지 보여주는 장애 전파도다.

```text
[데이터베이스 탈취 (DB Dump)]
          |
          +- (데이터 평문 저장 시) -------> [즉각적인 대규모 기밀성 파괴]
          |
          +- (데이터 암호화 저장 시)
                   |
                   v
          [해커의 암호화 키 탐색]
                   |
                   +- (키가 하드코딩/동일 서버 존재) -> [키 탈취 및 복호화 성공] -> 기밀성 파괴
                   |
                   +- (KMS/HSM으로 망 분리 보관) ----> [복호화 실패] -> 기밀성 방어 성공!
```

이 전파도의 핵심은 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 암호화했다"는 사실 자체보다 "암호화 키를 어떻게 물리적/논리적으로 분리하여 보관했는가"가 기밀성의 최종 승패를 가른다는 점이다. 소스코드나 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 암호화 키를 평문으로 하드코딩하는 안티패턴은 실무에서 가장 흔하게 발생하는 치명적 결함이다. 따라서 실무 아키텍처는 반드시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장소와 키 관리 시스템([KMS](/studynote/07_enterprise_systems/02_erp_systems/127_kms_knowledge_management_system/))의 권한 및 네트워크를 분리하여 설계해야 한다.

**📢 섹션 요약 비유**: 자물쇠로 금고를 아무리 단단히 잠가도(암호화), 그 자물쇠의 열쇠(키)를 금고 바로 위 화분에 숨겨둔다면(하드코딩) 도둑을 막을 수 없는 이치와 같습니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

철저한 기밀성 통제는 기업의 평판을 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/)하고 규제 기관의 철퇴를 피하는 핵심 장치다.

| 기대효과 구분 | 단순 비밀번호 의존 환경 | 강력한 기밀성 아키텍처 (암호화+[DRM](/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/)) | 실질적 가치 |
|:---|:---|:---|:---|
| **정보 유출 대응** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 탈취 시 100% 정보 노출 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 탈취되어도 해독 불가 | 치명적 평판 하락 및 배상금 방어 |
| **규제 컴플라이언스**| [개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/) 위반 (과태료 대상) | 안전한 암호화 조치로 면책 사유 충족 | 법적 [리스크](/studynote/11_design_supervision/02_architecture_principles/096_risk_non_risk_architecture_evaluation_flaws/) [제로화](/studynote/01_computer_architecture/15_advanced_topics/784_zeroization_circuit/) |
| **비즈니스 협업** | 외부 파트너와 자료 공유 기피 | DRM을 통한 뷰어 권한만 제어하여 공유 | 안전한 파트너 생태계 확장 |

미래의 기밀성 기술은 양자 컴퓨터의 등장이라는 거대한 위협에 직면해 있다. 양자 컴퓨터의 쇼어(Shor) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 현재 널리 쓰이는 [비대칭키 암호](/studynote/09_security/02_crypto/077_asymmetric_encryption/)([RSA](/studynote/09_security/03_network_security/110_rsa/), [ECC](/studynote/01_computer_architecture/15_advanced_topics/554_ecc_circuit/))를 단시간에 무력화할 수 있다. 이에 대응하기 위해 국제 표준화 기구인 NIST는 <strong><a href="/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/">양자 내성 암호</a>(<a href="/studynote/12_it_management/05_security_compliance/992_quantum_computing_pqc_transition/">PQC</a>: <a href="/studynote/14_data_engineering/04_mlops/183_post_quantum_cryptography_key_transition/">Post-Quantum Cryptography</a>)</strong> 표준을 제정하고 있다.

더불어, 암호화된 상태 그대로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 연산할 수 있는 <strong>동형 암호화(<a href="/studynote/09_security/20_extra_exam_prep/1098_homomorphic_encryption/">Homomorphic Encryption</a>)</strong> 기술이 실용화 단계에 접어들고 있다. 이 기술이 보편화되면 클라우드 환경에서 '사용 중인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [in Use](/studynote/04_software_engineering/10_trends_pm_quality/694_confidential_computing_data_in_use/))'의 기밀성 문제를 완벽히 해결하여 정보보안의 패러다임을 바꿀 것이다.

**📢 섹션 요약 비유**: 기존의 기밀성이 비밀 문서를 금고에 넣고 문을 닫는 것이었다면, 미래의 기밀성(동형 암호화)은 투명하지 않은 마법의 상자 안에서 손만 집어넣어 문서를 편집하고 꺼내는 완벽한 마술과 같습니다.

---

### 📌 관련 개념 맵 ([Knowledge Graph](/studynote/14_data_engineering/03_ml_dl_llm/160_knowledge_graph_graphrag_integration/))
- <strong>접근 제어 (<a href="/studynote/02_operating_system/09_file_system/547_access_control_rwx/">Access Control</a>)</strong> | 주체의 권한을 확인하여 기밀성 훼손 시도를 사전에 차단하는 관문
- <strong><a href="/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/">암호학</a> (<a href="/studynote/03_network/13_network_security_basics/652_cryptography_concept_encryption_decryption/">Cryptography</a>)</strong> | 기밀성을 보장하는 가장 강력한 수학적 도구이자 엔진
- <strong><a href="/studynote/07_enterprise_systems/02_erp_systems/127_kms_knowledge_management_system/">KMS</a> (<a href="/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a> <a href="/studynote/12_it_management/05_security_compliance/1013_management/">Management</a> System)</strong> | 암호화된 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 생살여탈권을 쥔 암호화 키의 생명주기를 관리하는 시스템
- <strong><a href="/studynote/12_it_management/03_ea_isp/903_drm_data_reference_model_standard/">DRM</a> (Digital Rights <a href="/studynote/12_it_management/05_security_compliance/1013_management/">Management</a>)</strong> | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 조직 밖을 벗어난 이후에도 기밀성 통제력을 유지하는 기술
- <strong><a href="/studynote/09_security/16_data_privacy/783_pipa_korea/">개인정보보호법</a> (Privacy Law)</strong> | 조직이 기밀성 통제를 강제적으로 구현해야 하는 강력한 법적 근거

### 📈 관련 키워드 및 발전 흐름도

```text
[접근 제어 (Access Control)]
    |
    v
[암호학 (Cryptography)]
    |
    v
[KMS (Key Management System)]
    |
    v
[DRM (Digital Rights Management)]
    |
    v
[개인정보보호법 (Privacy Law)]
```

이 흐름도는 접근 제어 ([Access Control](/studynote/02_operating_system/09_file_system/547_access_control_rwx/))에서 출발해 [개인정보보호법](/studynote/09_security/16_data_privacy/783_pipa_korea/) (Privacy Law)까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명
1. **기밀성**: 내 비밀 일기장을 허락받은 베프들만 볼 수 있게 하는 원칙이에요.
2. **원리**: 일기장을 보려면 암호(접근제어)를 대야 하고, 일기 내용도 외계어(암호화)로 적혀 있어서 남들은 봐도 모르게 만들어요.
3. **효과**: 일기장을 누가 훔쳐가도 외계어를 해독할 수 없으니까 내 비밀이 영원히 안전하게 지켜진답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 2 / 1108

<- **이전**: [1. 정보보안 3요소 — CIA (기밀성·무결성·가용성)](/studynote/09_security/01_intro_principles/001_cia_triad/)
**다음**: [3. 무결성 (Integrity) — 해시, 전자서명, MAC, HMAC, 체크섬](/studynote/09_security/01_intro_principles/003_integrity/) ->

---
