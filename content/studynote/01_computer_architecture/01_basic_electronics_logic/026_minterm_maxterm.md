+++
title = "26. 최소항·최대항 (Minterm / Maxterm) — 부울 함수 표준형"
date = 2026-04-29

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 최소항(Minterm)은 n개의 변수가 모두 AND로 연결된 곱항(Product Term)으로, 각 변수는 보수(Complement) 또는 비보수(Non-complement) 형태로 정확히 한 개의 입력 조합에서만 1이 된다. 최대항(Maxterm)은 n개의 변수가 모두 OR로 연결된 합항(Sum Term)으로, 정확히 한 입력 조합에서만 0이 된다.
> 2. **가치**: 부울 함수는 최소항의 합(SOP, Sum of Products)인 정규합 형태(Canonical SOP)와 최대항의 곱(POS, Product of Sums)인 정규곱 형태(Canonical POS)로 유일하게 표현될 수 있다. 이 두 표준형은 [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/)([Karnaugh Map](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/)) 최적화와 게이트 회로 구현의 이론적 기반이다.
> 3. **판단 포인트**: SOP는 1이 되는 입력 조합(Minterm)을 합산하고, POS는 0이 되는 입력 조합(Maxterm)을 곱한다. 진리표에서 1이 적으면 SOP, 0이 적으면 POS가 더 간단한 회로로 구현되므로, 실무에서는 1과 0의 개수를 비교해 표준형을 선택한다.

---

## Ⅰ. 개요 및 필요성

디지털 논리 회로 설계에서 가장 중요한 출발점은 "어떤 함수도 표준적이고 유일한 방법으로 표현할 수 있는가?"라는 질문이다. 이 질문에 답하는 것이 바로 최소항(Minterm)과 최대항(Maxterm)의 개념이다. 1800년대 조지 불(George Boole)이 정립한 불 대수(Boolean Algebra) 위에, 20세기 초 클로드 섀넌(Claude Shannon)이 이진 전자 회로에 적용하며 최소항·최대항은 디지털 설계의 기본 언어가 되었다.

n개의 변수로 정의되는 진리표는 2^n개의 행을 가지며, 각 행은 하나의 입력 조합을 나타낸다. 최소항은 이 각 조합에 대응하는 "AND로 묶인 항"이고, 최대항은 "OR로 묶인 항"이다. 임의의 부울 함수를 최소항의 합(SOP)이나 최대항의 곱(POS)으로 표현하면 표현 방식이 유일(Canonical)해진다. 이는 수학의 소인수분해처럼, 복잡한 논리 함수를 표준 단위 조각으로 분해할 수 있게 한다.

2변수 A, B의 최소항(m)과 최대항(M) 전체 목록:

| 행 | A | B | Minterm (mi) | Maxterm (Mi) |
|:---:|:---:|:---:|:---:|:---:|
| 0 | 0 | 0 | m0 = A'B' | M0 = A + B |
| 1 | 0 | 1 | m1 = A'B | M1 = A + B' |
| 2 | 1 | 0 | m2 = AB' | M2 = A'+ B |
| 3 | 1 | 1 | m3 = AB | M3 = A'+ B' |

*mi = 해당 행에서만 1 | Mi = 해당 행에서만 0*

최소항의 핵심 특성: 변수 값이 1이면 원래 변수(A), 0이면 보수 형태(A')로 표현하며, 그 결과 해당 입력 조합에서만 AND 전체가 1이 된다. 반면 최대항은 변수 값이 0이면 원래 변수(A), 1이면 보수 형태(A')로 표현하여, 해당 행에서만 OR 전체가 0이 된다.

- **📢 섹션 요약 비유**: 최소항은 자물쇠 잠금 코드다. 3자리 코드(A,B,C)에서 오직 '101' 조합에서만 자물쇠(AND)가 열린다. 최대항은 반대로 오직 '010' 조합에서만 잠금(OR=0)된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### SOP (정규합) vs POS (정규곱)

