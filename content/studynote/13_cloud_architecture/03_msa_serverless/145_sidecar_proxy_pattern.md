+++
title = "145. 사이드카 프록시 패턴 (Sidecar Proxy) - Envoy 기반"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 **메인 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)(비즈니스 로직) 옆에 보조 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/)([프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))를 배치**하여, 네트워크 통신의 로드밸런싱·재시도·[mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/)·[메트릭](/knowledge-base/studynote/03_network/07_network_layer_routing/342_routing_metric_hop_bandwidth_delay/)·트레이싱을 투명하게 처리하는 패턴이다.
> 2. **가치**: 통신 로직을 **코드에서 분리**하여 언어·프레임워크에 무관하게 일관된 네트워크 정책을 적용하며, [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 코드는 **비즈니스 로직에만 집중**한다.
> 3. **판단 포인트**: Envoy([Istio](/knowledge-base/studynote/12_it_management/05_security_compliance/302_service_mesh_istio/))·Linkerd-proxy(Linkerd)가 대표이며, [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반([Cilium](/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/))은 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) 없이 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨에서 처리하는 차세대 방식이다.

---

## Ⅰ. 개요 및 필요성

```text
K8s Pod:
  [메인 컨테이너: 비즈니스 로직]
  [사이드카 컨테이너: Envoy Proxy]
    → 모든 인바운드/아웃바운드 트래픽 가로채기
    → LB·재시도·mTLS·메트릭·트레이싱 처리
    → iptables/ebpf로 투명 프록시
```

- **📢 섹션 요약 비유**: [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 **오토바이 [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)**이다. 운전자(메인)는 운전에 집중하고, [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)([프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))가 짐(통신)을 처리한다.

---

## Ⅱ~Ⅴ. 결론

[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/) [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/)는 **[서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 메시의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플레인**이며, Envoy가 사실상 표준이고 eBPF가 차세대이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)** | 보조 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) |
| **Envoy** | L7 [프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/) |
| **iptables** | 트래픽 가로채기 |
| **[mTLS](/knowledge-base/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/)** | 상호 [TLS](/knowledge-base/studynote/02_operating_system/11_exam_summary/694_thread_local_storage_tls/) |
| **[eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/)** | [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
[라이브러리 기반 (~2015)] → [사이드카 프록시 (Envoy, 2016)]
    → [Istio/Linkerd 채택 (2017~)]
    → [Ambient Mesh (사이드카 없는 Istio, 2022)]
    → [현재: Cilium eBPF — 커널 레벨 프록시]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [사이드카](/knowledge-base/studynote/03_network/16_data_center_cloud/830_sidecar_proxy_architecture_envoy_decoupling/)는 **오토바이 옆칸**이에요. 운전자(메인)는 **운전만** 해요.
2. 옆칸([프록시](/knowledge-base/studynote/04_software_engineering/04_testing_quality/264_proxy_pattern_surrogate_access_control/))이 **짐(통신) 처리·보안·기록**을 대신해요.
3. 모든 오토바이에 **같은 옆칸**을 달면 규칙이 통일돼요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 144 / 371

← **이전**: [144. 서비스 메시 (Service Mesh) - 사이드카 기반 통신 인프라](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/144_service_mesh/)
**다음**: [146. mTLS (Mutual TLS) - 서비스 간 상호 인증·암호화](/knowledge-base/studynote/13_cloud_architecture/03_msa_serverless/146_mtls_mutual_tls/) →

---
