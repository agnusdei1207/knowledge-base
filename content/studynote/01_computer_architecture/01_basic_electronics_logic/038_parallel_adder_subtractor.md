+++
title = "038. 병렬 가감산기 (Parallel Adder-Subtractor)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 병렬 가감산기(Parallel Adder-Subtractor)는 단일 회로에서 ADD(덧셈)와 SUB(뺄셈)를 모두 처리하는 복합 산술 회로로, SUB 제어 신호 하나로 XOR 게이트를 통한 B 반전과 Carry-In=1(2의 보수 +1)을 동시에 제어한다.
> 2. **가치**: n비트 병렬 가감산기의 핵심은 Ripple Carry vs Carry Lookahead 트레이드오프 — Ripple Carry는 단순하지만 n단 지연, CLA(Carry Lookahead Adder)는 복잡하지만 O(log n) 지연으로 고속 CPU에 필수다.
> 3. **판단 포인트**: 오버플로(Overflow) 감지는 부호 있는 연산의 필수 기능으로, 두 양수를 더해 음수가 되거나 두 음수를 더해 양수가 될 때 발생하며, MSB Carry-In과 Carry-Out의 XOR로 검출한다.

---

## Ⅰ. 개요 및 필요성

1940년대 폰 노이만 아키텍처가 제안된 이후, ALU(Arithmetic Logic Unit) 설계의 핵심 과제는 "어떻게 하나의 회로로 덧셈과 뺄셈 모두를 처리할 것인가?"였다. 초기에는 덧셈 회로와 뺄셈 회로를 별도로 구현하는 방식을 검토했으나, 2의 보수 표현법과 XOR 게이트를 결합하면 하나의 가산기로 두 연산을 모두 처리할 수 있다는 것이 밝혀졌다.

병렬 가감산기는 이 원리를 n비트 전체에 동시에 적용한 회로다. "병렬(Parallel)"이라는 단어는 n개의 비트를 직렬이 아닌 동시에 처리한다는 의미다. 단일 제어 신호(SUB) 하나로 XOR 게이트를 통해 피연산자 B를 반전하고, 동시에 가산기의 Carry-In을 1로 설정하여 2의 보수(~B + 1)를 만들어 덧셈으로 뺄셈을 구현한다.

현대 CPU의 ALU는 이 병렬 가감산기를 기반으로 하며, 여기에 NZCV 플래그 생성 회로, 오버플로 감지 회로, 조건 분기를 위한 비교 회로가 추가된다. Intel x86, ARM, RISC-V 모두 이 기본 구조를 따른다.

- **📢 섹션 요약 비유**: 스위치 하나로 믹서기(더하기 모드)와 분리기(빼기 모드)를 바꾸는 것 — 회로 두 배 없이 기능 두 배.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 4비트 병렬 가감산기 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">4비트 병렬 가감산기:</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">A</div><div class="kb-diagram-node">3:0</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">FA3~FA0</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">B</div><div class="kb-diagram-node">3:0</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">XOR with SUB</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">FA3~FA0</div></div>
<div class="kb-diagram-connector">↑</div>
<div class="kb-diagram-note">SUB 신호 → Carry-In</div>
<div class="kb-diagram-note">B3 B2 B1 B0</div>
<div class="kb-diagram-note">XOR XOR XOR XOR ← SUB=1이면 B 반전, SUB=0이면 그대로</div>
<div class="kb-diagram-note">FA3 FA2 FA1 FA0 ← Full Adder 4개 병렬 연결</div>
<div class="kb-diagram-note">S3 S2 S1 S0 Cin=SUB (SUB=1이면 2의 보수 완성)</div>
<div class="kb-diagram-note">SUB=0: S = A + B (덧셈)</div>
<div class="kb-diagram-note">SUB=1: S = A + ~B + 1 = A - B (뺄셈, 2의 보수)</div>
</div>
</div>



| 제어 신호 | 동작 | Carry-In | B 처리 |
|:---|:---|:---:|:---|
| SUB=0 | 덧셈 (A + B) | 0 | 그대로 |
| SUB=1 | 뺄셈 (A - B) | 1 | XOR로 반전 (~B) |

### 수치 예시

```text
A = 0110 (6), B = 0011 (3)

덧셈 (SUB=0):
  B XOR 0000 = 0011 (변화 없음)
  Carry-In = 0
  0110 + 0011 + 0 = 1001 (9) ✓

뺄셈 (SUB=1):
  B XOR 1111 = 1100 (~B, 비트 반전)
  Carry-In = 1
  0110 + 1100 + 1 = 10011
  하위 4비트 = 0011 (3) ✓  (6 - 3 = 3)
```

