---
sidebar:
  order: 148
  label: "148. 예약 인스턴스•스팟 인스턴스 (Reserved and Spot Instances)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "예약 인스턴스•스팟 인스턴스 (Reserved and Spot Instances)"
date: "2026-08-06T23:27:50+09:00"
tags: ["notes-software"]
weight: 148
extra:
  question_no: "148"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "약정 할인과 중단 위험 비교가 비용 설계에 포함됨"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Reserved Instance (RI / 예약 인스턴스)**: 1년/3년 단위 장기 사용 약정을 조건으로 기본 On-Demand 요율 대비 최대 40~72% 할인된 가격으로 클라우드 컴퓨팅 자원을 선점 구매하는 비용 최적화 옵션.
- **Spot Instance (스팟 인스턴스)**: CSP(AWS) 데이터센터의 미사용 잉여 인스턴스(Unused Capacity)를 경매식 요율로 80~90% 대폭 할인받되, CSP가 필요 시 2분 전 노티 후 강제 회수(Interruption)해 가는 고위험 초저가 옵션.
- **On-Demand Instance**: 약정 0%, 중단 위험 0% 상태로 초/분 단위 사용한 만큼만 정가를 지불하는 기본 인스턴스.

</details>

- 정의/개념: 클라우드 인프라 구매 시 비용 절감을 위해 1~3년 장기 약정 할인(RI)과 2분 전 강제 회수 중단 위험을 감수한 초저가 할인(Spot)을 혼용 조합하는 비용 아키텍처인 **Reserved & Spot Instances**
- 배경/필요성: 100% On-Demand 정가 지불로 인한 비용 낭비 방지, Batch 연산 및 K8s 워커 노드의 90% 인프라 단가 절감 요구성

#### 한줄 요약

- 매일 타는 구간은 정기권을 사고 자리를 빼앗겨도 다음 차에서 이어 갈 일은 빈 좌석 표를 사듯, 수요 지속성과 중단 복구 가능성에 따라 구매 방식을 나눈다.

## Ⅱ. 특징 (구매 옵션 3대 분류)

<details><summary>핵심 용어</summary>

- **Capacity Reclaim & 2-Minute Warning**: 스팟 인스턴스는 CSP 자원 부족 시 2분 전 사전 노티(EventBridge) 후 인스턴스를 강제 셧다운 및 뺏어감.

</details>

- **On-Demand (무약정 0%, 중단 위험 0%, 정가 100% 지불)**
- **Reserved Instance / Savings Plans (1/3년 약정, 중단 위험 0%, 40~72% 할인)**
- **Spot Instance (약정 0%, 강제 회수 위험 100%, 80~90% 파격 할인)**

#### 한줄 요약

- 매일 필요한 좌석은 정기권, 중간에 내릴 수 있는 작업은 빈 좌석 표, 갑자기 생긴 이동은 일반 표를 사듯 수요 성격마다 가격과 위험이 달라진다.

## Ⅲ. 구조 및 구성요소 (Spot Fleet & Mixed Instances Group)

<details><summary>핵심 용어</summary>

- **Spot Fleet & Auto Scaling Group**: 특정 단일 인스턴스 타입 회수 시 서비스가 멈추는 것을 막기 위해 `c5.large`, `c5a.large`, `m5.large` 등 이종 타겟으로 스팟을 묶어 자동 대체 구매하는 기술.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   AWS Mixed Instances Group Strategy                   │
├────────────────────────────────────────────────────────────────────────┤
│ Baseline Static Traffic  ──► [1. Reserved Instances (RI / SP)] (30%) │
│ Dynamic Normal Traffic   ──► [2. On-Demand Instances]         (20%) │
│ Batch / K8s Worker Nodes ──► [3. Spot Fleet Multi-AZ Pools]     (50%) │
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 베이스라인은 RI 약정 할인, 변동분은 On-Demand, stateless 렌더링/K8s 노드는 Spot Fleet으로 기하급수적 절감을 렌더링하는 아키텍처.

| 인스턴스 구매 옵션 | 할인율 | 중단 위험 (Interruption) | 최적 사용 도메인 유스케이스 |
|:---|:---|:---|:---|
| **On-Demand** | **0% (정가)** | **0% (절대 안 끊김)** | **신규 서비스 테스트, 예측 불가능 트래픽** |
| **Reserved / SP** | **40% ~ 72%** | **0% (절대 안 끊김)** | **24시간 365일 가동되는 메인 Core DB/App** |
| **Spot Instance** | **80% ~ 90%** | **100% (2분 전 강제 회수)** | **K8s Worker, Spark Batch, CI/CD Runner** |

#### 한줄 요약

- 수요 분석표가 매일 필요한 좌석은 예약 장부로, 중단 가능한 작업은 스팟 풀과 진행표로, 갑작스러운 작업은 온디맨드 좌석으로 연결한다.

