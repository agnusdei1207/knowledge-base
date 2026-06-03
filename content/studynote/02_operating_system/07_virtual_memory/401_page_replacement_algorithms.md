+++
title = "401. 페이지 교체 알고리즘 (Page Replacement Algorithms)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)([Page Replacement Algorithm](/knowledge-base/studynote/02_operating_system/07_virtual_memory/395_page_replacement_algorithm/))은 빈 프레임이 없을 때 발생하는 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) 상황에서, <strong>디스크로 내쫓을 희생양(Victim) <a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a>를 결정하는 운영체제의 생존 수식</strong>이다.
> 2. **가치**: 10만 배의 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 일으키는 디스크 I/O를 최소화하기 위해 <strong>"어떤 놈을 쫓아내야 앞으로 가장 오랫동안 폴트가 안 날까?"</strong>를 통계적으로 예측하여 시스템 전체의 실질 접근 시간(EAT)을 방어한다.
> 3. **융합**: 이상적인 예측 불가의 [OPT](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/)(최적) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 롤모델로 삼아, FIFO의 맹점을 깨고 '지역성(Locality)'에 기반한 <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a>(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">Least Recently Used</a>)</strong>가 등장했으며, 이는 다시 하드웨어의 지원을 받는 근사(Approximation) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)들로 융합되어 현대 OS에 안착했다.

---

## Ⅰ. 개요 및 필요성

- **개념**: 램(RAM)이 꽉 찼을 때 `1. 누굴 버릴 것인가?`, `2. 그 빈자리에 뭘 가져올 것인가?`를 정하는 철학이다. 수많은 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 메모리에 깔려있을 때, 운영체제는 이 살생부 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 돌려 단 한 장의 카드를 스왑(Swap) 디스크로 던져버린다.
- **필요성**: 만약 OS가 무지성으로 "아무거나 맨 앞의 것을 지워!"라고 결정했는데, 하필 그 지워진 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 0.1초 뒤에 또 쓰일 `for` 문의 핵심 변수였다면? 지운 지 0.1초 만에 또 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/)가 터져서 디스크를 긁어와야 한다([스래싱](/knowledge-base/studynote/02_operating_system/04_synchronization/257_thrashing/)). 희생양 하나를 잘못 고른 대가는 무려 <strong>800만 나노초의 <a href="/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/">지연</a></strong>이다. 이 무시무시한 페널티를 막기 위해, OS는 과거의 기록을 샅샅이 뒤져 "가장 쓸모없는 쓰레기"를 골라내는 눈썰미가 필요했다.

  - *[FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 구단주*: "제일 옛날에 입단한 늙은 선수부터 쳐내!" (-> 노련한 주장을 잘라서 팀이 망함).
  - *[OPT](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/) 구단주*: "나는 미래를 보는 초능력자다. 내년에 제일 안 뛸 선수를 쳐내!" (-> 불가능함).
  - *[LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 구단주*: "최근 10경기 동안 한 번도 출전 안 한 놈을 쳐내자. 과거를 보면 미래가 보인다!" (-> 매우 합리적). 

- <strong>등장 배경 및 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a>의 진화 트랙</strong>:
  1. <strong>초창기 (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">FIFO</a>)</strong>: 구현이 쉬워서 그냥 들어온 순서대로 쫓아냈다. (Belady의 모순 터짐).
  2. <strong>이론적 한계점 (<a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/">OPT</a>)</strong>: "미래를 안다면 완벽할 텐데..."라는 기준점을 세움.
  3. **지역성(Locality)의 발견**: "가까운 과거에 쓴 놈은 곧 또 쓴다"는 법칙을 깨닫고, 과거의 빈도([LFU](/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/))나 최근 사용 시점([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))을 추적하는 똑똑한 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로 진화함.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">페이지 교체 알고리즘의 목표: Page Fault 횟수 최소화 시각화</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">상황: 램 프레임 3개 / 호출 스트링: 1 -&gt; 2 -&gt; 3 -&gt; 4 -&gt; 1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ 멍청한 알고리즘 (예: FIFO)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1</div><div class="kb-diagram-node">2</div><div class="kb-diagram-node">3</div><div class="kb-diagram-note">까지 꽉 참.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">'4'가 들어오려 할 때 제일 오래된 '1'을 버림.</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">4</div><div class="kb-diagram-node">2</div><div class="kb-diagram-node">3</div><div class="kb-diagram-note">상태가 됨.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">앗! 바로 다음 호출이 '1'이네? 또 '2'를 버리고 '1'을 가져옴! (폴트 폭발)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ 똑똑한 알고리즘 (예: LRU/OPT)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1</div><div class="kb-diagram-node">2</div><div class="kb-diagram-node">3</div><div class="kb-diagram-note">꽉 찬 상태에서 '4'가 올 때,</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">"1은 1초 뒤에 또 부르니까 절대 안 돼! 아까 쓴 '2'를 버리자!"</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1</div><div class="kb-diagram-node">4</div><div class="kb-diagram-node">3</div><div class="kb-diagram-note">상태가 됨.</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">그다음 호출 '1'이 들어올 때? 어, 램에 이미 있네! (Hit 적중!)</div></div>
</div>
</div>


**[다이어그램 해설]** 이 짧은 예시가 모든 걸 말해준다. OS의 단 한 번의 판단 미스가 연쇄적인 폴트(Cascade Fault)를 낳는다. "누구를 버릴 것인가"는 결국 "누가 가장 오랫동안 내게 필요 없을 것인가"라는 치열한 통계적 미래 예측 게임이다.

- **📢 섹션 요약 비유**: 냉장고(램)가 꽉 찼을 때 새 반찬(새 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/))을 넣기 위해, 유통기한이 제일 오래 남은 반찬을 버리는 게 아니라 "우리 식구가 제일 안 먹을 것 같은 반찬"을 귀신같이 골라내서 버리는 엄마의 눈썰미가 바로 교체 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [Reference](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) String ([참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)열) 기반의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 평가

[알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 평가할 때는 실제 프로그램이 내뿜는 수백만 개의 주소를 다 보지 않는다. 
[페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/)는 '[페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 번호'가 바뀔 때만 일어나므로, 4KB 안에서의 오프셋 변동은 전부 무시하고 오직 <strong>"<a href="/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/">페이지</a> 번호의 순서(<a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">Reference</a> String)"</strong>만을 추출하여 시뮬레이션을 돌린다.

- 주소 트레이스: `0x0100, 0x0150, 0x0200, 0x0100, 0x0400...`
- 이를 100단위 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) 번호로 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/): `1, 1, 2, 1, 4...`
- 연속된 중복 제거: <strong><code>1, 2, 1, 4</code> (이것이 <a href="/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/">참조</a>열!)</strong>
- OS 학자들은 이 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)열을 각 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)에 넣고 돌려서 "누가 폴트(Fault) 횟수가 제일 적은지"를 겨루어 챔피언을 가린다.

