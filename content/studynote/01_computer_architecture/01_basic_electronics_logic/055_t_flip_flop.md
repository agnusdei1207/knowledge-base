+++
title = "55. T 플립플롭 (T Flip-Flop)"
date = 2026-05-01

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: T 플립플롭 (T Flip-Flop, Toggle Flip-Flop)은 T=1일 때 상태를 반전하고, T=0일 때 유지하는 순차회로다. J-K 플립플롭의 J=K=T인 특수형이며, 가장 단순한 방식으로 2진 계수를 구현한다.
> 2. **가치**: 카운터와 주파수 분주기(Frequency Divider)에서 매우 유용하며, T=1 고정 시 매 클록마다 토글하여 자동으로 2분주기 동작을 한다. n개 직렬 연결로 n비트 카운터를 자연스럽게 구성한다.
> 3. **판단 포인트**: "toggle" 동작이 핵심이므로 주기성과 엣지 타이밍을 함께 봐야 한다. D 플립플롭으로 구현 시 D = T XOR Q로 연결하면 된다.

---

## Ⅰ. 개요 및 필요성

T 플립플롭은 이름 그대로 Toggle을 위한 플립플롭이다. 모든 플립플롭 유형 중 가장 단순한 동작 원리(T=1이면 반전, T=0이면 유지)를 가지면서도, 디지털 시스템에서 가장 자주 사용되는 응용 중 하나인 카운터와 분주기의 핵심 블록이 된다.

T 플립플롭의 등장 배경은 2진 카운터 설계에서 찾을 수 있다. 2진 카운터의 각 자리는 아래 자리가 0→1로 바뀔 때(즉 아래 자리가 1에서 0으로 토글할 때) 반전한다. 이 "조건부 반전" 동작이 T 플립플롭의 본질이다. T=1이면 다음 클록에서 반전, T=0이면 유지.

J-K 플립플롭에서 J와 K를 같은 값으로 묶으면 T 플립플롭이 된다. J=K=0이면 유지(J-K의 00 상태), J=K=1이면 토글(J-K의 11 상태). 따라서 T=J=K 하나의 입력으로 제어된다. 이는 J-K의 set/reset 기능을 포기하는 대신 입력을 단순화한 것이다.

- **📢 섹션 요약 비유**: T 플립플롭은 스위치를 한 번 누를 때마다 켜지고 꺼지는 전등이다. 스위치를 누르면(T=1) 상태가 바뀌고, 누르지 않으면(T=0) 그대로다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### T 플립플롭 동작표

| T | Q(현재) | Q(next) | 설명 |
| :---: | :---: | :---: | :--- |
| 0 | 0 | 0 | 유지 |
| 0 | 1 | 1 | 유지 |
| 1 | 0 | 1 | 반전 (0→1) |
| 1 | 1 | 0 | 반전 (1→0) |

부울식: Q(next) = T XOR Q(현재) = T ⊕ Q

### T 플립플롭 구현 방법



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">방법 1: J-K 플립플롭에서 구현</div>
<div class="kb-diagram-note">J = T, K = T (J와 K를 묶어 T로 연결)</div>
<div class="kb-diagram-note">→ T=0: J=K=0 → 유지</div>
<div class="kb-diagram-note">→ T=1: J=K=1 → 토글</div>
<div class="kb-diagram-note">방법 2: D 플립플롭에서 구현</div>
<div class="kb-diagram-note">D = T XOR Q (XOR 게이트 하나 추가)</div>
<div class="kb-diagram-note">→ T=0: D = 0 XOR Q = Q → Q 유지 (Q가 다시 입력됨)</div>
<div class="kb-diagram-note">→ T=1: D = 1 XOR Q = Q' → Q 반전</div>
<div class="kb-diagram-note">구현 게이트 수:</div>
<div class="kb-diagram-note">JK→T: J=K=T 연결만 (추가 게이트 없음)</div>
<div class="kb-diagram-note">D→T: XOR 게이트 1개 추가 (약 8T CMOS)</div>
</div>
</div>



### 주파수 분주기 동작



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">T=1 고정 시 파형:</div>
<div class="kb-diagram-note">CLK: 0101010101010101</div>
<div class="kb-diagram-note">Q: 0011001100110011 (T=1이면 매 상승 엣지마다 토글)</div>
<div class="kb-diagram-note">결과: CLK 주파수의 1/2 출력</div>
<div class="kb-diagram-note">→ 2분주기 (Divide-by-2)</div>
<div class="kb-diagram-note">n개 직렬 T 플립플롭 (모두 T=1 고정):</div>
<div class="kb-diagram-note">FF0: CLK/2 (최하위 비트)</div>
<div class="kb-diagram-note">FF1: CLK/4</div>
<div class="kb-diagram-note">FF2: CLK/8</div>
<div class="kb-diagram-note">FF3: CLK/16</div>
<div class="kb-diagram-note">...</div>
<div class="kb-diagram-note">FFn: CLK/2^(n+1)</div>
<div class="kb-diagram-note">→ n비트 이진 카운터 (비동기, 리플 방식)</div>
</div>
</div>



