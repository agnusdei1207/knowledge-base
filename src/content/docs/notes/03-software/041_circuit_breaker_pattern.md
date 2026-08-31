---
sidebar:
  order: 41
  label: "041. 서킷 브레이커 패턴"
  badge:
    text: "미출 · 50%"
    variant: note
title: "서킷 브레이커 패턴 (Circuit Breaker Pattern)"
date: "2026-08-31T10:48:00+09:00"
tags:
  - "notes-software"
weight: 41
extra:
  question_no: "041"
  source_status: "기출"
  source_history: ""
  priority: 50
  priority_note: "분산 시스템 연쇄 장애 차단 및 상태 전이"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **서킷 브레이커(Circuit Breaker)**: 원격 호출의 실패율을 감시하여 장애 발생 시 즉시 요청을 차단(Fast-Fail)하고 Fallback을 반환하는 패턴.
- **연쇄 장애(Cascading Failure)**: 단일 하위 서비스의 지연/장애가 상위 서비스들의 스레드 풀을 연쇄적으로 고갈시켜 전체 시스템이 마비되는 현상.

</details>

- 정의/개념: 원격 서비스 호출 실패율이 임계치를 초과할 때 호출을 즉시 차단하여 **연쇄 장애(Cascading Failure)** 를 방지하는 회복탄력성 패턴
- 배경/필요성: 분산 마이크로서비스 환경에서 특정 하위 서비스의 지연·장애가 상위 서비스들의 스레드 풀 및 커넥션을 연쇄적으로 고갈시켜 전체 시스템 마비(Cascading Failure)로 이어지는 취약성을 극복하고, 원격 호출 실패율과 응답 지연을 실시간 계측하여 임계치 초과 시 호출을 즉시 차단(Fast-Fail)하는 3단계 유한 상태 기계(Closed-Open-Half-Open)를 통해 **시스템 회복탄력성(Resilience)과 대체 응답(Fallback) 기반 부분 가용성을 보장**할 필요

#### 한줄 요약
- 원격 서비스 호출 실패율에 따라 연결을 자동 차단 및 복구하여 시스템 전반의 연쇄 장애를 방지한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **3단계 상태 전이**: 정상 호출(Closed) $\leftrightarrow$ 호출 차단(Open) $\leftrightarrow$ 시험 호출(Half-Open)의 순환 제어.
- **슬라이딩 윈도우(Sliding Window)**: 최근 N회 호출 또는 T초 동안의 실패율 및 지연 시간을 링버퍼에 집계하는 통계 방식.

</details>

- **Closed $\rightarrow$ Open $\rightarrow$ Half-Open** 3단계 유한 상태 기계(FSM) 기반의 자동 제어
- **슬라이딩 윈도우(Sliding Window)** 기반의 링버퍼 실패율 및 지연 시간 정밀 계측
- 장애 발생 시 **대체 응답(Fallback)** 반환을 통한 서비스 부분 가용성(Graceful Degradation) 보장

#### 한줄 요약
- 브레이커는 장애 전파를 막는 대신 정상일 수 있는 요청까지 실패시키므로, 임계치 설정이 곧 가용성과 오차단 사이의 눈금이 된다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **격벽(Bulkhead)**: 서비스별로 스레드 풀 또는 동시 실행 세마포어를 분리하여 특정 서비스 장애가 타 서비스 자원을 잠식하지 못하게 격리하는 패턴.

</details>

```text
[서킷 브레이커 인터셉터 아키텍처]
|-- 클라이언트 호출 요청
|-- 서킷 브레이커 인터셉터 (Resilience4j / Envoy)
|   |-- 슬라이딩 윈도우 계측기 (Count-based / Time-based Ring Buffer)
|   `-- 서킷 상태 머신 (State Machine)
|       |-- [Closed 상태] -> 정상 원격 마이크로서비스 호출 디스패치
|       |-- [Open 상태] -> 원격 호출 즉시 차단 (Fast-Fail) 및 Fallback 실행
|       `-- [Half-Open 상태] -> 제한된 시험 호출(Probe)로 서비스 복구 검증
`-- 격벽 격리기 (Bulkhead Thread Pool / Semaphore)
```

선의 의미: 계층 및 상태별 호출 분기 파이프라인

| 구성요소 | 책임 |
|:---|:---|
| 호출 인터셉터 | 서킷 상태에 따른 **호출 여부 결정** |
| 슬라이딩 윈도우 | 최근 호출의 **실패율 계산** |
| 상태 관리 머신 | 임계치·쿨다운 기반 **3상태 전이** |
| 대체 응답기 | 차단 시 **캐시·기본 응답 반환** |

#### 한줄 요약
- 슬라이딩 윈도우가 실패를 통계로 바꾸고 상태 머신이 그 통계를 차단 여부로 바꾸므로, 윈도우 크기와 임계치가 브레이커의 민감도를 결정한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Fast-Fail(빠른 실패)**: 서킷이 Open되었을 때 원격 네트워크 호출을 아예 시도하지 않고 즉시 예외를 던지거나 Fallback을 실행하여 스레드 낭비를 0화하는 기법.

</details>

```text
클라이언트 원격 서비스 호출 요청
        │
   현재 서킷 상태는 무엇인가?
   ┌────┴───────────────────────────┐
