+++
weight = 179
title = "179. 시계열 DB (Time-Series Database)"
date = "2026-04-21"
[extra]
categories = "studynote-devops-sre"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[057_tsdb_downsampling_retention_policy|시계열 데이터베이스]]([[340_process|Time-Series Database]], TSDB)는 `메트릭 이름 + 태그/레이블 + 타임스탬프 + 값` 형태의 append 중심 [[001_dikw_pyramid|데이터]]를 빠르게 쓰고 범위 조회하도록 설계된 전용 저장 엔진이다.
> 2. **가치**: InfluxDB와 [[136_prometheus|Prometheus]] TSDB는 시간 순 정렬, 블록 [[347_compaction|압축]], 보존 [[164_policy|정책]], [[042_rollup_l2_solution|롤업]]을 이용해 일반 [[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]]보다 훨씬 적은 저장 공간으로 긴 기간의 운영 [[342_routing_metric_hop_bandwidth_delay|메트릭]]을 보관한다.
> 3. **판단 포인트**: 단기 알림 중심인지, 장기 트렌드 분석 중심인지, 카디널리티(Cardinality) 한계를 어떻게 관리할지에 따라 [[136_prometheus|Prometheus]] TSDB, [[255_time_series_rollup_retention_compression|InfluxDB]], 장기 보존 계층의 조합이 달라진다.

---

## Ⅰ. 개요 및 필요성

[[057_tsdb_downsampling_retention_policy|시계열 데이터베이스]]는 시간이 붙은 수치 [[001_dikw_pyramid|데이터]]를 저장하기 위해 등장했다. 서버 CPU (Central Processing Unit) 사용률, 요청 [[015_지연_데이터_관점|지연]]시간, 큐 길이, 센서 온도처럼 같은 종류의 값이 몇 초 또는 몇 분 간격으로 계속 쌓이는 [[001_dikw_pyramid|데이터]]는, 일반 [[191_transaction_concept_states|트랜잭션]] [[001_dikw_pyramid|데이터]]와 구조가 다르다. [[289_cqrs_db|쓰기]]는 매우 자주 일어나고, 조회는 "최근 1시간", "지난 30일 추세"처럼 시간 범위를 기준으로 이루어지며, 오래된 [[001_dikw_pyramid|데이터]]는 세밀함보다 요약이 더 중요해진다.

[[083_relationship_in_er_model|관계]]형 [[002_database_definition|데이터베이스]]([[501_database|Database]], DB)로도 저장은 가능하지만 금방 한계가 드러난다. 타임스탬프 [[154_database_index_b_tree_search_optimization|인덱스]]가 계속 커지고, 고빈도 삽입으로 [[286_page_frame|페이지]] 분할과 [[480_write_amplification|쓰기 증폭]]이 생기며, 오래된 [[001_dikw_pyramid|데이터]]를 지우거나 일별 평균으로 줄이는 작업이 무겁다. 특히 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 수집처럼 초당 수만~수십만 샘플이 들어오는 환경에서는 "[[289_cqrs_db|쓰기]]·보존·집계"를 한 번에 고려한 구조가 필요하다.

TSDB가 다루는 핵심 레코드는 대개 단순하다. 예를 들어 `http_requests_total{service="pay", region="ap"} @ 10:00:15 = 5321`처럼 시리즈 정의와 시간, 값만 있으면 된다. 대신 같은 시리즈가 시간순으로 매우 많이 쌓이므로, 엔진은 정교한 조인보다 빠른 append, 범위 스캔, [[347_compaction|압축]], 보존 삭제에 최적화된다.

```text
┌──────────────────────────────────────────────────────────────┐
│ 메트릭이 TSDB를 거쳐 장기 보존으로 가는 흐름                   │
├──────────────────────────────────────────────────────────────┤
│ Exporter / Agent                                              │
│    │ sample = {series, timestamp, value}                      │
│    ▼                                                          │
│ Ingest Buffer + WAL                                            │
│    ▼                                                          │
│ Hot Block / Recent Cache                                      │
│    ▼                                                          │
│ Compressed Block / Shard                                      │
│    ▼                                                          │
│ Rollup + Retention Tier                                       │
│    ▼                                                          │
│ Alert / Dashboard / Capacity Trend                            │
└──────────────────────────────────────────────────────────────┘
```

