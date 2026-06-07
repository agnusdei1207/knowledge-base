---
title: "Ct Certificate Transparency"
date: "2026-05-05"
tags:
  - "studynote-security"
weight: 165
---
## 핵심 인사이트

> 1. **본질**: 인증서 투명성 ([CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/), Certificate Transparency)은 인증기관 ([CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/), Certificate Authority)이 발급한 인증서 정보를 추가 전용 공개 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 기록하게 해, 잘못 발급된 인증서를 누구나 발견할 수 있게 만드는 감시 체계다.
> 2. **가치**: CT는 위조 발급을 원천적으로 막기보다, 발급 사실을 숨기지 못하게 만들어 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유자와 브라우저가 빠르게 이상 징후를 탐지하도록 돕는다.
> 3. **판단 포인트**: CT는 인증서 폐기 자체를 대신하지 않으므로, 실무에서는 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링·[SCT](/studynote/09_security/04_endpoint_security/167_sct_signed_certificate_timestamp/) ([Signed Certificate Timestamp](/studynote/09_security/04_endpoint_security/167_sct_signed_certificate_timestamp/)) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)·폐기 체계까지 함께 운영해야 효과가 완성된다.

---

## Ⅰ. 개요 및 필요성

[CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) (Certificate Transparency)는 웹 공개 키 기반 구조 ([PKI](/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/), [Public Key Infrastructure](/studynote/09_security/uncategorized/1080_pki_public_key_infrastructure_ca_ra_certificate/))에서 인증서 발급 과정을 투명하게 드러내기 위한 공개 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 프레임워크다. 핵심 아이디어는 간단하다. 어떤 CA가 어떤 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 인증서를 발급했는지 <strong>숨길 수 없게 만드는 것</strong>이다. 이렇게 되면 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유자, 보안팀, 브라우저가 의심스러운 발급을 더 빨리 발견할 수 있다.

