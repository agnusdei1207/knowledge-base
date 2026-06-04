---
title: "330. 마이크로 세그멘테이션 제로 트러스트 네트워크 (Micro-segmentation ZTNA Zero Trust Network Access Cilium eBPF Kubernetes NetworkPolicy)"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)([Micro-segmentation](/studynote/13_cloud_architecture/01_virtualization/059_micro_segmentation_east_west_traffic/))은 네트워크를 작은 보안 구역으로 분리해 공격자가 내부에 침투해도 횡적(Lateral) 이동을 차단하는 [네트워크 보안](/studynote/03_network/20_performance_evaluation_advanced/1117_network_security_zero_trust_policy/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)이다. 경계 보안([Perimeter Security](/studynote/09_security/18_iot_ot_physical/936_perimeter_security/))의 성벽 안은 안전하다는 가정을 버리는 [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust의 핵심 구현체다.
> 2. **ZTNA와 차이**: [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) ([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) Network Access)는 사용자/디바이스 수준의 접근 제어이고, [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)은 워크로드/[서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간 트래픽을 제어한다. 두 기술이 결합되어야 완전한 [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust가 구현된다.
> 3. **판단 포인트**: [Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) 환경에서 [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)은 NetworkPolicy로 기본 구현하고, [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/)([eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 기반)으로 L7 레이어 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)까지 확장한다. eBPF는 [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 수준에서 패킷을 처리해 오버헤드 없이 세분화된 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 적용한다.

---

## Ⅰ. 개요 및 필요성

전통적인 경계 보안은 외부는 위험, 내부는 안전이라는 가정에 기반한다. 하지만 내부 위협, [공급망 공격](/studynote/09_security/15_malware_attack_vectors/764_supply_chain_attack/), [APT](/studynote/09_security/15_malware_attack_vectors/748_apt/) ([Advanced Persistent Threat](/studynote/09_security/04_endpoint_security/374_apt/))로 한 번 침투한 공격자는 내부 네트워크를 자유롭게 이동하며 피해를 확대한다.

[마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)은 어디서든 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)(Verify Everywhere)을 구현한다. 같은 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 내 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 간에도 허용된 트래픽만 통과시키고, 나머지는 모두 차단한다.

> 📢 **섹션 요약 비유**: 기존 보안은 건물 입구([방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/))만 지키는 것이다. [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)은 건물 내 모든 방문에 잠금장치를 달아, 침입자가 들어와도 한 방에만 갇히게 한다.

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
| K8s NetworkPolicy | L3/L4 | 기본 제공, YAML [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) ([eBPF](/studynote/02_operating_system/10_security/615_ebpf/)) | L3/L4/L7 | 고성능, [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/)/[gRPC](/studynote/03_network/09_application_layer_web_email/479_grpc_protobuf_http2/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [Istio](/studynote/12_it_management/05_security_compliance/945_service_mesh_istio/) [Service Mesh](/studynote/03_network/16_data_center_cloud/828_service_mesh_microservice_communication_infrastructure/) | L7 | [mTLS](/studynote/03_network/16_data_center_cloud/831_mtls_mutual_tls_microservices_zero_trust/), 트래픽 암호화 |

> 📢 **섹션 요약 비유**: [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) eBPF는 교통 경찰이 아니라 도로 자체에 내장된 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) [신호](/studynote/02_operating_system/02_process_thread/130_signal/)등이다. 차가 도로에 들어서는 순간 자동으로 허용/차단을 결정해 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 없이 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)을 적용한다.

---

## Ⅲ. 비교 및 연결

| 항목 | 경계 보안 | [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/) |
|:---|:---|:---|
| 보안 가정 | 내부는 안전 | 내부도 위험 |
| 횡적 이동 | 자유 이동 가능 | [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 차단 |
| 가시성 | 경계 트래픽만 | 모든 내부 트래픽 |
| 구현 복잡성 | 낮음 | 높음 ([정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 관리) |

[ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) vs [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/):
- <strong><a href="/studynote/12_it_management/05_security_compliance/980_ztna/">ZTNA</a></strong>: 사용자 -> 애플리케이션 접근 제어 (원격 접근)
- <strong><a href="/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/">마이크로 세그멘테이션</a></strong>: 워크로드 간 네트워크 제어 (동-서 트래픽)

> 📢 **섹션 요약 비유**: ZTNA는 건물 출입증 시스템([사용자 인증](/studynote/02_operating_system/10_security/604_authentication_factors/))이고, [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)은 건물 내 각 방의 열쇠(워크로드 간 접근 제어)다. 둘 다 있어야 완전한 [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 단계적 구현 로드맵

1. **가시성 확보**: 현재 워크로드 간 트래픽 흐름 맵핑 ([Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) Hubble, Wireshark)
2. **기본 NetworkPolicy 적용**: [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/) 간 기본 거부, 필요한 트래픽만 허용
3. <strong><a href="/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/">Cilium</a> 도입</strong>: L7 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) (특정 [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) 경로만 허용) 적용
4. <strong>지속 <a href="/studynote/02_operating_system/04_synchronization/229_monitor/">모니터</a>링</strong>: [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 위반 트래픽 탐지 및 알림

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 기본 거부(Default Deny) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 적용되어 있는가 (허용 목록 방식)?
2. 프로덕션 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)와 개발 [네임스페이스](/studynote/02_operating_system/01_overview_architecture/061_namespace/)가 NetworkPolicy로 격리되는가?
3. [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) Hubble로 모든 내부 트래픽을 가시화하고 있는가?

> 📢 **섹션 요약 비유**: Default Deny [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)은 화이트리스트(허용 목록) 방식이다. 모르는 사람은 모두 차단하고, 아는 사람만 들여보낸다.

---

## Ⅴ. 기대효과 및 결론

[마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/) 적용으로 공격자가 한 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 침해해도 다른 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)로의 이동이 차단된다. 내부 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 유출 경로가 최소화되고, 컴플라이언스([PCI](/studynote/01_computer_architecture/09_system_bus_interconnects/355_pci/)-DSS, [HIPAA](/studynote/09_security/17_framework_compliance/1058_hipaa/)) 요구사항도 충족된다.

[마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)의 핵심은 <strong>"<a href="/studynote/09_security/01_intro_principles/010_least_privilege/">최소 권한 원칙</a>(<a href="/studynote/09_security/01_intro_principles/010_least_privilege/">Least Privilege</a>)의 네트워크 레이어 구현"</strong>이다. 필요한 통신만 허용하고, 나머지는 차단한다.

> 📢 **섹션 요약 비유**: [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)은 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/) 하나로 외부를 막는 대신, 수백 개의 작은 [방화벽](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/)으로 내부 모든 통로를 지키는 것이다. 성벽 하나보다 미로가 더 안전하다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/) | [Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) 핵심 구현체 |
| [ZTNA](/studynote/12_it_management/05_security_compliance/980_ztna/) ([Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) Network Access) | 사용자 레벨 접근 제어 |
| [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) | [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) 기반 K8s 네트워킹/보안 |
| [eBPF](/studynote/02_operating_system/10_security/615_ebpf/) | [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨 고성능 패킷 처리 |
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

1. [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/)은 학교 각 교실에 잠금장치를 다는 거예요. 복도(네트워크)에 들어와도 허락받은 교실([서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))에만 들어갈 수 있어요.
2. [Cilium](/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/) eBPF는 복도 바닥에 내장된 발자국 인식 시스템이에요. 누가 어디로 가는지 즉시 파악하고 차단해요.
3. [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/) Trust는 친구라도 증명해야 들어올 수 있다는 원칙이에요. 예전에 허락받았어도 매번 다시 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 330 / 373

<- **이전**: [329. Secret Manager HashiCorp Vault 시크릿 관리 하드코딩 방지 (Secret Manager HashiCorp](/studynote/11_design_supervision/06_exam_summary/329_process/)
**다음**: [331. CSPM 클라우드 보안 형상 관리 (CSPM Cloud Security Posture Management CIS Benchmark](/studynote/15_devops_sre/05_devsecops/331_cspm/) ->

---
