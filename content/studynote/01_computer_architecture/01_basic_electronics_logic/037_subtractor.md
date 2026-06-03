+++
title = "037. 감산기 (Subtractor) — 반감산기·전감산기"
date = 2026-03-03

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 감산기(Subtractor)는 두 이진수를 빼는 회로로, 반감산기(Half Subtractor)는 Borrow 입력 없이, 전감산기(Full Subtractor)는 이전 단계 Borrow를 포함해 3비트를 처리한다.
> 2. **가치**: 디지털 시스템에서는 감산기를 독립 회로로 구현하지 않고 2의 보수(Two's Complement) 방식을 통해 가산기로 뺄셈을 처리한다 — A - B = A + (-B) = A + (~B + 1).
> 3. **판단 포인트**: [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)(Arithmetic Logic Unit)는 하나의 가산기 + Carry-In 제어 + 부호 비트 제어로 덧셈과 뺄셈을 모두 구현하는데, 이것이 하드웨어 설계의 핵심 최적화다.

---

## Ⅰ. 개요 및 필요성

컴퓨터 초기에는 덧셈 회로와 뺄셈 회로를 각각 별도로 구현하는 방법을 고려했다. 그러나 1940년대 폰 노이만(John von Neumann)과 동료들이 2의 보수(Two's Complement) 표현법을 채택하면서, 뺄셈을 덧셈 회로 하나로 처리하는 혁신이 이루어졌다. 이 결정은 CPU 하드웨어 복잡도를 절반으로 줄이는 핵심 설계 원칙이 되었다.

반감산기(Half Subtractor)는 두 1비트 수의 차(Difference)와 빌림(Borrow)을 계산하는 기본 회로다. 그러나 실제 다비트 뺄셈에서는 이전 자리에서 빌려온 Borrow도 고려해야 하므로 전감산기(Full Subtractor)가 필요하다. 전감산기는 전가산기와 구조적으로 유사하며, 내부적으로 반감산기 2개와 OR 게이트 1개로 구성된다.

중요한 점은, 현대 디지털 시스템에서 독립적인 감산기 회로는 거의 사용되지 않는다는 것이다. 대신 가산기 회로에 2의 보수 변환(XOR 게이트로 비트 반전 + Carry-In에 1 입력)을 결합하여 덧셈·뺄셈을 공용 회로로 처리한다. 이것이 현대 ALU의 핵심 설계 철학이다.

- **📢 섹션 요약 비유**: 별도의 감산기를 만드는 것은 집에 세탁기와 건조기를 따로 사는 것이다. 2의 보수 방식은 올인원 세탁건조기 하나로 두 기능을 모두 처리하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 반감산기 (Half Subtractor)

```text
입력: A(피감수), B(감수)
출력: D(차, Difference), Borrow(빌림)

진리표:
A  B | D  Borrow
0  0 | 0    0
0  1 | 1    1    ← A < B이므로 Borrow 발생
1  0 | 1    0
1  1 | 0    0

논리식:
  D      = A XOR B
  Borrow = A' AND B  (A가 0이고 B가 1일 때만 빌림 발생)

게이트: XOR 1개 + AND 1개 + NOT 1개 = 3 게이트
```

### 전감산기 (Full Subtractor)

```text
입력: A(피감수), B(감수), Bin(Borrow 입력)
출력: D(차), Bout(Borrow 출력)

진리표:
A  B  Bin | D  Bout
0  0   0  | 0    0
0  0   1  | 1    1
0  1   0  | 1    1
0  1   1  | 0    1
1  0   0  | 1    0
1  0   1  | 0    0
1  1   0  | 0    0
1  1   1  | 1    1

논리식:
  D    = A XOR B XOR Bin
  Bout = A'B + A'Bin + BBin
       = (NOT A AND B) OR (NOT A AND Bin) OR (B AND Bin)

구현: 반감산기 2개 + OR 1개
  HS1: D1 = A XOR B,       Br1 = A' AND B
  HS2: D  = D1 XOR Bin,    Br2 = D1' AND Bin
  Bout = Br1 OR Br2
```

| 비교 항목 | 반감산기 | 전감산기 |
|:---|:---|:---|
| **입력 수** | 2개 (A, B) | 3개 (A, B, Borrow_in) |
| **출력 수** | 차(D), Borrow_out | 차(D), Borrow_out |
| **Borrow 처리** | 불가 (생성만) | 이전 단의 Borrow 포함 |
| **다비트 뺄셈** | 최하위 비트만 가능 | 중간/상위 비트 처리 |
| **용도** | 단독 1비트 뺄셈 | n비트 병렬 뺄셈 |
| **게이트 수** | 3개 (XOR, AND, NOT) | 7개 (HS2 + OR) |

- **📢 섹션 요약 비유**: 전감산기는 "빌린 것"까지 계산에 포함하는 뺄셈 — 이전 자리에서 빌려온 것을 고려해야 한다.

---

## Ⅲ. 2의 보수로 뺄셈 구현

```text
원리: A - B = A + (-B) = A + (~B) + 1

하드웨어 구현:
  1. B의 모든 비트를 NOT (XOR 게이트로 구현)
  2. Carry-In에 1을 입력
  3. 가산기로 A + (~B + 1) 계산

예시 (4비트):
  A = 0110 (6)
  B = 0010 (2)

  ~B = 1101
  ~B + 1 = 1110 (2의 보수, -2)

  A + (~B+1) = 0110 + 1110 = 10100
  하위 4비트: 0100 (4) → 정답! (6-2=4)
```

### 가산기/감산기 공용 회로 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">병렬 가감산기 (ADD/SUB 공용):</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">A</div><div class="kb-diagram-node">n</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Full Adder n</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">n</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">B</div><div class="kb-diagram-node">n</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">XOR</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">Full Adder n</div></div>
<div class="kb-diagram-connector">↑</div>
<div class="kb-diagram-note">SUB 신호 (0=덧셈, 1=뺄셈)</div>
<div class="kb-diagram-note">Carry-In = SUB</div>
<div class="kb-diagram-note">SUB=0: A + B + 0 = A + B (덧셈)</div>
<div class="kb-diagram-note">SUB=1: A + ~B + 1 = A - B (뺄셈, 2의 보수)</div>
<div class="kb-diagram-note">추가 신호:</div>
<div class="kb-diagram-note">Overflow: C_out XOR C_n-1 (부호 있는 오버플로)</div>
<div class="kb-diagram-note">Carry: C_out (부호 없는 올림수)</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Zero: NOR(S</div><div class="kb-diagram-node">n:0</div><div class="kb-diagram-note">) (결과가 0인지)</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">Negative: S</div><div class="kb-diagram-node">n-1</div><div class="kb-diagram-note">(MSB = 부호 비트)</div></div>
</div>
</div>



- **📢 섹션 요약 비유**: 2의 보수로 뺄셈은 빚을 마이너스 잔액으로 변환해서 더하는 것 — 뺄셈 회로 없이 덧셈 회로 하나로 해결.

---

## Ⅳ. 실무 적용 및 기술사 판단

### RISC-V SUB 명령어 구현

```text
RISC-V SUB rd, rs1, rs2:
  실행: rd = rs1 - rs2

하드웨어 동작 (ALU 내부):
  1. rs2를 비트 반전 (NOT, 각 비트 XOR 1)
  2. 가산기 Carry-In=1 설정
  3. rs1 + ~rs2 + 1 계산
  4. 결과를 rd에 저장

비교: ADD rd, rs1, rs2
  1. Carry-In=0
  2. rs2를 그대로 사용
  3. rs1 + rs2 계산

차이: 단 두 제어 신호 (SUB=1 설정 = NOT 활성화 + Carry-In=1)
  → 완전히 별도 회로 없이 가산기 재사용
```

### ARM Cortex-A: 조건 분기와 감산기

```text
CMP r0, r1  (Compare = r0 - r1, 결과 버리고 플래그만 저장)
  내부 동작: 가감산기로 r0 - r1 수행
  저장: NZCV 플래그
    N (Negative): MSB of result
    Z (Zero): result == 0
    C (Carry): unsigned borrow
    V (Overflow): signed overflow

활용:
  BEQ  target  : Z=1이면 분기 (같으면 분기)
  BNE  target  : Z=0이면 분기 (다르면 분기)
  BLT  target  : N≠V이면 분기 (부호 있는 작으면)
  BGT  target  : Z=0 AND N=V이면 분기 (부호 있는 크면)
```

### 설계 판단 체크리스트

1. 독립 감산기 회로가 필요한가? 대부분 불필요. 가감산기 공용 회로 권장.
2. 부호 있는 뺄셈인가? 오버플로(V 플래그) 검출 로직 추가 필요.
3. 부호 없는 뺄셈인가? 빌림(Borrow = NOT Carry) 처리 방식 확인.
4. 결과가 음수가 될 수 있는가? 2의 보수 표현 범위 내인지 확인.
5. 비교 연산(CMP)이 필요한가? 감산 후 NZCV 플래그 저장 구조로 설계.

### 안티패턴

- **독립 감산기 회로 구현**: 현대 ALU에서 별도 감산기 회로를 구현하는 것은 면적과 전력의 낭비다. XOR 게이트와 Carry-In 제어만으로 기존 가산기를 감산기로 전환할 수 있다.
- **보수화 오류**: 2의 보수는 "모든 비트 반전 후 1 더하기"다. 1 더하는 과정을 가산기의 Carry-In으로 처리해야 하는데, 별도 +1 회로를 추가하면 게이트가 불필요하게 늘어난다.
- **오버플로 미검출**: 부호 있는 4비트 정수 범위는 -8~+7이다. +7 + 1 = -8(오버플로!), -8 - 1 = +7(오버플로!)이 발생해도 회로가 이를 감지하지 못하면 프로그램 오류가 된다. V 플래그 회로를 항상 포함해야 한다.

- **📢 섹션 요약 비유**: CPU가 1억 번의 뺄셈을 수행할 때 감산기 전용 회로 없이 가산기 하나로 처리한다는 발상이 하드웨어 비용을 반으로 줄였다.

---

## Ⅴ. 기대효과 및 결론

2의 보수 기반 가감산기 통합 설계는 디지털 컴퓨팅 역사에서 가장 영향력 있는 하드웨어 최적화 중 하나다. 별도 감산기 없이 가산기 하나로 덧셈·뺄셈·비교 연산을 모두 처리함으로써, CPU 설계의 단순성과 효율성을 동시에 달성했다.

| 기대효과 | 내용 |
|:---|:---|
| **회로 간소화** | 별도 감산기 불필요, 가산기 하나로 통합 |
| **면적 절감** | 동일 면적에 더 많은 기능 집적 |
| **전력 효율** | 게이트 수 감소 → 동적 전력 소모 감소 |
| **설계 표준화** | 모든 현대 CPU의 ALU 설계 기반 |
| **확장성** | 오버플로, 제로, 캐리 플래그로 다양한 조건 분기 지원 |

현대 GPU의 CUDA 코어와 TPU의 행렬 연산 유닛도 동일한 원리의 가감산기를 수천~수백만 개 병렬 배치하여 대규모 행렬 연산을 수행한다. 딥러닝 학습의 역전파(Backpropagation) 중 그래디언트 업데이트(W = W - lr * grad)도 결국 수백만 번의 부동소수점 뺄셈이며, 이 모든 연산의 기반에 가감산기 원리가 있다.

- **📢 섹션 요약 비유**: 세탁기 하나로 빨기·헹굼·탈수를 모두 — ALU도 하나의 가산기 회로로 덧셈·뺄셈을 모두 처리한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **반감산기** | 2입력 뺄셈 기본 블록 |
| **전감산기** | 3입력 뺄셈, 반감산기 2개 + OR |
| **2의 보수** | A-B = A + (~B+1), 뺄셈→덧셈 변환 |
| **가감산기** | ADD/SUB 공용 회로, SUB 제어 신호 |
| **ALU** | 가감산기 + 논리연산 + 플래그 생성 |
| **NZCV 플래그** | Negative, Zero, Carry, oVerflow |
| **CMP 명령어** | 감산 후 결과 버리고 플래그만 저장 |
| **오버플로 검출** | V = C_out XOR C_n-1 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">초기 이진 감산기 설계 — 독립 회로 구현 (1940s)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">2의 보수 방식 보급 (1950s~) — 가산기만으로 뺄셈 처리</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">ALU 통합 설계 — 가산기 + SUB 제어 신호 (1960s~)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">조건 플래그 체계 — NZCV 표준화 (x86, ARM, RISC-V)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">파이프라인 ALU — 각 파이프라인 단계별 가감산기 (1970s~)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">현대 ALU — FPU, SIMD 벡터 감산 (SSE, AVX, NEON)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">AI 가속기 — 수천 병렬 가감산기로 행렬 연산</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 감산기는 두 숫자를 빼는 기계예요 — 반감산기는 두 개, 전감산기는 세 개 입력을 처리해요.
2. 컴퓨터는 실제로 뺄셈 회로를 따로 만들지 않고, 덧셈 회로 하나로 2의 보수를 이용해 뺄셈을 해요.
3. "5-3"을 하려면 3을 뒤집어서(-3으로 만들어서) 5에 더하는 것 — 컴퓨터도 같은 방법을 쓴답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 37 / 803

← **이전**: [036. 올림수 예측 가산기 (Carry Lookahead Adder)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/036_carry_lookahead_adder/)
**다음**: [038. 병렬 가감산기 (Parallel Adder-Subtractor)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/038_parallel_adder_subtractor/) →

---