### ALU NZCV 플래그 생성



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">현대 ALU 플래그 체계:</div>
<div class="kb-diagram-note">N (Negative): S의 MSB 비트</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">n-1</div><div class="kb-diagram-note">= 1이면 결과가 음수 (2의 보수 해석)</div></div>
<div class="kb-diagram-note">Z (Zero): 결과가 모두 0이면 1</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">n-1:0</div><div class="kb-diagram-note">) = NOT(S</div><div class="kb-diagram-node">n-1</div><div class="kb-diagram-note">OR S</div><div class="kb-diagram-node">n-2</div><div class="kb-diagram-note">OR ... OR S</div><div class="kb-diagram-node">0</div><div class="kb-diagram-note">)</div></div>
<div class="kb-diagram-note">C (Carry): 최상위 올림수</div>
<div class="kb-diagram-note">→ C = Cout (부호 없는 덧셈의 올림, 뺄셈의 빌림 반전)</div>
<div class="kb-diagram-note">→ 부호 없는 오버플로 감지에 사용</div>
<div class="kb-diagram-note">V (oVerflow): 부호 있는 오버플로</div>
<div class="kb-diagram-row"><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">n-1</div><div class="kb-diagram-note">(MSB Carry-Out XOR MSB Carry-In)</div></div>
<div class="kb-diagram-note">→ 두 양수 합 = 음수, 또는 두 음수 합 = 양수일 때 V=1</div>
<div class="kb-diagram-note">활용 예 (ARM 조건 코드):</div>
<div class="kb-diagram-note">EQ (Equal): Z=1</div>
<div class="kb-diagram-note">NE (Not Equal): Z=0</div>
<div class="kb-diagram-note">LT (Less Than): N ≠ V (부호 있는)</div>
<div class="kb-diagram-note">GE (Greater or Equal): N = V</div>
<div class="kb-diagram-note">CC (Carry Clear): C=0 (부호 없는 빌림)</div>
</div>
</div>



- **📢 섹션 요약 비유**: ALU는 스위스 군용 칼 — 가감산기 날, 오버플로 경고, 영 감지, 올림 표시가 한 손잡이에 모두.

---

## Ⅲ. 비교 및 연결

### Ripple Carry vs Carry Lookahead 비교

```text
Ripple Carry Adder (RCA):
  각 FA의 Carry-Out → 다음 FA의 Carry-In으로 직렬 전달
  전달 지연: n × t_FA  (n=비트 수, t_FA=FA 지연)
  4비트:  4 × t_FA
  32비트: 32 × t_FA  (느림!)

Carry Lookahead Adder (CLA):
  Generate: G_i = A_i AND B_i (항상 올림 생성)
  Propagate: P_i = A_i XOR B_i (올림 전파)
  C_i+1 = G_i + P_i·C_i
  모든 캐리를 병렬로 미리 계산
  지연: O(log n) (2~3단계 로직 게이트)

32비트 비교:
  RCA: ~32 t_FA ≈ 32 × 0.1ns = 3.2ns (10 클록 @3GHz)
  CLA: ~5 게이트 지연 ≈ 0.5ns (1~2 클록 @3GHz)
```

| 가산기 방식 | 지연 | 게이트 수 | 전력 | 적합 용도 |
|:---|:---:|:---:|:---:|:---|
| Ripple Carry (RCA) | O(n) | 최소 | 낮음 | 저속/교육 |
| Carry Lookahead (CLA) | O(log n) | 중간 | 중간 | 범용 ALU |
| Carry Save (CSA) | O(1)* | 높음 | 높음 | 곱셈기 |
| Kogge-Stone | O(log n) | 최다 | 높음 | 고성능 CPU |

