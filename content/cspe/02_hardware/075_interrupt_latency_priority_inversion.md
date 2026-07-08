---
title: "인터럽트 레이턴시·우선순위 역전 (Interrupt Latency Priority Inversion)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 75
extra:
  question_no: "075"
  exam_status: "기출"
  exam_history: "137회"
---

## 미리 알고가기

- interrupt latency는 인터럽트 요청부터 ISR 첫 실행까지의 지연 시간임
- priority inversion은 높은 우선순위 태스크가 낮은 우선순위 태스크 보유 자원 때문에 대기하는 현상임
- 실시간 시스템에서는 둘 다 deadline miss의 직접 원인이 됨

## Ⅰ. 개요

- **정의/개념**: 인터럽트 레이턴시와 우선순위 역전은 실시간 시스템에서 이벤트 처리와 태스크 스케줄링이 지연되는 대표 문제로, 외부 이벤트 응답 상한과 자원 접근 질서를 동시에 관리해야 함을 보여주는 개념임
- **배경/필요성**: 제어 시스템은 센서 이벤트를 즉시 처리해야 하고 높은 우선순위 태스크가 중요한 제어를 수행하므로, 인터럽트 지연과 자원 경합은 곧 시스템 안정성 저하로 이어짐

## Ⅱ. 특징

- interrupt latency는 ISR 길이와 마스킹 정책과 커널 설계에 영향받음
- priority inversion은 mutex와 공유 자원 사용 시 숨어 있다가 심각한 지연을 만들 수 있음
- 두 문제 모두 평균 성능보다 worst-case 지연을 악화시킴
- 우선순위 설계와 동기화 정책을 함께 봐야 근본 원인을 찾을 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | 인터럽트 레이턴시 문제 | 우선순위 역전 문제 |
|:---|:---|:---|
| 발생 위치 | IRQ, ISR 경로 | 태스크 동기화 경로 |
| 직접 원인 | 긴 마스킹, ISR, 커널 비결정성 | 낮은 우선순위 태스크의 자원 점유 |
| 영향 | 이벤트 응답 지연 | 고우선 태스크 지연 |
| 대표 대응 | ISR 최소화 | priority inheritance, ceiling |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| IRQ, ISR Path | 인터럽트 요청과 서비스 루틴 경로가 응답 상한을 결정함 |
| Scheduler, Priority Queue | 태스크 우선순위 정책이 지연 전파 범위를 결정함 |
| Mutex, Shared Resource | 공유 자원 보호 방식이 우선순위 역전 발생 여부를 좌우함 |
| Monitoring, Tracing | latency와 blocking time을 계측해 원인을 재현 가능하게 함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 이벤트/자원 요청 | --> | ISR 또는 락 대기 | --> | 지연 누적      | --> | 우선순위 보정/최적화 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **이벤트 및 자원 요청**: 인터럽트나 태스크가 실행 자원을 요청함
2. **ISR 또는 락 대기**: 마스킹과 자원 점유 때문에 지연이 발생함
3. **지연 누적**: high-priority 태스크나 센서 응답이 밀림
4. **우선순위 보정 및 최적화**: 상속과 ceiling과 ISR 축소로 문제를 줄임

## Ⅵ. 문제점 및 해결 방안

1. 문제: ISR가 길고 인터럽트 마스킹 구간이 넓으면 중요한 외부 이벤트가 제때 처리되지 못할 수 있음
   - 해결방안: ISR를 최소화하고 deferred work로 분리하며 interrupt latency와 jitter로 검증함
2. 문제: 낮은 우선순위 태스크가 보유한 mutex 때문에 높은 우선순위 태스크가 막히고 중간 우선순위 태스크가 CPU를 차지하면 역전이 장시간 지속될 수 있음
   - 해결방안: priority inheritance나 priority ceiling을 적용하고 blocking time과 deadline miss rate로 검증함
3. 문제: 지연 원인을 평균 로그만으로 보면 sporadic latency spike를 놓쳐 실시간 결함이 숨겨질 수 있음
   - 해결방안: trace 기반 worst-case 분석을 수행하고 max latency와 percentile latency로 검증함

## Ⅶ. 적용 사례

- 모터 제어 펌웨어에서는 ISR 최소화와 우선순위 상속을 적용하고 확인 지표는 interrupt latency와 control jitter임
- 항공 전자 제어 소프트웨어에서는 ceiling protocol을 적용하고 확인 지표는 blocking upper bound와 deadline miss rate임
- 산업 로봇 태스크 스케줄링에서는 trace 분석을 운영하고 확인 지표는 max latency와 anomaly recurrence rate임

## Ⅷ. 결론

실시간 시스템의 안정성은 평균 CPU 사용률보다 인터럽트 지연 상한과 우선순위 역전 통제에 달려 있으므로, ISR와 동기화 정책을 함께 설계해야 함.
