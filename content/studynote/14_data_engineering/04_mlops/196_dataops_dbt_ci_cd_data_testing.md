+++
title = "196. 데이터옵스 (DataOps) CI/CD dbt 데이터 검증 테스트 코드"
date = 2026-04-21

[taxonomies]
tags = ["studynote-data-engineering"]

[extra]
tags = ["studynote-data-engineering"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DataOps는 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)에 [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/)([CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD, 자동화, 테스팅) 원칙을 적용해 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질과 배포 속도를 동시에 향상하는 방법론이다.
> 2. **가치**: dbt([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Build Tool)는 SQL 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환을 코드로 관리하고, 테스트·문서화·계보를 내장하여 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링의 Git+[CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD"를 실현한다.
> 3. **판단 포인트**: [데이터 계약](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)([Data Contract](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)) 도입으로 생산자(파이프라인)와 소비자(분석가) 간 인터페이스를 명시적으로 보장하고, 품질 저하를 조기에 감지한다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/965_dataops/) 정의 및 배경

DataOps는 Gartner(2019)가 정의한 방법론으로, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링·분석·[AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 파이프라인에 <strong>DevOps의 민첩성과 품질 보증 문화</strong>를 이식한다.

### 1.2 기존 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 문제

| 문제 | 증상 |
|:---|:---|
| 테스트 부재 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오류를 수일 후 발견 |
| 수동 배포 | 변경 적용에 수시간~수일 소요 |
| 문서화 없음 | "이 컬럼이 뭘 의미하는지 모름" |
| 의존성 불명확 | 상위 테이블 변경 시 하위 영향 알 수 없음 |
| 환경 불일치 | 개발/스테이징/운영 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 불일치 |

### 1.3 [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/965_dataops/) 핵심 원칙

```
DataOps 4대 원칙

+----------------------------------------------------+
|  1. 코드로서의 데이터 (Data as Code)                |
|     SQL/Python 변환 로직을 Git으로 버전 관리         |
|                                                    |
|  2. 지속적 통합 (Continuous Integration)            |
|     PR 생성 시 자동 데이터 테스트 실행               |
|                                                    |
|  3. 자동화된 품질 보증 (Automated QA)               |
|     not_null, unique, referential_integrity 검사   |
|                                                    |
|  4. 모니터링 기반 운영 (Observability)              |
|     데이터 신선도, 볼륨, 분포 이상 감지              |
+----------------------------------------------------+
```

📢 **섹션 요약 비유**: DataOps는 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)에 "자동차 안전 검사 시스템"을 도입하는 것이다. 매번 수동으로 점검(수동 배포)하는 대신, 출발 전 자동으로 브레이크·엔진·타이어를 검사(자동 테스트)하고 이상 시 출발을 막는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 dbt ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Build Tool) 아키텍처

dbt는 <strong><a href="/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/">ELT</a>(Extract-Load-Transform)</strong> 패턴의 Transform 단계를 SQL로 모듈화하는 프레임워크다.

```
dbt 핵심 구성요소

+------------------------------------------------------+
|                   dbt 프로젝트 구조                    |
|                                                      |
|  models/                                             |
|  +- staging/            <- Bronze -> Silver 변환        |
|  |   +- stg_orders.sql                               |
|  |   +- stg_customers.sql                            |
|  +- intermediate/       <- 중간 변환 레이어             |
|  |   +- int_order_items.sql                          |
|  +- marts/              <- Silver -> Gold (최종 모델)    |
|      +- finance/                                     |
|      |   +- fct_orders.sql                           |
|      +- marketing/                                   |
|          +- dim_customers.sql                        |
|                                                      |
|  tests/                 <- 데이터 품질 테스트           |
|  seeds/                 <- 정적 참조 데이터(CSV)        |
|  macros/                <- 재사용 SQL 함수              |
|  snapshots/             <- SCD(천천히 변하는 차원) 이력 |
+------------------------------------------------------+
```

### 2.2 dbt 모델 정의 및 테스트

```text
-- models/marts/finance/fct_orders.sql
-- 주문 팩트 테이블 생성
-- dbt Jinja 매크로 사용:
-- config(materialized='incremental', unique_key='order_id', on_schema_change='merge')

SELECT
    o.order_id,
    o.customer_id,
    c.segment AS customer_segment,
    p.product_name,
    o.quantity,
    o.unit_price,
    o.quantity * o.unit_price AS total_amount,
    o.created_at::DATE AS order_date
FROM stg_orders o           -- ref('stg_orders')
LEFT JOIN dim_customers c USING (customer_id)   -- ref('dim_customers')
LEFT JOIN dim_products p USING (product_id)     -- ref('dim_products')
-- incremental 조건: WHERE o.created_at > (SELECT MAX(created_at) FROM this_model)
```

```yaml
# models/marts/finance/schema.yml
# 데이터 품질 테스트 정의

version: 2
models:
  - name: fct_orders
    description: "주문 팩트 테이블 - 모든 주문 트랜잭션"
    columns:
      - name: order_id
        description: "주문 고유 식별자"
        tests:
          - not_null          # NULL 없어야 함
          - unique            # 중복 없어야 함

      - name: customer_id
        tests:
          - not_null
          - relationships:    # 참조 무결성
              to: ref('dim_customers')
              field: customer_id

      - name: customer_segment
        tests:
          - accepted_values:  # 허용된 값만
              values: ['Gold', 'Silver', 'Bronze', 'New']

      - name: total_amount
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: ">= 0"   # 음수 금액 불가
```

### 2.3 [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 파이프라인 아키텍처

```
GitHub Actions + dbt Cloud CI/CD 파이프라인

개발자 PR 생성
    |
    v
+--------------------------------------------------------+
|              GitHub Actions Workflow                    |
|                                                        |
|  Job 1: Lint & Format Check                            |
|  +- sqlfluff lint (SQL 스타일)                          |
|  +- yamllint (YAML 검증)                               |
|          | 통과                                         |
|          v                                             |
|  Job 2: dbt CI Run                                     |
|  +- dbt deps (패키지 설치)                              |
|  +- dbt compile (SQL 컴파일 검증)                       |
|  +- dbt run --target ci (스테이징 환경 실행)             |
|  +- dbt test (데이터 품질 테스트)                       |
|          | 통과                                         |
|          v                                             |
|  Job 3: 코드 리뷰 + 승인                               |
|          | 승인                                         |
|          v                                             |
|  Job 4: dbt 운영 환경 배포                              |
|  +- dbt run --target prod                              |
+--------------------------------------------------------+
```

### 2.4 dbt 핵심 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)

| [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) | 역할 |
|:---|:---|
| `dbt run` | SQL 모델 실행 및 테이블 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| `dbt test` | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 테스트 실행 |
| `dbt docs generate` | 자동 문서화 사이트 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| `dbt snapshot` | [SCD Type 2](/knowledge-base/studynote/12_it_management/05_security_compliance/957_scd_type_2/) 이력 테이블 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) |
| `dbt source freshness` | 소스 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 신선도 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |
| `dbt compile` | SQL 컴파일 (실행 없이 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/)) |
| `dbt seed` | CSV [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) -> 테이블 적재 |

