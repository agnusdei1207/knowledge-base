---
sidebar:
  order: 211
  label: "211. 메모리 누수•힙 고갈"
  badge:
    text: "기출 · 30%"
    variant: note
title: "메모리 누수•힙 고갈 (Memory Leak Heap Exhaustion)"
date: "2026-08-31T10:48:00+09:00"
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

- 정의/개념: 사용이 완료된 객체가 GC Root에 강한 참조(Strong Reference)로 묶여 가비지 컬렉터가 회수하지 못함으로써 힙 공간이 점진적으로 고갈되어 결국 OOM(OutOfMemoryError) 시스템 중단으로 이어지는 **소프트웨어 레벨 결함 및 성능 장애 현상**
- 배경/필요성: GC 기반 언어에서도 의도치 않은 강한 참조(Static/ThreadLocal 등)로 인한 **Full GC 후 힙 기저선 지속 우상향, 메모리 고갈 및 불시의 OOM 서비스 중단 한계**

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
[누수 진단 체계]
|-- APM 계측기
|-- 덤프 수집기
|-- MAT 분석기
`-- 코드 수정 조치
```

선의 의미: 진단 체계를 이루는 정적 포함 관계

| 구성요소 | 책임 |
|:---|:---|
| APM 계측기 | 할당률과 Full GC 기저선 관측 |
| 덤프 수집기 | 객체와 참조 그래프 힙 덤프 생성 |
| MAT 분석기 | **Dominator Tree**와 GC Root 경로 분석 |
| 코드 수정 조치 | 강한 참조와 ThreadLocal 해제 |

#### 한줄 요약
- APM이 추세를, 덤프가 특정 시점의 참조 그래프를, MAT가 지배 관계를 맡으므로 증상 관측과 원인 지목이 서로 다른 도구 계층에서 이뤄진다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **메모리 누수 진단 5단계**: 부하 인가 후 Full GC $\to$ 시점별 힙 덤프 추출 $\to$ Dominator Tree 분석 $\to$ 누수 vs 정상 고점유 판정 $\to$ 수정 후 회귀 검증.

</details>

```text
[부하·Full GC]
      |
1. 힙 덤프 추출
      |
2. 도미네이터 분석
      |
3. GC Root 경로 추적
      |
4. 참조 해제
      |
5. 회귀 검증
```

- 1. 힙 덤프 추출: 시점별 객체 참조 그래프 수집
- 2. 도미네이터 분석: 상위 Retained Heap 식별
- 3. GC Root 경로 추적: 회수 방해 강한 참조 확인
- 4. 참조 해제: 컬렉션과 ThreadLocal 정리
- 5. 회귀 검증: Full GC 후 기저선 회복 확인

#### 한줄 요약
- 판정의 갈림길은 Full GC 이후 기저선이 회복되는지 여부이며, 이 기준을 건너뛰면 단순 고점유에 힙 증설이라는 헛된 비용을 쓰게 된다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **정상 고점유 vs 메모리 누수 vs 힙 고갈**: 일시적 스파이크(정상 고점유), 미해제로 인한 지속 증가(누수), 할당 한계 도달 크래시(고갈).

</details>

| 비교 항목 | 정상 고점유 (High Utilization) | 메모리 누수 (Memory Leak) | 힙 고갈 (Heap Exhaustion / OOM) |
|:---|:---|:---|:---|
| 핵심 발생 원인 | 대용량 배치 처리, 순간적 트래픽 스파이크 | Static 참조, ThreadLocal 미해제 버그 | 누적된 누수 또는 단일 거대 객체 할당 시도|
| Full GC 후 기저선 | Full GC 이후 힙 사용 기저선이 즉시 회복| Full GC 이후에도 최저 기저선이 지속 우상향| GC 수행 후에도 메모리 확보 불가로 OOM 발생|
| 시스템 영향도 | 일시적 GC 정지(Stop-the-World) 지연 | 장시간 운영 시 결국 프로세스 다운으로 귀결 | `OutOfMemoryError` 발생 및 프로세스 강제 크래시|
| 최적 해결 대책 | JVM 힙 메모리 증설(-Xmx) 및 스케일아웃 | 소스코드 내 GC Root 강한 참조 제거 픽스 | 긴급 인스턴스 재기동 및 덤프 사후 분석 |

#### 한줄 요약
- GC 후 기저선 회복은 정상 고점유, 기저선 우상향은 메모리 누수, 할당 실패 크래시는 힙 고갈을 의미한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **HeapDumpOnOutOfMemoryError**: JVM 프로세스가 OOM으로 사망하기 직전 자동으로 힙 덤프 파일을 남기도록 설정하는 필수 파라미터.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 순간 트래픽 폭주에 따른 GC 지연을 코드 누수 버그로 오판 | 실시간 초당 할당률(Allocation Rate)과 Full GC 후 기저선 추세 교차 검증 | 오진단 방지 및 트래픽/버그 원인 분리 |
| OOM 발생 후 프로세스가 즉시 종료되어 원인 분석 불가 | **HeapDumpOnOutOfMemoryError** 옵션(`-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/log`) 필수 적용 | 장애 시점 100% 사후 분석 증적 확보 |
| 스레드 풀 환경에서 ThreadLocal 미해제로 사용자 정보 유출 및 누수 | 서블릿 필터/인터셉터의 `finally` 블록에서 `ThreadLocal.remove()` 강제 호출 | 스레드 풀 오염 및 누수 원천 차단 |
| 대용량 파일 업로드 시 힙에 바이트 배열 전체를 올려 OOM 유발 | 스트리밍 방식(InputStream) 및 청크 단위 버퍼 처리 전환 | 대용량 I/O 힙 점유율 극소화 |

#### 한줄 요약
- 네 대책은 진단 근거를 미리 남기고 참조 수명을 코드에서 명시적으로 끊는 비용이며, 스트리밍 전환은 구현 복잡도를 힙 안정성과 맞바꾼다.

## Ⅶ. 결론

- 대규모 트래픽을 처리하는 엔터프라이즈 백엔드 및 컨테이너(K8s) 환경에서 예기치 않은 파드 OOMKilled 강제 종료를 방어하는 **가장 핵심적인 런타임 신뢰성 및 애플리케이션 성능 엔지니어링(APM) 역량**으로 요구되며, 실무 조치 시에는 **단순 힙 증설(-Xmx)에 의존하지 않고 Full GC 후 최저 기저선 우상향 패턴 판정, MAT 도미네이터 트리 기반 누수 객체(Retained Heap) 및 GC Root 추적, ThreadLocal의 `finally` 내 `remove()` 명시적 해제, 대용량 파일 I/O의 스트리밍(청크) 처리 전환**을 결합하여 근본적인 코드 레벨 메모리 건전성을 완성

#### 한줄 요약
- 메모리 누수와 힙 고갈은 Full GC 후 기저선 추적, 힙 덤프 Dominator 분석, 명시적 참조 해제를 통해 해결하는 핵심 시스템 성능 엔지니어링 영역이다.
