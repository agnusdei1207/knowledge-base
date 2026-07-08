---
title: "In-Memory Computing 인메모리 컴퓨팅 (In-Memory Computing)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 249
extra:
  question_no: "249"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- In-Memory Computing은 메모리 셀 또는 메모리 어레이 내부에서 직접 연산을 수행하는 계산 방식임
- PIM보다 더 강하게 저장과 계산을 결합하는 경우가 많으며 아날로그 계산까지 포함할 수 있음
- 에너지 효율이 매우 높을 수 있지만 정확도와 공정 변동 관리가 어려운 편임

## Ⅰ. 개요

- **정의/개념**: In-Memory Computing은 메모리 어레이 내부에서 논리 연산이나 벡터 곱과 누산을 수행해 데이터 이동을 최소화하고 계산 에너지 효율을 높이는 비폰노이만형 컴퓨팅 방식임
- **배경/필요성**: AI와 데이터 분석에서 메모리 이동 비용이 전체 에너지와 지연의 큰 비중을 차지하면서 저장소 자체를 계산 자원으로 활용하려는 구조가 주목받음

## Ⅱ. 특징

- 저장과 계산의 물리적 거리를 거의 없애 데이터 이동 비용을 크게 줄임
- 디지털뿐 아니라 아날로그 저항 메모리 기반 계산도 가능함
- 행렬 연산 같은 대규모 병렬 계산에서 높은 효율 잠재력을 가짐
- 정확도 변동과 아날로그 노이즈와 소프트웨어 지원 부족이 과제임

## Ⅲ. 종류 및 비교

| 판단 기준 | In Memory Computing | PIM | Near Memory Computing |
|:---|:---|:---|:---|
| 연산 위치 | 메모리 셀 또는 어레이 내부 | 메모리 내부 또는 근접 로직 | 메모리 옆 전용 연산기 |
| 결합 강도 | 매우 높음 | 높음 | 중간 |
| 구현 난도 | 매우 높음 | 중간 | 중간 |
| 기대 효율 | 매우 높음 | 높음 | 중간 이상 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Memory Cell Array | 데이터를 저장하면서 동시에 연산 매체 역할을 수행하는 핵심 메모리 어레이임 |
| Sense and Compute Circuit | 읽기 회로와 계산 회로가 결합되어 셀 상태를 곧바로 연산 결과로 활용하는 회로 계층임 |
| Peripheral Logic | 입력 인코딩과 결과 후처리를 수행해 메모리 내 계산을 시스템과 연결하는 주변 제어 계층임 |
| Calibration Module | 공정 편차와 온도와 노이즈에 따른 계산 오차를 보정하는 안정화 계층임 |
| Software Mapping Layer | 어떤 연산을 인메모리 방식으로 바꿀지 결정하고 데이터 배치를 최적화하는 소프트웨어 계층임 |

```text
+-------------------+    +--------------------+    +-------------------+
| Memory Cell Array |<-> | Sense/Compute Cir. |<-> | Peripheral Logic  |
+-------------------+    +--------------------+    +-------------------+
                                      |
                                      v
                               +-------------------+
                               | Calibration / SW  |
                               +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 데이터 배치   | -> | 어레이 연산  | -> | 감지 및 변환 | -> | 오차 보정    | -> | 결과 사용    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **데이터 배치**: 계산 대상 데이터를 메모리 셀에 배치함
2. **어레이 연산**: 셀 상태와 전기적 특성을 이용해 연산을 수행함
3. **감지 및 변환**: 연산 결과를 읽어 시스템 표현으로 변환함
4. **오차 보정**: 편차와 노이즈를 보정함
5. **결과 사용**: 후속 추론이나 분석 단계에 결과를 전달함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 공정 편차와 아날로그 노이즈가 크면 계산 정확도와 재현성이 불안정해질 수 있음
   - 해결방안: calibration loop와 error compensation scheme을 적용하고 computation variance와 post calibration accuracy retention으로 검증함
2. 문제: 일반 소프트웨어 스택과 직접 연결이 어려우면 실제 개발과 운영 도입이 지연될 수 있음
   - 해결방안: compiler abstraction과 operator mapping library를 적용하고 software integration lead time과 supported operator coverage로 검증함
3. 문제: 특정 행렬 연산에는 강하지만 범용 워크로드에 그대로 적용하면 효율 이점이 약할 수 있음
   - 해결방안: workload specialization policy를 적용하고 acceleration hit rate와 non ideal workload slowdown ratio로 검증함

## Ⅶ. 적용 사례

- 아날로그 메모리 추론기가 보정 루프를 적용하며 확인 지표는 computation variance와 post calibration accuracy retention임
- 인메모리 가속 플랫폼이 연산자 매핑 라이브러리를 운영하며 확인 지표는 software integration lead time과 supported operator coverage임
- AI 추론 서비스가 적합 워크로드 선별 정책을 사용하며 확인 지표는 acceleration hit rate와 non ideal workload slowdown ratio임

## Ⅷ. 결론

In-Memory Computing은 메모리 이동 병목을 근본적으로 줄일 수 있지만 정확도 안정화와 소프트웨어 추상화가 상용화의 핵심 과제임.
