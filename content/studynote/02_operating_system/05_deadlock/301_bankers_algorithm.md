+++
title = "301. 다중 인스턴스 환경의 회피 - 은행원 알고리즘 (Banker's Algorithm, 에츠허르 데이크스트라 제안)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-operating-system"]

[extra]
tags = ["studynote-operating-system"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) (Banker's [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))은 에츠허르 [다익스트라](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/) (Edsger W. [Dijkstra](/knowledge-base/studynote/08_algorithm_stats/03_graph_search/036_dijkstra/))가 설계한 [교착 상태 회피](/knowledge-base/studynote/02_operating_system/05_deadlock/297_deadlock_avoidance/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)으로, [자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/) 요청 시 [안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/) 유지 여부를 검사하여 [불안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/299_unsafe_state/)로 이어지는 할당을 거부한다.
> 2. **가치**: 은행이 대출 전에 상환 가능 여부를 심사하듯, 시스템이 [자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/) 전에 모든 프로세스가 종료 가능한 순서(안전 순서)가 존재하는지 검증하여 [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)를 원천 방지한다.
> 3. **융합**: Available, Max, Allocation, Need 행렬 4개의 자료구조와 [안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) + 자원 요청 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 2개의 서브루틴으로 구성되며, 다중 인스턴스 자원 환경에서의 교착 회피 표준 해법이다.

---

## Ⅰ. 개요 및 필요성

다중 인스턴스 자원 환경에서는 [자원 할당](/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/) 그래프만으로 [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/)를 감지하기 어렵다. 프로세스가 최대 n개의 자원을 요청할 수 있고 현재 m개를 보유 중일 때, "이 요청을 들어줘도 나중에 모든 프로세스가 완료될 수 있는가?"를 미리 계산하는 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)이다.

이름의 유래: 은행은 예금 총액을 초과하는 대출을 해주지 않으면서도, 고객들이 돌아가며 빌리고 갚는 한 파산하지 않는다. 시스템도 마찬가지다.

**💡 비유**: 은행이 "지금 당신에게 이 금액을 대출해 줘도, 나머지 고객들의 대출 수요를 모두 충족하고 회수할 수 있는가?"를 확인하고 승인하는 것과 정확히 같다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">은행원 알고리즘 4개 자료구조</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">n = 프로세스 수, m = 자원 유형 수</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Available</div><div class="kb-diagram-node">m</div><div class="kb-diagram-note">: 각 자원 유형의 현재 사용 가능 인스턴스</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Max</div><div class="kb-diagram-node">n</div><div class="kb-diagram-node">m</div><div class="kb-diagram-note">: 각 프로세스의 최대 자원 요구량</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Allocation</div><div class="kb-diagram-node">n</div><div class="kb-diagram-node">m</div><div class="kb-diagram-note">: 각 프로세스에 현재 할당된 자원량</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Need</div><div class="kb-diagram-node">n</div><div class="kb-diagram-node">m</div><div class="kb-diagram-note">: 각 프로세스의 추가 필요량</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">관계: Need</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">j</div><div class="kb-diagram-note">= Max</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">j</div><div class="kb-diagram-note">- Allocation</div><div class="kb-diagram-node">i</div><div class="kb-diagram-node">j</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">예시 (5 프로세스, 3 자원 유형 A,B,C):</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Allocation Max Need Available</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">A B C A B C A B C A B C</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">P0: 0 1 0 7 5 3 7 4 3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">P1: 2 0 0 3 2 2 1 2 2 3 3 2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">P2: 3 0 2 9 0 2 6 0 0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">P3: 2 1 1 2 2 2 0 1 1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">P4: 0 0 2 4 3 3 4 3 1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">안전 순서: &lt;P1, P3, P4, P2, P0&gt; ← 존재하면 안전 상태</div></div>
</div>
</div>



