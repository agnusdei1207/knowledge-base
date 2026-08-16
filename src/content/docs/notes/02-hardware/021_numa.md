---
sidebar:
  order: 21
  label: "021. NUMA 비균등 메모리 접근 (Non-Uniform Memory Access)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "NUMA 비균등 메모리 접근 (Non-Uniform Memory Access)"
date: "2026-08-13T11:42:55+09:00"
tags:
  - "notes-hardware"
weight: 21
extra:
  question_no: "021"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "스레드•페이지 지역성의 핵심 선택 주제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **비균등 메모리 접근(Non-Uniform Memory Access, NUMA)**: 멀티소켓/멀티코어 시스템에서 프로세서와 물리 메모리(DRAM)의 상대적 물리 위치에 따라 메모리 접근 지연시간(Latency)과 대역폭이 비균등하게 달라지는 대용량 공유 메모리 아키텍처.
- **NUMA 노드(NUMA Node)**: CPU 코어 그룹, 사설/공유 캐시, 독점 메인 메모리 제어기(DRAM Channel)를 하나로 묶어 독립 제어하는 물리적/논리적 도메인 단위.
- **메모리 경합(Memory Contention)**: 단일 전역 메모리 버스에 다수 코어의 접근 요청이 동시에 몰려 신호 지연 및 억세스 병목이 일어나는 현상.

</details>

- 정의/개념: 프로세서 소켓과 물리 DRAM 메모리를 다수의 **NUMA 노드(NUMA Node)**로 분할 구축하여, 로컬 메모리와 원격 메모리 간의 접근 지연시간 차이가 발생하는 **비균등 메모리 접근** 아키텍처.
- 배경/필요성: 기존 UMA(Uniform Memory Access) 환경에서는 소켓 수가 늘어날 때 단일 공유 버스의 **메모리 경합** 및 전송 대역폭 한계로 인해 스케일아웃 확장이 불가능해짐에 따라 분산 메모리 채널 체계 필요성 증대.

#### 한줄 요약
- 소켓별 독립 메모리 제어기 및 노드 간 인터커넥트를 배치하여, 접근 위치(로컬 vs 원격)에 따른 지연 차이를 허용하면서 메인 메모리 대역폭을 극대화하는 멀티소켓 구조.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **로컬 메모리(Local Memory)**: 명령을 실행 중인 CPU 코어와 동일한 NUMA 노드 내부의 메모리 제어기에 직접 결합되어 무지연 접근이 가능한 메인 메모리.
- **원격 메모리(Remote Memory)**: 명령을 실행 중인 코어와 물리적으로 떨어져 타 NUMA 노드에 속해 있어 노드 간 인터커넥트(QPI, UPI, Infinity Fabric)를 우회 접근해야 하는 메모리.
- **ccNUMA (Cache-Coherent NUMA)**: NUMA의 비균등 메모리 분산 구조 위에서 하드웨어 캐시 일관성 프로토콜(MESI/MOESI)을 결합하여 단일 가상 주소 공간을 전역 보장하는 기술.
- **노드 간 인터커넥트(Inter-Node Interconnect)**: 노드 0과 노드 1 사이에서 원격 메모리 억세스 패킷 및 일관성 패킷을 초고속 전송하는 고속 직렬 링크 (Intel UPI, AMD IF).

</details>

- 소켓별로 **로컬 메모리** 채널을 독점 배치하여 프로세서 확장 시 메모리 접근 총 대역폭이 비례하여 확장.
- 타 노드의 **원격 메모리**는 인터커넥트 홉을 경유하여 로컬보다 긴 접근 지연 수반.
- 하드웨어 레벨의 **ccNUMA (Cache-Coherent NUMA)** 기술을 탑재하여 분산 메모리 환경에서도 단일 64-bit 가상 주소 공간 평면 유지.

#### 한줄 요약
- 로컬 메모리 우선 억세스 시 저지연 high-bandwidth를 확보하나 원격 억세스 시 홉 지연이 늘어나므로 스레드-메모리 Affinity 최적화가 필수적임.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **메모리 제어기(Memory Controller / Integrated MC)**: CPU 소켓 내부에 통합 탑재되어 4/8-Channel DDR4/DDR5/HBM DRAM 억세스를 제어하는 하드웨어 컨트롤러.
- **NUMA 인지 운영체제(NUMA-Aware OS)**: CPU 친화도(CPU Affinity)와 물리 메모리 페이지 allocation을 동일 NUMA 노드로 바인딩 관리하는 운영체제 커널 (Linux Kernel NUMA subsystem).
- **페이지 마이그레이션(Page Migration / AutoNUMA)**: 런타임에 억세스 패턴을 관찰하여 원격 접근 비율이 높은 물리 페이지를 요청 코어의 로컬 NUMA 노드로 자동 이동시키는 커널 기능.

