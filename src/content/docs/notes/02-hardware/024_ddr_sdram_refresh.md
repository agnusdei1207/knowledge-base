---
sidebar:
  order: 24
  label: "024. DDR SDRAM과 리프레시 방식 (DDR SDRAM Refresh)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "DDR SDRAM과 리프레시 방식 (DDR SDRAM Refresh)"
date: "2026-08-13T11:46:28+09:00"
tags:
  - "notes-hardware"
weight: 24
extra:
  question_no: "024"
  source_status: "기출"
  source_history: "129회"
  priority: 50
  priority_note: "뱅크 병렬성•리프레시 차단 비교"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **DDR SDRAM (Double Data Rate Synchronous DRAM)**: 시스템 버스 클록의 상승 엣지(Rising Edge)와 하강 엣지(Falling Edge) 모두에서 데이터를 전송(Double Data Rate)하여 단일 엣지 대비 데이터 전송율을 2배 높인 동기식 DRAM 규격.
- **DRAM (Dynamic Random-Access Memory)**: 1T1C 커패시터 전하 저장 방식을 사용하여 시간이 지남에 따라 전하 방전이 일어나므로 주기적인 리프레시(Refresh) 연산이 강제되는 메모리.
- **전하 누설 (Charge Leakage)**: 커패시터 하단 및 트랜지스터 서브스레시홀드 구간을 통해 DRAM 1비트 전하가 서서히 방전되어 데이터 1이 0으로 변질되는 물리적 현상.

</details>

- 정의/개념: 클록의 상승/하강 양 엣지에서 데이터를 전송(Double Data Rate)하며, 1T1C 커패시터의 **전하 누설**을 차단하기 위해 **tREFI/tRFC** 타이밍 규격 기반의 주기적 전하 복원을 구동하는 **DDR SDRAM** 메인 메모리 기술.
- 배경/필요성: 단일 엣지(SDR) 전송 한계를 극복하고 CPU와의 데이터 전송 대역폭을 극대화함과 동시에, 초미세 공정화에 따라 급증한 전하 누설 문제를 하드웨어 리프레시 타이밍 통제로 완벽 수습할 필요성 대두.

#### 한줄 요약
- 양 엣지(Double Edge) 데이터 전송과 뱅크 병렬성을 결합하고, tREFI 타이밍 규격 기반의 전하 리프레시를 구동하는 메인 메모리 기술.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **양 엣지 전송(Double-Edge Transfer)**: 1개 클록 주파수 주기 내에서 0->1 상승 엣지와 1->0 하강 엣지 2번 모두에 데이터를 싣는 버스 동기화 기술.
- **뱅크 병렬성(Bank-Level Parallelism, BLP)**: 단일 칩 내부를 8개~32개의 독립적인 뱅크(Bank) 구조로 파티셔닝하여 뱅크 0의 Precharge 중 뱅크 1의 Read/Write를 동시 가동하는 아키텍처.
- **버스트 전송(Burst Transfer)**: 단 1회의 Column Read/Write 명령 발송으로 지정된 버스트 길이(BL4, BL8, BL16)만큼 연속 메모리 묶음 데이터를 1클록 연속 인출하는 기법.
- **리프레시(Refresh)**: DRAM 셀 커패시터 전하가 완전 소멸하기 전에 Sense Amplifier로 행을 읽어 1.0V/0.0V 전압으로 다시 강제 재충전해주는 행위.

</details>

- 클록의 **양 엣지 전송** 기술을 적용하여 SDR 대비 동일 버스 클록 주파수에서 2배의 전송 속도(MT/s) 달성.
- 다중 뱅크의 **뱅크 병렬성**과 **버스트 전송**으로 행•열 명령 지연을 일부 중첩.
- 매 64ms 시간 이내에 모든 행을 재충전해야 하는 **tREFI(Refresh Interval)** 및 **tRFC(Refresh Cycle Time)** 대기 시간 수반.

