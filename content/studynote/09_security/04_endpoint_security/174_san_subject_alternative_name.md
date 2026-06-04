---
title: "174. SAN (Subject Alternative Name) — 인증서 다중 이름 확장"
date: "2026-04-05"
tags:
  - "studynote-security"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) (Subject Alternative Name)은 X.509 v3 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 대표할 수 있는 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) ([Domain Name System](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/)) 이름, IP (Internet [Protocol](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) 주소, 이메일, URI (Uniform Resource [Identifier](/studynote/05_database/02_modeling_normalization/088_identifier_in_er_model/))를 확장 필드에 명시하는 메커니즘이다.
> 2. **가치**: 가상 호스팅, 로드밸런서, 멀티도메인 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 환경에서 한 장의 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서로 여러 엔드포인트를 명시적으로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하게 해 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 운영 복잡도를 크게 줄인다.
> 3. **판단 포인트**: 현대 브라우저의 호스트 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)은 Common Name보다 SAN을 우선하며, 이름 집합이 고정적이면 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/), 하위 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)이 계속 늘면 와일드카드, 격리가 중요하면 별도 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 더 적합하다.

---

## Ⅰ. 개요 및 필요성

[SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) (Subject Alternative Name)은 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서의 "추가 신원 목록"이다. 과거에는 Subject의 Common Name 한 칸으로 서버 이름을 표현하는 관행이 많았지만, 한 IP 뒤에 여러 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 모이는 클라우드·로드밸런서·가상 호스팅 환경에서는 이름 하나만으로 현실을 담기 어려웠다. `api.example.com`, `admin.example.com`, `partner.example.net`처럼 서로 다른 접속 지점을 한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 게이트웨이가 처리할 때, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 하나의 이름만 대표하면 나머지는 모두 이름 불일치 오류가 된다.

