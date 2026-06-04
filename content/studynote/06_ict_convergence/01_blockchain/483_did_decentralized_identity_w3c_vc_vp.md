+++
title = "483. 탈중앙화 신원: DID, VC, VP W3C 표준 (Decentralized Identity: DID, VC, VP)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/)(Decentralized Identity, [탈중앙화](/knowledge-base/studynote/06_ict_convergence/01_blockchain/010_decentralization/) 신원)는 중앙 서버 없이 개인이 자신의 신원을 <strong>자기 주권(Self-Sovereign Identity, SSI)</strong>으로 관리하는 W3C 표준 기술이다.
> 2. **가치**: VC(Verifiable Credential, [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능 자격증명)는 Issuer(발급자)->Holder(보유자)->Verifier([검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자) 신뢰 삼각형으로 <strong>중앙 서버 조회 없이 오프라인 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong>이 가능한 디지털 자격증이다.
> 3. **판단 포인트**: [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) Document의 공개키(Public [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))와 [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) Method(체인별 등록 방식)가 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)의 핵심 요소이며, [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)([MyData](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/))·모바일 신분증과의 연계가 실무 적용의 핵심이다.

---

## Ⅰ. 개요 및 필요성

### 중앙화 신원 관리의 문제

현재 디지털 신원 시스템: Google·Facebook 계정, 주민번호 -> 중앙 기관이 신원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보유 -> 해킹, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 종료, [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 판매 위험. 2020년 Facebook 5억 명 정보 유출 사례.

SSI(Self-Sovereign Identity) 원칙:
- 개인이 자신의 신원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 **직접 소유·관리**
- 필요한 속성만 선택적 공개(Selective Disclosure)
- 특정 기업·기관에 종속 없음

- **📢 섹션 요약 비유**: — "현재는 여권사무소(Google)가 내 신분증을 보관하고 필요할 때 빌려주는 방식, DID는 내가 직접 신분증을 들고 다니며 필요한 정보만 보여주는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) 시스템 전체 흐름

```
+----------------------------------------------------------+
|            DID/VC/VP 신뢰 삼각형                          |
|                                                          |
|  Issuer (발급자)                                         |
|  예: 대학교, 정부, 병원                                   |
|       | VC 발급 (서명+메타데이터)                         |
|       v                                                  |
|  Holder (보유자) <--> DID 지갑 (Wallet)                    |
|  예: 개인 사용자       DID Document 저장                   |
|       | VP 생성 (필요한 속성만 선택)                      |
|       v                                                  |
|  Verifier (검증자)                                       |
|  예: 취업 회사, 공항                                      |
|       | ① VP의 서명 검증                                 |
|       v ② DID Registry에서 공개키 조회                   |
|  DID Registry (블록체인 / 분산 저장)                      |
+----------------------------------------------------------+
```

### 핵심 구성 요소 비교

| 구성 요소 | 설명 | 예시 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/">DID</a></strong> | 전 세계 고유 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/), URI 형식 | `did:ethr:0x1234...` |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/">DID</a> <a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/">Document</a></strong> | [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) 주체의 공개키·[인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)방법·[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 정의 | JSON-LD 형식 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/">DID</a> Method</strong> | 특정 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)/시스템에 [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) 등록 방식 | [did](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/):ethr, [did](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/):web, [did](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/):ion |
| **VC** | 발급자 서명이 포함된 디지털 자격증 | 대학 졸업증명서 |
| **VP** | Holder가 선택적으로 VC 속성을 제출 | 나이만 공개하는 성인 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) |

- **📢 섹션 요약 비유**: — "VC는 학교가 발급한 디지털 성적표, VP는 그 성적표에서 '수학 점수만 꺼내 보여주는 것', DID는 그 성적표를 찾아갈 수 있는 고유 주소다.

---

## Ⅲ. 비교 및 연결

### 중앙화 신원 vs [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) 비교

| 항목 | 중앙화 신원 | [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/)/SSI |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 위치</strong> | 기업 서버 | 개인 지갑 |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 방식</strong> | 서버 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출 | 공개키 서명 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| <strong>오프라인 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a></strong> | 불가 | 가능 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/">단일 장애점</a></strong> | 있음 | 없음 |
| **선택적 공개** | 제한적 | 완전 지원 |

### [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)([MyData](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/))와의 연계

[마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/): 개인이 자신의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(의료·금융·공공)를 직접 제3자 기관에 제공하는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/). DID가 신원 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 역할, VC가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근 권한 증명 역할 담당.

### 실제 적용 사례

