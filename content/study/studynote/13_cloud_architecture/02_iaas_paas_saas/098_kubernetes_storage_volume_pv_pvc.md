+++
weight = 98
title = "98. K8s 스토리지 관리 - 볼륨, PV, PVC (영구 스토리지)"
date = "2026-04-10"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 쿠버네티스의 스토리지는 [[085_pod_kubernetes_container_unit|파드]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])의 휘발성 생명주기와 영구적인 [[001_dikw_pyramid|데이터]]를 분리하는 [[015_virtualization|가상화]] 아키텍처다.
> 2. **가치**: 인프라 관리자는 [[153_pv_planned_value|PV]] (Persistent [[001_bigdata_3v_5v|Volume]])를 통해 스토리지를 공급하고, 개발자는 [[269_pvc_vs_svc_virtual_circuits|PVC]] (Persistent [[001_bigdata_3v_5v|Volume]] Claim)로 스토리지를 요청하여 인프라 [[528_provisioning|프로비저닝]]과 애플리케이션 개발을 완벽히 분리한다.
> 3. **판단 포인트**: [[001_dikw_pyramid|데이터]]의 [[196_durability_permanent_storage|영속성]](Persistence)과 [[528_provisioning|프로비저닝]] 자동화(동적 할당) 여부에 따라 emptyDir, 정적 [[153_pv_planned_value|PV]], 동적 [[528_provisioning|프로비저닝]]을 선택해야 한다.

---

## Ⅰ. 개요 및 필요성

[[561_container_based_deployment|컨테이너]] 환경에서 [[085_pod_kubernetes_container_unit|파드]]([[198_pod_kubernetes_minimum_deployment_unit|Pod]])는 기본적으로 상태가 없는([[239_stateless_redis|Stateless]]) 임시 작업자다. [[085_pod_kubernetes_container_unit|파드]]가 종료되거나 재생성되면 내부에 저장된 [[001_dikw_pyramid|데이터]]는 모두 소멸된다. 이를 해결하기 위해 쿠버네티스는 볼륨([[001_bigdata_3v_5v|Volume]])을 [[085_pod_kubernetes_container_unit|파드]]에 [[516_mount_mechanism|마운트]]([[516_mount_mechanism|Mount]])하여 [[001_dikw_pyramid|데이터]]를 외부에 저장하는 방식을 도입했다. 

하지만 기본 볼륨인 emptyDir나 hostPath는 [[085_pod_kubernetes_container_unit|파드]]의 생명주기나 특정 노드(Node)에 종속된다는 치명적인 한계가 있다. 애플리케이션이 요구하는 영구적인 [[001_dikw_pyramid|데이터]] 저장([[501_database|Database]] 등)을 위해서는 [[085_pod_kubernetes_container_unit|파드]]나 노드가 사라져도 [[001_dikw_pyramid|데이터]]가 보존되는 영구 스토리지([[059_persistent_storage_data_log_control_file|Persistent Storage]])가 필수적이다. 이를 위해 PV와 PVC라는 [[198_abstraction_control_data_process|추상화]] 계층이 등장했다.

- **📢 섹션 요약 비유**: [[085_pod_kubernetes_container_unit|파드]]는 언제든 체크아웃하면 냉장고가 비워지는 모텔 방과 같다. 영원히 보존해야 하는 김치([[001_dikw_pyramid|데이터]])를 보관하려면 모텔 밖의 공용 냉동고(영구 스토리지)가 필요하다.

---

## Ⅱ. 아키텍처 및 핵심 원리

쿠버네티스의 영구 스토리지 시스템은 공급([[153_pv_planned_value|PV]]), 수요([[269_pvc_vs_svc_virtual_circuits|PVC]]), 매핑(Binding)의 3단계로 동작한다.

1. **[[153_pv_planned_value|PV]] (Persistent [[001_bigdata_3v_5v|Volume]])**: 클러스터 관리자가 [[528_provisioning|프로비저닝]]한 물리/논리적 스토리지 리소스다. [[085_pod_kubernetes_container_unit|파드]]와 독립적인 생명주기를 가진다.
2. **[[269_pvc_vs_svc_virtual_circuits|PVC]] (Persistent [[001_bigdata_3v_5v|Volume]] Claim)**: 개발자가 [[085_pod_kubernetes_container_unit|파드]]에 필요한 용량과 접근 모드(Access Mode)를 명시하여 스토리지 리소스를 요청하는 명세서다.
3. **바인딩 (Binding)**: K8s 컨트롤러가 PVC의 요구 조건(용량, 모드 등)을 만족하는 PV를 찾아 1:1로 연결한다.

