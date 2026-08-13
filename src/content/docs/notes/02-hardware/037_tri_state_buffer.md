---
sidebar:
  order: 37
  label: "037. 3-상태 버퍼•트라이스테이트 (Tri-State Buffer)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "3-상태 버퍼•트라이스테이트 (Tri-State Buffer)"
date: "2026-08-13T11:55:49+09:00"
tags:
  - "notes-hardware"
weight: 37
extra:
  question_no: "037"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "외부 버스 공유와 경합 방지의 기출 주제"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **3-상태 버퍼 (Tri-State Buffer / Three-State Buffer)**: 출력을 일반적인 2진 논리 상태인 '0'(Low) 및 '1'(High) 이외에, 전기적으로 신호선과의 연결을 완전히 절연시키는 고임피던스(High-Impedance, High-Z) 상태를 포함하여 3가지 상태로 출력할 수 있는 디지털 논리 게이트 회로.
- **고임피던스(High-Impedance, High-Z)**: 출력단이 비활성화되어 공유선에 능동적인 0•1 전압을 구동하지 않는 상태.
- **버스 경합 (Bus Contention)**: 2개 이상의 출력 드라이버가 동일한 신호선에 '0'과 '1'을 동시에 출력하여 단락 전류(Short-Circuit Current)가 흐르고 기계적 IC 파손이 일어나는 현상.

</details>

- 정의/개념: 출력 활성화 신호(Output Enable, OE) 제어를 통해 논리 '0', 논리 '1' 및 전기적 절연 상태인 **고임피던스(High-Z)** 3가지 상태를 선택 출력하는 **3-상태 버퍼(Tri-State Buffer)** 회로.
- 배경/필요성: 동일한 물리 주소/데이터 버스선에 다수의 IC 칩 출력이 물리적으로 병렬 연결된 공유 버스 아키텍처에서, 비선택 칩들의 전기적 분리를 통해 **버스 경합(Bus Contention)** 및 단락 파손을 방지하기 위해 사용.

