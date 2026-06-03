+++
title = "366. 세그멘테이션과 외부 단편화 (가변 크기이므로 재발생) (Segmentation External Fragmentation)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 기법은 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 의미(함수, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 등)를 보존하기 위해 조각의 크기를 무작위(가변 크기)로 잘라내기 때문에, 이 조각들을 물리 메모리에 적재하고 해제하는 과정에서 필연적으로 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">외부 단편화</a>(<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">External Fragmentation</a>)가 완벽하게 부활</strong>하게 된다.
> 2. **가치(한계)**: 프로그래머 친화적인 훌륭한 보안/공유 메커니즘을 갖췄음에도 불구하고, 이 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)가 유발하는 '메모리 할당 실패([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))'와 이를 해결하기 위한 '[압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)([Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)) 오버헤드'를 견디지 못하고 시스템 아키텍처의 주류에서 밀려났다.
> 3. **융합**: 이 치명적 한계를 극복하기 위해, 세그먼트를 1차로 자른 뒤 그 조각을 다시 4KB 고정 페이지로 잘게 찢어 물리 메모리에 넣는 <strong>'<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a> 기반 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/">세그멘테이션</a>(<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/367_paged_segmentation/">Paged Segmentation</a>)'</strong> 이라는 융합형 진화 아키텍처를 탄생시키는 원인이 되었다.

---

## Ⅰ. 개요 및 필요성

- **개념**: [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)은 코드 조각을 의미 단위로 자르기 때문에 각 세그먼트의 크기(Limit)가 10KB, 50MB, 2MB 등 제각각이다. 이 가변적인 덩어리들이 메모리에 들어왔다 나갔다를 반복하면, 남는 빈 공간(Hole)들 역시 제각각의 크기로 메모리 전역에 흩어지게 된다. 전체 남은 용량은 충분하지만 쪼개져 있어서 새 세그먼트가 못 들어가는 현상이 바로 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)다.
- **필요성(해결의 필요성)**: [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/)이 등장하여 4KB 깍둑썰기로 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)를 멸종시켰으나, 의미 없이 찢어진 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)들 때문에 보안과 공유가 힘들어졌다. "다시 의미 단위로 자르는 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)으로 돌아가자!"며 도입을 시도했지만, 과거 [연속 메모리 할당](/knowledge-base/studynote/02_operating_system/06_memory_management/338_contiguous_memory_allocation/)([가변 분할 방식](/knowledge-base/studynote/02_operating_system/06_memory_management/340_variable_partition/)) 시절 사람들을 미치게 했던 '[외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) 지옥'이 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 환경에서 정확히 똑같이 재현되었다. 시스템이 멈추지 않으려면 이 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)를 관리할 특단의 대책이 필요했다.

- **발생 구조의 회귀**:
  1. <strong>가변 분할(<a href="/knowledge-base/studynote/02_operating_system/09_file_system/523_contiguous_allocation/">연속 할당</a>)의 악몽</strong>: 하나의 큰 프로그램 덩어리들이 들락거리며 파편화 발생.
  2. <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/">세그멘테이션</a>(비연속 할당)의 착각</strong>: 프로그램을 3~4개의 조각(세그먼트)으로 찢어서 비연속으로 넣으면 [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)가 줄어들 줄 알았다.
  3. **재앙의 부활**: 찢어놓은 조각들조차 크기가 제각각이었기 때문에, 결국 <strong>각 조각 단위(세그먼트 단위)로 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">외부 단편화</a>가 또다시 발생</strong>했다. 근본적인 '크기의 획일화'가 없이는 [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/)를 막을 수 없다는 공학적 진리가 증명된 셈이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">세그멘테이션 환경에서의 외부 단편화 발생 시뮬레이션</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">프로세스들의 세그먼트 적재 상태</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">물리 램</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Seg_A1</div><div class="kb-diagram-cell">▒ 빈공간 ▒</div><div class="kb-diagram-cell">Seg_B1</div><div class="kb-diagram-cell">▒ 빈공간 ▒</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">(10MB)</div><div class="kb-diagram-cell">(5MB)</div><div class="kb-diagram-cell">(15MB)</div><div class="kb-diagram-cell">(8MB)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">▶ 남은 공간 총합 = 5MB + 8MB = 13MB</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">새로운 세그먼트의 등장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">프로세스 C의 "데이터 세그먼트(10MB)"가 램에 올라오려 함.</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">할당기의 절망</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">"전체 공간은 13MB나 남았는데, 10MB짜리 덩어리가 들어갈 '연속된'</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">빈방이 하나도 없다. 적재 실패 (OOM Error)!"</div></div>