📢 **섹션 요약 비유**: dbt는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환의 "레고 설명서"다. 각 블록(SQL 모델)을 ref() 함수로 연결하면 복잡한 구조물을 만들 수 있고, 설명서(문서화)와 품질 검사(테스트)가 자동으로 포함된다.

---

## Ⅲ. 비교 및 연결

### 3.1 [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/965_dataops/) vs [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 매핑

| [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 개념 | [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/965_dataops/) 대응 |
|:---|:---|
| 소스 코드 | SQL 변환 로직 (dbt 모델) |
| [단위 테스트](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/397_unit_test/) | dbt [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 테스트 |
| [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD 파이프라인 | dbt Cloud + GitHub Actions |
| 모니터링/Alerting | Monte Carlo, Bigeye [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관측 |
| [인프라 코드](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/) ([IaC](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/793_iac_idempotency_template/)) | [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) + Airflow [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) [as](/knowledge-base/studynote/03_network/07_network_layer_routing/344_as_autonomous_system_asn/) [Code](/knowledge-base/studynote/02_operating_system/02_process_thread/082_process_memory_structure/) |
| 블루/그린 배포 | dbt 환경 분리 (dev/staging/prod) |
| [코드 리뷰](/knowledge-base/studynote/04_software_engineering/06_software_architecture/330_code_review/) | SQL [PR](/knowledge-base/studynote/15_devops_sre/02_cicd_gitops/067_pull_request_pr_merge_request_code_review/) 리뷰 (dbt Slim [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)) |

### 3.2 [데이터 계약](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/) ([Data Contract](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)) 패턴

[데이터 계약](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 생산자와 소비자 간 인터페이스를 명시적으로 정의하는 계약 문서다.

```yaml
# data-contract.yaml
# 주문 데이터 계약 예시

apiVersion: "0.9.2"
id: "order-events-v1"
name: "주문 이벤트 데이터 계약"

provider:
  name: "주문 서비스 팀"
  contact: "order-team@company.com"

consumer:
  name: "데이터 분석 팀"

terms:
  sla: "99.9% 가용성, 5분 내 지연"
  noticePeriod: "30일 사전 공지 후 변경"

models:
  - name: orders
    fields:
      - name: order_id
        type: string
        required: true
        unique: true
      - name: amount
        type: decimal(10,2)
        required: true
        minimum: 0

quality:
  - rule: "주문 금액은 0 이상"
    query: "SELECT COUNT(*) FROM orders WHERE amount < 0"
    mustBe: 0
```

### 3.3 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관측가능성 ([Data Observability](/knowledge-base/studynote/16_bigdata/13_intro_trends/255_data_observability/))

```
데이터 관측가능성 5대 기둥 (Monte Carlo)

1. 신선도 (Freshness)
   +- "주문 테이블이 마지막 업데이트된 것은 언제인가?"

2. 볼륨 (Volume)
   +- "예상보다 행 수가 급격히 감소/증가했는가?"

3. 스키마 (Schema)
   +- "컬럼이 추가/삭제/변경되었는가?"

4. 분포 (Distribution)
   +- "금액 컬럼의 평균/표준편차가 비정상적으로 변했는가?"

5. 계보 (Lineage)
   +- "이상 데이터가 어느 소스에서 유입되었는가?"
```

📢 **섹션 요약 비유**: [데이터 계약](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)은 음식 주문서와 같다. "피자 라지, 페페로니, 30분 이내 배달"처럼 소비자가 원하는 것을 명확히 적고, 생산자(파이프라인)가 이를 보장한다. 계약 위반 시 즉시 알림이 간다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 dbt 도입 단계별 성숙도 모델

```
DataOps 성숙도 단계

Level 0: 임시방편 (Ad-Hoc)
  +- SQL 스크립트 개인 PC 보관
  +- 수동 실행, 테스트 없음
  +- 문서화 없음

Level 1: 기본 자동화
  +- SQL을 Git에 저장
  +- Airflow/Cron 스케줄링
  +- 기본 not_null 테스트

Level 2: 표준화 (dbt 도입)
  +- dbt 모델 계층화 (staging/mart)
  +- 자동 문서화 + 테스트
  +- 환경 분리 (dev/prod)

Level 3: CI/CD 완전 자동화
  +- PR -> 자동 dbt test
  +- Slim CI (영향받는 모델만 테스트)
  +- 배포 승인 프로세스

Level 4: 데이터 계약 + 관측가능성
  +- Data Contract 도입
  +- Monte Carlo/Bigeye 모니터링
  +- 이상 감지 자동 알림
```

### 4.2 dbt Slim [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/) (변경 영향 범위 최소화)

```bash
# 전체 모델 테스트 (느림, O(N) 시간)
dbt run
dbt test

# Slim CI: 변경된 모델 + 의존 모델만 테스트 (빠름)
dbt run --select state:modified+   # 변경 + 하위 의존
dbt test --select state:modified+

# 실행 시간 비교
전체 테스트: 45분
Slim CI:    3분 (PR 당 93% 절감)
```

### 4.3 실무 [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/965_dataops/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 구성

| 역할 | 도구 | 비고 |
|:---|:---|:---|
| 변환 관리 | dbt Core / dbt Cloud | SQL 모델 관리 |
| [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) | [Apache Airflow](/knowledge-base/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/) | [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 스케줄링 |
| 소스 제어 | GitHub / GitLab | [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/) 관리 |
| [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD | GitHub Actions | 자동 테스트·배포 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관측 | Monte Carlo | 이상 감지 |
| [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | DataHub / Collibra | [메타데이터 관리](/knowledge-base/studynote/16_bigdata/10_governance/203_metadata_management/) |
| 품질 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) | Great Expectations | 복잡한 [검증](/knowledge-base/studynote/04_software_engineering/07_object_oriented/395_verification_process_review/) |

### 4.4 기술사 논술 핵심 포인트

| 논점 | 핵심 내용 |
|:---|:---|
| [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/965_dataops/) vs [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) | 원칙은 동일, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 특성(볼륨·[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 변화) 적용 |
| dbt 도입 효과 | SQL 표준화, 자동 계보, 테스트 내재화 |
| [Data Contract](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/) | 생산자-소비자 인터페이스 명시로 신뢰 확보 |
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관측가능성 | 5대 기둥(신선도·볼륨·[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)·분포·계보) |

📢 **섹션 요약 비유**: dbt [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD는 자동차 생산 라인의 품질 검사 게이트다. 각 조립 단계(SQL 모델)마다 자동으로 검사(테스트)하고, 불량품(오류 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))이 발견되면 다음 단계로 넘어가지 않는다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/965_dataops/) 도입 정량 효과

| 효과 | 도입 전 | 도입 후 |
|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오류 감지 시간 | 수일 후 | 배포 시 즉시 |
| 신기능 배포 주기 | 2~4주 | 1~3일 |
| 파이프라인 장애 [복구](/knowledge-base/studynote/09_security/13_secops_ir_forensics/658_ir_recovery/) | 4~8시간 | 30분 이내 |
| 문서화 커버리지 | 20% | 90%+ (자동화) |
| 테스트 커버리지 | 0% | 80%+ |

### 5.2 [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/965_dataops/) 성공 요소

```
DataOps 성공 3요소

기술(Technology)
  +- dbt + Airflow + GitHub Actions
  +- 데이터 관측가능성 도구

프로세스(Process)
  +- PR 리뷰 + 승인 프로세스
  +- 데이터 계약 표준화
  +- 인시던트 대응 Runbook

문화(Culture)
  +- "데이터도 소프트웨어" 인식
  +- 품질 책임 공유
  +- 지속적 개선 습관
```

### 5.3 결론 요약

DataOps는 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 품질과 속도를 동시에 개선하는 방법론이며, dbt는 그 기술적 구현의 핵심 도구다. 기술사 관점에서는 <strong>dbt 계층화 모델(staging/intermediate/marts), <a href="/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/">CI</a>/CD 자동화 파이프라인, <a href="/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/">데이터 계약</a>의 역할</strong>을 이해하고, 조직 내 [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/965_dataops/) 성숙도 향상 로드맵을 제시할 수 있어야 한다.

📢 **섹션 요약 비유**: DataOps는 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)의 "제조업 QC(품질 관리) 시스템"이다. 과거에는 완성품에서 불량을 발견했다면, DataOps는 각 공정 단계에서 실시간으로 품질을 검사해 불량이 다음 단계로 전파되는 것을 막는다.

---

### 📌 관련 개념 맵

| [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 방법론 | [DataOps](/knowledge-base/studynote/12_it_management/05_security_compliance/965_dataops/) | [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) [DevOps](/knowledge-base/studynote/04_software_engineering/uncategorized/652_devops_calms_culture/) 적용 |
| 도구 | dbt ([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Build Tool) | SQL 기반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 변환 프레임워크 |
| 패턴 | [Data Contract](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/) ([데이터 계약](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)) | 생산자-소비자 인터페이스 계약 |
| 모니터링 | [Data Observability](/knowledge-base/studynote/16_bigdata/13_intro_trends/255_data_observability/) ([데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관측가능성) | 5대 기둥 기반 품질 모니터링 |
| 테스트 | dbt Tests | not_null, unique, accepted_values |
| [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/)/CD | GitHub Actions | 자동 테스트·배포 워크플로우 |
| [오케스트레이션](/knowledge-base/studynote/13_cloud_architecture/02_iaas_paas_saas/073_container_orchestration_tools/) | [Apache Airflow](/knowledge-base/studynote/14_data_engineering/04_mlops/168_airflow_dag_pipeline_scheduling/) | [DAG](/knowledge-base/studynote/06_ict_convergence/05_data_science/401_bayesian_network_dag_causality/) 기반 파이프라인 스케줄링 |
| 변환 패턴 | [ELT](/knowledge-base/studynote/14_data_engineering/01_infrastructure/034_elt/) (Extract-Load-Transform) | dbt가 담당하는 Transform 단계 |
| 최적화 | Slim [CI](/knowledge-base/studynote/12_it_management/02_itsm_itil/874_configuration_item/) | 변경 영향 모델만 선택 테스트 |

### 👶 어린이를 위한 3줄 비유 설명

1. DataOps는 요리사가 요리([데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/))를 만들 때마다 맛 검사(테스트)를 자동으로 하는 시스템이에요. 쓴맛(오류)이 나면 손님(사용자)에게 내보내기 전에 잡아낸다고요.

### 📈 관련 키워드 및 발전 흐름도

```text
수동 데이터 파이프라인 (ad-hoc SQL · 스크립트)
    |
    v
DataOps: 데이터 파이프라인 CI/CD 자동화
    +-► dbt (data build tool): SQL 기반 변환 + 테스트
    +-► Great Expectations: 데이터 품질 검증
    +-► Git 기반 버전 관리 · PR 리뷰 · 자동 배포
    |
    v
데이터 테스트
    +-► 스키마 테스트: not_null · unique · accepted_values
    +-► 데이터 품질 테스트: 범위 · 참조 무결성
    +-► 프레시니스 테스트: 데이터 최신성 확인
    |
    v
Observability: Monte Carlo · Bigeye -> 데이터 이상 자동 감지
```
2. dbt는 레고 설명서예요. 각 레고 블록(SQL 모델)이 어떻게 연결되는지 그려주고, 완성된 모습(문서)과 품질 검사(테스트)도 함께 제공해요.
3. [데이터 계약](/knowledge-base/studynote/16_bigdata/12_trends/236_data_contract/)은 식당 메뉴판이에요. "피자는 30분 안에, 반드시 뜨겁게, 토핑은 이것들"처럼 소비자가 기대하는 것을 명확히 약속하고, 지키지 않으면 알림이 와요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 196 / 258

<- **이전**: [195. 연방 쿼리 (Federated Query) 데이터 패브릭 분산 메타 통계망 조인](/knowledge-base/studynote/14_data_engineering/04_mlops/195_federated_query_data_fabric_distributed_join/)
**다음**: [197. 데이터 카탈로그 (Data Catalog) 계보 (Lineage) 시각화 보안 정책 연계망](/knowledge-base/studynote/14_data_engineering/04_mlops/197_data_catalog_lineage_visualization_security/) ->

---
