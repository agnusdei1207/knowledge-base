---
title: 70. 스프린트 리뷰 (Sprint Review) - 데모 및 피드백
tags:
- software_engineering
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[067_sprint_timebox|스프린트]] 리뷰는 완성된 증분을 [[173_stakeholder_identification_impact_matrix|이해관계자]]에게 데모하고 피드백을 받는 이벤트다.
> 2. **가치**: 제품 방향을 [[395_verification_process_review|검증]]하고 다음 [[067_sprint_timebox|스프린트]]의 학습 재료를 얻는다.
> 3. **판단**: PPT가 아니라 실제 작동 소프트웨어를 보여 주는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

[[067_sprint_timebox|스프린트]]가 끝나면 결과를 공개해야 한다. 리뷰는 그 [[395_verification_process_review|검증]]의 시간이다.

실제 동작하는 소프트웨어를 보는 것이 가장 중요하다.

- **📢 섹션 요약 비유**: 시험 끝나고 답안이 아니라 실제 작품을 보여 주는 시간이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Increment
  ↓ demo
Sprint Review
  ↓
Feedback / Validation
```

| 요소 | 의미 |
| :-- | :-- |
| Increment | 완성 결과 |
| Demo | 실제 시연 |
| Feedback | 피드백 |

리뷰는 시연과 [[395_verification_process_review|검증]]이 중심이다. [[173_stakeholder_identification_impact_matrix|이해관계자]]의 반응을 통해 제품 방향을 조정한다.

- **📢 섹션 요약 비유**: 만든 것을 직접 보여 주고, 보는 사람이 의견을 주는 자리다.

---

## Ⅲ. 비교 및 연결

| 이벤트 | 목적 | 차이 |
| :-- | :-- | :-- |
| [[067_sprint_timebox|Sprint]] [[153_requirements_review_inspection_walkthrough|Review]] | [[395_verification_process_review|검증]]/피드백 | 외부 중심 |
| [[796_retrospective|Retrospective]] | 개선 | 내부 중심 |
| Planning | 계획 | 시작 단계 |

| 산출물 | 의미 |
| :-- | :-- |
| Feedback | 학습 재료 |
| [[066_product_backlog_grooming|Product Backlog]] Update | 다음 작업 반영 |

리뷰는 단순 발표가 아니라 실제 제품 [[395_verification_process_review|검증]]이다. 그래서 데모 품질과 피드백 수집이 중요하다.

- **📢 섹션 요약 비유**: 작품 전시회에서 관객 반응을 보는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. 실제 작동 결과를 보여 주는가?
2. [[173_stakeholder_identification_impact_matrix|이해관계자]] 피드백을 받는가?
3. 백로그에 반영하는가?
4. 데모가 PPT 중심으로 흐르지 않는가?
5. 결과와 학습이 연결되는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 슬라이드만 보여 주는 설계
- 피드백을 기록하지 않는 설계
- 리뷰를 형식적으로만 하는 설계
- [[173_stakeholder_identification_impact_matrix|이해관계자]] 참여가 없는 설계

기술사 관점에서는 리뷰를 "실행 결과 [[395_verification_process_review|검증]]과 제품 학습의 장"으로 봐야 한다.

- **📢 섹션 요약 비유**: 결과를 보여 주고 다음 길을 찾는 자리다.

---

## Ⅴ. 기대효과 및 결론

[[067_sprint_timebox|스프린트]] 리뷰는 제품을 더 나은 방향으로 가게 만드는 피드백 루프다.

결론적으로 [[067_sprint_timebox|스프린트]] 리뷰는 데모와 피드백을 통해 제품 가치를 [[395_verification_process_review|검증]]하는 자리다.

- **📢 섹션 요약 비유**: 보여 주고, 듣고, 다음을 고치는 시간이다.

---

## 관련 개념 맵

```text
Increment
  ↓
Sprint Review
  ↓
Feedback
  ↓
Backlog Update
```

---

## 관련 키워드 및 발전 흐름도

```text
Demo
  ↓
Sprint Review
  ↓
Feedback
  ↓
Product Learning
```

---

## 어린이를 위한 3줄 비유 설명

만든 걸 직접 보여 줘요.  
본 사람이 의견을 말해 줘요.  
[[067_sprint_timebox|스프린트]] 리뷰는 그런 시간이예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 70 / 973

← **이전**: [[069_daily_standup_scrum|69. 데일리 스탠드업 (Daily Scrum) - 진행 상황 공유, 장애 파악]]
**다음**: [[071_sprint_retrospective|71. 스프린트 회고 (Sprint Retrospective) - 프로세스 개선]] →

---
