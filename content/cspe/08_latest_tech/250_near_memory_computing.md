---
title: "Near-Memory Computing 근접 메모리 컴퓨팅 (Near-Memory Computing)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 250
extra:
  question_no: "250"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Near-Memory Computing은 메모리 안이 아니라 메모리 바로 옆에 연산기를 배치해 데이터 이동을 줄이는 구조임
- PIM과 IMC보다 구현 난이도와 정확도 부담이 낮아 현실적 절충안으로 자주 언급됨
- 메모리 계층 설계와 작업 분할 정책이 성능 효과를 크게 좌우함

## Ⅰ. 개요

- **정의/개념**: Near-Memory Computing은 메모리 모듈이나 패키지 근처에 전용 연산 유닛을 배치해 저장과 계산 사이 거리를 줄이고 메모리 병목을 완화하는 컴퓨팅 구조임
- **배경/필요성**: 메모리 내부 연산은 구현 난도가 높고 범용성 제약이 커서 보다 현실적인 대안으로 메모리 근접 연산 구조가 주목받음

## Ⅱ. 특징

- 메모리 이동량 감소 효과를 얻으면서도 메모리 셀 자체 변경은 최소화할 수 있음
- 디지털 연산기 중심이라 정확도와 디버깅 면에서 상대적으로 유리함
- 데이터 배치와 오프로딩 정책이 성능을 결정함
- 메모리 내부 연산보다 범용성이 높지만 이동 비용 절감 효과는 다소 낮을 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Near Memory Computing | In Memory Computing | 전통적 CPU 중심 구조 |
|:---|:---|:---|:---|
| 연산 위치 | 메모리 근처 전용 연산기 | 메모리 셀 또는 어레이 내부 | 원거리 프로세서 |
| 구현 난도 | 중간 | 높음 | 낮음 |
| 범용성 | 중간 이상 | 낮음 | 높음 |
| 이동 절감 효과 | 높음 | 매우 높음 | 낮음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Memory Module | 대량 데이터를 저장하며 근접 연산 유닛에 빠르게 공급하는 저장 계층임 |
| Near Memory Engine | 필터링과 집계와 벡터 연산을 메모리 바로 옆에서 수행하는 전용 계산 유닛임 |
| Interconnect Path | 메모리와 근접 연산기와 호스트를 연결해 지연을 최소화하는 고속 경로임 |
| Offload Controller | 어떤 연산을 근접 메모리 엔진으로 보낼지 결정하고 실행 순서를 조정하는 제어 계층임 |
| Runtime and Scheduler | 워크로드 분배와 메모리 계층 정책을 관리해 전체 처리 효율을 높이는 소프트웨어 계층임 |

```text
+-------------+    +-------------------+    +----------------+
| Host CPU/GPU| -> | Near Memory Engine| <->| Memory Module  |
+-------------+    +-------------------+    +----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 워크로드 분류 | -> | 연산 오프로딩 | -> | 근접 처리    | -> | 부분 결과 반환 | -> | 후속 계산    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **워크로드 분류**: 데이터 이동이 큰 연산을 선별함
2. **연산 오프로딩**: 적합한 작업을 근접 메모리 엔진에 보냄
3. **근접 처리**: 메모리 인근에서 필터링과 집계를 수행함
4. **부분 결과 반환**: 축약된 결과를 호스트로 전달함
5. **후속 계산**: 남은 복잡한 연산을 CPU나 가속기가 마무리함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 어떤 연산을 오프로딩할지 기준이 없으면 데이터 이동 절감보다 오프로딩 오버헤드가 더 커질 수 있음
   - 해결방안: workload classifier와 offload policy tuning을 적용하고 offload efficiency ratio와 unnecessary offload rate로 검증함
2. 문제: 메모리 계층과 근접 연산기의 자원 균형이 맞지 않으면 일부 경로가 병목이 되어 기대 성능이 나오지 않을 수 있음
   - 해결방안: bandwidth balanced architecture와 scheduler tuning을 적용하고 memory engine utilization balance와 end to end latency로 검증함
3. 문제: 호스트 소프트웨어와의 통합이 미흡하면 프로그래밍 모델 복잡도로 인해 실제 활용률이 낮아질 수 있음
   - 해결방안: runtime abstraction과 library based offload API를 적용하고 developer productivity score와 feature utilization rate로 검증함

## Ⅶ. 적용 사례

- 분석 서버가 워크로드 분류 기반 오프로딩을 적용하며 확인 지표는 offload efficiency ratio와 unnecessary offload rate임
- AI 추론 장치가 메모리와 엔진 균형 설계를 수행하며 확인 지표는 memory engine utilization balance와 end to end latency임
- 데이터 처리 플랫폼이 라이브러리형 오프로딩 API를 제공하며 확인 지표는 developer productivity score와 feature utilization rate임

## Ⅷ. 결론

Near-Memory Computing은 메모리 병목 완화를 위한 현실적 절충안이므로 오프로딩 정책과 메모리 계층 균형과 개발 추상화가 성공의 핵심임.
