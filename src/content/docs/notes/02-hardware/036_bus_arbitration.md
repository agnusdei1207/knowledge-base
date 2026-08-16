---
sidebar:
  order: 36
  label: "036. 버스 중재 방식 (Bus Arbitration)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "버스 중재 방식 (Bus Arbitration)"
date: "2026-08-13T11:55:03+09:00"
tags:
  - "notes-hardware"
weight: 36
extra:
  question_no: "036"
  source_status: "기출"
  source_history: "128회, 137회"
  priority: 70
  priority_note: "공정성•지연 절충의 반복 기출 핵심 주제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **버스 중재 (Bus Arbitration)**: 복수의 버스 마스터(CPU, DMAC, GPU, PCIe Switch)가 하나의 공유 버스(Shared Bus) 사용권을 동시 요구할 때, 신호 충돌(Collision)을 방지하고 배타적 사용권(Grant)을 1개 마스터에 할당하는 하드웨어 제어 기법.
- **버스 마스터 (Bus Master)**: 시스템 버스 상에서 주소와 제어 신호를 구동하여 독립 트랜잭션(Read/Write)을 시작할 수 있는 능력을 가진 하드웨어 제어 장치.
- **배타적 소유권 (Exclusive Ownership)**: 공유 신호선 충돌 및 데이터 훼손을 방지하기 위해 1개 클록 타임 슬라이스 동안 단 1개 마스터 장치에만 버스 구동 권한을 인가하는 원칙.

</details>

- 정의/개념: 다중 버스 마스터 환경에서 버스 경합(Bus Contention) 발생 시, 설정된 중재 알고리즘에 의거하여 단 1개의 **버스 마스터**에만 **배타적 소유권**을 인가하는 **버스 중재** 기술.
- 배경/필요성: CPU, DMA 제어기, GPU 등 여러 마스터가 공유 주소/데이터 버스 신호선을 동시에 구동할 경우 전기적 신호 충돌(Collision) 및 데이터 파손이 발생하므로, 제어기를 통한 트래픽 중계 필수.

#### 한줄 요약
- 공유 버스 상의 신호 충돌을 방지하기 위해 중재 알고리즘을 가동하여 특정 1개 마스터 장치에 배타적 승인(Grant)을 부여하는 제어 메커니즘.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **요청 신호 (Bus Request, BREQ)**: 버스 마스터가 버스 사용권을 필요로 할 때 중재기로 발송하는 하드웨어 핀 신호.
- **승인 신호 (Bus Grant, BGRT)**: 중재기가 경합을 거쳐 특정 마스터로 사용권 인가를 통지하는 핀 신호.
- **에이징 (Aging)**: 라운드 로빈 및 우선순위 중재 시, 장기간 버스 사용을 획득하지 못한 저우선순위 마스터의 틱(Tick)을 감지하여 수용 우선순위를 올려주는 기아(Starvation) 방지 기술.
- **버스트 한도 (Burst Limit)**: 1개 마스터가 승인 신호를 받은 후 연속해서 제어권을 독점할 수 있는 최대 타임 슬라이스 또는 킬로바이트 한도.

</details>

- 버스 **요청 신호**와 **승인 신호**로 사용권 요청•인가 수행.
- 특정 마스터의 무한 버스 점유를 방지하기 위해 **버스트 한도** 및 **시간 할당량**을 적용.
- 저우선순위 장치가 영구히 버스 사용을 획득하지 못하는 기아 현상 방지를 위한 **에이징** 메커니즘 내장.

#### 한줄 요약
- BREQ/BGRT 신호 교환 기반의 빠른 배타적 인가, Burst Limit 기반 독점 차단 및 에이징 기반 기아 현상 방지를 특성으로 가짐.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **중재기 (Bus Arbitrator)**: 중앙 집중 또는 분산식 중재 알고리즘을 하드웨어 Logic 회로로 집적하여 BREQ/BGRT 핀을 매핑 제어하는 제어 장치.
- **공유 버스 (Shared Bus)**: CPU, 메모리, 주변장치가 공동 공유하는 Address, Data, Control 물리 전송선.

</details>

```text
[ Centralized Bus Arbitration Architecture ]
┌───────────────────────────────────────────────────────────┐
│ Bus Masters (CPU, DMA Controller 1, DMA Controller 2)     │
│  ├─ Master 1 : BREQ1 (Request) ──> BGRT1 (Grant)          │
│  └─ Master 2 : BREQ2 (Request) ──> BGRT2 (Grant)          │
├───────────────────────────────────────────────────────────┤
│ Centralized Bus Arbitrator ASIC                           │
│  ├─ Priority Register & Round-Robin Counter               │
│  └─ Aging Timer & Bus Lock Monitor                        │
├───────────────────────────────────────────────────────────┤
│ Shared Bus Lines (Address / Data / Control Signals)       │
└───────────────────────────────────────────────────────────┘
```

| 구성요소 | 책임 |
|:---|:---|
| 중앙 중재기 | **요청 수집•정책 판정•Grant** 제어 |
| 요청•승인 신호 | 마스터와 중재기의 **사용권 Handshake** 제공 |
| 공유 버스 | 승인 마스터의 **주소•데이터•제어 신호** 전달 |
| Aging•Lock 감시기 | **기아•장기 독점** 탐지•완화 |

