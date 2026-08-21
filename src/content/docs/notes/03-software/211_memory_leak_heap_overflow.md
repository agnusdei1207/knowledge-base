---
sidebar:
  order: 211
  label: "211. 메모리 누수•힙 고갈 (Memory Leak Heap Exhaustion)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "메모리 누수•힙 고갈 (Memory Leak Heap Exhaustion)"
date: "2026-08-18T05:20:00+09:00"
tags: ["notes-software"]
weight: 211
extra:
  question_no: "211"
  source_status: "기출"
  source_history: "123회"
  priority: 30
  priority_note: "누수•힙 고갈의 원인과 진단이 기존 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **메모리 누수(Memory Leak)**: 사용이 끝난 불필요한 객체가 정적(Static) 컬렉션이나 미해제 리스너에 의해 강한 참조(Strong Reference)로 묶여 있어 가비지 컬렉터(GC)가 메모리를 회수하지 못하고 점유량이 지속 증가하는 결함.
- **힙 고갈 및 OOM(Heap Exhaustion & OutOfMemoryError)**: 지속적인 누수나 급격한 대량 객체 생성으로 인해 힙(Heap) 가용 공간이 소진되어 신규 객체 할당이 실패하고 프로세스가 비정상 종료되는 장애 상태.

</details>

- 정의/개념: 가비지 컬렉션(GC) 대상 객체의 미해제 누적과 순간적 할당 폭증으로 **가용 메모리가 소진되어 프로세스가 마비되는 장애 현상**
- 배경/필요성: 정적 컬렉션 무단 참조 및 메모리 한도 초과 시 발생하는 **OutOfMemoryError(OOM), 응답 불가 랙(Lag) 및 서비스 강제 종료 위험** 직면

#### 한줄 요약

- 힙 덤프(Heap Dump) 분석과 도미네이터 트리(Dominator Tree) 역추적을 통해 숨겨진 GC Root 참조를 끊어내고 힙 고갈을 방어

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **도미네이터 트리(Dominator Tree)**: 힙 덤프 분석 도구(MAT)에서 특정 최상위 객체가 살아있음으로 인해 함께 해제되지 못하는 하위 객체들의 합산 크기(Retained Size)를 계층 구조로 시각화한 분석 기법.
- **스레드 로컬(ThreadLocal) 누수**: 톰캣 등 서블릿 컨테이너의 스레드 풀 환경에서 스레드가 반환될 때 `ThreadLocal.remove()`를 호출하지 않아 장수 스레드가 과거 요청 객체를 영구 참조하는 누수.

</details>

- Full GC 수행 이후에도 최저 메모리 기저선(Baseline)이 톱니바퀴처럼 지속 상승하는 **우상향 톱니 패턴**
- 정적 컬렉션(Static Map), 해제 누락된 리스너, ThreadLocal 잔존 데이터가 유발하는 **소프트웨어 레벨 참조 결함**
- 힙 덤프 기반으로 가장 큰 메모리를 쥐고 있는 원흉을 식별하는 **Retained Size 및 Dominator 분석**

#### 한줄 요약

- GC 이후 기준선 우상향 패턴을 감시하고 MAT 덤프 분석으로 참조 고리를 제거하여 메모리 안정성을 확보

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **메모리 진단 4대 핵심 체계**: Metrics Instrumentation(실시간 APM 계측), Dump Snapshot(힙/스레드 덤프 수집), Dominator Analysis(MAT 원인 분석), Configuration Tuning(코드 수정/힙 조정).

</details>