## Ⅳ. 흐름도 (Spot Interruption Handler 2분 응급 대처 흐름)

<details><summary>핵심 용어</summary>

- **Spot Interruption Handler**: 2분 회수 경보 이벤트(`aws.ec2.spot-instance-interrupt-notice`)를 수신하여 현재 태스크를 타 노드로 Cordon/Drain 이체하는 K8s 컨트롤러.

</details>

```text
[AWS Spot Reclaim Warning (2-Min Notice)] ──► [EventBridge / Spot Interruption Handler]
                                                           │
                                                           ▼
 [New Spot Node Provisioning] ◄── [K8s Node Cordon & Drain (Task Re-scheduling)]
```

### 동작 원리

1. **Reclaim Trigger**: AWS 데이터센터 자원 부족으로 2분 전 Spot Interruption 경보 발행.
2. **Cordon & Drain**: K8s Spot Handler가 해당 노드에 신규 Pod 할당을 막고(Cordon), 기존 Pod를 타 노드로 이사시킴(Drain).
3. **Graceful Re-node**: 2분 이내에 안가 배치 및 신규 Spot 노드 띄우기 완결 (**Spot 안정적 렌더링**).

#### 한줄 요약

- 빈 좌석에서 작업하다 자리를 돌려줘야 하면 바깥 장부에 적은 마지막 진행 지점부터 다른 좌석에서 이어 가고, 마감이 가까우면 일반 표로 바꾼다.

## Ⅴ. 종류 및 비교 (RI Standard 대 RI Convertible 대 Savings Plans)

<details><summary>핵심 용어</summary>

- **Compute Savings Plans**: RI의 딱딱한 가상머신 규격 묶임을 깨고, 인스턴스 패밀리, 인스턴스 크기, 데이터센터 위치가 바뀌어도 할인 혜택을 알아서 유연 적용해 주는 현대적 약정 모델.

</details>

| 약정 상품 분류 | Standard RI | Convertible RI | Compute Savings Plans (최신) |
|:---|:---|:---|:---|
| **인스턴스 변경 자율성**| **불가 (동일 인스턴스 타입 고정)**| 인스턴스 타입 변경 가능 | **인스턴스 타입, OS, Region 변경 100% 무관 적용** |
| **할인율 파급력** | **최상 (70% 이상)** | 상 (60% 수준) | **상 (최대 66% 유연 할인)** |
| **실무 채택 선호도** | 낮음 (규격 변경 리스크) | 보통 | **최상 (모던 클라우드 추천 1순위)** |

#### 한줄 요약

- 매일 쓰는 좌석은 예약이 싸고, 자리를 잃어도 이어 갈 일은 스팟이 싸며, 갑작스러운 이동은 비싸더라도 온디맨드가 바로 대응한다.

## Ⅵ. 실무 고려사항 및 대책 (Spot Instance 3대 파행 요소 해복책)

<details><summary>핵심 용어</summary>

- **Spot Capacity Unavailable**: 특정 리전에 해당 타입 스팟 잔여 자원이 0이 되어 Spot Fleet 생성이 안 되는 병목 현상.

</details>

| 3대 스팟 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Spot Capacity 0건** | 특정 타입(c5.large) 스팟 자원 매진 | **`capacity-optimized` 믹스 전략으로 이종 타입 묶음**|
| **2. Pod State Loss** | 2분 회수 시 상태(State) 날아감 | **Stateless 앱(웹/API)에만 Spot 적용 (DB 적용 금지)** |
| **3. Spot Batch Failure** | 2분 이내 배치 연산 안 끝나고 튕김 | **Checkpointing 기반 하차 후 재개(Resume) 로직** |

> 사례: **카카오 / 당근마켓 K8s EKS 클러스터 Worker 노드 80% Spot Fleet 적용 및 인프라 비용 70% 절감**

#### 한줄 요약

- 평균이 아니라 매일 유지되는 최소 좌석만 예약하고, 스팟 작업은 진행표를 밖에 보관하며 마감 시각 전에는 온디맨드로 넘어가도록 임계값을 둔다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **Spot/RI 수립 기준(Spot and RI Standards)**: Base Load Compute Savings Plans, K8s Worker Spot Fleet Multi-AZ, Spot Handler 2분 훅 및 Stateful DB Spot 배제 원칙성에 의거한 체계.

</details>

- **Spot/RI 수립 기준**에 따라 비용 최적화 아키텍처 구축 시 **Compute Savings Plans + Spot Fleet Multi-AZ Group** 필수 적용

#### 한줄 요약

- 매일 필요한 좌석은 정기권으로 사고, 진행표를 들고 옮길 수 있는 일은 빈 좌석을 쓰며, 갑자기 늘어난 일은 일반 표로 처리한다.
