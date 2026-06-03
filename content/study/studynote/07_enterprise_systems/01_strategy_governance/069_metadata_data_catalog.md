+++
title = "69. 메타데이터 (Metadata) 관리 / 데이터 카탈로그 (Data Catalog)"
weight = 69
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[012_metadata|메타데이터]]는 [[001_dikw_pyramid|데이터]]의 구조, 의미, 출처를 설명하는 [[001_dikw_pyramid|데이터]]에 대한 [[001_dikw_pyramid|데이터]]다.
> 2. **가치**: [[213_data_catalog_metadata|데이터 카탈로그]]는 [[012_metadata|메타데이터]]를 모아 검색·탐색·거버넌스를 돕는 포털이다.
> 3. **판단**: [[001_dikw_pyramid|데이터]]가 많을수록 [[012_metadata|메타데이터]]가 있어야 찾고, 믿고, 재사용할 수 있다.

---

## Ⅰ. 개요 및 필요성

[[001_dikw_pyramid|데이터]]가 쌓일수록 "이게 뭐지?"를 설명해 주는 정보가 더 중요해진다. 그 역할을 [[012_metadata|메타데이터]]가 한다.

[[213_data_catalog_metadata|데이터 카탈로그]]는 이런 [[012_metadata|메타데이터]]를 한곳에 모아 사람이 쉽게 찾게 해 준다.

- **📢 섹션 요약 비유**: 도서관의 책 정보 카드와 검색창이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Data Assets
  ↓
Metadata Collection
  ↓
Data Catalog
  ↓
Search / Governance
```

| 구성 요소 | 의미 |
| :-- | :-- |
| [[012_metadata|Metadata]] | [[001_dikw_pyramid|데이터]] 설명 정보 |
| Lineage | 흐름/출처 |
| [[394_catalog_metadata|Catalog]] | 검색 포털 |

[[012_metadata|메타데이터]]는 테이블, 컬럼, 소유자, 품질 규칙, 계보를 담는다. 그래서 [[001_dikw_pyramid|데이터]] 이해와 통제가 쉬워진다.

- **📢 섹션 요약 비유**: 책 제목, 저자, 발행일, 위치를 적은 카드다.

---

## Ⅲ. 비교 및 연결

| 개념 | 초점 | 차이 |
| :-- | :-- | :-- |
| [[012_metadata|Metadata]] | 설명 정보 | [[001_dikw_pyramid|데이터]]의 [[001_dikw_pyramid|데이터]] |
| [[213_data_catalog_metadata|Data Catalog]] | 탐색/검색 | [[012_metadata|메타데이터]] 포털 |
| [[052_data_governance_framework|Data Governance]] | [[164_policy|정책]]/책임 | 관리 체계 |

| 메타정보 | 예 |
| :-- | :-- |
| [[505_schema|Schema]] | 구조 |
| Owner | 책임자 |
| Lineage | 출처 |

[[213_data_catalog_metadata|데이터 카탈로그]]는 단순 목록이 아니라 [[001_dikw_pyramid|데이터]] 자산을 재사용 가능하게 만드는 기반이다.

- **📢 섹션 요약 비유**: 어디에 뭐가 있는지 알면 창고가 도서관이 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. [[012_metadata|메타데이터]]가 자동 수집되는가?
2. 소유자와 계보가 보이는가?
3. 검색과 태깅이 되는가?
4. 품질 정보가 연결되는가?
5. 거버넌스와 연동되는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- [[012_metadata|메타데이터]] 없이 [[001_dikw_pyramid|데이터]]만 쌓는 설계
- [[394_catalog_metadata|카탈로그]]를 [[037_document|문서 저장소]]로만 쓰는 설계
- 소유자와 계보가 없는 설계
- 검색이 안 되는 [[394_catalog_metadata|카탈로그]]

기술사 관점에서는 [[012_metadata|메타데이터]]를 "[[001_dikw_pyramid|데이터]]를 이해하게 해 주는 설명서"로 봐야 한다.

- **📢 섹션 요약 비유**: 이름표가 있어야 물건을 다시 찾을 수 있다.

---

## Ⅴ. 기대효과 및 결론

[[012_metadata|메타데이터]]와 [[213_data_catalog_metadata|데이터 카탈로그]]는 [[001_dikw_pyramid|데이터]] 발견성과 [[642_reliability_mtbf_mttr_mttf_availability|신뢰성]]을 높인다. 그래서 분석과 [[190_ai_llm_requirements_specification|AI]] 활용이 쉬워진다.

결론적으로 [[012_metadata|메타데이터]]는 [[001_dikw_pyramid|데이터]]에 대한 [[001_dikw_pyramid|데이터]]이고, [[213_data_catalog_metadata|데이터 카탈로그]]는 그것을 모으는 포털이다.

- **📢 섹션 요약 비유**: 카드와 검색대가 함께 있어야 찾기가 쉽다.

---

## 관련 개념 맵

```text
Metadata
  ↓
Data Catalog
  ↓
Search / Lineage
  ↓
Data Governance
```

---

## 관련 키워드 및 발전 흐름도

```text
Metadata
  ↓
Data Catalog
  ↓
Data Discovery
  ↓
Data Governance
```

---

## 어린이를 위한 3줄 비유 설명

책 정보가 있어야 찾을 수 있어요.  
그 정보를 모아 놓은 곳이 있어요.  
[[012_metadata|메타데이터]]와 [[213_data_catalog_metadata|데이터 카탈로그]]예요.
