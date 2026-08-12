---
sidebar:
  order: 154
  label: "154. 쿠버네티스 Pod 스케줄링 (Kubernetes Pod Scheduling)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "쿠버네티스 Pod 스케줄링 (Kubernetes Pod Scheduling)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 154
extra:
  question_no: "154"
  source_status: "기출"
  source_history: "135회"
  priority: 70
  priority_note: "배치 조건•우선순위•축출 판단이 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Kubernetes Pod Scheduling (스케줄링)**: `kube-scheduler`가 생성 요청된 미배치(Pending) Pod를 수많은 Worker Node 중에서 리소스 여유, Taints/Tolerations, Affinity/Anti-affinity 규칙을 평가하여 가장 적합한 최적 Node로 배치 바인딩(Binding)하는 프로세스.
- **Filtering & Scoring**: 스케줄러의 2단계 알고리즘으로, 1단계 Filtering(부적합 노드 걸러내기) 후 2단계 Scoring(가장 점수가 높은 노드 1등 선정)을 거쳐 배치.
- **Node Affinity & Anti-Affinity**: "이 Pod는 GPU Node에만 띄워라(Affinity)" 또는 "이 Pod는 동일 Node에 중복 배치 금지(Anti-Affinity)"를 선언하는 하드/소프트 조건식.

</details>

- 정의/개념: 미배치 Pod의 Resource Request, Node Selectors, Affinity, Taints 조건을 평가하여 Filtering(거르기) 및 Scoring(점수화)을 거쳐 optimal Node에 배정하는 스케줄링 프레임워크인 **Kubernetes Pod Scheduling**
- 배경/필요성: 특정 Node 자원 쏠림 현상 예방, GPU 전용 노드 제한, HA를 위한 동일 노드 중복 배치 방지 요구성

#### 한줄 요약

- 좌석 배정처럼 필수 조건에 맞지 않는 노드를 먼저 제외한 뒤 남은 후보의 점수를 비교하면 대기 원인과 선택 이유가 분명해진다.

## Ⅱ. 특징 (Pod 스케줄링 3대 핵심 메커니즘)

<details><summary>핵심 용어</summary>

- **Taints & Tolerations**: Node에 칠해진 거부 도장(Taint)을 견딜 수 있는 인가 도장(Toleration)을 가진 Pod만 해당 Node에 들어올 수 있도록 차단하는 기법.

</details>

- **Two-Phase Scheduling Pipeline (Filtering 1차 필터링 $\rightarrow$ Scoring 2차 점수 채점)**
- **Constraint Policies (Node Affinity, Pod Anti-Affinity, Taints and Tolerations 적용)**
- **Priority & Preemption (우선순위가 높은 Pod 생성을 위해 저우선순위 Pod 강제 축출)**

#### 한줄 요약

- GPU처럼 반드시 필요한 조건은 필터에 두고 같은 영역 선호처럼 선택 가능한 조건은 점수에 두어야 파드가 불필요하게 대기하지 않는다.

## Ⅲ. 구조 및 구성요소 (스케줄링 2대 알고리즘 및 조건표)

<details><summary>핵심 용어</summary>

- **NodeName Binding**: kube-scheduler가 점수 1등 노드를 결정하면 `Pod.spec.nodeName = "node-02"` 명세에 기록하는 최종 승인 단계.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   kube-scheduler Scheduling Pipeline                   │
├────────────────────────────────────────────────────────────────────────┤
│ [Pending Pod] ──► 1. FILTERING (Predicates) ──► 2. SCORING (Priorities)│
│                     • NodeResourcesFit           • NodeResourcesBalanced│
│                     • NodeName / NodeSelector    • ImageLocality        │
│                     • Taints & Tolerations       • NodeAffinityScore    │
│                                                          │             │
│                                                          ▼             │
│ [Pod Bound to Node 2] ◄── [NodeName Binding] ◄── [Pick Best Node 2]    │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Pending Pod가 Filtering을 거쳐 부적합 노드를 지우고, Scoring에서 1등 노드를 선별하여 nodeName을 바인딩하는 구조.

| 스케줄링 기법 (Technique) | 적용 주체 | 주요 역할 및 설정 명세 |
|:---|:---|:---|
| **NodeSelector / Affinity** | **Pod 측에 선언** | **"나는 `disk=ssd` 레이블을 가진 Node에만 들어갈래"** |
| **Pod Anti-Affinity** | **Pod 측에 선언** | **"동일 서비스 Pod 2개가 같은 Node에 겹치지 마라"** |
| **Taints & Tolerations** | **Node & Pod 양측**| **"이 Node는 `gpu=true` Toleration이 없는 Pod는 거부함"**|
| **Priority & Preemption** | **Pod PriorityClass**| **비상시 중요 Pod 배치를 위해 일반 Pod를 강제 축출** |

