+++
title = "조합 논리 회로 (Combinational Logic Circuit)"
date = 2026-03-03

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

> **핵심 인사이트 3줄**
> 1. 조합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 회로(Combinational Logic Circuit)는 현재 입력만으로 출력이 결정되며, 기억 소자 없이 [논리 게이트](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/027_logic_gates/) 조합만으로 구성된다.
> 2. [진리표](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/024_truth_table/) → 부울 식 → [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/) → 게이트 최소화의 설계 흐름이 회로 복잡도를 줄이는 핵심이다.
> 3. 가산기·[비교기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/)·[멀티플렉서](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/041_multiplexer/)·[디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) 등 모든 [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) 연산 기반 회로가 조합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 원리로 동작한다.

---

## Ⅰ. 조합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 회로의 정의와 특성

조합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 회로(Combinational Logic Circuit)는 <strong>출력이 오직 현재 입력 조합에만 의존</strong>하는 회로다. 피드백이나 클럭이 없어 시간 개념이 없으며, 같은 입력이면 항상 같은 출력을 생성한다.

| 특성        | 조합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)           | 순서 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)             |
|------------|--------------------|-----------------------|
| 출력 결정   | 현재 입력만         | 입력 + 이전 상태      |
| 기억 소자   | 없음                | FF/[레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/) 있음      |
| 클럭        | 불필요              | 필요                  |
| 예시        | 가산기, [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)       | [카운터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/059_counter/), [레지스터](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/057_register/)       |



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">입력 A ──</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">─</div><div class="kb-diagram-node">AND</div><div class="kb-diagram-note">─</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">입력 B ── ─</div><div class="kb-diagram-node">OR</div><div class="kb-diagram-note">출력 Y</div></div>
<div class="kb-diagram-note">입력 C</div>
</div>
</div>



📢 **섹션 요약 비유**: 조합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 회로는 자판기 같다. 동전(입력)을 넣으면 곧바로 음료(출력)가 나오고, 과거에 뭘 눌렀는지는 기억하지 않는다.

---

## Ⅱ. 설계 방법론 — [부울 대수](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/022_boolean_algebra/)와 [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/)

### 설계 흐름

```
문제 정의 → 진리표 작성 → 부울 식 도출 → 카르노 맵 최소화 → 게이트 구현
```

### [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/) ([Karnaugh Map](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/)) 예시 — 2변수

```
      B=0   B=1
A=0 |  0  |  1  |
A=1 |  1  |  1  |
```
→ 최소화 결과: Y = A + B (OR 게이트 1개)

<strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/022_boolean_algebra/">부울 대수</a> 기본 법칙</strong>
- 흡수 법칙: A + AB = A
- 드 모르간: ¬(A·B) = ¬A + ¬B
- 합의 법칙: AB + ¬[AC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/) + BC = AB + ¬[AC](/knowledge-base/studynote/12_it_management/04_sdlc_testing/155_ac_actual_cost/)

📢 **섹션 요약 비유**: [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/)은 퍼즐 게임이다. 1을 그룹으로 묶을수록 수식이 단순해지고, 게이트 수가 줄어 회로 비용이 내려간다.

---

## Ⅲ. 주요 조합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 회로 — [반가산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/033_half_adder/)·[전가산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/034_full_adder/)·[멀티플렉서](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/041_multiplexer/)

### [반가산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/033_half_adder/) ([Half Adder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/033_half_adder/), HA)

| A | B | Sum (S) | Carry (C) |
|---|---|---------|-----------|
| 0 | 0 |    0    |     0     |
| 0 | 1 |    1    |     0     |
| 1 | 0 |    1    |     0     |
| 1 | 1 |    0    |     1     |

- S = A ⊕ B (XOR)
- C = A · B (AND)

### [전가산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/034_full_adder/) ([Full Adder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/034_full_adder/), FA)

- S = A ⊕ B ⊕ Cin
- Cout = AB + Cin(A⊕B)

### 4:1 [멀티플렉서](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/041_multiplexer/) ([MUX](/knowledge-base/studynote/03_network/19_frequent_topics_terms/944_mux_demux_multiplexer_demultiplexer_circuit_sharing/))



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">D0 ──</div>
<div class="kb-diagram-note">D1 ── 4:1 MUX Y</div>
<div class="kb-diagram-note">D2 ──</div>
<div class="kb-diagram-note">D3 ──</div>
<div class="kb-diagram-note">S1 S0 (선택 신호)</div>
</div>
</div>



Y = ¬S1·¬S0·D0 + ¬S1·S0·D1 + S1·¬S0·D2 + S1·S0·D3

📢 **섹션 요약 비유**: [전가산기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/034_full_adder/)는 3자리 덧셈 사람과 같다. 두 수 + 받아올림(Cin)을 더해 합과 올림(Cout)을 출력한다.

---

## Ⅳ. [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)·[인코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)·[비교기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/)·패리티 회로

### 2:4 [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/) ([Decoder](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/))

| EN | A1 | A0 | Y3 | Y2 | Y1 | Y0 |
|----|----|----|----|----|----|----|
|  1 |  0 |  0 |  0 |  0 |  0 |  1 |
|  1 |  0 |  1 |  0 |  0 |  1 |  0 |
|  1 |  1 |  0 |  0 |  1 |  0 |  0 |
|  1 |  1 |  1 |  1 |  0 |  0 |  0 |

### 1비트 크기 [비교기](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/) (Magnitude [Comparator](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/043_comparator/))

- A > B: A · ¬B
- A = B: A ⊕ B = 0 → A XNOR B
- A < B: ¬A · B

### 패리티 생성기 (Parity Generator)

- [짝수 패리티](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/108_even_parity/): P = D3⊕D2⊕D1⊕D0 (XOR 트리)
- 오류 1비트 검출, 수정 불가 → [해밍 코드](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/)([Hamming Code](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/111_hamming_code/))로 수정

