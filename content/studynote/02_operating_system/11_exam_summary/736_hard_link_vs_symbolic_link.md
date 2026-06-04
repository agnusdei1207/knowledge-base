+++
title = "736. 하드 링크 / 심볼릭 링크 차이 (Hard Link Vs Symbolic Link)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 리눅스 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템에서 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 '이름표([디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 엔트리)'와 '실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(i-node)'로 분리되어 있다. 링크(Link)는 하나의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 접근하기 위한 <strong>새로운 이름표를 다는 기술</strong>이다.
> 2. <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/">하드 링크</a> (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/">Hard Link</a>)</strong>: 원본 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)과 <strong>완벽히 동일한 i-node 번호</strong>를 가리키는 또 다른 이름표다. 원본을 지워도 [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)가 남아있으면 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 절대 지워지지 않으며, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 다르면([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 다르면) i-node 체계가 달라 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)할 수 없다.
> 3. <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/">심볼릭 링크</a> (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/">Symbolic Link</a> / Soft Link)</strong>: 원본 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 <strong>'경로(Path) 텍스트'만을 저장한 껍데기 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a></strong>이다. 원본 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 삭제되거나 이름이 바뀌면 허공을 맴도는 고아(Broken Link)가 되지만, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이나 운영체제의 경계를 자유롭게 넘나들 수 있는 유연성을 갖는다. (Windows의 바로 가기와 동일)

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/">하드 링크</a> (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/">Hard Link</a>)</strong>: 기존 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 i-node를 직접 가리키는 새로운 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 엔트리를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 것.
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/">심볼릭 링크</a> (Soft Link)</strong>: 기존 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 '경로 문자열'을 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 갖고 있는 완전히 새로운 i-node([파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하는 것.

- <strong>필요성 (<a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 공유와 중복 저장 방지)</strong>:
  - 10GB짜리 거대한 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 `/var/log` 폴더에도 두고 싶고, 내 홈 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)(`/home/user`)에서도 열어보고 싶다.
  - 이 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 `cp` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)로 복사하면 디스크 용량이 20GB로 늘어나는 끔찍한 낭비가 발생하고, 원본이 수정될 때 내 복사본은 수정되지 않는 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 문제가 터진다.
  - **해결책**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 복사하지 말고, <strong>"같은 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 가리키는 문(Link)"</strong>만 여러 개 만들자!

  - <strong>원본 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a></strong>: 서울 강남구 테헤란로 1번지 건물 (실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), i-node).
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/">하드 링크</a></strong>: 그 건물에 달린 '정문'과 '후문'. 정문을 부순다고(원본 삭제) 건물이 무너지지 않는다. 후문으로 들어가면 똑같은 건물이 나온다. (건물 자체를 부수려면 정문과 후문을 다 헐어야 함). 단, 강남구 건물의 문을 부산에 달 수는 없다 ([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 간 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 불가).
  - <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/">심볼릭 링크</a></strong>: 부산에 있는 내 책상에 놓인 포스트잇. 포스트잇에는 "강남구 테헤란로 1번지로 가시오"라고 적혀 있다. 강남구 건물이 헐리면(원본 삭제), 포스트잇을 보고 찾아가도 텅 빈 공터만 나온다 (Broken Link). 하지만 미국, 일본 어디에든 이 포스트잇은 둘 수 있다.

- **발전 과정**:
  1. <strong><a href="/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/">초기</a> Unix</strong>: 디스크 용량을 아끼기 위해 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 내부에서만 동작하는 [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/) 위주 사용.
  2. **네트워크 시대**: 서로 다른 디스크 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)과 네트워크 드라이브가 엮이면서, 이를 유연하게 넘나들 수 있는 [심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/)가 현대 OS의 표준 링킹 기법으로 대중화됨.

- **📢 섹션 요약 비유**: [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)는 내 본명(김철수)과 별명(철렁이)입니다. 이름만 다를 뿐 100% 동일한 나 자신입니다. [심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/)는 내 집 주소가 적힌 '명함'입니다. 명함을 찢는다고 내가 죽진 않지만, 내가 이사 가면 명함을 보고 찾아온 사람은 날 만날 수 없습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 리눅스 i-node 아키텍처와 Link의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)

