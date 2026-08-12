---
sidebar:
  order: 149
  label: "149. 오토 스케일링 HPA•VPA (Auto Scaling HPA VPA)"
  badge:
    text: "미출 • 70%"
    variant: note
title: "오토 스케일링 HPA•VPA (Auto Scaling HPA VPA)"
date: "2026-08-06T23:27:50+09:00"
tags:
  - "notes-software"
weight: 149
extra:
  question_no: "149"
  source_status: "미출"
  source_history: ""
  priority: 70
  priority_note: "복제본 수와 자원 크기 조정 비교 가치가 높음"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Auto Scaling (오토 스케일링)**: 애플리케이션의 실시간 CPU/메모리/트래픽 부하 지표 변화에 응답하여 컴퓨팅 자원(Node/Pod)의 개수나 스펙을 동적으로 자동 확장(Scale-out) 및 축소(Scale-in)하는 메커니즘.
- **HPA (Horizontal Pod Autoscaler)**: CPU 사용률이나 QPS 요청량 증가 시, 동일 컨테이너 포드(Pod)의 개수(Replicas)를 수평으로 개수 증설하는 쿠버네티스 컨트롤러 (Scale-out).
- **VPA (Vertical Pod Autoscaler)**: 포드의 개수는 그대로 유지한 채, 포드 단일 개체에 할당된 CPU/Memory 리소스 스펙(Limit/Request)을 수직으로 체급 업그레이드하는 컨트롤러 (Scale-up).

</details>

- 정의/개념: 부하 급증 시 포드 개수를 늘리는 수평 스케일링(HPA)과 포드의 CPU/Memory 체급을 높이는 수직 스케일링(VPA)을 통해 서비스 가용성을 자동 지탱하는 **Kubernetes Auto Scaling (HPA & VPA)**
- 배경/필요성: 수동 포드 개수 조절(Scale)의 트래픽 폭증 대응 불가, Pod 리소스 OOM(Out of Memory) Crash 방지 및 인프라 비용 효율화 요구성

#### 한줄 요약

- 주문이 몰리면 작업자 수를 늘리는 HPA와 작업자 한 명의 장비 크기를 바꾸는 VPA처럼, 병렬 처리량과 Pod당 자원 부족을 서로 다른 축으로 조정한다.

## Ⅱ. 특징 (HPA 대 VPA 2대 스케일링 차원)

<details><summary>핵심 용어</summary>

- **Horizontal vs Vertical**: HPA는 Pod 개수 N개 증설 (Scale-out / Stateless 앱 적합), VPA는 Pod 사양 체급 증설 (Scale-up / Stateful DB 적합).

</details>

- **HPA (Scale-out: Pod 개수 증설, Zero-Downtime, Web/API Stateless 앱 선호)**
- **VPA (Scale-up: CPU/Mem 사양 증설, Pod 재시작 동반, DB Stateful 앱 선호)**
- **Conflict Prevention (동일 CPU 지표에 대해 HPA와 VPA를 동시 적용 금지)**

#### 한줄 요약

- 주문량이 경계값을 오갈 때마다 작업자를 뽑고 내보내지 않도록 일정 시간 기다리듯, 안정화 구간과 증감 속도가 반복 확장·축소를 억제한다.

## Ⅲ. 구조 및 구성요소 (HPA & VPA 오토스케일링 4대 핵심 구조)

<details><summary>핵심 용어</summary>

- **Metrics Server & Custom Metrics**: Prometheus 및 Metrics Server가 15초 주기로 Pod CPU/RAM/QPS 지표를 수집해 HPA/VPA 컨트롤러로 릴레이.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Kubernetes Auto Scaling Architecture                 │
├────────────────────────────────────────────────────────────────────────┤
│ [Metrics Server / Prometheus] ──► (Metrics Scraping 15s)               │
│               │                                                        │
│               ▼                                                        │
│ ┌─────────────────────────────┐    ┌─────────────────────────────────┐ │
│ │  HPA Controller (Scale-out) │    │   VPA Controller (Scale-up)     │ │
│ │  • Increases Pod Replicas   │    │   • Adjusts CPU/Mem Request Limit │ │
│ │  • 1 Pod ──► 5 Pods         │    │   • 1Core/2GB ──► 4Core/8GB        │ │
│ └─────────────────────────────┘    └─────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: Metrics Server가 수집한 지표에 따라 HPA는 포드 개수를(가로), VPA는 포드 체급 사양을(세로) 동적 확장하는 구조.

| 구성 요소 (Component) | HPA (Horizontal Pod Autoscaler) | VPA (Vertical Pod Autoscaler) |
|:---|:---|:---|
| **스케일링 메커니즘** | **Pod 개수(Replicas) 수평 확장 (1 $\rightarrow$ 10)** | **Pod 당 CPU/Memory 수직 증설 (1G $\rightarrow$ 4G)** |
| **다운타임 발생 여부**| **0% (무중단 롤링 확장)** | 발생 가능 (Pod 재생성 적용 시 순간 재시작) |
| **추천 애플리케이션** | **Stateless Web, REST API, Microservices**| **Stateful RDBMS, Redis, Batch Job** |
| **공동 사용 주의점** | **동일 지표(CPU)로 HPA와 VPA 동시 세팅 금지 (무한 루프 방지)**| HPA는 커스텀 지표, VPA는 CPU 지표로 분리 |

