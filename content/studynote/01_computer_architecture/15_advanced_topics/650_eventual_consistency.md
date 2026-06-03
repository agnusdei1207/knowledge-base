+++
title = "650. 결과적 일관성 (Eventual Consistency)"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (Eventual [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))은 새로운 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)가 멈추면 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)된 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본들이 결국 동일한 값으로 수렴한다는 약한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 모델이다.
> 2. **가치**: 모든 노드의 즉시 합의를 기다리지 않으므로 [멀티 리전](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) 환경에서도 낮은 지연시간과 높은 가용성을 확보하기 쉽다.
> 3. **판단 포인트**: 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 "언젠가 맞는다"만으로 충분하지 않으며, 충돌 해결 규칙·수리 주기·내가 쓴 값 다시 보기(Read-Your-Writes) 같은 사용자 경험 보완책까지 함께 설계해야 한다.

---

## Ⅰ. 개요 및 필요성

결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 즉시 같아지지 않아도, 새로운 변경이 더 들어오지 않으면 결국 같은 상태로 수렴하도록 허용하는 모델이다. 대륙을 건너는 네트워크와 대규모 노드 집합에서는 모든 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 즉시 동기화하는 비용이 매우 크기 때문에, 많은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 저장소는 먼저 가까운 노드에 기록하고 나머지 전파는 뒤로 미룬다. 이 덕분에 사용자는 빠른 응답을 얻고, 시스템은 일부 노드 장애가 있어도 계속 동작할 수 있다.

중요한 점은 "결과적"이 "아무렇게나"를 뜻하지 않는다는 것이다. 언젠가 수렴하려면 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)가 결국 전달되어야 하고, 서로 다른 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)이 충돌했을 때 어떤 값으로 합칠지도 정해져 있어야 한다. 또한 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)만으로는 내가 방금 쓴 글이 새로고침에서 바로 보인다는 보장까지 주지 않으므로, [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) 같은 상위 정책이 자주 함께 쓰인다.

- **📢 섹션 요약 비유**: 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 동네 게시판에 소식을 붙이는 방식과 같다. 처음에는 골목마다 붙는 시간이 다르지만, 시간이 지나면 결국 모든 게시판에 같은 안내문이 붙는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

아키텍처 관점에서 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 <strong>로컬 승인 → 비동기 전파 → 불일치 탐지 → 수렴</strong>의 4단계로 이해하는 것이 가장 쉽다. [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 요청은 먼저 가까운 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본에 반영되고 즉시 응답된다. 이후 가십 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) (Gossip [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)), 힌티드 핸드오프 (Hinted Handoff), 안티 [엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/151_entropy/) (Anti-Entropy) 같은 메커니즘이 늦게 도착한 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본을 따라잡게 만든다. 핵심은 빠른 응답을 얻는 대신, 잠시 동안은 서로 다른 노드가 서로 다른 진실을 들고 있을 수 있다는 점이다.

아래 그림은 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)의 일반적인 전파 경로를 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Eventual consistency replication and convergence</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Client</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── Write ──▶ Replica A ──▶ ACK</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── async replicate ──▶ Replica B</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── async replicate ──▶ Replica C</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Readers may see A=new, B=old, C=old for a while</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">── repair / merge / anti-entropy ──▶ replicas converge</div></div>
</div>
</div>



