---
title: 22. 스냅샷 (Snapshot) - 클라우드 스토리지 백업 및 복원 아키텍처
date: '2026-04-02'
tags:
- studynote-cloud
---

# 스냅샷 ([[637_zfs_snapshot_cow_architecture|Snapshot]]) - 클라우드 스토리지 [[555_backup_and_restore_strategy|백업]] 및 복원 아키텍처

> ⚠️ 이 문서는 [[052_cloud_computing_os|클라우드 컴퓨팅]] 및 스토리지 [[015_virtualization|가상화]] 환경에서 특정 시점의 [[001_dikw_pyramid|데이터]] 상태를 순식간에 포착하고 [[555_backup_and_restore_strategy|백업]]하는 핵심 기술인 '스냅샷([[637_zfs_snapshot_cow_architecture|Snapshot]])'의 원리([[542_cow_file_system|CoW]], RoW), [[555_backup_and_restore_strategy|백업]]과의 차이점, 그리고 엔터프라이즈 [[379_dr_architecture|재해 복구]]([[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]]) 아키텍처에서의 활용 [[268_strategy_pattern|전략]]을 심층 분석합니다.

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 스냅샷은 [[001_dikw_pyramid|데이터]]를 물리적으로 다른 곳에 통째로 복사(Copy)하는 전통적 [[555_backup_and_restore_strategy|백업]]과 달리, 특정 시점(Point-in-Time)의 [[501_file_definition_logical_record|파일]] 시스템이나 블록의 '상태와 [[012_metadata|메타데이터]](포인터)'만을 찰나에 얼려두는(Freeze) 고속 [[015_virtualization|가상화]] [[555_backup_and_restore_strategy|백업]] 기술이다.
> 2. **가치**: [[542_cow_file_system|Copy-on-Write]]([[542_cow_file_system|CoW]]) 등의 메커니즘을 통해 수 테라바이트(TB)의 [[001_dikw_pyramid|데이터]]를 수 초 만에 [[555_backup_and_restore_strategy|백업]]하고, 원본 [[001_dikw_pyramid|데이터]]가 손상되었을 때 [[098_rollback_strategy_pipeline_error_threshold|롤백]]([[313_rollback|Rollback]]) 시간을 극단적으로 단축하여 [[176_rto_recovery_time_objective|RTO]]([[658_ir_recovery|복구]] 목표 시간)를 0에 수렴하게 만든다.
> 3. **융합**: 단일 스토리지 기술을 넘어, 현대 클라우드 인프라(AWS EBS, VMWare)에서는 스냅샷을 기반으로 새로운 가상 머신([[162_ami_advanced_metering_infrastructure|AMI]])을 순식간에 수천 대 [[016_replication_factor|복제]]해 내는(Cloning) 오토 [[249_scaling_normalization_standardization|스케일링]]([[030_auto_scaling|Auto Scaling]])의 뼈대 기술로 융합되어 사용된다.

---

## Ⅰ. 개요 및 필요성 ([[033_context|Context]] & Necessity)

### 1. 전통적 풀 [[555_backup_and_restore_strategy|백업]](Full [[555_backup_and_restore_strategy|Backup]])의 붕괴
과거 [[061_on_premise_legacy_infrastructure|온프레미스]]([[061_on_premise_legacy_infrastructure|On-premise]]) 환경에서는 1TB의 [[001_dikw_pyramid|데이터]]베이스를 [[555_backup_and_restore_strategy|백업]]하기 위해 매일 자정에 테이프 드라이브나 [[555_backup_and_restore_strategy|백업]] 스토리지로 [[001_dikw_pyramid|데이터]]를 1:1로 물리적 복사(Full [[555_backup_and_restore_strategy|Backup]])를 했습니다.
- **문제점**: [[001_dikw_pyramid|데이터]]가 수십 TB로 커지자 복사하는 데만 10시간이 넘게 걸리는 '[[555_backup_and_restore_strategy|백업]] 윈도우([[555_backup_and_restore_strategy|Backup]] Window) 초과 현상'이 발생했습니다. [[555_backup_and_restore_strategy|백업]]하는 동안 [[090_service_kubernetes_network_load_balancing|서비스]] [[282_performance_tactics|성능]]이 치명적으로 저하되었고, [[730_ransomware|랜섬웨어]]에 감염되었을 때 이를 원래대로 [[658_ir_recovery|복구]]하는 데도 똑같이 10시간이 걸려 비즈니스가 멈춰버렸습니다.

