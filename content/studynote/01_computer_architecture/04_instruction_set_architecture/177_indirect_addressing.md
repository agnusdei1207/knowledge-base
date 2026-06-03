+++
title = "177. 간접 주소 지정 (Indirect)"
date = 2026-03-19

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 간접 주소 지정 (Indirect Addressing)은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)의 주소 필드가 최종 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치가 아니라, <strong>그 위치가 저장된 메모리 칸</strong>을 먼저 가리키는 방식으로 `EA (Effective Address) = M[A]`로 이해한다.
> 2. **가치**: 짧은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 주소 필드로도 더 넓은 주소 공간과 동적 자료구조를 다룰 수 있어, 포인터 기반 소프트웨어와 주소 재배치의 토대를 제공한다.
> 3. **판단 포인트**: 유연성의 대가로 포인터를 한 번 더 따라가야 하므로, 캐시 미스와 지연시간이 민감한 경로에서는 [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)이나 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접 주소 지정보다 불리할 수 있다.

---

## Ⅰ. 개요 및 필요성

간접 주소 지정 (Indirect Addressing)은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)의 주소 필드가 곧바로 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 위치를 뜻하지 않고, <strong>최종 주소가 들어 있는 메모리 칸</strong>을 먼저 가리키는 주소 지정 방식이다. [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) ([Direct Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/))이 `EA = A`였다면, 간접 주소 지정은 `EA = M[A]`가 된다. 즉 프로세서는 "어디로 가야 하는가"를 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)에서 바로 읽지 않고, 한 번 더 메모리에 물어본 뒤 최종 목적지에 도달한다.

이 방식이 필요해진 이유는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 길이와 주소 공간의 성장이 서로 다른 속도로 커졌기 때문이다. 예를 들어 주소 필드가 12비트라면 [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)으로는 4,096개 위치밖에 표현하지 못하지만, 메모리 한 [워드](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) ([Word](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/))가 32비트 주소를 저장할 수 있다면 그 한 칸을 "주소 보관함"으로 써서 훨씬 넓은 공간을 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)할 수 있다. 또한 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 이동하더라도 포인터가 저장된 칸만 바꾸면 되므로, 코드 수정 없이 접근 대상을 바꿀 수 있다는 점도 중요하다.

아래 그림은 간접 주소 지정이 "주소를 한 번 더 따라가는 구조"라는 점을 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Indirect addressing: follow the address in memory                 │
├────────────────────────────────────────────────────────────────────┤
│ instruction field A = 100                                         │
│                 │                                                  │
│                 ▼                                                  │
│ Memory[100] = 5000        -> pointer slot                         │
│                 │                                                  │
│                 ▼                                                  │
│ Memory[5000] = operand    -> actual data                          │
│                                                                    │
│ direct mode    : EA = A                                           │
│ indirect mode  : EA = Memory[A]                                   │
└────────────────────────────────────────────────────────────────────┘
```

핵심은 주소 필드 자체가 좁아도, 메모리 안에 더 넓은 주소를 저장해 두면 간접적으로 더 큰 세계를 다룰 수 있다는 점이다. 그래서 간접 주소 지정은 단순한 문법 차이가 아니라, 작은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)와 큰 메모리 사이를 연결하는 확장 장치로 이해해야 한다.

- **📢 섹션 요약 비유**: 간접 주소 지정은 편지 봉투에 친구 집 주소를 바로 쓰는 대신, 먼저 친구가 남긴 "새 주소 안내 쪽지"가 있는 사물함을 찾아가고, 그 쪽지를 읽은 뒤 진짜 집으로 가는 방식과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

간접 주소 지정의 실행 핵심은 <strong>포인터 획득 단계</strong>와 <strong>실제 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 접근 단계</strong>가 분리된다는 점이다. [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 해독한 뒤 주소 필드 `A`를 메모리 주소 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) (Memory Address [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/), MAR)에 넣고 한 번 읽으면, 메모리 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) (Memory [Data](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/), [MDR](/knowledge-base/studynote/09_security/04_endpoint_security/327_mdr/))에 최종 주소가 들어온다. 이후 그 값을 다시 MAR에 넣어 두 번째 메모리 접근을 수행하면 비로소 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/)를 얻는다. [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 인출을 제외하고도 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) 접근에 메모리 사이클이 추가로 하나 더 필요한 셈이다.

| 구성 요소 | 역할 | 간접 주소 지정에서 중요한 이유 |
| :--- | :--- | :--- |
| 주소 필드 `A` | 첫 번째로 방문할 위치 | 최종 주소가 저장된 칸을 가리킨다 |
| `M[A]` | 포인터 값 | 유효 주소 `EA`가 된다 |
| `EA` | 실제 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) 주소 | 두 번째 메모리 접근의 목적지다 |
| `M[EA]` | 실제 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) | CPU가 연산에 사용할 값이다 |

다음 그림은 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 경로 수준에서 간접 주소 지정이 어떻게 동작하는지 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Micro-steps of indirect addressing                                 │
├────────────────────────────────────────────────────────────────────┤
│ IR.address ----> MAR ----> Memory read ----> MDR = pointer        │
│                           cycle 1                                 │
│                                                                    │
│ MDR(pointer) -> MAR ----> Memory read ----> MDR = operand         │
│                           cycle 2                                 │
│                                                                    │
│ result: EA = pointer, operand = Memory[EA]                        │
└────────────────────────────────────────────────────────────────────┘
```

