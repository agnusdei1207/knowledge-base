+++
title = "678. Ceph 스토리지 아키텍처"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Ceph는 범용 서버와 디스크를 묶어, 중앙 컨트롤러 없이도 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 배치·[복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)·[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하도록 설계한 [SDS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/632_sds/) (Software-Defined Storage) 아키텍처다.
> 2. **가치**: RADOS (Reliable Autonomic Distributed Object Store)와 CRUSH (Controlled [Replication](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) Under Scalable Hashing)를 기반으로 객체·블록·[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 하나의 저장 풀에서 통합 제공할 수 있다.
> 3. **판단 포인트**: Ceph는 확장성과 자율 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 매우 강력하지만, 네트워크·장애 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)·운영 자동화를 함께 설계해야 진가가 나오므로 “쉬운 [NAS](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/) ([Network Attached Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/))”로 접근하면 실패하기 쉽다.

---

## Ⅰ. 개요 및 필요성

Ceph는 대규모 저장 시스템에서 전통적인 스토리지 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)이 갖는 한계를 풀기 위해 등장했다. 고가의 [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) ([Storage Area Network](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/)) 장비나 [NAS](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/) ([Network Attached Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/)) 어플라이언스는 안정적이지만, 전용 컨트롤러와 [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/) 구조 때문에 규모가 커질수록 비용과 확장 한계가 뚜렷해진다. 특히 수백 대 이상 서버가 같은 저장 계층을 공유하면, 특정 컨트롤러나 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 경로가 병목이 되기 쉽다.

Ceph는 이 문제를 “더 큰 중앙 장비”로 해결하지 않고, “중앙 장비를 입출력 경로에서 최대한 제거하는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 설계”로 접근했다. 값싼 서버와 디스크를 계속 추가하면서도, 시스템이 스스로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 재배치하고 장애를 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)하게 만들자는 발상이다. 그래서 Ceph는 단순한 저장 제품이 아니라, 대규모 [프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/)와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터의 기본 저장 토대가 되었다.

