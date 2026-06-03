+++
title = "648. 캡 정리 (CAP Theorem)와 분산 스토리지"
date = 2026-05-08

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 캡 정리 ([CAP Theorem](/knowledge-base/studynote/14_data_engineering/05_exam_keywords/219_cap_pacelc_distributed_tradeoff/))는 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지에서 네트워크 분단이 발생했을 때, <strong><a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a> (<a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">Consistency</a>)</strong> 과 <strong><a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">가용성</a> (<a href="/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/">Availability</a>)</strong> 을 동시에 완벽히 보장할 수 없다는 장애 시점의 선택 원리를 설명한다.
> 2. **가치**: 이 정리는 `어떤 데이터는 잠시 틀려도 되는가, 아니면 잠시 멈추더라도 맞아야 하는가`를 분명히 하여, 저장 시스템 설계를 기술 문제가 아니라 비즈니스 의미 문제로 바꿔 준다.
> 3. **판단 포인트**: CAP은 흔한 오해처럼 "셋 중 둘을 고르는 표어"가 아니라, <strong>분단 허용은 현실에서 사실상 필수</strong>이며 분단 시 C와 A 중 무엇을 우선할지 결정하라는 정리다.

---

## Ⅰ. 개요 및 필요성

[분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지는 같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 여러 노드에 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)해 빠른 응답과 장애 대응을 얻으려 한다. 하지만 노드가 지역을 넘나들고 네트워크 장비가 여러 계층으로 연결될수록, 링크 단절·[스위치](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/238_switch_operation_principles/) 장애·패킷 손실로 인해 일부 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본끼리 통신이 끊기는 순간은 피할 수 없다. [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 바로 이 현실적 상황에서 저장 시스템이 어떤 행동을 해야 하는지를 설명하는 기본 원리다.

핵심 질문은 단순하다. 한쪽 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본에 기록된 최신 값이 다른 쪽으로 아직 전달되지 않았는데, 클라이언트가 읽기나 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 요청하면 어떻게 할 것인가? `정확하지 않다면 응답을 미루는 선택`은 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 지키지만 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 희생하고, `일단 응답하는 선택`은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)을 지키지만 값이 어긋날 수 있다. 따라서 CAP은 기술적 제약을 드러내는 동시에 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 우선순위를 묻는 프레임이 된다.

- **📢 섹션 요약 비유**: 본점과 지점의 전화선이 끊긴 은행과 같다. 지금 잔액을 꼭 맞춰야 하면 창구를 잠시 닫아야 하고, 손님을 계속 받으려면 잠깐 틀린 잔액을 보여줄 위험을 감수해야 한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

CAP을 저장 시스템 관점에서 보면 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 집합, 읽기·[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 경로, 분단 감지, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 동기화라는 네 요소로 정리된다. 분단 허용 ([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance) 은 현대 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템에서는 사실상 제거할 수 없는 전제이므로, 실제 설계는 분단이 생겼을 때 `강한 일관성을 유지할지` 혹은 `응답성을 유지할지`를 고르는 문제로 수렴한다.

아래 그림은 세 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 중 한쪽이 네트워크로 분리되었을 때 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지가 맞닥뜨리는 선택을 보여 준다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Replica set under a network partition</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Replica A</div><div class="kb-diagram-note">---</div><div class="kb-diagram-node">Replica B</div><div class="kb-diagram-note">X</div><div class="kb-diagram-node">Replica C</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">link broken</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">CP choice: block or reject minority-side requests</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">AP choice: answer on both sides and reconcile later</div></div>
</div>
</div>



| 요소 | 의미 | 저장 시스템에서의 해석 |
| :--- | :--- | :--- |
| [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Consistency](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)) | 모든 읽기가 하나의 최신 복사본처럼 보임 | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 선형화 가능성 보장 |
| [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/) ([Availability](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)) | 살아 있는 노드는 항상 응답 | 최신성보다 응답 지속을 우선 |
| 분단 허용 ([Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) Tolerance) | 네트워크 단절 중에도 시스템이 계속 존재 | [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 사이 통신 실패를 설계 전제로 수용 |

정족수 기반 읽기·[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 역시 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 안에서 움직인다. 예를 들어 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) 수 `N`에 대해 읽기 수 `R`과 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 수 `W`가 `R + W > N`을 만족하도록 잡으면 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)에 가까운 동작을 얻을 수 있지만, 분단 중에는 그 정족수를 모으지 못해 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/)이 떨어진다. 반대로 로컬 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본만 보고 바로 응답하면 분단 상황에서도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/)는 계속되지만 이후 충돌 조정과 병합이 필요해진다.