</div>
</div>


**[다이어그램 해설]** 가변 분할의 저주가 100% 동일하게 재현되었다. [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)은 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 주소를 찢었을 뿐, 결국 '하나의 세그먼트는 물리 메모리상에서 무조건 연속되어야 한다'는 치명적 제약을 가지고 있기 때문이다. 10MB짜리 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 세그먼트는 반드시 10MB의 연속된 물리 프레임을 요구하며, 빈 공간이 찢어져 있으면 단 1바이트도 들어갈 수 없다.

- **📢 섹션 요약 비유**: 주차장에 차를 댈 때, "경차, 중형차, 대형차" 크기별로 선을 안 긋고 차가 오는 대로 바짝 대게([세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)) 했더니, 나중에 대형차가 나간 자리에 경차 2대가 들어가고 애매한 공간이 남아서 결국 캠핑카가 못 들어오게 되는 주차장 파편화 현상입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 동적 메모리 할당 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 재등판

[외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)가 발생했으니, 빈 구멍(Hole)들을 어떻게 알뜰하게 쓸 것인지 뼈아픈 고민이 다시 시작된다. 운영체제는 가변 분할 시절에 쓰던 동적 할당 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 3형제를 그대로 다시 꺼내 든다.

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)에서의 작동 방식 | 결과 및 부작용 |
|:---|:---|:---|
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/344_first_fit/">최초 적합</a> (<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/344_first_fit/">First-fit</a>)</strong> | 빈 구멍 리스트를 뒤지다 세그먼트 크기보다 큰 첫 구멍에 냅다 쑤셔 넣음 | 속도는 가장 빠르나, 결국 메모리의 1/3이 버려지는 <strong>50% 법칙</strong>의 저주를 피할 수 없음 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/345_best_fit/">최적 적합</a> (<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/345_best_fit/">Best-fit</a>)</strong> | 세그먼트 크기와 가장 딱 맞는 구멍을 찾아 넣음 | 공간을 아끼려다 수십 바이트짜리 영원히 못 쓰는 <strong>악성 미세 <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/">단편화</a></strong>를 무수히 양산함 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/346_worst_fit/">최악 적합</a> (<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/346_worst_fit/">Worst-fit</a>)</strong> | 남은 구멍이 가장 큰 곳을 일부러 골라 쪼갬 | 가장 거대한 빈 공간마저 파괴하여 나중에 들어올 거대 세그먼트를 굶겨 죽임 |

---

### 치명적 오버헤드: 메모리 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) ([Compaction](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/))

First-fit을 쓰든 Best-fit을 쓰든 결국 메모리가 찢어져서 [OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)([Out of Memory](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/))이 발생한다. 이때 시스템이 죽는 것을 막을 유일한 물리적 해결책은 <strong>'메모리 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>(<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">Compaction</a>)'</strong>뿐이다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">외부 단편화 해소를 위한 압축 (Compaction) 오버헤드</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">1. 파편화 상태</div><div class="kb-diagram-node">Seg1(10M)</div><div class="kb-diagram-node">빈 5M</div><div class="kb-diagram-node">Seg2(15M)</div><div class="kb-diagram-node">빈 8M</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">2. OS의 압축 발동 (시스템 전체 멈춤 - Stop The World)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- Seg2(15M)의 데이터를 물리적으로 5MB 앞쪽으로 긁어서 복사(Memcpy)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">3. 세그먼트 테이블(STBR) 폭풍 업데이트</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">- Seg2의 Base 주소가 바뀌었으므로 장부 값도 동기화 갱신!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-node">4. 압축 완료</div><div class="kb-diagram-node">Seg1(10M)</div><div class="kb-diagram-node">Seg2(15M)</div><div class="kb-diagram-node">거대한 빈 공간 13M</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">⚠ 치명상: 15MB를 램에서 복사하는 수백만 클럭 동안 CPU는 마비 상태.</div></div>
</div>
</div>



**[다이어그램 해설]** 과거의 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)이 프로세스 통짜 덩어리를 옮겼다면, [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)에서의 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)은 수많은 프로세스의 조각조각(세그먼트)들을 하나하나 테트리스 하듯 밀어 붙여야 한다. 이 과정에서 발생하는 램 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) [대역폭](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/140_bandwidth/) 소모와, 수많은 프로세스의 [세그먼트 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/365_segment_table/) `Base` 값을 갱신해야 하는 작업은 현대의 [초고속](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/) 컴퓨팅 환경에서는 도저히 용납할 수 없는 끔찍한 오버헤드([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/))를 낳는다.

