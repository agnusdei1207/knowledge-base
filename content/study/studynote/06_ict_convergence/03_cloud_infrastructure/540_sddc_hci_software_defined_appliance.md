+++
weight = 540
title = "540. SDDC와 HCI 소프트웨어 정의 데이터센터 (SDDC HCI Software-Defined Datacenter)"
date = "2026-05-09"
[extra]
categories = "studynote-ict-convergence"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[631_sddc|SDDC]]([[023_sddc_software_defined_data_center|Software-Defined Data Center]])는 컴퓨팅, 스토리지, 네트워킹 전체를 소프트웨어로 추상화하여 하드웨어 벤더 종속성을 제거하고 자동화된 운영을 실현한다.
> 2. **가치**: [[630_hci|HCI]](Hyper-Converged Infrastructure)는 x86 서버 하나에 컴퓨팅·스토리지·네트워킹을 통합하여 [[459_quic_fec_forward_error_correction|초기]] 도입 비용과 관리 복잡성을 동시에 줄인다.
> 3. **판단 포인트**: [[631_sddc|SDDC]]/HCI는 [[061_on_premise_legacy_infrastructure|온프레미스]]와 클라우드의 중간 단계로, [[001_dikw_pyramid|데이터]] 주권과 클라우드 유연성을 동시에 요구하는 [[009_hybrid_cloud|하이브리드 클라우드]] 환경에 최적이다.

---

## Ⅰ. 개요 및 필요성

전통적인 [[001_dikw_pyramid|데이터]]센터는 컴퓨팅(서버), 스토리지([[493_san_storage_area_network|SAN]]/[[492_nas_network_attached_storage|NAS]]), 네트워크([[238_switch_operation_principles|스위치]]/라우터)가 벤더별 전용 하드웨어로 분리 운영된다. 이는 구매, 설치, 운영 각각에 전문 인력이 필요하고 자원 활용률이 낮다는 문제가 있다.

**[[631_sddc|SDDC]] 개념**:
- SDC(Software-Defined Computing): [[015_virtualization|가상화]](VMware vSphere, [[713_kvm_over_ip|KVM]])
- [[632_sds|SDS]](Software-Defined Storage): Ceph, VMware vSAN
- [[633_sdn_whitebox|SDN]](Software-Defined Networking): 제어 플레인과 [[001_dikw_pyramid|데이터]] 플레인 분리

이 세 가지를 통합하여 단일 관리 플랫폼에서 전체 인프라를 소프트웨어로 정의하고 자동화하는 것이 SDDC다.

- **📢 섹션 요약 비유**: 전통 [[001_dikw_pyramid|데이터]]센터는 요리사, 웨이터, 청소부가 각각 다른 사장 밑에서 일하는 식당이다. SDDC는 한 매니저(소프트웨어 플랫폼)가 전체 직원을 통합 관리하는 체인 레스토랑이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

**[[631_sddc|SDDC]] 레이어 구조**:

```
┌──────────────────────────────────────────────────────────────┐
│              관리 플레인 (Management Plane)                    │
│  VMware vCenter / NSX-T / vSAN / Aria Automation             │
├──────────────────────────────────────────────────────────────┤
│              제어 플레인 (Control Plane)                       │
│  SDN 컨트롤러 (OpenDaylight / NSX)                            │
│  SDS 오케스트레이터 (Ceph Mgr / vSAN)                          │
├──────────────────────────────────────────────────────────────┤
│              데이터 플레인 (Data Plane)                        │
│  x86 서버 (vSphere ESXi + vSAN + vNIC)                       │
│  HCI 노드 (Nutanix AHV / VMware VSAN ReadyNode)              │
└──────────────────────────────────────────────────────────────┘
```

| 기술 | 역할 | 대표 솔루션 |
|:---|:---|:---|
| SDC (가상 컴퓨팅) | [[598_vm_migration_nic|VM]], [[561_container_based_deployment|컨테이너]] 실행 환경 | VMware vSphere, [[713_kvm_over_ip|KVM]] |
| [[632_sds|SDS]] (Software-Defined Storage) | [[136_variance|분산]] 스토리지 풀, [[483_raid_overview|RAID]] 소프트웨어화 | Ceph, VMware vSAN |
| [[633_sdn_whitebox|SDN]] (Software-Defined Networking) | [[630_vswitch_vnf_overhead|가상 스위치]], [[690_firewall_generation_evolution|방화벽]], [[339_routing_overview_best_path_selection|라우팅]] 소프트웨어화 | NSX-T, OVN |
| [[630_hci|HCI]] (Hyper-Converged Infrastructure) | 위 세 가지 통합 단일 어플라이언스 | Nutanix, VMware VSAN |