### 2비트 카운터 예시



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">2비트 T 플립플롭 카운터 (T=1 고정):</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">클록</div><div class="kb-diagram-cell">Q1 Q0</div><div class="kb-diagram-cell">10진수</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">초기</div><div class="kb-diagram-cell">0 0</div><div class="kb-diagram-cell">0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↑ 1</div><div class="kb-diagram-cell">0 1</div><div class="kb-diagram-cell">1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↑ 2</div><div class="kb-diagram-cell">1 0</div><div class="kb-diagram-cell">2</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↑ 3</div><div class="kb-diagram-cell">1 1</div><div class="kb-diagram-cell">3</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">↑ 4</div><div class="kb-diagram-cell">0 0</div><div class="kb-diagram-cell">0 (4에서 0으로 되돌아감)</div></div>
<div class="kb-diagram-note">Q0: 매 클록마다 토글 (2분주)</div>
<div class="kb-diagram-note">Q1: Q0가 1→0이 될 때 토글 (4분주)</div>
</div>
</div>



- **📢 섹션 요약 비유**: T 플립플롭은 한 칸씩 넘어가는 계단 스위치다. 누를 때마다 올라가고(반전), 안 누르면 그 자리를 유지한다.

---

## Ⅲ. 비교 및 연결

### 4종 플립플롭 비교

| 항목 | D | J-K | T | S/R |
| :--- | :--- | :--- | :--- | :--- |
| **역할** | 저장 | set/reset/toggle | toggle | set/reset |
| **입력 수** | 1(D) | 2(J,K) | 1(T) | 2(S,R) |
| **복잡도** | 낮음 | 중간 | 낮음 | 낮음 |
| **금지 상태** | 없음 | 없음 | 없음 | S=R=1 |
| **토글** | 불가 | J=K=1 가능 | T=1 항상 | 불가 |
| **대표 응용** | 레지스터 | FSM, 카운터 | 카운터, 분주기 | 기본 래치 |
| **J-K 관계** | J=D, K=D' | 일반형 | J=K=T | 기원 |

### T 플립플롭 활용 비교

| 활용 | T 고정값 | 동작 |
|:---|:---:|:---|
| 2분주기 | 1 | 매 클록 토글 |
| 비동기 카운터 | 1 | 직렬 연결 |
| 동기 카운터 | 조합 논리 결과 | 선택적 토글 |
| 분주기 체인 | 1 | CLK/2^n |
| 조건부 증가 | Enable 신호 | T=Enable AND 조건 |

- **📢 섹션 요약 비유**: T는 두 칸짜리 방에서 문을 열 때마다 방이 바뀌는 장난감이다. D는 특정 방에 집어넣는 것이고, J-K는 원하는 방을 선택하거나 반전할 수 있는 것이다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 동기 8비트 카운터에서 T 입력 논리



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">동기 3비트 이진 카운터 (T 플립플롭 기반):</div>
<div class="kb-diagram-note">T0 = 1 (Q0는 항상 토글)</div>
<div class="kb-diagram-note">T1 = Q0 (Q0=1일 때만 Q1 토글)</div>
<div class="kb-diagram-note">T2 = Q0 AND Q1 (Q0=Q1=1일 때만 Q2 토글)</div>
<div class="kb-diagram-note">상태 전이:</div>
<div class="kb-diagram-note">000 → 001 → 010 → 011 → 100 → 101 → 110 → 111 → 000</div>
<div class="kb-diagram-note">이 패턴에서:</div>
<div class="kb-diagram-note">Q0: 1,2,3,4,5,6,7클록 후 반전 (매 클록)</div>
<div class="kb-diagram-note">Q1: Q0=1일 때만 반전 (2클록마다)</div>
<div class="kb-diagram-note">Q2: Q0=Q1=1일 때만 반전 (4클록마다)</div>
</div>
</div>



### 주파수 분주기 설계 (클록 도메인 교차)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">50MHz → 1Hz 클록 생성 (카운터 기반):</div>
<div class="kb-diagram-note">50,000,000 = 2^25.57... → 26비트 카운터 필요</div>
<div class="kb-diagram-note">실제 구현:</div>
<div class="kb-diagram-note">26개의 T 플립플롭 직렬 연결 (비동기)</div>
<div class="kb-diagram-note">또는</div>
<div class="kb-diagram-note">25비트 동기 카운터 + 출력 게이트</div>
<div class="kb-diagram-note">카운터 최상위 비트가 1Hz 클록으로 사용됨</div>
<div class="kb-diagram-note">FPGA 구현 예 (VHDL):</div>
<div class="kb-diagram-note">process(clk)</div>
<div class="kb-diagram-note">begin</div>
<div class="kb-diagram-note">if rising_edge(clk) then</div>
<div class="kb-diagram-note">counter &lt;= counter + 1;</div>
<div class="kb-diagram-note">end if;</div>
<div class="kb-diagram-note">end process;</div>
<div class="kb-diagram-note">slow_clk &lt;= counter(25); -- 50MHz / 2^26 ≈ 0.74Hz</div>
</div>
</div>