- **📢 섹션 요약 비유**: 흩어진 책들 사이의 빈 공간을 모으기 위해, 책장에 꽂힌 책 수천 권을 전부 빼서 왼쪽으로 빈틈없이 빽빽하게 다시 꽂는([압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)) 중노동을 하는 동안 도서관은 잠시 문을 닫아야(시스템 정지) 합니다.

---

## Ⅲ. 비교 및 연결

### 50퍼센트 규칙 (50-Percent Rule)의 굴레

가변 분할의 저주인 <strong>"50% 규칙"</strong>은 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) 환경에서도 수학적으로 완벽하게 똑같이 적용된다.
- 시스템이 평형 상태(통계적 균형)에 이르면, 전체 할당된 세그먼트 메모리 양이 $N$일 때, [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)로 발생한 쓸모없는 빈 공간의 양은 평균적으로 $0.5N$이 된다.
- 즉, 전체 램의 <strong>3분의 1 (약 33%)은 영구적으로 찢어진 쓰레기 공간으로 전락</strong>한다는 뜻이다.
- 16GB 램을 꽂았는데 5GB가 찢어져서 쓸 수 없다면? 어떤 고객도 이 비효율적인 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) OS를 사지 않을 것이다.

### 비교 1: [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/)의 [내부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/) vs [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)의 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)

| [단편화](/knowledge-base/studynote/03_network/06_network_layer_ip/291_fragmentation_and_reassembly_process/) 종류 | [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/) ([내부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/341_internal_fragmentation/)) | [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) ([외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)) |
|:---|:---|:---|
| **발생 원리** | 4KB 상자에 담고 남은 빈틈 | 덩치대로 자르고 남은 방 밖의 자투리 |
| **낭비량(Loss)** | 프로세스당 평균 2KB (현미경 수준) | **전체 메모리의 33% (치명적 수준)** |
| **시스템 체감** | 낭비가 너무 작아 사실상 무시됨 | 빈 공간은 넘치는데 앱이 실행 안 됨 ([OOM](/knowledge-base/studynote/02_operating_system/02_process_thread/157_oom_killer/)) |
| **해결 비용** | 해결 안 하고 그냥 버림 (비용 0) | <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>(<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">Compaction</a>) 필수 (시스템 마비)</strong> |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">아키텍처</div><div class="kb-diagram-cell">조각의 크기</div><div class="kb-diagram-cell">보안 및 공유</div><div class="kb-diagram-cell">단편화 처리 비용</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">페이징</div><div class="kb-diagram-cell">4KB 고정</div><div class="kb-diagram-cell">까다로움</div><div class="kb-diagram-cell">없음 (최강의 효율)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">세그멘테이션</div><div class="kb-diagram-cell">의미 단위 가변</div><div class="kb-diagram-cell">직관적 완벽함</div><div class="kb-diagram-cell">☠️ 압축 지옥 ☠️</div></div>
</div>
</div>


**[매트릭스 해설]** 왜 현대 운영체제가 낭만([세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/))을 버리고 톱니바퀴([페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/))를 택했는지 완벽하게 설명하는 지표다. 33%의 램을 허공에 날리고, 그걸 살려보겠다고 시스템을 수 초씩 멈추는([압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)) 아키텍처는 서버 시장에서 살아남을 수 없었다. 결국 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)는 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)이라는 위대한 개념을 무너뜨린 1등 공신이다.

