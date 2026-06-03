+++
title = "041. 멀티플렉서 (MUX, Multiplexer)"
date = 2026-03-20

[taxonomies]
tags = ["studynote-computer-architecture"]

[extra]
tags = ["studynote-computer-architecture"]
+++

> **핵심 인사이트**
> 1. 멀티플렉서([MUX](/knowledge-base/studynote/03_network/19_frequent_topics_terms/944_mux_demux_multiplexer_demultiplexer_circuit_sharing/))는 2ⁿ개의 입력 중 n비트 선택 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)([Select](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/) Line)에 의해 하나의 입력을 출력으로 선택하는 조합 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 회로로, 디지털 시스템에서 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) [라우팅](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/)([Routing](/knowledge-base/studynote/03_network/07_network_layer_routing/339_routing_overview_best_path_selection/))과 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/) 선택의 핵심 빌딩 블록이다.
> 2. MUX는 임의의 불 함수(Boolean Function)를 구현할 수 있는 범용 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 회로로, 2ⁿ⁺¹ -1개 입력 MUX로 n+1변수 함수를, 2ⁿ-1개 MUX로 n변수 함수를 진리표만으로 구현할 수 있다.
> 3. [디멀티플렉서](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/042_demultiplexer/)(DEMUX)는 MUX의 역()으로 하나의 입력을 선택 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)에 따라 2ⁿ개 출력 중 하나로 보내며, [MUX](/knowledge-base/studynote/03_network/19_frequent_topics_terms/944_mux_demux_multiplexer_demultiplexer_circuit_sharing/)-DEMUX 쌍은 [시분할 다중화](/knowledge-base/studynote/03_network/02_multiplexing_multiple_access/075_시분할_다중화_TDM/)(TDM) 통신의 핵심 하드웨어 구조다.

---

## Ⅰ. [MUX](/knowledge-base/studynote/03_network/19_frequent_topics_terms/944_mux_demux_multiplexer_demultiplexer_circuit_sharing/) 기본 구조

```
4:1 MUX (2비트 선택):

입력: I0, I1, I2, I3 (4개)
선택: S1, S0 (2비트)
출력: Y (1개)

진리표:
S1 S0 | Y
0 0 | I0
0 1 | I1
1 0 | I2
1 1 | I3

불 식:
Y = S1'S0'·I0 + S1'S0·I1 + S1S0'·I2 + S1S0·I3

게이트 구현:
4개의 AND 게이트 + 1개의 OR 게이트
각 AND: (선택 비트 조합) AND (입력)
OR: 4개의 AND 결과 합산

일반화: 2ⁿ:1 MUX = n비트 선택 신호
```

> 📢 **섹션 요약 비유**: MUX는 TV 리모컨 채널 선택 — 여러 방송 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/) 중 버튼([Select](/knowledge-base/studynote/05_database/04_transactions_concurrency/520_select/)) 누른 하나만 화면(출력)에 표시.

---

## Ⅱ. MUX로 불 함수 구현



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">MUX를 이용한 범용 논리 구현:</div>
<div class="kb-diagram-note">방법 1: 진리표 직접 매핑 (2ⁿ:1 MUX)</div>
<div class="kb-diagram-note">n변수 함수 -&gt; 2ⁿ:1 MUX</div>
<div class="kb-diagram-note">입력에 0/1 연결, 선택 신호 = 변수</div>
<div class="kb-diagram-note">예: F(A,B) = AB + A'B' 구현 (2변수)</div>
<div class="kb-diagram-note">A, B -&gt; 선택 신호 S1=A, S0=B</div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">A B</div><div class="kb-diagram-cell">F</div><div class="kb-diagram-cell">MUX 입력</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">0 0</div><div class="kb-diagram-cell">1</div><div class="kb-diagram-cell">I0 = 1</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">0 1</div><div class="kb-diagram-cell">0</div><div class="kb-diagram-cell">I1 = 0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1 0</div><div class="kb-diagram-cell">0</div><div class="kb-diagram-cell">I2 = 0</div></div>
<div class="kb-diagram-row kb-diagram-grid-row"><div class="kb-diagram-cell">1 1</div><div class="kb-diagram-cell">1</div><div class="kb-diagram-cell">I3 = 1</div></div>
<div class="kb-diagram-note">방법 2: 절반 크기 MUX 활용 (2ⁿ⁻¹:1 MUX)</div>
<div class="kb-diagram-note">마지막 변수를 MUX 입력으로 활용</div>
<div class="kb-diagram-note">n변수 함수 -&gt; 2ⁿ⁻¹:1 MUX</div>
<div class="kb-diagram-note">예: F(A,B,C) -&gt; 4:1 MUX + C 활용</div>
</div>
</div>



