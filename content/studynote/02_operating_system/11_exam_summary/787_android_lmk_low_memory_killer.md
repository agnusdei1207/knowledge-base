+++
title = "787. 안드로이드 LMK (Low Memory Killer) 작동"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 안드로이드 LMK (Low Memory Killer)는 데스크톱 리눅스의 느리고 극단적인 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)([Out of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)) 킬러를 모바일 환경에 맞게 개조하여, <strong>스마트폰의 RAM이 완전히 바닥나기 전에 단계별 <a href="/knowledge-base/studynote/03_network/08_transport_layer/431_ssthresh_slow_start_threshold/">임계치</a>(Threshold)에 따라 가장 안 쓰는 백그라운드 앱부터 미리미리 쳐 죽이는 선제적 방어 메커니즘</strong>이다.
> 2. **가치**: 스왑(Swap) 파티션을 쓸 수 없는 스마트폰의 하드웨어적 한계를 극복하고, 사용자가 무거운 게임을 켜거나 카메라를 실행할 때 "메모리 부족으로 멈추는(Freezing)" 최악의 사용자 경험(UX)을 막기 위해 뒷단에서 희생양 앱들을 소리 없이 암살해 쾌적한 램 공간을 상시 확보한다.
> 3. **융합**: [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)단(LMK 드라이버)의 물리적 메모리 감시망과, 유저단(Activity Manager)의 앱 중요도 평가 점수(OOM_ADJ)가 실시간으로 융합되어, "당장 화면에 보이는 앱은 절대 살리고, 며칠 전 썼던 숨겨진 앱은 가차 없이 죽인다"는 모바일 OS 최고의 트리아지(Triage, 우선순위 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)) 철학을 완성했다.

---

## Ⅰ. 개요 및 필요성

