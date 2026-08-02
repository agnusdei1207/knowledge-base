---
sidebar:
  order: 198
  label: "198. 전력 사용 효과성 (PUE)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "전력 사용 효과성 (Power Usage Effectiveness)"
date: "2026-08-03T08:48:47+09:00"
tags:
  - "notes-latest-tech"
weight: 198
extra:
  question_no: "198"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "PUE 전력 효율 산정•개선이 138회 출제됨"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **전력 사용 효과성(Power Usage Effectiveness, PUE)**: 같은 기간의 데이터센터 총 시설 에너지를 IT 장비 에너지로 나눈 시설 효율 지표이다.
- **시설 오버헤드**: 냉각•배전•조명 등 IT 장비 외 설비가 소비하는 에너지이다.

</details>

$$PUE = \frac{\text{데이터센터 총 시설 에너지}}{\text{IT 장비 에너지}}$$

- 정의/개념: **전력 사용 효과성(Power Usage Effectiveness, PUE)** 은 같은 기간의 총 시설 에너지를 **정보기술(Information Technology, IT)** 장비 에너지로 나눈 비율
- 배경/필요성: 총전력량만으로는 정보기술 소비와 냉각•배전의 **시설 오버헤드** 구분 곤란

#### 한줄 요약

- 서버가 100을 쓰고 데이터센터 전체가 150을 쓰면 PUE는 1.5이며, 나머지 50은 냉각•배전 등의 시설 사용량이다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **데이터센터 인프라 효율(DCiE)**: 정보기술 에너지를 총 시설 에너지로 나누어 백분율로 표시한 전력 사용 효과성의 역수 지표이다.
- **해석 경계**: 전력 사용 효과성이 냉각•배전 효율만 나타내며 정보기술 작업 효율•탄소•물 사용량은 직접 나타내지 않는 범위이다.

</details>

- **국제표준화기구/국제전기기술위원회(International Organization for Standardization/International Electrotechnical Commission, ISO/IEC) 30134-2:2026** 기반 동일 경계•기간 계측
- **전력 사용 효과성(Power Usage Effectiveness, PUE)** 이 1에 가까울수록 비정보기술 오버헤드 감소•**데이터센터 인프라 효율(Data Center infrastructure Efficiency, DCiE)** 증가
- 부하•기후 영향을 고려한 정보기술 효율과 **탄소•물 지표 병행**
#### 한줄 요약

- 점수가 낮아도 서버가 일을 효율적으로 하는지는 알 수 없으므로 같은 조건의 시설 손실만 비교해야 한다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **총 시설 계측**: 정한 데이터센터 경계 안의 정보기술•배전•냉각•조명 에너지를 모두 측정하는 기능이다.
- **정보기술 장비 계측**: 서버•저장•네트워크 장비가 실제 사용한 에너지를 같은 기간에 측정하는 기능이다.

</details>

**정보기술(Information Technology, IT) 장비 계측** 과 총 시설 계측은 같은 경계와 기간을 사용한다.

```mermaid
block-beta
  columns 3
  N0["총 시설 계측"]
  N1["IT 장비 계측"]
  N2["경계•기간 명세"]
  N3["오버헤드 분해"]
  N4["보조 지표"]
  N0 --- N1 --- N2
  N2 --- N3 --- N4
```

| 구성요소 | 책임 |
|:---|:---|
| 총 시설 계측 | **경계 내 전체 에너지 측정** |
| IT 장비 계측 | 서버•저장•네트워크의 **에너지 측정** |
| 경계•기간 명세 | 계측 위치•범주와 **측정 기간** 고정 |
| 오버헤드 분해 | 냉각•배전과 **조명 손실** 분석 |
| 보조 지표 | IT 효율•탄소와 **물•신뢰성** 보완 |

#### 한줄 요약

- 건물 전체와 서버 전력을 같은 시간에 재고 그 차이를 냉각•배전 항목으로 나눈다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **동일 조건 비교**: 계측 경계•기간•IT 부하•외기 온도를 맞춰 개선 전후 PUE를 대조하는 방법이다.
- **오버헤드 분해**: 총 시설과 IT 에너지의 차이를 냉각•배전•조명 등 원인별로 나누는 분석이다.

</details>

```mermaid
sequenceDiagram
  participant O as 운영 조직
  participant M as 에너지 계측
    participant C as PUE 계산•손실 분석
  participant V as 검증 체계
  O->>M: 1. 측정 경계•기간 전달
  M->>C: 2. 총•IT 에너지 전달
    C->>C: 3. PUE•부하 손실 분석
    C->>V: 4. 오버헤드 개선안 전달
  V->>O: 5. 재측정 결과 전달
```