> 📢 **섹션 요약 비유**: MUX로 [논리](/knowledge-base/studynote/09_security/04_endpoint_security/369_logic_bomb/) 함수 구현은 레고 범용 블록 — 진리표를 [MUX](/knowledge-base/studynote/03_network/19_frequent_topics_terms/944_mux_demux_multiplexer_demultiplexer_circuit_sharing/) 입력에 그대로 꽂아서 어떤 함수도 만들 수 있다.

---

## Ⅲ. [디멀티플렉서](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/042_demultiplexer/) (DEMUX)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">DEMUX (Demultiplexer):</div>
<div class="kb-diagram-note">하나의 입력 -&gt; 선택 신호에 따라 2ⁿ개 출력 중 하나로</div>
<div class="kb-diagram-note">1:4 DEMUX:</div>
<div class="kb-diagram-note">입력: D (1개)</div>
<div class="kb-diagram-note">선택: S1, S0 (2비트)</div>
<div class="kb-diagram-note">출력: Y0, Y1, Y2, Y3 (4개)</div>
<div class="kb-diagram-note">동작:</div>
<div class="kb-diagram-note">S1=0, S0=0: Y0 = D, Y1=Y2=Y3=0</div>
<div class="kb-diagram-note">S1=0, S0=1: Y1 = D, Y0=Y2=Y3=0</div>
<div class="kb-diagram-note">S1=1, S0=0: Y2 = D, Y0=Y1=Y3=0</div>
<div class="kb-diagram-note">S1=1, S0=1: Y3 = D, Y0=Y1=Y2=0</div>
<div class="kb-diagram-note">MUX-DEMUX 쌍:</div>
<div class="kb-diagram-note">송신측: DEMUX - 여러 데이터를 하나 선로에 다중화</div>
<div class="kb-diagram-note">수신측: MUX - 하나 선로에서 해당 데이터 선택</div>
<div class="kb-diagram-note">데이터1 - -&gt; 데이터1</div>
<div class="kb-diagram-note">데이터2 - DEMUX ─선로─ MUX -&gt; 데이터2</div>
<div class="kb-diagram-note">데이터3 - -&gt; 데이터3</div>
<div class="kb-diagram-note">TDM (Time Division Multiplexing) 구현</div>
</div>
</div>



> 📢 **섹션 요약 비유**: DEMUX는 우체국 배달 시스템 — 중앙 우체국(입력)에서 받은 우편을 각 가정(출력)에 주소(선택 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/))에 맞게 배달.

---

## Ⅳ. [MUX](/knowledge-base/studynote/03_network/19_frequent_topics_terms/944_mux_demux_multiplexer_demultiplexer_circuit_sharing/) 계층화와 [버스](/knowledge-base/studynote/01_computer_architecture/09_system_bus_interconnects/344_bus/) 구조



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">대형 MUX 구성:</div>
<div class="kb-diagram-note">계층 MUX (Hierarchical MUX):</div>
<div class="kb-diagram-note">16:1 MUX = 4개의 4:1 MUX + 1개의 4:1 MUX</div>
<div class="kb-diagram-note">2단계로 구현 (게이트 수 절약)</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">4:1</div><div class="kb-diagram-node">4:1</div></div>
<div class="kb-diagram-note">I0~I3 ─</div>
<div class="kb-diagram-row"><div class="kb-diagram-node">4:1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-node">4:1</div><div class="kb-diagram-connector">→</div><div class="kb-diagram-note">Y</div></div>
<div class="kb-diagram-note">I4~I7 ─</div>
<div class="kb-diagram-note">...</div>
<div class="kb-diagram-note">버스 선택 (Bus Multiplexing):</div>
<div class="kb-diagram-note">8비트 데이터 버스 선택:</div>
<div class="kb-diagram-note">8개의 2:1 MUX 병렬 사용</div>
<div class="kb-diagram-note">선택 신호 1개로 8개 MUX 동시 제어</div>
<div class="kb-diagram-tree-item" style="--depth:0">2개의 8비트 버스 중 하나 선택</div>
<div class="kb-diagram-note">CPU 내부 MUX 사용:</div>
<div class="kb-diagram-note">ALU 입력 선택 (레지스터 A or B)</div>
<div class="kb-diagram-note">PC 증가값 선택 (PC+1 or 분기 주소)</div>
<div class="kb-diagram-note">데이터 경로(Datapath) 핵심 요소</div>
</div>
</div>



> 📢 **섹션 요약 비유**: 계층 MUX는 회사 조직 — 팀장이 팀원 중 하나를, 부장이 팀장 중 하나를 선택하는 계층 선택 구조.

---

## Ⅴ. 실무 시나리오 — CPU [데이터패스](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/205_datapath/)



