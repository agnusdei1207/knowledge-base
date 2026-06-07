---
title: "026. Da Data Administrator"
date: "2026-04-29"
tags:
  - "studynote-database"
weight: 26
---
## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) ([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Administrator, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 관리자)는 조직 전체의 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산([Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Asset)을 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/)적으로 관리하는 역할로, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표준 정의, [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/) 설계·검토, [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 관리, [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)([Metadata](/studynote/05_database/01_db_architecture_relational/012_metadata/)) 관리를 담당한다. DBA가 특정 DB 시스템의 운영·[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 책임진다면, DA는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자체의 의미·품질·거버넌스를 책임진다.
> 2. **가치**: 대규모 금융·공공 기관에서 같은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 부서마다 다른 이름(고객ID vs 회원번호), 다른 형식(날짜: YYYYMMDD vs YYYY-MM-[DD](/studynote/04_software_engineering/10_trends_pm_quality/769_architecture/))으로 관리되면 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합(EDW, [MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/))이 불가능해진다. DA는 전사 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표준을 수립하여 이 문제를 해결한다.
> 3. **판단 포인트**: 국가정보화 사업에서 [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 산출물([데이터 표준화](/studynote/05_database/02_modeling_normalization/126_data_standardization_word_domain_term/) 정의서, [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) [데이터 모델](/studynote/05_database/01_db_architecture_relational/014_data_model_components/))은 발주처 산출물 검토의 핵심 항목이다. KDAS (Korea [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Architecture](/studynote/12_it_management/05_security_compliance/319_architecture/) Standard, 한국형 [데이터 아키텍처](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 표준)와 [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)# 도구는 공공 부문 [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 업무의 실질적 표준이다.

---

## Ⅰ. 개요 및 필요성

```text
+------------------------------------------------------------+
|         DA vs DBA 역할 구분                                  |
+--------------------------+---------------------------------+
|       DA (데이터 관리자)  |      DBA (DB 관리자)            |
+--------------------------+---------------------------------+
| 데이터 표준·의미 정의     | DB 엔진 설치·운영               |
| 논리/개념 데이터 모델     | 물리 스키마 구현                |
| 메타데이터 관리           | 성능 튜닝·백업·복구             |
| 데이터 품질 지표 수립     | 가용성·보안 관리                |
| 전사 데이터 거버넌스      | 특정 DBMS 운영 전문가           |
+--------------------------+---------------------------------+
```

- **📢 섹션 요약 비유**: DA는 도시 전체의 도로 체계를 설계하는 도시 계획가이고, DBA는 특정 도로의 포장·유지보수 담당 기술자다. 도시 계획가([DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/))가 없으면 도로들이 연결되지 않는다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 주요 업무 영역

```text
+---------------------------------------------------------+
|              DA 업무 영역                                  |
+---------------------------------------------------------+
| 1. 데이터 표준화                                          |
|    - 용어 사전, 도메인 정의, 코드 표준화                   |
|    - 예: "고객번호" = 10자리 숫자, CUSTOMER_ID            |
|                                                         |
| 2. 데이터 모델링                                          |
|    - 개념/논리/물리 데이터 모델 설계·검토                   |
|    - ERD (Entity-Relationship Diagram) 작성              |
|                                                         |
| 3. 메타데이터 관리                                        |
|    - 데이터 사전, 데이터 카탈로그 운영                     |
|    - 데이터 리니지(Lineage) 추적                          |
|                                                         |
| 4. 데이터 품질 관리                                       |
|    - 품질 기준 수립, 이상 데이터 탐지·정제                 |
+---------------------------------------------------------+
```

### [데이터 표준화](/studynote/05_database/02_modeling_normalization/126_data_standardization_word_domain_term/)의 실제 효과

```text
표준화 전:                    표준화 후 (DA 수립):
A시스템: CUST_NO (숫자8자리)   전사: CUSTOMER_ID (숫자10자리)
B시스템: 고객ID (숫자6자리)    모든 시스템: CUSTOMER_ID 통일
C시스템: customer_code (문자)  -> EDW 통합, MDM 구축 가능
```

- **📢 섹션 요약 비유**: [데이터 표준화](/studynote/05_database/02_modeling_normalization/126_data_standardization_word_domain_term/)는 전국 단위 도로명 주소 통일이다. "서울시 강남구 테헤란로 152"처럼 모든 곳에서 같은 형식을 쓰면, 택배([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 통합)가 정확하게 목적지를 찾을 수 있다.

---

## Ⅲ. 비교 및 연결

| 역할 | [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) | [DBA](/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 아키텍트 |
|:---|:---|:---|:---|
| **주요 관심** | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 의미·표준·품질 | DB 운영·[성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 전사 [데이터 아키텍처](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) |
| **산출물** | 표준화 정의서, [논리](/studynote/09_security/04_endpoint_security/369_logic_bomb/) 모델 | 물리 [스키마](/studynote/05_database/01_db_architecture_relational/005_schema/), 튜닝 보고서 | [데이터 아키텍처](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 로드맵 |
| **규모** | 전사 수준 | DB 인스턴스 수준 | 기업 [전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 수준 |

- **📢 섹션 요약 비유**: DA는 도서관 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 체계 담당자([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표준·[분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)), DBA는 서가 정리사(DB 운영·정렬), [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 아키텍트는 도서관 전체 건물 설계자([전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) 아키텍처)다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 공공 사업 [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 산출물 요건 (행안부 고시)
1. <strong><a href="/studynote/05_database/02_modeling_normalization/126_data_standardization_word_domain_term/">데이터 표준화</a> 정의서</strong>: 용어, [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/), 코드, 엔터티 표준 정의.
2. <strong><a href="/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a> <a href="/studynote/05_database/01_db_architecture_relational/014_data_model_components/">데이터 모델</a></strong>: [정규화](/studynote/01_computer_architecture/02_data_representation_arithmetic/093_normalization/)된 ERD, 엔터티·[속성](/studynote/05_database/02_modeling_normalization/082_attribute_types_er_model/)·[관계](/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) 명세.
3. <strong><a href="/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/">DA</a># 도구 산출물</strong>: 표준화 이력, 승인 워크플로우 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/).
4. <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질 계획서</strong>: 측정 항목, 기준값, 개선 계획.

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 없이 개발팀이 각자 컬럼명을 정하는 [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)("비표준 모델링"). 3년 후 EDW 구축 프로젝트에서 300개 테이블의 컬럼명 불일치를 매핑하는 데 6개월이 소요된 실제 사례가 있다.

- **📢 섹션 요약 비유**: [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 없는 개발은 지도 없이 여러 팀이 각자 길을 닦는 것이다. 나중에 연결하려 보면 도로가 서로 높이·폭이 달라서 이어붙일 수 없다.

---

## Ⅴ. 기대효과 및 결론

| 기대효과 | 내용 |
|:---|:---|
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 통합</strong> | 표준화 기반 EDW·[MDM](/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) 구축 가능 |
| **품질 보장** | 전사 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 기준 수립·관리 |
| **거버넌스** | [GDPR](/studynote/09_security/16_data_privacy/791_gdpr_eu/)·[데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 3법 컴플라이언스 기반 |

현대 DA는 [데이터 메시](/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/studynote/12_it_management/05_security_compliance/320_data_mesh/)) 아키텍처에서 [도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 오너십을 지원하는 "연방형 거버넌스(Federated Governance)" 역할로 진화하고 있다.

- **📢 섹션 요약 비유**: 현대 DA는 각 국가([도메인](/studynote/05_database/02_modeling_normalization/064_relation_domain/))의 자율성을 존중하면서 국제 표준(연방 거버넌스)을 관리하는 UN 같은 역할이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/">DBA</a></strong> | DA와 역할 분담; [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)=[전략](/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/), [DBA](/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/)=운영 |
| **EDW** | [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 표준화 기반 전사 [데이터 웨어하우스](/studynote/12_it_management/05_security_compliance/209_data_warehouse_schema_on_write/) |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/012_metadata/">메타데이터</a></strong> | DA의 핵심 관리 대상 |
| <strong><a href="/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 품질</strong> | DA의 측정·개선 책임 영역 |
| <strong><a href="/studynote/12_it_management/05_security_compliance/320_data_mesh/">Data Mesh</a></strong> | 현대 [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) [데이터 거버넌스](/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/)에서 [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 역할 |

### 📈 관련 키워드 및 발전 흐름도

```text
[데이터 표준화 필요 인식 — 사일로 데이터 문제]
    |
    v
[DA 역할 정립 — 데이터 표준·모델·품질 관리]
    |
    v
[EDW/MDM — DA 표준화 기반 통합 데이터 플랫폼]
    |
    v
[데이터 카탈로그 — 메타데이터 자동화 관리]
    |
    v
[Data Mesh — 분산 도메인 오너십 + 연방 거버넌스]
```

### 👶 어린이를 위한 3줄 비유 설명

1. DA는 학교 도서관의 도서 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/) 담당 선생님이에요! 책([데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))마다 정해진 규칙으로 제목·저자·장르를 정리해서 누구나 쉽게 찾게 해요.
2. DA가 없으면 각 선생님이 다른 방식으로 책을 정리해서, 다른 반(시스템)의 책과 합치기가 매우 어려워요.
3. 요즘은 AI가 자동으로 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 [분류](/studynote/16_bigdata/05_analysis/104_classification_analysis/)·정리하는 [데이터 카탈로그](/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) 도구가 [DA](/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/) 업무를 도와주고 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 26 / 600

<- **이전**: [25. DBA (Database Administrator) — 데이터베이스 관리자](/studynote/05_database/01_db_architecture_relational/025_dba_database_administrator/)
**다음**: [27. 데이터베이스 설계자 (Database Designer) — DB 설계 역할과 책임](/studynote/05_database/01_db_architecture_relational/027_database_designer/) ->

---
