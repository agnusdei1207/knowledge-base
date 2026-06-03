+++
title = "178. 레지스터 간접 주소 지정 (Register Indirect)"
date = 2026-04-19

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/) ([Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) [Indirect Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/))은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 최종 메모리 주소를 직접 담지 않고, **그 주소를 가진 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)만 지정**하여 `EA (Effective Address) = contents of register`로 유효 주소를 얻는 방식이다.
> 2. **가치**: 긴 주소를 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)에 매번 적지 않아도 되므로 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 형식은 짧고 단순하게 유지하면서도, 실제 접근 대상은 실행 중에 유연하게 바꿀 수 있다.
> 3. **판단 포인트**: [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)보다 범용성이 크고 메모리 [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)보다 빠르지만, 결국 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 메모리에서 읽어야 하므로 캐시 지역성·[레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 압박·포인터 체인 길이를 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

[레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/) ([Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) [Indirect Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/))은 **[명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 안에는 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 번호만 적고, 그 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 안에 들어 있는 값을 메모리 주소로 해석하는 방식**이다. 예를 들어 `LOAD R0, [R2]`라면 `R2`의 내용이 0x1000일 때 실제 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/)는 `Memory[0x1000]`에서 읽힌다. 즉 "주소를 담은 작은 손잡이"를 CPU (Central Processing Unit) 내부에 두고, [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 그 손잡이만 집는다.

이 방식이 필요해진 이유는 두 가지다. 첫째, [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) ([Direct Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/))은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 길이가 짧을수록 표현 가능한 주소 범위가 제한된다. 둘째, 메모리 [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/) ([Indirect Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/))은 주소를 메모리에서 한 번 더 읽어 와야 하므로, [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 인출을 제외해도 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) 접근에 메모리 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)가 추가된다. [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)은 이 둘 사이에서 **[명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 짧게, 주소는 넓게, 접근은 비교적 빠르게** 만들기 위한 절충안이다.

아래 그림은 왜 "주소를 메모리가 아니라 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 올려두는가"를 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Why register-indirect exists                                      │
├────────────────────────────────────────────────────────────────────┤
│ direct         : instruction -> memory(data)                      │
│                  fast enough, but address bits are expensive      │
│                                                                    │
│ memory indirect: instruction -> memory(pointer) -> memory(data)   │
│                  flexible, but one more memory trip               │
│                                                                    │
│ register indirect                                                  │
│                : instruction -> register(pointer) -> memory(data) │
│                  short encoding + only one operand memory access  │
└────────────────────────────────────────────────────────────────────┘
```

핵심은 **주소를 따라가는 유연성은 유지하되, 그 중간 매개체를 느린 메모리 대신 빠른 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)로 옮긴다**는 데 있다. 그래서 포인터, [스택 포인터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/), 버퍼 시작 주소처럼 실행 중 달라지는 위치를 다룰 때 매우 유리하다.

- **📢 섹션 요약 비유**: [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)은 건물 주소를 종이에 길게 적어 들고 다니는 대신, 휴대폰 즐겨찾기에 저장해 두고 바로 길찾기를 누르는 방식과 같다. 목적지는 메모리에 있지만, 찾아가는 실마리는 손안의 빠른 즐겨찾기에 둔다.

---

## Ⅱ. 아키텍처 및 핵심 원리

이 방식의 핵심 수식은 단순하다. **유효 주소 `EA`는 선택된 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)의 내용**이며, 실제 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/)는 `Memory[EA]`에서 읽는다. 즉 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 "어느 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 볼지"만 말하고, 주소 계산의 책임은 이미 준비된 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 값에 맡긴다. 현대 Load-Store 구조에서 메모리 접근 명령이 대부분 이 철학 위에 서 있다.

| 구성 요소 | 역할 | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접에서 중요한 이유 |
| :--- | :--- | :--- |
| [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)의 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 필드 | 사용할 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 번호 지정 | 긴 절대 주소 대신 작은 인덱스만 인코딩한다 |
| [범용 레지스터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/162_gpr/) (General Purpose [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/), [GPR](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/162_gpr/)) | 주소값 보관 | 실행 중 바뀌는 포인터를 빠르게 유지한다 |
| [주소 버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/346_address_bus/) ([Address Bus](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/346_address_bus/)) | 메모리 접근 주소 전달 | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 값이 그대로 메모리 주소가 된다 |
| 캐시/메모리 계층 | 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 저장 | 최종 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/)는 결국 여기서 읽는다 |
| 제어 장치 | 해독과 접근 순서 제어 | "[레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 읽기 → 메모리 읽기" 순서를 만든다 |

아래 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로는 전형적인 동작 순서를 요약한다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Register-indirect data path                                       │
├────────────────────────────────────────────────────────────────────┤
│ IR : LOAD R0, [R2]                                                 │
│          │                                                         │
│          ├─ register field = R2                                    │
│          ▼                                                         │
│ Register file : R2 = 0x1000                                        │
│          │                                                         │
│          ▼                                                         │
│ Address bus  -----------------------------> Cache / Memory         │
│                                              │                     │
│                                              ▼                     │
│                                        M[0x1000] = 42             │
│                                              │                     │
│                                              ▼                     │
│                                           R0 <- 42                │
└────────────────────────────────────────────────────────────────────┘
```

이 구조의 장점은 **[명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 절약**과 **실행 시 유연성**이 동시에 성립한다는 점이다. 예를 들어 32비트 고정 길이 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)에서 64비트 주소를 직접 넣는 것은 불가능하지만, [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 번호는 몇 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)만으로도 표현 가능하다. 반면 실제 주소는 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 폭만큼 유지할 수 있으므로, 작은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 형식으로도 큰 주소 공간을 다룰 수 있다.

또한 이 방식은 반복 처리에 잘 맞는다. 컴파일러는 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 포인터를 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 유지한 뒤 반복마다 값을 읽고, 다음 위치로 포인터만 갱신한다. 그래서 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)은 단일 명령 기법이 아니라, **포인터 기반 프로그램을 하드웨어가 효율적으로 실행하게 만드는 기본 골격**으로 보는 편이 정확하다.

- **📢 섹션 요약 비유**: 이 방식은 창고 안 물건 위치를 창고 벽에 길게 써 붙이는 대신, 작업자의 PDA (Portable Digital Assistant)에 선반 번호를 넣어 두고 바로 찾게 하는 것과 같다. 안내판은 짧아지고, 실제 위치는 계속 바꿔도 따라갈 수 있다.

---

## Ⅲ. 비교 및 연결

[레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)을 이해하려면 "주소를 어디에 두는가"를 기준으로 다른 방식과 비교하는 것이 가장 빠르다. [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)은 주소를 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)에 두고, 메모리 [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)은 주소를 메모리에 두며, [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)은 주소를 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 둔다. 결국 차이는 **유연성과 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)시간을 어느 지점에서 교환하느냐**다.

