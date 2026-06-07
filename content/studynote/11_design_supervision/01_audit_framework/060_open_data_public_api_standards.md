---
title: "060. Open Data Public Api Standards"
date: "2026-04-10"
tags:
  - "studynote-design-supervision"
weight: 60
---
## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 공공데이터 개방은 사람이 읽는 문서가 아니라 기계가 바로 활용할 수 있는 표준 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)와 API를 제공하는 것이다.
> 2. **가치**: CSV, [JSON](/studynote/11_design_supervision/06_exam_summary/343_json/), [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/), LOD(Linked Open [Data](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/))로 개방하면 민간 서비스와 연계가 쉬워진다.
> 3. **판단 포인트**: [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 필터링, [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/), 코드 표준화, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 분리, 현행화가 감리 핵심이다.

---

## Ⅰ. 개요 및 필요성

공공데이터는 시민과 기업이 다시 활용할 수 있어야 의미가 있다. PDF나 HWP처럼 사람이 보기만 좋은 형태는 개방 효과가 낮다.

그래서 감리에서는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 얼마나 기계 친화적으로 공개되는지, 그리고 민간 서비스가 안전하게 붙을 수 있는지를 본다.

- **📢 섹션 요약 비유**: 요리 재료를 포장 상자째 주는 것이 아니라, 바로 요리할 수 있게 손질해 주는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

공공데이터 개방은 단순 업로드가 아니라 포맷, [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/), [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/), 보안, 현행화가 함께 맞아야 한다.

```text
공공기관 DB
   v
정제 / 비식별화
   v
표준 포맷(CSV/JSON)
   v
REST API / LOD
```

| 항목 | 의미 |
| :-- | :-- |
| CSV/[JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) | 기계가 읽기 쉬운 표준 포맷 |
| [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) | 실시간 조회 가능한 인터페이스 |
| LOD | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 간 의미적 연결 |
| [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/) | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 설명서와 검색 정보 |

공공데이터는 5-Star 모델로도 설명할 수 있다. [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 개방에서 시작해, API와 링크드 오픈 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)로 갈수록 개방 수준이 높아진다.

- **📢 섹션 요약 비유**: 서랍에 넣어 두는 것보다, 라벨을 붙여 정리장에 올려 두는 것이 훨씬 [쓰기](/studynote/13_cloud_architecture/05_data_engineering/289_cqrs_db/) 쉽다.

---

## Ⅲ. 비교 및 연결

| 단계 | 특징 | [감리 관점](/studynote/11_design_supervision/01_audit_framework/008_audit_perspective/) |
| :-- | :-- | :-- |
| [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 업로드 | 사람이 보기 쉬움 | 미흡 |
| CSV/[JSON](/studynote/11_design_supervision/06_exam_summary/343_json/) | 기계 친화적 | 기본 권장 |
| [REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) | 실시간 연계 가능 | 우수 |
| LOD | [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 연결성 최고 | 고도화 |

개방 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 단순 공개가 아니라 상호운용성의 문제다. 코드값 표준화, [개인정보 비식별화](/studynote/16_bigdata/13_intro_trends/251_data_anonymization/), [인증](/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/)/[인가](/studynote/04_software_engineering/08_security_compliance_devsecops/509_authorization_models_rbac_abac/) 정책이 맞아야 실제 활용이 가능하다.

- **📢 섹션 요약 비유**: 같은 언어를 써야 서로 다른 나라의 사람들도 대화할 수 있는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

감리에서는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)셋 선정, [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 설계, [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/), 보안, 현행화를 함께 점검해야 한다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/)와 비공개 정보가 제거되었는가?
2. CSV/[JSON](/studynote/11_design_supervision/06_exam_summary/343_json/)/[REST API](/studynote/03_network/09_application_layer_web_email/477_rest_api_architecture/) 등 표준 포맷인가?
3. 공공 표준 코드와 [메타데이터](/studynote/05_database/01_db_architecture_relational/012_metadata/)가 있는가?
4. [API](/studynote/02_operating_system/01_overview_architecture/014_api_posix/) 게이트웨이와 별도 개방망이 있는가?
5. [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 배치/실시간으로 현행화되는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- PDF나 HWP만 올려놓고 개방했다고 하는 설계
- [개인정보](/studynote/09_security/16_data_privacy/781_personal_information/) 필터링 없이 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 배포하는 설계
- 운영 DB와 동일한 경로로 외부에 직접 노출하는 설계

- **📢 섹션 요약 비유**: 문만 열어 두고 정작 표지판이 없으면 손님은 아무것도 못 찾는다.

---

## Ⅴ. 기대효과 및 결론

공공데이터 개방은 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경제의 기반이다. 표준 규격이 잘 맞으면 민간은 빠르게 서비스를 만들 수 있고, 공공은 반복 개발을 줄일 수 있다.

결국 개방의 핵심은 "열었다"가 아니라 "바로 쓸 수 있다"다.

- **📢 섹션 요약 비유**: 텃밭에서 채소를 그냥 던져 주는 게 아니라, 씻고 손질해 바로 요리할 수 있게 내어 주는 것이다.

---

## 관련 개념 맵

```text
공공 DB
   v
정제 / 비식별화
   v
표준 포맷 / API
   v
민간 서비스 활용
```

---

## 관련 키워드 및 발전 흐름도

```text
파일 공개
   v
CSV / JSON
   v
REST API
   v
LOD / 데이터 생태계
```

---

## 어린이를 위한 3줄 비유 설명

공공데이터는 모두가 같이 쓸 수 있게 나누는 정보예요.
보기만 좋은 종이보다, 바로 쓸 수 있는 형태가 더 좋아요.
그래야 여러 앱이 쉽게 만들어질 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 91 / 530

<- **이전**: [59. 보안 장비 정책 룰셋 최적화 상태 점검 (Security Device Ruleset Audit)](/studynote/11_design_supervision/01_audit_framework/631_security_device_ruleset_audit/)
**다음**: [61. 재해 복구 (DR) 모의 훈련 참관 - RTO/RPO 달성 점검](/studynote/11_design_supervision/01_audit_framework/061_dr_mock_drill_rto_rpo_audit/) ->

---
