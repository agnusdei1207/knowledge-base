---
title: "Wear Leveling"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/) ([Wear Leveling](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/))는 SSD나 [USB](/studynote/01_computer_architecture/09_system_bus_interconnects/359_usb/) [플래시 메모리](/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/)의 낸드(NAND) 셀이 구조적으로 <strong>'<a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a>/지우기 횟수 한계(P/E Cycle)'를 가진다는 치명적 결함을 극복하기 위해, 컨트롤러(<a href="/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/">FTL</a>)가 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 여러 블록에 골고루 분산시켜 기록하는 수명 연장 <a href="/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>이다.
> 2. **가치**: 특정 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 영역([FAT](/studynote/02_operating_system/09_file_system/525_fat_file_allocation_table/) 테이블 등)이나 자주 갱신되는 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 디스크의 한 구역만 집중적으로 파괴하여 디스크 전체가 사망하는 현상을 막아, 오늘날 플래시 스토리지가 엔터프라이즈 서버와 스마트폰의 심장으로 쓰일 수 있게 만든 1등 공신이다.
> 3. **융합**: [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 주소(LBA)에 같은 값을 계속 쓰지만, 밑바닥의 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 컨트롤러는 '[가상 메모리](/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)' 매핑 기법을 모방하여 물리적 주소(PBA)를 계속 바꿔치기하는 '소프트웨어와 하드웨어의 완벽한 [추상화](/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/) 분리(Decoupling)' 아키텍처다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - [플래시 메모리](/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/) 셀에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓸 때는 높은 [전압](/studynote/01_computer_architecture/01_basic_electronics_logic/001_voltage/)(약 20V)을 가해 전자를 산화막 안에 가두는데, 이 과정에서 절연체가 서서히 손상된다. (마모, Wear out)
  - 통상 셀 하나당 1,000번 ~ [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/),000번 썼다 지우면(P/E Cycle) 그 셀은 완전히 타버려 배드 블록(Bad Block)이 된다.
  - [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)는 수만 개의 블록들이 모두 '비슷한 횟수'로 낡아가도록 지휘하는 두뇌(컨트롤러)의 지능적인 튜닝 로직이다.

- **필요성(문제의식)**:
  - 과거 하드 디스크([HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/)) 기반의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템인 FAT32나 NTFS를 SSD에 그대로 깔면 재앙이 터진다.
  - OS는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)나 [MBR](/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/)(부트 레코드) 같은 특정 0번 블록 구역을 초당 수백 번씩 미친 듯이 덮어쓴다(Overwrite in place).
  - [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)가 없다면 이 0번 블록은 단 며칠 만에 수명을 다해 죽어버리고, 나머지 99%의 공간이 멀쩡한데도 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 전체가 인식 불능으로 버려지게 된다.
  - **해결책**: "OS가 0번 블록에 계속 쓰라고 지시해도, 내가 몰래 1번 블록, 2번 블록, 100번 블록으로 진짜 물리적 위치를 뺑뺑이 돌리면서 저장하자!"

  - **평준화 안 됨**: 공장장이 매일 출근하는 1번 창고 바닥만 집중적으로 지게차를 굴려서, 1번 바닥만 한 달 만에 완전히 다 파여서 공장 전체가 마비됨. (다른 99개 창고는 새것임).
  - <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/">마모 평준화</a></strong>: 영리한 물류 로봇([FTL](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/) 컨트롤러)이 공장장(OS) 몰래, 매일 지게차가 달리는 동선을 1번부터 100번 창고까지 돌아가며 분산시킨다. 10년 뒤 모든 창고 바닥이 똑같이 닳았을 때 공장 수명이 다하게 만든다.

- **등장 배경**:
  - 2000년대 후반 SSD가 대중화되면서 NAND 플래시의 MLC/TLC 적층 기술로 인해 셀당 수명이 기하급수적으로 짧아지자(10만 번 $\rightarrow$ 1천 번), 이를 소프트웨어 컨트롤러 기술력으로 상쇄하기 위해 [FTL](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)([Flash Translation Layer](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/)) 내부에 도입되었다.

