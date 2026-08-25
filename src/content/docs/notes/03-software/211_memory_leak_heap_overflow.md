---
sidebar:
  order: 211
  label: "211. 메모리 누수•힙 고갈"
  badge:
    text: "기출 · 30%"
    variant: note
title: "메모리 누수•힙 고갈 (Memory Leak Heap Exhaustion)"
date: "2026-08-25T11:00:00+09:00"
tags:
  - "notes-software"
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

- **Memory Leak (메모리 누수)**: 사용 완료된 객체가 정적(Static) 컬렉션 등에 강한 참조(Strong Reference)로 묶여 GC가 회수하지 못하는 결함.
- **Heap Exhaustion (힙 고갈 / OOM)**: 힙 공간이 완전히 소진되어 신규 객체 할당 시 `java.lang.OutOfMemoryError`가 발생하는 장애.

</details>

- 정의/개념: GC 대상 객체의 참조 미해제로 인해 **가용 힙 메모리가 점진적으로 소진되어 OutOfMemoryError(OOM)가 발생하는 런타임 장애**
- 배경/필요성: 정적 컬렉션 무단 참조 및 ThreadLocal 미해제로 인한 **Stop-the-World GC 지연, OutOfMemoryError 크래시 및 전사 서비스 중단 해결 불가**

#### 한줄 요약
- 힙 덤프(Heap Dump) 분석과 Dominator Tree 역추적을 통해 GC Root 강한 참조를 제거하고 힙 안정성을 확보한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Dominator Tree (도미네이터 트리)**: 특정 부모 객체가 해제될 때 함께 수거될 수 있는 하위 객체들의 합산 메모리 크기(Retained Heap)를 시각화한 트리.
- **ThreadLocal Leak**: 스레드 풀 환경에서 재사용되는 스레드의 ThreadLocal 변수를 미해제하여 과거 사용자 데이터가 메모리에 영구 잔존하는 현상.

</details>

- Full GC 수행 이후에도 최저 메모리 기저선이 지속 상승하는 **우상향 톱니바퀴 패턴**
- Static Map, 등록 해제 누락된 리스너, ThreadLocal 미해제가 유발하는 **소프트웨어 레벨 참조 결함**
- 힙 덤프 기반으로 가장 큰 메모리를 점유한 객체를 식별하는 **Dominator Tree 역추적**

#### 한줄 요약
- 우상향 톱니 패턴 감지, 소프트웨어 참조 결함 격리, Dominator Tree 역추적을 통해 누수 원인을 규명한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **메모리 누수 진단 4대 체계**: Real-Time APM(힙 점유율 감시), Dump Snapshot Collector(hprof 덤프 수집), MAT Analyzer(Dominator 역추적), Code Remediation(참조 해제).

</details>

```text
[JVM 메모리 누수 진단 및 힙 덤프 분석 아키텍처]
|-- 1. Real-time APM Monitoring (Scouter / Pinpoint: 힙 사용량 우상향 및 Full GC 주기 감시)
`-- 2. Dump Snapshot Collector (`jcmd <pid> GC.heap_dump /tmp/dump.hprof` 스냅샷 추출)
`-- 3. Eclipse MAT Diagnostic Analyzer
    |-- Dominator Tree (Retained Heap 상위 점유 객체 식별)
    `-- Shortest Paths to GC Roots (Static Map -> ThreadLocal -> Entity 참조 경로 역추적)
`-- 4. Code Remediation & JVM Tuning (`collection.clear()`, `ThreadLocal.remove()` 강제 적용)
```

선의 의미: 계층 및 실시간 APM이 우상향 누수를 감지하면 jcmd로 힙 덤프를 추출하여 MAT에서 GC Root를 역추적하고 소스코드를 수정하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **실시간 APM 계측기** | 힙 영역별 점유율, **Full GC 수행 횟수, 초당 객체 할당률(Allocation Rate) 모니터링** | Scouter, Pinpoint |
| **덤프 스냅샷 수집기** | OOM 시점 또는 이상 징후 시점에 **전체 객체와 참조 그래프를 담은 `.hprof` 덤프 생성** | jcmd, jmap |
| **MAT 분석기 (Analyzer)**| 덤프 파일을 파싱하여 **가장 많은 메모리를 점유한 Dominator 객체와 GC Root 경로 역추적** | Eclipse MAT |
| **소스코드 수정 조치** | 정적 컬렉션 비우기, **ThreadLocal 해제, I/O 스트림 및 Native 메모리 명시적 close 처리**| 근본 원인 제거 |

#### 한줄 요약
- APM 계측기, 덤프 수집기, MAT 분석기, 소스코드 수정 조치가 결합된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **메모리 누수 진단 5단계**: 부하 인가 후 Full GC $\to$ 시점별 힙 덤프 추출 $\to$ Dominator Tree 분석 $\to$ 누수 vs 정상 고점유 판정 $\to$ 수정 후 회귀 검증.

