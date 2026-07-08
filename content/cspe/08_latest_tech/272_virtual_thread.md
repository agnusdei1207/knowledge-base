---
title: "Virtual Thread 가상 스레드 (Virtual Thread)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 272
extra:
  question_no: "272"
  exam_status: "기출"
  exam_history: "138회"
  exam_note: "전망"
---

## 미리 알고가기

- Virtual Thread는 OS 스레드보다 훨씬 가볍게 생성되는 사용자 수준 스레드 모델임
- 동기식 코드를 유지하면서도 높은 동시성을 얻으려는 목적에서 주목받음
- 스케줄링은 런타임이 담당하고 실제 OS 스레드는 carrier 역할을 함

## Ⅰ. 개요

- **정의/개념**: Virtual Thread는 런타임이 관리하는 경량 사용자 수준 스레드로 블로킹 스타일 코드를 유지하면서도 대량 동시성을 낮은 메모리 비용으로 처리하게 하는 실행 모델임
- **배경/필요성**: 전통적 OS 스레드는 높은 생성 비용과 메모리 오버헤드가 있어 대규모 I O 동시성을 처리하기 어려워 경량 스레드 모델이 필요해짐

## Ⅱ. 특징

- 생성 비용과 메모리 사용량이 낮아 대량 연결 처리에 적합함
- 비동기 콜백보다 읽기 쉬운 동기식 코드 구조를 유지할 수 있음
- 블로킹 지점에서 런타임이 carrier thread를 효율적으로 재사용함
- CPU 집약 작업에는 단순히 virtual thread 수만 늘려도 효과가 제한됨

## Ⅲ. 종류 및 비교

| 판단 기준 | Virtual Thread | OS Thread | Async Event Loop |
|:---|:---|:---|:---|
| 생성 비용 | 낮음 | 높음 | 낮음 |
| 코드 가독성 | 높음 | 높음 | 중간 |
| 대규모 I O 동시성 | 높음 | 낮음 | 높음 |
| CPU 집약 작업 적합성 | 중간 | 중간 | 중간 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Virtual Thread Instance | 애플리케이션 로직을 담는 경량 실행 단위로 수많은 동시 작업을 표현함 |
| Scheduler | virtual thread를 실제 carrier thread에 매핑하고 블로킹 지점에서 다시 배치하는 런타임 스케줄러임 |
| Carrier Thread | 실제 OS 스레드로서 virtual thread의 실행을 잠시 맡아주는 하부 실행 자원임 |
| Blocking I O Adapter | 블로킹 호출이 발생할 때 carrier 점유를 최소화하도록 런타임과 연계하는 I O 계층임 |
| Monitoring Hook | 대량 동시 실행 상황에서 지연과 고정 점유 현상을 추적하는 관측 계층임 |

```text
+------------------+    +------------------+    +-----------------+
| Virtual Threads  | -> | Runtime Scheduler| -> | Carrier Threads |
+------------------+    +------------------+    +-----------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 가상 스레드 생성 | -> | 스케줄링    | -> | I O 블로킹 감지 | -> | carrier 해제 | -> | 완료 후 재개   |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **가상 스레드 생성**: 요청마다 경량 스레드를 빠르게 생성함
2. **스케줄링**: 런타임이 carrier thread에 실행을 배치함
3. **I O 블로킹 감지**: 대기 상태가 되면 실행을 분리함
4. **carrier 해제**: 다른 가상 스레드가 해당 carrier를 사용함
5. **완료 후 재개**: I O가 끝나면 가상 스레드를 다시 실행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 블로킹 코드가 많더라도 외부 라이브러리가 carrier 고정을 일으키면 기대한 동시성 향상이 제한될 수 있음
   - 해결방안: pinning analysis와 library compatibility review를 적용하고 carrier pinning rate와 concurrent request throughput으로 검증함
2. 문제: CPU 집약 작업을 무분별하게 가상 스레드에 올리면 스케줄링 이점보다 컨텍스트 전환 부담이 커질 수 있음
   - 해결방안: workload classification과 bounded executor design을 적용하고 runnable queue length와 CPU saturation efficiency로 검증함
3. 문제: 대량 가상 스레드 환경에서 기존 스레드 모니터링 방식만 쓰면 병목 원인 추적이 어려워질 수 있음
   - 해결방안: virtual thread aware observability를 적용하고 blocked thread diagnosis time과 scheduler visibility score로 검증함

## Ⅶ. 적용 사례

- 대량 I O 서버가 라이브러리 호환성 검토를 수행하며 확인 지표는 carrier pinning rate와 concurrent request throughput임
- 혼합 워크로드 플랫폼이 작업 분류 실행기를 적용하며 확인 지표는 runnable queue length와 CPU saturation efficiency임
- JVM 운영팀이 가상 스레드 관측 도구를 도입하며 확인 지표는 blocked thread diagnosis time와 scheduler visibility score임

## Ⅷ. 결론

Virtual Thread는 동기식 프로그래밍과 대규모 동시성을 동시에 잡는 유력한 모델이지만 pinning과 작업 특성 분리가 성능 실현의 핵심임.
