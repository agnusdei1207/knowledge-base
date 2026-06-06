---
title: "Block / File / Object Storage"
date: "2026-03-03"
tags:
  - "studynote-cloud"
---

> **핵심 인사이트 3줄**
> 1. 블록·[파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)·[오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 저장 단위·접근 방식·확장 방식이 근본적으로 다르며, 워크로드 특성에 맞는 선택이 성능과 비용을 결정한다.
> 2. 블록은 고성능 DB/[VM](/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)(낮은 레이턴시), [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 공유 [NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/)/CIFS(협업), 오브젝트는 무한 확장 [비정형 데이터](/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)(S3)에 최적화되어 있다.
> 3. 클라우드에서는 EBS(블록)·EFS([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))·S3(오브젝트)를 혼합해 다계층 스토리지 아키텍처를 구성하는 것이 표준 패턴이다.

---

## Ⅰ. 세 가지 스토리지 유형 비교

| 특성          | 블록 스토리지      | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지    | [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)  |
|-------------|-----------------|---------------|-----------------|
| 저장 단위     | 고정 크기 블록   | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)/디렉토리   | 오브젝트([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)+메타)|
| 접근 방식     | [블록 장치](/studynote/02_operating_system/08_storage_and_io_systems/442_block_device/) ([SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/))  | [NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/)/CIFS/SMB  | [HTTP](/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/)    |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수정   | 블록 단위 수정   | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수정 가능  | 덮어쓰기만 가능   |
| 확장성        | 제한적           | 중간           | 무한(페타바이트+) |
| 레이턴시      | 매우 낮음 (μs)  | 낮음 (ms)      | 높음 (ms~s)      |
| 비용          | 높음             | 중간           | 낮음             |
| AWS [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)   | EBS              | EFS / FSx     | S3               |

📢 **섹션 요약 비유**: 블록은 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 드라이브, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 공유 폴더 네트워크, 오브젝트는 구글 드라이브와 같다 — 각각 속도, 공유, 무한 확장을 위해 만들어졌다.

---

## Ⅱ. 블록 스토리지 — EBS, [SAN](/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/)

### 블록 스토리지 동작 원리

```
EC2 인스턴스
   | iSCSI / FC / NVMe-oF
   v
블록 스토리지 (EBS)
   [블록 0][블록 1][블록 2]...[블록 N]
          파일시스템(ext4/NTFS)은 OS가 관리
```

### 블록 스토리지 유형 (AWS EBS)

| 유형          | 특성                      | 사용 사례           |
|-------------|--------------------------|-------------------|
| gp3 ([SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))   | 범용, 16,000 IOPS        | 대부분 워크로드     |
| io2 Block Express | 고성능, 256K IOPS  | [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) DB, SAP    |
| st1 ([HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/))   | [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 최적화, 저렴        | 빅데이터, [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)      |
| sc1 ([HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/))   | 최저 비용                 | 아카이브 [콜드 데이터](/studynote/01_computer_architecture/15_advanced_topics/676_cold_data_archiving/) |

📢 **섹션 요약 비유**: 블록 스토리지는 컴퓨터에 직접 꽂는 SSD다 — 빠르고 신뢰할 수 있지만, 다른 컴퓨터와 동시에 쓰기가 어렵다.

---

## Ⅲ. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지 — [NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/), EFS

### [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)

```
클라이언트 A -----+
                  | NFS v4.1 / SMB 3.0
클라이언트 B -----+
                  v
         파일 스토리지 서버 (EFS / NetApp)
               /shared/
               +-- project/
               |   +-- data.csv
               |   +-- config.yaml
               +-- logs/
```

### AWS EFS vs FSx 비교

| [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)      | 특성                    | 사용 사례          |
|-----------|------------------------|------------------|
| EFS       | 완전 관리형 [NFS](/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/), 자동 확장 | [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 공유 볼륨 |
| FSx Lustre | 고성능, ML 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)   | [HPC](/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/), SageMaker    |
| FSx Windows | SMB, AD 통합          | Windows [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버  |
| FSx NetApp | ONTAP, 멀티프로토콜     | 엔터프라이즈 [NAS](/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/)   |

📢 **섹션 요약 비유**: [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지는 학교 서버의 공유 폴더다 — 여러 학생이 같은 폴더에 접속해 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 열고 수정하고 저장할 수 있다.

---

## Ⅳ. [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) — S3 원리

### 오브젝트 구조

```
버킷 (Bucket): my-data-bucket
   +-- 오브젝트 (Object)
          +-- Key: "2024/01/15/logs/app.log"
          +-- Value: 실제 데이터 (바이너리)
          +-- 메타데이터: Content-Type, ETag, 커스텀 태그
          +-- 버전 ID: v1, v2, v3...
```

### S3 스토리지 클래스 (비용 최적화)

| 클래스              | 접근 빈도   | 비용      | [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 |
|------------------|-----------|---------|---------|
| S3 Standard      | 자주       | 높음     | 즉시      |
| S3 IA            | 가끔       | 중간     | 즉시      |
| S3 Glacier Instant | 드물게   | 낮음     | 즉시      |
| S3 Glacier Deep  | 거의 없음  | 매우 낮음 | 12시간   |

📢 **섹션 요약 비유**: [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 거대한 창고 선반이다 — 번호표([Key](/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))를 알면 어떤 박스(Object)든 꺼낼 수 있고, 선반은 무한히 늘어난다.

---

## Ⅴ. 다계층 스토리지 아키텍처

```
클라우드 스토리지 아키텍처:

Web App ---> EFS (공유 정적 파일)
             v
  DB -------> EBS io2 (고성능 블록)
             v
  로그 ------> S3 Standard (원본)
                   v 30일 후
             S3 IA (비용 절감)
                   v 90일 후
             Glacier (장기 보관)
```

### 선택 가이드

| 워크로드            | 권장 스토리지        |
|------------------|-------------------|
| RDBMS (RDS)      | EBS gp3/io2        |
| [컨테이너](/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 공유 볼륨 | EFS                |
| 대용량 미디어      | S3 + CloudFront   |
| ML 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋   | FSx Lustre + S3   |
| [백업](/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·아카이브      | S3 Glacier         |

📢 **섹션 요약 비유**: 다계층 스토리지는 집의 수납 공간이다 — 자주 쓰는 물건은 서랍(EBS), 가족이 함께 쓰는 것은 공용 선반(EFS), 거의 안 쓰는 것은 창고(S3 Glacier).

---

## 📌 관련 개념 맵

```
클라우드 스토리지 유형
+-- 블록 스토리지
|   +-- EBS (AWS), Persistent Disk (GCP)
|   +-- SAN (Storage Area Network)
|   +-- iSCSI / NVMe-oF
+-- 파일 스토리지
|   +-- EFS / FSx (AWS), Filestore (GCP)
|   +-- NFS (Network File System)
|   +-- SMB / CIFS
+-- 오브젝트 스토리지
    +-- S3 (AWS), GCS (GCP), Azure Blob
    +-- S3 API 표준 (호환 생태계)
    +-- S3 스토리지 클래스 계층
```

---

## 📈 관련 키워드 및 발전 흐름도

```
+-----------------------------------------------------------------+
|             클라우드 스토리지 발전 흐름                          |
+--------------+--------------------+-----------------------------+
| 1990년대     | SAN / NAS 등장     | 블록·파일 스토리지 기업화    |
| 2006년       | AWS S3 출시        | 오브젝트 스토리지 클라우드화 |
| 2008년       | AWS EBS 출시       | 클라우드 블록 스토리지 표준  |
| 2015년       | AWS EFS GA         | 관리형 NFS 서비스            |
| 2018년       | S3 Intelligent Tier| AI 기반 자동 계층 이동       |
| 2020년대     | NVMe-oF·CSI       | 컨테이너 스토리지 표준화     |
+--------------+--------------------+-----------------------------+

핵심 키워드 연결:
블록(EBS) -> DB/VM 고성능 워크로드
파일(EFS) -> 컨테이너·공유 파일시스템
오브젝트(S3) -> 비정형 데이터·무한 확장
     v
다계층 스토리지 정책 -> 비용 최적화 (FinOps)
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 블록 스토리지는 개인 SSD다 — 혼자 빠르게 쓰는 데는 최고지만 친구와 나누기 어렵다.
2. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지는 학교 공용 사물함이다 — 여러 명이 같은 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 꺼내 볼 수 있다.
3. [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 구글 드라이브다 — 인터넷만 있으면 어디서든 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 올리고 내려받고, 용량은 거의 무한하다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 31 / 371

<- **이전**: [31. 로드 밸런서 — 트래픽 분산의 핵심 기술](/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/)
**다음**: [CDN (Content Delivery Network, 콘텐츠 전달 네트워크)](/studynote/13_cloud_architecture/01_virtualization/033_cdn/) ->

---
