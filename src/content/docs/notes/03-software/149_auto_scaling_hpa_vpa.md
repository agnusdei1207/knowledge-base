---
sidebar:
  order: 149
  label: "149. 오토 스케일링 HPA•VPA (Auto Scaling HPA VPA)"
  badge:
    text: "미출 • 70%"
    variant: note
title: "오토 스케일링 HPA•VPA (Auto Scaling HPA VPA)"
date: "2026-08-14T01:48:00+09:00"
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

<details><summary>용어 설명</summary>

- **Auto Scaling (오토 스케일링)**: 애플리케이션의 실시간 CPU/메모리/트래픽 부하 지표 변화에 응답하여 컴퓨팅 자원(Node/Pod)의 개수나 스펙을 동적으로 자동 확장(Scale-out) 및 축소(Scale-in)하는 메커니즘.
- **HPA (Horizontal Pod Autoscaler)**: CPU 사용률이나 QPS 요청량 증가 시, 동일 컨테이너 포드(Pod)의 개수(Replicas)를 수평으로 개수 증설하는 쿠버네티스 컨트롤러 (Scale-out).
- **VPA (Vertical Pod Autoscaler)**: 포드의 개수는 그대로 유지한 채, 포드 단일 개체에 할당된 CPU/Memory 리소스 스펙(Limit/Request)을 수직으로 체급 업그레이드하는 컨트롤러 (Scale-up).

</details>

- 정의/개념: 지표에 따라 복제본•자원 요청을 조정하는 **HPA•VPA**
- 배경/필요성: 수동 증설은 **부하 변동•자원 부족**에 적시 대응 곤란

#### 한줄 요약

- 주문이 몰리면 작업자 수를 늘리는 HPA와 작업자 한 명의 장비 크기를 바꾸는 VPA처럼, 병렬 처리량과 Pod당 자원 부족을 서로 다른 축으로 조정한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Horizontal vs Vertical**: HPA는 Pod 개수 N개 증설 (Scale-out / Stateless 앱 적합), VPA는 Pod 사양 체급 증설 (Scale-up / Stateful DB 적합).

</details>

- **HPA**는 지표에 따라 Pod 복제본 수를 수평 조정
- **VPA**는 관측 사용량에 따라 CPU•Memory 요청 조정
- 동일 자원 지표를 함께 쓰면 **제어 충돌** 가능

#### 한줄 요약

- 주문량이 경계값을 오갈 때마다 작업자를 뽑고 내보내지 않도록 일정 시간 기다리듯, 안정화 구간과 증감 속도가 반복 확장·축소를 억제한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Metrics Server & Custom Metrics**: Prometheus 및 Metrics Server가 15초 주기로 Pod CPU/RAM/QPS 지표를 수집해 HPA/VPA 컨트롤러로 릴레이.

</details>

```text
[지표 공급자] ───── [HPA 제어기]
      │                  │
[VPA 제어기] ───── [워크로드 제어기]
                         │
                    [스케줄러•노드]
```

| 구성요소 | 책임 |
|---|---|
| 지표 공급자 | **자원•사용자 지표** 수집•제공 |
| HPA 제어기 | 목표 지표로 **복제본 수** 계산 |
| VPA 제어기 | 사용량으로 **자원 요청값** 추천•적용 |
| 워크로드 제어기 | 원하는 복제본과 Pod 템플릿 반영 |
| 스케줄러•노드 | **Pod 배치**와 실행 용량 제공 |

#### 한줄 요약

- 같은 측정판을 본 HPA와 VPA가 각각 작업자 수와 장비 크기를 정하고, 워크로드 제어기와 스케줄러가 실제 작업자와 자리를 배치한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **HPA Target Replica Algorithm**: `DesiredReplicas = ceil[ CurrentReplicas * ( CurrentMetricValue / TargetMetricValue ) ]` 수치로 수평 복제본 계산.

</details>

```text
[부하 변화]
    │
    ▼
1. 지표 수집
    │
    ▼
2. 목표 대비 편차 계산
    │
    ▼
3. 복제본•요청값 결정
    │
    ▼
4. 워크로드 반영
    │
    ▼
5. 배치•안정화 검증
    │
    ▼
[확장 결과]
```

### 동작 원리

1. **지표 수집**: CPU•Memory•QPS 등 현재 부하 관측
2. **목표 대비 편차 계산**: 현재값과 정책 목표 비교
3. **복제본•요청값 결정**: HPA 또는 VPA 조정량 산출
4. **워크로드 반영**: 제어기가 복제본•Pod 명세 갱신
5. **배치•안정화 검증**: Pending•SLO와 진동 여부 확인

#### 한줄 요약

- 주문량이 늘면 HPA가 작업자 수를 바꾸고 한 작업자가 계속 힘들어하면 VPA가 장비 크기를 바꾸며, 실제로 자리가 없으면 포드가 대기 상태로 남는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Cluster Autoscaler (CA / Karpenter)**: Pod 레벨 확장(HPA)을 넘어서, Node 자체(AWS EC2)의 갯수를 수평 증설해 주는 인프라 레이어 오토스케일러.

</details>

| 오토스케일러 종류 | 대상 (Target Level) | 스케일링 동작 메커니즘 | 실무 적용 도구 예시 |
|:---|:---|:---|:---|
| **HPA** | **Pod Level (수평)** | **Pod 개수 증설 (Scale-out)** | **K8s Native HPA, KEDA** |
| **VPA** | **Pod Level (수직)** | **Pod 리소스 체급 증설 (Scale-up)**| **K8s Native VPA** |
| **Cluster Autoscaler**| **Node Level (인프라)**| **Worker Node EC2 개수 증설** | **Karpenter, Cluster Autoscaler** |

#### 한줄 요약

- 작업을 나눌 수 있으면 같은 장비의 작업자를 늘리고, 한 작업자에게 필요한 장비 크기가 틀렸으면 CPU·메모리 요청값을 바꾼다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

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

<details><summary>용어 설명</summary>

- **Auto Scaling 수립 기준(Auto Scaling Standards)**: HPA(Stateless), VPA(Stateful), KEDA Event-driven, Karpenter Node Autoscaler 연동성에 의거한 체계.

</details>

- 병렬 부하는 **HPA**, Pod 자원 오차는 VPA로 조정

#### 한줄 요약

- 나눌 수 있는 주문은 작업자 수로, 한 작업자의 장비 부족은 장비 크기로 해결하되 작업장 자리가 먼저 확보돼야 실제 확장이 끝난다.