3변수 함수 F(A, B, C) 예시:



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">진리표: F(A,B,C)</div>
<div class="kb-diagram-note">A B C | F</div>
<div class="kb-diagram-note">0 0 0 | 0 ← Maxterm M0</div>
<div class="kb-diagram-note">0 0 1 | 1 ← Minterm m1</div>
<div class="kb-diagram-note">0 1 0 | 0 ← Maxterm M2</div>
<div class="kb-diagram-note">0 1 1 | 1 ← Minterm m3</div>
<div class="kb-diagram-note">1 0 0 | 0 ← Maxterm M4</div>
<div class="kb-diagram-note">1 0 1 | 1 ← Minterm m5</div>
<div class="kb-diagram-note">1 1 0 | 0 ← Maxterm M6</div>
<div class="kb-diagram-note">1 1 1 | 1 ← Minterm m7</div>
<div class="kb-diagram-note">SOP = Σm(1,3,5,7) = A'B'C + A'BC + AB'C + ABC = C</div>
<div class="kb-diagram-note">POS = ΠM(0,2,4,6) = (A+B+C)(A+B'+C)(A'+B+C)(A'+B'+C) = C</div>
</div>
</div>



위 예시는 F=C로 간소화되지만, 최소항/최대항 전개를 거쳐야만 그 유일성과 등가성이 수학적으로 보장된다.

### 3변수 최소항 완전 목록

| 번호 | A | B | C | Minterm 식 |
|:---:|:---:|:---:|:---:|:---:|
| m0 | 0 | 0 | 0 | A'B'C' |
| m1 | 0 | 0 | 1 | A'B'C |
| m2 | 0 | 1 | 0 | A'BC' |
| m3 | 0 | 1 | 1 | A'BC |
| m4 | 1 | 0 | 0 | AB'C' |
| m5 | 1 | 0 | 1 | AB'C |
| m6 | 1 | 1 | 0 | ABC' |
| m7 | 1 | 1 | 1 | ABC |

### 3변수 최대항 완전 목록

| 번호 | A | B | C | Maxterm 식 |
|:---:|:---:|:---:|:---:|:---:|
| M0 | 0 | 0 | 0 | A+B+C |
| M1 | 0 | 0 | 1 | A+B+C' |
| M2 | 0 | 1 | 0 | A+B'+C |
| M3 | 0 | 1 | 1 | A+B'+C' |
| M4 | 1 | 0 | 0 | A'+B+C |
| M5 | 1 | 0 | 1 | A'+B+C' |
| M6 | 1 | 1 | 0 | A'+B'+C |
| M7 | 1 | 1 | 1 | A'+B'+C' |

### 최소항-최대항 이중성 (Duality)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">mi 와 Mi는 드모르간 법칙으로 서로 보수:</div>
<div class="kb-diagram-note">m0 = A'B' → 보수 취하면 → A + B = M0</div>
<div class="kb-diagram-note">m1 = A'B → 보수 취하면 → A + B' = M1</div>
<div class="kb-diagram-note">F = Σm(1,3) = ΠM(0,2)</div>
<div class="kb-diagram-note">즉, SOP에 포함된 Minterm 번호와</div>
<div class="kb-diagram-note">POS에서 제외된 Maxterm 번호는 서로 여집합</div>
<div class="kb-diagram-note">핵심 관계:</div>
<div class="kb-diagram-note">mi의 보수 = Mi (드모르간 법칙)</div>
<div class="kb-diagram-note">SOP Minterm 집합 ∪ POS Maxterm 집합 = 전체 집합</div>
<div class="kb-diagram-note">SOP Minterm 집합 ∩ POS Maxterm 집합 = 공집합</div>
</div>
</div>



### SOP/POS 변환 방법



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">1. SOP → POS 변환:</div>
<div class="kb-diagram-note">F = Σm(0,2,5) (3변수)</div>
<div class="kb-diagram-note">POS: SOP에 없는 번호가 POS 번호</div>
<div class="kb-diagram-note">나머지 번호: 1, 3, 4, 6, 7</div>
<div class="kb-diagram-note">→ ΠM(1,3,4,6,7)</div>
<div class="kb-diagram-note">2. POS → SOP 변환:</div>
<div class="kb-diagram-note">F = ΠM(0,3,6)</div>
<div class="kb-diagram-note">SOP: POS에 없는 번호</div>
<div class="kb-diagram-note">나머지 번호: 1, 2, 4, 5, 7</div>
<div class="kb-diagram-note">→ Σm(1,2,4,5,7)</div>
</div>
</div>



- **📢 섹션 요약 비유**: SOP와 POS는 같은 문을 양쪽에서 설명하는 것이다. "문이 열리는 3가지 경우(SOP)"와 "문이 닫히는 5가지 경우(POS)"는 같은 문의 서로 다른 설명이지만 완전히 동등하다.

