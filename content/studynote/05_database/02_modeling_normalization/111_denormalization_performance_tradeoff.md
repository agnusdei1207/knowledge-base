---
title: "111. Denormalization Performance Tradeoff"
date: "2026-04-19"
tags:
  - "studynote-database"
weight: 111
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 역정규화(Denormalization)는 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)로 분해한 테이블을 <strong>의도적으로 다시 합치거나 중복 컬럼을 추가</strong>하여, 조인([JOIN](/studynote/05_database/04_transactions_concurrency/521_join/)) 횟수를 줄이고 <strong>읽기(<a href="/studynote/05_database/04_transactions_concurrency/520_select/">SELECT</a>) <a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>을 극적으로 향상</strong>시키는 물리 설계 전략이다.
> 2. **가치**: [3NF](/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)~[BCNF](/studynote/05_database/04_transactions_concurrency/529_bcnf/) [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [무결성](/studynote/09_security/01_intro_principles/003_integrity/)을 보장하지만, 수천만 건 테이블의 3~5중 조인은 DB CPU를 폭발시킨다. 역정규화는 **"정확성을 조금 양보하고 속도를 얻는"** 실무적 타협이다.
> 3. **판단 포인트**: 역정규화는 <strong>읽기 위주(<a href="/studynote/12_it_management/05_security_compliance/316_olap/">OLAP</a>/<a href="/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/">DW</a>)</strong>에서 효과가 크고, <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 위주(<a href="/studynote/05_database/06_dw_olap_trends/327_hint_handoff/">OLTP</a>)</strong>에서는 [갱신 이상](/studynote/05_database/02_modeling_normalization/093_update_anomaly/)([Update Anomaly](/studynote/05_database/02_modeling_normalization/093_update_anomaly/)) 위험이 커지므로 반드시 [트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/)·배치 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 등 [보호](/studynote/02_operating_system/10_security/571_protection_vs_security/) 장치를 병행해야 한다.

---

## Ⅰ. 개요 및 필요성

[정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)의 이상적 세계에서는 "모든 사실을 한 곳에만 저장"하지만, 현실의 수천만 건 주문 테이블에서 고객명을 보여주려면 고객 테이블과 조인해야 한다. 이 조인이 매 [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 호출마다 반복되면 DB가 지친다.

```text
+-------------------------------------------------------+
|      정규화 vs 역정규화 트레이드오프                    |
+-------------------------------------------------------+
|  [정규화 (3NF)]                                       |
|   주문(주문ID, 고객ID, 금액)                           |
|   고객(고객ID, 이름, 주소)                             |
|   -> 고객명 조회 시 JOIN 필요 -> 느림                   |
|   -> 이름 변경 시 고객 테이블 1곳만 수정 -> 무결성 ✅   |
|                                                       |
|  [역정규화]                                           |
|   주문(주문ID, 고객ID, 고객명, 금액) <- 중복 추가      |
|   -> JOIN 없이 바로 조회 -> 빠름 ✅                     |
|   -> 이름 변경 시 주문+고객 둘 다 수정 -> 위험 ⚠️      |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)는 도서관에서 책을 1권만 보관하는 것(깨끗), 역정규화는 자주 보는 책을 교실마다 복사본을 두는 것(빠르지만 수정 시 전부 교체해야 함)이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 역정규화 주요 기법

| 기법 | 설명 | 효과 |
|:---|:---|:---|
| **테이블 병합** | 1:1 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 테이블을 합침 | [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 제거 |
| **중복 컬럼 추가** | 자주 조회하는 컬럼을 복사 | [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 감소 |
| **파생 컬럼 추가** | 합계·건수 등 계산값을 미리 저장 | 집계 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 제거 |
| **테이블 분할 (수평)** | 연도별·지역별로 테이블 분리 | 스캔 범위 축소 |
| **테이블 분할 (수직)** | 자주 쓰는 컬럼과 안 쓰는 컬럼 분리 | I/O 감소 |

### [갱신 이상](/studynote/05_database/02_modeling_normalization/093_update_anomaly/) 방지 장치

역정규화로 중복이 생기면 반드시 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 메커니즘이 필요하다:
1. <strong>DB <a href="/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a></strong>: 원본 변경 시 복사본 자동 갱신.
2. <strong>배치 <a href="/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/">동기화</a></strong>: 야간 배치로 중복 컬럼 일괄 갱신.
3. **애플리케이션 레벨**: 코드에서 양쪽 동시 기록.

- **📢 섹션 요약 비유**: 역정규화는 편의점 냉장고에 복사본(중복 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))을 놓는 것이다. 본사 가격이 바뀌면 전 지점 냉장고 스티커를 다 바꿔야([동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/)) 한다.

---

## Ⅲ. 비교 및 연결

| 비교 | [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) ([3NF](/studynote/05_database/02_modeling_normalization/105_third_normal_form_3nf_transitive/)+) | 역정규화 |
|:---|:---|:---|
| **목표** | [무결성](/studynote/09_security/01_intro_principles/003_integrity/) ([Integrity](/studynote/09_security/01_intro_principles/003_integrity/)) | <strong><a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a> (<a href="/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">Performance</a>)</strong> |
| **중복** | 최소 | 의도적 허용 |
| **읽기** | 느림 ([JOIN](/studynote/05_database/04_transactions_concurrency/521_join/) 다수) | <strong>빠름 (<a href="/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a> 감소)</strong> |
| <strong><a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a></strong> | 빠름 (1곳 수정) | 느림 ([동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 필요) |
| **적합** | [OLTP](/studynote/05_database/06_dw_olap_trends/327_hint_handoff/) (거래) | <strong><a href="/studynote/12_it_management/05_security_compliance/316_olap/">OLAP</a>·<a href="/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/">DW</a> (분석)</strong> |

---

## Ⅳ. 실무 적용 및 기술사 판단

### 역정규화 판단 기준
1. <strong><a href="/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/">쿼리</a> 빈도</strong>: 해당 조인이 초당 1,000회 이상 -> 역정규화 검토.
2. **테이블 크기**: 수천만 건 이상의 대형 테이블 -> 조인 비용 크게 증가.
3. <strong>읽기/<a href="/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/">쓰기</a> 비율</strong>: 읽기 80%+ -> 역정규화 효과 극대화.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- **무분별한 역정규화**: 모든 테이블을 합쳐서 하나의 거대 테이블 -> [갱신 이상](/studynote/05_database/02_modeling_normalization/093_update_anomaly/) 폭발, [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)의 의미 상실.

---

## Ⅴ. 기대효과 및 결론

| 지표 | [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) (조인) | 역정규화 | 개선 |
|:---|:---|:---|:---|
| [SELECT](/studynote/05_database/04_transactions_concurrency/520_select/) [응답 시간](/studynote/01_computer_architecture/03_architecture_basics_performance/138_response_time/) | 200ms (3-way [JOIN](/studynote/05_database/04_transactions_concurrency/521_join/)) | <strong>20ms (<a href="/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a> 0)</strong> | 90% 단축 |
| DB CPU 사용률 | 80% | **30%** | 60% 절감 |
| 갱신 복잡도 | 낮음 | 높음 ([트리거](/studynote/05_database/04_transactions_concurrency/507_acid_properties/) 필요) | 트레이드오프 |

역정규화는 "[정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)를 알고 있는 사람만이 의도적으로 깨뜨릴 수 있는" 고급 설계 기법이며, 반드시 [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/) 후 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 측정 결과에 기반하여 적용해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/">정규화</a> (<a href="/studynote/05_database/02_modeling_normalization/103_first_normal_form_1nf_atomic_value/">1NF</a>~5NF)</strong> | 역정규화의 선행 단계, [무결성 보장](/studynote/05_database/07_exam_summary/442_consistency_integrity/) |
| <strong>조인 (<a href="/studynote/05_database/04_transactions_concurrency/521_join/">JOIN</a>)</strong> | 역정규화가 줄이려는 대상 연산 |
| <strong><a href="/studynote/12_it_management/05_security_compliance/316_olap/">OLAP</a> / <a href="/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/">DW</a></strong> | 역정규화가 가장 효과적인 환경 |
| <strong><a href="/studynote/05_database/04_transactions_concurrency/507_acid_properties/">트리거</a> (Trigger)</strong> | 중복 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) 메커니즘 |
| <strong>Materialized <a href="/studynote/05_database/03_relational_model/151_sql_view_virtual_table/">View</a></strong> | 역정규화의 대안, 뷰를 물리적으로 저장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[정규화 이론 확립 (Codd, 1970s) — 무결성 중심 설계]
    |
    v
[OLTP 성능 이슈 대두 (1990s) — 대용량 조인 병목]
    |
    v
[역정규화 실무 패턴 정립 — 중복 컬럼·파생 컬럼·테이블 병합]
    |
    v
[DW/OLAP Star Schema (2000s) — 분석 환경 전면 역정규화]
    |
    v
[현재: Materialized View + CQRS — 정규화(쓰기)와 역정규화(읽기) 분리]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 도서관([정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/))에 책이 1권만 있으면 깨끗하지만, 빌리려면 **도서관까지 가야 해서** 시간이 오래 걸려요.
2. 역정규화는 자주 보는 책을 <strong>교실마다 복사본</strong>을 두는 거예요. 바로 볼 수 있어서 빨라요!
3. 대신 책 내용이 바뀌면 <strong>모든 복사본</strong>을 다 바꿔야 하는 번거로움이 있답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 111 / 600

<- **이전**: [110. 제5정규형 (5NF / PJ-NF) - 조인 종속성 완전 제거와 정규화 최종 종착점](/studynote/05_database/02_modeling_normalization/110_fifth_normal_form_5nf_pjnf/)
**다음**: [112. 역정규화 개념 (Denormalization Concept) - 물리 설계 단계의 성능 최적화 패턴](/studynote/05_database/02_modeling_normalization/112_denormalization_concept/) ->

---
