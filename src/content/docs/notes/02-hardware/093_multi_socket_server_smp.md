---
sidebar:
  order: 93
  label: "093. 멀티소켓 서버•SMP (Multi-Socket Server•SMP)"
  badge:
    text: "미출 • 50%"
    variant: note
title: "멀티소켓 서버•SMP (Multi-Socket Server•SMP)"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **Multi-Socket Server**: 단일 파워 메인보드 상에 2개 이상의 독립 물리 CPU 소켓(2P, 4P, 8P)을 장착하여 고성능 연산 및 메모리 대역폭을 확장하는 서버 시스템.
- **SMP(Symmetric Multiprocessing)**: 여러 개의 CPU 소켓 코어들이 하나의 대칭적 메모리 공간과 OS 커널을 대등하게 공유하여 명령을 병렬 수행하는 아키텍처.
- **ccNUMA(Cache-Coherent Non-Uniform Memory Access)**: 각 CPU 소켓이 로컬 DRAM 메인보드 선로를 보유하되, 칩 간 고속 전용 인터커넥트(UPI/Infinity Fabric)를 통해 타 소켓 메모리를 일관성(Coherency) 있게 억세스하는 기술.

</details>

- 정의/개념: 단일 메인보드 하드웨어 상에서 복수 소켓 CPU 및 독립 로컬 메모리를 고속 인터커넥트 패브릭으로 결합 대칭 연동하는 **멀티소켓 서버 & SMP**
- 배경/필요성: 단일 CPU 소켓 코어 수, 핀 수 및 로컬 메인보드 메모리 채널 한계 극복을 통한 엔터프라이즈 멀티태스킹 대역폭 확장 요구성

#### 한줄 요약

- NUMA는 소켓별 로컬 메모리와 인터커넥트 원격 접근을 결합한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Interconnect Fabric(UPI/Infinity Fabric)**: 소켓 간 캐시 일관성 패킷, 원격 메모리 억세스 및 I/O 억세스를 초저지연 시리얼 전송하는 소켓 인터페이스 (Intel UPI, AMD Infinity Fabric).
- **Local vs Remote Access**: CPU가 본인 소켓 전용 DRAM 억세스(Local, ~80ns) 시와 타 소켓 패브릭을 경유한 DRAM 억세스(Remote, ~140ns) 시 발생하는 지연시간 및 대역폭의 불균형 속성.

</details>

- 소켓 당 독립 8채널 LPDDR/DDR5 메모리 통로를 통합 제공하는 **SMP** 확장성
- **ccNUMA** 아키텍처 수용을 통한 소켓 간 주소 공간 통합 및 캐시 일관성 유지
- 소켓 간 **Interconnect Fabric(UPI)** 레이어 병목으로 인한 **Local vs Remote Access** 레이턴시 편차 극복 과제

#### 한줄 요약

- 원격 메모리 접근과 공유 쓰기 증가에 따른 지연•캐시 일관성 트래픽이 핵심이다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **NUMA Node**: 1개의 물리 CPU 소켓 코어 그룹, L1/L2/L3 캐시, 메모리 컨트롤러 및 1차 파티션 로컬 DRAM으로 구성된 단위 블록.
- **First-Touch Allocation**: OS 커널 상에서 메모리 페이지를 최초 할당 시 해당 요청을 발생시킨 CPU 코어의 로컬 NUMA Node DRAM에 최우선 할당하는 물리 정책.

</details>

```text
운영체제 NUMA 정책
└─ NUMA 노드 집합
   ├─ 소켓•캐시•로컬 메모리 × N
   └─ 일관성 인터커넥트
```

선의 의미: OS 커널 NUMA 스케줄러 정책 하에 소켓별 NUMA Node(CPU+DRAM) 집합이 소켓 간 인터커넥트 패브릭을 통해 1개 시스템으로 결합되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| NUMA Node (Socket 0/1) | 로컬 CPU 코어 연산, L3 캐시 및 전용 로컬 DRAM 메모리 인터페이스 제어 |
| Interconnect Fabric | 소켓 간 **UPI/Infinity Fabric** 링크 형성, Snoop 프로토콜 패킷 및 원격 DMA 수송 |
| OS NUMA Scheduler | **First-Touch Allocation** 정책 기반 프로세스 - DRAM 물리 할당 및 코어 affinity 제어 |
| I/O Subsystem | 소켓별 배치된 PCIe Gen5 / CXL 슬롯 라우팅 및 NUMA 노드 차원 I/O 맵핑 |

#### 한줄 요약

- 운영체제 NUMA 정책, NUMA 노드 집합, 일관성 인터커넥트의 구조이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Numactl / CPU Affinity**: 특정 멀티소켓 OS 런타임 상에서 프로세스 스레드 및 메모리 영역을 특정 NUMA 노드 코어 및 DRAM으로 강제 바인딩 고정하는 Linux 도구/기능.

