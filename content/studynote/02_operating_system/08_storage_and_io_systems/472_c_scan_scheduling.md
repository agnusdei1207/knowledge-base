---
title: "472. C-SCAN (Circular SCAN) - 한 방향으로만 처리하고 끝에 도달하면 시작점으로 빠르게 복귀 (대기 시간 균등화)"
date: "2026-05-09"
tags:
  - "studynote-operating-system"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: C-SCAN(Circular SCAN)은 엘리베이터(SCAN) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 양방향으로 움직이며 발생시키던 '위치에 따른 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)의 심각한 편차'를 해결하기 위해, <strong>디스크 헤드가 오직 '한쪽 방향'으로만 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 훑으며 전진하고, 끝에 도달하면 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>를 읽지 않은 채 출발점으로 빛의 속도로 복귀하는 <a href="/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/">단방향</a> 순환 큐잉 기법</strong>이다.
> 2. **가치**: 디스크의 정중앙에 있든 맨 구석 양 끝단에 있든, 모든 I/O 요청이 바늘이 돌아오기를 기다리는 <strong>'최대 대기 시간(Max Waiting Time)'과 '평균 대기 시간 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>(<a href="/studynote/08_algorithm_stats/08_stats/136_variance/">Variance</a>)'을 완벽하게 균등화(Equalize)시켜 시스템의 예측 가능성을 극대화</strong>한다.
> 3. **융합(한계)**: 돌아오는 길에 있는 요청을 뻔히 보면서도 무시하고 지나쳐야 하는 극한의 비효율(오버헤드)이 존재하지만, 현대 커널은 이를 <strong>C-LOOK(요청 없는 허공은 건너뛰기)과 융합하여 실시간 스트리밍 등 타이밍이 생명인 엔터프라이즈 환경의 스탠다드로 채택</strong>했다.

---

## Ⅰ. 개요 및 필요성