- **개념**:
- 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 기본 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러는 메모리가 1바이트도 남지 않은 <strong>100% 고갈(파산) 상태</strong>가 되어야만 몽둥이를 빼든다. 이 과정에서 시스템은 수 초간 완전히 얼어붙는다(Hang).
- 안드로이드 <strong>LMK (Low Memory Killer)</strong>는 파산하기 전에, 램 잔여량이 20%, 15%, [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 단위의 "경계선(Threshold)" 밑으로 떨어질 때마다 단계적으로 개입하여 미리 정해둔 우선순위(ADJ 점수)가 높은 앱들을 부드럽게 죽여 나가는 스마트 예방 시스템이다.

- **필요성(문제의식)**:
- 안드로이드 스마트폰은 초창기에 램이 512MB, 1GB밖에 안 됐다. 게다가 [플래시 메모리](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/)(eMMC)의 수명과 속도 문제 때문에 하드디스크처럼 [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/)(Swap)를 쓸 수도 없었다.
- 사용자는 카톡을 하다가, 유튜브를 보고, 다시 게임을 켠다. 앱들은 자기가 종료된 줄 알지만 안드로이드는 다음 실행 속도를 위해 이들을 뒤에 "캐시" 상태로 얼려둔 채 램을 갉아먹게 놔둔다.
- 게임(무거운 앱)을 켜는 순간, 램 500MB가 한방에 필요하다. 스왑 공간도 없는데 일반 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러가 돌면 게임이 멈추거나 폰이 재부팅된다.
- **해결책**: "사용자 눈에 안 띄게, 램이 부족할 기미가 보이면 뒤에서 자고 있는 카톡이나 오래된 앱부터 미리미리 목을 쳐서(Kill) 게임이 쓸 넓은 램 500MB를 미리 비워두자!"

- <strong>일반 <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/">OOM</a> 킬러</strong>: 비행기 연료가 100% 바닥나서 엔진이 꺼지기 직전 1초에, 가장 무거운 짐 하나를 버리고 간신히 불시착을 면하는 무식한 생존법.
- **안드로이드 LMK**: 비행기 연료 게이지가 30% 남았을 때 불필요한 의자를 버리고, 20% 남았을 때 승객 수하물을 버리고, [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% 남았을 때 기내식을 버리는 식으로 미리미리 무게를 줄여 추락의 공포 자체를 느끼지 못하게 하는 꼼꼼한 기장.

- **등장 배경**:
- 안드로이드 프로젝트 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/), 구글 엔지니어들이 데스크톱용 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 모바일의 극악한 메모리 환경을 견디지 못하는 것을 보고 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 소스를 뜯어고쳐 LMK 모듈을 쑤셔 넣었다. 이후 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 바깥(유저 스페이스) 데몬인 `lmkd`로 진화하며 현대 안드로이드 램 관리의 핵심이 되었다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">안드로이드 LMK의 단계적 암살(Kill) 메커니즘 시각화</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">스마트폰 전체 RAM: 8GB</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">메모리 잔여량 📉</div><div class="kb-diagram-node">LMK 트리거 및 희생자 선정 타겟</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(안전) 2GB 남음 ──▶ 아무 일 없음. 평화로운 상태.</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">1단계 타격</div><div class="kb-diagram-note">: 빈 앱 (Empty App) 사살</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(이미 다 끝났는데 찌꺼기만 남은 앱들 강제 종료)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">2단계 타격</div><div class="kb-diagram-note">: 캐시된 앱 (Cached App) 사살</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(어제 쓰다 홈버튼 누르고 백그라운드에 쌓인 앱들)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">3단계 타격</div><div class="kb-diagram-note">: 서비스 앱 (Service App) 사살</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(음악 재생 등 뒤에서 몰래 도는 앱들까지 쳐냄)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">4단계 타격</div><div class="kb-diagram-note">: 보여지는 앱 (Visible App) 사살</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(화면에 떠 있는 게임을 제외한 모든 앱 몰살)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">Foreground App</div><div class="kb-diagram-note">을 살리기 위해,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">뒤에 숨어있는 앱들을 등급별로 썰어버리며 램을 지속적으로 상납함.</div></div>
</div>
</div>



**[다이어그램 해설]** 안드로이드의 메모리 관리는 '계급 사회'다. 유저와 상호작용하는 앱(Foreground)은 성골 귀족이고, 한 달 전에 쓰다 놔둔 앱(Cached)은 언제든 죽여도 되는 천민이다. 이 계급을 바탕으로 안드로이드는 잔여 메모리가 특정 선([Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/))을 넘을 때마다 해당 선에 배정된 천민 계급부터 학살을 시작한다. 사용자가 무거운 게임(Genshin 등)을 켜면 메모리가 500MB, 200MB 훅훅 떨어지는데, 이때 LMK가 뒤에서 캐시된 앱과 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 앱들을 0.1초 만에 연속으로 수십 개씩 도륙(SIGKILL)내며 램을 확보해 준다. 덕분에 게임은 단 1초의 버벅임 없이 실행될 수 있다. 나중에 홈 화면으로 돌아가서 어제 쓰던 앱을 다시 켰을 때 처음 로고부터 다시 로딩된다면(리프레시 현상), 그건 그 앱이 어제 이 LMK의 칼날에 암살당했기 때문이다.

- **📢 섹션 요약 비유**: 왕(현재 쓰는 앱)이 지나가야 하는데 길이 좁으면, 경호원(LMK)이 길거리에 있는 천민(오래된 앱)들부터 평민([서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 앱), 귀족(보이는 앱) 순서대로 몽둥이로 밀어내어 왕이 한 번도 멈추지 않고 길을 통과하게 만드는 철저한 신분제 교통정리 시스템입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 운명의 생사부: oom_score_adj (OOM_ADJ 점수)

LMK가 "누구를 죽일지" 결정하는 유일한 기준표다. 안드로이드 프레임워크의 최고 관리자인 `ActivityManagerService (AMS)`가 앱의 상태가 바뀔 때마다 실시간으로 이 점수를 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)(`/proc/<pid>/oom_score_adj`)에 박아 넣는다.

| ADJ 계급 (상태) | oom_score_adj 점수 | 생존 우선순위 | 설명 (언제 죽는가?) |
|:---|:---:|:---:|:---|
| **Foreground App** | **0** | 신 (절대 안 죽음) | 지금 화면에 떠서 사용자가 터치하고 있는 앱. 이걸 죽이면 안드로이드가 욕을 먹으므로 폰이 터질 때까지 살린다. |
| **Visible App** | **100 ~ 200** | 귀족 (거의 안 죽음) | 화면 뒤에 살짝 가려져서 일부만 보이거나(팝업창 뒤), 상단바에 표시된 앱. |
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> App</strong> | **300 ~ 500** | 평민 (버티다 죽음) | 보이지는 않지만 노래를 재생 중이거나 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 다운로드 중인 백그라운드 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 앱. |
| **Cached App** | **900 ~ 999** | 노비 (가장 먼저 죽음) | 홈버튼을 누르고 나간 후 아무 일도 안 하고 메모리만 파먹고 있는 껍데기. (LMK의 1순위 먹잇감). |

### 인 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) LMK (과거) vs 유저 스페이스 lmkd (현재) 의 진화

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 안드로이드는 이 킬러 로직을 리눅스 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 소스 한가운데 박아버렸다. 하지만 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)단에서 복잡한 정책을 돌리려니 오버헤드가 크고 구글이 맘대로 로직을 튜닝하기 힘들었다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">안드로이드 9(Pie) 이후의 차세대 lmkd (User-space) 구조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1. 메모리 압박 감지 (Kernel PSI)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">리눅스 커널의 PSI (Pressure Stall Information) 모니터가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">"어! RAM이 모자라서 CPU가 스와핑 대기하느라 10% 지연되고 있어!" 라고 탐지.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▼ (이벤트 알람 발송)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">========================= (커널/유저 경계) ==========================</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">2. 유저 스페이스 lmkd (Low Memory Killer Daemon)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- AMS(안드로이드 프레임워크)가 준 <code>OOM_ADJ</code> 점수표(생사부)를 들고 있음.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 알람을 받자마자, 점수표에서 점수가 가장 높은 999점(캐시 앱)부터 찾음.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▼ (사형 선고)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">3. SIGKILL (-9) 발송 및 메모리 회수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 타겟 앱의 프로세스를 강제 사살.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- 회수된 수백 MB의 램이 즉시 Foreground(게임) 앱으로 흘러 들어감. 🚀</div></div>
</div>
</div>



