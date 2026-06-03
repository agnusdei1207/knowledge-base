---
title: 736. 하드 링크 / 심볼릭 링크 차이 (Hard Link Vs Symbolic Link)
date: '2026-05-09'
tags:
- studynote-operating-system
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 리눅스 [[501_file_definition_logical_record|파일]] 시스템에서 [[501_file_definition_logical_record|파일]]은 '이름표([[506_directory_structure_symbol_table|디렉터리]] 엔트리)'와 '실제 [[001_dikw_pyramid|데이터]](i-node)'로 분리되어 있다. 링크(Link)는 하나의 [[001_dikw_pyramid|데이터]]에 접근하기 위한 **새로운 이름표를 다는 기술**이다.
> 2. **[[511_hard_link|하드 링크]] ([[511_hard_link|Hard Link]])**: 원본 [[501_file_definition_logical_record|파일]]과 **완벽히 동일한 i-node 번호**를 가리키는 또 다른 이름표다. 원본을 지워도 [[511_hard_link|하드 링크]]가 남아있으면 [[001_dikw_pyramid|데이터]]는 절대 지워지지 않으며, [[501_file_definition_logical_record|파일]] 시스템이 다르면([[514_partition_slice_volume|파티션]]이 다르면) i-node 체계가 달라 [[087_process_state_transition|생성]]할 수 없다.
> 3. **[[512_symbolic_link|심볼릭 링크]] ([[512_symbolic_link|Symbolic Link]] / Soft Link)**: 원본 [[501_file_definition_logical_record|파일]]의 **'경로(Path) 텍스트'만을 저장한 껍데기 [[501_file_definition_logical_record|파일]]**이다. 원본 [[501_file_definition_logical_record|파일]]이 삭제되거나 이름이 바뀌면 허공을 맴도는 고아(Broken Link)가 되지만, [[501_file_definition_logical_record|파일]] 시스템이나 운영체제의 경계를 자유롭게 넘나들 수 있는 유연성을 갖는다. (Windows의 바로 가기와 동일)

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - **[[511_hard_link|하드 링크]] ([[511_hard_link|Hard Link]])**: 기존 [[501_file_definition_logical_record|파일]]의 i-node를 직접 가리키는 새로운 [[506_directory_structure_symbol_table|디렉터리]] 엔트리를 [[087_process_state_transition|생성]]하는 것.
  - **[[512_symbolic_link|심볼릭 링크]] (Soft Link)**: 기존 [[501_file_definition_logical_record|파일]]의 '경로 문자열'을 [[001_dikw_pyramid|데이터]]로 갖고 있는 완전히 새로운 i-node([[501_file_definition_logical_record|파일]])를 [[087_process_state_transition|생성]]하는 것.

- **필요성 ([[501_file_definition_logical_record|파일]] 공유와 중복 저장 방지)**: 
  - 10GB짜리 거대한 [[568_logs_distributed_logging_elk_fluentd|로그]] [[501_file_definition_logical_record|파일]]을 `/var/log` 폴더에도 두고 싶고, 내 홈 [[506_directory_structure_symbol_table|디렉터리]](`/home/user`)에서도 열어보고 싶다.
  - 이 [[501_file_definition_logical_record|파일]]을 `cp` [[158_instruction|명령어]]로 복사하면 디스크 용량이 20GB로 늘어나는 끔찍한 낭비가 발생하고, 원본이 수정될 때 내 복사본은 수정되지 않는 [[212_synchronization_mechanisms|동기화]] 문제가 터진다.
  - **해결책**: [[501_file_definition_logical_record|파일]]을 복사하지 말고, **"같은 [[001_dikw_pyramid|데이터]]를 가리키는 문(Link)"**만 여러 개 만들자! 

  - **원본 [[501_file_definition_logical_record|파일]]**: 서울 강남구 테헤란로 1번지 건물 (실제 [[001_dikw_pyramid|데이터]], i-node).
  - **[[511_hard_link|하드 링크]]**: 그 건물에 달린 '정문'과 '후문'. 정문을 부순다고(원본 삭제) 건물이 무너지지 않는다. 후문으로 들어가면 똑같은 건물이 나온다. (건물 자체를 부수려면 정문과 후문을 다 헐어야 함). 단, 강남구 건물의 문을 부산에 달 수는 없다 ([[514_partition_slice_volume|파티션]] 간 [[087_process_state_transition|생성]] 불가).
  - **[[512_symbolic_link|심볼릭 링크]]**: 부산에 있는 내 책상에 놓인 포스트잇. 포스트잇에는 "강남구 테헤란로 1번지로 가시오"라고 적혀 있다. 강남구 건물이 헐리면(원본 삭제), 포스트잇을 보고 찾아가도 텅 빈 공터만 나온다 (Broken Link). 하지만 미국, 일본 어디에든 이 포스트잇은 둘 수 있다.