</details>

```text
[ ccNUMA Architecture : Multi-Socket Server ]
┌──────────────────────────────────────┐     ┌──────────────────────────────────────┐
│ NUMA Node 0                          │     │ NUMA Node 1                          │
│ ┌──────────────────┐ ┌─────────────┐ │     │ ┌──────────────────┐ ┌─────────────┐ │
│ │ Cores (0 ~ 15)   │ │ Local L3    │ │     │ │ Cores (16 ~ 31)  │ │ Local L3    │ │
│ └──────────────────┘ └─────────────┘ │     │ └──────────────────┘ └─────────────┘ │
│ Integrated Memory Controller         │     │ Integrated Memory Controller         │
│  └─ [ Local DRAM Node 0 ]            │     │  └─ [ Local DRAM Node 1 ]            │
└──────────────────┬───────────────────┘     └──────────────────┬───────────────────┘
                   │                                            │
                   └─── High-Speed Interconnect Link (UPI / IF) ┘
                        (Remote Access : Additional Hop Latency)
```

| 구성요소 | 책임 |
|:---|:---|
| NUMA 노드 | **코어•캐시•메모리 제어기•DRAM** 묶음 |
| 통합 메모리 제어기 | 노드의 **로컬 DRAM 채널** 제어 |
| 노드 간 인터커넥트 | **원격 접근•일관성 패킷** 전달 |
| NUMA 인지 OS | **스레드•페이지 배치•이동** 관리 |

#### 한줄 요약
- NUMA Node(Local DRAM), Inter-Node Interconnect(UPI/IF) 및 NUMA-Aware OS 커널 바인딩이 유기적 계층 구조를 이룸.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **CPU 친화도(CPU Affinity)**: 특정 스레드/프로세스가 지정된 NUMA 노드의 코어 세트에서만 바인딩되어 실행되도록 고정하는 스케줄링 설정.
- **홈 노드(Home Node)**: 해당 물리 주소 페이지의 실제 DRAM이 꽂혀있는 기준 NUMA 노드.
- **원격 메모리 요청(Remote Memory Request)**: 로컬 노드가 아닌 타 노드의 홈 디렉터리 및 DRAM으로 인터커넥트 링크를 통해 쏘아 보내는 메모리 억세스.

</details>

```text
[ Memory Access Request (CPU Core on Node 0) ]
                      │
                      ▼
          [ 1. 홈 노드 판별 ]
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
[ 2. 로컬 접근 ]            [ 3. 원격 접근 ]
  ├─ Direct MC Bus Access     ├─ Inter-Node Link (UPI) 패킷 발송
  └─ Low Latency (예: 60ns)   └─ High Latency (예: 140ns)
        │                           │
        └─────────────┬─────────────┘
                      ▼
           [ 4. 데이터 반환 ]
                      │
           [ 원격 접근 비율 지속 감시 ]
                      ├─ 원격 비율 경미 : 현 상태 유지
                      └─ 원격 비율 과다 : [ AutoNUMA Page Migration (Node 1 -> Node 0 이동) ]
```

### 동작 원리

1. **홈 노드 판별**: 물리 주소가 속한 **Home Node**를 판별함.
2. **로컬 접근**: 같은 노드이면 로컬 메모리 제어기로 접근함.
3. **원격 접근**: 다른 노드이면 **Interconnect**로 요청을 전달함.
4. **데이터 반환**: 원격 비율이 높으면 **페이지 마이그레이션**을 검토함.

#### 한줄 요약
- Address Home Node 판별 -> 로컬 억세스(저지연) / 원격 억세스(인터커넥트 홉) -> AutoNUMA Page Migration 순서로 동작함.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **UMA (Uniform Memory Access)**: 단일 전역 버스나 크로스바 스위치를 사용하여 어떤 코어에서 물리 메모리를 억세스하든 지연시간이 동일한 구형 아키텍처.
- **다중 소켓(Multi-Socket)**: 메인보드 상에 2개, 4개, 8개의 독립 CPU 소켓을 물리 탑재하여 랙 서버 용량을 늘리는 기술.
- **배치 민감도(Placement Sensitivity)**: 스레드와 페이지 할당 위치(로컬 vs 원격)에 따라 전체 애플리케이션 처리 성능이 최대 수 배 이상 요동치는 현상.

