+++
weight = 176
title = "176. 분산 DB 쿼리 플랜 지연 역추적 (Slow Query Tracing)"
date = "2026-04-21"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[136_variance|분산]] [[002_database_definition|데이터베이스]]([[501_database|Database]], DB)에서 슬로우 [[298_qkv_attention|쿼리]] 역추적은 단일 SQL의 평균 시간만 보는 일이 아니라, 요청 트레이스·샤드별 실행 스팬·[[298_qkv_attention|쿼리]] 플랜을 연결해 [[015_지연_데이터_관점|지연]]이 어디서 누적되는지 인과 [[083_relationship_in_er_model|관계]]를 복원하는 작업이다.
> 2. **가치**: [[342_routing_metric_hop_bandwidth_delay|메트릭]]만으로는 "느리다"까지만 보이지만, 트레이스와 플랜을 결합하면 "어느 샤드에서 어떤 연산자가 왜 오래 걸렸는가"까지 내려갈 수 있어 장애 대응 속도가 크게 빨라진다.
> 3. **판단 포인트**: 진단 순서는 `쿼리 fingerprint 확인 → 샤드별 시간 편차 확인 → 실제 실행 계획과 추정치 비교 → 잠금·네트워크·통계 상태 점검`이 가장 재현 가능하다.

---

## Ⅰ. 개요 및 필요성

[[136_variance|분산]] DB에서 슬로우 [[298_qkv_attention|쿼리]](Slow Query) 역추적은 하나의 사용자 요청이 [[014_api_posix|Application Programming Interface]] ([[014_api_posix|API]]), Structured Query Language (SQL) 라우터, 여러 샤드, 병합 노드를 거치는 동안 어디서 병목이 생겼는지 추적하는 관측 기법이다. 단일 DB에서는 `EXPLAIN ANALYZE` 한 번으로 상당 부분 원인을 볼 수 있지만, [[136_variance|분산]] 환경에서는 같은 SQL이라도 샤드별 [[001_dikw_pyramid|데이터]] 분포와 네트워크 홉 때문에 [[015_지연_데이터_관점|지연]] 구조가 달라진다.

문제가 어려운 이유는 증상이 한 군데에만 나타나지 않기 때문이다. 애플리케이션에서는 단순히 응답시간 증가로 보이고, DB 레벨에서는 특정 샤드의 Full Scan이나 [[510_lock|Lock]] Wait으로 드러나며, 인프라 레벨에서는 네트워크 재전송이나 연결 풀 포화로 표현될 수 있다. 이 셋을 따로 보면 원인이 흩어지고, 함께 보면 비로소 선후관계가 생긴다.

[[100_sre_site_reliability_engineering_error_budget|Site Reliability Engineering]] ([[100_sre_site_reliability_engineering_error_budget|SRE]]) 관점에서 슬로우 [[298_qkv_attention|쿼리]]는 [[123_slo_service_level_objective|Service Level Objective]] ([[181_slo_service_level_objective|SLO]]) 훼손의 전형적 원인이다. P99 [[015_지연_데이터_관점|지연]]시간 하나가 연결 풀 고갈, [[014_api_posix|API]] [[573_timeout_retry_backoff_strategy|타임아웃]], 재시도 폭증으로 연쇄 전파되기 때문이다. 그래서 [[136_variance|분산]] DB에서는 "DB만 본다"가 아니라 요청 단위의 [[401_transport_layer_role_end_to_end_multiplexing|end-to-end]] 관찰이 필수다.

