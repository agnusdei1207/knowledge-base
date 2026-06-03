+++
title = "74. 페어 프로그래밍 (Pair Programming) - Driver / Navigator"

[taxonomies]
tags = ["software_engineering"]

[extra]
tags = ["software_engineering"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 페어 프로그래밍은 두 사람이 한 자리에서 함께 코드를 만드는 개발 방식이다.
> 2. **가치**: 품질 향상과 지식 공유에 좋다.
> 3. **판단**: Driver와 Navigator 역할을 분리해 효율을 높인다.

---

## Ⅰ. 개요 및 필요성

혼자 코딩하면 실수를 놓치기 쉽다.

둘이 함께 하면 즉시 검토할 수 있다.

- **📢 섹션 요약 비유**: 한 사람이 운전하고 다른 사람이 길 안내를 하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Driver -> code
Navigator -> review
```

| 역할 | 의미 |
| :-- | :-- |
| Driver | 입력 |
| Navigator | 방향/검토 |

Driver가 타이핑하고 Navigator가 큰 그림과 오류를 본다.

- **📢 섹션 요약 비유**: 운전은 한 사람이, 길 찾기는 다른 사람이 한다.

---

## Ⅲ. 비교 및 연결

| 구분 | Driver | Navigator |
| :-- | :-- | :-- |
| 역할 | 작성 | 검토 |
| 초점 | 구현 | 품질 |

| 효과 | 의미 |
| :-- | :-- |
| Knowledge Sharing | 지식 공유 |
| [Defect](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) Reduction | [결함](/knowledge-base/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 감소 |

페어 프로그래밍은 실시간 리뷰와 학습 효과가 크다.

- **📢 섹션 요약 비유**: 한 명은 손, 한 명은 눈이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 역할을 교대하는가?
2. 리뷰와 작성이 분리되는가?
3. 지식 공유가 되는가?
4. 품질 향상에 도움이 되는가?
5. 과도한 비용을 고려하는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 한 명만 계속 치는 설계
- Navigator가 방관하는 설계
- 형식적 페어링만 하는 설계
- 비용 대비 효과를 무시하는 설계

기술사 관점에서는 페어 프로그래밍을 "실시간 품질 검증과 지식 공유 방식"으로 설명해야 한다.

- **📢 섹션 요약 비유**: 둘이 같이 하니 실수가 줄어든다.

---

## Ⅴ. 기대효과 및 결론

페어 프로그래밍은 품질과 학습 효과를 높인다.

결론적으로 Driver/Navigator 구조를 가진 협업 코딩 방식이다.

- **📢 섹션 요약 비유**: 운전과 길 안내를 나눠 하는 협업이다.

---

## 관련 개념 맵

```text
Pair Programming
  ↓
Driver / Navigator
  ↓
Quality / Sharing
```

---

## 관련 키워드 및 발전 흐름도

```text
XP
  ↓
Pair Programming
  ↓
Collaborative Coding
```

---

## 어린이를 위한 3줄 비유 설명

한 명은 글을 써요.  
한 명은 길을 봐요.  
페어 프로그래밍은 같이 하는 코딩이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 74 / 973

← **이전**: [73. XP (e/Xtreme Programming) - 5가지 가치, 12가지 실천 방법](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/073_xp_extreme_programming/)
**다음**: [75. 공동 코드 소유 (Collective Code Ownership)](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/075_collective_code_ownership/) →

---