```text
┌─────────────────────────────────────────────────────────────┐
│          PV와 PVC의 바인딩 및 파드 마운트 아키텍처        │
├─────────────────────────────────────────────────────────────┤
│  [ Infra Admin ]                  [ Developer ]             │
│   물리 스토리지 ──▶ 생성 ──▶ PV ◀── 바인딩 ──▶ PVC        │
│   (NFS, EBS 등)     (공급)                 (수요)       │
│                                                 │           │
│                                                 ▼           │
│                                           Pod (마운트)      │
└─────────────────────────────────────────────────────────────┘
```

이 구조는 개발자가 AWS EBS나 NFS의 복잡한 연결 방식을 몰라도, K8s 표준 인터페이스인 PVC만으로 스토리지 자원을 할당받을 수 있게 하는 핵심 메커니즘이다.

- **📢 섹션 요약 비유**: PV는 구청에서 미리 만들어둔 상가 건물(공급)이고, PVC는 세입자가 제출한 10평짜리 점포 임대 신청서(수요)다. 구청장(K8s)이 조건에 맞는 건물을 찾아 열쇠를 넘겨준다(바인딩).

---

## Ⅲ. 비교 및 연결

스토리지 할당 방식은 관리자의 개입 여부에 따라 정적(Static) [[528_provisioning|프로비저닝]]과 동적(Dynamic) [[528_provisioning|프로비저닝]]으로 나뉜다.

| 비교 항목 | 정적 [[528_provisioning|프로비저닝]] (Static [[528_provisioning|Provisioning]]) | 동적 [[528_provisioning|프로비저닝]] (Dynamic [[528_provisioning|Provisioning]]) |
| :--- | :--- | :--- |
| **핵심 원리** | 관리자가 사전에 여러 PV를 수동으로 [[087_process_state_transition|생성]] | [[269_pvc_vs_svc_virtual_circuits|PVC]] 요청 시 StorageClass를 통해 자동 [[087_process_state_transition|생성]] |
| **장점** | 스토리지 자원의 엄격한 통제 및 제한 가능 | 인프라 관리자의 개입 제로, 유연한 확장 |
| **단점** | [[269_pvc_vs_svc_virtual_circuits|PVC]] 요구량과 [[153_pv_planned_value|PV]] 크기가 불일치하면 자원 낭비 발생 | 클라우드 제공자(AWS 등) [[014_api_posix|API]] 연동 필수 |
| **사용 객체** | [[153_pv_planned_value|PV]], [[269_pvc_vs_svc_virtual_circuits|PVC]] | StorageClass, [[269_pvc_vs_svc_virtual_circuits|PVC]] |

과거에는 관리자가 10GB, 50GB 등 다양한 크기의 PV를 미리 만들어 두어야(Static) 했으나, 현재는 StorageClass 자판기를 통해 개발자가 PVC를 날리는 즉시 클라우드 스토리지가 [[087_process_state_transition|생성]](Dynamic)되는 방식이 주류를 이룬다.

- **📢 섹션 요약 비유**: 정적 할당은 미리 만들어둔 기성품 옷([[153_pv_planned_value|PV]]) 중에서 맞는 사이즈를 찾는 것이고, 동적 할당은 주문서([[269_pvc_vs_svc_virtual_circuits|PVC]])를 넣는 즉시 3D 프린터(StorageClass)가 맞춤형 옷을 뽑아내는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 스토리지를 설계할 때는 **접근 모드(Access Mode)**와 **반환 [[164_policy|정책]](Reclaim [[164_policy|Policy]])**을 시스템 요구사항에 맞게 판단해야 한다.

### [[435_checklist_based_testing|체크리스트]] 및 의사결정
1. **Access Mode 선택**:
   - `ReadWriteOnce (RWO)`: 단일 노드에서만 읽기/[[289_cqrs_db|쓰기]] 가능. 일반적인 RDBMS [[085_pod_kubernetes_container_unit|파드]]에 적합.
   - `ReadWriteMany (RWX)`: 여러 노드에서 동시 읽기/[[289_cqrs_db|쓰기]] 가능. 웹 서버의 공유 정적 리소스([[543_nfs_network_file_system|NFS]] 등)에 필수.
2. **Reclaim [[164_policy|Policy]] [[009_config|설정]]**:
   - `Retain`: PVC가 삭제되어도 PV와 [[001_dikw_pyramid|데이터]]는 보존됨. 중요한 운영 DB [[001_dikw_pyramid|데이터]]는 반드시 Retain으로 [[009_config|설정]]해야 함.
   - `Delete`: [[269_pvc_vs_svc_virtual_circuits|PVC]] 삭제 시 PV와 실제 스토리지(EBS 등)도 함께 삭제됨. 임시 [[001_dikw_pyramid|데이터]]나 동적 [[528_provisioning|프로비저닝]]의 기본값.

### [[128_water_scrum_fall_anti_pattern|안티패턴]]
- 스테이트풀(Stateful) 애플리케이션을 배포하면서 일반 Deployment와 emptyDir를 결합하는 설계. (반드시 StatefulSet과 [[269_pvc_vs_svc_virtual_circuits|PVC]] 템플릿을 사용해야 함)

