---
sidebar:
  order: 40
  label: "040. 데이터센터 물 사용 효율 지표 (WUE, Water Usage Effectiveness)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "데이터센터 물 사용 효율 지표 (WUE, Water Usage Effectiveness)"
date: "2026-08-16T17:16:00+09:00"
tags:
  - "notes-evaluation"
weight: 40
extra:
  question_no: "040"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "최근 기출, 냉각수 효율을 재는 환경 지표"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **물사용효율(Water Usage Effectiveness, WUE)**: 데이터센터의 연간 물 사용량을 순수 IT 장비의 연간 소비 전력량으로 나눈 수자원 효율 평가 표준 지표.
- **데이터센터 수자원 효율(Data Center Water Efficiency)**: 증발식 냉각탑 등으로 인한 막대한 수자원 소비를 줄이고 수자원 재활용률을 높이는 친환경 관리 체계.
- **지속가능성 지표(Sustainability Metrics)**: PUE(전력), CUE(탄소)와 함께 데이터센터의 친환경 ESG 성과를 종합 평가하는 주요 3대 지표.

</details>

- 정의/개념: 현장 물 사용량을 IT 에너지로 나눈 **WUE** 지표
- 배경/필요성: 절대 물 사용량만으로는 **부하 대비 효율 비교 불가**

#### 한줄 요약
- IT 에너지 1kWh당 **현장 물 소비량** 평가

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **연간 물 소비량 대비 IT 전력 비율(Annual Water / IT Energy)**: WUE = (연간 총 물 소비량(L)) / (연간 IT 장비 전력 소비량(kWh))로 산출되며, 수치가 낮을수록 물 효율이 우수.
- **냉각탑 증발수 관리(Cooling Tower Evaporation)**: 수랭식 냉각탑의 증발 및 비산으로 인한 수자원 고갈 리스크를 억제하는 핵심 관리 영역.
- **PUE-WUE 상충 관계(PUE vs WUE Trade-off)**: 증발 냉각을 강화하면 전력 효율(PUE)은 개선되나 물 소비(WUE)가 급증하는 상충 관계 최적화 필요.

</details>

- **현장 물 사용**을 L/kWh로 정규화
- 현장과 발전소의 **간접 물 사용** 경계 분리
- **전력-물 상충**과 PUE 변화 동시 평가
- **ISO/IEC 30134-9** 기반 측정·보고

#### 한줄 요약
- WUE 개선의 **PUE·탄소 풍선 효과** 동시 검증

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **냉각탑 증발 및 비산수(Evaporation & Drift Water)**: 냉동기 응축열을 대기로 방출하는 과정에서 증발 및 바람에 날려 손실되는 냉각수.
- **가습 및 수처리 설비(Humidification & Treatment)**: 전산실 적정 습도 유지를 위한 가습수 및 배관 부식/스케일 방지를 위한 화학 수처리수.
- **IT 장비 소비 전력(IT Equipment Energy)**: WUE 산출 공식의 분모가 되는 데이터센터 연간 IT 장비 전력 소비량(kWh).
- **재이용수 설비(Recycled/Rainwater System)**: 빗물 집수(Rainwater Harvesting), 중수도(Greywater) 재활용을 통해 상수도 소비를 억제하는 친환경 설비.

</details>

```text
[물 경계•용도 계측]   [IT 에너지 계측]
             \           /
                  [WUE 계산] ----- [지역 물 부족도]
                       |
               [물•전력 통합 분석]
```

선의 의미: 물·IT 계측과 지역 부족도를 통합 분석

| 구성요소 | 책임 및 평가 초점 |
|:---|:---|
| 물 경계•용도 계측 | 상수·지하수·**재이용수** 분리 계측 |
| IT 에너지 계측 | 동일 기간 **IT 장비 에너지** 측정 |
| WUE 계산 | 현장 물 사용량을 IT 에너지로 나눔 |
| 지역 물 부족도 | **물 부족도** 기반 지역 위험 가중 |
| 물•전력 통합 분석 | WUE·PUE·탄소·가용성 교차 평가 |

#### 한줄 요약
- 수원·용도·지역 부족도를 반영한 **WUE 평가**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **수자원 계측기 설치(Water Metering Installation)**: 냉각탑 급수관, 배수관, 가습 라인에 유량계(Flow Meter)를 설치하는 단계.
- **소비량 데이터 수집 및 분석(Water Consumption Monitoring)**: DCIM을 통해 일간/월간 수자원 소비량과 농축 배수(Blowdown) 주기를 모니터링하는 단계.
- **WUE 지표 산출 및 이상치 탐지(WUE Calculation)**: 연간 WUE를 계산하고 누수나 비효율 증발 구간을 조기 탐지하는 단계.
- **무수/폐루프 냉각 전환(Waterless Cooling Transition)**: 공랭식 프리쿨링 및 폐루프 액체 냉각을 도입하여 물 소비를 원천 감축하는 단계.

