---
title: 159. PKI (Public Key Infrastructure) — 공개키 인증서 체계
date: '2026-05-05'
tags:
- studynote-security
---

## 핵심 인사이트

> 1. **본질**: PKI ([[984_pki_public_key_infrastructure_ca_ra_certificate|Public Key Infrastructure]])는 공개키 암호를 실제 사회와 인터넷에서 신뢰 가능하게 [[289_cqrs_db|쓰기]] 위해, **[[303_authentication_authorization_patterns|인증]]기관·[[303_authentication_authorization_patterns|인증]]서·[[395_verification_process_review|검증]] 절차를 체계화한 공개키 신뢰 인프라**다.
> 2. **가치**: 서버나 사용자의 공개키가 진짜 주체의 것임을 [[395_verification_process_review|검증]]해 [[706_mitm_man_in_the_middle_hsts|중간자 공격]] (MitM, Man-in-the-Middle) 위험을 줄이고, [[675_digital_signature_process_asymmetric_key|전자서명]]·전송 구간 보안·기기 [[303_authentication_authorization_patterns|인증]]을 가능하게 만든다.
> 3. **판단 포인트**: PKI의 성패는 [[001_algorithm_definition|알고리즘]] 이름보다 [[303_authentication_authorization_patterns|인증]]기관 ([[089_contract_account_smart_contract|CA]], Certificate Authority) 운영, [[303_authentication_authorization_patterns|인증]]서 수명주기, 폐기 [[395_verification_process_review|검증]], 개인키 [[571_protection_vs_security|보호]]를 얼마나 엄격히 설계했는지에 달려 있다.

---

## Ⅰ. 개요 및 필요성

PKI는 공개키 기반 암호를 실무에 적용하기 위한 신뢰 체계다. 공개키 암호만으로는 "이 공개키가 정말 그 서버의 것인가"를 해결할 수 없기 때문에, 제3자의 [[395_verification_process_review|검증]]과 서명 체계가 필요하다. PKI는 바로 이 문제를 풀기 위해 [[303_authentication_authorization_patterns|인증]]기관, 등록 절차, [[303_authentication_authorization_patterns|인증]]서 형식, [[395_verification_process_review|검증]] 규칙을 묶어 놓은 구조다.

이 체계가 필요한 이유는 공개키의 수학적 안전성과 신원의 진위가 별개이기 때문이다. 아무리 강한 [[001_algorithm_definition|알고리즘]]을 써도 공격자가 가짜 공개키를 끼워 넣으면 사용자는 그 키로 안전하게 공격자에게 비밀을 보내게 된다. 그래서 인터넷 규모의 통신에서는 "암호화 가능"보다 먼저 **"누구의 키인지 증명 가능"** 해야 한다.

결국 PKI의 출발점은 암호 기술 그 자체가 아니라 신뢰 문제다. 웹의 [[471_https_http_over_tls|HTTPS]] ([[461_http_stateless_connection_oriented|HyperText Transfer Protocol]] Secure), [[675_digital_signature_process_asymmetric_key|전자서명]], 가상사설망 ([[983_vpn_virtual_private_network|VPN]], Virtual Private Network), [[188_code_signing_software_authentication|코드 서명]], 기기 [[303_authentication_authorization_patterns|인증]]이 모두 이 신뢰 문제를 해결한 덕분에 현실적으로 작동한다.

- **📢 섹션 요약 비유**: PKI는 자물쇠를 만드는 기술만이 아니라, 그 자물쇠가 진짜 은행 금고 것인지 [[396_validation|확인]]해 주는 공증 사무소 시스템과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

PKI의 핵심 구성은 [[303_authentication_authorization_patterns|인증]]기관, 등록기관 ([[161_ra_registration_authority|RA]], [[161_ra_registration_authority|Registration Authority]]), 디지털 [[303_authentication_authorization_patterns|인증]]서, [[303_authentication_authorization_patterns|인증]]서 폐기 목록 ([[678_crl_certificate_revocation_list|CRL]], [[678_crl_certificate_revocation_list|Certificate Revocation List]]) 및 온라인 [[303_authentication_authorization_patterns|인증]]서 상태 [[295_protocol_field_tcp_udp_icmp|프로토콜]] ([[679_ocsp_online_certificate_status_protocol|OCSP]], Online Certificate Status [[295_protocol_field_tcp_udp_icmp|Protocol]]) 같은 폐기 [[395_verification_process_review|검증]] 체계다. 주체는 자신의 공개키와 신원 정보를 등록하고, [[303_authentication_authorization_patterns|인증]]기관은 이를 [[396_validation|확인]]한 뒤 X.509 [[303_authentication_authorization_patterns|인증]]서에 [[675_digital_signature_process_asymmetric_key|전자서명]]한다. [[395_verification_process_review|검증]]자는 이 서명과 [[303_authentication_authorization_patterns|인증]] 경로를 [[396_validation|확인]]해 신뢰 여부를 판단한다.