1. **모바일 운전면허증**: iOS/Android 지갑 기반 [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/), 경찰 앱으로 VP [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)
2. **학위 증명**: MIT Digital Diploma (Blockcerts), 취업 시 즉시 제출·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)
3. **코로나 백신 증명서**: EU DGCA(Digital Green Certificate), 여권 없이 QR로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)
4. **금융 KYC**: [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) 기반 KYC 완료 VC -> 매번 서류 없이 재사용

- **📢 섹션 요약 비유**: — "한 번 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)받은 신분증(VC)을 여러 곳에 재사용하되, 필요한 정보만 골라 보여줄 수 있는 스마트 신분증이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) Method별 특성

| [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) Method | 기반 | 특징 | 적합 환경 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/">did</a>:ethr</strong> | Ethereum | 이더리움 [스마트 컨트랙트](/knowledge-base/studynote/06_ict_convergence/01_blockchain/022_smart_contract/) | 공개 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/">did</a>:web</strong> | 웹 서버 | [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 기반, 가장 단순 | 기업 내부 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/">did</a>:ion</strong> | Bitcoin(ION) | DPKI([분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) [PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/)) | 대규모 공공 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/">did</a>:<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">key</a></strong> | 키 자체 | 서버 없음, 임시 신원 | 테스트·[IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) |

### 기술사 핵심 판단
1. <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/354_did_decentralized_identity_zkp/">ZKP</a>(<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/229_zkp_data_clean_room/">영지식 증명</a>) 연계</strong>: VC의 선택적 공개를 ZKP로 강화 -> 나이 범위만 공개 (나이 자체 비공개)
2. **키 관리**: [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) 개인키 분실 = 신원 분실 -> 소셜 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)(Social [Recovery](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)) 필요
3. **표준 준수**: W3C [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) Core 1.0, Verifiable Credentials [Data Model](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) 1.1
4. **프라이버시 규제**: GDPR의 '잊힐 권리' vs [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) 불변성 -> [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) [Document](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/) 비활성화 메커니즘

- **📢 섹션 요약 비유**: — "DID는 각자가 들고 다니는 디지털 지갑 속 신분증 모음 — 필요한 것만 꺼내 보여주고, 어디서 발급받았는지 누구나 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 가능하다.

---

## Ⅴ. 기대효과 및 결론

| 효과 항목 | 내용 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/">데이터 주권</a> <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/">회복</a></strong> | 개인이 자신의 신원 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 직접 관리 |
| **프라이버시 강화** | 필요한 속성만 선택적 공개 |
| **재사용 가능 KYC** | 한 번 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)으로 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 재사용 |
| **행정 비용 절감** | 서류 발급·[검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 자동화 |

[DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/)/VC/VP는 Web3 시대의 디지털 신원 인프라다. SSI 원칙에 기반한 W3C 표준은 개인 [데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/)을 실현하고, ZKP와 결합하면 진정한 프라이버시 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 신원 증명이 가능하다. 기술사는 Issuer-Holder-Verifier 신뢰 모델과 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/) [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) Registry의 역할을 명확히 설명해야 한다.

- **📢 섹션 요약 비유**: — "[DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/)/VC는 21세기 디지털 여권 시스템 — 국가(Issuer)가 여권을 발급하고, 개인(Holder)이 보관하며, 공항(Verifier)이 QR로 즉시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 연결 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 설명 |
| SSI | DID의 설계 철학, 자기 주권 신원 |
| W3C [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) Core | [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) 국제 표준 |
| [ZKP](/knowledge-base/studynote/12_it_management/05_security_compliance/354_did_decentralized_identity_zkp/) | VC 선택적 공개의 프라이버시 강화 수단 |
| [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) | [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/)/VC 실무 적용 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |

### 📈 관련 키워드 및 발전 흐름도

```text
[관계 설명] -> [탈중앙화 신원: DID · VC] -> [DID · VC 실무 적용 서비스]
```

### 👶 어린이를 위한 3줄 비유 설명

1. 지금은 구글이나 카카오가 내 신분증을 보관하고 있는데, DID는 내가 직접 내 신분증을 가지고 다니는 거예요.
2. VC는 학교가 '이 학생은 수학을 잘 해요'라고 도장 찍어준 디지털 증명서예요.
3. VP는 그 증명서에서 '수학 점수만 보여주고 나머지는 가리는 것'이라 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)를 적게 공개해도 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 483 / 552

<- **이전**: [482. 블록체인 트릴레마: 확장성-탈중앙화-보안 (Blockchain Trilemma)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/482_blockchain_trilemma_scalability_decentralization_security/)
**다음**: [484. DAO 탈중앙화 자율 조직 (DAO, Decentralized Autonomous Organization)](/knowledge-base/studynote/06_ict_convergence/01_blockchain/484_dao_decentralized_autonomous_organization/) ->

---
