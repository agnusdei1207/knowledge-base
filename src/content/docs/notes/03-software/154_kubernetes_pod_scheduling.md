---
sidebar:
  order: 154
  label: "154. 쿠버네티스 Pod 스케줄링"
  badge:
    text: "기출 · 70%"
    variant: note
title: "쿠버네티스 Pod 스케줄링 (Kubernetes Pod Scheduling)"
date: "2026-08-26T13:11:54+09:00"
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

- **kube-scheduler**: Pending 상태인 파드의 자원 요구량(Request), 어피니티, 테인트를 분석하여 최적의 워커 노드를 결정하고 바인딩하는 제어면 컴포넌트.
- **Filtering & Scoring**: 조건 미달 노드를 탈락시키는 1단계 필터링(Predicates)과 잔여 후보 노드의 점수를 매기는 2단계 스코어링(Priorities).

</details>

- 정의/개념: 미배치 파드(Pending)의 자원 요구량과 제약 조건을 분석하여 **Filtering과 Scoring 2단계 평가를 통해 최적의 워커 노드에 바인딩하는 스케줄링 메커니즘**
- 배경/필요성: 빈 노드에 순서대로 얹으면 자원 요구량과 하드웨어 제약을 무시해 GPU 작업이 일반 노드에 떨어지고 같은 서비스의 복제본이 한 노드에 몰려 장애 반경이 커지므로, 배치 가능 여부를 먼저 걸러낸 뒤 남은 후보를 점수화해 자원 균형과 장애 격리를 함께 만족시키는 2단계 평가 계층이 필요

#### 한줄 요약
- 필터링은 배치 가능 여부를 가르고 스코어링은 그중 나은 곳을 고르는 서로 다른 역할이므로, 파드가 Pending에 머무는 원인은 점수가 낮아서가 아니라 필터를 통과한 노드가 하나도 없기 때문이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Taints & Tolerations**: 노드에 거부 표식(Taint)을 부여하여 일반 파드 배치를 차단하고, 대응하는 Toleration을 가진 파드만 진입을 허용.
- **Node/Pod Affinity**: 파드가 특정 라벨의 노드에 배치되거나(NodeAffinity), 특정 파드와 같은 노드 또는 다른 노드(AntiAffinity)에 배치되도록 강제/선호.

</details>

- 부적합 노드를 걸러내고 최적 후보를 채점하는 **2단계(Filtering $\rightarrow$ Scoring) 스케줄링**
- 노드/파드 어피니티 및 테인트/톨러레이션을 통한 **정밀한 워크로드 격리 및 배치 통제**
- 우선순위가 높은 중요 파드를 위해 저우선 파드를 퇴거시키는 **우선순위 및 선점(Preemption)**

#### 한줄 요약
- 선언적 배치 제약 조건과 자원 점수화를 통해 클러스터 자원 활용성과 고가용성을 보장한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **스케줄링 3단계 파이프라인**: Scheduling Queue(우선순위 정렬), Filtering(Hard 제약 검사), Scoring(Soft 가중치 채점), Binding(노드 확정).

</details>

| 구성요소 | 책임 | 주요 특징 |
|:---|:---|:---|
| 스케줄링 큐 (Queue) | 미배치된 파드를 **우선순위(PriorityClass) 순서대로 정렬하여 인출** | 우선순위 큐 |
| 필터링 계층 (Filtering) | CPU/메모리 부족, Taint 불일치 등 **실행 불가능한 부적합 노드를 엄격 배제** | Hard 제약 검사 |
| 스코어링 계층 (Scoring) | 자원 균형도, 지역성, 선호도 점수를 합산하여 **최적의 1등 후보 노드 선정** | Soft 가중치 채점 |
| 노드/파드 어피니티 | 라벨(Label) 조건을 기반으로 **특정 노드 선호 또는 파드 간 장애 영역 분산 강제** | Affinity / AntiAffinity |
| 테인트/톨러레이션 | GPU 전용 노드 또는 컨트롤 플레인에 **비인가 일반 파드가 배치되는 것을 원천 차단** | NoSchedule, NoExecute |