---

### [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 분류와 진화 계보

현존하는 모든 교체 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 아래 3가지 철학 중 하나에 뿌리를 두고 있다.

1. **시간 기반 (Time-based)**:
   - <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">FIFO</a> (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">First-In First-Out</a>)</strong>: 가장 먼저 들어온 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 쫓아낸다. (멍청함)
   - <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a> (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">Least Recently Used</a>)</strong>: 가장 오랫동안 '사용([참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/))'되지 않은 놈을 쫓아낸다. (대세)
2. **빈도 기반 (Frequency-based)**:
   - <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/">LFU</a> (<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/">Least Frequently Used</a>)</strong>: 과거에 가장 '적게' 불린 놈을 쫓아낸다. ([참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 횟수 카운트)
   - <strong><a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/410_mfu_algorithm/">MFU</a> (<a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/410_mfu_algorithm/">Most Frequently Used</a>)</strong>: 가장 '많이' 불린 놈을 쫓아낸다. (역발상: 적게 불린 건 방금 올라온 놈일 테니 살려두자).
3. <strong>근사/<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/527_hardware_assisted_virtualization/">하드웨어 보조</a> (Approximation)</strong>:
   - <strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/">Clock</a> (<a href="/knowledge-base/studynote/02_operating_system/07_virtual_memory/407_second_chance_algorithm/">2차 기회 알고리즘</a>)</strong>: LRU가 너무 무거워서, [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)(R [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)) 하나만 가지고 시계바늘을 돌리며 LRU를 '흉내' 낸다. (현대 OS의 실질적 지배자).