| 방식 | 유효 주소 계산 | [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) 접근 관점 | 강점 | 약점 |
| :--- | :--- | :--- | :--- | :--- |
| [즉시 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/174_immediate_addressing/) ([Immediate Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/174_immediate_addressing/)) | 주소 계산 없음 | 메모리 접근 없이 상수 사용 | 가장 단순 | 변수 위치 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 불가 |
| [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) ([Register Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)) | [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/)가 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 자체 | 메모리 접근 없음 | 가장 빠름 | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 이미 값이 있어야 함 |
| [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) ([Direct Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)) | `EA = A` | 메모리 1회 | 해석이 단순 | 주소 필드 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수 한계 |
| [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/) ([Indirect Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)) | `EA = Memory[A]` | 포인터용 메모리 + [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)용 메모리 | 매우 유연 | 메모리 접근이 더 많음 |
| [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/) ([Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) [Indirect Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)) | `EA = Register` | [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)용 메모리 1회 | 유연성과 속도의 균형 | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 확보 필요 |
| [변위 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/) ([Displacement Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/)) | `EA = Base Register + Offset` | 구조체·[배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 접근에 강함 | 기준점+상대거리 표현 | 오프셋 해석 필요 |

소프트웨어와의 연결도 분명하다. C 언어의 포인터 역참조 `*p`, [스택 포인터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/) ([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) Pointer, [SP](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/))가 가리키는 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 최상단, 힙 버퍼 시작 주소, 동적 자료구조 순회는 모두 "주소를 값처럼 들고 다닌다"는 점에서 같은 철학을 공유한다. 다만 구조체 필드처럼 기준 주소에서 일정 거리만 더 가면 되는 경우는 순수 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접보다 [변위 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/)이 더 자연스럽다.

실제 고성능 시스템에서는 두 방식이 자주 결합된다. "포인터는 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 두고, 그 포인터 기준으로 오프셋을 더해 필드를 읽는" 패턴이 대표적이다. 그래서 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)은 단독 주제가 아니라, [변위 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/)·자동 증가 (Auto-increment)·로드 스토어 아키텍처와 이어지는 **중심 [허브](/knowledge-base/studynote/03_network/03_physical_layer_media/152_hub_dummy_switching_intelligent/) 개념**으로 기억하는 것이 좋다.

