---
title: "NUMA 비균등 메모리 접근 (Non-Uniform Memory Access)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 26
extra:
  question_no: "026"
  exam_status: "기출"
  exam_history: "127회"
---

## 미리 알고가기

- NUMA는 코어가 어느 메모리에 접근하느냐에 따라 지연 시간이 달라지는 구조임
- local memory는 같은 소켓에 연결된 메모리이고 remote memory는 다른 소켓의 메모리임
- first-touch 정책은 최초 접근한 코어 근처에 페이지를 배치하려는 방식임

## Ⅰ. 개요

- **정의/개념**: NUMA는 여러 CPU 소켓이 각자 로컬 메모리를 가지면서도 전체 주소 공간은 공유하되, 접근 위치에 따라 메모리 지연 시간과 대역폭이 달라지는 멀티프로세서 구조임
- **배경/필요성**: 대형 SMP에서 모든 프로세서가 하나의 메모리 버스에 붙으면 확장성이 떨어지므로, 메모리 컨트롤러를 분산해 대역폭을 늘리면서 소프트웨어로 지역성을 관리하는 구조가 필요함

## Ⅱ. 특징

- 각 소켓이 로컬 메모리를 직접 제어하므로 메모리 대역폭을 수평 확장하기 좋음
- 같은 주소 공간을 유지해 프로그래밍 모델은 공유 메모리처럼 단순하게 보임
- remote access는 interconnect hop을 거쳐 local access보다 지연이 크고 변동성도 커짐
- 성능은 하드웨어보다 스레드 배치와 메모리 배치 정책에 크게 좌우됨

## Ⅲ. 종류 및 비교

| 판단 기준 | UMA | NUMA |
|:---|:---|:---|
| 메모리 지연 | 모든 코어에서 거의 동일함 | local과 remote 간 지연 차이가 큼 |
| 확장성 | 소켓 수가 늘면 메모리 병목이 커짐 | 소켓별 메모리를 분산해 확장성이 높음 |
| 소프트웨어 부담 | 배치 정책 영향이 상대적으로 작음 | 스레드와 데이터의 locality 관리가 중요함 |
| 적합 환경 | 소규모 대칭 멀티프로세서 | 대용량 서버와 in-memory 워크로드 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| CPU Socket | 연산 코어와 마지막 레벨 캐시를 포함하며 주로 자신의 로컬 메모리에 우선 접근함 |
| Local Memory Controller | 소켓에 직접 연결된 DRAM을 관리해 가장 짧은 지연 경로를 제공함 |
| Inter-Socket Interconnect | 다른 소켓 메모리에 접근할 때 요청과 응답을 전달하는 통신 경로임 |
| NUMA-Aware OS Scheduler | 스레드와 페이지를 같은 노드에 묶어 remote access를 줄이도록 배치함 |

```text
+------------+      +------------------+      +------------+
| CPU Socket0| <--> | Interconnect     | <--> | CPU Socket1|
+------------+      +------------------+      +------------+
      |                                              |
      v                                              v
+------------+                                +------------+
| Local DRAM0|                                | Local DRAM1|
+------------+                                +------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 스레드 배치 결정  | --> | 페이지 초기 배치   | --> | local 또는 remote 접근 | --> | 필요 시 재배치   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **스레드 배치 결정**: 운영체제가 실행 스레드를 특정 NUMA 노드에 배치함
2. **페이지 초기 배치**: first-touch나 정책 기반으로 메모리를 노드에 할당함
3. **local 또는 remote 접근**: 같은 노드면 짧은 지연으로 처리하고 다르면 interconnect를 거침
4. **필요 시 재배치**: 장기적으로 remote 비율이 높으면 페이지 migration이나 thread rebalance를 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 스레드와 데이터가 다른 노드에 흩어지면 remote access가 늘어 지연과 대역폭 손실이 커짐
   - 해결방안: CPU pinning과 first-touch 배치를 적용하고 remote memory access ratio와 memory latency로 검증함
2. 문제: 페이지 migration을 과도하게 수행하면 locality 개선보다 복사 비용이 더 커질 수 있음
   - 해결방안: hot page 기준으로 선별 이동하고 page migration cost와 locality gain으로 검증함
3. 문제: cross-socket 트래픽이 몰리면 interconnect 병목으로 전체 처리량이 흔들릴 수 있음
   - 해결방안: sharding과 node-local allocation을 강화하고 interconnect utilization과 throughput stability로 검증함

## Ⅶ. 적용 사례

- 인메모리 데이터베이스는 샤드와 작업 스레드를 같은 노드에 고정해 remote access를 줄이고, remote memory access ratio와 transaction latency로 결과를 확인함
- JVM 기반 대형 서비스는 GC 스레드와 heap 배치를 NUMA 인지형으로 조정해 locality를 높이고, GC pause time과 interconnect utilization로 결과를 확인함
- DPDK 네트워크 서버는 NIC와 같은 NUMA 노드에 worker를 배치해 패킷 경로를 짧게 만들고, packets per second와 memory latency로 결과를 확인함

## Ⅷ. 결론

NUMA의 핵심은 메모리를 많이 붙이는 데 있지 않고 계산과 데이터의 위치를 함께 통제해 remote access를 예외로 만드는 데 있음.
