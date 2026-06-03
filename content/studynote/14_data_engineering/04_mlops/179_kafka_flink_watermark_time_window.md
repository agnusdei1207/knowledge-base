+++
title = "179. 카프카 (Kafka) + 플링크 (Flink) 시간 창 (Time Window) 워터마크 (Watermark)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Kafka는 재생 가능한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 이벤트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를, Flink는 상태 기반 이벤트 시간(Event Time) 처리 엔진을 제공하여 실시간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 계산 가능한 시간 모델로 바꾼다.
> 2. **가치**: Watermark는 "어느 시점까지의 이벤트가 거의 다 도착했는가"를 표현해, 네트워크 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 순서 뒤바뀜이 있어도 Time Window 집계를 일관되게 닫을 수 있게 한다.
> 3. **판단 포인트**: 허용 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/), 윈도우 종류, 키 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/), Exactly-Once 보장 수준을 어떻게 잡느냐가 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간·정확도·상태 크기의 균형을 결정한다.

---

## Ⅰ. 개요 및 필요성

Kafka + Flink 조합은 "이벤트를 잃지 않고 모으는 계층"과 "그 이벤트를 시간 기준으로 계산하는 계층"을 분리해 실시간 분석과 의사결정을 가능하게 만든다. 클릭 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), 결제 이벤트, 센서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 온라인 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)(Feature) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)처럼 수집은 끊기지 않고 들어오지만 결과는 분·초 단위로 바로 필요할 때 특히 강력하다. 이때 Kafka는 입력을 순서 있는 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)로 보존하고, Flink는 그 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 다시 읽어 상태 기반 계산과 재처리를 수행한다.

배치 처리만으로는 이런 요구를 만족하기 어렵다. 하루 뒤 집계로는 이상 거래를 막기 늦고, 몇 분 전 행동으로는 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 기반 추천이 이미 식어 버릴 수 있다. 반대로 처리 시간(Processing Time)만 믿고 즉시 집계하면 모바일 네트워크 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이나 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 재균형 때문에 늦게 도착한 이벤트가 잘못된 창에 들어가 결과가 흔들린다.

아래 구조는 Kafka가 "이벤트를 보존"하고 Flink가 "시간 의미를 계산"하는 역할을 각각 맡는다는 점을 보여준다. 실시간 파이프라인의 핵심은 빠르게 읽는 것보다, 시간이 뒤엉킨 이벤트를 비즈니스적으로 올바른 결과로 정리하는 데 있다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Kafka + Flink 실시간 파이프라인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">App / Sensor / Event Source</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Kafka Topic (Partitioned Log)</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Flink Source ─▶ keyBy ─▶ Watermark ─▶ Window / State</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─▶ Alert / Online Feature</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─▶ Lake / Warehouse Sink</div></div>
</div>
</div>



특히 Machine [Learning](/knowledge-base/studynote/03_network/05_lan_wan_l2_devices/240_switch_learning_forwarding_flooding/) (ML) 파이프라인에서는 이벤트가 언제 처리되었는지보다 "언제 발생했는지"가 더 중요하다. 사용자 클릭이 늦게 도착하더라도 실제 발생 시각 기준으로 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), 구매 전환, 실시간 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/)를 계산해야 모델 입력과 사후 분석이 일치하기 때문이다. 그래서 Kafka + Flink에서 Watermark와 Window는 단순 API가 아니라 시간 정의 자체라고 볼 수 있다.

- **📢 섹션 요약 비유**: Kafka는 우편물을 잃지 않고 쌓아 두는 우체국 창고이고, Flink는 도착 순서가 뒤죽박죽이어도 실제 발송 시간 순서로 다시 정리하는 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 기계와 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Kafka + Flink의 핵심은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)별로 흘러오는 이벤트에 타임스탬프를 부여하고, Watermark로 시간 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 정도를 추정하며, Window 안에 상태를 모았다가 적절한 시점에 결과를 내보내는 것이다. 여기서 Kafka는 순서 보장 단위를 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)으로 나누고, Flink는 각 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)을 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 태스크가 읽으면서 키별 상태와 체크포인트를 관리한다.

