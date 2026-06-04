+++
title = "144. 서비스 메시 (Service Mesh) - 사이드카 기반 통신 인프라"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)는 <strong>각 마이크로서비스에 <a href="/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/">사이드카</a> <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/">프록시</a>(Envoy)를 배치</strong>하여, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신의 <strong>로드밸런싱·<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/307_circuit_breaker_pattern/">서킷 브레이커</a>·<a href="/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/">mTLS</a>·트레이싱·트래픽 제어</strong>를 애플리케이션 코드 변경 없이 인프라 레벨에서 처리하는 패턴이다.
> 2. **가치**: [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 통신 로직(재시도·[타임아웃](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/573_timeout_retry_backoff_strategy/)·암호화)을 <strong>각 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>가 직접 구현하면 중복·불일치</strong>가 발생하지만, [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)는 <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/">사이드카</a>가 일괄 처리</strong>하여 일관성을 보장한다.
> 3. **판단 포인트**: [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)(가장 기능 풍부)·Linkerd(경량)·[Cilium](/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/)([eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반, [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 없음)이 대표이며, 컨트롤 플레인([정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 관리)과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플레인([사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))으로 구성된다.

---

## Ⅰ. 개요 및 필요성

```text
서비스 메시 구조:
  데이터 플레인: Envoy 사이드카 (각 Pod 옆)
    -> 트래픽 가로채기 -> LB·재시도·mTLS·트레이싱
  컨트롤 플레인: Istiod (정책·설정 배포)
    -> VirtualService·DestinationRule 등 CRD
```

- **📢 섹션 요약 비유**: [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)는 <strong>우체국 네트워크</strong>이다. 편지(요청)를 직접 전달하는 대신, 우체부([사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/))가 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)·배달·보안을 대행한다.

---

## Ⅱ~Ⅴ. 결론

[서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)는 <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/619_msa_traffic_hardware/">MSA</a> 통신의 인프라 표준</strong>이며, [Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)(기능)·[Cilium](/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/)([eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))이 주류이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/">서비스 메시</a></strong> | [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 통신 |
| **Envoy** | [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) |
| <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/">Istio</a></strong> | 컨트롤 플레인 |
| <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/">mTLS</a></strong> | [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 암호화 |
| <strong><a href="/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/">Cilium</a></strong> | [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반 (차세대) |

### 📈 관련 키워드 및 발전 흐름도

```text
[라이브러리 기반 (Netflix OSS, 2014)] -> [Linkerd v1 (2017)]
    -> [Istio + Envoy (2017)] -> [Linkerd2 (Rust, 경량)]
    -> [현재: Cilium (eBPF, 사이드카 없음)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [서비스 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/)는 <strong>우체국 시스템</strong>이에요. 편지를 직접 가져가지 않고 <strong>우체부(<a href="/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/">사이드카</a>)</strong>가 배달해요.
2. 우체부가 <strong><a href="/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a>·보안·재배달</strong>을 다 해줘서 보내는 사람은 편해요.
3. 우체국 본부(컨트롤 플레인)가 <strong>모든 우체부에게 규칙</strong>을 알려줘요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 143 / 371

<- **이전**: [143. Strangler Fig 패턴 - 모놀리스->MSA 점진적 전환](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/143_strangler_fig_pattern/)
**다음**: [145. 사이드카 프록시 패턴 (Sidecar Proxy) - Envoy 기반](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/145_sidecar_proxy_pattern/) ->

---
