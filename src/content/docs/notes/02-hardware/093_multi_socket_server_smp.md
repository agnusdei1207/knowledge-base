---
sidebar:
  order: 93
  label: "093. 멀티소켓 서버•SMP"
  badge:
    text: "미출 • 50%"
    variant: note
title: "멀티소켓 서버•SMP (Multi-Socket Server•SMP)"
date: "2026-08-17T09:25:00+09:00"
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

- **Multi-Socket Server(멀티소켓 서버)**: 단일 메인보드에 2개 이상의 독립된 CPU 소켓을 장착하고 고속 버스로 연결하여 대규모 코어와 테라바이트급 메모리를 단일 시스템으로 운영하는 서버.
- **SMP(Symmetric Multiprocessing, 대칭형 다중 처리)**: 모든 CPU 코어가 단일 운영체제 하에서 동일한 권한으로 전체 시스템 메모리와 I/O를 공유하는 병렬 컴퓨팅 구조.
- **ccNUMA(Cache-Coherent Non-Uniform Memory Access)**: 소켓별로 물리적 메모리가 분할 배치되어 접근 거리에 따른 지연시간 차이가 존재하지만 하드웨어가 캐시 일관성을 완벽히 보장하는 아키텍처.

</details>

- 정의/개념: 단일 마더보드에 2개 이상의 물리 CPU 소켓을 장착하고, 고속 점대점 인터커넥트(Intel UPI, AMD Infinity Fabric)로 결합하여 단일 공유 메모리 공간(SMP) 및 캐시 일관성 불균일 메모리 접근(ccNUMA)을 제공하는 엔터프라이즈 서버 아키텍처
- 배경/필요성: 단일 소켓의 코어 수 및 메모리 채널 한계 극복과 대규모 인메모리 DB 및 고밀도 가상화 컴퓨팅 풀 확장 필요

#### 한줄 요약

- 다중 소켓 간 고속 인터커넥트와 캐시 일관성을 지원하는 **대칭형 멀티프로세싱(SMP) 및 ccNUMA 서버 아키텍처**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Interconnect Fabric(소켓 간 고속 링크)**: CPU 소켓 간에 캐시 스눕(Snoop) 패킷과 원격 메모리 데이터를 초저지연으로 중계하는 점대점 직렬 버스(Intel UPI: Ultra Path Interconnect).
- **NUMA Ratio(누마 비율)**: 로컬 메모리 접근 지연시간 대비 다른 소켓의 원격 메모리(Remote Memory) 접근 지연시간의 비율(보통 1.5배~2.5배 수준).

</details>

- 다수의 CPU 코어가 분산된 물리 메모리를 단일 주소 공간으로 투명하게 공유하는 **대칭형 다중 처리(SMP) 단일 OS 뷰**
- 하드웨어 디렉터리 프로토콜 기반으로 소켓 간 캐시 일관성을 실시간 유지하는 **ccNUMA 아키텍처**
- 로컬 메모리 접근($\sim 80\,\text{ns}$) 대비 원격 메모리 접근($\sim 140\,\text{ns}$) 시 발생하는 **NUMA Ratio 지연시간 불균형 관리**

#### 한줄 요약

- **단일 OS 통합 가상 메모리 뷰(SMP)·ccNUMA 하드웨어 캐시 일관성·로컬 대비 원격 메모리 지연 비율(NUMA Ratio: 1.5~2.5x) 관리**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NUMA Node**: 단일 CPU 소켓 내부의 코어들과 해당 소켓의 메모리 컨트롤러에 직결된 로컬 DRAM 뱅크의 결합 단위.
- **First-Touch Allocation**: 프로세스가 메모리를 동적 할당할 때 실제 페이지에 첫 쓰기(Write)를 수행한 스레드가 속한 로컬 NUMA 노드의 메모리에 우선 배치하는 커널 메모리 정책.

</details>