- **발전 과정**:
  1. **[[459_quic_fec_forward_error_correction|초기]] Unix**: 디스크 용량을 아끼기 위해 [[501_file_definition_logical_record|파일]] 시스템 내부에서만 동작하는 [[511_hard_link|하드 링크]] 위주 사용.
  2. **네트워크 시대**: 서로 다른 디스크 [[514_partition_slice_volume|파티션]]과 네트워크 드라이브가 엮이면서, 이를 유연하게 넘나들 수 있는 [[512_symbolic_link|심볼릭 링크]]가 현대 OS의 표준 링킹 기법으로 대중화됨.

- **📢 섹션 요약 비유**: [[511_hard_link|하드 링크]]는 내 본명(김철수)과 별명(철렁이)입니다. 이름만 다를 뿐 100% 동일한 나 자신입니다. [[512_symbolic_link|심볼릭 링크]]는 내 집 주소가 적힌 '명함'입니다. 명함을 찢는다고 내가 죽진 않지만, 내가 이사 가면 명함을 보고 찾아온 사람은 날 만날 수 없습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 리눅스 i-node 아키텍처와 Link의 [[083_relationship_in_er_model|관계]]

리눅스의 [[501_file_definition_logical_record|파일]]은 `[디렉터리 (파일 이름)] ──가리킴──▶ [i-node (메타데이터)] ──가리킴──▶ [Data Blocks]` 의 3단 구조를 가진다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 하드 링크 vs 심볼릭 링크 내부 구조 비교                 │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │  [ 원본 파일 A 생성 (`echo "hello" > A`) ]                          │
  │   - 디렉터리: 이름 `A` ──▶ [ i-node 100번 (Link Count: 1) ]         │
  │                                └──▶ Data Block ("hello")          │
  │                                                                   │
  │  [ 하드 링크 B 생성 (`ln A B`) ]                                    │
  │   - 디렉터리: 이름 `B` ──▶ [ i-node 100번 (Link Count: 2) ] ◀──     │
  │   ★ 새로운 i-node를 만들지 않음! 기존 i-node의 래퍼런스 카운트만 +1 올림!  │
  │                                                                   │
  │  [ 심볼릭 링크 C 생성 (`ln -s A C`) ]                               │
  │   - 디렉터리: 이름 `C` ──▶ [ i-node 200번 (Link Count: 1) ]         │
  │                                └──▶ Data Block (텍스트 "A" 라는 경로) │
  │   ★ 완전히 새로운 i-node를 생성함! 원본의 카운트(Link Count)는 오르지 않음!│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설 (삭제 시나리오)]**
만약 사용자가 `rm A`를 치면 무슨 일이 일어날까?
- **[[511_hard_link|하드 링크]] 측면**: `A`라는 이름표가 떨어져 나간다. i-node 100번의 Link Count가 `2 -> 1`로 줄어든다. 카운트가 0이 아니므로 OS는 [[001_dikw_pyramid|데이터]]를 안 지운다! `B`를 열면 여전히 "hello"가 정상적으로 나온다.
- **[[512_symbolic_link|심볼릭 링크]] 측면**: `A`가 사라졌지만 `C`는 여전히 "A로 가라"는 텍스트를 들고 있다. 사용자가 `C`를 여는 순간 OS는 "A를 찾을 수 없음(No such [[501_file_definition_logical_record|file]] or [[506_directory_structure_symbol_table|directory]])" 에러를 뱉는다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### [[511_hard_link|하드 링크]] vs [[512_symbolic_link|심볼릭 링크]] 심층 비교

