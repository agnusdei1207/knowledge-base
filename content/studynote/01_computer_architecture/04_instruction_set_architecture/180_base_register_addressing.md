+++
title = "180. 베이스 레지스터 주소 지정 (Base Register)"
date = 2026-04-19

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) (Base [Register Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/))은 [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/) ([Base Register](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/))에 저장된 시작 주소와 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 안의 변위 ([Displacement](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/))를 더해 유효 주소 [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) (Effective Address)를 만드는 방식이다.
> 2. **가치**: 프로그램이나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록이 메모리 어디로 옮겨져도 [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/) 값만 바꾸면 같은 기계어를 재사용할 수 있어, 재배치 (Relocation), 코드 밀도, 메모리 관리 효율을 동시에 높인다.
> 3. **판단 포인트**: 접근 대상이 "한 기준점 주변의 고정 위치"라면 강하지만, 반복마다 위치가 크게 변하는 순회 패턴은 [인덱스 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/) ([Indexed Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/))이나 상대 주소 지정 ([Relative Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/182_relative_addressing/))이 더 적합하다.

---

## Ⅰ. 개요 및 필요성

베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)은 <strong>큰 주소는 <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/">레지스터</a>에 넣고, <a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a>에는 그 기준점에서 얼마나 떨어져 있는지만 적는 방식</strong>이다. [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)처럼 절대 주소를 매번 길게 넣지 않아도 되고, 프로그램이 메모리 다른 위치로 이동해도 기준 주소만 다시 잡아 주면 같은 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)를 그대로 사용할 수 있다.

이 방식이 필요해진 이유는 메모리 주소 공간은 커지는데 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수는 늘 제한되어 있기 때문이다. 절대 주소를 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)마다 싣는 구조는 코드가 커지고, 프로그램을 다른 물리 주소에 적재할 때마다 기계어를 다시 수정해야 하는 부담이 생긴다. 반대로 [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/)를 두면 [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/) ([Operating System](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/))와 로더 (Loader)가 프로그램 시작 주소만 재설정해 동일한 코드와 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/)를 계속 유지할 수 있다.

특히 프로세스별 메모리 구역, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 세그먼트, 재배치 가능한 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/)에서는 이 방식의 효과가 크다. 결국 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)은 <strong>큰 주소 공간과 짧은 <a href="/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/">명령어</a> 사이를 연결하는 실용적 절충안</strong>이다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ 같은 명령어를 다른 적재 위치에서 재사용하는 방식                   │
├────────────────────────────────────────────────────────────────────┤
│ 명령어: LOAD R1, 12(BR)                                            │
│                                                                    │
│ Case A: BR = 4000  -> EA = 4012 -> 프로세스 A의 데이터 접근        │
│ Case B: BR = 9000  -> EA = 9012 -> 프로세스 B의 데이터 접근        │
│                                                                    │
│ 바뀌는 것은 BR 값뿐이고, 명령어 자체는 그대로 유지된다.            │
└────────────────────────────────────────────────────────────────────┘
```

- **📢 섹션 요약 비유**: 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)은 아파트 동은 관리실이 기억하고, 택배 기사에게는 몇 호실인지 만 알려 주는 방식과 같다. 건물이 옆 단지로 옮겨져도 관리실의 기준 주소만 바꾸면 배달 규칙은 그대로 유지된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

핵심 수식은 단순하다. <strong><code>EA = BR + Disp</code></strong> 다. 여기서 `BR`은 [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/) 값, `Disp`는 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)에 포함된 작은 변위, `EA`는 실제 메모리 접근 주소다. 즉 주소를 "큰 기준점"과 "짧은 거리"로 나누어 표현하는 셈이다.

| 구성 요소 | 역할 | 설계 포인트 |
| :--- | :--- | :--- |
| [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/) ([Base Register](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/)) | 현재 코드/[데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 구역의 시작 주소 보관 | [컨텍스트](/knowledge-base/studynote/02_operating_system/01_overview_architecture/033_context/) 스위치나 로더가 갱신 |
| 변위 ([Displacement](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/)) 필드 | 기준점에서의 상대 거리 표현 | [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 폭이 좁을수록 코드 밀도 증가 |
| AGU (Address Generation Unit) | `BR + Disp` 계산 | 파이프라인 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 최소화 |
| 리미트 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) ([Limit Register](/knowledge-base/studynote/02_operating_system/06_memory_management/330_limit_register/)) | 허용 범위 검사 | [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/)와 경계 위반 방지 |
| 캐시/메모리 | 최종 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 제공 | 실제 성능은 지역성에 좌우 |

아래 그림은 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)이 주소 생성과 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)를 함께 처리하는 전형적 흐름을 보여 준다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Base register addressing data path                                 │
├────────────────────────────────────────────────────────────────────┤
│ instruction field        register file                              │
│   disp = +24  ─────┐     BR = 0x4000                                │
│                    │            │                                   │
│                    ▼            ▼                                   │
│              displacement       base read                           │
│                    └──────┬──────┘                                  │
│                           ▼                                         │
│                  AGU: EA = 0x4018                                   │
│                           │                                         │
│               range check with Limit Register                       │
│                  0 <= disp < limit ?                                │
│                           │                                         │
│                 yes ─────────────▶ cache / memory                   │
│                 no  ─────────────▶ protection fault                 │
└────────────────────────────────────────────────────────────────────┘
```