| 구성 요소 | 역할 | 실무 포인트 |
| :--- | :--- | :--- |
| Kafka Topic / [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 이벤트 보존, [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리 단위 제공 | [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 수가 처리 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성과 재처리 속도에 영향 |
| Timestamp Assigner | 이벤트 발생 시각 부여 | 소스 시스템 시계를 신뢰할 수 있는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) 필요 |
| [Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) [Strategy](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 시간 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 하한선 계산 | 허용 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 유휴 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 감지가 중요 |
| Window [Operator](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/565_operator_pattern_kubernetes_automation/) | 일정 시간 구간별 상태 집계 | 창 크기와 상태 크기가 함께 증가 |
| Checkpointed Sink | 장애 시 중복/손실 제어 | 정확한 결과가 필요하면 [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 싱크 고려 |

Watermark의 핵심 수식은 보통 `watermark = 지금까지 본 최대 event time - 허용 지연`이다. 그러나 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리에서는 이 Watermark가 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)마다 따로 계산된 뒤, 전체 연산자는 보통 "활성 입력 중 최소 [Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/)"를 사용한다. 즉 빠른 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 하나가 아니라 가장 늦은 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 창 종료를 결정한다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">파티션별 Watermark가 하나로 합쳐지는 방식</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">허용 지연 = 1분</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Partition A : 10:00 ─ 10:02 ─ 10:05 WM_A = 10:04</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Partition B : 10:01 ─ 10:03 ─ 10:04 WM_B = 10:03</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Global Watermark = min(WM_A, WM_B) = 10:03</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Window [10:00, 10:03) 는 Global Watermark &gt; 10:03일 때 종료</div></div>
</div>
</div>



이 구조 때문에 유휴 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)(Idleness)을 처리하지 않으면 전체 Watermark가 멈출 수 있다. 예를 들어 한 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)은 더 이상 이벤트가 없는데 "아직 늦은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 올지도 모른다"고 간주되면, 다른 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)이 아무리 앞으로 나아가도 창이 닫히지 않는다. 실무에서 Watermark가 느리다고 느껴질 때는 대개 계산식보다 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 편차와 유휴 입력 처리가 원인이다.

윈도우는 Watermark와 함께 작동하는 상태 컨테이너다. 비중첩 집계에는 Tumbling Window, 이동 평균에는 Sliding Window, 사용자 활동 구간 분석에는 [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) Window가 잘 맞는다. 중요한 것은 윈도우가 단순한 그룹 함수가 아니라 "언제까지 기다리고, 언제 결과를 닫을지"를 포함한 시간 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이라는 점이다.

| Window 종류 | 특징 | 잘 맞는 사례 |
| :--- | :--- | :--- |
| Tumbling Window | 고정 길이, 서로 겹치지 않음 | 1분 거래 건수, 분당 오류율 |
| Sliding Window | 고정 길이, 주기적으로 겹침 | 최근 5분 이동 평균, [이상 탐지](/knowledge-base/studynote/09_security/05_web_app_security/236_anomaly_based_detection_zero_day_false_positive/) |
| [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) Window | 활동 공백으로 닫힘 | 사용자 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 분석, 기기 활동 구간 |

즉 Kafka + Flink의 핵심 원리는 "[로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 읽는 것"이 아니라 "시간의 불완전성을 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)으로 통제하는 것"이다. [Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/), Window, [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/), Checkpoint가 함께 맞물려야 실시간 파이프라인이 빠르면서도 재현 가능한 결과를 낸다.

- **📢 섹션 요약 비유**: Watermark는 시험 답안 마감 시각과 같다. 조금 늦게 들어오는 학생은 받아 주되, 영원히 기다릴 수는 없으니 어느 순간 "이제 채점 시작"을 선언해야 한다.

---

## Ⅲ. 비교 및 연결

Kafka + Flink를 제대로 이해하려면 시간 기준과 엔진 역할의 경계를 함께 봐야 한다. 먼저 Processing Time은 가장 단순하지만 입력 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 결과를 바꿀 수 있고, Event Time + Watermark는 더 복잡하지만 실제 비즈니스 시점을 기준으로 재현 가능한 결과를 제공한다. 특히 모바일, 글로벌 네트워크, [사물인터넷](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/)(Internet of Things, [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/))처럼 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 편차가 큰 환경에서는 이 차이가 직접적인 품질 차이로 이어진다.

