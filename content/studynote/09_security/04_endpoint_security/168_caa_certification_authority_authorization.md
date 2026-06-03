+++
title = "168. CAA (Certification Authority Authorization) — 허용된 CA DNS 레코드"
date = 2026-04-05

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CAA ([Certification Authority](/knowledge-base/studynote/09_security/03_network_security/160_ca_certification_authority/) [Authorization](/knowledge-base/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/))는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유자가 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) ([Domain Name System](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/))에 "어떤 인증기관 ([CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/), Certificate Authority)만 내 인증서를 발급할 수 있는가"를 선언하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 레코드다.
> 2. **가치**: 신뢰 저장소에 많은 CA가 들어 있는 웹 [PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) ([Public Key Infrastructure](/knowledge-base/studynote/09_security/uncategorized/984_pki_public_key_infrastructure_ca_ra_certificate/)) 환경에서, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유자가 허용한 기관 외의 오발급 가능성을 발급 직전에 줄여 주는 저비용 예방 통제다.
> 3. **판단 포인트**: CAA는 [CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) ([Certificate Transparency](/knowledge-base/studynote/09_security/04_endpoint_security/165_ct_certificate_transparency/))처럼 사후 공개 감시를 대체하지 않으며, 정확한 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 운영과 [DNSSEC](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/518_dnssec_dns_security_extensions/) ([Domain Name System](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Extensions) 같은 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)가 함께 갈 때 효과가 커진다.

---

## Ⅰ. 개요 및 필요성

CAA는 인증서 발급 권한을 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유자가 명시적으로 제한하는 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이다. 웹 브라우저는 수많은 공인 CA를 신뢰하지만, [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유자는 보통 그중 일부만 사용한다. 문제는 공격자나 운영 실수가 엉뚱한 CA를 통해도 인증서 발급 시도로 이어질 수 있다는 점이다.

이 개념이 필요해진 배경은 웹 PKI의 약한 고리 문제다. 어떤 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)이 DigiCert만 쓰더라도, 브라우저 신뢰 저장소에 있는 다른 CA가 잘못된 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)으로 인증서를 발급하면 사용자 입장에서는 여전히 위험하다. CAA는 이 상황에서 "[도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 주인이 허용한 기관만 발급하라"는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 DNS에 공개해, 발급 전에 한 번 더 걸러내는 장치를 제공한다.

2017년 이후 공인 CA는 인증서 발급 전 CAA 레코드를 확인하는 절차를 사실상 필수로 수행한다. 따라서 CAA는 선언적 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) 한 줄로 끝나 보이지만, 실제로는 전 세계 CA의 발급 절차 안에 들어간 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 제어점이다.

- **📢 섹션 요약 비유**: CAA는 우리 회사 도장은 지정된 인감 담당자만 찍을 수 있다고 출입구에 붙여 두는 승인 명부와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CAA 레코드는 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 존에 게시되며, CA는 인증서 발급 요청을 받으면 해당 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)과 상위 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 조회해 허용 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 확인한다. 대표 태그는 `issue`, `issuewild`, `iodef`이며, 각각 일반 인증서 허용 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/), [와일드카드 인증서](/knowledge-base/studynote/09_security/04_endpoint_security/175_wildcard_certificate/) 허용 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/), 위반 통지 수단을 뜻한다. 따라서 CAA는 암호 알고리즘이 아니라 **발급 전에 수행되는 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 기반 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 검사**다.

| 태그 | 의미 | 활용 포인트 |
| :--- | :--- | :--- |
| `issue` | 일반 인증서 발급 허용 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 지정 | 특정 공인 CA만 허용 |
| `issuewild` | [와일드카드 인증서](/knowledge-base/studynote/09_security/04_endpoint_security/175_wildcard_certificate/) 발급 허용 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 지정 | `*.example.com` 통제 강화 |
| `iodef` | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반 보고 수단 | 메일·URL로 보안팀 알림 |
| [flag](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) | 향후 확장용 제어 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) | 일반적으로 `0` 사용 |

아래 그림은 CAA가 인증서 발급 파이프라인 어디에 개입하는지 보여 준다.

```text
┌──────────────────────────────────────────────────────────────────────┐
│                  CAA check in certificate issuance                   │
├──────────────────────────────────────────────────────────────────────┤
│ Applicant ─▶ CA request                                              │
│                │                                                     │
│                ▼                                                     │
│         CA queries DNS CAA record                                    │
│                │                                                     │
│       Allowed? ── Yes ─▶ Validate domain ─▶ Issue certificate        │
│                │                                                     │
│                └─ No ─▶ Reject / alert via iodef                     │
└──────────────────────────────────────────────────────────────────────┘
```

