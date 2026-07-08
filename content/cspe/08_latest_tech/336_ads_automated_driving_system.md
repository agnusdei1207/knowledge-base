---
title: "ADS 자율주행시스템 (Automated Driving System)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 336
extra:
  question_no: "336"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- ADS는 특정 ODD 안에서 동적 주행 과업을 시스템이 수행하는 자동운전 체계를 뜻함
- ADAS와 달리 운전자 보조를 넘어서 인지와 판단과 제어와 fallback을 시스템이 맡는 범위가 있음
- 센서 성능보다 ODD 정의와 안전 사례와 fallback 설계가 실제 상용성의 핵심임

## Ⅰ. 개요

- **정의/개념**: Automated Driving System은 정의된 ODD 안에서 주변 환경 인지와 경로 판단과 차량 제어와 최소 위험 상태 전환까지 수행해 주행 과업을 시스템이 책임지는 자율주행 체계임
- **배경/필요성**: 운전 피로와 사고 감소와 이동 서비스 자동화 요구가 커지면서 단순 운전자 보조를 넘어 특정 조건에서 시스템이 주행을 맡는 구조가 필요해짐

## Ⅱ. 특징

- ODD 범위를 명확히 정의하고 그 범위 안에서 시스템 책임이 성립함
- 인지와 예측과 계획과 제어가 폐루프 구조로 연동됨
- 이상 상황에서 fallback이나 최소 위험 상태 전환이 필수 요구임
- edge case와 분포 변화 대응이 어려워 검증과 인증 비용이 매우 큼

## Ⅲ. 종류 및 비교

| 판단 기준 | SAE Level 2 | SAE Level 3 | SAE Level 4+ |
|:---|:---|:---|:---|
| 시스템 역할 | 보조 | 조건부 자동운전 | 고도 자동운전 |
| 운전자 책임 | 상시 책임 | 인계 요청 시 개입 | ODD 내 시스템 책임 우세 |
| ODD 제약 | 상대적으로 넓음 | 명확히 정의 | 매우 엄격히 정의 |
| fallback 주체 | 운전자 | 시스템 + 운전자 인계 | 시스템 중심 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Sensor and Perception Stack | 카메라와 라이다와 레이더와 지도 정보를 활용해 객체와 차선과 주변 환경을 인지하는 입력 계층임 |
| Localization and World Model | 차량 위치와 주변 상태를 통합 표현해 계획 알고리즘이 사용할 주행 문맥을 구성하는 상황 모델 계층임 |
| Prediction and Planning Engine | 타 객체의 움직임을 예측하고 안전 경로와 행동을 결정해 자율주행 의사결정을 수행하는 핵심 판단 계층임 |
| Control and Fallback Module | 조향과 제동과 가속 제어를 수행하고 이상 시 최소 위험 상태 전환을 담당하는 실행 안전 계층임 |
| ODD and Safety Monitor | 운행 조건 적합 여부와 센서 건강도와 시스템 한계를 감시해 ADS 책임 범위를 실시간으로 관리하는 감독 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Sensors /   | -> | Perception  | -> | Planning    | -> | Control /   |
| Map         |    | / World     |    | / Prediction|    | Fallback    |
+-------------+    +-------------+    +-------------+    +-------------+
                              ^
                              |
                     +-----------------+
                     | ODD / Safety Mon|
                     +-----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 환경 감지     | -> | 상황 모델 생성 | -> | 경로/행동 계획 | -> | 차량 제어     | -> | ODD/위험 감시 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **환경 감지**: 센서가 주변 객체와 도로 상태를 수집함
2. **상황 모델 생성**: 위치와 맥락을 통합한 world model을 구성함
3. **경로와 행동 계획**: 안전 경로와 속도와 차선 변경을 결정함
4. **차량 제어**: 조향과 가감속 명령을 실행함
5. **ODD와 위험 감시**: 한계 초과 시 fallback이나 인계를 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: ODD 정의가 모호하면 시스템이 처리 가능한 범위를 벗어난 상황에서도 주행을 지속해 안전 위험이 커질 수 있음
   - 해결방안: explicit ODD contract와 runtime boundary monitoring을 적용하고 ODD violation detection rate와 unsafe ODD continuation incident count로 검증함
2. 문제: long tail edge case 검증이 부족하면 실제 도로에서 드문 상황이 치명적 실패로 이어질 수 있음
   - 해결방안: scenario based validation at scale과 simulation plus field feedback loop를 적용하고 critical scenario coverage와 unknown edge case recurrence rate로 검증함
3. 문제: fallback 전환과 운전자 인계 설계가 약하면 Level 3 환경에서 책임 전환 실패가 발생할 수 있음
   - 해결방안: minimum risk maneuver design과 takeover readiness monitoring을 적용하고 takeover success rate and minimum risk maneuver completion rate로 검증함

## Ⅶ. 적용 사례

- 자율주행 개발 조직이 ODD 계약 기반 감시를 운영하며 확인 지표는 ODD violation detection rate와 unsafe ODD continuation incident count임
- 시뮬레이션 검증 플랫폼이 long tail 시나리오 검증을 확대하며 확인 지표는 critical scenario coverage와 unknown edge case recurrence rate임
- Level 3 차량 프로그램이 인계 준비도 모니터링을 적용하며 확인 지표는 takeover success rate and minimum risk maneuver completion rate임

## Ⅷ. 결론

ADS는 센서 기술보다 ODD와 fallback과 검증 체계가 더 핵심이므로 시스템 책임 범위를 명확히 관리하는 안전 설계가 우선되어야 함.
