---
title: "PV PVC PersistentVolume"
date: "2026-05-09"
tags:
  - "studynote-devops-sre"
weight: 314
---
> **핵심 인사이트**
> - [PV](/studynote/12_it_management/04_sdlc_testing/153_pv_planned_value/) (PersistentVolume)는 클러스터 관리자가 준비한 스토리지 자원이고, [PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) (PersistentVolumeClaim)는 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 요청하는 스토리지 주문서다.
> - StorageClass (스토리지클래스)를 이용한 동적 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/)으로 [PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 자동으로 PV가 만들어진다.
> - 접근 모드(ReadWriteOnce / ReadOnlyMany / ReadWriteMany)가 스토리지 공유 범위를 결정한다.

---

## Ⅰ. PV와 [PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) 개념

[PV](/studynote/12_it_management/04_sdlc_testing/153_pv_planned_value/) (PersistentVolume)는 클러스터 수준의 스토리지 오브젝트로 관리자가 직접 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하거나 동적으로 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/)된다.

[PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) (PersistentVolumeClaim)는 사용자가 필요한 용량·접근 모드를 선언하는 요청 오브젝트다.

```
+------------------------------------------------------+
|                  스토리지 바인딩 흐름                |
|                                                      |
|  개발자                관리자                        |
|  PVC 생성  --Binding--->  PV 매칭                    |
|  (10Gi 요청)             (10Gi NFS)                  |
|      |                                              |
|      v                                              |
|   파드에서 volumeMounts로 사용                       |
+------------------------------------------------------+
```

접근 모드:

| 모드              | 설명                          |
|-------------------|-------------------------------|
| ReadWriteOnce     | 단일 노드 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)            |
| ReadOnlyMany      | 다중 노드 읽기 전용            |
| ReadWriteMany     | 다중 노드 읽기/[쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)            |

> 📢 **Ⅰ 섹션 요약 비유**
> PV는 창고이고, PVC는 "10평짜리 창고 주세요"라는 신청서다.

---

## Ⅱ. StorageClass와 동적 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/)

StorageClass (스토리지클래스)는 프로비저너(Provisioner), 파라미터, Reclaim Policy를 정의한다.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
reclaimPolicy: Delete
```

PVC에 `storageClassName: fast-ssd` 를 명시하면 [PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 시 자동으로 EBS 볼륨이 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·바인딩된다.

Reclaim [Policy](/studynote/10_ai/02_dl_architecture_new/164_policy/):
- Delete: [PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) 삭제 시 PV도 삭제
- Retain: [PV](/studynote/12_it_management/04_sdlc_testing/153_pv_planned_value/) 보존(수동 정리)
- Recycle: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화 후 재사용(deprecated)

> 📢 **Ⅱ 섹션 요약 비유**
> StorageClass는 창고 유형 [카탈로그](/studynote/05_database/07_exam_summary/394_catalog_metadata/) — 냉동창고·일반창고 중 선택하면 자동으로 계약이 체결된다.

---

## Ⅲ. StatefulSet과 volumeClaimTemplates

StatefulSet은 `volumeClaimTemplates`를 통해 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)별 고유 PVC를 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)한다.

```yaml
volumeClaimTemplates:
- metadata:
    name: data
  spec:
    accessModes: ["ReadWriteOnce"]
    resources:
      requests:
        storage: 5Gi
```

[Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) `db-0` -> [PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) `data-db-0`, [Pod](/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) `db-1` -> [PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) `data-db-1` 식으로 각 [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 독립 볼륨을 가진다.

> 📢 **Ⅲ 섹션 요약 비유**
> StatefulSet은 기숙사 — 각 학생([파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/))이 자기 방([PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/))을 갖는 구조다.

---

## Ⅳ. [CSI](/studynote/12_it_management/02_itsm_itil/068_csi/) ([Container Storage Interface](/studynote/13_cloud_architecture/02_iaas_paas_saas/099_csi_container_storage_interface_kubernetes_plugin/))

[CSI](/studynote/12_it_management/02_itsm_itil/068_csi/) ([Container Storage Interface](/studynote/13_cloud_architecture/02_iaas_paas_saas/099_csi_container_storage_interface_kubernetes_plugin/))는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/)가 외부 스토리지 드라이버를 표준 인터페이스로 연결하는 플러그인 체계다.

```
파드
 |
 v
kubelet ---> CSI Driver ---> 스토리지 백엔드
             (AWS EBS, GCP PD, Ceph 등)
```

[CSI](/studynote/12_it_management/02_itsm_itil/068_csi/) 이전에는 in-tree 플러그인으로 코어 코드에 직접 통합됐으나, CSI로 분리돼 벤더가 독립적으로 드라이버를 배포할 수 있다.

> 📢 **Ⅳ 섹션 요약 비유**
> CSI는 [쿠버네티스](/studynote/06_ict_convergence/03_cloud_infrastructure/196_kubernetes_k8s_container_orchestration/) 스토리지 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)의 [USB](/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) 표준 — 어떤 드라이브든 같은 [포트](/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)에 꽂으면 동작한다.

---

## Ⅴ. 개념 맵 및 발전 흐름도

### 개념 맵

| 구성 요소            | 역할                                    |
|----------------------|-----------------------------------------|
| [PV](/studynote/12_it_management/04_sdlc_testing/153_pv_planned_value/)                   | 클러스터 스토리지 자원 오브젝트          |
| [PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/)                  | [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)가 요청하는 스토리지 주문서          |
| StorageClass         | 동적 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) 정의                |
| Provisioner          | 실제 볼륨 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 드라이버                  |
| AccessMode           | 노드 간 접근 범위 제어                   |
| [CSI](/studynote/12_it_management/02_itsm_itil/068_csi/)                  | 외부 스토리지 드라이버 표준 인터페이스   |
| [StatefulSet](/studynote/13_cloud_architecture/02_iaas_paas_saas/088_statefulset_kubernetes_persistent_workload/)          | [파드](/studynote/13_cloud_architecture/02_iaas_paas_saas/085_pod_kubernetes_container_unit/)별 고유 [PVC](/studynote/03_network/05_lan_wan_l2_devices/269_pvc_vs_svc_virtual_circuits/) 자동 [생성](/studynote/02_operating_system/02_process_thread/087_process_state_transition/)                |

### 관련 키워드 및 발전 흐름도

```
Persistent Storage
    +-- PV + PVC -> 정적 프로비저닝
    +-- StorageClass -> 동적 프로비저닝
    +-- CSI Driver -> 외부 스토리지 연동
    +-- StatefulSet volumeClaimTemplates -> 파드별 독립 볼륨
```

> 🧒 **어린이 비유**
> PV는 학교 사물함, PVC는 "사물함 하나 주세요" 신청서예요. StorageClass는 작은 사물함이냐 큰 사물함이냐를 결정하는 규칙이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 314 / 373

<- **이전**: [HPA CA Autoscaling](/studynote/15_devops_sre/05_devsecops/313_hpa_ca/)
**다음**: [Helm Package Manager](/studynote/15_devops_sre/05_devsecops/315_process/) ->

---
