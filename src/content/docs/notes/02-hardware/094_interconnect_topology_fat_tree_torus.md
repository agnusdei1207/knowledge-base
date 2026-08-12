---
sidebar:
  order: 94
  label: "094. 인터커넥트 토폴로지: 팻트리•토러스 (Interconnect Topology: Fat-Tree•Torus)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "인터커넥트 토폴로지: 팻트리•토러스 (Interconnect Topology: Fat-Tree•Torus)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-hardware"
weight: 94
extra:
  question_no: "094"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "집단•인접 통신 패턴에 따른 토폴로지 선택"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Interconnect Topology**: Supercomputer 및 AI 데이터센터 내 수천~수만 개의 노드(Node)와 스위치를 결합하는 물리적/논리적 네트워크 패브릭 구조.
- **Fat-Tree**: 상위 계층(Spine/Core)으로 갈수록 대역폭 선로 수(Link)를 굵게 배치하여 1:1 무병목(Non-Blocking) 전송을 보장하는 계층형 트리 토폴로지.
- **Torus**: N차원 격자(Grid) 구조의 양 끝 노드를 순환 고리(Wraparound Link)로 직결 연계하여 인접 노드 간 초저지연 통신을 서빙하는 매시 토폴로지.

</details>

- 정의/개념: AI 대규모 클러스터 및 HPC 환경에서 데이터 패킷 분배, 양분 대역폭(Bisection Bandwidth) 및 홉(Hop) 지연시간을 결정짓는 **인터커넥트 토폴로지 (Fat-Tree vs Torus)**
- 배경/필요성: AI 딥러닝 텐서 교환(All-Reduce) 시 유발되는 네트워크 핫스팟(Hotspot) 및 병목 현상 해소 필요성

#### 한줄 요약

- 전역 집단 통신과 최근접 이웃 통신 패턴에 따라 팻트리 또는 토러스를 결정한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Bisection Bandwidth**: 전체 네트워크 노드를 임의의 1:1 반으로 분할했을 때 두 집단 간을 연결하는 최소 총 전송 대역폭.
- **Network Diameter**: 네트워크 패브릭 상에서 가장 먼 2개 노드 간을 통과할 때 소요되는 최대 홉(Hop) 수.
- **ECMP(Equal-Cost Multi-Path)**: Fat-Tree 구조 상에서 동등한 비용의 상향 경로로 패킷 트래픽을 분산 전송하는 파이프라인 로드밸런싱.

</details>

- 상위 계층 병목을 제거하여 무병목 1:1 전신 통신을 보장하는 Non-Blocking **Fat-Tree**
- 3D/6D 그리드 링 구조로 인접 노드 억세스 레이턴시를 최적화하는 **Torus**
- **Bisection Bandwidth** 극대화(Fat-Tree) vs 칩/랙 간 광케이블 배선 비용 절감(Torus)

#### 한줄 요약

- 양분 대역폭과 망 지름 및 배선 비용 사이에는 상충 관계가 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Spine/Core Switch**: Fat-Tree 계층에서 최상단에 배치되어 전체 Leaf 스위치 트래픽을 상호 라우팅하는 백본 스위치.
- **Leaf/Access Switch**: 하단 서버 노드들과 직접 1:1 연결되는 1차 접근 스위치.
- **Wraparound Link**: Torus 구조에서 맨 끝단 경계 노드를 반대편 경계 노드로 직결하여 링을 완성하는 루프 케이블.

</details>

```text
                 [연산 노드]
                  /       \
       [리프 스위치]     [토러스 라우터]
              |                 |
       [스파인 스위치]      [순환 링크]
```

선의 의미: Fat-Tree(좌측)의 Leaf-Spine 계층 경로 및 Torus(우측)의 3D/6D 라우터-Wraparound 직결 루프 경로의 인터커넥트 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| Leaf Switch | 서버 랙 노드 1:1 수용 및 상위 Spine 스위치로 **ECMP** 패킷 분산 전송 |
| Spine Switch | 하단 Leaf 스위치 간 **Non-Blocking 1:1 Bisection Bandwidth** 전송 보장 |
| Torus Router | 3D/6D 공간 좌표계 기반으로 인접 노드 주소 탐색 및 데이터 패킷 인가 |
| Wraparound Link | 경계 노드 간 바운더리 선로를 직결 링으로 묶어 **Network Diameter** 50% 단축 |

#### 한줄 요약

- 리프 스위치와 스파인 스위치의 계층 경로 및 토러스 라우터와 순환 링크의 순환 경로 구조이다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Adaptive Routing**: 네트워크 소켓 혼잡 상황을 인지하여 동적으로 비혼잡 우회 경로로 패킷을 전환하는 라우팅 기법.

