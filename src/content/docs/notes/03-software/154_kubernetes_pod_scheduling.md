---
sidebar:
  order: 154
  label: "154. 쿠버네티스 Pod 스케줄링 (Kubernetes Pod Scheduling)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "쿠버네티스 Pod 스케줄링 (Kubernetes Pod Scheduling)"
date: "2026-08-14T02:08:00+09:00"
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

<details><summary>용어 설명</summary>

- **쿠버네티스 파드 스케줄링(Kubernetes Pod Scheduling)**: 스케줄러(kube-scheduler)가 대기(Pending) 상태인 파드(Pod)를 리소스 여유, 테인트(Taint), 어피니티(Affinity) 규칙에 따라 적합한 노드에 배치(Binding)하는 프로세스.
- **필터링 & 스코어링(Filtering & Scoring)**: 스케줄링 단계로, 1단계 필터링(부적합 노드 배제) 후 2단계 스코어링(최적 노드 선정)을 수행.
- **노드 어피니티(Node Affinity/Anti-Affinity)**: 특정 파드를 특정 노드군에 배치하거나(Affinity), 중복 배치를 방지(Anti-Affinity)하는 선언적 배치 제약 조건.

</details>

- 정의/개념: Pending Pod를 적합한 Node에 Binding하는 **Pod Scheduling**
- 배경/필요성: 무조건 배치는 **자원 부족•격리•장애 영역** 제약 위반

#### 한줄 요약

- 좌석 배정처럼 필수 조건에 맞지 않는 노드를 먼저 제외한 뒤 남은 후보의 점수를 비교하면 대기 원인과 선택 이유가 분명해진다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Taints & Tolerations**: Node에 칠해진 거부 도장(Taint)을 견딜 수 있는 인가 도장(Toleration)을 가진 Pod만 해당 Node에 들어올 수 있도록 차단하는 기법.

</details>

- **2단계 스케줄링 파이프라인(Two-Phase Scheduling Pipeline)**: 필터링으로 부적합 노드를 제외하고, 스코어링으로 적합도가 높은 노드를 채점하여 우선순위 결정.
- **제약 조건 정책(Constraint Policies)**: 노드 어피니티, 파드 안티-어피니티, 테인트/톨러레이션(Taints & Tolerations)을 적용하여 세밀한 배치 통제.
- **우선순위 및 선점(Priority & Preemption)**: 우선순위 높은 파드를 배치하기 위해 저우선순위 파드를 강제로 축출(Eviction)하는 기법.

#### 한줄 요약

- GPU처럼 반드시 필요한 조건은 필터에 두고 같은 영역 선호처럼 선택 가능한 조건은 점수에 두어야 파드가 불필요하게 대기하지 않는다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **NodeName Binding**: kube-scheduler가 점수 1등 노드를 결정하면 `Pod.spec.nodeName = "node-02"` 명세에 기록하는 최종 승인 단계.

</details>

| 구성요소 | 책임 |
|---|---|
| NodeSelector•Affinity | Label 기반 **Node 필수•선호 조건** 선언 |
| Pod Anti-Affinity | 같은 Pod 집합의 **장애 영역 분산** |
| Taints•Tolerations | Node 거부 조건과 **Pod 허용 예외** 결합 |
| Priority•Preemption | 중요 Pod를 위한 **우선순위•선점** 통제 |

#### 한줄 요약

- 대기열은 접수 창구, 필터는 입장 조건 검사, 점수는 좌석 선호 계산, 바인딩은 최종 좌석표 기록에 해당한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Topology Spread Constraints**: Pod를 여러 가용 영역(AZ) 및 Node 간에 균등한 비율로 찢어서 분산 배치시키는 고가용성 스케줄링 기법.

</details>

```text
[Pending Pod]
      │
      ▼
1. Scheduling Queue 인출
      │
      ▼
2. 부적합 Node Filtering
      │
      ▼
3. 후보 Node Scoring
      │
      ▼
4. 최고 점수 Node Binding
      │
      ▼
[Node 배치 결과]
```

### 동작 원리

1. **Scheduling Queue 인출**: 미배치 Pod를 우선순위로 선택
2. **부적합 Node Filtering**: 자원•Taint•Affinity 위반 제외
3. **후보 Node Scoring**: 균형•지역성•선호 기준 평가
4. **최고 점수 Node Binding**: 선택 Node를 Pod에 연결

#### 한줄 요약

- 파드 하나를 대기열에서 꺼낸 뒤 실행 불가능한 노드를 버리고 남은 후보를 채점해 가장 높은 노드를 객체에 기록한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **requiredDuringScheduling (Hard)**: 조건 미충족 시 Pod가 절대로 배치 안 되고 Pending으로 남음.
- **preferredDuringScheduling (Soft)**: 가급적 선호하되, 노드가 없으면 조건 미충족 노드라도 들어가서 구동됨.

</details>

| 조건 강도 | 구체적 스케줄링 설정 구문 | 노드 미존재 시 동작 행위 |
|:---|:---|:---|
| **Hard Constraint (필수)** | `requiredDuringSchedulingIgnoredDuringExecution` | **Pod가 절대로 배치되지 않고 `Pending` 대기** |
| **Soft Constraint (선호)** | `preferredDuringSchedulingIgnoredDuringExecution` | **선호 노드가 없으면 다른 일반 노드에 일단 배치됨** |

#### 한줄 요약

- 필터 조건을 지나치게 좁히면 후보 자체가 사라지고 점수 조건만 바꾸면 파드는 실행되면서 배치 위치만 달라진다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

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

- 실행 필수 조건은 **Filtering**, 배치 선호는 Scoring으로 분리

#### 한줄 요약

- 실행 불가능한 노드는 제외하고 가용 후보 안에서 분산과 비용 선호를 점수화한다.
