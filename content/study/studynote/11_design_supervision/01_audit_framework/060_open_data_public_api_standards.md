+++
weight = 60
title = "60. 공공데이터 개방 (Open Data) 표준 규격 및 감리"
date = "2026-04-10"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 공공데이터 개방은 사람이 읽는 문서가 아니라 기계가 바로 활용할 수 있는 표준 [[001_dikw_pyramid|데이터]]와 API를 제공하는 것이다.
> 2. **가치**: CSV, [[343_json|JSON]], [[477_rest_api_architecture|REST API]], LOD(Linked Open [[001_dikw_pyramid|Data]])로 개방하면 민간 서비스와 연계가 쉬워진다.
> 3. **판단 포인트**: [[781_personal_information|개인정보]] 필터링, [[012_metadata|메타데이터]], 코드 표준화, [[014_api_posix|API]] 분리, 현행화가 감리 핵심이다.

---

## Ⅰ. 개요 및 필요성

공공데이터는 시민과 기업이 다시 활용할 수 있어야 의미가 있다. PDF나 HWP처럼 사람이 보기만 좋은 형태는 개방 효과가 낮다.

그래서 감리에서는 [[001_dikw_pyramid|데이터]]가 얼마나 기계 친화적으로 공개되는지, 그리고 민간 서비스가 안전하게 붙을 수 있는지를 본다.

- **📢 섹션 요약 비유**: 요리 재료를 포장 상자째 주는 것이 아니라, 바로 요리할 수 있게 손질해 주는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

공공데이터 개방은 단순 업로드가 아니라 포맷, [[012_metadata|메타데이터]], [[014_api_posix|API]], 보안, 현행화가 함께 맞아야 한다.

```text
공공기관 DB
   ↓
정제 / 비식별화
   ↓
표준 포맷(CSV/JSON)
   ↓
REST API / LOD
```

| 항목 | 의미 |
| :-- | :-- |
| CSV/[[343_json|JSON]] | 기계가 읽기 쉬운 표준 포맷 |
| [[477_rest_api_architecture|REST API]] | 실시간 조회 가능한 인터페이스 |
| LOD | [[001_dikw_pyramid|데이터]] 간 의미적 연결 |
| [[012_metadata|메타데이터]] | [[001_dikw_pyramid|데이터]] 설명서와 검색 정보 |

공공데이터는 5-Star 모델로도 설명할 수 있다. [[501_file_definition_logical_record|파일]] 개방에서 시작해, API와 링크드 오픈 [[001_dikw_pyramid|데이터]]로 갈수록 개방 수준이 높아진다.

- **📢 섹션 요약 비유**: 서랍에 넣어 두는 것보다, 라벨을 붙여 정리장에 올려 두는 것이 훨씬 [[289_cqrs_db|쓰기]] 쉽다.

---

## Ⅲ. 비교 및 연결

| 단계 | 특징 | [[008_audit_perspective|감리 관점]] |
| :-- | :-- | :-- |
| [[501_file_definition_logical_record|파일]] 업로드 | 사람이 보기 쉬움 | 미흡 |
| CSV/[[343_json|JSON]] | 기계 친화적 | 기본 권장 |
| [[477_rest_api_architecture|REST API]] | 실시간 연계 가능 | 우수 |
| LOD | [[001_dikw_pyramid|데이터]] 연결성 최고 | 고도화 |

개방 [[001_dikw_pyramid|데이터]]는 단순 공개가 아니라 상호운용성의 문제다. 코드값 표준화, [[251_data_anonymization|개인정보 비식별화]], [[303_authentication_authorization_patterns|인증]]/[[509_authorization_models_rbac_abac|인가]] 정책이 맞아야 실제 활용이 가능하다.

- **📢 섹션 요약 비유**: 같은 언어를 써야 서로 다른 나라의 사람들도 대화할 수 있는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

감리에서는 [[001_dikw_pyramid|데이터]]셋 선정, [[014_api_posix|API]] 설계, [[282_performance_tactics|성능]], 보안, 현행화를 함께 점검해야 한다.

### [[435_checklist_based_testing|체크리스트]]

1. [[781_personal_information|개인정보]]와 비공개 정보가 제거되었는가?
2. CSV/[[343_json|JSON]]/[[477_rest_api_architecture|REST API]] 등 표준 포맷인가?
3. 공공 표준 코드와 [[012_metadata|메타데이터]]가 있는가?
4. [[014_api_posix|API]] 게이트웨이와 별도 개방망이 있는가?
5. [[001_dikw_pyramid|데이터]]가 배치/실시간으로 현행화되는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- PDF나 HWP만 올려놓고 개방했다고 하는 설계
- [[781_personal_information|개인정보]] 필터링 없이 [[001_dikw_pyramid|데이터]]를 배포하는 설계
- 운영 DB와 동일한 경로로 외부에 직접 노출하는 설계

- **📢 섹션 요약 비유**: 문만 열어 두고 정작 표지판이 없으면 손님은 아무것도 못 찾는다.

---

## Ⅴ. 기대효과 및 결론

공공데이터 개방은 [[001_dikw_pyramid|데이터]] 경제의 기반이다. 표준 규격이 잘 맞으면 민간은 빠르게 서비스를 만들 수 있고, 공공은 반복 개발을 줄일 수 있다.

결국 개방의 핵심은 "열었다"가 아니라 "바로 쓸 수 있다"다.

- **📢 섹션 요약 비유**: 텃밭에서 채소를 그냥 던져 주는 게 아니라, 씻고 손질해 바로 요리할 수 있게 내어 주는 것이다.

---

## 관련 개념 맵

```text
공공 DB
   ↓
정제 / 비식별화
   ↓
표준 포맷 / API
   ↓
민간 서비스 활용
```

---

## 관련 키워드 및 발전 흐름도

```text
파일 공개
   ↓
CSV / JSON
   ↓
REST API
   ↓
LOD / 데이터 생태계
```

---

## 어린이를 위한 3줄 비유 설명

공공데이터는 모두가 같이 쓸 수 있게 나누는 정보예요.  
보기만 좋은 종이보다, 바로 쓸 수 있는 형태가 더 좋아요.  
그래야 여러 앱이 쉽게 만들어질 수 있어요.
