+++
weight = 626
title = "626. 재해 복구 시스템 (DRS) 스토리지 미러링"
date = "2026-05-08"
[extra]
categories = "studynote-computer-architecture"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[175_drs_bcp_strategy|재해 복구 시스템]] (DRS, Disaster [[658_ir_recovery|Recovery]] System) 스토리지 [[333_raid_1|미러링]]은 주 센터의 [[289_cqrs_db|쓰기]] [[001_dikw_pyramid|데이터]]를 원격 센터에 [[016_replication_factor|복제]]해, 건물 단위 재난에서도 [[090_service_kubernetes_network_load_balancing|서비스]] 재개의 기반 [[001_dikw_pyramid|데이터]]를 남기는 기술이다.
> 2. **가치**: 이 기술은 디스크 고장에 대응하는 RAID보다 [[571_protection_vs_security|보호]] 범위가 넓으며, 랙·전원·[[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 전체 장애를 견디는 지리적 복원력을 만든다.
> 3. **판단 포인트**: 동기식 ([[010_동기식_비동기식_전송|Synchronous]]) [[333_raid_1|미러링]]은 [[015_지연_데이터_관점|지연]]과 거리 제한을 감수하는 대신 [[177_rpo_recovery_point_objective|RPO]] 0에 가깝고, 비동기식 (Asynchronous) [[333_raid_1|미러링]]은 [[282_performance_tactics|성능]]과 장거리를 확보하는 대신 [[001_dikw_pyramid|데이터]] 유실 가능성을 받아들인다.

---

## Ⅰ. 개요 및 필요성

[[175_drs_bcp_strategy|재해 복구 시스템]] (DRS, Disaster [[658_ir_recovery|Recovery]] System)은 화재, 침수, 광역 정전, 통신 두절처럼 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 전체가 멈추는 사고를 전제로 설계한 [[658_ir_recovery|복구]] 체계다. 이때 핵심이 되는 하드웨어 기술이 스토리지 [[333_raid_1|미러링]] (Storage Mirroring)이다. 즉 운영 중인 주 센터의 [[001_dikw_pyramid|데이터]]를 멀리 떨어진 보조 센터에도 거의 같은 시점으로 [[016_replication_factor|복제]]해 두어, [[090_service_kubernetes_network_load_balancing|서비스]] 재개에 필요한 저장 기반을 잃지 않게 만든다.

이 개념이 필요한 이유는 서버 내부 이중화만으로는 건물 수준 재난을 막지 못하기 때문이다. [[483_raid_overview|RAID]], 이중 전원공급장치, 듀얼 스위치는 같은 랙이나 같은 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 안의 고장에는 강하지만, 센터 자체가 정전되거나 폐쇄되면 함께 영향을 받는다. 따라서 고가용성 (HA, High [[452_availability|Availability]])이 "같은 장소 안에서 안 멈추는 구조"라면, DRS는 "장소가 사라져도 다시 시작할 수 있는 구조"라고 볼 수 있다.

스토리지 [[333_raid_1|미러링]]이 없으면 원격지에 서버가 남아 있어도 최신 [[001_dikw_pyramid|데이터]]가 없다. 결국 운영자는 오래된 [[555_backup_and_restore_strategy|백업]]을 찾아 [[658_ir_recovery|복구]]해야 하고, 그만큼 목표 [[658_ir_recovery|복구]] 시점 ([[177_rpo_recovery_point_objective|RPO]], [[177_rpo_recovery_point_objective|Recovery Point Objective]])과 목표 [[658_ir_recovery|복구]] 시간 ([[176_rto_recovery_time_objective|RTO]], [[176_rto_recovery_time_objective|Recovery Time Objective]])이 동시에 악화된다. 그래서 DRS의 본질은 원격 센터에 장비를 두는 것이 아니라, **주 센터의 [[289_cqrs_db|쓰기]] 흐름을 어디까지 원격에 [[016_replication_factor|복제]]할 것인가**를 정하는 데 있다.

- **📢 섹션 요약 비유**: DRS [[333_raid_1|미러링]]은 집에 금고 하나 더 두는 것이 아니라, 다른 동네 은행 금고에 내 통장 내용을 계속 복사해 두는 것과 같다. 집이 불타도 다른 곳에서 바로 잔액을 확인할 수 있어야 진짜 대비가 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

스토리지 [[333_raid_1|미러링]]의 핵심 질문은 간단하다. "주 센터에 [[289_cqrs_db|쓰기]] 요청이 들어왔을 때, 언제 완료 응답 (ACK, Acknowledgement)을 줄 것인가?" 이 답에 따라 동기식과 비동기식이 갈린다. 동기식은 원격 센터까지 반영된 뒤 ACK를 주고, 비동기식은 주 센터에만 먼저 반영한 뒤 나중에 원격으로 보낸다.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│             ACK timing decides latency, distance, and data loss          │
├──────────────────────────────────────────────────────────────────────────┤
│ Sync  : Host -> Primary -> WAN -> Secondary -> ACK -> Host              │
│ Async : Host -> Primary -> ACK -> Host                                  │
│                          └──── Journal / Queue ───▶ Secondary           │
└──────────────────────────────────────────────────────────────────────────┘
```

이 그림에서 보듯 동기식은 [[289_cqrs_db|쓰기]] [[015_지연_데이터_관점|지연]]시간에 네트워크 왕복시간 ([[441_rtt_round_trip_time_srtt_smoothed|RTT]], [[441_rtt_round_trip_time_srtt_smoothed|Round Trip Time]])이 직접 들어간다. 그래서 보통 수 ms 이하 [[015_지연_데이터_관점|지연]]과 비교적 짧은 거리의 메트로 구간에서 유리하다. 반면 비동기식은 주 센터 응답 경로에서 원격 WAN을 떼어 내기 때문에 [[282_performance_tactics|성능]]과 거리에서 훨씬 유연하지만, 큐에 남아 아직 전송되지 않은 [[001_dikw_pyramid|데이터]]가 있으면 장애 시 그 구간만큼 RPO가 생긴다.

| 구분 | 동기식 [[333_raid_1|미러링]] | 비동기식 [[333_raid_1|미러링]] |
| :-- | :-- | :-- |
| ACK 시점 | 원격 센터 기록 후 | 주 센터 기록 직후 |
| [[177_rpo_recovery_point_objective|RPO]] | 0에 근접 | 0보다 큼 |
| [[015_지연_데이터_관점|지연]] 영향 | WAN 왕복시간 직접 반영 | 주 센터 [[282_performance_tactics|성능]] 위주 |
| 거리 제약 | 큼 | 작음 |
| 적합 업무 | 금융 거래, 계정 원장 | 쇼핑몰, 일반 업무 시스템 |

실제 구현에서는 단순 [[501_file_definition_logical_record|파일]] 복사보다 더 정교한 장치가 필요하다. [[002_database_definition|데이터베이스]] [[568_logs_distributed_logging_elk_fluentd|로그]]와 [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]처럼 여러 볼륨이 함께 움직이는 경우, [[194_consistency_database_integrity|일관성]] 그룹 ([[194_consistency_database_integrity|Consistency]] Group)으로 [[289_cqrs_db|쓰기]] 순서를 보존해야 [[658_ir_recovery|복구]] 후 [[001_dikw_pyramid|데이터]]가 맞는다. 또한 전송 중단 시를 대비한 저널링 (Journaling), [[140_bandwidth|대역폭]] 부족 시 변경분 [[347_compaction|압축]], 분할 뇌 (Split-Brain) 방지를 위한 위트니스 (Witness)도 함께 고려된다.

- **📢 섹션 요약 비유**: 동기식은 두 권의 장부에 동시에 도장을 찍고 둘 다 확인받아야 다음 손님을 받는 방식이고, 비동기식은 먼저 앞 장부에만 기록하고 뒷장부는 점원이 틈날 때 옮겨 적는 방식과 같다.

---

## Ⅲ. 비교 및 연결

스토리지 [[333_raid_1|미러링]]은 [[555_backup_and_restore_strategy|백업]], [[022_snapshot_backup_architecture|스냅샷]], RAID와 자주 혼동되지만 [[571_protection_vs_security|보호]] 목적이 다르다. 이 경계를 정확히 알아야 DRS를 과신하지 않는다.

| 기법 | 주 [[571_protection_vs_security|보호]] 범위 | 강점 | 한계 |
| :-- | :-- | :-- | :-- |
| [[483_raid_overview|RAID]] | 디스크 단위 고장 | 빠른 국소 복원 | 사이트 장애는 막지 못함 |
| [[022_snapshot_backup_architecture|스냅샷]] ([[637_zfs_snapshot_cow_architecture|Snapshot]]) | 시점 복원 | 빠른 [[369_logic_bomb|논리]] [[658_ir_recovery|복구]] | 같은 스토리지 장애에는 취약 |
| [[555_backup_and_restore_strategy|백업]] ([[555_backup_and_restore_strategy|Backup]]) | 장기 보관, 삭제·[[730_ransomware|랜섬웨어]] 대응 | 과거 [[288_version_ihl_tos_total_length|버전]] 보존 | [[658_ir_recovery|복구]] 시간이 길 수 있음 |
| [[333_raid_1|미러링]] (Mirroring) | 센터 장애 시 연속성 | 원격 최신본 확보 | 손상 [[001_dikw_pyramid|데이터]]도 함께 [[016_replication_factor|복제]]될 수 있음 |

즉 [[333_raid_1|미러링]]은 "[[090_service_kubernetes_network_load_balancing|서비스]] 연속성"에 강하고, [[555_backup_and_restore_strategy|백업]]은 "과거로 돌아가기"에 강하다. 예를 들어 운영자가 실수로 테이블을 삭제하면 그 [[369_logic_bomb|논리]]적 손상은 미러를 통해 반대편으로도 전파될 수 있다. 그래서 DRS [[333_raid_1|미러링]]이 있어도 불변 [[555_backup_and_restore_strategy|백업]] ([[298_immutable|Immutable]] [[555_backup_and_restore_strategy|Backup]])이나 시점 [[022_snapshot_backup_architecture|스냅샷]]은 별도로 필요하다.

또한 [[333_raid_1|미러링]] 방식은 RPO와 RTO를 동시에 좌우한다. 동기식은 RPO를 줄이는 데 강하지만, 실제 [[658_ir_recovery|복구]]에 필요한 서버 부팅·애플리케이션 기동·네트워크 절체까지 자동화되어 있지 않으면 RTO는 길 수 있다. 따라서 DRS 설계는 저장장치 [[016_replication_factor|복제]]만 보는 것이 아니라, [[016_replication_factor|복제]]된 [[001_dikw_pyramid|데이터]]를 실제 [[090_service_kubernetes_network_load_balancing|서비스]]로 이어 주는 전체 [[658_ir_recovery|복구]] 체인과 함께 보아야 한다.

- **📢 섹션 요약 비유**: [[333_raid_1|미러링]]은 현재 장면을 다른 카메라로 실시간 중계하는 것이고, [[555_backup_and_restore_strategy|백업]]은 과거 방송을 녹화해 두는 것이다. 중계만 있다고 원하는 장면으로 되돌릴 수 있는 것은 아니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 업무 특성에 따라 [[333_raid_1|미러링]] 방식을 나눈다. 계좌 이체나 증권 주문처럼 한 건의 손실도 민감한 시스템은 [[015_지연_데이터_관점|지연]]을 감수하고 메트로 거리 동기식을 검토한다. 반면 전국 쇼핑몰, 그룹웨어, 분석 시스템처럼 수 ms의 응답성이 중요한 업무는 비동기식이나 주기적 [[022_snapshot_backup_architecture|스냅샷]] [[016_replication_factor|복제]]가 더 현실적일 수 있다.

기술사 관점에서 확인할 질문은 다음과 같다.

1. **[[015_지연_데이터_관점|지연]] 예산이 충분한가?** 동기식이면 왕복 [[015_지연_데이터_관점|지연]]이 애플리케이션 응답시간에 직접 들어온다.
2. **[[140_bandwidth|대역폭]]이 피크 [[289_cqrs_db|쓰기]]량을 감당하는가?** 평시 평균이 아니라 배치·정산 시간대까지 봐야 한다.
3. **[[194_consistency_database_integrity|일관성]] 그룹이 구성되었는가?** [[001_dikw_pyramid|데이터]] [[501_file_definition_logical_record|파일]]과 [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]]이 따로 놀면 [[658_ir_recovery|복구]] 후 DB가 깨질 수 있다.
4. **위트니스와 절체 절차가 있는가?** 링크 단절 시 양쪽 센터가 동시에 주 센터라고 주장하면 더 큰 장애가 된다.
5. **미러 외에 [[555_backup_and_restore_strategy|백업]]이 있는가?** [[730_ransomware|랜섬웨어]]·운영 실수·[[369_logic_bomb|논리]] 손상은 미러만으로 막기 어렵다.

대형 환경에서는 3DC (3 [[801_data_center_3_tier_architecture_core_aggregation_access|Data Center]]) 전략도 자주 쓴다. 가까운 센터에는 동기식으로 무손실을 노리고, 먼 센터에는 비동기식으로 광역 재난까지 대비하는 방식이다. 이 구조는 비용이 크지만, [[282_performance_tactics|성능]]·[[177_rpo_recovery_point_objective|RPO]]·지역 재난 대응을 동시에 만족시키려는 현실적 절충안이다.

- **📢 섹션 요약 비유**: 중요한 계약서는 옆방 복사기 한 장만으로는 부족하다. 바로 옆 서랍에는 원본과 동시에 복사하고, 먼 지점 금고에는 약간 늦더라도 추가 사본을 보내 두는 방식이 더 안전하다.

---

## Ⅴ. 기대효과 및 결론

DRS 스토리지 [[333_raid_1|미러링]]을 잘 설계하면 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 전체 장애를 곧바로 [[090_service_kubernetes_network_load_balancing|서비스]] 종료로 받아들이지 않아도 된다. 원격 센터에 최신 [[001_dikw_pyramid|데이터]] 기반이 남아 있으므로, 절체 자동화와 운영 훈련이 갖춰져 있다면 다운타임과 [[001_dikw_pyramid|데이터]] 손실을 크게 줄일 수 있다. 특히 금융·공공·의료처럼 [[090_service_kubernetes_network_load_balancing|서비스]] 연속성이 규제나 신뢰와 직결되는 분야에서 효과가 크다.

다만 [[333_raid_1|미러링]]은 공짜 안전장치가 아니다. 전용 회선 비용, 스토리지 컨트롤러 기능, [[015_지연_데이터_관점|지연]] 증가, 운영 복잡도, 정기적인 [[360_ospf_dr_bdr_designated_router_lsa_flooding|DR]] 훈련이 함께 따라온다. 또한 애플리케이션이 다중 센터 [[289_cqrs_db|쓰기]] 순서를 감당하지 못하면 하드웨어 [[333_raid_1|미러링]]만으로는 [[194_consistency_database_integrity|일관성]]을 완벽히 보장하지 못한다.

앞으로는 연속 [[001_dikw_pyramid|데이터]] [[571_protection_vs_security|보호]] ([[193_crl_distribution_point_cdp|CDP]], Continuous [[001_dikw_pyramid|Data]] [[571_protection_vs_security|Protection]]), 스토리지 [[015_virtualization|가상화]], 클라우드 블록 [[016_replication_factor|복제]], [[136_variance|분산]] [[002_database_definition|데이터베이스]] 합의 프로토콜이 [[333_raid_1|미러링]]을 더 소프트웨어 정의 방식으로 바꾸고 있다. 그래도 핵심 기억법은 같다. **DRS [[333_raid_1|미러링]]은 [[001_dikw_pyramid|데이터]]를 복사하는 기능이 아니라, 원격지에서 어떤 시점의 [[289_cqrs_db|쓰기]]를 완료로 인정할지 정하는 아키텍처 선택**이다.

- **📢 섹션 요약 비유**: [[333_raid_1|미러링]]은 거울 하나 더 놓는 일이 아니라, 멀리 떨어진 곳에서도 같은 장부를 믿고 영업을 계속할 수 있게 만드는 원격 분신술과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [[483_raid_overview|RAID]] (Redundant [[055_array|Array]] of Independent Disks) | 로컬 디스크 장애를 막지만 센터 장애까지는 [[571_protection_vs_security|보호]]하지 못한다 |
| 동기식 [[016_replication_factor|복제]] ([[010_동기식_비동기식_전송|Synchronous]] [[016_replication_factor|Replication]]) | 원격 반영 후 ACK를 주어 낮은 RPO를 만든다 |
| 비동기식 [[016_replication_factor|복제]] (Asynchronous [[016_replication_factor|Replication]]) | [[015_지연_데이터_관점|지연]]과 거리 부담을 줄이는 대신 [[001_dikw_pyramid|데이터]] 손실 창을 남긴다 |
| 위트니스 (Witness) | 분할 뇌 상황에서 어느 쪽이 주 센터인지 판단을 돕는다 |
| 목표 [[658_ir_recovery|복구]] 시점 ([[177_rpo_recovery_point_objective|RPO]], [[177_rpo_recovery_point_objective|Recovery Point Objective]]) | [[333_raid_1|미러링]] 방식 선택의 핵심 기준이 된다 |

### 📈 관련 키워드 및 발전 흐름도

```text
로컬 디스크 이중화 (RAID)
    │
    ▼
원격 스냅샷 · 비동기 복제
    │
    ▼
메트로 구간 동기 미러링
    │
    ▼
3DC 하이브리드 DR 구조
    │
    ▼
CDP · 합의 기반 분산 저장 구조
```

이 흐름은 저장장치 [[571_protection_vs_security|보호]]가 "디스크 고장 대응"에서 "센터 장애 이후 [[090_service_kubernetes_network_load_balancing|서비스]] 지속"으로 확장되는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 중요한 공책을 한 권만 갖고 있으면, 집이 망가졌을 때 내용을 다 잃을 수 있어요.
2. 그래서 다른 동네에도 같은 내용을 계속 적어 두면, 원래 공책이 없어져도 다시 시작할 수 있어요.
3. 다만 멀리 있는 공책까지 바로 적으려면 느려지고, 나중에 적으면 조금 잃을 수도 있답니다.