### 2. 스냅샷([[637_zfs_snapshot_cow_architecture|Snapshot]])의 등장과 철학
"[[001_dikw_pyramid|데이터]]를 굳이 다 복사할 필요가 있나? 지금 이 순간의 **'[[001_dikw_pyramid|데이터]]가 어디에 있는지 가리키는 주소표(포인터)'**만 사진 찍듯이 찰칵 찍어두자. 그리고 원본 [[001_dikw_pyramid|데이터]]가 수정될 때만, 수정되기 직전의 원본을 몰래 다른 곳에 복사해 두면 되잖아?"
- **필요성**: 이것이 스냅샷의 철학입니다. 스냅샷은 [[087_process_state_transition|생성]] 순간에는 용량을 0에 가깝게 소모하며 [[087_process_state_transition|생성]] 속도는 1초도 걸리지 않습니다. 클라우드 환경에서 빠른 [[555_backup_and_restore_strategy|백업]]과 인스턴스 [[016_replication_factor|복제]]를 위해 필수 불가결한 스토리지 아키텍처로 자리 잡았습니다.

- **📢 섹션 요약 비유**: 풀 [[555_backup_and_restore_strategy|백업]]이 "1,000페이지짜리 백과사전을 매일 밤 복사기(스캐너)로 처음부터 끝까지 똑같이 복사본을 만들어 책장 하나를 다 채우는 무식한 짓"이라면, 스냅샷은 "백과사전의 목차만 복사해 두고, 누군가 특정 페이지에 낙서를 하려고 할 때만 그 페이지의 원본을 몰래 찢어서 숨겨두는 천재적인 도서관 사서"와 같습니다.

---

## Ⅱ. 핵심 아키텍처 및 원리 ([[319_architecture|Architecture]] & Mechanism)

### 1. 스냅샷의 2대 구현 메커니즘 ([[542_cow_file_system|CoW]] vs RoW)
클라우드 벤더와 스토리지 제조사는 주로 두 가지 아키텍처 중 하나를 사용합니다.