| 비교 항목 | [[511_hard_link|하드 링크]] ([[511_hard_link|Hard Link]]) | [[512_symbolic_link|심볼릭 링크]] (Symbolic/Soft Link) |
|:---|:---|:---|
| **i-node 번호** | **원본과 동일 (i-node 공유)** | **원본과 다름 (새로운 i-node)** |
| **[[501_file_definition_logical_record|파일]] 크기** | 0바이트 (이름표만 추가되므로 용량 0) | 경로 문자열의 길이만큼 (예: 수 [[074_byte|바이트]]) |
| **원본 삭제 시** | 링크는 멀쩡함. [[001_dikw_pyramid|데이터]] 100% 보존. | 링크는 깨짐 (Broken/Dangling Link). |
| **[[506_directory_structure_symbol_table|디렉터리]] 링킹** | **운영체제가 강제로 금지함 (순환 고리 위험)**| [[506_directory_structure_symbol_table|디렉터리]], [[501_file_definition_logical_record|파일]] 상관없이 마음껏 가능 |
| **[[514_partition_slice_volume|파티션]] 횡단** | **불가능 (다른 [[514_partition_slice_volume|파티션]]은 i-node 테이블이 다름)**| **가능 (네트워크 [[516_mount_mechanism|마운트]], 외장 하드 다 됨)** |

### [[506_directory_structure_symbol_table|디렉터리]](폴더) [[511_hard_link|하드 링크]]를 금지하는 이유

리눅스에서 `ln dir1 dir2` [[158_instruction|명령어]]를 치면 "[[511_hard_link|hard link]] not allowed for [[506_directory_structure_symbol_table|directory]]" 에러가 뜬다. 왜 폴더는 [[511_hard_link|하드 링크]]를 못 만들게 할까?
- [[506_directory_structure_symbol_table|디렉터리]]에 [[511_hard_link|하드 링크]]를 허용하면, 상위 폴더가 하위 폴더의 자식이 되고, 하위 폴더가 다시 상위 폴더를 가리키는 **무한 순환 트리 (Infinite Loop Cycle)**가 발생할 위험이 크기 때문이다.
- 이렇게 되면 [[555_backup_and_restore_strategy|백업]] 프로그램이나 `find` [[158_instruction|명령어]] 같은 [[501_file_definition_logical_record|파일]] 시스템 순회 프로그램들이 무한 루프에 빠져 영원히 폴더를 빠져나오지 못하고 시스템 메모리를 터뜨린다.
- *예외*: 리눅스의 모든 폴더에 있는 `.`(현재 폴더)와 `..`(부모 폴더)만이 유일하게 OS 커널이 예외적으로 직접 만들어주는 '안전한 [[506_directory_structure_symbol_table|디렉터리]] [[511_hard_link|하드 링크]]'다.

- **📢 섹션 요약 비유**: [[511_hard_link|하드 링크]]는 피가 섞인 '친자식'이라서 호적([[514_partition_slice_volume|파티션]])을 함부로 옮길 수 없고 촌수([[506_directory_structure_symbol_table|디렉터리]] 순환)를 꼬이게 해선 안 됩니다. [[512_symbolic_link|심볼릭 링크]]는 '입양아'나 '친구'라서 호적과 국적을 마음대로 넘나들며 자유로운 [[083_relationship_in_er_model|관계]]를 맺을 수 있습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. **시나리오 — 클라우드/[[063_docker_architecture|도커]] 환경의 [[082_zero_downtime_deployment_rolling_blue_green_canary|무중단 배포]] (Blue/Green [[087_deployment_kubernetes_workload_rolling_update|Deployment]])**: 톰캣(Tomcat) 서버에 새로운 [[288_version_ihl_tos_total_length|버전]]의 `app-v2.0.war`를 배포했다. 서버를 끄지 않고 `app-v1.0.war`에서 `v2.0`으로 트래픽을 갈아 끼우고 싶다.
   - **아키텍처 적용 (Symlink의 마법)**: Nginx나 Tomcat의 [[009_config|설정]] [[501_file_definition_logical_record|파일]]은 항상 `/deploy/current` 라는 [[501_file_definition_logical_record|파일]]을 바라보게 세팅한다.
   - 평소에는 `current -> app-v1.0` ([[512_symbolic_link|심볼릭 링크]])로 연결되어 있다.
   - 배포 파이프라인([[071_jenkins_ci_cd_pipeline_automation|Jenkins]])이 `app-v2.0` [[501_file_definition_logical_record|파일]]을 올린 뒤, 마지막 0.1초 순간에 [[512_symbolic_link|심볼릭 링크]]를 `ln -sfn app-v2.0 current` [[158_instruction|명령어]]로 덮어씌운다.
   - 웹 서버(Nginx)는 아무것도 모른 채 그저 `current`를 읽을 뿐인데, 링크가 바뀌었으므로 즉시 새 [[288_version_ihl_tos_total_length|버전]] 코드가 서비스된다. 구버전 롤백도 링크만 다시 돌리면 끝이다. 실무에서 가장 많이 쓰이는 [[512_symbolic_link|심볼릭 링크]]의 대명사다.

