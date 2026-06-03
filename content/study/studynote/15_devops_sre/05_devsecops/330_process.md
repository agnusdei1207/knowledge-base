+++
weight = 330
title = "330. 마이크로 세그멘테이션 제로 트러스트 네트워크 (Micro-segmentation ZTNA Zero Trust Network Access Cilium eBPF Kubernetes NetworkPolicy)"
date = "2026-05-09"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]([[059_micro_segmentation_east_west_traffic|Micro-segmentation]])은 네트워크를 작은 보안 구역으로 분리해 공격자가 내부에 침투해도 횡적(Lateral) 이동을 차단하는 [[1117_network_security_zero_trust_policy|네트워크 보안]] [[268_strategy_pattern|전략]]이다. 경계 보안([[936_perimeter_security|Perimeter Security]])의 성벽 안은 안전하다는 가정을 버리는 [[585_zero_skipping|Zero]] Trust의 핵심 구현체다.
> 2. **ZTNA와 차이**: [[339_ztna|ZTNA]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Network Access)는 사용자/디바이스 수준의 접근 제어이고, [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 워크로드/[[090_service_kubernetes_network_load_balancing|서비스]] 간 트래픽을 제어한다. 두 기술이 결합되어야 완전한 [[585_zero_skipping|Zero]] Trust가 구현된다.
> 3. **판단 포인트**: [[205_kubernetes_container_orchestration|Kubernetes]] 환경에서 [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 NetworkPolicy로 기본 구현하고, [[825_cilium_ebpf_kubernetes_networking_security|Cilium]]([[615_ebpf|eBPF]] 기반)으로 L7 레이어 [[164_policy|정책]]까지 확장한다. eBPF는 [[022_kernel_role|커널]] 수준에서 패킷을 처리해 오버헤드 없이 세분화된 [[164_policy|정책]]을 적용한다.

---

## Ⅰ. 개요 및 필요성

전통적인 경계 보안은 외부는 위험, 내부는 안전이라는 가정에 기반한다. 하지만 내부 위협, [[764_supply_chain_attack|공급망 공격]], [[748_apt|APT]] ([[374_apt|Advanced Persistent Threat]])로 한 번 침투한 공격자는 내부 네트워크를 자유롭게 이동하며 피해를 확대한다.

[[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 어디서든 [[395_verification_process_review|검증]](Verify Everywhere)을 구현한다. 같은 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 내 [[090_service_kubernetes_network_load_balancing|서비스]] 간에도 허용된 트래픽만 통과시키고, 나머지는 모두 차단한다.

> 📢 **섹션 요약 비유**: 기존 보안은 건물 입구([[690_firewall_generation_evolution|방화벽]])만 지키는 것이다. [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 건물 내 모든 방문에 잠금장치를 달아, 침입자가 들어와도 한 방에만 갇히게 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
+-----------------------------------------------------------+
|          마이크로 세그멘테이션 구조 (K8s)                  |
+-----------------------------------------------------------+
|                                                           |
|  [기존 - 플랫 네트워크]        [마이크로 세그멘테이션]      |
|  Pod A <-----------> Pod B     Pod A  |  Pod B            |
|  Pod C <-----------> Pod D     -------+-------            |
|  (모든 Pod 간 통신 허용)        Pod C  |  Pod D            |
|                                (정책으로 격리)             |
|                                                           |
|  Cilium eBPF 정책 구조:                                    |
|  L3: IP/CIDR 기반 허용/차단                                |
|  L4: 포트/프로토콜 필터링                                   |
|  L7: HTTP 메서드/경로 필터링 (GET /api/v1만 허용 등)        |
+-----------------------------------------------------------+
```

| 기술 | 레이어 | 특징 |
|:---|:---|:---|
| K8s NetworkPolicy | L3/L4 | 기본 제공, YAML [[164_policy|정책]] |
| [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] ([[615_ebpf|eBPF]]) | L3/L4/L7 | 고성능, [[461_http_stateless_connection_oriented|HTTP]]/[[479_grpc_protobuf_http2|gRPC]] [[164_policy|정책]] |
| [[302_service_mesh_istio|Istio]] [[828_service_mesh_microservice_communication_infrastructure|Service Mesh]] | L7 | [[831_mtls_mutual_tls_microservices_zero_trust|mTLS]], 트래픽 암호화 |

> 📢 **섹션 요약 비유**: [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] eBPF는 교통 경찰이 아니라 도로 자체에 내장된 [[190_ai_llm_requirements_specification|AI]] [[130_signal|신호]]등이다. 차가 도로에 들어서는 순간 자동으로 허용/차단을 결정해 [[015_지연_데이터_관점|지연]] 없이 [[164_policy|정책]]을 적용한다.

---

## Ⅲ. 비교 및 연결

| 항목 | 경계 보안 | [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]] |
|:---|:---|:---|
| 보안 가정 | 내부는 안전 | 내부도 위험 |
| 횡적 이동 | 자유 이동 가능 | [[164_policy|정책]]으로 차단 |
| 가시성 | 경계 트래픽만 | 모든 내부 트래픽 |
| 구현 복잡성 | 낮음 | 높음 ([[164_policy|정책]] 관리) |

[[339_ztna|ZTNA]] vs [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]:
- **[[339_ztna|ZTNA]]**: 사용자 -> 애플리케이션 접근 제어 (원격 접근)
- **[[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]**: 워크로드 간 네트워크 제어 (동-서 트래픽)

> 📢 **섹션 요약 비유**: ZTNA는 건물 출입증 시스템([[604_authentication_factors|사용자 인증]])이고, [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 건물 내 각 방의 열쇠(워크로드 간 접근 제어)다. 둘 다 있어야 완전한 [[585_zero_skipping|Zero]] Trust다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 단계적 구현 로드맵

1. **가시성 확보**: 현재 워크로드 간 트래픽 흐름 맵핑 ([[825_cilium_ebpf_kubernetes_networking_security|Cilium]] Hubble, Wireshark)
2. **기본 NetworkPolicy 적용**: [[061_namespace|네임스페이스]] 간 기본 거부, 필요한 트래픽만 허용
3. **[[825_cilium_ebpf_kubernetes_networking_security|Cilium]] 도입**: L7 [[164_policy|정책]] (특정 [[461_http_stateless_connection_oriented|HTTP]] 경로만 허용) 적용
4. **지속 [[229_monitor|모니터]]링**: [[164_policy|정책]] 위반 트래픽 탐지 및 알림

### [[435_checklist_based_testing|체크리스트]]

1. 기본 거부(Default Deny) [[164_policy|정책]]이 적용되어 있는가 (허용 목록 방식)?
2. 프로덕션 [[061_namespace|네임스페이스]]와 개발 [[061_namespace|네임스페이스]]가 NetworkPolicy로 격리되는가?
3. [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] Hubble로 모든 내부 트래픽을 가시화하고 있는가?

> 📢 **섹션 요약 비유**: Default Deny [[164_policy|정책]]은 화이트리스트(허용 목록) 방식이다. 모르는 사람은 모두 차단하고, 아는 사람만 들여보낸다.

---

## Ⅴ. 기대효과 및 결론

[[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]] 적용으로 공격자가 한 [[090_service_kubernetes_network_load_balancing|서비스]]를 침해해도 다른 [[090_service_kubernetes_network_load_balancing|서비스]]로의 이동이 차단된다. 내부 [[001_dikw_pyramid|데이터]] 유출 경로가 최소화되고, 컴플라이언스([[355_pci|PCI]]-DSS, [[863_hipaa|HIPAA]]) 요구사항도 충족된다.

[[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]의 핵심은 **"[[010_least_privilege|최소 권한 원칙]]([[010_least_privilege|Least Privilege]])의 네트워크 레이어 구현"**이다. 필요한 통신만 허용하고, 나머지는 차단한다.

> 📢 **섹션 요약 비유**: [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 [[690_firewall_generation_evolution|방화벽]] 하나로 외부를 막는 대신, 수백 개의 작은 [[690_firewall_generation_evolution|방화벽]]으로 내부 모든 통로를 지키는 것이다. 성벽 하나보다 미로가 더 안전하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]] | [[667_zero_trust_runtime_integrity_measurement|Zero Trust]] 핵심 구현체 |
| [[339_ztna|ZTNA]] ([[667_zero_trust_runtime_integrity_measurement|Zero Trust]] Network Access) | 사용자 레벨 접근 제어 |
| [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] | [[615_ebpf|eBPF]] 기반 K8s 네트워킹/보안 |
| [[615_ebpf|eBPF]] | [[022_kernel_role|커널]] 레벨 고성능 패킷 처리 |
| Default Deny | 화이트리스트 기반 접근 제어 |
| NetworkPolicy | K8s 기본 네트워크 접근 제어 |

### 📈 관련 키워드 및 발전 흐름도

```text
경계 보안 시대              Zero Trust 등장              현대 마이크로 세그멘테이션
------------------   --------------------------   ------------------------
방화벽 중심 경계     ->  NIST Zero Trust 프레임워크  ->  eBPF 기반 고성능 정책
내부는 안전 가정         Forrester Zero Trust 모델      Cilium + Hubble
VPN 원격 접근            NetworkPolicy (K8s)            서비스 메시 통합
                          ZTNA 솔루션 등장               AI 기반 트래픽 이상 탐지
```

### 👶 어린이를 위한 3줄 비유 설명

1. [[1044_micro_segmentation_east_west_traffic_security|마이크로 세그멘테이션]]은 학교 각 교실에 잠금장치를 다는 거예요. 복도(네트워크)에 들어와도 허락받은 교실([[090_service_kubernetes_network_load_balancing|서비스]])에만 들어갈 수 있어요.
2. [[825_cilium_ebpf_kubernetes_networking_security|Cilium]] eBPF는 복도 바닥에 내장된 발자국 인식 시스템이에요. 누가 어디로 가는지 즉시 파악하고 차단해요.
3. [[585_zero_skipping|Zero]] Trust는 친구라도 증명해야 들어올 수 있다는 원칙이에요. 예전에 허락받았어도 매번 다시 [[396_validation|확인]]해요.
