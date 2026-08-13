---
sidebar:
  order: 118
  label: "118. 람다 아키텍처 (Lambda Architecture)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "람다 아키텍처 (Lambda Architecture)"
date: "2026-08-13T22:24:00+09:00"
tags:
  - "notes-software"
weight: 118
extra:
  question_no: "118"
  source_status: "기출"
  source_history: "120회"
  priority: 50
  priority_note: "120회 기출, 배치•속도 계층 비교 기준"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **Lambda Architecture**: Nathan Marz가 제안한 데이터 처리 파이프라인 패러다임으로, 정확성을 보장하는 배치 계층(Batch Layer), 초저지연을 보장하는 속도 계층(Speed Layer), 둘을 병합해 응답하는 서비스 계층(Serving Layer) 3가지 파이프라인을 이중 병렬 구축하는 빅데이터 아키텍처.
- **Batch Layer (배치 계층)**: 전체 불변 데이터 원천(Immutable Data)을 주기로 일괄 계산하여 100% 완벽하고 정확한 Batch View를 생성하는 계층 (Hadoop, Spark).
- **Speed Layer (속도 계층 / 실시간 계층)**: 배치 계층의 처리 유예 시간(Lag) 동안 유입되는 최신 스트림 데이터를 초저지연으로 즉시 계산하여 Real-Time View를 생성하는 계층 (Kafka, Flink, Storm).
- **Serving Layer (서비스 계층)**: Batch View와 Real-Time View 결과를 상호 통합 및 중복 제거하여, 클라이언트 쿼리에 최신 합산 응답을 렌더링하는 계층 (HBase, Cassandra).

</details>

- 정의/개념: 배치•속도 뷰를 병합하는 **람다 아키텍처**
- 배경/필요성: 실시간 경로만으로는 **전체 이력 재계산•오류 정정** 제약

#### 한줄 요약

- 전체 장부와 최신분 임시 장부를 따로 만들고 조회할 때 합친다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **Immutable Raw Data (불변 원본 데이터)**: 덮어쓰기(Update)를 절대 하지 않고Append-Only 형태로 데이터 원천 보존.
- **Eventually Exact (최종 정확성)**: Speed Layer의 임시 오차를 Batch Layer의 주기적 배치 계산으로 100% 정정 보완.

</details>

- **Batch Layer + Speed Layer + Serving Layer 3대 계층 구조**
- **Immutable & Append-Only Master Dataset** 기반 전면 재계산(Re-computation) 지원
- **Dual Codebase Dual Maintenance Overhead (배치/스트림 이중 코드 유지보수 오버헤드)**

#### 한줄 요약

- 최신성을 얻는 대신 같은 계산을 두 경로에서 일치하게 유지해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **Dual Pipeline Convergence**: 동일한 비즈니스 로직을 Batch(Spark)용과 Stream(Flink)용 2가지 코드 베이스로 이중 개발하는 람다의 치명적 오버헤드.

</details>

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Lambda Architecture Pipeline                    │
├────────────────────────────────────────────────────────────────────────┤
│ New Data Stream ──► [Batch Layer (Hadoop/Spark)] ──► [Batch View]      │
│     │               (All Historical Data, Slow)           │            │
│     │                                                     ▼            │
│     └─────────────► [Speed Layer (Flink/Storm)]  ──► [Serving Layer]   │
│                     (Recent Stream Data, Fast)     (Query Merge Output)│
└────────────────────────────────────────────────────────────────────────┘
```

선의 의미: 데이터 스트림이 배치 계층과 속도 계층으로 동시 분기되어 연산된 후, 서비스 계층에서 통합 병합 조회되는 아키텍처.

| 구성요소 | 책임 |
|:---|:---|
| **원본 데이터셋** | 불변 이벤트를 재처리 가능하게 보관 |
| **배치 계층** | 전체 이력으로 배치 뷰 재계산 |
| **속도 계층** | 미반영 최신 이벤트의 실시간 뷰 생성 |
| **서비스 계층** | 배치•실시간 뷰의 시간 경계 병합 |

#### 한줄 요약

- 원본 장부, 전체 계산자, 최신 계산자, 조회 장부, 시간표로 구성된다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **Kappa Architecture**: Jay Kreps가 제안한 아키텍처로, 람다의 이중 배치/스트림 유지보수 단점을 극복하기 위해 Batch Layer를 제거하고, 오직 Stream Engine (Flink/Kafka Log Replay) 단일 파이프라인으로 전면 통일한 구조.

</details>

```text
[신규 이벤트]
      │
      ▼