```text
[ 2-Socket ccNUMA 멀티소켓 서버 하드웨어 아키텍처 ]
┌──────────────────────────────┐        ┌──────────────────────────────┐
│ NUMA 노드 0 (Socket 0)       │        │ NUMA 노드 1 (Socket 1)       │
│  ├─ CPU Core 0 ~ 63 (L3 캐시)│        │  ├─ CPU Core 64 ~ 127 (L3)   │
│  ├─ 로컬 메모리 컨트롤러 (DDR)│        │  ├─ 로컬 메모리 컨트롤러 (DDR)│
│  └─ PCIe Root Complex 0      │        │  └─ PCIe Root Complex 1      │
└──────────────┬───────────────┘        └──────────────┬───────────────┘
               │                                       │
               │ [ 로컬 DRAM 0 ]                       │ [ 로컬 DRAM 1 ]
               │ (Local: ~80ns)                        │ (Local: ~80ns)
               ▼                                       ▼
┌──────────────┴───────────────────────────────────────┴──────────────┐
│ 소켓 간 인터커넥트 패브릭 (Intel UPI / AMD Infinity Fabric: ~140ns) │
└─────────────────────────────────────────────────────────────────────┘
```

선의 의미: NUMA 노드 0(CPU+Local DRAM), NUMA 노드 1(CPU+Local DRAM), 소켓 간 인터커넥트(UPI/IF) 및 OS NUMA 스케줄러 간의 아키텍처 구조도.

| 구성요소 | 책임 |
|:---|:---|
| NUMA 노드(Socket) | CPU 코어 그룹과 해당 소켓의 메모리 컨트롤러에 직결된 로컬 DRAM으로 구성된 기본 단위 |
| 인터커넥트 패브릭 | 소켓 간 원격 메모리 I/O 데이터 전송 및 캐시 일관성 스눕(Snoop) 프로토콜을 처리하는 고속 점대점 링크 |
| OS NUMA 스케줄러 | First-Touch 할당 정책 및 AutoNUMA 페이지 마이그레이션을 통해 메모리 지역성을 최적화하는 스케줄러 |
| PCIe I/O 서브시스템 | 소켓별 Root Complex에 직결되어 각 NUMA 노드에 로컬화된 고속 I/O 디바이스(NIC, NVMe) 통제 |

#### 한줄 요약

- **NUMA 노드(Socket+Local DRAM)·소켓 간 인터커넥트 패브릭(UPI/IF)·OS NUMA 스케줄러·소켓별 PCIe I/O 컨트롤러**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **numactl / CPU Affinity**: 특정 프로세스나 스레드를 지정된 CPU 코어 및 로컬 NUMA 메모리 노드에 강제로 결박(Binding)하여 원격 접근을 차단하는 튜닝 툴.

</details>

```text
[ 멀티소켓 NUMA 메모리 할당 및 스케줄링 흐름 ]
                         │
                         ▼
   [ 1. 애플리케이션 기동 시 numactl 로 특정 NUMA 노드(예: 노드 0)에 바인딩 ]
                         │
                         ▼
   [ 2. 스레드가 메모리 할당 요청 ──> First-Touch 정책에 의해 로컬 DRAM 0 에 적재 ]
                         │
        +────────────────┴────────────────────────+
        │             [ 메모리 접근 위치 판정 ]   │
        │             /                         \ │
        │     [ 로컬 DRAM 0 접근 ]            [ 원격 DRAM 1 접근 ]
        │            │                                │
        │     로컬 버스 직접 인출             3. 소켓 간 인터커넥트(UPI) 경유
        │     (지연시간: ~80ns)               원격 패킷 전송 (지연: ~140ns)
        +────────────────┬────────────────────────+
                         │
                         ▼
   [ 4. AutoNUMA 커널 데몬이 원격 접근 감지 시 페이지를 로컬 노드로 마이그레이션 ]
```

**동작 원리**

1. **스레드 바인딩**: `numactl --cpunodebind=0 --membind=0` 명령으로 프로세스를 소켓 0에 고정
2. **로컬 메모리 할당**: First-Touch 커널 메커니즘에 의해 소켓 0에 직결된 로컬 DDR 메모리에 물리 페이지 할당
3. **메모리 I/O 처리**: 로컬 접근은 내부 크로스바로 즉시 인출, 원격 접근은 UPI 인터커넥트를 통해 패킷 통신
4. **자동 마이그레이션**: Linux AutoNUMA가 힌트 페이지 폴트를 통해 원격 접근 빈도를 모니터링하여 데이터 페이지를 스레드 근처로 이동

#### 한줄 요약

