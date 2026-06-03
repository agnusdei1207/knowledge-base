+++
title = "471. SCAN 스케줄링 (엘리베이터 알고리즘) (Scan Elevator Scheduling)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SCAN 스케줄링은 하드디스크 바늘(Head)이 <strong>엘리베이터처럼 한쪽 방향으로 끝까지 쭉 밀고 가면서 가는 길에 있는 모든 요청을 싹쓸이한 뒤, 디스크 끝에 도달하면 방향을 틀어 반대쪽 끝까지 싹쓸이하는 가장 본능적이고 상식적인 디스크 큐잉 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a></strong>이다.
> 2. **가치**: 가까운 놈만 쫓다 바늘이 한곳에 갇혀버리는 [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/)(최단 거리 우선)의 치명적인 <strong>'기아 현상(<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/">Starvation</a>)'을 원천 봉쇄</strong>하면서도, 바늘이 널뛰는 [FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/)(순차 처리)의 비효율성을 박살 내어 <strong>공평성(Fairness)과 <a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">처리량</a>(<a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/139_throughput/">Throughput</a>)의 황금 비율을 달성</strong>했다.
> 3. **융합(한계)**: 하지만 엘리베이터가 양 끝을 찍고 돌아올 때, 방금 막 지나친 가운데 구역의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)들이 다음 차례가 올 때까지 너무 오래 기다려야 하는 불균형([Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/))이 존재하여, 훗날 <strong><a href="/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/">C-SCAN</a>(<a href="/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/">단방향</a> 스위핑)이나 LOOK(끝까지 안 가고 꺾기) 같은 현대적 변종 아키텍처로 진화하는 튼튼한 뼈대 역할</strong>을 했다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 디스크 헤드는 0번 트랙(가장자리)부터 199번 트랙(중심) 사이를 오간다. SCAN은 바늘이 움직이는 방향(Direction)에 절대적인 락([Lock](/knowledge-base/studynote/05_database/04_transactions_concurrency/510_lock/))을 건다. 바늘이 0번에서 199번을 향해(안쪽으로) 움직이기 시작했다면, 중간에 큐([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/))에 나보다 뒤에 있는(바깥쪽) 아무리 가까운 요청이 들어와도 절대 방향을 꺾지 않는다. 199번 끝을 찍은 뒤에야 "하행선입니다~" 하고 방향을 꺾어 바깥쪽으로 내려오면서 요청을 줍는다.
- **필요성**: 이전 세대의 에이스였던 [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/)(가장 가까운 곳 먼저)는 미친 효율을 자랑했지만, 특정 구역에 요청이 몰리면 반대쪽 구역의 요청이 평생 처리되지 못하는 '기아 현상([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/))'을 낳았다. OS의 존재 이유는 효율보다 '[신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)'이다. 1주일째 응답 없는 앱이 있는 서버는 아무도 쓰지 않는다. "모든 요청이 언젠가는 무조건 처리된다는 보장(공평성)을 주면서도, 바늘이 낭비 없이 움직이게 할 방법이 없을까?"라는 딜레마 속에서, 인류가 매일 타는 '엘리베이터의 움직임'을 컴퓨터에 그대로 복사해 넣은 천재적인 휴리스틱이 탄생했다.

