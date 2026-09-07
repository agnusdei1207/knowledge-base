---
sidebar:
  order: 29
  label: "029. NUMA 인지 스케줄링"
  badge:
    text: "미출 · 50%"
    variant: note
title: "NUMA 인지 스케줄링 (NUMA-aware Scheduling)"
date: "2026-09-07T09:55:00+09:00"
tags:
  - "notes-software"
weight: 29
extra:
  question_no: "029"
  source_status: "기출"
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
- 배경/필요성: 멀티소켓 NUMA 서버에서 스레드와 메모리 노드 불일치 시 발생하는 **소켓 간 인터커넥트 원격 접근 지연(로컬 대비 2~3배) 및 대역폭 포화 병목 한계**

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
- First-Touch와 AutoNUMA는 지역성을 지키는 대신 각각 초기 할당 위치에 대한 제약과 런타임 이주 비용을 요구하므로, 정적 고정과 동적 보정 사이의 선택이 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **인터커넥트(Interconnect)**: Intel UPI(Ultra Path Interconnect), AMD Infinity Fabric 등 소켓 간 고속 통신 링크.
- **vNUMA(Virtual NUMA)**: 가상 머신(VM)에 호스트의 물리 NUMA 토폴로지를 그대로 노출하여 게스트 OS 수준의 최적화를 가능하게 하는 기술.

</details>

```text
[NUMA 인지 스케줄링 체계]
  │
  ├─ [NUMA 노드 0] (로컬 도메인 0)
  │     ├─ [CPU 코어 0~15] (로컬 런 큐 스케줄링)
  │     └─ [로컬 DRAM 0] (로컬 메모리 저지연 접근)
  │
  ├─ [초고속 인터커넥트] (UPI·Infinity Fabric)
  │     └─ [원격 메모리 버스] (소켓 간 일관성 전송)
  │
  └─ [NUMA 노드 1] (원격 도메인 1)
        ├─ [CPU 코어 16~31] (로컬 런 큐)
        ├─ [로컬 DRAM 1] (로컬 메모리)
        └─ [AutoNUMA 엔진] (힌트 폴트 감지 및 이주)
```

선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| NUMA 노드 | 코어와 DRAM의 **로컬 자원 단위** |
| 인터커넥트 | 일관성 패킷과 **원격 메모리 전송** |
| AutoNUMA 엔진 | 힌트 폴트 기반 **페이지·스레드 이주** |
| numactl 도구 | CPU·메모리의 **노드 바인딩** |

#### 한줄 요약
- AutoNUMA는 실행 중 접근 패턴을 관측해 옮기고 numactl은 시작 시점에 고정하므로, 자동 최적화와 수동 확정 중 무엇을 쓸지는 워크로드의 안정성에 달린다.

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
- 페이지 이주는 원격 접근을 없애는 대신 복사 비용을 즉시 지불하므로, 비용 편익 분석 단계가 이주가 이득이 되는 접근 횟수의 경계를 정한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Interleave Policy**: 메모리 페이지를 모든 NUMA 노드에 균등하게 라운드로빈 분산하여 단일 노드 대역폭 병목을 분산시키는 정책.

</details>

| 메모리 할당 정책 | Local Node Policy (기본) | Node Bind Policy (강제) | Interleave Policy (분산) |
|:---|:---|:---|:---|
| 할당 방식 | **현재 실행 중인 로컬 노드 우선** | **지정된 특정 NUMA 노드에만 할당** | **모든 NUMA 노드에 라운드로빈 분산** |
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
- NUMA 바인딩은 원격 접근을 없애는 대신 스케줄러의 배치 자유도를 포기하므로, 지역성이 뚜렷한 워크로드는 numactl로 고정하고 접근이 흩어지는 워크로드는 interleave로 대역폭을 고르게 쓴다.

## Ⅶ. 결론

- 멀티소켓 대규모 엔터프라이즈 서버 및 HPC/AI 연산 인프라의 **핵심 메모리 지역성 최적화 표준 기술**로 정립되었으며, 실무 고성능 환경에서는 **DBMS/초저지연 애플리케이션의 `numactl`(--cpunodebind/--membind) 물리 고정, 가상화 환경의 vNUMA 토폴로지 노출, 대규모 분산 메모리 워크로드의 `numactl --interleave=all` 및 `vm.zone_reclaim_mode=0` 튜닝**을 결합하여 메모리 대역폭을 극대화

#### 한줄 요약
- NUMA 인지 스케줄링은 하드웨어 토폴로지와 소프트웨어 배치를 일치시켜 멀티소켓 서버의 메모리 병목을 해소하는 핵심 인프라 기술이다.