#### 한줄 요약
- Bus Masters, Centralized/Distributed Arbitrator Logic, BREQ/BGRT Handshake Lines 및 Shared Bus로 구성됨.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **경합 상태 (Bus Contention State)**: 2개 이상의 마스터 장치가 동일한 시스템 클록 엣지에서 BREQ 신호를 동시 출력한 불일치 상태.
- **사용권 반납 (Bus Release)**: 전송을 완결한 마스터가 BGRT 신호를 소거하고 버스 점유 핀(BUSY)을 0으로 릴리즈 해주는 하드웨어 동작.

</details>

```text
[ Multiple Bus Masters Contention Asserted ]
                         │
                         ▼
        [ 1. 요청 수신 ]
                         │
                         ▼
        [ 2. 우선순위 평가 ]
                         │
                         ▼
        [ 3. 배타적 승인•전송 ]
                         │
                         ▼
        [ 4. 사용권 반납•순환 ]
```

### 동작 원리

1. 요청 수신: 복수 마스터의 **BREQ**와 버스 상태를 수집함.
2. 우선순위 평가: Priority•Round-Robin•Aging 정책으로 승자를 정함.
3. 배타적 승인•전송: **BGRT** 후 Burst Limit 안에서 전송함.
4. 사용권 반납•순환: Release 후 다음 대기 마스터를 승인함.

#### 한줄 요약
- BREQ Assert -> Priority Evaluation -> BGRT Assert -> Data Transfer -> Bus Release & Next Master Grant 순으로 동작함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **중앙 집중식 중재 (Centralized Arbitration)**: 1개의 독립된 하드웨어 제어기(Central Arbitrator)가 시스템 전체 마스터의 BREQ/BGRT 신호를 통합 통제하는 방식.
- **분산식 중재 (Distributed Arbitration)**: 전용 중재기 없이, 각 마스터 칩이 공유 중재 버스 상의 신호를 스스로 대조하여 승인을 독자 판단하는 방식.
- **단일 장애점 (Single Point of Failure, SPOF)**: 중앙 제어기 파손 시 전체 시스템 버스 통신이 100% 마비되는 아키텍처 취약점.

</details>

| 비교 항목 | 중앙 집중식 중재 (Centralized) | 분산식 중재 (Distributed) |
|:---|:---|:---|
| 제어 아키텍처 | **단일 중앙 중재기 칩**이 전체 통제 | **각 마스터 칩 내부 중재 로직**이 상호 협선 통제 |
| 신호선 개수 | **많음** (마스터당 1:1 BREQ/BGRT 핀선 필요) | **적음** (공유 중재 버스 라인 공동 활용) |
| 판정 지연  | **매우 짧음** (중앙 ASIC의 1-Step direct 룩업) | 상대적 큼 (마스터 간 상호 토큰/합의 지연) |
| 시스템 내결함성 | 중앙 중재기가 **SPOF**가 될 수 있음 | 참여자 고장이 합의에 영향을 줄 수 있음 |
| 주요 적용 환경 | SoC 공유 자원•메모리 컨트롤러 | 토큰•분산 우선순위 기반 공유 매체 |

#### 한줄 요약
- 중앙 집중식은 단일 ASIC 기반 저지연 및 정밀 통제에 우수하나 SPOF에 취약하며, 분산식은 SPOF가 없는 고가용성 네트워크 시스템에 우수함.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **라운드 로빈 중재 (Round-Robin Arbitration)**: 버스 승인 기회를 회전 휠 방식(0 -> 1 -> 2 -> 0)으로 순환 부여하여 모든 마스터에 동일한 대역폭 지분을 공정 보장하는 알고리즘.
- **트래픽 등급 (Traffic Class / QoS)**: 버스 패킷에 우선순위 태그(QoS 0~7)를 달아, 실시간 CPU 억세스는 최우선 통과시키고 백그라운드 DMA는 차순위 처리하는 기술.

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 고정 우선순위 중재 시 저우선순위 마스터의 **기아** 발생 | **에이징** 기법 및 **라운드 로빈** 알고리즘 적용| 저우선 마스터의 최소 승인율 및 공정성 보장 |
| 특정 DMA 제어기가 버스를 연속 억세스하여 CPU 명령 인출 지연 | **버스트 한도** 및 **시간 할당량** 적용 | 단일 장치의 버스 독점 차단 및 CPU 파이프라인 정지 방지 |
| 중앙 중재기 고장 시 시스템 전체가 멈추는 **단일 장애점** | 중재기 이중화 또는 **분산식 중재** 전환 | 단일 제어기 고장 영향 범위 축소 |
| 실시간 카메라 전송 시 버스 승인 지연으로 인한 프레임 드롭 | **트래픽 등급** 기반 동적 우선순위 격상 | 실시간 입출력 트래픽 지연시간 완벽 보장 |

#### 한줄 요약
- Round-Robin/Aging 적용, Burst Limit 제어, Arbitrator Redundancy 및 Traffic Class QoS 스케줄링을 가동함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **버스 중재 선택 기준 (Bus Arbitration Selection Criteria)**: 대상 시스템의 입출력 저지연 목표, 버스 마스터 개수, 가용성 요구(SPOF 방지) 및 트래픽 QoS를 평가하여 중재 방식을 확정하는 프레임워크.

</details>

- 저지연 단일 제어는 **Centralized**, 고장 분산 요구는 **Distributed** 선택.

#### 한줄 요약
- 마스터 수•지연•공정성•SPOF를 기준으로 중재 구조와 QoS를 결정함.