| 시간 기준 | 장점 | 약점 | 잘 맞는 경우 |
| :--- | :--- | :--- | :--- |
| Processing Time | 구현 단순, [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 최소 | 늦은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 취약, 재현성 약함 | 내부 운영 지표, 극저복잡 집계 |
| Event Time + [Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) | 정확한 시간 의미, 재처리 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 상태·설계 복잡도 증가 | 결제, 사용자 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/), ML [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |

엔진 관점에서도 역할이 다르다. Kafka는 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 저장과 전송의 중심이고, Kafka Streams는 애플리케이션 안에서 비교적 가벼운 [스트림 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/)를 수행한다. 반면 Flink는 큰 상태, 복잡한 조인, 정교한 Event Time 제어, Exactly-Once [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)가 필요한 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 처리에 더 적합하다.

| 기술 | 주 역할 | 강점 | 한계 |
| :--- | :--- | :--- | :--- |
| Kafka | 이벤트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) / 버퍼 | 재생 가능, [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 확장성 | 자체적으로 윈도우·상태 계산은 제한적 |
| Kafka Streams | 애플리케이션 내 [스트림 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) | 단순 배포, 로컬 상태 | 대규모 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 상태·복잡 조인 한계 |
| Flink | [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 상태ful [스트림 처리](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/229_stream_processing_kafka_flink/) | Event Time, 대규모 상태, 정교한 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 운영 복잡도 높음 |

이 조합은 [Machine Learning Operations](/knowledge-base/studynote/12_it_management/05_security_compliance/220_mlops_machine_learning_operations/) ([MLOps](/knowledge-base/studynote/12_it_management/05_security_compliance/348_mlops/))와도 연결된다. 같은 Kafka [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 재생하면 온라인 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 계산 로직을 과거 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 다시 적용해 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)할 수 있고, Feature Store나 레이크하우스와 연결해 오프라인 학습 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 실시간 추론 입력의 의미 차이를 줄일 수 있다. 즉 Watermark와 Window는 단순 스트리밍 기술이 아니라, 온라인·오프라인 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 지키는 장치이기도 하다.

- **📢 섹션 요약 비유**: Processing Time은 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 정류장 시계만 보고 출발하는 방식이고, Event Time + Watermark는 승객이 실제 언제 도착했는지까지 반영해 노선을 기록하는 방식과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 Window와 Watermark를 "정답 공식"으로 잡는 것이 아니라, 비즈니스 손실과 운영 비용의 균형으로 결정해야 한다. 허용 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 길게 잡으면 정확도는 올라가지만 상태가 오래 남아 메모리와 체크포인트 비용이 커진다. 반대로 너무 짧게 잡으면 결과는 빨리 나오지만 늦은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많아 보정 로직이나 재처리 비용이 증가한다.

| 시나리오 | 권장 설계 | 이유 |
| :--- | :--- | :--- |
| 실시간 대시보드 | 1분 Tumbling Window + 짧은 허용 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 빠른 가시성이 우선, 소폭 오차 허용 가능 |
| 결제/정산 집계 | Event Time + Exactly-Once Sink + 보정 경로 | 중복·누락 비용이 매우 큼 |
| 모바일 [세션](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) 분석 | [Session](/knowledge-base/studynote/02_operating_system/02_process_thread/160_session_controlling_terminal/) Window + 비교적 긴 허용 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | 네트워크 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)과 앱 백그라운드 복귀 고려 |
| [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 센서 모니터링 | Event Time + 유휴 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 감지 + 큰 상태 관리 | 연결 불안정과 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 편차가 흔함 |

늦은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)도 미리 정해야 한다. 허용 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 안에 들어오면 기존 결과를 업데이트하고, 조금 더 늦은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 사이드 출력으로 보내 보정 배치에 합류시키며, 매우 늦은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [감사](/knowledge-base/studynote/02_operating_system/10_security/606_auditing_linux_auditd/) [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)만 남기고 버리는 방식이 흔하다. 이 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)을 명시하지 않으면 운영 중 "왜 숫자가 뒤늦게 바뀌었는가"라는 갈등이 반복된다.



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">늦은 데이터 처리 경로</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">Late Event</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 허용 지연 이내 ─▶ Window 재계산 / 결과 갱신</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 약간 초과 ─▶ Side Output → 보정 파이프라인</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">─ 크게 초과 ─▶ Drop / Audit Log</div></div>
</div>
</div>



체크리스트는 다음과 같다.

1. 이벤트 타임스탬프가 신뢰 가능한 소스에서 오는가?
2. [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 키가 특정 고객·디바이스에 치우쳐 상태 편중을 만들지 않는가?
3. [Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)의 원인이 허용 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)인지, 유휴 [파티션](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/)인지, 백프레셔인지 구분되고 있는가?
4. 결과 업데이트를 허용할지, 한 번 출력 후 보정 배치로 돌릴지 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)이 정해져 있는가?
5. 체크포인트 간격과 Kafka [트랜잭션](/knowledge-base/studynote/05_database/04_transactions_concurrency/191_transaction_concept_states/) 시간 제한이 서로 맞는가?

