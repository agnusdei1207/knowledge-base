---
sidebar:
  order: 29
  label: "029. NUMA 인지 스케줄링 (NUMA-aware Scheduling)"
  badge:
    text: "미출제 • 50%"
    variant: note
title: "NUMA 인지 스케줄링 (NUMA-aware Scheduling)"
date: "2026-08-13T14:12:00+09:00"
tags:
  - "notes-software"
weight: 29
extra:
  question_no: "029"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "NUMA 지역성 기반 스레드 배치 가치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NUMA (Non-Uniform Memory Access)**: 멀티소켓 CPU 아키텍처에서 물리적 거리 및 버스(Interconnect, QPI/UPI)에 따라 특정 CPU가 특정 메모리에 접근하는 속도(Latency)가 불균일한 메모리 구조.
- **NUMA-aware Scheduling**: OS 커널 스케줄러 및 메모리 관리자가 프로세스/스레드의 구동 CPU 노드와 물리 메모리(DRAM) 할당 위치를 동일한 NUMA Node로 상호 결합(Locality)하여 원격 접근 지연을 줄이는 기술.
- **Remote Memory Access**: CPU가 다른 NUMA 노드의 메모리에 인터커넥트를 거쳐 접근하는 통신.

</details>

- 정의/개념: 멀티소켓 NUMA 시스템 상에서 프로세스 스레드와 물리 페이지 할당 위치를 동일한 노드로 바인딩하여 원격 메모리 지연을 극복하는 **NUMA-aware Scheduling**
- 배경/필요성: 스레드•페이지의 노드 불일치는 **원격 접근 지연**과 링크 부하 유발

#### 한줄 요약

- NUMA 인지 스케줄링으로 스레드와 페이지를 공동 배치하는 것이 핵심이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **First-Touch Policy**: 메모리 페이지 최초 할당 시 해당 페이지를 실제로 가장 먼저 읽거나 쓴 CPU 코어의 로컬 NUMA 노드 메모리에 물리 공간을 배정하는 기법.
- **AutoNUMA (NUMA Balancing)**: Linux 커널이 백그라운드에서 스레드의 주기적 억세스 패턴을 모니터링하여, 멀리 떨어진 타 노드의 메모리 페이지를 해당 스레드가 속한 로컬 노드로 자동 이주(Page Migration)시키는 기능.

</details>

- **Local Memory Access** 비율을 높여 원격 경로 사용 감소
- 초기 할당 정책 (**First-Touch Policy**) 및 런타임 페이지 이주 (**AutoNUMA Page Migration**)
- CPU Affinity 바인딩 과도 적용 시 노드 간 메모리 불균형(Memory Pressure) 트레이드오프

#### 한줄 요약

- 지역성 이득과 이주 비용의 절충이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **vNUMA (Virtual NUMA)**: 하이퍼바이저가 게스트 VM에게 물리 하드웨어의 NUMA 토폴로지 정보를 그대로 노출하여, 게스트 OS 내부에서도 NUMA-aware 스케줄링이 작동되게 하는 기술.

</details>

```text
                    [NUMA Node]
                         |
             [Interconnect (UPI/QPI)]
                    /            \
     [AutoNUMA Balancing]      [numactl]
```

선의 의미: 토폴로지 관리자(numactl/lscpu)가 CPU 코어-메모리 매핑을 파악하여 배치 정책(First-touch) 및 재배치 제어기(AutoNUMA)로 노드 자원을 할당하는 아키텍처.

| 구성요소 | 주요 역할 및 핵심 기능 |
|:---|:---|
| NUMA Node | 물리 CPU 소켓 및 고속 내장 메모리 컨트롤러로 결합된 단일 자원 그룹 |
| Interconnect (UPI/QPI) | NUMA Node 간 데이터를 이송하는 통신 버스로, 원격 억세스 시 병목 유발 |
| AutoNUMA Balancing | 주기적 메모리 Scan 및 **Page Fault (Hint Fault)** 트리거를 통한 페이지 로컬 이주 |
| `numactl` | CLI 툴로 특정 프로세스를 원하는 NUMA Node CPU/Memory에 지정 바인딩 |