- **📢 섹션 요약 비유**: 예쁜 모양의 수제 [쿠키](/knowledge-base/studynote/03_network/09_application_layer_web_email/475_cookie_local_state/)(세그먼트)를 굽다 보면 반죽 자투리가 너무 많이 남아서 다시 뭉치는 데([압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)) 힘을 다 빼지만, 기계로 네모난 식빵([페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/))만 썰어내면 버리는 반죽 없이 1초 만에 포장이 끝나는 효율성의 차이입니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무적 한계: 힙([Heap](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/)) 메모리와 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)의 악연
- 현대 OS는 물리 메모리를 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/)으로 관리하여 이 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)를 극복했다.
- 하지만 아이러니하게도, <strong>애플리케이션(C/C++, Java)이 쓰는 가상 힙(<a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/078_heap_datastructure/">Heap</a>) 메모리 공간 내부</strong>에서는 여전히 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)과 똑같은 "가변 크기 할당(`malloc(20)`, `malloc(1000)`)"을 수행한다.
- 그 결과, [가상 메모리](/knowledge-base/studynote/02_operating_system/07_virtual_memory/381_virtual_memory/) 공간 안에서 똑같은 형태의 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/">외부 단편화</a></strong>가 무수히 발생한다. 
- 자바(Java)는 이 파편화를 끄집어모으기 위해 [가비지 컬렉터](/knowledge-base/studynote/05_database/uncategorized/591_mvcc_garbage_collection_vacuum/)(GC)가 주기적으로 <strong><a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">압축</a>(<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/">Compaction</a>)</strong>을 수행하며 애플리케이션을 강제로 멈춘다(Stop-The-World).
- 즉, OS가 물리적 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)를 [페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/)으로 박멸했지만, 소프트웨어 단에서의 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)는 2026년 현재까지도 백엔드 튜닝의 영원한 숙제로 남아있다.

### 파편화를 막는 현대적 우회 기법 ([Slab](/knowledge-base/studynote/02_operating_system/11_exam_summary/760_slab_allocator_object_caching/) / Pool)
C++ 게임 서버 개발자들은 이 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)를 막기 위해, 크기가 제각각인 객체를 그때그때 할당하지 않는다. 대신 부팅 시 똑같은 크기의 빈 방(오브젝트 풀)을 수만 개 뚫어놓고 돌려막기(Object [Pooling](/knowledge-base/studynote/10_ai/04_ai_ops_ethics/285_pooling_layer/))를 한다. 사실상 가변 분할(세그먼트)을 버리고 <strong>고정 분할(<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a>)의 철학을 힙 메모리 관리에 적용한 것이다.</strong>

- **📢 섹션 요약 비유**: 종이(메모리)를 아끼려고 매번 그림 크기에 딱 맞춰 가위질(동적 할당)을 하다 보니 책상이 쓰레기통이 되어 청소하느라(GC [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)) 하루가 다 갔습니다. 결국 아예 A4, B5 규격 종이(오브젝트 풀)만 사서 쓰고 남는 여백은 신경 쓰지 않는 쪽으로 실무의 노하우가 정립된 것입니다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 내용 |
|:---|:---|
| **설계의 반면교사** | 크기가 가변적인 조각들을 메모리에 넣고 빼는 구조는 필연적으로 붕괴한다는 시스템 공학적 교훈을 각인 |
| <strong><a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a>의 정당성 확보</strong> | 테이블을 2번 읽는 페널티([페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/))가 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)으로 시스템이 멈추는 페널티([세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/))보다 압도적으로 싸다는 것을 증명 |
| <strong>GC 컴팩션 <a href="/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/">알고리즘</a> 발전</strong>| OS 레벨에서 포기한 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) 기술이 JVM, V8 엔진 등 런타임 언어의 백그라운드 쓰레기 수집 최적화 기술로 계승 발전 |