리눅스의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 `[디렉터리 (파일 이름)] --가리킴---> [i-node (메타데이터)] --가리킴---> [Data Blocks]` 의 3단 구조를 가진다.

```text
  +-------------------------------------------------------------------+
  |                 하드 링크 vs 심볼릭 링크 내부 구조 비교                 |
  +-------------------------------------------------------------------+
  |                                                                   |
  |  [ 원본 파일 A 생성 (`echo "hello" > A`) ]                          |
  |   - 디렉터리: 이름 `A` ---> [ i-node 100번 (Link Count: 1) ]         |
  |                                +---> Data Block ("hello")          |
  |                                                                   |
  |  [ 하드 링크 B 생성 (`ln A B`) ]                                    |
  |   - 디렉터리: 이름 `B` ---> [ i-node 100번 (Link Count: 2) ] <---     |
  |   ★ 새로운 i-node를 만들지 않음! 기존 i-node의 래퍼런스 카운트만 +1 올림!  |
  |                                                                   |
  |  [ 심볼릭 링크 C 생성 (`ln -s A C`) ]                               |
  |   - 디렉터리: 이름 `C` ---> [ i-node 200번 (Link Count: 1) ]         |
  |                                +---> Data Block (텍스트 "A" 라는 경로) |
  |   ★ 완전히 새로운 i-node를 생성함! 원본의 카운트(Link Count)는 오르지 않음!|
  +-------------------------------------------------------------------+
```

**[다이어그램 해설 (삭제 시나리오)]**
만약 사용자가 `rm A`를 치면 무슨 일이 일어날까?
- <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/">하드 링크</a> 측면</strong>: `A`라는 이름표가 떨어져 나간다. i-node 100번의 Link Count가 `2 -> 1`로 줄어든다. 카운트가 0이 아니므로 OS는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 안 지운다! `B`를 열면 여전히 "hello"가 정상적으로 나온다.
- <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/">심볼릭 링크</a> 측면</strong>: `A`가 사라졌지만 `C`는 여전히 "A로 가라"는 텍스트를 들고 있다. 사용자가 `C`를 여는 순간 OS는 "A를 찾을 수 없음(No such [file](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) or [directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/))" 에러를 뱉는다.

- **📢 섹션 요약 비유**: 공장 컨베이어벨트가 어떤 순서로 부품을 받아 가공하고 내보내는지 설계도를 펼쳐 보는 것과 같다.

---

## Ⅲ. 비교 및 연결

### [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/) vs [심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/) 심층 비교

| 비교 항목 | [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/) ([Hard Link](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)) | [심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/) (Symbolic/Soft Link) |
|:---|:---|:---|
| **i-node 번호** | **원본과 동일 (i-node 공유)** | **원본과 다름 (새로운 i-node)** |
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 크기</strong> | 0바이트 (이름표만 추가되므로 용량 0) | 경로 문자열의 길이만큼 (예: 수 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/)) |
| **원본 삭제 시** | 링크는 멀쩡함. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 100% 보존. | 링크는 깨짐 (Broken/Dangling Link). |
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/">디렉터리</a> 링킹</strong> | **운영체제가 강제로 금지함 (순환 고리 위험)**| [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/), [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 상관없이 마음껏 가능 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">파티션</a> 횡단</strong> | <strong>불가능 (다른 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">파티션</a>은 i-node 테이블이 다름)</strong>| <strong>가능 (네트워크 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/516_mount_mechanism/">마운트</a>, 외장 하드 다 됨)</strong> |

### [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)(폴더) [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)를 금지하는 이유

