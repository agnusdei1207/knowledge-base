---
title: 307. 다차원 큐브 MOLAP ROLAP HOLAP 성능 튜닝 (Multidimensional OLAP)
date: '2026-04-21'
tags:
- studynote-enterprise-systems
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[316_olap|OLAP]] ([[211_olap_drill_down_roll_up_surrogate_key|Online Analytical Processing]]) 큐브는 사전 집계를 통해 BI [[298_qkv_attention|쿼리]] [[138_response_time|응답 시간]]을 1초 이내로 단축하는 다차원 [[001_dikw_pyramid|데이터]] 구조다.
> 2. **가치**: MOLAP은 <1초 응답으로 경영진 대시보드에 최적이나 스토리지 비용이 크고, ROLAP은 무제한 차원을 지원하지만 5~30초 [[015_지연_데이터_관점|지연]]이 있다.
> 3. **판단 포인트**: 큐브 빌드 시간([[336_molap|MOLAP]] 수시간)과 [[001_dikw_pyramid|데이터]] 신선도 요구를 맞바꾸는 트레이드오프가 핵심 설계 결정이다.

## Ⅰ. 개요 및 필요성

[[316_olap|OLAP]] ([[211_olap_drill_down_roll_up_surrogate_key|Online Analytical Processing]])은 다차원 관점에서 [[001_dikw_pyramid|데이터]]를 [[331_neuromorphic_ai_db|Slice]]·Dice·[[330_olap_rollup_drilldown|Roll-up]]·Drill-down하는 분석 기법이다.
수억 건의 거래 [[001_dikw_pyramid|데이터]]를 매번 집계하면 수십 분이 걸리지만, 큐브(Cube)에 사전 집계해두면 1초 이내로 조회 가능하다.

주요 유형:
- [[336_molap|MOLAP]] ([[336_molap|Multidimensional OLAP]]): [[001_dikw_pyramid|데이터]]를 전용 다차원 [[055_array|배열]] 구조로 저장
- [[337_rolap|ROLAP]] ([[337_rolap|Relational OLAP]]): [[083_relationship_in_er_model|관계]]형 DB([[334_star_schema|스타 스키마]]) 위에서 동적 집계
- [[338_holap|HOLAP]] ([[338_holap|Hybrid OLAP]]): 요약 [[001_dikw_pyramid|데이터]]는 [[336_molap|MOLAP]], 세부 [[001_dikw_pyramid|데이터]]는 [[337_rolap|ROLAP]]

MDX (Multidimensional Expressions)는 [[316_olap|OLAP]] 큐브 [[298_qkv_attention|쿼리]] 언어다.

📢 **섹션 요약 비유**: [[316_olap|OLAP]] 큐브는 미리 잘라 놓은 요리 재료 통이다. 주문이 들어오면 즉시 꺼내 담기만 하면 되므로 응답이 [[148_5g_embb_urllc_mmtc|초고속]]이다.

## Ⅱ. 아키텍처 및 핵심 원리

### [[336_molap|MOLAP]] vs [[337_rolap|ROLAP]] vs [[338_holap|HOLAP]] 비교

| 항목 | [[336_molap|MOLAP]] | [[337_rolap|ROLAP]] | [[338_holap|HOLAP]] |
|:---|:---|:---|:---|
| 저장 방식 | 다차원 [[055_array|배열]] (전용 엔진) | [[083_relationship_in_er_model|관계]]형 DB [[334_star_schema|스타 스키마]] | 혼합 |
| [[298_qkv_attention|쿼리]] 속도 | <1초 (사전 집계) | 5~30초 (온디맨드) | 중간 |
| [[001_dikw_pyramid|데이터]] 신선도 | 큐브 빌드 주기 (수시간) | 실시간 가능 | 중간 |
| 스토리지 | 크다 (원본의 2~5배) | 원본 [[209_data_warehouse_schema_on_write|DW]] 동일 | 중간 |
| 확장성 | 차원 수 제한 (~20개) | 무제한 | 중간 |
| 도구 | SSAS [[336_molap|MOLAP]], Essbase | SSAS [[337_rolap|ROLAP]], Mondrian | SSAS [[338_holap|HOLAP]] |

### [[103_ascii|ASCII]] 다이어그램: [[336_molap|MOLAP]] 3차원 큐브 구조

```
  ┌────────────────────────────────────────────────┐
  │           MOLAP Cube: Sales                    │
  │                                                │
  │         제품 차원 (Product)                     │
  │        ┌─────┬─────┬─────┐                    │
  │       /│     │     │     │/                   │
  │      / └─────┴─────┴─────┘                    │
  │  시간 / ──────────────────▶ 지역 차원 (Region)  │
  │  차원 ┌─────┬─────┬─────┐                      │
  │ (Time)│2022 │2023 │2024 │                      │
  │       ├─────┼─────┼─────┤                      │
  │       │ 서울 │ 부산 │ 대구 │  각 셀 = 사전 집계값 │
  │       ├─────┼─────┼─────┤  (합계, 평균, 최대 등) │
  │       │ ... │ ... │ ... │                      │
  │       └─────┴─────┴─────┘                      │
  │  큐브 빌드: 야간 배치 (수시간)                   │
  │  조회 응답: <1초 (사전 집계 인덱스)              │
  └────────────────────────────────────────────────┘
```

### [[179_table_partitioning_concept|파티셔닝]] [[268_strategy_pattern|전략]]

| [[268_strategy_pattern|전략]] | 방법 | 효과 |
|:---|:---|:---|
| 시간 [[179_table_partitioning_concept|파티셔닝]] | 연도별 큐브 분리 | 빌드 시간 [[136_variance|분산]], 부분 갱신 |
| 증분 빌드 | 변경 [[001_dikw_pyramid|데이터]]만 재빌드 | 90% 빌드 시간 단축 |
| 집계 최소화 | 자주 쓰는 조합만 | 스토리지 50% 절감 |

