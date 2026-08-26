---
sidebar:
  order: 148
  label: "148. 예약 인스턴스•스팟 인스턴스"
  badge:
    text: "기출 · 50%"
    variant: note
title: "예약 인스턴스•스팟 인스턴스 (Reserved and Spot Instances)"
date: "2026-08-26T09:58:00+09:00"
tags:
  - "notes-software"
weight: 148
extra:
  question_no: "148"
  source_status: "기출"
  source_history: "135회"
  priority: 50
  priority_note: "약정 할인과 중단 위험 비교가 비용 설계에 포함됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **RI / Savings Plans**: 1~3년 장기 약정을 통해 기본 정가 대비 최대 72% 할인받는 요율 최적화 옵션.
- **Spot Instance**: CSP의 미사용 잉여 컴퓨팅 자원을 최대 90% 할인받아 사용하되 2분 전 경고 후 회수되는 초저비용 옵션.

</details>

- 정의/개념: 클라우드 인프라 비용을 최적화하기 위해 **장기 약정 기반의 예약 인스턴스(RI/SP)와 잉여 자원 기반의 스팟 인스턴스(Spot)를 최적 조합하는 구매 전략**
- 배경/필요성: 모든 인프라를 기본 정가(On-Demand)로 운영 시 발생하는 **컴퓨팅 비용 과다 청구 및 워크로드별 중단 허용도 차이 미반영 해결 불가**

#### 한줄 요약
- 베이스라인은 예약 약정으로 단가를 낮추고 무상태 워크로드는 스팟으로 최대 90% 비용을 절감한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **2-Minute Notice**: 스팟 인스턴스 회수 2분 전에 EventBridge로 발송되는 사전 경고 이벤트.
- **Spot Fleet**: 특정 인스턴스 회수 시 대체 가능한 다수의 패밀리(c5, m5, r5)를 묶어 가용성을 유지하는 풀(Pool).

</details>

- 24/365 가동되는 안정적 베이스라인 트래픽을 위한 **Savings Plans / RI 약정 할인**
- 언제든 재시작 가능한 무상태(Stateless) 웹/배치를 위한 **최대 90% 초저가 스팟 인스턴스**
- 예측 불가능한 돌발 스파이크 트래픽을 즉시 흡수하는 **정가 온디맨드(On-Demand) 병용**

#### 한줄 요약
- 워크로드의 지속성과 중단 허용도에 따라 예약, 스팟, 온디맨드를 혼합 운영한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **혼합 인스턴스 그룹(Mixed Instances Group)**: Baseline(Savings Plans), Stateless Burst(Spot Fleet), Peak Buffer(On-Demand).

</details>

```text
[혼합 인스턴스 그룹(Mixed Instances Group) 아키텍처]
|-- 1. Baseline Capacity (24/365 고정 부하)
|   |-- Stateful Core DB (RDS / Aurora)
|   `-- Compute Savings Plans 적용 (최대 66%~72% 약정 할인)
|-- 2. Stateless Scale-Out (무상태 동적 확장)
|   |-- EKS Worker Nodes / AI 딥러닝 배치
|   `-- Spot Fleet 풀 구성 (최대 90% 할인, 이종 패밀리 분산)
`-- 3. Peak Spike Buffer (돌발 피크 트래픽)
    `-- On-Demand 인스턴스 (스팟 매진 시 자동 폴백 및 무중단 보장)
```

선의 의미: 계층 및 기본 수요는 Savings Plans, 무상태 확장은 Spot, 긴급 폴백은 On-Demand로 분기 결합하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 예약 약정 (RI / SP) | 코어 DB 및 항시 가동 서버에 대해 **1~3년 약정 요율을 적용하여 고정 비용 절감** | 최대 72% 할인 |
| 스팟 플릿 (Spot Fleet) | 이종 인스턴스 풀(Pool)을 구성하여 **무상태 웹/배치 작업을 90% 할인된 가격에 처리** | Capacity-Optimized |
| 온디맨드 (On-Demand) | 예측 불가한 트래픽 스파이크 및 **스팟 자원 회수 시 즉시 가동되는 안전 버퍼** | 100% 무중단 보장 |
| 스팟 핸들러 (Handler) | 2분 회수 경보 수신 시 **K8s Pod Cordon/Drain을 실행하여 무중단 태스크 이체** | Graceful Shutdown |