**[[630_hci|HCI]](Hyper-Converged Infrastructure) 특징**:
- 표준 x86 서버에 컴퓨팅(CPU/RAM) + 스토리지([[327_ssd|SSD]]/[[465_hdd_structure|HDD]]) + 네트워킹을 단일 노드로 통합
- 노드 추가만으로 선형 확장([[202_scale_out_distributed_horizontal_expansion|Scale-Out]]): 3노드 → 6노드 → N노드
- 소프트웨어 정의 스토리지(vSAN, Nutanix AOS)로 노드 간 [[001_dikw_pyramid|데이터]] [[136_variance|분산]]·[[016_replication_factor|복제]]

- **📢 섹션 요약 비유**: [[630_hci|HCI]] 노드는 레고 블록이다 — 블록을 추가할수록 전체 [[282_performance_tactics|성능]]과 용량이 선형으로 증가하며, 모든 블록이 동일한 규격이라 관리가 단순하다.

---

## Ⅲ. 비교 및 연결

**기존 3계층 아키텍처 vs [[630_hci|HCI]]**:

| 구분 | 3계층 (서버+[[493_san_storage_area_network|SAN]]+네트워크) | [[630_hci|HCI]] |
|:---|:---|:---|
| 구성 | 전용 하드웨어 계층 분리 | 단일 x86 노드 통합 |
| 확장 | 각 계층 개별 확장 (복잡) | 노드 추가로 선형 확장 (단순) |
| 비용 | 높음 (전용 [[493_san_storage_area_network|SAN]], [[696_fibre_channel_protocol|FC]] [[238_switch_operation_principles|스위치]]) | 낮음 (표준 x86 서버) |
| [[282_performance_tactics|성능]] | 높음 (전용 스토리지 최적화) | 중간 ([[632_sds|SDS]] 오버헤드) |
| 관리 | 복잡 (다수 관리 콘솔) | 단순 (단일 콘솔) |

**[[632_sds|SDS]](Software-Defined Storage) — Ceph**: [[191_oss_license_compliance|오픈소스]] [[136_variance|분산]] 스토리지. 객체 스토리지(RADOS GW), 블록 스토리지([[754_rbd|RBD]]), [[501_file_definition_logical_record|파일]] 시스템(CephFS)을 동시 제공. [[205_kubernetes_container_orchestration|Kubernetes]] [[098_kubernetes_storage_volume_pv_pvc|영구 스토리지]]([[153_pv_planned_value|PV]]) 백엔드로 널리 사용.

**[[009_hybrid_cloud|하이브리드 클라우드]] 연장**: VMware vSphere 기반 [[061_on_premise_legacy_infrastructure|온프레미스]] HCI를 AWS VMware Cloud로 연결하면 동일한 vSphere 관리 도구로 [[061_on_premise_legacy_infrastructure|온프레미스]]와 AWS 클라우드를 함께 운영 가능.

- **📢 섹션 요약 비유**: SDS는 기존 금고(전용 [[493_san_storage_area_network|SAN]])를 없애고, 사무실 직원들(서버 노드)의 서랍을 묶어서 하나의 공용 금고로 만드는 것이다 — 관리는 쉽지만 보안 설계는 더 중요해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술사 시험 판단 포인트**:
1. [[631_sddc|SDDC]] = SDC + [[632_sds|SDS]] + [[633_sdn_whitebox|SDN]] 세 요소의 결합임을 명확히 정의한다.
2. [[630_hci|HCI]] 확장 방식(노드 추가 = [[202_scale_out_distributed_horizontal_expansion|Scale-Out]])을 기존 3계층의 각 계층 개별 확장과 대비한다.
3. [[630_hci|HCI]] 한계([[632_sds|SDS]] 오버헤드, [[282_performance_tactics|성능]] 예측 어려움, [[459_quic_fec_forward_error_correction|초기]] 라이선스 비용)도 균형 있게 기술한다.

