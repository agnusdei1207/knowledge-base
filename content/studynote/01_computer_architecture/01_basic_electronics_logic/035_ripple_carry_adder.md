+++
title = "035. 리플 캐리 가산기 (Ripple Carry Adder)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

> **핵심 인사이트**
> 1. RCA (Ripple Carry Adder)는 [전가산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/034_full_adder/)(FA)를 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 연결해 하위 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 캐리가 상위 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/)로 전파(ripple)되는 구조로, 구현이 단순하지만 캐리 [전파 지연](/knowledge-base/studynote/03_network/01_data_communication/016_전파_지연/)(Carry [Propagation Delay](/knowledge-base/studynote/03_network/01_data_communication/016_전파_지연/))이 [성능](/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/282_performance_tactics/) 병목이다.
> 2. n-bit RCA의 최악 [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/)은 O(n)이므로, 고속 가산이 필요한 CPU는 CLA ([Carry Lookahead Adder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/036_carry_lookahead_adder/)) 또는 CSA (Carry Save Adder)로 대체한다.
> 3. 비용·면적 vs 속도의 트레이드오프가 핵심: RCA는 게이트 수 최소, CLA는 빠르지만 게이트 수 증가.

---

## Ⅰ. 기본 원리 — [전가산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/034_full_adder/)의 체인

```
  A3 B3    A2 B2    A1 B1    A0 B0
  │  │     │  │     │  │     │  │
 [FA3]←C3─[FA2]←C2─[FA1]←C1─[FA0]←Cin=0
  │        │        │        │
  S3       S2       S1       S0
  │
  Cout
```

- **FA ([Full Adder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/034_full_adder/))** 하나가 1비트 합(Sum)과 캐리(Carry Out) [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/)
- Carry Out이 다음 FA의 Carry In으로 전달 → 물결처럼 전파
- n-bit 합산 시 FA를 n개 [직렬](/knowledge-base/studynote/03_network/03_physical_layer_media/149_serial_communication_rs232_rs485/) 연결

### [진리표](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/024_truth_table/) (FA 단일)

| A | B | Cin | Sum | Cout |
|---|---|-----|-----|------|
| 0 | 0 | 0   | 0   | 0    |
| 0 | 1 | 0   | 1   | 0    |
| 1 | 1 | 0   | 0   | 1    |
| 1 | 1 | 1   | 1   | 1    |

> 📢 **섹션 요약 비유**: 손가락 덧셈처럼 1의 자리부터 올림수를 차례로 전달 — 7살도 하는 방식이지만, 64비트면 64번 기다려야 한다.

---

## Ⅱ. [지연 시간](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/141_latency/) 분석

```
게이트 지연 단위 = t_gate

FA 1개 지연: Sum = 2t, Carry = 2t
n-bit RCA 총 지연:
  - S0 : 2t
  - S1 : 2t + 2t = 4t   (C1 전파 후)
  - Sn-1: 2n·t           ← O(n) 선형 증가
```

| [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 수 | RCA [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) | CLA [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) |
|---------|---------|---------|
| 4-bit   | 8t      | 4t      |
| 8-bit   | 16t     | 5t      |
| 32-bit  | 64t     | 8t      |

- **Critical Path**: 최하위 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 캐리 → 최상위 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) [순전파](/knowledge-base/studynote/10_ai/03_llm_nlp/271_forward_propagation/) 경로

> 📢 **섹션 요약 비유**: 릴레이 경기처럼 바통을 한 명씩 전달 — 선수가 많을수록 총 시간이 선형 증가.

---

## Ⅲ. 개선 기법 — CLA와 CSA

### 3-1. CLA ([Carry Lookahead Adder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/036_carry_lookahead_adder/))

```
Generate: Gi = Ai AND Bi   → 이 자리에서 캐리 생성
Propagate: Pi = Ai XOR Bi  → 입력 캐리를 다음 자리로 전달

C1 = G0 + P0·C0
C2 = G1 + P1·G0 + P1·P0·C0
C3 = G2 + P2·G1 + P2·P1·G0 + P2·P1·P0·C0  (병렬 계산)
```

- **O(log n)** [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)으로 단축
- 상위 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 캐리를 하위 [비트](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/073_bit/) 결과를 기다리지 않고 직접 계산

### 3-2. CSA (Carry Save Adder) — 3피연산자 합산

```
3개 숫자(A, B, C) 동시 합산:
  CSA: (A, B, C) → (Sum, Carry) 병렬 생성
  최종 RCA/CLA로 Sum + Carry 처리
```

