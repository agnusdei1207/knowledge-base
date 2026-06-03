+++
title = "775. 파티션 MBR GPT 크기 제한 (Partition MBR GPT Size Limit)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 테이블은 하나의 물리적 하드 디스크를 여러 개의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 드라이브(C:, D:)로 쪼갤 때, **어디서부터 어디까지가 어느 드라이브인지 기록해 두는 디스크의 첫 번째 목차([Index](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)) 영역**이다.
> 2. **가치**: 1980년대 만들어진 고전적인 **[MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) ([Master Boot Record](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/))** 방식은 32비트 주소 체계의 한계 때문에 '최대 2TB 디스크 크기'와 '최대 4개의 주 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)'이라는 치명적 족쇄를 가지고 있었다.
> 3. **융합**: 이를 극복하기 위해 등장한 **[GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) (GUID [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Table)**는 64비트 주소 체계를 도입하여 최대 9.4ZB(제타바이트)의 무한에 가까운 용량과 128개의 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 지원하며, [UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/)(통합 확장 [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 인터페이스) 부팅 아키텍처와 결합하여 현대 스토리지의 글로벌 표준이 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 
  - 공장 출고 상태의 깡통 하드 디스크에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓰려면, 먼저 '방([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))'을 만들어야 한다. 방의 크기와 개수를 적어두는 규격이 MBR과 GPT다.
  - **[MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/)**: 디스크의 맨 앞 0번 섹터(512바이트)에 부트 로더 코드와 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 테이블(64바이트)을 욱여넣은 구형 규격.
  - **[GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)**: 고유 [식별자](/knowledge-base/studynote/03_network/06_network_layer_ip/289_identification_flags_fragmentation_offset/)(GUID)를 사용하여 전 세계의 모든 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 겹치지 않는 이름을 갖게 하고, 디스크 맨 앞과 맨 뒤에 테이블을 이중 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)하는 최신 규격.

- **필요성(문제의식)**: 
  - 2010년대 들어 하드 디스크 용량이 3TB, 4TB로 커졌다.
  - 낡은 [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) 방식으로 4TB 디스크를 포맷했더니, OS가 앞부분 2TB만 인식하고 나머지 2TB는 아예 없는 공간(Unallocated) 취급을 해버려 쓸 수가 없었다.
  - **해결책**: "주소(LBA)를 담는 공간이 32비트라서 2TB밖에 못 세는 거구나. 주소 공간을 64비트로 늘린 새로운 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 규격([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))을 만들자!"

  - **[MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/)**: 방이 4개밖에 없는 낡은 아파트 도면. 방 번호를 쓸 수 있는 칸이 작아서, 아파트가 아무리 커져도 최대 2천 층(2TB)까지만 번호를 매길 수 있다. 그 이상 높이 지으면 번호를 못 매겨서 윗층에는 사람이 못 산다.
  - **[GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)**: 방을 128개까지 마음대로 쪼갤 수 있고, 방 번호 칸이 엄청 넓어서 94억 층(9.4 ZB)까지도 번호를 매길 수 있는 최첨단 마천루 빌딩 도면.

- **등장 배경**: 
  - 인텔이 기존 BIOS의 한계를 부수기 위해 만든 EFI(나중의 [UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/)) 규격의 일부로 제정되었다. 디스크 대용량화의 압박으로 인해 윈도우 8 / 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 2.6 시절부터 MBR을 빠르게 대체하기 시작했다.

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                 MBR과 GPT의 디스크 레이아웃(Layout) 구조 비교         │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  [ MBR (Master Boot Record) 레이아웃 ]                        │
  │   LBA 0: [ 부트 코드 (446B) | 파티션 테이블 (64B) | 서명 (2B) ]     │
  │   LBA 1~: [ 파티션 1 (C:) ]                                   │
  │           [ 파티션 2 (D:) ]                                   │
  │           [ 파티션 3 (확장 파티션) ] -> 논리 드라이브 쪼개기 꼼수 사용│
  │   ※ 2TB 이상 공간은 인식 불가! (버려짐)                          │
  │                                                             │
  │  [ GPT (GUID Partition Table) 레이아웃 ]                      │
  │   LBA 0: [ Protective MBR ] (구형 OS가 디스크 덮어쓰는 것 방지용 가짜 MBR)│
  │   LBA 1: [ GPT 헤더 (Primary) ]                             │
  │   LBA 2~33: [ 파티션 엔트리 (128개 지원) ]                      │
  │   LBA 34~: [ 파티션 1 (C:) ]                                  │
  │            [ 파티션 2 (D:) ]                                  │
  │            ...                                              │
  │   LBA End-33: [ 파티션 엔트리 복사본 (Secondary/Backup) ]       │
  │   LBA End: [ GPT 헤더 복사본 ] ◀ 디스크 맨 끝에 백업본 존재! 완벽한 복원력│
  └─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** MBR은 0번 섹터(512바이트)라는 극도로 좁은 단칸방에 부팅 코드와 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 정보를 다 때려 박은 기형적 구조다. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 1개당 16바이트만 할당되어 딱 4개의 주 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)만 만들 수 있었다. 반면 GPT는 공간을 시원시원하게 쓴다. LBA 1번부터 33번까지 무려 32개의 블록을 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 명부로 써서 128개의 방을 만든다. 가장 훌륭한 점은 다이어그램 맨 밑의 "[백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)본(Secondary)"이다. MBR은 0번 섹터가 물리적으로 긁히면 디스크 전체가 증발하지만, GPT는 디스크 맨 끝단에 테이블을 똑같이 복사해 두어 앞쪽이 깨져도 뒤에서 1초 만에 자동 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)(Self-Healing)하는 강력한 [회복](/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/) [탄력성](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/571_resiliency_fault_tolerance_patterns/)(Resilience)을 지녔다.