</details>

```text
              [운영자]
                  │ 1. 물 계측 경계•기간 확정
                  ▼
   ┌─────────────────┴─────────────────┐
   ▼ 2. 수원•용도별 물 사용량 집계       ▼ 3. IT 장비 에너지 집계
[용수계측기]                         [IT계측기]
   │ 물 사용량 전달                       │ IT 에너지 전달
   └─────────────────┬─────────────────┘
                     ▼
              [환경분석기]
                  │ 4. WUE•지역 물 부담 산출
                  │ 5. WUE•PUE•탄소•가용성 비교
                  │
                  ▼
              [운영자]
```

### 동작 원리

1. 물 계측 경계•기간 확정: 물·에너지의 범위와 기간 통일
2. 수원•용도별 물 사용량 집계: 수원·냉각·시설 용도 분리
3. IT 장비 에너지 집계: 동일 기간 IT 에너지 합산
4. WUE•지역 물 부담 산출: WUE와 지역 부족 위험 계산
5. WUE•PUE•탄소•가용성 비교: 냉각 대안의 풍선 효과 평가

#### 한줄 요약

- 동일 기간 WUE와 **PUE·탄소·가용성** 교차 검증

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **증발식 수랭 시스템(Evaporative Cooling, High WUE)**: 높은 열교환 효율로 PUE는 우수하나 막대한 물 소비로 가뭄 및 수자원 규제 위험에 노출되는 시스템.
- **공랭식 및 폐루프 냉각 시스템(Closed-loop / Air-cooled, Low/Zero WUE)**: 물을 대기에 증발시키지 않고 밀폐 순환하여 WUE를 0에 가깝게 낮추는 친환경 시스템.

</details>

| 데이터센터 물 환경 지속가능성 지표 | 현장 찐 소비량 (WUE) | 발전소 포함 꼬리표 (Source WUE) | 무식한 전체 톤수 (절대 물 사용량) |
|:---|:---|:---|:---|
| 실무 적용 잣대 및 타기팅 | 현장 냉각 물 효율 | 전력 공급망 물 영향 | 전체 취수 부담 |
| 핵심 측정 팩터 특징 | 현장 **물/IT 에너지** | 발전소 포함 물 부담 | 절대 물 사용량 |
| 한계 | 간접 물 미반영 | 전력원별 계수 불확실 | IT 부하 차이 미반영 |

> 물 부담은 WUE, 전력 부담은 **PUE**로 구분

#### 한줄 요약
- 현장 WUE와 발전소 포함 **간접 물 지표** 구분

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **냉각수 재이용(Water Recycling & Rainwater Harvesting)**: 하수 처리 재이용수나 빗물을 고도 정수하여 냉각수로 활용함으로써 상수도 의존도 탈피.
- **무수 액침 냉각(Waterless Immersion Cooling)**: 비전도성 유체를 활용한 직접 액체 냉각(Direct Liquid Cooling)으로 수자원 소비와 전력 소비를 동시 절감.
- **기후 환경별 냉각 믹스(Climate-adaptive Cooling Strategy)**: 습도와 기온이 높은 하절기에는 보조 수랭, 건조한 동절기에는 건식 공랭을 선택적으로 운용하는 하이브리드 전략.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 직접·간접 물 사용 혼합 | **전력원·측정 경계** 공개 | 환경 영향 분리 입증 |
| 가뭄 지역의 식수 소비 | 부족도 가중·**재이용수 우선** | 신선한 취수 부담 억제 |
| 물 절감의 전력·탄소 증가 | **전력-물 통합 판단** | 풍선 효과 방지 |

#### 한줄 요약
- 가뭄 지역은 **재이용수**와 저수량 냉각 우선

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **수자원 및 에너지 통합 지속가능 인프라(Integrated Water-Energy Sustainability)**: PUE와 WUE를 통합 모니터링하여 전력과 수자원 소비 간의 최적 균형점을 달성하는 차세대 친환경 데이터센터 운영 체계.

</details>

- 물 부족 지역은 재이용수를 우선하고 PUE·탄소 악화 시 재검토

#### 한줄 요약
- **지역 물 부족도·PUE**를 함께 보고 냉각 방식 선택