**📢 섹션 요약 비유**: 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 자원 배분의 사전 심사 시스템 — "지금 이 요청을 들어줘도 미래에 모두 회수할 수 있는가"를 계산하는 안전망입니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/) [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Safety Algorithm:</div>
<div class="kb-diagram-note">① Work = Available.copy()</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">② Finish</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">= false for all i</div></div>
<div class="kb-diagram-note">③ 반복:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">i를 찾기: Finish</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">== false AND Need</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">≤ Work</div></div>
<div class="kb-diagram-note">찾으면:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Work = Work + Allocation</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">// 자원 반납 받음</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Finish</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">= true</div></div>
<div class="kb-diagram-note">못 찾으면: 종료</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">④ Finish</div><div class="kb-diagram-node">i</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">안전 상태</div></div>
<div class="kb-diagram-note">그렇지 않으면 → 불안전 상태</div>
</div>
</div>



### 자원 요청 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) (Resource-Request [Algorithm](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-note">프로세스 Pi가 Request</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">요청 시:</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">① Request</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">≤ Need</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">?</div></div>
<div class="kb-diagram-note">아니면 → 오류 (최대 요구 초과)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">② Request</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">≤ Available?</div></div>
<div class="kb-diagram-note">아니면 → Pi를 대기 상태로 (자원 부족)</div>
<div class="kb-diagram-note">③ 가정적 할당:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Available = Available - Request</div><div class="kb-diagram-node">i</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Allocation</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">= Allocation</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">+ Request</div><div class="kb-diagram-node">i</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Need</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">= Need</div><div class="kb-diagram-node">i</div><div class="kb-diagram-note">- Request</div><div class="kb-diagram-node">i</div></div>
<div class="kb-diagram-note">④ 안전 상태인가?</div>
<div class="kb-diagram-note">안전 → 실제로 자원 할당 완료</div>
<div class="kb-diagram-note">불안전 → 가상 할당 취소, Pi를 대기 상태로</div>
</div>
</div>



### 안전 순서 탐색 과정 [시각화](/knowledge-base/studynote/16_bigdata/01_intro/003_bigdata_7v/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">안전 순서 탐색 단계별 상세 예시</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">초기: Work=</div><div class="kb-diagram-node">3,3,2</div><div class="kb-diagram-note">, Finish=</div><div class="kb-diagram-node">F,F,F,F,F</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">단계1: Need</div><div class="kb-diagram-node">1</div><div class="kb-diagram-note">=</div><div class="kb-diagram-node">1,2,2</div><div class="kb-diagram-note">≤ Work=</div><div class="kb-diagram-node">3,3,2</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">P1 완료!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Work =</div><div class="kb-diagram-node">3,3,2</div><div class="kb-diagram-note">+</div><div class="kb-diagram-node">2,0,0</div><div class="kb-diagram-note">=</div><div class="kb-diagram-node">5,3,2</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Finish =</div><div class="kb-diagram-node">F,T,F,F,F</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">단계2: Need</div><div class="kb-diagram-node">3</div><div class="kb-diagram-note">=</div><div class="kb-diagram-node">0,1,1</div><div class="kb-diagram-note">≤ Work=</div><div class="kb-diagram-node">5,3,2</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">P3 완료!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Work =</div><div class="kb-diagram-node">5,3,2</div><div class="kb-diagram-note">+</div><div class="kb-diagram-node">2,1,1</div><div class="kb-diagram-note">=</div><div class="kb-diagram-node">7,4,3</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Finish =</div><div class="kb-diagram-node">F,T,F,T,F</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">단계3: Need</div><div class="kb-diagram-node">4</div><div class="kb-diagram-note">=</div><div class="kb-diagram-node">4,3,1</div><div class="kb-diagram-note">≤ Work=</div><div class="kb-diagram-node">7,4,3</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">P4 완료!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Work =</div><div class="kb-diagram-node">7,4,3</div><div class="kb-diagram-note">+</div><div class="kb-diagram-node">0,0,2</div><div class="kb-diagram-note">=</div><div class="kb-diagram-node">7,4,5</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Finish =</div><div class="kb-diagram-node">F,T,F,T,T</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">단계4: Need</div><div class="kb-diagram-node">2</div><div class="kb-diagram-note">=</div><div class="kb-diagram-node">6,0,0</div><div class="kb-diagram-note">≤ Work=</div><div class="kb-diagram-node">7,4,5</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">P2 완료!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Work =</div><div class="kb-diagram-node">7,4,5</div><div class="kb-diagram-note">+</div><div class="kb-diagram-node">3,0,2</div><div class="kb-diagram-note">=</div><div class="kb-diagram-node">10,4,7</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Finish =</div><div class="kb-diagram-node">F,T,T,T,T</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">단계5: Need</div><div class="kb-diagram-node">0</div><div class="kb-diagram-note">=</div><div class="kb-diagram-node">7,4,3</div><div class="kb-diagram-note">≤ Work=</div><div class="kb-diagram-node">10,4,7</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">P0 완료!</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Finish =</div><div class="kb-diagram-node">T,T,T,T,T</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">안전 순서: P1,P3,P4,P2,P0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">✅ 결론: 안전 상태</div></div>
</div>
</div>



**[다이어그램 해설]** 안전 순서 탐색은 욕심쟁이(Greedy) 방식으로 현재 가용 자원(Work)으로 완료 가능한 프로세스를 찾아 완료시키고 자원을 누적해가는 시뮬레이션이다. 시뮬레이션이 완전히 성공하면(Finish 모두 true) 시스템이 [안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/)다. 자원 요청 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 먼저 가상으로 할당한 뒤 이 [안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/) 시뮬레이션을 돌려본다 — 성공하면 실제 할당하고, 실패하면 취소한다.

**📢 섹션 요약 비유**: 안전 순서 탐색은 퍼즐 게임처럼 "어떤 순서로 빠져나오면 모두 탈출할 수 있는가"를 미리 풀어보는 것 — 성공하면 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/), 실패하면 그 조각은 넣지 않습니다.