#### 한줄 요약
- OE(Output Enable) 신호에 따라 0, 1 및 High-Z(전기적 절연) 3개 상태를 출력하여 공유 버스 상의 칩 간 단락 및 신호 충돌을 원천 차단하는 회로.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **출력 활성화 신호 (Output Enable, OE / active-low OE#)**: 3-상태 버퍼의 드라이버를 켜서 0/1 신호를 버스로 쏘아 보낼지, 아니면 High-Z 상태로 숨길지를 제어하는 1-bit 제어 핀.
- **OE 상호 배타 (OE Mutual Exclusion)**: 공유 버스에 꽂힌 N개의 3-상태 버퍼 중 특정 시점에 단 1개의 OE 신호만 Active(1 또는 0)가 되도록 디코더 하드웨어를 강제하는 제어 규칙.
- **부동 현상 (Floating State)**: 버스 상의 모든 3-상태 버퍼가 High-Z 상태로 놓여, 버스 전압이 0V도 5V도 아닌 불안정한 공중 전위 상태(Uncertain Logic)로 떠돌아다니는 현상.
- **턴어라운드 시간 (Bus Turnaround Time)**: 3-상태 버퍼가 Write 구동에서 High-Z로 완전히 빠져나간 뒤 타 칩이 Read 구동을 시작할 때까지의 안전 갭 시간.

</details>

- 비선택 장치의 드라이버를 **고임피던스(High-Z)** 상태로 전환시켜 공유 버스 선상에서 전기적으로 완전 유연하게 분리.
- 버스 경합을 막기 위하여 컨트롤러 단에서 **OE 상호 배타(OE Mutual Exclusion)** 조건 및 충분한 **턴어라운드 시간(Turnaround Time)** 보장 필수.
- 버스 상의 모든 출력이 High-Z가 되는 **부동 현상(Floating)** 시의 노이즈 취약점을 막기 위해 풀업(Pull-Up) / 풀다운(Pull-Down) 바이어스 저항 결합.

#### 한줄 요약
- High-Z 전기적 절연 기능 제공, OE 상호 배타 제어 수반 및 Floating 방지용 Pull-up/down 바이어스 결합 특성을 지님.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Pass Transistor (PMOS/NMOS)**: 3-상태 버퍼의 최종 출력을 담당하며, OE 신호가 0(Disable)일 때 두 트랜지스터가 모두 켜지지 않아 High-Z를 형성하는 CMOS 회로 소자.
- **바이어스 저항 (Pull-Up / Pull-Down Resistor)**: 버스가 무구동(High-Z) 상태일 때 전압을 VCC(1) 또는 GND(0)로 끌어당겨 정해진 논리 상태를 고정해 주는 바이어스 저항.
- **버스 홀드 (Bus Hold Cell)**: 약한 래치(Weak Latch) 회로를 버스 핀에 달아, High-Z 상태에서도 가장 최근에 직전 버스가 가졌던 0 또는 1 논리 전압을 그대로 유지시켜 전력 소모를 억제하는 회로.

</details>

```text
[ Tri-State Buffer CMOS Logic & Shared Bus ]
               VCC
                │
            ┌───┴───┐
     Data───┤ PMOS  │ (Turn OFF when OE disabled)
            └───┬───┐
                ├───┼─── Output ──> [ Shared Bus Line ] ──┐
            ┌───┴───┐                                      │
     Data───┤ NMOS  │ (Turn OFF when OE disabled)          │
            └───┬───┘                             ┌────────┴────────┐
                │                                 │ Pull-Up Resistor│
               GND                                └────────┬────────┘
                                                           │
                                                          VCC (Prevents Floating)
```

| 구성요소 | 책임 |
|:---|:---|
| OE 핀 | **Drive•High-Z 상태** 선택 |
| CMOS 출력단 | 활성 시 **논리 0•1 전압** 구동 |
| Pull-Up•Down 저항 | 무구동 버스의 **기본 논리 상태** 설정 |
| Bus Hold Cell | 약한 피드백으로 **직전 버스 상태** 유지 |

#### 한줄 요약
- OE Control Pin, CMOS Push-Pull Output Stage, Pull-Up/Down Bias Resistor 및 Bus Hold Cell로 구동됨.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **순간 단락 (Pass-Through Short)**: 3-상태 버퍼 A가 High-Z로 빠져나오기 전에 버퍼 B가 켜져 순간적으로 VCC와 GND가 직통 연결되는 과도 단락 현상.

</details>

```text
[ Shared Memory DQ Bus Write/Read Transition Sequence ]
                         │
                         ▼
        [ 1. Host Memory Controller Assert Write OE = 1 ]
                         │
        [ Host Drives Write Data '0' / '1' on Shared DQ Bus ]
                         │
                         ▼
        [ 2. Host Write Complete ──> Assert Host OE = 0 (High-Z State) ]
                         │
                         ▼
        [ 3. Wait Bus Turnaround Time (tTA) ] (Both Drivers High-Z)
                         │
                         ▼
        [ 4. Memory Device Assert Read OE = 1 ]
                         │
        [ Memory Drives Read Data '0' / '1' on Shared DQ Bus to Host ]
```

### 동작 원리

1. **쓰기 구동**: 호스트 컨트롤러가 쓰기 OE=1을 출력하여 공유 **DQ 데이터 버스** 상에 데이터를 구동함.
2. **High-Z 전환**: 쓰기 완결 시 호스트는 즉시 자신의 OE=0으로 스위칭하여 출력을 **고임피던스(High-Z)**로 빠져나오게 함.
3. **턴어라운드 대기**: **순간 단락(Pass-Through Short)** 방지를 위해 지정된 버스 **턴어라운드 시간(tTA)** 동안 버스를 무구동 대기함.
4. **읽기 구동**: 메모리 칩이 안전하게 자신의 읽기 OE=1을 활성화하여 읽기 데이터를 호스트로 반환함.

#### 한줄 요약
- Host Write OE=1 -> Host Write OE=0 (High-Z) -> Bus Turnaround Wait (tTA) -> Memory Read OE=1 순으로 제어함.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **멀티플렉서 (Multiplexer, MUX)**: 3-상태 버퍼를 쓰지 않고, 앤드-오어(AND-OR) 조합 논리 회로를 이용하여 여러 입력 중 1개를 선택 출력하는 내부 선택기.
- **오픈 드레인 (Open-Drain)**: 논리 0만 강하게 끌어내리고 1은 풀업 저항에 의존하여, 다수 출력선을 그냥 묶어 앤드 연산(Wired-AND)을 만드는 회로 (I2C, Interrupt Line).

</details>

| 비교 항목 | 3-상태 버퍼 (Tri-State Buffer) | 멀티플렉서 (Multiplexer, MUX) | 오픈 드레인 (Open-Drain) |
|:---|:---|:---|:---|
| **출력 상태** | **0, 1, High-Z (3가지)** | 0, 1 (2가지) | **0, High-Z (Wired-AND)** |
| **적용 영역** | **칩 외부 양방향 공유 버스** | **칩 내부(SoC) 신호 선택** | **공유 제어선 (I2C, IRQ Line)** |
| **하드웨어 구현** | 핀 수 절감 (양방향 핀 공유) | MUX 게이트 면적 증가 | 외부 풀업 저항 필수 수반 |
| **충돌 위험**| OE 겹침 시 구동 충돌 | 선택 신호 오류 시 논리 오동작 | Low 동시 구동은 전기적으로 허용 |
| **억세스 속도** | 초고속 (양방향 직접 구동) | 매우 빠름 | 상대적 느림 (풀업 저항 R-C 지연) |

#### 한줄 요약
- 3-상태 버퍼는 칩 외부 양방향 버스의 핀 수 절감에 우수하고, MUX는 칩 내부 논리 단락 위험 제거에 우수하며, 오픈드레인은 Wired-AND 핀 공유에 우수함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **논리 합성 (Logic Synthesis)**: Verilog/VHDL RTL 코드를 실리콘 게이트로 변환하는 도구로, 현대 ASIC 도구는 칩 내부 3-상태 버퍼 사용을 금지하고 MUX 구조로 자동 대체함.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| OE 신호 스큐로 두 드라이버가 동시에 켜지는 **순간 단락** | 디코더 **OE 상호 배타** 및 **비중첩 Turnaround** 삽입 | 과도 전류와 출력 충돌 방지 |
| 버스 상의 모든 출력이 High-Z로 빠질 때 노이즈 유입 (**부동 현상**) | 버스 핀에 **Pull-Up 저항** 또는 **Bus Hold Cell** 탑재 | 부동 상태 노이즈 차단 및 스위칭 전력 소모 절감 |
| ASIC / FPGA 칩 내부에서 3-상태 버퍼 선언 시 합성 오류 발생 | **논리 합성(Synthesis)** 시 칩 내부는 **MUX**로 전환, 칩 외부 핀에만 적용 | ASIC DFT 테스트 검증성 및 내부 신호 안전성 확보 |
| 양방향 버스 고속 구동 시 신호 반사파(Reflection)로 인한 데이터 왜곡 | **On-Die Termination (ODT)** 임피던스 매칭 적용 | 고주파 핀 신호 무결성(Signal Integrity) 보장 |

#### 한줄 요약
- OE 상호 배타 디코더, Bus Hold/Pull-up 적용, ASIC 내부 MUX 대체 합성 및 ODT 임피던스 매칭 기법을 구동함.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **공유 버스 회로 선택 기준 (Shared Bus Circuit Decision Criteria)**: 대상 버스의 물리적 위치(On-Chip vs Off-Chip), 전송 방향성(Unidirectional vs Bidirectional), 핀 수 제약 및 신호 속도를 종합 분석하여 3-상태 버퍼, MUX, 오픈 드레인을 채택하는 프레임워크.

</details>

- 외부 병렬 양방향 버스는 **Tri-State**, 칩 내부 선택 경로는 **MUX** 적용.

#### 한줄 요약
- 물리 공유선과 합성 가능성을 기준으로 Tri-State•MUX•Open-Drain을 선택함.