- <strong>등장 배경 및 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>의 진화</strong>:
  1. **FCFS의 무지성**: 순서만 지키려다 기계 모터가 타버림.
  2. **SSTF의 탐욕**: 효율만 따지다 구석진 곳의 앱이 굶어 죽음([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/)).
  3. **SCAN의 중용**: "방향성"이라는 제약 조건을 하나 강제함으로써, 동선 낭비도 막고 굶어 죽는 앱도 없애는 완벽한 타협점을 찾아냄.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">SCAN (엘리베이터) 알고리즘의 우아한 동선 시각화</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">큐 요청 순서</div><div class="kb-diagram-note">: 98, 183, 37, 122, 14, 124</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">헤드 위치</div><div class="kb-diagram-note">: 53번 트랙 /</div><div class="kb-diagram-node">현재 방향</div><div class="kb-diagram-note">: 0번을 향해 하행 중!</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ SCAN 발동: "무조건 끝(0번)까지 내려가면서 다 줍고, 그다음 꺾어라!"</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">14 37 53 98 122 124 183</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">0 │</div><div class="kb-diagram-node">시작</div><div class="kb-diagram-note">│ │ │ 199</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶①</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶②</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">──▶③</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶④</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">✅ 이동 경로: 53 -&gt; 37 -&gt; 14 -&gt; 0(끝점 찍기!) -&gt; 98 -&gt; 122...</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">🌟 특징: SSTF처럼 와이퍼가 요동치지 않고, 끝을 찍을 때까지 묵묵히 전진함.</div></div>
</div>
</div>


**[다이어그램 해설]** 이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 가장 중요한 특징은 <strong>"0번(또는 199번)이라는 디스크의 물리적 끝점(End Point)을 무조건 찍고 돌아온다"</strong>는 것이다. 큐에 14번까지만 요청이 들어왔음에도 불구하고, SCAN은 14번을 처리한 뒤 멈추지 않고 아무런 요청도 없는 0번 벽까지 쿵! 하고 찍은 뒤에야 방향을 틀어 올라간다. 이 융통성 없는 끝점 찍기가 훗날 LOOK [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 진화하게 되는 빌미가 된다.

- **📢 섹션 요약 비유**: 청소 로봇(SCAN)이 거실을 청소할 때, 쓰레기(요청)가 있는 곳만 쫓아다니며 핑퐁 치는 게([SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/)) 아니라, 벽 끝에서 반대쪽 벽 끝까지 지그재그로 우직하게 밀고 나가며 전체를 훑습니다. 설령 벽 근처에 쓰레기가 없어도 일단 벽을 쿵 찍고 돌아섭니다. 쓰레기를 하나도 놓치지 않는 확실한 청소법입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 기아 현상 ([Starvation](/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/))의 수학적 박멸

SSTF에서 구석에 있던 999번 요청이 굶어 죽었던 이유는, 바늘이 50번대에서만 계속 맴돌았기 때문이다.
SCAN [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 하에서는 이 악순환이 수학적으로 불가능하다.
- 바늘이 50번에서 상행(오른쪽)으로 출발했다.
- 50번대에서 새로운 요청이 1초에 1만 개씩 쏟아져 들어온다 치자.
- SCAN [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 이 1만 개의 요청을 <strong>"현재 <a href="/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/">진행</a> 방향(상행)에 있는가?"</strong>로 필터링한다.
- 바늘은 50 -> 51 -> 52로 계속 전진하므로, 50번 자리에 새 요청이 아무리 많이 들어와도 뒤를 돌아보지 않는다.
- 결국 바늘은 무조건 999번(디스크 끝)에 도달하게 되어 있으며, <strong>디스크의 어떤 구석에 박힌 요청이라도 최대 '디스크 1왕복 시간' 안에는 무조건 처리된다는 강력한 시간 상한선(Upper Bound)</strong>이 보장된다.

---

### 불균형의 저주 ([Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) Problem)

SCAN은 공평해 보이지만 위치에 따라 대기 시간이 로또급으로 차이 나는 치명적인 구조적 결함을 안고 있다.
- **가운데(50번) 위치의 꿀 혜택**: 바늘이 상행할 때 1번, 하행할 때 1번 지나간다. 즉, 바늘이 전체를 왕복하는 동안 중간에 있는 트랙은 아주 짧은 주기로 2번이나 바늘의 은혜를 입는다.
- **양 끝단(0번, 199번) 위치의 피눈물**: 바늘이 199번을 찍고 0번으로 출발했다. 하필 그 직후 198번에 새로운 요청이 들어왔다. 이 불쌍한 198번 요청은 바늘이 저 멀리 0번 끝까지 갔다가 다시 199번으로 돌아올 때까지 <strong>디스크 전체 왕복 시간의 2배(Maximum Delay)</strong>를 꼬박 기다려야 한다.
- **결론**: SCAN은 양 끝단 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에게 너무 가혹하며, [응답 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)의 편차([Variance](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/))가 위치에 따라 심하게 요동친다.

- **📢 섹션 요약 비유**: 강남역(가운데)에 서 있으면 서울행 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)와 부산행 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 수시로 지나가서 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 타기가 엄청 쉽습니다. 하지만 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 종점(디스크 양 끝)에 사는 사람은 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 한 번 떠나버리면 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)가 반대쪽 종점을 찍고 다시 돌아올 때까지 하루 종일 정류장에서 떨어야 하는 끔찍한 차별 대우를 받게 됩니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) vs SCAN

