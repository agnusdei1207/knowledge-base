+++
title = "370. DID 분산신원 ZKP 영지식증명 자기주권신원 (DID Decentralized Identity ZKP Self-Sovereign Identity)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-devops-sre"]

[extra]
tags = ["studynote-devops-sre"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) (Decentralized [Identifier](/knowledge-base/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/))는 중앙 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 기관 없이 개인이 자신의 신원을 직접 소유·제어하는 SSI (Self-Sovereign Identity) 패러다임의 기술 구현으로, W3C [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) 표준과 VC (Verifiable Credential)/VP (Verifiable Presentation) 생태계가 기반이다.
> 2. **가치**: [ZKP](/knowledge-base/studynote/12_it_management/05_security_compliance/354_did_decentralized_identity_zkp/) ([Zero-Knowledge Proof](/knowledge-base/studynote/06_ict_convergence/01_blockchain/037_zero_knowledge_proof_zkp/))는 "만 19세 이상이다"를 증명할 때 생년월일 전체를 공개하지 않고도 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자가 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하도록 하는 선택적 공개(Selective Disclosure) 기술로, [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 최소화 원칙([GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/))과 신원 증명을 동시에 달성한다.
> 3. **판단 포인트**: [MyData](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/) ([마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)) 개념은 개인이 자신의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 제3자에게 능동적으로 제공·이동할 권리를 보장하며, [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) + VC + ZKP가 기술적 실현 기반이다.

---

## Ⅰ. 개요 및 필요성

전통 디지털 신원 모델은 중앙화된 [IdP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/) ([Identity Provider](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/), Google, Facebook, 정부 기관)가 사용자 신원을 소유하고 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)을 대행한다. 서버 해킹 시 대규모 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 유출이 발생한다.

"이 사람이 성인인가?"를 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하기 위해 생년월일, 이름, 주민번호 등 불필요한 정보까지 공개해야 하는 과잉 공개 문제가 있다. GDPR의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 최소화 원칙에 위반된다.

- 📢 섹션 요약 비유: 전통 신원 시스템은 여권을 정부가 보관하고 필요할 때 꺼내주는 구조다. DID는 내가 직접 여권을 들고 다니며, 필요한 정보만 선택해 보여주는 구조다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DID/VC/VP 생태계 구조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">발급기관 (Issuer)</div><div class="kb-diagram-note">— 대학, 병원, 정부</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">VC (Verifiable Credential) 발급 + 디지털 서명</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">소유자 (Holder)</div><div class="kb-diagram-note">— 사용자 디바이스 지갑(Wallet)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">VC 보관, VP (Verifiable Presentation) 구성</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">검증자 (Verifier)</div><div class="kb-diagram-note">— 서비스 제공자</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">VP 서명 검증 + ZKP로 최소 정보 확인</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">DID Registry</div><div class="kb-diagram-note">— 블록체인 or 분산 네트워크</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">DID Document (공개키, 서비스 엔드포인트) 저장</div></div>
</div>
</div>



| 구성 요소                          | 역할                                           | 표준            |
| :--------------------------------- | :--------------------------------------------- | :-------------- |
| [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) (Decentralized [Identifier](/knowledge-base/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/))     | 중앙 기관 없는 고유 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)                      | W3C [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) Core    |
| VC (Verifiable Credential)         | 발급기관 서명 포함 디지털 자격증명              | W3C VC v2.0     |
| VP (Verifiable Presentation)       | 필요한 VC만 선택해 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자에게 제시             | W3C VC          |
| [ZKP](/knowledge-base/studynote/12_it_management/05_security_compliance/354_did_decentralized_identity_zkp/) ([Zero-Knowledge Proof](/knowledge-base/studynote/06_ict_convergence/01_blockchain/037_zero_knowledge_proof_zkp/))         | 정보 공개 없이 진위 증명                        | zk-SNARK, BBS+  |

<strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/354_did_decentralized_identity_zkp/">ZKP</a> 원리</strong>: 증명자(Prover)가 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자(Verifier)에게 "명제가 참이다"를 실제 정보 없이 증명. zk-SNARK ([Zero](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/)-Knowledge Succinct Non-interactive ARgument of Knowledge)와 BBS+ 서명이 대표 구현이다.

- 📢 섹션 요약 비유: ZKP는 마술사가 카드를 뒤집지 않고 "이 카드가 에이스다"를 증명하는 것과 같다. 카드(정보)를 보여주지 않고도 사실임을 수학적으로 증명한다.

---

## Ⅲ. 비교 및 연결

| 항목           | 중앙화 신원([IdP](/knowledge-base/studynote/09_security/11_iam_access_control/536_idp_identity_provider/))             | 탈중앙 신원([DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/)/SSI)         |
| :------------- | :--------------------------- | :--------------------------- |
| 신원 소유      | 플랫폼(구글, 정부)           | 개인 직접 소유               |
| 프라이버시     | 낮음 (전체 공개 필요)        | 높음 ([ZKP](/knowledge-base/studynote/12_it_management/05_security_compliance/354_did_decentralized_identity_zkp/) 선택적 공개)       |
| [단일 장애점](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/454_spof/)    | 있음                         | 없음                         |
| 표준           | OAuth2, [OIDC](/knowledge-base/studynote/09_security/11_iam_access_control/537_oidc_openid_connect/)                  | W3C [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/), VC                  |

<strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/">MyData</a> (<a href="/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/">마이데이터</a>)</strong>: 개인이 자신의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(금융·의료·공공)를 제3자에게 능동적으로 제공·이동하는 권리 보장. 한국 금융 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/)는 2022년 시행으로 은행·카드사 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 핀테크 앱으로 통합 조회·이동할 수 있다.