#### 한줄 요약

- 같은 측정판을 본 HPA와 VPA가 각각 작업자 수와 장비 크기를 정하고, 워크로드 제어기와 스케줄러가 실제 작업자와 자리를 배치한다.

## Ⅳ. 흐름도 (HPA Auto Scaling 계산 및 동작 흐름)

<details><summary>핵심 용어</summary>

- **HPA Target Replica Algorithm**: `DesiredReplicas = ceil[ CurrentReplicas * ( CurrentMetricValue / TargetMetricValue ) ]` 수치로 수평 복제본 계산.

</details>

```text
[Metrics Server CPU 85% Scrape] ──► [HPA Algorithm Calculation]
                                                  │
                                                  ▼
   [Kubernetes Cluster Autoscaler] ◄── [Deployment Replicas (3 ──► 6 Scale-out)]
```

### 동작 원리

1. **Metrics Scraping**: Metrics Server가 Pod 평균 CPU 사용률 85% 감지 (타깃 50%).
2. **Calculation**: HPA 알고리즘에 의해 현재 3개 포드를 6개 포드로 스케일아웃 확정.
3. **Cluster Autoscaler**: 포드를 배치할 노드 슬롯이 부족하면 Node Cluster Autoscaler가 AWS EC2 노드 자체를 스케일아웃 (**Auto Scaling 완결**).

#### 한줄 요약

- 주문량이 늘면 HPA가 작업자 수를 바꾸고 한 작업자가 계속 힘들어하면 VPA가 장비 크기를 바꾸며, 실제로 자리가 없으면 포드가 대기 상태로 남는다.

## Ⅴ. 종류 및 비교 (HPA vs VPA vs Cluster Autoscaler)

<details><summary>핵심 용어</summary>

- **Cluster Autoscaler (CA / Karpenter)**: Pod 레벨 확장(HPA)을 넘어서, Node 자체(AWS EC2)의 갯수를 수평 증설해 주는 인프라 레이어 오토스케일러.

</details>

| 오토스케일러 종류 | 대상 (Target Level) | 스케일링 동작 메커니즘 | 실무 적용 도구 예시 |
|:---|:---|:---|:---|
| **HPA** | **Pod Level (수평)** | **Pod 개수 증설 (Scale-out)** | **K8s Native HPA, KEDA** |
| **VPA** | **Pod Level (수직)** | **Pod 리소스 체급 증설 (Scale-up)**| **K8s Native VPA** |
| **Cluster Autoscaler**| **Node Level (인프라)**| **Worker Node EC2 개수 증설** | **Karpenter, Cluster Autoscaler** |

#### 한줄 요약

- 작업을 나눌 수 있으면 같은 장비의 작업자를 늘리고, 한 작업자에게 필요한 장비 크기가 틀렸으면 CPU·메모리 요청값을 바꾼다.

## Ⅵ. 실무 고려사항 및 대책 (HPA/VPA 오토스케일링 3대 실무 지침)

<details><summary>핵심 용어</summary>

- **KEDA (Kubernetes Event-driven Autoscaling)**: CPU/Memory 외에 Kafka Topic Lag, RabbitMQ 큐 쌓인 개수, AWS SQS 메시지 수 기반으로 포드를 미리 오토스케일링해 주는 오픈소스 프레임워크.

</details>

| 3대 오토스케일링 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Flapping / Thrashing** | 지표가 순간 소폭 변할 때마다 Pod 생성/파기 반복| **Scale-down Stabilization Window (5분) 설정** |
| **2. Slow Pod Boot Delay** | Pod 부팅 시간이 3분 걸려 초기 트래픽 퐁당 | **Prometheus 기반 KEDA 이벤트 오토스케일링** |
| **3. Node Resource Exhaust** | HPA로 Pod만 늘다가 Node 메모리 부족 터짐 | **AWS Karpenter 도입으로 초고속 Node 자동 덤프**|

> 사례: **쿠팡 / 당근마켓 / 카카오 KEDA 및 Karpenter 기반 초고속 5초 오토스케일링 적용 사례**

#### 한줄 요약

- 주문 신호가 울린 순간이 아니라 새 작업자가 자리를 받아 일을 시작한 순간까지 재고, 작업장에 빈자리가 없으면 노드부터 늘려야 한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Auto Scaling 수립 기준(Auto Scaling Standards)**: HPA(Stateless), VPA(Stateful), KEDA Event-driven, Karpenter Node Autoscaler 연동성에 의거한 체계.

</details>

- **Auto Scaling 수립 기준**에 따라 차세대 클라우드 네이티브 구축 시 **Kubernetes HPA & KEDA & Karpenter** 필수 적용

#### 한줄 요약

- 나눌 수 있는 주문은 작업자 수로, 한 작업자의 장비 부족은 장비 크기로 해결하되 작업장 자리가 먼저 확보돼야 실제 확장이 끝난다.
