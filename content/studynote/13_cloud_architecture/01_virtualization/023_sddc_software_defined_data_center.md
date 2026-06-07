---
title: "Sddc Software Defined Data Center"
date: "2026-04-29"
tags:
  - "studynote-cloud-architecture"
weight: 23
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) (Software-Defined [Data Center](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/), [소프트웨어 정의 데이터센터](/studynote/03_network/17_sdn_nfv/858_sddc_software_defined_data_center_infrastructure/))는 컴퓨팅·스토리지·네트워킹·보안 등 모든 인프라 자원을 하드웨어 [종속성](/studynote/15_devops_sre/01_culture_methodology/008_dependencies/) 없이 소프트웨어로 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/)·자동화하여 프로그래밍 가능한(Programmable) [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)를 실현하는 아키텍처 패러다임이다.
> 2. **가치**: SDDC는 물리적 인프라 변경 없이 워크로드를 분 단위로 재배치하고, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출 한 번으로 전체 환경을 [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·확장·[복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하는 인프라의 소프트웨어화를 통해 [하이브리드 클라우드](/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/)와 멀티클라우드 운영 민첩성을 극대화한다.
> 3. **판단 포인트**: [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) 구현 시 SDC (Server [Virtualization](/studynote/06_ict_convergence/03_cloud_infrastructure/190_virtualization_computing_architecture_cloud/)) · [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) (Software-Defined Storage) · [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) (Software-Defined Networking) · NSX (Network [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) 4대 구성 요소의 통합 관리 레이어([Management](/studynote/12_it_management/05_security_compliance/1013_management/) Plane)가 단일 제어점이 되므로, 이 계층의 가용성과 보안이 전체 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)의 복원력을 결정한다.

---

## Ⅰ. 개요 및 필요성

[SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) (Software-Defined [Data Center](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/))는 하드웨어(HW) 자원을 물리적으로 직접 구성하는 전통 방식 대신, 모든 인프라를 소프트웨어 레이어에서 정의하고 API로 제어하는 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 운영 모델이다.

전통 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)에서는 새 서버 도입 시 케이블링·[VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)·스토리지 볼륨 할당에 수 주가 소요되며, 하드웨어 제조사에 종속된 관리 도구가 복잡성을 증폭시킨다. SDDC는 이 모든 과정을 코드([IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/), [Infrastructure as Code](/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/))로 자동화하여 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) 시간을 분 단위로 단축한다.

```text
+----------------------------------------------------------------+
|                    SDDC 계층 구조                               |
+----------------------------------------------------------------+
|                                                                |
|  +-------------------------------------------------+          |
|  |   Management & Automation Layer (vRealize/vSphere)|         |
|  |   — 단일 제어 평면, API, 정책 기반 자동화          |         |
|  +-------------------------------------------------+          |
|          <-> API                <-> API               <-> API        |
|  +--------------+   +--------------+   +--------------+       |
|  |  SDC (서버)  |   |  SDS (스토리지)|  |  SDN (네트워크)|     |
|  |  vSphere/KVM |   |  vSAN/Ceph   |  |  NSX/OpenFlow |      |
|  +--------------+   +--------------+   +--------------+       |
|          <->                    <->                    <->           |
|  +-------------------------------------------------+          |
|  |        물리 하드웨어 (x86 서버, SSD, NIC)         |         |
|  +-------------------------------------------------+          |
+----------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: SDDC는 레고 블록으로 지은 집을 설계도(소프트웨어)만 바꾸면 즉시 다른 모양으로 재조립할 수 있게 한 것과 같다. 벽돌(하드웨어)은 그대로지만, 집 구조(인프라)는 몇 초 만에 바꿀 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) 4대 구성 요소

| 구성 요소 | 기술 | 핵심 기능 |
|:---|:---|:---|
| **SDC (소프트웨어 정의 컴퓨팅)** | VMware vSphere, [KVM](/studynote/01_computer_architecture/15_advanced_topics/713_kvm_over_ip/), Hyper-V | 서버 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/); [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)·[컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 동적 할당 |
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/632_sds/">SDS</a> (소프트웨어 정의 스토리지)</strong> | vSAN, Ceph, NetApp ONTAP | 스토리지 [풀링](/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/), [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 I/O 티어링 |
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/">SDN</a> (<a href="/studynote/03_network/17_sdn_nfv/850_sdn_software_defined_networking_concept/">소프트웨어 정의 네트워킹</a>)</strong> | VMware NSX, [OpenFlow](/studynote/03_network/17_sdn_nfv/855_openflow_standard_protocol_sdn_southbound/), [OVS](/studynote/03_network/17_sdn_nfv/860_ovs_open_vswitch_sdn_openflow/) | [오버레이 네트워크](/studynote/03_network/16_data_center_cloud/815_overlay_network_virtualization_l2_extension/), [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/) |
| <strong><a href="/studynote/09_security/13_secops_ir_forensics/638_security_automation/">보안 자동화</a></strong> | NSX [Firewall](/studynote/03_network/13_network_security_basics/690_firewall_generation_evolution/), [Zero Trust](/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) | 워크로드 이동에 따른 [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/) 자동 적용 |

### [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) 자동화 흐름

```text
+--------------------------------------------------------+
|         IaC 기반 SDDC 프로비저닝 자동화 흐름             |
+--------------------------------------------------------+
|                                                        |
|  개발팀 요청 (API/Git Push)                             |
|       |                                                |
|       v                                                |
|  Terraform/Ansible 실행                                 |
|       |                                                |
|       +- vSphere VM 생성 (SDC)                          |
|       +- vSAN 볼륨 할당 (SDS)                           |
|       +- NSX 네트워크 구성 (SDN)                        |
|       +- 방화벽 정책 자동 적용 (보안)                    |
|       |                                                |
|       v                                                |
|  완료 -> Slack 알림 + CMDB 자동 업데이트                  |
+--------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) 자동화는 주문만 하면 로봇이 서버 꽂기, 케이블 연결, 네트워크 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)까지 자동으로 처리하는 무인 물류 창고와 같다. 사람이 손댈 일이 없고, 주문서(코드) 한 장으로 모든 것이 해결된다.