#### 한줄 요약

- 대기열은 접수 창구, 필터는 입장 조건 검사, 점수는 좌석 선호 계산, 바인딩은 최종 좌석표 기록에 해당한다.

## Ⅳ. 흐름도 (Node Filtering & Scoring 처리 흐름)

<details><summary>핵심 용어</summary>

- **Topology Spread Constraints**: Pod를 여러 가용 영역(AZ) 및 Node 간에 균등한 비율로 찢어서 분산 배치시키는 고가용성 스케줄링 기법.

</details>

```text
[All Nodes (100 Nodes)] ──► [Filtering: CPU/Memory Fit & Taints (10 Nodes Left)]
                                                │
                                                ▼
  [Bind Node 2] ◄── [Pick Max Score Node 2] ◄── [Scoring: ImageLocality & Balance (Scores)]
```

### 동작 원리

1. **Filtering**: 전체 100개 노드 중 CPU 부족 노드, Taint 차단 노드를 빼고 10개 생존.
2. **Scoring**: 이미 도커 이미지를 다운로드받은 노드(ImageLocality)에 가산점을 주어 Node 2가 95점으로 1등.
3. **Binding**: `spec.nodeName: node-02` 명시 완료 (**Pod Scheduling 완결**).

#### 한줄 요약

- 파드 하나를 대기열에서 꺼낸 뒤 실행 불가능한 노드를 버리고 남은 후보를 채점해 가장 높은 노드를 객체에 기록한다.

## Ⅴ. 종류 및 비교 (Hard Affinity 대 Soft Affinity)

<details><summary>핵심 용어</summary>

- **requiredDuringScheduling (Hard)**: 조건 미충족 시 Pod가 절대로 배치 안 되고 Pending으로 남음.
- **preferredDuringScheduling (Soft)**: 가급적 선호하되, 노드가 없으면 조건 미충족 노드라도 들어가서 구동됨.

</details>

| 조건 강도 | 구체적 스케줄링 설정 구문 | 노드 미존재 시 동작 행위 |
|:---|:---|:---|
| **Hard Constraint (필수)** | `requiredDuringSchedulingIgnoredDuringExecution` | **Pod가 절대로 배치되지 않고 `Pending` 대기** |
| **Soft Constraint (선호)** | `preferredDuringSchedulingIgnoredDuringExecution` | **선호 노드가 없으면 다른 일반 노드에 일단 배치됨** |

#### 한줄 요약

- 필터 조건을 지나치게 좁히면 후보 자체가 사라지고 점수 조건만 바꾸면 파드는 실행되면서 배치 위치만 달라진다.

## Ⅵ. 실무 고려사항 및 대책 (Pod 스케줄링 3대 난제 대책)

<details><summary>핵심 용어</summary>

- **Pod Pending Emergency**: Node의 Memory/CPU Request 수치가 차올라 신규 Pod가 안 뜨고 `0/10 nodes are available` 에러 표출.

</details>

| 3대 스케줄링 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Pod Pending (자원 부족)**| Node 자원 Request가 한계치 초과 | **Karpenter / Cluster Autoscaler 노드 증설**|
| **2. Taint Node Isolation** | Master Node에 Taint 설정되어 배치 불가 | **Pod spec에 matching Toleration 추가 세팅** |
| **3. Node Skew / Single Point**| 1개 Node에 Pod 10개가 쏠려 배치됨 | **`topologySpreadConstraints` 로 1/N 균등 분산**|

> 사례: **카카오 / 당근마켓 / 쿠팡 Karpenter 연동 Pod 스케줄링 및 Topology Spread 분산 배치**

#### 한줄 요약

- GPU 파드에 필수 레이블을 요구했다면 노드 자동 확장 템플릿에도 같은 레이블과 자원 정보가 있어야 새 노드가 생긴 뒤 배치된다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Pod Scheduling 수립 기준(Scheduling Standards)**: Filtering/Scoring 파이프라인, Hard/Soft Affinity, Taints/Tolerations 및 TopologySpreadConstraints 분산성에 의거한 체계.

</details>

- **Pod Scheduling 수립 기준**에 따라 전사 클러스터 구축 시 **Kubernetes Pod Scheduling & Karpenter** 필수 적용

#### 한줄 요약

- 실행 불가능 조건은 필터에만 두고 장애 분산 같은 선호는 점수로 표현해야 가용 후보를 유지하면서 배치 품질을 높일 수 있다.
