---
title: "162. CRL (Certificate Revocation List) — 폐지 인증서 목록"
date: "2026-05-05"
tags:
  - "studynote-security"
---


## 핵심 인사이트

> 1. **본질**: [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) ([Certificate Revocation List](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/))은 인증서가 만료되기 전이라도 더 이상 신뢰하면 안 되는 인증서의 일련번호를 <strong>인증기관이 서명해 배포하는 폐지 목록</strong>이다.
> 2. **가치**: 개인키 유출, 조직 퇴사, 장비 폐기 같은 사건이 발생했을 때, 유효기간이 남은 인증서라도 <strong>즉시 신뢰에서 제외할 수 있는 최소한의 사후 통제 장치</strong>가 된다.
> 3. **판단 포인트**: CRL은 구조가 단순하고 오프라인 배포에 유리하지만, 목록 크기와 갱신 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 한계가 있어 <strong>대규모 공개 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>에서는 <a href="/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/">OCSP</a> (Online Certificate Status <a href="/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/">Protocol</a>) 등과 함께 판단</strong>해야 한다.

---

## Ⅰ. 개요 및 필요성

CRL은 [공개키 기반 구조](/studynote/03_network/13_network_security_basics/676_pki_public_key_infrastructure/) ([PKI](/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/), [Public Key Infrastructure](/studynote/09_security/uncategorized/1080_pki_public_key_infrastructure_ca_ra_certificate/))에서 더 이상 신뢰할 수 없는 인증서를 별도로 기록한 목록이다. 인증서는 보통 만료일까지 유효하지만, 현실에서는 만료 전에 폐기해야 하는 일이 자주 발생한다. 대표적으로 개인키 유출, 인증서 오발급, 조직 이동, 장비 폐기, [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유권 상실 등이 있다.

만약 이런 사건이 발생했는데도 만료일만 믿고 계속 인증서를 유효하다고 보면, 공격자는 탈취한 키로 정상 서버처럼 위장할 수 있다. 따라서 PKI는 발급만큼이나 "중도 폐기" 메커니즘이 중요하다. CRL은 이 문제를 가장 전통적이고 보편적으로 해결해 온 방식이다.

즉 CRL의 존재 이유는 "유효기간이 남아 있어도 더 이상 믿지 말아야 하는 인증서가 있다"는 사실을 시스템 전체에 공유하는 데 있다. 이 점을 이해해야 [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) ([Certification Authority](/studynote/09_security/03_network_security/160_ca_certification_authority/)), [OCSP](/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/), 인증서 상태 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)이 왜 필요한지도 연결된다.

