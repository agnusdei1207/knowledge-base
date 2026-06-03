+++
title = "10. 기수 정렬 (Radix Sort) — O(d·n), 고정 자릿수"
date = 2026-04-21

[taxonomies]
tags = ["studynote-algorithm"]

[extra]
tags = ["studynote-algorithm"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 정렬은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 자릿수(digit) 단위로 분리해 각 자릿수마다 안정 정렬을 반복 적용함으로써 O(d·n) 시간에 정수를 정렬한다.
> 2. **가치**: 자릿수 d가 상수에 가까운 고정 길이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)(전화번호, IP 주소, 주민번호 등)에서 O(n)에 수렴하며 대용량 정수 정렬에 강점을 보인다.
> 3. **판단 포인트**: 서브루틴으로 반드시 안정 정렬([계수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/))을 사용해야 하며, 문자열·실수처럼 고정 자릿수가 아닌 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에는 추가 처리가 필요하다.

---

## Ⅰ. 개요 및 필요성

비교 정렬의 O(n log n) 한계를 넘기 위한 또 다른 접근이 <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/">기수</a> 정렬 (<a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/">Radix</a> Sort)</strong>이다. [계수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)이 값의 전체 범위 k에 의존하는 반면, [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 정렬은 <strong>각 자릿수(0~9, 26알파벳 등) 범위 k만 사용</strong>하므로 k가 고정된다([기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 진법 수). 32비트 정수도 10진수 10자리, 2진수 32비트로 분해하면 각 자릿수는 0~9 또는 0~1로 제한된다.

### 두 가지 처리 방향

| 방식 | 이름 | 설명 |
|:---:|:---:|:---|
| LSD | Least Significant Digit (최하위 자릿수 우선) | 일의 자리부터 정렬 → 쉽고 안정적 |
| MSD | Most Significant Digit (최상위 자릿수 우선) | 최고 자리부터 정렬 → [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)적, 사전식 정렬에 유리 |

📢 **섹션 요약 비유**: [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 정렬은 우편번호로 편지를 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하는 것과 같다. 먼저 마지막 자리 숫자로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하고, 그 다음 앞 자리로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하면 최종적으로 완벽한 순서가 된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### LSD [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 정렬 [ASCII](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/103_ascii/) 다이어그램

```
입력: [170, 45, 75, 90, 802, 24, 2, 66]

── 1라운드: 일의 자리(1s)로 안정 정렬 ─────────────
 0│ 170, 90
 2│ 802, 2
 4│ 24
 5│ 45, 75
 6│ 66
결과: [170, 90, 802, 2, 24, 45, 75, 66]

── 2라운드: 십의 자리(10s)로 안정 정렬 ─────────────
 0│ 802, 2
 2│ 24
 4│ 45
 6│ 66
 7│ 170, 75
 9│ 90
결과: [802, 2, 24, 45, 66, 170, 75, 90]

── 3라운드: 백의 자리(100s)로 안정 정렬 ────────────
 0│ 2, 24, 45, 66, 75, 90
 1│ 170
 8│ 802
결과: [2, 24, 45, 66, 75, 90, 170, 802] ✅
```

### [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) 핵심 코드 흐름

```
┌─────────────────────────────────────────────────┐
│  RadixSort(arr, maxDigits d):                   │
│    for i = 1 to d:                              │
│      안정 정렬(arr, 기준=i번째 자릿수)           │
│      ↑ 계수 정렬(Counting Sort) 사용            │
│                                                 │
│  왜 안정 정렬이 필수인가?                        │
│  → 이전 자릿수 정렬 결과를 상위 자릿수 정렬이   │
│    덮어쓰지 않아야 함 (같은 상위 자리면 하위    │
│    자리 순서 유지)                               │
└─────────────────────────────────────────────────┘
```

### 시간/[공간 복잡도](/knowledge-base/studynote/08_algorithm_stats/01_basics/003_space_complexity/)

| 항목 | 복잡도 | 비고 |
|:---|:---:|:---|
| 시간 (전체) | **O(d·(n+k))** | d=자릿수, k=[기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/)(진법) |
| d가 상수일 때 | **O(n)** | 32비트 정수: d=32(2진), d=[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/)(10진) |
| 공간 | O(n+k) | [계수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/) 보조 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) |
| 안정 정렬 | ✅ | LSD 방식 |
| 제자리 정렬 | ❌ | 보조 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 필요 |

📢 **섹션 요약 비유**: [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 정렬은 다단계 [파일](/knowledge-base/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) 시스템이다. 먼저 날짜의 일(day) 단위로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하고, 그다음 월(month), 마지막으로 년(year) 단위로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하면, 최종적으로 완벽한 날짜 순서가 만들어진다.

---

## Ⅲ. 비교 및 연결

### LSD vs MSD 비교

| 구분 | LSD | MSD |
|:---|:---:|:---:|
| 처리 순서 | 최하위 자릿수 → 최상위 | 최상위 자릿수 → 최하위 |
| 구현 | 반복(Iterative) | [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/)(Recursive) |
| 안정성 | ✅ 안정 | 추가 처리 필요 |
| 적합 사례 | 고정 길이 정수 | 사전식 정렬, 가변 길이 문자열 |
| 메모리 | O(n+k) | O(n+k·d) [재귀](/knowledge-base/studynote/08_algorithm_stats/01_basics/014_recursion/) [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) |

### 비비교 정렬 계열 비교

| [알고리즘](/knowledge-base/studynote/08_algorithm_stats/01_basics/001_algorithm_definition/) | 시간 | 공간 | 키 조건 |
|:---|:---:|:---:|:---|
| [계수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/) ([Counting Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)) | O(n+k) | O(n+k) | k ≤ O(n) |
| [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 정렬 ([Radix](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) Sort) | O(d·(n+k)) | O(n+k) | 고정 자릿수 |
| [버킷 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) ([Bucket Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) | O(n) avg | O(n) | 균등 분포 |

📢 **섹션 요약 비유**: [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 정렬과 [계수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)는 고속도로와 IC(인터체인지)의 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/)다. [계수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)이 각 자릿수에서 효율적으로 분기(처리)하고, [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 정렬이 전체 경로를 통합 관리한다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실제 적용 시나리오

**시나리오 1 — 전화번호 정렬**: 11자리 숫자 n=1억 건  
→ d=[11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/), k=[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/), 시간 = O([11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/)·(10⁸+[10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/))) ≈ O(n)  
→ 비교 정렬 O(n log n) 대비 약 3.5배 빠름

<strong>시나리오 2 — <a href="/knowledge-base/studynote/03_network/06_network_layer_ip/286_ipv4_internet_protocol_version_4_rfc_791/">IPv4</a> 주소 정렬</strong>: 4바이트(8비트×4), k=256  
→ d=4, 각 옥텟(Octet)별로 [계수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)  
→ 네트워크 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 테이블 정렬에 활용

<strong>시나리오 3 — 해시 <a href="/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/">버킷 정렬</a></strong>: 해시값(고정 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/))으로 레코드 정렬  
→ [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 구성 시 활용

### [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 선택 트레이드오프

```
┌──────────────────────────────────────────────────────┐
│  기수(Radix) = 2  (2진수)                             │
│   → d = 32비트, 패스 횟수 많음, k=2 (매우 작은 배열) │
│                                                      │
│  기수(Radix) = 256 (1바이트)                          │
│   → d = 4 (32비트 정수), 패스 횟수 적음, k=256       │
│                                                      │
│  실무 권장: 기수 = 256 (바이트 단위)                  │
│  → 4패스로 32비트 정수 완전 정렬                      │
└──────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 선택은 사탕을 몇 개씩 묶어 포장할지 결정하는 것과 같다. 한 개씩(2진수)이면 포장 횟수가 많고, 100개씩(256진수)이면 한 번에 많이 처리할 수 있다.

---

## Ⅴ. 기대효과 및 결론

[기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 정렬은 <strong>자릿수 분해라는 독창적 아이디어</strong>로 정수/고정 길이 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)의 대규모 정렬 문제를 O(n)에 가깝게 해결한다. [데이터베이스](/knowledge-base/studynote/05_database/01_db_architecture_relational/002_database_definition/) 시스템, 네트워크 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/), 암호화 해시 처리 등 실무의 고성능 정렬 요구에 직접 대응한다.

### 효과 정리

| 효과 | 내용 |
|:---|:---|
| [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) | 고정 자릿수 조건 충족 시 O(n) 수렴 |
| 안정성 | LSD 방식에서 완벽한 안정 정렬 |
| 확장성 | 문자열, IP, 날짜 등 다양한 형식으로 확장 가능 |
| 캐시 효율 | [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 기반으로 메모리 지역성(Locality) 양호 |

📢 **섹션 요약 비유**: [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 정렬은 대용량 물류 센터 자동화 시스템이다. 바코드의 각 자리를 순서대로 스캔하면서 여러 컨베이어 벨트로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하면, 수백만 개 박스가 단 몇 번의 패스만으로 완벽하게 정렬된다.

---

### 📌 관련 개념 맵

| 개념 | 연결 [관계](/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/) | 설명 |
|:---|:---|:---|
| [계수 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/) ([Counting Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)) | → 서브루틴 | 각 자릿수 정렬에 사용 |
| [버킷 정렬](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) ([Bucket Sort](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/)) | 유사 개념 | 값 분포 기반 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/) |
| 안정 정렬 (Stable Sort) | → 필수 성질 | LSD에서 이전 자릿수 보존 |
| 비교 기반 하한 | ↔ 돌파 | Ω(n log n) 한계 우회 |
| [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/)([Radix](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/)) | → 설계 파라미터 | [기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 선택이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 결정 |

### 📈 관련 키워드 및 발전 흐름도

```text
[비교 정렬 (O(n log n)) — 비교 기반 한계]
    │
    ▼
[계수 정렬 (Counting Sort) — 자릿수별 안정 정렬]
    │
    ▼
[LSD Radix Sort — 낮은 자릿수부터 반복]
    │
    ▼
[MSD Radix Sort — 높은 자릿수부터 재귀]
    │
    ▼
[고정 자릿수 정수/문자열 정렬 — 전화번호·IP·날짜]
    │
    ▼
[대용량 비비교 정렬 엔진 — DB·네트워크·검색 인덱스]
```
[기수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) 정렬은 비교 정렬의 O(n log n) 한계를 자릿수 분해와 안정 정렬로 우회해, 고정 길이 키의 대용량 정렬을 빠르게 처리한다.

### 👶 어린이를 위한 3줄 비유 설명

📮 <strong>우편번호 <a href="/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/">분류</a></strong>: 편지를 우편번호 마지막 자리 → 그다음 자리 → 맨 앞 자리 순으로 [분류](/knowledge-base/studynote/16_bigdata/05_analysis/104_classification_analysis/)하면, 마치 마법처럼 모든 편지가 순서대로 쌓여요.  
🗂️ **서랍장 정리**: 10개 서랍이 있고, 각 자릿수마다 한 번씩 정리하면 몇 번의 정리로 수백만 개도 완벽하게 정돈할 수 있어요.  
🔢 **자릿수 미용실**: 숫자의 일의 자리, 십의 자리, 백의 자리를 차례로 꾸미면(정렬하면), 마지막엔 모두 아름답게 줄을 서 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 17 / 175

← **이전**: [9. 계수 정렬 (Counting Sort) — O(n+k), 비교 불필요](/knowledge-base/studynote/08_algorithm_stats/02_sorting/016_counting_sort/)
**다음**: [11. 버킷 정렬 (Bucket Sort) — O(n) 평균, 균등 분포](/knowledge-base/studynote/08_algorithm_stats/02_sorting/018_bucket_sort/) →

---
