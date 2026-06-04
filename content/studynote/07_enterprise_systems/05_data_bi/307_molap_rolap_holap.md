---
title: "307. 다차원 큐브 MOLAP ROLAP HOLAP 성능 튜닝 (Multidimensional OLAP)"
date: "2026-04-21"
tags:
  - "studynote-enterprise-systems"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) ([Online Analytical Processing](/studynote/14_data_engineering/05_exam_keywords/211_olap_drill_down_roll_up_surrogate_key/)) 큐브는 사전 집계를 통해 BI [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/)을 1초 이내로 단축하는 다차원 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조다.
> 2. **가치**: MOLAP은 <1초 응답으로 경영진 대시보드에 최적이나 스토리지 비용이 크고, ROLAP은 무제한 차원을 지원하지만 5~30초 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 있다.
> 3. **판단 포인트**: 큐브 빌드 시간([MOLAP](/studynote/05_database/06_dw_olap_trends/336_molap/) 수시간)과 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 요구를 맞바꾸는 트레이드오프가 핵심 설계 결정이다.

## Ⅰ. 개요 및 필요성

[OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) ([Online Analytical Processing](/studynote/14_data_engineering/05_exam_keywords/211_olap_drill_down_roll_up_surrogate_key/))은 다차원 관점에서 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [Slice](/studynote/05_database/06_dw_olap_trends/331_neuromorphic_ai_db/)·Dice·[Roll-up](/studynote/05_database/06_dw_olap_trends/330_olap_rollup_drilldown/)·Drill-down하는 분석 기법이다.
수억 건의 거래 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 매번 집계하면 수십 분이 걸리지만, 큐브(Cube)에 사전 집계해두면 1초 이내로 조회 가능하다.

주요 유형:
- [MOLAP](/studynote/05_database/06_dw_olap_trends/336_molap/) ([Multidimensional OLAP](/studynote/05_database/06_dw_olap_trends/336_molap/)): [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 전용 다차원 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 구조로 저장
- [ROLAP](/studynote/05_database/06_dw_olap_trends/337_rolap/) ([Relational OLAP](/studynote/05_database/06_dw_olap_trends/337_rolap/)): [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB([스타 스키마](/studynote/05_database/06_dw_olap_trends/334_star_schema/)) 위에서 동적 집계
- [HOLAP](/studynote/05_database/06_dw_olap_trends/338_holap/) ([Hybrid OLAP](/studynote/05_database/06_dw_olap_trends/338_holap/)): 요약 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [MOLAP](/studynote/05_database/06_dw_olap_trends/336_molap/), 세부 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 [ROLAP](/studynote/05_database/06_dw_olap_trends/337_rolap/)

MDX (Multidimensional Expressions)는 [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) 큐브 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어다.

📢 **섹션 요약 비유**: [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) 큐브는 미리 잘라 놓은 요리 재료 통이다. 주문이 들어오면 즉시 꺼내 담기만 하면 되므로 응답이 [초고속](/studynote/06_ict_convergence/02_iot_mobility/148_5g_embb_urllc_mmtc/)이다.

## Ⅱ. 아키텍처 및 핵심 원리

### [MOLAP](/studynote/05_database/06_dw_olap_trends/336_molap/) vs [ROLAP](/studynote/05_database/06_dw_olap_trends/337_rolap/) vs [HOLAP](/studynote/05_database/06_dw_olap_trends/338_holap/) 비교

| 항목 | [MOLAP](/studynote/05_database/06_dw_olap_trends/336_molap/) | [ROLAP](/studynote/05_database/06_dw_olap_trends/337_rolap/) | [HOLAP](/studynote/05_database/06_dw_olap_trends/338_holap/) |
|:---|:---|:---|:---|
| 저장 방식 | 다차원 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) (전용 엔진) | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB [스타 스키마](/studynote/05_database/06_dw_olap_trends/334_star_schema/) | 혼합 |
| [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 속도 | <1초 (사전 집계) | 5~30초 (온디맨드) | 중간 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 | 큐브 빌드 주기 (수시간) | 실시간 가능 | 중간 |
| 스토리지 | 크다 (원본의 2~5배) | 원본 [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 동일 | 중간 |
| 확장성 | 차원 수 제한 (~20개) | 무제한 | 중간 |
| 도구 | SSAS [MOLAP](/studynote/05_database/06_dw_olap_trends/336_molap/), Essbase | SSAS [ROLAP](/studynote/05_database/06_dw_olap_trends/337_rolap/), Mondrian | SSAS [HOLAP](/studynote/05_database/06_dw_olap_trends/338_holap/) |

### [ASCII](/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램: [MOLAP](/studynote/05_database/06_dw_olap_trends/336_molap/) 3차원 큐브 구조

```
  +------------------------------------------------+
  |           MOLAP Cube: Sales                    |
  |                                                |
  |         제품 차원 (Product)                     |
  |        +-----+-----+-----+                    |
  |       /|     |     |     |/                   |
  |      / +-----+-----+-----+                    |
  |  시간 / -------------------> 지역 차원 (Region)  |
  |  차원 +-----+-----+-----+                      |
  | (Time)|2022 |2023 |2024 |                      |
  |       +-----+-----+-----+                      |
  |       | 서울 | 부산 | 대구 |  각 셀 = 사전 집계값 |
  |       +-----+-----+-----+  (합계, 평균, 최대 등) |
  |       | ... | ... | ... |                      |
  |       +-----+-----+-----+                      |
  |  큐브 빌드: 야간 배치 (수시간)                   |
  |  조회 응답: <1초 (사전 집계 인덱스)              |
  +------------------------------------------------+
```

### [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)

| [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) | 방법 | 효과 |
|:---|:---|:---|
| 시간 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/) | 연도별 큐브 분리 | 빌드 시간 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/), 부분 갱신 |
| 증분 빌드 | 변경 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 재빌드 | 90% 빌드 시간 단축 |
| 집계 최소화 | 자주 쓰는 조합만 | 스토리지 50% 절감 |

📢 **섹션 요약 비유**: 큐브 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)은 도서관 서가를 연도별로 나누는 것이다. 최근 책만 꺼내려면 최근 서가만 뒤지면 된다.