</details>

```text
[워크로드 스레드•데이터]
          │
          ▼
1. CPU 선호도 설정
          │
          ▼
2. 최초 접근 페이지 배치
          │
          ▼
3. 원격 접근률 측정
      ┌────┴────────┐
      │ 낮음        │ 높음
      ▼             ▼
[현재 배치 유지] 4. 스레드•페이지 공동 배치
                   │
                   ▼
              5. 이동 후 재측정
                   │
                   └── 원격 접근률 측정으로 반복
```

### 동작 원리

1. **CPU 선호도 설정**: **Numactl** 및 **CPU Affinity** 설정을 통한 프로세스 타깃 NUMA Node 인가.
2. **최초 접근 페이지 배치**: **First-Touch Allocation** 구동으로 스레드가 실행되는 로컬 DRAM 상에 물리 페이지 작성.
3. **원격 접근률 측정**: **Interconnect Fabric** 레이어 상의 원격 억세스(Remote Access) 트래픽 감시.
4. **스레드·페이지 공동 배치**: 원격 트래픽 비중 우세 시 스레드 및 메모리를 1개 노드로 재배치(Auto-NUMA Balancing).
5. **이동 후 재측정**: 로컬 억세스 비율(>90%) 확보 및 레이턴시 보정 확인.

#### 한줄 요약

- 자주 함께 사용하는 스레드와 페이지에 스레드·페이지 공동 배치를 적용하고 이동 후 재측정하여 원격 메모리 접근을 줄인다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **UMA(Uniform Memory Access)**: 모든 CPU 코어가 단일 버스를 통해 모든 메모리에 동일한 지연시간으로 억세스하는 단일 소켓 아키텍처.

</details>

| 비교 항목 | 멀티소켓 ccNUMA 서버 | 단일 소켓 UMA 서버 |
|:---|:---|:---|
| 확장성 | 극대화된 코어 수 및 대용량 메모리(수 TB) 인가 | 소켓 제한으로 인한 코어 수 및 메모리 용량 한계 |
| 메모리 억세스 지연 | **Local vs Remote Access** 레이턴시 분손 발생 (~80ns vs ~140ns) | 모든 코어가 동일 전송 레이턴시 유지 (**UMA**) |
| 인터커넥트 병목 | 소켓 간 **UPI/Infinity Fabric** 패브릭 트래픽 병목 가능 | 내부 시스템 버스 전송으로 인터커넥트 병목 전무 |
| TCO 및 시스템 단가 | 고비용 메인보드, 복잡한 전력/방열 및 고가 시스템 | 저비용 단일 메인보드, 간편한 서버 구축 |

#### 한줄 요약

- 코어와 메모리 요구가 단일 소켓 안에 들면 단일 소켓을 유지하고, 초과하면 공유 주소 공간에서 로컬 메모리 접근 비율을 보존하며 멀티소켓 서버로 확장한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **False Sharing**: 서로 다른 CPU 소켓의 코어들이 동시 접근하는 데이터가 1개 64-Byte 캐시 라인 내에 겹쳐 소켓 간 Snoop 트래픽을 유발하는 캐시 무효화 문제.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 소켓 간 원격 메모리 억세스 빈발로 성능 저하 | **Numactl --physcpubind --membind** 적용 | 로컬 메모리 억세스 전환 |
| 복수 소켓 코어 간 **False Sharing** 발생으로 캐시 무효화 | **64-Byte Cache Line Padding (alignas)** 구조체 적용 | 소켓 간 캐시 트래픽 소멸 |
| VM 가상머신 자원이 소켓 0, 소켓 1에 분산 배치 | Hypervisor **vCPU - NUMA Node Pinning** 수용 | 가상화 레이턴시 최적화 |

> 사례: 4-Socket **ccNUMA** 서버 상의 In-Memory DB (SAP HANA / Oracle) NUMA 튜닝 실증

#### 한줄 요약

- CPU•메모리 선호도와 NUMA 토폴로지에 따라 빈번히 접근하는 스레드와 메모리를 같은 노드에 배치한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **멀티소켓 확장 기준(Multi-Socket Adoption Criteria)**: 업무 워크로드의 스케일아웃 vs 스케일업 요구성, NUMA 튜닝 가능성 및 TCO 단가에 기반한 수립 체계.

</details>

- **멀티소켓 확장 기준**에 따라 대용량 인메모리 DB 및 초대형 가상화 노드는 **멀티소켓 ccNUMA 서버**, 웹/애플리케이션 노드는 **단일 소켓 서버** 채택

#### 한줄 요약

- ccNUMA 메인보드 아키텍처 기반 소켓 간 UPI 인터커넥트 및 NUMA 노드 바인딩 최적화 멀티소켓 서버 구축 체계 적용.
