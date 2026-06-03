+++
title = "전가산기 (Full Adder) 와 리플 캐리 가산기"
date = 2026-03-04

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전가산기(Full Adder)는 두 입력 비트와 이전 자리의 올림수(Carry-in)를 합산해 합(Sum)과 올림수(Carry-out)를 출력하는 조합 논리 회로로, [반가산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/033_half_adder/)([Half Adder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/033_half_adder/)) 2개와 OR 게이트 1개로 구성된다.
> 2. **가치**: 전가산기 n개를 직렬 연결한 [리플 캐리 가산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/035_ripple_carry_adder/)([Ripple Carry Adder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/035_ripple_carry_adder/))는 가장 단순한 n비트 덧셈기이나, 올림수가 차례로 전파되는 지연(Carry Propagation Delay)이 O(n)이어서 고속 회로에는 부적합하다.
> 3. **판단 포인트**: [올림수 예측 가산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/036_carry_lookahead_adder/)(CLA·Carry Look-Ahead Adder)는 모든 올림수를 병렬 계산해 O(log n) 지연으로 개선하며, 현대 ALU의 기반 회로다.

---

## Ⅰ. 개요 및 필요성

이진수 덧셈은 디지털 컴퓨팅의 가장 기본적인 산술 연산이다. 십진수 덧셈에서 "받아 올림"이 발생하듯, 이진수에서는 올림수(Carry)가 다음 자리로 전파된다. 반가산기(Half Adder)는 두 입력 비트(A, B)만 처리하여 합(Sum)과 올림수(Carry)를 계산하지만, 실제 다비트 덧셈에서는 이전 자리에서 올라온 올림수(Carry-in)도 처리해야 한다.

전가산기(Full Adder)는 이 문제를 해결한다. 3개의 입력(A, B, Carry-in)을 받아 합(Sum)과 올림수(Carry-out)를 출력하는 회로로, 이것이 현대 CPU의 ALU(Arithmetic Logic Unit)에서 이진 덧셈의 핵심 블록이다. 1940년대 최초 디지털 컴퓨터 ENIAC에서 사용된 이래, 전가산기는 형태만 바뀌었을 뿐 70년 이상 CPU의 핵심 회로로 사용되고 있다.