### 오버플로(Overflow) 검출 원리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">부호 있는 n비트 표현 범위:</div>
<div class="kb-diagram-tree-item" style="--depth:1">2^(n-1) ~ 2^(n-1) - 1</div>
<div class="kb-diagram-note">4비트: -8 ~ +7</div>
<div class="kb-diagram-note">오버플로 발생 조건:</div>
<div class="kb-diagram-note">양수 + 양수 = 음수 (결과가 +7 초과)</div>
<div class="kb-diagram-note">음수 + 음수 = 양수 (결과가 -8 미만)</div>
<div class="kb-diagram-note">(양수 + 음수 = 절대 오버플로 없음)</div>
<div class="kb-diagram-note">오버플로 검출 회로:</div>
<div class="kb-diagram-note">V = C_n XOR C_(n-1)</div>
<div class="kb-diagram-note">(최상위 Carry-Out XOR 최상위 비트의 Carry-In)</div>
<div class="kb-diagram-note">V = 1이면 오버플로 발생</div>
<div class="kb-diagram-note">예시 (4비트 부호 있는):</div>
<div class="kb-diagram-note">A = 0111 (+7), B = 0001 (+1)</div>
<div class="kb-diagram-note">0111 + 0001 = 1000 = -8 (오버플로!)</div>
<div class="kb-diagram-note">C_4=0, C_3=1 → V = 0 XOR 1 = 1 (오버플로 감지)</div>
<div class="kb-diagram-note">A = 1000 (-8), B = 1111 (-1)</div>
<div class="kb-diagram-note">1000 + 1111 = 10111 → 하위 4비트 0111 = +7 (오버플로!)</div>
<div class="kb-diagram-note">C_4=1, C_3=0 → V = 1 XOR 0 = 1 (오버플로 감지)</div>
</div>
</div>



- **📢 섹션 요약 비유**: RCA는 편지를 한 명씩 전달, CLA는 모든 수신자에게 동시에 복사본 발송 — 수신자가 많을수록 CLA가 압도적으로 빠르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### RISC-V 32비트 ALU 실현



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RISC-V 32비트 ALU:</div>
<div class="kb-diagram-note">32비트 CLA 기반 병렬 가감산기</div>
<div class="kb-diagram-note">SUB 신호: rs2를 반전 + Carry-In=1</div>
<div class="kb-diagram-note">NZCV 플래그 → 조건 분기 명령어 활용:</div>
<div class="kb-diagram-note">BEQ (Branch if Equal): Z=1</div>
<div class="kb-diagram-note">BNE (Branch if Not Equal): Z=0</div>
<div class="kb-diagram-note">BLT (Branch if Less Than): N XOR V = 1 (부호 있는)</div>
<div class="kb-diagram-note">BGE (Branch if Greater or Equal): N XOR V = 0</div>
<div class="kb-diagram-note">BLTU (Branch LT Unsigned): C=1 (부호 없는)</div>
<div class="kb-diagram-note">BGEU (Branch GEU Unsigned): C=0</div>
<div class="kb-diagram-note">임계 경로(Critical Path) 영향:</div>
<div class="kb-diagram-note">클락 속도: 3GHz → 한 클락 = 0.33ns</div>
<div class="kb-diagram-note">32비트 CLA 지연 목표: &lt; 0.15ns (절반 이내)</div>
<div class="kb-diagram-note">→ 파이프라인 설계로 1클락 = 1회 가감산 가능</div>
</div>
</div>



### AVX-512 벡터 가감산기 (Intel)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">AVX-512: 512비트 SIMD 연산</div>
<div class="kb-diagram-note">VPADDD: 16개의 32비트 정수 동시 덧셈</div>
<div class="kb-diagram-note">VPSUBD: 16개의 32비트 정수 동시 뺄셈</div>
<div class="kb-diagram-note">실제 회로: 16개의 32비트 가감산기 병렬 배치</div>
<div class="kb-diagram-note">→ 1클락에 16개 ADD/SUB 동시 처리</div>
<div class="kb-diagram-note">→ 딥러닝 행렬 연산, 이미지 처리에 필수</div>
</div>
</div>



### 설계 판단 체크리스트

1. 요구되는 클록 주파수에서 가산기 지연이 충분한가? (RCA vs CLA)
2. 오버플로 감지 로직(V 플래그)이 포함되었는가?
3. 부호 없는 연산에서 캐리(C 플래그)가 올바르게 생성되는가?
4. 제로(Z 플래그) 감지를 위한 NOR 트리가 최적화되었는가?
5. 조건 분기 명령에 필요한 플래그 조합이 모두 지원되는가?
6. SIMD/벡터 연산 필요 시 다수의 가감산기 병렬 배치가 가능한가?

### 안티패턴