| 단계 | 핵심 질문 | 대표 메커니즘 |
| :--- | :--- | :--- |
| 로컬 승인 | 어디까지 기록되면 성공으로 볼 것인가 | 로컬 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/), 근접 리전 우선 응답 |
| 비동기 전파 | 늦은 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본을 어떻게 따라잡게 할 것인가 | Gossip, Hinted Handoff |
| 불일치 탐지 | 누가 더 최신인지 어떻게 판단할 것인가 | [벡터 시계](/knowledge-base/studynote/05_database/04_transactions_concurrency/258_vector_clock/) ([Vector Clock](/knowledge-base/studynote/05_database/04_transactions_concurrency/258_vector_clock/)), [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 번호 |
| 수렴 | 충돌을 무엇으로 합칠 것인가 | 최종 작성 우선 (Last-Write-Wins), 충돌 없는 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 형식 (Conflict-free Replicated [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Type, CRDT), 애플리케이션 병합 |

특히 충돌 해결 규칙이 약하면 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 쉽게 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 손실로 변한다. 서버 시계가 완벽히 맞지 않은 환경에서 최종 작성 우선만 남발하면 더 늦게 도착한 오래된 값이 승리할 수 있다. 그래서 중요한 도메인에서는 애플리케이션 의미를 아는 병합 규칙이나 정족수 읽기/[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 함께 사용해 수렴 품질을 높인다.

- **📢 섹션 요약 비유**: 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 반 친구들이 필기 내용을 서로 복사해 가는 것과 같다. 빨리 퍼지게 할 수는 있지만, 누가 최신 내용을 적었는지 표시가 없으면 틀린 답이 정답처럼 퍼질 수 있다.

---

## Ⅲ. 비교 및 연결

결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 이해하려면 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (Strong [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))과 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))을 함께 봐야 한다. 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 어느 노드에서 읽어도 바로 최신 값이 보이지만, 그만큼 합의 비용과 지연시간이 크다. 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 빠르고 잘 버티지만, 순간적으로는 오래된 값을 보여 줄 수 있다. [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 그 사이에서 "적어도 내가 방금 쓴 값은 다시 보이게 하자"는 사용자 경험 보완책이다.

| 항목 | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (Strong [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) | [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) | 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) (Eventual [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) |
| :--- | :--- | :--- | :--- |
| 최신성 | 항상 최신 값 | 내 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 기준 최신성 보완 | 전체 수렴만 보장 |
| 지연시간 | 상대적으로 큼 | 중간 | 작음 |
| 장애 허용성 | 낮아질 수 있음 | 중간 | 높음 |
| 대표 활용 | 계좌, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 잠금, [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) | 사용자 프로필, 작성 직후 조회 | 피드, 리뷰, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 장바구니 |

이 모델은 BASE 특성 (Basically Available, Soft [state](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/), Eventual [consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))과 [PACELC](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리의 EL 축과도 직접 연결된다. 즉 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 단순한 [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 용어가 아니라, <strong>가용성과 응답성을 높이는 대신 정합성 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/233_recovery_database_restoration_overview/">회복</a> 로직을 뒤로 넘기는 아키텍처 선택</strong>이다. 따라서 저장소뿐 아니라 캐시, 검색 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), 이벤트 기반 마이크로서비스에서도 같은 철학이 반복된다.

- **📢 섹션 요약 비유**: 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)이 교사가 출석을 바로바로 부르는 방식이라면, 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 조장이 나중에 출석부를 모아 맞추는 방식이다. 둘 다 목적은 같지만 속도와 정확도 확보 방식이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 "틀려도 된다"가 아니라 "잠깐 달라도 된다"로 해석해야 한다. 예를 들어 좋아요 수, 상품 리뷰, [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 집계, 장바구니는 짧은 불일치를 허용하는 대신 높은 처리량과 복원력을 얻을 수 있다. 반면 계좌 잔액, 재고 차감, [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 잠금처럼 잘못된 중간 상태가 곧 사고로 이어지는 영역은 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 또는 최소한 더 강한 정족수 설계가 필요하다.

### 설계 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 오래된 값을 몇 초까지 허용할 수 있는가?
2. 충돌이 발생했을 때 기계적으로 병합 가능한가, 아니면 사람이 의미를 판단해야 하는가?
3. 사용자가 방금 쓴 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 곧바로 다시 봐야 하는가?
4. 수렴 지연이 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 수준 협약 ([Service Level Agreement](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/), [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/))에 어떤 영향을 주는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 금전·재고 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 무비판적으로 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 적용하는 설계
- 충돌 해결 없이 최종 작성 우선만 켜 두고 "언젠가 맞겠지"라고 보는 태도
- 모바일/웹 사용자에게 내가 쓴 값 다시 보기 보장을 주지 않아 체감 장애를 만드는 인터페이스

현실적인 절충은 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 기본으로 두되, [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 토큰, 스티키 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 읽기 우선 리전 고정, 정족수 읽기를 섞어 체감 불일치를 줄이는 것이다. 기술사 답안에서는 저장소 모델만 쓰지 말고, <strong>사용자에게 어떤 불일치가 언제 보이는지</strong>까지 함께 설명해야 완성도가 높다.

- **📢 섹션 요약 비유**: 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 운용은 택배 조회와 같다. 물건은 이미 움직이고 있지만 모든 화면이 동시에 같은 상태를 보여 주지는 않는다. 중요한 건 결국 도착하고, 내가 보기에 너무 헷갈리지 않게 중간 안내를 잘 주는 것이다.

---

## Ⅴ. 기대효과 및 결론

결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)의 가장 큰 장점은 높은 가용성과 낮은 지연시간이다. 노드 몇 개가 느리거나 일시적으로 끊겨도 전체 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)가 멈추지 않고, 사용자 가까운 위치에서 빠르게 응답할 수 있다. 그래서 대규모 글로벌 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)와 [멀티 리전](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/100_multi_region_deployment_pipeline_disaster_recovery/) 저장소, 대량 이벤트 처리 시스템에서 매우 강력한 무기가 된다.

하지만 복잡도는 사라지지 않고 위치만 이동한다. 즉시 합의 비용을 줄인 대신, 충돌 해결, 수렴 모니터링, [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 보장, 운영 관측성을 설계자가 떠안게 된다. 따라서 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 "싼 선택"이 아니라 <strong>어떤 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>는 늦게 맞춰도 괜찮다는 전제를 정확히 통제할 때만 가치가 생기는 선택</strong>으로 기억해야 한다.

- **📢 섹션 요약 비유**: 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 큰 운동장에서 아이들을 자유롭게 뛰게 하되, 끝나고 나면 다시 줄을 세워 인원을 맞추는 방식과 같다. 뛰는 동안은 빠르고 즐겁지만, 마무리 정리 규칙이 없으면 금방 혼란스러워진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) ([Replication](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)) | 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 여러 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본이 시간이 지나며 수렴하는 구조를 전제로 한다. |
| 가십 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) (Gossip [Protocol](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)) | 늦은 노드까지 변경 내용을 퍼뜨리는 대표적 전파 메커니즘이다. |
| 안티 [엔트로피](/knowledge-base/studynote/08_algorithm_stats/09_info_theory/151_entropy/) (Anti-Entropy) | [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 간 차이를 백그라운드에서 수리해 수렴을 보장한다. |
| [벡터 시계](/knowledge-base/studynote/05_database/04_transactions_concurrency/258_vector_clock/) ([Vector Clock](/knowledge-base/studynote/05_database/04_transactions_concurrency/258_vector_clock/)) | 동시 업데이트 충돌을 감지하고 선후 관계를 추적한다. |
| [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) | 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)의 약한 사용자 경험을 보완하는 상위 보장이다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">복제 저장소 (Replication)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">로컬 승인 · 비동기 복제</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">결과적 일관성 (Eventual Consistency)</div>
<div class="kb-diagram-note">: 일시적 불일치 허용 · 최종 수렴 보장</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ Gossip · Hinted Handoff · Anti-Entropy</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ Vector Clock · CRDT · 애플리케이션 병합</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">세션 일관성 · 정족수 조정 · 사용자 경험 보완 전략</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 결과적 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)은 친구들에게 소식을 한 명씩 전해 주는 것과 비슷해요.
2. 처음엔 어떤 친구는 알고 어떤 친구는 모르지만, 시간이 지나면 모두가 같은 소식을 듣게 돼요.
3. 대신 중요한 비밀이라면 그냥 퍼뜨리기만 하지 말고, 누가 가장 최신 이야기를 들었는지도 같이 적어 둬야 해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 651 / 803

← **이전**: [649. PACELC 정리](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/649_pacelc_theorem/)
**다음**: [651. 서버 랙 PDU (Power Distribution Unit)](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/651_server_rack_pdu/) →

---