예를 들어 `example.com. IN CAA 0 issue "digicert.com"`은 DigiCert 계열만 일반 인증서를 발급할 수 있다는 뜻이다. `issuewild`를 비워 두거나 특정 CA만 지정하면 [와일드카드 인증서](/knowledge-base/studynote/09_security/04_endpoint_security/175_wildcard_certificate/) 발급 범위를 더 엄격히 제한할 수 있다. 또한 `iodef`를 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)해 두면 위반 시도나 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 오류를 보안팀이 더 빨리 감지할 수 있다.

중요한 기술 포인트는 CAA가 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/)처럼 동작할 수 있다는 점이다. 일반적으로 하위 호스트명에 명시된 CAA가 없으면 CA는 상위 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)으로 올라가 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 찾는다. 따라서 서브도메인 위임 구조, 멀티 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 사용 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), 외부 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 호스팅 환경을 함께 고려해 설계해야 한다.

- **📢 섹션 요약 비유**: CAA는 도장 찍기 전에 결재선 명단을 먼저 확인하게 하는 규칙과 같아서, 명단에 없는 사람은 서류를 만들기 시작하기도 전에 멈추게 한다.

---

## Ⅲ. 비교 및 연결

CAA는 [CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/), [DNSSEC](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/518_dnssec_dns_security_extensions/), 온라인 인증서 상태 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) ([OCSP](/knowledge-base/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/), Online Certificate Status [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)), 인증서 폐기 목록 ([CRL](/knowledge-base/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/), [Certificate Revocation List](/knowledge-base/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/))과 자주 함께 언급되지만 역할이 다르다. CAA는 발급 전 예방 통제이고, CT는 발급 후 공개 감시이며, DNSSEC는 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 응답 위변조 방지, OCSP는 발급된 인증서의 폐기 상태 확인에 가깝다. 즉 모두 인증서 생태계에 중요하지만 관여 시점이 다르다.

| 항목 | CAA | [CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) | [DNSSEC](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/518_dnssec_dns_security_extensions/) | [OCSP](/knowledge-base/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/) / [CRL](/knowledge-base/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) |
| :--- | :--- | :--- | :--- | :--- |
| 핵심 질문 | 누가 발급할 수 있는가 | 무엇이 발급되었는가 | [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 응답이 위조되지 않았는가 | 지금도 유효한가 |
| 통제 시점 | 발급 전 | 발급 후 | 질의 시 | 운영 중 |
| 성격 | 예방 | 탐지·[감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) | [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) | 상태 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |
| 한계 | 허용 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 범위만 제어 | 발급 자체를 막지는 못함 | [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 선택 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 아님 | 오발급 예방은 못 함 |

이 비교가 중요한 이유는 CAA 하나만으로 웹 PKI가 완성되지 않기 때문이다. 예를 들어 CAA가 있어도 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 응답이 변조되면 잘못된 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 볼 수 있으므로 DNSSEC가 도움이 된다. 반대로 CAA가 발급을 제한해도 이미 발급된 이상 인증서를 발견하려면 [CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 모니터링이 필요하다.

실무적으로는 자동 인증서 발급 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) (ACME, Automated Certificate [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) [Environment](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/))과도 연결된다. 자동 갱신 파이프라인이 여러 CA를 혼용하는 경우, CAA가 그 범위를 정확히 제한하지 않으면 운영 편의성 때문에 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 느슨해질 수 있다. 따라서 CAA는 "허용된 발급자 집합을 선언하는 거버넌스"로 보는 것이 맞다.

- **📢 섹션 요약 비유**: CAA는 사전 승인 명부, CT는 공개 게시판, DNSSEC는 게시판 위조 방지 봉인, OCSP는 이미 발급된 신분증이 취소되었는지 확인하는 전화와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

대표적인 실무 시나리오는 기업이 운영 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)과 외부 위탁 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 함께 관리하는 경우다. 본사 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) `example.com`은 DigiCert만 쓰지만, 마케팅 서브도메인 `campaign.example.com`은 별도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 사업자가 Let's Encrypt를 쓰는 식의 혼합 구성이 있을 수 있다. 이때 상위 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)에만 단순 CAA를 걸면 하위 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 발급이 실패하거나, 반대로 하위 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 누락으로 원치 않는 CA가 허용될 수 있다.