```text
[ 메모리 누수 및 힙 고갈 진단/트러블슈팅 아키텍처 구조도 ]

 1. [ 실시간 런타임 계측 계층 (APM: Scouter / Pinpoint / Datadog) ]
    ┌─────────────────────────────────────────────────────────────┐
    │  • 힙 메모리 점유율, GC 빈도/지연(Stop-the-World), 초당 할당률│
    └────────────────────────────┬────────────────────────────────┘
                                 │ (Full GC 후 기준선 지속 상승 감지)
                                 ▼
 2. [ 덤프 스냅샷 수집 계층 (Dump Collector: jcmd / jmap) ] ─────┐
    • OOM 발생 시 `-XX:+HeapDumpOnOutOfMemoryError` 자동 스냅샷  │
    └────────────────────────────┬────────────────────────────────┘
                                 │ (.hprof 덤프 파일 전달)
                                 ▼
 3. [ 정밀 분석 엔진 (Memory Analyzer Tool: MAT) ] ──────────────┐
    • Dominator Tree ➔ Retained Heap 80% 차지하는 객체 식별      │
    • GC Root 참조 경로 역추적 (Static List ➔ HashMap ➔ Entity)   │
    └────────────────────────────┬────────────────────────────────┘
                                 │ (원인 코드 특정 및 픽스)
                                 ▼
 4. [ 소스 수정 및 인프라 조치 (Remediation & Heap Tuning) ]
    • `collection.clear()`, `ThreadLocal.remove()` 강제 적용
    • JVM Max Heap 크기(-Xmx) 및 컨테이너 메모리 리밋 증설
```

선의 의미: 실시간 APM이 우상향 누수를 감지하면 jcmd로 힙 덤프를 추출하여 MAT에서 GC Root를 역추적하고 소스코드를 수정하는 구조.

| 구성요소 | 책임 |
|:---|:---|
| 실시간 APM 계측기 | 힙 영역별 점유율, **Full GC 수행 횟수, 초당 객체 할당률(Allocation Rate) 모니터링** |
| 덤프 스냅샷 수집기 | OOM 시점 또는 이상 징후 시점에 **전체 객체와 참조 그래프를 담은 `.hprof` 덤프 생성** |
| MAT 분석기 (Analyzer) | 덤프 파일을 파싱하여 **가장 많은 메모리를 점유한 Dominator 객체와 GC Root 경로 역추적** |
| 소스코드 수정 조치 | 정적 컬렉션 비우기, **ThreadLocal 해제, I/O 스트림 및 Native 메모리 명시적 close 처리** |

#### 한줄 요약

- APM 계측, 덤프 수집, MAT 분석기, 소스 수정 조치가 결합하여 메모리 장애를 해결

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **메모리 누수 진단 5단계 절차**: 반복 부하 후 GC 강제 $\to$ 힙 덤프 델타(Delta) 추출 $\to$ Dominator 역추적 $\to$ 누수 vs 정상 고점유 판정 $\to$ 수정 후 회귀 검증.

</details>

```text
[ 메모리 누수 및 힙 고갈 트러블슈팅 파이프라인 ]

 ┌────────────────────────────────────────┐
 │ 1. 부하 테스트 후 Full GC 강제 수행   │
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 2. 시점별 힙 덤프(Heap Dump) 스냅샷 추출│
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 3. MAT: Retained Size 상위 Dominator 역추적
 └───────────────────┬────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 4. 메모리 상태 정밀 판정 및 코드 수정 │
 ├───────────────────┬────────────────────┤
 │ 덤프 간 지속 우상향│ GC 후 바닥선 회복 │
 │ • 메모리 누수 확정│ • 정상 고점유 확정 │
 │   참조 코드 제거  │   힙 용량 증설     │
 └───────────────────┴────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────┐
 │ 5. 동일 부하 인가 후 기준선 안정 검증  │
 └────────────────────────────────────────┘
```

### 동작 원리

1. 부하 인가: JMeter로 1,000 TPS 부하를 30분간 인가한 후 Full GC를 실행하여 살아남은 객체 환경 조성.
2. 덤프 추출: 10분 간격으로 2개의 힙 덤프 파일(`dump_1.hprof`, `dump_2.hprof`)을 생성하여 MAT에 로드.
3. 도미네이터 분석: `dump_2`에서 `SessionManager.activeUserMap` 정적 객체의 Retained Heap이 1.2GB로 폭증함을 확인.
4. 원인 판정: 사용자 로그아웃 시 Map에서 제거되지 않는 버그를 특정하고, 소스코드에 `map.remove(userId)`를 추가.
5. 회귀 검증: 재배포 후 동일한 1,000 TPS 부하를 가했을 때 Full GC 이후 힙 점유율이 25% 기저선으로 정상 회복됨을 확인.