아래 그림은 [[303_authentication_authorization_patterns|인증]]서 발급과 [[395_verification_process_review|검증]]의 흐름을 요약한 것이다.

```text
┌────────────────────────────────────────────────────────────────────┐
│                 PKI의 발급·검증 신뢰 사슬                         │
├────────────────────────────────────────────────────────────────────┤
│ [발급 단계]                                                       │
│ Subject(서버/사용자) -> RA 신원 확인 -> CA 서명 -> 인증서 발급    │
│                                                                    │
│ [검증 단계]                                                       │
│ Client <- 서버 인증서 제시                                         │
│   │                                                                │
│   ├─ 인증서 유효기간 확인                                          │
│   ├─ 서명자 CA 확인                                                │
│   ├─ Root CA 신뢰 저장소와 체인 검증                              │
│   └─ CRL/OCSP로 폐기 여부 확인                                    │
│                                                                    │
│ 결과: "키를 받음"이 아니라 "키의 주인을 검증함"                 │
└────────────────────────────────────────────────────────────────────┘
```

이 그림의 핵심은 사용자가 서버의 공개키를 그냥 받는 것이 아니라, [[303_authentication_authorization_patterns|인증]] 경로 (Certificate Chain)를 [[395_verification_process_review|검증]]한다는 점이다. 루트 [[303_authentication_authorization_patterns|인증]]기관 (Root [[089_contract_account_smart_contract|CA]])의 공개키는 운영체제나 브라우저의 신뢰 저장소에 미리 탑재되어 있고, 중간 [[303_authentication_authorization_patterns|인증]]기관 (Intermediate [[089_contract_account_smart_contract|CA]])이 그 아래에서 실제 [[303_authentication_authorization_patterns|인증]]서를 발급한다. 사용자는 이 사슬 전체가 끊기지 않고, 유효기간과 폐기 상태까지 문제가 없을 때만 신뢰를 부여한다.

| 구성 요소 | 역할 | 운영상 중요 포인트 |
| :--- | :--- | :--- |
| [[089_contract_account_smart_contract|CA]] | [[303_authentication_authorization_patterns|인증]]서 서명과 신뢰 앵커 제공 | 개인키 [[571_protection_vs_security|보호]], 발급 [[164_policy|정책]] 관리 |
| [[161_ra_registration_authority|RA]] | 신청자 신원 [[396_validation|확인]] | [[395_verification_process_review|검증]] 절차 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]] 확보 |
| X.509 [[303_authentication_authorization_patterns|인증]]서 | 공개키와 신원 바인딩 | 주체명, 유효기간, 용도 포함 |
| [[678_crl_certificate_revocation_list|CRL]]/[[679_ocsp_online_certificate_status_protocol|OCSP]] | [[303_authentication_authorization_patterns|인증]]서 폐기 여부 [[396_validation|확인]] | 해지 반영 속도와 [[452_availability|가용성]] 중요 |
| 루트 저장소 | 최종 신뢰 기준 | OS/브라우저 배포 [[164_policy|정책]]과 연결 |

PKI는 기술 구조이면서 운영 체계이기도 하다. [[303_authentication_authorization_patterns|인증]]기관 개인키가 노출되면 신뢰 체계 전체가 흔들리고, 폐기 [[396_validation|확인]]이 느리면 이미 위험한 [[303_authentication_authorization_patterns|인증]]서를 계속 믿게 된다. 따라서 PKI의 핵심 원리는 "공개키에 서명한다"보다, **신뢰 사슬을 안전하게 운영한다**는 데 있다.

- **📢 섹션 요약 비유**: PKI는 신분증 한 장이 아니라, 신분증을 발급하고 조회하고 말소하는 주민등록 행정 시스템 전체와 같다.

---

## Ⅲ. 비교 및 연결

PKI의 가치는 "그냥 공개키 배포"와 비교할 때 가장 분명해진다. 공개키를 웹페이지나 메일로 직접 배포하면, 공격자가 그 전달 경로를 위조할 때 사용자는 진위를 판단하기 어렵다. 반면 PKI는 제3자 서명을 통해 공개키와 주체를 묶어 준다. 또한 대칭키 기반 사전 공유 방식보다 대규모 인터넷 환경에 더 잘 맞는다. 모든 상대와 미리 비밀키를 교환하지 않아도 되기 때문이다.

