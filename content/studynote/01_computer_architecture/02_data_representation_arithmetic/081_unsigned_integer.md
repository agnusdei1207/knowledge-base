+++
title = "81. 부호 없는 정수 (Unsigned Integer)"
date = 2026-05-05

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 부호 없는 정수(Unsigned Integer)는 할당된 모든 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 수치(Magnitude) 표현에만 사용하여, 0과 양의 정수만을 나타내는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 체계다.
> 2. **가치**: 부호 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)(Sign [Bit](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/086_fenwick_tree/))를 사용하지 않으므로 동일한 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 폭에서 [부호 있는 정수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/082_signed_integer/)([Signed Integer](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/082_signed_integer/))보다 양수 표현 범위를 정확히 2배 확장할 수 있다.
> 3. **판단 포인트**: 음수가 존재할 수 없는 물리적 메모리 주소(Pointer)나 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/), [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) 설계 시 필수적으로 적용하여 자원 효율성을 극대화해야 한다.

---

## Ⅰ. 개요 및 필요성

부호 없는 정수(Unsigned Integer)는 시스템 내에서 크기나 수량, 위치 정보만을 순수하게 표현하기 위해 고안되었다. [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 컴퓨터 설계자들은 메모리와 레지스터의 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 하나하나가 극도로 제한된 자원임을 인식했다. 파일의 크기나 메모리 주소처럼 태생적으로 0보다 작을 수 없는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)에 부호 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)([MSB](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/080_msb/))를 할당하는 것은 가용 메모리 공간을 절반으로 깎아먹는 심각한 낭비였다.

이를 해결하기 위해 MSB조차 수치의 [가중치](/knowledge-base/studynote/10_ai/03_llm_nlp/267_weight_bias_activation/)(2ⁿ⁻¹)로 온전히 편입시키는 Unsigned 체계를 도입했다. 이 방식은 별도의 부호 검사 로직이 필요 없어 연산 속도를 높일 수 있고, 하드웨어가 접근할 수 있는 절대적인 주소 공간을 최대치로 밀어 올리는 기반이 되었다.

- **📢 섹션 요약 비유**: 부호 없는 정수는 자동차의 주행 거리계(Odometer)와 같다. 차가 앞으로 가든 뒤로 가든 거리계의 숫자는 항상 0에서 시작해 999,999를 향해 양의 방향으로만 커진다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 전방위 수치화 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 할당
모든 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 수치를 나타내므로 $n$ [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)의 시스템에서 표현 범위는 $0$ 부터 $2^n - 1$ 이다. 32비트 운영체제에서 `unsigned int`는 최대 약 42억($2^{32}-1$)까지 주소를 지정할 수 있지만, `signed int`는 21억까지만 가능하다. 이는 32비트 CPU가 물리적으로 4GB의 RAM을 꽉 채워 쓸 수 있게 한 아키텍처적 근간이다.