#### 한줄 요약

- 부하 인가 $\to$ 덤프 추출 $\to$ 도미네이터 분석 $\to$ 원인 판정/수정 $\to$ 회귀 검증의 5단계

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **정상 고점유 vs 메모리 누수 vs 힙 고갈**: 일시적 스파이크(정상 고점유), 미해제로 인한 지속 증가(누수), 할당 한계 도달(고갈).

</details>

| 구분 | 정상 고점유 (High Utilization) | 메모리 누수 (Memory Leak) | 힙 고갈 (Heap Exhaustion / OOM) |
|:---|:---|:---|:---|
| **적용 기준** | 대용량 배치 처리나 순간적 트래픽 스파이크 발생 시 | 버그로 인해 특정 객체 참조가 영구히 해제되지 않을 때 | 누적된 누수 또는 단일 요청의 거대 객체 할당 시도 시 |
| **핵심 특징** | **Full GC 이후 힙 사용 기저선(Baseline)이 원상 복구됨** | **Full GC 이후에도 최저 기저선이 계단식으로 지속 우상향** | **`java.lang.OutOfMemoryError` 발생 및 프로세스 크래시** |
| **한계** | 일시적 GC 정지(Stop-the-World) 지연 발생 가능 | 장시간 운영 시 결국 힙 고갈(OOM)로 귀결됨 | 서비스 전면 중단 및 즉각적인 인스턴스 재기동 필요 |

#### 한줄 요약

- GC 후 원상 복구는 정상 고점유, 기저선 우상향은 메모리 누수, 할당 실패 크래시는 힙 고갈을 의미

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **OOM Kill 방어와 덤프 자동화**: 리눅스 커널의 OOM Killer가 프로세스를 강제 종료하기 전에 JVM 옵션(`-XX:+HeapDumpOnOutOfMemoryError`)으로 분석용 증적을 자동 확보하는 통제.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 순간 트래픽 폭주에 따른 GC 지연을 코드 누수 버그로 오판 | **실시간 초당 할당률(Allocation Rate)과 Full GC 후 기저선 추세 교차 검증** | 오진단 방지 및 트래픽/버그 원인 분리 |
| OOM 발생 후 프로세스가 즉시 종료되어 원인 분석 불가 | **`-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/log` 옵션 필수 적용** | 장애 시점 100% 사후 분석 증적 확보 |
| 스레드 풀 환경에서 ThreadLocal 미해제로 사용자 정보 유출 및 누수 | **서블릿 필터/인터셉터의 `finally` 블록에서 `ThreadLocal.remove()` 강제 호출** | 스레드 풀 오염 및 누수 원천 차단 |

#### 한줄 요약

- 할당률 교차 검증, OOM 자동 덤프 설정, ThreadLocal 명시적 remove를 통해 메모리 장애를 완벽 통제

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **지속적 메모리 프로파일링(Continuous Profiling)**: 프로덕션 환경에서 eBPF 또는 JFR(Java Flight Recorder)을 통해 오버헤드 1% 미만으로 메모리 할당을 상시 추적하는 최신 엔지니어링 실천.

</details>

- **메모리 누수 및 힙 고갈** 시스템의 장기적 신뢰성을 파괴하는 치명적 런타임 장애이며, Full GC 후 기저선 회복 여부를 상시 감시하고 MAT 덤프 분석과 ThreadLocal 해제를 철저히 준수하여 무결점 무중단 서비스를 완성해야 함

#### 한줄 요약

- Full GC 후 기저선 추적과 MAT 도미네이터 분석 및 명시적 참조 해제를 통해 메모리 안정성을 완성