### 설계 판단 체크리스트

1. 토글이 필요한 카운터인가? T 플립플롭 또는 D+XOR 선택
2. 클록 에지 기준이 분명한가? (상승/하강 엣지 선택)
3. 비동기 카운터의 리플 지연이 허용 가능한가?
4. 동기 카운터가 필요하면 T 입력 조합 논리를 설계했는가?
5. 분주 비율이 요구사항과 일치하는가?
6. FPGA라면 내장 카운터 프리미티브를 활용하는 게 나은가?

### 안티패턴

- **비동기 카운터의 글리치 무시**: 비동기 카운터에서 각 플립플롭의 전파 지연 차이로 순간적인 잘못된 출력(Glitch)이 발생한다. 예: 011→100 전환 시 011→111→101→100 같은 중간 글리치가 나타날 수 있다. 고속 회로에서는 동기 카운터를 사용해야 한다.
- **클록 글리치로 오동작**: T 입력의 글리치나 클록 신호의 노이즈가 T=1 구간을 만들어 의도치 않은 토글을 유발한다. 클록 신호에 필터나 버퍼를 사용해야 한다.
- **반전 조건 명확화 미흡**: 동기 카운터에서 T 입력 논리를 잘못 설계하면 카운터가 잘못된 순서로 동작한다. 상태 다이어그램과 T 입력 표(Excitation Table)를 항상 함께 검토해야 한다.

- **📢 섹션 요약 비유**: T 플립플롭은 계단을 오를 때마다 한 칸씩 넘어가는 발판이다. 발판을 밟으면(T=1) 한 칸 위로, 안 밟으면(T=0) 그자리 유지다.

---

## Ⅴ. 기대효과 및 결론

T 플립플롭은 구현이 단순하고 카운터 설계에 직관적이다. 토글 기반 순차회로의 대표 예이며, 모든 디지털 시스템의 클록 분주 회로에 이 원리가 사용된다.

| 기대효과 | 내용 |
|:---|:---|
| **카운터 최적화** | 단순한 입력(T=1 고정)으로 자연스러운 이진 카운터 |
| **주파수 분주** | n개 직렬로 CLK/2^n 생성 |
| **설계 단순화** | J-K의 토글 기능만 필요할 때 입력 수 감소 |
| **교육적 가치** | 이진 표현과 카운터의 연결을 직관적으로 설명 |
| **FPGA 활용** | 합성 도구가 자동으로 D+XOR 또는 J-K로 변환 |

현대 FPGA에서 T 플립플롭은 직접 지원되는 경우도 있지만, 대부분 D 플립플롭과 XOR 게이트의 조합으로 합성된다. 딥러닝 칩에서도 메모리 접근 카운터, 타이밍 발생기, 시퀀스 제어 회로에 T 플립플롭 원리가 광범위하게 활용된다.

- **📢 섹션 요약 비유**: T 플립플롭은 전등을 켰다 껐다만 하는 스위치다. 복잡한 조건 없이 오직 "반전"이라는 단순한 동작으로 이진 카운팅이라는 강력한 기능을 구현한다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| **Toggle** | T=1이면 Q 상태 반전 |
| **카운터** | T 플립플롭 직렬 연결 |
| **J-K 플립플롭** | J=K=T인 일반형 |
| **D 플립플롭** | D = T XOR Q로 구현 |
| **주파수 분주기** | CLK/2^n 생성 |
| **LFSR** | 특수한 피드백 시프트 레지스터 |
| **비동기 카운터** | 직렬 T FF 연결 |
| **동기 카운터** | T 입력 조합 논리 설계 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">J-K 플립플롭 (J=K=T인 특수형 연결)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">T 플립플롭 (Toggle 전용, 단순화)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">비동기 카운터 (직렬 T FF, T=1 고정)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">동기 카운터 (T 입력 조합 논리 설계)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">주파수 분주기 (CLK/2, CLK/4, ..., CLK/2^n)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">클록 생성기, 타이머 (SoC 내 타임베이스)</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. T 플립플롭은 스위치를 누를 때마다 켜지고 꺼져요.
2. 누르지 않으면 그대로예요.
3. 그래서 숫자를 세거나 시간을 재는 카운터 만들기에 딱 좋아요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 55 / 803

← **이전**: [54. J-K 플립플롭 (J-K Flip-Flop)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/054_jk_flip_flop/)
**다음**: [56. 마스터-슬레이브 플립플롭 (Master-Slave Flip-Flop)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/056_master_slave_flip_flop/) →

---
