+++
title = "58. 시프트 레지스터 (Shift Register)"
date = 2026-04-19

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 시프트 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)(Shift [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/))는 [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)([Flip-Flop](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/))을 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)로 연결해 클록마다 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 한 칸씩 이동시키는 순차 논리회로다.
> 2. **가치**: [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/)-[병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 변환과 2의 거듭제곱 연산, 지연선, 통신 인터페이스에서 매우 유용하다.
> 3. **판단 포인트**: SISO, SIPO, PISO, PIPO 같은 형태와 LFSR (Linear Feedback Shift [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/)), Barrel Shifter 응용을 함께 봐야 한다.

---

## Ⅰ. 개요 및 필요성

시프트 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 옆 칸으로 밀어 보내는 회로다. 작은 저장소들이 줄지어 있고, 클록이 들어올 때마다 모두 한 칸씩 이동한다.

[초기](/knowledge-base/studynote/03_network/08_transport_layer/459_quic_fec_forward_error_correction/) 하드웨어는 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 통신이나 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 이동 연산을 효율적으로 처리하기 위해 이런 구조를 필요로 했다.

- **📢 섹션 요약 비유**: 시프트 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)는 컨베이어 벨트 위의 상자들처럼 한 칸씩 밀려가는 구조다.

---

## Ⅱ. 동작 구조

각 [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)의 출력이 다음 [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)의 입력으로 연결된다.

```text
SI -> [FF0] -> [FF1] -> [FF2] -> [FF3] -> SO
          ^       ^       ^       ^
        같은 CLK가 모두에 동시에 들어감
```

클록이 한 번 오면 모든 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)가 동시에 한 칸씩 이동한다. 이 단순한 구조가 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 처리를 가능하게 한다.

- **📢 섹션 요약 비유**: 줄 서 있던 사람들이 신호가 울릴 때마다 한 칸씩 앞으로 움직이는 모습이다.

---

## Ⅲ. 종류와 방향

시프트 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)는 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 입출력 방식에 따라 나뉜다.

- **SISO (Serial-In Serial-Out)**: 한 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)씩 넣고 한 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)씩 뺀다.
- **SIPO (Serial-In Parallel-Out)**: 한 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)씩 넣고 여러 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 한 번에 뺀다.
- **PISO (Parallel-In Serial-Out)**: 여러 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 한 번에 넣고 한 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)씩 뺀다.
- **PIPO (Parallel-In Parallel-Out)**: 한 번에 넣고 한 번에 뺀다.

방향이 양쪽인 구조나, [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 로드가 가능한 구조도 자주 쓴다.

- **📢 섹션 요약 비유**: 들어오는 문과 나가는 문이 하나인지 여러 개인지에 따라 다른 우편함 구조가 된다.

---

## Ⅳ. 활용과 응용

시프트 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)는 다양한 곳에 쓰인다.

- [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 통신 버퍼
- 지연선(delay line)
- [산술 시프트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/121_arithmetic_shift/)(곱셈/나눗셈)
- LFSR (Linear Feedback Shift [Register](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/175_register_addressing/))
- Barrel Shifter

특히 LFSR은 난수 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)과 패턴 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)에, Barrel Shifter는 빠른 시프트 연산에 쓰인다.

- **📢 섹션 요약 비유**: 레일 위에서 짐을 조금씩 옮기다가, 필요하면 한 번에 훅 밀어 보내는 장치다.

---

## Ⅴ. 실무 비교와 설계 관점

[레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)와 달리 시프트 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)는 "저장"보다 "이동"이 핵심이다. 그래서 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 흐름을 다루는 설계에서 중요하다.

설계할 때는 다음을 본다.

- 입력/출력 방향
- [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 폭
- [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 로드 필요 여부
- 시프트 속도
- 통신 프로토콜과의 연계

- **📢 섹션 요약 비유**: 서랍장보다 컨베이어 벨트에 더 가까운 장치다.

---

## 관련 개념 맵

```text
플립플롭
   v
직렬 연결
   v
비트 이동
   v
통신 / LFSR / Barrel Shifter
```

---

## 관련 키워드 및 발전 흐름도

1. [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/) [배열](/knowledge-base/studynote/08_algorithm_stats/04_datastructure/055_array/) -> 기본 저장과 이동
2. [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 통신 요구 -> SISO/SIPO/PISO/PIPO 등장
3. [산술 시프트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/121_arithmetic_shift/) -> 빠른 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 이동 활용
4. LFSR -> 난수와 패턴 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/) 응용
5. Barrel Shifter -> 고속 [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 시프트로 발전

---

## 어린이를 위한 3줄 비유 설명

시프트 [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)는 줄지어 선 친구들이 한 칸씩 옆으로 움직이는 거예요.
뒤에서 새 친구가 들어오면 앞사람들이 같이 밀려나요.
그래서 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)를 옮기거나 나누고 붙이는 데 아주 편해요.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 58 / 803

<- **이전**: [57. 레지스터 (Register)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)
**다음**: [59. 카운터 (Counter)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/) ->

---
