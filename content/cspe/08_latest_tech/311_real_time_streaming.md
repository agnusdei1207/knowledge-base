---
title: "Real-time Streaming 실시간 스트리밍 (Real-time Streaming)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 311
extra:
  question_no: "311"
  exam_status: "기출"
  exam_history: "136회"
---

## 미리 알고가기

- Real-time Streaming은 끝이 정해지지 않은 이벤트 흐름을 지연을 낮게 유지하며 지속 처리하는 방식임
- event time과 processing time이 다를 수 있어 watermark와 window 개념이 중요함
- 정확도는 state 관리와 checkpoint와 sink 연계 방식에 크게 좌우됨

## Ⅰ. 개요

- **정의/개념**: Real-time Streaming은 연속적으로 발생하는 이벤트를 수집 즉시 상태 기반으로 처리해 지연을 최소화하면서 실시간 분석과 제어 결과를 만들어내는 데이터 처리 패러다임임
- **배경/필요성**: 사기 탐지와 운영 모니터링과 개인화 추천처럼 데이터 가치가 발생 시점에 가까울수록 커지는 업무가 늘면서 배치 중심 처리만으로는 의사결정 속도를 맞추기 어려워짐

## Ⅱ. 특징

- 무한 이벤트 흐름을 window와 state로 나누어 지속 처리함
- event time과 watermark를 사용해 지연 도착 데이터까지 고려한 정확도를 유지함
- 낮은 지연과 높은 처리량과 장애 복구 가능성을 동시에 설계해야 함
- sink 정합성과 backpressure 관리가 약하면 실시간성보다 운영 불안정이 먼저 드러날 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Batch Processing | Micro-batch Streaming | Real-time Streaming |
|:---|:---|:---|:---|
| 처리 단위 | 일정량 누적 후 일괄 처리 | 짧은 주기 배치 | 이벤트 연속 처리 |
| 지연 특성 | 높음 | 중간 | 낮음 |
| 상태 관리 | 단순함 | 중간 | 중요함 |
| 대표 용도 | 정산, 대규모 집계 | near real-time 분석 | FDS, 실시간 제어 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Event Producer | 애플리케이션과 센서와 로그 소스가 이벤트를 생성해 실시간 파이프라인의 시작점을 형성함 |
| Streaming Broker | 유입 속도와 처리 속도 차이를 완충하고 재처리용 로그를 보관해 안정적 전달을 지원하는 중간 버퍼 계층임 |
| Stream Processing Engine | 필터와 집계와 조인과 패턴 탐지를 상태 기반으로 수행해 실시간 비즈니스 로직을 실행하는 핵심 처리 계층임 |
| State and Checkpoint Store | 연산 상태와 오프셋을 저장해 장애 복구와 정확한 재처리의 기준점을 제공하는 신뢰 계층임 |
| Sink and Serving Layer | 경보와 대시보드와 캐시와 운영 시스템에 결과를 전달해 실시간 가치를 소비자에게 연결하는 출력 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| Producers   | -> | Broker      | -> | Stream Proc | -> | State Store | -> | Sinks       |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 이벤트 수집   | -> | 버퍼/분산 저장 | -> | 상태/윈도우 연산 | -> | 체크포인트    | -> | 결과 전달     |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **이벤트 수집**: 생산자가 이벤트를 지속 발행함
2. **버퍼와 분산 저장**: 브로커가 순서와 보관 정책에 따라 이벤트를 저장함
3. **상태와 윈도우 연산**: 엔진이 watermark와 state를 활용해 실시간 계산을 수행함
4. **체크포인트**: 처리 상태와 오프셋을 저장해 복구 지점을 만든다
5. **결과 전달**: sink에 경보와 지표와 후속 이벤트를 전달함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 이벤트 도착 순서가 뒤섞이고 지연이 커지면 윈도우 계산이 조기에 닫혀 실시간 분석 정확도가 떨어질 수 있음
   - 해결방안: event time standard와 adaptive watermark policy를 적용하고 late event drop rate와 window correction ratio로 검증함
2. 문제: 처리량 급증 시 backpressure가 누적되면 지연이 빠르게 커지고 실시간 SLA를 잃을 수 있음
   - 해결방안: autoscaling policy와 operator hotspot balancing을 적용하고 end to end latency와 consumer lag growth rate로 검증함
3. 문제: 상태 크기가 커진 스트리밍 작업은 체크포인트와 복구 시간이 길어져 장애 후 재가동 안정성이 떨어질 수 있음
   - 해결방안: state TTL governance와 incremental checkpoint strategy를 적용하고 checkpoint duration과 recovery time objective attainment rate로 검증함

## Ⅶ. 적용 사례

- 실시간 이상 탐지 플랫폼이 적응형 watermark를 운영하며 확인 지표는 late event drop rate와 window correction ratio임
- 이벤트 분석 서비스가 autoscaling을 적용하며 확인 지표는 end to end latency와 consumer lag growth rate임
- 상태 기반 스트림 연산이 증분 체크포인트를 도입하며 확인 지표는 checkpoint duration과 recovery time objective attainment rate임

## Ⅷ. 결론

Real-time Streaming은 빠른 처리만이 아니라 시간 의미와 상태 복구를 함께 설계해야 실제 실시간 가치가 유지됨.