---

## Ⅲ. 비교 및 연결

| 항목 | SOP (최소항 합) | POS (최대항 곱) |
|:---|:---|:---|
| **구성 단위** | 최소항 AND로 묶음 | 최대항 OR로 묶음 |
| **F=1 조건** | 포함된 최소항이 1일 때 | 모든 최대항이 1일 때 |
| **논리 게이트** | AND → OR (2단) | OR → AND (2단) |
| **최적화 도구** | [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/) (1 묶기) | [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/) (0 묶기) |
| **장점** | 1의 개수가 적을 때 유리 | 0의 개수가 적을 때 유리 |
| **회로 구조** | NAND-NAND 등가 | NOR-NOR 등가 |
| **HDL 표현** | assign F = m1\|m3\|m5 | assign F = M0&M2&M4 |

### 관련 개념과의 연결

| 관련 개념 | 연결 방식 |
|:---|:---|
| 불 대수(Boolean Algebra) | 최소항/최대항의 수학적 기반 |
| [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/) | 최소항 그룹화로 간소화 |
| 드모르간 법칙 | mi ↔ Mi 보수 변환 원리 |
| NAND/NOR 게이트 | SOP/POS의 실제 구현 소자 |
| EDA 논리 합성 | 최소항 기반 자동 회로 합성 내부 표현 |
| VHDL/Verilog | HDL에서 최소항 기반 회로 기술 |

### 표준형 선택 기준



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">진리표 분석:</div>
<div class="kb-diagram-note">1의 개수 &lt; 0의 개수 → SOP가 더 간단</div>
<div class="kb-diagram-note">0의 개수 &lt; 1의 개수 → POS가 더 간단</div>
<div class="kb-diagram-note">같은 경우 → 카르노 맵으로 추가 판단</div>
<div class="kb-diagram-note">예: 8행 진리표에서 F=1 행이 3개, F=0 행이 5개</div>
<div class="kb-diagram-note">→ SOP = Σm(a,b,c) : 3항 합</div>
<div class="kb-diagram-note">→ POS = ΠM(d,e,f,g,h) : 5항 곱</div>
<div class="kb-diagram-note">→ SOP 선택 (항 수가 적음)</div>
</div>
</div>



- **📢 섹션 요약 비유**: SOP는 "이 재료들이 있으면 요리 완성(OR/합)", POS는 "이 재료들이 하나라도 빠지면 요리 실패(AND/곱)"이다. 결과는 같지만 레시피 작성 방식이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### VHDL/Verilog 회로 구현 예시

```verilog
// F = Σm(1,3,5,7) = C (SOP로 최적화)
module func_f(input A, B, C, output F);
    assign F = C;  // 카르노 맵으로 C로 간소화
endmodule

// 카르노 맵 없이 SOP 직접 구현 (비최적화)
assign F = (~A & ~B & C) | (~A & B & C) |
           (A & ~B & C)  | (A & B & C);
// = C (드모르간+부울 대수로 동일)

// POS 방식 구현
module func_f_pos(input A, B, C, output F);
    // F = ΠM(0,2,4,6) = C
    assign F = (A|B|C) & (A|~B|C) & (~A|B|C) & (~A|~B|C);
    // = C (동일 결과)
endmodule
```

### 설계 판단 체크리스트

1. 진리표에서 1의 개수와 0의 개수를 비교했는가?
2. SOP/POS 중 더 적은 항을 가진 방식을 선택했는가?
3. 카르노 맵으로 최소항 그룹화가 가능한가?
4. don't care 조건이 있다면 최소항 번호에 포함시켰는가?
5. 최적화된 식을 NAND/NOR 게이트로 변환 가능한가?
6. EDA 도구에 최소항 번호를 정확히 입력했는가?

### 안티패턴

- **비최적 표준형 사용**: 1이 7개, 0이 1개인 진리표에서 SOP(7항)를 쓰는 경우. POS(1항)가 훨씬 간단하다.
- **don't care 누락**: 사용하지 않는 입력 조합을 최적화에 활용하지 않으면 게이트 수가 불필요하게 늘어난다. don't care는 Σd(...)로 별도 표기하고 카르노 맵에서 'X'로 처리해야 한다.
- **최소항 번호 오류**: 변수 순서(MSB→LSB)를 잘못 지정하면 완전히 다른 함수가 된다. 항상 "A는 최상위 비트" 등의 순서를 명시해야 한다.