### 결론 및 미래 전망

[세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)과 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) ([External Fragmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/))의 끈질긴 악연은, 컴퓨터 구조론에서 "[논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)적 우아함"과 "물리적 통제력"이 어떻게 충돌하는지를 보여주는 가장 극적인 드라마다. 33% 메모리 낭비와 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이라는 무거운 짐을 견디지 못한 순수 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)은 역사의 뒤안길로 퇴장했다. 하지만 인간 친화적인 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)의 '보안과 공유' 매커니즘만큼은 포기하기 아까웠기에, 공학자들은 세그먼트를 일단 나눈 뒤, 그 세그먼트를 다시 4KB의 페이지로 난도질해버리는 기상천외한 키메라 아키텍처인 <strong>'<a href="/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/">페이징</a> 기반 <a href="/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/">세그멘테이션</a>(<a href="/knowledge-base/studynote/02_operating_system/06_memory_management/367_paged_segmentation/">Paged Segmentation</a>)'</strong>을 발명하게 된다. (다음 키워드에서 계속)

- **📢 섹션 요약 비유**: 아름다운 조각상([세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/))을 만들었으나 보관할 상자(메모리)에 안 맞아서 남는 빈틈([외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/)) 때문에 버려야 할 위기에 처하자, 조각상을 레고 블록([페이징](/knowledge-base/studynote/02_operating_system/04_synchronization/259_paging/))으로 개조해 버리기로 결심한 예술과 공학의 타협점입니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) ([Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| [세그먼트 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/365_segment_table/) ([Segment Table](/knowledge-base/studynote/02_operating_system/06_memory_management/365_segment_table/)) | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [세그멘테이션 기반 페이징](/knowledge-base/studynote/02_operating_system/06_memory_management/367_paged_segmentation/) ([Paged Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/367_paged_segmentation/)) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [커널](/knowledge-base/studynote/02_operating_system/01_overview_architecture/022_kernel_role/) 메모리 할당 방식 (kmalloc, vmalloc) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">세그먼트 테이블 (Segment Table)</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">세그멘테이션과 외부 단편화 (가변 크기이므로 재발생) (Segmentation External Fragmentation)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">세그멘테이션 기반 페이징 (Paged Segmentation)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">커널 메모리 할당 방식 (kmalloc, vmalloc)</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 [압축](/knowledge-base/studynote/02_operating_system/06_memory_management/347_compaction/)해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)과 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) (가변 크기이므로 재발생) ([Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) [External Fragmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/))은 컴퓨터가 메모리를 방처럼 나눠 쓰고 주소를 찾는 방법이에요.
2. 먼저 [세그먼트 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/365_segment_table/) ([Segment Table](/knowledge-base/studynote/02_operating_system/06_memory_management/365_segment_table/))을 이해하면 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)과 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) (가변 크기이므로 재발생) ([Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) [External Fragmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/))이 왜 필요한지 더 쉽게 보여요.
3. 그래서 [세그멘테이션](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/)과 [외부 단편화](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/) (가변 크기이므로 재발생) ([Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/364_segmentation/) [External Fragmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/342_external_fragmentation/))을 잘 알면 나중에 [세그멘테이션 기반 페이징](/knowledge-base/studynote/02_operating_system/06_memory_management/367_paged_segmentation/) ([Paged Segmentation](/knowledge-base/studynote/02_operating_system/06_memory_management/367_paged_segmentation/))도 훨씬 쉽게 배울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 366 / 800

← **이전**: [365. 세그먼트 테이블 (Segment Table) - 기준(Base) 주소와 한계(Limit) 길이](/knowledge-base/studynote/02_operating_system/06_memory_management/365_segment_table/)
**다음**: [367. 세그멘테이션 기반 페이징 (Paged Segmentation) - 인텔 x86 아키텍처 (세그먼트를 다시 페이지로)](/knowledge-base/studynote/02_operating_system/06_memory_management/367_paged_segmentation/) →

---