#### 한줄 요약
- 예약 약정(기본 부하), 스팟 플릿(무상태 확장), 온디맨드(비상 버퍼), 스팟 핸들러로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **스팟 인스턴스 회수 대응 5단계**: 회수 이벤트 수신 $\to$ K8s Cordon $\to$ K8s Drain $\to$ 대체 인스턴스 기동 $\to$ 무중단 서비스 재개.

</details>

```text
CSP로부터 스팟 인스턴스 2분 전 회수 신호 발생
        │
   [회수 이벤트 수신] EventBridge가 `spot-instance-interrupt-notice` 감지 및 핸들러 전달
        │
   [K8s Cordon] 스팟 핸들러가 해당 노드에 `kubectl cordon`을 실행하여 신규 Pod 배포 즉시 차단
        │
   [K8s Drain] `kubectl drain`을 실행하여 실행 중인 파드를 타 정상 노드로 안전하게 Graceful 퇴거
        │
   [대체 자원 기동] ASG가 Spot Fleet 풀에서 타 인스턴스 타입을 즉시 증설하거나 온디맨드로 폴백
        │
   클라이언트는 500 에러 없이 정상적으로 무중단 서비스 지속 이용
```

#### 한줄 요약
- 이벤트 수신 → Cordon 차단 → Drain 이체 → 대체 노드 기동 → 무중단 재개 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **온디맨드 vs Savings Plans vs 스팟**: 가격 할인율, 중단 위험, 적합 워크로드에 따른 3대 옵션 비교.

</details>

| 비교 항목 | 온디맨드 (On-Demand) | 예약 인스턴스 (Savings Plans) | 스팟 인스턴스 (Spot Instance) |
|:---|:---|:---|:---|
| 가격 할인율 | 정가 기준 (할인율 0%) | **최대 66% ~ 72% 할인** | **최대 90% 초저가 할인** |
| 인스턴스 중단 위험 | **중단 위험 0% (완전 안정)** | **중단 위험 0% (완전 안정)** | **2분 전 회수 위험 존재** |
| 약정 기간 조건 | 무약정 (사용한 초 단위 과금) | **1년 또는 3년 장기 약정** | 무약정 (잉여 자원 경매제) |
| 최적 적용 대상 | **신규 런칭 서비스, 돌발 스파이크**| **24/365 DB, 베이스라인 API** | **무상태 웹 서버, AI 학습, 배치**|

#### 한줄 요약
- 정가는 온디맨드, 베이스라인은 Savings Plans 약정, 중단 가능한 배치는 스팟을 선택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Capacity-Optimized Strategy**: 스팟 요청 시 현재 CSP 리전에서 자원 회수 확률이 가장 낮은 인스턴스 풀을 자동으로 골라 할당하는 전략.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 특정 인스턴스 타입 스팟 자원 고갈로 증설 실패 | **Spot Fleet에 `capacity-optimized` 전략 및 10개 이상 타입 지정** | 스팟 프로비저닝 성공률 99.9% 달성 |
| 스팟 인스턴스 회수로 인한 데이터베이스 상태(State) 유실 | **Stateful DB는 전면 배제하고 오직 무상태(Stateless) 파드에만 스팟 적용**| 데이터 정합성 파괴 원천 차단 |
| 장기 배치 연산 도중 스팟 회수로 작업 처음부터 재실행 | **애플리케이션 체크포인팅(Checkpointing) 구현 및 중간 상태 S3 저장** | 회수 시 마지막 체크포인트부터 즉시 재개 |
| 약정 후 서비스 축소로 인한 RI/SP 약정 비용 낭비 | **특정 패밀리에 종속되지 않는 Compute Savings Plans 선택** | 약정 유연성 확보 및 손실 방지 |

#### 한줄 요약
- 이종 풀 구성, 무상태 한정 적용, 체크포인팅, Compute Savings Plans로 위험을 완벽히 통제한다.

## Ⅶ. 결론

- 기본 부하는 **예약 약정**, 무상태 확장은 **스팟** 선택

#### 한줄 요약
- 예약 및 스팟 인스턴스는 워크로드의 특성과 중단 허용도에 맞추어 비용을 극대화하는 엔터프라이즈 클라우드 요율 최적화의 핵심 기법이다.