---
title: "66. 제품 백로그 (Product Backlog) - 요구사항 우선순위 목록"
tags:
  - "software_engineering"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 제품 백로그(Product Backlog)는 제품에 필요한 기능, [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 수정, [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/), 개선 항목을 우선순위로 정리한 단일 목록이다.
> 2. **가치**: 백로그 그루밍(Grooming, Refinement)을 통해 요구사항을 작게 쪼개고 우선순위를 지속적으로 조정할 수 있다.
> 3. **판단**: 백로그는 한 번 만드는 문서가 아니라, 제품 가치와 시장 변화에 따라 계속 살아 움직이는 리스트다.

---

## Ⅰ. 개요 및 필요성

애자일에서는 모든 요구를 한 번에 다 만들 수 없다. 그래서 무엇을 먼저 할지 정리한 백로그가 필요하다.

백로그 그루밍은 이 목록을 점검하고, 크기를 조정하고, 우선순위를 정리하는 활동이다.

- **📢 섹션 요약 비유**: 장바구니에 물건을 넣되, 먼저 살 것과 나중에 살 것을 구분하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Ideas / Bugs / Enhancements
  v
Product Backlog
  v
Refinement / Grooming
  v
Sprint Planning
```

| 항목 | 역할 |
| :-- | :-- |
| Feature | 새 기능 |
| Bug | [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/) 수정 |
| [Technical Debt](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/) | 내부 품질 개선 |
| Priority | 순서 결정 |

제품 백로그는 PO(Product Owner)가 책임지고 관리한다. 팀은 이 목록을 바탕으로 [스프린트](/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/)에 들어갈 일을 결정한다.

- **📢 섹션 요약 비유**: 냉장고 속 재료를 언제 꺼내 쓸지 정리한 메모장이다.

---

## Ⅲ. 비교 및 연결

| 개념 | 의미 | 차이 |
| :-- | :-- | :-- |
| Backlog | 전체 요구 목록 | 상위 목록 |
| [Sprint](/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) Backlog | 이번 [스프린트](/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) 작업 | 단기 실행 목록 |
| Roadmap | 장기 제품 계획 | 시간 축 중심 |

| 활동 | 역할 |
| :-- | :-- |
| Grooming / Refinement | 항목 정리, 크기 조정, 우선순위 갱신 |
| Estimation | 작업 크기 추정 |
| Prioritization | 가치 순서 결정 |

제품 백로그는 목록 자체보다 관리 방식이 중요하다. 제대로 관리되지 않으면 우선순위가 흔들리고 팀도 혼란스러워진다.

- **📢 섹션 요약 비유**: 할 일 목록이 너무 길어지면, 다시 정리해 줄 사람이 필요하다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 백로그가 하나의 기준 목록으로 유지되는가?
2. 항목이 작고 명확하게 쪼개졌는가?
3. 우선순위가 비즈니스 가치와 연결되는가?
4. 추정과 검토가 정기적으로 이뤄지는가?
5. [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)와 [결함](/studynote/04_software_engineering/06_software_architecture/352_defect_definition/)도 포함되는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 백로그가 회의 때마다 뒤집히는 설계
- 큰 요구사항을 쪼개지 않는 설계
- 개발팀이 우선순위를 임의로 바꾸는 설계
- [기술 부채](/studynote/12_it_management/02_itsm_itil/100_technical_debt_monitoring_release_policy/)를 백로그에서 빼는 설계

기술사 관점에서는 제품 백로그를 "문서"가 아니라 "의사결정 도구"로 봐야 한다. 그루밍은 백로그를 살아 있게 만드는 과정이다.

- **📢 섹션 요약 비유**: 장바구니를 정리하지 않으면 무엇을 먼저 사야 할지 모르게 된다.

---

## Ⅴ. 기대효과 및 결론

백로그를 잘 관리하면 제품의 방향이 분명해지고, [스프린트](/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/)도 더 예측 가능해진다.

결론적으로 제품 백로그는 요구사항을 우선순위로 관리하는 살아 있는 목록이다.

- **📢 섹션 요약 비유**: 먹을 것, 고칠 것, 바꿀 것을 한 줄로 잘 정리해 둔 목록이다.

---

## 관련 개념 맵

```text
Product Vision
  v
Product Backlog
  v
Grooming / Refinement
  v
Sprint Planning
```

---

## 관련 키워드 및 발전 흐름도

```text
요구사항 수집
  v
제품 백로그
  v
그루밍
  v
스프린트 계획
```

---

## 어린이를 위한 3줄 비유 설명

해야 할 일을 한 상자에 다 넣어요.
먼저 할 것부터 정해요.
제품 백로그는 그런 정리표예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 66 / 973

<- **이전**: [65. 개발 팀 (Development Team) - 자기 조직화, 다기능 팀](/studynote/04_software_engineering/02_requirements_analysis/065_development_team_scrum/)
**다음**: [67. 스프린트 (Sprint) - 1~4주의 개발 주기](/studynote/04_software_engineering/02_requirements_analysis/067_sprint_timebox/) ->

---
