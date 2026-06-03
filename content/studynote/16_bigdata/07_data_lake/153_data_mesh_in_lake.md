+++
title = "153. 데이터 메시 관점의 레이크하우스 (Data Mesh on Lakehouse)"
date = 2026-04-21

[taxonomies]
tags = ["studynote-bigdata"]

[extra]
tags = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)
1. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)([Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/))는 조직 원칙이고 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 기술 플랫폼이며, 둘의 결합은 <strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a>별 자율성</strong>과 <strong>전사 거버넌스 <a href="/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/">일관성</a></strong>을 동시에 달성하는 현대 [데이터 아키텍처](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)의 핵심 패턴이다.
2. 각 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 자신의 Delta 테이블을 소유·운영하고 Unity Catalog를 통해 표준화된 접근 제어와 리니지 추적을 공유함으로써, 중앙화 병목 없이 전사 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질이 관리된다.
3. <strong><a href="/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/">데이터 제품</a>(<a href="/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/">Data Product</a>)</strong>이 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 간 계약 단위가 되며, 각 제품은 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)·[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)·품질 지표를 명시적으로 선언하여 소비자가 신뢰하고 사용할 수 있는 인터페이스를 제공한다.

---

## Ⅰ. 개요 및 필요성

전통적 중앙화 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)는 단일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 팀이 전사 모든 [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인을 소유하는 구조다. [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전문 지식 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 변환하다 보면 비즈니스 맥락을 잃은 '[컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 빈곤' [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 양산된다. 또한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 요청이 중앙 팀 병목이 되어 시간이 지날수록 조직 전체의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 활용 속도가 떨어진다.

Zhamak Dehghani가 2019년 제시한 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 원칙은 이 문제를 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 중심 소유권 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)으로 해결한다. [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 이 원칙을 기술적으로 구현하는 최적 인프라다.

| [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) 원칙 | [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 기술 매핑 |
|:---|:---|
| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지향 소유권 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)별 [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/), Delta 테이블 소유 |
| [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)·[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 계약이 있는 Gold Delta 테이블 |
| 셀프서비스 인프라 | [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) Workflows 템플릿, AutoLoader |
| 연합 거버넌스 | [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/) 중앙 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) + [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 자율 실행 |

> 📢 **섹션 요약 비유**: 중앙화 레이크가 모든 요리를 하나의 주방에서 하는 대형 식당이라면, [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 각 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)이 자기 레스토랑을 운영하되 공통 식품위생법(거버넌스)은 동일하게 따르는 푸드코트다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```
┌──────────────────────────────────────────────────────────────────┐
│            Data Mesh on Lakehouse 아키텍처                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Unity Catalog (연합 거버넌스 레이어)                      │    │
│  │  - 중앙 접근 제어 정책 (컬럼 마스킹, 행 필터)              │    │
│  │  - 감사 로그 통합, 리니지 추적                             │    │
│  └────────────────────────────┬────────────────────────────┘    │
│                               │ 정책 적용                        │
│             ┌─────────────────┼──────────────────┐              │
│             │                 │                  │              │
│   ┌─────────▼──────┐ ┌───────▼────────┐ ┌──────▼──────────┐   │
│   │  도메인: 영업    │ │ 도메인: 마케팅  │ │ 도메인: 물류     │   │
│   │  catalog.sales  │ │ catalog.mkt    │ │ catalog.logist. │   │
│   │                │ │               │ │                │   │   │
│   │  Bronze (raw)  │ │ Bronze (raw)  │ │ Bronze (raw)   │   │   │
│   │  Silver        │ │ Silver        │ │ Silver         │   │   │
│   │  Gold 제품 테이블│ │ Gold 제품 테이블│ │ Gold 제품 테이블│   │   │
│   │  (SLA 계약 포함)│ │ (SLA 계약 포함)│ │ (SLA 계약 포함)│   │   │
│   └────────────────┘ └───────────────┘ └────────────────┘   │   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  소비자 도메인 (교차 도메인 쿼리)                           │   │
│  │  - Unity Catalog 공유 테이블 읽기                          │   │
│  │  - Delta Sharing으로 외부 공유                             │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

<strong><a href="/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/">도메인</a>별 <a href="/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/">레이크하우스</a> 구성 요소</strong>

| 구성 요소 | 역할 | 도구 |
|:---|:---|:---|
| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 테이블 [네임스페이스](/knowledge-base/studynote/02_operating_system/01_overview_architecture/061_namespace/) | [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/) [catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) 수준 |
| [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/) | Bronze→Silver→Gold 변환 | [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) Workflows / [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) |
| [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) 테이블 | 외부 소비 인터페이스 | Gold Delta Table + [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 문서 |
| 품질 [모니터](/knowledge-base/studynote/02_operating_system/04_synchronization/229_monitor/)링 | 제품 [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/) 준수 추적 | [DLT](/knowledge-base/studynote/03_network/18_optical_nextgen_automation/919_dlt_distributed_ledger_technology_consensus_bottleneck/) Expectations / Soda |
| 셀프서비스 템플릿 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 신규 팀 온보딩 | [Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/) Repos + [Terraform](/knowledge-base/studynote/15_devops_sre/05_devsecops/195_terraform_hashicorp_agnostic_aws_gcp/) |

> 📢 **섹션 요약 비유**: [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) on Lakehouse는 프랜차이즈 식당 모델이다. 각 지점([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))이 자율적으로 운영하되 본사([Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/)) 레시피와 위생 기준(거버넌스 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/))은 모두 동일하게 따른다.

---

## Ⅲ. 비교 및 연결

<strong>중앙화 레이크 vs <a href="/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/">Data Mesh</a> on <a href="/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/">Lakehouse</a></strong>

| 항목 | 중앙화 레이크 | [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) on [Lakehouse](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) |
|:---|:---|:---|
| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 소유권 | 단일 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 팀 | 각 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀 |
| [파이프](/knowledge-base/studynote/02_operating_system/02_process_thread/123_pipe/)라인 병목 | 중앙 팀 큐 대기 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 자율 배포 |
| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 지식 | 희석 (중앙팀 학습 필요) | 보존 ([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀 직접 구현) |
| 거버넌스 | 강중앙화 (느린 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) 적용) | 연합 (중앙 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) + [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 자율) |
| 스케일 | 조직 성장에 따라 병목 심화 | 수평 확장 가능 |

**연관 개념 연결**

- <strong><a href="/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/">Data Product</a> (012)</strong>: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Mesh의 핵심 계약 단위, Gold 테이블로 구현
- <strong><a href="/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/">Unity Catalog</a> (008)</strong>: 연합 거버넌스의 기술 구현체
- <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/">Data Fabric</a> (014)</strong>: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Mesh가 조직 원칙이라면 [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Fabric은 기술 원칙 중심

> 📢 **섹션 요약 비유**: [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Mesh는 나라(전사)의 헌법(거버넌스)은 공유하되, 각 지방자치단체([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))가 자기 영토를 자율적으로 관리하는 연방제 모델이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

**도입 성공 조건**

- **조직 성숙도**: [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 엔지니어링 역량을 보유하거나 확보할 수 있는지 [확인](/knowledge-base/studynote/04_software_engineering/12_testing_maintenance/396_validation/)
- **플랫폼 표준화**: 모든 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)이 동일한 [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 플랫폼([Databricks](/knowledge-base/studynote/16_bigdata/03_spark/074_photon_engine/)/[Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/))을 사용
- **제품 계약 문화**: Gold 테이블을 공개 인터페이스로 취급하는 팀 문화 정착
- <strong>중앙 <a href="/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/">정책</a> 최소화</strong>: 거버넌스 팀은 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)만 선언하고 집행은 플랫폼에 위임

**기술사 답안 포인트**

| 질문 | 핵심 답변 |
|:---|:---|
| [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) 4원칙 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유권, [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/), 셀프서비스 인프라, 연합 거버넌스 |
| [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 매핑 이유 | [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/) = 연합 거버넌스, Delta 테이블 = [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) |
| 중앙화 대비 단점 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 간 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/) 관리, 공통 용어(Ontology) 표준화 어려움 |
| 성공 전제 조건 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 역량, 셀프서비스 인프라, 플랫폼 표준화 |

> 📢 **섹션 요약 비유**: [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) 도입은 중앙 집중 관료제에서 분권 민주주의로 전환하는 과정이다. 더 많은 자유(자율)는 더 많은 책임([데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) 품질)을 의미한다.

---

## Ⅴ. 기대효과 및 결론

| 효과 | 내용 |
|:---|:---|
| 병목 해소 | 중앙 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 팀 의존성 제거로 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 속도 3~5배 향상 |
| 품질 향상 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 전문 지식 보존으로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 맥락 정확도 향상 |
| 거버넌스 확장 | 조직 성장에 비례하지 않는 거버넌스 오버헤드 |
| [데이터 민주화](/knowledge-base/studynote/16_bigdata/01_intro/010_data_democratization/) | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 직접 [데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/)을 생산·소비하는 문화 정착 |

[Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) on Lakehouse는 수백 개 이상의 [데이터 파이프라인](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/645_data_pipeline_acceleration/)을 운영하는 대규모 조직에서 중앙화 병목을 해소하는 현실적 아키텍처다. 기술사 시험에서는 <strong><a href="/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/">Data Mesh</a> 4원칙</strong>, <strong><a href="/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/">레이크하우스</a>와의 기술 매핑</strong>, <strong>중앙화 vs 연합 거버넌스 트레이드오프</strong>가 핵심 논점이다.

> 📢 **섹션 요약 비유**: [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) on Lakehouse는 공유 주방([레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/) 인프라)이 있는 공동 주택에서, 각 세대([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))가 자기 요리([데이터 제품](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/))를 직접 만들되 주방 위생 규칙([Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/) 거버넌스)은 모두가 따르는 구조다.

---

### 📌 관련 개념 맵

| 개념 | [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 소유권 | [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) 원칙 1 | [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀이 자체 Delta 테이블 소유 |
| [Data Product](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) | [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) 원칙 2 | [SLA](/knowledge-base/studynote/12_it_management/02_itsm_itil/085_sla/)·[스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/) 계약이 있는 Gold 테이블 |
| 셀프서비스 인프라 | [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) 원칙 3 | 표준화 Workflows 템플릿 |
| 연합 거버넌스 | [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/) 원칙 4 | [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/) 중앙 [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/) + [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 자율 |
| [Data Fabric](/knowledge-base/studynote/12_it_management/05_security_compliance/212_data_fabric_virtualization/) | 대비 개념 | 기술 중심 접근 (vs 조직 중심 [Data Mesh](/knowledge-base/studynote/12_it_management/05_security_compliance/320_data_mesh/)) |
| [Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/) | 기술 구현체 | 연합 거버넌스의 단일 제어 지점 |

---

### 📈 관련 키워드 및 발전 흐름도

```text
[중앙 집중 데이터 레이크 (Centralized Data Lake) — 모든 데이터를 한 곳에 수집]
    │
    ▼
[데이터 사일로 문제 (Data Silo) — 팀 간 데이터 접근 병목·거버넌스 공백 발생]
    │
    ▼
[데이터 메시 (Data Mesh) — 도메인 팀이 데이터 제품 소유·서빙하는 분산 아키텍처]
    │
    ▼
[데이터 제품 (Data Product) — 발견 가능·접근 가능·신뢰 가능한 자립 데이터 단위]
    │
    ▼
[연합 거버넌스 (Federated Governance) — 중앙 정책과 도메인 자율성의 균형 유지]
```

이 흐름은 중앙 집중 [데이터 레이크](/knowledge-base/studynote/12_it_management/05_security_compliance/208_data_lake_schema_on_read/)의 한계를 [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/)가 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/) 소유권과 연합 거버넌스로 극복하는 아키텍처 전환을 나타낸다.

### 👶 어린이를 위한 3줄 비유 설명
1. [데이터 메시](/knowledge-base/studynote/12_it_management/05_security_compliance/211_data_mesh_domain_ownership/) [레이크하우스](/knowledge-base/studynote/16_bigdata/07_data_lake/146_lakehouse/)는 각 반([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/))이 자기 교실(Delta 테이블)을 스스로 관리하는 학교예요.
2. 교장 선생님([Unity Catalog](/knowledge-base/studynote/16_bigdata/07_data_lake/150_unity_catalog/))은 학교 전체 규칙만 정하고, 각 반 선생님([도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/) 팀)이 자기 반을 운영해요.
3. 다른 반에서 우리 반 정보를 볼 때는 선생님 허락(접근 제어)을 받아야 하고, 누가 봤는지 기록도 남아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 153 / 262

← **이전**: [152. 메달리온 아키텍처 (Medallion Architecture) — Delta Lake 기반 3계층](/knowledge-base/studynote/16_bigdata/07_data_lake/152_medallion_architecture/)
**다음**: [154. 데이터 제품 (Data Product) — API 인터페이스와 SLA 품질 지표](/knowledge-base/studynote/16_bigdata/07_data_lake/154_data_product/) →

---