**실무 시나리오**: 병원의 전자의무기록(EMR) 인프라 현대화 — 레거시 3계층 아키텍처(서버 + NetApp [[493_san_storage_area_network|SAN]] + [[539_netflow_sflow_traffic_monitoring|Cisco]] [[696_fibre_channel_protocol|FC]] [[238_switch_operation_principles|스위치]])를 Nutanix [[630_hci|HCI]] 4노드 클러스터로 교체. 관리 콘솔 통일, [[493_san_storage_area_network|SAN]] 전문 인력 불필요, 99.99% [[452_availability|가용성]] 유지, 향후 노드 추가로 용량 선형 확장 가능.

- **📢 섹션 요약 비유**: [[630_hci|HCI]] 도입은 자동차 한 대에 엔진·연료·운전석을 통합한 것처럼 — 부품을 따로 사고 조립할 필요 없이 그냥 타면 되는 완성 패키지다.

---

## Ⅴ. 기대효과 및 결론

[[631_sddc|SDDC]]/[[630_hci|HCI]] 도입 기대 효과:
- **관리 단순화**: 단일 플랫폼에서 컴퓨팅/스토리지/네트워크 통합 관리
- **비용 절감**: 전용 [[493_san_storage_area_network|SAN]]/[[696_fibre_channel_protocol|FC]] [[238_switch_operation_principles|스위치]] 제거로 [[459_quic_fec_forward_error_correction|초기]] 구축 비용 30~50% 절감
- **유연한 확장**: 노드 추가로 온디맨드 확장, 과잉 구매 불필요
- **하이브리드 연장**: [[061_on_premise_legacy_infrastructure|온프레미스]] HCI를 클라우드로 확장, 일관된 운영 경험

그러나 단일 벤더(VMware/Nutanix) 의존, [[632_sds|SDS]] 오버헤드로 인한 [[282_performance_tactics|성능]] 제약, [[459_quic_fec_forward_error_correction|초기]] 라이선스 비용 등 한계도 명확히 인지하고 도입 결정해야 한다.

- **📢 섹션 요약 비유**: [[631_sddc|SDDC]]/HCI는 스마트홈 시스템이다 — 조명, 냉난방, 보안을 하나의 앱으로 제어하면 편리하지만, 앱(소프트웨어 플랫폼) 없이는 아무것도 안 되는 의존성이 생긴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[633_sdn_whitebox|SDN]] (Software-Defined Networking) | 제어/[[001_dikw_pyramid|데이터]] 플레인 분리, [[855_openflow_standard_protocol_sdn_southbound|OpenFlow]] · 505 |
| [[009_hybrid_cloud|하이브리드 클라우드]] ([[009_hybrid_cloud|Hybrid Cloud]]) | [[061_on_premise_legacy_infrastructure|온프레미스]] 연동, VMware Cloud · 500 |
| Ceph | [[136_variance|분산]] 스토리지, [[191_oss_license_compliance|오픈소스]] [[632_sds|SDS]] · 539 |
| 클라우드 마이그레이션 6R | Retain [[268_strategy_pattern|전략]], [[061_on_premise_legacy_infrastructure|온프레미스]] 현대화 · 539 |
| [[436_dpu|DPU]] ([[229_dpu_ipu_infrastructure_accelerator_offloading|Data Processing Unit]]) | [[630_vswitch_vnf_overhead|가상 스위치]] [[440_offloading|오프로딩]], [[633_sdn_whitebox|SDN]] 가속 · 526 |

### 📈 관련 키워드 및 발전 흐름도

```text
[제어 · 데이터 플레인 분리] → [SDDC · HCI 소프트웨어 정의 데이터센터] → [가상 스위치 오프로딩 · SDN 가속]
```

### 👶 어린이를 위한 3줄 비유 설명

1. SDDC는 집의 모든 가전제품을 하나의 스마트홈 앱으로 제어하는 것처럼, 서버·저장소·네트워크를 소프트웨어 하나로 관리해요.
2. HCI는 컴퓨터, 저장소, 네트워크를 한 박스에 넣은 것 — 블록처럼 쌓을수록 [[282_performance_tactics|성능]]이 커져요.
3. 기존 방식은 엔진, 바퀴, 핸들을 따로 사서 조립하는 것, HCI는 완성된 자동차를 바로 구매하는 것이에요.