- **📢 섹션 요약 비유**: MBR은 수첩 첫 장에 연필로 대충 그려놓은 지도라서 물이 젖으면 끝장나고 길도 4개밖에 못 그립니다. GPT는 수첩 앞뒤 표지(양끝)에 코팅해서 붙여둔 정밀 지도로, 앞표지가 찢어져도 뒤표지를 보고 128갈래 길을 안전하게 찾아가는 현대식 내비게이션입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2TB 한계의 수학적 원리 (32비트 LBA의 저주)

도대체 왜 MBR은 2TB(테라바이트)에서 성장이 멈췄을까? 이는 컴퓨터 공학의 고질적인 '변수 크기 설계 미스' 때문이다.

1. **디스크 주소 체계**: 디스크는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 512바이트 크기의 작은 블록(섹터)으로 쪼개서 저장한다. 각 섹터에는 0번, 1번, 2번... 주소(LBA, Logical Block Addressing)가 매겨진다.
2. **MBR의 공간 제약**: MBR의 16바이트 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 레코드 안에는 "이 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 시작하는 섹터 번호"와 "총 섹터 개수"를 적는 칸이 있다. 이 칸의 크기가 하필 **32비트(4바이트)**로 설계되었다.
3. **수학적 한계 계산**: 32비트로 표현할 수 있는 가장 큰 숫자는 $2^{32} = 4,294,967,296$ 개다. 
4. **용량 환산**: `4,294,967,296개 섹터 × 512 바이트/섹터 = 약 2.2조 바이트 = 2.2 TB (테라바이트)`.
5. **결론**: [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) 테이블은 42억 번 섹터까지만 숫자를 셀 수 있다. 4TB 디스크를 사서 84억 번 섹터에 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 쓰려고 해도, [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) 장부에는 그 숫자를 적을 칸이 물리적으로 부족해서 에러가 나는 것이다.

### GPT의 64비트 LBA 확장

GPT는 이 어리석은 실수를 반복하지 않기 위해 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 크기를 기록하는 변수를 **64비트(8바이트)**로 대폭 늘렸다.

- **[GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 한계 계산**: $2^{64}$ 개 섹터 $\times$ 512 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) = 약 **9.4 ZB (제타바이트)**.
- 현재 인류가 생산하는 모든 디스크를 다 합쳐도 도달하기 힘든 천문학적인 용량이다. 우리가 살아있는 동안에는 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 용량 한계를 걱정할 일이 사라졌다.

