---
title: "468. 클라우드 백업 스냅샷 복제 전략 (Cloud Backup Snapshot Replication Strategy)"
date: 2026-05-09
tags:
  - "studynote-cloud-architecture"
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 클라우드 백업 스냅샷 복제 전략은 **볼륨 레벨 스냅샷(Incremental, Copy-on-Write/Redirect-on-Write 기반) -> 객체 스토리지(S3/Blob/GCS) -> Cross-Region Replication(CRR) + Object Lock/Immutable Storage + Lifecycle Policy**의 3계층 파이프라인으로, RPO/RTO·일관성(Crash/Application)·비용(스냅샷 스폴링) 간 트레이드오프를 엔지니어링하는 DR 아키텍처 의사결정 프레임이다.
> 2. **가치**: 3-2-1-1-0 백업 룰(원본 3사본, 2종 미디어, 1 오프사이트, 1 오프라인/불변, 0 에러 검증)을 자동화하여 랜섬웨어·리전 장애·계정 침해 시 RTO를 86,400초(24h)에서 300초 이내로 단축하고, AWS EBS 기준 스냅샷 스토리지 비용을 Standard 0.05 USD/GB·Standard-IA 0.0125 USD/GB·Glacier 0.004 USD/GB로 92% 절감 가능하다.
> 3. **판단 포인트**: **① 동기 복제(ZERO RPO, 고비용·고지연) vs 비동기 스냅샷 복제(수 분 RPO, 저비용)**, **② 애플리케이션 일관성 확보(Pre/Post Script, VSS, fsfreeze, Quiesce API 사용 여부)**, **③ 불변성(Amazon S3 Object Lock, Azure Blob Immutable Storage, WORM) 및 에어갭(Disconnected Vault) 적용 수준**, **④ 멀티클라우드/리전 종속 탈피(Cohesity, Druva, Veeam 등 3rd-party 활용)** 이 4대 의사결정 축이다.

---

## Ⅰ. 개요 및 필요성

클라우드 전환이 가속화되면서 데이터 보호 패러다임은 **LTO 테이프 -> 온프레미스 디스크 백업(Veeam, NetBackup) -> 클라우드 네이티브 스냅샷(AWS Backup, Azure Backup, GCP Backup) -> 멀티 리전 불변 백업 + CDP(Continuous Data Protection)** 로 진화했다. 그러나 "스냅샷 = 백업"이라는 잘못된 등식이 운영 현장에서 랜섬웨어 취약점의 주범이 되면서, 2023년 MGM Resorts·SolarWinds·DaVita 사태 이후 **"스냅샷조차도 공격자가 암호화할 수 있으므로, 별도의 불변 오프사이트 사본이 필수"** 라는 교훈이 제도화되었다.

핵심 기술적 과제는 다음과 같다.

- **볼륨 무결성 문제**: 단순히 디스크 I/O를 정지하지 않고 찍은 스냅샷은 **Crash-Consistent** 상태이며, 데이터베이스(InnoDB, PostgreSQL, Oracle)는 redo/undo 로그가 일치하지 않아 복구 후 깨질 수 있다. **Application-Consistent** 스냅샷을 위해서는 OS 레벨 quiesce(Windows VSS, Linux fsfreeze/xfs_freeze) 또는 애플리케이션 API 호출(MySQL FLUSH TABLES WITH READ LOCK, Oracle ALTER SYSTEM BEGIN BACKUP) 후 스냅샷을 발행해야 한다.
- **RPO/RTO 격차**: 클라우드 리전 단일 장애(예: AWS us-east-1 2021-12-07 Kinesis 장애)나 계정 침해 시, 동일 리전 내 스냅샷은 무용지물이다. **다른 리전·다른 계정·다른 CSP**로의 복제 경로가 DR의 핵심이다.
- **비용 스폴링(Snapshot Sprawl)**: 스냅샷이 무분별하게 쌓이면 AWS 기준 월 수천만 원의 스토리지 비용이 발생한다. **Lifecycle Policy(예: 30일 후 Standard-IA, 90일 후 Glacier Deep Archive)**로 자동 계층화해야 한다.
- **컴플라이언스**: PCI-DSS 4.0, HIPAA, 금융감독원의 전자금융감독규정, 개인정보보호법은 모두 **오프사이트 백업의 위치·암호화·보존 기간·접근 통제**를 명시한다. 서울 리전 데이터의 해외 리전 이관 시 데이터 주권 검토가 필요하다.

