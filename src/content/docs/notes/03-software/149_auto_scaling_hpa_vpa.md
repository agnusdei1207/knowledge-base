---
sidebar:
  order: 149
  label: "149. 오토 스케일링 HPA•VPA"
  badge:
    text: "미출 · 70%"
    variant: note
title: "오토 스케일링 HPA•VPA (Auto Scaling HPA VPA)"
date: "2026-09-07T10:05:00+09:00"
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

- **HPA vs VPA**: Pod 복제본 개수를 증감시키는 수평 확장(HPA: Scale-out)과 Pod의 CPU/Memory 요청 스펙을 증감시키는 수직 확장(VPA: Scale-up).
- **Metrics Server**: Kubelet으로부터 Pod 및 Node의 CPU/Memory 사용량 메트릭을 수집하여 HPA/VPA 컨트롤러에 제공하는 핵심 애드온.

</details>

- 정의/개념: 쿠버네티스 환경에서 실시간 부하 지표에 따라 Pod 복제본 수를 수평 증감하는 HPA와 Pod 자원 스펙을 수직 조정하는 VPA 메커니즘
- 배경/필요성: 고정 리소스 할당 방식으로 인한 피크 타임 성능 병목(OOM/다운), 트래픽 감소 시 유휴 자원 방치 및 수동 대응 지연 한계

#### 한줄 요약
- HPA는 부하를 나눌 수 있을 때만, VPA는 나눌 수 없을 때만 유효하므로 둘은 같은 문제의 경쟁 대안이 아니라 워크로드의 병렬화 가능 여부에 따라 갈리는 서로 다른 답이다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Desired Replicas 공식**: $\text{DesiredReplicas} = \lceil \text{CurrentReplicas} \times (\text{CurrentMetric} / \text{TargetMetric}) \rceil$.
- **KEDA(Kubernetes Event-driven Autoscaling)**: CPU 외에 Kafka Lag, SQS 큐 길이 등 외부 이벤트를 기반으로 Pod를 사전 오토스케일링하는 프레임워크.

</details>

- 부하에 따라 Pod 개수를 수평 스케일아웃하는 무상태(Stateless) 최적화 HPA
- 관측된 실제 사용량을 분석하여 Pod 자원 크기를 재조정하는 유휴 자원 회수 최적화 VPA
- 잦은 생성·삭제 진동(Flapping)을 방지하는 안정화 윈도우(Stabilization Window)

#### 한줄 요약
- 수평 복제본 확장과 수직 자원 재조정을 통해 인프라 탄력성과 비용 효율을 극대화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **오토스케일링 4대 컴포넌트**: Metrics Provider(지표 수집), HPA Controller(복제본 계산), VPA Controller(스펙 추천), Workload Controller(Pod 명세 반영).

</details>

```text
[쿠버네티스 오토스케일링]
├─ [지표 수집 계층]
│  └─ Metrics Provider (CPU·메모리·QPS)
├─ [스케일링 제어 계층]
│  ├─ HPA Controller (수평: 복제본 개수)
│  └─ VPA Controller (수직: 요청 스펙)
└─ [반영 및 인프라 계층]
   ├─ Workload Controller (Deployment 갱신)
   └─ Node Autoscaler (Pending 시 노드 증설)
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 지표 공급자 | CPU·메모리·QPS 수집 |
| HPA 제어기 | 목표 지표별 복제본 수 증감 |
| VPA 제어기 | Pod의 자원 요청량 갱신 |
| 워크로드 제어기 | Deployment·StatefulSet의 Pod 명세 반영 |
| 노드 스케일러 | Pending Pod를 위한 워커 노드 증설 |

#### 한줄 요약
- HPA·VPA 제어기는 지표 공급자와 워크로드 제어기 사이에 끼어들어 운영자가 손으로 정하던 복제본 수와 자원 요청량 결정을 대신하고, 노드 스케일러는 그 결정이 Pending으로 막히지 않도록 배치될 워커 노드 용량을 뒤에서 채운다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **HPA 스케일링 5단계**: 지표 수집 $\to$ 목표 편차 계산 $\to$ 복제본 수 산출 $\to$ Deployment 스케일아웃 $\to$ 노드 용량 확보 및 배포.

</details>

```text
대외 트래픽 유입으로 애플리케이션 부하 급증
        │
   [지표 수집] Metrics Server가 Pod별 평균 CPU 사용률(예: 85%) 관측
        │
   [목표 편차 계산] HPA 설정 목표값(50%) 대비 초과 편차 비율 계산
        │
   [복제본 산출] Desired Replicas 공식에 따라 Pod 복제본을 3개에서 6개로 증설 결정
        │
   [Deployment 반영] Deployment의 `replicas: 6`으로 갱신하여 신규 Pod 3개 생성 요청
        │
   노드 자원이 부족할 경우 Karpenter가 새 EC2 노드를 즉시 기동하여 신규 Pod 스케줄링 완료