| 항목 | 단순 공개키 배포 | 사전 공유키 ([[142_psk_pre_shared_key|PSK]], Pre-Shared [[067_db_key_uniqueness_minimality|Key]]) | PKI |
| :--- | :--- | :--- | :--- |
| 신원 [[395_verification_process_review|검증]] | 약함 | 제한적 | 강함 |
| 확장성 | 낮음 | 참여자 증가 시 관리 어려움 | 대규모 환경에 적합 |
| 관리 포인트 | 배포 경로 신뢰 | 비밀키 배포·교체 | [[303_authentication_authorization_patterns|인증]]서 발급·폐기·체인 관리 |
| 대표 활용 | 실험·폐쇄망 | 소규모 장비 연동 | [[471_https_http_over_tls|HTTPS]], [[675_digital_signature_process_asymmetric_key|전자서명]], [[983_vpn_virtual_private_network|VPN]] |

PKI는 [[694_thread_local_storage_tls|TLS]] (Transport Layer [[283_security_tactics|Security]]), [[188_code_signing_software_authentication|코드 서명]], 전자문서 서명, 스마트카드, 사설 [[303_authentication_authorization_patterns|인증]]체계와 모두 연결된다. 특히 TLS에서는 서버 [[303_authentication_authorization_patterns|인증]]서 [[395_verification_process_review|검증]]을 통해 안전한 [[140_session_key|세션 키]] 교환의 출발점을 만들고, 기업 내부에서는 사설 CA를 통해 기기 [[303_authentication_authorization_patterns|인증]]과 사용자 [[303_authentication_authorization_patterns|인증]]서를 운영하기도 한다. 즉 PKI는 단독 보안 제품이 아니라, **여러 보안 [[295_protocol_field_tcp_udp_icmp|프로토콜]]이 신뢰를 시작하는 기반층**이다.

- **📢 섹션 요약 비유**: 단순 공개키 배포가 명함을 직접 나눠 주는 일이라면, PKI는 국가가 발행한 신분증으로 본인 여부를 [[396_validation|확인]]하는 절차에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 PKI를 설계할 때 가장 중요한 질문은 "공개키를 어떻게 믿게 만들 것인가"보다 "신뢰 체계를 어떻게 운영할 것인가"이다. 공용 웹서비스라면 공인 [[089_contract_account_smart_contract|CA]] [[303_authentication_authorization_patterns|인증]]서와 자동 갱신 체계가 적합하고, 내부 [[090_service_kubernetes_network_load_balancing|서비스]]나 사설망이라면 사설 CA와 단말 루트 배포 [[164_policy|정책]]이 더 중요할 수 있다. 또한 [[303_authentication_authorization_patterns|인증]]서 수명을 짧게 가져가면 폐기 의존도를 줄일 수 있지만, 자동화 없이는 운영 부담이 급격히 커진다.

개인키 [[571_protection_vs_security|보호]]도 핵심 판단 요소다. 루트 [[089_contract_account_smart_contract|CA]] 키나 중요 [[188_code_signing_software_authentication|코드 서명]]키는 [[475_hsm|하드웨어 보안 모듈]] ([[475_hsm|HSM]], [[157_hsm_hardware_security_module|Hardware Security Module]])에 보관하는 것이 일반적이다. 웹 서버 [[303_authentication_authorization_patterns|인증]]서의 경우에도 ACME (Automatic Certificate [[372_management|Management]] [[066_gitlab_flow_environment_branch_strategy|Environment]]) 기반 자동 갱신, [[303_authentication_authorization_patterns|인증]]서 투명성 ([[162_continuous_training_pipeline_model_retraining|CT]], [[165_ct_certificate_transparency|Certificate Transparency]]) [[568_logs_distributed_logging_elk_fluentd|로그]], [[679_ocsp_online_certificate_status_protocol|OCSP]] 스테이플링 ([[680_ocsp_stapling_tls_handshake_performance|OCSP Stapling]]) 같은 운영 기법을 함께 검토해야 한다.

### 판단 [[435_checklist_based_testing|체크리스트]]

