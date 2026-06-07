---
title: "Data Quality Dimensions"
date: "2026-04-21"
tags:
  - "studynote-bigdata"
weight: 201
---
## 핵심 인사이트 (3줄 요약)

- **본질**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질([Data Quality](/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/))은 완전성(Completeness)·[정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)(Accuracy)·[일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/))·적시성(Timeliness)·유일성(Uniqueness)·유효성(Validity)의 6차원으로 측정되며, 각 차원은 서로 다른 [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 유형을 포착한다.
- **가치**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 저하는 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 모델 오작동, 잘못된 경영 의사결정, 규제 위반으로 이어지며 IBM 연구에 따르면 미국 기업에 연간 3.1조 달러의 경제적 손실을 유발한다.
- **판단 포인트**: 단순히 "NULL이 없다"는 완전성만 보는 것은 불충분하며, 6차원을 모두 측정해야 진정한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 수준을 파악할 수 있다는 점이 기술사 답안의 차별점이다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질의 중요성

"Garbage In, Garbage Out" — [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 분석과 AI의 근본 원칙이다. 아무리 정교한 [머신러닝](/studynote/10_ai/03_llm_nlp/241_machine_learning_basics/) [알고리즘](/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/)도 품질 낮은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로는 신뢰할 수 없는 결과를 낸다.

주요 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 문제 사례:
- **의료**: 잘못된 환자 정보 -> 오진·약물 오처방
- **금융**: 중복 거래 레코드 -> 과장된 매출 보고
- **물류**: 부정확한 주소 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) -> 배송 실패율 증가
- **ML**: 편향된 학습 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) -> 차별적 모델 출력

### 1.2 [DAMA](/studynote/03_network/02_multiplexing_multiple_access/117_dama/) 6차원 개요

[DAMA](/studynote/03_network/02_multiplexing_multiple_access/117_dama/) ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Management](/studynote/12_it_management/05_security_compliance/1013_management/) Association) DMBOK이 정의한 6대 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 차원:

| 차원 | 영문 | 핵심 질문 |
|:---|:---|:---|
| 완전성 | Completeness | 필요한 값이 모두 있는가? |
| [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/) | Accuracy | 실세계 사실과 일치하는가? |
| [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | [Consistency](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 서로 다른 시스템에서 동일한가? |
| 적시성 | Timeliness | 필요한 시점에 사용 가능한가? |
| 유일성 | Uniqueness | 중복이 없는가? |
| 유효성 | Validity | 정해진 형식·규칙을 따르는가? |

**📢 섹션 요약 비유**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 6차원은 <strong>식당 음식 평가 기준</strong>과 같다. 맛([정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)), 양(완전성), 신선도(적시성), 위생(유효성), 메뉴 [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)([일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)), 중복 주문 없음(유일성) — 이 중 하나라도 빠지면 좋은 식당이 아니다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 6차원 상세 설명

```
+--------------------------------------------------------------+
|                  데이터 품질 6차원                            |
|                                                              |
|  +--------------+  완전성(Completeness)                      |
|  | NULL 비율    |  · 필수 항목 채움 비율 = 채워진 값/전체 × 100|
|  | 측정         |  · 목표: 핵심 필드 99.9% 이상              |
|  +--------------+                                            |
|  +--------------+  정확성(Accuracy)                          |
|  | 외부 기준    |  · 실세계 정보와 일치 여부                  |
|  | 비교         |  · 검증: 공공 DB 대조, 현장 확인 샘플링     |
|  +--------------+                                            |
|  +--------------+  일관성(Consistency)                       |
|  | 시스템 간    |  · 동일 속성이 다른 시스템 간 일치           |
|  | 비교         |  · 예: CRM 고객 나이 ≠ DW 고객 나이 -> 불일치|
|  +--------------+                                            |
|  +--------------+  적시성(Timeliness)                        |
|  | SLA 기준     |  · 데이터가 사용 가능한 시점의 최신성        |
|  | 측정         |  · 배치: 매일 06:00 갱신 SLA              |
|  +--------------+                                            |
|  +--------------+  유일성(Uniqueness)                        |
|  | 중복 탐지    |  · 동일 엔티티의 중복 레코드 없음            |
|  | 알고리즘     |  · 중복률 = 중복 레코드 수/전체 레코드 수    |
|  +--------------+                                            |
|  +--------------+  유효성(Validity)                          |
|  | 규칙 검사    |  · 형식·도메인·참조 무결성 준수             |
|  | 엔진         |  · 예: 날짜 형식, 코드 목록, FK 무결성      |
|  +--------------+                                            |
+--------------------------------------------------------------+
```

### 2.2 품질 점수 계산

<strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질 종합 점수 (DQS, <a href="/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/">Data Quality</a> Score)</strong>:

```
DQS = (W1×Completeness + W2×Accuracy + W3×Consistency
       + W4×Timeliness + W5×Uniqueness + W6×Validity) / ΣWi

여기서 Wi는 비즈니스 중요도에 따른 가중치
```

**실무 예시**: 고객 [마스터 데이터](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 품질 측정

| 차원 | 점수 | [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/) | 가중 점수 |
|:---|:---:|:---:|:---:|
| 완전성 | 98.5% | 0.25 | 24.6 |
| [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/) | 95.2% | 0.30 | 28.6 |
| [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | 92.1% | 0.20 | 18.4 |
| 적시성 | 99.0% | 0.[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | 9.9 |
| 유일성 | 97.8% | 0.[10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/) | 9.8 |
| 유효성 | 96.3% | 0.05 | 4.8 |
| **종합 DQS** | | | **96.1%** |

**📢 섹션 요약 비유**: 품질 점수는 <strong>학교 성적표</strong>와 같다. 수학만 100점(완전성만 완벽)이고 나머지가 엉망이면 진학에 실패한다. 종합 점수가 중요하다.

---

## Ⅲ. 비교 및 연결

### 3.1 차원별 대표 문제와 원인

| 차원 | 대표 문제 | 주요 원인 |
|:---|:---|:---|
| 완전성 | 고객 이메일 30% NULL | 필수 [입력 검증](/studynote/09_security/uncategorized/1034_input_validation/) 미적용, 레거시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 마이그레이션 |
| [정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/) | 주소가 실제와 다름 | 입력 오류, 이사 후 업데이트 미실시 |
| [일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) | [CRM](/studynote/07_enterprise_systems/02_erp_systems/107_crm_customer_relationship_management/) vs [DW](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) 고객 수 불일치 | [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) 오류, 실시간 [동기화](/studynote/02_operating_system/03_cpu_scheduling/212_synchronization_mechanisms/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
| 적시성 | 전날 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 오늘 의사결정 | [배치 처리](/studynote/13_cloud_architecture/05_data_engineering/228_batch_processing_hadoop_spark/) [지연](/studynote/03_network/01_data_communication/015_지연_데이터_관점/), [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 오류 |
| 유일성 | 동일 고객 레코드 3개 | 채널별 독립 입력, [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 부재 |
| 유효성 | 나이 필드에 999 입력 | 입력 유효성 검사 미적용 |

### 3.2 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 vs 유사 개념

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) |
|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질(DQ) vs [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) | 거버넌스의 목표 중 하나가 DQ 확보 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 vs [데이터 정제](/studynote/07_enterprise_systems/05_data_bi/266_data_cleansing/)(Cleansing) | 정제는 DQ 향상을 위한 활동 |
| DQ 차원 vs DQ 규칙 | 차원은 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계, 규칙은 세부 검사 기준 |

**📢 섹션 요약 비유**: 6차원과 실제 문제의 [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 <strong>건강검진 항목</strong>과 같다. 혈압([정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)), 체중(완전성), 혈당(유효성) 등 각 항목이 다른 건강 위험을 측정하듯, 각 차원은 다른 유형의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위험을 잡아낸다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인에서의 DQ 검사

```
[소스 데이터 추출]
         |
         v
[DQ 검사 1: 완전성 + 유효성 검사] --실패---> [격리(Quarantine) + 알림]
         |통과
         v
[데이터 변환(Transformation)]
         |
         v
[DQ 검사 2: 일관성 + 유일성 검사] --실패---> [오류 로그 + 수동 검토 큐]
         |통과
         v
[목적 시스템 로드]
         |
         v
[DQ 검사 3: 적시성 + 정확성 샘플링] --실패---> [대시보드 경보]
```

**"Fail Fast" 원칙**: 품질 문제는 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 최대한 앞단에서 잡아야 수정 비용 최소화.

### 4.2 차원별 측정 [쿼리](/studynote/10_ai/04_ai_ops_ethics/298_qkv_attention/) 예시 (SQL)

```sql
-- 완전성 측정
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) AS null_email,
    ROUND(100.0 * SUM(CASE WHEN email IS NOT NULL THEN 1 ELSE 0 END)
          / COUNT(*), 2) AS completeness_pct
FROM customers;

-- 유일성 측정
SELECT
    COUNT(*) AS total,
    COUNT(DISTINCT customer_id) AS unique_ids,
    COUNT(*) - COUNT(DISTINCT customer_id) AS duplicates
FROM customers;
```

**📢 섹션 요약 비유**: [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인의 DQ 검사는 <strong>공장 품질 검사 라인</strong>과 같다. 불량품을 최대한 공정 [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)에 걸러야 완성품 폐기 비용을 줄일 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 향상 기대효과

| 효과 | 정량적 기대치 |
|:---|:---|
| [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 모델 정확도 | 품질 개선 [10](/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)% -> 모델 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 5~15% 향상 |
| 운영 효율 | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수정 재작업 비용 30~50% 절감 |
| 규제 준수 | [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 오류 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 위반 위험 제거 |
| 의사결정 [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) | "이 숫자를 믿을 수 있나?" 토론 시간 제거 |

### 5.2 결론

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 6차원은 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 얼마나 좋은가"를 다각도에서 측정하는 <strong>표준 언어</strong>다. 조직마다 비즈니스 우선순위에 따라 [가중치](/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)를 다르게 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/)하되, 모든 차원을 지속적으로 측정하고 개선하는 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질 관리 체계(DQM, <a href="/studynote/13_cloud_architecture/05_data_engineering/270_data_quality_great_expectations/">Data Quality</a> <a href="/studynote/12_it_management/05_security_compliance/1013_management/">Management</a>)</strong>를 구축해야 한다.

**📢 섹션 요약 비유**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 관리는 <strong>지속적인 운동 습관</strong>과 같다. 한 번 좋아진다고 끝이 아니라, 꾸준히 측정하고 관리해야 오래 건강(품질)을 유지할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [DAMA](/studynote/03_network/02_multiplexing_multiple_access/117_dama/) DMBOK | 표준 출처 | 6차원 품질 프레임워크 정의 |
| Great Expectations | 측정 도구 | 품질 기대값 정의·[검증](/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) 자동화 |
| AWS Deequ | 측정 도구 | Spark 기반 대용량 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 검사 |
| [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) | 연계 기술 | 유일성·[일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 확보를 위한 [마스터 데이터 관리](/studynote/12_it_management/01_governance_strategy/051_mdm_master_data_management/) |
| [ETL](/studynote/12_it_management/05_security_compliance/215_etl_vs_elt_pipeline/) [Pipeline](/studynote/12_it_management/02_itsm_itil/082_pipeline/) | 적용 위치 | DQ 검사가 삽입되는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 처리 [파이프](/studynote/02_operating_system/02_process_thread/123_pipe/)라인 |
| [DataOps](/studynote/12_it_management/05_security_compliance/965_dataops/) | 방법론 연계 | DQ 검사를 [CI](/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD에 통합한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 운영 방식 |
| Completeness | 6차원 중 하나 | 결측값 없는 완전한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 수집 (Data Ingestion) — 원천 시스템에서 원시 데이터 유입]
    |
    v
[데이터 품질 진단 (DQ Assessment) — 완전성·정확성·일관성·적시성 측정]
    |
    v
[데이터 클렌징 (Data Cleansing) — 결측·중복·오류 데이터 처리]
    |
    v
[마스터 데이터 관리 (MDM — Master Data Management) — 핵심 데이터 단일 진실 공급원 확보]
    |
    v
[데이터 거버넌스 (Data Governance) — 지속적 품질 측정·정책·책임 체계 운영]
```

이 흐름은 원시 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 수집에서 품질 진단·클렌징을 거쳐 [마스터 데이터 관리](/studynote/12_it_management/01_governance_strategy/051_mdm_master_data_management/)와 거버넌스로 이어지는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 관리 체계를 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 6차원은 숙제 검사표와 같아 — 빠진 게 없는지(완전성), 맞는지([정확성](/studynote/16_bigdata/01_intro/002_bigdata_5v/)), 예쁘게 썼는지(유효성), 제시간에 냈는지(적시성), 똑같은 답을 두 번 쓰지 않았는지(유일성), 모든 책에서 같은 답이 나오는지([일관성](/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)).
2. 이 중 하나라도 통과 못 하면 선생님(시스템)이 그 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 믿지 못해서 틀린 결정을 내릴 수 있어.
3. "쓰레기를 넣으면 쓰레기가 나온다(Garbage In, Garbage Out)"는 말처럼, 나쁜 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 만든 AI는 나쁜 답변을 내놔.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 201 / 262

<- **이전**: [194. 데이터 소유자 (Data Owner) — 비즈니스 책임자와 접근 승인](/studynote/16_bigdata/10_governance/200_data_owner/)
**다음**: [196. 데이터 품질 관리 도구 (Data Quality Tools) — Great Expectations/Deequ/Soda Core](/studynote/16_bigdata/10_governance/202_data_quality_tools/) ->

---