그래서 TSDB는 단순히 "시간 컬럼이 있는 [[002_database_definition|데이터베이스]]"가 아니다. 시간순 입력, 최근 [[001_dikw_pyramid|데이터]]의 빠른 조회, 오래된 [[001_dikw_pyramid|데이터]]의 요약 보존, 고카디널리티 제어를 함께 푸는 운영 저장소다. 관측성([[642_observability_telemetry|Observability]])에서 TSDB가 중요한 이유도 [[342_routing_metric_hop_bandwidth_delay|메트릭]]의 양보다 시간 [[164_policy|정책]]을 다루는 능력에 있다.

- **📢 섹션 요약 비유**: TSDB는 매일 같은 온도를 적는 날씨 관측 장부와 같다. 사람 정보나 주문 정보처럼 복잡한 [[083_relationship_in_er_model|관계]]를 적는 장부가 아니라, 시간에 따라 바뀌는 숫자를 빠르게 쓰고 오래된 기록은 묶어서 보관하는 데 특화돼 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

TSDB의 핵심 원리는 매우 단순하다. 최근 [[001_dikw_pyramid|데이터]]는 빠르게 받아 두고, 일정 시간이 지나면 [[347_compaction|압축]]된 불변 블록으로 굳히며, 더 오래된 [[001_dikw_pyramid|데이터]]는 더 거친 해상도로 [[042_rollup_l2_solution|롤업]]한다. InfluxDB와 [[136_prometheus|Prometheus]] TSDB의 세부 구현은 다르지만, Write-Ahead Log (WAL), 메모리상의 최근 버퍼, [[347_compaction|압축]] 블록, 보존 [[164_policy|정책]]이라는 큰 흐름은 비슷하다.

| 구성 요소 | 역할 | [[255_time_series_rollup_retention_compression|InfluxDB]] / [[136_prometheus|Prometheus]] 관점 |
| :--- | :--- | :--- |
| 최근 [[289_cqrs_db|쓰기]] 버퍼 | 최신 샘플을 빠르게 수용 | [[255_time_series_rollup_retention_compression|InfluxDB]] 캐시, [[136_prometheus|Prometheus]] Head Block |
| WAL (Write-Ahead Log) | 장애 시 유실 방지 | 디스크 재복구 시작점 |
| [[347_compaction|압축]] 블록 / 샤드 | 시간 구간별 불변 저장 단위 | [[136_prometheus|Prometheus]] Block, [[255_time_series_rollup_retention_compression|InfluxDB]] Shard 계열 |
| 태그 / 레이블 [[154_database_index_b_tree_search_optimization|인덱스]] | 시리즈 [[655_ir_detection_analysis|식별]]과 필터링 | [[255_time_series_rollup_retention_compression|InfluxDB]] Tag, [[136_prometheus|Prometheus]] Label |
| 보존 [[164_policy|정책]] / [[042_rollup_l2_solution|롤업]] | 오래된 원본 정리와 요약 유지 | [[515_mvcc|Retention]] [[164_policy|Policy]], Recording Rule, Downsampling |

아래 그림은 최근 [[001_dikw_pyramid|데이터]]가 차곡차곡 쌓였다가 [[347_compaction|압축]] 블록으로 굳고, 이후 더 긴 보존 계층으로 넘어가는 과정을 보여준다. 이 구조 덕분에 TSDB는 "최근 [[001_dikw_pyramid|데이터]]는 빠르게, 오래된 [[001_dikw_pyramid|데이터]]는 싸게"라는 두 목표를 동시에 추구할 수 있다.

