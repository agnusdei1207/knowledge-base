---
title: 309. 시계열 데이터베이스 InfluxDB 다운샘플링 롤업 (Time-Series DB Downsampling)
date: '2026-04-21'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시계열 DB의 다운샘플링(Downsampling)은 고해상도 [[001_dikw_pyramid|데이터]]를 시간 경과에 따라 자동으로 저해상도로 [[042_rollup_l2_solution|롤업]]하여 스토리지를 최대 99.97%까지 절감한다.
> 2. **가치**: 1초 단위 원시 [[001_dikw_pyramid|데이터]]를 무기한 보관하면 연간 TB~PB 급 스토리지가 필요하지만, 다운샘플링으로 실제 비용 지출을 1%대로 [[347_compaction|압축]]할 수 있다.
> 3. **판단 포인트**: [[042_rollup_l2_solution|롤업]] 후 원시 [[001_dikw_pyramid|데이터]]는 삭제되므로, 어느 시간 해상도까지 보존할지를 사전에 비즈니스 요구사항과 함께 결정해야 한다.

## Ⅰ. 개요 및 필요성

[[101_iot_concept|IoT]] 센서, 서버 [[342_routing_metric_hop_bandwidth_delay|메트릭]], 금융 시세 [[001_dikw_pyramid|데이터]]는 초당 수천~수백만 건의 [[001_dikw_pyramid|데이터]] 포인트를 [[087_process_state_transition|생성]]한다.
이 [[001_dikw_pyramid|데이터]]를 모두 원시 형태로 무기한 보관하면 스토리지 비용이 폭발적으로 증가한다.

InfluxDB는 시계열 전용 TSDB ([[340_process|Time-Series Database]])로, 리텐션 [[164_policy|정책]]([[515_mvcc|Retention]] [[164_policy|Policy]])과 연속 [[298_qkv_attention|쿼리]](Continuous Query) 또는 [[150_task|Task]]([[255_time_series_rollup_retention_compression|InfluxDB]] 2.x)를 통해 자동 다운샘플링을 지원한다.

스토리지 절감 계산:
- 1초 [[001_dikw_pyramid|데이터]] 1일 = 86,400 포인트 (100%)
- 1분 [[042_rollup_l2_solution|롤업]] 1일 = 1,440 포인트 (절감 98.3%, 1.7% 남음)
- 1시간 [[042_rollup_l2_solution|롤업]] 1일 = 24 포인트 (절감 99.97%, 0.03% 남음)

📢 **섹션 요약 비유**: 다운샘플링은 사진 원본을 수년 후 썸네일로 [[347_compaction|압축]] 저장하는 것이다. 오래될수록 해상도는 낮아지지만 공간은 훨씬 절약된다.

## Ⅱ. 아키텍처 및 핵심 원리

### [[255_time_series_rollup_retention_compression|InfluxDB]] 핵심 개념

| 개념 | 설명 | 예시 |
|:---|:---|:---|
| Measurement | 테이블에 해당 | cpu_usage |
| Tag | [[154_database_index_b_tree_search_optimization|인덱스]]되는 [[012_metadata|메타데이터]] (String) | host=server01 |
| Field | 실제 측정값 (Number) | value=82.5 |
| Timestamp | 나노초 [[233_precision_recall_f1_roc_auc_threshold|정밀도]] | 2024-01-15T12:00:00Z |
| [[515_mvcc|Retention]] [[164_policy|Policy]] | [[001_dikw_pyramid|데이터]] 보관 기간 | 30d, INF |
| Continuous Query | 자동 집계 작업 | MEAN 1분 [[042_rollup_l2_solution|롤업]] |

### Tag vs Field 설계 원칙

- **Tag** (인덱싱됨): 자주 필터링하는 저카디널리티 값 (host, region, env)
- **Field** (비인덱싱): 측정 수치 (CPU%, 온도, 응답시간)
- 고카디널리티 값을 Tag로 쓰면 [[154_database_index_b_tree_search_optimization|인덱스]] 폭발 → DB [[282_performance_tactics|성능]] 급락