**[다이어그램 해설]** 이것이 안드로이드 메모리 아키텍처의 거대한 전환점이다. 옛날엔 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)이 직접 죽였다면, 이제 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 단순히 "지금 메모리 숨 막혀요(PSI)"라고 알람만 울린다. 진짜 살생부 엑셀 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/)을 들고 다니며 누구 목을 칠지 결정하는 '사형 집행인' 역할은 완전히 유저 영역(User Space)의 독립된 C/C++ 데몬인 `lmkd`로 빠져나왔다. 이렇게 역할을 분리함으로써 구글은 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 소스를 수정하지 않고도 기기 제조사(삼성, 샤오미)마다 램 용량(4GB, 12GB 등)에 맞춰 킬러의 성향(잔인하게 죽일지, 버틸지)을 정밀하게 튜닝할 수 있게 되었다.

- **📢 섹션 요약 비유**: 옛날엔 경찰서장([커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/))이 직접 명부를 들고 돌아다니며 범죄자를 쏴 죽였다면, 지금은 서장님은 [CCTV](/knowledge-base/studynote/09_security/18_iot_ot_physical/933_cctv/)(PSI)로 감시만 하고, "지금 A구역 위험해!"라고 무전만 치면 대기하던 암살단(lmkd)이 명부(ADJ)를 보고 즉각 타겟을 깔끔하게 암살하고 빠지는 전문화된 분업화입니다.

---

## Ⅲ. 비교 및 연결

### Android LMK vs iOS Jetsam (애플의 메모리 암살자)

안드로이드 폰은 램이 12GB인데도 버벅거리고, 아이폰은 램 6GB로도 부드럽다. 그 비밀은 메모리 킬러의 사상 차이에 있다.

| 비교 항목 | 안드로이드 LMK (lmkd) | 애플 iOS Jetsam |
|:---|:---|:---|
| **기반 OS 철학** | 리눅스의 자유방임주의 (일단 램을 막 주다가 모자라면 때려잡음) | Unix 기반 극단적 통제 (앱이 켜질 때부터 한도를 빡빡하게 잠금) |
| **메모리 한도(Limit)**| 앱 하나가 전체 램의 70~80%를 달라고 해도 줌. | 앱마다 쓸 수 있는 메모리 `High Watermark`가 명확히 박혀있음. 선 넘으면 즉사. |
| **죽이는 놈 찾기** | 메모리 압박이 오면 "가장 중요도(ADJ)가 낮은 백그라운드 놈"을 죽임 | 메모리 압박이 오면 "가장 중요도 낮은 놈" + <strong>"자기 한도(Limit)를 초과한 가장 뚱뚱한 놈"</strong>을 핀포인트 폭격함 |
| **백그라운드 통제** | 비교적 유연하게 풀어줘서 백그라운드 멀티태스킹이 강함 | 앱이 화면 뒤로 넘어가면 가차 없이 램 상태를 동결(Freeze)해버리거나 즉시 Jetsam으로 쳐냄 |