#### 한줄 요약
- Double-Edge clocking 및 Bank-Level Parallelism을 통한 고대역폭 인출 특성과 tREFI/tRFC 타이밍 제어 기반 전하 복원 특성을 지님.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **메모리 컨트롤러(Memory Controller)**: CPU 소켓 내에 배치되어 주소를 Channel, Rank, Bank, Row, Column 비트로 파싱하고 ACT, PRE, REF 명령 타이밍을 스케줄링하는 유닛.
- **DDR PHY(DDR Physical Layer)**: 컨트롤러 명령 신호를 수십 GHz 고주파 미세 아날로그 전기 신호로 구동 정밀 변환하는 물리 계층 IC 블록.
- **DQ / DQS**: 실제 8/16-bit 데이터 라인(DQ)과 데이터를 보정 래칭하기 위한 데이터 스트로브 동기 신호(DQS).
- **행 버퍼(Row Buffer)**: 뱅크 내부에서 ACT 명령 구동 시 선택된 Row 행 전체(8KB)의 전하를 읽어온 후 래칭 보관하는 SRAM 성격의 고속 버퍼.
- **리프레시 카운터(Refresh Counter)**: 매 tREFI 주기마다 리프레시를 실행할 DRAM 칩 내부의 Row 주소를 0번부터 순차적으로 올리는 칩 내장 카운터.

- **자동 재생(Auto Refresh, CBR)**: DRAM 컨트롤러가 주기적으로 명령을 내려 메모리 셀 커패시터의 전하 누설을 방지하고 데이터를 보존하는 동작.
</details>

```text
[ DDR SDRAM Interface & Controller Architecture ]
┌───────────────────────────────────────────────────────────┐
│ Memory Controller (Address Scheduler : Act, Read, Ref)    │
│  └─ Command Scheduler & Refresh Queue (tREFI Timer)       │
├───────────────────────────────────────────────────────────┤
│ DDR PHY (Physical I/O Layer : DQ / DQS Signal Training)   │
├───────────────────────────────────────────────────────────┤
│ DRAM Chip Array (Multi-Bank Group)                        │
│  ├─ Bank 0 ~ Bank N (Row Buffer + Sense Amplifiers)       │
│  └─ Internal Refresh Counter (Row Address Increment)      │
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 책임 |
|:---|:---|
| 메모리 컨트롤러 | **주소 매핑•명령•Refresh** 스케줄링 |
| DDR PHY | **DQ•DQS 타이밍•신호 무결성** 제어 |
| 행 버퍼 | 활성 행의 **감지•복원•열 접근** 제공 |
| 리프레시 카운터 | 다음 **Refresh 대상 행** 선택 |

#### 한줄 요약
- Memory Controller, DDR PHY(DQ/DQS Training), Row Buffer 및 Internal Refresh Counter가 연동 구동됨.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **행 활성(Activate, ACT)**: 해당 Bank의 특정 Row를 열어 행 버퍼로 로드시키는 명령.
- **프리차지(Precharge, PRE)**: 오픈된 Row를 닫고 비트라인을 VCC/2 수준으로 초기화하는 명령.
- **리프레시 간격(Refresh Interval, tREFI)**: 64ms 주기 동안 전체 행을 나누어 전하 충전하기 위해 발송되는 평균 리프레시 명령 간격 (일반적으로 7.8us).
- **리프레시 주기 시간(Refresh Cycle Time, tRFC)**: REF 명령 수신 시 칩 내부가 리프레시를 완료할 때까지 타 명령을 거부하고 전면 대기하는 시간 (예: 110~350ns).

</details>

```text
[ Memory Controller Command Execution Loop ]
                    │
                    ▼
          [ tREFI 기한 도래 여부 ]
          ├─ Timer Expired (기한 도래)
          │   REF 명령 발송
          │   tRFC 동안 대상 범위 접근 제한
          │   Refresh Counter 대상 행 충전
          │
          └─ Normal Operation (일반 접근)
              ACT ──> Row Buffer 로드
              CAS ──> DQ/DQS Burst Transfer
              PRE ──> Bitline Equalize
