---
sidebar:
  order: 94
  label: "094. 인터커넥트 토폴로지: 팻트리•토러스 (Interconnect Topology: Fat-Tree•Torus)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "인터커넥트 토폴로지: 팻트리•토러스 (Interconnect Topology: Fat-Tree•Torus)"
date: "2026-08-13T12:21:04+09:00"
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

<details><summary>용어 설명</summary>

- **Interconnect Topology**: Supercomputer 및 AI 데이터센터 내 수천~수만 개의 노드(Node)와 스위치를 결합하는 물리적/논리적 네트워크 패브릭 구조.
- **Fat-Tree**: 상위 계층으로 갈수록 링크 용량을 늘려 양분 대역폭을 확보하는 계층형 트리 토폴로지.
- **Torus**: N차원 격자의 양 끝 노드를 순환 링크로 연결하여 경계 없는 인접 관계를 만드는 토폴로지.

</details>

- 정의/개념: AI 대규모 클러스터 및 HPC 환경에서 데이터 패킷 분배, 양분 대역폭(Bisection Bandwidth) 및 홉(Hop) 지연시간을 결정짓는 **인터커넥트 토폴로지 **
- 배경/필요성: 단순 계층망은 대규모 집단 통신 시 **상위 링크 병목** 발생

#### 한줄 요약

- 전역 집단 통신과 최근접 이웃 통신 패턴에 따라 팻트리 또는 토러스를 결정한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Bisection Bandwidth**: 전체 네트워크 노드를 임의의 1:1 반으로 분할했을 때 두 집단 간을 연결하는 최소 총 전송 대역폭.
- **Network Diameter**: 네트워크 패브릭 상에서 가장 먼 2개 노드 간을 통과할 때 소요되는 최대 홉(Hop) 수.
- **ECMP(Equal-Cost Multi-Path)**: Fat-Tree 구조 상에서 동등한 비용의 상향 경로로 패킷 트래픽을 분산 전송하는 파이프라인 로드밸런싱.

</details>

- 충분한 상향 링크로 높은 양분 대역폭을 제공하는 **Fat-Tree**
- 다차원 격자와 순환 링크로 인접 통신을 단축하는 **Torus**
- **양분 대역폭**과 스위치•배선 비용 간 상충 관계

#### 한줄 요약

- 양분 대역폭과 망 지름 및 배선 비용 사이에는 상충 관계가 있다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

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
| Spine Switch | 하단 Leaf 간 경로 제공과 **양분 대역폭** 확보 |
| Torus Router | 다차원 좌표에 따라 다음 인접 노드 선택 |
| Wraparound Link | 반대편 경계를 연결해 **망 지름**과 경로 단축 |

#### 한줄 요약

- 리프 스위치와 스파인 스위치의 계층 경로 및 토러스 라우터와 순환 링크의 순환 경로 구조이다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Adaptive Routing**: 네트워크 소켓 혼잡 상황을 인지하여 동적으로 비혼잡 우회 경로로 패킷을 전환하는 라우팅 기법.

</details>

```text
팻트리 경로
[출발 노드]
     │
     ▼ 패킷 주입
[리프 스위치]
     │
     ▼ 1. ECMP 상향 경로 선택
[스파인 스위치]
     │
     ▼ 2. 목적 리프 하향 전달
[목적 노드]

토러스 경로
[출발 노드]
     │
     ▼ 패킷 주입
[토러스 라우터]
     │
     ▼ 3. 목적 좌표 방향 선택
[다음 홉]
     │
     ▼ 4. 이웃 홉 전달
[목적 좌표 도달?]
     ├─ 아니오: 3단계로 반복
     └─ 예: [목적 노드]
```

### 동작 원리

1. **ECMP 상향 경로 선택**: 동등 비용 경로 중 상위 스파인 선택
2. **목적 리프 하향 전달**: 목적 리프와 노드로 패킷 전달
3. **목적 좌표 방향 선택**: 현재 좌표에서 다음 차원 결정
4. **이웃 홉 전달**: 목적 도달까지 **순환 링크** 경유 반복

#### 한줄 요약

- 팻트리는 ECMP 상향 경로 선택과 목적 리프 하향 전달, 토러스는 목적 좌표 방향 선택과 이웃 홉 전달로 패킷을 전달한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **All-Reduce**: AI 딥러닝 분산 학습 시 모든 GPU의 그래디언트(Gradient) 값을 합산하여 전역 공유하는 대표적 집단 통신(Collective Comm).

</details>

| 비교 항목 | Fat-Tree (Leaf-Spine Topology) | Torus (3D / 6D Torus Topology) |
|:---|:---|:---|
| 전송 특성 | 다중 상향 경로와 높은 **양분 대역폭** | 인접 노드 간 짧은 경로 |
| 양분 대역폭 | 링크 증설로 **비차단 구성** 가능 | 차원과 규모에 따라 제한 |
| 주요 통신 패턴 | **All-Reduce** 등 전역 집단 통신 | 스텐실 등 최근접 이웃 통신 |
| 비용 구조 | 상위 스위치와 링크 비용 증가 | 노드별 다차원 링크 비용 증가 |

#### 한줄 요약

- 높은 양분 대역폭이 필요한 집단 통신에는 팻트리, 최근접 이웃 통신이 반복되는 작업에는 토러스가 유리하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Deadlock**: Torus 등의 순환 고리 토폴로지 상에서 패킷들이 상호 버퍼를 대기하며 트랜잭션이 영구 마비되는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Torus 순환 경로의 **Deadlock** 위험 | 가상 채널과 순서화 라우팅 적용 | 순환 대기 조건 차단 |
| Fat-Tree 스위치•링크 비용 증가 | 워크로드에 맞춘 **오버서브스크립션** 설계 | 구축 TCO 절감 |
| **All-Reduce** 시 특정 링크 핫스팟 | 적응형 라우팅과 망내 집계 적용 | 혼잡 분산과 통신량 감소 |

> 사례: NVIDIA **InfiniBand Fat-Tree (Dragonfly/Fat-Tree)** 및 구글 TPU **3D Torus** 구축 비교

#### 한줄 요약

- 전역 집단 통신은 **양분 대역폭**, 인접 통신은 홉 수를 우선한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **토폴로지 선택 기준(Interconnect Topology Selection Criteria)**: 통신 패턴(All-Reduce vs Grid), 양분 대역폭 요구, 케이블 비용에 따른 선택 체계.

</details>

- 전역 **집단 통신** 중심이면 Fat-Tree, 최근접 이웃 중심이면 **Torus** 선택

#### 한줄 요약

- 대용량 All-Reduce 전역 집단 통신을 위한 팻트리(Fat-Tree) 및 최근접 이웃 통신을 위한 토러스(Torus) 토폴로지 최적 구축 체계 적용.