### 과목 융합 관점

- <strong><a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/">가상 메모리</a> (zRAM의 융합)</strong>: 스마트폰은 디스크가 낸드 플래시(eMMC/UFS)라서 잦은 스와핑을 하면 디스크 수명이 닳아 폰이 1년 만에 죽는다. 그래서 진짜 디스크 스왑을 버리고 도입한 마법이 <strong>zRAM</strong>이다. 물리 램(RAM) 공간의 일부를 떼어서 그 안에 데이터를 '[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)(Zip)'해서 쑤셔 넣는 가상의 스왑 파티션이다. LMK가 발동하기 직전, [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)은 잘 안 쓰는 앱의 메모리 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 디스크로 내보내는 대신, CPU로 3배 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해서 zRAM 공간에 쑤셔 넣는다. 이렇게 하면 LMK의 칼날을 피하면서도 더 많은 앱을 백그라운드에 살려둘 수 있다(리프레시 방어).
- <strong>프로세스 통신 (<a href="/knowledge-base/studynote/02_operating_system/10_security/662_android_binder_ipc_thread_pool/">Binder</a> <a href="/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/">IPC</a>)</strong>: ADJ 점수 계산은 소름 돋게 정교하다. 만약 A라는 날씨 앱이 뒤에 숨어있어서(Cached 계급) 당장 죽어야 할 타겟이 됐다 치자. 그런데 앞 화면에 떠 있는 카카오톡(Foreground 계급)이 A 날씨 앱에게 날씨를 물어보려고 안드로이드의 [Binder](/knowledge-base/studynote/02_operating_system/10_security/662_android_binder_ipc_thread_pool/) [IPC](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/)([프로세스 간 통신](/knowledge-base/studynote/02_operating_system/02_process_thread/117_ipc/)) 파이프를 딱 꽂고 있다면? AMS는 "오, 위대한 카톡님이 A 앱을 필요로 하시는구나!"라며 **A 앱의 점수를 즉각 귀족(Foreground 수준)으로 승격(Inheritance)** 시켜 LMK의 칼날로부터 극적으로 구출해 낸다.

