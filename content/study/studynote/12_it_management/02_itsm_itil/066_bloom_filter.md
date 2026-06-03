---
title: 66. 블룸 필터 (Bloom Filter)
tags:
- it_management
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [[061_bloomfilter|블룸 필터]]([[061_bloomfilter|Bloom Filter]])는 원소 존재 여부를 빠르게 추정하는 확률적 자료 구조다.
> 2. **가치**: 메모리를 적게 쓰면서도 "없음"을 빠르게 판단할 수 있어 캐시, 검색, 중복 검사에 유용하다.
> 3. **판단**: false positive는 가능하지만 false negative는 없다는 점을 이해해야 한다.

---

## Ⅰ. 개요 및 필요성

대규모 데이터에서 "이 값이 있을까?"를 매우 빠르게 [[396_validation|확인]]해야 할 때가 있다. 이때 [[061_bloomfilter|블룸 필터]]가 큰 역할을 한다.

정확한 집합 검색보다 메모리 효율이 중요한 환경에서 특히 유리하다.

- **📢 섹션 요약 비유**: 도서관에서 책이 없다는 건 빨리 말해 주지만, 있다고 말할 때는 가끔 착각할 수 있는 안내판이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
Item
  ↓
Multiple Hash Functions
  ↓
Bit Array
  ↓
Membership Test
```

| 요소 | 역할 |
| :-- | :-- |
| [[086_fenwick_tree|Bit]] [[055_array|Array]] | [[533_bit_vector_bitmap|비트 벡터]] 저장 |
| Hash Functions | 여러 위치에 표시 |
| Query | 모두 1이면 존재 가능성 |

아이템을 넣을 때 여러 해시 위치의 [[073_bit|비트]]를 1로 만든다. 조회할 때 해당 위치가 모두 1이면 있을 수도 있다고 판단한다.

- **📢 섹션 요약 비유**: 여러 도장을 찍어 두고, 모든 도장이 찍혀 있으면 들어왔을 가능성이 있다고 보는 방식이다.

---

## Ⅲ. 비교 및 연결

| 특징 | [[061_bloomfilter|Bloom Filter]] | Hash Set |
| :-- | :-- | :-- |
| 메모리 | 매우 적음 | 상대적으로 큼 |
| 정확도 | false positive 가능 | 정확 |
| 속도 | 매우 빠름 | 빠름 |

| 사용처 | 예 |
| :-- | :-- |
| 캐시 | 없는 항목 빠른 배제 |
| 검색 | 중복/필터링 |
| [[136_variance|분산]] 시스템 | 네트워크 호출 감소 |

[[061_bloomfilter|블룸 필터]]는 "없다"는 빠르게 확정해 주는 데 특히 유리하다. 그래서 불필요한 조회를 줄이는 용도로 좋다.

- **📢 섹션 요약 비유**: "이 집엔 없어요"를 빨리 알려 주는 경비 시스템이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [[435_checklist_based_testing|체크리스트]]

1. false positive를 허용할 수 있는가?
2. 메모리 절감 효과가 필요한가?
3. [[667_hash_function_integrity_one_way|해시 함수]] 수와 [[073_bit|비트]] [[055_array|배열]] 크기를 맞췄는가?
4. 삭제가 필요한 경우 대안이 있는가?
5. 확률적 오차를 서비스에 반영했는가?

### [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 정확한 결과가 필요한 곳에 쓰는 설계
- false positive를 무시하는 설계
- 해시 충돌과 [[055_array|배열]] 크기를 고려하지 않는 설계
- 삭제가 필요한데 일반 Bloom Filter만 쓰는 설계

기술사 관점에서는 [[061_bloomfilter|블룸 필터]]를 "정확한 검색 구조"가 아니라 "빠른 사전 필터"로 봐야 한다.

- **📢 섹션 요약 비유**: 문 앞에서 대충 걸러 주는 안내원이지, 최종 판결을 내리는 판사는 아니다.

---

## Ⅴ. 기대효과 및 결론

[[061_bloomfilter|블룸 필터]]는 대규모 시스템에서 메모리와 조회 비용을 줄이는 데 매우 유용하다. 특히 없음 판정의 속도가 중요한 경우 좋다.

결론적으로 Bloom Filter는 확률적 membership test를 위한 효율적 자료 구조다.

- **📢 섹션 요약 비유**: 빠르게 거르고, 정확한 [[396_validation|확인]]은 뒤에서 하는 방식이다.

---

## 관련 개념 맵

```text
Hash Functions
  ↓
Bloom Filter
  ↓
Membership Test
  ↓
Probabilistic DS
```

---

## 관련 키워드 및 발전 흐름도

```text
Set Membership
  ↓
Bloom Filter
  ↓
Count-Min Sketch
  ↓
Approximate Query
```

---

## 어린이를 위한 3줄 비유 설명

먼저 없다고 빨리 걸러 줘요.  
있다고 하면 가끔 틀릴 수 있어요.  
[[061_bloomfilter|블룸 필터]]는 그런 빠른 [[396_validation|확인]] 도구예요.
