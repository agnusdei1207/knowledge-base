---
title: 173. 주소 지정 방식 (Addressing Modes)
date: '2026-04-19'
tags:
- studynote-computer-architecture
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 주소 지정 방식 (Addressing Modes)은 [[158_instruction|명령어]]의 [[160_operand|피연산자]] 필드를 CPU (Central Processing Unit)가 값, [[057_register|레지스터]], 혹은 유효 주소 (Effective Address, [[110_enterprise_architecture_ea|EA]]) 계산식 중 무엇으로 해석할지 정하는 규칙이다.
> 2. **가치**: 같은 [[158_instruction|명령어]] 길이 안에서도 상수, 변수, 포인터, [[055_array|배열]], 분기 대상을 효율적으로 표현할 수 있어 [[157_isa|ISA]] ([[157_isa|Instruction Set Architecture]])의 표현력과 코드 밀도 ([[082_process_memory_structure|Code]] Density)를 높인다.
> 3. **판단 포인트**: 주소 모드가 풍부할수록 소프트웨어 작성은 편해지지만 decode, AGU (Address Generation Unit), [[082_pipeline|pipeline]] 설계는 복잡해지므로 현대 [[195_risc|RISC]] (Reduced [[158_instruction|Instruction]] Set Computer)는 단순한 load/store 중심 모드로 수렴한다.

---

## Ⅰ. 개요 및 필요성

주소 지정 방식은 "[[158_instruction|명령어]]에 적힌 숫자를 어디까지 믿고, 어디서부터 계산해야 하는가"를 정하는 해석 규칙이다. 같은 `X`라는 필드라도 어떤 명령은 `X`를 상수로 읽고, 어떤 명령은 [[057_register|레지스터]] 번호로 읽으며, 어떤 명령은 `PC (Program Counter) + X` 같은 주소 계산식의 일부로 읽는다. 결국 주소 지정 방식은 [[158_instruction|명령어]] [[073_bit|비트]]와 실제 [[001_dikw_pyramid|데이터]] 위치 사이를 이어 주는 번역 계층이다.

이 개념이 필요한 이유는 [[158_instruction|명령어]]가 항상 메모리 전체 주소를 직접 담기에는 너무 짧기 때문이다. 또한 프로그램은 상수 한 개만 읽는 경우도 있고, [[055_array|배열]] `a[i]`처럼 기준 주소에 [[154_database_index_b_tree_search_optimization|인덱스]]를 더해야 하는 경우도 있으며, 위치 독립 코드처럼 현재 실행 위치 기준으로 상대 주소를 써야 하는 경우도 있다. 주소 지정 방식이 없다면 [[158_instruction|명령어]]는 지나치게 길어지고, 고급 언어의 포인터·[[055_array|배열]]·[[294_function_calling_tool_use|함수 호출]]을 하드웨어가 자연스럽게 받쳐 주기 어렵다.

