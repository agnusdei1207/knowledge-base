---
title: 196. 데이터 품질 관리 도구 (Data Quality Tools) — Great Expectations/Deequ/Soda Core
date: '2026-04-21'
tags:
- studynote-bigdata
---

## 핵심 인사이트 (3줄 요약)

- **본질**: Great Expectations(Python), AWS Deequ(Spark), Soda Core(YAML) 세 도구는 각각 다른 기술 [[057_stack|스택]]에 최적화된 [[191_oss_license_compliance|오픈소스]] [[001_dikw_pyramid|데이터]] 품질(DQ) 자동화 도구로, [[324_dataops|DataOps]] [[123_pipe|파이프]]라인에 "품질 게이트"를 삽입한다.
- **가치**: [[090_configuration_item|CI]]/CD ([[019_continuous_integration|Continuous Integration]]/[[164_continuous_delivery|Continuous Delivery]]) [[123_pipe|파이프]]라인에 DQ 체크를 통합함으로써 품질 문제를 프로덕션 적재 전에 조기 감지·차단하는 자동화된 방어선을 구축한다.
- **판단 포인트**: 기술 [[057_stack|스택]](Python [[645_data_pipeline_acceleration|데이터 파이프라인]] vs Spark 대규모 처리 vs YAML 선언형 접근)과 팀 역량에 따라 도구를 선택하며, 상용 [[090_service_kubernetes_network_load_balancing|서비스]] Monte Carlo는 ML [[123_pipe|파이프]]라인 이상 감지에 특화된다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]] 품질 관리 도구([[270_data_quality_great_expectations|Data Quality]] Tools)는 [[645_data_pipeline_acceleration|데이터 파이프라인]] 내에서 **자동화된 품질 검사·[[229_monitor|모니터]]링·리포팅**을 수행하는 소프트웨어다. 수동 SQL [[298_qkv_attention|쿼리]]로 품질을 [[396_validation|확인]]하는 방식은 확장성이 없고, 새로운 [[001_dikw_pyramid|데이터]] 소스 추가 시마다 검사 스크립트를 재작성해야 하는 문제가 있다.

### DQ 도구가 필요한 이유

- **수동 검사의 한계**: 수백 개의 테이블·수천 개의 컬럼을 매일 수동으로 [[396_validation|확인]] 불가
- **[[123_pipe|파이프]]라인 통합 필요**: Airflow·dbt·Spark [[123_pipe|파이프]]라인에 품질 게이트를 코드로 정의
- **표준화**: 팀별로 다른 품질 검사 방식을 하나의 프레임워크로 통일
- **문서화**: 품질 기준이 코드로 명시되어 자동으로 최신 문서 [[087_process_state_transition|생성]]

**📢 섹션 요약 비유**: DQ 도구는 **자동화된 품질 검사 로봇**이다. 공장 생산 라인에서 사람이 일일이 제품을 검사하던 것을 자동화 센서와 로봇이 대체하듯, DQ 도구는 [[001_dikw_pyramid|데이터]] 품질 검사를 자동화한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 3대 DQ 도구 비교

```
┌────────────────────────────────────────────────────────────────┐
│                  데이터 품질 도구 3종 비교                      │
├──────────────────┬─────────────────────┬───────────────────────┤
│ Great Expectations│    AWS Deequ        │     Soda Core         │
├──────────────────┼─────────────────────┼───────────────────────┤
│ 언어: Python     │ 언어: Scala/Python  │ 언어: YAML (SodaCL)   │
│ 실행: Pandas/    │ 실행: Apache Spark  │ 실행: 20+ 데이터소스  │
│       SQLAlchemy │ (분산처리)          │  커넥터               │
│ 접근: 코드 정의  │ 접근: 제약 검증     │ 접근: 선언형 YAML     │
│ 강점: 표현력,    │ 강점: 대규모 데이터,│ 강점: 비기술자 친화,  │
│  풍부한 기대값   │  Spark 네이티브     │  클라우드 통합        │
│ 출력: Data Docs  │ 출력: 메트릭 저장소 │ 출력: Soda Cloud 대시 │
│  (HTML 문서)     │  (S3/JDBC)          │  보드                 │
│ 통합: Airflow,   │ 통합: EMR, Databricks│통합: dbt, Airflow,    │
│  dbt, Prefect    │  Glue               │  GitHub Actions       │
└──────────────────┴─────────────────────┴───────────────────────┘
```

### Great Expectations 핵심 개념

```python
# Expectation Suite 정의 예시
import great_expectations as ge

context = ge.get_context()
suite = context.create_expectation_suite("customer_data_suite")

# Expectation 정의
validator.expect_column_values_to_not_be_null("email")
validator.expect_column_values_to_match_regex(
    "phone", r"^\d{3}-\d{4}-\d{4}$"
)
validator.expect_column_values_to_be_between(
    "age", min_value=0, max_value=150
)
validator.expect_column_values_to_be_unique("customer_id")
```

