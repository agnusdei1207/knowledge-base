---
sidebar:
  order: 93
  label: "093. 멀티소켓 서버•SMP"
  badge:
    text: "미출 · 50%"
    variant: note
title: "멀티소켓 서버•SMP (Multi-Socket Server•SMP)"
date: "2026-08-25T10:25:00+09:00"
tags:
  - "notes-hardware"
weight: 93
extra:
  question_no: "093"
  source_status: "미출"
  source_history: ""
  priority: 50
  priority_note: "지역성•원격 메모리 비용 중심 설계"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **멀티소켓 서버(Multi-Socket Server)**: 단일 메인보드에 2개 이상의 독립된 CPU 소켓을 장착하고 고속 인터커넥트로 연결한 서버.
- **SMP(Symmetric Multiprocessing)**: 모든 CPU 코어가 단일 OS 아래에서 전체 시스템 메모리와 I/O를 대칭적으로 공유하는 병렬 구조.
- **ccNUMA(Cache-Coherent NUMA)**: 물리적 메모리가 소켓별로 분할 배치되어 접근 거리에 따른 지연시간 차이가 존재하나 캐시 일관성을 하드웨어가 보장하는 아키텍처.

</details>

- 정의/개념: 다수 물리 CPU 소켓을 점대점 고속 인터커넥트로 연결해 단일 공유 메모리 공간을 제공하는 **멀티소켓 서버(ccNUMA SMP)**
- 배경/필요성: 단일 소켓 CPU의 코어 수 및 메모리 한계로 인해 **대규모 인메모리 DB 및 고밀도 가상화 컴퓨팅 수용 불가**

#### 한줄 요약
- 다중 CPU 소켓을 고속 버스로 결합하여 단일 OS 아래 대규모 코어와 테라바이트급 메모리를 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **인터커넥트 패브릭(Interconnect Fabric)**: CPU 소켓 간에 캐시 스눕(Snoop) 패킷과 원격 메모리 데이터를 중계하는 점대점 직렬 버스(Intel UPI, AMD Infinity Fabric).
- **NUMA 비율(NUMA Ratio)**: 로컬 메모리 접근 지연시간 대비 다른 소켓의 원격 메모리(Remote Memory) 접근 지연시간의 비율(보통 1.5배~2.5배).

</details>

- 단일 OS 하에서 수백 개의 CPU 코어가 분산 메모리를 투명하게 공유하는 **대칭형 다중 처리(SMP)**
- 하드웨어 디렉터리 프로토콜 기반의 완벽한 소켓 간 **캐시 일관성(Cache Coherency)** 유지
- 물리적 거리에 따라 지연시간이 차이 나는 **ccNUMA** 구조 및 소프트웨어 메모리 지역성 최적화 필수

#### 한줄 요약
- 하드웨어 캐시 일관성을 유지하는 공유 메모리 구조이며, 원격 메모리 접근 지연을 줄이는 지역성 설계가 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **UPI / Infinity Fabric**: 인텔과 AMD의 독자적인 소켓 간 고속 점대점 인터커넥트 버스로 초당 수십 기가트랜스퍼(GT/s)의 대역폭 제공.

</details>

```text
[멀티소켓 ccNUMA 서버 아키텍처]
|-- NUMA 노드 0 (소켓 0)
|   |-- CPU 코어 그룹 (L1/L2/L3 캐시)
|   |-- 로컬 메모리 컨트롤러 -> 로컬 DRAM 0 (~80ns)
|   `-- 소켓 0 로컬 PCIe Root Complex (로컬 NVMe/NIC)
|-- 소켓 간 인터커넥트 패브릭 (Intel UPI / AMD IF - ~140ns 원격 통신)
`-- NUMA 노드 1 (소켓 1)
    |-- CPU 코어 그룹 (L1/L2/L3 캐시)
    |-- 로컬 메모리 컨트롤러 -> 로컬 DRAM 1 (~80ns)
    `-- 소켓 1 로컬 PCIe Root Complex
```

선의 의미: 계층 및 소켓 간 점대점 버스 연결

| 구성요소 | 책임 |
|:---|:---|
| **NUMA 노드(Socket)** | CPU 코어 그룹과 해당 소켓의 메모리 컨트롤러에 직결된 로컬 DRAM 기본 단위 |
| **인터커넥트 패브릭** | 소켓 간 원격 메모리 I/O 데이터 전송 및 캐시 일관성 디렉터리 스눕 처리 |
| OS NUMA 스케줄러 | First-Touch 할당 및 AutoNUMA 페이지 마이그레이션으로 메모리 지역성 극대화 |
| 소켓별 PCIe Root Complex | 각 NUMA 노드에 로컬화된 고속 I/O 디바이스(NIC, GPU, NVMe) 통제 |

#### 한줄 요약
- 소켓별 NUMA 노드, 고속 인터커넥트 패브릭, OS NUMA 스케줄러, 로컬 PCIe 컨트롤러가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **First-Touch 정책**: 리눅스 커널에서 프로세스가 메모리를 처음 접근(쓰기)하는 시점에 해당 코어가 속한 로컬 NUMA 노드에 물리 페이지를 할당하는 기본 정책.

</details>

```text
애플리케이션 스레드가 메모리 할당(malloc) 후 최초 쓰기 발생
        │
   OS가 First-Touch 정책에 따라 실행 중인 코어의 로컬 DRAM에 페이지 할당
        │
   스레드가 메모리 읽기/쓰기 명령 실행
        │
   접근 대상 물리 주소가 로컬 소켓 메모리인가?
   ┌────┴─────┐
  예           아니오 (원격 소켓 메모리)
   │             │