- **오버플로 무시**: 4비트 부호 있는 정수 연산에서 V 플래그를 체크하지 않으면 +7 + 1 = -8이라는 잘못된 결과를 프로그램이 그대로 사용할 수 있다. 특히 보안 관점에서 정수 오버플로는 심각한 취약점(Integer Overflow Vulnerability)이 된다.
- **부호 있는/없는 혼용**: 부호 있는 비교는 V/N 플래그를 사용하고, 부호 없는 비교는 C 플래그를 사용한다. 혼용하면 잘못된 비교 결과가 발생한다. 예: 0xFFFFFFFF > 0x00000001 (부호 없는: 참, 부호 있는: -1 < 1 = 거짓).
- **RCA로 고속 ALU 구현**: 32비트 RCA는 수십 나노초의 지연이 발생하여 GHz 클록에서 1클락 연산이 불가능하다. 고속 ALU에는 반드시 CLA(Kogge-Stone, Brent-Kung 등) 구조를 사용해야 한다.

- **📢 섹션 요약 비유**: 온도계가 최대 눈금을 초과하면 바늘이 반대쪽으로 튀는 것처럼 — 오버플로는 결과가 표현 범위를 벗어나는 것.

---

## Ⅴ. 기대효과 및 결론

병렬 가감산기는 현대 디지털 시스템에서 산술 연산의 핵심 회로다. 단일 제어 신호로 덧셈·뺄셈을 모두 처리하고, 오버플로·캐리·제로·음수 플래그를 생성하여 조건 분기와 비교 연산을 지원한다. 이 단순하지만 강력한 설계는 70년 이상 디지털 컴퓨팅의 기반을 이루고 있다.

| 기대효과 | 내용 |
|:---|:---|
| **회로 통합** | 별도 감산기 불필요, 단일 회로로 ADD/SUB |
| **플래그 지원** | NZCV 플래그로 다양한 조건 분기 지원 |
| **고속화** | CLA 기반으로 O(log n) 지연 달성 |
| **확장성** | SIMD로 수십~수백 개 병렬 배치 가능 |
| **보안성** | 오버플로 감지로 정수 오버플로 취약점 방지 |

AI 시대의 딥러닝 가속기(TPU, GPU)에서 행렬 곱셈(GEMM)의 누적 덧셈은 모두 병렬 가감산기 기반이다. FP16/BF16 형식의 부동소수점 가산은 가수 부분의 정렬 후 정수 병렬 가감산기로 처리되며, 엔비디아 A100 GPU의 경우 FP16 가산기가 수천 개 병렬로 동작하여 초당 수백 테라플롭(TFLOPS)의 성능을 달성한다.

- **📢 섹션 요약 비유**: CPU 3GHz는 초당 30억 번 계산 — 가감산기가 0.15나노초 이내에 끝나야 다음 명령을 받을 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **전가산기** | 병렬 가감산기의 기본 블록 |
| **2의 보수** | XOR+Carry-In으로 뺄셈 구현 원리 |
| **CLA** | O(log n) 고속 캐리 처리 |
| **NZCV 플래그** | 조건 분기 및 비교 연산 지원 |
| **오버플로** | V = C_out XOR C_n-1 검출 |
| **ALU** | 가감산기 + 논리연산 통합 |
| **SIMD** | 다수 가감산기 벡터 병렬 처리 |
| **CMP 명령어** | 감산 후 플래그만 저장 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">전감산기 + 전가산기 분리 — 각각 독립 회로 (비효율)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">병렬 가감산기 통합 — XOR + Carry-In으로 ADD/SUB 공용</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">CLA로 고속화 — O(log n) Carry 계산 (Intel/AMD ALU)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">NZCV 플래그 — 조건 분기 연산 지원 표준화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">파이프라인 ALU — 1클락 64비트 가감산</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">SIMD + 벡터 ALU — 256/512비트 병렬 연산 (AVX-512)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">AI 가속기 — 행렬 곱 전용 병렬 가산기 (TPU, GPU)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 병렬 가감산기는 스위치 하나로 덧셈과 뺄셈을 모두 할 수 있는 계산기 회로예요.
2. 자리 올림수(Carry)를 미리 계산하는 CLA 방식 덕분에 32자리 수도 빠르게 계산할 수 있어요.
3. 오버플로는 계산기 표시 범위를 벗어나는 것 — CPU가 이를 감지해서 프로그램이 이상한 결과를 쓰지 않도록 막아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 38 / 803

← **이전**: [037. 감산기 (Subtractor) — 반감산기·전감산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/037_subtractor/)
**다음**: [039. 디코더 (Decoder) — n-to-2^n 조합 논리 회로](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) →

---