```text
┌──────────────────────────────────────────────────────────────┐
│        분산 쿼리가 느려질 수 있는 지점은 한 군데가 아니다      │
├──────────────────────────────────────────────────────────────┤
│ Client ─▶ API ─▶ SQL Router ─▶ Shard A                      │
│                            ├▶ Shard B                       │
│                            └▶ Shard C ─▶ Merge / Sort       │
│                                                              │
│ 어느 한 지점의 지연이 최종 응답시간으로 합쳐져 나타남         │
└──────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: [[136_variance|분산]] 슬로우 [[298_qkv_attention|쿼리]] 추적은 택배가 늦었을 때 "도착이 늦다"만 보는 것이 아니라, 물류센터·간선차량·지역배송 중 어디서 막혔는지 배송 이력을 따라가는 일과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

핵심은 요청 경로마다 공통 [[289_identification_flags_fragmentation_offset|식별자]]를 심는 것이다. 애플리케이션이 [[146_opentelemetry_otel_observability_standard|OpenTelemetry]] 트레이스를 만들고, DB 드라이버가 SQL fingerprint와 바인드 정보를 태그로 남기며, [[136_variance|분산]] DB [[264_proxy_pattern_surrogate_access_control|프록시]]나 코디네이터가 샤드별 하위 스팬을 기록하면 하나의 [[303_trace_id|Trace ID]] 아래에 전체 경로가 모인다. 여기에 슬로우 [[298_qkv_attention|쿼리]] [[568_logs_distributed_logging_elk_fluentd|로그]]와 `EXPLAIN ANALYZE` 결과를 묶으면 "느린 요청"이 "느린 플랜"과 연결된다.

| 관측 [[130_signal|신호]] | 주로 답하는 질문 | 대표 [[001_dikw_pyramid|데이터]] |
| :--- | :--- | :--- |
| [[342_routing_metric_hop_bandwidth_delay|메트릭]] | 얼마나 자주 느린가? | P95/P99, 큐 길이, 연결 수 |
| [[568_logs_distributed_logging_elk_fluentd|로그]] | 어떤 SQL이 반복되는가? | normalized SQL, rows examined, [[510_lock|lock]] wait |
| 트레이스 | 요청 경로 어디서 느린가? | [[303_trace_id|Trace ID]], span duration, shard label |
| [[166_execution_plan_optimizer_navigation_tree|실행 계획]] | 왜 느린 연산이 생겼는가? | scan type, estimated rows, actual rows |

아래 그림은 Trace ID와 [[298_qkv_attention|쿼리]] 플랜이 어떻게 연결되는지 보여준다.

```text
Request Trace ID: 9f2c...
┌──────────────────────────────────────────────────────────────┐
│ API Span (35 ms)                                             │
│  └─ SQL Router Span (910 ms)                                 │
│      ├─ Shard-01 Span (42 ms)  : Index Range Scan            │
│      ├─ Shard-02 Span (51 ms)  : Index Range Scan            │
│      ├─ Shard-03 Span (781 ms) : Table Scan   ◀ bottleneck   │
│      └─ Merge Sort Span (36 ms)                              │
└──────────────────────────────────────────────────────────────┘