- **📢 섹션 요약 비유**: CRL은 아직 사용 기간이 남은 출입증이라도 분실 신고가 들어오면 경비실이 "이 번호는 더 이상 통과시키지 마라"라고 공지하는 블랙리스트와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CRL의 기본 원리는 단순하다. 인증기관은 폐지된 인증서의 일련번호와 폐지 시각, 사유 등을 모아 목록을 만들고, 그 목록에 전자서명해 배포한다. [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자는 서버가 제시한 인증서 체인을 확인한 뒤, 해당 인증서 번호가 CRL에 포함되어 있는지 검사한다. 이때 인증서 안에는 보통 [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) 배포 지점 ([CDP](/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/), [CRL Distribution Point](/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/))이 포함되어 있어, [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자가 어디서 목록을 받아야 하는지 알 수 있다.

아래 그림은 [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) 기반 상태 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 흐름을 보여준다.

```text
+--------------------------------------------------------------------+
|                    CRL 기반 인증서 상태 검증 흐름                  |
+--------------------------------------------------------------------+
| [CA] -- 폐지 목록 서명/배포 --> [CRL 저장소]                       |
|   |                                                                |
|   +-- 인증서에 CDP 포함                                            |
|                                                                    |
| [검증자] -- 인증서 수신 --> 일련번호 확인 --> CRL 조회 --> 허용/차단 |
+--------------------------------------------------------------------+
```

이 구조의 강점은 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자가 실시간 질의 없이도 일정 주기로 목록을 내려받아 사용할 수 있다는 점이다. 반면 목록 전체를 받아야 하므로, 폐지 건수가 많아질수록 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 크기와 배포 부담이 커질 수 있다. 이를 보완하기 위해 델타 [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) ([Delta CRL](/studynote/09_security/04_endpoint_security/196_delta_crl_efficiency_improvement/))처럼 변경분만 배포하는 방식도 사용된다.

| 구성 요소 | 역할 | 핵심 포인트 |
| :--- | :--- | :--- |
| [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) | [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·서명 | 목록 무결성과 신뢰의 출발점 |
| [CDP](/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) | [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) 배포 위치 제공 | 인증서에 포함되어 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자가 [참조](/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) |
| [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) 항목 | 폐지된 일련번호, 시각, 사유 | 번호 충돌 없이 정확히 관리되어야 함 |
| [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자 | 인증서와 [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) 대조 | 캐시 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/), 갱신 주기, 실패 처리 중요 |

따라서 CRL의 핵심 원리는 "목록 기반 폐지 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)"이다. 온라인 질의형 프로토콜보다 단순하지만, 그만큼 갱신 주기와 목록 크기 관리가 설계 품질을 좌우한다.

- **📢 섹션 요약 비유**: CRL은 매번 본사에 전화하는 대신, 오늘 사용 금지된 출입증 번호표를 아침마다 받아 두고 경비실에서 대조하는 방식과 같다.

---

## Ⅲ. 비교 및 연결

CRL의 경계는 OCSP와 비교할 때 분명해진다. CRL은 일정 시점의 전체 폐지 목록을 내려받아 확인하는 배치형 접근이고, OCSP는 특정 인증서 하나의 상태를 실시간으로 묻는 질의형 접근이다. 전자는 구조가 단순하고 오프라인·폐쇄망에 유리하지만, 후자는 최신성 면에서 유리하다.

| 항목 | [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) | [OCSP](/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/) |
| :--- | :--- | :--- |
| [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 방식 | 목록 전체 다운로드 후 대조 | 인증서별 실시간 질의 |
| 장점 | 단순, 오프라인 활용 가능, 배치 배포 용이 | 최신 상태 반영, [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 효율 우수 |
| 약점 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 크기 증가, 갱신 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 가능 | 추가 네트워크 왕복, 서버 의존성 |
| 적합 환경 | 폐쇄망, 주기적 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 환경 | 공개 웹 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/), 최신성 중요 환경 |

또한 CRL은 X.509 인증서 체계, [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/)/[RA](/studynote/09_security/03_network_security/161_ra_registration_authority/) ([Registration Authority](/studynote/09_security/03_network_security/161_ra_registration_authority/)), [OCSP](/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/) 스테이플링, 인증서 투명성 ([CT](/studynote/14_data_engineering/04_mlops/162_continuous_training_pipeline_model_retraining/), [Certificate Transparency](/studynote/09_security/04_endpoint_security/165_ct_certificate_transparency/))과도 연결된다. CRL만으로 모든 상태 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 문제를 해결할 수는 없지만, 여전히 많은 환경에서 기본적인 폐지 메커니즘으로 남아 있다. 특히 실시간 외부 질의가 어려운 망에서는 CRL의 존재 가치가 크다.

결국 CRL은 오래된 기술이 아니라, <strong>단순성과 배치 배포라는 장점을 가진 기본 상태 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a> 방식</strong>으로 이해하는 것이 적절하다. 이 관점이 있어야 왜 현대 환경에서 OCSP와 병행되는지도 설명된다.

- **📢 섹션 요약 비유**: CRL이 매일 배포되는 금지 명단이라면, OCSP는 특정 번호 하나를 즉석에서 조회하는 고객센터 전화 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 CRL을 사용할 때 "목록이 있느냐"보다 "얼마나 최신인지, 어떻게 배포되는지, 실패 시 어떻게 동작하는지"를 봐야 한다. 공공기관 폐쇄망, 산업 제어망, 내부 PKI처럼 외부 실시간 질의가 제한된 환경에서는 CRL이 여전히 현실적인 선택이다. 반면 공개 웹 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 CRL만으로 빠른 폐지 반영을 기대하면 갱신 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 [대역폭](/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 문제에 부딪힐 수 있다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. `thisUpdate`, `nextUpdate`를 기준으로 [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) 만료 여부를 엄격히 관리하는가?
2. [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) 저장소가 가용하고, [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자가 적절히 캐시·갱신하는가?
3. 폐지 사유와 일련번호 관리가 정확한가?
4. 대규모 환경이라면 델타 [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) 또는 [OCSP](/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/) 병행 전략이 있는가?
5. [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 실패 시 허용/차단 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 명확히 정의했는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 오래된 CRL을 계속 캐시하면서도 최신성 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 하지 않는 운영
- 공개 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)에서 목록 크기 증가를 무시하고 CRL만으로 실시간 보안을 기대하는 설계
- 네트워크 실패 시 예외 처리 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 없이 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 우회해 버리는 구성

기술사 답안에서는 "CRL은 단순하고 배치 배포에 강하지만, 최신성 한계 때문에 환경에 따라 OCSP와 병행해야 한다"고 정리하면 좋다. 즉 CRL은 폐지 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)의 출발점이지, 모든 환경에서 단독 정답은 아니다.

- **📢 섹션 요약 비유**: [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) 운용은 학교 정문에 붙인 분실 학생증 명단을 매일 새로 갈아 끼우는 일과 같다. 명단이 오래되면 경비가 틀린 판단을 하게 된다.

---

## Ⅴ. 기대효과 및 결론

CRL을 적절히 운영하면 만료 전 사고가 난 인증서를 신속히 신뢰 체계에서 제외할 수 있고, 폐쇄망이나 배치 중심 환경에서도 비교적 단순하게 상태 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)을 구현할 수 있다. 또한 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자가 일정 주기로 목록을 관리하므로, 외부 실시간 연결이 불안정한 곳에서도 기본적인 보안 통제를 유지할 수 있다. 이런 점에서 CRL은 [PKI](/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) 운영의 기초 체력을 담당한다.

하지만 목록이 커질수록 배포 효율이 떨어지고, 갱신 간격이 길수록 최신성 공백이 생긴다. 그래서 현대 인터넷 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 [OCSP](/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/), [OCSP](/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/) 스테이플링, 델타 [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) 같은 보완책을 함께 사용한다. 결국 CRL은 "낡은 방식"이 아니라, <strong>단순성과 배치 운영에 강한 기본 메커니즘</strong>으로 기억하는 것이 맞다.

결론적으로 CRL은 인증서의 중도 폐기를 조직적으로 공유하는 목록 기반 통제 수단이다. 이 본질을 이해하면 왜 PKI에서 발급만큼 폐지가 중요한지, 왜 실시간 질의형 기술이 뒤이어 등장했는지도 자연스럽게 정리된다.

- **📢 섹션 요약 비유**: CRL은 모든 출입문에 공통으로 붙여 두는 사용 금지 명단과 같다. 최신으로 잘 갈아 끼우면 든든하지만, 오래된 명단이면 오히려 위험해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [PKI](/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) ([Public Key Infrastructure](/studynote/09_security/uncategorized/1080_pki_public_key_infrastructure_ca_ra_certificate/)) | CRL이 동작하는 전체 신뢰 인프라 |
| [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) ([Certification Authority](/studynote/09_security/03_network_security/160_ca_certification_authority/)) | [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)과 서명의 주체 |
| [CDP](/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/) ([CRL Distribution Point](/studynote/09_security/04_endpoint_security/193_crl_distribution_point_cdp/)) | [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)자가 CRL을 가져오는 배포 위치 |
| [OCSP](/studynote/03_network/13_network_security_basics/679_ocsp_online_certificate_status_protocol/) (Online Certificate Status [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) | CRL의 최신성 한계를 보완하는 실시간 질의 방식 |
| 델타 [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) ([Delta CRL](/studynote/09_security/04_endpoint_security/196_delta_crl_efficiency_improvement/)) | 변경분만 배포해 [CRL](/studynote/03_network/13_network_security_basics/678_crl_certificate_revocation_list/) 부담을 줄이는 확장 기법 |

### 📈 관련 키워드 및 발전 흐름도

```text
인증서 발급
    |
    v
중도 폐기 필요 발생
    |
    v
CRL (Certificate Revocation List)
    |
    v
델타 CRL · 캐시 최적화
    |
    v
OCSP · OCSP 스테이플링
```

이 흐름은 "발급 중심 [PKI](/studynote/09_security/03_network_security/159_pki_public_key_infrastructure/) -> 폐지 목록 관리 -> 최신성 보완"으로 인증서 상태 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 기술이 발전하는 방향을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 아직 날짜가 남은 학생증이라도 잃어버리면 학교는 그 번호를 더 이상 쓰면 안 된다고 알려야 해요.
2. CRL은 그런 "쓰면 안 되는 학생증 번호 목록"을 모아 놓은 종이예요.
3. 경비 아저씨가 그 목록을 보고 확인하면, 잃어버린 학생증으로 몰래 들어오는 걸 막을 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 215 / 1108

<- **이전**: [161. RA (Registration Authority) — 인증 요청 검증/승인](/studynote/09_security/03_network_security/161_ra_registration_authority/)
**다음**: [163. OCSP (Online Certificate Status Protocol) — 실시간 인증서 상태 질의](/studynote/09_security/04_endpoint_security/163_ocsp_online_certificate_status_protocol/) ->

---