- **DataContext**: Great Expectations 프로젝트의 최상위 [[033_context|컨텍스트]] — [[009_config|설정]]·[[001_dikw_pyramid|데이터]]소스·스위트 관리
- **Expectation Suite**: 특정 [[001_dikw_pyramid|데이터]]셋에 대한 품질 규칙 모음
- **Checkpoint**: [[001_dikw_pyramid|데이터]]소스 + Expectation Suite 조합을 실행하는 유닛
- **[[001_dikw_pyramid|Data]] Docs**: 체크포인트 실행 결과를 자동 [[087_process_state_transition|생성]]하는 HTML 품질 문서

### AWS Deequ 핵심 개념

Deequ는 [[206_spark_inmemory_rdd_lazy_evaluation_lineage|Apache Spark]] 위에서 동작하는 **대규모 [[001_dikw_pyramid|데이터]]셋 제약 [[395_verification_process_review|검증]] [[336_library_vs_framework|라이브러리]]**다. 수백억 레코드를 Spark [[136_variance|분산]] 처리로 한 번의 패스에 검사한다.

```scala
// Deequ Constraint Verification 예시 (Scala)
val verificationResult = VerificationSuite()
  .onData(dataset)
  .addCheck(
    Check(CheckLevel.Error, "customer_check")
      .hasSize(_ >= 1000)
      .isComplete("email")
      .isUnique("customer_id")
      .satisfies("age >= 0 AND age <= 150", "age range")
  )
  .run()
```

**📢 섹션 요약 비유**: Great Expectations는 **Python 개발자의 [[397_unit_test|단위 테스트]]([[397_unit_test|Unit Test]])**이고, Deequ는 **공장 전체 생산량을 한 번에 검사하는 대형 품질 기계**다. 소규모는 Great Expectations, 수십억 레코드 Spark 환경은 Deequ가 적합하다.

---

## Ⅲ. 비교 및 연결

### 도구 선택 가이드

| 상황 | 추천 도구 | 이유 |
|:---|:---|:---|
| Python [[645_data_pipeline_acceleration|데이터 파이프라인]](Airflow+Pandas) | Great Expectations | Python 네이티브, 풍부한 Expectation |
| Spark 기반 대규모 처리(EMR, [[074_photon_engine|Databricks]]) | AWS Deequ | Spark 네이티브, 대규모 [[282_performance_tactics|성능]] |
| 비기술자 [[001_dikw_pyramid|데이터]] 분석가 팀 | Soda Core | YAML 선언형, 비코딩 친화 |
| 엔터프라이즈 ML [[123_pipe|파이프]]라인 이상 감지 | Monte Carlo | [[190_ai_llm_requirements_specification|AI]] 기반 자동 이상 감지 |
| dbt 사용 환경 | dbt Tests + Soda | dbt 네이티브 테스트 + Soda 연동 |

### [[324_dataops|DataOps]] [[123_pipe|파이프]]라인에서의 위치

```
[데이터 소스]
     │
     ▼ ← Great Expectations (원본 데이터 품질 체크)
[Extract]
     │
     ▼ ← Deequ (대규모 변환 중 제약 검증)
[Transform]
     │
     ▼ ← Soda Core (적재 후 목적지 데이터 검증)
[Load/Publish]
     │
     ▼ ← Monte Carlo (프로덕션 데이터 이상 감지 상시 모니터링)
[Analytics/ML]
```

**📢 섹션 요약 비유**: 세 도구의 [[083_relationship_in_er_model|관계]]는 **공항 보안 검색대** 같다. 탑승권 [[396_validation|확인]](추출 전 체크), 수하물 X-ray(변환 중 체크), 탑승 게이트(적재 후 체크) — 여러 단계 방어선이 있어야 문제가 최종 목적지까지 전달되지 않는다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[090_configuration_item|CI]]/CD 통합 패턴 ([[324_dataops|DataOps]])

```yaml
# GitHub Actions에서 Soda Core 실행 예시
name: Data Quality Check
on: [push]
jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Soda Scan
        run: |
          pip install soda-core-bigquery
          soda scan -d bigquery -c configuration.yml checks.yml
```

Soda Core의 **SodaCL (Soda Checks Language)**:
```yaml
# checks.yml
checks for customer_data:
  - missing_count(email) = 0:
      name: 이메일 결측값 없음
  - duplicate_count(customer_id) = 0:
      name: 고객 ID 유일성
  - invalid_count(age) = 0:
      valid range: [0, 150]
      name: 나이 유효 범위
```

### Monte Carlo: ML [[123_pipe|파이프]]라인 [[001_dikw_pyramid|데이터]] 관측성

Monte Carlo는 통계 기반 **이상 감지([[111_anomaly_detection|Anomaly Detection]])**를 통해 품질 규칙을 명시적으로 정의하지 않아도 자동으로 이상을 감지한다:
- 레코드 수 급격한 변화 감지
- 컬럼 null 비율 갑작스러운 증가
- 수치형 컬럼 분포 변화 (Mean/StdDev 이상)
- 적재 [[015_지연_데이터_관점|지연]](Freshness) 알림

