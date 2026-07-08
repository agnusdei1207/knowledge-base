---
title: "Water Usage Effectiveness 물사용효율 (Water Usage Effectiveness)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 326
extra:
  question_no: "326"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- WUE는 데이터센터가 IT 에너지 처리에 얼마나 많은 물을 사용했는지 보는 지표임
- WUE는 보통 $WUE = \frac{\text{Annual Site Water Usage}}{\text{IT Equipment Energy}}$로 계산하며 단위는 $L/kWh$를 많이 사용함
- 냉각 방식에 따라 PUE와 WUE가 서로 반대 방향으로 움직일 수 있어 함께 봐야 함

## Ⅰ. 개요

- **정의/개념**: Water Usage Effectiveness는 데이터센터가 냉각과 설비 운영을 위해 사용한 물의 양을 IT 장비 에너지 기준으로 나누어 수자원 효율을 평가하는 데이터센터 지속가능성 지표임
- **배경/필요성**: 고효율 냉각이 전력 절감에는 유리해도 지역 물 자원 부담을 키울 수 있어 데이터센터 지속가능성을 전력뿐 아니라 물 사용 관점에서도 평가할 필요가 커짐

## Ⅱ. 특징

- 냉각 전략이 지역 수자원에 미치는 영향을 계량적으로 보여줌
- 증발 냉각과 수냉 구조의 환경 tradeoff를 평가하기 좋음
- PUE와 함께 보면 에너지와 물의 상충 관계를 파악할 수 있음
- 지역 물 스트레스와 재활용수 사용 여부를 직접 반영하지 않아 해석 보완이 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | WUE | PUE | SCI |
|:---|:---|:---|:---|
| 측정 대상 | 물 사용 효율 | 전력 사용 효율 | 기능 단위 탄소 효율 |
| 주요 활용 | 냉각 방식 평가 | 시설 오버헤드 평가 | 소프트웨어 지속가능성 |
| 환경 관점 | 수자원 영향 | 에너지 영향 | 탄소 영향 |
| 한계 | 지역 물 스트레스 보완 필요 | 물 영향 미반영 | 시설 물 사용 직접 반영 약함 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Site Water Usage | 냉각과 가습과 설비 보조에 사용된 물 총량으로 WUE 분자의 핵심 항목이 되는 수자원 측정값임 |
| IT Equipment Energy | 서버와 스토리지와 네트워크 장비가 소비한 에너지로 물 사용 효율을 서비스 처리 기준에 연결하는 분모 항목임 |
| Cooling Method Profile | 증발 냉각과 수냉과 외기 냉방 같은 방식별 물 소비 특성을 반영해 WUE 해석에 맥락을 부여하는 기술 요소임 |
| Water Source and Reuse Policy | 상수도와 재활용수와 비음용수 활용 여부를 관리해 실제 지역 환경 부담을 줄이는 운영 정책 계층임 |
| Sustainability Review Layer | WUE와 PUE와 지역 물 스트레스 정보를 함께 비교해 냉각 전략의 전체 지속가능성을 판단하는 거버넌스 계층임 |

```text
+-------------------+
| Site Water Usage  |
+-------------------+
          |
          v
+-------------------+
| Divide by IT Load |
+-------------------+
          |
          v
+-------------------+
| WUE               |
+-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 물 사용 범위 정의 | -> | 물/IT 에너지 측정 | -> | WUE 계산     | -> | 냉각 방식 분석 | -> | 재활용/개선 반영 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **물 사용 범위 정의**: 어떤 용수 사용을 지표에 포함할지 정함
2. **물과 IT 에너지 측정**: 연간 물 사용과 IT 에너지를 수집함
3. **WUE 계산**: $WUE = \frac{\text{Annual Site Water Usage}}{\text{IT Equipment Energy}}$를 산정함
4. **냉각 방식 분석**: 물 사용 증가 원인과 냉각 구조 영향을 분석함
5. **재활용과 개선 반영**: 재활용수와 운전 최적화 정책을 적용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: WUE 수치만으로 지역 수자원 스트레스를 판단하면 동일 수치라도 환경 부담이 전혀 다른 지역 차이를 놓칠 수 있음
   - 해결방안: water stress weighted WUE review와 site context reporting을 적용하고 contextualized WUE coverage와 high stress site mitigation rate로 검증함
2. 문제: PUE 개선을 위해 수냉과 증발 냉각을 확대할 때 물 사용 증가가 숨겨지면 지속가능성 판단이 편향될 수 있음
   - 해결방안: PUE WUE joint governance와 cooling tradeoff approval process를 적용하고 energy water tradeoff detection rate와 approved mitigation action completion rate로 검증함
3. 문제: 재활용수와 비음용수 전략이 없으면 저WUE 목표를 달성해도 지역 상수 사용 부담은 계속 높게 남을 수 있음
   - 해결방안: recycled water sourcing program과 potable water reduction target을 적용하고 recycled water ratio와 potable water dependency reduction rate로 검증함

## Ⅶ. 적용 사례

- 데이터센터 거버넌스가 지역 맥락 포함 WUE 검토를 운영하며 확인 지표는 contextualized WUE coverage와 high stress site mitigation rate임
- 냉각 설계 조직이 PUE WUE 공동 심사를 적용하며 확인 지표는 energy water tradeoff detection rate와 approved mitigation action completion rate임
- 시설 운영팀이 재활용수 조달 전략을 도입하며 확인 지표는 recycled water ratio와 potable water dependency reduction rate임

## Ⅷ. 결론

WUE는 물 사용을 보이지 않게 남겨두지 않는 핵심 지표이므로 PUE와 지역 수자원 맥락을 함께 봐야 실제 친환경 운영 판단이 가능함.