- **📢 섹션 요약 비유**: 방을 뺄 때([[269_pvc_vs_svc_virtual_circuits|PVC]] 삭제), 주인이 방 안의 물건을 그대로 둘지(Retain) 아니면 쓰레기차를 불러 싹 치워버릴지(Delete) 미리 계약서에 명시하는 것과 같다.

---

## Ⅴ. 기대효과 및 결론

PV와 [[269_pvc_vs_svc_virtual_circuits|PVC]] [[198_abstraction_control_data_process|추상화]]를 통해 쿠버네티스는 애플리케이션([[198_pod_kubernetes_minimum_deployment_unit|Pod]])과 인프라(Storage)의 라이프사이클을 완벽하게 분리했다. 이는 [[213_msa_microservices_architecture|마이크로서비스 아키텍처]]([[619_msa_traffic_hardware|MSA]])에서 [[561_container_based_deployment|컨테이너]]의 이동성과 [[001_dikw_pyramid|데이터]]의 안정성을 동시에 보장하는 기반이 된다.

미래의 K8s 스토리지는 [[068_csi|CSI]] ([[099_csi_container_storage_interface_kubernetes_plugin|Container Storage Interface]]) 표준을 통해 더욱 다양한 써드파티 스토리지와 투명하게 연동되며, 동적 [[528_provisioning|프로비저닝]]을 넘어 볼륨 [[022_snapshot_backup_architecture|스냅샷]], [[149_clone_system_call|클론]]([[149_clone_system_call|Clone]]) 등 엔터프라이즈 스토리지 기능을 기본 지원하는 방향으로 진화하고 있다. 스토리지 [[015_virtualization|가상화]]는 더 이상 물리 디스크의 [[516_mount_mechanism|마운트]]가 아니라, [[001_dikw_pyramid|데이터]]의 라이프사이클 자동화다.

- **📢 섹션 요약 비유**: 이젠 이사를 가도([[085_pod_kubernetes_container_unit|파드]] 재생성) 내 금고([[153_pv_planned_value|PV]])가 알아서 새집으로 배달된다. 개발자는 그저 금고 열쇠([[269_pvc_vs_svc_virtual_circuits|PVC]])만 잘 챙기면 된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **[[001_bigdata_3v_5v|Volume]] (emptyDir/hostPath)** | [[085_pod_kubernetes_container_unit|파드]]/노드와 생명주기를 같이하는 종속형 스토리지 |
| **StorageClass** | 동적 [[528_provisioning|프로비저닝]]을 위해 스토리지 유형과 [[087_process_state_transition|생성]]자를 정의하는 템플릿 |
| **[[068_csi|CSI]] ([[099_csi_container_storage_interface_kubernetes_plugin|Container Storage Interface]])** | K8s와 외부 스토리지 시스템을 연결하는 범용 플러그인 표준 |
| **[[088_statefulset_kubernetes_persistent_workload|StatefulSet]]** | [[269_pvc_vs_svc_virtual_circuits|PVC]] 템플릿을 내장하여 순차적인 스토리지 할당이 필요한 앱 컨트롤러 |

### 📈 관련 키워드 및 발전 흐름도

```text
기본 Volume (emptyDir, hostPath)
    │ 파드 생명주기 종속성 극복
    ▼
정적 PV (Persistent Volume) / PVC
    │ 인프라 관리자 사전 생성의 비효율성 극복
    ▼
StorageClass 기반 동적 프로비저닝 (Dynamic Provisioning)
    │ 클라우드 스토리지 API 연동 추상화
    ▼
CSI (Container Storage Interface)
```

이 흐름도는 단순 [[561_container_based_deployment|컨테이너]] [[516_mount_mechanism|마운트]]([[001_bigdata_3v_5v|Volume]])에서 시작하여 인프라 분리([[153_pv_planned_value|PV]]/[[269_pvc_vs_svc_virtual_circuits|PVC]])를 거쳐 완전 자동화(StorageClass) 및 플러그인 표준화([[068_csi|CSI]])로 발전하는 스토리지 관리의 진화 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[085_pod_kubernetes_container_unit|파드]]는 하루살이 요정이라 잠들면 주머니(기본 볼륨)에 있던 장난감이 다 사라져요.
2. 그래서 요정 마을 이장님이 절대 부서지지 않는 마법 창고([[153_pv_planned_value|PV]])를 튼튼하게 지어두셨어요.
3. 요정들이 "창고 1칸 쓸래요!" 하고 신청서([[269_pvc_vs_svc_virtual_circuits|PVC]])를 내면, 창고 열쇠를 받아서 장난감을 영원히 안전하게 보관할 수 있답니다.