---

## Ⅲ. 비교 및 연결

### 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 한계



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">은행원 알고리즘 한계 및 실무 대안</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">한계 1: 사전에 Max 정보가 필요</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 실제 OS에서 프로세스의 최대 자원 요구 예측 불가</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">한계 2: 프로세스 수와 자원 수가 고정</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 동적 생성/종료, 자원 추가 시 재계산 필요</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">한계 3: O(n²×m) 시간 복잡도</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">→ 수천 프로세스 환경에서 실시간 검사 비현실적</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">실무 대안:</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">① 교착 예방 (Lock Ordering): 순환 대기 원천 차단</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">② 타임아웃: 락 대기 시간 제한 후 롤백</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">③ 데이터베이스: 탐지 후 희생자 롤백</div></div>
</div>
</div>



**[비교 해설]** 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 이론적으로 완벽하지만 실무에서 전면 채택은 거의 없다. 대부분의 일반 목적 OS는 Ostrich [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(무시)을 채택하는 반면, 데이터베이스는 탐지+[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)를, 실시간 OS는 예방(PCP)을 채택한다. 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 자원 수와 프로세스 수가 제한적이고 사전 정보를 알 수 있는 임베디드·실시간 환경에서 실용적이다.

**📢 섹션 요약 비유**: 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 완벽한 이론 — 하지만 실제 은행은 대규모 고객에게 실시간 심사를 해주기 어렵듯이, 대규모 OS에서는 현실적 한계가 있습니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 시나리오
1. <strong>클라우드 <a href="/knowledge-base/studynote/02_operating_system/01_overview_architecture/041_resource_allocation/">자원 할당</a>자</strong>: [Kubernetes](/knowledge-base/studynote/12_it_management/05_security_compliance/205_kubernetes_container_orchestration/) Admission Controller가 [Pod](/knowledge-base/studynote/06_ict_convergence/03_cloud_infrastructure/198_pod_kubernetes_minimum_deployment_unit/) 배치 전 노드 자원 여유분(Available) 대비 요청량을 확인하는 것은 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 간소화 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/).
2. **항공 예약 시스템**: 좌석 배정 전 "이 예약을 처리해도 다른 예약 의무를 이행할 수 있는가"를 확인하는 것이 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/).

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong>Max 과소 <a href="/knowledge-base/studynote/15_devops_sre/01_culture_methodology/009_config/">설정</a></strong>: 프로세스가 실제로 필요한 것보다 Max를 적게 신고하면 [안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/298_safe_state/) 판단이 잘못되어 [교착 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/281_deadlock_definition/) 발생 가능.
- **N·M 크기 간과**: 큰 시스템에서 O(n²m)의 반복 실행 시 [스케줄러](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/079_kube_scheduler_pod_placement/) 레이턴시가 급증.

