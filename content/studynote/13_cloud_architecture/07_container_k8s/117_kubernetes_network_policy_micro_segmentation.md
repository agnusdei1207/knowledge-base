+++
title = "117. K8s Network Policy 마이크로 세그멘테이션 - Pod 간 트래픽 격리·제로 트러스트"
date = 2026-04-19

[taxonomies]
tags = ["studynote-cloud-architecture"]

[extra]
tags = ["studynote-cloud-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: K8s Network Policy는 **[Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 간 네트워크 트래픽을 라벨 기반으로 허용/거부**하는 선언적 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 규칙이며, [마이크로 세그멘테이션](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)([Micro-segmentation](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/059_micro_segmentation_east_west_traffic/))을 통해 클러스터 내부 **East-West 트래픽을 제어**한다.
> 2. **가치**: 기본 K8s는 **모든 [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 간 통신이 허용(Flat Network)**되므로, 하나의 Pod가 침투당하면 클러스터 전체가 위험하다. Network Policy로 **"frontend → backend만 허용, backend → DB만 허용"**처럼 최소 권한을 적용한다.
> 3. **판단 포인트**: Network Policy는 **[CNI](/knowledge-base/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인([Calico](/knowledge-base/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/)·[Cilium](/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/))이 실제 적용**하며, 기본 [CNI](/knowledge-base/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/)([Flannel](/knowledge-base/studynote/03_network/16_data_center_cloud/823_flannel_overlay_cni_vxlan/))는 Network Policy를 지원하지 않는다. Cilium의 L7([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[gRPC](/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 차세대 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│    Network Policy 예시                                │
├───────────────────────────────────────────────────────┤
│  [기본: Flat Network — 모든 Pod 간 통신 허용]         │
│   frontend ←→ backend ←→ db ←→ 모든 Pod             │
│   → 1개 Pod 침투 시 전체 위험                        │
│                                                       │
│  [Network Policy 적용: 마이크로 세그멘테이션]         │
│   frontend → backend:8080 ✅                         │
│   backend → db:5432 ✅                               │
│   frontend → db:5432 ❌ (차단)                       │
│   외부 → frontend:443 ✅ (Ingress)                   │
│   → 최소 권한, 횡이동(Lateral Movement) 차단         │
└───────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: Flat Network는 모든 방 문이 열린 건물이고, Network Policy는 각 방에 카드키(라벨)가 있어야만 들어갈 수 있는 보안 건물이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Network [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 구성 요소

| 요소 | 설명 |
|:---|:---|
| **podSelector** | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 적용될 대상 [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) (라벨) |
| **policyTypes** | [Ingress](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/)(수신) / [Egress](/knowledge-base/studynote/16_bigdata/09_platform/189_egress/)(발신) |
| **[ingress](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/094_ingress_kubernetes_l7_routing_gateway/).from** | 트래픽을 허용할 소스 ([Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/)/[Namespace](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/)/CIDR) |
| **[egress](/knowledge-base/studynote/16_bigdata/09_platform/189_egress/).to** | 트래픽을 허용할 목적지 |
| **ports** | 허용할 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)/[프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) |

### [CNI](/knowledge-base/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) 플러그인별 지원

| [CNI](/knowledge-base/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) | L3/L4 [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | L7 [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) |
|:---|:---|:---|:---|
| **[Flannel](/knowledge-base/studynote/03_network/16_data_center_cloud/823_flannel_overlay_cni_vxlan/)** | ✗ | ✗ | ✗ |
| **[Calico](/knowledge-base/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/)** | ✅ | 일부 | 옵션 |
| **[Cilium](/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/)** | ✅ | **✅ ([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[gRPC](/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/))** | **✅** |

- **📢 섹션 요약 비유**: Calico는 IP·[포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) 기반 [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)(L4)이고, Cilium은 URL 경로까지 검사하는 [WAF](/knowledge-base/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) 수준(L7)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | 기본 ([정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 없음) | L3/L4 [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | L7 [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
|:---|:---|:---|:---|
| **제어 수준** | 없음 | IP·[포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) | **[HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 경로·메서드** |
| **횡이동** | 가능 | **차단** | **정밀 차단** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기본 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/): Default Deny
```yaml
# 모든 Ingress 차단 → 필요한 것만 허용 (화이트리스트)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

---

## Ⅴ. 기대효과 및 결론

| 지표 | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 없음 | Network [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | 개선 |
|:---|:---|:---|:---|
| 횡이동 위험 | 100% | **차단** | [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) |
| 공격 표면 | 전체 [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) | **최소 권한** | 90% 축소 |

Network Policy는 **K8s [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)의 기초**이며, [Cilium](/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반 L7 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 [Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/) 수준의 보안을 달성하는 방향으로 진화하고 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[마이크로 세그멘테이션](/knowledge-base/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)** | Network Policy가 구현하는 보안 원칙 |
| **[Calico](/knowledge-base/studynote/03_network/16_data_center_cloud/824_calico_bgp_routing_cni_network_policy/)** | L3/L4 Network [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) [CNI](/knowledge-base/studynote/03_network/16_data_center_cloud/822_cni_container_network_interface_kubernetes/) |
| **[Cilium](/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/)** | L7 ([HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[gRPC](/knowledge-base/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/)) [Policy](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/), [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 기반 |
| **[제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)** | Network Policy가 기여하는 [보안 아키텍처](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/302_security_architecture_design/) |
| **[Service Mesh](/knowledge-base/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/)** | L7 트래픽 제어의 상위 개념 |

### 📈 관련 키워드 및 발전 흐름도

```text
[Flat Network (K8s 기본 — 모든 Pod 간 통신 허용)]
    │
    ▼
[K8s Network Policy (2017) — L3/L4 Pod 간 격리]
    │
    ▼
[Calico (2018~) — BGP 기반 L3/L4 정책]
    │
    ▼
[Cilium (2020~) — eBPF 기반 L7 정책]
    │
    ▼
[현재: Cilium Service Mesh — Network Policy + L7 관측성 통합]
```

### 👶 어린이를 위한 3줄 비유 설명
1. K8s 기본은 모든 방 문이 열려있는 **자유로운 건물**이에요.
2. Network Policy는 각 방에 **카드키(라벨)**가 있어야만 들어갈 수 있게 해요.
3. 덕분에 나쁜 사람(공격자)이 한 방에 들어와도 **다른 방으로 못 가서** 피해가 줄어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 116 / 371

← **이전**: [116. 컨테이너 이미지 보안 스캐닝 (Container Image Security Scanning) - CVE·SBOM·정책](/knowledge-base/studynote/13_cloud_architecture/07_container_k8s/116_kubernetes_container_image_security_scanning/)
**다음**: [118. OCI 이미지 레지스트리 보안 (Image Registry Security) - 태그 불변성·서명·취약점 정책](/knowledge-base/studynote/13_cloud_architecture/07_container_k8s/118_oci_image_registry_tag_vulnerability/) →

---
