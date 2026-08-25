---
sidebar:
  order: 29
  label: "029. NUMA 인지 스케줄링"
  badge:
    text: "미출 · 50%"
    variant: note
title: "NUMA 인지 스케줄링 (NUMA-aware Scheduling)"
date: "2026-08-25T10:48:00+09:00"
tags:
  - "notes-software"
weight: 29
extra:
  question_no: "029"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "NUMA 지역성 기반 스레드 및 메모리 배치"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **NUMA(Non-Uniform Memory Access)**: CPU 소켓마다 로컬 메모리를 독점 연결하고, 타 소켓 메모리는 인터커넥트(UPI/Infinity Fabric)를 경유해 접근 지연이 발생하는 아키텍처.
- **NUMA 인지 스케줄링(NUMA-aware Scheduling)**: 스레드가 실행되는 CPU 코어와 할당된 메모리를 동일한 로컬 NUMA 노드에 배치하는 커널 스케줄링 기법.

</details>

- 정의/개념: 다중 소켓 환경에서 스레드와 할당 메모리를 동일 노드에 배치하여 **원격 메모리 접근 지연**을 최소화하는 커널 스케줄링 기법
- 배경/필요성: 스레드와 메모리 노드 불일치 시 **소켓 간 인터커넥트 버스 병목 및 2~3배의 원격 메모리 레이턴시 증가 해결 불가**

#### 한줄 요약
- 프로세서와 메모리 노드의 물리 토폴로지를 일치시켜 로컬 메모리 접근 비율을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **First-Touch Policy**: 가상 메모리 할당 시점이 아니라, 프로세스가 메모리에 처음 쓰기(Write)를 수행한 CPU 코어의 로컬 NUMA 노드에 물리 페이지를 할당하는 정책.
- **AutoNUMA**: 런타임에 원격 메모리 접근 빈도를 감지하여 메모리 페이지를 해당 스레드가 실행 중인 로컬 노드로 자동 마이그레이션하는 리눅스 기능.

</details>

- **First-Touch Policy** 기반 초기 로컬 메모리 물리 프레임 할당으로 인터커넥트 트래픽 차단
- **AutoNUMA(자동 NUMA 밸런싱)** 기반의 런타임 페이지 이주 및 스레드-메모리 친화도 유지
- 특정 노드 메모리 고갈 시 타 노드 할당(Remote)과 조기 스왑(Swap) 간의 트레이드오프

#### 한줄 요약
- First-Touch로 로컬에 할당하고, AutoNUMA로 런타임 페이지를 이주하여 지역성을 보존한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **인터커넥트(Interconnect)**: Intel UPI(Ultra Path Interconnect), AMD Infinity Fabric 등 소켓 간 고속 통신 링크.
- **vNUMA(Virtual NUMA)**: 가상 머신(VM)에 호스트의 물리 NUMA 토폴로지를 그대로 노출하여 게스트 OS 수준의 최적화를 가능하게 하는 기술.

</details>

```text
[NUMA 2-Socket 시스템 스케줄링 구조]
|-- NUMA 노드 0 (소켓 0)
|   |-- CPU 코어 0 ~ 15 (스케줄링 도메인 0)
|   |-- 로컬 메모리 컨트롤러 & 로컬 DRAM 0 (접근 지연 ~50ns)
|   `-- 로컬 런 큐 & 로컬 페이지 할당기
|-- 소켓 간 초고속 인터커넥트 (Intel UPI / AMD Infinity Fabric: 원격 접근 지연 ~150ns)
`-- NUMA 노드 1 (소켓 1)
    |-- CPU 코어 16 ~ 31 (스케줄링 도메인 1)
    |-- 로컬 메모리 컨트롤러 & 로컬 DRAM 1
    `-- AutoNUMA 엔진 (원격 접근 힌트 폴트 감지 -> 노드 0 <-> 1 페이지 이주)