</details>

```text
JVM 메모리 이상 징후 및 힙 고갈 트러블슈팅
        │
   1. [부하 인가 및 GC] 1,000 TPS 부하를 인가한 후 Full GC를 실행하여 불필요한 객체 정리
        │
   2. [힙 덤프 추출] 10분 간격으로 2개의 힙 덤프 파일(`dump_1.hprof`, `dump_2.hprof`) 생성
        │
   3. [도미네이터 분석] MAT에서 `SessionManager.activeUserMap` 정적 객체의 Retained Heap 폭증 확인
        │
   4. [원인 판정 및 수정] 로그아웃 시 Map 미삭제 버그를 특정하고 `map.remove(userId)` 코드 반영
        │
   5. [회귀 검증] 재배포 후 동일 부하에서 Full GC 이후 힙 점유율이 25% 기저선으로 정상 회복 확인
```

#### 한줄 요약
- 부하 인가 → 덤프 추출 → 도미네이터 분석 → 원인 판정/수정 → 회귀 검증 순으로 진행된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **정상 고점유 vs 메모리 누수 vs 힙 고갈**: 일시적 스파이크(정상 고점유), 미해제로 인한 지속 증가(누수), 할당 한계 도달 크래시(고갈).

</details>

| 비교 항목 | 정상 고점유 (High Utilization) | 메모리 누수 (Memory Leak) | 힙 고갈 (Heap Exhaustion / OOM) |
|:---|:---|:---|:---|
| 핵심 발생 원인 | **대용량 배치 처리, 순간적 트래픽 스파이크** | **Static 참조, ThreadLocal 미해제 버그** | **누적된 누수 또는 단일 거대 객체 할당 시도**|
| Full GC 후 기저선 | **Full GC 이후 힙 사용 기저선이 즉시 회복**| **Full GC 이후에도 최저 기저선이 지속 우상향**| **GC 수행 후에도 메모리 확보 불가로 OOM 발생**|
| 시스템 영향도 | 일시적 GC 정지(Stop-the-World) 지연 | 장시간 운영 시 결국 프로세스 다운으로 귀결 | **`OutOfMemoryError` 발생 및 프로세스 강제 크래시**|
| 최적 해결 대책 | JVM 힙 메모리 증설(-Xmx) 및 스케일아웃 | **소스코드 내 GC Root 강한 참조 제거 픽스** | 긴급 인스턴스 재기동 및 덤프 사후 분석 |

#### 한줄 요약
- GC 후 기저선 회복은 정상 고점유, 기저선 우상향은 메모리 누수, 할당 실패 크래시는 힙 고갈을 의미한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **HeapDumpOnOutOfMemoryError**: JVM 프로세스가 OOM으로 사망하기 직전 자동으로 힙 덤프 파일을 남기도록 설정하는 필수 파라미터.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 순간 트래픽 폭주에 따른 GC 지연을 코드 누수 버그로 오판 | **실시간 초당 할당률(Allocation Rate)과 Full GC 후 기저선 추세 교차 검증** | 오진단 방지 및 트래픽/버그 원인 분리 |
| OOM 발생 후 프로세스가 즉시 종료되어 원인 분석 불가 | **`-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/log` 옵션 필수 적용** | 장애 시점 100% 사후 분석 증적 확보 |
| 스레드 풀 환경에서 ThreadLocal 미해제로 사용자 정보 유출 및 누수 | **서블릿 필터/인터셉터의 `finally` 블록에서 `ThreadLocal.remove()` 강제 호출** | 스레드 풀 오염 및 누수 원천 차단 |
| 대용량 파일 업로드 시 힙에 바이트 배열 전체를 올려 OOM 유발 | **스트리밍 방식(InputStream) 및 청크 단위 버퍼 처리 전환** | 대용량 I/O 힙 점유율 극소화 |

#### 한줄 요약
- 할당률 교차 검증, OOM 자동 덤프 설정, ThreadLocal 명시적 remove, 스트리밍 처리로 운영한다.

## Ⅶ. 결론

- 시스템의 장기적인 신뢰성과 고가용성을 확보하기 위해 **APM을 통한 Full GC 후 힙 메모리 기저선 우상향 패턴을 상시 관측**하고, **Eclipse MAT 기반의 Dominator Tree 역추적과 ThreadLocal 명시적 해제 가이드라인을 개발 표준으로 준수**하여 무결점 엔터프라이즈 JVM 완성

#### 한줄 요약
- 메모리 누수와 힙 고갈은 Full GC 후 기저선 추적, 힙 덤프 Dominator 분석, 명시적 참조 해제를 통해 해결하는 핵심 시스템 성능 엔지니어링 영역이다.