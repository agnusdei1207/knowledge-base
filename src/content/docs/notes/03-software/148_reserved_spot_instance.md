---
sidebar:
  order: 148
  label: "148. 예약 인스턴스•스팟 인스턴스 (Reserved and Spot Instances)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "예약 인스턴스•스팟 인스턴스 (Reserved and Spot Instances)"
date: "2026-08-14T01:44:00+09:00"
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

<details><summary>용어 설명</summary>

- **Reserved Instance (RI / 예약 인스턴스)**: 1년/3년 단위 장기 사용 약정을 조건으로 기본 On-Demand 요율 대비 최대 40~72% 할인된 가격으로 클라우드 컴퓨팅 자원을 선점 구매하는 비용 최적화 옵션.
- **Spot Instance (스팟 인스턴스)**: CSP(AWS) 데이터센터의 미사용 잉여 인스턴스(Unused Capacity)를 경매식 요율로 80~90% 대폭 할인받되, CSP가 필요 시 2분 전 노티 후 강제 회수(Interruption)해 가는 고위험 초저가 옵션.
- **On-Demand Instance**: 약정 0%, 중단 위험 0% 상태로 초/분 단위 사용한 만큼만 정가를 지불하는 기본 인스턴스.

</details>

- 정의/개념: 약정•가용 용량으로 요율을 낮추는 **Reserved•Spot Instance**
- 배경/필요성: 단일 구매 방식은 **수요 안정성•중단 허용도** 차이를 반영 불가

#### 한줄 요약

- 매일 타는 구간은 정기권을 사고 자리를 빼앗겨도 다음 차에서 이어 갈 일은 빈 좌석 표를 사듯, 수요 지속성과 중단 복구 가능성에 따라 구매 방식을 나눈다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Capacity Reclaim & 2-Minute Warning**: 스팟 인스턴스는 CSP 자원 부족 시 2분 전 사전 노티(EventBridge) 후 인스턴스를 강제 셧다운 및 뺏어감.

</details>

- **On-Demand**는 약정 없이 변동 수요에 대응
- **Reserved•Savings Plans**는 안정 수요를 약정해 할인
- **Spot Instance**는 잉여 용량을 쓰며 회수 위험 수용

#### 한줄 요약

- 매일 필요한 좌석은 정기권, 중간에 내릴 수 있는 작업은 빈 좌석 표, 갑자기 생긴 이동은 일반 표를 사듯 수요 성격마다 가격과 위험이 달라진다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Spot Fleet & Auto Scaling Group**: 특정 단일 인스턴스 타입 회수 시 서비스가 멈추는 것을 막기 위해 `c5.large`, `c5a.large`, `m5.large` 등 이종 타겟으로 스팟을 묶어 자동 대체 구매하는 기술.

</details>

```text
[혼합 인스턴스 그룹]
 ├── [Reserved•SP 기반 용량]
 ├── [On-Demand 변동 용량]
 └── [Spot 중단 가능 용량]
```

| 구성요소 | 책임 |
|---|---|
| Reserved•SP 기반 용량 | **안정 수요**의 약정 요율 적용 |
| On-Demand 변동 용량 | 예측하기 어려운 **탄력 수요** 처리 |
| Spot 중단 가능 용량 | **재시작 가능 작업**의 잉여 용량 활용 |

#### 한줄 요약

- 수요 분석표가 매일 필요한 좌석은 예약 장부로, 중단 가능한 작업은 스팟 풀과 진행표로, 갑작스러운 작업은 온디맨드 좌석으로 연결한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Spot Interruption Handler**: 2분 회수 경보 이벤트(`aws.ec2.spot-instance-interrupt-notice`)를 수신하여 현재 태스크를 타 노드로 Cordon/Drain 이체하는 K8s 컨트롤러.

</details>

```text
[회수 경고]
    │
    ▼
1. 중단 이벤트 수신
    │
    ▼
2. 신규 배치 차단
    │
    ▼
3. 상태 체크포인트
    │
    ▼
4. 작업 재배치
    │
    ▼
5. 대체 용량 확보
    │
    ▼
[처리 재개]
```

### 동작 원리

1. **중단 이벤트 수신**: 회수 대상과 종료 시점 식별
2. **신규 배치 차단**: Cordon으로 새 작업 할당 방지
3. **상태 체크포인트**: 재개 지점을 외부 저장소에 기록
4. **작업 재배치**: Drain으로 실행 작업을 다른 노드로 이동
5. **대체 용량 확보**: Spot Pool 또는 On-Demand 보충

#### 한줄 요약

- 빈 좌석에서 작업하다 자리를 돌려줘야 하면 바깥 장부에 적은 마지막 진행 지점부터 다른 좌석에서 이어 가고, 마감이 가까우면 일반 표로 바꾼다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Compute Savings Plans**: RI의 딱딱한 가상머신 규격 묶임을 깨고, 인스턴스 패밀리, 인스턴스 크기, 데이터센터 위치가 바뀌어도 할인 혜택을 알아서 유연 적용해 주는 현대적 약정 모델.

</details>

| 약정 상품 분류 | Standard RI | Convertible RI | Compute Savings Plans (최신) |
|:---|:---|:---|:---|
| 인스턴스 변경 자율성 | **불가 (동일 인스턴스 타입 고정)**| 인스턴스 타입 변경 가능 | **인스턴스 타입, OS, Region 변경 100% 무관 적용** |
| 할인율 파급력 | **최상 (70% 이상)** | 상 (60% 수준) | **상 (최대 66% 유연 할인)** |
| 실무 채택 선호도 | 낮음 (규격 변경 리스크) | 보통 | **최상 (모던 클라우드 추천 1순위)** |

#### 한줄 요약

- 매일 쓰는 좌석은 예약이 싸고, 자리를 잃어도 이어 갈 일은 스팟이 싸며, 갑작스러운 이동은 비싸더라도 온디맨드가 바로 대응한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Spot Capacity Unavailable**: 특정 리전에 해당 타입 스팟 잔여 자원이 0이 되어 Spot Fleet 생성이 안 되는 병목 현상.

</details>

| 3대 스팟 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| 1. Spot Capacity 0건 | 특정 타입(c5.large) 스팟 자원 매진 | **`capacity-optimized` 믹스 전략으로 이종 타입 묶음**|
| 2. Pod State Loss | 2분 회수 시 상태(State) 날아감 | **Stateless 앱(웹/API)에만 Spot 적용 (DB 적용 금지)** |
| 3. Spot Batch Failure | 2분 이내 배치 연산 안 끝나고 튕김 | **Checkpointing 기반 하차 후 재개(Resume) 로직** |

> 사례: **카카오 / 당근마켓 K8s EKS 클러스터 Worker 노드 80% Spot Fleet 적용 및 인프라 비용 70% 절감**

#### 한줄 요약

- 평균이 아니라 매일 유지되는 최소 좌석만 예약하고, 스팟 작업은 진행표를 밖에 보관하며 마감 시각 전에는 온디맨드로 넘어가도록 임계값을 둔다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Spot/RI 수립 기준(Spot and RI Standards)**: Base Load Compute Savings Plans, K8s Worker Spot Fleet Multi-AZ, Spot Handler 2분 훅 및 Stateful DB Spot 배제 원칙성에 의거한 체계.

</details>

- 안정 수요는 **Savings Plans**, 재시작 가능 작업은 Spot 적용

#### 한줄 요약

- 매일 필요한 좌석은 정기권으로 사고, 진행표를 들고 옮길 수 있는 일은 빈 좌석을 쓰며, 갑자기 늘어난 일은 일반 표로 처리한다.
