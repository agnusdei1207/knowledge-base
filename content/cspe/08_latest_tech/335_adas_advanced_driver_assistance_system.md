---
title: "ADAS 첨단운전자지원 (Advanced Driver Assistance System)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 335
extra:
  question_no: "335"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- ADAS는 운전자를 대체하는 시스템이 아니라 인지와 판단과 제어 일부를 보조하는 안전 기능 집합임
- 대표 기능으로 AEB와 ACC와 LKA와 BSD 같은 경고 및 개입 기능이 포함됨
- 센서 품질과 HMI 설계와 운전자 인계 기준이 안전 효과를 크게 좌우함

## Ⅰ. 개요

- **정의/개념**: ADAS는 카메라와 레이더와 초음파와 제어 로직을 활용해 운전자의 인지와 판단과 조작을 보조함으로써 사고 예방과 주행 편의 향상을 지원하는 차량 안전 보조 시스템임
- **배경/필요성**: 운전자는 피로와 사각지대와 반응 지연으로 위험 상황을 늦게 인지할 수 있어 센서 기반 보조 시스템을 통해 사고 가능성을 줄일 필요가 커짐

## Ⅱ. 특징

- 경고와 개입을 통해 충돌 위험을 조기에 줄이는 능동 안전 성격이 강함
- 센서 융합을 통해 단일 센서보다 인지 정확도와 환경 대응 범위를 넓힘
- 운전자 편의 기능과 안전 기능이 결합되어 상용화 확산 속도가 빠름
- 과도한 시스템 신뢰나 오경고 누적은 운전자 오용과 무시를 동시에 유발할 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Passive Safety | ADAS | ADS |
|:---|:---|:---|:---|
| 개입 시점 | 사고 후 피해 완화 | 사고 전 보조 개입 | 특정 조건에서 주행 수행 |
| 운전자 역할 | 전적 책임 | 주 책임 유지 | 조건부 또는 시스템 책임 |
| 대표 기술 | 에어백, 차체 구조 | AEB, ACC, LKA | Level 3+ 자동운전 |
| 핵심 가치 | 피해 감소 | 위험 예방과 편의 | 자율 주행 자동화 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Sensor Suite | 카메라와 레이더와 초음파가 주변 객체와 차선과 거리 정보를 수집해 ADAS 인지의 기본 입력을 형성함 |
| Perception and Fusion Module | 여러 센서 정보를 결합해 객체와 차선과 위험 상황을 더 정확히 판단하는 인지 계층임 |
| Decision and Warning Logic | 충돌 위험과 차선 이탈과 운전자 상태를 평가해 경고 또는 개입 여부를 결정하는 판단 계층임 |
| Actuation Interface | 제동과 조향과 가감속 제어를 차량 시스템에 전달해 실제 보조 개입을 수행하는 실행 계층임 |
| HMI and Driver Monitoring | 운전자에게 상태와 경고를 전달하고 주의 수준을 확인해 사람과 시스템 협력 안정성을 높이는 인터페이스 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Sensors     | -> | Perception  | -> | Decision    | -> | Warning /   |
|             |    | / Fusion    |    | Logic       |    | Actuation   |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 주변 환경 감지 | -> | 센서 융합 분석 | -> | 위험도 평가    | -> | 경고/개입 결정 | -> | 운전자/차량 반응 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **주변 환경 감지**: 센서가 차량 주변 상황을 수집함
2. **센서 융합 분석**: 객체와 차선과 거리 정보를 통합 판단함
3. **위험도 평가**: 충돌 가능성과 이탈 위험을 계산함
4. **경고와 개입 결정**: 경보 또는 제동과 조향 보조를 실행함
5. **운전자와 차량 반응**: 결과를 운전자에게 알리고 차량 제어에 반영함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 악천후와 역광과 센서 오염 상황에서 인지 성능이 저하되면 오경고와 미경고가 동시에 증가할 수 있음
   - 해결방안: sensor degradation aware fusion과 environmental robustness validation을 적용하고 false alert rate under adverse weather와 missed critical event rate로 검증함
2. 문제: 운전자가 시스템을 과신하면 ADAS의 한계를 넘는 상황에서도 적절한 개입을 늦춰 안전 위험이 커질 수 있음
   - 해결방안: driver attention monitoring과 limitation explicit HMI design을 적용하고 driver takeover response time와 misuse incident count로 검증함
3. 문제: 차량별 옵션 구성과 센서 조합이 다르면 동일 기능이라도 성능 편차와 검증 복잡도가 크게 늘어날 수 있음
   - 해결방안: feature variant governance와 configuration aware verification matrix를 적용하고 variant specific defect escape rate와 test coverage across sensor configurations로 검증함

## Ⅶ. 적용 사례

- ADAS 검증 조직이 열악 환경 융합 검증을 운영하며 확인 지표는 false alert rate under adverse weather와 missed critical event rate임
- 차량 UX 팀이 한계 명시형 HMI를 적용하며 확인 지표는 driver takeover response time와 misuse incident count임
- 품질 보증 부문이 변형 조합 검증 매트릭스를 운영하며 확인 지표는 variant specific defect escape rate와 test coverage across sensor configurations로 검증함

## Ⅷ. 결론

ADAS는 센서와 알고리즘의 성능만이 아니라 운전자와의 역할 분담이 안전성을 결정하므로 인지 강건성과 HMI 설계가 함께 완성되어야 함.