흔한 안티패턴은 Processing Time으로 시작한 뒤, 늦은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 쌓이자 나중에 수작업 보정을 붙이는 것이다. 또 허용 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)을 과도하게 길게 잡아 상태가 폭증하거나, 한 개의 Hot [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) 때문에 특정 태스크만 느려지는 경우도 많다. 기술사 답안에서는 [Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) 정의, Window 종류, Exactly-Once 보장, Late [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리까지 한 묶음으로 설명해야 실제 설계 역량이 드러난다.

- **📢 섹션 요약 비유**: 실무의 [Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) 설계는 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/)를 몇 분까지 기다릴지 정하는 운행 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)과 같다. 너무 오래 기다리면 전체 노선이 밀리고, 너무 빨리 떠나면 승객을 잃는다.

---

## Ⅴ. 기대효과 및 결론

Kafka + Flink 기반 Event Time 처리는 순서가 뒤엉킨 현실 세계의 이벤트를 재현 가능한 숫자로 바꿔 준다. 같은 Kafka [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/)를 다시 읽어도 비슷한 Window 결과를 재구성할 수 있고, 실시간 경보와 [피처](/knowledge-base/studynote/10_ai/03_llm_nlp/247_feature_label_variables/) 계산을 배치 재처리와 같은 의미 체계 위에 둘 수 있다. 이는 실시간 분석뿐 아니라 모델 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/), 사후 정산, 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)에도 큰 장점이다.

하지만 이 접근이 공짜는 아니다. 상태 저장소 크기, 체크포인트 비용, [Key](/knowledge-base/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/) Skew, 잘못된 타임스탬프, 복잡한 Sink [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 문제가 함께 따라온다. 특히 Watermark는 "정확한 진실"이 아니라 "이 정도 늦음까지는 기다리겠다"는 운영 합의이므로, 비즈니스 부서와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어가 같은 기준을 공유해야 한다.

결론적으로 기억할 핵심은 단순하다. Kafka가 이벤트를 잃지 않게 해 주고, Flink가 시간을 계산 가능하게 만든다. 그리고 Window와 Watermark는 그 사이에서 "언제 결과를 확정할 것인가"를 정하는 계약이다. 이 계약을 잘 설계할수록 실시간 파이프라인은 빠르면서도 신뢰할 수 있게 된다.

- **📢 섹션 요약 비유**: Kafka + Flink는 택배를 모아 두는 창고와 배송 시간을 계산하는 관제실이 함께 움직이는 구조와 같다. 창고만 있어도, 관제실만 있어도 부족하고 둘이 맞물려야 정확한 배송 일정이 나온다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Kafka Topic / [Partition](/knowledge-base/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 이벤트 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 보존과 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/)성의 기본 단위 |
| Event Time | 실제 비즈니스 발생 시각을 기준으로 계산하는 시간 모델 |
| [Watermark](/knowledge-base/studynote/16_bigdata/04_streaming/085_watermark/) | 시간 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 하한선을 표현해 Window 종료 시점을 정하는 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| Time Window | 일정 구간의 이벤트를 상태로 모아 집계·조인하는 연산 단위 |
| Checkpoint | 장애 후 상태와 오프셋을 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/)해 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)을 유지하는 장치 |
| [State](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/272_state_pattern/) Backend | 키별 상태를 메모리 또는 디스크에 저장하는 계층 |
| Exactly-Once | 재처리 시 중복·누락 없이 결과를 내기 위한 보장 수준 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">이벤트 발생</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Kafka Append Log</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Timestamp Assign / Watermark 계산</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Keyed Window State</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ 실시간 결과 출력</div>
<div class="kb-diagram-tree-item" style="--depth:2">▶ Replay / Backfill 검증</div>
</div>
</div>



이 흐름은 [로그](/knowledge-base/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/) 저장, 시간 [진행](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/216_progress_in_synchronization/) 추정, 상태 기반 집계, 재처리 가능성이 하나의 파이프라인으로 연결되는 구조를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. Kafka는 편지를 잃어버리지 않게 순서대로 쌓아 두는 큰 우체통이에요.
2. Flink는 조금 늦게 온 편지도 원래 보낸 시간대로 다시 정리해 주는 똑똑한 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)기예요.
3. Watermark는 "이제 이 시간까지 온 편지는 거의 다 모였어"라고 알려 주는 마감선이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 179 / 258

← **이전**: [178. 파케이 (Parquet) 컬럼형 압축 포맷과 RLE (Run-Length Encoding) 최적화](/knowledge-base/studynote/14_data_engineering/04_mlops/178_parquet_rle_encoding_columnar_compression/)
**다음**: [180. CDC (Change Data Capture)와 Debezium 기반 Binlog 실시간 동기화](/knowledge-base/studynote/14_data_engineering/04_mlops/180_cdc_debezium_binlog_realtime_sync/) →

---
