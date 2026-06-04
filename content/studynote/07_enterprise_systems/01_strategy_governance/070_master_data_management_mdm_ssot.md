+++
title = "70. 마스터 데이터 관리 (MDM, Master Data Management) - 전사 공통 기준정보 단일화 (Single Source of Truth)"

[taxonomies]
tags = ["enterprise_systems"]

[extra]
tags = ["enterprise_systems"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MDM은 고객, 제품, 조직 같은 핵심 기준정보를 전사적으로 일관되게 관리하는 체계다.
> 2. **가치**: 중복과 불일치를 줄여 [Single Source of Truth](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/119_gitops_single_source_of_truth/)(SSOT)를 만든다.
> 3. **판단**: [마스터 데이터](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/)가 [분산](/knowledge-base/studynote/08_algorithm_stats/08_stats/136_variance/)되면 보고·분석·운영이 모두 흔들린다.

---

## Ⅰ. 개요 및 필요성

회사 안에 같은 고객 정보가 여러 [버전](/knowledge-base/studynote/03_network/06_network_layer_ip/288_version_ihl_tos_total_length/)으로 있으면 문제가 생긴다. MDM은 이를 하나로 맞추는 작업이다.

그래서 대기업과 멀티 시스템 환경에서 중요하다.

- **📢 섹션 요약 비유**: 같은 주소를 모두 같은 이름표로 맞춰 두는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Source Systems
  ↓
Master Data Hub
  ↓
Golden Record
  ↓
SSOT
```

| 요소 | 의미 |
| :-- | :-- |
| Master [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | 기준정보 |
| Golden Record | 통합된 정본 |
| SSOT | 단일 진실 स्रोत |

MDM은 중복을 제거하고 규칙에 따라 하나의 정본을 만든다. 그래서 시스템 간 충돌이 줄어든다.

- **📢 섹션 요약 비유**: 여러 장의 신분증을 하나의 정식 신분증으로 합치는 것이다.

---

## Ⅲ. 비교 및 연결

| 개념 | 초점 | 차이 |
| :-- | :-- | :-- |
| [MDM](/knowledge-base/studynote/05_database/07_exam_summary/539_mdm_master_data_management/) | 기준정보 통합 | 운영/분석 공통 |
| [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) | 설명 정보 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| [Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | 검색/탐색 | 찾기 중심 |

| 대상 | 예 |
| :-- | :-- |
| [C고객](/knowledge-base/studynote/12_it_management/01_governance_strategy/026_three_c_analysis/) | 고객 |
| Product | 제품 |
| Org | 조직 |

MDM은 단순 저장이 아니라 정합성과 책임을 함께 관리하는 체계다.

- **📢 섹션 요약 비유**: 모두가 같은 이름으로 부르도록 통일하는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 기준정보 [도메인](/knowledge-base/studynote/05_database/02_modeling_normalization/064_relation_domain/)이 정의되었는가?
2. Golden Record 규칙이 있는가?
3. 소스 시스템 간 충돌 해결이 있는가?
4. [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 책임자가 있는가?
5. SSOT가 운영되는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 각 시스템이 제각각 기준정보를 관리하는 설계
- 정본 규칙 없이 중복만 합치는 설계
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 품질 책임이 없는 설계
- MDM을 단순 [마스](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/172_maas_mobility_as_a_service/)터 테이블로 보는 설계

기술사 관점에서는 MDM을 "전사 기준정보의 단일화 체계"로 설명해야 한다.

- **📢 섹션 요약 비유**: 전화번호부를 한 권으로 맞추는 일이다.

---

## Ⅴ. 기대효과 및 결론

MDM은 고객/제품/조직 정보를 통합해 업무 [일관성](/knowledge-base/studynote/05_database/04_transactions_concurrency/194_consistency_database_integrity/)과 분석 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 높인다.

결론적으로 MDM은 전사 기준정보를 하나로 관리하는 체계다.

- **📢 섹션 요약 비유**: 모두가 같은 명단을 보는 것이다.

---

## 관련 개념 맵

```text
Master Data
  ↓
MDM
  ↓
Golden Record
  ↓
SSOT
```

---

## 관련 키워드 및 발전 흐름도

```text
Master Data
  ↓
MDM
  ↓
Data Quality
  ↓
SSOT
```

---

## 어린이를 위한 3줄 비유 설명

같은 이름표를 모두 하나로 맞춰요.
그래야 헷갈리지 않아요.
MDM은 그런 정리예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 70 / 482

← **이전**: [69. 메타데이터 (Metadata) 관리 / 데이터 카탈로그 (Data Catalog)](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/069_metadata_data_catalog/)
**다음**: [71. 디지털 트랜스포메이션 (DX / DT, Digital Transformation) - AI, 클라우드, 빅데이터로 비즈니스 모델](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/071_digital_transformation_dx/) →

---
