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
- 로컬 메모리는 같은 소켓에 연결된 메모리이고 원격 메모리는 다른 소켓의 메모리임
- 최초 접근 정책은 처음 접근한 코어 근처에 페이지를 배치하는 방식임

## Ⅰ. 개요

- **정의/개념**: NUMA는 여러 CPU 소켓이 각자 로컬 메모리를 가지면서도 전체 주소 공간은 공유하되, 접근 위치에 따라 메모리 지연 시간과 대역폭이 달라지는 멀티프로세서 구조임
- **배경/필요성**: 대형 SMP의 공유 메모리 버스 병목을 줄이기 위해 메모리 제어기와 접근 경로를 분산하는 구조가 필요함

## Ⅱ. 특징

- 소켓을 추가하면 로컬 메모리 컨트롤러와 메모리 채널도 늘어나 전체 메모리 대역폭이 증가함
- 같은 주소 공간을 유지해 공유 메모리 프로그래밍 모델을 제공함
- 원격 접근은 인터커넥트 경유로 로컬 접근보다 지연이 크고 변동성도 커짐
- 성능은 하드웨어보다 스레드 배치와 메모리 배치 정책에 좌우됨

## Ⅲ. 종류 및 비교

| 판단 기준 | UMA | NUMA |
|:---|:---|:---|
| 메모리 지연 | 모든 코어에서 거의 동일함 | local과 remote 간 지연 차이가 큼 |
| 확장성 | 소켓 수가 늘면 메모리 병목이 커짐 | 소켓별 메모리를 분산해 확장성이 높음 |
| 소프트웨어 부담 | 배치 정책 영향이 상대적으로 작음 | 스레드와 데이터의 locality 관리가 중요함 |
| 적합 환경 | 소규모 대칭 멀티프로세서 | 대용량 서버와 in-memory 워크로드 |

> 요약: UMA는 접근 지연이 균일하고, NUMA는 확장성을 얻는 대신 locality 관리가 필요함.

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

> 요약: NUMA는 소켓별 로컬 메모리와 interconnect로 대역폭을 늘리되 remote access 비용을 감수함.

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

> 요약: NUMA 성능은 스레드와 페이지를 같은 노드에 배치해 remote access를 줄이는 데 달려 있음.

## Ⅵ. 실무 적용 및 유의점

1. 스레드와 데이터가 다른 노드에 흩어지면 remote access가 늘어나므로 CPU pinning과 first-touch 배치를 적용하고 remote memory access ratio, memory latency로 확인함
2. page migration이 과도하면 locality 이득보다 복사 비용이 커지므로 hot page만 선별 이동하고 page migration cost, locality gain으로 확인함
3. cross-socket 트래픽이 몰리면 interconnect 병목이 생기므로 sharding과 node-local allocation을 적용하고 interconnect utilization, throughput stability로 확인함

## Ⅶ. 결론

NUMA는 메모리를 많이 붙이는 구조가 아니라 계산과 데이터를 같은 노드에 묶어 remote access를 예외로 만드는 구조임.

## 작성 근거(검토용)

- NUMA는 소켓 수보다 local·remote 지연 차이와 locality 배치 정책을 중심으로 설명함
- 모호한 표현은 remote memory access ratio, page migration cost, interconnect utilization으로 구체화함
- 결론은 메모리 확장보다 계산과 데이터 위치 통제로 정리함