1. 원본 데이터 저장
      │
  ┌───┴────────┐
  ▼            ▼
2. 전체 재계산  3. 최신 증분 계산
  │            │
  └───┬────────┘
      ▼
4. 시간 경계 병합
      │
      ▼
5. 통합 뷰 제공
```

### 동작 원리

1. **원본 데이터 저장**: 불변 이벤트를 장기 저장소에 기록
2. **전체 재계산**: 전체 이력으로 정확한 배치 뷰 생성
3. **최신 증분 계산**: 배치 미반영 구간을 실시간 처리
4. **시간 경계 병합**: 컷오프로 중복•누락 없이 뷰 결합
5. **통합 뷰 제공**: 최신성과 재계산 결과를 함께 응답

#### 한줄 요약

- 임시 장부로 최신분을 보여주다가 전체 장부가 완성되면 겹친 임시 기록을 치운다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **Single Stream Pipeline**: 카파 아키텍처는 오직 Stream Engine 단일화로 코드 중복 및 결과 불일치(Inconsistency) 문제 소멸.

</details>

| 비교 항목 | Lambda Architecture (람다) | Kappa Architecture (카파) |
|:---|:---|:---|
| **파이프라인 구조** | **이중 파이프라인 (Batch + Speed Layer)**| **단일 파이프라인 (Stream Layer Only)** |
| **코드 베이스 관리** | **이중 유지보수 오버헤드 (Spark + Flink)**| **단일 코드 베이스 (Flink / Kafka)** |
| **과거 데이터 재처리**| **Batch Layer 전면 재계산 (HDFS)** | **Kafka Log Replay 기반 스트림 재계산** |
| **결과 정합성** | 배치•스트림 로직 차이 위험 | 단일 로직이나 재생 부작용 관리 필요 |

#### 한줄 요약

- 람다는 두 장부를 만들고, 카파는 같은 처리기로 과거 기록까지 다시 읽는다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **Code Duplication Drift**: 배치 계층의 Java/Scala 코드와 속도 계층의 Stream 코드가 시간이 지남에 따라 파행되어 뷰 정합성이 깨지는 현상.

</details>

| 람다 실무 문제점 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. Dual Code Drift** | 배치/스트림 개발자가 달라 로직 불일치 | **Apache Beam / Flink Table API 통일 프레임워크 도입**|
| **2. Serving Layer Overlap**| Batch View와 Real-Time View 중복 합산 | **Time Window 경계 컷오프(Cut-off) 메커니즘 정립** |
| **3. Complex Maintenance** | 2개 분산 클러스터(Hadoop+Kafka) 운영 부담| **카파 아키텍처 (Stream Unified)로 전환 파이프라인** |

> 사례: **SKT / KT 대용량 통신 로그 처리 람다 아키텍처 및 Flink 기반 카파 전환**

#### 한줄 요약

- 두 장부의 시간 경계를 명시해야 같은 거래를 두 번 더하거나 빠뜨리지 않는다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **빅데이터 파이프라인 수립 기준(Data Pipeline Standards)**: 100% 재계산 정확성, 이중 로직 유지 비용, Flink 스트림 성숙도 및 Kappa 수용성에 의거한 체계.

</details>

- 전체 재계산이 별도 필요하면 **Lambda**, 로그 재생으로 충분하면 Kappa 선택

#### 한줄 요약

- 선택 기준은 빠른 증분 답과 정확한 전체 재계산의 운영 비용을 비교한다.