```text
┌──────────────────────────────────────────────────────────────┐
│ TSDB 저장 엔진의 시간 계층                                    │
├──────────────────────────────────────────────────────────────┤
│ Raw Sample (10s)                                              │
│    │                                                          │
│    ▼                                                          │
│ Head / Cache + WAL                                            │
│    │ flush / checkpoint                                       │
│    ▼                                                          │
│ Compressed Block / Shard                                      │
│    │ compaction                                               │
│    ▼                                                          │
│ Long Block + Downsampled Series                               │
│    │ retention policy                                         │
│    ▼                                                          │
│ Raw 삭제 · Rollup 유지                                         │
└──────────────────────────────────────────────────────────────┘
```

[[347_compaction|압축]]이 잘 되는 이유도 시계열의 특성 때문이다. 타임스탬프는 대체로 일정 간격이므로 Delta-of-Delta 방식으로 아주 작게 저장할 수 있고, 값은 이전 값과 비슷하게 움직여 XOR 기반 Gorilla 계열 [[347_compaction|압축]]이 잘 먹는다. 값이 계속 같거나 완만하게 변하면 Run-Length Encoding이나 단순 [[073_bit|비트]] [[347_compaction|압축]]도 효과적이다.

| [[347_compaction|압축]] / 요약 기법 | 원리 | 효과 |
| :--- | :--- | :--- |
| Delta-of-Delta | 타임스탬프 간격의 변화량만 저장 | 일정 주기 샘플에서 매우 높은 [[347_compaction|압축]]률 |
| XOR / Gorilla 계열 | 이전 [[087_floating_point|부동소수점]] 값과의 차이만 저장 | 작은 변화가 많은 [[342_routing_metric_hop_bandwidth_delay|메트릭]]에 유리 |
| Chunk / Block [[347_compaction|Compaction]] | 작은 조각을 큰 불변 블록으로 병합 | 조회 효율과 삭제 효율 향상 |
| Downsampling / [[042_rollup_l2_solution|Rollup]] | 10초 원본을 1분, 1시간 집계로 축소 | 장기 보존 비용 절감 |

InfluxDB는 Measurement, Tag, Field 분리가 뚜렷해 태그를 인덱싱 축으로 관리하는 데 강점이 있고, [[136_prometheus|Prometheus]] TSDB는 [[342_routing_metric_hop_bandwidth_delay|Metric]] Name + Label Set을 하나의 시리즈로 보고 최근 알림 [[298_qkv_attention|쿼리]]와 [[205_kubernetes_container_orchestration|Kubernetes]] [[342_routing_metric_hop_bandwidth_delay|메트릭]] 수집에 최적화되어 있다. 그러나 둘 다 공통적으로 "시간 범위 스캔이 빠르고, 오래된 [[001_dikw_pyramid|데이터]]를 [[164_policy|정책]]적으로 줄일 수 있어야 한다"는 동일한 목적 아래 움직인다.

- **📢 섹션 요약 비유**: TSDB 엔진은 냉장고와 냉동고를 함께 쓰는 주방과 같다. 바로 쓸 재료는 냉장고에 두고, 오래 둘 것은 냉동실에 [[347_compaction|압축]] 보관하며, 너무 오래된 재료는 손질해 육수나 소스로 다시 저장한다.

---

## Ⅲ. 비교 및 연결

TSDB를 이해하려면 일반 DB와 [[136_prometheus|Prometheus]] TSDB, InfluxDB의 경계를 함께 봐야 한다. [[083_relationship_in_er_model|관계]]형 DB는 조인과 [[191_transaction_concept_states|트랜잭션]]에 강하지만 초고빈도 시계열 [[289_cqrs_db|쓰기]]와 장기 범위 집계에는 불리하다. [[136_prometheus|Prometheus]] TSDB는 짧은~중간 보존 기간의 인프라 [[342_routing_metric_hop_bandwidth_delay|메트릭]]과 경보에 매우 강하고, InfluxDB는 더 유연한 수집·보존 [[164_policy|정책]]과 장기 센서 [[001_dikw_pyramid|데이터]], 혼합 [[341_time_series_ar_ma_arma|시계열 분석]]에 상대적으로 잘 맞는다.

