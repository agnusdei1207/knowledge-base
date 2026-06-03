+++
title = "69. 메타데이터 (Metadata) 관리 / 데이터 카탈로그 (Data Catalog)"

[taxonomies]
tags = ["enterprise_systems"]

[extra]
tags = ["enterprise_systems"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 구조, 의미, 출처를 설명하는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 대한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)다.
> 2. **가치**: [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 모아 검색·탐색·거버넌스를 돕는 포털이다.
> 3. **판단**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 많을수록 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)가 있어야 찾고, 믿고, 재사용할 수 있다.

---

## Ⅰ. 개요 및 필요성

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 쌓일수록 "이게 뭐지?"를 설명해 주는 정보가 더 중요해진다. 그 역할을 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)가 한다.

[데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 이런 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 한곳에 모아 사람이 쉽게 찾게 해 준다.

- **📢 섹션 요약 비유**: 도서관의 책 정보 카드와 검색창이다.

---

## Ⅱ. 아키텍처 및 핵심 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Data Assets</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Metadata Collection</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Data Catalog</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Search / Governance</div>
</div>
</div>



| 구성 요소 | 의미 |
| :-- | :-- |
| [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 설명 정보 |
| Lineage | 흐름/출처 |
| [Catalog](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/) | 검색 포털 |

[메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)는 테이블, 컬럼, 소유자, 품질 규칙, 계보를 담는다. 그래서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 이해와 통제가 쉬워진다.

- **📢 섹션 요약 비유**: 책 제목, 저자, 발행일, 위치를 적은 카드다.

---

## Ⅲ. 비교 및 연결

| 개념 | 초점 | 차이 |
| :-- | :-- | :-- |
| [Metadata](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) | 설명 정보 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) |
| [Data Catalog](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/) | 탐색/검색 | [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 포털 |
| [Data Governance](/knowledge-base/studynote/12_it_management/01_governance_strategy/052_data_governance_framework/) | [정책](/knowledge-base/studynote/10_ai/02_dl_architecture_new/164_policy/)/책임 | 관리 체계 |

| 메타정보 | 예 |
| :-- | :-- |
| [Schema](/knowledge-base/studynote/05_database/04_transactions_concurrency/505_schema/) | 구조 |
| Owner | 책임자 |
| Lineage | 출처 |

[데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 단순 목록이 아니라 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 자산을 재사용 가능하게 만드는 기반이다.

- **📢 섹션 요약 비유**: 어디에 뭐가 있는지 알면 창고가 도서관이 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)가 자동 수집되는가?
2. 소유자와 계보가 보이는가?
3. 검색과 태깅이 되는가?
4. 품질 정보가 연결되는가?
5. 거버넌스와 연동되는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 없이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)만 쌓는 설계
- [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)를 [문서 저장소](/knowledge-base/studynote/14_data_engineering/01_infrastructure/037_document/)로만 쓰는 설계
- 소유자와 계보가 없는 설계
- 검색이 안 되는 [카탈로그](/knowledge-base/studynote/05_database/07_exam_summary/394_catalog_metadata/)

기술사 관점에서는 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)를 "[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 이해하게 해 주는 설명서"로 봐야 한다.

- **📢 섹션 요약 비유**: 이름표가 있어야 물건을 다시 찾을 수 있다.

---

## Ⅴ. 기대효과 및 결론

[메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)와 [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 발견성과 [신뢰성](/knowledge-base/studynote/04_software_engineering/10_trends_pm_quality/642_reliability_mtbf_mttr_mttf_availability/)을 높인다. 그래서 분석과 [AI](/knowledge-base/studynote/04_software_engineering/03_design_architecture/190_ai_llm_requirements_specification/) 활용이 쉬워진다.

결론적으로 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 대한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)이고, [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)는 그것을 모으는 포털이다.

- **📢 섹션 요약 비유**: 카드와 검색대가 함께 있어야 찾기가 쉽다.

---

## 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Metadata</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Data Catalog</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Search / Lineage</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Data Governance</div>
</div>
</div>



---

## 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Metadata</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Data Catalog</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Data Discovery</div>
<div class="kb-diagram-connector">↓</div>
<div class="kb-diagram-note">Data Governance</div>
</div>
</div>



---

## 어린이를 위한 3줄 비유 설명

책 정보가 있어야 찾을 수 있어요.  
그 정보를 모아 놓은 곳이 있어요.  
[메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/)와 [데이터 카탈로그](/knowledge-base/studynote/12_it_management/05_security_compliance/213_data_catalog_metadata/)예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 69 / 482

← **이전**: [68. CDO (Chief Data Officer) / CIO (Chief Information Officer) 역할 분리](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/068_cdo_cio_role_separation_governance/)
**다음**: [70. 마스터 데이터 관리 (MDM, Master Data Management) - 전사 공통 기준정보 단일화 (Single Source](/knowledge-base/studynote/07_enterprise_systems/01_strategy_governance/070_master_data_management_mdm_ssot/) →

---
