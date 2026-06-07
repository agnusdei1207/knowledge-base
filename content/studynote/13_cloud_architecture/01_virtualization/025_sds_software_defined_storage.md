---
title: "025. Sds Software Defined Storage"
date: "2026-04-29"
tags:
  - "studynote-cloud-architecture"
weight: 25
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) ([Software Defined Storage](/studynote/01_computer_architecture/15_advanced_topics/632_sds/), 소프트웨어 정의 스토리지)는 스토리지 하드웨어([HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/), [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/), [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/))와 제어 소프트웨어를 분리(Disaggregation)하여, 이기종 하드웨어를 추상화하고 단일 API로 제어하는 스토리지 아키텍처다.
> 2. **가치**: SDS는 고가의 전용 스토리지 어플라이언스(EMC, NetApp) 의존도를 줄이고 상용 x86 서버 + [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) 소프트웨어(Ceph, [GlusterFS](/studynote/01_computer_architecture/15_advanced_topics/679_glusterfs/), VMware vSAN)로 동일한 기능을 더 낮은 비용에 제공한다. 스케일아웃([Scale-out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/)) 방식으로 페타바이트 규모까지 선형적으로 용량을 확장한다.
> 3. **판단 포인트**: SDS는 [SDDC](/studynote/01_computer_architecture/15_advanced_topics/631_sddc/) (Software Defined [Data Center](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/), [소프트웨어 정의 데이터센터](/studynote/03_network/17_sdn_nfv/858_sddc_software_defined_data_center_infrastructure/))의 3대 구성 요소([SDN](/studynote/01_computer_architecture/15_advanced_topics/633_sdn_whitebox/), [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/), SDVC) 중 하나로, [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 환경([Kubernetes](/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/))에서 [PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) (Persistent [Volume](/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/) Claim)를 통해 영구 스토리지를 동적으로 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/)하는 [CSI](/studynote/12_it_management/02_itsm_itil/068_csi/) ([Container Storage Interface](/studynote/13_cloud_architecture/02_iaas_paas_saas/099_csi_container_storage_interface_kubernetes_plugin/)) 드라이버로 구현된다.

---

## Ⅰ. 개요 및 필요성

전통적 스토리지는 하드웨어+소프트웨어가 단일 어플라이언스로 통합되어, [벤더 종속](/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/), 고비용, 수직적 확장([Scale-up](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/)) 한계를 가졌다.

```text
+-----------------------------------------------------------+
|         SDS 핵심 아키텍처                                   |
+-----------------------------------------------------------+
|                                                           |
|  [앱 계층]    K8s PVC / NFS / S3 API / Block API          |
|       |                                                   |
|  [SDS 계층]   Ceph / GlusterFS / vSAN / Longhorn          |
|       |       (데이터 배치, 복제, 복구, 티어링)             |
|       |                                                   |
|  [물리 계층]   x86 서버 + HDD / SSD / NVMe                 |
|               (이기종 하드웨어 추상화)                      |
+-----------------------------------------------------------+
```