```text
  +-------------------------------------------------------------+
  |                 Wear Leveling (마모 평준화) 매커니즘의 매핑 원리        |
  +-------------------------------------------------------------+
  |                                                             |
  |  [ 운영체제 (OS)의 착각 ]                                       |
  |   - 파일 A 내용이 갱신됨. "논리 주소(LBA) 1번에 계속 덮어써라!"        |
  |     1차 쓰기: LBA 1 --+                                       |
  |     2차 쓰기: LBA 1 --+---> [ FTL (SSD 컨트롤러 내부) ]          |
  |     3차 쓰기: LBA 1 --+      - 매핑 테이블 (LBA -> 물리 블록 PBA)   |
  |                                |                             |
  |  =============================|============================ |
  |                               v                             |
  |  [ SSD 물리적 낸드 플래시 (PBA) ]                              |
  |                                                             |
  |  1차 쓰기: [ 물리 블록 10 ] 에 기록 (LBA 1 -> PBA 10 연결)        |
  |  2차 쓰기: 물리 블록 10은 놔두고 [ 물리 블록 45 ] 에 기록!             |
  |          (기존 블록 10은 '무효(Invalid)' 처리)                   |
  |  3차 쓰기: 또 다른 빈 공간인 [ 물리 블록 88 ] 에 기록!                 |
  |                                                             |
  |  -> 결과: OS는 1번 자리만 3번 긁었다고 믿지만, 실제 SSD는 10번, 45번,  |
  |          88번 셀을 골고루 1번씩 사용하여 수명을 3배로 연장함! 🚀         |
  +-------------------------------------------------------------+
```

**[다이어그램 해설]** 이것이 플래시 스토리지가 동작하는 근본적인 속임수다. [플래시 메모리](/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/)는 특성상 전자가 채워진 곳에 그냥 덮어쓰기(Overwrite)가 물리적으로 불가능하다. 무조건 블록 전체를 지우고(Erase) 다시 써야 하는데, 이 지우는 과정에서 셀이 타들어 간다. 그래서 FTL은 OS가 기존 LBA 1번에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 덮어쓰라고 명령하면, 그 명령을 씹고 항상 '완전히 새로운 빈 블록'인 PBA 45번을 찾아 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓴 뒤 매핑 포인터만 싹 바꿔치기한다(Out-of-place Update). 이 포인터 바꿔치기 덕분에 한 놈만 패는 OS의 고질병을 막고 100만 개의 블록을 골고루 폭행(Leveling)하는 예술적 평준화가 이루어진다.

- **📢 섹션 요약 비유**: OS라는 독재자가 "1번 노예(셀)만 죽을 때까지 때려라!"라고 명령했지만, 중간 관리자([FTL](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/))가 매일 밤 노예들의 이름표(매핑 테이블)를 몰래 바꿔서 100명의 노예가 한 대씩만 공평하게 맞도록 조작하는 고도의 인력 관리술입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)의 2가지 아키텍처 (동적 vs 정적)