- **📢 섹션 요약 비유**: 회의 참석자 전원이 같은 최신 회의록을 볼 때까지 회의를 멈출지, 아니면 각자 가진 복사본으로 일단 진행하고 나중에 맞출지 결정하는 문제와 같다. 둘 다 장단점이 분명하다.

---

## Ⅲ. 비교 및 연결

CAP은 보통 CP와 AP의 비교로 가장 잘 드러난다. [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 계열은 분단 시 일부 요청을 거절하거나 대기시켜 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 단일 진실을 지키고, [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 계열은 응답을 우선한 뒤 나중에 상태를 수렴시킨다. 이 차이는 단순 철학 차이가 아니라 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 방식, 사용자 경험, 운영비까지 바꾼다.

| 항목 | [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 지향 스토리지 | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 지향 스토리지 |
| :--- | :--- | :--- |
| 분단 시 행동 | 일부 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)/읽기 차단 | 살아 있는 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본은 계속 응답 |
| [데이터 모델](/knowledge-base/studynote/05_database/01_db_architecture_relational/014_data_model_components/) | 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 리더 기반 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) | 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 충돌 병합 |
| 장점 | 금전·[메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 같은 [정확성](/knowledge-base/studynote/16_bigdata/01_intro/002_bigdata_5v/) 보장 | 높은 [가용성](/knowledge-base/studynote/01_computer_architecture/13_reliability_power_management/452_availability/), 광역 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 친화 |
| 약점 | 장애 시 체감 중단 가능 | 일시적 불일치와 병합 로직 필요 |
| 연결 개념 | 합의 [프로토콜](/knowledge-base/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/), 정족수 | 가십, 읽기 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/), 충돌 해소 |

이 비교는 이후의 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/), 정족수 조정, [PACELC](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/342_pacelc/) 정리로 이어진다. 특히 CAP이 `분단 시의 선택`을 말한다면, 평상시 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)의 균형은 패컬크 정리 ([PACELC Theorem](/knowledge-base/studynote/14_data_engineering/01_infrastructure/041_pacelc_theorem_cap_extension/)) 가 더 잘 설명한다. 따라서 CAP은 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 스토리지를 보는 첫 렌즈이고, 그 위에 세부 튜닝 이론이 덧붙는 구조로 이해하는 것이 좋다.