```text
+----------------------- 클라우드 백업·스냅샷·복제 3계층 구조 -----------------------+
|                                                                                  |
|   [Production Workload]            [DR / Cross-Region Target]                    |
|   +------------------+             +------------------+                          |
|   |  App / DB Tier   |             |  Cold DR Region  |                          |
|   |  (EC2, RDS, EKS) |             |  (us-west-2)     |                          |
|   +--------+---------+             +--------^---------+                          |
|            | VSS/fsfreeze                    | CRR (S3 Cross-Region              |
|            | Quiesce API                    | Replication rule)                  |
|   +--------v---------+             +--------+---------+                          |
|   |  Block Storage   |--snapshot--->|  Object Storage  |                          |
|   |  (EBS, Disk)     |             |  (S3 Standard)   |                          |
|   +------------------+             |   +-IA Tier      |                          |
|            |                        |   +-Glacier IR   |                          |
|            | IAM / KMS              |   +-Deep Archive |                          |
|   +--------v---------+             |  + Object Lock   |                          |
|   |  Mgmt Plane       |------------->|  (WORM/Immutable)|                          |
|   |  (AWS Backup,     |   control   +------------------+                          |
|   |   Azure Backup)   |                                                           |
|   +------------------+                                                           |
|                                                                                  |
+----------------------------------------------------------------------------------+
```

기존 패러다임(온프레미스 Veeam + LTO 테이프)이 **RPO 24h, RTO 48h, 용량 한계, 오프사이트 회수 시간 4시간** 수준이었다면, 클라우드 기반 전략은 **RPO 5분(비동기 스냅샷), RTO 1시간(cold standby), RPO 0 / RTO 수십 초(Active-Active + 동기 복제)** 까지 압축하며, 동시에 **불변성(Immutability) + 에어갭(Logical Air Gap)** 으로 랜섬웨어 대응력을 강화했다.

- **📢 섹션 요약 비유**: 옛날 사진관 방식(필름 직접 보관)은 도난·화재에 취약하지만, 요즘 클라우드 사진첩(Google Photos, iCloud)은 여러 나라 데이터센터에 자동 복제·암호화·버전 보존되므로 한 곳이 사라져도 사진이 안전하다. 클라우드 스냅샷 복제 전략이 바로 이 원리다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 스냅샷 메커니즘 (COW vs ROW)

| 메커니즘 | 동작 원리 | 장점 | 단점 | 대표 구현 |
|:---|:---|:---|:---|:---|
| **Copy-on-Write (COW)** | 원본 블록 덮어쓰기 발생 시 새 위치에 복사 후 메타데이터 갱신 | 첫 스냅샷이 논리적으로 즉시 생성, 읽기 성능 저하 없음 | 쓰기 시 복사 오버헤드(2배 I/O), EBS·Xen 기반 | AWS EBS, VMware VMFS |
| **Redirect-on-Write (ROW)** | 새 쓰기는 별도 영역에 기록, 메타데이터만 갱신 | 쓰기 성능 저하 없음, SSD 친화적 | 초기 스냅샷 생성 비용 큼, 삭제 전까지 공간 점유 | ZFS, Btrfs, NetApp WAFL, 일부 HCI |
| **Incremental Forever** | 첫 풀 + 이후 델타 블록만 저장 | 스토리지 효율 극대화(중복 제거), RPO 단축 | 메타데이터 체인 손상 시 전체 재구성, 복원 시 모든 체인 필요 | Veeam, Commvault, Rubrik |

> **핵심**: AWS EBS 스냅샷은 S3에 **Incremental Forever** 방식으로 저장된다. 첫 스냅샷이 풀 백업이며, 이후는 변경된 블록만 기록된다. 스냅샷 자체 삭제 시 후속 스냅샷에서 참조하는 블록은 유지되므로 **참조 무결성(referential integrity)** 관리가 백엔드에서 자동 수행된다.

### 2. 복제 모드(Replication Mode) 분류

