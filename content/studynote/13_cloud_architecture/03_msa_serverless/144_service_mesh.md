---
title: 144. 서비스 메시 (Service Mesh) - 사이드카 기반 통신 인프라
date: '2026-04-19'
tags:
- studynote-cloud-architecture
---

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [[302_service_mesh_istio|서비스 메시]]는 **각 마이크로서비스에 [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]](Envoy)를 배치**하여, [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신의 **로드밸런싱·[[307_circuit_breaker_pattern|서킷 브레이커]]·[[831_mtls_mutual_tls_microservices_zero_trust|mTLS]]·트레이싱·트래픽 제어**를 애플리케이션 코드 변경 없이 인프라 레벨에서 처리하는 패턴이다.
> 2. **가치**: [[090_service_kubernetes_network_load_balancing|서비스]] 간 통신 로직(재시도·[[573_timeout_retry_backoff_strategy|타임아웃]]·암호화)을 **각 [[090_service_kubernetes_network_load_balancing|서비스]]가 직접 구현하면 중복·불일치**가 발생하지만, [[302_service_mesh_istio|서비스 메시]]는 **[[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]]가 일괄 처리**하여 일관성을 보장한다.
> 3. **판단 포인트**: [[302_service_mesh_istio|Istio]](가장 기능 풍부)·Linkerd(경량)·[[825_cilium_ebpf_kubernetes_networking_security|Cilium]]([[615_ebpf|eBPF]] 기반, [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 없음)이 대표이며, 컨트롤 플레인([[164_policy|정책]] 관리)과 [[001_dikw_pyramid|데이터]] 플레인([[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]])으로 구성된다.

---

## Ⅰ. 개요 및 필요성

```text
서비스 메시 구조:
  데이터 플레인: Envoy 사이드카 (각 Pod 옆)
    → 트래픽 가로채기 → LB·재시도·mTLS·트레이싱
  컨트롤 플레인: Istiod (정책·설정 배포)
    → VirtualService·DestinationRule 등 CRD
```

- **📢 섹션 요약 비유**: [[302_service_mesh_istio|서비스 메시]]는 **우체국 네트워크**이다. 편지(요청)를 직접 전달하는 대신, 우체부([[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]])가 [[104_classification_analysis|분류]]·배달·보안을 대행한다.

---

## Ⅱ~Ⅴ. 결론

[[302_service_mesh_istio|서비스 메시]]는 **[[619_msa_traffic_hardware|MSA]] 통신의 인프라 표준**이며, [[302_service_mesh_istio|Istio]](기능)·[[825_cilium_ebpf_kubernetes_networking_security|Cilium]]([[615_ebpf|eBPF]] [[282_performance_tactics|성능]])이 주류이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[302_service_mesh_istio|서비스 메시]]** | [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] 통신 |
| **Envoy** | [[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]] [[264_proxy_pattern_surrogate_access_control|프록시]] |
| **[[302_service_mesh_istio|Istio]]** | 컨트롤 플레인 |
| **[[831_mtls_mutual_tls_microservices_zero_trust|mTLS]]** | [[090_service_kubernetes_network_load_balancing|서비스]] 간 암호화 |
| **[[825_cilium_ebpf_kubernetes_networking_security|Cilium]]** | [[615_ebpf|eBPF]] 기반 (차세대) |

### 📈 관련 키워드 및 발전 흐름도

```text
[라이브러리 기반 (Netflix OSS, 2014)] → [Linkerd v1 (2017)]
    → [Istio + Envoy (2017)] → [Linkerd2 (Rust, 경량)]
    → [현재: Cilium (eBPF, 사이드카 없음)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. [[302_service_mesh_istio|서비스 메시]]는 **우체국 시스템**이에요. 편지를 직접 가져가지 않고 **우체부([[830_sidecar_proxy_architecture_envoy_decoupling|사이드카]])**가 배달해요.
2. 우체부가 **[[104_classification_analysis|분류]]·보안·재배달**을 다 해줘서 보내는 사람은 편해요.
3. 우체국 본부(컨트롤 플레인)가 **모든 우체부에게 규칙**을 알려줘요!