#### 한줄 요약
- 스케줄링 큐가 도착 순서대로 처리하던 배치를 우선순위 정렬로 대신해 중요한 파드가 뒤에 와도 먼저 자리를 잡고, 어피니티와 테인트/톨러레이션이 관리자가 노드를 직접 지정하던 배치를 라벨 선언으로 대신하므로 노드가 교체돼도 명세는 그대로 쓰인다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **스케줄링 5단계**: 큐 인출 $\to$ 노드 필터링 $\to$ 가중치 스코어링 $\to$ 1등 노드 선정 $\to$ etcd 바인딩.

</details>

```text
Pending 상태의 파드가 스케줄러에 도달
        │
   [큐 인출] 스케줄러가 대기 큐에서 PriorityClass가 가장 높은 파드 인출
        │
   [노드 필터링] Request 자원 부족 노드 및 Taint 불일치 노드를 1차 탈락 (Filtering)
        │
   [노드 스코어링] 통과 노드들을 대상으로 PodAntiAffinity 및 자원 균형도 점수 계산 (Scoring)
        │
   [최고 득점 노드 선정] 총점이 가장 높은 1등 노드를 최종 타깃으로 낙점 (동점 시 라운드로빈)
        │
   kube-apiserver에 바인딩 요청을 전송하여 `pod.spec.nodeName` 확정 및 etcd 갱신
```

#### 한줄 요약
- 스케줄러는 선언된 요청량만 보고 실제 사용량은 보지 않으므로, 요청을 실제보다 크게 잡으면 노드가 남아도 배치가 막히고 작게 잡으면 배치는 되지만 노드가 과부하에 빠진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Hard Constraint vs Soft Constraint**: 필수 조건(`required`)과 선호 조건(`preferred`)의 스케줄링 동작 비교.

</details>

| 비교 항목 | Hard 제약 (필수 조건: required) | Soft 제약 (선호 조건: preferred) |
|:---|:---|:---|
| 설정 키워드 | **`requiredDuringSchedulingIgnoredDuringExecution`** | **`preferredDuringSchedulingIgnoredDuringExecution`** |
| 스케줄링 단계 | **1단계 필터링 (Filtering: 불만족 시 탈락)** | **2단계 스코어링 (Scoring: 점수 가산)** |
| 조건 미충족 시 동작| **파드가 절대 뜨지 않고 영구 Pending 상태 유지** | **선호 노드가 없어도 일반 노드에 정상 스케줄링**|
| 최적 적용 사례 | **GPU 하드웨어 필수, SSD 전용 스토리지 필수** | **가급적 타 AZ 분산 선호, 특정 인스턴스 선호** |

#### 한줄 요약
- 필수 하드웨어는 Hard 제약, 권장 분산 배치는 Soft 제약을 적용하여 스케줄링 유연성을 확보한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Topology Spread Constraints**: 파드를 여러 AZ 및 노드에 특정 허용 비율(maxSkew: 1) 이내로 균등하게 강제 분산 배치하는 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 노드 가용 자원 부족으로 대규모 파드 Pending 정체 | **Karpenter 도입으로 요구 스펙 맞춤형 노드 즉시 자동 프로비저닝** | 스케줄링 대기 시간 수 초 단축 |
| 특정 노드 1대에 동일 서비스 파드가 몰려 노드 다운 시 서비스 장애 | **`topologySpreadConstraints` (maxSkew: 1) 전사 적용** | 가용 영역(AZ) 및 노드 간 완벽 균등 분산 |
| GPU 머신러닝 전용 고가 노드에 일반 웹 파드가 배치되어 자원 낭비 | **GPU 노드에 `Taint: dedicated=gpu:NoSchedule` 설정** | 전용 특수 노드 자원 완벽 보호 |
| 고우선순위 파드가 노드 부족으로 기동 불가 | **PriorityClass 및 Preemption(선점) 설정으로 저우선 파드 축출** | 핵심 서비스 가용성 보장 |

#### 한줄 요약
- Karpenter 자동 증설, 토폴로지 균등 분산, Taint 전용 격리, 선점 우선순위로 스케줄링을 최적화한다.

## Ⅶ. 결론

- 배치 후보 선별은 **필터링**, 분산 최적화는 **스코어링** 선택

#### 한줄 요약
- 쿠버네티스 파드 스케줄링은 2단계 평가와 선언적 배치 제약을 통해 자원 균형과 장애 격리를 달성하는 핵심 오케스트레이션 엔진이다.
