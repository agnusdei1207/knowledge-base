+++
title = "69. 데크/원형 큐 (Deque / Circular Queue)"

[taxonomies]
tags = ["it_management"]

[extra]
tags = ["it_management"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 데크([Deque](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/084_deque/))는 양쪽 끝에서 삽입/삭제가 가능한 자료 구조이고, 원형 큐는 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 끝을 다시 처음과 연결해 공간을 효율적으로 쓰는 큐다.
> 2. **가치**: 스택과 큐의 장점을 함께 쓰거나, 고정 크기 버퍼를 효율적으로 관리할 수 있다.
> 3. **판단**: 구현은 단순해 보여도 포인터/[인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 관리와 가득 참/비어 있음 판별이 중요하다.

---

## Ⅰ. 개요 및 필요성

양방향으로 넣고 빼야 하거나, [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 공간을 낭비하지 않고 순환적으로 쓰고 싶을 때가 있다.

그럴 때 데크와 원형 큐가 유용하다.

- **📢 섹션 요약 비유**: 앞문과 뒷문이 모두 있는 버스와, 원을 그리며 도는 줄이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Deque: addFront/addRear, removeFront/removeRear
Circular Queue: front/rear wrap-around
```

| 구조 | 특징 |
| :-- | :-- |
| [Deque](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/084_deque/) | 양쪽 끝 연산 |
| Circular [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) | [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 순환 |

원형 큐는 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 끝을 다시 처음과 연결해 공간 활용을 높인다. 데크는 그보다 더 유연하게 양끝 연산을 지원한다.

- **📢 섹션 요약 비유**: 링 모양의 도로와 양쪽 출입문이 있는 상자다.

---

## Ⅲ. 비교 및 연결

| 구분 | [Deque](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/084_deque/) | Circular [Queue](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/058_queue/) |
| :-- | :-- | :-- |
| 연산 | 양방향 | [FIFO](/knowledge-base/studynote/02_operating_system/04_synchronization/261_fifo_page_replacement/) 순환 |
| 구조 | 더 유연 | 더 단순 |
| 용도 | 슬라이딩 윈도우 | 버퍼/스케줄링 |

| 관련 개념 | 의미 |
| :-- | :-- |
| Buffer | 고정 길이 저장 |
| Wrap-around | [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 순환 |

데크는 스택과 큐를 모두 흉내 낼 수 있어 범용성이 높고, 원형 큐는 고정 버퍼 관리에 좋다.

- **📢 섹션 요약 비유**: 한 상자는 양쪽으로 쓰고, 다른 상자는 돌려 쓰는 방식이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. front/rear [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 정확히 관리하는가?
2. full/empty 상태를 구분하는가?
3. 원형 순환을 올바르게 처리하는가?
4. 슬라이딩 윈도우에 적합한가?
5. 구현 복잡도와 메모리 효율을 비교했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 순환을 잘못 처리하는 설계
- 가득 참/비어 있음 판별을 혼동하는 설계
- 양방향 연산이 필요한데 일반 큐만 쓰는 설계
- 버퍼 크기를 고정하면서 공간을 낭비하는 설계

기술사 관점에서는 데크와 원형 큐를 "공간 효율적인 순차 저장 구조"로 설명해야 한다.

- **📢 섹션 요약 비유**: 줄도 돌리고, 문도 두 개 달아 둘 수 있다.

---

## Ⅴ. 기대효과 및 결론

데크와 원형 큐는 버퍼 관리와 양방향 처리에서 효율적이다.

결론적으로 데크는 양방향 자료 구조이고, 원형 큐는 순환 버퍼다.

- **📢 섹션 요약 비유**: 하나는 양쪽 문, 하나는 원형 길이다.

---

## 관련 개념 맵

```text
Deque
  ↓
Circular Queue
  ↓
Wrap-around
  ↓
Buffer Management
```

---

## 관련 키워드 및 발전 흐름도

```text
Queue
  ↓
Deque
  ↓
Circular Queue
  ↓
Efficient Buffer
```

---

## 어린이를 위한 3줄 비유 설명

앞에서도 뒤에서도 넣고 뺄 수 있어요.  
원형 큐는 끝이 다시 처음과 이어져요.  
데크와 원형 큐는 그런 자료 구조예요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 121 / 587

← **이전**: [68. 스택/큐 (Stack / Queue)](/knowledge-base/studynote/12_it_management/02_itsm_itil/068_stack_queue/)
**다음**: [69. ITIL 4 의 핵심 개념 변화](/knowledge-base/studynote/12_it_management/02_itsm_itil/069_itil4_core_change/) →

---