2. **시나리오 — [[730_ransomware|랜섬웨어]] 방어 및 [[022_snapshot_backup_architecture|스냅샷]] [[555_backup_and_restore_strategy|백업]] (Hard Link의 극의)**: 리눅스 서버에서 매시간 전체 시스템 [[501_file_definition_logical_record|파일]] 100GB를 [[555_backup_and_restore_strategy|백업]]해야 한다. 하루면 [[555_backup_and_restore_strategy|백업]] 용량이 2400GB(2.4TB)가 되어 디스크가 터져버린다.
   - **아키텍처 적용 (rsync와 [[511_hard_link|Hard Link]])**: 애플의 Time Machine이나 리눅스의 `rsync --link-dest` 증분 [[555_backup_and_restore_strategy|백업]] 도구의 핵심 원리다.
   - 1시간 전 [[555_backup_and_restore_strategy|백업]]과 지금 [[555_backup_and_restore_strategy|백업]]을 비교해서 **바뀌지 않은 [[501_file_definition_logical_record|파일]](99%)은 진짜로 100GB를 복사하지 않고 '[[511_hard_link|하드 링크]]'만 [[087_process_state_transition|생성]]**한다. 바뀐 1%의 [[501_file_definition_logical_record|파일]]만 진짜로 복사(i-node 새로 [[087_process_state_transition|생성]])한다.
   - [[555_backup_and_restore_strategy|백업]] 폴더를 열어보면 완벽한 100GB짜리 폴더 24개가 보이지만, 실제 디스크 사용량은 100GB + (수정된 용량 약간) 뿐이다.
   - 만약 해커가 최신 원본을 지워버려도? 과거 [[555_backup_and_restore_strategy|백업]]본이 쥐고 있는 [[511_hard_link|하드 링크]]의 Link Count 덕분에 진짜 [[001_dikw_pyramid|데이터]] 블록은 삭제되지 않고 안전하게 보존된다.