- **📢 섹션 요약 비유**: Ceph는 거대한 창고 하나를 더 비싸게 짓는 대신, 여러 창고에 물건을 나눠 두고 주소 계산 규칙을 모두에게 알려 병목을 없앤 도시형 물류 시스템과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Ceph의 핵심은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 실제로 저장하는 계층과, 저장 위치를 계산하는 규칙을 분리한 데 있다. 클라이언트는 MON ([Monitor](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)) 노드로부터 클러스터 맵을 받고, CRUSH 규칙으로 객체가 어느 PG (Placement Group)를 거쳐 어떤 OSD ([Object Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) Daemon) 집합에 저장될지를 직접 계산한다. 즉, 중앙 서버가 매번 “이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 여기 있다”를 알려주는 방식이 아니라, 클라이언트와 노드가 같은 규칙으로 같은 답을 계산하는 방식이다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| MON ([Monitor](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)) | 클러스터 멤버십과 맵 상태 유지 | 홀수 개 구성과 쿼럼 유지가 중요 |
| MGR (Manager) | 운영 통계, 대시보드, 자동화 보조 | 운영 가시성과 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 확장 담당 |
| OSD ([Object Storage](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) Daemon) | 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 수행 | 디스크 성능과 네트워크 품질이 핵심 |
| PG (Placement Group) | 객체를 배치하기 위한 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 묶음 | 너무 많거나 적으면 운영 효율 저하 |
| CRUSH | 장애 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 고려한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치 계산 | 랙·호스트·실 단위 규칙 설계 필요 |
| RADOS | Ceph의 기본 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 객체 저장 계층 | 상위 인터페이스의 공통 토대 |

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ Client                                                                  │
│   │ get cluster map                                                      │
│   ▼                                                                      │
│ MON quorum --------------------> CRUSH placement                         │
│                                      │                                   │
│                                      ▼                                   │
│                               PG selection                               │
│                                      │                                   │
│                     ┌────────────────┼────────────────┐                  │
│                     ▼                ▼                ▼                  │
│                  OSD set A        OSD set B        OSD set C             │
│               replica / shard  replica / shard  replica / shard          │
└──────────────────────────────────────────────────────────────────────────┘
```

이 기반 위에서 Ceph는 세 가지 대표 인터페이스를 제공한다. 객체 저장은 RADOS Gateway (RGW), 블록 저장은 RADOS [Block Device](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/442_block_device/) ([RBD](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/754_rbd/)), [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유는 Ceph [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) System (CephFS)이 담당한다. 즉, 저장 본체는 하나인데 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 얼굴만 다르게 씌우는 구조라서, [프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/)에서 스토리지 종류를 통합하는 데 큰 장점이 있다.

- **📢 섹션 요약 비유**: Ceph는 매번 안내 데스크에 물어보지 않아도, 모두가 같은 지도를 들고 물건 위치를 스스로 계산해 찾아가는 창고 시스템과 같다.

---

## Ⅲ. 비교 및 연결

Ceph의 강점은 “[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 객체 저장”에만 머무르지 않고, 블록과 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 인터페이스까지 통합한다는 데 있다. 이 점에서 Ceph는 전통적 저장 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)과도 다르고, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 중심 스케일아웃 솔루션인 GlusterFS와도 다르며, 분석용 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템인 [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) ([Hadoop](/knowledge-base/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) [Distributed File System](/knowledge-base/studynote/02_operating_system/09_file_system/553_distributed_file_system/))와도 다르다.

| 비교 대상 | 핵심 구조 | 잘 맞는 영역 | 한계 |
| :--- | :--- | :--- | :--- |
| 전통 [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/) / [NAS](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/) [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) | 중앙 컨트롤러 중심 | 낮은 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 검증된 엔터프라이즈 운영 | 비용과 수평 확장 한계 |
| **Ceph** | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 객체 기반 + 통합 인터페이스 | [프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/), 범용 저장 통합 | 설계와 운영 난이도 높음 |
| [GlusterFS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/679_glusterfs/) | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유 중심 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 볼륨 | 단순한 공유 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 저장 | 블록·객체 통합은 약함 |
| [HDFS](/knowledge-base/studynote/14_data_engineering/01_infrastructure/013_hdfs/) | 대용량 분석 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 중심 | 배치 분석, [데이터 지역성](/knowledge-base/studynote/14_data_engineering/01_infrastructure/019_data_locality/) | 범용 공유 저장으로는 부적합 |

또한 Ceph는 OpenStack의 가상머신 이미지 저장, Kubernetes의 영속 볼륨, Amazon S3 (Simple Storage [Service](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)) 호환 오브젝트 저장소 구축과 자연스럽게 연결된다. 이 말은 Ceph가 단순히 “디스크를 많이 묶는 기술”이 아니라, 컴퓨트 가상화와 클라우드 오케스트레이션을 떠받치는 공통 저장 플랫폼이라는 뜻이다. 반대로 특정 업무가 단순 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버 하나만 원한다면 Ceph의 범용성이 오히려 과할 수 있다.

- **📢 섹션 요약 비유**: Ceph가 다목적 물류 허브라면, GlusterFS는 대형 공유 창고이고, HDFS는 대규모 원자재 보관 창고다. 비슷해 보여도 목적이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **[프라이빗 클라우드](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/008_private_cloud/)의 통합 저장소**
   - 가상머신 디스크는 [RBD](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/754_rbd/), 이미지 저장은 RGW, 공유 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 CephFS로 나눠 제공할 수 있다.
   - 물리 저장 풀을 통합하므로 장비 종류를 줄이고 운영 표준화를 만들기 쉽다.

2. **대규모 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 및 아카이브 저장**
   - 일반 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 대신 삭제 코딩을 적용하면 저장 효율을 크게 높일 수 있다.
   - 다만 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시 계산 비용과 네트워크 비용이 늘어나는 점을 함께 고려해야 한다.

3. **[컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 플랫폼 영속 볼륨**
   - 애플리케이션별로 독립된 볼륨을 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)·회수하기 좋다.
   - 다중 테넌트 환경에서 격리와 확장이 동시에 필요할 때 강점을 보인다.

### 채택/회피 판단 체크포인트

- **채택이 유리한 경우**
  - 블록·[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)·객체 저장을 하나의 플랫폼으로 통합하고 싶을 때
  - 노드 추가로 선형에 가까운 확장을 기대할 때
  - 하드웨어 단일 장애보다 클러스터 자율 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를 우선할 때

- **회피가 유리한 경우**
  - 운영 인력이 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템과 장애 분석에 익숙하지 않을 때
  - 매우 작은 규모에서 단순 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유만 필요할 때
  - 네트워크 품질과 장애 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 설계를 충분히 확보할 수 없을 때

실무에서는 Ceph를 설치하는 것보다 설계하는 일이 더 중요하다. MON 쿼럼 수, 랙 단위 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 규칙, [Solid State Drive](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) ([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))와 Hard Disk Drive ([HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/)) 계층 분리, 재균형 시 허용 가능한 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 트래픽, 장애 시 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 목표를 모두 먼저 정해야 한다. 기술사 관점에서는 “Ceph가 된다”보다 “이 워크로드에 Ceph의 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 운영비를 지불할 가치가 있는가”를 판단하는 능력이 핵심이다.

- **📢 섹션 요약 비유**: Ceph 도입은 창고를 하나 더 사는 일이 아니라, 도시 전체 물류 규칙을 새로 설계하는 일과 같다. 규칙을 잘 짜면 매우 강하지만, 준비 없이 시작하면 혼란도 커진다.

---

## Ⅴ. 기대효과 및 결론

Ceph가 주는 가장 큰 효과는 저장장치를 전용 장비 중심에서 소프트웨어 중심으로 바꿔 놓는 데 있다. 범용 서버를 계속 추가하면서 확장하고, 장애가 나도 시스템이 스스로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다시 맞추며, 하나의 저장 토대 위에서 여러 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)를 올릴 수 있다는 점은 대규모 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)센터에 매우 매력적이다. 특히 [벤더 종속](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/051_vendor_lock_in_cloud_computing/)을 줄이고 클라우드 운영 자동화와 결합하기 좋다.

하지만 Ceph는 “공짜로 얻는 확장성”이 아니다. 운영 복잡도, 관측 체계, 네트워크 품질, 업그레이드 절차, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 예측까지 모두 설계 자산이 되어야 한다. 그래서 Ceph는 **“값싼 디스크 묶음”이 아니라 “규칙 기반 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)”**로 기억하는 편이 맞다.

- **📢 섹션 요약 비유**: Ceph는 큰 금고 하나가 아니라, 서로 연결된 여러 금고를 스스로 관리하는 자동 보관 도시와 같다. 도시가 클수록 힘을 발하지만, 운영 규칙도 그만큼 중요해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| RADOS | Ceph의 바닥층으로, 객체 저장과 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)의 공통 기반을 제공한다. |
| CRUSH | 중앙 조회 없이도 장애 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)을 고려한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 배치를 계산하게 한다. |
| OSD | 실제 디스크를 관리하며 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/), [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 재균형을 수행하는 실행 단위다. |
| [RBD](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/754_rbd/) | 가상머신과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스용 블록 볼륨 제공에 쓰인다. |
| CephFS | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 공유가 필요한 워크로드를 Ceph 위에서 수용한다. |
| RGW | S3 호환 오브젝트 인터페이스를 제공해 애플리케이션과 연결한다. |

### 📈 관련 키워드 및 발전 흐름도

```text
전용 스토리지 배열 중심 구조
        │
        ▼
범용 서버 기반 분산 저장 요구
        │
        ▼
RADOS + CRUSH 기반 Ceph 아키텍처
        │
        ▼
RBD / CephFS / RGW 통합 저장 플랫폼
        │
        ▼
프라이빗 클라우드와 클라우드 네이티브 저장 토대
```

이 흐름은 저장 시스템이 전용 하드웨어 상자에서 벗어나, 규칙과 소프트웨어가 중심이 되는 플랫폼으로 진화했음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Ceph는 장난감을 한 상자에 몰아넣는 대신, 여러 상자에 나눠 넣고 어디에 넣을지 계산 규칙을 모두가 알고 있는 방식이에요.
2. 그래서 상자 하나가 망가져도 다른 상자들로 다시 맞춰 만들 수 있어요.
3. 게다가 같은 장난감 창고로 상자 놀이, 책 놀이, 공 놀이를 모두 할 수 있어서 아주 큰 창고처럼 쓸 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 679 / 803

← **이전**: [677. 오브젝트 스토리지 (Object Storage)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/677_object_storage/)
**다음**: [679. GlusterFS 분산 스토리지](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/679_glusterfs/) →

---