중요한 점은 [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/)가 보통 자주 바뀌는 루프 변수용 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)가 아니라는 것이다. 이 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)는 "현재 프로세스의 주소 기준점"처럼 비교적 안정적인 영역을 가리키고, [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)마다 작은 변위만 달라진다. 그래서 구조체 필드 접근, [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 세그먼트 내부 [참조](/knowledge-base/studynote/05_database/05_distributed_nosql_newsql/316_reference_pattern_nosql/), [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 프레임 근처 접근처럼 <strong>한 기준점 주변의 값들을 반복해서 읽는 상황</strong>에 강하다.

또한 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 관점에서도 의미가 크다. 단순히 편하게 주소를 줄여 적는 것이 아니라, 베이스와 리미트 조합을 쓰면 프로세스가 자기 구역 밖으로 나가는 접근을 하드웨어적으로 막을 수 있다. 즉 이 방식은 주소 계산 기법이면서 동시에 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) [메모리 보호](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/307_memory_protection/) 메커니즘과도 맞닿아 있다.

- **📢 섹션 요약 비유**: 이 구조는 창고에서 A구역이라는 기준 표지를 먼저 세워 두고, 그 안에서 24번 칸만 적어 물건을 찾는 방식과 같다. 구역표와 허용 범위를 함께 보면 잘못된 창고 침입도 바로 막을 수 있다.

---

## Ⅲ. 비교 및 연결

베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)은 [변위 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/) ([Displacement Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/))의 대표 파생형이지만, **무엇을 기준점으로 삼느냐** 에서 다른 주소 지정 방식과 경계가 갈린다. 이 차이를 보면 왜 [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/)가 재배치와 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)에 강한지, 왜 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)가 반복 순회에 강한지가 분명해진다.

