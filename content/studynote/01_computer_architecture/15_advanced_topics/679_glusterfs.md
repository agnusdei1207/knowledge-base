---
title: 679. GlusterFS 분산 스토리지
date: '2026-05-08'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: GlusterFS는 여러 서버의 [[506_directory_structure_symbol_table|디렉터리]]를 브릭 (Brick)으로 묶어, 하나의 큰 [[501_file_definition_logical_record|파일]] 볼륨처럼 보이게 만드는 스케일아웃 [[501_file_definition_logical_record|파일]] 시스템이다.
> 2. **가치**: 범용 리눅스 서버와 디스크만으로도 공유 [[501_file_definition_logical_record|파일]] 저장 공간을 단계적으로 늘릴 수 있어, 대용량 미디어·[[555_backup_and_restore_strategy|백업]]·아카이브용 [[136_variance|분산]] [[492_nas_network_attached_storage|NAS]] ([[492_nas_network_attached_storage|Network Attached Storage]]) 대체재로 매력적이다.
> 3. **판단 포인트**: 구조가 단순하고 확장하기 쉽지만, 작은 [[501_file_definition_logical_record|파일]]이 매우 많거나 분할 뇌 문제와 [[012_metadata|메타데이터]] 충돌에 민감한 업무에는 신중해야 한다.

---

## Ⅰ. 개요 및 필요성

GlusterFS는 “용량이 꽉 차면 [[501_file_definition_logical_record|파일]] 서버를 또 하나 만든다”는 기존 [[492_nas_network_attached_storage|NAS]] 확장 방식의 불편을 줄이기 위해 등장했다. 기존 방식에서는 저장 장치를 추가할 때마다 새로운 공유 경로가 생기고, 사용자는 어느 서버에 어떤 [[501_file_definition_logical_record|파일]]이 있는지 따로 기억해야 한다. 규모가 커질수록 운영자는 경로와 권한을 늘 관리해야 하고, 사용자는 저장소가 여러 조각으로 흩어진 느낌을 받는다.

GlusterFS는 이 문제를 서버를 더 큰 중앙 장비로 바꾸지 않고, 여러 서버의 [[506_directory_structure_symbol_table|디렉터리]]를 하나의 [[369_logic_bomb|논리]] 볼륨으로 묶는 방식으로 해결한다. 즉, 사용자는 하나의 공유 공간만 보지만, 실제 [[501_file_definition_logical_record|파일]]은 여러 서버에 [[136_variance|분산]]되거나 [[016_replication_factor|복제]]된다. 그래서 GlusterFS는 “저장장치 교체”보다 “[[501_file_definition_logical_record|파일]] 공간의 수평 확장”에 초점을 둔 기술이다.

- **📢 섹션 요약 비유**: GlusterFS는 방마다 작은 옷장을 따로 두는 대신, 여러 방의 옷장을 하나의 거대한 드레스룸처럼 보이게 연결해 주는 구조와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