리눅스에서 `ln dir1 dir2` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 치면 "[hard link](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/) not allowed for [directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)" 에러가 뜬다. 왜 폴더는 [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)를 못 만들게 할까?
- [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/)에 [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)를 허용하면, 상위 폴더가 하위 폴더의 자식이 되고, 하위 폴더가 다시 상위 폴더를 가리키는 <strong>무한 순환 트리 (Infinite Loop Cycle)</strong>가 발생할 위험이 크기 때문이다.
- 이렇게 되면 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 프로그램이나 `find` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 같은 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 순회 프로그램들이 무한 루프에 빠져 영원히 폴더를 빠져나오지 못하고 시스템 메모리를 터뜨린다.
- *예외*: 리눅스의 모든 폴더에 있는 `.`(현재 폴더)와 `..`(부모 폴더)만이 유일하게 OS 커널이 예외적으로 직접 만들어주는 '안전한 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)'다.

- **📢 섹션 요약 비유**: [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)는 피가 섞인 '친자식'이라서 호적([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))을 함부로 옮길 수 없고 촌수([디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 순환)를 꼬이게 해선 안 됩니다. [심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/)는 '입양아'나 '친구'라서 호적과 국적을 마음대로 넘나들며 자유로운 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)를 맺을 수 있습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오

1. <strong>시나리오 — 클라우드/<a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/063_docker_architecture/">도커</a> 환경의 <a href="/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/082_zero_downtime_deployment_rolling_blue_green_canary/">무중단 배포</a> (Blue/Green <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/087_deployment_kubernetes_workload_rolling_update/">Deployment</a>)</strong>: 톰캣(Tomcat) 서버에 새로운 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)의 `app-v2.0.war`를 배포했다. 서버를 끄지 않고 `app-v1.0.war`에서 `v2.0`으로 트래픽을 갈아 끼우고 싶다.
   - **아키텍처 적용 (Symlink의 마법)**: Nginx나 Tomcat의 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)은 항상 `/deploy/current` 라는 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 바라보게 세팅한다.
   - 평소에는 `current -> app-v1.0` ([심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/))로 연결되어 있다.
   - 배포 파이프라인([Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/))이 `app-v2.0` [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 올린 뒤, 마지막 0.1초 순간에 [심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/)를 `ln -sfn app-v2.0 current` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)로 덮어씌운다.
   - 웹 서버(Nginx)는 아무것도 모른 채 그저 `current`를 읽을 뿐인데, 링크가 바뀌었으므로 즉시 새 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 코드가 서비스된다. 구버전 롤백도 링크만 다시 돌리면 끝이다. 실무에서 가장 많이 쓰이는 [심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/)의 대명사다.

2. <strong>시나리오 — <a href="/knowledge-base/studynote/09_security/15_malware_attack_vectors/730_ransomware/">랜섬웨어</a> 방어 및 <a href="/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/">스냅샷</a> <a href="/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/">백업</a> (Hard Link의 극의)</strong>: 리눅스 서버에서 매시간 전체 시스템 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 100GB를 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)해야 한다. 하루면 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 용량이 2400GB(2.4TB)가 되어 디스크가 터져버린다.
   - <strong>아키텍처 적용 (rsync와 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/">Hard Link</a>)</strong>: 애플의 Time Machine이나 리눅스의 `rsync --link-dest` 증분 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 도구의 핵심 원리다.
   - 1시간 전 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)과 지금 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)을 비교해서 <strong>바뀌지 않은 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>(99%)은 진짜로 100GB를 복사하지 않고 '<a href="/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/">하드 링크</a>'만 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a></strong>한다. 바뀐 1%의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)만 진짜로 복사(i-node 새로 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/))한다.
   - [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 폴더를 열어보면 완벽한 100GB짜리 폴더 24개가 보이지만, 실제 디스크 사용량은 100GB + (수정된 용량 약간) 뿐이다.
   - 만약 해커가 최신 원본을 지워버려도? 과거 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)본이 쥐고 있는 [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)의 Link Count 덕분에 진짜 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록은 삭제되지 않고 안전하게 보존된다.

### 의사결정 및 튜닝 플로우