#### 한줄 요약

- 토폴로지, 메모리 바인딩, NUMA 노드가 배치 경계를 정한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **NUMA Hint Fault**: Linux AutoNUMA 엔진이 페이지 프로텍션을 변경(PROT_NONE)하여 해당 페이지 억세스 시 하드웨어 트랩을 발동, 스레드와 페이지의 노드 불일치를 감지하는 기술.

</details>

```text
┌──────────────────────────────┐
│ 1. 토폴로지•부하 수집      │
│ 2. 스레드•페이지 공동 배치 │
│ 3. 원격 접근 통계 감시     │
│ 4. 이주 편익 판정          │
│ 5. 스레드•페이지 이주      │
└──────────────────────────────┘
```

### 동작 원리

1. **토폴로지·부하 수집**: `numactl --hardware` 시스템 노드 간 거리(Distance Vector) 및 CPU/Memory 상태 파악.
2. **스레드·페이지 공동 배치**: 프로세스 런타임 생성 시 **First-Touch Policy** 적용 및 로컬 노드 메모리 1차 할당.
3. **원격 접근 통계 감시**: **NUMA Hint Fault** 및 PMU 하드웨어 카운터 모니터링을 통한 원격 억세스 추적.
4. **이주 편익 판정**: 페이지 이주 비용(Page Copy) 대비 원격 지연 절감 편익 계산.
5. **스레드·페이지 이주**: 편익 우위 시 스레드를 해당 노드로 이송하거나 페이지를 로컬 노드로 **AutoNUMA Page Migration**.

#### 한줄 요약

- 이주 편익 판정 결과에 따라 스레드•페이지 이주를 수행한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Interleave Policy**: 메모리 페이지를 모든 NUMA 노드에 균등하게 순환 분산(Round-Robin) 배치하여 메모리 대역폭을 극대화하는 정책.

</details>

| 메모리 할당 정책 | 동작 매커니즘 | 주요 용도 및 특성 |
|:---|:---|:---|
| **Local Node (First-Touch)** | 최초 접근 CPU의 로컬 노드에 우선 할당 | 높은 지역성 / 노드 메모리 편중 가능 |
| **Node Bind** | 지정된 특정 NUMA 노드(e.g., Node 0)에만 강제 할당 | 프로세스 격리, DB 전용 파티셔닝 |
| **Interleave** | 모든 NUMA 노드에 페이지를 순차 분산 할당 | **대용량 대역폭(Bandwidth) 요구 작업** |
| **Preferred Node** | 지정 노드 우선 할당하되 용량 부족 시 타 노드 우회 | 유연한 리소스 수용성 확보 |

#### 한줄 요약

- 메모리 거리 반영은 NUMA 인지, 부하 중심은 NUMA 비인지 스케줄링이 핵심이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **NUMA Node Memory Exhaustion**: 특정 노드의 가용 메모리가 고갈되어 할당 실패나 원격 할당이 발생하는 상태.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 노드의 메모리 압력 증가 | 바인딩 완화 또는 **Interleave** 정책 검토 | 노드 간 용량 편차 완화 |
| AutoNUMA 스캔•이주 비용 증가 | 측정 후 정적 바인딩과 자동 균형 선택 | 스캔과 원격 접근 비용 절충 |
| vCPU•메모리와 물리 노드 불일치 | **vNUMA** 노출과 CPU•메모리 공동 배치 | 원격 접근 빈도 감소 |

> 사례: PostgreSQL / Oracle DB 구동 시 `numactl --interleave=all` 또는 `numactl --cpunodebind=0 --membind=0` 적용

#### 한줄 요약

- 병렬 초기화, 절감 임계값, 재이주 대기시간을 적용한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **NUMA 최적화 기준(NUMA Optimization Criteria)**: 메모리 대역폭 위주(Interleave) vs 단일 억세스 지연 위주(Locality/Bind) 요구에 따른 수립 체계.

</details>

- 지연 민감 작업은 **Node Bind**, 대역폭•용량 분산은 **Interleave** 선택

#### 한줄 요약

- 원격 접근 절감량과 이주 비용을 함께 평가하는 것이 핵심이다.
