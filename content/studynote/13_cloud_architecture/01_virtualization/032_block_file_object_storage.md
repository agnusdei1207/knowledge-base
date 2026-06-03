+++
title = "블록·파일·오브젝트 스토리지 (Block / File / Object Storage)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-cloud"]

[extra]
tags = ["studynote-cloud"]
+++

> **핵심 인사이트 3줄**
> 1. 블록·[파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)·[오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 저장 단위·접근 방식·확장 방식이 근본적으로 다르며, 워크로드 특성에 맞는 선택이 성능과 비용을 결정한다.
> 2. 블록은 고성능 DB/[VM](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/598_vm_migration_nic/)(낮은 레이턴시), [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 공유 [NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/)/CIFS(협업), 오브젝트는 무한 확장 [비정형 데이터](/knowledge-base/studynote/14_data_engineering/01_infrastructure/004_unstructured_data/)(S3)에 최적화되어 있다.
> 3. 클라우드에서는 EBS(블록)·EFS([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))·S3(오브젝트)를 혼합해 다계층 스토리지 아키텍처를 구성하는 것이 표준 패턴이다.

---

## Ⅰ. 세 가지 스토리지 유형 비교

| 특성          | 블록 스토리지      | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지    | [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)  |
|-------------|-----------------|---------------|-----------------|
| 저장 단위     | 고정 크기 블록   | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)/디렉토리   | 오브젝트([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)+메타)|
| 접근 방식     | [블록 장치](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/442_block_device/) ([SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/))  | [NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/)/CIFS/SMB  | [HTTP](/knowledge-base/studynote/03_network/09_application_layer_web_email/461_http_stateless_connection_oriented/) [REST API](/knowledge-base/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/)    |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수정   | 블록 단위 수정   | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 수정 가능  | 덮어쓰기만 가능   |
| 확장성        | 제한적           | 중간           | 무한(페타바이트+) |
| 레이턴시      | 매우 낮음 (μs)  | 낮음 (ms)      | 높음 (ms~s)      |
| 비용          | 높음             | 중간           | 낮음             |
| AWS [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)   | EBS              | EFS / FSx     | S3               |

📢 **섹션 요약 비유**: 블록은 [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 드라이브, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 공유 폴더 네트워크, 오브젝트는 구글 드라이브와 같다 — 각각 속도, 공유, 무한 확장을 위해 만들어졌다.

---

## Ⅱ. 블록 스토리지 — EBS, [SAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/493_san_storage_area_network/)

### 블록 스토리지 동작 원리

```
EC2 인스턴스
   │ iSCSI / FC / NVMe-oF
   ↓
블록 스토리지 (EBS)
   [블록 0][블록 1][블록 2]...[블록 N]
          파일시스템(ext4/NTFS)은 OS가 관리
```

### 블록 스토리지 유형 (AWS EBS)

| 유형          | 특성                      | 사용 사례           |
|-------------|--------------------------|-------------------|
| gp3 ([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))   | 범용, 16,000 IOPS        | 대부분 워크로드     |
| io2 Block Express | 고성능, 256K IOPS  | [Oracle](/knowledge-base/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) DB, SAP    |
| st1 ([HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/))   | [처리량](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/) 최적화, 저렴        | 빅데이터, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)      |
| sc1 ([HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/))   | 최저 비용                 | 아카이브 [콜드 데이터](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/676_cold_data_archiving/) |

📢 **섹션 요약 비유**: 블록 스토리지는 컴퓨터에 직접 꽂는 SSD다 — 빠르고 신뢰할 수 있지만, 다른 컴퓨터와 동시에 쓰기가 어렵다.

---

## Ⅲ. [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지 — [NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/), EFS

### [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">클라이언트 A</div>
<div class="kb-diagram-note">NFS v4.1 / SMB 3.0</div>
<div class="kb-diagram-note">클라이언트 B</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">파일 스토리지 서버 (EFS / NetApp)</div>
<div class="kb-diagram-note">/shared/</div>
<div class="kb-diagram-tree-item" style="--depth:7">project/</div>
<div class="kb-diagram-note">── data.csv</div>
<div class="kb-diagram-note">── config.yaml</div>
<div class="kb-diagram-tree-item" style="--depth:7">logs/</div>
</div>
</div>



### AWS EFS vs FSx 비교

| [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)      | 특성                    | 사용 사례          |
|-----------|------------------------|------------------|
| EFS       | 완전 관리형 [NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/), 자동 확장 | [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 공유 볼륨 |
| FSx Lustre | 고성능, ML 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)   | [HPC](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/548_automotive_hpc/), SageMaker    |
| FSx Windows | SMB, AD 통합          | Windows [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 서버  |
| FSx NetApp | ONTAP, 멀티프로토콜     | 엔터프라이즈 [NAS](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/492_nas_network_attached_storage/)   |

📢 **섹션 요약 비유**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지는 학교 서버의 공유 폴더다 — 여러 학생이 같은 폴더에 접속해 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 열고 수정하고 저장할 수 있다.

---

## Ⅳ. [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) — S3 원리

### 오브젝트 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">버킷 (Bucket): my-data-bucket</div>
<div class="kb-diagram-tree-item" style="--depth:1">오브젝트 (Object)</div>
<div class="kb-diagram-tree-item" style="--depth:5">Key: "2024/01/15/logs/app.log"</div>
<div class="kb-diagram-tree-item" style="--depth:5">Value: 실제 데이터 (바이너리)</div>
<div class="kb-diagram-tree-item" style="--depth:5">메타데이터: Content-Type, ETag, 커스텀 태그</div>
<div class="kb-diagram-tree-item" style="--depth:5">버전 ID: v1, v2, v3...</div>
</div>
</div>



### S3 스토리지 클래스 (비용 최적화)

| 클래스              | 접근 빈도   | 비용      | [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 시간 |
|------------------|-----------|---------|---------|
| S3 Standard      | 자주       | 높음     | 즉시      |
| S3 IA            | 가끔       | 중간     | 즉시      |
| S3 Glacier Instant | 드물게   | 낮음     | 즉시      |
| S3 Glacier Deep  | 거의 없음  | 매우 낮음 | 12시간   |

📢 **섹션 요약 비유**: [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 거대한 창고 선반이다 — 번호표([Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/))를 알면 어떤 박스(Object)든 꺼낼 수 있고, 선반은 무한히 늘어난다.

---

## Ⅴ. 다계층 스토리지 아키텍처



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">클라우드 스토리지 아키텍처:</div>
<div class="kb-diagram-note">Web App ──→ EFS (공유 정적 파일)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">DB → EBS io2 (고성능 블록)</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">로그 → S3 Standard (원본)</div>
<div class="kb-diagram-note">↓ 30일 후</div>
<div class="kb-diagram-note">S3 IA (비용 절감)</div>
<div class="kb-diagram-note">↓ 90일 후</div>
<div class="kb-diagram-note">Glacier (장기 보관)</div>
</div>
</div>



### 선택 가이드

| 워크로드            | 권장 스토리지        |
|------------------|-------------------|
| RDBMS (RDS)      | EBS gp3/io2        |
| [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 공유 볼륨 | EFS                |
| 대용량 미디어      | S3 + CloudFront   |
| ML 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋   | FSx Lustre + S3   |
| [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)·아카이브      | S3 Glacier         |

📢 **섹션 요약 비유**: 다계층 스토리지는 집의 수납 공간이다 — 자주 쓰는 물건은 서랍(EBS), 가족이 함께 쓰는 것은 공용 선반(EFS), 거의 안 쓰는 것은 창고(S3 Glacier).

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">클라우드 스토리지 유형</div>
<div class="kb-diagram-tree-item" style="--depth:0">블록 스토리지</div>
<div class="kb-diagram-note">── EBS (AWS), Persistent Disk (GCP)</div>
<div class="kb-diagram-note">── SAN (Storage Area Network)</div>
<div class="kb-diagram-note">── iSCSI / NVMe-oF</div>
<div class="kb-diagram-tree-item" style="--depth:0">파일 스토리지</div>
<div class="kb-diagram-note">── EFS / FSx (AWS), Filestore (GCP)</div>
<div class="kb-diagram-note">── NFS (Network File System)</div>
<div class="kb-diagram-note">── SMB / CIFS</div>
<div class="kb-diagram-tree-item" style="--depth:0">오브젝트 스토리지</div>
<div class="kb-diagram-tree-item" style="--depth:2">S3 (AWS), GCS (GCP), Azure Blob</div>
<div class="kb-diagram-tree-item" style="--depth:2">S3 API 표준 (호환 생태계)</div>
<div class="kb-diagram-tree-item" style="--depth:2">S3 스토리지 클래스 계층</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">클라우드 스토리지 발전 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1990년대</div><div class="kb-diagram-cell">SAN / NAS 등장</div><div class="kb-diagram-cell">블록·파일 스토리지 기업화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2006년</div><div class="kb-diagram-cell">AWS S3 출시</div><div class="kb-diagram-cell">오브젝트 스토리지 클라우드화</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2008년</div><div class="kb-diagram-cell">AWS EBS 출시</div><div class="kb-diagram-cell">클라우드 블록 스토리지 표준</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2015년</div><div class="kb-diagram-cell">AWS EFS GA</div><div class="kb-diagram-cell">관리형 NFS 서비스</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2018년</div><div class="kb-diagram-cell">S3 Intelligent Tier</div><div class="kb-diagram-cell">AI 기반 자동 계층 이동</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2020년대</div><div class="kb-diagram-cell">NVMe-oF·CSI</div><div class="kb-diagram-cell">컨테이너 스토리지 표준화</div></div>
<div class="kb-diagram-note">핵심 키워드 연결:</div>
<div class="kb-diagram-note">블록(EBS) → DB/VM 고성능 워크로드</div>
<div class="kb-diagram-note">파일(EFS) → 컨테이너·공유 파일시스템</div>
<div class="kb-diagram-note">오브젝트(S3) → 비정형 데이터·무한 확장</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">다계층 스토리지 정책 → 비용 최적화 (FinOps)</div>
</div>
</div>



---

## 👶 어린이를 위한 3줄 비유 설명

1. 블록 스토리지는 개인 SSD다 — 혼자 빠르게 쓰는 데는 최고지만 친구와 나누기 어렵다.
2. [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스토리지는 학교 공용 사물함이다 — 여러 명이 같은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 꺼내 볼 수 있다.
3. [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/)는 구글 드라이브다 — 인터넷만 있으면 어디서든 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 올리고 내려받고, 용량은 거의 무한하다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 31 / 371

← **이전**: [31. 로드 밸런서 — 트래픽 분산의 핵심 기술](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/031_load_balancer/)
**다음**: [CDN (Content Delivery Network, 콘텐츠 전달 네트워크)](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/033_cdn/) →

---
