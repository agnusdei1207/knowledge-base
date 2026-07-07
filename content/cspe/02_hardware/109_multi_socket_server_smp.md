---
title: "멀티소켓 서버·SMP (Multi-Socket Server SMP)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 109
---

# 멀티소켓 서버·SMP (Multi-Socket Server SMP)

## 미리 알고가기

- 소켓: CPU(Central Processing Unit) 패키지가 장착되는 물리 단위임
- SMP(Symmetric Multiprocessing): 여러 프로세서가 하나의 OS(Operating System)와 공유 메모리 공간을 대칭적으로 사용하는 구조임
- NUMA(Non-Uniform Memory Access): 소켓별 로컬 메모리와 원격 메모리 접근 지연이 다른 구조임
- LLC(Last-Level Cache): 코어들이 메모리 접근 전 마지막으로 공유하거나 참조하는 캐시 계층임
- 캐시 일관성: 여러 CPU 캐시가 같은 메모리 값을 일관되게 보이도록 하는 규칙임

## 1. 개요

- **정의/개념**: 멀티소켓 서버·SMP는 둘 이상의 CPU 소켓이 하나의 시스템 이미지와 공유 메모리 공간을 구성해 병렬 처리 능력과 메모리 용량을 확장하는 서버 구조임.
- **배경/필요성**: 단일 CPU의 코어 수, 메모리 채널, I/O(Input/Output) lane은 물리적으로 제한되어 대형 데이터베이스, 가상화, 메모리 집약 업무 요구를 모두 수용하기 어려움. 여러 소켓을 연결하면 코어와 메모리를 늘릴 수 있지만 원격 접근 지연과 일관성 비용을 관리해야 함.
- **비유**: 여러 작업장이 하나의 공장처럼 움직이지만, 자기 창고와 남의 창고 사이 이동 시간이 다른 구조임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 서버 확장 구조와 NUMA 영향 판단 | SMP, socket, shared memory, cache coherence, NUMA | 단순 코어 수 증가로만 설명 |

> 요약: 멀티소켓 SMP는 CPU와 메모리 용량을 확장하지만 NUMA와 일관성 비용을 함께 관리해야 함.

## 2. 특징 및 비교

| 판단 기준 | 단일소켓 서버 | 멀티소켓 SMP |
|:---|:---|:---|
| 확장 자원 | 한 CPU의 코어, 메모리 채널, I/O lane에 제한됨 | 여러 소켓의 코어·메모리·I/O를 결합함 |
| 메모리 접근 | 지연이 비교적 균일함 | 로컬/원격 메모리 지연 차이가 발생함 |
| 운영 편의 | 구조가 단순하고 튜닝 부담이 낮음 | OS scheduling, NUMA placement 튜닝 필요 |
| 적합 업무 | 일반 웹, 중소형 DB(Database), 단일 노드 서비스 | 대형 DB, ERP(Enterprise Resource Planning), 가상화, 인메모리 분석 |

> 요약: 멀티소켓은 수직 확장을 제공하지만 워크로드가 NUMA 비용을 감당할 때 효과적임.

## 3. 구성요소/구조