현업 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)의 역사에서 가장 치열했던 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 대결이다.

| 비교 척도 | [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) (Shortest [Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/) First) | SCAN (엘리베이터) |
|:---|:---|:---|
| **이동 철학** | "무조건 내 눈앞에 가까운 놈 먼저!" | "무조건 방향 안 꺾고 일직선으로 쭉 밀기!" |
| <strong>기아(<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/">Starvation</a>)</strong> | ☠️ 심심하면 터짐 (치명적 약점) | **🟢 절대 안 터짐 (완벽 방어)** |
| <strong>평균 <a href="/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/">탐색 시간</a></strong> | 수학적으로 가장 짧음 (효율 최상) | SSTF보다 살짝 길지만 훌륭함 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/">응답 시간</a> <a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a></strong> | 극단적으로 심함 (1초 ~ 영원히) | **양 끝단 차별은 있지만 SSTF보단 훨씬 일정함** |

### 데드라인([Deadline](/knowledge-base/studynote/02_operating_system/11_exam_summary/766_realtime_scheduling_deadline/)) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)로의 진화
리눅스는 SCAN의 "끝단 차별 문제"를 해결하기 위해 가만히 있지 않았다.
아무리 SCAN을 돌려도, 특정 요청이 큐에 들어온 지 너무 오래되어 굶어 죽기 일보 직전이라면? 
리눅스의 <strong><a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/766_realtime_scheduling_deadline/">Deadline</a> <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a></strong>는 엘리베이터(SCAN) 큐 옆에, <strong>시간 초시계가 달린 <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">FIFO</a> 큐(Read 500ms, Write 5초 제한)</strong>를 하나 더 몰래 놔둔다. 평소엔 엘리베이터처럼 예쁘게 처리하다가, 구석탱이 요청이 데드라인(500ms)을 넘겨서 비명을 지르면, 엘리베이터 방향이고 뭐고 깡그리 무시하고 즉시 그쪽으로 바늘을 꺾어버려 응답 지연의 상한선을 철통같이 방어한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">상황</div><div class="kb-diagram-cell">SSTF의 대처</div><div class="kb-diagram-cell">SCAN의 대처</div><div class="kb-diagram-cell">Deadline의 대처</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">구석에 요청옴</div><div class="kb-diagram-cell">무시함 (효율)</div><div class="kb-diagram-cell">가던 길 다 가고 감</div><div class="kb-diagram-cell">가던 길 다 가고 감</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1분째 굶는 중</div><div class="kb-diagram-cell">☠️ 계속 무시함</div><div class="kb-diagram-cell">가던 길 다 가고 감</div><div class="kb-diagram-cell">🚀 즉시 꺾어서 감</div></div>
</div>
</div>


**[매트릭스 해설]** 컴퓨터 시스템에서 "언젠가 처리해 줄게(SCAN)"는 완벽한 정답이 아니다. "최소 0.5초 안에는 무조건 처리해 줄게([Deadline](/knowledge-base/studynote/02_operating_system/11_exam_summary/766_realtime_scheduling_deadline/))"라는 하드 타임 리밋(Time Limit)이 있어야만 실시간 오디오/비디오 스트리밍이 끊기지 않는 엔터프라이즈 OS로 인정받는다.

- **📢 섹션 요약 비유**: [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 기사(SCAN)가 정해진 노선대로만 차를 몹니다. 그런데 저기 정류장에 임산부(데드라인 임박 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))가 쓰러져 가고 있습니다. 규칙을 깨고 차를 돌려([SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) 꺾기) 임산부부터 병원으로 이송하는 융통성([Deadline](/knowledge-base/studynote/02_operating_system/11_exam_summary/766_realtime_scheduling_deadline/) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/))이 있어야 진정한 명품 시스템입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: [HDD](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/465_hdd_structure/) 서버의 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 시스템 조각화와 SCAN의 위력
1. **문제 상황**: [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [백업](/knowledge-base/studynote/02_operating_system/09_file_system/555_backup_and_restore_strategy/) [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 10GB를 하드디스크에 쓰는데, 하드디스크가 오래되어 빈 공간이 1번, 50만 번, 10만 번으로 조각조각 찢어져 있다.
2. **OS의 큐잉**: 커널은 이 10GB를 4KB씩 250만 개의 I/O 요청으로 찢어서 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 큐에 던진다. 
3. **SCAN의 무쌍 (Elevator Sweep)**:
   - 만약 FCFS였다면 바늘이 1번 갔다가 50만 번 갔다가 10만 번 가면서 헤드 모터가 타버렸을 것이다.
   - 하지만 SCAN [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)(CFQ의 뼈대)는 이 250만 개의 지저분한 요청을 트랙 번호순으로 싹 정렬한다.
   - 그리고 디스크 0번부터 끝번까지 바늘을 부드럽게 1바이트 쓱~ 밀고 지나가며 250만 개의 흩어진 조각들을 마치 원래 하나였던 것처럼 빛의 속도로 긁어모은다.
4. **결과**: 이 엘리베이터의 스위핑(Sweeping) 효과 덕분에, 물리적으로 파편화된 디스크라도 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 큐 깊이([Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) Depth)만 깊게 세팅해 주면 순차 읽기(Sequential Read)에 버금가는 막강한 스루풋을 뽑아낼 수 있다.

### SSD에서의 엘리베이터 퇴출
앞서 말했듯 SSD는 바늘이 없다. 1번을 찌르나 50만 번을 찌르나 속도가 같다. [SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/) 앞단에서 엘리베이터(SCAN) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 돌리며 번호순으로 예쁘게 줄을 세우는 짓은, 그 줄 세우는 연산(Sorting) 자체가 CPU 낭비다. 현대 리눅스는 하드웨어가 [NVMe](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/482_nvme/) SSD임을 감지하는 순간, 이 위대했던 엘리베이터 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)를 즉각 폐기하고 `none/noop` (아무 짓도 안 하고 들어온 대로 던지기) [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)로 자동 전환해 버린다.

- **📢 섹션 요약 비유**: 엘리베이터 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/)는 층계참을 오르내리는 '무거운 기계식 관성'이 있을 때만 의미가 있습니다. 내가 10층짜리 건물에서 층간 순간 이동 포탈([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))을 얻었는데, 굳이 "효율을 위해 1층부터 10층까지 순서대로 줍자"라며 머리를 싸매고 동선 계획을 짜는 건 그야말로 시간 낭비, 뻘짓의 극치입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| <strong>기아(<a href="/knowledge-base/studynote/02_operating_system/05_deadlock/314_starvation_prevention/">Starvation</a>) 현상 원천 멸종</strong> | 디스크 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 방향이 끝을 찍고 무조건 돌아오므로, 어떤 악성 트래픽이 몰려도 특정 I/O가 영원히 소외되는 시스템 버그 완전 소거 |
| **디스크 기계 장치 수명 보존** | 바늘이 이리저리 꺾이는 급발진/급정거 빈도를 최소화하여, [데이터센터](/knowledge-base/studynote/03_network/16_data_center_cloud/801_data_center_3_tier_architecture_core_aggregation_access/) 내 수십만 대 하드디스크의 액추에이터 마모와 발열을 극적으로 낮춤 |
| <strong>현대 I/O <a href="/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/">스케줄러</a>의 아키텍처 원형</strong>| 이후 파생된 [C-SCAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/), LOOK, CFQ 등 모든 진보된 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) [디스크 스케줄링](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/468_disk_scheduling_purpose/) 기법들이 이 '[단방향](/knowledge-base/studynote/03_network/01_data_communication/008_단방향_반이중_전이중/) 싹쓸이' 철학을 복사해 감 |