| 방식 | 기준점 | 더해지는 값 | 강한 상황 | 약한 상황 |
| :--- | :--- | :--- | :--- | :--- |
| [직접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/) ([Direct Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/176_direct_addressing/)) | 없음 | 절대 주소 자체 | 해석 단순 | 긴 주소 필드, 재배치 불리 |
| 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/) (Base [Register Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)) | [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/) | 작은 상수 변위 | 재배치, 세그먼트 접근, [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) | 동적 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) 순회 |
| [인덱스 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/) ([Indexed Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/)) | 기준 주소 | [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 값 | [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/), 반복 순회 | 기준 구역 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 설명엔 약함 |
| 상대 주소 지정 ([Relative Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/182_relative_addressing/)) | [PC](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/) (Program [Counter](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)) | 분기 오프셋 | 위치 독립 코드, 분기 | 일반 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 접근엔 제한 |
| [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/) ([Register Indirect Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/178_register_indirect_addressing/)) | [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 안의 정확한 주소 | 없음 | 포인터 추적 | 주변 필드 반복 접근 비효율 |

베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)의 핵심은 <strong>기준점이 <a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/">레지스터</a> 안에 있고 그 기준점 자체가 재배치 가능하다</strong> 는 데 있다. 반면 [인덱스 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/)은 루프마다 바뀌는 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)를 중심으로 사고하므로 반복 처리에 더 적합하다. 상대 주소 지정은 PC를 기준으로 삼아 위치 독립 코드와 분기 거리를 표현하는 데 강하다.

[운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)와도 바로 연결된다. 프로세스를 물리 메모리의 어디에 적재하든 [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/)만 바꿔 주면 되므로, 로더와 메모리 관리자는 절대 주소를 대량 수정하지 않고도 프로그램을 실행할 수 있다. 따라서 이 방식은 단순한 [ISA](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/) ([Instruction Set Architecture](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/157_isa/)) 편의 기능이 아니라 <strong>재배치 가능한 실행 모델의 기반</strong>이다.

- **📢 섹션 요약 비유**: [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/)는 건물 기준으로 몇 호인지 찾는 방식이고, [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/) [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)는 복도를 몇 칸 더 갈지 세는 방식이다. 둘 다 더하기를 쓰지만, 하나는 정착된 기준점을 잡고 다른 하나는 움직이는 발걸음을 센다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)은 로더, 컴파일러, [운영체제](/knowledge-base/studynote/02_operating_system/01_overview_architecture/001_operating_system_purpose/)가 함께 만드는 약속으로 드러난다. 프로그램 시작 시 로더가 코드나 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 영역의 기준 주소를 잡아 주고, 실행 중에는 컴파일러가 만든 `base + displacement` 형태 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)가 전역 변수, 지역 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/), 구조체 필드를 읽는다. 이 구조는 특히 재배치 가능한 [모듈](/knowledge-base/studynote/04_software_engineering/04_testing_quality/192_module_independence/), 임베디드 메모리 맵, 단순 세그먼트 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 설계에서 중요하다.

### 실무 판단 기준

1. **접근 대상이 한 기준점 주변에 모여 있는가?** 전역 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 블록, [스택](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/057_stack/) 프레임, 구조체처럼 지역성이 강하면 적합하다.
2. **프로그램 적재 위치가 자주 달라질 수 있는가?** 재배치와 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)가 중요할수록 [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/)의 가치가 커진다.
3. **변위 폭이 충분한가?** 너무 좁으면 기준 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)를 자주 다시 잡아야 해서 코드가 늘고 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 압박도 커진다.
4. <strong><a href="/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/">보호</a> 경계가 필요한가?</strong> 리미트 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)나 [페이지](/knowledge-base/studynote/01_computer_architecture/07_virtual_memory_os_integration/286_page_frame/) [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)와 함께 설계해야 메모리 안전성이 살아난다.

```text
┌────────────────────────────────────────────────────────────────────┐
│ Addressing choice in practice                                       │
├────────────────────────────────────────────────────────────────────┤
│ target stays near one stable region?                                │
│   ├─ yes                                                            │
│   │   ├─ need relocation/protection? -> Base Register Addressing    │
│   │   └─ fixed nearby branch target? -> Relative Addressing         │
│   └─ no                                                             │
│       ├─ index changes every iteration? -> Indexed Addressing       │
│       └─ exact pointer already known? -> Register Indirect          │
└────────────────────────────────────────────────────────────────────┘
```

### [안티패턴](/knowledge-base/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)

- [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 전체를 순회하면서도 매번 [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/)만 바꾸려 해 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 갱신 오버헤드를 키우는 설계
- 베이스만 두고 범위 검사를 생략해 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/) 기능을 놓치는 설계
- 변위 범위가 부족한데 무리하게 하나의 베이스에 모든 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 몰아넣는 설계

즉 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)은 **기준점이 안정적일 때** 가장 빛난다. 기준점이 계속 움직이는 문제를 억지로 여기에 넣으면 설계가 복잡해지고, 오히려 [인덱스 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/)보다 불리해진다.

- **📢 섹션 요약 비유**: 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)은 쇼핑몰 층별 안내도처럼 기준 층은 고정하고 몇 번째 매장인지만 말할 때 효율적이다. 그런데 매장 자체가 계속 움직이는 임시 장터라면 다른 길찾기 방식이 더 낫다.

---

## Ⅴ. 기대효과 및 결론