### 기술사 판단 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 실제 사용하는 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 목록과 CAA `issue` [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 일치하는가?
2. [와일드카드 인증서](/knowledge-base/studynote/09_security/04_endpoint_security/175_wildcard_certificate/) 사용 여부에 맞춰 `issuewild`를 별도로 관리하는가?
3. 서브도메인 위임 구조에서 [상속](/knowledge-base/studynote/04_software_engineering/04_testing_quality/234_uml_class_relationships_generalization_dependency/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 의도대로 작동하는가?
4. `iodef` 알림 채널이 유효하며 보안팀이 실제로 모니터링하는가?
5. [DNSSEC](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/518_dnssec_dns_security_extensions/), [CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 모니터링, 인증서 자산 관리와 함께 운영되는가?

### 채택 / 회피 기준

- **채택**: 공개 [HTTPS](/knowledge-base/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 운영하고, 허용된 CA를 명확히 제한하고 싶은 대부분의 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)
- **주의 필요**: 여러 위탁사가 각기 다른 CA를 쓰는 복잡한 서브도메인 구조, 자동화 파이프라인과 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 불일치가 잦은 환경

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- CAA를 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/)해 두고 실제 인증서 발급 업체 변경 시 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 갱신하지 않는 경우
- `issuewild`를 고려하지 않아 일반 인증서 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)만으로 와일드카드까지 통제된다고 착각하는 경우
- CAA가 있으니 [CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 모니터링이나 DNSSEC는 필요 없다고 보는 경우

- **📢 섹션 요약 비유**: CAA 운영은 문에 자물쇠를 다는 것에서 끝나지 않고, 누가 열쇠를 갖고 있는지 명단을 계속 최신 상태로 유지하는 일과 같다.

---

## Ⅴ. 기대효과 및 결론

CAA의 가장 큰 장점은 비용 대비 효과가 크다는 점이다. [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 레코드 몇 줄만으로 허용되지 않은 CA의 발급 시도를 상당 부분 사전에 걸러낼 수 있고, 인증서 거버넌스를 문서가 아니라 실제 발급 절차에 연결할 수 있다. 특히 대형 조직처럼 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 수가 많고 위탁 운영이 섞인 환경에서 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 일관성을 높이는 데 유용하다.

그러나 CAA는 만능 방패가 아니다. 이미 잘못 발급된 인증서를 회수해 주지도 않고, 허용된 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 내부의 운영 실수까지 모두 없애 주지도 않는다. 또한 [DNS](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 관리가 부정확하거나 응답 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)이 약하면 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 자체가 흔들릴 수 있으므로, CAA는 **사전 제한 장치**로 기억해야 한다.

결국 CAA의 핵심은 인증서 발급 권한을 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유자가 더 명시적으로 통제하게 만드는 데 있다. 웹 PKI가 "모든 신뢰된 CA가 잠재적으로 발급 가능"한 구조였다면, CAA는 그 범위를 줄여 "내가 허락한 CA만 발급 가능"한 구조로 좁혀 준다.

- **📢 섹션 요약 비유**: 좋은 CAA [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)은 누구나 출입 가능한 건물을 지정 출입자 명단이 있는 건물로 바꾸는 것과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) (Certificate Authority) | CAA [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)의 직접 통제 대상 |
| [DNSSEC](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/518_dnssec_dns_security_extensions/) ([Domain Name System](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) Extensions) | CAA 조회 결과의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 강화 |
| [CT](/knowledge-base/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) ([Certificate Transparency](/knowledge-base/studynote/09_security/04_endpoint_security/165_ct_certificate_transparency/)) | CAA가 막지 못한 오발급을 사후 감시 |
| ACME | 자동 발급 환경에서 CAA [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 일치 여부가 중요 |
| `issuewild` | [와일드카드 인증서](/knowledge-base/studynote/09_security/04_endpoint_security/175_wildcard_certificate/) 허용 범위를 별도로 제어 |
| `iodef` | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반 또는 이상 시도 알림 채널 |

### 📈 관련 키워드 및 발전 흐름도

```text
다수 CA를 신뢰하는 웹 PKI
    │
    ▼
오발급 · 약한 고리 문제 부각
    │
    ▼
CAA (Certification Authority Authorization)
    │
    ├─ issue / issuewild 정책
    ├─ iodef 통지
    └─ 발급 전 DNS 조회
    │
    ▼
DNSSEC · CT 모니터링 · 자동화된 인증서 거버넌스
```

이 흐름은 인증서 보안이 단순 신뢰 체인 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)에서, 발급 권한 통제와 공개 감시를 함께 갖춘 방향으로 발전하는 모습을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. CAA는 "우리 집 열쇠는 이 열쇠집만 만들 수 있어요"라고 문 앞에 써 두는 규칙이에요.
2. 다른 열쇠집이 몰래 열쇠를 만들려 하면, 먼저 그 문구를 보고 안 된다고 멈춰요.
3. 그래서 우리 집 열쇠를 누가 만들 수 있는지 더 똑똑하게 지킬 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 221 / 1108

← **이전**: [167. SCT (Signed Certificate Timestamp) — CT 증명](/knowledge-base/studynote/09_security/04_endpoint_security/167_sct_signed_certificate_timestamp/)
**다음**: [169. PKCS#10 — 인증서 서명 요청 (CSR) 형식](/knowledge-base/studynote/09_security/04_endpoint_security/169_pkcs10_csr/) →

---