- 곱셈기(Multiplier) 내부에서 부분 합(Partial Product) 처리에 필수

> 📢 **섹션 요약 비유**: CLA는 경기 전 각 구간 예상 결과를 미리 계산해두는 [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) — 모든 구간을 동시에 달릴 수는 없지만 바통 위치를 예측해 준비한다.

---

## Ⅳ. 구현 예시

```verilog
// 1-bit Full Adder
module full_adder(input A, B, Cin, output Sum, Cout);
  assign Sum  = A ^ B ^ Cin;
  assign Cout = (A & B) | (Cin & (A ^ B));
endmodule

// 4-bit Ripple Carry Adder
module rca_4bit(input [3:0] A, B, input Cin, output [3:0] S, output Cout);
  wire c1, c2, c3;
  full_adder fa0(A[0], B[0], Cin, S[0], c1);
  full_adder fa1(A[1], B[1], c1,  S[1], c2);
  full_adder fa2(A[2], B[2], c2,  S[2], c3);
  full_adder fa3(A[3], B[3], c3,  S[3], Cout);
endmodule
```

> 📢 **섹션 요약 비유**: LEGO처럼 FA 블록을 일렬로 이어 붙이면 RCA 완성 — 단순하지만 길면 느리다.

---

## Ⅴ. 실무 시나리오 — CPU [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) 설계

| 상황              | 선택       | 이유                              |
|-------------------|-----------|-----------------------------------|
| 교육용 4-bit 계산기 | RCA       | 단순성 우선                        |
| [FPGA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/606_dynamic_partial_reconfiguration/) 32-bit 가산  | CLA       | 타이밍 클로저 요구                 |
| [GPU](/knowledge-base/studynote/01_computer_architecture/12_accelerators_ai_hardware/418_gpu/) [누산기](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/161_accumulator/) 내부    | CSA + CLA | 다수 [피연산자](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/160_operand/) [병렬](/knowledge-base/studynote/05_database/07_exam_summary/430_index_fast_full_scan/) 처리             |
| [RISC-V](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/200_riscv/) [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)       | CLA 2단계 | 게이트 수·속도 균형                |

> 📢 **섹션 요약 비유**: 단거리면 RCA, 마라톤 속도전이면 CLA — 도구는 목적에 맞게 선택한다.

---

## 📌 관련 개념 맵

```
리플 캐리 가산기 (RCA)
├── 구성 단위: FA (Full Adder)
│   ├── Half Adder (HA) × 2 + OR
│   └── 입력: A, B, Cin / 출력: Sum, Cout
├── 성능 병목: 캐리 전파 지연 O(n)
├── 개선
│   ├── CLA (Carry Lookahead Adder) → O(log n)
│   │   ├── Generate (Gi)
│   │   └── Propagate (Pi)
│   └── CSA (Carry Save Adder) → 3→2 압축
└── 응용
    ├── ALU (Arithmetic Logic Unit)
    ├── 곱셈기 (부분 합 합산)
    └── FPU (부동소수점 가산)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[반가산기 HA]
      │ 캐리 처리 한계
      ▼
[전가산기 FA] → Cin 포함 1비트 합산
      │ 직렬 연결
      ▼
[RCA (Ripple Carry Adder)] → 단순·저비용·O(n) 지연
      │ 속도 개선 필요
      ├──────────────────────────────┐
      ▼                              ▼
[CLA (Carry Lookahead)]        [CSA (Carry Save)]
O(log n) 지연·병렬 캐리        3→2 압축·곱셈기 내부
      │
      ▼
[계층적 CLA / Kogge-Stone / Brent-Kung]
초고속 VLSI 가산기 설계
      │
      ▼
[현대 CPU ALU / FPU / GPU]
GHz 클럭에서 1사이클 가산
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 리플 캐리 가산기는 덧셈할 때 받아올림을 한 자리씩 차례로 전달하는 방식이에요.
2. 자릿수가 많아질수록 기다리는 시간이 길어지는 게 단점이에요.
3. 컴퓨터에서는 더 빠른 방법(CLA)을 써서 여러 자리를 동시에 계산해요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 35 / 803

← **이전**: [전가산기 (Full Adder) 와 리플 캐리 가산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/034_full_adder/)
**다음**: [036. 올림수 예측 가산기 (Carry Lookahead Adder)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/036_carry_lookahead_adder/) →

---
