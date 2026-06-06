---
title: "Double Word"
date: "2026-03-19"
tags:
  - "studynote-computer-architecture"
---

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)(Double [Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/), Dword)는 기준 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)의 2배 크기를 뜻하는 상대적 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 단위다.
> 2. **가치**: 더 넓은 정수 범위, 더 큰 주소 공간, 더 높은 계산 정밀도를 다룰 수 있게 해 준다.
> 3. **판단 포인트**: [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) 기준은 아키텍처와 [ABI](/studynote/02_operating_system/01_overview_architecture/015_abi/)([Application Binary Interface](/studynote/02_operating_system/01_overview_architecture/015_abi/))에 따라 달라지므로, "더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) = 항상 64비트"라고 단정하면 설계를 잘못 읽게 된다.

---

## Ⅰ. 개요 및 필요성

컴퓨터는 처음부터 큰 숫자를 다루지 못했다. [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)([Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)) 크기가 작으면 [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), 주소, 길이 값을 표현할 때 금방 한계에 부딪힌다. 더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)는 이 한계를 두 배 단위로 넓혀 주는 가장 기본적인 확장 개념이다.

용어는 환경마다 다르다. 16비트 시대의 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)와 32비트 시대의 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)는 같은 말이 아니고, 따라서 더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)도 고정된 숫자가 아니다. Windows API의 `DWORD`는 역사적으로 32비트를 뜻하지만, 현대 64비트 시스템의 기본 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)와는 관계가 달라진다.

```text
바이트(8b) --> 워드 --> 더블 워드 --> 쿼드 워드
                 |        |
                 |        +- 2개의 워드를 묶은 확장 폭
                 +- 기준은 아키텍처마다 다름
```

이 구조의 핵심은 "두 개를 묶어서 하나로 본다"는 점이다. 단순히 크기가 아니라 연산과 저장의 관점을 바꾼다.

- **📢 섹션 요약 비유**: 작은 상자 하나로는 큰 장난감을 못 담는다. 상자 두 개를 이어 붙이면 더 긴 물건을 한 번에 넣을 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)는 보통 상위 절반과 하위 절반으로 나뉘어 처리된다. [ALU](/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)([Arithmetic Logic Unit](/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/))는 올림수(carry)를 다음 절반으로 넘기며, [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)와 메모리 버스는 이 2배 폭을 한 번에 다룰 수 있도록 설계된다.

| 단위 | 전형적 의미(x86 관점) | 실무 메모 |
| :-- | :-- | :-- |
| [Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) | 8비트 | 주소 지정의 기본 단위 |
| [Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) | 16비트 | [초기](/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) x86의 자연 단위 |
| Double [Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) | 32비트 | `DWORD`, Windows API에서 자주 사용 |
| Quad [Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) | 64비트 | 포인터/[카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/)/64비트 연산 |

```text
[상위 32비트] -+
               +--> 더블 워드(64비트)
[하위 32비트] -+
```

상위와 하위는 논리적으로 하나지만, 실제 메모리 배치에서는 엔디언(Endianness)에 따라 순서가 달라질 수 있다. 그래서 [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 형식이나 네트워크 [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/)에서는 "순서"를 명확히 적어야 한다.

- **📢 섹션 요약 비유**: 두 칸짜리 도시락은 밥과 반찬이 따로 들어가지만, 한 번 들고 가는 상자다. 안쪽은 나뉘어도 밖에서는 하나처럼 쓴다.

---

## Ⅲ. 비교 및 연결

더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)는 단순히 "크다"가 아니라 "어디서 쓰이느냐"가 중요하다. 메모리 주소, [카운터](/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 포맷, MMIO(Memory-Mapped I/O) [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)처럼 고정 폭이 필요한 곳에서 특히 유용하다.

| 비교 대상 | 의미 | 판단 포인트 |
| :-- | :-- | :-- |
| [Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) | 기본 연산 폭 | CPU 세대에 따라 달라짐 |
| Double [Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) | 2배 폭 | 큰 정수, 주소, 구조체 필드 |
| [Double Precision](/studynote/01_computer_architecture/02_data_representation_arithmetic/090_double_precision/) | 64비트 [부동소수점](/studynote/01_computer_architecture/02_data_representation_arithmetic/087_floating_point/) | 크기와 의미가 다름 |
| Pointer | 주소값 | [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) 폭과 직접 연결 |

`double` 타입과 더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)는 종종 같은 64비트를 쓰지만, 의미는 다르다. 하나는 수치 표현이고, 하나는 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 단위다. 이 차이를 놓치면 타입 이름만 보고 자료형을 오해한다.