```text
+-----------+        +-----------+
| Socket 0  | <----> | Socket 1  |
| Core/LLC  |        | Core/LLC  |
+-----------+        +-----------+
     |                    |
     v                    v
+-----------+        +-----------+
| Memory    |        | Memory    |
+-----------+        +-----------+
        \              /
         v            v
       +----------------+
       | OS SMP image   |
       +----------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| CPU 소켓 | 코어, 캐시, 메모리 컨트롤러, I/O root complex를 포함함 | 작업장 |
| 소켓 간 링크 | UPI(Ultra Path Interconnect), Infinity Fabric 등으로 소켓 간 캐시 일관성과 데이터 이동을 지원함 | 작업장 연결 통로 |
| 로컬 메모리 | 각 소켓에 직접 연결된 메모리 채널로 낮은 지연을 제공함 | 가까운 창고 |
| OS 스케줄러 | 스레드와 메모리를 NUMA 노드에 배치하고 부하를 조정함 | 공장 배치 관리자 |

> 요약: 멀티소켓 SMP는 소켓, 로컬 메모리, 소켓 간 링크, OS 배치 정책이 함께 동작함.

### 원리/흐름도

```text
+----------+      +----------+      +----------+      +----------+
| Boot     | ---> | Place    | ---> | Execute  | ---> | Tune     |
+----------+      +----------+      +----------+      +----------+
```

1. **부팅 인식** — BIOS(Basic Input/Output System)/OS가 소켓, NUMA 노드, 메모리, I/O topology를 탐지함
2. **자원 배치** — 스레드, 메모리 페이지, interrupt, PCIe(Peripheral Component Interconnect Express) 장치를 적절한 NUMA 노드에 배치함
3. **병렬 실행** — 여러 소켓의 코어가 공유 주소 공간에서 작업을 병렬 수행함
4. **성능 조정** — 원격 메모리 접근, lock contention, cache coherence traffic을 모니터링해 튜닝함

> 요약: 멀티소켓 운영은 자원 인식 후 NUMA locality를 유지하며 병렬 실행을 조정하는 과정임.

## 4. 문제점 및 개선방안

- **P1 원격 메모리 지연**: 스레드가 다른 소켓 메모리에 자주 접근하면 latency와 inter-socket traffic이 증가함
- **P1 대응**: NUMA-aware scheduling, memory binding, first-touch 정책으로 로컬 접근을 늘림 (확인: remote memory access ratio)
- **P2 일관성 트래픽 증가**: 공유 데이터와 lock 경합이 많으면 cache coherence 메시지가 성능을 제한함
- **P2 대응**: lock sharding, per-socket queue, read-mostly data 복제로 일관성 트래픽을 줄임 (확인: inter-socket bandwidth)
- **P3 라이선스·전력 비용**: 소켓 수 기반 라이선스와 높은 전력·냉각 요구가 총비용을 증가시킴
- **P3 대응**: scale-up과 scale-out TCO(Total Cost of Ownership)를 비교하고 workload별 소켓 수 표준을 정함 (확인: cost per transaction)

> 요약: 멀티소켓의 병목은 코어 부족보다 NUMA locality, 공유 데이터, 비용 구조에서 발생하며 배치와 비용 평가로 통제해야 함.

## 5. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 대형 DB(Database) 서버 | DB 프로세스와 buffer pool을 NUMA(Non-Uniform Memory Access) 노드에 맞춰 배치해 원격 메모리 접근을 줄임 | remote memory access ratio, p99 latency |
| 가상화 호스트 | VM(Virtual Machine)의 vCPU(Virtual CPU), 메모리, PCIe(Peripheral Component Interconnect Express) 장치를 같은 소켓에 가깝게 배치함 | CPU ready time, inter-socket bandwidth |
| 상용 소프트웨어 플랫폼 | 소켓 수 기반 라이선스와 전력 비용을 scale-out 대안과 비교해 표준 서버 구성을 정함 | cost per transaction, power draw |

> 요약: 실무에서는 소켓 수 증가가 아니라 NUMA 배치 효과와 총비용을 측정해 멀티소켓 도입을 판단함.

## 6. 결론

- **발전 방향**: chiplet CPU, CXL(Compute Express Link) memory, composable infrastructure와 결합해 소켓 내부·외부 자원 경계가 더 유연해짐
- **기술사적 판단**: 대형 서버 선택은 최대 소켓 수보다 workload의 NUMA 민감도, 라이선스 정책, 장애 영향 범위를 기준으로 해야 함
- **기술사 제언**: 성능 시험에는 단일 스레드와 총 처리량뿐 아니라 NUMA별 메모리 접근과 inter-socket traffic 지표를 포함해야 함
