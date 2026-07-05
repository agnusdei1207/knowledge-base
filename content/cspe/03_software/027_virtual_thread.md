---
title: "가상 스레드 (Virtual Thread)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 27
---

## 핵심 인사이트 (3줄 요약)
- OS 스레드와 1:1 매핑되지 않고, JVM이 수백만 개를 가볍게 스케줄링할 수 있는 경량 사용자 스레드.
- 기존 블로킹 I/O 처리의 성능 한계와 리액티브 프로그래밍의 극악한 디버깅 난이도를 동시에 해결함.
- Thread-per-request 모델의 직관성을 유지하면서도, I/O 작업에서 최소 리소스로 최대 Throughput을 달성.
---
## Ⅰ. 개요 및 필요성
- **개요**: 자바 21(Project Loom)에서 공식 도입된 기능으로, 운영체제가 아닌 언어 런타임(JVM)이 직접 스케줄링하는 가상 스레드 모델.
- **필요성**: 기존 플랫폼 스레드는 1MB의 스택 메모리와 컨텍스트 스위칭 오버헤드로 인해 수만 개의 접속을 감당하기 어려웠음. 비동기 리액티브(WebFlux) 방식이 대안이었으나, 학습 곡선이 높고 스택 트레이스 단절로 유지보수가 어려워 동기식 코드의 회귀가 절실했음.
---
## Ⅱ. 아키텍처 및 핵심 원리
- **작동 메커니즘**:
  1. 가상 스레드는 OS 스레드(Carrier Thread) 위에서 실행됨.
  2. I/O 블로킹이 발생하면, 런타임이 `Continuation` 객체를 통해 가상 스레드의 스택 상태를 힙(Heap) 메모리에 저장(Unmount)함.
  3. 해방된 Carrier Thread는 즉시 다른 가상 스레드를 넘겨받아(Mount) 실행을 이어감.

```text
[ Virtual Thread 1 ]  [ Virtual Thread 2 ] ... [ Virtual Thread 1,000,000 ]
         | (1. I/O Block ➡️ Unmount) 
+---------------------------------------------------+
|               Continuation (Heap)                 |
+---------------------------------------------------+
|               ForkJoinPool (JVM)                  |
+---------------------------------------------------+
         | (2. Mount)
[ Carrier Thread 1 ]  [ Carrier Thread 2 ] ... (OS Threads ≈ CPU Cores)
```
---
## Ⅲ. 비교 및 연결
| 구분 | Virtual Thread (Java 21+) | Reactive Programming (WebFlux) | Platform Thread |
|---|---|---|---|
| **프로그래밍 모델** | 동기/명령형 (Imperative) | 비동기/선언형 (Declarative) | 동기/명령형 |
| **메모리 풋프린트** | 매우 작음 (가변 힙 할당) | 작음 | 매우 큼 (고정 스택 1MB) |
| **디버깅 / 추적** | 직관적 (콜 스택 완전 유지) | 복잡 (콜백 단절) | 직관적 |
| **적합한 워크로드** | 대규모 I/O Bound | 데이터 스트림 가공 및 조작 | 순수 CPU Bound |
---
## Ⅳ. 실무 적용 및 기술사 판단
- **Pinning 현상 주의**: `synchronized` 블록이나 JNI 내에서 블로킹이 발생하면 Carrier Thread 자체가 잠겨버리므로, `ReentrantLock`으로 교체해야 함.
- **메모리 폭발 경계**: 가상 스레드는 수백만 개 생성이 가능하므로 무거운 객체를 담은 `ThreadLocal` 사용 시 OOM이 발생할 수 있음. 대안으로 `Scoped Values` 활용이 필수적.
---
## Ⅴ. 기대효과 및 결론
- API Gateway, BFF, 혹은 타 서비스 연동이 잦은 MSA 환경에서 코드 가독성을 해치지 않고 엄청난 성능 향상을 가져옴.
- 리액티브로의 완전 전환이라는 패러다임에서 "필요할 때마다 스레드를 만드는" 전통적 패러다임으로의 회귀를 이끌며, 백엔드 아키텍처의 판도를 바꾸고 있음.
---
### 📌 관련 개념 맵
- 동시성 모델 ➡️ Thread-per-request ➡️ Reactive Programming ➡️ Project Loom(Virtual Thread)

### 📈 관련 키워드 및 발전 흐름도
- Platform Thread ➡️ NIO/Netty (Event Loop) ➡️ Reactive Streams (WebFlux) ➡️ Kotlin Coroutine ➡️ Virtual Thread

### 👶 어린이를 위한 3줄 비유 설명
1. 10명의 종업원(OS 스레드)이 각각 1개의 식탁만 전담하면, 손님이 밥을 먹는 동안 종업원은 그냥 서서 놀아야 해요.
2. 하지만 종업원이 요리를 주문하고(I/O), 기다리는 동안 다른 테이블로 옮겨 다니면(Virtual Thread) 10명으로도 1만 개의 식탁을 돌볼 수 있어요!
3. 그래서 종업원을 더 뽑지 않고도 엄청나게 많은 손님을 받을 수 있게 해주는 마법 같은 방법이랍니다.