| 항목 | [[083_relationship_in_er_model|관계]]형 DB | [[136_prometheus|Prometheus]] TSDB | [[255_time_series_rollup_retention_compression|InfluxDB]] |
| :--- | :--- | :--- | :--- |
| 주된 [[014_data_model_components|데이터 모델]] | 행 기반 [[002_structured_data|정형 데이터]] | [[342_routing_metric_hop_bandwidth_delay|메트릭]] + Label Set | Measurement + Tag + Field |
| 강점 | 조인, [[191_transaction_concept_states|트랜잭션]], 정합성 | 경보, PromQL, K8s 친화성 | 장기 보존, 다양한 수집 계층, [[341_time_series_ar_ma_arma|시계열 분석]] 유연성 |
| 약점 | 고빈도 삽입·삭제 비용 큼 | 기본 단기 보존, 고카디널리티 주의 | 태그 설계 실패 시 [[154_database_index_b_tree_search_optimization|인덱스]] 비용 증가 |
| 잘 맞는 용도 | 업무 시스템, 리포팅 | 운영 관측성, 실시간 알림 | [[101_iot_concept|IoT]], 공정 [[001_dikw_pyramid|데이터]], 장기 추세 |

여기서 가장 중요한 공통 [[096_risk_non_risk_architecture_evaluation_flaws|리스크]]는 카디널리티다. 카디널리티는 "고유 시계열 개수"를 뜻하며, 대략 `메트릭 수 × 태그/레이블 조합 수`로 늘어난다. `user_id`, `request_id`, `session_id`처럼 사실상 무한한 값을 태그나 레이블에 넣으면 시리즈 수가 폭증해 메모리와 [[154_database_index_b_tree_search_optimization|인덱스]]가 무너진다.

예를 들어 `http_requests_total{service="pay", status="200"}`는 안전한 편이지만, 여기에 `request_id`를 붙이면 요청마다 새로운 시리즈가 생긴다. 이는 [[342_routing_metric_hop_bandwidth_delay|메트릭]]을 저장하는 TSDB를 [[568_logs_distributed_logging_elk_fluentd|로그]] 저장소처럼 오용하는 대표 사례다. 관측성에서는 태그/레이블을 "집계 차원"으로만 쓰고, 개별 이벤트 [[289_identification_flags_fragmentation_offset|식별자]]는 [[568_logs_distributed_logging_elk_fluentd|로그]]나 트레이스로 보내는 것이 원칙에 가깝다.

또한 TSDB는 [[168_grafana|Grafana]], [[146_opentelemetry_otel_observability_standard|OpenTelemetry]], 장기 보존 계층과 강하게 연결된다. Prometheus는 Remote Write로 장기 저장소에 넘길 수 있고, InfluxDB는 수집 에이전트와 [[150_task|태스크]]를 통해 [[042_rollup_l2_solution|롤업]]과 [[341_time_series_ar_ma_arma|시계열 분석]]을 확장할 수 있다. 즉 TSDB는 독립 제품이 아니라, 관측성 [[123_pipe|파이프]]라인의 중심 저장 계층으로 이해하는 편이 정확하다.

- **📢 섹션 요약 비유**: [[136_prometheus|Prometheus]] TSDB와 InfluxDB는 둘 다 시간표 전용 서랍장이지만, 하나는 현재 열차 운행 상황판에 더 강하고 다른 하나는 장기간 운행 기록을 보관하는 기록실에 더 강한 셈이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 "어떤 TSDB가 최고인가"보다 "어떤 질문을 얼마나 오래, 얼마나 자주 던질 것인가"가 더 중요하다. 알림 중심이면 최근 [[001_dikw_pyramid|데이터]] 조회와 간결한 질의가 중요하고, 용량 계획이나 설비 운영이면 장기 보존과 [[042_rollup_l2_solution|롤업]] [[164_policy|정책]]이 더 중요하다. 그래서 하나의 TSDB로 모든 요구를 해결하려 하기보다, 단기 운영 계층과 장기 분석 계층을 분리하는 설계가 흔하다.