- **📢 섹션 요약 비유**: CP는 정답을 확인하기 전에는 시험지를 제출하지 않는 학생이고, AP는 일단 답을 적어 내고 나중에 정오표를 붙이는 학생과 같다. 어떤 방식이 맞는지는 시험 종류에 따라 달라진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 한 덩어리로 보지 말고 의미별로 나눠야 한다. 계좌 잔액, 권한 정보, 리더 선출 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)는 [CP](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/086_CP_순환_전치_GI/) 성향이 맞고, 추천 피드, 장바구니, 읽기 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 캐시 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 성향이 더 실용적일 수 있다. 즉 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 판단은 저장 엔진 하나를 고르는 문제가 아니라, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 종류마다 허용 가능한 오차와 중단 시간을 정의하는 일이다.

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 잠시 틀리면 금전·보안·규제 문제가 발생하는가?
2. 분단 시 사용자가 `오류 메시지`를 더 싫어하는가, `잠시 오래된 값`을 더 싫어하는가?
3. 읽기 이후 곧바로 자신의 [쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 확인해야 하는가?
4. 충돌이 생겼을 때 자동 병합 가능한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조인가, 아니면 사람 판단이 필요한가?
5. [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본이 여러 지역에 퍼져 있다면, 장애 영역과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간을 별도로 측정하고 있는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 전 세계 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 배치 시스템을 두고도 `우리는 CA`라고 가정하는 경우
- 댓글 수나 캐시 같은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)까지 모두 CP로 묶어, 작은 네트워크 흔들림에도 [서비스](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 전체가 굳어 버리는 경우
- [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 시스템을 도입하고도 충돌 해결 규칙과 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 보완책을 준비하지 않는 경우

기술사 관점에서는 CAP을 선택 이론이 아니라 `장애 설계 문서`로 다뤄야 한다. 분단이 일어났을 때 어떤 요청을 막고, 어떤 요청은 살리며, [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) 후 어떤 방식으로 다시 맞출지까지 써야 한다. 그래야 CAP이 시험용 슬로건이 아니라 실제 장애 대응 아키텍처가 된다.

- **📢 섹션 요약 비유**: 비 오는 날 우산을 펼칠지 뛰어갈지 미리 정해 두는 것과 같다. 비가 오고 나서야 고민하면 이미 다 젖는다.

---

## Ⅴ. 기대효과 및 결론

[CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 관점을 명확히 적용하면 시스템이 장애 시 어떤 모습을 보일지 예측 가능해진다. 사용자는 어떤 상황에서 잠시 대기해야 하는지, 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 약간 늦게 맞춰질 수 있는지 일관된 경험을 하게 되고, 운영자는 불필요한 과설계나 잘못된 기대를 줄일 수 있다. 즉 CAP은 기능보다 `실패 시 행동의 품질`을 높여 주는 이론이다.

물론 CAP만으로 설계가 끝나지는 않는다. 평상시 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간, 정족수 비용, 충돌 병합 난이도, 하드웨어 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 특성은 추가로 따져야 한다. 그래도 이 주제를 기억할 때 가장 중요한 문장은 하나다. <strong><a href="/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/">분산</a> 스토리지는 분단을 피할 수 없고, 따라서 장애 순간에 무엇을 지킬지 미리 결정해야 한다.</strong> 이것이 [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리가 남기는 가장 실무적인 메시지다.

- **📢 섹션 요약 비유**: CAP은 세 가지 보물을 다 주는 마법 주문이 아니라, 폭풍이 왔을 때 무엇을 먼저 건질지 정하게 해 주는 선장의 우선순위 표와 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 선형화 가능성 (Linearizability) | CAP에서 말하는 강한 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 가장 엄격하게 해석한 대표 모델이다. |
| 정족수 (Quorum) | [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/)본 중 몇 개의 확인을 받아 읽기·[쓰기](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)를 성립시킬지 결정해 C와 A 균형을 조절한다. |
| 최종 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) ([Eventual Consistency](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/650_eventual_consistency/)) | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 성향 스토리지가 분단 이후에도 결국 상태를 수렴시키는 대표 모델이다. |
| 패컬크 정리 ([PACELC Theorem](/knowledge-base/studynote/14_data_engineering/01_infrastructure/041_pacelc_theorem_cap_extension/)) | CAP이 다루지 않는 평상시 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간과 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)의 균형까지 확장해 설명한다. |
| 충돌 없는 [복제](/knowledge-base/studynote/14_data_engineering/01_infrastructure/016_replication_factor/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입 (Conflict-free Replicated [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Type, CRDT) | [AP](/knowledge-base/studynote/03_network/11_wireless_mobile_communication/572_ap_access_point_ds_distribution_system/) 시스템에서 충돌 병합 비용을 줄이기 위한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조적 해법이다. |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Single-node storage assumptions</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Replication across unreliable networks</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CAP trade-off under partition</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Quorum / eventual consistency design patterns</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">PACELC and workload-specific consistency tuning</div>
</div>
</div>



이 흐름은 저장 시스템 논의가 `복제하면 더 안전하다`는 수준에서, `복제 중 어떤 실패 행동을 선택할 것인가`를 설계하는 수준으로 깊어졌음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 친구 셋이 같은 공책을 같이 쓰는데, 두 친구 사이 전화가 끊기면 바로 문제가 생겨요.
2. 그때는 잠깐 기다리면서 공책 내용을 꼭 맞출지, 아니면 일단 쓰고 나중에 맞출지 골라야 해요.
3. [CAP](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/341_process/) 정리는 컴퓨터가 이런 어려운 순간에 어떤 선택을 해야 하는지 알려주는 규칙이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 649 / 803

← **이전**: [647. 비잔틴 장애 허용 (BFT) 분산 시스템 검증](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/647_bft_verification/)
**다음**: [649. PACELC 정리](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/649_pacelc_theorem/) →

---