베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)의 가장 큰 효과는 **긴 주소를 짧게 표현하면서도 재배치 가능성을 확보한다** 는 점이다. 덕분에 같은 기계어를 서로 다른 메모리 위치에서 재사용할 수 있고, 프로그램별 주소 공간 격리도 설계하기 쉬워진다. 이는 [초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 세그먼트 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)부터 현대 컴파일러의 베이스 포인터 기반 접근까지 넓게 이어지는 장점이다.

하지만 모든 메모리 접근을 이 한 가지로 해결할 수는 없다. 반복 [인덱스](/knowledge-base/studynote/05_database/03_relational_model/154_database_index_b_tree_search_optimization/)가 크게 변하는 [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) 순회, 분기 대상 계산, 완전 동적 포인터 추적은 각각 [인덱스 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/), 상대 주소 지정, [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) [간접 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/177_indirect_addressing/)이 더 자연스럽다. 또한 [베이스 레지스터](/knowledge-base/studynote/02_operating_system/06_memory_management/329_base_register/) 수가 부족하면 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 압박과 추가 주소 계산이 생긴다.

정리하면 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)은 <strong>주소 전체를 매번 말하지 않고, 기준점과 거리로 메모리를 다루는 대표적 재배치 친화 방식</strong>으로 기억하면 좋다. 즉 이 기법의 핵심은 빠른 덧셈 그 자체보다, <strong>프로그램을 옮겨도 같은 코드가 계속 통하도록 만드는 주소 관리 철학</strong>에 있다.

- **📢 섹션 요약 비유**: 좋은 캠퍼스 안내는 건물 전체 좌표를 매번 읽지 않는다. 공학관 기준 2층 12호실처럼 기준점만 잡아 주면, 캠퍼스가 커져도 길찾기 규칙은 훨씬 단순해진다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| [EA](/knowledge-base/studynote/12_it_management/03_ea_isp/110_enterprise_architecture_ea/) (Effective Address) | 베이스 값과 변위를 합쳐 실제 접근 주소를 만든다 |
| [변위 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/) ([Displacement Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/)) | 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)의 상위 원리다 |
| 리미트 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) ([Limit Register](/knowledge-base/studynote/02_operating_system/06_memory_management/330_limit_register/)) | 베이스 기준 접근 범위를 검사해 [보호](/knowledge-base/studynote/02_operating_system/10_security/571_protection_vs_security/)를 제공한다 |
| [인덱스 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/) ([Indexed Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/)) | 동적 반복 순회에 강한 인접 개념이다 |
| 상대 주소 지정 ([Relative Addressing](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/182_relative_addressing/)) | PC를 기준점으로 삼는 변형이다 |
| 재배치 (Relocation) | 베이스 값 갱신만으로 프로그램 적재 위치를 바꾸는 효과다 |
| 로더 (Loader) | 실행 시 베이스 값을 세팅하는 대표 주체다 |

### 📈 관련 키워드 및 발전 흐름도

```text
긴 절대 주소의 비효율
        │
        ▼
기준점 + 변위라는 분리 표현
        │
        ▼
베이스 레지스터 주소 지정
        │
        ├──────────────▶ 재배치 (Relocation)와 메모리 보호
        ├──────────────▶ 인덱스 주소 지정으로 반복 접근 확장
        └──────────────▶ PC-relative와 위치 독립 코드로 분화
```

이 흐름도는 주소 전체를 [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/)에 넣기 어려운 문제에서 출발해, 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)이 재배치와 파생 주소 지정 방식의 중심축이 되었음을 보여 준다.

### 👶 어린이를 위한 3줄 비유 설명

1. 베이스 [레지스터 주소 지정](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)은 큰 서랍장의 시작 칸을 먼저 기억해 두고, 거기서 세 칸 옆처럼 찾는 방법이에요.
2. 그래서 서랍장 자체를 다른 방으로 옮겨도 시작 칸 번호만 다시 알려 주면 같은 설명으로 물건을 찾을 수 있어요.
3. 컴퓨터는 이렇게 큰 주소를 다 말하지 않고도 빠르고 똑똑하게 메모리를 찾는답니다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 180 / 803

← **이전**: [179. 변위 주소 지정 (Displacement)](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/179_displacement_addressing/)
**다음**: [181. 인덱스 주소 지정 (Indexed)](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/181_indexed_addressing/) →

---