SAN이 중요한 이유는 단순 편의성 때문만이 아니다. 브라우저와 [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) (Transport Layer [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) 클라이언트는 "내가 접속한 호스트가 이 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 주장하는 이름 집합 안에 있는가"를 기계적으로 판정해야 한다. 즉 SAN은 사람이 읽는 설명란이 아니라, <strong>호스트 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>의 기준 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a></strong>다.

아래 그림은 왜 SAN이 필요해졌는지를 "하나의 게이트웨이, 여러 이름" 관점에서 보여 준다.

```text
+----------------------------------------------------------------------+
| Why SAN became necessary                                             |
+----------------------------------------------------------------------+
| One gateway / one IP                                                 |
|   +- api.example.com                                                 |
|   +- admin.example.com                                               |
|   +- partner.example.net                                             |
|                                                                      |
| Certificate with one name only                                       |
|   +- valid for just one endpoint                                     |
|                                                                      |
| Certificate with SAN list                                            |
|   +- DNS: api.example.com                                            |
|   +- DNS: admin.example.com                                          |
|   +- DNS: partner.example.net                                        |
|                                                                      |
| Result: one certificate can explicitly prove multiple identities     |
+----------------------------------------------------------------------+
```

SAN이 없으면 서버가 안전한 키를 가지고 있어도, 클라이언트는 "접속한 이름과 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서의 이름이 다르다"며 연결을 거부한다. 결국 SAN은 암호화의 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 문제가 아니라, <strong>신뢰의 범위를 정확히 적어 두는 문제</strong>다.

- **📢 섹션 요약 비유**: SAN은 건물 출입증 뒷면에 적힌 "이 사람이 출입할 수 있는 모든 출입문 목록"과 같다. 정문 하나만 적혀 있으면 지하 주차장 문에서는 막히지만, 허용된 문이 목록으로 적혀 있으면 어디서 들어와도 같은 사람으로 확인된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

SAN은 X.509 v3 확장 필드 안에 들어간다. [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 본문에는 Subject, 공개키, 유효기간 같은 기본 정보가 있고, SAN은 그중 "이 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 대변할 수 있는 이름들"을 추가로 적는 역할을 한다. 실무에서는 [CSR](/studynote/09_security/04_endpoint_security/169_pkcs10_csr/) (Certificate Signing Request) 단계에서 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 목록을 선언하고, [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) (Certificate Authority)가 각 이름에 대한 통제권을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)한 뒤 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서로 발급한다.

```text
+----------------------------------------------------------------------+
| TLS hostname validation with SAN                                     |
+----------------------------------------------------------------------+
| Client requests: https://api.example.com                             |
|        |                                                             |
|        v                                                             |
| Server sends certificate                                             |
|   +- Subject CN = www.example.com        (legacy / secondary)        |
|   +- SAN extension                                                   |
|      +- DNS: api.example.com                                         |
|      +- DNS: admin.example.com                                       |
|      +- DNS: *.internal.example.com                                  |
|      +- IP : 10.10.10.5                                              |
|        |                                                             |
| Client matcher                                                       |
|   +- requested host ∈ SAN list  -> continue handshake                |
|   +- requested host ∉ SAN list  -> name mismatch error               |
+----------------------------------------------------------------------+
```

핵심은 SAN이 "추가 정보"가 아니라 <strong>실제 매칭 테이블</strong>이라는 점이다. 특히 [SNI](/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/) ([Server Name Indication](/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/))는 서버가 어떤 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 내보낼지 고르는 힌트이고, SAN은 클라이언트가 받은 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 맞는지 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하는 근거다. 즉 SNI와 SAN은 대체 관계가 아니라, `선택 -> 검증`의 순서로 연결된다.

| [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 엔트리 타입 | 표현 예시 | 주 용도 | 주의점 |
| :--- | :--- | :--- | :--- |
| `dNSName` | `api.example.com` | [Hypertext Transfer Protocol](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) Secure ([HTTPS](/studynote/03_network/09_application_layer_web_email/471_https_http_over_tls/)), [Application Programming Interface](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) ([API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/)), 일반 웹 서버 | 가장 흔한 유형이며 FQDN (Fully Qualified [Domain](/studynote/05_database/02_modeling_normalization/064_relation_domain/) Name) 기준으로 맞춰야 한다. |
| `iPAddress` | `10.10.10.5` | [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 없이 IP로 직접 접속하는 관리망 | 운영 중 IP 변경 가능성이 크므로 재발급 부담을 고려해야 한다. |
| `rfc822Name` | `admin@example.com` | S/[MIME](/studynote/03_network/09_application_layer_web_email/492_mime_multipurpose_internet_mail_extensions/) 메일 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 | 웹 서버 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)과는 별도 목적이다. |
| `uniformResourceIdentifier` | `spiffe://cluster/ns/app` | [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/), 워크로드 ID | URI 자체를 신원으로 쓰는 환경에서 유용하다. |
| wildcard entry | `*.example.com` | 하위 1단계 서브도메인 다수 | 패턴도 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 안에 들어가며, 범위가 넓어질수록 노출 반경도 커진다. |

또 하나의 원리는 <strong>명시성</strong>이다. SAN은 "이름이 많아도 다 알아서 허용"이 아니라, [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 책임질 이름을 구체적으로 열거하거나 패턴으로 한정한다. 그래서 새 호스트가 추가되면 기존 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 자동으로 따라가지 않고, 필요한 경우 재발급이 발생한다. 이것이 번거로워 보여도, 반대로 말하면 <strong>허용 범위를 증명 가능한 방식으로 고정</strong>해 준다는 뜻이다.

- **📢 섹션 요약 비유**: SAN은 택배 주소록과 같다. 택배 기사에게 "아무 집이나 내 집으로 쳐 주세요"가 아니라, 배송 가능한 주소를 정확히 적어 둬야 실수 없이 배달된다.

---

## Ⅲ. 비교 및 연결

SAN을 이해할 때 가장 자주 헷갈리는 대상은 Common Name, [와일드카드 인증서](/studynote/09_security/04_endpoint_security/175_wildcard_certificate/), SNI다. 셋은 비슷해 보이지만 담당하는 질문이 다르다.

| 구분 | [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) | Common Name | Wildcard | [SNI](/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/) |
| :--- | :--- | :--- | :--- | :--- |
| 핵심 질문 | "이 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서는 어떤 이름들까지 유효한가?" | "주체를 어떻게 표시할 것인가?" | "하위 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/) 집합을 패턴으로 표현할 수 있는가?" | "서버는 어떤 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 내보낼 것인가?" |
| 위치 | X.509 v3 확장 필드 | Subject DN (Distinguished Name) 내부 | 보통 SAN의 `dNSName` 값 형태 | [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) ClientHello 확장 |
| 현대 웹 중요도 | 매우 높음 | 보조적 | 상황별 높음 | 매우 높음 |
| 대표 장점 | 다중 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/), 명시적 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | 레거시 호환 | 서브도메인 확장성 | 다중 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 선택 |
| 대표 한계 | 이름 추가 시 재발급 | 단독으로는 호스트 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 불충분 | 범위가 넓어 사고 반경 확대 | [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 기능이 아니라 선택 기능 |

이 비교가 중요한 이유는 운영 판단이 달라지기 때문이다. 예를 들어 `api.example.com`, `admin.example.com`, `billing.partner.net`처럼 <strong><a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a> 집합이 고정되어 있고 서로 다른 <a href="/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a>까지 포함</strong>해야 하면 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 적합하다. 반면 `tenant1.example.com`, `tenant2.example.com`처럼 같은 존 아래 하위 호스트가 계속 늘면 와일드카드가 편할 수 있다. 다만 와일드카드는 보통 한 단계 하위 서브도메인에만 적용되고, 범위가 넓을수록 유출 시 파급 범위가 커진다.

또한 SNI와 SAN을 혼동하면 안 된다. SNI가 없으면 서버가 틀린 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 내보낼 수 있고, SAN이 없으면 클라이언트가 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 받아도 이름을 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 없다. 그래서 멀티도메인 HTTPS는 흔히 `SNI로 인증서 선택 -> SAN으로 이름 검증`의 두 단계를 함께 사용한다.

- **📢 섹션 요약 비유**: SNI는 호텔 프런트에 "몇 호실 손님인지" 알려 주는 말이고, SAN은 받은 객실 키가 정말 그 방을 열 수 있는지 확인하는 열쇠 목록이다. 방 번호를 말해도 키가 틀리면 못 들어가고, 키가 맞아도 프런트가 엉뚱한 키를 주면 역시 못 들어간다.

---

## Ⅳ. 실무 적용 및 기술사 판단

[SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 설계의 핵심은 "몇 개를 넣을 수 있는가"보다 "어디까지 한 장으로 묶어도 되는가"다. [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 하나에 너무 많은 이름을 넣으면 운영은 편해지지만, 개인키 유출·오발급·재발급 시 영향 범위가 함께 커진다. 반대로 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)마다 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 지나치게 쪼개면 자동화와 갱신 비용이 늘어난다. 따라서 SAN은 편의성과 격리 수준 사이의 균형 문제다.

| 운영 상황 | 권장 선택 | 이유 |
| :--- | :--- | :--- |
| 로드밸런서 하나가 3~10개의 고정 FQDN을 처리 | [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 | 명시적 이름 목록 관리가 쉽고 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 수를 줄일 수 있다. |
| 같은 존 아래 서브도메인이 계속 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 와일드카드 또는 와일드카드 + [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) | 신규 서브도메인 추가 때마다 재발급할 부담을 줄인다. |
| 보안 등급이 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 혼재 | [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 분리 | 하나의 키 유출이 전체 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로 번지는 것을 막는다. |
| 사내 [서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/), 워크로드 ID 기반 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) | URI [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 활용 | DNS가 아닌 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ID를 신원으로 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 좋다. |
| [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 대신 IP로 직접 접속하는 관리 구간 | IP [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) | 접속 방식과 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 기준을 일치시킨다. |

### 실무 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [CSR](/studynote/09_security/04_endpoint_security/169_pkcs10_csr/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 실제 접속 호스트명과 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 목록이 정확히 일치하는가?
2. 공용 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)라면 브라우저·모바일 앱·[API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 클라이언트가 모두 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 기준으로 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하도록 되어 있는가?
3. 새 호스트 추가 시 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 재발급, 배포, [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) 절차가 자동화되어 있는가?
4. 내부망 전용 이름이나 사설 주소는 공인 [CA](/studynote/06_ict_convergence/01_blockchain/089_contract_account_smart_contract/) 대신 사설 PKI에서 관리해야 하는가?
5. 와일드카드와 SAN을 혼용할 때 범위가 과도하게 넓어지지 않았는가?

### 자주 발생하는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- Common Name만 넣고 SAN을 비워 둔 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 배포
- 보안 성격이 다른 수십 개의 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)명을 한 장에 과도하게 묶는 구성
- [SNI](/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/) 구성은 했지만 실제 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 목록을 갱신하지 않아 이름 불일치를 일으키는 운영
- IP 접속을 허용하면서 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) SAN만 등록해 두는 불일치

기술사 답안에서는 "[SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) = 멀티도메인용 필드"까지만 쓰면 아쉽다. 더 좋은 답은 <strong>"SAN은 현대 <a href="/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/">TLS</a> 호스트 <a href="/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>의 기준 필드이며, 멀티도메인·와일드카드·<a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> ID 같은 이름 <a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a>을 <a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>서에 기계적으로 인코딩하는 확장"</strong>이라고 정리하는 것이다.

- **📢 섹션 요약 비유**: [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 운영은 우산을 몇 명이 함께 쓸지 정하는 일과 같다. 한 우산을 너무 많이 같이 쓰면 편하지만, 우산 하나가 망가졌을 때 모두가 젖는다. 반대로 우산을 너무 많이 나누면 들고 다니는 짐이 늘어난다.

---

## Ⅴ. 기대효과 및 결론

[SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 덕분에 현대 웹과 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 인프라는 하나의 게이트웨이, 여러 가상 호스트, 자동화된 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 배포를 현실적으로 운영할 수 있게 되었다. 브라우저는 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 목록을 기준으로 이름 일치를 판단하고, 운영팀은 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 수를 줄이면서도 필요한 이름 집합을 명시적으로 통제할 수 있다. 즉 SAN의 효과는 단순 절약이 아니라, <strong>신뢰 범위의 표준화</strong>에 있다.

물론 SAN이 만능은 아니다. 이름이 많아질수록 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 재발급 영향 범위가 커지고, 너무 넓은 와일드카드나 과도한 멀티도메인 구성은 사고 시 blast radius를 키운다. 따라서 기억해야 할 핵심은 "SAN은 가능한 한 많이 넣는 기술"이 아니라 <strong>필요한 이름만 정확히 선언하는 최소 권한형 <a href="/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>서 설계</strong>라는 점이다.

- **📢 섹션 요약 비유**: 좋은 출입증은 모든 문을 열게 만들지 않는다. 꼭 필요한 문만 열리게 해야 편의성과 안전이 함께 지켜진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| X.509 v3 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 | SAN이 포함되는 표준 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 구조다. |
| [CSR](/studynote/09_security/04_endpoint_security/169_pkcs10_csr/) (Certificate Signing Request) | [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 목록을 CA에 전달하는 발급 입력 문서다. |
| [SNI](/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/) ([Server Name Indication](/studynote/03_network/13_network_security_basics/688_sni_esni_ech_encrypted_client_hello/)) | 서버가 어떤 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서를 내보낼지 고르는 [TLS](/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 확장이다. |
| [와일드카드 인증서](/studynote/09_security/04_endpoint_security/175_wildcard_certificate/) | SAN의 `dNSName` 패턴 활용 방식으로 연결된다. |
| [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) (mutual Transport Layer [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) | 서버·클라이언트 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서 모두에서 SAN을 신원 표현에 활용할 수 있다. |
| URI [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) / SPIFFE (Secure Production Identity Framework For Everyone) | 워크로드·[서비스 메시](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) 환경에서 [DNS](/studynote/03_network/10_application_layer_dns_mgmt/511_dns_hierarchical_distributed_architecture/) 외 식별자를 표현한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
Single-name certificate era
    |
    v
X.509 v3 extension model
    |
    v
SAN (DNS / IP / email / URI)
    |
    +- explicit multi-domain validation
    +- wildcard naming strategy
    +- workload identity expression
    |
    v
SNI-based certificate selection
    |
    v
Modern TLS for load balancer, virtual hosting, service mesh
```

이 흐름은 [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)서가 단일 이름 표기에서 출발해, 다중 엔드포인트와 자동화된 현대 인프라를 지탱하는 이름 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 포맷으로 발전한 과정을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. SAN은 한 장의 출입증에 "이 사람이 들어가도 되는 문들"을 여러 개 적어 두는 칸이에요.
2. 그래서 같은 열쇠로도 정문, 옆문, 지하문 중 허락된 문인지 바로 확인할 수 있어요.
3. 하지만 아무 문이나 다 적으면 위험하니까, 정말 필요한 문만 적어 두는 게 중요해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 227 / 1108

<- **이전**: [173. X.509 v3 인증서 — Subject/Issuer/SAN/Key Usage/NSC](/studynote/09_security/04_endpoint_security/173_x509_v3_certificate/)
**다음**: [175. 와일드카드 인증서 (Wildcard Certificate)](/studynote/09_security/04_endpoint_security/175_wildcard_certificate/) ->

---