```

선의 의미: 계층 및 로컬/원격 메모리 인터커넥트 토폴로지

| 구성요소 | 책임 |
|:---|:---|
| **NUMA 노드** | CPU 코어 그룹과 로컬 메모리 컨트롤러를 묶은 독립적인 저지연 자원 단위 |
| **인터커넥트 (UPI/IF)** | 서로 다른 NUMA 노드 간 캐시 일관성(MESI) 패킷 및 원격 메모리 데이터 전송 |
| **AutoNUMA 엔진** | 원격 메모리 접근 힌트 폴트를 수집하여 페이지/스레드를 최적 노드로 자동 이주 |
| **numactl 도구** | 사용자 공간에서 프로세스의 CPU 코어 바인딩 및 메모리 할당 정책을 강제 제어 |

#### 한줄 요약
- NUMA 노드, 소켓 인터커넥트, AutoNUMA 엔진, numactl 도구가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **NUMA 힌트 폴트(NUMA Hint Fault)**: 커널이 페이지 권한을 PROT_NONE으로 일시 변경하여 스레드가 원격 메모리에 접근할 때 트랩을 발생시켜 접근 통계를 수집하는 기법.

</details>

```text
스레드 생성 및 메모리 할당 요청
        │
   First-Touch 정책: 스레드가 실행 중인 로컬 NUMA 노드 0에 물리 메모리 할당
        │
   스레드가 타 코어로 마이그레이션되어 노드 1의 코어에서 실행 중
        │
   커널이 페이지 권한을 PROT_NONE으로 설정하여 NUMA 힌트 폴트 유발
        │
   스레드가 메모리 접근 시 원격 접근 힌트 폴트 인터럽트 발생 및 통계 누적
        │
   페이지 이주 비용 대비 원격 지연 단축 이득이 큰가?
   ┌────┴─────┐
  예           아니오
   │             │
페이지를 노드 1 로컬 메모리로   현재 노드 배치 유지
물리 복사 (Page Migration)   (원격 접근 지속)
```

#### 한줄 요약
- First-Touch 할당 → 힌트 폴트 감시 → 비용 편익 분석 → 페이지 물리 이주 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Interleave Policy**: 메모리 페이지를 모든 NUMA 노드에 균등하게 라운드로빈 분산하여 단일 노드 대역폭 병목을 분산시키는 정책.

</details>

| 메모리 할당 정책 | Local Node Policy (기본) | Node Bind Policy (강제) | Interleave Policy (분산) |
|:---|:---|:---|:---|
| **할당 방식** | **현재 실행 중인 로컬 노드 우선** | **지정된 특정 NUMA 노드에만 할당** | **모든 NUMA 노드에 라운드로빈 분산** |
| 지연시간 특성 | 로컬 접근 시 최저 지연 (~50ns) | 로컬 보장 (지연시간 편차 없음) | 전체 평균 지연시간 균일화 (~100ns) |
| 단점 및 위험 | 특정 노드 메모리 편중 시 스왑 | **지정 노드 용량 초과 시 OOM 발생** | L3/로컬 캐시 지역성 저하 |
| 주 적용처 | 범용 애플리케이션 | 초저지연 주식 거래, 전용 DB 인스턴스 | 대규모 공유 메모리 DBMS, 빅데이터 연산 |

#### 한줄 요약
- 단일 프로세스는 Local/Bind 정책, 대규모 공유 메모리는 Interleave 정책을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **numactl**: 리눅스에서 `numactl --cpunodebind=0 --membind=0 ./app` 명령으로 CPU와 메모리를 특정 노드에 물리 고정하는 명령어.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 NUMA 노드 메모리 고갈로 인한 시스템 조기 스왑 | 대용량 DB 기동 시 **`numactl --interleave=all`** 적용 | 메모리 용량 및 대역폭을 전 소켓으로 균등 확장 |
| AutoNUMA의 과도한 페이지 이주 연산으로 CPU 오버헤드 | 고정 워크로드에 **`numactl --membind` 및 코어 피닝** 적용 | 런타임 이주 오버헤드 0화 및 결정론적 레이턴시 확보 |
| 가상화 환경에서 게스트 OS가 NUMA 토폴로지 미인지 | 하이퍼바이저에서 **vNUMA(Virtual NUMA)** 활성화 | 게스트 커널이 물리 NUMA 인식 후 로컬 메모리 최적화 |
| `zone_reclaim_mode` 활성화로 인한 성능 급락 | **`sysctl vm.zone_reclaim_mode=0`** 설정 | 불필요한 로컬 캐시 회수 대신 타 노드 여유 메모리 할당 |

#### 한줄 요약
- numactl 바인딩, interleave 설정, vNUMA 가상화 투영, zone_reclaim_mode 비활성화로 성능을 극대화한다.

## Ⅶ. 결론

- 멀티소켓 고성능 DB(Oracle, MySQL, Redis)는 **`numactl` 기반 Node Bind 및 vNUMA**를 적용하여 메모리 인터커넥트 병목을 원천 차단하고 베어메탈 최고 속도 확립

#### 한줄 요약
- NUMA 인지 스케줄링은 하드웨어 토폴로지와 소프트웨어 배치를 일치시켜 멀티소켓 서버의 메모리 병목을 해소하는 핵심 인프라 기술이다.