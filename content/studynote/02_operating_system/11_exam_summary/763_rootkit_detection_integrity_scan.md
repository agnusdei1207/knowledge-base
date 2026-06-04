+++
title = "763. 루트킷 탐지 무결성 스캔 (Rootkit Detection Integrity Scan)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)([Rootkit](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/))은 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(Ring 0)의 가장 깊은 곳을 장악하여 백신 프로그램의 눈을 속이고 자신의 존재를 시스템에서 완전히 투명하게 지워버리는 은닉형 악성코드다. 이를 탐지하는 유일한 방패가 <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> 스캔(<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">Integrity</a> Scan)</strong>이다.
> 2. **가치**: [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)에 감염되면 `ls`, `ps`, `netstat` 등 관리자가 맹신하던 모든 기본 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)들의 출력 결과가 조작된 거짓말이 되므로, OS를 절대 믿지 않고 외부의 수학적 해시(SHA-256) 암호화 서명이나 격리된 오프라인 스캐너를 통해 진실을 밝혀내는 철학적 전환을 제공한다.
> 3. **융합**: 과거 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 용량이나 수정 시간(Timestamp)만 보던 1차원적 탐지에서 벗어나, 현대에는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 시스템 콜 테이블 후킹 감지, [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 런타임 행동 분석, 하드웨어 [TPM](/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/476_tpm/) 칩을 연동한 시큐어 부트([Secure Boot](/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/)) 등 하드웨어-OS 융합 보안 체계로 진화했다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
  - <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/">루트킷</a> (<a href="/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/">Rootkit</a>)</strong>: 시스템 최고 관리자 권한(Root)을 영구적으로 탈취한 뒤, 해커의 [백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 실행 중인 악성 프로세스, 열려있는 해킹 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/)를 감춰주는(Cloaking) 특수 목적 악성코드 세트다.
  - <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> 스캔 (<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">Integrity</a> Scan)</strong>: 시스템의 중요 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이나 메모리 구조가 '허가되지 않은 자에 의해 변조되지 않고 깨끗한 원본 상태를 유지하고 있음'을 암호학적으로 증명하고 대조하는 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) 행위다.

- **필요성(문제의식)**:
  - 해커가 서버를 뚫고 [백도어](/knowledge-base/studynote/03_network/14_network_security_threats/737_backdoor_c2_beacon_behavior_analysis/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 심었다. 관리자가 `ls` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)로 폴더를 뒤져본다.
  - 그런데 [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)이 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 목록 읽기 함수([System Call](/knowledge-base/studynote/02_operating_system/01_overview_architecture/013_system_call/))를 조작해서, 해커 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 이름이 나오면 화면에 출력되지 않게 빼버린다. 관리자 눈에는 서버가 평온해 보인다.
  - **해결책**: "감염된 OS가 들려주는 정보는 모조리 사기다! 오염 불가능한 외부의 깨끗한 기준([Baseline](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) Hash DB)을 만들어두고, 1바이트라도 변경되면 즉시 알람을 울리는 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 감시자(Tripwire)를 배치하자!"

  - <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/">루트킷</a> 감염</strong>: 미술관 경비원(백신)이 [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/) 화면을 열심히 보고 있는데, 해커([루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/))가 이미 카메라 렌즈 앞에 '아무 일 없는 텅 빈 복도' 사진을 붙여놓은 상태. 경비원은 화면만 보고 "안전하다"고 착각함.
  - <strong><a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> 스캔</strong>: 화면을 믿지 못하는 관장이 매일 밤 12시에 직접 레이저 스캐너를 들고 복도로 걸어 나가, 어제 바닥에 찍어둔 지문 해시(Hash) 패턴과 오늘 바닥의 패턴이 단 1mm라도 달라진 게 없는지 암호학적으로 검사하는 치밀한 행위.

- **등장 배경**:
  - 1990년대 해커들이 유닉스 환경의 `login`, `ps` 같은 기본 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 바이너리 자체를 덮어쓰는 1세대 [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)([User-mode Rootkit](/knowledge-base/studynote/09_security/04_endpoint_security/361_user_mode_rootkit/))을 유행시켰고, 2000년대 [LKM](/knowledge-base/studynote/02_operating_system/01_overview_architecture/067_lkm/)([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/))을 악용한 2세대 [커널 루트킷](/knowledge-base/studynote/09_security/04_endpoint_security/360_kernel_rootkit/)(Kernel-mode [Rootkit](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/))이 판을 치자, 이에 맞서 Tripwire, AIDE 같은 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 감시 도구들이 엔터프라이즈 보안의 표준으로 정착했다.

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                 루트킷의 은닉(Cloaking) 원리와 무결성 탐지 구조       │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  [ 1. 루트킷이 관리자의 눈을 멀게 하는 원리 (System Call 후킹) ]    │
  │                                                             │
  │   관리자: `$ ps` (프로세스 목록 좀 보여줘)                     │
  │        │                                                    │
  │        ▼                                                    │
  │   [ 😈 루트킷이 장악한 커널 테이블 (sys_call_table) ]            │
  │   원래 `sys_getdents` 주소 대신 ──▶ [ 해커의 가짜 함수 ]로 점프!  │
  │        │                              │ (해커의 프로세스 ID=99 삭제)│
  │        ▼                              ▼                     │
  │   진짜 프로세스 목록 가져옴 ──▶ (필터링 후 조작된 찌꺼기 리턴) ──▶ 관리자 騙│
  │                                                             │
  │  [ 2. 무결성 스캐너 (AIDE / Tripwire)의 방어 원리 ]             │
  │                                                             │
  │   ┌── 안전 금고 (Offline DB) ───────────────┐               │
  │   │ 원본 `/bin/ps` 의 SHA-256 해시: a1b2... │               │
  │   └─────────────────────────────────────────┘               │
  │        ▲ 대조 (Match?)                                      │
  │        │                                                    │
  │   무결성 스캐너 (자체 엔진으로 직접 디스크 바이너리 스캔)             │
  │        ▼ 해시 재계산                                          │
  │   현재 `/bin/ps` 의 SHA-256 해시: x9y8... (다름! 변조됨!)        │
  │                                                             │
  │   ▶ 결과: 루트킷이 파일 크기와 수정 날짜(Timestamp)를 똑같이 위조해도, │
  │           내용이 1바이트라도 바뀌면 해시값이 완전히 틀어져 무조건 적발됨! │
  └─────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 그림 상단은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨 [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)의 고전적인 수법인 '시스템 콜 후킹(Hooking)'을 보여준다. OS의 모든 정보는 결국 시스템 콜 관문(Table)을 통과해야 하므로, 이 문지기를 해커 매수로 매수해 버리면 OS 위에서 도는 모든 백신과 모니터링 도구는 조작된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(눈먼 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))만 받게 된다. 이 은폐막을 뚫는 유일한 방법이 하단의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 해시 스캔이다. 해커가 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 날짜와 크기를 똑같이 위조하는 '타임스톰핑(Timestomping)' 기술을 써도, [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 내부 기계어 1비트의 변화가 발생하면 [해시 함수](/knowledge-base/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/)(SHA-256)의 성질(눈사태 효과)에 의해 해시값이 완전히 달라져 버린다. 수학은 절대 거짓말을 하지 않기 때문에 [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)을 완벽히 색출할 수 있다.

- **📢 섹션 요약 비유**: 마피아가 경찰서장([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))을 매수해서 동네 범죄 기록을 다 지워버리면 일반 순경(백신)들은 알 길이 없습니다. 하지만 정부 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)관([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캐너)이 예전에 경찰서장 몰래 본부에 복사해 둔 '절대 장부 해시값'을 들고 내려와 현재 장부와 대조하면, 서장의 거짓말이 100% 폭로되는 강력한 감찰 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캔 파이프라인 아키텍처

Tripwire, OSSEC 등 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 감시 도구(FIM, [File](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [Integrity](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) Monitoring)의 표준 동작 주기는 다음과 같다.

1. <strong><a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/">기준선</a>(<a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/">Baseline</a>) <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/">생성</a> (가장 중요!)</strong>: 서버를 처음 설치하고 인터넷을 연결하기 직전의 '가장 깨끗한(Pristine) 상태'에서 OS 핵심 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)들(`/etc/passwd`, `/bin/ls`, [부트로더](/knowledge-base/studynote/02_operating_system/01_overview_architecture/029_bootloader/) 등)의 해시([MD5](/knowledge-base/studynote/03_network/13_network_security_basics/668_md5_hash_collision_vulnerability/)/SHA)와 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 속성을 쫙 뽑아내어 암호화된 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)베이스에 저장한다.
2. **오프라인/Read-Only 보관**: 이 [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) DB [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)마저 [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)이 변조하면 끝장이므로, DB [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 방지(Read-Only) [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)(CD-ROM, 결합된 S3 버킷)나 별도의 중앙 로깅 서버로 빼돌린다.
3. **주기적 무작위 스캔**: 스케줄러가 매일 밤, 혹은 랜덤한 시간에 깨어나 현재 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템의 중요 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 해시를 다시 맹렬하게 계산한다.
4. **편차(Deviation) 경고**: [기준선](/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/) 해시와 1비트라도 다른 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 발견되면, 시스템 관리자에게 즉시 Pager/이메일을 쏘고 해당 서버를 네트워크에서 강제 격리(Quarantine)시킨다.

### [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)의 메모리 은닉 기법과 동적 탐지 (Volatility)

해커들도 진화하여, 디스크에 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 남기지 않고 <strong>오직 RAM (메모리) 위에만 존재하는 Fileless <a href="/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/">루트킷</a>(메모리 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/480_injection/">인젝션</a>)</strong>을 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 시작했다. 디스크 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캐너는 메모리 위의 유령을 잡을 수 없다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 Direct Kernel Object Manipulation (DKOM) 탐지 원리    │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   [ 해커의 DKOM 은닉 수법 (연결 리스트 조작) ]                          │
  │                                                                   │
  │   OS의 프로세스 관리 리스트 (task_struct Double Linked List)          │
  │                                                                   │
  │   [PID 100] ◀──▶ [PID 101(해커)] ◀──▶ [PID 102]                  │
  │         └─────────────── (건너뛰기) ───────────────┘                  │
  │                                                                   │
  │   ※ 해커가 커널 메모리를 직접 조작하여, 100번이 102번을 가리키게 포인터만 뺌. │
  │   ※ 101번은 스케줄러 큐에 남아 실행은 되지만, 관리 리스트에는 없어서 투명해짐! │
  │                                                                   │
  │   [ 메모리 포렌식 도구(Volatility)의 교차 검증 탐지 ]                     │
  │                                                                   │
  │   1. 시점 1: 조작된 커널 리스트를 따라가며 PID 수집 -> [100, 102] 발견     │
  │   2. 시점 2: 메모리를 바이트 단위로 풀스캔(Carving)하여 `task_struct`의   │
  │             특정 시그니처(Magic Number)를 무식하게 다 찾아냄.            │
  │             -> 메모리 바닥에서 [100, 101, 102] 3개 덩어리 발견!         │
  │                                                                   │
  │   ▶ 교차 비교: "어? 정상 리스트엔 없는데 메모리 바닥엔 101번이 숨어있네?"      │
  │             -> 🚨 루트킷(DKOM) 은닉 100% 탐지 성공!                   │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 이것은 OS 해킹의 최고봉인 DKOM(직접 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 객체 조작)과 이를 잡는 [메모리 포렌식](/knowledge-base/studynote/09_security/13_secops_ir_forensics/665_memory_forensics/)의 쫓고 쫓기는 추격전이다. 해커는 시스템 콜 테이블을 건드리는 게 너무 잘 걸리자, 아예 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 자료구조 포인터 선을 끊어서(Unlink) OS의 정상적인 명부에서 자기 프로세스를 지워버렸다. 명부에 없으니 `ps` [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 당연히 해커를 못 본다. 방어자(Volatility 등 메모리 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캐너)는 OS가 주는 엑셀 명부 따위는 쓰레기통에 버리고, <strong>램(RAM) 덤프 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a> 전체를 1바이트씩 노가다로 훑어가며(Memory Carving) 프로세스 구조체 모양을 가진 덩어리</strong>를 싹 다 건져 올린다. 그리고 두 결과를 [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/)(Cross [View](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/))하여 숨겨진 투명 프로세스를 멱살 잡아 끌어낸다.

- **📢 섹션 요약 비유**: 해커가 학교 출석부에서 자기 이름만 화이트로 몰래 지워버려서(DKOM), 선생님이 출석부를 부를 땐 해커가 없는 것처럼 보입니다. 하지만 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 교장 선생님이 출석부 대신 직접 교실 문을 잠그고 머릿수([메모리 풀](/knowledge-base/studynote/02_operating_system/06_memory_management/369_memory_pool/) 스캔)를 하나하나 다 세어본 뒤 출석부 이름 개수와 비교하여 숨어있던 유령 학생을 잡아내는 기법입니다.

---

## Ⅲ. 비교 및 연결

### 백신([Anti-Virus](/knowledge-base/studynote/09_security/04_endpoint_security/323_antivirus/)) vs [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 감시(FIM) vs [메모리 포렌식](/knowledge-base/studynote/09_security/13_secops_ir_forensics/665_memory_forensics/) 비교

서버 아키텍처를 지키는 3중 방어막의 역할 분담이다.

| 방어 도구 체계 | 탐지 대상 및 타겟 | 핵심 탐지 원리 메커니즘 | 치명적 한계점 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/09_security/04_endpoint_security/323_antivirus/">Anti-Virus</a> (전통적 백신)</strong> | 알려진 일반 악성코드, [트로이목마](/knowledge-base/studynote/09_security/15_malware_attack_vectors/726_trojan_horse/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) | 블랙리스트(시그니처 패턴 매칭). 나쁜 놈 DB와 대조. | <strong><a href="/knowledge-base/studynote/09_security/15_malware_attack_vectors/761_zero_day/">제로데이</a>(0-day)</strong> 공격이나 처음 보는 변종 [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)은 절대 잡지 못함. |
| <strong>FIM (<a href="/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/">무결성</a> 스캐너, Tripwire)</strong>| 시스템 핵심 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 환경 [설정](/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 바이너리 | 화이트리스트(해시 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)). 1바이트라도 원본과 다르면 알람. | <strong>메모리(RAM) 위에서만 도는 <a href="/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>리스(Fileless) 공격</strong>은 탐지 불가. |
| <strong><a href="/knowledge-base/studynote/09_security/13_secops_ir_forensics/665_memory_forensics/">Memory Forensics</a> (Volatility)</strong>| [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 자료구조, 은닉된 프로세스 및 [포트](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/446_port_and_bus/) | 크로스 뷰(Cross-[view](/knowledge-base/studynote/05_database/03_relational_model/151_sql_view_virtual_table/)) 분석. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [API](/knowledge-base/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 결과와 실제 램 바닥 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [교차 검증](/knowledge-base/studynote/10_ai/03_llm_nlp/250_cross_validation_kfold/). | 실시간 라이브 차단이 어려움. 장애 발생 후 램 덤프를 떠서 사후 분석해야 함. |

### 과목 융합 관점

- <strong>하드웨어 구조 (<a href="/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/">Secure Boot</a> 및 <a href="/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/476_tpm/">TPM</a>)</strong>: 가장 악질적인 [부트킷](/knowledge-base/studynote/09_security/04_endpoint_security/362_bootkit/)([Bootkit](/knowledge-base/studynote/09_security/04_endpoint_security/362_bootkit/))은 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 켜지기도 전인 MBR이나 [UEFI](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/706_uefi/) 단계에서 먼저 실행되어 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캐너 자체를 바보로 만든다. 이를 막기 위해 메인보드의 <strong><a href="/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/476_tpm/">TPM</a>(<a href="/knowledge-base/studynote/01_computer_architecture/14_hardware_security_trends/476_tpm/">Trusted Platform Module</a>)</strong> 칩과 결합된 <strong>시큐어 부트(<a href="/knowledge-base/studynote/02_operating_system/10_security/608_secure_boot/">Secure Boot</a>)</strong>가 도입되었다. 부트 로더 $\rightarrow$ [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) $\rightarrow$ OS 드라이버로 이어지는 모든 부팅 체인 단계마다 전자 서명의 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 하드웨어 레벨에서 암호학적으로 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)하여 서명이 다르면 컴퓨터를 아예 켜주지 않는 최후의 하드웨어/OS 융합 방패다.
- <strong>클라우드 <a href="/knowledge-base/studynote/04_software_engineering/11_testing_validation/513_container_security/">컨테이너 보안</a> (<a href="/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/">Immutable Infrastructure</a>)</strong>: Docker나 Kubernetes의 철학인 "[불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)([Immutable](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/298_immutable/))" 자체가 완벽한 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 방어 전략이다. [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) 내부의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 하나라도 변조되면([루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/) 감염 시도), 관리자는 그 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)이 뭔지 스캔하고 고치는 수고를 하지 않는다. 그냥 <strong>그 <a href="/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/">컨테이너</a>를 죽여버리고(Kill) 새롭고 깨끗한 100% 무결점 이미지를 0.1초 만에 새로 찍어낸다.</strong> [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캔을 넘어선 클라우드식 "[무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 파괴 후 리셋" 철학이다.

- **📢 섹션 요약 비유**: 구형 백신이 수배 전단(블랙리스트)을 들고 길거리에서 지명수배자를 찾는 경찰이라면, [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캔은 매일 아침 성벽(OS)의 금이 간 곳이 없는지 벽돌 하나하나를 두드려보는 순찰병이고, 클라우드 [불변 인프라](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/204_immutable_infrastructure_configuration_drift_prevention/)는 성벽에 금이 가면 1초 만에 새 성벽을 복사해 덮어씌워 버리는 마법입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 인프라 보안 튜닝

1. **시나리오 — 금융권 서버망의 Tripwire 알람 폭주 (False Positive)**: 보안 규제([ISMS](/knowledge-base/studynote/09_security/17_framework_compliance/836_iso_27001_isms/), PCI-DSS) 때문에 1,000대의 리눅스 서버에 Tripwire를 설치했다. 그런데 개발팀이 새벽에 애플리케이션 코드를 배포하거나 리눅스 `yum update`를 칠 때마다 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 해시가 싹 바뀌어 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 알람이 수만 건씩 쏟아지는 양치기 소년 사태가 터졌다.
   - <strong>아키텍트 판단 (<a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/">CI</a>/CD 파이프라인 연동 및 예외 튜닝)</strong>: [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캐너는 시스템 변경의 '합법성'을 모른다. 아키텍트는 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/090_configuration_item/)/CD 파이프라인 배포 프로세스 내에 Tripwire의 <strong><a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/025_baseline/">Baseline</a> 자동 갱신(Update) 스크립트</strong>를 삽입하여, [젠킨스](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)([Jenkins](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/071_jenkins_ci_cd_pipeline_automation/)) 배포 직후에만 잠시 합법적 해시 갱신을 허용하는 아키텍처를 연동해야 한다. 또한 자주 바뀌는 `/var/log`나 `/tmp` 폴더는 애초에 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캔 범위에서 제외(Exclude)하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 최적화를 해야 보안팀이 피로에 지쳐 진짜 알람을 무시하는 인적 재난을 막을 수 있다.

2. <strong>시나리오 — <a href="/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a> 기반의 차세대 런타임 보안 도입</strong>: 디스크 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캔(정적 방어)만으로는 메모리에서 실행되는 익스플로잇이나 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 바이패스 공격을 막기 부족해졌다. 보안팀이 실시간 차단 솔루션을 요구한다.
   - <strong>아키텍트 판단 (<a href="/knowledge-base/studynote/03_network/16_data_center_cloud/825_cilium_ebpf_kubernetes_networking_security/">Cilium</a> Tetragon / Falco 도입)</strong>: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)([LKM](/knowledge-base/studynote/02_operating_system/01_overview_architecture/067_lkm/))을 이용한 보안 도구는 오히려 OS 패닉을 유발할 수 있다. [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 소스를 수정하지 않고도 시스템 콜 훅(Hook)을 마이크로초 단위로 추적할 수 있는 최첨단 <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/">eBPF</a>(Extended <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/069_ebpf/">BPF</a>)</strong> 기반의 런타임 보안 도구를 배포한다. 만약 Nginx 프로세스가 갑자기 쉘(`/bin/bash`)을 실행하려 하거나, `chmod` 권한을 몰래 바꾸려는 비정상 행위(Behavior)를 시도하면, [eBPF](/knowledge-base/studynote/02_operating_system/10_security/615_ebpf/) 엔진이 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 레벨에서 즉각 그 시스템 콜을 차단하고 프로세스를 죽여(Kill) [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)의 활동 자체를 마비시킨다.

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │                 OS 계층별 안티-루트킷(Anti-Rootkit) 방어 스택 설계도        │
  ├───────────────────────────────────────────────────────────────────┤
  │                                                                   │
  │   1. [ 펌웨어 레벨 (Ring -1) ] : 부트킷/펌웨어 변조 방어                   │
  │       - 조치: 메인보드 UEFI Secure Boot 활성화, TPM 하드웨어 칩 결합       │
  │               (OS 부트로더의 해시 서명이 안 맞으면 아예 부팅 거부)             │
  │                                                                   │
  │   2. [ 커널 레벨 (Ring 0) ] : 커널 모듈/LKM 루트킷 방어                    │
  │       - 조치: 커널 파라미터 `modules_disabled=1` 설정 (모듈 적재 원천 차단) │
  │               커널 모듈 서명(Signed Module) 의무화 강제 적용              │
  │                                                                   │
  │   3. [ 런타임 행동 분석 (eBPF) ] : 메모리 은닉(DKOM)/파일리스 방어            │
  │       - 조치: Falco 등 도입하여 허가되지 않은 시스템 콜 호출 실시간 차단        │
  │                                                                   │
  │   4. [ 파일 시스템 레벨 (Ring 3) ] : 바이너리 변조/백도어 방어              │
  │       - 조치: AIDE, Tripwire를 통한 매일 자정 크론탭 무결성 해시 스캔        │
  └───────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/) 방어는 절대 단일 솔루션으로 불가능한 '심층 방어([Defense in Depth](/knowledge-base/studynote/09_security/01_intro_principles/012_defense_in_depth/))'의 결정체다. 4번 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 스캔만 맹신하면 이미 2번 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 장악한 [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)의 눈속임에 당한다. 1번 펌웨어부터 4번 유저 스페이스까지 이어지는 트러스트 체인(Chain of Trust)을 설계하는 것이 아키텍트의 임무다. 특히 운영 중인 서버라면 함부로 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)이 꽂히지 못하게 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 파라미터(sysctl)로 아예 `insmod` 기능을 잠가버리는(modules_disabled) 하드코어한 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 하드닝(Hardening) 결단도 필요하다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **스캔 DB를 동일 서버 내에 평문으로 방치**: [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/)을 검사하는 엔진 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)(Tripwire 실행 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/))과 기준이 되는 원본 해시 DB([Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/)) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 대상 서버의 루트 디렉터리에 아무 암호화 없이 그냥 놔두는 짓. 고도로 숙련된 [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)은 이 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) DB [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 자체를 찾아내어 해커 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)의 해시값으로 업데이트(조작)해 버린다. [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) DB는 반드시 외부 로깅 서버에 있거나 하드웨어적인 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 방지(Read-Only)가 적용된 [매체](/knowledge-base/studynote/03_network/03_physical_layer_media/121_transmission_media_guided_unguided/)에 격리 보관해야 한다.

- **📢 섹션 요약 비유**: 적군([루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/))이 쳐들어오는지 감시하라고 파수꾼([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캐너)을 세워놨는데, 파수꾼이 보는 '아군 얼굴 명부(DB)' 책자를 아무나 수정할 수 있게 성벽 위에 던져두면([안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)), 적군이 몰래 자기 얼굴을 명부에 그려 넣고 유유히 성문을 통과하게 됩니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캔 부재 환경 | 복합 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 아키텍처 도입 | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (은닉 탐지율)**| [커널 루트킷](/knowledge-base/studynote/09_security/04_endpoint_security/360_kernel_rootkit/) 및 [파일리스 공격](/knowledge-base/studynote/09_security/15_malware_attack_vectors/769_fileless_attack/) 0% 탐지 | 1바이트 변조도 SHA-256 대조로 100% 탐지 | 오탐/미탐 없는 수학적(수치적) 악성코드 색출률 달성 |
| <strong>정성 (침해 <a href="/knowledge-base/studynote/09_security/01_intro_principles/009_incident_response/">사고 대응</a>)</strong>| 해킹 후 어디까지 털렸는지 파악 불가, 전체 포맷 | 변조된 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 리스트(diff) 즉시 확보 | 포렌식 조사 기간 수 개월 -> 수 분 단축 및 타겟 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
| **정성 (규제 준수)** | 금융/공공 기관 [ISMS](/knowledge-base/studynote/09_security/17_framework_compliance/836_iso_27001_isms/) 보안 심사 탈락 | 시스템 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 유지 항목 완벽 소명 | 엔터프라이즈 인프라의 대외 보안 [신뢰도](/knowledge-base/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/)([Compliance](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/058_it_compliance_sox_basel_gdpr_isms/)) 증명 |

### 미래 전망
- <strong><a href="/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/">AI</a> 융합 변종 <a href="/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/">루트킷</a>과 <a href="/knowledge-base/studynote/09_security/04_endpoint_security/324_behavior_based_detection/">행위 기반 탐지</a></strong>: 기존 [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 테이블을 수정하는 뻔한 수법을 썼지만, 최근에는 AI를 탑재해 탐지 도구가 스캔할 때는 정상처럼 행동하다 스캔 주기가 끝나면 다시 악성 행위를 하는 회피형 [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)이 등장했다. 이를 잡기 위해 해시(정적) 스캔뿐만 아니라, 시스템 콜 호출 패턴을 머신러닝으로 분석해 비정상적 행동([Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/) Behavior) 스파이크를 즉시 잡아내는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 결합형 [EDR](/knowledge-base/studynote/09_security/04_endpoint_security/325_edr/)(Endpoint [Detection](/knowledge-base/studynote/09_security/19_ai_advanced_security/961_deepfake_detection/) and Response)이 주류로 자리 잡았다.
- <strong><a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/795_confidential_computing/">기밀 컴퓨팅</a> (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/795_confidential_computing/">Confidential Computing</a>)</strong>: 클라우드 인프라 제공자(AWS, GCP)조차 믿을 수 없는 시대다. 인텔 SGX나 [AMD SEV](/knowledge-base/studynote/09_security/04_endpoint_security/391_amd_sev/) 기술을 이용해 CPU 칩 안에 암호화된 '[보안 엔클레이브](/knowledge-base/studynote/02_operating_system/10_security/666_secure_enclave_trustzone_sgx_tee/)([Secure Enclave](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/790_secure_enclave/))' 메모리 구역을 만들면, 해커가 OS [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 권한(Root)을 통째로 장악하더라도 이 엔클레이브 안의 메모리는 아예 들여다볼 수조차 없다. [루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/)의 권력 한계를 하드웨어 칩으로 억누르는 궁극의 보안 패러다임이다.

### 참고 표준
- <strong>NIST <a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/">SP</a> 800-115</strong>: 기술적 정보 보안 테스팅과 시스템 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 점검에 관한 미국 국립표준기술연구소의 공식 대응 가이드.
- **FIPS 140-2 / 140-3**: 암호화 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)과 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)(SHA 계열 해시 등)을 수행하는 소프트웨어/하드웨어가 지켜야 할 연방 정보 처리 표준.

[루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/) 탐지와 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캔의 역사는 "믿는 도끼에 발등 찍힌다"는 속담의 해커 버전이다. 시스템 관리자의 가장 충직한 심복이었던 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)과 기본 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)들이 해커에게 세뇌당해 관리자의 눈을 가리는 순간, 인프라는 돌이킬 수 없는 파국을 맞는다. [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 스캔은 "나 자신조차 믿지 마라"는 [제로 트러스트](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/)([Zero Trust](/knowledge-base/studynote/02_operating_system/10_security/667_zero_trust_runtime_integrity_measurement/))의 가장 밑바닥 철학을 수학적 해시(Hash)라는 절대 변하지 않는 법칙을 통해 하드코어하게 증명해 내는 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)의 마지막 양심이자 등대다.

