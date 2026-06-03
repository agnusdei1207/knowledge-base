+++
title = "540. SDDC와 HCI 소프트웨어 정의 데이터센터 (SDDC HCI Software-Defined Datacenter)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [SDDC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/)([Software-Defined Data Center](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/023_sddc_software_defined_data_center/))는 컴퓨팅, 스토리지, 네트워킹 전체를 소프트웨어로 추상화하여 하드웨어 벤더 종속성을 제거하고 자동화된 운영을 실현한다.
> 2. **가치**: [HCI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/)(Hyper-Converged Infrastructure)는 x86 서버 하나에 컴퓨팅·스토리지·네트워킹을 통합하여 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 도입 비용과 관리 복잡성을 동시에 줄인다.
> 3. **판단 포인트**: [SDDC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/)/HCI는 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)와 클라우드의 중간 단계로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 주권과 클라우드 유연성을 동시에 요구하는 [하이브리드 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/) 환경에 최적이다.

---

## Ⅰ. 개요 및 필요성

전통적인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터는 컴퓨팅(서버), 스토리지([SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/)/[NAS](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/)), 네트워크([스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)/라우터)가 벤더별 전용 하드웨어로 분리 운영된다. 이는 구매, 설치, 운영 각각에 전문 인력이 필요하고 자원 활용률이 낮다는 문제가 있다.

<strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/">SDDC</a> 개념</strong>:
- SDC(Software-Defined Computing): [가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)(VMware vSphere, [KVM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/))
- [SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/)(Software-Defined Storage): Ceph, VMware vSAN
- [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)(Software-Defined Networking): 제어 플레인과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플레인 분리

이 세 가지를 통합하여 단일 관리 플랫폼에서 전체 인프라를 소프트웨어로 정의하고 자동화하는 것이 SDDC다.

- **📢 섹션 요약 비유**: 전통 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터는 요리사, 웨이터, 청소부가 각각 다른 사장 밑에서 일하는 식당이다. SDDC는 한 매니저(소프트웨어 플랫폼)가 전체 직원을 통합 관리하는 체인 레스토랑이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

<strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/">SDDC</a> 레이어 구조</strong>:



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">관리 플레인 (Management Plane)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">VMware vCenter / NSX-T / vSAN / Aria Automation</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">제어 플레인 (Control Plane)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SDN 컨트롤러 (OpenDaylight / NSX)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SDS 오케스트레이터 (Ceph Mgr / vSAN)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">데이터 플레인 (Data Plane)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">x86 서버 (vSphere ESXi + vSAN + vNIC)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">HCI 노드 (Nutanix AHV / VMware VSAN ReadyNode)</div></div>
</div>
</div>