**📢 섹션 요약 비유**: 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)의 Max 신고 오류는 대출 신청서에 잘못된 소득을 기재하는 것 — 시스템이 잘못된 판단을 내려 결국 파산(교착)에 이를 수 있습니다.

---

## Ⅴ. 기대효과 및 결론

| 구분 | 교착 예방 | 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)(회피) | 교착 탐지+[복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) |
|:---|:---|:---|:---|
| 자원 이용률 | 낮음 | 중간 | 높음 |
| 교착 보장 | 100% | 100% | 탐지 주기 내 |
| 구현 복잡도 | 낮음 | 높음 | 중간 |
| 사전 정보 | 불필요 | Max 필요 | 불필요 |

**📢 섹션 요약 비유**: 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)은 자원 관리의 완벽한 보험 상품 — 가격(오버헤드)이 비싸고 가입 조건(Max 사전 정보)이 까다롭지만, 보장(교착 방지)은 완벽합니다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| [불안전 상태](/knowledge-base/studynote/02_operating_system/05_deadlock/299_unsafe_state/) ([Unsafe State](/knowledge-base/studynote/02_operating_system/05_deadlock/299_unsafe_state/)) | 현재 개념으로 들어오기 전에 함께 이해하면 경계가 선명해지는 기반 개념이다. |
| 단일 인스턴스 환경의 회피 | 현재 개념이 등장하게 만든 직접적인 선행 흐름이다. |
| [은행원 알고리즘 자료구조](/knowledge-base/studynote/02_operating_system/05_deadlock/302_bankers_data_structure/) | 현재 개념이 구현·세분화될 때 바로 연결되는 후속 개념이다. |
| [은행원 알고리즘 한계](/knowledge-base/studynote/02_operating_system/05_deadlock/303_bankers_limitations/) | 확장 학습이나 심화 비교로 이어지는 다음 단계의 키워드다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-node">단일 인스턴스 환경의 회피</div></div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">다중 인스턴스 환경의 회피</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">은행원 알고리즘 자료구조</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">▶</div><div class="kb-diagram-node">은행원 알고리즘 한계</div></div>
</div>
</div>



이 흐름도는 선행 개념에서 현재 개념으로 넘어온 뒤, 구현 세분화와 후속 확장으로 이어지는 학습 순서를 압축해 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 선생님이 학생들에게 색종이를 나눠줄 때 "지금 이 학생에게 3장 줘도, 다른 모든 학생 프로젝트를 도울 수 있는가?"를 먼저 계산해요.
2. 계산해서 "가능해요!"(안전 순서 존재) 나오면 줘요. 불가능하면 기다려 달라고 해요.
3. 이것이 은행원 [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) — 자원을 욕심껏 주는 게 아니라, 모두가 행복한 순서를 찾은 뒤에만 나눠줍니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 301 / 800

← **이전**: [300. 단일 인스턴스 환경의 회피 (Rag Avoidance)](/knowledge-base/studynote/02_operating_system/05_deadlock/300_rag_avoidance/)
**다음**: [302. 은행원 알고리즘 자료구조 (Bankers Data Structure)](/knowledge-base/studynote/02_operating_system/05_deadlock/302_bankers_data_structure/) →

---