이 기술이 필요해진 배경에는 [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 오남용과 침해 사고가 있었다. 대표적으로 DigiNotar 사건처럼, 신뢰받던 CA가 침해되면 공격자는 유명 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 대한 가짜 인증서를 발급받아 [중간자 공격](/studynote/03_network/14_network_security_threats/706_mitm_man_in_the_middle_hsts/) (MitM, Man-in-the-Middle)이나 피싱에 악용할 수 있다. 기존 PKI에서는 진짜 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 운영자가 이런 사실을 한참 뒤에야 알아차리는 경우가 많았다.

CT는 이 문제를 "완벽한 사전 차단"이 아니라 "발급 은닉 불가"라는 방식으로 다룬다. 즉 누군가 몰래 가짜 인증서를 만들어도, 브라우저가 요구하는 증빙을 얻으려면 공개 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 흔적을 남겨야 한다. 이 점이 CT의 가장 강력한 설계 철학이다.

```text
+----------------------------------------------------------------------+
|                 CT의 목적: 발급 사실을 숨기지 못하게 함             |
+----------------------------------------------------------------------+
| Without CT: mis-issued certificate can stay hidden                  |
| With CT   : issuance must appear in public log and be monitored     |
|                                                                  |
| Result: CA trust becomes auditable, not blind                      |
+----------------------------------------------------------------------+
```

따라서 CT는 "신뢰를 없애는 기술"이 아니라, <strong>신뢰를 감시 가능한 형태로 바꾸는 기술</strong>이라고 보는 편이 정확하다.

- **📢 섹션 요약 비유**: CT는 동사무소가 서류를 떼 줄 때마다 마을 게시판에 바로 공고하게 만들어, 몰래 가짜 서류를 발급해도 숨길 수 없게 하는 제도와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 생태계의 주요 참여자는 [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/), [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 서버, [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/) ([Monitor](/studynote/02_operating_system/04_synchronization/229_monitor/)), 감사자 또는 브라우저 검사기 (Auditor)다. CA는 인증서 또는 사전 인증서 (Precertificate)를 [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)에 제출하고, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 이를 기록하겠다는 서명된 약속인 SCT를 돌려준다. 서버는 이 SCT를 인증서나 [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) (Transport Layer [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) 핸드셰이크에 포함해 제시하고, 브라우저는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)에 맞는 SCT가 있는지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)한다.

[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 보통 [머클 트리](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/) ([Merkle Tree](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/)) 기반의 **추가 전용 (Append-only)** 구조를 사용한다. 새로운 항목은 끝에만 더해지며, 기존 기록을 수정하거나 삭제하면 루트 해시가 바뀌기 때문에 외부 감시자가 변조를 탐지할 수 있다. 즉 CT는 "[로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 공개한다"에서 끝나지 않고, <strong><a href="/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/">로그</a> <a href="/studynote/09_security/01_intro_principles/003_integrity/">무결성</a>까지 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 가능한 형태</strong>로 만든다.

| 구성 요소 | 역할 | 핵심 포인트 |
| :--- | :--- | :--- |
| [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) | 인증서 발급 및 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 제출 | [SCT](/studynote/09_security/04_endpoint_security/167_sct_signed_certificate_timestamp/) 확보 필요 |
| [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) Log | 공개 기록 보관 | Append-only, [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 증명 |
| [Monitor](/studynote/02_operating_system/04_synchronization/229_monitor/) | 특정 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 발급 감시 | 오발급 조기 탐지 |
| Auditor / Browser | [SCT](/studynote/09_security/04_endpoint_security/167_sct_signed_certificate_timestamp/) 및 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반 시 경고 |
| [Merkle Tree](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/) | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/) 증명 | 변조 시 해시 불일치 발생 |

아래 그림은 CT의 대표적인 동작 흐름을 보여준다.

```text
+----------------------------------------------------------------------+
|                      CT의 발급·검증 흐름                            |
+----------------------------------------------------------------------+
| CA -- submit cert/precert ---> CT Log                                |
| CA <------- SCT (signed promise) ------- CT Log                       |
| CA -- issue cert with SCT ---> Website Server                         |
| Browser -- connect ---> Server                                        |
| Browser <-- cert + SCT -- Server                                      |
| Browser -- verify SCT / policy / proof ---> Trust or Warn             |
| Monitor -- watch logs for suspicious domains ---> Security Team       |
+----------------------------------------------------------------------+
```

핵심 원리는 두 가지다. 첫째, 인증서가 브라우저에서 신뢰받으려면 공개 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)와 연결된 흔적이 필요하다는 점이다. 둘째, [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유자는 [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 실시간 감시해 자기 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 대한 예상치 못한 발급을 발견할 수 있다는 점이다. 그래서 CT는 발급 이후의 가시성과 대응 속도를 크게 높인다.

- **📢 섹션 요약 비유**: CT는 열쇠를 복사해 줄 때 복사점이 영수증을 공개 게시판에 붙이고, 집주인이 그 게시판을 계속 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있게 만든 구조와 같다.

---

## Ⅲ. 비교 및 연결

CT를 이해할 때 자주 헷갈리는 개념은 인증서 해지 목록 ([CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/), [Certificate Revocation List](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/)), 온라인 인증서 상태 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) ([OCSP](/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/), Online Certificate Status [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)), 그리고 인증기관 허가 ([CAA](/studynote/09_security/04_endpoint_security/168_caa_certification_authority_authorization/), [Certification Authority Authorization](/studynote/09_security/04_endpoint_security/168_caa_certification_authority_authorization/))다. CT는 <strong>발급 사실의 공개와 감시</strong>에 초점을 두고, [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/)/OCSP는 <strong>이미 발급된 인증서의 폐기 상태 <a href="/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>에 초점을 둔다. CAA는 어떤 CA가 내 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 인증서를 발급해도 되는지 미리 선언하는 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이다.

| 항목 | [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) | [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) / [OCSP](/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/) | [CAA](/studynote/09_security/04_endpoint_security/168_caa_certification_authority_authorization/) |
| :--- | :--- | :--- | :--- |
| 목적 | 발급 사실 공개·감시 | 발급 후 폐기 상태 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) | 발급 권한 사전 제한 |
| 시점 | 발급 시점 중심 | 발급 이후 | 발급 이전 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| 핵심 효과 | 오발급 은닉 방지 | 폐기 여부 전달 | 허용된 [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 범위 축소 |
| 한계 | 스스로 폐기하지는 못함 | 오발급 탐지는 약함 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반 감시는 별도 필요 |

이처럼 CT는 다른 인증서 보안 기술을 대체하기보다 보완한다. 예를 들어 잘못 발급된 인증서를 [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)가 발견하면, 운영자는 곧바로 CA에 폐기를 요청하고 [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/)/OCSP를 통해 폐기 상태가 배포되도록 해야 한다. 즉 CT는 "보이는 것", 해지 체계는 "막는 것"에 더 가깝다.

또한 CT는 보안 운영과도 직접 연결된다. 대규모 조직은 자사 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)과 하위 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)에 대한 [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링을 자동화해, 의심스러운 발급이 생기면 보안팀에 경보를 보내는 식으로 운용한다. 그래서 CT는 브라우저 표준이면서 동시에 실무 보안 관제 도구이기도 하다.

- **📢 섹션 요약 비유**: CT가 게시판에 수상한 서류 발급 사실을 보여주는 CCTV라면, CRL과 OCSP는 그 서류가 이제 무효라는 빨간 도장을 찍어 알려주는 절차에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 CT의 가치는 "우리 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)으로 누가 언제 인증서를 발급받았는지"를 스스로 감시할 수 있다는 데 있다. 예를 들어 대기업 보안팀이 `*.example.com`에 대한 [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링을 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)해 두면, 예기치 않은 하위 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 인증서가 발급된 순간 이를 감지하고 발급 주체를 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)할 수 있다. 이는 오발급, 계정 탈취, 자동화 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 오류를 조기에 발견하는 데 유용하다.

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 주요 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)과 서브도메인에 대한 [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링이 자동화되어 있는가?
2. 공개 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)용 인증서가 브라우저 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)에 맞는 SCT를 포함하는가?
3. 의심 발급 발견 시 폐기 요청, 교체 배포, 원인 분석 절차가 준비되어 있는가?
4. 멀티 [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 환경에서 발급 경로와 승인 절차를 추적할 수 있는가?
5. 내부 테스트용 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 정보가 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 공개로 노출되어도 되는지 검토했는가?

### 판단 원칙

- **필수 대응**: 외부 공개 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 인증서는 [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)과 브라우저 요구사항을 반드시 만족해야 한다.
- **운영 보완**: CT는 탐지 수단이므로, 경보 이후의 해지·재발급·원인분석 프로세스가 함께 있어야 한다.
- **주의 사항**: 공개 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 특성상 내부 호스트명이나 민감한 서브도메인 노출 위험을 고려해야 한다.

기술사 답안에서는 CT를 단순히 "인증서 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)"라고만 쓰지 말고, [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 신뢰를 투명성으로 보완하는 구조라는 점을 명확히 적는 것이 중요하다. 또한 CT가 오발급을 드러내 주지만, 그 자체로 무효화까지 대신하지는 않는다는 한계를 함께 적어야 균형 잡힌 답안이 된다.

- **📢 섹션 요약 비유**: [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) 운영은 CCTV를 설치하는 것만으로 끝나지 않는다. 이상 장면이 보이면 즉시 출동하고 자물쇠를 바꾸는 대응 체계까지 있어야 진짜 안전하다.

---

## Ⅴ. 기대효과 및 결론

CT가 정착되면 웹 PKI의 신뢰는 훨씬 더 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능해진다. [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유자는 오발급을 더 빨리 발견할 수 있고, 브라우저는 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 증빙이 없는 인증서를 더 엄격히 배제할 수 있다. 결과적으로 공격자는 가짜 인증서를 발급받더라도 그 사실을 장기간 숨기기 어려워진다.

물론 CT가 모든 인증서 위험을 없애는 것은 아니다. [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/)링하지 않으면 공개되어도 못 볼 수 있고, 발견 후 폐기 절차가 느리면 실질적 피해를 막기 어렵다. 또한 공개 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)는 투명성을 주는 대신 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 정보 노출이라는 trade-off를 만든다.

그럼에도 CT의 의미는 분명하다. 인터넷 신뢰를 소수 CA의 비밀스러운 판단에만 맡기지 않고, <strong>공개 기록과 상호 감시가 가능한 체계</strong>로 바꿨다는 데 있다. 즉 CT는 인증서 보안의 완성품이 아니라, 더 투명한 신뢰 구조를 만드는 핵심 기반이다.

- **📢 섹션 요약 비유**: CT는 모두가 볼 수 있는 회계장부와 같다. 장부를 공개한다고 도둑이 완전히 사라지지는 않지만, 몰래 빼돌리기는 훨씬 어려워진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) (Certificate Authority) | 인증서를 발급하는 신뢰 주체 |
| [SCT](/studynote/09_security/04_endpoint_security/167_sct_signed_certificate_timestamp/) ([Signed Certificate Timestamp](/studynote/09_security/04_endpoint_security/167_sct_signed_certificate_timestamp/)) | [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 등록 사실을 증명하는 서명된 약속 |
| [Merkle Tree](/studynote/06_ict_convergence/01_blockchain/007_merkle_tree/) | [CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/) [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)의 [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 보장하는 핵심 자료구조 |
| [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) / [OCSP](/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/) | 오발급 발견 후 폐기 상태를 전달하는 수단 |
| [CAA](/studynote/09_security/04_endpoint_security/168_caa_certification_authority_authorization/) | 허용된 CA를 사전 제한하는 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 기반 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [PKI](/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) ([Public Key Infrastructure](/studynote/09_security/uncategorized/1080_pki_public_key_infrastructure_ca_ra_certificate/)) | CT가 보완하는 전체 신뢰 기반 |

### 📈 관련 키워드 및 발전 흐름도

```text
CA 중심 신뢰 모델
    |
    v
오발급·CA 침해 문제 노출
    |
    v
CT (Certificate Transparency)
    |
    +- SCT 검증
    +- 로그 모니터링
    +- CRL / OCSP / CAA와 결합
```

이 흐름은 웹 PKI가 "맹목적 신뢰"에서 "투명성과 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 가능한 신뢰"로 이동한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. CT는 누가 내 이름으로 신분증을 만들었는지 모두가 보는 게시판에 적어 두는 규칙이에요.
2. 그래서 나쁜 사람이 몰래 가짜 신분증을 만들어도 숨기기 어려워져요.
3. 하지만 이상한 신분증을 발견하면 바로 없애는 일은 또 따로 해야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 218 / 1108

<- **이전**: [164. OCSP 스테이플링 — 서버가 OCSP 응답 사전 가져옴](/studynote/09_security/04_endpoint_security/164_ocsp_stapling/)
**다음**: [166. CT 로그 서버 — Google/Rustproof 등 다수 운영](/studynote/09_security/04_endpoint_security/166_ct_log_server/) ->

---