- **📢 섹션 요약 비유**: 회사에서 구조조정을 할 때 "제일 오래 다닌 사람을 자르자([FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/))", "실적이 제일 없는 사람을 자르자([LFU](/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/))", "최근 한 달 동안 제일 논 사람을 자르자([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))"라고 기준을 세우며 피 터지게 싸우는 인사팀의 회의와 같습니다.

---

## Ⅲ. 비교 및 연결

### 비교 1: 5대 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 대격돌

면접과 실무를 관통하는 핵심 5대 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 장단점 비교다.

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 교체 기준 (Victim) | 장점 | 단점 및 한계 |
|:---|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/">OPT</a> (최적)</strong> | 앞으로 가장 오랫동안 **안 쓸** [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | [Page Fault](/knowledge-base/studynote/02_operating_system/07_virtual_memory/387_page_fault/) 횟수가 **수학적으로 가장 적음 (1등)** | 미래를 알 수 없어 **구현 불가능** (비교 연구용) |
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/">FIFO</a></strong> | 램에 가장 **먼저** 들어온 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | 구현이 [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) 하나면 끝나서 매우 간단함 | 중요한 변수(가장 먼저 선언됨)가 자꾸 쫓겨나 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 박살 남 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a></strong> | 가장 **오랫동안 안 본** [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | OPT에 가장 근접한 현실적 최강의 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 달성 | 모든 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)의 타임스탬프를 갱신해야 해서 **오버헤드 최악** |
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/">LFU</a></strong> | [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) **횟수가 가장 적은** [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | 장기적인 빈도를 반영하여 합리적임 | 초반에 반짝 쓰인 찌꺼기 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)가 카운트만 높아서 평생 안 쫓겨남 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/">Clock</a> (2차 기회)</strong>| [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 0인 (최근 안 쓴) [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) | LRU와 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)은 비슷한데 **오버헤드가 거의 없음** | **현대 OS(리눅스, 맥)가 채택한 최종 승리자** |

### 왜 빈도([LFU](/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/), [MFU](/knowledge-base/studynote/02_operating_system/07_virtual_memory/410_mfu_algorithm/))는 멸종했는가?

[LFU](/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/)(최소 빈도)는 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적으로 완벽해 보이지만, 실제 프로그램의 '페이즈 트랜지션(Phase Transition)'을 반영하지 못한다.
- **상황**: 프로그램 초반에 `Init()` 함수가 불리며 1만 번 호출되었다(카운트 10000). 이후 게임이 시작되며 `Draw()` 함수가 100번 불렸다(카운트 100).
- 램이 모자라서 쫓아내야 할 때, LFU는 카운트가 100밖에 안 되는 `Draw()` 함수를 쫓아낸다!
- 정작 `Init()`은 초기화 끝나서 영원히 안 쓸 쓰레기인데 카운트가 10000이라서 램에 영원히 알박기를 해버린다. 이 치명적인 맹점 때문에 카운팅 기반 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 교과서에서나 배우고 실제 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/)에선 쓰이지 않는다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">평가 요소</div><div class="kb-diagram-cell">LRU (최근)</div><div class="kb-diagram-cell">LFU (빈도)</div><div class="kb-diagram-cell">Clock (근사)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">찌꺼기 처리</div><div class="kb-diagram-cell">완벽 (즉시 버림)</div><div class="kb-diagram-cell">최악 (알박기 함)</div><div class="kb-diagram-cell">훌륭 (서서히 버림)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">하드웨어 짐</div><div class="kb-diagram-cell">무거움 (시간 기록)</div><div class="kb-diagram-cell">무거움 (숫자 더함)</div><div class="kb-diagram-cell">가벼움 (비트 1개)</div></div>
</div>
</div>