</details>

```text
팻트리 경로
[출발 노드]
     │
     ▼ 1. 리프 패킷 주입
[리프 스위치]
     │
     ▼ 2. ECMP 상향 경로 선택
[스파인 스위치]
     │
     ▼ 3. 목적 리프 하향 전달
[목적 노드]

토러스 경로
[출발 노드]
     │
     ▼ 4. 목적 좌표 방향 선택
[토러스 라우터]
     │
     ▼ 5. 이웃 홉 전달
[목적 좌표 도달?]
     ├─ 아니오: 4단계로 반복
     └─ 예: [목적 노드]
```

### 동작 원리

1. **리프 패킷 주입**: Fat-Tree 상에서 출발 노드가 **Leaf Switch**로 패킷 인가.
2. **ECMP 상향 경로 선택**: **ECMP** 다중 경로 해싱을 통해 상위 **Spine Switch**로 비혼잡 상향 라우팅.
3. **목적 리프 하향 전달**: 스파인 스위치에서 목적지 Leaf 스위치 및 타깃 노드로 하향 전송.
4. **목적 좌표 방향 선택 (Torus)**: Torus 라우터에서 X, Y, Z 차원 좌표 거리 계산.
5. **이웃 홉 전달 (Torus)**: **Wraparound Link** 및 **Adaptive Routing**을 활용해 차원 단계를 밟으며 홉 전송 완결.

#### 한줄 요약

- 팻트리는 ECMP 상향 경로 선택과 목적 리프 하향 전달, 토러스는 목적 좌표 방향 선택과 이웃 홉 전달로 패킷을 전달한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **All-Reduce**: AI 딥러닝 분산 학습 시 모든 GPU의 그래디언트(Gradient) 값을 합산하여 전역 공유하는 대표적 집단 통신(Collective Comm).

</details>

| 비교 항목 | Fat-Tree (Leaf-Spine Topology) | Torus (3D / 6D Torus Topology) |
|:---|:---|:---|
| 전송 특성 | 무병목 **Non-Blocking**, 일관된 지연시간 | 최근접(Nearest-Neighbor) 노드 간 초저지연 |
| 양분 대역폭 | 최고 수치 (**1:1 Bisection Bandwidth**) | 노드 규모 확장에 따라 대역폭 한계 발생 |
| 주요 통신 패턴 | **All-Reduce** 전역 집단 통신에 최적화 | Grid 3D stencil, 차분 격자 연산에 최적화 |
| 케이블/스위치 비용| 고비용 (수많은 Spine 스위치 및 광케이블 소요) | 저비용 (인접 노드 직결 케이블로 백본 스위치 최소화) |

#### 한줄 요약

- 높은 양분 대역폭이 필요한 집단 통신에는 팻트리, 최근접 이웃 통신이 반복되는 작업에는 토러스가 유리하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Deadlock**: Torus 등의 순환 고리 토폴로지 상에서 패킷들이 상호 버퍼를 대기하며 트랜잭션이 영구 마비되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Torus 순환 패킷 경로 상의 **Deadlock** 발생 | 가상 채널(Virtual Channel) 및 순서화 라우팅 수용 | 데드락 원천 예방 |
| Fat-Tree 스위치/케이블 비용 폭증 문제 | Slim-Tree 및 1:1.5 **Oversubscription** 조절 | 구축 TCO 절감 |
| 딥러닝 **All-Reduce** 시 특정 링크 핫스팟 병목 | **Adaptive Routing** 및 In-Network Computing(SHARP) | 전역 학습 속도 향상 |

> 사례: NVIDIA **InfiniBand Fat-Tree (Dragonfly/Fat-Tree)** 및 구글 TPU **3D Torus** 구축 비교

#### 한줄 요약

- 전체 축약에는 높은 양분 대역폭과 ECMP 다중 경로를 확보한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **토폴로지 선택 기준(Interconnect Topology Selection Criteria)**: 통신 패턴(All-Reduce vs Grid), 양분 대역폭 요구, 케이블 비용에 따른 선택 체계.

</details>

- **토폴로지 선택 기준**에 따라 대규모 AI GPU 클러스터 및 LLM 학습은 **Fat-Tree (InfiniBand)**, 기상/물리 시뮬레이션 수퍼컴은 **Torus** 채택

#### 한줄 요약

- 대용량 All-Reduce 전역 집단 통신을 위한 팻트리(Fat-Tree) 및 최근접 이웃 통신을 위한 토러스(Torus) 토폴로지 최적 구축 체계 적용.