전가산기의 중요성은 단순히 덧셈에 그치지 않는다. 2의 보수(Two's Complement) 방식을 통해 뺄셈, BCD(Binary Coded Decimal) 변환, 이진 곱셈기의 부분합 처리 등 다양한 산술 연산의 기초가 된다.

- **📢 섹션 요약 비유**: 전가산기는 세 명이 함께 더하는 덧셈이다 — 두 숫자(A, B)에 이전 자리에서 올라온 1(Cin)까지 더해 결과(Sum)와 다음 자리 올림(Cout)을 계산한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 전가산기 진리표

| A | B | Cin | Sum | Cout |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

### 부울 대수식

```text
Sum  = A XOR B XOR Cin
     = (A ⊕ B) ⊕ Cin

Cout = (A AND B) OR (Cin AND (A XOR B))
     = AB + Cin(A⊕B)

SOP 형태:
  Sum  = A'B'C + A'BC' + AB'C' + ABC
  Cout = AB + AC + BC
```

### 반가산기 2개로 전가산기 구성

```text
HA1: S1  = A XOR B   (1차 합)
     C1  = A AND B   (1차 올림)

HA2: Sum = S1 XOR Cin  (최종 합)
     C2  = S1 AND Cin  (2차 올림)

Cout = C1 OR C2    (최종 올림수)

게이트 수:
  XOR × 2 = 10T (CMOS 기준 각 5T)
  AND × 2 = 12T
  OR  × 1 = 6T
  총 = 28T (약)
```

### 전가산기 구현 다이어그램



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">A</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">HA1: XOR₁</div><div class="kb-diagram-cell">──→ HA2: XOR₂ ──→ Sum</div></div>
<div class="kb-diagram-note">B HA1: AND₁ │</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">HA2: AND₂ ──</div></div>
<div class="kb-diagram-note">Cin ─ OR ──→ Cout</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">C1</div></div>
<div class="kb-diagram-note">Step-by-step (A=1, B=1, Cin=1 예시):</div>
<div class="kb-diagram-note">S1 = 1 XOR 1 = 0</div>
<div class="kb-diagram-note">C1 = 1 AND 1 = 1</div>
<div class="kb-diagram-note">Sum = 0 XOR 1 = 1</div>
<div class="kb-diagram-note">C2 = 0 AND 1 = 0</div>
<div class="kb-diagram-note">Cout = 1 OR 0 = 1</div>
<div class="kb-diagram-note">결과: Sum=1, Cout=1 → 1+1+1 = 11₂ = 3 ✓</div>
</div>
</div>



- **📢 섹션 요약 비유**: 전가산기는 반가산기 두 팀이 이어달리기다 — 첫 팀(HA1)이 A+B를 계산하고, 두 번째 팀(HA2)이 그 결과에 Cin을 더한다.

---

## Ⅲ. 리플 캐리 가산기 (Ripple Carry Adder)

### 4비트 리플 캐리 가산기 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">4비트 리플 캐리 가산기:</div>
<div class="kb-diagram-note">A3 B3 A2 B2 A1 B1 A0 B0</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">FA3</div><div class="kb-diagram-note">──</div><div class="kb-diagram-node">FA2</div><div class="kb-diagram-note">──</div><div class="kb-diagram-node">FA1</div><div class="kb-diagram-note">──</div><div class="kb-diagram-node">FA0</div><div class="kb-diagram-note">── Cin=0</div></div>
<div class="kb-diagram-note">C3→ C2→ C1→ Sum0</div>
<div class="kb-diagram-note">Sum3 Sum2 Sum1</div>
<div class="kb-diagram-note">신호 전파 순서:</div>
<div class="kb-diagram-note">FA0 계산 → C1 생성 → FA1 계산 → C2 생성 → FA2 계산 → C3 생성 → FA3 계산</div>
<div class="kb-diagram-note">올림수 전파 지연: n × t_FA (n=비트 수)</div>
<div class="kb-diagram-note">4비트: 4 × t_FA</div>
<div class="kb-diagram-note">32비트: 32 × t_FA (느림!)</div>
<div class="kb-diagram-note">64비트: 64 × t_FA (매우 느림!)</div>
</div>
</div>



### 가산기 방식별 성능 비교

| 방식 | 지연 | 회로 복잡도 | 게이트 수 | 적용 |
|:---|:---:|:---:|:---:|:---|
| 리플 캐리 가산기 (RCA) | O(n) | 낮음 | 최소 | 교육용, 저속 회로 |
| CLA 가산기 | O(log n) | 중간 | 많음 | 범용 ALU |
| 계층적 CLA | O(log n) | 중간 | 중간 | 32/64비트 ALU |
| 캐리 저장 가산기 (CSA) | O(1) | 높음 | 높음 | 곱셈기, 파이프라인 |
| Kogge-Stone | O(log n) | 높음 | 최다 | Intel CPU ALU |
| Brent-Kung | O(log n) | 높음 | 중간 | VLSI 설계 |

- **📢 섹션 요약 비유**: 리플 캐리는 릴레이 경주다 — 앞 선수(FA0)가 배턴(Carry)을 넘기기 전까지 다음 선수(FA1)가 출발 못하므로 전체 시간이 n배 걸린다.

---

## Ⅳ. 올림수 예측 가산기 (CLA, Carry Look-Ahead Adder)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">CLA의 핵심 개념:</div>
<div class="kb-diagram-note">Gi = Ai AND Bi (Generate: 반드시 올림수 생성)</div>
<div class="kb-diagram-note">Pi = Ai XOR Bi (Propagate: 올림수 전파 가능)</div>
<div class="kb-diagram-note">올림수 재귀 공식:</div>
<div class="kb-diagram-note">C1 = G0 + P0·C0</div>
<div class="kb-diagram-note">C2 = G1 + P1·G0 + P1·P0·C0</div>
<div class="kb-diagram-note">C3 = G2 + P2·G1 + P2·P1·G0 + P2·P1·P0·C0</div>
<div class="kb-diagram-note">→ 모든 올림수를 C0(초기값)와 G, P로 동시에 계산</div>
<div class="kb-diagram-note">→ 지연: O(1) (단, 게이트 입력 수 제한으로 실제 O(log n))</div>
</div>
</div>



- **📢 섹션 요약 비유**: CLA는 모든 릴레이 선수가 동시에 출발 신호를 받는 것이다 — "만약 앞 선수가 배턴을 줄 것 같다면"을 미리 계산해 일제히 달린다.

---

## Ⅴ. 기대효과 및 결론

전가산기는 디지털 컴퓨팅의 기본 산술 블록으로, 70년 넘게 그 본질적인 구조를 유지하면서 발전해왔다. 단순한 28T CMOS 회로에서 시작하여, 현대 고성능 CPU의 수십억 트랜지스터 속에서도 전가산기의 원리가 그대로 작동하고 있다.

| 기대효과 | 내용 |
|:---|:---|
| **산술 연산 기반** | 덧셈 → 뺄셈(2의 보수) → 곱셈 → 나눗셈의 기본 |
| **회로 단순성** | HA 2개 + OR 1개의 단순한 구조 |
| **확장성** | n개 직렬 연결로 n비트 가산기 구성 |
| **고속화 기반** | CLA, Kogge-Stone 등 고속 가산기의 핵심 블록 |
| **설계 재사용** | ALU, FPU, 곱셈기 등 상위 회로의 빌딩 블록 |

3GHz CPU에서 단 0.33나노초 클록 주기 안에 64비트 덧셈을 완료해야 한다. 이를 위해 Intel, AMD, ARM은 모두 Kogge-Stone 또는 Brent-Kung 계열 병렬 접두사 가산기(Parallel Prefix Adder)를 사용한다. 이 고속 가산기들도 모두 전가산기를 최소 블록으로 한다. 또한 딥러닝 가속기(TPU, GPU)에서 행렬 곱셈의 누적 덧셈도 전가산기 기반의 캐리 저장 가산기(CSA, Carry Save Adder)로 구현된다.

- **📢 섹션 요약 비유**: 가산기 방식은 음식 배달 방식이다 — 리플 캐리는 한 명이 순서대로 배달하고, CLA는 여러 경로를 미리 계획해 동시에 배달한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **반가산기** | 전가산기 구성 요소 (HA × 2) |
| **리플 캐리 가산기** | 전가산기 직렬 연결, O(n) 지연 |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/036_carry_lookahead_adder/">올림수 예측 가산기</a></strong> | 병렬 올림수 계산, O(log n) |
| **ALU** | 전가산기 기반 산술 논리 장치 |
| **곱셈기** | CSA(캐리 저장 가산기) 기반 |
| **FPU** | 부동소수점 가산기 (가수 덧셈) |
| **2의 보수** | 가산기로 뺄셈 구현 원리 |
| **Kogge-Stone** | 현대 CPU의 최속 가산기 구조 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">반가산기 (1940s) → 전가산기 (1940s)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">리플 캐리 가산기 — 직렬 n비트 덧셈기 (1950s)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">올림수 예측 가산기 (CLA) — O(log n) 지연 (1960s)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">계층적 CLA — 블록 단위 O(log n) (1970s)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">캐리 저장 가산기 (CSA) — 곱셈기 파이프라인 최적화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Kogge-Stone (1973) / Brent-Kung (1982) — 병렬 접두사</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">현대 CPU/GPU ALU — GHz 클록 64비트 1사이클 덧셈</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 전가산기는 세 개의 구슬을 더하는 기계다 — 두 구슬(A, B)에 앞에서 넘어온 구슬(Cin)까지 더해서, 남은 구슬(Sum)과 다음으로 넘길 구슬(Cout)을 알려준다.
2. 리플 캐리 가산기는 릴레이 경주다 — 앞 주자가 배턴을 주기 전까지 다음 주자가 달릴 수 없어서, 8명이면 8배, 64명이면 64배 느려진다.
3. CLA 가산기는 모든 주자가 동시에 준비하는 경주다 — "혹시 배턴이 올 경우"를 미리 계산해 놓고 한꺼번에 달려서 훨씬 빠르다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 34 / 803

← **이전**: [반가산기 (Half Adder)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/033_half_adder/)
**다음**: [035. 리플 캐리 가산기 (Ripple Carry Adder)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/035_ripple_carry_adder/) →

---