- **📢 섹션 요약 비유**: [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/)이 없는 SOP 직접 구현은 긴 문장을 줄임말 없이 쓰는 것이고, [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/) 최적화는 "등"으로 줄여쓰는 것이다. 둘 다 같은 의미지만 간결함이 다르다.

---

## Ⅴ. 기대효과 및 결론

최소항·최대항의 도입으로 디지털 논리 설계는 다음과 같은 구조적 이점을 얻는다.

| 기대효과 | 내용 |
|:---|:---|
| **표준화** | 어떤 부울 함수도 SOP/POS로 유일 표현 |
| **최적화 기반** | [카르노 맵](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/) 최적화의 이론적 시작점 |
| **CAD 합성** | 논리 합성 도구(EDA)의 내부 표현 형태 |
| **게이트 최소화** | 최소항 수 최소화 = 게이트 수 최소화 |
| **설계 검증** | 두 회로가 동일한 최소항 집합이면 동등함 증명 가능 |
| **HDL 자동화** | SystemVerilog, VHDL에서 case문을 최소항으로 자동 변환 |

최소항/최대항은 디지털 회로 설계 자동화 도구(EDA, Electronic Design Automation)의 논리 합성(Logic Synthesis) 내부에서 BDD (Binary Decision Diagram)와 함께 게이트 최소화에 활용된다. 현대 FPGA와 ASIC 설계에서 수백만 개의 게이트를 자동으로 최적화하는 EDA 도구들은 내부적으로 모두 최소항/최대항 기반 알고리즘(Quine-McCluskey, Espresso 등)을 사용한다.

또한 정형 검증(Formal Verification) 분야에서도 BDD와 결합하여, 두 회로가 동일한 부울 함수를 구현하는지(등가 검증, Equivalence Checking) 확인하는 데 핵심적으로 활용된다. 기술사 시험에서는 "SOP vs POS 선택 기준"과 "don't care 조건 처리"가 자주 출제된다.

- **📢 섹션 요약 비유**: 최소항/최대항은 디지털 회로의 악보다. 음악(부울 함수)을 악보(SOP/POS)로 적으면 어떤 연주자(회로 합성 도구)도 동일하게 연주할 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| <strong><a href="/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/">카르노 맵</a></strong> | 최소항/최대항 기반 함수 최적화 |
| **SOP/POS** | 표준 정규형 표현 |
| **드모르간 법칙** | 최소항↔최대항 변환 원리 |
| **논리 합성 (EDA)** | 최소항 기반 자동 회로 합성 |
| **VHDL/Verilog** | 최소항 기반 회로 [HDL](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/072_hdl/) 구현 |
| **Quine-McCluskey** | 최소항 기반 함수 최소화 알고리즘 |
| **BDD** | Binary Decision Diagram, 최소항 공간 효율 표현 |
| **don't care** | 미사용 최소항, 최적화 활용 가능 |

### 📈 관련 키워드 및 발전 흐름도



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">진리표 — 입출력 완전 정의</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">최소항/최대항 — SOP/POS 표준형 변환</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">카르노 맵 — 최소항 그룹화로 간소화 (1~4변수)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">Quine-McCluskey — 5변수 이상 알고리즘 최소화</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">논리 게이트 회로 — AND/OR/NOT 구현</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">EDA 논리 합성 — 자동 최적화 회로 생성 (Espresso 등)</div>
<div class="kb-diagram-connector">▼</div>
<div class="kb-diagram-note">FPGA/ASIC — 최종 물리 회로 구현</div>
</div>
</div>



### 👶 어린이를 위한 3줄 비유 설명

1. 최소항은 자물쇠 비밀번호예요! 3개의 버튼 중 딱 하나의 조합에서만 불(1)이 켜지는 특별한 코드예요.
2. 최대항은 반대로, 딱 하나의 조합에서만 불이 꺼지는(0) 코드예요.
3. 이 두 가지를 이용하면 어떤 복잡한 회로도 "켜지는 경우의 합(SOP)" 또는 "꺼지는 경우의 곱(POS)"으로 완벽하게 표현할 수 있답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 26 / 803

← **이전**: [25. 카르노 맵 (Karnaugh Map) — 진리표의 시각적 논리 최적화](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/025_karnaugh_map/)
**다음**: [27. 논리 게이트 (Logic Gates) — 디지털 회로의 기본 소자](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/027_logic_gates/) →

---
