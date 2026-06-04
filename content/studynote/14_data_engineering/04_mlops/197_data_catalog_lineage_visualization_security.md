---
title: "197. 데이터 카탈로그 (Data Catalog) 계보 (Lineage) 시각화 보안 정책 연계망"
date: "2026-04-21"
tags:
  - "studynote-data-engineering"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)([Data Catalog](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산의 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)를 중앙에서 관리하는 "[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 도서관 목록 시스템"이며, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보([Data Lineage](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/))는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 원천부터 소비까지 흐름을 추적한다.
> 2. **가치**: [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)/[CCPA](/studynote/09_security/16_data_privacy/800_ccpa/) 규정 준수를 위한 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 주체 권리(삭제권, 이동권) 이행 시, 계보 추적으로 영향받는 모든 시스템을 자동으로 식별하고 대응할 수 있다.
> 3. **판단 포인트**: 자동 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 수집(OpenLineage 표준)과 태그 기반 [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/) 연계가 핵심이며, [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) 성숙도에 따라 도구 선택이 달라진다.

---

## Ⅰ. 개요 및 필요성

### 1.1 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 필요성

조직의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산이 증가할수록 "어디에 어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 있는지" 파악이 어려워진다.

```
데이터 카탈로그가 없는 현실

분석가: "고객 이탈률 분석하려면 어떤 테이블 써야 하나?"
         -> Slack에 질문 -> 2시간 기다림
         -> "customer_v2 쓰세요, customer는 deprecated"
         -> "근데 PII가 포함되어 있어서 권한 신청 필요해요"
         -> 권한 신청 -> 승인 3일 소요

총 소요 시간: 데이터 찾기에만 3일 낭비
```

| 문제 | [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 해결책 |
|:---|:---|
| "이 테이블이 뭘 의미하나?" | 비즈니스 용어 정의, 컬럼 설명 |
| "어떤 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 써야 하나?" | 검색, 추천, [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 지표 |
| "이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 써도 되나?" | 접근 권한, PII 태그 자동 표시 |
| "이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 어디서 왔나?" | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보(Lineage) [시각화](/studynote/16_bigdata/01_intro/003_bigdata_7v/) |
| "이 테이블 변경하면 영향은?" | 하위 의존 계보 추적 |

### 1.2 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보 ([Data Lineage](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/)) 정의

[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보는 <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a>의 원천(Source)부터 최종 소비(Consumption)까지 흐름</strong>을 추적하는 기능이다.

```
데이터 계보 예시

[원천 시스템]         [처리]              [소비]
PostgreSQL(주문DB)
    | 원시 데이터
    v
S3 Bronze Layer   -> Spark 변환 ->  Silver Layer
    |                                 |
    |                        dbt 집계 모델
    |                                 |
    |                                 v
    +----------------------> Gold Layer (KPI)
                                      |
                           +----------+----------+
                           v          v           v
                        Tableau   ML 모델     REST API
                       (대시보드) (이탈 예측)  (앱 서빙)
```

📢 **섹션 요약 비유**: [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 도서관의 도서 목록 시스템이다. 책 제목(테이블명), [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)(카테고리), 저자([데이터 소유자](/studynote/16_bigdata/10_governance/200_data_owner/)), 내용 요약(컬럼 설명), 대출 가능 여부(접근 권한)를 한눈에 볼 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2.1 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 핵심 구성요소

```
+----------------------------------------------------------+
|                  데이터 카탈로그 아키텍처                   |
|                                                          |
|  +----------------------------------------------------+  |
|  |              메타데이터 수집 레이어                   |  |
|  |                                                    |  |
|  |  커넥터 기반 자동 크롤링:                            |  |
|  |  +- JDBC (Oracle, PostgreSQL, MySQL)               |  |
|  |  +- Hive Metastore / AWS Glue Catalog              |  |
|  |  +- dbt Artifacts (manifest.json)                  |  |
|  |  +- Kafka Schema Registry                          |  |
|  |  +- REST API / OpenLineage                         |  |
|  +--------------------------+-------------------------+  |
|                             |                            |
|  +--------------------------v-------------------------+  |
|  |              메타데이터 저장 레이어                   |  |
|  |                                                    |  |
|  |  +- 기술적 메타데이터: 스키마, 타입, 통계           |  |
|  |  +- 비즈니스 메타데이터: 정의, 소유자, 용어집       |  |
|  |  +- 운영 메타데이터: 접근 로그, 업데이트 이력       |  |
|  |  +- 계보 메타데이터: 소스->변환->소비 흐름            |  |
|  +--------------------------+-------------------------+  |
|                             |                            |
|  +--------------------------v-------------------------+  |
|  |                서빙 레이어                           |  |
|  |                                                    |  |
|  |  +- 검색 엔진 (Elasticsearch)                      |  |
|  |  +- 계보 시각화 (그래프 DB)                         |  |
|  |  +- 보안 정책 엔진 (태그 기반 ABAC)                 |  |
|  |  +- REST API / GraphQL                             |  |
|  +----------------------------------------------------+  |
+----------------------------------------------------------+
```

### 2.2 주요 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 제품 비교

| 제품 | 유형 | 특징 | 계보 지원 |
|:---|:---|:---|:---|
| Apache Atlas | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계 연계 | 상세 계보 |
| DataHub | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | LinkedIn 개발, 실시간 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) | Push 기반 |
| OpenMetadata | [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) | 현대적 UI, 통합 품질 | 완전 지원 |
| Collibra | 상용 | 거버넌스 중심 | 상세 계보 |
| Alation | 상용 | 검색 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/), 사용 패턴 분석 | 지원 |
| AWS Glue [Data Catalog](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | 클라우드 | AWS [서비스](/studynote/13_cloud_architecture/02_iaas_paas_saas/090_service_kubernetes_network_load_balancing/) 자동 연계 | 제한적 |

### 2.3 OpenLineage 표준

```
OpenLineage: 계보 메타데이터 수집 오픈 표준

+----------------------------------------------------------+
|  OpenLineage 이벤트 흐름                                  |
|                                                          |
|  Airflow/Spark/dbt/Flink                                 |
|  (파이프라인 실행 엔진)                                   |
|         | OpenLineage 이벤트 발생                         |
|         | { "run": {...}, "job": {...},                  |
|         |   "inputs": [...], "outputs": [...] }          |
|         v                                                |
|  OpenLineage API 서버                                    |
|  (Marquez 또는 플랫폼별 구현)                             |
|         | 계보 정보 저장                                  |
|         v                                                |
|  데이터 카탈로그 (DataHub / OpenMetadata)                 |
|  -> 시각적 계보 그래프 표시                                |
+----------------------------------------------------------+
```

### 2.4 [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/) 연계: 태그 기반 접근 제어 ([ABAC](/studynote/09_security/11_iam_access_control/572_abac/))

| 태그 | 의미 | [보안 정책](/studynote/09_security/01_intro_principles/007_security_policy/) |
|:---|:---|:---|
| `pii:email` | 이메일 주소 포함 | 기본 마스킹, DBA만 접근 |
| `pii:ssn` | 주민등록번호 | 암호화 필수, 승인 필요 |
| `sensitivity:confidential` | 기밀 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 특정 팀만 접근 |
| `gdpr:personal` | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) | 삭제권/이동권 이행 대상 |
| `ccpa:regulated` | [CCPA](/studynote/09_security/16_data_privacy/800_ccpa/) 규제 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 판매 금지, 삭제 요청 처리 |

📢 **섹션 요약 비유**: [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보는 식품의 원산지 추적 시스템이다. "이 김치가 어느 배추 농장에서 왔는지, 어떤 공장에서 가공됐는지, 어느 마트에서 팔렸는지"를 역방향으로 추적할 수 있다.

---

## Ⅲ. 비교 및 연결

### 3.1 [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)/CCPA와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보 연계

```
GDPR 삭제권(Right to be Forgotten) 이행 시나리오

사용자: "내 모든 데이터 삭제 요청"
    |
    v
데이터 카탈로그 조회
    | user_id로 태그된 모든 데이터셋 검색
    v
+-----------------------------------------------+
|  영향받는 데이터 자산 목록 (계보로 자동 추적)    |
|                                               |
|  ① PostgreSQL.users 테이블  -> 직접 삭제        |
|  ② S3/bronze/user_events   -> 덮어쓰기/삭제    |
|  ③ Silver.user_profile     -> 재처리 필요      |
|  ④ Gold.customer_360       -> 재집계 필요      |
|  ⑤ ML Feature Store        -> 피처 삭제        |
|  ⑥ Elasticsearch 인덱스    -> 인덱스 업데이트   |
+-----------------------------------------------+
    | 자동화된 삭제 워크플로우 실행
    v
완료 증명 리포트 생성 (규정 준수 감사용)
```

### 3.2 컬럼 레벨 보안 (Column-Level [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/))

```sql
-- Apache Atlas + Ranger 연계 컬럼 마스킹 예시
-- email 컬럼: 마스킹 정책 적용

-- 일반 사용자 조회 결과:
SELECT email FROM customers;
-- 결과: k***@example.com (앞 1자리 + *** + @도메인)

-- 권한 있는 사용자 조회 결과:
SELECT email FROM customers;
-- 결과: kim@example.com (원본)

-- 정책 정의 (Ranger Policy)
-- 태그: pii:email
-- 일반 사용자 -> MASK_SHOW_FIRST_1 적용
-- 데이터팀 -> 원본 표시
```

### 3.3 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 검색 패턴

| 검색 유형 | 예시 | 결과 |
|:---|:---|:---|
| 키워드 검색 | "고객 이탈" | 관련 테이블, 대시보드, 보고서 |
| 태그 기반 | `pii:email` | 이메일 포함 모든 자산 |
| 소유자 기반 | `owner:data-team` | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)팀 소유 자산 |
| 계보 기반 | 특정 테이블 -> 영향 하위 | 하위 의존 모든 자산 |
| 품질 기반 | freshness < 1일 | 최근 업데이트 자산 |

📢 **섹션 요약 비유**: 컬럼 레벨 보안은 신분에 따른 문서 열람 권한과 같다. 일반 직원은 주민번호를 "***-*****"처럼 가린 문서만 볼 수 있고, 인사팀만 원본 서류에 접근할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4.1 DataHub 실시간 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 아키텍처

```
DataHub 아키텍처 (LinkedIn 오픈소스)

+------------------------------------------------------+
|                                                      |
|  데이터 소스 (Kafka, Snowflake, dbt, Airflow, ...)   |
|         | OpenLineage / DataHub Ingestion Framework  |
|         v                                            |
|  Kafka Topic: MetadataChangeEvent (MCE)              |
|         | 실시간 메타데이터 이벤트 스트림              |
|         v                                            |
|  +----------------------------------------------+   |
|  |  DataHub GMS (Generalized Metadata Service)  |   |
|  |  +- 메타데이터 저장 (Apache Cassandra)        |   |
|  |  +- 그래프 저장 (Neo4j / MySQL)               |   |
|  |  +- 검색 인덱스 (Elasticsearch)               |   |
|  +----------------------------------------------+   |
|         |                                            |
|         v                                            |
|  DataHub Frontend (React UI)                         |
|  +- 데이터 검색                                      |
|  +- 계보 시각화                                      |
|  +- 정책 관리                                        |
+------------------------------------------------------+
```

### 4.2 기술사 관점: [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) 프레임워크

| 거버넌스 요소 | [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 역할 |
|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 정의 (Definition) | 비즈니스 용어집, 컬럼 설명 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권 (Ownership) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋별 소유팀/담당자 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 (Quality) | 품질 규칙, 측정 결과 연계 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 보안 ([Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/)) | 태그 기반 [ABAC](/studynote/09_security/11_iam_access_control/572_abac/) [정책](/studynote/10_ai/02_dl_architecture_new/164_policy/) |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 프라이버시 (Privacy) | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)/[CCPA](/studynote/09_security/16_data_privacy/800_ccpa/) 태그, 삭제 워크플로우 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보 (Lineage) | 영향 분석, [변경 관리](/studynote/12_it_management/02_itsm_itil/079_change_enablement/) |

### 4.3 도입 성숙도 모델

```
데이터 카탈로그 성숙도 4단계

Level 1: 기술적 메타데이터
  +- 스키마, 컬럼 타입, 통계 자동 수집

Level 2: 비즈니스 메타데이터
  +- 비즈니스 용어, 소유자, 설명 추가

Level 3: 데이터 계보 + 품질
  +- 흐름 추적, 이상 감지 연계

Level 4: 능동적 거버넌스
  +- AI 추천, 자동 태깅, 정책 자동 집행
```

### 4.4 OpenMetadata [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) 예시

```yaml
# OpenMetadata 데이터셋 정의 예시
name: customers
displayName: "고객 마스터 테이블"
description: "전체 고객 정보를 포함하는 핵심 테이블"
owner: "@data-team"
tags:
  - "PII.Sensitive"
  - "GDPR.PersonalData"
columns:
  - name: customer_id
    description: "고객 고유 식별자 (UUID)"
    dataType: STRING
    tags: []
  - name: email
    description: "고객 이메일 주소"
    dataType: STRING
    tags:
      - "PII.Email"
      - "GDPR.PersonalData"
    dataQuality:
      - rule: "not_null"
      - rule: "matches_regex: ^[\\w.+-]+@[\\w-]+\\.[\\w.]+$"
```

📢 **섹션 요약 비유**: [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/) 프레임워크는 병원의 의무기록 관리 시스템과 같다. 누가 어떤 기록을 언제 봤는지([감사](/studynote/02_operating_system/10_security/606_auditing_linux_auditd/)), 기록의 원본 출처(계보), 누가 볼 수 있는지(접근 권한), 정보 삭제 요청(삭제권)을 모두 관리한다.

---

## Ⅴ. 기대효과 및 결론

### 5.1 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 도입 기대효과

| 효과 | 정량 지표 |
|:---|:---|
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [탐색 시간](/studynote/01_computer_architecture/08_io_storage_systems/324_seek_time/) | 3일 -> 10분 (90% 감소) |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 중복 자산 | 중복 파이프라인 40% 제거 |
| 규정 준수 대응 | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 삭제 요청 처리 3일 -> 1시간 |
| [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) | 품질 지표 가시화로 의사결정 [신뢰도](/studynote/14_data_engineering/02_math_mining/085_confidence_association_rule_conditional_probability/) 향상 |
| 온보딩 시간 | 신규 분석가 생산성 2배 향상 |

### 5.2 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)와 [AI](/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/)/ML 연계

```
AI 강화 데이터 카탈로그 기능

1. 자동 태깅 (Auto Tagging)
   NLP로 컬럼명/설명 분석 -> PII 자동 감지

2. 유사 데이터셋 추천 (Similar Assets)
   "이 테이블과 유사한 데이터 3개 추천"

3. 이상 설명 (Anomaly Explanation)
   "주문량이 30% 급감한 이유: 결제 서버 장애"

4. 자연어 쿼리 (NL to SQL)
   "지난달 APAC 지역 상위 10 고객" -> SQL 자동 생성
```

### 5.3 결론 요약

[데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)와 계보는 현대 [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)의 핵심 인프라이며, [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)/[CCPA](/studynote/09_security/16_data_privacy/800_ccpa/) 규정 준수와 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [신뢰성](/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/) 확보를 위한 필수 요소다. 기술사 관점에서는 <strong>OpenLineage 표준 기반 자동 계보 수집, 태그 기반 <a href="/studynote/09_security/11_iam_access_control/572_abac/">ABAC</a> <a href="/studynote/09_security/01_intro_principles/007_security_policy/">보안 정책</a>, <a href="/studynote/09_security/16_data_privacy/791_gdpr_eu/">GDPR</a> 삭제권 이행과 계보의 연계 방법</strong>을 명확히 설명할 수 있어야 한다.

📢 **섹션 요약 비유**: [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 기업 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 "GPS + 사용설명서 + 출입 카드 시스템"이다. 어디에 있는지(GPS), 어떻게 사용하는지(사용설명서), 누가 접근할 수 있는지(출입 카드)를 통합 관리한다.

---

### 📌 관련 개념 맵

| [관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 개념 | 설명 |
|:---|:---|:---|
| 핵심 시스템 | [Data Catalog](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) ([데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)) | [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 중앙 관리 시스템 |
| 기능 | [Data Lineage](/studynote/12_it_management/05_security_compliance/214_data_lineage_tracking/) ([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보) | 원천 -> 소비 흐름 추적 |
| 표준 | OpenLineage | 계보 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 수집 오픈 표준 |
| 제품 | DataHub | LinkedIn [오픈소스](/studynote/12_it_management/05_security_compliance/191_oss_license_compliance/) [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) 플랫폼 |
| 제품 | Apache Atlas | [Hadoop](/studynote/03_network/16_data_center_cloud/843_hadoop_rack_awareness_data_replication_topology/) 생태계 거버넌스 도구 |
| 보안 | [ABAC](/studynote/09_security/11_iam_access_control/572_abac/) ([Attribute-Based Access Control](/studynote/09_security/11_iam_access_control/572_abac/)) | 태그 기반 접근 제어 |
| 보안 | Column-Level [Security](/studynote/04_software_engineering/05_devops_ci_cd/283_security_tactics/) (컬럼 레벨 보안) | 컬럼별 마스킹/암호화 |
| 규정 | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 삭제권 | [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 삭제 요청 권리 |
| 규정 | [CCPA](/studynote/09_security/16_data_privacy/800_ccpa/) | 캘리포니아 소비자 프라이버시법 |

### 👶 어린이를 위한 3줄 비유 설명

1. [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 도서관의 책 목록 컴퓨터예요. "고객"이라고 검색하면 관련 책([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))들이 어디 있는지, 누가 빌릴 수 있는지 바로 알 수 있어요.

### 📈 관련 키워드 및 발전 흐름도

```text
데이터 사일로 · 메타데이터 부재
    |
    v
데이터 카탈로그
    +-► 메타데이터 수집: 스키마 · 통계 · 태그 · 오너
    +-► 검색 · 디스커버리: "고객 테이블 어디?"
    +-► 접근 제어: RBAC · 태그 기반 정책
    |
    v
데이터 계보 (Lineage) 시각화
    +-► 업스트림/다운스트림 영향 분석
    +-► 변경 전 임팩트 평가
    |
    v
도구: DataHub (LinkedIn) · Amundsen (Lyft) · Unity Catalog
```
2. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 계보는 음식 원산지 추적이에요. 내 접시에 올라온 음식이 어느 농장 재료로, 어느 공장에서 만들어졌는지 역방향으로 따라갈 수 있죠.
3. [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/) 삭제권에 계보를 연계하면, 한 사람의 정보를 삭제할 때 그 정보가 복사된 모든 곳(10개 창고)을 자동으로 찾아 동시에 지울 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 197 / 258

<- **이전**: [196. 데이터옵스 (DataOps) CI/CD dbt 데이터 검증 테스트 코드](/studynote/14_data_engineering/04_mlops/196_dataops_dbt_ci_cd_data_testing/)
**다음**: [198. 지식 증류 (Knowledge Distillation) 소프트 타겟 확률 분포 모방](/studynote/14_data_engineering/04_mlops/198_knowledge_distillation_soft_target_probability/) ->

---