- **개념**: C-SCAN의 'C'는 Circular(원형)를 뜻한다. 디스크의 바늘을 마치 시계처럼 둥글게 이어진 트랙을 맴돌듯 쓴다. 바늘이 0번 트랙에서 199번 트랙으로 '상행'하며 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 싹쓸이한다. 199번 벽을 찍은 순간, 방향을 꺾어 내려오며 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 줍는 SCAN(양방향)과 달리, C-SCAN은 <strong>아무 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>도 줍지 않고 0.001초 만에 0번 트랙(시작점)으로 홱! 하고 <a href="/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/">롤백</a>(Return)해 버린다.</strong> 그리고 다시 0번부터 상행하며 줍는다. 오직 '1Way([단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/))' 싹쓸이다.
- **필요성**: 기존 SCAN(엘리베이터)은 치명적인 불평등(Inequality)의 악마였다. 100번(중간) 트랙에 사는 앱은 바늘이 올라갈 때 한번, 내려올 때 한번 훑어주니 꿀을 빤다. 하지만 198번(끝단)에 사는 앱은 바늘이 199번을 찍고 내려가버리면, 바늘이 0번까지 갔다가 다시 199번으로 올라올 때까지 <strong>디스크 전체를 2번 횡단하는 우주적인 시간(Double Delay)</strong>을 굶은 채로 기다려야 했다. "가운데 사는 놈이나 구석에 사는 놈이나 제발 똑같은 시간만 기다리게 해 줘!" 이 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)의 널뛰기(High [Variance](/studynote/08_algorithm_stats/08_stats/136_variance/))를 때려잡기 위해 공학자들은 '돌아오는 길의 효율'을 과감히 쓰레기통에 버리고 [단방향](/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 복귀라는 강수를 둔다.

- **등장 배경 및 공평성의 집착**:
  1. **SCAN의 양극화**: 위치에 따라 대기 시간이 2배 이상 차이 나는 불공정 터짐.
  2. **실시간(RTOS) 시스템의 불만**: "나는 0.5초마다 영상 프레임이 꼬박꼬박 와야 해! 평균 속도보다 일정함(Jitter [Zero](/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/))이 중요해!"
  3. <strong>시간 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>(<a href="/studynote/08_algorithm_stats/08_stats/136_variance/">Variance</a>) <a href="/studynote/09_security/13_secops_ir_forensics/656_ir_containment/">억제</a></strong>: 귀환 시간(Return Sweep)을 희생해서라도 대기 시간의 표준편차를 0에 수렴시키는 C-SCAN이 발명됨.

```text
+-----------------------------------------------------------------------+
|        SCAN (불평등) vs C-SCAN (절대 평등) 바늘 동선 시각화           |
+-----------------------------------------------------------------------+
|                                                                       |
| [ 큐 요청 순서 ]:  98, 183, 37, 122, 14, 124                          |
| [ 헤드 위치 ]: 53번 트랙 / [ 199번을 향해 상행 중! ]                  |
|                                                                       |
| -> 1. 기본 SCAN (가운데 꿀 빨고 양끝단 굶어 죽음)                      |
|   14   37     53     98    122 124        183      199                |
|   |    |      [시작] --->     |  |          |        |                 |
|   |    |             +-----> |  |          |        |                  |
|   |    |                    +--> |          |        |                 |
|   |    |                       +----------> |        |                 |
|   |    |                                  +--------> |                 |
|   |    |<------------------------------------------+                   |
|   |<---+                                                               |
|                                                                       |
| -> 2. C-SCAN (돌아올 땐 줍지 않고 0번으로 순간 이동 롤백!)             |
|   14   37     53     98    122 124        183      199                |
|   |    |      [시작] --->     |  |          |        |                 |
|   |    |             +-----> |  |          |        |                  |
|   |    |                    +--> |          |        |                 |
|   |    |                       +----------> |        |                 |
|   |    |                                  +--------> |                 |
| 0 |    | <-- (줍지 않고 빛의 속도로 점프하여 0번 벽으로 복귀!) ---+    |
| +-->|    |                                                             |
|    +-->|                                                               |
| ✅ 특징: 14번과 37번은 눈앞에서 바늘이 지나가도 못 줍지만, 0번으로    |
|        돌아와서 다시 훑어주기 때문에 대기 시간이 완벽히 일정해짐.     |
+-----------------------------------------------------------------------+
```
**[다이어그램 해설]** 그림 2를 보면 인간의 직관으론 이해가 안 된다. 183번에서 199번 끝을 찍고 0번으로 돌아올 때, 가는 길목에 있는 37번과 14번을 왜 안 줍고 쌩까는가? "기왕 돌아가는 길에 주우면(SCAN) 훨씬 빠르잖아!" 이게 C-SCAN을 이해하는 가장 큰 장벽이다. 하지만 줍는 순간 그건 SCAN이 되어 양 끝단 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 다시 2배의 시간 동안 굶겨 죽이게 된다. <strong>'무조건 맨 앞부터 순서대로 쓸어 담는다'</strong>는 원형(Circular)의 철학을 지키기 위해, 돌아가는 헛스윙 오버헤드를 눈물 머금고 감수한 것이다.

- **📢 섹션 요약 비유**: [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 노선입니다. SCAN은 서울에서 부산까지 손님을 태우고 가다가, 부산에서 다시 서울로 올라오면서 반대편 손님을 태웁니다(양방향). C-SCAN은 서울에서 부산까지 손님을 다 내리면, [버스](/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 텅 빈 채 고속도로 1차선을 타고 서울로 미친 듯이 무정차 직행([롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/))한 뒤, 다시 서울에서 부산행 손님을 태웁니다. 기름값(오버헤드)은 버리지만, 서울역 승객과 대전역 승객의 배차 간격(대기 시간)은 100% 일정해집니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 리턴 스윕(Return Sweep)의 하드웨어적 진실

"빈 차로 199번에서 0번까지 돌아오면, 그 거리를 이동하느라 8ms([탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/))가 똑같이 버려지는 거 아냐? 완전 손해네!"라고 생각할 수 있다.
- 하지만 <strong>하드디스크의 물리적 스펙</strong>은 다르다.
- 바늘이 1칸씩 10번을 이동하는 데 걸리는 시간(탐색 후 멈춤)보다, 바늘을 멈추지 않고 끝에서 끝으로 한 방에 풀스윙(Full-stroke Seek) 튕겨내는 속도가 기계적으로 압도적으로 더 빠르다.
- 즉, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽으며 멈칫멈칫 내려오는 SCAN의 하행선 시간보다, C-SCAN이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽지 않고 0번으로 번개처럼 점프(Return Sweep)하는 시간이 체감상 훨씬 짧기 때문에 이 1Way 싹쓸이 전략이 실무 하드웨어 위에서 수학적으로 성립하는 것이다.

---

### 대기 시간 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/)([Variance](/studynote/08_algorithm_stats/08_stats/136_variance/))의 수학적 평탄화

OS 시험 문제에서 C-SCAN이 정답이 되는 핵심 키워드는 <strong>"<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a>의 <a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>(편차) 최소화"</strong>다.
- **SCAN (양방향)**:
  - 100번 트랙: 바늘이 올라갈 때 한 번, 내려올 때 한 번 긁는다. 대기 주기 = `짧음`
  - 0번 트랙: 바늘이 199번까지 갔다가 다시 0번으로 내려와야 한다. 대기 주기 = `디스크 2번 왕복 시간` (최악)
- <strong>C-SCAN (<a href="/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/">단방향</a>)</strong>:
  - 100번 트랙: 바늘이 지나갔다? 그럼 바늘이 199번 찍고 0번으로 돌아와서 다시 100번으로 와야 한다. 대기 주기 = `디스크 1번 왕복 시간`
  - 0번 트랙: 바늘이 지나갔다? 199번 찍고 0번으로 돌아오면 바로 먹는다. 대기 주기 = `디스크 1번 왕복 시간`
- **결과**: <strong>어떤 트랙에 <a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>가 있든, 최대 대기 시간은 '디스크 1번 왕복 시간'으로 완벽하게 수렴하고 고정된다.</strong> 이것이 실시간 운영체제가 열광하는 완벽한 예측 가능성(Determinism)이다.

- **📢 섹션 요약 비유**: 놀이공원 꼬마기차입니다. 앞자리에 탔든 맨 뒷자리에 탔든, 기차가 한 바퀴 돌고 오는 시간은 정확히 10분으로 정해져 있습니다. "내가 구석 자리에 앉았다고 20분을 기다리고, 한가운데 앉았다고 2분 만에 타는" 그런 차별 대우(SCAN)가 아예 불가능한 완벽한 둥근 원(Circular) 형태의 공평한 트랙입니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: SCAN (효율의 끝) vs C-SCAN (평등의 끝)

| 평가 지표 | SCAN (엘리베이터) | C-SCAN (순환 엘리베이터) |
|:---|:---|:---|
| **바늘 이동 방식** | 상하 양방향 모두 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 긁음 | 상행 시에만 긁고, 하행은 **빈 차로 쾌속 점프** |
| <strong>디스크 전체 <a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>(<a href="/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">Throughput</a>)</strong>| 미세하게 더 높음 (버리는 동선이 없으므로) | [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)(헛스윙) 하느라 **약간의 손해 발생** |
| <strong>대기 시간의 편차 (<a href="/studynote/08_algorithm_stats/08_stats/136_variance/">Variance</a>)</strong>| 최악. 양 끝단과 중앙의 대기시간이 극과 극임 | **최상 (0에 수렴). 누구든 대기 시간이 똑같음** |
| <strong>실시간(RTOS) <a href="/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/">호환성</a></strong> | 예측 불가능하여 튕길 수 있음 | **최대 대기 시간(Max Delay) 보장으로 완벽 호환**|

### 멀티미디어 스트리밍 환경의 구세주
유튜브 서버에서 하드디스크에 저장된 4K 영상을 수만 명에게 뿌려준다고 치자.
- 영상 스트리밍은 '평균 속도'가 100MB/s가 나오는 게 중요한 게 아니다. 단 1초라도 속도가 5MB/s로 떨어져 영상이 '[버퍼링](/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/)(버벅댐)' 걸리면 유저는 쌍욕을 하며 끈다.
- SCAN을 쓰면, 디스크 끝단에 저장된 영상 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 조각은 바늘이 왕복하는 긴 시간 동안 읽히지 않아 유저 폰에 [버퍼링](/studynote/02_operating_system/08_storage_and_io_systems/454_buffering/) 렉이 무조건 터진다.
- C-SCAN을 쓰면, 디스크 전체 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/)은 약간 떨어지지만 <strong>"어떤 <a href="/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/">파일</a>이든 최대 X 밀리초 안에는 무조건 1번씩 읽힌다"</strong>는 강력한 족쇄가 채워진다. 이 대기 시간 평탄화 덕분에, 모든 유저가 끊김 없이 안정적으로 스트리밍을 볼 수 있는 인프라가 완성된다.

```text
+----------+------------+------------+------------------------------+
| 스케줄러   | 중앙 데이터 대기| 구석 데이터 대기| 최종 서비스 체감 |
+----------+------------+------------+------------------------------+
| SSTF     | 1초 (VIP)   | 평생 굶어죽음 ☠️| 에러 뿜고 서버 마비    |
| SCAN     | 2초 (빠름)  | 10초 (너무 느림)| 일부 유저 뚝뚝 끊김    |
| C-SCAN   | 5초 (느려짐) | 5초 (극적 빨라짐)| 🚀 전원 스무스 재생  |
+----------+------------+------------+------------------------------+
```
**[매트릭스 해설]** "다 같이 평균적으로 늦어지더라도, 튀는 놈([Outlier](/studynote/14_data_engineering/02_math_mining/076_outlier_detection_iqr_dbscan_isolation_forest/)) 없이 다 같이 똑같은 시간에 받자!" 공학에서 '최악의 경우(Worst Case)'를 방어하는 것이, '최상의 경우(Best Case)'를 높이는 것보다 시스템 안정성에 수만 배 더 가치 있다는 걸 증명하는 철학적 결과물이다.

- **📢 섹션 요약 비유**: 인터넷 기사가 "어떤 집은 1000메가 나오고, 어떤 집은 10메가 나오는" 불안정한 인터넷(SCAN)보다, "우리 동네는 어느 집이든 무조건 500메가가 고정으로 딱 박혀 나옵니다(C-SCAN)"라고 광고하는 인터넷을 훨씬 더 좋은 통신망으로 쳐주는 것과 같습니다. 인프라의 생명은 '균일함'입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: 왜 C-LOOK으로 다시 진화했는가? (바보 같은 끝점 찍기)
C-SCAN은 이론상 완벽한 평등을 이뤘지만, 융통성이 너무 없어서 실무진 뒷목을 잡게 했다.
1. **끝점 성애자**:
   - 큐에 가장 마지막으로 들어온 요청이 150번 트랙이다. 151번~199번 벽 끝까지는 텅텅 비어 있다.
   - 하지만 C-SCAN은 멍청한 기계라 150번을 처리하고도 **굳이 텅 빈 허공을 가르며 디스크 맨 끝 벽(199번)까지 쿵! 하고 찍은 다음에야** 0번으로 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)한다. (무의미한 49번 트랙 전진).
   - 0번으로 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)할 때도, 제일 앞의 요청이 20번 트랙이면 20번으로 바로 가면 되는데 굳이 0번 벽까지 쿵! 찍고 20번으로 올라온다.
