---
sidebar:
  order: 118
  label: "118. 람다 아키텍처 (Lambda Architecture)"
  badge:
    text: "기출 • 50%"
    variant: note
title: "람다 아키텍처 (Lambda Architecture)"
date: "2026-08-06T23:27:50+09:00"
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

- 정의/개념: 대용량 데이터의 100% 정확성을 담당하는 배치 계층과 실시간 최신성을 담당하는 속도 계층을 병렬 구축하고 서비스 계층에서 병합하여 응답하는 분산 아키텍처인 **Lambda Architecture**
- 배경/필요성: 실시간 스트림 처리만으로는 발생 가능한 장애 수렴 복구 및 과거 데이터 전체 재계산(Re-processing) 불가 문제 해결 요구성

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

## Ⅲ. 구조 및 구성요소 (람다 아키텍처 3대 레이어 파이프라인)

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

| 계층 (Layer) | 담당 역할 및 주요 기술 스택 | 연산 방식 및 뷰(View) 특성 |
|:---|:---|:---|
| **Batch Layer** | **Hadoop HDFS, Apache Spark (전체 데이터 재계산)** | **Batch View 생성 (100% 정확, 수시간 지연)** |
| **Speed Layer** | **Apache Kafka, Apache Flink, Storm (최신 데이터)** | **Real-Time View 생성 (Sub-second, 임시 처리)** |
| **Serving Layer** | **HBase, Cassandra, Elasticsearch (병합 조회)** | **Batch View + Real-Time View 쿼리 통합** |

#### 한줄 요약

- 원본 장부, 전체 계산자, 최신 계산자, 조회 장부, 시간표로 구성된다.

## Ⅳ. 흐름도 (람다 아키텍처 대 카파 아키텍처 비교 흐름)

<details><summary>핵심 용어</summary>

- **Kappa Architecture**: Jay Kreps가 제안한 아키텍처로, 람다의 이중 배치/스트림 유지보수 단점을 극복하기 위해 Batch Layer를 제거하고, 오직 Stream Engine (Flink/Kafka Log Replay) 단일 파이프라인으로 전면 통일한 구조.

</details>

```text
[1. Lambda Architecture]
 Raw Data ──┬──► Batch Layer (Spark) ──► Batch View ──────┐
            └──► Speed Layer (Flink) ──► Real-Time View ──┴─► Serving Layer (이중 로직)

[2. Kappa Architecture]
 Raw Data ─────► Stream Layer (Flink / Kafka Log Replay) ─────► Serving Layer (단일 로직!)
```

### 동작 원리

1. **Lambda**: 동일 로직을 Batch(Spark)용과 Stream(Flink)용 코드로 각각 이중 구현하여 서빙 레이어에서 결과 병합.
2. **Kappa**: Batch Layer를 전면 폐기하고, Kafka Log Replay 기능으로 과거 스트림 데이터를 재계산하여 **단일 코드베이스로 전체 파이프라인 통합**.

#### 한줄 요약

- 임시 장부로 최신분을 보여주다가 전체 장부가 완성되면 겹친 임시 기록을 치운다.

## Ⅴ. 종류 및 비교 (람다 아키텍처 대 카파 아키텍처)

<details><summary>핵심 용어</summary>

- **Single Stream Pipeline**: 카파 아키텍처는 오직 Stream Engine 단일화로 코드 중복 및 결과 불일치(Inconsistency) 문제 소멸.

</details>

| 비교 항목 | Lambda Architecture (람다) | Kappa Architecture (카파) |
|:---|:---|:---|
| **파이프라인 구조** | **이중 파이프라인 (Batch + Speed Layer)**| **단일 파이프라인 (Stream Layer Only)** |
| **코드 베이스 관리** | **이중 유지보수 오버헤드 (Spark + Flink)**| **단일 코드 베이스 (Flink / Kafka)** |
| **과거 데이터 재처리**| **Batch Layer 전면 재계산 (HDFS)** | **Kafka Log Replay 기반 스트림 재계산** |
| **결과 정합성** | 배치-스트림 간 로직 미세 차이 위험 | **100% 동일 로직 보장 (정합성 완벽)** |

#### 한줄 요약

- 람다는 두 장부를 만들고, 카파는 같은 처리기로 과거 기록까지 다시 읽는다.

## Ⅵ. 실무 고려사항 및 대책 (람다 아키텍처 실무 한계 해결)

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

- **빅데이터 파이프라인 수립 기준**에 따라 차세대 실시간 파이프라인 구축 시 **Flink 기반 Kappa Architecture** 우선 채택

#### 한줄 요약

- 선택 기준은 빠른 증분 답과 정확한 전체 재계산의 운영 비용을 비교한다.