이 구조 때문에 간접 주소 지정은 유연하지만 느릴 수밖에 없다. 첫 번째 접근이 포인터를 읽는 동안 캐시 미스가 나면 지연이 커지고, 두 번째 접근에서 또 다른 캐시 미스가 나면 흔히 말하는 포인터 체이싱 (Pointer Chasing) 병목이 발생한다. 그래서 현대 구조는 순수 메모리 간접 주소 지정 자체를 남발하기보다, 일단 포인터를 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)에 올린 뒤 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접 주소 지정 ([Register Indirect Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/178_register_indirect_addressing/))으로 후속 접근을 빠르게 처리하는 방향으로 발전했다.

또한 이 원리는 한 단계로 끝날 수도 있지만, 이론적으로는 `EA = M[M[A]]`처럼 다중 간접도 가능하다. 다만 단계가 늘수록 지연과 예측 불가능성이 커지므로, 실제 시스템에서는 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/)과 단순성을 위해 단계를 제한하거나 캐시·변환 버퍼로 보완한다.

- **📢 섹션 요약 비유**: 간접 주소 지정은 건물 안내 데스크에서 목적지 호수를 먼저 확인하고, 그다음 엘리베이터를 타고 실제 사무실로 가는 절차와 같다. 길 찾기는 쉬워지지만, 안내 데스크를 거치는 시간이 추가된다.

---

## Ⅲ. 비교 및 연결

간접 주소 지정의 가치는 다른 주소 지정 방식과 비교할 때 더 분명해진다. [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)은 단순하고 빠르지만 주소 필드 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수에 묶이고, [즉시 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/174_immediate_addressing/) ([Immediate Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/174_immediate_addressing/))은 상수 처리에는 강하지만 메모리 변수를 가리킬 수 없다. 반면 간접 주소 지정은 한 번 더 돌아가는 대신, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 어디로 이동하든 포인터 값만 바꿔 대응할 수 있다.