SDS의 3가지 스토리지 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/):
- **블록 스토리지(Block)**: [데이터베이스](/studynote/05_database/01_db_architecture_relational/002_database_definition/), [VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/) 디스크
- <strong><a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 스토리지(<a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">File</a>)</strong>: [NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/)/SMB, 공유 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)시스템
- <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/">오브젝트 스토리지</a>(Object)</strong>: S3 호환, 대규모 [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)

- **📢 섹션 요약 비유**: SDS는 LEGO 스토리지 시스템이다. 어떤 브랜드의 블록(하드웨어)이든 조립해서 원하는 모양(스토리지 [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/))을 만들 수 있다. 전용 LEGO 세트(전용 어플라이언스)가 필요 없다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### Ceph — [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) 레퍼런스 아키텍처

```text
+------------------------------------------------------------+
|                  Ceph 아키텍처                               |
+------------------------------------------------------------+
|                                                            |
|  [클라이언트]                                               |
|  librados / S3 API / RBD / CephFS                         |
|       |                                                    |
|  [RADOS (Reliable Autonomic Distributed Object Store)]    |
|  MON (모니터) - 클러스터 상태 관리                          |
|  OSD (Object Storage Daemon) - 실제 데이터 저장·복제        |
|  MGR (Manager) - 메트릭, 대시보드                           |
|  MDS (Metadata Server) - CephFS 파일 메타데이터             |
|       |                                                    |
|  [CRUSH 알고리즘] - 데이터 배치 결정 (중앙 조회 없이)        |
+------------------------------------------------------------+
```

### K8s [CSI](/studynote/12_it_management/02_itsm_itil/068_csi/) 기반 동적 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/)

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ceph-rbd
provisioner: rbd.csi.ceph.com
parameters:
  pool: kubernetes
reclaimPolicy: Delete
volumeBindingMode: Immediate
---
# PVC 생성 시 자동으로 Ceph에서 볼륨 할당
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  storageClassName: ceph-rbd
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 100Gi
```

- **📢 섹션 요약 비유**: SDS의 동적 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/)은 클라우드 호텔 예약이다. 방이 필요하면([PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) 요청) 즉시 방이 생기고(볼륨 할당), 체크아웃하면([PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) 삭제) 방이 자동으로 정리된다(볼륨 삭제).

---

## Ⅲ. 비교 및 연결

| 항목 | 전통 [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/)/[NAS](/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/) | [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) (Ceph/vSAN) |
|:---|:---|:---|
| **확장 방식** | [Scale-up](/studynote/01_computer_architecture/15_advanced_topics/621_scale_up_system_bus/) (고가 어플라이언스 교체) | [Scale-out](/studynote/14_data_engineering/05_exam_keywords/202_scale_out_distributed_horizontal_expansion/) (노드 추가) |
| <strong><a href="/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/">벤더 종속</a></strong> | 높음 (EMC, NetApp 전용) | 낮음 (x86 범용 하드웨어) |
| **비용** | 높음 (라이선스+HW) | 낮음 ([OSS](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) + [COTS](/studynote/04_software_engineering/06_software_architecture/372_cots/)) |
| <strong><a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong> | 벤더별 상이 | S3, [CSI](/studynote/12_it_management/02_itsm_itil/068_csi/) 표준 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) |

- **📢 섹션 요약 비유**: 전통 스토리지는 특정 브랜드 전용 자동차 부품이고, SDS는 모든 차에 맞는 범용 부품이다. 부품이 범용화되면 선택의 폭이 넓어지고 가격이 내려간다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 공공 클라우드 [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) 구축 (Ceph + OpenStack)
1. 상용 스토리지 어플라이언스(EMC) 교체 -> x86 서버 30대 + Ceph 구축.
2. 비용: 어플라이언스 3억 -> x86+Ceph 8,000만원 (73% 절감).
3. [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/): IOPS 30% 향상 ([NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) OSD 노드 활용).
4. [가용성](/studynote/01_computer_architecture/13_reliability_power_management/452_availability/): 3-way [복제](/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) + Ceph 자동 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) -> 노드 장애 시 5분 내 자동 재균형.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- 단순 비용 절감만 보고 SDS를 도입했으나 운영 전문성 부족으로 장애 대응 실패. SDS는 소프트웨어 복잡성(CRUSH [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 이해, OSD 튜닝, [모니터](/studynote/02_operating_system/04_synchronization/229_monitor/) 정족수 관리)이 높아, 전문 교육 없이 도입하면 전통 어플라이언스보다 운영 비용이 더 높아진다.

- **📢 섹션 요약 비유**: [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) 전문성 없는 도입은 수동 변속 차를 운전할 줄 모르고 구입한 것이다. 가격이 저렴해도 운전하지 못하면 오히려 더 큰 비용이 발생한다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| **비용 절감** | 상용 어플라이언스 대비 60~75% 절감 |
| **유연한 확장** | 노드 추가로 페타바이트 선형 확장 |
| <strong>표준 <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong> | S3, CSI로 [클라우드 네이티브](/studynote/04_software_engineering/11_testing_validation/923_cloud_native_architecture/) 통합 |

SDS는 [Hyperconverged Infrastructure](/studynote/13_cloud_architecture/01_virtualization/026_hci/) ([HCI](/studynote/01_computer_architecture/15_advanced_topics/630_hci/), [하이퍼컨버지드 인프라](/studynote/01_computer_architecture/15_advanced_topics/630_hci/))로 발전하여 컴퓨팅·스토리지·네트워킹을 단일 소프트웨어 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/)으로 통합(예: Nutanix, VMware vSAN)하고 있다. [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 스토리지(Longhorn, Rook-Ceph)는 K8s 네이티브 SDS의 표준으로 자리잡았다.

- **📢 섹션 요약 비유**: SDS의 진화([HCI](/studynote/01_computer_architecture/15_advanced_topics/630_hci/))는 가전제품의 스마트홈 통합이다. TV, 냉장고, 에어컨(컴퓨팅, 스토리지, 네트워크)이 각각 따로 있던 것을 하나의 앱(소프트웨어 [스택](/studynote/08_algorithm_stats/04_datastructure/057_stack/))으로 통합 관리한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/631_sddc/">SDDC</a></strong> | SDS는 SDDC의 스토리지 레이어 |
| **Ceph** | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) 사실상 표준 |
| <strong>K8s <a href="/studynote/12_it_management/02_itsm_itil/068_csi/">CSI</a></strong> | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 환경 [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) 연동 표준 |
| <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/630_hci/">HCI</a></strong> | 컴퓨팅+스토리지+네트워크 통합 [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) |
| <strong>S3 <a href="/studynote/02_operating_system/01_overview_architecture/014_api_posix/">API</a></strong> | [SDS](/studynote/01_computer_architecture/15_advanced_topics/632_sds/) [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) 표준 인터페이스 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 SAN/NAS — 전용 어플라이언스, 벤더 종속]
    |
    v
[SDS (Ceph/GlusterFS) — 상용 HW + 소프트웨어 분리]
    |
    v
[K8s CSI 통합 — 컨테이너 네이티브 동적 프로비저닝]
    |
    v
[HCI (Nutanix/vSAN) — 컴퓨팅+스토리지+네트워크 통합]
    |
    v
[AI 기반 스토리지 자동화 — 데이터 티어링, 이상 탐지]
```

### 👶 어린이를 위한 3줄 비유 설명

1. SDS는 LEGO 스토리지예요! 어떤 브랜드의 블록(하드웨어)이든 모아서 원하는 크기의 창고(스토리지)를 만들 수 있어요.
2. 예전에는 특정 회사(EMC, NetApp)의 비싼 전용 창고를 사야 했지만, 이제는 일반 부품으로 더 크고 저렴하게 만들 수 있어요.
3. 요즘은 이 창고를 클라우드 앱이 필요할 때마다 자동으로 만들고 삭제하는 기능도 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 24 / 371

<- **이전**: [24. SDN (Software Defined Networking) — 소프트웨어 정의 네트워킹](/studynote/13_cloud_architecture/01_virtualization/024_sdn_software_defined_networking/)
**다음**: [26. HCI (Hyperconverged Infrastructure) — 하이퍼컨버지드 인프라](/studynote/13_cloud_architecture/01_virtualization/026_hci/) ->

---