**동작 원리**

1. **측정 경계•기간 전달**: 시설•**정보기술(Information Technology, IT)** 의 **계측 위치•기간** 제공
2. **총•정보기술 에너지 전달**: 같은 기간의 **두 에너지 값** 제공
3. **전력 사용 효과성(Power Usage Effectiveness, PUE)•부하 손실 분석**: 산정 PUE와 **정보기술 부하•기후** 를 대조해 손실 원인 판정
4. **오버헤드 개선안 전달**: 냉각•배전 손실의 **개선 조건** 제공
5. **재측정 결과 전달**: 동일 조건의 PUE와 **총전력•서비스 수준 목표(Service Level Objective, SLO)** 제공

#### 한줄 요약

- 계절과 서버 부하를 함께 기록해야 냉각 조정이 실제로 시설 전력을 줄였는지 알 수 있다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **부분 전력 사용 효과성(pPUE)**: 명시한 구역•모듈의 총에너지를 해당 IT 에너지로 나눈 지표이다.
- **이상적 하한**: 총 시설 에너지가 IT 에너지보다 작을 수 없어 PUE가 이론적으로 가질 수 있는 최솟값 1이다.

</details>

| 시설 전력 효율 지표 | 전력 사용 효과성(Power Usage Effectiveness, PUE) | 부분 전력 사용 효과성(partial Power Usage Effectiveness, pPUE) | 데이터센터 인프라 효율(Data Center infrastructure Efficiency, DCiE) |
|:---|:---|:---|:---|
| 적용 기준 | 데이터센터 **전체 효율** | 구역•모듈별 **병목 진단** | **IT 전력 비중** 표시 |
| 핵심 특징 | **총 시설 / IT 에너지** | **부분 시설 / 부분 IT** | **IT / 총 시설 × 100** |
| 한계 | 경계•부하 차이에 따른 **비교 왜곡** | 전체 시설로 **일반화 불가** | PUE와 같은 정보의 **역수** |

#### 한줄 요약

- 전체 점수와 특정 구역 점수는 섞어 비교하지 않고, DCiE는 PUE를 반대로 표현한 값으로 본다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **부하•계절 영향**: 정보기술 사용률과 외기 온도 차이가 냉각•배전 에너지와 전력 사용 효과성을 바꾸는 효과이다.
- **단독 최적화**: 전력 사용 효과성만 낮추면서 총전력•물•탄소•장비 효율•서비스 신뢰성의 악화를 놓치는 접근이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| **계측 경계 차이** 미검증 시 서로 다른 설비 포함 범위로 전력 사용 효과성 비교 왜곡 | 계측 위치•포함 설비•기간을 명시하고 동일 조건 비교 | **전력 사용 효과성(Power Usage Effectiveness, PUE)** 동일 경계 비교성 확보 |
| **부하•계절 영향** 미검증 시 낮은 정보기술 부하나 기후 차이를 개선 효과로 오판 | **정보기술(Information Technology, IT)** 부하•외기 온도를 함께 기록하고 연간•부하구간별 분석 | 부하•계절 **효과 오판** 감소 |
| **PUE 단독 최적화** 미검증 시 총전력•물 사용•장비 효율•신뢰성 악화 | 총에너지, **물 사용 효과성(Water Usage Effectiveness, WUE)**, IT 작업 효율, 온도•**서비스 수준 목표(Service Level Objective, SLO)** 를 공동 검증 | 물•탄소•**신뢰성 악화** 방지 |

#### 한줄 요약

- 핵심 운영 위험마다 실행 가능한 대책과 검증 효과를 함께 확인한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **동일 경계 비교성**: 포함 설비•계측 위치•기간이 같아 두 전력 사용 효과성 값의 차이를 해석할 수 있는 성질이다.
- **보조 지표**: 전력 사용 효과성이 표현하지 못하는 물 사용 효과성•탄소•정보기술 작업 효율•서비스 수준 목표를 함께 판단하는 값이다.

</details>

- 시설 전체는 **전력 사용 효과성(Power Usage Effectiveness, PUE)**, 구역 병목은 **부분 전력 사용 효과성(partial Power Usage Effectiveness, pPUE)** 으로 비교하고 **물 사용 효과성(Water Usage Effectiveness, WUE)** 과 탄소 평가는 분리

#### 한줄 요약

- 핵심 판단 기준을 먼저 정한 뒤 적용 범위를 결정하는 것이 중요하다.
