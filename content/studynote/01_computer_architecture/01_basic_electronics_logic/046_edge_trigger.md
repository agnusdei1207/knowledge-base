+++
title = "046. 에지 트리거 — Edge Trigger"
date = 2026-04-05

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

> **핵심 인사이트**
> 1. 에지 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)(Edge Trigger)는 클럭 신호의 엣지(Rising 또는 Falling) 순간에만 데이터를 샘플링하는 [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/) 동작 방식 — 레벨 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)([Level Trigger](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/047_level_trigger/))보다 타이밍 제어가 정밀하며 현대 디지털 회로에서 표준이다.
> 2. 상승 에지(Rising Edge) [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)는 0→1 전환 순간에 입력 D를 포착해 출력 Q에 저장 — 클럭 사이클당 단 한 번 데이터가 업데이트되므로 레이스 컨디션([Race Condition](/knowledge-base/studynote/02_operating_system/03_cpu_scheduling/213_race_condition/))이 제거된다.
> 3. 에지 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)의 셋업/홀드 타임 제약은 메타스태빌리티(Metastability)를 방지하는 핵심 — 데이터가 에지 직전/직후 일정 시간 동안 안정되어야 [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)이 확정적으로 동작한다.

---

## Ⅰ. 레벨 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) vs 에지 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">래치 (Level Trigger):</div>
<div class="kb-diagram-note">클럭 HIGH 동안 데이터 투명(Transparent)</div>
<div class="kb-diagram-note">클럭 LOW 동안 데이터 잠금(Latched)</div>
<div class="kb-diagram-note">문제: 클럭 HIGH 동안 입력 변화 → 출력 연속 변화</div>
<div class="kb-diagram-note">→ 레이스 컨디션 (Race Condition) 위험</div>
<div class="kb-diagram-note">D Latch 동작:</div>
<div class="kb-diagram-note">CLK=1: Q = D (투명, 따라감)</div>
<div class="kb-diagram-note">CLK=0: Q = 이전값 (잠금)</div>
<div class="kb-diagram-note">에지 트리거 플립플롭 (D Flip-Flop):</div>
<div class="kb-diagram-note">클럭 에지 순간에만 데이터 포착</div>
<div class="kb-diagram-note">클럭 에지 이후: 출력 유지</div>
<div class="kb-diagram-note">Rising Edge D Flip-Flop:</div>
<div class="kb-diagram-note">CLK: 0→1 전환 순간 → Q = D 포착</div>
<div class="kb-diagram-note">이후: Q 유지 (D 변해도 Q 불변)</div>
<div class="kb-diagram-note">비교:</div>
<div class="kb-diagram-note">래치 에지 트리거 FF</div>
<div class="kb-diagram-note">데이터 포착 CLK HIGH 전체 CLK 에지 순간만</div>
<div class="kb-diagram-note">레이스 컨디션 위험 없음</div>
<div class="kb-diagram-note">복잡도 낮음 높음</div>
<div class="kb-diagram-note">사용처 CPU 내부 일부 대부분 순차 로직</div>
<div class="kb-diagram-note">현대 디지털 회로:</div>
<div class="kb-diagram-note">대부분 에지 트리거 플립플롭 사용</div>
<div class="kb-diagram-note">FPGA, ASIC: D 플립플롭이 기본 빌딩 블록</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 레벨 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)는 열린 문(CLK HIGH면 누구나 입장), 에지 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)는 회전문(클릭 순간에만 한 명 통과). 회전문이 더 안전!

---