### [[103_ascii|ASCII]] 다이어그램: [[001_dikw_pyramid|데이터]] 보존 계층 ([[515_mvcc|Retention]] Tier)

```
  실시간 수집 (초당 수천 포인트)
        │
        ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  Tier 1: Raw (1초 해상도)                                    │
  │  보관: 30일  스토리지: 100%  용도: 실시간 모니터링·알람       │
  └───────────────────────────┬──────────────────────────────────┘
                              │ Continuous Query: MEAN(value) 1분
                              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  Tier 2: 1분 롤업                                            │
  │  보관: 1년   스토리지: 1.7%  용도: 일간 트렌드·용량 계획     │
  └───────────────────────────┬──────────────────────────────────┘
                              │ Continuous Query: MEAN(value) 1시간
                              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  Tier 3: 1시간 롤업                                          │
  │  보관: 5년+  스토리지: 0.03%  용도: 연간 리포트·장기 분석    │
  └──────────────────────────────────────────────────────────────┘
```

### TSM 스토리지 엔진 (Time-Structured Merge Tree)

InfluxDB는 LSM (Log-Structured Merge Tree) 변형인 TSM 엔진을 사용한다.
- WAL (Write-Ahead Log) → 인메모리 Cache → TSM [[501_file_definition_logical_record|파일]] → [[347_compaction|Compaction]]
- 시계열 특성상 [[289_cqrs_db|쓰기]]는 항상 최신 타임스탬프 → [[347_compaction|압축]] 효율 극대화

| TSDB 비교 | [[255_time_series_rollup_retention_compression|InfluxDB]] | TimescaleDB | [[136_prometheus|Prometheus]] |
|:---|:---|:---|:---|
| 기반 | 전용 TSM | PostgreSQL 확장 | 자체 TSDB |
| [[298_qkv_attention|쿼리]] 언어 | Flux/InfluxQL | SQL | PromQL |
| 주요 용도 | [[101_iot_concept|IoT]], [[342_routing_metric_hop_bandwidth_delay|메트릭]] | 금융, 이벤트 | K8s [[229_monitor|모니터]]링 |

📢 **섹션 요약 비유**: TSM 엔진은 날짜별로 자동 정리되는 일기장이다. 새 내용은 날짜 순서대로 추가되고, 오래된 [[286_page_frame|페이지]]는 자동으로 요약·[[347_compaction|압축]]된다.

## Ⅲ. 비교 및 연결

### 시계열 DB 활용 패턴

| 패턴 | 도구 선택 | 이유 |
|:---|:---|:---|
| [[205_kubernetes_container_orchestration|Kubernetes]] [[342_routing_metric_hop_bandwidth_delay|메트릭]] | [[136_prometheus|Prometheus]] | PromQL 생태계, Alert 통합 |
| [[101_iot_concept|IoT]] 장비 [[001_dikw_pyramid|데이터]] | [[255_time_series_rollup_retention_compression|InfluxDB]] | 고쓰기 [[139_throughput|처리량]], 다운샘플링 |
| 금융 [[341_time_series_ar_ma_arma|시계열 분석]] | TimescaleDB | SQL [[298_qkv_attention|쿼리]], 복잡 [[521_join|JOIN]] |

📢 **섹션 요약 비유**: Prometheus는 단거리 달리기 선수(짧은 보관, 빠른 조회), InfluxDB는 중거리 선수(중기 보관, 다운샘플링), TimescaleDB는 마라톤 선수(장기 보관, SQL 분석)다.

## Ⅳ. 실무 적용 및 기술사 판단

### 다운샘플링 설계 [[435_checklist_based_testing|체크리스트]]

- [ ] [[001_dikw_pyramid|데이터]] 소스별 수집 빈도 파악 (초당 포인트 수)
- [ ] 비즈니스별 최소 필요 해상도 정의 (알람: 1초, 트렌드: 1분, 리포트: 1시간)
- [ ] [[042_rollup_l2_solution|롤업]] [[147_aggregate_function_group_by|집계 함수]] 선정: MEAN, MAX, MIN, SUM
- [ ] 원시 [[001_dikw_pyramid|데이터]] 보관 기간 결정 (스토리지 비용과 분석 요구 균형)
- [ ] 고카디널리티 Tag 사용 금지 (UUID, 사용자 ID는 Field로)

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