| 운영 상황 | 권장 판단 | 이유 |
| :--- | :--- | :--- |
| [[205_kubernetes_container_orchestration|Kubernetes]] 인프라 경보 중심 | [[136_prometheus|Prometheus]] TSDB 우선 | 수집·경보·[[298_qkv_attention|쿼리]] 생태계가 잘 맞음 |
| 공장 센서 / 설비 장기 추세 | [[255_time_series_rollup_retention_compression|InfluxDB]] 계열 검토 | 장기 보존, 태그 기반 [[341_time_series_ar_ma_arma|시계열 분석]]에 강점 |
| 멀티클러스터 장기 보존 | [[136_prometheus|Prometheus]] + Remote Storage | 단기 알림과 장기 분석 요구를 분리 가능 |
| 복잡한 조인 리포트 필요 | TSDB + Warehouse 병행 | TSDB 단독으로는 [[083_relationship_in_er_model|관계]]형 분석 한계 |

실무 [[435_checklist_based_testing|체크리스트]]는 다음과 같다.

1. 태그/레이블은 집계 차원인가, 아니면 사실상 개별 [[289_identification_flags_fragmentation_offset|식별자]]인가?
2. 원본 해상도와 [[042_rollup_l2_solution|롤업]] 해상도를 몇 단계로 가져갈 것인가?
3. 최근 7일 알림용 [[001_dikw_pyramid|데이터]]와 1년 용량 계획용 [[001_dikw_pyramid|데이터]]를 같은 스토어에 둘 필요가 있는가?
4. [[289_cqrs_db|쓰기]] 속도, WAL 적재량, 컴팩션 [[015_지연_데이터_관점|지연]], [[298_qkv_attention|쿼리]] 팬아웃을 함께 [[229_monitor|모니터]]링하는가?
5. [[342_routing_metric_hop_bandwidth_delay|메트릭]], [[568_logs_distributed_logging_elk_fluentd|로그]], 트레이스의 경계를 분명히 구분하고 있는가?

흔한 [[128_water_scrum_fall_anti_pattern|안티패턴]]도 뚜렷하다. 무한 보존을 기본으로 두고 원본 [[001_dikw_pyramid|데이터]]를 계속 쌓는 경우, 요청 ID를 태그로 넣어 시리즈 폭발을 만드는 경우, TSDB에서 복잡한 조인과 행 단위 갱신까지 기대하는 경우가 대표적이다. 또 다운샘플링 [[164_policy|정책]] 없이 장기 보존만 늘리면 저장 비용은 물론 [[298_qkv_attention|쿼리]] [[015_지연_데이터_관점|지연]]도 함께 커진다.

기술사 답안에서는 "Prometheus냐 InfluxDB냐"보다 보존 기간, [[042_rollup_l2_solution|롤업]] [[164_policy|정책]], 카디널리티 관리, 장기 보존 계층 결합 여부를 함께 제시해야 설득력이 있다. 즉 TSDB 선택은 제품 비교보다 시간 해상도 [[164_policy|정책]]과 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 모델링 문제에 더 가깝다.