- **📢 섹션 요약 비유**: 은행 계좌 잔고를 표시하는 전광판이 4자리밖에 없으면(32비트), 돈을 10억을 벌어도 9999원까지만 표시되는(2TB 한계) 끔찍한 에러가 발생합니다. 전광판을 20자리(64비트)로 교체하여 워렌 버핏의 재산도 한 번에 표시할 수 있게 만든 것이 GPT의 핵심입니다.

---

## Ⅲ. 비교 및 연결

### 부팅 아키텍처와의 강제 결합 (BIOS vs [UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/))

MBR과 GPT는 단순한 용량 차이를 넘어, 컴퓨터가 처음 켜지는 부팅(Booting) 아키텍처와 운명 공동체로 묶여 있다.

| [펌웨어](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) 규격 | 호환 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 특징 및 부팅 동작 방식 | 한계점 |
|:---|:---|:---|:---|
| **Legacy BIOS** | **[MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/)** 전용 | 메인보드 칩셋이 디스크의 0번 섹터([MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/))에 있는 446바이트짜리 기계어 코드를 무식하게 읽어서 무조건 실행함. | 코드가 너무 작아 보안 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)([Secure Boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/)) 불가. 부팅 속도 느림. |
| **[UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/)** | **[GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/)** 전용 (표준) | 메인보드가 소형 OS처럼 동작. GPT의 EFI System [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)([ESP](/knowledge-base/studynote/03_network/07_network_layer_routing/382_esp_encapsulating_security_payload_confidentiality/)) 이라는 특정 FAT32 폴더를 읽어 그 안의 `.efi` [부트로더](/knowledge-base/studynote/02_operating_system/01_overview_architecture/029_bootloader/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 우아하게 실행함. | 과거 32비트 윈도우 OS 설치 불가. (무조건 64비트 OS 강제) |

### 과목 융합 관점

- **시스템 보안 ([Secure Boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/))**: [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) 시절에는 해커가 0번 섹터(446바이트)의 부팅 코드를 몰래 변조([Bootkit](/knowledge-base/studynote/09_security/04_endpoint_security/362_bootkit/))하면 백신 프로그램이 켜지기도 전에 OS 권한을 탈취당했다. [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) + [UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) 조합으로 넘어오면서, 메인보드는 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 안에 있는 [부트로더](/knowledge-base/studynote/02_operating_system/01_overview_architecture/029_bootloader/)(`.efi`) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 디지털 서명([RSA](/knowledge-base/studynote/09_security/03_network_security/110_rsa/) Hash)을 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하여, 마이크로소프트나 우분투의 공식 서명이 없는 악성 [부트로더](/knowledge-base/studynote/02_operating_system/01_overview_architecture/029_bootloader/)는 아예 실행을 거부해 버리는 '시큐어 부트' 방어막을 완성할 수 있었다.
- **[가상화](/knowledge-base/studynote/13_cloud_architecture/01_virtualization/015_virtualization/) 및 클라우드 (EBS 볼륨 제약)**: AWS EC2 인스턴스를 만들 때 3TB짜리 디스크(EBS)를 붙이려면 반드시 [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 포맷이어야 한다. 구형 [AMI](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/162_ami_advanced_metering_infrastructure/)(아마존 머신 이미지)가 MBR로 만들어져 있으면 2TB 이상을 확장할 수 없어 디스크 리사이징(Resizing) 작업 시 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 테이블을 GPT로 마이그레이션해야 하는 엄청난 운영 오버헤드가 발생한다.

- **📢 섹션 요약 비유**: 구형 자동차(BIOS)는 차 열쇠 구멍([MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/))에 아무 열쇠나 쑤셔 넣어서 맞으면 무조건 시동이 걸렸지만, 최신 스마트카([UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/))는 스마트키([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))에 담긴 암호 칩([전자 서명](/knowledge-base/studynote/03_network/19_frequent_topics_terms/988_digital_signature/))을 컴퓨터가 분석하여 진짜 주인일 때만 시동을 걸어주는 철통 보안 시스템입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 운영 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

1. **시나리오 — 구형 리눅스 서버 디스크 4TB 증설 후 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 에러**: 10년 된 CentOS 6 장비에 스토리지 용량이 부족해 4TB 디스크를 추가로 꽂고, 평소 쓰던 `fdisk /dev/sdb` 명령어로 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 만들었다. 그런데 화면에 `Value out of range` 경고가 뜨며 2TB만 잡히는 현상 발생.
   - **원인 분석**: `fdisk`는 태생적으로 [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) 전용 구형 [파티셔닝](/knowledge-base/studynote/05_database/03_relational_model/179_table_partitioning_concept/) 도구다. 4TB 디스크에 구형 도구를 들이대니 자동으로 MBR을 그려버렸고 주소 한계에 봉착했다.
   - **아키텍트 판단 ([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 전용 도구 채택)**: 2TB 이상의 디스크를 다룰 때는 낡은 `fdisk`를 버리고 무조건 GPT를 100% 지원하는 **`parted` (최신 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)) 또는 `gdisk` (GNU Parted)** 명령어를 사용해야 한다. `gdisk`로 디스크 라벨을 GPT로 변환하면 4TB 전체를 단일 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)으로 우아하게 통짜 할당할 수 있다.

2. **시나리오 — Protective MBR의 함정**: 엔지니어가 8TB 디스크를 GPT로 포맷해서 쓰다가, 실수로 낡은 윈도우 [XP](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/073_xp_extreme_programming/) 설치 CD를 넣고 부팅했다. 구형 OS가 "어? [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 테이블이 없네?"라며 디스크를 초기화하려 들까 봐 식은땀을 흘렸다.
   - **아키텍트 판단 (하위 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 방어막)**: 다행히 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 날아가지 않았다. [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) 아키텍처는 LBA 0번 위치에 **'Protective [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) (방어용 [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/))'**이라는 가짜 장부를 심어둔다. 낡은 유틸리티나 구형 OS가 이 디스크를 쳐다보면, 가짜 MBR이 "이 디스크 전체(8TB)는 꽉 찬 알 수 없는 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(Type 0xEE) 하나로 되어 있으니 건드리지 마!"라고 거짓말을 한다. 구형 툴은 꽉 찼다는 말에 쫄아서 덮어쓰기를 포기하므로, GPT의 진짜 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 완벽하게 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)된다. 천재적인 하위 [호환성](/knowledge-base/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 꼼수다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 서버 스토리지 파티션 규격 선택을 위한 의사결정 트리         │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ 새로운 물리 디스크 또는 클라우드 블록 스토리지를 붙였다 ]               │
  │                │                                                  │
  │                ▼                                                  │
  │      디스크의 총 용량이 2TB (테라바이트) 를 초과하는가?                     │
  │          ├─ 예 ─────▶ [ 무조건 GPT (GUID Partition Table) 채택! ]  │
  │          │             (MBR 선택 시 나머지 용량 영구 증발)                │
  │          └─ 아니오                                                │
  │                │                                                  │
  │                ▼                                                  │
  │      한 디스크를 5개 이상의 파티션으로 쪼갤 계획이 있는가? (예: Docker 풀)      │
  │          ├─ 예 ─────▶ [ GPT 채택 ]                                │
  │          │             (MBR은 논리 드라이브 꼼수를 써야 해서 마운트 꼬임 위험)│
  │          └─ 아니오                                                │
  │                │                                                  │
  │                ▼                                                  │
  │      구형 레거시 장비(Legacy BIOS 전용 보드)의 부팅용(OS 설치) 디스크인가?    │
  │          ├─ 예 ─────▶ [ 어쩔 수 없이 MBR (Master Boot Record) 채택 ]│
  │          │                                                        │
  │          └─ 아니오 ──▶ [ 모든 현대 시스템은 GPT를 기본값(Default)으로! ]│
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 인프라 아키텍트에게 2TB는 마지노선(Threshold)이다. 요즘 시대에 MBR을 고집할 이유는 "10년 전 박물관에 가야 할 서버 보드를 부팅시킬 때"뿐이다. 클라우드의 시대, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 스케일이 페타바이트를 논하는 시대에는 GPT가 공기와 같은 표준이다. 특히 리눅스의 LVM([논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 볼륨 매니저)을 올릴 때 밑바탕의 피지컬 볼륨([PV](/knowledge-base/studynote/12_it_management/04_sdlc_testing/153_pv_planned_value/)) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 짤 때 반드시 GPT를 써두어야 나중에 디스크 용량을 무중단으로 확장(Extend)할 때 LBA 주소 제한에 걸려 서버를 밀어야 하는 최악의 사태를 막을 수 있다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **단일 디스크에 무분별한 다중 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 쪼개기**: "C드라이브는 OS용, D드라이브는 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)용, E드라이브는 앱용..." 이런 식으로 물리 디스크 1개를 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 5~6개로 하드코딩해서 쪼개는 구시대적 윈도우 습관. 운영하다 보면 무조건 어느 한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(특히 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))의 용량이 100% 꽉 차서 장애가 난다. 현대 리눅스 인프라에서는 **전체 디스크를 GPT로 통짜 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 1개만 잡고, 그 위에 LVM(Logical [Volume](/knowledge-base/studynote/14_data_engineering/01_infrastructure/001_bigdata_3v_5v/) Manager)을 올려 소프트웨어적으로 볼륨을 고무줄처럼 유연하게 늘리고 줄이는 것**이 정석이다.