- **📢 섹션 요약 비유**: iOS가 기숙사 사감처럼 학생들(앱)의 간식(메모리) 양을 처음부터 1개로 빡빡하게 통제하는 스파르타식(Jetsam)이라면, 안드로이드는 뷔페처럼 자유롭게 먹게 놔두다 고기가 떨어지려 하면(압박) 안 먹고 조는 애들(백그라운드)의 접시부터 강제로 뺏어버리는(LMK) 자율적 약육강식 체제입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오 및 운영 [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

1. **시나리오 — 내가 만든 앱이 홈 화면만 가면 귀신같이 죽는 현상 (리프레시 지옥)**: 안드로이드 앱 개발자가 이미지 캐싱과 동영상 데이터를 엄청나게 올려두는 무거운 앱을 만들었다. 사용자가 카톡에 답장하려고 홈버튼을 누르고 나갔다가 10초 뒤에 돌아왔는데, 앱이 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화면부터 다시 로딩된다.
- **원인 분석**: 앱이 화면(Foreground)에서 내려가는 순간, AMS는 이 앱의 ADJ 점수를 신(0)에서 천민(900대)으로 수직 강등시킨다. 이때 이 앱이 램을 무식하게 많이(예: 1GB) 먹고 있었다면, LMK 입장에서는 "와, 저 천민 하나만 죽이면 램 1GB를 한 방에 털 수 있네!"라며 가장 최우선 타겟(Best Victim)으로 삼고 즉각 쳐 죽인 것이다.
- **아키텍트 판단 (메모리 다이어트 및 콜백 대응)**: 안드로이드 개발의 철칙은 "화면에서 내려갈 때 짐을 버려라"다. 앱은 `onTrimMemory()` 콜백을 무조건 구현하여, OS가 "메모리 모자란데 죽기 싫으면 짐 좀 버려"라고 경고를 날릴 때 즉각 Bitmap 이미지 캐시와 비트맵 풀을 `null`로 날려버려 램 다이어트를 해야 한다. 앱을 가볍게 만들면 LMK는 굳이 가벼운 놈을 죽여봤자 얻을 게 없으므로 암살 명단에서 뒤로 미뤄주어 생존 확률이 극적으로 올라간다.

2. **시나리오 — 음악 플레이어 앱이 중간에 픽픽 끊기며 죽는 장애**: 화면을 끄고 음악을 듣거나 GPS 만보기를 켜고 걷고 있는데, 30분쯤 지나면 자꾸 앱이 죽어서 음악이 꺼진다.
- **원인 분석**: 개발자가 이 작업을 일반 쓰레드나 일반 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)(Activity)에 묶어놓고 화면을 껐다. 화면이 꺼진 앱은 'Cached App(노비 계급)'으로 추락하므로, 유저가 다른 카메라 앱을 켜는 순간 LMK가 즉시 학살해 버린 것이다.
- <strong>아키텍트 판단 (Foreground <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> 승격)</strong>: 음악 재생, GPS 추적 같은 작업은 안드로이드 시스템의 룰에 맞춰 <strong>Foreground <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a> (포그라운드 <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a>)</strong>라는 특수 [컴포넌트](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/603_component_independent_deployment_unit/)로 분리하여 실행해야 한다. 이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 상단 노티피케이션 바에 강제로 알림을 띄우는 조건으로, 시스템에게 "나 뒤에 숨어있지만 사용자에게 아주 중요한 일을 하고 있어!"라고 어필한다. 이 순간 AMS는 앱의 ADJ 점수를 귀족 급(보이는 앱 수준)으로 끌어올려 주어, 웬만한 메모리 부족 사태에도 LMK가 절대 건드리지 못하는 철갑 방패를 얻게 된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">안드로이드 앱 생존(LMK 회피)을 위한 아키텍처 생명주기</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">📱 내 앱이 백그라운드로 내려갔을 때 생존하는 법</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">앱이 보이지 않을 때도 음악 재생/위치 추적을 계속해야 하는가?</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">Foreground Service 적용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(상단바 알림 띄우고 ADJ 점수 올려서 깡패 생존 보장)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 아니오 (단순히 화면에서 사라진 일반 앱임)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell"><code>onTrimMemory(TRIM_MEMORY_UI_HIDDEN)</code> 콜백 신호가 커널에서 날아옴!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">OOM 킬러의 1순위 먹잇감 등극</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(무거운 캐시를 쥐고 있다가 램 용량 강탈 목적으로 사살됨)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">이미지 캐시와 불필요한 메모리 즉각 해제(null)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(몸집을 깃털처럼 줄여서 LMK 눈에 안 띄게 숨어 생존 연장)</div></div>
</div>
</div>



**[다이어그램 해설]** 안드로이드 개발자는 절대 메모리가 무한하다고 생각하면 안 된다. "내 앱만 소중하다"며 메모리를 물고 늘어지는 악덕 앱은 OS(LMK)의 가차 없는 철퇴를 맞고 유저에게 "최적화 개판인 앱"으로 별점 테러를 받게 된다. 훌륭한 아키텍처는 운영체제와 대화(Callback)하는 앱이다. OS가 힘들다고 SOS 신호를 보낼 때 스스로 캐시를 비워주는 '양보의 미덕'을 코딩하는 것만이 멀티태스킹의 리프레시(재시작) 지옥에서 내 앱을 살려내는 유일한 정도()다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/">Task</a> Killer (메모리 정리 앱)의 맹신</strong>: 사용자들이 램을 확보하겠다고 시중에 떠도는 '램 정리 앱([Task](/knowledge-base/studynote/02_operating_system/02_process_thread/150_task/) Killer)'을 깔아서 수시로 로켓 버튼을 눌러 강제 청소를 하는 행위. 안드로이드는 "빈 램(Free RAM)은 낭비되는 램이다"라는 철학을 가진다. 빈 램에 앱들을 올려둬야(Cached) 다음 실행이 1초 만에 끝난다. 정리 앱이 억지로 다 쳐 죽여서 램을 비워놓으면, 사용자가 카톡을 다시 켤 때마다 CPU가 [플래시 메모리](/knowledge-base/studynote/01_computer_architecture/06_memory_hierarchy_cache/256_flash_memory/)(eMMC)에서 무거운 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 전체를 100% 다시 퍼 올려야 하므로, 램은 비어있을지언정 <strong>배터리 소모가 극심해지고 스마트폰 속도가 오히려 반토막</strong>이 나는 끔찍한 역효과가 난다. 안드로이드의 메모리 관리는 LMK라는 최고 권위자에게 100% 맡겨두는 게 정답이다.