<div class="kb-diagram" data-diagram="ascii-converted">
<div class="kb-diagram-flow">
<div class="kb-diagram-note">RISC CPU 데이터패스의 MUX:</div>
<div class="kb-diagram-note">ALU 입력 선택 MUX:</div>
<div class="kb-diagram-note">A 포트: 레지스터 파일 읽기값 (Rs)</div>
<div class="kb-diagram-note">B 포트 선택:</div>
<div class="kb-diagram-note">명령어 ADD R1, R2, R3: R3 선택</div>
<div class="kb-diagram-note">명령어 ADDI R1, R2, 10: 즉시값 10 선택</div>
<div class="kb-diagram-tree-item" style="--depth:0">2:1 MUX, 선택 = 명령어 타입 비트</div>
<div class="kb-diagram-note">PC 선택 MUX:</div>
<div class="kb-diagram-note">입력0: PC + 4 (순차 실행)</div>
<div class="kb-diagram-note">입력1: 분기 목적지 주소</div>
<div class="kb-diagram-tree-item" style="--depth:0">2:1 MUX, 선택 = 조건 분기 성공 여부</div>
<div class="kb-diagram-note">메모리 데이터 MUX:</div>
<div class="kb-diagram-note">레지스터 쓰기 값 선택:</div>
<div class="kb-diagram-note">입력0: ALU 연산 결과</div>
<div class="kb-diagram-note">입력1: 메모리 로드 값</div>
<div class="kb-diagram-tree-item" style="--depth:0">2:1 MUX, 선택 = Load 명령어 여부</div>
<div class="kb-diagram-note">FPGA에서 MUX:</div>
<div class="kb-diagram-note">LUT (Look-Up Table) = 사실상 MUX 배열</div>
<div class="kb-diagram-note">Xilinx LUT6: 6비트 선택 -&gt; 64:1 MUX</div>
<div class="kb-diagram-note">모든 논리 함수 = LUT로 구현</div>
</div>
</div>



> 📢 **섹션 요약 비유**: CPU [데이터패스](/knowledge-base/studynote/01_computer_architecture/05_control_unit_pipelining/205_datapath/)의 MUX는 철도 분기기 — [명령어](/knowledge-base/studynote/01_computer_architecture/04_instruction_set_architecture/158_instruction/) 종류에 따라 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)가 올바른 경로([ALU](/knowledge-base/studynote/01_computer_architecture/02_data_representation_arithmetic/117_alu/) or 메모리)로 흐르도록 분기.

---

## 📌 관련 개념 맵

```
멀티플렉서 (MUX)
+-- 구조
| +-- 2ⁿ:1 MUX (n비트 선택)
| +-- 계층 MUX
+-- 역기능
| +-- DEMUX (디멀티플렉서)
+-- 응용
| +-- 불 함수 구현 (범용 논리)
| +-- 버스 선택 (Bus Multiplexing)
| +-- CPU 데이터패스
| +-- TDM 통신
+-- FPGA
+-- LUT = MUX 배열
```

---

## 📈 관련 키워드 및 발전 흐름도

```
[MUX 회로 이론 (1940s~)]
릴레이 기반 스위칭 회로
|
v
[TTL/CMOS MUX IC (1970s)]
74153, 74151 (4:1, 8:1 MUX) 표준 IC
|
v
[CPU 데이터패스 MUX (1980s~)]
단일칩 마이크로프로세서 핵심 구성
|
v
[FPGA LUT = MUX (1985~)]
LUT 기반 프로그래머블 논리
모든 함수 MUX 구조로 구현
|
v
[현재: 고속 직렬 MUX]
SerDes (직렬화/역직렬화)
수십 Gbps 광통신 채널 다중화
```

---

## 👶 어린이를 위한 3줄 비유 설명

1. 멀티플렉서는 여러 수도꼭지(입력) 중에서 손잡이(선택 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/))로 하나만 골라 물(출력)이 나오게 하는 분배기예요.
2. 4개 입력이 있으면 2비트 [신호](/knowledge-base/studynote/02_operating_system/02_process_thread/130_signal/)(00, 01, [10](/knowledge-base/studynote/02_operating_system/08_storage_and_io_systems/489_raid_10_hybrid/), [11](/knowledge-base/studynote/03_network/06_network_layer_ip/308_static_dynamic_nat_pat_port_address_translation/))로 어느 것을 선택할지 결정해요.
3. CPU 내부에도 수십 개의 MUX가 있어서 어떤 [데이터](/knowledge-base/studynote/05_database/01_db_architecture_relational/001_dikw_pyramid/)를 계산에 쓸지 매 순간 선택하고 있어요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 41 / 803

← **이전**: [040. 인코더 (Encoder)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/040_encoder/)
**다음**: [042. 디멀티플렉서 (Demultiplexer, DEMUX)](/knowledge-base/studynote/01_computer_architecture/01_basic_electronics_logic/042_demultiplexer/) →

---