</details>

| 비교 항목 | NUMA (Non-Uniform Memory Access) | UMA (Uniform Memory Access) |
|:---|:---|:---|
| 메모리 접근 지연 | 위치에 따른 **로컬•원격 지연 차이** | 모든 코어가 유사한 메모리 지연 공유 |
| 메모리 대역폭 | **매우 높음** (소켓별 독점 DRAM 채널 분산 제공) | 제한적 (단일 전역 버스에 억세스가 쏠려 포화) |
| 시스템 확장성 | 소켓별 채널로 **용량•대역폭 확장** | 공유 메모리 경로의 경합으로 제한 |
| 소프트웨어 민감도 | **배치 민감도** 매우 큼 (NUMA 튜닝 필수) | 민감도 없음 (OS 스케줄러가 임의 조율 가능) |
| 대표 채택 환경 | 최신 2-Socket/4-Socket 엔터프라이즈 서버 | 단일 소켓 PC, 모바일 AP, 소형 임베디드 |

#### 한줄 요약
- NUMA는 비균등 지연 대가로 멀티소켓 대역폭/용량 확장에 우수하며, UMA는 균등 지연을 제공하나 확장성에 한계가 있음.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **최초 접근 정책(First-Touch Policy)**: 페이지를 최초 접근한 스레드의 NUMA 노드에 물리 페이지를 배치하는 정책.
- **자동 NUMA 균형(Automatic NUMA Balancing)**: Linux 커널이 런타임 페이지 폴트 통계를 분석해 스레드와 페이지를 동일 노드로 끌어당기는 자율 동기화 기능.
- **재배치 진동(Placement Oscillation / Ping-Ponging)**: 멀티스레드가 공유 데이터를 동시 억세스할 때 AutoNUMA가 페이지를 노드 0과 노드 1 사이에서 무한히 오가며 칩 오버헤드를 일으키는 부작용.
- **`numactl`**: Linux CLI 도구로, 특정 프로세스를 특정 NUMA 노드의 코어 및 로컬 메모리에 명시적으로 바인딩 구동하는 튜닝 툴 (`numactl --cpunodebind=0 --membind=0`).

</details>

| 문제 및 병목 원인 | 실무적 대책 및 해결 방안 | 기대 효과 |
|:---|:---|:---|
| 단일 메인 스레드가 데이터 초기화 시 **First-Touch Policy**로 특정 노드 메모리만 포화 | 스레드 생성 후 **병렬 초기화** 및 `numactl --interleave` 적용 | 모든 NUMA 노드 메모리 채널로 분산 균등 할당 |
| DB•Redis에서 원격 접근 증가로 트랜잭션 지연 상승 | `numactl`로 **CPU Affinity•로컬 메모리 바인딩** 고정 | 원격 접근 감소와 쿼리 지연 안정화 |
| AutoNUMA 활성화 시 노드 간 페이지 무한 이동 **재배치 진동** 발생 | AutoNUMA **마이그레이션 임계치** 조율 및 대형 DB에선 AutoNUMA 비활성화 | 불필요한 노드 간 메모리 이사 트래픽 차단 |
| Oracle / Postgre DB의 버퍼 풀이 원격 노드에 배치되어 TPS 하락 | **버퍼 풀 지역화** 및 소켓 단위 파티셔닝 | DB 노드 내 전용 버퍼 히트율 상향으로 처리량 극대화 |

#### 한줄 요약
- Parallel Init, `numactl` Local Binding, AutoNUMA Oscillation 차단 및 Buffer Pool Localization 기법을 적용함.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **NUMA 튜닝 프레임워크(NUMA Optimization Framework)**: 멀티소켓 서버 구축 시 하드웨어 노드 토폴로지 분석, OS 커널 바인딩, DB 버퍼 풀 파티셔닝을 결합하여 로컬 메모리 히트율을 극대화하는 종합 가이드라인.

</details>

- 공유 데이터가 적으면 **Local Binding**, 노드 간 공유가 크면 **Interleave**•**분할** 선택.

#### 한줄 요약
- 원격 접근률과 대역폭 균형을 기준으로 스레드•페이지 배치를 결정함.