- **📢 섹션 요약 비유**: 같은 2층 버스라도 사람을 실어 나를 수도 있고, 짐을 실어 나를 수도 있다. 크기만 같다고 역할도 같은 것은 아니다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)를 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/), [ABI](/studynote/02_operating_system/01_overview_architecture/015_abi/), [프로토콜](/studynote/03_network/06_network_layer_ip/295_protocol_field_tcp_udp_icmp/) 필드, [파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/) 헤더에서 자주 본다. 이때 중요한 것은 정렬(alignment), 부호(signedness), 엔디언, 그리고 "이 값이 몇 비트인가"를 문서화하는 일이다.

### [체크리스트](/studynote/04_software_engineering/11_testing_validation/435_checklist_based_testing/)
1. 필드 폭이 명시되어 있는가?
2. 부호 있는 값과 없는 값이 분리되어 있는가?
3. 32비트/64비트 환경에서 타입 크기가 달라지지 않는가?
4. 메모리 정렬이 [성능](/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 저하를 일으키지 않는가?
5. 외부 시스템과의 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)([파일](/studynote/02_operating_system/09_file_system/501_file_definition_logical_record/), 네트워크, [ABI](/studynote/02_operating_system/01_overview_architecture/015_abi/))이 적혀 있는가?

### [안티패턴](/studynote/04_software_engineering/02_requirements_analysis/128_water_scrum_fall_anti_pattern/)
- `int`를 아무 문맥에서나 32비트라고 가정
- `DWORD`와 `double`을 같은 의미로 착각
- 엔디언을 문서화하지 않음
- 구조체 정렬을 무시하고 [레지스터](/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 매핑

기술사 관점에서는 "숫자가 커진다"보다 "표현 경계가 넓어진다"를 강조해야 한다. 그 경계가 시스템 설계와 [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/) 문제를 함께 만들기 때문이다.

- **�� 섹션 요약 비유**: 큰 우체통이 있어도 편지 순서와 주소가 틀리면 배달이 엉킨다. 크기보다 규칙이 먼저다.

---

## Ⅴ. 기대효과 및 결론

더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)는 큰 숫자와 큰 주소를 다루게 해 주고, 정밀한 계산과 대형 시스템 설계를 가능하게 한다. 하지만 기준 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)가 무엇인지, 어떤 아키텍처를 말하는지 항상 함께 적어야 혼동이 없다.

결론적으로 더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)는 "두 배의 크기"가 아니라 "두 배의 사고 범위"다. 단위를 넓히는 순간 연산 범위, 정렬, [호환성](/studynote/04_software_engineering/06_software_architecture/344_compatibility_usability/)까지 같이 생각해야 한다.

- **📢 섹션 요약 비유**: 두 바구니를 이어 붙이면 더 많은 열매를 담을 수 있지만, 손잡이를 어디에 붙일지도 같이 정해야 한다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :-- | :-- |
| [Byte](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) | 주소 지정의 최소 단위 |
| [Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) | CPU 자연 연산 폭 |
| Double [Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)(DWORD) | 2배 폭의 정수 단위 |
| Quad [Word](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/) | 더 넓은 정수/주소 |
| [ABI](/studynote/02_operating_system/01_overview_architecture/015_abi/)([Application Binary Interface](/studynote/02_operating_system/01_overview_architecture/015_abi/)) | 타입 크기와 호출 규약 |
| Endianness | [바이트](/studynote/01_computer_architecture/02_data_representation_arithmetic/074_byte/) 배치 순서 |

### 📈 관련 키워드 및 발전 흐름도

```text
8비트 바이트
    |
    v
16/32비트 워드
    |
    v
더블 워드(DWORD)
    |
    v
64비트 주소/정밀도
    |
    v
ABI 호환성과 데이터 포맷 표준화
```

이 흐름은 하드웨어의 폭 확장이 곧 소프트웨어 경계 정의로 이어진다는 점을 보여준다. 이후에는 64비트가 기본이 되면서 더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)라는 이름 자체도 역사적 표현이 되었다.

### 👶 어린이를 위한 3줄 비유 설명

1. 작은 가방 하나에는 공룡 장난감이 안 들어가요.
2. 가방 두 개를 붙이면 더 큰 장난감을 넣을 수 있어요.
3. 더블 [워드](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)는 두 칸짜리 가방처럼 큰 [데이터](/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 담는 방법이에요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 76 / 803

<- **이전**: [75. 워드 (Word)](/studynote/01_computer_architecture/02_data_representation_arithmetic/075_word/)
**다음**: [77. 기수 (Radix)](/studynote/01_computer_architecture/02_data_representation_arithmetic/077_radix/) ->

---