### 의사결정 및 튜닝 플로우

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 파일 참조 및 백업 아키텍처 (Link 방식) 설계 플로우          │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [서버 내 동일한 파일을 여러 경로/사용자가 공유해야 하는 상황 발생]            │
  │                │                                                  │
  │                ▼                                                  │
  │      공유할 대상이 파일인가, 디렉터리(폴더)인가?                             │
  │          ├─ 디렉터리 ─▶ [무조건 Symbolic Link 사용]                  │
  │          │            (OS 정책상 디렉터리 하드 링크는 금지됨)              │
  │          └─ 파일                                                  │
  │                │                                                  │
  │                ▼                                                  │
  │      공유할 파일들이 서로 다른 파티션(볼륨, 마운트 포인트)에 위치하는가?        │
  │          ├─ 예 ─────▶ [무조건 Symbolic Link 사용]                  │
  │          │            (하드 링크는 동일한 i-node 테이블을 써야 하므로 파티션│
  │          │             횡단이 하드웨어적으로 불가능함)                    │
  │          └─ 아니오 (같은 파티션 안이다)                               │
  │                │                                                  │
  │                ▼                                                  │
  │      원본 파일이 삭제되더라도 링크된 파일의 데이터는 영구 보존되어야 하는가?    │
  │          ├─ 예 ─────▶ [Hard Link 사용 (백업, 버전 관리 아키텍처)]       │
  │          │            (원본 이름이 지워져도 데이터 블록은 100% 생존)         │
  │          │                                                        │
  │          └─ 아니오 ──▶ [Symbolic Link 사용 (버전 스위칭, 단순 바로가기)] │
  │                         (원본을 지우면 링크도 깨져서 404 에러를 내뱉어야 함) │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** "리눅스 초보는 [[512_symbolic_link|심볼릭 링크]]를 쓰고, 리눅스 고수는 [[511_hard_link|하드 링크]]를 쓴다." [[555_backup_and_restore_strategy|백업]] 엔지니어에게 [[511_hard_link|하드 링크]]는 신이 내린 선물이다. `rm` [[158_instruction|명령어]]가 하드디스크의 0과 1을 지우는 [[158_instruction|명령어]](Erase)가 아니라, 그저 i-node의 Link Count를 1 빼는 '산수 [[158_instruction|명령어]]'에 불과하다는 뼈저린 진리를 이해할 때 비로소 [[501_file_definition_logical_record|파일]] 시스템을 지배할 수 있다.

### 도입 [[435_checklist_based_testing|체크리스트]]
- **Git과 [[511_hard_link|하드 링크]]의 마법**: 개발자들이 숨 쉬듯 쓰는 `git` 시스템에서 수만 번의 커밋을 해도 `.git/objects` 폴더가 터지지 않는 이유는 무엇일까? [[501_file_definition_logical_record|파일]] 내용이 완전히 똑같으면 Git은 해시값을 i-node처럼 취급하여 [[511_hard_link|하드 링크]]와 유사한 객체 재활용(Deduplication) 기법을 사용한다. 이 중복 제거 철학을 시스템 용량 산정에 적용하고 있는가?

- **📢 섹션 요약 비유**: [[512_symbolic_link|심볼릭 링크]]는 '즐겨찾기 버튼'입니다. 즐겨찾기를 100개 만들어도 웹페이지 원본이 닫히면 모두 엑박(404)이 뜹니다. [[511_hard_link|하드 링크]]는 '공동 명의 문서'입니다. 공동 명의자가 10명이라면, 9명이 권리를 포기([[197_rm_rate_monotonic_scheduling|rm]])해도 마지막 1명이 남아있는 한 그 재산([[001_dikw_pyramid|데이터]])은 영원히 보존됩니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [[501_file_definition_logical_record|파일]] 단순 복사 ([[086_CP_순환_전치_GI|cp]]) | [[511_hard_link|Hard Link]] 기반 아키텍처 | [[512_symbolic_link|Symbolic Link]] 기반 아키텍처 |
|:---|:---|:---|:---|
| **정량 (디스크 용량)**| 복사할 때마다 100%씩 용량 증가 | **수백 개를 링크해도 용량 증가 0%** | 링크 텍스트 크기(수십 [[074_byte|바이트]])만 증가 |
| **정량 ([[087_process_state_transition|생성]]/삭제 속도)**| 수 GB 복사 시 수십 초 [[015_지연_데이터_관점|지연]] | **1나노초 (카운트만 올림)** | 1나노초 (텍스트만 씀) |
| **정성 (운영 유연성)**| [[001_dikw_pyramid|데이터]] 파편화 및 [[212_synchronization_mechanisms|동기화]] 붕괴 | [[022_snapshot_backup_architecture|스냅샷]], 증분 [[555_backup_and_restore_strategy|백업]] 솔루션에 최적 | 시스템 [[506_directory_structure_symbol_table|디렉터리]] 경로 [[198_abstraction_control_data_process|추상화]] 및 배포 최적화 |

