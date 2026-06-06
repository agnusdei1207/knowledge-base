---
title: "061. Bloomfilter"
date: "2026-04-05"
tags:
  - "studynote-it-management"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Bloom Filter는 원소가 집합에 있는지 빠르게 검사하는 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 자료구조이며, False Negative는 없고 False Positive만 허용한다.
> 2. **가치**: [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/)과 여러 [해시 함수](/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/)만으로 대규모 집합을 매우 적은 메모리로 표현할 수 있어 대용량 시스템에 유리하다.
> 3. **판단**: 삭제가 필요하면 Counting Bloom Filter나 Cuckoo Filter를 고려하고, 멤버십 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)만 필요할 때 가장 빛난다.

---

## Ⅰ. 개요 및 필요성

대규모 [로그](/studynote/04_software_engineering/09_cloud_native_ai_architecture/568_logs_distributed_logging_elk_fluentd/), URL, 블랙리스트, 캐시 조회처럼 "이미 본 적이 있는가?"를 빠르게 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/)해야 하는 일이 많다. 전통적인 집합 구조는 정확하지만 메모리를 많이 쓴다.

Bloom Filter는 정확도를 조금 양보하는 대신, 메모리와 속도를 크게 아낀다. 그래서 거대한 시스템에서 "일단 없다고 빨리 거르기" 용도로 아주 유용하다.

- **📢 섹션 요약 비유**: 모든 책을 직접 펼쳐 보는 대신, 책장 앞에서 색깔 스티커로 먼저 거르는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

```text
삽입
원소 -> h1,h2,...,hk -> 비트 배열의 k개 위치를 1로 설정

조회
원소 -> h1,h2,...,hk -> 모두 1이면 "있을 가능성"
                              하나라도 0이면 "없음"
```

| 구성 요소 | 역할 |
| :-- | :-- |
| [Bit](/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/) [Array](/studynote/08_algorithm_stats/04_datastructure/055_array/) | 매우 작은 메모리로 상태 저장 |
| Hash Functions | 여러 위치에 표시하여 충돌 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/) 감소 |
| Insert | 해시 위치 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 1로 [설정](/studynote/15_devops_sre/01_culture_methodology/009_config/) |
| Query | 해당 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 모두 1인지 [확인](/studynote/04_software_engineering/12_testing_maintenance/396_validation/) |

Bloom Filter는 "없음"은 확실히 말할 수 있지만, "있음"은 가능성만 말한다. 이 특성이 False Positive를 허용하는 대신 공간 효율을 얻는 핵심이다.

- **📢 섹션 요약 비유**: 도장 여러 개를 찍어 두고, 하나라도 비어 있으면 그 손님은 아니라고 바로 판단하는 방식이다.

---

## Ⅲ. 비교 및 연결

| 자료구조 | 장점 | 단점 |
| :-- | :-- | :-- |
| HashSet | 정확함 | 메모리 큼 |
| Bloom Filter | 메모리 적음, 빠름 | False Positive 가능 |
| Counting Bloom Filter | 삭제 가능 | 메모리 조금 증가 |
| Cuckoo Filter | 삭제와 높은 효율 | 구현이 더 복잡 |

Bloom Filter는 웹 크롤러 중복 방지, 캐시 프리체크, 스팸 차단, [분산](/studynote/08_algorithm_stats/08_stats/136_variance/) 시스템의 사전 필터링에 잘 맞는다. 즉, 대량 조회 전에 불필요한 I/O를 줄이는 데 강하다.

- **📢 섹션 요약 비유**: 큰 줄을 모두 세지 않고, 먼저 "아예 아닐 사람"부터 빠르게 걷어내는 검문소다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)

1. 메모리 절약이 실제 목표인가?
2. False Positive를 허용할 수 있는가?
3. 삭제가 필요한가, 단순 조회만 필요한가?
4. [해시 함수](/studynote/03_network/13_network_security_basics/667_hash_function_integrity_one_way/) 개수와 [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 크기를 계산했는가?
5. 후속 시스템이 False Positive를 다시 검증하는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- False Positive를 절대 허용할 수 없는 곳에 쓰는 설계
- 삭제가 필요함에도 일반 Bloom Filter를 쓰는 설계
- [비트](/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) [배열](/studynote/08_algorithm_stats/04_datastructure/055_array/) 크기를 대충 잡아 성능을 망치는 설계
- "있음" 결과를 무조건 확정으로 오해하는 설계

기술사 관점에서는 Bloom Filter를 정답 저장소로 보면 안 된다. Bloom Filter는 대용량 시스템의 앞단에서 비용을 줄이는 필터라는 점이 핵심이다.

- **📢 섹션 요약 비유**: 경비원이 모든 사람을 완벽히 기억하지 못해도, 일단 수상한 사람만 빨리 골라내는 데는 충분한 도구다.

---

## Ⅴ. 기대효과 및 결론

Bloom Filter는 정확도와 자원의 균형을 잘 맞춘 [확률](/studynote/08_algorithm_stats/08_stats/130_probability/)적 자료구조다. 대규모 시스템에서 불필요한 조회를 줄이고 응답 속도를 높이는 데 유용하다.

결국 핵심은 "완벽한 답"보다 "충분히 빠른 거르기"가 필요한 문제에 이 구조를 쓰는 것이다.

- **📢 섹션 요약 비유**: 전부 맞히는 시험지가 아니라, 틀린 답만 빨리 골라내는 검사표다.

---

## 관련 개념 맵

```text
Bit Array
   v
Bloom Filter
   v
Probabilistic Membership Test
   v
Cache / Crawler / Log Dedup
   v
Large-scale Systems
```

---

## 관련 키워드 및 발전 흐름도

```text
HashSet
   v
Bloom Filter
   v
Counting Bloom Filter
   v
Cuckoo Filter
   v
Approximate Membership Query
```

---

## 어린이를 위한 3줄 비유 설명

아무 책이나 다 찾는 대신, 먼저 스티커를 보고 빨리 걸러내는 거예요.
스티커가 모두 붙어 있으면 아마 맞을 수 있지만, 하나라도 없으면 아니에요.
그래서 아주 많은 것을 빨리 검사할 때 좋아요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 105 / 587

<- **이전**: [60. RPA (Robotic Process Automation) 및 초자동화 (Hyperautomation)](/studynote/12_it_management/01_governance_strategy/060_rpa_hyperautomation/)
**다음**: [61. ITSM (IT Service Management)](/studynote/12_it_management/02_itsm_itil/845_itsm/) ->

---