- **📢 섹션 요약 비유**: 자동차 트렁크(램)를 텅텅 비우겠다고, 여행 갈 때마다 트렁크에 실어둔 텐트와 의자를 다 집에 버리고 오면(램 정리 앱), 막상 놀러 가서 매번 텐트를 다시 사서 조립하느라 돈(배터리)과 시간(CPU)이 다 박살 납니다. 트렁크는 꽉꽉 채워 다니고, 짐이 넘칠 때만 안드로이드 기장님(LMK)이 알아서 안 쓰는 짐을 버리게 놔두는 게 최적의 효율입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 일반 Linux [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/) 킬러 | 안드로이드 LMK (lmkd) | 개선 효과 |
|:---|:---|:---|:---|
| **정량 (발동 시점)** | 메모리 100% 고갈(0MB 남음) 시 폭발 | 메모리 20% 등 여유 임계점 도달 시 선제 타격 | 폰 멈춤(Freezing) 방지 및 프레임 드랍 원천 차단 |
| **정량 (희생자 점수)**| 메모리 많이 먹는 놈 위주 사살 (무차별) | 화면(Foreground) 상태 점수 철저히 반영 | 사용자가 터치 중인 화면 앱의 생존율 100% 보장 |
| <strong>정성 (UX <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a>)</strong> | 시스템과 무관한 핵심 데몬이 죽을 위험 | 철저한 천민 계급(Cached) 위주의 조용한 암살 | 멀티태스킹의 체감 속도 상승 (보이지 않는 스케줄링 예술) |

### 미래 전망
- <strong><a href="/knowledge-base/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/">머신러닝</a> 기반 LMK 예측</strong>: 현재의 LMK는 잔여 메모리 '수치'라는 딱딱한 룰 기반이다. 차세대 안드로이드 버전에선 딥러닝([AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/))이 탑재되어, "이 사용자는 아침 출근 시간에 '카카오톡'과 '음악 앱'만 번갈아 쓴다"는 패턴을 학습한다. 램이 부족해져도, 평소 점수가 낮은 음악 앱이더라도 AI가 "이건 5분 뒤에 쓸 앱이니까 죽이지 마!"라고 쉴드를 치고, 어제 켰던 무거운 게임 앱부터 핀포인트로 암살하는 사용자 맞춤형 지능형 킬러로 진화하고 있다.
- <strong>MGLRU (Multi-Generational <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a>) 도입</strong>: 구형 리눅스의 메모리 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 정리 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))은 안 쓰는 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 찾는 데 CPU를 너무 많이 소모했다. 구글이 직접 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)을 뜯어고쳐 최근 세대(Generation) 기반의 MGLRU를 도입하면서, lmkd가 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 찾고 죽이는 과정의 CPU 부하를 절반 이하로 떨어뜨려 최신 안드로이드 13부터 램 4GB짜리 보급형 폰에서도 놀라운 부드러움을 선사하고 있다.