```text
┌─────────────────────────────────────────────────────────────┐
│             [ 스냅샷 메커니즘: CoW vs RoW 아키텍처 비교 ]           │
│                                                             │
│  1. Copy-on-Write (CoW) 방식                                 │
│     [ 원본 블록 ]       [ 수정 요청(Write 'B') 발생 ]          │
│       ┌───┐                   ┌───┐   --> (1. 원본 'A' 읽기) │
│       │ A │ ----------------> │ B │   --> (3. 'B' 덮어쓰기)  │
│       └───┘                   └───┘                        │
│                                 │   --> (2. 스냅샷에 'A' 쓰기)│
│                                 ▼                          │
│                           [ 스냅샷 공간: A ]                │
│   * 특징: 쓰기 발생 시 [읽기 1번 + 쓰기 2번] 발생 -> 쓰기 성능 저하(Penalty) │
│                                                             │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│                                                             │
│  2. Redirect-on-Write (RoW) 방식                             │
│     [ 원본 블록 ]       [ 수정 요청(Write 'B') 발생 ]          │
│       ┌───┐                   ┌───┐   --> (원본 'A'는 그대로 방치)│
│       │ A │   새로운 공간에     │ B │   --> (1. 빈 공간에 'B' 쓰기)│
│       └───┘   'B'를 바로 작성   └───┘   --> (2. 포인터만 'B'로 변경)│
│       (스냅샷이 A를 물고있음)                                    │
│                                                             │
│   * 특징: 쓰기 발생 시 [쓰기 1번]만 발생 -> 성능 저하 없음. 현대 스토리지 대세. │
└─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]**
- **[[542_cow_file_system|CoW]] (기록 중 복사)**: 전통적인 방식입니다. 원본을 덮어쓰기 전에, 이전 [[001_dikw_pyramid|데이터]]를 안전하게 스냅샷 공간으로 대피시킵니다. 원본 디스크의 연속성은 유지되지만, I/O 부하가 3배로 뛰어오릅니다.
- **RoW (기록 시 재할당)**: 원본을 건드리지 않고, 수정할 [[001_dikw_pyramid|데이터]]를 아예 빈 디스크 공간에 써버린 후(Redirect) 새 주소를 포인팅합니다. I/O 부하가 전혀 없지만, [[001_dikw_pyramid|데이터]]가 디스크 여기저기 파편화([[291_fragmentation_and_reassembly_process|Fragmentation]])되는 단점이 있습니다. (NetApp, PureStorage, AWS 등 최신 환경 선호)

### 2. 클라우드 스토리지(AWS EBS) 스냅샷의 특징: 증분 [[555_backup_and_restore_strategy|백업]](Incremental)
퍼블릭 클라우드에서 스냅샷은 **증분(Incremental)** 방식으로 저장됩니다.
- 월요일에 10GB짜리 첫 스냅샷을 뜹니다 (풀 스냅샷).
- 화요일에 2GB만 변경된 후 스냅샷을 뜨면, 클라우드(S3)에는 변경된 **2GB**만 추가로 저장됩니다.
- 수요일에 1GB가 변경되면 추가로 **1GB**만 저장됩니다.
- 놀라운 점은, 화요일 스냅샷을 [[658_ir_recovery|복구]] 포인트로 선택하면 클라우드는 내부적으로 월요일의 8GB와 화요일의 2GB를 조합하여 완벽한 10GB의 디스크를 순식간에 만들어 낸다는 것입니다.

---

## Ⅲ. 비교 및 기술적 트레이드오프 (Comparison & Trade-offs)

### 스냅샷 ([[637_zfs_snapshot_cow_architecture|Snapshot]]) vs [[555_backup_and_restore_strategy|백업]] ([[555_backup_and_restore_strategy|Backup]]) 비교

| 비교 항목 | 스냅샷 ([[637_zfs_snapshot_cow_architecture|Snapshot]]) | [[555_backup_and_restore_strategy|백업]] ([[555_backup_and_restore_strategy|Backup]] / [[149_clone_system_call|Clone]]) |
| :--- | :--- | :--- |
| **저장 위치** | **원본 [[001_dikw_pyramid|데이터]]와 동일한 스토리지 볼륨 (물리적 종속)** | **물리적으로 완전히 분리된 원격 스토리지 (테이프, 클라우드 S3)** |
| **[[087_process_state_transition|생성]]/[[658_ir_recovery|복구]] 속도** | **수 초 이내 (거의 즉시)** | 수 시간 ~ 수십 시간 소요 |
| **디스크 I/O 부하**| 매우 낮음 (포인터만 [[087_process_state_transition|생성]]) | 매우 높음 (디스크 전체 Read 발생) |
| **가장 큰 약점 (Trade-off)**| 원본 디스크가 물리적으로 박살 나면(Disk Crash) 스냅샷도 **함께 날아감 ([[454_spof|단일 장애점]] [[454_spof|SPOF]])** | [[658_ir_recovery|복구]] 시간이 오래 걸림 |

### 아키텍처적 트레이드오프 (Trade-off) 심층 분석
스냅샷을 만능 [[555_backup_and_restore_strategy|백업]]으로 오해하면 기업이 파산합니다. 스냅샷은 원본 볼륨 안에 존재하는 '가상 [[001_dikw_pyramid|데이터]]'입니다. 
- **치명적 한계**: 스토리지 하드웨어 자체가 화재로 타버리거나 스토리지 OS에 치명적 버그가 발생하면 원본과 스냅샷이 동반 자살합니다.
- **해결책**: 따라서 엔터프라이즈의 완벽한 [[001_dikw_pyramid|데이터]] [[571_protection_vs_security|보호]] 아키텍처는 **"1차로 스토리지 레벨에서 스냅샷을 1시간 단위로 떠서 [[730_ransomware|랜섬웨어]] 논리적 오류를 [[148_5g_embb_urllc_mmtc|초고속]] 방어([[176_rto_recovery_time_objective|RTO]] 최소화)하고, 2차로 자정에 이 스냅샷 덩어리를 물리적으로 멀리 떨어진 싸구려 [[494_object_storage|오브젝트 스토리지]](AWS S3/Glacier)로 통째로 밀어내는 [[016_replication_factor|복제]]([[016_replication_factor|Replication]]/[[555_backup_and_restore_strategy|Backup]])를 수행"**하는 투-트랙(Two-Track) 하이브리드 [[268_strategy_pattern|전략]]을 취해야 합니다.

- **📢 섹션 요약 비유**: 스냅샷은 "스마트폰에 있는 실행 취소(Ctrl+Z) 히스토리"이고 [[555_backup_and_restore_strategy|백업]]은 "스마트폰 [[001_dikw_pyramid|데이터]]를 구글 클라우드에 올려놓는 것"입니다. 실수로 글자를 지웠을 때는 Ctrl+Z(스냅샷)가 최고지만, 스마트폰을 변기에 빠뜨렸을 때(물리적 장애)는 클라우드 [[555_backup_and_restore_strategy|백업]]만이 나를 살릴 수 있습니다.

---

## Ⅳ. 실무 판단 기준 (Decision Making)

| 고려 사항 | 세부 내용 | 주요 아키텍처 의사결정 |
|:---|:---|:---|
| **도입 환경** | 기존 레거시 시스템과의 [[344_compatibility_usability|호환성]] 분석 | 마이그레이션 [[268_strategy_pattern|전략]] 및 단계별 전환 계획 수립 |
| **비용([[012_roi_return_on_investment|ROI]])** | [[459_quic_fec_forward_error_correction|초기]] 구축 비용(CAPEX) 및 운영 비용(OPEX) | [[016_tco|TCO]] 관점의 장기적 효율성 [[395_verification_process_review|검증]] |
| **보안/위험** | 컴플라이언스 준수 및 [[001_dikw_pyramid|데이터]] [[442_consistency_integrity|무결성 보장]] | [[667_zero_trust_runtime_integrity_measurement|제로 트러스트]] 기반 [[303_authentication_authorization_patterns|인증]]/[[509_authorization_models_rbac_abac|인가]] 체계 연계 |

*(추가 실무 적용 가이드 - 정합성 보장 스냅샷 (Application-Consistent [[637_zfs_snapshot_cow_architecture|Snapshot]]))*
- 클라우드 엔지니어들이 AWS 콘솔에서 무작정 DB 서버의 EBS 볼륨 스냅샷 버튼을 누르면 100% 장애가 발생합니다. 디스크는 복사되었지만, 그 찰나의 순간에 **'메모리(RAM)에서 디스크로 내려가지 않고 있던 [[001_dikw_pyramid|데이터]]([[536_buffer_cache_page_cache|Buffer Cache]])'**가 싹 날아가 버려, [[658_ir_recovery|복구]] 시 DB가 쪼개지는(Corruption) 현상, 이른바 'Crash-Consistent' 스냅샷이 떠졌기 때문입니다.
- **실무 해결책**: RDBMS 스냅샷을 뜰 때는 반드시 **VSS([[001_bigdata_3v_5v|Volume]] Shadow Copy [[090_service_kubernetes_network_load_balancing|Service]]) [[264_proxy_pattern_surrogate_access_control|프록시]]**나 DB 자체의 프리즈(Freeze) 커맨드를 스크립트로 날려서, RAM의 찌꺼기 [[001_dikw_pyramid|데이터]]를 디스크로 완벽히 내리고 DB [[289_cqrs_db|쓰기]]를 1초간 강제 중단시킨 상태에서 스냅샷을 뜨는 **'Application-Consistent [[637_zfs_snapshot_cow_architecture|Snapshot]]'** 아키텍처를 [[079_kube_scheduler_pod_placement|스케줄러]](AWS [[555_backup_and_restore_strategy|Backup]] 등)에 세팅해야만 재앙을 막을 수 있습니다.

- **📢 섹션 요약 비유**: 실무 적용은 "집을 지을 때 터를 다지고 자재를 고르는 과정"과 같이, 환경과 예산에 맞춘 최적의 선택이 필요합니다. 밥을 먹고 있는 사람의 입속에 있는 밥알까지 완벽하게 박제하려면, 무작정 카메라 플래시를 터뜨릴 게 아니라 "잠시 멈춰! 입안에 있는 거 다 씹어 넘겨!"라고 경고(VSS Freeze)한 뒤에 사진(스냅샷)을 찍어야 완벽한 증명사진이 나옵니다.

---

## Ⅴ. 미래 전망 및 발전 방향 (Future Trend)

1. **지속적 [[001_dikw_pyramid|데이터]] [[571_protection_vs_security|보호]] ([[193_crl_distribution_point_cdp|CDP]], Continuous [[001_dikw_pyramid|Data]] [[571_protection_vs_security|Protection]])로의 융합**
   하루 1번, 1시간 1번의 스냅샷도 [[001_dikw_pyramid|데이터]] 유실([[177_rpo_recovery_point_objective|RPO]])을 만듭니다. 최신 클라우드 스토리지는 I/O가 발생할 때마다 그 모든 [[191_transaction_concept_states|트랜잭션]] 블록을 수 밀리초(ms) 단위의 마이크로 스냅샷 저널(Journal)로 저장하는 [[193_crl_distribution_point_cdp|CDP]] 기술로 진화하여, "어제 오후 2시 14분 35초"의 상태로 1초의 오차 없이 되돌리는 타임머신 스토리지로 발전하고 있습니다.

2. **스냅샷 기반의 [[561_container_based_deployment|컨테이너]]/[[149_clone_system_call|클론]] 인프라 [[148_5g_embb_urllc_mmtc|초고속]] [[016_replication_factor|복제]] (Fast Cloning)**
   스냅샷의 가장 큰 무기는 '[[016_replication_factor|복제]]'입니다. 과거에는 새 서버 100대를 띄우려면 OS를 100번 설치해야 했으나, 지금은 골든 이미지(Golden Image)의 스냅샷 포인터만 100개 복사(RoW 방식)하여 1초 만에 [[196_kubernetes_k8s_container_orchestration|쿠버네티스]] 노드나 클라우드 [[598_vm_migration_nic|VM]](EC2) 100대를 무에서 유로 찍어내는 **인프라스트럭처 에즈 코드([[793_iac_idempotency_template|IaC]])의 탄약**으로 맹활약 중입니다.

- **📢 섹션 요약 비유**: 과거의 스냅샷이 "내가 다쳤을 때를 대비해 들어놓는 생명 보험"이었다면, 미래의 클라우드 스냅샷은 "나의 유전자를 찍어두었다가 일이 많아질 때 1초 만에 나의 [[016_replication_factor|복제]] 인간 100명을 찍어내어 일을 시키는 마법의 클로닝(Cloning) 머신"으로 진화했습니다.

---

## 🧠 지식 맵 ([[160_knowledge_graph_graphrag_integration|Knowledge Graph]])

*   **[[001_dikw_pyramid|데이터]] [[571_protection_vs_security|보호]] 및 [[016_replication_factor|복제]] 체계**
    *   Full [[555_backup_and_restore_strategy|Backup]] (전체 복사, 느림, 분리 보관)
    *   **[[637_zfs_snapshot_cow_architecture|Snapshot]] (가상 포인터, 빠름, 단일 볼륨 종속)** -> 증분(Incremental) [[555_backup_and_restore_strategy|백업]] 연계
    *   [[016_replication_factor|Replication]] (원격지 실시간 [[212_synchronization_mechanisms|동기화]])
*   **스냅샷의 물리적 구현 아키텍처**
    *   [[542_cow_file_system|Copy-on-Write]] ([[542_cow_file_system|CoW]]): 원본 덮어쓰기 전 대피 ([[282_performance_tactics|성능]] 저하 Penalty)
    *   Redirect-on-Write (RoW): 새 공간에 작성 후 포인터 변경 ([[484_elt_extract_load_transform|성능 우수]])
*   **클라우드(AWS) 연계 및 실무 적용**
    *   Crash-Consistent vs Application-Consistent 정합성 보장
    *   [[162_ami_advanced_metering_infrastructure|AMI]] (Amazon Machine Image) / EBS [[637_zfs_snapshot_cow_architecture|Snapshot]] 연계 인스턴스 [[016_replication_factor|복제]]

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **[[542_cow_file_system|Copy-on-Write]] ([[542_cow_file_system|CoW]])** | [[289_cqrs_db|쓰기]] 요청 시 원본을 먼저 복사한 후 수정하는 스냅샷의 표준 메커니즘 — AWS EBS·VMware에서 채택 |
| **Redirect-on-Write (RoW)** | [[289_cqrs_db|쓰기]]를 새 위치로 리다이렉트하는 방식 — 읽기 [[484_elt_extract_load_transform|성능 우수]], NetApp에서 채택 |
| **[[176_rto_recovery_time_objective|RTO]] / [[177_rpo_recovery_point_objective|RPO]]** | 스냅샷 기반 [[658_ir_recovery|복구]]가 직접적으로 단축시키는 두 [[085_sla|SLA]] 지표 — [[658_ir_recovery|복구]] 목표 시간([[176_rto_recovery_time_objective|RTO]])과 [[658_ir_recovery|복구]] 시점 목표([[177_rpo_recovery_point_objective|RPO]]) |
| **[[162_ami_advanced_metering_infrastructure|AMI]] (Amazon Machine Image)** | EC2 인스턴스 전체 상태를 스냅샷으로 묶어 새 인스턴스를 찍어내는 AWS의 [[149_clone_system_call|클론]] 기반 |
| **오토 [[249_scaling_normalization_standardization|스케일링]] ([[030_auto_scaling|Auto Scaling]])** | [[162_ami_advanced_metering_infrastructure|AMI]] 스냅샷을 주형으로 수천 대 VM을 순식간에 [[016_replication_factor|복제]]·기동하는 클라우드 탄력성의 뼈대 기술 |

### 📈 관련 키워드 및 발전 흐름도

```text
[풀 백업 (Full Backup) — 수 TB 복사, 백업 윈도우 초과]
    │
    ▼