1. 공인 CA와 사설 [[089_contract_account_smart_contract|CA]] 중 어느 신뢰 범위가 필요한가?
2. [[303_authentication_authorization_patterns|인증]]서 발급·갱신·폐기 절차가 자동화되어 있는가?
3. 루트/중간 [[089_contract_account_smart_contract|CA]] 개인키 [[571_protection_vs_security|보호]] 수준이 충분한가?
4. 폐기 [[395_verification_process_review|검증]]과 짧은 [[303_authentication_authorization_patterns|인증]]서 수명 전략을 어떻게 조합할 것인가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 루트 [[089_contract_account_smart_contract|CA]] 개인키를 일반 서버 파일시스템에 보관하는 것
- [[303_authentication_authorization_patterns|인증]]서 만료 모니터링 없이 수동 운영에 의존하는 것
- 사설 CA를 도입하고도 단말 신뢰 저장소 배포를 관리하지 않는 것

- **📢 섹션 요약 비유**: PKI 운영은 도장 하나 만드는 일이 아니라, 도장 보관함·발급 창구·폐기 공고판까지 함께 운영하는 관청 시스템과 같다.

---

## Ⅴ. 기대효과 및 결론

PKI의 가장 큰 효과는 서로 처음 만나는 주체들 사이에 신뢰를 빠르게 세울 수 있다는 점이다. [[303_authentication_authorization_patterns|인증]]서를 통해 공개키와 신원을 연결하면, 전송 구간 암호화와 [[675_digital_signature_process_asymmetric_key|전자서명]]의 출발점을 안전하게 만들 수 있다. 이 덕분에 인터넷 규모의 웹 [[090_service_kubernetes_network_load_balancing|서비스]], 기업망, 전자문서, 소프트웨어 배포가 모두 신뢰 가능한 방식으로 운영된다.

하지만 PKI는 복잡하다. [[303_authentication_authorization_patterns|인증]]기관 침해, 잘못된 발급, 폐기 [[015_지연_데이터_관점|지연]], 루트 저장소 [[164_policy|정책]] 문제는 체계 전체를 흔들 수 있다. 따라서 PKI는 "강한 암호를 쓰는 기술"이라기보다, **공개키의 신뢰를 지속적으로 운영하는 사회적·기술적 인프라**로 기억해야 한다.

결론적으로 PKI의 본질은 공개키 그 자체가 아니라 그 공개키를 믿게 만드는 절차와 구조에 있다. 암호화는 수학으로 시작하지만, 인터넷 규모의 신뢰는 결국 운영되는 인프라 위에서 완성된다.

- **📢 섹션 요약 비유**: PKI는 열쇠를 만드는 공장이 아니라, 그 열쇠의 진품 여부를 계속 [[396_validation|확인]]해 주는 국가 [[303_authentication_authorization_patterns|인증]] 체계와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[694_thread_local_storage_tls|TLS]] | PKI를 이용해 서버 [[303_authentication_authorization_patterns|인증]]과 [[160_session_controlling_terminal|세션]] 보안의 출발점을 형성 |
| [[089_contract_account_smart_contract|CA]] | [[303_authentication_authorization_patterns|인증]]서 서명과 신뢰 앵커 제공 |
| X.509 [[303_authentication_authorization_patterns|인증]]서 | 공개키와 주체 정보를 묶는 표준 형식 |
| [[678_crl_certificate_revocation_list|CRL]]/[[679_ocsp_online_certificate_status_protocol|OCSP]] | [[303_authentication_authorization_patterns|인증]]서 해지 여부를 [[396_validation|확인]]하는 메커니즘 |
| [[475_hsm|HSM]] | 고가치 [[089_contract_account_smart_contract|CA]] 개인키 [[571_protection_vs_security|보호]]를 위한 하드웨어 경계 |

### 📈 관련 키워드 및 발전 흐름도

```text
공개키 암호 도입
    │
    ▼
공개키 진위 문제 발생
    │
    ▼
PKI 구축
    ├─ CA/RA 운영
    ├─ X.509 인증서 발급
    ├─ 체인 검증
    └─ CRL/OCSP 폐기 확인
    │
    ▼
HTTPS · 전자서명 · VPN · 기기 인증 확산
```

이 흐름도는 공개키 암호가 실제 [[090_service_kubernetes_network_load_balancing|서비스]] 인프라가 되기 위해, [[001_algorithm_definition|알고리즘]] 위에 별도의 신뢰 운영 체계가 덧붙여졌음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. PKI는 누가 진짜인지 [[396_validation|확인]]해 주는 디지털 신분증 시스템이에요.
2. 그래서 인터넷에서 처음 만난 컴퓨터도 "이 친구가 맞구나" 하고 믿을 수 있어요.
3. 하지만 신분증을 잘 만들고 잘 관리해야만 모두가 안심하고 쓸 수 있어요.