단순히 쓰는 위치만 바꾼다고 평준화가 끝나지 않는다. [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 안에는 "절대 지워지지 않는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/), 사진 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))" 들이 큰 공간을 차지하고 있기 때문이다.

| 종류 | 개념 및 동작 원리 | 한계점 및 해결책 |
|:---|:---|:---|
| <strong>동적 <a href="/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/">마모 평준화</a> (Dynamic)</strong> | 사용자가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 변경(Write)할 때만 개입하여, **남아있는 빈 블록들 중에서** 사용 횟수가 가장 적은 블록을 찾아 할당한다. | **치명적 한계**: SSD의 80%가 안 변하는 동영상 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)로 꽉 차 있으면, 나머지 20%의 빈 공간끼리만 돌려막기를 하다가 그 20%가 먼저 다 타서 죽어버린다. (반쪽짜리 평준화) |
| <strong>정적 <a href="/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/">마모 평준화</a> (Static)</strong> | [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 컨트롤러가 백그라운드에서 한 번도 안 지워진 <strong>정적인 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>(동영상 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>)를 강제로 빈 곳으로 이사(Move)</strong> 시킨다! 그리고 그 깨끗한 블록을 새로 쓸 수 있게 뺏어온다. | **완벽한 평준화**: [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 안의 모든 블록이 100% 공평하게 마모됨. (단점: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 복사 이동([Write Amplification](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/))에 따른 내부 오버헤드 발생) |

### [SSD FTL](/studynote/02_operating_system/11_exam_summary/731_ssd_ftl_flash_translation_layer/) ([Flash Translation Layer](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/))의 구조

OS의 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템과 순수 플래시 하드웨어 사이에 있는 "미니 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)([FTL](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/))"의 구조를 뜯어보면 웨어 레벨링이 어떻게 구현되는지 알 수 있다.

```text
  +-------------------------------------------------------------------+
  |                 SSD 컨트롤러 내부 FTL (Flash Translation Layer) 구조    |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [ OS 파일 시스템 (ext4, NTFS) ] -- (LBA 논리 주소로 읽기/쓰기 명령) |
  |        |                                                          |
  |  ======|====================== (NVMe / SATA 버스) ================|
  |        v                                                          |
  |   [ SSD 컨트롤러 칩 (자체 ARM 코어 + 램 탑재) ]                        |
  |    +--------------------------------------------------------+     |
  |    | 1. Address Mapping Table (주소 변환기)                  |     |
  |    |    LBA 100 -> PBA 500 (논리를 물리로 변환)               |     |
  |    +--------------------------------------------------------+     |
  |    | 2. Wear Leveling Engine (마모 평준화 엔진) <- 핵심!        |     |
  |    |    - 모든 PBA 블록의 "Erase Count(지운 횟수)"를 모니터링 함.  |     |
  |    +--------------------------------------------------------+     |
  |    | 3. Garbage Collector (가비지 컬렉터)                     |     |
  |    |    - 버려진 유효하지 않은 데이터 블록들을 모아서 싹 청소함.         |     |
  |    +--------------------------------------------------------+     |
  |        |                                                          |
  |        v [ 플래시 메모리 다이 (낸드 셀) ]                               |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 일반 하드디스크([HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/)) 컨트롤러는 멍청한 모터 제어기일 뿐이지만, [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 컨트롤러는 내부에 자체 CPU(주로 쿼드코어 ARM)와 거대한 램([DRAM](/studynote/01_computer_architecture/06_memory_hierarchy_cache/251_dram/))을 탑재한 초정밀 컴퓨터다. 이 FTL이라는 미니 [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 셀의 건강 상태(지운 횟수)를 엑셀 표처럼 다 기록하고 있다. 정적 웨어 레벨링이 돌 때면 백그라운드에서 "어? 1번 블록은 지운 횟수가 10번인데, 900번 블록은 5000번이나 지웠네? 1번 블록에 있는 OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 900번 블록으로 강제로 이사 보내고, 1번 블록을 비워서 새로운 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 작업에 던져줘야지!"라는 극도로 지능적인 스와핑을 수행한다.

- **📢 섹션 요약 비유**: 체육관([SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))에서 배드민턴(빈번한 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/))을 치는 사람들 때문에 바닥 한가운데만 푹 파이는(동적 한계) 걸 막으려고, 체육관 구석에 돗자리를 펴고 가만히 앉아있는 관중(정적인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))들을 강제로 일으켜 세워 가운데로 자리를 옮기게 한 뒤, 그 관중이 앉아있던 깨끗한 구석 바닥에서 배드민턴을 치게 만드는(정적 평준화) 극강의 공간 활용술입니다.

---

## Ⅲ. 비교 및 연결

### [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)와 [Write Amplification](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/) ([쓰기 증폭](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/))의 딜레마

[마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)를 잘하려고 할수록 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 수명이 깎이는 기괴한 파라독스가 발생한다. 이를 <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/">쓰기 증폭</a>(WA)</strong>이라고 부른다.

| 지표 | 개념 및 산출 공식 | 딜레마 (왜 수명이 깎이는가?) |
|:---|:---|:---|
| <strong><a href="/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/">WAF</a></strong> ([Write Amplification](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/) Factor) | 실제 낸드에 쓰인 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 양 / 호스트(OS)가 쓴 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 양 | OS가 1MB를 썼는데 FTL이 평준화와 가비지 컬렉션을 한답시고 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 딴 곳으로 옮기느라 내부적으로 3MB를 썼다면 [WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) = 3 이다. 값이 1에 가까울수록 좋다. |
| **정적 웨어 레벨링의 그림자** | 안 쓰는 블록을 강제로 옮겨 평준화 달성 | 완벽한 평준화를 위해 무고한 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들을 읽고 쓰는 내부 복사(Internal Copy)가 폭증하여 [WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/) 수치를 올리고 전체 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 수명을 역으로 갉아먹는다. |
| <strong>오버 <a href="/studynote/09_security/11_iam_access_control/528_provisioning/">프로비저닝</a> (OP)</strong> | [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 용량의 7~28%를 숨겨두고 유저에게 안 보여줌 | 100GB SSD를 사도 10GB는 숨겨둔다(OP). 이 예비 공간이 넓어야 빈 곳을 찾기 쉽고 복사 비용([WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/))이 줄어 수명이 폭발적으로 늘어난다. |

### 과목 융합 관점

- <strong><a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 시스템 (TRIM <a href="/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a>)</strong>: 과거 OS는 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 지울 때 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 이름([디렉터리](/studynote/02_operating_system/09_file_system/506_directory_structure_symbol_table/) 엔트리)만 날리고, [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 컨트롤러에게는 "이거 지웠어"라고 말해주지 않았다. SSD는 버려진 쓰레기 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)인지 모르고 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)를 한답시고 쓰레기를 정성스럽게 다른 블록으로 이사(Copy)시켜주는 미친 짓을 반복했다. 이를 막기 위해 OS가 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 지울 때 SSD에게 "이 [논리 주소](/studynote/02_operating_system/06_memory_management/322_logical_virtual_address/)(LBA)는 이제 완전 쓰레기야, 신경 꺼!"라고 알려주는 <strong>TRIM <a href="/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a></strong>가 융합되었고, 덕분에 SSD의 [쓰기 증폭](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/)이 사라지고 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)이 비약적으로 향상되었다.
- **클라우드 스토리지 (AWS EBS / IOPS 통제)**: 클라우드에서 제공하는 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/) 된 SSD는 뒷단에서 무수히 많은 입주자(Tenant)가 I/O를 날린다. AWS는 스토리지 컨트롤러 레벨에서 웨어 레벨링으로 인한 내부 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 한계를 계산하여, 유저가 계약한 IOPS(초당 입출력 횟수)를 넘으면 가차 없이 대역폭을 꺾어버리는(Throttling) 버킷 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 적용해 물리적 플래시의 파괴를 방어한다.

- **📢 섹션 요약 비유**: 수명을 늘리겠다(웨어 레벨링)고 건강한 장기(블록)와 아픈 장기를 쉴 새 없이 수술로 위치를 바꾸다 보면, 그 수술 자체가 주는 스트레스([쓰기 증폭](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/)) 때문에 환자([SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))가 먼저 죽어버릴 수 있습니다. 그래서 병원(제조사)은 애초에 수술용 예비 장기(오버 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/))를 잔뜩 숨겨두고 이를 여유롭게 교체하는 전략을 씁니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 서버 튜닝

1. <strong>시나리오 — <a href="/studynote/05_database/01_db_architecture_relational/002_database_definition/">데이터베이스</a>(DB) 서버의 <a href="/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/">SSD</a> 조기 사망(Wear Out) 사태</strong>: [온프레미스](/studynote/07_enterprise_systems/01_strategy_governance/061_on_premise_legacy_infrastructure/) 장비에 [Oracle](/studynote/05_database/03_relational_model/188_pl_sql_t_sql_procedural/) DB를 깔고 캐시 사이즈를 너무 작게 잡았다. 6개월 만에 고가의 엔터프라이즈 [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) SSD의 "남은 수명 지표([Wear Leveling](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/) Count)"가 0%로 떨어져 하드웨어가 읽기 전용(Read-Only) 모드로 잠겨버리는 장애가 발생했다.
   - **원인 분석**: DB가 초당 수천 번씩 [Redo](/studynote/05_database/04_transactions_concurrency/234_redo_roll_forward_durability_recovery/) Log와 [Undo](/studynote/11_design_supervision/06_exam_summary/393_undo/) [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 4KB 블록 단위로 미친 듯이 썼다. 아무리 정적 [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)가 돌더라도, 절대적인 물리적 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)량(TBW, TeraBytes Written) 자체가 낸드 칩의 물리적 한계를 돌파한 것이다. 엔터프라이즈 장비라도 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 한계는 존재한다.
   - <strong>아키텍트 판단 (아키텍처 및 <a href="/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a> 튜닝)</strong>: 소프트웨어 레벨에서 I/O를 꺾어야 한다. 첫째, DB의 메모리 캐시(Buffer Pool)를 대폭 늘려(RAM 증설) 물리적 디스크 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 횟수 자체를 방어한다. 둘째, OS의 [마운트](/studynote/02_operating_system/09_file_system/516_mount_mechanism/) 옵션에 `noatime` ([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 읽을 때마다 접근 시간 기록 끄기)을 무조건 추가한다. 셋째, 디스크의 전체 용량을 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)할 때 100% 다 잡지 않고 **마지막 20% 공간을 미할당(Unallocated) 상태로 남겨두어**, [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 컨트롤러가 이를 오버 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/)(OP) 영역으로 자율적으로 쓰게 만들어 [쓰기 증폭](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/)([WAF](/studynote/03_network/13_network_security_basics/696_waf_web_application_firewall/))을 극단적으로 낮춘다.

2. **시나리오 — 보안 문서 영구 삭제(Wiping)의 불확실성**: 국방부 규정에 따라 기밀문서를 [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 불가능하게 파기하기 위해, 리눅스의 `shred`나 `dd` [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)로 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)에 0과 1의 쓰레기 값을 7번 덮어쓰기(Overwrite) 했다. 그런데 포렌식 장비로 스캔하니 원본 기밀문서가 고스란히 복원되었다.
   - **원인 분석**: [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)의 배신이다. OS가 `dd` 명령으로 "A [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 위치에 0을 7번 덮어써라"라고 지시했지만, [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 컨트롤러([FTL](/studynote/02_operating_system/08_storage_and_io_systems/478_ftl_flash_translation_layer/))는 수명 연장을 위해 똑같은 낸드 셀에 7번을 쓰지 않는다. 원본이 들어있던 물리 셀(PBA)은 고이 놔둔 채 '무효(Invalid)' 처리만 해두고, 계속 엉뚱한 새 셀들을 찾아다니며 0을 7번 써댄 것이다. 따라서 하드웨어 메모리 칩을 직접 떼어서 포렌식하면 원래 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 생생하게 살아있다.
   - <strong>아키텍트 판단 (<a href="/studynote/09_security/04_endpoint_security/405_secure_erase/">Secure Erase</a> <a href="/studynote/04_software_engineering/05_devops_ci_cd/271_command_pattern/">커맨드</a> 호출)</strong>: [플래시 메모리](/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/)에서 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 덮어쓰기 삭제는 100% 무의미하다. 기밀을 파기하려면 반드시 하드웨어 컨트롤러에 꽂아 넣는 <strong><code>nvme format</code> <a href="/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> <a href="/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a>나 <code>ATA Secure Erase</code> <a href="/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a></strong>를 전송해야 한다. 이 명령을 받으면 FTL은 매핑 테이블 전체를 암호학적으로 폐기하거나(Crypto Erase), 낸드 셀 전체에 고전압을 쏴서 동시에 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화해 버려 완벽한 물리적 파기를 보장한다.

```text
  +-------------------------------------------------------------------+
  |                 플래시 메모리(SSD) 수명 연장을 위한 아키텍트 점검 트리      |
  +-------------------------------------------------------------------+
  |                                                                   |
  |   [ SSD 기반의 고부하 시스템 인프라 구축 시 점검 사항 ]                     |
  |                |                                                  |
  |                v                                                  |
  |      OS 마운트 시 `discard` (TRIM) 옵션을 활성화했는가?                    |
  |          +- 아니오 ---> 🚨 [수명 경고] FTL이 쓰레기 데이터까지 평준화 이사시키느라|
  |          |             디스크 수명 급감. 즉시 fstrim 크론탭 설정 필수!        |
  |          +- 예 ------> 통과                                        |
  |                |                                                  |
  |                v                                                  |
  |      스토리지 파티셔닝 시 여유 공간(Unallocated)을 10~20% 남겨두었는가?       |
  |          +- 아니오 ---> 🚨 [성능 경고] 디스크가 90% 찰 경우, 빈 블록을 찾지 못해 |
  |          |             Write Amplification 폭증 및 속도 1/10 토막 발생!  |
  |          +- 예 ------> 통과 (자연스러운 Over-Provisioning 달성)       |
  |                |                                                  |
  |                v                                                  |
  |      로그 기록(SWAP 포함)이 디스크 한 곳을 집중 타격하는 아키텍처인가?           |
  |          +- 예 ------> RAM Disk(tmpfs)를 활용하여 디스크 로깅 우회 고려.    |
  |          +- 아니오 ---> 최종 SSD 인프라 배포 승인! 🚀                    |
  +-------------------------------------------------------------------+
```

**[다이어그램 해설]** 클라우드나 물리 서버에 SSD를 달고 HDD처럼 대충 포맷해서 쓰면 1년 안에 인프라 장애를 맞는다. 아키텍트는 SSD의 FTL이 어떻게 숨을 쉬는지 알아야 한다. TRIM은 FTL에게 어떤 짐을 버려도 되는지 알려주는 신호탄이고, [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 미할당(여백)은 FTL이 무거운 짐을 이리저리 옮길 때 숨통을 틔워주는 임시 작업 공간(오버 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/))이다. 꽉 찬 SSD가 유독 느려지는 이유는 빈 공간이 없어 이 평준화 작업과 가비지 컬렉션이 극악의 병목을 일으키기 때문이므로, 저장 공간의 80% 이상을 절대 채우지 않는 것이 불문율이다.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **SSD에서 디스크 조각 모음(Defragmentation) 실행**: 과거 [HDD](/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 시절 흩어진 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 모아 헤드 탐색 속도를 높이던 조각 모음을 SSD에서 돌리는 무지함. SSD는 물리적 헤드가 없어서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 아무리 파편화되어 있어도 읽기(Seek) 속도가 일정하다(O(1)). 조각 모음을 돌리는 행위는 쓸데없이 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 위치만 바꿔대어 FTL의 막대한 [쓰기 증폭](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/)(WA)을 유발하고, 하루 만에 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 수명 1년 치를 날려버리는 최악의 학대 행위다. 윈도우 등 현대 OS는 SSD를 감지하면 조각 모음 기능 자체를 강제로 막아버린다.

- **📢 섹션 요약 비유**: 순간 이동 마법을 쓰는 마법사([SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))에게, 굳이 물건들을 일렬로 예쁘게 정렬해 놓으라고(조각 모음) 체력을 낭비시키는 꼴입니다. 마법사는 물건이 어딜 박혀있든 1초 만에 가져오므로, 쓸데없이 물건을 옮기라며 마력(수명)을 고갈시켜서는 안 됩니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [Wear Leveling](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/) 부재 ([초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 플래시) | 정적/동적 [Wear Leveling](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/) 적용 시 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (디스크 수명)** | 특정 블록 집중 파괴로 수주~수개월 내 사망 | 모든 블록 마모도 99% 평준화 일치 (수년 생존) | [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 수명 주기(TBW 보증) 수천 배 비약적 상승 |
| **정량 (I/O 퍼포먼스)**| In-place 덮어쓰기 시 지우기(Erase) 대기 발생 | 새 빈 블록 찾아 즉시 기록(Out-of-place) | [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [지연 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)(Write [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)) 마이크로초 보장 |
| <strong>정성 (<a href="/studynote/04_software_engineering/04_testing_quality/198_abstraction_control_data_process/">추상화</a>)</strong> | OS가 배드 블록을 직접 관리해야 함 | OS는 완벽한 무결점 디스크로 착각함 | [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 코드의 단순화 및 범용 OS [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 달성 |

### 미래 전망
- <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/703_zns_ssd/">ZNS</a> (<a href="/studynote/01_computer_architecture/15_advanced_topics/703_zns_ssd/">Zoned Namespace</a>) SSD의 부상</strong>: 웨어 레벨링과 FTL을 컨트롤러에 맡겨놨더니 컨트롤러 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목과 D-RAM 비용이 너무 커졌다. 클라우드 공룡(AWS, Meta)들은 이제 SSD에서 멍청한 FTL을 빼버리고, 호스트 OS [커널](/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 SSD의 플래시 존(Zone)을 직접 통제하여 순차적(Sequential)으로만 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 밀어 넣고 평준화를 직접 지휘하는 <strong><a href="/studynote/01_computer_architecture/15_advanced_topics/703_zns_ssd/">ZNS</a> 기술</strong>로 눈을 돌렸다. [쓰기 증폭](/studynote/02_operating_system/08_storage_and_io_systems/480_write_amplification/)이 사라져 오버 [프로비저닝](/studynote/09_security/11_iam_access_control/528_provisioning/)을 0%로 만들어도 수명이 유지되는 차세대 [데이터센터](/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 스토리지의 표준이 되고 있다.
- <strong>QLC/PLC를 버티는 <a href="/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 기반 평준화</strong>: 하나의 셀에 4비트(QLC), 5비트([PLC](/studynote/09_security/18_iot_ot_physical/896_plc_programmable_logic_controller/))를 구겨 넣으면서 셀 수명이 고작 수백 번 수준으로 곤두박질쳤다. 이를 10년 보증으로 팔기 위해, 단순한 횟수 기반 평준화를 넘어 AI가 유저의 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 패턴을 머신러닝으로 분석해 '차가운 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)'와 '뜨거운 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)'를 물리적으로 분리하는 초정밀 예측형 웨어 레벨링 칩셋이 탑재되고 있다.

### 참고 표준
- <strong><a href="/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/">NVMe</a> (<a href="/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/">Non-Volatile Memory Express</a>)</strong>: 플래시 기반 메모리의 극단적 병렬성과 웨어 레벨링 백그라운드 작업을 호스트 CPU에 방해받지 않고 초고속으로 수행하기 위한 [PCIe](/studynote/01_computer_architecture/09_system_bus_interconnects/356_pcie/) 기반 최신 스토리지 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 표준.
- **JEDEC TRIM / SCSI UNMAP**: 호스트 OS가 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 삭제 시 FTL에게 무효 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 통보하여 쓸데없는 평준화 가비지 컬렉션을 멈추게 하는 글로벌 하드웨어 [명령어](/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 규격.

[플래시 메모리](/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/) [마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)([Wear Leveling](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/))는 "유한한 생명을 가진 소자들의 짐을 어떻게 완벽히 나누어 짊어지게 할 것인가"에 대한 가장 철학적이고 수학적인 해답이다. [운영체제](/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)는 영원불멸의 철판(디스크)이 있다고 믿지만, 그 밑바닥에서는 수십억 개의 플래시 셀들이 각자의 생명력(수명)을 조금씩 내어주며 완벽한 환상(Illusion)을 만들어내고 있다. 가장 나약한 부품들로 가장 강력한 인프라를 직조해 낸 FTL의 평준화 마법이야말로, 현대 [반도체](/studynote/01_computer_architecture/01_basic_electronics_logic/009_semiconductor/) 산업이 이룩한 가장 눈물겨운 속임수이자 예술이다.

- **📢 섹션 요약 비유**: 100명의 군인이 통나무를 메고 행군할 때, 한 명의 어깨가 부서질 때까지 놔두는 게 아니라 초 단위로 어깨를 바꾸어 매게([마모 평준화](/studynote/02_operating_system/08_storage_and_io_systems/479_wear_leveling/)) 함으로써, 가장 약한 병사의 체력으로도 가장 무거운 통나무를 목적지까지 무사히 운반해 내는 완벽한 분배의 마법입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 데드락 희생자 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/) [복구](/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)망 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [역 페이지 테이블](/studynote/02_operating_system/06_memory_management/363_inverted_page_table/) 전역 해시 매핑 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| 다중 큐 [SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 장점 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [오브젝트 스토리지](/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 분리 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[역 페이지 테이블 전역 해시 매핑]
    |
    v
[플래시 메모리 마모 평준화 (Wear Leveling)]
    |
    +---> [다중 큐 SSD NVMe 프로토콜 장점]
    +---> [오브젝트 스토리지 메타데이터 분리]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 스케치북([SSD](/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))에 연필로 글씨를 쓰고 지우개로 1,000번쯤 지우면 종이가 찢어져서 버려야 해요. 이게 [플래시 메모리](/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/)의 수명이에요.
2. 만약 일기를 항상 스케치북 첫 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)(0번 블록)에만 썼다 지웠다 하면, 다른 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)는 다 새것인데 첫 [페이지](/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)만 찢어져서 스케치북 전체를 버려야 하잖아요?
3. 그래서 똑똑한 요정(컨트롤러)이 우리가 일기를 쓸 때마다 "오늘은 1페이지, 내일은 5페이지, 모레는 10페이지"로 몰래 자리를 계속 바꿔줘서 스케치북 모든 장을 골고루 닳게 만들어 오래오래 쓰게 해준답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 771 / 800

<- **이전**: [770. 역 페이지 테이블 전역 해시 매핑 (Inverted Page Table Hash)](/studynote/02_operating_system/11_exam_summary/770_inverted_page_table_hash/)
**다음**: [772. 다중 큐 SSD NVMe 프로토콜 장점 (Multi Queue SSD NVMe Protocol)](/studynote/02_operating_system/11_exam_summary/772_multi_queue_ssd_nvme_protocol/) ->

---
