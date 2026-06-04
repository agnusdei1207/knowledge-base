---
title: "113. 역정규화 기법 (Denormalization Techniques) - 테이블 병합·분할·중복 컬럼"
date: "2026-04-19"
tags:
  - "studynote-database"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [역정규화](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/) 기법은 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)된 스키마에서 **테이블 병합(Merge)·분할(Split)·중복 컬럼 추가(Redundancy)·파생 컬럼 추가(Derived)** 등의 구체적 물리 설계 패턴을 적용하여 읽기 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 최적화하는 실무 방법론이다.
> 2. **가치**: [역정규화](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/) "개념"을 안다고 실전에서 바로 적용할 수 없다. <strong>어떤 상황에서 어떤 기법을 선택하는가(병합 vs 분할 vs 중복)</strong>의 판단 기준이 기술사 시험과 실무 모두에서 핵심이다.
> 3. **판단 포인트**: [수평 분할](/studynote/05_database/05_distributed_nosql_newsql/268_horizontal_fragmentation/)은 <strong><a href="/studynote/02_operating_system/09_file_system/514_partition_slice_volume/">Partition</a> <a href="/studynote/05_database/02_modeling_normalization/067_db_key_uniqueness_minimality/">Key</a>(연도·지역)</strong>로 스캔 범위를 줄이고, [수직 분할](/studynote/05_database/05_distributed_nosql_newsql/269_vertical_fragmentation/)은 <strong>핫 컬럼과 콜드 컬럼</strong>을 분리하여 I/O를 최적화하며, 파생 컬럼은 <strong>집계 <a href="/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 제거</strong>에 효과적이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    역정규화 5대 기법 한눈에 보기                       |
+-------------------------------------------------------+
|  [1] 테이블 병합: 1:1 관계 테이블 합치기              |
|      사원 + 사원상세 -> 사원통합                       |
|                                                       |
|  [2] 중복 컬럼 추가: FK 참조값을 복사                 |
|      주문(고객ID) + 고객(이름) -> 주문(고객명 복사)    |
|                                                       |
|  [3] 파생 컬럼 추가: 계산값 미리 저장                 |
|      주문상세(수량×단가) -> 주문(총액)                 |
|                                                       |
|  [4] 수평 분할: 행 기준 분리                          |
|      주문(10년치) -> 주문_2024, 주문_2025              |
|                                                       |
|  [5] 수직 분할: 열 기준 분리                          |
|      상품(이름,가격,설명,이미지) ->                    |
|      상품_핫(이름,가격) + 상품_콜드(설명,이미지)      |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [역정규화](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/) 기법은 대형 마트 물류 최적화다. 병합은 인접 매대 통합, [수평 분할](/studynote/05_database/05_distributed_nosql_newsql/268_horizontal_fragmentation/)은 층별 분리, [수직 분할](/studynote/05_database/05_distributed_nosql_newsql/269_vertical_fragmentation/)은 냉장·상온 구역 분리, 중복은 자주 찾는 상품을 여러 매대에 복사 배치.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 기법별 선택 기준