아래 그림은 같은 [[160_operand|피연산자]] 필드가 모드에 따라 완전히 다른 뜻을 갖는다는 점을 보여준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Same operand field, different meaning                             │
├────────────────────────────────────────────────────────────────────┤
│ LOAD R1, X                                                        │
│   immediate    -> R1 <- X                                         │
│   direct       -> EA <- X       -> R1 <- M[EA]                    │
│   reg indirect -> EA <- R[X]    -> R1 <- M[EA]                    │
│   PC-relative  -> EA <- PC + X  -> branch/data target             │
└────────────────────────────────────────────────────────────────────┘
```

이 그림의 핵심은 [[158_instruction|명령어]] [[073_bit|비트]]가 곧바로 "주소"가 아니라는 점이다. CPU는 opcode만 읽는 것이 아니라, 그 뒤에 붙은 mode 정보까지 함께 해석해 비로소 실제 [[001_dikw_pyramid|데이터]] 위치나 즉시값의 의미를 확정한다. 따라서 주소 지정 방식은 메모리 접근 문법이면서 동시에 [[170_instruction_format|명령어 형식]] 설계의 핵심 축이다.

- **📢 섹션 요약 비유**: 주소 지정 방식은 쪽지에 적힌 "3번 서랍"이 진짜 서랍 번호인지, 열쇠함 번호인지, "지금 서 있는 자리에서 세 칸 옆"이라는 뜻인지 구분하는 해석 규칙과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

주소 지정 방식의 중심에는 유효 주소 계산이 있다. CPU는 [[158_instruction|명령어]]를 해독한 뒤 [[160_operand|피연산자]]가 메모리에 있다면 유효 주소를 만들고, [[057_register|레지스터]]나 즉시값이라면 그 계산을 생략한다. 이때 현대 프로세서는 산술 [[369_logic_bomb|논리]] 연산 장치 ([[117_alu|Arithmetic Logic Unit]], [[117_alu|ALU]])와 별도로 AGU를 두어 `base + offset`, `index × scale + displacement` 같은 주소 계산을 빠르게 처리한다.

| 주소 지정 방식 | 기본 해석식 | 메모리 접근 특성 | 대표 사용처 |
| :--- | :--- | :--- | :--- |
| 즉시 ([[174_immediate_addressing|Immediate]]) | [[160_operand|operand]] = literal | 메모리 접근 없음 | 상수, 초기값 |
| [[057_register|레지스터]] ([[175_register_addressing|Register]]) | [[160_operand|operand]] = Rn | 메모리 접근 없음 | 자주 쓰는 지역값 |
| 직접 ([[176_direct_addressing|Direct]]) | [[110_enterprise_architecture_ea|EA]] = A | 메모리 1회 | 고정 주소 [[001_dikw_pyramid|데이터]] |
| [[057_register|레지스터]] 간접 ([[178_register_indirect_addressing|Register Indirect]]) | [[110_enterprise_architecture_ea|EA]] = Rb | 메모리 1회 | 포인터, [[057_stack|스택]] |
| 베이스+변위 (Base + [[179_displacement_addressing|Displacement]]) | [[110_enterprise_architecture_ea|EA]] = Rb + d | 메모리 1회 | 구조체, [[057_stack|스택]] 프레임 |
| [[154_database_index_b_tree_search_optimization|인덱스]]/스케일 ([[181_indexed_addressing|Indexed]]/Scaled) | [[110_enterprise_architecture_ea|EA]] = base + [[154_database_index_b_tree_search_optimization|index]]×scale + d | 메모리 1회 | [[055_array|배열]] 원소 접근 |
| [[164_pc|PC]] 상대 ([[182_relative_addressing|PC-Relative]]) | [[110_enterprise_architecture_ea|EA]] = [[164_pc|PC]] + d | 메모리/분기 대상 계산 | 분기, 위치 독립 코드 |

고전 교재의 간접 주소 지정은 `EA = M[A]`처럼 메모리에서 다시 주소를 읽는 **메모리 간접 (Memory [[177_indirect_addressing|Indirect]])**도 포함한다. 이 방식은 포인터의 포인터를 하드웨어가 직접 처리하는 느낌을 주지만, 실제로는 메모리 접근이 한 번 더 필요해 [[015_지연_데이터_관점|지연]]이 크다. 그래서 현대 범용 ISA는 대부분 [[057_register|레지스터]] 간접을 중심으로 설계하고, 깊은 간접 참조는 소프트웨어와 캐시 계층이 감당하게 만든다.

아래 그림은 현대 파이프라인에서 주소 계산이 어디에 위치하는지를 요약한다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Address generation in a modern pipeline                           │
├────────────────────────────────────────────────────────────────────┤
│ instruction -> mode decode -> operand select -> AGU -> EA         │
│                                  │                  │             │
│                                  │                  └-> data cache │
│                                  └-> imm/reg bypass               │
└────────────────────────────────────────────────────────────────────┘
```

즉시값과 [[057_register|레지스터]] [[160_operand|피연산자]]는 AGU를 거치지 않고 곧바로 실행 단계로 들어간다. 반면 메모리 [[160_operand|피연산자]]는 mode decode 결과에 따라 [[329_base_register|base register]], [[154_database_index_b_tree_search_optimization|index]] [[175_register_addressing|register]], displacement를 조합해 EA를 만든 뒤 캐시와 메모리 계층으로 전달된다. 이 과정이 늦어지면 load-use stall, branch target [[015_지연_데이터_관점|지연]], fetch 경계 복잡도가 생기므로 주소 모드 설계는 단순 문법이 아니라 [[282_performance_tactics|성능]] 설계 문제이기도 하다.

- **📢 섹션 요약 비유**: AGU는 택배 기사 앞에서 주소를 미리 표준 주소 체계로 바꿔 주는 내비게이션 직원과 같아서, 기사([[117_alu|ALU]])가 길 찾느라 배송을 멈추지 않게 해 준다.

---

## Ⅲ. 비교 및 연결

주소 지정 방식을 이해하려면 "값을 바로 쓰는 방식"과 "주소를 계산해 찾아가는 방식"을 구분해야 한다. 즉시·[[057_register|레지스터]] 방식은 빠르지만 표현 범위가 제한되고, 직접·간접·[[154_database_index_b_tree_search_optimization|인덱스]] 방식은 표현력이 높지만 주소 계산과 메모리 접근 비용이 따른다. 결국 주소 모드는 편의성과 하드웨어 단순성의 교환 [[083_relationship_in_er_model|관계]] 위에 놓여 있다.