- 스레드 NUMA 노드 바인딩(CPU Affinity) $\to$ **First-Touch 로컬 메모리 우선 할당 $\to$ 로컬 vs 원격(Remote) 메모리 I/O 감시 $\to$ AutoNUMA 페이지 마이그레이션 $\to$ 캐시 일관성 유지 완료**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **ccNUMA vs 1-Socket UMA vs Cluster MPP**:
  - ccNUMA: 다중 소켓 단일 OS, 공유 메모리(수 TB), 하드웨어 캐시 일관성, 원격 지연 존재
  - 1-Socket UMA: 단일 CPU, 균일 메모리 접근, 최소 지연, 확장성 한계
  - Cluster MPP: 독립 노드 클러스터(Shared-Nothing), 네트워크 메시지 전달, 무제한 확장

</details>

| 비교 항목 | 멀티소켓 서버 (ccNUMA / SMP) | 단일 소켓 서버 (1-Socket UMA) | 분산 클러스터 (MPP / Scale-Out) |
|:---|:---|:---|:---|
| 메모리 구조 및 일관성 | 물리 분산, 논리 단일 공유 메모리 (하드웨어 ccNUMA) | 균일 메모리 접근 (UMA), 단일 소켓 내 캐시 일관성 | 비공유(Shared-Nothing) 구조, 네트워크 메시지 전달 |
| 최대 확장성 및 지연시간 | 수 TB 메모리 및 수백 코어 (원격 메모리 지연 존재) | 단일 CPU 용량 한계 (초저지연 균일 접근) | 수천 대 노드 무제한 확장 (네트워크 지연 발생) |
| 한계 및 주 적용 분야 | NUMA 원격 접근 병목 및 고비용 (대규모 인메모리 DB) | 확장성 한계 (일반 웹서버, 마이크로서비스) | 분산 프로그래밍 복잡도 (빅데이터 분석, HPC) |

#### 한줄 요약

- 대용량 단일 메모리는 **멀티소켓(ccNUMA)**, 균일 저지연은 **단일 소켓(UMA)**, 대규모 확장은 **분산 클러스터(MPP)**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **False Sharing(거짓 공유)**: 서로 다른 코어가 사용하는 독립된 변수들이 동일한 64바이트 캐시 라인에 위치하여 캐시 무효화 트래픽이 폭증하는 현상.
- **vNUMA(Virtual NUMA)**: 가상 머신에 물리 서버의 NUMA 토폴로지를 그대로 노출하여 게스트 OS가 로컬 메모리를 최적 활용하도록 돕는 가상화 기술.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 스레드의 소켓 간 잦은 마이그레이션으로 인한 원격 메모리 접근(Remote Access) 지연시간 급증 | **numactl / taskset 기반 CPU 코어 및 NUMA 노드 바인딩(Pinning)** 적용 | 메모리 접근 지역성(Locality) 극대화 및 소켓 간 인터커넥트 병목 방지 |
| 서로 다른 코어의 독립 변수가 동일 캐시 라인(64B)에 위치하여 발생하는 거짓 공유(False Sharing) | **64바이트 단위 데이터 구조체 캐시 라인 정렬(Align) 및 패딩(Padding)** 적용 | 소켓 간 불필요한 캐시 무효화(Invalidation) 트래픽 차단 |
| 가상 머신(VM) 메모리가 복수 NUMA 노드에 걸쳐 분산 할당되어 발생하는 게스트 성능 저하 | 하이퍼바이저 상에서 **vNUMA 토폴로지 매핑 및 vCPU-물리 NUMA 노드 일치(Pinning)** | 가상화 환경에서의 원격 메모리 지연 극소화 및 네이티브급 성능 확보 |

#### 한줄 요약

- **numactl 기반 CPU & Memory 노드 바인딩·64바이트 캐시 라인 패딩(False Sharing 방지)·하이퍼바이저 vNUMA 토폴로지 일치**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **CXL 기반 메모리 확장으로의 진화**: 기존 독자 인터커넥트(UPI)에 더해 CXL.mem 프로토콜을 활용하여 이종 가속기 및 대용량 풀링 메모리를 멀티소켓 SMP 환경에 유연하게 결합하는 추세.

</details>

- 미션 크리티컬 DB 및 AI 거대 모델 학습 시스템에서 **2-Socket/4-Socket ccNUMA 서버 표준 채택 및 CXL 기반 메모리 풀링 확장 결합**

#### 한줄 요약

- **메모리 지역성(Locality) 극대화와 소켓 간 인터커넥트 최적화**를 통한 멀티소켓 확장