**📢 섹션 요약 비유**: Great Expectations/Deequ/Soda가 **정해진 규칙을 [[396_validation|확인]]하는 [[435_checklist_based_testing|체크리스트]]**라면, Monte Carlo는 **이상한 낌새를 자동으로 감지하는 [[190_ai_llm_requirements_specification|AI]] 경비원**이다.

---

## Ⅴ. 기대효과 및 결론

### DQ 도구 도입 효과

| 항목 | Before | After |
|:---|:---|:---|
| 품질 이슈 감지 | 사용자 리포트 후 발견 (수일 [[015_지연_데이터_관점|지연]]) | [[123_pipe|파이프]]라인 실행 시 즉시 감지 |
| 품질 문서 | 수동 작성, 항상 오래됨 | [[001_dikw_pyramid|Data]] Docs 자동 [[087_process_state_transition|생성]], 항상 최신 |
| 새 [[001_dikw_pyramid|데이터]]소스 온보딩 | 수주 소요 | 템플릿 기반 수일 내 온보딩 |
| 규정 준수 증거 | 수동 수집 | 자동 리포트 [[087_process_state_transition|생성]] |

### 결론

DQ 도구는 **[[052_data_governance_framework|데이터 거버넌스]]를 자동화하는 실행 엔진**이다. [[164_policy|정책]]과 표준이 서류상 존재하는 거버넌스에서 코드로 구현된 거버넌스로 전환시키는 핵심 기술이다. 기술 [[057_stack|스택]]에 맞는 도구를 선택하고, [[324_dataops|DataOps]] 철학에 따라 [[090_configuration_item|CI]]/CD [[123_pipe|파이프]]라인에 통합하는 것이 현대 [[001_dikw_pyramid|데이터]] 엔지니어링의 베스트 프랙티스다.

**📢 섹션 요약 비유**: DQ 도구가 없는 [[001_dikw_pyramid|데이터]] 팀은 **속도 계기판 없이 운전하는 자동차**와 같다. 얼마나 빠른지(품질이 얼마나 좋은지) 알 수 없어 위험한 속도(저품질 [[001_dikw_pyramid|데이터]])로 달리고 있어도 모른다.

---

### 📌 관련 개념 맵

| 개념 | [[083_relationship_in_er_model|관계]] | 설명 |
|:---|:---|:---|
| Great Expectations | 핵심 도구 | Python 기반 Expectation Suite DQ 자동화 |
| AWS Deequ | 핵심 도구 | Spark 네이티브 대규모 제약 [[395_verification_process_review|검증]] |
| Soda Core | 핵심 도구 | YAML SodaCL 선언형 DQ 체크 |
| Monte Carlo | 상용 이상 감지 | ML 기반 자동 [[001_dikw_pyramid|데이터]] 이상 감지 [[090_service_kubernetes_network_load_balancing|서비스]] |
| [[324_dataops|DataOps]] | 연관 방법론 | DQ 도구를 [[090_configuration_item|CI]]/CD에 통합하는 [[001_dikw_pyramid|데이터]] 운영 방식 |
| [[168_airflow_dag_pipeline_scheduling|Apache Airflow]] | 통합 오케스트레이터 | DQ 체크를 워크플로우에 삽입 |
| dbt | 통합 변환 도구 | dbt Test + Soda 조합으로 변환 품질 보장 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 프로파일링 (Data Profiling) — 현황 파악]
    │
    ▼
[데이터 정제 (Data Cleansing) — 오류 수정]
    │
    ▼
[데이터 품질 규칙 (Data Quality Rule) — 자동 검증]
    │
    ▼
[데이터 관측 가능성 (Data Observability) — 실시간 모니터링]
    │
    ▼
[데이터 품질 SLA (Data Quality SLA) — 비즈니스 계약]
```

이 흐름은 [[001_dikw_pyramid|데이터]]를 먼저 [[613_profiling_gprof|프로파일링]]해 상태를 파악하고, 정제·규칙·[[111_observability_metrics_logs_traces|관측 가능성]]으로 관리한 뒤 품질 SLA로 비즈니스 약속까지 연결하는 과정을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

- Great Expectations는 **[[435_checklist_based_testing|체크리스트]]를 자동으로 [[396_validation|확인]]하는 로봇**이에요: "이메일 빈칸 없어야 해, 나이는 0~150이어야 해" 같은 규칙을 코드로 쓰면 매번 자동으로 [[396_validation|확인]]해줘요.
- Deequ는 **수십억 개 [[001_dikw_pyramid|데이터]]를 한 번에 검사하는 대형 품질 기계**예요: 소규모 검사는 Great Expectations로, 엄청나게 큰 [[001_dikw_pyramid|데이터]]는 Deequ로 빠르게 처리해요.
- Soda Core는 **요리 레시피처럼 YAML로 쓰는 품질 검사 도구**예요: 코딩을 몰라도 "빈칸 없어야 해, 중복 없어야 해"라고 쉽게 쓸 수 있어요.