| 모드 | RPO | 대역폭/지연 | 사용 사례 | 기술 예 |
|:---|:---|:---|:---|:---|
| **동기 복제(Synchronous)** | 0초 | 동일 AZ 내 필수, 왕복 지연 < 10ms 제약 | 미션 크리티컬(핵심 뱅킹, HA) | AWS EBS Multi-Attach + FSx, Azure Ultra Disk, GCP Hyperdisk-Balanced (regional PD) |
| **비동기 복제(Asynchronous)** | 초~분 | WAN 비용 발생, 지연 무관 | DR, 리전 간 재해 대비 | S3 CRR, Azure Blob Object Replication, RDS Cross-Region Read Replica, Aurora Global Database |
| **스냅샷 기반 복제** | 분~시간(스케줄 의존) | 배치 전송, 비용 최저 | 일반 워크로드, 장기 보존 | AWS Backup Cross-Region Copy, Azure Backup Vault (GRS), GCP Snapshot Schedule |
| **CDP(Continuous Data Protection)** | ~초 | 로그/블록 단위 스트리밍 | Zero-RPO 요구 | Zerto, Veeam CDP, AWS Aurora Backtrack, Druva |

### 3. 핵심 아키텍처 흐름

```text
+------------------- End-to-End 스냅샷·복제 파이프라인 상세 -------------------+
|                                                                              |
|  +------------+   ①Quiesce    +------------+   ②Snapshot   +------------+   |
|  |  App Server|--------------->|  EBS / Disk|--------------->|  S3 / Blob |   |
|  |  + DB      |  VSS/fsfreeze |  (Primary) |  Incremental  |  (Primary) |   |
|  +------------+   ②-1 Post     +------------+               +-----+------+   |
|                            ^                                    |           |
|                            | Lifecycle Policy                    | ③ CRR     |
|                            | (IA/Glacier)                        v           |
|                       +----+------+                       +--------------+   |
|                       | KMS/CMK   |                       | S3 / Blob    |   |
|                       | 암호화     |                       | (DR Region)  |   |
|                       +-----------+                       | +Object Lock |   |
|                                                            +------+-------+   |
|   ⑤Restore/DR Drill                                          |           |
|   +------------+                                             |           |
|   |  Test Env  |<----------------- ④Recovery/Validation -----+           |
|   |  Sandbox   |     (자동 검증 스크립트)                                  |
|   +------------+                                                           |
|                                                                              |
+------------------------------------------------------------------------------+
```

**단계별 상세 동작:**

1. **Pre-Snapshot Hook**: AWS Systems Manager Automation Runbook, Azure Automation Runbook, GCP Cloud Functions가 `fsfreeze -f /mnt/data` -> 스냅샷 -> `fsfreeze -u` 순서로 호출. DB는 FLUSH BINARY LOGS / pg_basebackup / BEGIN BACKUP 수행.
2. **Snapshot 생성**: EBS API(`CreateSnapshot`)는 비동기적으로 실행되며, 완료까지 수 분~수십 분 소요. 증분 블록만 S3로 업로드된다.
3. **Cross-Region Copy**: AWS Backup의 `CopyAction` 또는 S3 CRR Rule로 대상 리전에 복제. 전송 중 SSE-KMS로 암호화 유지, 리전 간 TLS 1.2+ 적용.
4. **Object Lock 적용**: S3 Object Lock Governance/Compliance 모드로 retention 기간(예: 7일~10년) 설정. 이 기간 동안에는 Root 계정이라도 삭제 불가(Compliance 모드).
5. **자동 검증**: AWS Lambda가 주기적으로 가장 오래된 스냅샷으로 테스트 인스턴스 부팅 -> DB 무결성 체크섬 확인 -> Slack/Teams 알림.

### 4. 핵심 컴포넌트 표

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Quiesce Agent** | OS·DB 일관성 확보 | Windows VSS Writer, Linux `fsfreeze`(LVM)·`xfs_freeze`, Oracle RMAN `ALTER SYSTEM BEGIN BACK
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 468 / 800

<- **이전**: [467. 클라우드 재해 복구 DR 다중 리전](/studynote/13_cloud_architecture/06_exam_summary/467_cloud_disaster_recovery_dr_multi_region/)
**다음**: [469. 클라우드 오토스케일링 수요 기반 확장](/studynote/13_cloud_architecture/06_exam_summary/469_cloud_autoscaling_demand_based_scaling/) ->

---