```text
┌──────────────────────────────────────────────────────────────┐
│ TSDB 선택의 실무 분기                                         │
├──────────────────────────────────────────────────────────────┤
│ 실시간 알림 중심? ──────── 예 ─▶ Prometheus TSDB 중심         │
│            │                                                  │
│            아니오                                              │
│            ▼                                                  │
│ 장기 센서·추세 보존 중심? ─ 예 ─▶ InfluxDB 계열 검토          │
│            │                                                  │
│            아니오                                              │
│            ▼                                                  │
│ 조인·정형 분석 비중 큼 ───▶ Warehouse / RDBMS 병행            │
└──────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: TSDB 선택은 냉장고를 고르는 일이 아니라, 신선식품 냉장고·장기 보관 냉동고·식자재 창고를 어떻게 나눌지 정하는 일과 같다. 어떤 음식을 얼마나 오래 보관할지에 따라 답이 달라진다.

---

## Ⅴ. 기대효과 및 결론

TSDB를 올바르게 도입하면 [[342_routing_metric_hop_bandwidth_delay|메트릭]] 저장 비용을 크게 줄이면서도, 최근 장애 분석부터 월간 용량 계획까지 시간 범위 질문에 빠르게 답할 수 있다. 최근 [[001_dikw_pyramid|데이터]]는 세밀하게 유지하고 오래된 [[001_dikw_pyramid|데이터]]는 [[042_rollup_l2_solution|롤업]]해 남기므로, 운영자는 "지금 무슨 일이 일어나는가"와 "한 달간 어떤 추세였는가"를 같은 계보에서 볼 수 있다. 이는 관측성 품질과 운영 의사결정 속도를 동시에 높인다.

하지만 TSDB는 만능 저장소가 아니다. 조인과 다중 엔터티 [[083_relationship_in_er_model|관계]] 분석, 강한 [[191_transaction_concept_states|트랜잭션]], 개별 레코드 수정에는 적합하지 않다. 또한 카디널리티 관리에 실패하면 [[347_compaction|압축]]률과 조회 속도가 모두 무너질 수 있으므로, 태그 설계와 보존 [[164_policy|정책]]이 기술보다 더 중요한 경우도 많다.

결국 기억해야 할 본질은 이렇다. TSDB는 "시간이 붙은 숫자를 저장하는 [[002_database_definition|데이터베이스]]"가 아니라, 시간에 따라 가치가 달라지는 [[001_dikw_pyramid|데이터]]를 어떻게 저장·[[347_compaction|압축]]·요약·폐기할지 결정하는 엔진이다. InfluxDB와 [[136_prometheus|Prometheus]] TSDB의 차이를 이해하는 것도 중요하지만, 그보다 먼저 시계열 [[001_dikw_pyramid|데이터]]의 시간 [[164_policy|정책]]을 설계할 줄 알아야 한다.

- **📢 섹션 요약 비유**: TSDB는 숫자를 모아 두는 창고가 아니라, 신선한 재료는 바로 쓰고 오래된 재료는 육수로 우려내며 남는 것은 버리는 주방 운영 규칙에 더 가깝다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[342_routing_metric_hop_bandwidth_delay|Metric]] / Measurement | 시계열의 이름과 의미를 정의하는 기본 단위 |
| Label / Tag | 집계와 필터링 축을 결정하는 시리즈 [[655_ir_detection_analysis|식별]] 정보 |
| Cardinality | 고유 시계열 개수로, TSDB 비용과 [[282_performance_tactics|성능]]의 핵심 제약 |
| WAL (Write-Ahead Log) | 최근 샘플 유실을 방지하는 [[658_ir_recovery|복구]] [[568_logs_distributed_logging_elk_fluentd|로그]] |
| [[347_compaction|Compaction]] | 작은 조각을 큰 [[347_compaction|압축]] 블록으로 묶는 저장 최적화 과정 |
| Downsampling / [[042_rollup_l2_solution|Rollup]] | 오래된 [[001_dikw_pyramid|데이터]]를 더 거친 해상도로 유지하는 장기 보존 [[268_strategy_pattern|전략]] |
| PromQL / Flux | TSDB에 시간 범위 질의를 던지는 대표 언어 계열 |

### 📈 관련 키워드 및 발전 흐름도

```text
Timestamped Sample
    │
    ▼
Append Ingest + WAL
    │
    ▼
Compressed Chunk / Block
    │
    ▼
Retention + Rollup
    │
    ▼
Alerting · Dashboard · Capacity Planning
```

이 흐름은 TSDB의 핵심이 단순 저장이 아니라, 시간 해상도와 보존 [[164_policy|정책]]을 단계적으로 관리하는 데 있음을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. TSDB는 매일 키를 재서 적는 성장 노트처럼, 시간 순서대로 숫자를 모으는 특별한 공책이에요.
2. 오래된 숫자는 하나하나 다 남기지 않고 "이번 달 평균"처럼 묶어서 적으면 훨씬 덜 복잡해져요.
3. 그래서 지금 얼마나 자랐는지도 빨리 보고, 오래전부터 어떻게 변했는지도 쉽게 알 수 있어요.