### 참고 표준
- <strong>Linux <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/">커널</a> 메모리 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/">Cgroups</a> 및 PSI (Pressure Stall Information)</strong>: 메모리 부족 압박을 실시간으로 감지하고 lmkd에 알람을 쏘는 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)의 최신 모니터링 이벤트 표준 인터페이스.
- <strong>Android AMS (Activity Manager <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">Service</a>) Lifecycle</strong>: 앱의 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/), 백그라운드 전환, 사망에 이르는 전 생명주기를 통제하고 킬러에게 점수(OOM_ADJ)를 부여하는 안드로이드 OS 최상위 자바 프레임워크 룰.

안드로이드 LMK는 "한정된 자원(RAM) 안에서 무한한 욕망(앱 실행)을 어떻게 충족시킬 것인가"라는 경제학적 딜레마에 대한 모바일 공학의 처절한 대답이다. 수 기가바이트를 처먹는 모바일 게임과 무거운 SNS 앱들이 난무하는 전쟁터에서, 폰이 버벅거리거나 멈추지 않는 유일한 이유는 지금 여러분이 화면을 바라보는 이 1초의 찰나에도 뒷단에서 수많은 백그라운드 앱들이 LMK의 무자비한 칼날에 목이 잘려 나가며 램(RAM)을 눈물겹게 상납하고 있기 때문이다. 이 소리 없는 학살의 교향곡이야말로 스마트폰 멀티태스킹을 매끄럽게 돌아가게 하는 진정한 마법이다.

- **📢 섹션 요약 비유**: 타이타닉호(스마트폰)가 가라앉고 있는데 구명보트(RAM)는 절반밖에 없습니다. 일반 OS는 가라앉기 직전에 제비뽑기로 사람을 밀어냅니다. 하지만 LMK 선장은 배에 물이 조금 차오르자마자 즉시 "1등석 귀족(현재 켜진 앱) 탑승! 3등석 짐칸(백그라운드 캐시) 승객은 즉시 바다로 뛰어내려라!"라며 냉혹하지만 가장 질서 정연하게 배의 평화를 유지하는 잔혹한 재난 대처법입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [클론](/knowledge-base/studynote/02_operating_system/02_process_thread/149_clone_system_call/)([clone](/knowledge-base/studynote/02_operating_system/02_process_thread/149_clone_system_call/)) 시스템 콜 [스레드](/knowledge-base/studynote/02_operating_system/02_process_thread/092_thread_lwp/) 공유 [플래그](/knowledge-base/studynote/03_network/04_data_link_layer_error/186_character_stuffing_dle_stx_etx/) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [cgroups](/knowledge-base/studynote/02_operating_system/01_overview_architecture/062_cgroups/) 메모리, CPU 자원 제한 격리 [컨테이너](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/561_container_based_deployment/) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| iOS 앱 [샌드박싱](/knowledge-base/studynote/02_operating_system/10_security/602_sandboxing_kernel_wrapper/) 구조 | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [라이브 패칭](/knowledge-base/studynote/02_operating_system/11_exam_summary/789_live_patching_kpatch_no_downtime/) ([Kpatch](/knowledge-base/studynote/02_operating_system/11_exam_summary/789_live_patching_kpatch_no_downtime/)) [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 정지 없는 보안 | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">cgroups 메모리, CPU 자원 제한 격리 컨테이너</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">안드로이드 LMK (Low Memory Killer) 작동</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">iOS 앱 샌드박싱 구조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">라이브 패칭 (Kpatch) 커널 정지 없는 보안</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 스마트폰 책상(메모리)은 너무 좁아서 그림책(앱)을 3권만 펼치면 꽉 차요. 근데 우리는 자꾸 새 그림책을 꺼내고 싶잖아요.
2. 옛날 컴퓨터는 책상이 꽉 차서 멈출 때까지 기다렸다가, 한꺼번에 책을 엎어버려서(폰 멈춤) 짜증이 났어요.
3. 하지만 안드로이드 로봇(LMK)은 우리가 3번째 그림책을 꺼내려는 순간, "어! 좁다!" 하고 눈치채고 어제 펼쳐둔 제일 안 보는 책 1권을 번개처럼 몰래 서랍에 치워버려요. 그래서 책상이 언제나 널널하게 유지된답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 787 / 800

← **이전**: [786. cgroups 메모리, CPU 자원 제한 격리 컨테이너 (Cgroups Memory CPU Isolation Container)](/knowledge-base/studynote/02_operating_system/11_exam_summary/786_cgroups_memory_cpu_isolation_container/)
**다음**: [788. iOS 앱 샌드박싱 구조 (Ios App Sandboxing Architecture)](/knowledge-base/studynote/02_operating_system/11_exam_summary/788_ios_app_sandboxing_architecture/) →

---