[Closed: 정상 운용]               [Open: 차단 상태]
원격 마이크로서비스 호출 실행        원격 호출 차단 후 Fallback 즉시 실행 (Fast-Fail)
        │                                │
실패율이 임계치(50%)를 초과했는가?    쿨다운 대기 시간(예: 10초)이 경과했는가?
   ┌────┴─────┐                          ┌────┴─────┐
  예           아니오 (Closed 유지)     예           아니오 (Open 유지)
   │                                     │
[Open 상태로 즉시 전이]            [Half-Open 상태로 전이]
                                         │
                                  제한된 N개의 시험 호출(Probe Request) 전송
                                         │
                                  시험 호출이 모두 성공했는가?
                                  ┌──────┴──────┐
                                 예              아니오
                                  │               │
                           [Closed 상태 복귀]  [Open 상태 재진입]
```

#### 한줄 요약
- Half-Open의 시험 호출 수가 회복 판정의 표본이므로, 너무 적으면 성급히 닫히고 너무 많으면 아직 장애 중인 서비스에 부하를 다시 얹는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Resilience4j vs Hystrix vs Envoy Service Mesh**: 최신 경량 자바 라이브러리, 유지보수 중단된 레거시, 인프라 계층 사이드카 프록시 비교.

</details>

| 비교 항목 | Resilience4j | Netflix Hystrix (Deprecated) | Envoy / Istio (Service Mesh) |
|:---|:---|:---|:---|
| 구현 계층 | **애플리케이션 라이브러리 (JVM)** | 애플리케이션 라이브러리 (JVM) | **인프라 사이드카 프록시 (L7)** |
| 아키텍처 방식 | 함수형 데코레이터 (경량화) | 전용 스레드 풀 격리 (무거움) | 코드 무수정 네트워크 가로채기 |
| 다국어 지원 | Java, Kotlin 전용 | Java 전용 | **모든 언어 지원 (Polyglot)** |
| 장단점 | 가볍고 모듈별 독립 선택 가능 | 유지보수 중단, 스레드 전환 오버헤드 | 언어 무관하나 1-Hop 네트워크 지연 |

#### 한줄 요약
- Java 생태계는 Resilience4j, 폴리글랏 컨테이너 인프라는 Envoy Service Mesh를 채택한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **최소 호출 표본(minimumNumberOfCalls)**: 서버 기동 직후 1~2회의 일시적 실패로 서킷이 오작동하여 열리는 것을 방지하기 위한 최소 표본 수.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 트래픽 유입 초기에 단발성 실패로 인한 오차단 | **최소 호출 표본(`minimumNumberOfCalls: 20~50`)** 설정 | 통계 신뢰도 확보 및 조기 오차단 방지 |
| 피호출 서비스 지연 시 호출자 스레드 풀 동반 고갈 | **서킷 브레이커와 격벽(Bulkhead) 패턴** 결합 | 서비스별 스레드 풀 분리로 자원 잠식 차단 |
| 서킷 개방 시 클라이언트 에러 급증 | Redis 캐시 또는 정적 기본값을 반환하는 **Fallback 구현** | 서비스 부분 가용성(Graceful Degradation) 보장 |
| 느린 응답으로 인한 서킷 미작동 | **느린 호출 임계치(`slowCallRateThreshold`)** 병행 구성 | 지연율 기반 서킷 개방으로 P99 레이턴시 방어 |

#### 한줄 요약
- 서킷 브레이커는 일부 요청을 즉시 실패시키는 대가로 호출자의 자원 고갈을 막으므로, 최소 표본수와 임계치를 잘못 잡으면 정상 트래픽까지 끊기며 Fallback 품질이 곧 사용자 체감이 된다.

## Ⅶ. 결론

- 대규모 분산 시스템 및 클라우드 네이티브 아키텍처의 **핵심 결함 내성(Fault Tolerance) 표준 패턴**으로 확립되었으며, 실무 구축 시에는 **Resilience4j(애플리케이션 계층) 또는 Envoy/Istio Service Mesh(인프라 계층)를 기반으로, 오차단을 방지하는 최소 호출 표본(minimumNumberOfCalls) 튜닝, 서비스별 자원 잠식을 막는 격벽(Bulkhead), 사용자 경험을 보존하는 캐시/기본값 Fallback 전략**을 결합하여 운영

#### 한줄 요약
- 서킷 브레이커는 분산 환경에서 장애를 빠르게 감지하고 차단하여 시스템 전체의 붕괴를 막는 핵심 안정성 패턴이다.