로컬 메모리 버스 소켓 간 인터커넥트(UPI/IF) 경유
직접 인출 (~80ns)원격 패킷 전송 (~140ns, NUMA Penalty 발생)
   │             │
   │        AutoNUMA 커널 데몬이 원격 접근 빈도 감지
   │             │
   │        해당 페이지를 스레드가 실행 중인 로컬 노드로 자동 마이그레이션
   └────┬────────┘
        │
   캐시 일관성 유지 하에 트랜잭션 완료
```

#### 한줄 요약
- First-Touch 할당 → 로컬/원격 메모리 접근 분기 → AutoNUMA 자동 마이그레이션 → 트랜잭션 완료 순으로 처리된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Cluster MPP(Massively Parallel Processing)**: 노드 간 메모리를 공유하지 않고(Shared-Nothing) 고속 네트워크 메시지로 협업하는 대규모 분산 구조.

</details>

| 서버 아키텍처 | 멀티소켓 서버 (ccNUMA / SMP) | 단일 소켓 서버 (1-Socket UMA) | 분산 클러스터 (MPP / Scale-Out) |
|:---|:---|:---|:---|
| 메모리 구조 | 물리 분산, 논리 단일 공유 메모리 | 균일 메모리 접근 (UMA) | 비공유(Shared-Nothing) 구조 |
| 캐시 일관성 | **하드웨어 디렉터리 ccNUMA** | 단일 소켓 내 캐시 일관성 | 하드웨어 일관성 없음 (네트워크 통신) |
| 확장성 및 지연 | 수십 TB 메모리 (원격 지연 존재) | 단일 CPU 용량 한계 (초저지연) | 수천 대 무제한 확장 (네트워크 지연) |
| 주요 응용처 | 대규모 RDBMS, SAP HANA, 가상화 팜 | 웹 서버, 마이크로서비스, 단일 DB | 빅데이터(Hadoop), 초거대 AI 분산 학습 |

#### 한줄 요약
- 단일 대용량 인메모리 DB는 멀티소켓 ccNUMA, 경량 서비스는 단일 소켓, 대규모 AI 분산은 MPP 클러스터가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **거짓 공유(False Sharing)**: 서로 다른 코어가 사용하는 독립된 변수들이 동일한 64바이트 캐시 라인에 위치하여 캐시 무효화 트래픽이 폭증하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 스레드 이동으로 인한 원격 메모리 접근 지연 급증 | **numactl / taskset** 기반 CPU 및 NUMA 메모리 노드 바인딩 | 메모리 지역성 극대화 및 소켓 간 인터커넥트 병목 차단 |
| 동일 캐시 라인(64B) 공유로 인한 **거짓 공유** 발생 | 64바이트 단위 데이터 구조체 정렬(Align) 및 패딩 적용 | 소켓 간 불필요한 캐시 무효화(Invalidation) 트래픽 차단 |
| 가상 머신 메모리가 복수 노드에 걸쳐 성능 저하 | 하이퍼바이저 **vNUMA 토폴로지 매핑** 및 코어 피닝 | 가상화 환경 원격 메모리 지연 극소화 및 네이티브 성능 확보 |
| 원격 소켓 I/O 장치(NIC/NVMe) 접근 시 대역폭 저하 | 인터럽트 및 DMA 처리를 로컬 NUMA 코어에 바인딩 | 소켓 간 UPI 대역폭 낭비 방지 및 I/O 처리율 극대화 |

#### 한줄 요약
- numactl 노드 바인딩, 64B 캐시 정렬, vNUMA 매핑, I/O 디바이스 로컬화를 통해 성능을 최적화한다.

## Ⅶ. 결론

- 대규모 인메모리 DB 및 핵심 ERP 시스템은 **4-Socket ccNUMA 서버**를 구축하고, **numactl 노드 바인딩 및 CXL 메모리 확장**을 결합하여 고성능 엔터프라이즈 인프라 달성

#### 한줄 요약
- 멀티소켓 서버는 하드웨어 캐시 일관성 기반 단일 메모리 공간을 제공하며, 메모리 지역성 최적화가 성능의 핵심이다.