```text
  +-------------------------------------------------------------------+
  |                 파일 참조 및 백업 아키텍처 (Link 방식) 설계 플로우          |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [서버 내 동일한 파일을 여러 경로/사용자가 공유해야 하는 상황 발생]            |
  |                |                                                  |
  |                v                                                  |
  |      공유할 대상이 파일인가, 디렉터리(폴더)인가?                             |
  |          +- 디렉터리 --> [무조건 Symbolic Link 사용]                  |
  |          |            (OS 정책상 디렉터리 하드 링크는 금지됨)              |
  |          +- 파일                                                  |
  |                |                                                  |
  |                v                                                  |
  |      공유할 파일들이 서로 다른 파티션(볼륨, 마운트 포인트)에 위치하는가?        |
  |          +- 예 ------> [무조건 Symbolic Link 사용]                  |
  |          |            (하드 링크는 동일한 i-node 테이블을 써야 하므로 파티션|
  |          |             횡단이 하드웨어적으로 불가능함)                    |
  |          +- 아니오 (같은 파티션 안이다)                               |
  |                |                                                  |
  |                v                                                  |
  |      원본 파일이 삭제되더라도 링크된 파일의 데이터는 영구 보존되어야 하는가?    |
  |          +- 예 ------> [Hard Link 사용 (백업, 버전 관리 아키텍처)]       |
  |          |            (원본 이름이 지워져도 데이터 블록은 100% 생존)         |
  |          |                                                        |
  |          +- 아니오 ---> [Symbolic Link 사용 (버전 스위칭, 단순 바로가기)] |
  |                         (원본을 지우면 링크도 깨져서 404 에러를 내뱉어야 함) |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** "리눅스 초보는 [심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/)를 쓰고, 리눅스 고수는 [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)를 쓴다." [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 엔지니어에게 [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)는 신이 내린 선물이다. `rm` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 하드디스크의 0과 1을 지우는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)(Erase)가 아니라, 그저 i-node의 Link Count를 1 빼는 '산수 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)'에 불과하다는 뼈저린 진리를 이해할 때 비로소 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템을 지배할 수 있다.

### 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
- <strong>Git과 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/">하드 링크</a>의 마법</strong>: 개발자들이 숨 쉬듯 쓰는 `git` 시스템에서 수만 번의 커밋을 해도 `.git/objects` 폴더가 터지지 않는 이유는 무엇일까? [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 내용이 완전히 똑같으면 Git은 해시값을 i-node처럼 취급하여 [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)와 유사한 객체 재활용(Deduplication) 기법을 사용한다. 이 중복 제거 철학을 시스템 용량 산정에 적용하고 있는가?

- **📢 섹션 요약 비유**: [심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/)는 '즐겨찾기 버튼'입니다. 즐겨찾기를 100개 만들어도 웹페이지 원본이 닫히면 모두 엑박(404)이 뜹니다. [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)는 '공동 명의 문서'입니다. 공동 명의자가 10명이라면, 9명이 권리를 포기([rm](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/197_rm_rate_monotonic_scheduling/))해도 마지막 1명이 남아있는 한 그 재산([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 영원히 보존됩니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 단순 복사 ([cp](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/)) | [Hard Link](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/) 기반 아키텍처 | [Symbolic Link](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/) 기반 아키텍처 |
|:---|:---|:---|:---|
| **정량 (디스크 용량)**| 복사할 때마다 100%씩 용량 증가 | **수백 개를 링크해도 용량 증가 0%** | 링크 텍스트 크기(수십 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/))만 증가 |
| <strong>정량 (<a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a>/삭제 속도)</strong>| 수 GB 복사 시 수십 초 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | **1나노초 (카운트만 올림)** | 1나노초 (텍스트만 씀) |
| **정성 (운영 유연성)**| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 파편화 및 [동기화](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 붕괴 | [스냅샷](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/022_snapshot_backup_architecture/), 증분 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 솔루션에 최적 | 시스템 [디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 경로 [추상화](/knowledge-base/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 및 배포 최적화 |

### 미래 전망
- <strong>Btrfs, ZFS의 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/">Copy-On-Write</a>(<a href="/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/">COW</a>)와 Reflink</strong>: [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)는 좋지만 "링크된 놈을 수정하면 원본도 같이 수정되어버린다"는 치명적 단점이 있다. 현대의 Btrfs [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템은 `cp --reflink` 라는 하이브리드 기능을 제공한다. 복사할 때는 [하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)처럼 용량을 안 먹는데, 나중에 수정(Write)을 시도할 때만 물리적으로 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 쪼개서 복사본을 만들어주는 [COW](/knowledge-base/studynote/02_operating_system/09_file_system/542_cow_file_system/) 기법이 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 이미지 레이어(OverlayFS)의 핵심 기술로 쓰이고 있다.

### 결론
[하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/)와 [심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/)의 차이는, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템이 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 그 자체([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Block)"와 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 가리키는 포인터(i-node 및 [Directory](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) Entry)"를 어떻게 철저하게 계층화하여 분리해 냈는지를 보여주는 가장 훌륭한 교보재다. 이름표([디렉터리](/knowledge-base/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/))가 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 본질이 아니라, 디스크 구석에 박혀있는 숫자의 덩어리(i-node)가 진짜 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 본질임을 깨닫는 순간, `rm` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)로 삭제한 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 왜 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 툴로 1초 만에 살아나는지, 수 테라바이트의 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)이 어떻게 1초 만에 끝나는지 시스템의 진짜 민낯을 보게 된다.

- **📢 섹션 요약 비유**: 그림([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))은 하나인데 액자([하드 링크](/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/))를 여러 개 씌우는 것과, 액자는 하나인데 그 액자가 어디 있는지 메모지([심볼릭 링크](/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/))만 수백 장 뿌리는 것의 차이입니다. 액자가 몇 개든 메모지가 몇 장이든 전시회장의 그림은 오직 단 하나뿐이며, 공간(디스크)은 절대 낭비되지 않습니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [FAT](/knowledge-base/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/) 방식 [연결 할당](/knowledge-base/studynote/02_operating_system/09_file_system/524_linked_allocation/) 최적화 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| i-node 직접/간접 포인터 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [VFS](/knowledge-base/studynote/02_operating_system/09_file_system/517_virtual_file_system_vfs/) 가상 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [버퍼 캐시](/knowledge-base/studynote/02_operating_system/09_file_system/536_buffer_cache_page_cache/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 입출력 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[i-node 직접/간접 포인터 인덱스]
    |
    v
[하드 링크 / 심볼릭 링크 차이 (Hard Link Vs Symbolic Link)]
    |
    +---> [VFS 가상 파일 시스템]
    +---> [버퍼 캐시 파일 입출력 지연]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. '[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)'는 강아지 1마리예요. 강아지에게 '초코'라는 이름표를 달아줬어요.
2. <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/511_hard_link/">하드 링크</a></strong>는 강아지 목줄에 '바둑이'라는 이름표를 하나 더 다는 거예요. 동생이 바둑이라고 부르든, 내가 초코라고 부르든 달려오는 강아지는 똑같아요! 이름표를 하나 떼어내도 강아지는 안 죽어요.
3. <strong><a href="/knowledge-base/studynote/02_operating_system/09_file_system/512_symbolic_link/">심볼릭 링크</a></strong>는 강아지 집 앞에 "이 강아지는 초코입니다"라고 쪽지를 써 붙이는 거예요. 쪽지를 보고 강아지인 줄 알 수 있지만, 만약 진짜 강아지가 딴 곳으로 이사 가버리면 쪽지만 보고 온 사람은 허탕을 치게 된답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 736 / 800

<- **이전**: [735. i-node 직접/간접 포인터 인덱스 (Inode Direct Indirect Pointer Index)](/knowledge-base/studynote/02_operating_system/11_exam_summary/735_inode_direct_indirect_pointer_index/)
**다음**: [737. VFS 가상 파일 시스템 (VFS Virtual File System Abstraction)](/knowledge-base/studynote/02_operating_system/11_exam_summary/737_vfs_virtual_file_system_abstraction/) ->

---