| 기법 | 적용 조건 | 효과 | 부작용 |
|:---|:---|:---|:---|
| **병합** | 1:1 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/), 항상 함께 조회 | [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 제거 | 테이블 비대 |
| **중복 컬럼** | FK 참조값 빈번 조회 | [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 감소 | [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 필요 |
| **파생 컬럼** | SUM/COUNT 집계 빈번 | 집계 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 제거 | 갱신 시 재계산 |
| <strong><a href="/studynote/05_database/05_distributed_nosql_newsql/268_horizontal_fragmentation/">수평 분할</a></strong> | 대용량+시간/지역 기반 조회 | 스캔 범위 축소 | 교차 [파티션](/studynote/02_operating_system/09_file_system/514_partition_slice_volume/) 조인 비용 |
| <strong><a href="/studynote/05_database/05_distributed_nosql_newsql/269_vertical_fragmentation/">수직 분할</a></strong> | 핫/콜드 컬럼 명확 | I/O 감소 | 재조립 [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 필요 |

### [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 메커니즘

| 방식 | 적합 | [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
|:---|:---|:---|
| <strong>DB <a href="/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a></strong> | 실시간 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 필수 | 0 (즉시) |
| **배치 스크립트** | 일정 [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 허용 | 분~시간 |
| **앱 듀얼 라이트** | 코드 레벨 제어 | 0 (즉시) |

- **📢 섹션 요약 비유**: [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)는 자동 분사 소화기(즉시 반응), 배치는 야간 청소([지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 허용), 듀얼 라이트는 수동 소화기(코드에서 직접 처리)이다.

---

## Ⅲ. 비교 및 연결

| 비교 | [수평 분할](/studynote/05_database/05_distributed_nosql_newsql/268_horizontal_fragmentation/) | [수직 분할](/studynote/05_database/05_distributed_nosql_newsql/269_vertical_fragmentation/) |
|:---|:---|:---|
| **기준** | 행(Row) | 열(Column) |
| **효과** | 스캔 범위 축소 | I/O 크기 축소 |
| **적합** | 시간/지역별 대용량 | 핫/콜드 컬럼 분리 |
| **예** | 주문_2024, 주문_2025 | 상품_기본, 상품_상세 |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 기술사 답안 구성
1. <strong>병목 <a href="/studynote/09_security/13_secops_ir_forensics/655_ir_detection_analysis/">식별</a></strong>: "주문 조회 API가 3-way JOIN으로 초당 5,000회 호출, 평균 200ms".
2. **기법 선택**: "중복 컬럼(고객명)을 주문 테이블에 추가하여 [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 제거".
3. <strong><a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a> 설계</strong>: "고객명 변경 시 DB [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)로 주문 테이블의 복사 컬럼을 자동 갱신".
4. **효과 측정**: "[JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 제거 후 [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) 200ms -> 20ms, DB CPU 80% -> 30%".

---

## Ⅴ. 기대효과 및 결론

[역정규화](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/) 기법은 "이론([정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))과 실전([성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/))"의 균형을 맞추는 <strong>DB 설계자의 핵심 역량</strong>이다. 최근 DB 레벨에서는 [파티셔닝](/studynote/05_database/03_relational_model/179_table_partitioning_concept/)([수평 분할](/studynote/05_database/05_distributed_nosql_newsql/268_horizontal_fragmentation/))이 표준 기능으로 내장되어 있고, [CQRS](/studynote/12_it_management/05_security_compliance/306_cqrs/) + Event Sourcing으로 읽기 전용 [역정규화](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/) 뷰를 이벤트 기반으로 자동 생성하는 패턴이 주류다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/05_database/02_modeling_normalization/112_denormalization_concept/">역정규화 개념</a></strong> | 기법의 이론적 배경 |
| <strong><a href="/studynote/05_database/03_relational_model/179_table_partitioning_concept/">파티셔닝</a></strong> | [수평 분할](/studynote/05_database/05_distributed_nosql_newsql/268_horizontal_fragmentation/)의 DB 내장 구현 (Range/Hash/List) |
| <strong>Materialized <a href="/studynote/05_database/03_relational_model/151_sql_view_virtual_table/">View</a></strong> | 파생 컬럼의 자동화 대안 |
| <strong><a href="/studynote/12_it_management/05_security_compliance/306_cqrs/">CQRS</a></strong> | 읽기([역정규화](/studynote/05_database/02_modeling_normalization/111_denormalization_performance_tradeoff/))와 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/)([정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)) 분리 아키텍처 |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a></strong> | 중복 컬럼 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 메커니즘 |

### 📈 관련 키워드 및 발전 흐름도

```text
[역정규화 수동 설계 (1990s) — DBA의 경험 기반 판단]
    |
    v
[파티셔닝 내장 (2000s) — Oracle/MySQL 수평 분할 표준화]
    |
    v
[Materialized View 자동 갱신 — 파생 컬럼 자동화]
    |
    v
[CQRS + Event Sourcing (2010s) — 읽기 뷰 이벤트 기반 생성]
    |
    v
[현재: NewSQL Auto-sharding — 분산 DB가 분할을 자동 관리]
```

### 👶 어린이를 위한 3줄 비유 설명
1. <strong>병합</strong>은 방 2개를 벽을 허물어 1개로 만드는 거예요 (찾으러 안 다녀도 됨).
2. <strong>분할</strong>은 큰 옷장을 여름옷·겨울옷 서랍으로 나누는 거예요 (찾기 빨라짐).
3. <strong>중복</strong>은 리모컨을 거실·안방에 1개씩 두는 거예요 (가까이서 바로 잡지만, 건전지를 2개 관리해야 해요)!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 113 / 600

<- **이전**: [112. 역정규화 개념 (Denormalization Concept) - 물리 설계 단계의 성능 최적화 패턴](/studynote/05_database/02_modeling_normalization/112_denormalization_concept/)
**다음**: [114. 데이터베이스 설계 단계 (Database Design Phases) - 개념·논리·물리 3단계 체계](/studynote/05_database/02_modeling_normalization/114_database_design_phases/) ->

---