## Ⅲ. 비교 및 연결

### 큐브 빌드 시간 최적화

| 최적화 방법 | 효과 | 주의 |
|:---|:---|:---|
| 증분 빌드 (Incremental) | 전체 대비 90% 시간 단축 | 팩트 변경 시 무효화 |
| [병렬](/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 빌드 | CPU 코어 활용 극대화 | 메모리 압박 |
| 집계 설계 최소화 | 스토리지·빌드 시간 감소 | [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 속도 일부 저하 |

📢 **섹션 요약 비유**: 큐브 빌드는 시험 전 정리된 요약 노트 만들기다. 노트가 완성되면 시험은 빠르지만, 노트 만드는 데 밤새 걸린다.

## Ⅳ. 실무 적용 및 기술사 판단

### [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) 설계 [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

- [ ] 조회 응답 [SLA](/studynote/12_it_management/02_itsm_itil/869_sla/): <1초면 [MOLAP](/studynote/05_database/06_dw_olap_trends/336_molap/), 5~30초 허용이면 [ROLAP](/studynote/05_database/06_dw_olap_trends/337_rolap/) 검토
- [ ] [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 요구: 실시간이면 [ROLAP](/studynote/05_database/06_dw_olap_trends/337_rolap/) 또는 [HTAP](/studynote/05_database/05_distributed_nosql_newsql/294_oltp_vs_olap/) 검토
- [ ] 차원 수: 20개 초과 시 [ROLAP](/studynote/05_database/06_dw_olap_trends/337_rolap/) 권장
- [ ] 스토리지 예산: MOLAP은 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 2~5배 스토리지 필요
- [ ] [스타 스키마](/studynote/05_database/06_dw_olap_trends/334_star_schema/)(팩트·[차원 테이블](/studynote/07_enterprise_systems/05_data_bi/273_dimension_table_analysis_perspective/)) [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 선행 필수

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

| [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/) | 문제 | 해결 방법 |
|:---|:---|:---|
| 모든 차원 조합 사전 집계 | 스토리지 폭발 | 자주 쓰는 조합만 선택적 집계 |
| 세분화된 시간 차원 과다 | 희소 큐브, 빌드 시간 급증 | 일·월·분기·연 4레벨로 제한 |

📢 **섹션 요약 비유**: 모든 집계를 미리 계산하는 건 모든 음식 레시피를 미리 만들어 냉동해두는 것이다. 냉동실이 넘친다.

## Ⅴ. 기대효과 및 결론

| 항목 | [Raw](/studynote/01_computer_architecture/05_control_unit_pipelining/225_raw/) SQL | [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) 큐브 도입 |
|:---|:---|:---|
| [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) | 5~30분 (수억 행 집계) | <1초 ([MOLAP](/studynote/05_database/06_dw_olap_trends/336_molap/)) |
| 경영진 셀프서비스 | 불가 (IT 의존) | 드래그앤드롭 분석 |
| BI 도구 연동 | 제한적 | Excel, [Power BI](/studynote/16_bigdata/08_visualization/165_power_bi/) 직접 연결 |

📢 **섹션 요약 비유**: 큐브 도입 결정은 사전에 재료를 손질해 두느냐 vs 주문받고 바로 손질하느냐의 선택이다. 주문량이 많으면 미리 손질하는 게 낫지만, 신선도가 중요하다면 즉석 요리가 낫다.

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [MOLAP](/studynote/05_database/06_dw_olap_trends/336_molap/) | 유형 | 다차원 [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 사전 집계 |
| [ROLAP](/studynote/05_database/06_dw_olap_trends/337_rolap/) | 유형 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)형 DB 온디맨드 집계 |
| [HOLAP](/studynote/05_database/06_dw_olap_trends/338_holap/) | 유형 | 혼합 방식 |
| MDX | [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 언어 | 큐브 조회 전용 언어 |
| Cube [Partition](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) | 최적화 | 증분 빌드로 빌드 시간 단축 |

### 📈 관련 키워드 및 발전 흐름도

```
평면 2D 리포트 한계 - 다차원 분석 필요성
    |
    v
MOLAP - 전용 큐브 스토리지 (빠른 쿼리, 공간 비용)
    |
    v
ROLAP - RDB 기반 스타 스키마 (확장성, 느린 쿼리)
    |
    v
HOLAP - MOLAP+ROLAP 하이브리드 계층화
    |
    v
현대 OLAP (Druid, ClickHouse) - 실시간 집계 진화
```

> **키워드**: [MOLAP](/studynote/05_database/06_dw_olap_trends/336_molap/), [ROLAP](/studynote/05_database/06_dw_olap_trends/337_rolap/), [HOLAP](/studynote/05_database/06_dw_olap_trends/338_holap/), [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) Cube, [Star Schema](/studynote/05_database/05_distributed_nosql_newsql/296_star_schema/), [Snowflake Schema](/studynote/12_it_management/05_security_compliance/955_snowflake_schema/), Drill-Down, ClickHouse

### 👶 어린이를 위한 3줄 비유 설명

1. [OLAP](/studynote/12_it_management/05_security_compliance/316_olap/) 큐브는 미리 잘라 포장해 둔 음식 세트예요. 주문이 오면 바로 꺼내주면 돼요.
2. MOLAP은 모든 세트를 미리 만들어 냉장 보관한 것, ROLAP은 주문 즉시 만드는 것이에요.
3. HOLAP은 자주 팔리는 인기 메뉴는 미리 만들고, 특별 주문만 즉석 요리하는 방식이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 307 / 482

<- **이전**: [306. 데이터 거버넌스 3요소 원칙 조직 프로세스 IT시스템 (Data Governance)](/studynote/07_enterprise_systems/05_data_bi/306_data_governance_3_elements/)
**다음**: [308. AI BI 증강 분석 자동화 (Augmented Analytics)](/studynote/07_enterprise_systems/05_data_bi/308_ai_bi_augmented_analytics/) ->

---
