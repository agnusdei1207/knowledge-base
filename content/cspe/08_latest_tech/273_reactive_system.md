---
title: "Reactive System 리액티브 시스템 (Reactive System)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 273
extra:
  question_no: "273"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- 리액티브 시스템은 반응성만이 아니라 탄력성과 복원력과 메시지 기반 상호작용을 함께 갖춘 시스템을 의미함
- 비동기 프로그래밍과 혼동하기 쉬우나 더 넓은 아키텍처 원칙임
- Reactive Manifesto의 네 축을 구조적 관점에서 이해해야 함

## Ⅰ. 개요

- **정의/개념**: Reactive System은 사용자와 외부 이벤트에 신속히 응답하면서도 장애와 부하 변화에 견디도록 메시지 기반 비동기 상호작용과 탄력적 확장과 복원력을 갖춘 시스템 아키텍처임
- **배경/필요성**: 대규모 분산 서비스는 응답 지연과 장애 전파와 급격한 부하 변동이 빈번해 전통적 동기 결합 구조만으로는 안정성과 확장성을 유지하기 어려워짐

## Ⅱ. 특징

- 반응성으로 사용자 체감 응답성을 유지함
- 복원력으로 부분 장애가 전체 실패로 번지지 않게 함
- 탄력성으로 부하 변화에 따라 자원을 조절함
- 메시지 기반 비동기로 결합도를 낮추고 격리를 강화함

## Ⅲ. 종류 및 비교

| 판단 기준 | Reactive System | 전통적 동기식 시스템 | 단순 비동기 처리 |
|:---|:---|:---|:---|
| 결합도 | 낮음 | 높음 | 중간 |
| 장애 격리 | 높음 | 낮음 | 중간 |
| 확장성 | 높음 | 중간 | 중간 |
| 핵심 가치 | 반응성, 탄력성, 복원력 | 단순성 | 처리 분산 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Event Source | 사용자 요청과 센서와 외부 메시지처럼 시스템 반응을 유발하는 입력 원천임 |
| Message Channel | 컴포넌트 간 비동기 통신을 담당해 직접 결합을 줄이고 버퍼 역할을 수행하는 전달 계층임 |
| Reactive Component | 이벤트를 소비하고 상태를 변경하고 결과를 발행하는 독립 실행 컴포넌트임 |
| Elastic Runtime | 부하에 따라 컴포넌트 인스턴스를 확장하거나 축소하는 실행 환경임 |
| Failure Isolation Layer | 회로 차단과 재시도와 격리를 통해 장애 전파를 제한하는 복원 계층임 |

```text
+-------------+    +----------------+    +----------------+
| Event Source| -> | Message Channel| -> | Reactive Comp. |
+-------------+    +----------------+    +----------------+
                                     \-> Elastic / Failure Control
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 이벤트 발생   | -> | 메시지 전달  | -> | 비동기 처리   | -> | 상태 반영    | -> | 확장 또는 복구 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **이벤트 발생**: 외부 요청이나 상태 변화가 입력됨
2. **메시지 전달**: 채널이 이벤트를 대상 컴포넌트에 전달함
3. **비동기 처리**: 컴포넌트가 독립적으로 작업을 수행함
4. **상태 반영**: 결과를 저장하거나 다음 이벤트를 발행함
5. **확장 또는 복구**: 부하와 장애 상태에 따라 자동 조정함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 비동기 메시지 경로가 많아질수록 흐름 추적이 어려워 장애 원인 분석 시간이 길어질 수 있음
   - 해결방안: end to end tracing과 correlation id standard를 적용하고 trace completeness rate와 root cause isolation time으로 검증함
2. 문제: 메시지 폭주 상황에서 backpressure 설계가 없으면 큐 적체와 지연 급증이 발생할 수 있음
   - 해결방안: backpressure protocol과 bounded queue policy를 적용하고 queue saturation rate와 p99 processing latency로 검증함
3. 문제: 컴포넌트 분할이 지나치면 관리 오버헤드가 커져 오히려 운영 복잡도가 상승할 수 있음
   - 해결방안: domain driven partition review와 service granularity governance를 적용하고 inter service call amplification rate와 operational complexity score로 검증함

## Ⅶ. 적용 사례

- 이벤트 처리 플랫폼이 correlation id 기반 추적을 운영하며 확인 지표는 trace completeness rate와 root cause isolation time임
- 실시간 주문 시스템이 backpressure 정책을 적용하며 확인 지표는 queue saturation rate와 p99 processing latency임
- 대규모 마이크로서비스가 경계 재검토를 수행하며 확인 지표는 inter service call amplification rate와 operational complexity score임

## Ⅷ. 결론

Reactive System은 비동기 처리 기법을 넘어 반응성과 복원력과 탄력성을 함께 설계하는 아키텍처이므로 메시지 흐름 통제와 장애 격리가 핵심임.