---

## Ⅲ. 비교 및 연결

| 항목 | 전통 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) | [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) | [퍼블릭 클라우드](/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/) |
|:---|:---|:---|:---|
| <strong><a href="/studynote/09_security/11_iam_access_control/528_provisioning/">프로비저닝</a></strong> | 수 주 | 수 분 | 수 초 |
| <strong>HW <a href="/studynote/15_devops_sre/01_culture_methodology/008_dependencies/">종속성</a></strong> | 높음 | 낮음 | 없음 |
| **운영 비용** | 높음 | 중간 | 사용량 기반 |
| <strong><a href="/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/">데이터 거버넌스</a></strong> | 완전 통제 | 완전 통제 | 클라우드 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 의존 |
| **하이브리드 연계** | 어려움 | 원활 | [CSP](/studynote/09_security/05_web_app_security/475_csp/) 의존 |

SDDC는 [퍼블릭 클라우드](/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)(AWS/Azure)와 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)를 하이브리드로 연결하는 [브리지](/studynote/04_software_engineering/04_testing_quality/260_bridge_pattern_abstraction_implementation/) 역할을 하며, VMware Cloud on AWS처럼 동일한 [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) 관리 인터페이스로 양쪽을 통합 운영하는 것이 주류 구현 패턴이다.

- **📢 섹션 요약 비유**: SDDC는 자사 공장([온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/))과 임대 공장([퍼블릭 클라우드](/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/))을 같은 [ERP](/studynote/07_enterprise_systems/02_erp_systems/081_erp_enterprise_resource_planning/)(관리 소프트웨어)로 한 번에 관리하는 제조업 [스마트 팩토리](/studynote/06_ict_convergence/02_iot_mobility/166_smart_factory/) 플랫폼과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 금융기관 [하이브리드 클라우드](/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/) 전환
규제 요건으로 고객 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)에 유지하면서, 배치 분석 워크로드는 클라우드로 버스팅(Cloud Bursting)해야 한다.

1. <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/631_sddc/">SDDC</a> 구축</strong>: [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)에 VMware vSphere + NSX + vSAN으로 [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) 환경 구성.
2. **하이브리드 연결**: VMware HCX로 [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) ↔ VMware Cloud on AWS 연계.
3. <strong><a href="/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a> 기반 워크로드 이동</strong>: 분석 VM을 야간 배치 시 AWS로 자동 마이그레이션, 완료 후 복귀.
4. **통합 모니터링**: vRealize Operations로 온·오프프레미스 자원 단일 뷰 관리.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/) NSX [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/)이 [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 이동 시에도 자동으로 따라가는지 [검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/).
- [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) 관리 클러스터(vCenter/NSX Manager) 자체의 HA(고가용성) 및 [DR](/studynote/03_network/07_network_layer_routing/360_ospf_dr_bdr_designated_router_lsa_flooding/)([재해 복구](/studynote/04_software_engineering/06_software_architecture/379_dr_architecture/)) 구성.
- [IaC](/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) 코드 저장소(Git)와 [CMDB](/studynote/12_it_management/02_itsm_itil/875_cmdb/)([형상 관리](/studynote/04_software_engineering/01_overview_principles/020_software_configuration_management/) DB)의 실시간 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/).

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- SDDC를 도입하고도 운영팀이 수동으로 VLAN을 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)하고 스토리지를 할당하는 기존 방식을 유지하는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/). SDDC의 자동화 이점을 활용하지 못하고, 수동 작업과 자동화 작업이 혼재되어 형상 불일치([Configuration Drift](/studynote/15_devops_sre/04_iac_cloud_native/193_configuration_drift/))가 발생한다.

