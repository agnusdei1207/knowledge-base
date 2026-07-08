---
title: "Software Carbon Intensity 소프트웨어 탄소집약도 (Software Carbon Intensity)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 322
extra:
  question_no: "322"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- SCI는 소프트웨어 기능 단위당 탄소 배출량을 보는 지표임
- SCI는 보통 $SCI = \frac{(E \times I) + M}{R}$로 표현하며 여기서 $E$는 전력 사용량, $I$는 전력 탄소 강도, $M$은 배분된 embodied emission, $R$은 기능 단위임
- 총 배출량만 보는 것보다 요청 1건이나 학습 1회 같은 서비스 단위 효율을 비교하기에 적합함

## Ⅰ. 개요

- **정의/개념**: Software Carbon Intensity는 소프트웨어가 특정 기능 단위를 처리하는 과정에서 발생시키는 탄소 배출량을 측정해 서비스 효율성과 지속가능성을 비교하게 하는 기능 단위 기반 탄소 지표임
- **배경/필요성**: 전체 인프라 전력량만으로는 어떤 서비스와 기능이 실제로 배출 개선을 이끌었는지 판단하기 어려워 소프트웨어 수준의 탄소 효율 지표가 필요해짐

## Ⅱ. 특징

- 기능 단위당 배출량을 보므로 규모가 다른 서비스 간 비교가 가능함
- 운영 전력뿐 아니라 하드웨어에 배분된 embodied emission까지 반영할 수 있음
- 코드 최적화와 자원 배치와 탄소인지 실행 정책 효과를 하나의 지표로 연결하기 좋음
- 측정 경계와 기능 단위 정의가 불명확하면 조직 간 비교와 내부 추세 해석이 왜곡될 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | SCI | Total Carbon Emission | PUE |
|:---|:---|:---|:---|
| 측정 초점 | 기능 단위당 배출 | 전체 배출 총량 | 시설 전력 효율 |
| 비교 가능성 | 서비스 간 높음 | 규모 의존 큼 | 시설 비교 중심 |
| 소프트웨어 개선 반영 | 직접적 | 제한적 | 간접적 |
| 대표 활용 | 요청당 탄소 관리 | ESG 총량 보고 | 데이터센터 운영 효율 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Energy Consumption $E$ | 소프트웨어가 실행되는 동안 사용한 전력량을 나타내며 runtime efficiency를 평가하는 가장 직접적인 입력값임 |
| Grid Carbon Intensity $I$ | 전력이 공급된 시간과 지역의 탄소 강도를 반영해 동일 전력 사용도 배출량이 다를 수 있음을 설명하는 환경 계수임 |
| Embodied Emission $M$ | 서버와 장비 제조 과정의 탄소를 서비스에 배분해 운영 전력 외의 하드웨어 환경 비용까지 반영하는 항목임 |
| Functional Unit $R$ | 요청 수와 거래 건수와 학습 횟수처럼 비교 기준이 되는 기능 단위를 정의해 SCI를 실무 지표로 만드는 기준 축임 |
| Boundary and Allocation Rule | 어떤 시스템 범위와 배분 방식을 쓸지 정해 수치 일관성과 조직 간 해석 가능성을 유지하는 측정 통제 계층임 |

```text
+-------------+    +-------------+    +-------------+
| Energy E    | +  | Embodied M  | -> | Emissions   |
+-------------+    +-------------+    +-------------+
        |
        v
+-------------+    +-------------+
| Carbon I    | -> | Divide by R |
+-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 경계 정의     | -> | 전력/탄소 수집 | -> | 기능 단위 산정 | -> | SCI 계산     | -> | 개선 우선순위 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **경계 정의**: 어떤 시스템과 시간 범위를 측정할지 정함
2. **전력과 탄소 수집**: 전력 사용량과 지역별 탄소 강도를 수집함
3. **기능 단위 산정**: 요청 수나 배치 건수 같은 산출 기준을 정의함
4. **SCI 계산**: $SCI = \frac{(E \times I) + M}{R}$로 기능 단위당 배출량을 계산함
5. **개선 우선순위 설정**: SCI가 높은 워크로드를 찾아 개선함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 기능 단위를 부적절하게 정의하면 같은 서비스라도 SCI 수치가 과대 또는 과소 평가되어 개선 우선순위가 왜곡될 수 있음
   - 해결방안: business aligned functional unit design과 metric governance review를 적용하고 SCI interpretability score와 unit redefinition frequency로 검증함
2. 문제: 지역과 시간별 탄소 강도 데이터를 정밀하게 연결하지 못하면 실제 배출과 SCI 계산값 차이가 커질 수 있음
   - 해결방안: granular carbon signal integration과 timestamp aligned measurement를 적용하고 carbon data alignment accuracy와 estimated versus actual emission gap로 검증함
3. 문제: embodied emission 배분 기준이 제각각이면 조직 간 SCI 비교와 투자 판단의 신뢰성이 떨어질 수 있음
   - 해결방안: embodied allocation standard와 infrastructure tagging discipline를 적용하고 embodied allocation consistency score와 asset attribution coverage로 검증함

## Ⅶ. 적용 사례

- SaaS 조직이 업무 정렬 기능 단위를 정의하며 확인 지표는 SCI interpretability score와 unit redefinition frequency임
- 멀티리전 플랫폼이 시간 정렬 탄소 신호를 연계하며 확인 지표는 carbon data alignment accuracy와 estimated versus actual emission gap임
- 클라우드 운영팀이 embodied 배분 표준을 적용하며 확인 지표는 embodied allocation consistency score와 asset attribution coverage임

## Ⅷ. 결론

SCI는 총량이 아닌 기능 효율을 보는 지표이므로 측정 경계와 기능 단위와 배분 기준을 명확히 할 때만 Green Software 개선 지표로 의미가 생김.