📢 **섹션 요약 비유**: 큐브 [[179_table_partitioning_concept|파티셔닝]]은 도서관 서가를 연도별로 나누는 것이다. 최근 책만 꺼내려면 최근 서가만 뒤지면 된다.

## Ⅲ. 비교 및 연결

### 큐브 빌드 시간 최적화

| 최적화 방법 | 효과 | 주의 |
|:---|:---|:---|
| 증분 빌드 (Incremental) | 전체 대비 90% 시간 단축 | 팩트 변경 시 무효화 |
| [[430_index_fast_full_scan|병렬]] [[514_partition_slice_volume|파티션]] 빌드 | CPU 코어 활용 극대화 | 메모리 압박 |
| 집계 설계 최소화 | 스토리지·빌드 시간 감소 | [[298_qkv_attention|쿼리]] 속도 일부 저하 |

📢 **섹션 요약 비유**: 큐브 빌드는 시험 전 정리된 요약 노트 만들기다. 노트가 완성되면 시험은 빠르지만, 노트 만드는 데 밤새 걸린다.

## Ⅳ. 실무 적용 및 기술사 판단

### [[316_olap|OLAP]] 설계 [[435_checklist_based_testing|체크리스트]]

- [ ] 조회 응답 [[085_sla|SLA]]: <1초면 [[336_molap|MOLAP]], 5~30초 허용이면 [[337_rolap|ROLAP]] 검토
- [ ] [[001_dikw_pyramid|데이터]] 신선도 요구: 실시간이면 [[337_rolap|ROLAP]] 또는 [[294_oltp_vs_olap|HTAP]] 검토
- [ ] 차원 수: 20개 초과 시 [[337_rolap|ROLAP]] 권장
- [ ] 스토리지 예산: MOLAP은 원시 [[001_dikw_pyramid|데이터]]의 2~5배 스토리지 필요
- [ ] [[334_star_schema|스타 스키마]](팩트·[[273_dimension_table_analysis_perspective|차원 테이블]]) [[093_normalization|정규화]] 선행 필수

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

| [[128_water_scrum_fall_anti_pattern|안티패턴]] | 문제 | 해결 방법 |
|:---|:---|:---|
| 모든 차원 조합 사전 집계 | 스토리지 폭발 | 자주 쓰는 조합만 선택적 집계 |
| 세분화된 시간 차원 과다 | 희소 큐브, 빌드 시간 급증 | 일·월·분기·연 4레벨로 제한 |

📢 **섹션 요약 비유**: 모든 집계를 미리 계산하는 건 모든 음식 레시피를 미리 만들어 냉동해두는 것이다. 냉동실이 넘친다.

## Ⅴ. 기대효과 및 결론

| 항목 | [[225_raw|Raw]] SQL | [[316_olap|OLAP]] 큐브 도입 |
|:---|:---|:---|
| [[298_qkv_attention|쿼리]] [[138_response_time|응답 시간]] | 5~30분 (수억 행 집계) | <1초 ([[336_molap|MOLAP]]) |
| 경영진 셀프서비스 | 불가 (IT 의존) | 드래그앤드롭 분석 |
| BI 도구 연동 | 제한적 | Excel, [[165_power_bi|Power BI]] 직접 연결 |

📢 **섹션 요약 비유**: 큐브 도입 결정은 사전에 재료를 손질해 두느냐 vs 주문받고 바로 손질하느냐의 선택이다. 주문량이 많으면 미리 손질하는 게 낫지만, 신선도가 중요하다면 즉석 요리가 낫다.

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| [[336_molap|MOLAP]] | 유형 | 다차원 [[055_array|배열]] 사전 집계 |
| [[337_rolap|ROLAP]] | 유형 | [[083_relationship_in_er_model|관계]]형 DB 온디맨드 집계 |
| [[338_holap|HOLAP]] | 유형 | 혼합 방식 |
| MDX | [[298_qkv_attention|쿼리]] 언어 | 큐브 조회 전용 언어 |
| Cube [[514_partition_slice_volume|Partition]] | 최적화 | 증분 빌드로 빌드 시간 단축 |

### 📈 관련 키워드 및 발전 흐름도

```
평면 2D 리포트 한계 - 다차원 분석 필요성
    │
    ▼
MOLAP - 전용 큐브 스토리지 (빠른 쿼리, 공간 비용)
    │
    ▼
ROLAP - RDB 기반 스타 스키마 (확장성, 느린 쿼리)
    │
    ▼
HOLAP - MOLAP+ROLAP 하이브리드 계층화
    │
    ▼
현대 OLAP (Druid, ClickHouse) - 실시간 집계 진화
```

> **키워드**: [[336_molap|MOLAP]], [[337_rolap|ROLAP]], [[338_holap|HOLAP]], [[316_olap|OLAP]] Cube, [[296_star_schema|Star Schema]], [[313_snowflake_schema|Snowflake Schema]], Drill-Down, ClickHouse

### 👶 어린이를 위한 3줄 비유 설명

1. [[316_olap|OLAP]] 큐브는 미리 잘라 포장해 둔 음식 세트예요. 주문이 오면 바로 꺼내주면 돼요.
2. MOLAP은 모든 세트를 미리 만들어 냉장 보관한 것, ROLAP은 주문 즉시 만드는 것이에요.
3. HOLAP은 자주 팔리는 인기 메뉴는 미리 만들고, 특별 주문만 즉석 요리하는 방식이에요.