```

#### 한줄 요약
- 지표 수집과 반영 사이의 시차 때문에 조정은 언제나 부하보다 늦게 도착하므로, 급격한 스파이크에서는 사후 반응형 스케일링만으로 부족하고 선제 트리거가 함께 필요해진다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **HPA vs VPA vs Cluster Autoscaler**: Pod 수평 확장(HPA), Pod 수직 확장(VPA), 노드 인프라 확장(CA/Karpenter).

</details>

| 비교 항목 | HPA (Horizontal Pod Autoscaler) | VPA (Vertical Pod Autoscaler) | Cluster Autoscaler / Karpenter |
|:---|:---|:---|:---|
| 확장 대상 계층 | Pod 수평 계층 (Scale-out) | Pod 수직 계층 (Scale-up) | Node 인프라 계층 (EC2 증설) |
| 핵심 동작 방식 | Pod 복제본(Replicas) 개수 증감 | Pod CPU/Memory Request 체급 변경 | Worker Node 서버 인스턴스 증설 |
| 파드 재시작 여부 | 신규 Pod 추가로 기존 Pod 무중단 유지 | 자원 변경을 위해 Pod 재시작(Eviction) | 노드 추가이므로 기존 Pod 무영향 |
| 최적 적용 대상 | 무상태(Stateless) 웹/API 서버 | 단일 인스턴스 배치, Stateful DB | 클러스터 전체 용량 부족 시 |

#### 한줄 요약
- 무상태 웹 서버는 HPA, 단일 인스턴스 배치는 VPA, 클러스터 용량 부족은 Karpenter를 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Flapping (Thrashing)**: 트래픽이 임계치 경계에서 요동칠 때 Pod 생성과 삭제가 무한 반복되어 시스템 오버헤드가 폭증하는 현상.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 트래픽 변동 시 Pod 생성과 삭제가 무한 반복되는 **Flapping** | Scale-down 안정화 윈도우(`stabilizationWindowSeconds: 300`) 설정 | 파드 생성/삭제 진동 0화 |
| Java JVM Pod 부팅 지연(3분)으로 초기 트래픽 급증 시 장애 | Kafka Lag/SQS 기반 KEDA 이벤트 오토스케일링 사전 트리거 | 트래픽 대응 지연시간 80% 단축 |
| HPA로 Pod만 증설되다가 노드 용량 고갈로 Pending 누적 | AWS Karpenter 도입하여 5초 이내 최적 워커 노드 동적 증설 | Pod 스케줄링 지연 해소 |
| 동일 CPU 지표에 HPA와 VPA 동시 적용 시 제어 충돌 | HPA는 CPU/Custom 지표, VPA는 Memory 전용으로 분리 운영 | 오토스케일링 제어 충돌 원천 차단 |

#### 한줄 요약
- 안정화 윈도우 설정, KEDA 사전 트리거, Karpenter 노드 연동, 지표 분리 운영으로 안정성을 확보한다.

## Ⅶ. 결론

- 쿠버네티스(Kubernetes) 기반 컨테이너 오케스트레이션 및 마이크로서비스 아키텍처의 가장 핵심적인 자동 탄력성(Elasticity) 제어 메커니즘으로 확립되었으며, 실무 구축 시에는 무상태(Stateless) 웹/API 워크로드에 HPA + KEDA(이벤트 기반 사전 확장) 적용, 단일 프로세스 배치/Stateful 워크로드에는 VPA 자원 추천 모드(Off/Initial) 적용, 스케일다운 시 진동(Flapping)을 방지하는 안정화 윈도우(Stabilization Window) 튜닝 및 노드 병목을 제거하는 Karpenter 초고속 프로비저너 연동을 결합하여 무결점 확장성과 리소스 최적화를 완성

#### 한줄 요약
- HPA와 VPA는 부하 특성에 따라 수평 및 수직으로 자원을 동적 조정하여 시스템 가용성과 비용 효율을 동시에 보장하는 쿠버네티스의 핵심 탄력성 기술이다.
