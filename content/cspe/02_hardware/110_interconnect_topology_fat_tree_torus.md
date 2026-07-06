---
title: "인터커넥트 토폴로지 — 팻트리·토러스 (Interconnect Topology Fat Tree Torus)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 110
---

## 미리 알고가기

- 토폴로지: 노드와 링크가 어떤 구조로 연결되는지를 나타내는 네트워크 형태임
- 팻트리: 상위 계층으로 갈수록 더 넓은 대역폭을 제공해 병목을 줄이는 트리형 구조임
- 토러스: 노드를 격자로 배치하고 양 끝을 연결해 순환 경로를 만든 구조임
- HPC(High Performance Computing): 대규모 병렬 계산을 수행하는 고성능 컴퓨팅 환경임
- Bisection Bandwidth: 네트워크를 둘로 나눴을 때 양쪽 사이를 연결하는 총 대역폭임

## Ⅰ. 개요

- **정의**: 인터커넥트 토폴로지는 서버, 스위치, 가속기, 노드가 링크로 연결되는 구조이며, 팻트리와 토러스는 각각 계층적 무차단 대역폭과 규칙적 근접 연결을 목표로 하는 대표 구조임.
- **배경/필요성**: HPC, AI(Artificial Intelligence) 클러스터, 데이터센터의 대규모 병렬 시스템은 연산 성능보다 노드 간 통신 지연과 대역폭이 전체 처리 시간을 제한할 수 있음. 토폴로지 선택은 collective communication, shuffle, nearest-neighbor 계산의 성능과 비용을 직접 좌우함.
- **비유**: 팻트리는 큰 간선도로를 계층적으로 넓히는 도시 도로망이고, 토러스는 격자형 골목을 순환 연결한 계획도시와 같음.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 대규모 병렬 시스템 네트워크 설계 | fat tree, torus, latency, bisection bandwidth, traffic pattern | 단순 네트워크 모양 설명 |

> 요약: 인터커넥트 토폴로지는 통신 패턴에 맞춰 지연, 대역폭, 비용, 장애 경로를 선택하는 설계 기준임.

## Ⅱ. 특징/비교

| 판단 기준 | 팻트리 | 토러스 |
|:---|:---|:---|
| 구조 | edge-aggregation-core 계층으로 상위 대역폭 확장 | 2D/3D 격자 노드를 양 끝 순환 연결 |
| 대역폭 특성 | 설계에 따라 높은 bisection bandwidth 제공 | 인접 통신에 강하지만 전역 통신은 hop 증가 |
| 비용 | 스위치와 케이블 수가 많아질 수 있음 | 규칙적 배선으로 확장 예측이 쉬움 |
| 적합 패턴 | AI all-reduce, 데이터센터 east-west traffic | stencil, mesh simulation, HPC 근접 통신 |

> 요약: 팻트리는 전역 통신 대역폭, 토러스는 규칙적 근접 통신과 비용 효율을 우선함.

## Ⅲ. 구성요소

```text
Fat tree:
              +------+
              | Core |
              +------+
             /        \
        +------+    +------+
        | Agg  |    | Agg  |
        +------+    +------+
        /   \        /   \
     +---+ +---+  +---+ +---+
     |N1 | |N2 |  |N3 | |N4 |
     +---+ +---+  +---+ +---+

Torus:
     +---+---+---+
     |N1 |N2 |N3 |
     +---+---+---+
      |   |   |
     +---+---+---+
     |N4 |N5 |N6 |
     +---+---+---+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| 노드 | 서버, GPU(Graphics Processing Unit), 스토리지, 계산 장치처럼 통신의 말단임 | 도시의 건물 |
| 링크 | 노드와 스위치 사이 데이터가 이동하는 물리·논리 경로임 | 도로 |
| 스위치·라우터 | 패킷을 목적지 방향으로 전달하고 혼잡을 제어함 | 교차로 관제 |
| 라우팅 정책 | 경로 선택, 부하 분산, 장애 우회를 결정함 | 내비게이션 규칙 |

> 요약: 토폴로지는 노드, 링크, 스위치, 라우팅 정책이 결합해 통신 성능을 결정하는 구조임.

## Ⅳ. 절차

```text
+----------+      +----------+      +----------+      +----------+
| Profile  | ---> | Select   | ---> | Plan     | ---> | Validate |
+----------+      +----------+      +----------+      +----------+
```

1. **통신 패턴 분석** — all-to-all, all-reduce, nearest-neighbor, storage traffic 비중을 파악함
2. **토폴로지 선택** — 전역 대역폭은 팻트리, 규칙적 근접 통신은 토러스 계열을 우선 검토함
3. **경로·용량 설계** — bisection bandwidth, oversubscription, hop count, 케이블 길이를 산정함
4. **운영 검증** — 장애 우회, 혼잡 제어, collective 성능, link utilization을 측정함

> 요약: 토폴로지 설계는 워크로드 통신 패턴을 기준으로 구조와 용량을 선택한 뒤 실측으로 검증함.

## Ⅴ. 문제점

- **P1 트래픽 패턴 불일치**: 토폴로지와 워크로드 통신 패턴이 맞지 않으면 특정 링크에 혼잡이 집중됨
- **P2 케이블·포트 비용**: 고대역폭 팻트리는 스위치 포트와 케이블 수가 급증해 구축 비용과 장애 지점이 늘어남
- **P3 장애 영향 경로**: 토러스나 oversubscribed 구조에서는 일부 링크 장애가 우회 경로 지연과 혼잡을 크게 만들 수 있음

> 요약: 토폴로지 문제는 평균 대역폭보다 패턴 적합성, 물리 구축 비용, 장애 시 경로 변화에서 발생함.

## Ⅵ. 개선방안

- **P1 대응**: workload trace 기반 시뮬레이션과 topology-aware scheduling으로 통신이 가까운 노드를 함께 배치함 (확인: link hotspot count)
- **P2 대응**: oversubscription ratio, cable plan, port speed를 TCO(Total Cost of Ownership) 기준으로 최적화함 (확인: cost per effective bandwidth)
- **P3 대응**: adaptive routing, redundant link, failure domain 설계와 장애 훈련을 적용함 (확인: degraded throughput)

> 요약: 인터커넥트 개선은 토폴로지 자체보다 워크로드 배치와 장애 시 경로 제어를 포함해야 함.

## Ⅶ. 전망

- **발전 방향**: InfiniBand, Ethernet fabric, NVLink/NVSwitch, optical interconnect가 결합해 AI 클러스터용 계층형 토폴로지가 고도화됨
- **기술사적 판단**: 네트워크 설계는 포트 속도보다 collective 성능, bisection bandwidth, 장애 격리, 증설 단위를 기준으로 평가해야 함
- **기술사 제언**: 대규모 클러스터는 애플리케이션 통신 trace를 기반으로 토폴로지를 선정하고, link utilization과 collective latency를 운영 SLO(Service Level Objective)로 관리해야 함