2. **C-LOOK의 탄생 (현대 디스크의 최종 진화)**:
   - "야! 가는 길에 더 이상 큐에 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 없으면, 끝까지 가지 말고 그 자리에서 바로 뒤돌아(Turn)!"
   - 이 상식적인 **"미리 쳐다보기(LOOK)"** 로직을 C-SCAN에 덧씌운 것이 바로 **C-LOOK** [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.
   - 현대 OS는 바보 같은 SCAN, C-SCAN을 생으로 쓰지 않고 100% 이 LOOK과 C-LOOK으로 튜닝하여 디스크의 헛스윙(오버헤드)을 0으로 소멸시켰다. (다음 장 상세 서술).

### [RAID](/studynote/02_operating_system/08_storage_and_io_systems/483_raid_overview/) 스토리지 배열에서의 C-SCAN
여러 대의 하드디스크를 묶어 쓰는 [RAID 5](/studynote/02_operating_system/08_storage_and_io_systems/487_raid_5_distributed_parity/), [RAID 6](/studynote/02_operating_system/08_storage_and_io_systems/488_raid_6_dual_parity/) 서버 장비에서는 C-SCAN의 위력이 배가된다.
[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 여러 디스크의 동일한 트랙([스트라이핑](/studynote/01_computer_architecture/08_io_storage_systems/332_raid_0/))에 쪼개져 저장되는데, 만약 바늘들이 제각각 앞뒤로 요동치면(SCAN) 디스크 간의 타이밍이 어긋나 패리티(Parity) 연산 시 렉이 걸린다. 하지만 모든 디스크 바늘이 C-SCAN으로 "무조건 0번에서 끝으로 쭉 훑고, 다 같이 0번으로 [롤백](/studynote/15_devops_sre/02_cicd_gitops/098_rollback_strategy_pipeline_error_threshold/)!" 하는 일방통행 군무를 추면, 5대의 디스크가 기계적으로 완벽한 일체감을 보이며 I/O 스루풋이 미친 듯이 뻥튀기된다.

- **📢 섹션 요약 비유**: C-SCAN은 고지식한 순찰병이라, 도둑이 5층까지만 있는 걸 뻔히 뻔히 알면서도 규정대로 무조건 옥상(199층)까지 순찰을 다 돌고 내려오는 낭비를 범했습니다. C-LOOK은 도둑이 5층까지만 있다는 무전([Queue](/studynote/08_algorithm_stats/04_datastructure/058_queue/))을 듣자마자 5층에서 바로 발길을 돌려 1층으로 복귀하는 융통성 넘치는 스마트 순찰병으로의 진화입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| <strong><a href="/studynote/08_algorithm_stats/08_stats/136_variance/">Variance</a>(<a href="/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a>) 제로 달성</strong> | 디스크의 중앙이든 양 끝단이든 모든 실린더 구역의 최대 대기 시간(Max [Response Time](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/))을 수학적으로 완벽히 동일하게 평준화 |
| **기계적 동선 최적화** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 읽으며 천천히 후진하는(SCAN) 대신, 0.001초 만에 풀스윙으로 되감기([Rollback](/studynote/02_operating_system/05_deadlock/313_rollback/)) 하는 하드웨어 모터의 물리적 강점 활용 |
| <strong>스트리밍 <a href="/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/">서비스</a> 기반 구축</strong>| 꼬리 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)(Tail [Latency](/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/), 구석 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 렉)을 없애, 실시간 비디오/오디오 스트리밍 서버가 화면 끊김 없이 안정적으로 프레임을 토해내게 방어 |

### 결론 및 미래 전망

C-SCAN (Circular SCAN)은 시스템 공학에서 "효율성(전체 [처리량](/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/))의 일부를 제물로 바쳐서라도, 공평성(균일한 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/))이라는 가치를 수호하는 것이 궁극적으로는 더 위대한 아키텍처다"라는 것을 증명한 철학적 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다. 돌아오는 길의 헛스윙(Return Sweep)을 감수하면서까지 둥근 원(Circular)의 질서를 강제한 이 결단은, 하드디스크를 넘어 수많은 네트워크 패킷 큐잉 [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)과 [라운드 로빈](/studynote/02_operating_system/03_cpu_scheduling/178_round_robin_scheduling/)(Round-Robin) [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)의 이념적 뿌리가 되었다. 비록 [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)([Seek Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/)) 자체가 존재하지 않는 [NVMe](/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) SSD가 세상을 뒤덮으며 바늘의 동선을 통제하던 C-SCAN의 낭만은 역사 속으로 퇴장하고 있지만, "소외되는 구석 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 없이 모두가 일정한 시간에 응답받아야 한다"는 이 [QoS](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/)([Quality of Service](/studynote/03_network/07_network_layer_routing/388_qos_quality_of_service_best_effort_intserv_diffserv/))의 철학은 차세대 클라우드 로드밸런싱 시스템의 가장 밑바닥에서 영원히 살아남아 세상을 통치할 것이다.

- **📢 섹션 요약 비유**: 모두를 1등으로 만들려다 꼴찌를 굶어 죽게 만든 차가운 천재([SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))의 시대를 지나, 모두가 조금씩 손해를 보더라도 누구 하나 뒤처지는 사람 없이 다 같이 손잡고 똑같은 시간에 결승선을 통과하게 만든 따뜻하고 공평한 복지 시스템(C-SCAN)의 승리입니다. 서버는 1등의 속도가 아니라 꼴찌의 속도로 평가받는 법이니까요.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [SSTF](/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) (Shortest [Seek Time](/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/) First) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| SCAN 스케줄링 ([엘리베이터 알고리즘](/studynote/02_operating_system/08_storage_and_io_systems/471_scan_elevator_scheduling/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| LOOK 및 C-LOOK | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 리눅스 I/O [스케줄러](/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도

```text
[SCAN 스케줄링 (엘리베이터 알고리즘)]
    |
    v
[C-SCAN (Circular SCAN)]
    |
    +---> [LOOK 및 C-LOOK]
    +---> [리눅스 I/O 스케줄러]
```

이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. C-SCAN (Circular SCAN)은 컴퓨터가 디스크와 장치가 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받는 길을 정리하는 방법이에요.
2. 먼저 SCAN 스케줄링 ([엘리베이터 알고리즘](/studynote/02_operating_system/08_storage_and_io_systems/471_scan_elevator_scheduling/))을 이해하면 C-SCAN (Circular SCAN)이 왜 필요한지 더 쉽게 보여요.
3. 그래서 C-SCAN (Circular SCAN)을 잘 알면 나중에 LOOK 및 C-LOOK도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 472 / 800

<- **이전**: [471. SCAN 스케줄링 (엘리베이터 알고리즘) (Scan Elevator Scheduling)](/studynote/02_operating_system/08_storage_and_io_systems/471_scan_elevator_scheduling/)
**다음**: [473. LOOK 및 C-LOOK - 양 끝까지 가지 않고 마지막 요청까지만 이동 후 턴 (SCAN/C-SCAN 최적화)](/studynote/02_operating_system/08_storage_and_io_systems/473_look_c_look_scheduling/) ->

---