- **📢 섹션 요약 비유**: 큰 땅(디스크)에 벽돌로 담([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))을 쌓아 방을 나누면 나중에 방 크기를 바꿀 때 벽을 다 부숴야 합니다([안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)). 대신 땅 전체에 큰 운동장(통짜 [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/))을 하나 만들고, 그 위에 언제든 옮길 수 있는 칸막이 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(LVM)을 치는 것이 스마트한 오피스 설계입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/) ([Master Boot Record](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/)) | [GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/) (GUID [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Table) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (최대 용량)** | 2.2 TB (테라바이트) 한계 | **9.4 ZB (제타바이트)** 무한대 | 빅데이터 스토리지, [RAID](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 어레이 단일 볼륨 맵핑 완벽 지원 |
| **정량 ([파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 개수)** | 기본 주 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 4개 (확장 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 필요) | **기본 128개** (무한 확장 가능) | 복잡한 멀티 부팅 및 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 격리 아키텍처 수용 |
| **정성 ([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 및 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/))**| 단일 테이블 파괴 시 디스크 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영구 유실 | 헤더 [이중화](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/456_dual_redundancy/) 및 CRC32 [체크섬](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/112_checksum/) 해시 내장 | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 훼손 시 끝단 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/)본(Secondary)을 통한 자가 치유(Self-Healing) |

### 미래 전망
- **[NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/)([Namespace](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/))와의 결합**: 스토리지 용량이 30TB, 100TB로 진화하면서 소프트웨어적 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))을 넘어서, [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) 컨트롤러 칩 자체에서 하드웨어적으로 용량을 완전히 찢어버리는 [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) 분할 기술이 등장했다. GPT는 이 찢어진 하드웨어 영역 위에서 각자의 OS를 부팅시키는 마이크로 레이아웃으로 역할이 한 단계 더 추상화되고 있다.
- **블록 스토리지의 종말과 [ZNS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/703_zns_ssd/)**: 미래의 [플래시 메모리](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/)([ZNS](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/703_zns_ssd/))는 LBA 블록 구조 자체를 혐오한다. 블록을 무작위로 쪼개는 행위가 [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 수명을 깎기 때문이다. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 테이블을 앞/뒤에 박아두는 고전적 샌드위치 구조는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 연속 기록(Sequential Write)을 방해하므로, 차세대 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템에서는 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 테이블 개념조차 희미해지고 통짜 객체(Object) 맵핑으로 진화할 가능성이 높다.

### 참고 표준
- **[UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) (Unified Extensible [Firmware](/knowledge-base/studynote/02_operating_system/01_overview_architecture/032_firmware/) Interface) [Specification](/knowledge-base/studynote/04_software_engineering/03_design_architecture/148_requirements_specification_formal_informal/)**: 인텔 주도로 만들어진 포럼에서 GPT의 디스크 레이아웃 [바이트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 구조(LBA 0~34)를 명확히 정의한 국제 규격.
- **LBA (Logical Block Addressing)**: 디스크의 물리적 실린더/헤드/섹터(CHS)의 복잡성을 버리고, 0번부터 N번까지 1차원 배열로 디스크를 평평하게(Flat) 다루는 현대 스토리지의 기본 주소 체계.

디스크 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 규격의 진화는 "변수 크기를 너무 아끼면 훗날 재앙을 맞는다"는 컴퓨터 공학의 가장 뼈아픈 [교훈](/knowledge-base/studynote/09_security/13_secops_ir_forensics/659_ir_lessons_learned/)(Y2K 버그의 디스크 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/))이다. 1983년에 만들어진 MBR은 32비트면 영원히 충분할 줄 알았으나, 불과 30년 만에 터져나온 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 폭주 앞에 무릎을 꿇었다. GPT는 64비트의 광활한 주소 공간과 [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) 테이블이라는 선견지명을 통해, 인류가 멸망하는 그날까지 디스크 용량 한계를 걱정할 필요 없는 영원한 평화를 인프라 세계에 가져다주었다.

- **📢 섹션 요약 비유**: 우편번호를 3자리([MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/))로 만들어서 동네가 커지자 번호가 고갈돼 대혼란이 일어난 것을 반면교사 삼아, 우편번호를 아예 20자리([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))로 만들어 지구뿐만 아니라 우주 식민지의 모든 집 주소까지 겹치지 않게 완벽히 대비해 둔 천재적인 행정 개편입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [오브젝트 스토리지](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/494_object_storage/) [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 분리 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [네트워크 파일 시스템](/knowledge-base/studynote/02_operating_system/11_exam_summary/774_nfs_stateless_network_file_system/) ([NFS](/knowledge-base/studynote/02_operating_system/09_file_system/543_nfs_network_file_system/)) 무상태 ([Stateless](/knowledge-base/studynote/15_devops_sre/05_devsecops/239_stateless_redis/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [클라우드 컴퓨팅](/knowledge-base/studynote/02_operating_system/01_overview_architecture/052_cloud_computing_os/) OS [자원 풀링](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/638_resource_pooling_cxl/) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러 [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/) [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[네트워크 파일 시스템 (NFS) 무상태 (Stateless)]
    │
    ▼
[파티션 MBR GPT 크기 제한 (Partition MBR GPT Size Limit)]
    │
    ├──▶ [클라우드 컴퓨팅 OS 자원 풀링]
    └──▶ [OOM 킬러 메모리 보호 정책]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 낡은 아파트 도면([MBR](/knowledge-base/studynote/02_operating_system/09_file_system/515_mbr_vs_gpt/))은 방 번호를 적는 칸이 너무 작아서 최대 2천 층(2TB)까지만 방을 만들 수 있었어요. 그 이상 지으면 번호를 못 매겨서 버려졌죠.
2. 하지만 최신 마천루 도면([GPT](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/302_gpt_autoregressive/))은 방 번호 칸이 엄청 넓어서 우주 끝까지 층을 쌓아도(9.4ZB) 다 번호를 매길 수 있어요!
3. 게다가 낡은 도면은 찢어지면 끝이지만, 최신 도면은 건물 맨 꼭대기(디스크 끝)에 복사본을 몰래 숨겨놔서 앞부분이 찢어져도 1초 만에 완벽하게 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)해 내는 마법을 쓴답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 775 / 800

← **이전**: [774. 네트워크 파일 시스템 (NFS) 무상태 (Stateless)](/knowledge-base/studynote/02_operating_system/11_exam_summary/774_nfs_stateless_network_file_system/)
**다음**: [776. 클라우드 컴퓨팅 OS 자원 풀링 (Cloud Computing Resource Pooling)](/knowledge-base/studynote/02_operating_system/11_exam_summary/776_cloud_computing_resource_pooling/) →

---