## Ⅱ. D [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/) 내부 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">Rising Edge D Flip-Flop:</div>
<div class="kb-diagram-note">마스터-슬레이브 구조로 구현</div>
<div class="kb-diagram-note">마스터-슬레이브 D Flip-Flop:</div>
<div class="kb-diagram-note">CLK=0: 마스터 래치 투명 (D 포착)</div>
<div class="kb-diagram-note">슬레이브 래치 잠금</div>
<div class="kb-diagram-note">CLK=1: 마스터 래치 잠금</div>
<div class="kb-diagram-note">슬레이브 래치 투명 (마스터 값 출력)</div>
<div class="kb-diagram-note">효과:</div>
<div class="kb-diagram-note">CLK 상승 에지에서 D → Q 전달</div>
<div class="kb-diagram-note">나머지 시간: Q 유지</div>
<div class="kb-diagram-note">게이트 수준 구현:</div>
<div class="kb-diagram-note">NOT 게이트 2개 + NAND/NOR 조합</div>
<div class="kb-diagram-note">최소 6개 NAND 게이트</div>
<div class="kb-diagram-note">비동기 리셋/프리셋:</div>
<div class="kb-diagram-note">RESET: Q를 즉시 0으로</div>
<div class="kb-diagram-note">PRESET: Q를 즉시 1으로</div>
<div class="kb-diagram-note">(CLK과 무관하게 즉시 동작)</div>
<div class="kb-diagram-note">사용: 전원 인가 시 초기화</div>
<div class="kb-diagram-note">프리셋 우선 회로:</div>
<div class="kb-diagram-note">if (RESET=0): Q=0</div>
<div class="kb-diagram-note">elif (PRESET=0): Q=1</div>
<div class="kb-diagram-note">else: 에지 트리거 동작</div>
<div class="kb-diagram-note">타이밍 파라미터:</div>
<div class="kb-diagram-note">tsu (Setup Time): 에지 전 최소 안정 시간</div>
<div class="kb-diagram-note">th (Hold Time): 에지 후 최소 유지 시간</div>
<div class="kb-diagram-note">tpd (Propagation Delay): 에지 → Q 변화 시간</div>
<div class="kb-diagram-note">디지털 교과서 전형적 값:</div>
<div class="kb-diagram-note">tsu ≈ 0.1~0.5 ns</div>
<div class="kb-diagram-note">th ≈ 0.05~0.2 ns</div>
<div class="kb-diagram-note">tpd ≈ 0.2~1.0 ns</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 마스터-슬레이브는 이중 잠금 금고 — 바깥 금고(마스터)에 먼저 넣고, 클릭 후 안쪽 금고(슬레이브)로 이전. 한 번에 하나씩만 들어가요!

---

## Ⅲ. 메타스태빌리티



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">메타스태빌리티 (Metastability):</div>
<div class="kb-diagram-note">셋업/홀드 타임 위반 시 출력이</div>
<div class="kb-diagram-note">0도 1도 아닌 불확정 상태에 빠지는 현상</div>
<div class="kb-diagram-note">발생 조건:</div>
<div class="kb-diagram-note">데이터 변화와 클럭 에지가 너무 가까울 때</div>
<div class="kb-diagram-note">Safe: D 변화 tsu ── CLK에지</div>
<div class="kb-diagram-note">Unsafe: D 변화 tsu 위반 ─ CLK에지</div>
<div class="kb-diagram-note">메타스태빌리티 상태:</div>
<div class="kb-diagram-note">Q = 중간 전압 (예: 0.8V, 정상은 0 or 1.8V)</div>
<div class="kb-diagram-note">결과:</div>
<div class="kb-diagram-tree-item" style="--depth:1">다음 단계 회로가 0 또는 1로 잘못 해석</div>
<div class="kb-diagram-tree-item" style="--depth:1">불확정 상태가 수 나노초 지속 가능</div>
<div class="kb-diagram-tree-item" style="--depth:1">해결 안 되면 시스템 오동작</div>
<div class="kb-diagram-note">발생 빈도:</div>
<div class="kb-diagram-note">MTBF_meta = exp(C2 × T_resolution) / (C1 × f_clk × f_data)</div>
<div class="kb-diagram-note">→ T_resolution 증가 (더 기다림) → MTBF 지수 증가</div>
<div class="kb-diagram-note">CDC (Clock Domain Crossing)에서 흔함:</div>
<div class="kb-diagram-note">서로 다른 주파수 도메인 간 신호 전달</div>
<div class="kb-diagram-note">→ 수신 클럭과 데이터 타이밍 무관</div>
<div class="kb-diagram-note">메타스태빌리티 해결:</div>
<div class="kb-diagram-note">1. 2단계 동기화 플립플롭 (2-FF Synchronizer):</div>
<div class="kb-diagram-note">FF1 → FF2 → 다음 회로</div>
<div class="kb-diagram-note">FF1에서 메타 발생 → FF2까지 해소 시간 확보</div>
<div class="kb-diagram-note">2. FIFO (비동기 FIFO):</div>
<div class="kb-diagram-note">두 클럭 도메인 사이 버퍼</div>
<div class="kb-diagram-note">그레이 코드 포인터로 메타 방지</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 메타스태빌리티는 동전이 서는 상태 — 던진 동전이 0(앞)도 1(뒤)도 아닌 세워진 채로! 2단계 동기화는 동전이 쓰러질 때까지 기다리는 것!