| 비교 축 | 단순 모드 ([[174_immediate_addressing|Immediate]]/[[175_register_addressing|Register]]) | 계산형 모드 ([[177_indirect_addressing|Indirect]]/[[181_indexed_addressing|Indexed]]/Relative) |
| :--- | :--- | :--- |
| 속도 | 가장 빠름 | 주소 계산과 캐시 접근 필요 |
| 코드 표현력 | 낮음 | 높음 |
| 컴파일러 부담 | 작음 | 최적화 선택이 중요 |
| 하드웨어 부담 | 낮음 | decode·AGU 복잡도 증가 |
| 대표 매핑 | `x = 5`, `sum += r1` | `*p`, `a[i]`, `label+offset` |

[[157_isa|ISA]] 관점에서는 [[196_cisc|CISC]] (Complex [[158_instruction|Instruction]] Set Computer)가 복합 주소 지정을 풍부하게 제공해 왔고, RISC는 이를 크게 단순화했다. 예를 들어 x86 계열은 `base + index×scale + displacement`를 한 명령에서 폭넓게 지원하지만, ARM·[[200_riscv|RISC-V]] 계열은 load/store와 단순 변위를 중심으로 규칙성을 유지한다. 덕분에 RISC는 디코더와 파이프라인을 가볍게 만들 수 있고, CISC는 코드 밀도와 하위 호환성에서 이점을 얻는다.

이 주제는 고급 언어의 [[001_dikw_pyramid|데이터]] 모델과도 직접 연결된다. 포인터 역참조는 [[057_register|레지스터]] 간접에, [[055_array|배열]] 인덱싱은 [[154_database_index_b_tree_search_optimization|인덱스]] 주소 지정에, 구조체 필드 접근은 베이스+변위에, 위치 독립 코드는 [[164_pc|PC]] 상대 주소에 대응된다. 즉 주소 지정 방식은 단순한 어셈블리 문법이 아니라, 소프트웨어 추상화가 하드웨어에 내려앉는 지점이다.