| [[128_water_scrum_fall_anti_pattern|안티패턴]] | 문제 | 해결 방법 |
|:---|:---|:---|
| 모든 [[001_dikw_pyramid|데이터]] 무기한 보관 | 스토리지 폭발, [[282_performance_tactics|성능]] 저하 | [[515_mvcc|Retention]] [[164_policy|Policy]] 필수 설계 |
| UUID를 Tag로 사용 | 카디널리티 폭발 → DB 메모리 부족 | Field로 변경 |
| 단일 Measurement에 모든 [[342_routing_metric_hop_bandwidth_delay|메트릭]] | 태그 조합 폭발 | [[064_relation_domain|도메인]]별 Measurement 분리 |

📢 **섹션 요약 비유**: 고카디널리티 Tag는 도서관에서 책마다 새 서가를 만드는 것이다. 서가가 폭발해 도서관이 무너진다.

## Ⅴ. 기대효과 및 결론

| 항목 | 다운샘플링 미적용 | 적용 후 |
|:---|:---|:---|
| 스토리지 (1년) | 100% | 1초→1분: 1.7%, 1초→1시간: 0.03% |
| 장기 [[298_qkv_attention|쿼리]] 속도 | 수분 (수억 행 스캔) | 수초 (소량 [[042_rollup_l2_solution|롤업]] [[001_dikw_pyramid|데이터]]) |
| 인프라 비용 | 매월 증가 | 예측 가능한 고정 비용 |

📢 **섹션 요약 비유**: 다운샘플링 후 원시 [[001_dikw_pyramid|데이터]] 삭제는 음식을 냉동 건조하는 것이다. 공간은 극적으로 줄지만 원래 맛(세밀한 분석)을 완전히 재현하기는 어렵다.

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[255_time_series_rollup_retention_compression|InfluxDB]] | 플랫폼 | 시계열 전용 TSDB |
| [[515_mvcc|Retention]] [[164_policy|Policy]] | 핵심 [[009_config|설정]] | [[001_dikw_pyramid|데이터]] 보관 기간 [[164_policy|정책]] |
| Continuous Query | 핵심 기능 | 자동 집계·[[042_rollup_l2_solution|롤업]] |
| TSM Engine | 저장 엔진 | 시계열 최적화 저장 구조 |
| Tag vs Field | 설계 원칙 | [[154_database_index_b_tree_search_optimization|인덱스]] 폭발 방지 |

### 📈 관련 키워드 및 발전 흐름도

```
RDB 시계열 저장 - 쓰기 병목·스토리지 폭증
    │
    ▼
시계열 DB 전용 (InfluxDB, Prometheus) 등장
    │
    ▼
고해상도 실시간 데이터 → 시간 경과 후 용량 문제
    │
    ▼
Downsampling - 집계 함수로 해상도 단계적 축소
    │
    ▼
Retention Policy + CQ (Continuous Query) 자동화
```

> **키워드**: [[255_time_series_rollup_retention_compression|InfluxDB]], [[135_time_series_db|Time Series DB]], Downsampling, [[515_mvcc|Retention]] [[164_policy|Policy]], Continuous Query, [[136_prometheus|Prometheus]], Telegraf, Flux

### 👶 어린이를 위한 3줄 비유 설명

1. 시계열 DB는 매초 사진을 찍는 카메라예요. 오래된 사진은 자동으로 작은 썸네일로 [[347_compaction|압축]]돼요.
2. 다운샘플링은 1분치 사진 60장을 1장의 평균 사진으로 만드는 거예요.
3. Tag는 서랍 라벨, Field는 서랍 안 물건이에요. 라벨이 너무 많으면 서랍장이 꽉 차서 못 열어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 309 / 482

← **이전**: [[308_ai_bi_augmented_analytics|308. AI BI 증강 분석 자동화 (Augmented Analytics)]]
**다음**: [[310_neo4j_fraud_detection|310. 그래프 데이터베이스 Neo4j 사기 탐지 최단 경로 (Neo4j Fraud Detection)]] →

---