```

### 동작 원리

- **기한 확인**: **tREFI** 범위 안에서 REF 명령을 스케줄링함.
- **Refresh 수행**: 대상 행을 복원하고 **tRFC** 동안 관련 접근을 제한함.
- **일반 접근**: **ACT•CAS•PRE**로 행 활성, 열 전송, 비트라인 초기화 수행

#### 한줄 요약
- tREFI 기한 감시 후 REF 명령으로 tRFC 락업 전하 충전을 가동하며 일반 접근 시 ACT->CAS 버스트 전송->PRE를 수행함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **전체 뱅크 리프레시(All-Bank Refresh / REFab)**: 단일 REF 명령으로 랭크 내의 모든 뱅크를 일제히 락업시키고 리프레시를 수행하는 방식.
- **뱅크별 리프레시(Per-Bank Refresh / REFpb)**: 특정 1개 뱅크만 락업하여 리프레시하고, 타 뱅크는 정상적인 Read/Write 연산을 병렬 허용하는 LPDDR/DDR5 방식.
- **자체 리프레시(Self Refresh / SR)**: 시스템이 C-State/S3 절전 대기 모드 진입 시 외부 컨트롤러 클록을 끄고 DRAM 칩 내부 온-칩 타이머로 리프레시를 자율 수행하는 상태.

</details>

| 리프레시 방식 | All-Bank Refresh (REFab) | Per-Bank Refresh (REFpb) | Self Refresh (SR) |
|:---|:---|:---|:---|
| 작동 메커니즘 | 랭크 내 모든 뱅크 일제히 락업 리프레시 | 1개 뱅크만 선택 락업, 타 뱅크 가동 | 외부 클록 차단 후 On-chip 타이머 자율 충전 |
| 버스 대기 영향 | **tRFC 동안 랭크 전면 접근 불가** (Tail Latency) | **타 뱅크 정상 접근 가능** (지연 최소화) | 외부 메모리 버스 접근 전면 차단 |
| 적용 아키텍처 | DDR3, DDR4 표준 | LPDDR4, LPDDR5, DDR5 표준 | 모바일, 노트북 S3/Sleep 절전 모드 |
| 제어 복잡도 | 단순함 | 메모리 컨트롤러 스케줄러 복잡함 | DRAM 칩 내부 자체 전력 회로 복잡 |

#### 한줄 요약
- All-Bank(단순하나 랭크 전체 락업), Per-Bank(타 뱅크 억세스 허용으로 꼬리 지연 차단), Self Refresh(절전 모드 자율 유지)로 나뉨.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **꼬리 지연(Tail Latency / p99 Latency)**: 실시간 트랜잭션 요청이 하필 tRFC 리프레시 락업 주기와 겹쳐 응답 지연이 급증하는 99번째 백분위수 지연 현상.
- **로해머 (Rowhammer Attack)**: 특정 DRAM 행(Row)을 짧은 시간 내 수백만 번 집중 억세스(ACT/PRE)하여 인접 행 셀 커패시터 전하를 누설 강제 유출시켜 비트를 반전시키는 보안 공격.
- **TRR (Target Row Refresh)**: 로해머 공격을 방지하기 위해 집중 억세스되는 인접 행을 하드웨어적으로 감지하여 추가 리프레시를 강제 집행하는 방어 회로.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| All-Bank Refresh 시 tRFC 락업으로 인한 실시간 **꼬리 지연** 증대 | DDR5 / LPDDR5 **Per-Bank Refresh (REFpb)** 및 뱅크 스케줄링 적용 | 억세스 차단 시간 분산 및 p99 지연 대폭 감소 |
| 특정 Row 집중 억세스로 인접 비트를 파괴하는 **로해머** 보안 취약점 | 컨트롤러/DRAM 내장 **TRR(Target Row Refresh)** 및 RFM 연동 | 인접 행 전하 강제 충전으로 비트 반전 공격 차단 |
| 고온 환경(85℃ 이상) 작동 시 DRAM 전하 누설 속도 급증으로 데이터 파손 | 온도 센서 연동 2x Refresh (tREFI 간격 7.8us -> 3.9us 단축) | 고온 환경 데이터 보존성 완벽 유지 |
| 초고속 전송(6400+ MT/s) 시 DQ/DQS 신호 스큐로 데이터 오류 | 부팅 시 **PHY Write/Read Training** 및 DQS Centering 수행 | 데이터 샘플링 마진 확보 및 신호 무결성 유지 |

#### 한줄 요약
- REFpb(Tail Latency 차단), TRR 연동(Rowhammer 방어), Temperature-based 2x Refresh 및 PHY Training을 구동함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **DDR/Refresh 최적화 기준(DDR Refresh Optimization Criteria)**: 대상 시스템의 리얼타임 응답 목표(p99 Latency), 동작 온도 범위, 보안 위협(Rowhammer)을 평가하여 REFpb 및 TRR 타이밍 파라미터를 확정하는 프레임워크.

</details>

- p99가 중요하면 **Per-Bank Refresh**, 고온•Rowhammer에는 **가변 Refresh•TRR** 적용.

#### 한줄 요약
- 대역폭•Refresh 정지•보안 요구로 DDR 세대와 Refresh 방식을 결정함.