- **📢 섹션 요약 비유**: 거울([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)) 속에 비친 내 얼굴이 해커가 씌워놓은 가면([루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/))인지 진짜 내 얼굴인지 구분이 안 갈 때, 거울을 믿지 않고 매일 아침 병원에 가서 내 유전자(DNA 해시값 [무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/))를 검사하여 가짜 나를 판별해 내는 지독하고도 가장 확실한 보안 생존술입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 디바이스 드라이버 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/) 인터페이스 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [인터럽트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/016_interrupt_mechanism/) 처리 상프/하프 메커니즘 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [ASLR](/knowledge-base/studynote/02_operating_system/06_memory_management/374_aslr/) 메모리 레이아웃 난수화 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [SELinux](/knowledge-base/studynote/02_operating_system/10_security/583_selinux/) 보안 강제 [접근 통제](/knowledge-base/studynote/04_software_engineering/06_software_architecture/387_access_control_pattern/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[인터럽트 처리 상프/하프 메커니즘]
    │
    ▼
[루트킷 탐지 무결성 스캔 (Rootkit Detection Integrity Scan)]
    │
    ├──▶ [ASLR 메모리 레이아웃 난수화]
    └──▶ [SELinux 보안 강제 접근 통제]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 아주 똑똑한 도둑([루트킷](/knowledge-base/studynote/02_operating_system/10_security/603_rootkit_syscall_hooking/))이 미술관에 몰래 숨어들어와서, 경비원 아저씨의 [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/) 카메라 렌즈에 '아무도 없는 복도 사진'을 찰싹 붙여놨어요.
2. 경비원 아저씨는 화면만 보고 "아무 일도 없네!"라고 믿어버리죠. 화면(기본 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/))을 완전히 조작당한 거예요.
3. 그래서 깐깐한 미술관장님은 화면을 안 믿고, 매일 자정마다 직접 레이저 스캐너([무결성](/knowledge-base/studynote/09_security/01_intro_principles/003_integrity/) 검사기)를 들고 나가서 어제 바닥에 남겨둔 비밀 암호(해시값)가 지워지진 않았는지 확인해서 도둑을 기어코 잡아낸답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 763 / 800

← **이전**: [762. 인터럽트 처리 상프/하프 메커니즘 (Interrupt Top Bottom Half)](/knowledge-base/studynote/02_operating_system/11_exam_summary/762_interrupt_top_bottom_half/)
**다음**: [764. ASLR 메모리 레이아웃 난수화 (ASLR Memory Layout Randomization)](/knowledge-base/studynote/02_operating_system/11_exam_summary/764_aslr_memory_layout_randomization/) →

---