| 기술 | 역할 | 대표 솔루션 |
|:---|:---|:---|
| SDC (가상 컴퓨팅) | [VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/), [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 실행 환경 | VMware vSphere, [KVM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/) |
| [SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/) (Software-Defined Storage) | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지 풀, [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 소프트웨어화 | Ceph, VMware vSAN |
| [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) (Software-Defined Networking) | [가상 스위치](/knowledge-base/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/), [방화벽](/knowledge-base/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/), [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 소프트웨어화 | NSX-T, OVN |
| [HCI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/) (Hyper-Converged Infrastructure) | 위 세 가지 통합 단일 어플라이언스 | Nutanix, VMware VSAN |

<strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/">HCI</a>(Hyper-Converged Infrastructure) 특징</strong>:
- 표준 x86 서버에 컴퓨팅(CPU/RAM) + 스토리지([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/)/[HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/)) + 네트워킹을 단일 노드로 통합
- 노드 추가만으로 선형 확장([Scale-Out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)): 3노드 → 6노드 → N노드
- 소프트웨어 정의 스토리지(vSAN, Nutanix AOS)로 노드 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)·[복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)

- **📢 섹션 요약 비유**: [HCI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/) 노드는 레고 블록이다 — 블록을 추가할수록 전체 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 용량이 선형으로 증가하며, 모든 블록이 동일한 규격이라 관리가 단순하다.

---

## Ⅲ. 비교 및 연결

<strong>기존 3계층 아키텍처 vs <a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/">HCI</a></strong>:

| 구분 | 3계층 (서버+[SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/)+네트워크) | [HCI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/) |
|:---|:---|:---|
| 구성 | 전용 하드웨어 계층 분리 | 단일 x86 노드 통합 |
| 확장 | 각 계층 개별 확장 (복잡) | 노드 추가로 선형 확장 (단순) |
| 비용 | 높음 (전용 [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/), [FC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/)) | 낮음 (표준 x86 서버) |
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 높음 (전용 스토리지 최적화) | 중간 ([SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/) 오버헤드) |
| 관리 | 복잡 (다수 관리 콘솔) | 단순 (단일 콘솔) |

<strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/">SDS</a>(Software-Defined Storage) — Ceph</strong>: [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지. 객체 스토리지(RADOS GW), 블록 스토리지([RBD](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/754_rbd/)), [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템(CephFS)을 동시 제공. [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) [영구 스토리지](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/098_kubernetes_storage_volume_pv_pvc/)([PV](/knowledge-base/studynote/12_it_management/04_sdlc_testing/153_pv_planned_value/)) 백엔드로 널리 사용.

<strong><a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/">하이브리드 클라우드</a> 연장</strong>: VMware vSphere 기반 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) HCI를 AWS VMware Cloud로 연결하면 동일한 vSphere 관리 도구로 [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)와 AWS 클라우드를 함께 운영 가능.

- **📢 섹션 요약 비유**: SDS는 기존 금고(전용 [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/))를 없애고, 사무실 직원들(서버 노드)의 서랍을 묶어서 하나의 공용 금고로 만드는 것이다 — 관리는 쉽지만 보안 설계는 더 중요해진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**기술사 시험 판단 포인트**:
1. [SDDC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) = SDC + [SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/) + [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 세 요소의 결합임을 명확히 정의한다.
2. [HCI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/) 확장 방식(노드 추가 = [Scale-Out](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/))을 기존 3계층의 각 계층 개별 확장과 대비한다.
3. [HCI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/) 한계([SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/) 오버헤드, [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 예측 어려움, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 라이선스 비용)도 균형 있게 기술한다.

**실무 시나리오**: 병원의 전자의무기록(EMR) 인프라 현대화 — 레거시 3계층 아키텍처(서버 + NetApp [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) + [Cisco](/knowledge-base/studynote/03_network/10_application_layer_dns_mgmt/539_netflow_sflow_traffic_monitoring/) [FC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/))를 Nutanix [HCI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/) 4노드 클러스터로 교체. 관리 콘솔 통일, [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) 전문 인력 불필요, 99.99% [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) 유지, 향후 노드 추가로 용량 선형 확장 가능.

- **📢 섹션 요약 비유**: [HCI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/) 도입은 자동차 한 대에 엔진·연료·운전석을 통합한 것처럼 — 부품을 따로 사고 조립할 필요 없이 그냥 타면 되는 완성 패키지다.

---

## Ⅴ. 기대효과 및 결론

[SDDC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/)/[HCI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/630_hci/) 도입 기대 효과:
- **관리 단순화**: 단일 플랫폼에서 컴퓨팅/스토리지/네트워크 통합 관리
- **비용 절감**: 전용 [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/)/[FC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/696_fibre_channel_protocol/) [스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 제거로 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 구축 비용 30~50% 절감
- **유연한 확장**: 노드 추가로 온디맨드 확장, 과잉 구매 불필요
- **하이브리드 연장**: [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) HCI를 클라우드로 확장, 일관된 운영 경험

그러나 단일 벤더(VMware/Nutanix) 의존, [SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/) 오버헤드로 인한 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 제약, [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 라이선스 비용 등 한계도 명확히 인지하고 도입 결정해야 한다.

- **📢 섹션 요약 비유**: [SDDC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/631_sddc/)/HCI는 스마트홈 시스템이다 — 조명, 냉난방, 보안을 하나의 앱으로 제어하면 편리하지만, 앱(소프트웨어 플랫폼) 없이는 아무것도 안 되는 의존성이 생긴다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) (Software-Defined Networking) | 제어/[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 플레인 분리, [OpenFlow](/knowledge-base/studynote/03_network/17_sdn_nfv/855_openflow_standard_protocol_sdn_southbound/) · 505 |
| [하이브리드 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/) ([Hybrid Cloud](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/)) | [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 연동, VMware Cloud · 500 |
| Ceph | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지, [오픈소스](/knowledge-base/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/) · 539 |
| 클라우드 마이그레이션 6R | Retain [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), [온프레미스](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 현대화 · 539 |
| [DPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/436_dpu/) ([Data Processing Unit](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/229_dpu_ipu_infrastructure_accelerator_offloading/)) | [가상 스위치](/knowledge-base/studynote/02_operating_system/10_security/630_vswitch_vnf_overhead/) [오프로딩](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/440_offloading/), [SDN](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) 가속 · 526 |

### 📈 관련 키워드 및 발전 흐름도

```text
[제어 · 데이터 플레인 분리] → [SDDC · HCI 소프트웨어 정의 데이터센터] → [가상 스위치 오프로딩 · SDN 가속]
```

### 👶 어린이를 위한 3줄 비유 설명

1. SDDC는 집의 모든 가전제품을 하나의 스마트홈 앱으로 제어하는 것처럼, 서버·저장소·네트워크를 소프트웨어 하나로 관리해요.
2. HCI는 컴퓨터, 저장소, 네트워크를 한 박스에 넣은 것 — 블록처럼 쌓을수록 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 커져요.
3. 기존 방식은 엔진, 바퀴, 핸들을 따로 사서 조립하는 것, HCI는 완성된 자동차를 바로 구매하는 것이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 540 / 552

← **이전**: [539. 클라우드 마이그레이션 6R 전략 (Cloud Migration 6R Strategy)](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/539_cloud_migration_6r_strategy/)
**다음**: [541. 베어메탈 클라우드 가상화 오버헤드 없는 서비스 (Bare Metal Cloud No Hypervisor)](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/541_bare_metal_cloud_no_hypervisor/) →

---
