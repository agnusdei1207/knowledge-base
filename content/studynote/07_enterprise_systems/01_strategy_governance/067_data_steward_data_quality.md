---
title: 67. 데이터 스튜어드 (Data Steward) - 실무 부서 데이터 품질 관리 책임자
tags:
- enterprise_systems
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[001_dikw_pyramid|데이터]] 스튜어드는 현업 부서의 [[001_dikw_pyramid|데이터]] 품질과 정의를 실무적으로 책임지는 역할이다.
> 2. **가치**: [[001_dikw_pyramid|데이터]] 오너와 함께 거버넌스를 현실에 적용하게 만드는 핵심 실행자다.
> 3. **판단**: [[001_dikw_pyramid|데이터]] 품질은 IT만의 일이 아니므로 현업 책임과 운영 규칙이 함께 있어야 한다.

---

## Ⅰ. 개요 및 필요성

[[052_data_governance_framework|데이터 거버넌스]]는 [[164_policy|정책]]만으로 끝나지 않는다. 현업 [[001_dikw_pyramid|데이터]]가 실제로 만들어지고 수정되는 자리에서 품질을 관리해야 한다.

그 역할이 [[001_dikw_pyramid|데이터]] 스튜어드다.

- **📢 섹션 요약 비유**: 쓰는 사람 옆에서 정리와 규칙을 챙겨 주는 집사다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Business Data
  ↓
Data Steward
  ↓
Quality Rules
  ↓
Trusted Data
```

| 역할 | 의미 |
| :-- | :-- |
| [[200_data_owner|Data Owner]] | 최종 책임 |
| [[001_dikw_pyramid|Data]] Steward | 현업 품질 운영 |
| [[001_dikw_pyramid|Data]] Custodian | 기술 보관/운영 |

[[001_dikw_pyramid|데이터]] 스튜어드는 코드값, 용어, 품질 규칙, 변경 절차를 현장에서 관리한다.

- **📢 섹션 요약 비유**: 책상 위 물건이 어디에 놓여야 하는지 챙기는 사람이다.

---

## Ⅲ. 비교 및 연결

| 역할 | 초점 | 차이 |
| :-- | :-- | :-- |
| [[200_data_owner|Data Owner]] | 책임/승인 | [[164_policy|정책]] |
| [[001_dikw_pyramid|Data]] Steward | 품질 운영 | 현업 실무 |
| [[001_dikw_pyramid|Data]] Custodian | 시스템 관리 | IT |

| 관리 대상 | 예 |
| :-- | :-- |
| 코드값 | 표준화 |
| 정의 | 통일 |
| 이력 | 추적 |

스튜어드가 있어야 [[052_data_governance_framework|데이터 거버넌스]]가 조직 전체에서 실제로 작동한다.

- **📢 섹션 요약 비유**: 규칙을 쓰는 사람과, 현장에서 지키게 하는 사람이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 현업에 스튜어드가 지정되어 있는가?
2. 품질 규칙이 운영되는가?
3. 오너/스튜어드/보관 책임이 구분되는가?
4. 코드값과 용어가 표준화되는가?
5. 변경 승인 절차가 있는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- IT만으로 품질을 책임지려는 설계
- 스튜어드 역할 없이 규칙만 만드는 설계
- 권한과 책임이 없는 설계
- 품질 이슈를 방치하는 설계

기술사 관점에서는 [[001_dikw_pyramid|데이터]] 스튜어드를 "현업 품질 책임자"로 설명해야 한다.

- **📢 섹션 요약 비유**: 정리 담당이 있어야 방이 계속 깨끗하다.

---

## Ⅴ. 기대효과 및 결론

[[001_dikw_pyramid|데이터]] 스튜어드가 있으면 품질과 정의가 현업에서 지속 관리된다. 그래서 [[001_dikw_pyramid|데이터]] [[085_confidence_association_rule_conditional_probability|신뢰도]]가 높아진다.

결론적으로 [[001_dikw_pyramid|데이터]] 스튜어드는 현업 [[001_dikw_pyramid|데이터]] 품질의 실행 책임자다.

- **📢 섹션 요약 비유**: 정리하는 사람이 있으면 물건이 늘 제자리에 있다.

---

## 관련 개념 맵

```text
Data Owner
  ↓
Data Steward
  ↓
Data Quality
  ↓
Data Governance
```

---

## 관련 키워드 및 발전 흐름도

```text
Data Governance
  ↓
Data Steward
  ↓
Quality Rules
  ↓
Trusted Data
```

---

## 어린이를 위한 3줄 비유 설명

정리하는 사람이 따로 있어요.  
그 사람이 물건을 바로잡아요.  
[[001_dikw_pyramid|데이터]] 스튜어드는 그런 사람예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 67 / 482

← **이전**: [[066_data_governance_framework|66. 데이터 거버넌스 (Data Governance) - 데이터 품질, 보안, 프라이버시 전사 관리 체계]]
**다음**: [[068_cdo_cio_role_separation_governance|68. CDO (Chief Data Officer) / CIO (Chief Information Officer) 역할 분리]] →

---