**[매트릭스 해설]** 컴퓨터 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 세계에서 "과거의 기억(Time)"이 "과거의 누적 횟수(Frequency)"를 이긴 대표적인 사례다. 그리고 그 무거운 시간 기록조차 버리고, "최근에 썼어(1) 안 썼어(0)?"라는 극단적 흑백 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)([Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/))로 최적화한 것이 공학의 승리다.

- **📢 섹션 요약 비유**: 옷장 정리할 때 "내가 이 옷을 살면서 총 100번 입었지([LFU](/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/))" 하며 고집부리는 사람은 유행 지난 촌스러운 옷을 평생 못 버립니다. 반면 "이 옷 안 입은 지 1년 넘었네([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))" 하며 쿨하게 버리는 사람이 옷장을 항상 트렌디([Working Set](/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/))하게 유지합니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오: [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) 및 웹 캐시([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/), Memcached)에서의 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)
- **상황**: OS의 [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리뿐만 아니라, 백엔드 개발자가 쓰는 메모리 캐시 DB([Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/))에서도 이 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 100% 똑같이 적용된다.
- <strong>Redis의 <code>maxmemory-policy</code></strong>: 
  - [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 램을 2GB로 제한해 두었는데 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 꽉 찼다.
  - 이때 [Redis](/knowledge-base/studynote/05_database/04_transactions_concurrency/542_redis/) 설정에 `allkeys-lru`를 주면, 수백만 개의 [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) 중 가장 오랫동안 조회(GET)되지 않은 Key부터 쓰레기통에 버리며 새로운 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 받는다.
  - 만약 `volatile-lfu`를 주면 조회 빈도(횟수)가 적은 놈부터 버린다.
  - **결론**: 캐시 시스템을 운영하는 엔지니어는 자신의 비즈니스가 '최근 뜬 핫이슈 뉴스([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 유리)'인지, '스테디셀러 상품([LFU](/knowledge-base/studynote/02_operating_system/04_synchronization/263_lfu_page_replacement/) 유리)'인지 파악하여 이 교체 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)을 튜닝하는 것이 실무 1순위 역량이다.

### [Database](/knowledge-base/studynote/05_database/04_transactions_concurrency/501_database/) 버퍼 풀(Buffer Pool)의 변종 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) (Midpoint Insertion)
MySQL의 InnoDB 스토리지 엔진은 단순한 LRU를 쓰지 않는다.
- 누군가 100GB짜리 테이블을 `SELECT *`로 풀 스캔(Full Scan) 해버리면?
- 100GB의 쓰레기 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 들어오면서 기존에 잘 쓰고 있던 캐시를 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)에 의해 모조리 다 밀어내버린다(Buffer Pool Pollution).
- 이를 막기 위해 MySQL은 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/) 리스트를 Old/[New](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 구역으로 나누고, 새로 들어온 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 머리(Head)가 아니라 **중간(Midpoint)에 꽂아 넣어서**, 진짜 자주 불리는 놈만 [New](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 구역으로 살려주는 <strong>'변형 <a href="/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/">LRU</a>'</strong>를 독자적으로 쓴다. (실무 DB 최적화의 정수다).

- **📢 섹션 요약 비유**: 식당 매니저(MySQL)가 일반 손님(단순 [LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))은 문 앞 대기석(Old 구역)에 먼저 앉히고, 진짜 단골(자주 찔리는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))인 걸 확인해야만 VIP석([New](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 구역)으로 모십니다. 웬 뜨내기 단체 손님(풀 스캔) 100명이 우르르 몰려와도 VIP석 손님은 절대 쫓겨나지 않게 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)하는 고급 관리 스킬입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| **EAT(실질 접근 시간) 방어** | 디스크 I/O를 유발하는 [페이지 폴트](/knowledge-base/studynote/02_operating_system/11_exam_summary/720_page_fault_isr/) [확률](/knowledge-base/studynote/08_algorithm_stats/08_stats/130_probability/)($p$)을 기하급수적으로 낮추어 메모리 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 램 스피드에 수렴시킴 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/">워킹 셋</a>(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/265_working_set/">Working Set</a>) 유지</strong> | 프로세스의 런타임 행동 패턴(지역성)을 귀신같이 추적하여, 당장 필요한 핵심 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 절대 램에서 쫓겨나지 않게 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) |
| **캐시 경제학의 표준 정립**| 하드웨어 L1 캐시부터 [CDN](/knowledge-base/studynote/03_network/09_application_layer_web_email/506_cdn_content_delivery_network_edge_caching/) 클라우드 서버까지, 모든 '용량 제한 저장소'가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 관리하는 절대적인 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 뼈대를 제공 |