| 방식 | 유효 주소 계산 | 장점 | 약점 |
| :--- | :--- | :--- | :--- |
| [즉시 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/174_immediate_addressing/) ([Immediate Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/174_immediate_addressing/)) | 주소 계산 없음 | 상수 처리에 가장 빠름 | 메모리 위치 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/) 불가 |
| [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) ([Direct Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)) | `EA = A` | 단순하고 빠름 | 주소 범위와 재배치에 취약 |
| 간접 주소 지정 (Indirect Addressing) | `EA = M[A]` | 넓은 주소 공간, [동적 연결](/knowledge-base/studynote/02_operating_system/06_memory_management/332_dynamic_linking/) | 메모리 접근 1회 추가 |
| [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접 주소 지정 ([Register Indirect Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/178_register_indirect_addressing/)) | `EA = R` | 빠르고 유연함 | 먼저 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 준비 필요 |
| [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) 상대 주소 지정 ([PC-Relative](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/182_relative_addressing/) Addressing) | `EA = PC + d` | 위치 독립 코드에 유리 | 기준 주소와 변위 해석 필요 |

이 비교에서 중요한 판단 포인트는 <strong>유연성을 어디서 확보하느냐</strong>다. 간접 주소 지정은 메모리 안의 포인터를 따라가며 유연성을 얻고, [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접 주소 지정은 CPU 내부 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 활용해 그 유연성을 더 빠르게 구현한다. 그래서 현대 프로세서 관점에서는 순수한 메모리 간접 주소 지정이 교과서적 원형이라면, 실제 고성능 구현은 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접과 캐시 계층으로 그 개념을 최적화한 형태에 가깝다.

또한 간접 주소 지정은 소프트웨어 개념과도 자연스럽게 연결된다. C 언어의 포인터 역참조, 링크드 리스트의 다음 노드, 객체의 가상 함수 테이블, 운영체제의 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)은 모두 "직접 값이 아니라 그 값을 찾기 위한 또 다른 위치"를 따른다는 점에서 같은 철학을 공유한다. 다만 [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/)은 주소 변환 구조이지 ISA의 주소 지정 모드 그 자체는 아니라는 점은 구분해서 기억해야 한다.

- **📢 섹션 요약 비유**: [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)이 지도에 목적지가 바로 적힌 경우라면, 간접 주소 지정은 안내 표지판을 먼저 읽고 다음 길로 꺾는 여행과 같다. 한 번 더 확인해야 하지만, 목적지가 바뀌어도 표지판만 바꾸면 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 간접 주소 지정이 빛나는 곳은 접근 대상이 자주 바뀌거나, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조가 실행 중에 연결·해제되는 영역이다. 예를 들어 링크드 리스트, 트리, 해시 버킷 체인처럼 "다음 위치"가 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 안에 저장되는 구조는 간접 주소 지정 철학 없이는 설명하기 어렵다. 함수 포인터 테이블, 점프 테이블, 동적 디스패치, 운영체제의 주소 변환 계층도 마찬가지다.

반대로 고정된 하드웨어 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)나 매우 짧은 실시간 제어 루프에서는 간접 주소 지정이 오히려 부담이 될 수 있다. 매번 포인터를 따라가야 하므로 지연시간이 늘고, 메모리 지역성이 나쁘면 캐시 미스로 실행 시간이 흔들리기 때문이다. 이런 구간은 [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/), [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/), 또는 미리 계산한 베이스+오프셋 방식이 더 낫다.