Plan Hash: a13b...
Query Fingerprint: SELECT * FROM orders WHERE user_id = ?
Slow Log Row: rows_examined=1,240,000 / rows_sent=20
```

여기서 중요한 것은 단순 SQL 전문보다 **query fingerprint**다. 바인드 값이 다른 동일 형태 SQL을 하나로 묶어야 반복 패턴을 찾을 수 있고, 샤드별 span과 플랜 hash를 조합해야 특정 [[298_qkv_attention|쿼리]] 회귀(regression)를 감지할 수 있다. 또한 estimated rows와 actual rows 차이가 크면 통계 노후화(stale [[168_clustering_factor_index_physical_alignment|statistics]]), plan hash는 같은데 특정 샤드만 느리면 [[001_dikw_pyramid|데이터]] 스큐나 핫 [[514_partition_slice_volume|파티션]]을 의심할 수 있다.

운영 부담을 줄이려면 모든 요청에 상세 계획을 붙이기보다, 일정 임계값 이상 느린 trace만 샘플링해 플랜 캡처를 수행하는 것이 일반적이다. 즉 핵심 원리는 **전수 계측이 아니라 상관 가능한 선택적 계측**이다.

- **📢 섹션 요약 비유**: 트레이스는 CCTV이고 [[298_qkv_attention|쿼리]] 플랜은 주방 조리표다. 둘을 함께 봐야 "어느 요리사가 어느 공정에서 병목을 만들었는지" 정확히 말할 수 있다.

---

## Ⅲ. 비교 및 연결

슬로우 [[298_qkv_attention|쿼리]] 분석 도구는 서로 대체 [[083_relationship_in_er_model|관계]]가 아니라 보완 [[083_relationship_in_er_model|관계]]다. [[136_prometheus|Prometheus]] [[342_routing_metric_hop_bandwidth_delay|메트릭]]은 현상을 빠르게 감지하지만 SQL 원문을 모른다. [[568_logs_distributed_logging_elk_fluentd|로그]]는 SQL 패턴을 알려 주지만 요청 전체 맥락을 잃기 쉽다. 트레이스는 경로를 보여 주지만 계획이 없으면 왜 느린지 단정하기 어렵다. 따라서 [[136_variance|분산]] DB에서는 세 [[130_signal|신호]]를 조합한 관측 설계가 정답에 가깝다.

| 접근 | 장점 | 한계 | [[136_variance|분산]] 환경에서의 역할 |
| :--- | :--- | :--- | :--- |
| [[342_routing_metric_hop_bandwidth_delay|메트릭]] 중심 | 가벼움, 알람에 적합 | 원인 설명이 약함 | [[181_slo_service_level_objective|SLO]] 위반 조기 탐지 |
| [[568_logs_distributed_logging_elk_fluentd|로그]] 중심 | SQL 반복 패턴 파악 용이 | 요청 맥락 손실 | fingerprint별 상위 문제 [[655_ir_detection_analysis|식별]] |
| 트레이스 중심 | 호출 경로와 [[015_지연_데이터_관점|지연]] 위치 파악 | 저장 비용 큼 | 샤드·[[090_service_kubernetes_network_load_balancing|서비스]] 경계 병목 [[396_validation|확인]] |
| [[166_execution_plan_optimizer_navigation_tree|실행 계획]] 중심 | 연산자 수준 RCA 가능 | 실시간 전수 수집 어려움 | [[154_database_index_b_tree_search_optimization|인덱스]]·통계·조인 [[268_strategy_pattern|전략]] 판단 |

[[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]] 관리시스템(Relational [[501_database|Database]] [[372_management|Management]] System, RDBMS) 단일 노드 환경과 비교하면 경계가 더 분명해진다. 단일 DB는 "이 [[154_database_index_b_tree_search_optimization|인덱스]]가 없어서 느리다"로 끝나는 경우가 많지만, [[136_variance|분산]] DB는 같은 [[154_database_index_b_tree_search_optimization|인덱스]]가 있어도 크로스샤드 조인, [[184_partition_pruning|파티션 프루닝]] 실패, 리더 노드 편중, [[016_replication_factor|복제]] [[015_지연_데이터_관점|지연]] 같은 별도 변수가 추가된다. 그래서 `EXPLAIN`만 잘 읽는 [[002_database_definition|데이터베이스]] 관리자 역량에 더해, 네트워크·[[264_proxy_pattern_surrogate_access_control|프록시]]·애플리케이션 계층을 함께 보는 [[642_observability_telemetry|observability]] 관점이 필요하다.

[[146_opentelemetry_otel_observability_standard|OpenTelemetry]], [[136_prometheus|Prometheus]], Jaeger나 [[168_grafana|Grafana]] Tempo, `pg_stat_statements` 또는 엔진별 slow query [[568_logs_distributed_logging_elk_fluentd|로그]]는 이 연결을 위한 기본 부품들이다. 결국 이 주제는 DB 튜닝 단독 과목이 아니라, **[[136_variance|분산]] 시스템 [[111_observability_metrics_logs_traces|관측 가능성]]의 한 사례**로 이해해야 한다.

- **📢 섹션 요약 비유**: [[342_routing_metric_hop_bandwidth_delay|메트릭]]은 체온계, [[568_logs_distributed_logging_elk_fluentd|로그]]는 진료 기록, 트레이스는 정밀 촬영, [[298_qkv_attention|쿼리]] 플랜은 수술 장면에 가깝다. 어느 하나만으로는 병을 알 수 있지만, 정확한 수술 계획은 모두를 함께 볼 때 나온다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 가장 효과적인 접근은 단계적 triage다. 먼저 P99 알람으로 문제 시점을 잡고, 그 구간의 query fingerprint 상위 항목을 [[396_validation|확인]]한 뒤, 같은 fingerprint의 샤드별 span [[136_variance|분산]]을 본다. 이후 느린 샤드의 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]을 비교해 scan type, [[521_join|join]] method, actual rows, [[510_lock|lock]] wait을 [[396_validation|확인]]하면 상당수 원인을 빠르게 좁힐 수 있다.

| 관찰된 증상 | 우선 의심할 원인 | 권장 조치 |
| :--- | :--- | :--- |
| 특정 샤드만 유독 느림 | [[001_dikw_pyramid|데이터]] 스큐, 핫 [[514_partition_slice_volume|파티션]] | 리샤딩, [[514_partition_slice_volume|파티션]] 키 재검토, 핫키 캐시 |
| 모든 샤드가 고르게 느림 | 잘못된 [[154_database_index_b_tree_search_optimization|인덱스]], 광범위 조건절 | [[154_database_index_b_tree_search_optimization|인덱스]] 추가, SQL 재작성, predicate 정리 |
| estimated rows ≪ actual rows | 통계 노후화 | ANALYZE, 통계 수집 주기 조정 |
| DB span 전 대기시간이 김 | 연결 풀 고갈, 큐 적체 | pool size·[[319_timeout_prevention|timeout]] 조정, 애플리케이션 backpressure |
| 특정 시점에만 급격히 악화 | 배포 후 플랜 회귀, [[005_schema|스키마]] 변경 | plan hash 비교, 배포 [[098_rollback_strategy_pipeline_error_threshold|롤백]], [[167_sql_hint_optimizer_override|힌트]] 검토 |

### [[435_checklist_based_testing|체크리스트]]

1. SQL 전문은 [[172_maas_mobility_as_a_service|마스]]킹하되 fingerprint와 주요 태그는 남기고 있는가?
2. Trace ID와 slow log를 join할 수 있는 공통 키가 있는가?
3. 느린 [[298_qkv_attention|쿼리]]만 plan capture 하도록 샘플링 기준을 두었는가?
4. P99 알람과 [[298_qkv_attention|쿼리]]별 [[181_slo_service_level_objective|SLO]] 예산이 연결되어 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 평균 응답시간만 보고 P99 악화를 놓치는 경우
- 모든 [[298_qkv_attention|쿼리]]에 `EXPLAIN ANALYZE`를 붙여 운영 부하를 키우는 경우
- SQL 원문을 그대로 수집해 [[781_personal_information|개인정보]]·[[782_sensitive_information|민감정보]]를 노출하는 경우
- [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[568_logs_distributed_logging_elk_fluentd|로그]], 트레이스를 서로 다른 보존기간으로 두어 [[325_correlation_analysis_pearson_spearman|상관 분석]]이 불가능한 경우

기술사 답안에서는 "[[154_database_index_b_tree_search_optimization|인덱스]] 튜닝"만 적기보다, **관측 → [[325_correlation_analysis_pearson_spearman|상관 분석]] → 원인 [[104_classification_analysis|분류]] → 구조 조치**의 흐름을 보여 주는 편이 좋다. [[136_variance|분산]] 환경의 [[298_qkv_attention|쿼리]] 문제는 SQL 한 줄보다 [[001_dikw_pyramid|데이터]] 분포와 호출 구조가 더 큰 원인인 경우가 많기 때문이다.

- **📢 섹션 요약 비유**: 좋은 운영자는 막힌 고속도로에서 차를 더 세게 몰라고 하지 않는다. 어느 톨게이트와 어느 차선이 병목인지 먼저 찾아야 우회로와 차선 확장을 올바르게 결정할 수 있다.

---

## Ⅴ. 기대효과 및 결론

[[136_variance|분산]] DB 슬로우 [[298_qkv_attention|쿼리]] 역추적 체계를 갖추면 "DB가 느리다"는 막연한 경보가 "Shard-03의 Table Scan 회귀로 인해 checkout [[014_api_posix|API]] P99가 1.8초까지 상승" 같은 행동 가능한 문장으로 바뀐다. 이는 장애 [[658_ir_recovery|복구]] 시간을 줄일 뿐 아니라, 반복되는 query fingerprint를 기준으로 구조적 개선 우선순위를 세우게 해 준다.

또한 [[090_service_kubernetes_network_load_balancing|서비스]], [[264_proxy_pattern_surrogate_access_control|프록시]], DB를 관통하는 공통 Trace ID를 쓰면 조직 간 책임 공방도 줄어든다. 애플리케이션 팀은 재시도 폭증을, 플랫폼 팀은 [[264_proxy_pattern_surrogate_access_control|프록시]] 큐를, DBA는 플랜 회귀를 같은 화면에서 볼 수 있기 때문이다. 즉 관측 [[001_dikw_pyramid|데이터]]가 기술적 진실의 공용 언어가 된다.

한계도 있다. 트레이스 저장 비용, plan capture 오버헤드, [[782_sensitive_information|민감정보]] [[172_maas_mobility_as_a_service|마스]]킹, 보존기간 불일치 문제는 실제 운영에서 반드시 설계해야 한다. 앞으로는 plan regression [[961_deepfake_detection|detection]], adaptive [[056_표본화_Sampling|sampling]], 자동 [[154_database_index_b_tree_search_optimization|인덱스]] 추천이 결합되면서 더 자율적인 [[002_database_definition|데이터베이스]] 운영으로 발전할 가능성이 크다. 따라서 이 주제는 "느린 SQL 찾기"가 아니라 **[[136_variance|분산]] [[015_지연_데이터_관점|지연]]의 인과 경로를 복원하는 [[642_observability_telemetry|observability]] 기법**으로 기억해야 한다.

- **📢 섹션 요약 비유**: 슬로우 [[298_qkv_attention|쿼리]] 역추적은 자동차 계기판이 아니라 블랙박스 분석에 가깝다. 단순히 속도가 느렸다는 사실을 넘어서, 어느 구간에서 왜 브레이크가 걸렸는지까지 밝혀야 재발을 막을 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Query Fingerprint | 바인드 값이 다른 동일 형태 SQL을 묶어 반복 패턴을 찾는 기준 |
| [[146_opentelemetry_otel_observability_standard|OpenTelemetry]] | 애플리케이션·[[264_proxy_pattern_surrogate_access_control|프록시]]·DB 구간의 공통 Trace ID를 만드는 계측 표준 |
| EXPLAIN ANALYZE | 실제 실행 연산자와 row 수를 [[396_validation|확인]]해 플랜 원인을 해석하는 도구 |
| P99 [[141_latency|Latency]] | 평균이 가리는 tail [[141_latency|latency]] 문제를 드러내는 핵심 [[181_slo_service_level_objective|SLO]] 지표 |
| [[001_dikw_pyramid|Data]] Skew | 특정 샤드에 [[001_dikw_pyramid|데이터]]가 몰려 [[136_variance|분산]] [[298_qkv_attention|쿼리]] 시간이 불균형해지는 현상 |
| Plan Regression | 배포나 통계 변화 이후 이전보다 나쁜 [[166_execution_plan_optimizer_navigation_tree|실행 계획]]이 선택되는 문제 |

### 📈 관련 키워드 및 발전 흐름도

```text
슬로우 쿼리 로그 수집
    │
    ▼
Query Fingerprint 정규화
    │
    ▼
Trace ID 기반 요청 상관 분석
    │
    ▼
샤드별 실행 계획 비교 · Plan Hash 관리
    │
    ▼
Adaptive Sampling · 자동 튜닝 연계
```

이 흐름은 "느린 SQL 목록"에서 출발해 "요청 단위 인과 복원"과 "자동 분석"으로 발전하는 관측 성숙도를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [[136_variance|분산]] DB는 여러 창고에서 물건을 가져오는 큰 가게라서, 주문이 늦으면 어느 창고에서 늦었는지 먼저 찾아야 해요.
2. 트레이스는 물건이 지나간 길을 보여 주고, [[298_qkv_attention|쿼리]] 플랜은 왜 그 창고가 느렸는지 이유를 알려줘요.
3. 그래서 둘을 같이 보면 "어디서 막혔는지"와 "왜 막혔는지"를 한 번에 알 수 있어요.