### 결론 및 미래 전망

[페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Page Replacement](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) Algorithms)은 "모든 것을 가질 수 없다면, 가장 쓸모없는 것부터 우아하게 버려라"라는 컴퓨터 과학의 미니멀리즘 철학이다. 완벽한 예지력([OPT](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/))을 갈망했던 인간은 결국 하드웨어의 벽에 막혀 과거를 돌아보는 지혜([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))를 택했고, 그마저도 무거워 시곗바늘을 돌리는 근사치([Clock](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/))와 타협했다. 이 타협의 역사는 완벽함보다 '가성비([Heuristics](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/210_heuristics_scheduling/))'가 시스템 설계에서 얼마나 중요한지를 가르쳐 준다. 향후 기계학습(ML) 칩이 발전하면, CPU 내부에서 OS 대신 인공지능이 프로그램의 동작 패턴을 학습하여 "3초 뒤에 이 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/)를 버리게 될 거야"라고 [OPT](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/)([최적 교체](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/301_opt_replacement/))에 한없이 수렴하는 예측을 던져주는 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 기반 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) 시대가 열릴 것이다.

- **📢 섹션 요약 비유**: 다이어트할 때 "이 세상 모든 맛있는 걸 먹으면서 살을 빼겠다([OPT](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/))"는 불가능한 꿈을 버리고, "어제 안 먹은 야채를 먹고 오늘 찐 살은 버린다([LRU](/knowledge-base/studynote/02_operating_system/04_synchronization/262_lru_page_replacement/))"는 현실적인 타협을 통해 건강(시스템 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))을 유지해 나가는 현명한 생존 전략입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [전역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/) ([Global Replacement](/knowledge-base/studynote/02_operating_system/07_virtual_memory/399_global_replacement/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [지역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/400_local_replacement/) ([Local Replacement](/knowledge-base/studynote/02_operating_system/07_virtual_memory/400_local_replacement/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [최적 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/402_optimal_page_replacement/) ([OPT](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/), Optimal) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| 벨라디의 모순 (Belady's [Anomaly](/knowledge-base/studynote/05_database/04_transactions_concurrency/530_anomaly/)) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">지역 교체 (Local Replacement)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">페이지 교체 알고리즘 (Page Replacement Algorithms)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">최적 교체 알고리즘 (OPT, Optimal)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">벨라디의 모순 (Belady's Anomaly)</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Page Replacement](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) Algorithms)은 컴퓨터가 메모리를 더 크게 보이게 하고 부족함을 숨기는 방법이에요.
2. 먼저 [지역 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/400_local_replacement/) ([Local Replacement](/knowledge-base/studynote/02_operating_system/07_virtual_memory/400_local_replacement/))을 이해하면 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Page Replacement](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) Algorithms)이 왜 필요한지 더 쉽게 보여요.
3. 그래서 [페이지 교체](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) ([Page Replacement](/knowledge-base/studynote/02_operating_system/04_synchronization/260_page_replacement/) Algorithms)을 잘 알면 나중에 [최적 교체 알고리즘](/knowledge-base/studynote/02_operating_system/07_virtual_memory/402_optimal_page_replacement/) ([OPT](/knowledge-base/studynote/02_operating_system/11_exam_summary/724_optimal_page_replacement_unrealizable/), Optimal)도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 401 / 800

← **이전**: [400. 지역 교체 (Local Replacement) - 자신의 프레임 풀 내에서만 교체](/knowledge-base/studynote/02_operating_system/07_virtual_memory/400_local_replacement/)
**다음**: [402. 최적 교체 알고리즘 (OPT, Optimal) - 앞으로 가장 오랫동안 안 쓸 페이지 교체 (구현 불가, 비교 기준)](/knowledge-base/studynote/02_operating_system/07_virtual_memory/402_optimal_page_replacement/) →

---