아래 흐름은 설계 시 간접 주소 지정을 어디에 쓸지 빠르게 가르는 기준이다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ When should indirection be used?                                  │
├────────────────────────────────────────────────────────────────────┤
│ target address changes at run time?                               │
│   ├─ yes -> indirection is useful                                 │
│   └─ no                                                           │
│        ├─ fixed hardware register? -> direct access preferred     │
│        └─ hot inner loop? -> keep pointer in register if possible │
└────────────────────────────────────────────────────────────────────┘
```

### 실무 판단 기준

1. **접근 대상이 이동하는가?** [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구조 재배치나 동적 바인딩이 필요하면 간접 주소 지정이 유리하다.
2. **지연시간 예산이 빡빡한가?** 캐시 미스 두 번을 감당하기 어려운 실시간 경로라면 피하는 편이 안전하다.
3. <strong>포인터를 <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/">레지스터</a>에 올릴 수 있는가?</strong> 가능하다면 순수 메모리 간접보다 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접이 더 현실적이다.
4. **추적 단계가 깊어지는가?** 다중 간접은 디버깅 난이도와 지연을 함께 키운다.

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- 단순 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 순회처럼 연속 접근이 가능한데도 불필요하게 포인터 체인을 만드는 것
- 간접 주소 지정이 "무조건 현대적이고 유연하다"고 보고 캐시 비용을 무시하는 것
- [페이지 테이블](/knowledge-base/studynote/02_operating_system/06_memory_management/353_page_table/) 같은 주소 변환 구조와 [ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/) 주소 지정 모드를 완전히 같은 개념으로 섞어 설명하는 것

- **📢 섹션 요약 비유**: 간접 주소 지정은 사무실 전화번호부를 통해 담당자를 찾는 방식이라 조직이 자주 바뀌면 편하지만, 당장 소방서에 전화해야 하는 긴급 상황에서는 단축번호보다 느리다.

---

## Ⅴ. 기대효과 및 결론

간접 주소 지정의 가장 큰 효과는 <strong>코드와 <a href="/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/">데이터</a> 위치를 느슨하게 분리</strong>한다는 점이다. [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 최종 주소를 직접 품지 않아도 되므로 작은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 형식으로 더 큰 메모리 공간을 다룰 수 있고, 포인터 기반 자료구조나 [동적 연결](/knowledge-base/studynote/02_operating_system/06_memory_management/332_dynamic_linking/)도 자연스럽게 구현할 수 있다. 이 덕분에 컴퓨터는 고정된 위치의 값만 읽는 기계에서, 실행 중 구조가 바뀌는 복잡한 소프트웨어를 다루는 기계로 진화할 수 있었다.

하지만 이 유연성은 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 세금을 동반한다. 메모리를 한 번 더 읽는 비용, 캐시 지역성 악화, 디버깅 복잡도 증가는 모두 간접 주소 지정이 감수해야 할 대가다. 그래서 현대 시스템은 간접 주소 지정을 버리지 않되, 캐시, 변환 색인 버퍼 ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/), [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/)), [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접, 프리페치로 비용을 낮추는 방향을 택한다.

정리하면 간접 주소 지정은 "주소를 한 번 더 따라가서 목적지에 도달하는" 구조다. 기억할 핵심은 분명하다. <strong>작은 <a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a>로 큰 주소 공간과 동적 구조를 다루게 해 주지만, <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/">성능</a>과 단순성을 일부 희생하는 교환 <a href="/knowledge-base/studynote/05_database/02_modeling_normalization/083_relationship_in_er_model/">관계</a></strong>라는 점이다.

- **📢 섹션 요약 비유**: 간접 주소 지정은 여행 앱의 공유 링크와 같다. 링크 하나만 바꿔도 목적지를 다른 곳으로 바꿀 수 있지만, 앱을 한 번 열어 확인해야 하므로 종이에 바로 적힌 주소보다는 한 단계 더 느리다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| 유효 주소 (Effective Address, [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/)) | 간접 주소 지정에서는 `EA = M[A]`로 계산된다 |
| [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) ([Direct Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)) | `EA = A`이므로 간접 주소 지정의 기준 비교축이 된다 |
| [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 간접 주소 지정 ([Register Indirect Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/178_register_indirect_addressing/)) | 메모리 간접의 유연성을 CPU 내부에서 더 빠르게 구현한 형태다 |
| 포인터 (Pointer) | 간접 주소 지정의 소프트웨어적 표현이다 |
| 링크드 리스트 ([Linked List](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/056_linked_list/)) | 다음 노드 주소를 따라가는 전형적 응용 구조다 |
| [TLB](/knowledge-base/studynote/02_operating_system/06_memory_management/357_tlb/) ([Translation Lookaside Buffer](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/291_tlb/)) | 주소를 다시 찾는 비용을 줄이는 [하드웨어 보조](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/527_hardware_assisted_virtualization/) 구조다 |

### 📈 관련 키워드 및 발전 흐름도

```text
small instruction address field
          │
          ▼
direct addressing hits range limit
          │
          ▼
indirect addressing  EA = Memory[A]
          │
          ├──────────────▶ pointer-based data structures
          │
          ├──────────────▶ dynamic binding and jump tables
          │
          ▼
register-indirect / TLB / cache-based optimization
```

이 흐름도는 간접 주소 지정이 단순한 우회 기법이 아니라, 주소 필드 한계를 넘어 동적 자료구조와 현대 메모리 최적화로 이어지는 다리 역할을 한다는 점을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 간접 주소 지정은 장난감이 있는 서랍 번호를 바로 주는 대신, 먼저 "어느 서랍을 열어야 하는지 적힌 쪽지"가 든 상자를 찾아가는 방법이에요.
2. 그래서 한 번 더 열어 봐야 하지만, 장난감 위치가 바뀌어도 쪽지만 바꾸면 다시 찾을 수 있어요.
3. 컴퓨터는 이렇게 한 번 더 물어보는 대신 더 많은 물건과 더 복잡한 연결을 다룰 수 있게 돼요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 177 / 803

← **이전**: [176. 직접 주소 지정 (Direct)](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)
**다음**: [178. 레지스터 간접 주소 지정 (Register Indirect)](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/178_register_indirect_addressing/) →

---
