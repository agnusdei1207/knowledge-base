+++
title = "179. Self-signed 인증서 — 자체 발급 인증서, 내부용"
date = 2026-05-06

[taxonomies]
tags = ["studynote-security"]

[extra]
tags = ["studynote-security"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Self-signed [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서는 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) (Certificate Authority)의 서명 대신 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 주체가 자기 공개키에 스스로 서명한 X.509 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서로, 암호화 채널은 만들 수 있지만 공개 인터넷 기본 신뢰는 얻지 못한다.
> 2. **가치**: 개발 환경, 폐쇄망, 장비 간 [mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) ([Mutual TLS](/knowledge-base/studynote/09_security/04_endpoint_security/187_mtls_mutual_tls_authentication/)), [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 부트스트랩처럼 "누가 누구를 믿을지"를 운영자가 직접 통제할 수 있는 환경에서는 빠르고 저렴하게 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) (Transport Layer [Security](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))를 적용할 수 있다.
> 3. **판단 포인트**: 접속자가 브라우저 불특정 다수이거나 서버 수가 많아지는 순간 Self-signed 한 장씩 배포하는 방식은 금방 한계에 닿으므로, 공인 CA나 사설 [PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) ([Public Key Infrastructure](/knowledge-base/studynote/09_security/uncategorized/984_pki_public_key_infrastructure_ca_ra_certificate/))로 넘어갈 시점을 같이 판단해야 한다.

---

## Ⅰ. 개요 및 필요성

Self-signed [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서는 발급자와 주체가 같은 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서다. 즉 "누가 이 공개키의 주인인가"를 외부 기관이 보증하지 않고, 서버나 장비가 스스로 선언한다. TLS가 해결하려는 문제는 원래 두 가지다. 하나는 **전송 구간 암호화**, 다른 하나는 <strong>상대 신원 <a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>이다. Self-signed는 첫 번째는 빠르게 해결하지만, 두 번째는 운영자가 별도 절차로 메워야 한다.

이 개념이 필요한 이유는 모든 환경이 공인 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 체계를 요구하지 않기 때문이다. 로컬 개발 서버, 사내 폐쇄망 관리 콘솔, 공장 설비 제어망, 테스트용 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/), [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 장비 등록 구간은 외부 공인 CA를 붙이는 비용과 절차가 과할 수 있다. 이때 Self-signed는 "일단 암호화는 바로 적용하자"라는 현실적 해법이 된다.

다만 핵심은 무료라는 점이 아니라 <strong>신뢰를 기본 제공하지 않는다는 점</strong>이다. 운영자가 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 직접 배포하거나, 클라이언트에 신뢰 저장소(Trust Store)를 구성하거나, [인증서 핀닝](/knowledge-base/studynote/09_security/04_endpoint_security/182_certificate_pinning_ssl_tls_security/)(Pinning)을 걸지 않으면 브라우저와 운영체제는 이 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 모르는 발급자로 본다.

- **📢 섹션 요약 비유**: Self-signed [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서는 동네 모임에서 급히 만든 출입증과 같다. 문은 잠글 수 있지만, 그 출입증을 모르는 사람에게는 "이걸 누가 보증했지?"라는 질문이 남는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Self-signed [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서의 핵심은 "암호 수학은 정상이지만 신뢰 사슬이 짧다"는 데 있다. 서버는 개인키와 공개키를 만들고, 자기 공개키 정보를 담은 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서에 자신의 개인키로 서명한다. 클라이언트는 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서의 유효기간, [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) ([Subject Alternative Name](/knowledge-base/studynote/09_security/04_endpoint_security/174_san_subject_alternative_name/)), 서명 무결성까지는 검사할 수 있지만, 마지막 단계에서 <strong>이 서명을 믿을 만한 루트까지 연결할 수 있는가</strong>를 본다.

| [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 항목 | Self-signed에서의 상태 | 의미 |
| :--- | :--- | :--- |
| 유효기간 검사 | 가능 | 만료 전후 여부는 정상적으로 판단 가능 |
| [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) / 호스트명 일치 | 가능 | `example.local`처럼 이름이 맞아야 함 |
| 개인키 소유 증명 | 가능 | 해당 서버가 개인키를 갖고 있음을 보여 줌 |
| 신뢰 체인 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 기본 실패 | 루트 저장소에 없는 발급자이기 때문 |
| 폐기·대량 배포 | 약함 | 클라이언트마다 직접 신뢰 배포 필요 |

아래 그림은 브라우저가 Self-signed [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 어떻게 바라보는지 보여 준다.

```text
+----------------------------------------------------------------------+
| Self-signed certificate verification path                           |
+----------------------------------------------------------------------+
| Server presents certificate                                         |
|   Subject = intranet.example                                        |
|   Issuer  = intranet.example   <- same entity                       |
|   Signature = signed by its own private key                         |
|                                                                      |
| Client checks                                                        |
|   1. Valid time window ......................... OK / FAIL           |
|   2. SAN matches requested host ............... OK / FAIL            |
|   3. Signature math is consistent ............. OK                   |
|   4. Chain reaches trusted root store ......... FAIL by default      |
|                                                                      |
| Result                                                               |
|   Encryption can still work, but trusted identity is not granted    |
+----------------------------------------------------------------------+
```

중요한 오해 하나를 바로잡아야 한다. Self-signed라고 해서 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 자체가 평문이 되는 것은 아니다. 사용자가 경고를 무시하고 접속하면 대개 [세션 키](/knowledge-base/studynote/09_security/03_network_security/140_session_key/) 교환과 암호화는 그대로 일어난다. 문제는 그 채널의 반대편이 <strong>진짜 서버인지, 같은 모양의 다른 Self-signed <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>서를 내민 공격자인지</strong>를 기본적으로 분간하지 못한다는 데 있다.

그래서 실무에서는 Self-signed를 단독으로 두지 않는다. 클라이언트에 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 신뢰 저장소로 심거나, 모바일 앱처럼 특정 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 지문을 고정하는 핀닝을 적용하거나, 더 나아가 사설 루트 CA를 만들고 그 아래에서 여러 서버 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 발급하는 방식으로 확장한다.

- **📢 섹션 요약 비유**: 자물쇠는 튼튼한데, 그 자물쇠를 단 문이 진짜 우리 집 문인지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해 줄 관리실이 없는 상황과 같다.

---

## Ⅲ. 비교 및 연결

Self-signed를 이해할 때 가장 중요한 비교 대상은 공인 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서와 사설 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서다. 세 방식 모두 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 암호화는 가능하지만, <strong>신뢰를 배포하는 방식</strong>이 전혀 다르다.

| 방식 | 누가 서명하는가 | 기본 사용자 경험 | 운영 확장성 | 적합한 상황 |
| :--- | :--- | :--- | :--- | :--- |
| Self-signed 리프 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 | 서버 자신 | 브라우저 경고 발생 | 낮음 | 개발, 단일 장비, 임시 내부 통신 |
| 사설 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 하위 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 | 조직 내부 루트 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) | 내부 단말에 루트 배포 시 정상 | 높음 | 사내망, [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/), 장비 다수 운영 |
| 공인 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 하위 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 | 공개 신뢰 루트 [CA](/knowledge-base/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) | 브라우저 기본 신뢰 | 매우 높음 | 외부 공개 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) |

여기서 Self-signed와 사설 PKI를 혼동하면 안 된다. Self-signed 리프 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서는 <strong>서버 한 대가 자기 자신을 직접 보증</strong>하는 구조다. 반면 사설 CA는 내부 루트 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 먼저 신뢰 저장소에 배포하고, 그 아래에서 여러 서버 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 발급한다. 서버가 1대일 때는 Self-signed가 단순하지만, 50대가 되면 루트 하나를 배포하는 사설 CA가 훨씬 관리하기 쉽다.

또한 Self-signed는 [mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/), [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) (Internet of Things), [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 부트스트랩과도 연결된다. 고정된 장비끼리만 통신하고 상대 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 미리 알고 있다면 Self-signed 또는 핀닝 기반 신뢰가 가능하다. 그러나 사람 사용자가 일반 브라우저로 접근하는 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)라면 Let's Encrypt 같은 ACME (Automatic Certificate [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) [Environment](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/)) 자동화 체계가 훨씬 현실적이다.

- **📢 섹션 요약 비유**: Self-signed는 각 방이 자기 방문증을 직접 만드는 방식이고, 사설 CA는 건물 관리실이 모든 방 출입증을 통합 발급하는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무 판단의 핵심은 "암호화가 되느냐"가 아니라 "신뢰를 어떻게 배포할 것이냐"다. 아래 표처럼 환경에 따라 적합도가 크게 갈린다.

| 운영 시나리오 | 적합도 | 판단 이유 |
| :--- | :--- | :--- |
| 로컬 개발 서버, 테스트 [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) | 매우 높음 | 발급이 즉시 가능하고 사용자 수가 제한적 |
| 폐쇄망 관리자 포털 | 보통 | 가능하지만 단말 신뢰 저장소 배포가 필수 |
| 수십 개 이상 내부 [마이크로서비스](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/532_microservices_decomposition_patterns/) | 낮음~보통 | 개별 Self-signed보다 사설 CA가 더 적합 |
| 모바일 앱 + 고정 서버 | 보통 | [인증서 핀닝](/knowledge-base/studynote/09_security/04_endpoint_security/182_certificate_pinning_ssl_tls_security/)이 있으면 가능하지만 갱신 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 필요 |
| 외부 공개 웹 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) | 매우 낮음 | 브라우저 경고와 [피싱](/knowledge-base/studynote/09_security/15_malware_attack_vectors/752_phishing/) 혼동 위험 때문에 부적합 |

### 실무 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 이 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 신뢰해야 하는 클라이언트 수는 몇 대인가?
2. [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 갱신 시 신뢰 저장소 또는 핀닝 값을 어떻게 동시에 바꿀 것인가?
3. SAN에 실제 접속 이름이 모두 들어 있는가?
4. [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 분실·유출·교체 시 폐기 절차를 운영자가 수행할 수 있는가?
5. 지금 필요한 것이 단일 서버 암호화인지, 다수 서버 PKI인지 구분했는가?

### 자주 발생하는 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 사내 사용자 수가 많은데도 서버마다 Self-signed [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 따로 배포하는 구조
- 브라우저 경고를 사용자 교육으로만 무시하게 하고 기술적 신뢰 배포는 하지 않는 운영
- 공개 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 Self-signed를 사용해 [피싱](/knowledge-base/studynote/09_security/15_malware_attack_vectors/752_phishing/) 경고와 정상 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 구분을 흐리게 만드는 설계
- [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 갱신일을 놓쳐 앱 핀닝과 서버 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 동시에 깨지는 배포

기술사 답안에서는 <strong>"Self-signed는 암호화는 제공하지만 공개 신뢰를 제공하지 않으며, 소수의 고정 클라이언트를 운영자가 직접 통제할 수 있을 때만 실용적이고, 규모가 커지면 사설 CA나 공인 CA로 전환해야 한다"</strong>라고 정리하면 판단력이 드러난다.

- **📢 섹션 요약 비유**: 가족끼리만 쓰는 집 열쇠는 직접 깎아도 되지만, 입주민이 많은 아파트 출입카드는 결국 관리사무소 체계가 필요해지는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

Self-signed [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서는 가장 빠르게 TLS를 붙이는 방법이다. 덕분에 개발과 테스트에서 평문 전송을 줄이고, 폐쇄망과 장비 간 통신에서 기밀성을 빠르게 확보할 수 있다. 특히 외부 네트워크에 의존하지 않는다는 점은 격리망, 공장망, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 장비 등록 구간에서 분명한 장점이다.

하지만 Self-signed의 한계도 뚜렷하다. 신뢰를 기본 제공하지 못하고, [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 수가 늘수록 배포·회전·폐기 비용이 급격히 커진다. 따라서 Self-signed는 "싸고 쉬운 만능 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서"가 아니라, <strong>신뢰 범위가 작은 환경에서만 유효한 국소 해법</strong>으로 기억하는 것이 정확하다.

결론적으로 Self-signed의 가치는 공개 인터넷을 위한 대체재가 아니라, PKI가 과한 구간에서 암호화를 신속하게 확보하는 데 있다. 그리고 그다음 단계가 사설 CA인지, 공인 CA인지, [인증서 핀닝](/knowledge-base/studynote/09_security/04_endpoint_security/182_certificate_pinning_ssl_tls_security/)인지까지 이어서 설계할 때 비로소 안전한 운영이 된다.

- **📢 섹션 요약 비유**: Self-signed는 응급용 손전등과 같다. 당장 어둠을 밝히는 데는 매우 유용하지만, 건물 전체 조명 설비를 대신할 수는 없다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| X.509 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 | Self-signed도 같은 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 형식을 사용하되 발급자와 주체가 같다는 점이 다르다. |
| Trust Store | Self-signed를 신뢰하게 만들려면 클라이언트의 신뢰 저장소를 직접 구성해야 한다. |
| 사설 [PKI](/knowledge-base/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) ([Public Key Infrastructure](/knowledge-base/studynote/09_security/uncategorized/984_pki_public_key_infrastructure_ca_ra_certificate/)) | Self-signed의 확장형 대안으로, 내부 루트 CA를 통해 여러 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 체계적으로 발급한다. |
| [인증서 핀닝](/knowledge-base/studynote/09_security/04_endpoint_security/182_certificate_pinning_ssl_tls_security/) (Pinning) | 특정 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서나 공개키를 애플리케이션에 고정해 Self-signed 신뢰를 제한적으로 보강한다. |
| [mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) ([Mutual TLS](/knowledge-base/studynote/09_security/04_endpoint_security/187_mtls_mutual_tls_authentication/)) | 양쪽이 서로 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 구조로, 고정된 내부 통신에서 Self-signed 또는 사설 CA와 자주 결합된다. |
| ACME (Automatic Certificate [Management](/knowledge-base/studynote/12_it_management/05_security_compliance/372_management/) [Environment](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/066_gitlab_flow_environment_branch_strategy/)) | 공개 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서는 Self-signed 대신 자동 갱신 공인 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 운영하는 현실적 대안이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
평문 내부 통신
    |
    v
TLS 적용 필요 인식
    |
    +- 소수 고정 클라이언트 -> Self-signed 인증서
    |                          +- Trust Store 배포
    |                          +- Pinning / mTLS 적용
    |
    v
엔드포인트 증가 · 자동화 필요
    |
    v
사설 PKI 또는 공인 CA + ACME 체계로 확장
```

이 흐름은 Self-signed가 최종 목적지가 아니라, 작은 신뢰 범위에서 시작해 더 큰 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) 체계로 넘어가는 출발점이 될 수 있음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Self-signed [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서는 내가 내 이름표를 직접 만들어 붙이는 것과 비슷해요.
2. 우리 가족끼리는 그 이름표를 믿을 수 있지만, 모르는 사람은 진짜인지 다시 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)하고 싶어 해요.
3. 그래서 작은 모임에서는 편하지만, 사람이 많아지면 선생님이나 관리실이 찍어 주는 공식 이름표가 더 좋아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 232 / 1108

<- **이전**: [178. OV (Organization Validation) 인증서](/knowledge-base/studynote/09_security/04_endpoint_security/178_ov_organization_validation_certificate/)
**다음**: [180. 인증서 체인 검증 (Certificate Chain of Trust)](/knowledge-base/studynote/09_security/04_endpoint_security/180_certificate_chain_of_trust/) ->

---