- **📢 섹션 요약 비유**: [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)이 집 주소를 편지에 바로 쓰는 방식이라면, [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)은 주소가 저장된 연락처를 휴대폰에 넣고 필요할 때 꺼내 보는 방식이다. 집이 자주 바뀌면 후자가 훨씬 관리하기 쉽다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 이 방식이 빛나는 상황은 **접근 대상이 실행 중 바뀌고, 그 바뀐 주소를 자주 재사용해야 할 때**다. [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 포인터 순회, 네트워크 버퍼 처리, 시스템 콜 인자 접근, 인터프리터의 바이트코드 포인터, 메모리 복사 루프가 대표적이다. 컴파일러는 이런 경로에서 포인터를 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 고정해 두고, 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근을 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접 형태로 바꿔 메모리 트래픽을 줄인다.

반대로 주소를 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 오래 유지하지 못하면 이점이 줄어든다. [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)가 부족해 포인터가 다시 [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/)에 spill되면, 다음 접근 때 주소 자체를 메모리에서 다시 읽어 와야 한다. 또한 링크드 리스트처럼 다음 노드 주소를 따라가는 포인터 체인이 길어지면, 각 단계마다 캐시 미스 가능성이 커져 "[레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접이니까 빠르다"는 기대가 깨질 수 있다.

아래 흐름은 설계 시 어떤 접근 방식을 우선 고려할지 가르는 기준이다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Choosing register-indirect access                                 │
├────────────────────────────────────────────────────────────────────┤
│ does the target address change at run time?                       │
│   ├─ no  -> prefer direct / immediate / fixed offset access       │
│   └─ yes                                                          │
│        ├─ can the pointer stay in a GPR? -> register indirect     │
│        ├─ repeated field access from one base? -> base + offset   │
│        └─ long pointer chain? -> flatten / cache-optimize layout  │
└────────────────────────────────────────────────────────────────────┘
```

### 실무 판단 기준

1. **포인터를 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 유지할 수 있는가?** 유지 가능해야 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접의 이점이 살아난다.
2. **접근 패턴이 연속적인가?** 연속 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 순회라면 캐시 친화성이 높아 효과가 크다.
3. **필드 접근이 많은가?** 구조체 멤버 접근은 [변위 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/)과 결합하는 편이 낫다.
4. **포인터 체인이 깊은가?** 깊을수록 캐시 미스와 예측 실패가 커지므로 자료구조 재설계가 필요할 수 있다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 단순 연속 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/)인데도 불필요하게 노드 기반 구조를 사용해 포인터 추적을 늘리는 것
- [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 압박을 무시하고 포인터 변수를 과도하게 늘려 spill을 유발하는 것
- "주소를 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 둔다"는 이유만으로 메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 자체가 사라진다고 오해하는 것

- **📢 섹션 요약 비유**: [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)은 택배 기사에게 오늘 갈 집 목록을 내비게이션 즐겨찾기로 넣어 두는 것과 같다. 하지만 골목이 너무 꼬여 있거나 매번 주소록을 다시 꺼내야 한다면, 즐겨찾기만으로 배송 속도가 마법처럼 빨라지지는 않는다.

---

## Ⅴ. 기대효과 및 결론

[레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)의 가장 큰 효과는 **작은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 형식과 넓은 주소 공간 사이를 자연스럽게 연결한다**는 점이다. [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)는 짧게 유지하면서도 실행 중 변경되는 주소를 다룰 수 있어, 포인터 중심 소프트웨어와 현대 Load-Store 아키텍처의 접점이 된다. 이 덕분에 CPU는 고정된 메모리 위치만 읽는 기계가 아니라, 실행 중 움직이는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조를 추적하는 기계가 된다.

물론 한계도 분명하다. 주소는 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에서 빠르게 읽더라도, 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 결국 캐시와 메모리 계층에서 와야 한다. 따라서 캐시 미스, [Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/) ([TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/)) 미스, [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 압박, 포인터 지역성 부족은 그대로 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 변수로 남는다. [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)의 핵심은 "주소 준비를 빠르게 했다"이지 "메모리 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)이 사라졌다"가 아니다.

정리하면 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)은 **주소를 CPU 가까이에 두어 유연성과 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)을 균형 있게 확보하는 방식**이다. 기억할 핵심은 분명하다. **주소는 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)는 메모리에 두고, 그 사이의 비용을 최소화하는 주소 지정 모드**라는 점이다.

- **📢 섹션 요약 비유**: 이 방식은 자주 가는 목적지의 좌표를 자동차 내비게이션 즐겨찾기에 저장해 두는 것과 같다. 길 찾기 시작은 빨라지지만, 실제 도로 정체까지 없어지는 것은 아니라는 점까지 함께 기억해야 한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 유효 주소 (Effective Address, [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)) | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접에서는 선택된 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)의 내용이 EA가 된다 |
| [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/) ([Indirect Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)) | 주소를 한 번 더 따라간다는 철학은 같지만, 중간 저장 위치가 메모리다 |
| [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) ([Register Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)) | [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) 자체가 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 있을 때 사용하는 더 빠른 형태다 |
| [변위 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/) ([Displacement Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/)) | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접에 오프셋 계산을 더해 구조체·[배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 접근을 확장한 형태다 |
| 로드-스토어 아키텍처 ([Load-Store Architecture](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/197_load_store_architecture/)) | 메모리 접근을 제한된 명령으로 통제할 때 핵심적으로 활용된다 |
| 포인터 (Pointer) | 소프트웨어가 주소를 값처럼 다루는 대표적 표현이다 |
| [스택 포인터](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/) ([Stack](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) Pointer, [SP](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/166_sp/)) | 함수 호출과 복귀에서 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접 철학을 매 순간 사용한다 |

### 📈 관련 키워드 및 발전 흐름도

```text
short instruction format
        │
        ▼
direct addressing range limit
        │
        ▼
indirect addressing for flexibility
        │
        ▼
register indirect addressing
        │
        ├──────────────▶ pointer-based traversal
        ├──────────────▶ load-store memory access
        └──────────────▶ displacement / auto-index extension
```

이 흐름도는 "짧은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)"와 "넓은 주소 공간"의 충돌을 해결하는 과정에서 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)이 핵심 징검다리로 자리 잡았음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)은 장난감이 있는 서랍 번호를 종이에 길게 적는 대신, 주머니 속 작은 메모장에 적어 두고 꺼내 보는 방법이에요.
2. 그래서 컴퓨터는 긴 주소를 매번 말하지 않아도, 메모장에 적힌 번호를 보고 바로 서랍을 찾을 수 있어요.
3. 하지만 장난감은 아직 서랍 안에 있으니, 메모장을 빨리 봤다고 해서 서랍까지 가는 시간이 완전히 없어지는 것은 아니에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 178 / 803

← **이전**: [177. 간접 주소 지정 (Indirect)](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)
**다음**: [179. 변위 주소 지정 (Displacement)](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/) →

---
