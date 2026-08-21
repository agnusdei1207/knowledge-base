---
sidebar:
  order: 154
  label: "154. 쿠버네티스 Pod 스케줄링 (Kubernetes Pod Scheduling)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "쿠버네티스 Pod 스케줄링 (Kubernetes Pod Scheduling)"
date: "2026-08-18T01:50:00+09:00"
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

- **쿠버네티스 파드 스케줄링(Pod Scheduling)**: kube-scheduler가 대기(Pending) 상태인 파드의 자원 요구량, 라벨 어피니티(Affinity), 테인트(Taints)를 분석하여 최적의 워커 노드를 결정하고 바인딩하는 프로세스.
- **자원 불균형 및 단일 장애점 편중(Resource Imbalance & Node Skew)**: 스케줄링 제약 부재 시 특정 노드에만 파드가 몰려 자원이 고갈되거나 장애 영역(AZ)에 파드가 편중되어 단일 장애가 발생하는 위험.

</details>

- 정의/개념: 미배치 파드(Pending)의 자원 요구량과 제약 조건을 분석하여 **필터링과 스코어링을 통해 최적의 워커 노드에 바인딩**하는 스케줄링 메커니즘
- 배경/필요성: 단순 라운드로빈 배치가 초래하는 **노드별 자원 불균형, GPU/특수 장비 미스매칭 및 단일 장애점(SPOF) 집중 위험** 직면

#### 한줄 요약

- 필터링과 스코어링 2단계 파이프라인을 거쳐 파드를 가장 적합한 워커 노드에 균형 있게 분산 배치

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **2단계 스케줄링(Filtering & Scoring)**: 1단계에서 자원 부족 노드를 걸러내는 필터링(Predicates)과 2단계에서 가중치를 매겨 1등 노드를 뽑는 스코어링(Priorities).
- **테인트 및 톨러레이션(Taints & Tolerations)**: 노드에 거부 도장(Taint)을 찍어 일반 파드 유입을 막고 해당 도장을 견디는 톨러레이션(Toleration) 보유 파드만 진입을 허용하는 격리 기법.

</details>

- 부적합 노드를 걸러내고 최적 후보를 채점하는 **2단계(Filtering $\to$ Scoring) 스케줄링**
- 노드/파드 어피니티 및 테인트/톨러레이션을 통한 **정밀한 워크로드 격리 및 배치 통제**
- 우선순위가 높은 중요 파드를 위해 저우선 파드를 퇴거시키는 **우선순위 및 선점(Preemption)**

#### 한줄 요약

- 선언적 배치 제약 조건과 자원 기반 점수화를 통해 클러스터 자원 활용률과 안정성을 극대화

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **스케줄링 제약 매트릭스**: NodeAffinity(노드 선호), PodAntiAffinity(파드 분산), Taints/Tolerations(노드 격리), TopologySpread(균등 분할).

</details>

```text
[ 쿠버네티스 파드 스케줄링 2단계 파이프라인 구조도 ]

 1. [ 스케줄링 큐 (Scheduling Queue) ] ──► [ Pending Pod 인출 ]
                                                    │
                                                    ▼
 2. [ 1단계: Filtering (Predicates) ] ─────────────────────────────┐
    • Node 자원 여유 검사 (CPU/RAM Request)                        │
    • Taints & Tolerations 검사 (GPU/Master 격리)                  │
    • NodeAffinity (Hard: required) 필수 조건 검사                 │
    └───────────────────────────┬──────────────────────────────────┘
                                │ (통과한 노드 후보군)
                                ▼
 3. [ 2단계: Scoring (Priorities) ] ───────────────────────────────┐
    • NodeAffinity (Soft: preferred) 가중치 점수                   │
    • PodAnti-Affinity 및 Topology Spread 가중치 점수              │
    • Node 자원 균형도 (LeastRequested vs MostAllocated)           │
    └───────────────────────────┬──────────────────────────────────┘
                                │ (1등 최고 점수 노드)
                                ▼
 4. [ Binding 단계 ] ──► [ Pod.spec.nodeName = "node-01" 확정 ]
```

선의 의미: Pending 파드가 Filtering(부적합 배제)과 Scoring(점수 채점)을 거쳐 최종 노드에 바인딩되는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 스케줄링 큐 (Queue) | 미배치된 파드를 **우선순위(PriorityClass) 순서대로 정렬하여 인출** |
| 필터링 계층 (Filtering) | CPU/메모리 부족, Taint 불일치 등 **실행 불가능한 부적합 노드를 엄격 배제** |
| 스코어링 계층 (Scoring) | 자원 균형도, 지역성, 선호도 점수를 합산하여 **최적의 1등 후보 노드 선정** |
| 노드/파드 어피니티 | 라벨(Label) 조건을 기반으로 **특정 노드 선호 또는 파드 간 장애 영역 분산 강제** |
| 테인트/톨러레이션 | GPU 전용 노드 또는 컨트롤 플레인에 **비인가 일반 파드가 배치되는 것을 원천 차단** |