### 결론 및 미래 전망

SCAN 스케줄링 (엘리베이터 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))은 인류가 발명한 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 중 일상생활의 직관(엘리베이터)이 컴퓨터 아키텍처에 100% 동일하게 이식되어 대성공을 거둔 가장 아름답고 고전적인 사례다. "가까운 것을 좇는 인간의 탐욕([SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/))"이 낳은 불평등을 "한 방향으로 끝까지 간다"는 기계적인 규칙 하나로 우아하게 통제하며, 시스템 공학에서 효율성(Efficiency)과 공평성(Fairness)이라는 영원한 두 마리 토끼의 황금 타협점을 찾아냈다. 낸드 플래시([SSD](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/327_ssd/))의 폭발적인 보급으로 바늘이 움직이는 [탐색 시간](/knowledge-base/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/)([Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/)) 자체가 0초가 되며 이 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 본래 목적은 역사의 박물관으로 향하고 있다. 그러나 디스크 바늘은 사라졌을지언정, "수많은 요청을 큐에 모은 뒤 한 방향으로 정렬하여 배치(Batch) 처리한다"는 이 위대한 스위핑(Sweeping) 철학은 현대의 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [쿼리](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 옵티마이저나 네트워크 패킷 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 깊숙한 곳에 영원한 영혼으로 살아 숨 쉬고 있다.

- **📢 섹션 요약 비유**: 엘리베이터가 "내려가는 길이니까 올라가는 버튼은 무시하고 일단 1층까지 쭉 가겠습니다"라고 하는 건, 당장 올라가고 싶은 내 입장에선 답답한 일입니다. 하지만 그렇게 룰을 지키지 않고 부르는 대로 휙휙 꺾으면 건물 전체 사람들이 영원히 엘리베이터를 못 타게 됩니다. SCAN은 개인의 답답함을 시스템 전체의 질서로 승화시킨 거대한 사회적 약속입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [FCFS](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/173_fcfs_scheduling/) (First-Come, First-Served) 스케줄링 | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) (Shortest [Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/) First) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [C-SCAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) ([Circular SCAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| LOOK 및 C-LOOK | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">SSTF (Shortest Seek Time First)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">SCAN 스케줄링 (엘리베이터 알고리즘) (Scan Elevator Scheduling)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">C-SCAN (Circular SCAN)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">LOOK 및 C-LOOK</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. SCAN 스케줄링 (엘리베이터 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) (Scan Elevator Scheduling)은 컴퓨터가 디스크와 장치가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 주고받는 길을 정리하는 방법이에요.
2. 먼저 [SSTF](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/) (Shortest [Seek Time](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/467_disk_access_time/) First)을 이해하면 SCAN 스케줄링 (엘리베이터 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) (Scan Elevator Scheduling)이 왜 필요한지 더 쉽게 보여요.
3. 그래서 SCAN 스케줄링 (엘리베이터 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)) (Scan Elevator Scheduling)을 잘 알면 나중에 [C-SCAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) ([Circular SCAN](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/))도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 471 / 800

← **이전**: [470. SSTF (Shortest Seek Time First) - 현재 헤드 위치에서 가장 가까운 요청 처리 (기아 발생 가능)](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/470_sstf_disk_scheduling/)
**다음**: [472. C-SCAN (Circular SCAN) - 한 방향으로만 처리하고 끝에 도달하면 시작점으로 빠르게 복귀 (대기 시간 균등화)](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/472_c_scan_scheduling/) →

---