### 미래 전망
- **Btrfs, ZFS의 [[542_cow_file_system|Copy-On-Write]]([[542_cow_file_system|COW]])와 Reflink**: [[511_hard_link|하드 링크]]는 좋지만 "링크된 놈을 수정하면 원본도 같이 수정되어버린다"는 치명적 단점이 있다. 현대의 Btrfs [[501_file_definition_logical_record|파일]] 시스템은 `cp --reflink` 라는 하이브리드 기능을 제공한다. 복사할 때는 [[511_hard_link|하드 링크]]처럼 용량을 안 먹는데, 나중에 수정(Write)을 시도할 때만 물리적으로 [[501_file_definition_logical_record|파일]]을 쪼개서 복사본을 만들어주는 [[542_cow_file_system|COW]] 기법이 [[561_container_based_deployment|컨테이너]] 이미지 레이어(OverlayFS)의 핵심 기술로 쓰이고 있다.

### 결론
[[511_hard_link|하드 링크]]와 [[512_symbolic_link|심볼릭 링크]]의 차이는, [[501_file_definition_logical_record|파일]] 시스템이 "[[001_dikw_pyramid|데이터]] 그 자체([[001_dikw_pyramid|Data]] Block)"와 "[[001_dikw_pyramid|데이터]]를 가리키는 포인터(i-node 및 [[506_directory_structure_symbol_table|Directory]] Entry)"를 어떻게 철저하게 계층화하여 분리해 냈는지를 보여주는 가장 훌륭한 교보재다. 이름표([[506_directory_structure_symbol_table|디렉터리]])가 [[501_file_definition_logical_record|파일]]의 본질이 아니라, 디스크 구석에 박혀있는 숫자의 덩어리(i-node)가 진짜 [[501_file_definition_logical_record|파일]]의 본질임을 깨닫는 순간, `rm` [[158_instruction|명령어]]로 삭제한 [[501_file_definition_logical_record|파일]]이 왜 [[658_ir_recovery|복구]] 툴로 1초 만에 살아나는지, 수 테라바이트의 [[555_backup_and_restore_strategy|백업]]이 어떻게 1초 만에 끝나는지 시스템의 진짜 민낯을 보게 된다.

- **📢 섹션 요약 비유**: 그림([[001_dikw_pyramid|데이터]])은 하나인데 액자([[511_hard_link|하드 링크]])를 여러 개 씌우는 것과, 액자는 하나인데 그 액자가 어디 있는지 메모지([[512_symbolic_link|심볼릭 링크]])만 수백 장 뿌리는 것의 차이입니다. 액자가 몇 개든 메모지가 몇 장이든 전시회장의 그림은 오직 단 하나뿐이며, 공간(디스크)은 절대 낭비되지 않습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [[525_fat_file_allocation_table|FAT]] 방식 [[524_linked_allocation|연결 할당]] 최적화 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| i-node 직접/간접 포인터 [[154_database_index_b_tree_search_optimization|인덱스]] | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [[517_virtual_file_system_vfs|VFS]] 가상 [[501_file_definition_logical_record|파일]] 시스템 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [[536_buffer_cache_page_cache|버퍼 캐시]] [[501_file_definition_logical_record|파일]] 입출력 [[015_지연_데이터_관점|지연]] | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[i-node 직접/간접 포인터 인덱스]
    │
    ▼
[하드 링크 / 심볼릭 링크 차이 (Hard Link Vs Symbolic Link)]
    │
    ├──▶ [VFS 가상 파일 시스템]
    └──▶ [버퍼 캐시 파일 입출력 지연]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. '[[001_dikw_pyramid|데이터]]'는 강아지 1마리예요. 강아지에게 '초코'라는 이름표를 달아줬어요.
2. **[[511_hard_link|하드 링크]]**는 강아지 목줄에 '바둑이'라는 이름표를 하나 더 다는 거예요. 동생이 바둑이라고 부르든, 내가 초코라고 부르든 달려오는 강아지는 똑같아요! 이름표를 하나 떼어내도 강아지는 안 죽어요.
3. **[[512_symbolic_link|심볼릭 링크]]**는 강아지 집 앞에 "이 강아지는 초코입니다"라고 쪽지를 써 붙이는 거예요. 쪽지를 보고 강아지인 줄 알 수 있지만, 만약 진짜 강아지가 딴 곳으로 이사 가버리면 쪽지만 보고 온 사람은 허탕을 치게 된답니다.