#### 한줄 요약

- 스케줄링 큐, 필터링, 스코어링, 어피니티, 테인트/톨러레이션이 결합하여 최적 배치를 완성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **파드 스케줄링 5단계 절차**: 큐 인출 $\to$ 노드 필터링 $\to$ 가중치 스코어링 $\to$ 1등 노드 선정 $\to$ etcd 바인딩.

</details>

```text
[ kube-scheduler 파드 노드 배치 및 바인딩 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. Pending 파드 Scheduling Queue 인출  │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. 리소스 및 Hard 제약 기반 Node Filtering
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. 분산도 및 Soft 제약 기반 Node Scoring│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. 최고 득점 노드 선정 (동점 시 무작위)│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. API 서버 호출 및 nodeName 바인딩 완료
 └────────────────────────────────────────┘
```

### 동작 원리

1. 큐 인출: 스케줄러가 대기 큐에서 우선순위가 가장 높은 Pending 파드를 꺼냄.
2. 노드 필터링: 전체 노드 중 Request 자원이 부족하거나 Taint가 걸린 노드를 즉시 탈락시킴.
3. 노드 스코어링: 필터링을 통과한 후보 노드들을 대상으로 PodAntiAffinity 및 자원 균형 플러그인 점수를 계산.
4. 노드 선정: 총합 점수가 가장 높은 노드를 타깃 노드로 최종 낙점(동점 시 라운드로빈).
5. 바인딩: API 서버에 Binding 서브리소스를 전송하여 `pod.spec.nodeName`을 기록하고 etcd를 갱신.

#### 한줄 요약

- 큐 인출 $\to$ 필터링 $\to$ 스코어링 $\to$ 최고점 선정 $\to$ 바인딩의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Hard Constraint vs Soft Constraint**: 필수 조건(Hard)과 선호 조건(Soft)의 스케줄링 동작 비교.

</details>

| 구분 | Hard 제약 (필수 조건: required) | Soft 제약 (선호 조건: preferred) |
|:---|:---|:---|
| **적용 기준** | SSD 필수, GPU 필수, 동일 노드 절대 중복 금지 | 가급적 분산 선호, 특정 가용 영역 선호 |
| **핵심 특징** | **`requiredDuringSchedulingIgnoredDuringExecution`** | **`preferredDuringSchedulingIgnoredDuringExecution`** |
| **한계** | 조건 미충족 시 파드가 절대 뜨지 않고 영구 Pending | 선호 노드가 없으면 조건 미충족 일반 노드에 배치됨 |

#### 한줄 요약

- 필수 하드웨어는 Hard 제약, 권장 분산 배치는 Soft 제약을 적용하여 스케줄링 유연성을 확보

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **토폴로지 분산 제약(Topology Spread Constraints)**: 파드를 여러 AZ(가용 영역) 및 노드에 특정 비율(maxSkew) 이내로 균등 분산 배치하는 현대적 고가용성 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 노드 가용 자원 부족으로 대규모 파드 Pending 정체 | **Karpenter 도입으로 요구 스펙 맞춤형 노드 즉시 자동 프로비저닝** | 스케줄링 대기 시간 수 초 단축 |
| 특정 노드 1대에 동일 서비스 파드가 몰려 노드 다운 시 서비스 장애 | **`topologySpreadConstraints` (maxSkew: 1) 전사 적용** | 가용 영역(AZ) 및 노드 간 완벽 균등 분산 |
| GPU 머신러닝 전용 고가 노드에 일반 웹 파드가 배치되어 자원 낭비 | **GPU 노드에 `Taint: dedicated=gpu:NoSchedule` 설정** | 전용 특수 노드 자원 완벽 보호 |

#### 한줄 요약

- Karpenter 자동 프로비저닝, 토폴로지 균등 분산, Taint 전용 격리를 통해 스케줄링 효율을 극대화

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **지능형 스케줄링 프레임워크(Scheduling Framework)**: K8s 1.18+ 이후 필터/스코어 플러그인을 커스텀 개발하여 삽입할 수 있는 확장 인터페이스.

</details>

- **쿠버네티스 파드 스케줄링** 분산 클러스터의 자원 효율성과 서비스 무중단 가용성을 좌우하는 핵심 엔진이며, 필수 조건(Hard)과 선호 조건(Soft)을 정교하게 조합하고 토폴로지 분산 제약을 적용해야 함

#### 한줄 요약

- 2단계 스케줄링과 토폴로지 분산 제약을 통해 자원 최적화와 고가용성을 완성