- 📢 섹션 요약 비유: 중앙화 신원은 식당 예약을 레스토랑 서버(중앙 서버)가 관리하는 것이고, DID는 내가 직접 예약 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)서(VC)를 들고 다니는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

<strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/">DID</a>/SSI 도입 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/">체크리스트</a></strong>
1. 사용 사례 정의: 교육 자격증 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 의료 기록 공유, 금융 KYC
2. [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) Method 선택: [did](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/):web (웹 기반, 간단), [did](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/):ethr (Ethereum), [did](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/):ion ([비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)코인)
3. VC 발급 시스템 구축: 발급기관 서명 키 관리([HSM](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/475_hsm/)), VC 취소 목록(Revocation) 관리
4. [ZKP](/knowledge-base/studynote/12_it_management/05_security_compliance/354_did_decentralized_identity_zkp/) 적용: BBS+ 서명으로 VC에서 필요한 [속성](/knowledge-base/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)만 선택적 공개
5. 규제 준수: [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) [Right to be Forgotten](/knowledge-base/studynote/09_security/16_data_privacy/794_right_to_be_forgotten/) 대응

<strong><a href="/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/">안티패턴</a></strong>
- 모든 VC를 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)에 직접 저장 → [GDPR](/knowledge-base/studynote/09_security/16_data_privacy/791_gdpr_eu/) 위반
- [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) 없이 VC만 발급 → 신원 소유권 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)화 효과 없음
- [ZKP](/knowledge-base/studynote/12_it_management/05_security_compliance/354_did_decentralized_identity_zkp/) 없는 VC 제시 → 불필요한 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/) 과잉 공개

- 📢 섹션 요약 비유: 모든 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)를 [블록체인](/knowledge-base/studynote/06_ict_convergence/01_blockchain/004_blockchain/)에 저장하는 것은 주민등록증을 투명한 유리 케이스에 넣어 공개 전시하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

[DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/)/VC 기반 모바일 신분증(행정안전부 모바일 운전면허증)은 QR 코드 스캔으로 신원을 즉각 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하며, 불필요한 정보 없이 연령 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)이 가능하다. EU Digital Identity Wallet (eIDAS 2.0)은 2024년 EU 전역에 [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) 기반 디지털 신원 지갑을 도입한다.

미래는 AI가 개인 디지털 에이전트로서 [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) Wallet을 관리하고, ZKP로 최소 정보만 공개하며 신원 증명이 완전히 자동화되는 세계로 발전한다.

- 📢 섹션 요약 비유: [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/)/SSI의 미래는 스마트 디지털 여권이다. 해외여행 시 입국심사관에게 여권 전체를 보여주는 대신, "입국 자격이 있다"는 증명만 ZKP로 전달하고 [개인정보](/knowledge-base/studynote/09_security/16_data_privacy/781_personal_information/)는 공개되지 않는다.

---

### 📌 관련 개념 맵

| 개념                                    | 연결 포인트                                               |
| :-------------------------------------- | :-------------------------------------------------------- |
| [DID](/knowledge-base/studynote/12_it_management/05_security_compliance/231_did_decentralized_identity/) (Decentralized [Identifier](/knowledge-base/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/))          | W3C 표준, 중앙 기관 없는 고유 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)                    |
| VC (Verifiable Credential)              | 발급기관 서명 포함 디지털 자격증명                       |
| [ZKP](/knowledge-base/studynote/12_it_management/05_security_compliance/354_did_decentralized_identity_zkp/) ([Zero-Knowledge Proof](/knowledge-base/studynote/06_ict_convergence/01_blockchain/037_zero_knowledge_proof_zkp/))              | 정보 공개 없이 진위 증명, BBS+·zk-SNARK 구현            |
| SSI (Self-Sovereign Identity)           | 개인이 신원을 직접 소유·제어하는 패러다임               |
| [MyData](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/266_mydata_open_api_token_security/)                                  | 개인 [데이터 주권](/knowledge-base/studynote/09_security/16_data_privacy/809_data_sovereignty/) 보장, 한국 금융 [마이데이터](/knowledge-base/studynote/16_bigdata/01_intro/012_mydata/) 사례         |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">중앙화 신원 (구글, 정부 IdP)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">연합 신원 (SAML, OAuth2, OIDC)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">DID (W3C 표준, 분산 식별자)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">VC/VP (검증 가능한 자격증명/발표)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">ZKP (선택적 공개, BBS+/zk-SNARK)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">MyData + FIDO2 통합 자기주권 신원 생태계</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. DID는 내가 직접 들고 다니는 디지털 신분증이에요. 회사(구글, 정부)가 보관하지 않고 내 폰에 저장해요.
2. ZKP는 나이가 몇 살인지 알려주지 않고 "성인이 맞다"는 것만 수학으로 증명하는 마법이에요.
3. MyData는 내 은행 통장 정보를 내가 원하는 앱에 직접 보내줄 수 있는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이동 권리예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 370 / 373

← **이전**: [369. 블록체인 분산원장 스마트계약 BFT 합의 (Blockchain DLT Smart Contract BFT PBFT Consensus)](/knowledge-base/studynote/15_devops_sre/05_devsecops/369_dlt_bft/)
**다음**: [371. DevOps 클라우드 기술사 핵심 키워드 통합 요약 (DevOps Cloud PE Integrated Keyword Summary)](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/371_process/) →

---