GlusterFS의 기본 단위는 브릭이다. 브릭은 보통 한 서버의 [[506_directory_structure_symbol_table|디렉터리]] 하나를 의미하며, 여러 브릭이 모여 볼륨을 이룬다. 클라이언트는 [[554_fuse_filesystem_in_userspace|FUSE]] ([[554_fuse_filesystem_in_userspace|Filesystem in Userspace]]) 기반 [[516_mount_mechanism|마운트]]나 네이티브 클라이언트를 통해 이 볼륨을 접속하고, 내부 번역기 계층이 [[501_file_definition_logical_record|파일]] 이름과 규칙에 따라 어느 브릭에 읽기·[[289_cqrs_db|쓰기]]를 수행할지 결정한다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| 브릭 (Brick) | 실제 [[501_file_definition_logical_record|파일]]이 놓이는 기본 저장 [[506_directory_structure_symbol_table|디렉터리]] | 서버·디스크 단위 확장의 기본 블록 |
| 볼륨 ([[001_bigdata_3v_5v|Volume]]) | 여러 브릭을 묶은 [[369_logic_bomb|논리]] 저장소 | 사용자에게는 하나의 [[501_file_definition_logical_record|파일]] 공간으로 보임 |
| 번역기 (Translator) | [[136_variance|분산]], [[016_replication_factor|복제]], [[136_variance|분산]]-[[016_replication_factor|복제]], [[136_variance|분산]]-삭제 코딩 규칙 수행 | 성능과 [[452_availability|가용성]] 정책을 결정 |
| 클라이언트 [[516_mount_mechanism|마운트]] | [[501_file_definition_logical_record|파일]] 시스템 인터페이스 제공 | 응용 프로그램 [[344_compatibility_usability|호환성]] 확보 |
| Self-heal | 장애 후 [[016_replication_factor|복제]]본을 다시 맞춤 | 네트워크 분리 시 충돌 관리 중요 |

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ Client mount                                                            │
│   │                                                                     │
│   ▼                                                                     │
│ Gluster translator stack                                                │
│   │                                                                     │
│   ├─ distribute -> Brick A                                              │
│   ├─ replicate  -> Brick B                                              │
│   └─ disperse   -> Brick C / Brick D / Brick E                          │
└──────────────────────────────────────────────────────────────────────────┘
```

GlusterFS에서 중요한 볼륨 유형은 세 가지다. [[136_variance|분산]] 볼륨은 [[501_file_definition_logical_record|파일]]을 여러 브릭에 나눠 배치해 용량을 늘리고, [[016_replication_factor|복제]] 볼륨은 같은 [[501_file_definition_logical_record|파일]]을 여러 브릭에 저장해 [[452_availability|가용성]]을 높이며, [[136_variance|분산]]-[[016_replication_factor|복제]] 또는 [[136_variance|분산]]-삭제 코딩 (Dispersed) 볼륨은 두 요구를 함께 만족시키려는 절충안이다. 따라서 GlusterFS는 “무조건 빠른 [[501_file_definition_logical_record|파일]] 시스템”보다 “[[501_file_definition_logical_record|파일]] 공유의 용량·[[452_availability|가용성]] 조합을 유연하게 선택하는 플랫폼”으로 보는 편이 맞다.

- **📢 섹션 요약 비유**: GlusterFS는 여러 창고를 하나의 매장 뒤편 창고처럼 묶고, 물건 성격에 따라 어떤 창고에는 나눠 놓고 어떤 창고에는 복사본까지 만들어 두는 운영 규칙과 같다.

---

## Ⅲ. 비교 및 연결

GlusterFS는 [[136_variance|분산]] 저장 기술이지만 Ceph나 [[013_hdfs|HDFS]] ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[553_distributed_file_system|Distributed File System]])와 지향점이 다르다. Ceph가 객체 기반 통합 저장 플랫폼이라면, GlusterFS는 [[501_file_definition_logical_record|파일]] 공유를 빠르게 확장하는 데 집중한다. HDFS는 대용량 배치 분석을 위해 설계된 [[501_file_definition_logical_record|파일]] 시스템이라 일반적인 공유 폴더 의미론과는 거리가 있다.

| 구분 | GlusterFS | Ceph | [[013_hdfs|HDFS]] ([[843_hadoop_rack_awareness_data_replication_topology|Hadoop]] [[553_distributed_file_system|Distributed File System]]) |
| :--- | :--- | :--- | :--- |
| 중심 인터페이스 | [[501_file_definition_logical_record|파일]] 공유 | 객체·블록·[[501_file_definition_logical_record|파일]] 통합 | 분석용 대용량 [[501_file_definition_logical_record|파일]] |
| 구조 복잡도 | 비교적 단순 | 높음 | 중간 |
| 강점 | 손쉬운 공유 스토리지 확장 | 범용 통합 저장 플랫폼 | [[019_data_locality|데이터 지역성]] 기반 분석 처리 |
| 약점 | 작은 [[501_file_definition_logical_record|파일]]·충돌 관리에 민감 | 운영 난이도 높음 | 일반 POSIX (Portable [[001_operating_system_purpose|Operating System]] Interface) 공유에 부적합 |
| 잘 맞는 업무 | 미디어, [[555_backup_and_restore_strategy|백업]], 일반 [[501_file_definition_logical_record|파일]] 공유 | [[008_private_cloud|프라이빗 클라우드]], 통합 스토리지 | 배치 분석, [[568_logs_distributed_logging_elk_fluentd|로그]] 저장 |

이 비교는 GlusterFS의 위치를 분명하게 해 준다. GlusterFS는 “[[501_file_definition_logical_record|파일]] 시스템을 거의 그대로 쓰고 싶은 조직”에게 유리하고, Ceph는 여러 저장 유형을 한 번에 통합하고 싶은 조직에게 유리하다. 따라서 GlusterFS를 선택할 때는 기술적 최고 성능보다, 운영 단순성과 [[501_file_definition_logical_record|파일]] 공유 친화성이 더 중요한 판단 기준이 된다.

- **📢 섹션 요약 비유**: GlusterFS가 여러 창고를 연결한 대형 서고라면, Ceph는 창고·금고·택배센터가 합쳐진 복합 물류도시이고, HDFS는 공장 원자재 창고에 가깝다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **미디어 원본 저장소**
   - 큰 영상 [[501_file_definition_logical_record|파일]]과 이미지 [[501_file_definition_logical_record|파일]]을 여러 팀이 공유해야 할 때 적합하다.
   - [[501_file_definition_logical_record|파일]] 크기가 크고 순차 읽기가 많을수록 GlusterFS의 장점이 잘 드러난다.

2. **[[555_backup_and_restore_strategy|백업]] 저장소**
   - 여러 서버의 [[555_backup_and_restore_strategy|백업]] [[001_dikw_pyramid|데이터]]를 하나의 큰 볼륨으로 수집하기 쉽다.
   - [[016_replication_factor|복제]] 또는 [[136_variance|분산]]-삭제 코딩 구성으로 용량과 안전성의 균형을 잡을 수 있다.

3. **지사·엣지 환경 공유 스토리지**
   - 고가 어플라이언스 없이 일반 서버만으로 공유 [[501_file_definition_logical_record|파일]] 공간을 만들 수 있다.
   - 중앙 장비 도입이 부담스러운 환경에서 단계적 확장이 가능하다.

### 채택/회피 판단 체크포인트

- **채택이 유리한 경우**
  - 큰 [[501_file_definition_logical_record|파일]] 중심의 공유 저장소가 필요할 때
  - 범용 리눅스 서버를 활용해 손쉽게 확장하고 싶을 때
  - 전통 [[501_file_definition_logical_record|파일]] 시스템 사용 경험을 유지하면서 용량을 늘리고 싶을 때

- **회피가 유리한 경우**
  - 작은 [[501_file_definition_logical_record|파일]]이 매우 많고 [[012_metadata|메타데이터]] 연산이 집중될 때
  - [[001_dikw_pyramid|데이터]]베이스나 가상머신 ([[598_vm_migration_nic|Virtual Machine]]) 부팅 디스크처럼 [[015_지연_데이터_관점|지연]] 시간에 민감한 랜덤 [[289_cqrs_db|쓰기]] 업무일 때
  - 네트워크 분리 가능성이 높고, [[016_replication_factor|복제]] 볼륨 충돌 관리 체계를 마련하기 어려울 때

실무에서 가장 주의할 부분은 분할 뇌 문제다. [[016_replication_factor|복제]] 볼륨이 네트워크 단절을 겪으면 서로 다른 브릭에서 각각 “내가 최신”이라고 주장하는 상황이 생길 수 있다. 그래서 쿼럼, 아비터 브릭, 운영 절차를 함께 설계해야 하며, 노드 추가 후 재균형 시간과 자기 치유 시간을 [[090_service_kubernetes_network_load_balancing|서비스]] 허용 범위 안에 넣어야 한다. GlusterFS는 단순해 보이지만, “[[501_file_definition_logical_record|파일]] 공유는 단순하고 [[658_ir_recovery|복구]]는 자동”이라고 과신하면 안 된다.

- **📢 섹션 요약 비유**: GlusterFS 운영은 여러 점원이 같은 재고 장부를 공유하는 상점과 같다. 평소에는 편하지만, 통신이 끊긴 상태에서 각자 따로 적기 시작하면 나중에 장부를 맞추는 일이 가장 어렵다.

---

## Ⅴ. 기대효과 및 결론

GlusterFS의 장점은 명확하다. 범용 서버를 붙여 용량을 키우기 쉽고, 사용자에게는 하나의 큰 [[501_file_definition_logical_record|파일]] 공간처럼 보이며, 대형 미디어 [[501_file_definition_logical_record|파일]]·[[555_backup_and_restore_strategy|백업]] [[501_file_definition_logical_record|파일]]·일반 협업 자료를 비교적 친숙한 방식으로 저장할 수 있다. 즉, 전통적 [[501_file_definition_logical_record|파일]] 공유 환경을 크게 깨지 않으면서 수평 확장을 실현하는 데 좋은 도구다.

반면 모든 [[136_variance|분산]] 저장 문제가 GlusterFS로 풀리지는 않는다. [[012_metadata|메타데이터]]가 매우 많거나, 낮은 [[015_지연_데이터_관점|지연]]의 랜덤 입출력이 필요하거나, 블록·객체 저장까지 함께 통합해야 하면 다른 기술이 더 낫다. 따라서 GlusterFS는 **“가장 범용적인 [[136_variance|분산]] 저장소”가 아니라 “[[501_file_definition_logical_record|파일]] 공유 중심의 단순한 스케일아웃 스토리지”**로 기억해야 한다.

- **📢 섹션 요약 비유**: GlusterFS는 고급 만능 멀티툴보다, 큰 [[501_file_definition_logical_record|파일]]을 나눠 보관하기에 딱 좋은 튼튼한 공구함에 가깝다. 할 일에 맞으면 매우 편하지만, 모든 일을 한 번에 해결해 주지는 않는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 브릭 (Brick) | GlusterFS의 물리적 저장 기본 단위다. |
| 볼륨 ([[001_bigdata_3v_5v|Volume]]) | 여러 브릭을 하나의 [[369_logic_bomb|논리]] [[501_file_definition_logical_record|파일]] 공간으로 묶는다. |
| 번역기 (Translator) | [[136_variance|분산]], [[016_replication_factor|복제]], [[136_variance|분산]]-삭제 코딩 정책을 실제 [[501_file_definition_logical_record|파일]] 경로에 적용한다. |
| Self-heal | [[016_replication_factor|복제]]본 간 불일치를 장애 후 다시 맞추는 [[658_ir_recovery|복구]] 메커니즘이다. |
| Split-brain | 네트워크 분리 후 어느 [[016_replication_factor|복제]]본이 최신인지 결정하기 어려운 충돌 상태다. |
| Arbiter | 전체 [[016_replication_factor|복제]] 비용을 줄이면서 충돌 판정을 돕는 보조 브릭 구성 방식이다. |

### 📈 관련 키워드 및 발전 흐름도

```text
단일 NAS (Network Attached Storage) 확장 한계
        │
        ▼
브릭 기반 스케일아웃 파일 공유
        │
        ▼
GlusterFS 분산 / 복제 볼륨
        │
        ▼
분산-복제 / 분산-삭제 코딩 기반 고가용성 파일 저장
        │
        ▼
온프레미스 / 엣지 환경의 단순한 공유 스토리지 확장
```

이 흐름은 [[501_file_definition_logical_record|파일]] 공유 스토리지가 더 큰 단일 장비를 사는 방향보다, 여러 노드를 [[369_logic_bomb|논리]]적으로 묶는 방향으로 발전했음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. GlusterFS는 친구들 방에 있는 여러 장난감 상자를 한 큰 상자처럼 보이게 묶어 주는 거예요.
2. 그래서 새 상자를 하나 더 놓으면 장난감을 더 많이 넣을 수 있어요.
3. 하지만 친구들이 서로 말을 안 하고 따로 정리하면, 나중에 어느 상자가 맞는지 다시 맞춰야 해요.
