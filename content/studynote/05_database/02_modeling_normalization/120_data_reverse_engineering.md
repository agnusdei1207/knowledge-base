+++
title = "120. 데이터 역공학 (Data Reverse 엔진ering) - 기존 DB에서 ERD·모델 복원"
date = 2026-04-19

[taxonomies]
tags = ["studynote-database"]

[extra]
tags = ["studynote-database"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/)은 <strong>문서 없는 기존 DB의 물리 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/">스키마</a>(테이블·컬럼·<a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a>·FK)를 분석하여 ERD·개념 모델·<a href="/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/">데이터 사전</a>을 복원</strong>하는 프로세스다.
> 2. **가치**: 레거시 시스템은 설계 문서가 분실·미작성된 경우가 많아, [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/) 없이는 <strong>시스템 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/909_asis_update_ea_maintenance_synchronization/">현행화</a>·마이그레이션·리팩터링이 불가능</strong>하다.
> 3. **판단 포인트**: CASE 도구(ERwin·[DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)#)의 자동 [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/) 기능으로 물리 [스키마](/knowledge-base/studynote/05_database/01_db_architecture_relational/005_schema/)를 읽어 ERD를 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)하고, 이후 <strong>수동으로 비즈니스 의미(엔터티명·<a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a> 설명)를 부여</strong>하는 2단계 프로세스가 필요하다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    정공학 vs 역공학                                   |
+-------------------------------------------------------+
|  [정공학 (Forward Engineering)]                       |
|   요구사항 -> ERD -> 릴레이션 -> 물리 DB               |
|                                                       |
|  [역공학 (Reverse Engineering)]                       |
|   물리 DB -> 릴레이션 -> ERD -> 비즈니스 의미 복원      |
|                                                       |
|  활용: 레거시 현행화, 마이그레이션, 문서화             |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 정공학은 설계도를 그려서 건물을 짓는 것이고, [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/)은 이미 지어진 건물을 조사해서 설계도를 복원하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/) 프로세스

| 단계 | 활동 | 산출물 |
|:---|:---|:---|
| **1. 물리 추출** | [DDL](/knowledge-base/studynote/05_database/01_db_architecture_relational/020_ddl/)·[메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 수집 | 테이블·컬럼·FK 목록 |
| <strong>2. <a href="/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/">논리</a> 복원</strong> | FK [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) -> ERD [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | 자동 ERD |
| **3. 의미 부여** | 비즈니스 규칙·엔터티명 | 개념 ERD |
| **4. 문서화** | [데이터 사전](/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/) 작성 | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 표준 문서 |

- **📢 섹션 요약 비유**: [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/)은 완성된 요리를 맛보고 레시피를 추정하는 것이다. 재료(테이블)는 쉽게 알지만, 요리사의 의도(비즈니스 규칙)는 인터뷰가 필요하다.

---

## Ⅲ. 비교 및 연결

| 비교 | 정공학 | [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/) |
|:---|:---|:---|
| **방향** | 개념->물리 | **물리->개념** |
| **시점** | 신규 개발 | <strong>레거시 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/909_asis_update_ea_maintenance_synchronization/">현행화</a></strong> |
| **문서** | [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) | **복원** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/) 도구
- **ERwin**: DB 연결 -> 자동 ERD [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/).
- <strong><a href="/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/">DA</a># (다샵)</strong>: 국내 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 모델링 표준 도구.
- **DBeaver**: 무료 ERD 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 기능.

---

## Ⅴ. 기대효과 및 결론

[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/)은 <strong>레거시 시스템의 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/909_asis_update_ea_maintenance_synchronization/">현행화</a>·클라우드 마이그레이션·<a href="/knowledge-base/studynote/12_it_management/01_governance_strategy/842_data_governance_framework/">데이터 거버넌스</a></strong>의 필수 사전 작업이며, 자동 추출 + 수동 의미 부여의 2단계 접근이 가장 효과적이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **정공학** | [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/)의 반대 방향 (개념->물리) |
| **ERD** | [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/)의 핵심 산출물 |
| <strong><a href="/knowledge-base/studynote/05_database/07_exam_summary/393_data_dictionary/">데이터 사전</a></strong> | [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/)으로 복원하는 [메타데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/012_metadata/) 문서 |
| **CASE 도구** | ERwin, [DA](/knowledge-base/studynote/12_it_management/03_ea_isp/104_da_as_is_analysis/)# 등 자동 [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/) 도구 |
| <strong>레거시 <a href="/knowledge-base/studynote/12_it_management/03_ea_isp/909_asis_update_ea_maintenance_synchronization/">현행화</a></strong> | [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/)의 주요 목적 |

### 📈 관련 키워드 및 발전 흐름도

```text
[수동 DB 문서화 (종이·엑셀, 1990s)]
    |
    v
[CASE 도구 역공학 (ERwin, 2000s) — DDL->ERD 자동 변환]
    |
    v
[메타데이터 관리 (2010s) — 데이터 카탈로그 연동]
    |
    v
[자동 문서화 (dbt docs, 2020s)]
    |
    v
[현재: AI 기반 역공학 — 테이블 관계·비즈니스 의미 자동 추론]
```

### 👶 어린이를 위한 3줄 비유 설명
1. 정공학은 **레시피를 보고 요리를 만드는** 거예요.
2. [역공학](/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/)은 완성된 요리를 **맛보고 레시피를 알아내는** 거예요.
3. 설계도가 없는 옛날 건물(레거시)을 수리하려면 먼저 <strong>설계도를 복원(<a href="/knowledge-base/studynote/04_software_engineering/01_overview_principles/029_reverse_engineering/">역공학</a>)</strong>해야 한답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 120 / 600

<- **이전**: [119. 팩트 테이블과 디멘전 테이블 (Fact & Dimension Table) - DW 스타 스키마 핵심 구성 요소](/knowledge-base/studynote/05_database/02_modeling_normalization/119_fact_table_dimension_table/)
**다음**: [121. 데이터 아키텍처 프레임워크 (Zachman Framework) - 엔터프라이즈 데이터 설계 체계](/knowledge-base/studynote/05_database/02_modeling_normalization/121_data_architecture_framework_zachman/) ->

---