---

## Ⅳ. FPGA와 에지 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">FPGA 내부 에지 트리거:</div>
<div class="kb-diagram-note">FPGA 기본 요소:</div>
<div class="kb-diagram-note">LUT (Look-Up Table): 조합 논리</div>
<div class="kb-diagram-note">FF (Flip-Flop): 순차 로직</div>
<div class="kb-diagram-note">각 LUT마다 D 플립플롭 내장</div>
<div class="kb-diagram-note">→ 설계자 선택적 활용</div>
<div class="kb-diagram-note">Verilog 에지 트리거:</div>
<div class="kb-diagram-note">// Rising Edge D Flip-Flop</div>
<div class="kb-diagram-note">always @(posedge clk) begin</div>
<div class="kb-diagram-note">q &lt;= d; // 비차단(non-blocking) 할당</div>
<div class="kb-diagram-note">end</div>
<div class="kb-diagram-note">// Async Reset</div>
<div class="kb-diagram-note">always @(posedge clk or negedge rst_n) begin</div>
<div class="kb-diagram-note">if (!rst_n)</div>
<div class="kb-diagram-note">q &lt;= 1'b0;</div>
<div class="kb-diagram-note">else</div>
<div class="kb-diagram-note">q &lt;= d;</div>
<div class="kb-diagram-note">end</div>
<div class="kb-diagram-note">글로벌 클럭 네트워크:</div>
<div class="kb-diagram-note">FPGA: 전용 글로벌 클럭 버퍼</div>
<div class="kb-diagram-note">저스큐(Low Skew) 클럭 분배</div>
<div class="kb-diagram-note">Xilinx: BUFG, BUFR, MMCM</div>
<div class="kb-diagram-note">Intel: GCLK, PLL</div>
<div class="kb-diagram-note">STA (Static Timing Analysis):</div>
<div class="kb-diagram-note">에지 트리거 타이밍 검증</div>
<div class="kb-diagram-note">모든 FF-to-FF 경로 셋업/홀드 확인</div>
<div class="kb-diagram-note">도구: Vivado Timing Analyzer, Quartus TimeQuest</div>
<div class="kb-diagram-note">WNS (Worst Negative Slack): 최악 타이밍 여유</div>
<div class="kb-diagram-note">WNS &gt; 0: 설계 통과</div>
<div class="kb-diagram-note">WNS &lt; 0: 타이밍 위반 → 수정 필요</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [FPGA](/knowledge-base/studynote/01_computer_architecture/15_advanced_topics/606_dynamic_partial_reconfiguration/) 에지 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)는 레고 블록 — D [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)(레고 블록)을 LUT과 조합해 원하는 순차 회로 구성. Verilog는 레고 조립 설명서!

---