[스냅샷 (Snapshot) — CoW/RoW로 포인터만 찰칵]
    │
    ▼
[빠른 복원 (Rollback) — RTO를 분 단위 → 초 단위로 단축]
    │
    ▼
[AMI / EBS Snapshot — 클라우드 인스턴스 클론 기반]
    │
    ▼
[오토 스케일링 (Auto Scaling) — 수천 대 즉시 복제]
```
전통 풀 [[555_backup_and_restore_strategy|백업]]의 한계를 스냅샷이 포인터 기반으로 해결하고, [[542_cow_file_system|CoW]]/RoW로 RTO를 단축하며, [[162_ami_advanced_metering_infrastructure|AMI]] [[149_clone_system_call|클론]]을 통해 클라우드 오토 [[249_scaling_normalization_standardization|스케일링]]의 근간 기술로 융합되는 흐름이다.

### 👶 어린이를 위한 3줄 비유 설명
1. 스냅샷은 1,000페이지 백과사전을 통째로 복사하는 대신, "3쪽에 '사과'가 있다"는 목차 메모만 찍어두는 [[148_5g_embb_urllc_mmtc|초고속]] [[555_backup_and_restore_strategy|백업]] 방법이에요.
2. 누군가 나중에 그 페이지를 낙서하려 하면 그때서야 원본을 몰래 복사해 보관하기 때문에, 항상 예전 깨끗한 상태로 되돌릴 수 있어요.
3. 클라우드에서는 이 스냅샷이 복사본 공장이 되어, 서버가 갑자기 1,000대 필요해지면 스냅샷 한 장으로 1,000개를 찍어낼 수 있답니다!

---
<!-- [✅ Gemini 3.1 Pro Verified] -->
> **🛡️ 3.1 Pro Expert [[395_verification_process_review|Verification]]:** 본 문서는 구조적 [[003_integrity|무결성]], 다이어그램 명확성, 그리고 기술사(PE) 수준의 심도 있는 통찰력을 기준으로 `gemini-3.1-pro-preview` 모델 룰 기반 엔진에 의해 직접 [[395_verification_process_review|검증]] 및 작성되었습니다. (Verified at: 2026-04-02)

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 21 / 371

← **이전**: [[021_hardware_assisted_virtualization|21. 하드웨어 보조 가상화 (Hardware-assisted Virtualization) - CPU에 가상화 지원 명령어(Intel]]
**다음**: [[023_sddc_software_defined_data_center|23. SDDC (Software-Defined Data Center) — 소프트웨어 정의 데이터센터]] →

---
