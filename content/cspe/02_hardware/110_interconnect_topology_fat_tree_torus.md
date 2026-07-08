---
title: "인터커넥트 토폴로지 — 팻트리·토러스 (Interconnect Topology Fat Tree Torus)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 110
extra:
  question_no: "110"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- 팻트리는 상위 계층으로 갈수록 더 넓은 대역폭을 제공하는 계층형 구조임
- 토러스는 격자 노드의 양 끝을 연결해 순환 경로를 만드는 구조임
- 토폴로지 선택은 통신 패턴과 bisection bandwidth에 직접 영향을 줌

## Ⅰ. 개요

- **정의/개념**: 인터커넥트 토폴로지는 서버와 스위치와 가속기 노드가 어떤 링크 구조로 연결되는지를 뜻하며, 팻트리와 토러스는 각각 전역 대역폭과 규칙적 근접 통신을 중시하는 대표 토폴로지임
- **배경/필요성**: AI 클러스터와 HPC 시스템에서는 계산 성능보다 노드 간 통신 지연과 혼잡이 전체 처리 시간을 제한할 수 있으므로, 워크로드 통신 패턴에 맞는 토폴로지 선택이 필요함

## Ⅱ. 특징

- 팻트리는 상위로 갈수록 링크를 넓혀 전역 통신 대역폭 확보에 유리함
- 토러스는 인접 통신이 많은 격자형 계산에서 홉 예측과 배선 규칙성이 좋음
- 팻트리는 포트 수와 케이블 비용이 커질 수 있고 토러스는 전역 통신 홉 수가 늘어날 수 있음
- 토폴로지 가치는 모양 자체보다 실제 traffic pattern과 장애 우회 능력에서 결정됨

## Ⅲ. 종류 및 비교

| 판단 기준 | 팻트리 | 토러스 |
|:---|:---|:---|
| 구조 | 계층형 스위치 트리 | 2D 또는 3D 순환 격자 |
| 대역폭 특성 | 높은 bisection bandwidth 확보 가능 | 인접 통신 효율 우수 |
| 비용 구조 | 포트와 케이블 비용 증가 가능 | 규칙적 배선으로 확장 예측 쉬움 |
| 적합 패턴 | all-reduce, east-west traffic | stencil, nearest-neighbor 연산 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Compute Node | 서버와 GPU 노드가 실제 계산과 통신의 말단이 되어 트래픽 패턴을 형성함 |
| Link | 노드와 스위치를 잇는 물리 경로로 지연과 혼잡과 장애 우회 능력을 결정함 |
| Switch or Router | 패킷을 적절한 경로로 전달하며 팻트리에서는 계층 대역폭 구조를 형성함 |
| Routing Policy | 경로 선택과 부하 분산과 장애 우회를 담당해 같은 토폴로지라도 성능 차이를 만듦 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 패턴 분석      | --> | 토폴로지 선택 | --> | 용량 설계      | --> | 혼잡 검증      |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **패턴 분석**: all-to-all과 all-reduce와 nearest-neighbor 비중을 파악함
2. **토폴로지 선택**: 전역 통신이 크면 팻트리, 근접 통신이 크면 토러스를 우선 검토함
3. **용량 설계**: bisection bandwidth와 hop count와 oversubscription을 산정함
4. **혼잡 검증**: 실제 트래픽과 장애 시나리오로 링크 병목과 우회 성능을 측정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 워크로드 통신 패턴과 맞지 않는 토폴로지를 고르면 일부 링크에 혼잡이 집중될 수 있음
   - 해결방안: trace 기반 시뮬레이션과 topology-aware scheduling을 적용하고 link hotspot count와 collective latency로 검증함
2. 문제: 팻트리는 스위치 포트와 케이블 수가 급증해 구축 비용과 장애 지점이 커질 수 있음
   - 해결방안: oversubscription과 증설 단위를 함께 설계하고 cost per effective bandwidth와 cable complexity로 검증함
3. 문제: 토러스나 저오버헤드 구조는 일부 링크 장애 시 우회 경로 지연이 급격히 증가할 수 있음
   - 해결방안: adaptive routing과 장애 훈련을 적용하고 degraded throughput과 failover reroute time으로 검증함

## Ⅶ. 적용 사례

- AI 학습 클러스터에서는 팻트리 기반 fabric을 사용하고 확인 지표는 collective latency와 bisection bandwidth utilization임
- HPC 시뮬레이션 환경에서는 토러스 구조를 배치하고 확인 지표는 hop count와 link hotspot count임
- 데이터센터 증설 검토에서는 토폴로지별 비용과 장애 영향을 비교하고 확인 지표는 cost per effective bandwidth와 degraded throughput임

## Ⅷ. 결론

인터커넥트 토폴로지는 네트워크 모양 선택이 아니라 통신 패턴과 비용과 장애 우회 능력을 함께 맞추는 시스템 설계 문제임.
