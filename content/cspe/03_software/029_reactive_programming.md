---
title: "리액티브 프로그래밍 (Reactive Programming)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 29
---

## 핵심 인사이트 (3줄 요약)
- 시스템 내의 모든 데이터 흐름을 비동기 스트림으로 다루고, 변화를 관찰(Subscribe)하여 반응하는 선언형 프로그래밍 패러다임.
- 구독자가 감당할 수 있는 만큼만 데이터를 요청하는 배압(Backpressure)을 통해 시스템 과부하(OOM)를 원천적으로 방지.
- 장애가 전파되지 않는 복원력(Resilience)과 트래픽 급증에도 유연한 탄력성(Elasticity)을 제공하여 클라우드 네이티브 MSA의 핵심 기반이 됨.
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **Reactive Streams의 핵심 인터페이스 (표준 SPI)** | 1. `Publisher`: 무한 또는 유한한 데이터를 생성하여 스트림으로 통지 | "이 개념의 핵심" |
| **Push-Pull 하이브리드** | 데이터는 생산자로부터 밀려오지만(Push), 소비자가 허락한 양만큼만(Pull) 들어오는 형태 | "이 개념의 핵심" |
| **End-to-End Non-Blocking 제약** | WebFlux를 도입하더라도 DB 계층에서 기존 JDBC(블로킹)를 사용하면 리액티브의 이점이 완벽히 소멸함 | "화장실 잠금" |
| **디버깅 난이도 폭발** | 콜백과 스레드 스위칭으로 인해 스택 트레이스(Stack Trace)가 단절되어 에러 원인 추적이 극도로 어려움 | "접시 쌓기" |
| **리액티브 프로그래밍** | 리액티브 프로그래밍 (Reactive Programming)의 핵심 개념 | "이 개념의 핵심" |
| **Pull 기반 동적 요청** | Subscriber가 10개 처리 후 10개를 다시 `request` | "이 개념의 핵심" |
| **Drop (버리기)** | 큐 버퍼 초과 시 새로 들어오는 데이터를 무시 | "이 개념의 핵심" |

---


## Ⅰ. 개요 및 필요성
- **개요**: Reactive Manifesto(응답성, 복원력, 탄력성, 메시지 구동)의 철학을 구현하기 위해, 관찰자 패턴(Observer)과 이터레이터(Iterator) 패턴을 결합한 비동기 프로그래밍 모델.
- **필요성**: 기존 MSA의 동기 통신 연쇄 호출에서는 단일 서비스 지연이 전체 시스템의 스레드 풀을 고갈시키는 장애(Cascading Failure)로 이어지므로, 논블로킹 기반의 강력한 회복 탄력성이 요구됨.
---
## Ⅱ. 아키텍처 및 핵심 원리
- **Reactive Streams의 핵심 인터페이스 (표준 SPI)**:
  1. `Publisher`: 무한 또는 유한한 데이터를 생성하여 스트림으로 통지.
  2. `Subscriber`: 데이터를 구독하며 처리.
  3. `Subscription`: 둘 사이의 연결 고리로, `request(n)`을 통해 데이터를 조절함(Backpressure).
- **Push-Pull 하이브리드**: 데이터는 생산자로부터 밀려오지만(Push), 소비자가 허락한 양만큼만(Pull) 들어오는 형태.

```text
[ Publisher ]  ---(1) onSubscribe(Subscription)--->  [ Subscriber ]
               <---(2) request(n) (Backpressure)--- 
               ---(3) onNext(data) x n -----------> 
               ---(4) onComplete() / onError() ---> 
```
---
## Ⅲ. 비교 및 연결
| Backpressure(배압) 전략 | 동작 방식 원리 | 적용 시나리오 |
|---|---|---|
| **Pull 기반 동적 요청** | Subscriber가 10개 처리 후 10개를 다시 `request` | 일반적이고 안정적인 API 통신 |
| **Drop (버리기)** | 큐 버퍼 초과 시 새로 들어오는 데이터를 무시 | 유실되어도 무방한 로그 수집, 센서 데이터 |
| **Latest (최신 유지)** | 가장 최신 데이터만 버퍼에 남기고 덮어씀 | 주식 호가 창, 실시간 대시보드 상태 |
| **Buffer (버퍼링)** | 메모리 허용 한도까지 임시 큐에 모아둠 | 간헐적인 피크 타임 배치 작업 |
---
## Ⅳ. 실무 적용 및 기술사 판단
- **End-to-End Non-Blocking 제약**: WebFlux를 도입하더라도 DB 계층에서 기존 JDBC(블로킹)를 사용하면 리액티브의 이점이 완벽히 소멸함. 반드시 Spring Data R2DBC, MongoDB Reactive Driver 등 비동기 지원 DB 생태계로 교체해야 함.
- **디버깅 난이도 폭발**: 콜백과 스레드 스위칭으로 인해 스택 트레이스(Stack Trace)가 단절되어 에러 원인 추적이 극도로 어려움. Micrometer Observation 및 분산 트레이싱(Jaeger) 연동이 무조건 선행되어야 함.
---
## Ⅴ. 기대효과 및 결론
- 리액티브 아키텍처는 C10K 문제를 넘어 고도의 스트리밍 데이터 가공, 실시간 알림 등 복잡한 비동기 워크플로우를 함수형(선언형) 코드로 우아하게 풀어냄.
- 다만 단순 CRUD 서비스에 무분별하게 적용할 경우 과도한 학습 곡선 대비 효용이 떨어지므로, Virtual Thread 등 대안 기술과 트레이드오프를 엄밀히 저울질해야 함.
---
### 📌 관련 개념 맵
- 이벤트 루프 ➡️ Reactive Manifesto ➡️ Reactive Streams (표준 규격) ➡️ Spring WebFlux / RxJava

### 📈 관련 키워드 및 발전 흐름도
- 동기/명령형 프로그래밍 ➡️ 콜백 지옥(Callback Hell) ➡️ Promise/Future ➡️ Reactive Extensions (Rx) ➡️ Project Reactor

### 👶 어린이를 위한 3줄 비유 설명
1. 일반 정수기는 물을 틀면 내가 컵을 치울 때까지 물이 콸콸 쏟아져서 넘칠 수 있어요(메모리 초과).
2. 리액티브 정수기(Publisher)는 "물 100ml만 줘"라고 내가 컵(Subscriber) 크기만큼만 요청할 때만 물을 줍니다.
3. 이렇게 넘치지 않게 조절하는 똑똑한 약속(Backpressure) 덕분에 아무리 바빠도 시스템이 고장 나지 않아요.