- **📢 섹션 요약 비유**: SDDC를 도입하고 수동 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)을 고집하는 건, 자동세탁기를 사서 매번 손빨래하는 것과 같다. 기계는 있지만 편리함이 없다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 | 수치 |
|:---|:---|:---|
| <strong><a href="/studynote/09_security/11_iam_access_control/528_provisioning/">프로비저닝</a> 가속</strong> | [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)·네트워크·스토리지 동시 자동 구성 | 수 주 -> 수 분 |
| **운영 비용 절감** | 자동화로 수동 관리 인력 감소 | OPEX 30~40% 절감 |
| **하이브리드 민첩성** | [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/)·클라우드 통합 운영 | 워크로드 이동 시간 90% 단축 |

SDDC는 VMware의 Broadcom 인수 이후 라이선스 [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 변화로 인해 [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) 대안(OpenStack, Proxmox)으로의 전환 검토가 늘고 있다. [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)([Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/))를 SDDC의 표준 워크로드 실행 환경으로 채택하는 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 네이티브 SDDC로의 진화가 가속화되고 있다.

- **📢 섹션 요약 비유**: SDDC는 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)를 실리콘 기반 하드웨어 덩어리에서, 코드로 정의되고 API로 제어되는 살아있는 소프트웨어로 탈바꿈시키는 디지털 전환의 인프라 기초다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/">SDN</a> (소프트웨어 정의 네트워크)</strong> | SDDC의 네트워크 구성 요소; 오버레이 가상 네트워크 |
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/632_sds/">SDS</a> (소프트웨어 정의 스토리지)</strong> | SDDC의 스토리지 구성 요소; [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 기반 I/O 자동화 |
| <strong><a href="/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/">IaC</a> (<a href="/studynote/15_devops_sre/02_cicd_gitops/062_infrastructure_as_code/">Infrastructure as Code</a>)</strong> | [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) 자동화 수단; [Terraform](/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/)·[Ansible](/studynote/15_devops_sre/05_devsecops/198_ansible_os_configuration_management_ssh/) |
| <strong><a href="/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/">하이브리드 클라우드</a></strong> | SDDC와 [퍼블릭 클라우드](/studynote/13_cloud_architecture/01_virtualization/007_public_cloud/)를 연결하는 운영 모델 |
| <strong>NSX (Network <a href="/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/">Security</a>)</strong> | VMware SDDC의 [마이크로 세그멘테이션](/studynote/03_network/20_performance_evaluation_advanced/1044_micro_segmentation_east_west_traffic_security/) 보안 구성 요소 |

### 📈 관련 키워드 및 발전 흐름도

```text
[서버 가상화 (VMware vSphere) — 컴퓨팅 추상화]
    |
    v
[SDN + SDS — 네트워크·스토리지 소프트웨어화]
    |
    v
[SDDC — 4대 구성 요소 통합 + 단일 관리 플레인]
    |
    v
[하이브리드 클라우드 — SDDC ↔ 퍼블릭 클라우드 통합]
    |
    v
[컨테이너 네이티브 SDDC — Kubernetes + 서비스 메시]
```
서버 [가상화](/studynote/13_cloud_architecture/01_virtualization/015_virtualization/)에서 [SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/)/SDS로 확장, SDDC로 통합되어 [하이브리드 클라우드](/studynote/13_cloud_architecture/01_virtualization/009_hybrid_cloud/)와 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 기반 [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 네이티브 아키텍처로 진화하는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명

1. SDDC는 거대한 레고 도시를 <strong>설계 프로그램</strong>으로 뚝딱뚝딱 만드는 것처럼, 서버·네트워크·저장소를 컴퓨터 코드 몇 줄로 즉시 만들어내는 마법의 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/)예요!
2. 예전에는 새 서버를 쓰려면 몇 주 동안 케이블 꽂고 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)해야 했지만, SDDC에서는 버튼 하나로 수 분 만에 준비돼요.
3. 회사 창고([온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/))와 임대 창고(클라우드)를 같은 앱으로 동시에 관리할 수 있어서, 짐이 많을 때 임대 창고를 즉시 빌릴 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 22 / 371

<- **이전**: [22. 스냅샷 (Snapshot) - 클라우드 스토리지 백업 및 복원 아키텍처](/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/)
**다음**: [24. SDN (Software Defined Networking) — 소프트웨어 정의 네트워킹](/studynote/13_cloud_architecture/01_virtualization/024_sdn_software_defined_networking/) ->

---