📢 **섹션 요약 비유**: [디코더](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/039_decoder/)는 우체국 분류기다. 입력(주소) 2비트로 4개 창구 중 하나에만 패킷을 보낸다.

---

## Ⅴ. 실무 활용 — [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)·[FPGA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/606_dynamic_partial_reconfiguration/)·타이밍 해저드

### [ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) ([Arithmetic Logic Unit](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/)) 내부 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row"><div class="kb-diagram-note">입력 A</div><div class="kb-diagram-node">8bit</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">입력 B</div><div class="kb-diagram-node">8bit</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">OP 코드</div><div class="kb-diagram-node">3bit</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">조합 논리</div><div class="kb-diagram-cell">결과</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">게이트 망</div><div class="kb-diagram-cell">플래그</div></div>
</div>
</div>



### 타이밍 해저드 (Timing Hazard)

| 종류        | 원인                    | 해결                   |
|------------|------------------------|------------------------|
| 정적 해저드  | [전파 지연](/knowledge-base/studynote/03_network/01_data_communication/016_전파_지연/) 차이           | 합의 항(consensus) 추가 |
| 동적 해저드  | 다중 경로 [지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/) 불일치     | 회로 재설계             |

### [FPGA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/606_dynamic_partial_reconfiguration/) 매핑

현대 FPGA는 LUT(Look-Up Table, 룩업 테이블) 기반으로 조합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/)를 구현한다. 4/5/6입력 LUT에 [진리표](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/024_truth_table/)를 직접 저장해 임의 함수를 구현한다.

📢 **섹션 요약 비유**: 타이밍 해저드는 마라톤 릴레이에서 선수들이 다른 경로로 달려 배턴을 동시에 건네지 못하는 것과 같다. 합의 항을 추가하면 두 팀이 동시에 도착하도록 조율된다.

---

## 📌 관련 개념 맵



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">조합 논리 회로</div>
<div class="kb-diagram-tree-item" style="--depth:0">설계 도구</div>
<div class="kb-diagram-note">── 진리표 (Truth Table)</div>
<div class="kb-diagram-note">── 부울 대수 (Boolean Algebra)</div>
<div class="kb-diagram-note">── 카르노 맵 (Karnaugh Map, K-Map)</div>
<div class="kb-diagram-tree-item" style="--depth:0">기본 회로</div>
<div class="kb-diagram-note">── 반가산기 (Half Adder, HA)</div>
<div class="kb-diagram-note">── 전가산기 (Full Adder, FA)</div>
<div class="kb-diagram-note">── 4비트 리플 캐리 가산기 (Ripple Carry Adder, RCA)</div>
<div class="kb-diagram-note">── 선행 올림 가산기 (Carry Look-ahead Adder, CLA)</div>
<div class="kb-diagram-tree-item" style="--depth:0">데이터 선택/변환</div>
<div class="kb-diagram-note">── 멀티플렉서 (Multiplexer, MUX)</div>
<div class="kb-diagram-note">── 디멀티플렉서 (Demultiplexer, DEMUX)</div>
<div class="kb-diagram-note">── 인코더 (Encoder)</div>
<div class="kb-diagram-note">── 디코더 (Decoder)</div>
<div class="kb-diagram-tree-item" style="--depth:0">오류 검출</div>
<div class="kb-diagram-tree-item" style="--depth:2">패리티 비트 (Parity Bit)</div>
<div class="kb-diagram-tree-item" style="--depth:2">해밍 코드 (Hamming Code)</div>
</div>
</div>



---

## 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">조합 논리 회로 기술 발전 흐름</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1940~60년대</div><div class="kb-diagram-cell">진공관/트랜지스터</div><div class="kb-diagram-cell">개별 게이트 회로 구성</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1970년대</div><div class="kb-diagram-cell">SSI/MSI IC</div><div class="kb-diagram-cell">74시리즈 표준 로직 IC 등장</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1980년대</div><div class="kb-diagram-cell">CPLD 등장</div><div class="kb-diagram-cell">프로그래머블 논리 소자</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1990년대</div><div class="kb-diagram-cell">FPGA 일반화</div><div class="kb-diagram-cell">LUT 기반 조합 논리 매핑</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2000년대</div><div class="kb-diagram-cell">EDA 자동화</div><div class="kb-diagram-cell">HDL(VHDL/Verilog) 합성 툴</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">2010~현재</div><div class="kb-diagram-cell">HLS·AI 가속기</div><div class="kb-diagram-cell">조합 논리 → DNN 레이어 매핑</div></div>
<div class="kb-diagram-note">핵심 키워드 연결:</div>
<div class="kb-diagram-note">논리 게이트 → 부울 대수 → 카르노 맵 → 가산기 → ALU</div>
<div class="kb-diagram-note">NAND/NOR 드모르간 SOP/POS 올림 전파 플래그 레지스터</div>
<div class="kb-diagram-note">범용 게이트 CLA(선행 올림)</div>
</div>
</div>



---

## 👶 어린이를 위한 3줄 비유 설명

1. 조합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 회로는 레고 조립과 같다 — 여러 작은 게이트 블록을 연결하면 큰 계산 기계가 만들어진다.
2. [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/)은 퍼즐 맞추기다 — 비슷한 조각을 묶을수록 전체 그림이 단순해진다.
3. 가산기는 받아올림을 하는 수학 선생님이다 — 자리마다 합을 계산하고 넘치면 옆 자리에 알려준다.

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 32 / 803

← **이전**: [31. 범용 게이트 — NAND와 NOR으로 모든 논리를](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/031_universal_gate/)
**다음**: [반가산기 (Half Adder)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/033_half_adder/) →

---