| [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 타입 (32비트 기준) | 부호 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 여부 | 최솟값 | 최댓값 |
|:---|:---|:---|:---|
| [부호 있는 정수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/082_signed_integer/) (Signed) | O ([MSB](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/080_msb/) 사용) | -2,147,483,648 | 2,147,483,647 |
| 부호 없는 정수 (Unsigned) | X (모두 수치) | 0 | **4,294,967,295** |

### 연산기([ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)) 동작 원리: 제로 확장과 [논리 시프트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/120_logical_shift/)
하드웨어 관점에서 부호 없는 정수는 처리가 매우 단순하다.
- [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 버스를 확장할 때 부호를 복사할 필요 없이 상위 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 전부 0으로 채우는 <strong>제로 확장(<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/">Zero</a> Extension)</strong> 로직을 거친다.
- 나눗셈을 위한 우측 [시프트 연산](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/119_shift_operations/) 시 빈자리에 무조건 0을 밀어 넣는 <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/120_logical_shift/">논리 시프트</a>(<a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/120_logical_shift/">Logical Shift</a>)</strong> [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 사용된다. 복잡한 판별 게이트가 없어 클럭 지연이 최소화된다.

- **📢 섹션 요약 비유**: 부호 없는 정수의 연산은 빈 통에 물을 채우는 것과 같다. 통이 커지면([비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 확장) 그냥 빈 공간을 공기(0)로 냅두면 되고, 물을 덜어내면(시프트) 위부터 텅 비게 둔다.

---

## Ⅲ. 비교 및 연결

### 랩어라운드(Wraparound)와 [언더플로우](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/096_underflow/)
[부호 있는 정수](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/082_signed_integer/)가 범위를 넘어서면 양수가 음수가 되는 '[오버플로우](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/095_overflow/)'가 발생하지만, 부호 없는 정수는 모듈로(Modulo) 연산 특성에 의해 닫힌 원형 트랙을 도는 **랩어라운드(Wraparound)** 현상을 겪는다.

```text
┌──────────────────────────────────────────────────────┐
│        부호 없는 정수의 한계 돌파: 랩어라운드 현상           │
├──────────────────────────────────────────────────────┤
│   [ 8비트 Unsigned 기준: 0 ~ 255 범위 ]                  │
│                                                      │
│   255 (11111111) + 1  ──▶  0 (00000000)   : 원점으로   │
│     0 (00000000) - 1  ──▶ 255 (11111111)  : 최댓값으로 │
│                                                      │
│ * 핵심 판단: 0에서 작은 뺄셈을 수행하면 시스템상 가장      │
│   거대한 숫자로 순간이동(언더플로우) 해버린다.             │
└──────────────────────────────────────────────────────┘
```

이러한 특성 때문에 부호 없는 정수를 루프(Loop) [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)로 사용할 때, `i >= 0` 조건으로 감소시키면 `i`가 0에서 -1이 되는 대신 42억으로 랩어라운드되어 무한 루프에 빠지는 치명적인 버그가 발생한다.

- **📢 섹션 요약 비유**: 랩어라운드는 아날로그 시계의 바늘이다. 12시(최댓값)에서 1분을 더 가면 13시가 되지 않고 12시 1분([초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/)화)이 되며, 정각에서 1분을 빼면 갑자기 11시 59분(거대 숫자)이 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 실무 도입 [체크리스트](/knowledge-base/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. **메모리 포인터(Pointer) 선언**: 메모리의 절대 주소값이나 구조체 크기(Size)를 담는 변수(`size_t`)는 시스템 헤더에 규정된 대로 `unsigned` 계열을 강제하고 있는가?
2. <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/">비트</a> 마스크(Bitmask) 연산</strong>: 다수의 플래그를 ON/OFF 하는 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 단위 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 연산 변수는 부호 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)의 간섭을 막기 위해 철저하게 부호 없는 정수로 선언했는가?

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- <strong><a href="/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/">배열</a> <a href="/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/">인덱스</a>에 Signed 타입 혼용</strong>: C/C++에서 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)의 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 계산할 때 `int`와 `unsigned int`를 무분별하게 섞어 쓰면(Integer Conversion Rules), 컴파일러가 암시적으로 모든 값을 Unsigned로 승격시킨다. 이 상태에서 음수 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 유입되면 랩어라운드가 발생해 엉뚱한 메모리 주소(버퍼 오버런)를 참조하게 되어 해킹의 표적이 된다.

- **📢 섹션 요약 비유**: [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)에 부호를 혼용하는 것은 일방통행 도로에 양방향 통행 차량을 허용하는 것과 같다. 겉보기엔 도로 폭이 여유로워 보이지만, 역주행 차량(음수)이 들어오는 순간 대형 사고(보안 취약점)가 발생한다.

---

## Ⅴ. 기대효과 및 결론

부호 없는 정수의 적극적인 활용은 마이크로프로세서가 가진 하드웨어 레지스터와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 버스의 폭을 낭비 없이 100% 효율로 끌어내는 기술이다. 부호 검사가 생략된 단순한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 패스([Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) Path)는 클럭 스피드 향상에 기여하며, 특히 저전력 [IoT](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 디바이스나 네트워크 [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/) 프로토콜에서 헤더 길이를 최소화하는 데 핵심적이다.

결론적으로 부호 없는 정수는 "음수가 필요 없다"는 시스템의 제약 사항을 "범위 2배 확장과 속도 향상"이라는 하드웨어적 이점으로 치환한 모범적인 아키텍처 설계의 결과물이다.

- **📢 섹션 요약 비유**: 부호 없는 정수는 무조건 앞으로만 가는 경주마에 눈가리개를 씌운 것이다. 옆이나 뒤를 볼 필요가 없기 때문에 오직 최고 속도로 트랙(연산)을 질주할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/120_logical_shift/">논리 시프트</a> (<a href="/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/120_logical_shift/">Logical Shift</a>)</strong> | 빈자리를 무조건 0으로 채우는 Unsigned 전용의 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 단위 나눗셈 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) |
| <strong>제로 확장 (<a href="/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/585_zero_skipping/">Zero</a> Extension)</strong> | Unsigned [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 더 큰 레지스터로 옮길 때 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 무결성을 보장하는 방법 |
| <strong>모듈로 연산 (<a href="/knowledge-base/studynote/09_security/03_network_security/114_modulo_arithmetic/">Modulo Arithmetic</a>)</strong> | 표현 한계 초과 시 값이 원점으로 되돌아오는 유한한 정수 집합의 수학적 기반 |

### 📈 관련 키워드 및 발전 흐름도

```text
정수 표현의 비트 한계 (Hardware Constraints)
    │
    ▼
부호 없는 정수 도입 (부호 비트 제거)
    │
    ▼
양수 범위 2배 확장 · 제로 확장 (Zero Extension)
    │
    ▼
논리 시프트 (Logical Shift) 최적화
    │
    ▼
메모리 주소 (Pointer) 및 네트워크 포트 규격화 표준안 정립
```

이 흐름도는 "하드웨어 한계 극복 → 수치 전용 설계 → [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 수준 가속 → 시스템 표준(주소 체계) 확립"으로 확장되는 부호 없는 정수의 진화를 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 부호 없는 정수는 0부터 시작해서 무조건 양수만 잴 수 있는 아주 긴 줄자예요.
2. 마이너스(-)라는 뒷걸음질이 없기 때문에, 똑같은 길이의 줄자라도 훨씬 더 큰 숫자까지 잴 수 있답니다.
3. 하지만 0에서 뒤로 한 칸 가라고 명령하면 줄자 끝에서 맨 처음으로 순간이동(랩어라운드) 해버리니 조심해야 해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 81 / 803

← **이전**: [80. MSB (Most Significant Bit)](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/080_msb/)
**다음**: [82. 부호 있는 정수 (Signed Integer)](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/082_signed_integer/) →

---