## Ⅴ. 실무 시나리오 — [ASIC](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/070_asic/) 타이밍 클로저



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">고속 ASIC 에지 트리거 타이밍 설계:</div>
<div class="kb-diagram-note">설계 사양:</div>
<div class="kb-diagram-note">ARM Cortex-A55 클론 설계</div>
<div class="kb-diagram-note">목표 주파수: 2 GHz</div>
<div class="kb-diagram-note">공정: TSMC 7nm</div>
<div class="kb-diagram-note">tclk = 0.5 ns 안에 모든 타이밍 맞춰야</div>
<div class="kb-diagram-note">타이밍 제약 설정:</div>
<div class="kb-diagram-note"># Synopsys Design Constraints</div>
<div class="kb-diagram-row"><div class="kb-diagram-note">create_clock -period 0.5</div><div class="kb-diagram-node">get_ports clk</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">set_input_delay 0.1 -clock clk</div><div class="kb-diagram-node">all_inputs</div></div>
<div class="kb-diagram-row"><div class="kb-diagram-note">set_output_delay 0.1 -clock clk</div><div class="kb-diagram-node">all_outputs</div></div>
<div class="kb-diagram-note">Critical Path 분석:</div>
<div class="kb-diagram-note">FF1 → Adder(32bit) → Comparator → FF2</div>
<div class="kb-diagram-note">타이밍 분해:</div>
<div class="kb-diagram-note">tclk-q (FF1): 0.05 ns</div>
<div class="kb-diagram-note">조합 논리: 0.38 ns ← 병목</div>
<div class="kb-diagram-note">배선 지연: 0.02 ns</div>
<div class="kb-diagram-note">tsu (FF2): 0.03 ns</div>
<div class="kb-diagram-note">총합: 0.48 ns &lt; 0.5 ns ✓</div>
<div class="kb-diagram-note">WNS = 0.5 - 0.48 = 0.02 ns (아슬아슬!)</div>
<div class="kb-diagram-note">최적화 기법:</div>
<div class="kb-diagram-note">파이프라인 삽입:</div>
<div class="kb-diagram-note">긴 조합 논리 → 중간에 FF 삽입</div>
<div class="kb-diagram-note">→ 각 스테이지 짧아짐 → 주파수 증가</div>
<div class="kb-diagram-note">로직 리타이밍 (Retiming):</div>
<div class="kb-diagram-note">FF 위치 이동으로 타이밍 균등화</div>
<div class="kb-diagram-note">클럭 스큐 활용 (Useful Skew):</div>
<div class="kb-diagram-note">의도적 스큐로 Critical Path 여유 증가</div>
<div class="kb-diagram-note">최종 검증:</div>
<div class="kb-diagram-note">코너 분석: SS(slow-slow), FF(fast-fast), TT</div>
<div class="kb-diagram-note">온도: -40°C ~ 125°C</div>
<div class="kb-diagram-note">전압: VDD ±10%</div>
<div class="kb-diagram-note">모든 코너에서 WNS &gt; 0 → 테이프아웃</div>
</div>
</div>



> 📢 **섹션 요약 비유**: [ASIC](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/070_asic/) 타이밍 클로저는 100m 허들 — 0.5ns([클럭 주기](/knowledge-base/studynote/01_computer_architecture/03_architecture_basics_performance/133_clock_cycle_time/))라는 시간 안에 모든 신호가 FF에서 다음 FF까지 전달. 허들([지연](/knowledge-base/studynote/03_network/01_data_communication/015_지연_데이터_관점/)) 하나라도 높으면 탈락(타이밍 위반)!

---

## 📌 관련 개념 맵

```
에지 트리거 (Edge Trigger)
+-- 비교
|   +-- 레벨 트리거 (래치)
|   +-- 에지 트리거 (D FF)
+-- 내부 구조
|   +-- 마스터-슬레이브 래치
|   +-- 비동기 Reset/Preset
+-- 타이밍
|   +-- 셋업/홀드 타임
|   +-- 메타스태빌리티
|   +-- CDC 동기화
+-- 구현
    +-- FPGA (LUT+FF)
    +-- ASIC (STA, 타이밍 클로저)
    +-- Verilog always @(posedge)
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[초기 플립플롭 (1940s~50s)]
SR 래치, JK 플립플롭
레벨 트리거 주류
      |
      v
[CMOS D 플립플롭 (1970s~)]
마스터-슬레이브 에지 트리거
저전력, 고속
      |
      v
[VLSI / FPGA 시대 (1980s~)]
에지 트리거 표준화
STA(정적 타이밍 분석) 필수화
      |
      v
[현재: 초미세 공정]
7nm/3nm 에지 트리거
Pulse Latch (하이브리드)
      |
      v
[미래: 양자/아날로그]
래치 기반 회로 재조명
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 에지 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/)는 정확한 순간 포착 — 클럭이 0→1 바뀌는 그 순간(에지)에만 데이터를 기억해요. 항상 열려있는 문(래치)보다 훨씬 안전!
2. 메타스태빌리티는 동전이 서는 것 — 너무 바쁠 때 데이터가 들어오면(셋업 위반) [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/)이 0도 1도 아닌 중간에 멈출 수 있어요!
3. FPGA는 D [플립플롭](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/051_flip_flop/) 레고 — Verilog로 "posedge clk"라고 쓰면 에지 [트리거](/knowledge-base/studynote/05_database/04_transactions_concurrency/507_acid_properties/) FF 자동 [생성](/knowledge-base/studynote/02_operating_system/02_process_thread/087_process_state_transition/). LUT+FF 조합이 디지털 회로의 기본!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 46 / 803

← **이전**: [045. 클럭 — Clock Signal](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/045_clock/)
**다음**: [047. 레벨 트리거 — Level Trigger](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/047_level_trigger/) →

---
