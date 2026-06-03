---
title: 53. 가상화 아키텍처 (Virtualization Architecture)
date: '2026-05-01'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[015_virtualization|가상화]] 아키텍처는 물리 자원을 [[198_abstraction_control_data_process|추상화]]해 여러 독립 실행 환경을 만드는 구조다.
> 2. **가치**: Type 1/Type 2 [[054_hypervisor|하이퍼바이저]], CPU/MEM/IO [[015_virtualization|가상화]], 스냅샷과 라이브 마이그레이션이 핵심이다.
> 3. **판단 포인트**: 격리, [[282_performance_tactics|성능]], 운영 편의성은 항상 trade-off (상충관계)이며, [[561_container_based_deployment|컨테이너]]와 구분해서 설명해야 한다.

---

## Ⅰ. 개요 및 필요성

[[015_virtualization|가상화]]는 하나의 물리 서버를 여러 [[369_logic_bomb|논리]] 서버처럼 사용하게 해 준다. 서버 자원이 비싸고 활용률이 낮던 시절, [[015_virtualization|가상화]]는 자원 효율과 운영 유연성을 크게 높였다.

현재는 클라우드와 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]] 운영의 기본이 되었고, 장애 격리와 테스트 환경 구성에도 중요하다.

- **📢 섹션 요약 비유**: [[015_virtualization|가상화]] 아키텍처는 한 건물 안에 여러 개의 독립된 집을 만드는 일과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

[[015_virtualization|가상화]]의 중심은 [[054_hypervisor|하이퍼바이저]]다. [[054_hypervisor|하이퍼바이저]]가 물리 하드웨어 위에서 [[598_vm_migration_nic|VM]] ([[598_vm_migration_nic|Virtual Machine]])을 관리하고, 각 VM은 자신의 OS를 가진다.

```text
┌──────────────────────────────────────────────┐
│ Apps ─ Guest OS ─ Virtual Hardware ── VM     │
├──────────────────────────────────────────────┤
│            Hypervisor (Type 1/2)             │
├──────────────────────────────────────────────┤
│          Physical CPU / Memory / Storage     │
└──────────────────────────────────────────────┘
```

| 요소 | 역할 | 포인트 |
| :--- | :--- | :--- |
| [[054_hypervisor|하이퍼바이저]] | 자원 분배 | [[598_vm_migration_nic|VM]] 실행/제어 |
| vCPU/vMEM | 가상 자원 | 스케줄링 대상 |
| vNIC/vDisk | 가상 I/O | 네트워크/스토리지 [[198_abstraction_control_data_process|추상화]] |
| [[637_zfs_snapshot_cow_architecture|Snapshot]] | 상태 저장 | [[658_ir_recovery|복구]]/실험 |
| [[629_live_migration_pre_copy|Live Migration]] | 무중단 이동 | HA/유지보수 |

핵심은 "물리와 [[369_logic_bomb|논리]]를 분리"하는 것이다. 이 분리 덕분에 격리와 이식성이 생긴다.

- **📢 섹션 요약 비유**: [[015_virtualization|가상화]] 아키텍처는 같은 바닥에 가벽을 세워 서로 다른 방을 만드는 구조다.

---

## Ⅲ. 비교 및 연결

[[015_virtualization|가상화]]는 [[561_container_based_deployment|컨테이너]]와 자주 비교된다. VM은 OS까지 포함해 강한 격리를 제공하고, [[561_container_based_deployment|컨테이너]]는 OS 커널을 공유해 가볍고 빠르다.

| 항목 | [[598_vm_migration_nic|VM]] | [[561_container_based_deployment|컨테이너]] |
| :--- | :--- | :--- |
| 격리 수준 | 높음 | 중간 |
| 부팅 속도 | 느림 | 빠름 |
| OS 중복 | 있음 | 없음 |
| 사용 사례 | 멀티테넌시, 레거시 | [[532_microservices_decomposition_patterns|마이크로서비스]], [[090_configuration_item|CI]]/CD |

Type 1 [[054_hypervisor|하이퍼바이저]]는 하드웨어 위에서 직접 동작해 [[282_performance_tactics|성능]]과 안정성이 좋고, Type 2는 호스트 OS 위에서 실행되어 편하지만 오버헤드가 있다.

- **📢 섹션 요약 비유**: VM은 아파트 한 세대, [[561_container_based_deployment|컨테이너]]는 같은 집 안의 독립 방과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 CPU 오버커밋, 메모리 [[632_memory_ballooning_hypervisor|ballooning]], 스토리지 IOPS, 네트워크 [[015_virtualization|가상화]], HA cluster 구성을 함께 본다. 격리와 [[282_performance_tactics|성능]] 균형을 맞춰야 한다.

### [[435_checklist_based_testing|체크리스트]]

1. Type 1 또는 Type 2 선택이 목적에 맞는가?
2. 자원 오버커밋 비율이 통제되는가?
3. 스냅샷과 [[555_backup_and_restore_strategy|백업]] 정책이 구분되어 있는가?
4. 라이브 마이그레이션과 장애 [[658_ir_recovery|복구]]가 가능한가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 테스트와 운영 VM을 무분별하게 섞는 경우
- 스토리지/네트워크 병목을 무시하는 경우
- [[561_container_based_deployment|컨테이너]]와 VM의 역할을 혼동하는 경우

기술사 관점에서는 [[015_virtualization|가상화]]가 단순 서버 분할이 아니라, 자원 격리와 운영 [[198_abstraction_control_data_process|추상화]]를 통해 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]를 운영하는 핵심 기술이라는 점을 설명해야 한다.

- **📢 섹션 요약 비유**: [[015_virtualization|가상화]] 아키텍처는 여러 명이 한 냄비를 쓰되, 각자 자기 그릇을 따로 갖는 식당과 같다.

---

## Ⅴ. 기대효과 및 결론

[[015_virtualization|가상화]] 아키텍처는 서버 활용률을 높이고, 운영 유연성과 장애 대응력을 키운다. 클라우드 인프라와 프라이빗 [[801_data_center_3_tier_architecture_core_aggregation_access|데이터센터]]의 바탕이 되는 이유다.

결국 [[015_virtualization|가상화]]는 "하드웨어를 [[369_logic_bomb|논리]]적으로 쪼개 운영을 쉽게 만드는 기술"로 요약된다.

- **📢 섹션 요약 비유**: [[015_virtualization|가상화]]는 하나의 큰 상자를 여러 작은 서랍으로 나누는 정리법이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[054_hypervisor|하이퍼바이저]] | [[598_vm_migration_nic|VM]] 제어 |
| Type 1/2 | 배치 구조 |
| [[637_zfs_snapshot_cow_architecture|Snapshot]] | 상태 저장 |
| [[629_live_migration_pre_copy|Live Migration]] | 무중단 이동 |
| [[194_container_virtualization_docker_namespace|Container]] | 경량 대안 |

### 📈 관련 키워드 및 발전 흐름도

```text
물리 서버
    │
    ▼
하이퍼바이저
    │
    ▼
가상 머신 (VM)
    │
    ▼
클라우드 / 멀티테넌시
```

이 흐름은 물리 자원 직접 운영에서 [[369_logic_bomb|논리]]적 분리 운영으로 발전한 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[015_virtualization|가상화]]는 큰 집을 여러 작은 집처럼 나눠 쓰는 거예요.
2. 그래서 한 집이 고장 나도 다른 집은 덜 흔들려요.
3. 필요하면 집을 통째로 옮기는 것처럼 옮길 수도 있어요.