- **📢 섹션 요약 비유**: 단순 모드는 "물건을 손에 들고 바로 쓰는 방식"이고, 계산형 모드는 "창고 위치표를 보고 창고 칸까지 찾아가 꺼내는 방식"이라서 편리함과 시간이 함께 바뀐다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 접근 패턴에 맞는 주소 지정 방식 선택이 [[282_performance_tactics|성능]]과 이식성을 좌우한다. 상수는 즉시값으로 두는 것이 가장 싸고, 반복문 내부의 핵심 변수는 [[057_register|레지스터]]에 오래 머물수록 좋다. [[055_array|배열]]·구조체는 베이스+변위 또는 스케일 [[154_database_index_b_tree_search_optimization|인덱스]]를 활용해야 하며, 공유 라이브러리와 실행 [[501_file_definition_logical_record|파일]] 재배치를 고려하는 코드는 [[164_pc|PC]] 상대 주소 지정을 우선 사용해야 한다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Access-pattern driven mode choice                                 │
├────────────────────────────────────────────────────────────────────┤
│ constant?        -> immediate                                     │
│ hot local value? -> register                                      │
│ array/struct?    -> base + offset / scaled index                  │
│ relocatable code?-> PC-relative                                   │
│ pointer chain?   -> reg indirect, but watch cache stalls          │
└────────────────────────────────────────────────────────────────────┘
```

### 실무 판단 기준

1. **위치 독립 코드**: [[374_aslr|ASLR]] (Address Space Layout Randomization)과 공유 라이브러리를 고려하면 절대 주소보다 [[164_pc|PC]] 상대 주소가 안전하다.
2. **루프 최적화**: 연속 [[055_array|배열]] 순회는 base register를 고정하고 offset만 바꾸는 편이 유리하다.
3. **포인터 체인 경계**: 깊은 간접 참조는 주소 계산보다 캐시 미스 비용이 더 커지므로 [[001_dikw_pyramid|데이터]] 구조 자체를 평탄화할지 검토해야 한다.
4. **[[157_isa|ISA]] 복잡도 선택**: 범용 고성능 코어는 일부 복합 모드를 감당할 수 있지만, 임베디드·가속기 코어는 단순 모드가 [[395_verification_process_review|검증]]과 전력 측면에서 유리하다.

### 자주 나오는 [[128_water_scrum_fall_anti_pattern|안티패턴]]

- 절대 주소를 남발해 재배치와 보안 대응을 어렵게 만드는 것
- 포인터를 여러 단계로 중첩해 메모리 [[015_지연_데이터_관점|지연]]을 주소 모드 문제로 오해하는 것
- 복합 주소 식을 무조건 빠르다고 보고, 실제 캐시 지역성이나 파이프라인 제약을 무시하는 것

기술사 답안에서는 주소 지정 방식을 종류만 나열하기보다, **어떤 모드가 어떤 소프트웨어 패턴을 얼마나 적은 [[073_bit|비트]]와 몇 번의 메모리 접근으로 표현하는지**까지 설명해야 깊이가 살아난다.

- **📢 섹션 요약 비유**: 주소 모드 선택은 배달 경로를 정하는 일과 같아서, 물건 하나는 손에 들고 가면 되지만 창고 물건은 선반 번호 체계를 잘 써야 가장 빨리 찾을 수 있다.

---

## Ⅴ. 기대효과 및 결론

좋은 주소 지정 방식 설계는 [[158_instruction|명령어]] 집합을 더 작고 더 유연하게 만든다. 같은 [[073_bit|비트]] 수로 더 많은 [[001_dikw_pyramid|데이터]] 접근 패턴을 표현할 수 있어 코드 크기를 줄이고, 컴파일러가 고급 언어 구조를 자연스럽게 기계어로 매핑할 수 있게 된다. 특히 [[055_array|배열]], 포인터, [[294_function_calling_tool_use|함수 호출]], 위치 독립 코드처럼 현대 소프트웨어의 기본 구조가 주소 모드 덕분에 효율적으로 구현된다.

반면 주소 모드가 많아질수록 하드웨어가 더 똑똑해져야 한다. decode 경로가 길어지고, AGU 설계가 복잡해지며, 예외 처리와 [[395_verification_process_review|검증]] 비용도 증가한다. 그래서 현대 아키텍처는 "무조건 많은 모드"보다 **자주 쓰는 패턴을 단순하게 빠르게 처리하는 방향**으로 최적화한다.

결론적으로 주소 지정 방식은 메모리 주소를 적는 기술이 아니라, **제한된 [[170_instruction_format|명령어 형식]] 안에서 [[001_dikw_pyramid|데이터]] 세계를 효율적으로 호출하는 문법**이다. 기억할 핵심은 "주소 모드가 곧 코드 표현력이며, 그 대가는 하드웨어 복잡도"라는 균형이다.

- **📢 섹션 요약 비유**: 주소 지정 방식의 진화는 작은 서랍장에 많은 물건을 넣기 위해, 물건 이름표 대신 위치 규칙과 [[104_classification_analysis|분류]] 규칙을 정교하게 만든 과정과 같다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [[170_instruction_format|명령어 형식]] ([[170_instruction_format|Instruction Format]]) | 주소 모드 [[073_bit|비트]]가 어디에 들어가는지 결정한다. |
| 유효 주소 (Effective Address, [[110_enterprise_architecture_ea|EA]]) | 메모리 접근 직전에 확정되는 실제 주소다. |
| AGU (Address Generation Unit) | 베이스·[[154_database_index_b_tree_search_optimization|인덱스]]·변위를 조합해 EA를 계산한다. |
| load/store 아키텍처 | 메모리 접근을 제한된 명령으로 단순화한 설계 철학이다. |
| 위치 독립 코드 (Position Independent [[082_process_memory_structure|Code]], PIC) | [[164_pc|PC]] 상대 주소 지정과 강하게 연결된다. |
| 캐시 지역성 (Cache Locality) | 주소 지정 방식이 실제 [[282_performance_tactics|성능]]으로 이어질 때 가장 큰 영향 요소다. |

### 📈 관련 키워드 및 발전 흐름도

```text
operand field
    │
    ▼
mode decode
    │
    ├──────────────▶ immediate / register
    │
    └──────────────▶ EA generation
                         │
                         ├─ base + displacement
                         ├─ index / scale
                         └─ PC-relative
                              │
                              ▼
                   load/store · branch · position-independent code
```

이 흐름도는 주소 지정 방식이 단순 [[104_classification_analysis|분류]]표가 아니라, [[160_operand|operand]] 해석에서 실제 메모리 접근과 코드 재배치까지 이어지는 실행 경로임을 보여준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 주소 지정 방식은 컴퓨터가 쪽지에 적힌 힌트를 보고 보물이 어디 있는지 찾는 규칙이에요.
2. 어떤 쪽지는 "여기 숫자 그대로 써"라고 하고, 어떤 쪽지는 "서랍 번호를 먼저 보고 가"라고 말해요.
3. 그래서 작은 쪽지 한 장으로도 컴퓨터는 아주 많은 물건을 똑똑하게 찾아낼 수 있어요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 173 / 803

← **이전**: [[172_variable_length_instruction|172. 가변 길이 명령어 (Variable-Length Instruction)]]
**다음**: [[174_immediate_addressing|174. 즉시 주소 지정 (Immediate)]] →

---
