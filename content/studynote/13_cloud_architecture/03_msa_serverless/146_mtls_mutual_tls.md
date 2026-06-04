+++
title = "146. mTLS (Mutual TLS) - 서비스 간 상호 인증·암호화"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: mTLS는 <strong>클라이언트와 서버가 양쪽 모두 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>서를 <a href="/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/">검증</a>(상호 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>)</strong>하는 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) 확장이며, [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/))에서 <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 간 통신의 암호화·<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>·<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a></strong>을 보장하는 핵심 메커니즘이다.
> 2. **가치**: 일반 TLS는 <strong>서버만 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a></strong>(클라이언트는 아무나)하지만, mTLS는 <strong>양쪽 모두 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a></strong>하여 [Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 네트워크에서 "네트워크 내부라도 신뢰하지 않는" 원칙을 실현한다.
> 3. **판단 포인트**: [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/))가 <strong>자동 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>서 발급·회전·<a href="/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/">mTLS</a> 적용</strong>을 사이드카에서 처리하므로, 애플리케이션 코드 변경 없이 적용된다.

---

## Ⅰ. 개요 및 필요성

```text
TLS:   클라이언트 -> 서버 인증서 검증 (서버만 인증)
mTLS:  클라이언트 ↔ 서버 양쪽 인증서 교환·검증
  -> Zero Trust: 내부 네트워크도 암호화
  Istio: 자동 인증서 발급 -> Envoy 사이드카에서 mTLS
```

- **📢 섹션 요약 비유**: TLS는 <strong>신분증 <a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a>(서버만)</strong>, mTLS는 <strong>양쪽 모두 신분증 <a href="/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/">확인</a></strong>이다.

---

## Ⅱ~Ⅴ. 결론

mTLS는 <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">Zero Trust</a>·<a href="/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/">서비스 메시</a>의 보안 핵심</strong>이며, Istio가 자동화를 제공한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/">mTLS</a></strong> | 상호 [인증](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/">Zero Trust</a></strong> | 내부도 불신 |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/">Istio</a></strong> | 자동 [mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/) |
| <strong><a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>서 회전</strong> | 자동 갱신 |
| **SPIFFE** | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) ID 표준 |

### 📈 관련 키워드 및 발전 흐름도

```text
[평문 통신 (~2015)] -> [TLS (서버 인증)]
    -> [mTLS (상호 인증, 2017~)]
    -> [Istio 자동 mTLS (2018)]
    -> [현재: SPIFFE/SPIRE — 서비스 ID 표준]
```

### 👶 어린이를 위한 3줄 비유 설명
1. TLS는 <strong>가게(서버)만 신분증</strong>을 보여주는 거예요.
2. mTLS는 <strong>손님(클라이언트)도 신분증</strong>을 보여야 들어갈 수 있어요.
3. 이렇게 하면 <strong>가짜 손님</strong>이 못 들어와서 안전해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 145 / 371

<- **이전**: [145. 사이드카 프록시 패턴 (Sidecar Proxy) - Envoy 기반](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/145_sidecar_proxy_pattern/)
**다음**: [147. DDD (Domain-Driven Design) - 도메인 주도 설계](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/147_ddd_domain_driven_design/) ->

---
